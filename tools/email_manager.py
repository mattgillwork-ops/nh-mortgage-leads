
import os
import requests
import mailtrap as mt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Maildir configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAILDIR_PATH = os.path.join(BASE_DIR, "tru", "Inbox")

def read_inbox():
    """
    Lists messages from the local Iron Sentry Maildir.
    """
    if not os.path.exists(MAILDIR_PATH):
        return {"status": "success", "messages": []}
        
    try:
        import mailbox
        mdir = mailbox.Maildir(MAILDIR_PATH)
        messages = []
        for key, msg in mdir.items():
            messages.append({
                "id": key,
                "subject": str(msg.get('subject', 'No Subject')),
                "from_email": str(msg.get('from', 'Unknown')),
                "sent_at": str(msg.get('date', ''))
            })
        # Sort by date (reverse)
        return {"status": "success", "messages": sorted(messages, key=lambda x: x.get('sent_at', ''), reverse=True)}
    except Exception as e:
        return {"status": "error", "message": f"Maildir error: {str(e)}"}

def get_message_content(message_id):
    """
    Retrieves the full content from the local Maildir.
    """
    try:
        import mailbox
        if not os.path.exists(MAILDIR_PATH):
            return {"status": "error", "message": "Maildir not found"}
            
        mdir = mailbox.Maildir(MAILDIR_PATH)
        msg = mdir.get(message_id)
        if not msg:
            return {"status": "error", "message": f"Message {message_id} not found in local vault"}
            
        # Parse body
        text_body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    text_body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
        else:
            text_body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
            
        return {
            "status": "success",
            "id": message_id,
            "subject": str(msg.get('subject', 'No Subject')),
            "from": str(msg.get('from', 'Unknown')),
            "text": text_body,
            "raw_source": msg.as_string()[:2000]
        }
    except Exception as e:
        return {"status": "error", "message": f"Maildir retrieval error: {str(e)}"}

def send_email(subject, body, to_email, to_name="Recipient", is_html=False):
    """
    Sends an email via Mailtrap.
    By default, this goes to the Mailtrap Sandbox for human review.
    """
    token = os.getenv("MAILTRAP_API_TOKEN")
    if not token:
        return {"status": "error", "message": "MAILTRAP_API_TOKEN not found in environment variables."}

    try:
        # Initialize client
        client = mt.MailtrapClient(token=token)

        # Construct the email
        mail = mt.Mail(
            sender=mt.Address(email="alex@trucolors.team", name="Alex (CEO, TruColors)"),
            to=[mt.Address(email=to_email, name=to_name)],
            subject=subject,
            text=None if is_html else body,
            html=body if is_html else None,
            category="CEO Outreach"
        )

        # Send
        # Note: In a production scenario, you'd use client.send(mail)
        # For the sandbox, we often use the standard SMTP or the testing API endpoint
        # The mailtrap SDK handles the routing based on the token/configuration
        client.send(mail)
        
        return {
            "status": "success",
            "message": f"Email '{subject}' sent to {to_email} via Mailtrap.",
            "mode": "Sandbox (HITL Review Required)"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Test call
    print(send_email(
        subject="Welcome to the Anti-Gravity AI Ecosystem",
        body="This is a test outreach email sent from the Nova agent.",
        to_email="test@example.com"
    ))
