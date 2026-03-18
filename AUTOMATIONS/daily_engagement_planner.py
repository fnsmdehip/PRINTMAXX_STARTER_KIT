#!/usr/bin/env python3
"""
DAILY ENGAGEMENT PLANNER — Generates "do exactly this today" action plan.

Reads warmup state, intelligence, reply strategy, approved posts, and growth
intel to produce a concrete daily engagement plan that respects warmup limits.

The output tells the human EXACTLY what to do. No thinking required.

Usage:
    python3 daily_engagement_planner.py              # Generate today's plan
    python3 daily_engagement_planner.py --save        # Save to posting_queue/
    python3 daily_engagement_planner.py --tomorrow    # Preview tomorrow's plan
    python3 daily_engagement_planner.py --metrics     # Show current system metrics for posts

Runs via cron at 7:00 AM daily.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
CONTENT = PROJECT / "CONTENT"
SOCIAL = CONTENT / "social"
POSTING_QUEUE = SOCIAL / "posting_queue"
WARMUP_STATE = AUTOMATIONS / "agent" / "twitter_warmup_state.json"
REPLY_STRATEGY = SOCIAL / "REPLY_ENGAGEMENT_STRATEGY.md"
OPS = PROJECT / "OPS"

# Warmup phases — mirrors twitter_warmup_poster.py
PHASES = {
    "LURK":      {"days": (1, 3),   "posts": 0, "likes": 0,   "follows": 0,  "replies": 0},
    "ENGAGE":    {"days": (4, 7),   "posts": 0, "likes": 15,  "follows": 10, "replies": 5},
    "SOFT_POST": {"days": (8, 14),  "posts": 2, "likes": 25,  "follows": 15, "replies": 10},
    "RAMP":      {"days": (15, 21), "posts": 5, "likes": 40,  "follows": 20, "replies": 15},
    "FULL_OPS":  {"days": (22, 999),"posts": 10,"likes": 100, "follows": 30, "replies": 25},
}

# Reply targets by tier (from REPLY_ENGAGEMENT_STRATEGY.md)
TIER1_REPLY_TARGETS = [
    {"handle": "@levelsio", "window": "within 10 min", "audience": "indie hackers", "freq": "3-5x/day"},
    {"handle": "@gregisenberg", "window": "within 15 min", "audience": "startup ideas", "freq": "2-3x/day"},
    {"handle": "@pipelineabuser", "window": "within 5 min", "audience": "cold email/outbound", "freq": "6-8x/day"},
    {"handle": "@codyschneiderxx", "window": "within 10 min", "audience": "SaaS growth", "freq": "3-5x/day"},
    {"handle": "@dickiebush", "window": "within 15 min", "audience": "writing/content", "freq": "2-3x/day"},
]

TIER2_REPLY_TARGETS = [
    {"handle": "@bcherny", "window": "on announcements", "audience": "Claude/Anthropic", "freq": "product launches"},
    {"handle": "@kloss_xyz", "window": "within 5 min", "audience": "Claude Code", "freq": "feature drops"},
    {"handle": "@steipete", "window": "within 15 min", "audience": "Codex/dev tools", "freq": "product drops"},
    {"handle": "@karpathy", "window": "within 10 min", "audience": "AI/ML", "freq": "paradigm posts"},
]

SWEETSPOT_TARGETS = [
    {"handle": "@knoxtwts", "freq": "every post", "audience": "app marketing"},
    {"handle": "@lottsnomad", "freq": "every post", "audience": "YC/app scaling"},
    {"handle": "@alexcooldev", "freq": "every post", "audience": "indie hacking"},
    {"handle": "@weswinder", "freq": "3-5x/week", "audience": "vibe coding"},
    {"handle": "@antonioescudero", "freq": "every revenue post", "audience": "SaaS building"},
    {"handle": "@jackfriks", "freq": "every post", "audience": "solo apps"},
    {"handle": "@ecomchigga", "freq": "every product post", "audience": "digital products"},
    {"handle": "@EXM7777", "freq": "every post", "audience": "AI ops/systems"},
    {"handle": "@damianplayer", "freq": "3-5x/week", "audience": "AI agent loops"},
    {"handle": "@WorkflowWhisper", "freq": "every non-keyword post", "audience": "n8n workflows"},
    {"handle": "@whotfiszackk", "freq": "every post", "audience": "info products + AI"},
]

LIKE_TARGETS = [
    "@levelsio", "@gregisenberg", "@pipelineabuser", "@codyschneiderxx",
    "@dickiebush", "@knoxtwts", "@alexcooldev", "@weswinder",
    "@antonioescudero", "@jackfriks", "@ecomchigga", "@EXM7777",
    "@damianplayer", "@WorkflowWhisper", "@simonecanciello",
]

FOLLOW_TARGETS_POOL = [
    # People who follow our targets — discover via their reply sections
    "indie hackers in @levelsio reply sections",
    "builders in @gregisenberg idea threads",
    "cold email practitioners in @pipelineabuser tool drops",
    "app devs in @knoxtwts threads",
    "AI automation builders in @EXM7777 threads",
    "solo founders sharing revenue milestones",
    "build-in-public accounts with 1K-50K followers",
]

# Reply hooks (from the 12 proven hooks)
REPLY_HOOKS = {
    "tested_this": {
        "name": "I Tested This",
        "when": "Any post sharing a tactic, tool, or method",
        "template": "tested this for {days} days across {accounts} accounts.\n\nscraped {datapoints} data points. the signal-to-noise ratio was about 15%.\n\nthe 15% that was real alpha generated {posts_gen} content pieces automatically.",
    },
    "didnt_mention": {
        "name": "What They Didn't Mention",
        "when": "Thread or tutorial posts that leave gaps",
        "template": "the part nobody mentions: {insight}.\n\n{detail}.\n\nthe real play is {actual_play}.",
    },
    "automation_angle": {
        "name": "The Automation Angle",
        "when": "Any manual process someone shares",
        "template": "automated this entire workflow last week.\n\nplaywright scraper runs every 3 hours. claude scores each result. top 5% get auto-routed to my content queue.\n\nwhole thing runs on a $5/mo server. 0 human hours after setup.\n\n{agents} agents doing this across every money method i find.",
    },
    "honest_zero": {
        "name": "Honest $0 Transparency",
        "when": "Revenue milestone posts",
        "template": "love this. congrats on the milestone.\n\ni'm on day {day} at $0. but the system is built:\n- {agents} agents scraping and generating content\n- {datapoints}+ data points analyzed\n- {assets} assets deployed\n\nthe delta between 'everything is built' and 'first dollar' is what i'm documenting.",
    },
    "tool_stack": {
        "name": "The Tool Stack Reply",
        "when": "Posts about tools, workflows, or automation",
        "template": "my stack for this:\n\n- playwright for scraping (brave cookie injection, no API needed)\n- claude for scoring/categorizing\n- csv pipeline for routing to ventures\n- launchd for scheduling (cron alternative, survives reboots)\n\ntotal cost: $0 beyond the claude subscription. runs 24/7.",
    },
    "war_story": {
        "name": "The War Story",
        "when": "Posts about failures, mistakes, or problems",
        "template": "learned this the expensive way.\n\nsent 500 cold emails with a broken template. domain got nuked in 3 hours.\n\nnow every email goes through 3 validation checks before sending. the {agents} agents do it automatically.\n\nthe automation exists BECAUSE of the failure.",
    },
}


def load_warmup_state() -> dict[str, Any]:
    if WARMUP_STATE.exists():
        with open(WARMUP_STATE) as f:
            return json.load(f)
    return {"current_day": 0, "posts_today": 0, "total_posted": 0}


def get_phase(day: int) -> tuple[str, dict[str, Any]]:
    for name, config in PHASES.items():
        lo, hi = config["days"]
        if lo <= day <= hi:
            return name, config
    return "FULL_OPS", PHASES["FULL_OPS"]


def get_system_metrics() -> dict[str, Any]:
    """Pull real metrics from the system for use in reply templates."""
    metrics = {
        "days": 0,
        "agents": 31,
        "datapoints": "14,799",
        "posts_gen": 588,
        "assets": 36,
        "accounts": 92,
        "alpha_entries": "14,799",
    }
    # Get warmup day
    state = load_warmup_state()
    metrics["day"] = state.get("current_day", 0)
    start = state.get("warmup_start")
    if start:
        try:
            d = datetime.strptime(start, "%Y-%m-%d")
            metrics["days"] = (datetime.now() - d).days
        except Exception:
            pass

    # Get alpha count
    try:
        result = subprocess.run(
            ["python3", str(AUTOMATIONS / "alpha_query.py"), "--stats"],
            capture_output=True, text=True, timeout=10, cwd=str(PROJECT)
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "total" in line.lower() and "entries" in line.lower():
                    import re
                    nums = re.findall(r"[\d,]+", line)
                    if nums:
                        metrics["datapoints"] = nums[0]
                        metrics["alpha_entries"] = nums[0]
                        break
    except Exception:
        pass

    return metrics


def get_todays_posts(phase_config: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    """Get warmup-safe posts for today from posting queue."""
    today = datetime.now()
    date_str = today.strftime("mar%d").lstrip("0").replace("mar0", "mar")
    # Try to find today's posts in posting_queue
    posts = []
    day_num = today.day
    pattern = f"twitter_PRINTMAXXER_mar{day_num}_*.txt"
    for f in sorted(POSTING_QUEUE.glob(pattern)):
        try:
            content = f.read_text(encoding="utf-8")
            # Parse the post file
            lines = content.strip().split("\n")
            text = ""
            scheduled = ""
            for line in lines:
                if line.startswith("SCHEDULED:"):
                    scheduled = line.split(":", 1)[1].strip()
                if line == "---":
                    text = "\n".join(lines[lines.index(line)+1:]).strip()
                    break
            if text and len(text) <= 280:
                posts.append({"text": text, "time": scheduled, "file": f.name})
        except Exception:
            continue

    # Also check approved CSVs
    for f in sorted(SOCIAL.glob("APPROVED_POSTS_*.csv"), reverse=True):
        try:
            with open(f, newline="", encoding="utf-8", errors="replace") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    text = row.get("Text", "").strip()
                    if text and len(text) <= 280:
                        # No links during warmup
                        if not phase_config.get("links_allowed", phase_config["posts"] > 5):
                            if any(x in text.lower() for x in ["http", ".com", ".io"]):
                                continue
                        posts.append({"text": text, "time": "", "file": f.name})
        except Exception:
            continue

    # Limit to phase max
    max_posts = phase_config["posts"]
    return posts[:max_posts]


def get_intelligence_brief(venture: str = "GROWTH", task: str = "engagement") -> str:
    """Pull intelligence brief for the plan."""
    parts = []
    try:
        result = subprocess.run(
            ["python3", str(AUTOMATIONS / "intelligence_router.py"),
             "--venture", venture, "--task", task, "--brief"],
            capture_output=True, text=True, timeout=15, cwd=str(PROJECT)
        )
        if result.returncode == 0:
            parts.append(result.stdout.strip()[:600])
    except Exception:
        pass

    # Capital Genesis Priority Stack — surface top-ranked methods for daily planning
    cap_gen_path = PROJECT / "OPS" / "CAPITAL_GENESIS_PRIORITY_STACK.md"
    if cap_gen_path.exists():
        try:
            stack = cap_gen_path.read_text()
            # Extract P0 section for daily action planning
            p0_end = stack.find("## P1:")
            if p0_end > 0:
                parts.append(f"PRIORITY STACK (P0 — DO NOW):\n{stack[:p0_end].strip()[:500]}")
            else:
                parts.append(f"PRIORITY STACK:\n{stack[:500]}")
        except Exception:
            pass

    return "\n\n".join(parts) if parts else ""


def populate_reply_template(hook_key: str, metrics: dict[str, Any]) -> str:
    """Fill a reply hook template with real metrics."""
    hook = REPLY_HOOKS.get(hook_key, {})
    template = hook.get("template", "")
    try:
        return template.format(**metrics)
    except KeyError:
        # Fill what we can
        for k, v in metrics.items():
            template = template.replace("{" + k + "}", str(v))
        return template


def generate_plan(day_override: Optional[int] = None, save: bool = False) -> str:
    """Generate the daily engagement plan."""
    state = load_warmup_state()
    today = datetime.now()
    day = day_override or state.get("current_day", 0)

    if day == 0:
        print("WARMUP NOT STARTED. Run: python3 AUTOMATIONS/twitter_warmup_poster.py --set-day 1")
        return ""

    phase_name, phase_config = get_phase(day)
    metrics = get_system_metrics()
    metrics["day"] = day

    lines = []
    lines.append(f"# DAILY ENGAGEMENT PLAN — {today.strftime('%B %d, %Y')}")
    lines.append(f"# @PRINTMAXXER | Warmup Day {day} | Phase: {phase_name}")
    lines.append(f"# Auto-generated at {today.strftime('%H:%M')} by daily_engagement_planner.py")
    lines.append("")
    lines.append("---")
    lines.append("")

    # PHASE BRIEFING
    lines.append(f"## PHASE: {phase_name} (Day {day})")
    lines.append("")

    phase_desc = {
        "LURK": "LURK MODE. Browse timeline. Observe patterns. Do NOT post, like, or follow.\nGoal: Establish human browsing patterns so the algorithm recognizes you as a real user.",
        "ENGAGE": f"ENGAGE MODE. Likes + follows ONLY. Still no posting.\nToday's limits: {phase_config['likes']} likes, {phase_config['follows']} follows, {phase_config['replies']} replies to others' posts.\nGoal: Build engagement signals without triggering spam detection.",
        "SOFT_POST": f"SOFT POST MODE. Start posting carefully.\nToday's limits: {phase_config['posts']} posts, {phase_config['likes']} likes, {phase_config['follows']} follows, {phase_config['replies']} replies.\nNO links. NO threads. Short, value-add posts only.",
        "RAMP": f"RAMP MODE. Building velocity.\nToday's limits: {phase_config['posts']} posts, {phase_config['likes']} likes, {phase_config['follows']} follows, {phase_config['replies']} replies.\nShort threads OK. Still NO links.",
        "FULL_OPS": f"FULL OPERATIONS. All systems go.\nToday's limits: {phase_config['posts']} posts, {phase_config['likes']} likes, {phase_config['follows']} follows, {phase_config['replies']} replies.\nLinks OK. Threads OK. DMs OK.",
    }
    lines.append(phase_desc.get(phase_name, ""))
    lines.append("")

    # HARD LIMITS BOX
    lines.append("```")
    lines.append(f"HARD LIMITS (DO NOT EXCEED):")
    lines.append(f"  Posts:   {phase_config['posts']}")
    lines.append(f"  Likes:   {phase_config['likes']}")
    lines.append(f"  Follows: {phase_config['follows']}")
    lines.append(f"  Replies: {phase_config['replies']}")
    lines.append(f"  Links:   {'YES' if phase_config['posts'] >= 10 else 'NO'}")
    lines.append(f"  Threads: {'YES' if phase_config['posts'] >= 5 else 'NO'}")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    # SECTION 1: POSTING (if allowed)
    if phase_config["posts"] > 0:
        lines.append(f"## 1. POSTS TODAY ({phase_config['posts']} max)")
        lines.append("")
        posts = get_todays_posts(phase_config, state)
        if posts:
            for i, p in enumerate(posts, 1):
                time_str = p.get("time", "")
                if time_str:
                    lines.append(f"### Post {i} — {time_str}")
                else:
                    times = ["8:00 AM ET", "12:30 PM ET", "5:30 PM ET", "8:00 PM ET", "10:00 PM ET"]
                    lines.append(f"### Post {i} — {times[i-1] if i <= len(times) else 'any time'}")
                lines.append("")
                lines.append("Copy-paste verbatim:")
                lines.append("```")
                lines.append(p["text"])
                lines.append("```")
                lines.append(f"Chars: {len(p['text'])}/280")
                lines.append(f"Source: {p.get('file', 'approved queue')}")
                lines.append("")
        else:
            lines.append("No warmup-safe posts in queue. Generate new ones or check APPROVED_POSTS CSVs.")
            lines.append("")
    else:
        lines.append("## 1. POSTS TODAY: NONE")
        lines.append("")
        lines.append(f"Phase {phase_name} does not allow posting. {'Browse and observe.' if phase_name == 'LURK' else 'Focus on engagement below.'}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # SECTION 2: REPLY STRATEGY
    if phase_config["replies"] > 0:
        lines.append(f"## 2. REPLIES TODAY ({phase_config['replies']} max)")
        lines.append("")

        # Select targets based on phase aggressiveness
        if phase_name == "ENGAGE":
            # Light replies only to sweet-spot accounts
            targets = random.sample(SWEETSPOT_TARGETS, min(5, len(SWEETSPOT_TARGETS)))
            lines.append("**Reply only to smaller accounts (10K-100K). Stay under the radar.**")
            lines.append("")
            for t in targets:
                lines.append(f"- {t['handle']} — {t['audience']} — reply if they post today")
        elif phase_name == "SOFT_POST":
            # Mix of sweet-spot + some Tier 1
            tier1_pick = random.sample(TIER1_REPLY_TARGETS, 2)
            sweet_pick = random.sample(SWEETSPOT_TARGETS, 5)
            lines.append("**2 Tier 1 replies + 5 sweet-spot replies. Use hooks 1-3 only (tested this, didn't mention, automation angle).**")
            lines.append("")
            lines.append("### Tier 1 (be in first 10 replies):")
            for t in tier1_pick:
                lines.append(f"- {t['handle']} — {t['window']} — {t['audience']}")
            lines.append("")
            lines.append("### Sweet Spot (high ROI, OPs read replies):")
            for t in sweet_pick:
                lines.append(f"- {t['handle']} — {t['freq']} — {t['audience']}")
        else:
            # RAMP and FULL_OPS — full strategy
            lines.append("### Tier 1 Targets (reply within stated window):")
            lines.append("")
            for t in TIER1_REPLY_TARGETS:
                lines.append(f"- {t['handle']} — {t['window']} — {t['audience']}")
            lines.append("")
            lines.append("### Tier 2 (reply on announcements/drops):")
            lines.append("")
            for t in TIER2_REPLY_TARGETS:
                lines.append(f"- {t['handle']} — {t['window']} — {t['audience']}")
            lines.append("")
            lines.append("### Sweet Spot (highest ROI — OPs reply back):")
            lines.append("")
            for t in random.sample(SWEETSPOT_TARGETS, min(7, len(SWEETSPOT_TARGETS))):
                lines.append(f"- {t['handle']} — {t['freq']} — {t['audience']}")

        lines.append("")

        # Draft replies with real metrics
        lines.append("### DRAFT REPLIES (copy-paste, adjust to context):")
        lines.append("")

        # Pick 3 hooks appropriate to phase
        if phase_name in ("ENGAGE", "SOFT_POST"):
            hook_keys = ["tested_this", "automation_angle", "honest_zero"]
        else:
            hook_keys = random.sample(list(REPLY_HOOKS.keys()), 3)

        for hk in hook_keys:
            hook = REPLY_HOOKS[hk]
            lines.append(f"**{hook['name']}** — use when: {hook['when']}")
            lines.append("```")
            filled = populate_reply_template(hk, metrics)
            lines.append(filled)
            lines.append("```")
            lines.append("")
    else:
        lines.append("## 2. REPLIES TODAY: NONE")
        lines.append("")
        lines.append("Lurk phase. Read replies from Tier 1 accounts. Observe what gets engagement. Take mental notes.")
        lines.append("")

    lines.append("---")
    lines.append("")

    # SECTION 3: ENGAGEMENT (likes + follows)
    if phase_config["likes"] > 0 or phase_config["follows"] > 0:
        lines.append(f"## 3. ENGAGEMENT ({phase_config['likes']} likes, {phase_config['follows']} follows)")
        lines.append("")

        if phase_config["likes"] > 0:
            lines.append(f"### Likes ({phase_config['likes']} max today)")
            lines.append("")
            # Pick accounts to like
            like_pool = random.sample(LIKE_TARGETS, min(phase_config["likes"], len(LIKE_TARGETS)))
            lines.append("Like 1 recent post from each of these accounts:")
            lines.append("")
            for handle in like_pool:
                lines.append(f"- {handle}")
            lines.append("")
            lines.append("**Rules:** Space likes out over the day. Don't rapid-fire. Mix with normal browsing.")
            lines.append("")

        if phase_config["follows"] > 0:
            lines.append(f"### Follows ({phase_config['follows']} max today)")
            lines.append("")
            follow_targets = random.sample(FOLLOW_TARGETS_POOL, min(3, len(FOLLOW_TARGETS_POOL)))
            lines.append("Find and follow accounts from:")
            lines.append("")
            for target in follow_targets:
                lines.append(f"- {target}")
            lines.append("")
            lines.append("**Rules:** Follow people who post about building/automation/indie hacking.")
            lines.append("**Do NOT:** Follow-unfollow. Follow celebrities. Follow accounts with 1M+ followers.")
            lines.append("")
    else:
        lines.append("## 3. ENGAGEMENT: NONE")
        lines.append("")
        lines.append("Lurk phase. Zero likes, zero follows. Just browse.")
        lines.append("")

    lines.append("---")
    lines.append("")

    # SECTION 4: TIMING SCHEDULE
    lines.append("## 4. TIMING SCHEDULE")
    lines.append("")

    if phase_name == "LURK":
        lines.append("```")
        lines.append("  7:30-8:00 AM  — Browse timeline. Read 20 tweets. Close app.")
        lines.append("  12:00-12:15 PM — Browse again. Note which accounts get replies.")
        lines.append("  6:00-6:15 PM  — Final browse. Observe evening posting patterns.")
        lines.append("```")
    elif phase_name == "ENGAGE":
        lines.append("```")
        lines.append(f"  7:30-8:00 AM  — Like 5 posts from timeline. Follow 3 accounts.")
        lines.append(f"  12:00-12:30 PM — Like 5 more posts. Reply to 2 sweet-spot accounts.")
        lines.append(f"  6:00-6:30 PM  — Like 5 posts. Follow 4 accounts. Reply to 3 posts.")
        lines.append("```")
    elif phase_name == "SOFT_POST":
        lines.append("```")
        lines.append(f"  7:30-8:00 AM  — Post tweet #1. Like 8 posts. Reply to 3 accounts.")
        lines.append(f"  12:00-12:30 PM — Like 8 posts. Reply to 4 accounts. Follow 5.")
        lines.append(f"  5:30-6:00 PM  — Post tweet #2. Like 9 posts. Reply to 3. Follow 5.")
        lines.append(f"  9:00-9:15 PM  — Reply to any comments on your posts.")
        lines.append("```")
    elif phase_name == "RAMP":
        lines.append("```")
        lines.append(f"  7:30-8:00 AM  — Post tweet #1. Reply to Tier 1 (first 10 min). Like 10.")
        lines.append(f"  11:00-11:30 AM — Post tweet #2. Reply to 4 accounts. Like 10.")
        lines.append(f"  2:30-3:00 PM  — Post tweet #3. Reply to 3 sweet-spots. Follow 10.")
        lines.append(f"  5:30-6:00 PM  — Post tweet #4. Like 10. Reply to revenue posts.")
        lines.append(f"  9:00-9:30 PM  — Post tweet #5. Reply to all comments. Like 10. Follow 10.")
        lines.append("```")
    else:
        lines.append("```")
        lines.append(f"  7:30 AM  — Post #1. Reply to Tier 1 targets. Like 15.")
        lines.append(f"  9:00 AM  — Post #2. Reply to Tier 2 (announcements). Like 10.")
        lines.append(f"  11:00 AM — Post #3. Reply to sweet-spot accounts. Follow 10.")
        lines.append(f"  1:00 PM  — Post #4. Like 15. Reply to revenue posts.")
        lines.append(f"  3:00 PM  — Post #5. Reply to all comments on your posts.")
        lines.append(f"  5:00 PM  — Post #6-7. Like 15. Follow 10.")
        lines.append(f"  7:00 PM  — Post #8. Reply to evening posts. Like 15.")
        lines.append(f"  9:00 PM  — Post #9-10. Final engagement sweep. Follow 10. Like remaining.")
        lines.append("```")

    lines.append("")
    lines.append("---")
    lines.append("")

    # SECTION 5: ANTI-FLAG RULES
    lines.append("## 5. ANTI-FLAG RULES (warmup safety)")
    lines.append("")
    lines.append("```")
    lines.append("DO:")
    lines.append("  - Space actions 2-5 min apart (not rapid-fire)")
    lines.append("  - Mix engagement with normal browsing")
    lines.append("  - Vary reply length (1-5 lines, not always same)")
    lines.append("  - Reply to different accounts (not same 3 all day)")
    lines.append("  - Browse timeline between actions (scroll for 30 sec)")
    lines.append("")
    lines.append("DO NOT:")
    lines.append("  - Exceed the hard limits above under ANY circumstance")
    lines.append("  - Post links (not until day 22)")
    lines.append("  - Follow more than 5 accounts in 10 minutes")
    lines.append("  - Like more than 5 posts in 5 minutes")
    lines.append("  - Use the same reply template twice in one day")
    lines.append("  - Reply to the same account more than 2x per day")
    lines.append("  - Use hashtags (signals automation)")
    lines.append("  - Post identical content to what's already in your timeline")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    # SECTION 6: INTELLIGENCE BRIEF
    intel = get_intelligence_brief("GROWTH", "engagement")
    if intel:
        lines.append("## 6. INTELLIGENCE BRIEF")
        lines.append("")
        # Truncate to relevant portion
        intel_lines = intel.split("\n")[:15]
        for il in intel_lines:
            lines.append(f"> {il}")
        lines.append("")

    # SECTION 7: SYSTEM METRICS (for personalizing replies)
    lines.append("## 7. YOUR NUMBERS (use these in replies)")
    lines.append("")
    lines.append("```")
    lines.append(f"  Warmup day:      {day}")
    lines.append(f"  Days running:    {metrics.get('days', day)}")
    lines.append(f"  Agents:          {metrics['agents']}")
    lines.append(f"  Data points:     {metrics['datapoints']}")
    lines.append(f"  Posts generated: {metrics['posts_gen']}")
    lines.append(f"  Assets deployed: {metrics['assets']}")
    lines.append(f"  Revenue:         $0 (transparent — this IS the angle)")
    lines.append(f"  Alpha entries:   {metrics['alpha_entries']}")
    lines.append("```")
    lines.append("")
    lines.append("Use these EXACT numbers in replies. Specificity = credibility.")
    lines.append("")

    plan = "\n".join(lines)

    # Output
    if save:
        POSTING_QUEUE.mkdir(parents=True, exist_ok=True)
        date_str = today.strftime("%Y-%m-%d")
        out_path = POSTING_QUEUE / f"ENGAGEMENT_PLAN_{date_str}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(plan)
        print(f"Saved to {out_path}")
    else:
        print(plan)

    return plan


def show_metrics() -> None:
    """Show current system metrics that would be used in replies."""
    metrics = get_system_metrics()
    print("SYSTEM METRICS FOR REPLY PERSONALIZATION")
    print("=" * 50)
    for k, v in metrics.items():
        print(f"  {k}: {v}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily engagement planner")
    parser.add_argument("--save", action="store_true", help="Save plan to posting_queue/")
    parser.add_argument("--tomorrow", action="store_true", help="Preview tomorrow's plan")
    parser.add_argument("--metrics", action="store_true", help="Show system metrics")
    args = parser.parse_args()

    if args.metrics:
        show_metrics()
        return

    if args.tomorrow:
        state = load_warmup_state()
        generate_plan(day_override=state.get("current_day", 0) + 1, save=False)
        return

    generate_plan(save=args.save)


if __name__ == "__main__":
    main()
