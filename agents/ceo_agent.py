"""
CEO Orchestrator Agent for the Anti-Gravity Agent Ecosystem.
Receives tasks, classifies them, delegates to sub-agents, and verifies results.
"""

import os
import json
import logging
import datetime
from agents.base_agent import BaseAgent
from tools.git_manager import GitManager


class CEOAgent(BaseAgent):
    """
    The CEO is the master orchestrator. It:
    1. Receives a user task
    2. Classifies it and decides which sub-agent handles it
    3. Delegates the work
    4. Sends the result to the Verifier
    5. Returns the final output (or retries on FAIL)
    """

    def __init__(self, sub_agents: dict = None):
        super().__init__(agent_name="Alex (CEO)", model_name="anti-ceo")
        self.sub_agents = sub_agents or {}
        self.max_verification_retries = 2

    def classify_task(self, prompt: str) -> dict:
        """
        Use the CEO model to classify the task and decide delegation.
        Returns a dict like: {"task_type": "code", "delegate_to": "coder", ...}
        """
        result = self.execute(prompt, json_mode=True)

        # Handle case where resilience module returned a fallback string
        if isinstance(result, str) and result.startswith("CRITICAL FAILURE"):
            return {"task_type": "general", "delegate_to": "self", "sub_task": prompt, "priority": "high"}

        try:
            parsed = json.loads(result)
            # Validate required fields
            required = ["task_type", "delegate_to", "sub_task"]
            if not all(k in parsed for k in required):
                self.logger.warning(f"CEO classification missing fields, defaulting to self. Got: {parsed}")
                return {"task_type": "general", "delegate_to": "self", "sub_task": prompt, "priority": "medium"}
            return parsed
        except json.JSONDecodeError:
            self.logger.warning(f"CEO failed to parse classification JSON: {result[:100]}")
            return {"task_type": "general", "delegate_to": "self", "sub_task": prompt, "priority": "medium"}

    def delegate(self, classification: dict) -> tuple[str, str]:
        """
        Delegate the task to the appropriate sub-agent.
        Returns (response, agent_name).
        """
        delegate_to = classification.get("delegate_to", "self")
        sub_task = classification.get("sub_task", "")

        if delegate_to == "self":
            # CEO handles simple tasks directly
            self.logger.info("Handling task directly (general/simple).")
            response = self.execute(sub_task)
            return response, "CEO (anti-ceo)"

        if delegate_to in self.sub_agents:
            agent = self.sub_agents[delegate_to]
            
            # Interactive Approval for Code Tasks (skip on retries)
            if classification.get("task_type") == "code" and not classification.get("_skip_approval"):
                plan = classification.get("implementation_plan", "No plan provided.")
                
                # Harden against list format from model
                if isinstance(plan, list):
                    plan = "\n".join(str(item) for item in plan)
                
                print("\n" + "=" * 56)
                print("  [ALEX] IMPLEMENTATION PLAN:")
                print("  " + "\n  ".join(str(plan).split("\n")))
                print("=" * 56 + "\n")
                
                while True:
                    # Optional: skip interactive prompt if --auto-approve is in sys.argv
                    import sys
                    if "--auto-approve" in sys.argv:
                        print("Auto-approving plan due to --auto-approve flag.")
                        break
                        
                    choice = input(f"Approve this plan for the {delegate_to.capitalize()} agent? [Y/N]: ").strip().lower()
                    if choice == 'y':
                        break
                    elif choice == 'n':
                        feedback = input("Please provide feedback to Alex: ").strip()
                        self.logger.info("Plan rejected. Generating revised plan...")
                        new_prompt = f"Original task: {sub_task}\nUser feedback on plan: {feedback}\nGenerate a revised sub_task and implementation_plan."
                        new_class = self.classify_task(new_prompt)
                        # Merge the revised plan/subtask into a code task format
                        new_class["task_type"] = "code"
                        new_class["delegate_to"] = delegate_to
                        return self.delegate(new_class)
                    else:
                        print("Please enter 'Y' or 'N'.")

            self.logger.info(f"Delegating to {delegate_to} agent...")
            
            # Phantom Plan Fix: Inject the plan into the prompt sent to the sub-agent
            full_prompt = sub_task
            plan = classification.get("implementation_plan")
            if plan:
                full_prompt += f"\n\n### IMPLEMENTATION PLAN ###\n{plan}"
                
            response = agent.run(full_prompt)
            return response, f"{delegate_to.capitalize()} ({agent.model_name})"
        else:
            self.logger.warning(f"Unknown agent '{delegate_to}'. CEO handling directly.")
            response = self.execute(sub_task)
            return response, "CEO (anti-ceo)"

    def verify(self, original_task: str, agent_output: str) -> dict:
        """
        Send the output to the Verifier agent for quality check.
        Returns the verifier's verdict dict.
        """
        verifier = self.sub_agents.get("verifier")
        if not verifier:
            self.logger.warning("No Verifier agent registered. Skipping verification.")
            return {"verdict": "PASS", "confidence": 0.5, "issues": [], "recommendations": [],
                    "summary": "No verifier available — auto-passed."}

        verification_prompt = (
            f"## Original Task\n{original_task}\n\n"
            f"## Agent Output\n{agent_output}\n\n"
            f"Please verify whether the output fully satisfies the original task."
        )
        result = verifier.run(verification_prompt)

        try:
            # DeepSeek-R1 wraps its reasoning in <think> tags, extract JSON after it
            if "<think>" in result:
                # Get content after </think>
                result = result.split("</think>")[-1].strip()

            parsed = json.loads(result)
            return parsed
        except json.JSONDecodeError:
            self.logger.warning(f"Verifier output was not valid JSON: {result[:200]}")
            return {"verdict": "PASS", "confidence": 0.3, "issues": ["Verifier output unparseable"],
                    "recommendations": [], "summary": "Could not parse verifier output — auto-passed with low confidence."}

    def generate_phase_review(self, task: str, response: str, verification: dict):
        """Generates a PHASE_REVIEW.md in the workspace root."""
        self.logger.info("Generating Phase Review...")
        review_content = (
            f"# Phase Review: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"## Task Overview\n{task[:200]}...\n\n"
            f"## Key Accomplishments\n- {verification.get('summary', 'Task completed successfully.')}\n\n"
            f"## Issues Resolved during Iteration\n"
        )
        
        if verification.get('issues'):
            for issue in verification['issues']:
                review_content += f"- FIXED: {issue}\n"
        else:
            review_content += "- No major issues encountered.\n"
            
        review_content += f"\n## Hardware & Logic Optimizations\n- Model Used: {self.model_name}\n- Verification Confidence: {verification.get('confidence', 'N/A')}\n"
        
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            review_path = os.path.join(base_dir, "PHASE_REVIEW.md")
            with open(review_path, 'w', encoding='utf-8') as f:
                f.write(review_content)
            self.logger.info(f"Phase Review saved to {review_path}")
        except Exception as e:
            self.logger.error(f"Failed to save Phase Review: {e}")

    def run(self, prompt: str) -> tuple[str, str, dict]:
        """
        Full CEO pipeline:
        1. Classify the task
        2. Delegate to the right agent
        3. Verify the result
        4. Retry if verification fails (up to max_verification_retries)
        5. Return (final_response, model_used, verification_result)
        """
        self.logger.info("=" * 50)
        self.logger.info(f"CEO received task: {prompt[:80]}...")
        self.logger.info("=" * 50)

        # Augment prompt with Obsidian context
        obsidian_context = self.memory.get_context()

        # Step 1: Classify
        classification = self.classify_task(f"{obsidian_context}\n\nTask: {prompt}")
        self.logger.info(f"Classification: {json.dumps(classification, indent=2)}")

        # Step 2: Delegate
        response, model_used = self.delegate(classification)

        # Step 3: Verify (skip for "general" self-handled tasks)
        verification = {"verdict": "PASS", "summary": "Self-handled task — no verification needed."}
        if classification.get("delegate_to") != "self":
            retries = 0
            while retries < self.max_verification_retries:
                verification = self.verify(prompt, response)
                self.logger.info(f"Verification verdict: {verification.get('verdict', 'UNKNOWN')}")

                if verification.get("verdict") == "PASS":
                    # Step 3.5: Generate Phase Review
                    self.generate_phase_review(prompt, response, verification)
                    break

                # FAIL — retry with the same agent
                retries += 1
                self.logger.warning(f"Verification FAILED (attempt {retries}/{self.max_verification_retries})")
                self.logger.warning(f"Issues: {verification.get('issues', [])}")
                self.logger.warning(f"Recommendations: {verification.get('recommendations', [])}")

                # Build a retry prompt with the feedback while preserving the original task
                original_sub_task = classification.get("sub_task", prompt)
                plan = classification.get("implementation_plan", "")
                plan_text = f"\n\n### ORIGINAL IMPLEMENTATION PLAN ###\n{plan}" if plan else ""
                
                retry_prompt = (
                    f"Your previous output was rejected by our QA team. You must rewrite it.\n"
                    f"Original task instructions: {original_sub_task}{plan_text}\n\n"
                    f"### QA FEEDBACK TO FIX ###\n"
                    f"Issues found: {verification.get('issues', [])}\n"
                    f"Recommendations: {verification.get('recommendations', [])}\n"
                    f"Please fix the issues and produce a corrected output."
                )
                response, model_used = self.delegate({
                    **classification,
                    "sub_task": retry_prompt,
                    "_skip_approval": True
                })

        # Step 4: Selective Git Auto-Commit (safety net for file-writing agents)
        # Only commit when: a specialist agent ran AND the task passed verification.
        # Read-only tasks (research, analysis, general) are NOT committed.
        FILE_WRITING_AGENTS = {"coder", "devops", "ux"}
        if (
            classification.get("delegate_to") in FILE_WRITING_AGENTS
            and verification.get("verdict") == "PASS"
        ):
            try:
                agent_name = classification.get("delegate_to", "unknown").capitalize()
                task_summary = classification.get("sub_task", prompt)[:80].replace('"', "'")
                commit_msg = f"[Agent: {agent_name}] {task_summary}"
                git = GitManager()
                git.add_files()  # Stage all changed files
                result = git.commit(commit_msg)
                self.logger.info(f"Git safety commit: {result}")
            except Exception as e:
                # Non-fatal: if git fails, log it and keep going
                self.logger.warning(f"Git auto-commit skipped: {e}")

        # Step 5: Log to Obsidian
        self.memory.log_memory(prompt, response, model_used, agent_name=self.agent_name)

        return response, model_used, verification
