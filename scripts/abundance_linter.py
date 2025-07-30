#!/usr/bin/env python3
"""
Abundance Linter - Enforces calm, mission-driven tone
Rejects urgency language that violates State of Abundance
"""

import sys
import re
from pathlib import Path

# Urgency patterns to reject
URGENCY_PATTERNS = [
    r'\b(ASAP|asap)\b',
    r'\burgent(ly)?\b',
    r'\bimmediately\b',
    r'\bright\s+now\b',
    r'\bhurry\b',
    r'\brush\b',
    r'\bdeadline\s+is\s+today\b',
    r'\btime\s+is\s+running\s+out\b',
    r'\bcritical\s+deadline\b',
    r'\bemergency\b',
    r'\bcrisis\b',
    r'\bmust\s+have\s+today\b',
]

# Positive abundance patterns we encourage
ABUNDANCE_PATTERNS = [
    r'\b(abundance|abundant)\b',
    r'\bforce\s+multiplication\b',
    r'\bsoft\s+power\b',
    r'\battract(ing|s)?\b',
    r'\bcompound(ing|s)?\b',
    r'\borchestrat(e|ing)\b',
    r'\benable(s|d)?\b',
    r'\bcascad(e|ing)\b',
]

def check_file(filepath):
    """Check a single file for urgency language"""
    violations = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check each line
        for line_num, line in enumerate(content.split('\n'), 1):
            for pattern in URGENCY_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        'file': filepath,
                        'line': line_num,
                        'pattern': pattern,
                        'content': line.strip()
                    })

    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)

    return violations

def main():
    """Main linter function"""
    # Get files from command line or stdin
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not files:
        # Read from stdin if no files provided
        for line in sys.stdin:
            files.append(line.strip())

    all_violations = []

    for filepath in files:
        if Path(filepath).exists():
            violations = check_file(filepath)
            all_violations.extend(violations)

    # Report violations
    if all_violations:
        print("❌ Abundance Linter: Urgency language detected!")
        print("This violates our State of Abundance philosophy.\n")

        for v in all_violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    Found: '{v['content']}'")
            print(f"    Pattern: {v['pattern']}\n")

        print("💡 Suggestion: Rephrase with calm, confident language.")
        print("Examples:")
        print("  ❌ 'We need this ASAP!' → ✅ 'This aligns with our priorities.'")
        print("  ❌ 'Urgent deadline!' → ✅ 'We're progressing systematically.'")
        print("  ❌ 'Must fix immediately!' → ✅ 'Let's address this thoughtfully.'")

        sys.exit(1)
    else:
        print("✅ Abundance Linter: All files pass! Calm, confident tone maintained.")
        sys.exit(0)

if __name__ == "__main__":
    main()
