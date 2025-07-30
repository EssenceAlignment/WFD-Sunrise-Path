#!/usr/bin/env python3
"""
Hidden Gems Scanner - Mines commit history for overlooked high-impact changes
Appends findings to hidden_gems.context.md
"""

import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path

# Patterns that indicate high-impact changes
HIGH_IMPACT_PATTERNS = [
    r'implement.*automation',
    r'force.*multipli',
    r'cascade.*effect',
    r'abundance.*system',
    r'context.*alignment',
    r'funding.*discover',
    r'grant.*opportunit',
    r'501.*c.*3',
    r'nonprofit.*verif',
    r'impact.*measur',
]

def scan_commits(days_back=7):
    """Scan recent commits for hidden gems"""
    gems = []

    # Get commits from last N days
    since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    cmd = ['git', 'log', f'--since={since_date}', '--oneline', '--all']

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits = result.stdout.strip().split('\n')

        for commit in commits:
            if not commit:
                continue

            # Check commit message for high-impact patterns
            for pattern in HIGH_IMPACT_PATTERNS:
                if re.search(pattern, commit, re.IGNORECASE):
                    # Get full commit details
                    commit_hash = commit.split()[0]
                    details_cmd = ['git', 'show', '--stat', commit_hash]
                    details = subprocess.run(details_cmd, capture_output=True, text=True)

                    gem = {
                        'commit': commit,
                        'pattern': pattern,
                        'details': details.stdout[:500],  # First 500 chars
                        'discovered': datetime.now().isoformat()
                    }
                    gems.append(gem)
                    break

    except subprocess.CalledProcessError as e:
        print(f"Error scanning commits: {e}")

    return gems

def append_to_hidden_gems(gems):
    """Append discovered gems to hidden_gems.context.md"""

    gems_file = Path('hidden_gems.context.md')

    # Create file if it doesn't exist
    if not gems_file.exists():
        gems_file.write_text("""# Hidden Gems - Auto-Discovered High-Impact Changes

This file is automatically updated by the nightly gem scanner.
It captures overlooked changes that have force multiplication potential.

---

""")

    # Append new gems
    if gems:
        with open(gems_file, 'a') as f:
            f.write(f"\n## Scan: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

            for gem in gems:
                f.write(f"### 💎 {gem['commit']}\n")
                f.write(f"- **Pattern Matched**: `{gem['pattern']}`\n")
                f.write(f"- **Discovered**: {gem['discovered']}\n")
                f.write(f"- **Details**:\n```\n{gem['details']}\n```\n\n")

        print(f"✨ Added {len(gems)} hidden gems to {gems_file}")
    else:
        print("🔍 No new hidden gems found in this scan")

def update_force_metrics():
    """Update force multiplication metrics"""

    metrics_file = Path('scripts/force_metrics.csv')

    # Initialize if doesn't exist
    if not metrics_file.exists():
        metrics_file.write_text("timestamp,gems_found,force_multiplier,impact_score\n")

    # Count total gems
    gems_content = Path('hidden_gems.context.md').read_text() if Path('hidden_gems.context.md').exists() else ""
    total_gems = gems_content.count('### 💎')

    # Calculate force multiplier (exponential based on gems)
    force_multiplier = min(10 * (1.1 ** total_gems), 100)  # Cap at 100x

    # Append metrics
    with open(metrics_file, 'a') as f:
        f.write(f"{datetime.now().isoformat()},{total_gems},{force_multiplier:.2f},{total_gems * 10}\n")

def main():
    """Main scanning function"""
    print("🔍 Starting hidden gems scan...")

    # Scan last 7 days by default
    gems = scan_commits(days_back=7)

    # Append findings
    append_to_hidden_gems(gems)

    # Update metrics
    update_force_metrics()

    print("✅ Hidden gems scan complete!")

if __name__ == "__main__":
    main()
