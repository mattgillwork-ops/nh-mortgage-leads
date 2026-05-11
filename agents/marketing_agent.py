"""
Marketing Agent for the Anti-Gravity Agent Ecosystem.
Specializes in creative writing, ad copy, email campaigns, and brand messaging.
"""

from agents.base_agent import BaseAgent


class MarketingAgent(BaseAgent):
    """
    Specialist marketing/creative agent powered by mistral:latest.
    Handles all marketing and creative writing tasks delegated by the CEO.
    """

    def __init__(self):
        super().__init__(agent_name="Marketing", model_name="anti-marketing")

    def run(self, prompt: str) -> str:
        """Execute a marketing/creative task with Obsidian context augmentation."""
        context = self.memory.get_context()
        augmented_prompt = f"{context}\n\n### MARKETING TASK ###\n{prompt}"

        self.logger.info("Executing marketing task...")
        response = self.execute(augmented_prompt)

        # Log to Obsidian
        self.memory.log_memory(prompt, response, self.model_name, agent_name=self.agent_name)

        return response
