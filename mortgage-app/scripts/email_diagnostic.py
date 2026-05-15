import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env.local")

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def run_diagnostic():
    print(f"--- EMAIL DIAGNOSTIC (Direct REST) ---")
    print(f"Target Email: {ADMIN_EMAIL}")
    
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": "NH Mortgage Journal <onboarding@resend.dev>",
        "to": [ADMIN_EMAIL],
        "subject": "⚠️ SYSTEM DIAGNOSTIC: Priority Delivery Test",
        "html": "<h1>Diagnostic Success</h1><p>If you see this, the Resend relay is functional via REST API.</p>"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    run_diagnostic()
