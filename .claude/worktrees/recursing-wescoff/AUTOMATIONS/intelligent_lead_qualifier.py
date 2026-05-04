#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Intelligent Lead Qualifier
=====================================
Quant-level lead qualification engine for 2.87M+ bulk leads.

Takes Overture Maps bulk leads → deduplicates by domain → prioritizes by industry budget →
analyzes websites (HTTP + HTML) → scores on aesthetics, SEO, AIO/GIO, modernity, activity →
outputs ranked qualified leads ready for cold email pipeline.

Usage:
    python3 intelligent_lead_qualifier.py --prefilter              # Phase 1: fast pre-filter
    python3 intelligent_lead_qualifier.py --analyze --batch 500    # Phase 2: website analysis
    python3 intelligent_lead_qualifier.py --status                 # Show progress
    python3 intelligent_lead_qualifier.py --top 100                # Show top 100 leads
    python3 intelligent_lead_qualifier.py --export-hot             # Export hot leads for cold email
    python3 intelligent_lead_qualifier.py --full --batch 200       # Run everything end-to-end
"""

import csv
import os
import subprocess
import sys
import json
import time
import re
import hashlib
import argparse
import signal
import traceback
from datetime import datetime
from urllib.parse import urlparse
from collections import defaultdict, Counter
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Try imports
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    subprocess.run(["pip3", "install", "requests", "beautifulsoup4", "--quiet"], check=True)
    import requests
    from bs4 import BeautifulSoup

BASE_DIR = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
BULK_DIR = f"{BASE_DIR}/AUTOMATIONS/leads/bulk"
OUTPUT_DIR = f"{BASE_DIR}/AUTOMATIONS/leads/qualified"
PROGRESS_FILE = f"{OUTPUT_DIR}/progress.json"
PREFILTERED_FILE = f"{OUTPUT_DIR}/PREFILTERED_LEADS.csv"
ANALYZED_FILE = f"{OUTPUT_DIR}/ANALYZED_LEADS.csv"
HOT_LEADS_FILE = f"{OUTPUT_DIR}/HOT_LEADS_QUALIFIED.csv"
WARM_LEADS_FILE = f"{OUTPUT_DIR}/WARM_LEADS_QUALIFIED.csv"

# Graceful shutdown
shutdown_requested = False
def signal_handler(sig, frame):
    global shutdown_requested
    print("\nShutdown requested, saving progress...")
    shutdown_requested = True
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================
# INDUSTRY INTELLIGENCE
# ============================================================

# Industry budget tiers: higher = more likely to pay for web redesign
# Based on actual market data from lead_scoring_criteria.md
INDUSTRY_BUDGET_TIERS = {
    # TIER 1: High discretionary budget, care about aesthetics (15 pts)
    "dentist": {"budget_score": 15, "avg_website_spend": 5000, "aesthetics_priority": "HIGH",
                "demo_url": "https://dental-demo.surge.sh", "typical_revenue": "800K-2M"},
    "orthodontist": {"budget_score": 15, "avg_website_spend": 5000, "aesthetics_priority": "HIGH",
                     "demo_url": "https://dental-demo.surge.sh", "typical_revenue": "800K-2M"},
    "cosmetic_dentist": {"budget_score": 15, "avg_website_spend": 8000, "aesthetics_priority": "HIGHEST",
                         "demo_url": "https://dental-demo.surge.sh", "typical_revenue": "1M-3M"},
    "lawyer": {"budget_score": 14, "avg_website_spend": 6000, "aesthetics_priority": "HIGH",
               "demo_url": "https://legal-demo.surge.sh", "typical_revenue": "500K-5M"},
    "attorney": {"budget_score": 14, "avg_website_spend": 6000, "aesthetics_priority": "HIGH",
                 "demo_url": "https://legal-demo.surge.sh", "typical_revenue": "500K-5M"},
    "realtor": {"budget_score": 13, "avg_website_spend": 4000, "aesthetics_priority": "HIGHEST",
                "demo_url": "https://realtor-demo.surge.sh", "typical_revenue": "200K-1M"},
    "real_estate": {"budget_score": 13, "avg_website_spend": 4000, "aesthetics_priority": "HIGHEST",
                    "demo_url": "https://realtor-demo.surge.sh", "typical_revenue": "200K-1M"},
    "chiropractor": {"budget_score": 13, "avg_website_spend": 3500, "aesthetics_priority": "HIGH",
                     "demo_url": "https://fitness-demo.surge.sh", "typical_revenue": "300K-800K"},
    "doctor": {"budget_score": 12, "avg_website_spend": 4000, "aesthetics_priority": "MEDIUM",
               "demo_url": "https://dental-demo.surge.sh", "typical_revenue": "500K-3M"},
    "physician": {"budget_score": 12, "avg_website_spend": 4000, "aesthetics_priority": "MEDIUM",
                  "demo_url": "https://dental-demo.surge.sh", "typical_revenue": "500K-3M"},
    "veterinarian": {"budget_score": 12, "avg_website_spend": 3000, "aesthetics_priority": "MEDIUM",
                     "demo_url": "https://dental-demo.surge.sh", "typical_revenue": "400K-1.5M"},

    # TIER 2: Moderate budget, some aesthetic interest (10 pts)
    "salon": {"budget_score": 10, "avg_website_spend": 2500, "aesthetics_priority": "HIGH",
              "demo_url": "https://fitness-demo.surge.sh", "typical_revenue": "200K-600K"},
    "spa": {"budget_score": 11, "avg_website_spend": 3000, "aesthetics_priority": "HIGHEST",
            "demo_url": "https://fitness-demo.surge.sh", "typical_revenue": "300K-1M"},
    "gym": {"budget_score": 10, "avg_website_spend": 2500, "aesthetics_priority": "MEDIUM",
            "demo_url": "https://fitness-demo.surge.sh", "typical_revenue": "300K-1.5M"},
    "fitness": {"budget_score": 10, "avg_website_spend": 2500, "aesthetics_priority": "MEDIUM",
                "demo_url": "https://fitness-demo.surge.sh", "typical_revenue": "200K-800K"},
    "accountant": {"budget_score": 10, "avg_website_spend": 2500, "aesthetics_priority": "LOW",
                   "demo_url": "https://legal-demo.surge.sh", "typical_revenue": "300K-1M"},

    # TIER 3: Lower budget but high volume (7 pts)
    "restaurant": {"budget_score": 7, "avg_website_spend": 1500, "aesthetics_priority": "MEDIUM",
                   "demo_url": "https://restaurant-site-demo.surge.sh", "typical_revenue": "300K-2M"},
    "plumber": {"budget_score": 8, "avg_website_spend": 2000, "aesthetics_priority": "LOW",
                "demo_url": "https://plumber-demo.surge.sh", "typical_revenue": "200K-800K"},
    "plumbing": {"budget_score": 8, "avg_website_spend": 2000, "aesthetics_priority": "LOW",
                 "demo_url": "https://plumber-demo.surge.sh", "typical_revenue": "200K-800K"},
    "auto_repair": {"budget_score": 7, "avg_website_spend": 1500, "aesthetics_priority": "LOW",
                    "demo_url": "https://plumber-demo.surge.sh", "typical_revenue": "300K-1M"},
    "automotive_repair": {"budget_score": 7, "avg_website_spend": 1500, "aesthetics_priority": "LOW",
                          "demo_url": "https://plumber-demo.surge.sh", "typical_revenue": "300K-1M"},
}

# Default for unknown categories
DEFAULT_INDUSTRY = {"budget_score": 5, "avg_website_spend": 1500, "aesthetics_priority": "LOW",
                    "demo_url": "https://printmaxx-local-demos.surge.sh", "typical_revenue": "unknown"}

# ============================================================
# PHASE 1: PRE-FILTER (no network, pure data processing)
# ============================================================

def get_industry_info(category):
    """Get industry intelligence for a category."""
    cat_lower = category.lower().strip() if category else ""
    # Try exact match first
    if cat_lower in INDUSTRY_BUDGET_TIERS:
        return INDUSTRY_BUDGET_TIERS[cat_lower]
    # Try partial match
    for key, info in INDUSTRY_BUDGET_TIERS.items():
        if key in cat_lower or cat_lower in key:
            return info
    return DEFAULT_INDUSTRY


def normalize_domain(website):
    """Extract and normalize domain from website URL."""
    if not website:
        return None
    website = website.strip()
    if not website.startswith(('http://', 'https://')):
        website = 'http://' + website
    try:
        parsed = urlparse(website)
        domain = parsed.netloc.lower()
        # Remove www.
        if domain.startswith('www.'):
            domain = domain[4:]
        # Remove trailing dots
        domain = domain.rstrip('.')
        if not domain or '.' not in domain:
            return None
        # Filter out obviously bad domains
        skip_domains = {'facebook.com', 'google.com', 'yelp.com', 'yellowpages.com',
                       'mapquest.com', 'linkedin.com', 'instagram.com', 'twitter.com',
                       'x.com', 'tiktok.com', 'youtube.com', 'bbb.org', 'angieslist.com',
                       'thumbtack.com', 'homeadvisor.com', 'angi.com', 'nextdoor.com',
                       'doordash.com', 'ubereats.com', 'grubhub.com', 'opentable.com',
                       'zocdoc.com', 'healthgrades.com', 'vitals.com', 'webmd.com',
                       'npi.com', 'apple.com', 'apps.apple.com', 'play.google.com',
                       'wix.com', 'squarespace.com', 'godaddy.com', 'wordpress.com',
                       'blogspot.com', 'tumblr.com', 'weebly.com', 'jimdo.com',
                       'example.com', 'test.com', 'localhost',
                       # Third-party review/directory/SaaS platforms
                       'tupalo.com', 'solutionreach.com', 'birdeye.com', 'podium.com',
                       'demandforce.com', 'patientpop.com', 'doctible.com', 'weave.com',
                       'yext.com', 'manta.com', 'superpages.com', 'dexknows.com',
                       'merchantcircle.com', 'citysearch.com', 'judysbook.com',
                       'chamberofcommerce.com', 'hotfrog.com', 'brownbook.net',
                       'cylex-usa.com', 'n49.com', 'localpages.com',
                       'zillow.com', 'realtor.com', 'redfin.com', 'trulia.com',
                       'coldwellbanker.com', 'kw.com', 'century21.com', 'remax.com',
                       'avvo.com', 'findlaw.com', 'justia.com', 'martindale.com',
                       'lawyers.com', 'nolo.com', 'yelp.com',
                       'ratemds.com', 'wellness.com', 'sharecare.com',
                       'bing.com', 'mapquest.com', 'foursquare.com',
                       'tripadvisor.com', 'toasttab.com', 'menufy.com',
                       'beyondmenu.com', 'allmenus.com', 'menupages.com'}
        if domain in skip_domains:
            return None
        # Filter domains that are just platform pages (e.g., yelp.com/biz/...)
        if any(platform in domain for platform in ['yelp.', 'facebook.', 'google.', 'yellowpages.']):
            return None
        return domain
    except Exception:
        return None


def prefilter_leads():
    """Phase 1: Pre-filter all bulk leads. Fast, no network."""
    print("=" * 60)
    print("PHASE 1: PRE-FILTERING LEADS")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read all bulk lead files (skip MASTER to avoid dupes)
    lead_files = sorted(Path(BULK_DIR).glob("US_LEADS_*.csv"))
    lead_files = [f for f in lead_files if 'MASTER' not in f.name]

    print(f"Found {len(lead_files)} lead files")

    # Track unique domains to deduplicate
    domain_map = {}  # domain -> best lead for that domain
    total_read = 0
    with_website = 0
    unique_domains = 0
    skipped_bad_domain = 0
    category_counts = Counter()

    for lead_file in lead_files:
        file_count = 0
        print(f"\n  Processing {lead_file.name}...")
        try:
            with open(lead_file, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_read += 1
                    file_count += 1

                    website = row.get('website', '').strip()
                    if not website:
                        continue
                    with_website += 1

                    domain = normalize_domain(website)
                    if not domain:
                        skipped_bad_domain += 1
                        continue

                    category = row.get('category', 'unknown')
                    industry_info = get_industry_info(category)

                    # Pre-score based on available data (no network)
                    pre_score = 0

                    # Industry budget score (0-15)
                    pre_score += industry_info['budget_score']

                    # Has phone (5 pts) - indicates active business
                    phone = row.get('phone', '').strip()
                    if phone and len(phone) >= 7:
                        pre_score += 5

                    # Has email (3 pts) - extra contact method
                    email = row.get('email', '').strip()
                    if email and '@' in email:
                        pre_score += 3

                    # Has full address (3 pts) - real business
                    address = row.get('address', '').strip()
                    city = row.get('city', '').strip()
                    state = row.get('state', '').strip()
                    if address and city and state:
                        pre_score += 3

                    # Confidence score from Overture (0-4 pts)
                    try:
                        conf = float(row.get('confidence_score', 0))
                        pre_score += min(int(conf * 4), 4)
                    except (ValueError, TypeError):
                        pass

                    # Aesthetics priority bonus (0-5 pts) - industries that CARE about how they look
                    aes = industry_info.get('aesthetics_priority', 'LOW')
                    if aes == 'HIGHEST':
                        pre_score += 5
                    elif aes == 'HIGH':
                        pre_score += 3
                    elif aes == 'MEDIUM':
                        pre_score += 1

                    # Build lead record
                    lead = {
                        'id': row.get('id', ''),
                        'name': row.get('name', ''),
                        'category': category,
                        'phone': phone,
                        'email': email,
                        'website': website,
                        'domain': domain,
                        'address': address,
                        'city': city,
                        'state': state,
                        'zip': row.get('zip', ''),
                        'country': row.get('country', 'US'),
                        'lon': row.get('lon', ''),
                        'lat': row.get('lat', ''),
                        'confidence_score': row.get('confidence_score', ''),
                        'pre_score': pre_score,
                        'budget_tier': industry_info['budget_score'],
                        'aesthetics_priority': industry_info.get('aesthetics_priority', 'LOW'),
                        'demo_url': industry_info.get('demo_url', ''),
                        'typical_revenue': industry_info.get('typical_revenue', 'unknown'),
                    }

                    # Deduplicate by domain: keep the lead with the highest pre_score
                    if domain not in domain_map or pre_score > domain_map[domain]['pre_score']:
                        if domain not in domain_map:
                            unique_domains += 1
                        domain_map[domain] = lead

                    category_counts[category] += 1

        except Exception as e:
            print(f"    ERROR reading {lead_file.name}: {e}")
            continue
        print(f"    Read {file_count:,} rows")

    # Sort by pre_score descending
    sorted_leads = sorted(domain_map.values(), key=lambda x: x['pre_score'], reverse=True)

    # Write pre-filtered CSV
    if sorted_leads:
        fieldnames = list(sorted_leads[0].keys())
        with open(PREFILTERED_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for lead in sorted_leads:
                writer.writerow(lead)

    # Save progress
    progress = load_progress()
    progress['prefilter'] = {
        'timestamp': datetime.now().isoformat(),
        'total_read': total_read,
        'with_website': with_website,
        'unique_domains': unique_domains,
        'skipped_bad_domain': skipped_bad_domain,
        'output_file': PREFILTERED_FILE,
        'category_counts': dict(category_counts.most_common(30)),
    }
    save_progress(progress)

    print(f"\n{'=' * 60}")
    print(f"PRE-FILTER COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total rows read:     {total_read:,}")
    print(f"With website:        {with_website:,} ({with_website/max(total_read,1)*100:.1f}%)")
    print(f"Bad/platform domains: {skipped_bad_domain:,}")
    print(f"Unique domains:      {unique_domains:,}")
    print(f"Output:              {PREFILTERED_FILE}")
    print(f"\nTop categories:")
    for cat, count in category_counts.most_common(15):
        industry = get_industry_info(cat)
        print(f"  {cat:25s}: {count:>8,}  (budget={industry['budget_score']}, aesthetics={industry.get('aesthetics_priority', 'LOW')})")

    # Show score distribution
    score_buckets = Counter()
    for lead in sorted_leads:
        bucket = (lead['pre_score'] // 5) * 5
        score_buckets[bucket] += 1
    print(f"\nPre-score distribution:")
    for bucket in sorted(score_buckets.keys(), reverse=True):
        bar = '#' * min(score_buckets[bucket] // 100, 60)
        print(f"  {bucket:>3}-{bucket+4}: {score_buckets[bucket]:>8,} {bar}")

    return len(sorted_leads)


# ============================================================
# PHASE 2: WEBSITE ANALYSIS (HTTP-level, batched)
# ============================================================

# Design age indicators
OLD_TECH_PATTERNS = {
    # Very old (pre-2015)
    'table_layout': (re.compile(r'<table[^>]*(?:width|cellpadding|cellspacing|border)', re.I), -15),
    'inline_styles_heavy': (re.compile(r'style="[^"]{50,}"', re.I), -5),
    'flash_content': (re.compile(r'(?:swfobject|\.swf|flash|shockwave)', re.I), -20),
    'marquee': (re.compile(r'<marquee', re.I), -20),
    'font_tags': (re.compile(r'<font\s', re.I), -15),
    'frames': (re.compile(r'<(?:frame|frameset|iframe\s+[^>]*frameborder)', re.I), -10),

    # Old (2015-2018)
    'jquery_old': (re.compile(r'jquery[.-](?:1\.[0-9]|2\.[0-2])', re.I), -8),
    'bootstrap_2': (re.compile(r'bootstrap[./](?:2\.)', re.I), -10),
    'bootstrap_3': (re.compile(r'bootstrap[./](?:3\.)', re.I), -5),
    'fontawesome_4': (re.compile(r'font-awesome[./](?:4\.)', re.I), -5),
    'angular_1': (re.compile(r'angular(?:\.min)?\.js', re.I), -8),

    # Outdated CMS indicators
    'old_wordpress': (re.compile(r'wp-(?:content|includes).*ver=(?:[1-4]\.[0-9])', re.I), -8),
    'joomla': (re.compile(r'/media/jui/|/components/com_', re.I), -5),
    'drupal_old': (re.compile(r'(?:drupal\.js|/sites/default/files)', re.I), -3),
}

MODERN_TECH_PATTERNS = {
    # Modern CSS
    'css_grid': (re.compile(r'display:\s*grid|grid-template', re.I), 5),
    'css_flexbox': (re.compile(r'display:\s*flex|flex-direction|justify-content', re.I), 3),
    'css_variables': (re.compile(r'--[a-zA-Z][\w-]*\s*:', re.I), 5),
    'css_animations': (re.compile(r'@keyframes|animation-name|transition:', re.I), 3),
    'tailwind': (re.compile(r'(?:tailwindcss|tailwind\.css|class="[^"]*(?:flex|grid|bg-|text-|px-|py-))', re.I), 8),

    # Modern frameworks
    'react': (re.compile(r'(?:__NEXT_DATA__|_next/static|react(?:\.production|DOM))', re.I), 8),
    'nextjs': (re.compile(r'__NEXT_DATA__|_next/static', re.I), 10),
    'vue': (re.compile(r'(?:vue\.(?:min\.)?js|__vue__|v-(?:if|for|bind))', re.I), 7),
    'svelte': (re.compile(r'svelte', re.I), 8),

    # Modern image handling
    'webp': (re.compile(r'\.webp', re.I), 3),
    'avif': (re.compile(r'\.avif', re.I), 5),
    'lazy_loading': (re.compile(r'loading="lazy"|data-lazy|lazyload', re.I), 3),
    'srcset': (re.compile(r'srcset="', re.I), 4),

    # Modern fonts
    'google_fonts': (re.compile(r'fonts\.googleapis\.com|fonts\.gstatic\.com', re.I), 2),
    'variable_fonts': (re.compile(r'font-variation-settings|wght\s', re.I), 4),

    # Performance
    'preload': (re.compile(r'rel="preload"|rel="preconnect"', re.I), 3),
    'service_worker': (re.compile(r'serviceWorker|service-worker', re.I), 5),
    'critical_css': (re.compile(r'<style[^>]*>.*?</style>', re.I | re.DOTALL), 1),
}

# SEO signals
SEO_SIGNALS = {
    'has_title': lambda soup: bool(soup.find('title') and soup.find('title').string and len(soup.find('title').string.strip()) > 5),
    'has_meta_desc': lambda soup: bool(soup.find('meta', attrs={'name': 'description'})),
    'has_h1': lambda soup: bool(soup.find('h1')),
    'has_h2': lambda soup: bool(soup.find('h2')),
    'has_schema': lambda soup: bool(soup.find('script', attrs={'type': 'application/ld+json'})),
    'has_og_tags': lambda soup: bool(soup.find('meta', attrs={'property': re.compile(r'^og:')})),
    'has_canonical': lambda soup: bool(soup.find('link', attrs={'rel': 'canonical'})),
    'has_sitemap_ref': lambda html: 'sitemap' in html.lower(),
    'has_robots_meta': lambda soup: bool(soup.find('meta', attrs={'name': 'robots'})),
    'has_alt_tags': lambda soup: len([img for img in soup.find_all('img') if img.get('alt')]) > 0,
}

# AIO/GIO readiness signals
AIO_SIGNALS = {
    'has_faq': lambda html: bool(re.search(r'(?:FAQ|frequently asked|common questions)', html, re.I)),
    'has_qa_schema': lambda html: bool(re.search(r'"@type"\s*:\s*"(?:FAQ|Question|Answer)Page"', html)),
    'has_howto_schema': lambda html: bool(re.search(r'"@type"\s*:\s*"HowTo"', html)),
    'has_local_business_schema': lambda html: bool(re.search(r'"@type"\s*:\s*"(?:Local|Medical|Dental|Legal|Health)Business"', html, re.I)),
    'has_about_page': lambda html: bool(re.search(r'href="[^"]*(?:about|team|our-story|who-we-are)', html, re.I)),
    'has_service_pages': lambda html: bool(re.search(r'href="[^"]*(?:services|what-we-do|our-services)', html, re.I)),
    'content_depth': lambda soup: len(soup.get_text(strip=True)) > 2000,  # Not thin content
}


def analyze_website(lead):
    """Analyze a single website. Returns enriched lead dict."""
    website = lead.get('website', '')
    domain = lead.get('domain', '')

    if not website:
        return None

    # Ensure URL has protocol
    url = website.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    result = dict(lead)  # Copy all existing fields
    result['analysis_timestamp'] = datetime.now().isoformat()
    result['analysis_status'] = 'pending'

    # Initialize scores
    result['design_score'] = 0       # 0-25 (higher = MORE outdated = BETTER prospect)
    result['seo_score'] = 0          # 0-20 (higher = WORSE seo = BETTER prospect)
    result['aio_score'] = 0          # 0-15 (higher = WORSE aio = BETTER prospect)
    result['activity_score'] = 0     # 0-15 (higher = MORE active = BETTER prospect)
    result['contact_score'] = 0      # 0-10
    result['total_score'] = 0        # 0-100 composite
    result['pain_signals'] = ''      # Human-readable issues found
    result['tech_stack'] = ''
    result['cms_detected'] = ''
    result['ssl_valid'] = ''
    result['response_time_ms'] = ''
    result['page_size_kb'] = ''
    result['mobile_friendly'] = ''
    result['copyright_year'] = ''
    result['is_active'] = ''

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
        }

        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True,
                              verify=False, stream=False)
        elapsed_ms = int((time.time() - start_time) * 1000)

        result['response_time_ms'] = elapsed_ms
        result['page_size_kb'] = round(len(response.content) / 1024, 1)
        result['ssl_valid'] = 'YES' if response.url.startswith('https://') else 'NO'
        result['analysis_status'] = 'analyzed'

        # Check if site is actually up and has content
        if response.status_code >= 400:
            result['is_active'] = 'DOWN'
            result['analysis_status'] = 'down'
            result['pain_signals'] = 'SITE_DOWN'
            result['total_score'] = 0  # Can't sell to a dead site
            return result

        html = response.text
        if len(html) < 200:
            result['is_active'] = 'EMPTY'
            result['analysis_status'] = 'empty'
            result['pain_signals'] = 'EMPTY_SITE'
            result['total_score'] = 0
            return result

        result['is_active'] = 'YES'
        soup = BeautifulSoup(html, 'html.parser')

        pain_signals = []
        tech_stack = []

        # ----- DESIGN ANALYSIS (0-25 pts, higher = more outdated = better prospect) -----
        design_score = 0

        # Check for old tech (each adds points = bad site = good prospect)
        for name, (pattern, weight) in OLD_TECH_PATTERNS.items():
            if pattern.search(html):
                design_score += abs(weight)
                pain_signals.append(f"OLD:{name}")
                tech_stack.append(name)

        # Check for modern tech (each subtracts = good site = worse prospect)
        modern_count = 0
        for name, (pattern, weight) in MODERN_TECH_PATTERNS.items():
            if pattern.search(html):
                design_score -= weight  # Subtract because modern = less need for redesign
                modern_count += 1
                tech_stack.append(f"modern:{name}")

        # Mobile responsive check
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport_meta:
            design_score += 10
            pain_signals.append("NO_MOBILE_VIEWPORT")
            result['mobile_friendly'] = 'NO'
        else:
            result['mobile_friendly'] = 'YES'

        # Check page load speed (slow = bad site)
        if elapsed_ms > 5000:
            design_score += 8
            pain_signals.append("VERY_SLOW_LOAD")
        elif elapsed_ms > 3000:
            design_score += 4
            pain_signals.append("SLOW_LOAD")

        # Page size check (huge = unoptimized)
        page_kb = result['page_size_kb']
        if page_kb > 5000:
            design_score += 5
            pain_signals.append("HUGE_PAGE_SIZE")

        # No HTTPS
        if result['ssl_valid'] == 'NO':
            design_score += 8
            pain_signals.append("NO_SSL")

        # CMS detection
        cms = 'unknown'
        if re.search(r'wp-content|wp-includes|wordpress', html, re.I):
            cms = 'wordpress'
        elif re.search(r'squarespace', html, re.I):
            cms = 'squarespace'
        elif re.search(r'wix\.com|wixsite', html, re.I):
            cms = 'wix'
        elif re.search(r'weebly', html, re.I):
            cms = 'weebly'
        elif re.search(r'godaddy-ws|godaddy\.com', html, re.I):
            cms = 'godaddy'
        elif re.search(r'shopify', html, re.I):
            cms = 'shopify'
        elif re.search(r'__NEXT_DATA__', html):
            cms = 'nextjs'
        result['cms_detected'] = cms

        # Old CMS template = higher redesign potential
        if cms in ('wix', 'weebly', 'godaddy'):
            design_score += 5
            pain_signals.append(f"BUDGET_CMS:{cms}")

        # Cap design score
        design_score = max(0, min(25, design_score))
        result['design_score'] = design_score

        # ----- SEO ANALYSIS (0-20 pts, higher = worse SEO = better prospect) -----
        seo_score = 20  # Start at max, subtract for good SEO
        seo_issues = 0

        for signal_name, check_fn in SEO_SIGNALS.items():
            try:
                if signal_name == 'has_sitemap_ref':
                    has_signal = check_fn(html)
                else:
                    has_signal = check_fn(soup)
                if has_signal:
                    seo_score -= 2  # Good SEO signal reduces prospect value
                else:
                    seo_issues += 1
                    pain_signals.append(f"SEO_MISSING:{signal_name}")
            except Exception:
                pass

        seo_score = max(0, min(20, seo_score))
        result['seo_score'] = seo_score

        # ----- AIO/GIO READINESS (0-15 pts, higher = worse = better prospect) -----
        aio_score = 15  # Start at max
        for signal_name, check_fn in AIO_SIGNALS.items():
            try:
                if 'soup' in check_fn.__code__.co_varnames:
                    has_signal = check_fn(soup)
                else:
                    has_signal = check_fn(html)
                if has_signal:
                    aio_score -= 2
                else:
                    pain_signals.append(f"AIO_MISSING:{signal_name}")
            except Exception:
                pass

        aio_score = max(0, min(15, aio_score))
        result['aio_score'] = aio_score

        # ----- ACTIVITY DETECTION (0-15 pts) -----
        activity_score = 0

        # Copyright year check
        copyright_match = re.search(r'(?:copyright|©|\(c\))\s*(?:20)?(\d{2})', html, re.I)
        if copyright_match:
            year = int(copyright_match.group(1))
            if year < 100:
                year += 2000
            result['copyright_year'] = str(year)
            current_year = datetime.now().year
            if year >= current_year:
                activity_score += 10  # Current year = active
            elif year >= current_year - 1:
                activity_score += 7
            elif year >= current_year - 2:
                activity_score += 4
                pain_signals.append(f"OLD_COPYRIGHT:{year}")
            else:
                activity_score += 1
                pain_signals.append(f"VERY_OLD_COPYRIGHT:{year}")
        else:
            activity_score += 5  # No copyright isn't necessarily inactive

        # Phone number on page (indicates active business)
        phone_on_page = bool(re.search(r'(?:\(\d{3}\)\s*\d{3}[-.\s]\d{4}|\d{3}[-.\s]\d{3}[-.\s]\d{4})', html))
        if phone_on_page:
            activity_score += 3

        # Social links (indicates active presence)
        social_count = len(re.findall(r'(?:facebook|twitter|instagram|linkedin|tiktok|youtube)\.com', html, re.I))
        if social_count >= 2:
            activity_score += 2

        activity_score = min(15, activity_score)
        result['activity_score'] = activity_score

        # ----- CONTACT COMPLETENESS (0-10 pts) -----
        contact_score = 0
        if phone_on_page:
            contact_score += 3
        if re.search(r'(?:contact|get.in.touch|reach.us|email.us)', html, re.I):
            contact_score += 2
        if re.search(r'(?:form|<input[^>]*type="(?:email|tel|text)")', html, re.I):
            contact_score += 3
        if re.search(r'(?:google\.com/maps|maps\.google|goo\.gl/maps)', html, re.I):
            contact_score += 2
        contact_score = min(10, contact_score)
        result['contact_score'] = contact_score

        # ----- COMPOSITE SCORE -----
        # Formula: pre_score (0-35) + design_pain (0-25) + seo_pain (0-20) + aio_pain (0-15) +
        #          activity_bonus (0-15 if active, 0 if dead) - modern_penalty
        # Higher = better prospect

        # Only count as prospect if business appears active
        if activity_score >= 4:
            total = (
                result['pre_score'] +        # 0-35 industry + data quality
                design_score +                # 0-25 design pain
                seo_score +                   # 0-20 seo pain
                aio_score +                   # 0-15 aio pain
                min(activity_score, 10)       # 0-10 activity bonus (capped)
            )
            # Normalize to 0-100
            total = min(100, int(total * 100 / 105))
        else:
            total = max(5, int(result['pre_score'] * 0.3))  # Low activity = low score

        result['total_score'] = total
        result['pain_signals'] = '|'.join(pain_signals[:15])  # Cap at 15 signals
        result['tech_stack'] = '|'.join(tech_stack[:10])

    except requests.exceptions.Timeout:
        result['analysis_status'] = 'timeout'
        result['is_active'] = 'TIMEOUT'
        result['pain_signals'] = 'TIMEOUT'
        result['total_score'] = int(result['pre_score'] * 0.5)  # Timeout = might be bad site
    except requests.exceptions.ConnectionError:
        result['analysis_status'] = 'connection_error'
        result['is_active'] = 'DOWN'
        result['pain_signals'] = 'CONNECTION_ERROR'
        result['total_score'] = 0
    except Exception as e:
        result['analysis_status'] = f'error:{str(e)[:50]}'
        result['is_active'] = 'ERROR'
        result['total_score'] = int(result['pre_score'] * 0.3)

    return result


def analyze_batch(batch_size=500, workers=10, resume=True, industry_filter=''):
    """Phase 2: Analyze websites in batches with parallel workers."""
    filter_msg = f", industry={industry_filter}" if industry_filter else ""
    print("=" * 60)
    print(f"PHASE 2: WEBSITE ANALYSIS (batch={batch_size}, workers={workers}{filter_msg})")
    print("=" * 60)

    if not os.path.exists(PREFILTERED_FILE):
        print("ERROR: Run --prefilter first!")
        return 0

    # Load already analyzed domains
    analyzed_domains = set()
    existing_results = []
    if resume and os.path.exists(ANALYZED_FILE):
        try:
            with open(ANALYZED_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    analyzed_domains.add(row.get('domain', ''))
                    existing_results.append(row)
            print(f"  Resuming: {len(analyzed_domains):,} domains already analyzed")
        except Exception:
            pass

    # Load pre-filtered leads
    industry_terms = [t.strip().lower() for t in industry_filter.split(',') if t.strip()] if industry_filter else []
    leads_to_analyze = []
    with open(PREFILTERED_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('domain') not in analyzed_domains:
                # Apply industry filter if specified
                if industry_terms:
                    cat = row.get('category', '').lower()
                    if not any(term in cat for term in industry_terms):
                        continue
                row['pre_score'] = int(row.get('pre_score', 0))
                leads_to_analyze.append(row)

    print(f"  {len(leads_to_analyze):,} leads remaining to analyze")

    # Take top batch_size by pre_score
    leads_to_analyze.sort(key=lambda x: x['pre_score'], reverse=True)
    batch = leads_to_analyze[:batch_size]

    if not batch:
        print("  No more leads to analyze!")
        return 0

    print(f"  Analyzing top {len(batch)} leads (pre_score range: {batch[0]['pre_score']}-{batch[-1]['pre_score']})")

    # Parallel analysis
    results = list(existing_results)
    analyzed_count = 0
    errors = 0
    start_time = time.time()

    # Suppress SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(analyze_website, lead): lead for lead in batch}

        for future in as_completed(futures):
            if shutdown_requested:
                print("\n  Shutdown requested, saving progress...")
                executor.shutdown(wait=False, cancel_futures=True)
                break

            analyzed_count += 1
            try:
                result = future.result(timeout=15)
                if result:
                    results.append(result)

                    # Progress output every 50
                    if analyzed_count % 50 == 0:
                        elapsed = time.time() - start_time
                        rate = analyzed_count / max(elapsed, 1)
                        eta = (len(batch) - analyzed_count) / max(rate, 0.1)
                        status = result.get('analysis_status', 'unknown')
                        score = result.get('total_score', 0)
                        print(f"  [{analyzed_count}/{len(batch)}] {rate:.1f}/s ETA:{eta:.0f}s | "
                              f"Last: {result.get('domain', '?')[:30]} score={score} status={status}")
            except Exception as e:
                errors += 1

    # Sort results by total_score descending
    for r in results:
        try:
            r['total_score'] = int(r.get('total_score', 0))
        except (ValueError, TypeError):
            r['total_score'] = 0
    results.sort(key=lambda x: x['total_score'], reverse=True)

    # Write analyzed leads
    if results:
        fieldnames = list(results[0].keys())
        with open(ANALYZED_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow(r)

    # Update progress
    progress = load_progress()
    progress['analysis'] = {
        'timestamp': datetime.now().isoformat(),
        'total_analyzed': len(results),
        'batch_analyzed': analyzed_count,
        'errors': errors,
        'output_file': ANALYZED_FILE,
    }
    save_progress(progress)

    elapsed = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"ANALYSIS BATCH COMPLETE")
    print(f"{'=' * 60}")
    print(f"Analyzed this batch:  {analyzed_count:,}")
    print(f"Errors:              {errors:,}")
    print(f"Total analyzed:      {len(results):,}")
    print(f"Time:                {elapsed:.0f}s ({analyzed_count/max(elapsed,1):.1f} sites/sec)")
    print(f"Output:              {ANALYZED_FILE}")

    # Export hot and warm leads
    export_qualified_leads(results)

    return analyzed_count


def export_qualified_leads(results=None):
    """Export hot and warm leads to separate files."""
    if results is None:
        if not os.path.exists(ANALYZED_FILE):
            print("No analyzed leads found. Run --analyze first.")
            return
        results = []
        with open(ANALYZED_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['total_score'] = int(row.get('total_score', 0))
                except (ValueError, TypeError):
                    row['total_score'] = 0
                results.append(row)

    hot_leads = [r for r in results if r.get('total_score', 0) >= 65 and r.get('is_active') == 'YES']
    warm_leads = [r for r in results if 45 <= r.get('total_score', 0) < 65 and r.get('is_active') == 'YES']

    for leads, filepath, label in [
        (hot_leads, HOT_LEADS_FILE, "HOT"),
        (warm_leads, WARM_LEADS_FILE, "WARM"),
    ]:
        if leads:
            # Sort by score descending
            leads.sort(key=lambda x: x.get('total_score', 0), reverse=True)
            fieldnames = list(leads[0].keys())
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for lead in leads:
                    writer.writerow(lead)
            print(f"  {label} leads: {len(leads):,} -> {filepath}")

    # Stats
    active = sum(1 for r in results if r.get('is_active') == 'YES')
    down = sum(1 for r in results if r.get('is_active') in ('DOWN', 'TIMEOUT', 'ERROR'))

    print(f"\n  Qualification Summary:")
    print(f"    Total analyzed:  {len(results):,}")
    print(f"    Active sites:    {active:,}")
    print(f"    Down/Error:      {down:,}")
    print(f"    HOT (>=65):      {len(hot_leads):,}")
    print(f"    WARM (45-64):    {len(warm_leads):,}")
    print(f"    COLD (<45):      {len(results) - len(hot_leads) - len(warm_leads):,}")


# ============================================================
# STATUS & DISPLAY
# ============================================================

def load_progress():
    """Load progress file."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_progress(data):
    """Save progress file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def show_status():
    """Show qualification pipeline status."""
    print("=" * 60)
    print("LEAD QUALIFICATION STATUS")
    print("=" * 60)

    progress = load_progress()

    # Pre-filter status
    pf = progress.get('prefilter', {})
    if pf:
        print(f"\nPhase 1 - Pre-Filter: COMPLETE ({pf.get('timestamp', '?')})")
        print(f"  Total read:      {pf.get('total_read', 0):,}")
        print(f"  With website:    {pf.get('with_website', 0):,}")
        print(f"  Unique domains:  {pf.get('unique_domains', 0):,}")
        if os.path.exists(PREFILTERED_FILE):
            count = sum(1 for _ in open(PREFILTERED_FILE)) - 1
            print(f"  Pre-filtered:    {count:,}")
    else:
        print(f"\nPhase 1 - Pre-Filter: NOT RUN")
        print(f"  Run: python3 {__file__} --prefilter")

    # Analysis status
    an = progress.get('analysis', {})
    if an:
        print(f"\nPhase 2 - Website Analysis: IN PROGRESS ({an.get('timestamp', '?')})")
        print(f"  Total analyzed:  {an.get('total_analyzed', 0):,}")
        print(f"  Last batch:      {an.get('batch_analyzed', 0):,}")
        print(f"  Errors:          {an.get('errors', 0):,}")

    # File sizes
    print(f"\nOutput Files:")
    for name, path in [
        ("Pre-filtered", PREFILTERED_FILE),
        ("Analyzed", ANALYZED_FILE),
        ("Hot Leads", HOT_LEADS_FILE),
        ("Warm Leads", WARM_LEADS_FILE),
    ]:
        if os.path.exists(path):
            count = sum(1 for _ in open(path)) - 1
            size = os.path.getsize(path) / 1024
            print(f"  {name:15s}: {count:>8,} leads ({size:.0f} KB)")
        else:
            print(f"  {name:15s}: not created yet")


def show_top(n=50):
    """Show top N qualified leads."""
    if not os.path.exists(ANALYZED_FILE):
        print("No analyzed leads. Run --analyze first.")
        return

    print(f"\n{'=' * 100}")
    print(f"TOP {n} QUALIFIED LEADS")
    print(f"{'=' * 100}")
    print(f"{'#':>3} {'Score':>5} {'Category':15s} {'Domain':30s} {'City':15s} {'St':2s} {'Pain Signals':40s}")
    print(f"{'-'*3} {'-'*5} {'-'*15} {'-'*30} {'-'*15} {'-'*2} {'-'*40}")

    with open(ANALYZED_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= n:
                break
            score = row.get('total_score', '?')
            cat = row.get('category', '?')[:15]
            domain = row.get('domain', '?')[:30]
            city = row.get('city', '?')[:15]
            state = row.get('state', '?')[:2]
            pain = row.get('pain_signals', '')[:40]
            print(f"{i+1:>3} {score:>5} {cat:15s} {domain:30s} {city:15s} {state:2s} {pain:40s}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='PRINTMAXX Intelligent Lead Qualifier')
    parser.add_argument('--prefilter', action='store_true', help='Phase 1: Pre-filter leads (fast, no network)')
    parser.add_argument('--analyze', action='store_true', help='Phase 2: Analyze websites (HTTP)')
    parser.add_argument('--batch', type=int, default=500, help='Batch size for analysis (default: 500)')
    parser.add_argument('--workers', type=int, default=10, help='Parallel workers (default: 10)')
    parser.add_argument('--status', action='store_true', help='Show pipeline status')
    parser.add_argument('--top', type=int, default=0, help='Show top N leads')
    parser.add_argument('--export-hot', action='store_true', help='Export hot leads')
    parser.add_argument('--full', action='store_true', help='Run full pipeline')
    parser.add_argument('--no-resume', action='store_true', help='Start analysis fresh')
    parser.add_argument('--industry', type=str, default='', help='Filter to specific industry (e.g., lawyer,realtor)')

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.top:
        show_top(args.top)
        return

    if args.export_hot:
        export_qualified_leads()
        return

    if args.full:
        prefilter_leads()
        if not shutdown_requested:
            analyze_batch(batch_size=args.batch, workers=args.workers, resume=not args.no_resume,
                         industry_filter=args.industry)
        return

    if args.prefilter:
        prefilter_leads()
        return

    if args.analyze:
        analyze_batch(batch_size=args.batch, workers=args.workers, resume=not args.no_resume,
                     industry_filter=args.industry)
        return

    # Default: show status
    show_status()


if __name__ == '__main__':
    main()
