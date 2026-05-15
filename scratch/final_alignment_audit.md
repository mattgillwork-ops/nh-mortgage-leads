**ANTIGRAVITY SYSTEM – FINAL ALIGNMENT REVIEW**  
*Prepared for Alex (CEO)*  

---

## 1. Executive Summary  

| Area | Current State | Alignment Verdict | Primary Drift Identified |
|------|---------------|-------------------|--------------------------|
| **Model Tiering** | Registry ↔ Model‑registry mismatches in 9 of 11 agents. | **Drift present** – hardware‑optimized tiering (DeepSeek‑R1 14B for Vera/Atlas, qwen3 14b for Alex/Rowan/Finn/Nova, etc.) is not reflected in `agent_registry.yaml`. | Model‑name mismatches cause the resilience module to fall back to weaker models, undermining the “hardware‑optimized” promise. |
| **Infrastructure** | Heartbeat runs every 600 s; Repair Orchestrator scans only the most recent 20 logs for “heartbeat down” or “aria missing”. | **Partial** – loop is functional but limited in coverage and frequency. | Infrequent health‑check interval; limited log‑scan scope; no proactive model‑availability verification. |
| **Tool Security** | BaseAgent parses `TOOL:` calls via regex and checks `authorized_tools`. | **Functional but fragile** – regex may miss variations; whitelist lists are incomplete for many agents (e.g., deep_thinker lacks `search_the_web`). | Potential for silent bypass or false‑negative security alerts. |
| **Agent Personas** | Modelfiles are absent; role‑model mapping relies on registry entries. | **Misaligned** – several agents run models that do not match their declared persona (e.g., Caleb runs 7B coder instead of 14B). | Reduces specialization, increases latency, and violates the “hardware‑optimized tiering” policy. |

Overall, the system **operates** but is **not fully aligned** with the intended architecture. The remaining drift is concentrated in model‑tiering, infrastructure health‑monitoring, and tool‑security enforcement.

---

## 2. Detailed Findings  

### 2.1 Model Tiering (Hardware‑Optimized)  

| Agent | Intended Primary Model (per AGENTS.md) | Registry Primary | Registry Fallback | Model‑registry Primary | **Drift?** |
|-------|----------------------------------------|------------------|-------------------|------------------------|------------|
| fast_router | `qwen2.5:7b` | `anti-fast-router:latest` | `qwen2.5:7b` | `qwen2.5:7b` | **Yes** – name mismatch; should be `qwen2.5:7b` (no “anti‑” prefix). |
| alex | `qwen3:14b` | `anti-ceo:latest` | `qwen2.5:14b` | `qwen3:14b` | **Yes** – name mismatch; should be `qwen3:14b`. |
| deep_thinker | `deepseek-r1:14b` | `anti-deep-thinker:latest` | `qwen3:14b` | `deepseek-r1:14b` | **Yes** – name mismatch; should be `deepseek-r1:14b`. |
| caleb | `qwen2.5-coder:14b` | `qwen2.5-coder:7b` | `deepseek-coder:latest` | `qwen2.5-coder:14b` | **Yes** – primary should be 14B, not 7B. |
| dax | `qwen2.5-coder:14b` | `qwen2.5-coder:7b` | `qwen2.5-coder:7b` | `qwen2.5-coder:14b` | **Yes** – same as caleb. |
| rowan | `qwen3:14b` | `anti-researcher:latest` | `qwen2.5:14b` | `qwen3:14b` | **No** – matches. |
| atlas | `deepseek-r1:14b` | `deepseek-r1:14b` | `qwen3:14b` | `deepseek-r1:14b` | **No** – matches. |
| vera | `deepseek-r1:14b` | `deepseek-r1:14b` | `qwen3:14b` | `deepseek-r1:14b` | **No** – matches. |
| aria | `qwen2.5vl:latest` (vision) | `anti-aria:latest` | `llama3.2-vision:latest` | `anti-aria:latest` | **Yes** – should be `qwen2.5vl:latest` (or `llama3.2-vision:latest` if vision‑only). |
| nova | `qwen3:14b` | `qwen2.5:7b` | `mistral:latest` | `qwen3:14b` | **Yes** – primary should be 14B. |
| finn | `qwen3:14b` | `qwen2.5:7b` | `mistral:latest` | `qwen3:14b` | **Yes** – primary should be 14B. |

**Impact:**  
- Agents that run a lower‑capacity model (7B/8B) than their intended 14B counterpart will experience reduced reasoning quality, higher latency, and may trigger unnecessary fallback cycles.  
- The “hardware‑optimized tiering” guarantee (e.g., DeepSeek‑R1 14B for Vera/Atlas) is broken for 9/11 agents.

### 2.2 Infrastructure – Heartbeat + Repair Orchestrator  

| Component | Current Behaviour | Desired Behaviour | Gap |
|-----------|-------------------|-------------------|-----|
| **Heartbeat interval** | Fixed at 600 s (10 min). | Should be aggressive enough to catch drift quickly; 5‑10 min is acceptable, but 60 s is ideal for critical agents. | **Latency** – slower detection of model‑registry drift or daemon failure. |
| **Pre‑flight check** | Verifies Ollama reachability only. | Should also verify that each agent’s primary model is installed and healthy (`ollama list` + model pull). | **Visibility** – missing health of individual models. |
| **Repair Orchestrator** | Scans last 20 log files for “heartbeat down” or “aria missing”. | Should scan for any *model‑registry mismatch* (e.g., primary ≠ installed) and for any agent that reports “model not found”. | **Coverage** – limited to a narrow set of failure patterns; many mis‑alignments go undetected. |
| **Model‑registry sync** | `repair_model_registry` only updates the *primary* entry when a mismatch is found in logs. | Should also verify that the *fallback* model is present, and optionally auto‑pull missing models. | **Completeness** – may leave an agent without a usable fallback. |
| **Crash‑guard** | Daemon exits on any uncaught exception in `run_pulse_cycle`. | Should catch exceptions, log them, and continue the loop (already done) but also trigger an immediate alert (e.g., Slack/email). | **Observability** – no alerting path. |

### 2.3 Tool Security (BaseAgent Firewall)  

- **Whitelist enforcement** relies on a regex `r"TOOL:\s*(\w+)\((.*?)\)"`.  
  - **Risk:** Variations such as `TOOL: search_the_web()` or `TOOL:search_the_web (arg)` will not be captured, leading to **silent bypass**.  
- **Authorized tool list** is taken from `agent_registry.yaml` → `permissions.tools`.  
  - **Observations:**  
    - `fast_router` only permits `triage` & `classify`. If a response contains `TOOL: read_file`, it will be blocked (good).  
    - `deep_thinker` permits only `read_file` & `list_dir`. If a response includes `TOOL: search_the_web`, it will be blocked – **correct**.  
    - However, many agents (e.g., `alex`, `rowan`, `nova`, `finn`) have *broad* tool permissions but the regex may not capture all tool names they intend to use (e.g., `browser_action`, `view_window`).  
- **Potential Gap:** The firewall does **not** validate that the *arguments* are safe (e.g., path traversal in `read_file`). This is out of scope for the current review but worth noting.

### 2.4 Agent Personas & Modelfile Consistency  

- **Modelfiles** (the source of truth for persona‑model mapping) are not provided in the review set.  
- **Registry vs. Persona:**  
  - `vera` (QA/Verifier) correctly uses `deepseek-r1:14b`.  
  - `atlas` (Security Analyst) correctly uses `deepseek-r1:14b`.  
  - `deep_thinker` (Architectural logic) should use `deepseek-r1:14b` – registry currently shows `anti-deep-thinker:latest` (name mismatch).  
  - `alex` (CEO) should be `qwen3:14b` – registry shows `anti-ceo:latest`.  
- **Result:** The *persona* (role) is **not** consistently reflected by the *model* name, violating the “Model Tiering” design principle.

---

## 3. Recommendations – Final Repair / Polishing Plan  

### 3.1 Model‑Tiering Alignment  

1. **Standardise Model Names**  
   - Remove all “anti‑” prefixes from `agent_registry.yaml`.  
   - Align each agent’s `primary` field with the exact model name defined in `model_registry.yaml`.  

   Example changes:  
   ```yaml
   fast_router:
     primary: "qwen2.5:7b"
     fallback: "qwen3:8b"
   alex:
     primary: "qwen3:14b"
     fallback: "qwen2.5:14b"
   deep_thinker:
     primary: "deepseek-r1:14b"
     fallback: "qwen3:14b"
   caleb:
     primary: "qwen2.5-coder:14b"
     fallback: "qwen2.5-coder:7b"
   dax:
     primary: "qwen2.5-coder:14b"
     fallback: "qwen2.5-coder:7b"
   rowan:
     primary: "qwen3:14b"
     fallback: "qwen2.5:14b"
   nova:
     primary: "qwen3:14b"
     fallback: "qwen2.5:14b"
   finn:
     primary: "qwen3:14b"
     fallback: "qwen2.5:14b"
   aria:
     primary: "qwen2.5vl:latest"
     fallback: "llama3.2-vision:latest"
   ```

2. **Validate Registry Consistency**  
   - Add a **validation script** (`tools/validate_registry.py`) that parses both YAML files and reports any discrepancy between `agent_registry.yaml` and `model_registry.yaml`. Run this as part of the CI pipeline (or nightly cron).  

3. **Model Availability Checks**  
   - Extend `BaseAgent._check_availability` to verify that the *primary* model is listed in `ollama list`. If missing, trigger an automatic pull (`ollama pull <model>`).  

### 3.2 Infrastructure – Heartbeat & Repair Orchestrator Enhancements  

1. **Reduce Pulse Interval**  
   - Change `CHECK_INTERVAL` from 600 s to **300 s** (5 min) for production. This gives faster detection of daemon or model failures without excessive load.  

2. **Broaden Pre‑flight Checks**  
   - Add a function `check_all_models()` that iterates over every agent’s `primary` model and confirms presence via `ollama list`. Log a warning if any are missing.  

3. **Enrich Repair Orchestrator Log Scan**  
   - Replace the simplistic “last 20 logs” scan with a **structured search** for keywords:  
     - `"model not found"`  
     - `"registry mismatch"`  
     - `"heartbeat down"`  
     - `"unauthorized tool"`  
   - For each match, invoke the appropriate repair function (restart daemon, update registry, pull missing model).  

4. **Add Alerting**  
   - When the orchestrator detects a failure it cannot auto‑repair, send a **system alert** (e.g., write to `alarms.log` and optionally push a webhook).  

5. **Graceful Degradation**  
   - If the heartbeat daemon itself crashes, the orchestrator should automatically **re‑spawn** it *and* log the event with a severity level.  

### 3.3 Tool Security – Robust Whitelist  

1. **Regex Improvement**  
   - Update `parse_and_execute_tools` to use a **more tolerant pattern**:  

     ```python
     tool_pattern = re.compile(r"TOOL:\s*(\w+)(?:\((.*?)\))?", re.IGNORECASE)
     ```

   - This captures `TOOL:search_the_web` as well as `TOOL:search_the_web(arg)`.  

2. **Argument Sanitisation**  
   - For `read_file` and `list_dir`, validate that the supplied path is within an allowed base directory (e.g., `BASE_DIR`). Reject paths that attempt to escape the sandbox.  

3. **Audit Trail**  
   - Log every *authorized* tool execution with a unique request ID. This aids forensic analysis if a security breach is later discovered.  

### 3.4 Agent Persona Consistency  

1. **Create Modelfile Templates** (if not already present) that bind a role to a model version, e.g.:

   ```yaml
   # Modelfile for deep_thinker
   name: anti-deep-thinker
   model: deepseek-r1:14b
   context: 8192
   ```

   - Align each agent’s `primary` entry in `agent_registry.yaml` with the model declared in its Modelfile.  

2. **Automated Persona‑Model Sync**  
   - Extend the validation script (see 3.1) to also compare the *role* (from AGENTS.md) with the *model* in the Modelfile, warning if they diverge.  

### 3.5 Continuous Alignment Guardrails  

| Guardrail | Frequency | Owner |
|-----------|-----------|-------|
| **Registry Validation** (`validate_registry.py`) | Nightly (or on every git push) | DevOps (Dax) |
| **Model Availability Health‑Check** (pre‑flight) | Every heartbeat cycle | Heartbeat Daemon |
| **Tool‑Call Auditing** (log‑based) | Real‑time (via BaseAgent) | BaseAgent |
| **Persona‑Model Sync Review** | Weekly (automated) | Architecture Lead (Deep Thinker) |
| **Infrastructure Drift Report** (`drift_report.md`) | Generated after each pulse cycle | Heartbeat Daemon |

---

## 4. Immediate Action Items (Next 24 h)

| # | Action | Owner | Deadline |
|---|--------|-------|----------|
| 1 | Update `agent_registry.yaml` to remove “anti‑” prefixes and align model names with `model_registry.yaml`. | Architecture Lead (Deep Thinker) | **T+12 h** |
| 2 | Run `tools/validate_registry.py` (create if missing) and fix any reported mismatches. | DevOps (Dax) | **T+12 h** |
| 3 | Reduce `CHECK_INTERVAL` in `heartbeat_daemon.py` from 600 s → 300 s. | DevOps (Dax) | **T+6 h** |
| 4 | Enhance `BaseAgent._check_availability` to verify primary model presence and auto‑pull if absent. | Deep Thinker | **T+12 h** |
| 5 | Refactor `parse_and_execute_tools` regex to tolerate optional parentheses and case variations. | Deep Thinker | **T+12 h** |
| 6 | Add structured log‑scan in `repair_orchestrator.py` for model‑registry drift keywords. | Deep Thinker | **T+12 h** |
| 7 | Commit all changes, trigger a full system health check (`py selfcheck.py --full`) and verify no drift warnings appear. | All | **T+24 h** |

---

## 5. Conclusion  

The Antigravity system is **functionally operational**, but **alignment drift**—particularly in model tiering, infrastructure health‑monitoring, and tool‑security enforcement—remains a material risk. By standardising model names, tightening health‑checks, expanding the repair orchestrator’s detection logic, and hardening the tool‑call whitelist, we will bring the implementation into full compliance with the **Intended Architecture** defined in AGENTS.md and WORKSPACE_AI_RULES.md.

Implementing the above plan will:

- **Guarantee hardware‑optimized tiering** (14B models where required).  
- **Accelerate fault detection** and reduce mean‑time‑to‑recovery.  
- **Eliminate silent security bypasses** through robust whitelist parsing and argument sanitisation.  
- **Ensure agent personas** faithfully map to their designated models, preserving specialisation and performance.

Once the immediate actions are completed and the validation script is integrated into the CI pipeline, the system will be **fully aligned** and ready for the next phase of business‑feature development (e.g., NH Mortgage Lead Gen).

*Prepared by Deep Thinker – Architectural Alignment Lead*