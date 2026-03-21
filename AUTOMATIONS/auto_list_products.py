#!/usr/bin/env python3

from __future__ import annotations
"""
Auto-List Products on Marketplaces
Reads ready-to-list product data from PRODUCTS/ and automates listing via Playwright.

Supported platforms: gumroad, etsy, redbubble, fiverr
Usage:
    python3 AUTOMATIONS/auto_list_products.py --platform gumroad --dry-run
    python3 AUTOMATIONS/auto_list_products.py --platform etsy --start 1 --count 5
    python3 AUTOMATIONS/auto_list_products.py --platform redbubble --list
"""

import argparse
import csv
import json
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = BASE / "PRODUCTS"
LOGS_DIR = BASE / "AUTOMATIONS" / "logs"
LOG_FILE = LOGS_DIR / "listing_log.csv"
PROGRESS_FILE = LOGS_DIR / "listing_progress.json"

PLATFORM_FILES = {
    "gumroad": PRODUCTS_DIR / "GUMROAD_READY_LISTINGS.md",
    "etsy": PRODUCTS_DIR / "ETSY_LISTINGS_20.md",
    "redbubble": PRODUCTS_DIR / "REDBUBBLE_LISTINGS.md",
    "fiverr": BASE / "OPS" / "FIVERR_LAUNCH_PACKAGE.md",
    "ebay": BASE / "output" / "ecom_autopilot" / "queues" / "ebay_queue.csv",
}

PLATFORM_URLS = {
    "gumroad": "https://app.gumroad.com/products/new",
    "etsy": "https://www.etsy.com/your/shops/me/tools/listings/create",
    "redbubble": "https://www.redbubble.com/portfolio/images/new",
    "fiverr": "https://www.fiverr.com/seller_dashboard",
    "ebay": "https://www.ebay.com/sl/sell",
}


def human_delay(min_s=2.0, max_s=5.0):
    """Random delay to mimic human behavior."""
    delay = random.uniform(min_s, max_s)
    time.sleep(delay)
    return delay


def log_action(platform, product_name, action, status, details=""):
    """Append an action to the listing log CSV."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_FILE.exists()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "platform", "product", "action", "status", "details"])
        writer.writerow([
            datetime.now().isoformat(),
            platform,
            product_name,
            action,
            status,
            details,
        ])


def load_progress():
    """Load listing progress from JSON."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {}


def save_progress(progress):
    """Save listing progress to JSON."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


# ---------------------------------------------------------------------------
# Parsers: extract structured product data from markdown files
# ---------------------------------------------------------------------------

def parse_gumroad_listings(filepath):
    """Parse GUMROAD_READY_LISTINGS.md into structured product dicts."""
    text = filepath.read_text()
    listings = []
    blocks = re.split(r"^## LISTING \d+:", text, flags=re.MULTILINE)
    for block in blocks[1:]:
        product = {}
        name_match = re.search(r"\*\*Gumroad Product Name:\*\*\s*(.+)", block)
        product["name"] = name_match.group(1).strip() if name_match else "Untitled"

        price_match = re.search(r"\*\*Price:\*\*\s*\$?([\d.]+)", block)
        product["price"] = price_match.group(1) if price_match else "0"

        oneliner_match = re.search(r"\*\*One-liner:\*\*\s*(.+)", block)
        product["summary"] = oneliner_match.group(1).strip() if oneliner_match else ""

        cat_match = re.search(r"\*\*Category:\*\*\s*(.+)", block)
        product["category"] = cat_match.group(1).strip() if cat_match else ""

        tags_match = re.search(r"\*\*Tags:\*\*\s*(.+)", block)
        product["tags"] = tags_match.group(1).strip() if tags_match else ""

        desc_match = re.search(r"\*\*Description:\*\*\s*\n(.*?)(?=\n\*\*What's Included|\n---|\Z)", block, re.DOTALL)
        product["description"] = desc_match.group(1).strip() if desc_match else ""

        includes_match = re.search(r"\*\*What's Included:\*\*\s*\n(.*?)(?=\n\*\*Who|\n---|\Z)", block, re.DOTALL)
        product["includes"] = includes_match.group(1).strip() if includes_match else ""

        product["full_description"] = product["description"]
        if product["includes"]:
            product["full_description"] += "\n\nWhat's Included:\n" + product["includes"]

        listings.append(product)
    return listings


def parse_etsy_listings(filepath):
    """Parse ETSY_LISTINGS_20.md into structured product dicts."""
    text = filepath.read_text()
    listings = []
    blocks = re.split(r"^### LISTING \d+:", text, flags=re.MULTILINE)
    for block in blocks[1:]:
        product = {}
        title_match = re.search(r"\*\*Etsy Title:\*\*\s*\n(.+)", block)
        product["name"] = title_match.group(1).strip() if title_match else "Untitled"

        price_match = re.search(r"\*\*Price:\*\*\s*\$?([\d.]+)", block)
        product["price"] = price_match.group(1) if price_match else "0"

        cat_match = re.search(r"\*\*Category:\*\*\s*(.+)", block)
        product["category"] = cat_match.group(1).strip() if cat_match else ""

        tags = []
        for m in re.finditer(r"^\d+\.\s+(.+)$", block, re.MULTILINE):
            tag = m.group(1).strip()
            if len(tag) <= 20:
                tags.append(tag)
        product["tags"] = tags[:13]

        desc_match = re.search(r"\*\*Description:\*\*\s*\n(.*?)(?=\n\*\*Listing Image|\n---|\Z)", block, re.DOTALL)
        product["description"] = desc_match.group(1).strip() if desc_match else ""

        listings.append(product)
    return listings


def parse_redbubble_listings(filepath):
    """Parse REDBUBBLE_LISTINGS.md into structured product dicts."""
    text = filepath.read_text()
    listings = []
    blocks = re.split(r"^## LISTING \d+:", text, flags=re.MULTILINE)
    for block in blocks[1:]:
        product = {}
        title_match = re.search(r"\*\*Title:\*\*\s*(.+)", block)
        product["name"] = title_match.group(1).strip() if title_match else "Untitled"

        desc_match = re.search(r"\*\*Description:\*\*\s*\n(.*?)(?=\n\*\*Tags|\n---|\Z)", block, re.DOTALL)
        product["description"] = desc_match.group(1).strip() if desc_match else ""

        tags = []
        for m in re.finditer(r"^\d+\.\s+(.+)$", block, re.MULTILINE):
            tags.append(m.group(1).strip())
        product["tags"] = tags[:15]

        cat_match = re.search(r"\*\*Category:\*\*\s*(.+)", block)
        product["category"] = cat_match.group(1).strip() if cat_match else ""

        media_match = re.search(r"\*\*Media:\*\*\s*(.+)", block)
        product["media"] = media_match.group(1).strip() if media_match else ""

        listings.append(product)
    return listings


def parse_fiverr_listings(filepath):
    """Parse FIVERR_LAUNCH_PACKAGE.md into structured gig dicts."""
    text = filepath.read_text()
    listings = []
    blocks = re.split(r"^## (?:GIG|Gig) \d+", text, flags=re.MULTILINE)
    for block in blocks[1:]:
        product = {}
        title_match = re.search(r"\*\*(?:Gig )?Title:\*\*\s*(.+)", block)
        product["name"] = title_match.group(1).strip() if title_match else "Untitled"

        cat_match = re.search(r"\*\*Category:\*\*\s*(.+)", block)
        product["category"] = cat_match.group(1).strip() if cat_match else ""

        desc_match = re.search(r"\*\*Description:\*\*\s*\n(.*?)(?=\n\*\*|\n---|\Z)", block, re.DOTALL)
        product["description"] = desc_match.group(1).strip() if desc_match else ""

        tags = []
        tags_match = re.search(r"\*\*Tags:\*\*\s*(.+)", block)
        if tags_match:
            tags = [t.strip() for t in tags_match.group(1).split(",")]
        product["tags"] = tags[:5]

        listings.append(product)
    return listings


def parse_ebay_queue(filepath):
    """Parse output/ecom_autopilot/queues/ebay_queue.csv into listing dicts."""
    listings = []
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = (row.get("queue_status") or "").strip().upper()
            title = (row.get("title") or row.get("product") or "").strip()
            if not title:
                continue
            listings.append(
                {
                    "name": title,
                    "price": (row.get("sell_price") or "0").strip(),
                    "description": (row.get("description") or "").strip(),
                    "tags": [t.strip() for t in (row.get("tags") or "").split(",") if t.strip()],
                    "category": (row.get("category") or "general").strip(),
                    "product_id": (row.get("product_id") or "").strip(),
                    "queue_status": status,
                    "source_price": (row.get("source_price") or "").strip(),
                    "margin_pct": (row.get("margin_pct") or "").strip(),
                }
            )
    # Prefer rows that are already account ready.
    listings.sort(key=lambda r: (0 if (r.get("queue_status") or "").upper() in {"AUTO_READY", "ACCOUNT_READY_NO_AUTOMATION"} else 1, r.get("name", "")))
    return listings


PARSERS = {
    "gumroad": parse_gumroad_listings,
    "etsy": parse_etsy_listings,
    "redbubble": parse_redbubble_listings,
    "fiverr": parse_fiverr_listings,
    "ebay": parse_ebay_queue,
}


# ---------------------------------------------------------------------------
# Playwright automation per platform
# ---------------------------------------------------------------------------

def try_selectors(page, selectors, action="click", value=None, timeout=5000):
    """Try multiple selectors until one works. Returns True on success."""
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            if loc.is_visible(timeout=timeout):
                if action == "click":
                    loc.click()
                elif action == "fill":
                    loc.click()
                    loc.fill(value or "")
                elif action == "type":
                    loc.click()
                    loc.type(value or "", delay=random.randint(20, 60))
                return True
        except Exception:
            continue
    return False


def wait_for_login(page, platform):
    """Pause and let user log in manually, then continue."""
    print(f"\n{'='*60}")
    print(f"  LOGIN REQUIRED: {platform.upper()}")
    print(f"  The browser is open at {PLATFORM_URLS[platform]}")
    print(f"  Log in manually, then press ENTER here to continue.")
    print(f"{'='*60}")
    input("  Press ENTER after logging in... ")
    human_delay(1, 2)
    print("  Continuing...\n")


def automate_gumroad(page, product, dry_run=False):
    """Automate listing a product on Gumroad."""
    name = product["name"]
    if dry_run:
        print(f"  [DRY RUN] Would create Gumroad product: {name}")
        print(f"    Price: ${product['price']}")
        print(f"    Description: {product.get('full_description', product['description'])[:100]}...")
        return True

    page.goto("https://app.gumroad.com/products/new")
    human_delay(2, 4)

    # Product name
    try_selectors(page, [
        'input[name="name"]',
        'input[placeholder*="Name"]',
        'input[placeholder*="name"]',
        '#product-name',
        'input[type="text"]',
    ], action="fill", value=name)
    human_delay()

    # Price
    try_selectors(page, [
        'input[name="price"]',
        'input[placeholder*="Price"]',
        'input[placeholder*="price"]',
        'input[type="number"]',
    ], action="fill", value=product["price"])
    human_delay()

    # Description (look for rich text or textarea)
    desc = product.get("full_description", product["description"])
    try_selectors(page, [
        'textarea[name="description"]',
        '[contenteditable="true"]',
        'textarea',
        '.ql-editor',
        '.ProseMirror',
    ], action="fill", value=desc[:5000])
    human_delay(1, 3)

    # Summary/one-liner
    if product.get("summary"):
        try_selectors(page, [
            'input[name="custom_summary"]',
            'input[placeholder*="summary"]',
            'textarea[name="summary"]',
        ], action="fill", value=product["summary"])
        human_delay()

    print(f"  Form filled for: {name}")
    print(f"  >> Review the listing in the browser, then click Publish manually.")
    input(f"  Press ENTER after publishing (or skip)... ")
    return True


def automate_etsy(page, product, dry_run=False):
    """Automate listing a product on Etsy."""
    name = product["name"]
    if dry_run:
        print(f"  [DRY RUN] Would create Etsy listing: {name}")
        print(f"    Price: ${product['price']}")
        print(f"    Tags: {', '.join(product.get('tags', [])[:5])}...")
        return True

    page.goto("https://www.etsy.com/your/shops/me/tools/listings/create")
    human_delay(3, 5)

    # Title
    try_selectors(page, [
        'input[name="title"]',
        '#listing-edit-title',
        'input[placeholder*="title"]',
        'textarea[name="title"]',
    ], action="fill", value=name)
    human_delay()

    # Description
    try_selectors(page, [
        'textarea[name="description"]',
        '#listing-edit-description',
        '[contenteditable="true"]',
        'textarea',
    ], action="fill", value=product["description"][:5000])
    human_delay()

    # Price
    try_selectors(page, [
        'input[name="price"]',
        '#listing-edit-price',
        'input[placeholder*="Price"]',
    ], action="fill", value=product["price"])
    human_delay()

    # Tags
    for tag in product.get("tags", [])[:13]:
        try_selectors(page, [
            'input[name="tags"]',
            'input[placeholder*="tag"]',
            'input[placeholder*="Tag"]',
            '#listing-edit-tags input',
        ], action="type", value=tag + "\n")
        human_delay(0.5, 1.5)

    print(f"  Form filled for: {name}")
    print(f"  >> Set as Digital Download, upload file, select category, then Publish.")
    input(f"  Press ENTER after publishing (or skip)... ")
    return True


def automate_redbubble(page, product, dry_run=False):
    """Automate listing a product on Redbubble."""
    name = product["name"]
    if dry_run:
        print(f"  [DRY RUN] Would create Redbubble listing: {name}")
        print(f"    Tags: {', '.join(product.get('tags', [])[:5])}...")
        return True

    page.goto("https://www.redbubble.com/portfolio/images/new")
    human_delay(3, 5)

    # Title
    try_selectors(page, [
        'input[name="work_title"]',
        '#work_title',
        'input[placeholder*="Title"]',
        'input[name="title"]',
    ], action="fill", value=name)
    human_delay()

    # Description
    try_selectors(page, [
        'textarea[name="work_description"]',
        '#work_description',
        'textarea[name="description"]',
        'textarea',
    ], action="fill", value=product["description"][:2000])
    human_delay()

    # Tags
    tag_text = ", ".join(product.get("tags", [])[:15])
    try_selectors(page, [
        'textarea[name="work_tag_field"]',
        '#work_tag_field',
        'input[name="tags"]',
        'textarea[placeholder*="tag"]',
    ], action="fill", value=tag_text)
    human_delay()

    print(f"  Form filled for: {name}")
    print(f"  >> Upload design image, enable products, set markup to 35%, then Save.")
    input(f"  Press ENTER after saving (or skip)... ")
    return True


def automate_fiverr(page, product, dry_run=False):
    """Automate listing a gig on Fiverr."""
    name = product["name"]
    if dry_run:
        print(f"  [DRY RUN] Would create Fiverr gig: {name}")
        print(f"    Category: {product.get('category', 'N/A')}")
        return True

    page.goto("https://www.fiverr.com/seller_dashboard")
    human_delay(3, 5)

    print(f"  Fiverr gig creation requires many manual steps.")
    print(f"  Gig: {name}")
    print(f"  Category: {product.get('category', 'N/A')}")
    print(f"  Description preview: {product['description'][:200]}...")
    print(f"  Tags: {', '.join(product.get('tags', []))}")
    print(f"\n  >> Navigate to Create Gig, fill using the data above.")
    input(f"  Press ENTER when done (or skip)... ")
    return True


def automate_ebay(page, product, dry_run=False):
    """Automate listing a product on eBay Seller flow (best effort)."""
    name = product["name"]
    if dry_run:
        print(f"  [DRY RUN] Would create eBay listing: {name}")
        print(f"    Price: ${product.get('price', '0')}")
        print(f"    Category: {product.get('category', 'general')}")
        return True

    page.goto("https://www.ebay.com/sl/sell")
    human_delay(3, 5)

    # Title
    try_selectors(page, [
        'input[name="title"]',
        'input[placeholder*="Tell us what"]',
        'input[placeholder*="title"]',
        'input[aria-label*="title"]',
        'input[type="text"]',
    ], action="fill", value=name)
    human_delay()

    # Price
    try_selectors(page, [
        'input[name="price"]',
        'input[aria-label*="Price"]',
        'input[placeholder*="price"]',
        'input[type="number"]',
    ], action="fill", value=str(product.get("price") or "0"))
    human_delay()

    # Description
    desc = product.get("description", "")
    if desc:
        try_selectors(page, [
            'textarea[name="description"]',
            'textarea[aria-label*="Description"]',
            '[contenteditable="true"]',
            'textarea',
        ], action="fill", value=desc[:4000])
        human_delay(1, 3)

    print(f"  Form filled for: {name}")
    print("  >> Add photos + shipping + condition specifics, then publish on eBay.")
    input("  Press ENTER after publishing (or skip)... ")
    return True


AUTOMATORS = {
    "gumroad": automate_gumroad,
    "etsy": automate_etsy,
    "redbubble": automate_redbubble,
    "fiverr": automate_fiverr,
    "ebay": automate_ebay,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Auto-list products on marketplaces")
    parser.add_argument("--platform", required=True, choices=["gumroad", "etsy", "redbubble", "fiverr", "ebay"])
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without browser automation")
    parser.add_argument("--list", action="store_true", help="List parsed products and exit")
    parser.add_argument("--start", type=int, default=1, help="Start from listing number (1-indexed)")
    parser.add_argument("--count", type=int, default=0, help="Number of listings to process (0 = all)")
    parser.add_argument("--headless", action="store_true", help="Run browser headless (not recommended)")
    parser.add_argument("--chrome-profile", dest="chrome_profile", default="", help="Path to Chrome user data dir (uses logged-in session)")
    args = parser.parse_args()

    platform = args.platform
    source_file = PLATFORM_FILES[platform]

    if not source_file.exists():
        print(f"ERROR: Source file not found: {source_file}")
        if platform == "ebay":
            print("Run first: python3 AUTOMATIONS/ecom_autopilot.py --tick")
        sys.exit(1)

    # Parse products
    parse_fn = PARSERS[platform]
    products = parse_fn(source_file)

    if not products:
        print(f"ERROR: No products parsed from {source_file}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  PRINTMAXX Auto-Lister: {platform.upper()}")
    print(f"  Source: {source_file.name}")
    print(f"  Products found: {len(products)}")
    print(f"  Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"{'='*60}\n")

    # List mode
    if args.list:
        for i, p in enumerate(products, 1):
            price = p.get("price", "N/A")
            print(f"  {i:>2}. {p['name'][:70]:<70} ${price}")
        print(f"\n  Total: {len(products)} products")
        return

    # Determine range
    start_idx = max(0, args.start - 1)
    end_idx = len(products) if args.count == 0 else min(len(products), start_idx + args.count)
    batch = products[start_idx:end_idx]

    print(f"  Processing listings {start_idx + 1} to {end_idx} ({len(batch)} products)\n")

    # Load progress
    progress = load_progress()
    progress_key = f"{platform}_listed"
    if progress_key not in progress:
        progress[progress_key] = []

    if args.dry_run:
        for i, product in enumerate(batch, start_idx + 1):
            print(f"\n--- Listing {i}/{len(products)} ---")
            AUTOMATORS[platform](None, product, dry_run=True)
            log_action(platform, product["name"], "dry_run", "OK")
        print(f"\n  Dry run complete. {len(batch)} listings previewed.")
        return

    # Live mode with Playwright
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: Playwright not installed. Run: pip install playwright && playwright install")
        sys.exit(1)

    with sync_playwright() as pw:
        # Try connecting to existing Chrome via CDP (user already logged in)
        chrome_cdp = os.environ.get("CHROME_CDP", "")
        chrome_profile = args.chrome_profile if hasattr(args, "chrome_profile") and args.chrome_profile else ""

        if chrome_cdp:
            print(f"  Connecting to Chrome via CDP: {chrome_cdp}")
            browser = pw.chromium.connect_over_cdp(chrome_cdp)
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.new_page()
        elif chrome_profile:
            print(f"  Launching Chrome with profile: {chrome_profile}")
            context = pw.chromium.launch_persistent_context(
                chrome_profile,
                headless=False,
                channel="chrome",
                viewport={"width": 1280, "height": 900},
            )
            page = context.new_page()
            browser = None  # persistent context manages its own browser
        else:
            browser = pw.chromium.launch(headless=args.headless)
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )
            page = context.new_page()

        # Navigate to platform and let user log in (skip if CDP — already logged in)
        page.goto(PLATFORM_URLS[platform])
        if not chrome_cdp and not chrome_profile:
            wait_for_login(page, platform)

        automator = AUTOMATORS[platform]
        succeeded = 0
        failed = 0

        for i, product in enumerate(batch, start_idx + 1):
            name = product["name"]

            # Skip if already listed
            if name in progress.get(progress_key, []):
                print(f"  [{i}] SKIP (already listed): {name}")
                continue

            print(f"\n--- Listing {i}/{len(products)}: {name} ---")

            retries = 2
            success = False
            for attempt in range(retries + 1):
                try:
                    success = automator(page, product, dry_run=False)
                    break
                except Exception as e:
                    if attempt < retries:
                        print(f"  Retry {attempt + 1}/{retries} after error: {e}")
                        human_delay(3, 6)
                    else:
                        print(f"  FAILED after {retries + 1} attempts: {e}")

            if success:
                succeeded += 1
                progress[progress_key].append(name)
                save_progress(progress)
                log_action(platform, name, "listed", "OK")
            else:
                failed += 1
                log_action(platform, name, "listed", "FAILED")

            human_delay(2, 4)

        browser.close()

    print(f"\n{'='*60}")
    print(f"  RESULTS: {succeeded} listed, {failed} failed, {len(batch) - succeeded - failed} skipped")
    print(f"  Log: {LOG_FILE}")
    print(f"  Progress: {PROGRESS_FILE}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
