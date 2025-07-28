"""
Main Script for Qualtrics Survey API Integration
Provides command-line interface for syncing survey data
"""
import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

from qualtrics_client import QualtricsClient
from oric_calculator import ORICCalculator
from google_sheets_sync import GoogleSheetsSync

load_dotenv()


def test_connection():
    """Test Qualtrics API connection"""
    print("Testing Qualtrics API connection...")
    try:
        client = QualtricsClient()
        print(f"✓ Connected to {client.data_center}")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        return False


def list_surveys():
    """List all available surveys"""
    try:
        client = QualtricsClient()
        # Note: You may need to implement a list_surveys method in QualtricsClient
        print("Available surveys:")
        print("Survey ID:", os.getenv('QUALTRICS_SURVEY_ID'))
        # For now, just show the configured survey
        if os.getenv('QUALTRICS_SURVEY_ID'):
            survey = client.get_survey(os.getenv('QUALTRICS_SURVEY_ID'))
            print(f"- {survey['result']['name']} ({survey['result']['id']})")
    except Exception as e:
        print(f"Error listing surveys: {str(e)}")


def sync_to_sheets(survey_id: str = None):
    """Sync survey responses to Google Sheets"""
    survey_id = survey_id or os.getenv('QUALTRICS_SURVEY_ID')
    if not survey_id:
        print("Error: No survey ID provided")
        return
    
    try:
        sync = GoogleSheetsSync()
        
        # Sync responses
        print("\n1. Syncing survey responses...")
        responses = sync.sync_survey_responses(survey_id)
        
        # Create dashboard data
        print("\n2. Creating dashboard data...")
        metrics = sync.create_dashboard_data(survey_id)
        
        # Generate insights
        print("\n3. Generating insights...")
        insights = sync.generate_insights_sheet(survey_id)
        
        print(f"\n✓ Successfully synced {len(responses)} responses")
        print(f"✓ Average ORIC Score: {metrics['Average ORIC Score']:.2f}")
        
    except Exception as e:
        print(f"Error during sync: {str(e)}")


def calculate_oric_demo():
    """Demo ORIC calculation with sample data"""
    print("Demo: Calculating ORIC score from sample responses...")
    
    # Sample survey responses (scale 1-5)
    sample_responses = {
        'Q1': 4,  # Change commitment questions
        'Q2': 3,
        'Q3': 4,
        'Q4': 5,
        'Q5': 4,
        'Q6': 3,  # Change efficacy questions
        'Q7': 3,
        'Q8': 4,
        'Q9': 3,
        'Q10': 4,
        'Q11': 5,  # Contextual factors
        'Q12': 4,
        'Q13': 4,
        'Q14': 5,
        'Q15': 4
    }
    
    calculator = ORICCalculator()
    result = calculator.calculate_score(sample_responses)
    
    print("\nResults:")
    print(f"Overall ORIC Score: {result['overall_score']:.2f}")
    print(f"Readiness Level: {result['readiness_level']}")
    print("\nSubscale Scores:")
    for subscale, score in result['subscale_scores'].items():
        print(f"  {subscale.replace('_', ' ').title()}: {score:.2f}")
    
    # Generate insights
    insights = calculator.generate_insights(result)
    print("\nKey Insights:")
    for insight in insights:
        print(f"  • {insight}")


def setup_webhook(webhook_url: str):
    """Set up webhook for automatic syncing"""
    survey_id = os.getenv('QUALTRICS_SURVEY_ID')
    if not survey_id:
        print("Error: No survey ID configured")
        return
    
    try:
        sync = GoogleSheetsSync()
        result = sync.setup_auto_sync(survey_id, webhook_url)
        print(f"✓ Webhook configured successfully: {result}")
    except Exception as e:
        print(f"Error setting up webhook: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description='Qualtrics Survey API Integration'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Test command
    subparsers.add_parser('test', help='Test API connection')
    
    # List surveys command
    subparsers.add_parser('list', help='List available surveys')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync to Google Sheets')
    sync_parser.add_argument(
        '--survey-id', 
        help='Survey ID to sync (defaults to env var)'
    )
    
    # Demo command
    subparsers.add_parser('demo', help='Demo ORIC calculation')
    
    # Webhook command
    webhook_parser = subparsers.add_parser(
        'webhook', 
        help='Set up webhook for auto-sync'
    )
    webhook_parser.add_argument(
        'webhook_url', 
        help='URL to receive webhook events'
    )
    
    args = parser.parse_args()
    
    if args.command == 'test':
        test_connection()
    elif args.command == 'list':
        list_surveys()
    elif args.command == 'sync':
        sync_to_sheets(args.survey_id)
    elif args.command == 'demo':
        calculate_oric_demo()
    elif args.command == 'webhook':
        setup_webhook(args.webhook_url)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
