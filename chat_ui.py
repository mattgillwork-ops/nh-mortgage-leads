#!/usr/bin/env python3
"""
Anti-Gravity Chat UI — FastAPI Backend
Run:  python chat_ui.py
Open: http://localhost:5001
"""

import os
import re
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

try:
    import ollama
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse
    import uvicorn
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    sys.exit(1)

# ── Config ─────────────────────────────────────────────────────────────────────
RELAY_MODEL    = "qwen3:14b"
OLLAMA_HOST    = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
WORKSPACE_ROOT = Path(__file__).parent
STATIC_DIR     = WORKSPACE_ROOT / "chat_static"
PORT           = 5001
HISTORY_LIMIT  = 20
STREAM_TIMEOUT = 120   # seconds; stall warning fires if no token received

STATIC_DIR.mkdir(exist_ok=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def load_file(rel: str, max_chars: int = 4000) -> str:
    try:
        txt = (WORKSPACE_ROOT / rel).read_text(encoding="utf-8", errors="replace")
        return txt[:max_chars] if len(txt) > max_chars else txt
    except Exception as e:
        return f"[Could not load {rel}: {e}]"

def safe_quote(s: str) -> str:
    """Escape double-quotes for use inside a shell string."""
    return s.replace('"', "'")

# ── System Prompt ──────────────────────────────────────────────────────────────
def build_system_prompt() -> str:
    now   = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    rules = load_file("WORKSPACE_AI_RULES.md")
    ctx   = load_file("GEMINI.md", max_chars=3000)
    tasks = load_file("CURRENT_TASKS.md", max_chars=2000)

    return f"""You are the Anti-Gravity Relay — qwen3:14b running locally as the sovereign AI chat interface.
You replace Gemini/Claude entirely. You have full ecosystem awareness.

Current Date/Time: {now}

=== WORKSPACE RULES ===
{rules}

=== SESSION CONTEXT ===
{ctx}

=== CURRENT TASKS ===
{tasks}

---
## ROUTING RULES (MANDATORY)

**RULE 1 — Alex First.**
For ANY non-trivial task, route to Alex by outputting this EXACT format on its own line:
  SHELL_EXEC: docker exec -i anti-sandbox-daemon python ask.py "your detailed prompt"

**RULE 2 — When SHELL_EXEC is required (no exceptions):**
- Research, SEO, keywords, traffic → Rowan + Nova + Finn
- Coding, file edits → Caleb
- QA, audits, security → Atlas or Vera
- Strategy, planning → Finn
- DevOps, infra → Dax
- Running scripts directly → SHELL_EXEC: python <script>

**RULE 3 — Write specific Alex prompts.**
Name the lead agent, deliverable, and output format. Example:
  SHELL_EXEC: docker exec -i anti-sandbox-daemon python ask.py "RESEARCH — Rowan leads. Top 5 high-intent NH mortgage keywords for Manchester/Nashua. Nova: 3 free traffic channels. Finn: 30-day plan with effort/impact."

**RULE 4 — One SHELL_EXEC per response, never more.**

**RULE 5 — Plans need approval.**
For large tasks, outline 2-3 bullets, then ask: "Should I send this to Alex?"

**RULE 6 — Simple scripts run directly.**
  SHELL_EXEC: python scripts/monitor_leads.py --stats
  SHELL_EXEC: python qa_check.py

**RULE 7 — Tone:** concise, markdown-formatted, headers + bullets.

**RULE 8 — Thinking:** your <think> blocks are shown to the user as collapsible reasoning.
"""

# ── Ollama Streaming ───────────────────────────────────────────────────────────
def _ollama_thread(messages: list, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
    try:
        client = ollama.Client(host=OLLAMA_HOST)
        for chunk in client.chat(
            model=RELAY_MODEL,
            messages=messages,
            stream=True,
            options={"num_ctx": 8192, "temperature": 0.4},
        ):
            token = chunk.get("message", {}).get("content", "")
            loop.call_soon_threadsafe(queue.put_nowait, {"token": token})
        loop.call_soon_threadsafe(queue.put_nowait, {"done": True})
    except Exception as e:
        loop.call_soon_threadsafe(queue.put_nowait, {"error": str(e)})


async def stream_to_queue(messages: list) -> asyncio.Queue:
    queue: asyncio.Queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(_ollama_thread, messages, queue, loop)
    return queue


# ── Stream Helpers ─────────────────────────────────────────────────────────────
async def process_stream(ws: WebSocket, messages: list) -> str:
    """
    Stream qwen3:14b response token by token.
    Emits: thinking_start / thinking_token / thinking_end / response_token.
    Returns the clean response (think blocks stripped).
    """
    queue = await stream_to_queue(messages)
    full_raw = ""
    in_think = False

    await ws.send_text(json.dumps({"type": "start"}))

    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=STREAM_TIMEOUT)
        except asyncio.TimeoutError:
            await ws.send_text(json.dumps({
                "type": "stall_warning",
                "content": f"⚠ No tokens for {STREAM_TIMEOUT}s — model may have stalled."
            }))
            break

        if "error" in item:
            await ws.send_text(json.dumps({"type": "error", "content": item["error"]}))
            break

        if "done" in item:
            if in_think:
                await ws.send_text(json.dumps({"type": "thinking_end"}))
            break

        token = item["token"]
        full_raw += token

        # ── Think-block state machine ─────────────────────────────────────
        if "<think>" in token and not in_think:
            in_think = True
            await ws.send_text(json.dumps({"type": "thinking_start"}))
            after = token.split("<think>", 1)[1]
            if "</think>" in after:
                # Whole think block in one token
                think_content, rest = after.split("</think>", 1)
                in_think = False
                if think_content:
                    await ws.send_text(json.dumps({"type": "thinking_token", "content": think_content}))
                await ws.send_text(json.dumps({"type": "thinking_end"}))
                if rest:
                    await ws.send_text(json.dumps({"type": "response_token", "content": rest}))
            elif after:
                await ws.send_text(json.dumps({"type": "thinking_token", "content": after}))
            continue

        if "</think>" in token and in_think:
            in_think = False
            before, rest = token.split("</think>", 1)
            if before:
                await ws.send_text(json.dumps({"type": "thinking_token", "content": before}))
            await ws.send_text(json.dumps({"type": "thinking_end"}))
            if rest:
                await ws.send_text(json.dumps({"type": "response_token", "content": rest}))
            continue

        if in_think:
            if token:
                await ws.send_text(json.dumps({"type": "thinking_token", "content": token}))
        else:
            if token:
                await ws.send_text(json.dumps({"type": "response_token", "content": token}))

    clean = re.sub(r"<think>.*?</think>", "", full_raw, flags=re.DOTALL).strip()
    return clean


async def synthesize(ws: WebSocket, messages: list) -> str:
    """Second-pass synthesis shown after shell output. Returns clean text."""
    queue = await stream_to_queue(messages)
    synth_raw = ""
    in_think = False

    await ws.send_text(json.dumps({"type": "synthesis_start"}))

    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=STREAM_TIMEOUT)
        except asyncio.TimeoutError:
            await ws.send_text(json.dumps({"type": "stall_warning", "content": "⚠ Synthesis timed out."}))
            break

        if "error" in item or "done" in item:
            break

        token = item["token"]
        synth_raw += token

        if "<think>" in token:
            in_think = True
        if "</think>" in token:
            in_think = False
            after = token.split("</think>", 1)[1]
            if after:
                await ws.send_text(json.dumps({"type": "synthesis_token", "content": after}))
            continue
        if not in_think and token:
            await ws.send_text(json.dumps({"type": "synthesis_token", "content": token}))

    return re.sub(r"<think>.*?</think>", "", synth_raw, flags=re.DOTALL).strip()


async def run_shell(ws: WebSocket, cmd: str) -> str:
    """Run a shell command, stream lines to client, return full output."""
    await ws.send_text(json.dumps({"type": "shell_start", "cmd": cmd}))
    lines = []
    success = False
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            cwd=str(WORKSPACE_ROOT),
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        async for raw in proc.stdout:
            line = raw.decode("utf-8", errors="replace").rstrip()
            lines.append(line)
            await ws.send_text(json.dumps({"type": "shell_line", "content": line}))
        await proc.wait()
        success = proc.returncode == 0
    except Exception as e:
        lines.append(f"[ERROR] {e}")

    await ws.send_text(json.dumps({"type": "shell_done", "success": success}))
    output = "\n".join(lines)
    return output[:8000] if len(output) > 8000 else output


# ── Heartbeat ──────────────────────────────────────────────────────────────────
async def heartbeat_loop(ws: WebSocket):
    """Ping client every 3 s so it can detect true disconnects vs. stalls."""
    try:
        while True:
            await asyncio.sleep(3)
            await ws.send_text(json.dumps({"type": "heartbeat", "ts": datetime.now().isoformat()}))
    except Exception:
        pass


# ── Auto-route heuristic ───────────────────────────────────────────────────────
ACTION_KEYWORDS = {
    "research", "build", "create", "run", "analyze", "check",
    "find", "audit", "generate", "write", "implement", "search",
    "investigate", "leads", "seo", "keyword", "traffic", "deploy",
    "launch", "optimize", "fix", "debug",
}

def should_auto_route(user_text: str) -> bool:
    words = set(re.findall(r"\w+", user_text.lower()))
    return bool(words & ACTION_KEYWORDS) and len(user_text.strip()) > 20


# ── FastAPI ────────────────────────────────────────────────────────────────────
app = FastAPI(title="Anti-Gravity Chat")


@app.get("/")
async def root():
    p = STATIC_DIR / "index.html"
    if p.exists():
        return HTMLResponse(p.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Anti-Gravity Chat</h1><p>Missing chat_static/index.html</p>")


@app.get("/health")
async def health():
    return {"status": "ok", "model": RELAY_MODEL, "ollama": OLLAMA_HOST}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    messages = [{"role": "system", "content": build_system_prompt()}]
    hb = asyncio.create_task(heartbeat_loop(ws))

    try:
        while True:
            raw = await ws.receive_text()
            msg = json.loads(raw)
            mtype = msg.get("type", "")

            # ── Direct-to-Alex bypass (toolbar button) ────────────────────
            if mtype == "direct_alex":
                user_text = msg.get("content", "").strip()
                if not user_text:
                    continue
                cmd = f'docker exec -i anti-sandbox-daemon python ask.py "{safe_quote(user_text)}"'
                messages.append({"role": "user", "content": user_text})
                await ws.send_text(json.dumps({"type": "start"}))
                await ws.send_text(json.dumps({"type": "activity", "phase": "relay", "msg": "↗ Routing directly to Alex..."}))
                shell_out = await run_shell(ws, cmd)
                messages.append({"role": "assistant", "content": f"[Direct Alex]\n{shell_out}"})
                await ws.send_text(json.dumps({"type": "done"}))
                continue

            if mtype != "message":
                continue

            user_text = msg.get("content", "").strip()
            if not user_text:
                continue

            messages.append({"role": "user", "content": user_text})

            # ── Phase 1: qwen3 reasons & responds ─────────────────────────
            await ws.send_text(json.dumps({"type": "activity", "phase": "thinking", "msg": "🧠 qwen3:14b thinking..."}))
            clean = await process_stream(ws, messages)
            messages.append({"role": "assistant", "content": clean})

            # ── Phase 2: Detect SHELL_EXEC ─────────────────────────────────
            m = re.search(r"SHELL_EXEC:\s*(.+)", clean, re.IGNORECASE)
            shell_cmd = m.group(1).strip().strip('`"\'') if m else None

            # ── Phase 2b: Auto-route if model forgot ──────────────────────
            if not shell_cmd and should_auto_route(user_text):
                await ws.send_text(json.dumps({
                    "type": "activity",
                    "phase": "auto_relay",
                    "msg": "⚡ Auto-routing to Alex (action detected)..."
                }))
                shell_cmd = f'docker exec -i anti-sandbox-daemon python ask.py "{safe_quote(user_text)}"'

            # ── Phase 3: Run shell + synthesize ───────────────────────────
            if shell_cmd:
                await ws.send_text(json.dumps({"type": "activity", "phase": "shell", "msg": "🔧 Executing command..."}))
                shell_out = await run_shell(ws, shell_cmd)

                messages.append({
                    "role": "user",
                    "content": f"[SHELL RESULT]\n{shell_out}\n\nSummarize the key findings and suggest next steps."
                })
                await ws.send_text(json.dumps({"type": "activity", "phase": "synthesis", "msg": "📋 Synthesizing results..."}))
                synth = await synthesize(ws, messages)
                messages.append({"role": "assistant", "content": synth})

            await ws.send_text(json.dumps({"type": "done"}))

            # Trim history window
            if len(messages) > HISTORY_LIMIT + 1:
                messages = [messages[0]] + messages[-HISTORY_LIMIT:]

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await ws.send_text(json.dumps({"type": "error", "content": str(e)}))
        except Exception:
            pass
    finally:
        hb.cancel()


# ── Entry ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*55}")
    print("  Anti-Gravity Chat UI")
    print(f"  Model : {RELAY_MODEL}")
    print(f"  URL   : http://localhost:{PORT}")
    print(f"{'='*55}\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
