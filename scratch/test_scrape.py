import asyncio
from playwright.async_api import async_playwright

async def test_scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to Freddie Mac...")
        await page.goto("https://www.freddiemac.com/pmms", wait_until="domcontentloaded")
        print("Wait for stats...")
        await page.wait_for_selector("p.stat.weight-bold", timeout=10000)
        stats = await page.query_selector_all("p.stat.weight-bold")
        for stat in stats:
            print(f"Stat found: {await stat.inner_text()}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_scrape())
