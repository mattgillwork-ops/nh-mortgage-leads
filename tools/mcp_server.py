
import asyncio
import json
from mcp.server.fastmcp import FastMCP
from browser_skill import browser_skill
from web_search import web_search
# Initialize the Anti-Gravity MCP Server
mcp = FastMCP("Anti-Gravity Core Skills")

@mcp.tool()
async def browser_action(action: str, url: str = None, selector: str = None, text: str = None, session_id: str = "default", headless: bool = True, wait_time: int = 2000) -> str:
    """
    Performs an automated browser action using Playwright with persistent session support.
    
    Args:
        action: The action to perform ('navigate', 'click', 'type', 'extract_seo', 'screenshot', 'scroll', 'hover', 'wait').
        url: The target URL (required for 'navigate').
        selector: CSS selector for click/type/hover/wait actions.
        text: Text to type for the 'type' action.
        session_id: Unique ID to persist cookies/sessions (default: 'default').
        headless: Whether to run in headless mode (default: True).
        wait_time: Milliseconds to wait after action (default: 2000).
    """
    command = {
        "action": action,
        "url": url,
        "selector": selector,
        "text": text,
        "session_id": session_id,
        "headless": headless,
        "wait_time": wait_time
    }
    result = await browser_skill(command)
    return json.dumps(result, indent=2)

@mcp.tool()
def search_the_web(query: str, max_results: int = 3) -> str:
    """
    Performs a live web search using DuckDuckGo/Google.
    
    Args:
        query: The search terms.
        max_results: Number of results to fetch (default 3).
    """
    return web_search(query, max_results=max_results)

if __name__ == "__main__":
    mcp.run(transport="stdio")

