import asyncio
from playwright.async_api import async_playwright
import json

async def debug_structure():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.freddiemac.com/pmms", wait_until="networkidle")
        
        # Search for the element containing 6.36%
        elements = await page.query_selector_all("p")
        for el in elements:
            text = await el.inner_text()
            if "6.36" in text:
                classes = await el.get_attribute("class")
                tag = await el.evaluate("el => el.tagName")
                print(f"Found match: <{tag} class='{classes}'>{text}</{tag}>")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_structure())
