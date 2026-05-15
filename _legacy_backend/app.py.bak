import os
import asyncio
import json
import glob
import re
import subprocess
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "tru", "Memory_Logs")
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def serve_dashboard():
    """Serves the main Command Center UI."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

def parse_log(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Extract Agent Name
        agent_match = re.search(r'\*\*Model\*\*:\s*(.*?)\n', content)
        agent = agent_match.group(1).strip() if agent_match else "System"
        
        # Extract Prompt Snippet
        prompt_match = re.search(r'## Prompt\n(.*?)(?:\n##|$)', content, re.DOTALL)
        prompt = prompt_match.group(1).strip() if prompt_match else ""
        prompt_snippet = prompt[:100] + "..." if len(prompt) > 100 else prompt
        
        # Extract Response Snippet
        response_match = re.search(r'## Response Summary\n(.*)', content, re.DOTALL)
        response = response_match.group(1).strip() if response_match else content
        # Strip some markdown for a cleaner snippet
        response_clean = re.sub(r'<[^>]+>|#|\*|`', '', response).strip()
        response_snippet = response_clean[:150] + "..." if len(response_clean) > 150 else response_clean
        
        return {
            "filename": os.path.basename(filepath),
            "agent": agent,
            "prompt": prompt_snippet,
            "response": response_snippet
        }
    except Exception as e:
        return {"filename": os.path.basename(filepath), "agent": "Unknown", "prompt": "Error parsing log", "response": str(e)}

async def get_latest_logs():
    """Returns the parsed content of the most recent logs."""
    files = sorted(glob.glob(os.path.join(LOG_DIR, "log_*.md")), key=os.path.getmtime)
    logs = []
    for f in files[-10:]: # Last 10 logs for better context
        parsed = parse_log(f)
        if parsed:
            logs.append(parsed)
    return logs

@app.get("/stream")
async def stream_logs(request: Request):
    async def event_generator():
        # 1. Send initial logs
        initial_logs = await get_latest_logs()
        for log in initial_logs:
            yield f"data: {json.dumps(log)}\n\n"
        
        # 2. Watch for new logs
        known_files = set(glob.glob(os.path.join(LOG_DIR, "log_*.md")))
        while True:
            if await request.is_disconnected():
                break
            
            current_files = set(glob.glob(os.path.join(LOG_DIR, "log_*.md")))
            new_files = current_files - known_files
            
            for f in new_files:
                parsed = parse_log(f)
                if parsed:
                    yield f"data: {json.dumps(parsed)}\n\n"
            
            known_files = current_files
            await asyncio.sleep(2) # Poll every 2 seconds

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/health")
async def health():
    return {"status": "online", "agent_count": 7, "vault_path": LOG_DIR}

@app.get("/api/document/{doc_name}")
async def get_document(doc_name: str):
    """Serve specific markdown documents from the workspace root."""
    allowed_docs = ["PHASE_REVIEW.md", "FUTURE_PROJECTS.md", "AGENT_USE_CASES.md", "WORKSPACE_AI_RULES.md", "CURRENT_TASKS.md", "master_business_plan.md", "POSSIBLE_PROJECTS.md"]
    if doc_name not in allowed_docs:
        return {"error": "Document not allowed or not found"}
        
    doc_path = os.path.join(BASE_DIR, doc_name)
    if os.path.exists(doc_path):
        with open(doc_path, "r", encoding="utf-8") as f:
            return {"content": f.read()}
    return {"error": f"File {doc_name} does not exist yet."}

@app.post("/api/run_health_check")
async def run_health_check():
    """Executes the selfcheck.py script and returns the output."""
    try:
        script_path = os.path.join(BASE_DIR, "selfcheck.py")
        result = subprocess.run(
            ["python", script_path, "--quick"], 
            capture_output=True, 
            text=True, 
            timeout=60
        )
        
        # Determine success from output
        success = "STATUS: ALL SYSTEMS OPERATIONAL" in result.stdout
        
        return {
            "success": success,
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {"success": False, "output": f"Failed to execute health check: {str(e)}", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
