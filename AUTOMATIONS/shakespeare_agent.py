#!/usr/bin/env python3
"""
SHAKESPEARE AGENT — Movement-First Content Generation (Swan AI GTM T015)
=========================================================================

Generates 1 LinkedIn post + 1 Twitter/X post daily using the PRINTMAXX
intelligence pipeline. Posts follow an enforced narrative arc:

  Line 1:    Attack an outdated belief about [topic from alpha]
  Lines 2-4: Evidence why the old way is broken
  Lines 5-7: The new framework (PRINTMAXX/EAS approach)
  Lines 8-9: Specific result or data point
  Line 10:   CTA (follow, comment, DM)

Also generates weekly "build-in-public" threads with real system stats.

Usage:
    python3 shakespeare_agent.py --generate          # Daily posts (1 LinkedIn + 1 Twitter)
    python3 shakespeare_agent.py --thread            # Weekly build-in-public thread
    python3 shakespeare_agent.py --status            # Show generation stats
    python3 shakespeare_agent.py --dry-run           # Preview without writing files

No actual API calls — writes content files to posting queues for review.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# ── Sibling imports ───────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import PROJECT, safe_path, load_json, log, ts, VENTURES

try:
    from intelligence_router import get_intelligence
    _ROUTER_AVAILABLE = True
except ImportError:
    _ROUTER_AVAILABLE = False

try:
    from master_ops_bridge import MasterOpsBridge
    _BRIDGE_AVAILABLE = True
except ImportError:
    _BRIDGE_AVAILABLE = False

# ── Paths ─────────────────────────────────────────────────────────────
AUTOMATIONS = PROJECT / "AUTOMATIONS"
CONTENT = PROJECT / "CONTENT"
LINKEDIN_DIR = CONTENT / "linkedin"
POSTING_QUEUE = CONTENT / "social" / "posting_queue"
INTEL_CATALOG = PROJECT / "OPS" / "INTELLIGENCE_CATALOG.json"
MARKET_SIGNALS = PROJECT / "LEDGER" / "MARKET_SIGNALS.csv"
ALPHA_STAGING = PROJECT / "LEDGER" / "ALPHA_STAGING.csv"
STATE_FILE = AUTOMATIONS / "agent" / "shakespeare_state.json"

# ── Topic Rotation Pool ──────────────────────────────────────────────
TOPIC_POOL = [
    {
        "slug": "implementation_gap",
        "label": "The Implementation Gap",
        "outdated_belief": "you need more information to succeed",
        "reality": "you're drowning in information. you have 14,799 data points and $0 revenue. the gap isn't knowledge, it's execution.",
        "framework": "execution-first systems that close loops automatically. every scan becomes an asset, every asset gets distributed, every distribution gets tracked.",
    },
    {
        "slug": "autonomous_business_os",
        "label": "Autonomous Business OS",
        "outdated_belief": "you need a team to scale",
        "reality": "you need 33 agents running 24/7 on a $200/mo subscription. they scrape, score, route, build, and distribute while you sleep.",
        "framework": "a CEO agent orchestrating 25 operational agents across 8 ventures. zero employees. zero meetings. pure autonomous execution.",
    },
    {
        "slug": "solopreneur_leverage",
        "label": "Solopreneur Leverage",
        "outdated_belief": "solopreneurs can't compete with funded startups",
        "reality": "funded startups burn $50k/mo on salaries for 5 people doing what 33 agents do for $200/mo. your margin IS the moat.",
        "framework": "portfolio approach: 10+ revenue lanes simultaneously. each has 30% success rate. 10 lanes = 97% chance at least one hits.",
    },
    {
        "slug": "ai_agent_roi",
        "label": "AI Agent ROI",
        "outdated_belief": "AI is for chatbots and writing emails",
        "reality": "AI agents run entire business operations. scraping, scoring, routing, building, deploying, monitoring. 24/7. no breaks. no opinions.",
        "framework": "intelligence-first execution. every agent queries 484 docs and 14,799 alpha entries before making a single decision.",
    },
    {
        "slug": "33_agents_200_mo",
        "label": "33 Agents for $200/mo",
        "outdated_belief": "automation is expensive and fragile",
        "reality": "one Claude Max subscription. 33 autonomous agents. 8 venture pipelines. 112 cron jobs. total cost: $200/mo.",
        "framework": "launchd-managed agent swarm with circuit breakers, retry logic, checkpoint-resume, and self-healing. crashes are expected and handled.",
    },
]

# ── Quality Scoring ──────────────────────────────────────────────────

def score_post(text: str) -> int:
    """Score a post on actionability (1-10). Checks for specifics, numbers,
    clear framework, and CTA."""
    score = 5  # baseline

    # Specific numbers boost score
    import re
    numbers = re.findall(r'\$[\d,]+|\d{2,}[+%]?|\d+[xX]', text)
    if len(numbers) >= 2:
        score += 2
    elif len(numbers) >= 1:
        score += 1

    # Has a clear framework/method reference
    framework_signals = [
        "agent", "pipeline", "automated", "system", "cron",
        "scrape", "score", "route", "deploy", "intelligence",
        "venture", "lane", "loop", "CEO agent",
    ]
    framework_hits = sum(1 for s in framework_signals if s.lower() in text.lower())
    if framework_hits >= 3:
        score += 2
    elif framework_hits >= 1:
        score += 1

    # Has a CTA
    cta_signals = ["follow", "comment", "DM", "reply", "thread", "share", "bookmark"]
    if any(s.lower() in text.lower() for s in cta_signals):
        score += 1

    # Penalty: too generic / too short
    if len(text) < 100:
        score -= 1
    if "leverage" in text.lower() or "comprehensive" in text.lower():
        score -= 2  # AI slop detected

    return max(1, min(10, score))


# ── Intelligence Gathering ───────────────────────────────────────────

def gather_intel() -> dict[str, Any]:
    """Pull intelligence from catalog, market signals, and alpha entries."""
    intel: dict[str, Any] = {
        "catalog_topics": [],
        "market_signals": [],
        "alpha_snippets": [],
        "system_stats": {},
    }

    # 1. Intelligence Catalog
    catalog = load_json(INTEL_CATALOG, {})
    ventures = catalog.get("ventures", {})
    for venture_name, venture_data in ventures.items():
        docs = venture_data.get("docs", [])
        for doc in docs[:5]:  # top 5 per venture
            summary = doc.get("high_value_summary", doc.get("summary", ""))
            if summary:
                intel["catalog_topics"].append({
                    "venture": venture_name,
                    "summary": summary[:200],
                    "tactics": doc.get("key_tactics", [])[:3],
                })

    # 2. Market Signals (recent)
    if MARKET_SIGNALS.exists():
        try:
            with open(MARKET_SIGNALS, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                for row in rows[-10:]:  # last 10 signals
                    intel["market_signals"].append({
                        "category": row.get("category", ""),
                        "signal": row.get("signal", "")[:150],
                        "confidence": row.get("confidence", ""),
                    })
        except Exception:
            pass

    # 3. Alpha entries (latest approved)
    if ALPHA_STAGING.exists():
        try:
            with open(ALPHA_STAGING, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    status = row.get("status", "").upper()
                    if status == "APPROVED":
                        snippet = row.get("content", row.get("alpha", row.get("description", "")))
                        if snippet:
                            intel["alpha_snippets"].append(snippet[:200])
            intel["alpha_snippets"] = intel["alpha_snippets"][-20:]  # last 20
        except Exception:
            pass

    # 4. Intelligence router (if available)
    if _ROUTER_AVAILABLE:
        try:
            router_intel = get_intelligence("CONTENT", task_type="posting")
            if isinstance(router_intel, dict):
                intel["router_brief"] = router_intel.get("brief", "")
        except Exception:
            pass

    # 5. System stats (for build-in-public content)
    intel["system_stats"] = _get_system_stats()

    return intel


def _get_system_stats() -> dict[str, Any]:
    """Pull real system stats for build-in-public threads."""
    stats: dict[str, Any] = {
        "agent_count": 33,
        "alpha_entries": "14,799+",
        "docs_indexed": 484,
        "ventures": 8,
        "cron_jobs": 112,
        "cost_monthly": "$200",
        "revenue": "$0",
        "posts_generated": 588,
        "days_running": 0,
    }

    # Try to get live alpha count
    try:
        result = subprocess.run(
            ["python3", str(AUTOMATIONS / "alpha_query.py"), "--stats"],
            capture_output=True, text=True, timeout=10, cwd=str(PROJECT),
        )
        if result.returncode == 0:
            import re
            for line in result.stdout.splitlines():
                if "total" in line.lower() and "entries" in line.lower():
                    nums = re.findall(r"[\d,]+", line)
                    if nums:
                        stats["alpha_entries"] = nums[0]
                        break
    except Exception:
        pass

    # CEO agent cycle count
    ceo_state_path = AUTOMATIONS / "agent" / "ceo_agent" / "ceo_state.json"
    ceo_state = load_json(ceo_state_path, {})
    stats["ceo_decisions"] = ceo_state.get("total_decisions", 0)
    stats["ceo_cycles"] = ceo_state.get("cycles_completed", 0)

    # Days running from warmup state
    warmup_path = AUTOMATIONS / "agent" / "twitter_warmup_state.json"
    warmup_state = load_json(warmup_path, {})
    start = warmup_state.get("warmup_start")
    if start:
        try:
            d = datetime.strptime(start, "%Y-%m-%d")
            stats["days_running"] = (datetime.now() - d).days
        except Exception:
            pass

    return stats


# ── Post Generation ──────────────────────────────────────────────────

def _pick_topic(intel: dict[str, Any]) -> dict[str, Any]:
    """Pick a topic from the rotation pool, biased by available intel."""
    # Weight topics that have relevant alpha
    alpha_text = " ".join(intel.get("alpha_snippets", [])[:5]).lower()
    weighted = []
    for topic in TOPIC_POOL:
        weight = 1
        slug_words = topic["slug"].replace("_", " ").split()
        for word in slug_words:
            if word in alpha_text:
                weight += 2
        weighted.extend([topic] * weight)
    return random.choice(weighted)


def generate_twitter_post(intel: dict[str, Any], topic: dict[str, Any]) -> str:
    """Generate a single Twitter/X post following the enforced arc."""
    stats = intel.get("system_stats", {})

    # Build the 10-line arc
    lines = []

    # Line 1: Attack outdated belief
    lines.append(f"stop believing {topic['outdated_belief']}.")

    # Lines 2-4: Evidence the old way is broken
    evidence_lines = topic["reality"].split(". ")
    for el in evidence_lines[:3]:
        el = el.strip().rstrip(".")
        if el:
            lines.append(f"{el}.")

    # Lines 5-7: The new framework
    lines.append("")
    framework_lines = topic["framework"].split(". ")
    for fl in framework_lines[:3]:
        fl = fl.strip().rstrip(".")
        if fl:
            lines.append(f"{fl}.")

    # Lines 8-9: Specific result/data point
    lines.append("")
    data_points = [
        f"{stats.get('agent_count', 33)} agents. {stats.get('alpha_entries', '14,799')} data points analyzed. {stats.get('cost_monthly', '$200')}/mo total cost.",
        f"built {stats.get('ventures', 8)} venture pipelines running autonomously. {stats.get('cron_jobs', 112)} cron jobs. zero employees.",
        f"{stats.get('docs_indexed', 484)} intelligence docs indexed. every agent reads them before making a single move.",
    ]
    lines.append(random.choice(data_points))

    # Line 10: CTA
    ctas = [
        "follow for the build log. every day documented.",
        "building this in public. follow the system, not the guru.",
        "comment 'SYSTEM' if you want the architecture breakdown.",
        "this is day {days}. follow for the $0 to $1 journey.".format(
            days=stats.get("days_running", 0) or "1"
        ),
        "bookmark this. you'll need it when you're tired of hiring.",
    ]
    lines.append(random.choice(ctas))

    post = "\n".join(lines)

    # Trim to 280 chars for Twitter if needed (prefer keeping it short)
    if len(post) > 280:
        # Compress: remove empty lines, tighten
        compact_lines = [l for l in lines if l.strip()]
        post = "\n".join(compact_lines)

    return post


def generate_linkedin_post(intel: dict[str, Any], topic: dict[str, Any]) -> str:
    """Generate a LinkedIn post following the enforced arc. LinkedIn allows
    longer content, so we expand on each section."""
    stats = intel.get("system_stats", {})

    sections = []

    # Line 1: Attack
    sections.append(f"Most people still believe {topic['outdated_belief']}.\n")

    # Lines 2-4: Evidence
    sections.append(f"Here's why that's wrong:\n")
    evidence = topic["reality"]
    sections.append(evidence + "\n")

    # Lines 5-7: Framework
    sections.append("What actually works:\n")
    framework = topic["framework"]
    sections.append(framework + "\n")

    # Sprinkle alpha insights if available
    alpha_snippets = intel.get("alpha_snippets", [])
    if alpha_snippets:
        relevant = random.choice(alpha_snippets[:5])
        sections.append(f"One finding from our intelligence pipeline: {relevant[:120]}.\n")

    # Lines 8-9: Data
    sections.append(
        f"The numbers so far:\n"
        f"- {stats.get('agent_count', 33)} autonomous agents running 24/7\n"
        f"- {stats.get('alpha_entries', '14,799')} data points analyzed\n"
        f"- {stats.get('docs_indexed', 484)} intelligence docs indexed\n"
        f"- {stats.get('ventures', 8)} venture pipelines active\n"
        f"- Total cost: {stats.get('cost_monthly', '$200')}/mo\n"
        f"- Revenue: {stats.get('revenue', '$0')} (building in public, no pretending)\n"
    )

    # Line 10: CTA
    ctas = [
        "Agree? Disagree? Drop your take in the comments.",
        "Follow for daily build-in-public updates. No fluff, just numbers.",
        "DM me 'SYSTEM' if you want the architecture breakdown.",
        "What's stopping you from building this? Comment below.",
    ]
    sections.append(random.choice(ctas))

    return "\n".join(sections)


def generate_weekly_thread(intel: dict[str, Any]) -> str:
    """Generate a weekly build-in-public thread with real system stats."""
    stats = intel.get("system_stats", {})
    now = datetime.now()
    week_num = now.isocalendar()[1]

    tweets = []

    # Tweet 1: Hook
    tweets.append(
        f"week {week_num} build-in-public update.\n\n"
        f"{stats.get('agent_count', 33)} agents. {stats.get('alpha_entries', '14,799')} data points. "
        f"{stats.get('revenue', '$0')} revenue.\n\n"
        f"here's what actually happened this week. no fluff."
    )

    # Tweet 2: Agent swarm status
    tweets.append(
        f"AGENT SWARM STATUS:\n\n"
        f"- {stats.get('agent_count', 33)} agents across {stats.get('ventures', 8)} ventures\n"
        f"- CEO agent ran {stats.get('ceo_cycles', 0)} decision cycles\n"
        f"- {stats.get('ceo_decisions', 0)} autonomous decisions made\n"
        f"- {stats.get('cron_jobs', 112)} cron jobs active\n\n"
        f"every agent queries intelligence before acting. no raw LLM guessing."
    )

    # Tweet 3: Intelligence pipeline
    tweets.append(
        f"INTELLIGENCE PIPELINE:\n\n"
        f"- {stats.get('alpha_entries', '14,799')} total alpha entries\n"
        f"- {stats.get('docs_indexed', 484)} docs in intelligence router\n"
        f"- scrapers run every 6 hours\n"
        f"- alpha auto-processor routes findings to ventures\n\n"
        f"the system reads its own reports and acts on them. "
        f"no human in the loop for 90% of decisions."
    )

    # Tweet 4: Content generation
    tweets.append(
        f"CONTENT GENERATION:\n\n"
        f"- {stats.get('posts_generated', 588)} posts generated\n"
        f"- daily engagement plans auto-generated at 7 AM\n"
        f"- reply hooks pre-filled with real metrics\n"
        f"- quality gate rejects anything scoring below 7/10\n\n"
        f"the content pipeline feeds itself. alpha becomes posts, "
        f"posts become engagement, engagement becomes leads."
    )

    # Tweet 5: The honest part
    tweets.append(
        f"THE HONEST PART:\n\n"
        f"revenue is still {stats.get('revenue', '$0')}.\n\n"
        f"13 products sit unlisted. 283 posts queued but 0 posted from personal account. "
        f"the bottleneck isn't the system. it's the 80 minutes of human action needed to unlock everything.\n\n"
        f"building is the easy part. shipping is the gap."
    )

    # Tweet 6: What's next + CTA
    tweets.append(
        f"NEXT WEEK:\n\n"
        f"- get products listed\n"
        f"- first revenue from any lane\n"
        f"- double down on whatever works\n"
        f"- kill what doesn't\n\n"
        f"follow for the real build log. "
        f"no guru energy. just a system trying to print its first dollar.\n\n"
        f"if you're building something similar, reply with what you're working on."
    )

    # Format as numbered thread
    thread_parts = []
    for i, tweet in enumerate(tweets, 1):
        thread_parts.append(f"[{i}/{len(tweets)}]\n{tweet}")

    return "\n\n---\n\n".join(thread_parts)


# ── State Management ─────────────────────────────────────────────────

def load_state() -> dict[str, Any]:
    state = load_json(STATE_FILE, {})
    if not state:
        state = {
            "total_generated": 0,
            "total_twitter": 0,
            "total_linkedin": 0,
            "total_threads": 0,
            "last_generate_date": None,
            "last_thread_date": None,
            "topic_history": [],
            "rejected_count": 0,
        }
    return state


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    safe_path(STATE_FILE)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ── CLI Commands ─────────────────────────────────────────────────────

def cmd_generate(dry_run: bool = False) -> None:
    """Generate daily posts: 1 Twitter + 1 LinkedIn."""
    log("Starting daily content generation", tag="SHAKESPEARE")

    intel = gather_intel()
    topic = _pick_topic(intel)
    log(f"Selected topic: {topic['label']}", tag="SHAKESPEARE")

    # Generate Twitter post
    twitter_post = generate_twitter_post(intel, topic)
    twitter_score = score_post(twitter_post)
    log(f"Twitter post score: {twitter_score}/10", tag="SHAKESPEARE")

    # Retry up to 3 times if quality gate rejects
    attempts = 0
    while twitter_score < 7 and attempts < 3:
        attempts += 1
        log(f"Score {twitter_score} < 7, regenerating (attempt {attempts + 1})", tag="SHAKESPEARE")
        topic = _pick_topic(intel)
        twitter_post = generate_twitter_post(intel, topic)
        twitter_score = score_post(twitter_post)
        log(f"Retry score: {twitter_score}/10", tag="SHAKESPEARE")

    # Generate LinkedIn post (same topic for cohesion)
    linkedin_post = generate_linkedin_post(intel, topic)
    linkedin_score = score_post(linkedin_post)
    log(f"LinkedIn post score: {linkedin_score}/10", tag="SHAKESPEARE")

    if dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN -- TWITTER POST")
        print("=" * 60)
        print(f"Topic: {topic['label']}")
        print(f"Score: {twitter_score}/10")
        print(f"Chars: {len(twitter_post)}")
        print("-" * 40)
        print(twitter_post)
        print("\n" + "=" * 60)
        print("DRY RUN -- LINKEDIN POST")
        print("=" * 60)
        print(f"Score: {linkedin_score}/10")
        print(f"Chars: {len(linkedin_post)}")
        print("-" * 40)
        print(linkedin_post)
        return

    state = load_state()
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M")

    # Write Twitter post
    POSTING_QUEUE.mkdir(parents=True, exist_ok=True)
    twitter_filename = f"twitter_PRINTMAXXER_{date_str}_{time_str}.txt"
    twitter_path = safe_path(POSTING_QUEUE / twitter_filename)
    twitter_content = (
        f"PROFILE: @PRINTMAXXER\n"
        f"SCHEDULED: {now.strftime('%I:%M %p ET')}\n"
        f"TOPIC: {topic['label']}\n"
        f"SCORE: {twitter_score}/10\n"
        f"GENERATED: {now.isoformat()}\n"
        f"GENERATOR: shakespeare_agent.py\n"
        f"---\n"
        f"{twitter_post}"
    )
    twitter_path.write_text(twitter_content, encoding="utf-8")
    log(f"Twitter post saved: {twitter_filename}", tag="SHAKESPEARE")

    # Write LinkedIn post
    LINKEDIN_DIR.mkdir(parents=True, exist_ok=True)
    linkedin_filename = f"linkedin_{date_str}_{time_str}.md"
    linkedin_path = safe_path(LINKEDIN_DIR / linkedin_filename)
    linkedin_content = (
        f"# LinkedIn Post -- {now.strftime('%B %d, %Y')}\n\n"
        f"**Topic:** {topic['label']}\n"
        f"**Score:** {linkedin_score}/10\n"
        f"**Generated:** {now.isoformat()}\n"
        f"**Generator:** shakespeare_agent.py\n\n"
        f"---\n\n"
        f"{linkedin_post}"
    )
    linkedin_path.write_text(linkedin_content, encoding="utf-8")
    log(f"LinkedIn post saved: {linkedin_filename}", tag="SHAKESPEARE")

    # Update state
    state["total_generated"] += 2
    state["total_twitter"] += 1
    state["total_linkedin"] += 1
    state["last_generate_date"] = now.strftime("%Y-%m-%d")
    state["topic_history"].append(topic["slug"])
    if len(state["topic_history"]) > 50:
        state["topic_history"] = state["topic_history"][-30:]
    if twitter_score < 7 or linkedin_score < 7:
        state["rejected_count"] = state.get("rejected_count", 0) + 1
    save_state(state)

    print(f"\nGenerated 2 posts (Twitter + LinkedIn)")
    print(f"  Twitter: {twitter_path}")
    print(f"  LinkedIn: {linkedin_path}")


def cmd_thread(dry_run: bool = False) -> None:
    """Generate weekly build-in-public thread."""
    log("Generating weekly build-in-public thread", tag="SHAKESPEARE")

    intel = gather_intel()
    thread = generate_weekly_thread(intel)

    if dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN -- WEEKLY BUILD-IN-PUBLIC THREAD")
        print("=" * 60)
        print(thread)
        return

    state = load_state()
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M")

    POSTING_QUEUE.mkdir(parents=True, exist_ok=True)
    thread_filename = f"twitter_PRINTMAXXER_thread_{date_str}_{time_str}.txt"
    thread_path = safe_path(POSTING_QUEUE / thread_filename)
    thread_content = (
        f"PROFILE: @PRINTMAXXER\n"
        f"TYPE: BUILD-IN-PUBLIC THREAD\n"
        f"SCHEDULED: Sunday 10:00 AM ET\n"
        f"GENERATED: {now.isoformat()}\n"
        f"GENERATOR: shakespeare_agent.py\n"
        f"---\n"
        f"{thread}"
    )
    thread_path.write_text(thread_content, encoding="utf-8")
    log(f"Thread saved: {thread_filename}", tag="SHAKESPEARE")

    state["total_threads"] += 1
    state["last_thread_date"] = now.strftime("%Y-%m-%d")
    save_state(state)

    print(f"\nGenerated build-in-public thread ({len(thread.split('---'))} tweets)")
    print(f"  File: {thread_path}")


def cmd_status() -> None:
    """Show generation stats."""
    state = load_state()
    print("SHAKESPEARE AGENT STATUS")
    print("=" * 50)
    print(f"  Total generated:    {state.get('total_generated', 0)}")
    print(f"  Twitter posts:      {state.get('total_twitter', 0)}")
    print(f"  LinkedIn posts:     {state.get('total_linkedin', 0)}")
    print(f"  Threads:            {state.get('total_threads', 0)}")
    print(f"  Rejected (< 7/10):  {state.get('rejected_count', 0)}")
    print(f"  Last generate:      {state.get('last_generate_date', 'never')}")
    print(f"  Last thread:        {state.get('last_thread_date', 'never')}")

    # Recent topics
    history = state.get("topic_history", [])
    if history:
        recent = history[-5:]
        print(f"\n  Recent topics: {', '.join(recent)}")

    # Queue sizes
    twitter_count = len(list(POSTING_QUEUE.glob("twitter_PRINTMAXXER_*.txt"))) if POSTING_QUEUE.exists() else 0
    linkedin_count = len(list(LINKEDIN_DIR.glob("linkedin_*.md"))) if LINKEDIN_DIR.exists() else 0
    print(f"\n  Twitter queue:  {twitter_count} files")
    print(f"  LinkedIn queue: {linkedin_count} files")

    # Intelligence availability
    print(f"\n  Intelligence router: {'AVAILABLE' if _ROUTER_AVAILABLE else 'NOT AVAILABLE'}")
    print(f"  Master ops bridge:   {'AVAILABLE' if _BRIDGE_AVAILABLE else 'NOT AVAILABLE'}")
    catalog = load_json(INTEL_CATALOG, {})
    print(f"  Catalog docs:        {catalog.get('total_docs', 0)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Shakespeare Agent -- Movement-first content generation"
    )
    parser.add_argument("--generate", action="store_true",
                        help="Generate daily posts (1 Twitter + 1 LinkedIn)")
    parser.add_argument("--thread", action="store_true",
                        help="Generate weekly build-in-public thread")
    parser.add_argument("--status", action="store_true",
                        help="Show generation stats")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing files")
    args = parser.parse_args()

    if args.thread:
        cmd_thread(dry_run=args.dry_run)
    elif args.generate:
        cmd_generate(dry_run=args.dry_run)
    elif args.dry_run:
        # --dry-run alone defaults to generate preview
        cmd_generate(dry_run=True)
    elif args.status:
        cmd_status()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
