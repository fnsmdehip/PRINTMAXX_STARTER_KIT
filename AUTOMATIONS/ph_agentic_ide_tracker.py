#!/usr/bin/env python3
"""
PRINTMAXX Automation: ProductHunt Agentic IDE Tracker

Monitors ProductHunt daily for agentic IDE / AI coding tool launches,
auto-generates comparison content (vs Cursor, Claude Code, Windsurf),
checks for affiliate programs, and routes to the content pipeline for
SEO and community distribution.

Usage:
    python ph_agentic_ide_tracker.py --run
    python ph_agentic_ide_tracker.py --status
    python ph_agentic_ide_tracker.py --dry-run
"""

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

# ---------------------------------------------------------------------------
# _common import with fallback
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

    def safe_path(target: Path) -> Path:
        """Validate that target resolves inside PROJECT."""
        resolved = target.resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError:
            raise ValueError(
                f"Path escape detected: {resolved} is outside PROJECT {PROJECT}"
            )
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result: dict, task: str) -> None:
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS_DIR / "logs" / "ph_agentic_ide_tracker.log"
DATA_DIR = AUTOMATIONS_DIR / "data" / "ph_agentic_ide"
CONTENT_DIR = AUTOMATIONS_DIR / "content" / "comparisons"
PIPELINE_DIR = AUTOMATIONS_DIR / "pipeline" / "pending"
STATE_FILE = DATA_DIR / "seen_launches.json"
CSV_LOG = DATA_DIR / "launches.csv"

COMPARISON_TOOLS = ["Cursor", "Claude Code", "Windsurf"]

AFFILIATE_PATTERNS = [
    "affiliate",
    "partner",
    "referral",
    "ref=",
    "/partners",
    "/affiliates",
    "commission",
    "revenue share",
]

KEYWORD_TRIGGERS = [
    "agentic",
    "agentic ide",
    "ai coding",
    "ai code editor",
    "ai ide",
    "copilot",
    "code assistant",
    "developer ai",
    "autonomous coding",
    "vibe coding",
    "llm ide",
    "ai pair programming",
]

PH_GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"
PH_API_TOKEN = os.environ.get("PH_API_TOKEN", "")

CSV_HEADERS = [
    "date",
    "id",
    "name",
    "tagline",
    "url",
    "votes",
    "topics",
    "website",
    "affiliate_found",
    "content_generated",
    "routed_to_pipeline",
]


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
def setup_logging() -> logging.Logger:
    try:
        log_path = safe_path(LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    except (ValueError, OSError) as exc:
        print(f"[ERROR] Cannot initialise log path: {exc}", file=sys.stderr)
        sys.exit(1)

    logger = logging.getLogger("ph_agentic_ide_tracker")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
    )

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


logger = setup_logging()


# ---------------------------------------------------------------------------
# Directory bootstrap
# ---------------------------------------------------------------------------
def bootstrap_dirs() -> None:
    for d in [DATA_DIR, CONTENT_DIR, PIPELINE_DIR]:
        try:
            safe_path(d).mkdir(parents=True, exist_ok=True)
        except (ValueError, OSError) as exc:
            logger.error("Failed to create directory %s: %s", d, exc)
            sys.exit(1)


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------
def load_seen_ids() -> set:
    try:
        p = safe_path(STATE_FILE)
        if p.exists():
            with p.open("r", encoding="utf-8") as fh:
                return set(json.load(fh).get("seen", []))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        logger.warning("Could not load seen IDs: %s", exc)
    return set()


def save_seen_ids(seen: set, dry_run: bool = False) -> None:
    if dry_run:
        return
    try:
        p = safe_path(STATE_FILE)
        with p.open("w", encoding="utf-8") as fh:
            json.dump({"seen": sorted(seen), "updated": datetime.now(timezone.utc).isoformat()}, fh, indent=2)
    except (ValueError, OSError) as exc:
        logger.error("Failed to save seen IDs: %s", exc)


# ---------------------------------------------------------------------------
# ProductHunt API
# ---------------------------------------------------------------------------
def _graphql_request(query: str, variables: dict) -> dict:
    if not PH_API_TOKEN:
        raise RuntimeError("PH_API_TOKEN environment variable is not set.")

    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        PH_GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PH_API_TOKEN}",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_daily_launches(date_str: str) -> list:
    """Return today's ProductHunt launches as a list of dicts."""
    query = """
    query DailyPosts($postedAfter: DateTime!, $postedBefore: DateTime!, $after: String) {
      posts(
        postedAfter: $postedAfter
        postedBefore: $postedBefore
        order: VOTES
        after: $after
        first: 50
      ) {
        pageInfo { hasNextPage endCursor }
        edges {
          node {
            id
            name
            tagline
            url
            votesCount
            website
            topics { edges { node { name } } }
          }
        }
      }
    }
    """
    launches = []
    after_cursor = None

    # date_str = "YYYY-MM-DD"
    posted_after = f"{date_str}T00:00:00Z"
    posted_before = f"{date_str}T23:59:59Z"

    while True:
        variables = {
            "postedAfter": posted_after,
            "postedBefore": posted_before,
        }
        if after_cursor:
            variables["after"] = after_cursor

        data = _graphql_request(query, variables)
        posts = data.get("data", {}).get("posts", {})
        edges = posts.get("edges", [])

        for edge in edges:
            node = edge.get("node", {})
            topics = [
                t["node"]["name"]
                for t in node.get("topics", {}).get("edges", [])
            ]
            launches.append({
                "id": node.get("id"),
                "name": node.get("name", ""),
                "tagline": node.get("tagline", ""),
                "url": node.get("url", ""),
                "votes": node.get("votesCount", 0),
                "website": node.get("website", ""),
                "topics": topics,
                "date": date_str,
            })

        page_info = posts.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break
        after_cursor = page_info.get("endCursor")

    return launches


# ---------------------------------------------------------------------------
# Relevance filter
# ---------------------------------------------------------------------------
def is_relevant(launch: dict) -> bool:
    text = (
        launch.get("name", "") + " " +
        launch.get("tagline", "") + " " +
        " ".join(launch.get("topics", []))
    ).lower()
    return any(kw in text for kw in KEYWORD_TRIGGERS)


# ---------------------------------------------------------------------------
# Affiliate check
# ---------------------------------------------------------------------------
def check_affiliate_program(website: str) -> dict:
    """Lightweight affiliate check: probe common paths and scan homepage."""
    result = {"found": False, "url": "", "note": ""}
    if not website:
        result["note"] = "no website"
        return result

    common_paths = ["/affiliates", "/partners", "/affiliate", "/partner-program", "/referral"]
    for path in common_paths:
        probe_url = website.rstrip("/") + path
        try:
            req = urllib.request.Request(
                probe_url,
                headers={"User-Agent": "PRINTMAXX-Bot/1.0 (affiliate-check)"},
                method="HEAD",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status in (200, 301, 302):
                    result["found"] = True
                    result["url"] = probe_url
                    result["note"] = f"HTTP {resp.status} at {probe_url}"
                    return result
        except (urllib.error.URLError, OSError):
            continue

    # Scan homepage text for affiliate keywords
    try:
        req = urllib.request.Request(
            website,
            headers={"User-Agent": "PRINTMAXX-Bot/1.0 (affiliate-check)"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read(65536).decode("utf-8", errors="replace").lower()
            for pat in AFFILIATE_PATTERNS:
                if pat in html:
                    result["found"] = True
                    result["url"] = website
                    result["note"] = f"Keyword '{pat}' found on homepage"
                    return result
    except (urllib.error.URLError, OSError):
        pass

    result["note"] = "not found"
    return result


# ---------------------------------------------------------------------------
# Comparison content generator
# ---------------------------------------------------------------------------
def generate_comparison_content(launch: dict, affiliate_info: dict) -> dict:
    name = launch["name"]
    tagline = launch["tagline"]
    url = launch["url"]
    website = launch["website"]
    votes = launch["votes"]
    date = launch["date"]

    affiliate_note = (
        f"**Affiliate program found:** {affiliate_info['url']}"
        if affiliate_info["found"]
        else "No affiliate program detected yet — check manually."
    )

    comparisons = {}
    for tool in COMPARISON_TOOLS:
        comparisons[tool] = _comparison_block(name, tagline, tool)

    content = {
        "title": f"{name} vs {', '.join(COMPARISON_TOOLS)}: Which Agentic IDE Wins?",
        "meta_description": (
            f"{name} launched on ProductHunt: '{tagline}'. "
            f"We compare it head-to-head with {', '.join(COMPARISON_TOOLS)} "
            "so you can pick the right AI coding tool."
        ),
        "slug": _slugify(f"{name}-vs-cursor-claude-code-windsurf"),
        "product": {
            "name": name,
            "tagline": tagline,
            "ph_url": url,
            "website": website,
            "votes": votes,
            "launched": date,
        },
        "affiliate": affiliate_info,
        "affiliate_cta": affiliate_note,
        "comparisons": comparisons,
        "seo_keywords": [
            f"{name} vs Cursor",
            f"{name} vs Claude Code",
            f"{name} vs Windsurf",
            f"{name} review",
            f"best agentic IDE {date[:4]}",
            "AI coding tool comparison",
        ],
        "community_hooks": {
            "reddit_r_programming": f"I tested {name} (just launched on PH) against Cursor & Claude Code — here's what happened",
            "reddit_r_webdev": f"New AI IDE '{name}' vs the big 3 — raw first impressions",
            "twitter": f"🚀 {name} just dropped on @ProductHunt — '{tagline}'. We put it through its paces vs Cursor, Claude Code & Windsurf. Full breakdown 👇",
            "hackernews": f"{name} – {tagline} (producthunt.com)",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    return content


def _comparison_block(name: str, tagline: str, competitor: str) -> dict:
    return {
        "headline": f"{name} vs {competitor}",
        "intro": (
            f"{name} ({tagline}) entered a market already shaped by {competitor}. "
            f"Here's a direct comparison to help developers decide."
        ),
        "dimensions": [
            {
                "dimension": "Agentic capability",
                "notes": f"Evaluate whether {name}'s agent loop competes with {competitor}'s.",
            },
            {
                "dimension": "Context window & codebase awareness",
                "notes": f"How well does {name} understand large codebases vs {competitor}?",
            },
            {
                "dimension": "Editor integration",
                "notes": f"VS Code / JetBrains / standalone — compare {name} and {competitor}.",
            },
            {
                "dimension": "Pricing & free tier",
                "notes": f"Is {name} cheaper or more generous than {competitor}?",
            },
            {
                "dimension": "Unique differentiator",
                "notes": f"What does {name} offer that {competitor} does not?",
            },
        ],
        "cta": f"Try {name} free → {{website}} | Compare full specs below.",
    }


def _slugify(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------
def write_json(path: Path, data: dict, dry_run: bool = False) -> None:
    try:
        p = safe_path(path)
        if dry_run:
            logger.info("[DRY-RUN] Would write JSON: %s", p)
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        logger.debug("Wrote JSON: %s", p)
    except (ValueError, OSError) as exc:
        logger.error("Failed to write JSON %s: %s", path, exc)


def append_csv_row(row: dict, dry_run: bool = False) -> None:
    try:
        p = safe_path(CSV_LOG)
        if dry_run:
            logger.info("[DRY-RUN] Would append CSV row for: %s", row.get("name"))
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        write_header = not p.exists()
        with p.open("a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_HEADERS, extrasaction="ignore")
            if write_header:
                writer.writeheader()
            writer.writerow(row)
    except (ValueError, OSError) as exc:
        logger.error("Failed to append CSV: %s", exc)


# ---------------------------------------------------------------------------
# Pipeline router
# ---------------------------------------------------------------------------
def route_to_pipeline(content: dict, launch: dict, dry_run: bool = False) -> str:
    slug = content["slug"]
    pipeline_file = PIPELINE_DIR / f"{launch['date']}_{slug}.json"
    payload = {
        "source": "ph_agentic_ide_tracker",
        "priority": "high" if launch["votes"] >= 100 else "normal",
        "tasks": ["publish_seo_post", "schedule_community_posts", "affiliate_link_check"],
        "content": content,
    }
    write_json(pipeline_file, payload, dry_run=dry_run)
    logger.info("Routed to pipeline: %s (dry_run=%s)", pipeline_file.name, dry_run)
    return str(pipeline_file)


# ---------------------------------------------------------------------------
# Core run logic
# ---------------------------------------------------------------------------
def run_tracker(dry_run: bool = False) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    logger.info("=== ph_agentic_ide_tracker START date=%s dry_run=%s ===", today, dry_run)

    bootstrap_dirs()
    seen_ids = load_seen_ids()

    try:
        logger.info("Fetching ProductHunt launches for %s …", today)
        launches = fetch_daily_launches(today)
        logger.info("Fetched %d launches total", len(launches))
    except RuntimeError as exc:
        logger.error("API error: %s", exc)
        sys.exit(1)
    except (urllib.error.URLError, OSError) as exc:
        logger.error("Network error fetching launches: %s", exc)
        sys.exit(1)

    relevant = [l for l in launches if is_relevant(l)]
    logger.info("%d relevant agentic/AI IDE launches found", len(relevant))

    new_count = 0
    for launch in relevant:
        lid = launch["id"]
        if lid in seen_ids:
            logger.debug("Already processed: %s (%s)", launch["name"], lid)
            continue

        logger.info("Processing new launch: %s — %s", launch["name"], launch["tagline"])

        # Affiliate check
        try:
            affiliate_info = check_affiliate_program(launch["website"])
        except Exception as exc:
            logger.warning("Affiliate check failed for %s: %s", launch["name"], exc)
            affiliate_info = {"found": False, "url": "", "note": f"error: {exc}"}

        if affiliate_info["found"]:
            logger.info("  Affiliate program found: %s", affiliate_info["url"])
        else:
            logger.info("  No affiliate program detected")

        # Generate comparison content
        content = generate_comparison_content(launch, affiliate_info)

        # Write content JSON
        content_file = CONTENT_DIR / f"{launch['date']}_{content['slug']}.json"
        write_json(content_file, content, dry_run=dry_run)

        # Route to pipeline
        pipeline_path = route_to_pipeline(content, launch, dry_run=dry_run)

        # Append to CSV log
        csv_row = {
            "date": launch["date"],
            "id": lid,
            "name": launch["name"],
            "tagline": launch["tagline"],
            "url": launch["url"],
            "votes": launch["votes"],
            "topics": "|".join(launch["topics"]),
            "website": launch["website"],
            "affiliate_found": affiliate_info["found"],
            "content_generated": str(content_file),
            "routed_to_pipeline": pipeline_path,
        }
        append_csv_row(csv_row, dry_run=dry_run)

        # Capture skill learnings
        try:
            capture_skill_from_result(
                {"launch": launch, "affiliate": affiliate_info, "content_slug": content["slug"]},
                task="ph_agentic_ide_launch_processing",
            )
        except Exception:
            pass

        seen_ids.add(lid)
        new_count += 1

    save_seen_ids(seen_ids, dry_run=dry_run)
    logger.info("=== ph_agentic_ide_tracker END new=%d ===", new_count)


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------
def print_status() -> None:
    bootstrap_dirs()
    seen_ids = load_seen_ids()
    print(f"Seen launches (all time): {len(seen_ids)}")

    csv_path = safe_path(CSV_LOG) if CSV_LOG.exists() else None
    if csv_path and csv_path.exists():
        try:
            with csv_path.open("r", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            today_rows = [r for r in rows if r.get("date") == today]
            aff_found = [r for r in rows if r.get("affiliate_found") == "True"]
            print(f"Total CSV entries: {len(rows)}")
            print(f"Launches today: {len(today_rows)}")
            print(f"Affiliate programs found (all time): {len(aff_found)}")
            pending = list(safe_path(PIPELINE_DIR).glob("*.json"))
            print(f"Pending pipeline items: {len(pending)}")
        except (OSError, csv.Error) as exc:
            print(f"Could not read CSV: {exc}")
    else:
        print("No CSV log found yet.")

    try:
        skills = recall_skills_for_task("ph_agentic_ide_launch_processing")
        if skills:
            print(f"Recalled skills: {skills}")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: ProductHunt Agentic IDE Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Fetch and process today's launches")
    group.add_argument("--status", action="store_true", help="Print tracker status and stats")
    group.add_argument("--dry-run", action="store_true", help="Run without writing any files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        if args.status:
            print_status()
        elif args.run:
            run_tracker(dry_run=False)
        elif args.dry_run:
            run_tracker(dry_run=True)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(0)
    except Exception as exc:
        logger.exception("Unhandled exception: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()