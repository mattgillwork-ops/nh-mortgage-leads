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

# --- Logging Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "heartbeat.log")

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
        ollama.list()
        logging.info("[PRE-FLIGHT OK] Ollama is reachable.")
        return True
    except Exception as e:
        logging.error(f"[PRE-FLIGHT FAIL] Ollama is not reachable: {e}")
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
    # If issues are found, Alex will attempt self-repair.
    run_task(
        "Run a quick system health check using selfcheck.py --quick. "
        "If any agent models are missing, re-create them using their Modelfile. "
        "If any required directories are missing, create them. "
        "Write a one-paragraph summary of the system status to system_audit.md."
    )

    # --- Task 2: Knowledge Pruning ---
    # Keep Learnings.md relevant and concise.
    run_task(
        "Run knowledge_manager.py in dry-run mode first. "
        "Review the output. If the pruning looks correct and safe, run it for real. "
        "If any entries would be incorrectly deleted, skip pruning and log a warning."
    )

    # --- Task 3: Infrastructure Goal Review ---
    # Review the hardening task list and identify what to work on next.
    # NOTE: This is strictly infrastructure review, not business planning.
    run_task(
        "Review CURRENT_TASKS.md. Identify the next incomplete infrastructure "
        "hardening task. If a task is clearly actionable (e.g. a code fix), "
        "complete it autonomously. Log the result to PHASE_REVIEW.md."
    )

    logging.info("=== Pulse cycle complete. ===")


def main():
    logging.info("Anti-Gravity Heartbeat Daemon Starting...")

    # Audit frequency: every 10 minutes for initial testing.
    # Increase to 21600 (6 hours) for production.
    CHECK_INTERVAL = 600

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
