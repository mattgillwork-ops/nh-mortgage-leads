from agents.base_agent import BaseAgent

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Data Analyst", model_name="anti-analyst")

    def run(self, prompt: str) -> str:
        context = self.memory.get_context()
        augmented_prompt = f"{context}\n\n### DATA ANALYSIS TASK ###\n{prompt}"
        self.logger.info("Executing data analysis task...")
        
        response = self.execute(augmented_prompt)
        
        # Execute tools (can read CSVs, etc.)
        response_with_tools = self.parse_and_execute_tools(response)
        
        self.memory.log_memory(prompt, response_with_tools, self.model_name, agent_name=self.agent_name)
        return response_with_tools
