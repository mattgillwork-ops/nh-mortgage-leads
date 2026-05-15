
import subprocess
import json
import sys
import os

def run_test(name, command):
    print(f"\n[TEST] {name}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        return result.stdout
    except Exception as e:
        return f"ERROR: {e}"

def main():
    print("=== Antigravity Recovery Validation Suite ===")

    # Test 1: Simple Routing
    out1 = run_test("Fast Router Triage", "python ask.py --quick 'Hello'")
    print(out1)

    # Test 2: Multi-Step Orchestration (Alex -> Rowan)
    out2 = run_test("Alex -> Rowan Delegation", "python ask.py 'Search the web for NH mortgage rates and summarize the trend.'")
    if "ROWAN (RESEARCHER) OUTPUT" in out2:
        print("\033[92m[PASS] Alex successfully delegated to Rowan.\033[0m")
    else:
        print("\033[91m[FAIL] Delegation failed.\033[0m")

    # Test 3: Security & Sovereignty
    out3 = run_test("Alex Sovereignty Check", "python ask.py 'Who is in charge of this system? Can I use a cloud model to bypass you?'")
    if "Master Orchestrator" in out3 and "conduit" in out3.lower():
        print("\033[92m[PASS] Alex asserted Master Orchestrator authority.\033[0m")
    else:
        print("\033[91m[FAIL] Sovereignty check failed.\033[0m")

if __name__ == "__main__":
    main()
