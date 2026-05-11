"""
Base Agent infrastructure for the Anti-Gravity Agent Ecosystem.
Contains shared utilities: MemoryManager, resilience_module, and BaseAgent.
All specialized agents inherit from BaseAgent.
"""

import os
import json
import logging
import datetime
import re
import subprocess
import yaml
import chromadb
from chromadb.config import Settings
from functools import wraps
import ollama
from google import genai
from dotenv import load_dotenv
import pyautogui
import base64
from io import BytesIO
from PIL import Image

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(name)s]: %(message)s')

# Module-level flag to suppress duplicate warnings
_gemini_key_warned = False

# Module-level Gemini client (initialized once)
_gemini_client = None

def _get_gemini_client():
    """Returns a shared Gemini client instance, or None if no API key."""
    global _gemini_client, _gemini_key_warned
    if _gemini_client is not None:
        return _gemini_client
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        _gemini_client = genai.Client(api_key=api_key)
        return _gemini_client
    elif not _gemini_key_warned:
        logging.getLogger("BaseAgent").warning("GEMINI_API_KEY not found. Cloud fallback may fail.")
        _gemini_key_warned = True
    return None


def resilience_module(max_retries=3):
    """
    Decorator that wraps local Ollama calls with automatic retry + cloud fallback.
    If the local model fails 3 consecutive times, it triggers cloud_fallback().
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            failures = 0
            last_error = None
            while failures < max_retries:
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    failures += 1
                    last_error = e
                    self.logger.warning(f"Local model failed ({failures}/{max_retries}): {e}")

            self.logger.error(f"3 consecutive failures. Triggering Cloud Fallback.")
            prompt = args[0] if args else kwargs.get("prompt", "")
            return self.cloud_fallback(prompt)
        return wrapper
    return decorator
    return decorator


class MemoryManager:
    """Manages Obsidian-backed semantic memory (RAG) using ChromaDB."""

    def __init__(self, vault_path=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.vault_path = vault_path or os.path.join(base_dir, "tru")
        self.rules_path = os.path.join(self.vault_path, "Core_Rules")
        self.logs_path = os.path.join(self.vault_path, "Memory_Logs")
        self.db_path = os.path.join(self.vault_path, "vector_db")

        # Initialize ChromaDB (Local Persistent)
        self.chroma_client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name="episodic_memory",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Ensure directories exist
        os.makedirs(self.logs_path, exist_ok=True)
        os.makedirs(self.rules_path, exist_ok=True)

    def _get_embedding(self, text: str):
        """Generate embedding using Ollama's nomic-embed-text."""
        try:
            response = ollama.embeddings(model="nomic-embed-text", prompt=text)
            return response["embedding"]
        except Exception as e:
            logging.error(f"Embedding failure: {e}")
            return None

    def get_context(self, query: str = None) -> str:
        """Retrieves core rules and semantically relevant memory from Obsidian."""
        context = "### SYSTEM CONTEXT FROM OBSIDIAN VAULT ###\n"

        # 1. Load Core Rules (Mandatory)
        if os.path.exists(self.rules_path):
            import glob
            for file in glob.glob(os.path.join(self.rules_path, "*.md")):
                with open(file, 'r', encoding='utf-8') as f:
                    context += f"\n--- Core Rule: {os.path.basename(file)} ---\n{f.read()}\n"

        # 2. Semantic Memory Retrieval (RAG)
        if query and self.collection.count() > 0:
            embedding = self._get_embedding(query)
            if embedding:
                results = self.collection.query(
                    query_embeddings=[embedding],
                    n_results=5,
                    include=["documents", "metadatas"]
                )
                if results["documents"] and results["documents"][0]:
                    context += "\n### RELEVANT PAST MEMORIES (SEMANTIC SEARCH) ###\n"
                    for i, doc in enumerate(results["documents"][0]):
                        meta = results["metadatas"][0][i]
                        context += f"\n--- Memory ({meta.get('agent', 'unknown')} | {meta.get('date', '')}) ---\n{doc}\n"
        
        return context

    def log_memory(self, prompt: str, response: str, model_used: str, agent_name: str = "unknown"):
        """Saves episodic memory with YAML frontmatter and indexes it in the Vector DB."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.logs_path, f"log_{file_ts}.md")

        # Prepare Metadata
        metadata = {
            "agent": agent_name,
            "model": model_used,
            "date": timestamp,
            "task_type": "orchestration" if agent_name == "CEO" else "execution",
            "status": "completed"
        }

        # Truncate content for indexing to avoid context bloat
        clean_content = f"Task: {prompt}\nResult: {response[:2000]}"
        
        # 1. Save to Obsidian (File System)
        yaml_frontmatter = yaml.dump(metadata, default_flow_style=False)
        content = f"---\n{yaml_frontmatter}---\n\n# Task Log\n\n## Prompt\n{prompt}\n\n## Response\n{response}\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        # 2. Index in Vector DB
        embedding = self._get_embedding(clean_content)
        if embedding:
            self.collection.add(
                ids=[file_ts],
                embeddings=[embedding],
                documents=[clean_content],
                metadatas=[metadata]
            )
        
        logging.getLogger(agent_name).info(f"Episodic memory indexed: {filename}")


class BaseAgent:
    """
    Base class for all Anti-Gravity agents.
    Provides shared Ollama execution, cloud fallback, and memory integration.
    """

    def __init__(self, agent_name: str, model_name: str):
        self.agent_name = agent_name
        self.model_name = model_name
        self.logger = logging.getLogger(agent_name)
        self.workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Shared memory manager
        self.memory = MemoryManager()

        # Cloud fallback via the new google-genai SDK
        self.cloud_client = _get_gemini_client()
        self.cloud_model_name = "gemini-2.0-flash"

    @resilience_module(max_retries=3)
    def execute(self, prompt: str, system_override: str = None, json_mode: bool = False) -> str:
        """
        Execute a prompt against this agent's local Ollama model.
        Wrapped by the resilience module for automatic retry + fallback.
        """
        messages = []
        if system_override:
            messages.append({"role": "system", "content": system_override})
        messages.append({"role": "user", "content": prompt})

        kwargs = {"model": self.model_name, "messages": messages}
        if json_mode:
            kwargs["format"] = "json"

        # Support for vision (multimodal)
        if hasattr(self, "current_images") and self.current_images:
            # Find the last 'user' message and inject the images
            for msg in reversed(messages):
                if msg["role"] == "user":
                    msg["images"] = self.current_images
                    break
            # Clear images after use to prevent stale context
            self.current_images = []
        
        max_internal_retries = 2
        for attempt in range(max_internal_retries + 1):
            response = ollama.chat(**kwargs)
            content = response['message']['content']
            
            # Strict-Tool Enforcement: If output has python code block but no XML tool tags
            if not json_mode and "```python" in content and "<write_file" not in content and "<run_command" not in content and "<replace_file_content" not in content:
                if attempt < max_internal_retries:
                    self.logger.warning("Agent forgot XML tool tags. Forcing internal retry.")
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "user", "content": "SYSTEM ERROR: You wrote code but forgot the <write_file path='...'> tags. Please output your response again using the correct XML tags so the file can be saved."})
                    kwargs["messages"] = messages
                    continue
            
            return content
            
        return content

    def cloud_fallback(self, prompt: str) -> str:
        """Emergency cloud fallback via Gemini API (google-genai SDK)."""
        self.logger.info("Executing via Cloud Fallback (Gemini)...")
        try:
            if self.cloud_client is None:
                return "CRITICAL FAILURE: No GEMINI_API_KEY configured. Cloud fallback unavailable."
            response = self.cloud_client.models.generate_content(
                model=self.cloud_model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"CRITICAL FAILURE: Cloud Fallback also failed. Error: {str(e)}"

    def validate_path(self, path: str) -> str:
        """Ensures the path is within the workspace and sanitized."""
        full_path = os.path.abspath(os.path.join(self.workspace_root, path))
        if not full_path.lower().startswith(self.workspace_root.lower()):
            raise PermissionError(f"Access denied: {path} is outside the workspace.")
        if ".." in path or "~" in path:
            raise ValueError(f"Invalid path characters detected in: {path}")
        return full_path

    def reflect(self, prompt: str, failed_response: str, error_log: str) -> str:
        """The Reflection Phase: Agent critiques its own failure and generates a fix."""
        self.logger.info("Entering Reflection Phase (Self-Healing)...")
        reflection_prompt = f"""
### ORIGINAL TASK ###
{prompt}

### YOUR PREVIOUS ATTEMPT ###
{failed_response}

### TOOL ERRORS ENCOUNTERED ###
{error_log}

### INSTRUCTIONS ###
You encountered errors during tool execution. 
1. Identify the root cause of the error (e.g., wrong file path, syntax error, or placeholder use).
2. Explain how you will fix it.
3. Output the CORRECTED implementation using the XML tool tags.
"""
        return self.execute(reflection_prompt)

    def parse_and_execute_tools(self, response: str) -> str:
        """
        Parses XML-like tool tags from the agent's response and executes them.
        Supported tools: <write_file path="...">, <read_file path="..." />, <run_command>
        """
        from docker_runner import execute_in_sandbox
        
        output_log = []
        
        # 1. <write_file path="X"> content </write_file>
        write_pattern = re.compile(r'<write_file path=[\'"]([^\'"]+)[\'"]>(.*?)</write_file>', re.DOTALL)
        for match in write_pattern.finditer(response):
            path, content = match.groups()
            try:
                full_path = self.validate_path(path)
                
                # Core File Protection
                core_files = ["base_agent.py", "ceo_agent.py", "main.py", "qa_check.py"]
                if any(path.endswith(f) for f in core_files):
                    output_log.append(f"[TOOL ERROR] Core System files are locked. Use the <replace_file_content> tool instead of <write_file> for {path}.")
                    continue
                
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Shrinkage Monitor
                if os.path.exists(full_path):
                    old_size = os.path.getsize(full_path)
                    new_size = len(content.encode('utf-8'))
                    if old_size > 500 and new_size < (old_size * 0.5): # If it shrinks by more than 50%
                        output_log.append(f"[TOOL ERROR] CRITICAL WARNING: Major code deletion detected. {path} would shrink from {old_size} to {new_size} bytes. Overwrite blocked. Use <replace_file_content> instead.")
                        continue
                        
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content.strip() + '\n')
                output_log.append(f"[TOOL OK] Wrote file: {path}")
            except Exception as e:
                output_log.append(f"[TOOL ERROR] Failed to write {path}: {e}")

        # 2. <read_file path="X" />
        read_pattern = re.compile(r'<read_file path=[\'"]([^\'"]+)[\'"]\s*/>')
        for match in read_pattern.finditer(response):
            path = match.group(1)
            try:
                full_path = self.validate_path(path)
                    
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                output_log.append(f"[TOOL OK] Read file {path}:\n{content[:500]}...\n")
            except Exception as e:
                output_log.append(f"[TOOL ERROR] Failed to read {path}: {e}")

        # 3. <replace_file_content path="X"> <target>Y</target> <replacement>Z</replacement> </replace_file_content>
        replace_pattern = re.compile(r'<replace_file_content path=[\'"]([^\'"]+)[\'"]>\s*<target>(.*?)</target>\s*<replacement>(.*?)</replacement>\s*</replace_file_content>', re.DOTALL)
        for match in replace_pattern.finditer(response):
            path, target, replacement = match.groups()
            try:
                full_path = self.validate_path(path)
                
                if not os.path.exists(full_path):
                    output_log.append(f"[TOOL ERROR] Failed to edit {path}: File does not exist.")
                    continue
                
                with open(full_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                if target not in file_content:
                    target_stripped = target.strip()
                    if target_stripped and target_stripped in file_content:
                        new_content = file_content.replace(target_stripped, replacement.strip())
                    else:
                        output_log.append(f"[TOOL ERROR] Failed to edit {path}: <target> text not found in file. Ensure exact match without placeholders.")
                        continue
                else:
                    new_content = file_content.replace(target, replacement)
                    
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                output_log.append(f"[TOOL OK] Successfully edited file: {path}")
            except Exception as e:
                output_log.append(f"[TOOL ERROR] Failed to edit {path}: {e}")

        # 4. <run_command> cmd </run_command>
        run_pattern = re.compile(r'<run_command>(.*?)</run_command>', re.DOTALL)
        for match in run_pattern.finditer(response):
            cmd = match.group(1).strip()
            try:
                output = execute_in_sandbox(cmd)
                output_log.append(f"[TOOL OK] Executed command via Sandbox: {cmd}\nOutput:\n{output[:500]}")
            except Exception as e:
                output_log.append(f"[TOOL ERROR] Failed to run command: {e}")

        # 5. <view_window />
        view_pattern = re.compile(r'<view_window\s*/>')
        if view_pattern.search(response):
            try:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                visual_logs = os.path.join(base_dir, "tru", "Visual_Logs")
                os.makedirs(visual_logs, exist_ok=True)
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(visual_logs, filename)
                
                # Take screenshot
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
                
                # Convert to Base64 for the agent's vision
                buffered = BytesIO()
                screenshot.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                # Store in agent instance for the NEXT execute call or immediate feedback
                if not hasattr(self, "current_images"):
                    self.current_images = []
                self.current_images.append(img_str)
                
                output_log.append(f"[TOOL OK] Screenshot captured: {filename}. I can now 'see' the current window state.")
            except Exception as e:
                output_log.append(f"[TOOL ERROR] Failed to capture window: {e}")

        if output_log:
            return response + "\n\n### Tool Execution Results ###\n" + "\n".join(output_log)
        return response

    def run(self, prompt: str) -> str:
        """
        Main execution method. Subclasses should override this 
        to implement agent-specific behavior.
        """
        raise NotImplementedError("Subclasses must implement run()")
