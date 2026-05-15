"""
Coder Agent for the Anti-Gravity Agent Ecosystem.
Specializes in code generation, debugging, refactoring, and technical documentation.
"""

from agents.base_agent import BaseAgent


class CoderAgent(BaseAgent):
    """
    Specialist coding agent powered by qwen2.5-coder:14b.
    Handles all code-related tasks delegated by the CEO.
    """

    def __init__(self):
        super().__init__(agent_name="Caleb", agent_id="caleb")

    def run(self, prompt: str) -> str:
        """Execute a coding task with Obsidian context augmentation and Reflexion."""
        # Augment with workspace context for better code awareness
        context = self.memory.get_context(prompt)
        augmented_prompt = f"{context}\n\n### CODING TASK ###\n{prompt}"

        self.logger.info("Executing coding task...")
        response = self.execute(augmented_prompt)
        
        # Execute any tools hallucinated by the agent
        result = self.parse_and_execute_tools(response)

        # Reflexion Loop: If tool errors occurred, try one self-healing cycle
        if "[TOOL ERROR]" in result:
            self.logger.warning("Tool errors detected. Starting Reflexion loop...")
            reflection_result = self.reflect(prompt, response, result)
            result = self.parse_and_execute_tools(reflection_result)

        # Log to Obsidian
        self.memory.log_memory(prompt, result, self.model_name, agent_name=self.agent_name)

        return result
