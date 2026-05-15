import ollama
try:
    print("Testing Ollama library connection...")
    models = ollama.list()
    print(f"Success! Found {len(models.get('models', []))} models.")
except Exception as e:
    print(f"Failure! Error: {e}")
