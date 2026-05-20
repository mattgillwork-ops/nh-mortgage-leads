import os
import sys
import asyncio
import requests
from playwright.async_api import async_playwright
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from datetime import datetime

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
            await page.goto(source_url, wait_until="domcontentloaded", timeout=90000)
            
            # Strategy 1: Verified Selector
            print("[WAIT] Searching for rate elements...")
            rate = None
            try:
                await page.wait_for_selector("p.stat.weight-bold", timeout=15000)
                stats = await page.query_selector_all("p.stat.weight-bold")
                for stat in stats:
                    text = await stat.inner_text()
                    clean_text = text.replace('%', '').strip()
                    if "." in clean_text:
                        try:
                            rate = float(clean_text)
                            print(f"[EXTRACT] Found via selector: {rate}%")
                            break
                        except: continue
            except:
                print("[WARN] Primary selector failed. Attempting Regex Fallback...")

            # Strategy 2: Regex Fallback (Text-based search)
            if not rate:
                body_text = await page.evaluate("() => document.body.innerText")
                import re
                # Look for "30-year Fixed-Rate Mortgage" followed by a percentage
                match = re.search(r"30-year Fixed-Rate Mortgage\s*([\d\.]+)%", body_text, re.IGNORECASE)
                if match:
                    rate = float(match.group(1))
                    print(f"[EXTRACT] Found via regex: {rate}%")
            
            if not rate:
                # Capture diagnostic data
                print("[DIAGNOSTIC] Capturing state for debugging...")
                await page.screenshot(path="sync_failure.png")
                with open("sync_failure.html", "w", encoding="utf-8") as f:
                    html_content = await page.evaluate("() => document.documentElement.outerHTML")
                    f.write(html_content)
                raise Exception("Critical: Could not extract mortgage rate from Freddie Mac site.")

            print(f"[VERIFIED] Market Rate: {rate}%")
            
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
            
            print(f"[PUSH] Syncing to Supabase: {endpoint}")
            response = requests.post(endpoint, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                print("[SUCCESS] Market intelligence synced successfully.")
            else:
                print(f"[ERROR] Supabase API Error {response.status_code}: {response.text}")
                sys.exit(1)
                
            await browser.close()
            
        except Exception as e:
            print(f"[CRITICAL] Rate Sync Failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(sync_rates())
