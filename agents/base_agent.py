import os
import json
import yaml
import logging
import re
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
import ollama

# Initial setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(name)s]: %(message)s')

# Smart Bridge: Detect if running inside Docker or on Host
def get_ollama_endpoint():
    if os.path.exists("/.dockerenv") or os.environ.get("DOCKER_CONTAINER"):
        return "http://host.docker.internal:11434"
    return "http://127.0.0.1:11434"

def resilience_module(max_retries=3):
    """Tiered Model Resilience: Primary -> Fallback -> Cloud Gate."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, prompt, *args, **kwargs):
            # Determine the model to use
            primary = self.config.get('model', {}).get('primary')
            fallback = self.config.get('model', {}).get('fallback')
            
            failures = 0
            active_model = primary
            
            while failures < max_retries:
                try:
                    # Inject the active model into the function call
                    kwargs['active_model'] = active_model
                    return func(self, prompt, *args, **kwargs)
                except Exception as e:
                    failures += 1
                    self.logger.warning(f"[{self.agent_id}] Execution failed ({failures}/{max_retries}): {e}")
                    
                    if failures == 1 and fallback and self._check_availability(fallback):
                        self.logger.info(f"[{self.agent_id}] Switching to fallback model: {fallback}")
                        active_model = fallback
                    elif failures >= max_retries:
                        self.logger.error(f"[{self.agent_id}] All local models failed. Triggering Cloud Gate...")
                        return self.cloud_fallback(prompt)
                    
                    # Small backoff
                    import time
                    time.sleep(1)
            
            return "ERROR: Resilience loop exhausted."
        return wrapper
    return decorator

class MemoryManager:
    """v3 Memory Governance: 15-field schema and LTM proposals."""
    def __init__(self, agent_id, vault_path):
        self.agent_id = agent_id
        self.vault_path = vault_path
        self.proposal_path = os.path.join(vault_path, "Proposals")
        os.makedirs(self.proposal_path, exist_ok=True)

    def get_context(self, query):
        # Simplified context retrieval for now
        return "### CONTEXT: v3 Ecosystem Hardened Foundations active ###"

    def log_memory(self, prompt, response, model, agent_name, task_id=None, confidence=0.9):
        timestamp = datetime.now().isoformat()
        mem_type = "short_term"
        
        frontmatter = {
            "title": f"Task: {prompt[:30]}...",
            "memory_type": mem_type,
            "source_agent": self.agent_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            "confidence_level": confidence,
            "status": "active",
            "model_used": model
        }
        
        entry = f"---\n{yaml.dump(frontmatter)}---\n\n### PROMPT ###\n{prompt}\n\n### RESPONSE ###\n{response}"
        filename = f"{timestamp.replace(':','-')}_{self.agent_id}.md"
        
        log_dir = os.path.join(self.vault_path, "Memory_Logs")
        os.makedirs(log_dir, exist_ok=True)
        
        try:
            with open(os.path.join(log_dir, filename), 'w', encoding='utf-8') as f:
                f.write(entry)
        except Exception as e:
            logging.error(f"Failed to log memory: {e}")

class BaseAgent:
    """Antigravity v3.8 Sovereign Foundation - 100% Local Web Intelligence."""
    def __init__(self, agent_name, agent_id):
        self.agent_name = agent_name
        self.agent_id = agent_id
        self.logger = logging.getLogger(agent_id)
        
        # Explicit Client Bridge
        self.endpoint = get_ollama_endpoint()
        self.client = ollama.Client(host=self.endpoint)
        self.logger.info(f"Ollama Client initialized at {self.endpoint}")

        # Load configuration from registry
        self.config = self._resolve_identity()
        self.model_name = self.config.get('model', {}).get('primary', 'qwen2.5:7b')
        self.authorized_tools = self.config.get('permissions', {}).get('tools', [])
        
        # Cloud dependencies REMOVED to enforce sovereignty
        self.genai_client = None
        
        # Initialize Memory
        self.vault_path = os.path.join(os.getcwd(), "tru")
        self.memory = MemoryManager(agent_id, self.vault_path)

    def _resolve_identity(self):
        registry_path = os.path.join(os.getcwd(), "agent_registry.yaml")
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry = yaml.safe_load(f)
            return registry.get('agents', {}).get(self.agent_id, {})
        except Exception as e:
            self.logger.error(f"Failed to load registry: {e}")
            return {}

    def _check_availability(self, model_name: str) -> bool:
        if model_name.startswith("openai:"):
            return True
        try:
            installed = [m.model for m in self.client.list().models]
            return any(model_name in name for name in installed)
        except Exception as e:
            self.logger.debug(f"Availability check failed: {e}")
            return False

    def cloud_fallback(self, prompt: str) -> str:
        """Emergency Cloud Gate: Blocked in Sovereign Mode."""
        self.logger.error(f"[{self.agent_id}] SOVEREIGNTY VIOLATION PREVENTED. Cloud fallback is DISABLED.")
        return "ERROR: Cloud fallback is disabled in Sovereign Mode. Local models must be used."

    def parse_and_execute_tools(self, response: str) -> str:
        """v4 Sovereign Firewall: Enforce authorized tools and EXECUTE using local scripts."""
        tool_pattern = re.compile(r"TOOL:\s*(\w+)(?:\((.*?)\))?", re.IGNORECASE)
        tool_matches = tool_pattern.findall(response)
        
        if not tool_matches:
            return response
            
        final_response = response
        for tool_name, tool_args in tool_matches:
            if f"--- TOOL OUTPUT ({tool_name}) ---" in response:
                continue

            if tool_name not in self.authorized_tools:
                self.logger.error(f"SECURITY ALERT: Blocked unauthorized tool '{tool_name}' from agent '{self.agent_id}'")
                return f"ERROR: Unauthorized tool call detected: {tool_name}. Access denied by Firewall."

            self.logger.info(f"[{self.agent_id}] Executing whitelisted tool: {tool_name}")
            
            tool_output = ""
            try:
                if tool_name == "search_the_web":
                    from tools.web_search import web_search
                    query = tool_args.strip("'\"") if tool_args else ""
                    tool_output = web_search(query)
                elif tool_name == "browser_action" or tool_name == "extract_seo":
                    import subprocess
                    import sys
                    # Wrap simple string args into JSON for browser_skill
                    cmd_json = tool_args if tool_args.strip().startswith("{") else json.dumps({"action": "navigate", "url": tool_args.strip("'\"")})
                    result = subprocess.run(
                        [sys.executable, "tools/browser_skill.py", cmd_json],
                        capture_output=True, text=True, timeout=90
                    )
                    tool_output = result.stdout if result.returncode == 0 else f"[Browser Error] {result.stderr}"
                elif tool_name == "read_file":
                    from tools.file_manager import read_file
                    path = tool_args.strip("'\"") if tool_args else ""
                    if ".." in path or path.startswith("/") or (len(path) > 1 and path[1] == ":"):
                         tool_output = "[SECURITY ERROR] Path traversal or absolute path detected. Access denied."
                    else:
                        tool_output = read_file(path)
                elif tool_name == "list_dir":
                    from tools.file_manager import list_dir
                    path = tool_args.strip("'\"") if tool_args else "."
                    tool_output = list_dir(path)
                elif tool_name == "write_file":
                    from tools.file_manager import write_file
                    import ast
                    try:
                        parsed = ast.literal_eval(f"({tool_args})")
                        if isinstance(parsed, tuple) and len(parsed) >= 2:
                            path = parsed[0].strip()
                            content = parsed[1]
                        else:
                            path = tool_args.strip("'\"")
                            content = ""
                    except Exception:
                        parts = tool_args.split(",", 1)
                        path = parts[0].strip("'\" ")
                        content = parts[1].strip("'\" ") if len(parts) > 1 else ""
                    
                    if ".." in path or path.startswith("/") or (len(path) > 1 and path[1] == ":"):
                         tool_output = "[SECURITY ERROR] Path traversal or absolute path detected. Access denied."
                    else:
                         tool_output = write_file(path, content)
                elif tool_name == "replace_file_content":
                    from tools.file_manager import replace_file_content
                    import ast
                    try:
                        parsed = ast.literal_eval(f"({tool_args})")
                        if isinstance(parsed, tuple) and len(parsed) >= 3:
                            path = parsed[0].strip()
                            target = parsed[1]
                            replacement = parsed[2]
                        else:
                            path = ""
                            target = ""
                            replacement = ""
                    except Exception:
                        path = ""
                        target = ""
                        replacement = ""
                        
                    if ".." in path or path.startswith("/") or (len(path) > 1 and path[1] == ":"):
                         tool_output = "[SECURITY ERROR] Path traversal or absolute path detected. Access denied."
                    elif not path or not target:
                         tool_output = "[FileManager ERROR] Invalid parameters for replace_file_content."
                    else:
                         tool_output = replace_file_content(path, target, replacement)
                else:
                    tool_output = f"[Error: Tool '{tool_name}' logic not yet mapped in BaseAgent. Current whitelist: {self.authorized_tools}]"
            except Exception as e:
                tool_output = f"[Error executing tool '{tool_name}': {e}]"
            
            final_response += f"\n\n--- TOOL OUTPUT ({tool_name}) ---\n{tool_output}\n"
            
        return final_response

    def run(self, prompt: str) -> str:
        """Standard entry point for all agents."""
        response = self.execute(prompt)
        response = self.parse_and_execute_tools(response)
        self.memory.log_memory(prompt, response, self.model_name, self.agent_name)
        return response

    @resilience_module(max_retries=3)
    def execute(self, prompt: str, active_model: str = None, **kwargs) -> str:
        """Execute with resilience via explicit client."""
        ctx = self.config.get('context', 4096)
        current_date = datetime.now().strftime("%B %d, %Y")
        system_injection = f"\n\n[SYSTEM INFO: Current Date is {current_date}]\n"
        
        if active_model and active_model.startswith("openai:"):
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "ERROR: OPENAI_API_KEY is not set in .env"
            
            openai_client = openai.OpenAI(api_key=api_key)
            model_id = active_model.split(":")[1]
            
            try:
                response_format = {"type": "json_object"} if kwargs.get('json_mode') else {"type": "text"}
                messages = [{'role': 'user', 'content': system_injection + prompt}]
                if kwargs.get('json_mode') and "json" not in prompt.lower():
                    messages[0]['content'] += "\nPlease format your response in JSON."
                
                response = openai_client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    response_format=response_format
                )
                return response.choices[0].message.content
            except Exception as e:
                self.logger.warning(f"OpenAI unavailable ({type(e).__name__}): {e}")
                self.logger.info(f"[{self.agent_id}] Falling back to local model...")
                raise  # Triggers resilience_module fallback to local model

        chat_format = 'json' if kwargs.get('json_mode') else ''
        
        response = self.client.chat(
            model=active_model, 
            messages=[{'role': 'user', 'content': system_injection + prompt}],
            options={"num_ctx": ctx},
            format=chat_format
        )
        return response['message']['content']
