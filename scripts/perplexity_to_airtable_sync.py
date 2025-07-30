#!/usr/bin/env python3
"""
Recovery Compass Perplexity → Airtable Sync
Automatically syncs discovered funding opportunities to Airtable
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re

class PerplexityAirtableSync:
    def __init__(self):
        # Get API keys from environment or keychain
        self.airtable_api_key = self._get_api_key('airtable')
        self.perplexity_api_key = self._get_api_key('perplexity')

        # Airtable configuration
        self.airtable_base_id = os.getenv('AIRTABLE_BASE_ID', '')  # Set this after creating base
        self.funding_table = 'Funding Opportunities'
        self.airtable_endpoint = f'https://api.airtable.com/v0/{self.airtable_base_id}'

    def _get_api_key(self, service: str) -> str:
        """Get API key from keychain"""
        import subprocess
        try:
            result = subprocess.run(
                ['security', 'find-generic-password', '-s', f'recovery-compass-{service}-key', '-w'],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except:
            return os.getenv(f'{service.upper()}_API_KEY', '')

    def categorize_funding_type(self, description: str) -> Dict[str, any]:
        """Categorize funding as traditional or non-traditional"""
        non_traditional_keywords = [
            'dao', 'web3', 'crypto', 'blockchain', 'gitcoin',
            'crowdfunding', 'social impact bond', 'impact investment',
            'venture philanthropy', 'catalytic funding'
        ]

        traditional_keywords = [
            'federal grant', 'state grant', 'foundation',
            'samhsa', 'hrsa', 'cdc', 'nih', 'government'
        ]

        description_lower = description.lower()

        # Check for non-traditional
        if any(keyword in description_lower for keyword in non_traditional_keywords):
            return {
                'type': 'Non-Traditional',
                'confidence': 0.9
            }

        # Check for traditional
        if any(keyword in description_lower for keyword in traditional_keywords):
            return {
                'type': 'Traditional',
                'confidence': 0.9
            }

        # Default to traditional with lower confidence
        return {
            'type': 'Traditional',
            'confidence': 0.6
        }

    def calculate_priority_score(self, opportunity: Dict) -> int:
        """Calculate priority score based on multiple factors"""
        score = 50  # Base score

        # Deadline urgency (up to +30 points)
        if opportunity.get('deadline'):
            days_until = (opportunity['deadline'] - datetime.now()).days
            if days_until < 30:
                score += 30
            elif days_until < 60:
                score += 20
            elif days_until < 90:
                score += 10

        # Amount range (up to +20 points)
        amount = opportunity.get('amount_max', 0)
        if amount > 1000000:
            score += 20
        elif amount > 500000:
            score += 15
        elif amount > 100000:
            score += 10
        elif amount > 50000:
            score += 5

        # Success probability from AI analysis
        success_prob = opportunity.get('success_probability', 0.5)
        score += int(success_prob * 20)

        return min(100, score)  # Cap at 100

    def parse_amount_range(self, amount_text: str) -> Dict[str, int]:
        """Parse amount text to extract min/max values"""
        # Remove commas and dollar signs
        clean_text = amount_text.replace(',', '').replace('$', '')

        # Find all numbers
        numbers = re.findall(r'\d+', clean_text)

        if len(numbers) >= 2:
            return {
                'min': int(numbers[0]),
                'max': int(numbers[1])
            }
        elif len(numbers) == 1:
            return {
                'min': 0,
                'max': int(numbers[0])
            }
        else:
            return {
                'min': 0,
                'max': 0
            }

    def create_airtable_record(self, opportunity: Dict) -> Optional[str]:
        """Create a new record in Airtable"""

        # Categorize funding type
        categorization = self.categorize_funding_type(
            f"{opportunity.get('name', '')} {opportunity.get('description', '')}"
        )

        # Parse amount range
        amount_range = self.parse_amount_range(opportunity.get('amount', ''))

        # Calculate priority score
        priority_score = self.calculate_priority_score({
            **opportunity,
            'amount_max': amount_range['max'],
            'success_probability': opportunity.get('match_score', 0.5)
        })

        # Prepare record data
        # Handle deadline - convert datetime to string if needed
        deadline = opportunity.get('deadline', '')
        if isinstance(deadline, datetime):
            deadline = deadline.strftime('%Y-%m-%d')

        record_data = {
            "fields": {
                "Name": opportunity.get('name', 'Untitled Opportunity'),
                "Funder": opportunity.get('funder', 'Unknown'),
                "Type": categorization['type'],
                "Category": self._determine_categories(opportunity),
                "Amount Range": f"${amount_range['min']:,} - ${amount_range['max']:,}",
                "Deadline": deadline,
                "Priority Score": priority_score,
                "Success Probability": opportunity.get('match_score', 0.5),
                "Discovery Source": "Perplexity AI",
                "Discovery Date": datetime.now().strftime('%Y-%m-%d'),
                "Status": "New",
                "Next Action": "Review and assess fit",
                "Notes": opportunity.get('description', '')
            }
        }

        # Make API request
        headers = {
            'Authorization': f'Bearer {self.airtable_api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            f'{self.airtable_endpoint}/{self.funding_table}',
            headers=headers,
            json=record_data
        )

        if response.status_code == 200:
            record_id = response.json()['id']
            print(f"✅ Created Airtable record: {record_id} for {opportunity.get('name')}")
            return record_id
        else:
            print(f"❌ Failed to create record: {response.status_code} - {response.text}")
            return None

    def _determine_categories(self, opportunity: Dict) -> List[str]:
        """Determine funding categories based on opportunity details"""
        categories = []

        text = f"{opportunity.get('name', '')} {opportunity.get('description', '')} {opportunity.get('funder', '')}".lower()

        # Check each category
        if any(word in text for word in ['federal', 'government', 'gov', 'samhsa', 'hrsa', 'nih']):
            categories.append('Federal')

        if any(word in text for word in ['state', 'california', 'county']):
            categories.append('State')

        if any(word in text for word in ['foundation', 'trust', 'fund']):
            categories.append('Foundation')

        if any(word in text for word in ['dao', 'web3', 'gitcoin', 'crypto']):
            categories.append('Web3/DAO')

        if any(word in text for word in ['corporate', 'company', 'inc', 'llc']):
            categories.append('Corporate')

        if any(word in text for word in ['crowdfunding', 'campaign']):
            categories.append('Crowdfunding')

        if any(word in text for word in ['social impact bond', 'sib', 'pay for success']):
            categories.append('Social Impact Bond')

        return categories if categories else ['Foundation']  # Default to Foundation

    def check_duplicate(self, opportunity: Dict) -> bool:
        """Check if opportunity already exists in Airtable"""
        # Search by name
        params = {
            'filterByFormula': f"{{Name}} = '{opportunity.get('name', '')}'"
        }

        headers = {
            'Authorization': f'Bearer {self.airtable_api_key}'
        }

        response = requests.get(
            f'{self.airtable_endpoint}/{self.funding_table}',
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            records = response.json().get('records', [])
            return len(records) > 0

        return False

    def sync_opportunities(self, opportunities: List[Dict]) -> Dict[str, int]:
        """Sync a list of opportunities to Airtable"""
        results = {
            'created': 0,
            'duplicates': 0,
            'errors': 0
        }

        for opportunity in opportunities:
            try:
                # Check for duplicates
                if self.check_duplicate(opportunity):
                    print(f"⏭️  Skipping duplicate: {opportunity.get('name')}")
                    results['duplicates'] += 1
                    continue

                # Create new record
                record_id = self.create_airtable_record(opportunity)
                if record_id:
                    results['created'] += 1
                else:
                    results['errors'] += 1

            except Exception as e:
                print(f"❌ Error processing opportunity: {str(e)}")
                results['errors'] += 1

        return results

# Example usage
if __name__ == "__main__":
    # Initialize sync
    sync = PerplexityAirtableSync()

    # Example opportunities (would come from Perplexity discovery)
    sample_opportunities = [
        {
            'name': 'SAMHSA Recovery Housing Grant',
            'funder': 'SAMHSA',
            'amount': '$250,000 - $500,000',
            'deadline': datetime.now() + timedelta(days=45),
            'description': 'Federal grant for recovery housing programs',
            'match_score': 0.85
        },
        {
            'name': 'Gitcoin Grants Round 20',
            'funder': 'Gitcoin DAO',
            'amount': '$10,000 - $50,000',
            'deadline': datetime.now() + timedelta(days=20),
            'description': 'Web3 quadratic funding for public goods',
            'match_score': 0.72
        }
    ]

    # Sync to Airtable
    results = sync.sync_opportunities(sample_opportunities)

    print("\n📊 Sync Results:")
    print(f"✅ Created: {results['created']}")
    print(f"⏭️  Duplicates: {results['duplicates']}")
    print(f"❌ Errors: {results['errors']}")
