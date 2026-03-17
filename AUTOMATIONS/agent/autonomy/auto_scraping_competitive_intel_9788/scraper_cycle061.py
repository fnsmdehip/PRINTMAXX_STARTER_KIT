#!/usr/bin/env python3
"""
Competitive Intel Scraper - Cycle 061
Strategy: MENTAL_HEALTH + FINANCIAL_HABITS + PRODUCTIVITY + OUTDOOR
Unexplored territory: journaling, gratitude, savings, morning routine,
                      sleep, deep work, walking/hiking, gardening
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

CYCLE = 61
TIMESTAMP = datetime.now(timezone.utc).isoformat()

GENERIC_TRACKER_EXCLUSIONS = [
    "Streaks", "Habitica", "Productive", "HabitMinder",
    "Habit Tracker", "Loop Habit Tracker", "Done",
    "Way of Life", "Strides", "Momentum", "Daily",
    "Bezel", "Finish", "Tally", "Bearable", "Daylio",
    "Reflectly", "Jour", "Five Minute Journal",
]

NICHES = [
    # MENTAL HEALTH
    {
        "id": "journaling_streak",
        "label": "Daily Journaling Streak",
        "itunes_terms": ["journaling streak daily dedicated", "journal every day streak app"],
        "reddit_subs": ["Journaling", "bulletjournal", "LifelongLearning"],
        "expected_demand": "Journaling=500K+, bulletjournal=2M+",
        "rescan": False,
    },
    {
        "id": "gratitude_streak",
        "label": "Daily Gratitude Practice Streak",
        "itunes_terms": ["gratitude streak dedicated app", "daily gratitude habit tracker dedicated"],
        "reddit_subs": ["gratitude", "selfimprovement", "decidingtobebetter"],
        "expected_demand": "selfimprovement=1.4M+",
        "rescan": False,
    },
    {
        "id": "anxiety_habit",
        "label": "Anxiety Management Daily Habit",
        "itunes_terms": ["anxiety relief streak dedicated", "anxiety management habit daily app"],
        "reddit_subs": ["Anxiety", "anxietySupport", "mentalhealth"],
        "expected_demand": "Anxiety=700K+",
        "rescan": False,
    },
    # FINANCIAL HABITS
    {
        "id": "no_spend_streak",
        "label": "No-Spend Day Streak",
        "itunes_terms": ["no spend streak dedicated", "no buy challenge streak app dedicated"],
        "reddit_subs": ["NoSpend", "Frugal", "leanfire"],
        "expected_demand": "NoSpend=100K+, Frugal=1M+",
        "rescan": False,
    },
    {
        "id": "savings_streak",
        "label": "Daily Savings Habit Tracker",
        "itunes_terms": ["daily savings streak dedicated", "save money habit streak app"],
        "reddit_subs": ["personalfinance", "financialindependence", "povertyfinance"],
        "expected_demand": "personalfinance=19M+",
        "rescan": False,
    },
    # PRODUCTIVITY
    {
        "id": "deep_work_streak",
        "label": "Deep Work / Focus Session Streak",
        "itunes_terms": ["deep work streak dedicated app", "focus session streak daily"],
        "reddit_subs": ["DeepWork", "productivity", "GetMotivated"],
        "expected_demand": "productivity=2M+",
        "rescan": False,
    },
    {
        "id": "morning_routine_streak",
        "label": "Morning Routine Streak Tracker",
        "itunes_terms": ["morning routine streak dedicated app", "morning habit streak daily tracker"],
        "reddit_subs": ["morningrunners", "morningroutine", "getdisciplined"],
        "expected_demand": "getdisciplined=600K+",
        "rescan": False,
    },
    # OUTDOOR / NATURE
    {
        "id": "walking_streak",
        "label": "Daily Walking Streak",
        "itunes_terms": ["daily walking streak dedicated", "walk every day habit streak app"],
        "reddit_subs": ["Walking", "outdoorwalking", "Hiking"],
        "expected_demand": "Walking=200K+, Hiking=1.2M+",
        "rescan": False,
    },
    {
        "id": "gardening_habit",
        "label": "Daily Gardening Habit Tracker",
        "itunes_terms": ["gardening habit streak daily", "garden every day dedicated streak"],
        "reddit_subs": ["gardening", "vegetablegardening", "plants"],
        "expected_demand": "gardening=5M+",
        "rescan": False,
    },
    # SLEEP / RECOVERY
    {
        "id": "sleep_streak",
        "label": "Sleep Quality Streak Tracker",
        "itunes_terms": ["sleep quality streak dedicated", "bedtime routine streak dedicated app"],
        "reddit_subs": ["sleep", "insomnia", "sleephacks"],
        "expected_demand": "sleep=250K+, insomnia=300K+",
        "rescan": False,
    },
]


def log(msg):
    print(f"[C{CYCLE}] {msg}", flush=True)


def itunes_search(term, limit=10):
    """Search iTunes App Store, return list of app names/ratings."""
    url = f"https://itunes.apple.com/search?term={urllib.parse.quote(term)}&entity=software&limit={limit}&country=us"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX/1.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            data = json.loads(r.read().decode())
        apps = []
        for a in data.get("results", []):
            apps.append({
                "name": a.get("trackName", ""),
                "developer": a.get("artistName", ""),
                "ratings_count": a.get("userRatingCount", 0),
                "price": a.get("price", 0),
                "description": a.get("description", "")[:200],
            })
        return apps
    except Exception as e:
        log(f"  iTunes error ({term[:40]}): {e}")
        return []


def reddit_size(subreddit):
    """Get subscriber count for a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX-CI-Bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        return data.get("data", {}).get("subscribers", 0)
    except Exception as e:
        log(f"  Reddit error (r/{subreddit}): {e}")
        return 0


def is_generic(app_name):
    """Return True if app is a generic tracker (not niche-dedicated)."""
    name_lower = app_name.lower()
    for excl in GENERIC_TRACKER_EXCLUSIONS:
        if excl.lower() in name_lower:
            return True
    return False


def analyze_niche(niche):
    """
    Run iTunes + Reddit analysis for one niche.
    Returns verdict: BLUE_OCEAN | SOFT_COMPETITION | OCCUPIED
    """
    nid = niche["id"]
    log(f"\n--- Analyzing: {niche['label']} ---")

    # iTunes scan
    all_apps = []
    for term in niche["itunes_terms"]:
        apps = itunes_search(term)
        all_apps.extend(apps)
        time.sleep(0.8)

    # Deduplicate by name
    seen_names = set()
    unique_apps = []
    for a in all_apps:
        if a["name"] not in seen_names:
            seen_names.add(a["name"])
            unique_apps.append(a)

    # Split: generic vs dedicated
    generic_filtered = [a for a in unique_apps if is_generic(a["name"])]
    dedicated_apps = [a for a in unique_apps if not is_generic(a["name"])]

    # Sort dedicated by ratings
    dedicated_apps.sort(key=lambda x: x["ratings_count"], reverse=True)

    log(f"  Apps found: {len(unique_apps)} total | {len(dedicated_apps)} dedicated | {len(generic_filtered)} generic filtered")

    # Reddit community size
    reddit_breakdown = {}
    total_community = 0
    for sub in niche["reddit_subs"]:
        size = reddit_size(sub)
        reddit_breakdown[sub] = size
        total_community += size
        log(f"  r/{sub}: {size:,}")
        time.sleep(0.6)

    # Verdict logic
    top_app_ratings = dedicated_apps[0]["ratings_count"] if dedicated_apps else 0
    num_dedicated = len(dedicated_apps)

    if num_dedicated == 0:
        verdict = "BLUE_OCEAN"
        reasoning = f"No dedicated niche app found. {len(generic_filtered)} generic trackers filtered out."
    elif num_dedicated <= 2 and top_app_ratings < 5000:
        verdict = "SOFT_COMPETITION"
        reasoning = f"{num_dedicated} weak competitor(s). Top: '{dedicated_apps[0]['name']}' ({top_app_ratings} ratings). Beatable."
    elif num_dedicated <= 3 and top_app_ratings < 15000:
        verdict = "SOFT_COMPETITION"
        reasoning = f"{num_dedicated} competitors, low traction. Top: '{dedicated_apps[0]['name']}' ({top_app_ratings:,} ratings)."
    else:
        verdict = "OCCUPIED"
        top = dedicated_apps[0]
        reasoning = f"{num_dedicated} competitors. Top: '{top['name']}' ({top['ratings_count']:,} ratings)."

    log(f"  Verdict: {verdict} | Community: {total_community:,}")

    return {
        "niche": niche,
        "analysis": {
            "verdict": verdict,
            "total_community": total_community,
            "dedicated_apps": dedicated_apps,
            "generic_filtered": generic_filtered,
            "reddit_breakdown": reddit_breakdown,
            "reasoning": reasoning,
        }
    }


def run_cycle():
    log(f"=== CYCLE {CYCLE} START: {TIMESTAMP} ===")
    log(f"Strategy: MENTAL_HEALTH + FINANCIAL_HABITS + PRODUCTIVITY + OUTDOOR")
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

    # ── STORE → LEDGER/COMPETITIVE_INTEL.csv ──────────────────────────────
    import csv
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
        writer = csv.DictWriter(f, fieldnames=fieldnames)
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
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(alpha_entries)
        log(f"ALPHA: {len(alpha_entries)} entries appended to ALPHA_STAGING.csv")

    # ── UPDATE CYCLE STATE ──────────────────────────────────────────────────
    state_file = DATA_DIR / "cycle_state.json"
    state = {}
    if state_file.exists():
        with open(state_file) as f:
            state = json.load(f)

    prev_bos = state.get("cumulative_blue_oceans", 43)
    total_bos = prev_bos + len(new_bos)

    new_state = {
        "venture": "SCRAPING_competitive_intel",
        "last_cycle": TIMESTAMP,
        "cycle_number": CYCLE,
        "cycle_status": "COMPLETE",
        "current_step": "done",
        "configured_at": TIMESTAMP,
        "stats": {
            "itunes_terms_scanned": len(NICHES) * 2,
            "reddit_subs_scraped": sum(len(n["reddit_subs"]) for n in NICHES),
            "new_bos_confirmed": len(new_bos),
            "soft_competition": len(soft_competition),
            "occupied": len(occupied),
            "alpha_entries": len(alpha_entries),
            "ci_rows_added": len(ci_rows),
            "blue_oceans_confirmed": total_bos,
        },
        "cumulative_blue_oceans": total_bos,
        "p0_alerts": state.get("p0_alerts", []),
        "cycle_61_results": {
            "strategy": "MENTAL_HEALTH + FINANCIAL_HABITS + PRODUCTIVITY + OUTDOOR",
            "new_blue_oceans": new_bos,
            "soft_competition": soft_competition,
            "occupied": occupied,
            "biggest_community": max(
                [(nid, results[nid]["analysis"]["total_community"]) for nid in new_bos],
                key=lambda x: x[1]
            ) if new_bos else ("none", 0),
        },
        "prev_cycle_summary": {
            "cycle": 60,
            "new_bos": 1,
            "total_bos": 43,
            "top_finds": ["declutter_habit (4.47M)"],
        },
    }

    with open(state_file, "w") as f:
        json.dump(new_state, f, indent=2)

    # ── SAVE CLEAN DATA ────────────────────────────────────────────────────
    clean_file = DATA_DIR / f"clean_cycle{CYCLE:03d}.json"
    with open(clean_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    log(f"DATA: clean_cycle{CYCLE:03d}.json saved")

    # ── ALERT ─────────────────────────────────────────────────────────────
    ts_short = datetime.now().strftime("%H%M")
    alert_file = OUTPUT_DIR / f"alert_20260317_{ts_short}_cycle{CYCLE:03d}.txt"

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
            alert_lines.append(f"  ✓ {nid}: {r['analysis']['total_community']:,} community")
            alert_lines.append(f"    → {r['analysis']['reasoning']}")

    if soft_competition:
        alert_lines.append("\nSOFT COMPETITION (beatable with quality):")
        for nid in soft_competition:
            r = results[nid]
            alert_lines.append(f"  ~ {nid}: {r['analysis']['total_community']:,} community")
            alert_lines.append(f"    → {r['analysis']['reasoning']}")

    if occupied:
        alert_lines.append(f"\nOCCUPIED: {', '.join(occupied)}")

    alert_lines.extend([
        "",
        "P0 BUILD PIPELINE (ranked by community size):",
        "  #1 READING_STREAK — 23M community",
        "  #2 SAVINGS_STREAK — 19M+ community (if BO confirmed this cycle)",
        "  #3 CLEAN_EATING_STREAK — 11.4M",
        "  #4 WATER_HABIT — 12.5M",
        "  #5 CODING_STREAK — 4.7M",
        "",
        "CRITICAL: PRAYERLOCK — Ramadan ending ~April 1. Ship NOW.",
        "CRITICAL: Running streak (4.19M demand) still unbuilt.",
    ])

    alert_content = "\n".join(alert_lines)
    with open(alert_file, "w") as f:
        f.write(alert_content)

    with open(DATA_DIR / "alert_latest.txt", "w") as f:
        f.write(alert_content)
    with open(OUTPUT_DIR / "alert_latest.txt", "w") as f:
        f.write(alert_content)

    log(f"\n{alert_content}")

    return {
        "cycle": CYCLE,
        "new_bos": new_bos,
        "soft_competition": soft_competition,
        "occupied": occupied,
        "total_bos": total_bos,
        "alpha_entries": len(alpha_entries),
        "ci_rows": len(ci_rows),
    }


if __name__ == "__main__":
    result = run_cycle()
    print(f"\n=== CYCLE {CYCLE} COMPLETE ===")
    print(f"BOs: {len(result['new_bos'])} | Soft: {len(result['soft_competition'])} | Total BOs: {result['total_bos']}")
    print(f"New BOs: {result['new_bos']}")
