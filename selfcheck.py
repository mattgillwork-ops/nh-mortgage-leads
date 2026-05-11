"""
Anti-Gravity Agent Ecosystem — Self-Check Diagnostic
=====================================================
Run: py selfcheck.py

Performs a comprehensive health, security, alignment, and identity
verification across the entire agent ecosystem.
"""

import os
import sys
import json
import glob
import time
import datetime
import ollama
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_PATH = os.path.join(BASE_DIR, "tru")
CORE_RULES_PATH = os.path.join(VAULT_PATH, "Core_Rules")
KNOWLEDGE_PATH = os.path.join(VAULT_PATH, "Knowledge_Graph")
MEMORY_LOGS_PATH = os.path.join(VAULT_PATH, "Memory_Logs")

REQUIRED_MODELS = [
    "anti-ceo",
    "anti-coder",
    "anti-marketing",
    "anti-verifier",
    "anti-fast-router",
    "anti-deep-thinker",
    "anti-analyst",
    "anti-devops",
    "anti-researcher",
    "anti-ux",
]

REQUIRED_CORE_FILES = [
    os.path.join(CORE_RULES_PATH, "AGENTS.md"),
    os.path.join(CORE_RULES_PATH, "GEMINI.md"),
]

REQUIRED_DIRECTORIES = [
    VAULT_PATH,
    CORE_RULES_PATH,
    KNOWLEDGE_PATH,
    MEMORY_LOGS_PATH,
    os.path.join(VAULT_PATH, "Visual_Logs"),
    os.path.join(BASE_DIR, "tools"),
]

REQUIRED_SOURCE_FILES = [
    os.path.join(BASE_DIR, "main.py"),
    os.path.join(BASE_DIR, "requirements.txt"),
    os.path.join(BASE_DIR, ".gitignore"),
    os.path.join(BASE_DIR, "agents", "__init__.py"),
    os.path.join(BASE_DIR, "agents", "base_agent.py"),
    os.path.join(BASE_DIR, "agents", "ceo_agent.py"),
    os.path.join(BASE_DIR, "agents", "coder_agent.py"),
    os.path.join(BASE_DIR, "agents", "marketing_agent.py"),
    os.path.join(BASE_DIR, "agents", "verifier_agent.py"),
    os.path.join(BASE_DIR, "agents", "analyst_agent.py"),
    os.path.join(BASE_DIR, "agents", "devops_agent.py"),
    os.path.join(BASE_DIR, "agents", "researcher_agent.py"),
    os.path.join(BASE_DIR, "agents", "ux_agent.py"),
    os.path.join(BASE_DIR, "tools", "web_search.py"),
    os.path.join(BASE_DIR, "tools", "mcp_server.py"),
]

SENSITIVE_PATTERNS = [
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "API_KEY",
    "SECRET",
    "PASSWORD",
    "TOKEN",
]

# Max memory logs before warning (prevents unbounded growth)
MEMORY_LOG_WARNING_THRESHOLD = 500

# Identity challenge prompts — each agent should respond in character
IDENTITY_CHALLENGES = {
    "anti-ceo": {
        "prompt": "What is your name and what is your primary role? Respond in one sentence.",
        "expected_keywords": ["ceo", "orchestrat", "delegat", "route", "task"],
    },
    "anti-coder": {
        "prompt": "What is your name and what do you specialize in? Respond in one sentence.",
        "expected_keywords": ["cod", "programm", "software", "debug", "script", "develop"],
    },
    "anti-marketing": {
        "prompt": "What is your name and what is your specialty? Respond in one sentence.",
        "expected_keywords": ["market", "creative", "copy", "brand", "content", "advertis"],
    },
    "anti-verifier": {
        "prompt": "Evaluate this task: 'Task: Print hello. Output: print(\"hello\")'. Ensure you return your standard JSON verdict.",
        "expected_keywords": ["verdict", "pass", "confidence"],
    },
    "anti-analyst": {
        "prompt": "What is your name and what do you do? Respond in one sentence.",
        "expected_keywords": ["analyst", "data", "insight", "metric", "trend"],
    },
    "anti-devops": {
        "prompt": "What is your name and what is your role? Respond in one sentence.",
        "expected_keywords": ["devops", "deploy", "infrastructure", "git", "pipeline", "docker"],
    },
    "anti-researcher": {
        "prompt": "What is your name and what is your purpose? Respond in one sentence.",
        "expected_keywords": ["research", "gather", "information", "web", "search", "summarize"],
    },
    "anti-ux": {
        "prompt": "What is your name and what do you specialize in? Respond in one sentence.",
        "expected_keywords": ["ux", "ui", "design", "glassmorphism", "aesthetic", "visual"],
    },
}

# Routing accuracy test cases
ROUTING_TESTS = [
    {"prompt": "Write a Python web scraper", "expected_delegate": "coder"},
    {"prompt": "Write a catchy email subject line for our sale", "expected_delegate": "communications"},
    {"prompt": "What is the capital of Japan?", "expected_delegate": "researcher"},
    {"prompt": "Analyze the CSV file to find the average revenue", "expected_delegate": "analyst"},
    {"prompt": "Deploy this docker container to AWS", "expected_delegate": "devops"},
    {"prompt": "Search the web for the latest news on AI", "expected_delegate": "researcher"},
    {"prompt": "Make this dashboard look like a premium glassmorphic interface", "expected_delegate": "ux"},
]


# ============================================================
# HELPERS
# ============================================================

class Colors:
    """ANSI color codes for terminal output."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 56}")
    print(f"  {title}")
    print(f"{'=' * 56}{Colors.RESET}\n")


def print_pass(msg):
    print(f"  {Colors.GREEN}[PASS]{Colors.RESET} {msg}")


def print_fail(msg):
    print(f"  {Colors.RED}[FAIL]{Colors.RESET} {msg}")


def print_warn(msg):
    print(f"  {Colors.YELLOW}[WARN]{Colors.RESET} {msg}")


def print_info(msg):
    print(f"  {Colors.CYAN}[INFO]{Colors.RESET} {msg}")


# ============================================================
# CHECK MODULES
# ============================================================

def check_ollama_health():
    """Check 1: Verify Ollama server is running and responsive."""
    print_header("CHECK 1: Ollama Server Health")
    passed = 0
    failed = 0

    try:
        models = ollama.list()
        print_pass(f"Ollama server is running and responsive.")
        print_info(f"Total models installed: {len(models.get('models', []))}")
        passed += 1
    except Exception as e:
        print_fail(f"Ollama server is NOT reachable: {e}")
        print_info("Is Ollama running? Try: ollama serve")
        failed += 1

    return passed, failed


def check_model_availability():
    """Check 2: Verify all required custom models are registered in Ollama."""
    print_header("CHECK 2: Model Availability")
    passed = 0
    failed = 0

    try:
        result = ollama.list()
        # Handle different response formats from the Ollama SDK
        model_list = result.get("models", []) if isinstance(result, dict) else getattr(result, "models", [])
        installed = []
        for m in model_list:
            name = m["name"] if isinstance(m, dict) else getattr(m, "model", getattr(m, "name", ""))
            installed.append(name.split(":")[0])

        for model in REQUIRED_MODELS:
            if model in installed:
                print_pass(f"Model '{model}' is registered.")
                passed += 1
            else:
                print_fail(f"Model '{model}' is MISSING from Ollama.")
                failed += 1
    except Exception as e:
        print_fail(f"Could not query Ollama model list: {e}")
        failed += len(REQUIRED_MODELS)

    return passed, failed


def check_identity_drift():
    """Check 3: Challenge each agent to verify they still know who they are."""
    print_header("CHECK 3: Agent Identity Drift")
    passed = 0
    failed = 0

    for model_name, challenge in IDENTITY_CHALLENGES.items():
        try:
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": challenge["prompt"]}]
            )
            answer = response["message"]["content"].lower()

            # Check if any expected keywords appear in the response
            matches = [kw for kw in challenge["expected_keywords"] if kw in answer]

            if len(matches) >= 1:
                print_pass(f"'{model_name}' identity intact. Matched: {matches}")
                passed += 1
            else:
                print_fail(f"'{model_name}' IDENTITY DRIFT DETECTED!")
                print_info(f"  Response: {answer[:120]}...")
                print_info(f"  Expected keywords: {challenge['expected_keywords']}")
                failed += 1

        except Exception as e:
            print_fail(f"'{model_name}' failed to respond: {e}")
            failed += 1

    return passed, failed


def check_routing_accuracy():
    """Check 4: Verify the CEO correctly routes different task types."""
    print_header("CHECK 4: CEO Routing Accuracy")
    passed = 0
    failed = 0

    for test in ROUTING_TESTS:
        try:
            response = ollama.chat(
                model="anti-ceo",
                messages=[{"role": "user", "content": test["prompt"]}],
                format="json",
            )
            content = response["message"]["content"]
            parsed = json.loads(content)
            actual = parsed.get("delegate_to", "unknown")

            if actual == test["expected_delegate"]:
                print_pass(f"'{test['prompt'][:40]}...' -> {actual} (correct)")
                passed += 1
            else:
                print_fail(f"'{test['prompt'][:40]}...' -> {actual} (expected: {test['expected_delegate']})")
                failed += 1

        except Exception as e:
            print_fail(f"Routing test failed for '{test['prompt'][:40]}...': {e}")
            failed += 1

    return passed, failed


def check_vault_structure():
    """Check 5: Verify the Obsidian vault directory structure is intact."""
    print_header("CHECK 5: Obsidian Vault Structure")
    passed = 0
    failed = 0

    for directory in REQUIRED_DIRECTORIES:
        if os.path.isdir(directory):
            print_pass(f"Directory exists: {os.path.relpath(directory, BASE_DIR)}")
            passed += 1
        else:
            print_fail(f"Directory MISSING: {os.path.relpath(directory, BASE_DIR)}")
            failed += 1

    return passed, failed


def check_core_rules_integrity():
    """Check 6: Verify core rule files exist and are not empty."""
    print_header("CHECK 6: Core Rules Integrity")
    passed = 0
    failed = 0

    for filepath in REQUIRED_CORE_FILES:
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            if size > 50:
                print_pass(f"{os.path.basename(filepath)} intact ({size} bytes)")
                passed += 1
            else:
                print_warn(f"{os.path.basename(filepath)} exists but suspiciously small ({size} bytes)")
                failed += 1
        else:
            print_fail(f"{os.path.basename(filepath)} is MISSING!")
            failed += 1

    return passed, failed


def check_source_files():
    """Check 7: Verify all required source code files exist."""
    print_header("CHECK 7: Source File Inventory")
    passed = 0
    failed = 0

    for filepath in REQUIRED_SOURCE_FILES:
        if os.path.isfile(filepath):
            print_pass(f"{os.path.relpath(filepath, BASE_DIR)}")
            passed += 1
        else:
            print_fail(f"MISSING: {os.path.relpath(filepath, BASE_DIR)}")
            failed += 1

    return passed, failed


def check_security():
    """Check 8: Security audit — API keys, .env exposure, .gitignore coverage."""
    print_header("CHECK 8: Security Audit")
    passed = 0
    failed = 0

    # 8a. Check that .env is NOT committed (exists in .gitignore)
    gitignore_path = os.path.join(BASE_DIR, ".gitignore")
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        if ".env" in gitignore_content:
            print_pass(".env is listed in .gitignore")
            passed += 1
        else:
            print_fail(".env is NOT in .gitignore — API keys may be exposed!")
            failed += 1
    else:
        print_fail(".gitignore file does not exist!")
        failed += 1

    # 8b. Scan Python files for hardcoded secrets
    py_files = glob.glob(os.path.join(BASE_DIR, "**", "*.py"), recursive=True)
    secrets_found = False
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            for pattern in SENSITIVE_PATTERNS:
                # Look for hardcoded assignments like API_KEY = "sk-..."
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if pattern in stripped and "=" in stripped and ("\"" in stripped or "'" in stripped):
                        # Exclude lines that use os.getenv or os.environ
                        if "getenv" not in stripped and "environ" not in stripped and "#" not in stripped.split("=")[0]:
                            print_fail(f"Potential hardcoded secret in {os.path.relpath(py_file, BASE_DIR)}:{i+1}")
                            print_info(f"  -> {stripped[:80]}")
                            secrets_found = True
                            failed += 1
        except Exception:
            pass

    if not secrets_found:
        print_pass("No hardcoded secrets found in Python source files.")
        passed += 1

    # 8c. Check if .env file exists (informational)
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.isfile(env_path):
        print_pass(".env file exists for environment variable management.")
        passed += 1
    else:
        print_warn(".env file not found. Cloud fallback (Gemini) will not work.")

    return passed, failed


def check_memory_health():
    """Check 9: Memory log health — count, size, and growth rate."""
    print_header("CHECK 9: Memory Health")
    passed = 0
    failed = 0

    if not os.path.isdir(MEMORY_LOGS_PATH):
        print_fail("Memory_Logs directory does not exist.")
        return 0, 1

    log_files = sorted(glob.glob(os.path.join(MEMORY_LOGS_PATH, "*.md")))
    log_count = len(log_files)
    total_size = sum(os.path.getsize(f) for f in log_files)
    total_size_kb = total_size / 1024

    print_info(f"Total memory logs: {log_count}")
    print_info(f"Total memory size: {total_size_kb:.1f} KB")

    if log_count == 0:
        print_warn("No memory logs found. System has not logged any tasks yet.")
    elif log_count < MEMORY_LOG_WARNING_THRESHOLD:
        print_pass(f"Memory log count ({log_count}) is within healthy range.")
        passed += 1
    else:
        print_warn(f"Memory log count ({log_count}) exceeds threshold ({MEMORY_LOG_WARNING_THRESHOLD}).")
        print_info("Consider archiving old logs to prevent context window bloat.")
        failed += 1

    # Check most recent log timestamp
    if log_files:
        newest = log_files[-1]
        mod_time = os.path.getmtime(newest)
        mod_dt = datetime.datetime.fromtimestamp(mod_time)
        age = datetime.datetime.now() - mod_dt
        print_info(f"Most recent log: {os.path.basename(newest)} ({age.seconds // 60} min ago)")

        # Verify the newest log is readable and non-empty
        try:
            with open(newest, 'r', encoding='utf-8') as f:
                content = f.read()
            if len(content) > 20:
                print_pass("Latest memory log is readable and non-empty.")
                passed += 1
            else:
                print_fail("Latest memory log appears corrupted (too small).")
                failed += 1
        except Exception as e:
            print_fail(f"Could not read latest memory log: {e}")
            failed += 1

    return passed, failed


def check_resilience_config():
    """Check 10: Verify the resilience/fallback configuration is intact."""
    print_header("CHECK 10: Resilience & Fallback Configuration")
    passed = 0
    failed = 0

    # Check that base_agent.py contains the resilience decorator
    base_agent_path = os.path.join(BASE_DIR, "agents", "base_agent.py")
    if os.path.isfile(base_agent_path):
        with open(base_agent_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "resilience_module" in content:
            print_pass("Resilience module decorator is present in base_agent.py")
            passed += 1
        else:
            print_fail("Resilience module decorator is MISSING from base_agent.py!")
            failed += 1

        if "max_retries=3" in content:
            print_pass("Default retry count is set to 3.")
            passed += 1
        else:
            print_warn("Default retry count may have been modified.")

        if "cloud_fallback" in content:
            print_pass("Cloud fallback method is present.")
            passed += 1
        else:
            print_fail("Cloud fallback method is MISSING!")
            failed += 1

        if "gemini" in content.lower():
            print_pass("Gemini API integration is configured.")
            passed += 1
        else:
            print_fail("Gemini API integration appears to be missing.")
            failed += 1
    else:
        print_fail("base_agent.py not found!")
        failed += 4

    # Check if GEMINI_API_KEY is available
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print_pass("GEMINI_API_KEY environment variable is set.")
        passed += 1
    else:
        print_warn("GEMINI_API_KEY not set. Cloud fallback will fail if needed.")

    return passed, failed


def check_mcp_health():
    """Check 11: Verify MCP server and tool registry."""
    print_header("CHECK 11: MCP Server & Tool Registry")
    passed = 0
    failed = 0

    mcp_path = os.path.join(BASE_DIR, "tools", "mcp_server.py")
    if os.path.isfile(mcp_path):
        print_pass("MCP Server script (mcp_server.py) exists.")
        passed += 1
        
        # Check for FastMCP import
        with open(mcp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "FastMCP" in content:
            print_pass("MCP server is using the modern FastMCP framework.")
            passed += 1
        else:
            print_fail("MCP server is using outdated or missing FastMCP framework.")
            failed += 1
    else:
        print_fail("MCP Server script is MISSING!")
        failed += 1

    # Check for mcp dependency
    try:
        import mcp
        print_pass("MCP Python SDK is installed.")
        passed += 1
    except ImportError:
        print_fail("MCP Python SDK is NOT installed.")
        failed += 1

    return passed, failed


def check_hardened_security():
    """Check 12: Verify hardened tool regex and security protocols."""
    print_header("CHECK 12: Hardened Security Audit")
    passed = 0
    failed = 0

    base_agent_path = os.path.join(BASE_DIR, "agents", "base_agent.py")
    if os.path.isfile(base_agent_path):
        with open(base_agent_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for the hardened MCP regex
        if r"mcp_pattern = re.compile(r'<\|?mcp_call" in content:
            print_pass("Hardened MCP tool-calling regex is present in BaseAgent.")
            passed += 1
        else:
            print_fail("Hardened MCP regex is MISSING. Hallucination risk is high!")
            failed += 1
            
        if "asyncio.run(self._execute_mcp_tool" in content:
            print_pass("BaseAgent is correctly bridging sync and async for MCP.")
            passed += 1
        else:
            print_fail("BaseAgent is missing the MCP execution bridge.")
            failed += 1
    else:
        print_fail("BaseAgent.py is missing!")
        failed += 2

    return passed, failed


# ============================================================
# MAIN RUNNER
# ============================================================

def run_selfcheck(skip_live=False):
    """Run the full self-check diagnostic suite."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("  +==================================================+")
    print("  |     Anti-Gravity Self-Check Diagnostic v1.0       |")
    print("  +==================================================+")
    print(f"{Colors.RESET}")
    print(f"  Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Workspace: {BASE_DIR}")

    total_passed = 0
    total_failed = 0
    start_time = time.time()

    # Static checks (fast, no model calls)
    checks = [
        check_ollama_health,
        check_model_availability,
        check_vault_structure,
        check_core_rules_integrity,
        check_source_files,
        check_security,
        check_memory_health,
        check_resilience_config,
        check_mcp_health,
        check_hardened_security,
    ]

    for check in checks:
        p, f = check()
        total_passed += p
        total_failed += f

    # Live checks (slower, require model inference)
    if not skip_live:
        print(f"\n{Colors.YELLOW}  Running live agent checks (this may take 1-2 minutes)...{Colors.RESET}")

        p, f = check_identity_drift()
        total_passed += p
        total_failed += f

        p, f = check_routing_accuracy()
        total_passed += p
        total_failed += f
    else:
        print(f"\n{Colors.YELLOW}  Skipping live agent checks (use --full to include).{Colors.RESET}")

    # Final Report
    elapsed = time.time() - start_time
    total_checks = total_passed + total_failed

    print_header("SELF-CHECK REPORT")
    print(f"  Total Checks:  {total_checks}")
    print(f"  {Colors.GREEN}Passed:        {total_passed}{Colors.RESET}")
    print(f"  {Colors.RED}Failed:        {total_failed}{Colors.RESET}")
    print(f"  Time Elapsed:  {elapsed:.1f}s")
    print()

    if total_failed == 0:
        print(f"  {Colors.GREEN}{Colors.BOLD}STATUS: ALL SYSTEMS OPERATIONAL{Colors.RESET}")
    elif total_failed <= 2:
        print(f"  {Colors.YELLOW}{Colors.BOLD}STATUS: MINOR ISSUES DETECTED{Colors.RESET}")
    else:
        print(f"  {Colors.RED}{Colors.BOLD}STATUS: CRITICAL ISSUES FOUND — ACTION REQUIRED{Colors.RESET}")

    print()

    # Save report to Obsidian
    save_report_to_obsidian(total_passed, total_failed, elapsed)

    return total_failed


def save_report_to_obsidian(passed, failed, elapsed):
    """Save a summary of the self-check to the Obsidian Memory_Logs."""
    if not os.path.isdir(MEMORY_LOGS_PATH):
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(MEMORY_LOGS_PATH, f"selfcheck_{timestamp}.md")

    status = "ALL SYSTEMS OPERATIONAL" if failed == 0 else f"{failed} ISSUES FOUND"
    report = (
        f"# Self-Check Report: {timestamp}\n\n"
        f"**Status**: {status}\n"
        f"**Passed**: {passed}\n"
        f"**Failed**: {failed}\n"
        f"**Duration**: {elapsed:.1f}s\n"
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print_info(f"Report saved to Obsidian: {os.path.basename(filename)}")


if __name__ == "__main__":
    skip_live = "--quick" in sys.argv
    if "--full" in sys.argv:
        skip_live = False
    elif "--quick" in sys.argv:
        skip_live = True
    else:
        # Default: run full checks including live agent tests
        skip_live = False

    exit_code = run_selfcheck(skip_live=skip_live)
    sys.exit(exit_code)
