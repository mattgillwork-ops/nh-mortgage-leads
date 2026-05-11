from agents.base_agent import BaseAgent

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Researcher", model_name="anti-researcher")

    def run(self, prompt: str) -> str:
        context = self.memory.get_context()
        augmented_prompt = f"{context}\n\n### RESEARCH TASK ###\n{prompt}"
        self.logger.info("Executing research task...")
        
        response = self.execute(augmented_prompt)
        
        # Researchers might use tools to read files, so we execute them
        response_with_tools = self.parse_and_execute_tools(response)
        
        self.memory.log_memory(prompt, response_with_tools, self.model_name, agent_name=self.agent_name)
        return response_with_tools
