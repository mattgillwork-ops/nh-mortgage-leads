"""
Anti-Gravity Context Checkpoint Tool
====================================
Summarizes the current session state and updates GEMINI.md.
Usage: python tools/context_checkpoint.py "Optional summary of last actions"
"""

import os
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEMINI_PATH = os.path.join(BASE_DIR, "GEMINI.md")
TASKS_PATH = os.path.join(BASE_DIR, "CURRENT_TASKS.md")
FUTURE_PATH = os.path.join(BASE_DIR, "FUTURE_PROJECTS.md")

def get_file_content(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Not found."

def main():
    print("Generating Context Checkpoint...")
    
    manual_summary = sys.argv[1] if len(sys.argv) > 1 else "Infrastructure hardening and context optimization."
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    current_tasks = get_file_content(TASKS_PATH)
    future_projects = get_file_content(FUTURE_PATH)
    
    # Read the current GEMINI.md to preserve core architecture details
    old_gemini = get_file_content(GEMINI_PATH)
    
    # Extract the "Agent Squad" and "Key Architecture Details" sections (the stable parts)
    squad_match = old_gemini.split("## The Agent Squad")
    squad_section = "## The Agent Squad" + squad_match[1].split("##")[0] if len(squad_match) > 1 else ""
    
    arch_match = old_gemini.split("## Key Architecture Details")
    arch_section = "## Key Architecture Details" + arch_match[1].split("##")[0] if len(arch_match) > 1 else ""

    handoff_content = f"""# Anti-Gravity AI Ecosystem — Session Handoff (AUTO-GENERATED)

**Read this file first when resuming work.**

## Last Update: {timestamp}
**Last Actions**: {manual_summary}

{squad_section}

## Current Status
### Active Tasks
{current_tasks}

### Future Pipeline
{future_projects}

{arch_section}

## Instructions for Next Session
1. Read this `GEMINI.md` to align on current progress.
2. Run `/lets get started` to initialize the system.
3. Prioritize delegation to local agents via `ask.py`.
"""

    with open(GEMINI_PATH, 'w', encoding='utf-8') as f:
        f.write(handoff_content)
    
    print(f"Checkpoint saved to {GEMINI_PATH}")

if __name__ == "__main__":
    main()
