#!/usr/bin/env python3
"""
PRINTMAXX Automation: Young Founder Acquisition Scanner

Scrapes r/SideProject, r/indiehackers, and Hacker News for posts by young/solo
founders showing traction signals (revenue mentions, user counts, growth stats)
with low engagement/votes. Scores by acquisition potential and flags undervalued
assets for outreach.

Acquisition scoring: estimated_valuation / engagement * traction_multiplier
  - MRR * 36  (~3x ARR, mid of 2-4x annual multiple)
  - ARR * 3   (fallback)
  - users * 10 (rough $10/user estimate fallback)

Part of the PRINTMAXX [ACQUISITION] pipeline — method: unacknowledged young founder.

Usage:
  python young_founder_acquisition_scanner.py --run
  python young_founder_acquisition_scanner.py --dry-run
  python young_founder_acquisition_scanner.py --status
"""

import argparse
import csv
import json
import logging
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import from _common, fall back to local definitions
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path):
        """Validate that path resolves within PROJECT; raise ValueError otherwise."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(f"Path '{resolved}' is outside PROJECT root '{PROJECT}'")
        return resolved

    def recall_skills_for_task(task_name):  # noqa: D401
        return {}

    def capture_skill_from_result(result, task_name):
        pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_NAME = "young_founder_acquisition_scanner"

LOG_DIR    = PROJECT / "AUTOMATIONS" / "logs"
LOG_FILE   = LOG_DIR / f"{SCRIPT_NAME}.log"
OUTPUT_DIR = PROJECT / "AUTOMATIONS" / "outputs"
OUTPUT_CSV  = OUTPUT_DIR / f"{SCRIPT_NAME}_results.csv"
OUTPUT_JSON = OUTPUT_DIR / f"{SCRIPT_NAME}_results.json"

REDDIT_UA        = "PRINTMAXX-AcquisitionScanner/1.0 (acquisition research)"
HN_SEARCH_BASE   = "https://hn.algolia.com/api/v1/search_by_date"

REDDIT_SUBREDDITS = ["SideProject", "indiehackers"]
HN_QUERIES = [
    "MRR revenue solo founder",
    "launched side project users growth",
    "bootstrapped paying customers",
]

# Traction signal patterns
_MRR_RE = re.compile(
    r"\$\s*([\d,]+(?:\.\d+)?)\s*(k|K)?\s*(?:MRR|mrr|per\s+month|/mo|monthly\s+revenue)",
    re.IGNORECASE,
)
_ARR_RE = re.compile(
    r"\$\s*([\d,]+(?:\.\d+)?)\s*(k|K)?\s*(?:ARR|arr|annual(?:\s+revenue)?|annually)",
    re.IGNORECASE,
)
_USERS_RE = re.compile(
    r"([\d,]+(?:\.\d+)?)\s*(k|K)?\s*"
    r"(?:users|customers|subscribers|signups|sign[\s-]?ups|downloads|installs)",
    re.IGNORECASE,
)
_GROWTH_RE = re.compile(
    r"([\d]+(?:\.\d+)?)\s*%\s*(?:growth|increase|MoM|WoW|YoY)",
    re.IGNORECASE,
)
_REVENUE_KW = re.compile(
    r"\b(?:revenue|MRR|ARR|paying|profit|income|earning|sales|customers?)\b",
    re.IGNORECASE,
)
_FOUNDER_KW = re.compile(
    r"\b(?:solo\s+founder|indie\s+hacker|side\s+project|bootstrapped|self[\s-]?funded|"
    r"built\s+(?:by\s+)?myself|I\s+(?:built|made|created|launched)|single\s+founder)\b",
    re.IGNORECASE,
)
_YOUNG_KW = re.compile(
    r"\b(?:first\s+(?:startup|company|product)|just\s+launched|recently\s+launched|"
    r"been\s+building|couple\s+(?:of\s+)?months|few\s+months|year\s+(?:old|in)|"
    r"early\s+stage|pre[\s-]?seed|v1|MVP|beta|day\s+\d+)\b",
    re.IGNORECASE,
)

CSV_FIELDS = [
    "source", "post_id", "title", "url", "author", "created_utc",
    "upvotes", "comments", "mrr_usd", "arr_usd", "users_count",
    "traction_signals", "acquisition_score", "text_snippet",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging():
    """Configure append-mode file logging + stdout; return logger."""
    handlers = [logging.StreamHandler(sys.stdout)]
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_path = safe_path(LOG_FILE)
        handlers.append(logging.FileHandler(log_path, mode="a", encoding="utf-8"))
    except (ValueError, OSError) as exc:
        print(f"[WARNING] Could not open log file: {exc}", file=sys.stderr)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        handlers=handlers,
    )
    return logging.getLogger(SCRIPT_NAME)


logger = setup_logging()

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_json(url, retries=3, backoff=2.0):
    """GET url, return parsed JSON dict/list, or None on failure."""
    headers = {"User-Agent": REDDIT_UA, "Accept": "application/json"}
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as exc:
            logger.warning("HTTP %s fetching %s (attempt %d/%d)", exc.code, url, attempt, retries)
            if exc.code in (429, 503):
                time.sleep(backoff * attempt)
            else:
                break
        except urllib.error.URLError as exc:
            logger.warning("URLError on %s: %s (attempt %d/%d)", url, exc.reason, attempt, retries)
            time.sleep(backoff * attempt)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Parse/IO error on %s: %s", url, exc)
            break
    return None

# ---------------------------------------------------------------------------
# Traction extraction
# ---------------------------------------------------------------------------

def _num(raw, has_k):
    """Parse raw string to float, multiply by 1000 if has_k is truthy."""
    try:
        val = float(raw.replace(",", ""))
        return val * 1000 if has_k else val
    except (ValueError, AttributeError):
        return 0.0


def extract_mrr(text):
    return max((_num(m.group(1), m.group(2)) for m in _MRR_RE.finditer(text)), default=0.0)


def extract_arr(text):
    return max((_num(m.group(1), m.group(2)) for m in _ARR_RE.finditer(text)), default=0.0)


def extract_users(text):
    return max((_num(m.group(1), m.group(2)) for m in _USERS_RE.finditer(text)), default=0.0)


def count_traction_signals(text):
    """Return integer signal count across five distinct signal categories."""
    return sum([
        bool(_REVENUE_KW.search(text)),
        bool(_FOUNDER_KW.search(text)),
        bool(_YOUNG_KW.search(text)),
        bool(_GROWTH_RE.search(text)),
        bool(_USERS_RE.search(text)),
    ])

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_post(mrr, arr, users, engagement, traction_signals):
    """
    Acquisition opportunity score = (valuation_estimate / engagement) * traction_signals.

    A high score means high implied value relative to community attention —
    indicating a potentially undervalued, under-the-radar asset.
    """
    if mrr > 0:
        valuation = mrr * 36          # ~3x ARR (mid 2-4x annual multiple)
    elif arr > 0:
        valuation = arr * 3
    elif users > 0:
        valuation = users * 10        # rough $10/user
    else:
        valuation = 0.0

    return round((valuation / max(engagement, 1)) * max(traction_signals, 1), 4)

# ---------------------------------------------------------------------------
# Reddit scraping
# ---------------------------------------------------------------------------

def scrape_reddit(subreddit, limit=100, dry_run=False):
    """Fetch recent posts from a subreddit; return list of candidate dicts."""
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}&raw_json=1"
    logger.info("Reddit r/%s — fetching up to %d posts", subreddit, limit)

    if dry_run:
        logger.info("[DRY-RUN] Would fetch: %s", url)
        return []

    data = fetch_json(url)
    if not data:
        logger.error("No data returned for r/%s", subreddit)
        return []

    candidates = []
    try:
        posts = data.get("data", {}).get("children", [])
    except AttributeError:
        logger.error("Unexpected Reddit JSON structure for r/%s", subreddit)
        return []

    for post in posts:
        try:
            p = post.get("data", {})
            title    = p.get("title", "")
            selftext = p.get("selftext", "")
            combined = f"{title}\n{selftext}"

            traction = count_traction_signals(combined)
            if traction < 2:
                continue

            mrr   = extract_mrr(combined)
            arr   = extract_arr(combined)
            users = extract_users(combined)
            engagement = max(p.get("score", 1), 1) + p.get("num_comments", 0)

            candidates.append({
                "source":            f"reddit/r/{subreddit}",
                "post_id":           p.get("id", ""),
                "title":             title[:200],
                "url":               f"https://www.reddit.com{p.get('permalink', '')}",
                "author":            p.get("author", ""),
                "created_utc":       datetime.fromtimestamp(
                                         p.get("created_utc", 0), tz=timezone.utc
                                     ).isoformat(),
                "upvotes":           p.get("score", 0),
                "comments":          p.get("num_comments", 0),
                "mrr_usd":           mrr,
                "arr_usd":           arr,
                "users_count":       users,
                "traction_signals":  traction,
                "acquisition_score": score_post(mrr, arr, users, engagement, traction),
                "text_snippet":      combined[:300].replace("\n", " "),
            })
        except Exception as exc:
            logger.warning("Error processing Reddit post: %s", exc)

    logger.info("r/%s: %d acquisition candidates found", subreddit, len(candidates))
    return candidates

# ---------------------------------------------------------------------------
# Hacker News scraping (Algolia HN Search API)
# ---------------------------------------------------------------------------

def scrape_hn(query, pages=3, dry_run=False):
    """Fetch HN stories matching query via Algolia; return list of candidate dicts."""
    candidates = []

    for page in range(pages):
        params = urllib.parse.urlencode({
            "query":       query,
            "tags":        "story",
            "page":        page,
            "hitsPerPage": 50,
        })
        url = f"{HN_SEARCH_BASE}?{params}"
        logger.info("HN Algolia — query=%r page=%d", query, page)

        if dry_run:
            logger.info("[DRY-RUN] Would fetch: %s", url)
            continue

        data = fetch_json(url)
        if not data:
            logger.warning("No data for HN query=%r page=%d", query, page)
            break

        hits = data.get("hits", [])
        if not hits:
            break

        for hit in hits:
            try:
                title      = hit.get("title") or ""
                story_text = hit.get("story_text") or ""
                combined   = f"{title}\n{story_text}"

                traction = count_traction_signals(combined)
                if traction < 2:
                    continue

                mrr   = extract_mrr(combined)
                arr   = extract_arr(combined)
                users = extract_users(combined)

                points      = hit.get("points") or 1
                num_comments = hit.get("num_comments") or 0
                engagement  = max(points, 1) + num_comments

                object_id = hit.get("objectID", "")
                hn_url    = (
                    f"https://news.ycombinator.com/item?id={object_id}" if object_id else ""
                )

                candidates.append({
                    "source":            "hackernews",
                    "post_id":           object_id,
                    "title":             title[:200],
                    "url":               hit.get("url") or hn_url,
                    "author":            hit.get("author", ""),
                    "created_utc":       hit.get("created_at", ""),
                    "upvotes":           points,
                    "comments":          num_comments,
                    "mrr_usd":           mrr,
                    "arr_usd":           arr,
                    "users_count":       users,
                    "traction_signals":  traction,
                    "acquisition_score": score_post(mrr, arr, users, engagement, traction),
                    "text_snippet":      combined[:300].replace("\n", " "),
                })
            except Exception as exc:
                logger.warning("Error processing HN hit: %s", exc)

        time.sleep(0.6)

    logger.info("HN query=%r: %d acquisition candidates found", query, len(candidates))
    return candidates

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_results(posts, dry_run=False):
    """Sort by score and write CSV + JSON output through safe_path()."""
    if not posts:
        logger.info("No candidates to write.")
        return

    posts.sort(key=lambda x: x.get("acquisition_score", 0), reverse=True)

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        csv_path  = safe_path(OUTPUT_CSV)
        json_path = safe_path(OUTPUT_JSON)
    except (ValueError, OSError) as exc:
        logger.error("Output path validation failed: %s", exc)
        return

    if dry_run:
        logger.info("[DRY-RUN] Would write %d records to %s and %s", len(posts), csv_path, json_path)
        logger.info("[DRY-RUN] Top 5 by acquisition score:")
        for p in posts[:5]:
            logger.info(
                "  score=%-10.2f  %-30s  %s",
                p["acquisition_score"], p["source"], p["title"][:70],
            )
        return

    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(posts)
        logger.info("CSV written: %s (%d rows)", csv_path, len(posts))
    except OSError as exc:
        logger.error("Failed to write CSV: %s", exc)

    try:
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(posts, fh, indent=2, ensure_ascii=False)
        logger.info("JSON written: %s", json_path)
    except OSError as exc:
        logger.error("Failed to write JSON: %s", exc)

# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def show_status():
    """Print file sizes, modification times, and row counts from last run."""
    print(f"\n=== PRINTMAXX Acquisition Scanner — Status ===\n")
    for path in (OUTPUT_CSV, OUTPUT_JSON, LOG_FILE):
        try:
            p = safe_path(path)
            if p.exists():
                stat  = p.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                print(f"  {p.name:<52}  {stat.st_size:>10,} bytes   modified: {mtime}")
            else:
                print(f"  {p.name:<52}  [not found]")
        except ValueError as exc:
            print(f"  [path error] {exc}")

    try:
        csv_path = safe_path(OUTPUT_CSV)
        if csv_path.exists():
            with open(csv_path, "r", encoding="utf-8") as fh:
                rows = sum(1 for _ in fh) - 1
            print(f"\n  Last scan: {rows} acquisition candidate(s) recorded.")
    except (ValueError, OSError) as exc:
        logger.warning("Could not read CSV row count: %s", exc)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "PRINTMAXX: Scan Reddit & HN for under-the-radar young-founder "
            "acquisition targets with traction but low engagement."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run", action="store_true",
        help="Execute full scan and write CSV/JSON results.",
    )
    group.add_argument(
        "--status", action="store_true",
        help="Report status of last run outputs.",
    )
    group.add_argument(
        "--dry-run", dest="dry_run", action="store_true",
        help="Simulate scan without writing output files.",
    )
    return parser.parse_args()


def main():
    args   = parse_args()
    run_ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if args.status:
        show_status()
        return

    logger.info("=== PRINTMAXX Acquisition Scanner START %s ===", run_ts)
    logger.info("Mode: %s", "DRY-RUN" if args.dry_run else "RUN")

    try:
        skills_ctx = recall_skills_for_task(SCRIPT_NAME)
        if skills_ctx:
            logger.debug("Skills context keys: %s", list(skills_ctx.keys()))
    except Exception as exc:
        logger.debug("recall_skills_for_task skipped: %s", exc)

    all_posts = []

    # Reddit
    for subreddit in REDDIT_SUBREDDITS:
        try:
            posts = scrape_reddit(subreddit, limit=100, dry_run=args.dry_run)
            all_posts.extend(posts)
        except Exception as exc:
            logger.error("Unhandled error scraping r/%s: %s", subreddit, exc)
        time.sleep(1.2)

    # Hacker News
    for query in HN_QUERIES:
        try:
            posts = scrape_hn(query, pages=3, dry_run=args.dry_run)
            all_posts.extend(posts)
        except Exception as exc:
            logger.error("Unhandled error scraping HN query=%r: %s", query, exc)
        time.sleep(0.5)

    # Deduplicate by (source, post_id)
    seen, unique_posts = set(), []
    for p in all_posts:
        key = (p["source"], p["post_id"])
        if key not in seen:
            seen.add(key)
            unique_posts.append(p)

    logger.info("Unique acquisition candidates: %d", len(unique_posts))
    write_results(unique_posts, dry_run=args.dry_run)

    try:
        capture_skill_from_result(
            {"candidate_count": len(unique_posts), "run_ts": run_ts},
            SCRIPT_NAME,
        )
    except Exception as exc:
        logger.debug("capture_skill_from_result skipped: %s", exc)

    logger.info("=== PRINTMAXX Acquisition Scanner END %s ===", run_ts)


if __name__ == "__main__":
    main()