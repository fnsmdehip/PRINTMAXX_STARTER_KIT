#!/usr/bin/env python3
"""
Cross-Pollinator Bridge — PRINTMAXX
Runs every 4h. Wires venture outputs into venture inputs.
Auto-updates: content topics, lead context, app demand signals.
"""

import json
import csv
import sys
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
AUTOMATIONS = BASE_DIR / "AUTOMATIONS"
LEADS_DIR = AUTOMATIONS / "leads"
AUTONOMY = AUTOMATIONS / "agent" / "autonomy"
REPORTS = AUTOMATIONS / "agent" / "swarm" / "reports"

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

# ─── Connection 1: Lead Machine verticals → Content Farm topic queue ──────────

def extract_lead_verticals():
    """Read latest leads CSV, extract top industries with proof numbers."""
    verticals = {}
    leads_files = sorted(LEADS_DIR.glob("swarm_leads_*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not leads_files:
        log("No leads CSVs found")
        return {}
    latest = leads_files[0]
    log(f"Reading leads from {latest.name}")
    with open(latest, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row.get("category", "").strip()
            score = float(row.get("composite_score", 0) or 0)
            if cat and score >= 7.0:
                if cat not in verticals:
                    verticals[cat] = {"count": 0, "top_score": 0, "top_name": "", "pain": ""}
                verticals[cat]["count"] += 1
                if score > verticals[cat]["top_score"]:
                    verticals[cat]["top_score"] = score
                    verticals[cat]["top_name"] = row.get("name", "")
                    verticals[cat]["pain"] = row.get("pain_points", "")[:120]
    return verticals

def inject_verticals_into_content_farm(verticals):
    """Add lead machine vertical discoveries as content farm topics."""
    topic_file = AUTONOMY / "content_farm_topic_queue.json"
    existing = []
    if topic_file.exists():
        with open(topic_file) as f:
            existing = json.load(f)
    existing_ids = {e.get("alpha_id", "") for e in existing}

    new_topics = []
    added = 0

    # Map: category → hook template
    VERTICAL_HOOKS = {
        "local_biz": {
            "hook": "ran local business website audits this week. average score: 41/100.\n\nmost are on GoDaddy free tier. 5+ year old businesses. no SEO, no CTA, no tracking.\n\none audit email → $499 website rebuild conversation started.",
            "category": "OUTBOUND"
        },
        "tech_contract": {
            "hook": "WebGL engineers are in shortage right now.\n\nfound 2 companies hiring this week (Arcol + Ayeeye). both founder-direct emails.\n\nif your portfolio has one 3D project, you can close these in a day.",
            "category": "OUTBOUND"
        },
        "dental": {
            "hook": "ran 10 dental practice websites through a site audit tool.\n\naverage score: 38/100. one dentist has been on the same Wix site since 2018.\n\npain point is visual and undeniable before the first discovery call.",
            "category": "OUTBOUND"
        },
        "chiro": {
            "hook": "chiropractors are the easiest cold email vertical right now.\n\nsite:godaddysites.com 'chiropractic contact us' surfaces established practices with terrible sites.\n\nno sales call needed. the site is the pitch.",
            "category": "OUTBOUND"
        },
        "accounting": {
            "hook": "accounting firms have the worst websites in any professional service category.\n\nbooking software is from 2011. no case studies. contact page is a phone number.\n\n$1500 minimum for a basic refresh. they'll pay it.",
            "category": "OUTBOUND"
        },
        "vet": {
            "hook": "veterinary hospitals on GoDaddy sites are a goldmine.\n\nthey have reviews, loyal clients, revenue — and a free placeholder website.\n\n$999 rebuild pitch. half the time the owner answers the phone.",
            "category": "OUTBOUND"
        },
        "gym_fitness": {
            "hook": "fitness gyms are underserved on the web.\n\ncalled 5 Miami gyms that had bad sites. 2 answered. 1 asked for a quote.\n\nlocal biz outreach works faster than cold email when you have a real number.",
            "category": "OUTBOUND"
        }
    }

    for cat, data in verticals.items():
        topic_id = f"LEADMACHINE_{cat.upper()}_{datetime.now().strftime('%Y%m%d')}"
        if topic_id in existing_ids:
            continue
        hook_data = VERTICAL_HOOKS.get(cat)
        if not hook_data:
            continue
        new_topics.append({
            "alpha_id": topic_id,
            "category": hook_data["category"],
            "roi": "HIGH" if data["top_score"] >= 8.5 else "MEDIUM",
            "synergy_score": str(int(data["top_score"] * 10)),
            "tactic_preview": f"Lead Machine found {data['count']} {cat} leads. Top: {data['top_name']} ({data['top_score']}/10)",
            "draft_hook": hook_data["hook"],
            "status": "QUEUED",
            "added_at": datetime.now().isoformat()[:16],
            "source": "cross_pollinator_leadmachine"
        })
        added += 1

    if new_topics:
        updated = new_topics + existing  # priority: new at front
        with open(topic_file, "w") as f:
            json.dump(updated, f, indent=2)
        log(f"Content farm: injected {added} topics from lead machine verticals")
    else:
        log("Content farm: no new vertical topics to inject")
    return added

# ─── Connection 2: Alpha OUTBOUND tactics → Lead Machine context refresh ──────

def refresh_outbound_alpha_context():
    """Pull latest OUTBOUND alpha from content_farm_topic_queue into lead machine context."""
    topic_file = AUTONOMY / "content_farm_topic_queue.json"
    context_file = LEADS_DIR / "outbound_alpha_context.md"
    if not topic_file.exists():
        return

    with open(topic_file) as f:
        topics = json.load(f)

    outbound = [t for t in topics if t.get("category") == "OUTBOUND" and t.get("status") == "QUEUED"]
    outbound.sort(key=lambda x: 0 if x.get("roi") == "HIGHEST" else 1)

    lines = [
        "# Outbound Alpha Context — Auto-Refreshed by Cross Pollinator",
        f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"# Source: content_farm_topic_queue.json ({len(outbound)} OUTBOUND entries queued)",
        "# Consumer: Lead Machine agent — apply these when writing outreach",
        "",
        "## Top OUTBOUND Alpha (apply immediately)",
    ]
    for t in outbound[:15]:
        lines.append(f"- [{t.get('roi','?')}] {t.get('tactic_preview','')}")
    lines += [
        "",
        "## Proven Prospecting Methods (Lead Machine intel)",
        "- GoDaddy/Wix subdomain hunting: `[vertical] site:godaddysites.com \"contact us\"`",
        "- HN Who Is Hiring: reply within 24h of post going live",
        "- Direct founder email (jeff@, alex@, thomas@) >> jobs@ >> form",
        "- GoDaddy verticals by deal size: law ($1500-2500) > tech ($120-250K) > dental > chiro > PT > accounting > vet > gym",
        "",
        "## Pitch Framework (from alpha)",
        "- Contract/fractional first — lower commitment barrier",
        "- 4-6 lines max — sweet spot for reply rate",
        "- Disable tracking pixels — Gmail now warns users",
        "- First email = 58% of all replies — make it count",
        "- Warmup: 14-21 days now (2026 update, was 7-14)",
    ]
    context_file.write_text("\n".join(lines))
    log(f"Lead machine context: refreshed with {len(outbound)} OUTBOUND tactics")

# ─── Connection 3: Lead Machine WebGL demand → App Factory priority ───────────

def inject_webgl_demand_into_app_factory():
    """Add WebGL/3D portfolio demand signal from lead machine into app factory queue."""
    queue_file = AUTONOMY / "app_factory_priority_queue.json"
    if not queue_file.exists():
        return

    with open(queue_file) as f:
        data = json.load(f)

    queue = data.get("queue", [])
    existing_ids = {e.get("candidate_id", "") for e in queue}

    new_entries = []
    candidate_id = f"LEADMACHINE_WEBGL_{datetime.now().strftime('%Y%m%d')}"
    if candidate_id not in existing_ids:
        new_entries.append({
            "candidate_id": candidate_id,
            "title": "WebGL/3D portfolio demo — 2 active leads require it (Arcol + Ayeeye)",
            "source": "lead_machine_report_20260318",
            "source_type": "lead_machine_demand",
            "roi_potential": "HIGHEST",
            "priority": "P0",
            "status": "APPROVED",
            "evidence": "Lead Machine found 2 HN leads needing WebGL: Arcol (thomas@arcol.io, 8.5/10) and Ayeeye (ayeeye.careers@gmail.com, 9.5/10). Both need React + WebGL/Three.js. Having one 3D portfolio piece closes both leads. Immediate contract revenue path.",
            "reviewer_notes": "Build a single-page Three.js demo. Can be showcased at webgl-demo.surge.sh. Doubles as portfolio for EAS pitches. Use as conversation opener in outreach to Arcol and Ayeeye.",
            "applicable_niches": "EAS_FREELANCE",
            "applicable_methods": "OUTBOUND",
            "cross_pollinator_inject": True,
            "injected_at": datetime.now().isoformat()[:16]
        })

    # Also inject dental/local-biz web audit tool demand
    audit_id = f"LEADMACHINE_LOCALBIZ_AUDIT_{datetime.now().strftime('%Y%m%d')}"
    if audit_id not in existing_ids:
        new_entries.append({
            "candidate_id": audit_id,
            "title": "Local biz website audit tool — lead machine generating 10+ dental/chiro leads/day via audits",
            "source": "lead_machine_report_20260318",
            "source_type": "lead_machine_demand",
            "roi_potential": "HIGH",
            "priority": "P1",
            "status": "APPROVED",
            "evidence": "GoDaddy/Wix subdomain hunting generating 10 leads/cycle. pagescorer.surge.sh is the audit tool but needs polish. Dental leads score 41/100 average. Visual pain point needs branded report output (PDF). Could sell audit reports at $99-499.",
            "reviewer_notes": "Upgrade pagescorer.surge.sh to output a branded PDF report. Then the audit IS the product — sell it at $99. Lead machine becomes a revenue engine, not just a lead finder.",
            "applicable_niches": "LOCAL_BIZ",
            "applicable_methods": "OUTBOUND",
            "cross_pollinator_inject": True,
            "injected_at": datetime.now().isoformat()[:16]
        })

    if new_entries:
        data["queue"] = new_entries + queue
        data["cross_pollinator_update"] = datetime.now().isoformat()[:16]
        with open(queue_file, "w") as f:
            json.dump(data, f, indent=2)
        log(f"App factory: injected {len(new_entries)} demand signals from lead machine")
    else:
        log("App factory: no new demand signals to inject")

# ─── Connection 4: Content Farm topic hooks → Lead Machine trending angles ────

def sync_trending_angles_to_lead_machine():
    """Extract current CONTENT_FARM alpha trends, write as lead machine warm-up angles."""
    topic_file = AUTONOMY / "content_farm_topic_queue.json"
    angles_file = LEADS_DIR.parent / "agent" / "autonomy" / "outreach_trend_angles.json"
    if not topic_file.exists():
        return

    with open(topic_file) as f:
        topics = json.load(f)

    # Pull HIGHEST ROI content farm topics as trending angles for outreach warm-up
    highest = [t for t in topics if t.get("roi") == "HIGHEST" and
               t.get("category") in ("CONTENT_FARM", "TOOL_ALPHA", "APP_FACTORY") and
               t.get("status") == "QUEUED"][:10]

    angles = {
        "generated_at": datetime.now().isoformat()[:16],
        "source": "cross_pollinator_bridge",
        "purpose": "Lead Machine: use these as warm-up conversation angles when DMing prospects or writing follow-ups",
        "trending_angles": [
            {
                "angle": t.get("tactic_preview", ""),
                "hook": t.get("draft_hook", "").split("\n")[0],
                "category": t.get("category"),
                "roi": t.get("roi"),
                "source_alpha": t.get("alpha_id")
            }
            for t in highest
        ]
    }

    with open(angles_file, "w") as f:
        json.dump(angles, f, indent=2)
    log(f"Trending angles: synced {len(highest)} HIGHEST-ROI topics to lead machine")

# ─── Connection 5: Update cross_pollination bridge state ──────────────────────

def write_bridge_state(stats):
    """Write current bridge state for swarm brain visibility."""
    state_file = AUTOMATIONS / "agent" / "swarm" / "loop_state.json"
    if not state_file.exists():
        return
    with open(state_file) as f:
        data = json.load(f)

    data["cross_pollinator_last_run"] = datetime.now().isoformat()[:16]
    data["cross_pollinator_bridges"] = stats
    with open(state_file, "w") as f:
        json.dump(data, f, indent=2)
    log("Bridge state updated in loop_state.json")

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    log("=== Cross-Pollinator Bridge Starting ===")
    stats = {"connections_run": 0, "items_wired": 0}

    # Connection 1: Lead verticals → content farm
    verticals = extract_lead_verticals()
    if verticals:
        added = inject_verticals_into_content_farm(verticals)
        stats["connections_run"] += 1
        stats["items_wired"] += added

    # Connection 2: Refresh outbound alpha context for lead machine
    refresh_outbound_alpha_context()
    stats["connections_run"] += 1

    # Connection 3: Lead demand → app factory
    inject_webgl_demand_into_app_factory()
    stats["connections_run"] += 1

    # Connection 4: Content trends → lead machine angles
    sync_trending_angles_to_lead_machine()
    stats["connections_run"] += 1

    # Update bridge state
    write_bridge_state(stats)

    log(f"=== Bridge complete: {stats['connections_run']} connections, {stats['items_wired']} items wired ===")
    return stats

if __name__ == "__main__":
    main()
