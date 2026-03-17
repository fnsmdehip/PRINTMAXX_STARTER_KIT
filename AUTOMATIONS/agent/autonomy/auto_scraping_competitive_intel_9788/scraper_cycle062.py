#!/usr/bin/env python3
"""
Competitive Intel Scraper - Cycle 062
Strategy: CREATIVE_ARTS + RELATIONSHIPS + BIOHACKING + PETS + ECO
Unexplored territory: drawing/art practice, music streak, writing streak,
                      couples habits, social connection, cold plunge/IF,
                      pet care, zero waste, composting
Date: 2026-03-17
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
AGENT_DIR = BASE_DIR / "AUTOMATIONS/agent/autonomy/auto_scraping_competitive_intel_9788"
DATA_DIR = AGENT_DIR / "data"
OUTPUT_DIR = AGENT_DIR / "output"
LEDGER_FILE = BASE_DIR / "LEDGER/COMPETITIVE_INTEL.csv"

CYCLE = 62
TIMESTAMP = datetime.now(timezone.utc).isoformat()

GENERIC_TRACKER_EXCLUSIONS = [
    "Streaks", "Habitica", "Productive", "HabitMinder",
    "Habit Tracker", "Loop Habit Tracker", "Done",
    "Way of Life", "Strides", "Momentum", "Daily",
    "Bezel", "Finish", "Tally", "Bearable", "Daylio",
    "Reflectly", "Jour", "Five Minute Journal",
    "Streaks Coach", "HabitBull", "Habit List", "Good Habits",
    "Habits - Daily Routine Planner", "MyFitnessPal", "Noom",
]

NICHES = [
    # ── CREATIVE ARTS ──────────────────────────────────────────────────────
    {
        "id": "drawing_streak",
        "label": "Daily Drawing Practice Streak",
        "itunes_terms": ["drawing streak daily practice dedicated", "draw every day habit tracker"],
        "reddit_subs": ["learnart", "sketching", "drawing"],
        "expected_demand": "learnart=700K+, drawing=3M+",
        "rescan": False,
    },
    {
        "id": "music_practice_streak",
        "label": "Daily Music Practice Streak",
        "itunes_terms": ["music practice streak daily dedicated", "instrument practice habit tracker app"],
        "reddit_subs": ["learnmusic", "Guitar", "piano"],
        "expected_demand": "Guitar=4M+, piano=400K+",
        "rescan": False,
    },
    {
        "id": "writing_streak",
        "label": "Daily Writing Practice Streak",
        "itunes_terms": ["writing streak daily dedicated app", "write every day habit streak tracker"],
        "reddit_subs": ["writing", "fiction", "worldbuilding"],
        "expected_demand": "writing=2.8M+, fiction=800K+",
        "rescan": False,
    },
    {
        "id": "photography_habit",
        "label": "Daily Photography Habit Tracker",
        "itunes_terms": ["daily photography streak habit tracker dedicated", "photo a day habit app dedicated"],
        "reddit_subs": ["photography", "photojournalism", "itookapicture"],
        "expected_demand": "photography=21M+",
        "rescan": False,
    },
    # ── RELATIONSHIPS / SOCIAL ─────────────────────────────────────────────
    {
        "id": "couples_habit",
        "label": "Couples Daily Habit & Check-In Tracker",
        "itunes_terms": ["couples habit tracker daily dedicated", "relationship habit streak app dedicated"],
        "reddit_subs": ["relationship_advice", "relationships", "marriage"],
        "expected_demand": "relationship_advice=3.7M+, relationships=2.5M+",
        "rescan": False,
    },
    {
        "id": "social_connection_habit",
        "label": "Daily Social Connection Habit (call a friend)",
        "itunes_terms": ["social connection habit tracker daily dedicated", "call friend streak app dedicated"],
        "reddit_subs": ["socialskills", "lonely", "makingfriends"],
        "expected_demand": "socialskills=800K+, lonely=250K+",
        "rescan": False,
    },
    # ── BIOHACKING ─────────────────────────────────────────────────────────
    {
        "id": "cold_plunge_streak",
        "label": "Cold Plunge / Cold Shower Streak",
        "itunes_terms": ["cold plunge streak tracker dedicated", "cold shower habit streak app dedicated"],
        "reddit_subs": ["coldplunge", "coldshowers", "thermogenesis"],
        "expected_demand": "coldplunge=200K+, coldshowers=500K+",
        "rescan": False,
    },
    {
        "id": "fasting_streak",
        "label": "Intermittent Fasting Streak Tracker",
        "itunes_terms": ["intermittent fasting streak dedicated niche app", "fasting streak habit tracker dedicated"],
        "reddit_subs": ["intermittentfasting", "fasting", "leangains"],
        "expected_demand": "intermittentfasting=800K+, fasting=250K+",
        "rescan": False,
    },
    {
        "id": "sunlight_habit",
        "label": "Morning Sunlight Habit Tracker",
        "itunes_terms": ["morning sunlight habit tracker dedicated", "sunlight exposure streak app dedicated"],
        "reddit_subs": ["morningsunlight", "biohacking", "circadian"],
        "expected_demand": "biohacking=300K+",
        "rescan": False,
    },
    # ── PETS ───────────────────────────────────────────────────────────────
    {
        "id": "dog_training_streak",
        "label": "Daily Dog Training Streak Tracker",
        "itunes_terms": ["dog training streak daily habit dedicated", "dog training session tracker streak dedicated"],
        "reddit_subs": ["Dogtraining", "dogs", "puppy101"],
        "expected_demand": "dogs=4M+, Dogtraining=400K+",
        "rescan": False,
    },
    # ── ECO / SUSTAINABILITY ───────────────────────────────────────────────
    {
        "id": "zero_waste_habit",
        "label": "Zero Waste Daily Habit Tracker",
        "itunes_terms": ["zero waste habit tracker dedicated", "eco habit streak tracker dedicated app"],
        "reddit_subs": ["ZeroWaste", "Anticonsumption", "sustainability"],
        "expected_demand": "ZeroWaste=600K+, sustainability=800K+",
        "rescan": False,
    },
    {
        "id": "plastic_free_streak",
        "label": "Plastic-Free Daily Streak",
        "itunes_terms": ["plastic free streak dedicated app", "single use plastic habit tracker dedicated"],
        "reddit_subs": ["PlasticFreeLiving", "ZeroWaste", "environment"],
        "expected_demand": "ZeroWaste=600K+, environment=1.8M+",
        "rescan": False,
    },
]


def log(msg):
    print(msg)
    log_file = AGENT_DIR / "logs" / f"cycle_{CYCLE:03d}.log"
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, "a") as f:
        f.write(f"{datetime.now().isoformat()} {msg}\n")


def itunes_search(term, country="us", media="software", limit=15, retries=2):
    """Search iTunes API for apps matching term."""
    encoded = urllib.parse.quote(term)
    url = f"https://itunes.apple.com/search?term={encoded}&country={country}&media={media}&limit={limit}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
                return data.get("results", [])
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
    return []


def reddit_sub_size(subreddit, retries=2):
    """Get subscriber count for a subreddit via Reddit JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "PRINTMAXX-CI-Bot/2.0 (research)"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return data.get("data", {}).get("subscribers", 0)
        except Exception:
            if attempt < retries - 1:
                time.sleep(1.5)
    return 0


def is_generic_tracker(app_name):
    """Return True if app is a generic habit tracker, not a niche-specific one."""
    name_lower = app_name.lower()
    for exclusion in GENERIC_TRACKER_EXCLUSIONS:
        if exclusion.lower() in name_lower:
            return True
    generic_keywords = [
        "habit tracker", "habit monitor", "routine tracker",
        "goal tracker", "life tracker", "daily planner",
        "wellness tracker", "health tracker", "self improvement",
    ]
    for kw in generic_keywords:
        if kw in name_lower:
            return True
    return False


def analyze_niche(niche):
    """Run full analysis for one niche: iTunes + Reddit → verdict."""
    nid = niche["id"]
    log(f"\n  Analyzing: {nid}")

    # ── iTunes scan ─────────────────────────────────────────────────────────
    all_apps = []
    for term in niche["itunes_terms"]:
        apps = itunes_search(term)
        time.sleep(0.8)
        all_apps.extend(apps)

    # Deduplicate by trackId
    seen = set()
    unique_apps = []
    for app in all_apps:
        tid = app.get("trackId")
        if tid and tid not in seen:
            seen.add(tid)
            unique_apps.append(app)

    dedicated_apps = []
    generic_filtered = []
    for app in unique_apps:
        name = app.get("trackName", "")
        ratings = app.get("userRatingCount", 0)
        if is_generic_tracker(name):
            generic_filtered.append({"name": name, "ratings_count": ratings})
        else:
            dedicated_apps.append({
                "name": name,
                "ratings_count": ratings,
                "price": app.get("formattedPrice", "Free"),
                "developer": app.get("artistName", ""),
                "version": app.get("version", ""),
            })

    # Sort dedicated by ratings desc
    dedicated_apps.sort(key=lambda x: x["ratings_count"], reverse=True)

    # ── Reddit scan ─────────────────────────────────────────────────────────
    reddit_sizes = {}
    total_community = 0
    for sub in niche["reddit_subs"]:
        size = reddit_sub_size(sub)
        reddit_sizes[sub] = size
        total_community += size
        log(f"    r/{sub}: {size:,}")
        time.sleep(0.5)

    # ── Verdict ─────────────────────────────────────────────────────────────
    n_dedicated = len(dedicated_apps)
    top_ratings = dedicated_apps[0]["ratings_count"] if dedicated_apps else 0

    if n_dedicated == 0:
        verdict = "BLUE_OCEAN"
        reasoning = f"No dedicated niche app found. {len(generic_filtered)} generic trackers filtered out."
    elif n_dedicated == 1 and top_ratings < 5000:
        verdict = "SOFT_COMPETITION"
        reasoning = f"1 weak competitor(s). Top: '{dedicated_apps[0]['name']}' ({top_ratings:,} ratings). Beatable."
    elif n_dedicated <= 2 and top_ratings < 1000:
        verdict = "SOFT_COMPETITION"
        reasoning = f"{n_dedicated} very weak competitors. Top: '{dedicated_apps[0]['name']}' ({top_ratings:,} ratings). Easily beatable."
    else:
        verdict = "OCCUPIED"
        reasoning = f"{n_dedicated} competitors. Top: '{dedicated_apps[0]['name']}' ({top_ratings:,} ratings)."

    log(f"    Verdict: {verdict} | Community: {total_community:,} | Dedicated: {n_dedicated}")

    return {
        "niche": niche,
        "analysis": {
            "verdict": verdict,
            "dedicated_apps": dedicated_apps[:3],
            "generic_filtered": generic_filtered,
            "total_community": total_community,
            "reddit_breakdown": reddit_sizes,
            "reasoning": reasoning,
        },
    }


def run_cycle():
    log(f"=== CYCLE {CYCLE} START: {TIMESTAMP} ===")
    log(f"Strategy: CREATIVE_ARTS + RELATIONSHIPS + BIOHACKING + PETS + ECO")
    log(f"Niches to scan: {len(NICHES)}")

    results = {}
    new_bos = []
    soft_competition = []
    occupied = []

    for niche in NICHES:
        nid = niche["id"]
        result = analyze_niche(niche)
        results[nid] = result
        verdict = result["analysis"]["verdict"]

        if verdict == "BLUE_OCEAN":
            new_bos.append(nid)
            log(f"  *** BLUE OCEAN: {nid} ***")
        elif verdict == "SOFT_COMPETITION":
            soft_competition.append(nid)
        else:
            occupied.append(nid)

    log(f"\nCLEAN: {len(results)} results | BOs: {len(new_bos)} | Soft: {len(soft_competition)} | Occupied: {len(occupied)}")

    # ── Save clean data ──────────────────────────────────────────────────────
    clean_file = DATA_DIR / f"clean_cycle{CYCLE:03d}.json"
    with open(clean_file, "w") as f:
        json.dump(results, f, indent=2)
    log(f"CLEAN: Saved {clean_file.name}")

    # ── STORE → LEDGER/COMPETITIVE_INTEL.csv ────────────────────────────────
    import csv as csv_module
    ci_rows = []
    for nid, r in results.items():
        analysis = r["analysis"]
        ci_rows.append({
            "scan_date": datetime.now().strftime("%Y-%m-%d"),
            "cycle": CYCLE,
            "niche_id": nid,
            "niche_label": r["niche"]["label"],
            "verdict": analysis["verdict"],
            "community_size": analysis["total_community"],
            "dedicated_apps_count": len(analysis["dedicated_apps"]),
            "generic_filtered": len(analysis["generic_filtered"]),
            "top_app": analysis["dedicated_apps"][0]["name"] if analysis["dedicated_apps"] else "",
            "top_app_ratings": analysis["dedicated_apps"][0]["ratings_count"] if analysis["dedicated_apps"] else 0,
            "reasoning": analysis["reasoning"],
            "rescan": r["niche"].get("rescan", False),
            "reddit_breakdown": json.dumps(analysis["reddit_breakdown"]),
        })

    ledger_exists = LEDGER_FILE.exists()
    with open(LEDGER_FILE, "a", newline="") as f:
        fieldnames = list(ci_rows[0].keys())
        writer = csv_module.DictWriter(f, fieldnames=fieldnames)
        if not ledger_exists:
            writer.writeheader()
        writer.writerows(ci_rows)
    log(f"STORE: {len(ci_rows)} rows appended to LEDGER/COMPETITIVE_INTEL.csv")

    # ── ALPHA STAGING ────────────────────────────────────────────────────────
    alpha_staging = BASE_DIR / "LEDGER/ALPHA_STAGING.csv"
    alpha_entries = []
    for nid in new_bos + soft_competition:
        r = results[nid]
        community = r["analysis"]["total_community"]
        verdict = r["analysis"]["verdict"]
        roi = "HIGHEST" if community > 5_000_000 else ("HIGH" if community > 1_000_000 else "MEDIUM")
        priority = "P1" if community > 2_000_000 else "P2"
        tag = "BLUE_OCEAN" if verdict == "BLUE_OCEAN" else "SOFT_COMPETITION"
        action_prefix = "Build dedicated" if verdict == "BLUE_OCEAN" else "Undercut weak competitors in"
        alpha_entries.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": f"CI_CYCLE_{CYCLE}",
            "type": "APP_FACTORY",
            "title": f"ALPHA_CI{CYCLE}_{nid.upper()}",
            "content": f"{tag}: {nid}. Community: {community:,}. {r['analysis']['reasoning']}",
            "status": "PENDING_REVIEW",
            "roi_potential": roi,
            "priority": priority,
            "venture": "APP_FACTORY",
            "action": f"{action_prefix} {nid.replace('_', ' ')} niche. Target $2.99-$4.99.",
        })

    if alpha_entries:
        with open(alpha_staging, "a", newline="") as f:
            fieldnames = list(alpha_entries[0].keys())
            writer = csv_module.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(alpha_entries)
        log(f"ALPHA: {len(alpha_entries)} entries appended to ALPHA_STAGING.csv")

    # ── UPDATE CYCLE STATE ───────────────────────────────────────────────────
    state_file = DATA_DIR / "cycle_state.json"
    state = {}
    if state_file.exists():
        with open(state_file) as f:
            state = json.load(f)

    prev_bos = state.get("cumulative_blue_oceans", 44)
    total_bos = prev_bos + len(new_bos)

    new_state = {
        "venture": "SCRAPING_competitive_intel",
        "last_cycle": TIMESTAMP,
        "cycle_number": CYCLE,
        "cycle_status": "COMPLETE",
        "current_step": "done",
        "configured_at": TIMESTAMP,
        "stats": {
            "niches_scanned": len(NICHES),
            "new_bos_confirmed": len(new_bos),
            "soft_competition": len(soft_competition),
            "occupied": len(occupied),
            "alpha_entries": len(alpha_entries),
            "ci_rows_added": len(ci_rows),
            "blue_oceans_confirmed": total_bos,
        },
        "cumulative_blue_oceans": total_bos,
        "p0_alerts": state.get("p0_alerts", []),
        f"cycle_{CYCLE}_results": {
            "strategy": "CREATIVE_ARTS + RELATIONSHIPS + BIOHACKING + PETS + ECO",
            "new_blue_oceans": new_bos,
            "soft_competition": soft_competition,
            "occupied": occupied,
            "biggest_community": max(
                [(nid, results[nid]["analysis"]["total_community"]) for nid in new_bos],
                key=lambda x: x[1],
                default=("none", 0),
            ),
        },
    }

    with open(state_file, "w") as f:
        json.dump(new_state, f, indent=2)
    log(f"STATE: cycle_state.json updated. Total BOs: {total_bos}")

    # ── GENERATE ALERT ───────────────────────────────────────────────────────
    alert_lines = [
        f"CYCLE {CYCLE} ALERT — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
        f"NEW BOs: {len(new_bos)} | SOFT COMPETITION: {len(soft_competition)} | OCCUPIED: {len(occupied)}",
        f"TOTAL CUMULATIVE BLUE OCEANS: {total_bos}",
        "",
    ]

    if new_bos:
        alert_lines.append("NEW BLUE OCEANS (build priority):")
        for nid in new_bos:
            r = results[nid]
            community = r["analysis"]["total_community"]
            reasoning = r["analysis"]["reasoning"]
            alert_lines.append(f"  ✓ {nid}: {community:,} community")
            alert_lines.append(f"    → {reasoning}")
        alert_lines.append("")

    if soft_competition:
        alert_lines.append("SOFT COMPETITION (beatable with quality):")
        for nid in soft_competition:
            r = results[nid]
            community = r["analysis"]["total_community"]
            reasoning = r["analysis"]["reasoning"]
            alert_lines.append(f"  ~ {nid}: {community:,} community")
            alert_lines.append(f"    → {reasoning}")
        alert_lines.append("")

    alert_lines.append(f"OCCUPIED: {', '.join(occupied) if occupied else 'none'}")
    alert_lines.append("")
    alert_lines.append("P0 BUILD PIPELINE (ranked by community size):")

    # Pull from state p0 alerts
    p0 = new_state.get("p0_alerts", [])
    for i, alert in enumerate(p0[:7], 1):
        alert_lines.append(f"  #{i} {alert}")

    alert_lines.append("")
    alert_lines.append("CRITICAL: PRAYERLOCK — Ramadan ending ~April 1. Ship NOW.")
    alert_lines.append("CRITICAL: Running streak (4.19M demand) still unbuilt.")

    alert_text = "\n".join(alert_lines)
    alert_file = DATA_DIR / "alert_latest.txt"
    with open(alert_file, "w") as f:
        f.write(alert_text)

    log(f"\n=== CYCLE {CYCLE} COMPLETE ===")
    log(f"New BOs: {new_bos}")
    log(f"Cumulative BOs: {total_bos}")
    print(alert_text)

    return new_state


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    run_cycle()
