#!/usr/bin/env python3
"""
PRINTMAXX Automation System — Make.com Automation Monitor

PURPOSE: Monitor r/SideProject, r/nocode, r/makecom for Make.com AI tool builders
         and automation pain points. Extract workflow friction points as content seeds
         and service leads. Generate engagement posts around AI + Make.com automation gaps.

TYPE: scraper
METHOD CONTEXT: [ACQUISITION] Working on an AI tool for Make.com automation.
                Looking for feedback.

Cron-ready: no interactive input, clean exit codes.
Usage:
    python makecom_automation_monitor.py --run
    python makecom_automation_monitor.py --status
    python makecom_automation_monitor.py --dry-run
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

# ---------------------------------------------------------------------------
# Project root & common utilities
# ---------------------------------------------------------------------------

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path: Path) -> Path:
        """Validate that path is within PROJECT; raise ValueError otherwise."""
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path {resolved} is outside PROJECT root {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result: dict) -> None:
        pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_NAME = "makecom_automation_monitor"
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_DIR = AUTOMATIONS_DIR / "logs"
DATA_DIR = AUTOMATIONS_DIR / "data" / SCRIPT_NAME
LOG_FILE = LOG_DIR / f"{SCRIPT_NAME}.log"
LEADS_CSV = DATA_DIR / "service_leads.csv"
SEEDS_JSON = DATA_DIR / "content_seeds.json"
POSTS_JSON = DATA_DIR / "engagement_posts.json"
STATE_JSON = DATA_DIR / "state.json"

SUBREDDITS = ["SideProject", "nocode", "makecom"]

PAIN_KEYWORDS = [
    "stuck", "frustrated", "can't figure out", "struggling", "help", "broken",
    "not working", "error", "webhook", "limit", "workaround", "slow", "expensive",
    "alternative", "replace", "migrate", "can't afford", "too complex",
    "documentation", "confusing", "how do i", "is it possible", "anyone know",
    "best way to", "need help", "issue with", "problem with", "fail", "timeout",
    "rate limit", "api", "module", "scenario", "trigger", "filter", "router",
    "iterator", "aggregator", "http module", "json", "parse", "transform",
    "automate", "workflow", "integration", "connection", "oauth", "auth",
]

MAKECOM_KEYWORDS = [
    "make.com", "make ", "integromat", "scenario", "blueprint", "module",
    "webhook", "automation", "nocode", "no-code", "workflow", "zapier alternative",
    "n8n", "activepieces", "pipedream",
]

AI_KEYWORDS = [
    "ai", "chatgpt", "openai", "claude", "llm", "gpt", "artificial intelligence",
    "machine learning", "prompt", "ai agent", "automation ai", "ai workflow",
    "ai integration", "ai tool",
]

REDDIT_BASE = "https://www.reddit.com"
USER_AGENT = "PRINTMAXX:makecom-monitor:v1.0 (automation research)"
REQUEST_DELAY = 2.0  # seconds between requests — be respectful

PAIN_THEMES = [
    "complex JSON parsing",
    "webhook payload handling",
    "rate limit management",
    "error handling and retries",
    "OAuth token refresh flows",
    "multi-step data transformation",
    "dynamic routing logic",
    "AI prompt chaining inside scenarios",
    "cross-scenario data sharing",
    "API pagination loops",
    "conditional logic sprawl",
    "zero visibility when debugging",
]

ENGAGEMENT_TEMPLATES = [
    (
        "gap_question",
        (
            "Been building AI workflows in Make.com and keep hitting the same wall: "
            "{pain_theme}. Anyone else running into this? "
            "Curious what workarounds people are using — or if there's a better tool "
            "for this specific case. [Not selling anything, genuinely mapping pain points "
            "to build something useful]"
        ),
    ),
    (
        "validation_ask",
        (
            "Quick question for Make.com builders: when it comes to {pain_theme}, "
            "how are you handling it right now? "
            "I'm building an AI layer that's supposed to solve exactly this, "
            "but want to make sure I'm not solving the wrong problem. "
            "What's the most painful part of your current setup?"
        ),
    ),
    (
        "insight_share",
        (
            "Noticed a pattern in r/{subreddit}: most Make.com threads about {pain_theme} "
            "end with 'I just gave up and did it manually'. "
            "That gap between 'automation should handle this' and 'it doesn't quite work' "
            "is exactly what I'm trying to close. What's the specific step that always breaks?"
        ),
    ),
    (
        "soft_cta",
        (
            "If you've ever rage-quit a Make.com scenario because of {pain_theme}, "
            "I'd love 10 minutes of your time. "
            "Building an AI tool specifically for this and early feedback would be gold. "
            "Drop a comment or DM — happy to share what I'm building too."
        ),
    ),
]

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def setup_logging() -> logging.Logger:
    """Configure file + stream logging. File handler appends to LOG_FILE."""
    logger = logging.getLogger(SCRIPT_NAME)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    try:
        log_path = safe_path(LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except Exception as exc:
        print(f"[WARN] Cannot set up file logging: {exc}", file=sys.stderr)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger


log = setup_logging()

# ---------------------------------------------------------------------------
# Reddit scraping (urllib only)
# ---------------------------------------------------------------------------


def reddit_get(url: str) -> dict:
    """Fetch a Reddit JSON endpoint; return parsed dict."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        log.warning("HTTP %s fetching %s", exc.code, url)
        raise
    except urllib.error.URLError as exc:
        log.warning("URL error for %s: %s", url, exc.reason)
        raise


def fetch_subreddit_posts(subreddit: str, limit: int = 100) -> list:
    """Fetch recent posts from a subreddit via /new.json."""
    url = f"{REDDIT_BASE}/r/{subreddit}/new.json?limit={limit}"
    log.debug("Fetching %s", url)
    try:
        data = reddit_get(url)
        return [p["data"] for p in data.get("data", {}).get("children", [])]
    except Exception as exc:
        log.error("Failed to fetch r/%s: %s", subreddit, exc)
        return []


def search_subreddit(subreddit: str, query: str, limit: int = 50) -> list:
    """Search a subreddit for query string; returns post data dicts."""
    encoded = urllib.parse.quote(query)
    url = (
        f"{REDDIT_BASE}/r/{subreddit}/search.json"
        f"?q={encoded}&sort=new&restrict_sr=1&limit={limit}&t=month"
    )
    log.debug("Searching r/%s for '%s'", subreddit, query)
    try:
        data = reddit_get(url)
        return [p["data"] for p in data.get("data", {}).get("children", [])]
    except Exception as exc:
        log.error("Search r/%s '%s' failed: %s", subreddit, query, exc)
        return []

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------


def score_post(post: dict) -> dict:
    """Score a Reddit post for Make.com relevance, pain signals, and AI relevance."""
    text = (
        (post.get("title") or "")
        + " "
        + (post.get("selftext") or "")
        + " "
        + (post.get("url") or "")
    ).lower()

    makecom_hits = [kw for kw in MAKECOM_KEYWORDS if kw in text]
    pain_hits = [kw for kw in PAIN_KEYWORDS if kw in text]
    ai_hits = [kw for kw in AI_KEYWORDS if kw in text]

    makecom_score = len(makecom_hits)
    pain_score = len(pain_hits)
    ai_score = len(ai_hits)
    total_score = (makecom_score * 3) + (pain_score * 2) + ai_score

    return {
        "id": post.get("id", ""),
        "subreddit": post.get("subreddit", ""),
        "title": post.get("title", ""),
        "url": f"{REDDIT_BASE}{post.get('permalink', '')}",
        "author": post.get("author", "[deleted]"),
        "score": post.get("score", 0),
        "num_comments": post.get("num_comments", 0),
        "created_utc": post.get("created_utc", 0),
        "created_dt": datetime.fromtimestamp(
            post.get("created_utc", 0), tz=timezone.utc
        ).isoformat(),
        "selftext_snippet": (post.get("selftext") or "")[:300],
        "makecom_keywords": makecom_hits,
        "pain_keywords": pain_hits,
        "ai_keywords": ai_hits,
        "makecom_score": makecom_score,
        "pain_score": pain_score,
        "ai_score": ai_score,
        "total_score": total_score,
        "is_lead": makecom_score >= 1 and pain_score >= 1,
        "is_ai_gap": makecom_score >= 1 and ai_score >= 1,
        "is_seed": total_score >= 4,
    }


def extract_friction_points(scored_posts: list) -> list:
    """Deduplicate and rank posts that represent genuine Make.com friction."""
    seen = set()
    friction = []
    for post in scored_posts:
        pid = post["id"]
        if pid in seen:
            continue
        seen.add(pid)
        if post["pain_score"] >= 1 and post["makecom_score"] >= 1:
            friction.append({
                "post_id": pid,
                "subreddit": post["subreddit"],
                "title": post["title"],
                "url": post["url"],
                "friction_keywords": post["pain_keywords"][:5],
                "context_snippet": post["selftext_snippet"],
                "engagement": post["score"] + post["num_comments"],
                "created_dt": post["created_dt"],
            })
    friction.sort(key=lambda x: x["engagement"], reverse=True)
    return friction

# ---------------------------------------------------------------------------
# Engagement post generation
# ---------------------------------------------------------------------------


def generate_engagement_posts(friction_points: list, dry_run: bool = False) -> list:
    """Generate engagement post drafts from extracted friction data."""
    posts = []
    used_themes: set = set()

    for fp in friction_points[:20]:
        raw_kws = fp.get("friction_keywords", [])
        if raw_kws:
            theme = " / ".join(raw_kws[:2])
        else:
            theme = next(
                (t for t in PAIN_THEMES if t not in used_themes),
                PAIN_THEMES[len(posts) % len(PAIN_THEMES)],
            )
        used_themes.add(theme)
        subreddit = fp.get("subreddit", "makecom")

        for tpl_name, tpl_body in ENGAGEMENT_TEMPLATES:
            posts.append({
                "template": tpl_name,
                "target_subreddit": subreddit,
                "source_post_id": fp["post_id"],
                "source_url": fp["url"],
                "pain_theme": theme,
                "body": tpl_body.format(pain_theme=theme, subreddit=subreddit),
                "generated_at": datetime.now(tz=timezone.utc).isoformat(),
                "status": "dry_run" if dry_run else "draft",
            })

    log.info("Generated %d engagement post drafts", len(posts))
    return posts

# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------


def ensure_dirs() -> None:
    """Create required output directories under PROJECT."""
    for d in [LOG_DIR, DATA_DIR]:
        try:
            safe_path(d).mkdir(parents=True, exist_ok=True)
        except ValueError as exc:
            log.error("Refusing to create directory outside PROJECT: %s", exc)
            sys.exit(1)
        except OSError as exc:
            log.error("Cannot create directory %s: %s", d, exc)
            sys.exit(1)


def load_state() -> dict:
    """Load run state from JSON; return defaults if absent or corrupt."""
    try:
        p = safe_path(STATE_JSON)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as exc:
        log.warning("Could not load state: %s", exc)
    return {"seen_ids": [], "last_run": None, "total_leads": 0, "total_seeds": 0}


def save_state(state: dict) -> None:
    try:
        p = safe_path(STATE_JSON)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as exc:
        log.error("Could not save state: %s", exc)


def save_leads_csv(leads: list) -> int:
    """Append new leads to CSV; return count written."""
    if not leads:
        return 0
    try:
        p = safe_path(LEADS_CSV)
        write_header = not p.exists()
        fieldnames = [
            "id", "subreddit", "title", "url", "author",
            "score", "num_comments", "created_dt",
            "makecom_keywords", "pain_keywords", "ai_keywords",
            "total_score", "is_lead", "is_ai_gap",
        ]
        with open(p, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            if write_header:
                writer.writeheader()
            for lead in leads:
                row = dict(lead)
                for key in ("makecom_keywords", "pain_keywords", "ai_keywords"):
                    row[key] = "|".join(row.get(key, []))
                writer.writerow(row)
        log.info("Appended %d leads to %s", len(leads), p)
        return len(leads)
    except Exception as exc:
        log.error("Could not save leads CSV: %s", exc)
        return 0


def save_json_append(path: Path, new_items: list) -> None:
    """Append new_items to an existing JSON array file (or create it)."""
    try:
        p = safe_path(path)
        existing = []
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.extend(new_items)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        log.info("Saved %d items to %s (total %d)", len(new_items), p, len(existing))
    except Exception as exc:
        log.error("Could not save %s: %s", path, exc)


def dir_disk_usage(path: Path) -> str:
    """Return human-readable disk usage of path via subprocess du."""
    try:
        result = subprocess.run(
            ["du", "-sh", str(path)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.split()[0]
    except Exception:
        pass
    return "unknown"

# ---------------------------------------------------------------------------
# Core run / status
# ---------------------------------------------------------------------------


def run(dry_run: bool = False) -> int:
    """
    Full scrape → analyse → generate cycle.
    Returns 0 on success, 1 on fatal error.
    """
    log.info("=== %s START (dry_run=%s) ===", SCRIPT_NAME, dry_run)
    recall_skills_for_task(SCRIPT_NAME)

    ensure_dirs()
    state = load_state()
    seen_ids: set = set(state.get("seen_ids", []))

    all_scored: list = []

    search_terms = [
        "make.com automation",
        "make scenario help",
        "makecom error",
        "nocode ai workflow",
        "make.com alternative",
    ]

    for sub in SUBREDDITS:
        log.info("Scraping r/%s recent posts...", sub)
        posts = fetch_subreddit_posts(sub, limit=100)
        time.sleep(REQUEST_DELAY)

        search_results: list = []
        for term in search_terms:
            search_results.extend(search_subreddit(sub, term, limit=25))
            time.sleep(REQUEST_DELAY)

        combined = {p["id"]: p for p in posts + search_results}
        new_posts = [p for pid, p in combined.items() if pid not in seen_ids]
        log.info("r/%s: %d total fetched, %d new", sub, len(combined), len(new_posts))

        for post in new_posts:
            all_scored.append(score_post(post))
            seen_ids.add(post["id"])

    log.info("Total new scored posts: %d", len(all_scored))

    leads = [p for p in all_scored if p["is_lead"]]
    seeds = [p for p in all_scored if p["is_seed"]]
    log.info("Leads: %d | Seeds: %d", len(leads), len(seeds))

    friction_points = extract_friction_points(all_scored)
    log.info("Friction points: %d", len(friction_points))

    engagement_posts = generate_engagement_posts(friction_points, dry_run=dry_run)

    if dry_run:
        log.info("[DRY RUN] Would write %d leads, %d seeds, %d posts", len(leads), len(seeds), len(engagement_posts))
        if engagement_posts:
            log.info("[DRY RUN] Sample post body:\n%s", engagement_posts[0]["body"])
        log.info("=== %s DRY RUN COMPLETE ===", SCRIPT_NAME)
        return 0

    saved_leads = save_leads_csv(leads)
    save_json_append(SEEDS_JSON, seeds)
    save_json_append(POSTS_JSON, engagement_posts)

    state["seen_ids"] = list(seen_ids)
    state["last_run"] = datetime.now(tz=timezone.utc).isoformat()
    state["total_leads"] = state.get("total_leads", 0) + saved_leads
    state["total_seeds"] = state.get("total_seeds", 0) + len(seeds)
    save_state(state)

    result = {
        "run_at": state["last_run"],
        "new_leads": saved_leads,
        "new_seeds": len(seeds),
        "friction_points": len(friction_points),
        "engagement_posts_drafted": len(engagement_posts),
    }
    capture_skill_from_result(result)

    log.info("=== %s COMPLETE ===", SCRIPT_NAME)
    return 0


def status() -> int:
    """Print a summary of current run state and output file stats."""
    try:
        state = load_state()
    except Exception as exc:
        print(f"Cannot read state: {exc}", file=sys.stderr)
        return 1

    print(f"=== {SCRIPT_NAME} STATUS ===")
    print(f"Last run   : {state.get('last_run', 'never')}")
    print(f"Posts seen : {len(state.get('seen_ids', []))}")
    print(f"Total leads: {state.get('total_leads', 0)}")
    print(f"Total seeds: {state.get('total_seeds', 0)}")

    try:
        leads_path = safe_path(LEADS_CSV)
        if leads_path.exists():
            with open(leads_path, encoding="utf-8") as f:
                row_count = sum(1 for _ in f) - 1
            print(f"Leads CSV  : {leads_path} ({row_count} rows)")
        else:
            print(f"Leads CSV  : not yet created")
    except Exception as exc:
        log.warning("Could not stat leads CSV: %s", exc)

    for label, path in [("Seeds JSON", SEEDS_JSON), ("Posts JSON", POSTS_JSON)]:
        try:
            p = safe_path(path)
            if p.exists():
                with open(p, encoding="utf-8") as f:
                    items = json.load(f)
                print(f"{label:<10}: {p} ({len(items)} entries)")
            else:
                print(f"{label:<10}: not yet created")
        except Exception as exc:
            log.warning("Could not stat %s: %s", path, exc)

    try:
        data_dir = safe_path(DATA_DIR)
        if data_dir.exists():
            usage = dir_disk_usage(data_dir)
            print(f"Data dir   : {data_dir} (disk usage: {usage})")
    except Exception as exc:
        log.warning("Could not check disk usage: %s", exc)

    return 0

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "PRINTMAXX — Make.com Automation Monitor. "
            "Scrapes Reddit for Make.com automation pain points, extracts content seeds "
            "and service leads, and generates engagement post drafts."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute full scrape + analysis + generate cycle and write outputs.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print current state and output file statistics.",
    )
    group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Scrape and analyse but skip all file writes.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            sys.exit(status())
        elif args.run:
            sys.exit(run(dry_run=False))
        elif args.dry_run:
            sys.exit(run(dry_run=True))
    except KeyboardInterrupt:
        log.info("Interrupted.")
        sys.exit(0)
    except Exception as exc:
        log.exception("Unhandled exception: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()