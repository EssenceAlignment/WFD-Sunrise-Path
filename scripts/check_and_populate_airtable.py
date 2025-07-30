#!/usr/bin/env python3
"""
Check Airtable structure and populate with funding opportunities
"""

import requests
import json
from datetime import datetime, timedelta


class AirtableChecker:
    def __init__(self):
        self.api_key = 'patMwDeT8VWbBMHf8.2329f87a34a686f59fc3e705b92dbf09fe67a4c33c6234742da92bf8b295247c'
        self.base_id = 'appNBesu9xYl5Mvm1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def list_tables(self):
        """List all tables in the base"""
        url = f'https://api.airtable.com/v0/meta/bases/{self.base_id}/tables'

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            tables = response.json()['tables']
            print("📋 Tables in base:")
            for table in tables:
                print(f"  - {table['name']} (ID: {table['id']})")
                print("    Fields:")
                for field in table['fields']:
                    print(f"      - {field['name']} ({field['type']})")
            return tables
        else:
            print(f"❌ Error listing tables: {response.status_code}")
            print(response.text)
            return None

    def create_funding_table_if_needed(self):
        """Create the funding opportunities table with proper structure"""
        url = f'https://api.airtable.com/v0/meta/bases/{self.base_id}/tables'

        table_config = {
            "name": "Funding Opportunities",
            "fields": [
                {"name": "Opportunity Name", "type": "singleLineText"},
                {"name": "Funder", "type": "singleLineText"},
                {"name": "Type", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Traditional"},
                        {"name": "Non-Traditional"}
                    ]
                }},
                {"name": "Category", "type": "multipleSelects", "options": {
                    "choices": [
                        {"name": "Federal"},
                        {"name": "State"},
                        {"name": "Foundation"},
                        {"name": "Corporate"},
                        {"name": "Web3/DAO"},
                        {"name": "Crowdfunding"},
                        {"name": "Social Impact Bond"},
                        {"name": "Venture Philanthropy"}
                    ]
                }},
                {"name": "Amount Range", "type": "singleLineText"},
                {"name": "Deadline", "type": "date"},
                {"name": "Priority Score", "type": "number", "options": {"precision": 0}},
                {"name": "Success Probability", "type": "percent", "options": {"precision": 0}},
                {"name": "Status", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "New", "color": "blueLight2"},
                        {"name": "Researching", "color": "yellowLight2"},
                        {"name": "Applying", "color": "orangeLight2"},
                        {"name": "Submitted", "color": "purpleLight2"},
                        {"name": "Awarded", "color": "greenLight2"},
                        {"name": "Rejected", "color": "redLight2"}
                    ]
                }},
                {"name": "Discovery Source", "type": "singleLineText"},
                {"name": "Discovery Date", "type": "date"},
                {"name": "Next Action", "type": "singleLineText"},
                {"name": "Notes", "type": "multilineText"},
                {"name": "URL", "type": "url"}
            ]
        }

        response = requests.post(url, headers=self.headers, json=table_config)

        if response.status_code == 200:
            print("✅ Created Funding Opportunities table!")
            return response.json()
        else:
            print(f"❌ Error creating table: {response.status_code}")
            print(response.text)
            return None

    def create_sample_record(self):
        """Create a sample record to test the API"""

        # First, let's list existing tables
        tables = self.list_tables()

        if not tables:
            print("\n🔨 Creating Funding Opportunities table...")
            self.create_funding_table_if_needed()
            tables = self.list_tables()

        # Find the first table or Funding Opportunities table
        funding_table = None
        for table in tables:
            if 'funding' in table['name'].lower() or 'opportunities' in table['name'].lower():
                funding_table = table
                break

        if not funding_table:
            funding_table = tables[0] if tables else None

        if not funding_table:
            print("❌ No tables found!")
            return

        print(f"\n📝 Using table: {funding_table['name']}")

        # Get the first field name (should be the primary field)
        primary_field = funding_table['fields'][0]['name']

        # Create a simple record
        record_data = {
            "fields": {
                primary_field: "SAMHSA Recovery Community Services Program - Test"
            }
        }

        # Add other fields if they exist
        field_names = [f['name'] for f in funding_table['fields']]

        if 'Funder' in field_names:
            record_data['fields']['Funder'] = 'SAMHSA'

        if 'Amount' in field_names or 'Amount Range' in field_names:
            field_name = 'Amount' if 'Amount' in field_names else 'Amount Range'
            record_data['fields'][field_name] = '$500,000 - $750,000'

        if 'Type' in field_names:
            record_data['fields']['Type'] = 'Traditional'

        if 'Status' in field_names:
            record_data['fields']['Status'] = 'New'

        # Try to create the record
        url = f"https://api.airtable.com/v0/{self.base_id}/{funding_table['id']}"

        print(f"\n🚀 Creating test record with data:")
        print(json.dumps(record_data, indent=2))

        response = requests.post(url, headers=self.headers, json=record_data)

        if response.status_code == 200:
            print(f"✅ Successfully created record!")
            print(f"   Record ID: {response.json()['id']}")
        else:
            print(f"❌ Error creating record: {response.status_code}")
            print(response.text)


if __name__ == "__main__":
    checker = AirtableChecker()
    checker.create_sample_record()
