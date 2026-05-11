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

## Current Phase: Infrastructure Hardening (COMPLETE)
All 5 phases done. Git commit `7a7fa88` is the baseline.
1. ✅ Heartbeat Daemon — `sys.executable`, crash guard, Ollama pre-flight
2. ✅ Knowledge Manager — relevance-based pruning (not date-based), `--dry-run` mode
3. ✅ Web Search — DuckDuckGo primary, Google fallback, robots.txt check
4. ✅ New Tools — `tools/file_manager.py`, `tools/env_checker.py`
5. ✅ Git Safety Net — auto-commit in `ceo_agent.py` on verified file-write tasks only

## Key Architecture Details
- **Entry point**: `ask.py` → routes to Alex (CEO) → delegates to sub-agents
- **Resilience**: 3 retries + Gemini cloud fallback (needs `GEMINI_API_KEY` in `.env`)
- **Memory**: ChromaDB vector DB + Obsidian markdown logs in `tru/Memory_Logs/`
- **Security**: Path validation, core file protection, shrinkage monitor, `shlex` command quoting
- **Reflexion Loop**: Agents self-heal on tool errors (observe → reflect → fix)
- **Dashboard**: FastAPI backend at `localhost:8000`, Docker container `antigravity-dashboard`

## What's Next (Priority Order)
1. **Agency Operations** — Build the Anti-Gravity agency landing page (Caleb + Aria)
2. **SEO Automation** — Integrate Playwright for Rowan's competitive audits
3. **Email Pipeline** — Mailtrap integration for Nova's outreach (human-in-the-loop)

## User Preferences
- Infrastructure and hardening BEFORE business features
- Use DuckDuckGo for search (privacy, no rate limits)
- No hardcoded credentials — use environment variables
- Obsidian vault (`tru/`) is the permanent source of truth
- Git auto-commit only when it adds value (file-writing agents, not research)
- Free tools preferred; avoid Google/Outlook for email (risk of AI account bans)

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
