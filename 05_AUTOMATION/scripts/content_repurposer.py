#!/usr/bin/env python3
"""
content_repurposer.py - Transform content between formats

Converts between: Twitter thread, Medium article, Substack post, newsletter,
Gumroad listing, video script, carousel, Pinterest pin.

Implements the Zero Waste Protocol: 1 input -> 15 outputs.

Usage:
    python3 content_repurposer.py --input thread.md --output-format medium
    python3 content_repurposer.py --input article.md --output-format all
    python3 content_repurposer.py --input thread.md --output-format thread,medium,substack

Example:
    # Convert a Twitter thread to a Medium article
    python3 content_repurposer.py --input CONTENT/social/ai/thread_01.md --output-format medium

    # Generate all 15 outputs from a single piece
    python3 content_repurposer.py --input CONTENT/social/ai/thread_01.md --output-format all --niche ai
"""

import argparse
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
CONTENT_DIR = PROJECT_DIR / "CONTENT"
LOG_DIR = AUTOMATIONS_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "content_repurposer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

OUTPUT_FORMATS = [
    "thread", "medium", "substack", "newsletter", "gumroad",
    "video_script", "carousel", "pinterest", "seo_page",
    "skool", "reply_bait", "dm_funnel", "cross_niche",
    "reddit", "linkedin",
]

OUTPUT_DIRS = {
    "thread": "social",
    "medium": "medium_articles",
    "substack": "substack_posts",
    "newsletter": "newsletters",
    "gumroad": "gumroad_listings",
    "video_script": "video_scripts",
    "carousel": "carousels",
    "pinterest": "pinterest_pins",
    "seo_page": "longtail_pages",
    "skool": "skool_threads",
    "reply_bait": "social",
    "dm_funnel": "dm_funnels",
    "cross_niche": "cross_niche",
    "reddit": "reddit",
    "linkedin": "linkedin",
}


def read_input(filepath):
    """Read input content file."""
    path = Path(filepath)
    if not path.is_absolute():
        path = PROJECT_DIR / filepath

    if not path.exists():
        logger.error(f"Input file not found: {path}")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        return f.read()


def extract_key_points(content):
    """Extract main ideas from content."""
    lines = content.strip().split("\n")
    points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip frontmatter
        if line.startswith("---"):
            continue
        # Skip headers that are just formatting
        if line.startswith("#") and len(line) < 5:
            continue
        # Bullet points or numbered items
        if re.match(r"^[\-\*\d]", line):
            points.append(re.sub(r"^[\-\*\d\.\)]+\s*", "", line))
        # Regular sentences with substance
        elif len(line) > 30:
            points.append(line)

    return points[:15]  # Cap at 15 key points


def extract_hook(content):
    """Extract or generate a hook from the first line."""
    lines = [l.strip() for l in content.strip().split("\n") if l.strip() and not l.startswith("---")]
    if lines:
        hook = lines[0].lstrip("#").strip()
        return hook
    return "here's what I found"


def to_thread(content, niche=""):
    """Convert content to Twitter thread format."""
    points = extract_key_points(content)
    hook = extract_hook(content)

    tweets = [f"{hook}\n\na thread:"]
    for i, point in enumerate(points[:6], 1):
        tweet = point[:270]
        tweets.append(tweet)

    # CTA tweet
    tweets.append(
        "full breakdown on my gumroad (link in bio)\n\n"
        "reply THREAD if you want the next one on a specific topic"
    )

    return "\n\n---\n\n".join(tweets)


def to_medium(content, niche=""):
    """Convert content to Medium article format."""
    points = extract_key_points(content)
    hook = extract_hook(content)

    article = f"# {hook}\n\n"
    article += f"*{datetime.now().strftime('%B %d, %Y')}*\n\n"

    # Intro
    if len(points) > 2:
        article += f"{points[0]}\n\n"
        article += f"{points[1]}\n\n"

    # Body sections
    for i, point in enumerate(points[2:8], 1):
        article += f"## {i}. Key insight\n\n"
        article += f"{point}\n\n"

    # Conclusion
    article += "## Bottom line\n\n"
    article += "The tactics here are not theory. They are tested, measured, and repeatable.\n\n"
    article += "If you want the full breakdown with implementation steps, "
    article += "check the link in my bio.\n\n"
    article += "---\n\n"
    article += f"*Tags: {niche}, solopreneur, automation, revenue*\n"

    return article


def to_substack(content, niche=""):
    """Convert to Substack post format."""
    points = extract_key_points(content)
    hook = extract_hook(content)

    post = f"# {hook}\n\n"
    post += "Hey,\n\n"
    post += f"{points[0] if points else 'Quick breakdown today.'}\n\n"

    for point in points[1:7]:
        post += f"- {point}\n"

    post += "\n**What to do with this:**\n\n"
    post += "1. Pick one tactic from above\n"
    post += "2. Test it this week\n"
    post += "3. Reply to this email with your results\n\n"
    post += "Talk soon,\n"
    post += "PRINTMAXX\n"

    return post


def to_newsletter(content, niche=""):
    """Convert to Beehiiv newsletter format."""
    points = extract_key_points(content)
    hook = extract_hook(content)

    nl = f"Subject: {hook[:60]}\n"
    nl += f"Preview: {points[0][:90] if points else hook[:90]}\n\n"
    nl += "---\n\n"
    nl += f"# {hook}\n\n"

    for point in points[:5]:
        nl += f"**>** {point}\n\n"

    nl += "---\n\n"
    nl += "**This week's action item:** Pick one insight above and test it before Friday.\n\n"
    nl += "Reply with what you tried. I read every response.\n\n"
    nl += "-- PRINTMAXX\n"

    return nl


def to_gumroad(content, niche=""):
    """Convert to Gumroad product listing spec."""
    points = extract_key_points(content)
    hook = extract_hook(content)

    listing = f"# Product: {hook} - Full Breakdown\n\n"
    listing += "**Price:** $9\n"
    listing += "**Format:** PDF + Notion Template\n\n"
    listing += "## What's inside:\n\n"

    for i, point in enumerate(points[:8], 1):
        listing += f"{i}. {point}\n"

    listing += "\n## Who this is for:\n\n"
    listing += "- Solopreneurs who want to stop guessing\n"
    listing += "- Builders who want proven frameworks\n"
    listing += "- Anyone tired of theory without numbers\n\n"
    listing += "## What you get:\n\n"
    listing += "- Complete step-by-step breakdown (25+ pages)\n"
    listing += "- Notion template for tracking\n"
    listing += "- Swipe files and templates\n"
    listing += "- Lifetime updates\n\n"
    listing += f"**Tags:** {niche}, breakdown, playbook, solopreneur\n"

    return listing


def to_video_script(content, niche=""):
    """Convert to faceless video script (TikTok/Reels/Shorts)."""
    points = extract_key_points(content)
    hook = extract_hook(content)

    script = "# Faceless Video Script\n\n"
    script += f"**Duration:** 30-60 seconds\n"
    script += f"**Format:** Text-on-screen slideshow\n"
    script += f"**Audio:** Lo-fi or trending sound\n\n"
    script += f"## SLIDE 1 (0-5s) - HOOK\n"
    script += f'"{hook}"\n'
    script += f"[Large text, dark background, slight zoom]\n\n"

    for i, point in enumerate(points[:4], 2):
        script += f"## SLIDE {i} ({(i-1)*8}-{i*8}s)\n"
        script += f'"{point[:100]}"\n'
        script += f"[Clean text, relevant background image]\n\n"

    script += f"## SLIDE {min(len(points)+1, 7)} (Final) - CTA\n"
    script += '"Full breakdown in bio"\n'
    script += "[Arrow pointing down, gumroad link overlay]\n\n"
    script += "---\n"
    script += "**Caption:** " + hook[:100] + "\n"
    script += f"**Hashtags:** #{niche} #solopreneur #buildinpublic #automation\n"

    return script


def to_carousel(content, niche=""):
    """Convert to Instagram/LinkedIn carousel spec."""
    points = extract_key_points(content)
    hook = extract_hook(content)

    carousel = "# Carousel Spec\n\n"
    carousel += f"**Slides:** {min(len(points) + 2, 10)}\n"
    carousel += f"**Size:** 1080x1350 (portrait)\n\n"

    carousel += "## Slide 1 - Cover\n"
    carousel += f"**Headline:** {hook[:60]}\n"
    carousel += "**Subtext:** Swipe to learn\n"
    carousel += "**Style:** Bold text, gradient background\n\n"

    for i, point in enumerate(points[:7], 2):
        carousel += f"## Slide {i}\n"
        carousel += f"**Text:** {point[:120]}\n"
        carousel += "**Layout:** Large text, minimal design\n\n"

    carousel += f"## Slide {min(len(points) + 2, 10)} - CTA\n"
    carousel += "**Text:** Want the full breakdown?\n"
    carousel += "**CTA:** Link in bio | Save this post\n\n"

    return carousel


def to_pinterest(content, niche=""):
    """Convert to Pinterest pin spec."""
    hook = extract_hook(content)
    points = extract_key_points(content)

    pin = "# Pinterest Pin Spec\n\n"
    pin += f"**Title:** {hook[:100]}\n"
    pin += f"**Size:** 1000x1500 (2:3)\n"
    pin += f"**Board:** {niche} tips\n\n"
    pin += "## Pin Description:\n\n"
    pin += f"{hook}. "

    for point in points[:3]:
        pin += f"{point[:80]}. "

    pin += f"\n\n**Link:** printmaxx.com/blog/{niche}-tips\n"
    pin += f"**Keywords:** {niche}, solopreneur, money, automation, tips\n"

    return pin


def to_seo_page(content, niche=""):
    """Convert to longtail SEO page."""
    hook = extract_hook(content)
    points = extract_key_points(content)
    slug = re.sub(r"[^a-z0-9]+", "-", hook.lower())[:60].strip("-")

    page = f"---\n"
    page += f"title: {hook}\n"
    page += f"slug: {slug}\n"
    page += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
    page += f"niche: {niche}\n"
    page += f"---\n\n"
    page += f"# {hook}\n\n"
    page += f"## Quick answer\n\n"
    page += f"{points[0] if points else hook}\n\n"

    for i, point in enumerate(points[1:6], 1):
        page += f"## {point[:60]}\n\n"
        page += f"{point}\n\n"

    page += "## FAQ\n\n"
    page += f"### What is {niche} optimization?\n\n"
    page += f"A systematic approach to maximizing results in {niche}.\n\n"
    page += "## Next steps\n\n"
    page += "Pick one tactic above and implement it today.\n"

    return page


def to_reply_bait(content, niche=""):
    """Convert to reply bait post format."""
    hook = extract_hook(content)
    points = extract_key_points(content)

    post = f"{hook}\n\n"
    for point in points[:3]:
        post += f"- {point[:80]}\n"
    post += "\nreply 'BREAKDOWN' and I'll send you the full method"

    return post


def to_dm_funnel(content, niche=""):
    """Convert to DM funnel sequence."""
    hook = extract_hook(content)
    points = extract_key_points(content)

    funnel = "# DM Funnel Sequence\n\n"
    funnel += f"**Trigger keyword:** BREAKDOWN\n"
    funnel += f"**Source post:** {hook[:80]}\n\n"
    funnel += "## DM 1 (Immediate auto-reply):\n"
    funnel += f"hey, you asked about the {niche} breakdown. here it is:\n\n"
    funnel += f"[key point 1]\n[key point 2]\n[key point 3]\n\n"
    funnel += "want the full 25-page version with templates? $9 on my gumroad\n\n"
    funnel += "## DM 2 (If no response after 24h):\n"
    funnel += "quick question - did that breakdown help?\n\n"
    funnel += "## DM 3 (If they respond positively):\n"
    funnel += "glad it helped. I also do 1-on-1 implementation calls if you want it set up.\n"
    funnel += "$200/hr, most people need 1-2 hours. DM me 'CALL' if interested.\n"

    return funnel


def to_cross_niche(content, niche=""):
    """Generate cross-niche adaptations (faith/fitness/tech)."""
    hook = extract_hook(content)
    niches = ["faith", "fitness", "tech"]

    output = "# Cross-Niche Adaptations\n\n"
    for target_niche in niches:
        output += f"## {target_niche.upper()} Version\n\n"
        adapted = hook.replace("solopreneur", f"{target_niche} creator")
        output += f"**Hook:** {adapted}\n\n"
        output += f"**Angle:** Apply this to {target_niche} audience specifically\n"
        output += f"**Account:** @{target_niche}_account\n\n"

    return output


def to_reddit(content, niche=""):
    """Convert to Reddit post format."""
    hook = extract_hook(content)
    points = extract_key_points(content)

    post = f"# {hook}\n\n"
    post += "I've been testing this for the past few weeks and here's what I found:\n\n"
    for point in points[:6]:
        post += f"- {point}\n"
    post += "\nHappy to answer questions in the comments.\n"
    post += f"\n**Subreddits:** r/SideProject, r/EntrepreneurRideAlong, r/{niche}\n"

    return post


def to_linkedin(content, niche=""):
    """Convert to LinkedIn post format."""
    hook = extract_hook(content)
    points = extract_key_points(content)

    post = f"{hook}\n\n"
    for point in points[:5]:
        post += f"{point}\n\n"
    post += "Agree? What would you add?\n\n"
    post += f"#{niche} #solopreneur #buildinpublic"

    return post


FORMAT_FUNCS = {
    "thread": to_thread,
    "medium": to_medium,
    "substack": to_substack,
    "newsletter": to_newsletter,
    "gumroad": to_gumroad,
    "video_script": to_video_script,
    "carousel": to_carousel,
    "pinterest": to_pinterest,
    "seo_page": to_seo_page,
    "skool": to_reddit,  # Similar format
    "reply_bait": to_reply_bait,
    "dm_funnel": to_dm_funnel,
    "cross_niche": to_cross_niche,
    "reddit": to_reddit,
    "linkedin": to_linkedin,
}


def main():
    parser = argparse.ArgumentParser(
        description="Repurpose content across formats (Zero Waste Protocol)"
    )
    parser.add_argument("--input", required=True, help="Input content file path")
    parser.add_argument(
        "--output-format",
        required=True,
        help="Output format(s): comma-separated or 'all'",
    )
    parser.add_argument("--niche", default="", help="Content niche")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: CONTENT/<format>/)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    content = read_input(args.input)

    if args.output_format.lower() == "all":
        formats = OUTPUT_FORMATS
    else:
        formats = [f.strip() for f in args.output_format.split(",")]

    logger.info(f"Repurposing to {len(formats)} formats")
    input_name = Path(args.input).stem
    timestamp = datetime.now().strftime("%Y%m%d")

    for fmt in formats:
        if fmt not in FORMAT_FUNCS:
            logger.warning(f"Unknown format: {fmt}, skipping")
            continue

        result = FORMAT_FUNCS[fmt](content, niche=args.niche)

        if args.dry_run:
            logger.info(f"\n=== {fmt.upper()} ({len(result)} chars) ===")
            logger.info(result[:500])
            if len(result) > 500:
                logger.info(f"... ({len(result) - 500} more chars)")
            continue

        # Write to appropriate directory
        out_subdir = OUTPUT_DIRS.get(fmt, fmt)
        out_dir = Path(args.output_dir) if args.output_dir else CONTENT_DIR / out_subdir
        out_dir.mkdir(parents=True, exist_ok=True)

        out_file = out_dir / f"{input_name}_{fmt}_{timestamp}.md"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(result)

        logger.info(f"Wrote {fmt}: {out_file} ({len(result)} chars)")

    logger.info(f"Repurposing complete: {len(formats)} formats generated")


if __name__ == "__main__":
    main()
