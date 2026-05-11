from agents.base_agent import BaseAgent

class DevOpsAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="DevOps", model_name="anti-devops")

    def run(self, prompt: str) -> str:
        context = self.memory.get_context()
        augmented_prompt = f"{context}\n\n### INFRASTRUCTURE TASK ###\n{prompt}"
        self.logger.info("Executing DevOps task...")
        
        response = self.execute(augmented_prompt)
        
        # Execute tools (especially <run_command>)
        response_with_tools = self.parse_and_execute_tools(response)
        
        self.memory.log_memory(prompt, response_with_tools, self.model_name, agent_name=self.agent_name)
        return response_with_tools
