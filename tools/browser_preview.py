import asyncio
from playwright.async_api import async_playwright

async def capture_screenshot_and_summary(url):
    # Initialize Playwright
    async with async_playwright() as p:
        # Launch a browser
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to the URL
            await page.goto(url)

            # Capture screenshot
            screenshot_path = "screenshot.png"
            await page.screenshot(path=screenshot_path)

            # Get page title and visible text
            page_title = await page.title()
            visible_text = await page.text_content('body')

            # Truncate visible text to 5000 characters
            if len(visible_text) > 5000:
                visible_text = visible_text[:5000] + " [Truncated]"

            # Return summary
            summary = {
                "url": url,
                "title": page_title,
                "visible_text": visible_text,
                "screenshot_path": screenshot_path
            }

            return summary

        except Exception as e:
            return {"error": str(e)}

        finally:
            # Close browser
            await browser.close()

# Example usage
if __name__ == "__main__":
    url = "http://localhost:3000"
    result = asyncio.run(capture_screenshot_and_summary(url))
    print(result)
