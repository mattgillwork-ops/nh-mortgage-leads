# Research & Accuracy Protocol

To prevent hallucinations (like the "Grok" incident), all agents must adhere to the following rules when performing research or providing factual information:

## 1. The "Current Events" Search Trigger
You MUST use the `web_search` tool if the task involves:
- **Product Releases**: Any mention of models, software, or hardware released after **2023**.
- **Company News**: Current status of tech companies (xAI, OpenAI, Anthropic, Google, etc.).
- **Specific Versions**: Versions of libraries (e.g. "ChromaDB v0.5") where syntax may have changed.
- **External Benchmarks**: Comparison of cloud models (Grok vs. Gemini vs. GPT-4).

## 2. Confidence Scoring
Before outputting research, mentally assess your confidence. If you are less than 95% certain of the *current* state of the topic, you are FORBIDDEN from guessing. You must use `web_search`.

## 3. Hallucination Markers (Internal Verification)
When reviewing research, the Verifier must check for:
- **Semantic Drift**: Does the agent's explanation match an older academic concept instead of the modern product? (e.g., explaining "Grok" as explainable AI).
- **Outdated Links/Prices**: Verify if links or pricing mentioned are current.

## 4. Source Citation
The Researcher agent MUST cite at least 2 search results when answering questions about technology released in the last 2 years.
