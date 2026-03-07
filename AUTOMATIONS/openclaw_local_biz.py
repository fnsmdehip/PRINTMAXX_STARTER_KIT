#!/usr/bin/env python3
"""
OpenClaw Local Business Pipeline — 24/7 autonomous lead-to-client engine.
Finds businesses without websites, auto-builds a preview, deploys to surge.sh, queues outreach.
Op N61 — Nationwide Local Biz Website Redesign — PRIORITY_LAUNCH rank #1.

Usage: --discover "Austin TX" "dentist" | --build | --outreach | --daemon | --status
"""

import argparse
import csv
import html as html_mod
import json
import os
import random
import re
import signal
import socket
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ── paths & guardrails ───────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS  = PROJECT_ROOT / "AUTOMATIONS"
LEADS_DIR    = AUTOMATIONS / "leads" / "openclaw"
BUILD_DIR    = AUTOMATIONS / "leads" / "openclaw" / "_sites"
LEADS_CSV    = LEADS_DIR / "openclaw_leads.csv"
OUTREACH_CSV = LEADS_DIR / "outreach_queue.csv"
STATE_FILE   = LEADS_DIR / ".openclaw_state.json"
LOG_FILE     = LEADS_DIR / "openclaw.log"

LEADS_HEADERS = [
    "business_name", "address", "phone", "website", "email",
    "grade", "website_score", "category", "city",
    "preview_url", "status", "discovered_at",
]
OUTREACH_HEADERS = [
    "business_name", "email", "phone", "preview_url",
    "email_subject", "email_body", "status", "created_at",
]

# daemon config
DAEMON_CITIES = [
    "Austin TX","Miami FL","Phoenix AZ","Denver CO","Atlanta GA","Nashville TN",
    "Tampa FL","Charlotte NC","Orlando FL","Dallas TX","San Antonio TX",
    "Jacksonville FL","Raleigh NC","Columbus OH","Indianapolis IN","Memphis TN",
    "Las Vegas NV","Oklahoma City OK","Portland OR","Tucson AZ",
]
DAEMON_NICHES = [
    "dentist","plumber","hvac","lawyer","restaurant","salon","gym",
    "chiropractor","auto repair","roofing",
]
CYCLE_INTERVAL_S = 4 * 3600  # 4 hours per city

_shutdown = False
def _sig(s, f):
    global _shutdown
    _shutdown = True
    print("\n[!] Shutdown requested.")
signal.signal(signal.SIGINT, _sig)
signal.signal(signal.SIGTERM, _sig)


def safe_path(p):
    """Verify path stays inside project root."""
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} outside {PROJECT_ROOT}")
    return resolved


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        safe_path(LOG_FILE)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

def load_state():
    if STATE_FILE.exists():
        try: return json.loads(STATE_FILE.read_text())
        except Exception: pass
    return {"last_cycles": {}, "total_leads": 0, "total_sites_built": 0}

def save_state(st):
    safe_path(STATE_FILE)
    STATE_FILE.write_text(json.dumps(st, indent=2, default=str))

# ── HTTP helpers (stdlib only) ────────────────────────────────────────────────

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def http_get(url, timeout=12):
    """GET with urllib — returns (body_str, final_url, status, error)."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        body = resp.read(500_000).decode("utf-8", errors="replace")
        return body, resp.url, resp.status, None
    except urllib.error.HTTPError as e:
        return "", url, e.code, str(e)
    except Exception as e:
        return "", url, 0, str(e)[:120]

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower().strip()).strip("-")[:60]

# ── Phase 1: Lead Discovery ──────────────────────────────────────────────────

def search_businesses(city, niche, limit=20):
    """Search DuckDuckGo HTML for local businesses."""
    query = f"{niche} in {city}"
    encoded = urllib.parse.quote_plus(query)
    results = []

    for start in range(0, min(limit, 40), 10):
        url = f"https://html.duckduckgo.com/html/?q={encoded}&s={start}"
        body, _, status, err = http_get(url, timeout=15)
        if err or status != 200:
            log(f"  search error page {start}: {err}")
            continue

        # parse result snippets
        for m in re.finditer(
            r'<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            body, re.DOTALL
        ):
            raw_url = m.group(1)
            title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            # DuckDuckGo wraps URLs in redirects — extract actual URL
            actual = raw_url
            parsed = urllib.parse.urlparse(raw_url)
            qs = urllib.parse.parse_qs(parsed.query)
            if "uddg" in qs:
                actual = qs["uddg"][0]

            if not title or not actual:
                continue
            # skip aggregator sites
            dominated = ["yelp.com", "yellowpages.com", "facebook.com",
                         "mapquest.com", "bbb.org", "angi.com",
                         "thumbtack.com", "google.com", "tripadvisor.com",
                         "nextdoor.com", "healthgrades.com", "zocdoc.com"]
            domain = urllib.parse.urlparse(actual).hostname or ""
            if any(d in domain for d in dominated):
                continue

            results.append({"name": title, "url": actual, "domain": domain})
            if len(results) >= limit:
                break

        time.sleep(random.uniform(1.5, 3.0))
        if len(results) >= limit:
            break

    return results

def extract_contact(body, url):
    """Pull phone, email, address from page HTML."""
    phone, email, address = "", "", ""
    # phone
    ph = re.findall(r'tel:([+\d\-() .]{7,20})', body)
    if not ph: ph = re.findall(r'(?:phone|call|tel)[:\s]*([(\d][\d\-() .]{8,18})', body, re.I)
    if not ph: ph = re.findall(r'\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}', body)
    if ph: phone = re.sub(r'[^\d+]', '', ph[0])
    # email
    em = re.findall(r'mailto:([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,})', body)
    if not em: em = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', body)
    _junk = ["example.com","wixpress","sentry","wordpress","googleapis","schema.org"]
    for e in em:
        if not any(x in e.lower() for x in _junk):
            email = e; break
    # address
    addr = re.findall(
        r'\d{1,5}\s+[\w\s]{2,30}(?:St|Ave|Blvd|Dr|Rd|Ln|Way|Ct|Pkwy|Hwy|Circle|Place|Suite)\.?[,\s]+[\w\s]+,?\s*[A-Z]{2}\s*\d{5}',
        body, re.I)
    if addr: address = addr[0].strip()
    return phone, email, address

def grade_website(body, url, status, err):
    """Grade A-F. Returns (grade, score 0-100, signals list)."""
    if err or status == 0: return "F", 0, ["no_website_reachable"]
    if status >= 400: return "F", 5, [f"http_{status}"]
    signals, score, lower = [], 50, body.lower()
    length = len(body)
    if length < 500: score -= 25; signals.append("nearly_empty")
    elif length < 2000: score -= 10; signals.append("very_thin_content")
    if 'viewport' in lower: score += 10
    else: score -= 15; signals.append("no_viewport")
    if url.startswith("http://"): score -= 10; signals.append("no_https")
    if 'wix.com' in lower or 'squarespace.com' in lower: score += 5
    if '<table' in lower and lower.count('<table') > 3: score -= 15; signals.append("table_layout")
    if '<marquee' in lower or '<blink' in lower: score -= 20; signals.append("archaic_html")
    if 'under construction' in lower or 'coming soon' in lower: score -= 20; signals.append("under_construction")
    if 'font-family' in lower or ('google' in lower and 'fonts' in lower): score += 5
    if '@media' in lower: score += 5
    if 'flex' in lower or 'grid' in lower: score += 5
    if re.search(r'\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}', body): score += 5
    else: signals.append("no_phone_visible")
    yr = datetime.now().year
    if str(yr) in body or str(yr - 1) in body: score += 5
    elif re.search(r'20[01]\d', body): score -= 10; signals.append("outdated_copyright")
    if 'parked' in lower and 'godaddy' in lower: score -= 30; signals.append("parked_domain")
    score = max(0, min(100, score))
    grade = "A" if score >= 75 else "B" if score >= 55 else "C" if score >= 35 else "D" if score >= 15 else "F"
    return grade, score, signals


def discover(city, niche, limit=20):
    """Full discovery: search -> visit -> grade -> save CSV."""
    log(f"Discovering {niche} in {city} (limit {limit})...")
    LEADS_DIR.mkdir(parents=True, exist_ok=True)

    raw = search_businesses(city, niche, limit=limit)
    log(f"  Found {len(raw)} raw results")

    # load existing to dedup
    existing = set()
    if LEADS_CSV.exists():
        with open(LEADS_CSV, "r") as f:
            for row in csv.DictReader(f):
                existing.add(row.get("website", "").lower().strip())

    leads = []
    for biz in raw:
        if _shutdown:
            break
        if biz["url"].lower().strip() in existing:
            continue

        log(f"  Checking: {biz['name'][:50]}")
        body, final_url, status, err = http_get(biz["url"])
        grade, score, sigs = grade_website(body, final_url, status, err)
        phone, email, address = ("", "", "")
        if body:
            phone, email, address = extract_contact(body, final_url)

        lead = {
            "business_name": biz["name"],
            "address": address,
            "phone": phone,
            "website": biz["url"],
            "email": email,
            "grade": grade,
            "website_score": score,
            "category": niche,
            "city": city,
            "preview_url": "",
            "status": "new",
            "discovered_at": datetime.now().isoformat(),
        }
        leads.append(lead)
        existing.add(biz["url"].lower().strip())
        time.sleep(random.uniform(1.0, 2.0))

    # append to CSV
    write_header = not LEADS_CSV.exists()
    safe_path(LEADS_CSV)
    with open(LEADS_CSV, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEADS_HEADERS, extrasaction="ignore")
        if write_header:
            w.writeheader()
        w.writerows(leads)

    grades = {}
    for l in leads:
        grades[l["grade"]] = grades.get(l["grade"], 0) + 1
    log(f"  Saved {len(leads)} leads. Grades: {grades}")

    # update state
    st = load_state()
    st["total_leads"] = st.get("total_leads", 0) + len(leads)
    st["last_cycles"][f"{city}|{niche}"] = datetime.now().isoformat()
    save_state(st)

    return leads

# ── Phase 2: Site Builder ────────────────────────────────────────────────────

LANDING_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{biz_name} | {city}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1a1a2e;line-height:1.6}}
.hero{{background:linear-gradient(135deg,#0f0c29 0%,#302b63 50%,#24243e 100%);color:#fff;padding:80px 20px;text-align:center}}
.hero h1{{font-size:clamp(1.8rem,5vw,3rem);margin-bottom:12px;font-weight:800}}
.hero p{{font-size:1.15rem;opacity:.85;max-width:600px;margin:0 auto 28px}}
.cta-btn{{display:inline-block;background:#e94560;color:#fff;padding:16px 40px;border-radius:8px;text-decoration:none;font-weight:700;font-size:1.1rem;transition:transform .2s,box-shadow .2s}}
.cta-btn:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(233,69,96,.4)}}
.section{{max-width:900px;margin:0 auto;padding:60px 20px}}
.section h2{{font-size:1.8rem;margin-bottom:24px;color:#302b63;text-align:center}}
.services{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-top:20px}}
.svc-card{{background:#f8f9ff;border-radius:12px;padding:28px 20px;text-align:center;border:1px solid #e8e8f0;transition:transform .2s}}
.svc-card:hover{{transform:translateY(-4px);box-shadow:0 8px 20px rgba(0,0,0,.08)}}
.svc-card h3{{color:#302b63;margin-bottom:8px}}
.contact{{background:#f0f0f8;padding:60px 20px;text-align:center}}
.contact h2{{font-size:1.8rem;margin-bottom:16px;color:#302b63}}
.contact p{{font-size:1.1rem;margin-bottom:8px}}
.contact a{{color:#e94560;text-decoration:none;font-weight:600}}
.footer{{background:#0f0c29;color:rgba(255,255,255,.6);padding:30px 20px;text-align:center;font-size:.85rem}}
.footer a{{color:#e94560;text-decoration:none}}
@media(max-width:600px){{.hero{{padding:50px 16px}}.hero h1{{font-size:1.6rem}}.section{{padding:40px 16px}}}}
</style>
</head>
<body>
<div class="hero">
<h1>{biz_name}</h1>
<p>Your trusted {category} professionals in {city}. Quality service, real results.</p>
<a href="tel:{phone_raw}" class="cta-btn">Call {phone_display}</a>
</div>
<div class="section">
<h2>Our Services</h2>
<div class="services">
{services_html}
</div>
</div>
<div class="contact">
<h2>Get in Touch</h2>
{address_html}
<p>Phone: <a href="tel:{phone_raw}">{phone_display}</a></p>
{email_html}
<div style="margin-top:24px">
<a href="tel:{phone_raw}" class="cta-btn">Call Now</a>
</div>
</div>
<div class="footer">
<p>&copy; {year} {biz_name}. All rights reserved.</p>
<p style="margin-top:8px">Website by <a href="https://printmaxx.co">PRINTMAXX</a></p>
</div>
</body>
</html>"""

_SVC = {
    "dentist": ["General Dentistry","Teeth Cleaning","Cosmetic Dentistry","Emergency Dental","Dental Implants","Orthodontics"],
    "plumber": ["Emergency Plumbing","Drain Cleaning","Water Heater Repair","Pipe Repair","Bathroom Remodeling","Leak Detection"],
    "hvac": ["AC Repair","Heating Repair","HVAC Installation","Duct Cleaning","Thermostat Install","Maintenance Plans"],
    "lawyer": ["Personal Injury","Family Law","Criminal Defense","Estate Planning","Business Law","Free Consultation"],
    "restaurant": ["Dine-In","Takeout & Delivery","Catering","Private Events","Daily Specials","Online Ordering"],
    "salon": ["Haircuts & Styling","Color & Highlights","Manicure & Pedicure","Facial Treatments","Waxing","Bridal Packages"],
    "gym": ["Personal Training","Group Classes","Free Weights","Cardio Equipment","Nutrition Plans","Free Trial"],
    "chiropractor": ["Spinal Adjustment","Back Pain Relief","Sports Injury","Posture Correction","X-Ray Services","Wellness Plans"],
    "auto repair": ["Oil Change","Brake Service","Engine Repair","Transmission","AC Service","Diagnostics"],
    "roofing": ["Roof Repair","Roof Replacement","Leak Repair","Storm Damage","Free Inspection","Gutter Service"],
}
NICHE_SERVICES = {**_SVC, "dental": _SVC["dentist"], "plumbing": _SVC["plumber"]}

DEFAULT_SERVICES = ["Professional Service", "Quality Results", "Free Estimates", "Experienced Team", "Licensed & Insured", "Satisfaction Guaranteed"]


def build_site_html(lead):
    """Generate landing page HTML for a lead."""
    biz = html_mod.escape(lead.get("business_name", "Local Business"))
    city = html_mod.escape(lead.get("city", ""))
    cat = lead.get("category", "").lower()
    phone = lead.get("phone", "")
    email = lead.get("email", "")
    address = lead.get("address", "")

    phone_display = phone if phone else "(XXX) XXX-XXXX"
    phone_raw = re.sub(r'[^\d+]', '', phone) if phone else ""
    if not phone_raw:
        phone_raw = "#"
        phone_display = "Contact Us"

    services = NICHE_SERVICES.get(cat, DEFAULT_SERVICES)
    svc_html = ""
    for s in services:
        svc_html += f'<div class="svc-card"><h3>{html_mod.escape(s)}</h3><p>Professional {html_mod.escape(s.lower())} services for {html_mod.escape(city)} residents.</p></div>\n'

    addr_html = f'<p>{html_mod.escape(address)}</p>' if address else ""
    em_html = f'<p>Email: <a href="mailto:{html_mod.escape(email)}">{html_mod.escape(email)}</a></p>' if email else ""

    return LANDING_TEMPLATE.format(
        biz_name=biz, city=city, category=html_mod.escape(cat.title()),
        phone_raw=phone_raw, phone_display=phone_display,
        services_html=svc_html, address_html=addr_html,
        email_html=em_html, year=datetime.now().year,
    )


def deploy_surge(site_dir, domain_slug):
    """Deploy to surge.sh. Returns (url, success)."""
    domain = f"{domain_slug}.surge.sh"
    try:
        result = subprocess.run(
            ["npx", "surge", "--project", str(site_dir), "--domain", domain],
            capture_output=True, text=True, timeout=60,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode == 0:
            return f"https://{domain}", True
        log(f"  surge error: {result.stderr[:200]}")
        return f"https://{domain}", False
    except subprocess.TimeoutExpired:
        log("  surge deploy timed out")
        return f"https://{domain}", False
    except FileNotFoundError:
        log("  npx/surge not found")
        return f"https://{domain}", False


def build_sites(deploy=True):
    """Build preview sites for all D/F grade leads without a preview_url."""
    if not LEADS_CSV.exists():
        log("No leads CSV found. Run --discover first.")
        return 0

    rows = []
    with open(LEADS_CSV, "r") as f:
        rows = list(csv.DictReader(f))

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    built = 0

    for i, row in enumerate(rows):
        if _shutdown:
            break
        if row.get("grade", "C") not in ("D", "F"):
            continue
        if row.get("preview_url", "").strip():
            continue

        biz_slug = slugify(row.get("business_name", f"biz-{i}"))
        city_slug = slugify(row.get("city", "local"))
        domain_slug = f"{biz_slug}-{city_slug}"

        site_dir = BUILD_DIR / domain_slug
        safe_path(site_dir)
        site_dir.mkdir(parents=True, exist_ok=True)

        page_html = build_site_html(row)
        index = site_dir / "index.html"
        index.write_text(page_html)
        log(f"  Built: {domain_slug}/index.html")

        preview_url = f"file://{index}"
        if deploy:
            url, ok = deploy_surge(site_dir, domain_slug)
            if ok:
                preview_url = url
                log(f"  Deployed: {url}")
            else:
                log(f"  Deploy failed, local only: {index}")

        row["preview_url"] = preview_url
        row["status"] = "site_built"
        built += 1

    # rewrite CSV with updated preview_urls
    safe_path(LEADS_CSV)
    with open(LEADS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEADS_HEADERS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    st = load_state()
    st["total_sites_built"] = st.get("total_sites_built", 0) + built
    save_state(st)
    log(f"Built {built} preview sites.")
    return built

# ── Phase 3: Outreach ────────────────────────────────────────────────────────

def generate_email(lead):
    """Generate a cold email. No AI slop. Direct value prop."""
    biz = lead.get("business_name", "there")
    city = lead.get("city", "your area")
    cat = lead.get("category", "service")
    preview = lead.get("preview_url", "")
    phone = lead.get("phone", "")

    # subject line variations
    subjects = [
        f"I built {biz} a free website",
        f"Quick question for {biz}",
        f"Free website mockup for {biz}",
    ]
    subject = random.choice(subjects)

    body = (
        f"Hi,\n\n"
        f"I was looking for {cat} businesses in {city} and noticed "
        f"{biz} doesn't have a modern website yet (or the current one "
        f"could use a refresh).\n\n"
        f"I went ahead and built a free preview of what a clean, "
        f"mobile-friendly site could look like for you:\n\n"
        f"  {preview}\n\n"
        f"No strings attached. If you like it, we can get it live on "
        f"your own domain for a one-time fee. If not, no hard feelings.\n\n"
        f"Let me know what you think.\n\n"
        f"Max\n"
        f"PRINTMAXX Web Services\n"
        f"printmaxx.co"
    )

    return subject, body


def generate_outreach():
    """Create outreach queue from D/F leads with preview sites."""
    if not LEADS_CSV.exists():
        log("No leads CSV. Run --discover and --build first.")
        return 0

    rows = []
    with open(LEADS_CSV, "r") as f:
        rows = list(csv.DictReader(f))

    # load existing outreach to dedup
    existing_outreach = set()
    if OUTREACH_CSV.exists():
        with open(OUTREACH_CSV, "r") as f:
            for r in csv.DictReader(f):
                existing_outreach.add(r.get("business_name", "").lower())

    outreach_rows = []
    for row in rows:
        if row.get("grade", "C") not in ("D", "F"):
            continue
        if not row.get("preview_url", "").strip():
            continue
        if row.get("business_name", "").lower() in existing_outreach:
            continue

        subject, body = generate_email(row)
        outreach_rows.append({
            "business_name": row.get("business_name", ""),
            "email": row.get("email", ""),
            "phone": row.get("phone", ""),
            "preview_url": row.get("preview_url", ""),
            "email_subject": subject,
            "email_body": body.replace("\n", "\\n"),
            "status": "queued",
            "created_at": datetime.now().isoformat(),
        })

    if not outreach_rows:
        log("No new outreach to generate. Need D/F leads with built sites.")
        return 0

    write_header = not OUTREACH_CSV.exists()
    safe_path(OUTREACH_CSV)
    with open(OUTREACH_CSV, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUTREACH_HEADERS, extrasaction="ignore")
        if write_header:
            w.writeheader()
        w.writerows(outreach_rows)

    log(f"Queued {len(outreach_rows)} outreach emails.")
    w_email = sum(1 for r in outreach_rows if r["email"])
    log(f"  {w_email} have email addresses, {len(outreach_rows) - w_email} need manual lookup.")
    return len(outreach_rows)

# ── Phase 4: Daemon Loop ─────────────────────────────────────────────────────

def run_daemon():
    """24/7 autonomous loop: discover -> build -> outreach, cycling cities."""
    log("Starting OpenClaw daemon (Ctrl+C to stop)...")
    st = load_state()
    cycle = 0

    while not _shutdown:
        cycle += 1
        log(f"\n{'='*50}")
        log(f"DAEMON CYCLE {cycle}")
        log(f"{'='*50}")

        # pick city + niche combo that hasn't been run recently
        now = datetime.now()
        best_combo = None
        oldest_ts = now.isoformat()

        for city in DAEMON_CITIES:
            for niche in DAEMON_NICHES:
                key = f"{city}|{niche}"
                last = st.get("last_cycles", {}).get(key, "2000-01-01T00:00:00")
                if last < oldest_ts:
                    oldest_ts = last
                    best_combo = (city, niche)

        if not best_combo:
            best_combo = (random.choice(DAEMON_CITIES), random.choice(DAEMON_NICHES))

        city, niche = best_combo
        log(f"Selected: {niche} in {city}")

        # Phase 1: Discover
        try:
            discover(city, niche, limit=15)
        except Exception as e:
            log(f"Discovery error: {e}")

        if _shutdown:
            break

        # Phase 2: Build
        try:
            build_sites(deploy=True)
        except Exception as e:
            log(f"Build error: {e}")

        if _shutdown:
            break

        # Phase 3: Outreach
        try:
            generate_outreach()
        except Exception as e:
            log(f"Outreach error: {e}")

        # reload state for next iteration
        st = load_state()

        # wait
        log(f"Cycle {cycle} complete. Sleeping {CYCLE_INTERVAL_S // 60} min...")
        for _ in range(CYCLE_INTERVAL_S):
            if _shutdown:
                break
            time.sleep(1)

    log("Daemon stopped.")

# ── Status ────────────────────────────────────────────────────────────────────

def show_status():
    """Show pipeline status dashboard."""
    st = load_state()
    total = 0
    grades = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    with_preview = 0
    with_email = 0

    if LEADS_CSV.exists():
        with open(LEADS_CSV, "r") as f:
            for row in csv.DictReader(f):
                total += 1
                g = row.get("grade", "?")
                grades[g] = grades.get(g, 0) + 1
                if row.get("preview_url", "").strip():
                    with_preview += 1
                if row.get("email", "").strip():
                    with_email += 1

    outreach_count = 0
    outreach_queued = 0
    if OUTREACH_CSV.exists():
        with open(OUTREACH_CSV, "r") as f:
            for row in csv.DictReader(f):
                outreach_count += 1
                if row.get("status", "") == "queued":
                    outreach_queued += 1

    hot = grades.get("D", 0) + grades.get("F", 0)

    print(f"\n{'='*55}")
    print(f"  OPENCLAW LOCAL BIZ PIPELINE STATUS")
    print(f"{'='*55}")
    print(f"  Total leads:        {total}")
    print(f"  Grades:             A={grades['A']}  B={grades['B']}  C={grades['C']}  D={grades['D']}  F={grades['F']}")
    print(f"  Hot leads (D+F):    {hot}")
    print(f"  With email:         {with_email}")
    print(f"  Preview sites:      {with_preview}")
    print(f"  Outreach queued:    {outreach_queued} / {outreach_count} total")
    print(f"  Sites built (all):  {st.get('total_sites_built', 0)}")
    print(f"")
    print(f"  Leads CSV:    {LEADS_CSV}")
    print(f"  Outreach CSV: {OUTREACH_CSV}")
    print(f"  Sites dir:    {BUILD_DIR}")
    print(f"{'='*55}")

    cmd = "python3 AUTOMATIONS/openclaw_local_biz.py"
    if hot > 0 and with_preview == 0:
        print(f"\n  Next step: {cmd} --build")
    elif with_preview > 0 and outreach_queued == 0:
        print(f"\n  Next step: {cmd} --outreach")
    elif total == 0:
        print(f"\n  Next step: {cmd} --discover \"Austin TX\" \"dentist\"")
    print()

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw: autonomous local business website pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  --discover 'Austin TX' 'dentist'\n  --build\n  --build --no-deploy\n  --outreach\n  --daemon\n  --status")

    parser.add_argument("--discover", nargs=2, metavar=("CITY", "NICHE"),
                        help="Find leads: --discover 'Austin TX' 'dentist'")
    parser.add_argument("--limit", type=int, default=20,
                        help="Max leads per discovery run (default 20)")
    parser.add_argument("--build", action="store_true",
                        help="Build preview sites for D/F grade leads")
    parser.add_argument("--no-deploy", action="store_true",
                        help="Build HTML only, skip surge.sh deployment")
    parser.add_argument("--outreach", action="store_true",
                        help="Generate outreach emails for built sites")
    parser.add_argument("--daemon", action="store_true",
                        help="Run 24/7 autonomous loop")
    parser.add_argument("--status", action="store_true",
                        help="Show pipeline status")

    args = parser.parse_args()

    LEADS_DIR.mkdir(parents=True, exist_ok=True)

    if args.status:
        show_status()
    elif args.discover:
        city, niche = args.discover
        discover(city, niche, limit=args.limit)
        show_status()
    elif args.build:
        build_sites(deploy=not args.no_deploy)
        show_status()
    elif args.outreach:
        generate_outreach()
        show_status()
    elif args.daemon:
        run_daemon()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
