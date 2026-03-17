#!/usr/bin/env python3
"""
PRINTMAXX Alpha Auto-Processor
================================

Reads PENDING_REVIEW / NEW alpha from ALPHA_STAGING.csv, scores, deduplicates,
and routes each entry to the correct destination:

  Route A  NEW VENTURE       -> stub in OPS/
  Route B  BOLSTER EXISTING  -> append to matching OPS/ file
  Route C  RESEARCH TASK     -> cron entry in AUTOMATIONS/auto_generated_cron_entries.txt
  Route D  HIGH-VALUE QUEUE  -> LEDGER/ALPHA_HIGH_VALUE_QUEUE.md
  Route E  ARCHIVE           -> mark ARCHIVED

Usage:
    python3 AUTOMATIONS/alpha_auto_processor.py --dry-run            # preview
    python3 AUTOMATIONS/alpha_auto_processor.py --process-new        # since last run
    python3 AUTOMATIONS/alpha_auto_processor.py --process-all        # full backlog
    python3 AUTOMATIONS/alpha_auto_processor.py --batch-size 50      # custom batch
    python3 AUTOMATIONS/alpha_auto_processor.py --status             # show stats
"""

from __future__ import annotations

import argparse
import csv
csv.field_size_limit(10 * 1024 * 1024)  # 10MB limit for large alpha entries
import hashlib
import os
import re
import subprocess
import sys
import textwrap
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_CSV = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
HIGH_VALUE_QUEUE = PROJECT_ROOT / "LEDGER" / "ALPHA_HIGH_VALUE_QUEUE.md"
CRON_ENTRIES_FILE = PROJECT_ROOT / "AUTOMATIONS" / "auto_generated_cron_entries.txt"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE = LOG_DIR / "alpha_processor.log"
OPS_DIR = PROJECT_ROOT / "OPS"
LAST_RUN_MARKER = PROJECT_ROOT / "AUTOMATIONS" / ".alpha_processor_last_run"
APP_FACTORY_COMMAND_CENTER = PROJECT_ROOT / "AUTOMATIONS" / "app_factory_command_center.py"

# Statuses we process
PROCESSABLE_STATUSES = {"PENDING_REVIEW", "NEW", ""}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(msg: str) -> None:
    """Append to log file and print to stderr."""
    ts = now_iso()
    line = f"[{ts}] {msg}"
    print(line, file=sys.stderr)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def safe_path(target: Path) -> Path:
    """Verify path is within project root."""
    resolved = target.resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved


def text_hash(text: str) -> str:
    """Short hash for dedup."""
    return hashlib.md5(text.lower().strip().encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# OPS index  (filename -> first line / title)
# ---------------------------------------------------------------------------

def build_ops_index() -> dict[str, tuple[str, str]]:
    """
    Return {lowercase_stem: (full_path, first_meaningful_line)} for OPS/*.md
    """
    index: dict[str, tuple[str, str]] = {}
    ops = safe_path(OPS_DIR)
    if not ops.is_dir():
        return index
    for f in ops.iterdir():
        if f.is_file() and f.suffix == ".md":
            stem = f.stem.lower()
            try:
                first_line = ""
                with open(f, "r", errors="replace") as fh:
                    for line in fh:
                        stripped = line.strip().lstrip("#").strip()
                        if stripped:
                            first_line = stripped[:200]
                            break
                index[stem] = (str(f), first_line)
            except Exception:
                pass
    return index


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

# Keywords that boost score components
ENGAGEMENT_KEYWORDS = [
    "viral", "trending", "million", "followers", "subscribers",
    "views", "likes", "engagement", "growth", "audience",
]

SPECIFICITY_KEYWORDS = [
    r"\$\d", r"\d+%", r"\d+k", r"\d+x",
    "step-by-step", "framework", "template", "checklist",
    "exact", "specific", "how to", "tutorial",
]

ACTIONABILITY_KEYWORDS = [
    "sign up", "create", "build", "launch", "deploy",
    "automate", "scrape", "monitor", "list", "post",
    "use", "set up", "configure", "install",
]

REVENUE_KEYWORDS = [
    r"\$\d", "revenue", "profit", "income", "mrr",
    "arr", "commission", "affiliate", "monetiz",
    "payout", "earnings", "roi", "margin",
]

LOW_VALUE_SIGNALS = [
    "engagement bait", "no specifics", "vague", "duplicate",
    "generic", "recycled",
]


def _kw_score(text: str, keywords: list[str], max_pts: int) -> int:
    """Count how many keyword patterns match, scale to max_pts."""
    hits = 0
    lower = text.lower()
    for kw in keywords:
        if kw.startswith(r"\\") or re.search(r"[\\(){}|]", kw):
            if re.search(kw, lower, re.IGNORECASE):
                hits += 1
        else:
            if kw in lower:
                hits += 1
    return min(hits * (max_pts // max(len(keywords) // 3, 1)), max_pts)


def score_alpha(row: dict) -> int:
    """
    Score an alpha entry 0-100 based on:
      engagement (25)  specificity (25)  actionability (25)  revenue (25)
    """
    # Combine all text fields for analysis
    text_parts = [
        row.get("tactic", ""),
        row.get("extracted_method", ""),
        row.get("reviewer_notes", ""),
        row.get("category", ""),
    ]
    text = " ".join(str(p) for p in text_parts if p)

    engagement = _kw_score(text, ENGAGEMENT_KEYWORDS, 25)
    specificity = _kw_score(text, SPECIFICITY_KEYWORDS, 25)
    actionability = _kw_score(text, ACTIONABILITY_KEYWORDS, 25)
    revenue = _kw_score(text, REVENUE_KEYWORDS, 25)

    # Bonus for HIGH/HIGHEST roi_potential
    roi = str(row.get("roi_potential", "")).upper()
    if "HIGHEST" in roi:
        revenue = min(revenue + 10, 25)
    elif "HIGH" in roi:
        revenue = min(revenue + 5, 25)

    # Bonus for high synergy_score
    try:
        syn = int(row.get("synergy_score", 0))
        if syn > 500:
            engagement = min(engagement + 5, 25)
        elif syn > 100:
            engagement = min(engagement + 2, 25)
    except (ValueError, TypeError):
        pass

    # Penalty for low-value signals
    for sig in LOW_VALUE_SIGNALS:
        if sig in text.lower():
            specificity = max(specificity - 5, 0)

    total = engagement + specificity + actionability + revenue

    # Floor at 5 if there is any substantial text
    if len(text) > 50 and total < 5:
        total = 5

    return min(total, 100)


# ---------------------------------------------------------------------------
# Dedup / Redundancy
# ---------------------------------------------------------------------------

def check_redundancy(row: dict, seen_hashes: set[str], ops_index: dict) -> str | None:
    """
    Return a reason string if redundant, else None.
    """
    tactic = str(row.get("tactic", "")).strip()
    url = str(row.get("source_url", "")).strip()

    # 1) URL-based dedup
    if url and url.startswith("http"):
        url_h = text_hash(url)
        if url_h in seen_hashes:
            return f"Duplicate URL: {url[:80]}"
        seen_hashes.add(url_h)

    # 2) Content-based dedup (first 150 chars of tactic)
    if tactic:
        content_h = text_hash(tactic[:150])
        if content_h in seen_hashes:
            return f"Duplicate content: {tactic[:60]}..."
        seen_hashes.add(content_h)

    # 3) Check if alpha is already covered by OPS file
    if tactic:
        tactic_lower = tactic.lower()
        for stem, (path, first_line) in ops_index.items():
            # Check if the tactic's core keywords appear in the OPS filename
            words = re.findall(r"[a-z]{4,}", tactic_lower)[:5]
            stem_lower = stem.replace("_", " ")
            matches = sum(1 for w in words if w in stem_lower)
            if matches >= 3:
                return f"Covered by OPS: {Path(path).name}"

    return None


# ---------------------------------------------------------------------------
# Routing logic
# ---------------------------------------------------------------------------

# Timeframe patterns for Route C (RESEARCH TASK)
TIMEFRAME_PATTERNS = [
    r"\b(daily|every\s*day)\b",
    r"\b(weekly|every\s*week)\b",
    r"\b(monthly|every\s*month)\b",
    r"\bevery\s+\d+\s*(hour|minute|day|week|month)s?\b",
    r"\b(check|monitor|track|scan|scrape)\s+(regularly|periodically|continuously)\b",
    r"\b(monitor|watch|alert|notify)\b.*\b(change|update|new|price|drop)\b",
    r"\bcron\b",
    r"\bscheduled?\b.*\b(task|job|run)\b",
]

# Category-to-OPS-keyword mapping for Route B
CATEGORY_OPS_MAP = {
    "OUTBOUND": ["cold_email", "outbound", "outreach", "email_launch", "leads"],
    "CONTENT_FARM": ["content", "posting", "social", "tiktok", "youtube", "reels"],
    "CONTENT_FORMAT": ["content", "posting", "video", "carousel"],
    "APP_FACTORY": ["app_factory", "app_clone", "app_quality", "mobile_app"],
    "TOOL_ALPHA": ["tool", "automation", "scraper", "browser", "mcp"],
    "GROWTH_HACK": ["growth", "hack", "edge", "grey_hat", "seo", "viral"],
    "SEO_GEO_ASO": ["seo", "geo", "aso", "keyword", "ranking"],
    "MONETIZATION": ["monetiz", "revenue", "pricing", "affiliate", "gumroad"],
    "ECOM": ["ecom", "arb", "dropship", "product", "listing", "etsy", "amazon"],
    "ECOM_ARB": ["ecom", "arb", "dropship", "product"],
    "AI_ALPHA": ["ai_agent", "automation", "tool", "mcp", "claude"],
    "AI_INFLUENCER": ["influencer", "nsfw", "persona", "findom", "fanvue"],
    "FREELANCE": ["freelance", "fiverr", "upwork", "service"],
}

# High-value categories get a score bonus
HIGH_VALUE_CATEGORIES = {
    "TOOL_ALPHA", "APP_FACTORY", "MONETIZATION", "ECOM_ARB", "AI_ALPHA",
}


def find_ops_match(row: dict, ops_index: dict) -> str | None:
    """
    Find the best OPS/ file to bolster. Returns path or None.
    """
    category = str(row.get("category", "")).strip().upper()
    tactic = str(row.get("tactic", "")).lower()

    # Gather search keywords from category map
    search_terms = CATEGORY_OPS_MAP.get(category, [])

    # Also extract significant words from tactic text
    tactic_words = set(re.findall(r"[a-z]{5,}", tactic))

    best_match = None
    best_score = 0

    for stem, (path, first_line) in ops_index.items():
        match_score = 0
        stem_words = stem.replace("_", " ").lower()

        # Category keyword matches
        for term in search_terms:
            if term in stem_words:
                match_score += 3

        # Tactic word matches in filename
        for w in tactic_words:
            if w in stem_words:
                match_score += 1

        # First line content match
        first_lower = first_line.lower()
        for w in list(tactic_words)[:8]:
            if w in first_lower:
                match_score += 1

        if match_score > best_score:
            best_score = match_score
            best_match = path

    # Require minimum relevance
    if best_score >= 4:
        return best_match
    return None


def detect_timeframe(text: str) -> str | None:
    """
    Check if the alpha mentions a monitoring/recurring task.
    Returns a cron schedule string if detected, else None.
    """
    lower = text.lower()
    for pattern in TIMEFRAME_PATTERNS:
        m = re.search(pattern, lower)
        if m:
            matched = m.group(0).lower()
            # Map to cron schedule
            if "daily" in matched or "every day" in matched:
                return "0 6 * * *"
            elif "weekly" in matched or "every week" in matched:
                return "0 6 * * 1"
            elif "monthly" in matched or "every month" in matched:
                return "0 6 1 * *"
            elif "hour" in matched:
                hrs = re.search(r"\d+", matched)
                h = int(hrs.group()) if hrs else 2
                return f"0 */{h} * * *"
            elif "minute" in matched:
                return "*/30 * * * *"
            else:
                # Generic monitoring => daily
                return "0 7 * * *"
    return None


def route_alpha(
    row: dict,
    score: int,
    ops_index: dict,
) -> tuple[str, str, str | None]:
    """
    Determine the route for an alpha entry.

    Returns: (route_name, new_status, target_path_or_info)
      route_name: VENTURE | BOLSTER | RESEARCH | HIGH_VALUE | ARCHIVE
      new_status: the status to write back
      target: path or info string
    """
    tactic = str(row.get("tactic", ""))
    category = str(row.get("category", "")).strip().upper()

    # Route E: ARCHIVE if very low score
    if score < 15:
        return ("ARCHIVE", "ARCHIVED", "Low score ({})".format(score))

    # Route C: RESEARCH TASK if timeframe detected
    cron = detect_timeframe(tactic)
    if cron and score >= 20:
        return ("RESEARCH", "CONVERTED_TO_RESEARCH", cron)

    # Route D: HIGH-VALUE QUEUE if score >= 70 (needs human review)
    if score >= 70:
        return ("HIGH_VALUE", "QUEUED_FOR_REVIEW", None)

    # Route B: BOLSTER EXISTING if we find a matching OPS file
    match = find_ops_match(row, ops_index)
    if match and score >= 20:
        return ("BOLSTER", "INTEGRATED", match)

    # Route A: NEW VENTURE if score >= 35 and category suggests opportunity
    if score >= 35 and category in HIGH_VALUE_CATEGORIES:
        return ("VENTURE", "ROUTED_TO_VENTURE", None)

    # Route A: NEW VENTURE if score >= 40 for any category
    if score >= 40:
        return ("VENTURE", "ROUTED_TO_VENTURE", None)

    # Route B fallback: even without exact match, bolster if reasonable
    if score >= 25 and match:
        return ("BOLSTER", "INTEGRATED", match)

    # Route E: ARCHIVE everything else
    return ("ARCHIVE", "ARCHIVED", "Score {} below routing threshold".format(score))


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

def create_venture_stub(row: dict, score: int, dry_run: bool) -> str:
    """Create a stub OPS file for a new venture opportunity."""
    alpha_id = row.get("alpha_id", "UNKNOWN")
    category = row.get("category", "GENERAL")
    tactic = row.get("tactic", "")[:500]
    source = row.get("source", "")
    url = row.get("source_url", "")

    # Build filename
    slug = re.sub(r"[^a-z0-9]+", "_", category.lower())[:30]
    filename = f"VENTURE_{alpha_id}_{slug}.md"
    filepath = safe_path(OPS_DIR / filename)

    content = (
        f"# Venture Opportunity: {alpha_id}\n\n"
        f"**Source:** {source}\n"
        f"**URL:** {url}\n"
        f"**Category:** {category}\n"
        f"**Score:** {score}/100\n"
        f"**Created:** {now_iso()}\n"
        f"**Status:** NEEDS_EVALUATION\n\n"
        f"## Opportunity Details\n\n"
        f"{tactic}\n\n"
        f"## Estimated Revenue Potential\n\n"
        f"- TBD (needs deeper analysis)\n\n"
        f"## Required Steps\n\n"
        f"1. Validate opportunity (check if still active)\n"
        f"2. Assess required investment (time, money, accounts)\n"
        f"3. Build minimum viable implementation\n"
        f"4. Test with small budget/effort\n"
        f"5. Scale if results confirm potential\n\n"
        f"## Related Alpha\n\n"
        f"- {alpha_id} (this entry)\n\n"
        f"## Notes\n\n"
        f"Auto-generated by alpha_auto_processor.py. Needs human review.\n"
    )

    if not dry_run:
        with open(filepath, "w") as f:
            f.write(content)

    return str(filepath)


def bolster_existing(row: dict, target_path: str, score: int, dry_run: bool) -> None:
    """Append alpha intelligence to an existing OPS file."""
    alpha_id = row.get("alpha_id", "UNKNOWN")
    tactic = row.get("tactic", "")[:400]
    source = row.get("source", "")
    url = row.get("source_url", "")

    section = (
        f"\n\n---\n\n"
        f"## Pending Enhancement ({alpha_id}, Score: {score})\n\n"
        f"**Source:** {source} | **URL:** {url}\n"
        f"**Added:** {now_iso()}\n\n"
        f"{tactic}\n\n"
    )

    if not dry_run:
        target = safe_path(Path(target_path))
        with open(target, "a") as f:
            f.write(section)


def add_cron_entry(row: dict, cron_schedule: str, dry_run: bool) -> None:
    """Append a cron entry specification."""
    alpha_id = row.get("alpha_id", "UNKNOWN")
    tactic = row.get("tactic", "")[:200]
    source = row.get("source_url", "")

    entry = (
        f"# {alpha_id}: {tactic[:80]}...\n"
        f"# Source: {source}\n"
        f"# Added: {now_iso()}\n"
        f"# {cron_schedule}  # TODO: create monitoring script for this\n"
        f"\n"
    )

    if not dry_run:
        target = safe_path(CRON_ENTRIES_FILE)
        with open(target, "a") as f:
            f.write(entry)


def add_to_high_value_queue(row: dict, score: int, dry_run: bool) -> None:
    """Add entry to the high-value queue for human review."""
    alpha_id = row.get("alpha_id", "UNKNOWN")
    tactic = row.get("tactic", "")[:500]
    source = row.get("source", "")
    url = row.get("source_url", "")
    category = row.get("category", "")

    entry = (
        f"\n\n---\n\n"
        f"### {alpha_id} (Score: {score}/100) | {category}\n\n"
        f"**Source:** {source} | **URL:** {url}\n\n"
        f"{tactic}\n\n"
        f"**Action needed:** Review and decide: approve for execution, assign to venture, or archive.\n\n"
    )

    if not dry_run:
        target = safe_path(HIGH_VALUE_QUEUE)
        # Create file with header if it doesn't exist
        if not target.exists():
            with open(target, "w") as f:
                f.write("# Alpha High-Value Queue\n\n")
                f.write("Entries scored 70+ that need human review before routing.\n\n")
                f.write(f"Last updated: {now_iso()}\n")
        with open(target, "a") as f:
            f.write(entry)


# ---------------------------------------------------------------------------
# CSV read / write
# ---------------------------------------------------------------------------

def read_alpha_csv() -> tuple[list[str], list[dict]]:
    """Read ALPHA_STAGING.csv, return (fieldnames, rows)."""
    if not ALPHA_CSV.exists():
        log(f"ERROR: {ALPHA_CSV} not found")
        sys.exit(1)

    rows = []
    fieldnames = []
    with open(ALPHA_CSV, "r", newline="", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            rows.append(row)
    return fieldnames, rows


def write_alpha_csv(fieldnames: list[str], rows: list[dict]) -> None:
    """Write back the full CSV."""
    target = safe_path(ALPHA_CSV)
    with open(target, "w", newline="", errors="replace") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_batch(
    rows: list[dict],
    ops_index: dict,
    dry_run: bool = False,
    batch_size: int = 100,
    process_all: bool = False,
) -> dict:
    """
    Process alpha entries in batches.
    Returns summary counters.
    """
    stats = Counter()
    stats["total_rows"] = len(rows)
    seen_hashes: set[str] = set()

    # Pre-seed hashes with already-processed entries to detect cross-batch dupes
    for row in rows:
        status = str(row.get("status", "")).strip().upper()
        if status not in PROCESSABLE_STATUSES:
            url = str(row.get("source_url", "")).strip()
            tactic = str(row.get("tactic", "")).strip()
            if url and url.startswith("http"):
                seen_hashes.add(text_hash(url))
            if tactic:
                seen_hashes.add(text_hash(tactic[:150]))

    # Identify processable rows
    processable = []
    for i, row in enumerate(rows):
        status = str(row.get("status", "")).strip().upper()
        if status in PROCESSABLE_STATUSES:
            processable.append(i)

    if not process_all:
        processable = processable[:batch_size]

    log(f"Found {len(processable)} entries to process (batch_size={batch_size}, process_all={process_all})")

    processed = 0
    for idx in processable:
        row = rows[idx]
        alpha_id = row.get("alpha_id", f"ROW{idx}")

        # Score
        sc = score_alpha(row)
        stats["scored"] += 1

        # Dedup
        reason = check_redundancy(row, seen_hashes, ops_index)
        if reason:
            if not dry_run:
                row["status"] = "ARCHIVED"
                row["reviewer_notes"] = f"Auto-archived: {reason}"
            stats["ARCHIVE"] += 1
            stats["deduped"] += 1
            log(f"  [{alpha_id}] ARCHIVED (dedup): {reason}")
            processed += 1
            continue

        # Route
        route_name, new_status, target = route_alpha(row, sc, ops_index)

        if route_name == "VENTURE":
            path = create_venture_stub(row, sc, dry_run)
            if not dry_run:
                row["status"] = new_status
                row["reviewer_notes"] = f"Auto-routed to venture: {Path(path).name}"
                row["ops_generated"] = "TRUE"
            stats["VENTURE"] += 1
            log(f"  [{alpha_id}] VENTURE (score={sc}): {Path(path).name}")

        elif route_name == "BOLSTER":
            bolster_existing(row, target, sc, dry_run)
            if not dry_run:
                row["status"] = new_status
                row["reviewer_notes"] = f"Auto-integrated into: {Path(target).name}"
            stats["BOLSTER"] += 1
            log(f"  [{alpha_id}] BOLSTER (score={sc}): {Path(target).name}")

        elif route_name == "RESEARCH":
            add_cron_entry(row, target, dry_run)
            if not dry_run:
                row["status"] = new_status
                row["reviewer_notes"] = f"Auto-converted to research task: {target}"
            stats["RESEARCH"] += 1
            log(f"  [{alpha_id}] RESEARCH (score={sc}): cron={target}")

        elif route_name == "HIGH_VALUE":
            add_to_high_value_queue(row, sc, dry_run)
            if not dry_run:
                row["status"] = new_status
                row["reviewer_notes"] = f"Queued for human review (score={sc})"
            stats["HIGH_VALUE"] += 1
            log(f"  [{alpha_id}] HIGH_VALUE (score={sc})")

        elif route_name == "ARCHIVE":
            if not dry_run:
                row["status"] = new_status
                row["reviewer_notes"] = f"Auto-archived: {target}"
            stats["ARCHIVE"] += 1
            log(f"  [{alpha_id}] ARCHIVE (score={sc}): {target}")

        processed += 1

    stats["processed"] = processed
    return stats


def show_status() -> None:
    """Show current alpha pipeline stats."""
    _, rows = read_alpha_csv()
    counts = Counter()
    for row in rows:
        status = str(row.get("status", "")).strip().upper()
        if not status:
            status = "(EMPTY)"
        counts[status] += 1

    print("\n=== ALPHA STAGING STATUS ===\n")
    print(f"Total entries: {len(rows)}")
    print()
    for status, count in counts.most_common(20):
        bar = "#" * min(count // 50, 40)
        print(f"  {status:25s} {count:>6d}  {bar}")

    # Last run info
    if LAST_RUN_MARKER.exists():
        print(f"\nLast processor run: {LAST_RUN_MARKER.read_text().strip()}")
    else:
        print("\nLast processor run: NEVER")

    # Log tail
    if LOG_FILE.exists():
        print(f"\nRecent log: {LOG_FILE}")
        lines = LOG_FILE.read_text().strip().split("\n")
        for line in lines[-5:]:
            print(f"  {line}")


def refresh_app_factory_queue() -> None:
    """Keep the app-factory queue current after live alpha routing."""
    if not APP_FACTORY_COMMAND_CENTER.exists():
        return
    try:
        subprocess.run(
            [sys.executable, str(APP_FACTORY_COMMAND_CENTER), "--refresh", "--top", "5", "--limit", "40"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=PROJECT_ROOT,
        )
    except Exception as exc:
        log(f"App factory queue refresh failed: {exc}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Alpha Auto-Processor: score, dedup, and route alpha entries."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without making changes",
    )
    parser.add_argument(
        "--process-all",
        action="store_true",
        help="Process ALL pending entries (full backlog)",
    )
    parser.add_argument(
        "--process-new",
        action="store_true",
        help="Process only entries since last run",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of entries to process per batch (default: 100)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current pipeline statistics",
    )
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if not (args.dry_run or args.process_all or args.process_new):
        parser.print_help()
        return

    # Read CSV
    log("=== Alpha Auto-Processor starting ===")
    fieldnames, rows = read_alpha_csv()
    log(f"Loaded {len(rows)} rows from ALPHA_STAGING.csv")

    # Build OPS index
    ops_index = build_ops_index()
    log(f"Indexed {len(ops_index)} OPS/ files")

    # Process
    batch_size = len(rows) if args.process_all else args.batch_size
    stats = process_batch(
        rows,
        ops_index,
        dry_run=args.dry_run,
        batch_size=batch_size,
        process_all=args.process_all,
    )

    # Write back CSV (unless dry run)
    if not args.dry_run:
        write_alpha_csv(fieldnames, rows)
        # Update last run marker
        safe_path(LAST_RUN_MARKER).write_text(now_iso())
        refresh_app_factory_queue()
        log("CSV updated and last-run marker saved")

    # Report
    mode = "DRY RUN" if args.dry_run else "LIVE"
    report = textwrap.dedent(f"""
    === ALPHA AUTO-PROCESSOR REPORT ({mode}) ===

    Total rows in CSV:  {stats['total_rows']}
    Entries processed:  {stats['processed']}
    Entries scored:     {stats['scored']}

    Routing breakdown:
      NEW VENTURE:      {stats['VENTURE']}
      BOLSTER EXISTING: {stats['BOLSTER']}
      RESEARCH TASKS:   {stats['RESEARCH']}
      HIGH-VALUE QUEUE: {stats['HIGH_VALUE']}
      ARCHIVED:         {stats['ARCHIVE']}
        (of which deduped: {stats['deduped']})

    """)
    print(report)
    log(report.strip())
    log("=== Alpha Auto-Processor complete ===")


if __name__ == "__main__":
    main()
