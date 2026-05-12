# Anti-Gravity Memory Protocol
**STATUS**: CRITICAL CORE RULE
**ENFORCEMENT**: MANDATORY READ FOR ALL AGENTS

## 1. Vault Architecture Overview
The Obsidian vault (`tru/`) is the shared "source of truth" for the entire Multi-Agent ecosystem. It is divided into strictly enforced layers. You must understand where to read and write data based on its permanence.

## 2. Short-Term Memory (Episodic)
**Path**: `tru/Memory_Logs/`
- **Purpose**: A chronological scratchpad and audit trail. This is where your execution logs are automatically saved. 
- **Rule 1 (Write-Only)**: You may generate temporary thoughts or intermediate steps here via the system's auto-logger.
- **Rule 2 (No Business Logic)**: You must **NEVER** read from `Memory_Logs` to find active business context, tasks, or project briefs. The Knowledge Manager prunes this folder autonomously. Do not rely on it for permanent state.

## 3. Long-Term Memory (Project State)
**Path**: `tru/Projects/`
- **Purpose**: The active, mutable collaboration layer for the agency. 
- **Rule 3 (Shared State)**: If you are working on a specific task (e.g., SEO Audit, Code Refactor), you must write your findings, outlines, and code blueprints into a designated Project file here.
- **Rule 4 (Link MOCs)**: Every project file must link back to `[[Active_Projects_MOC]]`.

## 4. Long-Term Memory (Knowledge Graph)
**Path**: `tru/Knowledge_Graph/`
- **Purpose**: Persistent, distilled truths, Standard Operating Procedures (SOPs), and immutable agency facts.
- **Rule 5 (Distillation)**: Only write to the Knowledge Graph when a project is completed and its insights have been verified as universally true for future tasks.

## 5. Structural Metadata (YAML & Wikilinks)
- **YAML Frontmatter**: Always use YAML blocks at the top of notes for structured metadata (`status`, `agent`, `date`).
- **Wikilinks**: Always use Obsidian Wikilinks `[[Like This]]` when referencing other agents or projects in the body text. Do not use standard markdown links for internal vault files.

---
*Failure to adhere to this protocol will result in fragmented memory, context bloat, and system hallucination.*
