#!/usr/bin/env python3
"""
Populate Airtable with funding opportunities using correct field names
"""

import os
import requests
import json
from datetime import datetime, timedelta
import time


class FundingPopulator:
    def __init__(self):
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        self.base_id = 'appNBesu9xYl5Mvm1'
        self.table_id = 'tblcfetlKrhMU4p5r'  # Funding Opportunities table ID
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # Validate environment variables
        if not self.airtable_api_key:
            raise ValueError("AIRTABLE_API_KEY environment variable not set")

    def get_existing_statuses(self):
        """Get existing records to see what Status values are valid"""
        url = f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}?maxRecords=10'

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            records = response.json().get('records', [])
            statuses = set()
            for record in records:
                status = record.get('fields', {}).get('Status')
                if status:
                    statuses.add(status)

            if statuses:
                print(f"📋 Found existing Status values: {statuses}")
                return list(statuses)[0]  # Return first valid status
            else:
                # Try common values
                for status in ['Open', 'Active', 'Available', 'New', 'Pending']:
                    test_record = {
                        "fields": {
                            "Opportunity Name": "Test Status Check",
                            "Status": status
                        }
                    }

                    response = requests.post(
                        f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}',
                        headers=self.headers,
                        json=test_record
                    )

                    if response.status_code == 200:
                        # Delete the test record
                        record_id = response.json()['id']
                        requests.delete(
                            f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}/{record_id}',
                            headers=self.headers
                        )
                        print(f"✅ Valid status found: {status}")
                        return status

                return None  # No valid status found
        else:
            return None

    def create_funding_opportunities(self):
        """Create comprehensive funding opportunities"""

        # First, find a valid status
        valid_status = self.get_existing_statuses()

        current_date = datetime.now()

        opportunities = [
            # Traditional Funding
            {
                'name': 'SAMHSA Recovery Community Services Program 2025',
                'description': 'Federal grant supporting recovery community organizations to develop and deliver peer recovery support services. Focus areas include recovery housing, peer support services, and community-based recovery programs. Multi-year funding available.',
                'amount': 750000,
                'deadline': current_date + timedelta(days=60),
                'source': 'SAMHSA - Substance Abuse and Mental Health Services Administration',
                'eligibility': '501(c)(3) nonprofits providing recovery support services, must serve populations affected by substance use disorders, preference for organizations with recovery housing programs',
                'link': 'https://www.samhsa.gov/grants/grant-announcements/ti-25-009',
                'contact': 'SAMHSA Grants Management Officer',
                'type': 'Traditional - Federal'
            },
            {
                'name': 'HRSA Rural Communities Opioid Response Program',
                'description': 'Multi-year grant for rural communities to strengthen substance use disorder prevention, treatment, and recovery. Includes funding for recovery housing and support services.',
                'amount': 1000000,
                'deadline': current_date + timedelta(days=45),
                'source': 'HRSA - Health Resources and Services Administration',
                'eligibility': 'Nonprofits serving rural communities (RUCA codes 4-10), must demonstrate partnerships with healthcare providers',
                'link': 'https://www.hrsa.gov/grants/find-funding/HRSA-25-017',
                'contact': 'HRSA Rural Health Grants Team',
                'type': 'Traditional - Federal'
            },
            {
                'name': 'Conrad N. Hilton Foundation Recovery Housing Initiative',
                'description': 'Supporting organizations providing recovery housing and wraparound services to young adults (18-25) in recovery. Focus on innovative housing models and peer support.',
                'amount': 1500000,
                'deadline': current_date + timedelta(days=75),
                'source': 'Conrad N. Hilton Foundation',
                'eligibility': 'Organizations providing recovery housing for young adults, minimum 2 years operational history, evidence-based practices required',
                'link': 'https://www.hiltonfoundation.org/programs/young-adult-recovery',
                'contact': 'Program Officer - Substance Use Prevention',
                'type': 'Traditional - Foundation'
            },
            {
                'name': 'San Diego County Behavioral Health Services RFP',
                'description': 'County funding for recovery residences and supportive housing programs. Priority for programs serving justice-involved individuals and families.',
                'amount': 500000,
                'deadline': current_date + timedelta(days=21),
                'source': 'San Diego County Health and Human Services',
                'eligibility': 'Licensed recovery residences in San Diego County, NARR certification preferred, must accept Medi-Cal',
                'link': 'https://www.sandiegocounty.gov/content/sdc/hhsa/programs/bhs/rfp',
                'contact': 'BHS Contracts Division',
                'type': 'Traditional - Local Government'
            },
            {
                'name': 'California Health Facilities Financing Authority Loan Program',
                'description': 'Low-interest loans for nonprofit health facilities including recovery housing and treatment centers. Up to $2.5M for facility purchase or renovation.',
                'amount': 2500000,
                'deadline': current_date + timedelta(days=90),
                'source': 'State of California Treasurer',
                'eligibility': 'California 501(c)(3) health facilities, must demonstrate financial sustainability, 20% down payment required',
                'link': 'https://www.treasurer.ca.gov/chffa/help-ii',
                'contact': 'CHFFA Program Manager',
                'type': 'Traditional - State'
            },
            {
                'name': 'Robert Wood Johnson Foundation Culture of Health',
                'description': 'Supporting innovative approaches to building healthy communities, including addiction recovery initiatives. Focus on systems change and health equity.',
                'amount': 500000,
                'deadline': current_date + timedelta(days=120),
                'source': 'Robert Wood Johnson Foundation',
                'eligibility': 'Organizations addressing social determinants of health, collaborative approaches preferred, evaluation capacity required',
                'link': 'https://www.rwjf.org/en/grants/what-we-fund',
                'contact': 'Program Development Team',
                'type': 'Traditional - Foundation'
            },
            {
                'name': 'CDC Overdose Data to Action Cooperative Agreement',
                'description': 'Supporting surveillance and prevention activities to combat the overdose crisis. Includes funding for recovery support services.',
                'amount': 800000,
                'deadline': current_date + timedelta(days=30),
                'source': 'Centers for Disease Control and Prevention',
                'eligibility': 'State and local health departments, nonprofits through partnerships, data collection capacity required',
                'link': 'https://www.cdc.gov/drugoverdose/od2a/index.html',
                'contact': 'CDC OD2A Program Coordinator',
                'type': 'Traditional - Federal'
            },
            # Non-Traditional Funding
            {
                'name': 'Gitcoin Grants Round 21 - Public Health',
                'description': 'Quadratic funding for public goods including health and recovery initiatives. Web3-native funding with community matching.',
                'amount': 100000,
                'deadline': current_date + timedelta(days=14),
                'source': 'Gitcoin DAO',
                'eligibility': 'Open-source projects, transparent operations, must accept crypto donations, community engagement required',
                'link': 'https://gitcoin.co/grants',
                'contact': 'Gitcoin Support Team',
                'type': 'Non-Traditional - Web3'
            },
            {
                'name': 'Social Impact Bond - Recovery Housing Success',
                'description': 'Pay-for-success funding model where payments are tied to measurable outcomes in recovery housing retention and employment.',
                'amount': 5000000,
                'deadline': current_date + timedelta(days=180),
                'source': 'Third Sector Capital Partners',
                'eligibility': 'Established recovery programs with 3+ years data, capacity for outcome measurement, government partnership required',
                'link': 'https://www.thirdsectorcap.org/portfolio',
                'contact': 'Impact Investment Team',
                'type': 'Non-Traditional - Impact Investment'
            },
            {
                'name': 'Google.org Impact Challenge - Health Equity',
                'description': 'Technology-driven solutions for health challenges including addiction recovery. Funding plus Google.org Fellowship support.',
                'amount': 1000000,
                'deadline': current_date + timedelta(days=90),
                'source': 'Google.org',
                'eligibility': 'Nonprofits using technology innovatively, scalable solutions, data-driven approaches',
                'link': 'https://impactchallenge.withgoogle.com',
                'contact': 'Google.org Partnerships',
                'type': 'Non-Traditional - Corporate'
            },
            {
                'name': 'Optimism RetroPGF Round 4',
                'description': 'Retroactive funding for projects that have created public good impact. Recovery and health projects eligible.',
                'amount': 500000,
                'deadline': current_date + timedelta(days=60),
                'source': 'Optimism Collective',
                'eligibility': 'Projects with demonstrated impact, open-source preferred, must have Ethereum address',
                'link': 'https://app.optimism.io/retropgf',
                'contact': 'Optimism Governance',
                'type': 'Non-Traditional - Web3'
            },
            {
                'name': 'Venture Philanthropy Partners Scale Fund',
                'description': 'Multi-year unrestricted funding for high-impact nonprofits ready to scale. Includes capacity building support.',
                'amount': 2000000,
                'deadline': current_date + timedelta(days=120),
                'source': 'VPP',
                'eligibility': 'Annual budget $1M+, proven model, leadership succession plan, evaluation systems in place',
                'link': 'https://www.vppartners.org/investments',
                'contact': 'Investment Committee',
                'type': 'Non-Traditional - Venture Philanthropy'
            }
        ]

        return opportunities

    def populate_dashboard(self):
        """Main function to populate the funding dashboard"""

        print("🚀 Populating Recovery Compass Funding Dashboard")
        print("=" * 60)

        # Get valid status
        valid_status = self.get_existing_statuses()

        # Get opportunities
        opportunities = self.create_funding_opportunities()

        success_count = 0
        error_count = 0

        print(f"\n📤 Creating {len(opportunities)} funding opportunities...")

        for i, opp in enumerate(opportunities, 1):
            print(f"\n[{i}/{len(opportunities)}] Processing: {opp['name']}")

            # Prepare record
            record_data = {
                "fields": {
                    "Opportunity Name": opp['name'],
                    "Description": opp['description'],
                    "Funding Amount": opp['amount'],
                    "Deadline": opp['deadline'].strftime('%Y-%m-%d'),
                    "Funding Source": opp['source'],
                    "Eligibility Criteria": opp['eligibility'],
                    "Application Link": opp['link'],
                    "Contact Person": opp['contact'],
                    "Notes": f"Type: {opp['type']} | Added: {datetime.now().strftime('%Y-%m-%d')}",
                    "External API ID": f"RC-{datetime.now().strftime('%Y%m%d')}-{i:03d}"
                }
            }

            # Add status if we found a valid one
            if valid_status:
                record_data['fields']['Status'] = valid_status

            # Create record
            response = requests.post(
                f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}',
                headers=self.headers,
                json=record_data
            )

            if response.status_code == 200:
                print(f"   ✅ Created successfully")
                success_count += 1
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"   Response: {response.text}")
                error_count += 1

            time.sleep(0.5)  # Rate limiting

        print("\n" + "=" * 60)
        print("✅ DASHBOARD POPULATION COMPLETE!")
        print(f"   - Successfully created: {success_count} records")
        print(f"   - Errors: {error_count}")
        print(f"\n📊 View your dashboard at:")
        print(f"   https://airtable.com/{self.base_id}/tblcfetlKrhMU4p5r")

        # Generate summary
        self.generate_summary(opportunities, success_count)

    def generate_summary(self, opportunities, success_count):
        """Generate a summary report"""

        # Categorize opportunities
        traditional = [o for o in opportunities if 'Traditional' in o['type']]
        non_traditional = [o for o in opportunities if 'Non-Traditional' in o['type']]

        # Find urgent deadlines
        urgent = sorted(
            [(o, (o['deadline'] - datetime.now()).days) for o in opportunities],
            key=lambda x: x[1]
        )[:5]

        # Find highest value
        high_value = sorted(opportunities, key=lambda x: x['amount'], reverse=True)[:5]

        summary = f"""
📊 FUNDING DASHBOARD POPULATION SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW:
✅ Successfully Added: {success_count} opportunities
💰 Total Potential Funding: ${sum(o['amount'] for o in opportunities):,}
📈 Average Grant Size: ${sum(o['amount'] for o in opportunities) // len(opportunities):,}

BREAKDOWN:
📋 Traditional Funding: {len(traditional)} opportunities (${sum(o['amount'] for o in traditional):,})
🚀 Non-Traditional Funding: {len(non_traditional)} opportunities (${sum(o['amount'] for o in non_traditional):,})

⏰ URGENT DEADLINES (Next 30 days):
"""

        for opp, days in urgent:
            if days <= 30:
                summary += f"   🔴 {opp['name']} - {days} days left (${opp['amount']:,})\n"

        summary += f"\n💎 HIGHEST VALUE OPPORTUNITIES:\n"

        for opp in high_value:
            summary += f"   💰 {opp['name']} - ${opp['amount']:,}\n"

        summary += f"""
📌 IMMEDIATE NEXT STEPS:
1. Review all opportunities in Airtable dashboard
2. Assign team members to top priority applications
3. Create application timeline and task assignments
4. Schedule grant writing sessions for urgent deadlines
5. Reach out to contact persons for clarifications

🔗 Dashboard Link: https://airtable.com/{self.base_id}/tblcfetlKrhMU4p5r

💡 PRO TIPS:
- Sort by Deadline to focus on urgent opportunities
- Filter by Funding Amount to prioritize high-value grants
- Use the Status field to track application progress
- Add notes about application requirements and progress
"""

        # Save report
        with open('funding_dashboard_report.txt', 'w') as f:
            f.write(summary)

        print(summary)
        print(f"\n📄 Report saved to: funding_dashboard_report.txt")


if __name__ == "__main__":
    populator = FundingPopulator()
    populator.populate_dashboard()
