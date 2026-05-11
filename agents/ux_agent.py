"""
UX/UI Design Agent ('Aria') for the Anti-Gravity Agent Ecosystem.
Specializes in premium aesthetics, CSS, and visual verification.
"""

from agents.base_agent import BaseAgent

class UXAgent(BaseAgent):
    """
    Aria is the UX/UI specialist. She:
    1. Researches modern design trends.
    2. Generates premium CSS and styled React components.
    3. Uses the <view_window /> tool to visually verify her work.
    """

    def __init__(self):
        super().__init__(agent_name="Aria (UX)", model_name="anti-ux")

    def run(self, prompt: str) -> str:
        # Aria always checks for visual context if possible
        # We can prepend a system instruction to encourage tool use
        system_instr = (
            "You are Aria, the Vision-Aware UX Designer. Your goal is to create premium, state-of-the-art web interfaces.\n"
            "OPERATING PROTOCOL:\n"
            "1. USE RESEARCH: Always incorporate modern design tokens (Glassmorphism, Neon accents, Sleek Dark Mode).\n"
            "2. VISUAL FEEDBACK: If you are iterating on an existing UI, use <view_window /> to see the current state.\n"
            "3. ACCESSIBILITY: Ensure high contrast and readable typography (Inter, Outfit, or Roboto).\n"
            "4. TOOL USE: Use <write_file> for CSS/JSX and <replace_file_content> for surgical edits."
        )
        
        # Initial execution
        response = self.execute(prompt, system_override=system_instr)
        
        # Process tools (like <view_window /> or <write_file />)
        response = self.parse_and_execute_tools(response)
        
        return response
