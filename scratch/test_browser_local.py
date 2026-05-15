import asyncio
from tools.browser_skill import browser_skill
import json

async def test():
    cmd = {
        "action": "navigate",
        "url": "https://www.freddiemac.com/pmms",
        "take_screenshot": True
    }
    result = await browser_skill(cmd)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test())
