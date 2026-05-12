# Anti-Gravity Routing & Fallback Protocol
**STATUS**: CRITICAL CORE RULE
**ENFORCEMENT**: MANDATORY READ FOR ALL AGENTS

## 1. Sovereign Model Hierarchy
To protect data privacy and prioritize local infrastructure, the system follows a strict 3-Layer routing hierarchy. No data may leave the local network without explicit user authorization.

### Layer 1: Specialist Agent (Primary)
- **Model**: Assigned 14B Specialist (e.g., `anti-ceo`, `anti-coder`).
- **Goal**: Handle tasks with domain-specific fine-tuning.
- **Constraint**: Must attempt local execution at least 2 times before escalating.

### Layer 2: Local Powerhouse (Secondary)
- **Model**: Large Local Generalist (e.g., `gemma2:27b`, `qwen3.6`, or `nemotron3:33b`).
- **Purpose**: Used when the specialist fails due to logic complexity, context window pressure, or model-specific errors.
- **Constraint**: Retries the original prompt with higher parameter counts to attempt a local resolution.

### Layer 3: Cloud Fallback (Emergency)
- **Model**: Gemini 2.0 Flash (External).
- **Rule**: **INTERACTIVE APPROVAL REQUIRED**. 
- **Constraint**: If Layer 1 and 2 fail, the system must present a "Failure Review" to the user and request permission to use the cloud. Silent fallbacks are strictly prohibited.

## 2. Failure Reflection
When a local model hits a fatal error, the agent must enter a **Reflection Phase** before escalating.
- **Analyze**: Determine if the error was Hardware (OOM), Software (Ollama crash), or Logic (Prompt too complex).
- **Prevent**: Generate a `system_drift_report.md` with suggestions to prevent the error in the future.

---
*The ecosystem prioritizes sovereignty and privacy over immediate completion speed.*
