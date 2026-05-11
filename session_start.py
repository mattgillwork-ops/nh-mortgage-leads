"""
Anti-Gravity Session Start Protocol
===================================
Triggered by: /lets get started
Aligns the system, checks health, and reports readiness.
"""

import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = sys.executable # Use the current interpreter

def run_command(cmd, desc):
    print(f"\n[INIT] {desc}...")
    try:
        result = subprocess.run([PYTHON_EXE] + cmd, capture_output=True, text=True, cwd=BASE_DIR)
        if result.returncode == 0:
            print(f"      OK.")
            return result.stdout
        else:
            print(f"      FAIL (Code {result.returncode})")
            print(f"      Error: {result.stderr[:200]}")
            return None
    except Exception as e:
        print(f"      CRITICAL ERROR: {e}")
        return None

def main():
    print("=" * 60)
    print("  ANTI-GRAVITY AI SYSTEM INITIALIZATION  ")
    print("=" * 60)
    
    # 1. Health Audit
    run_command(["selfcheck.py", "--quick"], "Running System Health Audit")
    
    # 2. Knowledge Refresh
    run_command(["knowledge_manager.py", "--dry-run"], "Analyzing Knowledge Graph")
    
    # 3. Read Handoff
    if os.path.exists("GEMINI.md"):
        print("[INIT] Loading Session Context (GEMINI.md)...")
        with open("GEMINI.md", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Show first 10 lines of handoff
            for line in lines[:15]:
                print(f"      {line.strip()}")
    
    print("\n" + "=" * 60)
    print("  SYSTEM ALIGNED AND READY FOR DUTY  ")
    print("  Alex (CEO) is now in command.  ")
    print("=" * 60)

if __name__ == "__main__":
    main()
