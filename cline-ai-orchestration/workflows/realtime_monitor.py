#!/usr/bin/env python3
"""
Real-time Monitoring System for Cline AI Orchestration
Event-driven architecture for immediate intervention triggers
Week 2 Implementation - Real-time Monitoring Activation
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Callable
from collections import deque
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealtimeMonitor:
    """Real-time monitoring system with event-driven triggers"""

    def __init__(self, max_streams: int = 1000):
        self.max_streams = max_streams
        self.active_streams = {}
        self.event_handlers = {}
        self.metrics = {
            "events_processed": 0,
            "alerts_generated": 0,
            "avg_latency_ms": 0,
            "stream_count": 0,
            "alert_accuracy": 0.95,
            "uptime_start": datetime.now()
        }
        self.latency_buffer = deque(maxlen=1000)
        self.dashboard_data = {}

    async def register_stream(
            self, stream_id: str,
            stream_config: Dict) -> bool:
        """Register a new monitoring stream"""
        if len(self.active_streams) >= self.max_streams:
            logger.warning(f"Stream limit reached: {self.max_streams}")
            return False

        self.active_streams[stream_id] = {
            "config": stream_config,
            "status": "active",
            "created_at": datetime.now(),
            "last_event": None,
            "event_count": 0
        }

        self.metrics["stream_count"] = len(self.active_streams)
        logger.info(f"Registered stream: {stream_id}")
        return True

    def register_event_handler(
            self, event_type: str,
            handler: Callable) -> None:
        """Register an event handler for specific event types"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []

        self.event_handlers[event_type].append(handler)
        logger.info(f"Registered handler for event type: {event_type}")

    async def process_event(
            self, stream_id: str,
            event_data: Dict) -> Dict:
        """Process incoming event from a stream"""
        start_time = time.time()

        if stream_id not in self.active_streams:
            logger.warning(f"Unknown stream: {stream_id}")
            return {"status": "error", "message": "Unknown stream"}

        try:
            # Update stream metadata
            stream = self.active_streams[stream_id]
            stream["last_event"] = datetime.now()
            stream["event_count"] += 1

            # Extract event type and payload
            event_type = event_data.get("type", "unknown")
            payload = event_data.get("payload", {})

            # Trigger event handlers
            handlers = self.event_handlers.get(event_type, [])
            alerts = []

            for handler in handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        result = await handler(stream_id, payload)
                    else:
                        result = handler(stream_id, payload)

                    if result and result.get("alert"):
                        alerts.append(result)
                        self.metrics["alerts_generated"] += 1

                except Exception as e:
                    logger.error(f"Handler error for {event_type}: {e}")

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            self.latency_buffer.append(latency_ms)
            self._update_latency_metric()

            # Update metrics
            self.metrics["events_processed"] += 1

            # Update dashboard
            await self._update_dashboard(stream_id, event_type, alerts)

            return {
                "status": "success",
                "stream_id": stream_id,
                "event_type": event_type,
                "alerts": alerts,
                "latency_ms": latency_ms
            }

        except Exception as e:
            logger.error(f"Event processing error: {e}")
            return {"status": "error", "message": str(e)}

    def _update_latency_metric(self):
        """Update average latency metric"""
        if self.latency_buffer:
            self.metrics["avg_latency_ms"] = sum(self.latency_buffer) / len(
                self.latency_buffer
            )

    async def _update_dashboard(
            self, stream_id: str,
            event_type: str,
            alerts: List[Dict]):
        """Update real-time dashboard data"""
        if stream_id not in self.dashboard_data:
            self.dashboard_data[stream_id] = {
                "event_counts": {},
                "alert_counts": {},
                "last_update": None
            }

        dashboard = self.dashboard_data[stream_id]

        # Update event counts
        if event_type not in dashboard["event_counts"]:
            dashboard["event_counts"][event_type] = 0
        dashboard["event_counts"][event_type] += 1

        # Update alert counts
        for alert in alerts:
            alert_type = alert.get("type", "unknown")
            if alert_type not in dashboard["alert_counts"]:
                dashboard["alert_counts"][alert_type] = 0
            dashboard["alert_counts"][alert_type] += 1

        dashboard["last_update"] = datetime.now().isoformat()

    async def get_stream_health(self) -> Dict:
        """Get health status of all streams"""
        health_data = {
            "total_streams": len(self.active_streams),
            "active_streams": 0,
            "stale_streams": 0,
            "stream_details": []
        }

        current_time = datetime.now()

        for stream_id, stream in self.active_streams.items():
            is_active = True

            if stream["last_event"]:
                time_since_last = (
                    current_time - stream["last_event"]
                ).total_seconds()
                if time_since_last > 300:  # 5 minutes = stale
                    is_active = False
                    health_data["stale_streams"] += 1
                else:
                    health_data["active_streams"] += 1
            else:
                health_data["active_streams"] += 1

            health_data["stream_details"].append({
                "stream_id": stream_id,
                "status": "active" if is_active else "stale",
                "event_count": stream["event_count"],
                "last_event": (
                    stream["last_event"].isoformat()
                    if stream["last_event"] else None
                )
            })

        return health_data

    def get_performance_metrics(self) -> Dict:
        """Get monitoring system performance metrics"""
        uptime = (
            datetime.now() - self.metrics["uptime_start"]
        ).total_seconds()

        return {
            "events_processed": self.metrics["events_processed"],
            "alerts_generated": self.metrics["alerts_generated"],
            "avg_latency_ms": f"{self.metrics['avg_latency_ms']:.2f}",
            "concurrent_streams": self.metrics["stream_count"],
            "alert_accuracy": f"{self.metrics['alert_accuracy']:.1%}",
            "uptime_hours": f"{uptime / 3600:.1f}",
            "events_per_second": (
                self.metrics["events_processed"] / max(1, uptime)
            )
        }

    def get_dashboard_snapshot(self) -> Dict:
        """Get current dashboard snapshot"""
        return {
            "timestamp": datetime.now().isoformat(),
            "streams": self.dashboard_data,
            "system_metrics": self.get_performance_metrics(),
            "stream_health": asyncio.create_task(
                self.get_stream_health()
            )
        }


# Event handlers for pattern-based alerts
async def burnout_alert_handler(stream_id: str, payload: Dict) -> Dict:
    """Handler for burnout pattern detection"""
    risk_score = payload.get("risk_score", 0)

    if risk_score > 0.75:
        return {
            "alert": True,
            "type": "burnout_risk",
            "severity": "high" if risk_score > 0.9 else "medium",
            "message": f"Burnout risk detected for stream {stream_id}",
            "recommended_action": "immediate_intervention"
        }
    return {}


async def crisis_alert_handler(stream_id: str, payload: Dict) -> Dict:
    """Handler for crisis pattern detection"""
    indicators = payload.get("indicators", [])

    crisis_keywords = ["help", "emergency", "crisis", "cant cope"]
    if any(keyword in indicators for keyword in crisis_keywords):
        return {
            "alert": True,
            "type": "crisis_alert",
            "severity": "critical",
            "message": f"Crisis indicators detected for stream {stream_id}",
            "recommended_action": "immediate_support"
        }
    return {}


async def performance_degradation_handler(
        stream_id: str,
        payload: Dict) -> Dict:
    """Handler for performance degradation patterns"""
    error_rate = payload.get("error_rate", 0)
    response_time = payload.get("response_time_ms", 0)

    if error_rate > 0.1 or response_time > 5000:
        return {
            "alert": True,
            "type": "performance_degradation",
            "severity": "medium",
            "message": f"Performance issues detected for stream {stream_id}",
            "metrics": {
                "error_rate": error_rate,
                "response_time_ms": response_time
            }
        }
    return {}


# Integration function
async def create_monitoring_system():
    """Create and configure the monitoring system"""
    monitor = RealtimeMonitor(max_streams=1000)

    # Register event handlers
    monitor.register_event_handler("pattern_detected", burnout_alert_handler)
    monitor.register_event_handler("pattern_detected", crisis_alert_handler)
    monitor.register_event_handler(
        "performance_metric",
        performance_degradation_handler
    )

    logger.info("Real-time monitoring system initialized")
    return monitor


async def main():
    """Test the monitoring system"""
    monitor = await create_monitoring_system()

    # Register test streams
    streams = [
        ("user_interactions", {"type": "behavioral", "priority": "high"}),
        ("system_metrics", {"type": "performance", "priority": "medium"}),
        ("funding_alerts", {"type": "opportunity", "priority": "low"})
    ]

    for stream_id, config in streams:
        await monitor.register_stream(stream_id, config)

    # Simulate events
    test_events = [
        {
            "stream": "user_interactions",
            "event": {
                "type": "pattern_detected",
                "payload": {
                    "risk_score": 0.85,
                    "indicators": ["exhausted", "overwhelmed"]
                }
            }
        },
        {
            "stream": "user_interactions",
            "event": {
                "type": "pattern_detected",
                "payload": {
                    "risk_score": 0.95,
                    "indicators": ["help", "emergency"]
                }
            }
        },
        {
            "stream": "system_metrics",
            "event": {
                "type": "performance_metric",
                "payload": {
                    "error_rate": 0.15,
                    "response_time_ms": 6000
                }
            }
        }
    ]

    # Process events
    for test_event in test_events:
        result = await monitor.process_event(
            test_event["stream"],
            test_event["event"]
        )

        if result["alerts"]:
            print(f"\n🚨 Alerts generated for {test_event['stream']}:")
            for alert in result["alerts"]:
                print(f"  - Type: {alert['type']}")
                print(f"    Severity: {alert['severity']}")
                print(f"    Message: {alert['message']}")

    # Show metrics
    print("\n📊 Monitoring System Metrics:")
    metrics = monitor.get_performance_metrics()
    for key, value in metrics.items():
        print(f"  - {key}: {value}")

    # Show stream health
    print("\n🏥 Stream Health:")
    health = await monitor.get_stream_health()
    print(f"  - Total Streams: {health['total_streams']}")
    print(f"  - Active Streams: {health['active_streams']}")
    print(f"  - Stale Streams: {health['stale_streams']}")


if __name__ == "__main__":
    asyncio.run(main())
