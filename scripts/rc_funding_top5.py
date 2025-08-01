#!/usr/bin/env python3
"""Recovery Compass Top 5 Funding Dashboard - Dual Table View"""

import os
import sys
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.rc_funding_dashboard_web import FundingDashboardWeb


class FundingTop5Dashboard(FundingDashboardWeb):
    def __init__(self):
        super().__init__()

        # Enhanced categorization patterns
        self.traditional_patterns = [
            'samhsa', 'hrsa', 'cdc', 'federal', 'state', 'county', 'foundation',
            'robert wood johnson', 'conrad hilton', 'government', 'cooperative agreement',
            'block grant', 'categorical grant'
        ]

        self.non_traditional_patterns = [
            'web3', 'dao', 'gitcoin', 'crypto', 'retroactive', 'quadratic',
            'social impact bond', 'sib', 'impact investment', 'pay for success',
            'venture philanthropy', 'corporate', 'google.org', 'crowdfunding',
            'mission-related investment', 'mri', 'optimism'
        ]

    def categorize_opportunity(self, opportunity):
        """Enhanced categorization logic"""
        search_text = f"{opportunity.get('name', '')} {opportunity.get('source', '')} {opportunity.get('description', '')}".lower()

        # Check patterns
        for pattern in self.non_traditional_patterns:
            if pattern in search_text:
                return 'Non-Traditional'

        for pattern in self.traditional_patterns:
            if pattern in search_text:
                return 'Traditional'

        # Fallback based on existing type field
        if 'type' in opportunity:
            if any(word in opportunity['type'].lower() for word in ['web3', 'impact', 'venture', 'corporate']):
                return 'Non-Traditional'

        return 'Traditional'  # Default to traditional if uncertain

    def calculate_rc_score(self, opportunity):
        """Calculate RC-Score = Impact × Fit × Probability"""

        # Impact Score (based on amount and reach)
        amount = opportunity.get('amount', 0)
        if amount >= 2000000:
            impact_score = 100
        elif amount >= 1000000:
            impact_score = 80
        elif amount >= 500000:
            impact_score = 60
        elif amount >= 100000:
            impact_score = 40
        else:
            impact_score = 20

        # Fit Score (based on alignment keywords)
        search_text = f"{opportunity.get('name', '')} {opportunity.get('description', '')}".lower()
        fit_score, _ = self.calculate_alignment_score(search_text)

        # Probability Score (based on eligibility match and deadline)
        probability_score = 50  # Base score

        # Boost for matching eligibility
        eligibility = opportunity.get('eligibility', '').lower()
        if '501(c)(3)' in eligibility:
            probability_score += 20
        if 'recovery' in eligibility or 'substance' in eligibility:
            probability_score += 15
        if 'california' in eligibility or 'san diego' in eligibility:
            probability_score += 15

        # Adjust for deadline urgency
        urgency = self.calculate_urgency_score(opportunity.get('deadline'))
        if urgency >= 80:  # Very urgent
            probability_score -= 10  # Harder to prepare in time
        elif urgency >= 40:  # Reasonable timeline
            probability_score += 10

        probability_score = min(100, probability_score)

        # Calculate composite RC-Score
        rc_score = (impact_score * 0.3 + fit_score * 0.4 + probability_score * 0.3)

        return {
            'rc_score': rc_score,
            'impact': impact_score,
            'fit': fit_score,
            'probability': probability_score
        }

    def fetch_and_categorize_opportunities(self):
        """Fetch, categorize, and score all opportunities"""
        # Get base opportunities
        opportunities = self.fetch_and_score_opportunities()

        # Enhance with categorization and RC-Score
        for opp in opportunities:
            opp['category'] = self.categorize_opportunity(opp)
            scores = self.calculate_rc_score(opp)
            opp.update(scores)

        return opportunities

    def generate_top5_html(self, traditional_top5, non_traditional_top5):
        """Generate dual-table HTML dashboard"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#1a1f3a">
    <title>Recovery Compass Top 5 Funding Opportunities</title>
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
            max-width: 1400px;
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

        .logo {{
            width: 120px;
            height: 120px;
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
        }}

        /* Dual Table Layout */
        .tables-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: var(--space-4);
            margin-top: var(--space-5);
        }}

        @media (max-width: 1024px) {{
            .tables-container {{
                grid-template-columns: 1fr;
            }}
        }}

        .table-section {{
            background: #ffffff;
            border: 1px solid var(--rc-border);
            border-radius: 12px;
            padding: var(--space-4);
            box-shadow: 0 6px 24px var(--rc-shadow);
            transition: all 0.3s ease;
        }}

        .table-section:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 32px var(--rc-shadow);
        }}

        .table-header {{
            display: flex;
            align-items: center;
            gap: var(--space-2);
            margin-bottom: var(--space-3);
            padding-bottom: var(--space-2);
            border-bottom: 2px solid var(--rc-navy);
        }}

        .table-icon {{
            width: 40px;
            height: 40px;
            background: var(--rc-gold);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }}

        .table-title {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--rc-navy);
            letter-spacing: 0.03em;
        }}

        .opportunity-row {{
            padding: var(--space-3);
            border-bottom: 1px solid rgba(26, 31, 58, 0.1);
            transition: all 0.3s ease;
        }}

        .opportunity-row:last-child {{
            border-bottom: none;
        }}

        .opportunity-row:hover {{
            background: var(--rc-hover);
            transform: translateX(4px);
            box-shadow: inset 0 0 0 2px var(--rc-border);
        }}

        .row-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: var(--space-2);
        }}

        .opportunity-name {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            font-size: 1.125rem;
            color: var(--rc-navy);
            flex: 1;
            margin-right: var(--space-2);
            letter-spacing: 0.01em;
        }}

        .rc-score-badge {{
            background: var(--rc-gold);
            color: var(--rc-navy);
            padding: 6px 14px;
            border-radius: 20px;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 0.875rem;
            white-space: nowrap;
            box-shadow: 0 2px 4px rgba(212, 175, 55, 0.3);
        }}

        .opportunity-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: var(--space-2);
            margin-bottom: var(--space-2);
        }}

        .detail-item {{
            font-family: 'Montserrat', sans-serif;
            font-size: 0.875rem;
        }}

        .detail-label {{
            color: var(--rc-forest);
            font-weight: 500;
            letter-spacing: 0.01em;
        }}

        .detail-value {{
            color: var(--rc-navy);
            font-weight: 600;
            letter-spacing: 0.01em;
        }}

        .amount {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--rc-forest);
            letter-spacing: 0.02em;
        }}

        .deadline {{
            color: var(--rc-copper);
            font-weight: 600;
        }}

        .scores-breakdown {{
            display: flex;
            gap: var(--space-3);
            margin-top: var(--space-2);
            padding-top: var(--space-2);
            border-top: 1px solid rgba(26, 31, 58, 0.05);
        }}

        .score-item {{
            font-family: 'Montserrat', sans-serif;
            font-size: 0.75rem;
            color: var(--rc-forest);
            letter-spacing: 0.01em;
        }}

        .score-value {{
            font-weight: 700;
            color: var(--rc-navy);
        }}

        .view-link {{
            display: inline-block;
            margin-top: var(--space-2);
            padding: var(--space-1) var(--space-2);
            color: var(--rc-navy);
            text-decoration: none;
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.3s ease;
            border-bottom: 2px solid transparent;
        }}

        .view-link:hover {{
            color: var(--rc-gold);
            transform: translateX(4px);
            border-bottom-color: var(--rc-gold);
        }}

        /* Summary Stats */
        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--space-3);
            margin: var(--space-5) 0;
        }}

        .stat-card {{
            background: #ffffff;
            border: 1px solid var(--rc-border);
            padding: var(--space-3);
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(10, 22, 40, 0.12),
                       0 1px 2px rgba(10, 22, 40, 0.24);
            transition: all 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(10, 22, 40, 0.15);
        }}

        .stat-value {{
            font-family: 'Montserrat', sans-serif;
            font-size: 2rem;
            font-weight: 900;
            color: var(--rc-navy);
            letter-spacing: 0.02em;
        }}

        .stat-label {{
            font-family: 'Montserrat', sans-serif;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--rc-forest);
            margin-top: var(--space-1);
            letter-spacing: 0.01em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <img src="/static/brand/recovery_compass_logo.png"
                     alt="Recovery Compass Logo"
                     class="logo"
                     style="object-fit: contain;">
                <h1>Top 5 Funding Opportunities</h1>
                <div class="subtitle">Strategic funding intelligence powered by RC-Score™ algorithm</div>
            </div>
        </div>

        <div class="summary-stats">
            <div class="stat-card">
                <div class="stat-value">${sum(o['amount'] for o in traditional_top5):,.0f}</div>
                <div class="stat-label">Traditional Funding Potential</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${sum(o['amount'] for o in non_traditional_top5):,.0f}</div>
                <div class="stat-label">Non-Traditional Funding Potential</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${sum(o['amount'] for o in traditional_top5 + non_traditional_top5):,.0f}</div>
                <div class="stat-label">Total Top 10 Potential</div>
            </div>
        </div>

        <div class="tables-container">
            <!-- Traditional Funding Table -->
            <div class="table-section">
                <div class="table-header">
                    <div class="table-icon">📋</div>
                    <h2 class="table-title">Top 5 Traditional</h2>
                </div>
"""

        # Add traditional opportunities
        for i, opp in enumerate(traditional_top5, 1):
            days_left = opp.get('days_left', 'N/A')
            if isinstance(days_left, int):
                days_text = f"{days_left}d" if days_left > 0 else "Expired"
            else:
                days_text = "TBD"

            html += f"""
                <div class="opportunity-row">
                    <div class="row-header">
                        <div class="opportunity-name">{i}. {opp['name']}</div>
                        <div class="rc-score-badge">RC: {opp['rc_score']:.0f}</div>
                    </div>
                    <div class="opportunity-details">
                        <div class="detail-item">
                            <span class="detail-label">Amount:</span>
                            <span class="detail-value amount">${opp['amount']:,}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Deadline:</span>
                            <span class="detail-value deadline">{days_text}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Source:</span>
                            <span class="detail-value">{opp['source'][:30]}...</span>
                        </div>
                    </div>
                    <div class="scores-breakdown">
                        <div class="score-item">Impact: <span class="score-value">{opp['impact']}</span></div>
                        <div class="score-item">Fit: <span class="score-value">{opp['fit']}</span></div>
                        <div class="score-item">Probability: <span class="score-value">{opp['probability']}</span></div>
                    </div>
                    {f'<a href="{opp["link"]}" target="_blank" class="view-link">View Opportunity →</a>' if opp.get('link') else ''}
                </div>
"""

        html += """
            </div>

            <!-- Non-Traditional Funding Table -->
            <div class="table-section">
                <div class="table-header">
                    <div class="table-icon">🚀</div>
                    <h2 class="table-title">Top 5 Non-Traditional</h2>
                </div>
"""

        # Add non-traditional opportunities
        for i, opp in enumerate(non_traditional_top5, 1):
            days_left = opp.get('days_left', 'N/A')
            if isinstance(days_left, int):
                days_text = f"{days_left}d" if days_left > 0 else "Expired"
            else:
                days_text = "TBD"

            html += f"""
                <div class="opportunity-row">
                    <div class="row-header">
                        <div class="opportunity-name">{i}. {opp['name']}</div>
                        <div class="rc-score-badge">RC: {opp['rc_score']:.0f}</div>
                    </div>
                    <div class="opportunity-details">
                        <div class="detail-item">
                            <span class="detail-label">Amount:</span>
                            <span class="detail-value amount">${opp['amount']:,}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Deadline:</span>
                            <span class="detail-value deadline">{days_text}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Source:</span>
                            <span class="detail-value">{opp['source'][:30]}...</span>
                        </div>
                    </div>
                    <div class="scores-breakdown">
                        <div class="score-item">Impact: <span class="score-value">{opp['impact']}</span></div>
                        <div class="score-item">Fit: <span class="score-value">{opp['fit']}</span></div>
                        <div class="score-item">Probability: <span class="score-value">{opp['probability']}</span></div>
                    </div>
                    {f'<a href="{opp["link"]}" target="_blank" class="view-link">View Opportunity →</a>' if opp.get('link') else ''}
                </div>
"""

        html += """
            </div>
        </div>
    </div>
</body>
</html>
"""

        return html

    def run_top5_dashboard(self, output_dir='out'):
        """Main function to generate top 5 dashboard"""
        print("\n🧭 Recovery Compass Top 5 Funding Intelligence")
        print("━" * 50)
        print("🔄 Analyzing funding opportunities...")

        # Fetch and categorize
        opportunities = self.fetch_and_categorize_opportunities()

        # Separate by category
        traditional = [o for o in opportunities if o['category'] == 'Traditional']
        non_traditional = [o for o in opportunities if o['category'] == 'Non-Traditional']

        # Sort by RC-Score and take top 5 of each
        traditional_top5 = sorted(traditional, key=lambda x: x['rc_score'], reverse=True)[:5]
        non_traditional_top5 = sorted(non_traditional, key=lambda x: x['rc_score'], reverse=True)[:5]

        print(f"✅ Found {len(traditional)} traditional opportunities")
        print(f"✅ Found {len(non_traditional)} non-traditional opportunities")
        print("🎯 Selected top 5 of each category based on RC-Score")

        # Generate HTML
        html = self.generate_top5_html(traditional_top5, non_traditional_top5)

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'funding'), exist_ok=True)

        # Save to file
        output_file = os.path.join(output_dir, 'funding', 'top5.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"💾 Dashboard saved to: {output_file}")

        # Generate summary
        total_traditional = sum(o['amount'] for o in traditional_top5)
        total_non_traditional = sum(o['amount'] for o in non_traditional_top5)

        print("\n📊 Top 5 Summary:")
        print(f"   Traditional: ${total_traditional:,.0f}")
        print(f"   Non-Traditional: ${total_non_traditional:,.0f}")
        print(f"   Total Potential: ${total_traditional + total_non_traditional:,.0f}")

        return output_file

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate Recovery Compass Top 5 Funding Dashboard')
    parser.add_argument('--output', '-o', default='out', help='Output directory')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser')

    args = parser.parse_args()

    dashboard = FundingTop5Dashboard()
    output_file = dashboard.run_top5_dashboard(args.output)

    if not args.no_browser:
        webbrowser.open(f'file://{os.path.abspath(output_file)}')

if __name__ == "__main__":
    main()
