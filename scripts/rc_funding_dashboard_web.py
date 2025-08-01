#!/usr/bin/env python3
"""Recovery Compass Funding Dashboard - Brand-Compliant Web Version"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime
import argparse
import webbrowser
from scripts.populate_airtable_funding import FundingPopulator

class FundingDashboardWeb(FundingPopulator):
    def __init__(self):
        super().__init__()
        self.alignment_keywords = {
            # Mental health & recovery (highest priority)
            'recovery': 30, 'mental health': 30, 'substance': 30, 'behavioral': 30,
            'addiction': 30, 'treatment': 25, 'sober': 25, 'housing': 25,
            'trauma-informed': 30, 'healing': 25, 'wellness': 20,

            # Innovation & pilot
            'innovation': 20, 'pilot': 20, 'demonstration': 20, 'technology': 15,
            'digital': 15, 'AI': 15, 'data': 15, 'environmental response': 25,

            # Vulnerable populations
            'youth': 20, 'veterans': 20, 'homeless': 20, 'justice': 20,
            'rural': 15, 'underserved': 15, 'indigenous': 20, 'LGBTQ': 20,

            # Collaboration
            'collaborative': 15, 'partnership': 15, 'coalition': 15,
            'community': 10, 'peer': 10, 'integrated': 15,

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
                print(f"Error fetching data: {response.status_code}")
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
            opp_type = "Traditional Grant"
            if any(keyword in search_text.lower() for keyword in ['web3', 'dao', 'gitcoin', 'crypto', 'retroactive', 'quadratic']):
                opp_type = "Innovation Funding"

            # Calculate days left
            days_left = None
            if fields.get('Deadline'):
                try:
                    deadline = datetime.strptime(fields.get('Deadline'), '%Y-%m-%d')
                    days_left = (deadline - datetime.now()).days
                except:
                    pass

            opportunity = {
                'name': fields.get('Opportunity Name'),
                'amount': fields.get('Funding Amount', 0),
                'deadline': fields.get('Deadline'),
                'days_left': days_left,
                'source': fields.get('Funding Source', 'Unknown'),
                'type': opp_type,
                'alignment_score': alignment_score,
                'urgency_score': urgency_score,
                'combined_score': combined_score,
                'matched_keywords': keywords,
                'description': fields.get('Description', ''),
                'link': fields.get('Application Link', ''),
                'record_id': record['id']
            }

            scored_opportunities.append(opportunity)

        # Sort by combined score
        scored_opportunities.sort(key=lambda x: x['combined_score'], reverse=True)

        return scored_opportunities

    def generate_html_dashboard(self, opportunities):
        """Generate brand-compliant HTML dashboard"""

        # Calculate statistics
        traditional = [o for o in opportunities if o['type'] == 'Traditional Grant']
        innovation = [o for o in opportunities if o['type'] == 'Innovation Funding']
        urgent = [o for o in opportunities if o['urgency_score'] >= 80]

        trad_total = sum(o['amount'] for o in traditional)
        innov_total = sum(o['amount'] for o in innovation)
        total_potential = trad_total + innov_total

        # Generate professional HTML with Recovery Compass branding
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recovery Compass Strategic Funding Intelligence</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            /* Primary Brand Colors */
            --rc-navy-deep: #0a1628;
            --rc-navy: #1a2332;
            --rc-gold: #d4af37;
            --rc-copper: #b87333;
            --rc-cream: #f8f6f1;

            /* Accent & Support Colors */
            --rc-forest: #1e3a2f;
            --rc-gold-light: #e6d19a;
            --rc-copper-light: #d4a574;

            /* Functional Colors */
            --rc-shadow: rgba(10, 22, 40, 0.15);
            --rc-border: rgba(212, 175, 55, 0.2);
            --rc-hover: rgba(212, 175, 55, 0.1);

            /* Spacing System (8-point grid) */
            --space-1: 8px;
            --space-2: 16px;
            --space-3: 24px;
            --space-4: 32px;
            --space-5: 40px;
            --space-6: 48px;
            --space-8: 64px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--rc-cream), #ffffff);
            color: var(--rc-navy);
            font-size: 16px;
            line-height: 1.7;
            font-weight: 500;
            letter-spacing: 0.01em;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: var(--space-3);
        }}

        /* Header Section */
        .header {{
            background: linear-gradient(135deg, var(--rc-navy-deep), var(--rc-navy));
            color: var(--rc-gold);
            padding: 2rem 1.5rem;
            border-bottom: 2px solid var(--rc-gold);
            box-shadow: 0 4px 20px var(--rc-shadow);
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at top right, var(--rc-gold) 0%, transparent 50%);
            opacity: 0.1;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .logo-section {{
            margin-bottom: var(--space-3);
        }}

        .logo {{
            width: 180px;
            height: 180px;
            margin: 0 auto var(--space-2);
            display: block;
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
        }}

        .header h1 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 2.2rem;
            font-weight: 900;
            margin-bottom: var(--space-1);
            letter-spacing: 0.05em;
            font-feature-settings: "liga" 1, "kern" 1, "ss02" 1;
            font-variant-ligatures: common-ligatures;
            text-rendering: optimizeLegibility;
            text-shadow: 0 2px 4px rgba(10, 22, 40, 0.2);
        }}

        .header .subtitle {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            opacity: 0.85;
            letter-spacing: 0.02em;
            margin-bottom: var(--space-2);
        }}

        .header .timestamp {{
            font-family: 'Montserrat', sans-serif;
            font-size: 0.9rem;
            opacity: 0.7;
            font-weight: 500;
            letter-spacing: 0.01em;
        }}

        /* Statistics Cards */
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: var(--space-3);
            margin-bottom: var(--space-5);
        }}

        .stat-card {{
            background: #ffffff;
            border: 1px solid var(--rc-border);
            padding: var(--space-4);
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(10, 22, 40, 0.12),
                       0 1px 2px rgba(10, 22, 40, 0.24);
            transition: all 0.3s ease;
            text-align: center;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(10, 22, 40, 0.15);
        }}

        .stat-card h3 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--rc-forest);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: var(--space-1);
        }}

        .stat-card .value {{
            font-family: 'Montserrat', sans-serif;
            font-size: 2rem;
            font-weight: 900;
            color: var(--rc-navy);
            line-height: 1.2;
            letter-spacing: 0.02em;
        }}

        .stat-card .subvalue {{
            font-family: 'Montserrat', sans-serif;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--rc-forest);
            margin-top: var(--space-1);
            letter-spacing: 0.01em;
        }}

        /* Navigation Filters */
        .filters {{
            display: flex;
            gap: var(--space-2);
            margin-bottom: var(--space-4);
            flex-wrap: wrap;
            justify-content: center;
        }}

        .filter-btn {{
            padding: var(--space-2) var(--space-3);
            border: 2px solid var(--rc-navy);
            background: white;
            color: var(--rc-navy);
            border-radius: 24px;
            cursor: pointer;
            font-family: 'Montserrat', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 0.01em;
            transition: all 0.3s ease;
            min-width: 140px;
            text-align: center;
        }}

        .filter-btn:hover {{
            background: var(--rc-navy);
            color: var(--rc-cream);
            transform: translateY(-1px);
        }}

        .filter-btn.active {{
            background: var(--rc-navy);
            color: var(--rc-cream);
        }}

        /* Opportunities Grid */
        .opportunities {{
            display: grid;
            gap: var(--space-3);
        }}

        .opportunity {{
            background: #ffffff;
            border: 1px solid var(--rc-border);
            padding: var(--space-4);
            border-radius: 12px;
            box-shadow: 0 6px 24px var(--rc-shadow);
            transition: all 0.3s ease;
            border-left: 4px solid var(--rc-copper);
            position: relative;
            overflow: hidden;
        }}

        .opportunity::after {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100%;
            background: linear-gradient(90deg, transparent, var(--rc-gold));
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .opportunity:hover {{
            transform: translateX(4px);
            box-shadow: 0 4px 16px rgba(26, 31, 58, 0.12);
        }}

        .opportunity:hover::after {{
            opacity: 0.05;
        }}

        .opportunity.urgent {{
            border-left-color: var(--rc-gold);
        }}

        .opportunity.soon {{
            border-left-color: var(--rc-copper);
        }}

        .opportunity.normal {{
            border-left-color: var(--rc-forest);
        }}

        .opportunity-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: var(--space-2);
            gap: var(--space-3);
        }}

        .opportunity-title {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--rc-navy);
            line-height: 1.3;
            flex: 1;
            letter-spacing: 0.02em;
        }}

        .score-badge {{
            background: var(--rc-gold);
            color: var(--rc-navy);
            padding: var(--space-1) var(--space-2);
            border-radius: 20px;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 1.125rem;
            white-space: nowrap;
            min-width: 80px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(212, 175, 55, 0.3);
        }}

        .opportunity-meta {{
            display: flex;
            gap: var(--space-3);
            margin-bottom: var(--space-2);
            flex-wrap: wrap;
            align-items: center;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: var(--space-1);
            color: var(--rc-forest);
            font-size: 1rem;
        }}

        .meta-item.amount {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--rc-navy);
            letter-spacing: 0.02em;
        }}

        .meta-item.deadline {{
            font-weight: 600;
        }}

        .deadline.urgent {{
            color: var(--rc-gold);
        }}

        .deadline.soon {{
            color: var(--rc-copper);
        }}

        .deadline.normal {{
            color: var(--rc-forest);
        }}

        .type-badge {{
            background: var(--rc-forest);
            color: var(--rc-cream);
            padding: 6px 16px;
            border-radius: 16px;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.875rem;
            font-weight: 600;
            letter-spacing: 0.01em;
        }}

        .type-badge.innovation {{
            background: var(--rc-gold);
            color: var(--rc-navy);
        }}

        .keywords {{
            margin-top: var(--space-2);
            display: flex;
            gap: var(--space-1);
            flex-wrap: wrap;
        }}

        .keyword {{
            background: rgba(212, 175, 55, 0.1);
            color: var(--rc-copper);
            padding: 4px 12px;
            border-radius: 12px;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.875rem;
            font-weight: 500;
            letter-spacing: 0.01em;
        }}

        .navigate-btn {{
            display: inline-block;
            margin-top: var(--space-3);
            padding: var(--space-2) var(--space-4);
            background: var(--rc-navy);
            color: var(--rc-cream);
            text-decoration: none;
            border-radius: 24px;
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            letter-spacing: 0.01em;
            transition: all 0.3s ease;
            font-size: 1rem;
            border: 2px solid transparent;
        }}

        .navigate-btn:hover {{
            background: var(--rc-forest);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(26, 31, 58, 0.2);
            border-color: var(--rc-gold);
        }}

        .navigate-btn:hover {{
            background: var(--rc-forest);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(26, 31, 58, 0.2);
        }}

        .empty-state {{
            text-align: center;
            padding: var(--space-8);
            color: var(--rc-forest);
        }}

        .empty-state h3 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: var(--space-2);
            letter-spacing: 0.02em;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}

            .stat-card .value {{
                font-size: 1.75rem;
            }}

            .opportunity-header {{
                flex-direction: column;
                gap: var(--space-2);
            }}

            .filters {{
                justify-content: stretch;
            }}

            .filter-btn {{
                flex: 1;
                min-width: auto;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <div class="logo-section">
                    <img src="/static/brand/recovery_compass_logo.png"
                         alt="Recovery Compass - Tree of Life Compass Logo"
                         class="logo"
                         style="width: 180px; height: 180px; object-fit: contain;">
                </div>
                <h1>Recovery Compass Strategic Funding Intelligence</h1>
                <div class="subtitle">Environmental Response Design™ funding insights for transformative care</div>
                <div class="timestamp">Intelligence Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p PST')}</div>
            </div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <h3>Total Opportunities</h3>
                <div class="value">{len(opportunities)}</div>
                <div class="subvalue">Active funding pathways</div>
            </div>
            <div class="stat-card">
                <h3>Total Potential</h3>
                <div class="value">${total_potential:,.0f}</div>
                <div class="subvalue">Available funding</div>
            </div>
            <div class="stat-card">
                <h3>Traditional Grants</h3>
                <div class="value">{len(traditional)}</div>
                <div class="subvalue">${trad_total:,.0f} potential</div>
            </div>
            <div class="stat-card">
                <h3>Innovation Funding</h3>
                <div class="value">{len(innovation)}</div>
                <div class="subvalue">${innov_total:,.0f} potential</div>
            </div>
            <div class="stat-card">
                <h3>Critical Deadlines</h3>
                <div class="value">{len(urgent)}</div>
                <div class="subvalue">Within 14 days</div>
            </div>
        </div>

        <div class="filters">
            <button class="filter-btn active" onclick="filterOpportunities('all')">All Pathways</button>
            <button class="filter-btn" onclick="filterOpportunities('urgent')">Critical Timing</button>
            <button class="filter-btn" onclick="filterOpportunities('traditional')">Traditional</button>
            <button class="filter-btn" onclick="filterOpportunities('innovation')">Innovation</button>
            <button class="filter-btn" onclick="filterOpportunities('high-score')">High Alignment</button>
        </div>

        <div class="opportunities" id="opportunities">
"""

        # Add opportunities
        for opp in opportunities:
            # Determine urgency class
            urgency_class = 'normal'
            if opp['urgency_score'] >= 80:
                urgency_class = 'urgent'
            elif opp['urgency_score'] >= 60:
                urgency_class = 'soon'

            # Days left display
            days_display = 'Timeline unavailable'
            if opp['days_left'] is not None:
                if opp['days_left'] < 0:
                    days_display = 'Opportunity closed'
                elif opp['days_left'] == 0:
                    days_display = 'Final day'
                elif opp['days_left'] == 1:
                    days_display = '1 day remaining'
                else:
                    days_display = f"{opp['days_left']} days remaining"

            # Keywords HTML
            keywords_html = ''
            if opp['matched_keywords']:
                keywords_html = '<div class="keywords">'
                for keyword in opp['matched_keywords'][:6]:
                    # Capitalize keywords professionally
                    display_keyword = keyword.title().replace('Ai', 'AI').replace('Lgbtq', 'LGBTQ')
                    keywords_html += f'<span class="keyword">{display_keyword}</span>'
                keywords_html += '</div>'

            # Type class
            type_class = 'innovation' if opp['type'] == 'Innovation Funding' else ''

            # Application link
            navigate_btn = ''
            if opp['link']:
                navigate_btn = f'<a href="{opp["link"]}" target="_blank" class="navigate-btn">Navigate to Opportunity</a>'

            html += f"""
            <div class="opportunity {urgency_class}"
                 data-type="{opp['type'].lower().replace(' ', '-')}"
                 data-score="{opp['combined_score']}"
                 data-urgency="{opp['urgency_score']}">
                <div class="opportunity-header">
                    <h2 class="opportunity-title">{opp['name']}</h2>
                    <div class="score-badge">{opp['combined_score']:.0f}</div>
                </div>
                <div class="opportunity-meta">
                    <div class="meta-item amount">${opp['amount']:,}</div>
                    <div class="meta-item deadline {urgency_class}">{days_display}</div>
                    <div class="meta-item">{opp['alignment_score']}% strategic alignment</div>
                    <div class="meta-item"><span class="type-badge {type_class}">{opp['type']}</span></div>
                </div>
                <div class="meta-item">Funding Source: {opp['source']}</div>
                {keywords_html}
                {navigate_btn}
            </div>
"""

        # Complete HTML
        html += """
        </div>

        <div class="empty-state" id="empty-state" style="display: none;">
            <h3>No opportunities match your current navigation criteria</h3>
            <p>Adjust your filters to explore different funding pathways</p>
        </div>
    </div>

    <script>
        function filterOpportunities(filter) {
            const opportunities = document.querySelectorAll('.opportunity');
            const buttons = document.querySelectorAll('.filter-btn');
            const emptyState = document.getElementById('empty-state');
            let visibleCount = 0;

            // Update active button
            buttons.forEach(btn => {
                btn.classList.remove('active');
            });

            // Find and activate the correct button
            buttons.forEach(btn => {
                const btnText = btn.textContent.toLowerCase();
                if ((filter === 'all' && btnText.includes('all')) ||
                    (filter === 'urgent' && btnText.includes('critical')) ||
                    (filter === 'traditional' && btnText.includes('traditional')) ||
                    (filter === 'innovation' && btnText.includes('innovation')) ||
                    (filter === 'high-score' && btnText.includes('high'))) {
                    btn.classList.add('active');
                }
            });

            // Filter opportunities
            opportunities.forEach(opp => {
                const type = opp.dataset.type;
                const score = parseFloat(opp.dataset.score);
                const urgency = parseFloat(opp.dataset.urgency);

                let show = false;

                switch(filter) {
                    case 'all':
                        show = true;
                        break;
                    case 'urgent':
                        show = urgency >= 80;
                        break;
                    case 'traditional':
                        show = type === 'traditional-grant';
                        break;
                    case 'innovation':
                        show = type === 'innovation-funding';
                        break;
                    case 'high-score':
                        show = score >= 80;
                        break;
                }

                opp.style.display = show ? 'block' : 'none';
                if (show) visibleCount++;
            });

            // Show/hide empty state
            emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    </script>
</body>
</html>
"""

        return html

    def run_dashboard(self):
        """Main dashboard function"""
        print("\n🧭 Recovery Compass Strategic Funding Intelligence")
        print("━" * 50)
        print("🔄 Accessing funding intelligence database...")

        opportunities = self.fetch_and_score_opportunities()

        if not opportunities:
            print("❌ Unable to access funding intelligence at this time")
            return

        print(f"✅ Analyzed {len(opportunities)} funding opportunities")
        print("🎨 Generating strategic intelligence dashboard...")

        # Generate HTML
        html = self.generate_html_dashboard(opportunities)

        # Save to file
        dashboard_file = os.path.join(os.path.dirname(__file__), 'rc_funding_dashboard.html')
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"💾 Intelligence compiled: {dashboard_file}")
        print("🌐 Launching Recovery Compass funding navigator...")

        # Open in default browser
        webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')

        print("\n✅ Recovery Compass Strategic Funding Intelligence is ready!")
        print("   Navigate wisely towards transformative funding opportunities.")

def main():
    dashboard = FundingDashboardWeb()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()
