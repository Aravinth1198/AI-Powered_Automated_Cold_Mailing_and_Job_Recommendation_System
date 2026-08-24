"""Helper functions for n8n integration"""

from n8n_connection import N8NConnection
from n8n_config import N8N_CONFIG, SINGLE_WEBHOOK_URL
import pandas as pd
from typing import Dict, Optional

def get_n8n_connection(webhook_type: str = 'main') -> N8NConnection:
    """
    Get N8N connection instance
    
    Args:
        webhook_type: Type of webhook to connect to
        
    Returns:
        N8NConnection instance
    """
    if webhook_type == 'main':
        url = SINGLE_WEBHOOK_URL
    else:
        url = N8N_CONFIG.get(f'{webhook_type}_webhook', SINGLE_WEBHOOK_URL)
    
    return N8NConnection(url)

def send_to_n8n(
    user_data: Dict,
    matching_jobs: pd.DataFrame,
    model_info: Optional[Dict] = None,
    webhook_type: str = 'main'
) -> Dict:
    """
    Quick function to send data to n8n
    
    Args:
        user_data: User information dictionary
        matching_jobs: DataFrame of matching jobs
        model_info: ML model information
        webhook_type: Type of webhook to use
        
    Returns:
        Response from n8n
    """
    n8n = get_n8n_connection(webhook_type)
    return n8n.send_job_matching_data(user_data, matching_jobs, model_info)

# Example usage in your main application
def example_integration():
    """Example of how to integrate in your main app"""
    
    # Your user data from the UI
    user_data = {
        'email': 'user@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'profession': 'Student',
        'experience': 0,
        'skills': 'Python, Machine Learning, SQL',
        'preferred_domain_1': 'Data Science',
        'preferred_domain_2': 'Machine Learning',
        'preferred_domain_3': 'Software Development'
    }
    
    # Your matching jobs from ML model
    matching_jobs = pd.DataFrame([
        {
            'job_id': 1,
            'job_title': 'Data Scientist',
            'company': 'DataCorp',
            'domain': 'Data Science',
            'required_skills': 'Python, Machine Learning, SQL',
            'contact_email': 'hr@datacorp.com'
        }
    ])
    
    # Model information
    model_info = {
        'model_name': 'Random Forest',
        'accuracy': 0.92,
        'f1_score': 0.89
    }
    
    # Send to n8n
    result = send_to_n8n(user_data, matching_jobs, model_info)
    
    if result['success']:
        print("Data sent to n8n successfully!")
        # Continue with your application logic
    else:
        print(f"Failed to send data: {result.get('error')}")

if __name__ == "__main__":
    example_integration()