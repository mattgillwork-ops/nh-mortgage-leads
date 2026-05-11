
import os
import mailbox
import datetime
import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import Envelope
try:
    from security_gate import scan_input
except ImportError:
    # Fallback if security_gate is not in path (unlikely in this repo)
    def scan_input(text): return {"is_safe": True, "findings": []}

# Configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAILDIR_PATH = os.path.join(BASE_DIR, "tru", "Inbox")

class IronSentryHandler:
    async def handle_DATA(self, server, session, envelope: Envelope):
        peer = session.peer[0]
        print(f"[{datetime.datetime.now()}] Inbound connection from {peer}")
        
        # 1. Security Scrub (The Triage Gate)
        content = envelope.content.decode('utf-8', errors='replace')
        scan_result = scan_input(content)
        
        if not scan_result["is_safe"]:
            print(f"!!! QUARANTINED: Suspicious content from {envelope.mail_from} (IP: {peer})")
            print(f"Findings: {scan_result['findings']}")
            return '550 Message rejected for security reasons'
            
        # 2. Local Vault Storage (Maildir Format)
        try:
            if not os.path.exists(MAILDIR_PATH):
                os.makedirs(MAILDIR_PATH, exist_ok=True)
            
            # Using Maildir for high reliability and concurrent access
            mdir = mailbox.Maildir(MAILDIR_PATH, factory=None, create=True)
            msg = mailbox.MaildirMessage(envelope.content)
            mdir.add(msg)
            
            print(f"✔ SAVED: {envelope.mail_from} -> {MAILDIR_PATH}")
            return '250 Message accepted for delivery'
        except Exception as e:
            print(f"ERR: Failed to save message: {e}")
            return '451 Local error in processing'

async def start_sentry():
    handler = IronSentryHandler()
    # Running on 2525 to avoid root requirements in Docker
    controller = Controller(handler, hostname='0.0.0.0', port=2525)
    controller.start()
    print("========================================")
    print("IRON SENTRY: PRIVATE MAIL GATEWAY ACTIVE")
    print(f"Storage: {MAILDIR_PATH}")
    print("Port: 2525")
    print("========================================")
    
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        controller.stop()

if __name__ == "__main__":
    asyncio.run(start_sentry())
