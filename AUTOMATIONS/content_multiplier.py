#!/usr/bin/env python3

from __future__ import annotations
"""
Content Multiplier Engine - 1 Piece to 20+ Variants
Source: ALPHA271 - "1-to-20 repurposing hub-and-spoke model with AI automation"
Also: Zero Waste Protocol alignment

Takes a single piece of content (blog post, thread, research) and generates:
1. 5 Twitter/X posts (hook + value)
2. 3 LinkedIn posts (professional angle)
3. 1 Thread (5-7 tweets)
4. 1 Newsletter intro
5. 3 Instagram captions
6. 2 Reddit posts (GEO-optimized)
7. 1 Medium article intro
8. 1 Substack note
9. 3 TikTok/Reels script hooks (15-30 sec)

Usage:
    python3 content_multiplier.py --input "Your content here"
    python3 content_multiplier.py --file /path/to/content.md
    python3 content_multiplier.py --file /path/to/content.md --output-dir /path/to/output
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "AUTOMATIONS" / "content_posting" / "multiplied"
BUFFER_DIR = BASE_DIR / "AUTOMATIONS" / "content_posting"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "content_multiplier.log"

# Platform character limits
LIMITS = {
    "twitter": 280,
    "linkedin": 3000,
    "instagram": 2200,
    "reddit_title": 300,
    "reddit_body": 40000,
    "tiktok": 2200,
    "medium": 100000,
    "substack": 100000,
    "newsletter": 5000,
}

# PRINTMAXXER voice patterns from copy-style.md
HOOKS = {
    "consequence_first": [
        "I {action}. {result}. here's how.",
        "{number} {things} in {time}. {method}.",
        "stop {bad_thing}. just {good_thing}.",
        "{tool} changed everything. {specific_result}.",
        "I tested {thing}. {number} {metric}. the {insight}.",
    ],
    "self_reply_funnel": [
        "the thread nobody asked for but everyone needs.",
        "i've been doing this for {time}. here's what actually works.",
        "this is the exact system. no fluff.",
        "bookmark this. you'll need it.",
        "replying with the full breakdown.",
    ],
    "engagement_bait": [
        "unpopular opinion: {claim}.",
        "nobody talks about this but {insight}.",
        "{number}% of people don't know {thing}.",
        "the real reason {thing} works: {reason}.",
        "I wasted {time} before learning {lesson}.",
    ],
}


def extract_key_points(content):
    """Extract key points, numbers, and insights from content."""
    points = []
    numbers = re.findall(r'\$[\d,]+(?:\.\d+)?(?:/mo|/yr|/month|/year)?|\d+(?:\.\d+)?%|\d+[kKmM]+|\d+x', content)
    sentences = re.split(r'[.!?]\s+', content)

    # Find sentences with numbers (highest signal)
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        has_number = any(n in s for n in numbers) or bool(re.search(r'\d', s))
        if has_number and len(s) > 20:
            points.append({"text": s, "has_number": True, "priority": "high"})
        elif len(s) > 30 and len(s) < 200:
            points.append({"text": s, "has_number": False, "priority": "medium"})

    return points, numbers


def generate_twitter_posts(content, key_points, numbers):
    """Generate 5 Twitter/X posts from content."""
    posts = []

    # Post 1: Consequence-first hook with biggest number
    biggest_number = numbers[0] if numbers else "this"
    top_point = key_points[0]["text"] if key_points else content[:200]
    post1 = f"{top_point[:240]}"
    if len(post1) > 280:
        post1 = post1[:277] + "..."
    posts.append({"platform": "twitter", "type": "consequence_first", "content": post1.lower()})

    # Post 2: "stop X. just Y." format
    if len(key_points) > 1:
        post2 = f"stop overthinking this.\n\njust {key_points[1]['text'][:200].lower()}."
        posts.append({"platform": "twitter", "type": "action_directive", "content": post2[:280]})

    # Post 3: Number-heavy post
    number_points = [p for p in key_points if p["has_number"]]
    if number_points:
        post3_lines = [p["text"][:80].lower() for p in number_points[:4]]
        post3 = "\n".join(post3_lines)
        posts.append({"platform": "twitter", "type": "number_stack", "content": post3[:280]})

    # Post 4: Engagement question
    post4 = f"what's your take on this:\n\n{key_points[0]['text'][:200].lower() if key_points else content[:200].lower()}\n\nworking on this. curious what you'd change."
    posts.append({"platform": "twitter", "type": "engagement_question", "content": post4[:280]})

    # Post 5: Self-reply CTA
    post5 = f"been testing this for a while now.\n\n{key_points[-1]['text'][:180].lower() if key_points else content[:180].lower()}\n\nfull breakdown in the reply."
    posts.append({"platform": "twitter", "type": "self_reply_hook", "content": post5[:280]})

    return posts


def generate_thread(content, key_points, numbers):
    """Generate a 5-7 tweet thread."""
    tweets = []

    # Tweet 1: Hook
    hook = f"i spent the last few weeks on this.\n\nhere's exactly what i found:\n\n(thread)"
    tweets.append(hook)

    # Tweets 2-5: Key points
    for i, point in enumerate(key_points[:4]):
        tweet = f"{i+2}/ {point['text'][:250].lower()}"
        tweets.append(tweet)

    # Tweet 6: Summary
    summary = f"{len(key_points[:4])+2}/ summary:\n\n"
    for p in key_points[:3]:
        summary += f"- {p['text'][:60].lower()}\n"
    tweets.append(summary[:280])

    # Tweet 7: CTA
    cta = f"{len(key_points[:4])+3}/ if this was useful, follow @PRINTMAXXER for more breakdowns like this.\n\nworking on a full guide. drop a reply if you want it."
    tweets.append(cta)

    return tweets


def generate_linkedin_posts(content, key_points, numbers):
    """Generate 3 LinkedIn posts (professional angle)."""
    posts = []

    # LinkedIn 1: Insight + personal take
    li1 = f"Something most people miss:\n\n{key_points[0]['text'] if key_points else content[:500]}\n\n"
    if len(key_points) > 2:
        li1 += "Here's what that means in practice:\n\n"
        for p in key_points[1:4]:
            li1 += f"- {p['text'][:100]}\n"
    li1 += "\nThe takeaway: execution speed matters more than perfect strategy.\n\nAgree or disagree?"
    posts.append({"platform": "linkedin", "type": "insight", "content": li1[:3000]})

    # LinkedIn 2: Framework post
    li2 = "Framework I've been using:\n\n"
    for i, p in enumerate(key_points[:5]):
        li2 += f"Step {i+1}: {p['text'][:80]}\n"
    li2 += "\nSimple but effective. The compound effect is real."
    posts.append({"platform": "linkedin", "type": "framework", "content": li2[:3000]})

    # LinkedIn 3: Contrarian take
    li3 = f"Unpopular take:\n\n{key_points[0]['text'] if key_points else content[:300]}\n\n"
    li3 += "Most people overthink this. The ones winning are just shipping faster.\n\n"
    li3 += "What's your approach?"
    posts.append({"platform": "linkedin", "type": "contrarian", "content": li3[:3000]})

    return posts


def generate_instagram_captions(content, key_points, numbers):
    """Generate 3 Instagram captions."""
    captions = []

    for i, point in enumerate(key_points[:3]):
        caption = f"{point['text'][:150]}\n\n"
        caption += "Save this for later.\n\n"
        caption += "#buildinpublic #solopreneur #indiehacker #automation #printmaxxer"
        captions.append({"platform": "instagram", "type": "carousel_caption", "content": caption[:2200]})

    return captions


def generate_reddit_posts(content, key_points, numbers):
    """Generate 2 GEO-optimized Reddit posts."""
    posts = []

    # Reddit 1: Value post for r/SideProject or r/indiehackers
    title1 = f"Here's what I learned: {key_points[0]['text'][:200] if key_points else content[:200]}"
    body1 = f"Been working on this for a while. Wanted to share some findings.\n\n"
    for p in key_points[:6]:
        body1 += f"**{p['text'][:100]}**\n\n"
    body1 += "Happy to answer questions. Still figuring some of this out myself."
    posts.append({"platform": "reddit", "type": "value_post", "title": title1[:300], "body": body1[:5000], "subreddit": "r/SideProject"})

    # Reddit 2: Discussion post
    title2 = f"Discussion: {key_points[1]['text'][:200] if len(key_points) > 1 else content[:200]}"
    body2 = f"Curious what others think about this.\n\n"
    body2 += f"{content[:1000]}\n\n"
    body2 += "What's your experience been?"
    posts.append({"platform": "reddit", "type": "discussion", "title": title2[:300], "body": body2[:5000], "subreddit": "r/Entrepreneur"})

    return posts


def generate_tiktok_scripts(content, key_points, numbers):
    """Generate 3 TikTok/Reels scripts (15-30 sec)."""
    scripts = []

    for i, point in enumerate(key_points[:3]):
        script = f"""HOOK (0-3s): "{point['text'][:50].lower()}..."
BODY (3-20s): Break down the key insight. Show screen recording or text overlay with the numbers.
CTA (20-30s): "Follow for more breakdowns like this. Link in bio."
TEXT OVERLAY: {point['text'][:80]}
TRENDING AUDIO: Use trending sound in first 5 seconds"""
        scripts.append({"platform": "tiktok", "type": "short_form", "content": script})

    return scripts


def generate_newsletter_intro(content, key_points, numbers):
    """Generate newsletter intro paragraph."""
    intro = f"This week I dug into something interesting.\n\n"
    intro += f"{key_points[0]['text'] if key_points else content[:300]}\n\n"
    intro += "Here's what you need to know:\n\n"
    for p in key_points[:5]:
        intro += f"- {p['text'][:100]}\n"
    intro += "\nLet me break this down."
    return {"platform": "newsletter", "type": "intro", "content": intro[:5000]}


def generate_medium_intro(content, key_points, numbers):
    """Generate Medium article intro."""
    intro = f"# {key_points[0]['text'][:80] if key_points else 'What I Learned'}\n\n"
    intro += f"{content[:500]}\n\n"
    intro += "In this article, I'll break down exactly what works and what doesn't.\n\n"
    intro += "---\n\n"
    for p in key_points[:3]:
        intro += f"## {p['text'][:60]}\n\n"
        intro += f"{p['text']}\n\n"
    return {"platform": "medium", "type": "article_draft", "content": intro[:10000]}


def generate_substack_note(content, key_points, numbers):
    """Generate Substack note."""
    note = f"{key_points[0]['text'][:200] if key_points else content[:200]}\n\n"
    note += "Full breakdown in my next post. Subscribe to not miss it."
    return {"platform": "substack", "type": "note", "content": note[:500]}


def write_buffer_csv(posts, output_dir):
    """Write posts to Buffer-compatible CSV format."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Group by platform
    by_platform = {}
    for post in posts:
        platform = post.get("platform", "unknown")
        if platform not in by_platform:
            by_platform[platform] = []
        by_platform[platform].append(post)

    files_written = []

    for platform, platform_posts in by_platform.items():
        filename = output_dir / f"{platform}_multiplied_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if platform == "reddit":
                writer.writerow(["title", "body", "subreddit", "type"])
                for p in platform_posts:
                    writer.writerow([p.get("title", ""), p.get("body", ""), p.get("subreddit", ""), p.get("type", "")])
            elif platform == "tiktok":
                writer.writerow(["script", "type"])
                for p in platform_posts:
                    writer.writerow([p.get("content", ""), p.get("type", "")])
            else:
                writer.writerow(["content", "type"])
                for p in platform_posts:
                    writer.writerow([p.get("content", ""), p.get("type", "")])
        files_written.append(str(filename))

    # Also write a thread file
    return files_written


def multiply_content(content, output_dir=None):
    """Main function: take content, output 20+ variants."""
    if output_dir is None:
        output_dir = OUTPUT_DIR

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print("CONTENT MULTIPLIER - 1 piece to 20+ variants")
    print(f"{'='*60}")
    print(f"Input length: {len(content)} chars")

    # Extract key points
    key_points, numbers = extract_key_points(content)
    print(f"Key points found: {len(key_points)}")
    print(f"Numbers found: {len(numbers)}")

    if not key_points:
        # Fallback: split content into chunks
        sentences = [s.strip() for s in re.split(r'[.!?]\s+', content) if len(s.strip()) > 20]
        key_points = [{"text": s, "has_number": False, "priority": "medium"} for s in sentences[:10]]

    all_posts = []

    # Generate for each platform
    print("\nGenerating...")

    twitter_posts = generate_twitter_posts(content, key_points, numbers)
    print(f"  Twitter posts: {len(twitter_posts)}")
    all_posts.extend(twitter_posts)

    thread = generate_thread(content, key_points, numbers)
    print(f"  Thread tweets: {len(thread)}")
    for t in thread:
        all_posts.append({"platform": "twitter", "type": "thread", "content": t})

    linkedin_posts = generate_linkedin_posts(content, key_points, numbers)
    print(f"  LinkedIn posts: {len(linkedin_posts)}")
    all_posts.extend(linkedin_posts)

    ig_captions = generate_instagram_captions(content, key_points, numbers)
    print(f"  Instagram captions: {len(ig_captions)}")
    all_posts.extend(ig_captions)

    reddit_posts = generate_reddit_posts(content, key_points, numbers)
    print(f"  Reddit posts: {len(reddit_posts)}")
    all_posts.extend(reddit_posts)

    tiktok_scripts = generate_tiktok_scripts(content, key_points, numbers)
    print(f"  TikTok scripts: {len(tiktok_scripts)}")
    all_posts.extend(tiktok_scripts)

    newsletter = generate_newsletter_intro(content, key_points, numbers)
    print(f"  Newsletter intro: 1")
    all_posts.append(newsletter)

    medium = generate_medium_intro(content, key_points, numbers)
    print(f"  Medium draft: 1")
    all_posts.append(medium)

    substack = generate_substack_note(content, key_points, numbers)
    print(f"  Substack note: 1")
    all_posts.append(substack)

    total = len(all_posts)
    print(f"\nTOTAL VARIANTS: {total}")

    # Write to CSVs
    files = write_buffer_csv(all_posts, output_dir)
    print(f"\nFiles written:")
    for f in files:
        print(f"  {f}")

    # Write full JSON output
    json_file = output_dir / f"all_variants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, indent=2, ensure_ascii=False)
    print(f"  {json_file}")

    # Log
    os.makedirs(LOG_FILE.parent, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} | Input: {len(content)} chars | Output: {total} variants | Files: {len(files)}\n")

    print(f"\n{'='*60}")
    print(f"DONE. {total} content pieces generated from 1 input.")
    print(f"{'='*60}\n")

    return all_posts


def main():
    parser = argparse.ArgumentParser(description="Content Multiplier - 1 piece to 20+ variants")
    parser.add_argument("--input", "-i", type=str, help="Content text to multiply")
    parser.add_argument("--file", "-f", type=str, help="Path to content file (.md, .txt)")
    parser.add_argument("--output-dir", "-o", type=str, help="Output directory")
    args = parser.parse_args()

    content = None

    if args.input:
        content = args.input
    elif args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"ERROR: File not found: {filepath}")
            sys.exit(1)
        content = filepath.read_text(encoding='utf-8')
    else:
        # Demo mode with sample content
        content = """I monitor 200+ competitor pricing pages. they update something, I know in 30 seconds.
visualping.io sends alerts the second anything changes. it's borderline illegal how much intel this gives you.
Cold email with intent signals gets 2-4x reply rate vs spray and pray.
58% of all replies come from the first email. Stop writing 8-email sequences. Focus on email #1.
Plain text emails from a real name outperform HTML branded templates every time.
First name tokens are now spam flags. Use business context instead.
4-6 lines is the sweet spot for cold email length.
TikTok completion rate threshold increased in 2026. First hour determines distribution.
YouTube Shorts 50-60 seconds is the sweet spot. 18-22 per month is optimal.
Instagram DM shares are now the priority metric. First 2 seconds critical.
1-to-20 content repurposing: one piece of research becomes 20 social posts, 3 articles, and a product."""
        print("Running in DEMO mode with sample content...")

    output_dir = args.output_dir if args.output_dir else None
    multiply_content(content, output_dir)


if __name__ == "__main__":
    main()
