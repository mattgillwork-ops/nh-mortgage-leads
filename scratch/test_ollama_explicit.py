from ollama import Client
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
if not host.startswith("http"):
    host = f"http://{host}"

print(f"Testing Ollama connection to: {host}")
client = Client(host=host)

try:
    models = client.list()
    print(f"Success! Found {len(models.get('models', []))} models.")
except Exception as e:
    print(f"Failure! Error: {e}")
