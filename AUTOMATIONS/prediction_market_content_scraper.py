#!/usr/bin/env python3
"""
PRINTMAXX Automation System — Prediction Market Content Scraper

Scrapes Polymarket Gamma API (public, no auth) for top 20 markets by weekly
volume. Extracts question, current odds, volume, and close date. Filters for
high-engagement categories (politics, crypto, macro). Generates 3 content
angles per market: hot take on odds, contrarian 'market is wrong' take, and
outcome prediction. Pipes results to engagement_bait_converter.py and post
queue. Also checks resolved markets and generates 'called it' posts.

Usage:
    python3 prediction_market_content_scraper.py --run
    python3 prediction_market_content_scraper.py --status
    python3 prediction_market_content_scraper.py --dry-run
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
# _common imports with fallback
# ---------------------------------------------------------------------------
try:
    from _common import (
        PROJECT,
        capture_skill_from_result,
        recall_skills_for_task,
        safe_path,
    )
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path):
        """Validate that path is within the PROJECT directory."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(
                f"Path {resolved!r} is outside PROJECT root {PROJECT!r}"
            )
        return resolved

    def recall_skills_for_task(task_description):
        return []

    def capture_skill_from_result(result, task_description):
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_NAME = "prediction_market_content_scraper"
LOG_FILE = safe_path(PROJECT / "AUTOMATIONS" / "logs" / f"{SCRIPT_NAME}.log")
QUEUE_DIR = safe_path(PROJECT / "AUTOMATIONS" / "post_queue")
DATA_DIR = safe_path(PROJECT / "AUTOMATIONS" / "data" / "prediction_markets")
CALLED_IT_DIR = safe_path(PROJECT / "AUTOMATIONS" / "data" / "called_it")
SNAPSHOT_FILE = DATA_DIR / "last_snapshot.json"
RESOLVED_CACHE = CALLED_IT_DIR / "resolved_cache.json"
STATUS_FILE = DATA_DIR / "status.json"

GAMMA_API_BASE = "https://gamma-api.polymarket.com"
MARKETS_ENDPOINT = f"{GAMMA_API_BASE}/markets"

TOP_N = 20
FETCH_LIMIT = 100

HIGH_ENGAGEMENT_KEYWORDS = {
    "politics",
    "political",
    "election",
    "elections",
    "president",
    "senate",
    "congress",
    "government",
    "policy",
    "trump",
    "crypto",
    "cryptocurrency",
    "bitcoin",
    "btc",
    "ethereum",
    "eth",
    "defi",
    "macro",
    "economics",
    "economy",
    "fed",
    "federal reserve",
    "inflation",
    "recession",
    "interest rate",
    "gdp",
    "finance",
    "market",
    "stocks",
    "geopolitics",
    "war",
    "conflict",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def setup_logging():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(LOG_FILE), mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )


log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------


def fetch_json(url, timeout=30):
    """Fetch JSON from a URL using only urllib."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "PRINTMAXX/1.0 (prediction-market-scraper)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        log.error("HTTP error fetching %s: %s %s", url, exc.code, exc.reason)
    except urllib.error.URLError as exc:
        log.error("URL error fetching %s: %s", url, exc.reason)
    except json.JSONDecodeError as exc:
        log.error("JSON decode error for %s: %s", url, exc)
    except Exception as exc:
        log.error("Unexpected error fetching %s: %s", url, exc)
    return None


def fetch_top_markets(limit=FETCH_LIMIT):
    """
    Fetch active markets from Polymarket Gamma API sorted by weekly volume.
    Falls back to volumeClob sort if volume1wk is unavailable.
    """
    for order_key in ("volume1wk", "volumeClob"):
        params = urllib.parse.urlencode(
            {
                "limit": limit,
                "order": order_key,
                "sort": "desc",
                "active": "true",
                "closed": "false",
            }
        )
        url = f"{MARKETS_ENDPOINT}?{params}"
        log.info("Fetching markets (%s): %s", order_key, url)
        data = fetch_json(url)
        if data is not None:
            return data
        log.warning("Sort by %s failed; trying next option", order_key)
    return []


def fetch_recently_resolved(limit=50):
    """Fetch recently closed/resolved markets."""
    params = urllib.parse.urlencode(
        {
            "limit": limit,
            "order": "endDate",
            "sort": "desc",
            "closed": "true",
        }
    )
    url = f"{MARKETS_ENDPOINT}?{params}"
    log.info("Fetching resolved markets: %s", url)
    return fetch_json(url) or []


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def _decode_json_field(value):
    """Decode a field that may be a JSON-encoded string."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return value
    return value


def parse_odds(market):
    """Return a human-readable odds string from outcomePrices."""
    try:
        prices = _decode_json_field(
            market.get("outcomePrices") or market.get("bestBid") or []
        )
        if not prices:
            return "N/A"
        outcomes = _decode_json_field(market.get("outcomes") or [])
        floats = [float(p) for p in prices]
        if outcomes and len(outcomes) == len(floats):
            return ", ".join(
                f"{o}: {v * 100:.1f}%" for o, v in zip(outcomes, floats)
            )
        return ", ".join(f"{v * 100:.1f}%" for v in floats)
    except Exception:
        return "N/A"


def parse_volume(market):
    """Return weekly volume as float, trying multiple field names."""
    for key in ("volume1wk", "volumeClob1wk", "volumeClob", "volume"):
        val = market.get(key)
        if val is not None:
            try:
                return float(val)
            except (TypeError, ValueError):
                pass
    return 0.0


def parse_close_date(market):
    """Return ISO close date string."""
    for key in ("endDate", "endDateIso", "closeTime"):
        val = market.get(key)
        if val:
            return str(val)
    return "N/A"


def leading_outcome(market):
    """Return (outcome_name, pct_float) for the highest-probability outcome."""
    try:
        prices = _decode_json_field(market.get("outcomePrices") or [])
        outcomes = _decode_json_field(market.get("outcomes") or [])
        if not prices:
            return ("Yes", 50.0)
        floats = [float(p) for p in prices]
        idx = floats.index(max(floats))
        name = outcomes[idx] if outcomes and idx < len(outcomes) else "Yes"
        return (name, floats[idx] * 100.0)
    except Exception:
        return ("Yes", 50.0)


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------


def is_high_engagement(market):
    """Return True if market matches any high-engagement keyword."""
    parts = [
        (market.get("category") or "").lower(),
        (market.get("question") or "").lower(),
    ]
    tags = _decode_json_field(market.get("tags") or [])
    if isinstance(tags, list):
        parts.extend(str(t).lower() for t in tags)
    combined = " ".join(parts)
    return any(kw in combined for kw in HIGH_ENGAGEMENT_KEYWORDS)


# ---------------------------------------------------------------------------
# Content angle generation
# ---------------------------------------------------------------------------


def generate_content_angles(market):
    """
    Return a list of 3 content angle dicts for a single market.

    Angles:
      1. hot_take        — lean into consensus odds
      2. contrarian      — 'market is wrong' narrative
      3. outcome_prediction — explicit prediction with tagging
    """
    question = market.get("question") or "Unknown market"
    odds_str = parse_odds(market)
    volume = parse_volume(market)
    close_date = parse_close_date(market)
    leader, pct = leading_outcome(market)

    volume_fmt = f"${volume:,.0f}"
    pct_fmt = f"{pct:.1f}%"
    underdog_pct = f"{100.0 - pct:.1f}%"

    hot_take = (
        f"Polymarket has spoken: '{question}' → {leader} at {pct_fmt}. "
        f"{volume_fmt} in weekly volume and the crowd is NOT wavering. "
        f"At this point, fading the market is a donation. "
        f"Closes {close_date}. #Polymarket #PredictionMarkets"
    )

    contrarian = (
        f"Unpopular opinion: the market is MISPRICED on '{question}'. "
        f"{leader} at {pct_fmt} is way too confident. "
        f"I'd be looking hard at the {underdog_pct} side. "
        f"Current odds: {odds_str} | Closes {close_date}. "
        f"#Contrarian #Polymarket #PredictionMarkets"
    )

    prediction = (
        f"Locking in my prediction now: '{question}' → {leader}. "
        f"Market agrees at {pct_fmt}. Tagging this for the 'called it' post. "
        f"Volume: {volume_fmt} this week. Closes {close_date}. "
        f"#CalledIt #Polymarket #PredictionMarkets"
    )

    return [
        {"angle_type": "hot_take", "content": hot_take},
        {"angle_type": "contrarian", "content": contrarian},
        {"angle_type": "outcome_prediction", "content": prediction},
    ]


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------


def ensure_dirs():
    for directory in (DATA_DIR, QUEUE_DIR, CALLED_IT_DIR, LOG_FILE.parent):
        safe_path(directory).mkdir(parents=True, exist_ok=True)


def write_json(path, data):
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def read_json(path):
    p = safe_path(path)
    if not p.exists():
        return None
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        log.warning("Could not read %s: %s", p, exc)
        return None


def write_csv(path, rows, fieldnames):
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def append_to_post_queue(posts, dry_run=False):
    """Write posts as JSONL to a timestamped file in the post queue."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    queue_file = safe_path(QUEUE_DIR / f"posts_{timestamp}.jsonl")
    if dry_run:
        log.info("[DRY-RUN] Would write %d posts to %s", len(posts), queue_file)
        for post in posts[:3]:
            log.info("[DRY-RUN] Sample: %s", post.get("content", "")[:120])
        return
    queue_file.parent.mkdir(parents=True, exist_ok=True)
    with open(queue_file, "w", encoding="utf-8") as fh:
        for post in posts:
            fh.write(json.dumps(post, ensure_ascii=False) + "\n")
    log.info("Wrote %d posts to queue: %s", len(posts), queue_file)


# ---------------------------------------------------------------------------
# engagement_bait_converter pipe
# ---------------------------------------------------------------------------


def pipe_to_engagement_bait_converter(enriched_markets, dry_run=False):
    """
    Pass enriched market data to engagement_bait_converter.py via stdin.
    Returns parsed JSON output on success, None on failure or missing script.
    """
    converter = safe_path(
        PROJECT / "AUTOMATIONS" / "engagement_bait_converter.py"
    )
    if not converter.exists():
        log.warning(
            "engagement_bait_converter.py not found at %s — skipping", converter
        )
        return None

    payload = json.dumps(enriched_markets, ensure_ascii=False).encode("utf-8")
    cmd = [sys.executable, str(converter)]
    if dry_run:
        cmd.append("--dry-run")

    log.info("Piping %d markets to engagement_bait_converter", len(enriched_markets))
    try:
        result = subprocess.run(
            cmd,
            input=payload,
            capture_output=True,
            timeout=120,
        )
        if result.returncode != 0:
            log.error(
                "engagement_bait_converter exited %d: %s",
                result.returncode,
                result.stderr.decode("utf-8", errors="replace")[:500],
            )
            return None
        stdout = result.stdout.decode("utf-8", errors="replace").strip()
        if stdout:
            return json.loads(stdout)
    except subprocess.TimeoutExpired:
        log.error("engagement_bait_converter timed out after 120s")
    except json.JSONDecodeError as exc:
        log.error("Could not parse engagement_bait_converter output: %s", exc)
    except Exception as exc:
        log.error("Error running engagement_bait_converter: %s", exc)
    return None


# ---------------------------------------------------------------------------
# Resolved market "called it" checker
# ---------------------------------------------------------------------------


def load_resolved_cache():
    cached = read_json(RESOLVED_CACHE)
    return cached if isinstance(cached, dict) else {}


def check_resolved_markets(dry_run=False):
    """
    Fetch recently resolved markets. Cross-reference with the last snapshot
    to identify markets we previously tracked and predicted. Generate
    'called it' posts for correct predictions and resolved-note posts for
    untracked markets. Updates the resolved cache to avoid reprocessing.
    """
    log.info("Checking for newly resolved markets...")
    resolved = fetch_recently_resolved()
    if not resolved:
        if isinstance(resolved, list):
            log.info("No resolved markets returned.")
        else:
            log.warning("Unexpected response type from resolved-markets API.")
        return []

    if isinstance(resolved, dict):
        resolved = resolved.get("data") or resolved.get("markets") or []

    snapshot = read_json(SNAPSHOT_FILE) or {}
    tracked = {
        m["id"]: m
        for m in snapshot.get("markets", [])
        if m.get("id")
    }
    cache = load_resolved_cache()
    new_posts = []
    now_iso = datetime.now(timezone.utc).isoformat()

    for market in resolved:
        mid = str(
            market.get("id") or market.get("conditionId") or ""
        ).strip()
        if not mid or mid in cache:
            continue

        question = market.get("question") or "Unknown market"
        winning_outcome = (
            market.get("winnerOutcome")
            or market.get("result")
            or "resolved"
        )
        close_date = parse_close_date(market)

        if mid in tracked:
            prev = tracked[mid]
            leader, pct = leading_outcome(prev)
            if leader.lower() in str(winning_outcome).lower():
                post = {
                    "type": "called_it",
                    "market_id": mid,
                    "question": question,
                    "predicted": leader,
                    "actual": winning_outcome,
                    "confidence_pct": round(pct, 1),
                    "close_date": close_date,
                    "content": (
                        f"CALLED IT. '{question}' — predicted {leader} "
                        f"({pct:.1f}% market consensus). "
                        f"Result: {winning_outcome}. Closed {close_date}. "
                        f"#CalledIt #Polymarket #PredictionMarkets"
                    ),
                    "generated_at": now_iso,
                }
            else:
                post = {
                    "type": "missed_call",
                    "market_id": mid,
                    "question": question,
                    "predicted": leader,
                    "actual": winning_outcome,
                    "confidence_pct": round(pct, 1),
                    "close_date": close_date,
                    "content": (
                        f"Market humbles us all. '{question}' — the crowd "
                        f"was pricing {leader} at {pct:.1f}% and got "
                        f"{winning_outcome}. That's why we trade. "
                        f"Closed {close_date}. #Polymarket #PredictionMarkets"
                    ),
                    "generated_at": now_iso,
                }
            log.info(
                "%s: %s → %s", post["type"], question[:60], winning_outcome
            )
        else:
            post = {
                "type": "resolved_note",
                "market_id": mid,
                "question": question,
                "actual": winning_outcome,
                "close_date": close_date,
                "content": (
                    f"Market settled: '{question}' resolved as "
                    f"{winning_outcome}. Closed {close_date}. "
                    f"#Polymarket #PredictionMarkets"
                ),
                "generated_at": now_iso,
            }

        new_posts.append(post)
        cache[mid] = {
            "question": question,
            "result": winning_outcome,
            "processed_at": now_iso,
        }

    save_resolved_cache(cache)

    if new_posts:
        append_to_post_queue(new_posts, dry_run=dry_run)
        csv_path = safe_path(
            CALLED_IT_DIR
            / f"called_it_{datetime.now(timezone.utc).strftime('%Y%m%d')}.csv"
        )
        write_csv(
            csv_path,
            new_posts,
            fieldnames=[
                "type",
                "market_id",
                "question",
                "predicted",
                "actual",
                "confidence_pct",
                "close_date",
                "content",
                "generated_at",
            ],
        )
        log.info("Generated %d resolved-market posts", len(new_posts))

    return new_posts


def save_resolved_cache(cache):
    write_json(RESOLVED_CACHE, cache)


# ---------------------------------------------------------------------------
# Main scraper run
# ---------------------------------------------------------------------------


def run_scraper(dry_run=False):
    """
    Full scrape-filter-generate-queue pipeline.
    Returns True on success, False on unrecoverable error.
    """
    mode_label = "DRY RUN" if dry_run else "LIVE RUN"
    log.info("=== PRINTMAXX Prediction Market Scraper — %s ===", mode_label)

    recall_skills_for_task(
        "scrape Polymarket prediction markets, filter high-engagement categories, "
        "generate content angles, queue posts"
    )

    # 1. Fetch
    raw = fetch_top_markets()
    if not raw:
        log.error("No market data received from Polymarket Gamma API. Aborting.")
        return False
    if isinstance(raw, dict):
        raw = raw.get("data") or raw.get("markets") or []
    log.info("Fetched %d raw markets", len(raw))

    # 2. Filter
    filtered = [m for m in raw if is_high_engagement(m)]
    log.info("High-engagement filter: %d / %d markets", len(filtered), len(raw))
    if len(filtered) < 5:
        log.info("Too few filtered results; using full market list")
        filtered = raw

    # 3. Sort and trim
    filtered.sort(key=parse_volume, reverse=True)
    top_markets = filtered[:TOP_N]
    log.info("Selected top %d markets by weekly volume", len(top_markets))

    # 4. Build enriched records
    now_iso = datetime.now(timezone.utc).isoformat()
    enriched = []
    for market in top_markets:
        record = {
            "id": str(
                market.get("id") or market.get("conditionId") or ""
            ).strip(),
            "question": market.get("question") or "",
            "odds": parse_odds(market),
            "volume_weekly": parse_volume(market),
            "close_date": parse_close_date(market),
            "category": market.get("category") or "",
            "slug": market.get("slug") or "",
            "content_angles": generate_content_angles(market),
            "scraped_at": now_iso,
        }
        enriched.append(record)

    # 5. Persist snapshot
    snapshot = {"scraped_at": now_iso, "markets": enriched}
    write_json(SNAPSHOT_FILE, snapshot)
    log.info("Snapshot saved: %s", SNAPSHOT_FILE)

    # 6. CSV summary
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    csv_path = safe_path(DATA_DIR / f"markets_{date_str}.csv")
    write_csv(
        csv_path,
        enriched,
        fieldnames=[
            "id",
            "question",
            "odds",
            "volume_weekly",
            "close_date",
            "category",
            "scraped_at",
        ],
    )
    log.info("CSV saved: %s", csv_path)

    # 7. Flatten content angles into post objects
    all_posts = []
    for record in enriched:
        for angle in record["content_angles"]:
            all_posts.append(
                {
                    "market_id": record["id"],
                    "question": record["question"],
                    "angle_type": angle["angle_type"],
                    "content": angle["content"],
                    "volume_weekly": record["volume_weekly"],
                    "close_date": record["close_date"],
                    "category": record["category"],
                    "source": "polymarket",
                    "generated_at": now_iso,
                }
            )
    log.info(
        "Generated %d content posts across %d markets",
        len(all_posts),
        len(enriched),
    )

    # 8. engagement_bait_converter pipe
    converter_output = pipe_to_engagement_bait_converter(enriched, dry_run=dry_run)
    if converter_output:
        capture_skill_from_result(
            converter_output, "engagement bait conversion of prediction markets"
        )
        log.info(
            "engagement_bait_converter returned %d enhanced posts",
            len(converter_output),
        )
        final_posts = converter_output
    else:
        final_posts = all_posts

    # 9. Post queue
    append_to_post_queue(final_posts, dry_run=dry_run)

    # 10. Resolved-market "called it" checker
    check_resolved_markets(dry_run=dry_run)

    # 11. Status file
    status = {
        "last_run": now_iso,
        "mode": mode_label,
        "markets_fetched": len(raw),
        "markets_after_filter": len(top_markets),
        "posts_generated": len(final_posts),
        "status": "success",
    }
    write_json(STATUS_FILE, status)
    log.info("Run complete: %s", status)
    return True


# ---------------------------------------------------------------------------
# --status display
# ---------------------------------------------------------------------------


def show_status():
    """Print last-run status and snapshot summary to stdout."""
    status = read_json(STATUS_FILE)
    if not status:
        print("No status file found. Has the scraper been run yet?")
        return

    print(json.dumps(status, indent=2))

    snapshot = read_json(SNAPSHOT_FILE)
    if snapshot:
        markets = snapshot.get("markets") or []
        print(f"\nLast snapshot:    {snapshot.get('scraped_at', 'N/A')}")
        print(f"Markets tracked:  {len(markets)}")
        if markets:
            print("\nTop 5 by weekly volume:")
            sorted_markets = sorted(
                markets, key=lambda x: x.get("volume_weekly", 0), reverse=True
            )
            for m in sorted_markets[:5]:
                vol = m.get("volume_weekly", 0)
                q = (m.get("question") or "")[:72]
                print(f"  ${vol:>12,.0f}  {q}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX — Polymarket Prediction Market Content Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Scrape markets, generate content angles, and write to post queue",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print last-run status and snapshot summary",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Run full pipeline but do not write to post queue",
    )
    return parser


def main():
    setup_logging()
    ensure_dirs()
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            show_status()
            sys.exit(0)
        elif args.run:
            success = run_scraper(dry_run=False)
            sys.exit(0 if success else 1)
        elif args.dry_run:
            success = run_scraper(dry_run=True)
            sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log.info("Interrupted.")
        sys.exit(0)
    except Exception as exc:
        log.exception("Fatal error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()