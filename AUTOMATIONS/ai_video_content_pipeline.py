#!/usr/bin/env python3
"""
PRINTMAXX AI Video Content + Affiliate Pipeline
# CRON: 0 6 * * *  python3 AUTOMATIONS/ai_video_content_pipeline.py --generate fitness --count 5 >> AUTOMATIONS/logs/video_pipeline.log 2>&1

Generates video scripts optimized for AI video tools (Seedance 2.0, Kling, Pika).
Each script: hook (3s) + body (15-45s) + CTA (5s) with affiliate offer integration.
Tracks performance in LEDGER/AI_VIDEO_CONTENT_TRACKER.csv.

The thesis: AI video + affiliate offers + volume uploading = revenue before saturation.
Seedance 2.0, Kling 2.6, Veo 3.1 produce scroll-stopping video at $0.
50-100 videos/day across 5-10 accounts. first movers print.

Usage:
    python3 ai_video_content_pipeline.py --generate "fitness" --count 10
    python3 ai_video_content_pipeline.py --offers
    python3 ai_video_content_pipeline.py --schedule
    python3 ai_video_content_pipeline.py --status
    python3 ai_video_content_pipeline.py --niches
"""

import argparse
import csv
import hashlib
import json
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
SCRIPTS_DIR = AUTOMATIONS_DIR / "auto_ops" / "video_scripts"
TOOL_TRACKER_CSV = PROJECT_ROOT / "10_RESEARCH" / "VIDEO_RESEARCH" / "tools_tracker" / "ALL_TOOLS_TRACKER.csv"
LOGS_DIR = AUTOMATIONS_DIR / "logs"
LOCK_FILE = AUTOMATIONS_DIR / ".video_pipeline.lock"

TRACKER_CSV = LEDGER_DIR / "AI_VIDEO_CONTENT_TRACKER.csv"
LOG_FILE = LOGS_DIR / f"video_pipeline_{datetime.now().strftime('%Y-%m-%d')}.log"

TRACKER_HEADERS = [
    "script_id", "niche", "affiliate_offer", "platform", "script_file",
    "video_status", "posted_at", "views", "clicks", "conversions",
    "revenue", "notes"
]

# ============================================================
# AUTO TOOL SELECTION (Capital Genesis logic)
# ============================================================
# Reads ALL_TOOLS_TRACKER.csv and picks the best video gen tools
# based on quality score, value score, free tier, and API availability.
# Phase-aware: at $0 revenue, prioritize free tiers and value.
# This replaces all hardcoded tool recommendations.

# Content type → tool selection criteria
CONTENT_TYPE_CRITERIA = {
    "hero": {"min_quality": 9.0, "prefer": "quality"},       # ads, landing page
    "volume": {"min_quality": 7.0, "prefer": "value"},       # daily social shorts
    "product_demo": {"min_quality": 8.0, "prefer": "multimodal"},  # product showcase
    "artistic": {"min_quality": 7.0, "prefer": "creative"},  # stylized content
    "long_form": {"min_quality": 8.0, "prefer": "length"},   # faceless youtube
    "default": {"min_quality": 7.0, "prefer": "value"},      # fallback
}


def load_video_tools() -> list:
    """Load video generation tools from the perpetual tracker, sorted by value."""
    if not TOOL_TRACKER_CSV.exists():
        return []
    tools = []
    try:
        with open(TOOL_TRACKER_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("category") == "video_gen" and row.get("status") != "DECLINING":
                    tools.append(row)
    except Exception:
        return []
    # Sort by quality_score descending
    tools.sort(key=lambda t: float(t.get("quality_score", 0)), reverse=True)
    return tools


def select_tools_for_content(content_type: str = "default", max_tools: int = 3) -> list:
    """Auto-select best video tools based on Capital Genesis logic.

    Phase 0 ($0 revenue): prioritize free tier tools, then cheapest paid.
    Returns list of dicts with tool_name, quality, prompt_hint, and reason.
    """
    tools = load_video_tools()
    if not tools:
        # Fallback if tracker unavailable
        return [
            {"tool_name": "Kling 3.0", "quality": 9.5, "prompt_hint": "vertical format, engaging, scroll-stopping", "reason": "fallback (tracker unavailable)"},
            {"tool_name": "Seedance 2.0", "quality": 9.0, "prompt_hint": "9:16 aspect ratio for social media", "reason": "fallback"},
        ]

    criteria = CONTENT_TYPE_CRITERIA.get(content_type, CONTENT_TYPE_CRITERIA["default"])
    min_q = criteria["min_quality"]

    # Filter by minimum quality
    qualified = [t for t in tools if float(t.get("quality_score", 0)) >= min_q]
    if not qualified:
        qualified = tools[:5]  # take top 5 if none meet threshold

    # Score each tool for this content type (Capital Genesis Phase 0 logic)
    scored = []
    for t in qualified:
        quality = float(t.get("quality_score", 5))
        has_free = "free" in str(t.get("free_tier", "")).lower() or "yes" in str(t.get("free_tier", "")).lower() or "credit" in str(t.get("free_tier", "")).lower()
        has_api = t.get("api_available", "").lower() in ("yes", "true", "yes (self-host)")

        # Phase 0 scoring: free tier is king, then quality, then API
        score = quality * 0.35
        if has_free:
            score += 3.0  # massive bonus for free tier at Phase 0
        if has_api:
            score += 1.5  # bonus for automation potential

        # Content-type-specific boosts
        if criteria["prefer"] == "quality":
            score += quality * 0.15  # extra quality weight for hero content
        elif criteria["prefer"] == "value":
            if has_free:
                score += 1.0  # extra free tier bonus for volume
        elif criteria["prefer"] == "multimodal":
            if "multimodal" in t.get("best_for", "").lower() or "reference" in t.get("best_for", "").lower():
                score += 2.0
        elif criteria["prefer"] == "length":
            max_len = t.get("max_length", "")
            if "min" in max_len or "2min" in max_len:
                score += 2.0

        scored.append((t, round(score, 2)))

    scored.sort(key=lambda x: x[1], reverse=True)

    # Build result
    result = []
    for t, score in scored[:max_tools]:
        result.append({
            "tool_name": t["tool_name"],
            "quality": t.get("quality_score", "?"),
            "free_tier": t.get("free_tier", "none"),
            "api_cost": t.get("api_cost_per_sec", "n/a"),
            "prompt_hint": f"{t.get('best_for', '')}. {t.get('notes', '')[:80]}",
            "reason": f"score={score}, quality={t.get('quality_score')}, free={t.get('free_tier', 'no')[:30]}",
        })
    return result


def get_recommended_tools_string(content_type: str = "default") -> str:
    """Get a formatted string of recommended tools for script output."""
    tools = select_tools_for_content(content_type)
    parts = []
    for t in tools:
        free_note = f" ({t['free_tier']})" if t.get("free_tier") and t["free_tier"] != "none" else ""
        parts.append(f"{t['tool_name']}{free_note}")
    return ", ".join(parts)


def get_tool_prompts(content_type: str, topic: str, style: str, tone: str, duration: int) -> str:
    """Generate tool-specific prompts for the top-ranked tools."""
    tools = select_tools_for_content(content_type)
    prompts = []
    for t in tools:
        name = t["tool_name"]
        prompts.append(
            f'**{name} Prompt:**\n'
            f'"{topic}. Style: {style}. Mood: {tone}. '
            f'{duration} seconds, 9:16 vertical, scroll-stopping."'
        )
    return "\n\n".join(prompts)

# ============================================================
# NICHE PRESETS
# ============================================================

NICHE_CONFIG = {
    "fitness": {
        "account": "@WalkToUnlock / fitness accounts",
        "tone": "motivational, direct, energetic",
        "topics": [
            "morning workout routine that takes 10 minutes",
            "the one exercise that fixes bad posture",
            "how to lose belly fat without running",
            "protein intake mistake most people make",
            "why walking 10K steps beats the gym",
            "bodyweight exercises that build real muscle",
            "the 5-minute stretch that fixes back pain",
            "how intermittent fasting actually works",
            "home workout vs gym: real results compared",
            "the supplement nobody talks about for recovery",
            "cold shower benefits backed by science",
            "how to build discipline with one habit",
            "calorie deficit explained in 30 seconds",
            "the pushup variation that targets everything",
            "meal prep for muscle gain on a budget",
            "why you can't lose weight (it's not calories)",
            "creatine: everything you need to know in 60 seconds",
            "how to fix rounded shoulders permanently",
            "the 7-minute HIIT that actually works",
            "sleep optimization: the muscle recovery hack",
        ],
        "affiliate_offers": [
            {"name": "Athletic Greens (AG1)", "network": "Direct", "payout": "$40-$80/sale", "url_pattern": "athleticgreens.com"},
            {"name": "Transparent Labs supplements", "network": "Direct", "payout": "15-20% commission", "url_pattern": "transparentlabs.com"},
            {"name": "Optimum Nutrition (Amazon)", "network": "Amazon Associates", "payout": "3-10%", "url_pattern": "amazon.com"},
            {"name": "Noom weight loss", "network": "CJ Affiliate", "payout": "$10-$15/trial", "url_pattern": "noom.com"},
            {"name": "Peloton app", "network": "ShareASale", "payout": "$5-$10/trial", "url_pattern": "onepeloton.com"},
        ],
        "video_style": "dynamic movement, before/after, workout demonstrations, text overlays with stats",
        "hashtags": "#fitness #workout #gym #fitnessmotivation #exercise #health",
    },
    "finance": {
        "account": "new finance account",
        "tone": "confident, data-driven, no-BS",
        "topics": [
            "the credit card hack banks don't want you to know",
            "how to invest $100 and actually see returns",
            "why your savings account is losing money",
            "the side hustle that pays $500/week",
            "how compound interest makes you rich while you sleep",
            "crypto vs stocks in 2026: real data",
            "the budgeting method that actually works",
            "how I automated my investments (step by step)",
            "tax write-offs nobody tells you about",
            "high-yield savings: where to put your money now",
            "the stock that 10x'd and why nobody noticed",
            "how to negotiate your salary (exact script)",
            "passive income streams ranked by effort",
            "why you should never pay off your mortgage early",
            "the 50/30/20 rule is wrong. here's what works.",
            "how AI is changing personal finance",
            "the app that rounds up your change and invests it",
            "credit score hacks: 100 points in 30 days",
            "how to start investing with zero knowledge",
            "the money habit that separates rich from poor",
        ],
        "affiliate_offers": [
            {"name": "Robinhood", "network": "MaxBounty", "payout": "$20-$50/signup", "url_pattern": "robinhood.com"},
            {"name": "SoFi Invest", "network": "CJ Affiliate", "payout": "$50-$100/funded account", "url_pattern": "sofi.com"},
            {"name": "Acorns", "network": "Direct", "payout": "$10-$15/signup", "url_pattern": "acorns.com"},
            {"name": "Wealthfront", "network": "Direct", "payout": "$20-$30/funded account", "url_pattern": "wealthfront.com"},
            {"name": "NerdWallet credit cards", "network": "Direct", "payout": "$30-$150/approval", "url_pattern": "nerdwallet.com"},
        ],
        "video_style": "charts, numbers on screen, money visuals, calculator animations, luxury lifestyle B-roll",
        "hashtags": "#money #finance #investing #wealth #personalfinance #stocks",
    },
    "tech": {
        "account": "@PRINTMAXXER",
        "tone": "builder energy, practical, insider knowledge",
        "topics": [
            "the AI tool that replaced my entire team",
            "how I built a SaaS in one weekend with Claude",
            "5 free tools that do the same thing as $99/mo apps",
            "the browser extension that saves 2 hours per day",
            "AI video tools ranked: which one is actually free",
            "how to automate your entire workflow with Zapier",
            "the VPN everyone should be using (and why)",
            "best free hosting in 2026 (I tested 10 platforms)",
            "the productivity stack that 10x'd my output",
            "how AI agents will replace 80% of desk jobs",
            "the GitHub repo that does $1000/mo tools for free",
            "Seedance 2.0 just dropped. here's what it does.",
            "why every creator needs a personal website in 2026",
            "the email tool that gets 40% open rates",
            "AI coding assistants: which one actually writes good code",
            "how to scrape any website legally (step by step)",
            "the note-taking app that changed how I think",
            "why I switched from Google to Perplexity",
            "the automation that runs my business while I sleep",
            "ChatGPT vs Claude vs Gemini: honest comparison",
        ],
        "affiliate_offers": [
            {"name": "NordVPN", "network": "CJ Affiliate", "payout": "$10-$15/signup", "url_pattern": "nordvpn.com"},
            {"name": "Notion", "network": "Direct", "payout": "$5-$10/paid signup", "url_pattern": "notion.so"},
            {"name": "Hostinger", "network": "Direct", "payout": "$40-$80/sale", "url_pattern": "hostinger.com"},
            {"name": "Vercel Pro", "network": "Direct", "payout": "15-20% recurring", "url_pattern": "vercel.com"},
            {"name": "Zapier", "network": "Direct", "payout": "$10-$20/paid signup", "url_pattern": "zapier.com"},
        ],
        "video_style": "screen recordings, tool demos, before/after workflows, code on screen",
        "hashtags": "#tech #ai #automation #productivity #tools #coding",
    },
    "beauty": {
        "account": "beauty niche account",
        "tone": "authentic, results-focused, slightly aspirational",
        "topics": [
            "the skincare routine that actually cleared my skin",
            "LED face mask: is it worth the hype? (real results)",
            "the $8 product that replaced my $80 serum",
            "dermatologist secrets they charge $200 to tell you",
            "morning skincare routine in under 3 minutes",
            "the ingredient that reverses aging (not retinol)",
            "microcurrent device: 30 days real results",
            "sunscreen mistakes that age your skin faster",
            "the Korean skincare step everyone skips",
            "how to get glass skin in 2 weeks",
            "gua sha vs jade roller: which actually works",
            "the lash serum that doubled my lash length",
            "dermaplaning at home: safe or dangerous?",
            "the vitamin C serum dermatologists actually use",
            "double cleansing: why and how to do it right",
            "niacinamide explained in 30 seconds",
            "the hair growth secret nobody talks about",
            "ice roller benefits: real or placebo?",
            "retinol for beginners: the only guide you need",
            "the body care routine that changed my skin texture",
        ],
        "affiliate_offers": [
            {"name": "CurrentBody LED", "network": "ShareASale", "payout": "8-12% commission", "url_pattern": "currentbody.com"},
            {"name": "NuFACE microcurrent", "network": "Direct", "payout": "10-15% commission", "url_pattern": "mynuface.com"},
            {"name": "Skincare products (Amazon)", "network": "Amazon Associates", "payout": "3-10%", "url_pattern": "amazon.com"},
            {"name": "Sephora affiliate", "network": "Rakuten", "payout": "5-8%", "url_pattern": "sephora.com"},
            {"name": "Dermstore", "network": "ShareASale", "payout": "5-10%", "url_pattern": "dermstore.com"},
        ],
        "video_style": "close-up application, before/after skin, product unboxing, routine demonstrations",
        "hashtags": "#skincare #beauty #glowup #skincareroutine #beautytips #dermatologist",
    },
    "faith": {
        "account": "@PrayerLock",
        "tone": "calming, respectful, inspirational",
        "topics": [
            "the morning prayer that changed my life",
            "5 minutes of peace: guided breathing with prayer",
            "how consistent prayer improved my mental health",
            "Ramadan preparation: the spiritual checklist",
            "the dua for anxiety that actually calms you",
            "Islamic sleep routine: Sunnah practices",
            "how to build a daily prayer habit",
            "the Quran verse for when you feel lost",
            "night prayers: why tahajjud changes everything",
            "gratitude practice from Islamic tradition",
            "how dhikr reduces stress (science agrees)",
            "the 3-minute wudu routine for busy days",
            "Ramadan fasting tips for beginners",
            "how prayer improves focus and productivity",
            "the evening routine of the Prophet (PBUH)",
            "dealing with hardship: Islamic perspective",
            "the charity that multiplies your blessings",
            "Friday reminders: what to do on Jummah",
            "how to memorize Quran: practical method",
            "the spiritual detox: 7 days of intention",
        ],
        "affiliate_offers": [
            {"name": "Islamic books (Amazon)", "network": "Amazon Associates", "payout": "3-10%", "url_pattern": "amazon.com"},
            {"name": "Prayer mat/accessories", "network": "Amazon Associates", "payout": "3-10%", "url_pattern": "amazon.com"},
            {"name": "Quran app premium", "network": "Direct", "payout": "varies", "url_pattern": "quran.com"},
            {"name": "Halal supplement brands", "network": "Direct", "payout": "10-20%", "url_pattern": "varies"},
            {"name": "Islamic courses (Bayyinah)", "network": "Direct", "payout": "$5-$15/signup", "url_pattern": "bayyinah.com"},
        ],
        "video_style": "serene landscapes, calligraphy, nature scenes, soft lighting, Arabic text overlays",
        "hashtags": "#islam #prayer #dua #quran #muslim #ramadan #faith",
    },
}

# ============================================================
# UTILS
# ============================================================

def safe_path(path: Path) -> Path:
    resolved = path.resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"Path {resolved} outside project root")
    return resolved


def ensure_dirs():
    for d in [LEDGER_DIR, LOGS_DIR, SCRIPTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    try:
        with open(safe_path(LOG_FILE), "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def acquire_lock() -> bool:
    lf = safe_path(LOCK_FILE)
    if lf.exists():
        try:
            pid = int(lf.read_text().strip())
            os.kill(pid, 0)
            return False
        except (ProcessLookupError, ValueError, PermissionError):
            pass
    lf.write_text(str(os.getpid()))
    return True


def release_lock():
    lf = safe_path(LOCK_FILE)
    if lf.exists():
        lf.unlink()

# ============================================================
# SCRIPT GENERATION
# ============================================================

HOOK_TEMPLATES = [
    "stop scrolling. {topic_short}.",
    "nobody's talking about this: {topic_short}.",
    "I tried {topic_short} for 30 days. here's what happened.",
    "the {niche} industry doesn't want you to know this.",
    "this changed everything about how I {action}.",
    "{topic_short}. and it's not what you think.",
    "here's the truth about {topic_short}.",
    "I wasted months before I figured this out.",
    "if you're still {bad_habit}, watch this.",
    "the secret to {desired_outcome} in 2026.",
]

CTA_TEMPLATES = [
    "link in bio for the full breakdown.",
    "I put the exact product I use in my bio.",
    "comment '{keyword}' and I'll send you the link.",
    "full guide in my bio. it's free.",
    "the tool I mentioned is linked in my bio.",
    "follow for more {niche} tips that actually work.",
    "save this before it gets taken down.",
    "I tested 10 options. the best one is in my bio.",
    "link to everything I mentioned is in my bio.",
    "this took me months to figure out. save it.",
]

BODY_STRUCTURES = [
    # Problem -> Agitate -> Solution -> Proof
    "the problem: {problem}. most people try {wrong_approach} which doesn't work because {why_wrong}. instead, {solution}. {proof_statement}.",
    # Myth -> Truth -> Method
    "everyone thinks {myth}. but the truth is {truth}. here's what actually works: {method}. {proof_statement}.",
    # Story -> Lesson -> Action
    "I used to {old_behavior}. then I tried something different. now I {new_behavior}. the key is {key_insight}. {proof_statement}.",
    # Quick List
    "3 things that changed my {niche_area}: first, {point_1}. second, {point_2}. third, {point_3}. the one that made the biggest difference: {biggest}.",
    # Before/After
    "before: {before_state}. I changed one thing in my routine. after 30 days: {after_state}. the difference was {specific_result}.",
]


def generate_script(niche: str, topic: str, config: dict) -> dict:
    """Generate a single video script with hook, body, CTA."""
    script_id = hashlib.md5(f"{niche}{topic}{datetime.now().isoformat()}".encode()).hexdigest()[:10]

    # Parse topic into components
    topic_short = topic.split("(")[0].strip()
    if len(topic_short) > 50:
        topic_short = topic_short[:50]

    # Generate hook
    hook_vars = {
        "topic_short": topic_short,
        "niche": niche,
        "action": _niche_action(niche),
        "bad_habit": _niche_bad_habit(niche),
        "desired_outcome": _niche_outcome(niche),
    }
    hook = random.choice(HOOK_TEMPLATES).format(**hook_vars)

    # Generate body
    body_vars = {
        "problem": _generate_problem(topic, niche),
        "wrong_approach": _generate_wrong_approach(topic, niche),
        "why_wrong": _generate_why_wrong(topic, niche),
        "solution": _generate_solution(topic, niche),
        "proof_statement": _generate_proof(niche),
        "myth": _generate_myth(topic, niche),
        "truth": _generate_truth(topic, niche),
        "method": _generate_method(topic, niche),
        "old_behavior": _generate_old_behavior(niche),
        "discovery": topic_short,
        "new_behavior": _generate_new_behavior(niche),
        "key_insight": _generate_key_insight(topic, niche),
        "niche_area": niche,
        "point_1": _generate_point(topic, niche, 1),
        "point_2": _generate_point(topic, niche, 2),
        "point_3": _generate_point(topic, niche, 3),
        "biggest": _generate_point(topic, niche, 1),
        "before_state": _generate_before(niche),
        "change": topic_short,
        "after_state": _generate_after(niche),
        "specific_result": _generate_specific_result(niche),
    }
    body = random.choice(BODY_STRUCTURES).format(**body_vars)

    # Generate CTA
    affiliate = random.choice(config.get("affiliate_offers", [{"name": "product"}]))
    cta_vars = {
        "keyword": niche.upper()[:4],
        "niche": niche,
    }
    cta = random.choice(CTA_TEMPLATES).format(**cta_vars)

    # Estimate duration
    word_count = len(hook.split()) + len(body.split()) + len(cta.split())
    est_seconds = max(15, min(60, int(word_count / 2.5)))  # ~2.5 words/sec speaking

    script = {
        "script_id": script_id,
        "niche": niche,
        "topic": topic,
        "hook": hook,
        "body": body,
        "cta": cta,
        "full_script": f"{hook}\n\n{body}\n\n{cta}",
        "affiliate_offer": affiliate.get("name", ""),
        "affiliate_network": affiliate.get("network", ""),
        "affiliate_payout": affiliate.get("payout", ""),
        "est_duration_seconds": est_seconds,
        "video_style": config.get("video_style", ""),
        "hashtags": config.get("hashtags", ""),
        "aspect_ratio": "9:16",
        "recommended_tools": get_recommended_tools_string("volume"),
        "platforms": "TikTok, Instagram Reels, YouTube Shorts, Facebook Reels",
        "generated_at": datetime.now().isoformat(),
    }

    return script


def _niche_action(niche):
    actions = {
        "fitness": "work out", "finance": "manage money", "tech": "build things",
        "beauty": "take care of my skin", "faith": "practice daily prayer",
    }
    return actions.get(niche, "approach this")

def _niche_bad_habit(niche):
    habits = {
        "fitness": "skipping workouts", "finance": "not investing",
        "tech": "using expensive tools", "beauty": "following generic routines",
        "faith": "skipping morning prayer",
    }
    return habits.get(niche, "doing it wrong")

def _niche_outcome(niche):
    outcomes = {
        "fitness": "getting fit without the gym", "finance": "building wealth",
        "tech": "automating your workflow", "beauty": "clear glowing skin",
        "faith": "inner peace and consistency",
    }
    return outcomes.get(niche, "real results")

def _generate_problem(topic, niche):
    return f"most people struggle with {topic.split()[2:5] and ' '.join(topic.split()[2:5]) or niche}"

def _generate_wrong_approach(topic, niche):
    wrongs = {
        "fitness": "spending 2 hours at the gym", "finance": "putting everything in savings",
        "tech": "paying for 10 different subscriptions", "beauty": "buying expensive products randomly",
        "faith": "forcing long prayer sessions without consistency",
    }
    return wrongs.get(niche, "the obvious approach")

def _generate_why_wrong(topic, niche):
    reasons = {
        "fitness": "consistency beats intensity every time",
        "finance": "inflation eats your savings faster than you think",
        "tech": "free alternatives exist for 90% of paid tools",
        "beauty": "your skin barrier needs specifics, not generics",
        "faith": "habits are built through small daily actions, not marathons",
    }
    return reasons.get(niche, "it doesn't address the root cause")

def _generate_solution(topic, niche):
    return f"focus on {topic.split(':')[0].strip() if ':' in topic else topic[:30]}"

def _generate_proof(niche):
    proofs = {
        "fitness": "I saw results in 2 weeks doing this consistently.",
        "finance": "my portfolio grew 23% using this exact approach.",
        "tech": "I cut my tool costs from $200/mo to $0.",
        "beauty": "my skin cleared up within 14 days.",
        "faith": "I haven't missed a prayer in 60 days.",
    }
    return proofs.get(niche, "the results speak for themselves.")

def _generate_myth(topic, niche):
    return f"{topic.split()[0:4] and ' '.join(topic.split()[0:4]) or niche + ' advice'} is straightforward"

def _generate_truth(topic, niche):
    return f"there's a specific approach to {niche} that most people miss"

def _generate_method(topic, niche):
    return f"{topic[:40]}. it's simpler than you think."

def _generate_old_behavior(niche):
    olds = {
        "fitness": "skip workouts 4 days a week", "finance": "spend everything I earned",
        "tech": "do everything manually", "beauty": "use random products from TikTok ads",
        "faith": "only pray when I remembered",
    }
    return olds.get(niche, "do things the hard way")

def _generate_new_behavior(niche):
    news = {
        "fitness": "train 6 days a week in under 20 minutes",
        "finance": "invest automatically every paycheck",
        "tech": "automate 80% of my repetitive tasks",
        "beauty": "follow a science-backed 3-step routine",
        "faith": "pray 5 times daily without missing",
    }
    return news.get(niche, "see consistent results")

def _generate_key_insight(topic, niche):
    return f"the key to {topic[:20]} is consistency, not perfection"

def _generate_point(topic, niche, n):
    points = {
        "fitness": ["compound movements over isolation", "sleep 7+ hours", "track protein intake"],
        "finance": ["automate your investments", "eliminate subscriptions", "increase your income"],
        "tech": ["use free open source", "automate repetitive tasks", "build once deploy everywhere"],
        "beauty": ["cleanse properly", "always use SPF", "less products more consistency"],
        "faith": ["set prayer alarms", "start with 2 minutes", "connect with community"],
    }
    pts = points.get(niche, ["step 1", "step 2", "step 3"])
    return pts[min(n-1, len(pts)-1)]

def _generate_before(niche):
    befores = {
        "fitness": "I couldn't do 5 pushups", "finance": "I had $200 in savings",
        "tech": "I wasted 4 hours daily on manual work", "beauty": "my skin was breaking out constantly",
        "faith": "I felt disconnected and anxious",
    }
    return befores.get(niche, "things were not great")

def _generate_after(niche):
    afters = {
        "fitness": "I hit 50 pushups and lost 15 pounds",
        "finance": "I have a 6-month emergency fund and growing portfolio",
        "tech": "I automated my entire workflow",
        "beauty": "my skin is clear and glowing",
        "faith": "I feel centered and at peace daily",
    }
    return afters.get(niche, "everything improved")

def _generate_specific_result(niche):
    results = {
        "fitness": "15 pounds lost in 8 weeks with just 20 min/day",
        "finance": "saved $4,200 in 3 months without earning more",
        "tech": "saved 20 hours per week on automation alone",
        "beauty": "zero breakouts for 30 days straight",
        "faith": "60-day unbroken prayer streak",
    }
    return results.get(niche, "measurable improvement in 30 days")

# ============================================================
# BATCH GENERATION
# ============================================================

def generate_batch(niche: str, count: int) -> list:
    """Generate a batch of video scripts for a niche."""
    config = NICHE_CONFIG.get(niche)
    if not config:
        log(f"Unknown niche: {niche}. Available: {', '.join(NICHE_CONFIG.keys())}", "ERROR")
        return []

    topics = config["topics"]
    if count > len(topics):
        # Cycle through topics
        selected = topics * (count // len(topics) + 1)
        selected = selected[:count]
    else:
        selected = random.sample(topics, count)

    scripts = []
    for topic in selected:
        script = generate_script(niche, topic, config)
        scripts.append(script)

    # Save scripts to files
    batch_dir = safe_path(SCRIPTS_DIR / niche / datetime.now().strftime("%Y-%m-%d"))
    batch_dir.mkdir(parents=True, exist_ok=True)

    for script in scripts:
        script_file = batch_dir / f"{script['script_id']}.md"
        content = f"""# Video Script: {script['topic']}

**Niche:** {script['niche']}
**Duration:** ~{script['est_duration_seconds']}s
**Aspect Ratio:** {script['aspect_ratio']}
**Affiliate:** {script['affiliate_offer']} ({script['affiliate_network']}, {script['affiliate_payout']})
**Tools:** {script['recommended_tools']}
**Platforms:** {script['platforms']}
**Generated:** {script['generated_at']}

---

## HOOK (first 3 seconds)

{script['hook']}

## BODY (15-45 seconds)

{script['body']}

## CTA (last 5 seconds)

{script['cta']}

---

## Full Script (copy-paste for voiceover)

{script['full_script']}

---

## Video Direction

**Visual Style:** {script['video_style']}

{get_tool_prompts('volume', script['topic'], script['video_style'], config['tone'], script['est_duration_seconds'])}

**Hashtags:** {script['hashtags']}
"""
        script_file.write_text(content)
        script["script_file"] = str(script_file.relative_to(PROJECT_ROOT))

    # Track in CSV
    track_scripts(scripts)

    log(f"Generated {len(scripts)} scripts for niche '{niche}' in {batch_dir}")
    return scripts


def track_scripts(scripts: list):
    """Append scripts to tracker CSV."""
    csv_path = safe_path(TRACKER_CSV)
    file_exists = csv_path.exists() and csv_path.stat().st_size > 0

    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_HEADERS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        for s in scripts:
            writer.writerow({
                "script_id": s["script_id"],
                "niche": s["niche"],
                "affiliate_offer": s["affiliate_offer"],
                "platform": "ALL",
                "script_file": s.get("script_file", ""),
                "video_status": "SCRIPTED",
                "posted_at": "",
                "views": 0,
                "clicks": 0,
                "conversions": 0,
                "revenue": 0,
                "notes": f"Duration: ~{s['est_duration_seconds']}s. Topic: {s['topic'][:50]}",
            })

# ============================================================
# OFFERS DISPLAY
# ============================================================

def show_offers():
    """Show available affiliate offers by niche."""
    print("\n" + "=" * 70)
    print("  AFFILIATE OFFERS BY NICHE")
    print("=" * 70)

    for niche, config in NICHE_CONFIG.items():
        print(f"\n  [{niche.upper()}] ({config['account']})")
        print(f"  {'Offer':<35} {'Network':<15} {'Payout':<20}")
        print(f"  {'-'*35} {'-'*15} {'-'*20}")
        for offer in config.get("affiliate_offers", []):
            print(f"  {offer['name']:<35} {offer['network']:<15} {offer['payout']:<20}")

    print(f"\n  SIGNUP LINKS:")
    print(f"    ClickBank:    https://accounts.clickbank.com/signup/")
    print(f"    MaxBounty:    https://www.maxbounty.com/signup.cfm")
    print(f"    CJ Affiliate: https://www.cj.com/")
    print(f"    ShareASale:   https://www.shareasale.com/")
    print(f"    Amazon:       https://affiliate-program.amazon.com/")
    print(f"    Digistore24:  https://www.digistore24.com/signup/")
    print("=" * 70 + "\n")

# ============================================================
# SCHEDULE
# ============================================================

def show_schedule():
    """Generate a daily posting schedule."""
    print("\n" + "=" * 70)
    print("  DAILY POSTING SCHEDULE")
    print("=" * 70)

    schedule = [
        {"time": "6:00 AM", "platform": "TikTok", "niche": "fitness", "note": "Early morning workout audience"},
        {"time": "7:00 AM", "platform": "Instagram Reels", "niche": "beauty", "note": "Morning skincare routine viewers"},
        {"time": "8:00 AM", "platform": "YouTube Shorts", "niche": "tech", "note": "Commute scrollers"},
        {"time": "9:00 AM", "platform": "TikTok", "niche": "finance", "note": "Market open energy"},
        {"time": "12:00 PM", "platform": "Instagram Reels", "niche": "fitness", "note": "Lunch break scrolling"},
        {"time": "1:00 PM", "platform": "TikTok", "niche": "tech", "note": "Afternoon productivity crowd"},
        {"time": "3:00 PM", "platform": "YouTube Shorts", "niche": "beauty", "note": "Afternoon wind-down"},
        {"time": "5:00 PM", "platform": "TikTok", "niche": "faith", "note": "Maghrib/evening prayer time"},
        {"time": "6:00 PM", "platform": "Instagram Reels", "niche": "finance", "note": "Post-work reflection"},
        {"time": "8:00 PM", "platform": "TikTok", "niche": "fitness", "note": "Evening workout motivation"},
        {"time": "9:00 PM", "platform": "YouTube Shorts", "niche": "faith", "note": "Night routine/reflection"},
        {"time": "10:00 PM", "platform": "TikTok", "niche": "beauty", "note": "Nighttime skincare crowd"},
    ]

    print(f"\n  {'Time':<12} {'Platform':<18} {'Niche':<12} {'Note':<40}")
    print(f"  {'-'*12} {'-'*18} {'-'*12} {'-'*40}")
    for s in schedule:
        print(f"  {s['time']:<12} {s['platform']:<18} {s['niche']:<12} {s['note']:<40}")

    print(f"\n  Total: {len(schedule)} posts/day across {len(set(s['platform'] for s in schedule))} platforms")
    print(f"  Niches: {', '.join(sorted(set(s['niche'] for s in schedule)))}")
    print(f"\n  Generate scripts: python3 ai_video_content_pipeline.py --generate [niche] --count [N]")
    print("=" * 70 + "\n")

# ============================================================
# STATUS
# ============================================================

def show_status():
    """Show pipeline status."""
    print("\n" + "=" * 70)
    print("  AI VIDEO CONTENT PIPELINE STATUS")
    print("=" * 70)

    # Check tracker
    total_scripts = 0
    by_status = {}
    by_niche = {}
    total_views = 0
    total_revenue = 0.0

    if TRACKER_CSV.exists():
        with open(TRACKER_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_scripts += 1
                status = row.get("video_status", "UNKNOWN")
                niche = row.get("niche", "UNKNOWN")
                by_status[status] = by_status.get(status, 0) + 1
                by_niche[niche] = by_niche.get(niche, 0) + 1
                try:
                    total_views += int(row.get("views", 0))
                    total_revenue += float(row.get("revenue", 0))
                except (ValueError, TypeError):
                    pass

    print(f"\n  SCRIPTS:")
    print(f"    Total generated:   {total_scripts}")
    for status, count in sorted(by_status.items()):
        print(f"    {status}:{'':>{16-len(status)}} {count}")
    print(f"\n  BY NICHE:")
    for niche, count in sorted(by_niche.items()):
        print(f"    {niche}:{'':>{16-len(niche)}} {count}")
    print(f"\n  PERFORMANCE:")
    print(f"    Total views:       {total_views:,}")
    print(f"    Total revenue:     ${total_revenue:,.2f}")

    # Check script files on disk
    script_count = 0
    if SCRIPTS_DIR.exists():
        for md_file in SCRIPTS_DIR.rglob("*.md"):
            script_count += 1
    print(f"\n  SCRIPT FILES ON DISK: {script_count}")

    # Available niches
    print(f"\n  AVAILABLE NICHES ({len(NICHE_CONFIG)}):")
    for niche, config in NICHE_CONFIG.items():
        topics = len(config.get("topics", []))
        offers = len(config.get("affiliate_offers", []))
        print(f"    {niche:<12} {topics} topics, {offers} affiliate offers, account: {config.get('account', 'N/A')}")

    print(f"\n  FILES:")
    print(f"    Tracker:     {TRACKER_CSV}")
    print(f"    Scripts dir: {SCRIPTS_DIR}")
    print(f"    Log:         {LOG_FILE}")

    print(f"\n  QUICK START:")
    print(f"    python3 ai_video_content_pipeline.py --generate fitness --count 5")
    print(f"    python3 ai_video_content_pipeline.py --offers")
    print(f"    python3 ai_video_content_pipeline.py --schedule")
    print("=" * 70 + "\n")


def show_niches():
    """Show available niches with details."""
    print("\n  AVAILABLE NICHES:\n")
    for niche, config in NICHE_CONFIG.items():
        print(f"  [{niche.upper()}]")
        print(f"    Account: {config['account']}")
        print(f"    Tone: {config['tone']}")
        print(f"    Topics: {len(config['topics'])}")
        print(f"    Offers: {len(config.get('affiliate_offers', []))}")
        print(f"    Style: {config.get('video_style', '')[:60]}")
        print()

# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX AI Video Content + Affiliate Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ai_video_content_pipeline.py --generate fitness --count 10
  python3 ai_video_content_pipeline.py --generate finance --count 5
  python3 ai_video_content_pipeline.py --offers
  python3 ai_video_content_pipeline.py --schedule
  python3 ai_video_content_pipeline.py --status
  python3 ai_video_content_pipeline.py --niches
        """,
    )
    parser.add_argument("--generate", type=str, metavar="NICHE", help="Generate scripts for niche")
    parser.add_argument("--count", type=int, default=5, help="Number of scripts to generate (default: 5)")
    parser.add_argument("--offers", action="store_true", help="Show affiliate offers by niche")
    parser.add_argument("--schedule", action="store_true", help="Show daily posting schedule")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--niches", action="store_true", help="Show available niches")

    args = parser.parse_args()
    ensure_dirs()

    if not any([args.generate, args.offers, args.schedule, args.status, args.niches]):
        args.status = True

    if args.offers:
        show_offers()
    elif args.schedule:
        show_schedule()
    elif args.niches:
        show_niches()
    elif args.status:
        show_status()
    elif args.generate:
        if not acquire_lock():
            log("Another instance running.", "WARN")
            sys.exit(1)
        try:
            scripts = generate_batch(args.generate, args.count)
            if scripts:
                print(f"\nGenerated {len(scripts)} video scripts for '{args.generate}'")
                print(f"\nScripts saved to: {SCRIPTS_DIR / args.generate}/")
                print(f"\nSample script:\n")
                sample = scripts[0]
                print(f"  Topic: {sample['topic']}")
                print(f"  Duration: ~{sample['est_duration_seconds']}s")
                print(f"  Affiliate: {sample['affiliate_offer']}")
                print(f"  ---")
                print(f"  HOOK: {sample['hook']}")
                print(f"  BODY: {sample['body'][:150]}...")
                print(f"  CTA: {sample['cta']}")
                print(f"\n  Full scripts in: {sample.get('script_file', SCRIPTS_DIR)}")
                print(f"\nNext steps:")
                top_tools = select_tools_for_content("volume", max_tools=2)
                tool_names = " or ".join(t["tool_name"] for t in top_tools)
                print(f"  1. Open script file and copy the AI video tool prompt")
                print(f"  2. Generate video on {tool_names} (auto-selected by Capital Genesis ranking)")
                print(f"  3. Add captions in CapCut")
                print(f"  4. Upload to TikTok, Reels, Shorts")
                print(f"  5. Set affiliate link in bio")
        finally:
            release_lock()


if __name__ == "__main__":
    main()
