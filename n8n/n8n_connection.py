import requests
import json
import math
import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import Dict, List, Optional, Any
import logging
import os
import sys

# NEW: reach the utils/ package at the project root for the resume text parser
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.resume_data import parse_education, parse_work_experience, parse_projects

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _json_safe(value: Any) -> Any:
    """
    Recursively converts a value into something Python's json module (and
    therefore requests' json= parameter) can actually serialize.

    BUG FIX: matching_jobs.to_dict('records') can contain pandas.Timestamp
    (e.g. from a 'posted_date' column that Excel or pandas parsed as a real
    date rather than plain text), pandas.NaT, NaN floats, or numpy scalar
    types (np.int64, np.float64, np.bool_) — none of which the standard
    json encoder knows how to handle, which is exactly what caused:
        "Error sending data: Object of type Timestamp is not JSON serializable"
    This walks the whole payload and converts anything like that into a
    plain str/int/float/bool/None before it ever reaches json.dumps().
    """
    if value is None:
        return None
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    # NaT must be checked before the Timestamp/datetime branch below —
    # pandas.NaTType actually satisfies isinstance(value, datetime), so it
    # would otherwise fall into that branch and serialize as the string
    # "NaT" instead of a proper JSON null.
    if value is pd.NaT:
        return None
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        f = float(value)
        return None if math.isnan(f) else f
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

class N8NConnection:
    """Simple connection to n8n cloud webhook"""
    
    def __init__(self, webhook_url: str):
        """
        Initialize N8N connection with your webhook URL
        
        Args:
            webhook_url: Your n8n cloud webhook URL
                        Example: https://your-instance.n8n.cloud/webhook/your-webhook-path
        """
        self.webhook_url = webhook_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.timeout = 60  # 60 seconds timeout
    
    def send_data(self, data: Dict) -> Dict:
        """
        Send data to n8n webhook
        
        Args:
            data: Dictionary containing data to send
            
        Returns:
            Response from n8n
        """
        try:
            logger.info(f"Sending data to n8n webhook: {self.webhook_url}")
            
            # BUG FIX: sanitize before serializing so any pandas Timestamp /
            # NaT / numpy scalar hiding in the data (most commonly from an
            # Excel date column) can't blow up json.dumps() inside requests.
            safe_data = _json_safe(data)
            
            response = requests.post(
                self.webhook_url,
                json=safe_data,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info("Successfully sent data to n8n")
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'response': response.json() if response.content else {},
                    'message': 'Data sent successfully'
                }
            else:
                logger.error(f"Failed to send data: HTTP {response.status_code}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': f"HTTP {response.status_code}",
                    'response': response.text
                }
                
        except requests.exceptions.Timeout:
            logger.error("Timeout while sending data to n8n")
            return {
                'success': False,
                'error': 'Request timeout'
            }
        except requests.exceptions.ConnectionError:
            logger.error("Connection error while sending data to n8n")
            return {
                'success': False,
                'error': 'Connection failed'
            }
        except Exception as e:
            logger.error(f"Error sending data: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_job_matching_data(
        self,
        user_data: Dict,
        matching_jobs: pd.DataFrame,
        model_info: Optional[Dict] = None
    ) -> Dict:
        """
        Send user data and matching jobs to n8n
        
        Args:
            user_data: Dictionary containing user information
            matching_jobs: DataFrame containing matching jobs
            model_info: Optional information about the ML model used
            
        Returns:
            Response from n8n
        """
        # Prepare payload
        payload = {
            'timestamp': datetime.now().isoformat(),
            'data_type': 'job_matching',
            'user': {
                'email': user_data.get('email', ''),
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'profession': user_data.get('profession', ''),
                'experience_years': float(user_data.get('experience', 0)),
                'skills': self._parse_skills(user_data.get('skills', '')),
                'preferred_domains': [
                    user_data.get('preferred_domain_1', ''),
                    user_data.get('preferred_domain_2', ''),
                    user_data.get('preferred_domain_3', '')
                ],
                # NEW: structured resume data for the Jake's Resume LaTeX
                # template. Raw text from the Tkinter form is parsed here
                # (Python side) rather than in n8n, so the workflow always
                # receives clean, predictable JSON instead of pipe-delimited
                # strings it would have to re-parse itself.
                'location': user_data.get('location', ''),
                'education': parse_education(user_data.get('education_raw', '')),
                'work_experience': parse_work_experience(user_data.get('work_experience_raw', '')),
                'projects': parse_projects(user_data.get('projects_raw', ''))
            },
            'matching_jobs': matching_jobs.to_dict('records') if not matching_jobs.empty else [],
            'total_matches': len(matching_jobs) if not matching_jobs.empty else 0,
            'model_info': model_info or {}
        }
        
        # Send to n8n
        return self.send_data(payload)
    
    def send_custom_data(self, data: Dict) -> Dict:
        """
        Send custom data to n8n
        
        Args:
            data: Any custom data dictionary
            
        Returns:
            Response from n8n
        """
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        return self.send_data(data)
    
    def test_connection(self) -> bool:
        """
        Test connection to n8n webhook
        
        Returns:
            True if connection successful, False otherwise
        """
        test_data = {
            'test': True,
            'timestamp': datetime.now().isoformat(),
            'message': 'Connection test from Job Matching System'
        }
        
        result = self.send_data(test_data)
        return result.get('success', False)
    
    def _parse_skills(self, skills: str) -> List[str]:
        """Parse skills string into list"""
        if not skills:
            return []
        
        # Split by comma and clean
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
        return skill_list


# Example usage and configuration
if __name__ == "__main__":
    # REPLACE THIS WITH YOUR N8N CLOUD WEBHOOK URL
    N8N_WEBHOOK_URL = "https://aravinth1198.app.n8n.cloud/webhook/153b9105-702d-4485-95fd-5b1a1a904aa9"
    
    # Create connection
    n8n = N8NConnection(N8N_WEBHOOK_URL)
    
    # Test connection
    print("Testing connection to n8n...")
    if n8n.test_connection():
        print("✓ Connection successful!")
    else:
        print("✗ Connection failed. Check your webhook URL.")
    
    # Example user data
    user_data = {
        'email': 'john.doe@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'profession': 'Working Professional',
        'experience': 5,
        'skills': 'Python, Java, SQL, AWS, Docker',
        'preferred_domain_1': 'Software Development',
        'preferred_domain_2': 'Cloud Computing',
        'preferred_domain_3': 'DevOps'
    }
    
    # Example matching jobs
    matching_jobs = pd.DataFrame([
        {
            'job_id': 1,
            'job_title': 'Senior Software Engineer',
            'company': 'TechCorp',
            'domain': 'Software Development',
            'required_skills': 'Python, Java, SQL, AWS',
            'experience_required': 3,
            'job_type': 'Working Professional',
            'contact_email': 'hr@techcorp.com'
        }
    ])
    
    # Send data
    print("\nSending job matching data to n8n...")
    result = n8n.send_job_matching_data(
        user_data,
        matching_jobs,
        model_info={'model_name': 'Random Forest', 'accuracy': 0.92}
    )
    
    if result['success']:
        print("✓ Data sent successfully!")
        print(f"Response: {result.get('response', {})}")
    else:
        print(f"✗ Failed to send data: {result.get('error', 'Unknown error')}")