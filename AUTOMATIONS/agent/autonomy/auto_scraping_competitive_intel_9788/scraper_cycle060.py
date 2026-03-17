#!/usr/bin/env python3
"""
Competitive Intel Scraper - Cycle 060
Strategy: RESCAN_FALSE_POSITIVES + FAITH_CREATIVE_LIFESTYLE_SWEEP
Re-evaluating C059 false positives with generic-tracker exclusion fix.
New niches: bible_reading_streak, photography_streak, chess_habit,
            cooking_streak, declutter_habit, handwriting_habit
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

CYCLE = 60
TIMESTAMP = datetime.now(timezone.utc).isoformat()

# Generic tracker apps to exclude from BO verdicts (not dedicated niche apps)
GENERIC_TRACKER_EXCLUSIONS = [
    "Streaks", "Habitica", "Productive", "HabitMinder",
    "Habit Tracker", "Loop Habit Tracker", "Done",
    "Way of Life", "Strides", "Momentum", "Daily",
    "Bezel", "Finish", "Tally"
]

NICHES = [
    # RESCAN: C059 false positives (Streaks app contaminated results)
    {
        "id": "cold_shower_streak",
        "label": "Cold Shower Streak (RESCAN)",
        "itunes_terms": ["cold shower streak app", "cold shower challenge dedicated"],
        "reddit_subs": ["coldshowers", "Wim_Hof", "coldplunge"],
        "expected_demand": "coldshowers=300K+",
        "rescan": True,
    },
    {
        "id": "drawing_streak",
        "label": "Drawing/Sketch Streak (RESCAN)",
        "itunes_terms": ["drawing streak daily app", "sketch habit daily dedicated"],
        "reddit_subs": ["learnart", "learntodraw", "ArtFundamentals"],
        "expected_demand": "learntodraw=4M+",
        "rescan": True,
    },
    {
        "id": "vitamin_habit",
        "label": "Vitamin/Supplement Habit (RESCAN)",
        "itunes_terms": ["vitamin tracker dedicated streak", "supplement reminder streak dedicated"],
        "reddit_subs": ["Supplements", "vitamins", "nootropics"],
        "expected_demand": "Supplements=1M+",
        "rescan": True,
    },
    {
        "id": "swimming_streak",
        "label": "Swimming Streak (RESCAN)",
        "itunes_terms": ["swimming streak dedicated app", "swim habit tracker dedicated"],
        "reddit_subs": ["Swimming", "openwater", "triathlon"],
        "expected_demand": "Swimming=250K+",
        "rescan": True,
    },
    # NEW: Faith niche
    {
        "id": "bible_reading_streak",
        "label": "Bible Reading Streak",
        "itunes_terms": ["bible reading streak app", "daily bible habit dedicated streak"],
        "reddit_subs": ["Christianity", "Reformed", "TrueChristian"],
        "expected_demand": "Christianity=1M+",
        "rescan": False,
    },
    # NEW: Creative niches
    {
        "id": "photography_streak",
        "label": "Photography Practice Streak",
        "itunes_terms": ["photography streak daily habit", "photo challenge daily streak"],
        "reddit_subs": ["photography", "photochallenge", "beginnerphotography"],
        "expected_demand": "photography=5M+",
        "rescan": False,
    },
    {
        "id": "chess_habit",
        "label": "Chess Daily Habit Streak",
        "itunes_terms": ["chess habit daily streak", "chess practice streak dedicated"],
        "reddit_subs": ["chess", "chessbeginners", "learnchess"],
        "expected_demand": "chess=1M+",
        "rescan": False,
    },
    # NEW: Lifestyle niches
    {
        "id": "cooking_streak",
        "label": "Daily Cooking Streak",
        "itunes_terms": ["cooking habit streak daily", "cook every day streak app"],
        "reddit_subs": ["Cooking", "MealPrepSunday", "EatCheapAndHealthy"],
        "expected_demand": "Cooking=1.5M+",
        "rescan": False,
    },
    {
        "id": "declutter_habit",
        "label": "Declutter/Minimalism Habit",
        "itunes_terms": ["declutter habit streak daily", "minimalism habit streak dedicated"],
        "reddit_subs": ["minimalism", "declutter", "ZeroWaste"],
        "expected_demand": "minimalism=2M+",
        "rescan": False,
    },
    {
        "id": "handwriting_habit",
        "label": "Handwriting Practice Streak",
        "itunes_terms": ["handwriting practice streak daily", "penmanship habit daily dedicated"],
        "reddit_subs": ["Handwriting", "PenmanshipPorn", "fountainpens"],
        "expected_demand": "Handwriting=500K+",
        "rescan": False,
    },
]


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def safe_itunes_search(term, limit=5):
    """Search iTunes for paid apps matching term. Returns list of apps."""
    encoded = urllib.parse.quote(term)
    url = f"https://itunes.apple.com/search?term={encoded}&entity=software&limit={limit}&price=1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        time.sleep(0.5)
        return data.get("results", [])
    except Exception as e:
        log(f"  iTunes error for '{term}': {e}")
        return []


def get_reddit_size(subreddit):
    """Get subscriber count for a subreddit. Returns int."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "printmaxx-intel-bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        subscribers = data.get("data", {}).get("subscribers", 0)
        time.sleep(0.8)
        return subscribers
    except Exception as e:
        log(f"  Reddit error for r/{subreddit}: {e}")
        return 0


def is_generic_tracker(app_name):
    """Return True if app is a generic habit tracker, not a dedicated niche app."""
    app_lower = app_name.lower()
    for excl in GENERIC_TRACKER_EXCLUSIONS:
        if excl.lower() in app_lower:
            return True
    return False


def analyze_niche(niche, itunes_results, reddit_data):
    """
    Determine if niche is a Blue Ocean.
    Returns dict with verdict + reasoning.
    """
    # Filter out generic trackers
    dedicated_apps = []
    generic_apps = []
    for app in itunes_results:
        name = app.get("trackName", "")
        if is_generic_tracker(name):
            generic_apps.append(name)
        else:
            dedicated_apps.append({
                "name": name,
                "price": app.get("formattedPrice", "?"),
                "rating": app.get("averageUserRating", 0),
                "ratings_count": app.get("userRatingCount", 0),
                "version": app.get("version", "?"),
            })

    total_community = sum(reddit_data.values())

    if not dedicated_apps:
        verdict = "BLUE_OCEAN"
        reasoning = f"No dedicated niche app found. {len(generic_apps)} generic trackers filtered out."
    elif len(dedicated_apps) == 1:
        app = dedicated_apps[0]
        if app["ratings_count"] < 50:
            verdict = "BLUE_OCEAN"
            reasoning = f"Only 1 weak competitor: '{app['name']}' ({app['ratings_count']} ratings). Low entrenchment."
        elif app["ratings_count"] < 500:
            verdict = "SOFT_COMPETITION"
            reasoning = f"1 competitor: '{app['name']}' ({app['ratings_count']} ratings). Beatable."
        else:
            verdict = "OCCUPIED"
            reasoning = f"Strong competitor: '{app['name']}' ({app['ratings_count']} ratings)."
    else:
        # Multiple dedicated apps
        top = max(dedicated_apps, key=lambda x: x["ratings_count"])
        if top["ratings_count"] < 200:
            verdict = "SOFT_COMPETITION"
            reasoning = f"{len(dedicated_apps)} weak competitors. Top: '{top['name']}' ({top['ratings_count']} ratings)."
        else:
            verdict = "OCCUPIED"
            reasoning = f"{len(dedicated_apps)} competitors. Top: '{top['name']}' ({top['ratings_count']} ratings)."

    return {
        "verdict": verdict,
        "dedicated_apps": dedicated_apps,
        "generic_filtered": generic_apps,
        "total_community": total_community,
        "reddit_breakdown": reddit_data,
        "reasoning": reasoning,
    }


def run_cycle():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log(f"=== CYCLE {CYCLE} START ===")
    log(f"Strategy: RESCAN_FALSE_POSITIVES + FAITH_CREATIVE_LIFESTYLE_SWEEP")
    log(f"Niches: {len(NICHES)} ({sum(1 for n in NICHES if n.get('rescan'))} rescans, {sum(1 for n in NICHES if not n.get('rescan'))} new)")

    results = {}
    new_bos = []
    soft_competition = []
    occupied = []
    recovered_bos = []  # C059 false positives now confirmed BO

    # ── SCRAPE ──────────────────────────────────────────────────────────────
    for niche in NICHES:
        nid = niche["id"]
        log(f"Scanning: {niche['label']} ({'RESCAN' if niche.get('rescan') else 'NEW'})")

        # iTunes search
        itunes_apps = []
        for term in niche["itunes_terms"]:
            apps = safe_itunes_search(term)
            itunes_apps.extend(apps)

        # Reddit community sizes
        reddit_data = {}
        for sub in niche["reddit_subs"]:
            size = get_reddit_size(sub)
            reddit_data[sub] = size
            log(f"  r/{sub}: {size:,}")

        # Analyze
        analysis = analyze_niche(niche, itunes_apps, reddit_data)
        results[nid] = {
            "niche": niche,
            "analysis": analysis,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }

        verdict = analysis["verdict"]
        community = analysis["total_community"]
        log(f"  Verdict: {verdict} | Community: {community:,} | {analysis['reasoning']}")

        if verdict == "BLUE_OCEAN":
            if niche.get("rescan"):
                recovered_bos.append(nid)
                log(f"  *** RECOVERED BO: {nid} (was false positive in C059) ***")
            else:
                new_bos.append(nid)
                log(f"  *** NEW BLUE OCEAN: {nid} ***")
        elif verdict == "SOFT_COMPETITION":
            soft_competition.append(nid)
        else:
            occupied.append(nid)

    # ── CLEAN + DEDUPLICATE ──────────────────────────────────────────────────
    log(f"\nCLEAN: {len(results)} results, {len(new_bos)} new BOs, {len(recovered_bos)} recovered, {len(soft_competition)} soft")

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

    # Append to LEDGER
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
    all_bos_this_cycle = new_bos + recovered_bos
    alpha_entries = []
    for nid in all_bos_this_cycle:
        r = results[nid]
        community = r["analysis"]["total_community"]
        roi = "HIGHEST" if community > 5_000_000 else ("HIGH" if community > 1_000_000 else "MEDIUM")
        priority = "P1" if community > 2_000_000 else "P2"
        tag = "RECOVERED_BO" if nid in recovered_bos else "NEW_BO"
        alpha_entries.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": f"CI_CYCLE_{CYCLE}",
            "type": "APP_FACTORY",
            "title": f"ALPHA_CI{CYCLE}_{nid.upper()}",
            "content": f"Blue Ocean confirmed: {nid}. Community: {community:,}. {r['analysis']['reasoning']} [{tag}]",
            "status": "PENDING_REVIEW",
            "roi_potential": roi,
            "priority": priority,
            "venture": "APP_FACTORY",
            "action": f"Build dedicated {nid.replace('_',' ')} app. Paid $2.99-$4.99.",
        })

    if alpha_entries:
        alpha_exists = alpha_staging.exists()
        with open(alpha_staging, "a", newline="") as f:
            fieldnames = list(alpha_entries[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not alpha_exists:
                writer.writeheader()
            writer.writerows(alpha_entries)
        log(f"ALPHA: {len(alpha_entries)} entries appended to ALPHA_STAGING.csv")

    # ── UPDATE CYCLE STATE ──────────────────────────────────────────────────
    # Load existing state
    state_file = DATA_DIR / "cycle_state.json"
    state = {}
    if state_file.exists():
        with open(state_file) as f:
            state = json.load(f)

    prev_bos = state.get("cumulative_blue_oceans", 42)
    total_bos = prev_bos + len(new_bos) + len(recovered_bos)

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
            "recovered_bos": len(recovered_bos),
            "soft_competition": len(soft_competition),
            "occupied": len(occupied),
            "alpha_entries": len(alpha_entries),
            "ci_rows_added": len(ci_rows),
            "blue_oceans_confirmed": total_bos,
        },
        "cumulative_blue_oceans": total_bos,
        "p0_alerts": state.get("p0_alerts", []),
        "cycle_60_results": {
            "strategy": "RESCAN_FALSE_POSITIVES + FAITH_CREATIVE_LIFESTYLE",
            "new_blue_oceans": new_bos,
            "recovered_blue_oceans": recovered_bos,
            "soft_competition": soft_competition,
            "occupied": occupied,
            "biggest_community": max(
                [(nid, results[nid]["analysis"]["total_community"]) for nid in all_bos_this_cycle],
                key=lambda x: x[1]
            ) if all_bos_this_cycle else ("none", 0),
        },
        "prev_cycle_summary": {
            "cycle": 59,
            "new_bos": 5,
            "total_bos": 42,
            "top_finds": ["water_habit (12.5M)", "study_streak (3.3M)"],
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
        f"=" * 60,
        f"NEW BOs: {len(new_bos)} | RECOVERED BOs: {len(recovered_bos)} | TOTAL: {total_bos}",
        "",
    ]

    if recovered_bos:
        alert_lines.append("RECOVERED (C059 false positives now confirmed BO):")
        for nid in recovered_bos:
            r = results[nid]
            alert_lines.append(f"  ✓ {nid}: {r['analysis']['total_community']:,} community | {r['analysis']['reasoning']}")

    if new_bos:
        alert_lines.append("\nNEW BLUE OCEANS:")
        for nid in new_bos:
            r = results[nid]
            alert_lines.append(f"  ✓ {nid}: {r['analysis']['total_community']:,} community | {r['analysis']['reasoning']}")

    if soft_competition:
        alert_lines.append(f"\nSOFT COMPETITION (beatable): {', '.join(soft_competition)}")

    alert_lines.extend([
        "",
        f"CUMULATIVE BLUE OCEANS: {total_bos}",
        "",
        "P0 BUILDS (unchanged from C059):",
        "  #1 CLEAN_EATING_STREAK — 11.4M community",
        "  #2 READING_STREAK — 23M community",
        "  #3 WATER_HABIT — 12.5M community",
        "  #4 CODING_STREAK — 4.7M community",
        "  #5 RUNNING_STREAK — 4.2M community",
        "",
        "CRITICAL: PRAYERLOCK — ~13 days remaining in Ramadan",
    ])

    alert_content = "\n".join(alert_lines)
    with open(alert_file, "w") as f:
        f.write(alert_content)

    # Also update alert_latest.txt
    with open(DATA_DIR / "alert_latest.txt", "w") as f:
        f.write(alert_content)

    log(f"\n{alert_content}")

    return {
        "cycle": CYCLE,
        "new_bos": new_bos,
        "recovered_bos": recovered_bos,
        "soft_competition": soft_competition,
        "occupied": occupied,
        "total_bos": total_bos,
        "alpha_entries": len(alpha_entries),
        "ci_rows": len(ci_rows),
    }


if __name__ == "__main__":
    result = run_cycle()
    print(f"\n=== CYCLE {CYCLE} COMPLETE ===")
    print(f"New BOs: {len(result['new_bos'])} | Recovered: {len(result['recovered_bos'])} | Total: {result['total_bos']}")
