import asyncio
import json
import sys
import os
import time
from playwright.async_api import async_playwright
import browser_manager

async def browser_skill(command):
    """
    Executes a browser-based action using Playwright with persistent sessions.
    Input: JSON command string or dict.
    Actions: navigate, click, type, extract_seo, screenshot, get_text, scroll, hover, wait
    """
    if isinstance(command, str):
        try:
            cmd = json.loads(command)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON command"}
    else:
        cmd = command

    action = cmd.get("action", "navigate")
    url = cmd.get("url")
    selector = cmd.get("selector")
    text = cmd.get("text")
    wait_time = cmd.get("wait_time", 2000)
    session_id = cmd.get("session_id", "default")
    headless = cmd.get("headless", True)

    session_dir = browser_manager.get_session_dir(session_id)
    config = browser_manager.get_default_config()

    async with async_playwright() as p:
        # Using launch_persistent_context to keep cookies, localStorage, etc.
        context = await p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=headless,
            user_agent=config["user_agent"],
            viewport=config["viewport"]
        )
        
        # In persistent context, the first page is already created
        page = context.pages[0] if context.pages else await context.new_page()

        try:
            # Set default timeout
            page.set_default_timeout(30000)

            if url:
                print(f"[BROWSER] Navigating to {url}...")
                await page.goto(url, wait_until="domcontentloaded")
                # Wait a bit for JS-heavy sites
                await page.wait_for_timeout(1000)
            
            if action == "click" and selector:
                print(f"[BROWSER] Clicking {selector}...")
                await page.click(selector)
                await page.wait_for_timeout(wait_time)
            
            elif action == "type" and selector and text:
                print(f"[BROWSER] Typing into {selector}...")
                await page.fill(selector, text)
                await page.wait_for_timeout(wait_time)

            elif action == "scroll":
                direction = cmd.get("direction", "down")
                amount = cmd.get("amount", 500)
                print(f"[BROWSER] Scrolling {direction} by {amount}px...")
                if direction == "down":
                    await page.evaluate(f"window.scrollBy(0, {amount})")
                else:
                    await page.evaluate(f"window.scrollBy(0, -{amount})")
                await page.wait_for_timeout(wait_time)

            elif action == "hover" and selector:
                print(f"[BROWSER] Hovering over {selector}...")
                await page.hover(selector)
                await page.wait_for_timeout(wait_time)

            elif action == "wait" and selector:
                print(f"[BROWSER] Waiting for {selector}...")
                await page.wait_for_selector(selector, state="visible")

            # Default result data
            result = {
                "status": "success", 
                "url": page.url,
                "title": await page.title()
            }

            if action == "extract_seo":
                print("[BROWSER] Extracting SEO data...")
                
                async def get_attr_safe(selector, attr):
                    try:
                        loc = page.locator(selector)
                        if await loc.count() > 0:
                            return await loc.first.get_attribute(attr) or "None"
                    except:
                        pass
                    return "None"

                seo_data = {
                    "title": await page.title(),
                    "meta_description": await get_attr_safe('meta[name="description"]', "content"),
                    "canonical": await get_attr_safe('link[rel="canonical"]', "href"),
                    "robots": await get_attr_safe('meta[name="robots"]', "content"),
                    "h1": await page.locator('h1').all_text_contents(),
                    "h2": (await page.locator('h2').all_text_contents())[:10], 
                    "og_title": await get_attr_safe('meta[property="og:title"]', "content"),
                    "og_description": await get_attr_safe('meta[property="og:description"]', "content"),
                    "links_count": await page.locator('a').count(),
                    "images_count": await page.locator('img').count(),
                    "images_without_alt": await page.locator('img:not([alt])').count()
                }
                
                # Basic Performance Metric (LCP estimate)
                try:
                    performance_timing = await page.evaluate("() => JSON.stringify(window.performance.timing)")
                    timing = json.loads(performance_timing)
                    result["performance"] = {
                        "dom_interactive": timing["domInteractive"] - timing["navigationStart"],
                        "dom_complete": timing["domComplete"] - timing["navigationStart"],
                        "load_event": timing["loadEventEnd"] - timing["navigationStart"]
                    }
                except:
                    result["performance"] = "Unavailable"

                result["seo_data"] = seo_data

            if action == "screenshot" or cmd.get("take_screenshot"):
                screenshot_dir = os.path.join(browser_manager.BASE_DIR, "tru", "Visual_Logs")
                os.makedirs(screenshot_dir, exist_ok=True)
                timestamp = int(time.time())
                path = os.path.join(screenshot_dir, f"browser_{session_id}_{timestamp}.png")
                await page.screenshot(path=path)
                result["screenshot_path"] = path

            # Extract content summary
            try:
                # Try to get meaningful text
                visible_text = await page.evaluate("() => document.body.innerText")
                if visible_text:
                    result["content_summary"] = visible_text[:5000].strip() + ("..." if len(visible_text) > 5000 else "")
            except:
                result["content_summary"] = "Could not extract text summary."

            return result

        except Exception as e:
            print(f"[BROWSER ERROR] {str(e)}")
            return {"status": "error", "message": str(e)}
        finally:
            # We must close the context to release the lock on user_data_dir
            await context.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided. Usage: py browser_skill.py '{\"action\": \"navigate\", \"url\": \"...\"}'"}))
        sys.exit(1)
    
    command_input = sys.argv[1]
    output = asyncio.run(browser_skill(command_input))
    print(json.dumps(output, indent=2))
