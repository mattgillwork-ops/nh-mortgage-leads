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

    prompt = " ".join(args)
    if not prompt.strip():
        print("Error: No task provided.")
        sys.exit(1)

    # Boot agents
    coder = CoderAgent()
    devops = DevOpsAgent()
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    marketing = MarketingAgent()
    ux = UXAgent()
    verifier = VerifierAgent()
    
    ceo = CEOAgent(sub_agents={
        "coder": coder, 
        "devops": devops,
        "researcher": researcher,
        "analyst": analyst,
        "marketing": marketing, 
        "ux": ux,
        "verifier": verifier
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
