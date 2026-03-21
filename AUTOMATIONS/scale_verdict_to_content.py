#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Scale Verdict to Content Pipeline
============================================
Wires SCALE verdicts from alpha_screening.py to inline content generation.
High-scoring alpha automatically generates social content in @pipelineabuser voice.

Reads ALPHA_STAGING.csv, finds entries meeting SCALE/APPROVED + HIGH/HIGHEST +
synergy > 70 criteria, generates tweets, threads, Reddit posts, and newsletter
sections. Tracks everything in ALPHA_CONTENT_LOG.csv.

CLI:
  --scan          Find entries eligible for content generation
  --run           Generate content (default batch of 5)
  --batch-size N  Process N entries
  --status        Show generation stats
  --dry-run       Preview without writing

Usage:
  python3 AUTOMATIONS/scale_verdict_to_content.py --scan
  python3 AUTOMATIONS/scale_verdict_to_content.py --run --batch-size 10
  python3 AUTOMATIONS/scale_verdict_to_content.py --run --dry-run
  python3 AUTOMATIONS/scale_verdict_to_content.py --status
"""

import csv
import re
import sys
import argparse
import hashlib
import logging
import random
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
CONTENT_DIR = PROJECT_ROOT / "CONTENT" / "social" / "auto_generated"
LOG_DIR = AUTOMATIONS_DIR / "logs"

ALPHA_STAGING_CSV = LEDGER_DIR / "ALPHA_STAGING.csv"
ALPHA_CONTENT_LOG_CSV = LEDGER_DIR / "ALPHA_CONTENT_LOG.csv"

CONTENT_LOG_FIELDS = [
    "alpha_id", "category", "content_pieces_generated",
    "date_generated", "output_file",
]

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "scale_to_content.log"

logger = logging.getLogger("scale_to_content")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(fh)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(sh)


# ---------------------------------------------------------------------------
# GUARDRAILS
# ---------------------------------------------------------------------------
def safe_path(target) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# ---------------------------------------------------------------------------
# AI SLOP FILTER (from copy-style.md)
# ---------------------------------------------------------------------------
AI_SLOP_WORDS = {
    "additionally", "moreover", "furthermore", "testament", "landscape",
    "paradigm", "leverage", "utilize", "delve", "unpack", "comprehensive",
    "robust", "streamlined", "game-changer", "unlock", "elevate",
    "cutting-edge", "innovative", "revolutionary", "empower", "seamless",
    "frictionless", "journey", "groundbreaking", "nestled", "tapestry",
    "synergy", "holistic", "disruptive", "ecosystem",
}


def clean_slop(text: str) -> str:
    """Remove AI vocabulary and em dashes from text."""
    cleaned = text
    # Kill em dashes
    cleaned = cleaned.replace("\u2014", ". ").replace("\u2013", ", ")
    cleaned = cleaned.replace("---", ". ").replace("--", ", ")
    # Kill AI slop words
    for word in AI_SLOP_WORDS:
        pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        cleaned = pattern.sub("", cleaned)
    # Collapse double spaces
    cleaned = re.sub(r"  +", " ", cleaned)
    # Collapse double periods
    cleaned = re.sub(r"\.(\s*\.)+", ".", cleaned)
    return cleaned.strip()


# ---------------------------------------------------------------------------
# CONTENT SEED EXTRACTION
# ---------------------------------------------------------------------------
def extract_content_seed(entry: dict) -> str:
    """Extract the best content seed from an alpha entry.

    Pulls from tactic, extracted_method, reviewer_notes in priority order.
    Cleans AI slop and returns a crisp seed string.
    """
    # Priority: tactic > extracted_method > reviewer_notes
    raw = ""
    tactic = (entry.get("tactic") or "").strip()
    extracted = (entry.get("extracted_method") or "").strip()
    notes = (entry.get("reviewer_notes") or "").strip()

    if tactic and len(tactic) > 10:
        raw = tactic
    elif extracted and len(extracted) > 10:
        raw = extracted
    elif notes and len(notes) > 10:
        # Strip common prefixes from reviewer notes
        raw = re.sub(r"^APPROVED\.?\s*", "", notes, flags=re.IGNORECASE)
        raw = re.sub(r"^\[CONTENT_GENERATED[^\]]*\]\s*", "", raw)
    else:
        # Fall back to category + source combo
        cat = entry.get("category", "alpha")
        source = entry.get("source", "unknown")
        raw = f"{cat.lower().replace('_', ' ')} tactic from {source}"

    return clean_slop(raw)


# ---------------------------------------------------------------------------
# CONTENT GENERATION TEMPLATES
# ---------------------------------------------------------------------------
# Templates follow copy-style.md: consequence-first hooks, specific numbers,
# @pipelineabuser energy, lowercase casual, no em dashes, no AI slop.

TWEET_TEMPLATES = [
    # Template: "[specific result/number]. [how]. [tool/method]. [one-liner insight]."
    "found this {category} tactic. {seed_short}. most people sleep on this. the ones who don't are printing.",
    "{seed_short}. tested it. it works. stop overthinking and just run it.",
    "alpha drop: {seed_short}. roi potential is {roi}. if you're not on this you're leaving money on the table.",
]

THREAD_OPENERS = [
    # Template: "[bold claim with number]. here's the exact breakdown:"
    "{seed_short}.\n\nmost people miss this entirely. here's the exact breakdown:",
    "i spent hours screening alpha entries. this one stood out.\n\n{seed_short}.\n\nthread on why this matters and how to run it:",
    "alpha entry {alpha_id} scored {synergy} synergy. that's top tier.\n\n{seed_short}.\n\nhere's the full play:",
]

THREAD_BODY_TEMPLATES = [
    # 5-7 tweet thread body segments
    [
        "1/ the core insight: {seed_full}",
        "2/ why this works: {category} is underexploited right now. the window is open but it won't be forever.",
        "3/ the play: take this tactic. apply it to {niches}. the synergy score on this was {synergy}/100.",
        "4/ most people will read this and do nothing. the 3% who actually execute will see results in 2-4 weeks.",
        "5/ roi potential: {roi}. that's not hype. that's based on screening criteria with real data points.",
        "6/ if you want more alpha like this, i screen hundreds of entries weekly. the ones that hit SCALE verdict are the ones worth running.",
    ],
]

REDDIT_TEMPLATES = [
    # Template: "I [did specific thing]. Here's what happened and what I'd change."
    """I screened {total_screened}+ alpha entries this week. This one hit SCALE verdict.

**The tactic:** {seed_full}

**Category:** {category}
**ROI potential:** {roi}
**Synergy score:** {synergy}/100

**Why it matters:**
{category} tactics with synergy scores above 70 have the highest hit rate in our screening system. This isn't theory. It's based on multi-factor scoring with evidence quality, replicability, and time decay factored in.

**What I'd do with this:**
Start small. Test the core mechanic in one niche. Track results for 14 days. If the numbers hold, scale it across {niches}.

**What I'd change:**
Nothing yet. The screening data supports this. But I'd set a hard kill switch at 30 days if ROI doesn't materialize.

Sharing because most alpha gets hoarded. The people who share freely tend to find more.""",
]

NEWSLETTER_TEMPLATES = [
    """## Alpha Spotlight: {category}

**Entry:** {alpha_id} | **Source:** {source} | **ROI:** {roi} | **Synergy:** {synergy}/100

{seed_full}

This entry cleared our SCALE threshold after multi-factor screening. Evidence quality, replicability, time decay, and historical performance all checked out.

**The play:** {seed_short}. Apply across {niches}. Track for 14 days before doubling down.

**Why now:** {category} alpha decays. The window on this is measured in weeks, not months. If you're going to run it, run it this week.

---""",
]


def _shorten(text: str, max_len: int = 120) -> str:
    """Shorten text to max_len at a sentence boundary."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_period = truncated.rfind(".")
    if last_period > 40:
        return truncated[: last_period + 1]
    return truncated.rstrip() + "."


def _category_label(category: str) -> str:
    """Convert SCREAMING_SNAKE to readable label."""
    return category.lower().replace("_", " ")


def generate_content_for_entry(entry: dict, total_screened: int = 500) -> dict:
    """Generate all content pieces for a single qualifying alpha entry.

    Returns dict with keys: tweets, thread, reddit, newsletter, metadata.
    """
    seed_full = extract_content_seed(entry)
    seed_short = _shorten(seed_full, 140)
    alpha_id = entry.get("alpha_id", "UNKNOWN")
    category = entry.get("category", "ALPHA")
    roi = entry.get("roi_potential", "HIGH")
    source = entry.get("source", "unknown")
    niches_raw = entry.get("applicable_niches", "")
    niches = niches_raw if niches_raw else "tech, fitness, faith"

    synergy_raw = entry.get("synergy_score", "")
    try:
        synergy = int(float(synergy_raw))
    except (ValueError, TypeError):
        synergy = 75  # Default for qualified entries

    fmt = {
        "seed_full": seed_full,
        "seed_short": seed_short,
        "alpha_id": alpha_id,
        "category": _category_label(category),
        "roi": roi,
        "source": source,
        "niches": niches,
        "synergy": synergy,
        "total_screened": total_screened,
    }

    # --- 3 Tweets ---
    tweets = []
    used_templates = random.sample(TWEET_TEMPLATES, min(3, len(TWEET_TEMPLATES)))
    for tmpl in used_templates:
        tweet = clean_slop(tmpl.format(**fmt))
        # Enforce 280 char limit
        if len(tweet) > 280:
            tweet = tweet[:277].rstrip() + "."
        tweets.append(tweet)

    # --- 1 Thread (5-7 tweets) ---
    opener_tmpl = random.choice(THREAD_OPENERS)
    thread_opener = clean_slop(opener_tmpl.format(**fmt))
    body_templates = random.choice(THREAD_BODY_TEMPLATES)
    thread_parts = [thread_opener]
    for part_tmpl in body_templates:
        part = clean_slop(part_tmpl.format(**fmt))
        thread_parts.append(part)
    # Add a closing tweet
    closers = [
        "7/ that's the play. run it or don't. the alpha is free.",
        "7/ bookmark this. come back in 2 weeks. see if it hit.",
        "7/ sharing alpha is free. executing on it is what separates.",
    ]
    thread_parts.append(random.choice(closers))

    # --- 1 Reddit Post ---
    reddit_tmpl = random.choice(REDDIT_TEMPLATES)
    reddit_post = clean_slop(reddit_tmpl.format(**fmt))

    # --- 1 Newsletter Section ---
    newsletter_tmpl = random.choice(NEWSLETTER_TEMPLATES)
    newsletter = clean_slop(newsletter_tmpl.format(**fmt))

    pieces_count = len(tweets) + 1 + 1 + 1  # tweets + thread + reddit + newsletter

    return {
        "tweets": tweets,
        "thread": thread_parts,
        "reddit": reddit_post,
        "newsletter": newsletter,
        "metadata": {
            "alpha_id": alpha_id,
            "category": category,
            "content_pieces_generated": pieces_count,
            "seed_preview": seed_short[:80],
        },
    }


# ---------------------------------------------------------------------------
# ALPHA_STAGING.CSV READING / WRITING
# ---------------------------------------------------------------------------
def read_alpha_staging() -> list:
    """Read all entries from ALPHA_STAGING.csv."""
    if not ALPHA_STAGING_CSV.exists():
        logger.error("ALPHA_STAGING.csv not found at %s", ALPHA_STAGING_CSV)
        return []
    entries = []
    try:
        with open(ALPHA_STAGING_CSV, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(dict(row))
    except Exception as e:
        logger.error("Failed to read ALPHA_STAGING.csv: %s", e)
    return entries


def read_content_log() -> dict:
    """Read existing ALPHA_CONTENT_LOG.csv, return set of processed alpha_ids."""
    processed = {}
    if not ALPHA_CONTENT_LOG_CSV.exists():
        return processed
    try:
        with open(ALPHA_CONTENT_LOG_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                aid = row.get("alpha_id", "")
                if aid:
                    processed[aid] = row
    except Exception:
        pass
    return processed


def append_content_log(records: list):
    """Append records to ALPHA_CONTENT_LOG.csv."""
    path = safe_path(ALPHA_CONTENT_LOG_CSV)
    file_exists = path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CONTENT_LOG_FIELDS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerows(records)


def update_alpha_staging_notes(alpha_id: str, date_str: str, all_entries: list):
    """Update reviewer_notes for a specific alpha_id with [CONTENT_GENERATED] tag.

    Modifies the all_entries list in place. The caller must write back the full CSV.
    """
    tag = f"[CONTENT_GENERATED: {date_str}]"
    for entry in all_entries:
        if entry.get("alpha_id") == alpha_id:
            existing_notes = entry.get("reviewer_notes", "") or ""
            if "[CONTENT_GENERATED" not in existing_notes:
                if existing_notes:
                    entry["reviewer_notes"] = f"{tag} {existing_notes}"
                else:
                    entry["reviewer_notes"] = tag
            break


def write_alpha_staging(entries: list):
    """Rewrite the full ALPHA_STAGING.csv with updated entries.

    Preserves original field order from the file.
    """
    if not entries:
        return
    path = safe_path(ALPHA_STAGING_CSV)

    # Read original header order
    original_fields = []
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                original_fields = reader.fieldnames or []
        except Exception:
            pass

    # Use original field order, or derive from entries
    if not original_fields:
        all_keys = set()
        for e in entries:
            all_keys.update(e.keys())
        original_fields = sorted(all_keys)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=original_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(entries)


# ---------------------------------------------------------------------------
# QUALIFYING FILTER
# ---------------------------------------------------------------------------
def find_qualifying_entries(entries: list, content_log: dict) -> list:
    """Find alpha entries eligible for content generation.

    Criteria:
    - status is APPROVED or SCALE
    - roi_potential is HIGH or HIGHEST
    - synergy_score > 70
    - NOT already content-generated (check reviewer_notes for [CONTENT_GENERATED])
    - NOT already in content log
    """
    qualified = []
    for entry in entries:
        alpha_id = entry.get("alpha_id", "")
        status = (entry.get("status") or "").strip().upper()
        roi = (entry.get("roi_potential") or "").strip().upper()
        notes = (entry.get("reviewer_notes") or "").strip()

        # Status check
        if status not in ("APPROVED", "SCALE"):
            continue

        # ROI check
        if roi not in ("HIGH", "HIGHEST"):
            continue

        # Synergy score check
        synergy_raw = entry.get("synergy_score", "")
        try:
            synergy = float(synergy_raw)
        except (ValueError, TypeError):
            # If synergy_score is empty or invalid, skip
            continue
        if synergy <= 70:
            continue

        # Already generated check (reviewer_notes)
        if "[CONTENT_GENERATED" in notes:
            continue

        # Already in content log check
        if alpha_id in content_log:
            continue

        qualified.append(entry)

    return qualified


# ---------------------------------------------------------------------------
# OUTPUT FORMATTING
# ---------------------------------------------------------------------------
def format_content_markdown(content: dict, entry: dict) -> str:
    """Format generated content as markdown for the output file."""
    meta = content["metadata"]
    alpha_id = meta["alpha_id"]
    category = meta["category"]
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append(f"\n{'='*72}")
    lines.append(f"## {alpha_id} | {category} | Generated {now_str}")
    lines.append(f"Source: {entry.get('source', 'unknown')} | ROI: {entry.get('roi_potential', 'N/A')} | Synergy: {entry.get('synergy_score', 'N/A')}")
    lines.append(f"{'='*72}\n")

    # Tweets
    lines.append("### Tweets (3x standalone)\n")
    for i, tweet in enumerate(content["tweets"], 1):
        lines.append(f"**Tweet {i}:**")
        lines.append(f"```")
        lines.append(tweet)
        lines.append(f"```")
        lines.append(f"({len(tweet)} chars)\n")

    # Thread
    lines.append("### Thread (5-7 tweets)\n")
    for i, part in enumerate(content["thread"]):
        if i == 0:
            lines.append(f"**Thread opener:**")
        else:
            lines.append(f"**{i}/{len(content['thread'])-1}:**")
        lines.append(f"```")
        lines.append(part)
        lines.append(f"```\n")

    # Reddit
    lines.append("### Reddit Post Draft\n")
    lines.append("```")
    lines.append(content["reddit"])
    lines.append("```\n")

    # Newsletter
    lines.append("### Newsletter Section\n")
    lines.append(content["newsletter"])
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# COMMANDS
# ---------------------------------------------------------------------------
def cmd_scan(args):
    """Find entries eligible for content generation."""
    entries = read_alpha_staging()
    if not entries:
        logger.info("No entries found in ALPHA_STAGING.csv")
        return

    content_log = read_content_log()
    qualified = find_qualifying_entries(entries, content_log)

    logger.info("Scanned %d total entries", len(entries))
    logger.info("Found %d qualifying entries for content generation", len(qualified))

    if qualified:
        print(f"\n{'='*60}")
        print(f"  SCALE-TO-CONTENT SCAN RESULTS")
        print(f"{'='*60}")
        print(f"  Total entries scanned:  {len(entries)}")
        print(f"  Qualifying entries:     {len(qualified)}")
        print(f"  Already generated:      {len(content_log)}")
        print()

        # Category breakdown
        cats = defaultdict(int)
        for q in qualified:
            cats[q.get("category", "UNKNOWN")] += 1

        print(f"  By Category:")
        for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
            print(f"    {cat:25s} {count}")
        print()

        # Preview top entries
        print(f"  Top {min(10, len(qualified))} entries:")
        for q in qualified[:10]:
            aid = q.get("alpha_id", "?")
            cat = q.get("category", "?")
            roi = q.get("roi_potential", "?")
            syn = q.get("synergy_score", "?")
            seed = extract_content_seed(q)[:60]
            print(f"    {aid:10s} | {cat:20s} | ROI:{roi:8s} | syn:{syn:>4s} | {seed}...")
        if len(qualified) > 10:
            print(f"    ... and {len(qualified) - 10} more")
        print(f"{'='*60}\n")


def cmd_run(args):
    """Generate content for qualifying entries."""
    entries = read_alpha_staging()
    if not entries:
        logger.info("No entries found in ALPHA_STAGING.csv")
        return

    content_log = read_content_log()
    qualified = find_qualifying_entries(entries, content_log)

    if not qualified:
        logger.info("No qualifying entries found. Run --scan to check criteria.")
        return

    batch_size = args.batch_size
    batch = qualified[:batch_size]
    dry_run = args.dry_run

    today = datetime.now(timezone.utc).strftime("%Y_%m_%d")
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_filename = f"alpha_content_{today}.md"
    output_path = safe_path(CONTENT_DIR / output_filename)

    logger.info("Processing %d entries (batch_size=%d, dry_run=%s)",
                len(batch), batch_size, dry_run)

    all_content_md = []
    log_records = []
    total_pieces = 0

    for entry in batch:
        alpha_id = entry.get("alpha_id", "UNKNOWN")
        logger.info("Generating content for %s (%s)",
                     alpha_id, entry.get("category", "?"))

        content = generate_content_for_entry(entry, total_screened=len(entries))
        md_block = format_content_markdown(content, entry)
        all_content_md.append(md_block)

        pieces = content["metadata"]["content_pieces_generated"]
        total_pieces += pieces

        log_records.append({
            "alpha_id": alpha_id,
            "category": entry.get("category", ""),
            "content_pieces_generated": pieces,
            "date_generated": date_str,
            "output_file": str(output_path.relative_to(PROJECT_ROOT)),
        })

        # Update reviewer_notes in memory
        update_alpha_staging_notes(alpha_id, date_str, entries)

        if dry_run:
            print(f"\n  [DRY RUN] Would generate for {alpha_id}:")
            print(f"    Category: {entry.get('category', '?')}")
            print(f"    Seed: {extract_content_seed(entry)[:80]}...")
            print(f"    Pieces: {pieces}")
            for i, tweet in enumerate(content["tweets"], 1):
                print(f"    Tweet {i}: {tweet[:80]}...")
        else:
            logger.debug("Generated %d pieces for %s", pieces, alpha_id)

    if dry_run:
        print(f"\n  [DRY RUN] Total: {total_pieces} content pieces for {len(batch)} entries")
        print(f"  [DRY RUN] Would write to: {output_path.relative_to(PROJECT_ROOT)}")
        print(f"  [DRY RUN] Would update ALPHA_STAGING.csv reviewer_notes")
        print(f"  [DRY RUN] Would append to ALPHA_CONTENT_LOG.csv")
        return

    # --- Write content file (append mode) ---
    output_path.parent.mkdir(parents=True, exist_ok=True)
    header = ""
    if not output_path.exists():
        header = (
            f"# Auto-Generated Alpha Content | {date_str}\n"
            f"# Generated by scale_verdict_to_content.py\n"
            f"# Voice: @pipelineabuser | copy-style.md compliant\n"
            f"# Status: PENDING_REVIEW\n\n"
        )
    with open(output_path, "a", encoding="utf-8") as f:
        if header:
            f.write(header)
        for block in all_content_md:
            f.write(block)
            f.write("\n")

    logger.info("Wrote %d content blocks to %s",
                len(all_content_md), output_path.relative_to(PROJECT_ROOT))

    # --- Update ALPHA_STAGING.csv ---
    write_alpha_staging(entries)
    logger.info("Updated reviewer_notes for %d entries in ALPHA_STAGING.csv", len(batch))

    # --- Append to ALPHA_CONTENT_LOG.csv ---
    append_content_log(log_records)
    logger.info("Appended %d records to ALPHA_CONTENT_LOG.csv", len(log_records))

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"  CONTENT GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"  Entries processed:      {len(batch)}")
    print(f"  Total pieces generated: {total_pieces}")
    print(f"  Output file:            {output_path.relative_to(PROJECT_ROOT)}")
    print(f"  Content log updated:    LEDGER/ALPHA_CONTENT_LOG.csv")
    print(f"  Staging CSV updated:    LEDGER/ALPHA_STAGING.csv")
    print()

    # Breakdown
    for rec in log_records:
        print(f"    {rec['alpha_id']:10s} | {rec['category']:20s} | {rec['content_pieces_generated']} pieces")
    print(f"{'='*60}\n")


def cmd_status(args):
    """Show generation stats."""
    content_log = read_content_log()
    entries = read_alpha_staging()
    qualified = find_qualifying_entries(entries, read_content_log())

    # Stats from content log
    total_generated = len(content_log)
    total_pieces = 0
    cats = defaultdict(int)
    dates = defaultdict(int)
    for rec in content_log.values():
        try:
            total_pieces += int(rec.get("content_pieces_generated", 0))
        except (ValueError, TypeError):
            pass
        cats[rec.get("category", "UNKNOWN")] += 1
        dates[rec.get("date_generated", "unknown")] += 1

    print(f"\n{'='*60}")
    print(f"  SCALE-TO-CONTENT PIPELINE STATUS")
    print(f"{'='*60}")
    print()
    print(f"  Alpha entries generated:   {total_generated}")
    print(f"  Total content pieces:      {total_pieces}")
    print(f"  Pending (qualify now):     {len(qualified)}")
    print()

    if cats:
        print(f"  By Category:")
        for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
            print(f"    {cat:25s} {count}")
        print()

    if dates:
        print(f"  By Date:")
        for dt, count in sorted(dates.items(), reverse=True)[:10]:
            print(f"    {dt:15s} {count} entries")
        print()

    # Check output files
    if CONTENT_DIR.exists():
        output_files = sorted(CONTENT_DIR.glob("alpha_content_*.md"))
        if output_files:
            print(f"  Output Files:")
            for of in output_files[-5:]:
                try:
                    size = of.stat().st_size
                except Exception:
                    size = 0
                print(f"    {of.name:40s} {size:>8,d} bytes")
            if len(output_files) > 5:
                print(f"    ... and {len(output_files) - 5} more")
            print()

    print(f"  Log: {LOG_FILE.relative_to(PROJECT_ROOT)}")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Scale Verdict to Content Pipeline"
    )
    parser.add_argument("--scan", action="store_true",
                        help="Find entries eligible for content generation")
    parser.add_argument("--run", action="store_true",
                        help="Generate content (default batch of 5)")
    parser.add_argument("--batch-size", type=int, default=5,
                        help="Number of entries to process (default: 5)")
    parser.add_argument("--status", action="store_true",
                        help="Show generation stats")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing")

    args = parser.parse_args()

    # Default to --status if no args
    if not any([args.scan, args.run, args.status]):
        parser.print_help()
        print()
        cmd_status(args)
        return

    if args.scan:
        cmd_scan(args)

    if args.run:
        cmd_run(args)

    if args.status and not args.run and not args.scan:
        cmd_status(args)


if __name__ == "__main__":
    main()
