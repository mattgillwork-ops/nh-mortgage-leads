# Gemini AI Configuration and Routing Rules

This workspace adheres to a strict model tiering and fallback architecture to optimize for cost, performance, and reliability. 

## Model Tiering Rules

1. **Primary Fast Router**: 
   - **Models**: Local `qwen2.5:7b` or `llama3.1:8b` via Ollama.
   - **Use Case**: Basic tool selection, workspace navigation, and simple decision-making tasks. This is the default entry point for all operations to save tokens.

2. **Deep Thinker**: 
   - **Models**: Local `qwen2.5:32b` or `gemma2:27b` via Ollama.
   - **Use Case**: Heavy reasoning, complex coding, architectural planning, and tasks requiring extensive context comprehension.

## Cloud Fallback Logic

To ensure the workspace remains unblocked, the following fallback logic is strictly enforced:
- **Condition**: If local models (Fast Router or Deep Thinker) fail to solve a problem, get stuck in an infinite loop, or encounter an error 3 consecutive times.
- **Action**: Automatically fall back to the cloud-based **Gemini 3.1 Pro** model to resolve the blocker.
