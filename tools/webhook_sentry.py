
from fastapi import FastAPI, Request, HTTPException
import os
import mailbox
import email.utils
from email.mime.text import MIMEText
import datetime
try:
    from security_gate import scan_input
except ImportError:
    def scan_input(text): return {"is_safe": True, "findings": []}

app = FastAPI(title="Iron Sentry Webhook Gateway")

# Configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAILDIR_PATH = os.path.join(BASE_DIR, "tru", "Inbox")

@app.post("/inbound")
async def handle_inbound(request: Request):
    try:
        data = await request.json()
        print(f"[{datetime.datetime.now()}] Webhook received from Cloudflare")
        
        # 1. Security Scrub (The Triage Gate)
        content = data.get("text", "")
        subject = data.get("subject", "No Subject")
        sender = data.get("from", "Unknown")
        
        scan_result = scan_input(f"Subject: {subject}\n\n{content}")
        
        if not scan_result["is_safe"]:
            print(f"!!! QUARANTINED: Suspicious webhook payload from {sender}")
            return {"status": "quarantined", "findings": scan_result["findings"]}
            
        # 2. Local Vault Storage (Maildir Construction)
        if not os.path.exists(MAILDIR_PATH):
            os.makedirs(MAILDIR_PATH, exist_ok=True)
            
        # Construct a standard RFC822 email message from the JSON payload
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = data.get("to", "alex@trucolors.team")
        msg['Date'] = email.utils.formatdate(localtime=True)
        msg['X-Iron-Sentry-Verified'] = 'True'
        
        mdir = mailbox.Maildir(MAILDIR_PATH, factory=None, create=True)
        mdir.add(msg.as_bytes())
        
        print(f"✔ SAVED: {sender} -> {MAILDIR_PATH}")
        return {"status": "success", "vault_id": datetime.datetime.now().isoformat()}

    except Exception as e:
        print(f"ERR: Webhook processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2525)
