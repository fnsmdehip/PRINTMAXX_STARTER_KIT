#!/usr/bin/env python3
"""
PRINTMAXX Content Factory
=========================
Unified content pipeline: ingest -> adapt -> schedule -> track -> recycle.

Takes content from CONTENT/social/{niche}/ directories, adapts for multiple
platforms, schedules with natural timing, tracks what's posted, and recycles
top performers after 30 days.

CLI:
  --status          Show factory status (content counts, queue depth, recycling)
  --ingest          Scan content dirs and load new pieces into the queue
  --adapt           Adapt queued content for all target platforms
  --schedule        Generate Buffer-compatible CSVs with optimal timing
  --recycle-winners Re-queue top performers with modifications (30+ days old)
  --factory INPUT   Take a single piece of text and generate 50+ adapted variants
  --dry-run         Preview actions without writing files
  --niche NICHE     Filter to specific niche (faith, fitness, tech, etc.)
  --platform PLAT   Filter to specific platform (twitter, linkedin, reddit, etc.)
  --export-buffer   Export scheduled content as Buffer-compatible CSVs
  --daily           Run full daily cycle: ingest + adapt + schedule + recycle

Usage:
  python3 AUTOMATIONS/content_factory.py --status
  python3 AUTOMATIONS/content_factory.py --daily --dry-run
  python3 AUTOMATIONS/content_factory.py --factory "cold emailed 200 dentists. 27% open rate. booked 4 calls."
  python3 AUTOMATIONS/content_factory.py --ingest --niche faith
  python3 AUTOMATIONS/content_factory.py --export-buffer --platform twitter
  python3 AUTOMATIONS/content_factory.py --recycle-winners
"""

import os
import sys
import csv
import json
import re
import hashlib
import argparse
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_SOCIAL = BASE_DIR / "CONTENT" / "social"
LEDGER_DIR = BASE_DIR / "LEDGER"
OPS_DIR = BASE_DIR / "OPS"
AUTOMATIONS_DIR = BASE_DIR / "AUTOMATIONS"
CONTENT_POSTING = AUTOMATIONS_DIR / "content_posting"
BUFFER_EXPORT_DIR = AUTOMATIONS_DIR / "content_posting" / "buffer_exports"

# Tracking files
FACTORY_QUEUE_CSV = LEDGER_DIR / "CONTENT_FACTORY_QUEUE.csv"
FACTORY_POSTED_CSV = LEDGER_DIR / "CONTENT_FACTORY_POSTED.csv"
FACTORY_RECYCLED_CSV = LEDGER_DIR / "CONTENT_FACTORY_RECYCLED.csv"
CONTENT_POSTED_CSV = LEDGER_DIR / "CONTENT_POSTED.csv"
CONTENT_PERFORMANCE_CSV = LEDGER_DIR / "CONTENT_PERFORMANCE.csv"
CONTENT_WINNERS_CSV = LEDGER_DIR / "CONTENT_WINNERS.csv"


def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(BASE_DIR)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved


# ---------------------------------------------------------------------------
# ACCOUNT + PLATFORM CONFIG
# ---------------------------------------------------------------------------
ACCOUNTS = {
    "printmaxxer":  {"niche": "tech",     "handle": "@PRINTMAXXER",    "platforms": ["twitter", "linkedin", "reddit"]},
    "growthpilled": {"niche": "tech",     "handle": "@growthpilled",   "platforms": ["twitter", "linkedin"]},
    "outboundtwts": {"niche": "tech",     "handle": "@outboundtwts",   "platforms": ["twitter", "linkedin"]},
    "clipvault":    {"niche": "memes",    "handle": "@clipvault_",     "platforms": ["twitter", "tiktok", "instagram"]},
    "toolstwts":    {"niche": "tech",     "handle": "@toolstwts",      "platforms": ["twitter"]},
    "repscheme":    {"niche": "fitness",  "handle": "@repscheme",      "platforms": ["twitter", "tiktok", "instagram"]},
    "voidpilled":   {"niche": "esoteric", "handle": "@voidpilled",     "platforms": ["twitter"]},
    "selahmoments": {"niche": "faith",    "handle": "@selahmoments",   "platforms": ["twitter", "tiktok", "instagram"]},
    "shiplog":      {"niche": "tech",     "handle": "@shiplog_",       "platforms": ["twitter"]},
    "silentframes": {"niche": "aesthetic","handle": "@silentframes",   "platforms": ["twitter", "instagram"]},
    "velvetframes": {"niche": "beauty",   "handle": "@velvetframes",   "platforms": ["twitter", "instagram"]},
    "drifthour":    {"niche": "ambient",  "handle": "@drifthour",      "platforms": ["twitter", "youtube"]},
}

# Map niches to content directories
NICHE_DIRS = {
    "tech":      ["printmaxxer", "ai", "growthpilled", "outboundtwts", "toolstwts", "shiplog"],
    "faith":     ["faith", "selahmoments", "ramadan"],
    "fitness":   ["fitness", "repscheme"],
    "memes":     ["memes", "clipvault"],
    "esoteric":  ["esoteric"],
    "aesthetic":  ["aesthetic", "silentframes"],
    "beauty":    ["beauty_curated"],
    "ambient":   ["drifthour"],
    "findom":    ["findom"],
}

# Peak posting times per platform (UTC hours). 2-4 slots per platform.
PLATFORM_PEAK_TIMES = {
    "twitter":   [13, 17, 22, 1],     # 8am, 12pm, 5pm, 8pm EST
    "linkedin":  [12, 16, 21],         # 7am, 11am, 4pm EST
    "tiktok":    [11, 17, 2],          # 6am, 12pm, 9pm EST
    "instagram": [14, 19, 0],          # 9am, 2pm, 7pm EST
    "reddit":    [13, 18, 23],         # 8am, 1pm, 6pm EST
    "youtube":   [15, 20],             # 10am, 3pm EST
    "substack":  [14],                 # 9am EST (1 post/day max)
}

# Character limits per platform
CHAR_LIMITS = {
    "twitter":   280,
    "linkedin":  3000,
    "tiktok":    2200,
    "instagram": 2200,
    "reddit":    40000,
    "youtube":   5000,
    "substack":  100000,
}

# Hashtag strategies per platform
HASHTAG_STRATEGY = {
    "twitter":   {"count": (0, 2), "style": "minimal"},        # 0-2 hashtags, embedded
    "linkedin":  {"count": (0, 3), "style": "bottom"},         # 0-3 at bottom
    "tiktok":    {"count": (3, 7), "style": "bottom_fyp"},     # 3-7, always include #fyp
    "instagram": {"count": (5, 15), "style": "bottom_block"},  # 5-15 in block
    "reddit":    {"count": (0, 0), "style": "none"},           # zero hashtags
    "youtube":   {"count": (3, 8), "style": "description"},    # in description
    "substack":  {"count": (0, 0), "style": "none"},
}

# Niche-specific hashtag pools
NICHE_HASHTAGS = {
    "tech":     ["#buildinpublic", "#indiehackers", "#solopreneur", "#saas", "#automation",
                 "#startup", "#coding", "#ai", "#productivity", "#nocode"],
    "faith":    ["#faith", "#prayer", "#christianity", "#bible", "#godisgood",
                 "#prayerlife", "#devotional", "#scripture", "#morningprayer", "#faithjourney"],
    "fitness":  ["#fitness", "#gym", "#workout", "#gains", "#fitfam",
                 "#bodybuilding", "#nutrition", "#protein", "#training", "#healthylifestyle"],
    "memes":    ["#memes", "#funny", "#viral", "#relatable", "#trending"],
    "esoteric": ["#philosophy", "#consciousness", "#wisdom", "#awakening", "#metaphysics"],
    "aesthetic": ["#aesthetic", "#photography", "#art", "#minimal", "#design"],
    "beauty":   ["#beauty", "#skincare", "#makeup", "#glam", "#selfcare"],
    "ambient":  ["#ambient", "#lofi", "#chill", "#relaxing", "#study"],
    "findom":   ["#findom", "#paypig", "#tribute", "#goddess"],
}

# AI slop words to filter
AI_SLOP = {
    "additionally", "moreover", "furthermore", "testament", "landscape",
    "paradigm", "leverage", "utilize", "delve", "unpack", "comprehensive",
    "robust", "streamlined", "game-changer", "unlock", "elevate",
    "cutting-edge", "innovative", "revolutionary", "empower", "seamless",
    "frictionless", "journey", "groundbreaking", "nestled", "tapestry",
}


# ---------------------------------------------------------------------------
# CONTENT EXTRACTION
# ---------------------------------------------------------------------------

def extract_posts_from_md(filepath: Path) -> list[dict]:
    """Extract individual posts/tweets from a markdown content file."""
    posts = []
    text = filepath.read_text(encoding="utf-8", errors="replace")

    # Skip non-content files
    skip_patterns = ["CENTRAL_INDEX", "GUIDE", "PLAYBOOK", "AUDIT", "STRATEGY", "INDEX"]
    if any(p in filepath.stem.upper() for p in skip_patterns):
        return []

    # Try to detect tweet-style content (numbered lists, separated blocks)
    # Pattern 1: Lines that look like standalone tweets (short, no markdown headers)
    lines = text.split("\n")
    current_block = []
    in_content = False

    for line in lines:
        stripped = line.strip()

        # Skip markdown headers and metadata lines
        if stripped.startswith("#") and len(stripped) < 80:
            if current_block and in_content:
                block_text = "\n".join(current_block).strip()
                if 20 < len(block_text) < 3000 and not block_text.startswith("```"):
                    posts.append({
                        "text": block_text,
                        "source_file": str(filepath.relative_to(BASE_DIR)),
                        "extracted_at": datetime.now(timezone.utc).isoformat(),
                    })
            current_block = []
            in_content = False
            continue

        # Skip code blocks, tables, metadata
        if stripped.startswith("```") or stripped.startswith("|") or stripped.startswith("---"):
            if current_block and in_content:
                block_text = "\n".join(current_block).strip()
                if 20 < len(block_text) < 3000:
                    posts.append({
                        "text": block_text,
                        "source_file": str(filepath.relative_to(BASE_DIR)),
                        "extracted_at": datetime.now(timezone.utc).isoformat(),
                    })
            current_block = []
            in_content = False
            continue

        if stripped:
            in_content = True
            current_block.append(stripped)
        elif current_block and in_content:
            # Empty line = block separator
            block_text = "\n".join(current_block).strip()
            if 20 < len(block_text) < 3000 and not block_text.startswith("```"):
                posts.append({
                    "text": block_text,
                    "source_file": str(filepath.relative_to(BASE_DIR)),
                    "extracted_at": datetime.now(timezone.utc).isoformat(),
                })
            current_block = []
            in_content = False

    # Don't forget last block
    if current_block and in_content:
        block_text = "\n".join(current_block).strip()
        if 20 < len(block_text) < 3000 and not block_text.startswith("```"):
            posts.append({
                "text": block_text,
                "source_file": str(filepath.relative_to(BASE_DIR)),
                "extracted_at": datetime.now(timezone.utc).isoformat(),
            })

    return posts


def extract_posts_from_csv(filepath: Path) -> list[dict]:
    """Extract posts from a CSV file (Buffer format or similar)."""
    posts = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Try common column names for content text
                text = (row.get("text") or row.get("post_text") or
                        row.get("tweet_text") or row.get("content") or
                        row.get("Text") or "")
                text = text.strip().strip('"')
                if len(text) > 20:
                    posts.append({
                        "text": text,
                        "source_file": str(filepath.relative_to(BASE_DIR)),
                        "extracted_at": datetime.now(timezone.utc).isoformat(),
                    })
    except Exception:
        pass
    return posts


def content_hash(text: str) -> str:
    """Generate a short hash for deduplication."""
    normalized = re.sub(r"\s+", " ", text.lower().strip())
    return hashlib.md5(normalized.encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# PLATFORM ADAPTATION
# ---------------------------------------------------------------------------

def adapt_for_platform(text: str, platform: str, niche: str) -> str:
    """Adapt content text for a specific platform's format and limits."""
    adapted = text.strip()

    # Clean AI slop
    for word in AI_SLOP:
        pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        adapted = pattern.sub("", adapted)

    # Remove em dashes
    adapted = adapted.replace("—", ". ").replace("–", ". ")

    # Platform-specific formatting
    if platform == "twitter":
        # Keep short. Remove excessive hashtags. Lowercase energy.
        adapted = adapted.lower() if not any(c.isupper() for c in adapted[:3]) else adapted
        if len(adapted) > 280:
            # Truncate at last sentence boundary before 277 chars
            truncated = adapted[:277]
            last_period = truncated.rfind(".")
            if last_period > 100:
                adapted = truncated[:last_period + 1]
            else:
                adapted = truncated.rstrip() + "..."
        # Strip hashtags for twitter (they hurt reach)
        adapted = re.sub(r"#\w+\s*", "", adapted).strip()

    elif platform == "linkedin":
        # Professional tone. Add line breaks for readability.
        # Capitalize first letter of sentences
        sentences = adapted.split(". ")
        adapted = ".\n\n".join(s.strip().capitalize() if s else s for s in sentences if s.strip())
        if not adapted.endswith("."):
            adapted += "."

    elif platform == "tiktok":
        # Short caption. Add #fyp. Casual tone.
        if len(adapted) > 300:
            # Use first 2-3 sentences as caption
            sentences = re.split(r"[.!?]+", adapted)
            caption_parts = []
            length = 0
            for s in sentences:
                s = s.strip()
                if not s:
                    continue
                if length + len(s) > 250:
                    break
                caption_parts.append(s)
                length += len(s)
            adapted = ". ".join(caption_parts)
            if not adapted.endswith((".", "!", "?")):
                adapted += "."

    elif platform == "instagram":
        # Longer caption OK. Add line breaks.
        adapted = adapted.replace(". ", ".\n\n")

    elif platform == "reddit":
        # No hashtags. Conversational. Can be longer.
        adapted = re.sub(r"#\w+\s*", "", adapted).strip()
        # Remove promotional CTAs for Reddit
        cta_patterns = [r"link in bio", r"reply \w+ for", r"DM me for"]
        for pat in cta_patterns:
            adapted = re.sub(pat, "", adapted, flags=re.IGNORECASE).strip()

    elif platform == "youtube":
        # Description format. Can include links and timestamps.
        pass

    elif platform == "substack":
        # Newsletter format. Expand into paragraphs.
        adapted = adapted.replace(". ", ".\n\n")

    # Add hashtags based on platform strategy
    hashtag_config = HASHTAG_STRATEGY.get(platform, {"count": (0, 0), "style": "none"})
    min_tags, max_tags = hashtag_config["count"]
    if max_tags > 0 and niche in NICHE_HASHTAGS:
        pool = NICHE_HASHTAGS[niche]
        num_tags = random.randint(min_tags, min(max_tags, len(pool)))
        selected = random.sample(pool, num_tags)

        if platform == "tiktok":
            selected = ["#fyp"] + [t for t in selected if t != "#fyp"]

        tag_str = " ".join(selected)

        if hashtag_config["style"] in ("bottom", "bottom_fyp", "bottom_block", "description"):
            adapted = adapted.rstrip() + "\n\n" + tag_str
        elif hashtag_config["style"] == "minimal":
            adapted = adapted.rstrip() + " " + tag_str

    # Enforce character limit
    limit = CHAR_LIMITS.get(platform, 5000)
    if len(adapted) > limit:
        adapted = adapted[:limit - 3].rstrip() + "..."

    return adapted.strip()


# ---------------------------------------------------------------------------
# SCHEDULING
# ---------------------------------------------------------------------------

def generate_schedule(posts: list[dict], start_date: datetime = None,
                      days: int = 30, platform_filter: str = None) -> list[dict]:
    """Generate a posting schedule with natural timing jitter."""
    if start_date is None:
        start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        start_date += timedelta(days=1)  # Start tomorrow

    scheduled = []
    # Group posts by account+platform
    post_queue = defaultdict(list)
    for p in posts:
        key = (p.get("account", "printmaxxer"), p.get("platform", "twitter"))
        if platform_filter and key[1] != platform_filter:
            continue
        post_queue[key].append(p)

    for (account, platform), account_posts in post_queue.items():
        peak_hours = PLATFORM_PEAK_TIMES.get(platform, [13, 17])
        posts_per_day = min(len(peak_hours), 4)

        idx = 0
        for day_offset in range(days):
            if idx >= len(account_posts):
                break
            post_date = start_date + timedelta(days=day_offset)

            # Skip weekends for LinkedIn
            if platform == "linkedin" and post_date.weekday() >= 5:
                continue

            for slot_hour in peak_hours[:posts_per_day]:
                if idx >= len(account_posts):
                    break
                # Add jitter: +/- 15 minutes
                jitter_min = random.randint(-15, 15)
                post_time = post_date.replace(hour=slot_hour % 24, minute=max(0, min(59, 30 + jitter_min)))

                entry = account_posts[idx].copy()
                entry["scheduled_at"] = post_time.strftime("%Y-%m-%d %H:%M")
                entry["scheduled_date"] = post_time.strftime("%Y-%m-%d")
                entry["scheduled_time"] = post_time.strftime("%H:%M")
                entry["status"] = "scheduled"
                scheduled.append(entry)
                idx += 1

    # Sort by time
    scheduled.sort(key=lambda x: x.get("scheduled_at", ""))
    return scheduled


# ---------------------------------------------------------------------------
# RECYCLING
# ---------------------------------------------------------------------------

def find_winners_for_recycling(min_age_days: int = 30) -> list[dict]:
    """Find top-performing posts that are old enough to recycle."""
    winners = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=min_age_days)

    if not CONTENT_PERFORMANCE_CSV.exists():
        return winners

    try:
        with open(CONTENT_PERFORMANCE_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                posted_at = row.get("posted_at", "")
                if not posted_at:
                    continue
                try:
                    post_date = datetime.fromisoformat(posted_at.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    continue

                if post_date > cutoff:
                    continue  # Too recent

                # Check if it was a winner (high engagement)
                try:
                    score = float(row.get("winner_score", 0))
                except (ValueError, TypeError):
                    score = 0

                if score >= 50:
                    winners.append({
                        "text": row.get("full_text", row.get("content_preview", "")),
                        "original_account": row.get("account", ""),
                        "original_platform": row.get("platform", ""),
                        "original_score": score,
                        "original_posted_at": posted_at,
                        "source_file": "recycled_winner",
                    })
    except Exception:
        pass

    return winners


def recycle_post(text: str) -> str:
    """Modify a winning post for re-posting (avoid exact duplicate detection)."""
    modifications = [
        # Swap opening
        (r"^(i |I )", lambda m: random.choice(["just ", "update: ", "still true: ", "reminder: ", ""])),
        # Add "update" prefix
        (r"^", lambda m: random.choice(["", "update: ", "still works: ", ""]) if random.random() > 0.5 else ""),
        # Swap "here's" with alternatives
        (r"here'?s", lambda m: random.choice(["here's", "this is", "check"])),
    ]

    recycled = text
    mod_applied = False
    for pattern, replacement in modifications:
        if not mod_applied and random.random() > 0.5:
            try:
                recycled = re.sub(pattern, replacement, recycled, count=1)
                mod_applied = True
            except Exception:
                pass

    if not mod_applied:
        # At minimum, add a subtle variation
        suffixes = [
            "",
            "\n\nstill works.",
            "\n\nthis still hits.",
            "\n\nnothing has changed.",
        ]
        recycled = recycled.rstrip() + random.choice(suffixes)

    return recycled.strip()


# ---------------------------------------------------------------------------
# FACTORY MODE (1 input -> 50+ outputs)
# ---------------------------------------------------------------------------

def factory_expand(text: str, niche: str = "tech") -> list[dict]:
    """Take a single piece of content and generate 50+ adapted variants."""
    variants = []
    source_hash = content_hash(text)

    # 1. Direct platform adaptations (6 platforms)
    for platform in PLATFORM_PEAK_TIMES:
        adapted = adapt_for_platform(text, platform, niche)
        variants.append({
            "text": adapted,
            "platform": platform,
            "niche": niche,
            "variant_type": "platform_adapt",
            "source_hash": source_hash,
        })

    # 2. Hook variations (8 different hooks)
    hook_templates = [
        "most people don't know this: {core}",
        "unpopular opinion: {core}",
        "i tested this for 30 days. {core}",
        "stop doing it wrong. {core}",
        "the thing nobody talks about: {core}",
        "here's what actually works: {core}",
        "this changed everything for me. {core}",
        "everyone's overcomplicating this. {core}",
    ]
    # Extract core message (first 2 sentences)
    sentences = re.split(r"[.!?]+", text)
    core = ". ".join(s.strip() for s in sentences[:2] if s.strip())
    if core and not core.endswith("."):
        core += "."

    for template in hook_templates:
        hooked = template.format(core=core)
        for platform in ["twitter", "linkedin", "tiktok"]:
            adapted = adapt_for_platform(hooked, platform, niche)
            variants.append({
                "text": adapted,
                "platform": platform,
                "niche": niche,
                "variant_type": "hook_variation",
                "source_hash": source_hash,
            })

    # 3. Question format (engagement posts)
    question_templates = [
        "am i the only one who thinks {topic}?",
        "what's your take on {topic}?",
        "agree or disagree: {topic}",
        "{topic}. hot take or common sense?",
    ]
    topic = sentences[0].strip().rstrip(".").lower() if sentences else text[:100]
    for template in question_templates:
        q = template.format(topic=topic)
        for platform in ["twitter", "tiktok"]:
            variants.append({
                "text": q,
                "platform": platform,
                "niche": niche,
                "variant_type": "question_format",
                "source_hash": source_hash,
            })

    # 4. Thread opener (for Twitter threads)
    thread_opener = f"{core}\n\na thread on what i learned:"
    variants.append({
        "text": adapt_for_platform(thread_opener, "twitter", niche),
        "platform": "twitter",
        "niche": niche,
        "variant_type": "thread_opener",
        "source_hash": source_hash,
    })

    # 5. Cross-niche adaptations
    niche_angles = {
        "faith":   "from a spiritual perspective: ",
        "fitness": "this applies to training too. ",
        "tech":    "same principle in tech: ",
        "memes":   "",
    }
    for target_niche, prefix in niche_angles.items():
        if target_niche == niche:
            continue
        cross = prefix + core
        for platform in ["twitter", "instagram"]:
            adapted = adapt_for_platform(cross, platform, target_niche)
            variants.append({
                "text": adapted,
                "platform": platform,
                "niche": target_niche,
                "variant_type": "cross_niche",
                "source_hash": source_hash,
            })

    return variants


# ---------------------------------------------------------------------------
# BUFFER EXPORT
# ---------------------------------------------------------------------------

def export_buffer_csv(scheduled: list[dict], output_dir: Path = None):
    """Export scheduled content as Buffer-compatible CSVs, one per account+platform."""
    if output_dir is None:
        output_dir = BUFFER_EXPORT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    grouped = defaultdict(list)
    for entry in scheduled:
        key = f"{entry.get('account', 'unknown')}_{entry.get('platform', 'unknown')}"
        grouped[key].append(entry)

    files_written = []
    for key, entries in grouped.items():
        filepath = safe_path(output_dir / f"buffer_{key}.csv")
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "Text"])
            for e in entries:
                writer.writerow([
                    e.get("scheduled_date", ""),
                    e.get("scheduled_time", ""),
                    e.get("text", ""),
                ])
        files_written.append(str(filepath.relative_to(BASE_DIR)))

    return files_written


# ---------------------------------------------------------------------------
# QUEUE MANAGEMENT
# ---------------------------------------------------------------------------

def load_queue() -> list[dict]:
    """Load the content factory queue."""
    if not FACTORY_QUEUE_CSV.exists():
        return []
    try:
        with open(FACTORY_QUEUE_CSV, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def save_queue(entries: list[dict]):
    """Save the content factory queue."""
    if not entries:
        return
    fieldnames = ["queue_id", "content_hash", "text", "niche", "account", "platform",
                  "variant_type", "source_file", "source_hash", "status",
                  "scheduled_at", "scheduled_date", "scheduled_time",
                  "created_at", "posted_at"]

    FACTORY_QUEUE_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(FACTORY_QUEUE_CSV), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(entries)


def load_posted_hashes() -> set:
    """Load hashes of already-posted content for dedup."""
    hashes = set()
    for csv_path in [FACTORY_POSTED_CSV, CONTENT_POSTED_CSV]:
        if csv_path.exists():
            try:
                with open(csv_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        h = row.get("content_hash", "")
                        if h:
                            hashes.add(h)
            except Exception:
                pass
    return hashes


# ---------------------------------------------------------------------------
# INGEST
# ---------------------------------------------------------------------------

def ingest_content(niche_filter: str = None) -> list[dict]:
    """Scan CONTENT/social/ directories and extract new content pieces."""
    all_posts = []
    posted_hashes = load_posted_hashes()
    queue_hashes = {e.get("content_hash", "") for e in load_queue()}
    known_hashes = posted_hashes | queue_hashes

    # Also scan CSV content files
    csv_dirs = [CONTENT_POSTING]

    for niche, dirs in NICHE_DIRS.items():
        if niche_filter and niche != niche_filter:
            continue

        for dirname in dirs:
            content_dir = CONTENT_SOCIAL / dirname
            if not content_dir.exists():
                continue

            # Scan .md files
            for md_file in content_dir.glob("*.md"):
                posts = extract_posts_from_md(md_file)
                for p in posts:
                    h = content_hash(p["text"])
                    if h not in known_hashes:
                        p["niche"] = niche
                        p["content_hash"] = h
                        p["status"] = "queued"
                        p["created_at"] = datetime.now(timezone.utc).isoformat()
                        all_posts.append(p)
                        known_hashes.add(h)

    # Scan CSV files in content_posting/
    for csv_dir in csv_dirs:
        if not csv_dir.exists():
            continue
        for csv_file in csv_dir.glob("*.csv"):
            posts = extract_posts_from_csv(csv_file)
            for p in posts:
                h = content_hash(p["text"])
                if h not in known_hashes:
                    # Guess niche from filename
                    fname = csv_file.stem.lower()
                    niche = "tech"
                    for n in NICHE_DIRS:
                        if n in fname:
                            niche = n
                            break
                    if niche_filter and niche != niche_filter:
                        continue
                    p["niche"] = niche
                    p["content_hash"] = h
                    p["status"] = "queued"
                    p["created_at"] = datetime.now(timezone.utc).isoformat()
                    all_posts.append(p)
                    known_hashes.add(h)

    return all_posts


# ---------------------------------------------------------------------------
# ADAPT
# ---------------------------------------------------------------------------

def adapt_queue(queue: list[dict], platform_filter: str = None) -> list[dict]:
    """Take queued content and create platform-adapted versions."""
    adapted_entries = []
    posted_hashes = load_posted_hashes()

    for entry in queue:
        if entry.get("status") != "queued":
            continue
        if entry.get("platform"):
            # Already adapted
            adapted_entries.append(entry)
            continue

        text = entry.get("text", "")
        niche = entry.get("niche", "tech")

        # Find accounts for this niche
        target_accounts = [(name, info) for name, info in ACCOUNTS.items()
                           if info["niche"] == niche]
        if not target_accounts:
            # Default to printmaxxer for tech content
            target_accounts = [("printmaxxer", ACCOUNTS["printmaxxer"])]

        for account_name, account_info in target_accounts:
            for platform in account_info["platforms"]:
                if platform_filter and platform != platform_filter:
                    continue

                adapted_text = adapt_for_platform(text, platform, niche)
                h = content_hash(adapted_text)

                if h in posted_hashes:
                    continue

                adapted_entries.append({
                    "queue_id": f"CF_{h}",
                    "content_hash": h,
                    "text": adapted_text,
                    "niche": niche,
                    "account": account_name,
                    "platform": platform,
                    "variant_type": "platform_adapt",
                    "source_file": entry.get("source_file", ""),
                    "source_hash": entry.get("content_hash", ""),
                    "status": "adapted",
                    "created_at": entry.get("created_at", datetime.now(timezone.utc).isoformat()),
                })

    return adapted_entries


# ---------------------------------------------------------------------------
# STATUS
# ---------------------------------------------------------------------------

def show_status():
    """Show factory status overview."""
    queue = load_queue()
    posted_hashes = load_posted_hashes()

    # Count content files
    md_count = 0
    csv_count = 0
    for niche, dirs in NICHE_DIRS.items():
        for dirname in dirs:
            d = CONTENT_SOCIAL / dirname
            if d.exists():
                md_count += len(list(d.glob("*.md")))
    for f in CONTENT_POSTING.glob("*.csv"):
        csv_count += 1

    # Queue stats
    queued = len([e for e in queue if e.get("status") == "queued"])
    adapted = len([e for e in queue if e.get("status") == "adapted"])
    scheduled = len([e for e in queue if e.get("status") == "scheduled"])

    # Platform breakdown
    platform_counts = defaultdict(int)
    niche_counts = defaultdict(int)
    for e in queue:
        platform_counts[e.get("platform", "unknown")] += 1
        niche_counts[e.get("niche", "unknown")] += 1

    print("=" * 60)
    print("  PRINTMAXX CONTENT FACTORY STATUS")
    print("=" * 60)
    print()
    print(f"  Content Sources:")
    print(f"    Markdown files:    {md_count}")
    print(f"    CSV files:         {csv_count}")
    print(f"    Content dirs:      {len(NICHE_DIRS)} niches")
    print()
    print(f"  Queue:")
    print(f"    Raw/queued:        {queued}")
    print(f"    Adapted:           {adapted}")
    print(f"    Scheduled:         {scheduled}")
    print(f"    Total in queue:    {len(queue)}")
    print(f"    Already posted:    {len(posted_hashes)}")
    print()
    if platform_counts:
        print(f"  By Platform:")
        for plat, count in sorted(platform_counts.items(), key=lambda x: -x[1]):
            print(f"    {plat:15s}  {count}")
        print()
    if niche_counts:
        print(f"  By Niche:")
        for niche, count in sorted(niche_counts.items(), key=lambda x: -x[1]):
            print(f"    {niche:15s}  {count}")
    print()

    # Recycling candidates
    winners = find_winners_for_recycling()
    print(f"  Recycling:")
    print(f"    Winners 30d+ old:  {len(winners)}")
    print()
    print("=" * 60)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Content Factory")
    parser.add_argument("--status", action="store_true", help="Show factory status")
    parser.add_argument("--ingest", action="store_true", help="Scan and ingest new content")
    parser.add_argument("--adapt", action="store_true", help="Adapt queued content for platforms")
    parser.add_argument("--schedule", action="store_true", help="Generate posting schedule")
    parser.add_argument("--recycle-winners", action="store_true", help="Re-queue top performers")
    parser.add_argument("--factory", type=str, help="Factory mode: expand single input to 50+ variants")
    parser.add_argument("--export-buffer", action="store_true", help="Export Buffer-compatible CSVs")
    parser.add_argument("--daily", action="store_true", help="Full daily cycle")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--niche", type=str, help="Filter by niche")
    parser.add_argument("--platform", type=str, help="Filter by platform")
    parser.add_argument("--days", type=int, default=30, help="Schedule days ahead (default: 30)")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.factory:
        niche = args.niche or "tech"
        variants = factory_expand(args.factory, niche)
        print(f"\nFactory mode: generated {len(variants)} variants from input\n")
        for i, v in enumerate(variants[:10], 1):
            print(f"  [{i}] ({v['platform']}/{v['niche']}/{v['variant_type']})")
            preview = v["text"][:120].replace("\n", " ")
            print(f"      {preview}...")
            print()
        if len(variants) > 10:
            print(f"  ... and {len(variants) - 10} more variants")
        print()

        if not args.dry_run:
            # Save variants to queue
            queue = load_queue()
            for v in variants:
                v["queue_id"] = f"CF_{content_hash(v['text'])}"
                v["content_hash"] = content_hash(v["text"])
                v["status"] = "adapted"
                v["created_at"] = datetime.now(timezone.utc).isoformat()
                queue.append(v)
            save_queue(queue)
            print(f"  Saved {len(variants)} variants to queue")
        else:
            print("  [DRY RUN] Would save to queue")
        return

    if args.daily or args.ingest:
        print("\n[INGEST] Scanning content directories...")
        new_posts = ingest_content(niche_filter=args.niche)
        print(f"  Found {len(new_posts)} new content pieces")
        if new_posts and not args.dry_run:
            queue = load_queue()
            queue.extend(new_posts)
            save_queue(queue)
            print(f"  Added to queue (total: {len(queue)})")
        elif args.dry_run:
            print("  [DRY RUN] Would add to queue")
            for p in new_posts[:5]:
                preview = p["text"][:80].replace("\n", " ")
                print(f"    - [{p['niche']}] {preview}...")
            if len(new_posts) > 5:
                print(f"    ... and {len(new_posts) - 5} more")

    if args.daily or args.adapt:
        print("\n[ADAPT] Adapting content for platforms...")
        queue = load_queue()
        adapted = adapt_queue(queue, platform_filter=args.platform)
        print(f"  Created {len(adapted)} adapted versions")
        if adapted and not args.dry_run:
            save_queue(adapted)
            print(f"  Queue updated ({len(adapted)} entries)")
        elif args.dry_run:
            print("  [DRY RUN] Would update queue")
            for a in adapted[:5]:
                print(f"    - [{a['account']}/{a['platform']}] {a['text'][:60]}...")

    if args.daily or args.schedule:
        print("\n[SCHEDULE] Generating posting schedule...")
        queue = load_queue()
        ready = [e for e in queue if e.get("status") in ("adapted", "queued")]
        scheduled = generate_schedule(ready, days=args.days, platform_filter=args.platform)
        print(f"  Scheduled {len(scheduled)} posts over {args.days} days")
        if scheduled and not args.dry_run:
            for e in scheduled:
                e["status"] = "scheduled"
            save_queue(scheduled)
        elif args.dry_run:
            print("  [DRY RUN] Schedule preview:")
            for s in scheduled[:10]:
                print(f"    {s.get('scheduled_at', '?'):16s} | {s.get('account', '?'):15s} | {s.get('platform', '?'):10s} | {s.get('text', '')[:50]}...")

    if args.daily or args.recycle_winners:
        print("\n[RECYCLE] Checking for recyclable winners...")
        winners = find_winners_for_recycling()
        print(f"  Found {len(winners)} posts eligible for recycling (30+ days old, score >= 50)")
        recycled = []
        for w in winners:
            modified = recycle_post(w["text"])
            recycled.append({
                "text": modified,
                "niche": "tech",  # Default, would need mapping
                "source_file": "recycled_winner",
                "content_hash": content_hash(modified),
                "status": "queued",
                "variant_type": "recycled",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
        if recycled and not args.dry_run:
            queue = load_queue()
            queue.extend(recycled)
            save_queue(queue)
            print(f"  Added {len(recycled)} recycled posts to queue")
        elif args.dry_run and recycled:
            print("  [DRY RUN] Would recycle:")
            for r in recycled[:3]:
                print(f"    - {r['text'][:80]}...")

    if args.export_buffer:
        print("\n[EXPORT] Generating Buffer CSVs...")
        queue = load_queue()
        scheduled = [e for e in queue if e.get("status") == "scheduled"]
        if not scheduled:
            # Auto-schedule if nothing is scheduled yet
            ready = [e for e in queue if e.get("status") in ("adapted", "queued")]
            scheduled = generate_schedule(ready, days=args.days, platform_filter=args.platform)

        if scheduled:
            if args.dry_run:
                print(f"  [DRY RUN] Would export {len(scheduled)} posts as Buffer CSVs")
            else:
                files = export_buffer_csv(scheduled)
                print(f"  Exported {len(scheduled)} posts to {len(files)} files:")
                for f in files:
                    print(f"    - {f}")
        else:
            print("  No scheduled content to export. Run --daily first.")

    if args.daily:
        print("\n" + "=" * 60)
        print("  DAILY CYCLE COMPLETE")
        print("=" * 60)
        show_status()


if __name__ == "__main__":
    main()
