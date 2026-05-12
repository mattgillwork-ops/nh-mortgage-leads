import os
import re
import glob
import yaml
from datetime import datetime

# Path definitions
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "tru", "Memory_Logs")

# Normalization map for agents
AGENT_MAP = {
    "alex": "Alex_CEO",
    "ceo": "Alex_CEO",
    "coder": "Caleb_Coder",
    "anti-coder": "Caleb_Coder",
    "verifier": "Vera_Verifier",
    "anti-verifier": "Vera_Verifier",
    "devops": "Dax_DevOps",
    "anti-devops": "Dax_DevOps",
    "marketing": "Nova_Marketing",
    "anti-marketing": "Nova_Marketing",
    "researcher": "Rowan_Researcher",
    "anti-researcher": "Rowan_Researcher",
    "analyst": "Atlas_Analyst",
    "anti-analyst": "Atlas_Analyst",
    "brainstormer": "Finn_Brainstormer",
    "ux": "Aria_UX",
    "fast router": "Alex_CEO", # Treat Fast Router tasks as CEO orchestration
    "deep thinker": "Alex_CEO" # Treat deep thinker tasks as CEO orchestration
}

def normalize_agent(agent_str: str) -> str:
    agent_lower = agent_str.lower()
    for key, mapped in AGENT_MAP.items():
        if key in agent_lower:
            return mapped
    return "Unknown_Agent"

def process_log_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already processed
    if "## Meta Connections" in content:
        return False

    agent = "Unknown_Agent"
    date_str = ""
    status = "completed"
    task_type = "execution"
    model = ""
    
    body_content = content

    # Check for existing YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                body_content = parts[2].strip()
                if isinstance(frontmatter, dict):
                    agent = frontmatter.get("agent", agent)
                    date_str = frontmatter.get("date", date_str)
                    model = frontmatter.get("model", model)
                    status = frontmatter.get("status", status)
                    task_type = frontmatter.get("task_type", task_type)
            except yaml.YAMLError:
                pass

    # If no agent found in YAML, try to find it in markdown
    if agent == "Unknown_Agent" or not agent:
        agent_match = re.search(r'\*\*Agent\*\*:\s*(.+)', content, re.IGNORECASE)
        model_match = re.search(r'\*\*Model\*\*:\s*(.+)', content, re.IGNORECASE)
        if agent_match:
            agent = agent_match.group(1).strip()
        elif model_match:
            agent = model_match.group(1).strip()

    # If no date found in YAML, extract from filename
    if not date_str:
        # e.g., log_20260510_174333.md
        filename = os.path.basename(file_path)
        date_match = re.search(r'log_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})', filename)
        if date_match:
            year, month, day, hr, mn, sc = date_match.groups()
            date_str = f"{year}-{month}-{day} {hr}:{mn}:{sc}"
        else:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Normalize agent
    normalized_agent = normalize_agent(agent)
    
    # Extract just the YYYY-MM-DD for the session link
    session_date = date_str.split(" ")[0] if " " in date_str else date_str

    # Build new YAML frontmatter
    new_metadata = {
        "agent": normalized_agent,
        "date": date_str,
        "model": model if model else "unknown",
        "status": status,
        "task_type": task_type
    }
    new_yaml = yaml.dump(new_metadata, default_flow_style=False)

    # Clean up old markdown headers if they existed
    body_content = re.sub(r'# Task Log:?\s*\d*.*?\n+', '', body_content)
    body_content = re.sub(r'\*\*Agent\*\*:.*?\n', '', body_content)
    body_content = re.sub(r'\*\*Model\*\*:.*?\n', '', body_content)
    body_content = body_content.strip()

    # We need to insert Meta Connections before "## Prompt"
    meta_block = f"""# Task Log

## Meta Connections
- Agent: [[{normalized_agent}_MOC]]
- Project: [[Phase_1_and_2_Hardening]]
- Session: [[Session_{session_date}]]

"""
    if "## Prompt" in body_content:
        body_content = body_content.replace("## Prompt", meta_block + "## Prompt", 1)
    else:
        # Fallback if ## Prompt is missing
        body_content = meta_block + body_content

    # Assemble final file
    final_content = f"---\n{new_yaml}---\n\n{body_content}\n"

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    return True


if __name__ == "__main__":
    print("Starting retroactive log linking...")
    log_files = glob.glob(os.path.join(LOGS_DIR, "*.md"))
    
    processed = 0
    skipped = 0
    
    for file_path in log_files:
        if process_log_file(file_path):
            processed += 1
        else:
            skipped += 1
            
    print(f"Complete! Processed: {processed}, Skipped: {skipped}, Total: {len(log_files)}")
