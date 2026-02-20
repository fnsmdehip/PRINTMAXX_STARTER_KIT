#!/usr/bin/env python3
"""
Gumroad Auto-Lister via agent-browser CLI.

Lists products on Gumroad using the agent-browser CLI tool.
Assumes agent-browser is already connected to an open browser
session where the user is logged into Gumroad.

Usage:
    python3 TOOLS/ab_gumroad_lister.py --dry-run          # preview what will be listed
    python3 TOOLS/ab_gumroad_lister.py                     # list all pending products
    python3 TOOLS/ab_gumroad_lister.py --max 2             # list first 2 only
    python3 TOOLS/ab_gumroad_lister.py --max 1 --verbose   # list 1 with full debug output
"""

import json
import os
import subprocess
import sys
import time
import random
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent
CATALOG = BASE / "PRODUCTS" / "GUMROAD_AUTOLIST" / "catalog.json"
PROGRESS_FILE = BASE / "AUTOMATIONS" / "logs" / "gumroad_listing_progress.json"
SCREENSHOT_DIR = BASE / "AUTOMATIONS" / "logs"
LOG_FILE = BASE / "AUTOMATIONS" / "logs" / "gumroad_ab_lister.log"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
GUMROAD_NEW_PRODUCT_URL = "https://app.gumroad.com/products/new"
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 3  # seconds
AB_TIMEOUT = 30  # seconds per agent-browser command


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def log(msg: str, level: str = "INFO") -> None:
    """Print and append to log file."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Human-like delays
# ---------------------------------------------------------------------------
def human_delay(min_s: float = 1.0, max_s: float = 3.0) -> None:
    """Sleep a random duration to mimic human timing."""
    delay = random.uniform(min_s, max_s)
    time.sleep(delay)


# ---------------------------------------------------------------------------
# agent-browser wrapper
# ---------------------------------------------------------------------------
def ab_run(args: list[str], timeout: int = AB_TIMEOUT, verbose: bool = False) -> tuple[bool, str]:
    """
    Run an agent-browser CLI command.

    Returns (success: bool, stdout: str).
    """
    cmd = ["agent-browser"] + args
    if verbose:
        log(f"  CMD: {' '.join(cmd)}", "DEBUG")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if verbose and stdout:
            # Truncate very long output for readability
            display = stdout[:2000] + ("..." if len(stdout) > 2000 else "")
            log(f"  OUT: {display}", "DEBUG")
        if result.returncode != 0:
            if verbose and stderr:
                log(f"  ERR: {stderr}", "DEBUG")
            return False, stderr or stdout
        return True, stdout
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT after {timeout}s: {' '.join(cmd)}", "WARN")
        return False, "TIMEOUT"
    except FileNotFoundError:
        log("agent-browser not found in PATH. Install it first.", "ERROR")
        sys.exit(1)
    except Exception as exc:
        log(f"  Exception running agent-browser: {exc}", "ERROR")
        return False, str(exc)


def ab_run_retry(args: list[str], retries: int = MAX_RETRIES,
                 timeout: int = AB_TIMEOUT, verbose: bool = False) -> tuple[bool, str]:
    """Run an agent-browser command with retries and exponential backoff."""
    for attempt in range(1, retries + 1):
        ok, out = ab_run(args, timeout=timeout, verbose=verbose)
        if ok:
            return True, out
        if attempt < retries:
            wait = RETRY_BACKOFF_BASE * attempt + random.uniform(0, 1)
            log(f"  Retry {attempt}/{retries} in {wait:.1f}s ...", "WARN")
            time.sleep(wait)
    return False, out


# ---------------------------------------------------------------------------
# Snapshot parser — extract element references from accessibility tree
# ---------------------------------------------------------------------------
def take_snapshot(verbose: bool = False) -> str:
    """Take an accessibility snapshot and return the raw text."""
    ok, snap = ab_run(["snapshot"], timeout=15, verbose=verbose)
    if not ok:
        log("Failed to take snapshot", "WARN")
        return ""
    return snap


def find_ref_by_text(snapshot: str, text: str, partial: bool = True) -> str | None:
    """
    Search the accessibility tree text for an element reference (@eN)
    associated with the given text.

    Returns the @ref string (e.g. '@e12') or None.
    """
    lines = snapshot.split("\n")
    text_lower = text.lower()
    for line in lines:
        line_lower = line.lower()
        if (partial and text_lower in line_lower) or (not partial and text_lower == line_lower.strip()):
            # Look for @eN pattern in the same line
            match = re.search(r"(@e\d+)", line)
            if match:
                return match.group(1)
    return None


def find_ref_by_role(snapshot: str, role: str, name_hint: str = "") -> str | None:
    """
    Find an element ref by ARIA role and optional name hint.
    """
    lines = snapshot.split("\n")
    role_lower = role.lower()
    name_lower = name_hint.lower()
    for line in lines:
        line_lower = line.lower()
        if role_lower in line_lower:
            if name_lower and name_lower not in line_lower:
                continue
            match = re.search(r"(@e\d+)", line)
            if match:
                return match.group(1)
    return None


def find_all_refs_by_role(snapshot: str, role: str) -> list[tuple[str, str]]:
    """Return list of (ref, line_text) for all elements matching the role."""
    results = []
    lines = snapshot.split("\n")
    role_lower = role.lower()
    for line in lines:
        if role_lower in line.lower():
            match = re.search(r"(@e\d+)", line)
            if match:
                results.append((match.group(1), line.strip()))
    return results


# ---------------------------------------------------------------------------
# Catalog / Progress management
# ---------------------------------------------------------------------------
def load_catalog() -> list[dict]:
    """Load the product catalog from disk."""
    if not CATALOG.exists():
        log(f"Catalog not found at {CATALOG}", "ERROR")
        sys.exit(1)
    with open(CATALOG) as f:
        data = json.load(f)
    items = data.get("items", [])
    log(f"Loaded {len(items)} items from catalog")
    return items


def load_progress() -> dict:
    """Load listing progress from disk."""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            log("Progress file corrupt, starting fresh", "WARN")
    return {"listed": [], "failed": [], "history": []}


def save_progress(progress: dict) -> None:
    """Persist progress to disk."""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


# ---------------------------------------------------------------------------
# Product listing logic
# ---------------------------------------------------------------------------
def navigate_to_new_product(verbose: bool = False) -> bool:
    """Navigate to the Gumroad new product page."""
    log("  Navigating to new product page ...")
    ok, _ = ab_run_retry(["open", GUMROAD_NEW_PRODUCT_URL], verbose=verbose)
    if not ok:
        log("  Failed to navigate to new product page", "ERROR")
        return False
    # Wait for page load
    human_delay(2.0, 4.0)
    return True


def fill_product_name(name: str, snapshot: str, verbose: bool = False) -> bool:
    """Fill in the product name field."""
    log(f"  Filling product name: {name}")

    # Strategy 1: find by placeholder
    ok, _ = ab_run(["find", "placeholder", "Name", "fill", name], verbose=verbose)
    if ok:
        human_delay()
        return True

    # Strategy 2: find name input from snapshot
    ref = find_ref_by_text(snapshot, "Name")
    if ref:
        ok, _ = ab_run(["fill", ref, name], verbose=verbose)
        if ok:
            human_delay()
            return True

    # Strategy 3: try common selectors
    for sel in ['input[placeholder*="Name"]', 'input[name="name"]',
                'input[aria-label*="name" i]', 'input[type="text"]']:
        ok, _ = ab_run(["fill", sel, name], verbose=verbose)
        if ok:
            human_delay()
            return True

    log("  Could not find product name field", "WARN")
    return False


def fill_price(price_cents: int, snapshot: str, verbose: bool = False) -> bool:
    """Fill in the product price field."""
    price_dollars = price_cents / 100
    price_str = f"{price_dollars:.2f}" if price_dollars != int(price_dollars) else str(int(price_dollars))
    log(f"  Setting price: ${price_str}")

    # Strategy 1: find by placeholder
    ok, _ = ab_run(["find", "placeholder", "Price", "fill", price_str], verbose=verbose)
    if ok:
        human_delay()
        return True

    # Strategy 2: snapshot reference
    ref = find_ref_by_text(snapshot, "price")
    if not ref:
        ref = find_ref_by_role(snapshot, "spinbutton")
    if ref:
        ok, _ = ab_run(["fill", ref, price_str], verbose=verbose)
        if ok:
            human_delay()
            return True

    # Strategy 3: CSS selectors
    for sel in ['input[placeholder*="rice"]', 'input[name="price"]',
                'input[type="number"]', 'input[aria-label*="rice" i]']:
        ok, _ = ab_run(["fill", sel, price_str], verbose=verbose)
        if ok:
            human_delay()
            return True

    log("  Could not find price field", "WARN")
    return False


def click_create_button(snapshot: str, verbose: bool = False) -> bool:
    """Click the create / next / continue button on the new product form."""
    log("  Clicking create button ...")

    # Try text-based finding for various button labels
    for label in ["Create product", "Add product", "Create", "Next", "Continue", "Save"]:
        ok, _ = ab_run(["find", "text", label, "click"], verbose=verbose)
        if ok:
            human_delay(2.0, 4.0)
            return True

    # Try from snapshot
    for label in ["Create", "Add", "Next", "Continue", "Save"]:
        ref = find_ref_by_role(snapshot, "button", label)
        if ref:
            ok, _ = ab_run(["click", ref], verbose=verbose)
            if ok:
                human_delay(2.0, 4.0)
                return True

    log("  Could not find create button", "WARN")
    return False


def fill_description(description: str, verbose: bool = False) -> bool:
    """Fill in the product description in the editor page."""
    log("  Filling description ...")
    # Truncate very long descriptions
    desc = description[:3000]

    # Strategy 1: contenteditable / rich text editor
    for sel in ['div[contenteditable="true"]', '.ProseMirror', '.ql-editor',
                'textarea[name="description"]', '[data-testid="description"]']:
        ok, _ = ab_run(["click", sel], verbose=verbose)
        if ok:
            # Select all existing text and replace
            ab_run(["press", "Control+a"], verbose=verbose)
            time.sleep(0.3)
            ok2, _ = ab_run(["type", sel, desc], timeout=60, verbose=verbose)
            if ok2:
                human_delay()
                return True

    # Strategy 2: find by text label
    ok, _ = ab_run(["find", "text", "Description", "click"], verbose=verbose)
    if ok:
        human_delay(0.5, 1.0)
        ab_run(["press", "Tab"], verbose=verbose)
        time.sleep(0.3)
        # Type the description using keyboard
        # Split into chunks to avoid issues with very long text
        chunk_size = 500
        for i in range(0, len(desc), chunk_size):
            chunk = desc[i:i + chunk_size]
            ab_run(["press", "Control+a"], verbose=verbose) if i == 0 else None
            # Use eval to type since type command needs a selector
            escaped = chunk.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")
            ab_run(["eval", f"await page.keyboard.type('{escaped}', {{delay: 5}})"], timeout=60, verbose=verbose)
            human_delay(0.3, 0.8)
        return True

    # Strategy 3: snapshot-based approach
    snap = take_snapshot(verbose=verbose)
    ref = find_ref_by_text(snap, "description")
    if ref:
        ok, _ = ab_run(["click", ref], verbose=verbose)
        if ok:
            time.sleep(0.5)
            escaped = desc.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")
            ab_run(["eval", f"await page.keyboard.type('{escaped}', {{delay: 5}})"], timeout=60, verbose=verbose)
            human_delay()
            return True

    log("  Could not find description field", "WARN")
    return False


def add_tags(tags: list[str], verbose: bool = False) -> bool:
    """Add tags to the product."""
    if not tags:
        return True
    log(f"  Adding {len(tags)} tags ...")

    for tag in tags[:15]:  # Gumroad limits tags
        # Try to find tag input
        for sel in ['input[placeholder*="tag" i]', 'input[placeholder*="Tag" i]',
                    'input[name="tag"]', 'input[aria-label*="tag" i]']:
            ok, _ = ab_run(["fill", sel, tag], verbose=verbose)
            if ok:
                human_delay(0.3, 0.6)
                ab_run(["press", "Enter"], verbose=verbose)
                human_delay(0.3, 0.8)
                break
        else:
            # Try find command
            ok, _ = ab_run(["find", "placeholder", "Add a tag", "fill", tag], verbose=verbose)
            if ok:
                human_delay(0.3, 0.6)
                ab_run(["press", "Enter"], verbose=verbose)
                human_delay(0.3, 0.8)
            else:
                log(f"  Could not find tag input for tag: {tag}", "WARN")
                return False
    return True


def upload_file(file_path: Path, verbose: bool = False) -> bool:
    """Upload the product file (PDF)."""
    if not file_path.exists():
        log(f"  File not found: {file_path}", "WARN")
        return False
    log(f"  Uploading file: {file_path.name} ({file_path.stat().st_size / 1024:.0f} KB)")

    # Strategy 1: find file input and upload
    ok, _ = ab_run(["upload", 'input[type="file"]', str(file_path)], timeout=60, verbose=verbose)
    if ok:
        log("  File uploaded successfully")
        human_delay(3.0, 5.0)  # Wait for upload to process
        return True

    # Strategy 2: look for upload button/area and click it first
    for label in ["Upload", "Add file", "Choose file", "Add content", "Content"]:
        ok, _ = ab_run(["find", "text", label, "click"], verbose=verbose)
        if ok:
            human_delay(1.0, 2.0)
            # Now try the file input again
            ok2, _ = ab_run(["upload", 'input[type="file"]', str(file_path)], timeout=60, verbose=verbose)
            if ok2:
                log("  File uploaded successfully")
                human_delay(3.0, 5.0)
                return True

    # Strategy 3: snapshot-based
    snap = take_snapshot(verbose=verbose)
    refs = find_all_refs_by_role(snap, "button")
    for ref, text in refs:
        if any(kw in text.lower() for kw in ["upload", "file", "content", "add"]):
            ab_run(["click", ref], verbose=verbose)
            human_delay(1.0, 2.0)
            ok, _ = ab_run(["upload", 'input[type="file"]', str(file_path)], timeout=60, verbose=verbose)
            if ok:
                log("  File uploaded successfully")
                human_delay(3.0, 5.0)
                return True

    log("  Could not upload file", "WARN")
    return False


def save_or_publish(publish: bool, verbose: bool = False) -> bool:
    """Click save or publish button."""
    action = "Publishing" if publish else "Saving"
    log(f"  {action} product ...")

    # Try publish first if requested
    if publish:
        for label in ["Publish and continue", "Publish", "Save and continue", "Save"]:
            ok, _ = ab_run(["find", "text", label, "click"], verbose=verbose)
            if ok:
                human_delay(2.0, 4.0)
                return True
    else:
        for label in ["Save", "Save changes", "Save and continue", "Save draft"]:
            ok, _ = ab_run(["find", "text", label, "click"], verbose=verbose)
            if ok:
                human_delay(2.0, 4.0)
                return True

    # Snapshot approach
    snap = take_snapshot(verbose=verbose)
    for keyword in (["Publish", "Save"] if publish else ["Save"]):
        ref = find_ref_by_role(snap, "button", keyword)
        if ref:
            ok, _ = ab_run(["click", ref], verbose=verbose)
            if ok:
                human_delay(2.0, 4.0)
                return True

    log(f"  Could not find {action.lower()} button", "WARN")
    return False


def take_verification_screenshot(sku: str, verbose: bool = False) -> str | None:
    """Take a screenshot for verification and return the path."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ss_name = f"gumroad_listed_{sku}_{ts}.png"
    ss_path = SCREENSHOT_DIR / ss_name
    ss_path.parent.mkdir(parents=True, exist_ok=True)
    ok, _ = ab_run(["screenshot", str(ss_path)], verbose=verbose)
    if ok:
        log(f"  Screenshot: {ss_path}")
        return str(ss_path)
    log("  Screenshot failed", "WARN")
    return None


def get_current_url(verbose: bool = False) -> str:
    """Get the current browser URL."""
    ok, url = ab_run(["get", "url"], verbose=verbose)
    return url if ok else ""


def list_single_product(item: dict, dry_run: bool = False, verbose: bool = False) -> bool:
    """
    List a single product on Gumroad.

    Steps:
        1. Navigate to new product page
        2. Take snapshot of the accessibility tree
        3. Fill name
        4. Fill price
        5. Click create
        6. Wait for editor to load, take new snapshot
        7. Fill description
        8. Add tags
        9. Upload file
        10. Save/publish
        11. Verification screenshot

    Returns True on success, False on failure.
    """
    sku = item.get("sku", "unknown")
    name = item.get("name", "Untitled")
    price_cents = item.get("price_cents", 0)
    description = item.get("description_md", "")
    tags = item.get("tags", [])
    file_relpath = item.get("file_relpath", "")
    publish = item.get("publish", True)
    file_path = BASE / file_relpath if file_relpath else None

    price_str = f"${price_cents / 100:.2f}"

    log(f"\n{'='*60}")
    log(f"  Product: {name}")
    log(f"  SKU:     {sku}")
    log(f"  Price:   {price_str}")
    log(f"  Tags:    {', '.join(tags)}")
    log(f"  File:    {file_path.name if file_path and file_path.exists() else 'MISSING'}")
    log(f"  Publish: {publish}")

    if dry_run:
        log("  [DRY RUN] Would list this product -- skipping")
        return True

    # ---------------------------------------------------------------
    # Step 1: Navigate
    # ---------------------------------------------------------------
    if not navigate_to_new_product(verbose=verbose):
        return False

    # ---------------------------------------------------------------
    # Step 2: Take snapshot of the new product form
    # ---------------------------------------------------------------
    snap = take_snapshot(verbose=verbose)
    if verbose and snap:
        log(f"  Snapshot length: {len(snap)} chars", "DEBUG")

    # ---------------------------------------------------------------
    # Step 3: Fill product name
    # ---------------------------------------------------------------
    if not fill_product_name(name, snap, verbose=verbose):
        log("  CRITICAL: Could not fill product name -- aborting product", "ERROR")
        take_verification_screenshot(f"{sku}_error_name", verbose=verbose)
        return False

    # ---------------------------------------------------------------
    # Step 4: Fill price
    # ---------------------------------------------------------------
    fill_price(price_cents, snap, verbose=verbose)
    # Price failure is non-fatal; can be edited later

    # ---------------------------------------------------------------
    # Step 5: Click create / continue
    # ---------------------------------------------------------------
    if not click_create_button(snap, verbose=verbose):
        log("  CRITICAL: Could not click create button -- aborting product", "ERROR")
        take_verification_screenshot(f"{sku}_error_create", verbose=verbose)
        return False

    # Wait for the product editor page to load
    log("  Waiting for editor page to load ...")
    ab_run(["wait", "3000"], verbose=verbose)
    human_delay(2.0, 3.0)

    # ---------------------------------------------------------------
    # Step 6: Take a new snapshot of the editor page
    # ---------------------------------------------------------------
    editor_snap = take_snapshot(verbose=verbose)

    # ---------------------------------------------------------------
    # Step 7: Fill description
    # ---------------------------------------------------------------
    fill_description(description, verbose=verbose)

    # ---------------------------------------------------------------
    # Step 8: Add tags
    # ---------------------------------------------------------------
    add_tags(tags, verbose=verbose)

    # ---------------------------------------------------------------
    # Step 9: Upload file
    # ---------------------------------------------------------------
    if file_path and file_path.exists():
        upload_file(file_path, verbose=verbose)
    elif file_path:
        log(f"  File not found: {file_path}", "WARN")

    # ---------------------------------------------------------------
    # Step 10: Save / Publish
    # ---------------------------------------------------------------
    saved = save_or_publish(publish, verbose=verbose)
    if not saved:
        log("  WARNING: Save/publish may have failed -- check manually", "WARN")
        take_verification_screenshot(f"{sku}_error_save", verbose=verbose)
        # Still treat as partial success since the product was created

    # Wait for save to process
    human_delay(2.0, 3.0)

    # ---------------------------------------------------------------
    # Step 11: Verification screenshot
    # ---------------------------------------------------------------
    take_verification_screenshot(sku, verbose=verbose)

    # Capture the final URL for logging
    final_url = get_current_url(verbose=verbose)
    if final_url:
        log(f"  Final URL: {final_url}")

    log(f"  LISTED: {name}")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gumroad Auto-Lister using agent-browser CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 TOOLS/ab_gumroad_lister.py --dry-run           # Preview products
  python3 TOOLS/ab_gumroad_lister.py --max 1 --verbose   # List 1 product with debug output
  python3 TOOLS/ab_gumroad_lister.py                      # List all pending products
        """,
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview products without actually listing them")
    parser.add_argument("--max", type=int, default=0,
                        help="Maximum number of products to list (0 = all)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed agent-browser command output")
    parser.add_argument("--sku", type=str, default="",
                        help="List only the product with this SKU")
    parser.add_argument("--reset-progress", action="store_true",
                        help="Clear progress file and start fresh")
    args = parser.parse_args()

    log("=" * 60)
    log("Gumroad Auto-Lister (agent-browser)")
    log("=" * 60)

    # Verify agent-browser is reachable
    ok, version = ab_run(["get", "url"], verbose=args.verbose)
    if not ok:
        log("Cannot connect to agent-browser. Make sure:", "ERROR")
        log("  1. agent-browser is installed (which agent-browser)", "ERROR")
        log("  2. A browser session is open and connected", "ERROR")
        log("  3. You are logged into Gumroad in that browser", "ERROR")
        sys.exit(1)
    log(f"Connected to browser. Current URL: {version}")

    # Load catalog
    items = load_catalog()

    # Load or reset progress
    if args.reset_progress:
        progress = {"listed": [], "failed": [], "history": []}
        save_progress(progress)
        log("Progress reset")
    else:
        progress = load_progress()

    # Filter
    if args.sku:
        pending = [i for i in items if i["sku"] == args.sku]
        if not pending:
            log(f"SKU '{args.sku}' not found in catalog", "ERROR")
            sys.exit(1)
    else:
        already = set(progress.get("listed", []))
        pending = [i for i in items if i["sku"] not in already]

    if args.max > 0:
        pending = pending[:args.max]

    log(f"")
    log(f"  Total in catalog:  {len(items)}")
    log(f"  Already listed:    {len(progress.get('listed', []))}")
    log(f"  Previously failed: {len(progress.get('failed', []))}")
    log(f"  To list now:       {len(pending)}")
    log(f"  Dry run:           {args.dry_run}")
    log(f"")

    if not pending:
        log("Nothing to list. All products are already listed.")
        return

    succeeded = 0
    failed = 0

    for idx, item in enumerate(pending, 1):
        log(f"\n--- Product {idx}/{len(pending)} ---")
        try:
            success = list_single_product(item, dry_run=args.dry_run, verbose=args.verbose)
        except KeyboardInterrupt:
            log("\nInterrupted by user", "WARN")
            save_progress(progress)
            sys.exit(130)
        except Exception as exc:
            log(f"  Unexpected error: {exc}", "ERROR")
            success = False
            # Take an error screenshot
            try:
                take_verification_screenshot(f"{item.get('sku', 'unknown')}_exception", verbose=args.verbose)
            except Exception:
                pass

        if success:
            succeeded += 1
            if not args.dry_run:
                if item["sku"] not in progress.get("listed", []):
                    progress.setdefault("listed", []).append(item["sku"])
                # Remove from failed list if it was there
                if item["sku"] in progress.get("failed", []):
                    progress["failed"].remove(item["sku"])
                progress.setdefault("history", []).append({
                    "sku": item["sku"],
                    "name": item["name"],
                    "status": "listed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                save_progress(progress)
        else:
            failed += 1
            if not args.dry_run:
                if item["sku"] not in progress.get("failed", []):
                    progress.setdefault("failed", []).append(item["sku"])
                progress.setdefault("history", []).append({
                    "sku": item["sku"],
                    "name": item["name"],
                    "status": "failed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                save_progress(progress)

        # Human-like delay between products
        if idx < len(pending):
            between_delay = random.uniform(5, 12)
            log(f"  Waiting {between_delay:.0f}s before next product ...")
            time.sleep(between_delay)

    # Final summary
    log(f"\n{'='*60}")
    log(f"  SUMMARY")
    log(f"  Succeeded: {succeeded}")
    log(f"  Failed:    {failed}")
    log(f"  Progress:  {PROGRESS_FILE}")
    log(f"  Log:       {LOG_FILE}")
    log(f"{'='*60}")


if __name__ == "__main__":
    main()
