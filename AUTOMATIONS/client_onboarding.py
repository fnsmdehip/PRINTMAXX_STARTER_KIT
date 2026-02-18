#!/usr/bin/env python3
"""Client onboarding automation. Converts a qualified lead into a full onboarding package."""

import argparse, csv, os, re, sys
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent
LEADS_CSV = BASE / "leads" / "qualified" / "HOT_LEADS_QUALIFIED.csv"
CLIENTS_DIR = BASE / "output" / "clients"
TRACKER_CSV = CLIENTS_DIR / "CLIENT_TRACKER.csv"
TIERS = {
    "starter":      {"label": "Starter",      "price": 500,  "pages": 5,  "extras": "5-page responsive website, contact form, Google Maps embed"},
    "professional": {"label": "Professional", "price": 1500, "pages": 10, "extras": "10-page site, scroll animations, SEO optimization, analytics, speed optimization"},
    "premium":      {"label": "Premium",      "price": 3000, "pages": 15, "extras": "Full package: 15+ pages, animations, SEO, ongoing monthly maintenance, priority support, A/B testing"},
}
TRACKER_FIELDS = ["client_id", "lead_id", "name", "slug", "industry", "city", "state", "tier", "price", "onboarded_at", "status"]

def load_leads():
    if not LEADS_CSV.exists():
        print(f"ERROR: leads CSV not found at {LEADS_CSV}"); sys.exit(1)
    with open(LEADS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower().strip())
    return re.sub(r"-+", "-", re.sub(r"[\s_]+", "-", s)).strip("-")[:60]

def fuzzy_match(leads, query):
    q = query.lower()
    return [l for l in leads if q in l.get("name", "").lower() or q in l.get("category", "").lower()
            or q in l.get("city", "").lower() or q in l.get("domain", "").lower()]

def find_by_id(leads, lead_id):
    return next((l for l in leads if l.get("id", "").startswith(lead_id)), None)

def pain_summary(raw):
    if not raw:
        return "No specific issues detected"
    issues = []
    if "NO_SSL" in raw: issues.append("Missing SSL certificate")
    if "NO_MOBILE_VIEWPORT" in raw: issues.append("Not mobile-friendly")
    if "SLOW_LOAD" in raw: issues.append("Slow page load")
    if "flash_content" in raw: issues.append("Uses outdated Flash")
    if "table_layout" in raw: issues.append("Outdated table-based layout")
    if "font_tags" in raw: issues.append("Legacy font tags")
    seo_missing = raw.count("SEO_MISSING")
    if seo_missing > 0: issues.append(f"{seo_missing} SEO elements missing")
    aio_missing = raw.count("AIO_MISSING")
    if aio_missing > 0: issues.append(f"{aio_missing} AI-optimization elements missing")
    return "; ".join(issues) if issues else "Minor issues only"

def gen_welcome_email(lead, tier_info):
    name = lead["name"]
    city = lead.get("city", "")
    return f"""# Welcome to Your New Web Presence

Hi {name} team,

Thanks for choosing us for your website redesign. We are genuinely excited to work with you.

Here is what happens next:

1. **This week**: We review the project brief (attached) and schedule a 30-minute kickoff call.
2. **Within 48 hours of kickoff**: You receive a design mockup for your homepage.
3. **Week 2-3**: Full site build with your feedback at every step.
4. **Week 4**: Launch day. Your new site goes live.

Your package: **{tier_info['label']}** (${tier_info['price']:,})
Includes: {tier_info['extras']}

What we need from you right away (see checklist.md):
- Your logo files (PNG or SVG)
- Brand colors (hex codes if you have them)
- 5-10 photos of your {lead.get('category','business').replace('_',' ')} in {city}
- Any specific text you want on the site

Questions? Reply to this email. We typically respond within 2 hours during business days.

Looking forward to building something great for {name}.

Best,
PRINTMAXX Web Studio
"""

def gen_project_brief(lead, tier_info):
    score = lead.get("total_score", "N/A")
    design = lead.get("design_score", "N/A")
    seo = lead.get("seo_score", "N/A")
    pain = pain_summary(lead.get("pain_signals", ""))
    domain = lead.get("domain", "N/A")
    industry = lead.get("category", "unknown").replace("_", " ").title()
    return f"""# Project Brief: {lead['name']}

## Client Information
| Field | Value |
|-------|-------|
| Business | {lead['name']} |
| Industry | {industry} |
| Location | {lead.get('city','')}, {lead.get('state','')} {lead.get('zip','')} |
| Phone | {lead.get('phone','N/A')} |
| Email | {lead.get('email','N/A')} |
| Current Site | {lead.get('website','N/A')} |
| Domain | {domain} |

## Current Website Audit
| Metric | Score |
|--------|-------|
| Overall | {score}/100 |
| Design | {design}/25 |
| SEO | {seo}/20 |
| Mobile Friendly | {lead.get('mobile_friendly','N/A')} |
| SSL Valid | {lead.get('ssl_valid','N/A')} |
| Load Time | {lead.get('response_time_ms','N/A')}ms |

## Issues Identified
{pain}

## Scope of Work
- **Package**: {tier_info['label']} (${tier_info['price']:,})
- **Pages**: {tier_info['pages']}
- **Deliverables**: {tier_info['extras']}
- **Demo Reference**: {lead.get('demo_url','N/A')}

## Competitor Landscape
Based on {lead.get('city','local')} {industry.lower()} businesses, most competitors have modern, mobile-first sites with online booking. This redesign will bring {lead['name']} to parity and beyond.

## Goals
1. Modern, mobile-responsive design that builds trust instantly
2. SEO-optimized pages to rank for "{industry.lower()} in {lead.get('city','')}"
3. Clear calls-to-action (call, book online, get directions)
4. Fast load times (under 2 seconds)
5. SSL security and accessibility compliance
"""

def gen_timeline(lead, tier_info):
    start = datetime.now()
    weeks = []
    for i, (title, tasks) in enumerate([
        ("Discovery & Planning", ["Kickoff call (30 min)", "Review brand assets received", "Competitive analysis of local market", "Wireframe homepage + key pages", "Client approval on wireframes"]),
        ("Design & Content", ["Full homepage design mockup", "Interior page designs", "Mobile responsive layouts", "Content integration (text + photos)", "Client review and revision round 1"]),
        ("Development & Build", ["Convert designs to live code", "Contact forms and integrations", "Speed optimization", "SEO setup (meta tags, schema, sitemap)", "Cross-browser and mobile testing"]),
        ("Launch & Handoff", ["Final client review", "Domain DNS configuration", "SSL certificate installation", "Go live", "Training session (15 min): how to request updates", "Post-launch checkup (Day 7)"]),
    ]):
        w_start = start + timedelta(weeks=i)
        w_end = w_start + timedelta(days=4)
        task_list = "\n".join(f"- [ ] {t}" for t in tasks)
        weeks.append(f"## Week {i+1}: {title}\n**{w_start.strftime('%b %d')} - {w_end.strftime('%b %d, %Y')}**\n\n{task_list}\n")
    return f"# Project Timeline: {lead['name']}\n\nPackage: {tier_info['label']} | Start: {start.strftime('%B %d, %Y')}\n\n" + "\n".join(weeks)

def gen_invoice(lead, tier_info):
    today = datetime.now()
    due = today + timedelta(days=7)
    inv_num = f"INV-{today.strftime('%Y%m%d')}-{slugify(lead['name'])[:10].upper()}"
    deposit = tier_info["price"] // 2
    return f"""# Invoice

**Invoice #**: {inv_num}
**Date**: {today.strftime('%B %d, %Y')}
**Due**: {due.strftime('%B %d, %Y')}

## Bill To
{lead['name']}
{lead.get('address','')}
{lead.get('city','')}, {lead.get('state','')} {lead.get('zip','')}

## Services

| Item | Description | Amount |
|------|-------------|--------|
| {tier_info['label']} Website Package | {tier_info['extras']} | ${tier_info['price']:,}.00 |

**Total: ${tier_info['price']:,}.00**

## Payment Schedule
| Milestone | Amount | Due |
|-----------|--------|-----|
| Deposit (50%) | ${deposit:,}.00 | {due.strftime('%B %d, %Y')} |
| Final (50%) | ${tier_info['price'] - deposit:,}.00 | Upon launch |

## Payment Methods
- Stripe invoice (link will be sent separately)
- Bank transfer (details on request)

Terms: Net 7. Work begins upon receipt of deposit.
"""

def gen_checklist(lead):
    industry = lead.get("category", "business").replace("_", " ")
    return f"""# Client Checklist: {lead['name']}

Please provide the following items so we can begin. Email them to us or share via Google Drive.

## Required (before we start design)
- [ ] Logo file (PNG, SVG, or AI format)
- [ ] Brand colors (hex codes, e.g. #1A2B3C) or say "use your judgment"
- [ ] 5-10 photos of your {industry} (interior, exterior, team, equipment)
- [ ] List of services you offer with brief descriptions
- [ ] Business hours
- [ ] Preferred contact method for customers (phone, email, form, booking link)

## Required (before launch)
- [ ] Domain registrar login (GoDaddy, Namecheap, etc.) OR grant us DNS access
- [ ] Google Business Profile access (for local SEO integration)
- [ ] Any existing analytics accounts (Google Analytics ID if you have one)

## Optional (makes the site better)
- [ ] Testimonials or reviews you want featured
- [ ] Staff bios and headshots
- [ ] Insurance/payment types accepted
- [ ] "About Us" story or founding details
- [ ] Social media links (Facebook, Instagram, Yelp, etc.)
- [ ] Any competitor websites you like the look of

## Timeline Reminder
The sooner we receive these items, the sooner we launch. Typical turnaround: 4 weeks from deposit.
"""

def load_tracker():
    if not TRACKER_CSV.exists():
        return []
    with open(TRACKER_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_to_tracker(entry):
    CLIENTS_DIR.mkdir(parents=True, exist_ok=True)
    exists = TRACKER_CSV.exists()
    with open(TRACKER_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
        if not exists:
            w.writeheader()
        w.writerow(entry)

def onboard(lead, tier_key, dry_run=False):
    tier_info = TIERS[tier_key]
    slug = slugify(lead["name"])
    out_dir = CLIENTS_DIR / slug

    files = {
        "welcome_email.md": gen_welcome_email(lead, tier_info),
        "project_brief.md": gen_project_brief(lead, tier_info),
        "timeline.md": gen_timeline(lead, tier_info),
        "invoice.md": gen_invoice(lead, tier_info),
        "checklist.md": gen_checklist(lead),
    }

    if dry_run:
        print(f"\n[DRY RUN] Would onboard: {lead['name']}")
        print(f"  Industry : {lead.get('category','?').replace('_',' ').title()}")
        print(f"  Location : {lead.get('city','')}, {lead.get('state','')}")
        print(f"  Score    : {lead.get('total_score','?')}/100")
        print(f"  Tier     : {tier_info['label']} (${tier_info['price']:,})")
        print(f"  Output   : {out_dir}/")
        print(f"  Files    :")
        for name, content in files.items():
            print(f"    - {name} ({len(content):,} chars)")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (out_dir / name).write_text(content, encoding="utf-8")

    tracker_entry = {
        "client_id": f"CLT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "lead_id": lead.get("id", ""),
        "name": lead["name"],
        "slug": slug,
        "industry": lead.get("category", ""),
        "city": lead.get("city", ""),
        "state": lead.get("state", ""),
        "tier": tier_key,
        "price": tier_info["price"],
        "onboarded_at": datetime.now().isoformat(),
        "status": "onboarded",
    }
    save_to_tracker(tracker_entry)
    print(f"\nOnboarded: {lead['name']}")
    print(f"  Package written to: {out_dir}/")
    for name in files:
        print(f"    - {name}")
    print(f"  Tracked in: {TRACKER_CSV}")

def list_clients():
    rows = load_tracker()
    if not rows:
        print("No clients onboarded yet.")
        return
    print(f"\n{'ID':<26} {'Name':<35} {'Tier':<14} {'City':<18} {'Date'}")
    print("-" * 110)
    for r in rows:
        dt = r.get("onboarded_at", "")[:10]
        price = f"${int(r.get('price',0)):,}"
        print(f"{r.get('client_id',''):<26} {r.get('name',''):<35} {r.get('tier',''):<7} {price:<7} {r.get('city',''):<18} {dt}")
    print(f"\nTotal: {len(rows)} client(s)")

def main():
    p = argparse.ArgumentParser(description="Client onboarding package generator")
    p.add_argument("--from-lead", metavar="ID", help="Lead ID (or prefix) from HOT_LEADS_QUALIFIED.csv")
    p.add_argument("--search", metavar="QUERY", help="Fuzzy search leads by name/city/industry")
    p.add_argument("--tier", choices=TIERS.keys(), default="professional", help="Pricing tier (default: professional)")
    p.add_argument("--list-clients", action="store_true", help="Show all onboarded clients")
    p.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = p.parse_args()

    if args.list_clients:
        list_clients()
        return

    if not args.from_lead and not args.search:
        p.print_help()
        print("\nExamples:")
        print('  python3 client_onboarding.py --search "dental" --dry-run')
        print('  python3 client_onboarding.py --from-lead 261eec26 --tier starter')
        print('  python3 client_onboarding.py --list-clients')
        return
    leads = load_leads()
    if args.from_lead:
        lead = find_by_id(leads, args.from_lead)
        if not lead:
            print(f"No lead found matching ID prefix: {args.from_lead}")
            sys.exit(1)
        onboard(lead, args.tier, args.dry_run); return
    if args.search:
        matches = fuzzy_match(leads, args.search)
        if not matches:
            print(f'No leads matching "{args.search}"')
            sys.exit(1)
        print(f'\nFound {len(matches)} lead(s) matching "{args.search}":\n')
        print(f"  {'#':<4} {'Name':<40} {'Industry':<20} {'City':<16} {'Score':<6} {'ID (prefix)'}")
        print(f"  {'-'*4} {'-'*40} {'-'*20} {'-'*16} {'-'*6} {'-'*12}")
        for i, l in enumerate(matches[:20], 1):
            print(f"  {i:<4} {l.get('name','')[:39]:<40} {l.get('category',''):<20} {l.get('city',''):<16} {l.get('total_score','?'):<6} {l.get('id','')[:8]}")
        if args.dry_run or len(matches) > 1:
            if args.dry_run and len(matches) == 1:
                onboard(matches[0], args.tier, dry_run=True)
            elif args.dry_run:
                print(f"\n[DRY RUN] Previewing first match:")
                onboard(matches[0], args.tier, dry_run=True)
            else:
                print(f"\nMultiple matches. Use --from-lead <ID prefix> to select one, or add --dry-run to preview first match.")
        else:
            onboard(matches[0], args.tier, args.dry_run)


if __name__ == "__main__":
    main()
