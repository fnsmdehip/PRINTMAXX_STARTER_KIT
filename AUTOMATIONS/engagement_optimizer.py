#!/usr/bin/env python3
"""
PRINTMAXX Engagement Optimizer
=================================
Analyzes content performance, A/B tests hook styles, prevents algo bans via
rate limit tracking, and generates "what to post next" recommendations.

Reads:
    - LEDGER/DISTRIBUTION_TRACKER.csv (distribution history)
    - LEDGER/PLATFORM_ACTIVITY_LOG.csv (from algo_ban_prevention.py)
    - CONTENT/social/auto_generated/ (content inventory)
    - AUTOMATIONS/algo_ban_prevention.py (rate limit constants)

Usage:
    python3 AUTOMATIONS/engagement_optimizer.py --analyze           # analyze content performance
    python3 AUTOMATIONS/engagement_optimizer.py --recommend         # what to post next
    python3 AUTOMATIONS/engagement_optimizer.py --rate-check        # check rate limit safety
    python3 AUTOMATIONS/engagement_optimizer.py --schedule-week     # generate full week schedule
    python3 AUTOMATIONS/engagement_optimizer.py --ab-report         # A/B test hook analysis
    python3 AUTOMATIONS/engagement_optimizer.py --freshness         # content freshness audit

Cron:
    0 7 * * 1 cd $BASE && python3 AUTOMATIONS/engagement_optimizer.py --schedule-week >> AUTOMATIONS/logs/engagement.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_TRACKER = PROJECT_ROOT / "LEDGER" / "DISTRIBUTION_TRACKER.csv"
ACTIVITY_LOG = PROJECT_ROOT / "LEDGER" / "PLATFORM_ACTIVITY_LOG.csv"
CONTENT_DIR = PROJECT_ROOT / "CONTENT" / "social" / "auto_generated"
DIST_DIR = PROJECT_ROOT / "CONTENT" / "social" / "distribution"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
ENGAGEMENT_DATA = PROJECT_ROOT / "LEDGER" / "ENGAGEMENT_METRICS.csv"
AB_TEST_LOG = PROJECT_ROOT / "LEDGER" / "AB_TEST_LOG.csv"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] engagement_optimizer: {msg}"
    print(line, file=sys.stderr)
    safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_DIR / "engagement.log"), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Rate limits (mirrored from algo_ban_prevention.py)
# ---------------------------------------------------------------------------
RATE_LIMITS = {
    "twitter": {
        "posts_per_day_safe": 25,
        "posts_per_day_aggressive": 50,
        "posts_per_day_ban": 100,
        "min_spacing_min": 30,
        "warmup_week1": 5,
        "warmup_week2": 10,
        "warmup_week3": 15,
        "warmup_week4_plus": 25,
    },
    "linkedin": {
        "posts_per_day_safe": 2,
        "posts_per_day_aggressive": 3,
        "posts_per_day_ban": 5,
        "min_spacing_min": 240,
    },
    "reddit": {
        "posts_per_day_safe": 3,
        "posts_per_day_aggressive": 5,
        "posts_per_day_ban": 10,
        "self_promo_max_pct": 10,
        "min_spacing_min": 120,
    },
    "instagram": {
        "posts_per_day_safe": 3,
        "posts_per_day_aggressive": 5,
        "posts_per_day_ban": 10,
        "min_spacing_min": 60,
    },
    "tiktok": {
        "posts_per_day_safe": 3,
        "posts_per_day_aggressive": 5,
        "posts_per_day_ban": 10,
        "min_spacing_min": 60,
    },
    "substack": {
        "posts_per_day_safe": 2,
        "posts_per_day_aggressive": 3,
        "posts_per_day_ban": 5,
        "min_spacing_min": 360,
    },
}

# Account-to-platform mapping
ACCOUNTS = {
    "PRINTMAXXER": ["twitter", "linkedin", "reddit", "substack"],
    "repscheme": ["twitter", "reddit"],
    "drifthour": ["twitter"],
    "voidpilled": ["twitter", "reddit"],
    "selahmoments": ["twitter"],
}

# Optimal posting windows (hour UTC -> engagement multiplier)
OPTIMAL_HOURS = {
    "twitter": {
        8: 1.3, 9: 1.2, 10: 1.1, 11: 1.0, 12: 1.4, 13: 1.2,
        14: 1.0, 15: 1.1, 16: 1.0, 17: 1.3, 18: 1.2, 19: 1.4,
        20: 1.3, 21: 1.5,
    },
    "linkedin": {
        7: 1.3, 8: 1.5, 9: 1.2, 10: 1.0, 11: 0.9, 12: 1.3,
        13: 1.0, 14: 0.8, 15: 0.7, 16: 0.8, 17: 1.2,
    },
    "reddit": {
        8: 1.0, 9: 1.3, 10: 1.2, 11: 1.1, 12: 1.0, 13: 1.3,
        14: 1.1, 15: 1.0, 16: 1.2, 17: 1.4,
    },
    "substack": {
        7: 1.0, 8: 1.3, 9: 1.2, 10: 1.4, 11: 1.1, 14: 1.2,
    },
}

# Hook style categories for A/B testing
HOOK_STYLES = {
    "consequence_first": {
        "pattern": r'^(i |the |this |that |just |stop )',
        "description": "leads with result or consequence",
        "examples": ["i tested this and revenue doubled", "the results were wild"],
    },
    "question_hook": {
        "pattern": r'^(why |how |what |are you |do you |have you )',
        "description": "opens with a question",
        "examples": ["why is nobody talking about this?"],
    },
    "number_lead": {
        "pattern": r'^(\d+|[$]\d)',
        "description": "leads with a specific number",
        "examples": ["47 apps tested. 3 actually worked.", "$2.5k in one day"],
    },
    "imperative": {
        "pattern": r'^(stop |start |build |test |use |try |set up |automate )',
        "description": "direct command/imperative",
        "examples": ["stop overthinking this", "build it in one session"],
    },
    "story_open": {
        "pattern": r'^(last |yesterday |spent |been |found |discovered )',
        "description": "narrative opening",
        "examples": ["last week I tested this framework", "found something wild"],
    },
    "contrast": {
        "pattern": r'(not|but|however|instead|while|most people)',
        "description": "contrast or opposition pattern",
        "examples": ["most people do X. the play is Y.", "everyone says A but B"],
    },
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_distribution_tracker() -> list[dict]:
    """Load distribution tracker data."""
    if not DIST_TRACKER.exists():
        return []
    with open(DIST_TRACKER, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_activity_log() -> list[dict]:
    """Load platform activity log (from algo_ban_prevention)."""
    if not ACTIVITY_LOG.exists():
        return []
    with open(ACTIVITY_LOG, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_engagement_metrics() -> list[dict]:
    """Load engagement metrics if available."""
    if not ENGAGEMENT_DATA.exists():
        return []
    with open(ENGAGEMENT_DATA, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_content_inventory() -> list[dict]:
    """Scan content inventory for available posts."""
    items = []
    if not CONTENT_DIR.exists():
        return items

    for f in sorted(CONTENT_DIR.iterdir()):
        if f.suffix == ".csv":
            try:
                with open(f, "r", newline="", encoding="utf-8") as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        row["_file"] = f.name
                        row["_mtime"] = datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                        items.append(row)
            except Exception:
                pass
        elif f.suffix == ".json" and "manifest" not in f.name:
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                data["_file"] = f.name
                data["_mtime"] = datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                items.append(data)
            except Exception:
                pass

    return items


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------
def classify_hook_style(text: str) -> str:
    """Classify what hook style a piece of content uses."""
    text_lower = text.lower().strip()
    for style_name, style_info in HOOK_STYLES.items():
        if re.match(style_info["pattern"], text_lower):
            return style_name
    return "other"


def analyze_content_performance(tracker: list[dict], metrics: list[dict]) -> dict:
    """Analyze which content formats and hooks perform best."""
    analysis = {
        "total_distributed": len(tracker),
        "by_platform": defaultdict(lambda: {"total": 0, "posted": 0}),
        "by_account": defaultdict(lambda: {"total": 0, "posted": 0}),
        "by_hook_style": defaultdict(lambda: {"count": 0, "posted": 0}),
        "by_format": defaultdict(lambda: {"count": 0}),
        "freshness": {"fresh": 0, "stale": 0, "expired": 0},
        "posting_velocity": {},
    }

    now = datetime.now()

    for entry in tracker:
        platform = entry.get("platform", "unknown")
        account = entry.get("account", "unknown")
        status = entry.get("status", "UNKNOWN")
        text = entry.get("content_text", entry.get("formatted_text", ""))

        analysis["by_platform"][platform]["total"] += 1
        analysis["by_account"][account]["total"] += 1

        if status == "POSTED":
            analysis["by_platform"][platform]["posted"] += 1
            analysis["by_account"][account]["posted"] += 1

        # Hook style analysis
        if text:
            hook = classify_hook_style(text)
            analysis["by_hook_style"][hook]["count"] += 1
            if status == "POSTED":
                analysis["by_hook_style"][hook]["posted"] += 1

        # Content format
        fmt = entry.get("notes", "")
        fmt_match = re.search(r'format:(\S+)', fmt)
        if fmt_match:
            analysis["by_format"][fmt_match.group(1)]["count"] += 1

        # Freshness check
        created = entry.get("created_at", "")
        if created:
            try:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00").replace("+00:00", ""))
                age_days = (now - created_dt).days
                if age_days <= 3:
                    analysis["freshness"]["fresh"] += 1
                elif age_days <= 7:
                    analysis["freshness"]["stale"] += 1
                else:
                    analysis["freshness"]["expired"] += 1
            except (ValueError, TypeError):
                pass

    # Posting velocity (posts per day over last 7 days)
    for entry in tracker:
        posted_at = entry.get("posted_at", entry.get("scheduled_time", ""))
        if not posted_at:
            continue
        try:
            date_str = posted_at[:10]
            platform = entry.get("platform", "unknown")
            key = f"{date_str}|{platform}"
            analysis["posting_velocity"][key] = analysis["posting_velocity"].get(key, 0) + 1
        except (ValueError, IndexError):
            pass

    # If engagement metrics exist, correlate
    if metrics:
        engagement_by_hook = defaultdict(list)
        for m in metrics:
            text = m.get("text", m.get("content_text", ""))
            engagement = 0
            for field in ("likes", "impressions", "clicks", "retweets", "replies"):
                val = m.get(field, "0")
                try:
                    engagement += int(str(val).replace(",", ""))
                except ValueError:
                    pass
            if text:
                hook = classify_hook_style(text)
                engagement_by_hook[hook].append(engagement)

        analysis["engagement_by_hook"] = {
            k: {
                "avg": sum(v) / len(v) if v else 0,
                "max": max(v) if v else 0,
                "count": len(v),
            }
            for k, v in engagement_by_hook.items()
        }

    return dict(analysis)


def check_rate_limits(tracker: list[dict], activity: list[dict]) -> dict:
    """Check current posting rates against safe limits."""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Count today's activity
    today_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    # From distribution tracker
    for entry in tracker:
        posted = entry.get("posted_at", entry.get("scheduled_time", ""))
        if posted and posted[:10] == today:
            platform = entry.get("platform", "unknown")
            account = entry.get("account", "unknown").lstrip("@")
            today_counts[account][platform] += 1

    # From activity log
    for entry in activity:
        ts = entry.get("timestamp", entry.get("created_at", ""))
        if ts and ts[:10] == today:
            platform = entry.get("platform", "unknown")
            account = entry.get("account", "unknown").lstrip("@")
            action = entry.get("action", entry.get("action_type", "post"))
            if action in ("post", "tweet", "publish"):
                today_counts[account][platform] += 1

    # Compare against limits
    results = {
        "date": today,
        "accounts": {},
        "warnings": [],
        "blocks": [],
        "overall_safe": True,
    }

    for account, platforms in ACCOUNTS.items():
        results["accounts"][account] = {}
        for platform in platforms:
            current = today_counts.get(account, {}).get(platform, 0)
            limits = RATE_LIMITS.get(platform, {})
            safe_limit = limits.get("posts_per_day_safe", 10)
            aggressive_limit = limits.get("posts_per_day_aggressive", 20)
            ban_limit = limits.get("posts_per_day_ban", 50)

            status = "SAFE"
            remaining = safe_limit - current

            if current >= ban_limit:
                status = "BLOCKED"
                results["blocks"].append(f"{account}/{platform}: {current}/{ban_limit} (BAN RISK)")
                results["overall_safe"] = False
                remaining = 0
            elif current >= aggressive_limit:
                status = "AGGRESSIVE"
                results["warnings"].append(f"{account}/{platform}: {current}/{aggressive_limit}")
                results["overall_safe"] = False
                remaining = ban_limit - current
            elif current >= safe_limit:
                status = "WARN"
                results["warnings"].append(f"{account}/{platform}: {current}/{safe_limit}")
                remaining = aggressive_limit - current

            results["accounts"][account][platform] = {
                "current": current,
                "safe_limit": safe_limit,
                "aggressive_limit": aggressive_limit,
                "ban_limit": ban_limit,
                "remaining_safe": max(0, safe_limit - current),
                "remaining_aggressive": max(0, aggressive_limit - current),
                "status": status,
            }

    return results


def generate_recommendations(
    tracker: list[dict],
    analysis: dict,
    rate_check: dict,
    inventory: list[dict],
) -> list[dict]:
    """Generate 'what to post next' recommendations."""
    recommendations = []
    now = datetime.now()

    # 1. Platform gap analysis: which platforms have capacity?
    for account, platforms in ACCOUNTS.items():
        for platform in platforms:
            rate_info = rate_check.get("accounts", {}).get(account, {}).get(platform, {})
            remaining = rate_info.get("remaining_safe", 0)
            if remaining > 0:
                # Find unposted content for this platform/account
                unposted = [
                    e for e in tracker
                    if e.get("platform") == platform
                    and e.get("account", "").lstrip("@") == account
                    and e.get("status") in ("PENDING", "READY", "SCHEDULED")
                ]

                if unposted:
                    recommendations.append({
                        "priority": "HIGH",
                        "action": f"POST to {platform}",
                        "account": account,
                        "platform": platform,
                        "detail": f"{len(unposted)} items ready, {remaining} slots remaining today",
                        "content_preview": unposted[0].get("formatted_text", unposted[0].get("content_text", ""))[:80],
                    })
                elif remaining >= 3:
                    recommendations.append({
                        "priority": "MEDIUM",
                        "action": f"GENERATE content for {platform}",
                        "account": account,
                        "platform": platform,
                        "detail": f"No content queued but {remaining} slots available. Run content_factory.py.",
                    })

    # 2. Content freshness: warn if content is getting stale
    freshness = analysis.get("freshness", {})
    if freshness.get("expired", 0) > freshness.get("fresh", 0):
        recommendations.append({
            "priority": "HIGH",
            "action": "GENERATE fresh content",
            "account": "all",
            "platform": "all",
            "detail": f"{freshness['expired']} expired items vs {freshness['fresh']} fresh. Run batch-alpha or --from-session.",
        })

    # 3. Hook style diversification
    hook_counts = analysis.get("by_hook_style", {})
    if hook_counts:
        total_hooks = sum(h.get("count", 0) for h in hook_counts.values() if isinstance(h, dict))
        if total_hooks > 10:
            dominant = max(hook_counts.items(), key=lambda x: x[1].get("count", 0) if isinstance(x[1], dict) else 0)
            dominant_pct = (dominant[1].get("count", 0) / total_hooks * 100) if total_hooks > 0 and isinstance(dominant[1], dict) else 0
            if dominant_pct > 60:
                underused = [
                    name for name, info in hook_counts.items()
                    if isinstance(info, dict) and info.get("count", 0) < total_hooks * 0.1
                    and name != "other"
                ]
                if underused:
                    recommendations.append({
                        "priority": "MEDIUM",
                        "action": "DIVERSIFY hook styles",
                        "account": "all",
                        "platform": "twitter",
                        "detail": f"'{dominant[0]}' is {dominant_pct:.0f}% of hooks. Try: {', '.join(underused[:3])}",
                    })

    # 4. Engagement-based hook optimization
    engagement_data = analysis.get("engagement_by_hook", {})
    if engagement_data:
        best_hook = max(engagement_data.items(), key=lambda x: x[1].get("avg", 0))
        if best_hook[1].get("avg", 0) > 0:
            recommendations.append({
                "priority": "HIGH",
                "action": f"USE MORE '{best_hook[0]}' hooks",
                "account": "all",
                "platform": "twitter",
                "detail": f"Avg engagement: {best_hook[1]['avg']:.0f} (best performer). Double down.",
            })

    # 5. Cross-platform repurposing
    twitter_only = sum(
        1 for e in tracker
        if e.get("platform") == "twitter"
        and e.get("status") == "POSTED"
    )
    linkedin_count = sum(1 for e in tracker if e.get("platform") == "linkedin")
    reddit_count = sum(1 for e in tracker if e.get("platform") == "reddit")

    if twitter_only > 10 and linkedin_count < twitter_only * 0.1:
        recommendations.append({
            "priority": "MEDIUM",
            "action": "REPURPOSE Twitter content for LinkedIn",
            "account": "PRINTMAXXER",
            "platform": "linkedin",
            "detail": f"{twitter_only} Twitter posts but only {linkedin_count} LinkedIn. Repurpose top performers.",
        })

    if twitter_only > 10 and reddit_count < twitter_only * 0.05:
        recommendations.append({
            "priority": "MEDIUM",
            "action": "REPURPOSE for Reddit",
            "account": "PRINTMAXXER",
            "platform": "reddit",
            "detail": f"Reddit underserved. Expand Twitter threads into Reddit posts.",
        })

    # 6. Audience overlap prevention
    posted_by_account_today = defaultdict(int)
    today = now.strftime("%Y-%m-%d")
    for e in tracker:
        posted = e.get("posted_at", e.get("scheduled_time", ""))
        if posted and posted[:10] == today:
            acct = e.get("account", "").lstrip("@")
            posted_by_account_today[acct] += 1

    total_today = sum(posted_by_account_today.values())
    if total_today > 15:
        recommendations.append({
            "priority": "WARN",
            "action": "REDUCE posting volume today",
            "account": "all",
            "platform": "all",
            "detail": f"{total_today} total posts today across all accounts. Risk of audience fatigue/overlap.",
        })

    # 7. Trending topic injection (if no posts about trending recently)
    recommendations.append({
        "priority": "LOW",
        "action": "CHECK trending topics",
        "account": "PRINTMAXXER",
        "platform": "twitter",
        "detail": "Run content_trend_pipeline.py --scan to find fresh viral angles.",
    })

    # Sort by priority
    priority_order = {"HIGH": 0, "MEDIUM": 1, "WARN": 2, "LOW": 3}
    recommendations.sort(key=lambda r: priority_order.get(r.get("priority", "LOW"), 3))

    return recommendations


# ---------------------------------------------------------------------------
# A/B Testing
# ---------------------------------------------------------------------------
AB_FIELDS = [
    "test_id", "variant_a_text", "variant_b_text",
    "variant_a_hook", "variant_b_hook",
    "variant_a_engagement", "variant_b_engagement",
    "winner", "platform", "account", "created_at", "resolved_at",
]


def generate_ab_tests(inventory: list[dict]) -> list[dict]:
    """Generate A/B test pairs from existing content inventory."""
    tests = []

    # Group content by topic/source
    by_topic = defaultdict(list)
    for item in inventory:
        text = item.get("tweet_text", item.get("draft", ""))
        if not text or len(text) < 20:
            continue
        topic_key = item.get("source_topic", item.get("source_alpha_id", "general"))
        by_topic[topic_key].append(text)

    # Create pairs with different hook styles
    test_id = 1
    for topic, texts in by_topic.items():
        if len(texts) < 2:
            continue

        # Pick two texts with different hook styles
        classified = [(t, classify_hook_style(t)) for t in texts]
        styles_seen = set()
        pair = []
        for t, style in classified:
            if style not in styles_seen and len(pair) < 2:
                pair.append((t, style))
                styles_seen.add(style)

        if len(pair) == 2:
            tests.append({
                "test_id": f"AB{test_id:03d}",
                "variant_a_text": pair[0][0][:280],
                "variant_b_text": pair[1][0][:280],
                "variant_a_hook": pair[0][1],
                "variant_b_hook": pair[1][1],
                "variant_a_engagement": "",
                "variant_b_engagement": "",
                "winner": "",
                "platform": "twitter",
                "account": "@PRINTMAXXER",
                "created_at": datetime.now().isoformat(),
                "resolved_at": "",
            })
            test_id += 1

    return tests[:20]  # Max 20 tests at a time


def save_ab_tests(tests: list[dict]) -> None:
    """Save A/B test log."""
    safe_path(AB_TEST_LOG.parent).mkdir(parents=True, exist_ok=True)

    existing = []
    if AB_TEST_LOG.exists():
        with open(AB_TEST_LOG, "r", newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

    all_tests = existing + tests
    with open(safe_path(AB_TEST_LOG), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=AB_FIELDS)
        writer.writeheader()
        writer.writerows(all_tests)


# ---------------------------------------------------------------------------
# Weekly schedule generator
# ---------------------------------------------------------------------------
def generate_weekly_schedule(
    tracker: list[dict],
    rate_check: dict,
    inventory: list[dict],
) -> dict:
    """Generate a full week posting schedule."""
    schedule = {
        "generated_at": datetime.now().isoformat(),
        "week_start": datetime.now().strftime("%Y-%m-%d"),
        "week_end": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
        "days": {},
        "totals": defaultdict(int),
    }

    for day_offset in range(7):
        day = datetime.now() + timedelta(days=day_offset)
        day_str = day.strftime("%Y-%m-%d")
        day_name = day.strftime("%A")
        schedule["days"][day_str] = {
            "day_name": day_name,
            "slots": [],
        }

        for account, platforms in ACCOUNTS.items():
            for platform in platforms:
                limits = RATE_LIMITS.get(platform, {})
                safe_limit = limits.get("posts_per_day_safe", 5)
                optimal = OPTIMAL_HOURS.get(platform, {})

                # Determine daily quota
                # Weekends: reduce by 30% for natural patterns
                if day_name in ("Saturday", "Sunday"):
                    daily_quota = max(1, int(safe_limit * 0.7))
                else:
                    daily_quota = safe_limit

                # Per-account budget
                from distribution_engine import ACCOUNT_DAILY_BUDGET
                acct_budget = ACCOUNT_DAILY_BUDGET.get(account, {}).get(platform, daily_quota)
                effective_quota = min(daily_quota, acct_budget)

                # Pick optimal hours
                if optimal:
                    sorted_hours = sorted(optimal.items(), key=lambda x: x[1], reverse=True)
                    best_hours = [h for h, _ in sorted_hours[:effective_quota]]
                else:
                    best_hours = [9, 12, 17][:effective_quota]

                for hour in best_hours[:effective_quota]:
                    jitter = random.randint(0, 25)
                    slot_time = f"{hour:02d}:{jitter:02d}"
                    schedule["days"][day_str]["slots"].append({
                        "time": slot_time,
                        "account": account,
                        "platform": platform,
                        "status": "PLANNED",
                    })
                    schedule["totals"][f"{account}_{platform}"] += 1

    return schedule


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------
def cmd_analyze() -> None:
    """Analyze content performance."""
    tracker = load_distribution_tracker()
    metrics = load_engagement_metrics()
    analysis = analyze_content_performance(tracker, metrics)

    print("\n--- Content Performance Analysis ---\n")
    print(f"  Total distributed: {analysis['total_distributed']}")

    print("\n  By platform:")
    for platform, info in sorted(analysis["by_platform"].items()):
        if isinstance(info, dict):
            print(f"    {platform}: {info['total']} total, {info['posted']} posted")

    print("\n  By account:")
    for account, info in sorted(analysis["by_account"].items()):
        if isinstance(info, dict):
            print(f"    {account}: {info['total']} total, {info['posted']} posted")

    print("\n  By hook style:")
    for style, info in sorted(analysis["by_hook_style"].items()):
        if isinstance(info, dict):
            print(f"    {style}: {info['count']} ({info.get('posted', 0)} posted)")

    print(f"\n  Content freshness:")
    freshness = analysis.get("freshness", {})
    print(f"    Fresh (0-3 days): {freshness.get('fresh', 0)}")
    print(f"    Stale (4-7 days): {freshness.get('stale', 0)}")
    print(f"    Expired (7+ days): {freshness.get('expired', 0)}")

    if analysis.get("engagement_by_hook"):
        print("\n  Engagement by hook style:")
        for style, data in sorted(
            analysis["engagement_by_hook"].items(),
            key=lambda x: x[1].get("avg", 0),
            reverse=True,
        ):
            print(f"    {style}: avg={data['avg']:.0f} max={data['max']} (n={data['count']})")

    # Posting velocity
    velocity = analysis.get("posting_velocity", {})
    if velocity:
        print("\n  Recent posting velocity (last 7 days):")
        recent = sorted(velocity.items(), reverse=True)[:7]
        for key, count in recent:
            date, platform = key.split("|") if "|" in key else (key, "unknown")
            print(f"    {date} {platform}: {count} posts")


def cmd_recommend() -> None:
    """Generate recommendations."""
    tracker = load_distribution_tracker()
    metrics = load_engagement_metrics()
    activity = load_activity_log()
    inventory = load_content_inventory()

    analysis = analyze_content_performance(tracker, metrics)
    rate_check = check_rate_limits(tracker, activity)
    recommendations = generate_recommendations(tracker, analysis, rate_check, inventory)

    print("\n--- What to Post Next ---\n")

    if not recommendations:
        print("  No specific recommendations. Everything looks balanced.")
        return

    for i, rec in enumerate(recommendations, 1):
        priority = rec.get("priority", "LOW")
        action = rec.get("action", "")
        account = rec.get("account", "")
        platform = rec.get("platform", "")
        detail = rec.get("detail", "")
        preview = rec.get("content_preview", "")

        marker = {"HIGH": ">>", "MEDIUM": ">", "WARN": "!!", "LOW": "  "}.get(priority, "  ")
        print(f"  {marker} [{priority}] {action}")
        print(f"     Account: {account} | Platform: {platform}")
        print(f"     {detail}")
        if preview:
            print(f"     Preview: {preview[:60]}...")
        print()


def cmd_rate_check() -> None:
    """Check rate limit safety."""
    tracker = load_distribution_tracker()
    activity = load_activity_log()
    results = check_rate_limits(tracker, activity)

    print(f"\n--- Rate Limit Check ({results['date']}) ---\n")

    if results["overall_safe"]:
        print("  ALL CLEAR: within safe limits across all platforms.\n")
    else:
        print("  WARNING: some limits exceeded.\n")

    for account, platforms in results["accounts"].items():
        print(f"  {account}:")
        for platform, info in platforms.items():
            status = info["status"]
            current = info["current"]
            safe = info["safe_limit"]
            remaining = info["remaining_safe"]
            indicator = {
                "SAFE": "  ",
                "WARN": "* ",
                "AGGRESSIVE": "**",
                "BLOCKED": "XX",
            }.get(status, "  ")
            print(f"    {indicator} {platform}: {current}/{safe} ({remaining} remaining) [{status}]")
        print()

    if results["warnings"]:
        print("  Warnings:")
        for w in results["warnings"]:
            print(f"    - {w}")

    if results["blocks"]:
        print("\n  BLOCKS (stop posting immediately):")
        for b in results["blocks"]:
            print(f"    - {b}")


def cmd_schedule_week() -> None:
    """Generate full week schedule."""
    tracker = load_distribution_tracker()
    activity = load_activity_log()
    inventory = load_content_inventory()
    rate_check = check_rate_limits(tracker, activity)

    try:
        schedule = generate_weekly_schedule(tracker, rate_check, inventory)
    except ImportError:
        # Fallback if distribution_engine not importable
        schedule = {
            "generated_at": datetime.now().isoformat(),
            "week_start": datetime.now().strftime("%Y-%m-%d"),
            "week_end": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
            "days": {},
            "totals": defaultdict(int),
        }
        for day_offset in range(7):
            day = datetime.now() + timedelta(days=day_offset)
            day_str = day.strftime("%Y-%m-%d")
            schedule["days"][day_str] = {"day_name": day.strftime("%A"), "slots": []}
            for account, platforms in ACCOUNTS.items():
                for platform in platforms:
                    safe = RATE_LIMITS.get(platform, {}).get("posts_per_day_safe", 3)
                    quota = min(safe, 5)
                    for h in [9, 12, 17][:quota]:
                        schedule["days"][day_str]["slots"].append({
                            "time": f"{h:02d}:{random.randint(0, 30):02d}",
                            "account": account,
                            "platform": platform,
                            "status": "PLANNED",
                        })

    # Save schedule
    safe_path(DIST_DIR).mkdir(parents=True, exist_ok=True)
    schedule_file = safe_path(DIST_DIR / "weekly_schedule.json")
    # Convert defaultdict to regular dict for JSON
    schedule["totals"] = dict(schedule.get("totals", {}))
    with open(schedule_file, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=2)

    print(f"\n--- Weekly Schedule ({schedule['week_start']} to {schedule['week_end']}) ---\n")

    total_slots = 0
    for day_str, day_info in sorted(schedule["days"].items()):
        slots = day_info.get("slots", [])
        total_slots += len(slots)
        print(f"  {day_info['day_name']} ({day_str}): {len(slots)} posts")
        # Group by account
        by_acct = defaultdict(list)
        for s in sorted(slots, key=lambda x: x.get("time", "")):
            by_acct[s["account"]].append(f"{s['time']} {s['platform']}")
        for acct, times in sorted(by_acct.items()):
            print(f"    {acct}: {', '.join(times)}")

    print(f"\n  Total: {total_slots} posts over 7 days")
    print(f"  Schedule saved: {schedule_file}")

    # Platform totals
    if schedule.get("totals"):
        print("\n  Totals by account/platform:")
        for key, count in sorted(schedule["totals"].items()):
            print(f"    {key}: {count}")


def cmd_ab_report() -> None:
    """Show A/B test status and generate new tests."""
    inventory = load_content_inventory()

    # Load existing tests
    existing = []
    if AB_TEST_LOG.exists():
        with open(AB_TEST_LOG, "r", newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

    print(f"\n--- A/B Test Report ---\n")
    print(f"  Existing tests: {len(existing)}")

    resolved = [t for t in existing if t.get("winner")]
    pending = [t for t in existing if not t.get("winner")]

    if resolved:
        print(f"\n  Resolved tests ({len(resolved)}):")
        wins = defaultdict(int)
        for t in resolved:
            winner = t.get("winner", "")
            if "a" in winner.lower():
                wins[t.get("variant_a_hook", "unknown")] += 1
            else:
                wins[t.get("variant_b_hook", "unknown")] += 1
        for hook, count in sorted(wins.items(), key=lambda x: -x[1]):
            print(f"    {hook}: {count} wins")

    if pending:
        print(f"\n  Pending tests ({len(pending)}):")
        for t in pending[:5]:
            print(f"    {t.get('test_id', '?')}: [{t.get('variant_a_hook', '?')}] vs [{t.get('variant_b_hook', '?')}]")
            print(f"      A: {t.get('variant_a_text', '')[:60]}...")
            print(f"      B: {t.get('variant_b_text', '')[:60]}...")

    # Generate new tests
    new_tests = generate_ab_tests(inventory)
    if new_tests:
        save_ab_tests(new_tests)
        print(f"\n  Generated {len(new_tests)} new A/B tests")
        for t in new_tests[:3]:
            print(f"    {t['test_id']}: [{t['variant_a_hook']}] vs [{t['variant_b_hook']}]")
    else:
        print(f"\n  No new A/B tests generated (need more diverse content)")


def cmd_freshness() -> None:
    """Content freshness audit."""
    tracker = load_distribution_tracker()
    now = datetime.now()

    print(f"\n--- Content Freshness Audit ---\n")

    categories = {"fresh": [], "stale": [], "expired": []}

    for entry in tracker:
        created = entry.get("created_at", "")
        if not created:
            continue
        try:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00").replace("+00:00", ""))
            age_days = (now - created_dt).days
            text = entry.get("content_text", entry.get("formatted_text", ""))[:60]
            platform = entry.get("platform", "?")
            status = entry.get("status", "?")

            item = {"age": age_days, "text": text, "platform": platform, "status": status}

            if age_days <= 3:
                categories["fresh"].append(item)
            elif age_days <= 7:
                categories["stale"].append(item)
            else:
                categories["expired"].append(item)
        except (ValueError, TypeError):
            pass

    for cat, items in categories.items():
        label = {"fresh": "Fresh (0-3 days)", "stale": "Stale (4-7 days)", "expired": "Expired (7+ days)"}
        print(f"  {label.get(cat, cat)}: {len(items)} items")
        for item in items[:3]:
            print(f"    [{item['age']}d] {item['platform']} ({item['status']}): {item['text']}...")
        if len(items) > 3:
            print(f"    ... and {len(items) - 3} more")
        print()

    total = sum(len(v) for v in categories.values())
    if total > 0:
        fresh_pct = len(categories["fresh"]) / total * 100
        print(f"  Freshness score: {fresh_pct:.0f}% fresh")
        if fresh_pct < 30:
            print("  ACTION: Run content_factory.py --batch-alpha 5 to generate fresh content")
        elif fresh_pct < 50:
            print("  NOTE: Content getting stale. Schedule a generation run soon.")
        else:
            print("  GOOD: Content pipeline is healthy.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Engagement Optimizer: analyze, recommend, optimize",
    )
    parser.add_argument("--analyze", action="store_true",
                        help="Analyze content performance")
    parser.add_argument("--recommend", action="store_true",
                        help="What to post next recommendations")
    parser.add_argument("--rate-check", action="store_true",
                        help="Check rate limit safety across platforms")
    parser.add_argument("--schedule-week", action="store_true",
                        help="Generate full week posting schedule")
    parser.add_argument("--ab-report", action="store_true",
                        help="A/B test hook style analysis")
    parser.add_argument("--freshness", action="store_true",
                        help="Content freshness audit")
    args = parser.parse_args()

    if args.analyze:
        cmd_analyze()
    elif args.recommend:
        cmd_recommend()
    elif args.rate_check:
        cmd_rate_check()
    elif args.schedule_week:
        cmd_schedule_week()
    elif args.ab_report:
        cmd_ab_report()
    elif args.freshness:
        cmd_freshness()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
