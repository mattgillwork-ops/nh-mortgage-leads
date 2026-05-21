#!/usr/bin/env python3
"""
Anti-Gravity Research Drive — OpenAI Edition
=============================================
Routes Alex (CEO) through OpenAI GPT-4o as the primary engine.
Delegates research to Rowan and strategy synthesis to Finn.
All output is saved to tru/Research/nh_traffic_research.md
"""

import os
import sys
import io
from datetime import datetime
from dotenv import load_dotenv

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    print("[ERROR] openai package not installed. Run: pip install openai")
    sys.exit(1)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("[ERROR] OPENAI_API_KEY is not set in .env")
    sys.exit(1)

client = OpenAI(api_key=API_KEY)
MODEL = "gpt-4o"

OUTPUT_PATH = os.path.join("tru", "Research", "nh_traffic_research.md")

CURRENT_DATE = datetime.now().strftime("%B %d, %Y")
SYSTEM_CONTEXT = f"""You are part of the Anti-Gravity AI Ecosystem. The date is {CURRENT_DATE}.
We operate three web properties targeting the New Hampshire mortgage market:
1. Lead Funnel (mortgage-app): A 6-step Next.js pre-qualification funnel with UTM tracking, Supabase persistence, and local vault lead storage.
2. Blog Site (nh-mortgage-blog): A Next.js blog covering local NH mortgage topics (NHHFA, closing costs, city-specific guides for Manchester, Portsmouth, Concord, Nashua, Hanover).
3. Comparison Site (nh-financial-review): A lender comparison/list site.

Affiliate programs (Impact.com, CJ Affiliate) are pending approval — not yet active.
Our goal is to drive organic search traffic and local traffic to generate real leads from New Hampshire homebuyers NOW, before affiliates are live.
"""

def call_openai(system_role: str, user_prompt: str, label: str) -> str:
    print(f"\n[OPENAI:{MODEL}] Running {label}...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_CONTEXT + "\n\n" + system_role},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4,
        max_tokens=2500
    )
    result = response.choices[0].message.content.strip()
    print(f"[DONE] {label} complete. ({len(result)} chars)")
    return result


def alex_orchestrate() -> dict:
    """Alex (CEO) breaks down the research objective into targeted sub-tasks."""
    system = """You are Alex, CEO Orchestrator of the Anti-Gravity AI ecosystem.
Your role: Decompose the user's research goal into 3 precise, actionable sub-tasks:
  - One for Rowan (Keyword & SEO Researcher): What specific NH mortgage keyword clusters, intent signals, and on-page SEO opportunities should Rowan investigate?
  - One for Nova (Marketing Channel Researcher): What specific free/low-cost traffic channels should Nova evaluate for immediate lead generation?
  - One for Finn (Strategist): After receiving Rowan and Nova's findings, what synthesis framework should Finn use to create a prioritized action plan?

Output ONLY as JSON with keys: rowan_task, nova_task, finn_instructions"""

    prompt = """Research objective: Identify the best ways to drive organic search traffic and local traffic to our New Hampshire mortgage sites to generate our first real leads. Affiliates are not yet approved. Budget is zero or near-zero. We need tactics that can produce results within 30-90 days."""

    result = call_openai(system, prompt, "Alex — CEO Orchestration")
    
    import json
    import re
    # Extract JSON block even if model wraps it in markdown
    json_match = re.search(r'\{.*\}', result, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    # Fallback if JSON parse fails
    return {
        "rowan_task": "Research NH mortgage keyword clusters, local intent queries, and on-page SEO opportunities for Manchester, Portsmouth, Concord, Nashua.",
        "nova_task": "Identify free traffic channels: Reddit NH communities, Facebook homebuyer groups, Nextdoor, Google Business Profile, and Google Search Console submission strategies.",
        "finn_instructions": "Synthesize all findings into a prioritized action plan with effort level, expected impact, and 30/60/90-day milestones."
    }


def rowan_research(task: str) -> str:
    """Rowan (SEO Researcher) digs into NH mortgage keyword clusters and on-page SEO."""
    system = """You are Rowan, the SEO Keyword Research Specialist for Anti-Gravity.
You specialize in finding low-competition, high-intent keywords for local mortgage markets.
Be extremely specific to New Hampshire. Use real mortgage terminology, real NH city names, real government programs (e.g., NHHFA, Home Start, InvestNH).
For each keyword cluster, provide: target query, search intent (informational/commercial/transactional), estimated monthly volume (low/med/high), SEO difficulty (low/med/high), and the best landing asset to target it."""

    return call_openai(system, task, "Rowan — SEO Keyword Research")


def nova_research(task: str) -> str:
    """Nova (Marketing) researches free channels for immediate traffic and lead gen."""
    system = """You are Nova, the Marketing and Growth Specialist for Anti-Gravity.
You specialize in zero-budget and near-zero-budget traffic acquisition strategies.
Focus on what can realistically drive traffic to a New Hampshire mortgage site TODAY.
Be specific: name the exact subreddits, Facebook groups, Nextdoor strategies, Google tools, and community tactics.
For each channel: explain how to use it, what content works, how to avoid being seen as spam, and expected timeline to first leads."""

    return call_openai(system, task, "Nova — Marketing Channel Research")


def finn_synthesize(rowan_output: str, nova_output: str, finn_instructions: str) -> str:
    """Finn (Strategist) synthesizes all findings into a final prioritized plan."""
    system = """You are Finn, the Strategy and Planning Specialist for Anti-Gravity.
You excel at synthesizing research into clear, prioritized action plans.
Format the output as a proper implementation plan with:
- Executive Summary
- Priority 1 Actions (High Impact / Low Effort — do this FIRST)
- Priority 2 Actions (High Impact / Higher Effort — build toward these)
- Priority 3 Actions (Longer Term / Compounding)
- For each action: description, effort (1-5), expected impact (1-5), timeline, owner (which agent), and specific first step.
- A 30/60/90 day milestone roadmap."""

    prompt = f"""Synthesize the following research into a prioritized action plan for driving traffic and generating our first leads.

## Rowan's SEO & Keyword Research:
{rowan_output}

## Nova's Marketing Channel Research:
{nova_output}

## Synthesis Instructions:
{finn_instructions}"""

    return call_openai(system, prompt, "Finn — Strategy Synthesis")


def save_report(alex_tasks: dict, rowan: str, nova: str, finn: str):
    """Saves the full research drive output as a vault markdown file."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    content = f"""---
type: research
project: NH Mortgage Traffic Acquisition
date: {CURRENT_DATE}
agents: [Alex, Rowan, Nova, Finn]
model: OpenAI {MODEL}
status: pending_review
---

# NH Traffic & Lead Generation Research Drive

**Date**: {CURRENT_DATE}  
**Objective**: Identify the best ways to drive organic search and local traffic to our NH mortgage sites and generate first leads before affiliate approvals.  
**Router**: OpenAI {MODEL} (Alex — CEO Orchestrator)

---

## 1. Alex's Research Brief (Orchestration Layer)
```json
{str(alex_tasks)}
```

---

## 2. Rowan's SEO & Keyword Research

{rowan}

---

## 3. Nova's Marketing Channel Research

{nova}

---

## 4. Finn's Synthesized Action Plan

{finn}

---

*Generated by Anti-Gravity Research Drive | Awaiting User Approval*
"""
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n[VAULT] Research report saved to: {OUTPUT_PATH}")


def main():
    print("=" * 65)
    print("  ANTI-GRAVITY RESEARCH DRIVE — OpenAI Edition")
    print(f"  Model: {MODEL} | Orchestrator: Alex (CEO)")
    print("=" * 65)
    
    # Step 1: Alex decomposes the objective
    print("\n[STEP 1/4] Alex orchestrating research objective...")
    alex_tasks = alex_orchestrate()
    print(f"  -> Rowan Task: {alex_tasks.get('rowan_task', '')[:80]}...")
    print(f"  -> Nova Task:  {alex_tasks.get('nova_task', '')[:80]}...")

    # Step 2: Rowan researches keywords
    print("\n[STEP 2/4] Rowan conducting SEO & keyword research...")
    rowan_output = rowan_research(alex_tasks.get("rowan_task", ""))

    # Step 3: Nova researches channels
    print("\n[STEP 3/4] Nova researching traffic channels...")
    nova_output = nova_research(alex_tasks.get("nova_task", ""))

    # Step 4: Finn synthesizes into a plan
    print("\n[STEP 4/4] Finn synthesizing into prioritized action plan...")
    finn_output = finn_synthesize(rowan_output, nova_output, alex_tasks.get("finn_instructions", ""))

    # Save to vault
    save_report(alex_tasks, rowan_output, nova_output, finn_output)
    
    print("\n" + "=" * 65)
    print("  RESEARCH DRIVE COMPLETE")
    print(f"  Report saved to: {OUTPUT_PATH}")
    print("  Awaiting user approval before execution.")
    print("=" * 65)
    
    # Print Finn's plan to console for immediate review
    print("\n\n" + "=" * 65)
    print("  FINN'S PRIORITIZED ACTION PLAN (Preview)")
    print("=" * 65)
    print(finn_output)


if __name__ == "__main__":
    main()
