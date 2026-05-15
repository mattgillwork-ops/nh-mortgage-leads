import ollama
import yaml
import os

def verify_agents():
    registry_path = 'model_registry.yaml'
    if not os.path.exists(registry_path):
        print("Model registry not found.")
        return

    with open(registry_path, 'r') as f:
        config = yaml.safe_load(f)
    
    agents = config.get('agents', {})
    
    print("| Agent | Primary Model | Fallback Model | Status |")
    print("|-------|---------------|----------------|--------|")
    
    for name, models in agents.items():
        primary = models.get('primary')
        fallback = models.get('fallback', 'N/A')
        
        try:
            # Check if model exists in Ollama
            ollama.show(primary)
            status = "ONLINE"
        except Exception:
            status = "MISSING"
            
        print(f"| {name.capitalize()} | {primary} | {fallback} | {status} |")

if __name__ == "__main__":
    verify_agents()
