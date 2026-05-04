#!/usr/bin/env python3
"""
PRINTMAXX Automation: PH AI Tool Launch Monitor

Daily scanner for ProductHunt AI builder/agent tool launches (Replit, Cursor, Bolt, etc.).
Scores each launch for APP_FACTORY throughput applicability, extracts affiliate links,
and queues 3 content pieces per launch via engagement_bait_converter.py.

Usage:
    python3 ph_ai_tool_monitor.py --run
    python3 ph_ai_tool_monitor.py --status
    python3 ph_ai_tool_monitor.py --dry-run
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

# ---------------------------------------------------------------------------
# Path bootstrap — try _common first, fall back to inline definitions
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result  # type: ignore
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p: Path) -> Path:
        """Validate that *p* resolves inside PROJECT and return it."""
        resolved = Path(p).resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError:
            raise ValueError(f"Path escape detected: {resolved} is outside {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result: dict, skill: str) -> None:
        return None


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_NAME = "ph_ai_tool_monitor"
LOG_FILE: Path = PROJECT / "AUTOMATIONS" / "logs" / f"{SCRIPT_NAME}.log"
OUTPUT_DIR: Path = PROJECT / "AUTOMATIONS" / "data" / SCRIPT_NAME
QUEUE_FILE: Path = OUTPUT_DIR / "content_queue.json"
LAUNCHES_CSV: Path = OUTPUT_DIR / "launches.csv"
STATUS_FILE: Path = OUTPUT_DIR / "status.json"
CONVERTER_SCRIPT: Path = PROJECT / "AUTOMATIONS" / "scripts" / "engagement_bait_converter.py"

# ProductHunt GraphQL endpoint
PH_GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"

# AI builder/agent tool keywords for relevance scoring
AI_BUILDER_KEYWORDS = [
    "replit", "cursor", "bolt", "lovable", "v0", "windsurf", "devin",
    "agent", "copilot", "ai builder", "ai dev", "no-code", "low-code",
    "code generation", "app factory", "ai tool", "ai assistant",
    "autonomous", "workflow", "automation", "llm", "generative",
    "claude", "openai", "gpt", "gemini", "anthropic",
]

APP_FACTORY_KEYWORDS = [
    "build", "ship", "deploy", "generate", "scaffold", "prototype",
    "production", "scale", "pipeline", "factory", "batch", "throughput",
    "fast", "instant", "one-click", "end-to-end", "full-stack",
]

# Minimum relevance score to qualify a launch
MIN_RELEVANCE_SCORE = 3
CONTENT_PIECES_PER_LAUNCH = 3


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging(dry_run: bool = False) -> logging.Logger:
    log_path = safe_path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(SCRIPT_NAME)
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ")

    fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    if dry_run:
        logger.info("DRY-RUN mode — no files will be written, no subprocesses launched")

    return logger


# ---------------------------------------------------------------------------
# ProductHunt data fetching
# ---------------------------------------------------------------------------

PH_QUERY = """
query FetchTodayLaunches($after: String) {
  posts(order: VOTES, after: $after, first: 50) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        name
        tagline
        description
        url
        votesCount
        commentsCount
        createdAt
        website
        thumbnail { url }
        topics {
          edges {
            node { name slug }
          }
        }
        makers {
          edges {
            node { name username twitterUsername }
          }
        }
      }
    }
  }
}
"""


def fetch_ph_launches(token: str, logger: logging.Logger) -> list:
    """Fetch today's ProductHunt launches via GraphQL. Returns list of post dicts."""
    launches = []
    cursor = None
    page = 0

    while True:
        page += 1
        variables = {}
        if cursor:
            variables["after"] = cursor

        payload = json.dumps({"query": PH_QUERY, "variables": variables}).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"PRINTMAXX/{SCRIPT_NAME}/1.0",
        }

        req = urllib.request.Request(PH_GRAPHQL_URL, data=payload, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            logger.error("PH GraphQL HTTP %s: %s", exc.code, exc.reason)
            break
        except urllib.error.URLError as exc:
            logger.error("PH GraphQL URL error: %s", exc.reason)
            break
        except json.JSONDecodeError as exc:
            logger.error("PH GraphQL JSON decode error: %s", exc)
            break

        errors = body.get("errors")
        if errors:
            logger.error("PH GraphQL errors: %s", errors)
            break

        posts_data = body.get("data", {}).get("posts", {})
        edges = posts_data.get("edges", [])
        for edge in edges:
            node = edge.get("node", {})
            launches.append(node)

        page_info = posts_data.get("pageInfo", {})
        if not page_info.get("hasNextPage") or page >= 5:
            break
        cursor = page_info.get("endCursor")
        logger.debug("Fetched page %d (%d posts so far)", page, len(launches))

    logger.info("Fetched %d total launches from ProductHunt", len(launches))
    return launches


def fetch_ph_launches_mock(logger: logging.Logger) -> list:
    """Return synthetic launch data for dry-run / testing without a PH token."""
    logger.info("Using MOCK ProductHunt data (no token provided)")
    return [
        {
            "id": "mock-001",
            "name": "Replit Agent 4",
            "tagline": "Build, design, and ship anything AI fast in one flow",
            "description": (
                "Replit Agent 4 lets you describe what you want to build and it "
                "autonomously writes code, installs packages, and deploys your app."
            ),
            "url": "https://www.producthunt.com/posts/replit-agent-4",
            "website": "https://replit.com",
            "votesCount": 1842,
            "commentsCount": 214,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "thumbnail": {"url": "https://ph-files.imgix.net/mock.png"},
            "topics": {"edges": [
                {"node": {"name": "Artificial Intelligence", "slug": "artificial-intelligence"}},
                {"node": {"name": "Developer Tools", "slug": "developer-tools"}},
            ]},
            "makers": {"edges": [
                {"node": {"name": "Amjad Masad", "username": "amasad", "twitterUsername": "amasad"}},
            ]},
        },
        {
            "id": "mock-002",
            "name": "Cursor Tab Pro",
            "tagline": "AI code completions that understand your whole codebase",
            "description": "Next-gen AI pair programmer with full repo context and agent mode.",
            "url": "https://www.producthunt.com/posts/cursor-tab-pro",
            "website": "https://cursor.sh",
            "votesCount": 967,
            "commentsCount": 88,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "thumbnail": {"url": "https://ph-files.imgix.net/mock2.png"},
            "topics": {"edges": [
                {"node": {"name": "Developer Tools", "slug": "developer-tools"}},
            ]},
            "makers": {"edges": []},
        },
    ]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_launch(post: dict) -> dict:
    """
    Score a PH post for AI builder relevance and APP_FACTORY throughput applicability.
    Returns a dict with scores and extracted metadata.
    """
    text = " ".join([
        (post.get("name") or ""),
        (post.get("tagline") or ""),
        (post.get("description") or ""),
    ]).lower()

    topics = [
        e["node"]["name"].lower()
        for e in post.get("topics", {}).get("edges", [])
    ]
    text_with_topics = text + " " + " ".join(topics)

    ai_score = sum(1 for kw in AI_BUILDER_KEYWORDS if kw in text_with_topics)
    factory_score = sum(1 for kw in APP_FACTORY_KEYWORDS if kw in text_with_topics)
    vote_bonus = min(post.get("votesCount", 0) // 200, 3)
    total_score = ai_score + factory_score + vote_bonus

    makers = [
        e["node"]
        for e in post.get("makers", {}).get("edges", [])
    ]
    affiliate_link = _build_affiliate_link(post.get("url", ""), post.get("id", ""))

    return {
        "id": post.get("id", ""),
        "name": post.get("name", ""),
        "tagline": post.get("tagline", ""),
        "url": post.get("url", ""),
        "website": post.get("website", ""),
        "votes": post.get("votesCount", 0),
        "comments": post.get("commentsCount", 0),
        "created_at": post.get("createdAt", ""),
        "topics": ", ".join(e["node"]["name"] for e in post.get("topics", {}).get("edges", [])),
        "makers": ", ".join(m.get("name", "") for m in makers),
        "maker_twitter": ", ".join(
            f"@{m['twitterUsername']}" for m in makers if m.get("twitterUsername")
        ),
        "ai_keyword_score": ai_score,
        "factory_keyword_score": factory_score,
        "vote_bonus": vote_bonus,
        "total_score": total_score,
        "qualifies": total_score >= MIN_RELEVANCE_SCORE,
        "affiliate_link": affiliate_link,
        "thumbnail": (post.get("thumbnail") or {}).get("url", ""),
    }


def _build_affiliate_link(ph_url: str, post_id: str) -> str:
    """Construct a ProductHunt affiliate/ref link."""
    if not ph_url:
        return ""
    parsed = urllib.parse.urlparse(ph_url)
    qs = urllib.parse.parse_qs(parsed.query)
    qs["ref"] = ["printmaxx_appfactory"]
    qs["utm_source"] = ["printmaxx"]
    qs["utm_medium"] = ["monitor"]
    qs["utm_campaign"] = [f"ph_launch_{post_id}"]
    new_query = urllib.parse.urlencode({k: v[0] for k, v in qs.items()})
    return urllib.parse.urlunparse(parsed._replace(query=new_query))


# ---------------------------------------------------------------------------
# Content queue generation
# ---------------------------------------------------------------------------

CONTENT_TEMPLATES = [
    {
        "type": "thread",
        "template": (
            "🧵 Just spotted {name} on @ProductHunt\n\n"
            "{tagline}\n\n"
            "Here's why this matters for AI app builders: [EXPAND]\n\n"
            "APP_FACTORY score: {total_score}/10\n\n"
            "Link: {affiliate_link}"
        ),
    },
    {
        "type": "short_form",
        "template": (
            "{name} dropped on PH today 👀\n\n"
            "'{tagline}'\n\n"
            "If you're building AI apps at scale, this could 10x your throughput.\n\n"
            "→ {affiliate_link}\n\n"
            "#AITools #AppFactory #BuildWithAI"
        ),
    },
    {
        "type": "review_post",
        "template": (
            "REVIEW: {name}\n\n"
            "Tagline: {tagline}\n\n"
            "APP_FACTORY Applicability Score: {total_score}/10\n"
            "AI Keyword Matches: {ai_keyword_score}\n"
            "Throughput Signals: {factory_keyword_score}\n"
            "PH Votes: {votes}\n\n"
            "Why it matters for batch app production: [DEEP DIVE]\n\n"
            "Affiliate: {affiliate_link}\n"
            "Made by: {makers}"
        ),
    },
]


def generate_content_queue(scored_launches: list) -> list:
    """Generate CONTENT_PIECES_PER_LAUNCH content items per qualifying launch."""
    queue = []
    templates = CONTENT_TEMPLATES[:CONTENT_PIECES_PER_LAUNCH]

    for launch in scored_launches:
        if not launch["qualifies"]:
            continue
        for tmpl in templates:
            content = tmpl["template"].format(**{k: str(v) for k, v in launch.items()})
            queue.append({
                "launch_id": launch["id"],
                "launch_name": launch["name"],
                "content_type": tmpl["type"],
                "content": content,
                "affiliate_link": launch["affiliate_link"],
                "score": launch["total_score"],
                "queued_at": datetime.now(timezone.utc).isoformat(),
                "status": "pending",
            })

    return queue


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _ensure_dirs(dry_run: bool, logger: logging.Logger) -> None:
    if dry_run:
        return
    for d in [LOG_FILE.parent, OUTPUT_DIR]:
        safe_path(d).mkdir(parents=True, exist_ok=True)


def save_launches_csv(launches: list, dry_run: bool, logger: logging.Logger) -> None:
    if not launches:
        logger.info("No launches to save to CSV")
        return
    if dry_run:
        logger.info("[DRY-RUN] Would write %d launches to %s", len(launches), LAUNCHES_CSV)
        return

    dest = safe_path(LAUNCHES_CSV)
    fieldnames = list(launches[0].keys())
    try:
        with dest.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(launches)
        logger.info("Wrote %d launches to %s", len(launches), dest)
    except OSError as exc:
        logger.error("Failed to write launches CSV: %s", exc)


def save_content_queue(queue: list, dry_run: bool, logger: logging.Logger) -> None:
    if not queue:
        logger.info("Content queue is empty — no qualifying launches")
        return
    if dry_run:
        logger.info("[DRY-RUN] Would write %d content items to %s", len(queue), QUEUE_FILE)
        for item in queue:
            logger.info("  [%s] %s: %s...", item["content_type"], item["launch_name"], item["content"][:80])
        return

    dest = safe_path(QUEUE_FILE)
    # Merge with existing queue
    existing = []
    if dest.exists():
        try:
            with dest.open("r", encoding="utf-8") as fh:
                existing = json.load(fh)
        except (json.JSONDecodeError, OSError):
            existing = []

    existing_ids = {(i["launch_id"], i["content_type"]) for i in existing}
    new_items = [i for i in queue if (i["launch_id"], i["content_type"]) not in existing_ids]
    merged = existing + new_items

    try:
        with dest.open("w", encoding="utf-8") as fh:
            json.dump(merged, fh, indent=2, ensure_ascii=False)
        logger.info("Content queue: %d new items added (%d total) → %s", len(new_items), len(merged), dest)
    except OSError as exc:
        logger.error("Failed to write content queue: %s", exc)


def save_status(data: dict, dry_run: bool, logger: logging.Logger) -> None:
    if dry_run:
        return
    dest = safe_path(STATUS_FILE)
    try:
        with dest.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
    except OSError as exc:
        logger.error("Failed to write status file: %s", exc)


def load_status(logger: logging.Logger) -> dict:
    dest = safe_path(STATUS_FILE)
    if not dest.exists():
        return {}
    try:
        with dest.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read status file: %s", exc)
        return {}


# ---------------------------------------------------------------------------
# Converter handoff
# ---------------------------------------------------------------------------

def invoke_converter(queue: list, dry_run: bool, logger: logging.Logger) -> None:
    """Call engagement_bait_converter.py for each pending content item."""
    if not queue:
        return

    converter = safe_path(CONVERTER_SCRIPT)
    if not converter.exists():
        logger.warning("Converter script not found at %s — skipping handoff", converter)
        return

    pending = [i for i in queue if i.get("status") == "pending"]
    logger.info("Handing off %d pending items to engagement_bait_converter", len(pending))

    for item in pending:
        payload = json.dumps(item)
        cmd = [sys.executable, str(converter), "--input-json", payload]
        if dry_run:
            logger.info("[DRY-RUN] Would invoke: %s", " ".join(cmd[:3] + ["..."]))
            continue
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                logger.info("Converter OK: %s / %s", item["launch_name"], item["content_type"])
                item["status"] = "converted"
            else:
                logger.warning(
                    "Converter exited %d for %s: %s",
                    result.returncode, item["launch_name"], result.stderr[:200],
                )
        except subprocess.TimeoutExpired:
            logger.error("Converter timed out for %s", item["launch_name"])
        except OSError as exc:
            logger.error("Converter launch error: %s", exc)


# ---------------------------------------------------------------------------
# CLI handlers
# ---------------------------------------------------------------------------

def _load_ph_token(logger: logging.Logger) -> str:
    """Try to load PH API token from env-style config file or environment."""
    import os  # stdlib — not exotic

    token = os.environ.get("PH_API_TOKEN", "")
    if token:
        return token

    config_path = PROJECT / "AUTOMATIONS" / "config" / "ph_api.json"
    if config_path.exists():
        try:
            with safe_path(config_path).open("r", encoding="utf-8") as fh:
                cfg = json.load(fh)
            token = cfg.get("token", "")
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not read PH config: %s", exc)

    return token


def cmd_run(args: argparse.Namespace, logger: logging.Logger) -> int:
    dry_run = args.dry_run
    logger.info("=== PH AI Tool Monitor RUN start (dry_run=%s) ===", dry_run)

    _ensure_dirs(dry_run, logger)

    token = _load_ph_token(logger)
    if token:
        raw_launches = fetch_ph_launches(token, logger)
    else:
        logger.warning("No PH_API_TOKEN found — falling back to mock data")
        raw_launches = fetch_ph_launches_mock(logger)

    if not raw_launches:
        logger.warning("No launches fetched — exiting cleanly")
        return 0

    scored = [score_launch(post) for post in raw_launches]
    qualified = [s for s in scored if s["qualifies"]]
    logger.info(
        "Scored %d launches: %d qualify (score >= %d)",
        len(scored), len(qualified), MIN_RELEVANCE_SCORE,
    )

    # Log top qualifiers
    for launch in sorted(qualified, key=lambda x: x["total_score"], reverse=True)[:5]:
        logger.info(
            "  QUALIFIED [%d] %s — %s",
            launch["total_score"], launch["name"], launch["tagline"][:60],
        )

    save_launches_csv(scored, dry_run, logger)

    queue = generate_content_queue(scored)
    save_content_queue(queue, dry_run, logger)

    invoke_converter(queue, dry_run, logger)

    status = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "launches_fetched": len(raw_launches),
        "launches_qualified": len(qualified),
        "content_items_queued": len(queue),
        "dry_run": dry_run,
    }
    save_status(status, dry_run, logger)
    logger.info("=== RUN complete: %d items queued ===", len(queue))
    return 0


def cmd_status(logger: logging.Logger) -> int:
    status = load_status(logger)
    if not status:
        print("No status data found. Run with --run first.")
        return 0

    print(f"Last run:          {status.get('last_run', 'N/A')}")
    print(f"Launches fetched:  {status.get('launches_fetched', 0)}")
    print(f"Launches qualified:{status.get('launches_qualified', 0)}")
    print(f"Content queued:    {status.get('content_items_queued', 0)}")
    print(f"Dry run:           {status.get('dry_run', False)}")

    queue_dest = safe_path(QUEUE_FILE)
    if queue_dest.exists():
        try:
            with queue_dest.open("r", encoding="utf-8") as fh:
                queue = json.load(fh)
            pending = sum(1 for i in queue if i.get("status") == "pending")
            converted = sum(1 for i in queue if i.get("status") == "converted")
            print(f"\nQueue totals:      {len(queue)} items ({pending} pending, {converted} converted)")
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not read queue file: %s", exc)

    return 0


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description="PRINTMAXX: ProductHunt AI tool launch monitor for APP_FACTORY",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Run the full scan and queue pipeline")
    group.add_argument("--status", action="store_true", help="Show last-run status")
    group.add_argument("--dry-run", action="store_true", help="Simulate run without writing files")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logger = setup_logging(dry_run=getattr(args, "dry_run", False))

    try:
        if args.status:
            sys.exit(cmd_status(logger))
        else:
            sys.exit(cmd_run(args, logger))
    except KeyboardInterrupt:
        logger.info("Interrupted — exiting cleanly")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unhandled error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()