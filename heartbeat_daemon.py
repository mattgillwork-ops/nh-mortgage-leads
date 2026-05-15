"""
Anti-Gravity Heartbeat Daemon
==============================
Autonomous background process that runs system audits and infrastructure
maintenance cycles. Infrastructure health is always prioritized over
business tasks.

Runs every CHECK_INTERVAL seconds. Crash-resistant with file-based logging.
"""

import time
import subprocess
import logging
import os
import sys
import datetime
import yaml

# --- Logging Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "heartbeat.log")

def get_ollama_endpoint():
    if os.path.exists("/.dockerenv") or os.environ.get("DOCKER_CONTAINER"):
        return "http://host.docker.internal:11434"
    return "http://127.0.0.1:11434"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] HEARTBEAT: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Use the same Python interpreter that is running THIS script.
# This fixes the 'python' vs 'py' ambiguity on Windows.
PYTHON_EXE = sys.executable
ASK_SCRIPT = os.path.join(BASE_DIR, "ask.py")
SELFCHECK_SCRIPT = os.path.join(BASE_DIR, "selfcheck.py")


def preflight_check() -> bool:
    """
    Verify that Ollama is reachable before starting the pulse loop.
    Returns True if all systems are go, False otherwise.
    """
    logging.info("Running pre-flight checks...")
    try:
        import ollama
        client = ollama.Client(host=get_ollama_endpoint())
        
        # 1. Verify Ollama Reachability
        client.list()
        logging.info("[PRE-FLIGHT OK] Ollama is reachable.")
        
        # 2. Verify Critical Agent Models
        registry_path = os.path.join(BASE_DIR, "agent_registry.yaml")
        if os.path.exists(registry_path):
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry = yaml.safe_load(f)
            
            installed = [m.model for m in client.list().models]
            missing = []
            for agent_id, data in registry.get('agents', {}).items():
                primary = data.get('model', {}).get('primary')
                if primary and not any(primary in name for name in installed):
                    missing.append(primary)
            
            if missing:
                logging.warning(f"[PRE-FLIGHT WARNING] Missing models: {missing}")
                # We don't fail pre-flight here, but we log it for the Repair Orchestrator
        
        return True
    except Exception as e:
        logging.error(f"[PRE-FLIGHT FAIL] Core system check failed: {e}")
        logging.error("Heartbeat will retry in 60 seconds.")
        return False


def run_task(prompt: str) -> str:
    """
    Triggers Alex (CEO) to run an autonomous task via ask.py.
    Uses sys.executable to ensure the correct Python interpreter is used.
    """
    try:
        logging.info(f"Triggering Task: {prompt[:80]}...")
        result = subprocess.run(
            [PYTHON_EXE, ASK_SCRIPT, prompt],
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=300  # 5-minute timeout per task to prevent hangs
        )
        if result.returncode != 0:
            logging.warning(f"Task exited with code {result.returncode}. stderr: {result.stderr[:200]}")
        return result.stdout
    except subprocess.TimeoutExpired:
        logging.error(f"Task timed out after 5 minutes: {prompt[:80]}")
        return "[TIMEOUT]"
    except Exception as e:
        logging.error(f"Failed to trigger heartbeat task: {e}")
        return str(e)


def run_pulse_cycle():
    """
    Executes one full heartbeat cycle.
    Priority: Infrastructure Health > Knowledge Maintenance > Goal Review.
    Business tasks are NOT in this loop — that is for Phase 2 (later).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"=== Pulse Check at {timestamp} ===")

    # --- Task 1: Infrastructure Health Check ---
    # Run selfcheck.py in quick mode to verify all systems are operational.
    # We use a direct subprocess call here to get the return code.
    health_check = subprocess.run(
        [PYTHON_EXE, SELFCHECK_SCRIPT, "--quick"],
        capture_output=True,
        text=True,
        cwd=BASE_DIR
    )
    if health_check.returncode != 0:
        logging.critical("INFRASTRUCTURE COLLAPSE DETECTED! Heartbeat stopping to prevent data corruption.")
        logging.critical(health_check.stdout)
        sys.exit(1)
    
    logging.info("[HEALTH OK] System foundation verified.")

    # --- Task 2: Autonomous Repair ---
    # Scan logs for failures and attempt remediation.
    logging.info("Initiating Autonomous Repair Cycle...")
    subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "tools/repair_orchestrator.py")], cwd=BASE_DIR)

    # --- Task 3: Knowledge Pruning ---

    # --- Task 4: Autonomous Rate Engine Audit ---
    # Refresh NH mortgage rates and auto-deploy if they've changed.
    logging.info("Initiating Autonomous Rate Audit...")
    subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "tools/daily_rate_audit.py")], cwd=BASE_DIR)

    logging.info("=== Pulse cycle complete. ===")


def main():
    logging.info("Anti-Gravity Heartbeat Daemon Starting...")

    # Audit frequency: every 5 minutes (300s) for Zero-Drift compliance.
    CHECK_INTERVAL = 300

    # Pre-flight: Wait until Ollama is available before starting loop
    while not preflight_check():
        time.sleep(60)

    logging.info(f"Pre-flight passed. Pulse loop starting (interval: {CHECK_INTERVAL}s).")

    while True:
        try:
            run_pulse_cycle()
        except Exception as e:
            # Daemon-level crash guard: log the error but keep running.
            logging.critical(f"DAEMON CRASH CAUGHT — Recovering: {e}", exc_info=True)

        logging.info(f"Sleeping for {CHECK_INTERVAL}s...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
