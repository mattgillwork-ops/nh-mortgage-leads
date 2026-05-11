"""
Anti-Gravity Knowledge Manager
================================
Autonomously prunes and consolidates the Learnings.md file.
Uses a relevance-based approach — NOT a date filter.

An entry is considered "stale" if:
  1. It has not been referenced in any Memory_Log in the last 30 days.
  2. It is a duplicate of another entry (fuzzy match > 90%).

Run modes:
  python knowledge_manager.py          -> Live pruning run
  python knowledge_manager.py --dry-run -> Preview only, no changes made
"""

import os
import sys
import re
import glob
import logging
import datetime
import difflib

logging.basicConfig(level=logging.INFO, format='%(levelname)s [KnowledgeManager]: %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEARNINGS_PATH = os.path.join(BASE_DIR, "Learnings.md")
MEMORY_LOGS_DIR = os.path.join(BASE_DIR, "tru", "Memory_Logs")
STALE_DAYS_THRESHOLD = 30
SIMILARITY_THRESHOLD = 0.90


def load_entries(file_path: str) -> list[str]:
    """Load individual bullet entries from a Markdown file."""
    if not os.path.exists(file_path):
        logging.warning(f"Learnings file not found: {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- '):
            entries.append(stripped)

    logging.info(f"Loaded {len(entries)} entries from {os.path.basename(file_path)}.")
    return entries


def get_recent_log_content(days: int = 30) -> str:
    """Read all memory logs from the last N days and return their combined text."""
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    combined = ""

    if not os.path.exists(MEMORY_LOGS_DIR):
        return combined

    for log_file in glob.glob(os.path.join(MEMORY_LOGS_DIR, "log_*.md")):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
        if mtime >= cutoff:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    combined += f.read() + "\n"
            except Exception:
                pass

    logging.info(f"Loaded {len(combined)} chars from recent memory logs (last {days} days).")
    return combined


def is_referenced(entry: str, log_content: str) -> bool:
    """
    Check if a learning entry's key concepts appear in recent memory logs.
    Uses a keyword extraction approach to avoid exact-string dependency.
    """
    # Extract meaningful keywords (words > 4 chars, not common stopwords)
    stopwords = {'this', 'that', 'with', 'from', 'have', 'been', 'will', 'also',
                 'more', 'into', 'than', 'when', 'they', 'which', 'their', 'there'}
    words = re.findall(r'\b[a-zA-Z]{4,}\b', entry.lower())
    keywords = [w for w in words if w not in stopwords]

    if not keywords:
        return True  # Can't evaluate, keep it

    # If at least 2 keywords appear in recent logs, consider it referenced
    hits = sum(1 for kw in keywords if kw in log_content.lower())
    return hits >= min(2, len(keywords))


def find_duplicates(entries: list[str]) -> set[int]:
    """
    Find indices of entries that are near-duplicates of a previous entry.
    Keeps the first occurrence, marks subsequent near-duplicates for removal.
    """
    to_remove = set()
    for i in range(len(entries)):
        if i in to_remove:
            continue
        for j in range(i + 1, len(entries)):
            if j in to_remove:
                continue
            ratio = difflib.SequenceMatcher(None, entries[i], entries[j]).ratio()
            if ratio >= SIMILARITY_THRESHOLD:
                logging.info(f"Duplicate found (similarity={ratio:.2f}): '{entries[j][:60]}...'")
                to_remove.add(j)

    return to_remove


def load_header(file_path: str) -> str:
    """Extract the non-bullet header content from the Learnings file."""
    if not os.path.exists(file_path):
        return "# System Learnings\n\nAutonomously pruned by the Heartbeat daemon.\n\n"

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header_lines = []
    for line in lines:
        if line.strip().startswith('- '):
            break
        header_lines.append(line)

    return "".join(header_lines)


def prune(dry_run: bool = False):
    """Main pruning function."""
    logging.info(f"Starting knowledge pruning (dry_run={dry_run})...")

    entries = load_entries(LEARNINGS_PATH)
    if not entries:
        logging.info("No entries to prune.")
        return

    recent_logs = get_recent_log_content(days=STALE_DAYS_THRESHOLD)

    # Step 1: Find stale entries (not referenced in recent logs)
    stale_indices = set()
    for i, entry in enumerate(entries):
        if not is_referenced(entry, recent_logs):
            logging.info(f"[STALE] '{entry[:80]}'")
            stale_indices.add(i)

    # Step 2: Find duplicates
    duplicate_indices = find_duplicates(entries)

    # Step 3: Combine and report
    remove_indices = stale_indices | duplicate_indices
    kept = [e for i, e in enumerate(entries) if i not in remove_indices]
    removed = [e for i, e in enumerate(entries) if i in remove_indices]

    logging.info(f"--- Pruning Summary ---")
    logging.info(f"Total entries: {len(entries)}")
    logging.info(f"Stale (unreferenced): {len(stale_indices)}")
    logging.info(f"Duplicates: {len(duplicate_indices)}")
    logging.info(f"Will keep: {len(kept)}")
    logging.info(f"Will remove: {len(removed)}")

    if dry_run:
        logging.info("[DRY RUN] No changes made. Run without --dry-run to apply.")
        for entry in removed:
            logging.info(f"  [WOULD REMOVE] {entry[:80]}")
        return

    # Step 4: Write the pruned file
    header = load_header(LEARNINGS_PATH)
    with open(LEARNINGS_PATH, 'w', encoding='utf-8') as f:
        f.write(header)
        for entry in kept:
            f.write(entry + "\n")

    logging.info(f"Pruning complete. {len(removed)} entries removed.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    prune(dry_run=dry_run)
