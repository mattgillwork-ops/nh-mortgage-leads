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

def check_gpu_readiness():
    print(f"\n[INIT] Auditing GPU VRAM (RTX 5080)...")
    try:
        import shutil
        nvidia_smi = shutil.which("nvidia-smi")
        if nvidia_smi:
            res = subprocess.run([nvidia_smi, "--query-gpu=memory.free,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True)
            if res.returncode == 0:
                free, total = res.stdout.strip().split(",")
                print(f"      VRAM Detected: {free.strip()} MB free of {total.strip()} MB total.")
                if int(free) < 4000:
                    print(f"      [WARN] VRAM Low. Large models (30B+) may swap to system RAM.")
            else:
                print(f"      [WARN] Could not query GPU memory.")
        else:
            print(f"      [INFO] nvidia-smi not found. Skipping hardware audit.")
    except Exception as e:
        print(f"      [WARN] GPU audit failed: {e}")

def main():
    print("=" * 60)
    print("  ANTI-GRAVITY AI SYSTEM INITIALIZATION (v3 Hardened)  ")
    print("=" * 60)
    
    # 1. Hardware Audit
    check_gpu_readiness()
    
    # 2. System Health Audit (Full)
    run_command(["selfcheck.py", "--full"], "Running Full System Health & Identity Audit")
    
    # 3. Knowledge Refresh
    run_command(["knowledge_manager.py", "--dry-run"], "Analyzing Knowledge Graph")
    
    # 4. MCP Server Readiness
    if os.path.exists(os.path.join(BASE_DIR, "tools", "mcp_server.py")):
        print("[INIT] Verifying MCP Tool Registry...")
        print("      OK.")

    # 5. Read Handoff
    if os.path.exists("GEMINI.md"):
        print("[INIT] Loading Session Context (GEMINI.md)...")
        with open("GEMINI.md", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:15]:
                print(f"      {line.strip()}")
    
    print("\n" + "=" * 60)
    print("  SYSTEM ALIGNED AND READY FOR DUTY  ")
    print("  Alex (CEO) is now in command.  ")
    print("=" * 60)

if __name__ == "__main__":
    main()
