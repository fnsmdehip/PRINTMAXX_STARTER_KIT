#!/usr/bin/env python3
"""
PRINTMAXX App Store Competitor Monitor
Tracks App Store listings for key competitors identified in MASTER_ALPHA_SCAN_CONSOLIDATED.md.
Uses iTunes Search API (free, no auth needed) to detect pricing changes, rating shifts, and new versions.

Competitors tracked (from 417 alpha findings):
  Faith: Hallow ($2M+/mo), Pray.com ($1.5M+/mo), Glorify, Abide
  Screen time: Opal ($600K/mo), BePresent ($300K/mo)
  Study: Gauth ($1.2M/mo), Knowunity ($460K/mo)
  Fitness: FitBod, MyFitnessPal, Streaks Workout
  Productivity: Forest, Flora, Focus Keeper
  Sleep: Sleep Cycle, Pillow, AutoSleep

Stores historical data in AUTOMATIONS/logs/competitor_history.json.
Alerts on: price change, rating drop/spike (>0.1), new version, removal.

Cron entry (daily at 7:00 AM):
  0 7 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/competitor_monitor.py --scan >> AUTOMATIONS/logs/competitor_appstore.log 2>&1

Usage:
    python3 competitor_monitor.py --scan          # Scan all competitors, detect changes
    python3 competitor_monitor.py --report         # Show latest snapshot
    python3 competitor_monitor.py --alerts         # Show only changes/alerts
    python3 competitor_monitor.py --add "App Name" # Add a competitor to track
    python3 competitor_monitor.py --history "Hallow" # Show history for one app
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "competitor_history.json"
ALERTS_FILE = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "competitor_alerts.json"
LOG_FILE = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "competitor_appstore.log"

# Competitors identified from MASTER_ALPHA_SCAN_CONSOLIDATED.md across PrintMaxx niches
COMPETITORS = {
    "faith": [
        {"name": "Hallow", "search_term": "Hallow Prayer Meditation", "est_revenue": "$2M+/mo"},
        {"name": "Pray.com", "search_term": "Pray.com Daily Prayer", "est_revenue": "$1.5M+/mo"},
        {"name": "Glorify", "search_term": "Glorify Daily Devotional", "est_revenue": "Unknown"},
        {"name": "Abide", "search_term": "Abide Bible Meditation", "est_revenue": "Unknown"},
    ],
    "screen_time": [
        {"name": "Opal", "search_term": "Opal Screen Time", "est_revenue": "$600K/mo"},
        {"name": "BePresent", "search_term": "BePresent Screen Time", "est_revenue": "$300K/mo"},
        {"name": "one sec", "search_term": "one sec screen time", "est_revenue": "Unknown"},
    ],
    "study": [
        {"name": "Gauth", "search_term": "Gauth AI Study", "est_revenue": "$1.2M/mo"},
        {"name": "Knowunity", "search_term": "Knowunity Study", "est_revenue": "$460K/mo"},
        {"name": "Quizlet", "search_term": "Quizlet Flashcards", "est_revenue": "Unknown"},
    ],
    "fitness": [
        {"name": "FitBod", "search_term": "Fitbod Workout", "est_revenue": "Unknown"},
        {"name": "Streaks Workout", "search_term": "Streaks Workout", "est_revenue": "Unknown"},
        {"name": "StepBet", "search_term": "StepBet Walking", "est_revenue": "Unknown"},
    ],
    "productivity": [
        {"name": "Forest", "search_term": "Forest Focus Timer", "est_revenue": "Unknown"},
        {"name": "Flora", "search_term": "Flora Focus Timer", "est_revenue": "Unknown"},
        {"name": "Focus Keeper", "search_term": "Focus Keeper Timer", "est_revenue": "Unknown"},
    ],
    "sleep": [
        {"name": "Sleep Cycle", "search_term": "Sleep Cycle alarm", "est_revenue": "Unknown"},
        {"name": "Pillow", "search_term": "Pillow Sleep Tracker", "est_revenue": "Unknown"},
        {"name": "AutoSleep", "search_term": "AutoSleep Track Sleep", "est_revenue": "Unknown"},
    ],
}


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def load_alerts():
    if ALERTS_FILE.exists():
        try:
            with open(ALERTS_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_alerts(alerts):
    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=2)


def fetch_app_store(search_term, country="us", limit=3):
    """Query iTunes Search API for an app. Returns list of results."""
    import urllib.parse
    encoded = urllib.parse.quote(search_term)
    url = f"https://itunes.apple.com/search?term={encoded}&entity=software&country={country}&limit={limit}"
    req = Request(url, headers={"User-Agent": "PrintMaxx-CompetitorMonitor/1.0"})
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("results", [])
    except (URLError, HTTPError, json.JSONDecodeError) as e:
        log(f"ERROR fetching '{search_term}': {e}")
        return []


def extract_app_data(result):
    """Extract relevant fields from iTunes API result."""
    return {
        "trackId": result.get("trackId"),
        "trackName": result.get("trackName", ""),
        "bundleId": result.get("bundleId", ""),
        "price": result.get("price", 0),
        "formattedPrice": result.get("formattedPrice", "Free"),
        "averageUserRating": round(result.get("averageUserRating", 0), 2),
        "userRatingCount": result.get("userRatingCount", 0),
        "version": result.get("version", ""),
        "currentVersionReleaseDate": result.get("currentVersionReleaseDate", ""),
        "releaseNotes": (result.get("releaseNotes", "") or "")[:500],
        "primaryGenreName": result.get("primaryGenreName", ""),
        "contentAdvisoryRating": result.get("contentAdvisoryRating", ""),
        "sellerName": result.get("sellerName", ""),
        "minimumOsVersion": result.get("minimumOsVersion", ""),
        "fileSizeBytes": result.get("fileSizeBytes", "0"),
        "screenshotUrls": result.get("screenshotUrls", [])[:3],
        "description": (result.get("description", "") or "")[:300],
    }


def find_best_match(results, target_name):
    """Find the result whose trackName best matches the target competitor name."""
    if not results:
        return None
    target_lower = target_name.lower()
    # exact or startswith match first
    for r in results:
        name = r.get("trackName", "").lower()
        if target_lower in name or name.startswith(target_lower):
            return r
    # fallback to first result
    return results[0]


def detect_changes(app_name, current, previous):
    """Compare current snapshot to previous and return list of alert dicts."""
    alerts = []
    ts = datetime.now().isoformat()

    if not previous:
        return [{"type": "NEW_TRACKING", "app": app_name, "message": f"Started tracking {app_name}", "timestamp": ts}]

    # Price change
    old_price = previous.get("price", 0)
    new_price = current.get("price", 0)
    if old_price != new_price:
        direction = "increased" if new_price > old_price else "decreased"
        alerts.append({
            "type": "PRICE_CHANGE",
            "app": app_name,
            "message": f"{app_name} price {direction}: {previous.get('formattedPrice', '?')} -> {current.get('formattedPrice', '?')}",
            "old_value": old_price,
            "new_value": new_price,
            "timestamp": ts,
        })

    # Rating change (threshold: 0.1)
    old_rating = previous.get("averageUserRating", 0)
    new_rating = current.get("averageUserRating", 0)
    if abs(new_rating - old_rating) >= 0.1:
        direction = "up" if new_rating > old_rating else "down"
        alerts.append({
            "type": "RATING_CHANGE",
            "app": app_name,
            "message": f"{app_name} rating {direction}: {old_rating} -> {new_rating}",
            "old_value": old_rating,
            "new_value": new_rating,
            "timestamp": ts,
        })

    # Rating count spike (>10% increase)
    old_count = previous.get("userRatingCount", 0)
    new_count = current.get("userRatingCount", 0)
    if old_count > 0 and new_count > old_count:
        pct_increase = (new_count - old_count) / old_count * 100
        if pct_increase >= 10:
            alerts.append({
                "type": "RATING_COUNT_SPIKE",
                "app": app_name,
                "message": f"{app_name} rating count +{pct_increase:.0f}%: {old_count:,} -> {new_count:,}",
                "old_value": old_count,
                "new_value": new_count,
                "timestamp": ts,
            })

    # New version
    old_version = previous.get("version", "")
    new_version = current.get("version", "")
    if old_version and new_version and old_version != new_version:
        notes_preview = current.get("releaseNotes", "")[:200]
        alerts.append({
            "type": "NEW_VERSION",
            "app": app_name,
            "message": f"{app_name} updated: v{old_version} -> v{new_version}",
            "old_value": old_version,
            "new_value": new_version,
            "release_notes": notes_preview,
            "timestamp": ts,
        })

    return alerts


def scan_all(history, extra_apps=None):
    """Scan all competitors and return (updated_history, all_alerts)."""
    all_alerts = []
    scan_ts = datetime.now().isoformat()

    all_apps = []
    for niche, apps in COMPETITORS.items():
        for app in apps:
            all_apps.append((niche, app))

    # Add any extra tracked apps
    if extra_apps:
        for app in extra_apps:
            all_apps.append(("custom", app))

    total = len(all_apps)
    log(f"Scanning {total} competitor apps across {len(COMPETITORS)} niches...")

    for i, (niche, app) in enumerate(all_apps, 1):
        name = app["name"]
        search_term = app["search_term"]
        log(f"  [{i}/{total}] {name} ({niche})")

        results = fetch_app_store(search_term)
        if not results:
            log(f"    No results found for '{search_term}'")
            time.sleep(1)
            continue

        best = find_best_match(results, name)
        if not best:
            log(f"    No match for '{name}'")
            time.sleep(1)
            continue

        current = extract_app_data(best)
        current["niche"] = niche
        current["est_revenue"] = app.get("est_revenue", "Unknown")
        current["scan_timestamp"] = scan_ts

        # Get previous snapshot
        app_key = name.lower().replace(" ", "_")
        prev_data = None
        if app_key in history:
            snapshots = history[app_key].get("snapshots", [])
            if snapshots:
                prev_data = snapshots[-1]

        # Detect changes
        changes = detect_changes(name, current, prev_data)
        all_alerts.extend(changes)

        # Store in history
        if app_key not in history:
            history[app_key] = {"name": name, "niche": niche, "snapshots": []}
        history[app_key]["snapshots"].append(current)

        # Keep last 90 snapshots (about 3 months daily)
        if len(history[app_key]["snapshots"]) > 90:
            history[app_key]["snapshots"] = history[app_key]["snapshots"][-90:]

        for c in changes:
            if c["type"] != "NEW_TRACKING":
                log(f"    ALERT: {c['message']}")

        # Rate limit: 1 request per second to be polite to Apple
        time.sleep(1)

    log(f"Scan complete. {len(all_alerts)} alerts generated.")
    return history, all_alerts


def print_report(history):
    """Print latest snapshot for all tracked apps."""
    if not history:
        print("No history data. Run --scan first.")
        return

    print(f"\n{'='*80}")
    print(f"  PRINTMAXX APP STORE COMPETITOR REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*80}\n")

    by_niche = {}
    for key, data in history.items():
        niche = data.get("niche", "unknown")
        if niche not in by_niche:
            by_niche[niche] = []
        latest = data["snapshots"][-1] if data.get("snapshots") else {}
        by_niche[niche].append((data["name"], latest))

    for niche, apps in sorted(by_niche.items()):
        print(f"--- {niche.upper().replace('_', ' ')} ---")
        for name, snap in apps:
            if not snap:
                print(f"  {name}: No data")
                continue
            price = snap.get("formattedPrice", "?")
            rating = snap.get("averageUserRating", 0)
            count = snap.get("userRatingCount", 0)
            version = snap.get("version", "?")
            est_rev = snap.get("est_revenue", "?")
            updated = snap.get("currentVersionReleaseDate", "?")[:10]
            print(f"  {name:<25} {price:<8} {rating:.1f}/5 ({count:>8,} ratings) v{version} | Updated: {updated} | Est: {est_rev}")
        print()


def print_alerts(count=20):
    """Print recent alerts."""
    alerts = load_alerts()
    if not alerts:
        print("No alerts found. Run --scan first.")
        return

    recent = alerts[-count:]
    print(f"\n{'='*80}")
    print(f"  COMPETITOR ALERTS (last {len(recent)})")
    print(f"{'='*80}\n")

    for a in reversed(recent):
        ts = a.get("timestamp", "?")[:16]
        atype = a.get("type", "?")
        msg = a.get("message", "?")
        icon = {"PRICE_CHANGE": "$", "RATING_CHANGE": "*", "NEW_VERSION": "^",
                "RATING_COUNT_SPIKE": "+", "NEW_TRACKING": ">"}
        print(f"  [{ts}] {icon.get(atype, '?')} {msg}")

    print()


def print_app_history(app_name, history):
    """Print historical snapshots for a specific app."""
    key = app_name.lower().replace(" ", "_")
    if key not in history:
        # Try partial match
        matches = [k for k in history if app_name.lower() in k]
        if matches:
            key = matches[0]
        else:
            print(f"No history found for '{app_name}'. Available: {', '.join(history.keys())}")
            return

    data = history[key]
    print(f"\n--- History for {data['name']} ({data.get('niche', '?')}) ---\n")
    print(f"  {'Date':<20} {'Price':<10} {'Rating':<8} {'Count':<12} {'Version':<10}")
    print(f"  {'-'*60}")

    for snap in data.get("snapshots", []):
        ts = snap.get("scan_timestamp", "?")[:16]
        price = snap.get("formattedPrice", "?")
        rating = snap.get("averageUserRating", 0)
        count = snap.get("userRatingCount", 0)
        version = snap.get("version", "?")
        print(f"  {ts:<20} {price:<10} {rating:<8.1f} {count:<12,} v{version}")
    print()


def add_custom_app(name, history):
    """Add a custom app to track."""
    key = name.lower().replace(" ", "_")
    if key in history:
        print(f"'{name}' is already being tracked.")
        return

    # Search for it
    results = fetch_app_store(name)
    if not results:
        print(f"No App Store results found for '{name}'.")
        return

    best = find_best_match(results, name)
    current = extract_app_data(best)
    current["niche"] = "custom"
    current["est_revenue"] = "Unknown"
    current["scan_timestamp"] = datetime.now().isoformat()

    history[key] = {
        "name": best.get("trackName", name),
        "niche": "custom",
        "snapshots": [current],
    }
    save_history(history)
    print(f"Added '{best.get('trackName', name)}' to tracking. Price: {current['formattedPrice']}, Rating: {current['averageUserRating']}")


def main():
    parser = argparse.ArgumentParser(description="PrintMaxx App Store Competitor Monitor")
    parser.add_argument("--scan", action="store_true", help="Scan all competitors and detect changes")
    parser.add_argument("--report", action="store_true", help="Show latest snapshot for all tracked apps")
    parser.add_argument("--alerts", action="store_true", help="Show recent alerts/changes")
    parser.add_argument("--history", type=str, metavar="APP_NAME", help="Show history for a specific app")
    parser.add_argument("--add", type=str, metavar="APP_NAME", help="Add a custom app to track")
    parser.add_argument("--alert-count", type=int, default=20, help="Number of alerts to show (default 20)")
    args = parser.parse_args()

    if not any([args.scan, args.report, args.alerts, args.history, args.add]):
        parser.print_help()
        return

    history = load_history()

    if args.add:
        add_custom_app(args.add, history)
        return

    if args.scan:
        # Load any custom apps from history
        custom_apps = []
        for key, data in history.items():
            if data.get("niche") == "custom":
                custom_apps.append({
                    "name": data["name"],
                    "search_term": data["name"],
                })

        history, new_alerts = scan_all(history, extra_apps=custom_apps if custom_apps else None)
        save_history(history)

        # Append new alerts
        existing_alerts = load_alerts()
        existing_alerts.extend(new_alerts)
        # Keep last 500 alerts
        if len(existing_alerts) > 500:
            existing_alerts = existing_alerts[-500:]
        save_alerts(existing_alerts)

        # Print summary
        change_alerts = [a for a in new_alerts if a["type"] != "NEW_TRACKING"]
        if change_alerts:
            print(f"\n{len(change_alerts)} CHANGES DETECTED:")
            for a in change_alerts:
                print(f"  {a['message']}")
        else:
            print("\nNo changes detected since last scan.")

        print(f"\nTracking {len(history)} apps. History saved to {HISTORY_FILE}")

    if args.report:
        print_report(history)

    if args.alerts:
        print_alerts(args.alert_count)

    if args.history:
        print_app_history(args.history, history)


if __name__ == "__main__":
    main()
