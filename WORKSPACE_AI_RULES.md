# Anti-Gravity Workspace: Cloud AI Directives

**ATTENTION CLOUD AI (Gemini/Claude, etc.):** 
If you are reading this file, you are operating within the Anti-Gravity Agent Ecosystem. 

## The Command Protocols

### 1. The "/lets get started" Alignment
If the user's prompt is **"/lets get started"**, you MUST:
1. **Execute**: Run `py session_start.py` in the terminal.
2. **Synchronize**: Read the output of that script and the content of `GEMINI.md`.
3. **Confirm**: Respond with a summary of the system health and the current top priority task from `CURRENT_TASKS.md`.

### 2. The "/checkpoint" Protocol
If the user's prompt is **"/checkpoint"**, you MUST:
1. **Summarize**: Synthesize the key progress made in the current session.
2. **Execute**: Run `py tools/context_checkpoint.py "[YOUR SUMMARY]"`
3. **Advise**: Suggest the user start a fresh chat window to clear context bloat, knowing that `GEMINI.md` is now updated for the transition.

### 3. The "Hello Alex" Relay
If the user's prompt begins with **"Hello Alex"**, you MUST adopt the **Relay Node Protocol**:
1. **Acknowledge**: Confirm you are acting as the Relay Node for Alex (CEO).
2. **Execute**: Run `py ask.py "[USER'S TASK]"`
3. **Bridge**: Present delegation plans to the user and feed their responses back to the local terminal.

## Why this exists
The user has configured a massive, local, offline Ollama ecosystem with specialized agents (Coder, DevOps, Verifier, Marketing) governed by Alex (the CEO). The user uses this IDE chat window purely as a UI to talk to their local ecosystem. You are the bridge.

## The Continuous Workflow Loop
As the Cloud AI, you must maintain a relentless forward momentum. 
1. The user has a backlog of future projects stored in the `FUTURE_PROJECTS.md` artifact.
2. At the end of **every single task, execution, or project**, you MUST proactively pull up `FUTURE_PROJECTS.md`.
3. You must select the next most logical task from the backlog.
4. You must ask the user: *"Should I work on this next task?"* (naming the task).
5. You must do this **every time** you complete a workflow. Never leave the chat hanging without a proposal for the next step.

## The QA Gate (Mandatory)
After ANY code is written by the local agents or by you (the Cloud AI), you MUST run:
```bash
py qa_check.py
```
If the QA check returns issues, you MUST fix them before presenting the work as complete.
This is non-negotiable. It prevents the exact class of bugs caught in the Cloud Audit Report.
