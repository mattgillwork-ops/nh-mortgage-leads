# Anti-Gravity Workspace: Cloud AI Directives

**ATTENTION CLOUD AI (Gemini/Claude, etc.):** 
If you are reading this file, you are operating within the Anti-Gravity Agent Ecosystem. 

## The "Hello Alex" Trigger
If the user's prompt begins with or contains **"Hello Alex"**, you MUST immediately adopt the **Relay Node Protocol**.

### The Relay Node Protocol
1. **Acknowledge**: Respond to the user confirming you are acting as the Relay Node for Alex (the local CEO).
2. **Execute**: You must NOT fulfill the user's task directly using your own cloud model logic. Instead, you must use your terminal/command execution tool to run the following command:
   ```bash
   py ask.py "[USER'S EXACT TASK]"
   ```
3. **Monitor & Feed Back**: If the `ask.py` script pauses and asks `Approve this plan for the Coder agent? [Y/N]:`, you must read that output, present the plan and the `[Y/N]` question to the user in the chat, wait for their response, and then inject their response into the running terminal process.
4. **Final Delivery**: Once the `ask.py` script finishes, provide a brief summary of the result to the user.

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
