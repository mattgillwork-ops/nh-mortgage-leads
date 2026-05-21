#!/usr/bin/env python3
"""
Anti-Gravity GPT Shell
======================
Replaces the Antigravity Cloud AI chat layer with a local terminal session
powered by OpenAI GPT-4o as the routing brain.

GPT-4o reads the workspace rules, then decides what to relay to Alex
via `docker exec -i anti-sandbox-daemon python ask.py "..."`.

Usage:
    python gpt_shell.py
"""

import os
import sys
import io
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    print("[ERROR] openai package not installed. Run: pip install openai")
    sys.exit(1)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("[ERROR] OPENAI_API_KEY is not set in .env")
    sys.exit(1)

client = OpenAI(api_key=API_KEY)
MODEL = "gpt-4o"

WORKSPACE_ROOT = os.path.dirname(os.path.abspath(__file__))


def load_file(path: str) -> str:
    """Load a file relative to the workspace root."""
    try:
        full = os.path.join(WORKSPACE_ROOT, path)
        with open(full, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        return f"[Could not load {path}: {e}]"


def load_gemini_md() -> str:
    return load_file("GEMINI.md")


def load_workspace_rules() -> str:
    return load_file("WORKSPACE_AI_RULES.md")


def load_current_tasks() -> str:
    return load_file("CURRENT_TASKS.md")


def build_system_prompt() -> str:
    rules = load_workspace_rules()
    gemini = load_gemini_md()
    tasks = load_current_tasks()
    current_date = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")

    return f"""You are the Anti-Gravity AI Shell — a GPT-4o-powered relay that replaces the cloud AI chat interface.
You operate according to the workspace rules below and have full awareness of the ecosystem.

Current Date/Time: {current_date}

=== WORKSPACE_AI_RULES.md ===
{rules}

=== GEMINI.md (Session Context) ===
{gemini}

=== CURRENT_TASKS.md ===
{tasks}

---

## Your Core Behavior

1. **You are a RELAY NODE.** Your primary job is to understand the user's intent and route it to Alex via:
   `docker exec -i anti-sandbox-daemon python ask.py "..."`
   You do NOT solve tasks yourself unless they are trivial clarifications.

2. **Alex First Protocol:** EVERY task goes to Alex first via ask.py. No exceptions.

3. **Research tasks:** When the user asks to research something, craft a precise, structured research prompt before sending it to ask.py. Be specific — name which agents should lead (Rowan for SEO/keywords, Nova for marketing, Finn for strategy synthesis).

4. **Tool usage:** When you decide to run a command, output it clearly in this format:
   ```
   SHELL_EXEC: <the full command>
   ```
   The shell will execute it and show you the output.

5. **Plans:** When a task requires a plan before execution, present the plan to the user and wait for their explicit approval before sending to ask.py.

6. **Checkpoint:** If the user says `/checkpoint`, summarize the session and run `python tools/context_checkpoint.py "..."`.

7. **Tone:** Be concise, direct, and technical. No fluff. You are a power tool for a developer.
"""


def run_shell_command(cmd: str) -> str:
    """Execute a shell command and capture output."""
    print(f"\n\033[93m[SHELL] Executing: {cmd}\033[0m")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=WORKSPACE_ROOT,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
        )
        output = result.stdout.strip() if result.stdout else ""
        if result.stderr and result.returncode != 0:
            output += f"\n[STDERR] {result.stderr.strip()}"
        return output if output else "(Command ran with no output.)"
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] Command took too long and was killed."
    except Exception as e:
        return f"[ERROR] Failed to run command: {e}"


def parse_and_execute(response: str, messages: list) -> str:
    """
    Scans GPT-4o's response for SHELL_EXEC directives,
    runs them, and injects the output back as a tool result.
    """
    import re
    exec_pattern = re.compile(r'SHELL_EXEC:\s*(.+)', re.IGNORECASE)
    matches = exec_pattern.findall(response)

    if not matches:
        return response

    augmented = response
    for cmd in matches:
        cmd = cmd.strip().strip('`').strip('"')
        output = run_shell_command(cmd)
        augmented += f"\n\n[SHELL OUTPUT for `{cmd}`]:\n{output}"
        # Inject shell output so GPT-4o can reason about it on next turn
        messages.append({
            "role": "user",
            "content": f"[SYSTEM] Shell command completed. Output:\n{output}\n\nPlease summarize the result for the user."
        })
        # Get GPT-4o to synthesize the output
        synthesis = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3,
            max_tokens=1500
        )
        synthesis_text = synthesis.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": synthesis_text})
        augmented += f"\n\n[GPT-4o SYNTHESIS]\n{synthesis_text}"

    return augmented


def gpt_think(messages: list) -> str:
    """Call GPT-4o with the current conversation history."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.4,
        max_tokens=2000
    )
    return response.choices[0].message.content.strip()


def print_banner():
    print("\033[96m")
    print("=" * 66)
    print("  ANTI-GRAVITY GPT SHELL")
    print(f"  Powered by: OpenAI {MODEL}")
    print("  Alex (CEO) + Full Ollama Squad remain unchanged.")
    print("  This shell replaces the Antigravity Cloud AI relay layer.")
    print("=" * 66)
    print("\033[0m")
    print("Type your request. Alex will be notified automatically.")
    print("Type 'exit' or Ctrl+C to quit.\n")


def main():
    print_banner()

    system_prompt = build_system_prompt()
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            user_input = input("\033[92mYou > \033[0m").strip()

            if not user_input:
                continue

            if user_input.lower() in ('exit', 'quit', 'q'):
                print("Shutting down GPT Shell. Alex and the squad remain online.")
                break

            # Add user message
            messages.append({"role": "user", "content": user_input})

            # GPT-4o thinks and decides what to do
            print(f"\n\033[94m[GPT-4o] Processing...\033[0m")
            response = gpt_think(messages)

            # Add to history
            messages.append({"role": "assistant", "content": response})

            # Check if GPT-4o decided to run a command
            if "SHELL_EXEC:" in response:
                response = parse_and_execute(response, messages)

            # Display the response
            print(f"\n\033[95m[Anti-Gravity]\033[0m {response}\n")
            print("-" * 66)

            # Keep context manageable — trim old messages if over 30 turns
            if len(messages) > 32:
                # Always keep system prompt + last 20 messages
                messages = [messages[0]] + messages[-20:]

        except KeyboardInterrupt:
            print("\n\nShutting down GPT Shell.")
            break
        except Exception as e:
            print(f"\033[91m[ERROR] {e}\033[0m")


if __name__ == "__main__":
    main()
