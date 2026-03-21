#!/usr/bin/env python3

from __future__ import annotations
"""
savvy_lead_scraper.py - Quant-level local business lead scoring

Discovers local businesses via DuckDuckGo HTML search (html.duckduckgo.com).
Visits their websites and scores them on a 0-100 website quality scale.
LOW scores = HOT leads (bad website = needs redesign).

Uses ONLY free, no-API-key methods: requests + beautifulsoup4.
No Selenium, no Playwright, no browser automation. Runs in background.

Usage:
    python3 savvy_lead_scraper.py --category "dental" --city "Austin TX" --limit 50
    python3 savvy_lead_scraper.py --category "plumbing" --city "Denver CO" --limit 30 --resume
    python3 savvy_lead_scraper.py --help

Output:
    CSV with columns: business_name, address, phone, website, google_rating,
    review_count, website_score, signals_detected, email_if_found

Dependencies:
    pip install requests beautifulsoup4
"""

import argparse
import csv
import hashlib
import json
import os
import random
import re
import signal
import socket
import ssl
import sys
import time
import urllib.parse
import urllib.robotparser
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)

try:
    from duckduckgo_search import DDGS
    _HAS_DDGS = True
except ImportError:
    _HAS_DDGS = False

try:
    from googlesearch import search as google_search
    _HAS_GOOGLE = True
except ImportError:
    _HAS_GOOGLE = False


# ============================================================================
# CONSTANTS
# ============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
LEADS_DIR = SCRIPT_DIR / "leads"
CHECKPOINT_DIR = LEADS_DIR / ".checkpoints"

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

CSV_HEADERS = [
    "business_name", "address", "phone", "website", "google_rating",
    "review_count", "website_score", "signals_detected", "email_if_found",
    "category", "city", "scraped_at",
]

# Graceful shutdown
_shutdown = False
def _handle_signal(sig, frame):
    global _shutdown
    _shutdown = True
    print("\n[!] Shutdown requested. Saving progress...")
signal.signal(signal.SIGINT, _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)


# ============================================================================
# HTTP HELPERS
# ============================================================================

_PROXY = None  # Set via --proxy flag


def get_session():
    """Create a requests session with realistic headers and optional proxy."""
    s = requests.Session()
    s.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    })
    if _PROXY:
        s.proxies = {"http": _PROXY, "https": _PROXY}
    return s


def rate_limit(lo=1.0, hi=2.5):
    time.sleep(random.uniform(lo, hi))


def safe_get(session, url, timeout=15):
    """Returns (response, error_string)."""
    try:
        r = session.get(url, timeout=timeout, allow_redirects=True)
        return r, None
    except requests.exceptions.SSLError:
        return None, "SSL_ERROR"
    except requests.exceptions.ConnectionError:
        return None, "CONN_ERROR"
    except requests.exceptions.Timeout:
        return None, "TIMEOUT"
    except requests.exceptions.TooManyRedirects:
        return None, "REDIRECTS"
    except Exception as e:
        return None, str(e)[:80]


# ============================================================================
# CHECKPOINT / RESUME
# ============================================================================

def _ckpt_path(category, city):
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    key = hashlib.md5(f"{category}_{city}".lower().encode()).hexdigest()[:12]
    return CHECKPOINT_DIR / f"ckpt_{key}.json"


def load_checkpoint(category, city):
    p = _ckpt_path(category, city)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    return {"done": [], "results": []}


def save_checkpoint(category, city, data):
    p = _ckpt_path(category, city)
    p.write_text(json.dumps(data, default=str, indent=2))


# ============================================================================
# EXTRACT HELPERS
# ============================================================================

def extract_emails(text):
    if not text:
        return []
    raw = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)
    junk = ["example.com", "sentry", "wixpress", "googleapis", "schema.org",
            "w3.org", "cloudflare", ".png", ".jpg", ".gif", ".webp", ".svg",
            "webpack", "wordpress.org", "gravatar"]
    return list({e for e in raw if not any(j in e.lower() for j in junk)})


def extract_phones(text):
    if not text:
        return []
    raw = re.findall(r'\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}', text)
    seen, out = set(), []
    for p in raw:
        d = re.sub(r'\D', '', p)
        if len(d) == 10 and d not in seen:
            seen.add(d)
            out.append(f"({d[:3]}) {d[3:6]}-{d[6:]}")
        elif len(d) == 11 and d[0] == '1' and d[1:] not in seen:
            seen.add(d[1:])
            out.append(f"({d[1:4]}) {d[4:7]}-{d[7:]}")
    return out


# ============================================================================
# BUSINESS DISCOVERY (DuckDuckGo HTML -- no API keys, no JS needed)
# ============================================================================

# Aggregator / directory domains to skip (we want actual business websites)
_SKIP_DOMAINS = [
    "google.com", "yelp.com", "yellowpages.com", "facebook.com",
    "instagram.com", "twitter.com", "x.com", "linkedin.com",
    "youtube.com", "wikipedia.org", "reddit.com", "bbb.org",
    "mapquest.com", "tripadvisor.com", "healthgrades.com",
    "zocdoc.com", "vitals.com", "webmd.com", "nerdwallet.com",
    "angi.com", "thumbtack.com", "homeadvisor.com", "nextdoor.com",
    "avvo.com", "findlaw.com", "justia.com", "realtor.com",
    "zillow.com", "redfin.com", "trulia.com", "indeed.com",
    "deltadental.com", "aspen-dental.com", "1800dentist.com",
    "dentistry.com", "mouthhealthy.org", "ada.org",
    "duckduckgo.com", "html.duckduckgo.com", "brave.com",
    "search.brave.com", "bing.com", "yahoo.com", "google.com",
    "opencare.com", "toprateddentist.com", "denscore.com",
    "expertise.com", "threebestrated.com", "dentistsup.com",
    "getyourdentist.com",
]


def _skip_domain(href):
    return any(d in href.lower() for d in _SKIP_DOMAINS)


def _clean_result_title(raw_title, url):
    """Clean up a search result title into a business name."""
    name = raw_title.strip()

    # Remove common breadcrumb fragments
    name = re.sub(r'›[^›]*$', '', name).strip()
    name = re.sub(r'›.*', '', name).strip()

    # If the title starts with the domain glued in, extract after .com/.net/.org
    m = re.search(r'\.(com|net|org|co|io|us)\s*(.+)', name, re.I)
    if m and len(m.group(2).strip()) > 5:
        name = m.group(2).strip()

    # Strip trailing pipes ("... | Site Name")
    name = re.sub(r'\s*[|]\s*.*$', '', name).strip()
    # Strip trailing dash suffixes if result is still >5 chars
    dash_stripped = re.sub(r'\s*-\s*[^-]*$', '', name).strip()
    if len(dash_stripped) > 5:
        name = dash_stripped

    # Remove "Home" prefix
    name = re.sub(r'^Home\s*[-|:]\s*', '', name, flags=re.I).strip()

    # If name is junk, derive from URL domain
    if not name or len(name) < 3 or (name == name.lower() and ' ' not in name):
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        domain_name = re.sub(r'\.(com|net|org|co|io|us)$', '', domain)
        domain_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', domain_name)
        domain_name = re.sub(r'[-_.]', ' ', domain_name).strip().title()
        if domain_name and len(domain_name) >= 3:
            name = domain_name

    return name


def scrape_duckduckgo(session, category, city, limit):
    """Search DuckDuckGo for local business websites.

    Uses the duckduckgo_search library (DDGS) which handles rate limiting
    and anti-bot evasion internally. Falls back to raw HTML POST if the
    library is unavailable. Runs multiple query variations to maximize
    coverage and filters out aggregator sites.
    """
    biz, seen_urls, seen_names = [], set(), set()

    # Multiple query variations targeting actual business sites (not directories)
    queries = [
        f"{category} near {city}",
        f"best {category} {city} website",
        f"{category} office {city}",
        f"{category} practice {city}",
        f"local {category} {city}",
        f"{category} {city} site:.com",
        f'"{category}" "{city}" official website',
    ]

    for qi, q in enumerate(queries):
        if len(biz) >= limit or _shutdown:
            break

        rate_limit(1.0, 2.5)

        raw_results = []

        if _HAS_DDGS:
            # Use the duckduckgo_search library (handles rate limits internally)
            try:
                ddgs = DDGS()
                raw_results = list(ddgs.text(q, max_results=15))
            except Exception as e:
                print(f"\n    [DDG] Query {qi+1} error: {str(e)[:60]}")
                continue
        else:
            # Fallback: raw HTTP POST to DDG HTML endpoint
            ddg_session = get_session()
            ddg_session.headers.update({
                "Referer": "https://html.duckduckgo.com/",
                "Origin": "https://html.duckduckgo.com",
                "Content-Type": "application/x-www-form-urlencoded",
            })
            try:
                resp = ddg_session.post("https://html.duckduckgo.com/html/",
                                        data={"q": q}, timeout=20,
                                        allow_redirects=True)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    for a_tag in soup.select("a.result__a"):
                        raw_href = a_tag.get("href", "")
                        href = raw_href
                        if "uddg=" in raw_href:
                            m = re.search(r'uddg=([^&]+)', raw_href)
                            if m:
                                href = urllib.parse.unquote(m.group(1))
                        title = a_tag.get_text(strip=True)
                        parent = a_tag.find_parent(class_="result")
                        body = ""
                        if parent:
                            snippet = parent.select_one(".result__snippet")
                            if snippet:
                                body = snippet.get_text(" ", strip=True)
                        raw_results.append({"title": title, "href": href, "body": body})
            except Exception as e:
                print(f"\n    [DDG] Query {qi+1} fallback error: {str(e)[:60]}")
                continue

        # Process results from either method
        for r in raw_results:
            try:
                href = r.get("href", "")
                if not href or not href.startswith("http"):
                    continue
                if _skip_domain(href):
                    continue

                # Deduplicate by domain
                parsed = urlparse(href)
                domain = parsed.netloc.lower().replace("www.", "")
                if domain in seen_urls:
                    continue

                # Extract title
                raw_title = r.get("title", "")
                name = _clean_result_title(raw_title, href)

                if not name or len(name) < 3:
                    continue

                # Dedup by name
                nk = re.sub(r'[^a-z0-9]', '', name.lower())
                if nk in seen_names and len(nk) > 3:
                    continue

                # Extract phones from snippet body
                body = r.get("body", "")
                phs = extract_phones(body)

                seen_urls.add(domain)
                if nk and len(nk) > 2:
                    seen_names.add(nk)

                biz.append({
                    "business_name": name,
                    "address": "",
                    "phone": phs[0] if phs else "",
                    "website": href,
                    "google_rating": "",
                    "review_count": "",
                    "category": category,
                    "city": city,
                    "_src": "duckduckgo",
                })

                if len(biz) >= limit:
                    break

            except Exception:
                continue

    return biz[:limit]


def scrape_brave(session, category, city, limit):
    """Search Brave for local business websites. Primary fallback when DDG is blocked.

    Brave Search serves real HTML results (no JS rendering needed).
    No API key required for HTML scraping.
    """
    biz, seen_urls, seen_names = [], set(), set()

    queries = [
        f"{category} near {city}",
        f"best {category} {city}",
        f"{category} office {city}",
        f"local {category} {city}",
    ]

    for qi, q in enumerate(queries):
        if len(biz) >= limit or _shutdown:
            break

        rate_limit(2.0, 4.0)
        raw_results = []

        try:
            encoded_q = urllib.parse.quote_plus(q)
            brave_url = f"https://search.brave.com/search?q={encoded_q}&source=web"
            bsess = get_session()
            bsess.headers.update({
                "Referer": "https://search.brave.com/",
            })
            resp, err = safe_get(bsess, brave_url, timeout=15)
            if resp and resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                # Brave uses div.snippet a for result links
                for a_tag in soup.select("div.snippet a[href]"):
                    href = a_tag.get("href", "")
                    if href.startswith("http"):
                        title = a_tag.get_text(strip=True)
                        raw_results.append({"title": title, "href": href, "body": ""})
                # Also try direct external links as fallback
                if not raw_results:
                    for a_tag in soup.find_all("a", href=True):
                        href = a_tag.get("href", "")
                        if href.startswith("http") and "brave.com" not in href and "search." not in href:
                            title = a_tag.get_text(strip=True)
                            if title and len(title) > 5:
                                raw_results.append({"title": title, "href": href, "body": ""})
            elif resp:
                print(f"\n    [Brave] Query {qi+1} status: {resp.status_code}")
            else:
                print(f"\n    [Brave] Query {qi+1} error: {err}")
        except Exception as e:
            print(f"\n    [Brave] Query {qi+1} error: {str(e)[:60]}")
            continue

        # Process results
        for r in raw_results:
            try:
                href = r.get("href", "")
                if not href or not href.startswith("http"):
                    continue
                if _skip_domain(href):
                    continue

                parsed = urlparse(href)
                domain = parsed.netloc.lower().replace("www.", "")
                if domain in seen_urls:
                    continue

                raw_title = r.get("title", "")
                name = _clean_result_title(raw_title, href)
                if not name or len(name) < 3:
                    domain_name = re.sub(r'\.(com|net|org|co|io|us)$', '', domain)
                    domain_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', domain_name)
                    domain_name = re.sub(r'[-_.]', ' ', domain_name).strip().title()
                    name = domain_name if domain_name and len(domain_name) >= 3 else ""
                if not name or len(name) < 3:
                    continue

                nk = re.sub(r'[^a-z0-9]', '', name.lower())
                if nk in seen_names and len(nk) > 3:
                    continue

                body = r.get("body", "")
                phs = extract_phones(body)

                seen_urls.add(domain)
                if nk and len(nk) > 2:
                    seen_names.add(nk)

                biz.append({
                    "business_name": name,
                    "address": "",
                    "phone": phs[0] if phs else "",
                    "website": href,
                    "google_rating": "",
                    "review_count": "",
                    "category": category,
                    "city": city,
                    "_src": "brave",
                })

                if len(biz) >= limit:
                    break
            except Exception:
                continue

    return biz[:limit]


def scrape_google(session, category, city, limit):
    """Search Google for local business websites. Last resort fallback.

    Uses googlesearch-python library. Google aggressively rate-limits, so
    Brave is preferred as the first fallback.
    """
    biz, seen_urls, seen_names = [], set(), set()

    queries = [
        f"{category} near {city}",
        f"best {category} {city} website",
        f"local {category} {city}",
    ]

    for qi, q in enumerate(queries):
        if len(biz) >= limit or _shutdown:
            break

        rate_limit(3.0, 6.0)  # Very slow for Google
        raw_results = []

        if _HAS_GOOGLE:
            try:
                for url in google_search(q, num_results=15, lang="en"):
                    raw_results.append({"title": "", "href": url, "body": ""})
            except Exception as e:
                print(f"\n    [Google] Query {qi+1} error: {str(e)[:60]}")
                continue

        # Process results
        for r in raw_results:
            try:
                href = r.get("href", "")
                if not href or not href.startswith("http"):
                    continue
                if _skip_domain(href):
                    continue

                parsed = urlparse(href)
                domain = parsed.netloc.lower().replace("www.", "")
                if domain in seen_urls:
                    continue

                domain_name = re.sub(r'\.(com|net|org|co|io|us)$', '', domain)
                domain_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', domain_name)
                name = re.sub(r'[-_.]', ' ', domain_name).strip().title()
                if not name or len(name) < 3:
                    continue

                nk = re.sub(r'[^a-z0-9]', '', name.lower())
                if nk in seen_names and len(nk) > 3:
                    continue

                seen_urls.add(domain)
                if nk and len(nk) > 2:
                    seen_names.add(nk)

                biz.append({
                    "business_name": name,
                    "address": "",
                    "phone": "",
                    "website": href,
                    "google_rating": "",
                    "review_count": "",
                    "category": category,
                    "city": city,
                    "_src": "google",
                })

                if len(biz) >= limit:
                    break
            except Exception:
                continue

    return biz[:limit]


def discover_businesses(session, category, city, limit=50):
    """Discover businesses using search engines.

    Tries DuckDuckGo first, falls back to Google if DDG is blocked/rate-limited.
    Uses multiple search query variations to find actual business websites,
    filtering out aggregator sites (Yelp, YellowPages, Healthgrades, etc.).
    """
    all_biz, seen = [], set()
    print(f"[*] Searching: {category} in {city}")

    # Fallback chain: DDG -> Brave -> Google
    print(f"  [DuckDuckGo] Running query variations...", end=" ", flush=True)
    results = scrape_duckduckgo(session, category, city, limit)
    print(f"{len(results)} results")
    all_biz.extend(results)

    if len(all_biz) == 0:
        print(f"  [DDG returned 0] Falling back to Brave Search...")
        print(f"  [Brave] Running query variations...", end=" ", flush=True)
        results = scrape_brave(session, category, city, limit)
        print(f"{len(results)} results")
        all_biz.extend(results)

    if len(all_biz) == 0:
        print(f"  [Brave returned 0] Falling back to Google...")
        print(f"  [Google] Running query variations...", end=" ", flush=True)
        results = scrape_google(session, category, city, limit)
        print(f"{len(results)} results")
        all_biz.extend(results)

    # Deduplicate
    unique = []
    for b in all_biz:
        nk = re.sub(r'[^a-z0-9]', '', b["business_name"].lower())
        if nk not in seen and len(nk) > 2:
            seen.add(nk)
            unique.append(b)
    # Prioritize those with real websites
    unique.sort(key=lambda b: (0 if b.get("website") and "yelp.com" not in b.get("website", "") else 1,
                                0 if b.get("phone") else 1))
    print(f"  -> {len(unique)} unique businesses (from {len(all_biz)} raw)")
    return unique[:limit]


# ============================================================================
# WEBSITE ANALYSIS & SCORING (0-100, low = bad = hot lead)
# ============================================================================

def resolve_website(session, biz):
    """If URL is a Yelp page, try to extract the real business website."""
    url = biz.get("website", "")
    if not url or "yelp.com/biz/" not in url:
        return biz
    rate_limit(1.5, 3.0)
    resp, err = safe_get(session, url, timeout=15)
    if resp and resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.select("a[href]"):
            if "biz_redir" in a.get("href", ""):
                m = re.search(r'url=([^&]+)', a["href"])
                if m:
                    biz["website"] = urllib.parse.unquote(m.group(1))
                    break
        if not biz.get("phone"):
            phs = extract_phones(soup.get_text(" ", strip=True))
            if phs: biz["phone"] = phs[0]
    return biz


def analyze_website(session, url):
    """Score a website 0-100. Higher = better site. Lower = hotter lead."""
    if not url or not url.startswith("http"):
        return {"score": 15, "signals": ["no_website"], "emails": []}

    listing = ["yelp.com", "yellowpages.com", "facebook.com", "instagram.com",
               "twitter.com", "x.com", "linkedin.com", "bbb.org"]
    if any(d in url.lower() for d in listing):
        return {"score": 20, "signals": ["directory_listing_only"], "emails": []}

    signals = []
    score = 50

    # 1. SSL
    if url.startswith("https"):
        score += 5; signals.append("has_ssl")
    else:
        score -= 10; signals.append("NO_ssl")

    # 2. Fetch
    t0 = time.time()
    resp, err = safe_get(session, url, timeout=15)
    load = time.time() - t0
    if err or not resp:
        return {"score": 10, "signals": signals + [f"unreachable:{err}"], "emails": []}
    if resp.status_code >= 400:
        return {"score": 12, "signals": signals + [f"http_{resp.status_code}"], "emails": []}

    # 3. Speed
    if load < 1.0: score += 5; signals.append(f"fast:{load:.1f}s")
    elif load < 3.0: signals.append(f"ok:{load:.1f}s")
    elif load < 6.0: score -= 5; signals.append(f"slow:{load:.1f}s")
    else: score -= 10; signals.append(f"VERY_slow:{load:.1f}s")

    html = resp.text
    hl = html.lower()
    soup = BeautifulSoup(html, "html.parser")

    # 4. Mobile responsive
    vp = soup.find("meta", attrs={"name": "viewport"})
    if vp and "width=device-width" in str(vp):
        score += 5; signals.append("mobile_ok")
    else:
        score -= 15; signals.append("NOT_mobile")

    # 5. Old tech
    old_markers = {"font-awesome/4": "FA4", "bootstrap/3": "BS3", "bootstrap/2": "BS2",
                   "jquery-1.": "jQ1", "jquery/1.": "jQ1", "jquery-2.": "jQ2", "jquery/2.": "jQ2"}
    old_found = list({v for k, v in old_markers.items() if k in hl})
    if old_found:
        score -= min(len(old_found) * 5, 20)
        signals.extend([f"OLD:{x}" for x in old_found[:3]])

    # 6. Modern tech
    mod_markers = {"_next/": "NextJS", "nuxt": "Nuxt", "gatsby": "Gatsby",
                   "tailwindcss": "Tailwind", "tailwind": "Tailwind"}
    mod_found = list({v for k, v in mod_markers.items() if k in hl})
    if mod_found:
        score += min(len(mod_found) * 3, 12)
        signals.extend([f"MOD:{x}" for x in mod_found[:3]])

    # 7. CMS
    gen = soup.find("meta", attrs={"name": "generator"})
    gc = gen.get("content", "").lower() if gen else ""
    if "wordpress" in gc or "wp-content" in hl or "wp-includes" in hl:
        signals.append("WordPress")
    elif "squarespace" in gc or "squarespace" in hl:
        score += 5; signals.append("Squarespace")
    elif "wix" in gc or "wix.com" in hl:
        score += 3; signals.append("Wix")
    elif "weebly" in hl: signals.append("Weebly")
    elif "godaddy" in hl: signals.append("GoDaddy")

    # 8. Social links
    soc_count = 0
    for a in soup.find_all("a", href=True):
        h = a["href"].lower()
        if any(p in h for p in ["facebook.com", "instagram.com", "twitter.com", "x.com",
                                 "linkedin.com", "youtube.com", "tiktok.com"]):
            soc_count += 1
    if soc_count >= 3: score += 5; signals.append(f"social:{soc_count}")
    elif soc_count >= 1: score += 2; signals.append(f"social:{soc_count}")
    else: score -= 5; signals.append("no_social")

    # 9. Contact form
    has_form = False
    for form in soup.find_all("form"):
        ft = (form.get_text(" ", strip=True) + str(form)).lower()
        if any(kw in ft for kw in ["contact", "message", "email", "appointment",
                                     "schedule", "book", "quote", "estimate"]):
            has_form = True; break
        if form.find("textarea") and form.find("input", {"type": "email"}):
            has_form = True; break
    if has_form: score += 5; signals.append("contact_form")
    else: score -= 3; signals.append("no_form")

    # 10. Google Maps embed
    has_map = ("maps.google" in hl or "google.com/maps" in hl or "maps.googleapis" in hl)
    if not has_map:
        for iframe in soup.find_all("iframe", src=True):
            if "google" in iframe["src"].lower() and "map" in iframe["src"].lower():
                has_map = True; break
    if has_map: score += 3; signals.append("map_embed")

    # 11. Title / meta description
    title = soup.find("title")
    tt = title.get_text(strip=True) if title else ""
    md = soup.find("meta", attrs={"name": "description"})
    dt = md.get("content", "") if md else ""
    if tt and 15 <= len(tt) <= 70: score += 3; signals.append("good_title")
    elif not tt or len(tt) < 10: score -= 5; signals.append("bad_title")
    if dt and 50 <= len(dt) <= 160: score += 3; signals.append("good_desc")
    elif not dt: score -= 5; signals.append("no_desc")

    # 12. Schema.org
    has_schema = ("schema.org" in hl or soup.find("script", {"type": "application/ld+json"}))
    if has_schema: score += 5; signals.append("schema")
    else: score -= 3; signals.append("no_schema")

    # 13. Image optimization
    imgs = soup.find_all("img")
    if imgs:
        lazy = sum(1 for i in imgs if i.get("loading") == "lazy" or i.get("data-src"))
        webp = sum(1 for i in imgs if ".webp" in (i.get("src", "") + i.get("data-src", "")).lower())
        if lazy / len(imgs) > 0.3: score += 3; signals.append("lazy_load")
        if webp > 0: score += 2; signals.append("webp")
    else:
        score -= 2; signals.append("no_images")

    # 14. Copyright year
    footer = soup.find("footer") or soup.find(class_=re.compile(r"footer", re.I))
    page_text = soup.get_text(" ", strip=True)
    for text_block in [footer.get_text(" ", strip=True) if footer else "", page_text]:
        ym = re.search(r'(?:copyright|\xa9|©)\s*(\d{4})', text_block.lower())
        if ym:
            yr = int(ym.group(1))
            now = datetime.now().year
            if yr >= now - 1: score += 3; signals.append(f"(c){yr}")
            elif yr >= now - 3: signals.append(f"(c){yr}")
            else: score -= 8; signals.append(f"OLD_(c){yr}")
            break

    # 15. Phone on page
    phs = extract_phones(page_text)
    if phs: score += 2; signals.append(f"phone_on_site:{len(phs)}")

    # 16. Hours listed
    hrs = [r'(mon|tue|wed|thu|fri|sat|sun)\w*\s*[-:]\s*\d',
           r'\d{1,2}:\d{2}\s*(am|pm)\s*[-to]+\s*\d{1,2}:\d{2}\s*(am|pm)',
           r'hours of operation', r'business hours', r'office hours']
    if any(re.search(p, page_text.lower()) for p in hrs):
        score += 3; signals.append("hours_listed")

    # Emails
    emails = extract_emails(html)

    return {"score": max(0, min(100, score)), "signals": signals, "emails": emails}


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_scraper(category, city, limit=50, resume=False):
    """Full pipeline: discover -> resolve -> analyze -> score -> CSV."""
    LEADS_DIR.mkdir(parents=True, exist_ok=True)

    ckpt = load_checkpoint(category, city) if resume else {"done": [], "results": []}
    done_urls = set(ckpt.get("done", []))
    scored = ckpt.get("results", [])

    if resume and scored:
        print(f"[*] Resuming: {len(scored)} already scored")

    session = get_session()

    print(f"\n{'='*60}")
    print(f"  SAVVY LEAD SCRAPER")
    print(f"  {category.upper()} in {city.upper()} | limit {limit}")
    print(f"{'='*60}\n")

    raw = discover_businesses(session, category, city, limit=limit)
    if not raw:
        print("[!] No businesses found. Check search terms or connection.")
        return []

    # Resolve real websites
    print(f"\n[*] Resolving business websites...")
    for i, b in enumerate(raw):
        if _shutdown: break
        raw[i] = resolve_website(session, b)

    # Analyze
    print(f"\n[*] Analyzing {len(raw)} websites (1-3s delay each)...\n")
    for i, b in enumerate(raw):
        if _shutdown: break
        url = b.get("website", "")
        uk = url.lower().strip() if url else f"nourl_{b['business_name']}"
        if uk in done_urls:
            print(f"  [{i+1}/{len(raw)}] SKIP: {b['business_name'][:40]}"); continue
        print(f"  [{i+1}/{len(raw)}] {b['business_name'][:40]}", end="")
        if url and not any(d in url for d in ["yelp.com", "yellowpages.com"]):
            print(f"  {url[:45]}", end="")
        print()
        rate_limit(1.0, 2.5)
        a = analyze_website(session, url)
        scored.append({
            "business_name": b["business_name"],
            "address": b.get("address", ""),
            "phone": b.get("phone", ""),
            "website": b.get("website", ""),
            "google_rating": b.get("google_rating", ""),
            "review_count": b.get("review_count", ""),
            "website_score": a["score"],
            "signals_detected": "; ".join(a["signals"]),
            "email_if_found": "; ".join(a["emails"][:3]),
            "category": category, "city": city,
            "scraped_at": datetime.now().isoformat(),
        })
        done_urls.add(uk)
        tag = "HOT LEAD" if a["score"] <= 30 else "WARM" if a["score"] <= 50 else "COOL" if a["score"] <= 70 else "GOOD SITE"
        em = f" | emails:{len(a['emails'])}" if a["emails"] else ""
        print(f"           -> {a['score']}/100 [{tag}]{em}")
        if (i + 1) % 5 == 0:
            save_checkpoint(category, city, {"done": list(done_urls), "results": scored})

    save_checkpoint(category, city, {"done": list(done_urls), "results": scored})

    # Sort low->high (hottest first)
    scored.sort(key=lambda x: x.get("website_score", 100))

    # Write CSV
    city_slug = re.sub(r'[^a-z0-9]+', '_', city.lower()).strip('_')
    cat_slug = re.sub(r'[^a-z0-9]+', '_', category.lower()).strip('_')
    out = LEADS_DIR / f"{cat_slug}_{city_slug}_leads.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        w.writeheader()
        for r in scored:
            w.writerow({k: r.get(k, "") for k in CSV_HEADERS})

    # Summary
    hot = [b for b in scored if b.get("website_score", 100) <= 30]
    warm = [b for b in scored if 30 < b.get("website_score", 100) <= 50]
    cool = [b for b in scored if 50 < b.get("website_score", 100) <= 70]
    good = [b for b in scored if b.get("website_score", 100) > 70]
    em_count = len([b for b in scored if b.get("email_if_found")])

    print(f"\n{'='*60}")
    print(f"  RESULTS: {len(scored)} businesses scored")
    print(f"  HOT  (0-30):  {len(hot)}")
    print(f"  WARM (31-50): {len(warm)}")
    print(f"  COOL (51-70): {len(cool)}")
    print(f"  GOOD (71+):   {len(good)}")
    print(f"  With emails:  {em_count}")
    print(f"  Output: {out}")
    if hot:
        print(f"\n  TOP HOT LEADS:")
        for h in hot[:5]:
            print(f"    {h['website_score']:3d}/100 | {h['business_name'][:35]} | {h.get('website', 'N/A')[:50]}")
    print(f"{'='*60}\n")
    return scored


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Savvy Lead Scraper - Quant-level local business lead scoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 savvy_lead_scraper.py --category "dental" --city "Austin TX" --limit 50
  python3 savvy_lead_scraper.py --category "plumbing" --city "Denver CO" --limit 30 --resume
  python3 savvy_lead_scraper.py --category "restaurant" --city "Miami FL"

Scoring (lower = hotter lead):
  0-30:  HOT LEAD  (bad website, needs redesign)
  31-50: WARM LEAD (mediocre, room for improvement)
  51-70: COOL      (decent, not priority)
  71-100: GOOD SITE (modern, skip for outreach)

Output: AUTOMATIONS/leads/[category]_[city]_leads.csv
""")
    parser.add_argument("--category", "-c", required=True,
                        help="Business category (dental, plumbing, restaurant, etc.)")
    parser.add_argument("--city", "-C", required=True,
                        help="City and state (e.g., 'Austin TX', 'Denver CO')")
    parser.add_argument("--limit", "-l", type=int, default=50,
                        help="Max businesses to scrape (default: 50)")
    parser.add_argument("--resume", "-r", action="store_true",
                        help="Resume from last checkpoint")
    parser.add_argument("--output", "-o",
                        help="Custom output CSV path (overrides default)")
    parser.add_argument("--proxy", "-p",
                        help="Proxy URL (e.g., socks5://user:pass@host:port, http://host:port)")

    args = parser.parse_args()

    if args.proxy:
        global _PROXY
        _PROXY = args.proxy
        print(f"[*] Using proxy: {args.proxy[:30]}...")

    results = run_scraper(category=args.category, city=args.city,
                          limit=args.limit, resume=args.resume)
    if args.output and results:
        p = Path(args.output)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            w.writeheader()
            for r in results:
                w.writerow({k: r.get(k, "") for k in CSV_HEADERS})
        print(f"[+] Also saved to: {p}")
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
