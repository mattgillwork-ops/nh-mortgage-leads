import os
import sys
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEMINI_PATH = os.path.join(BASE_DIR, "GEMINI.md")
TASKS_PATH = os.path.join(BASE_DIR, "CURRENT_TASKS.md")
FUTURE_PATH = os.path.join(BASE_DIR, "FUTURE_PROJECTS.md")
PYTHON_EXE = sys.executable

def get_file_content(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Not found."

def extract_section(content, section_title):
    """Extracts a section from markdown content until the next ## header."""
    if section_title not in content:
        return ""
    start = content.split(section_title)[1]
    section = section_title + start.split("##")[0]
    return section.strip()

def main():
    print("Generating Context Checkpoint (v3 Hardened)...")
    
    manual_summary = sys.argv[1] if len(sys.argv) > 1 else "Context optimization and session sync."
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    current_tasks = get_file_content(TASKS_PATH)
    future_projects = get_file_content(FUTURE_PATH)
    old_gemini = get_file_content(GEMINI_PATH)
    
    # Preserve Critical Infrastructure Sections
    squad_section = extract_section(old_gemini, "## The Agent Squad")
    arch_section = extract_section(old_gemini, "## Key Architecture Details")
    prefs_section = extract_section(old_gemini, "## User Preferences")
    issues_section = extract_section(old_gemini, "## Known Issues")
    files_section = extract_section(old_gemini, "## Important Files")

    # 1. Index Session Learnings into Knowledge Graph
    print("[CHECKPOINT] Indexing session learnings...")
    try:
        subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "knowledge_manager.py"), "--index"], capture_output=True)
        print("      OK.")
    except Exception as e:
        print(f"      [WARN] Knowledge indexing failed: {e}")

    handoff_content = f"""# Anti-Gravity AI Ecosystem — Session Handoff

**Read this file first when resuming work.**

## Last Checkpoint: {timestamp}
**Summary**: {manual_summary}

{squad_section}

## Current Phase: Intelligence & Growth Initiation (ACTIVE)

## Current Status
### Active Tasks
{current_tasks}

### Future Pipeline
{future_projects}

{arch_section}

{prefs_section}

{files_section}

{issues_section}

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
