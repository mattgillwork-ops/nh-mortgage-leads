
import asyncio
import json
from mcp.server.fastmcp import FastMCP
from browser_skill import browser_skill
from web_search import web_search
from email_manager import send_email, read_inbox, get_message_content

# Initialize the Anti-Gravity MCP Server
mcp = FastMCP("Anti-Gravity Core Skills")

@mcp.tool()
async def browser_action(action: str, url: str, selector: str = None, text: str = None) -> str:
    """
    Performs an automated browser action (navigate, click, type, extract_seo, screenshot).
    
    Args:
        action: The action to perform ('navigate', 'click', 'type', 'extract_seo', 'screenshot').
        url: The target URL.
        selector: CSS selector for click/type actions.
        text: Text to type for the 'type' action.
    """
    command = {
        "action": action,
        "url": url,
        "selector": selector,
        "text": text
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

@mcp.tool()
def send_business_email(subject: str, body: str, to_email: str, to_name: str = "Recipient") -> str:
    """
    Sends a business outreach email via the Mailtrap pipeline.
    The email will go to the Sandbox for human review before final delivery.
    
    Args:
        subject: The subject line of the email.
        body: The content of the email.
        to_email: The recipient's email address.
        to_name: The name of the recipient.
    """
    result = send_email(subject, body, to_email, to_name)
    return json.dumps(result, indent=2)

@mcp.tool()
def read_business_inbox() -> str:
    """
    Retrieves the list of latest emails from the business inbox.
    Used by Rowan for security triaging and Atlas for intent analysis.
    """
    result = read_inbox()
    return json.dumps(result, indent=2)

@mcp.tool()
def get_email_details(message_id: str) -> str:
    """
    Retrieves full content and headers for a specific email.
    Essential for scam detection and forensic header analysis.
    
    Args:
        message_id: The unique ID of the message to inspect.
    """
    result = get_message_content(message_id)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")
