"""
Anti-Gravity Agent Ecosystem — Main Entry Point
================================================
This script boots up the full CEO + Sub-Agent pipeline and provides
an interactive CLI for testing the multi-agent system.
"""

import sys
import json
from agents.ceo_agent import CEOAgent
from agents.coder_agent import CoderAgent
from agents.marketing_agent import MarketingAgent
from agents.verifier_agent import VerifierAgent
from agents.researcher_agent import ResearcherAgent
from agents.devops_agent import DevOpsAgent
from agents.analyst_agent import AnalystAgent
from agents.ux_agent import UXAgent


def main():
    print("=" * 56)
    print("    🚀 Anti-Gravity Agent Ecosystem v2.0 🚀")
    print("=" * 56)
    print()
    print("  Agents Online:")
    print("  ├── 👨‍💼 Alex (CEO)         (anti-ceo)")
    print("  ├── 💻 Coder Agent       (anti-coder)")
    print("  ├── 🛠️ DevOps Agent      (anti-devops)")
    print("  ├── 🔍 Researcher Agent  (anti-researcher)")
    print("  ├── 📊 Analyst Agent     (anti-analyst)")
    print("  ├── 📣 Marketing Agent   (anti-marketing)")
    print("  ├── 🎨 Aria (UX Agent)    (anti-ux)")
    print("  └── ✅ Verifier Agent    (anti-verifier)")
    print()

    # Boot up sub-agents
    coder = CoderAgent()
    devops = DevOpsAgent()
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    marketing = MarketingAgent()
    ux = UXAgent()
    verifier = VerifierAgent()

    # Boot CEO with references to sub-agents
    ceo = CEOAgent(sub_agents={
        "coder": coder,
        "devops": devops,
        "researcher": researcher,
        "analyst": analyst,
        "marketing": marketing,
        "ux": ux,
        "verifier": verifier,
    })

    print("All agents initialized. Ready for tasks.\n")

    while True:
        try:
            print("-" * 56)
            print("Enter your task (or 'exit' to quit):")
            user_input = input("> ")

            if user_input.lower() in ['exit', 'quit']:
                print("Shutting down Anti-Gravity Agent Ecosystem...")
                break

            if not user_input.strip():
                continue

            print("\n⏳ Processing...\n")

            # Run the full CEO pipeline
            response = ceo.run(user_input)

            # Display results
            print("\n📋 RESPONSE:\n")
            print(response)
            print("\n" + "=" * 56)

        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")



if __name__ == "__main__":
    main()
