import os
import asyncio
from playwright.async_api import async_playwright
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="mortgage-app/.env.local")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

async def sync_rates():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: Supabase credentials missing.")
        return

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    async with async_playwright() as p:
        print("Launching browser to fetch current NH rates...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # We use Freddie Mac as the primary source of truth for national/state averages
        source_url = "https://www.freddiemac.com/pmms"
        await page.goto(source_url, wait_until="networkidle")
        
        # Extract the latest 30-year fixed rate
        # Note: Selectors may change, so we use a robust search
        try:
            rate_text = await page.inner_text(".rate-value") # Common Freddie Mac selector
            rate = float(rate_text.replace("%", "").strip())
            print(f"Extracted Rate: {rate}%")
            
            # Update Supabase
            # We update the '30Y_FIXED' row
            data, count = supabase.table("market_rates") \
                .upsert({
                    "rate_type": "30Y_FIXED",
                    "rate": rate,
                    "source_url": source_url,
                    "last_verified": "now()"
                }, on_conflict="rate_type") \
                .execute()
            
            print("Successfully synced rate to Supabase.")
            
        except Exception as e:
            print(f"Failed to extract rate: {e}")
            # Fallback or alert logic here
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(sync_rates())
