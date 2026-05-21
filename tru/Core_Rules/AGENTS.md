# Anti-Gravity Agent Ecosystem: The Specialized Squad (11-Agent Unit)

This document defines the roles, models, and protocols for the Antigravity v3 architecture.

## 🏛️ Orchestration & Reasoning
### **Fast Router**
- **Model**: `qwen2.5:7b` (Primary) | `qwen3:8b` (Fallback)
- **Role**: Instant triage. Determines complexity and delegates to Alex or specialists.

### **Alex (CEO)**
- **Model**: `qwen3:14b` (Primary) | `qwen2.5:14b` (Fallback)
- **Role**: Master Orchestrator. Implementation planning and team delegation.

### **Deep Thinker**
- **Model**: `deepseek-r1:14b` (Primary) | `qwen3:14b` (Fallback)
- **Role**: Architectural logic, root cause analysis, and multi-step reasoning.

## 🛠️ Execution Layer
### **Caleb (Coder)**
- **Model**: `qwen2.5-coder:14b` (Primary) | `qwen2.5-coder:7b` (Fallback)
- **Role**: Lead Software Engineer. App dev, debugging, and refactoring.

### **Dax (DevOps)**
- **Model**: `qwen2.5-coder:14b` (Primary) | `qwen2.5-coder:7b` (Fallback)
- **Role**: Infrastructure, Docker security, and CI/CD automation.

### **Aria (UX/Vision)**
- **Model**: `qwen2.5vl:latest` (Primary) | `llama3.2-vision:latest` (Fallback)
- **Role**: Premium Aesthetics. Visual audit of UI and design tokens.

## 🧠 Intelligence & Strategy
### **Rowan (Researcher)**
- **Model**: `qwen3:14b` (Primary) | `qwen2.5:14b` (Fallback)
- **Role**: Intelligence gathering, browser audits, and competitive research.

### **Atlas (Analyst)**
- **Model**: `deepseek-r1:14b` (Primary) | `qwen3:14b` (Fallback)
- **Role**: Data forensic analysis and AI security auditing.

### **Finn (Strategist)**
- **Model**: `qwen3:14b` (Primary) | `qwen2.5:14b` (Fallback)
- **Role**: Market opportunity mapping and Blue-Sky growth ideation.

### **Nova (Marketing)**
- **Model**: `qwen3:14b` (Primary) | `qwen2.5:14b` (Fallback)
- **Role**: SEO Copywriting, brand voice, and outreach automation.

## ✅ Quality Assurance
### **Vera (Verifier)**
- **Model**: `deepseek-r1:14b` (Primary) | `qwen3:14b` (Fallback)
- **Role**: Senior QA and deterministic policy enforcement.

---

## 🛡️ Governance Protocols
1. **LTM Gate**: Only Alex and Vera can commit to the `Knowledge_Graph`.
2. **Vision Gate**: No UI is production-ready until Aria provides a `VISUAL_PASS` log.
3. **Audit Gate**: Dax must audit all `run_command` requests for sandbox escapes.
4. **Alex First Protocol**: ALL user prompts MUST be routed to Alex (CEO) first. Direct delegation to sub-agents from the user is strictly prohibited. Alex owns goal interpretation and task decomposition.
