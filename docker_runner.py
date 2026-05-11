"""
Anti-Gravity Docker Execution Engine
====================================
Provides an isolated Docker environment for executing AI-generated 
code and shell commands. Prevents OS corruption.
"""

import os
import subprocess
import logging
import shlex

logger = logging.getLogger("DockerRunner")

def execute_in_sandbox(command: str, workspace_path: str = None) -> str:
    """
    Executes a shell command inside the `anti-sandbox` Docker container.
    Mounts the workspace_path into the container so the AI can edit project files,
    but physically prevents access to the host OS (C: drive).
    
    Returns the stdout/stderr of the command.
    """
    if workspace_path is None:
        # Default to the root of the Anti-Gravity project
        workspace_path = os.path.dirname(os.path.abspath(__file__))

    # Validate workspace path is absolute
    workspace_path = os.path.abspath(workspace_path)
    
    logger.info(f"Executing command in Docker Sandbox: {command[:50]}...")
    
    try:
        # Strip CRLF (\r) to prevent bash errors
        command = command.replace('\r', '')
        
        # Security: Basic check for nested shell escapes or suspicious characters
        # But since we use bash -c, we must allow certain shell characters.
        # We will log the command for auditing.
        
        container_name = "anti-sandbox-daemon"
        
        # Check if daemon is running
        check_cmd = ["docker", "ps", "-q", "-f", f"name={container_name}"]
        check_result = subprocess.run(check_cmd, capture_output=True, text=True)
        
        if not check_result.stdout.strip():
            logger.info(f"Starting persistent daemon: {container_name}")
            # Start the daemon
            start_cmd = [
                "docker", "run", "-d", "--rm", "--name", container_name,
                "-v", f"{workspace_path}:/workspace",
                "-w", "/workspace",
                "anti-sandbox",
                "tail", "-f", "/dev/null"
            ]
            subprocess.run(start_cmd, capture_output=True, check=True)
        
        # Execute the command inside the persistent daemon
        # We use a list to avoid host-side shell injection.
        docker_cmd = [
            "docker", "exec", container_name,
            "/bin/bash", "-c", command
        ]
        
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout for safety
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
            
        return output.strip() if output.strip() else "[Command executed successfully with no output]"

    except subprocess.TimeoutExpired:
        return "[ERROR] Command timed out after 120 seconds."
    except Exception as e:
        return f"[ERROR] Failed to execute in Docker: {str(e)}"

if __name__ == "__main__":
    # Simple test
    print("Testing Docker Sandbox...")
    print(execute_in_sandbox("echo 'Hello from inside the sandbox!' && pwd"))
