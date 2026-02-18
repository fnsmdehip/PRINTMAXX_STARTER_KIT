#!/usr/bin/env python3
"""
PRINTMAXX Prompt Logger — tracks every user prompt across sessions.
When conversations compact, agents search old prompts to audit completion.

Usage:
    python3 AUTOMATIONS/prompt_logger.py --log "prompt text here"
    python3 AUTOMATIONS/prompt_logger.py --log-file /path/to/file.txt
    python3 AUTOMATIONS/prompt_logger.py --search "keyword"
    python3 AUTOMATIONS/prompt_logger.py --audit
    python3 AUTOMATIONS/prompt_logger.py --complete P001 --notes "done in session X"
    python3 AUTOMATIONS/prompt_logger.py --today
    python3 AUTOMATIONS/prompt_logger.py --session 2026-02-13
    python3 AUTOMATIONS/prompt_logger.py --summary
    python3 AUTOMATIONS/prompt_logger.py --export

Storage: LEDGER/PROMPT_LOG.jsonl (one JSON object per line)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, date
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
LOG_FILE = LEDGER_DIR / "PROMPT_LOG.jsonl"
EXPORT_FILE = BASE_DIR / "OPS" / "PROMPT_AUDIT_LOG.md"

# ---------------------------------------------------------------------------
# Tag extraction keywords
# ---------------------------------------------------------------------------
TAG_KEYWORDS = [
    "build", "scrape", "deploy", "research", "create", "fix", "update",
    "launch", "run", "test", "audit", "organize", "search", "install",
    "automate", "monitor", "export", "import", "generate", "list",
    "tweet", "post", "content", "email", "cold", "app", "agent",
    "dashboard", "parallel", "cron", "alpha", "ops", "seed", "log",
    "ship", "compile", "refactor", "debug", "integrate", "migrate",
    "clone", "fork", "setup", "configure", "schedule", "delete",
    "compress", "compact", "prompt", "track", "score", "rank",
]


def extract_tags(text: str) -> list[str]:
    """Pull action-relevant keywords from prompt text."""
    lower = text.lower()
    found = [kw for kw in TAG_KEYWORDS if re.search(r"\b" + re.escape(kw) + r"\b", lower)]
    return sorted(set(found))


# ---------------------------------------------------------------------------
# JSONL helpers
# ---------------------------------------------------------------------------

def _ensure_dirs():
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_FILE.parent.mkdir(parents=True, exist_ok=True)


def read_all_entries() -> list[dict]:
    """Read every line from PROMPT_LOG.jsonl."""
    if not LOG_FILE.exists():
        return []
    entries = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def next_id(entries: list[dict]) -> str:
    """Auto-increment P001, P002, ..."""
    if not entries:
        return "P001"
    nums = []
    for e in entries:
        m = re.match(r"P(\d+)", e.get("id", ""))
        if m:
            nums.append(int(m.group(1)))
    nxt = max(nums) + 1 if nums else 1
    return f"P{nxt:03d}"


def append_entry(entry: dict):
    """Append a single JSON entry to the log file."""
    _ensure_dirs()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def rewrite_all(entries: list[dict]):
    """Rewrite the full log file (used for updates)."""
    _ensure_dirs()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Core operations
# ---------------------------------------------------------------------------

def log_prompt(text: str, status: str = "LOGGED", completion: str = "PENDING",
               notes: str = "", completed_at: str = None) -> dict:
    """Create and append a new prompt entry. Returns the entry."""
    entries = read_all_entries()
    pid = next_id(entries)
    now = datetime.now()
    entry = {
        "id": pid,
        "timestamp": now.isoformat(timespec="seconds"),
        "session_date": now.strftime("%Y-%m-%d"),
        "prompt_text": text.strip(),
        "tags": extract_tags(text),
        "status": status,
        "completion_status": completion,
        "completed_at": completed_at,
        "notes": notes,
    }
    append_entry(entry)
    return entry


def log_prompt_with_overrides(text: str, session_date: str = None,
                               completion: str = "PENDING",
                               notes: str = "", completed_at: str = None) -> dict:
    """Log with explicit session_date (for seeding historical prompts)."""
    entries = read_all_entries()
    pid = next_id(entries)
    now = datetime.now()
    entry = {
        "id": pid,
        "timestamp": now.isoformat(timespec="seconds"),
        "session_date": session_date or now.strftime("%Y-%m-%d"),
        "prompt_text": text.strip(),
        "tags": extract_tags(text),
        "status": "LOGGED",
        "completion_status": completion,
        "completed_at": completed_at,
        "notes": notes,
    }
    append_entry(entry)
    return entry


def search_prompts(keyword: str) -> list[dict]:
    """Return entries whose prompt_text contains keyword (case-insensitive)."""
    entries = read_all_entries()
    kw = keyword.lower()
    return [e for e in entries if kw in e.get("prompt_text", "").lower()
            or kw in " ".join(e.get("tags", [])).lower()]


def audit_pending() -> list[dict]:
    """Return all entries with completion_status != COMPLETED."""
    entries = read_all_entries()
    return [e for e in entries if e.get("completion_status") != "COMPLETED"]


def complete_prompt(pid: str, notes: str = ""):
    """Mark a prompt as COMPLETED."""
    entries = read_all_entries()
    found = False
    for e in entries:
        if e["id"] == pid.upper():
            e["completion_status"] = "COMPLETED"
            e["completed_at"] = datetime.now().isoformat(timespec="seconds")
            if notes:
                e["notes"] = notes
            found = True
            break
    if not found:
        print(f"ERROR: Prompt {pid} not found.")
        sys.exit(1)
    rewrite_all(entries)
    print(f"Marked {pid} as COMPLETED.")


def show_today():
    """Show prompts from today."""
    today = date.today().isoformat()
    entries = read_all_entries()
    return [e for e in entries if e.get("session_date") == today]


def show_session(session_date: str):
    """Show prompts from a specific date."""
    entries = read_all_entries()
    return [e for e in entries if e.get("session_date") == session_date]


def show_summary():
    """Print stats about the prompt log."""
    entries = read_all_entries()
    total = len(entries)
    completed = sum(1 for e in entries if e.get("completion_status") == "COMPLETED")
    pending = sum(1 for e in entries if e.get("completion_status") == "PENDING")
    in_progress = sum(1 for e in entries if e.get("completion_status") == "IN_PROGRESS")
    dates = sorted(set(e.get("session_date", "unknown") for e in entries))

    print("=" * 60)
    print("  PRINTMAXX PROMPT LOG SUMMARY")
    print("=" * 60)
    print(f"  Total prompts:   {total}")
    print(f"  COMPLETED:       {completed}")
    print(f"  PENDING:         {pending}")
    print(f"  IN_PROGRESS:     {in_progress}")
    print(f"  Session dates:   {len(dates)}")
    if dates:
        print(f"  First session:   {dates[0]}")
        print(f"  Latest session:  {dates[-1]}")
    print("=" * 60)

    # Per-date breakdown
    if dates:
        print("\n  Per-session breakdown:")
        for d in dates:
            day_entries = [e for e in entries if e.get("session_date") == d]
            day_done = sum(1 for e in day_entries if e.get("completion_status") == "COMPLETED")
            print(f"    {d}: {len(day_entries)} prompts ({day_done} completed)")
    print()


def export_markdown():
    """Export all prompts to OPS/PROMPT_AUDIT_LOG.md."""
    _ensure_dirs()
    entries = read_all_entries()
    lines = [
        "# PRINTMAXX Prompt Audit Log",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Total prompts: {len(entries)}",
        "",
    ]

    # Group by session date
    dates = sorted(set(e.get("session_date", "unknown") for e in entries))
    for d in dates:
        day_entries = [e for e in entries if e.get("session_date") == d]
        lines.append(f"## Session: {d}")
        lines.append("")
        for e in day_entries:
            status_icon = {
                "COMPLETED": "[x]",
                "IN_PROGRESS": "[-]",
                "PENDING": "[ ]",
            }.get(e.get("completion_status", "PENDING"), "[ ]")
            short = e["prompt_text"][:120].replace("\n", " ")
            if len(e["prompt_text"]) > 120:
                short += "..."
            lines.append(f"- {status_icon} **{e['id']}** ({e.get('completion_status', 'PENDING')}): {short}")
            if e.get("tags"):
                lines.append(f"  - Tags: {', '.join(e['tags'])}")
            if e.get("notes"):
                lines.append(f"  - Notes: {e['notes']}")
        lines.append("")

    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Exported {len(entries)} prompts to {EXPORT_FILE}")


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_entries(entries: list[dict], title: str = "Results"):
    """Pretty-print a list of prompt entries."""
    if not entries:
        print(f"\n  {title}: No entries found.\n")
        return
    print(f"\n{'=' * 70}")
    print(f"  {title} ({len(entries)} entries)")
    print(f"{'=' * 70}")
    for e in entries:
        status = e.get("completion_status", "PENDING")
        icon = {"COMPLETED": "+", "IN_PROGRESS": "~", "PENDING": "!"}.get(status, "?")
        short = e["prompt_text"][:100].replace("\n", " ")
        if len(e["prompt_text"]) > 100:
            short += "..."
        print(f"\n  [{icon}] {e['id']}  |  {e.get('session_date', '?')}  |  {status}")
        print(f"      {short}")
        if e.get("tags"):
            print(f"      tags: {', '.join(e['tags'])}")
        if e.get("notes"):
            print(f"      notes: {e['notes']}")
    print(f"\n{'=' * 70}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Prompt Logger - track and audit user prompts across sessions"
    )
    parser.add_argument("--log", type=str, help="Log a new prompt (inline text)")
    parser.add_argument("--log-file", type=str, help="Log a prompt from a text file")
    parser.add_argument("--search", type=str, help="Search prompts by keyword")
    parser.add_argument("--audit", action="store_true", help="Show all non-completed prompts")
    parser.add_argument("--complete", type=str, metavar="PROMPT_ID", help="Mark a prompt as COMPLETED")
    parser.add_argument("--notes", type=str, default="", help="Notes when completing a prompt")
    parser.add_argument("--today", action="store_true", help="Show prompts from today")
    parser.add_argument("--session", type=str, metavar="YYYY-MM-DD", help="Show prompts from a specific date")
    parser.add_argument("--summary", action="store_true", help="Show log stats")
    parser.add_argument("--export", action="store_true", help="Export to OPS/PROMPT_AUDIT_LOG.md")
    parser.add_argument("--seed", action="store_true", help="Seed initial entries from Feb 13 session")

    args = parser.parse_args()

    # No args = show summary
    if len(sys.argv) == 1:
        show_summary()
        print("FUTURE AGENTS: At session start, run `python3 AUTOMATIONS/prompt_logger.py --audit`")
        print("to check for incomplete prompts from prior sessions.")
        print("At session end, log all user prompts with `python3 AUTOMATIONS/prompt_logger.py --log \"prompt text\"`.")
        return

    if args.log:
        entry = log_prompt(args.log)
        print(f"Logged {entry['id']}: {entry['prompt_text'][:80]}...")
        print(f"  tags: {', '.join(entry['tags'])}")

    elif args.log_file:
        path = Path(args.log_file)
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        entry = log_prompt(text)
        print(f"Logged {entry['id']} from file ({len(text)} chars)")
        print(f"  tags: {', '.join(entry['tags'])}")

    elif args.search:
        results = search_prompts(args.search)
        print_entries(results, f"Search results for '{args.search}'")

    elif args.audit:
        results = audit_pending()
        print_entries(results, "PENDING / IN_PROGRESS prompts (not yet completed)")

    elif args.complete:
        complete_prompt(args.complete, notes=args.notes)

    elif args.today:
        results = show_today()
        print_entries(results, f"Today's prompts ({date.today().isoformat()})")

    elif args.session:
        results = show_session(args.session)
        print_entries(results, f"Session {args.session}")

    elif args.summary:
        show_summary()

    elif args.export:
        export_markdown()

    elif args.seed:
        seed_initial_entries()

    # Always print the reminder at the end
    print("---")
    print("FUTURE AGENTS: At session start, run `python3 AUTOMATIONS/prompt_logger.py --audit`")
    print("to check for incomplete prompts from prior sessions.")
    print("At session end, log all user prompts with `python3 AUTOMATIONS/prompt_logger.py --log \"prompt text\"`.")


# ---------------------------------------------------------------------------
# Seed initial entries from today's session (Feb 13 2026)
# ---------------------------------------------------------------------------

def seed_initial_entries():
    """Seed the log with prompts from the Feb 13 2026 session."""
    existing = read_all_entries()
    if existing:
        print(f"Log already has {len(existing)} entries. Skipping seed to avoid duplicates.")
        return

    today = "2026-02-13"
    seeds = [
        {
            "text": "also we havent run high signal reddit and high signal twitter and my twitter bookmark scrapers in a few days, run those daily. extract alpha auto filter alpha and repurpose into content...",
            "completion": "COMPLETED",
            "completed_at": "2026-02-13T14:00:00",
            "notes": "Built daily_research_pipeline.py, installed cron for daily scraping",
        },
        {
            "text": "can u organize signal accounts and alpha by type if not already done like pipelineabuser is edgy growth business hacks some people are specially mostly ios app people, etc. organize and make it easy for future agents to work with and nav also add and scrape recent posts by zach_yadegari for good ios app tips",
            "completion": "COMPLETED",
            "completed_at": "2026-02-13T15:00:00",
            "notes": "Built SIGNAL_ACCOUNT_DIRECTORY.md, updated CSV categories, added @zach_yadegari",
        },
        {
            "text": "also you shouldve auto created new ops or research tasks or other stuff from the sorted alpha and started running it and making it automated why did that not happen? make sure agent claude instructions clearly ensure streamlining",
            "completion": "COMPLETED",
            "completed_at": "2026-02-13T16:00:00",
            "notes": "Built alpha_to_ops.py, generated 337 ops from sorted alpha",
        },
        {
            "text": "use agent teams run parallel max print stop wasting time",
            "completion": "COMPLETED",
            "completed_at": "2026-02-13T16:30:00",
            "notes": "Switched to parallel agent teams for all subsequent tasks",
        },
        {
            "text": "also u said u completed a lot this session and stuff but never acted on what u did dont just build systems autonomously act on them like those tweets i sent i wanted processes for and give me like a dashboard or build them into printmaxxterminal app so i can easily monitor shit like a master dash n8n kinda quant thing",
            "completion": "COMPLETED",
            "completed_at": "2026-02-13T18:00:00",
            "notes": "Built master dashboard at printmaxx-command.surge.sh with live monitoring",
        },
        {
            "text": "see if any claude code agent system task 24/7 ai assist entrepreneurship thing already built on github repos we can use. also note we do have a printmaxxterminal.app but idk if thats best for this",
            "completion": "COMPLETED",
            "completed_at": "2026-02-13T18:30:00",
            "notes": "Searched GitHub, found top 10 repos for 24/7 AI agent systems",
        },
        {
            "text": "ImportYeti customs data tweet alpha + Seedance 2.0 AI content generation tweet alpha - extract and process these",
            "completion": "IN_PROGRESS",
            "completed_at": None,
            "notes": "Tweet-based alpha extraction started, processing in pipeline",
        },
        {
            "text": "we need a better system of saving all my prompts so if we need to compact convo i and u can search old prompts to audit that we fully did what i wanted",
            "completion": "IN_PROGRESS",
            "completed_at": None,
            "notes": "Building prompt_logger.py (this task)",
        },
    ]

    for s in seeds:
        log_prompt_with_overrides(
            text=s["text"],
            session_date=today,
            completion=s["completion"],
            notes=s["notes"],
            completed_at=s["completed_at"],
        )

    print(f"Seeded {len(seeds)} prompts from Feb 13 2026 session.")


if __name__ == "__main__":
    main()
