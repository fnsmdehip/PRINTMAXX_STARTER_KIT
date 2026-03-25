#!/usr/bin/env python3
"""
PRINTMAXX Automation: Product Hunt Dev Utility Monitor

Daily scraper for Product Hunt /topics/developer-tools. Identifies utility app
launches (file preview, code tools, macOS utilities with 100+ upvotes), extracts
concept patterns for the App Factory queue, and generates dev-productivity content
posts from qualifying launches.

Usage:
    python ph_dev_utility_monitor.py --run
    python ph_dev_utility_monitor.py --status
    python ph_dev_utility_monitor.py --dry-run
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import from _common or define fallbacks
# ---------------------------------------------------------------------------

try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result  # noqa: F401
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(target: Path) -> Path:
        """Validate that *target* resolves inside PROJECT and return it."""
        resolved = Path(target).resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError:
            raise ValueError(
                f"Path escape blocked: {resolved} is outside PROJECT {PROJECT}"
            )
        return resolved

    def recall_skills_for_task(task: str) -> dict:  # noqa: D401
        """Stub when _common is unavailable."""
        return {}

    def capture_skill_from_result(result: dict, task: str) -> None:  # noqa: D401
        """Stub when _common is unavailable."""
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_NAME = "ph_dev_utility_monitor"
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS_DIR / "logs" / f"{SCRIPT_NAME}.log"
OUTPUT_DIR = AUTOMATIONS_DIR / "data" / SCRIPT_NAME
QUEUE_FILE = OUTPUT_DIR / "app_factory_queue.json"
RUNS_CSV = OUTPUT_DIR / "runs.csv"
POSTS_CSV = OUTPUT_DIR / "qualifying_posts.csv"
CONTENT_DIR = OUTPUT_DIR / "content_posts"

PH_GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"
PH_TOPIC_SLUG = "developer-tools"
MIN_VOTES = 100

UTILITY_KEYWORDS = {
    "file preview", "quick look", "code tool", "macos utility", "developer tool",
    "markdown", "sqlite", "mermaid", "preview", "file manager", "productivity",
    "terminal", "cli", "command line", "text editor", "code editor", "diff",
    "git", "database", "api", "debug", "profiler", "lint", "format", "snippet",
    "clipboard", "launcher", "spotlight", "alfred", "raycast", "automator",
    "workflow", "script", "regex", "json", "yaml", "csv viewer",
}

POSTS_CSV_FIELDS = [
    "scraped_at", "post_id", "name", "tagline", "votes", "url",
    "website", "topics", "matched_keywords",
]

RUNS_CSV_FIELDS = ["run_at", "mode", "posts_fetched", "qualifying", "queued", "status"]


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(message: str, level: str = "INFO") -> None:
    """Append a timestamped log entry to LOG_FILE."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = f"[{timestamp}] [{level}] {message}"
    print(entry)
    try:
        log_path = safe_path(LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(entry + "\n")
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] Could not write log: {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Product Hunt API
# ---------------------------------------------------------------------------

GRAPHQL_QUERY = """
query DevToolPosts($topic: String!, $cursor: String) {
  posts(topic: $topic, order: VOTES, after: $cursor, first: 50) {
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
        votesCount
        createdAt
        url
        website
        topics {
          edges {
            node {
              name
              slug
            }
          }
        }
      }
    }
  }
}
"""


def fetch_ph_posts(api_token: str, dry_run: bool = False) -> list[dict]:
    """Fetch posts from PH GraphQL API for the developer-tools topic."""
    if dry_run:
        log("DRY-RUN: skipping live PH API call, returning sample data")
        return _sample_posts()

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": f"PRINTMAXX/{SCRIPT_NAME} (+automation)",
    }

    all_posts: list[dict] = []
    cursor = None

    for page in range(1, 6):  # max 5 pages / 250 posts
        payload = json.dumps(
            {
                "query": GRAPHQL_QUERY,
                "variables": {"topic": PH_TOPIC_SLUG, "cursor": cursor},
            }
        ).encode("utf-8")

        req = urllib.request.Request(PH_GRAPHQL_URL, data=payload, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            log(f"HTTP {exc.code} on page {page}: {exc.reason}", "ERROR")
            break
        except urllib.error.URLError as exc:
            log(f"URL error on page {page}: {exc.reason}", "ERROR")
            break

        if "errors" in body:
            log(f"GraphQL errors: {body['errors']}", "ERROR")
            break

        edges = body.get("data", {}).get("posts", {}).get("edges", [])
        page_info = body.get("data", {}).get("posts", {}).get("pageInfo", {})

        for edge in edges:
            node = edge.get("node", {})
            topic_names = [
                t["node"]["name"]
                for t in node.get("topics", {}).get("edges", [])
            ]
            all_posts.append(
                {
                    "id": node.get("id"),
                    "name": node.get("name", ""),
                    "tagline": node.get("tagline", ""),
                    "description": node.get("description", ""),
                    "votes": node.get("votesCount", 0),
                    "created_at": node.get("createdAt", ""),
                    "url": node.get("url", ""),
                    "website": node.get("website", ""),
                    "topics": topic_names,
                }
            )

        log(f"Page {page}: fetched {len(edges)} posts (total so far: {len(all_posts)})")

        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")

    return all_posts


def _sample_posts() -> list[dict]:
    """Return a minimal set of fake posts for dry-run / CI testing."""
    return [
        {
            "id": "dry-001",
            "name": "Looq: Preview Files",
            "tagline": "A better Quick Look: code, Markdown, Mermaid, SQLite & more",
            "description": "Looq extends Quick Look with syntax highlighting, Mermaid diagrams, SQLite browser, and more.",
            "votes": 387,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "url": "https://www.producthunt.com/posts/looq-preview-files",
            "website": "https://looq.app",
            "topics": ["Developer Tools", "macOS", "Productivity"],
        },
        {
            "id": "dry-002",
            "name": "CodeSnap Pro",
            "tagline": "Beautiful code screenshots for developers",
            "description": "Turn your code into shareable images with syntax highlighting.",
            "votes": 142,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "url": "https://www.producthunt.com/posts/codesnap-pro",
            "website": "https://codesnap.app",
            "topics": ["Developer Tools", "Design"],
        },
        {
            "id": "dry-003",
            "name": "SimpleChat",
            "tagline": "Chat with friends",
            "description": "A simple chat app.",
            "votes": 45,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "url": "https://www.producthunt.com/posts/simplechat",
            "website": "https://simplechat.io",
            "topics": ["Messaging"],
        },
    ]


# ---------------------------------------------------------------------------
# Filtering & pattern extraction
# ---------------------------------------------------------------------------

def matches_utility_criteria(post: dict) -> tuple[bool, list[str]]:
    """Return (qualifies, matched_keywords) for a post."""
    if post["votes"] < MIN_VOTES:
        return False, []

    combined = " ".join([
        post["name"],
        post["tagline"],
        post["description"] or "",
        " ".join(post["topics"]),
    ]).lower()

    matched = [kw for kw in UTILITY_KEYWORDS if kw in combined]
    return bool(matched), matched


def extract_concept_pattern(post: dict, matched_keywords: list[str]) -> dict:
    """Derive an App Factory clone-target spec from a qualifying post."""
    topics_lower = [t.lower() for t in post["topics"]]

    platform = "macOS" if any("macos" in t or "mac" in t for t in topics_lower) else "cross-platform"
    primary_capability = matched_keywords[0] if matched_keywords else "utility"

    # Rough category heuristics
    if any(k in matched_keywords for k in ("file preview", "quick look", "preview")):
        category = "file-preview-utility"
    elif any(k in matched_keywords for k in ("code tool", "code editor", "text editor")):
        category = "code-editor-tool"
    elif any(k in matched_keywords for k in ("terminal", "cli", "command line")):
        category = "terminal-cli-utility"
    elif any(k in matched_keywords for k in ("git",)):
        category = "git-helper"
    elif any(k in matched_keywords for k in ("database", "sqlite")):
        category = "database-browser"
    else:
        category = "developer-productivity"

    return {
        "source_id": post["id"],
        "source_name": post["name"],
        "source_url": post["url"],
        "source_votes": post["votes"],
        "platform": platform,
        "category": category,
        "primary_capability": primary_capability,
        "matched_keywords": matched_keywords,
        "clone_target_summary": (
            f"Build a {platform} {category} inspired by '{post['name']}': "
            f"{post['tagline']}"
        ),
        "queued_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Content post generation
# ---------------------------------------------------------------------------

CONTENT_TEMPLATE = """\
# Dev Productivity Spotlight: {name}

**Tagline:** {tagline}
**Votes:** {votes} | **Source:** {url}

## What it does
{description}

## Why developers love it
{name} hits the sweet spot for developer utilities: {matched_summary}.
With {votes} upvotes on launch day, it's clearly solving a real pain point.

## Key concept for builders
Category: **{category}** — Platform: **{platform}**

If you're building in this space, consider:
- Core capability: {primary_capability}
- Keyword signals: {keywords}
- Differentiation angle: extend the core with integrations or a tighter UX.

## App Factory Note
Clone target queued. Primary capability: `{primary_capability}`.
Build priority score (votes / 100): **{priority:.1f}**

---
*Auto-generated by PRINTMAXX / {script} on {date}*
"""


def generate_content_post(post: dict, pattern: dict) -> str:
    """Render a markdown content post for a qualifying launch."""
    desc = (post["description"] or post["tagline"] or "").strip()
    if len(desc) > 300:
        desc = desc[:297] + "..."

    return CONTENT_TEMPLATE.format(
        name=post["name"],
        tagline=post["tagline"],
        votes=post["votes"],
        url=post["url"],
        description=desc,
        matched_summary=", ".join(pattern["matched_keywords"][:5]),
        category=pattern["category"],
        platform=pattern["platform"],
        primary_capability=pattern["primary_capability"],
        keywords=", ".join(pattern["matched_keywords"]),
        priority=post["votes"] / 100,
        script=SCRIPT_NAME,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    )


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def _ensure_dirs(dry_run: bool = False) -> None:
    if dry_run:
        return
    for d in (OUTPUT_DIR, CONTENT_DIR, LOG_FILE.parent):
        safe_path(d).mkdir(parents=True, exist_ok=True)


def load_queue() -> list[dict]:
    try:
        p = safe_path(QUEUE_FILE)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        log(f"Could not load queue: {exc}", "WARN")
    return []


def save_queue(queue: list[dict], dry_run: bool = False) -> None:
    if dry_run:
        log(f"DRY-RUN: would write {len(queue)} items to queue")
        return
    path = safe_path(QUEUE_FILE)
    path.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"Queue saved: {len(queue)} items → {path}")


def append_posts_csv(qualifying: list[tuple[dict, list[str]]], dry_run: bool = False) -> None:
    if dry_run:
        return
    path = safe_path(POSTS_CSV)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=POSTS_CSV_FIELDS)
        if write_header:
            writer.writeheader()
        scraped_at = datetime.now(timezone.utc).isoformat()
        for post, keywords in qualifying:
            writer.writerow(
                {
                    "scraped_at": scraped_at,
                    "post_id": post["id"],
                    "name": post["name"],
                    "tagline": post["tagline"],
                    "votes": post["votes"],
                    "url": post["url"],
                    "website": post["website"],
                    "topics": "|".join(post["topics"]),
                    "matched_keywords": "|".join(keywords),
                }
            )


def append_run_csv(
    mode: str,
    posts_fetched: int,
    qualifying: int,
    queued: int,
    status: str,
    dry_run: bool = False,
) -> None:
    if dry_run:
        return
    path = safe_path(RUNS_CSV)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=RUNS_CSV_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(
            {
                "run_at": datetime.now(timezone.utc).isoformat(),
                "mode": mode,
                "posts_fetched": posts_fetched,
                "qualifying": qualifying,
                "queued": queued,
                "status": status,
            }
        )


def write_content_post(post: dict, content: str, dry_run: bool = False) -> None:
    slug = post["name"].lower().replace(" ", "_")[:40]
    slug = "".join(c if c.isalnum() or c == "_" else "" for c in slug)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    filename = f"{date_str}_{slug}.md"
    path = safe_path(CONTENT_DIR / filename)
    if dry_run:
        log(f"DRY-RUN: would write content post → {path}")
        return
    path.write_text(content, encoding="utf-8")
    log(f"Content post written → {path}")


# ---------------------------------------------------------------------------
# Core run logic
# ---------------------------------------------------------------------------

def run(dry_run: bool = False) -> int:
    """Execute the full scrape-filter-queue-content pipeline. Returns exit code."""
    mode = "dry-run" if dry_run else "run"
    log(f"=== {SCRIPT_NAME} starting [{mode}] ===")

    try:
        _ensure_dirs(dry_run)
    except Exception as exc:
        log(f"Directory setup failed: {exc}", "ERROR")
        return 1

    api_token = os.environ.get("PH_API_TOKEN", "")
    if not api_token and not dry_run:
        log("PH_API_TOKEN not set — aborting live run", "ERROR")
        return 1

    # Recall any stored skills/context for this task
    try:
        recall_skills_for_task("ph_scrape_dev_tools")
    except Exception:
        pass

    # Fetch
    try:
        posts = fetch_ph_posts(api_token, dry_run=dry_run)
    except Exception as exc:
        log(f"Fetch failed: {exc}", "ERROR")
        append_run_csv(mode, 0, 0, 0, "fetch_error", dry_run=dry_run)
        return 1

    log(f"Fetched {len(posts)} posts total")

    # Filter
    qualifying: list[tuple[dict, list[str]]] = []
    for post in posts:
        ok, keywords = matches_utility_criteria(post)
        if ok:
            qualifying.append((post, keywords))
            log(f"  QUALIFY [{post['votes']:>4}v] {post['name']} — {keywords}")
        else:
            log(f"  skip    [{post['votes']:>4}v] {post['name']}")

    log(f"Qualifying posts: {len(qualifying)}/{len(posts)}")

    # Load existing queue, de-duplicate by source_id
    queue = load_queue()
    existing_ids = {item["source_id"] for item in queue}
    new_patterns: list[dict] = []

    for post, keywords in qualifying:
        pattern = extract_concept_pattern(post, keywords)
        if pattern["source_id"] not in existing_ids:
            new_patterns.append(pattern)
            existing_ids.add(pattern["source_id"])
            content = generate_content_post(post, pattern)
            write_content_post(post, content, dry_run=dry_run)

    queue.extend(new_patterns)
    save_queue(queue, dry_run=dry_run)
    append_posts_csv(qualifying, dry_run=dry_run)
    append_run_csv(mode, len(posts), len(qualifying), len(new_patterns), "ok", dry_run=dry_run)

    # Capture skill from result for future sessions
    try:
        capture_skill_from_result(
            {
                "posts_fetched": len(posts),
                "qualifying": len(qualifying),
                "new_queued": len(new_patterns),
            },
            "ph_scrape_dev_tools",
        )
    except Exception:
        pass

    log(f"=== Done: {len(new_patterns)} new items queued ===")
    return 0


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------

def status() -> int:
    """Print a summary of the current queue and recent runs."""
    print(f"\n{'='*60}")
    print(f"  {SCRIPT_NAME} — STATUS REPORT")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"{'='*60}\n")

    # Queue summary
    try:
        queue = load_queue()
        print(f"App Factory Queue: {len(queue)} items")
        by_category: dict[str, int] = {}
        for item in queue:
            cat = item.get("category", "unknown")
            by_category[cat] = by_category.get(cat, 0) + 1
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            print(f"  {count:>4}  {cat}")
    except Exception as exc:
        print(f"  [error reading queue: {exc}]")

    print()

    # Recent runs
    try:
        runs_path = safe_path(RUNS_CSV)
        if runs_path.exists():
            with runs_path.open(encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            recent = rows[-10:]
            print(f"Recent runs (last {len(recent)}):")
            for row in recent:
                print(
                    f"  {row.get('run_at','')}  "
                    f"mode={row.get('mode','')}  "
                    f"fetched={row.get('posts_fetched','')}  "
                    f"qualifying={row.get('qualifying','')}  "
                    f"queued={row.get('queued','')}  "
                    f"status={row.get('status','')}"
                )
        else:
            print("No run history found.")
    except Exception as exc:
        print(f"  [error reading runs: {exc}]")

    # Content posts
    try:
        content_path = safe_path(CONTENT_DIR)
        if content_path.exists():
            posts = sorted(content_path.glob("*.md"))
            print(f"\nContent posts: {len(posts)} files")
            for p in posts[-5:]:
                print(f"  {p.name}")
    except Exception as exc:
        print(f"  [error reading content: {exc}]")

    print()
    return 0


# ---------------------------------------------------------------------------
# Git / subprocess helper (optional: auto-commit outputs)
# ---------------------------------------------------------------------------

def git_add_outputs(dry_run: bool = False) -> None:
    """Stage new output files if inside a git repo (best-effort)."""
    if dry_run:
        return
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return
        subprocess.run(
            ["git", "-C", str(PROJECT), "add", str(OUTPUT_DIR)],
            capture_output=True,
            timeout=10,
        )
        log("git add of output directory completed (commit separately)")
    except Exception as exc:
        log(f"git add skipped: {exc}", "WARN")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "PRINTMAXX: Scrape PH /developer-tools for utility app launches, "
            "feed App Factory queue, generate content posts."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Run the full scrape-filter-queue-content pipeline (requires PH_API_TOKEN).",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print queue summary and recent run history.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate a run using sample data; no files written, no API calls.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            sys.exit(status())
        elif args.dry_run:
            sys.exit(run(dry_run=True))
        else:
            code = run(dry_run=False)
            if code == 0:
                git_add_outputs()
            sys.exit(code)
    except KeyboardInterrupt:
        log("Interrupted by user", "WARN")
        sys.exit(130)
    except Exception as exc:
        log(f"Unhandled exception: {exc}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()