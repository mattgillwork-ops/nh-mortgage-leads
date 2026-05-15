import os
import json
from datetime import datetime
import subprocess

RATES_FILE = "mortgage-app/src/data/rates.json"

def run_daily_audit():
    print(f"[SYSTEM] Initiating Daily Rate Audit for {datetime.now().strftime('%Y-%m-%d')}...")
    
    # Task Rowan to find the latest data
    prompt = "Identify the current 30-year fixed mortgage rate for NH (New Hampshire) as of today. Return ONLY a JSON object like: {\"rate\": 5.XX, \"lender\": \"Name\", \"date\": \"YYYY-MM-DD\"}"
    
    try:
        # Use ask.py to trigger Rowan
        result = subprocess.run(
            ["python", "ask.py", "--researcher", prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Extract JSON from Rowan's output (basic implementation)
        # In a production version, we'd use a more robust parser
        raw_output = result.stdout
        if "{" in raw_output and "}" in raw_output:
            json_str = raw_output[raw_output.find("{"):raw_output.rfind("}")+1]
            rate_data = json.loads(json_str)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(RATES_FILE), exist_ok=True)
            
            with open(RATES_FILE, 'w') as f:
                json.dump(rate_data, f, indent=2)
            
            print(f"[SUCCESS] Rate Engine updated: {rate_data['rate']}% via {rate_data['lender']}")
            
            # --- Autonomous Deployment ---
            # Check if there are changes to the rates file
            status = subprocess.run(["git", "status", "--porcelain", RATES_FILE], capture_output=True, text=True, cwd="mortgage-app")
            if status.stdout.strip():
                print("[SYSTEM] Rates changed. Initiating autonomous redeploy...")
                # Commit and push from the main repo (since mortgage-app is part of it)
                subprocess.run(["git", "add", RATES_FILE], cwd=".")
                subprocess.run(["git", "commit", "-m", f"AUTONOMOUS: Daily Rate Update ({rate_data['date']})"], cwd=".")
                # Push to the main repo if linked, or the standalone if that's where the user is looking
                # For this setup, we'll push to the mortgage-app standalone repo if it exists
                subprocess.run(["git", "push"], cwd=".")
                print("[SUCCESS] Autonomous redeploy triggered.")
            else:
                print("[INFO] No rate change detected. Skipping redeploy.")
            
    except Exception as e:
        print(f"[CRITICAL] Rate Audit Failed: {e}")

if __name__ == "__main__":
    run_daily_audit()
