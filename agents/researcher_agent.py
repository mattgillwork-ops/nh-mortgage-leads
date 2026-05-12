from agents.base_agent import BaseAgent

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Researcher", model_name="anti-researcher")

    def run(self, prompt: str) -> str:
        """Execute a research task with recursive tool execution."""
        context = self.memory.get_context(query=prompt)
        current_prompt = f"{context}\n\n### RESEARCH TASK ###\n{prompt}"
        
        self.logger.info("Executing research task...")
        
        # Multi-pass loop to handle tool calls
        max_passes = 3
        full_conversation = []
        
        for i in range(max_passes):
            response = self.execute(current_prompt)
            full_conversation.append(response)
            
            # Execute tools and get results
            result_with_tools = self.parse_and_execute_tools(response)
            
            # If tools were executed, feed the results back to the model
            if "### Tool Execution Results ###" in result_with_tools:
                tool_output = result_with_tools.split("### Tool Execution Results ###")[-1]
                current_prompt = f"### PREVIOUS ATTEMPT ###\n{response}\n\n### Tool Execution Results ###\n{tool_output}\n\n### INSTRUCTIONS ###\nPlease acknowledge the tool results and provide your final confirmation or next steps based on the actual data."
                continue
            else:
                # No more tools called, we are done
                break
                
        # Final Response
        final_response = full_conversation[-1]
        
        # Log to Obsidian
        self.memory.log_memory(prompt, "\n\n".join(full_conversation), self.model_name, agent_name=self.agent_name)

        return final_response
