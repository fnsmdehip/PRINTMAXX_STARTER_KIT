#!/usr/bin/env python3
"""
PRINTMAXX Persistent Memory System — Local Subconscious
═══════════════════════════════════════════════════════

Zero-dependency alternative to Letta cloud. Runs entirely local.
Provides persistent memory across Claude Code sessions via files.

Three memory layers:
  1. CORE MEMORIES — Who you are, what you're building, key decisions
  2. WORKING MEMORIES — Current tasks, recent learnings, active priorities
  3. EPISODIC MEMORIES — Session summaries, what worked/failed, patterns

The system auto-compacts: old working memories get promoted to core
or archived. Nothing is lost, everything is searchable.

Usage:
  python3 AUTOMATIONS/persistent_memory.py --remember "key insight"
  python3 AUTOMATIONS/persistent_memory.py --recall "topic"
  python3 AUTOMATIONS/persistent_memory.py --session-start     # Inject context
  python3 AUTOMATIONS/persistent_memory.py --session-end "summary"
  python3 AUTOMATIONS/persistent_memory.py --compact            # Auto-organize
  python3 AUTOMATIONS/persistent_memory.py --status             # Memory stats
  python3 AUTOMATIONS/persistent_memory.py --search "query"     # Full search
  python3 AUTOMATIONS/persistent_memory.py --forget "id"        # Remove memory
  python3 AUTOMATIONS/persistent_memory.py --priorities         # Current top priorities
"""

import json
import os
import sys
import re
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# ── paths ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE / "OPS" / "memory"
CORE_FILE = MEMORY_DIR / "core_memories.jsonl"
WORKING_FILE = MEMORY_DIR / "working_memories.jsonl"
EPISODIC_FILE = MEMORY_DIR / "episodic_memories.jsonl"
PRIORITIES_FILE = MEMORY_DIR / "current_priorities.json"
SESSION_LOG = MEMORY_DIR / "session_log.jsonl"

def safe_path(p):
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(BASE)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved

def ensure_dirs():
    safe_path(MEMORY_DIR)
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


# ── memory operations ────────────────────────────────────────────────────────

def remember(text, layer="working", tags=None, importance=50):
    """Store a memory."""
    ensure_dirs()

    memory = {
        "id": hashlib.md5(f"{text}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
        "timestamp": datetime.now().isoformat(),
        "text": text,
        "tags": tags or [],
        "importance": importance,
        "access_count": 0,
        "last_accessed": None,
    }

    file_map = {
        "core": CORE_FILE,
        "working": WORKING_FILE,
        "episodic": EPISODIC_FILE,
    }

    target = file_map.get(layer, WORKING_FILE)
    safe_path(target)

    # Check for duplicates (fuzzy)
    existing = load_memories(target)
    for m in existing:
        if _similarity(m["text"], text) > 0.85:
            print(f"  Skipped (duplicate of {m['id']}): {text[:60]}...")
            return None

    with open(target, "a") as f:
        f.write(json.dumps(memory) + "\n")

    print(f"  Remembered [{layer}] ({memory['id']}): {text[:60]}...")
    return memory

def recall(query, top_k=10):
    """Search all memory layers for relevant memories."""
    all_memories = []

    for label, fpath in [("core", CORE_FILE), ("working", WORKING_FILE), ("episodic", EPISODIC_FILE)]:
        memories = load_memories(fpath)
        for m in memories:
            m["layer"] = label
            m["relevance"] = _relevance_score(query, m)
            all_memories.append(m)

    # Sort by relevance
    all_memories.sort(key=lambda x: x["relevance"], reverse=True)

    return all_memories[:top_k]

def search(query, top_k=20):
    """Full text search across all memories."""
    results = recall(query, top_k=top_k)

    print(f"\n  Search results for: '{query}' ({len(results)} found)")
    print("  " + "=" * 60)

    for i, m in enumerate(results, 1):
        layer_color = {"core": "CORE", "working": "WORK", "episodic": "EPIS"}.get(m.get("layer", "?"), "?")
        ts = m.get("timestamp", "?")[:10]
        print(f"\n  {i}. [{layer_color}] [{m['relevance']:.0f}%] ({ts})")
        print(f"     {m['text'][:120]}")
        if m.get("tags"):
            print(f"     Tags: {', '.join(m['tags'])}")

    return results

def forget(memory_id):
    """Remove a memory by ID."""
    for fpath in [CORE_FILE, WORKING_FILE, EPISODIC_FILE]:
        if not fpath.exists():
            continue
        memories = load_memories(fpath)
        filtered = [m for m in memories if m.get("id") != memory_id]
        if len(filtered) < len(memories):
            safe_path(fpath)
            with open(fpath, "w") as f:
                for m in filtered:
                    f.write(json.dumps(m) + "\n")
            print(f"  Forgot memory {memory_id}")
            return True

    print(f"  Memory {memory_id} not found")
    return False


# ── session management ───────────────────────────────────────────────────────

def session_start():
    """Generate context injection for session start."""
    ensure_dirs()

    context = []
    context.append("# PERSISTENT MEMORY — SESSION CONTEXT")
    context.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    context.append("")

    # Core memories (always include)
    core = load_memories(CORE_FILE)
    if core:
        context.append("## Core Memories (permanent)")
        for m in sorted(core, key=lambda x: x.get("importance", 0), reverse=True):
            context.append(f"- {m['text']}")
        context.append("")

    # Recent working memories (last 7 days)
    working = load_memories(WORKING_FILE)
    recent_working = [m for m in working if _is_recent(m, days=7)]
    if recent_working:
        context.append("## Recent Working Memories (last 7 days)")
        for m in sorted(recent_working, key=lambda x: x.get("importance", 0), reverse=True)[:15]:
            ts = m.get("timestamp", "?")[:10]
            context.append(f"- [{ts}] {m['text']}")
        context.append("")

    # Recent episodic memories (last 3 sessions)
    episodic = load_memories(EPISODIC_FILE)
    recent_ep = sorted(episodic, key=lambda x: x.get("timestamp", ""), reverse=True)[:3]
    if recent_ep:
        context.append("## Recent Session Summaries")
        for m in recent_ep:
            ts = m.get("timestamp", "?")[:10]
            context.append(f"- [{ts}] {m['text'][:200]}")
        context.append("")

    # Current priorities
    if PRIORITIES_FILE.exists():
        try:
            priorities = json.loads(PRIORITIES_FILE.read_text())
            if priorities:
                context.append("## Current Priorities")
                for p in priorities[:5]:
                    context.append(f"- [{p.get('score', '?')}] {p.get('action', p.get('text', '?'))[:80]}")
                context.append("")
        except Exception:
            pass

    # Stats
    total = len(core) + len(working) + len(episodic)
    context.append(f"## Memory Stats: {len(core)} core, {len(working)} working, {len(episodic)} episodic = {total} total")
    context.append("")

    result = "\n".join(context)
    print(result)

    # Log session start
    _log_session_event("start")

    return result

def session_end(summary):
    """Save session summary as episodic memory."""
    ensure_dirs()

    # Save as episodic memory
    remember(summary, layer="episodic", tags=["session_summary"], importance=70)

    # Extract and save any key learnings as working memories
    learning_patterns = [
        r"learned?:?\s*(.+?)(?:\.|$)",
        r"key insight:?\s*(.+?)(?:\.|$)",
        r"what worked:?\s*(.+?)(?:\.|$)",
        r"what failed:?\s*(.+?)(?:\.|$)",
    ]

    for pattern in learning_patterns:
        matches = re.findall(pattern, summary, re.IGNORECASE)
        for match in matches:
            if len(match) > 10:
                remember(match.strip(), layer="working", tags=["auto_extracted"], importance=60)

    # Log session end
    _log_session_event("end", summary=summary[:200])

    print(f"\n  Session summary saved. Episodic memories: {_count_memories(EPISODIC_FILE)}")

def compact():
    """Auto-organize memories: promote important working→core, archive old."""
    ensure_dirs()

    working = load_memories(WORKING_FILE)
    core = load_memories(CORE_FILE)

    promoted = 0
    archived = 0

    remaining = []
    for m in working:
        # Promote high-importance memories accessed multiple times
        if m.get("importance", 0) >= 80 and m.get("access_count", 0) >= 3:
            m["promoted_from"] = "working"
            m["promoted_at"] = datetime.now().isoformat()
            safe_path(CORE_FILE)
            with open(CORE_FILE, "a") as f:
                f.write(json.dumps(m) + "\n")
            promoted += 1
        # Archive very old memories (>30 days)
        elif not _is_recent(m, days=30) and m.get("importance", 0) < 60:
            archived += 1
            # Don't delete, just don't keep in working
        else:
            remaining.append(m)

    # Rewrite working memories
    if promoted > 0 or archived > 0:
        safe_path(WORKING_FILE)
        with open(WORKING_FILE, "w") as f:
            for m in remaining:
                f.write(json.dumps(m) + "\n")

    print(f"  Compacted: {promoted} promoted to core, {archived} archived")
    print(f"  Core: {_count_memories(CORE_FILE)}, Working: {len(remaining)}, Episodic: {_count_memories(EPISODIC_FILE)}")

def update_priorities():
    """Update current priorities from autonomous_money_printer."""
    ensure_dirs()
    try:
        sys.path.insert(0, str(BASE / "AUTOMATIONS"))
        from autonomous_money_printer import gather_system_state, generate_priorities
        state = gather_system_state()
        priorities = generate_priorities(state)

        safe_path(PRIORITIES_FILE)
        PRIORITIES_FILE.write_text(json.dumps(priorities[:10], indent=2))

        print(f"  Updated {len(priorities[:10])} priorities")
        for p in priorities[:5]:
            print(f"    [{p['score']}] {p['category']}: {p['action'][:60]}")
    except Exception as e:
        print(f"  Warning: Could not update priorities: {e}")

def get_status():
    """Show memory system status."""
    ensure_dirs()

    core_count = _count_memories(CORE_FILE)
    working_count = _count_memories(WORKING_FILE)
    episodic_count = _count_memories(EPISODIC_FILE)
    total = core_count + working_count + episodic_count

    print("=" * 60)
    print("  PERSISTENT MEMORY — STATUS")
    print("=" * 60)
    print(f"  Core memories:     {core_count}")
    print(f"  Working memories:  {working_count}")
    print(f"  Episodic memories: {episodic_count}")
    print(f"  Total:             {total}")

    # Recent memories
    working = load_memories(WORKING_FILE)
    recent = [m for m in working if _is_recent(m, days=3)]
    print(f"\n  Recent (3 days):   {len(recent)}")

    # Session count
    if SESSION_LOG.exists():
        try:
            sessions = sum(1 for line in SESSION_LOG.read_text().splitlines() if line.strip())
            print(f"  Session events:    {sessions}")
        except Exception:
            pass

    # Priorities
    if PRIORITIES_FILE.exists():
        try:
            priorities = json.loads(PRIORITIES_FILE.read_text())
            print(f"\n  Current priorities: {len(priorities)}")
            for p in priorities[:3]:
                print(f"    [{p.get('score', '?')}] {p.get('category', '?')}: {p.get('action', '?')[:50]}")
        except Exception:
            pass

    # Last session
    if SESSION_LOG.exists():
        try:
            lines = SESSION_LOG.read_text().strip().splitlines()
            if lines:
                last = json.loads(lines[-1])
                print(f"\n  Last session: {last.get('timestamp', '?')[:16]} ({last.get('event', '?')})")
        except Exception:
            pass


# ── helpers ──────────────────────────────────────────────────────────────────

def load_memories(filepath):
    """Load memories from JSONL file."""
    memories = []
    if filepath.exists():
        try:
            for line in filepath.read_text().splitlines():
                if line.strip():
                    try:
                        memories.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        except Exception:
            pass
    return memories

def _count_memories(filepath):
    if not filepath.exists():
        return 0
    try:
        return sum(1 for line in filepath.read_text().splitlines() if line.strip())
    except Exception:
        return 0

def _similarity(text1, text2):
    """Simple word-overlap similarity."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if not words1 or not words2:
        return 0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union) if union else 0

def _relevance_score(query, memory):
    """Score memory relevance to query (0-100)."""
    text = memory.get("text", "")
    tags = memory.get("tags", [])
    importance = memory.get("importance", 50)

    # Word overlap
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    tag_words = set(t.lower() for t in tags)

    word_overlap = len(query_words & text_words) / max(len(query_words), 1)
    tag_overlap = len(query_words & tag_words) / max(len(query_words), 1)

    # Recency boost
    recency = 1.0
    if _is_recent(memory, days=1):
        recency = 1.3
    elif _is_recent(memory, days=7):
        recency = 1.1
    elif not _is_recent(memory, days=30):
        recency = 0.8

    # Calculate score
    score = (word_overlap * 50 + tag_overlap * 20 + importance * 0.3) * recency
    return min(score, 100)

def _is_recent(memory, days=7):
    """Check if memory is from within last N days."""
    try:
        ts = datetime.fromisoformat(memory.get("timestamp", "2000-01-01"))
        return (datetime.now() - ts).days <= days
    except Exception:
        return False

def _log_session_event(event, summary=None):
    """Log session event."""
    ensure_dirs()
    safe_path(SESSION_LOG)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
    }
    if summary:
        entry["summary"] = summary

    with open(SESSION_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ── seed memories ────────────────────────────────────────────────────────────

def seed_core_memories():
    """Seed essential core memories if empty."""
    ensure_dirs()

    if _count_memories(CORE_FILE) > 0:
        print("  Core memories already seeded, skipping.")
        return

    seeds = [
        ("PRINTMAXX is a 24/7 autonomous money printing system with 21+ revenue methods, 90+ automation scripts, and a perpetual improvement loop.", 95, ["identity", "system"]),
        ("Account creation is the #1 blocker. 0 active accounts. Everything else is built and ready.", 100, ["blocker", "accounts"]),
        ("Top revenue methods: AI Findom (73.0), Affiliate Content (72.5), Programmatic SEO (71.8). All FREE.", 90, ["methods", "revenue"]),
        ("12,948 hot leads qualified. 0 emails sent. Cold email infrastructure needed.", 85, ["leads", "pipeline"]),
        ("7 PWA apps deployed to surge.sh. 0 in App Store. iOS submission needs Apple Developer account.", 80, ["apps", "deployment"]),
        ("Revenue: $478 total. Goal: $1K/mo then $10K/mo then $100K/mo.", 90, ["revenue", "goals"]),
        ("Quality standard: top-tier apps matching top 10 in category. No AI slop. No lazy shortcuts.", 95, ["quality", "standards"]),
        ("User preference: autonomous execution, no asking permission, go above and beyond, quant-level work.", 95, ["preferences", "execution"]),
        ("User preference: don't just do what specifically mentioned — independently discover and build new ops.", 90, ["preferences", "agentic"]),
        ("Copy style: @pipelineabuser voice. Consequence-first hooks. Specific numbers. No em dashes. No AI vocabulary.", 85, ["content", "voice"]),
        ("Disk at 97.2%. Be mindful of disk space. Clean old logs before creating large files.", 75, ["system", "disk"]),
        ("63 cron jobs running 24/7. Overnight runner at 2 AM. Brain morning briefing at 5:30 AM.", 80, ["automation", "cron"]),
        ("Cross-pollination between revenue methods is key. Fitness→faith, gaming→all, dating→faith matching.", 70, ["strategy", "cross_pollination"]),
        ("Seasonal opportunities: Ramadan (Feb-Mar), Back to School (Aug), BFCM (Nov), New Year (Jan).", 70, ["strategy", "seasonal"]),
        ("User's mission: print via normie-coded masses, reallocate to conscious builders. Karmic redistribution.", 90, ["mission", "philosophy"]),
    ]

    for text, importance, tags in seeds:
        remember(text, layer="core", tags=tags, importance=importance)

    print(f"\n  Seeded {len(seeds)} core memories.")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Persistent Memory System")
    parser.add_argument("--remember", type=str, help="Store a new memory")
    parser.add_argument("--recall", type=str, help="Recall memories about a topic")
    parser.add_argument("--search", type=str, help="Full search across all memories")
    parser.add_argument("--forget", type=str, help="Remove a memory by ID")
    parser.add_argument("--session-start", action="store_true", help="Generate session context")
    parser.add_argument("--session-end", type=str, help="Save session summary")
    parser.add_argument("--compact", action="store_true", help="Auto-organize memories")
    parser.add_argument("--status", action="store_true", help="Memory system status")
    parser.add_argument("--priorities", action="store_true", help="Update and show priorities")
    parser.add_argument("--seed", action="store_true", help="Seed core memories")
    parser.add_argument("--layer", type=str, default="working", choices=["core", "working", "episodic"], help="Memory layer")
    parser.add_argument("--importance", type=int, default=50, help="Importance score 0-100")
    parser.add_argument("--tags", type=str, help="Comma-separated tags")

    args = parser.parse_args()

    if args.remember:
        tags = args.tags.split(",") if args.tags else []
        remember(args.remember, layer=args.layer, tags=tags, importance=args.importance)
    elif args.recall:
        recall(args.recall)
    elif args.search:
        search(args.search)
    elif args.forget:
        forget(args.forget)
    elif args.session_start:
        session_start()
    elif args.session_end:
        session_end(args.session_end)
    elif args.compact:
        compact()
    elif args.status:
        get_status()
    elif args.priorities:
        update_priorities()
    elif args.seed:
        seed_core_memories()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
