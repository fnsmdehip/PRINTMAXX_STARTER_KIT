#!/usr/bin/env python3

from __future__ import annotations
"""
Competitor Price & Page Monitor (Visualping Alternative)
Source: @pipelineabuser tweet - "I monitor 200+ websites and get alerts when anything changes"
Also: ALPHA319 - Visualping competitor monitoring

Free alternative to Visualping ($5-50/mo). Monitors competitor pages for changes.
Stores page snapshots, detects diffs, outputs alerts.

Usage:
    python3 competitor_price_monitor.py                     # Run all monitors
    python3 competitor_price_monitor.py --add "https://example.com/pricing"
    python3 competitor_price_monitor.py --list               # List monitored URLs
    python3 competitor_price_monitor.py --report              # Show changes detected
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import difflib
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

BASE_DIR = Path(__file__).parent.parent
URLS_FILE = BASE_DIR / "AUTOMATIONS" / "monitor_urls.json"
SNAPSHOTS_DIR = BASE_DIR / "AUTOMATIONS" / "snapshots"
CHANGES_CSV = BASE_DIR / "LEDGER" / "COMPETITOR_CHANGES.csv"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "competitor_monitor.log"

# Default URLs to monitor (customize)
DEFAULT_URLS = [
    # SaaS pricing pages
    {"url": "https://vercel.com/pricing", "name": "Vercel Pricing", "category": "hosting"},
    {"url": "https://render.com/pricing", "name": "Render Pricing", "category": "hosting"},
    {"url": "https://railway.app/pricing", "name": "Railway Pricing", "category": "hosting"},
    {"url": "https://supabase.com/pricing", "name": "Supabase Pricing", "category": "database"},
    {"url": "https://planetscale.com/pricing", "name": "PlanetScale Pricing", "category": "database"},
    {"url": "https://webflow.com/pricing", "name": "Webflow Pricing", "category": "website_builder"},
    {"url": "https://carrd.co/#pricing", "name": "Carrd Pricing", "category": "website_builder"},
    # Tool comparison pages
    {"url": "https://www.producthunt.com/topics/ai", "name": "PH AI Topics", "category": "trends"},
    # Competitor changelogs
    {"url": "https://github.com/trending", "name": "GitHub Trending", "category": "trends"},
]


class HTMLTextExtractor(HTMLParser):
    """Strip HTML tags and extract text content."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.skip_tags = {"script", "style", "noscript", "head"}
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            text = data.strip()
            if text:
                self.result.append(text)

    def get_text(self):
        return "\n".join(self.result)


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")


def load_urls():
    """Load monitored URLs from config."""
    if URLS_FILE.exists():
        with open(URLS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_URLS


def save_urls(urls):
    """Save monitored URLs to config."""
    URLS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(URLS_FILE, "w") as f:
        json.dump(urls, f, indent=2)


def fetch_page(url):
    """Fetch a page and return its text content."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")
            # Extract text from HTML
            extractor = HTMLTextExtractor()
            extractor.feed(html)
            return extractor.get_text()
    except Exception as e:
        log(f"Fetch error: {url} - {e}")
        return None


def get_snapshot_path(url):
    """Get file path for a URL snapshot."""
    url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
    return SNAPSHOTS_DIR / f"{url_hash}.txt"


def save_snapshot(url, content):
    """Save page content snapshot."""
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    path = get_snapshot_path(url)
    with open(path, "w") as f:
        f.write(content)
    return path


def load_snapshot(url):
    """Load previous snapshot."""
    path = get_snapshot_path(url)
    if path.exists():
        with open(path, "r") as f:
            return f.read()
    return None


def compute_diff(old_content, new_content):
    """Compute meaningful diff between two page versions."""
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    differ = difflib.unified_diff(old_lines, new_lines, lineterm="")
    diff_lines = list(differ)

    added = [l[1:] for l in diff_lines if l.startswith("+") and not l.startswith("+++")]
    removed = [l[1:] for l in diff_lines if l.startswith("-") and not l.startswith("---")]

    # Filter out trivial changes (dates, timestamps, random IDs)
    meaningful_added = [l for l in added if len(l.strip()) > 10 and not re.match(r"^\d{4}-\d{2}", l.strip())]
    meaningful_removed = [l for l in removed if len(l.strip()) > 10 and not re.match(r"^\d{4}-\d{2}", l.strip())]

    # Check for price changes specifically
    price_pattern = r"\$[\d,]+(?:\.\d{2})?(?:/mo|/month|/yr|/year)?"
    old_prices = set(re.findall(price_pattern, old_content))
    new_prices = set(re.findall(price_pattern, new_content))
    price_changes = new_prices - old_prices

    return {
        "added_lines": meaningful_added[:20],
        "removed_lines": meaningful_removed[:20],
        "total_changes": len(meaningful_added) + len(meaningful_removed),
        "price_changes": list(price_changes),
        "has_price_change": len(price_changes) > 0,
    }


def save_change(entry):
    """Save detected change to CSV."""
    CHANGES_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = CHANGES_CSV.exists()

    fieldnames = [
        "change_id",
        "url",
        "name",
        "category",
        "change_type",
        "summary",
        "added_lines",
        "removed_lines",
        "price_changes",
        "total_changes",
        "detected_date",
        "status",
        "action_taken",
    ]

    with open(CHANGES_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)


def monitor_all():
    """Run monitoring on all tracked URLs."""
    urls = load_urls()
    changes_detected = []

    log(f"Monitoring {len(urls)} URLs...")

    for i, url_entry in enumerate(urls):
        url = url_entry["url"]
        name = url_entry.get("name", url)
        category = url_entry.get("category", "")

        log(f"  [{i+1}/{len(urls)}] {name}...")

        new_content = fetch_page(url)
        if not new_content:
            continue

        old_content = load_snapshot(url)

        if old_content is None:
            # First time seeing this page
            save_snapshot(url, new_content)
            log(f"    First snapshot saved ({len(new_content)} chars)")
            continue

        # Compute diff
        diff = compute_diff(old_content, new_content)

        if diff["total_changes"] > 0:
            change_type = "PRICE_CHANGE" if diff["has_price_change"] else "CONTENT_CHANGE"
            summary_parts = []
            if diff["has_price_change"]:
                summary_parts.append(f"Price changes: {', '.join(diff['price_changes'])}")
            summary_parts.append(f"{len(diff['added_lines'])} lines added, {len(diff['removed_lines'])} removed")

            change_entry = {
                "change_id": f"CHG_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i:03d}",
                "url": url,
                "name": name,
                "category": category,
                "change_type": change_type,
                "summary": "; ".join(summary_parts),
                "added_lines": " | ".join(diff["added_lines"][:5]),
                "removed_lines": " | ".join(diff["removed_lines"][:5]),
                "price_changes": ", ".join(diff["price_changes"]),
                "total_changes": diff["total_changes"],
                "detected_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "NEW",
                "action_taken": "",
            }

            save_change(change_entry)
            changes_detected.append(change_entry)
            log(f"    CHANGE DETECTED: {change_type} - {summary_parts[0]}")
        else:
            log(f"    No changes")

        # Update snapshot
        save_snapshot(url, new_content)

    return changes_detected


def add_url(url, name=None, category=""):
    """Add a URL to the monitoring list."""
    urls = load_urls()
    # Check for duplicates
    existing_urls = [u["url"] for u in urls]
    if url in existing_urls:
        print(f"URL already monitored: {url}")
        return

    urls.append({
        "url": url,
        "name": name or url,
        "category": category,
    })
    save_urls(urls)
    print(f"Added: {url} ({name or 'unnamed'})")

    # Take first snapshot
    content = fetch_page(url)
    if content:
        save_snapshot(url, content)
        print(f"First snapshot saved ({len(content)} chars)")


def main():
    parser = argparse.ArgumentParser(description="Competitor Price & Page Monitor")
    parser.add_argument("--add", type=str, help="Add URL to monitor")
    parser.add_argument("--name", type=str, help="Name for added URL")
    parser.add_argument("--category", type=str, default="", help="Category for added URL")
    parser.add_argument("--list", action="store_true", help="List monitored URLs")
    parser.add_argument("--report", action="store_true", help="Show detected changes")
    parser.add_argument("--init", action="store_true", help="Initialize with default URLs")
    args = parser.parse_args()

    if args.add:
        add_url(args.add, args.name, args.category)
        return

    if args.init:
        save_urls(DEFAULT_URLS)
        print(f"Initialized with {len(DEFAULT_URLS)} URLs")
        print("Taking first snapshots...")
        for entry in DEFAULT_URLS:
            content = fetch_page(entry["url"])
            if content:
                save_snapshot(entry["url"], content)
                print(f"  Snapshot: {entry['name']} ({len(content)} chars)")
        return

    if args.list:
        urls = load_urls()
        print(f"\n{'='*60}")
        print(f"MONITORED URLs ({len(urls)})")
        print(f"{'='*60}")
        for i, entry in enumerate(urls):
            has_snapshot = "Y" if get_snapshot_path(entry["url"]).exists() else "N"
            print(f"  {i+1}. [{has_snapshot}] {entry.get('name', entry['url'])} [{entry.get('category', '')}]")
            print(f"     {entry['url']}")
        return

    if args.report:
        if CHANGES_CSV.exists():
            with open(CHANGES_CSV, "r") as f:
                reader = list(csv.DictReader(f))
                print(f"\n{'='*60}")
                print(f"COMPETITOR CHANGES REPORT ({len(reader)} changes)")
                print(f"{'='*60}")
                for row in reader[-20:]:  # Last 20 changes
                    print(f"\n  [{row.get('change_type', '')}] {row.get('name', '')}")
                    print(f"  Date: {row.get('detected_date', '')}")
                    print(f"  Summary: {row.get('summary', '')}")
                    if row.get("price_changes"):
                        print(f"  PRICES: {row['price_changes']}")
        else:
            print("No changes detected yet. Run monitor first.")
        return

    # Default: run monitoring
    print(f"\n{'='*60}")
    print(f"COMPETITOR PRICE & PAGE MONITOR")
    print(f"Source: @pipelineabuser - 'I monitor 200+ websites'")
    print(f"{'='*60}")

    # Initialize if needed
    if not URLS_FILE.exists():
        save_urls(DEFAULT_URLS)

    changes = monitor_all()

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Changes detected: {len(changes)}")
    if changes:
        for change in changes:
            print(f"  [{change['change_type']}] {change['name']}: {change['summary']}")
    print(f"\nOutput: {CHANGES_CSV}")
    print(f"\nRun daily: add to crontab:")
    print(f"  0 8 * * * cd {BASE_DIR} && python3 AUTOMATIONS/competitor_price_monitor.py >> AUTOMATIONS/logs/competitor_monitor.log 2>&1")


if __name__ == "__main__":
    main()
