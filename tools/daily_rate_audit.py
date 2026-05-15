import os
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
        print("[ERROR] Supabase credentials missing. Verify .env.local.")
        return

    async with async_playwright() as p:
        try:
            print("[FETCH] Launching browser to scrape Freddie Mac market data...")
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page = await context.new_page()
            
            source_url = "https://www.freddiemac.com/pmms"
            print(f"[NAVIGATE] Connecting to {source_url}...")
            await page.goto(source_url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for the rate element to appear (using the verified selector)
            print("[WAIT] Searching for rate elements...")
            await page.wait_for_selector("p.stat.weight-bold", timeout=15000)
            
            # Extract all stats and find the one that looks like a rate (e.g. 6.xx)
            stats = await page.query_selector_all("p.stat.weight-bold")
            rate = None
            for stat in stats:
                text = await stat.inner_text()
                if "." in text and len(text.strip()) <= 5: # Typical rate format 6.36
                    try:
                        rate = float(text.strip())
                        break
                    except:
                        continue
            
            if not rate:
                raise Exception("Could not find a valid rate value in the expected elements.")

            print(f"[EXTRACT] Market Rate Found: {rate}%")
            
            # REST API Upsert (PostgREST style)
            # We use an RPC or a POST with Upsert header
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
                
            await browser.close()
            
        except Exception as e:
            print(f"[CRITICAL] Rate Sync Failed: {e}")

if __name__ == "__main__":
    asyncio.run(sync_rates())
