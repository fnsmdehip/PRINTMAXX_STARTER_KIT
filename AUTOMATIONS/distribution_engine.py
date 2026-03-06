#!/usr/bin/env python3
"""
PRINTMAXX Distribution Engine
================================
Automated multi-platform distribution. Reads content from CONTENT/social/,
generates platform-specific formatting, schedules optimal posting times,
and tracks distribution state in LEDGER/DISTRIBUTION_TRACKER.csv.

Platforms:
    - Twitter/X: 280 char limit, max 2 hashtags, no link penalty awareness
    - LinkedIn: professional tone, longer format, no hashtags in body
    - Reddit: subreddit-specific rules, value-first, no self-promo
    - Buffer CSV: ready for bulk upload
    - Substack Notes: newsletter-ready

Usage:
    python3 AUTOMATIONS/distribution_engine.py --prepare          # format content for all platforms
    python3 AUTOMATIONS/distribution_engine.py --schedule         # generate optimal posting schedule
    python3 AUTOMATIONS/distribution_engine.py --buffer-csv       # export Buffer-compatible CSV
    python3 AUTOMATIONS/distribution_engine.py --status           # show distribution status
    python3 AUTOMATIONS/distribution_engine.py --post-count       # count posts per platform
    python3 AUTOMATIONS/distribution_engine.py --mark-posted ID   # mark a content item as posted

Cron:
    0 6 * * * cd $BASE && python3 AUTOMATIONS/distribution_engine.py --prepare --schedule >> AUTOMATIONS/logs/distribution.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = PROJECT_ROOT / "CONTENT" / "social"
AUTO_GEN_DIR = CONTENT_DIR / "auto_generated"
DIST_DIR = PROJECT_ROOT / "CONTENT" / "social" / "distribution"
TRACKER_CSV = PROJECT_ROOT / "LEDGER" / "DISTRIBUTION_TRACKER.csv"
BUFFER_CSV = PROJECT_ROOT / "CONTENT" / "social" / "distribution" / "buffer_upload.csv"
SCHEDULE_FILE = PROJECT_ROOT / "CONTENT" / "social" / "distribution" / "schedule.json"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] distribution_engine: {msg}"
    print(line, file=sys.stderr)
    safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_DIR / "distribution.log"), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Platform rate limits (from algo_ban_prevention.py)
# ---------------------------------------------------------------------------
PLATFORM_LIMITS = {
    "twitter": {
        "posts_per_day_safe": 25,
        "posts_per_day_aggressive": 50,
        "hashtags_max": 2,
        "char_limit": 280,
        "link_penalty_pct": 25,
        "min_spacing_minutes": 30,
        "optimal_times_utc": [
            "08:00", "12:00", "15:00", "17:00", "19:00", "21:00",
        ],
    },
    "linkedin": {
        "posts_per_day_safe": 2,
        "posts_per_day_aggressive": 3,
        "char_limit": 3000,
        "min_spacing_minutes": 240,
        "optimal_times_utc": [
            "07:30", "08:30", "12:00", "17:00",
        ],
        "notes": "No hashtags in body. Dwell time matters. First line is hook.",
    },
    "reddit": {
        "posts_per_day_safe": 3,
        "posts_per_day_aggressive": 5,
        "self_promo_ratio_max_pct": 10,
        "min_spacing_minutes": 120,
        "char_limit": 40000,
        "optimal_times_utc": [
            "09:00", "13:00", "17:00",
        ],
        "notes": "Value-first. No direct links to own products in first posts.",
    },
    "substack": {
        "posts_per_day_safe": 2,
        "posts_per_day_aggressive": 3,
        "char_limit": 5000,
        "min_spacing_minutes": 360,
        "optimal_times_utc": [
            "08:00", "10:00", "14:00",
        ],
    },
}

# Number of posts per account per platform per day (safe mode)
ACCOUNT_DAILY_BUDGET = {
    "PRINTMAXXER": {"twitter": 8, "linkedin": 1, "reddit": 1, "substack": 1},
    "repscheme":   {"twitter": 5, "linkedin": 0, "reddit": 1, "substack": 0},
    "drifthour":   {"twitter": 5, "linkedin": 0, "reddit": 0, "substack": 0},
    "voidpilled":  {"twitter": 5, "linkedin": 0, "reddit": 1, "substack": 0},
    "selahmoments": {"twitter": 5, "linkedin": 0, "reddit": 0, "substack": 0},
}

# ---------------------------------------------------------------------------
# Tracker CSV management
# ---------------------------------------------------------------------------
TRACKER_FIELDS = [
    "dist_id", "content_file", "content_text", "platform", "account",
    "formatted_text", "char_count", "hashtags", "scheduled_time",
    "status", "posted_at", "created_at", "notes",
]


def load_tracker() -> list[dict]:
    """Load existing distribution tracker entries."""
    if not TRACKER_CSV.exists():
        return []
    with open(TRACKER_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_tracker(entries: list[dict]) -> None:
    """Save distribution tracker entries."""
    safe_path(TRACKER_CSV.parent).mkdir(parents=True, exist_ok=True)
    with open(safe_path(TRACKER_CSV), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
        writer.writeheader()
        writer.writerows(entries)


def next_dist_id(entries: list[dict]) -> str:
    """Generate next distribution ID."""
    existing = [e.get("dist_id", "") for e in entries]
    nums = []
    for eid in existing:
        m = re.search(r'DIST(\d+)', eid)
        if m:
            nums.append(int(m.group(1)))
    next_num = max(nums) + 1 if nums else 1
    return f"DIST{next_num:04d}"


# ---------------------------------------------------------------------------
# Content ingestion
# ---------------------------------------------------------------------------
def scan_content_files() -> list[dict]:
    """Scan auto_generated directory for unprocessed content."""
    content_items = []

    if not AUTO_GEN_DIR.exists():
        log("auto_generated directory not found")
        return content_items

    # Track already-distributed files
    existing = load_tracker()
    distributed_files = {e.get("content_file", "") for e in existing}

    # Scan CSV files (tweets)
    for csv_file in sorted(AUTO_GEN_DIR.glob("*.csv")):
        fname = csv_file.name
        if fname in distributed_files:
            continue
        try:
            with open(csv_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    text = row.get("tweet_text", row.get("draft", ""))
                    if not text or len(text) < 15:
                        continue
                    content_items.append({
                        "file": fname,
                        "text": text,
                        "format": row.get("format", "single_tweet"),
                        "account": row.get("account", "@PRINTMAXXER"),
                        "source": "csv",
                    })
        except Exception as e:
            log(f"Error reading {fname}: {e}")

    # Scan JSON files (threads)
    for json_file in sorted(AUTO_GEN_DIR.glob("*.json")):
        fname = json_file.name
        if fname in distributed_files or "manifest" in fname:
            continue
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("type") == "thread":
                tweets = data.get("tweets", [])
                for i, t in enumerate(tweets):
                    content_items.append({
                        "file": fname,
                        "text": t,
                        "format": f"thread_{i+1}of{len(tweets)}",
                        "account": data.get("account", "@PRINTMAXXER"),
                        "source": "thread_json",
                    })
        except Exception as e:
            log(f"Error reading {fname}: {e}")

    # Scan TXT files (LinkedIn, Reddit, Newsletter)
    for txt_file in sorted(AUTO_GEN_DIR.glob("*.txt")):
        fname = txt_file.name
        if fname in distributed_files:
            continue
        try:
            text = txt_file.read_text(encoding="utf-8", errors="replace")
            # Strip metadata comments
            lines = [l for l in text.split("\n") if not l.startswith("#")]
            clean_text = "\n".join(lines).strip()
            if len(clean_text) < 20:
                continue

            # Determine platform from filename
            if "linkedin" in fname:
                platform_hint = "linkedin"
            elif "reddit" in fname:
                platform_hint = "reddit"
            elif "newsletter" in fname:
                platform_hint = "substack"
            elif "gumroad" in fname:
                platform_hint = "gumroad"
            else:
                platform_hint = "general"

            content_items.append({
                "file": fname,
                "text": clean_text,
                "format": platform_hint,
                "account": "@PRINTMAXXER",
                "source": "txt",
            })
        except Exception as e:
            log(f"Error reading {fname}: {e}")

    log(f"Scanned {len(content_items)} content items from auto_generated/")
    return content_items


# ---------------------------------------------------------------------------
# Platform formatting
# ---------------------------------------------------------------------------
def format_for_twitter(text: str, max_hashtags: int = 2) -> dict:
    """Format content for Twitter/X."""
    formatted = text.strip()

    # Remove excessive hashtags (keep max 2)
    hashtags = re.findall(r'#\w+', formatted)
    if len(hashtags) > max_hashtags:
        for ht in hashtags[max_hashtags:]:
            formatted = formatted.replace(ht, "").strip()

    # Enforce 280 char limit
    if len(formatted) > 280:
        # Try to cut at sentence boundary
        cut = formatted[:277].rfind(".")
        if cut > 100:
            formatted = formatted[:cut + 1]
        else:
            formatted = formatted[:277] + "..."

    # Clean up whitespace
    formatted = re.sub(r'\s+', ' ', formatted).strip()

    return {
        "platform": "twitter",
        "formatted": formatted,
        "char_count": len(formatted),
        "hashtag_count": len(re.findall(r'#\w+', formatted)),
        "has_link": bool(re.search(r'https?://', formatted)),
        "within_limit": len(formatted) <= 280,
    }


def format_for_linkedin(text: str) -> dict:
    """Format content for LinkedIn."""
    formatted = text.strip()

    # LinkedIn prefers line breaks for readability
    # Ensure paragraphs are separated
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)

    # Remove hashtags from body (LinkedIn penalizes them in content)
    formatted = re.sub(r'#\w+', '', formatted).strip()

    # Ensure first line is a hook (short, punchy)
    lines = formatted.split('\n')
    if lines and len(lines[0]) > 150:
        # Split first line into hook + rest
        first_sentence_end = lines[0][:150].rfind(".")
        if first_sentence_end > 30:
            hook = lines[0][:first_sentence_end + 1]
            rest = lines[0][first_sentence_end + 1:].strip()
            lines = [hook, "", rest] + lines[1:]
            formatted = "\n".join(lines)

    # Enforce limit
    if len(formatted) > 3000:
        formatted = formatted[:2997] + "..."

    return {
        "platform": "linkedin",
        "formatted": formatted,
        "char_count": len(formatted),
        "within_limit": len(formatted) <= 3000,
        "has_hook": len(formatted.split('\n')[0]) <= 150 if formatted else False,
    }


def format_for_reddit(text: str, subreddit: str = "r/Entrepreneur") -> dict:
    """Format content for Reddit."""
    formatted = text.strip()

    # Reddit: remove all self-promotional language
    promo_patterns = [
        r'follow (?:me|for more)',
        r'check (?:out )?my (?:link|profile|bio)',
        r'link in (?:bio|comments)',
        r'subscribe to',
        r'use my (?:code|link)',
    ]
    for pattern in promo_patterns:
        formatted = re.sub(pattern, '', formatted, flags=re.IGNORECASE)

    # Clean up artifacts
    formatted = re.sub(r'\s+', ' ', formatted).strip()

    # Add "value-first" structure if missing
    if not formatted.startswith("##") and not formatted.startswith("**"):
        lines = formatted.split(". ")
        if len(lines) >= 3:
            formatted = f"{lines[0]}.\n\n" + ". ".join(lines[1:])

    return {
        "platform": "reddit",
        "formatted": formatted,
        "char_count": len(formatted),
        "subreddit": subreddit,
        "within_limit": len(formatted) <= 40000,
        "self_promo_removed": True,
    }


def format_for_substack(text: str) -> dict:
    """Format content for Substack Notes."""
    formatted = text.strip()

    # Substack Notes: clean, readable, medium-length
    if len(formatted) > 5000:
        formatted = formatted[:4997] + "..."

    # Add paragraph breaks if wall of text
    if "\n" not in formatted and len(formatted) > 300:
        sentences = re.split(r'(?<=[.!?])\s+', formatted)
        chunks = []
        current = ""
        for s in sentences:
            if len(current) + len(s) > 200:
                chunks.append(current.strip())
                current = s
            else:
                current += " " + s
        if current:
            chunks.append(current.strip())
        formatted = "\n\n".join(chunks)

    return {
        "platform": "substack",
        "formatted": formatted,
        "char_count": len(formatted),
        "within_limit": len(formatted) <= 5000,
    }


def format_content(item: dict) -> list[dict]:
    """Format a content item for all applicable platforms."""
    text = item["text"]
    account = item.get("account", "@PRINTMAXXER")
    content_format = item.get("format", "single_tweet")
    results = []

    # Twitter (all tweet-like content)
    if content_format in ("single_tweet", "niche_variant") or "thread" in content_format:
        tw = format_for_twitter(text)
        tw["account"] = account
        tw["source_format"] = content_format
        results.append(tw)

    # LinkedIn (only PRINTMAXXER, only longer content)
    if content_format == "linkedin" or (
        account == "@PRINTMAXXER" and len(text) > 200 and "thread" not in content_format
    ):
        li = format_for_linkedin(text)
        li["account"] = account
        li["source_format"] = content_format
        results.append(li)

    # Reddit (value-first content only)
    if content_format == "reddit" or (
        content_format in ("linkedin", "general") and len(text) > 200
    ):
        rd = format_for_reddit(text)
        rd["account"] = account
        rd["source_format"] = content_format
        results.append(rd)

    # Substack (newsletter content)
    if content_format in ("substack", "newsletter", "general") and len(text) > 100:
        ss = format_for_substack(text)
        ss["account"] = account
        ss["source_format"] = content_format
        results.append(ss)

    return results


# ---------------------------------------------------------------------------
# Scheduling
# ---------------------------------------------------------------------------
def generate_schedule(entries: list[dict]) -> list[dict]:
    """Generate optimal posting schedule for pending distribution items."""
    # Group by platform and account
    by_platform_account: Dict[str, list] = {}
    for entry in entries:
        if entry.get("status") not in ("PENDING", "READY"):
            continue
        key = f"{entry.get('platform', 'twitter')}_{entry.get('account', 'unknown')}"
        if key not in by_platform_account:
            by_platform_account[key] = []
        by_platform_account[key].append(entry)

    scheduled = []
    base_date = datetime.now()

    for key, items in by_platform_account.items():
        platform = items[0].get("platform", "twitter")
        account = items[0].get("account", "unknown")
        limits = PLATFORM_LIMITS.get(platform, PLATFORM_LIMITS["twitter"])
        optimal_times = limits.get("optimal_times_utc", ["09:00", "12:00", "17:00"])
        daily_limit = limits.get("posts_per_day_safe", 5)
        min_spacing = limits.get("min_spacing_minutes", 30)

        # Get account-specific budget
        acct_clean = account.lstrip("@")
        acct_budget = ACCOUNT_DAILY_BUDGET.get(acct_clean, {})
        platform_budget = acct_budget.get(platform, daily_limit)
        effective_limit = min(daily_limit, platform_budget)

        day_offset = 0
        time_idx = 0
        count_today = 0

        for item in items:
            if count_today >= effective_limit:
                day_offset += 1
                count_today = 0
                time_idx = 0

            if time_idx >= len(optimal_times):
                # Add extra slots with spacing
                hour = int(optimal_times[-1].split(":")[0]) + 1
                if hour > 23:
                    day_offset += 1
                    count_today = 0
                    time_idx = 0
                    hour = int(optimal_times[0].split(":")[0])
                slot_time = f"{hour:02d}:{random.randint(0, 59):02d}"
            else:
                slot_time = optimal_times[time_idx]
                # Add jitter (0-15 minutes) to avoid bot patterns
                jitter = random.randint(0, 15)
                h, m = slot_time.split(":")
                m = int(m) + jitter
                if m >= 60:
                    h = str(int(h) + 1)
                    m -= 60
                slot_time = f"{int(h):02d}:{m:02d}"

            sched_date = base_date + timedelta(days=day_offset)
            sched_str = sched_date.strftime("%Y-%m-%d") + f" {slot_time}"

            item["scheduled_time"] = sched_str
            item["status"] = "SCHEDULED"
            scheduled.append(item)

            count_today += 1
            time_idx += 1

    log(f"Scheduled {len(scheduled)} items across {len(by_platform_account)} platform/account combos")
    return scheduled


# ---------------------------------------------------------------------------
# Buffer CSV export
# ---------------------------------------------------------------------------
BUFFER_FIELDS = ["Text", "Date", "Time", "Profile"]

ACCOUNT_TO_BUFFER_PROFILE = {
    "@PRINTMAXXER": "PRINTMAXXER Twitter",
    "@repscheme": "repscheme Twitter",
    "@drifthour": "drifthour Twitter",
    "@voidpilled": "voidpilled Twitter",
    "@selahmoments": "selahmoments Twitter",
}


def export_buffer_csv(entries: list[dict]) -> str:
    """Export scheduled Twitter content as Buffer-compatible CSV."""
    safe_path(DIST_DIR).mkdir(parents=True, exist_ok=True)

    twitter_items = [
        e for e in entries
        if e.get("platform") == "twitter"
        and e.get("status") in ("SCHEDULED", "READY", "PENDING")
    ]

    if not twitter_items:
        log("No Twitter content to export for Buffer")
        return ""

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = safe_path(DIST_DIR / f"buffer_upload_{ts}.csv")

    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=BUFFER_FIELDS)
        writer.writeheader()

        for item in twitter_items:
            sched = item.get("scheduled_time", "")
            date_part = ""
            time_part = ""
            if sched:
                parts = sched.split(" ")
                date_part = parts[0] if len(parts) > 0 else ""
                time_part = parts[1] if len(parts) > 1 else ""

            profile = ACCOUNT_TO_BUFFER_PROFILE.get(
                item.get("account", ""),
                "PRINTMAXXER Twitter",
            )

            writer.writerow({
                "Text": item.get("formatted_text", item.get("content_text", "")),
                "Date": date_part,
                "Time": time_part,
                "Profile": profile,
            })

    log(f"Exported {len(twitter_items)} items to Buffer CSV: {outfile}")
    return str(outfile)


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------
def cmd_prepare() -> None:
    """Prepare content: scan, format for all platforms, add to tracker."""
    content_items = scan_content_files()
    if not content_items:
        print("No new content to prepare.")
        return

    existing = load_tracker()
    new_entries = []

    for item in content_items:
        formatted_results = format_content(item)
        for fmt in formatted_results:
            dist_id = next_dist_id(existing + new_entries)
            entry = {
                "dist_id": dist_id,
                "content_file": item["file"],
                "content_text": item["text"][:500],
                "platform": fmt["platform"],
                "account": fmt.get("account", "@PRINTMAXXER"),
                "formatted_text": fmt["formatted"][:500],
                "char_count": str(fmt.get("char_count", 0)),
                "hashtags": str(fmt.get("hashtag_count", 0)),
                "scheduled_time": "",
                "status": "PENDING",
                "posted_at": "",
                "created_at": datetime.now().isoformat(),
                "notes": f"source:{item.get('source', '')} format:{item.get('format', '')}",
            }
            new_entries.append(entry)

    all_entries = existing + new_entries
    save_tracker(all_entries)

    # Summary
    by_platform = {}
    for e in new_entries:
        p = e["platform"]
        by_platform[p] = by_platform.get(p, 0) + 1

    log(f"Prepared {len(new_entries)} distribution items")
    print(f"\n--- Prepared {len(new_entries)} items ---")
    for platform, count in sorted(by_platform.items()):
        print(f"  {platform}: {count}")
    print(f"  Total in tracker: {len(all_entries)}")


def cmd_schedule() -> None:
    """Generate posting schedule for pending items."""
    entries = load_tracker()
    pending = [e for e in entries if e.get("status") in ("PENDING", "READY")]
    if not pending:
        print("No pending items to schedule.")
        return

    scheduled = generate_schedule(pending)

    # Update tracker with scheduled times
    entry_map = {e["dist_id"]: e for e in entries}
    for s in scheduled:
        if s["dist_id"] in entry_map:
            entry_map[s["dist_id"]]["scheduled_time"] = s["scheduled_time"]
            entry_map[s["dist_id"]]["status"] = "SCHEDULED"

    save_tracker(list(entry_map.values()))

    # Save schedule summary
    safe_path(DIST_DIR).mkdir(parents=True, exist_ok=True)
    schedule_data = {
        "generated_at": datetime.now().isoformat(),
        "total_scheduled": len(scheduled),
        "by_platform": {},
        "by_account": {},
        "schedule": [],
    }
    for s in scheduled:
        p = s.get("platform", "unknown")
        a = s.get("account", "unknown")
        schedule_data["by_platform"][p] = schedule_data["by_platform"].get(p, 0) + 1
        schedule_data["by_account"][a] = schedule_data["by_account"].get(a, 0) + 1
        schedule_data["schedule"].append({
            "dist_id": s["dist_id"],
            "platform": p,
            "account": a,
            "time": s.get("scheduled_time", ""),
            "text_preview": s.get("formatted_text", s.get("content_text", ""))[:80],
        })

    with open(safe_path(SCHEDULE_FILE), "w", encoding="utf-8") as f:
        json.dump(schedule_data, f, indent=2)

    print(f"\n--- Scheduled {len(scheduled)} items ---")
    for platform, count in sorted(schedule_data["by_platform"].items()):
        print(f"  {platform}: {count}")
    for account, count in sorted(schedule_data["by_account"].items()):
        print(f"  {account}: {count}")


def cmd_buffer_csv() -> None:
    """Export Buffer-compatible CSV."""
    entries = load_tracker()
    outfile = export_buffer_csv(entries)
    if outfile:
        print(f"\nBuffer CSV exported: {outfile}")
    else:
        print("No Twitter content available for Buffer export.")


def cmd_status() -> None:
    """Show distribution status."""
    entries = load_tracker()

    print("\n--- Distribution Engine Status ---\n")

    if not entries:
        print("  No entries in tracker. Run --prepare first.")
        return

    # By status
    by_status = {}
    for e in entries:
        s = e.get("status", "UNKNOWN")
        by_status[s] = by_status.get(s, 0) + 1

    print("  By status:")
    for status, count in sorted(by_status.items()):
        print(f"    {status}: {count}")

    # By platform
    by_platform = {}
    for e in entries:
        p = e.get("platform", "unknown")
        by_platform[p] = by_platform.get(p, 0) + 1

    print("\n  By platform:")
    for platform, count in sorted(by_platform.items()):
        print(f"    {platform}: {count}")

    # By account
    by_account = {}
    for e in entries:
        a = e.get("account", "unknown")
        by_account[a] = by_account.get(a, 0) + 1

    print("\n  By account:")
    for account, count in sorted(by_account.items()):
        print(f"    {account}: {count}")

    # Pending vs posted
    pending = sum(1 for e in entries if e.get("status") in ("PENDING", "READY", "SCHEDULED"))
    posted = sum(1 for e in entries if e.get("status") == "POSTED")
    print(f"\n  Pending: {pending}")
    print(f"  Posted: {posted}")
    print(f"  Total: {len(entries)}")

    # Next scheduled
    scheduled = [e for e in entries if e.get("status") == "SCHEDULED" and e.get("scheduled_time")]
    if scheduled:
        scheduled.sort(key=lambda e: e.get("scheduled_time", ""))
        print(f"\n  Next 5 scheduled:")
        for e in scheduled[:5]:
            print(f"    {e['scheduled_time']} | {e['platform']} | {e['account']} | {e.get('formatted_text', e.get('content_text', ''))[:50]}...")


def cmd_post_count() -> None:
    """Count posts per platform per day."""
    entries = load_tracker()

    print("\n--- Post Counts ---\n")

    # Group by date + platform + account
    counts: Dict[str, Dict[str, int]] = {}
    for e in entries:
        sched = e.get("scheduled_time", e.get("posted_at", ""))
        if not sched:
            continue
        date = sched[:10]
        platform = e.get("platform", "unknown")
        account = e.get("account", "unknown").lstrip("@")
        key = f"{date} | {platform} | {account}"
        counts[key] = counts.get(key, 0) + 1

    if not counts:
        print("  No scheduled or posted content found.")
        return

    # Check against limits
    for key, count in sorted(counts.items()):
        parts = key.split(" | ")
        platform = parts[1] if len(parts) > 1 else "unknown"
        limit = PLATFORM_LIMITS.get(platform, {}).get("posts_per_day_safe", 99)
        warning = " << OVER LIMIT" if count > limit else ""
        print(f"  {key}: {count} posts{warning}")


def cmd_mark_posted(dist_id: str) -> None:
    """Mark a distribution item as posted."""
    entries = load_tracker()
    found = False
    for e in entries:
        if e.get("dist_id", "").upper() == dist_id.upper():
            e["status"] = "POSTED"
            e["posted_at"] = datetime.now().isoformat()
            found = True
            break

    if found:
        save_tracker(entries)
        print(f"Marked {dist_id} as POSTED")
    else:
        print(f"Distribution ID '{dist_id}' not found")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Distribution Engine: multi-platform content distribution",
    )
    parser.add_argument("--prepare", action="store_true",
                        help="Format content for all platforms")
    parser.add_argument("--schedule", action="store_true",
                        help="Generate optimal posting schedule")
    parser.add_argument("--buffer-csv", action="store_true",
                        help="Export Buffer-compatible CSV")
    parser.add_argument("--status", action="store_true",
                        help="Show distribution status")
    parser.add_argument("--post-count", action="store_true",
                        help="Count posts per platform per day")
    parser.add_argument("--mark-posted", type=str, default=None, metavar="ID",
                        help="Mark a distribution item as posted")
    args = parser.parse_args()

    if args.prepare:
        cmd_prepare()
    if args.schedule:
        cmd_schedule()
    if args.buffer_csv:
        cmd_buffer_csv()
    if args.status:
        cmd_status()
    if args.post_count:
        cmd_post_count()
    if args.mark_posted:
        cmd_mark_posted(args.mark_posted)

    if not any([args.prepare, args.schedule, args.buffer_csv,
                args.status, args.post_count, args.mark_posted]):
        parser.print_help()


if __name__ == "__main__":
    main()
