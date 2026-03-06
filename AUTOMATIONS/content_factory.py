#!/usr/bin/env python3
"""
PRINTMAXX Content Factory
==========================
One script to rule all content generation. Takes ANY input (alpha entry, build
log, research finding, tool discovery) and outputs ALL formats simultaneously.

Runs the copy-style.md checklist on every piece of output. No em dashes, no AI
vocabulary, consequence-first hooks, PRINTMAXXER voice.

Outputs:
    - 3 tweets (consequence-first hooks, PRINTMAXXER voice)
    - 1 tweet thread (5-7 tweets)
    - 1 LinkedIn post (B2B angle)
    - 1 Reddit post (value-first, platform-appropriate)
    - 1 newsletter section (2-3 paragraphs)
    - 1 Gumroad product angle (if applicable)

Usage:
    python3 AUTOMATIONS/content_factory.py --input "topic or finding"
    python3 AUTOMATIONS/content_factory.py --from-alpha ALPHA042
    python3 AUTOMATIONS/content_factory.py --from-session
    python3 AUTOMATIONS/content_factory.py --batch-alpha 10
    python3 AUTOMATIONS/content_factory.py --voice-check "CONTENT/social/auto_generated/tweets_*.csv"
    python3 AUTOMATIONS/content_factory.py --dry-run --input "cold email framework"

Cron:
    0 8 * * * cd $BASE && python3 AUTOMATIONS/content_factory.py --batch-alpha 5 >> AUTOMATIONS/logs/content_factory.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_CSV = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
OUTPUT_DIR = PROJECT_ROOT / "CONTENT" / "social" / "auto_generated"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
SESSION_LOG = PROJECT_ROOT / "OPS" / "SESSION_LOG.md"
COPY_STYLE = PROJECT_ROOT / ".claude" / "rules" / "copy-style.md"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] content_factory: {msg}"
    print(line, file=sys.stderr)
    safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_DIR / "content_factory.log"), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# BANNED vocabulary and patterns from copy-style.md
# ---------------------------------------------------------------------------
BANNED_WORDS = [
    "additionally", "moreover", "furthermore", "testament", "landscape",
    "paradigm", "leverage", "utilize", "delve", "dive into", "unpack",
    "comprehensive", "robust", "streamlined", "game-changer", "unlock",
    "elevate", "cutting-edge", "innovative", "revolutionary", "empower",
    "enable", "foster", "seamless", "frictionless", "journey",
    "groundbreaking", "synergy", "holistic", "unprecedented",
    "transformative", "disruptive", "ecosystem", "scalable",
]

BANNED_PHRASES = [
    "it's not just", "in order to", "due to the fact that",
    "at this point in time", "in terms of", "it's important to note",
    "it goes without saying", "i hope this helps",
    "let me know if you have questions", "happy to assist",
    "as of my last update", "great question",
    "in today's rapidly evolving", "in conclusion",
]

FIND_REPLACE = {
    "\u2014": ", ",    # em dash
    "\u2013": ", ",    # en dash
    "leverage": "use",
    "utilize": "use",
    "additionally": "also",
    "furthermore": "also",
    "delve into": "look at",
    "comprehensive": "",
    "robust": "solid",
    "innovative": "new",
    "seamless": "smooth",
    "streamlined": "simple",
    "empower": "help",
}

# ---------------------------------------------------------------------------
# Account definitions
# ---------------------------------------------------------------------------
ACCOUNTS = {
    "PRINTMAXXER": {
        "handle": "@PRINTMAXXER",
        "niche": "tech/building-in-public",
        "tone": "aggressive builder energy, specific numbers, consequence-first",
        "relevant_keywords": [
            "saas", "revenue", "mrr", "ship", "build", "launch", "code",
            "automation", "ai", "gpt", "claude", "startup", "indie",
            "product", "growth", "cold email", "gumroad", "stripe",
            "scraper", "tool", "wrapper", "api", "agent", "deploy",
        ],
    },
    "repscheme": {
        "handle": "@repscheme",
        "niche": "fitness",
        "tone": "discipline-focused, no excuses, numbers on gains",
        "relevant_keywords": [
            "gym", "fitness", "workout", "lift", "muscle", "protein",
            "creatine", "sleep", "discipline", "consistency",
        ],
    },
    "drifthour": {
        "handle": "@drifthour",
        "niche": "aesthetic/ambient",
        "tone": "atmospheric, minimal words, vibe-first, lowercase",
        "relevant_keywords": [
            "aesthetic", "lofi", "ambient", "music", "curate", "vibe",
            "golden hour", "morning", "walk", "silence", "minimal",
        ],
    },
    "voidpilled": {
        "handle": "@voidpilled",
        "niche": "esoteric",
        "tone": "cryptic, philosophical, brief, no hedging",
        "relevant_keywords": [
            "consciousness", "psychedelic", "brain", "neuroscience",
            "meditation", "energy", "frequency", "simulation", "reality",
            "pattern", "system", "data", "signal", "hidden", "deep",
        ],
    },
    "selahmoments": {
        "handle": "@selahmoments",
        "niche": "faith",
        "tone": "reflective, purposeful, community-oriented, lowercase",
        "relevant_keywords": [
            "faith", "god", "prayer", "steward", "grace", "blessing",
            "church", "ministry", "serve", "community", "worship",
        ],
    },
}

# ---------------------------------------------------------------------------
# Tweet hook templates (consequence-first, PRINTMAXXER voice)
# ---------------------------------------------------------------------------
TWEET_HOOKS = [
    "{consequence}. here's exactly how it works.",
    "{consequence}. most people miss this completely.",
    "i {action} and {consequence}. stop overthinking it.",
    "{consequence}. the play is right there if you're paying attention.",
    "{tool_or_method}. {consequence}. it's borderline illegal how good this is.",
    "{consequence}. tested it myself. {proof}.",
    "just {action}. {consequence}. no excuses left.",
    "{consequence}. one session. that's all it took.",
    "the {topic} play nobody talks about: {method}. {consequence}.",
    "{consequence}. and i almost didn't try it.",
]

THREAD_OPENERS = [
    "i {action} and the results were wild. full breakdown:",
    "{consequence}. here's the exact playbook (thread):",
    "spent {timeframe} testing this. {consequence}. here's everything:",
    "the {topic} strategy that actually works. no fluff, just steps:",
    "{consequence}. and it only took {timeframe}. here's how:",
]

THREAD_CLOSERS = [
    "that's the whole play. stop planning, start doing.",
    "repost this if it helped. building more of these.",
    "the formula: {method}. results speak for themselves.",
    "now you know. the rest is execution.",
    "if this saved you time, follow for more like this.",
]

LINKEDIN_TEMPLATES = [
    "I tested {method} for {timeframe}.\n\nResults:\n{bullets}\n\nThe takeaway: {takeaway}\n\nIf you're building in this space, this is worth trying.",
    "{consequence}.\n\nHere's what I learned after {timeframe} of testing:\n\n{bullets}\n\nThe B2B angle: {b2b_angle}",
    "Most people overthink {topic}.\n\nHere's the simple version:\n\n{bullets}\n\n{takeaway}",
]

REDDIT_TEMPLATES = [
    "## {title}\n\n{intro}\n\n**What I did:**\n{steps}\n\n**Results:**\n{results}\n\nHappy to answer questions.",
    "## {title}\n\n{intro}\n\n{body}\n\nLet me know if you want the details on any specific step.",
    "## {title}\n\nI spent {timeframe} on this and wanted to share what I found.\n\n{body}\n\n**Key numbers:** {results}",
]

NEWSLETTER_TEMPLATES = [
    "{hook}\n\n{body_p1}\n\n{body_p2}\n\nThe bottom line: {takeaway}",
    "{hook}\n\n{body_p1}\n\n{body_p2}\n\n{body_p3}",
]

GUMROAD_ANGLES = [
    "the {topic} playbook: everything I tested, what worked, what didn't. {price_anchor}.",
    "{method} template pack: copy my exact {topic} setup. save {timeframe} of trial and error.",
    "the {topic} swipe file: {number} proven {asset_type} you can use today.",
]

# ---------------------------------------------------------------------------
# Content input extraction
# ---------------------------------------------------------------------------
def extract_topic_from_text(text: str) -> dict:
    """Parse free text into structured content seed."""
    seed = {
        "raw_input": text,
        "topic": "",
        "method": "",
        "consequence": "",
        "tool": "",
        "numbers": [],
        "timeframe": "",
        "action": "",
        "proof": "",
        "input_type": "text",
    }

    # Extract numbers
    numbers = re.findall(r'\$[\d,]+[kK]?(?:/(?:mo|month|day|year|week))?|\d+(?:\.\d+)?%|\d+[xX]|\d{2,}\+?', text)
    seed["numbers"] = numbers[:5]

    # Extract tool names (domain style or known tools)
    tool_match = re.search(r'(\w+\.(?:io|ai|com|dev|app|co|sh|so))', text, re.IGNORECASE)
    if tool_match:
        seed["tool"] = tool_match.group(1)
    else:
        known = re.search(
            r'\b(n8n|GPT-\d|Claude|Cursor|Vercel|Supabase|Stripe|Notion|'
            r'Airtable|Zapier|Make|Buffer|Beehiiv|Substack|Gumroad|'
            r'Playwright|Puppeteer|RevenueCat|Capacitor)\b',
            text, re.IGNORECASE,
        )
        if known:
            seed["tool"] = known.group(1)

    # Extract timeframe
    tf_match = re.search(r'(\d+\s*(?:hours?|days?|weeks?|months?|minutes?|sessions?))', text, re.IGNORECASE)
    if tf_match:
        seed["timeframe"] = tf_match.group(1)
    else:
        seed["timeframe"] = random.choice(["one session", "2 hours", "a weekend", "30 minutes"])

    # First sentence as consequence, rest as method
    sentences = re.split(r'[.!?]\s+', text.strip())
    if sentences:
        seed["consequence"] = sentences[0].strip().rstrip(".")
        if len(seed["consequence"]) > 140:
            seed["consequence"] = seed["consequence"][:137] + "..."
    if len(sentences) > 1:
        seed["method"] = ". ".join(sentences[1:3]).strip()

    # Topic: first few important words
    words = [w for w in text.split()[:8] if len(w) > 3]
    seed["topic"] = " ".join(words[:4]).lower()

    # Action verb extraction
    action_match = re.search(
        r'\b(built|shipped|tested|launched|automated|scraped|deployed|'
        r'wired|connected|set up|configured|found|discovered|created)\b',
        text, re.IGNORECASE,
    )
    if action_match:
        seed["action"] = action_match.group(1).lower()
    else:
        seed["action"] = random.choice(["tested this", "set this up", "built this out"])

    # Proof
    if numbers:
        seed["proof"] = f"{numbers[0]} and counting"
    else:
        seed["proof"] = "results speak for themselves"

    return seed


def extract_from_alpha(entry: dict) -> dict:
    """Convert an ALPHA_STAGING row into a content seed."""
    tactic = ""
    for field in ("extracted_method", "tactic", "reviewer_notes", "alpha_text"):
        val = (entry.get(field) or "").strip()
        if val and len(val) > 15:
            val = re.sub(r'^APPROVED\.?\s*', '', val, flags=re.IGNORECASE)
            tactic = val.strip(". ")
            break

    if not tactic:
        tactic = entry.get("alpha_id", "unknown alpha")

    seed = extract_topic_from_text(tactic)
    seed["input_type"] = "alpha"
    seed["alpha_id"] = entry.get("alpha_id", "")
    seed["category"] = entry.get("category", "")
    seed["source"] = entry.get("source", "")
    return seed


def extract_from_session_log() -> list[dict]:
    """Pull recent session accomplishments as content seeds."""
    seeds = []
    if not SESSION_LOG.exists():
        log("SESSION_LOG.md not found")
        return seeds

    content = SESSION_LOG.read_text(encoding="utf-8", errors="replace")

    # Find recent session blocks
    session_blocks = re.split(r'(?=##\s+Session\s+\d|(?=\d{4}-\d{2}-\d{2}))', content)

    for block in session_blocks[-3:]:
        bullets = re.findall(r'[-*]\s+(.{20,200})', block)
        for bullet in bullets[:5]:
            if any(skip in bullet.lower() for skip in [
                "session_log", "persistent_task", "heartbeat",
                "updated ops", "read ", "checked ", "status:",
            ]):
                continue
            seed = extract_topic_from_text(bullet)
            seed["input_type"] = "session"
            seeds.append(seed)

    log(f"Extracted {len(seeds)} content seeds from session log")
    return seeds[:10]


# ---------------------------------------------------------------------------
# Voice check (copy-style.md compliance)
# ---------------------------------------------------------------------------
def voice_check(text: str) -> dict:
    """Run the copy-style.md pre-publish checklist on text.

    Returns dict with pass/fail, issues found, and cleaned text.
    """
    issues = []
    cleaned = text

    # 1. Em dashes
    if "\u2014" in cleaned or "\u2013" in cleaned:
        issues.append("em/en dash found")
        cleaned = cleaned.replace("\u2014", ", ").replace("\u2013", ", ")

    # 2. Banned AI vocabulary
    text_lower = cleaned.lower()
    for word in BANNED_WORDS:
        if word in text_lower:
            issues.append(f"banned word: '{word}'")
            if word in FIND_REPLACE:
                replacement = FIND_REPLACE[word]
                cleaned = re.sub(
                    rf'\b{re.escape(word)}\b',
                    replacement,
                    cleaned,
                    flags=re.IGNORECASE,
                )

    # 3. Banned phrases
    for phrase in BANNED_PHRASES:
        if phrase in text_lower:
            issues.append(f"banned phrase: '{phrase}'")
            cleaned = re.sub(re.escape(phrase), "", cleaned, flags=re.IGNORECASE)

    # 4. "It's not just X, it's Y" construction
    if re.search(r"it'?s not just .+, it'?s", text_lower):
        issues.append("'it's not just X, it's Y' construction")

    # 5. Excessive hedging
    hedges = ["might", "possibly", "perhaps", "somewhat", "maybe", "could potentially"]
    for sent in re.split(r'[.!?]', cleaned):
        hedge_count = sum(1 for h in hedges if h in sent.lower())
        if hedge_count >= 2:
            issues.append(f"excessive hedging: '{sent.strip()[:60]}...'")

    # 6. Title case headings
    title_case = re.findall(r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+', cleaned, re.MULTILINE)
    if title_case and len(title_case) > 1:
        issues.append("possible title case heading detected")

    # 7. Sycophantic tone
    syc_patterns = ["great question", "that's such an", "insightful observation"]
    for sp in syc_patterns:
        if sp in text_lower:
            issues.append(f"sycophantic tone: '{sp}'")

    # 8. Chatbot artifacts
    chatbot = ["i hope this helps", "let me know if", "happy to assist", "feel free to"]
    for cb in chatbot:
        if cb in text_lower:
            issues.append(f"chatbot artifact: '{cb}'")
            cleaned = re.sub(re.escape(cb) + r'[.!]*', '', cleaned, flags=re.IGNORECASE)

    # 9. Promotional language
    promo = ["breathtaking", "nestled", "cutting-edge", "state-of-the-art", "world-class"]
    for p in promo:
        if p in text_lower:
            issues.append(f"promotional language: '{p}'")

    # 10. Vague attributions
    vague = ["studies show", "experts believe", "experts agree", "research suggests"]
    for v in vague:
        if v in text_lower:
            issues.append(f"vague attribution: '{v}'")

    # 11. Filler phrases
    fillers = {
        "in order to": "to",
        "due to the fact that": "because",
        "at this point in time": "now",
        "it goes without saying": "",
    }
    for filler, replacement in fillers.items():
        if filler in text_lower:
            issues.append(f"filler phrase: '{filler}'")
            cleaned = re.sub(re.escape(filler), replacement, cleaned, flags=re.IGNORECASE)

    # 12. Significance inflation
    inflation = ["revolutionary", "transforms the landscape", "unprecedented levels",
                 "paradigm shift", "groundbreaking"]
    for inf in inflation:
        if inf in text_lower:
            issues.append(f"significance inflation: '{inf}'")

    # Clean up artifacts
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = re.sub(r'\s+([,.])', r'\1', cleaned)
    cleaned = re.sub(r'([,.])\1+', r'\1', cleaned)

    passed = len(issues) == 0
    return {
        "passed": passed,
        "issues": issues,
        "original": text,
        "cleaned": cleaned,
        "issue_count": len(issues),
    }


def voice_check_batch(texts: list[str]) -> list[dict]:
    """Run voice check on multiple texts."""
    return [voice_check(t) for t in texts]


# ---------------------------------------------------------------------------
# Content generators
# ---------------------------------------------------------------------------
def generate_tweets(seed: dict, count: int = 3) -> list[str]:
    """Generate consequence-first tweet variants."""
    tweets = []
    consequence = seed.get("consequence", "results were wild")
    method = seed.get("method", "")
    tool = seed.get("tool", "")
    action = seed.get("action", "tested this")
    proof = seed.get("proof", "results speak for themselves")
    topic = seed.get("topic", "this")
    numbers = seed.get("numbers", [])
    tool_or_method = tool if tool else (method[:60] if method else topic)

    available_hooks = list(TWEET_HOOKS)
    random.shuffle(available_hooks)

    for i in range(min(count, len(available_hooks))):
        template = available_hooks[i]
        try:
            tweet = template.format(
                consequence=consequence,
                method=method[:80] if method else topic,
                tool_or_method=tool_or_method,
                action=action,
                proof=proof,
                topic=topic,
                tool=tool if tool else "this tool",
                number=numbers[0] if numbers else "100+",
                timeframe=seed.get("timeframe", "one session"),
            )
        except (KeyError, IndexError):
            tweet = f"{consequence}. {method[:80] if method else topic}. just do it."

        # Lowercase for PRINTMAXXER voice
        tweet = tweet.lower()

        # Enforce 280 char limit
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."

        # Voice check and clean
        vc = voice_check(tweet)
        tweet = vc["cleaned"]

        if len(tweet) > 20:
            tweets.append(tweet)

    return tweets[:count]


def generate_thread(seed: dict, length: int = 6) -> list[str]:
    """Generate a 5-7 tweet thread."""
    thread = []
    consequence = seed.get("consequence", "results were wild")
    method = seed.get("method", "")
    topic = seed.get("topic", "this")
    tool = seed.get("tool", "")
    action = seed.get("action", "tested this")
    timeframe = seed.get("timeframe", "one session")
    numbers = seed.get("numbers", [])

    # Tweet 1: Hook
    opener = random.choice(THREAD_OPENERS)
    try:
        t1 = opener.format(
            consequence=consequence,
            action=action,
            topic=topic,
            timeframe=timeframe,
        )
    except KeyError:
        t1 = f"i {action} and {consequence}. full breakdown:"
    thread.append(t1.lower())

    # Tweet 2: Context / problem
    if method:
        t2 = f"the problem: most people overcomplicate {topic}. they spend weeks planning when the answer is right there."
    else:
        t2 = f"most people won't try this because it seems too simple. that's exactly why it works."
    thread.append(t2.lower())

    # Tweet 3-5: Method steps
    if method:
        method_parts = re.split(r'[.;]\s*', method)
        for i, part in enumerate(method_parts[:3]):
            part = part.strip()
            if len(part) > 15:
                step = f"step {i + 1}: {part}"
                if tool and i == 0:
                    step += f". i used {tool} for this."
                if numbers and i < len(numbers):
                    step += f" ({numbers[i]} results)"
                thread.append(step.lower())
    else:
        thread.append(f"step 1: find the exact thing that's working. don't guess. look at the data.")
        if tool:
            thread.append(f"step 2: set up {tool}. takes {timeframe}. stop overthinking the setup.")
        else:
            thread.append(f"step 2: set it up. takes {timeframe}. stop overthinking the setup.")
        thread.append(f"step 3: run it. measure it. iterate. that's the whole formula.")

    # Pad to desired length
    filler_insights = [
        f"the key insight: {topic} rewards consistency over perfection.",
        f"most people quit before the compound effect kicks in. don't be most people.",
        f"this works because everyone else is overthinking it. simplicity is the edge.",
        f"i tested {random.choice(['3', '5', '7', '10'])} variations. this one won by a mile.",
    ]
    while len(thread) < length - 1:
        thread.append(random.choice(filler_insights).lower())

    # Final tweet: closer
    closer = random.choice(THREAD_CLOSERS)
    try:
        final = closer.format(method=method[:60] if method else topic)
    except KeyError:
        final = "that's the play. stop planning, start doing."
    thread.append(final.lower())

    # Voice check each tweet
    cleaned_thread = []
    for t in thread[:length]:
        vc = voice_check(t)
        t_clean = vc["cleaned"]
        if len(t_clean) > 280:
            t_clean = t_clean[:277] + "..."
        cleaned_thread.append(t_clean)

    return cleaned_thread


def generate_linkedin(seed: dict) -> str:
    """Generate a LinkedIn post with B2B angle."""
    consequence = seed.get("consequence", "results were significant")
    method = seed.get("method", "")
    topic = seed.get("topic", "this approach")
    tool = seed.get("tool", "")
    timeframe = seed.get("timeframe", "2 weeks")
    numbers = seed.get("numbers", [])

    # Build bullet points
    bullets = []
    if method:
        for part in re.split(r'[.;]\s*', method)[:4]:
            part = part.strip()
            if len(part) > 10:
                bullets.append(f"- {part}")
    if not bullets:
        bullets = [
            f"- Tested the approach for {timeframe}",
            f"- Results: {numbers[0] if numbers else 'measurable improvement'}",
            f"- Setup time: {timeframe}",
        ]
    bullet_text = "\n".join(bullets)

    b2b_angles = [
        f"If you're running a team, this saves each person {timeframe} per week.",
        f"The B2B application: any company doing {topic} should test this immediately.",
        f"For agencies and consultancies: this is a service you can sell.",
        f"Enterprise teams are sleeping on this. The ROI is clear.",
    ]
    b2b = random.choice(b2b_angles)

    takeaway = f"The data is clear. {consequence}. Worth testing for any team."
    if tool:
        takeaway = f"Tool used: {tool}. {consequence}. Worth testing for any team."

    template = random.choice(LINKEDIN_TEMPLATES)
    try:
        post = template.format(
            consequence=consequence,
            method=method[:100] if method else topic,
            topic=topic,
            timeframe=timeframe,
            bullets=bullet_text,
            takeaway=takeaway,
            b2b_angle=b2b,
        )
    except KeyError:
        post = f"{consequence}.\n\nHere's what I found after {timeframe} of testing:\n\n{bullet_text}\n\n{takeaway}"

    vc = voice_check(post)
    return vc["cleaned"]


def generate_reddit(seed: dict) -> dict:
    """Generate a Reddit post (value-first, no self-promo)."""
    consequence = seed.get("consequence", "results were significant")
    method = seed.get("method", "")
    topic = seed.get("topic", "this approach")
    tool = seed.get("tool", "")
    timeframe = seed.get("timeframe", "a few weeks")
    numbers = seed.get("numbers", [])
    category = seed.get("category", "")

    subreddit_map = {
        "APP_FACTORY": ["r/SideProject", "r/indiehackers", "r/startups"],
        "TOOL_ALPHA": ["r/SaaS", "r/webdev", "r/Entrepreneur"],
        "GROWTH_HACK": ["r/Entrepreneur", "r/smallbusiness", "r/marketing"],
        "MONETIZATION": ["r/Entrepreneur", "r/passive_income", "r/indiehackers"],
        "CONTENT_FORMAT": ["r/content_marketing", "r/socialmedia", "r/marketing"],
        "OUTBOUND": ["r/sales", "r/Entrepreneur", "r/marketing"],
        "SEO_GEO_ASO": ["r/SEO", "r/webdev", "r/indiehackers"],
    }
    suggested_subs = subreddit_map.get(category, ["r/Entrepreneur", "r/SideProject"])

    title = f"I {seed.get('action', 'tested')} {topic} for {timeframe}. Here's what happened."
    if len(title) > 150:
        title = title[:147] + "..."

    intro = f"Been working on {topic} and wanted to share real results, not theory."

    steps = ""
    if method:
        parts = re.split(r'[.;]\s*', method)
        step_lines = []
        for i, part in enumerate(parts[:5]):
            part = part.strip()
            if len(part) > 10:
                step_lines.append(f"{i + 1}. {part}")
        steps = "\n".join(step_lines)

    results = consequence
    if numbers:
        results += f" ({', '.join(numbers[:3])})"

    body = ""
    if method:
        body = f"The approach:\n\n{steps}\n\n"
    body += f"Bottom line: {results}."
    if tool:
        body += f" Used {tool} for most of this."

    template = random.choice(REDDIT_TEMPLATES)
    try:
        post_text = template.format(
            title=title,
            intro=intro,
            steps=steps,
            results=results,
            body=body,
            timeframe=timeframe,
        )
    except KeyError:
        post_text = f"## {title}\n\n{intro}\n\n{body}\n\nHappy to answer questions."

    vc = voice_check(post_text)

    return {
        "title": title,
        "body": vc["cleaned"],
        "suggested_subreddits": suggested_subs,
    }


def generate_newsletter(seed: dict) -> str:
    """Generate a 2-3 paragraph newsletter section."""
    consequence = seed.get("consequence", "results were wild")
    method = seed.get("method", "")
    topic = seed.get("topic", "this approach")
    tool = seed.get("tool", "")
    timeframe = seed.get("timeframe", "this week")
    numbers = seed.get("numbers", [])

    hook = f"{consequence}. that's the headline from this week's testing."

    body_p1 = f"here's what happened: i spent {timeframe} on {topic}"
    if tool:
        body_p1 += f" using {tool}"
    body_p1 += "."
    if method:
        body_p1 += f" the method: {method[:200]}."

    body_p2 = "the numbers tell the story."
    if numbers:
        body_p2 += f" {', '.join(numbers[:3])}."
    body_p2 += f" {consequence}. and the setup was simpler than expected."

    body_p3 = f"if you're working on anything related to {topic}, this is worth testing."
    body_p3 += f" took me {timeframe} to get results. no reason you can't do the same."

    takeaway = f"the bottom line: {topic} works when you actually execute instead of planning forever."

    template = random.choice(NEWSLETTER_TEMPLATES)
    try:
        section = template.format(
            hook=hook,
            body_p1=body_p1,
            body_p2=body_p2,
            body_p3=body_p3,
            takeaway=takeaway,
        )
    except KeyError:
        section = f"{hook}\n\n{body_p1}\n\n{body_p2}\n\n{takeaway}"

    vc = voice_check(section)
    return vc["cleaned"]


def generate_gumroad_angle(seed: dict) -> Optional[str]:
    """Generate a Gumroad product angle if applicable."""
    topic = seed.get("topic", "")
    method = seed.get("method", "")
    category = seed.get("category", "")
    numbers = seed.get("numbers", [])

    productizable = ["APP_FACTORY", "TOOL_ALPHA", "GROWTH_HACK", "MONETIZATION",
                     "CONTENT_FORMAT", "OUTBOUND", "SEO_GEO_ASO"]
    has_method = len(method) > 30

    if category not in productizable and not has_method:
        return None

    price_anchors = ["$19", "$27", "$39", "$47", "$9"]
    asset_types = ["templates", "frameworks", "swipe files", "scripts", "checklists"]

    template = random.choice(GUMROAD_ANGLES)
    try:
        angle = template.format(
            topic=topic,
            method=method[:60] if method else topic,
            timeframe=seed.get("timeframe", "weeks"),
            number=numbers[0] if numbers else "50+",
            asset_type=random.choice(asset_types),
            price_anchor=random.choice(price_anchors),
        )
    except KeyError:
        angle = f"the {topic} playbook: everything tested, what worked, what didn't. {random.choice(price_anchors)}."

    vc = voice_check(angle)
    return vc["cleaned"]


# ---------------------------------------------------------------------------
# Cross-niche adaptation: generate account-specific tweet variants
# ---------------------------------------------------------------------------
NICHE_TEMPLATES = {
    "repscheme": [
        "the discipline is the same whether it's reps or {topic}. {consequence}.",
        "{consequence}. same energy as hitting a PR. consistent effort wins.",
        "no shortcuts. {consequence}. put in the work and the numbers follow.",
    ],
    "drifthour": [
        "{consequence}... let that sit for a moment.",
        "the aesthetic of doing the work quietly... {consequence}.",
        "found something worth sharing... {consequence}.",
    ],
    "voidpilled": [
        "{consequence}. the simulation rewards those who see the pattern.",
        "they don't want you to know this: {consequence}.",
        "esoteric alpha: {consequence}. hide in plain sight.",
    ],
    "selahmoments": [
        "stewardship means using every tool available. {consequence}.",
        "{consequence}. building with purpose, not just profit. selah.",
        "the work of your hands matters. {consequence}.",
    ],
}


def generate_niche_variants(seed: dict) -> dict:
    """Generate one tweet per niche account from the same seed."""
    variants = {}
    consequence = seed.get("consequence", "results were wild")
    topic = seed.get("topic", "this")

    for acct_name, templates in NICHE_TEMPLATES.items():
        template = random.choice(templates)
        try:
            tweet = template.format(
                consequence=consequence,
                topic=topic,
            )
        except KeyError:
            tweet = f"{consequence}."

        tweet = tweet.lower()
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        vc = voice_check(tweet)
        variants[acct_name] = vc["cleaned"]

    return variants


# ---------------------------------------------------------------------------
# Full content generation pipeline
# ---------------------------------------------------------------------------
def generate_all_content(seed: dict) -> dict:
    """Generate ALL content formats from a single seed."""
    log(f"Generating all content for seed: {seed.get('topic', 'unknown')[:50]}")

    result = {
        "seed": seed,
        "generated_at": datetime.now().isoformat(),
        "tweets": generate_tweets(seed, count=3),
        "thread": generate_thread(seed, length=6),
        "linkedin": generate_linkedin(seed),
        "reddit": generate_reddit(seed),
        "newsletter": generate_newsletter(seed),
        "gumroad_angle": generate_gumroad_angle(seed),
        "niche_variants": generate_niche_variants(seed),
        "voice_check_summary": {},
    }

    # Aggregate voice check
    all_texts = []
    all_texts.extend(result["tweets"])
    all_texts.extend(result["thread"])
    all_texts.append(result["linkedin"])
    all_texts.append(result["reddit"]["body"])
    all_texts.append(result["newsletter"])
    if result["gumroad_angle"]:
        all_texts.append(result["gumroad_angle"])
    all_texts.extend(result["niche_variants"].values())

    checks = voice_check_batch(all_texts)
    total_issues = sum(c["issue_count"] for c in checks)
    all_passed = all(c["passed"] for c in checks)

    result["voice_check_summary"] = {
        "all_passed": all_passed,
        "total_issues": total_issues,
        "items_checked": len(checks),
        "items_passed": sum(1 for c in checks if c["passed"]),
    }

    return result


# ---------------------------------------------------------------------------
# Save output
# ---------------------------------------------------------------------------
def save_content(content: dict, dry_run: bool = False) -> list[str]:
    """Save all generated content to CONTENT/social/auto_generated/."""
    safe_path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    seed = content.get("seed", {})
    topic_slug = re.sub(r'[^a-z0-9]+', '_', seed.get("topic", "unknown")[:30].lower()).strip("_")
    files_written = []

    if dry_run:
        print(f"\n{'='*70}")
        print(f"  CONTENT FACTORY OUTPUT (DRY RUN)")
        print(f"  Topic: {seed.get('topic', 'unknown')}")
        print(f"  Input type: {seed.get('input_type', 'text')}")
        print(f"  Voice check: {'PASSED' if content['voice_check_summary']['all_passed'] else 'ISSUES FOUND'}")
        print(f"  Issues: {content['voice_check_summary']['total_issues']}")
        print(f"{'='*70}\n")

        print("--- TWEETS (3) ---")
        for i, t in enumerate(content["tweets"], 1):
            print(f"  {i}. {t}")
            print(f"     [{len(t)} chars]")
        print()

        print("--- THREAD ({} tweets) ---".format(len(content["thread"])))
        for i, t in enumerate(content["thread"], 1):
            print(f"  {i}/{len(content['thread'])}. {t}")
        print()

        print("--- LINKEDIN ---")
        print(textwrap.indent(content["linkedin"], "  "))
        print()

        print("--- REDDIT ---")
        reddit = content["reddit"]
        print(f"  Subreddits: {', '.join(reddit['suggested_subreddits'])}")
        print(f"  Title: {reddit['title']}")
        print(textwrap.indent(reddit["body"][:500], "  "))
        print()

        print("--- NEWSLETTER ---")
        print(textwrap.indent(content["newsletter"][:500], "  "))
        print()

        if content["gumroad_angle"]:
            print("--- GUMROAD ANGLE ---")
            print(f"  {content['gumroad_angle']}")
        else:
            print("--- GUMROAD ANGLE: N/A (not productizable) ---")
        print()

        print("--- NICHE VARIANTS ---")
        for acct, tweet in content["niche_variants"].items():
            print(f"  @{acct}: {tweet}")
        print()

        return []

    # Save tweets CSV
    tweet_file = safe_path(OUTPUT_DIR / f"factory_tweets_{topic_slug}_{ts}.csv")
    with open(tweet_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "tweet_text", "format", "account", "source_topic",
            "voice_check", "status", "created_date",
        ])
        writer.writeheader()
        # Main account tweets
        for t in content["tweets"]:
            writer.writerow({
                "tweet_text": t,
                "format": "single_tweet",
                "account": "@PRINTMAXXER",
                "source_topic": seed.get("topic", ""),
                "voice_check": "PASSED" if voice_check(t)["passed"] else "NEEDS_REVIEW",
                "status": "PENDING_REVIEW",
                "created_date": datetime.now().strftime("%Y-%m-%d"),
            })
        # Niche variants
        for acct, tweet in content["niche_variants"].items():
            writer.writerow({
                "tweet_text": tweet,
                "format": "niche_variant",
                "account": f"@{acct}",
                "source_topic": seed.get("topic", ""),
                "voice_check": "PASSED" if voice_check(tweet)["passed"] else "NEEDS_REVIEW",
                "status": "PENDING_REVIEW",
                "created_date": datetime.now().strftime("%Y-%m-%d"),
            })
    files_written.append(str(tweet_file))

    # Save thread
    thread_file = safe_path(OUTPUT_DIR / f"factory_thread_{topic_slug}_{ts}.json")
    with open(thread_file, "w", encoding="utf-8") as f:
        json.dump({
            "type": "thread",
            "account": "@PRINTMAXXER",
            "topic": seed.get("topic", ""),
            "tweets": content["thread"],
            "tweet_count": len(content["thread"]),
            "status": "PENDING_REVIEW",
            "created_at": content["generated_at"],
        }, f, indent=2)
    files_written.append(str(thread_file))

    # Save LinkedIn
    li_file = safe_path(OUTPUT_DIR / f"factory_linkedin_{topic_slug}_{ts}.txt")
    with open(li_file, "w", encoding="utf-8") as f:
        f.write(f"# LinkedIn Post - {seed.get('topic', 'unknown')}\n")
        f.write(f"# Generated: {content['generated_at']}\n")
        f.write(f"# Status: PENDING_REVIEW\n\n")
        f.write(content["linkedin"])
    files_written.append(str(li_file))

    # Save Reddit
    reddit = content["reddit"]
    reddit_file = safe_path(OUTPUT_DIR / f"factory_reddit_{topic_slug}_{ts}.txt")
    with open(reddit_file, "w", encoding="utf-8") as f:
        f.write(f"# Reddit Post - {seed.get('topic', 'unknown')}\n")
        f.write(f"# Suggested subreddits: {', '.join(reddit['suggested_subreddits'])}\n")
        f.write(f"# Status: PENDING_REVIEW\n\n")
        f.write(f"Title: {reddit['title']}\n\n")
        f.write(reddit["body"])
    files_written.append(str(reddit_file))

    # Save newsletter
    nl_file = safe_path(OUTPUT_DIR / f"factory_newsletter_{topic_slug}_{ts}.txt")
    with open(nl_file, "w", encoding="utf-8") as f:
        f.write(f"# Newsletter Section - {seed.get('topic', 'unknown')}\n")
        f.write(f"# Status: PENDING_REVIEW\n\n")
        f.write(content["newsletter"])
    files_written.append(str(nl_file))

    # Save Gumroad angle
    if content["gumroad_angle"]:
        gum_file = safe_path(OUTPUT_DIR / f"factory_gumroad_{topic_slug}_{ts}.txt")
        with open(gum_file, "w", encoding="utf-8") as f:
            f.write(f"# Gumroad Product Angle - {seed.get('topic', 'unknown')}\n")
            f.write(f"# Status: PENDING_REVIEW\n\n")
            f.write(content["gumroad_angle"])
        files_written.append(str(gum_file))

    # Save combined manifest
    manifest_file = safe_path(OUTPUT_DIR / f"factory_manifest_{topic_slug}_{ts}.json")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": content["generated_at"],
            "seed_topic": seed.get("topic", ""),
            "seed_input_type": seed.get("input_type", "text"),
            "alpha_id": seed.get("alpha_id", ""),
            "voice_check_summary": content["voice_check_summary"],
            "files": files_written,
            "content_counts": {
                "tweets": len(content["tweets"]),
                "niche_variants": len(content["niche_variants"]),
                "thread_tweets": len(content["thread"]),
                "linkedin": 1,
                "reddit": 1,
                "newsletter": 1,
                "gumroad": 1 if content["gumroad_angle"] else 0,
            },
        }, f, indent=2)
    files_written.append(str(manifest_file))

    return files_written


# ---------------------------------------------------------------------------
# CLI entry points
# ---------------------------------------------------------------------------
def cmd_from_input(text: str, dry_run: bool = False) -> None:
    """Generate content from free text input."""
    log(f"Generating from input: {text[:80]}...")
    seed = extract_topic_from_text(text)
    content = generate_all_content(seed)
    files = save_content(content, dry_run=dry_run)
    if files:
        log(f"Saved {len(files)} files")
        for fp in files:
            print(f"  {fp}")
    vc = content["voice_check_summary"]
    print(f"\nVoice check: {'PASSED' if vc['all_passed'] else 'ISSUES: ' + str(vc['total_issues'])}")


def cmd_from_alpha(alpha_id: str, dry_run: bool = False) -> None:
    """Generate content from a specific alpha entry."""
    if not ALPHA_CSV.exists():
        log(f"ALPHA_STAGING.csv not found at {ALPHA_CSV}")
        return

    with open(ALPHA_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("alpha_id") or "").strip().upper() == alpha_id.upper():
                seed = extract_from_alpha(row)
                content = generate_all_content(seed)
                files = save_content(content, dry_run=dry_run)
                if files:
                    log(f"Generated content for {alpha_id}: {len(files)} files")
                    for fp in files:
                        print(f"  {fp}")
                vc = content["voice_check_summary"]
                print(f"\nVoice check: {'PASSED' if vc['all_passed'] else 'ISSUES: ' + str(vc['total_issues'])}")
                return

    log(f"Alpha ID '{alpha_id}' not found in ALPHA_STAGING.csv")
    print(f"Alpha ID '{alpha_id}' not found.")


def cmd_batch_alpha(count: int, dry_run: bool = False) -> None:
    """Generate content for N most recent approved alpha entries."""
    if not ALPHA_CSV.exists():
        log("ALPHA_STAGING.csv not found")
        return

    entries = []
    with open(ALPHA_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = (row.get("status") or "").strip().upper()
            if status in ("APPROVED", "PENDING_REVIEW"):
                entries.append(row)

    roi_order = {"HIGHEST": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    entries.sort(
        key=lambda e: roi_order.get((e.get("roi_potential") or "").upper(), 0),
        reverse=True,
    )
    entries = entries[:count]

    log(f"Batch processing {len(entries)} alpha entries")
    total_files = 0

    for entry in entries:
        seed = extract_from_alpha(entry)
        content = generate_all_content(seed)
        files = save_content(content, dry_run=dry_run)
        total_files += len(files)
        alpha_id = entry.get("alpha_id", "?")
        vc = content["voice_check_summary"]
        status = "PASSED" if vc["all_passed"] else f"ISSUES({vc['total_issues']})"
        print(f"  {alpha_id}: {len(files)} files, voice: {status}")

    log(f"Batch complete: {len(entries)} entries, {total_files} files generated")
    print(f"\nTotal: {len(entries)} entries processed, {total_files} files generated")


def cmd_from_session(dry_run: bool = False) -> None:
    """Generate content from recent session log entries."""
    seeds = extract_from_session_log()
    if not seeds:
        print("No content seeds found in session log.")
        return

    total_files = 0
    for seed in seeds[:5]:
        content = generate_all_content(seed)
        files = save_content(content, dry_run=dry_run)
        total_files += len(files)

    log(f"Session content: {len(seeds)} seeds, {total_files} files")
    print(f"\nGenerated content from {min(len(seeds), 5)} session items, {total_files} files")


def cmd_voice_check(filepath: str) -> None:
    """Run voice check on an existing content file."""
    import glob as g

    files = g.glob(filepath)
    if not files:
        files = g.glob(str(PROJECT_ROOT / filepath))
    if not files:
        print(f"No files matching: {filepath}")
        return

    total_issues = 0
    total_items = 0
    total_passed = 0

    for fpath in files:
        print(f"\n--- Voice Check: {Path(fpath).name} ---")

        if fpath.endswith(".csv"):
            with open(fpath, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    text = row.get("tweet_text", row.get("draft", ""))
                    if not text:
                        continue
                    vc = voice_check(text)
                    total_items += 1
                    if not vc["passed"]:
                        total_issues += vc["issue_count"]
                        print(f"  FAIL ({vc['issue_count']} issues): {text[:80]}...")
                        for issue in vc["issues"]:
                            print(f"    - {issue}")
                    else:
                        total_passed += 1
                        print(f"  PASS: {text[:80]}...")
        elif fpath.endswith(".json"):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                texts = data.get("tweets", [])
                if isinstance(texts, list):
                    for t in texts:
                        vc = voice_check(t)
                        total_items += 1
                        if not vc["passed"]:
                            total_issues += vc["issue_count"]
                            print(f"  FAIL: {t[:80]}...")
                        else:
                            total_passed += 1
            except (json.JSONDecodeError, AttributeError):
                pass
        else:
            text = Path(fpath).read_text(encoding="utf-8", errors="replace")
            vc = voice_check(text)
            total_items += 1
            if not vc["passed"]:
                total_issues += vc["issue_count"]
                print(f"  FAIL ({vc['issue_count']} issues)")
                for issue in vc["issues"]:
                    print(f"    - {issue}")
            else:
                total_passed += 1
                print(f"  PASS")

    print(f"\n--- Summary ---")
    print(f"  Items checked: {total_items}")
    print(f"  Passed: {total_passed}")
    print(f"  Total issues: {total_issues}")
    if total_items > 0:
        print(f"  Pass rate: {(total_passed / total_items) * 100:.0f}%")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Content Factory: one script to generate all content formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        examples:
          %(prog)s --input "cold email framework that got 40%% reply rate"
          %(prog)s --from-alpha ALPHA042
          %(prog)s --batch-alpha 10
          %(prog)s --from-session
          %(prog)s --voice-check "CONTENT/social/auto_generated/tweets_*.csv"
          %(prog)s --dry-run --input "scraper that monitors competitor pricing"
        """),
    )
    parser.add_argument(
        "--input", "-i", type=str, default=None,
        help="Free text input (topic, finding, tool discovery, etc.)",
    )
    parser.add_argument(
        "--from-alpha", type=str, default=None, metavar="ALPHA_ID",
        help="Generate from a specific alpha entry by ID",
    )
    parser.add_argument(
        "--from-session", action="store_true",
        help="Generate from recent session log entries",
    )
    parser.add_argument(
        "--batch-alpha", type=int, default=None, metavar="N",
        help="Batch generate from top N alpha entries",
    )
    parser.add_argument(
        "--voice-check", type=str, default=None, metavar="FILE",
        help="Run copy-style.md voice check on existing content file(s)",
    )
    parser.add_argument(
        "--dry-run", "-d", action="store_true",
        help="Preview output without saving files",
    )
    args = parser.parse_args()

    if args.voice_check:
        cmd_voice_check(args.voice_check)
    elif args.input:
        cmd_from_input(args.input, dry_run=args.dry_run)
    elif args.from_alpha:
        cmd_from_alpha(args.from_alpha, dry_run=args.dry_run)
    elif args.batch_alpha is not None:
        cmd_batch_alpha(args.batch_alpha, dry_run=args.dry_run)
    elif args.from_session:
        cmd_from_session(dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
