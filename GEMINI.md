# Anti-Gravity AI Ecosystem — Session Handoff

**Read this file first when resuming work.**

## What This Project Is
A multi-agent AI ecosystem running locally on Ollama (14B models) with an Obsidian vault (`tru/`) as the source of truth. Managed by a CEO agent (Alex) who delegates to specialized agents.

## The Agent Squad
| Agent | Role | Model |
|-------|------|-------|
| Alex | CEO/Orchestrator | `anti-ceo` |
| Caleb | Coder (React/Next.js) | `anti-coder` |
| Aria | UX/Design | `anti-ux` |
| Dax | DevOps/Docker | `anti-devops` |
| Nova | Marketing/SEO | `anti-marketing` |
| Rowan | Researcher | `anti-researcher` |
| Atlas | Security Analyst | `anti-analyst` |
| Vera | QA/Verifier | `anti-verifier` |
| Finn | Brainstormer/Strategy | `anti-brainstormer` |

## Current Phase: Intelligence & Growth Initiation (ACTIVE)
Infrastructure hardening and sovereign routing protocols completed (2026-05-12). All agents now utilize a 3-layer fallback hierarchy (Specialist -> Powerhouse -> Cloud Gate).

## Key Architecture Details
- **Entry point**: `ask.py` → routes to Alex (CEO) → delegates to sub-agents
- **Sovereign Routing**: 3-Layer local fallback (Specialist -> gemma2:27b -> Gemini).
- **Interactive Gate**: Cloud fallback requires explicit user `[Y/N]` approval to prevent data leakage.
- **Reflection Engine**: Automated `drift_report.md` generation on model failure.
- **Memory**: ChromaDB + Obsidian rules-first ingestion (`tru/Core_Rules/MEMORY_PROTOCOL.md`).

## What's Next (Priority Order)
1. **SEO Competitive Audits** — Atlas to crawl competitor sites and identify content gaps.
2. **Agency Landing Page** — Caleb and Aria to build the Anti-Gravity agency presence.
3. **Internal Intelligence Graph** — Link audit data back to the project vault.

## User Preferences
- Infrastructure and hardening BEFORE business features
- Use DuckDuckGo for search (privacy, no rate limits)
- No hardcoded credentials — use environment variables
- Obsidian vault (`tru/`) is the permanent source of truth
- Git auto-commit only when it adds value (file-writing agents, not research)
- Free tools preferred; **Email is currently out of scope (decommissioned)**.


## Important Files
- `WORKSPACE_AI_RULES.md` — Cloud AI directives (Hello Alex protocol)
- `tru/Core_Rules/AGENTS.md` — Agent roles and routing rules
- `CURRENT_TASKS.md` — Active task tracker
- `FUTURE_PROJECTS.md` — Approved project queue
- `POSSIBLE_PROJECTS.md` — Brainstorm/research ideas (Finn + Rowan)
- `selfcheck.py` — System diagnostic suite
- `heartbeat_daemon.py` — Autonomous background audit loop

## Known Issues
- `GEMINI_API_KEY` not set — cloud fallback disabled
- npm not in PATH (frontend builds need manual path setup)
- Git not in system PATH — `git_manager.py` uses absolute path fallback to `C:\Program Files\Git\bin\git.exe`
