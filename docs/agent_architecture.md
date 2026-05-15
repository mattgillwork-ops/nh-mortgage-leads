# Antigravity Multi-Agent System: Architectural Specification v3.0

## 1. System Overview
Antigravity is a sovereign, multi-agent business engine designed for autonomous lead generation, research, and technical development. The system is decoupled from third-party cloud dependencies, utilizing local LLMs via Ollama, containerized execution via Docker, and a persistent memory architecture mapped to an Obsidian Vault.

## 2. Architecture Diagram (Conceptual)
```text
[ USER ] <---> [ Fast Router (7B) ]
                     |
            [ Alex (CEO - 14B) ] <---> [ Deep Thinker (33B/14B) ]
                     |                         |
    +----------------+-------------------------+----------------+
    |                |                         |                |
[ Caleb ]        [ Dax ]                   [ Rowan ]        [ Atlas ]
(Coder)          (DevOps)                 (Researcher)     (Analyst)
    |                |                         |                |
    +----------------+------------+------------+----------------+
                                  |
                        [ Obsidian Vault ]
                        (LTM / Context / Logs)
```

## 3. Docker Service Map
| Service | Role | Network/Port | Persistence |
|---------|------|--------------|-------------|
| `ollama-local` | LLM Inference Engine | `11434` | `/root/.ollama` |
| `agent-sandbox` | Safe code execution environment | Isolated | `/tmp/sandbox` |
| `browser-node` | Playwright/Headless Browser | Internals | `/screenshots` |

## 4. MCP Tool Map
| Tool Name | Owner | Function |
|-----------|-------|----------|
| `web_search` | Rowan | DuckDuckGo search (privacy-first) |
| `file_manager` | Dax / Caleb | Secure read/write in workspace |
| `browser_interact` | Atlas | Headless browser navigation |
| `resend_dispatch` | Alex | Lead email notifications |

## 5. Final Agent Roster & Model Assignments
| Agent | Role | Primary Model | Fallback Model |
|-------|------|---------------|----------------|
| **Fast Router** | Classification | `qwen2.5:7b` | `qwen3:8b` |
| **Alex** | CEO / Orchestrator | `qwen3:14b` | `qwen2.5:14b` |
| **Deep Thinker** | Architect / Reasoning | `deepseek-r1:14b` | `qwen3:14b` |
| **Caleb** | Coder (Next.js/React) | `qwen2.5-coder:14b` | `qwen2.5-coder:7b` |
| **Dax** | DevOps / Security | `qwen2.5-coder:14b` | `qwen2.5-coder:7b` |
| **Rowan** | Researcher / SEO | `qwen3:14b` | `qwen2.5:14b` |
| **Atlas** | Security Analyst | `deepseek-r1:14b` | `qwen3:14b` |
| **Vera** | QA / Verifier | `deepseek-r1:14b` | `qwen3:14b` |
| **Aria** | UX / UI Design | `qwen2.5vl:latest` | `llama3.2-vision:latest` |
| **Nova** | Marketing / Growth | `qwen3:14b` | `qwen2.5:14b` |
| **Finn** | Brainstorming | `qwen3:14b` | `qwen2.5:14b` |

## 6. Agent Skill Sets
*   **Alex**: Goal decomposition, task delegation, synthesis.
*   **Deep Thinker**: Architectural risk assessment, complex logic.
*   **Caleb**: Typescript, Next.js, Clean Code, API integration.
*   **Dax**: Docker, CI/CD, Git persistence, firewall rules.
*   **Rowan**: Market analysis, SEO auditing, content strategy.

## 7. Fallback Behavior
1. **Tier 1 (Local Primary)**: Default execution on primary model.
2. **Tier 2 (Local Fallback)**: If primary returns null or error, switch to local fallback.
3. **Tier 3 (Cloud Fallback)**: **DISABLED**. System will halt and request user intervention if local models are exhausted.

## 8. Memory Governance Rules
- **Episodic Isolation**: Agents only see context relevant to their current sub-task.
- **Truth Anchoring**: All factual updates must be cross-referenced against the `Knowledge_Graph`.
- **Approval Gate**: Alex cannot write to Long-Term Memory (LTM) without Vera's verification or User approval.

## 9. Obsidian Vault Memory Schema
- `tru/Core_Rules/`: System directives and Modelfiles.
- `tru/Memory_Logs/`: Daily episodic task logs (JSON + Markdown).
- `tru/Knowledge_Graph/`: Persistent structured data (Mortgage rates, etc.).
- `tru/Projects/`: Individual project MOCs (Maps of Content).

## 10. Long-Term Memory Approval Flow
1. Agent proposes update in `tru/Proposals/`.
2. **Vera (QA)** audits for logic/formatting consistency.
3. **Alex (CEO)** reviews Vera's report.
4. User receives `[Y/N]` prompt for final commit to LTM.

## 11. Routing Rules
- All user input enters via **Fast Router**.
- Fast Router delegates to **Alex** for planning.
- Alex delegates sub-tasks to Specialists.
- Specialists return results to Alex for synthesis.

## 12. Troubleshooting
- **Ollama Offline**: Check service status: `ollama list`. Restart with `ollama serve`.
- **Model Missing**: Run `ollama pull [model_name]`.
- **Docker Failure**: Run `docker ps -a` to identify crashed nodes.

## 13. How to Add a New Agent
1. Create `agents/[name]_agent.py` inheriting from `BaseAgent`.
2. Create `Modelfile.[name]` in project root.
3. Add agent definition to `agent_registry.yaml`.
4. Run `ollama create anti-[name] -f Modelfile.[name]`.

## 14. How to Avoid Memory Contamination
- Use unique `task_id` for every sub-task.
- Ensure `BaseAgent.clear_context()` is called between unrelated goals.
- Audit `tru/Memory_Logs/` for hallucinated patterns.
