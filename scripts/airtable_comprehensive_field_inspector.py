#!/usr/bin/env python3
"""Comprehensive Airtable Field Inspector - Checks multiple records for all fields"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime
from scripts.populate_airtable_funding import FundingPopulator

class ComprehensiveFieldInspector(FundingPopulator):
    def inspect_all_fields(self):
        """Inspect multiple records to find all possible fields"""
        print("🔍 Comprehensive Airtable Field Inspector Starting...")
        print("=" * 80)

        # Get multiple records to see all fields
        url = f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}?maxRecords=10'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch records: {response.status_code}")
            print(f"Response: {response.text}")
            return

        data = response.json()
        records = data.get('records', [])

        if not records:
            print("❌ No records found in table")
            return

        print(f"📊 Analyzing {len(records)} records to find all fields...")
        print("=" * 80)

        # Collect all unique fields across all records
        all_fields = {}
        field_occurrences = {}

        for i, record in enumerate(records):
            record_id = record['id']
            fields = record.get('fields', {})

            for field_name, field_value in fields.items():
                if field_name not in all_fields:
                    all_fields[field_name] = {
                        'name': field_name,
                        'type': type(field_value).__name__,
                        'sample_value': str(field_value)[:50] + '...' if len(str(field_value)) > 50 else str(field_value),
                        'first_seen_in': record_id
                    }
                    field_occurrences[field_name] = 0
                field_occurrences[field_name] += 1

        # Sort fields by name
        sorted_fields = sorted(all_fields.items())

        # Display comprehensive field list
        print("\n📋 ALL FIELDS FOUND ACROSS RECORDS:\n")
        print(f"{'Field Name':<40} {'Type':<10} {'Occurrences':<12} {'Sample Value':<50}")
        print("-" * 112)

        for field_name, field_info in sorted_fields:
            occurrences = field_occurrences[field_name]
            print(f"{field_info['name']:<40} {field_info['type']:<10} {occurrences}/{len(records):<12} {field_info['sample_value']:<50}")

        # Check if specific fields exist that we tried to update before
        print("\n🔍 CHECKING FOR PREVIOUSLY ATTEMPTED FIELDS:")
        print("-" * 80)

        target_fields = ['Notes', 'External API ID', 'Priority Score', 'Description']
        for target in target_fields:
            if target in all_fields:
                print(f"✅ '{target}' - FOUND (Type: {all_fields[target]['type']})")
            else:
                print(f"❌ '{target}' - NOT FOUND")

        # Generate detailed report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report = f"""# Comprehensive Airtable Field Inspection Report

Generated: {timestamp}
Base ID: {self.base_id}
Table ID: {self.table_id}
Records Analyzed: {len(records)}

## All Available Fields

| Field Name | Type | Occurrences | Sample Value |
|------------|------|-------------|--------------|
"""

        for field_name, field_info in sorted_fields:
            occurrences = field_occurrences[field_name]
            report += f"| {field_info['name']} | {field_info['type']} | {occurrences}/{len(records)} | {field_info['sample_value']} |\n"

        report += f"""

## Field Analysis

### Previously Attempted Fields Status:
"""

        for target in target_fields:
            if target in all_fields:
                report += f"- ✅ **{target}**: Available (Type: {all_fields[target]['type']})\n"
            else:
                report += f"- ❌ **{target}**: Not found in any record\n"

        report += f"""

## Recommendations

Based on the field analysis:

1. **Fields that exist and can be updated**:
"""

        # Find text fields that exist
        text_fields = [f for f, info in all_fields.items() if info['type'] == 'str']
        for field in text_fields[:5]:  # Show top 5
            report += f"   - {field}\n"

        report += f"""

2. **Fields to avoid**:
   - 'Opportunity Name' (Primary field)
   - 'API Last Synced Time' (System field)

## Next Steps

Please select one of the existing fields from the list above for the test update.

Example: "Update the 'API Last Synced Time' field" (if you want to test with that)

## Debug Information

- Total unique fields found: {len(all_fields)}
- Records scanned: {len(records)}
- API Response Status: {response.status_code}
"""

        # Save comprehensive report
        report_file = 'airtable_comprehensive_field_report.md'
        with open(report_file, 'w') as f:
            f.write(report)

        print(f"\n✅ Comprehensive field inspection complete!")
        print(f"📄 Report saved to: {report_file}")
        print(f"\n🎯 Found {len(all_fields)} unique fields across {len(records)} records")
        print("\n⚠️  IMPORTANT: The fields 'Notes' and 'External API ID' that we tried to update earlier")
        print("    do not appear to exist in your table. Please choose from the available fields above.")

        return all_fields

if __name__ == "__main__":
    inspector = ComprehensiveFieldInspector()
    inspector.inspect_all_fields()
