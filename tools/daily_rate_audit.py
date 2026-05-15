import os
import sys
import asyncio
import requests
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

async def sync_rates():
    print(f"[SYSTEM] Initiating Verified Rate Sync for {datetime.now().strftime('%Y-%m-%d')}...")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[ERROR] Supabase credentials missing. Verify GitHub Secrets or .env.local.")
        sys.exit(1)

    async with async_playwright() as p:
        try:
            print("[FETCH] Launching browser to scrape Freddie Mac market data...")
            browser = await p.chromium.launch(headless=True)
            # Use a more modern, common user agent to avoid bot detection
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            source_url = "https://www.freddiemac.com/pmms"
            print(f"[NAVIGATE] Connecting to {source_url}...")
            await page.goto(source_url, wait_until="networkidle", timeout=60000)
            
            # Wait for the rate element to appear
            print("[WAIT] Searching for rate elements...")
            await page.wait_for_selector("p.stat.weight-bold", timeout=20000)
            
            stats = await page.query_selector_all("p.stat.weight-bold")
            rate = None
            for stat in stats:
                text = await stat.inner_text()
                # We expect a number like 6.88
                clean_text = text.replace('%', '').strip()
                if "." in clean_text:
                    try:
                        rate = float(clean_text)
                        break
                    except:
                        continue
            
            if not rate:
                # Capture screenshot for debugging in CI artifacts if possible
                await page.screenshot(path="rate_sync_debug.png")
                raise Exception("Could not find a valid rate value in the expected elements.")

            print(f"[EXTRACT] Market Rate Found: {rate}%")
            
            endpoint = f"{SUPABASE_URL}/rest/v1/market_rates"
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            payload = {
                "rate_type": "30Y_FIXED",
                "rate": rate,
                "source_url": source_url,
                "last_verified": datetime.now().isoformat()
            }
            
            response = requests.post(endpoint, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                print("[SUCCESS] Market intelligence synced to Supabase instantly via REST.")
            else:
                print(f"[ERROR] Supabase REST API failed: {response.status_code} - {response.text}")
                sys.exit(1)
                
            await browser.close()
            
        except Exception as e:
            print(f"[CRITICAL] Rate Sync Failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(sync_rates())
