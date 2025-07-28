"""
Google Sheets Integration for Qualtrics Survey Data
Syncs survey responses and ORIC scores to Google Sheets
"""
import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

from qualtrics_client import QualtricsClient
from oric_calculator import ORICCalculator

load_dotenv()


class GoogleSheetsSync:
    """Sync Qualtrics data to Google Sheets"""
    
    def __init__(self, credentials_path: Optional[str] = None, 
                 sheet_id: Optional[str] = None):
        """
        Initialize Google Sheets connection
        
        Args:
            credentials_path: Path to Google service account credentials
            sheet_id: Google Sheet ID to write to
        """
        self.credentials_path = credentials_path or os.getenv(
            'GOOGLE_CREDENTIALS_FILE'
        )
        self.sheet_id = sheet_id or os.getenv('GOOGLE_SHEET_ID')
        
        if not self.credentials_path:
            raise ValueError("Google credentials path is required")
        if not self.sheet_id:
            raise ValueError("Google Sheet ID is required")
        
        # Initialize Google Sheets service
        self.service = self._init_sheets_service()
        self.qualtrics = QualtricsClient()
        self.oric_calc = ORICCalculator()
    
    def _init_sheets_service(self):
        """Initialize Google Sheets API service"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            return build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            raise Exception(f"Failed to initialize Google Sheets: {str(e)}")
    
    def sync_survey_responses(self, survey_id: str, 
                            sheet_name: str = 'Survey Responses'):
        """
        Sync survey responses to Google Sheet
        
        Args:
            survey_id: Qualtrics survey ID
            sheet_name: Name of the sheet tab to write to
        """
        print(f"Syncing responses for survey {survey_id}...")
        
        # Export responses from Qualtrics
        try:
            file_id = self.qualtrics.export_responses(
                survey_id, 
                format='json'
            )
            response_data = self.qualtrics.download_export_file(
                survey_id, 
                file_id
            )
            
            # Parse the response data
            import zipfile
            import io
            
            with zipfile.ZipFile(io.BytesIO(response_data)) as zf:
                for filename in zf.namelist():
                    if filename.endswith('.json'):
                        with zf.open(filename) as f:
                            data = json.load(f)
                            responses = data.get('responses', [])
                            break
            
            # Process responses and calculate ORIC scores
            processed_data = []
            for response in responses:
                # Extract response values
                values = response.get('values', {})
                
                # Calculate ORIC score
                oric_result = self.oric_calc.calculate_score(values)
                
                # Prepare row data
                row = {
                    'Response ID': response.get('responseId'),
                    'Start Date': response.get('startDate'),
                    'End Date': response.get('endDate'),
                    'Status': response.get('status'),
                    'Progress': response.get('progress'),
                    'Duration': response.get('duration'),
                    'ORIC Overall Score': oric_result['overall_score'],
                    'Readiness Level': oric_result['readiness_level'],
                    'Change Commitment': oric_result['subscale_scores'].get(
                        'change_commitment'
                    ),
                    'Change Efficacy': oric_result['subscale_scores'].get(
                        'change_efficacy'
                    ),
                    'Contextual Factors': oric_result['subscale_scores'].get(
                        'contextual_factors'
                    ),
                    'Sync Timestamp': datetime.now().isoformat()
                }
                
                # Add individual question responses
                for q_id, q_value in values.items():
                    row[f'Response_{q_id}'] = q_value
                
                processed_data.append(row)
            
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(processed_data)
            
            # Write to Google Sheets
            self._write_to_sheet(df, sheet_name)
            
            print(f"Successfully synced {len(processed_data)} responses")
            
            return processed_data
            
        except Exception as e:
            print(f"Error syncing responses: {str(e)}")
            raise
    
    def _write_to_sheet(self, df: pd.DataFrame, sheet_name: str):
        """Write DataFrame to Google Sheet"""
        try:
            # Clear existing data
            range_name = f'{sheet_name}!A1:ZZ10000'
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()
            
            # Prepare data with headers
            values = [df.columns.tolist()] + df.values.tolist()
            
            # Update sheet with new data
            body = {
                'values': values
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f'{sheet_name}!A1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"Updated {result.get('updatedCells')} cells")
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise
    
    def create_dashboard_data(self, survey_id: str, 
                            dashboard_sheet: str = 'Dashboard Data'):
        """
        Create aggregated data for dashboard visualization
        
        Args:
            survey_id: Qualtrics survey ID
            dashboard_sheet: Sheet name for dashboard data
        """
        # Get current responses
        responses = self.sync_survey_responses(survey_id)
        
        if not responses:
            print("No responses to aggregate")
            return
        
        # Calculate aggregated metrics
        df = pd.DataFrame(responses)
        
        # Overall metrics
        metrics = {
            'Total Responses': len(df),
            'Average ORIC Score': df['ORIC Overall Score'].mean(),
            'Low Readiness %': (
                (df['Readiness Level'] == 'low').sum() / len(df) * 100
            ),
            'Moderate Readiness %': (
                (df['Readiness Level'] == 'moderate').sum() / len(df) * 100
            ),
            'High Readiness %': (
                (df['Readiness Level'] == 'high').sum() / len(df) * 100
            ),
            'Avg Change Commitment': df['Change Commitment'].mean(),
            'Avg Change Efficacy': df['Change Efficacy'].mean(),
            'Avg Contextual Factors': df['Contextual Factors'].mean(),
            'Last Updated': datetime.now().isoformat()
        }
        
        # Time series data for trend charts
        df['End Date'] = pd.to_datetime(df['End Date'])
        time_series = df.groupby(df['End Date'].dt.date).agg({
            'ORIC Overall Score': 'mean',
            'Change Commitment': 'mean',
            'Change Efficacy': 'mean',
            'Contextual Factors': 'mean'
        }).reset_index()
        
        # Write metrics to sheet
        metrics_df = pd.DataFrame([metrics])
        self._write_to_sheet(metrics_df, dashboard_sheet)
        
        # Write time series to another sheet
        self._write_to_sheet(time_series, f'{dashboard_sheet}_TimeSeries')
        
        print("Dashboard data created successfully")
        
        return metrics
    
    def setup_auto_sync(self, survey_id: str, webhook_url: str):
        """
        Set up webhook for automatic syncing
        
        Args:
            survey_id: Qualtrics survey ID
            webhook_url: URL to receive webhook events
        """
        try:
            # Create webhook subscription
            result = self.qualtrics.create_webhook(
                subscription_name=f"GoogleSheets_Sync_{survey_id}",
                webhook_url=webhook_url,
                survey_id=survey_id
            )
            
            print(f"Webhook created: {result}")
            return result
            
        except Exception as e:
            print(f"Error creating webhook: {str(e)}")
            raise
    
    def generate_insights_sheet(self, survey_id: str, 
                              insights_sheet: str = 'Insights'):
        """
        Generate insights and recommendations sheet
        
        Args:
            survey_id: Qualtrics survey ID
            insights_sheet: Sheet name for insights
        """
        # Get responses
        responses = self.sync_survey_responses(survey_id)
        
        if not responses:
            print("No responses to analyze")
            return
        
        # Generate insights for each response
        insights_data = []
        
        for response in responses:
            score_data = {
                'overall_score': response['ORIC Overall Score'],
                'subscale_scores': {
                    'change_commitment': response['Change Commitment'],
                    'change_efficacy': response['Change Efficacy'],
                    'contextual_factors': response['Contextual Factors']
                },
                'readiness_level': response['Readiness Level']
            }
            
            insights = self.oric_calc.generate_insights(score_data)
            
            insights_data.append({
                'Response ID': response['Response ID'],
                'ORIC Score': response['ORIC Overall Score'],
                'Readiness Level': response['Readiness Level'],
                'Key Insights': ' | '.join(insights[:3]),
                'All Insights': '\n'.join(insights)
            })
        
        # Write insights to sheet
        insights_df = pd.DataFrame(insights_data)
        self._write_to_sheet(insights_df, insights_sheet)
        
        print(f"Generated insights for {len(insights_data)} responses")
        
        return insights_data


# Example usage script
if __name__ == "__main__":
    # Initialize sync
    sync = GoogleSheetsSync()
    
    # Get survey ID from environment
    survey_id = os.getenv('QUALTRICS_SURVEY_ID')
    
    if survey_id:
        # Sync responses
        sync.sync_survey_responses(survey_id)
        
        # Create dashboard data
        sync.create_dashboard_data(survey_id)
        
        # Generate insights
        sync.generate_insights_sheet(survey_id)
    else:
        print("Please set QUALTRICS_SURVEY_ID in your .env file")
