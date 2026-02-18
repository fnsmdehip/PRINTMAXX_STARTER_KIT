#!/usr/bin/env python3
"""
PRINTMAXX SEO Monitoring Script
=================================
Tracks keyword rankings over time, logs position changes, and alerts on
significant ranking shifts.

Usage:
    python3 track_rankings.py                          # Check all keywords
    python3 track_rankings.py --keywords "prayer app, fitness timer"
    python3 track_rankings.py --from-csv keywords.csv  # Load from CSV
    python3 track_rankings.py --report                 # Generate report only
    python3 track_rankings.py --alert-threshold 3      # Alert on 3+ position shift

Environment Variables:
    SERPAPI_KEY         - SerpApi key (100 free searches/month)
    VALUESERP_KEY      - ValueSERP key (alternative)
    SERPER_API_KEY      - Serper.dev key (2,500 free searches)

Note: Without API keys, the script uses a lightweight HTML scraping approach
which may be rate-limited by Google. API keys are recommended for production use.
"""

import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RANKINGS_CSV = Path(__file__).resolve().parent / "rankings_history.csv"
LONGTAIL_SLUGS = PROJECT_ROOT / "LEDGER" / "GEO_LONGTAIL_SLUGS_300.csv"
REPORT_DIR = Path(__file__).resolve().parent / "reports"

# Our domains to track
OUR_DOMAINS = [
    "printmaxx.com",
    "printmaxx.io",
    "printmaxx.co",
]

# API keys
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")
VALUESERP_KEY = os.environ.get("VALUESERP_KEY", "")
SERPER_KEY = os.environ.get("SERPER_API_KEY", "")

# Defaults
DEFAULT_ALERT_THRESHOLD = 5  # positions
CHECK_DEPTH = 30  # check first 30 results


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def load_keywords_from_csv(filepath: Path) -> list:
    """Load keywords from a CSV file."""
    keywords = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Try common column names
            for key in row:
                k = key.lower().strip()
                if k in ("keyword", "keywords", "query", "search_term", "term"):
                    kw = row[key].strip()
                    if kw:
                        keywords.append(kw)
                    break
    return keywords


def load_keywords_from_slugs() -> list:
    """Load keywords from GEO_LONGTAIL_SLUGS_300.csv."""
    keywords = []
    if not LONGTAIL_SLUGS.exists():
        return keywords

    with open(LONGTAIL_SLUGS, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw = row.get("keyword", "").strip()
            if kw:
                keywords.append(kw)
    return keywords


def check_ranking_serpapi(keyword: str) -> list:
    """Check ranking using SerpApi."""
    if not SERPAPI_KEY:
        return []

    params = urllib.parse.urlencode({
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "q": keyword,
        "num": CHECK_DEPTH,
        "gl": "us",
        "hl": "en",
    })

    url = f"https://serpapi.com/search?{params}"
    data = _make_request(url)

    if not data:
        return []

    results = []
    organic = data.get("organic_results", [])
    for i, result in enumerate(organic):
        results.append({
            "position": i + 1,
            "url": result.get("link", ""),
            "title": result.get("title", ""),
            "domain": _extract_domain(result.get("link", "")),
        })

    return results


def check_ranking_serper(keyword: str) -> list:
    """Check ranking using Serper.dev."""
    if not SERPER_KEY:
        return []

    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": keyword,
        "num": CHECK_DEPTH,
        "gl": "us",
        "hl": "en",
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "X-API-KEY": SERPER_KEY,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        log(f"Serper error: {e}")
        return []

    results = []
    organic = data.get("organic", [])
    for i, result in enumerate(organic):
        results.append({
            "position": result.get("position", i + 1),
            "url": result.get("link", ""),
            "title": result.get("title", ""),
            "domain": _extract_domain(result.get("link", "")),
        })

    return results


def check_ranking_valueserp(keyword: str) -> list:
    """Check ranking using ValueSERP."""
    if not VALUESERP_KEY:
        return []

    params = urllib.parse.urlencode({
        "api_key": VALUESERP_KEY,
        "q": keyword,
        "num": CHECK_DEPTH,
        "location": "United States",
    })

    url = f"https://api.valueserp.com/search?{params}"
    data = _make_request(url)

    if not data:
        return []

    results = []
    organic = data.get("organic_results", [])
    for i, result in enumerate(organic):
        results.append({
            "position": result.get("position", i + 1),
            "url": result.get("link", ""),
            "title": result.get("title", ""),
            "domain": _extract_domain(result.get("link", "")),
        })

    return results


def _make_request(url: str) -> Optional[dict]:
    """Make HTTP request with error handling."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX-SEO/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        log(f"Request error: {e}")
        return None


def _extract_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return domain
    except Exception:
        return ""


def find_our_position(results: list) -> Optional[dict]:
    """Find our domain's position in search results."""
    for result in results:
        domain = result.get("domain", "")
        for our_domain in OUR_DOMAINS:
            if our_domain in domain:
                return result
    return None


def load_ranking_history() -> dict:
    """Load previous ranking data for comparison."""
    history = {}
    if not RANKINGS_CSV.exists():
        return history

    with open(RANKINGS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            keyword = row.get("keyword", "")
            if keyword:
                # Keep the most recent entry per keyword
                existing = history.get(keyword)
                if not existing or row.get("date", "") > existing.get("date", ""):
                    history[keyword] = row

    return history


def save_ranking_entry(entry: dict) -> None:
    """Append a single ranking entry to history CSV."""
    fieldnames = [
        "date", "keyword", "position", "url", "title", "domain",
        "previous_position", "position_change", "source",
    ]

    file_exists = RANKINGS_CSV.exists()
    with open(RANKINGS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)


def check_keywords(keywords: list, alert_threshold: int = DEFAULT_ALERT_THRESHOLD) -> list:
    """Check rankings for a list of keywords."""
    results = []
    history = load_ranking_history()
    today = datetime.now().strftime("%Y-%m-%d")

    # Determine which API to use
    check_func = None
    source = "none"
    if SERPER_KEY:
        check_func = check_ranking_serper
        source = "serper"
    elif SERPAPI_KEY:
        check_func = check_ranking_serpapi
        source = "serpapi"
    elif VALUESERP_KEY:
        check_func = check_ranking_valueserp
        source = "valueserp"

    if not check_func:
        log("WARNING: No SERP API key configured.")
        log("Set SERPER_API_KEY (recommended, 2500 free), SERPAPI_KEY, or VALUESERP_KEY.")
        log("Running in demo mode - will create history template.")

        # Demo mode: create template entries
        for keyword in keywords:
            entry = {
                "date": today,
                "keyword": keyword,
                "position": "NOT_CHECKED",
                "url": "",
                "title": "",
                "domain": "",
                "previous_position": "",
                "position_change": "0",
                "source": "demo",
            }
            save_ranking_entry(entry)
            results.append(entry)

        log(f"Demo entries created for {len(keywords)} keywords.")
        return results

    for i, keyword in enumerate(keywords):
        log(f"[{i+1}/{len(keywords)}] Checking: {keyword}")

        serp_results = check_func(keyword)
        our_result = find_our_position(serp_results)

        # Get previous ranking
        prev = history.get(keyword, {})
        prev_position = prev.get("position", "")

        if our_result:
            position = our_result["position"]
            position_change = 0
            if prev_position and prev_position.isdigit():
                position_change = int(prev_position) - position  # positive = improved

            entry = {
                "date": today,
                "keyword": keyword,
                "position": str(position),
                "url": our_result["url"],
                "title": our_result["title"],
                "domain": our_result["domain"],
                "previous_position": str(prev_position),
                "position_change": str(position_change),
                "source": source,
            }

            # Alert on significant changes
            if abs(position_change) >= alert_threshold:
                direction = "UP" if position_change > 0 else "DOWN"
                log(f"  ALERT: {keyword} moved {direction} {abs(position_change)} positions "
                    f"({prev_position} -> {position})")
        else:
            entry = {
                "date": today,
                "keyword": keyword,
                "position": f">{CHECK_DEPTH}",
                "url": "",
                "title": "",
                "domain": "",
                "previous_position": str(prev_position),
                "position_change": "dropped" if prev_position and prev_position.isdigit() else "not_ranked",
                "source": source,
            }

            if prev_position and prev_position.isdigit():
                log(f"  ALERT: {keyword} dropped out of top {CHECK_DEPTH} (was #{prev_position})")

        save_ranking_entry(entry)
        results.append(entry)
        time.sleep(2)  # Rate limiting between requests

    return results


def generate_report(days: int = 30) -> str:
    """Generate ranking report from historical data."""
    if not RANKINGS_CSV.exists():
        return "No ranking data found. Run `python3 track_rankings.py` first."

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    entries = []

    with open(RANKINGS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("date", "") >= cutoff:
                entries.append(row)

    if not entries:
        return f"No ranking data in the last {days} days."

    # Build report
    lines = [
        f"# SEO Rankings Report",
        f"**Period:** Last {days} days (since {cutoff})",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Keywords tracked:** {len(set(e['keyword'] for e in entries))}",
        "",
    ]

    # Latest positions
    latest = {}
    for e in entries:
        kw = e["keyword"]
        if kw not in latest or e["date"] > latest[kw]["date"]:
            latest[kw] = e

    # Ranked keywords
    ranked = {k: v for k, v in latest.items() if v["position"].isdigit()}
    unranked = {k: v for k, v in latest.items() if not v["position"].isdigit()}

    if ranked:
        lines.append("## Currently Ranking")
        lines.append("| Keyword | Position | Change | URL |")
        lines.append("|---------|----------|--------|-----|")
        for kw, data in sorted(ranked.items(), key=lambda x: int(x[1]["position"])):
            change = data.get("position_change", "0")
            change_str = ""
            try:
                c = int(change)
                if c > 0:
                    change_str = f"+{c}"
                elif c < 0:
                    change_str = str(c)
                else:
                    change_str = "="
            except ValueError:
                change_str = change
            lines.append(f"| {kw[:50]} | #{data['position']} | {change_str} | {data.get('url', '')[:60]} |")
        lines.append("")

    if unranked:
        lines.append("## Not Ranking (Below Top 30)")
        for kw in sorted(unranked.keys()):
            lines.append(f"- {kw}")
        lines.append("")

    # Alerts (significant movers)
    movers = []
    for e in entries:
        try:
            change = int(e.get("position_change", "0"))
            if abs(change) >= 3:
                movers.append(e)
        except ValueError:
            pass

    if movers:
        lines.append("## Significant Movers")
        for m in sorted(movers, key=lambda x: abs(int(x.get("position_change", "0"))), reverse=True)[:10]:
            change = int(m["position_change"])
            direction = "UP" if change > 0 else "DOWN"
            lines.append(f"- {m['keyword'][:50]}: {direction} {abs(change)} positions on {m['date']}")
        lines.append("")

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PRINTMAXX SEO Monitoring")
    parser.add_argument("--keywords", help="Comma-separated keywords to track")
    parser.add_argument("--from-csv", dest="from_csv", help="Load keywords from CSV file")
    parser.add_argument("--from-slugs", action="store_true",
                        help="Load keywords from GEO_LONGTAIL_SLUGS_300.csv")
    parser.add_argument("--report", action="store_true", help="Generate ranking report")
    parser.add_argument("--days", type=int, default=30, help="Report period in days")
    parser.add_argument("--alert-threshold", type=int, default=DEFAULT_ALERT_THRESHOLD,
                        help=f"Alert on position changes >= N (default: {DEFAULT_ALERT_THRESHOLD})")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of keywords to check")
    args = parser.parse_args()

    log("PRINTMAXX SEO Monitoring starting")

    if args.report:
        report = generate_report(args.days)
        print(report)

        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_file = REPORT_DIR / f"seo_report_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.write_text(report, encoding="utf-8")
        log(f"Report saved to {report_file}")
        return

    # Load keywords
    keywords = []

    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    elif args.from_csv:
        csv_path = Path(args.from_csv)
        if not csv_path.exists():
            log(f"CSV file not found: {csv_path}")
            sys.exit(1)
        keywords = load_keywords_from_csv(csv_path)
    elif args.from_slugs:
        keywords = load_keywords_from_slugs()
    else:
        # Default: load from slugs if available, else use default set
        keywords = load_keywords_from_slugs()
        if not keywords:
            keywords = [
                "prayer lock app",
                "faith productivity app",
                "walk to unlock app",
                "fitness lock screen app",
                "biomaxx supplement tracker",
                "AI workflow automation solopreneur",
                "best prayer timer app",
                "study lock focus app",
            ]
            log("Using default keyword set. Use --keywords or --from-slugs for custom.")

    if args.limit > 0:
        keywords = keywords[:args.limit]

    log(f"Tracking {len(keywords)} keywords")

    # Check rankings
    results = check_keywords(keywords, alert_threshold=args.alert_threshold)

    # Summary
    ranked = sum(1 for r in results if r["position"].isdigit())
    alerts = sum(1 for r in results if abs(int(r.get("position_change", "0") or "0")) >= args.alert_threshold
                 if r.get("position_change", "0").lstrip("-").isdigit())

    log("\n--- SEO MONITORING SUMMARY ---")
    log(f"Keywords checked: {len(results)}")
    log(f"Currently ranking (top {CHECK_DEPTH}): {ranked}")
    log(f"Alerts (>={args.alert_threshold} position change): {alerts}")
    log(f"History saved to: {RANKINGS_CSV}")
    log("Done.")


if __name__ == "__main__":
    main()
