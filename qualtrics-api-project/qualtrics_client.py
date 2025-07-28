"""
Qualtrics API Client Wrapper
Handles authentication and API calls to Qualtrics Survey Platform
"""
import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class QualtricsClient:
    """Client for interacting with Qualtrics API v3"""
    
    def __init__(self, api_token: Optional[str] = None, data_center: Optional[str] = None):
        self.api_token = api_token or os.getenv('QUALTRICS_API_TOKEN')
        self.data_center = data_center or os.getenv('QUALTRICS_DATA_CENTER')
        
        if not self.api_token:
            raise ValueError("Qualtrics API token is required")
        if not self.data_center:
            raise ValueError("Qualtrics data center URL is required")
        
        self.base_url = f"{self.data_center}/API/v3"
        self.headers = {
            "X-API-TOKEN": self.api_token,
            "Content-Type": "application/json"
        }
    
    def get_survey(self, survey_id: str) -> Dict[str, Any]:
        """Get survey details"""
        response = requests.get(
            f"{self.base_url}/surveys/{survey_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_survey_responses(self, survey_id: str, **kwargs) -> Dict[str, Any]:
        """
        Get survey responses with optional filters
        
        Args:
            survey_id: The survey ID
            **kwargs: Additional parameters like startDate, endDate, limit, etc.
        """
        params = {
            "surveyId": survey_id,
            **kwargs
        }
        
        response = requests.get(
            f"{self.base_url}/surveys/{survey_id}/responses",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def export_responses(self, survey_id: str, format: str = "json", **kwargs) -> str:
        """
        Export survey responses
        
        Args:
            survey_id: The survey ID
            format: Export format (json, csv, tsv, spss)
            **kwargs: Additional export parameters
        """
        # Start export
        export_data = {
            "format": format,
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/surveys/{survey_id}/export-responses",
            headers=self.headers,
            json=export_data
        )
        response.raise_for_status()
        
        progress_id = response.json()["result"]["progressId"]
        
        # Check export progress
        export_ready = False
        file_id = None
        
        while not export_ready:
            progress_response = requests.get(
                f"{self.base_url}/surveys/{survey_id}/export-responses/{progress_id}",
                headers=self.headers
            )
            progress_response.raise_for_status()
            
            progress_data = progress_response.json()
            status = progress_data["result"]["status"]
            
            if status == "complete":
                export_ready = True
                file_id = progress_data["result"]["fileId"]
            elif status == "failed":
                raise Exception("Export failed")
            
            # Wait a bit before checking again
            import time
            time.sleep(1)
        
        return file_id
    
    def download_export_file(self, survey_id: str, file_id: str) -> bytes:
        """Download the exported file"""
        response = requests.get(
            f"{self.base_url}/surveys/{survey_id}/export-responses/{file_id}/file",
            headers=self.headers,
            stream=True
        )
        response.raise_for_status()
        return response.content
    
    def create_webhook(self, subscription_name: str, webhook_url: str, 
                      survey_id: str, event_type: str = "response.completed") -> Dict[str, Any]:
        """
        Create a webhook subscription for survey events
        
        Args:
            subscription_name: Name for the subscription
            webhook_url: URL to receive webhook events
            survey_id: Survey to monitor
            event_type: Type of event to subscribe to
        """
        subscription_data = {
            "subscriptionName": subscription_name,
            "publicationUrl": webhook_url,
            "topics": f"surveyengine.completedResponse.{survey_id}",
            "encrypt": False
        }
        
        response = requests.post(
            f"{self.base_url}/eventsubscriptions",
            headers=self.headers,
            json=subscription_data
        )
        response.raise_for_status()
        return response.json()
    
    def list_webhooks(self) -> List[Dict[str, Any]]:
        """List all webhook subscriptions"""
        response = requests.get(
            f"{self.base_url}/eventsubscriptions",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["result"]["elements"]
    
    def delete_webhook(self, subscription_id: str) -> None:
        """Delete a webhook subscription"""
        response = requests.delete(
            f"{self.base_url}/eventsubscriptions/{subscription_id}",
            headers=self.headers
        )
        response.raise_for_status()
