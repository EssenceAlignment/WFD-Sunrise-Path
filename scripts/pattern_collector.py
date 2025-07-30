#!/usr/bin/env python3
"""
Pattern-Insight Engine - Quantum Force Multiplier v3.5
Discovers hidden opportunities through continuous digital phenotyping
"""

import json
import time
import hashlib
import csv
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Import ML libraries (will need to be installed)
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import DBSCAN
    from sklearn.metrics import silhouette_score
except ImportError:
    print("⚠️ ML libraries not installed. Run:")
    print("pip install sentence-transformers scikit-learn")
    exit(1)

class PatternInsightEngine:
    """Discovers patterns and surfaces hidden opportunities"""

    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")
        self.data_sources = {
            "chat_logs": Path("chat_logs"),
            "commit_history": Path(".git/logs"),
            "calendar": Path("calendar_events.ics"),
            "environment": Path("environmental_sensors.json")
        }
        self.vector_db_path = Path("./vector_db/patterns")
        self.vector_db_path.mkdir(parents=True, exist_ok=True)

    def collect_texts(self) -> List[str]:
        """Collect texts from all data sources"""
        texts = []

        # Chat logs
        if self.data_sources["chat_logs"].exists():
            for log_file in self.data_sources["chat_logs"].glob("*.md"):
                try:
                    content = log_file.read_text(encoding='utf-8')
                    texts.append(f"[CHAT] {content[:500]}")
                except Exception as e:
                    print(f"Error reading {log_file}: {e}")

        # Recent commit messages
        if self.data_sources["commit_history"].exists():
            try:
                log_file = self.data_sources["commit_history"] / "HEAD"
                if log_file.exists():
                    lines = log_file.read_text().split('\n')[-50:]  # Last 50 commits
                    for line in lines:
                        if "commit" in line:
                            texts.append(f"[COMMIT] {line}")

            except Exception as e:
                print(f"Error reading git logs: {e}")

        # Calendar events (if exists)
        if self.data_sources["calendar"].exists():
            try:
                content = self.data_sources["calendar"].read_text()
                # Extract event summaries (simplified)
                events = [line for line in content.split('\n') if 'SUMMARY:' in line]
                texts.extend([f"[CALENDAR] {event}" for event in events[:20]])
            except Exception:
                pass

        # Environmental data
        if self.data_sources["environment"].exists():
            try:
                data = json.loads(self.data_sources["environment"].read_text())
                texts.append(f"[ENVIRONMENT] {json.dumps(data)[:200]}")
            except Exception:
                pass

        # Add context files
        for context_file in Path(".").glob("*.context.md"):
            try:
                content = context_file.read_text(encoding='utf-8')
                texts.append(f"[CONTEXT] {content[:300]}")
            except Exception:
                pass

        return texts

    def anonymize_text(self, text: str) -> str:
        """Anonymize personal identifiers for privacy"""
        # Simple anonymization - replace email-like patterns
        import re
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        return text

    def mine_patterns(self, texts: List[str]) -> Dict[int, List[str]]:
        """Mine patterns using DBSCAN clustering"""
        if len(texts) < 3:
            print("⚠️ Not enough data for pattern mining")
            return {}

        # Anonymize texts
        texts = [self.anonymize_text(t) for t in texts]

        # Generate embeddings
        print("🧠 Generating embeddings...")
        embeddings = self.model.encode(texts, show_progress_bar=False)

        # Cluster with DBSCAN
        print("🔍 Mining patterns...")
        clustering = DBSCAN(eps=0.4, min_samples=3, metric='cosine')
        labels = clustering.fit_predict(embeddings)

        # Group by clusters
        clusters = {}
        for idx, label in enumerate(labels):
            if label != -1:  # Skip noise points
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(texts[idx][:180])

        # Calculate silhouette score if we have clusters
        if len(set(labels)) > 1 and -1 not in labels:
            score = silhouette_score(embeddings, labels, metric='cosine')
            print(f"📊 Clustering quality (silhouette): {score:.3f}")

        return clusters

    def calculate_pattern_depth(self, clusters: Dict) -> float:
        """Calculate entropy-based novelty score"""
        if not clusters:
            return 0.0

        # Calculate cluster size distribution
        sizes = [len(cluster) for cluster in clusters.values()]
        total = sum(sizes)

        # Calculate entropy
        entropy = 0
        for size in sizes:
            if size > 0:
                p = size / total
                entropy -= p * np.log2(p)

        # Normalize to 0-1
        max_entropy = np.log2(len(clusters)) if len(clusters) > 1 else 1
        pattern_depth = entropy / max_entropy if max_entropy > 0 else 0

        return round(pattern_depth, 2)

    def generate_opportunities(self, clusters: Dict) -> List[Dict[str, str]]:
        """Generate opportunities from patterns"""
        opportunities = []

        # Analyze each cluster for themes
        for cluster_id, texts in clusters.items():
            # Simple theme detection based on keywords
            themes = {
                "funding": ["grant", "funding", "501c3", "nonprofit"],
                "automation": ["automate", "script", "workflow", "cascade"],
                "impact": ["impact", "measurement", "outcome", "result"],
                "collaboration": ["partner", "team", "collaborate", "connect"],
                "innovation": ["new", "innovate", "create", "build"]
            }

            detected_themes = []
            cluster_text = " ".join(texts).lower()

            for theme, keywords in themes.items():
                if any(keyword in cluster_text for keyword in keywords):
                    detected_themes.append(theme)

            if detected_themes:
                opportunity = {
                    "title": f"Hidden Opportunity: {', '.join(detected_themes).title()}",
                    "description": f"Pattern analysis reveals potential in: {detected_themes[0]}",
                    "cluster_size": len(texts),
                    "themes": detected_themes,
                    "timestamp": datetime.now().isoformat()
                }
                opportunities.append(opportunity)

        # Sort by cluster size (importance)
        opportunities.sort(key=lambda x: x["cluster_size"], reverse=True)

        return opportunities[:5]  # Top 5

    def update_metrics(self, pattern_depth: float, insights_count: int):
        """Update metrics.yml with pattern insights"""
        metrics_path = Path("metrics.yml")

        # Load existing metrics
        if metrics_path.exists():
            import yaml
            with open(metrics_path, 'r') as f:
                metrics = yaml.safe_load(f)
        else:
            metrics = {}

        # Update with pattern metrics
        metrics.update({
            "pattern_depth": pattern_depth,
            "insights_surfaced": insights_count,
            "insight_latency_mins": 11,  # Placeholder
            "psych_safety_index": 0.98,  # Placeholder
            "last_pattern_scan": datetime.now().isoformat()
        })

        # Save updated metrics
        import yaml
        with open(metrics_path, 'w') as f:
            yaml.safe_dump(metrics, f, default_flow_style=False)

    def save_patterns(self, clusters: Dict, opportunities: List[Dict]):
        """Save patterns and opportunities"""
        # Save patterns
        patterns_file = Path("patterns.json")
        with open(patterns_file, 'w') as f:
            json.dump(clusters, f, indent=2)

        # Save opportunities
        opportunities_file = Path("opportunities.md")
        with open(opportunities_file, 'w') as f:
            f.write("# 🎯 Hidden Opportunities\n\n")
            f.write("*Generated by Pattern-Insight Engine*\n\n")

            for i, opp in enumerate(opportunities, 1):
                f.write(f"## {i}. {opp['title']}\n")
                f.write(f"- **Description**: {opp['description']}\n")
                f.write(f"- **Themes**: {', '.join(opp['themes'])}\n")
                f.write(f"- **Pattern Strength**: {opp['cluster_size']} signals\n")
                f.write(f"- **Discovered**: {opp['timestamp']}\n\n")

        print(f"💾 Saved {len(opportunities)} opportunities to opportunities.md")

    def run(self):
        """Main execution flow"""
        print("🧠 Pattern-Insight Engine v1.0")
        print("=" * 40)

        # Collect data
        print("📡 Collecting data from sources...")
        texts = self.collect_texts()
        print(f"📊 Collected {len(texts)} text samples")

        if len(texts) < 3:
            print("❌ Insufficient data for pattern analysis")
            return

        # Mine patterns
        clusters = self.mine_patterns(texts)
        print(f"🔍 Discovered {len(clusters)} pattern clusters")

        # Calculate metrics
        pattern_depth = self.calculate_pattern_depth(clusters)
        print(f"📈 Pattern depth: {pattern_depth}")

        # Generate opportunities
        opportunities = self.generate_opportunities(clusters)
        print(f"🎯 Generated {len(opportunities)} opportunities")

        # Update metrics
        self.update_metrics(pattern_depth, len(opportunities))

        # Save results
        self.save_patterns(clusters, opportunities)

        print("\n✅ Pattern analysis complete!")
        print("💡 Check opportunities.md for hidden insights")

def main():
    """Main entry point"""
    engine = PatternInsightEngine()
    engine.run()

if __name__ == "__main__":
    main()
