#!/usr/bin/env python3
"""
Recovery Compass Funding Dashboard Populator
Discovers and populates funding opportunities in Airtable
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re
import subprocess
import time


class FundingDashboardPopulator:
    def __init__(self):
        # Get API keys
        self.airtable_api_key = 'patMwDeT8VWbBMHf8.2329f87a34a686f59fc3e705b92dbf09fe67a4c33c6234742da92bf8b295247c'
        self.perplexity_api_key = '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'
        self.airtable_base_id = 'appNBesu9xYl5Mvm1'

        # Airtable configuration
        self.funding_table = 'Funding Opportunities'
        self.airtable_endpoint = f'https://api.airtable.com/v0/{self.airtable_base_id}'

    def discover_funding_opportunities(self) -> List[Dict]:
        """Use Perplexity to discover funding opportunities"""

        # Traditional funding sources query
        traditional_queries = [
            "2025 SAMHSA grants for addiction recovery organizations California deadline",
            "2025 HRSA behavioral health grants recovery housing funding opportunities",
            "2025 CDC overdose prevention grants California nonprofit organizations",
            "2025 California state grants substance abuse treatment recovery programs",
            "2025 foundation grants addiction recovery nonprofit organizations",
            "Robert Wood Johnson Foundation 2025 substance abuse grants",
            "Conrad N. Hilton Foundation recovery housing grants 2025",
            "2025 community foundation grants San Diego recovery organizations"
        ]

        # Non-traditional funding sources query
        non_traditional_queries = [
            "Web3 grants DAO funding public goods addiction recovery 2025",
            "Gitcoin grants round 2025 social impact recovery organizations",
            "Crowdfunding platforms nonprofit recovery housing campaigns 2025",
            "Social impact bonds pay for success addiction treatment 2025",
            "Impact investing recovery housing ventures 2025",
            "Corporate social responsibility grants recovery organizations 2025",
            "Venture philanthropy addiction recovery innovative solutions 2025",
            "Blockchain grants decentralized recovery support networks 2025"
        ]

        all_opportunities = []

        # Search traditional sources
        print("🔍 Searching for traditional funding sources...")
        for query in traditional_queries:
            opportunities = self._search_perplexity(query, "Traditional")
            all_opportunities.extend(opportunities)
            time.sleep(2)  # Rate limiting

        # Search non-traditional sources
        print("🔍 Searching for non-traditional funding sources...")
        for query in non_traditional_queries:
            opportunities = self._search_perplexity(query, "Non-Traditional")
            all_opportunities.extend(opportunities)
            time.sleep(2)  # Rate limiting

        return all_opportunities

    def _search_perplexity(self, query: str, funding_type: str) -> List[Dict]:
        """Search Perplexity for funding opportunities"""

        headers = {
            'Authorization': f'Bearer {self.perplexity_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'llama-3.1-sonar-small-128k-online',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a funding expert helping find grants for Recovery Compass, a 501(c)(3) nonprofit focused on addiction recovery housing and support. Extract specific funding opportunities with names, amounts, deadlines, and eligibility.'
                },
                {
                    'role': 'user',
                    'content': f'{query}. Provide specific grant names, funders, amounts, deadlines, and brief descriptions. Focus on opportunities that Recovery Compass would be eligible for.'
                }
            ],
            'temperature': 0.2,
            'max_tokens': 2000
        }

        try:
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                # Parse opportunities from response
                opportunities = self._parse_opportunities(content, funding_type)
                return opportunities
            else:
                print(f"❌ Perplexity API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Error searching Perplexity: {str(e)}")
            return []

    def _parse_opportunities(self, content: str, funding_type: str) -> List[Dict]:
        """Parse funding opportunities from Perplexity response"""
        opportunities = []

        # Split content into potential opportunities
        sections = content.split('\n\n')

        for section in sections:
            if len(section) < 50:  # Skip short sections
                continue

            opportunity = {
                'type': funding_type,
                'discovery_date': datetime.now()
            }

            # Extract grant name (usually in bold or at start)
            name_match = re.search(r'\*\*(.*?)\*\*|^([A-Z].*?(?:Grant|Program|Fund|Initiative))', section)
            if name_match:
                opportunity['name'] = name_match.group(1) or name_match.group(2)

            # Extract funder
            funder_match = re.search(r'(?:Funder|Organization|Agency|by):\s*(.*?)(?:\n|$)', section, re.I)
            if funder_match:
                opportunity['funder'] = funder_match.group(1).strip()

            # Extract amount
            amount_match = re.search(r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?|\$[\d.]+[MK]', section)
            if amount_match:
                opportunity['amount'] = amount_match.group(0)

            # Extract deadline
            deadline_match = re.search(r'(?:Deadline|Due|Submit by|Applications? (?:due|close)):\s*(.*?)(?:\n|$)', section, re.I)
            if deadline_match:
                deadline_str = deadline_match.group(1).strip()
                parsed_deadline = self._parse_deadline(deadline_str)
                if parsed_deadline:
                    opportunity['deadline'] = parsed_deadline

            # Use full section as description
            opportunity['description'] = section.strip()

            # Calculate match score based on keywords
            match_keywords = ['recovery', 'housing', 'addiction', 'substance', 'nonprofit', '501c3', 'california', 'san diego']
            match_count = sum(1 for keyword in match_keywords if keyword in section.lower())
            opportunity['match_score'] = min(0.95, 0.5 + (match_count * 0.1))

            # Only add if we have minimum required fields
            if opportunity.get('name') and (opportunity.get('amount') or opportunity.get('deadline')):
                opportunities.append(opportunity)

        return opportunities

    def _parse_deadline(self, deadline_str: str) -> Optional[datetime]:
        """Parse deadline string to datetime"""
        deadline_str = deadline_str.strip()

        # Common date patterns
        patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # MM/DD/YYYY or MM-DD-YYYY
            r'(\w+)\s+(\d{1,2}),?\s+(\d{4})',      # Month DD, YYYY
            r'(\d{1,2})\s+(\w+)\s+(\d{4})',        # DD Month YYYY
        ]

        for pattern in patterns:
            match = re.search(pattern, deadline_str)
            if match:
                try:
                    # Try to parse the date
                    if '/' in deadline_str or '-' in deadline_str:
                        # Numeric format
                        month, day, year = match.groups()
                        return datetime(int(year), int(month), int(day))
                    else:
                        # Text month format
                        # This is simplified - would need proper month parsing
                        return datetime.now() + timedelta(days=60)  # Default to 60 days
                except:
                    pass

        # Check for relative dates
        if 'rolling' in deadline_str.lower() or 'ongoing' in deadline_str.lower():
            return datetime.now() + timedelta(days=365)  # One year out

        # Default to 90 days if no date found
        return datetime.now() + timedelta(days=90)

    def create_airtable_base_if_needed(self):
        """Create Airtable base structure if it doesn't exist"""
        # This would check if the table exists and has the right fields
        # For now, we'll assume it exists
        pass

    def populate_dashboard(self):
        """Main function to discover and populate funding opportunities"""

        print("🚀 Starting Recovery Compass Funding Dashboard Population")
        print("=" * 60)

        # Discover opportunities
        print("\n📡 Discovering funding opportunities...")
        opportunities = self.discover_funding_opportunities()

        print(f"\n✅ Discovered {len(opportunities)} potential opportunities")

        # Filter and deduplicate
        unique_opportunities = []
        seen_names = set()

        for opp in opportunities:
            name = opp.get('name', '')
            if name and name not in seen_names:
                seen_names.add(name)
                unique_opportunities.append(opp)

        print(f"📋 Filtered to {len(unique_opportunities)} unique opportunities")

        # Sort by match score and priority
        unique_opportunities.sort(key=lambda x: x.get('match_score', 0), reverse=True)

        # Import the sync class and populate
        from perplexity_to_airtable_sync import PerplexityAirtableSync

        sync = PerplexityAirtableSync()
        sync.airtable_base_id = self.airtable_base_id
        sync.airtable_api_key = self.airtable_api_key

        print("\n📤 Syncing to Airtable...")
        results = sync.sync_opportunities(unique_opportunities)

        print("\n🎯 Population Complete!")
        print("=" * 60)
        print(f"✅ Created: {results['created']} new opportunities")
        print(f"⏭️  Skipped: {results['duplicates']} duplicates")
        print(f"❌ Errors: {results['errors']}")

        # Generate summary report
        self._generate_summary_report(unique_opportunities, results)

    def _generate_summary_report(self, opportunities: List[Dict], results: Dict):
        """Generate a summary report of discovered opportunities"""

        traditional = [o for o in opportunities if o.get('type') == 'Traditional']
        non_traditional = [o for o in opportunities if o.get('type') == 'Non-Traditional']

        report = f"""
📊 FUNDING DISCOVERY SUMMARY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW:
- Total Opportunities Discovered: {len(opportunities)}
- Traditional Funding: {len(traditional)}
- Non-Traditional Funding: {len(non_traditional)}
- Successfully Added to Airtable: {results['created']}

TOP 5 HIGHEST SCORING OPPORTUNITIES:
"""

        for i, opp in enumerate(opportunities[:5], 1):
            report += f"""
{i}. {opp.get('name', 'Unnamed')}
   - Type: {opp.get('type')}
   - Funder: {opp.get('funder', 'Unknown')}
   - Amount: {opp.get('amount', 'Not specified')}
   - Deadline: {opp.get('deadline', 'Not specified')}
   - Match Score: {opp.get('match_score', 0):.2f}
"""

        # Save report
        with open('funding_discovery_report.txt', 'w') as f:
            f.write(report)

        print(f"\n📄 Summary report saved to: funding_discovery_report.txt")


if __name__ == "__main__":
    populator = FundingDashboardPopulator()
    populator.populate_dashboard()
