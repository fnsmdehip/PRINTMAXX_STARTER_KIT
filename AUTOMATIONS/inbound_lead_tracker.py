#!/usr/bin/env python3
"""
PRINTMAXX Inbound Lead Tracker
================================

Captures and tracks inbound leads from all PRINTMAXX touchpoints:
  - Social media engagement (Twitter replies, DMs, mentions)
  - Email form submissions (FormSubmit.co via lead magnets + PWAs)
  - Reddit / forum interactions
  - Freelance opportunity responses
  - Product inquiries

Lead scoring ladder:
  COLD      -> first interaction, no explicit interest
  WARM      -> 2+ interactions OR engaged meaningfully with content
  HOT       -> requested price/product info, signed up to lead magnet
  CONVERTED -> purchased, subscribed, or hired

Usage:
    python3 AUTOMATIONS/inbound_lead_tracker.py --status
    python3 AUTOMATIONS/inbound_lead_tracker.py --stats
    python3 AUTOMATIONS/inbound_lead_tracker.py --scan
    python3 AUTOMATIONS/inbound_lead_tracker.py --scan --dry-run
    python3 AUTOMATIONS/inbound_lead_tracker.py --add --platform twitter --username @someone --type reply --score warm
    python3 AUTOMATIONS/inbound_lead_tracker.py --add --platform reddit --username u/someone --type comment --score cold --source-post "https://reddit.com/..."
    python3 AUTOMATIONS/inbound_lead_tracker.py --upgrade --platform twitter --username @someone --score hot
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEADS_CSV = PROJECT_ROOT / "LEDGER" / "INBOUND_LEADS.csv"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE = LOG_DIR / "inbound_lead_tracker.log"

REDDIT_SCRAPER_DIR = PROJECT_ROOT / "AUTOMATIONS" / "reddit_scraper_output"
TWITTER_SCRAPER_DIR = PROJECT_ROOT / "AUTOMATIONS" / "twitter_scraper_output"
FREELANCE_RESPONSES_DIR = PROJECT_ROOT / "CONTENT" / "freelance_responses"

# CSV column order must match LEDGER/INBOUND_LEADS.csv header
CSV_HEADERS = [
    "timestamp",
    "username",
    "platform",
    "engagement_type",
    "source_post",
    "score",
    "lead_type",
    "status",
    "direction",
]

# Valid score values (ordered by warmth)
SCORE_ORDER = ["COLD", "WARM", "HOT", "CONVERTED"]

# Valid platforms
PLATFORMS = {
    "twitter",
    "reddit",
    "email",
    "freelance",
    "direct",
    "formsubmit",
    "instagram",
    "tiktok",
    "youtube",
}


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------

def safe_path(target: Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(msg: str, level: str = "INFO") -> None:
    ts = _now_iso()
    line = f"[{ts}] [LEAD_TRACKER] [{level}] {msg}"
    print(line)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def _ensure_csv() -> None:
    """Create INBOUND_LEADS.csv with header if it does not exist."""
    safe_path(LEADS_CSV)
    LEADS_CSV.parent.mkdir(parents=True, exist_ok=True)
    if not LEADS_CSV.exists() or LEADS_CSV.stat().st_size == 0:
        with open(safe_path(LEADS_CSV), "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_HEADERS)
            writer.writeheader()


def _load_leads() -> list[dict]:
    """Load all rows from INBOUND_LEADS.csv."""
    _ensure_csv()
    rows = []
    with open(safe_path(LEADS_CSV), "r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(dict(row))
    return rows


def _dedup_key(platform: str, username: str) -> str:
    """Canonical dedup key: platform:lowercase_username."""
    return f"{platform.lower()}:{username.lower().lstrip('@').lstrip('u/')}"


def _build_dedup_index(leads: list[dict]) -> dict[str, int]:
    """Return {dedup_key: row_index} for fast lookups."""
    index: dict[str, int] = {}
    for i, row in enumerate(leads):
        key = _dedup_key(row.get("platform", ""), row.get("username", ""))
        index[key] = i  # later row wins if duplicates exist in file
    return index


def _append_row(row: dict) -> None:
    """Append a single row to INBOUND_LEADS.csv."""
    _ensure_csv()
    with open(safe_path(LEADS_CSV), "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_HEADERS)
        writer.writerow(row)


def _rewrite_leads(leads: list[dict]) -> None:
    """Full rewrite of INBOUND_LEADS.csv (used for upgrades/updates)."""
    _ensure_csv()
    with open(safe_path(LEADS_CSV), "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(leads)


# ---------------------------------------------------------------------------
# Lead construction
# ---------------------------------------------------------------------------

def _make_row(
    username: str,
    platform: str,
    engagement_type: str,
    score: str,
    source_post: str = "",
    lead_type: str = "INBOUND",
    status: str = "NEW",
    direction: str = "INBOUND",
    timestamp: str | None = None,
) -> dict:
    return {
        "timestamp": timestamp or _now_iso(),
        "username": username.strip(),
        "platform": platform.lower().strip(),
        "engagement_type": engagement_type.upper().strip(),
        "source_post": source_post.strip(),
        "score": score.upper().strip(),
        "lead_type": lead_type.upper().strip(),
        "status": status.upper().strip(),
        "direction": direction.upper().strip(),
    }


# ---------------------------------------------------------------------------
# --add command
# ---------------------------------------------------------------------------

def cmd_add(args: argparse.Namespace, dry_run: bool = False) -> None:
    """Manually add or update a single lead."""
    username = (args.username or "").strip()
    platform = (args.platform or "").strip().lower()
    engagement_type = (args.type or "MANUAL").strip()
    score = (args.score or "COLD").strip().upper()
    source_post = (getattr(args, "source_post", None) or "").strip()

    if not username:
        log("--username is required for --add", "ERROR")
        sys.exit(1)
    if not platform:
        log("--platform is required for --add", "ERROR")
        sys.exit(1)
    if score not in SCORE_ORDER:
        log(f"Invalid score '{score}'. Choose from: {SCORE_ORDER}", "ERROR")
        sys.exit(1)

    leads = _load_leads()
    index = _build_dedup_index(leads)
    key = _dedup_key(platform, username)

    if key in index:
        # Lead exists — upgrade score if new score is warmer
        existing = leads[index[key]]
        old_score = existing.get("score", "COLD").upper()
        new_score = score
        if SCORE_ORDER.index(new_score) > SCORE_ORDER.index(old_score):
            action = f"UPGRADE {username}@{platform}: {old_score} -> {new_score}"
        else:
            action = f"SKIP {username}@{platform}: already at {old_score} (requested {new_score} is not warmer)"
        log(action)
        if not dry_run and SCORE_ORDER.index(new_score) > SCORE_ORDER.index(old_score):
            leads[index[key]]["score"] = new_score
            leads[index[key]]["status"] = "UPDATED"
            if source_post:
                leads[index[key]]["source_post"] = source_post
            _rewrite_leads(leads)
            log(f"Updated lead: {username} on {platform}")
    else:
        row = _make_row(
            username=username,
            platform=platform,
            engagement_type=engagement_type,
            score=score,
            source_post=source_post,
        )
        log(f"ADD {row['score']} lead: {username} on {platform} [{engagement_type}]")
        if not dry_run:
            _append_row(row)
            log(f"Saved to {LEADS_CSV}")


# ---------------------------------------------------------------------------
# --upgrade command
# ---------------------------------------------------------------------------

def cmd_upgrade(args: argparse.Namespace, dry_run: bool = False) -> None:
    """Force-upgrade an existing lead's score."""
    username = (args.username or "").strip()
    platform = (args.platform or "").strip().lower()
    score = (args.score or "").strip().upper()

    if not username or not platform or not score:
        log("--upgrade requires --username, --platform, and --score", "ERROR")
        sys.exit(1)
    if score not in SCORE_ORDER:
        log(f"Invalid score '{score}'. Choose from: {SCORE_ORDER}", "ERROR")
        sys.exit(1)

    leads = _load_leads()
    index = _build_dedup_index(leads)
    key = _dedup_key(platform, username)

    if key not in index:
        log(f"Lead not found: {username} on {platform}. Use --add to create it.", "WARN")
        sys.exit(1)

    old_score = leads[index[key]].get("score", "COLD").upper()
    log(f"UPGRADE {username}@{platform}: {old_score} -> {score}")
    if not dry_run:
        leads[index[key]]["score"] = score
        leads[index[key]]["status"] = "UPDATED"
        _rewrite_leads(leads)
        log("Saved.")


# ---------------------------------------------------------------------------
# --scan helpers
# ---------------------------------------------------------------------------

def _score_from_engagement(engagement_ratio: float, likes: int, replies: int) -> str:
    """Derive a lead score from Twitter engagement numbers."""
    if likes >= 10 or replies >= 3 or engagement_ratio >= 0.05:
        return "WARM"
    return "COLD"


def _scan_reddit(dry_run: bool) -> int:
    """
    Scan reddit_scraper_output/ JSON files for leads.

    Each file is a list of alpha entries. We extract the OP (poster implied by
    source_url subreddit) as a COLD inbound signal. High-engagement posts
    (score >= 100) get bumped to WARM because they represent validated demand
    audiences that may respond to PRINTMAXX outreach.

    Returns count of new leads added.
    """
    if not REDDIT_SCRAPER_DIR.exists():
        log("reddit_scraper_output/ not found, skipping Reddit scan", "WARN")
        return 0

    leads = _load_leads()
    index = _build_dedup_index(leads)
    added = 0

    json_files = sorted(REDDIT_SCRAPER_DIR.glob("reddit_*.json"))
    if not json_files:
        log("No reddit_*.json files found", "WARN")
        return 0

    # Only scan the most-recent file to avoid re-adding same posts on each run
    latest = json_files[-1]
    log(f"Scanning Reddit file: {latest.name}")

    try:
        entries: list[dict] = json.loads(latest.read_text(encoding="utf-8"))
    except Exception as exc:
        log(f"Failed to parse {latest.name}: {exc}", "ERROR")
        return 0

    for entry in entries:
        source_url = entry.get("source_url", "")
        source = entry.get("source", "")  # e.g. "r/SideProject"
        notes = entry.get("notes", "")
        category = entry.get("category", "UNKNOWN")

        # Extract post score from notes like "Score: 629, Comments: 55"
        post_score = 0
        m = re.search(r"Score:\s*(\d+)", notes)
        if m:
            post_score = int(m.group(1))

        # Build a synthetic username from subreddit + post id
        # Real usernames aren't present in this data format (alpha scraper)
        # We use the subreddit as a "channel" and the post URL tail as id
        url_tail = source_url.rstrip("/").split("/")[-1] if source_url else ""
        if not url_tail:
            continue
        # Use subreddit name as platform qualifier and post id as username
        subreddit_name = source.lstrip("r/") if source else "reddit"
        synthetic_username = f"{subreddit_name}/{url_tail[:24]}"

        lead_score = "WARM" if post_score >= 100 else "COLD"
        engagement_type = f"REDDIT_{category}"

        key = _dedup_key("reddit", synthetic_username)
        if key in index:
            continue  # already tracked

        row = _make_row(
            username=synthetic_username,
            platform="reddit",
            engagement_type=engagement_type,
            score=lead_score,
            source_post=source_url,
            lead_type="INBOUND_SIGNAL",
            status="NEW",
            direction="INBOUND",
        )
        log(f"Reddit lead [{lead_score}]: {synthetic_username} | {category}")
        if not dry_run:
            _append_row(row)
            # Update index so within-batch dedup works
            leads.append(row)
            index[key] = len(leads) - 1
        added += 1

    return added


def _scan_twitter(dry_run: bool) -> int:
    """
    Scan twitter_scraper_output/ JSON files for leads.

    Each file is a list of tweet objects. Each unique handle with meaningful
    engagement becomes a lead. Engagement ratio >= 0.05 or likes >= 20 -> WARM.

    Returns count of new leads added.
    """
    if not TWITTER_SCRAPER_DIR.exists():
        log("twitter_scraper_output/ not found, skipping Twitter scan", "WARN")
        return 0

    leads = _load_leads()
    index = _build_dedup_index(leads)
    added = 0

    json_files = sorted(TWITTER_SCRAPER_DIR.glob("scrape_*.json"))
    if not json_files:
        json_files = sorted(TWITTER_SCRAPER_DIR.glob("*.json"))
    if not json_files:
        log("No Twitter scrape JSON files found", "WARN")
        return 0

    # Process the two most-recent files to catch recent signal without full re-scan
    recent_files = json_files[-2:]
    for fpath in recent_files:
        log(f"Scanning Twitter file: {fpath.name}")
        try:
            tweets: list[dict] = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception as exc:
            log(f"Failed to parse {fpath.name}: {exc}", "ERROR")
            continue

        for tweet in tweets:
            handle = tweet.get("handle", "").strip()
            if not handle:
                continue

            likes = int(tweet.get("likes", 0) or 0)
            replies = int(tweet.get("replies", 0) or 0)
            retweets = int(tweet.get("retweets", 0) or 0)
            try:
                eng_ratio = float(tweet.get("engagement_ratio", 0) or 0)
            except (ValueError, TypeError):
                eng_ratio = 0.0
            tweet_url = tweet.get("url", "")

            lead_score = _score_from_engagement(eng_ratio, likes, replies)

            key = _dedup_key("twitter", handle)
            if key in index:
                # Possibly upgrade score if this tweet has stronger engagement
                existing_score = leads[index[key]].get("score", "COLD").upper()
                if (
                    SCORE_ORDER.index(lead_score) > SCORE_ORDER.index(existing_score)
                    and not dry_run
                ):
                    leads[index[key]]["score"] = lead_score
                    leads[index[key]]["status"] = "UPDATED"
                    log(f"Twitter upgrade: @{handle} {existing_score} -> {lead_score}")
                continue

            row = _make_row(
                username=f"@{handle}",
                platform="twitter",
                engagement_type="TWEET_SIGNAL",
                score=lead_score,
                source_post=tweet_url,
                lead_type="INBOUND_SIGNAL",
                status="NEW",
                direction="INBOUND",
            )
            log(f"Twitter lead [{lead_score}]: @{handle} | likes={likes} replies={replies}")
            if not dry_run:
                _append_row(row)
                leads.append(row)
                index[key] = len(leads) - 1
            added += 1

    # Flush any score upgrades
    if not dry_run:
        _rewrite_leads(leads)

    return added


def _scan_freelance(dry_run: bool) -> int:
    """
    Scan CONTENT/freelance_responses/ markdown files for outbound opportunities.

    Each file corresponds to one freelance post we responded to. The post title
    encodes platform (usually reddit r/...) and the budget. We track these as
    OUTBOUND leads — we reached out, now waiting for response.

    Returns count of new leads added.
    """
    if not FREELANCE_RESPONSES_DIR.exists():
        log("freelance_responses/ not found, skipping", "WARN")
        return 0

    leads = _load_leads()
    index = _build_dedup_index(leads)
    added = 0

    md_files = sorted(FREELANCE_RESPONSES_DIR.glob("response_*.md"))
    if not md_files:
        log("No response_*.md files found in freelance_responses/", "WARN")
        return 0

    log(f"Scanning {len(md_files)} freelance response files")

    for fpath in md_files:
        content = fpath.read_text(encoding="utf-8")

        # Extract fields from the markdown header block
        url_match = re.search(r"## URL:\s*(.+)", content)
        subreddit_match = re.search(r"## Subreddit:\s*(.+)", content)
        budget_match = re.search(r"## Budget:\s*(\d+(?:\.\d+)?)", content)
        post_title_match = re.search(r"## Post:\s*(.+)", content)

        source_url = url_match.group(1).strip() if url_match else ""
        subreddit = subreddit_match.group(1).strip() if subreddit_match else "unknown"
        budget = float(budget_match.group(1)) if budget_match else 0
        post_title = post_title_match.group(1).strip() if post_title_match else fpath.stem

        # Derive platform from URL or subreddit
        if "reddit.com" in source_url or subreddit.startswith("r/"):
            platform = "reddit"
        elif "linkedin.com" in source_url:
            platform = "linkedin"
        else:
            platform = "freelance"

        # Use file stem as unique identifier (contains post title + date)
        # Truncate to keep it readable
        file_id = fpath.stem[:60]

        # HOT if budget >= 100, WARM if budget > 0, COLD otherwise
        if budget >= 100:
            lead_score = "HOT"
        elif budget > 0:
            lead_score = "WARM"
        else:
            lead_score = "COLD"

        key = _dedup_key(platform, file_id)
        if key in index:
            continue

        row = _make_row(
            username=file_id,
            platform=platform,
            engagement_type="FREELANCE_RESPONSE",
            score=lead_score,
            source_post=source_url,
            lead_type="OUTBOUND",
            status="RESPONDED",
            direction="OUTBOUND",
        )
        log(f"Freelance lead [{lead_score}]: {subreddit} budget=${budget:.0f}")
        if not dry_run:
            _append_row(row)
            leads.append(row)
            index[key] = len(leads) - 1
        added += 1

    return added


def cmd_scan(dry_run: bool = False) -> None:
    """Run all scanners and report totals."""
    log("Starting inbound lead scan" + (" (DRY RUN)" if dry_run else ""))

    reddit_count = _scan_reddit(dry_run)
    twitter_count = _scan_twitter(dry_run)
    freelance_count = _scan_freelance(dry_run)

    total = reddit_count + twitter_count + freelance_count
    log(
        f"Scan complete. New leads: reddit={reddit_count} "
        f"twitter={twitter_count} freelance={freelance_count} total={total}"
        + (" (DRY RUN - nothing written)" if dry_run else "")
    )


# ---------------------------------------------------------------------------
# --stats command
# ---------------------------------------------------------------------------

def cmd_stats() -> None:
    """Print lead funnel statistics."""
    leads = _load_leads()

    if not leads:
        print("No leads tracked yet. Run --scan to populate.")
        return

    total = len(leads)

    # By platform
    platform_counts: Counter = Counter(r.get("platform", "unknown") for r in leads)

    # By score
    score_counts: Counter = Counter(r.get("score", "COLD").upper() for r in leads)

    # By direction
    direction_counts: Counter = Counter(r.get("direction", "INBOUND") for r in leads)

    # By status
    status_counts: Counter = Counter(r.get("status", "NEW").upper() for r in leads)

    # Conversion funnel percentages
    def pct(count: int) -> str:
        return f"{count / total * 100:.1f}%" if total else "0%"

    print("\n" + "=" * 54)
    print("  PRINTMAXX INBOUND LEAD TRACKER — STATS")
    print("=" * 54)
    print(f"\n  Total leads tracked: {total}")

    print("\n  BY PLATFORM")
    print("  " + "-" * 30)
    for platform, count in platform_counts.most_common():
        print(f"  {platform:<20} {count:>4}  ({pct(count)})")

    print("\n  LEAD SCORE DISTRIBUTION (funnel)")
    print("  " + "-" * 30)
    for score in SCORE_ORDER:
        count = score_counts.get(score, 0)
        bar = "#" * min(count, 40)
        print(f"  {score:<12} {count:>4}  {bar}")

    print("\n  DIRECTION")
    print("  " + "-" * 30)
    for direction, count in direction_counts.most_common():
        print(f"  {direction:<20} {count:>4}  ({pct(count)})")

    print("\n  STATUS")
    print("  " + "-" * 30)
    for status, count in status_counts.most_common():
        print(f"  {status:<20} {count:>4}  ({pct(count)})")

    # Conversion rate (CONVERTED / total inbound)
    inbound_total = sum(
        1 for r in leads if r.get("direction", "INBOUND").upper() == "INBOUND"
    )
    converted = score_counts.get("CONVERTED", 0)
    hot = score_counts.get("HOT", 0)
    warm = score_counts.get("WARM", 0)

    print("\n  CONVERSION FUNNEL")
    print("  " + "-" * 30)
    if inbound_total:
        print(f"  Inbound leads:    {inbound_total}")
        print(f"  Warm or hotter:   {warm + hot + converted}  ({(warm + hot + converted) / inbound_total * 100:.1f}%)")
        print(f"  Hot or better:    {hot + converted}  ({(hot + converted) / inbound_total * 100:.1f}%)")
        print(f"  Converted:        {converted}  ({converted / inbound_total * 100:.1f}%)")

    print("\n" + "=" * 54 + "\n")


# ---------------------------------------------------------------------------
# --status command
# ---------------------------------------------------------------------------

def cmd_status() -> None:
    """Quick health status of the lead tracker."""
    leads = _load_leads()
    total = len(leads)
    hot = sum(1 for r in leads if r.get("score", "").upper() in ("HOT", "CONVERTED"))
    log_exists = LOG_FILE.exists()

    print(f"\n[LEAD TRACKER STATUS]")
    print(f"  CSV path:       {LEADS_CSV}")
    print(f"  Total leads:    {total}")
    print(f"  Hot/Converted:  {hot}")
    print(f"  Log file:       {LOG_FILE} ({'exists' if log_exists else 'not created yet'})")

    # Show scan source dirs
    for label, path in [
        ("Reddit scraper", REDDIT_SCRAPER_DIR),
        ("Twitter scraper", TWITTER_SCRAPER_DIR),
        ("Freelance responses", FREELANCE_RESPONSES_DIR),
    ]:
        file_count = len(list(path.glob("*"))) if path.exists() else 0
        print(f"  {label:<22} {path.name}/ ({file_count} files)")

    print()


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inbound_lead_tracker.py",
        description="PRINTMAXX inbound lead tracking — scan, add, score, and report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick health check
  python3 AUTOMATIONS/inbound_lead_tracker.py --status

  # Full stats report
  python3 AUTOMATIONS/inbound_lead_tracker.py --stats

  # Scan all sources (preview only)
  python3 AUTOMATIONS/inbound_lead_tracker.py --scan --dry-run

  # Scan all sources (write to CSV)
  python3 AUTOMATIONS/inbound_lead_tracker.py --scan

  # Manually add a Twitter lead
  python3 AUTOMATIONS/inbound_lead_tracker.py --add --platform twitter --username @someone --type reply --score warm

  # Add a Reddit lead with source URL
  python3 AUTOMATIONS/inbound_lead_tracker.py --add --platform reddit --username u/someuser --type comment --score cold --source-post "https://reddit.com/r/..."

  # Add a FormSubmit email lead (HOT — they opted in)
  python3 AUTOMATIONS/inbound_lead_tracker.py --add --platform email --username "user@example.com" --type form_submission --score hot

  # Upgrade an existing lead's score
  python3 AUTOMATIONS/inbound_lead_tracker.py --upgrade --platform twitter --username @someone --score hot
        """,
    )

    # Mode flags (mutually exclusive top-level actions)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--scan", action="store_true", help="Scan all source dirs for new leads")
    mode.add_argument("--stats", action="store_true", help="Print funnel statistics")
    mode.add_argument("--status", action="store_true", help="Print system health status")
    mode.add_argument("--add", action="store_true", help="Manually add a lead")
    mode.add_argument("--upgrade", action="store_true", help="Upgrade score of existing lead")

    # --add / --upgrade fields
    parser.add_argument("--platform", type=str, help="Platform: twitter, reddit, email, freelance, ...")
    parser.add_argument("--username", type=str, help="Username/handle/email of the lead")
    parser.add_argument("--type", dest="type", type=str, default="MANUAL", help="Engagement type: reply, dm, comment, form_submission, ...")
    parser.add_argument("--score", type=str, choices=[s.lower() for s in SCORE_ORDER] + SCORE_ORDER, help="Lead score: cold, warm, hot, converted")
    parser.add_argument("--source-post", type=str, default="", help="URL of the originating post/thread")

    # Modifiers
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without writing to CSV")

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    dry_run: bool = args.dry_run

    if args.status:
        cmd_status()
    elif args.stats:
        cmd_stats()
    elif args.scan:
        cmd_scan(dry_run=dry_run)
    elif args.add:
        cmd_add(args, dry_run=dry_run)
    elif args.upgrade:
        cmd_upgrade(args, dry_run=dry_run)
    else:
        parser.print_help()
        sys.exit(1)
