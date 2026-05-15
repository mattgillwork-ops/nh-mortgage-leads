---
title: "{{title}}"
memory_type: "{{short_term|long_term|project|research|infrastructure|design|brand|strategy|security|QA}}"
source_agent: "{{agent_id}}"
created_at: "{{timestamp}}"
updated_at: "{{timestamp}}"
task_id: "{{task_id}}"
confidence_level: 0.0
status: "proposed"
validated_by: "none"
validation_notes: "pending audit"
related_files: []
related_agents: []
tags: []
---

# Summary
{{concise_distilled_conclusion}}

# Evidence & References
- {{source_url_or_file}}
- {{observation_data}}

# Connections
- Agent: [[{{source_agent}}_MOC]]
- Task: [[Task_{{task_id}}]]
- Project: [[{{project_name}}]]

<!-- NO RAW CHAIN-OF-THOUGHT BELOW THIS LINE -->
