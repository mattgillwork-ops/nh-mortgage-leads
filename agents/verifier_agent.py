"""
Verification Agent for the Anti-Gravity Agent Ecosystem.
Specializes in QA, output verification, and providing actionable feedback.
"""

from agents.base_agent import BaseAgent


class VerifierAgent(BaseAgent):
    """
    Specialist QA/verification agent powered by deepseek-r1:8b.
    Uses chain-of-thought reasoning to systematically verify outputs
    against original task requirements.
    """

    def __init__(self):
        super().__init__(agent_name="Verifier", model_name="anti-verifier")

    def run(self, prompt: str) -> str:
        """
        Execute a verification task.
        The prompt should contain both the original task and the agent output to verify.
        Returns raw JSON string for the CEO to parse.
        """
        self.logger.info("Executing verification task...")
        response = self.execute(prompt, json_mode=True)

        # Log to Obsidian
        self.memory.log_memory(prompt[:200], response, self.model_name, agent_name=self.agent_name)

        return response
