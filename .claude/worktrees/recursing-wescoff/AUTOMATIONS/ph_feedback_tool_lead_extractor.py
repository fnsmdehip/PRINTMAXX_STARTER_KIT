#!/usr/bin/env python3
"""
PRINTMAXX Automation: Product Hunt Feedback Tool Lead Extractor

Scrapes ProductBridge PH upvoters — product managers and founders who upvote
multi-platform feedback tools are warm buyers for automation services.
Extracts emails/LinkedIn profiles, enriches data, and pushes into cold
outbound pipeline. Monitors all future PH feedback/VOC tool launches
as a recurring lead source.

Usage:
    python ph_feedback_tool_lead_extractor.py --run
    python ph_feedback_tool_lead_extractor.py --status
    python ph_feedback_tool_lead_extractor.py --dry-run

Cron example (daily at 07:00):
    0 7 * * * PH_API_TOKEN=<token> /usr/bin/python3 /path/to/ph_feedback_tool_lead_extractor.py --run
"""

import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ── _common import (with fallback for standalone use) ─────────────────────────
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(*parts):
        """Return a Path inside PROJECT, raising ValueError if it would escape."""
        target = Path(PROJECT).joinpath(*parts).resolve()
        if not str(target).startswith(str(PROJECT.resolve())):
            raise ValueError(
                f"Path escape blocked: {target} is outside project root {PROJECT}"
            )
        return target

    def recall_skills_for_task(task_name):  # noqa: D103
        return {}

    def capture_skill_from_result(task_name, result):  # noqa: D103
        pass

# ── Canonical paths (all via safe_path) ──────────────────────────────────────
LOG_FILE   = safe_path("AUTOMATIONS", "logs",    "ph_feedback_tool_lead_extractor.log")
OUTPUT_DIR = safe_path("AUTOMATIONS", "outputs", "ph_leads")
STATE_FILE = safe_path("AUTOMATIONS", "state",   "ph_feedback_tool_lead_extractor.json")

# ── Logging (append to file + stdout) ────────────────────────────────────────
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ── Config constants ──────────────────────────────────────────────────────────
PH_GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"
PH_TOKEN_ENV   = "PH_API_TOKEN"

# Seed: known ProductBridge slug; also expand via keyword search
SEED_SLUGS = ["productbridge"]

# Keywords to discover future feedback/VOC tool launches
MONITOR_KEYWORDS = [
    "feedback aggregator",
    "multi-platform feedback",
    "voice of customer",
    "user feedback tool",
    "customer feedback platform",
    "product feedback",
    "feedback collector",
    "voc tool",
]

# Headline fragments that mark a warm buyer
WARM_BUYER_TITLES = [
    "product manager",
    "product owner",
    "founder",
    "co-founder",
    "cto",
    "cpo",
    "vp product",
    "head of product",
    "director of product",
    "entrepreneur",
    "startup",
    "growth",
    "customer success",
    "chief product",
    "chief executive",
]

MAX_UPVOTERS_PER_POST  = 500
RATE_LIMIT_DELAY       = 1.2   # seconds between GraphQL calls
MIN_VOTES_FOR_DISCOVERY = 50   # ignore low-signal posts from keyword search


# ── GraphQL queries ───────────────────────────────────────────────────────────

_Q_POST_BY_SLUG = """
query PostBySlug($slug: String!) {
  post(slug: $slug) {
    id
    name
    tagline
    slug
    url
    votesCount
    createdAt
    topics { edges { node { name } } }
  }
}
"""

_Q_POST_VOTERS = """
query PostVoters($postId: ID!, $cursor: String) {
  post(id: $postId) {
    votes(first: 50, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      edges {
        node {
          user {
            id
            name
            username
            headline
            twitterUsername
            websiteUrl
          }
        }
      }
    }
  }
}
"""

_Q_SEARCH_POSTS = """
query SearchPosts($query: String!, $cursor: String) {
  posts(query: $query, first: 20, after: $cursor, order: VOTES) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        name
        tagline
        slug
        url
        votesCount
        createdAt
      }
    }
  }
}
"""


# ── Low-level API helper ──────────────────────────────────────────────────────

def _get_token() -> str:
    token = os.environ.get(PH_TOKEN_ENV, "")
    if not token:
        log.warning(
            "%s not set — PH API calls will be rate-limited or rejected", PH_TOKEN_ENV
        )
    return token


def _graphql(query: str, variables: dict, token: str) -> dict:
    """POST a GraphQL request to Product Hunt and return the parsed JSON body."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(
        PH_GRAPHQL_URL, data=payload, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        log.error("HTTP %s from PH API: %s", exc.code, body[:500])
        raise
    except urllib.error.URLError as exc:
        log.error("URLError querying PH API: %s", exc.reason)
        raise


# ── PH data fetchers ──────────────────────────────────────────────────────────

def fetch_post_by_slug(slug: str, token: str):
    """Return PH post dict for slug, or None on failure."""
    try:
        result = _graphql(_Q_POST_BY_SLUG, {"slug": slug}, token)
        return result.get("data", {}).get("post")
    except Exception as exc:
        log.error("fetch_post_by_slug(%r) failed: %s", slug, exc)
        return None


def fetch_upvoters(post_id: str, token: str, max_count: int = MAX_UPVOTERS_PER_POST) -> list:
    """Page through PH votes and return a list of user dicts."""
    users = []
    cursor = None

    while len(users) < max_count:
        try:
            variables = {"postId": post_id, "cursor": cursor}
            result = _graphql(_Q_POST_VOTERS, variables, token)
            votes_node = (
                result.get("data", {}).get("post", {}).get("votes", {})
            )
            for edge in votes_node.get("edges", []):
                user = edge.get("node", {}).get("user")
                if user:
                    users.append(user)

            page_info = votes_node.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break
            cursor = page_info.get("endCursor")
            time.sleep(RATE_LIMIT_DELAY)

        except Exception as exc:
            log.error("fetch_upvoters(post_id=%s) page error: %s", post_id, exc)
            break

    return users


def search_posts_by_keyword(keyword: str, token: str) -> list:
    """Return up to 3 pages of PH posts matching keyword, sorted by votes."""
    posts = []
    cursor = None

    for _ in range(3):
        try:
            variables = {"query": keyword, "cursor": cursor}
            result = _graphql(_Q_SEARCH_POSTS, variables, token)
            posts_node = result.get("data", {}).get("posts", {})
            for edge in posts_node.get("edges", []):
                node = edge.get("node")
                if node:
                    posts.append(node)
            page_info = posts_node.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break
            cursor = page_info.get("endCursor")
            time.sleep(RATE_LIMIT_DELAY)

        except Exception as exc:
            log.error("search_posts_by_keyword(%r) error: %s", keyword, exc)
            break

    return posts


# ── Enrichment ────────────────────────────────────────────────────────────────

def is_warm_buyer(user: dict) -> bool:
    """True when the user's headline matches a PM/founder/exec title."""
    headline = (user.get("headline") or "").lower()
    return any(title in headline for title in WARM_BUYER_TITLES)


def infer_linkedin(user: dict) -> str:
    """
    Return a LinkedIn URL if the user's websiteUrl points to linkedin.com;
    otherwise return a Google search URL for manual rep verification.
    """
    website = user.get("websiteUrl") or ""
    if "linkedin.com" in website:
        return website
    name     = urllib.parse.quote_plus(user.get("name") or "")
    username = urllib.parse.quote_plus(user.get("username") or "")
    return (
        f"https://www.google.com/search?q=site:linkedin.com+{name}+{username}"
    )


def infer_email_hint(user: dict) -> str:
    """
    PH does not expose emails.  Return an enrichment hint based on websiteUrl
    domain so reps / Apollo / Clay can complete the lookup downstream.
    """
    website = user.get("websiteUrl") or ""
    if website and "linkedin.com" not in website:
        try:
            domain = urllib.parse.urlparse(website).netloc.lstrip("www.")
            if domain:
                return f"[enrich:@{domain}]"
        except Exception:
            pass
    return ""


def enrich_user(user: dict, source_post: dict) -> dict:
    """Combine PH user fields with inferred enrichment columns."""
    return {
        "ph_user_id":    user.get("id", ""),
        "name":          user.get("name", ""),
        "username":      user.get("username", ""),
        "headline":      user.get("headline", ""),
        "twitter":       user.get("twitterUsername", ""),
        "website":       user.get("websiteUrl", ""),
        "ph_profile":    f"https://www.producthunt.com/@{user.get('username', '')}",
        "linkedin_hint": infer_linkedin(user),
        "email_hint":    infer_email_hint(user),
        "is_warm_buyer": is_warm_buyer(user),
        "source_post":   source_post.get("name", ""),
        "source_slug":   source_post.get("slug", ""),
        "source_url":    source_post.get("url", ""),
        "post_votes":    source_post.get("votesCount", 0),
        "scraped_at":    datetime.now(timezone.utc).isoformat(),
    }


# ── Output writers ────────────────────────────────────────────────────────────

_CSV_FIELDS = [
    "ph_user_id", "name", "username", "headline", "twitter", "website",
    "ph_profile", "linkedin_hint", "email_hint", "is_warm_buyer",
    "source_post", "source_slug", "source_url", "post_votes", "scraped_at",
]


def write_leads(leads: list, run_tag: str, dry_run: bool = False) -> Path:
    """Persist enriched leads to CSV and JSON; return the CSV path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_path  = safe_path(OUTPUT_DIR, f"leads_{run_tag}.csv")
    json_path = safe_path(OUTPUT_DIR, f"leads_{run_tag}.json")

    if dry_run:
        log.info("[DRY-RUN] Would write %d leads → %s", len(leads), csv_path)
        return csv_path

    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(leads)
        log.info("Wrote %d leads → %s", len(leads), csv_path)
    except Exception as exc:
        log.error("Failed to write CSV: %s", exc)
        raise

    try:
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(leads, fh, indent=2, ensure_ascii=False)
        log.info("Wrote %d leads → %s", len(leads), json_path)
    except Exception as exc:
        log.error("Failed to write JSON: %s", exc)

    return csv_path


# ── State persistence ─────────────────────────────────────────────────────────

def load_state() -> dict:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:
            log.warning("Could not read state file (%s) — starting fresh", exc)
    return {"processed_post_ids": [], "monitored_slugs": [], "runs": []}


def save_state(state: dict) -> None:
    path = safe_path(STATE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
        log.info("State saved → %s", path)
    except Exception as exc:
        log.error("Failed to save state: %s", exc)


# ── Pipeline stages ───────────────────────────────────────────────────────────

def discover_posts(token: str, state: dict) -> list:
    """
    Build the list of PH posts to process this run:
      1. Seed slugs (ProductBridge + any manually tracked slugs).
      2. Keyword discovery for new feedback/VOC launches.
    Already-processed post IDs are skipped.
    """
    posts = []
    seen_ids = set(state.get("processed_post_ids", []))

    # 1. Seed + previously monitored slugs
    all_slugs = list(dict.fromkeys(SEED_SLUGS + state.get("monitored_slugs", [])))
    for slug in all_slugs:
        post = fetch_post_by_slug(slug, token)
        if post and post["id"] not in seen_ids:
            posts.append(post)
            log.info("Seed post found: %s  (%s votes)", post["name"], post["votesCount"])
        time.sleep(RATE_LIMIT_DELAY)

    # 2. Keyword-based discovery
    discovered_ids = {p["id"] for p in posts}
    for keyword in MONITOR_KEYWORDS:
        results = search_posts_by_keyword(keyword, token)
        for post in results:
            pid = post.get("id")
            if (
                pid
                and pid not in seen_ids
                and pid not in discovered_ids
                and post.get("votesCount", 0) >= MIN_VOTES_FOR_DISCOVERY
            ):
                posts.append(post)
                discovered_ids.add(pid)
                log.info(
                    "Discovered: %s  (%s votes)  [keyword=%r]",
                    post["name"], post["votesCount"], keyword,
                )
        time.sleep(RATE_LIMIT_DELAY)

    log.info("Posts queued for processing: %d", len(posts))
    return posts


def process_posts(posts: list, token: str, dry_run: bool) -> list:
    """Fetch upvoters for every post, enrich each user, return combined lead list."""
    all_leads = []
    seen_user_ids: set = set()

    for post in posts:
        post_id   = post["id"]
        post_name = post.get("name", post_id)
        log.info("Fetching upvoters for: %s  (id=%s)", post_name, post_id)

        if dry_run:
            log.info("[DRY-RUN] Skipping API call for post %s", post_name)
            continue

        try:
            users = fetch_upvoters(post_id, token)
        except Exception as exc:
            log.error("Skipping post %s due to error: %s", post_name, exc)
            continue

        log.info("  %d upvoters fetched for %s", len(users), post_name)
        batch_warm = 0

        for user in users:
            uid = user.get("id")
            if not uid or uid in seen_user_ids:
                continue
            seen_user_ids.add(uid)
            lead = enrich_user(user, post)
            all_leads.append(lead)
            if lead["is_warm_buyer"]:
                batch_warm += 1

        log.info("  %d warm buyers in batch for %s", batch_warm, post_name)
        time.sleep(RATE_LIMIT_DELAY)

    return all_leads


def push_to_outbound_pipeline(csv_path: Path, dry_run: bool) -> None:
    """
    Optional hook: invoke AUTOMATIONS/bin/push_to_pipeline.sh with the CSV path
    to forward leads into Apollo, Instantly, or any downstream outbound tool.
    Silently skips if the script does not exist.
    """
    pipeline_cli = safe_path("AUTOMATIONS", "bin", "push_to_pipeline.sh")
    if not pipeline_cli.exists():
        log.info(
            "push_to_pipeline.sh not found — leads saved locally, skipping outbound push"
        )
        return

    if dry_run:
        log.info("[DRY-RUN] Would push %s to outbound pipeline via %s", csv_path, pipeline_cli)
        return

    try:
        result = subprocess.run(
            [str(pipeline_cli), str(csv_path)],
            capture_output=True,
            text=True,
            timeout=120,
            check=True,
        )
        log.info("Pipeline push stdout: %s", result.stdout.strip())
    except subprocess.CalledProcessError as exc:
        log.error(
            "Pipeline push exited %s — stderr: %s", exc.returncode, exc.stderr.strip()
        )
    except subprocess.TimeoutExpired:
        log.error("Pipeline push timed out after 120 s")
    except Exception as exc:
        log.error("Unexpected error during pipeline push: %s", exc)


# ── CLI commands ──────────────────────────────────────────────────────────────

def cmd_run(dry_run: bool = False) -> int:
    """Full extraction run: discover → scrape → enrich → write → push."""
    log.info(
        "=== ph_feedback_tool_lead_extractor START  dry_run=%s ===", dry_run
    )
    recall_skills_for_task("ph_lead_extraction")

    token = _get_token()
    state = load_state()
    run_tag = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    try:
        posts = discover_posts(token, state)
        if not posts:
            log.info("No new posts to process — exiting cleanly.")
            return 0

        leads = process_posts(posts, token, dry_run)
        warm_count = sum(1 for ld in leads if ld.get("is_warm_buyer"))
        log.info(
            "Run summary: %d posts, %d unique leads, %d warm buyers",
            len(posts), len(leads), warm_count,
        )

        csv_path = write_leads(leads, run_tag, dry_run)
        push_to_outbound_pipeline(csv_path, dry_run)

        if not dry_run:
            # Persist processed post IDs so future runs skip them
            seen = set(state.get("processed_post_ids", []))
            for post in posts:
                pid = post.get("id")
                if pid:
                    seen.add(pid)
            state["processed_post_ids"] = list(seen)

            state.setdefault("runs", [])
            state["runs"].append({
                "run_tag":     run_tag,
                "posts":       len(posts),
                "leads":       len(leads),
                "warm_buyers": warm_count,
                "timestamp":   datetime.now(timezone.utc).isoformat(),
            })
            state["runs"] = state["runs"][-100:]  # cap history
            save_state(state)

        capture_skill_from_result(
            "ph_lead_extraction",
            {"posts": len(posts), "leads": len(leads), "warm_buyers": warm_count},
        )

        log.info("=== ph_feedback_tool_lead_extractor DONE ===")
        return 0

    except Exception as exc:
        log.exception("Unhandled error in cmd_run: %s", exc)
        return 1


def cmd_status() -> int:
    """Print run history from the state file to stdout."""
    state = load_state()
    runs  = state.get("runs", [])

    if not runs:
        print("No runs recorded yet.")
        return 0

    header = f"{'Timestamp':<28}  {'Posts':>6}  {'Leads':>7}  {'Warm':>6}"
    print(f"\n{header}")
    print("-" * len(header))
    for run in runs[-25:]:
        print(
            f"{run.get('timestamp', '?'):<28}  "
            f"{run.get('posts', 0):>6}  "
            f"{run.get('leads', 0):>7}  "
            f"{run.get('warm_buyers', 0):>6}"
        )
    print("-" * len(header))
    print(
        f"{'TOTAL':<28}  "
        f"{sum(r.get('posts', 0)       for r in runs):>6}  "
        f"{sum(r.get('leads', 0)       for r in runs):>7}  "
        f"{sum(r.get('warm_buyers', 0) for r in runs):>6}"
    )
    print(f"\nProcessed post IDs : {len(state.get('processed_post_ids', []))}")
    print(f"Output directory   : {OUTPUT_DIR}")
    print(f"Log file           : {LOG_FILE}")
    print(f"State file         : {STATE_FILE}")
    return 0


# ── Argument parsing ──────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "PRINTMAXX — Product Hunt feedback-tool lead extractor.\n"
            "Scrapes upvoters of ProductBridge and similar VOC tools; "
            "enriches and pushes warm PM/founder leads to outbound pipeline."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full scrape-enrich-write-push pipeline.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Display run history and totals from state file.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate the run: discover posts but skip API scraping and file writes.",
    )
    return parser.parse_args()


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    args = _parse_args()
    if args.status:
        sys.exit(cmd_status())
    elif args.run:
        sys.exit(cmd_run(dry_run=False))
    elif args.dry_run:
        sys.exit(cmd_run(dry_run=True))


if __name__ == "__main__":
    main()