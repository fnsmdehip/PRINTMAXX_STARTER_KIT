#!/usr/bin/env python3

from __future__ import annotations
"""
Platform Account Creator - Automated account setup checklists and tab opener.

Generates platform-specific signup checklists, pulls profile content from
existing PRODUCTS/ listings, reads SECRETS/PAYMENT_INFO.md for form data,
opens browser tabs, tracks creation status in LEDGER/ACCOUNTS.csv.

Usage:
    python3 platform_account_creator.py --all                  # Show all platforms
    python3 platform_account_creator.py --platform gumroad     # Single platform
    python3 platform_account_creator.py --open-tabs            # Open all signup URLs
    python3 platform_account_creator.py --open-tabs --platform fiverr
    python3 platform_account_creator.py --status               # Show account status
    python3 platform_account_creator.py --verify               # Run verification checks
    python3 platform_account_creator.py --mark-done gumroad    # Mark platform as created

Supported: gumroad, fiverr, upwork, etsy, redbubble, stripe, buffer, beehiiv
"""

import os
import sys
import csv
import argparse
import subprocess
import platform as platform_mod
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict

# Project root for guardrails
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
PRODUCTS_DIR = PROJECT_ROOT / "PRODUCTS"
SECRETS_DIR = PROJECT_ROOT / "SECRETS"


def safe_path(target: Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def open_url(url: str):
    """Open URL in default browser using system command."""
    system = platform_mod.system()
    try:
        if system == 'Darwin':
            subprocess.run(['open', url], check=True, timeout=10)
        elif system == 'Linux':
            subprocess.run(['xdg-open', url], check=True, timeout=10)
        elif system == 'Windows':
            subprocess.run(['start', url], shell=True, check=True, timeout=10)
        else:
            print(f"[WARN] Unknown OS. Open manually: {url}")
            return False
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print(f"[WARN] Could not open: {url}")
        return False


class PaymentInfoReader:
    """Read SECRETS/PAYMENT_INFO.md for form filling hints."""

    def __init__(self):
        self.info_path = SECRETS_DIR / "PAYMENT_INFO.md"
        self.data = {}
        self._load()

    def _load(self):
        """Parse the PAYMENT_INFO.md key=value pairs."""
        if not self.info_path.exists():
            return

        try:
            with open(self.info_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#') and not line.startswith('##'):
                        key, _, value = line.partition('=')
                        key = key.strip()
                        value = value.strip()
                        if value:
                            self.data[key] = value
        except Exception:
            pass

    def get(self, key: str, default: str = "") -> str:
        return self.data.get(key, default)

    def has_info(self) -> bool:
        return bool(self.data)

    def get_email(self) -> str:
        return self.get('EMAIL', '')

    def get_name(self) -> str:
        return self.get('FULL_NAME', '')

    def get_platform_creds(self, platform_name: str) -> Dict[str, str]:
        """Get platform-specific credentials."""
        prefix = platform_name.upper()
        creds = {}
        for key, value in self.data.items():
            if key.startswith(prefix + '_'):
                short_key = key[len(prefix) + 1:]
                creds[short_key] = value
        return creds


class ProductContentScanner:
    """Scan PRODUCTS/ for existing content to use in platform profiles."""

    def __init__(self):
        self.products_dir = PRODUCTS_DIR

    def get_gumroad_content(self) -> Dict:
        """Scan Gumroad listings for profile content."""
        content = {'listings': [], 'categories': set()}
        gumroad_dir = self.products_dir / "GUMROAD_INSTANT_UPLOAD"
        if gumroad_dir.exists():
            for f in sorted(gumroad_dir.iterdir()):
                if f.suffix == '.md' and f.stem not in ('README', 'LISTING_METADATA', 'WHOP_LISTINGS_QUICK'):
                    content['listings'].append(f.stem)
                    content['categories'].add('digital products')

        # Also check top-level gumroad files
        for f in self.products_dir.iterdir():
            if 'gumroad' in f.name.lower() and f.suffix == '.md':
                content['listings'].append(f.stem)

        return content

    def get_fiverr_content(self) -> Dict:
        """Scan Fiverr gig listings."""
        content = {'gigs': [], 'categories': set()}
        fiverr_dir = self.products_dir / "FIVERR_INSTANT_UPLOAD"
        if fiverr_dir.exists():
            for f in sorted(fiverr_dir.iterdir()):
                if f.suffix == '.md' and f.stem not in ('README', 'FIVERR_METADATA'):
                    content['gigs'].append(f.stem)

        freelance_dir = self.products_dir / "FREELANCE_LISTINGS_READY"
        if freelance_dir.exists():
            for f in freelance_dir.iterdir():
                if 'fiverr' in f.name.lower():
                    content['gigs'].append(f.stem)

        return content

    def get_upwork_content(self) -> Dict:
        """Scan Upwork profile content."""
        content = {'profiles': [], 'specializations': []}
        freelance_dir = self.products_dir / "FREELANCE_LISTINGS_READY"
        if freelance_dir.exists():
            for f in freelance_dir.iterdir():
                if 'upwork' in f.name.lower():
                    content['profiles'].append(f.stem)

        # Check for boring gigs
        listings_dir = self.products_dir / "listings"
        if listings_dir.exists():
            for f in listings_dir.iterdir():
                if 'upwork' in f.name.lower() or 'boring' in f.name.lower():
                    content['profiles'].append(f.stem)

        return content

    def get_etsy_content(self) -> Dict:
        """Scan Etsy listing content."""
        content = {'listings': [], 'categories': set()}
        etsy_dir = self.products_dir / "ETSY_INSTANT_UPLOAD"
        if etsy_dir.exists():
            for f in etsy_dir.iterdir():
                if f.suffix == '.md':
                    content['listings'].append(f.stem)

        ecom_dir = self.products_dir / "ECOM_LISTINGS_READY"
        if ecom_dir.exists():
            for f in ecom_dir.iterdir():
                if 'etsy' in f.name.lower():
                    content['listings'].append(f.stem)

        return content

    def get_redbubble_content(self) -> Dict:
        """Scan Redbubble listing content."""
        content = {'designs': [], 'categories': set()}
        ecom_dir = self.products_dir / "ECOM_LISTINGS_READY"
        if ecom_dir.exists():
            for f in ecom_dir.iterdir():
                if 'redbubble' in f.name.lower():
                    content['designs'].append(f.stem)

        for f in self.products_dir.iterdir():
            if 'redbubble' in f.name.lower() or 'pod' in f.name.lower():
                content['designs'].append(f.stem)

        return content

    def get_all_product_count(self) -> int:
        """Count total product files across all directories."""
        count = 0
        for d in [self.products_dir]:
            if d.exists():
                for f in d.rglob('*.md'):
                    count += 1
        return count


# =============================================================================
# Platform definitions
# =============================================================================

PLATFORMS = {
    'gumroad': {
        'name': 'Gumroad',
        'signup_url': 'https://app.gumroad.com/signup',
        'login_url': 'https://app.gumroad.com/login',
        'dashboard_url': 'https://app.gumroad.com/dashboard',
        'category': 'digital_products',
        'required_fields': [
            'Email address',
            'Password',
            'Display name',
            'Profile bio (optional at signup, add after)',
            'Profile picture (optional at signup, add after)',
            'Payout method (PayPal or Stripe, configure after signup)',
        ],
        'setup_steps': [
            '1. Go to signup URL and create account with email',
            '2. Verify email address (check inbox)',
            '3. Set display name to your brand name',
            '4. Go to Settings > Profile: add bio, avatar, social links',
            '5. Go to Settings > Payouts: connect PayPal or Stripe',
            '6. Go to Settings > Integrations: connect analytics if needed',
            '7. Upload first product: Dashboard > New Product',
            '8. Set product pricing (recommended: $0+ for lead magnets, $9-$47 for paid)',
            '9. Customize product page with cover image (1280x720)',
            '10. Publish and share link',
        ],
        'profile_tips': [
            'Bio: 2-3 sentences. What you sell, who its for, social proof if any.',
            'Avatar: clean headshot or branded logo, 400x400px minimum',
            'Use existing listings from PRODUCTS/GUMROAD_INSTANT_UPLOAD/',
            'Start with a $0+ lead magnet to build email list',
        ],
        'verification_checks': [
            'Can log in successfully',
            'Profile bio is filled out',
            'Payout method connected (PayPal or Stripe)',
            'At least one product listed',
            'Product page has cover image',
        ],
    },
    'fiverr': {
        'name': 'Fiverr',
        'signup_url': 'https://www.fiverr.com/join',
        'login_url': 'https://www.fiverr.com/login',
        'dashboard_url': 'https://www.fiverr.com/seller_dashboard',
        'category': 'freelance',
        'required_fields': [
            'Email address (or Google/Apple/Facebook SSO)',
            'Username (permanent, choose carefully)',
            'Password',
            'Display name',
            'Profile description (up to 600 chars)',
            'Profile picture (must be a real photo, not logo)',
            'Languages',
            'Skills (up to 15 tags)',
        ],
        'setup_steps': [
            '1. Sign up at fiverr.com/join with email',
            '2. Complete email verification',
            '3. Choose username carefully (cannot change later)',
            '4. Complete seller onboarding questionnaire',
            '5. Upload profile photo (Fiverr requires real face photo)',
            '6. Write professional description using existing Fiverr gig content',
            '7. Add skills and languages',
            '8. Create first gig: Selling > Gigs > Create a New Gig',
            '9. Set pricing (start at $5-$25 for reviews, raise after)',
            '10. Add gig images (1550x370 for gallery, 690x426 for thumbnail)',
            '11. Set response time expectations',
            '12. Complete Fiverr Learn courses for badge (optional)',
        ],
        'profile_tips': [
            'Username: professional, memorable, no numbers if possible',
            'Description: lead with results, not credentials. "I build X that does Y."',
            'Start prices LOW to get first reviews, then raise',
            'Use gig content from PRODUCTS/FIVERR_INSTANT_UPLOAD/',
            'Response time under 1 hour boosts ranking significantly',
        ],
        'verification_checks': [
            'Can log in successfully',
            'Profile photo uploaded (real face)',
            'Profile description filled (600 chars)',
            'At least one gig published',
            'Gig has cover image and description',
            'Payment method configured for withdrawals',
        ],
    },
    'upwork': {
        'name': 'Upwork',
        'signup_url': 'https://www.upwork.com/nx/signup/?dest=home',
        'login_url': 'https://www.upwork.com/ab/account-security/login',
        'dashboard_url': 'https://www.upwork.com/nx/find-work/',
        'category': 'freelance',
        'required_fields': [
            'First name and last name',
            'Email address',
            'Password',
            'Country of residence',
            'Professional title (headline)',
            'Profile overview (up to 5000 chars)',
            'Hourly rate',
            'Skills (up to 15)',
            'Profile photo',
            'Employment history (at least 1 entry recommended)',
            'Education (optional but recommended)',
            'Portfolio items (2-3 minimum)',
        ],
        'setup_steps': [
            '1. Sign up at upwork.com with real legal name',
            '2. Verify email and phone number',
            '3. Complete profile setup wizard',
            '4. Set professional title (e.g., "Full Stack Developer | AI Automation")',
            '5. Write overview using Upwork profile content from PRODUCTS/',
            '6. Set hourly rate ($25-$75 for starting, adjust based on niche)',
            '7. Add top skills (match to job categories you target)',
            '8. Upload profile photo (professional headshot)',
            '9. Add portfolio items (screenshots, links to past work)',
            '10. Add employment history (freelance counts)',
            '11. Take Upwork skills tests for badges (optional but helps)',
            '12. Set availability and job preferences',
            '13. Submit profile for Upwork review (may take 24-48h)',
            '14. Once approved, start applying to jobs (use Connects wisely)',
        ],
        'profile_tips': [
            'Title: specific > generic. "Python Automation Expert" beats "Developer"',
            'Overview: first 2 lines are most important (shown in search preview)',
            'Start with lower rate to win first 3-5 jobs, then raise',
            'Use content from PRODUCTS/FREELANCE_LISTINGS_READY/',
            'Upwork may reject generic profiles. Be specific about what you do.',
        ],
        'verification_checks': [
            'Can log in successfully',
            'Profile approved by Upwork (status: Active)',
            'Profile photo uploaded',
            'Overview filled out',
            'At least 5 skills added',
            'Hourly rate set',
            'Payment method configured',
            'At least 1 portfolio item',
        ],
    },
    'etsy': {
        'name': 'Etsy',
        'signup_url': 'https://www.etsy.com/join',
        'login_url': 'https://www.etsy.com/signin',
        'dashboard_url': 'https://www.etsy.com/your/shops/me/dashboard',
        'category': 'ecommerce',
        'required_fields': [
            'Email address',
            'First name',
            'Password',
            'Shop name (permanent, choose carefully)',
            'Shop language',
            'Shop country',
            'Shop currency',
            'Payment method for receiving funds (bank account or PayPal)',
            'Billing info (credit card for Etsy fees)',
        ],
        'setup_steps': [
            '1. Create Etsy buyer account at etsy.com/join',
            '2. Go to etsy.com/sell and click "Open your Etsy shop"',
            '3. Set shop preferences (language, country, currency)',
            '4. Choose shop name (4-20 chars, letters and numbers only)',
            '5. Add your first listing to complete shop setup',
            '6. Set up payment: how you get paid (deposit schedule, bank info)',
            '7. Set up billing: how you pay Etsy fees (credit card)',
            '8. Go to Shop Manager > Settings: add shop icon and banner',
            '9. Write shop announcement and About section',
            '10. Set shipping profiles (digital = instant download)',
            '11. Add shop sections for organization',
            '12. Upload listings from PRODUCTS/ETSY_INSTANT_UPLOAD/',
            '13. Set up Etsy Ads (optional, $1/day minimum to start)',
        ],
        'profile_tips': [
            'Shop name: memorable, brandable. Cannot change easily.',
            'For digital products: set "Digital download" as listing type',
            'Etsy charges $0.20 per listing + 6.5% transaction fee',
            'Use listings from PRODUCTS/ETSY_INSTANT_UPLOAD/',
            'Tags are critical for Etsy SEO. Use all 13 tag slots.',
            'First photo is the thumbnail. Make it count.',
        ],
        'verification_checks': [
            'Can log in successfully',
            'Shop is open and visible',
            'Payment method configured (bank account)',
            'Billing method configured (credit card for fees)',
            'At least one listing published',
            'Shop icon and banner uploaded',
            'Shipping profile set up',
        ],
    },
    'redbubble': {
        'name': 'Redbubble',
        'signup_url': 'https://www.redbubble.com/auth/signup',
        'login_url': 'https://www.redbubble.com/auth/login',
        'dashboard_url': 'https://www.redbubble.com/portfolio/manage_works',
        'category': 'pod',
        'required_fields': [
            'Username',
            'Email address',
            'Password',
            'PayPal email (for payouts, add in account settings)',
        ],
        'setup_steps': [
            '1. Sign up at redbubble.com/auth/signup',
            '2. Verify email address',
            '3. Go to Account Settings: add artist profile info',
            '4. Set up payment: add PayPal email for payouts',
            '5. Upload first design: Add New Work',
            '6. Enable all relevant product types for each design',
            '7. Set markup percentages (default 20%, can increase)',
            '8. Write titles and tags for each design (SEO critical)',
            '9. Add to collections for organization',
            '10. Upload POD designs from PRODUCTS/ (Redbubble listings)',
        ],
        'profile_tips': [
            'Redbubble is pure POD. Upload design, they handle printing/shipping.',
            'Minimum payout: $20 via PayPal',
            'Upload at 4500x5400px for best quality across products',
            'Tags are the main discovery mechanism. Use all available slots.',
            'Use designs from PRODUCTS/ECOM_LISTINGS_READY/REDBUBBLE_*',
            'Enable ALL product types for each design to maximize surface area',
        ],
        'verification_checks': [
            'Can log in successfully',
            'Artist profile filled out',
            'PayPal email set for payouts',
            'At least one design uploaded',
            'Products enabled for designs',
        ],
    },
    'stripe': {
        'name': 'Stripe',
        'signup_url': 'https://dashboard.stripe.com/register',
        'login_url': 'https://dashboard.stripe.com/login',
        'dashboard_url': 'https://dashboard.stripe.com/',
        'category': 'payments',
        'required_fields': [
            'Email address',
            'Full legal name',
            'Password',
            'Business type (Individual or Company)',
            'Country',
            'Phone number (for 2FA)',
            'Bank account details (for payouts)',
            'SSN or EIN (for US tax compliance)',
            'Business address',
        ],
        'setup_steps': [
            '1. Sign up at dashboard.stripe.com/register',
            '2. Verify email address',
            '3. Complete business verification:',
            '   - Business type (Individual for solo)',
            '   - Legal name and DOB',
            '   - SSN last 4 (US) or equivalent',
            '   - Business address',
            '4. Add bank account for payouts',
            '5. Enable 2FA (required for live mode)',
            '6. Activate your account (may take 1-2 business days)',
            '7. Get API keys: Developers > API Keys',
            '8. Set up webhook endpoints if needed',
            '9. Consider creating Payment Links for quick checkout pages',
            '10. Connect to other platforms (Gumroad uses Stripe)',
        ],
        'profile_tips': [
            'Stripe is your payment backbone. Connect it to everything.',
            'Test mode is free and unlimited. Use it first.',
            'Payment Links = instant checkout pages without code',
            'Stripe takes 2.9% + $0.30 per transaction',
            'Enable Stripe Radar for fraud protection (free tier available)',
        ],
        'verification_checks': [
            'Can log in successfully',
            'Account activated (not in restricted mode)',
            'Bank account added for payouts',
            'API keys accessible',
            '2FA enabled',
            'Business verification complete',
        ],
    },
    'buffer': {
        'name': 'Buffer',
        'signup_url': 'https://buffer.com/get-started',
        'login_url': 'https://login.buffer.com/login',
        'dashboard_url': 'https://publish.buffer.com/',
        'category': 'social_media',
        'required_fields': [
            'Email address (or Google/Apple SSO)',
            'Password',
            'Social accounts to connect (add after signup)',
        ],
        'setup_steps': [
            '1. Sign up at buffer.com/get-started (free plan available)',
            '2. Connect social accounts:',
            '   - Twitter/X',
            '   - Instagram (business account required)',
            '   - LinkedIn',
            '   - Facebook Page',
            '   - TikTok',
            '   - Pinterest',
            '3. Set posting schedule for each channel',
            '4. Configure time zones',
            '5. Set up content categories/labels',
            '6. Install Buffer browser extension for easy sharing',
            '7. Test: create and schedule a post',
            '8. Free plan: 3 channels, 10 scheduled posts per channel',
            '9. Essentials plan ($6/mo/channel): unlimited scheduling',
        ],
        'profile_tips': [
            'Buffer free plan is good enough to start',
            'Set posting times based on audience analytics',
            'Use "Optimal Timing" feature for best engagement',
            'Connect ALL niche accounts from PRODUCTS/branding/',
            'Browser extension makes sharing research findings easy',
        ],
        'verification_checks': [
            'Can log in successfully',
            'At least 1 social account connected',
            'Posting schedule configured',
            'Test post sent successfully',
        ],
    },
    'beehiiv': {
        'name': 'Beehiiv',
        'signup_url': 'https://www.beehiiv.com/create',
        'login_url': 'https://app.beehiiv.com/login',
        'dashboard_url': 'https://app.beehiiv.com/',
        'category': 'newsletter',
        'required_fields': [
            'Email address',
            'Password',
            'Newsletter name',
            'Newsletter description',
            'Sender name',
            'Custom domain (optional, set up later)',
        ],
        'setup_steps': [
            '1. Sign up at beehiiv.com/create',
            '2. Choose newsletter name and URL slug',
            '3. Write newsletter description (1-2 sentences)',
            '4. Set sender name and reply-to email',
            '5. Customize landing page:',
            '   - Upload logo',
            '   - Set colors',
            '   - Write signup page copy',
            '6. Set up custom domain (optional but recommended)',
            '7. Create welcome email',
            '8. Set up automation: welcome sequence',
            '9. Enable referral program (built-in to Beehiiv)',
            '10. Import existing subscribers if any',
            '11. Send first newsletter issue',
            '12. Free plan: up to 2,500 subscribers',
        ],
        'profile_tips': [
            'Newsletter name: specific to niche. Not your personal name.',
            'Landing page copy: lead with what readers GET, not what you write about',
            'Beehiiv free plan is very generous (2,500 subs, unlimited sends)',
            'Referral program drives organic growth. Enable immediately.',
            'Ad network available at scale for monetization',
            'Connect to existing content from PRODUCTS/ for initial issues',
        ],
        'verification_checks': [
            'Can log in successfully',
            'Newsletter name and description set',
            'Landing page customized (logo, colors, copy)',
            'Welcome email configured',
            'Test email sent to self',
            'Signup form working (test with personal email)',
        ],
    },
}


class AccountTracker:
    """Track account creation status in LEDGER/ACCOUNTS.csv."""

    HEADERS = [
        'platform', 'status', 'email_used', 'username',
        'signup_date', 'verified_date', 'profile_complete',
        'first_listing_date', 'notes', 'last_checked'
    ]

    STATUSES = ['NOT_STARTED', 'SIGNUP_DONE', 'VERIFIED', 'PROFILE_COMPLETE', 'ACTIVE', 'SUSPENDED']

    def __init__(self):
        self.csv_path = safe_path(LEDGER_DIR / "ACCOUNTS.csv")
        self._init_csv()

    def _init_csv(self):
        """Create CSV with headers if it doesn't exist."""
        if not self.csv_path.exists():
            LEDGER_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.HEADERS)

            # Initialize all platforms as NOT_STARTED
            for platform_key in PLATFORMS:
                self._write_entry({
                    'platform': platform_key,
                    'status': 'NOT_STARTED',
                    'email_used': '',
                    'username': '',
                    'signup_date': '',
                    'verified_date': '',
                    'profile_complete': 'FALSE',
                    'first_listing_date': '',
                    'notes': '',
                    'last_checked': datetime.now().isoformat()
                })

    def _write_entry(self, entry: Dict):
        """Append entry to CSV."""
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                entry.get('platform', ''),
                entry.get('status', 'NOT_STARTED'),
                entry.get('email_used', ''),
                entry.get('username', ''),
                entry.get('signup_date', ''),
                entry.get('verified_date', ''),
                entry.get('profile_complete', 'FALSE'),
                entry.get('first_listing_date', ''),
                entry.get('notes', ''),
                entry.get('last_checked', datetime.now().isoformat()),
            ])

    def get_all_entries(self) -> List[Dict]:
        """Read all entries, returning the LATEST entry per platform."""
        if not self.csv_path.exists():
            return []

        entries = {}
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                platform = row.get('platform', '')
                entries[platform] = row  # Last entry wins

        return list(entries.values())

    def get_platform_status(self, platform_key: str) -> Optional[Dict]:
        """Get latest status for a specific platform."""
        entries = self.get_all_entries()
        for e in entries:
            if e.get('platform') == platform_key:
                return e
        return None

    def update_status(self, platform_key: str, new_status: str, notes: str = ""):
        """Append a new status entry for a platform."""
        existing = self.get_platform_status(platform_key)
        entry = {
            'platform': platform_key,
            'status': new_status,
            'email_used': existing.get('email_used', '') if existing else '',
            'username': existing.get('username', '') if existing else '',
            'signup_date': existing.get('signup_date', '') if existing else '',
            'verified_date': datetime.now().isoformat() if new_status == 'VERIFIED' else (existing.get('verified_date', '') if existing else ''),
            'profile_complete': 'TRUE' if new_status in ('PROFILE_COMPLETE', 'ACTIVE') else 'FALSE',
            'first_listing_date': existing.get('first_listing_date', '') if existing else '',
            'notes': notes,
            'last_checked': datetime.now().isoformat(),
        }
        if new_status == 'SIGNUP_DONE' and not entry['signup_date']:
            entry['signup_date'] = datetime.now().isoformat()
        self._write_entry(entry)

    def get_status_summary(self) -> str:
        """Return formatted status summary of all accounts."""
        entries = self.get_all_entries()
        if not entries:
            return "No accounts tracked yet."

        lines = [
            "=== ACCOUNT CREATION STATUS ===",
            "",
            f"{'Platform':<15} {'Status':<20} {'Email':<30} {'Notes':<30}",
            "-" * 95,
        ]

        by_status = defaultdict(int)
        for e in entries:
            platform = e.get('platform', 'unknown')
            status = e.get('status', 'UNKNOWN')
            email = e.get('email_used', '')
            notes = e.get('notes', '')[:30]
            by_status[status] += 1

            # Status indicator
            if status == 'ACTIVE':
                indicator = '[OK]'
            elif status == 'NOT_STARTED':
                indicator = '[--]'
            elif status in ('SIGNUP_DONE', 'VERIFIED'):
                indicator = '[..]'
            elif status == 'PROFILE_COMPLETE':
                indicator = '[~~]'
            else:
                indicator = '[??]'

            name = PLATFORMS.get(platform, {}).get('name', platform)
            lines.append(f"{name:<15} {indicator} {status:<16} {email:<30} {notes}")

        lines.append("")
        lines.append("Summary:")
        for status, count in sorted(by_status.items()):
            lines.append(f"  {status}: {count}")

        total = len(entries)
        active = by_status.get('ACTIVE', 0)
        lines.append(f"\n  Total: {active}/{total} active")

        return "\n".join(lines)


def print_platform_checklist(platform_key: str, payment_info: PaymentInfoReader, scanner: ProductContentScanner):
    """Print full setup checklist for a platform."""
    if platform_key not in PLATFORMS:
        print(f"[ERROR] Unknown platform: {platform_key}")
        print(f"Supported: {', '.join(PLATFORMS.keys())}")
        return

    p = PLATFORMS[platform_key]
    email = payment_info.get_email()
    name = payment_info.get_name()
    creds = payment_info.get_platform_creds(platform_key)

    print(f"\n{'='*60}")
    print(f"  {p['name']} - Account Setup Checklist")
    print(f"{'='*60}\n")

    print(f"Signup URL:    {p['signup_url']}")
    print(f"Login URL:     {p['login_url']}")
    print(f"Dashboard:     {p['dashboard_url']}")
    print(f"Category:      {p['category']}")
    print()

    # Pre-filled info
    if email or name or creds:
        print("--- Pre-filled Info (from SECRETS/PAYMENT_INFO.md) ---")
        if name:
            print(f"  Name:  {name}")
        if email:
            print(f"  Email: {email}")
        for key, val in creds.items():
            print(f"  {key}: {val}")
        print()

    # Required fields
    print("--- Required Fields ---")
    for field in p['required_fields']:
        print(f"  [ ] {field}")
    print()

    # Setup steps
    print("--- Setup Steps ---")
    for step in p['setup_steps']:
        print(f"  {step}")
    print()

    # Existing content
    content = {}
    if platform_key == 'gumroad':
        content = scanner.get_gumroad_content()
    elif platform_key == 'fiverr':
        content = scanner.get_fiverr_content()
    elif platform_key == 'upwork':
        content = scanner.get_upwork_content()
    elif platform_key == 'etsy':
        content = scanner.get_etsy_content()
    elif platform_key == 'redbubble':
        content = scanner.get_redbubble_content()

    if content:
        has_items = any(v for v in content.values() if v)
        if has_items:
            print("--- Existing Content (from PRODUCTS/) ---")
            for key, items in content.items():
                if items:
                    if isinstance(items, set):
                        items = list(items)
                    print(f"  {key}: {len(items)} items")
                    for item in items[:5]:
                        print(f"    - {item}")
                    if len(items) > 5:
                        print(f"    ... and {len(items) - 5} more")
            print()

    # Profile tips
    print("--- Profile Tips ---")
    for tip in p['profile_tips']:
        print(f"  * {tip}")
    print()

    # Verification checks
    print("--- Post-Creation Verification ---")
    for check in p['verification_checks']:
        print(f"  [ ] {check}")
    print()


def run_verification(tracker: AccountTracker):
    """Run verification checks for all platforms with SIGNUP_DONE or higher status."""
    entries = tracker.get_all_entries()
    active_statuses = {'SIGNUP_DONE', 'VERIFIED', 'PROFILE_COMPLETE', 'ACTIVE'}

    print("\n=== ACCOUNT VERIFICATION ===\n")

    has_any = False
    for entry in entries:
        platform_key = entry.get('platform', '')
        status = entry.get('status', '')

        if status not in active_statuses:
            continue

        has_any = True
        p = PLATFORMS.get(platform_key, {})
        name = p.get('name', platform_key)
        checks = p.get('verification_checks', [])

        print(f"\n{name} (current status: {status})")
        print(f"  Dashboard: {p.get('dashboard_url', 'N/A')}")
        print(f"  Verification checks:")
        for check in checks:
            print(f"    [ ] {check}")

    if not has_any:
        print("  No accounts have been created yet. Run --all to see setup checklists.")

    print("\nTo mark a platform as done: --mark-done <platform>")
    print("To open dashboard: --open-tabs --platform <platform>")


def main():
    parser = argparse.ArgumentParser(
        description="Platform Account Creator - Setup checklists and tracking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Supported platforms: {', '.join(PLATFORMS.keys())}

Examples:
  python3 platform_account_creator.py --all
  python3 platform_account_creator.py --platform gumroad
  python3 platform_account_creator.py --open-tabs
  python3 platform_account_creator.py --open-tabs --platform fiverr
  python3 platform_account_creator.py --status
  python3 platform_account_creator.py --verify
  python3 platform_account_creator.py --mark-done gumroad
"""
    )

    parser.add_argument('--platform', help='Specific platform to show/open')
    parser.add_argument('--all', action='store_true', help='Show all platform checklists')
    parser.add_argument('--status', action='store_true', help='Show account creation status')
    parser.add_argument('--open-tabs', action='store_true', help='Open signup URLs in browser')
    parser.add_argument('--verify', action='store_true', help='Run verification checks')
    parser.add_argument('--mark-done', metavar='PLATFORM', help='Mark platform as SIGNUP_DONE')
    parser.add_argument('--mark-active', metavar='PLATFORM', help='Mark platform as ACTIVE')
    parser.add_argument('--mark-verified', metavar='PLATFORM', help='Mark platform as VERIFIED')

    args = parser.parse_args()

    # No args = show help
    if not any([args.platform, args.all, args.status, args.open_tabs,
                args.verify, args.mark_done, args.mark_active, args.mark_verified]):
        parser.print_help()
        return

    payment_info = PaymentInfoReader()
    scanner = ProductContentScanner()
    tracker = AccountTracker()

    # Status mode
    if args.status:
        print(tracker.get_status_summary())
        return

    # Mark done
    if args.mark_done:
        p = args.mark_done.lower()
        if p not in PLATFORMS:
            print(f"[ERROR] Unknown platform: {p}. Supported: {', '.join(PLATFORMS.keys())}")
            sys.exit(1)
        tracker.update_status(p, 'SIGNUP_DONE', f'Marked done {datetime.now().strftime("%Y-%m-%d")}')
        print(f"[OK] {PLATFORMS[p]['name']} marked as SIGNUP_DONE")
        return

    if args.mark_active:
        p = args.mark_active.lower()
        if p not in PLATFORMS:
            print(f"[ERROR] Unknown platform: {p}. Supported: {', '.join(PLATFORMS.keys())}")
            sys.exit(1)
        tracker.update_status(p, 'ACTIVE', f'Marked active {datetime.now().strftime("%Y-%m-%d")}')
        print(f"[OK] {PLATFORMS[p]['name']} marked as ACTIVE")
        return

    if args.mark_verified:
        p = args.mark_verified.lower()
        if p not in PLATFORMS:
            print(f"[ERROR] Unknown platform: {p}. Supported: {', '.join(PLATFORMS.keys())}")
            sys.exit(1)
        tracker.update_status(p, 'VERIFIED', f'Verified {datetime.now().strftime("%Y-%m-%d")}')
        print(f"[OK] {PLATFORMS[p]['name']} marked as VERIFIED")
        return

    # Verify mode
    if args.verify:
        run_verification(tracker)
        return

    # Open tabs mode
    if args.open_tabs:
        if args.platform:
            p = args.platform.lower()
            if p not in PLATFORMS:
                print(f"[ERROR] Unknown platform: {p}. Supported: {', '.join(PLATFORMS.keys())}")
                sys.exit(1)
            url = PLATFORMS[p]['signup_url']
            status = tracker.get_platform_status(p)
            if status and status.get('status') not in ('NOT_STARTED', ''):
                url = PLATFORMS[p]['dashboard_url']
            print(f"[INFO] Opening {PLATFORMS[p]['name']}: {url}")
            open_url(url)
        else:
            print("[INFO] Opening all platform signup URLs...")
            for key, p in PLATFORMS.items():
                status = tracker.get_platform_status(key)
                url = p['signup_url']
                if status and status.get('status') not in ('NOT_STARTED', ''):
                    url = p['dashboard_url']
                print(f"  {p['name']}: {url}")
                open_url(url)
                import time
                time.sleep(0.5)  # Small delay between tabs
        return

    # Single platform checklist
    if args.platform:
        p = args.platform.lower()
        if p not in PLATFORMS:
            print(f"[ERROR] Unknown platform: {p}")
            print(f"Supported: {', '.join(PLATFORMS.keys())}")
            sys.exit(1)
        print_platform_checklist(p, payment_info, scanner)
        return

    # All platforms
    if args.all:
        total_products = scanner.get_all_product_count()
        print(f"\n{'#'*60}")
        print(f"  PLATFORM ACCOUNT CREATOR")
        print(f"  {len(PLATFORMS)} platforms | {total_products} product files ready")
        if payment_info.has_info():
            print(f"  Payment info loaded from SECRETS/PAYMENT_INFO.md")
        else:
            print(f"  [WARN] No payment info found. Fill SECRETS/PAYMENT_INFO.md")
        print(f"{'#'*60}")

        for key in PLATFORMS:
            print_platform_checklist(key, payment_info, scanner)

        print(f"\n{'='*60}")
        print(f"Next steps:")
        print(f"  1. Open all signup tabs: --open-tabs")
        print(f"  2. Create accounts one by one")
        print(f"  3. Mark as done: --mark-done <platform>")
        print(f"  4. Check status: --status")
        print(f"  5. Verify: --verify")
        print(f"{'='*60}\n")
        return


if __name__ == '__main__':
    main()
