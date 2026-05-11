# System Learnings

This file acts as a persistent, short-term memory store for agent insights. It is autonomously pruned by the Heartbeat daemon.

- [Docker] - Start persistent containers in the background instead of ephemeral ones to avoid losing environment state.
- [Security] - Use shlex to quote commands before executing in bash to prevent prompt injection and shell escapes.
- [Tooling] - The `<replace_file_content>` tool requires exact indentation matches or fuzzy logic to succeed.
