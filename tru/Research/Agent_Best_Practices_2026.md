# Agentic Design Patterns & Skill Repositories (2026)

This report summarizes the industry-standard best practices and tools for building autonomous multi-agent ecosystems as of mid-2026.

## 1. Core Design Patterns

### A. ReAct (Reason + Act)
The foundational loop. Agents reason about a task, choose a tool, observe the output, and repeat.
- **Best for**: Simple, deterministic tasks.
- **Anti-Gravity Status**: Currently our primary pattern.

### B. Planning (Plan-and-Execute)
Separates the "Strategy" (Planner) from the "Action" (Executor). A planner breaks a goal into sub-tasks; the executor runs them.
- **Best for**: Complex, multi-step goals.
- **2026 Standard**: Frameworks like **LangGraph** enable stateful, cyclic planning.

### C. Reflection (Evaluator-Optimizer)
An agent critiquing its own work or another agent's work.
- **Best for**: Code generation, writing, and high-accuracy research.
- **Anti-Gravity Status**: Partially implemented via **Vera (Verifier)**.

### D. Hierarchical Orchestration
A supervisor agent (like Alex) delegates to specialized subordinates (the Squad).
- **Best for**: Scaling complex businesses.

## 2. Frameworks & Skill Repositories

### A. Major Frameworks
1. **LangGraph**: The standard for stateful, complex agent logic.
2. **AutoGen**: Leader in autonomous multi-agent conversation.
3. **CrewAI**: Optimized for role-playing and distinct agent goals.
4. **Mastra**: TypeScript-first, built-in observability and MCP support.

### B. Skill Repositories
- **Volt-Agent / Awesome Agent Skills**: A curated library of 1,000+ versioned skills.
- **Anthropic / Building Effective Agents**: The blueprint for robust agentic engineering.

## 3. Emerging Standards: MCP

The **Model Context Protocol (MCP)** is now the universal language for agents.
- **Function**: Standardizes how agents connect to files, databases, and APIs.
- **Recommendation**: The Anti-Gravity squad should migrate tool-calling to MCP for better interoperability.

## 4. Best Practices for 2026
- **Architect for Control**: Use "Intent Previews" (Human-in-the-Loop) for high-stakes actions.
- **Observability**: Implement tracing for every agent step to debug "Phantom Task" hallucinations.
- **Context Hygiene**: Never append full history; use structured summaries and RAG pruning.
- **Skill Governance**: All tools should be in a central `skills/` repo with automated QA tests.
