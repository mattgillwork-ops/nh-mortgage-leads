import os
import sys
import shutil
import glob
import subprocess

def print_header(msg):
    print(f"\n\033[1;36m=== {msg} ===\033[0m")

def print_step(msg):
    print(f"\033[1;32m[+]\033[0m {msg}")

def print_warning(msg):
    print(f"\033[1;33m[!]\033[0m {msg}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/clone_workspace.py <target_directory>")
        sys.exit(1)

    target_dir = sys.argv[1]
    source_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print_header(f"Anti-Gravity Ecosystem Bootstrapper")
    print_step(f"Source: {source_dir}")
    print_step(f"Target: {target_dir}")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print_step("Created target directory.")
    else:
        print_warning("Target directory already exists. Proceeding with copy.")

    # Core files to copy
    core_files = [
        "agent_registry.yaml",
        "model_registry.yaml",
        "agent_router.py",
        "ask.py",
        "main.py",
        "server.py",
        "heartbeat_daemon.py",
        "session_start.py",
        "selfcheck.py",
        "knowledge_manager.py",
        "security_gate.py",
        "docker_runner.py",
        "qa_check.py",
        "requirements.txt",
        "Dockerfile.sandbox",
        "docker-compose.yml",
        "fix_gpu.ps1",
        "start_dashboard.ps1",
        "setup.sh",
        "launch.sh",
        "WORKSPACE_AI_RULES.md",
        "ARCHITECTURE_V3.md",
        ".env"
    ]

    print_header("Copying Core Logic & Tools")
    for file in core_files:
        src = os.path.join(source_dir, file)
        dst = os.path.join(target_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print_step(f"Copied {file}")

    # Copy Modelfiles
    modelfiles = glob.glob(os.path.join(source_dir, "Modelfile.*"))
    for modelfile in modelfiles:
        basename = os.path.basename(modelfile)
        shutil.copy2(modelfile, os.path.join(target_dir, basename))
        print_step(f"Copied {basename}")

    # Copy Agents and Tools directories
    for d in ["agents", "tools"]:
        src = os.path.join(source_dir, d)
        dst = os.path.join(target_dir, d)
        if not os.path.exists(dst):
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
            print_step(f"Copied directory {d}/")

    print_header("Bootstrapping Obsidian Vault (tru/)")
    tru_src = os.path.join(source_dir, "tru")
    tru_dst = os.path.join(target_dir, "tru")
    
    if not os.path.exists(tru_dst):
        os.makedirs(tru_dst)
        print_step("Created tru/ vault directory.")

    # Structure to recreate empty
    empty_dirs = [
        "Archive", "Audit", "Browser_Sessions", "Memory_Logs", "Data", "Leads", "Visual_Logs", "Projects", "Templates", "Research", "Knowledge_Graph", "vector_db", "chroma_db", ".obsidian"
    ]
    for d in empty_dirs:
        os.makedirs(os.path.join(tru_dst, d), exist_ok=True)

    # Core rules to copy
    rules_src = os.path.join(tru_src, "Core_Rules")
    if os.path.exists(rules_src):
        shutil.copytree(rules_src, os.path.join(tru_dst, "Core_Rules"), dirs_exist_ok=True)
        print_step("Copied tru/Core_Rules/")

    # Generate workspace templates
    print_header("Creating Fresh Workspace Templates")
    templates = {
        "CURRENT_TASKS.md": "# Active Tasks\n\n- `[ ]` Initial Setup for New Project\n",
        "FUTURE_PROJECTS.md": "# Future Pipeline\n\n- None yet.\n",
        "POSSIBLE_PROJECTS.md": "# Possible Projects\n\n- None yet.\n",
        "Learnings.md": "# System Learnings\n\n",
        "GEMINI.md": "# Anti-Gravity AI Ecosystem — Session Handoff\n\n**Summary**: Brand new workspace initialized.\n\n## The Agent Squad\n| Agent | Role | Model |\n|-------|------|-------|\n| Alex | CEO/Orchestrator | `anti-ceo` |\n| Caleb | Coder | `anti-coder` |\n| Aria | UX/Design | `anti-ux` |\n| Dax | DevOps | `anti-devops` |\n| Nova | Marketing | `anti-marketing` |\n| Rowan | Researcher | `anti-researcher` |\n| Atlas | Analyst | `anti-analyst` |\n| Vera | Verifier | `anti-verifier` |\n| Finn | Brainstormer | `anti-brainstormer` |\n"
    }

    for name, content in templates.items():
        with open(os.path.join(target_dir, name), "w", encoding="utf-8") as f:
            f.write(content)
        print_step(f"Created template {name}")

    print_header("Initializing Git Repository")
    try:
        subprocess.run(["git", "init"], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
        
        # Add basic .gitignore
        with open(os.path.join(target_dir, ".gitignore"), "w") as f:
            f.write("node_modules/\n.next/\n__pycache__/\nvenv/\n*.log\n.env\n")
            
        print_step("Initialized empty Git repository and .gitignore")
    except Exception as e:
        print_warning(f"Could not initialize git: {e}")

    print_header("Workspace Bootstrapping Complete!")
    print(f"\nNext Steps:")
    print(f"  1. cd {target_dir}")
    print(f"  2. py -m venv venv")
    print(f"  3. .\\venv\\Scripts\\activate")
    print(f"  4. pip install -r requirements.txt")
    print(f"  5. py selfcheck.py\n")

if __name__ == "__main__":
    main()
