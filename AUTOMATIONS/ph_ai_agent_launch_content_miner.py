#!/usr/bin/env python3
"""
PRINTMAXX Automation: Product Hunt AI Agent Launch Content Miner

Scrapes Product Hunt comments on the Context Overflow launch to surface pain points
around AI agent memory and context limits, converts top hits into engagement bait posts
centered on the agent context management narrative, and monitors comments for affiliate
or partner program announcements.

METHOD CONTEXT: [PH LAUNCH] Context Overflow: Knowledge Sharing for AI Agents
TYPE: scraper
SCHEDULE: cron-safe, no interactive input required
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
# Bootstrap: import from _common or define fallbacks
# ---------------------------------------------------------------------------
try:
    from _common import (
        PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path) -> Path:
        """Validate that path resolves within PROJECT root."""
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(
                f"Path escape attempt: {resolved} is outside PROJECT root {PROJECT}"
            )
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result, task: str):
        return result


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_NAME = "ph_ai_agent_launch_content_miner"

LOG_FILE        = PROJECT / "AUTOMATIONS" / "logs" / f"{SCRIPT_NAME}.log"
DATA_DIR        = PROJECT / "AUTOMATIONS" / "data" / SCRIPT_NAME
STATUS_FILE     = DATA_DIR / "status.json"
COMMENTS_CSV    = DATA_DIR / "ph_comments.csv"
PAIN_POINTS_JSON = DATA_DIR / "pain_points.json"
BAIT_POSTS_JSON = DATA_DIR / "engagement_bait_posts.json"
AFFILIATE_JSON  = DATA_DIR / "affiliate_monitor.json"

PH_GRAPHQL_URL  = "https://www.producthunt.com/frontend/graphql"
PH_PRODUCT_SLUG = "context-overflow"

PAIN_KEYWORDS = [
    "memory", "context window", "context limit", "token limit", "forget",
    "remember", "long-term", "persistent", "knowledge base", "knowledge graph",
    "recall", "retention", "history", "session", "stateless", "state",
    "conversation history", "agent memory", "rag", "retrieval", "lost context",
    "context length", "overflow", "truncat", "hallucin",
]

AFFILIATE_KEYWORDS = [
    "affiliate", "referral", "commission", "partner program", "revenue share",
    "referral link", "promo code", "discount code", "earn money",
    "refer a friend", "lifetime deal", "ltd",
]

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

BAIT_TEMPLATES = [
    (
        'Hot take: "{excerpt}" — This is exactly why agent context management '
        "is the most underrated problem in AI right now. {tags}",
        "hot_take",
    ),
    (
        "Everyone's building AI agents. Almost nobody is solving memory.\n\n"
        'A real developer just said: "{excerpt}"\n\n'
        "The agents that win will be the ones that remember. Context Overflow is onto something. {tags}",
        "social_proof",
    ),
    (
        "The #1 complaint I keep seeing from AI agent users:\n\n"
        '"{excerpt}"\n\n'
        "Context limits aren't a technical footnote — they're the product ceiling. {tags}",
        "pain_amplifier",
    ),
    (
        "If your AI agent forgets everything after 8k tokens you don't have an agent.\n"
        "You have expensive autocomplete.\n\n"
        "Persistent context = competitive moat in 2025. {tags}",
        "provocative",
    ),
    (
        "Spotted on Product Hunt — developers screaming about agent memory limits:\n\n"
        '"{excerpt}"\n\n'
        "The narrative is clear: long-term context = the next big unlock in AI tooling. {tags}",
        "trend_signal",
    ),
]


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _setup_logging() -> logging.Logger:
    log_path = safe_path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    log = logging.getLogger(SCRIPT_NAME)
    log.setLevel(logging.DEBUG)

    fh = logging.FileHandler(str(log_path), mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    ))

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    log.addHandler(fh)
    log.addHandler(ch)
    return log


logger = _setup_logging()


# ---------------------------------------------------------------------------
# Product Hunt GraphQL helpers
# ---------------------------------------------------------------------------

def _ph_request(query: str, variables: dict) -> dict:
    """POST a GraphQL query to Product Hunt and return the parsed JSON."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        PH_GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": _UA,
            "Accept": "application/json",
            "Origin": "https://www.producthunt.com",
            "Referer": f"https://www.producthunt.com/posts/{PH_PRODUCT_SLUG}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_post_metadata(slug: str) -> dict | None:
    """Return basic metadata for a PH post by slug, or None on failure."""
    query = """
    query PostMeta($slug: String!) {
      post(slug: $slug) {
        id name tagline votesCount commentsCount
        website
      }
    }
    """
    try:
        data = _ph_request(query, {"slug": slug})
        post = data.get("data", {}).get("post")
        if post:
            logger.info(
                "Post resolved: '%s' | %s votes | %s comments",
                post["name"], post["votesCount"], post["commentsCount"],
            )
        else:
            logger.warning("No post found for slug '%s'", slug)
        return post
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
        logger.error("fetch_post_metadata: %s", exc)
        return None


def _fetch_comment_page(post_id: str, cursor: str | None) -> tuple[list[dict], str | None]:
    """Fetch one page of comments. Returns (comments, next_cursor_or_None)."""
    query = """
    query PostComments($postId: ID!, $cursor: String) {
      post(id: $postId) {
        comments(first: 50, after: $cursor) {
          pageInfo { hasNextPage endCursor }
          edges {
            node {
              id body createdAt votesCount
              user { name username }
            }
          }
        }
      }
    }
    """
    try:
        variables: dict = {"postId": post_id}
        if cursor:
            variables["cursor"] = cursor
        data = _ph_request(query, variables)
        block = data.get("data", {}).get("post", {}).get("comments", {})
        edges = block.get("edges", [])
        page_info = block.get("pageInfo", {})
        comments = [e["node"] for e in edges if "node" in e]
        next_cursor = page_info.get("endCursor") if page_info.get("hasNextPage") else None
        return comments, next_cursor
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
        logger.error("_fetch_comment_page: %s", exc)
        return [], None


def collect_all_comments(post_id: str) -> list[dict]:
    """Paginate through every comment for a post and return them all."""
    all_comments: list[dict] = []
    cursor = None
    page = 0
    while True:
        page += 1
        logger.debug("Fetching page %d (cursor=%s)", page, cursor)
        comments, cursor = _fetch_comment_page(post_id, cursor)
        all_comments.extend(comments)
        logger.info("Page %d: +%d comments (running total: %d)", page, len(comments), len(all_comments))
        if not cursor:
            break
        time.sleep(1.5)  # polite crawl delay
    return all_comments


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def _score(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    lower = text.lower()
    matched = [kw for kw in keywords if kw in lower]
    return len(matched), matched


def analyze_comments(comments: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Classify comments into pain-point hits and affiliate/partner signal hits.
    Returns (pain_points, affiliate_hits) sorted by relevance descending.
    """
    pain_points: list[dict] = []
    affiliate_hits: list[dict] = []

    for c in comments:
        body = c.get("body", "")
        p_score, p_kws = _score(body, PAIN_KEYWORDS)
        a_score, a_kws = _score(body, AFFILIATE_KEYWORDS)

        base = {
            "id": c.get("id", ""),
            "author": c.get("user", {}).get("username", "unknown"),
            "body": body,
            "votes": c.get("votesCount", 0),
            "created_at": c.get("createdAt", ""),
        }

        if p_score:
            pain_points.append({**base, "pain_score": p_score, "pain_keywords": p_kws})

        if a_score:
            affiliate_hits.append({**base, "affiliate_score": a_score, "affiliate_keywords": a_kws})

    pain_points.sort(key=lambda x: (x["pain_score"], x["votes"]), reverse=True)
    affiliate_hits.sort(key=lambda x: x["affiliate_score"], reverse=True)

    logger.info(
        "Analysis: %d pain-point comments, %d affiliate signals",
        len(pain_points), len(affiliate_hits),
    )
    return pain_points, affiliate_hits


# ---------------------------------------------------------------------------
# Engagement bait post generation
# ---------------------------------------------------------------------------

def generate_bait_posts(pain_points: list[dict]) -> list[dict]:
    """Convert top pain-point comments into ready-to-post engagement bait."""
    posts: list[dict] = []
    top = pain_points[: min(20, len(pain_points))]

    for i, pp in enumerate(top):
        body = pp["body"]
        # pull first sentence or first 120 chars as excerpt
        excerpt = body.split(".")[0].strip()
        if len(excerpt) > 120:
            excerpt = excerpt[:117].rstrip() + "..."
        if not excerpt:
            excerpt = body[:120].strip()

        tags = " ".join(
            "#" + kw.replace(" ", "").replace("-", "")
            for kw in pp["pain_keywords"][:3]
        )

        tmpl_text, tmpl_type = BAIT_TEMPLATES[i % len(BAIT_TEMPLATES)]
        generated = tmpl_text.format(excerpt=excerpt, tags=tags)

        posts.append({
            "post_id": i + 1,
            "template_type": tmpl_type,
            "source_comment_id": pp["id"],
            "source_author": pp["author"],
            "source_pain_score": pp["pain_score"],
            "generated_post": generated,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "platform_targets": ["Twitter/X", "LinkedIn", "Indie Hackers"],
        })

    logger.info("Generated %d engagement bait posts", len(posts))
    return posts


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def _ensure_dirs() -> None:
    for d in (DATA_DIR, LOG_FILE.parent):
        safe_path(d).mkdir(parents=True, exist_ok=True)


def _save_comments_csv(comments: list[dict]) -> None:
    path = safe_path(COMMENTS_CSV)
    fieldnames = ["id", "author", "username", "body", "votes", "created_at"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for c in comments:
            writer.writerow({
                "id": c.get("id", ""),
                "author": c.get("user", {}).get("name", ""),
                "username": c.get("user", {}).get("username", ""),
                "body": c.get("body", "").replace("\n", " "),
                "votes": c.get("votesCount", 0),
                "created_at": c.get("createdAt", ""),
            })
    logger.info("Saved %d comments → %s", len(comments), path)


def _save_json(data, dest: Path, label: str) -> None:
    path = safe_path(dest)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    logger.info("Saved %s (%d items) → %s", label, len(data), path)


def _save_status(status: dict) -> None:
    path = safe_path(STATUS_FILE)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(status, fh, indent=2)


def _load_status() -> dict:
    path = safe_path(STATUS_FILE)
    if path.exists():
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "last_run": None,
        "status": "never_run",
        "comments_found": 0,
        "pain_points_found": 0,
        "bait_posts_generated": 0,
        "affiliate_hits": 0,
    }


# ---------------------------------------------------------------------------
# Notification helper (uses subprocess per allowed deps)
# ---------------------------------------------------------------------------

def _notify(title: str, message: str) -> None:
    """Send a macOS notification if osascript is available; silently skip otherwise."""
    try:
        script = (
            f'display notification "{message}" with title "{title}"'
        )
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass  # non-macOS or osascript unavailable — not fatal


# ---------------------------------------------------------------------------
# CLI actions
# ---------------------------------------------------------------------------

def run(dry_run: bool = False) -> dict:
    """Full scrape → analyse → generate pipeline."""
    logger.info("=== %s START (dry_run=%s) ===", SCRIPT_NAME.upper(), dry_run)
    recall_skills_for_task("scrape_ph_comments_pain_points")
    _ensure_dirs()

    # 1. Resolve post
    post = fetch_post_metadata(PH_PRODUCT_SLUG)
    if not post:
        logger.error("Cannot resolve PH post for slug '%s'. Aborting.", PH_PRODUCT_SLUG)
        status = {
            "last_run": datetime.now(timezone.utc).isoformat(),
            "status": "error",
            "error": "post_not_found",
        }
        if not dry_run:
            _save_status(status)
        sys.exit(1)

    post_id = str(post["id"])

    # 2. Collect comments
    comments = collect_all_comments(post_id)
    logger.info("Total comments collected: %d", len(comments))
    if not dry_run:
        _save_comments_csv(comments)

    # 3. Analyse
    pain_points, affiliate_hits = analyze_comments(comments)
    if not dry_run:
        _save_json(pain_points, PAIN_POINTS_JSON, "pain_points")
        _save_json(affiliate_hits, AFFILIATE_JSON, "affiliate_hits")

    # 4. Generate bait posts
    bait_posts = generate_bait_posts(pain_points)
    if not dry_run:
        _save_json(bait_posts, BAIT_POSTS_JSON, "bait_posts")

    # 5. Affiliate alert
    if affiliate_hits:
        msg = f"{len(affiliate_hits)} affiliate/partner signal(s) detected on Context Overflow PH launch!"
        logger.warning("AFFILIATE ALERT: %s", msg)
        for hit in affiliate_hits[:5]:
            logger.warning("  @%s (score=%d): %.100s", hit["author"], hit["affiliate_score"], hit["body"])
        _notify("PRINTMAXX Affiliate Alert", msg)
    else:
        logger.info("No affiliate program signals detected this run.")

    result = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "dry_run": dry_run,
        "comments_found": len(comments),
        "pain_points_found": len(pain_points),
        "bait_posts_generated": len(bait_posts),
        "affiliate_hits": len(affiliate_hits),
    }
    capture_skill_from_result(result, "scrape_ph_comments_pain_points")

    if not dry_run:
        _save_status(result)

    logger.info("=== RUN COMPLETE %s ===", json.dumps(result))
    return result


def show_status() -> None:
    """Print last run status to stdout."""
    _ensure_dirs()
    status = _load_status()
    print(json.dumps(status, indent=2))
    logger.info("Status check: %s", json.dumps(status))


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "PRINTMAXX: Scrape PH comments on Context Overflow launch, "
            "extract AI agent memory/context pain points, generate engagement bait posts, "
            "and monitor for affiliate program announcements."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full scrape-analyse-generate pipeline.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print the status of the last run and exit.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the pipeline without writing any output files.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = _parse_args()
    try:
        if args.status:
            show_status()
        elif args.dry_run:
            run(dry_run=True)
        else:
            run(dry_run=False)
    except KeyboardInterrupt:
        logger.info("Interrupted.")
        sys.exit(0)
    except Exception as exc:
        logger.exception("Fatal error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()