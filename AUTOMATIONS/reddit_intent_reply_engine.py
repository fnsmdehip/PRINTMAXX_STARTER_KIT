#!/usr/bin/env python3
"""
Reddit Intent Reply Engine — PRINTMAXX Automation System

Monitors Reddit for buying-signal posts matching print/marketing keywords,
scores intent confidence on a 0-100 scale, auto-generates context-aware reply
drafts via Claude CLI, and queues them as CSV rows for human review and posting.

Proven model: Reddit intent replies → ~$1.7K/mo average conversion revenue
(Tydal method: 200 days, $12K from targeted Reddit reply engagement).

Usage:
    python reddit_intent_reply_engine.py --run        # Full scrape → score → draft → queue
    python reddit_intent_reply_engine.py --status     # Show queue and run statistics
    python reddit_intent_reply_engine.py --dry-run    # Scrape/score only, no file writes
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── Project root ──────────────────────────────────────────────────────────────
PROJECT = Path(__file__).resolve().parent.parent

# ── Import from _common (graceful fallback if module absent) ──────────────────
try:
    sys.path.insert(0, str(PROJECT))
    from _common import (
        PROJECT as _PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
    PROJECT = _PROJECT
except ImportError:

    def safe_path(path) -> Path:
        """Validate that path resolves within PROJECT and return it."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(
                f"Security: '{resolved}' is outside project root '{PROJECT}'"
            )
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result: dict) -> None:
        pass


# ── Derived paths (all validated through safe_path) ──────────────────────────
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"

LOG_FILE    = safe_path(AUTOMATIONS_DIR / "logs"                    / "reddit_intent_reply_engine.log")
QUEUE_FILE  = safe_path(AUTOMATIONS_DIR / "data"                    / "reddit_reply_queue.csv")
STATE_FILE  = safe_path(AUTOMATIONS_DIR / "state"                   / "reddit_intent_state.json")
CONFIG_FILE = safe_path(AUTOMATIONS_DIR / "config"                  / "reddit_intent_config.json")
DRAFTS_DIR  = safe_path(AUTOMATIONS_DIR / "drafts" / "reddit_replies")

# ── Logging (append, cron-safe — no interactive TTY required) ─────────────────
def _setup_logging() -> logging.Logger:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("reddit_intent_reply_engine")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8")
        fh.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        )
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)
    return logger


log = _setup_logging()

# ── Default configuration (merged with CONFIG_FILE when present) ──────────────
DEFAULT_CONFIG: dict = {
    "brand_name": "PRINTMAXX",
    "brand_description": (
        "professional large-format printing — banners, signage, vinyl, "
        "trade show displays, vehicle wraps, and custom print solutions"
    ),
    "website": "https://printmaxx.com",
    "min_intent_score": 55,
    "max_posts_per_subreddit": 25,
    "max_search_queries": 6,
    "max_search_subreddits": 3,
    "request_delay_seconds": 2.5,
    "seen_ttl_days": 30,
    "subreddits": [
        "smallbusiness",
        "entrepreneur",
        "startups",
        "marketing",
        "Etsy",
        "ecommerce",
        "Flipping",
        "realestate",
        "eventplanning",
        "weddingplanning",
        "DIY",
        "graphic_design",
        "Design",
        "print",
        "signmaking",
    ],
    "search_queries": [
        "need banner printing",
        "custom signs where to order",
        "large format printing recommendation",
        "vinyl banner best company",
        "trade show display printing",
        "recommend print shop online",
        "yard signs bulk order",
        "retractable banner stand",
        "window decal printing",
        "custom stickers bulk",
        "printing company recommendation",
        "where to get posters printed",
    ],
    "high_intent_phrases": [
        "looking for", "where can i", "anyone recommend", "need help finding",
        "best place to", "where do you", "suggestions for", "where to get",
        "need a", "want to get", "trying to find", "anyone know", "can anyone",
        "recommendation", "recommend", "advice", "suggestions", "which company",
        "how do i get", "how do i find", "anyone use", "does anyone know",
        "any good", "any suggestions", "what do you use", "where should i",
    ],
    "product_keywords": [
        "print", "banner", "sign", "signage", "poster", "vinyl", "decal",
        "sticker", "flyer", "brochure", "trade show", "display", "backdrop",
        "large format", "wide format", "custom print", "printing company",
        "print shop", "bulk print", "marketing material", "promotional",
        "vehicle wrap", "window graphic", "floor graphic", "event banner",
        "retractable", "pop-up display", "fabric banner", "mesh banner",
        "yard sign", "corrugated", "foam board", "canvas print", "tablecloth",
        "table cover", "feather flag", "teardrop flag", "pull-up banner",
    ],
    "negative_signals": [
        "i sell", "my shop sells", "i offer", "check out my", "dm me",
        "hire me", "my etsy", "promo code", "affiliate", "[deleted]", "[removed]",
        "self promotion", "my service",
    ],
    "score_weights": {
        "high_intent_phrase": 25,
        "product_keyword_first": 20,
        "product_keyword_additional": 8,
        "product_keyword_cap_multiplier": 3,
        "title_keyword_bonus": 10,
        "recency_1h": 15,
        "recency_6h": 8,
        "recency_24h": 3,
        "has_body": 5,
        "negative_signal": -25,
    },
}


# ── Config I/O ────────────────────────────────────────────────────────────────
def load_config() -> dict:
    """Load user config from JSON, merging over defaults."""
    try:
        if CONFIG_FILE.exists():
            with open(safe_path(CONFIG_FILE), "r", encoding="utf-8") as fh:
                user_cfg = json.load(fh)
            merged = {**DEFAULT_CONFIG, **user_cfg}
            log.info("Config loaded from %s", CONFIG_FILE)
            return merged
    except Exception as exc:
        log.warning("Could not load config (%s); using defaults.", exc)
    return dict(DEFAULT_CONFIG)


# ── State: seen post IDs with timestamps ──────────────────────────────────────
def load_state() -> dict:
    try:
        if STATE_FILE.exists():
            with open(safe_path(STATE_FILE), "r", encoding="utf-8") as fh:
                return json.load(fh)
    except Exception as exc:
        log.warning("Could not load state: %s", exc)
    return {"seen_ids": {}, "last_run": None, "total_queued": 0}


def save_state(state: dict) -> None:
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path(STATE_FILE), "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
    except Exception as exc:
        log.error("Could not save state: %s", exc)


def prune_seen_ids(state: dict, ttl_days: int) -> dict:
    """Remove stale seen IDs to prevent unbounded state file growth."""
    cutoff = datetime.now(timezone.utc).timestamp() - (ttl_days * 86_400)
    before = len(state.get("seen_ids", {}))
    state["seen_ids"] = {
        k: v for k, v in state.get("seen_ids", {}).items() if v >= cutoff
    }
    removed = before - len(state["seen_ids"])
    if removed:
        log.info("Pruned %d expired seen IDs (TTL=%d days).", removed, ttl_days)
    return state


# ── Reddit JSON API (urllib only, no third-party deps) ────────────────────────
_REDDIT_HEADERS = {
    "User-Agent": "PRINTMAXX-IntentBot/1.0 (+https://printmaxx.com; contact@printmaxx.com)"
}


def _reddit_get(url: str, delay: float) -> Optional[dict]:
    """GET a Reddit JSON endpoint; return parsed dict or None on failure."""
    try:
        req = urllib.request.Request(url, headers=_REDDIT_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            log.warning("Rate-limited by Reddit (429). Sleeping 60s.")
            time.sleep(60)
        else:
            log.warning("HTTP %s for %s", exc.code, url)
    except urllib.error.URLError as exc:
        log.warning("URL error for %s: %s", url, exc)
    except Exception as exc:
        log.warning("Unexpected error fetching %s: %s", url, exc)
    finally:
        time.sleep(delay)
    return None


def _normalise_post(raw: dict, subreddit: str) -> dict:
    return {
        "id":          raw.get("id", ""),
        "subreddit":   raw.get("subreddit", subreddit),
        "title":       raw.get("title", ""),
        "body":        raw.get("selftext", ""),
        "url":         "https://www.reddit.com" + raw.get("permalink", ""),
        "author":      raw.get("author", "[unknown]"),
        "created_utc": float(raw.get("created_utc", 0)),
        "upvotes":     raw.get("score", 0),
        "num_comments":raw.get("num_comments", 0),
        "flair":       raw.get("link_flair_text", "") or "",
    }


def fetch_new_posts(subreddit: str, limit: int, delay: float) -> list:
    url = (
        f"https://www.reddit.com/r/{subreddit}/new.json"
        f"?limit={limit}&raw_json=1"
    )
    data = _reddit_get(url, delay)
    if not data:
        return []
    posts = []
    try:
        for child in data["data"]["children"]:
            posts.append(_normalise_post(child["data"], subreddit))
    except (KeyError, TypeError) as exc:
        log.warning("Parse error r/%s /new: %s", subreddit, exc)
    return posts


def search_subreddit(subreddit: str, query: str, limit: int, delay: float) -> list:
    q = urllib.parse.quote(query)
    url = (
        f"https://www.reddit.com/r/{subreddit}/search.json"
        f"?q={q}&restrict_sr=1&sort=new&limit={limit}&raw_json=1"
    )
    data = _reddit_get(url, delay)
    if not data:
        return []
    posts = []
    try:
        for child in data["data"]["children"]:
            posts.append(_normalise_post(child["data"], subreddit))
    except (KeyError, TypeError) as exc:
        log.warning("Parse error searching r/%s '%s': %s", subreddit, query, exc)
    return posts


# ── Intent scoring ─────────────────────────────────────────────────────────────
def score_post(post: dict, config: dict) -> tuple:
    """
    Score a post's buying intent 0–100.
    Returns (score: int, matched_signals: list[str]).
    """
    w = config["score_weights"]
    text = (post["title"] + " " + post["body"]).lower()
    title = post["title"].lower()
    signals = []
    total = 0

    # Negative signals first
    for neg in config["negative_signals"]:
        if neg.lower() in text:
            total += w["negative_signal"]
            signals.append(f"NEG:{neg}")

    # High-intent buying phrases
    for phrase in config["high_intent_phrases"]:
        if phrase.lower() in text:
            total += w["high_intent_phrase"]
            signals.append(f"INTENT:{phrase}")
            break  # one is enough — avoid double-counting synonyms

    # Product keyword matches
    matched_kws = [kw for kw in config["product_keywords"] if kw.lower() in text]
    if matched_kws:
        kw_score = w["product_keyword_first"] + w["product_keyword_additional"] * min(
            len(matched_kws) - 1,
            w["product_keyword_cap_multiplier"],
        )
        total += kw_score
        signals.extend(f"KW:{kw}" for kw in matched_kws[:6])

    # Title-presence bonus (keyword visible before clicking)
    for kw in config["product_keywords"]:
        if kw.lower() in title:
            total += w["title_keyword_bonus"]
            signals.append(f"TITLE_KW:{kw}")
            break

    # Recency bonus
    age = datetime.now(timezone.utc).timestamp() - post["created_utc"]
    if age < 3_600:
        total += w["recency_1h"];  signals.append("RECENCY:<1h")
    elif age < 21_600:
        total += w["recency_6h"];  signals.append("RECENCY:<6h")
    elif age < 86_400:
        total += w["recency_24h"]; signals.append("RECENCY:<24h")

    # Has a real body (more context for reply)
    if post["body"] and len(post["body"]) > 60:
        total += w["has_body"]; signals.append("HAS_BODY")

    return max(0, min(100, total)), signals


# ── Reply draft generation ─────────────────────────────────────────────────────
def _build_claude_prompt(post: dict, config: dict) -> str:
    age_s = datetime.now(timezone.utc).timestamp() - post["created_utc"]
    age_str = f"{int(age_s/3600)}h ago" if age_s > 3600 else f"{int(age_s/60)}m ago"
    body_excerpt = (post["body"] or "(no body text)")[:700].strip()
    return (
        f"You are a genuine Reddit community member who happens to work at "
        f"{config['brand_name']}, which provides {config['brand_description']}.\n\n"
        f"A Reddit user posted on r/{post['subreddit']} {age_str}:\n\n"
        f"TITLE: {post['title']}\n"
        f"BODY: {body_excerpt}\n\n"
        f"Write a single Reddit reply that:\n"
        f"1. Directly addresses their specific question or need\n"
        f"2. Feels authentic and community-appropriate — never promotional or salesy\n"
        f"3. Mentions {config['brand_name']} only if it genuinely fits (optional)\n"
        f"4. Is 2–5 sentences, written in natural Reddit voice\n"
        f"5. Does NOT start with 'I' or open with a compliment\n"
        f"6. Does NOT include bare URLs (a reviewer adds those)\n\n"
        f"Output only the reply text, nothing else:"
    )


def generate_reply_draft(post: dict, config: dict) -> str:
    """Generate a reply via Claude CLI subprocess; fall back to template on failure."""
    prompt = _build_claude_prompt(post, config)
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=45,
        )
        if result.returncode == 0 and result.stdout.strip():
            draft = result.stdout.strip()
            log.info(
                "Claude draft OK for %s (%d chars)", post["id"], len(draft)
            )
            return draft
        if result.stderr:
            log.warning("Claude stderr [%s]: %s", post["id"], result.stderr[:200])
    except FileNotFoundError:
        log.warning("Claude CLI not found; using template for %s.", post["id"])
    except subprocess.TimeoutExpired:
        log.warning("Claude CLI timeout for %s; using template.", post["id"])
    except Exception as exc:
        log.warning("Claude CLI error for %s: %s", post["id"], exc)

    return _template_reply(post, config)


def _template_reply(post: dict, config: dict) -> str:
    """Deterministic fallback when Claude CLI is unavailable."""
    title = post["title"].lower()
    brand = config["brand_name"]
    if any(k in title for k in ("banner", "vinyl", "sign", "backdrop")):
        return (
            "For large-format work the most important things are: resolution (at least 100 dpi "
            "at final size), correct bleed/margin setup, and always request a digital proof "
            f"before they run the job. Reputable shops like {brand} include proofs automatically. "
            "Happy to answer questions on file setup if that helps."
        )
    if any(k in title for k in ("sticker", "decal", "label")):
        return (
            "Worth understanding die-cut vs. kiss-cut before you order — it affects application "
            "significantly. Material choice (vinyl vs. paper, matte vs. gloss) depends on where "
            "they'll end up. What's the intended surface and environment?"
        )
    if any(k in title for k in ("trade show", "display", "retractable", "pop-up")):
        return (
            "Key variables are portability, setup time, and whether you need fabric or vinyl "
            "graphic panels. Fabric prints typically look sharper under trade show lighting. "
            "What's the booth size/format? That narrows things down fast."
        )
    return (
        "The main levers are quantity, material, and turnaround. Always request a digital proof "
        "before production — it's the single best way to avoid a costly reprint. "
        f"What's the application? That'll help narrow down the right substrate and finish."
    )


# ── Draft file persistence ─────────────────────────────────────────────────────
def save_draft_json(post: dict, draft: str, score: int, signals: list) -> Path:
    """Write a per-post JSON draft file; returns the file path."""
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{post['id']}_{post['subreddit']}.json"
    filepath = safe_path(DRAFTS_DIR / filename)
    payload = {
        "post_id":       post["id"],
        "subreddit":     post["subreddit"],
        "title":         post["title"],
        "post_url":      post["url"],
        "author":        post["author"],
        "created_utc":   post["created_utc"],
        "intent_score":  score,
        "signals":       signals,
        "reply_draft":   draft,
        "status":        "pending",
        "generated_at":  datetime.now(timezone.utc).isoformat(),
    }
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    return filepath


# ── Queue (CSV) management ────────────────────────────────────────────────────
_QUEUE_HEADERS = [
    "queued_at", "post_id", "subreddit", "title", "post_url",
    "author", "intent_score", "signals", "reply_draft", "status",
]


def _ensure_queue_file() -> None:
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not QUEUE_FILE.exists():
        with open(safe_path(QUEUE_FILE), "w", newline="", encoding="utf-8") as fh:
            csv.DictWriter(fh, fieldnames=_QUEUE_HEADERS).writeheader()


def add_to_queue(post: dict, score: int, signals: list, draft: str) -> None:
    _ensure_queue_file()
    row = {
        "queued_at":    datetime.now(timezone.utc).isoformat(),
        "post_id":      post["id"],
        "subreddit":    post["subreddit"],
        "title":        post["title"][:200],
        "post_url":     post["url"],
        "author":       post["author"],
        "intent_score": score,
        "signals":      "|".join(signals[:12]),
        "reply_draft":  draft.replace("\n", " "),
        "status":       "pending",
    }
    with open(safe_path(QUEUE_FILE), "a", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=_QUEUE_HEADERS).writerow(row)


def get_queue_stats() -> dict:
    counts = {"total": 0, "pending": 0, "posted": 0, "skipped": 0, "error": 0}
    if not QUEUE_FILE.exists():
        return counts
    try:
        with open(safe_path(QUEUE_FILE), "r", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                counts["total"] += 1
                status = row.get("status", "pending")
                if status in counts:
                    counts[status] += 1
    except Exception as exc:
        log.warning("Could not read queue file: %s", exc)
    return counts


# ── Full pipeline ──────────────────────────────────────────────────────────────
def run_pipeline(config: dict, dry_run: bool) -> dict:
    """
    Orchestrate: scrape → deduplicate → score → generate drafts → queue.
    Returns a summary dict.
    """
    log.info("=== Reddit Intent Reply Engine START | dry_run=%s ===", dry_run)
    recall_skills_for_task("reddit buying-intent monitoring and reply generation")

    state = load_state()
    state = prune_seen_ids(state, config.get("seen_ttl_days", 30))
    seen_ids: dict = state.get("seen_ids", {})

    delay  = config.get("request_delay_seconds", 2.5)
    limit  = config.get("max_posts_per_subreddit", 25)

    # ── 1. Fetch /new from every configured subreddit ────────────────────────
    all_posts: list = []
    for sub in config.get("subreddits", []):
        log.info("Fetching /new from r/%s (limit=%d) …", sub, limit)
        posts = fetch_new_posts(sub, limit=limit, delay=delay)
        all_posts.extend(posts)
        log.info("  → %d posts", len(posts))

    # ── 2. Targeted search queries on top N subreddits ───────────────────────
    search_subs  = config.get("subreddits", [])[:config.get("max_search_subreddits", 3)]
    search_qs    = config.get("search_queries", [])[:config.get("max_search_queries", 6)]
    for query in search_qs:
        for sub in search_subs:
            posts = search_subreddit(sub, query, limit=5, delay=delay)
            all_posts.extend(posts)

    # ── 3. Deduplicate by post ID ─────────────────────────────────────────────
    seen_this_run: set = set()
    unique_posts: list = []
    for p in all_posts:
        if p["id"] and p["id"] not in seen_this_run:
            seen_this_run.add(p["id"])
            unique_posts.append(p)
    log.info("Unique posts collected: %d", len(unique_posts))

    # ── 4. Filter previously-seen posts ──────────────────────────────────────
    new_posts = [p for p in unique_posts if p["id"] not in seen_ids]
    log.info("New (unseen) posts: %d", len(new_posts))

    # ── 5. Score and threshold filter ────────────────────────────────────────
    min_score = config.get("min_intent_score", 55)
    qualified: list = []
    for post in new_posts:
        score, signals = score_post(post, config)
        if score >= min_score:
            qualified.append((post, score, signals))
    qualified.sort(key=lambda x: x[1], reverse=True)
    log.info("Posts above score threshold (%d): %d", min_score, len(qualified))

    # ── 6. Generate drafts, save files, queue ────────────────────────────────
    queued = 0
    for post, score, signals in qualified:
        log.info(
            "  [score=%d] r/%s — %s",
            score, post["subreddit"], post["title"][:70],
        )
        if not dry_run:
            try:
                draft = generate_reply_draft(post, config)
                save_draft_json(post, draft, score, signals)
                add_to_queue(post, score, signals, draft)
                queued += 1
            except Exception as exc:
                log.error("Failed to draft/queue post %s: %s", post["id"], exc)

        # Always mark seen so we don't re-evaluate on next run
        seen_ids[post["id"]] = datetime.now(timezone.utc).timestamp()

    # ── 7. Persist state ─────────────────────────────────────────────────────
    state["seen_ids"]     = seen_ids
    state["last_run"]     = datetime.now(timezone.utc).isoformat()
    state["total_queued"] = state.get("total_queued", 0) + queued
    if not dry_run:
        save_state(state)

    summary = {
        "scraped":   len(unique_posts),
        "new":       len(new_posts),
        "qualified": len(qualified),
        "queued":    queued,
        "dry_run":   dry_run,
    }
    capture_skill_from_result({"action": "reddit_intent_pipeline", "summary": summary})

    log.info(
        "=== DONE — scraped=%d new=%d qualified=%d queued=%d ===",
        summary["scraped"], summary["new"], summary["qualified"], summary["queued"],
    )
    return summary


# ── Status display ─────────────────────────────────────────────────────────────
def show_status(config: dict) -> None:
    state = load_state()
    stats = get_queue_stats()
    print()
    print("=== PRINTMAXX Reddit Intent Reply Engine — STATUS ===")
    print(f"  Brand:             {config.get('brand_name')}")
    print(f"  Last run:          {state.get('last_run', 'never')}")
    print(f"  Seen IDs in state: {len(state.get('seen_ids', {}))}")
    print(f"  Total ever queued: {state.get('total_queued', 0)}")
    print(f"  Queue file:        {QUEUE_FILE}")
    print(f"  Log file:          {LOG_FILE}")
    print()
    print("  Queue breakdown:")
    print(f"    Total rows : {stats['total']}")
    print(f"    Pending    : {stats['pending']}")
    print(f"    Posted     : {stats['posted']}")
    print(f"    Skipped    : {stats['skipped']}")
    print(f"    Error      : {stats['error']}")
    print()
    subs = config.get("subreddits", [])
    print(f"  Subreddits ({len(subs)}): {', '.join(subs[:6])} ...")
    print(f"  Min intent score:  {config.get('min_intent_score')}")
    print("=" * 53)
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="reddit_intent_reply_engine.py",
        description="PRINTMAXX Reddit Intent Reply Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python reddit_intent_reply_engine.py --run\n"
            "  python reddit_intent_reply_engine.py --status\n"
            "  python reddit_intent_reply_engine.py --dry-run\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Run full pipeline: scrape → score → draft → queue",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print queue and run statistics, then exit",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Scrape and score only; no drafts generated, no files written",
    )
    return parser.parse_args()


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    args = parse_args()
    config = load_config()

    try:
        if args.status:
            show_status(config)

        elif args.dry_run:
            summary = run_pipeline(config, dry_run=True)
            print(
                f"\nDry run complete: {summary['scraped']} scraped, "
                f"{summary['new']} new, {summary['qualified']} qualified "
                f"(no writes performed)."
            )

        elif args.run:
            summary = run_pipeline(config, dry_run=False)
            print(
                f"\nRun complete: {summary['scraped']} scraped, "
                f"{summary['new']} new, {summary['qualified']} qualified, "
                f"{summary['queued']} drafts queued."
            )

    except KeyboardInterrupt:
        log.info("Interrupted.")
        sys.exit(0)
    except Exception as exc:
        log.exception("Fatal error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()