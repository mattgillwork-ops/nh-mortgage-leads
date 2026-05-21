"""
Anti-Gravity Quick Task Runner
==============================
Usage:
    py ask.py "your question or task here"
    py ask.py --code "write a function that does X"
    py ask.py --marketing "write ad copy for Y"

Routes tasks through local Ollama agents. Zero cloud tokens consumed.
"""

import sys
import os
import io

# Force UTF-8 for console output to prevent charmap errors on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.base_agent import BaseAgent
from agents.ceo_agent import CEOAgent
from agents.coder_agent import CoderAgent
from agents.marketing_agent import MarketingAgent
from agents.verifier_agent import VerifierAgent
from agents.devops_agent import DevOpsAgent
from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent
from agents.ux_agent import UXAgent
from agents.strategy_agent import StrategyAgent
from agents.researcher_agent import ResearcherAgent
from agents.devops_agent import DevOpsAgent
from agents.analyst_agent import AnalystAgent
from agents.ux_agent import UXAgent

import subprocess
from security_gate import scan_input


def run_preflight_check():
    """Runs a rapid health and security audit before starting the task."""
    print("[SYSTEM] Running Pre-Flight Audit...")
    try:
        # Run selfcheck in quick mode, capture output
        # Using sys.executable to ensure we use the same python environment
        result = subprocess.run(
            [sys.executable, "selfcheck.py", "--quick"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if "STATUS: CRITICAL ISSUES FOUND" in result.stdout:
            print("\033[91m[CRITICAL] System Health Check Failed!\033[0m")
            print(result.stdout)
            
            # If not interactive, we MUST block.
            if not sys.stdin.isatty():
                print("[CRITICAL] Non-interactive environment. Aborting to protect system integrity.")
                sys.exit(1)

            choice = input("Do you want to proceed anyway? (y/N): ")
            if choice.lower() != 'y':
                sys.exit(1)
        else:
            print("[SYSTEM] Pre-Flight Audit: \033[92mPASSED\033[0m")
    except Exception as e:
        print(f"[WARN] Pre-Flight Audit could not complete: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: py ask.py \"your question or task\"")
        print("       py ask.py --code \"write a function that...\"")
        print("       py ask.py --marketing \"write ad copy for...\"")
        print("\nAll tasks run on LOCAL Ollama models. Zero cloud tokens used.")
        sys.exit(0)

    # Parse arguments
    args = sys.argv[1:]

    # STRICT PROTOCOL: All bypass flags are deprecated.
    legacy_flags = ["--code", "--marketing", "--thinker", "--researcher", "--analyst", "--devops", "--ux", "--quick"]
    if len(args) > 0 and args[0] in legacy_flags:
        print(f"\n[WARNING] Direct delegation via {args[0]} is strictly prohibited under the Alex First Protocol.")
        print("[SYSTEM] Re-routing task to Alex (CEO Orchestrator) for proper decomposition...\n")
        args = args[1:]
    
    skip_check = False
    if "--skip-check" in args:
        skip_check = True
        args.remove("--skip-check")

    if not skip_check:
        run_preflight_check()

    prompt = " ".join(args)
    if not prompt.strip():
        print("Error: No task provided.")
        sys.exit(1)

    # Security Scan
    print("[SYSTEM] Scanning for security risks...")
    security_result = scan_input(prompt)
    if not security_result["is_safe"]:
        print(f"\033[91m[BLOCK] Security Risk Detected!\033[0m")
        print(f"Risk Score: {security_result['risk_score']}")
        print(f"Findings: {security_result['findings']}")
        print("This prompt has been blocked to protect the ecosystem.")
        sys.exit(1)
    else:
        print("[SYSTEM] Security Scan: \033[92mCLEARED\033[0m")

    # 2. Initialize the 11-Agent Squad
    fast_router = BaseAgent(agent_name="Fast Router", agent_id="fast_router")
    coder = CoderAgent()
    devops = DevOpsAgent()
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    marketing = MarketingAgent()
    ux = UXAgent()
    verifier = VerifierAgent()
    strategist = StrategyAgent()
    deep_thinker = BaseAgent(agent_name="Deep Thinker", agent_id="deep_thinker")
    
    # 3. Initialize Alex (CEO) with the full roster
    ceo = CEOAgent(sub_agents={
        "router": fast_router,
        "coder": coder, "caleb": coder,
        "devops": devops, "dax": devops,
        "researcher": researcher, "rowan": researcher,
        "analyst": analyst, "atlas": analyst,
        "marketing": marketing, "nova": marketing,
        "ux": ux, "aria": ux,
        "verifier": verifier, "vera": verifier,
        "strategist": strategist, "finn": strategist,
        "thinker": deep_thinker
    })

    # Full CEO pipeline - Alex First Protocol Enforced
    print("[LOCAL] Routing through Alex (CEO Orchestrator)...\n")
    response = ceo.run(prompt)
    print(response)


if __name__ == "__main__":
    main()
