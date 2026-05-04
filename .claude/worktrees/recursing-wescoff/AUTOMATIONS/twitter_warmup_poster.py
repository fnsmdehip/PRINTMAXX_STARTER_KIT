#!/usr/bin/env python3

from __future__ import annotations
"""
TWITTER WARMUP POSTER — Posts from approved queue with warmup-safe limits.

Reads from CONTENT/social/APPROVED_POSTS_*.csv and posts to Twitter/X
following the 21-day warmup schedule. Tracks what day we're on and
enforces rate limits automatically.

Warmup phases:
  Days 1-3:   LURK ONLY — no posts, no likes, no follows
  Days 4-7:   ENGAGE ONLY — likes + follows only, still no posts
  Days 8-14:  SOFT POST — 1-2 posts/day, replies only, NO links
  Days 15-21: RAMP UP — 3-5 posts/day, short threads OK, NO links
  Days 22+:   FULL OPS — up to 10 posts/day, links OK, threads OK

Usage:
    python3 twitter_warmup_poster.py --status       # Show current warmup phase
    python3 twitter_warmup_poster.py --post         # Post next warmup-safe batch
    python3 twitter_warmup_poster.py --set-day 1    # Reset warmup day counter
    python3 twitter_warmup_poster.py --dry-run      # Show what would be posted
    python3 twitter_warmup_poster.py --advance      # Manually advance day counter

The poster will REFUSE to exceed warmup limits. No override.
"""

import argparse
import csv
import json
import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT / "AUTOMATIONS" / "agent" / "twitter_warmup_state.json"
APPROVED_DIR = PROJECT / "CONTENT" / "social"
POSTED_LOG = PROJECT / "CONTENT" / "social" / "POSTED_LOG.csv"

# Warmup phases with hard limits
WARMUP_PHASES = {
    "LURK": {
        "days": (1, 3),
        "max_posts": 0,
        "max_likes": 0,
        "max_follows": 0,
        "links_allowed": False,
        "threads_allowed": False,
        "description": "Lurk only. Browse timeline. Establish human patterns."
    },
    "ENGAGE": {
        "days": (4, 7),
        "max_posts": 0,
        "max_likes": 15,
        "max_follows": 10,
        "links_allowed": False,
        "threads_allowed": False,
        "description": "Light engagement. Likes + follows only. NO posting."
    },
    "SOFT_POST": {
        "days": (8, 14),
        "max_posts": 2,
        "max_likes": 25,
        "max_follows": 15,
        "links_allowed": False,
        "threads_allowed": False,
        "description": "Start posting. 1-2 posts/day. Replies to popular accounts. NO links."
    },
    "RAMP": {
        "days": (15, 21),
        "max_posts": 5,
        "max_likes": 40,
        "max_follows": 20,
        "links_allowed": False,
        "threads_allowed": True,
        "description": "Build velocity. 3-5 posts/day. Short threads OK. Still NO links."
    },
    "FULL_OPS": {
        "days": (22, 999),
        "max_posts": 10,
        "max_likes": 100,
        "max_follows": 30,
        "links_allowed": True,
        "threads_allowed": True,
        "description": "Full operation. Up to 10 posts/day. Links OK. Threads OK. DMs OK."
    },
}


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {
        "warmup_start": None,
        "current_day": 0,
        "posts_today": 0,
        "last_post_date": None,
        "total_posted": 0,
        "posted_ids": [],
    }


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_phase(day):
    for name, config in WARMUP_PHASES.items():
        lo, hi = config["days"]
        if lo <= day <= hi:
            return name, config
    return "FULL_OPS", WARMUP_PHASES["FULL_OPS"]


def load_approved_posts():
    """Load all approved posts from CSV files, newest first."""
    posts = []
    for f in sorted(APPROVED_DIR.glob("APPROVED_POSTS_*.csv"), reverse=True):
        with open(f, newline="", encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                text = row.get("Text", "").strip()
                if text:
                    posts.append({
                        "text": text,
                        "source_file": f.name,
                        "date": row.get("Date", ""),
                        "time": row.get("Time", ""),
                        "profile": row.get("Profile", "@PRINTMAXXER"),
                    })
    return posts


def filter_for_warmup(posts, phase_config, state):
    """Filter posts based on warmup phase rules."""
    posted_set = set(state.get("posted_ids", []))
    filtered = []

    for p in posts:
        text = p["text"]
        # Skip already posted
        text_hash = str(hash(text[:80]))
        if text_hash in posted_set:
            continue

        # No links during warmup
        if not phase_config["links_allowed"]:
            if "http" in text.lower() or "https" in text.lower() or ".com" in text.lower():
                continue

        # Skip threads during early phases
        if not phase_config["threads_allowed"]:
            if len(text) > 280:
                continue

        filtered.append(p)

    return filtered


def pick_posts(filtered, max_count):
    """Pick posts to send, with some randomization for natural feel."""
    if len(filtered) <= max_count:
        return filtered
    # Mix of newest and random for natural posting pattern
    newest = filtered[:max_count // 2 + 1]
    rest = filtered[max_count // 2 + 1:]
    random_picks = random.sample(rest, min(max_count - len(newest), len(rest)))
    return newest + random_picks


def show_status(state):
    today = datetime.now().strftime("%Y-%m-%d")
    day = state.get("current_day", 0)

    if day == 0:
        print("WARMUP NOT STARTED")
        print("Run with --set-day 1 to begin warmup, or --advance to increment.")
        return

    phase_name, phase_config = get_phase(day)

    # Reset daily counter if new day
    if state.get("last_post_date") != today:
        state["posts_today"] = 0
        state["last_post_date"] = today
        save_state(state)

    print(f"TWITTER WARMUP STATUS")
    print(f"{'='*50}")
    print(f"Day: {day}")
    print(f"Phase: {phase_name}")
    print(f"Description: {phase_config['description']}")
    print(f"")
    print(f"Today's limits:")
    print(f"  Posts:   {state['posts_today']}/{phase_config['max_posts']}")
    print(f"  Likes:   0/{phase_config['max_likes']} (manual)")
    print(f"  Follows: 0/{phase_config['max_follows']} (manual)")
    print(f"  Links:   {'YES' if phase_config['links_allowed'] else 'NO'}")
    print(f"  Threads: {'YES' if phase_config['threads_allowed'] else 'NO'}")
    print(f"")
    print(f"Total posted all-time: {state['total_posted']}")
    print(f"Warmup started: {state.get('warmup_start', 'N/A')}")

    # Show what's in the queue
    posts = load_approved_posts()
    warmup_safe = filter_for_warmup(posts, phase_config, state)
    remaining_today = max(0, phase_config['max_posts'] - state['posts_today'])
    print(f"")
    print(f"Queue: {len(posts)} total approved | {len(warmup_safe)} warmup-safe | {remaining_today} slots left today")


def do_post(state, dry_run=False):
    # INTELLIGENCE-FIRST: Get engagement intelligence before posting
    import subprocess as _sp
    _intel_result = _sp.run(
        ["python3", str(Path(__file__).parent / "intelligence_router.py"),
         "--venture", "CONTENT", "--task", "posting", "--brief"],
        capture_output=True, text=True, timeout=30
    )
    if _intel_result.returncode == 0 and _intel_result.stdout.strip():
        print(f"\nINTELLIGENCE BRIEF:\n{_intel_result.stdout.strip()[:500]}\n")

    today = datetime.now().strftime("%Y-%m-%d")
    day = state.get("current_day", 0)

    if day == 0:
        print("ERROR: Warmup not started. Run --set-day 1 first.")
        return

    phase_name, phase_config = get_phase(day)

    # Reset daily counter if new day
    if state.get("last_post_date") != today:
        state["posts_today"] = 0
        state["last_post_date"] = today

    if phase_config["max_posts"] == 0:
        print(f"BLOCKED: Phase {phase_name} (Day {day}) does not allow posting.")
        print(f"Current phase: {phase_config['description']}")
        return

    remaining = phase_config["max_posts"] - state["posts_today"]
    if remaining <= 0:
        print(f"BLOCKED: Already posted {state['posts_today']}/{phase_config['max_posts']} today.")
        return

    posts = load_approved_posts()
    warmup_safe = filter_for_warmup(posts, phase_config, state)

    if not warmup_safe:
        print("No warmup-safe posts in queue.")
        return

    to_post = pick_posts(warmup_safe, remaining)

    if dry_run:
        print(f"DRY RUN — Would post {len(to_post)} tweets (Phase: {phase_name}, Day {day})")
        print(f"{'='*50}")
        for i, p in enumerate(to_post, 1):
            print(f"\n[{i}] ({len(p['text'])} chars)")
            print(f"    {p['text'][:200]}")
        return

    # Actually post via browser-use or API
    print(f"POSTING {len(to_post)} tweets (Phase: {phase_name}, Day {day})")
    print(f"{'='*50}")

    posted_count = 0
    for p in to_post:
        text = p["text"]
        print(f"\nPosting: {text[:100]}...")

        # TODO: Integrate with browser-use or Twitter API
        # For now, log to posted file and update state
        success = log_post(text, p)
        if success:
            posted_count += 1
            state["posts_today"] += 1
            state["total_posted"] += 1
            state["posted_ids"].append(str(hash(text[:80])))
            # Keep posted_ids from growing unbounded
            if len(state["posted_ids"]) > 5000:
                state["posted_ids"] = state["posted_ids"][-3000:]

        # Random delay between posts (human-like)
        if posted_count < len(to_post):
            import time
            delay = random.uniform(120, 600)  # 2-10 min between posts
            print(f"  Waiting {delay:.0f}s before next post...")
            if not dry_run:
                time.sleep(delay)

    save_state(state)
    print(f"\nPosted {posted_count}/{len(to_post)} tweets. Total all-time: {state['total_posted']}")


def log_post(text, post_meta):
    """Log posted content to POSTED_LOG.csv"""
    file_exists = POSTED_LOG.exists()
    try:
        with open(POSTED_LOG, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["text", "posted_at", "source_file", "profile", "platform", "status"])
            writer.writerow([
                text[:280],
                datetime.now().isoformat(),
                post_meta.get("source_file", ""),
                post_meta.get("profile", "@PRINTMAXXER"),
                "twitter",
                "QUEUED_FOR_MANUAL_POST",  # Until API integration
            ])
        return True
    except Exception as e:
        print(f"  ERROR logging post: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Twitter warmup-safe poster")
    parser.add_argument("--status", action="store_true", help="Show current warmup status")
    parser.add_argument("--post", action="store_true", help="Post next warmup-safe batch")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be posted")
    parser.add_argument("--set-day", type=int, help="Set warmup day counter")
    parser.add_argument("--advance", action="store_true", help="Advance warmup day by 1")
    args = parser.parse_args()

    state = load_state()

    if args.set_day is not None:
        state["current_day"] = args.set_day
        if args.set_day == 1:
            state["warmup_start"] = datetime.now().strftime("%Y-%m-%d")
        save_state(state)
        print(f"Warmup day set to {args.set_day}")
        show_status(state)
        return

    if args.advance:
        state["current_day"] = state.get("current_day", 0) + 1
        if state["current_day"] == 1:
            state["warmup_start"] = datetime.now().strftime("%Y-%m-%d")
        save_state(state)
        print(f"Advanced to day {state['current_day']}")
        show_status(state)
        return

    if args.dry_run:
        do_post(state, dry_run=True)
        return

    if args.post:
        do_post(state)
        return

    # Default: show status
    show_status(state)


if __name__ == "__main__":
    main()
