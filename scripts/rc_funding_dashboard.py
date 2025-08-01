#!/usr/bin/env python3
"""Recovery Compass Funding Dashboard - Real-time funding intelligence"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime, timedelta
import argparse
import json
from scripts.populate_airtable_funding import FundingPopulator

class FundingDashboard(FundingPopulator):
    def __init__(self):
        super().__init__()
        self.alignment_keywords = {
            # Mental health & recovery (highest priority)
            'recovery': 30, 'mental health': 30, 'substance': 30, 'behavioral': 30,
            'addiction': 30, 'treatment': 25, 'sober': 25, 'housing': 25,

            # Innovation & pilot
            'innovation': 20, 'pilot': 20, 'demonstration': 20, 'technology': 15,
            'digital': 15, 'AI': 15, 'data': 15,

            # Vulnerable populations
            'youth': 20, 'veterans': 20, 'homeless': 20, 'justice': 20,
            'rural': 15, 'underserved': 15,

            # Collaboration
            'collaborative': 15, 'partnership': 15, 'coalition': 15,
            'community': 10, 'peer': 10,

            # Non-traditional indicators
            'web3': 25, 'dao': 25, 'gitcoin': 25, 'crypto': 20,
            'retroactive': 20, 'quadratic': 20, 'impact': 15
        }

    def calculate_alignment_score(self, text):
        """Calculate alignment score based on keywords"""
        text_lower = text.lower()
        score = 0
        matched_keywords = []

        for keyword, points in self.alignment_keywords.items():
            if keyword in text_lower:
                score += points
                matched_keywords.append(keyword)

        # Cap at 100
        return min(score, 100), matched_keywords

    def calculate_urgency_score(self, deadline_str):
        """Calculate urgency score based on deadline"""
        if not deadline_str:
            return 0

        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            days_left = (deadline - datetime.now()).days

            if days_left < 0:
                return 0  # Expired
            elif days_left <= 7:
                return 100
            elif days_left <= 14:
                return 80
            elif days_left <= 30:
                return 60
            elif days_left <= 60:
                return 40
            else:
                return 20
        except:
            return 0

    def fetch_and_score_opportunities(self):
        """Fetch all opportunities and calculate scores"""
        url = f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}'
        all_records = []
        offset = None

        # Fetch all records (handling pagination)
        while True:
            params = {}
            if offset:
                params['offset'] = offset

            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"❌ Error fetching data: {response.status_code}")
                return []

            data = response.json()
            all_records.extend(data.get('records', []))

            offset = data.get('offset')
            if not offset:
                break

        # Score each opportunity
        scored_opportunities = []
        for record in all_records:
            fields = record.get('fields', {})

            # Skip if no opportunity name
            if not fields.get('Opportunity Name'):
                continue

            # Calculate alignment score
            search_text = f"{fields.get('Opportunity Name', '')} {fields.get('Description', '')} {fields.get('Funding Source', '')}"
            alignment_score, keywords = self.calculate_alignment_score(search_text)

            # Calculate urgency score
            urgency_score = self.calculate_urgency_score(fields.get('Deadline'))

            # Combined score (60% alignment, 40% urgency)
            combined_score = (alignment_score * 0.6) + (urgency_score * 0.4)

            # Determine type
            opp_type = "Traditional"
            if any(keyword in search_text.lower() for keyword in ['web3', 'dao', 'gitcoin', 'crypto', 'retroactive', 'quadratic']):
                opp_type = "Non-Traditional"

            opportunity = {
                'name': fields.get('Opportunity Name'),
                'amount': fields.get('Funding Amount', 0),
                'deadline': fields.get('Deadline'),
                'source': fields.get('Funding Source', 'Unknown'),
                'type': opp_type,
                'alignment_score': alignment_score,
                'urgency_score': urgency_score,
                'combined_score': combined_score,
                'matched_keywords': keywords,
                'description': fields.get('Description', '')[:100] + '...' if fields.get('Description') else '',
                'link': fields.get('Application Link', ''),
                'record_id': record['id']
            }

            scored_opportunities.append(opportunity)

        # Sort by combined score
        scored_opportunities.sort(key=lambda x: x['combined_score'], reverse=True)

        return scored_opportunities

    def display_dashboard(self, opportunities, args):
        """Display the funding dashboard"""
        # Clear screen for clean display
        if not args.no_clear:
            os.system('clear' if os.name == 'posix' else 'cls')

        # Header
        print("🎯 RECOVERY COMPASS FUNDING DASHBOARD")
        print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # Filter if needed
        filtered_opps = opportunities

        if args.urgent:
            filtered_opps = [o for o in opportunities if o['urgency_score'] >= 80]
            print(f"🚨 Showing URGENT opportunities only (deadline < 14 days)")
        elif args.web3:
            filtered_opps = [o for o in opportunities if o['type'] == 'Non-Traditional']
            print(f"🌐 Showing NON-TRADITIONAL opportunities only")
        elif args.traditional:
            filtered_opps = [o for o in opportunities if o['type'] == 'Traditional']
            print(f"📋 Showing TRADITIONAL opportunities only")

        if args.top:
            filtered_opps = filtered_opps[:args.top]
            print(f"🏆 Showing TOP {args.top} opportunities")

        print()

        # Display opportunities
        for i, opp in enumerate(filtered_opps, 1):
            # Calculate days left
            days_left = "N/A"
            if opp['deadline']:
                try:
                    deadline = datetime.strptime(opp['deadline'], '%Y-%m-%d')
                    days = (deadline - datetime.now()).days
                    if days < 0:
                        days_left = "EXPIRED"
                    else:
                        days_left = f"{days} days"
                except:
                    pass

            # Determine urgency emoji
            urgency_emoji = "🟢"
            if opp['urgency_score'] >= 80:
                urgency_emoji = "🔴"
            elif opp['urgency_score'] >= 60:
                urgency_emoji = "🟡"

            # Display opportunity
            print(f"{i}. {opp['name'][:60]}{'...' if len(opp['name']) > 60 else ''}")
            print(f"   Score: {opp['combined_score']:.0f}/100 | 🎯 {opp['alignment_score']}% aligned | {urgency_emoji} {days_left}")
            print(f"   💰 ${opp['amount']:,} | Type: {opp['type']} | Source: {opp['source']}")

            if args.detail and opp['matched_keywords']:
                print(f"   Keywords: {', '.join(opp['matched_keywords'][:5])}")

            if args.detail and opp['description']:
                print(f"   {opp['description']}")

            print()

        # Summary statistics
        print("=" * 80)
        print("📊 SUMMARY")

        traditional = [o for o in opportunities if o['type'] == 'Traditional']
        non_traditional = [o for o in opportunities if o['type'] == 'Non-Traditional']
        urgent = [o for o in opportunities if o['urgency_score'] >= 80]

        trad_total = sum(o['amount'] for o in traditional)
        non_trad_total = sum(o['amount'] for o in non_traditional)

        print(f"Traditional: {len(traditional)} opportunities (${trad_total:,})")
        print(f"Non-Traditional: {len(non_traditional)} opportunities (${non_trad_total:,})")
        print(f"⚡ Urgent (<14 days): {len(urgent)} opportunities")
        print(f"💎 Total potential: ${trad_total + non_trad_total:,}")

    def export_to_csv(self, opportunities, filename='funding_dashboard.csv'):
        """Export opportunities to CSV"""
        import csv

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Score', 'Alignment', 'Urgency', 'Amount',
                           'Deadline', 'Type', 'Source', 'Keywords', 'Link'])

            for opp in opportunities:
                writer.writerow([
                    opp['name'],
                    f"{opp['combined_score']:.0f}",
                    opp['alignment_score'],
                    opp['urgency_score'],
                    opp['amount'],
                    opp['deadline'] or 'N/A',
                    opp['type'],
                    opp['source'],
                    ', '.join(opp['matched_keywords']),
                    opp['link']
                ])

        print(f"✅ Exported {len(opportunities)} opportunities to {filename}")

    def run_dashboard(self, args):
        """Main dashboard function"""
        print("🔄 Fetching funding opportunities...")
        opportunities = self.fetch_and_score_opportunities()

        if not opportunities:
            print("❌ No opportunities found or error fetching data")
            return

        if args.export:
            self.export_to_csv(opportunities)
        else:
            self.display_dashboard(opportunities, args)

def main():
    parser = argparse.ArgumentParser(
        description='Recovery Compass Funding Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  rc-funding                  # Show all opportunities ranked by score
  rc-funding --urgent         # Show only urgent opportunities (<14 days)
  rc-funding --web3           # Show only non-traditional opportunities
  rc-funding --top 10         # Show only top 10 opportunities
  rc-funding --detail         # Show detailed view with keywords
  rc-funding --export         # Export to CSV file
        """
    )

    parser.add_argument('--urgent', action='store_true', help='Show only urgent opportunities')
    parser.add_argument('--web3', action='store_true', help='Show only non-traditional opportunities')
    parser.add_argument('--traditional', action='store_true', help='Show only traditional opportunities')
    parser.add_argument('--top', type=int, metavar='N', help='Show only top N opportunities')
    parser.add_argument('--detail', action='store_true', help='Show detailed information')
    parser.add_argument('--export', action='store_true', help='Export to CSV instead of display')
    parser.add_argument('--no-clear', action='store_true', help='Do not clear screen')

    args = parser.parse_args()

    dashboard = FundingDashboard()
    dashboard.run_dashboard(args)

if __name__ == "__main__":
    main()
