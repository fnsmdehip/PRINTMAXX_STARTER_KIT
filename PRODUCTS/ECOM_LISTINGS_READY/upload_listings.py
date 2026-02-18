#!/usr/bin/env python3
"""
Ecom Listing Upload Automation
Automates uploading listings to Etsy, Redbubble, and Gumroad using Playwright.

Usage:
    python3 upload_listings.py --platform etsy --listings ETSY_UPLOAD_READY_20.md
    python3 upload_listings.py --platform redbubble --listings REDBUBBLE_UPLOAD_READY_20.md
    python3 upload_listings.py --platform redbubble --listing-number 3
    python3 upload_listings.py --dry-run --platform etsy

Prerequisites:
    pip3 install playwright
    playwright install chromium

IMPORTANT: This script uses a persistent browser profile so you stay logged in.
           Log in manually ONCE, then the script handles uploads.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
LISTINGS_DIR = SCRIPT_DIR
USER_DATA_DIR = PROJECT_ROOT / ".browser_profiles" / "ecom_upload"

# Delays to avoid detection (seconds)
TYPING_DELAY = 50  # ms per keystroke
SHORT_WAIT = 1.5
MEDIUM_WAIT = 3.0
LONG_WAIT = 5.0


def parse_etsy_listings(filepath):
    """Parse ETSY_UPLOAD_READY_20.md into structured listings."""
    listings = []
    current = {}

    with open(filepath, "r") as f:
        content = f.read()

    # Split by listing headers
    blocks = re.split(r"## LISTING \d+", content)[1:]  # skip preamble

    for block in blocks:
        listing = {}

        type_match = re.search(r"\*\*TYPE:\*\*\s*(.+)", block)
        title_match = re.search(r"\*\*TITLE:\*\*\s*(.+)", block)
        price_match = re.search(r"\*\*PRICE:\*\*\s*\$?([\d.]+)", block)
        category_match = re.search(r"\*\*CATEGORY:\*\*\s*(.+)", block)
        tags_match = re.search(
            r"\*\*TAGS(?:\s*\([^)]*\))?:\*\*\s*\n?(.+)",
            block,
        )

        # Extract description between DESCRIPTION: and next **
        desc_match = re.search(
            r"\*\*DESCRIPTION:\*\*\s*\n(.*?)(?=\n\*\*[A-Z]|\n---|\Z)",
            block,
            re.DOTALL,
        )

        if title_match:
            listing["title"] = title_match.group(1).strip()
        if price_match:
            listing["price"] = price_match.group(1).strip()
        if category_match:
            listing["category"] = category_match.group(1).strip()
        if tags_match:
            listing["tags"] = [
                t.strip() for t in tags_match.group(1).split(",") if t.strip()
            ]
        if desc_match:
            listing["description"] = desc_match.group(1).strip()
        if type_match:
            listing["type"] = type_match.group(1).strip()

        if listing.get("title"):
            listings.append(listing)

    return listings


def parse_redbubble_listings(filepath):
    """Parse REDBUBBLE_UPLOAD_READY_20.md into structured listings."""
    listings = []

    with open(filepath, "r") as f:
        content = f.read()

    blocks = re.split(r"## LISTING \d+", content)[1:]

    for block in blocks:
        listing = {}

        type_match = re.search(r"\*\*TYPE:\*\*\s*(.+)", block)
        title_match = re.search(r"\*\*TITLE:\*\*\s*(.+)", block)
        category_match = re.search(r"\*\*CATEGORY:\*\*\s*(.+)", block)
        media_match = re.search(r"\*\*MEDIA:\*\*\s*(.+)", block)
        markup_match = re.search(r"\*\*MARKUP:\*\*\s*(.+)", block)
        tags_match = re.search(
            r"\*\*TAGS \(copy each separately\):\*\*\s*\n(.*?)(?=\n\*\*[A-Z]|\n---|\Z)",
            block,
            re.DOTALL,
        )
        desc_match = re.search(
            r"\*\*DESCRIPTION:\*\*\s*\n(.*?)(?=\n\*\*[A-Z]|\n---|\Z)",
            block,
            re.DOTALL,
        )
        products_match = re.search(r"\*\*ENABLE PRODUCTS:\*\*\s*(.+)", block)

        if title_match:
            listing["title"] = title_match.group(1).strip()
        if category_match:
            listing["category"] = category_match.group(1).strip()
        if media_match:
            listing["media"] = media_match.group(1).strip()
        if tags_match:
            listing["tags"] = [
                t.strip()
                for t in tags_match.group(1).split(",")
                if t.strip() and not t.strip().startswith("---")
            ]
        if desc_match:
            listing["description"] = desc_match.group(1).strip()
        if type_match:
            listing["type"] = type_match.group(1).strip()
        if products_match:
            listing["products"] = products_match.group(1).strip()

        if listing.get("title"):
            listings.append(listing)

    return listings


def upload_to_etsy(page, listing, design_path=None, dry_run=False):
    """Upload a single listing to Etsy."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Uploading to Etsy: {listing['title']}")

    if dry_run:
        print(f"  Title: {listing['title']}")
        print(f"  Price: ${listing.get('price', 'N/A')}")
        print(f"  Tags: {', '.join(listing.get('tags', [])[:13])}")
        print(f"  Category: {listing.get('category', 'N/A')}")
        print("  [Dry run - no browser actions taken]")
        return True

    try:
        # Navigate to new listing page
        page.goto("https://www.etsy.com/your/shops/me/tools/listings/create")
        page.wait_for_load_state("networkidle")
        time.sleep(LONG_WAIT)

        # Upload design file if provided
        if design_path and os.path.exists(design_path):
            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files(design_path)
            time.sleep(MEDIUM_WAIT)

        # Fill title
        title_input = page.locator('[name="title"], #title-input, [data-testid="title-input"]').first
        title_input.click()
        title_input.fill("")
        title_input.type(listing["title"], delay=TYPING_DELAY)
        time.sleep(SHORT_WAIT)

        # Fill description
        desc_input = page.locator('[name="description"], .description-editor, [data-testid="description-input"]').first
        desc_input.click()
        desc_input.fill("")
        desc_input.type(listing.get("description", ""), delay=TYPING_DELAY)
        time.sleep(SHORT_WAIT)

        # Fill price
        if listing.get("price"):
            price_input = page.locator('[name="price"], #price-input, [data-testid="price-input"]').first
            price_input.click()
            price_input.fill("")
            price_input.type(listing["price"], delay=TYPING_DELAY)
            time.sleep(SHORT_WAIT)

        # Add tags (Etsy allows 13)
        tags = listing.get("tags", [])[:13]
        for tag in tags:
            tag_input = page.locator('[name="tags"], #tag-input, [data-testid="tag-input"]').first
            tag_input.click()
            tag_input.type(tag, delay=TYPING_DELAY)
            tag_input.press("Enter")
            time.sleep(0.5)

        print(f"  Filled: {listing['title']}")
        print(f"  MANUAL CHECK REQUIRED: Review listing before publishing")

        # Do NOT auto-submit. Let human review.
        return True

    except Exception as e:
        print(f"  ERROR uploading {listing['title']}: {e}")
        return False


def upload_to_redbubble(page, listing, design_path=None, dry_run=False):
    """Upload a single listing to Redbubble."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Uploading to Redbubble: {listing['title']}")

    if dry_run:
        print(f"  Title: {listing['title']}")
        print(f"  Tags: {len(listing.get('tags', []))} tags")
        print(f"  Category: {listing.get('category', 'N/A')}")
        print(f"  Products: {listing.get('products', 'N/A')}")
        print("  [Dry run - no browser actions taken]")
        return True

    try:
        # Navigate to new work upload page
        page.goto("https://www.redbubble.com/portfolio/images/new")
        page.wait_for_load_state("networkidle")
        time.sleep(LONG_WAIT)

        # Upload design file
        if design_path and os.path.exists(design_path):
            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files(design_path)
            time.sleep(LONG_WAIT)  # design processing takes time

        # Fill title
        title_input = page.locator('#work_title_en, [name="work[title_en]"], input[placeholder*="title"]').first
        title_input.click()
        title_input.fill("")
        title_input.type(listing["title"], delay=TYPING_DELAY)
        time.sleep(SHORT_WAIT)

        # Fill description
        desc_input = page.locator('#work_description_en, [name="work[description_en]"], textarea[placeholder*="description"]').first
        desc_input.click()
        desc_input.fill("")
        desc_input.type(listing.get("description", ""), delay=TYPING_DELAY)
        time.sleep(SHORT_WAIT)

        # Add tags
        tags = listing.get("tags", [])[:15]
        tag_input = page.locator('#work_tag_field_en, [name="work[tag_field_en]"], input[placeholder*="tag"]').first
        for tag in tags:
            tag_input.click()
            tag_input.type(tag, delay=TYPING_DELAY)
            tag_input.press("Enter")
            time.sleep(0.3)

        print(f"  Filled: {listing['title']}")
        print(f"  MANUAL CHECK REQUIRED: Review design placement and enable products before saving")

        return True

    except Exception as e:
        print(f"  ERROR uploading {listing['title']}: {e}")
        return False


def run_upload(platform, listings_file, listing_number=None, designs_dir=None, dry_run=False):
    """Main upload orchestrator."""

    # Parse listings
    filepath = LISTINGS_DIR / listings_file
    if not filepath.exists():
        print(f"ERROR: Listings file not found: {filepath}")
        sys.exit(1)

    if platform == "etsy":
        listings = parse_etsy_listings(filepath)
    elif platform == "redbubble":
        listings = parse_redbubble_listings(filepath)
    else:
        print(f"ERROR: Unknown platform: {platform}")
        sys.exit(1)

    print(f"Parsed {len(listings)} listings from {listings_file}")

    # Filter to specific listing if requested
    if listing_number is not None:
        if listing_number < 1 or listing_number > len(listings):
            print(f"ERROR: Listing number {listing_number} out of range (1-{len(listings)})")
            sys.exit(1)
        listings = [listings[listing_number - 1]]
        print(f"Uploading listing #{listing_number} only")

    if dry_run:
        print("\n=== DRY RUN MODE - No browser actions ===\n")
        for i, listing in enumerate(listings, 1):
            if platform == "etsy":
                upload_to_etsy(None, listing, dry_run=True)
            elif platform == "redbubble":
                upload_to_redbubble(None, listing, dry_run=True)
        print(f"\n=== Dry run complete. {len(listings)} listings parsed successfully. ===")
        return

    # Launch browser with persistent profile
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: Playwright not installed. Run: pip3 install playwright && playwright install chromium")
        sys.exit(1)

    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,  # Must be visible for manual review
            viewport={"width": 1280, "height": 900},
            slow_mo=100,
        )
        page = browser.new_page()

        # Check if logged in
        if platform == "etsy":
            page.goto("https://www.etsy.com/your/shops/me")
            time.sleep(MEDIUM_WAIT)
            if "sign-in" in page.url.lower() or "signin" in page.url.lower():
                print("\nNot logged in to Etsy. Please log in manually in the browser window.")
                print("Press Enter when logged in...")
                input()
        elif platform == "redbubble":
            page.goto("https://www.redbubble.com/portfolio/manage-works")
            time.sleep(MEDIUM_WAIT)
            if "login" in page.url.lower() or "auth" in page.url.lower():
                print("\nNot logged in to Redbubble. Please log in manually in the browser window.")
                print("Press Enter when logged in...")
                input()

        # Upload each listing
        success_count = 0
        fail_count = 0

        for i, listing in enumerate(listings, 1):
            print(f"\n--- Listing {i}/{len(listings)} ---")

            # Check for design file
            design_path = None
            if designs_dir:
                # Look for design file matching listing number
                pattern = f"design_{i:02d}.*"
                matches = list(Path(designs_dir).glob(pattern))
                if matches:
                    design_path = str(matches[0])
                    print(f"  Found design file: {design_path}")

            if platform == "etsy":
                success = upload_to_etsy(page, listing, design_path)
            elif platform == "redbubble":
                success = upload_to_redbubble(page, listing, design_path)

            if success:
                success_count += 1
                print(f"  Review the listing in the browser, then press Enter to continue...")
                input()
            else:
                fail_count += 1
                print(f"  Failed. Press Enter to try next listing...")
                input()

            # Pause between uploads to avoid rate limiting
            if i < len(listings):
                print(f"  Waiting {MEDIUM_WAIT}s before next listing...")
                time.sleep(MEDIUM_WAIT)

        print(f"\n=== Upload complete ===")
        print(f"  Success: {success_count}/{len(listings)}")
        print(f"  Failed: {fail_count}/{len(listings)}")

        print("\nBrowser will stay open for final review. Close when done.")
        input("Press Enter to close browser...")
        browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Upload ecom listings to Etsy, Redbubble, or Gumroad"
    )
    parser.add_argument(
        "--platform",
        required=True,
        choices=["etsy", "redbubble"],
        help="Target platform",
    )
    parser.add_argument(
        "--listings",
        help="Listings markdown file (default: auto-detect based on platform)",
    )
    parser.add_argument(
        "--listing-number",
        type=int,
        help="Upload a specific listing number only (1-indexed)",
    )
    parser.add_argument(
        "--designs-dir",
        help="Directory containing design PNG files (named design_01.png, design_02.png, etc.)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse listings and show what would be uploaded, without launching browser",
    )

    args = parser.parse_args()

    # Auto-detect listings file
    if not args.listings:
        if args.platform == "etsy":
            args.listings = "ETSY_UPLOAD_READY_20.md"
        elif args.platform == "redbubble":
            args.listings = "REDBUBBLE_UPLOAD_READY_20.md"

    run_upload(
        platform=args.platform,
        listings_file=args.listings,
        listing_number=args.listing_number,
        designs_dir=args.designs_dir,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
