#!/usr/bin/env python3
"""
Gumroad Auto-Lister — Uses your Chrome profile (logged-in session).
Closes Chrome briefly, opens Playwright with your profile, lists products, done.

Usage:
    python3 TOOLS/gumroad_list_now.py --dry-run     # preview what will be listed
    python3 TOOLS/gumroad_list_now.py                # actually list products
    python3 TOOLS/gumroad_list_now.py --max 3        # list first 3 only
"""

import json
import os
import subprocess
import sys
import time
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CATALOG = BASE / "PRODUCTS" / "GUMROAD_AUTOLIST" / "catalog.json"
CHROME_USERDATA = os.path.expanduser("~/Library/Application Support/Google/Chrome")
PROGRESS_FILE = BASE / "AUTOMATIONS" / "logs" / "gumroad_listing_progress.json"


def load_catalog():
    with open(CATALOG) as f:
        data = json.load(f)
    return data["items"]


def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"listed": []}


def save_progress(progress):
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def human_delay(min_s=1.5, max_s=3.5):
    time.sleep(random.uniform(min_s, max_s))


def close_chrome():
    """Gently close Chrome so we can use the profile."""
    print("  Closing Chrome (will reopen after)...")
    subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to quit'],
                   capture_output=True, timeout=10)
    time.sleep(3)


def reopen_chrome():
    """Reopen Chrome after we're done."""
    subprocess.Popen(["open", "-a", "Google Chrome"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def list_product(page, item, dry_run=False):
    """List a single product on Gumroad."""
    name = item["name"]
    price_cents = item["price_cents"]
    price_dollars = price_cents / 100
    description = item.get("description_md", "")
    tags = item.get("tags", [])
    file_path = BASE / item.get("file_relpath", "")

    print(f"\n  Product: {name}")
    print(f"  Price: ${price_dollars:.2f}")
    print(f"  Tags: {', '.join(tags)}")
    print(f"  File: {file_path.name if file_path.exists() else 'MISSING'}")

    if dry_run:
        print("  [DRY RUN] Would list this product")
        return True

    try:
        # Go to new product page
        page.goto("https://app.gumroad.com/products/new", wait_until="networkidle", timeout=15000)
        human_delay(2, 4)

        # Gumroad's new product flow:
        # 1. Product name
        name_sel = 'input[placeholder*="Name"], input[name="name"], input[aria-label*="name" i]'
        page.wait_for_selector(name_sel, timeout=10000)
        page.fill(name_sel, name)
        human_delay()

        # 2. Price
        price_sel = 'input[placeholder*="Price"], input[name="price"], input[type="number"]'
        price_inputs = page.query_selector_all(price_sel)
        if price_inputs:
            price_inputs[0].fill(str(int(price_dollars)) if price_dollars == int(price_dollars) else f"{price_dollars:.2f}")
            human_delay()

        # 3. Click create / next button
        for btn_text in ["Create product", "Create", "Next", "Continue", "Save"]:
            btn = page.query_selector(f'button:has-text("{btn_text}")')
            if btn and btn.is_visible():
                btn.click()
                human_delay(2, 4)
                break

        # 4. Wait for product editor to load
        page.wait_for_load_state("networkidle", timeout=10000)
        human_delay(2, 3)

        # 5. Description — look for rich text editor or textarea
        desc_sel = 'div[contenteditable="true"], textarea[name="description"], .ProseMirror, .ql-editor'
        desc_el = page.query_selector(desc_sel)
        if desc_el:
            desc_el.click()
            # Clear existing content
            page.keyboard.press("Meta+a")
            page.keyboard.type(description[:2000], delay=5)  # type with slight delay
            human_delay()

        # 6. File upload if exists
        if file_path.exists():
            file_input = page.query_selector('input[type="file"]')
            if file_input:
                file_input.set_input_files(str(file_path))
                print(f"  Uploaded: {file_path.name}")
                human_delay(3, 5)  # wait for upload

        # 7. Tags
        for tag in tags[:10]:
            tag_input = page.query_selector('input[placeholder*="tag" i], input[placeholder*="Tag" i]')
            if tag_input:
                tag_input.fill(tag)
                page.keyboard.press("Enter")
                human_delay(0.5, 1)

        # 8. Save / Publish
        for btn_text in ["Save", "Publish", "Save changes", "Update"]:
            btn = page.query_selector(f'button:has-text("{btn_text}")')
            if btn and btn.is_visible():
                btn.click()
                human_delay(2, 4)
                break

        print(f"  LISTED: {name}")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        # Take screenshot for debugging
        try:
            ss_path = BASE / "AUTOMATIONS" / "logs" / f"gumroad_error_{int(time.time())}.png"
            page.screenshot(path=str(ss_path))
            print(f"  Screenshot saved: {ss_path}")
        except:
            pass
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Gumroad Auto-Lister (uses Chrome profile)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without listing")
    parser.add_argument("--max", type=int, default=0, help="Max products to list (0=all)")
    parser.add_argument("--skip-close", action="store_true", help="Don't close/reopen Chrome (for testing)")
    args = parser.parse_args()

    items = load_catalog()
    progress = load_progress()

    # Filter already-listed
    pending = [i for i in items if i["sku"] not in progress["listed"]]
    if args.max > 0:
        pending = pending[:args.max]

    print(f"\n  Gumroad Auto-Lister")
    print(f"  Total products: {len(items)}")
    print(f"  Already listed: {len(progress['listed'])}")
    print(f"  To list now: {len(pending)}")

    if not pending:
        print("  Nothing to list!")
        return

    if args.dry_run:
        for item in pending:
            list_product(None, item, dry_run=True)
        print(f"\n  Dry run complete. {len(pending)} products previewed.")
        return

    # Close Chrome so we can use the profile
    if not args.skip_close:
        close_chrome()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: pip install playwright && playwright install")
        sys.exit(1)

    succeeded = 0
    failed = 0

    try:
        with sync_playwright() as pw:
            # Launch with Chrome's actual profile — all cookies, logins, sessions
            context = pw.chromium.launch_persistent_context(
                CHROME_USERDATA,
                headless=False,
                channel="chrome",
                viewport={"width": 1280, "height": 900},
                args=["--disable-blink-features=AutomationControlled"],
            )
            page = context.new_page()

            # Verify we're logged in
            page.goto("https://app.gumroad.com/dashboard", timeout=15000)
            human_delay(2, 4)

            if "login" in page.url.lower():
                print("\n  NOT LOGGED IN to Gumroad. Please log in manually...")
                page.wait_for_url("**/dashboard**", timeout=120000)
                print("  Logged in!")

            for item in pending:
                success = list_product(page, item)
                if success:
                    succeeded += 1
                    progress["listed"].append(item["sku"])
                    save_progress(progress)
                else:
                    failed += 1

                # Delay between products
                if succeeded + failed < len(pending):
                    delay = random.uniform(5, 15)
                    print(f"  Waiting {delay:.0f}s before next product...")
                    time.sleep(delay)

            context.close()

    finally:
        # Always reopen Chrome
        if not args.skip_close:
            reopen_chrome()

    print(f"\n  Done! Listed: {succeeded}, Failed: {failed}")
    print(f"  Progress saved to {PROGRESS_FILE}")


if __name__ == "__main__":
    main()
