#!/usr/bin/env python3
"""
PRINTMAXX Auto Scheduler
=========================
Reads content files from CONTENT/social/ and generates Buffer-compatible CSV
files and Tweetlio-compatible JSON for bulk upload scheduling.

Scans .md files for PENDING_REVIEW or ready content, parses tweets/threads/posts,
and maps them onto a daily + weekly posting rhythm.

Daily posting schedule (ET):
    07:30 - Value tweet (tool/tactic)
    10:00 - Reply bait / hot take
    12:30 - Thread (1 per day)
    15:00 - QT caption placeholder
    18:00 - Community post reference
    21:00 - Engagement reply block

Weekly rhythm:
    Mon: Tools + automation
    Tue: Revenue + numbers
    Wed: Hot take / controversial
    Thu: Thread day
    Fri: Community engagement
    Sat: Behind the scenes
    Sun: Reflection + planning

Usage:
    python3 AUTOMATIONS/auto_scheduler.py --scan --account printmaxxer
    python3 AUTOMATIONS/auto_scheduler.py --generate --account all
    python3 AUTOMATIONS/auto_scheduler.py --preview --account selahmoments
    python3 AUTOMATIONS/auto_scheduler.py --generate --account printmaxxer

Output:
    CONTENT/social/printmaxxer/BUFFER_EXPORT_{date}.csv
    CONTENT/social/printmaxxer/TWEETLIO_EXPORT_{date}.json

Cron:
    0 5 * * 1 cd $BASE && python3 AUTOMATIONS/auto_scheduler.py --generate --account all >> AUTOMATIONS/logs/auto_scheduler.log 2>&1

Zero external dependencies. Uses only stdlib.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Path safety (guardrails-compliant)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = PROJECT_ROOT / "CONTENT" / "social"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"

ACCOUNT_CONTENT_DIRS: Dict[str, Path] = {
    "printmaxxer": CONTENT_DIR / "printmaxxer",
    "selahmoments": CONTENT_DIR / "selahmoments",
}


def safe_path(target: Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] auto_scheduler: {msg}"
    print(line, file=sys.stderr)
    try:
        safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
        with open(safe_path(LOG_DIR / "auto_scheduler.log"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # logging failures must never crash the scheduler


# ---------------------------------------------------------------------------
# Daily posting schedule (times in HH:MM, Eastern Time)
# ---------------------------------------------------------------------------
DAILY_SLOTS = [
    {"time": "07:30", "slot_type": "value_tweet",     "label": "Value tweet (tool/tactic)"},
    {"time": "10:00", "slot_type": "reply_bait",      "label": "Reply bait / hot take"},
    {"time": "12:30", "slot_type": "thread",           "label": "Thread (1 per day)"},
    {"time": "15:00", "slot_type": "qt_caption",       "label": "QT caption placeholder"},
    {"time": "18:00", "slot_type": "community_post",   "label": "Community post reference"},
    {"time": "21:00", "slot_type": "engagement_reply",  "label": "Engagement reply block"},
]

# Weekly content themes mapped to day-of-week (0=Mon, 6=Sun)
WEEKLY_THEMES: Dict[int, Dict[str, str]] = {
    0: {"theme": "tools_automation",    "label": "Mon: Tools + automation"},
    1: {"theme": "revenue_numbers",     "label": "Tue: Revenue + numbers"},
    2: {"theme": "hot_take",            "label": "Wed: Hot take / controversial"},
    3: {"theme": "thread_day",          "label": "Thu: Thread day"},
    4: {"theme": "community",           "label": "Fri: Community engagement"},
    5: {"theme": "behind_scenes",       "label": "Sat: Behind the scenes"},
    6: {"theme": "reflection_planning", "label": "Sun: Reflection + planning"},
}

# Map content type keywords to the slot they belong in
CONTENT_TYPE_TO_SLOT: Dict[str, str] = {
    "tweet":          "value_tweet",
    "value_tweet":    "value_tweet",
    "tool":           "value_tweet",
    "tactic":         "value_tweet",
    "hot_take":       "reply_bait",
    "reply_bait":     "reply_bait",
    "controversial":  "reply_bait",
    "thread":         "thread",
    "qt":             "qt_caption",
    "quote_tweet":    "qt_caption",
    "community":      "community_post",
    "engagement":     "engagement_reply",
    "reply":          "engagement_reply",
    "behind_scenes":  "value_tweet",
    "reflection":     "value_tweet",
    "revenue":        "value_tweet",
    "numbers":        "value_tweet",
}

# Which slot types to prefer on a given theme day (used for filling gaps)
THEME_SLOT_PREFERENCE: Dict[str, List[str]] = {
    "tools_automation":    ["value_tweet", "thread", "reply_bait"],
    "revenue_numbers":     ["value_tweet", "reply_bait", "thread"],
    "hot_take":            ["reply_bait", "value_tweet", "engagement_reply"],
    "thread_day":          ["thread", "value_tweet", "reply_bait"],
    "community":           ["community_post", "engagement_reply", "reply_bait"],
    "behind_scenes":       ["value_tweet", "community_post", "reply_bait"],
    "reflection_planning": ["value_tweet", "thread", "community_post"],
}


# ---------------------------------------------------------------------------
# Markdown content parsing
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    """Extract YAML-style frontmatter from markdown.

    Returns (metadata_dict, body_text).
    """
    metadata: Dict[str, str] = {}
    body = text

    # --- delimited frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if fm_match:
        fm_block = fm_match.group(1)
        body = fm_match.group(2)
        for line in fm_block.split("\n"):
            kv = line.split(":", 1)
            if len(kv) == 2:
                key = kv[0].strip().lower()
                val = kv[1].strip().strip('"').strip("'")
                metadata[key] = val
        return metadata, body

    # Fallback: HTML comment metadata  <!-- key: value -->
    lines = text.split("\n")
    body_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("<!--") and "-->" in stripped:
            inner = stripped.lstrip("<!-").rstrip("->").strip()
            kv = inner.split(":", 1)
            if len(kv) == 2:
                metadata[kv[0].strip().lower()] = kv[1].strip()
            body_start = i + 1
        elif stripped.startswith("#") and i == 0:
            metadata["title"] = stripped.lstrip("#").strip()
            body_start = i + 1
        elif stripped == "" and i == body_start:
            body_start = i + 1
        else:
            break
    body = "\n".join(lines[body_start:])

    return metadata, body


def _clean_tweet_text(text: str) -> str:
    """Strip markdown formatting, normalise whitespace."""
    c = text.strip()
    c = re.sub(r"\*\*(.+?)\*\*", r"\1", c)
    c = re.sub(r"\*(.+?)\*", r"\1", c)
    c = re.sub(r"__(.+?)__", r"\1", c)
    c = re.sub(r"_(.+?)_", r"\1", c)
    c = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", c)
    c = re.sub(r"```[a-z]*\n?", "", c)
    c = re.sub(r"`(.+?)`", r"\1", c)
    c = re.sub(r"[ \t]+", " ", c)
    c = re.sub(r"\n{3,}", "\n\n", c)
    return c.strip()


def _split_into_thread(text: str, max_len: int = 270) -> List[str]:
    """Break long text into thread-sized tweets."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    tweets: List[str] = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 > max_len and current:
            tweets.append(current.strip())
            current = sentence
        else:
            current = (current + " " + sentence).strip() if current else sentence
    if current:
        tweets.append(current.strip())
    return tweets if tweets else [text[:max_len]]


def _extract_numbered_or_bulleted(text: str) -> List[str]:
    """Pull items from numbered (1. / 1)) or bulleted (- / *) lists."""
    numbered = re.findall(
        r"(?:^|\n)\s*\d+[.)]\s*(.+?)(?=\n\s*\d+[.)]|\Z)", text, re.DOTALL
    )
    if numbered:
        return [n.strip() for n in numbered if n.strip()]

    bulleted = re.findall(
        r"(?:^|\n)\s*[-*]\s+(.+?)(?=\n\s*[-*]\s|\Z)", text, re.DOTALL
    )
    if bulleted:
        return [b.strip() for b in bulleted if b.strip()]

    return []


def extract_tweets_from_body(body: str) -> List[Dict[str, Any]]:
    """Extract individual tweets, threads, and posts from markdown body.

    Recognises:
    - Thread blocks  (### Thread ...)
    - Numbered or bulleted lists
    - Sections separated by horizontal rules (---)
    - Standalone paragraphs
    """
    items: List[Dict[str, Any]] = []
    working_body = body

    # --- Thread blocks ---
    thread_re = re.compile(
        r"(?:^|\n)#{2,3}\s*[Tt]hread[^\n]*\n(.*?)(?=\n#{2,3}\s|\Z)", re.DOTALL
    )
    for m in thread_re.finditer(body):
        thread_body = m.group(1)
        tweets = _extract_numbered_or_bulleted(thread_body)
        if len(tweets) >= 2:
            items.append({
                "type": "thread",
                "tweets": [_clean_tweet_text(t) for t in tweets],
                "text": "\n\n".join(_clean_tweet_text(t) for t in tweets),
            })
            working_body = working_body.replace(thread_body, "", 1)

    # --- Numbered / bulleted lists in remaining body ---
    list_items = _extract_numbered_or_bulleted(working_body)
    if list_items and len(list_items) >= 2:
        for raw in list_items:
            clean = _clean_tweet_text(raw)
            if clean and len(clean) >= 15:
                items.append({"type": "tweet", "text": clean, "tweets": [clean]})
        return items  # lists are the dominant structure, skip paragraph fallback

    # --- Horizontal-rule sections ---
    hr_sections = re.split(r"\n---+\n", working_body)
    if len(hr_sections) >= 2:
        for section in hr_sections:
            clean = _clean_tweet_text(section)
            if clean and len(clean) >= 15:
                items.append({"type": "tweet", "text": clean, "tweets": [clean]})
        return items

    # --- Paragraph fallback ---
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", working_body) if p.strip()]
    for para in paragraphs:
        clean = _clean_tweet_text(para)
        if not clean or len(clean) < 15:
            continue
        # Skip headings and metadata lines
        if re.match(r"^#{1,4}\s", para):
            continue
        if re.match(r"^(status|type|account|tags):", para, re.I):
            continue

        if len(clean) > 600:
            thread_tweets = _split_into_thread(clean)
            items.append({"type": "thread", "text": clean, "tweets": thread_tweets})
        else:
            items.append({"type": "tweet", "text": clean, "tweets": [clean]})

    return items


# ---------------------------------------------------------------------------
# Content classification helpers
# ---------------------------------------------------------------------------
def detect_content_type(metadata: Dict[str, str], text: str) -> str:
    """Return a content-type string from metadata or text heuristics."""
    for key in ("type", "content_type", "format"):
        if key in metadata:
            val = metadata[key].lower().strip()
            if val in CONTENT_TYPE_TO_SLOT:
                return val

    tags = metadata.get("tags", "").lower()
    text_lower = text.lower()

    if "thread" in tags or text.count("\n\n") >= 4 or len(text) > 800:
        return "thread"
    if any(w in text_lower for w in ["hot take", "controversial", "unpopular opinion"]):
        return "hot_take"
    if any(w in text_lower for w in ["tool", "automation", "workflow", "stack"]):
        return "tool"
    if any(w in text_lower for w in ["revenue", "$", "mrr", "arr", "income"]):
        return "revenue"
    if any(w in text_lower for w in ["community", "together", "shoutout", "s/o"]):
        return "community"
    if any(w in text_lower for w in ["behind the scenes", "bts", "building in public"]):
        return "behind_scenes"
    if any(w in text_lower for w in ["reflection", "looking back", "lessons"]):
        return "reflection"
    return "tweet"


def detect_theme_matches(text: str) -> List[str]:
    """Return weekly themes that this content could fill."""
    text_lower = text.lower()
    theme_kw: Dict[str, List[str]] = {
        "tools_automation":    ["tool", "automation", "workflow", "api", "script", "bot", "stack"],
        "revenue_numbers":     ["revenue", "$", "mrr", "arr", "income", "profit", "sales", "conversion"],
        "hot_take":            ["hot take", "controversial", "unpopular", "disagree", "wrong", "overrated"],
        "thread_day":          ["thread", "breakdown", "deep dive", "step by step"],
        "community":           ["community", "shoutout", "collab", "together", "dm me", "reply"],
        "behind_scenes":       ["behind the scenes", "bts", "building", "shipping", "wip"],
        "reflection_planning": ["reflection", "lesson", "looking back", "planning", "goals"],
    }
    matches = [
        theme for theme, kws in theme_kw.items() if any(kw in text_lower for kw in kws)
    ]
    return matches or ["tools_automation"]


# ---------------------------------------------------------------------------
# Content scanning
# ---------------------------------------------------------------------------
def scan_content_dir(account: str) -> List[Dict[str, Any]]:
    """Scan CONTENT/social/{account}/ for .md files with schedulable content."""
    content_path = ACCOUNT_CONTENT_DIRS.get(account)
    if content_path is None:
        log(f"Unknown account: {account}")
        return []
    if not content_path.exists():
        log(f"Content directory missing: {content_path}")
        return []

    safe_path(content_path)
    items: List[Dict[str, Any]] = []

    md_files = sorted(content_path.glob("*.md"))
    log(f"Found {len(md_files)} .md files in {content_path}")

    for md_file in md_files:
        try:
            raw = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            log(f"Error reading {md_file.name}: {e}")
            continue

        metadata, body = parse_frontmatter(raw)

        # Accept PENDING_REVIEW, ready, draft, pending, approved, or no explicit status
        status = metadata.get("status", "").lower().strip()
        if status and status not in (
            "pending_review", "ready", "draft", "pending", "approved", ""
        ):
            continue

        # Skip non-content files
        title = metadata.get("title", md_file.stem).lower()
        skip_words = ["changelog", "index", "readme", "template", "buffer_export", "tweetlio_export"]
        if any(sw in title for sw in skip_words):
            continue
        if md_file.name.startswith("BUFFER_EXPORT") or md_file.name.startswith("TWEETLIO_EXPORT"):
            continue

        content_items = extract_tweets_from_body(body)
        if not content_items:
            clean_body = _clean_tweet_text(body)
            if clean_body and len(clean_body) >= 15:
                if len(clean_body) <= 280:
                    content_items = [{"type": "tweet", "text": clean_body, "tweets": [clean_body]}]
                else:
                    content_items = [{
                        "type": "thread",
                        "text": clean_body,
                        "tweets": _split_into_thread(clean_body),
                    }]

        for ci in content_items:
            content_type = detect_content_type(metadata, ci["text"])
            slot_type = CONTENT_TYPE_TO_SLOT.get(content_type, "value_tweet")
            items.append({
                "account": account,
                "source_file": md_file.name,
                "source_path": str(md_file),
                "title": metadata.get("title", md_file.stem),
                "status": status or "pending_review",
                "content_type": content_type,
                "slot_type": slot_type,
                "theme_matches": detect_theme_matches(ci["text"]),
                "type": ci["type"],
                "text": ci["text"],
                "tweets": ci.get("tweets", [ci["text"]]),
                "char_count": len(ci["text"]),
                "metadata": metadata,
            })

    log(f"Extracted {len(items)} content items from {account}/")
    return items


def scan_all_accounts(accounts: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    return {acct: scan_content_dir(acct) for acct in accounts}


# ---------------------------------------------------------------------------
# Schedule generation
# ---------------------------------------------------------------------------
def assign_content_to_slots(
    items: List[Dict[str, Any]],
    start_date: datetime,
    days: int = 7,
) -> List[Dict[str, Any]]:
    """Map content items onto daily time slots over *days* days.

    Follows the weekly rhythm and daily posting schedule.
    """
    scheduled: List[Dict[str, Any]] = []

    # Bucket items by slot type
    by_slot: Dict[str, List[Dict[str, Any]]] = {
        slot["slot_type"]: [] for slot in DAILY_SLOTS
    }
    unassigned: List[Dict[str, Any]] = []

    for item in items:
        st = item.get("slot_type", "value_tweet")
        if st in by_slot:
            by_slot[st].append(item)
        else:
            unassigned.append(item)

    # Spread unassigned items across smallest buckets
    for item in unassigned:
        smallest = min(by_slot, key=lambda s: len(by_slot[s]))
        by_slot[smallest].append(item)

    # Fill day-by-day
    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        weekday = current_date.weekday()
        theme_info = WEEKLY_THEMES.get(weekday, WEEKLY_THEMES[0])
        theme = theme_info["theme"]
        date_str = current_date.strftime("%Y-%m-%d")

        for slot in DAILY_SLOTS:
            slot_type = slot["slot_type"]
            slot_time = slot["time"]
            slot_label = slot["label"]

            candidates = by_slot.get(slot_type, [])

            # Borrow from other slots if empty
            if not candidates:
                for fallback in THEME_SLOT_PREFERENCE.get(theme, ["value_tweet"]):
                    if fallback != slot_type and by_slot.get(fallback):
                        candidates = by_slot[fallback]
                        break

            if not candidates:
                scheduled.append({
                    "date": date_str,
                    "time": slot_time,
                    "slot_type": slot_type,
                    "slot_label": slot_label,
                    "theme": theme,
                    "theme_label": theme_info["label"],
                    "text": f"[EMPTY SLOT - needs {slot_type} content]",
                    "link": "",
                    "image": "",
                    "profile": "",
                    "account": "",
                    "source_file": "",
                    "content_type": "",
                    "is_empty": True,
                })
                continue

            # Prefer content that matches today's theme
            best_idx = 0
            for i, cand in enumerate(candidates):
                if theme in cand.get("theme_matches", []):
                    best_idx = i
                    break
            best = candidates.pop(best_idx)

            text = best["text"]
            if best["type"] == "thread" and best.get("tweets"):
                thread_tweets = best["tweets"]
                if len(thread_tweets) > 1:
                    text = "\n\n".join(
                        f"{i + 1}/{len(thread_tweets)} {t}"
                        for i, t in enumerate(thread_tweets)
                    )

            scheduled.append({
                "date": date_str,
                "time": slot_time,
                "slot_type": slot_type,
                "slot_label": slot_label,
                "theme": theme,
                "theme_label": theme_info["label"],
                "text": text,
                "link": best.get("metadata", {}).get("link", ""),
                "image": best.get("metadata", {}).get("image", ""),
                "profile": f"{best['account']} Twitter",
                "account": best["account"],
                "source_file": best.get("source_file", ""),
                "content_type": best.get("content_type", ""),
                "is_empty": False,
            })

    return scheduled


# ---------------------------------------------------------------------------
# Buffer CSV export
# ---------------------------------------------------------------------------
BUFFER_FIELDS = [
    "Text", "Link", "Image", "Scheduled Date", "Scheduled Time", "Profile",
]


def generate_buffer_csv(
    scheduled: List[Dict[str, Any]],
    account: str,
) -> Optional[Path]:
    """Write Buffer-compatible CSV to CONTENT/social/{account}/BUFFER_EXPORT_{date}.csv"""
    entries = [s for s in scheduled if not s.get("is_empty", False)]
    if not entries:
        log(f"No content to export for {account}")
        return None

    output_dir = ACCOUNT_CONTENT_DIRS.get(account, CONTENT_DIR / account)
    safe_path(output_dir).mkdir(parents=True, exist_ok=True)

    date_stamp = datetime.now().strftime("%Y%m%d")
    output_file = safe_path(output_dir / f"BUFFER_EXPORT_{date_stamp}.csv")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=BUFFER_FIELDS)
        writer.writeheader()
        for entry in entries:
            writer.writerow({
                "Text": entry["text"],
                "Link": entry.get("link", ""),
                "Image": entry.get("image", ""),
                "Scheduled Date": entry["date"],
                "Scheduled Time": entry["time"],
                "Profile": entry.get("profile", f"{account} Twitter"),
            })

    log(f"Buffer CSV: {output_file} ({len(entries)} rows)")
    return output_file


# ---------------------------------------------------------------------------
# Tweetlio JSON export
# ---------------------------------------------------------------------------
def generate_tweetlio_json(
    scheduled: List[Dict[str, Any]],
    account: str,
) -> Optional[Path]:
    """Write Tweetlio-compatible JSON to CONTENT/social/{account}/TWEETLIO_EXPORT_{date}.json

    Tweetlio schema per entry:
        content        - full tweet text
        scheduledDate  - ISO-8601 datetime string
        type           - "tweet" | "thread"
        threadTweets   - list of strings (threads only)
    """
    entries = [s for s in scheduled if not s.get("is_empty", False)]
    if not entries:
        return None

    output_dir = ACCOUNT_CONTENT_DIRS.get(account, CONTENT_DIR / account)
    safe_path(output_dir).mkdir(parents=True, exist_ok=True)

    date_stamp = datetime.now().strftime("%Y%m%d")
    output_file = safe_path(output_dir / f"TWEETLIO_EXPORT_{date_stamp}.json")

    tweetlio_entries: List[Dict[str, Any]] = []
    for entry in entries:
        scheduled_dt = f"{entry['date']}T{entry['time']}:00"
        is_thread = entry.get("slot_type") == "thread" or entry.get("content_type") == "thread"

        tl: Dict[str, Any] = {
            "content": entry["text"],
            "scheduledDate": scheduled_dt,
            "type": "thread" if is_thread else "tweet",
            "metadata": {
                "slot_type": entry.get("slot_type", ""),
                "theme": entry.get("theme", ""),
                "source_file": entry.get("source_file", ""),
                "account": entry.get("account", account),
            },
        }

        if is_thread:
            parts = re.split(r"\n\n\d+/\d+\s", entry["text"])
            if len(parts) > 1:
                first = re.sub(r"^\d+/\d+\s", "", parts[0])
                tl["threadTweets"] = [first.strip()] + [p.strip() for p in parts[1:]]
            else:
                tl["threadTweets"] = _split_into_thread(entry["text"])

        tweetlio_entries.append(tl)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tweetlio_entries, f, indent=2, ensure_ascii=False)

    log(f"Tweetlio JSON: {output_file} ({len(tweetlio_entries)} entries)")
    return output_file


# ---------------------------------------------------------------------------
# CLI: --scan
# ---------------------------------------------------------------------------
def cmd_scan(accounts: List[str]) -> None:
    """Scan content files and report what is available for scheduling."""
    all_items = scan_all_accounts(accounts)
    total = 0

    for account, items in all_items.items():
        print(f"\n{'=' * 60}")
        print(f"  Account: @{account}")
        print(f"  Directory: {ACCOUNT_CONTENT_DIRS.get(account, 'N/A')}")
        print(f"  Items found: {len(items)}")
        print(f"{'=' * 60}")

        if not items:
            print("  No schedulable content found.")
            continue

        # Group by source file
        by_file: Dict[str, List[Dict[str, Any]]] = {}
        for item in items:
            by_file.setdefault(item["source_file"], []).append(item)

        for fname, file_items in by_file.items():
            print(f"\n  {fname}:")
            for fi in file_items:
                status_tag = fi["status"].upper()
                type_tag = fi["type"].upper()
                ctype = fi["content_type"]
                chars = fi["char_count"]
                preview = fi["text"][:80].replace("\n", " ")
                print(f"    [{status_tag}] [{type_tag}] ({ctype}, {chars} chars)")
                print(f"      {preview}...")

        # Summaries
        type_counts: Dict[str, int] = {}
        slot_counts: Dict[str, int] = {}
        for item in items:
            type_counts[item["type"]] = type_counts.get(item["type"], 0) + 1
            slot_counts[item["slot_type"]] = slot_counts.get(item["slot_type"], 0) + 1

        print("\n  By type:")
        for t, c in sorted(type_counts.items()):
            print(f"    {t}: {c}")
        print("\n  By slot assignment:")
        for s, c in sorted(slot_counts.items()):
            print(f"    {s}: {c}")

        total += len(items)

    needed = 7 * len(DAILY_SLOTS)
    print(f"\n{'=' * 60}")
    print(f"  TOTAL: {total} content items across {len(accounts)} account(s)")
    print(f"  7-day schedule needs {needed} slots")
    if total >= needed:
        print(f"  Coverage: FULL ({total - needed} surplus)")
    else:
        print(f"  Coverage: GAPS ({needed - total} empty slots expected)")
    print(f"{'=' * 60}")


# ---------------------------------------------------------------------------
# CLI: --generate
# ---------------------------------------------------------------------------
def cmd_generate(accounts: List[str]) -> None:
    """Generate Buffer CSV and Tweetlio JSON for the next 7 days."""
    start_date = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + timedelta(days=1)
    all_items = scan_all_accounts(accounts)

    for account, items in all_items.items():
        if not items:
            print(f"\n  @{account}: No content to schedule.")
            continue

        print(f"\n  @{account}: Scheduling {len(items)} items over 7 days...")

        scheduled = assign_content_to_slots(items, start_date, days=7)

        csv_path = generate_buffer_csv(scheduled, account)
        if csv_path:
            print(f"  Buffer CSV:    {csv_path}")

        json_path = generate_tweetlio_json(scheduled, account)
        if json_path:
            print(f"  Tweetlio JSON: {json_path}")

        filled = sum(1 for s in scheduled if not s.get("is_empty", False))
        empty = sum(1 for s in scheduled if s.get("is_empty", False))
        print(f"  Slots: {filled}/{len(scheduled)} filled, {empty} empty")

        by_day: Dict[str, int] = {}
        for s in scheduled:
            if not s.get("is_empty", False):
                by_day[s["date"]] = by_day.get(s["date"], 0) + 1

        print("  Daily breakdown:")
        for date_str in sorted(by_day):
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = dt.strftime("%a")
            theme_label = WEEKLY_THEMES.get(dt.weekday(), {}).get("label", "")
            print(f"    {date_str} ({day_name}): {by_day[date_str]} posts | {theme_label}")


# ---------------------------------------------------------------------------
# CLI: --preview
# ---------------------------------------------------------------------------
def cmd_preview(accounts: List[str]) -> None:
    """Display what would be scheduled without writing any files."""
    start_date = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + timedelta(days=1)
    all_items = scan_all_accounts(accounts)

    for account, items in all_items.items():
        if not items:
            print(f"\n  @{account}: No content to preview.")
            continue

        print(f"\n{'=' * 70}")
        print(f"  PREVIEW: @{account} | {len(items)} items | 7-day schedule")
        print(f"{'=' * 70}")

        scheduled = assign_content_to_slots(items, start_date, days=7)

        current_date = ""
        for entry in scheduled:
            if entry["date"] != current_date:
                current_date = entry["date"]
                dt = datetime.strptime(current_date, "%Y-%m-%d")
                day_name = dt.strftime("%A")
                theme_label = entry.get("theme_label", "")
                print(f"\n  --- {current_date} ({day_name}) | {theme_label} ---")

            time_str = entry["time"]
            slot_label = entry["slot_label"]

            if entry.get("is_empty", False):
                print(f"    {time_str} | {slot_label}")
                print(f"             [EMPTY - no content available]")
            else:
                preview = entry["text"][:100].replace("\n", " ")
                source = entry.get("source_file", "?")
                print(f"    {time_str} | {slot_label}")
                print(f"             {preview}...")
                print(f"             (from: {source})")

        filled = sum(1 for s in scheduled if not s.get("is_empty", False))
        empty = sum(1 for s in scheduled if s.get("is_empty", False))
        print(f"\n  Summary: {filled} filled, {empty} empty, {len(scheduled)} total")
        print(f"  NO FILES WRITTEN (preview mode)")


# ---------------------------------------------------------------------------
# Account resolution
# ---------------------------------------------------------------------------
def resolve_accounts(account_arg: str) -> List[str]:
    """Turn CLI --account value into a list of valid account keys."""
    if account_arg.lower() == "all":
        return list(ACCOUNT_CONTENT_DIRS.keys())

    # Exact match
    if account_arg in ACCOUNT_CONTENT_DIRS:
        return [account_arg]

    # Case-insensitive
    lower = account_arg.lower()
    for name in ACCOUNT_CONTENT_DIRS:
        if name.lower() == lower:
            return [name]

    # Comma-separated
    parts = [p.strip().lower() for p in account_arg.split(",")]
    matched = [name for name in ACCOUNT_CONTENT_DIRS if name.lower() in parts]
    if matched:
        return matched

    print(f"Unknown account: {account_arg}")
    print(f"Available: {', '.join(ACCOUNT_CONTENT_DIRS.keys())}, all")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "PRINTMAXX Auto Scheduler: generate Buffer CSV and Tweetlio JSON "
            "from content files in CONTENT/social/"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python3 AUTOMATIONS/auto_scheduler.py --scan --account printmaxxer
  python3 AUTOMATIONS/auto_scheduler.py --generate --account all
  python3 AUTOMATIONS/auto_scheduler.py --preview --account selahmoments
        """,
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan content files and show what is available for scheduling",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate Buffer CSV + Tweetlio JSON for the next 7 days",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show what would be scheduled without writing any files",
    )
    parser.add_argument(
        "--account",
        type=str,
        default="printmaxxer",
        metavar="ACCOUNT",
        help="Account to process: printmaxxer | selahmoments | all (default: printmaxxer)",
    )

    args = parser.parse_args()
    accounts = resolve_accounts(args.account)

    ran = False
    if args.scan:
        cmd_scan(accounts)
        ran = True
    if args.generate:
        cmd_generate(accounts)
        ran = True
    if args.preview:
        cmd_preview(accounts)
        ran = True

    if not ran:
        parser.print_help()


if __name__ == "__main__":
    main()
