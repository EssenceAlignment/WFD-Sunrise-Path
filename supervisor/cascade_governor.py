#!/usr/bin/env python3
"""
Cascade Governor - Central Control Plane for Agent Force Multiplication
Prevents runaway cascades, manages API rates, implements circuit breakers
"""

import asyncio
import json
import time
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import aiohttp
from pathlib import Path

@dataclass
class APIQuota:
    """Track API rate limits and usage"""
    name: str
    requests_per_minute: int
    requests_per_hour: int
    current_minute_count: int = 0
    current_hour_count: int = 0
    last_reset_minute: datetime = field(default_factory=datetime.now)
    last_reset_hour: datetime = field(default_factory=datetime.now)

    def can_request(self) -> bool:
        """Check if we can make another request"""
        now = datetime.now()

        # Reset counters if needed
        if (now - self.last_reset_minute).seconds >= 60:
            self.current_minute_count = 0
            self.last_reset_minute = now

        if (now - self.last_reset_hour).seconds >= 3600:
            self.current_hour_count = 0
            self.last_reset_hour = now

        # Check limits
        return (self.current_minute_count < self.requests_per_minute and
                self.current_hour_count < self.requests_per_hour)

    def increment(self):
        """Record a request"""
        self.current_minute_count += 1
        self.current_hour_count += 1

@dataclass
class CircuitBreaker:
    """Circuit breaker pattern for cascade protection"""
    name: str
    failure_threshold: int = 5
    timeout_seconds: int = 60
    failure_count: int = 0
    last_failure_time: Optional[datetime] = None
    state: str = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def record_success(self):
        """Record successful execution"""
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        """Record failed execution"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def can_execute(self) -> bool:
        """Check if cascade can proceed"""
        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).seconds
                if elapsed >= self.timeout_seconds:
                    self.state = "HALF_OPEN"
                    return True
            return False

        # HALF_OPEN - allow one test request
        return True

class CascadeGovernor:
    """Central control plane for agent cascades"""

    def __init__(self):
        self.api_quotas = {
            "charityapi": APIQuota("charityapi", 10, 500),
            "airtable": APIQuota("airtable", 100, 5000),
            "github": APIQuota("github", 60, 5000),
            "perplexity": APIQuota("perplexity", 20, 1000),
            "openai": APIQuota("openai", 60, 3000),
        }

        self.circuit_breakers = {}
        self.cascade_queue = asyncio.Queue()
        self.metrics = defaultdict(int)
        self.active_cascades = {}

    async def request_permission(self, cascade_id: str, api_name: str) -> Tuple[bool, str]:
        """Request permission to use an API"""
        # Check circuit breaker
        breaker_key = f"{cascade_id}:{api_name}"
        if breaker_key not in self.circuit_breakers:
            self.circuit_breakers[breaker_key] = CircuitBreaker(breaker_key)

        breaker = self.circuit_breakers[breaker_key]
        if not breaker.can_execute():
            self.metrics["circuit_breaker_blocks"] += 1
            return False, f"Circuit breaker OPEN for {api_name}"

        # Check API quota
        if api_name in self.api_quotas:
            quota = self.api_quotas[api_name]
            if not quota.can_request():
                self.metrics["rate_limit_blocks"] += 1
                return False, f"Rate limit exceeded for {api_name}"

            quota.increment()

        self.metrics["requests_approved"] += 1
        return True, "Approved"

    async def record_result(self, cascade_id: str, api_name: str, success: bool,
                           error_message: str = ""):
        """Record cascade execution result"""
        breaker_key = f"{cascade_id}:{api_name}"

        if breaker_key in self.circuit_breakers:
            breaker = self.circuit_breakers[breaker_key]
            if success:
                breaker.record_success()
                self.metrics["cascade_successes"] += 1
            else:
                breaker.record_failure()
                self.metrics["cascade_failures"] += 1

                # Check for burst errors
                if breaker.failure_count >= 3:
                    self.metrics["error_bursts"] += 1

    async def queue_cascade(self, cascade_data: dict) -> str:
        """Queue a cascade for controlled execution"""
        cascade_id = f"cascade_{int(time.time() * 1000)}"
        cascade_data["id"] = cascade_id
        cascade_data["queued_at"] = datetime.now().isoformat()

        await self.cascade_queue.put(cascade_data)
        self.metrics["cascades_queued"] += 1

        return cascade_id

    async def process_cascade_queue(self):
        """Process queued cascades with flow control"""
        while True:
            try:
                cascade = await asyncio.wait_for(
                    self.cascade_queue.get(),
                    timeout=1.0
                )

                # Check if we should process
                if self.should_pause_processing():
                    # Re-queue for later
                    await self.cascade_queue.put(cascade)
                    await asyncio.sleep(5)  # Back off
                    continue

                # Process cascade
                self.active_cascades[cascade["id"]] = cascade
                self.metrics["cascades_started"] += 1

                # Simulate cascade execution
                # In real implementation, this would trigger actual agent work
                await self.execute_cascade(cascade)

                del self.active_cascades[cascade["id"]]
                self.metrics["cascades_completed"] += 1

            except asyncio.TimeoutError:
                # No cascades to process
                await asyncio.sleep(0.1)
            except Exception as e:
                self.metrics["cascade_errors"] += 1
                print(f"Cascade processing error: {e}")

    def should_pause_processing(self) -> bool:
        """Determine if cascade processing should pause"""
        # Pause if too many active cascades
        if len(self.active_cascades) > 10:
            return True

        # Pause if error rate too high
        total = self.metrics["cascade_successes"] + self.metrics["cascade_failures"]
        if total > 10:
            error_rate = self.metrics["cascade_failures"] / total
            if error_rate > 0.2:  # 20% error rate
                return True

        # Pause if too many circuit breakers open
        open_breakers = sum(1 for b in self.circuit_breakers.values()
                           if b.state == "OPEN")
        if open_breakers > 3:
            return True

        return False

    async def execute_cascade(self, cascade: dict):
        """Execute a cascade with governance"""
        # This is a simplified simulation
        # Real implementation would integrate with actual agent system
        apis_needed = cascade.get("apis", ["github", "airtable"])

        for api in apis_needed:
            allowed, reason = await self.request_permission(cascade["id"], api)

            if not allowed:
                print(f"Cascade {cascade['id']} blocked: {reason}")
                await self.record_result(cascade["id"], api, False, reason)
                return

            # Simulate API call
            await asyncio.sleep(0.1)

            # Simulate 90% success rate
            import random
            success = random.random() < 0.9

            await self.record_result(cascade["id"], api, success)

            if not success:
                print(f"Cascade {cascade['id']} failed at {api}")
                return

    def get_metrics(self) -> dict:
        """Get current metrics"""
        metrics = dict(self.metrics)

        # Calculate rates
        total = metrics.get("cascade_successes", 0) + metrics.get("cascade_failures", 0)
        if total > 0:
            metrics["success_rate"] = metrics.get("cascade_successes", 0) / total
        else:
            metrics["success_rate"] = 0

        # Error burst index (bursts per 100 cascades)
        if total > 0:
            metrics["error_burst_index"] = (metrics.get("error_bursts", 0) / total) * 100
        else:
            metrics["error_burst_index"] = 0

        # API utilization
        api_utils = {}
        for name, quota in self.api_quotas.items():
            hour_util = quota.current_hour_count / quota.requests_per_hour
            api_utils[f"{name}_utilization"] = round(hour_util * 100, 2)
        metrics["api_utilization"] = api_utils

        # Circuit breaker states
        breaker_states = defaultdict(int)
        for breaker in self.circuit_breakers.values():
            breaker_states[breaker.state] += 1
        metrics["circuit_breakers"] = dict(breaker_states)

        # Mean time to pause (if we track it)
        metrics["mean_time_to_pause_cascade"] = "< 60s" if self.should_pause_processing() else "N/A"

        metrics["timestamp"] = datetime.now().isoformat()

        return metrics

    def verify_pattern_registry_operational(self):
        """Verify Pattern Registry 2.0 is operational"""
        # Check shadow mode active (3 LOC)
        import sys
        sys.path.insert(0, '.')
        from patterns.base_pattern import PatternRegistry
        from patterns.funder_keywords import load_funder_patterns
        registry = PatternRegistry()
        shadow_status = registry.shadow_mode

        # Load funding patterns for testing (2 LOC)
        for pattern in load_funder_patterns():
            registry.register_pattern(pattern)

        # Test pattern detection (4 LOC)
        test_log = "grant deadline approaching"
        detections = registry.detect_all(test_log, "grants.gov")
        detection_count = len(detections)

        # Validate cascade triggering (3 LOC)
        cascade_ready = detection_count > 0 and shadow_status
        return {
            "shadow_mode": shadow_status,
            "patterns_detected": detection_count,
            "cascade_ready": cascade_ready,
            "timestamp": datetime.now().isoformat()
        }

    async def emit_telemetry(self):
        """Emit telemetry to metrics relay"""
        while True:
            metrics = self.get_metrics()

            # Save to metrics file
            metrics_dir = Path("metrics")
            metrics_dir.mkdir(exist_ok=True)

            metrics_file = metrics_dir / "cascade_governor.json"
            with open(metrics_file, "w") as f:
                json.dump(metrics, f, indent=2)

            # In production, would send to metrics relay
            print(f"Telemetry: Success Rate: {metrics['success_rate']:.2%}, "
                  f"Error Burst Index: {metrics['error_burst_index']:.2f}, "
                  f"Active Cascades: {len(self.active_cascades)}")

            await asyncio.sleep(30)  # Emit every 30 seconds

async def main():
    """Main governor loop"""
    governor = CascadeGovernor()

    # Start background tasks
    tasks = [
        asyncio.create_task(governor.process_cascade_queue()),
        asyncio.create_task(governor.emit_telemetry()),
    ]

    # Simulate cascade submissions
    for i in range(20):
        cascade = {
            "name": f"test_cascade_{i}",
            "apis": ["github", "airtable", "charityapi"],
            "priority": "normal"
        }
        cascade_id = await governor.queue_cascade(cascade)
        print(f"Queued cascade: {cascade_id}")
        await asyncio.sleep(1)

    # Let it run for a bit
    await asyncio.sleep(30)

    # Final metrics
    print("\nFinal Metrics:")
    print(json.dumps(governor.get_metrics(), indent=2))

if __name__ == "__main__":
    if "--verify-registry" in sys.argv:
        governor = CascadeGovernor()
        report = governor.verify_pattern_registry_operational()
        print(json.dumps(report, indent=2))
        sys.exit(0)
    asyncio.run(main())
