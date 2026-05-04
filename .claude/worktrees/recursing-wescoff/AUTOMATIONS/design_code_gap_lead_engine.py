#!/usr/bin/env python3
"""
PRINTMAXX Automation: Design-Code Gap Lead Engine

PURPOSE: Monitor Product Hunt launches in the design-to-code space, scrape
product details and upvote counts, identify agencies and developers who upvoted
or commented (social proof of pain), and generate cold outreach lists offering a
design-code audit service. Fulfillment layer: Visdiff or custom Playwright
screenshot diffing.

METHOD CONTEXT: [PH LAUNCH] Visdiff: Stop bridging the design-to-code gap, close it

USAGE:
    python design_code_gap_lead_engine.py --run       # Full pipeline run
    python design_code_gap_lead_engine.py --status    # Show last run stats
    python design_code_gap_lead_engine.py --dry-run   # Simulate without writes

CRON EXAMPLE:
    0 8 * * * /usr/bin/python3 /path/to/design_code_gap_lead_engine.py --run
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# _common import with local fallbacks
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

    def safe_path(p: Any) -> Path:
        """Ensure *p* resolves inside PROJECT to prevent path traversal."""
        resolved = Path(p).resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError:
            raise ValueError(
                f"Path {resolved} is outside PROJECT root {PROJECT}"
            )
        return resolved

    def recall_skills_for_task(task: str) -> list:  # noqa: ARG001
        return []

    def capture_skill_from_result(result: Any) -> None:  # noqa: ARG001
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS_DIR / "logs" / "design_code_gap_lead_engine.log"
OUTPUT_DIR = AUTOMATIONS_DIR / "outputs" / "design_code_gap"
LEADS_CSV = OUTPUT_DIR / "leads.csv"
PRODUCTS_JSON = OUTPUT_DIR / "ph_products.json"
STATUS_JSON = OUTPUT_DIR / "status.json"

PH_GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"
PH_API_TOKEN_ENV = "PH_API_TOKEN"

DESIGN_CODE_KEYWORDS = [
    "design to code",
    "design-to-code",
    "figma to code",
    "figma2code",
    "design system",
    "component library",
    "visual diff",
    "screenshot diff",
    "pixel perfect",
    "design qa",
    "design handoff",
    "visdiff",
    "chromatic",
    "percy",
    "applitools",
    "storybook",
    "ui design",
    "design gap",
    "design review",
]

TARGET_TOPICS = [
    "design-tools",
    "developer-tools",
    "design",
    "tech",
    "productivity",
]

AGENCY_SIGNALS = [
    "agency",
    "studio",
    "design studio",
    "dev shop",
    "freelance",
    "consultant",
    "ui/ux",
    "ux designer",
    "product designer",
    "frontend developer",
    "full-stack",
    "fullstack",
    "react developer",
    "web developer",
    "software engineer",
    "front-end",
]

OUTREACH_TEMPLATE = (
    "Hi {name},\n\n"
    "I saw you {action} {product} on Product Hunt — "
    "clearly the design-to-code gap is something you're actively trying to solve.\n\n"
    "We run a fast design-code audit (48 h turnaround) that catches "
    "pixel-drift, broken breakpoints, and component divergence before they reach "
    "production. We use Visdiff + Playwright screenshot diffing so the report is "
    "visual and immediately actionable for your team.\n\n"
    "Would a 15-minute call this week make sense?\n\n"
    "Best,\nPRINTMAXX Team"
)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(log_file: Path) -> logging.Logger:
    """Configure file + stdout logging, appending to log_file."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("design_code_gap_lead_engine")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(
            str(safe_path(log_file)), mode="a", encoding="utf-8"
        )
        fh.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%dT%H:%M:%S"
            )
        )
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)
    return logger


# ---------------------------------------------------------------------------
# HTTP helpers (urllib only)
# ---------------------------------------------------------------------------

def _get_ph_token() -> str:
    """Read PH API token from environment or subprocess (pass/secret store)."""
    token = os.environ.get(PH_API_TOKEN_ENV, "").strip()
    if not token:
        try:
            result = subprocess.run(
                ["pass", f"api/producthunt/{PH_API_TOKEN_ENV}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                token = result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass
    return token


def _graphql_request(
    query: str,
    variables: dict,
    token: str,
    logger: logging.Logger,
) -> dict:
    """Execute a GraphQL POST against the PH API using urllib."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "PRINTMAXX-LeadBot/1.0",
    }
    req = urllib.request.Request(
        PH_GRAPHQL_URL, data=payload, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        logger.error("PH API HTTP %s: %s", exc.code, exc.reason)
        raise
    except urllib.error.URLError as exc:
        logger.error("PH API URLError: %s", exc.reason)
        raise


# ---------------------------------------------------------------------------
# Product Hunt GraphQL queries
# ---------------------------------------------------------------------------

_PH_POSTS_QUERY = """
query FetchPosts($topic: String, $after: String) {
  posts(topic: $topic, after: $after, order: VOTES) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        name
        tagline
        description
        votesCount
        commentsCount
        createdAt
        url
        website
        makers { id name username headline twitterUsername }
        topics { edges { node { name } } }
      }
    }
  }
}
"""

_PH_COMMENTS_QUERY = """
query FetchComments($postId: ID!, $after: String) {
  post(id: $postId) {
    comments(after: $after, first: 50) {
      pageInfo { hasNextPage endCursor }
      edges {
        node {
          id
          body
          createdAt
          user { id name username headline twitterUsername }
        }
      }
    }
  }
}
"""

_PH_VOTERS_QUERY = """
query FetchVoters($postId: ID!, $after: String) {
  post(id: $postId) {
    votes(after: $after, first: 50) {
      pageInfo { hasNextPage endCursor }
      edges {
        node {
          user { id name username headline twitterUsername }
        }
      }
    }
  }
}
"""


# ---------------------------------------------------------------------------
# PH data fetching
# ---------------------------------------------------------------------------

def _is_design_code_relevant(post: dict) -> bool:
    """Return True if any design-to-code keyword appears in the post text."""
    blob = " ".join([
        post.get("name", ""),
        post.get("tagline", ""),
        post.get("description", "") or "",
    ]).lower()
    return any(kw in blob for kw in DESIGN_CODE_KEYWORDS)


def fetch_ph_posts(
    token: str,
    logger: logging.Logger,
    max_per_topic: int = 100,
) -> list:
    """Fetch PH posts across design/dev topics, returning only relevant ones."""
    all_posts: list = []
    seen_ids: set = set()

    for topic in TARGET_TOPICS:
        cursor: Optional[str] = None
        fetched = 0
        logger.info("Fetching PH posts for topic: %s", topic)

        while fetched < max_per_topic:
            variables: dict = {"topic": topic}
            if cursor:
                variables["after"] = cursor

            try:
                data = _graphql_request(_PH_POSTS_QUERY, variables, token, logger)
            except Exception as exc:
                logger.warning("Skipping topic %s after error: %s", topic, exc)
                break

            posts_data = data.get("data", {}).get("posts", {})
            edges = posts_data.get("edges", [])
            page_info = posts_data.get("pageInfo", {})

            for edge in edges:
                node = edge.get("node", {})
                node_id = node.get("id")
                if node_id and node_id not in seen_ids and _is_design_code_relevant(node):
                    seen_ids.add(node_id)
                    all_posts.append(node)
                fetched += 1

            if not page_info.get("hasNextPage") or fetched >= max_per_topic:
                break
            cursor = page_info.get("endCursor")

    logger.info("Found %d relevant PH posts across all topics", len(all_posts))
    return all_posts


def fetch_commenters(
    post_id: str,
    token: str,
    logger: logging.Logger,
) -> list:
    """Return list of commenter user dicts for a PH post."""
    users: list = []
    cursor: Optional[str] = None

    while True:
        variables: dict = {"postId": post_id}
        if cursor:
            variables["after"] = cursor

        try:
            data = _graphql_request(_PH_COMMENTS_QUERY, variables, token, logger)
        except Exception as exc:
            logger.warning("Comments fetch error for post %s: %s", post_id, exc)
            break

        comments_data = (
            data.get("data", {}).get("post", {}).get("comments", {})
        )
        edges = comments_data.get("edges", [])
        page_info = comments_data.get("pageInfo", {})

        for edge in edges:
            user = edge.get("node", {}).get("user")
            if user:
                users.append({**user, "action": "commented on"})

        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")

    return users


def fetch_voters(
    post_id: str,
    token: str,
    logger: logging.Logger,
) -> list:
    """Return list of upvoter user dicts for a PH post."""
    users: list = []
    cursor: Optional[str] = None

    while True:
        variables: dict = {"postId": post_id}
        if cursor:
            variables["after"] = cursor

        try:
            data = _graphql_request(_PH_VOTERS_QUERY, variables, token, logger)
        except Exception as exc:
            logger.warning("Voters fetch error for post %s: %s", post_id, exc)
            break

        votes_data = (
            data.get("data", {}).get("post", {}).get("votes", {})
        )
        edges = votes_data.get("edges", [])
        page_info = votes_data.get("pageInfo", {})

        for edge in edges:
            user = edge.get("node", {}).get("user")
            if user:
                users.append({**user, "action": "upvoted"})

        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")

    return users


# ---------------------------------------------------------------------------
# Lead scoring and assembly
# ---------------------------------------------------------------------------

def _score_lead(user: dict) -> int:
    """Heuristic priority score 0–10 based on headline and profile signals."""
    score = 0
    headline = (user.get("headline") or "").lower()
    for signal in AGENCY_SIGNALS:
        if signal in headline:
            score += 3
            break
    if user.get("twitterUsername"):
        score += 2
    if user.get("username"):
        score += 1
    if user.get("action") == "commented on":
        score += 2  # higher intent than a passive upvote
    return min(score, 10)


def build_leads(
    posts: list,
    token: str,
    logger: logging.Logger,
    dry_run: bool = False,
) -> list:
    """Aggregate scored leads from upvoters and commenters across all posts."""
    leads: list = []
    seen_users: set = set()
    scraped_at = datetime.now(timezone.utc).isoformat()

    for post in posts:
        post_id = post.get("id", "")
        post_name = post.get("name", "Unknown")
        votes_count = post.get("votesCount", 0)

        logger.info(
            "Processing post '%s' (id=%s, votes=%d)", post_name, post_id, votes_count
        )

        if dry_run:
            logger.info("[dry-run] Skipping voter/commenter API calls for '%s'", post_name)
            continue

        # Commenters first (higher engagement signal), then voters
        all_users: list = []
        try:
            all_users += fetch_commenters(post_id, token, logger)
        except Exception as exc:
            logger.warning("Could not fetch commenters for %s: %s", post_id, exc)

        try:
            all_users += fetch_voters(post_id, token, logger)
        except Exception as exc:
            logger.warning("Could not fetch voters for %s: %s", post_id, exc)

        for user in all_users:
            uid = user.get("id") or user.get("username")
            if not uid or uid in seen_users:
                continue
            seen_users.add(uid)

            display_name = user.get("name") or user.get("username") or "there"
            action = user.get("action", "engaged with")
            message = OUTREACH_TEMPLATE.format(
                name=display_name,
                action=action,
                product=post_name,
            )

            leads.append({
                "ph_user_id": user.get("id", ""),
                "name": user.get("name", ""),
                "username": user.get("username", ""),
                "twitter": user.get("twitterUsername") or "",
                "headline": user.get("headline") or "",
                "action": action,
                "source_product": post_name,
                "source_product_id": post_id,
                "source_votes": votes_count,
                "lead_score": _score_lead(user),
                "outreach_message": message,
                "ph_profile_url": f"https://www.producthunt.com/@{user.get('username', '')}",
                "scraped_at": scraped_at,
            })

    leads.sort(key=lambda x: x["lead_score"], reverse=True)
    logger.info("Assembled %d unique leads", len(leads))
    return leads


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def ensure_dirs() -> None:
    """Create required output and log directories within PROJECT."""
    safe_path(LOG_FILE.parent).mkdir(parents=True, exist_ok=True)
    safe_path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def write_products_json(posts: list, logger: logging.Logger) -> None:
    dest = safe_path(PRODUCTS_JSON)
    try:
        with open(str(dest), "w", encoding="utf-8") as fh:
            json.dump(posts, fh, indent=2, default=str)
        logger.info("Wrote %d products → %s", len(posts), dest)
    except OSError as exc:
        logger.error("Failed to write products JSON: %s", exc)
        raise


def write_leads_csv(leads: list, logger: logging.Logger) -> None:
    if not leads:
        logger.warning("No leads to write — CSV skipped.")
        return
    dest = safe_path(LEADS_CSV)
    fieldnames = list(leads[0].keys())
    try:
        with open(str(dest), "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads)
        logger.info("Wrote %d leads → %s", len(leads), dest)
    except OSError as exc:
        logger.error("Failed to write leads CSV: %s", exc)
        raise


def write_status(stats: dict, logger: logging.Logger) -> None:
    dest = safe_path(STATUS_JSON)
    try:
        with open(str(dest), "w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=2, default=str)
        logger.info("Status written → %s", dest)
    except OSError as exc:
        logger.error("Failed to write status JSON: %s", exc)
        raise


def read_status(logger: logging.Logger) -> dict:
    try:
        dest = safe_path(STATUS_JSON)
        with open(str(dest), "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        logger.info("No status file found — pipeline has not run yet.")
        return {}
    except json.JSONDecodeError as exc:
        logger.error("Corrupt status file: %s", exc)
        return {}
    except OSError as exc:
        logger.error("Could not read status file: %s", exc)
        return {}


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------

def run_pipeline(logger: logging.Logger, dry_run: bool = False) -> dict:
    """Main pipeline: fetch PH posts → extract leads → write outputs."""
    logger.info(
        "=== design_code_gap_lead_engine STARTING (dry_run=%s) ===", dry_run
    )

    skills = recall_skills_for_task(
        "monitor PH launches design-to-code cold outreach visdiff"
    )
    if skills:
        logger.info("Recalled %d skill(s) for task", len(skills))

    token = _get_ph_token()
    if not token:
        logger.warning(
            "No PH API token found. Set env var %s or configure 'pass'. "
            "Running in demo mode (no live API calls).",
            PH_API_TOKEN_ENV,
        )

    posts: list = []
    if token and not dry_run:
        try:
            posts = fetch_ph_posts(token, logger)
        except Exception as exc:
            logger.error("fetch_ph_posts failed: %s", exc)
    else:
        logger.info("[dry-run/no-token] Skipping PH post fetch")

    leads: list = []
    if posts:
        try:
            leads = build_leads(posts, token, logger, dry_run=dry_run)
        except Exception as exc:
            logger.error("build_leads failed: %s", exc)

    if not dry_run:
        try:
            write_products_json(posts, logger)
            write_leads_csv(leads, logger)
        except Exception as exc:
            logger.error("Output write failed: %s", exc)

    top_score = leads[0]["lead_score"] if leads else 0
    stats = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "posts_found": len(posts),
        "leads_found": len(leads),
        "top_lead_score": top_score,
        "outputs": {
            "products": str(PRODUCTS_JSON),
            "leads": str(LEADS_CSV),
        },
    }

    if not dry_run:
        try:
            write_status(stats, logger)
        except Exception as exc:
            logger.error("Status write failed: %s", exc)

    result = {"status": "ok", "stats": stats}
    capture_skill_from_result(result)

    logger.info(
        "=== DONE | posts=%d leads=%d top_score=%d ===",
        stats["posts_found"],
        stats["leads_found"],
        stats["top_lead_score"],
    )
    return stats


def show_status(logger: logging.Logger) -> None:
    """Print the last run stats from status.json to stdout."""
    status = read_status(logger)
    if not status:
        print("No previous run found.")
        return
    print(json.dumps(status, indent=2, default=str))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="design_code_gap_lead_engine",
        description=(
            "PRINTMAXX: Monitor Product Hunt design-to-code launches "
            "and generate cold outreach leads."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full pipeline",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print statistics from the last run",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate a run without writing any output files",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> int:
    args = parse_args(argv)

    try:
        ensure_dirs()
    except (ValueError, OSError) as exc:
        print(f"[ERROR] Could not create directories: {exc}", file=sys.stderr)
        return 1

    try:
        logger = setup_logging(LOG_FILE)
    except Exception as exc:
        print(f"[ERROR] Logging setup failed: {exc}", file=sys.stderr)
        return 1

    try:
        if args.run:
            run_pipeline(logger, dry_run=False)
        elif args.dry_run:
            run_pipeline(logger, dry_run=True)
        elif args.status:
            show_status(logger)
    except KeyboardInterrupt:
        logger.warning("Interrupted.")
        return 130
    except Exception as exc:
        logger.exception("Unhandled exception: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())