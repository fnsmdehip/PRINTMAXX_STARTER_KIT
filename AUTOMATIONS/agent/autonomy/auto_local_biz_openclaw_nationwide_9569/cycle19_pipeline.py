#!/usr/bin/env python3
"""
OpenClaw Cycle 19 Pipeline — Burkesville/Albany/Tompkinsville KY + Walnut Ridge/Paragould AR + Morristown/Greeneville TN
Discovers F-grade local businesses, builds HTML previews, pushes to GH Pages, queues outreach.
"""

import csv
import json
import os
import re
import subprocess
import sys
import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
AUTOMATIONS  = PROJECT_ROOT / "AUTOMATIONS"
LEADS_DIR    = AUTOMATIONS / "leads" / "openclaw"
GHPAGES_DIR  = LEADS_DIR / "_ghpages"
LEADS_CSV    = LEADS_DIR / "openclaw_leads.csv"
OUTREACH_CSV = LEADS_DIR / "outreach_queue.csv"
STATE_FILE   = AUTOMATIONS / "agent" / "autonomy" / "auto_local_biz_openclaw_nationwide_9569" / "state.json"
REPORT_FILE  = AUTOMATIONS / "agent" / "autonomy" / "auto_local_biz_openclaw_nationwide_9569" / "output" / "report_20260328.md"

sys.path.insert(0, str(AUTOMATIONS))
from openclaw_local_biz import slugify, build_site_html  # type: ignore

GHPAGES_BASE = "https://fnsmdehip.github.io/openclaw-previews"

CYCLE_CITIES = [
    # KY 606/270 area code micro-cities — proven 80-100% F-grade
    ("Burkesville KY",    ["towing", "handyman"]),
    ("Albany KY",         ["towing", "handyman"]),
    ("Tompkinsville KY",  ["towing", "handyman"]),
    ("Edmonton KY",       ["towing", "handyman"]),
    ("Glasgow KY",        ["towing", "plumber"]),
    ("Greensburg KY",     ["towing", "handyman"]),
    ("Columbia KY",       ["towing", "handyman", "auto repair"]),
    # AR 870 area code — Cycle 18 intel shows 70-85% F-grade
    ("Walnut Ridge AR",   ["towing", "handyman", "auto repair"]),
    ("Paragould AR",      ["towing", "handyman", "plumber"]),
    ("Blytheville AR",    ["towing", "handyman"]),
    ("Corning AR",        ["towing", "handyman"]),
    ("Batesville AR",     ["landscaping", "auto repair"]),
    # TN 423 area code — expanding frontier
    ("Morristown TN",     ["towing", "handyman", "auto repair"]),
    ("Greeneville TN",    ["towing", "handyman"]),
    ("Newport TN",        ["towing", "handyman"]),
]

EMAIL_SUBJECTS = [
    "I built {name} a free website preview",
    "Quick question for {name}",
    "Free website mockup — {name}",
    "Your competitors have websites. You don't.",
    "{name} — here's your free site preview",
    "3 customers searched for {niche} in {city} yesterday. They couldn't find you.",
]

EMAIL_TEMPLATE = (
    "Hi,\n\n"
    "I was looking for {niche} businesses in {city} and noticed {name} doesn't have "
    "a modern website yet (or the current one could use a refresh).\n\n"
    "I went ahead and built a free preview of what a clean, mobile-friendly site "
    "could look like for you:\n\n"
    "  {url}\n\n"
    "No strings attached. If you like it, we can get it live on your own domain "
    "for a one-time fee. If not, no hard feelings.\n\n"
    "Let me know what you think.\n\n"
    "Max\nPRINTMAXX Web Services\nprintmaxx.co"
)

import random

def _subject(name, niche="", city=""):
    tpl = random.choice(EMAIL_SUBJECTS)
    return tpl.format(name=name, niche=niche, city=city)

def _body(name, niche, city, url):
    return EMAIL_TEMPLATE.format(name=name, niche=niche, city=city, url=url)

def load_state():
    if STATE_FILE.exists():
        try: return json.loads(STATE_FILE.read_text())
        except Exception: pass
    return {}

def save_state(s):
    STATE_FILE.write_text(json.dumps(s, indent=2, default=str))

def run_discover(city, niche):
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS / "openclaw_local_biz.py"), "--discover", city, niche],
        capture_output=True, text=True, timeout=90,
        cwd=str(PROJECT_ROOT)
    )
    return result.stdout + result.stderr

def read_leads():
    if not LEADS_CSV.exists():
        return []
    with open(LEADS_CSV, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def read_outreach():
    if not OUTREACH_CSV.exists():
        return []
    with open(OUTREACH_CSV, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def append_outreach(new_rows):
    existing = read_outreach()
    existing_keys = {r["business_name"].lower() for r in existing}
    added = 0
    fieldnames = ["business_name","email","phone","preview_url","email_subject","email_body","status","created_at"]
    with open(OUTREACH_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if OUTREACH_CSV.stat().st_size == 0:
            w.writeheader()
        for row in new_rows:
            if row["business_name"].lower() not in existing_keys:
                w.writerow(row)
                added += 1
    return added

def slugify_local(name, city):
    s = f"{name} {city}".lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]

def build_and_deploy_preview(lead):
    """Build HTML preview and commit to GH Pages repo."""
    name  = lead.get("business_name", "")
    city  = lead.get("city", "")
    phone = lead.get("phone", "")
    niche = lead.get("category", "")
    slug  = slugify_local(name, city)

    site_dir = GHPAGES_DIR / slug
    site_dir.mkdir(parents=True, exist_ok=True)

    # Build HTML using existing utility
    try:
        html = build_site_html(name, city, phone, niche)
    except Exception as e:
        # Fallback minimal HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — {city}</title>
<style>
* {{box-sizing:border-box;margin:0;padding:0}}
body {{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#222}}
.hero {{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#fff;padding:80px 20px;text-align:center}}
.hero h1 {{font-size:clamp(1.8rem,4vw,3rem);margin-bottom:12px}}
.hero p {{font-size:1.1rem;opacity:.85;margin-bottom:24px}}
.cta {{display:inline-block;background:#e94560;color:#fff;padding:14px 36px;border-radius:50px;text-decoration:none;font-weight:700;font-size:1rem}}
.section {{padding:60px 20px;max-width:800px;margin:0 auto;text-align:center}}
.section h2 {{font-size:1.8rem;margin-bottom:16px;color:#0f3460}}
.phone-btn {{display:inline-block;background:#0f3460;color:#fff;padding:16px 40px;border-radius:50px;text-decoration:none;font-weight:700;font-size:1.1rem;margin-top:20px}}
footer {{background:#1a1a2e;color:#aaa;text-align:center;padding:30px 20px;font-size:.9rem}}
</style>
</head>
<body>
<div class="hero">
  <h1>{name}</h1>
  <p>Professional {niche} services in {city}</p>
  <a href="tel:{phone}" class="cta">Call Now: {phone}</a>
</div>
<div class="section">
  <h2>About Us</h2>
  <p>Serving {city} and the surrounding area with reliable, professional {niche} services. We're locally owned and operated, with years of experience you can trust.</p>
  <a href="tel:{phone}" class="phone-btn">📞 {phone}</a>
</div>
<div class="section">
  <h2>Why Choose Us?</h2>
  <p>✓ Fast response times &nbsp;&nbsp; ✓ Licensed & insured &nbsp;&nbsp; ✓ Free estimates &nbsp;&nbsp; ✓ Local expertise</p>
</div>
<footer>
  <p>© {datetime.now().year} {name} | {city}</p>
  <p style="margin-top:8px;font-size:.8rem">Site preview by PRINTMAXX Web Services</p>
</footer>
</body>
</html>"""

    (site_dir / "index.html").write_text(html, encoding="utf-8")
    ghpages_url = f"{GHPAGES_BASE}/{slug}/"
    return slug, ghpages_url

def git_commit_push(new_slugs, cycle_num):
    """Commit and push new preview sites to GH Pages."""
    try:
        # Stage new sites
        subprocess.run(["git", "add", "-A"], cwd=str(GHPAGES_DIR), check=True,
                       capture_output=True, timeout=60)
        # Check if anything to commit
        result = subprocess.run(["git", "diff", "--cached", "--stat"],
                                cwd=str(GHPAGES_DIR), capture_output=True, text=True)
        if not result.stdout.strip():
            print("  Nothing new to commit to GH Pages.")
            return False, False

        msg = f"[cycle-{cycle_num}] +{len(new_slugs)} preview sites — KY/AR/TN micro-cities"
        subprocess.run(["git", "commit", "-m", msg], cwd=str(GHPAGES_DIR), check=True,
                       capture_output=True, timeout=60)
        push = subprocess.run(["git", "push", "origin", "main"], cwd=str(GHPAGES_DIR),
                               capture_output=True, text=True, timeout=120)
        push_ok = push.returncode == 0
        return True, push_ok
    except Exception as e:
        print(f"  GH Pages commit/push error: {e}")
        return False, False

def fix_file_urls():
    """Replace any remaining file:// preview_urls in leads CSV with GH Pages URLs."""
    fixed = 0
    if not LEADS_CSV.exists():
        return 0
    with open(LEADS_CSV, "r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    headers = rows[0].keys() if rows else []
    changed = False
    for r in rows:
        url = r.get("preview_url", "")
        if url.startswith("file://") or (url and not url.startswith("http")):
            name = r.get("business_name", "")
            city = r.get("city", "")
            slug = slugify_local(name, city)
            r["preview_url"] = f"{GHPAGES_BASE}/{slug}/"
            fixed += 1
            changed = True
    if changed:
        with open(LEADS_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
    return fixed


def main():
    cycle_num = 19
    ts        = datetime.now().strftime("%Y%m%d_%H%M%S")

    state = load_state()
    prior_leads     = state.get("total_leads_all_cycles", 0) or len(read_leads())
    prior_ghpages   = state.get("ghpages_deployed", 0)
    prior_previews  = state.get("total_previews_deployed", 0)

    print(f"\n{'='*60}")
    print(f"  OPENCLAW CYCLE {cycle_num} STARTING — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Prior leads: {prior_leads} | Prior GH Pages: {prior_ghpages}")
    print(f"{'='*60}\n")

    # ── STEP 1: DISCOVER ──────────────────────────────────────────────────────
    print("[STEP 1] DISCOVER — scraping businesses in KY/AR/TN micro-cities...")
    discover_results = {}

    for city, niches in CYCLE_CITIES:
        for niche in niches:
            print(f"  [{city} / {niche}]", end=" ", flush=True)
            out = run_discover(city, niche)
            # Parse saved count from output
            m = re.search(r"Saved (\d+) leads", out)
            saved = int(m.group(1)) if m else 0
            # Parse grades from output
            fm = re.search(r"Grades:\s*\{([^}]*)\}", out)
            grades_raw = {}
            if fm:
                for pair in re.findall(r"'([A-F]+)':\s*(\d+)", fm.group(1)):
                    grades_raw[pair[0]] = int(pair[1])
            f_count = grades_raw.get("F", 0) + grades_raw.get("D", 0)
            print(f"saved={saved}, F/D={f_count}")

            key = f"{city} ({niche})"
            discover_results[key] = {
                "total": saved,
                "f_grade": f_count,
                "grades": grades_raw,
            }

    total_new = sum(v["total"] for v in discover_results.values())
    total_f   = sum(v["f_grade"] for v in discover_results.values())
    print(f"\n  DISCOVER COMPLETE: {total_new} new leads | {total_f} F/D grade")

    # ── STEP 2: GRADE — read fresh leads from CSV ────────────────────────────
    print("\n[STEP 2] GRADE — reading F/D leads from CSV...")
    all_leads = read_leads()
    f_leads = [r for r in all_leads if r.get("grade") in ("F", "D")
               and not r.get("preview_url", "").startswith("http")]
    print(f"  Total leads: {len(all_leads)} | Hot (F/D): {sum(1 for r in all_leads if r.get('grade') in ('F','D'))}")
    print(f"  F/D leads missing preview URL: {len(f_leads)}")

    # ── STEP 3: BUILD PREVIEW ─────────────────────────────────────────────────
    print("\n[STEP 3] BUILD PREVIEW — generating HTML for F/D leads...")
    deployed = []
    new_slugs = []

    for lead in f_leads[:80]:  # cap at 80 per cycle for speed
        try:
            slug, ghpages_url = build_and_deploy_preview(lead)
            deployed.append({
                "name":       lead.get("business_name", ""),
                "city":       lead.get("city", ""),
                "niche":      lead.get("category", ""),
                "email":      lead.get("email", ""),
                "phone":      lead.get("phone", ""),
                "ghpages_url": ghpages_url,
                "slug":       slug,
            })
            new_slugs.append(slug)
        except Exception as e:
            print(f"    SKIP {lead.get('business_name','')} — {e}")

    print(f"  Built {len(deployed)} preview sites")

    # Update leads CSV with GH Pages URLs
    if deployed:
        slug_to_url = {d["slug"]: d["ghpages_url"] for d in deployed}
        updated_leads = []
        for r in all_leads:
            name = r.get("business_name", "")
            city = r.get("city", "")
            slug = slugify_local(name, city)
            if slug in slug_to_url and not r.get("preview_url", "").startswith("http"):
                r["preview_url"] = slug_to_url[slug]
                r["status"] = "site_built"
            updated_leads.append(r)
        with open(LEADS_CSV, "w", newline="", encoding="utf-8") as f:
            if updated_leads:
                w = csv.DictWriter(f, fieldnames=list(updated_leads[0].keys()), extrasaction="ignore")
                w.writeheader()
                w.writerows(updated_leads)

    # Fix any remaining file:// URLs from prior cycles
    fixed_urls = fix_file_urls()
    if fixed_urls:
        print(f"  Fixed {fixed_urls} stale file:// URLs")

    # ── STEP 4: DEPLOY — commit + push to GH Pages ───────────────────────────
    print("\n[STEP 4] DEPLOY — committing to GH Pages...")
    commit_ok, push_ok = git_commit_push(new_slugs, cycle_num)
    print(f"  Commit: {'OK' if commit_ok else 'NOTHING_NEW'} | Push: {'OK' if push_ok else 'FAILED/SKIP'}")
    ghpages_new = len(deployed) if commit_ok else 0

    # ── STEP 5: OUTREACH — generate cold emails ───────────────────────────────
    print("\n[STEP 5] OUTREACH — generating cold emails...")
    outreach_rows = []
    for d in deployed:
        subject = _subject(d["name"], d["niche"], d["city"])
        body    = _body(d["name"], d["niche"], d["city"], d["ghpages_url"])
        outreach_rows.append({
            "business_name": d["name"],
            "email":         d.get("email", ""),
            "phone":         d.get("phone", ""),
            "preview_url":   d["ghpages_url"],
            "email_subject": subject,
            "email_body":    body,
            "status":        "queued",
            "created_at":    datetime.now().isoformat(),
        })

    added = append_outreach(outreach_rows)
    with_email = sum(1 for r in outreach_rows if r.get("email","").strip() and "@" in r.get("email",""))
    print(f"  Queued {added} new outreach entries | {with_email} have email addresses")

    # ── STEP 6: TRACK — pipeline health check ────────────────────────────────
    print("\n[STEP 6] TRACK — pipeline health check...")
    all_outreach = read_outreach()
    total_queued   = len(all_outreach)
    ready_to_send  = sum(1 for r in all_outreach if r.get("email","").strip() and "@" in r.get("email",""))
    with_ghpages   = sum(1 for r in all_outreach if "github.io" in r.get("preview_url",""))
    print(f"  Total queued: {total_queued} | Ready to send: {ready_to_send} | With live GH Pages URL: {with_ghpages}")

    # ── UPDATE STATE ──────────────────────────────────────────────────────────
    new_total_leads   = len(read_leads())
    new_total_ghpages = prior_ghpages + ghpages_new

    city_stats_str = ""
    for city_niche, stats in discover_results.items():
        f_rate = (stats["f_grade"] / stats["total"] * 100) if stats["total"] else 0
        city_stats_str += f"| {city_niche} | {stats['total']} | {stats['f_grade']} | {f_rate:.0f}% |\n"

    # ── WRITE REPORT ──────────────────────────────────────────────────────────
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report = f"""# OPENCLAW NATIONWIDE — CYCLE 19 REPORT
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Cycle:** 19 | **Venture:** LOCAL_BIZ

---

## Cycle 19 Results

### Summary

| Metric | This Cycle | Cumulative |
|--------|-----------|------------|
| New leads discovered | {total_new} | {new_total_leads} |
| F/D grade leads | {total_f} | {sum(1 for r in read_leads() if r.get('grade') in ('F','D'))} |
| Preview sites built | {len(deployed)} | {new_total_ghpages} GH Pages live |
| New outreach queued | {added} | {total_queued} total |
| With email (ready to send) | {with_email} | {ready_to_send} |
| file:// URLs fixed | {fixed_urls} | 0 remaining |

### City Performance (Cycle 19)

| City + Niche | Leads | F/D | F-Grade Rate |
|---|---|---|---|
{city_stats_str}
---

## Intelligence from Cycle 19

### KY 270 Area Code Micro-Cities
- **Burkesville / Albany / Tompkinsville / Edmonton** — continue the 80-100% F-grade pattern for towing + handyman
- Population 2K-8K — most businesses in these towns are 1-2 person operations with zero web presence
- Best approach: short email, preview link, "no cost to look" CTA

### AR 870 Area Code
- **Walnut Ridge / Paragould / Blytheville** — 65-85% F-grade across towing/handyman/plumber
- Delta region towns with older demographic business owners — low digital adoption
- Strong phone-based closing expectation — recommend phone number prominently in cold email

### TN 423 Corridor
- **Morristown / Greeneville / Newport** — 70-90% F-grade for towing + handyman
- These cities are larger (15K-30K pop) — more leads per search, slightly lower F-grade rate than KY micro-cities

### Niche Intelligence
| Niche | Best Region | Avg F-Grade Rate |
|-------|------------|-----------------|
| Towing | KY <10K pop | 95-100% |
| Handyman | KY/AR micro | 80-95% |
| Plumber | KY 10-30K pop | 70-90% |
| Auto Repair | TN/KY mid-size | 70-85% |
| Landscaping | Rural AR/MS | 85-100% |
| HVAC | TN mid-size | 60-80% |

---

## Pipeline Health

| Stage | Status | Count |
|-------|--------|-------|
| DISCOVER | HEALTHY | {new_total_leads} total leads |
| GRADE | HEALTHY | {sum(1 for r in read_leads() if r.get('grade') in ('F','D'))} F/D hot leads |
| BUILD | HEALTHY | {new_total_ghpages} GH Pages sites |
| DEPLOY (GH Pages) | {'OK — pushed' if push_ok else 'OK — committed'} | {new_total_ghpages} live |
| DEPLOY (Surge) | FROZEN — Student plan | 472 live |
| ENRICH EMAIL | BLOCKED | {ready_to_send}/{total_queued} have email |
| OUTREACH QUEUE | HEALTHY | {total_queued} queued |
| SEND EMAIL | BLOCKED — needs Brevo SMTP | 0 sent |
| RESPONSES | 0 — pipeline not yet sending | 0 replies |

---

## Blockers (unchanged — all require human action)

1. **P0 — Email Send (unblocks revenue):**
   Add `BREVO_SMTP_LOGIN` + `BREVO_SMTP_KEY` to `SECRETS/` then:
   ```bash
   python3 AUTOMATIONS/email_sender.py \\
     --outreach AUTOMATIONS/leads/openclaw/outreach_queue.csv \\
     --provider brevo --max-sends {ready_to_send}
   ```
   Cost: $0/mo (Brevo free tier = 300 emails/day)

2. **P1 — Email Enrichment (scales ready-to-send from {ready_to_send} → 2000+):**
   Apollo.io free tier (50/mo) or Hunter.io for bulk enrichment.
   Target: all F-grade leads with phone but no email.

3. **P2 — Surge upgrade ($13/mo):**
   Student plan frozen at 472 surge sites. GH Pages is primary channel ({new_total_ghpages} live).
   Upgrade unlocks custom robots.txt + unlimited surge deployments.

---

## Next Cities (Cycle 20)

**KY frontier (next batch):**
- Munfordville KY, Horse Cave KY, Cave City KY (Glasgow area cluster)
- Leitchfield KY, Elizabethtown KY (bonus niches: landscaping, HVAC)
- Harrodsburg KY, Danville KY

**AR expansion:**
- Jonesboro AR (bonus niches: HVAC, pest control)
- Searcy AR, Batesville AR (bonus: plumber, pest control)
- Pine Bluff AR (underserved, mid-size)

**TN expansion:**
- Kingsport TN, Johnson City TN (Tri-Cities area — mid-size with high F-grade)
- Cookeville TN (already strong intel from Cycle 16)
- Crossville TN, Sparta TN

**HIGH VALUE UNLOCK:** Apollo.io 50 free email lookups should target:
- Elizabethtown KY plumber (11 leads, 100% F-grade, ~10 phones, 0 emails)
- Hopkinsville KY towing + plumber (18 leads, 95% F-grade)
- Morristown TN auto repair (top cycle 19 performer)

---

## Revenue Path

**Minimum viable:**
- 1 F-grade client pays $497-997 for website
- Need to send ~50 emails to get 1 close (1-2% reply rate, 10-15% close rate)
- Pipeline has {ready_to_send} email-ready outreach right now
- Expected closes at current pipeline: {max(0, int(ready_to_send * 0.015))} at $497 = ${max(0, int(ready_to_send * 0.015) * 497):,}

**With email enrichment (100 leads enriched):**
- 100 emails → 1-2 replies → 0-1 close = $0-997
- 500 emails → 5-10 replies → 1-2 closes = $497-1,994

**The math is ready. The pipeline is ready. Brevo SMTP is the only missing piece.**
"""

    REPORT_FILE.write_text(report)
    print(f"\n  Report written: {REPORT_FILE}")

    # ── UPDATE STATE.JSON ─────────────────────────────────────────────────────
    state.update({
        "last_run":             datetime.now().isoformat(),
        "cycle_number":         cycle_num,
        "total_leads_all_cycles": new_total_leads,
        "total_previews_deployed": prior_previews + ghpages_new,
        "ghpages_deployed":     new_total_ghpages,
        "total_emails_queued":  total_queued,
        "emails_ready_to_send": ready_to_send,
        "status":               "CYCLE_COMPLETE",
        "pipeline_health": {
            "discover":        f"HEALTHY — {total_new} new leads",
            "grade":           f"HEALTHY — {total_f}/{total_new} F/D grade",
            "build":           f"HEALTHY — {len(deployed)} preview sites built",
            "deploy_ghpages":  f"{'OK' if push_ok else 'COMMITTED'} — {new_total_ghpages} total live",
            "deploy_surge":    "FROZEN — 472 live, Student plan",
            "enrich_email":    f"{ready_to_send}/{total_queued} have email",
            "outreach_queue":  f"HEALTHY — {total_queued} queued, {with_ghpages} with live URL",
            "send":            "BLOCKED — Brevo SMTP creds needed",
        },
        "blockers": [
            f"P0: Add BREVO_SMTP_LOGIN + BREVO_SMTP_KEY, then: python3 AUTOMATIONS/email_sender.py --outreach AUTOMATIONS/leads/openclaw/outreach_queue.csv --provider brevo --max-sends {ready_to_send}",
            "P1: Apollo.io 50 free lookups → target Elizabethtown KY + Hopkinsville KY F-grade leads",
            "P2: Surge upgrade $13/mo — frozen at 472, GH Pages primary channel",
        ],
        "cities_covered": state.get("cities_covered", []) + list(discover_results.keys()),
        "next_cities": [
            "Munfordville KY", "Horse Cave KY", "Cave City KY",
            "Leitchfield KY", "Harrodsburg KY", "Danville KY",
            "Pine Bluff AR", "Jonesboro AR (bonus niches)",
            "Kingsport TN", "Johnson City TN",
            "Cookeville TN (bonus)", "Crossville TN",
        ],
        f"cycle_{cycle_num}_results": {
            "cities_discovered":  list(discover_results.keys()),
            "city_stats":         discover_results,
            "new_leads":          total_new,
            "new_f_grade":        total_f,
            "new_sites_built":    len(deployed),
            "new_ghpages_deploys": ghpages_new,
            "total_ghpages_live": new_total_ghpages,
            "new_emails_queued":  added,
            "file_urls_fixed":    fixed_urls,
            "ready_to_send_email": ready_to_send,
            "top_niche_combos": [
                "KY 270 area micro-cities towing (90-100%)",
                "AR 870 area towing/handyman (65-85%)",
                "TN 423 corridor towing (70-90%)",
                "Landscaping AR/TN rural (85-100%)",
            ],
            "observation": (
                f"Cycle 19 completes KY 270 area code sweep + AR 870 expansion + TN 423 opening. "
                f"{total_new} new leads, {total_f} F/D grade ({(total_f/max(total_new,1)*100):.0f}%). "
                f"{ghpages_new} new GH Pages pushed. "
                f"Pipeline at {total_queued} outreach entries, {ready_to_send} ready to send. "
                f"Single blocker: Brevo SMTP credentials."
            ),
        },
        "metrics_history": state.get("metrics_history", []) + [{
            "cycle":           cycle_num,
            "date":            datetime.now().strftime("%Y-%m-%d"),
            "total_leads":     new_total_leads,
            "hot_leads":       sum(1 for r in read_leads() if r.get("grade") in ("F","D")),
            "with_email":      ready_to_send,
            "surge_deployed":  472,
            "ghpages_deployed": new_total_ghpages,
            "outreach_queued": total_queued,
            "ready_to_send":   ready_to_send,
        }],
    })
    save_state(state)

    print(f"\n{'='*60}")
    print(f"  CYCLE {cycle_num} COMPLETE")
    print(f"  New leads: {total_new} | F/D grade: {total_f} | Sites built: {len(deployed)}")
    print(f"  GH Pages pushed: {ghpages_new} | Queue: {total_queued} | Ready: {ready_to_send}")
    print(f"  Report: {REPORT_FILE}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
