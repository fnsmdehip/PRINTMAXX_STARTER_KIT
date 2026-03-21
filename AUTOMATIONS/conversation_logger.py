#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Conversation Logger
Extracts user prompts and assistant responses from Claude Code session transcripts
into a clean, searchable JSONL format.

Usage:
    python3 conversation_logger.py --extract       # Process new transcripts
    python3 conversation_logger.py --search "kw"   # Search through history
    python3 conversation_logger.py --stats          # Show totals
    python3 conversation_logger.py --recent 20      # Last N exchanges
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
OUTPUT_FILE = PROJECT_ROOT / "LEDGER" / "CONVERSATION_HISTORY.jsonl"
STATE_FILE = PROJECT_ROOT / "AUTOMATIONS" / ".conversation_logger_state.json"

TRANSCRIPT_DIRS = [
    Path.home() / ".claude" / "projects" / "-Users-macbookpro",
    Path.home() / ".claude" / "projects" / "-Users-macbookpro-Documents-p-PRINTMAXX-STARTER-KITttttt",
]

MAX_CONTENT_LEN = 5000  # truncate huge messages


def safe_path(target: Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = target.resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# ---------------------------------------------------------------------------
# State tracking (dedup)
# ---------------------------------------------------------------------------
def load_state() -> dict:
    """Load processing state: which files + byte offsets have been processed."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"processed_files": {}, "total_extracted": 0, "last_run": None}


def save_state(state: dict) -> None:
    """Persist processing state."""
    state["last_run"] = datetime.now().isoformat(timespec="seconds")
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Content extraction
# ---------------------------------------------------------------------------
def extract_text_from_content(content) -> str:
    """Extract plain text from Claude message content field.

    Content can be:
    - A string (user messages)
    - A list of content blocks (assistant messages with text/thinking/tool_use types)
    """
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict):
                btype = block.get("type", "")
                if btype == "text":
                    text_parts.append(block.get("text", ""))
                # Skip thinking, tool_use, tool_result — we only want final text
            elif isinstance(block, str):
                text_parts.append(block)
        return "\n".join(text_parts).strip()

    return str(content).strip() if content else ""


def process_transcript(filepath: Path, processed_offset: int = 0) -> tuple[list[dict], int]:
    """Process a single JSONL transcript file.

    Returns (entries, new_offset) where entries is a list of extracted
    conversation entries and new_offset is the byte position after processing.
    """
    entries = []
    session_id = filepath.stem  # UUID filename without .jsonl
    session_file = filepath.name
    new_offset = 0

    try:
        file_size = filepath.stat().st_size
        if file_size <= processed_offset:
            return [], processed_offset  # already fully processed

        with open(filepath, "r", errors="replace") as f:
            if processed_offset > 0:
                f.seek(processed_offset)

            while True:
                line = f.readline()
                if not line:
                    break
                new_offset = f.tell()
                line = line.strip()
                if not line:
                    continue

                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_type = obj.get("type", "")
                if msg_type not in ("user", "assistant"):
                    continue

                message = obj.get("message", {})
                if not isinstance(message, dict):
                    continue

                role = message.get("role", msg_type)
                content_raw = message.get("content", "")
                text = extract_text_from_content(content_raw)

                if not text:
                    continue  # skip empty / tool-only assistant turns

                timestamp = obj.get("timestamp", "")
                if not timestamp:
                    timestamp = datetime.now().isoformat(timespec="seconds")

                content_length = len(text)
                if content_length > MAX_CONTENT_LEN:
                    text = text[:MAX_CONTENT_LEN] + f"\n... [truncated, full length: {content_length}]"

                entry = {
                    "ts": timestamp,
                    "session_id": session_id,
                    "role": role,
                    "content": text,
                    "content_length": content_length,
                    "session_file": session_file,
                }
                entries.append(entry)

    except (OSError, PermissionError) as e:
        print(f"  WARN: Could not read {filepath}: {e}", file=sys.stderr)
        return [], processed_offset

    return entries, new_offset


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def cmd_extract() -> None:
    """Extract new conversations from all transcript dirs."""
    safe_path(OUTPUT_FILE)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    state = load_state()
    processed = state.get("processed_files", {})
    total_new = 0

    for tdir in TRANSCRIPT_DIRS:
        if not tdir.exists():
            print(f"  SKIP: {tdir} does not exist")
            continue

        jsonl_files = sorted(tdir.glob("*.jsonl"))
        print(f"  Scanning {tdir.name}: {len(jsonl_files)} transcript files")

        for jf in jsonl_files:
            fkey = str(jf)
            prev_offset = processed.get(fkey, 0)
            file_size = jf.stat().st_size

            if file_size <= prev_offset:
                continue  # already fully processed

            entries, new_offset = process_transcript(jf, prev_offset)

            if entries:
                with open(OUTPUT_FILE, "a") as out:
                    for entry in entries:
                        out.write(json.dumps(entry, ensure_ascii=False) + "\n")
                total_new += len(entries)

            processed[fkey] = new_offset

    state["processed_files"] = processed
    state["total_extracted"] = state.get("total_extracted", 0) + total_new
    save_state(state)

    print(f"\n  Extracted {total_new} new entries")
    print(f"  Total entries ever: {state['total_extracted']}")
    print(f"  Output: {OUTPUT_FILE}")


def cmd_search(keyword: str) -> None:
    """Search conversation history for a keyword."""
    if not OUTPUT_FILE.exists():
        print("No conversation history yet. Run --extract first.")
        return

    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    matches = 0

    with open(OUTPUT_FILE) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            content = entry.get("content", "")
            if pattern.search(content):
                matches += 1
                ts = entry.get("ts", "?")
                role = entry.get("role", "?")
                session = entry.get("session_id", "?")[:8]
                # Show first match context
                idx = pattern.search(content).start()
                start = max(0, idx - 60)
                end = min(len(content), idx + len(keyword) + 60)
                snippet = content[start:end].replace("\n", " ")
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet = snippet + "..."

                print(f"  [{ts}] ({role}) session:{session} | {snippet}")

                if matches >= 50:
                    print(f"\n  ... showing first 50 of potentially more matches")
                    break

    print(f"\n  Total matches: {matches}")


def cmd_stats() -> None:
    """Show conversation history statistics."""
    if not OUTPUT_FILE.exists():
        print("No conversation history yet. Run --extract first.")
        return

    user_count = 0
    asst_count = 0
    sessions = set()
    total_chars = 0
    earliest = None
    latest = None

    with open(OUTPUT_FILE) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            role = entry.get("role", "")
            if role in ("user", "human"):
                user_count += 1
            elif role in ("assistant",):
                asst_count += 1

            sessions.add(entry.get("session_id", ""))
            total_chars += entry.get("content_length", 0)

            ts = entry.get("ts", "")
            if ts:
                if earliest is None or ts < earliest:
                    earliest = ts
                if latest is None or ts > latest:
                    latest = ts

    file_size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)

    state = load_state()
    processed_count = len(state.get("processed_files", {}))

    print(f"  Conversation History Stats")
    print(f"  {'='*40}")
    print(f"  User messages:      {user_count:,}")
    print(f"  Assistant messages:  {asst_count:,}")
    print(f"  Total entries:       {user_count + asst_count:,}")
    print(f"  Unique sessions:     {len(sessions):,}")
    print(f"  Total chars logged:  {total_chars:,}")
    print(f"  History file size:   {file_size_mb:.1f} MB")
    print(f"  Transcript files:    {processed_count}")
    print(f"  Date range:          {earliest or 'N/A'} to {latest or 'N/A'}")
    print(f"  Last extraction:     {state.get('last_run', 'never')}")
    print(f"  Output:              {OUTPUT_FILE}")


def cmd_recent(n: int) -> None:
    """Show last N conversation exchanges."""
    if not OUTPUT_FILE.exists():
        print("No conversation history yet. Run --extract first.")
        return

    # Read all entries and take last N
    entries = []
    with open(OUTPUT_FILE) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                entries.append(entry)
            except json.JSONDecodeError:
                continue

    if not entries:
        print("  No entries in conversation history.")
        return

    recent = entries[-n:]
    print(f"  Last {len(recent)} conversation entries:\n")

    for entry in recent:
        ts = entry.get("ts", "?")
        role = entry.get("role", "?").upper()
        session = entry.get("session_id", "?")[:8]
        content = entry.get("content", "")
        length = entry.get("content_length", 0)

        # Truncate display to 300 chars
        display = content[:300].replace("\n", " ")
        if len(content) > 300:
            display += f"... [{length} chars total]"

        print(f"  [{ts}] {role} (session:{session})")
        print(f"    {display}")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Conversation Logger — extract and search Claude session transcripts"
    )
    parser.add_argument("--extract", action="store_true", help="Process new transcripts")
    parser.add_argument("--search", type=str, metavar="KEYWORD", help="Search conversation history")
    parser.add_argument("--stats", action="store_true", help="Show conversation statistics")
    parser.add_argument("--recent", type=int, metavar="N", help="Show last N exchanges")

    args = parser.parse_args()

    if not any([args.extract, args.search, args.stats, args.recent]):
        parser.print_help()
        sys.exit(1)

    if args.extract:
        print("Extracting conversations from Claude transcripts...")
        cmd_extract()
    elif args.search:
        print(f"Searching for: {args.search}")
        cmd_search(args.search)
    elif args.stats:
        cmd_stats()
    elif args.recent:
        cmd_recent(args.recent)


if __name__ == "__main__":
    main()
