#!/usr/bin/env python3
"""
PRINTMAXX Content Posting Scheduler
====================================
Reads generated content from CONTENT_FARM/NICHE_ACCOUNTS and content_generation/posts,
formats for each platform, and outputs ready-to-post files with a posting queue CSV.

Usage:
    python3 post_scheduler.py                    # Process all content
    python3 post_scheduler.py --niche faith      # Process only faith niche
    python3 post_scheduler.py --platform x       # Format only for X/Twitter
    python3 post_scheduler.py --days 7           # Schedule for next 7 days
"""

import csv
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT_POSTS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "content_generation" / "posts"
NICHE_ACCOUNTS_DIR = PROJECT_ROOT / "MONEY_METHODS" / "CONTENT_FARM" / "NICHE_ACCOUNTS"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
QUEUE_CSV = Path(__file__).resolve().parent / "posting_queue.csv"

# Platform character limits
PLATFORM_LIMITS = {
    "x": 280,
    "x_thread": 280,  # per tweet in thread
    "tiktok": 2200,
    "instagram": 2200,
    "linkedin": 3000,
    "youtube_shorts": 100,  # title only
    "threads": 500,
    "bluesky": 300,
}

# Posting schedule: niche -> {platform -> [times in EST]}
POSTING_SCHEDULE = {
    "faith": {
        "x": ["06:30", "12:00", "19:30"],
        "instagram": ["07:00", "18:00"],
        "tiktok": ["06:30", "11:00", "19:00"],
    },
    "fitness": {
        "x": ["05:30", "12:00", "18:00"],
        "instagram": ["06:00", "17:30"],
        "tiktok": ["05:30", "12:00", "17:00"],
    },
    "ai": {
        "x": ["08:00", "12:30", "17:00"],
        "instagram": ["09:00", "17:00"],
        "tiktok": ["08:00", "12:00", "18:00"],
    },
}

# Niche to account mapping
NICHE_ACCOUNTS = {
    "faith": "@DailyGraceQuotes",
    "fitness": "@5AMGainsClub",
    "ai": "@TheStackReport",
}


def log(msg: str) -> None:
    """Print timestamped log message."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def read_content_file(filepath: Path) -> dict:
    """Parse a content markdown file into structured data."""
    content = filepath.read_text(encoding="utf-8")
    result = {
        "filepath": str(filepath),
        "raw_content": content,
        "platform": "",
        "niche": "",
        "hook": "",
        "body": "",
        "cta": "",
        "hashtags": [],
        "media_notes": "",
    }

    # Detect platform from path
    path_str = str(filepath).lower()
    if "tiktok" in path_str:
        result["platform"] = "tiktok"
    elif "instagram" in path_str or "ig" in path_str:
        result["platform"] = "instagram"
    elif "x" in path_str or "twitter" in path_str:
        result["platform"] = "x"
    elif "linkedin" in path_str:
        result["platform"] = "linkedin"
    elif "youtube" in path_str:
        result["platform"] = "youtube_shorts"

    # Detect niche from path
    for niche in ["faith", "fitness", "ai"]:
        if niche in path_str:
            result["niche"] = niche
            break

    # Extract sections from markdown
    # Look for hook/problem section
    hook_match = re.search(
        r"##\s*(?:Video Hook|Hook).*?\n\n(.*?)(?=\n##|\Z)", content, re.DOTALL
    )
    if hook_match:
        result["hook"] = hook_match.group(1).strip()

    # Look for body/solution
    body_parts = []
    for section in ["Problem", "Solution", "Result", "Body", "Main", "Content"]:
        section_match = re.search(
            rf"##\s*{section}.*?\n\n(.*?)(?=\n##|\Z)", content, re.DOTALL
        )
        if section_match:
            body_parts.append(section_match.group(1).strip())
    result["body"] = "\n\n".join(body_parts)

    # Look for CTA section
    cta_match = re.search(
        r"##\s*(?:CTA|Call to Action).*?\n\n(.*?)(?=\n##|\Z)", content, re.DOTALL
    )
    if cta_match:
        result["cta"] = cta_match.group(1).strip()

    # Extract hashtags
    hashtags = re.findall(r"#\w+", content)
    result["hashtags"] = list(set(hashtags))

    # Extract media notes
    media_match = re.search(
        r"\*\*(?:Visual|Media|Video).*?:\*\*\s*(.*?)(?:\n|$)", content
    )
    if media_match:
        result["media_notes"] = media_match.group(1).strip()

    # If no structured sections found, use raw text minus frontmatter
    if not result["hook"] and not result["body"]:
        # Try to extract from code blocks (content templates use ```)
        code_blocks = re.findall(r"```\n(.*?)```", content, re.DOTALL)
        if code_blocks:
            result["body"] = code_blocks[0].strip()
        else:
            # Strip markdown headers and use remaining text
            clean = re.sub(r"^#.*$", "", content, flags=re.MULTILINE)
            clean = re.sub(r"\*\*.*?\*\*", "", clean)
            result["body"] = clean.strip()[:500]

    return result


def format_for_x(content: dict) -> str:
    """Format content for X/Twitter (280 char limit)."""
    parts = []
    if content["hook"]:
        parts.append(content["hook"])
    if content["body"]:
        # Take first sentence or paragraph
        first = content["body"].split("\n\n")[0]
        parts.append(first)
    if content["cta"]:
        parts.append(content["cta"])

    text = "\n\n".join(parts)

    # Truncate to character limit, preserving word boundaries
    if len(text) > PLATFORM_LIMITS["x"]:
        text = text[: PLATFORM_LIMITS["x"] - 3]
        last_space = text.rfind(" ")
        if last_space > 200:
            text = text[:last_space]
        text += "..."

    return text


def format_for_tiktok(content: dict) -> str:
    """Format content for TikTok caption."""
    parts = []
    if content["hook"]:
        parts.append(content["hook"])
    if content["body"]:
        parts.append(content["body"][:500])
    if content["cta"]:
        parts.append(content["cta"])

    # Add hashtags
    if content["hashtags"]:
        parts.append(" ".join(content["hashtags"][:5]))

    text = "\n\n".join(parts)
    if len(text) > PLATFORM_LIMITS["tiktok"]:
        text = text[: PLATFORM_LIMITS["tiktok"] - 3] + "..."

    return text


def format_for_instagram(content: dict) -> str:
    """Format content for Instagram caption."""
    parts = []
    if content["hook"]:
        parts.append(content["hook"])
    if content["body"]:
        parts.append(content["body"])
    if content["cta"]:
        parts.append(content["cta"])

    text = "\n\n".join(parts)

    # Add hashtags at end (Instagram convention)
    if content["hashtags"]:
        text += "\n\n.\n.\n.\n" + " ".join(content["hashtags"][:30])

    if len(text) > PLATFORM_LIMITS["instagram"]:
        text = text[: PLATFORM_LIMITS["instagram"] - 3] + "..."

    return text


def format_for_linkedin(content: dict) -> str:
    """Format content for LinkedIn."""
    parts = []
    if content["hook"]:
        parts.append(content["hook"])
    if content["body"]:
        parts.append(content["body"])
    if content["cta"]:
        parts.append(content["cta"])

    text = "\n\n".join(parts)
    if len(text) > PLATFORM_LIMITS["linkedin"]:
        text = text[: PLATFORM_LIMITS["linkedin"] - 3] + "..."

    return text


FORMATTERS = {
    "x": format_for_x,
    "tiktok": format_for_tiktok,
    "instagram": format_for_instagram,
    "linkedin": format_for_linkedin,
}


def scan_content_files(
    niche_filter: Optional[str] = None, platform_filter: Optional[str] = None
) -> list:
    """Scan all content directories for posts."""
    content_files = []

    # Scan generated posts directory
    if CONTENT_POSTS_DIR.exists():
        for md_file in CONTENT_POSTS_DIR.rglob("*.md"):
            # Skip README and meta files
            if md_file.name.startswith(("README", "DELIVERY", "GENERATION", "SAMPLE", "SOCIAL", "FINAL")):
                continue
            parsed = read_content_file(md_file)
            if niche_filter and parsed["niche"] != niche_filter:
                continue
            if platform_filter and parsed["platform"] != platform_filter:
                continue
            content_files.append(parsed)

    # Scan niche account templates
    if NICHE_ACCOUNTS_DIR.exists():
        templates_file = NICHE_ACCOUNTS_DIR / "CONTENT_TEMPLATES_90.md"
        if templates_file.exists():
            templates = parse_content_templates(templates_file)
            for t in templates:
                if niche_filter and t["niche"] != niche_filter:
                    continue
                content_files.append(t)

    log(f"Found {len(content_files)} content files")
    return content_files


def parse_content_templates(filepath: Path) -> list:
    """Parse the CONTENT_TEMPLATES_90.md into individual content items."""
    content = filepath.read_text(encoding="utf-8")
    templates = []

    # Split by ### headers (individual templates)
    sections = re.split(r"###\s+(A|B|C)\d+\s+-\s+", content)

    current_niche = "faith"  # Default, update based on section headers
    niche_map = {
        "SECTION A": "faith",
        "SECTION B": "fitness",
        "SECTION C": "ai",
    }

    # Detect section changes
    for key, niche in niche_map.items():
        if key in content:
            pass  # Niches are interleaved

    # Parse code blocks as individual templates
    blocks = re.findall(
        r"###\s+([ABC]\d+)\s+-\s+(.*?)\n.*?```\n(.*?)```",
        content,
        re.DOTALL,
    )

    for template_id, title, body in blocks:
        niche = "faith"
        if template_id.startswith("B"):
            niche = "fitness"
        elif template_id.startswith("C"):
            niche = "ai"

        templates.append({
            "filepath": str(filepath),
            "raw_content": body.strip(),
            "platform": "x",  # Templates are multi-platform
            "niche": niche,
            "hook": body.strip().split("\n")[0] if body.strip() else "",
            "body": body.strip(),
            "cta": "",
            "hashtags": re.findall(r"#\w+", body),
            "media_notes": "",
            "template_id": template_id,
            "template_title": title.strip(),
        })

    return templates


def generate_posting_schedule(
    content_files: list, days: int = 7, start_date: Optional[datetime] = None
) -> list:
    """Generate a posting schedule from content files."""
    if start_date is None:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date += timedelta(days=1)  # Start tomorrow

    queue = []
    content_idx = {}  # Track per niche-platform index

    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")

        for niche, platforms in POSTING_SCHEDULE.items():
            for platform, times in platforms.items():
                for time_str in times:
                    key = f"{niche}_{platform}"
                    if key not in content_idx:
                        content_idx[key] = 0

                    # Find matching content
                    matching = [
                        c for c in content_files
                        if c["niche"] == niche
                        and (c["platform"] == platform or c["platform"] == "x")
                    ]

                    if not matching:
                        continue

                    idx = content_idx[key] % len(matching)
                    content = matching[idx]
                    content_idx[key] += 1

                    # Format for platform
                    formatter = FORMATTERS.get(platform, format_for_x)
                    formatted_text = formatter(content)

                    account = NICHE_ACCOUNTS.get(niche, f"@{niche}_account")

                    queue.append({
                        "date": date_str,
                        "time": time_str,
                        "platform": platform,
                        "account": account,
                        "niche": niche,
                        "content": formatted_text,
                        "media_path": content.get("media_notes", ""),
                        "source_file": content["filepath"],
                        "char_count": len(formatted_text),
                        "status": "QUEUED",
                    })

    log(f"Generated {len(queue)} scheduled posts over {days} days")
    return queue


def write_posting_queue(queue: list, output_path: Path) -> None:
    """Write posting queue to CSV."""
    fieldnames = [
        "date", "time", "platform", "account", "niche",
        "content", "media_path", "source_file", "char_count", "status",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(queue)

    log(f"Queue written to {output_path} ({len(queue)} entries)")


def write_platform_files(queue: list, output_dir: Path) -> None:
    """Write ready-to-post files organized by platform and date."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for entry in queue:
        platform_dir = output_dir / entry["platform"] / entry["niche"]
        platform_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{entry['date']}_{entry['time'].replace(':', '')}_{entry['account'].replace('@', '')}.txt"
        filepath = platform_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Platform: {entry['platform']}\n")
            f.write(f"# Account: {entry['account']}\n")
            f.write(f"# Date: {entry['date']} {entry['time']} EST\n")
            f.write(f"# Characters: {entry['char_count']}\n")
            f.write(f"# Media: {entry['media_path']}\n")
            f.write(f"---\n\n")
            f.write(entry["content"])

    log(f"Platform files written to {output_dir}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="PRINTMAXX Content Posting Scheduler")
    parser.add_argument("--niche", choices=["faith", "fitness", "ai"], help="Filter by niche")
    parser.add_argument("--platform", choices=list(PLATFORM_LIMITS.keys()), help="Filter by platform")
    parser.add_argument("--days", type=int, default=7, help="Number of days to schedule (default: 7)")
    parser.add_argument("--output", type=str, default=None, help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Print stats without writing files")
    args = parser.parse_args()

    log("PRINTMAXX Content Posting Scheduler starting")
    log(f"Config: niche={args.niche}, platform={args.platform}, days={args.days}")

    # Scan content
    content_files = scan_content_files(
        niche_filter=args.niche,
        platform_filter=args.platform,
    )

    if not content_files:
        log("No content files found. Check paths and filters.")
        sys.exit(1)

    # Print content stats
    niche_counts = {}
    platform_counts = {}
    for c in content_files:
        niche_counts[c["niche"]] = niche_counts.get(c["niche"], 0) + 1
        platform_counts[c["platform"]] = platform_counts.get(c["platform"], 0) + 1

    log(f"Content by niche: {niche_counts}")
    log(f"Content by platform: {platform_counts}")

    if args.dry_run:
        log("Dry run. No files written.")
        return

    # Generate schedule
    queue = generate_posting_schedule(content_files, days=args.days)

    # Write outputs
    output_dir = Path(args.output) if args.output else OUTPUT_DIR
    write_posting_queue(queue, QUEUE_CSV)
    write_platform_files(queue, output_dir)

    # Summary
    log("--- SUMMARY ---")
    log(f"Total posts scheduled: {len(queue)}")
    log(f"Queue CSV: {QUEUE_CSV}")
    log(f"Platform files: {output_dir}")

    # Per-platform breakdown
    platform_summary = {}
    for entry in queue:
        key = f"{entry['platform']}_{entry['niche']}"
        platform_summary[key] = platform_summary.get(key, 0) + 1

    for key, count in sorted(platform_summary.items()):
        log(f"  {key}: {count} posts")

    log("Done.")


if __name__ == "__main__":
    main()
