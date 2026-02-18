#!/usr/bin/env python3
"""
PRINTMAXX Browser Automation - Account Setup
Handles: Decodo, GoLogin, SMSPool, ProtonMail, X accounts
Human handles: Payments only

COUPON: RESI50 = 50% off residential proxies for a year!
"""

from playwright.sync_api import sync_playwright
import time
import os

# Config
USER_DATA_DIR = os.path.expanduser("~/Documents/PRINTMAXX_BROWSER_DATA")
os.makedirs(USER_DATA_DIR, exist_ok=True)

# URLs
URLS = {
    "decodo_pricing": "https://decodo.com/proxies/residential-proxies/pricing",
    "decodo_signup": "https://decodo.com/",
    "gologin": "https://gologin.com/",
    "smspool": "https://smspool.net/",
    "protonmail": "https://proton.me/mail/signup",
    "x_signup": "https://x.com/i/flow/signup",
    "gumroad": "https://gumroad.com/"
}

def launch_browser(headless=False):
    """Launch persistent browser session"""
    p = sync_playwright().start()
    browser = p.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=headless,
        viewport={"width": 1280, "height": 900},
        args=['--disable-blink-features=AutomationControlled'],
        slow_mo=100  # Slow down for visibility
    )
    return p, browser

def wait_for_input(msg):
    """Pause and wait for user"""
    print(f"\n>>> {msg}")
    print(">>> Press ENTER to continue...")
    input()

def main():
    print("=" * 60)
    print("PRINTMAXX ACCOUNT SETUP AUTOMATION")
    print("=" * 60)
    print("\n[!] COUPON CODE: RESI50 (50% off residential proxies!)\n")

    p, browser = launch_browser(headless=False)
    page = browser.pages[0] if browser.pages else browser.new_page()

    # ========== PHASE 1: DECODO ==========
    print("\n[PHASE 1] DECODO PROXIES")
    print("-" * 40)
    print("Opening Decodo pricing page...")

    page.goto(URLS["decodo_pricing"])
    time.sleep(2)

    print("Page loaded!")
    print("\nSTEPS:")
    print("1. Select 'Residential Proxies' starter plan (1GB)")
    print("2. Click 'Get Started' or 'Sign Up'")
    print("3. Create account with email")
    print("4. Apply coupon: RESI50")
    print("5. YOU complete payment")

    wait_for_input("Complete Decodo signup + payment, then press ENTER")

    # ========== PHASE 1b: GoLogin ==========
    print("\n[PHASE 1b] GOLOGIN DOWNLOAD")
    print("-" * 40)

    page.goto(URLS["gologin"])
    time.sleep(2)

    print("STEPS:")
    print("1. Click 'Download' or 'Get Started Free'")
    print("2. Download the macOS app")
    print("3. Install and create free account (3 profiles)")

    wait_for_input("Download + install GoLogin, then press ENTER")

    # ========== PHASE 2: SMSPool ==========
    print("\n[PHASE 2] SMSPOOL PHONE NUMBERS")
    print("-" * 40)

    page.goto(URLS["smspool"])
    time.sleep(2)

    print("STEPS:")
    print("1. Click 'Sign Up'")
    print("2. Create account")
    print("3. Add $10 credit (YOU pay)")
    print("4. We'll buy 6 numbers for X verification later")

    wait_for_input("Complete SMSPool signup + $10 payment, then press ENTER")

    # ========== PHASE 3: ProtonMail ==========
    print("\n[PHASE 3] PROTONMAIL EMAILS")
    print("-" * 40)
    print("[!] Use Mullvad VPN - rotate servers between each signup!")

    emails = [
        ("printmaxxer@protonmail.com", "Sweden"),
        ("stackpilot.ai@protonmail.com", "Germany"),
        ("dailyanchor.co@protonmail.com", "Netherlands"),
        ("3hourphysique@protonmail.com", "Switzerland"),
        ("autoreplyai@protonmail.com", "Finland"),
        ("enterpriseauto@protonmail.com", "Norway"),
    ]

    for email, vpn_location in emails:
        print(f"\n>>> Creating: {email}")
        print(f">>> VPN Location: {vpn_location}")

        page.goto(URLS["protonmail"])
        time.sleep(2)

        wait_for_input(f"1. Connect Mullvad to {vpn_location}\n2. Create {email}\n3. Complete signup, then press ENTER")

    print("\n[!] All 6 emails created!")

    # ========== PHASE 4: X Accounts ==========
    print("\n[PHASE 4] X ACCOUNT CREATION")
    print("-" * 40)
    print("[!] Use GoLogin profiles for each account!")

    accounts = [
        ("Account1", "@PRINTMAXXER", "printmaxxer@protonmail.com"),
        ("Account2", "@StackPilotAI", "stackpilot.ai@protonmail.com"),
        ("Account3", "@DailyAnchorHQ", "dailyanchor.co@protonmail.com"),
        ("Account4", "@3HourPhysique", "3hourphysique@protonmail.com"),
        ("Account5", "@AutoReplyAI", "autoreplyai@protonmail.com"),
        ("Account6", "@EntAutoSolns", "enterpriseauto@protonmail.com"),
    ]

    for profile, handle, email in accounts:
        print(f"\n>>> GoLogin Profile: {profile}")
        print(f">>> Handle: {handle}")
        print(f">>> Email: {email}")
        print("\nSTEPS:")
        print(f"1. Open GoLogin profile '{profile}'")
        print(f"2. Go to x.com/i/flow/signup")
        print(f"3. Use email: {email}")
        print("4. Get phone from SMSPool (Twitter/X service)")
        print("5. Complete verification")
        print("6. Set bio from BRANDED_ACCOUNTS.md")

        wait_for_input(f"Complete {handle} account setup, then press ENTER")

    # ========== PHASE 6: Gumroad ==========
    print("\n[PHASE 6] GUMROAD SETUP")
    print("-" * 40)

    page.goto(URLS["gumroad"])
    time.sleep(2)

    print("STEPS:")
    print("1. Sign up with printmaxxer@protonmail.com")
    print("2. Verify email")
    print("3. Create 3 products (copy from PRODUCTS/gumroad_copy/*.md)")
    print("   - AI Clarity Stack ($47)")
    print("   - Daily Anchor System ($27)")
    print("   - 3-Hour Physique ($47)")

    wait_for_input("Complete Gumroad setup, then press ENTER")

    # ========== DONE ==========
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nCHECKLIST:")
    print("[ ] Decodo proxies active")
    print("[ ] GoLogin installed + 6 profiles configured")
    print("[ ] SMSPool funded ($10)")
    print("[ ] 6 ProtonMail emails created")
    print("[ ] 6 X accounts created")
    print("[ ] Gumroad + 3 products live")
    print("\nNEXT: Start Week 1 warmup (see HANDOFF_RETARDMAXX_SETUP.md Phase 5)")

    browser.close()
    p.stop()

if __name__ == "__main__":
    main()
