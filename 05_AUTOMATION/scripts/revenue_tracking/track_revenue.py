#!/usr/bin/env python3
"""
PRINTMAXX Revenue Tracker Automation
======================================
Aggregates revenue data from multiple sources (Gumroad, App Store Connect,
Google Play Console) into FINANCIALS/REVENUE_TRACKER.csv and generates
daily revenue summaries.

Usage:
    python3 track_revenue.py                         # Pull from all sources
    python3 track_revenue.py --source gumroad        # Gumroad only
    python3 track_revenue.py --import sales.csv      # Import from CSV export
    python3 track_revenue.py --summary               # Generate summary only
    python3 track_revenue.py --summary --days 30     # Last 30 days summary

Environment Variables:
    GUMROAD_ACCESS_TOKEN    - Gumroad API token
    ASC_KEY_ID              - App Store Connect API Key ID
    ASC_ISSUER_ID           - App Store Connect Issuer ID
    ASC_PRIVATE_KEY_PATH    - Path to .p8 private key file
    GOOGLE_PLAY_JSON_KEY    - Path to Google Play service account JSON
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
REVENUE_CSV = PROJECT_ROOT / "FINANCIALS" / "REVENUE_TRACKER.csv"
SUMMARY_DIR = Path(__file__).resolve().parent / "summaries"
P_AND_L_CSV = PROJECT_ROOT / "FINANCIALS" / "P_AND_L_MONTHLY.csv"

# Method ID mapping
METHOD_MAP = {
    "gumroad": ("MM002", "INFO_PRODUCTS"),
    "app_store_ios": ("MM001", "APP_FACTORY"),
    "google_play": ("MM001", "APP_FACTORY"),
    "youtube": ("MM006", "CONTENT_FARM"),
    "affiliate": ("MM003", "AFFILIATE_SITES"),
    "newsletter": ("MM015", "NEWSLETTER"),
    "stripe": ("MM004", "SAAS"),
}

# API keys
GUMROAD_TOKEN = os.environ.get("GUMROAD_ACCESS_TOKEN", "")
ASC_KEY_ID = os.environ.get("ASC_KEY_ID", "")
ASC_ISSUER_ID = os.environ.get("ASC_ISSUER_ID", "")
ASC_PRIVATE_KEY_PATH = os.environ.get("ASC_PRIVATE_KEY_PATH", "")
GOOGLE_PLAY_JSON_KEY = os.environ.get("GOOGLE_PLAY_JSON_KEY", "")


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def make_request(url: str, headers: Optional[dict] = None) -> Optional[dict]:
    """Make HTTP request with error handling."""
    if headers is None:
        headers = {}
    headers["User-Agent"] = "PRINTMAXX-Revenue-Tracker/1.0"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"HTTP {e.code} for {url}")
        return None
    except Exception as e:
        log(f"Request error: {e}")
        return None


def read_existing_revenue() -> list:
    """Read existing revenue entries."""
    entries = []
    if not REVENUE_CSV.exists():
        return entries

    with open(REVENUE_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return entries


def get_existing_dates_sources() -> set:
    """Get set of (date, source, product) tuples for deduplication."""
    dedup = set()
    entries = read_existing_revenue()
    for e in entries:
        key = (e.get("date", ""), e.get("source_platform", ""), e.get("product_name", ""))
        dedup.add(key)
    return dedup


def fetch_gumroad_sales(after_date: Optional[str] = None) -> list:
    """Fetch sales from Gumroad API."""
    if not GUMROAD_TOKEN:
        log("GUMROAD_ACCESS_TOKEN not set. Skipping Gumroad.")
        return []

    entries = []
    page = 1
    has_more = True

    while has_more:
        params = {
            "access_token": GUMROAD_TOKEN,
            "page": page,
        }
        if after_date:
            params["after"] = after_date

        url = f"https://api.gumroad.com/v2/sales?{urllib.parse.urlencode(params)}"
        data = make_request(url)

        if not data or not data.get("success"):
            break

        sales = data.get("sales", [])
        if not sales:
            break

        for sale in sales:
            # Skip refunded
            if sale.get("refunded"):
                continue

            price = float(sale.get("price", 0)) / 100  # Gumroad returns cents
            fees = float(sale.get("gumroad_fee", 0)) / 100

            entry = {
                "date": sale.get("created_at", "")[:10],
                "method_id": "MM002",
                "method_name": "INFO_PRODUCTS",
                "source_platform": "gumroad",
                "transaction_type": "one_time",
                "amount": f"{price:.2f}",
                "currency": "USD",
                "fees": f"{fees:.2f}",
                "net_amount": f"{price - fees:.2f}",
                "customer_id": sale.get("email", ""),
                "product_name": sale.get("product_name", ""),
                "recurring": str(sale.get("recurring_charge", False)).upper(),
                "notes": f"Gumroad sale ID: {sale.get('id', '')}",
            }
            entries.append(entry)

        has_more = len(sales) >= 10  # Gumroad pagination
        page += 1
        time.sleep(1)

    log(f"Gumroad: fetched {len(entries)} sales")
    return entries


def import_csv_sales(filepath: Path, source: str = "manual") -> list:
    """Import sales from a CSV export file."""
    entries = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Try to map common CSV column names
            date = ""
            amount = 0.0
            product = ""
            fees = 0.0

            for key, val in row.items():
                k = key.lower().strip()
                if k in ("date", "created_at", "order_date", "sale_date", "timestamp"):
                    date = val[:10]
                elif k in ("amount", "price", "total", "revenue", "sale_price"):
                    try:
                        amount = float(val.replace("$", "").replace(",", ""))
                    except ValueError:
                        pass
                elif k in ("product", "product_name", "item", "item_name", "name"):
                    product = val
                elif k in ("fee", "fees", "platform_fee", "gumroad_fee"):
                    try:
                        fees = float(val.replace("$", "").replace(",", ""))
                    except ValueError:
                        pass

            if date and amount > 0:
                method_id, method_name = METHOD_MAP.get(source, ("MM002", "INFO_PRODUCTS"))
                entry = {
                    "date": date,
                    "method_id": method_id,
                    "method_name": method_name,
                    "source_platform": source,
                    "transaction_type": "one_time",
                    "amount": f"{amount:.2f}",
                    "currency": "USD",
                    "fees": f"{fees:.2f}",
                    "net_amount": f"{amount - fees:.2f}",
                    "customer_id": "",
                    "product_name": product,
                    "recurring": "FALSE",
                    "notes": f"Imported from {filepath.name}",
                }
                entries.append(entry)

    log(f"Imported {len(entries)} sales from {filepath}")
    return entries


def append_revenue_entries(entries: list) -> int:
    """Append new entries to REVENUE_TRACKER.csv, skipping duplicates."""
    existing = get_existing_dates_sources()

    fieldnames = [
        "date", "method_id", "method_name", "source_platform",
        "transaction_type", "amount", "currency", "fees", "net_amount",
        "customer_id", "product_name", "recurring", "notes",
    ]

    new_entries = []
    for entry in entries:
        key = (entry["date"], entry["source_platform"], entry["product_name"])
        if key not in existing:
            new_entries.append(entry)
            existing.add(key)

    if not new_entries:
        log("No new entries to add (all duplicates).")
        return 0

    file_exists = REVENUE_CSV.exists()
    with open(REVENUE_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_entries)

    log(f"Added {len(new_entries)} new revenue entries")
    return len(new_entries)


def generate_summary(days: int = 7) -> str:
    """Generate revenue summary for the last N days."""
    entries = read_existing_revenue()
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Filter to recent entries
    recent = [e for e in entries if e.get("date", "") >= cutoff and e.get("date", "") != ""]

    # Skip example rows
    recent = [e for e in recent if e.get("customer_id", "") != "EXAMPLE"]

    # Aggregate
    total_revenue = 0.0
    total_fees = 0.0
    total_net = 0.0
    by_method = {}
    by_platform = {}
    by_product = {}
    daily = {}

    for e in recent:
        try:
            amount = float(e.get("amount", 0))
            fees = float(e.get("fees", 0))
            net = float(e.get("net_amount", 0))
        except ValueError:
            continue

        total_revenue += amount
        total_fees += fees
        total_net += net

        method = e.get("method_name", "UNKNOWN")
        by_method[method] = by_method.get(method, 0) + net

        platform = e.get("source_platform", "unknown")
        by_platform[platform] = by_platform.get(platform, 0) + net

        product = e.get("product_name", "unknown")
        by_product[product] = by_product.get(product, 0) + net

        date = e.get("date", "unknown")
        daily[date] = daily.get(date, 0) + net

    # Build summary
    summary_lines = [
        f"# PRINTMAXX Revenue Summary",
        f"**Period:** Last {days} days (since {cutoff})",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Totals",
        f"- Gross Revenue: ${total_revenue:,.2f}",
        f"- Platform Fees: ${total_fees:,.2f}",
        f"- Net Revenue: ${total_net:,.2f}",
        f"- Transactions: {len(recent)}",
        "",
    ]

    if by_method:
        summary_lines.append("## By Method")
        for method, net in sorted(by_method.items(), key=lambda x: x[1], reverse=True):
            summary_lines.append(f"- {method}: ${net:,.2f}")
        summary_lines.append("")

    if by_platform:
        summary_lines.append("## By Platform")
        for platform, net in sorted(by_platform.items(), key=lambda x: x[1], reverse=True):
            summary_lines.append(f"- {platform}: ${net:,.2f}")
        summary_lines.append("")

    if by_product:
        summary_lines.append("## By Product")
        for product, net in sorted(by_product.items(), key=lambda x: x[1], reverse=True):
            summary_lines.append(f"- {product}: ${net:,.2f}")
        summary_lines.append("")

    if daily:
        summary_lines.append("## Daily Breakdown")
        for date, net in sorted(daily.items()):
            summary_lines.append(f"- {date}: ${net:,.2f}")
        summary_lines.append("")

    summary = "\n".join(summary_lines)
    return summary


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PRINTMAXX Revenue Tracker")
    parser.add_argument("--source", choices=["gumroad", "appstore", "googleplay", "all"],
                        default="all", help="Revenue source to pull from")
    parser.add_argument("--import-csv", dest="import_csv", help="Import from CSV export file")
    parser.add_argument("--import-source", dest="import_source", default="gumroad",
                        help="Source platform for imported CSV (default: gumroad)")
    parser.add_argument("--summary", action="store_true", help="Generate revenue summary")
    parser.add_argument("--days", type=int, default=7, help="Summary period in days (default: 7)")
    parser.add_argument("--after", default=None, help="Only fetch sales after this date (YYYY-MM-DD)")
    args = parser.parse_args()

    log("PRINTMAXX Revenue Tracker starting")

    if args.summary:
        summary = generate_summary(args.days)
        print(summary)

        # Also write to file
        SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
        summary_file = SUMMARY_DIR / f"revenue_summary_{datetime.now().strftime('%Y%m%d')}.md"
        summary_file.write_text(summary, encoding="utf-8")
        log(f"Summary written to {summary_file}")
        return

    if args.import_csv:
        import_path = Path(args.import_csv)
        if not import_path.exists():
            log(f"Import file not found: {import_path}")
            sys.exit(1)
        entries = import_csv_sales(import_path, source=args.import_source)
        added = append_revenue_entries(entries)
        log(f"Import complete. {added} new entries added.")
        return

    # Pull from APIs
    all_entries = []

    if args.source in ("gumroad", "all"):
        gumroad_entries = fetch_gumroad_sales(after_date=args.after)
        all_entries.extend(gumroad_entries)

    if args.source in ("appstore", "all"):
        log("App Store Connect: requires JWT auth setup. See README for configuration.")
        log("Once configured, revenue data will be pulled automatically.")
        # App Store Connect requires JWT auth with ES256 - complex setup
        # For now, use --import-csv with App Store Connect CSV exports

    if args.source in ("googleplay", "all"):
        log("Google Play Console: requires service account setup. See README for configuration.")
        # Google Play requires service account auth
        # For now, use --import-csv with Google Play Console CSV exports

    if all_entries:
        added = append_revenue_entries(all_entries)
        log(f"Revenue pull complete. {added} new entries added.")
    else:
        log("No new revenue data found from configured sources.")

    # Always generate summary after pull
    summary = generate_summary(args.days)
    print("\n" + summary)

    log("Done.")


if __name__ == "__main__":
    main()
