"""
Anti-Gravity Web Search Tool
==============================
Provides live web search capabilities for the Researcher and other agents.

Primary engine: DuckDuckGo (no API key, no rate limits, privacy-respecting).
Fallback engine: Google (scraping, less reliable).

Returns structured results with URL, title, and clean text snippet.
Respects robots.txt before scraping page content.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib.robotparser
import logging

logger = logging.getLogger("WebSearch")

DDG_URL = "https://html.duckduckgo.com/html/"
GOOGLE_URL = "https://www.google.com/search"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def _can_fetch(url: str) -> bool:
    """
    Check robots.txt before scraping a URL.
    Returns True if scraping is allowed, False if blocked.
    Defaults to True on any error to avoid blocking legitimate searches.
    """
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", url)
    except Exception:
        return True  # Default permissive on error


def _fetch_page_text(url: str, max_chars: int = 6000) -> str:
    """Fetch and extract clean text from a single URL."""
    if not _can_fetch(url):
        return f"[Blocked by robots.txt: {url}]"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        text = soup.get_text(separator='\n', strip=True)
        if len(text) > max_chars:
            text = text[:max_chars] + "\n...[Truncated]"
        return text
    except Exception as e:
        return f"[Error fetching page: {e}]"


def _search_duckduckgo(query: str, max_results: int = 3) -> list[dict]:
    """Search using DuckDuckGo HTML interface. Returns list of {url, title} dicts."""
    try:
        resp = requests.post(DDG_URL, data={"q": query}, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        results = []
        for result in soup.select('.result__a'):
            href = result.get('href', '')
            title = result.get_text(strip=True)
            if href.startswith('http') and 'duckduckgo.com' not in href:
                results.append({"url": href, "title": title})
                if len(results) >= max_results:
                    break

        logger.info(f"DuckDuckGo returned {len(results)} results for: {query}")
        return results
    except Exception as e:
        logger.warning(f"DuckDuckGo search failed: {e}")
        return []


def _search_google_fallback(query: str, max_results: int = 3) -> list[dict]:
    """Fallback: scrape Google search results."""
    try:
        from urllib.parse import parse_qs
        resp = requests.get(GOOGLE_URL, params={"q": query}, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        results = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/url?'):
                parsed = parse_qs(urlparse(href).query)
                actual_url = parsed.get('q', [None])[0]
                if actual_url and actual_url.startswith('http') and 'google.com' not in actual_url:
                    results.append({"url": actual_url, "title": a_tag.get_text(strip=True)})
                    if len(results) >= max_results:
                        break

        logger.info(f"Google fallback returned {len(results)} results for: {query}")
        return results
    except Exception as e:
        logger.error(f"Google fallback also failed: {e}")
        return []


def web_search(query: str, max_results: int = 3, max_chars: int = 6000) -> str:
    """
    Main search function. Uses DuckDuckGo first, falls back to Google.

    Args:
        query: The search query string.
        max_results: Number of top results to fetch content from.
        max_chars: Maximum characters to return per result.

    Returns:
        A structured string with [URL], [Title], and extracted page text.
    """
    # Try DuckDuckGo first
    results = _search_duckduckgo(query, max_results)

    # Fall back to Google if DDG returned nothing
    if not results:
        logger.warning("DuckDuckGo returned no results. Trying Google fallback...")
        results = _search_google_fallback(query, max_results)

    if not results:
        return "[Search Error] No results found from any search engine."

    output_parts = []
    for i, result in enumerate(results):
        url = result["url"]
        title = result.get("title", "Unknown Title")
        text = _fetch_page_text(url, max_chars)
        output_parts.append(
            f"--- Result {i+1} ---\n"
            f"[URL]: {url}\n"
            f"[Title]: {title}\n"
            f"[Content]:\n{text}\n"
        )

    return "\n".join(output_parts)


if __name__ == "__main__":
    print(web_search("autonomous AI agent infrastructure hardening"))
