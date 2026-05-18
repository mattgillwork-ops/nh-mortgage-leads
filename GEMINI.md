# Anti-Gravity AI Ecosystem — Session Handoff

**Read this file first when resuming work.**

## Last Checkpoint: 2026-05-18 13:56:00
**Summary**: Session: Full ecosystem re-alignment. Ran session_start.py and selfcheck.py diagnostics (48/50 pass, 2 intentional sovereign-mode flags). Archived 472 stale memory logs (672→200, back under 500 threshold). Launched mortgage-app Next.js dev server and performed full 6-step lead funnel E2E walkthrough — all steps, validation, API submission, and Wealth Intelligence Report render verified. Fixed SEO metadata in layout.tsx (was default 'Create Next App'). Fixed markdown rendering bug in LeadFunnel.tsx Positive Pivot section. System fully operational.

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

## Current Status
### Active Tasks
- `[x]` **Phase 1: System Foundation & Autonomy**
  - `[x]` Upgrade `BaseAgent` with **Reflexion Logic** (Self-Healing loop).
  - `[x]` Deploy `heartbeat_daemon.py` and initiate autonomous pulse.
  - `[x]` Rename and rebuild the squad (Caleb, Nova, Atlas, etc.) in Ollama.
  - `[x]` Implement `knowledge_manager.py` for `Learnings.md` maintenance.

- `[x]` **Phase 2: Sovereign Infrastructure Hardening (COMPLETE & VERIFIED)**
  - `[x]` **Lean Squad Restructure**: Consolidated 9 agents into high-impact 6-agent hierarchy (now expanded to 11).
  - `[x]` **Infrastructure Purge**: Decommissioned experimental email/Cloudflare bridge.
  - `[x]` **Core Alignment**: Restored Cloud Gate, Whitelist Firewall, and v3 Startup/Checkpoint protocols.


- `[x]` **Project: NH Mortgage Lead Gen (PRIMARY FOCUS)**
  - `[x]` **Research (Phase 1)**: Initial keyword analysis for NH Mortgage market (Rowan).
  - `[x]` **Design Foundation (Phase 1)**: Build premium Next.js Design System & Hero (Aria & Caleb).
  - `[x]` **Development (Phase 2)**: Build the multi-step lead capture engine with 'Positive Pivot' UX logic (Caleb & Aria).
  - `[x]` **Verification (Phase 3)**: Full E2E funnel walkthrough verified (2026-05-18). SEO metadata & markdown rendering bugs fixed.

- `[x]` **Phase 3: Intelligence & Outreach (ACTIVE)**
  - `[x]` **Skill Building**: Develop robust Playwright-based browser interaction tools (Atlas + Caleb).
  - `[x]` **SEO Automation**: Integrate Headless Browser (Playwright) for SEO audits and research.
  - `[ ]` **Client Onboarding**: Finalize the sovereign "Client Intake" workflow.
  - `[x]` **Agency Landing Page**: Build the first "Anti-Gravity Agency" portal (Caleb & Aria).
  - `[ ]` **Agency Refinement**: (On hold) Aria to audit aesthetics.


### Future Pipeline
Not found.

## Key Architecture Details
- **Entry point**: `ask.py` → routes to Alex (CEO) → delegates to sub-agents
- **Sovereign Routing**: 3-Layer local fallback (Specialist -> gemma2:27b -> Gemini).
- **Interactive Gate**: Cloud fallback requires explicit user `[Y/N]` approval to prevent data leakage.
- **Reflection Engine**: Automated `drift_report.md` generation on model failure.
- **Memory**: ChromaDB + Obsidian rules-first ingestion (`tru/Core_Rules/MEMORY_PROTOCOL.md`).

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

## Instructions for Next Session
1. Read this `GEMINI.md` to align on current progress.
2. Run `/lets get started` to initialize the system.
3. Prioritize delegation to local agents via `ask.py`.
