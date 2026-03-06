#!/usr/bin/env python3
"""
PRINTMAXX Reddit Poster - reads pre-written posts, previews, generates, tracks.

Usage:
    python3 AUTOMATIONS/reddit_poster.py --preview          # show what would be posted
    python3 AUTOMATIONS/reddit_poster.py --generate         # create ready-to-post markdown files
    python3 AUTOMATIONS/reddit_poster.py --status           # show posting history from log
    python3 AUTOMATIONS/reddit_poster.py --subreddit SaaS   # filter by subreddit
    python3 AUTOMATIONS/reddit_poster.py --list             # list all post files

Does NOT actually post to Reddit. Prepares content files only.
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime, date
from pathlib import Path

# --- project root + guardrails ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"
CONTENT = PROJECT_ROOT / "CONTENT"
POSTS_DIR = CONTENT / "social" / "printmaxxer" / "REDDIT_POSTS"
GENERATED_DIR = POSTS_DIR / "generated"
LOG_DIR = AUTOMATIONS / "logs"
LOG_FILE = LOG_DIR / "reddit_poster.log"
HISTORY_FILE = POSTS_DIR / "posting_history.json"

# subreddit configs: rules summary + recommended approach
SUBREDDIT_CONFIGS = {
    "SideProject": {
        "rules": "show what you built, be transparent about being the creator",
        "approach": "honest launch post, show the build process, ask for feedback",
        "flair_options": ["Show & Tell", "Looking for feedback"],
        "self_promo_ok": True,
        "min_words": 150,
    },
    "indiehackers": {
        "rules": "share real numbers, be honest about struggles, value-first",
        "approach": "revenue/journey posts with specific numbers, lessons learned",
        "flair_options": [],
        "self_promo_ok": True,
        "min_words": 200,
    },
    "webdev": {
        "rules": "no self-promo, technical discussion only, no 'I built this' spam",
        "approach": "pure technical value. discuss the approach, link repo not product",
        "flair_options": ["Discussion", "Showoff Saturday"],
        "self_promo_ok": False,
        "min_words": 200,
    },
    "Entrepreneur": {
        "rules": "no blogspam, value-first, no affiliate links",
        "approach": "lessons learned format, specific numbers, actionable takeaways",
        "flair_options": [],
        "self_promo_ok": False,
        "min_words": 200,
    },
    "smallbusiness": {
        "rules": "no self-promo, community-first, help others",
        "approach": "share experience helping others, no product links",
        "flair_options": [],
        "self_promo_ok": False,
        "min_words": 150,
    },
    "startups": {
        "rules": "no launch posts outside designated threads, value-first",
        "approach": "strategic insights, fundraising lessons, growth experiments",
        "flair_options": [],
        "self_promo_ok": False,
        "min_words": 200,
    },
    "SaaS": {
        "rules": "tool reviews welcome, no pure ads, share real experience",
        "approach": "honest tool reviews, stack breakdowns, real costs",
        "flair_options": [],
        "self_promo_ok": True,
        "min_words": 200,
    },
    "marketing": {
        "rules": "no self-promo, educational content only",
        "approach": "case studies with numbers, strategy breakdowns, what worked",
        "flair_options": [],
        "self_promo_ok": False,
        "min_words": 200,
    },
}


def safe_path(target: Path) -> Path:
    """verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def setup_logging():
    """configure file + console logging."""
    safe_path(LOG_DIR)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(safe_path(LOG_FILE), mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """parse YAML-style frontmatter from markdown. returns (meta, body)."""
    meta = {}
    body = text
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if fm_match:
        fm_block = fm_match.group(1)
        body = fm_match.group(2).strip()
        for line in fm_block.strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta, body


def load_posts(subreddit_filter: str = None) -> list[dict]:
    """load all markdown post files from POSTS_DIR."""
    posts = []
    post_dir = safe_path(POSTS_DIR)
    if not post_dir.exists():
        logging.warning(f"posts directory not found: {post_dir}")
        return posts

    for f in sorted(post_dir.glob("*.md")):
        try:
            text = f.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            if not meta.get("subreddit") or not meta.get("title"):
                logging.warning(f"skipping {f.name}: missing subreddit or title in frontmatter")
                continue
            post = {
                "file": f.name,
                "path": str(f),
                "subreddit": meta["subreddit"].lstrip("r/"),
                "title": meta["title"],
                "flair": meta.get("flair", ""),
                "scheduled_date": meta.get("scheduled_date", ""),
                "body": body,
                "word_count": len(body.split()),
            }
            if subreddit_filter and post["subreddit"].lower() != subreddit_filter.lower():
                continue
            posts.append(post)
        except Exception as e:
            logging.error(f"error loading {f.name}: {e}")
    return posts


def load_history() -> list[dict]:
    """load posting history from JSON log."""
    hist_path = safe_path(HISTORY_FILE)
    if not hist_path.exists():
        return []
    try:
        return json.loads(hist_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError):
        return []


def save_history(history: list[dict]):
    """save posting history."""
    hist_path = safe_path(HISTORY_FILE)
    hist_path.write_text(json.dumps(history, indent=2, default=str), encoding="utf-8")


def validate_post(post: dict) -> list[str]:
    """validate a post against subreddit rules. returns list of warnings."""
    warnings = []
    sub = post["subreddit"]
    config = SUBREDDIT_CONFIGS.get(sub, {})

    min_words = config.get("min_words", 150)
    if post["word_count"] < min_words:
        warnings.append(f"too short: {post['word_count']} words (min {min_words} for r/{sub})")

    if post["word_count"] > 800:
        warnings.append(f"very long: {post['word_count']} words. consider trimming.")

    if not config.get("self_promo_ok", False):
        body_lower = post["body"].lower()
        promo_signals = ["check out my", "download here", "sign up", "use my link", "buy now"]
        for signal in promo_signals:
            if signal in body_lower:
                warnings.append(f"self-promo detected ('{signal}') in r/{sub} which bans self-promo")

    if not post["title"] or len(post["title"]) > 300:
        warnings.append("title missing or too long (>300 chars)")

    return warnings


def cmd_preview(args):
    """preview mode: show what would be posted."""
    posts = load_posts(args.subreddit)
    if not posts:
        logging.info("no posts found.")
        return

    logging.info(f"found {len(posts)} posts\n")
    for i, post in enumerate(posts, 1):
        warnings = validate_post(post)
        warn_str = f"  WARNINGS: {'; '.join(warnings)}" if warnings else ""
        sub_config = SUBREDDIT_CONFIGS.get(post["subreddit"], {})
        promo_tag = "[promo OK]" if sub_config.get("self_promo_ok") else "[NO promo]"

        print(f"--- POST {i}/{len(posts)} ---")
        print(f"  file:      {post['file']}")
        print(f"  subreddit: r/{post['subreddit']} {promo_tag}")
        print(f"  title:     {post['title']}")
        print(f"  flair:     {post['flair'] or '(none)'}")
        print(f"  scheduled: {post['scheduled_date'] or '(not set)'}")
        print(f"  words:     {post['word_count']}")
        if warnings:
            print(f"  WARNINGS:  {'; '.join(warnings)}")
        print(f"  preview:   {post['body'][:200]}...")
        print()


def cmd_generate(args):
    """generate mode: create ready-to-post markdown files from templates."""
    gen_dir = safe_path(GENERATED_DIR)
    gen_dir.mkdir(parents=True, exist_ok=True)

    today = date.today()
    generated = []

    for sub_name, config in SUBREDDIT_CONFIGS.items():
        if args.subreddit and sub_name.lower() != args.subreddit.lower():
            continue

        approach = config["approach"]
        rules = config["rules"]
        promo = "self-promo allowed" if config.get("self_promo_ok") else "NO self-promo"
        flair_line = f"flair: {config['flair_options'][0]}" if config.get("flair_options") else "flair: "

        filename = f"generated_{sub_name}_{today.isoformat()}.md"
        filepath = gen_dir / filename

        template = f"""---
subreddit: r/{sub_name}
title: "[FILL IN TITLE - value-first, no clickbait]"
{flair_line}
scheduled_date: {today.isoformat()}
---

<!-- SUBREDDIT RULES: {rules} -->
<!-- APPROACH: {approach} -->
<!-- PROMO POLICY: {promo} -->
<!-- MIN WORDS: {config.get('min_words', 150)} -->

[Write your post here. Lead with value. Specific numbers. No AI slop.]

"""
        safe_path(filepath).write_text(template, encoding="utf-8")
        generated.append(filename)
        logging.info(f"generated template: {filepath}")

    # log the generation event
    history = load_history()
    history.append({
        "action": "generate",
        "timestamp": datetime.now().isoformat(),
        "files": generated,
        "subreddit_filter": args.subreddit or "all",
    })
    save_history(history)
    logging.info(f"\ngenerated {len(generated)} templates in {gen_dir}")


def cmd_status(args):
    """status mode: show posting history."""
    history = load_history()
    posts = load_posts(args.subreddit)

    print("=== REDDIT POSTER STATUS ===\n")

    # post inventory
    print(f"total post files: {len(posts)}")
    by_sub = {}
    for p in posts:
        sub = p["subreddit"]
        by_sub.setdefault(sub, []).append(p)

    for sub in sorted(by_sub.keys()):
        sub_posts = by_sub[sub]
        config = SUBREDDIT_CONFIGS.get(sub, {})
        promo = "promo OK" if config.get("self_promo_ok") else "no promo"
        print(f"  r/{sub}: {len(sub_posts)} posts ({promo})")
        for p in sub_posts:
            warns = validate_post(p)
            warn_tag = f" [!{len(warns)} warnings]" if warns else ""
            print(f"    - {p['file']} ({p['word_count']}w){warn_tag}")

    # history log
    print(f"\nhistory entries: {len(history)}")
    for entry in history[-10:]:
        ts = entry.get("timestamp", "unknown")
        action = entry.get("action", "unknown")
        detail = ""
        if action == "generate":
            detail = f" ({len(entry.get('files', []))} templates)"
        elif action == "posted":
            detail = f" r/{entry.get('subreddit', '?')} - {entry.get('title', '?')[:50]}"
        print(f"  [{ts}] {action}{detail}")

    print()


def cmd_list(args):
    """list mode: show all post files."""
    posts = load_posts(args.subreddit)
    if not posts:
        print("no posts found.")
        return

    print(f"{'FILE':<45} {'SUBREDDIT':<20} {'WORDS':>6} {'SCHEDULED':<12}")
    print("-" * 90)
    for p in posts:
        print(f"{p['file']:<45} r/{p['subreddit']:<18} {p['word_count']:>6} {p['scheduled_date'] or '-':<12}")


def cmd_mark_posted(args):
    """mark a post as 'posted' in history."""
    posts = load_posts()
    target = args.file
    found = None
    for p in posts:
        if p["file"] == target:
            found = p
            break
    if not found:
        logging.error(f"post file not found: {target}")
        return

    history = load_history()
    history.append({
        "action": "posted",
        "timestamp": datetime.now().isoformat(),
        "file": found["file"],
        "subreddit": found["subreddit"],
        "title": found["title"],
        "word_count": found["word_count"],
    })
    save_history(history)
    logging.info(f"marked as posted: {found['file']} -> r/{found['subreddit']}")


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Reddit Poster - prepare and track Reddit posts"
    )
    parser.add_argument("--preview", action="store_true", help="preview all posts")
    parser.add_argument("--generate", action="store_true", help="generate post templates")
    parser.add_argument("--status", action="store_true", help="show posting history and stats")
    parser.add_argument("--list", action="store_true", help="list all post files")
    parser.add_argument("--mark-posted", dest="mark_posted", metavar="FILE", help="mark a post file as posted")
    parser.add_argument("--subreddit", "-s", help="filter by subreddit name (e.g. SaaS)")

    args = parser.parse_args()
    setup_logging()

    if args.preview:
        cmd_preview(args)
    elif args.generate:
        cmd_generate(args)
    elif args.status:
        cmd_status(args)
    elif args.list:
        cmd_list(args)
    elif args.mark_posted:
        args.file = args.mark_posted
        cmd_mark_posted(args)
    else:
        parser.print_help()
        print("\nexample: python3 AUTOMATIONS/reddit_poster.py --preview")


if __name__ == "__main__":
    main()
