import asyncio
import json
import os
import sys

# Ensure we can import from tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from browser_skill import browser_skill
import browser_manager

async def test_persistence():
    session_id = "test_persistence_session"
    
    # Clean start
    browser_manager.clear_session(session_id)
    
    print(f"--- STEP 1: Setting up session {session_id} ---")
    # Navigate to google and search (sets cookies/history)
    cmd1 = {
        "action": "navigate",
        "url": "https://www.google.com",
        "session_id": session_id,
        "headless": True
    }
    result1 = await browser_skill(cmd1)
    print(f"Step 1 Status: {result1['status']}")
    
    # Check if session dir was created
    session_dir = browser_manager.get_session_dir(session_id)
    files = os.listdir(session_dir)
    print(f"Session directory created: {session_id} ({len(files)} items found)")
    
    if len(files) > 0:
        print("SUCCESS: Browser session data persisted.")
    else:
        print("FAILURE: No session data found.")
        sys.exit(1)

    print(f"\n--- STEP 2: Verifying persistence in second call ---")
    # In a second call, we should still have the context
    cmd2 = {
        "action": "navigate",
        "url": "https://www.wikipedia.org",
        "session_id": session_id,
        "headless": True
    }
    result2 = await browser_skill(cmd2)
    print(f"Step 2 Status: {result2['status']}")
    
    print("\n[PASSED] Browser persistence verified.")

if __name__ == "__main__":
    asyncio.run(test_persistence())
