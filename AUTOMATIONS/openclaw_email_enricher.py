#!/usr/bin/env python3
"""
OpenClaw Email Enricher
Batch-visits real business websites (F/D grade leads without email)
to scrape contact pages for email addresses.
Writes results back to openclaw_leads.csv and outreach_queue.csv.
"""

from __future__ import annotations
import csv, re, ssl, socket, time, random, sys, json, urllib.request, urllib.parse
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEADS_CSV    = PROJECT_ROOT / "AUTOMATIONS/leads/openclaw/openclaw_leads.csv"
OUTREACH_CSV = PROJECT_ROOT / "AUTOMATIONS/leads/openclaw/outreach_queue.csv"
LOG_FILE     = PROJECT_ROOT / "AUTOMATIONS/leads/openclaw/enricher.log"

DIRECTORIES = {
    'yelp.com','angi.com','houzz.com','thumbtack.com','homeadvisor.com',
    'homeguide.com','carfax.com','meetaplumber.com','homestars.com',
    'checkatrade.com','bark.com','bbb.org','google.com','facebook.com',
    'yellowpages.com','superpages.com','manta.com','angieslist.com',
    'expertise.com','1800dentist.com','zocdoc.com','healthgrades.com',
    'vitals.com','ratemds.com','findlaw.com','avvo.com','justia.com',
    'buildzoom.com','porch.com','nextdoor.com','waze.com','tripadvisor.com',
}

JUNK_EMAILS = {'example.com','wixpress','sentry','wordpress','googleapis',
               'schema.org','cloudflare.com','w3.org','jquery.com'}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def http_get(url: str, timeout=8) -> tuple[str, str, int]:
    """Returns (body, final_url, status_code). Body empty on error."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        final = resp.geturl()
        body = resp.read(300_000).decode("utf-8", errors="replace")
        return body, final, resp.getcode()
    except Exception:
        return "", url, 0

def extract_emails(body: str) -> list[str]:
    # First try mailto links
    emails = re.findall(r'mailto:([a-zA-Z0-9_.+%-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,})', body)
    # Fallback: plain email pattern
    if not emails:
        emails = re.findall(r'\b([a-zA-Z0-9_.+%-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,})\b', body)
    cleaned = []
    for e in emails:
        e_lower = e.lower()
        if any(j in e_lower for j in JUNK_EMAILS): continue
        if e_lower.endswith(('.png', '.jpg', '.gif', '.svg', '.css', '.js')): continue
        if len(e) > 80: continue
        cleaned.append(e)
    return list(dict.fromkeys(cleaned))[:3]  # dedup, max 3

def find_contact_url(base_url: str, body: str) -> str | None:
    """Find a /contact or /about link in the page HTML."""
    parsed = urllib.parse.urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    for pattern in (r'href="(/contact[^"]*)"', r'href="(/about[^"]*)"',
                    r'href="(https?://[^"]*contact[^"]*)"'):
        m = re.search(pattern, body, re.I)
        if m:
            link = m.group(1)
            if link.startswith('http'):
                return link
            return root + link
    return None

def enrich_lead(row: dict) -> str | None:
    """Visit website and contact page; return email if found."""
    url = row.get('website', '')
    if not url.startswith('http'):
        return None

    domain = urllib.parse.urlparse(url).hostname or ''
    domain = domain.replace('www.', '')
    if any(d in domain for d in DIRECTORIES):
        return None

    # 1. Check homepage
    body, final_url, status = http_get(url)
    if body:
        emails = extract_emails(body)
        if emails:
            return emails[0]

        # 2. Try /contact page
        contact_url = find_contact_url(final_url, body)
        if contact_url:
            time.sleep(random.uniform(0.5, 1.2))
            cbody, _, _ = http_get(contact_url)
            if cbody:
                cemails = extract_emails(cbody)
                if cemails:
                    return cemails[0]

    return None

def run(limit: int = 60, dry_run: bool = False):
    log(f"OpenClaw Email Enricher starting (limit={limit}, dry_run={dry_run})")

    # Load CSV
    rows = []
    with open(LEADS_CSV) as f:
        rows = list(csv.DictReader(f))

    headers = list(rows[0].keys()) if rows else []

    # Find enrichable leads
    targets = []
    for i, r in enumerate(rows):
        if r.get('grade') not in ('F', 'D'): continue
        if r.get('email', '').strip(): continue
        url = r.get('website', '')
        if not url.startswith('http'): continue
        domain = (urllib.parse.urlparse(url).hostname or '').replace('www.', '')
        if any(d in domain for d in DIRECTORIES): continue
        targets.append((i, r))

    log(f"Found {len(targets)} enrichable leads (F/D, no email, real URL)")
    log(f"Processing up to {limit} leads...")

    enriched = 0
    for idx, (row_idx, row) in enumerate(targets[:limit]):
        biz = row.get('business_name', '')[:40]
        log(f"  [{idx+1}/{min(limit, len(targets))}] {biz}")

        email = enrich_lead(row)
        if email:
            log(f"    FOUND: {email}")
            if not dry_run:
                rows[row_idx]['email'] = email
            enriched += 1
        else:
            log(f"    not found")

        time.sleep(random.uniform(1.0, 2.5))

    log(f"\nEnrichment complete: {enriched}/{min(limit, len(targets))} emails found")

    if not dry_run and enriched > 0:
        with open(LEADS_CSV, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
            w.writeheader()
            w.writerows(rows)
        log(f"Updated {LEADS_CSV}")

        # Also update outreach_queue.csv if matching entries exist
        if OUTREACH_CSV.exists():
            orows = []
            with open(OUTREACH_CSV) as f:
                orows = list(csv.DictReader(f))
            oheaders = list(orows[0].keys()) if orows else []
            updated_emails = {r.get('business_name', ''): r.get('email', '') for r in rows if r.get('email')}
            changed = 0
            for or_ in orows:
                bname = or_.get('business_name', '')
                if bname in updated_emails and not or_.get('to_email', '').strip():
                    or_['to_email'] = updated_emails[bname]
                    changed += 1
            if changed:
                with open(OUTREACH_CSV, 'w', newline='') as f:
                    w = csv.DictWriter(f, fieldnames=oheaders, extrasaction='ignore')
                    w.writeheader()
                    w.writerows(orows)
                log(f"Updated {changed} outreach queue entries with emails")

    return enriched

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='OpenClaw Email Enricher')
    ap.add_argument('--limit', type=int, default=60, help='Max leads to process')
    ap.add_argument('--dry-run', action='store_true', help='Print only, do not write')
    args = ap.parse_args()
    found = run(limit=args.limit, dry_run=args.dry_run)
    print(f"\nResult: {found} emails found")
