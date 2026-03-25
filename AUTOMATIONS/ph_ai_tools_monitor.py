#!/usr/bin/env python3
"""
PRINTMAXX Automation: Product Hunt AI Tools Monitor

Daily scraper targeting AI productivity/tools launches on Product Hunt.
Extracts title, upvote count, maker info, and tags for each post.
Routes high-upvote AI tool launches to the founder outreach queue and
the engagement_bait_converter for positioning content.

Market signal context: AI Skills Manager validates MCP Marketplace pain point —
users want one place for all their AI tools/skills. Use as market signal,
not direct revenue driver.

Usage:
    python ph_ai_tools_monitor.py --run
    python ph_ai_tools_monitor.py --run --dry-run
    python ph_ai_tools_monitor.py --status
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Project root ──────────────────────────────────────────────────────────────
PROJECT = Path(__file__).resolve().parent.parent

# ── Try importing from _common; fall back to local definitions ────────────────
try:
    from _common import (
        PROJECT as _PROJECT,
        capture_skill_from_result,
        recall_skills_for_task,
        safe_path,
    )
    PROJECT = _PROJECT
except ImportError:
    def safe_path(p: Path) -> Path:
        """Validate that path is within PROJECT to prevent path traversal."""
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(
                f"Path {resolved!r} is outside PROJECT root {PROJECT!r}"
            )
        return resolved

    def recall_skills_for_task(task: str) -> List[str]:
        return []

    def capture_skill_from_result(result: Dict, task: str) -> None:
        pass

# ── Constants ─────────────────────────────────────────────────────────────────
AUTOMATIONS_DIR     = PROJECT / "AUTOMATIONS"
LOG_FILE            = AUTOMATIONS_DIR / "logs" / "ph_ai_tools_monitor.log"
DATA_DIR            = AUTOMATIONS_DIR / "data" / "ph_ai_tools"
OUTREACH_QUEUE      = AUTOMATIONS_DIR / "queues" / "founder_outreach.jsonl"
ENGAGEMENT_QUEUE    = AUTOMATIONS_DIR / "queues" / "engagement_bait_converter.jsonl"
STATE_FILE          = AUTOMATIONS_DIR / "state" / "ph_ai_tools_monitor.json"

HIGH_UPVOTE_THRESHOLD = 50
PH_GRAPHQL_URL = "https://www.producthunt.com/frontend/graphql"

AI_TAGS = {
    "ai", "artificial intelligence", "machine learning", "productivity",
    "developer tools", "chatgpt", "llm", "automation", "no-code", "workflow",
    "mcp", "agents", "claude", "openai", "copilot", "skills", "tools",
    "generative ai", "large language models",
}

AI_KEYWORDS = {
    "ai", "llm", "gpt", "claude", "gemini", "copilot", "agent",
    "automation", "workflow", "mcp", "skill", "productivity", "openai",
}

PH_GRAPHQL_QUERY = """
query GetFeaturedPosts($after: String) {
  posts(order: VOTES, featured: true, first: 50, after: $after) {
    edges {
      node {
        id
        name
        tagline
        votesCount
        url
        slug
        createdAt
        topics {
          edges {
            node {
              name
              slug
            }
          }
        }
        makers {
          id
          name
          username
          twitterUsername
          websiteUrl
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

# ── Logging setup ─────────────────────────────────────────────────────────────

def setup_logging() -> logging.Logger:
    """Configure appending file handler and stdout handler."""
    log_path = safe_path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("ph_ai_tools_monitor")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger


# ── HTTP / GraphQL helpers ────────────────────────────────────────────────────

def ph_graphql_request(
    query: str,
    variables: Optional[Dict] = None,
    timeout: int = 30,
) -> Dict:
    """POST a GraphQL query to Product Hunt and return the parsed JSON body."""
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        PH_GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; PRINTMAXX-PHMonitor/1.0)",
            "Referer": "https://www.producthunt.com/",
            "Origin": "https://www.producthunt.com",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all_posts(logger: logging.Logger) -> List[Dict]:
    """Paginate through PH GraphQL to collect all featured posts."""
    posts: List[Dict] = []
    cursor: Optional[str] = None
    page = 0

    while True:
        page += 1
        logger.debug("Fetching PH page %d (cursor=%s)", page, cursor)
        variables = {"after": cursor} if cursor else {}

        try:
            data = ph_graphql_request(PH_GRAPHQL_QUERY, variables)
        except urllib.error.HTTPError as exc:
            logger.error("HTTP %s fetching PH posts: %s", exc.code, exc.reason)
            break
        except urllib.error.URLError as exc:
            logger.error("URL error fetching PH posts: %s", exc.reason)
            break
        except json.JSONDecodeError as exc:
            logger.error("JSON decode error on PH response: %s", exc)
            break

        if "errors" in data:
            logger.error("GraphQL errors: %s", data["errors"])
            break

        post_data = data.get("data", {}).get("posts", {})
        edges = post_data.get("edges", [])
        page_info = post_data.get("pageInfo", {})

        if not edges:
            logger.debug("No edges on page %d; stopping pagination.", page)
            break

        for edge in edges:
            node = edge.get("node") or {}
            topics = [
                t["node"]["name"]
                for t in node.get("topics", {}).get("edges", [])
                if t.get("node")
            ]
            makers = [
                {
                    "id": m.get("id"),
                    "name": m.get("name", ""),
                    "username": m.get("username", ""),
                    "twitter": m.get("twitterUsername") or "",
                    "website": m.get("websiteUrl") or "",
                }
                for m in (node.get("makers") or [])
            ]
            posts.append(
                {
                    "id": node.get("id"),
                    "name": node.get("name", ""),
                    "tagline": node.get("tagline", ""),
                    "votes": node.get("votesCount", 0),
                    "url": node.get("url", ""),
                    "slug": node.get("slug", ""),
                    "created_at": node.get("createdAt", ""),
                    "tags": topics,
                    "makers": makers,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                }
            )

        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")

    logger.info("Fetched %d posts total across %d page(s).", len(posts), page)
    return posts


# ── Filtering ─────────────────────────────────────────────────────────────────

def is_ai_tool(post: Dict) -> bool:
    """Return True if the post is AI/productivity-related."""
    tag_names = {t.lower() for t in post.get("tags", [])}
    if tag_names & AI_TAGS:
        return True
    text = (
        (post.get("name") or "") + " " + (post.get("tagline") or "")
    ).lower()
    return bool(AI_KEYWORDS & set(text.split()))


def filter_ai_posts(posts: List[Dict], logger: logging.Logger) -> List[Dict]:
    """Filter posts to AI/productivity-related launches only."""
    ai_posts = [p for p in posts if is_ai_tool(p)]
    logger.info(
        "AI filter: %d / %d posts match AI/productivity criteria.",
        len(ai_posts),
        len(posts),
    )
    return ai_posts


# ── Directory setup ───────────────────────────────────────────────────────────

def ensure_dirs() -> None:
    """Create all required output directories."""
    for directory in (
        DATA_DIR,
        OUTREACH_QUEUE.parent,
        ENGAGEMENT_QUEUE.parent,
        STATE_FILE.parent,
        LOG_FILE.parent,
    ):
        safe_path(directory).mkdir(parents=True, exist_ok=True)


# ── File writers ──────────────────────────────────────────────────────────────

def write_csv(
    posts: List[Dict],
    logger: logging.Logger,
    dry_run: bool = False,
) -> Path:
    """Write AI posts to a dated CSV in the data directory."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    csv_path = safe_path(DATA_DIR / f"ph_ai_tools_{date_str}.csv")

    if dry_run:
        logger.info("[DRY-RUN] Would write %d rows to %s", len(posts), csv_path)
        return csv_path

    fieldnames = [
        "id", "name", "tagline", "votes", "url", "slug",
        "created_at", "tags", "maker_names", "maker_twitters",
        "maker_websites", "scraped_at",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for post in posts:
            row = dict(post)
            row["tags"] = "|".join(post.get("tags", []))
            row["maker_names"] = "|".join(
                m.get("name", "") for m in post.get("makers", [])
            )
            row["maker_twitters"] = "|".join(
                ("@" + m["twitter"]) if m.get("twitter") else ""
                for m in post.get("makers", [])
            )
            row["maker_websites"] = "|".join(
                m.get("website", "") for m in post.get("makers", [])
            )
            writer.writerow(row)

    logger.info("Wrote CSV  : %s  (%d rows)", csv_path, len(posts))
    return csv_path


def write_json(
    posts: List[Dict],
    logger: logging.Logger,
    dry_run: bool = False,
) -> Path:
    """Write AI posts to a dated JSON snapshot."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    json_path = safe_path(DATA_DIR / f"ph_ai_tools_{date_str}.json")

    if dry_run:
        logger.info("[DRY-RUN] Would write %d posts to %s", len(posts), json_path)
        return json_path

    payload = {
        "date": date_str,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "count": len(posts),
        "posts": posts,
    }
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)

    logger.info("Wrote JSON : %s  (%d posts)", json_path, len(posts))
    return json_path


def append_to_queue(
    queue_path: Path,
    entry: Dict,
    logger: logging.Logger,
    dry_run: bool = False,
) -> None:
    """Append a single JSONL record to a queue file."""
    safe_q = safe_path(queue_path)
    if dry_run:
        logger.info(
            "[DRY-RUN] Would append to %-40s : %s",
            safe_q.name,
            entry.get("product_name", "?"),
        )
        return
    safe_q.parent.mkdir(parents=True, exist_ok=True)
    with open(safe_q, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── Routing ───────────────────────────────────────────────────────────────────

def route_high_upvote_posts(
    posts: List[Dict],
    logger: logging.Logger,
    dry_run: bool = False,
) -> Tuple[int, int]:
    """
    Route posts above HIGH_UPVOTE_THRESHOLD to:
      1. founder_outreach queue
      2. engagement_bait_converter queue

    Returns (outreach_count, engagement_count).
    """
    outreach_n = 0
    engagement_n = 0

    for post in posts:
        if post.get("votes", 0) < HIGH_UPVOTE_THRESHOLD:
            continue

        logger.info(
            "Routing high-upvote post: '%s'  [%d votes]  %s",
            post["name"],
            post["votes"],
            post["url"],
        )

        queued_at = datetime.now(timezone.utc).isoformat()

        # ── Founder outreach queue ────────────────────────────────────────────
        outreach_entry = {
            "source": "product_hunt",
            "queued_at": queued_at,
            "product_name": post["name"],
            "tagline": post["tagline"],
            "votes": post["votes"],
            "url": post["url"],
            "slug": post["slug"],
            "tags": post["tags"],
            "makers": post["makers"],
            "signal": "high_upvote_ai_launch",
            "created_at": post["created_at"],
        }
        append_to_queue(OUTREACH_QUEUE, outreach_entry, logger, dry_run)
        outreach_n += 1

        # ── Engagement bait converter queue ───────────────────────────────────
        engagement_entry = {
            "source": "product_hunt",
            "queued_at": queued_at,
            "product_name": post["name"],
            "tagline": post["tagline"],
            "votes": post["votes"],
            "url": post["url"],
            "tags": post["tags"],
            "market_signal": (
                "AI Skills Manager validates MCP Marketplace pain point: "
                "users want one place for all AI tools/skills. "
                f"'{post['name']}' ({post['votes']} upvotes) — use as "
                "positioning content, not direct revenue."
            ),
            "positioning_hook": (
                f"[PH LAUNCH] {post['name']}: {post['tagline']} "
                f"— {post['votes']} upvotes signal real demand for "
                "unified AI tooling."
            ),
            "method_context": (
                "[PH LAUNCH] AI Skills Manager: One place for all your AI skills"
            ),
            "content_type": "engagement_bait",
        }
        append_to_queue(ENGAGEMENT_QUEUE, engagement_entry, logger, dry_run)
        engagement_n += 1

    return outreach_n, engagement_n


def maybe_trigger_downstream(
    script_name: str,
    logger: logging.Logger,
    dry_run: bool = False,
) -> None:
    """
    Optionally trigger a downstream PRINTMAXX automation via subprocess.
    Only fires when the script exists; failures are non-fatal.
    """
    script_path = safe_path(PROJECT / "AUTOMATIONS" / "scripts" / script_name)
    if not script_path.exists():
        logger.debug("Downstream script not found, skipping: %s", script_path)
        return

    if dry_run:
        logger.info("[DRY-RUN] Would trigger downstream: %s", script_path)
        return

    try:
        result = subprocess.run(
            [sys.executable, str(script_path), "--run"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            logger.info("Downstream '%s' exited cleanly.", script_name)
        else:
            logger.warning(
                "Downstream '%s' exited %d: %s",
                script_name,
                result.returncode,
                result.stderr.strip(),
            )
    except subprocess.TimeoutExpired:
        logger.warning("Downstream '%s' timed out.", script_name)
    except OSError as exc:
        logger.warning("Could not launch downstream '%s': %s", script_name, exc)


# ── State management ──────────────────────────────────────────────────────────

def load_state() -> Dict:
    """Load persisted run state; return empty dict on any error."""
    try:
        state_path = safe_path(STATE_FILE)
        if not state_path.exists():
            return {}
        with open(state_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def save_state(state: Dict, logger: logging.Logger) -> None:
    """Write run state to disk."""
    state_path = safe_path(STATE_FILE)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)
    logger.debug("State persisted to %s", state_path)


# ── Skill integration ─────────────────────────────────────────────────────────

def maybe_capture_skill(
    post: Dict,
    logger: logging.Logger,
    dry_run: bool = False,
) -> None:
    """Forward the top-ranked AI post to capture_skill_from_result if available."""
    if dry_run:
        return
    try:
        result = {
            "task": "ph_ai_tools_monitor",
            "product_name": post.get("name"),
            "tagline": post.get("tagline"),
            "votes": post.get("votes"),
            "tags": post.get("tags", []),
            "makers": post.get("makers", []),
            "market_signal": (
                "AI Skills Manager on PH — validates 'one place for all AI skills' "
                "pain point. High upvote count = confirmed user demand."
            ),
        }
        capture_skill_from_result(result, "ph_ai_tools_monitor")
    except Exception as exc:
        logger.debug("capture_skill_from_result skipped (%s).", exc)


# ── CLI commands ──────────────────────────────────────────────────────────────

def cmd_run(args: argparse.Namespace, logger: logging.Logger) -> int:
    """Scrape PH, filter AI posts, write outputs, route high-upvote posts."""
    label = "[DRY-RUN] " if args.dry_run else ""
    logger.info("=" * 60)
    logger.info("PH AI Tools Monitor — RUN  %s%s",
                label, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("=" * 60)

    # Surface any prior-session skill context
    try:
        skills = recall_skills_for_task("ph_ai_tools_monitor")
        if skills:
            logger.debug("Recalled skills: %s", skills)
    except Exception:
        pass

    # Create directories
    try:
        ensure_dirs()
    except (OSError, ValueError) as exc:
        logger.error("Directory setup failed: %s", exc)
        return 1

    # Scrape Product Hunt
    try:
        all_posts = fetch_all_posts(logger)
    except Exception as exc:
        logger.error("Unexpected error during scrape: %s", exc, exc_info=True)
        return 1

    if not all_posts:
        logger.warning("No posts returned — PH may be rate-limiting or unreachable.")
        return 0

    # Filter to AI posts and sort by votes
    ai_posts = filter_ai_posts(all_posts, logger)
    ai_posts.sort(key=lambda p: p.get("votes", 0), reverse=True)

    if not ai_posts:
        logger.info("No AI-tagged posts found today.")
    else:
        # Write structured outputs
        try:
            write_csv(ai_posts, logger, dry_run=args.dry_run)
            write_json(ai_posts, logger, dry_run=args.dry_run)
        except (OSError, ValueError) as exc:
            logger.error("Failed writing output files: %s", exc)
            return 1

        # Route high-upvote posts
        outreach_n, engagement_n = route_high_upvote_posts(
            ai_posts, logger, dry_run=args.dry_run
        )
        logger.info(
            "Routing complete — outreach: %d  |  engagement: %d",
            outreach_n,
            engagement_n,
        )

        # Skill capture for top post
        top = ai_posts[0]
        logger.info(
            "Top AI post : '%s'  (%d votes)\n  %s\n  %s",
            top["name"],
            top["votes"],
            top["tagline"],
            top["url"],
        )
        maybe_capture_skill(top, logger, dry_run=args.dry_run)

        # Optionally trigger downstream automation
        if outreach_n > 0:
            maybe_trigger_downstream(
                "founder_outreach_processor.py", logger, dry_run=args.dry_run
            )

    # Persist state
    state = load_state()
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    state["last_run_counts"] = {
        "total_posts_fetched": len(all_posts),
        "ai_posts_filtered": len(ai_posts),
        "outreach_queued": 0 if not ai_posts else outreach_n,
        "engagement_queued": 0 if not ai_posts else engagement_n,
    }
    if not args.dry_run:
        try:
            save_state(state, logger)
        except (OSError, ValueError) as exc:
            logger.warning("Could not save state: %s", exc)

    logger.info("Run complete.")
    return 0


def cmd_status(logger: logging.Logger) -> int:
    """Print last run state and current queue depths."""
    state = load_state()

    if not state:
        logger.info("No previous run state found at %s", STATE_FILE)
    else:
        last_run = state.get("last_run", "unknown")
        counts = state.get("last_run_counts", {})
        logger.info("Last run         : %s", last_run)
        logger.info("  Posts fetched  : %d", counts.get("total_posts_fetched", 0))
        logger.info("  AI posts found : %d", counts.get("ai_posts_filtered", 0))
        logger.info("  Outreach queue : +%d", counts.get("outreach_queued", 0))
        logger.info("  Engagement queue : +%d", counts.get("engagement_queued", 0))

    for label, qpath in (
        ("Outreach queue total", OUTREACH_QUEUE),
        ("Engagement queue total", ENGAGEMENT_QUEUE),
    ):
        try:
            safe_q = safe_path(qpath)
            if safe_q.exists():
                lines = [
                    ln for ln in safe_q.read_text(encoding="utf-8").splitlines()
                    if ln.strip()
                ]
                logger.info("%-28s : %d entries  (%s)", label, len(lines), safe_q)
            else:
                logger.info("%-28s : (not yet created)", label)
        except (OSError, ValueError) as exc:
            logger.warning("Could not read %s: %s", label, exc)

    return 0


# ── Argument parser ───────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ph_ai_tools_monitor.py",
        description=(
            "PRINTMAXX: Product Hunt AI Tools Monitor\n\n"
            "Scrapes PH for AI/productivity launches; routes high-upvote posts\n"
            "to founder outreach and engagement_bait_converter queues.\n\n"
            "Cron example (daily at 08:00):\n"
            "  0 8 * * * /usr/bin/python3 /path/to/ph_ai_tools_monitor.py --run"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--run",
        action="store_true",
        help="Scrape Product Hunt and route AI posts.",
    )
    mode.add_argument(
        "--status",
        action="store_true",
        help="Show last run state and queue depths.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate all writes without touching disk.",
    )
    return parser


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    logger = setup_logging()

    try:
        if args.run:
            sys.exit(cmd_run(args, logger))
        elif args.status:
            sys.exit(cmd_status(logger))
    except KeyboardInterrupt:
        logger.info("Interrupted.")
        sys.exit(0)
    except Exception as exc:
        logger.exception("Fatal unhandled error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()