#!/usr/bin/env python3
"""
PRINTMAXX Auto Account Creator
Browser automation for platform signups using Playwright.

Usage:
    python3 auto_account_creator.py --platform gumroad --email you@email.com
    python3 auto_account_creator.py --platform buffer --email you@email.com --headful
    python3 auto_account_creator.py --all --email you@email.com
    python3 auto_account_creator.py --list  # show supported platforms
    python3 auto_account_creator.py --platform gumroad --email you@email.com --proxy socks5://user:pass@host:port

Supports: Gumroad, Buffer, Beehiiv, Surge.sh (via npm)
"""

import argparse
import json
import os
import random
import string
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "screenshots"
SECRETS_FILE = PROJECT_ROOT / "SECRETS" / "PAYMENT_INFO.md"
ACCOUNTS_CSV = PROJECT_ROOT / "LEDGER" / "ACCOUNTS.csv"
LOG_FILE = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "account_creation.log"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
(PROJECT_ROOT / "AUTOMATIONS" / "logs").mkdir(parents=True, exist_ok=True)

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

PLATFORMS = {
    "gumroad": {
        "name": "Gumroad",
        "url": "https://app.gumroad.com/signup",
        "type": "browser",
        "fields": {
            "email": "label:has-text('Email') + input, input[name='email'], input[type='email'], #email, input[placeholder*='email' i]",
            "password": "label:has-text('Password') + input, input[name='password'], input[type='password'], #password, input[placeholder*='password' i]",
        },
        "submit": "button:has-text('Create account'), button[type='submit'], input[type='submit'], button:has-text('Sign up')",
        "success_indicators": ["dashboard", "settings", "products", "welcome"],
    },
    "buffer": {
        "name": "Buffer",
        "url": "https://login.buffer.com/signup",
        "type": "browser",
        "fields": {
            "email": "input[name='email'], input[type='email'], #email",
            "password": "input[name='password'], input[type='password'], #password",
        },
        "submit": "button[type='submit'], button:has-text('Sign Up'), button:has-text('Get started')",
        "success_indicators": ["dashboard", "publish", "channels", "welcome", "onboarding"],
    },
    "beehiiv": {
        "name": "Beehiiv",
        "url": "https://www.beehiiv.com/create",
        "type": "browser",
        "fields": {
            "email": "input[name='email'], input[type='email'], #email",
            "password": "input[name='password'], input[type='password'], #password",
            "name": "input[name='name'], input[name='full_name'], input[placeholder*='name' i]",
        },
        "submit": "button[type='submit'], button:has-text('Create'), button:has-text('Sign up'), button:has-text('Get started')",
        "success_indicators": ["dashboard", "publications", "welcome", "onboarding"],
    },
    "surge": {
        "name": "Surge.sh",
        "url": None,
        "type": "cli",
        "command": "npx surge --help",
        "note": "Surge creates account on first deploy: cd your-site && npx surge",
    },
}


def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%"
    pw = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%"),
    ]
    pw += [random.choice(chars) for _ in range(length - 4)]
    random.shuffle(pw)
    return "".join(pw)


def human_delay(min_s=0.5, max_s=2.0):
    time.sleep(random.uniform(min_s, max_s))


def human_type(page, selector, text):
    """Type text with human-like delays between keystrokes."""
    element = page.locator(selector).first
    element.click()
    human_delay(0.3, 0.7)
    for char in text:
        element.press_sequentially(char, delay=random.randint(30, 120))
    human_delay(0.2, 0.5)


def find_and_fill(page, selectors_str, value, field_name="field"):
    """Try multiple selectors to find and fill a field."""
    # First try Playwright's get_by_label (most reliable for accessible forms)
    label_names = {
        "email": ["Email", "Email address", "Your email"],
        "password": ["Password", "Create password", "Your password"],
        "name": ["Name", "Full name", "Your name"],
    }
    if field_name in label_names:
        for label in label_names[field_name]:
            try:
                loc = page.get_by_label(label, exact=False).first
                if loc.is_visible(timeout=1000):
                    loc.click()
                    human_delay(0.2, 0.5)
                    loc.fill("")
                    loc.press_sequentially(value, delay=random.randint(30, 100))
                    human_delay(0.3, 0.8)
                    log(f"Filled {field_name} using label: {label}")
                    return True
            except Exception:
                continue

    # Fallback to CSS selectors
    selectors = [s.strip() for s in selectors_str.split(",")]
    for selector in selectors:
        try:
            loc = page.locator(selector).first
            if loc.is_visible(timeout=2000):
                loc.click()
                human_delay(0.2, 0.5)
                loc.fill("")
                loc.press_sequentially(value, delay=random.randint(30, 100))
                human_delay(0.3, 0.8)
                log(f"Filled {field_name} using selector: {selector}")
                return True
        except Exception:
            continue
    log(f"Could not find {field_name} field with any selector", "WARN")
    return False


def click_submit(page, selectors_str):
    """Try multiple selectors to find and click submit."""
    selectors = [s.strip() for s in selectors_str.split(",")]
    for selector in selectors:
        try:
            loc = page.locator(selector).first
            if loc.is_visible(timeout=2000):
                human_delay(0.5, 1.5)
                loc.click()
                log(f"Clicked submit using selector: {selector}")
                return True
        except Exception:
            continue
    log("Could not find submit button with any selector", "WARN")
    return False


def screenshot(page, platform_name, stage):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOTS_DIR / f"{platform_name}_{stage}_{ts}.png"
    try:
        page.screenshot(path=str(path), full_page=True)
        log(f"Screenshot saved: {path}")
    except Exception as e:
        log(f"Screenshot failed: {e}", "WARN")
    return path


def check_success(page, indicators):
    """Check if signup succeeded by looking at URL and page content."""
    current_url = page.url.lower()
    for indicator in indicators:
        if indicator in current_url:
            return True
    try:
        content = page.content().lower()
        for indicator in indicators:
            if indicator in content:
                return True
    except Exception:
        pass
    return False


def save_account(platform, email, password, status, notes=""):
    """Save account info to a local JSON file (gitignored via SECRETS/)."""
    accounts_file = PROJECT_ROOT / "SECRETS" / "created_accounts.json"
    accounts = []
    if accounts_file.exists():
        try:
            accounts = json.loads(accounts_file.read_text())
        except Exception:
            accounts = []

    accounts.append({
        "platform": platform,
        "email": email,
        "password": password,
        "status": status,
        "notes": notes,
        "created_at": datetime.now().isoformat(),
    })

    accounts_file.write_text(json.dumps(accounts, indent=2))
    log(f"Account saved to {accounts_file}")


def create_browser_account(platform_key, email, password, headful=False, proxy=None):
    """Create account using Playwright browser automation."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log("Playwright not installed. Run: pip install playwright && python3 -m playwright install chromium", "ERROR")
        return False

    platform = PLATFORMS[platform_key]
    log(f"Creating {platform['name']} account for {email}")

    with sync_playwright() as p:
        launch_args = {
            "headless": not headful,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        }
        if proxy:
            launch_args["proxy"] = {"server": proxy}

        browser = p.chromium.launch(**launch_args)
        context = browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            timezone_id="America/New_York",
        )

        # Remove webdriver detection
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        """)

        page = context.new_page()

        try:
            log(f"Navigating to {platform['url']}")
            page.goto(platform["url"], wait_until="domcontentloaded", timeout=30000)
            # Extra wait for JS-heavy pages to render forms
            human_delay(3, 5)
            screenshot(page, platform_key, "01_loaded")

            # Handle cookie banners (be very specific to avoid clicking OAuth buttons)
            for cookie_sel in [
                "[class*='cookie'] button:has-text('Accept')",
                "[class*='cookie'] button:has-text('Got it')",
                "[class*='consent'] button:has-text('Accept')",
                "[id*='cookie'] button",
                "div[role='dialog'] button:has-text('Accept')",
                "div[role='dialog'] button:has-text('Got it')",
            ]:
                try:
                    loc = page.locator(cookie_sel).first
                    if loc.is_visible(timeout=500):
                        loc.click()
                        human_delay(0.5, 1)
                        break
                except Exception:
                    continue

            # Fill name field if present (Beehiiv)
            if "name" in platform.get("fields", {}):
                find_and_fill(page, platform["fields"]["name"], "PrintMaxx", "name")

            # Fill email
            email_filled = find_and_fill(page, platform["fields"]["email"], email, "email")
            if not email_filled:
                screenshot(page, platform_key, "ERROR_no_email_field")
                log(f"Could not find email field on {platform['name']}", "ERROR")
                save_account(platform["name"], email, password, "FAILED", "Could not find email field")
                browser.close()
                return False

            # Fill password
            pw_filled = find_and_fill(page, platform["fields"]["password"], password, "password")
            if not pw_filled:
                screenshot(page, platform_key, "ERROR_no_password_field")
                log(f"Could not find password field on {platform['name']}", "ERROR")
                save_account(platform["name"], email, password, "FAILED", "Could not find password field")
                browser.close()
                return False

            screenshot(page, platform_key, "02_filled")

            # Click submit
            submitted = click_submit(page, platform["submit"])
            if not submitted:
                # Try pressing Enter as fallback
                page.keyboard.press("Enter")
                log("Used Enter key as submit fallback")

            # Wait for navigation/response
            human_delay(3, 6)
            screenshot(page, platform_key, "03_submitted")

            # Check for CAPTCHA
            page_text = page.content().lower()
            captcha_indicators = [
                "recaptcha", "captcha", "hcaptcha", "turnstile",
                "challenge-running", "g-recaptcha",
            ]
            has_captcha = any(c in page_text for c in captcha_indicators)

            if has_captcha:
                log(f"CAPTCHA detected on {platform['name']}. Form was filled correctly.", "WARN")
                log("Human must complete CAPTCHA manually. Use --headful mode.", "WARN")
                screenshot(page, platform_key, "04_captcha")
                save_account(platform["name"], email, password, "CAPTCHA_BLOCKED",
                             "Form filled, CAPTCHA appeared. Use --headful to complete manually.")
                if headful:
                    log("Waiting 60s for manual CAPTCHA solve...", "INFO")
                    human_delay(60, 65)
                    screenshot(page, platform_key, "05_after_captcha_wait")
                    if check_success(page, platform["success_indicators"]):
                        log(f"Account created after manual CAPTCHA on {platform['name']}", "SUCCESS")
                        save_account(platform["name"], email, password, "CREATED",
                                     "Created after manual CAPTCHA solve")
            else:
                # Check for visible error messages (not just "error" anywhere in HTML)
                error_indicators = [
                    "already registered",
                    "already exists",
                    "already taken",
                    "invalid email",
                    "password too short",
                    "password must",
                    "try again later",
                    "account already",
                ]

                has_error = False
                error_msg = ""
                # Check visible text, not full HTML source
                try:
                    visible_text = page.inner_text("body").lower()
                except Exception:
                    visible_text = page_text

                for err in error_indicators:
                    if err in visible_text:
                        has_error = True
                        error_msg = err
                        break

                if has_error:
                    log(f"Signup error: '{error_msg}' found on page", "WARN")
                    screenshot(page, platform_key, "04_error")
                    save_account(platform["name"], email, password, "FAILED", f"Error: {error_msg}")
                elif check_success(page, platform["success_indicators"]):
                    log(f"Account created successfully on {platform['name']}", "SUCCESS")
                    screenshot(page, platform_key, "04_success")
                    save_account(platform["name"], email, password, "CREATED", "Auto-created via Playwright")
                else:
                    log(f"Signup submitted on {platform['name']}. Check email for verification.", "INFO")
                    screenshot(page, platform_key, "04_submitted")
                    save_account(platform["name"], email, password, "NEEDS_VERIFICATION",
                                 "Check email for verification link")

            # Wait a bit more in headful mode so user can see
            if headful:
                human_delay(5, 10)

            browser.close()
            # CAPTCHA = partial success (form worked, needs human)
            # has_error only defined in the else branch
            if has_captcha:
                return True  # form filling succeeded
            return not has_error

        except Exception as e:
            log(f"Error creating {platform['name']} account: {e}", "ERROR")
            try:
                screenshot(page, platform_key, "ERROR_exception")
            except Exception:
                pass
            save_account(platform["name"], email, password, "FAILED", str(e))
            browser.close()
            return False


def create_surge_account(email):
    """Surge.sh creates account on first deploy. Just verify npm/npx works."""
    import subprocess
    log("Surge.sh account creation works via CLI on first deploy")
    log("Run: cd your-site-dir && npx surge")
    log(f"When prompted, enter email: {email}")

    try:
        result = subprocess.run(
            ["npx", "surge", "--help"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            log("Surge CLI is available and working")
            save_account("Surge.sh", email, "N/A - set during first deploy", "READY",
                         "Run 'npx surge' in a site directory to create account")
            return True
        else:
            log(f"Surge CLI error: {result.stderr}", "WARN")
            return False
    except FileNotFoundError:
        log("npx not found. Install Node.js first.", "ERROR")
        return False
    except Exception as e:
        log(f"Surge check failed: {e}", "ERROR")
        return False


def list_platforms():
    print("\nSupported Platforms:")
    print("-" * 60)
    for key, p in PLATFORMS.items():
        ptype = p["type"]
        url = p.get("url", "CLI-based")
        print(f"  {key:12s}  {p['name']:12s}  [{ptype:7s}]  {url}")
    print()
    print("Usage:")
    print("  python3 auto_account_creator.py --platform gumroad --email you@email.com")
    print("  python3 auto_account_creator.py --all --email you@email.com")
    print("  python3 auto_account_creator.py --platform buffer --email you@email.com --headful")
    print()


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Auto Account Creator")
    parser.add_argument("--platform", choices=list(PLATFORMS.keys()), help="Platform to create account on")
    parser.add_argument("--all", action="store_true", help="Create accounts on all platforms")
    parser.add_argument("--list", action="store_true", help="List supported platforms")
    parser.add_argument("--email", default="fnsmdehip@proton.me", help="Email for signup")
    parser.add_argument("--password", default=None, help="Password (auto-generated if not set)")
    parser.add_argument("--headful", action="store_true", help="Show browser window")
    parser.add_argument("--proxy", default=None, help="Proxy URL (socks5://user:pass@host:port)")
    args = parser.parse_args()

    if args.list:
        list_platforms()
        return

    if not args.platform and not args.all:
        parser.print_help()
        return

    password = args.password or generate_password()
    log(f"Generated password: {password}")

    platforms_to_create = list(PLATFORMS.keys()) if args.all else [args.platform]
    results = {}

    for platform_key in platforms_to_create:
        platform = PLATFORMS[platform_key]
        log(f"\n{'='*50}")
        log(f"Processing: {platform['name']}")
        log(f"{'='*50}")

        if platform["type"] == "cli":
            success = create_surge_account(args.email)
        else:
            per_platform_pw = args.password or generate_password()
            success = create_browser_account(
                platform_key, args.email, per_platform_pw,
                headful=args.headful, proxy=args.proxy
            )

        results[platform_key] = success
        if args.all:
            human_delay(5, 10)  # delay between platforms

    # Summary
    print(f"\n{'='*50}")
    print("RESULTS SUMMARY")
    print(f"{'='*50}")
    for platform_key, success in results.items():
        status = "OK" if success else "FAILED/NEEDS_REVIEW"
        print(f"  {PLATFORMS[platform_key]['name']:12s}  {status}")

    print(f"\nScreenshots: {SCREENSHOTS_DIR}")
    print(f"Accounts:    {PROJECT_ROOT / 'SECRETS' / 'created_accounts.json'}")
    print(f"Log:         {LOG_FILE}")


if __name__ == "__main__":
    main()
