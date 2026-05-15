---
title: "VRAM Optimization Strategy for 14B Models"
memory_type: "infrastructure"
source_agent: "dax"
created_at: "2026-05-13 15:30:00"
updated_at: "2026-05-13 15:31:00"
task_id: "INFRA-404"
confidence_level: 0.95
status: "approved"
validated_by: "vera"
validation_notes: "Technical logic confirmed; aligns with RTX 5080 hardware boundaries."
related_files: ["docker-compose.yml", "selfcheck.py"]
related_agents: ["alex", "dax"]
tags: ["ollama", "vram", "performance"]
---

# Summary
To prevent VRAM spillover on 16GB cards, concurrent 14B model loading must be limited to 1 active instance. Subsequent agents should utilize 7B fallbacks if the primary 14B slot is occupied.

# Evidence & References
- Ollama `num_gpu` logs indicate 9.2GB VRAM usage per 14B-Q4_K_M instance.
- System RAM offloading detected at 11.5GB total VRAM usage.
