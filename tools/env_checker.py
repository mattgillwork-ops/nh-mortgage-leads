"""
Anti-Gravity Environment Checker Tool
=======================================
Verifies that required system tools are installed and reachable before agents run.
Used by the Heartbeat Daemon pre-flight check and by Dax (DevOps) before any deployment.

Returns structured status for each tool — agents can parse this to decide whether
to proceed or report a failure.
"""

import subprocess
import shutil
import sys
import os
import logging

logger = logging.getLogger("EnvChecker")


def _run(cmd: list[str], timeout: int = 10) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, (result.stdout + result.stderr).strip()
    except subprocess.TimeoutExpired:
        return False, f"[Timeout after {timeout}s]"
    except FileNotFoundError:
        return False, "[Not installed or not in PATH]"
    except Exception as e:
        return False, str(e)


def check_ollama() -> dict:
    """Check if Ollama is running and responsive."""
    ok, out = _run(["ollama", "list"])
    return {"tool": "ollama", "ok": ok, "detail": out[:200] if ok else out}


def check_docker() -> dict:
    """Check if Docker daemon is running."""
    ok, out = _run(["docker", "ps"])
    return {"tool": "docker", "ok": ok, "detail": "Docker daemon is running." if ok else out}


def check_git() -> dict:
    """Check if git is installed."""
    ok, out = _run(["git", "--version"])
    return {"tool": "git", "ok": ok, "detail": out}


def check_python() -> dict:
    """Confirm the Python interpreter version."""
    version = sys.version.split()[0]
    return {"tool": "python", "ok": True, "detail": f"Python {version} at {sys.executable}"}


def check_npm() -> dict:
    """Check if npm is installed (needed for frontend work)."""
    ok, out = _run(["npm", "--version"])
    return {"tool": "npm", "ok": ok, "detail": f"npm {out}" if ok else out}


def check_pip_package(package: str) -> dict:
    """Check if a Python package is importable."""
    try:
        __import__(package)
        return {"tool": f"pip:{package}", "ok": True, "detail": f"{package} is importable."}
    except ImportError:
        return {"tool": f"pip:{package}", "ok": False, "detail": f"{package} is NOT installed."}


def run_full_check(required_packages: list[str] = None) -> str:
    """
    Run all environment checks and return a formatted report string.
    Used by the Heartbeat pre-flight and by Dax before deployments.
    """
    if required_packages is None:
        required_packages = ["ollama", "chromadb", "fastapi", "yaml", "bs4", "requests", "pyautogui"]

    checks = [
        check_python(),
        check_ollama(),
        check_docker(),
        check_git(),
        check_npm(),
    ]

    for pkg in required_packages:
        checks.append(check_pip_package(pkg))

    lines = ["=== Environment Check ==="]
    all_ok = True
    for check in checks:
        status = "[OK]  " if check["ok"] else "[FAIL]"
        lines.append(f"  {status} [{check['tool']}] {check['detail']}")
        if not check["ok"]:
            all_ok = False

    lines.append("=========================")
    lines.append(f"Overall: {'ALL SYSTEMS GO' if all_ok else 'ISSUES DETECTED'}")

    report = "\n".join(lines)
    logger.info(f"Environment check complete. All OK: {all_ok}")
    return report


if __name__ == "__main__":
    print(run_full_check())
