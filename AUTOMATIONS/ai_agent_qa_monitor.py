#!/usr/bin/env python3
"""
PRINTMAXX Automation: AI Agent Q&A Monitor
==========================================
Daily scraper that monitors Context Overflow and Hacker News AI agent threads
for unanswered questions and trending pain points. Extracts content seeds for
Twitter threads, Reddit posts, and longtail SEO pages. Also surfaces HN
commenters building AI agents as warm B2B outreach targets.

Cron example:
    0 7 * * * /usr/bin/python3 /path/to/AUTOMATIONS/scripts/ai_agent_qa_monitor.py --run
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

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path: Path) -> Path:
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escape blocked: {resolved} is outside {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str):
        return None

    def capture_skill_from_result(result, task: str):
        return None


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_PATH = AUTOMATIONS_DIR / "logs" / "ai_agent_qa_monitor.log"
DATA_DIR = AUTOMATIONS_DIR / "data" / "ai_agent_qa_monitor"
STATUS_FILE = DATA_DIR / "status.json"
SEEDS_CSV = DATA_DIR / "content_seeds.csv"
OUTREACH_CSV = DATA_DIR / "b2b_outreach_targets.csv"

HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"
HN_SEARCH_DATE_URL = "https://hn.algolia.com/api/v1/search_by_date"
CONTEXT_OVERFLOW_BASE = "https://contextoverflow.com"

AI_AGENT_KEYWORDS = [
    "ai agent",
    "llm agent",
    "autonomous agent",
    "agent workflow",
    "context overflow",
    "tool calling",
    "function calling",
    "agentic",
    "multi-agent",
    "rag pipeline",
    "ai automation",
    "prompt engineering",
    "langchain",
    "langgraph",
    "crewai",
    "autogen",
]

PAIN_POINT_SIGNALS = [
    "how do i",
    "how to",
    "struggling with",
    "can't figure out",
    "anyone know",
    "best way to",
    "problem with",
    "issue with",
    "broken",
    "doesn't work",
    "help needed",
    "confused about",
    "not sure how",
    "anyone dealt with",
    "anyone else having",
]

CONTENT_TYPE_MAP = {
    "question": "twitter_thread",
    "pain_point": "reddit_post",
    "trending": "seo_page",
}

REQUEST_TIMEOUT = 15
REQUEST_DELAY = 1.5  # seconds between requests — be polite

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def setup_logging() -> logging.Logger:
    log_file = safe_path(LOG_PATH)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("ai_agent_qa_monitor")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(str(log_file), mode="a", encoding="utf-8")
        fh.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)
    return logger


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def fetch_json(url: str, params: dict = None, logger: logging.Logger = None) -> dict:
    """Fetch JSON from a URL with optional query params. Returns empty dict on error."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "PRINTMAXX-AIMonitor/1.0 (content research bot; contact@printmaxx.io)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        if logger:
            logger.warning("HTTP %s fetching %s", exc.code, url)
    except urllib.error.URLError as exc:
        if logger:
            logger.warning("URL error fetching %s: %s", url, exc.reason)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        if logger:
            logger.warning("Parse error for %s: %s", url, exc)
    except Exception as exc:  # noqa: BLE001
        if logger:
            logger.warning("Unexpected error fetching %s: %s", url, exc)
    return {}


def fetch_html(url: str, logger: logging.Logger = None) -> str:
    """Fetch raw HTML from a URL. Returns empty string on error."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "PRINTMAXX-AIMonitor/1.0 (content research bot; contact@printmaxx.io)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        if logger:
            logger.warning("Failed to fetch HTML from %s: %s", url, exc)
    return ""


# ---------------------------------------------------------------------------
# Text analysis helpers
# ---------------------------------------------------------------------------


def contains_ai_agent_topic(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in AI_AGENT_KEYWORDS)


def contains_pain_point(text: str) -> bool:
    lower = text.lower()
    return any(signal in lower for signal in PAIN_POINT_SIGNALS)


def is_question(text: str) -> bool:
    stripped = text.strip()
    return stripped.endswith("?") or stripped.lower().startswith(
        ("what ", "why ", "how ", "when ", "where ", "which ", "who ", "is ", "are ", "can ", "does ", "do ")
    )


def classify_seed_type(title: str, body: str = "") -> str:
    combined = f"{title} {body}"
    if is_question(title):
        return "question"
    if contains_pain_point(combined):
        return "pain_point"
    return "trending"


def score_item(title: str, points: int, num_comments: int) -> float:
    """Simple relevance score: keyword density + engagement proxy."""
    lower = title.lower()
    kw_hits = sum(1 for kw in AI_AGENT_KEYWORDS if kw in lower)
    pain_hits = sum(1 for s in PAIN_POINT_SIGNALS if s in lower)
    engagement = (points or 0) * 0.4 + (num_comments or 0) * 0.6
    return round(kw_hits * 10 + pain_hits * 5 + engagement, 2)


def generate_content_angle(seed_type: str, title: str) -> str:
    if seed_type == "question":
        return f"Thread: We answer this so you don't have to — '{title}'"
    if seed_type == "pain_point":
        return f"Pain point post: '{title}' — here's the fix and why it matters"
    return f"SEO page: Complete guide to '{title}'"


def generate_outreach_note(username: str, comment_text: str) -> str:
    snippet = comment_text[:120].replace("\n", " ").strip()
    return (
        f"HN user @{username} is actively building AI agents (comment: '{snippet}...'). "
        "Warm lead for PRINTMAXX automation tools."
    )


# ---------------------------------------------------------------------------
# HN scraper
# ---------------------------------------------------------------------------


def scrape_hn_ai_threads(logger: logging.Logger, dry_run: bool = False) -> tuple[list[dict], list[dict]]:
    """
    Search HN for AI agent discussions.
    Returns (content_seeds, outreach_targets).
    """
    logger.info("Scraping Hacker News for AI agent threads...")
    seeds = []
    targets = []

    for keyword in ["ai agent", "llm agent", "context overflow", "agentic workflow"]:
        if dry_run:
            logger.info("[DRY-RUN] Would search HN for: %s", keyword)
            continue

        params = {
            "query": keyword,
            "tags": "(story,comment)",
            "hitsPerPage": 30,
        }
        data = fetch_json(HN_SEARCH_URL, params=params, logger=logger)
        hits = data.get("hits", [])
        logger.info("  HN '%s': %d hits", keyword, len(hits))

        for hit in hits:
            story_id = hit.get("objectID", "")
            hit_type = hit.get("_tags", ["unknown"])[0]
            title = hit.get("title") or hit.get("story_title") or ""
            comment_text = hit.get("comment_text") or ""
            author = hit.get("author", "")
            points = hit.get("points") or 0
            num_comments = hit.get("num_comments") or 0
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
            created_at = hit.get("created_at", "")

            combined_text = f"{title} {comment_text}"
            if not contains_ai_agent_topic(combined_text):
                continue

            # Content seed from stories
            if hit_type == "story" and title:
                seed_type = classify_seed_type(title, comment_text)
                score = score_item(title, points, num_comments)
                seeds.append(
                    {
                        "source": "hacker_news",
                        "id": story_id,
                        "title": title,
                        "url": url,
                        "author": author,
                        "points": points,
                        "comments": num_comments,
                        "seed_type": seed_type,
                        "content_format": CONTENT_TYPE_MAP.get(seed_type, "twitter_thread"),
                        "content_angle": generate_content_angle(seed_type, title),
                        "score": score,
                        "created_at": created_at,
                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                    }
                )

            # B2B outreach targets: commenters actively building AI agents
            if hit_type == "comment" and author and comment_text:
                builder_signals = [
                    "building",
                    "i built",
                    "we built",
                    "working on",
                    "i made",
                    "launched",
                    "shipped",
                    "my project",
                    "our tool",
                ]
                if any(sig in comment_text.lower() for sig in builder_signals):
                    targets.append(
                        {
                            "source": "hacker_news",
                            "username": author,
                            "profile_url": f"https://news.ycombinator.com/user?id={author}",
                            "comment_url": f"https://news.ycombinator.com/item?id={story_id}",
                            "comment_snippet": comment_text[:200].replace("\n", " "),
                            "outreach_note": generate_outreach_note(author, comment_text),
                            "scraped_at": datetime.now(timezone.utc).isoformat(),
                        }
                    )

        time.sleep(REQUEST_DELAY)

    # Also fetch the Context Overflow Show HN thread specifically
    hn_co_seeds, hn_co_targets = scrape_hn_context_overflow_thread(logger, dry_run)
    seeds.extend(hn_co_seeds)
    targets.extend(hn_co_targets)

    logger.info("HN total: %d seeds, %d outreach targets", len(seeds), len(targets))
    return seeds, targets


def scrape_hn_context_overflow_thread(logger: logging.Logger, dry_run: bool = False) -> tuple[list[dict], list[dict]]:
    """Fetch comments from the Show HN: Context Overflow thread."""
    seeds = []
    targets = []

    if dry_run:
        logger.info("[DRY-RUN] Would fetch HN Context Overflow Show HN thread")
        return seeds, targets

    params = {"query": "Show HN Context Overflow AI Agents", "tags": "story", "hitsPerPage": 5}
    data = fetch_json(HN_SEARCH_URL, params=params, logger=logger)
    hits = data.get("hits", [])
    time.sleep(REQUEST_DELAY)

    for hit in hits:
        story_id = hit.get("objectID", "")
        title = hit.get("title", "")
        if "context overflow" not in title.lower():
            continue

        logger.info("  Found Context Overflow Show HN thread: %s", story_id)
        # Fetch comments via HN Firebase API (no auth needed)
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        item_data = fetch_json(item_url, logger=logger)
        kids = item_data.get("kids", [])[:50]  # top 50 comment IDs
        time.sleep(REQUEST_DELAY)

        for kid_id in kids:
            comment_url = f"https://hacker-news.firebaseio.com/v0/item/{kid_id}.json"
            comment_data = fetch_json(comment_url, logger=logger)
            author = comment_data.get("by", "")
            text = comment_data.get("text", "")
            time.sleep(0.3)

            if not text or not author:
                continue

            # Strip HTML entities crudely (no html module)
            text_clean = (
                text.replace("&#x27;", "'")
                .replace("&quot;", '"')
                .replace("&amp;", "&")
                .replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("<p>", " ")
                .replace("</p>", " ")
            )

            if contains_ai_agent_topic(text_clean) or is_question(text_clean):
                seed_type = classify_seed_type("", text_clean)
                score = score_item(text_clean[:80], 0, 0)
                seeds.append(
                    {
                        "source": "hn_context_overflow_thread",
                        "id": str(kid_id),
                        "title": text_clean[:120].strip(),
                        "url": f"https://news.ycombinator.com/item?id={kid_id}",
                        "author": author,
                        "points": 0,
                        "comments": 0,
                        "seed_type": seed_type,
                        "content_format": CONTENT_TYPE_MAP.get(seed_type, "twitter_thread"),
                        "content_angle": generate_content_angle(seed_type, text_clean[:80]),
                        "score": score,
                        "created_at": "",
                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                    }
                )

            builder_signals = ["building", "i built", "working on", "launched", "my tool", "we're building"]
            if any(sig in text_clean.lower() for sig in builder_signals):
                targets.append(
                    {
                        "source": "hn_context_overflow_thread",
                        "username": author,
                        "profile_url": f"https://news.ycombinator.com/user?id={author}",
                        "comment_url": f"https://news.ycombinator.com/item?id={kid_id}",
                        "comment_snippet": text_clean[:200],
                        "outreach_note": generate_outreach_note(author, text_clean),
                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                    }
                )

    return seeds, targets


# ---------------------------------------------------------------------------
# Context Overflow scraper
# ---------------------------------------------------------------------------


def scrape_context_overflow(logger: logging.Logger, dry_run: bool = False) -> tuple[list[dict], list[dict]]:
    """
    Scrape Context Overflow for unanswered questions and trending posts.
    Tries common API/HTML endpoints; degrades gracefully if unreachable.
    Returns (content_seeds, outreach_targets).
    """
    logger.info("Scraping Context Overflow...")
    seeds = []
    targets = []

    if dry_run:
        logger.info("[DRY-RUN] Would scrape %s", CONTEXT_OVERFLOW_BASE)
        return seeds, targets

    # Try the /api/questions endpoint first (Stack Exchange-style APIs are common)
    api_endpoints = [
        f"{CONTEXT_OVERFLOW_BASE}/api/questions?sort=newest&filter=unanswered&pagesize=50",
        f"{CONTEXT_OVERFLOW_BASE}/api/v1/questions?answered=false&limit=50",
        f"{CONTEXT_OVERFLOW_BASE}/questions?tab=unanswered&sort=newest",
    ]

    fetched_any = False
    for endpoint in api_endpoints:
        raw = fetch_html(endpoint, logger=logger)
        if not raw:
            time.sleep(REQUEST_DELAY)
            continue

        fetched_any = True
        # Attempt JSON parse first
        try:
            data = json.loads(raw)
            questions = (
                data.get("questions")
                or data.get("items")
                or data.get("results")
                or (data if isinstance(data, list) else [])
            )
            for q in questions:
                title = q.get("title") or q.get("name") or ""
                body = q.get("body") or q.get("description") or ""
                q_id = q.get("id") or q.get("question_id") or ""
                answer_count = q.get("answer_count") or q.get("answers") or 0
                votes = q.get("score") or q.get("votes") or 0
                author = q.get("owner", {}).get("user_name") or q.get("author") or ""
                q_url = q.get("link") or q.get("url") or f"{CONTEXT_OVERFLOW_BASE}/questions/{q_id}"
                created_at = q.get("creation_date") or q.get("created_at") or ""

                if not title:
                    continue

                seed_type = classify_seed_type(title, body)
                score = score_item(title, votes, 0)
                seeds.append(
                    {
                        "source": "context_overflow",
                        "id": str(q_id),
                        "title": title,
                        "url": q_url,
                        "author": author,
                        "points": votes,
                        "comments": 0,
                        "answer_count": answer_count,
                        "is_unanswered": answer_count == 0,
                        "seed_type": seed_type,
                        "content_format": CONTENT_TYPE_MAP.get(seed_type, "seo_page"),
                        "content_angle": generate_content_angle(seed_type, title),
                        "score": score,
                        "created_at": str(created_at),
                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
                logger.info("    [CO] seed: %s", title[:80])
            break  # success

        except (json.JSONDecodeError, AttributeError):
            # HTML response — extract question titles heuristically
            seeds.extend(_parse_co_html(raw, logger))
            break

        time.sleep(REQUEST_DELAY)

    if not fetched_any:
        logger.warning("Context Overflow unreachable — skipping (site may not be live yet)")

    logger.info("Context Overflow: %d seeds, %d outreach targets", len(seeds), len(targets))
    return seeds, targets


def _parse_co_html(html: str, logger: logging.Logger) -> list[dict]:
    """Naive HTML extraction for question titles when JSON API is unavailable."""
    seeds = []
    # Look for common question list patterns in HTML
    import re  # stdlib only

    # Match <a href="/questions/NNN">Title text</a> patterns
    pattern = re.compile(
        r'href=["\'](/questions/(\d+)[^"\']*)["\'][^>]*>([^<]{10,200})</a>',
        re.IGNORECASE,
    )
    seen = set()
    for match in pattern.finditer(html):
        path, q_id, title = match.group(1), match.group(2), match.group(3).strip()
        if title in seen or not title:
            continue
        seen.add(title)
        q_url = f"{CONTEXT_OVERFLOW_BASE}{path}"
        seed_type = classify_seed_type(title)
        seeds.append(
            {
                "source": "context_overflow",
                "id": q_id,
                "title": title,
                "url": q_url,
                "author": "",
                "points": 0,
                "comments": 0,
                "answer_count": None,
                "is_unanswered": None,
                "seed_type": seed_type,
                "content_format": CONTENT_TYPE_MAP.get(seed_type, "seo_page"),
                "content_angle": generate_content_angle(seed_type, title),
                "score": score_item(title, 0, 0),
                "created_at": "",
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        logger.info("    [CO-HTML] seed: %s", title[:80])
    return seeds


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------


def deduplicate_seeds(seeds: list[dict]) -> list[dict]:
    seen_titles = set()
    unique = []
    for seed in seeds:
        key = seed["title"].lower().strip()[:100]
        if key not in seen_titles:
            seen_titles.add(key)
            unique.append(seed)
    return unique


def deduplicate_targets(targets: list[dict]) -> list[dict]:
    seen_users = set()
    unique = []
    for t in targets:
        key = t["username"].lower().strip()
        if key not in seen_users:
            seen_users.add(key)
            unique.append(t)
    return unique


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

SEEDS_FIELDNAMES = [
    "source", "id", "title", "url", "author", "points", "comments",
    "seed_type", "content_format", "content_angle", "score",
    "created_at", "scraped_at",
]

OUTREACH_FIELDNAMES = [
    "source", "username", "profile_url", "comment_url",
    "comment_snippet", "outreach_note", "scraped_at",
]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str], logger: logging.Logger) -> None:
    validated = safe_path(path)
    validated.parent.mkdir(parents=True, exist_ok=True)

    existing = []
    if validated.exists():
        try:
            with open(validated, newline="", encoding="utf-8") as fh:
                existing = list(csv.DictReader(fh))
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not read existing CSV %s: %s", validated, exc)

    # Merge: append new rows not already present by id+source
    existing_keys = {(r.get("source", ""), r.get("id", "") or r.get("username", "")) for r in existing}
    new_rows = [
        r for r in rows
        if (r.get("source", ""), r.get("id", "") or r.get("username", "")) not in existing_keys
    ]
    all_rows = existing + new_rows

    try:
        with open(validated, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(all_rows)
        logger.info("Wrote %d rows (+%d new) to %s", len(all_rows), len(new_rows), validated.name)
    except Exception as exc:
        logger.error("Failed writing CSV %s: %s", validated, exc)


def write_status(status: dict, logger: logging.Logger) -> None:
    validated = safe_path(STATUS_FILE)
    validated.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(validated, "w", encoding="utf-8") as fh:
            json.dump(status, fh, indent=2)
    except Exception as exc:
        logger.error("Failed writing status: %s", exc)


def read_status(logger: logging.Logger) -> dict:
    validated = safe_path(STATUS_FILE)
    if not validated.exists():
        return {}
    try:
        with open(validated, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        logger.warning("Could not read status file: %s", exc)
        return {}


# ---------------------------------------------------------------------------
# CLI actions
# ---------------------------------------------------------------------------


def run(dry_run: bool, logger: logging.Logger) -> None:
    label = "[DRY-RUN] " if dry_run else ""
    logger.info("%sStarting AI Agent Q&A Monitor run", label)

    recall_skills_for_task("scrape_ai_agent_qa")

    hn_seeds, hn_targets = scrape_hn_ai_threads(logger, dry_run=dry_run)
    co_seeds, co_targets = scrape_context_overflow(logger, dry_run=dry_run)

    all_seeds = deduplicate_seeds(hn_seeds + co_seeds)
    all_targets = deduplicate_targets(hn_targets + co_targets)

    # Sort seeds by score descending
    all_seeds.sort(key=lambda x: x.get("score", 0), reverse=True)

    logger.info(
        "%sTotal: %d unique content seeds, %d unique outreach targets",
        label, len(all_seeds), len(all_targets),
    )

    if not dry_run:
        write_csv(SEEDS_CSV, all_seeds, SEEDS_FIELDNAMES, logger)
        write_csv(OUTREACH_CSV, all_targets, OUTREACH_FIELDNAMES, logger)

        status = {
            "last_run": datetime.now(timezone.utc).isoformat(),
            "seeds_total": len(all_seeds),
            "outreach_total": len(all_targets),
            "seeds_by_format": {
                fmt: sum(1 for s in all_seeds if s["content_format"] == fmt)
                for fmt in ["twitter_thread", "reddit_post", "seo_page"]
            },
            "sources": {
                "hacker_news": sum(1 for s in all_seeds if "hacker_news" in s["source"]),
                "context_overflow": sum(1 for s in all_seeds if "context_overflow" in s["source"]),
            },
            "top_seeds": [
                {"title": s["title"][:80], "format": s["content_format"], "score": s["score"]}
                for s in all_seeds[:5]
            ],
        }
        write_status(status, logger)
        capture_skill_from_result(status, "scrape_ai_agent_qa")
    else:
        logger.info("[DRY-RUN] Would write %d seeds and %d targets to CSV", len(all_seeds), len(all_targets))

    logger.info("%sRun complete.", label)


def status_report(logger: logging.Logger) -> None:
    data = read_status(logger)
    if not data:
        print("No status file found. Run with --run first.")
        return

    print("\n=== AI Agent Q&A Monitor — Status ===")
    print(f"  Last run:        {data.get('last_run', 'unknown')}")
    print(f"  Seeds total:     {data.get('seeds_total', 0)}")
    print(f"  Outreach total:  {data.get('outreach_total', 0)}")
    print()
    by_fmt = data.get("seeds_by_format", {})
    print("  Seeds by format:")
    for fmt, count in by_fmt.items():
        print(f"    {fmt:<20} {count}")
    print()
    sources = data.get("sources", {})
    print("  Seeds by source:")
    for src, count in sources.items():
        print(f"    {src:<22} {count}")
    print()
    print("  Top seeds:")
    for i, seed in enumerate(data.get("top_seeds", []), 1):
        print(f"    {i}. [{seed['format']}] {seed['title'][:70]}  (score: {seed['score']})")
    print()
    seeds_path = safe_path(SEEDS_CSV)
    outreach_path = safe_path(OUTREACH_CSV)
    print(f"  Content seeds:    {seeds_path}")
    print(f"  Outreach targets: {outreach_path}")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: AI Agent Q&A Monitor — scrapes HN and Context Overflow for content seeds and B2B leads.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Cron example:\n  0 7 * * * python3 ai_agent_qa_monitor.py --run",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Execute the scraper and write outputs")
    group.add_argument("--status", action="store_true", help="Print last run status")
    group.add_argument("--dry-run", action="store_true", dest="dry_run", help="Simulate run without writing files")
    args = parser.parse_args()

    logger = setup_logging()

    try:
        if args.run:
            run(dry_run=False, logger=logger)
        elif args.dry_run:
            run(dry_run=True, logger=logger)
        elif args.status:
            status_report(logger)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(0)
    except Exception as exc:
        logger.exception("Fatal error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()