#!/usr/bin/env python3
"""
PRINTMAXX Social Metrics Collector
====================================
Collects publicly available social media metrics (follower counts, engagement)
and tracks growth over time in LEDGER/SOCIAL_METRICS.csv.

Usage:
    python3 collect_metrics.py                              # Collect all accounts
    python3 collect_metrics.py --platform x                 # X/Twitter only
    python3 collect_metrics.py --accounts "@handle1,@handle2"
    python3 collect_metrics.py --report                     # Generate growth report
    python3 collect_metrics.py --from-csv accounts.csv      # Load accounts from CSV

Environment Variables:
    TWITTER_BEARER_TOKEN   - Twitter API v2 bearer token
    RAPIDAPI_KEY           - RapidAPI key (for social media scrapers)

Note: Without API keys, the script tracks metrics from manual input.
Use --manual to enter today's metrics interactively.
"""

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SOCIAL_METRICS_CSV = PROJECT_ROOT / "LEDGER" / "SOCIAL_METRICS.csv"
ACCOUNTS_CSV = PROJECT_ROOT / "LEDGER" / "ACCOUNTS.csv"
REPORT_DIR = Path(__file__).resolve().parent / "reports"

# API keys
TWITTER_BEARER = os.environ.get("TWITTER_BEARER_TOKEN", "")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")

# Default accounts to track (our niche accounts)
DEFAULT_ACCOUNTS = [
    {"handle": "@DailyGraceQuotes", "platform": "x", "niche": "faith"},
    {"handle": "@5AMGainsClub", "platform": "x", "niche": "fitness"},
    {"handle": "@TheStackReport", "platform": "x", "niche": "ai"},
    {"handle": "@DailyGraceQuotes", "platform": "instagram", "niche": "faith"},
    {"handle": "@5AMGainsClub", "platform": "instagram", "niche": "fitness"},
    {"handle": "@TheStackReport", "platform": "instagram", "niche": "ai"},
    {"handle": "@DailyGraceQuotes", "platform": "tiktok", "niche": "faith"},
    {"handle": "@5AMGainsClub", "platform": "tiktok", "niche": "fitness"},
    {"handle": "@TheStackReport", "platform": "tiktok", "niche": "ai"},
]

METRICS_FIELDNAMES = [
    "date", "platform", "handle", "niche", "followers", "following",
    "posts_count", "avg_likes", "avg_comments", "avg_views",
    "engagement_rate", "top_post_likes", "growth_since_last",
    "source", "notes",
]


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def ensure_metrics_csv() -> None:
    """Create SOCIAL_METRICS.csv if it doesn't exist."""
    if not SOCIAL_METRICS_CSV.exists():
        SOCIAL_METRICS_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(SOCIAL_METRICS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=METRICS_FIELDNAMES)
            writer.writeheader()
        log(f"Created {SOCIAL_METRICS_CSV}")


def load_metrics_history() -> list:
    """Load all historical metrics."""
    ensure_metrics_csv()
    entries = []
    with open(SOCIAL_METRICS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return entries


def get_last_metrics(handle: str, platform: str) -> Optional[dict]:
    """Get most recent metrics for an account."""
    entries = load_metrics_history()
    latest = None
    for e in entries:
        if e.get("handle", "").lower() == handle.lower() and e.get("platform", "").lower() == platform.lower():
            if not latest or e.get("date", "") > latest.get("date", ""):
                latest = e
    return latest


def fetch_twitter_metrics(handle: str) -> Optional[dict]:
    """Fetch metrics from Twitter API v2."""
    if not TWITTER_BEARER:
        return None

    username = handle.lstrip("@")
    url = (
        f"https://api.twitter.com/2/users/by/username/{username}"
        f"?user.fields=public_metrics,description,created_at"
    )

    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TWITTER_BEARER}",
    })

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        log(f"Twitter API error for {handle}: {e}")
        return None

    if "data" not in data:
        return None

    user_data = data["data"]
    metrics = user_data.get("public_metrics", {})

    return {
        "followers": str(metrics.get("followers_count", 0)),
        "following": str(metrics.get("following_count", 0)),
        "posts_count": str(metrics.get("tweet_count", 0)),
    }


def fetch_metrics_rapidapi(handle: str, platform: str) -> Optional[dict]:
    """Fetch metrics using RapidAPI social media scrapers."""
    if not RAPIDAPI_KEY:
        return None

    username = handle.lstrip("@")

    # Different RapidAPI endpoints per platform
    if platform == "instagram":
        url = f"https://instagram-scraper-api2.p.rapidapi.com/v1/info?username_or_id_or_url={username}"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com",
        }
    elif platform == "tiktok":
        url = f"https://tiktok-scraper7.p.rapidapi.com/user/info?unique_id={username}"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com",
        }
    else:
        return None

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        log(f"RapidAPI error for {handle} on {platform}: {e}")
        return None

    if platform == "instagram":
        user_data = data.get("data", {})
        return {
            "followers": str(user_data.get("follower_count", 0)),
            "following": str(user_data.get("following_count", 0)),
            "posts_count": str(user_data.get("media_count", 0)),
        }
    elif platform == "tiktok":
        user_info = data.get("data", {}).get("user", {})
        stats = data.get("data", {}).get("stats", {})
        return {
            "followers": str(stats.get("followerCount", 0)),
            "following": str(stats.get("followingCount", 0)),
            "posts_count": str(stats.get("videoCount", 0)),
        }

    return None


def collect_account_metrics(handle: str, platform: str, niche: str = "") -> dict:
    """Collect metrics for a single account."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Try APIs
    api_data = None
    source = "manual"

    if platform == "x":
        api_data = fetch_twitter_metrics(handle)
        if api_data:
            source = "twitter_api"
    elif platform in ("instagram", "tiktok"):
        api_data = fetch_metrics_rapidapi(handle, platform)
        if api_data:
            source = "rapidapi"

    # Build entry
    entry = {
        "date": today,
        "platform": platform,
        "handle": handle,
        "niche": niche,
        "followers": api_data.get("followers", "0") if api_data else "0",
        "following": api_data.get("following", "0") if api_data else "0",
        "posts_count": api_data.get("posts_count", "0") if api_data else "0",
        "avg_likes": "0",
        "avg_comments": "0",
        "avg_views": "0",
        "engagement_rate": "0.0",
        "top_post_likes": "0",
        "growth_since_last": "0",
        "source": source,
        "notes": "",
    }

    # Calculate growth since last
    last = get_last_metrics(handle, platform)
    if last:
        try:
            current_followers = int(entry["followers"])
            previous_followers = int(last.get("followers", "0"))
            growth = current_followers - previous_followers
            entry["growth_since_last"] = str(growth)
        except ValueError:
            pass

    return entry


def save_metrics_entry(entry: dict) -> None:
    """Append metrics entry to CSV."""
    ensure_metrics_csv()
    with open(SOCIAL_METRICS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=METRICS_FIELDNAMES)
        writer.writerow(entry)


def manual_input_mode(accounts: list) -> None:
    """Interactive mode for manual metrics entry."""
    today = datetime.now().strftime("%Y-%m-%d")
    log("Manual metrics entry mode. Enter current numbers for each account.")
    log("Press Enter to skip, type 'q' to quit.\n")

    for account in accounts:
        handle = account["handle"]
        platform = account["platform"]
        niche = account.get("niche", "")

        print(f"\n--- {handle} ({platform}) ---")
        last = get_last_metrics(handle, platform)
        if last:
            print(f"  Last recorded: {last.get('date', '?')} - "
                  f"{last.get('followers', '?')} followers")

        followers = input(f"  Followers: ").strip()
        if followers.lower() == "q":
            break
        if not followers:
            continue

        following = input(f"  Following: ").strip() or "0"
        posts_count = input(f"  Posts: ").strip() or "0"
        avg_likes = input(f"  Avg likes/post: ").strip() or "0"

        try:
            current = int(followers)
            previous = int(last.get("followers", "0")) if last else 0
            growth = current - previous
        except ValueError:
            growth = 0

        entry = {
            "date": today,
            "platform": platform,
            "handle": handle,
            "niche": niche,
            "followers": followers,
            "following": following,
            "posts_count": posts_count,
            "avg_likes": avg_likes,
            "avg_comments": "0",
            "avg_views": "0",
            "engagement_rate": "0.0",
            "top_post_likes": "0",
            "growth_since_last": str(growth),
            "source": "manual",
            "notes": "",
        }

        save_metrics_entry(entry)
        log(f"  Saved: {handle} on {platform} ({followers} followers, +{growth})")


def generate_growth_report(days: int = 30) -> str:
    """Generate growth report from historical data."""
    entries = load_metrics_history()
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [e for e in entries if e.get("date", "") >= cutoff]

    if not recent:
        return f"No metrics data in the last {days} days."

    lines = [
        f"# Social Metrics Growth Report",
        f"**Period:** Last {days} days (since {cutoff})",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    # Group by handle+platform
    accounts = {}
    for e in recent:
        key = f"{e['handle']}_{e['platform']}"
        if key not in accounts:
            accounts[key] = []
        accounts[key].append(e)

    for key, metrics in sorted(accounts.items()):
        if not metrics:
            continue

        # Sort by date
        metrics.sort(key=lambda x: x.get("date", ""))
        first = metrics[0]
        last = metrics[-1]

        handle = last["handle"]
        platform = last["platform"]
        niche = last.get("niche", "")

        lines.append(f"## {handle} ({platform})")
        if niche:
            lines.append(f"**Niche:** {niche}")

        try:
            start_followers = int(first.get("followers", 0))
            end_followers = int(last.get("followers", 0))
            growth = end_followers - start_followers
            growth_pct = (growth / max(start_followers, 1)) * 100

            lines.append(f"- Current followers: {end_followers:,}")
            lines.append(f"- Period growth: {growth:+,} ({growth_pct:+.1f}%)")
            lines.append(f"- Start ({first['date']}): {start_followers:,}")
            lines.append(f"- Posts: {last.get('posts_count', 'N/A')}")
            lines.append(f"- Avg likes: {last.get('avg_likes', 'N/A')}")
        except ValueError:
            lines.append(f"- Latest data: {last.get('followers', 'N/A')} followers")

        # Daily growth rate
        if len(metrics) >= 2:
            try:
                date_diff = (datetime.strptime(last["date"], "%Y-%m-%d") -
                             datetime.strptime(first["date"], "%Y-%m-%d")).days
                if date_diff > 0:
                    daily_growth = growth / date_diff
                    lines.append(f"- Daily growth rate: {daily_growth:+.1f} followers/day")
                    projected_30d = end_followers + int(daily_growth * 30)
                    lines.append(f"- Projected 30-day: {projected_30d:,} followers")
            except (ValueError, ZeroDivisionError):
                pass

        lines.append("")

    # Overall summary
    total_followers = 0
    total_growth = 0
    for metrics in accounts.values():
        if metrics:
            last = metrics[-1]
            try:
                total_followers += int(last.get("followers", 0))
                total_growth += int(last.get("growth_since_last", 0))
            except ValueError:
                pass

    lines.append("## Overall Summary")
    lines.append(f"- Total followers across all platforms: {total_followers:,}")
    lines.append(f"- Total recent growth: {total_growth:+,}")
    lines.append(f"- Accounts tracked: {len(accounts)}")

    return "\n".join(lines)


def load_accounts(source: str = "default") -> list:
    """Load accounts to track."""
    if source == "default":
        return DEFAULT_ACCOUNTS

    # Try loading from LEDGER/ACCOUNTS.csv
    if ACCOUNTS_CSV.exists():
        accounts = []
        with open(ACCOUNTS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                handle = row.get("handle", row.get("username", ""))
                platform = row.get("platform", "x")
                niche = row.get("niche", "")
                if handle:
                    accounts.append({
                        "handle": handle if handle.startswith("@") else f"@{handle}",
                        "platform": platform.lower(),
                        "niche": niche,
                    })
        if accounts:
            return accounts

    return DEFAULT_ACCOUNTS


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PRINTMAXX Social Metrics Collector")
    parser.add_argument("--platform", choices=["x", "instagram", "tiktok", "all"],
                        default="all", help="Platform to collect from")
    parser.add_argument("--accounts", help="Comma-separated handles to track")
    parser.add_argument("--from-csv", dest="from_csv", help="Load accounts from CSV")
    parser.add_argument("--manual", action="store_true", help="Manual entry mode")
    parser.add_argument("--report", action="store_true", help="Generate growth report")
    parser.add_argument("--days", type=int, default=30, help="Report period in days")
    args = parser.parse_args()

    log("PRINTMAXX Social Metrics Collector starting")

    if args.report:
        report = generate_growth_report(args.days)
        print(report)

        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_file = REPORT_DIR / f"social_report_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.write_text(report, encoding="utf-8")
        log(f"Report saved to {report_file}")
        return

    # Load accounts
    if args.accounts:
        accounts = []
        for handle in args.accounts.split(","):
            handle = handle.strip()
            if handle:
                accounts.append({
                    "handle": handle if handle.startswith("@") else f"@{handle}",
                    "platform": args.platform if args.platform != "all" else "x",
                    "niche": "",
                })
    elif args.from_csv:
        csv_path = Path(args.from_csv)
        if not csv_path.exists():
            log(f"CSV not found: {csv_path}")
            sys.exit(1)
        accounts = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                handle = row.get("handle", row.get("username", ""))
                if handle:
                    accounts.append({
                        "handle": handle,
                        "platform": row.get("platform", "x"),
                        "niche": row.get("niche", ""),
                    })
    else:
        accounts = load_accounts()

    # Filter by platform
    if args.platform != "all":
        accounts = [a for a in accounts if a["platform"] == args.platform]

    log(f"Tracking {len(accounts)} accounts")

    if args.manual:
        manual_input_mode(accounts)
        return

    # Automatic collection
    collected = 0
    for account in accounts:
        handle = account["handle"]
        platform = account["platform"]
        niche = account.get("niche", "")

        log(f"Collecting: {handle} ({platform})")
        entry = collect_account_metrics(handle, platform, niche)

        if entry["source"] != "manual":
            save_metrics_entry(entry)
            collected += 1
            log(f"  {entry['followers']} followers (growth: {entry['growth_since_last']})")
        else:
            log(f"  No API data available. Use --manual for manual entry.")

        time.sleep(1)

    log(f"\n--- COLLECTION SUMMARY ---")
    log(f"Accounts processed: {len(accounts)}")
    log(f"Metrics collected via API: {collected}")
    if collected < len(accounts):
        log(f"Accounts needing manual entry: {len(accounts) - collected}")
        log(f"Run with --manual flag for interactive entry.")
    log(f"Data saved to: {SOCIAL_METRICS_CSV}")
    log("Done.")


if __name__ == "__main__":
    main()
