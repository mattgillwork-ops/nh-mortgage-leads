import os
import glob
import json
import logging
import subprocess
import yaml

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "tru", "Memory_Logs")
REPAIR_LOG = os.path.join(BASE_DIR, "repair_actions.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [REPAIR] %(message)s',
    handlers=[
        logging.FileHandler(REPAIR_LOG),
        logging.StreamHandler()
    ]
)

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=BASE_DIR)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def repair_heartbeat():
    logging.info("Attempting to restart Heartbeat Daemon...")
    code, out, err = run_cmd("tasklist /FI \"IMAGENAME eq python.exe\" /V | findstr /i \"heartbeat\"")
    if code == 0 and out.strip():
        logging.info("Heartbeat Daemon appears to be running. Skipping restart.")
        return True
    
    code, out, err = run_cmd("start-process python -ArgumentList \"heartbeat_daemon.py\" -NoNewWindow")
    if code == 0:
        logging.info("Heartbeat Daemon restart command sent.")
        return True
    else:
        logging.error(f"Failed to restart Heartbeat: {err}")
        return False

def repair_model_registry(agent_id, model_name):
    logging.info(f"Syncing registry for {agent_id} to {model_name}...")
    registry_path = os.path.join(BASE_DIR, "agent_registry.yaml")
    if not os.path.exists(registry_path):
        return False
    
    with open(registry_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    if agent_id in config.get('agents', {}):
        config['agents'][agent_id]['model']['primary'] = model_name
        with open(registry_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
        logging.info(f"Registry updated for {agent_id}.")
        return True
    return False

def analyze_logs():
    logging.info(f"Scanning {LOG_DIR} for failures (depth: 50)...")
    log_files = glob.glob(os.path.join(LOG_DIR, "*.md"))
    if not log_files:
        return
    
    log_files.sort(key=os.path.getmtime, reverse=True)
    
    # Critical Patterns
    patterns = {
        "heartbeat down": repair_heartbeat,
        "heartbeat missing": repair_heartbeat,
        "model not found": lambda: logging.warning("Manual model pull required for missing model detected in logs."),
        "unauthorized tool": lambda: logging.warning("Security alert: Unauthorized tool call detected. Review agent permissions."),
        "registry mismatch": lambda: logging.warning("Registry mismatch detected. Check agent_registry.yaml vs model_registry.yaml.")
    }
    
    for log_file in log_files[:50]:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            for pattern, action in patterns.items():
                if pattern in content:
                    filename = os.path.basename(log_file)
                    logging.warning(f"Pattern '{pattern}' detected in {filename}. Executing repair action...")
                    action()
        except Exception as e:
            logging.error(f"Error scanning {log_file}: {e}")

if __name__ == "__main__":
    analyze_logs()
