#!/usr/bin/env python3
"""Airtable Field Inspector - Enumerates all available fields for user verification"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
from datetime import datetime
from scripts.populate_airtable_funding import FundingPopulator

class AirtableFieldInspector(FundingPopulator):
    def inspect_fields(self):
        """Inspect and enumerate all fields in the Airtable"""
        print("🔍 Airtable Field Inspector Starting...")
        print("=" * 80)

        # Get first record as sample
        url = f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}?maxRecords=1'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch records: {response.status_code}")
            print(f"Response: {response.text}")
            return

        data = response.json()
        if not data.get('records'):
            print("❌ No records found in table")
            return

        # Get the first record
        record = data['records'][0]
        record_id = record['id']
        fields = record.get('fields', {})

        print(f"📊 Analyzing Record: {record_id}")
        print(f"🔗 Direct Link: https://airtable.com/{self.base_id}/{self.table_id}/{record_id}")
        print("=" * 80)

        # Prepare field data
        field_data = []

        # Enumerate all fields
        for field_name, field_value in fields.items():
            field_info = {
                'name': field_name,
                'value': str(field_value)[:100] + '...' if len(str(field_value)) > 100 else str(field_value),
                'type': type(field_value).__name__,
                'populated': bool(field_value)
            }
            field_data.append(field_info)

        # Sort by field name for consistency
        field_data.sort(key=lambda x: x['name'])

        # Display fields
        print("\n📋 AVAILABLE FIELDS:\n")
        print(f"{'Field Name':<40} {'Type':<15} {'Populated':<10} {'Current Value':<50}")
        print("-" * 115)

        for field in field_data:
            print(f"{field['name']:<40} {field['type']:<15} {'Yes' if field['populated'] else 'No':<10} {field['value']:<50}")

        # Generate markdown report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report = f"""# Airtable Field Inspection Report

Generated: {timestamp}
Base ID: {self.base_id}
Table ID: {self.table_id}
Sample Record: {record_id}

## Available Fields

| Field Name | Type | Populated | Current Value |
|------------|------|-----------|---------------|
"""

        for field in field_data:
            report += f"| {field['name']} | {field['type']} | {'Yes' if field['populated'] else 'No'} | {field['value']} |\n"

        report += f"""

## Field Selection Guidance

1. **For AI Pattern annotations**, consider these fields:
   - Fields currently empty (Populated = No)
   - Text fields (Type = str)
   - Fields visible in your standard view

2. **Avoid updating**:
   - Formula fields (if any)
   - System fields
   - Primary fields

## Next Steps

Please review the fields above and tell me which field to update with AI pattern annotations.

Example response: "Update the 'Notes' field"

## API Details

- Request URL: {url}
- Request Method: GET
- Response Status: {response.status_code}
- Total Fields Found: {len(field_data)}
"""

        # Save report
        report_file = 'airtable_field_inspection_report.md'
        with open(report_file, 'w') as f:
            f.write(report)

        print(f"\n✅ Field inspection complete!")
        print(f"📄 Report saved to: {report_file}")
        print("\n🎯 Next step: Tell me which field to update for the test")

        return field_data

if __name__ == "__main__":
    inspector = AirtableFieldInspector()
    inspector.inspect_fields()
