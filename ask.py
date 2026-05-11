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

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.ceo_agent import CEOAgent
from agents.coder_agent import CoderAgent
from agents.marketing_agent import MarketingAgent
from agents.verifier_agent import VerifierAgent
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
    force_agent = None

    if args[0] == "--code":
        force_agent = "coder"
        args = args[1:]
    elif args[0] == "--marketing":
        force_agent = "marketing"
        args = args[1:]
    elif args[0] == "--quick":
        # Skip verification for maximum speed
        force_agent = "quick"
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

    # Boot agents
    coder = CoderAgent()
    devops = DevOpsAgent()
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    marketing = MarketingAgent()
    ux = UXAgent()
    verifier = VerifierAgent()
    
    ceo = CEOAgent(sub_agents={
        "coder": coder, "caleb": coder,
        "devops": devops, "dax": devops,
        "researcher": researcher, "rowan": researcher,
        "analyst": analyst, "atlas": analyst,
        "marketing": marketing, "nova": marketing, "communications": marketing,
        "ux": ux, "aria": ux,
        "verifier": verifier, "vera": verifier
    })

    if force_agent == "coder":
        print("[LOCAL] Routing directly to Coder Agent (anti-coder)...\n")
        response = coder.run(prompt)
        print(response)
    elif force_agent == "marketing":
        print("[LOCAL] Routing directly to Marketing Agent (anti-marketing)...\n")
        response = marketing.run(prompt)
        print(response)
    elif force_agent == "quick":
        # Use the fast router model directly, no verification
        print("[LOCAL] Quick mode (anti-fast-router, no verification)...\n")
        import ollama
        result = ollama.chat(model="anti-fast-router", messages=[{"role": "user", "content": prompt}])
        print(result["message"]["content"])
    else:
        # Full CEO pipeline
        print("[LOCAL] Routing through Alex (CEO Orchestrator)...\n")
        response, model_used, verification = ceo.run(prompt)
        print(f"--- Model: {model_used} | Verdict: {verification.get('verdict', 'N/A')} ---\n")
        print(response)


if __name__ == "__main__":
    main()
