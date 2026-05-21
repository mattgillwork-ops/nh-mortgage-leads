#!/usr/bin/env python3
"""
Anti-Gravity Relay Shell — qwen3:14b Edition
=============================================
Replaces the Antigravity Cloud AI chat layer with a fully local,
sovereign terminal powered by qwen3:14b via Ollama.

qwen3:14b reads workspace rules and session context, then decides
when to route tasks to Alex via:
    docker exec -i anti-sandbox-daemon python ask.py "..."

Usage:
    python relay.py
"""

import os
import sys
import io
import re
import subprocess
from datetime import datetime

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import ollama
except ImportError:
    print("[ERROR] ollama package not installed. Run: pip install ollama")
    sys.exit(1)

# ─── Configuration ────────────────────────────────────────────────────────────

RELAY_MODEL   = "qwen3:14b"
OLLAMA_HOST   = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
WORKSPACE_ROOT = os.path.dirname(os.path.abspath(__file__))
HISTORY_LIMIT  = 24   # max turns before trimming (keeps system prompt always)

# ─── ANSI Colors ──────────────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    MAGENTA = "\033[95m"
    RED     = "\033[91m"
    DIM     = "\033[2m"

# ─── File Helpers ─────────────────────────────────────────────────────────────

def load_file(rel_path: str, max_chars: int = 4000) -> str:
    try:
        full = os.path.join(WORKSPACE_ROOT, rel_path)
        with open(full, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return content[:max_chars] if len(content) > max_chars else content
    except Exception as e:
        return f"[Could not load {rel_path}: {e}]"

# ─── System Prompt ────────────────────────────────────────────────────────────

def build_system_prompt() -> str:
    current_date = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    rules        = load_file("WORKSPACE_AI_RULES.md")
    session      = load_file("GEMINI.md", max_chars=3000)
    tasks        = load_file("CURRENT_TASKS.md", max_chars=2000)

    return f"""You are the Anti-Gravity Relay — a locally-running qwen3:14b instance that replaces the cloud AI chat interface for this workspace.
You have full awareness of the ecosystem and act as the sovereign relay node between the user and Alex (CEO + the Ollama agent squad).

Current Date/Time: {current_date}

=== WORKSPACE_AI_RULES.md ===
{rules}

=== SESSION CONTEXT (GEMINI.md) ===
{session}

=== CURRENT TASKS ===
{tasks}

---

## YOUR OPERATING RULES

1. **Relay Node**: Your primary job is to understand user intent and route it to Alex via `ask.py`.
   When you decide a task must go to Alex, output:
   SHELL_EXEC: docker exec -i anti-sandbox-daemon python ask.py "your well-crafted prompt here"

2. **Alex First Protocol**: ALL non-trivial tasks MUST go through Alex. You do NOT solve tasks yourself.

3. **Craft good prompts**: When routing to Alex, write a specific, well-structured prompt — name which agents should lead (Rowan=SEO/research, Nova=marketing, Finn=strategy, Caleb=code, etc.).

4. **Plans before execution**: If a task requires a plan, present it to the user and WAIT for their approval before routing to Alex.

5. **Research tasks**: For research requests, craft a structured brief specifying: what to research, which agents lead, what the deliverable format should be.

6. **Shell commands**: You may also run direct shell commands when appropriate:
   SHELL_EXEC: python scripts/monitor_leads.py --stats
   SHELL_EXEC: python qa_check.py

7. **One SHELL_EXEC at a time**: Only output ONE SHELL_EXEC per response. Wait for the result.

8. **/checkpoint**: Summarize the session and run:
   SHELL_EXEC: python tools/context_checkpoint.py "your summary"

9. **Tone**: Concise, direct, technical. No fluff. You are a power tool.

10. **Thinking**: You have extended reasoning capability. Use <think> tags internally but strip them from your final response to the user.
"""

# ─── Shell Executor ───────────────────────────────────────────────────────────

def run_shell(cmd: str, timeout: int = 300) -> str:
    print(f"\n{C.YELLOW}[RELAY SHELL]{C.RESET} {C.DIM}{cmd}{C.RESET}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=WORKSPACE_ROOT,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
        )
        out = result.stdout.strip()
        err = result.stderr.strip()
        if out and err and result.returncode != 0:
            return f"{out}\n[STDERR] {err}"
        return out or err or "(No output)"
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] Command exceeded time limit and was killed."
    except Exception as e:
        return f"[ERROR] {e}"

# ─── Ollama Chat ──────────────────────────────────────────────────────────────

def chat(messages: list) -> str:
    """Call qwen3:14b via Ollama. Streams tokens to console, returns full text."""
    client = ollama.Client(host=OLLAMA_HOST)

    print(f"\n{C.MAGENTA}[Anti-Gravity Relay]{C.RESET} ", end="", flush=True)

    full_response = ""
    in_think_block = False

    try:
        stream = client.chat(
            model=RELAY_MODEL,
            messages=messages,
            stream=True,
            options={
                "num_ctx": 8192,
                "temperature": 0.4,
            }
        )

        for chunk in stream:
            token = chunk.get("message", {}).get("content", "")
            full_response += token

            # Handle qwen3 <think> blocks — dim them in console
            if "<think>" in token:
                in_think_block = True
            if in_think_block:
                # Print thinking in dim grey so user can see reasoning but it's subtle
                print(f"{C.DIM}{token}{C.RESET}", end="", flush=True)
            else:
                print(token, end="", flush=True)
            if "</think>" in token:
                in_think_block = False

        print()  # newline after stream completes

    except Exception as e:
        print(f"\n{C.RED}[ERROR] Ollama call failed: {e}{C.RESET}")
        return f"ERROR: {e}"

    # Strip <think>...</think> blocks from the returned text
    clean = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()
    return clean

# ─── Response Handler ─────────────────────────────────────────────────────────

def handle_response(response: str, messages: list) -> str:
    """Detect SHELL_EXEC directives, run them, inject results back."""
    exec_match = re.search(r'SHELL_EXEC:\s*(.+)', response, re.IGNORECASE)
    if not exec_match:
        return response

    cmd = exec_match.group(1).strip().strip('`').strip('"')
    shell_output = run_shell(cmd)

    # Truncate very long outputs (e.g. ask.py can produce huge responses)
    if len(shell_output) > 6000:
        shell_output = shell_output[:6000] + "\n\n[...output truncated for context...]"

    print(f"\n{C.DIM}--- Shell Output ---{C.RESET}")
    print(shell_output)
    print(f"{C.DIM}--- End Shell Output ---{C.RESET}\n")

    # Inject result for model to synthesize
    messages.append({
        "role": "user",
        "content": f"[SHELL RESULT for: {cmd}]\n{shell_output}\n\nPlease summarize the key findings for the user and suggest next steps."
    })
    synthesis = chat(messages)
    messages.append({"role": "assistant", "content": synthesis})
    return synthesis

# ─── Banner ───────────────────────────────────────────────────────────────────

def print_banner():
    print(f"\n{C.CYAN}{C.BOLD}")
    print("=" * 66)
    print("  ANTI-GRAVITY RELAY SHELL")
    print(f"  Model: {RELAY_MODEL} (local Ollama)")
    print("  Alex (CEO) + Full Squad: UNCHANGED")
    print("  This shell IS the Antigravity relay layer.")
    print("=" * 66)
    print(f"{C.RESET}")
    print(f"Type your request. {C.DIM}qwen3:14b will relay to Alex when needed.{C.RESET}")
    print(f"Type {C.YELLOW}'exit'{C.RESET} or Ctrl+C to quit.\n")

# ─── Main Loop ────────────────────────────────────────────────────────────────

def main():
    print_banner()

    # Verify model is available
    try:
        client = ollama.Client(host=OLLAMA_HOST)
        available = [m.model for m in client.list().models]
        if not any(RELAY_MODEL in m for m in available):
            print(f"{C.RED}[ERROR] {RELAY_MODEL} not found in Ollama. Run: ollama pull {RELAY_MODEL}{C.RESET}")
            sys.exit(1)
        print(f"{C.GREEN}[OK]{C.RESET} {RELAY_MODEL} confirmed online at {OLLAMA_HOST}\n")
    except Exception as e:
        print(f"{C.RED}[ERROR] Cannot reach Ollama at {OLLAMA_HOST}: {e}{C.RESET}")
        sys.exit(1)

    system_prompt = build_system_prompt()
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            user_input = input(f"{C.GREEN}You > {C.RESET}").strip()

            if not user_input:
                continue

            if user_input.lower() in ('exit', 'quit', 'q'):
                print("Relay shell offline. Alex and the squad remain active.")
                break

            # Add user turn
            messages.append({"role": "user", "content": user_input})

            # qwen3:14b reasons and responds
            response = chat(messages)
            messages.append({"role": "assistant", "content": response})

            # If model issued a shell command, execute it
            if "SHELL_EXEC:" in response:
                handle_response(response, messages)

            print(f"\n{C.DIM}" + "─" * 66 + f"{C.RESET}\n")

            # Trim history to prevent context overflow
            if len(messages) > HISTORY_LIMIT + 1:
                messages = [messages[0]] + messages[-(HISTORY_LIMIT):]

        except KeyboardInterrupt:
            print(f"\n{C.CYAN}Relay shell offline.{C.RESET}")
            break
        except Exception as e:
            print(f"{C.RED}[ERROR] {e}{C.RESET}")


if __name__ == "__main__":
    main()
