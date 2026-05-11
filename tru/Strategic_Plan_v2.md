# Anti-Gravity Strategic Roadmap v2 (2026)

*Synthesized by Cloud Orchestrator (Gemini) following Phase 1 & 2 Local Audits.*

## Executive Summary
The Anti-Gravity ecosystem is currently stable, featuring a resilient "Paranoia Protocol" and cloud-fallback mechanics. However, to scale into a robust enterprise engine, we must migrate from custom tool scripts to standardized protocols, and formalize our skill ecosystem.

## Phase 1: Skill Governance & Standardization

### 1. Migrate to Model Context Protocol (MCP)
- **Current State**: Tools (`browser_skill.py`, `web_search.py`) are ad-hoc Python scripts executed via `run_command`.
- **Target State**: Convert all tools into an MCP server format. This allows seamless, standardized discovery of tools by any agent without custom XML tag parsing.
- **Action**: Dax (DevOps) will scaffold a central MCP server within the `anti-sandbox` Docker environment.

### 2. Establish the Governed Skill Repository
- **Current State**: Tools live in a flat `tools/` directory.
- **Target State**: Create a `skills/` repository structure where every skill has a `SKILL.md` metadata file, a test suite, and a security policy.
- **Action**: Caleb (Coder) will restructure the tools directory and implement a continuous integration loop for testing skills.

## Phase 2: Security & Policy Enforcement

### 1. Deploy the Gatekeeper (PyRIT Integration)
- **Current State**: Vera (Verifier) acts as a post-execution QA node.
- **Target State**: Implement a pre-execution Security Gatekeeper using PyRIT. This node will scan all incoming external inputs (like emails or search results) for prompt injection *before* they hit the processing agents.
- **Action**: Atlas (Analyst) will lead the integration of PyRIT scripts into the CEO's ingestion pipeline.

### 2. Context Hygiene Automation
- **Current State**: We rely on periodic manual memory purges to fix "Phantom Tasks."
- **Target State**: Implement an automated RAG pruning script that runs continuously in the Heartbeat Daemon to summarize and compress episodic memory, discarding volatile logs after 24 hours.
- **Action**: Dax (DevOps) will expand the Heartbeat Daemon to run `knowledge_manager.py` against the ChromaDB vector indices.

## Phase 3: Advanced Orchestration

### 1. Stateful Planning (LangGraph Exploration)
- **Current State**: Agents operate in a stateless, linear relay.
- **Target State**: Evaluate migrating the `CEOAgent` from basic RAG loops to a stateful, cyclic orchestration graph using LangGraph.
- **Action**: Rowan (Researcher) and Caleb (Coder) will build a proof-of-concept LangGraph node for complex multi-agent workflows.

---
**Status**: APPROVED FOR EXECUTION
**Approval**: Awaiting User Sign-off
