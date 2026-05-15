"""
Strategy Agent (Finn) - Creative strategic alternatives.
"""

from agents.base_agent import BaseAgent

class StrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Finn", agent_id="finn")

    def run(self, prompt: str) -> str:
        """Execute a strategy task."""
        return self.execute(prompt)
