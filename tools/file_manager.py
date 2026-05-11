"""
Anti-Gravity File Manager Tool
================================
Provides safe, validated file operations for agents.
All paths are checked against the workspace boundary before any operation.

Agents should use these functions instead of raw shell commands for file ops.
"""

import os
import glob
import shutil
import logging

logger = logging.getLogger("FileManager")

# Workspace root is two levels up from this file (tools/file_manager.py -> root)
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _safe_path(path: str) -> str:
    """
    Validates and resolves a path. Raises PermissionError if outside workspace.
    """
    full_path = os.path.abspath(os.path.join(WORKSPACE_ROOT, path))
    if not full_path.lower().startswith(WORKSPACE_ROOT.lower()):
        raise PermissionError(f"[FileManager] Access denied: '{path}' is outside the workspace.")
    if ".." in path or "~" in path:
        raise ValueError(f"[FileManager] Invalid path characters in: '{path}'")
    return full_path


def read_file(path: str, max_chars: int = 20000) -> str:
    """Read a file and return its content (truncated to max_chars)."""
    try:
        full_path = _safe_path(path)
        if not os.path.exists(full_path):
            return f"[FileManager ERROR] File not found: {path}"
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content) > max_chars:
            content = content[:max_chars] + "\n...[Truncated]"
        logger.info(f"Read file: {path} ({len(content)} chars)")
        return content
    except PermissionError as e:
        return f"[FileManager BLOCKED] {e}"
    except Exception as e:
        return f"[FileManager ERROR] Failed to read {path}: {e}"


def write_file(path: str, content: str, overwrite: bool = True) -> str:
    """Write content to a file. Creates parent directories if needed."""
    try:
        full_path = _safe_path(path)

        # Protect core system files
        core_files = ["base_agent.py", "ceo_agent.py", "main.py", "qa_check.py", "selfcheck.py"]
        if any(os.path.basename(full_path) == f for f in core_files):
            return f"[FileManager BLOCKED] Core file '{path}' is write-protected. Use replace_file_content."

        if not overwrite and os.path.exists(full_path):
            return f"[FileManager ERROR] File already exists and overwrite=False: {path}"

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Wrote file: {path}")
        return f"[FileManager OK] Wrote {path}"
    except PermissionError as e:
        return f"[FileManager BLOCKED] {e}"
    except Exception as e:
        return f"[FileManager ERROR] Failed to write {path}: {e}"


def list_dir(path: str = ".") -> str:
    """List the contents of a directory within the workspace."""
    try:
        full_path = _safe_path(path)
        if not os.path.isdir(full_path):
            return f"[FileManager ERROR] Not a directory: {path}"
        entries = sorted(os.listdir(full_path))
        lines = []
        for entry in entries:
            entry_full = os.path.join(full_path, entry)
            if os.path.isdir(entry_full):
                lines.append(f"  [DIR]  {entry}/")
            else:
                size = os.path.getsize(entry_full)
                lines.append(f"  [FILE] {entry} ({size} bytes)")
        return f"Contents of '{path}':\n" + "\n".join(lines)
    except PermissionError as e:
        return f"[FileManager BLOCKED] {e}"
    except Exception as e:
        return f"[FileManager ERROR] Failed to list {path}: {e}"


def delete_file(path: str) -> str:
    """
    Safely delete a file. Will NEVER delete core system files or directories.
    """
    try:
        full_path = _safe_path(path)

        # Core file protection
        core_files = ["base_agent.py", "ceo_agent.py", "main.py", "qa_check.py",
                      "selfcheck.py", "heartbeat_daemon.py", "docker_runner.py",
                      "WORKSPACE_AI_RULES.md", "AGENTS.md"]
        if any(os.path.basename(full_path) == f for f in core_files):
            return f"[FileManager BLOCKED] Core file '{path}' cannot be deleted."

        if os.path.isdir(full_path):
            return f"[FileManager BLOCKED] Use delete_dir() for directories, not delete_file()."

        if not os.path.exists(full_path):
            return f"[FileManager ERROR] File not found: {path}"

        os.remove(full_path)
        logger.info(f"Deleted file: {path}")
        return f"[FileManager OK] Deleted {path}"
    except PermissionError as e:
        return f"[FileManager BLOCKED] {e}"
    except Exception as e:
        return f"[FileManager ERROR] Failed to delete {path}: {e}"


def find_files(pattern: str, base_path: str = ".") -> str:
    """Find files matching a glob pattern within the workspace."""
    try:
        full_base = _safe_path(base_path)
        matches = glob.glob(os.path.join(full_base, "**", pattern), recursive=True)
        # Filter to only workspace paths
        safe_matches = [m for m in matches if m.lower().startswith(WORKSPACE_ROOT.lower())]
        rel_matches = [os.path.relpath(m, WORKSPACE_ROOT) for m in safe_matches]
        if not rel_matches:
            return f"[FileManager] No files found matching '{pattern}' in '{base_path}'"
        return f"Found {len(rel_matches)} file(s):\n" + "\n".join(f"  {p}" for p in rel_matches)
    except PermissionError as e:
        return f"[FileManager BLOCKED] {e}"
    except Exception as e:
        return f"[FileManager ERROR] {e}"


if __name__ == "__main__":
    print(list_dir("."))
