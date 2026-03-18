#!/usr/bin/env python3
"""
ACTIONABLE AGGREGATOR -- Scans ALL sources for actionable items, deduplicates, and prioritizes.

Sources:
  - OPS/PERSISTENT_TASK_TRACKER.md (existing tasks)
  - OPS/DAILY_TACTICAL_PLAN.md (today's plan)
  - OPS/PROMPT_META_REVIEW.md (lost threads from prompts)
  - AUTOMATIONS/agent/swarm/reports/*.md (agent recommendations)
  - AUTOMATIONS/agent/ceo_agent/decisions.jsonl (CEO decisions needing human action)
  - LEDGER/DECISIONS.csv (pending decisions)

Priority levels:
  P0: Revenue-blocking human actions (payments, account setup)
  P1: System improvements with high ROI
  P2: Nice-to-have optimizations
  P3: Research/exploration

Usage:
    python3 AUTOMATIONS/actionable_aggregator.py              # Print queue
    python3 AUTOMATIONS/actionable_aggregator.py --save       # Save to OPS/ACTIONABLE_QUEUE.md + update tracker
    python3 AUTOMATIONS/actionable_aggregator.py --json       # JSON output
"""

from __future__ import annotations

import argparse
import csv
csv.field_size_limit(10 * 1024 * 1024)
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
OPS = PROJECT / "OPS"
LEDGER = PROJECT / "LEDGER"
LOGS = AUTOMATIONS / "logs"

# Source files
TRACKER_FILE = OPS / "PERSISTENT_TASK_TRACKER.md"
TACTICAL_PLAN = OPS / "DAILY_TACTICAL_PLAN.md"
META_REVIEW = OPS / "PROMPT_META_REVIEW.md"
SWARM_REPORTS = AUTOMATIONS / "agent" / "swarm" / "reports"
CEO_DECISIONS = AUTOMATIONS / "agent" / "ceo_agent" / "decisions.jsonl"
DECISIONS_CSV = LEDGER / "DECISIONS.csv"

# Output
OUTPUT_FILE = OPS / "ACTIONABLE_QUEUE.md"
LOG_FILE = LOGS / "actionable_aggregator.log"

# Priority keywords for classification
P0_KEYWORDS = [
    "stripe", "payment", "gumroad", "account creation", "account setup",
    "authenticate", "mcp", "gmail", "upload", "sign up", "signup",
    "revenue block", "p0", "human required", "blocker", "unblock",
]
P1_KEYWORDS = [
    "deploy", "launch", "fix", "broken", "error", "bug", "improvement",
    "optimize", "automate", "p1", "high roi", "pipeline", "conversion",
    "monetize", "monetization", "listing", "list product",
]
P2_KEYWORDS = [
    "refactor", "clean", "update", "upgrade", "enhance", "p2",
    "nice to have", "optimization", "performance",
]
P3_KEYWORDS = [
    "research", "explore", "investigate", "experiment", "p3",
    "try", "consider", "evaluate", "study",
]


def safe_path(target: str | Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [AGGREGATOR] [{level}] {msg}")


def log_to_file(msg: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")


def classify_priority(text: str) -> str:
    """Classify an item into P0/P1/P2/P3 based on keywords."""
    lower = text.lower()

    # Check for explicit priority markers first
    for p in ["p0", "p1", "p2", "p3"]:
        if f"({p})" in lower or f"[{p}]" in lower or f"priority: {p}" in lower or lower.startswith(p):
            return p.upper()

    # Keyword-based classification
    for kw in P0_KEYWORDS:
        if kw in lower:
            return "P0"
    for kw in P1_KEYWORDS:
        if kw in lower:
            return "P1"
    for kw in P2_KEYWORDS:
        if kw in lower:
            return "P2"
    for kw in P3_KEYWORDS:
        if kw in lower:
            return "P3"

    return "P2"  # Default


def is_human_action(text: str) -> bool:
    """Check if this requires human action (vs system/agent action)."""
    lower = text.lower()
    human_markers = [
        "human", "manual", "account", "sign up", "signup", "upload",
        "authenticate", "payment", "post from personal", "create account",
        "open browser", "paste", "click", "api key",
    ]
    return any(m in lower for m in human_markers)


def normalize_item(text: str) -> str:
    """Normalize item text for deduplication."""
    text = text.strip()
    # Remove checkbox markers
    text = re.sub(r"^-\s*\[[ x]\]\s*", "", text)
    # Remove leading bullets
    text = re.sub(r"^[-*]\s*", "", text)
    # Remove priority markers
    text = re.sub(r"\(P[0-3]\)", "", text, flags=re.IGNORECASE)
    # Remove timestamps
    text = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?", "", text)
    return text.strip()


def dedup_key(text: str) -> str:
    """Generate a deduplication key from item text."""
    normalized = normalize_item(text).lower()
    # Remove common filler words for fuzzy matching
    for word in ["the", "a", "an", "to", "for", "and", "or", "is", "in", "on", "at"]:
        normalized = normalized.replace(f" {word} ", " ")
    # Collapse whitespace
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized[:100]


class ActionableItem:
    """Represents a single actionable item."""

    def __init__(self, text: str, source: str, priority: str = "", is_human: bool = False) -> None:
        self.text = text.strip()
        self.source = source
        self.priority = priority or classify_priority(text)
        self.is_human = is_human or is_human_action(text)
        self.dedup_key = dedup_key(text)

    def __repr__(self) -> str:
        return f"[{self.priority}] {self.text} (from {self.source})"


def extract_from_tracker() -> list[ActionableItem]:
    """Extract actionable items from PERSISTENT_TASK_TRACKER.md."""
    items: list[ActionableItem] = []
    if not TRACKER_FILE.exists():
        return items

    text = TRACKER_FILE.read_text(encoding="utf-8", errors="replace")
    for line in text.split("\n"):
        stripped = line.strip()
        lower = stripped.lower()

        # Look for human blockers and action items
        if any(kw in lower for kw in ["blocker", "human", "action", "p0", "next action"]):
            if stripped.startswith("- ") or stripped.startswith("* "):
                items.append(ActionableItem(stripped, "PERSISTENT_TASK_TRACKER"))

    return items


def extract_from_tactical_plan() -> list[ActionableItem]:
    """Extract actionable items from DAILY_TACTICAL_PLAN.md."""
    items: list[ActionableItem] = []
    if not TACTICAL_PLAN.exists():
        return items

    text = TACTICAL_PLAN.read_text(encoding="utf-8", errors="replace")
    in_human_section = False
    in_action_section = False

    for line in text.split("\n"):
        stripped = line.strip()
        lower = stripped.lower()

        if "human" in lower and ("action" in lower or "required" in lower or "blocker" in lower):
            in_human_section = True
            in_action_section = False
            continue
        elif "action" in lower and "item" in lower:
            in_action_section = True
            in_human_section = False
            continue
        elif stripped.startswith("## ") or stripped.startswith("### "):
            in_human_section = False
            in_action_section = False
            continue

        if (in_human_section or in_action_section) and (stripped.startswith("- ") or stripped.startswith("| ")):
            items.append(ActionableItem(stripped, "DAILY_TACTICAL_PLAN", is_human=in_human_section))

    return items


def extract_from_meta_review() -> list[ActionableItem]:
    """Extract actionable items and lost threads from PROMPT_META_REVIEW.md."""
    items: list[ActionableItem] = []
    if not META_REVIEW.exists():
        return items

    # Only use if recent (< 3 days old)
    try:
        mtime = datetime.fromtimestamp(META_REVIEW.stat().st_mtime)
        if (datetime.now() - mtime).total_seconds() > 3 * 86400:
            return items
    except Exception:
        return items

    text = META_REVIEW.read_text(encoding="utf-8", errors="replace")
    current_section = ""

    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            current_section = stripped
            continue

        if current_section in ("## Actionable Items", "## Lost Threads"):
            if stripped.startswith("- "):
                source_tag = "PROMPT_META_REVIEW/lost_threads" if "Lost" in current_section else "PROMPT_META_REVIEW"
                items.append(ActionableItem(stripped, source_tag))

    return items


def extract_from_swarm_reports() -> list[ActionableItem]:
    """Extract actionable recommendations from recent swarm reports."""
    items: list[ActionableItem] = []
    if not SWARM_REPORTS.exists():
        return items

    cutoff = datetime.now() - timedelta(days=2)
    recent_reports: list[Path] = []

    for f in sorted(SWARM_REPORTS.iterdir(), reverse=True):
        if f.is_file() and f.suffix == ".md":
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime >= cutoff:
                    recent_reports.append(f)
            except Exception:
                continue

    # Only process last 10 reports to keep it fast
    for report_path in recent_reports[:10]:
        try:
            text = report_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        in_action_section = False
        for line in text.split("\n"):
            stripped = line.strip()
            lower = stripped.lower()

            if any(kw in lower for kw in ["action", "recommend", "next step", "todo", "blocker"]):
                if stripped.startswith("#"):
                    in_action_section = True
                    continue

            if stripped.startswith("#") and in_action_section:
                in_action_section = False

            if in_action_section and stripped.startswith("- "):
                items.append(ActionableItem(stripped, f"swarm/{report_path.name}"))

    return items


def extract_from_ceo_decisions() -> list[ActionableItem]:
    """Extract CEO decisions that need human action."""
    items: list[ActionableItem] = []
    if not CEO_DECISIONS.exists():
        return items

    cutoff = datetime.now() - timedelta(days=2)

    try:
        with open(CEO_DECISIONS, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    ts_str = d.get("ts", "")
                    try:
                        ts = datetime.fromisoformat(ts_str)
                    except (ValueError, TypeError):
                        continue

                    if ts < cutoff:
                        continue

                    # Look for decisions requiring human action
                    action = d.get("action", "") or d.get("summary", "") or ""
                    dtype = d.get("type", "")
                    status = d.get("status", "").lower()

                    if status in ("pending", "blocked", "needs_human"):
                        items.append(ActionableItem(
                            f"[CEO/{dtype}] {action}",
                            "ceo_decisions",
                            is_human=True,
                        ))
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return items


def extract_from_decisions_csv() -> list[ActionableItem]:
    """Extract pending decisions from LEDGER/DECISIONS.csv."""
    items: list[ActionableItem] = []
    if not DECISIONS_CSV.exists():
        return items

    try:
        with open(DECISIONS_CSV, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = (row.get("status", "") or "").lower()
                if status in ("pending", "blocked", "needs_human", "open"):
                    desc = row.get("description", "") or row.get("decision", "") or row.get("action", "") or ""
                    if desc:
                        items.append(ActionableItem(
                            desc,
                            "DECISIONS.csv",
                            is_human="human" in status,
                        ))
    except Exception:
        pass

    return items


def deduplicate(items: list[ActionableItem]) -> list[ActionableItem]:
    """Deduplicate items by normalized text key."""
    seen: set[str] = set()
    deduped: list[ActionableItem] = []

    for item in items:
        if item.dedup_key and item.dedup_key not in seen:
            seen.add(item.dedup_key)
            deduped.append(item)

    return deduped


def sort_items(items: list[ActionableItem]) -> list[ActionableItem]:
    """Sort by priority (P0 first), then human actions first within each priority."""
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

    def sort_key(item: ActionableItem) -> tuple[int, int]:
        p = priority_order.get(item.priority, 2)
        h = 0 if item.is_human else 1
        return (p, h)

    return sorted(items, key=sort_key)


def build_queue(items: list[ActionableItem]) -> str:
    """Build the actionable queue markdown."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []
    lines.append(f"# ACTIONABLE QUEUE -- {now}")
    lines.append(f"Total items: {len(items)} (deduplicated from all sources)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by priority
    by_priority: dict[str, list[ActionableItem]] = {"P0": [], "P1": [], "P2": [], "P3": []}
    for item in items:
        by_priority.setdefault(item.priority, []).append(item)

    priority_labels = {
        "P0": "CRITICAL -- Revenue-blocking human actions",
        "P1": "HIGH -- System improvements with high ROI",
        "P2": "MEDIUM -- Nice-to-have optimizations",
        "P3": "LOW -- Research/exploration",
    }

    for p in ["P0", "P1", "P2", "P3"]:
        p_items = by_priority.get(p, [])
        if not p_items:
            continue

        lines.append(f"## [{p}] {priority_labels.get(p, p)} ({len(p_items)} items)")
        lines.append("")

        for item in p_items:
            human_tag = " [HUMAN]" if item.is_human else ""
            lines.append(f"- [ ] {item.text}{human_tag}")
            lines.append(f"      Source: {item.source}")
        lines.append("")

    # Source summary
    sources: dict[str, int] = {}
    for item in items:
        base_source = item.source.split("/")[0]
        sources[base_source] = sources.get(base_source, 0) + 1

    lines.append("---")
    lines.append("### Sources")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        lines.append(f"- {src}: {count} items")
    lines.append("")

    return "\n".join(lines)


def update_tracker_with_new(items: list[ActionableItem]) -> int:
    """Add newly discovered items to PERSISTENT_TASK_TRACKER.md."""
    tracker_path = safe_path(TRACKER_FILE)
    if not tracker_path.exists():
        return 0

    existing = tracker_path.read_text(encoding="utf-8")
    existing_lower = existing.lower()

    new_items: list[ActionableItem] = []
    for item in items:
        # Only add items from non-tracker sources
        if item.source == "PERSISTENT_TASK_TRACKER":
            continue
        core = normalize_item(item.text)[:80]
        if core and core.lower() not in existing_lower:
            new_items.append(item)

    if not new_items:
        return 0

    addition = f"\n\n### AGGREGATOR FINDINGS -- {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    for item in new_items[:20]:  # Cap at 20 new items
        human_tag = " [HUMAN]" if item.is_human else ""
        addition += f"- [{item.priority}]{human_tag} {normalize_item(item.text)} (source: {item.source})\n"

    with open(tracker_path, "a", encoding="utf-8") as f:
        f.write(addition)

    return len(new_items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Actionable item aggregator across all sources")
    parser.add_argument("--save", action="store_true", help="Save to OPS/ACTIONABLE_QUEUE.md and update tracker")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    log("Scanning all sources for actionable items...")

    # Collect from all sources
    all_items: list[ActionableItem] = []

    sources_scanned: list[str] = []

    log("  Scanning PERSISTENT_TASK_TRACKER...")
    tracker_items = extract_from_tracker()
    all_items.extend(tracker_items)
    sources_scanned.append(f"tracker: {len(tracker_items)}")

    log("  Scanning DAILY_TACTICAL_PLAN...")
    tactical_items = extract_from_tactical_plan()
    all_items.extend(tactical_items)
    sources_scanned.append(f"tactical: {len(tactical_items)}")

    log("  Scanning PROMPT_META_REVIEW...")
    review_items = extract_from_meta_review()
    all_items.extend(review_items)
    sources_scanned.append(f"prompt_review: {len(review_items)}")

    log("  Scanning swarm reports...")
    swarm_items = extract_from_swarm_reports()
    all_items.extend(swarm_items)
    sources_scanned.append(f"swarm: {len(swarm_items)}")

    log("  Scanning CEO decisions...")
    ceo_items = extract_from_ceo_decisions()
    all_items.extend(ceo_items)
    sources_scanned.append(f"ceo: {len(ceo_items)}")

    log("  Scanning DECISIONS.csv...")
    csv_items = extract_from_decisions_csv()
    all_items.extend(csv_items)
    sources_scanned.append(f"decisions_csv: {len(csv_items)}")

    # Capital Genesis Priority Stack — pull P0 items as actionable
    log("  Scanning CAPITAL_GENESIS_PRIORITY_STACK...")
    cap_gen_path = Path(__file__).resolve().parent.parent / "OPS" / "CAPITAL_GENESIS_PRIORITY_STACK.md"
    cap_gen_items: list[ActionableItem] = []
    if cap_gen_path.exists():
        try:
            text = cap_gen_path.read_text()
            # Extract P0 rows (lines with "LAUNCH" action in the P0 table)
            in_p0 = False
            for line in text.split("\n"):
                if "## P0:" in line:
                    in_p0 = True
                    continue
                if in_p0 and line.startswith("## P"):
                    break
                if in_p0 and "| LAUNCH |" in line:
                    cols = [c.strip() for c in line.split("|") if c.strip()]
                    if len(cols) >= 3:
                        method_name = cols[1] if len(cols) > 1 else "unknown"
                        cap_gen_items.append(ActionableItem(
                            priority="P0",
                            text=f"[Capital Genesis] {method_name[:100]}",
                            source="capital_genesis_priority_stack",
                            is_human=False,
                        ))
        except Exception:
            pass
    all_items.extend(cap_gen_items)
    sources_scanned.append(f"capital_genesis: {len(cap_gen_items)}")

    log(f"  Raw total: {len(all_items)} items from {len(sources_scanned)} sources")

    # Deduplicate and sort
    deduped = deduplicate(all_items)
    sorted_items = sort_items(deduped)

    log(f"  After dedup: {len(sorted_items)} items")

    if args.json:
        result = {
            "generated": datetime.now().isoformat(),
            "total_raw": len(all_items),
            "total_deduped": len(sorted_items),
            "sources": sources_scanned,
            "items": [
                {
                    "priority": item.priority,
                    "text": item.text,
                    "source": item.source,
                    "is_human": item.is_human,
                }
                for item in sorted_items
            ],
        }
        print(json.dumps(result, indent=2))
    else:
        queue = build_queue(sorted_items)
        print(queue)

        if args.save:
            out_path = safe_path(OUTPUT_FILE)
            out_path.write_text(queue, encoding="utf-8")
            log(f"Saved to {out_path}")

            added = update_tracker_with_new(sorted_items)
            if added:
                log(f"Added {added} new items to PERSISTENT_TASK_TRACKER.md")

    log_to_file(f"Aggregation complete: {len(all_items)} raw, {len(sorted_items)} deduped, saved={args.save}")


if __name__ == "__main__":
    main()
