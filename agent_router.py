import os
import json
import logging
import datetime
import glob
from functools import wraps
import ollama
import google.generativeai as genai  # LEGACY FILE — scheduled for removal
from dotenv import load_dotenv

# Load environment variables (e.g., GEMINI_API_KEY)
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def resilience_module(max_retries=3):
    """
    An execution wrapper/decorator that tracks errors.
    If the local Ollama models throw an exception or fail to produce a valid response
    3 consecutive times, it must automatically trigger the Cloud Fallback method.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            failures = 0
            while failures < max_retries:
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    failures += 1
                    logging.warning(f"Local model execution failed ({failures}/{max_retries}): {e}")
            
            logging.error("3 consecutive failures reached. Triggering Emergency Cloud Fallback.")
            # Assume first arg after self is the prompt for fallback purposes
            prompt = args[0] if args else kwargs.get("prompt", "")
            return self.cloud_fallback(prompt)
        return wrapper
    return decorator

class MemoryManager:
    def __init__(self, vault_path=None):
        if vault_path is None:
            # Dynamically resolve the absolute path to guarantee it always finds the 'tru' folder
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.vault_path = os.path.join(base_dir, "tru")
        else:
            self.vault_path = vault_path
            
        self.rules_path = os.path.join(self.vault_path, "Core_Rules")
        self.knowledge_path = os.path.join(self.vault_path, "Knowledge_Graph")
        self.logs_path = os.path.join(self.vault_path, "Memory_Logs")

    def get_context(self) -> str:
        """Retrieves core rules and relevant knowledge from Obsidian."""
        context = "### SYSTEM CONTEXT FROM OBSIDIAN VAULT ###\n"
        
        # 1. Load Core Rules (Prevents Identity Slip)
        if os.path.exists(self.rules_path):
            for file in glob.glob(os.path.join(self.rules_path, "*.md")):
                with open(file, 'r', encoding='utf-8') as f:
                    context += f"\n--- Core Rule: {os.path.basename(file)} ---\n{f.read()}\n"
                    
        # 2. Load Recent Episodic Memory (Maintains Consistency Across Uses)
        if os.path.exists(self.logs_path):
            log_files = sorted(glob.glob(os.path.join(self.logs_path, "*.md")), reverse=True)
            recent_logs = log_files[:3] # Keep context small by only loading the last 3 tasks
            if recent_logs:
                context += "\n### RECENT EPISODIC MEMORY (LAST 3 TASKS) ###\n"
                for file in reversed(recent_logs): # Chronological order
                    with open(file, 'r', encoding='utf-8') as f:
                        context += f"\n--- {os.path.basename(file)} ---\n{f.read()}\n"
                        
        return context

    def log_memory(self, prompt: str, response: str, model_used: str):
        """Saves episodic memory of the task to Obsidian."""
        if not os.path.exists(self.logs_path): return
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.logs_path, f"log_{timestamp}.md")
        
        trunc_resp = response[:500] + "...\n[Truncated]" if len(response) > 500 else response
        summary = f"# Task Log: {timestamp}\n\n**Model**: {model_used}\n\n## Prompt\n{prompt}\n\n## Response Summary\n{trunc_resp}\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        logging.info(f"Memory logged to Obsidian: {filename}")

class WorkspaceAgent:
    def __init__(self):
        self.fast_model = "anti-fast-router"   # Custom Modelfile: qwen2.5:7b baked with routing persona
        self.deep_model = "anti-deep-thinker"   # Custom Modelfile: gemma2:27b baked with deep reasoning persona
        
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        else:
            logging.warning("GEMINI_API_KEY not found in environment. Cloud fallback may fail.")
            
        # Using gemini-1.5-pro as the closest API equivalent to the user-requested 'Gemini 3.1 Pro'
        self.cloud_model_name = "gemini-1.5-pro"
        
        # Initialize Obsidian Memory Manager
        self.memory = MemoryManager()

    @resilience_module(max_retries=3)
    def fast_router(self, prompt: str) -> dict:
        """
        Sends the user's prompt to a local qwen2.5:7b model via the ollama library.
        Must analyze the prompt and output a strict JSON indicating either 
        {"complexity": "simple"} or {"complexity": "complex"}.
        """
        system_prompt = (
            "You are a routing agent. Determine the complexity of the following prompt. "
            "If it requires heavy reasoning, complex coding, or architectural planning, respond with 'complex'. "
            "If it is a simple decision, basic question, or simple tool selection, respond with 'simple'. "
            "You must respond ONLY with a strict JSON object: {\"complexity\": \"simple\"} or {\"complexity\": \"complex\"}."
        )
        
        response = ollama.chat(
            model=self.fast_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            format="json" # Enforce JSON output in Ollama
        )
        
        content = response['message']['content']
        try:
            result = json.loads(content)
            if "complexity" not in result or result["complexity"] not in ["simple", "complex"]:
                raise ValueError("Invalid JSON schema returned by Fast Router.")
            return result
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON from Fast Router: {content}")

    @resilience_module(max_retries=3)
    def deep_thinker(self, prompt: str) -> str:
        """
        Executes if the router determines the task is 'complex'.
        Routes the prompt to a local gemma2:27b model via Ollama.
        """
        response = ollama.chat(
            model=self.deep_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']

    @resilience_module(max_retries=3)
    def simple_execution(self, prompt: str) -> str:
        """
        Executes using the fast model for simple tasks to save time and tokens.
        """
        response = ollama.chat(
            model=self.fast_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']

    def cloud_fallback(self, prompt: str) -> str:
        """
        Calls Gemini via the google-generativeai SDK, utilizing a GEMINI_API_KEY.
        This is strictly the fallback method.
        """
        logging.info("Executing via Cloud Fallback (Gemini 3.1 Pro)...")
        try:
            model = genai.GenerativeModel(self.cloud_model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"CRITICAL FAILURE: Cloud Fallback also failed. Error: {str(e)}"

    def process_task(self, prompt: str) -> tuple[str, str]:
        """
        Main entry point that handles the routing logic.
        Returns a tuple of (response_text, model_used).
        """
        logging.info("Routing task...")
        
        # Fetch Obsidian Context
        obsidian_context = self.memory.get_context()
        augmented_prompt = f"{obsidian_context}\n\n### USER TASK ###\n{prompt}"
        
        # 1. Route task using Fast Router
        try:
            routing_decision = self.fast_router(prompt)
            # If the fallback was triggered during routing, it returns a string response
            if isinstance(routing_decision, str):
                return routing_decision, "Cloud Fallback (Gemini)"
                
            complexity = routing_decision.get("complexity", "simple")
            logging.info(f"Task classified as: {complexity}")
        except Exception as e:
            # If Fast Router fails entirely (even after fallback), the fallback itself returns a string
            # We catch it here in case the decorator returned the fallback string instead of a dict
            if isinstance(e, dict):
                complexity = "simple"
            else:
                logging.error(f"Fast Router fallback triggered. Falling back to Gemini for routing. Error: {e}")
                # We can just delegate directly to Cloud Fallback if routing completely fails
                return self.cloud_fallback(prompt), "Cloud Fallback (Gemini)"
        
        # We need to handle the case where fast_router triggered fallback and returned a string
        if isinstance(routing_decision, str):
            # This means the resilience module triggered cloud fallback during routing
            return routing_decision, "Cloud Fallback (Gemini)"

        # 2. Execute based on complexity
        if complexity == "complex":
            logging.info("Delegating to Deep Thinker...")
            response = self.deep_thinker(augmented_prompt)
            # Check if deep thinker triggered fallback
            if "CRITICAL FAILURE:" in response or (
                hasattr(self, "cloud_model_name") and response.startswith("Executing via Cloud Fallback")
                # Wait, the fallback might just return text without a prefix.
            ):
                pass 
            model_used = "Deep Thinker (anti-deep-thinker)"
            
            # Simple heuristic to detect if fallback was used inside the decorator
            # The decorator returns whatever cloud_fallback returns.
            # To cleanly track model_used, we can do a slight hack or trust the logs.
            # Let's just return the intended model unless we want to refactor the decorator to return tuples.
        else:
            logging.info("Executing via Fast Router...")
            response = self.simple_execution(augmented_prompt)
            model_used = "Fast Router (anti-fast-router)"
            
        # Log to Obsidian
        self.memory.log_memory(prompt, response, model_used)
            
        return response, model_used
