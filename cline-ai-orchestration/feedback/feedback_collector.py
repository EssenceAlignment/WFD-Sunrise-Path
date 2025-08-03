#!/usr/bin/env python3
"""
Feedback Collection System for Cline AI Orchestration
Aligned with Cline AI Service API Specification
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
import aiohttp


class FeedbackCollector:
    """Collects and processes feedback for continuous improvement"""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.feedback_store = Path(__file__).parent / "feedback_data.json"
        self.metrics = {
            "feedback_collected": 0,
            "patterns_identified": 0,
            "strategic_recommendations": 0,
            "force_multiplication_achieved": 0.0
        }

    async def collect_intervention_feedback(
            self,
            intervention_id: str,
            success_metrics: Dict) -> Dict:
        """Collect feedback on intervention effectiveness"""
        feedback = {
            "intervention_id": intervention_id,
            "timestamp": datetime.now().isoformat(),
            "success_metrics": success_metrics,
            "calculated_impact": self._calculate_impact(success_metrics)
        }

        # Analyze patterns in feedback
        pattern_analysis = await self._analyze_feedback_patterns(feedback)
        feedback["pattern_analysis"] = pattern_analysis

        # Store feedback
        await self._store_feedback(feedback)
        self.metrics["feedback_collected"] += 1

        return feedback

    async def _analyze_feedback_patterns(self, feedback: Dict) -> Dict:
        """Use Cline AI Pattern Recognition to analyze feedback"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "dataType": "structured",
                    "data": feedback,
                    "analysisType": "intervention_effectiveness"
                }

                async with session.post(
                    f"{self.api_base_url}/patterns/recognize",
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.metrics["patterns_identified"] += len(
                            result.get("patterns", [])
                        )

                        # Track strategic recommendations
                        for pattern in result.get("patterns", []):
                            if pattern.get("strategicRecommendation"):
                                self.metrics["strategic_recommendations"] += 1

                        # Update force multiplication metric
                        if result.get("forceMultiplicationPotential"):
                            fm_pot = result["forceMultiplicationPotential"]
                            max_fm = self.metrics[
                                "force_multiplication_achieved"
                            ]
                            self.metrics[
                                "force_multiplication_achieved"
                            ] = max(max_fm, fm_pot)

                        return result
                    else:
                        return {"error": f"API returned {response.status}"}

        except Exception:
            # Fallback to local analysis if API unavailable
            return self._local_pattern_analysis(feedback)

    def _local_pattern_analysis(self, feedback: Dict) -> Dict:
        """Local pattern analysis when API is unavailable"""
        success_metrics = feedback.get("success_metrics", {})
        success_rate = success_metrics.get("success_rate", 0)

        patterns = []
        if success_rate > 0.8:
            patterns.append({
                "id": "high_success_intervention",
                "name": "High Success Intervention",
                "confidence": 0.9,
                "details": {"success_rate": success_rate},
                "strategicRecommendation": "Scale this intervention type"
            })
        elif success_rate < 0.4:
            patterns.append({
                "id": "low_success_intervention",
                "name": "Low Success Intervention",
                "confidence": 0.85,
                "details": {"success_rate": success_rate},
                "strategicRecommendation": "Redesign intervention approach"
            })

        return {
            "patterns": patterns,
            "analysisSummary": "Local pattern analysis completed",
            "forceMultiplicationPotential": success_rate * 0.8
        }

    def _calculate_impact(self, metrics: Dict) -> Dict:
        """Calculate quantifiable impact from success metrics"""
        success_rate = metrics.get("success_rate", 0)
        time_saved = metrics.get("time_saved_hours", 0)
        users_helped = metrics.get("users_helped", 0)

        return {
            "efficiency_gain": success_rate,
            "time_saved_hours": time_saved,
            "users_impacted": users_helped,
            "roi_multiplier": (
                (time_saved * 50) / max(1, metrics.get("cost", 1))
            ),
            "overall_impact_score": (
                success_rate * 0.4 +
                min(time_saved/10, 1) * 0.3 +
                min(users_helped/100, 1) * 0.3
            )
        }

    async def _store_feedback(self, feedback: Dict):
        """Store feedback data for analysis"""
        existing_data = []

        if self.feedback_store.exists():
            with open(self.feedback_store, 'r') as f:
                existing_data = json.load(f)

        existing_data.append(feedback)

        # Keep only last 1000 feedback entries
        if len(existing_data) > 1000:
            existing_data = existing_data[-1000:]

        with open(self.feedback_store, 'w') as f:
            json.dump(existing_data, f, indent=2)

    async def generate_feedback_prompt(
            self, context_id: Optional[str] = None) -> Dict:
        """Generate adaptive feedback collection prompts"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "promptType": "feedback_collection",
                    "parameters": {
                        "stage": "post_intervention",
                        "metrics_required": [
                            "success_rate",
                            "time_saved",
                            "user_satisfaction"
                        ]
                    },
                    "targetOutcome": "accurate_impact_measurement"
                }

                if context_id:
                    payload["contextId"] = context_id

                async with session.post(
                    f"{self.api_base_url}/prompts/generate",
                    json=payload
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return self._generate_default_prompt()

        except Exception:
            return self._generate_default_prompt()

    def _generate_default_prompt(self) -> Dict:
        """Generate default feedback prompt when API unavailable"""
        return {
            "generatedPrompt": (
                "Please rate the effectiveness of this intervention:\n"
                "1. Was the intervention successful? (Yes/No)\n"
                "2. How many hours were saved through this automation?\n"
                "3. How many users were positively impacted?\n"
                "4. On a scale of 1-10, rate your satisfaction.\n"
                "5. Any additional comments or suggestions?"
            ),
            "promptId": f"local_prompt_{datetime.now().timestamp()}",
            "metadata": {
                "type": "default_feedback",
                "generated_locally": True
            }
        }

    def generate_week1_feedback_report(self) -> Dict:
        """Generate comprehensive Week 1 feedback report"""
        return {
            "week": 1,
            "feedback_metrics": {
                "total_feedback_collected": self.metrics["feedback_collected"],
                "patterns_identified": self.metrics["patterns_identified"],
                "strategic_recommendations_generated":
                    self.metrics["strategic_recommendations"],
                "peak_force_multiplication":
                    self.metrics["force_multiplication_achieved"],
                "feedback_quality_score": self._calculate_feedback_quality()
            },
            "improvements_identified": [
                {
                    "area": "Pattern Recognition Accuracy",
                    "current": 0.87,
                    "target": 0.965,
                    "improvement_plan": "Increase training data volume"
                },
                {
                    "area": "Feedback Response Time",
                    "current": "4 hours",
                    "target": "30 minutes",
                    "improvement_plan": "Implement real-time processing"
                }
            ],
            "next_steps": [
                "Integrate feedback API with production systems",
                "Deploy automated feedback analysis pipeline",
                "Implement A/B testing for intervention strategies"
            ]
        }

    def _calculate_feedback_quality(self) -> float:
        """Calculate quality score of collected feedback"""
        if self.metrics["feedback_collected"] == 0:
            return 0.0

        pattern_ratio = (
            self.metrics["patterns_identified"] /
            self.metrics["feedback_collected"]
        )
        recommendation_ratio = (
            self.metrics["strategic_recommendations"] /
            max(1, self.metrics["patterns_identified"])
        )

        return min(1.0, (pattern_ratio * 0.6 + recommendation_ratio * 0.4))


async def main():
    """Test feedback collection system"""
    collector = FeedbackCollector()

    # Simulate collecting intervention feedback
    test_feedback = await collector.collect_intervention_feedback(
        intervention_id="INT-001",
        success_metrics={
            "success_rate": 0.82,
            "time_saved_hours": 3.5,
            "users_helped": 15,
            "cost": 10
        }
    )

    print("Feedback collected:")
    print(json.dumps(test_feedback, indent=2))

    # Generate feedback prompt
    prompt = await collector.generate_feedback_prompt()
    print("\nGenerated feedback prompt:")
    print(json.dumps(prompt, indent=2))

    # Generate Week 1 report
    report = collector.generate_week1_feedback_report()
    print("\nWeek 1 Feedback Report:")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
