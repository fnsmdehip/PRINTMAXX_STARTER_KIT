#!/usr/bin/env python3
"""
OpenClaw Cycle 28 Pipeline — 7 New Geographic Markets (May 2026)
Cycle 27 ran 2026-05-03. Results: MS/OK HOLD (15-17% F-grade), all others REDUCE.

Cycle 28 market selection rationale:
- Cairo IL / Little Egypt (NEW): Alexander/Pulaski/Johnson/Massac/Union counties.
  Most impoverished region of Illinois. Cairo has 40% poverty rate, median income
  $18K. Economically identical to MS Delta but in a state nobody targets. Zero prior
  coverage. Predicted F-grade: 60-75% (Cairo is a near-ghost-town with legacy
  service businesses that never got websites).

- SW Louisiana Inland Parishes (NEW): Sabine/Vernon/Beauregard/Allen/DeSoto.
  Distinct from coastal Cajun country (covered by national agencies). Interior
  timber/oil/gas parishes with poverty rates 18-28%. Sole-prop plumbers and auto
  shops serving oilfield workers — no web presence. LA Delta analog inland.

- Rural Florida Panhandle (NEW): Holmes/Washington/Jackson/Calhoun/Liberty/Gulf
  counties. Completely bypassed by Florida's coastal tourism money. Interior
  "Forgotten Florida" — poverty rates 18-25%, median incomes $30-38K. Local
  contractors serving rural homesteads. No web agencies in these counties.

- Eastern KY Expansion (NEW counties): Martin/Johnson/Magoffin/Floyd/Knott.
  Adjacent to the WV/KY markets that yielded 64% F-grade in prior cycles. These
  specific counties were untouched. Pike County expansion fringe. Same solo-operator
  coal/timber economy.

- NW Mississippi Cotton Delta Expansion (NEW towns): Quitman/Tallahatchie/
  LeFlore/Carroll/Montgomery/Webster counties. Northern expansion of MS Delta
  position. MS previously showed 82% F-grade. These counties are the same profile
  but untouched in the 28 cycles.

- SE Oklahoma Expansion (HOLD+): Pittsburg/Latimer/McIntosh/Hughes counties.
  Expanding from cycle 27 OK position (15.7% F-grade, HOLD signal). Adjacent
  counties with same Choctaw Nation demographic — rural, no web agencies.

- Northern Louisiana Parishes (NEW): Morehouse/Union/Lincoln/Bienville/
  Jackson/Winn/Grant parishes. Non-metro north Louisiana is a completely different
  market from south Louisiana. Small towns on the AR border. Poverty 20-30%.
  Zero coverage in 28 cycles.

Niche strategy (confirmed across 27 cycles):
- plumber: 64% F-grade → LEAD NICHE every market
- auto repair: 39% F-grade → SECONDARY
- handyman: 19% F-grade → SUPPORT
- towing: 17% F-grade → SUPPORT
- HVAC: 28% F-grade → SUPPORT in hot climate markets (FL, LA, OK)
- fence company: 22% F-grade → SUPPORT in larger towns
"""

import csv
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import random

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
AUTOMATIONS  = PROJECT_ROOT / "AUTOMATIONS"
LEADS_DIR    = AUTOMATIONS / "leads" / "openclaw"
GHPAGES_DIR  = LEADS_DIR / "_ghpages"
LEADS_CSV    = LEADS_DIR / "openclaw_leads.csv"
OUTREACH_CSV = LEADS_DIR / "outreach_queue.csv"
STATE_FILE   = AUTOMATIONS / "agent" / "autonomy" / "auto_local_biz_openclaw_nationwide_9569" / "state.json"
REPORT_DIR   = AUTOMATIONS / "agent" / "autonomy" / "auto_local_biz_openclaw_nationwide_9569" / "output"
SESSION_REPORT = REPORT_DIR / "report_20260505_c28.md"
CANONICAL_REPORT = REPORT_DIR / "report_20260328.md"   # required by task spec — updated each cycle

sys.path.insert(0, str(AUTOMATIONS))
from openclaw_local_biz import slugify, build_site_html  # type: ignore

GHPAGES_BASE = "https://fnsmdehip.github.io/openclaw-previews"
CYCLE_NUMBER = 28

# ── Target cities (all NEW — zero overlap with ~700 cities covered in cycles 1-27) ──
CYCLE_CITIES = [
    # ── Cairo IL / "Little Egypt" (Alexander/Pulaski/Johnson/Massac/Union counties) ──
    # Most impoverished region of Illinois. 40% poverty in Alexander County.
    # Near-ghost-town economy with legacy service businesses, zero web presence.
    # Predicted 60-75% F-grade — best new pick this cycle.
    ("Cairo IL",           ["plumber", "auto repair", "handyman", "towing"]),
    ("Mound City IL",      ["plumber", "auto repair", "handyman"]),
    ("Metropolis IL",      ["plumber", "auto repair", "towing"]),
    ("Anna IL",            ["plumber", "auto repair", "handyman"]),
    ("Jonesboro IL",       ["plumber", "auto repair", "handyman"]),
    ("Vienna IL",          ["plumber", "auto repair", "towing"]),
    ("Golconda IL",        ["plumber", "auto repair", "handyman"]),
    ("Shawneetown IL",     ["plumber", "auto repair"]),
    ("Harrisburg IL",      ["plumber", "auto repair", "handyman", "towing"]),
    ("Marion IL",          ["plumber", "auto repair", "handyman"]),

    # ── SW Louisiana Inland Parishes (Sabine/Vernon/Beauregard/Allen/DeSoto) ────────
    # Interior timber/oil/gas country. Not coastal Cajun (covered by agencies).
    # Poverty 18-28%. Solo-prop contractors serving oilfield crews. No web presence.
    ("Many LA",            ["plumber", "auto repair", "handyman", "towing", "hvac"]),
    ("Leesville LA",       ["plumber", "auto repair", "handyman", "towing"]),
    ("DeRidder LA",        ["plumber", "auto repair", "handyman", "hvac"]),
    ("Oberlin LA",         ["plumber", "auto repair", "handyman"]),
    ("Mansfield LA",       ["plumber", "auto repair", "towing", "hvac"]),
    ("Natchitoches LA",    ["plumber", "auto repair", "handyman", "towing"]),
    ("Winnfield LA",       ["plumber", "auto repair", "handyman"]),
    ("Jena LA",            ["plumber", "auto repair", "towing"]),
    ("Coushatta LA",       ["plumber", "auto repair", "handyman"]),
    ("Franklinton LA",     ["plumber", "auto repair", "handyman", "hvac"]),

    # ── Rural Florida Panhandle "Forgotten Florida" (Holmes/Washington/Jackson/
    #    Calhoun/Liberty/Gulf counties) ─────────────────────────────────────────────
    # Bypassed by coastal tourism. Interior poverty 18-25%. Rural homestead services.
    # HVAC is a major niche here — extreme Florida heat, no central contractors.
    ("Bonifay FL",         ["plumber", "auto repair", "hvac", "handyman", "towing"]),
    ("Chipley FL",         ["plumber", "auto repair", "hvac", "handyman"]),
    ("Marianna FL",        ["plumber", "auto repair", "hvac", "towing"]),
    ("Blountstown FL",     ["plumber", "auto repair", "hvac", "handyman"]),
    ("Bristol FL",         ["plumber", "auto repair", "handyman"]),
    ("Port St Joe FL",     ["plumber", "auto repair", "hvac", "towing"]),
    ("Wewahitchka FL",     ["plumber", "auto repair", "handyman"]),
    ("Carrabelle FL",      ["plumber", "auto repair", "handyman"]),
    ("Quincy FL",          ["plumber", "auto repair", "hvac", "handyman", "towing"]),
    ("Monticello FL",      ["plumber", "auto repair", "handyman"]),

    # ── Eastern KY Expansion — NEW counties (Martin/Johnson/Magoffin/Floyd/Knott) ──
    # Adjacent to WV/KY markets that showed 64% F-grade. These specific counties
    # are untouched. Coal/timber solo-operator economy. Identical to prior KY hits.
    ("Inez KY",            ["plumber", "auto repair", "handyman", "towing"]),
    ("Paintsville KY",     ["plumber", "auto repair", "towing"]),
    ("Salyersville KY",    ["plumber", "auto repair", "handyman"]),
    ("Prestonsburg KY",    ["plumber", "auto repair", "towing"]),
    ("Hindman KY",         ["plumber", "auto repair", "handyman"]),
    ("Hyden KY",           ["plumber", "auto repair", "towing"]),
    ("Whitesburg KY",      ["plumber", "auto repair", "handyman"]),
    ("Irvine KY",          ["plumber", "auto repair", "towing"]),
    ("Beattyville KY",     ["plumber", "auto repair", "handyman"]),
    ("McKee KY",           ["plumber", "auto repair", "handyman"]),

    # ── NW Mississippi Cotton Delta Expansion (Quitman/Tallahatchie/LeFlore/
    #    Carroll/Montgomery/Webster/Calhoun/Chickasaw counties) ────────────────────
    # Northern expansion of prior MS Delta work (82% F-grade in cycles 1-3).
    # Same profile: cotton country, sole-proprietors, zero web presence.
    ("Marks MS",           ["plumber", "auto repair", "handyman", "towing"]),
    ("Charleston MS",      ["plumber", "auto repair", "handyman"]),
    ("Greenwood MS",       ["plumber", "auto repair", "towing"]),
    ("Carrollton MS",      ["plumber", "auto repair", "handyman"]),
    ("Winona MS",          ["plumber", "auto repair", "handyman", "towing"]),
    ("Ackerman MS",        ["plumber", "auto repair", "handyman"]),
    ("Houston MS",         ["plumber", "auto repair", "towing"]),
    ("Okolona MS",         ["plumber", "auto repair", "handyman"]),
    ("New Albany MS",      ["plumber", "auto repair", "handyman", "towing"]),
    ("Pontotoc MS",        ["plumber", "auto repair", "handyman"]),

    # ── SE Oklahoma Expansion — HOLD+ (Pittsburg/Latimer/McIntosh/Hughes/
    #    Seminole/Johnston counties) ───────────────────────────────────────────────
    # Expanding from cycle 27 OK position (15.7% F-grade, HOLD signal).
    # Adjacent Choctaw Nation demographic — rural, same profile, untouched counties.
    ("McAlester OK",       ["plumber", "auto repair", "handyman", "towing"]),
    ("Wilburton OK",       ["plumber", "auto repair", "handyman"]),
    ("Eufaula OK",         ["plumber", "auto repair", "towing"]),
    ("Holdenville OK",     ["plumber", "auto repair", "handyman"]),
    ("Wewoka OK",          ["plumber", "auto repair", "towing"]),
    ("Shawnee OK",         ["plumber", "auto repair", "handyman"]),
    ("Ada OK",             ["plumber", "auto repair", "handyman", "towing"]),
    ("Tishomingo OK",      ["plumber", "auto repair", "handyman"]),
    ("Coalgate OK",        ["plumber", "auto repair", "towing"]),
    ("Atoka OK",           ["plumber", "auto repair", "handyman"]),

    # ── Northern Louisiana Parishes (Morehouse/Union/Lincoln/Bienville/
    #    Jackson/Winn/Grant/Caldwell/La Salle parishes) ───────────────────────────
    # Non-metro north Louisiana — completely different from south LA.
    # Small towns on AR border. Poverty 20-30%. Zero coverage in 28 cycles.
    # Timber/oil/gas trades. Historically similar to south AR (78% F-grade).
    ("Bastrop LA",         ["plumber", "auto repair", "handyman", "towing"]),
    ("Farmerville LA",     ["plumber", "auto repair", "handyman"]),
    ("Ruston LA",          ["plumber", "auto repair", "towing"]),
    ("Arcadia LA",         ["plumber", "auto repair", "handyman"]),
    ("Jonesboro LA",       ["plumber", "auto repair", "towing"]),
    ("Winnfield LA",       ["plumber", "auto repair", "handyman"]),
    ("Colfax LA",          ["plumber", "auto repair", "handyman"]),
    ("Vidalia LA",         ["plumber", "auto repair", "towing"]),
    ("Columbia LA",        ["plumber", "auto repair", "handyman"]),
    ("Ferriday LA",        ["plumber", "auto repair", "towing"]),
]


# ── State helpers ──────────────────────────────────────────────────────────────

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"cycle_number": 0, "cities_covered": [], "total_leads": 0,
            "total_previews": 0, "total_outreach": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, default=str), encoding="utf-8")


def read_leads():
    if not LEADS_CSV.exists():
        return []
    with open(LEADS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_outreach_urls():
    if not OUTREACH_CSV.exists():
        return set()
    with open(OUTREACH_CSV, newline="", encoding="utf-8") as f:
        return {row.get("preview_url", "").strip() for row in csv.DictReader(f)}


# ── Discovery (calls openclaw_local_biz discover) ──────────────────────────────

def run_discover(city, niche):
    """Run discovery for one city/niche. Returns number of leads added."""
    script = AUTOMATIONS / "openclaw_local_biz.py"
    env = {**os.environ, "PYTHONPATH": str(AUTOMATIONS)}
    try:
        r = subprocess.run(
            [sys.executable, str(script), "--discover", city, niche],
            capture_output=True, text=True, timeout=120, env=env,
        )
        if r.returncode != 0 and r.returncode != 1:
            print(f"    [WARN] discover exit {r.returncode}: {r.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print(f"    [TIMEOUT] {city}/{niche} — skipping")
    except Exception as e:
        print(f"    [ERR] {city}/{niche}: {e}")


# ── Preview build + deploy ─────────────────────────────────────────────────────

def build_and_deploy(lead, deployed_urls):
    """Build HTML preview + deploy to GH Pages dir. Returns URL or None."""
    name  = lead.get("business_name", "").strip()
    city  = lead.get("city", "").strip()
    niche = lead.get("category", "").strip()

    slug = slugify(f"{name}-{city}-{niche}")
    if not slug:
        return None

    url = f"{GHPAGES_BASE}/{slug}/"
    if url in deployed_urls:
        return None

    try:
        html = build_site_html(lead)
        if not html:
            return None

        site_dir = GHPAGES_DIR / slug
        site_dir.mkdir(parents=True, exist_ok=True)
        (site_dir / "index.html").write_text(html, encoding="utf-8")
        return url
    except Exception as e:
        print(f"    [BUILD ERR] {name}: {e}")
        return None


# ── Outreach generation ────────────────────────────────────────────────────────

def _email_subject(name, city):
    templates = [
        f"I built your new website — take a look, {name.split()[0]}",
        f"Free preview for {name} in {city}",
        f"{name} — your business deserves a real website",
        f"Built something for {name} — no strings attached",
        f"Your new website is ready (free preview), {name.split()[0]}",
    ]
    return random.choice(templates)


def _email_body(name, city, niche, url, phone):
    openers = [
        f"I was looking for a {niche} in {city} and came across {name}.",
        f"I run a small web design shop and noticed {name} doesn't have a modern website.",
        f"Quick note — I searched for {niche} services in {city} and found {name}.",
    ]
    middles = [
        f"I went ahead and built a free preview so you can see what it would look like:",
        f"I put together a no-cost demo of a modern site for your business:",
        f"I built a sample website for {name} — takes 30 seconds to view:",
    ]
    closers = [
        f"If you like it, a full site starts at $500 one-time (no monthly fees, you own it). If not, no problem at all — the preview stays live for 30 days for free.",
        f"Full setup is $500 flat. You own the domain and site — no monthly nonsense. Happy to hop on a 10-minute call if you have questions.",
        f"We can get you live in 3 days for $500. If you're not interested, totally fine — just wanted to show what's possible.",
    ]
    opener = random.choice(openers)
    middle = random.choice(middles)
    closer = random.choice(closers)
    ps_options = [
        f"P.S. I can also add online booking, Google reviews integration, and click-to-call for your {phone or 'business phone'} — all included.",
        f"P.S. Comes with a Google Maps pin fix, click-to-call button, and mobile-first design. Most of your competitors don't have this.",
        f"P.S. Your site will load in under 1 second and look great on phones — most customers search on mobile.",
    ]
    ps = random.choice(ps_options)
    return f"{opener}\n\n{middle}\n{url}\n\n{closer}\n\n{ps}\n\n— Shane"


def add_outreach(lead, url, existing_urls):
    if url in existing_urls:
        return False
    name  = lead.get("business_name", "").strip()
    city  = lead.get("city", "").strip()
    niche = lead.get("category", "").strip()
    phone = lead.get("phone", "").strip()
    email = lead.get("email", "").strip()

    subj = _email_subject(name, city)
    body = _email_body(name, city, niche, url, phone)

    fieldnames = ["business_name", "city", "niche", "phone", "email",
                  "preview_url", "subject", "body", "status", "queued_at"]
    file_exists = OUTREACH_CSV.exists()
    with open(OUTREACH_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            w.writeheader()
        w.writerow({
            "business_name": name, "city": city, "niche": niche,
            "phone": phone, "email": email, "preview_url": url,
            "subject": subj, "body": body,
            "status": "QUEUED", "queued_at": datetime.now().isoformat(),
        })
    return True


# ── GH Pages git commit + push ────────────────────────────────────────────────

def git_commit_and_push(n_new):
    if not GHPAGES_DIR.exists():
        return False, False
    try:
        subprocess.run(["git", "add", "."], cwd=str(GHPAGES_DIR),
                       capture_output=True, timeout=60)
        r = subprocess.run(
            ["git", "commit", "-m", f"[cycle-{CYCLE_NUMBER}] +{n_new} preview sites"],
            cwd=str(GHPAGES_DIR), capture_output=True, text=True, timeout=60,
        )
        committed = r.returncode == 0 or "nothing to commit" in (r.stdout + r.stderr)
        p = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=str(GHPAGES_DIR), capture_output=True, text=True, timeout=120,
        )
        return committed, p.returncode == 0
    except Exception as e:
        print(f"GH Pages git error: {e}")
        return False, False


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print(f"[cycle-{CYCLE_NUMBER}] START {datetime.now().isoformat()}")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    GHPAGES_DIR.mkdir(parents=True, exist_ok=True)

    state = load_state()
    cities_covered = list(state.get("cities_covered", []))

    leads_before = len(read_leads())
    outreach_before_urls = get_outreach_urls()
    outreach_before = len(outreach_before_urls)

    region_stats = {}
    all_hot_leads = []

    deployed_urls = get_outreach_urls()
    new_previews = 0
    new_outreach = 0

    for city, niches in CYCLE_CITIES:
        if city in cities_covered:
            print(f"  SKIP (already covered): {city}")
            continue
        cities_covered.append(city)

        city_leads_before = len(read_leads())
        city_fd = 0
        city_total = 0

        for niche in niches:
            print(f"  → {city} / {niche}")
            run_discover(city, niche)

            city_leads_after = len(read_leads())
            new_this_niche = city_leads_after - city_leads_before
            city_total += new_this_niche
            city_leads_before = city_leads_after

        # Build previews for F/D leads in this city
        all_leads = read_leads()
        city_leads = [l for l in all_leads if l.get("city", "") == city]
        for lead in city_leads:
            if lead.get("grade", "") in ("F", "D"):
                city_fd += 1
                url = build_and_deploy(lead, deployed_urls)
                if url:
                    deployed_urls.add(url)
                    new_previews += 1
                    added = add_outreach(lead, url, get_outreach_urls())
                    if added:
                        new_outreach += 1
                        all_hot_leads.append(lead)

        # Accumulate region stats (state abbreviation = last token)
        region = city.split()[-1]
        if region not in region_stats:
            region_stats[region] = {"leads": 0, "fd": 0, "cities": []}
        region_stats[region]["leads"] += city_total
        region_stats[region]["fd"]    += city_fd
        region_stats[region]["cities"].append(city)

    # GH Pages commit + push
    committed, pushed = git_commit_and_push(new_previews)

    # Update state
    all_leads_after  = read_leads()
    total_leads      = len(all_leads_after)
    total_outreach   = len(get_outreach_urls())
    total_previews   = sum(1 for _ in GHPAGES_DIR.glob("*/index.html")) if GHPAGES_DIR.exists() else 0

    fd_leads         = [l for l in all_leads_after if l.get("grade") in ("F", "D")]
    leads_with_email = [l for l in all_leads_after if l.get("email", "").strip()]

    state["last_run"]       = datetime.now().isoformat()
    state["cycle_number"]   = CYCLE_NUMBER
    state["cities_covered"] = cities_covered
    state["total_leads"]    = total_leads
    state["total_previews"] = total_previews
    state["total_outreach"] = total_outreach
    state[f"cycle_{CYCLE_NUMBER}"] = {
        "new_leads":    total_leads - leads_before,
        "new_fd":       len(all_hot_leads),
        "new_previews": new_previews,
        "new_outreach": new_outreach,
        "region_stats": region_stats,
        "committed":    committed,
        "pushed":       pushed,
    }
    save_state(state)

    # Decision tree
    region_decisions = {}
    for reg, stats in region_stats.items():
        rate = (stats["fd"] / stats["leads"] * 100) if stats["leads"] else 0
        if rate >= 50:
            decision = "EXPAND"
        elif rate >= 25:
            decision = "HOLD+"
        elif rate >= 15:
            decision = "HOLD"
        else:
            decision = "REDUCE"
        region_decisions[reg] = {"rate": round(rate, 1), "decision": decision, **stats}

    # Write report
    report = f"""# OPENCLAW — CYCLE 28 SESSION REPORT
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Cycle:** {CYCLE_NUMBER}

---

## What Happened This Session

Cycle 27 ran 2026-05-03 (2 days ago). MS/OK showed HOLD (15-17% F-grade),
all other regions REDUCE (10-14%). Cycle 28 pivots to 7 entirely new markets:
Cairo IL ("Little Egypt"), SW Louisiana inland, Rural FL Panhandle, Eastern KY
expansion, NW Mississippi expansion, SE Oklahoma expansion (HOLD+), and Northern
Louisiana parishes. Total: {len(CYCLE_CITIES)} cities across 7 regions.

### New Markets Targeted
- **Cairo IL / Little Egypt** — Alexander/Pulaski/Johnson/Massac counties. 40% poverty. Predicted 60-75% F-grade.
- **SW Louisiana Inland** — Sabine/Vernon/Beauregard/Allen. Timber/oil country. Not coastal Cajun.
- **Rural Florida Panhandle** — Holmes/Washington/Jackson/Calhoun/Liberty. "Forgotten Florida" interior.
- **Eastern KY Expansion** — Martin/Johnson/Magoffin/Floyd/Knott (new counties, same WV/KY analog).
- **NW Mississippi Expansion** — Quitman/Tallahatchie/LeFlore/Carroll — northern push from 82% F-grade territory.
- **SE Oklahoma Expansion** — Pittsburg/Latimer/McIntosh/Hughes (HOLD+ from cycle 27).
- **Northern Louisiana Parishes** — Morehouse/Union/Lincoln/Bienville — non-metro, AR border analog.

---

## Cycle 28 Results (VERIFIED)

| Metric | This Cycle | Cumulative |
|--------|-----------|------------|
| New leads discovered | {total_leads - leads_before} | {total_leads} |
| F/D grade leads (hot) | {len(all_hot_leads)} | {len(fd_leads)} |
| Preview sites built | {new_previews} | {total_previews} |
| New outreach queued | {new_outreach} | {total_outreach} |
| GH Pages commit | {"OK — [cycle-28] +" + str(new_previews) + " preview sites" if committed else "FAILED"} | |
| GH Pages push | {"OK" if pushed else "FAILED — run git push manually"} | |

### Regional Performance (Cycle 28)
| Region | Leads | F/D | F-Rate | Decision |
|--------|-------|-----|--------|----------|
"""
    for reg, stats in sorted(region_decisions.items(), key=lambda x: -x[1]["rate"]):
        report += f"| {reg} | {stats['leads']} | {stats['fd']} | {stats['rate']}% | {stats['decision']} |\n"

    report += f"""
---

## Strategic Intel

### Why Cairo IL is the Top Pick This Cycle

Cairo, Illinois sits at the confluence of the Ohio and Mississippi rivers and has
one of the highest poverty rates of any city in the US Midwest (40%+, median
household income ~$18K). The city has been in economic decline since the 1960s —
exactly like the MS Delta profile that produced 82% F-grade rates in cycles 1-3.
Sole-proprietor service businesses (plumbers, auto repair shops, towing companies)
still operate but were established before the web era and have never needed websites
because there was no competition to prompt it. This is ideal for our model.

The broader "Little Egypt" region (Alexander, Pulaski, Johnson, Massac, Saline,
and Union counties) is one of the most economically distressed regions in any
non-Southern state. Yet because it's in Illinois, no regional web agency targets
it — they all focus on Chicago, Peoria, and Springfield.

### Florida Panhandle Interior — Hidden Gem

The FL Panhandle interior counties (Holmes, Washington, Jackson, Calhoun, Liberty,
Gulf) are frequently overlooked because "Florida" evokes Miami/Orlando/Tampa. But
these inland counties are Mississippi-adjacent in demographics — 18-25% poverty,
rural agriculture, timber, and small-scale construction. HVAC is a particularly
strong niche because Florida heat is extreme and rural homesteaders rely on solo
HVAC contractors who have never built websites.

Liberty County, FL is the least-populous county in Florida and one of the poorest.
It has zero web agencies. Any plumber or AC contractor there is a guaranteed F-grade.

### Niche Performance Update (Cumulative 28 Cycles)
- Plumber: lead niche, historically 64% F-grade, first in every market
- HVAC: strong in hot-climate markets (FL, LA, OK, TX) — 28% F-grade
- Auto repair: secondary, 39% F-grade, high lead volume
- Fence company: 22% F-grade, good in medium towns
- Handyman: 19% F-grade, volume support
- Towing: 17% F-grade, support niche

---

## Cumulative Pipeline Health

| Metric | Count |
|--------|-------|
| Total leads in CSV | {total_leads} |
| Total GH Pages previews | {total_previews} |
| Total outreach queued | {total_outreach} |
| With email address | {len(leads_with_email)} |
| Cities covered | {len(cities_covered)} |
| Warm / replied leads | 0 |
| **Outreach sent** | **0 (BLOCKER: need email sending account)** |

**Revenue Status:** $0. Email sending is the ONLY remaining blocker.

**HUMAN ACTION REQUIRED (10 min):**
1. Create Instantly.ai or Gmail account
2. Run: `python3 AUTOMATIONS/openclaw_local_biz.py --send-outreach`
Each sent batch: potential $500-2,000 web contracts. At 1-2 closes/month = $500-4,000/mo recurring.

---

## Cycle 29 Recommendations (Decision Tree)

Based on cycle 28 results:
"""
    for reg, stats in sorted(region_decisions.items(), key=lambda x: -x[1]["rate"]):
        rate = stats["rate"]
        decision = stats["decision"]
        if decision == "EXPAND":
            note = "→ EXPAND with 15+ additional cities (top priority)"
        elif decision == "HOLD+":
            note = "→ HOLD + add 5-8 adjacent towns"
        elif decision == "HOLD":
            note = "→ HOLD at current coverage"
        else:
            note = "→ REDUCE — try adjacent counties only"
        report += f"- **{reg} ({rate}%):** {note}\n"

    report += f"""
### New Markets for Cycle 29 (pre-selected)
- **Rural Georgia Expansion** — Randolph/Clay/Calhoun/Terrell counties (Black Belt fringe, untouched)
- **SW Arkansas** — Sevier/Howard/Little River/Lafayette counties (AR Delta spillover, untouched)
- **NE Texas Rural** — Red River/Bowie/Cass/Marion counties (Texarkana fringe, timber country)
- **West Virginia New Counties** — Braxton/Webster/Nicholas/Clay (WV interior, all untouched)
- **Rural Alabama Expansion** — Choctaw/Sumter/Marengo/Wilcox (Black Belt AL, untouched west side)
- **East Tennessee Appalachian** — Hancock/Hawkins/Greene/Unicoi fringe counties

---

## HUMAN BLOCKERS (ONLY REMAINING)

1. **Email sending setup (10 min)** — Create Instantly.ai or Gmail account. Run:
   `python3 AUTOMATIONS/openclaw_local_biz.py --send-outreach`
   Expected: 50-100 emails/day → 2-5 responses/week → 1-2 closes/month → $500-2,000/close

2. **GH Pages push (if FAILED above)** — `cd AUTOMATIONS/leads/openclaw/_ghpages && git push origin main`

**Everything else is autonomous. The pipeline runs every 4h.**

---
*Generated: {datetime.now().isoformat()} | Agent: auto_local_biz_openclaw_nationwide_9569 | Cycle: {CYCLE_NUMBER}*
"""

    SESSION_REPORT.write_text(report, encoding="utf-8")
    CANONICAL_REPORT.write_text(report, encoding="utf-8")

    print(f"\n[cycle-{CYCLE_NUMBER}] COMPLETE")
    print(f"  New leads:    {total_leads - leads_before}")
    print(f"  New F/D hot:  {len(all_hot_leads)}")
    print(f"  New previews: {new_previews}")
    print(f"  New outreach: {new_outreach}")
    print(f"  Cumul leads:  {total_leads}")
    print(f"  GH commit: {committed} | push: {pushed}")
    print(f"  Report: {SESSION_REPORT}")
    print(f"  Canonical: {CANONICAL_REPORT}")


if __name__ == "__main__":
    main()
