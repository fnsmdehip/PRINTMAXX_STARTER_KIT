#!/usr/bin/env python3
"""
PRINTMAXX Website Signal Scorer
Scores local business websites on redesign opportunity (0-100).
Higher score = worse website = better prospect for cold email.

Usage:
  python3 AUTOMATIONS/website_signal_scorer.py --leads AUTOMATIONS/leads/dental_austin_tx_leads.csv
  python3 AUTOMATIONS/website_signal_scorer.py --urls "https://example.com,https://other.com"
  python3 AUTOMATIONS/website_signal_scorer.py --leads AUTOMATIONS/leads/*.csv --min-score 40
  python3 AUTOMATIONS/website_signal_scorer.py --leads AUTOMATIONS/leads/dental_*.csv --output output/dental_scores.csv
"""

import argparse
import csv
import glob
import json
import os
import re
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE / "output"
DEFAULT_OUTPUT = OUTPUT_DIR / "website_scores.csv"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

DEMO_URLS = {
    "dental":      "dental-demo.surge.sh",
    "dentist":     "dental-demo.surge.sh",
    "lawyer":      "legal-demo.surge.sh",
    "legal":       "legal-demo.surge.sh",
    "attorney":    "legal-demo.surge.sh",
    "plumber":     "plumber-demo.surge.sh",
    "plumbing":    "plumber-demo.surge.sh",
    "restaurant":  "restaurant-demo.surge.sh",
    "realtor":     "realtor-demo.surge.sh",
    "real_estate": "realtor-demo.surge.sh",
    "realestate":  "realtor-demo.surge.sh",
    "fitness":     "fitness-demo.surge.sh",
    "gym":         "fitness-demo.surge.sh",
}

# CMS fingerprints: (pattern_in_html, cms_name)
CMS_PATTERNS = [
    (r'wp-content|wp-includes|wordpress', 'WordPress'),
    (r'wix\.com|wixsite\.com|X-Wix', 'Wix'),
    (r'squarespace\.com|sqsp\.net|squarespace-cdn', 'Squarespace'),
    (r'weebly\.com|weeblycloud', 'Weebly'),
    (r'shopify\.com|cdn\.shopify', 'Shopify'),
    (r'godaddysites\.com|godaddy\.com/websites', 'GoDaddy'),
    (r'webflow\.io|webflow\.com', 'Webflow'),
    (r'duda\.co|dudaone\.com', 'Duda'),
    (r'jimdo\.com', 'Jimdo'),
    (r'site123\.com', 'Site123'),
]

# Modern CSS framework fingerprints
FRAMEWORK_PATTERNS = [
    (r'tailwindcss|tailwind\.', 'Tailwind'),
    (r'bootstrap', 'Bootstrap'),
    (r'bulma', 'Bulma'),
    (r'foundation\.zurb', 'Foundation'),
    (r'materialize', 'Materialize'),
    (r'chakra-ui', 'Chakra UI'),
]

# Social platform patterns
SOCIAL_PATTERNS = [
    (r'facebook\.com|fb\.com', 'Facebook'),
    (r'instagram\.com', 'Instagram'),
    (r'twitter\.com|x\.com', 'X/Twitter'),
    (r'linkedin\.com', 'LinkedIn'),
    (r'youtube\.com', 'YouTube'),
    (r'tiktok\.com', 'TikTok'),
    (r'yelp\.com', 'Yelp'),
    (r'pinterest\.com', 'Pinterest'),
]

_shutdown = False


def _sig_handler(sig, frame):
    global _shutdown
    _shutdown = True
    print("\n[!] Shutting down gracefully...")


signal.signal(signal.SIGINT, _sig_handler)


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------

def fetch_page(url, timeout=15):
    """Fetch a URL. Returns (response, html, load_time_s, error_str)."""
    # Ensure URL has scheme
    if not url.startswith("http"):
        url = "https://" + url

    session = requests.Session()
    session.headers.update({
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })

    start = time.time()
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        load_time = round(time.time() - start, 2)
        return resp, resp.text, load_time, None
    except requests.exceptions.SSLError:
        # Try without SSL
        try:
            http_url = url.replace("https://", "http://")
            resp = session.get(http_url, timeout=timeout, allow_redirects=True)
            load_time = round(time.time() - start, 2)
            return resp, resp.text, load_time, "ssl_error_fell_back_to_http"
        except Exception as e:
            return None, "", round(time.time() - start, 2), f"ssl_and_http_fail: {str(e)[:80]}"
    except requests.exceptions.Timeout:
        return None, "", timeout, "timeout"
    except requests.exceptions.ConnectionError as e:
        return None, "", round(time.time() - start, 2), f"connection_error: {str(e)[:80]}"
    except Exception as e:
        return None, "", round(time.time() - start, 2), f"error: {str(e)[:80]}"


# ---------------------------------------------------------------------------
# Signal Detection
# ---------------------------------------------------------------------------

def check_ssl(url):
    """Check if URL uses HTTPS."""
    return url.startswith("https://")


def check_mobile_responsive(soup, html):
    """Check for viewport meta tag and responsive indicators."""
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport:
        content = viewport.get("content", "")
        if "width=device-width" in content:
            return True, "viewport_ok"
    # Fallback: check for responsive CSS frameworks
    html_lower = html.lower()
    for pattern, name in FRAMEWORK_PATTERNS:
        if re.search(pattern, html_lower):
            return True, f"framework:{name}"
    # Check for media queries in inline styles
    if "@media" in html and ("max-width" in html or "min-width" in html):
        return True, "media_queries"
    return False, "no_viewport"


def detect_cms(html):
    """Detect CMS from HTML content."""
    html_lower = html.lower()
    for pattern, name in CMS_PATTERNS:
        if re.search(pattern, html_lower):
            return name
    return "custom/unknown"


def detect_frameworks(html):
    """Detect modern CSS frameworks."""
    html_lower = html.lower()
    found = []
    for pattern, name in FRAMEWORK_PATTERNS:
        if re.search(pattern, html_lower):
            found.append(name)
    return found


def check_contact_form(soup, html):
    """Check for contact/lead forms."""
    forms = soup.find_all("form")
    if not forms:
        return False, 0
    contact_forms = 0
    for form in forms:
        form_text = form.get_text().lower()
        form_html = str(form).lower()
        # Look for contact-related inputs
        if any(kw in form_html for kw in ["contact", "email", "phone", "message", "name", "submit", "send"]):
            contact_forms += 1
        elif form.find("textarea"):
            contact_forms += 1
        elif form.find("input", {"type": "email"}):
            contact_forms += 1
    return contact_forms > 0, contact_forms


def check_social_links(soup, html):
    """Find social media links."""
    found = []
    all_links = soup.find_all("a", href=True)
    for a in all_links:
        href = a.get("href", "").lower()
        for pattern, name in SOCIAL_PATTERNS:
            if re.search(pattern, href) and name not in found:
                found.append(name)
    return found


def check_maps_embed(soup):
    """Check for Google Maps iframe embed."""
    iframes = soup.find_all("iframe")
    for iframe in iframes:
        src = iframe.get("src", "").lower()
        if "google.com/maps" in src or "maps.google" in src:
            return True
    return False


def check_reviews(soup, html):
    """Check for reviews/testimonials section."""
    html_lower = html.lower()
    review_keywords = ["review", "testimonial", "what our", "patient says",
                       "client says", "5 stars", "star rating", "google review"]
    count = sum(1 for kw in review_keywords if kw in html_lower)
    return count >= 2, count


def extract_copyright_year(html):
    """Extract copyright year from page."""
    patterns = [
        r'(?:©|\(c\)|&copy;|copyright)\s*(\d{4})',
        r'(\d{4})\s*(?:©|\(c\)|&copy;|copyright)',
        r'©\s*\d{4}\s*[-–]\s*(\d{4})',  # "© 2020-2024" -> take latest
    ]
    years = []
    for pat in patterns:
        matches = re.findall(pat, html, re.IGNORECASE)
        for m in matches:
            y = int(m)
            if 2000 <= y <= 2030:
                years.append(y)
    return max(years) if years else None


def check_images(soup):
    """Analyze image optimization."""
    imgs = soup.find_all("img")
    total = len(imgs)
    lazy_count = 0
    for img in imgs:
        loading = img.get("loading", "")
        if loading == "lazy" or img.get("data-src") or img.get("data-lazy"):
            lazy_count += 1
    has_webp = bool(soup.find("source", {"type": "image/webp"}) or
                    soup.find("img", src=re.compile(r'\.webp')))
    return total, lazy_count, has_webp


def check_schema(soup):
    """Check for structured data / schema markup."""
    ld_json = soup.find_all("script", {"type": "application/ld+json"})
    return len(ld_json) > 0, len(ld_json)


def check_analytics(html):
    """Check for analytics/tracking scripts."""
    patterns = [
        (r'google-analytics\.com|gtag|ga\.js|analytics\.js|G-[A-Z0-9]+|UA-\d+', 'Google Analytics'),
        (r'googletagmanager\.com|GTM-[A-Z0-9]+', 'Google Tag Manager'),
        (r'facebook\.net/.*fbevents|fbq\(', 'Facebook Pixel'),
        (r'hotjar\.com|hj\(', 'Hotjar'),
        (r'clarity\.ms', 'Microsoft Clarity'),
    ]
    found = []
    for pat, name in patterns:
        if re.search(pat, html, re.IGNORECASE):
            found.append(name)
    return found


def extract_emails(html):
    """Extract email addresses from page."""
    raw = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', html)
    # Deduplicate, lowercase
    seen = set()
    emails = []
    skip_domains = {"example.com", "domain.com", "email.com", "sentry.io",
                    "wixpress.com", "googleapis.com", "w3.org", "schema.org",
                    "gravatar.com", "wordpress.org"}
    for e in raw:
        e_lower = e.lower()
        domain = e_lower.split("@")[1] if "@" in e_lower else ""
        if e_lower not in seen and domain not in skip_domains:
            seen.add(e_lower)
            emails.append(e_lower)
    return emails


def extract_phones(html, text):
    """Extract phone numbers from page text."""
    patterns = [
        r'\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}',
        r'\d{3}[\s.\-]\d{3}[\s.\-]\d{4}',
        r'\+1[\s.\-]?\d{3}[\s.\-]?\d{3}[\s.\-]?\d{4}',
    ]
    phones = set()
    for pat in patterns:
        for m in re.findall(pat, text):
            cleaned = re.sub(r'[^\d]', '', m)
            if len(cleaned) >= 10:
                phones.add(cleaned[-10:])  # Normalize to 10 digits
    return list(phones)


def measure_page_size(html):
    """Measure page size in KB."""
    return round(len(html.encode('utf-8')) / 1024, 1)


def check_meta_desc(soup):
    """Check for meta description."""
    desc = soup.find("meta", attrs={"name": "description"})
    if desc:
        content = desc.get("content", "").strip()
        return len(content) > 20, content[:100]
    return False, ""


def check_title(soup):
    """Check for proper title tag."""
    title = soup.find("title")
    if title:
        text = title.get_text().strip()
        return len(text) > 5, text[:80]
    return False, ""


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_website(signals):
    """
    Score 0-100 on redesign opportunity.
    Higher = worse website = better prospect.
    """
    score = 0
    reasons = []

    # No SSL = +20
    if not signals["has_ssl"]:
        score += 20
        reasons.append("+20 no_ssl")

    # Not mobile responsive = +25
    if not signals["is_mobile"]:
        score += 25
        reasons.append("+25 not_mobile")

    # Load time scoring
    lt = signals["load_time_s"]
    if lt > 8:
        score += 15
        reasons.append(f"+15 very_slow:{lt}s")
    elif lt > 5:
        score += 12
        reasons.append(f"+12 slow:{lt}s")
    elif lt > 3:
        score += 5
        reasons.append(f"+5 moderate:{lt}s")

    # Copyright year
    cy = signals["copyright_year"]
    current_year = datetime.now().year
    if cy and cy < current_year - 3:
        score += 10
        reasons.append(f"+10 old_copyright:{cy}")
    elif cy and cy < current_year - 1:
        score += 5
        reasons.append(f"+5 stale_copyright:{cy}")

    # No contact form = +10
    if not signals["has_contact_form"]:
        score += 10
        reasons.append("+10 no_form")

    # CMS-based scoring
    cms = signals["cms"]
    if cms == "WordPress":
        score += 8
        reasons.append("+8 wordpress")
    elif cms in ("Wix", "Squarespace", "Weebly", "GoDaddy", "Jimdo", "Site123"):
        score += 5
        reasons.append(f"+5 builder:{cms}")

    # No social links = +5
    if len(signals["social_links"]) == 0:
        score += 5
        reasons.append("+5 no_social")

    # No Google Maps embed = +3
    if not signals["has_maps"]:
        score += 3
        reasons.append("+3 no_maps")

    # No reviews/testimonials = +5
    if not signals["has_reviews"]:
        score += 5
        reasons.append("+5 no_reviews")

    # No schema markup = +3
    if not signals["has_schema"]:
        score += 3
        reasons.append("+3 no_schema")

    # No analytics = +5
    if len(signals["analytics"]) == 0:
        score += 5
        reasons.append("+5 no_analytics")

    # No lazy loading on images = +3
    if signals["total_images"] > 5 and signals["lazy_images"] == 0:
        score += 3
        reasons.append("+3 no_lazy_load")

    # Large page size = +3
    if signals["page_size_kb"] > 3000:
        score += 3
        reasons.append(f"+3 heavy_page:{signals['page_size_kb']}kb")

    # No meta description = +3
    if not signals["has_meta_desc"]:
        score += 3
        reasons.append("+3 no_meta_desc")

    # No proper title = +3
    if not signals["has_title"]:
        score += 3
        reasons.append("+3 no_title")

    # No modern CSS framework = +2
    if len(signals["css_frameworks"]) == 0 and cms == "custom/unknown":
        score += 2
        reasons.append("+2 no_modern_css")

    # Cap at 100
    score = min(score, 100)

    return score, reasons


def classify_tier(score):
    """Classify into HOT/WARM/COOL/COLD."""
    if score >= 60:
        return "HOT"
    elif score >= 40:
        return "WARM"
    elif score >= 25:
        return "COOL"
    return "COLD"


def assign_demo(category):
    """Assign matching demo URL based on industry category."""
    if not category:
        return ""
    cat_lower = category.lower().strip()
    for key, url in DEMO_URLS.items():
        if key in cat_lower:
            return url
    return ""


# ---------------------------------------------------------------------------
# Analyze single URL
# ---------------------------------------------------------------------------

def analyze_url(url, category="", business_name="", email="", city=""):
    """Full analysis of a single URL. Returns dict of all signals + score."""
    print(f"  Scoring: {url[:70]}...", end=" ", flush=True)

    resp, html, load_time, error = fetch_page(url)

    result = {
        "business_name": business_name,
        "url": url,
        "category": category,
        "city": city,
        "email": email,
        "fetch_error": error or "",
        "http_status": resp.status_code if resp else 0,
        "load_time_s": load_time,
        "page_size_kb": 0,
        "has_ssl": False,
        "is_mobile": False,
        "mobile_detail": "",
        "cms": "",
        "css_frameworks": [],
        "has_contact_form": False,
        "form_count": 0,
        "social_links": [],
        "has_maps": False,
        "has_reviews": False,
        "review_signal_count": 0,
        "copyright_year": None,
        "has_schema": False,
        "schema_count": 0,
        "analytics": [],
        "total_images": 0,
        "lazy_images": 0,
        "has_webp": False,
        "has_meta_desc": False,
        "meta_desc": "",
        "has_title": False,
        "title": "",
        "emails_found": [],
        "phones_found": [],
        "redesign_score": 0,
        "score_reasons": [],
        "tier": "COLD",
        "demo_url": assign_demo(category),
        "scored_at": datetime.now().isoformat(),
    }

    if not resp or not html:
        # Unreachable site = very high score (easy sell: "your site is down")
        result["redesign_score"] = 85
        result["score_reasons"] = ["+85 unreachable"]
        result["tier"] = "HOT"
        print(f"UNREACHABLE -> 85 HOT")
        return result

    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator=" ", strip=True)

    # Run all checks
    result["has_ssl"] = check_ssl(resp.url)
    result["page_size_kb"] = measure_page_size(html)

    is_mobile, mobile_detail = check_mobile_responsive(soup, html)
    result["is_mobile"] = is_mobile
    result["mobile_detail"] = mobile_detail

    result["cms"] = detect_cms(html)
    result["css_frameworks"] = detect_frameworks(html)

    has_form, form_count = check_contact_form(soup, html)
    result["has_contact_form"] = has_form
    result["form_count"] = form_count

    result["social_links"] = check_social_links(soup, html)
    result["has_maps"] = check_maps_embed(soup)

    has_reviews, review_count = check_reviews(soup, html)
    result["has_reviews"] = has_reviews
    result["review_signal_count"] = review_count

    result["copyright_year"] = extract_copyright_year(html)

    has_schema, schema_count = check_schema(soup)
    result["has_schema"] = has_schema
    result["schema_count"] = schema_count

    result["analytics"] = check_analytics(html)

    total_imgs, lazy_imgs, has_webp = check_images(soup)
    result["total_images"] = total_imgs
    result["lazy_images"] = lazy_imgs
    result["has_webp"] = has_webp

    has_desc, desc_text = check_meta_desc(soup)
    result["has_meta_desc"] = has_desc
    result["meta_desc"] = desc_text

    has_title, title_text = check_title(soup)
    result["has_title"] = has_title
    result["title"] = title_text

    result["emails_found"] = extract_emails(html)
    result["phones_found"] = extract_phones(html, page_text)

    # Merge email from lead CSV if we didn't find any
    if email and not result["emails_found"]:
        result["emails_found"] = [e.strip() for e in email.split(";") if "@" in e]

    # Score it
    score, reasons = score_website(result)
    result["redesign_score"] = score
    result["score_reasons"] = reasons
    result["tier"] = classify_tier(score)

    print(f"{score} {result['tier']}")
    return result


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "business_name", "url", "category", "city", "redesign_score", "tier",
    "demo_url", "email", "emails_found", "phones_found",
    "has_ssl", "is_mobile", "load_time_s", "page_size_kb",
    "cms", "css_frameworks", "has_contact_form", "social_links",
    "has_maps", "has_reviews", "copyright_year", "has_schema",
    "analytics", "total_images", "lazy_images", "has_webp",
    "has_meta_desc", "has_title", "title",
    "score_reasons", "fetch_error", "scored_at",
]


def load_leads_from_csv(csv_paths):
    """Load URLs from lead CSV files. Returns list of dicts."""
    leads = []
    seen_urls = set()

    for path_pattern in csv_paths:
        for fpath in sorted(glob.glob(path_pattern)):
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        url = (row.get("website") or "").strip()
                        if not url or url in seen_urls:
                            continue
                        seen_urls.add(url)
                        leads.append({
                            "url": url,
                            "business_name": (row.get("business_name") or "").strip(),
                            "category": (row.get("category") or "").strip(),
                            "city": (row.get("city") or "").strip(),
                            "email": (row.get("email_if_found") or row.get("email") or "").strip(),
                        })
            except Exception as e:
                print(f"  [warn] Could not read {fpath}: {e}")
    return leads


def write_csv(results, output_path):
    """Write results to CSV."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            row = dict(r)
            # Serialize lists to semicolon-separated strings
            for key in ["emails_found", "phones_found", "social_links",
                        "css_frameworks", "analytics", "score_reasons"]:
                if isinstance(row.get(key), list):
                    row[key] = "; ".join(str(x) for x in row[key])
            writer.writerow(row)
    print(f"\n  CSV saved: {output_path}")


def print_summary(results, top_n=20):
    """Print top prospects summary."""
    sorted_results = sorted(results, key=lambda x: x["redesign_score"], reverse=True)

    print("\n" + "=" * 72)
    print(f"  WEBSITE SIGNAL SCORER RESULTS")
    print(f"  {len(results)} sites analyzed | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 72)

    # Tier breakdown
    tiers = {"HOT": 0, "WARM": 0, "COOL": 0, "COLD": 0}
    for r in results:
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
    print(f"\n  HOT (60+): {tiers['HOT']}  |  WARM (40-59): {tiers['WARM']}  |  COOL (25-39): {tiers['COOL']}  |  COLD (<25): {tiers['COLD']}")

    # Score distribution
    scores = [r["redesign_score"] for r in results]
    if scores:
        avg = sum(scores) / len(scores)
        print(f"  avg score: {avg:.0f}  |  max: {max(scores)}  |  min: {min(scores)}")

    # Top prospects
    print(f"\n  TOP {min(top_n, len(sorted_results))} PROSPECTS (highest redesign opportunity):")
    print(f"  {'#':<3} {'Score':<6} {'Tier':<5} {'Business':<35} {'Key Issues'}")
    print(f"  {'-'*3} {'-'*5} {'-'*4} {'-'*35} {'-'*40}")

    for i, r in enumerate(sorted_results[:top_n]):
        name = (r["business_name"] or urlparse(r["url"]).netloc)[:34]
        # Top 3 score reasons
        top_reasons = "; ".join(r["score_reasons"][:3]) if r["score_reasons"] else "unreachable"
        print(f"  {i+1:<3} {r['redesign_score']:<6} {r['tier']:<5} {name:<35} {top_reasons}")

    # Emails found summary
    with_email = [r for r in sorted_results if r.get("emails_found")]
    hot_with_email = [r for r in sorted_results if r["tier"] == "HOT" and r.get("emails_found")]
    print(f"\n  sites with email: {len(with_email)}/{len(results)}")
    print(f"  HOT leads with email: {len(hot_with_email)} (ready for cold outreach)")

    if hot_with_email:
        print(f"\n  COLD EMAIL TARGETS (HOT + has email):")
        for r in hot_with_email[:10]:
            name = (r["business_name"] or urlparse(r["url"]).netloc)[:30]
            emails = "; ".join(r["emails_found"][:2])
            demo = r.get("demo_url", "")
            print(f"    {r['redesign_score']} | {name} | {emails} | demo: {demo}")

    print("\n" + "=" * 72)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Score local business websites on redesign opportunity (0-100)")
    parser.add_argument("--leads", nargs="+",
                        help="CSV file paths (supports globs)")
    parser.add_argument("--urls", type=str,
                        help="Comma-separated URLs to score")
    parser.add_argument("--output", "-o", type=str,
                        default=str(DEFAULT_OUTPUT),
                        help=f"Output CSV path (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--min-score", type=int, default=0,
                        help="Only output leads with score >= this value")
    parser.add_argument("--delay", type=float, default=1.5,
                        help="Seconds between requests (default: 1.5)")
    parser.add_argument("--top", type=int, default=20,
                        help="Number of top prospects to show (default: 20)")
    parser.add_argument("--category", type=str, default="",
                        help="Category for manual URLs (e.g., dental)")
    parser.add_argument("--city", type=str, default="",
                        help="City for manual URLs")

    args = parser.parse_args()

    if not args.leads and not args.urls:
        parser.print_help()
        print("\nError: provide --leads or --urls")
        sys.exit(1)

    # Collect URLs to score
    leads = []
    if args.leads:
        leads = load_leads_from_csv(args.leads)
        print(f"\n  Loaded {len(leads)} unique URLs from {len(args.leads)} path(s)")
    if args.urls:
        for url in args.urls.split(","):
            url = url.strip()
            if url:
                leads.append({
                    "url": url,
                    "business_name": "",
                    "category": args.category,
                    "city": args.city,
                    "email": "",
                })
        print(f"  Added {len(args.urls.split(','))} manual URLs")

    if not leads:
        print("  No URLs to score.")
        sys.exit(0)

    # Score each URL
    results = []
    print(f"\n  Scoring {len(leads)} websites (delay: {args.delay}s)...\n")

    for i, lead in enumerate(leads):
        if _shutdown:
            print("\n  [!] Interrupted. Saving partial results...")
            break

        result = analyze_url(
            url=lead["url"],
            category=lead.get("category", ""),
            business_name=lead.get("business_name", ""),
            email=lead.get("email", ""),
            city=lead.get("city", ""),
        )
        results.append(result)

        # Rate limit
        if i < len(leads) - 1 and not _shutdown:
            time.sleep(args.delay)

    # Filter by min score
    if args.min_score > 0:
        before = len(results)
        results = [r for r in results if r["redesign_score"] >= args.min_score]
        print(f"\n  Filtered: {before} -> {len(results)} (min score: {args.min_score})")

    # Output
    if results:
        write_csv(results, args.output)
        print_summary(results, top_n=args.top)
    else:
        print("  No results to write.")


if __name__ == "__main__":
    main()
