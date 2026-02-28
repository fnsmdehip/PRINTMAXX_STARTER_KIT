#!/usr/bin/env python3
"""
PRINTMAXX Playbook Enhancer
================================

Reads BOLSTER_EXISTING results from the alpha_auto_processor and auto-appends
properly formatted insights to target playbook/OPS files.

The alpha_auto_processor routes entries to "BOLSTER EXISTING" (Route B) and marks
them INTEGRATED, but only performs a shallow append. This script:

  1. Scans ALPHA_STAGING.csv for entries eligible for deep bolstering
  2. Determines the best target OPS/*.md file by category matching
  3. Formats insights as clean markdown sections
  4. Appends to targets under an "Alpha Insights (Auto-Appended)" section
  5. Marks entries in ALPHA_STAGING.csv with [BOLSTERED: date, target]
  6. Logs everything to LEDGER/ALPHA_BOLSTER_LOG.csv

Usage:
    python3 AUTOMATIONS/playbook_enhancer.py --scan              # find eligible entries
    python3 AUTOMATIONS/playbook_enhancer.py --run               # execute bolstering
    python3 AUTOMATIONS/playbook_enhancer.py --run --batch-size 5
    python3 AUTOMATIONS/playbook_enhancer.py --run --category OUTBOUND
    python3 AUTOMATIONS/playbook_enhancer.py --run --dry-run     # preview only
    python3 AUTOMATIONS/playbook_enhancer.py --status            # show stats
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_CSV = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
BOLSTER_LOG = PROJECT_ROOT / "LEDGER" / "ALPHA_BOLSTER_LOG.csv"
OPS_DIR = PROJECT_ROOT / "OPS"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE = LOG_DIR / "playbook_enhancer.log"

# Key categories eligible for bolstering
BOLSTER_CATEGORIES = {
    "OUTBOUND", "CONTENT_FARM", "CONTENT_FORMAT", "APP_FACTORY",
    "TOOL_ALPHA", "GROWTH_HACK", "SEO_GEO_ASO", "MONETIZATION",
    "ECOM", "ECOM_ARB", "AI_ALPHA", "AI_INFLUENCER", "FREELANCE",
}

# Category-to-OPS-file-pattern mapping
# Each category maps to a list of glob-like stems (lowercase) to match against OPS filenames
CATEGORY_FILE_MAP: dict[str, list[str]] = {
    "OUTBOUND":      ["cold_email", "outbound", "outreach", "leads_outreach", "email_launch", "cold_email_launch"],
    "CONTENT_FARM":  ["content", "posting", "social", "content_factory", "content_posting", "content_syndication"],
    "CONTENT_FORMAT": ["content", "posting", "video", "carousel", "content_factory"],
    "APP_FACTORY":   ["app_factory", "app_quality", "app_clone", "mobile_app", "ramadan"],
    "TOOL_ALPHA":    ["tool", "automation", "scraper", "browser", "mcp", "automation_map"],
    "GROWTH_HACK":   ["growth", "edge", "grey_hat", "hack", "viral", "definitive_growth"],
    "SEO_GEO_ASO":   ["seo", "geo", "aso", "keyword", "ranking", "entity_seo"],
    "MONETIZATION":  ["monetiz", "revenue", "gumroad", "pricing", "affiliate", "whop"],
    "ECOM":          ["ecom", "arb", "product", "listing", "etsy", "amazon", "dropship"],
    "ECOM_ARB":      ["ecom", "arb", "dropship", "product", "viral_product"],
    "AI_ALPHA":      ["ai_agent", "automation", "tool", "mcp", "claude"],
    "AI_INFLUENCER": ["influencer", "nsfw", "persona", "findom", "fanvue"],
    "FREELANCE":     ["freelance", "fiverr", "upwork", "service", "freelance_arb"],
}

# Minimum synergy_score threshold for auto-bolstering high-score entries
HIGH_SCORE_THRESHOLD = 70

# Bolster log CSV headers
BOLSTER_LOG_HEADERS = [
    "alpha_id", "target_file", "category", "date_bolstered", "tactic_summary",
]

# Alpha Insights section header used as an anchor in target files
INSIGHTS_SECTION = "## Alpha Insights (Auto-Appended)"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def now_date() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")


def log(msg: str) -> None:
    """Append to log file and print to stderr."""
    ts = now_iso()
    line = f"[{ts}] {msg}"
    print(line, file=sys.stderr)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def safe_path(target: Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def clean_tactic_text(text: str) -> str:
    """Clean up tactic text for display: strip excess whitespace, truncate."""
    # Collapse whitespace
    cleaned = re.sub(r"\s+", " ", text).strip()
    # Remove leading/trailing quotes
    cleaned = cleaned.strip('"').strip("'")
    # Truncate at 600 chars
    if len(cleaned) > 600:
        cleaned = cleaned[:597] + "..."
    return cleaned


def safe_int(val: str, default: int = 0) -> int:
    """Parse int from string safely."""
    try:
        return int(str(val).strip())
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# OPS file index
# ---------------------------------------------------------------------------

def build_ops_index() -> dict[str, str]:
    """
    Build {lowercase_stem: full_path_str} for all OPS/*.md files.
    """
    index: dict[str, str] = {}
    ops = safe_path(OPS_DIR)
    if not ops.is_dir():
        return index
    for f in ops.iterdir():
        if f.is_file() and f.suffix == ".md":
            stem = f.stem.lower()
            index[stem] = str(f)
    return index


def find_target_file(category: str, tactic: str, ops_index: dict[str, str]) -> str | None:
    """
    Find the best OPS/*.md file for a given category + tactic.
    Returns absolute path string or None.
    """
    category_upper = category.strip().upper()
    search_terms = CATEGORY_FILE_MAP.get(category_upper, [])

    if not search_terms:
        return None

    # Also extract significant words from tactic for secondary matching
    tactic_words = set(re.findall(r"[a-z]{5,}", tactic.lower()))

    best_match: str | None = None
    best_score = 0

    for stem, path in ops_index.items():
        score = 0
        stem_lower = stem.replace("_", " ").lower()

        # Category keyword matches (strong signal)
        for term in search_terms:
            if term in stem_lower or term in stem:
                score += 3

        # Tactic word matches in filename (weak signal)
        for w in list(tactic_words)[:10]:
            if w in stem_lower:
                score += 1

        if score > best_score:
            best_score = score
            best_match = path

    # Require minimum relevance of 3 (at least one category keyword match)
    if best_score >= 3:
        return best_match

    return None


# ---------------------------------------------------------------------------
# Bolster log management
# ---------------------------------------------------------------------------

def read_bolster_log() -> set[str]:
    """Read already-bolstered alpha_ids from the log."""
    bolstered: set[str] = set()
    if not BOLSTER_LOG.exists():
        return bolstered
    with open(BOLSTER_LOG, "r", newline="", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aid = row.get("alpha_id", "").strip()
            if aid:
                bolstered.add(aid)
    return bolstered


def append_bolster_log(alpha_id: str, target_file: str, category: str,
                       tactic_summary: str) -> None:
    """Append a row to the bolster log CSV."""
    target = safe_path(BOLSTER_LOG)
    write_header = not target.exists()
    with open(target, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=BOLSTER_LOG_HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow({
            "alpha_id": alpha_id,
            "target_file": Path(target_file).name,
            "category": category,
            "date_bolstered": now_date(),
            "tactic_summary": tactic_summary[:200],
        })


# ---------------------------------------------------------------------------
# CSV read / write
# ---------------------------------------------------------------------------

def read_alpha_csv() -> tuple[list[str], list[dict]]:
    """Read ALPHA_STAGING.csv, return (fieldnames, rows)."""
    if not ALPHA_CSV.exists():
        log(f"ERROR: {ALPHA_CSV} not found")
        sys.exit(1)
    rows: list[dict] = []
    fieldnames: list[str] = []
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
# Eligibility checks
# ---------------------------------------------------------------------------

def is_bolster_eligible(row: dict, already_bolstered: set[str]) -> bool:
    """
    Determine if a row is eligible for playbook bolstering.

    Eligible if:
      A) status contains BOLSTER or APPROVED, and reviewer_notes mention an OPS file
      B) status is INTEGRATED (already routed by processor, shallow append done)
      C) High synergy_score (>70) in a key category, not yet bolstered
    """
    alpha_id = str(row.get("alpha_id", "")).strip()
    if not alpha_id:
        return False

    # Already bolstered? Skip.
    if alpha_id in already_bolstered:
        return False

    status = str(row.get("status", "")).strip().upper()
    reviewer_notes = str(row.get("reviewer_notes", "")).strip()
    category = str(row.get("category", "")).strip().upper()
    synergy = safe_int(row.get("synergy_score", "0"))
    tactic = str(row.get("tactic", "")).strip()

    # Must have tactic text
    if len(tactic) < 20:
        return False

    # Path A: status contains BOLSTER or APPROVED with OPS target in notes
    if "BOLSTER" in status or "APPROVED" in status:
        if "OPS" in reviewer_notes.upper() or ".md" in reviewer_notes.lower():
            return True

    # Path B: status INTEGRATED (already routed by alpha_auto_processor Route B)
    if status == "INTEGRATED":
        # Check that reviewer_notes mention integration target
        if "auto-integrated" in reviewer_notes.lower():
            return True

    # Path C: High synergy_score in a key category
    if synergy > HIGH_SCORE_THRESHOLD and category in BOLSTER_CATEGORIES:
        # Must be in a processable or approved-ish state
        if status in ("APPROVED", "INTEGRATED", "QUEUED_FOR_REVIEW", "PENDING_REVIEW"):
            return True

    return False


def extract_existing_target(row: dict) -> str | None:
    """
    If the alpha_auto_processor already identified a target file in
    reviewer_notes, extract its filename.
    Returns a filename like 'CONTENT_POSTING_GUIDE.md' or None.
    """
    notes = str(row.get("reviewer_notes", ""))
    # Pattern: "Auto-integrated into: FILENAME.md"
    m = re.search(r"(?:integrated|routed)\s+(?:into|to):\s*([\w\-\.]+\.md)", notes, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Core bolstering logic
# ---------------------------------------------------------------------------

def format_insight_section(row: dict) -> str:
    """Format a single alpha entry as a clean markdown insight section."""
    alpha_id = str(row.get("alpha_id", "UNKNOWN")).strip()
    source = str(row.get("source", "")).strip()
    source_url = str(row.get("source_url", "")).strip()
    category = str(row.get("category", "")).strip()
    tactic = clean_tactic_text(str(row.get("tactic", "")))
    roi = str(row.get("roi_potential", "")).strip()
    synergy = str(row.get("synergy_score", "")).strip()
    extracted = str(row.get("extracted_method", "")).strip()
    date = now_date()

    # Build the insight block
    lines = [
        f"### Alpha Insight: {alpha_id} — {date}",
        f"**Source:** {source}" + (f" ([link]({source_url}))" if source_url.startswith("http") else ""),
        f"**Category:** {category}",
    ]

    if extracted and len(extracted) > 5:
        lines.append(f"**Method:** {extracted}")

    lines.append(f"**Insight:** {tactic}")

    meta_parts = []
    if roi:
        meta_parts.append(f"ROI: {roi}")
    if synergy:
        meta_parts.append(f"Synergy: {synergy}")
    if meta_parts:
        lines.append(f"**Potential:** {' | '.join(meta_parts)}")

    lines.append("")  # trailing blank line

    return "\n".join(lines)


def append_insight_to_file(target_path: str, insight_block: str,
                           dry_run: bool = False) -> bool:
    """
    Append an insight block to a target OPS file.

    If the file already has an "## Alpha Insights (Auto-Appended)" section,
    append below it. Otherwise, create the section at the bottom.

    Returns True if successful (or would have been in dry-run).
    """
    target = safe_path(Path(target_path))

    if not target.exists():
        log(f"  WARNING: target file does not exist: {target}")
        return False

    if dry_run:
        return True

    # Read existing content
    content = target.read_text(errors="replace")

    # Check if insights section already exists
    if INSIGHTS_SECTION in content:
        # Append after the existing section (at the end of the file, since the
        # section is typically at the bottom)
        new_content = content.rstrip() + "\n\n" + insight_block + "\n"
    else:
        # Create the section at the bottom
        new_content = (
            content.rstrip()
            + "\n\n---\n\n"
            + INSIGHTS_SECTION
            + "\n\n"
            + "_Insights auto-appended by playbook_enhancer.py. Review and integrate as needed._\n\n"
            + insight_block
            + "\n"
        )

    with open(target, "w", errors="replace") as f:
        f.write(new_content)

    return True


# ---------------------------------------------------------------------------
# Scan mode
# ---------------------------------------------------------------------------

def scan_eligible(rows: list[dict], already_bolstered: set[str],
                  category_filter: str | None = None) -> list[dict]:
    """Return list of eligible rows."""
    eligible: list[dict] = []
    for row in rows:
        if not is_bolster_eligible(row, already_bolstered):
            continue
        if category_filter:
            cat = str(row.get("category", "")).strip().upper()
            if cat != category_filter.upper():
                continue
        eligible.append(row)
    return eligible


def cmd_scan(rows: list[dict], already_bolstered: set[str],
             category_filter: str | None = None) -> None:
    """Show entries eligible for bolstering."""
    eligible = scan_eligible(rows, already_bolstered, category_filter)

    if not eligible:
        print("\nNo entries eligible for bolstering.")
        if category_filter:
            print(f"  (filtered to category: {category_filter})")
        return

    # Summarize by category
    by_cat: Counter = Counter()
    for row in eligible:
        cat = str(row.get("category", "UNKNOWN")).strip().upper()
        by_cat[cat] += 1

    print(f"\n=== BOLSTER-ELIGIBLE ENTRIES: {len(eligible)} ===\n")

    for cat, count in by_cat.most_common(20):
        bar = "#" * min(count, 50)
        print(f"  {cat:20s} {count:>5d}  {bar}")

    print(f"\nTotal eligible: {len(eligible)}")
    print(f"Already bolstered: {len(already_bolstered)}")

    # Show top 10 samples
    print(f"\n--- Sample entries (first 10) ---\n")
    for row in eligible[:10]:
        aid = row.get("alpha_id", "?")
        cat = row.get("category", "?")
        tactic = str(row.get("tactic", ""))[:80]
        status = row.get("status", "?")
        synergy = row.get("synergy_score", "?")
        print(f"  [{aid}] {cat} (status={status}, synergy={synergy})")
        print(f"    {tactic}...")
        print()


# ---------------------------------------------------------------------------
# Run mode
# ---------------------------------------------------------------------------

def cmd_run(rows: list[dict], fieldnames: list[str], ops_index: dict[str, str],
            already_bolstered: set[str], batch_size: int = 20,
            dry_run: bool = False, category_filter: str | None = None) -> dict:
    """Execute bolstering on eligible entries."""
    eligible = scan_eligible(rows, already_bolstered, category_filter)

    if not eligible:
        print("\nNo entries eligible for bolstering.")
        return {"processed": 0, "bolstered": 0, "skipped": 0, "no_target": 0}

    # Cap at batch size
    batch = eligible[:batch_size]

    stats: Counter = Counter()
    stats["total_eligible"] = len(eligible)
    stats["batch_size"] = len(batch)

    mode = "DRY RUN" if dry_run else "LIVE"
    log(f"=== Playbook Enhancer starting ({mode}) ===")
    log(f"Eligible: {len(eligible)}, Processing: {len(batch)}")

    for row in batch:
        alpha_id = str(row.get("alpha_id", "UNKNOWN")).strip()
        category = str(row.get("category", "")).strip().upper()
        tactic = str(row.get("tactic", "")).strip()

        # Step 1: Determine target file
        # First check if the processor already identified one
        existing_target_name = extract_existing_target(row)
        target_path: str | None = None

        if existing_target_name:
            # Look up in ops_index
            stem = existing_target_name.replace(".md", "").lower()
            target_path = ops_index.get(stem)

        # If no existing target found, find one by category
        if not target_path:
            target_path = find_target_file(category, tactic, ops_index)

        if not target_path:
            stats["no_target"] += 1
            log(f"  [{alpha_id}] SKIP: no target file found for category {category}")
            continue

        target_name = Path(target_path).name

        # Step 2: Check if this exact insight is already in the target (dedup)
        if not dry_run and Path(target_path).exists():
            existing_content = Path(target_path).read_text(errors="replace")
            if alpha_id in existing_content:
                stats["already_present"] += 1
                log(f"  [{alpha_id}] SKIP: already present in {target_name}")
                # Still mark as bolstered so we don't re-check
                already_bolstered.add(alpha_id)
                append_bolster_log(alpha_id, target_path, category,
                                   tactic[:200])
                # Update CSV row
                notes = str(row.get("reviewer_notes", ""))
                row["reviewer_notes"] = notes + f" [BOLSTERED: {now_date()}, {target_name}]"
                continue

        # Step 3: Format the insight
        insight_block = format_insight_section(row)

        # Step 4: Append to target file
        success = append_insight_to_file(target_path, insight_block, dry_run=dry_run)

        if not success:
            stats["failed"] += 1
            log(f"  [{alpha_id}] FAILED: could not write to {target_name}")
            continue

        # Step 5: Update tracking
        if not dry_run:
            # Update reviewer_notes in CSV
            notes = str(row.get("reviewer_notes", ""))
            row["reviewer_notes"] = notes + f" [BOLSTERED: {now_date()}, {target_name}]"

            # Append to bolster log
            append_bolster_log(alpha_id, target_path, category, tactic[:200])
            already_bolstered.add(alpha_id)

        stats["bolstered"] += 1
        log(f"  [{alpha_id}] BOLSTERED -> {target_name} ({category})")

    stats["processed"] = stats["bolstered"] + stats["no_target"] + stats.get("failed", 0) + stats.get("already_present", 0)

    # Write back CSV if not dry run
    if not dry_run and stats["bolstered"] > 0:
        write_alpha_csv(fieldnames, rows)
        log("CSV updated with bolster annotations")

    # Report
    print(f"""
=== PLAYBOOK ENHANCER REPORT ({mode}) ===

Total eligible:     {stats['total_eligible']}
Batch processed:    {stats['processed']}

Results:
  Bolstered:        {stats['bolstered']}
  No target found:  {stats['no_target']}
  Already present:  {stats.get('already_present', 0)}
  Failed:           {stats.get('failed', 0)}
""")

    log(f"=== Playbook Enhancer complete: {stats['bolstered']} bolstered ===")
    return dict(stats)


# ---------------------------------------------------------------------------
# Status mode
# ---------------------------------------------------------------------------

def cmd_status() -> None:
    """Show bolstering statistics."""
    print("\n=== PLAYBOOK ENHANCER STATUS ===\n")

    # Read bolster log
    already_bolstered = read_bolster_log()
    print(f"Total bolstered entries: {len(already_bolstered)}")

    # Breakdown by category and target file
    if BOLSTER_LOG.exists():
        by_cat: Counter = Counter()
        by_file: Counter = Counter()
        with open(BOLSTER_LOG, "r", newline="", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = row.get("category", "UNKNOWN")
                target = row.get("target_file", "UNKNOWN")
                by_cat[cat] += 1
                by_file[target] += 1

        if by_cat:
            print("\nBy category:")
            for cat, count in by_cat.most_common(20):
                bar = "#" * min(count, 40)
                print(f"  {cat:25s} {count:>5d}  {bar}")

        if by_file:
            print("\nTop target files:")
            for fname, count in by_file.most_common(15):
                print(f"  {fname:45s} {count:>5d}")
    else:
        print("\nNo bolster log found yet. Run --run to start bolstering.")

    # Check eligible count
    _, rows = read_alpha_csv()
    eligible = scan_eligible(rows, already_bolstered)
    print(f"\nCurrently eligible for bolstering: {len(eligible)}")

    # OPS file count
    ops_index = build_ops_index()
    print(f"OPS/*.md files indexed: {len(ops_index)}")

    # Log tail
    if LOG_FILE.exists():
        print(f"\nRecent log ({LOG_FILE.name}):")
        lines = LOG_FILE.read_text().strip().split("\n")
        for line in lines[-5:]:
            print(f"  {line}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Playbook Enhancer: deep-integrate alpha insights into OPS playbooks."
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Find entries eligible for bolstering (read-only)",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute bolstering (default batch of 20)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Number of entries to process per run (default: 20)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show bolstering stats",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without writing any files",
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Filter to specific category (e.g. OUTBOUND, CONTENT_FARM)",
    )
    args = parser.parse_args()

    if args.status:
        cmd_status()
        return

    if not (args.scan or args.run):
        parser.print_help()
        return

    # Read data
    fieldnames, rows = read_alpha_csv()
    already_bolstered = read_bolster_log()
    ops_index = build_ops_index()

    log(f"Loaded {len(rows)} rows, {len(already_bolstered)} already bolstered, {len(ops_index)} OPS files")

    if args.scan:
        cmd_scan(rows, already_bolstered, args.category)
        return

    if args.run:
        cmd_run(
            rows,
            fieldnames,
            ops_index,
            already_bolstered,
            batch_size=args.batch_size,
            dry_run=args.dry_run,
            category_filter=args.category,
        )
        return


if __name__ == "__main__":
    main()
