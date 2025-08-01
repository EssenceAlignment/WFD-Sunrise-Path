#!/usr/bin/env python3
"""Verify AI Pattern Updates in Airtable - Show exact records with patterns"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime
from scripts.populate_airtable_funding import FundingPopulator

class PatternVerification(FundingPopulator):
    def verify_patterns(self):
        """Show exact records that have AI pattern updates"""
        print("🔍 AI Pattern Verification Report")
        print("=" * 80)

        # Get all records to check for patterns
        url = f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}?maxRecords=100'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch records: {response.status_code}")
            return

        data = response.json()
        records = data.get('records', [])

        print(f"📊 Checking {len(records)} records for AI patterns...\n")

        # Track pattern updates
        records_with_patterns = []

        for record in records:
            record_id = record['id']
            fields = record.get('fields', {})

            # Check for AI patterns in Notes
            notes = fields.get('Notes', '')
            external_api_id = fields.get('External API ID', '')

            if '[AI Pattern:' in notes or 'PR2-' in external_api_id:
                pattern_info = {
                    'record_id': record_id,
                    'opportunity_name': fields.get('Opportunity Name', 'Unknown'),
                    'notes': notes,
                    'external_api_id': external_api_id,
                    'has_pattern_in_notes': '[AI Pattern:' in notes,
                    'has_pattern_in_api_id': 'PR2-' in external_api_id
                }
                records_with_patterns.append(pattern_info)

        # Display results
        print(f"✅ FOUND {len(records_with_patterns)} RECORDS WITH AI PATTERNS\n")

        for i, info in enumerate(records_with_patterns[:10], 1):  # Show first 10
            print(f"Record #{i}")
            print(f"  📌 Record ID: {info['record_id']}")
            print(f"  📋 Opportunity: {info['opportunity_name']}")
            print(f"  🔗 Direct Link: https://airtable.com/{self.base_id}/{self.table_id}/{info['record_id']}")

            if info['has_pattern_in_notes']:
                # Extract pattern from notes
                import re
                pattern_match = re.search(r'\[AI Pattern: ([^\]]+)\]', info['notes'])
                if pattern_match:
                    print(f"  ✅ Notes has pattern: {pattern_match.group(1)}")

            if info['has_pattern_in_api_id']:
                print(f"  ✅ External API ID: {info['external_api_id']}")

            print()

        # Generate verification instructions
        print("\n" + "=" * 80)
        print("📋 HOW TO SEE THESE AI PATTERNS IN YOUR AIRTABLE:\n")
        print("1. Open your Airtable: https://airtable.com/appNBesu9xYl5Mvm1/tblcfetlKrhMU4p5r")
        print("2. Look for the 'Notes' column")
        print("   - If not visible: Click '+' at the end of columns → Select 'Notes'")
        print("3. Look for the 'External API ID' column")
        print("   - If not visible: Click '+' at the end of columns → Select 'External API ID'")
        print("\n4. Or search for any of these specific records:")

        for info in records_with_patterns[:3]:
            print(f"   - {info['opportunity_name']}")

        # Save detailed report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report = f"""# AI Pattern Verification Report

Generated: {timestamp}

## Summary
- Total records checked: {len(records)}
- Records with AI patterns: {len(records_with_patterns)}

## Records with AI Pattern Updates

"""

        for i, info in enumerate(records_with_patterns, 1):
            report += f"""### {i}. {info['opportunity_name']}
- Record ID: {info['record_id']}
- Direct Link: https://airtable.com/{self.base_id}/{self.table_id}/{info['record_id']}
- Has pattern in Notes: {'Yes' if info['has_pattern_in_notes'] else 'No'}
- Has pattern in External API ID: {'Yes' if info['has_pattern_in_api_id'] else 'No'}

"""

        report_file = 'airtable_pattern_verification_report.md'
        with open(report_file, 'w') as f:
            f.write(report)

        print(f"\n📄 Full report saved to: {report_file}")
        print(f"\n✅ VERIFICATION COMPLETE: {len(records_with_patterns)} records have AI patterns")

if __name__ == "__main__":
    verifier = PatternVerification()
    verifier.verify_patterns()
