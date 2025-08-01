#!/usr/bin/env python3
"""Debug version to see why patterns aren't matching"""

import sys
sys.path.insert(0, '.')
from scripts.populate_airtable_funding import FundingPopulator
from supervisor.patterns.funder_keywords import load_funder_patterns
from supervisor.patterns.base_pattern import PatternRegistry
import requests

class PatternDebug(FundingPopulator):
    def debug_patterns(self):
        """Debug pattern matching"""
        print("🔍 Pattern Debug Starting...")

        # Load patterns
        registry = PatternRegistry()
        patterns = load_funder_patterns()
        for pattern in patterns:
            registry.register_pattern(pattern)
            print(f"✅ Loaded pattern: {pattern.name}")

        # Get first few records to test
        url = f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}?maxRecords=5'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch records: {response.status_code}")
            return

        records = response.json().get('records', [])
        print(f"\n📊 Testing {len(records)} records...\n")

        for i, record in enumerate(records):
            fields = record.get('fields', {})
            name = fields.get('Opportunity Name', '')
            desc = fields.get('Description', '')
            text = f"{name} {desc}".lower()

            print(f"Record {i+1}: {name[:50]}...")
            print(f"Text to match: {text[:100]}...")

            # Test each pattern
            for pattern in patterns:
                import re
                if re.search(pattern.pattern, text, re.IGNORECASE):
                    print(f"  ✅ MATCH: {pattern.name}")
                else:
                    print(f"  ❌ No match: {pattern.name} (pattern: {pattern.pattern[:50]}...)")

            print()

if __name__ == "__main__":
    debug = PatternDebug()
    debug.debug_patterns()
