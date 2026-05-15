"""
CEO Agent (Alex) - Master Orchestrator for Antigravity.
"""

import json
import re
import logging
from agents.base_agent import BaseAgent

class CEOAgent(BaseAgent):
    def __init__(self, sub_agents: dict = None):
        super().__init__(agent_name="Alex", agent_id="alex")
        self.sub_agents = sub_agents or {}

    def run(self, prompt: str) -> str:
        """The Orchestration Loop."""
        self.logger.info(f"Orchestrating goal: {prompt[:50]}...")
        
        # 1. High-Stakes Logic: Consult Deep Thinker for Architecture/Strategy
        if any(kw in prompt.lower() for kw in ["architecture", "strategy", "design system", "review"]):
            self.logger.info("High-stakes task. Consulting Deep Thinker...")
            reasoning = self.sub_agents['thinker'].execute(f"Analyze tradeoffs for: {prompt}")
            prompt = f"### ARCHITECTURAL ADVICE ###\n{reasoning}\n\n### TASK ###\n{prompt}"

        # 2. Planning & Execution (Alex's own reasoning)
        # We explicitly prompt for a delegation command if the task is complex
        response = self.execute(prompt)
        
        # 3. Structured Delegation Engine
        # Syntax: [DELEGATE: AgentName -> Task description]
        delegation_match = re.findall(r"\[DELEGATE: (.*?) -> (.*?)\]", response, re.IGNORECASE)
        
        for agent_ref, sub_task in delegation_match:
            # Map aliases (e.g. 'Rowan' to 'researcher')
            agent_map = {
                'rowan': 'researcher', 'researcher': 'researcher',
                'atlas': 'analyst', 'analyst': 'analyst',
                'caleb': 'coder', 'coder': 'coder',
                'dax': 'devops', 'devops': 'devops',
                'aria': 'ux', 'ux': 'ux',
                'vera': 'verifier', 'verifier': 'verifier',
                'nova': 'marketing', 'marketing': 'marketing',
                'finn': 'strategist', 'strategist': 'strategist',
                'thinker': 'thinker', 'deep_thinker': 'thinker'
            }
            
            agent_id = agent_map.get(agent_ref.lower())
            if agent_id and agent_id in self.sub_agents:
                self.logger.info(f"Executing Sovereign Delegation to {agent_id}: {sub_task[:50]}...")
                sub_resp = self.sub_agents[agent_id].run(sub_task)
                response += f"\n\n### {agent_id.upper()} OUTPUT ###\n{sub_resp}"

        # 4. Tool Execution (Firewall)
        response = self.parse_and_execute_tools(response)

        # 5. Memory Governance: Route Proposals to Vera
        if "PROPOSE LTM" in response or "Knowledge_Graph" in response:
            self.logger.info("LTM Proposal detected. Forwarding to Vera...")
            validation = self.sub_agents['vera'].execute(f"Validate this proposal: {response}")
            response = f"{response}\n\n### VERIFIER AUDIT ###\n{validation}"

        # 6. Final QA
        qa_result = self.sub_agents['vera'].execute(f"QA check on response: {response[:500]}")
        
        final_output = f"{response}\n\n### FINAL QA VERDICT ###\n{qa_result}"
        self.memory.log_memory(prompt, final_output, self.model_name, self.agent_name)
        return final_output
