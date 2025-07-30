#!/usr/bin/env python3
"""
Check Thresholds - Pre-commit hook for metrics validation
Ensures metrics stay within acceptable ranges
"""

import sys
import yaml
from pathlib import Path

def check_metrics_thresholds(min_alignment, max_freshness, required_abundance):
    """Check if metrics meet required thresholds"""

    metrics_path = Path("metrics.yml")
    if not metrics_path.exists():
        print("❌ metrics.yml not found!")
        return False

    with open(metrics_path, 'r') as f:
        metrics = yaml.safe_load(f)

    failures = []

    # Check alignment score
    alignment = metrics.get("alignment_score", 0)
    if alignment < min_alignment:
        failures.append(f"Alignment score {alignment} < {min_alignment}")

    # Check context freshness
    freshness = metrics.get("context_freshness_mins", 999)
    if freshness > max_freshness:
        failures.append(f"Context freshness {freshness}m > {max_freshness}m")

    # Check abundance level
    abundance = metrics.get("abundance_level", "LOW")
    if abundance != required_abundance:
        failures.append(f"Abundance level '{abundance}' != '{required_abundance}'")

    # Check manual work percentage
    manual_work = metrics.get("manual_work_pct", 100)
    if manual_work > 5:
        failures.append(f"Manual work {manual_work}% > 5%")

    # Check force multiplier
    force_mult = metrics.get("force_multiplier", 0)
    if force_mult < 10:
        failures.append(f"Force multiplier {force_mult} < 10")

    if failures:
        print("❌ Metrics Threshold Check Failed!")
        print("\nFailures:")
        for f in failures:
            print(f"  - {f}")
        print("\n💡 Run 'python scripts/metrics_collector.py' to refresh metrics")
        return False

    print("✅ All metrics within thresholds!")
    return True

def main():
    """Main entry point"""

    if len(sys.argv) != 4:
        print("Usage: check_thresholds.py <min_alignment> <max_freshness_mins> <required_abundance>")
        print("Example: check_thresholds.py 0.90 60 HIGH")
        sys.exit(1)

    try:
        min_alignment = float(sys.argv[1])
        max_freshness = int(sys.argv[2])
        required_abundance = sys.argv[3]
    except ValueError:
        print("❌ Invalid arguments!")
        print("  min_alignment must be a float (e.g., 0.90)")
        print("  max_freshness_mins must be an integer (e.g., 60)")
        print("  required_abundance must be a string (e.g., HIGH)")
        sys.exit(1)

    # Check metrics
    success = check_metrics_thresholds(min_alignment, max_freshness, required_abundance)

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
