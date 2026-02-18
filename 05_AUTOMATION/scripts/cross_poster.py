#!/usr/bin/env python3
"""
cross_poster.py - Format and queue content for multiple platforms simultaneously

Takes a single piece of content and reformats it for each target platform,
respecting character limits, hashtag conventions, and formatting rules.
Writes formatted versions to the posting queue.

Usage:
    python3 cross_poster.py --content "Your post text here" --platforms X,Instagram,LinkedIn
    python3 cross_poster.py --file /path/to/content.md --platforms all
    python3 cross_poster.py --file /path/to/thread.md --thread --platforms X,TikTok

Example:
    # Cross-post a quick insight to all platforms
    python3 cross_poster.py --content "I built a cold email system that sends 200/day. 12% reply rate. Here's the stack: Instantly + Clay + Apollo." --platforms X,LinkedIn,Instagram

    # Cross-post from file to all platforms
    python3 cross_poster.py --file CONTENT/social/ai/tip_001.md --platforms all
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
POSTING_QUEUE = AUTOMATIONS_DIR / "content_posting" / "posting_queue.csv"
LOG_DIR = AUTOMATIONS_DIR / "logs"
CONFIG_PATH = AUTOMATIONS_DIR / "config.json"

LOG_DIR.mkdir(parents=True, exist_ok=True)
POSTING_QUEUE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "cross_poster.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Platform constraints
PLATFORM_LIMITS = {
    "X": {"chars": 280, "hashtags": 3, "links": 1, "images": 4},
    "Twitter": {"chars": 280, "hashtags": 3, "links": 1, "images": 4},
    "Instagram": {"chars": 2200, "hashtags": 30, "links": 0, "images": 10},
    "LinkedIn": {"chars": 3000, "hashtags": 5, "links": 3, "images": 1},
    "TikTok": {"chars": 4000, "hashtags": 5, "links": 1, "images": 0},
    "Facebook": {"chars": 63206, "hashtags": 3, "links": 3, "images": 10},
    "Pinterest": {"chars": 500, "hashtags": 20, "links": 1, "images": 1},
    "Medium": {"chars": 999999, "hashtags": 5, "links": 99, "images": 99},
    "Substack": {"chars": 999999, "hashtags": 0, "links": 99, "images": 99},
    "Threads": {"chars": 500, "hashtags": 5, "links": 1, "images": 10},
}

ALL_PLATFORMS = list(PLATFORM_LIMITS.keys())


def load_config():
    """Load config if exists."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}


def read_content_file(filepath):
    """Read content from a markdown or text file."""
    path = Path(filepath)
    if not path.is_absolute():
        path = PROJECT_DIR / filepath

    if not path.exists():
        logger.error(f"Content file not found: {path}")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Strip frontmatter if present
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    return content


def extract_hashtags(text):
    """Pull existing hashtags from text."""
    tags = re.findall(r"#\w+", text)
    clean_text = re.sub(r"\s*#\w+", "", text).strip()
    return clean_text, tags


def truncate_smart(text, max_chars):
    """Truncate text at sentence boundary if possible."""
    if len(text) <= max_chars:
        return text

    # Try to cut at sentence end
    truncated = text[: max_chars - 3]
    last_period = truncated.rfind(".")
    last_newline = truncated.rfind("\n")
    cut_point = max(last_period, last_newline)

    if cut_point > max_chars * 0.5:
        return text[: cut_point + 1]

    return truncated.rstrip() + "..."


def format_for_platform(content, platform, hashtags=None):
    """Format content for a specific platform."""
    limits = PLATFORM_LIMITS.get(platform, PLATFORM_LIMITS["X"])
    clean_content, existing_tags = extract_hashtags(content)

    all_tags = list(set((hashtags or []) + existing_tags))
    max_tags = limits["hashtags"]
    selected_tags = all_tags[:max_tags]

    if platform in ("X", "Twitter"):
        # Short, punchy. Hook first line.
        lines = clean_content.split("\n")
        formatted = lines[0] if lines else clean_content
        formatted = truncate_smart(formatted, limits["chars"] - 30)
        if selected_tags:
            tag_str = " ".join(selected_tags[:3])
            if len(formatted) + len(tag_str) + 2 <= limits["chars"]:
                formatted = f"{formatted}\n\n{tag_str}"

    elif platform == "Instagram":
        # Full content, hashtags at end separated by dots
        formatted = truncate_smart(clean_content, limits["chars"] - 200)
        if selected_tags:
            tag_str = " ".join(selected_tags)
            formatted = f"{formatted}\n\n.\n.\n.\n{tag_str}"

    elif platform == "LinkedIn":
        # Professional framing, paragraph breaks, limited hashtags
        formatted = clean_content.replace("\n\n", "\n\n")
        formatted = truncate_smart(formatted, limits["chars"] - 100)
        if selected_tags:
            tag_str = " ".join(selected_tags[:5])
            formatted = f"{formatted}\n\n{tag_str}"

    elif platform == "TikTok":
        # Caption style, short hook, hashtags inline
        lines = clean_content.split("\n")
        hook = lines[0] if lines else clean_content
        formatted = truncate_smart(hook, 150)
        if selected_tags:
            tag_str = " ".join(selected_tags[:5])
            formatted = f"{formatted} {tag_str}"

    elif platform == "Pinterest":
        # Descriptive, keyword-rich
        formatted = truncate_smart(clean_content, limits["chars"] - 100)
        if selected_tags:
            tag_str = " ".join(selected_tags[:20])
            formatted = f"{formatted}\n\n{tag_str}"

    elif platform in ("Medium", "Substack"):
        # Full article, minimal changes
        formatted = clean_content

    elif platform == "Threads":
        formatted = truncate_smart(clean_content, limits["chars"] - 50)
        if selected_tags:
            tag_str = " ".join(selected_tags[:5])
            formatted = f"{formatted}\n\n{tag_str}"

    else:
        formatted = truncate_smart(clean_content, limits.get("chars", 500))

    return formatted


def queue_posts(formatted_posts, niche="", dry_run=False):
    """Write formatted posts to posting queue."""
    if dry_run:
        for platform, content in formatted_posts.items():
            logger.info(f"\n--- {platform} ({len(content)} chars) ---")
            logger.info(content[:300])
            if len(content) > 300:
                logger.info(f"... ({len(content) - 300} more chars)")
        return

    fieldnames = [
        "scheduled_time", "platform", "account", "niche", "content_type",
        "content_path", "caption", "hashtags", "status", "source", "original_id",
    ]

    file_exists = POSTING_QUEUE.exists()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(POSTING_QUEUE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for platform, content in formatted_posts.items():
            writer.writerow({
                "scheduled_time": "",
                "platform": platform,
                "account": "",
                "niche": niche,
                "content_type": "cross_post",
                "content_path": "",
                "caption": content,
                "hashtags": "",
                "status": "PENDING_SCHEDULE",
                "source": "cross_poster",
                "original_id": f"XPOST_{timestamp}",
            })

    logger.info(f"Queued {len(formatted_posts)} platform versions")


def main():
    parser = argparse.ArgumentParser(
        description="Cross-post content to multiple platforms"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--content", type=str, help="Content text to cross-post")
    group.add_argument("--file", type=str, help="Path to content file")
    parser.add_argument(
        "--platforms",
        type=str,
        default="X,Instagram,LinkedIn",
        help="Comma-separated platforms or 'all' (default: X,Instagram,LinkedIn)",
    )
    parser.add_argument("--niche", type=str, default="", help="Content niche tag")
    parser.add_argument(
        "--hashtags",
        type=str,
        default="",
        help="Additional hashtags (comma-separated)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--thread", action="store_true", help="Treat as thread/carousel")
    args = parser.parse_args()

    if args.content:
        content = args.content
    else:
        content = read_content_file(args.file)

    if args.platforms.lower() == "all":
        platforms = ALL_PLATFORMS
    else:
        platforms = [p.strip() for p in args.platforms.split(",")]

    extra_tags = [f"#{t.strip().lstrip('#')}" for t in args.hashtags.split(",") if t.strip()]

    logger.info(f"Cross-posting to {len(platforms)} platforms: {', '.join(platforms)}")

    formatted = {}
    for platform in platforms:
        if platform not in PLATFORM_LIMITS:
            logger.warning(f"Unknown platform: {platform}, skipping")
            continue
        formatted[platform] = format_for_platform(content, platform, extra_tags)

    queue_posts(formatted, niche=args.niche, dry_run=args.dry_run)
    logger.info("Cross-posting complete")


if __name__ == "__main__":
    main()
