import asyncio
import json
import sys
import os
from playwright.async_api import async_playwright

async def browser_skill(command):
    """
    Executes a browser-based action using Playwright.
    Input: JSON command string or dict.
    Actions: navigate, click, type, extract_seo, screenshot, get_text
    """
    if isinstance(command, str):
        try:
            cmd = json.loads(command)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON command"}
    else:
        cmd = command

    action = cmd.get("action")
    url = cmd.get("url")
    selector = cmd.get("selector")
    text = cmd.get("text")
    wait_time = cmd.get("wait_time", 2000)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()

        try:
            if action == "navigate" or url:
                await page.goto(url, wait_until="networkidle")
            
            if action == "click" and selector:
                await page.click(selector)
                await page.wait_for_timeout(wait_time)
            
            if action == "type" and selector and text:
                await page.fill(selector, text)
                await page.wait_for_timeout(wait_time)

            result = {"status": "success", "url": page.url}

            if action == "extract_seo":
                seo_data = {
                    "title": await page.title(),
                    "meta_description": await page.locator('meta[name="description"]').get_attribute("content") or "None",
                    "h1": await page.locator('h1').all_text_contents(),
                    "h2": await page.locator('h2').all_text_contents(),
                    "links_count": await page.locator('a').count(),
                    "images_without_alt": await page.locator('img:not([alt])').count()
                }
                result["seo_data"] = seo_data

            if action == "screenshot":
                screenshot_dir = os.path.join("tru", "Visual_Logs")
                os.makedirs(screenshot_dir, exist_ok=True)
                path = os.path.join(screenshot_dir, f"browser_{int(asyncio.get_event_loop().time())}.png")
                await page.screenshot(path=path)
                result["screenshot_path"] = path

            # Always return a summary of the page text (truncated)
            visible_text = await page.text_content('body')
            if visible_text:
                result["content_summary"] = visible_text[:3000].strip() + ("..." if len(visible_text) > 3000 else "")

            return result

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            await browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided. Usage: py browser_skill.py '{\"action\": \"navigate\", \"url\": \"...\"}'"}))
        sys.exit(1)
    
    command_input = sys.argv[1]
    output = asyncio.run(browser_skill(command_input))
    print(json.dumps(output, indent=2))
