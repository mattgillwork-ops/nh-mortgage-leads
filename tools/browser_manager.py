import os
import shutil
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSIONS_DIR = os.path.join(BASE_DIR, "tru", "Browser_Sessions")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BrowserManager")

def get_session_dir(session_id="default"):
    """Returns the path to the user data directory for a given session ID."""
    session_path = os.path.join(SESSIONS_DIR, session_id)
    os.makedirs(session_path, exist_ok=True)
    return session_path

def list_sessions():
    """Lists all available browser sessions."""
    if not os.path.exists(SESSIONS_DIR):
        return []
    return [d for d in os.listdir(SESSIONS_DIR) if os.path.isdir(os.path.join(SESSIONS_DIR, d))]

def clear_session(session_id):
    """Deletes the session data for a given ID."""
    session_path = os.path.join(SESSIONS_DIR, session_id)
    if os.path.exists(session_path):
        logger.info(f"Clearing browser session: {session_id}")
        shutil.rmtree(session_path)
        return True
    return False

def get_default_config():
    """Returns default Playwright context configuration."""
    return {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "viewport": {"width": 1280, "height": 800},
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
    }
