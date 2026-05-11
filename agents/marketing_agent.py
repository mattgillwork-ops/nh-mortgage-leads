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
        """Execute a marketing/creative task with recursive tool execution."""
        context = self.memory.get_context(query=prompt)
        current_prompt = f"{context}\n\n### MARKETING TASK ###\n{prompt}"
        
        self.logger.info("Executing marketing task...")
        
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
                current_prompt = f"### PREVIOUS ATTEMPT ###\n{response}\n\n### Tool Execution Results ###\n{tool_output}\n\n### INSTRUCTIONS ###\nPlease acknowledge the tool results and provide your final confirmation or next steps."
                continue
            else:
                # No more tools called, we are done
                break
                
        # Final Response
        final_response = full_conversation[-1]
        
        # Log to Obsidian
        self.memory.log_memory(prompt, "\n\n".join(full_conversation), self.model_name, agent_name=self.agent_name)

        return final_response
