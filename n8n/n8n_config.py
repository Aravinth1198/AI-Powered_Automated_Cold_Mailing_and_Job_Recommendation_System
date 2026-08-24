"""Configuration for n8n connection"""

# N8N Cloud Webhook URLs
# Replace these with your actual n8n cloud webhook URLs

N8N_CONFIG = {
    # Main webhook for job matching data
    'job_matching_webhook': 'https://aravinth1198.app.n8n.cloud/webhook/153b9105-702d-4485-95fd-5b1a1a904aa9',
    
    # Optional: Separate webhooks for different purposes
    'user_registration_webhook': 'https://your-instance.n8n.cloud/webhook/user-registration',
    'application_submission_webhook': 'https://your-instance.n8n.cloud/webhook/application-submission',
    'status_update_webhook': 'https://your-instance.n8n.cloud/webhook/status-update',
    
    # Connection settings
    'timeout': 60,  # seconds
    'retry_attempts': 3,
    'retry_delay': 2,  # seconds
}

# Or use a single webhook for everything
SINGLE_WEBHOOK_URL = 'https://aravinth1198.app.n8n.cloud/webhook/153b9105-702d-4485-95fd-5b1a1a904aa9'