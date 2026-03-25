#!/usr/bin/env python3
"""
PRINTMAXX Automation: Bootstrapped Founder Story Scraper

Scrapes r/indiehackers and Hacker News for posts matching 'shipped without
funding', 'bootstrapped and live', and young/18-year-old founder stories.
Extracts founder story, product name, and launch date. Routes each story to
engagement_bait_converter.py to generate 3 viral posts (narrative hook,
contrarian angle, founder-age-shock format). Flags acquisition targets when
traction signals exceed threshold.

Usage:
    python bootstrapped_founder_story_scraper.py --run
    python bootstrapped_founder_story_scraper.py --status
    python bootstrapped_founder_story_scraper.py --dry-run
"""

import argparse
import csv
import json
import logging
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root (two levels up from this file)
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent


def safe_path(path):
    """Resolve *path* and assert it lives inside PROJECT. Return resolved Path."""
    resolved = Path(path).resolve()
    try:
        resolved.relative_to(PROJECT)
    except ValueError:
        raise ValueError(
            f"Security violation: {resolved} is outside PROJECT root {PROJECT}"
        )
    return resolved


# ---------------------------------------------------------------------------
# Optional _common helpers — fall back to no-ops if the module is absent
# ---------------------------------------------------------------------------
try:
    from _common import (  # type: ignore
        PROJECT as _COMMON_PROJECT,
        safe_path as _common_safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
    # Prefer _common's PROJECT / safe_path if the module is present
    PROJECT = _COMMON_PROJECT
    safe_path = _common_safe_path  # noqa: F811
except ImportError:

    def recall_skills_for_task(task):  # type: ignore
        return []

    def capture_skill_from_result(result, skill_name):  # type: ignore
        pass


# ---------------------------------------------------------------------------
# Paths (all via safe_path to enforce PROJECT boundary)
# ---------------------------------------------------------------------------
_AUTOMATIONS = PROJECT / "AUTOMATIONS"
LOG_FILE = safe_path(_AUTOMATIONS / "logs" / "bootstrapped_founder_story_scraper.log")
OUTPUT_DIR = safe_path(_AUTOMATIONS / "output")
STATUS_FILE = safe_path(_AUTOMATIONS / "status" / "bootstrapped_founder_story_scraper.json")
STORIES_CSV = safe_path(OUTPUT_DIR / "founder_stories.csv")
ACQUISITION_JSON = safe_path(OUTPUT_DIR / "acquisition_targets.json")
ENGAGEMENT_SCRIPT = safe_path(_AUTOMATIONS / "engagement_bait_converter.py")

# ---------------------------------------------------------------------------
# Scraper configuration
# ---------------------------------------------------------------------------
REDDIT_SUBREDDITS = ["indiehackers", "startups", "entrepreneur"]

REDDIT_QUERIES = [
    "shipped without funding",
    "bootstrapped and live",
    "no funding shipped",
    "built without investors",
    "zero funding launched",
    "18 no funding shipped",
    "young founder shipped",
]

HN_QUERIES = [
    "shipped without funding",
    "bootstrapped launched",
    "18 year old founded",
    "young founder shipped",
    "no investors live",
    "bootstrapped side project live",
]

TRACTION_KEYWORDS = [
    "revenue", "mrr", "arr", "paying customers", "users", "signups",
    "waitlist", "growth", "profit", "sustainable", "cash flow",
    "subscribers", "traction", "product market fit", "pmf", "customers",
    "monthly recurring", "annual recurring",
]
TRACTION_THRESHOLD = 2  # minimum keyword hits to flag as acquisition target

AGE_KEYWORDS = [
    "18", "19", "20", "teenager", "young founder",
    "college dropout", "high school", "17 year", "18 year",
    "19 year", "20 year",
]

USER_AGENT = (
    "PRINTMAXX-BootstrappedFounderScraper/1.0 "
    "(founder story aggregator for PRINTMAXX automation; "
    "contact via github)"
)

CSV_FIELDS = [
    "source", "title", "founder_story", "product_name",
    "launch_date", "author", "score", "url",
    "traction_flagged", "age_shock",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging():
    """Configure root logger to append to LOG_FILE and echo to stdout."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    fmt = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def fetch_json(url, retries=3, backoff=2.0):
    """GET *url*, parse JSON, return dict/list or None on failure."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                return json.loads(raw)
        except urllib.error.HTTPError as exc:
            logging.warning("HTTP %s on attempt %d/%d: %s", exc.code, attempt, retries, url)
        except urllib.error.URLError as exc:
            logging.warning("URL error on attempt %d/%d (%s): %s", attempt, retries, url, exc.reason)
        except json.JSONDecodeError as exc:
            logging.error("JSON decode error for %s: %s", url, exc)
            return None
        if attempt < retries:
            time.sleep(backoff * attempt)
    return None


# ---------------------------------------------------------------------------
# Text analysis helpers
# ---------------------------------------------------------------------------

_PRODUCT_PATTERNS = [
    re.compile(
        r"(?:i|we)\s+(?:built|launched|shipped|created|made|released)\s+"
        r"([A-Z][A-Za-z0-9][A-Za-z0-9\s\-]{0,28})",
        re.IGNORECASE,
    ),
    re.compile(
        r"([A-Z][A-Za-z0-9\-]{2,20})\s+(?:is live|is now live|launched|shipped|went live)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:my|our)\s+(?:product|app|tool|saas|startup|side project)\s+"
        r"([A-Z][A-Za-z0-9\s\-]{1,20})",
        re.IGNORECASE,
    ),
    re.compile(r"introducing\s+([A-Z][A-Za-z0-9\s\-]{1,20})", re.IGNORECASE),
    re.compile(r"show\s+hn\s*:\s*([A-Za-z0-9][A-Za-z0-9\s\-]{1,30})", re.IGNORECASE),
]


def extract_product_name(text):
    """Return the first plausible product name found in *text*, or empty string."""
    for pat in _PRODUCT_PATTERNS:
        m = pat.search(text)
        if m:
            name = m.group(1).strip().rstrip(".,!?;:")
            if len(name) >= 2:
                return name
    return ""


def check_traction(text):
    """Return True when *text* contains >= TRACTION_THRESHOLD traction signals."""
    lower = text.lower()
    hits = sum(1 for kw in TRACTION_KEYWORDS if kw in lower)
    return hits >= TRACTION_THRESHOLD


def check_age_shock(text):
    """Return True when *text* suggests a notably young founder."""
    lower = text.lower()
    return any(kw in lower for kw in AGE_KEYWORDS)


# ---------------------------------------------------------------------------
# Scrapers
# ---------------------------------------------------------------------------

def scrape_reddit(subreddit, query, limit=25, dry_run=False):
    """Return list of story dicts from a Reddit subreddit search."""
    if dry_run:
        logging.info("[DRY-RUN] Would scrape r/%s for: %s", subreddit, query)
        return []

    url = (
        "https://www.reddit.com/r/{}/search.json"
        "?q={}&restrict_sr=1&sort=new&limit={}&t=month".format(
            subreddit,
            urllib.parse.quote(query),
            limit,
        )
    )
    data = fetch_json(url)
    if not data:
        logging.warning("No data from Reddit r/%s '%s'", subreddit, query)
        return []

    stories = []
    try:
        children = data["data"]["children"]
    except (KeyError, TypeError) as exc:
        logging.error("Unexpected Reddit response structure: %s", exc)
        return []

    for child in children:
        try:
            post = child["data"]
            title = post.get("title", "")
            selftext = post.get("selftext", "") or ""
            combined = title + " " + selftext
            created = post.get("created_utc") or 0
            permalink = post.get("permalink", "")
            stories.append({
                "source": f"reddit/r/{subreddit}",
                "title": title,
                "founder_story": selftext[:1200],
                "product_name": extract_product_name(combined),
                "launch_date": (
                    datetime.utcfromtimestamp(created).strftime("%Y-%m-%d")
                    if created else ""
                ),
                "author": post.get("author", ""),
                "score": post.get("score", 0),
                "url": f"https://www.reddit.com{permalink}",
                "traction_flagged": check_traction(combined),
                "age_shock": check_age_shock(combined),
            })
        except (KeyError, TypeError, OSError) as exc:
            logging.warning("Skipping Reddit post due to parse error: %s", exc)

    logging.info("Reddit r/%s '%s': %d posts", subreddit, query, len(stories))
    return stories


def scrape_hn(query, limit=25, dry_run=False):
    """Return list of story dicts from HN via the Algolia search API."""
    if dry_run:
        logging.info("[DRY-RUN] Would scrape HN for: %s", query)
        return []

    url = (
        "https://hn.algolia.com/api/v1/search"
        "?query={}&tags=story&hitsPerPage={}".format(
            urllib.parse.quote(query),
            limit,
        )
    )
    data = fetch_json(url)
    if not data:
        logging.warning("No data from HN query: %s", query)
        return []

    stories = []
    for hit in data.get("hits", []):
        try:
            title = hit.get("title", "") or ""
            story_text = hit.get("story_text", "") or ""
            combined = title + " " + story_text
            created_at = hit.get("created_at", "") or ""
            object_id = hit.get("objectID", "")
            stories.append({
                "source": "hackernews",
                "title": title,
                "founder_story": story_text[:1200],
                "product_name": extract_product_name(combined),
                "launch_date": created_at[:10] if created_at else "",
                "author": hit.get("author", ""),
                "score": hit.get("points", 0) or 0,
                "url": f"https://news.ycombinator.com/item?id={object_id}",
                "traction_flagged": check_traction(combined),
                "age_shock": check_age_shock(combined),
            })
        except (KeyError, TypeError, OSError) as exc:
            logging.warning("Skipping HN hit due to parse error: %s", exc)

    logging.info("HN '%s': %d stories", query, len(stories))
    return stories


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(stories):
    """Remove duplicate stories by URL. Preserve insertion order."""
    seen = set()
    unique = []
    for story in stories:
        url = story.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(story)
        elif not url:
            unique.append(story)
    return unique


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def save_stories_csv(stories, dry_run=False):
    """Write *stories* to STORIES_CSV."""
    if not stories:
        logging.info("No stories to write to CSV.")
        return
    if dry_run:
        logging.info("[DRY-RUN] Would write %d stories to %s", len(stories), STORIES_CSV)
        return
    try:
        STORIES_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path(STORIES_CSV), "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(stories)
        logging.info("Wrote %d stories → %s", len(stories), STORIES_CSV)
    except OSError as exc:
        logging.error("Failed to write stories CSV: %s", exc)


def save_acquisition_targets(stories, dry_run=False):
    """Write traction-flagged stories to ACQUISITION_JSON."""
    targets = [s for s in stories if s.get("traction_flagged")]
    if not targets:
        logging.info("No acquisition targets identified.")
        return
    if dry_run:
        logging.info(
            "[DRY-RUN] Would write %d acquisition targets to %s",
            len(targets), ACQUISITION_JSON,
        )
        return
    try:
        ACQUISITION_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path(ACQUISITION_JSON), "w", encoding="utf-8") as fh:
            json.dump(targets, fh, indent=2, ensure_ascii=False)
        logging.info("Flagged %d acquisition targets → %s", len(targets), ACQUISITION_JSON)
    except OSError as exc:
        logging.error("Failed to write acquisition targets JSON: %s", exc)


def write_status(status, dry_run=False):
    """Persist run metadata to STATUS_FILE."""
    if dry_run:
        logging.info("[DRY-RUN] Would write status to %s", STATUS_FILE)
        return
    try:
        STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path(STATUS_FILE), "w", encoding="utf-8") as fh:
            json.dump(status, fh, indent=2)
    except OSError as exc:
        logging.error("Failed to write status file: %s", exc)


# ---------------------------------------------------------------------------
# Engagement bait routing
# ---------------------------------------------------------------------------

def route_to_engagement_bait(stories, dry_run=False):
    """
    Pass each story as JSON via stdin to engagement_bait_converter.py.
    The converter is expected to produce 3 viral posts per story:
      1. narrative hook
      2. contrarian angle
      3. founder-age-shock format
    """
    if not ENGAGEMENT_SCRIPT.exists():
        logging.warning(
            "engagement_bait_converter.py not found at %s — skipping viral post generation.",
            ENGAGEMENT_SCRIPT,
        )
        return

    for story in stories:
        if not story.get("title") and not story.get("founder_story"):
            continue

        label = (story.get("title") or "untitled")[:70]

        if dry_run:
            logging.info("[DRY-RUN] Would route to engagement_bait_converter: %s", label)
            continue

        payload = json.dumps(story, ensure_ascii=False)
        try:
            result = subprocess.run(
                [sys.executable, str(ENGAGEMENT_SCRIPT)],
                input=payload,
                capture_output=True,
                text=True,
                timeout=90,
            )
            if result.returncode == 0:
                logging.info("Engagement bait generated: %s", label)
            else:
                logging.warning(
                    "engagement_bait_converter exited %d for '%s': %s",
                    result.returncode,
                    label,
                    result.stderr[:300],
                )
        except subprocess.TimeoutExpired:
            logging.error("engagement_bait_converter timed out for: %s", label)
        except OSError as exc:
            logging.error("Could not run engagement_bait_converter: %s", exc)


# ---------------------------------------------------------------------------
# Core run
# ---------------------------------------------------------------------------

def run_scraper(dry_run=False):
    """Collect stories, save outputs, and route to engagement bait converter."""
    logging.info("=== PRINTMAXX bootstrapped_founder_story_scraper START ===")
    recall_skills_for_task("scrape founder stories for PRINTMAXX viral post automation")

    all_stories = []

    for subreddit in REDDIT_SUBREDDITS:
        for query in REDDIT_QUERIES:
            all_stories.extend(scrape_reddit(subreddit, query, dry_run=dry_run))
            time.sleep(1.5)  # stay polite with Reddit rate limits

    for query in HN_QUERIES:
        all_stories.extend(scrape_hn(query, dry_run=dry_run))
        time.sleep(1.0)

    unique = deduplicate(all_stories)
    logging.info("Total unique stories: %d (from %d raw)", len(unique), len(all_stories))

    save_stories_csv(unique, dry_run=dry_run)
    save_acquisition_targets(unique, dry_run=dry_run)
    route_to_engagement_bait(unique, dry_run=dry_run)

    acquisition_count = sum(1 for s in unique if s.get("traction_flagged"))
    age_shock_count = sum(1 for s in unique if s.get("age_shock"))

    capture_skill_from_result(
        {
            "stories": len(unique),
            "acquisition_targets": acquisition_count,
            "age_shock_posts": age_shock_count,
        },
        "bootstrapped_founder_story_scraper",
    )

    status = {
        "last_run": datetime.utcnow().isoformat() + "Z",
        "stories_found": len(unique),
        "acquisition_targets": acquisition_count,
        "age_shock_posts": age_shock_count,
        "dry_run": dry_run,
    }
    write_status(status, dry_run=dry_run)

    logging.info(
        "=== DONE — %d stories | %d acquisition targets | %d age-shock posts ===",
        len(unique),
        acquisition_count,
        age_shock_count,
    )


# ---------------------------------------------------------------------------
# --status command
# ---------------------------------------------------------------------------

def show_status():
    """Print last run status from STATUS_FILE."""
    try:
        path = safe_path(STATUS_FILE)
        if not path.exists():
            print("No status file found. Run with --run first.")
            return
        with open(path, "r", encoding="utf-8") as fh:
            status = json.load(fh)
        print(json.dumps(status, indent=2))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error reading status: {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: Bootstrapped Founder Story Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Scrape sources and generate engagement bait posts",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Display last run status",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate a full run without writing files or calling subprocesses",
    )
    args = parser.parse_args()

    setup_logging()

    try:
        if args.status:
            show_status()
        elif args.run:
            run_scraper(dry_run=False)
        elif args.dry_run:
            run_scraper(dry_run=True)
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting cleanly.")
        sys.exit(0)
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Unhandled exception: %s", exc)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()