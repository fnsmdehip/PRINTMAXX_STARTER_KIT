#!/usr/bin/env python3
"""
PRINTMAXX Automation: iOS App Store Daily Price-Drop Acquisition Scanner
------------------------------------------------------------------------
Scans the iOS App Store for habit/productivity apps that have dropped >80%
in price — a known acquisition distress signal. Filters for apps with a
proven user base (existing ratings/reviews), extracts developer contact
information, scores each app for acquisition viability, and queues outreach
to owners for potential acquisition in the sub-$500 range.

Cron-ready. No interactive input required.

Usage:
    python ios_acquisition_scanner.py --run
    python ios_acquisition_scanner.py --run --dry-run
    python ios_acquisition_scanner.py --status
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import math
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import from _common or fall back to inline definitions
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

    def safe_path(path: Path) -> Path:
        """Validate that path resolves within PROJECT root."""
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(
                f"Path {resolved} is outside PROJECT root {PROJECT}"
            )
        return resolved

    def recall_skills_for_task(task: str) -> None:  # type: ignore[misc]
        return None

    def capture_skill_from_result(result: object, task: str) -> None:  # type: ignore[misc]
        return None

# ---------------------------------------------------------------------------
# Directory / file paths (all via safe_path on write)
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOGS_DIR        = AUTOMATIONS_DIR / "logs"
DATA_DIR        = AUTOMATIONS_DIR / "data" / "ios_acquisition"
PRICES_DB       = DATA_DIR / "price_history.json"
RESULTS_CSV     = DATA_DIR / "acquisition_candidates.csv"
QUEUE_JSON      = DATA_DIR / "outreach_queue.json"

# ---------------------------------------------------------------------------
# Scanner constants
# ---------------------------------------------------------------------------
SEARCH_TERMS: list[str] = [
    "habit tracker",
    "habit builder",
    "quit bad habits",
    "productivity timer",
    "focus timer",
    "daily routine tracker",
    "goal tracker",
    "self improvement",
    "mindfulness meditation",
    "addiction tracker",
    "screen time limiter",
    "digital detox",
    "streak tracker",
    "behavior change",
]

ITUNES_SEARCH_URL    = "https://itunes.apple.com/search"
ITUNES_LOOKUP_URL    = "https://itunes.apple.com/lookup"
COUNTRY              = "us"
ENTITY               = "software"
LIMIT                = 200
PRICE_DROP_THRESHOLD = 0.80    # flag apps that dropped > 80 % from peak
MIN_RATINGS          = 10      # require proven user base
MIN_SCORE_FOR_QUEUE  = 40.0    # acquisition viability threshold for outreach
REQUEST_DELAY_SEC    = 1.5     # polite delay between Apple API calls
MAX_HISTORY_SNAPSHOTS = 90     # price snapshots retained per app

# ---------------------------------------------------------------------------
# Logging setup (append to file, also echo to stdout)
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = safe_path(LOGS_DIR / "ios_acquisition_scanner.log")
    logger = logging.getLogger("ios_acquisition_scanner")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(str(log_file), mode="a", encoding="utf-8")
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger


log = setup_logging()

# ---------------------------------------------------------------------------
# Directory bootstrap
# ---------------------------------------------------------------------------

def ensure_dirs() -> None:
    for directory in (LOGS_DIR, DATA_DIR):
        directory.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Network helpers (urllib only)
# ---------------------------------------------------------------------------

def fetch_json(url: str, params: dict) -> dict:
    """GET a JSON endpoint using only urllib. Returns parsed dict."""
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        full_url,
        headers={"User-Agent": "PRINTMAXX-AcquisitionScanner/1.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)  # type: ignore[return-value]

# ---------------------------------------------------------------------------
# Persistence helpers (all writes through safe_path)
# ---------------------------------------------------------------------------

def load_price_history() -> dict:
    db_path = safe_path(PRICES_DB)
    if db_path.exists():
        try:
            with open(db_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Could not load price history (%s) — starting fresh.", exc)
    return {}


def save_price_history(history: dict) -> None:
    db_path = safe_path(PRICES_DB)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with open(db_path, "w", encoding="utf-8") as fh:
        json.dump(history, fh, indent=2)


def save_results_csv(candidates: list[dict], dry_run: bool = False) -> None:
    if not candidates:
        log.info("No candidates to write to CSV.")
        return
    out_path = safe_path(RESULTS_CSV)
    fieldnames = [
        "track_id", "track_name", "artist_name", "genre",
        "current_price", "previous_price", "price_drop_pct",
        "rating_count", "average_rating", "seller_name",
        "developer_url", "support_url", "track_view_url",
        "bundle_id", "last_updated", "acquisition_score", "scan_date",
    ]
    mode       = "a" if out_path.exists() else "w"
    write_hdr  = not out_path.exists()
    tag        = "[DRY-RUN] " if dry_run else ""
    log.info("%sWriting %d candidates to %s", tag, len(candidates), out_path)
    if dry_run:
        return
    with open(out_path, mode, newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        if write_hdr:
            writer.writeheader()
        writer.writerows(candidates)


def save_outreach_queue(candidates: list[dict], dry_run: bool = False) -> None:
    if not candidates:
        return
    queue_path = safe_path(QUEUE_JSON)
    existing: list[dict] = []
    if queue_path.exists():
        try:
            with open(queue_path, "r", encoding="utf-8") as fh:
                existing = json.load(fh)
        except (json.JSONDecodeError, OSError):
            existing = []

    known_ids  = {str(e.get("track_id")) for e in existing}
    new_items  = [c for c in candidates if str(c.get("track_id")) not in known_ids]
    skipped    = len(candidates) - len(new_items)
    tag        = "[DRY-RUN] " if dry_run else ""
    log.info(
        "%sQueuing %d new outreach targets (skipping %d already queued).",
        tag, len(new_items), skipped,
    )
    if dry_run or not new_items:
        return
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    with open(queue_path, "w", encoding="utf-8") as fh:
        json.dump(existing + new_items, fh, indent=2)

# ---------------------------------------------------------------------------
# iTunes Search / Lookup
# ---------------------------------------------------------------------------

def search_apps(term: str) -> list[dict]:
    try:
        data = fetch_json(ITUNES_SEARCH_URL, {
            "term":    term,
            "country": COUNTRY,
            "entity":  ENTITY,
            "limit":   LIMIT,
        })
        results = data.get("results", [])
        log.info("  '%s' → %d results", term, len(results))
        return results
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as exc:
        log.warning("Search failed for '%s': %s", term, exc)
        return []

# ---------------------------------------------------------------------------
# Acquisition scoring (0–100)
# ---------------------------------------------------------------------------

def score_acquisition(app: dict, price_drop_pct: float) -> float:
    """
    Score acquisition viability on a 0–100 scale.

    Breakdown
    ---------
    40 pts  — price-drop severity  (higher drop = stronger distress signal)
    20 pts  — rating count         (log scale; proven user base)
    20 pts  — average user rating  (quality proxy)
    10 pts  — current price        (affordability of entry ask)
    10 pts  — genre relevance      (habit / productivity fit)
    """
    score = 0.0

    # 1. Price-drop severity (40 pts)
    score += min(price_drop_pct * 40.0, 40.0)

    # 2. Rating count on log scale (20 pts)
    rating_count: int = app.get("userRatingCount") or 0
    if rating_count > 0:
        score += min(math.log10(rating_count + 1) / math.log10(10_001) * 20.0, 20.0)

    # 3. Average rating (20 pts)
    avg_rating: float = app.get("averageUserRating") or 0.0
    score += (avg_rating / 5.0) * 20.0

    # 4. Current (post-drop) price affordability (10 pts)
    price: float = app.get("price") or 0.0
    if price == 0.0:
        score += 5.0       # free — moderate bonus, check intent
    elif price <= 1.99:
        score += 10.0
    elif price <= 4.99:
        score += 7.0
    elif price <= 9.99:
        score += 4.0

    # 5. Genre relevance (10 pts)
    genre = (app.get("primaryGenreName") or "").lower()
    top_genres = {"health & fitness", "productivity", "lifestyle", "education"}
    if genre in top_genres:
        score += 10.0
    elif any(kw in genre for kw in ("health", "product", "lifest", "educat")):
        score += 5.0

    return round(score, 2)

# ---------------------------------------------------------------------------
# Core: price-drop detection
# ---------------------------------------------------------------------------

def detect_price_drops(
    apps: list[dict],
    history: dict,
    today: str,
) -> tuple[list[dict], dict]:
    """
    Compare current prices against stored history.

    Returns (candidates_list, updated_history).
    """
    candidates: list[dict] = []

    for app in apps:
        track_id = str(app.get("trackId") or "")
        if not track_id:
            continue

        current_price: float | None = app.get("price")
        if current_price is None:
            continue

        # Initialise history record
        if track_id not in history:
            history[track_id] = {
                "name":       app.get("trackName", ""),
                "prices":     [],
                "peak_price": current_price,
            }

        record = history[track_id]
        record["prices"].append({"date": today, "price": current_price})
        record["prices"] = record["prices"][-MAX_HISTORY_SNAPSHOTS:]

        if current_price > record.get("peak_price", 0):
            record["peak_price"] = current_price

        peak_price: float = record.get("peak_price", current_price)

        if peak_price <= 0.0 or current_price >= peak_price:
            continue

        drop_pct = (peak_price - current_price) / peak_price
        if drop_pct < PRICE_DROP_THRESHOLD:
            continue

        rating_count: int = app.get("userRatingCount") or 0
        if rating_count < MIN_RATINGS:
            continue

        acq_score = score_acquisition(app, drop_pct)

        candidates.append({
            "track_id":        track_id,
            "track_name":      app.get("trackName", ""),
            "artist_name":     app.get("artistName", ""),
            "genre":           app.get("primaryGenreName", ""),
            "current_price":   current_price,
            "previous_price":  peak_price,
            "price_drop_pct":  round(drop_pct * 100.0, 1),
            "rating_count":    rating_count,
            "average_rating":  app.get("averageUserRating") or 0.0,
            "seller_name":     app.get("sellerName", ""),
            "developer_url":   app.get("artistViewUrl", ""),
            "support_url":     app.get("supportUrl", ""),
            "track_view_url":  app.get("trackViewUrl", ""),
            "bundle_id":       app.get("bundleId", ""),
            "last_updated":    app.get("currentVersionReleaseDate", ""),
            "acquisition_score": acq_score,
            "scan_date":       today,
        })

    candidates.sort(key=lambda x: x["acquisition_score"], reverse=True)
    return candidates, history

# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_run(dry_run: bool = False) -> int:
    recall_skills_for_task("ios_app_price_drop_acquisition_scan")
    ensure_dirs()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log.info(
        "=== iOS Acquisition Scanner — %s%s ===",
        today,
        " [DRY-RUN]" if dry_run else "",
    )

    history = load_price_history()
    all_apps: dict[str, dict] = {}   # deduplicated by track_id

    for term in SEARCH_TERMS:
        for app in search_apps(term):
            tid = str(app.get("trackId") or "")
            if tid and tid not in all_apps:
                all_apps[tid] = app
        time.sleep(REQUEST_DELAY_SEC)

    log.info("Unique apps collected across all search terms: %d", len(all_apps))

    candidates, updated_history = detect_price_drops(
        list(all_apps.values()), history, today
    )
    log.info(
        "Price-drop candidates (>%.0f%% from peak, ≥%d ratings): %d",
        PRICE_DROP_THRESHOLD * 100,
        MIN_RATINGS,
        len(candidates),
    )

    high_value = [c for c in candidates if c["acquisition_score"] >= MIN_SCORE_FOR_QUEUE]
    log.info(
        "High-value acquisition targets (score ≥ %.0f): %d",
        MIN_SCORE_FOR_QUEUE,
        len(high_value),
    )

    if not dry_run:
        save_price_history(updated_history)

    save_results_csv(candidates, dry_run=dry_run)
    save_outreach_queue(high_value, dry_run=dry_run)

    capture_skill_from_result(
        {"candidates": len(candidates), "queued": len(high_value), "date": today},
        "ios_app_price_drop_acquisition_scan",
    )
    log.info("Scan complete.")
    return 0


def cmd_status() -> int:
    ensure_dirs()
    print(f"PROJECT root : {PROJECT}")
    print(f"Data dir     : {DATA_DIR}")

    history = load_price_history()
    print(f"Apps tracked in price history: {len(history)}")

    queue_path = safe_path(QUEUE_JSON)
    if queue_path.exists():
        try:
            with open(queue_path, "r", encoding="utf-8") as fh:
                queue: list[dict] = json.load(fh)
            pending = [e for e in queue if not e.get("contacted")]
            print(f"Outreach queue total : {len(queue)}")
            print(f"  Pending outreach   : {len(pending)}")
            if pending:
                top5 = sorted(
                    pending,
                    key=lambda x: x.get("acquisition_score", 0),
                    reverse=True,
                )[:5]
                print("\n  Top 5 pending targets:")
                for entry in top5:
                    print(
                        f"    [score {entry.get('acquisition_score', 0):.1f}]"
                        f"  {entry.get('track_name', '?')}"
                        f"  by {entry.get('artist_name', '?')}"
                        f"  (${entry.get('previous_price', '?')}"
                        f" → ${entry.get('current_price', '?')},"
                        f" {entry.get('price_drop_pct', '?')}% drop)"
                    )
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Could not read outreach queue: {exc}")
    else:
        print("Outreach queue: not yet created (run --run first)")

    results_path = safe_path(RESULTS_CSV)
    if results_path.exists():
        try:
            with open(results_path, "r", encoding="utf-8") as fh:
                row_count = sum(1 for _ in csv.reader(fh)) - 1  # subtract header
            print(f"\nAll-time candidates logged in CSV: {row_count}")
        except OSError as exc:
            print(f"Could not read results CSV: {exc}")
    else:
        print("\nResults CSV: not yet created (run --run first)")

    log_file = safe_path(LOGS_DIR / "ios_acquisition_scanner.log")
    if log_file.exists():
        try:
            size_kb = log_file.stat().st_size / 1024
            print(f"\nLog file: {log_file} ({size_kb:.1f} KB)")
            result = subprocess.run(
                ["tail", "-n", "5", str(log_file)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                print("  Last 5 log lines:")
                for line in result.stdout.strip().splitlines():
                    print(f"    {line}")
        except OSError:
            pass

    return 0

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: iOS App Store Daily Price-Drop Acquisition Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --run\n"
            "  %(prog)s --run --dry-run\n"
            "  %(prog)s --status\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run",    action="store_true", help="Execute the daily scan")
    group.add_argument("--status", action="store_true", help="Print scanner status summary")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the scan without writing output files",
    )
    args = parser.parse_args()

    try:
        if args.run:
            sys.exit(cmd_run(dry_run=args.dry_run))
        elif args.status:
            sys.exit(cmd_status())
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
        sys.exit(130)
    except Exception as exc:
        log.exception("Unhandled error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()