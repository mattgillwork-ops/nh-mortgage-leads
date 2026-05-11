from agents.ceo_agent import CEOAgent
from agents.coder_agent import CoderAgent
from agents.marketing_agent import MarketingAgent
from agents.verifier_agent import VerifierAgent
import os

# Boot agents
coder = CoderAgent()
marketing = MarketingAgent()
verifier = VerifierAgent()
ceo = CEOAgent(sub_agents={"coder": coder, "marketing": marketing, "verifier": verifier})

print("=== TEST 1: Simple Task (CEO handles directly) ===")
resp, model, verify = ceo.run("What is 2+2?")
print("Model:", model)
print("Verdict:", verify.get("verdict", "N/A"))
print("Response:", resp[:100], "...")
print()

print("=== TEST 2: Coding Task (CEO delegates to Coder) ===")
resp, model, verify = ceo.run("Write a Python function that checks if a number is prime.")
print("Model:", model)
print("Verdict:", verify.get("verdict", "N/A"))
print("Response:", resp[:150], "...")
print()

print("=== TEST 3: Marketing Task (CEO delegates to Marketing) ===")
resp, model, verify = ceo.run("Write an Instagram ad caption for a new AI productivity app called AntiGravity.")
print("Model:", model)
print("Verdict:", verify.get("verdict", "N/A"))
print("Response:", resp[:150], "...")
print()

logs = os.listdir(os.path.join("tru", "Memory_Logs"))
print("=== OBSIDIAN MEMORY:", len(logs), "logs saved ===")
for l in sorted(logs)[-6:]:
    print("  -", l)
