#!/usr/bin/env python3
"""
Competitive Intel Scraper - Cycle 063
Strategy: FINANCE_WELLNESS + MENTAL_HEALTH + SLEEP_HYGIENE + DIGITAL_WELLNESS + MICRO_HABITS
Unexplored territory: savings streaks, sobriety trackers, sleep consistency habits,
                      screen time detox, morning routines, posture, hydration, gratitude,
                      step walking, journaling sub-niches
Date: 2026-03-17
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
import csv as csv_module
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
AGENT_DIR = BASE_DIR / "AUTOMATIONS/agent/autonomy/auto_scraping_competitive_intel_9788"
DATA_DIR = AGENT_DIR / "data"
OUTPUT_DIR = AGENT_DIR / "output"
LEDGER_FILE = BASE_DIR / "LEDGER/COMPETITIVE_INTEL.csv"

CYCLE = 63
TIMESTAMP = datetime.now(timezone.utc).isoformat()

GENERIC_TRACKER_EXCLUSIONS = [
    "Streaks", "Habitica", "Productive", "HabitMinder",
    "Habit Tracker", "Loop Habit Tracker", "Done",
    "Way of Life", "Strides", "Momentum", "Daily",
    "Bezel", "Finish", "Tally", "Bearable", "Daylio",
    "Reflectly", "Jour", "Five Minute Journal",
    "Streaks Coach", "HabitBull", "Habit List", "Good Habits",
    "Habits - Daily Routine Planner", "MyFitnessPal", "Noom",
    "Fabulous", "Grit", "Habitify", "everyday",
    "Habit Rabbit", "Do Habits", "Habit-Bull",
    "Today Habit", "Habit Tracker", "Way of Life",
    "Routine", "Morning Routine", "Night Routine",
]

NICHES = [
    # ── FINANCE WELLNESS ────────────────────────────────────────────────────
    {
        "id": "savings_streak",
        "label": "Daily Savings Habit / Micro-Savings Streak",
        "itunes_terms": [
            "savings streak daily habit dedicated",
            "save money daily habit app streak",
            "micro savings habit tracker dedicated",
        ],
        "reddit_subs": ["personalfinance", "frugal", "povertyfinance"],
        "expected_demand": "personalfinance=18M+, frugal=2.5M+",
    },
    {
        "id": "budget_habit",
        "label": "Daily Budget Review Habit Streak",
        "itunes_terms": [
            "daily budget habit streak dedicated",
            "budgeting habit streak tracker app",
            "budget check habit daily app",
        ],
        "reddit_subs": ["personalfinance", "ynab", "budget"],
        "expected_demand": "personalfinance=18M+, ynab=300K+",
    },
    {
        "id": "debt_payoff_streak",
        "label": "Debt Snowball / Debt Payoff Streak Tracker",
        "itunes_terms": [
            "debt payoff streak habit tracker dedicated",
            "debt free journey streak app",
            "debt snowball habit app dedicated",
        ],
        "reddit_subs": ["debtfree", "personalfinance", "Fire"],
        "expected_demand": "debtfree=200K+, personalfinance=18M+",
    },
    # ── MENTAL HEALTH / SOBRIETY ─────────────────────────────────────────
    {
        "id": "sobriety_streak",
        "label": "Sobriety / Alcohol-Free Streak Tracker",
        "itunes_terms": [
            "sobriety streak counter dedicated app",
            "sober streak tracker dedicated",
            "alcohol free streak app dedicated",
        ],
        "reddit_subs": ["stopdrinking", "alcoholism", "sobriety"],
        "expected_demand": "stopdrinking=500K+, sobriety=200K+",
    },
    {
        "id": "anxiety_habit",
        "label": "Daily Anxiety Relief / Grounding Habit Streak",
        "itunes_terms": [
            "anxiety relief habit streak daily dedicated",
            "anxiety grounding habit tracker app dedicated",
            "daily calm anxiety streak dedicated",
        ],
        "reddit_subs": ["Anxiety", "mentalhealth", "mindfulness"],
        "expected_demand": "Anxiety=1.2M+, mentalhealth=1M+",
    },
    {
        "id": "therapist_homework_streak",
        "label": "Therapy Homework / CBT Habit Streak",
        "itunes_terms": [
            "therapy homework habit streak dedicated",
            "CBT habit tracker streak dedicated",
            "cognitive behavioral therapy habit app",
        ],
        "reddit_subs": ["therapy", "DBT", "CBT"],
        "expected_demand": "therapy=400K+, mentalhealth=1M+",
    },
    # ── SLEEP HYGIENE ────────────────────────────────────────────────────
    {
        "id": "sleep_streak",
        "label": "Sleep Consistency / Sleep Hygiene Streak",
        "itunes_terms": [
            "sleep consistency streak habit dedicated",
            "sleep hygiene habit streak app dedicated",
            "bedtime habit streak tracker dedicated",
        ],
        "reddit_subs": ["sleep", "insomnia", "sleephacks"],
        "expected_demand": "sleep=800K+, insomnia=500K+",
    },
    {
        "id": "no_screen_bedtime_streak",
        "label": "No Screens Before Bed / Digital Sunset Streak",
        "itunes_terms": [
            "no screen bedtime habit streak dedicated",
            "digital sunset habit streak tracker dedicated",
            "screen free bedtime streak app",
        ],
        "reddit_subs": ["nosurf", "digitalminimalism", "sleep"],
        "expected_demand": "nosurf=200K+, digitalminimalism=100K+",
    },
    # ── DIGITAL WELLNESS ─────────────────────────────────────────────────
    {
        "id": "phone_detox_streak",
        "label": "Phone / Social Media Detox Streak",
        "itunes_terms": [
            "phone detox streak habit dedicated",
            "social media detox streak app dedicated",
            "screen time detox habit streak",
        ],
        "reddit_subs": ["nosurf", "digitalminimalism", "StopSpeending"],
        "expected_demand": "nosurf=200K+, digitalminimalism=100K+",
    },
    # ── MICRO-HABITS & ROUTINES ─────────────────────────────────────────
    {
        "id": "morning_routine_streak",
        "label": "Morning Routine Streak Tracker (custom flow)",
        "itunes_terms": [
            "morning routine streak tracker dedicated app",
            "custom morning routine habit streak app",
            "daily morning ritual streak dedicated",
        ],
        "reddit_subs": ["morningRoutine", "selfimprovement", "productivity"],
        "expected_demand": "selfimprovement=2M+, productivity=1.5M+",
    },
    {
        "id": "walking_streak",
        "label": "Daily Walking Streak (10K steps / walk daily)",
        "itunes_terms": [
            "walking streak habit daily dedicated app",
            "walk every day streak dedicated",
            "daily steps streak habit tracker dedicated",
        ],
        "reddit_subs": ["walking", "loseit", "10000steps"],
        "expected_demand": "walking=400K+, loseit=2.2M+",
    },
    {
        "id": "hydration_streak",
        "label": "Daily Water Intake / Hydration Streak",
        "itunes_terms": [
            "water intake streak habit tracker dedicated",
            "hydration streak daily habit app dedicated",
            "drink water habit streak dedicated",
        ],
        "reddit_subs": ["water", "nutrition", "loseit"],
        "expected_demand": "loseit=2.2M+, nutrition=600K+",
    },
]


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def fetch_itunes(term: str, limit: int = 10) -> list:
    """Query iTunes Search API for apps matching term."""
    encoded = urllib.parse.quote(term)
    url = f"https://itunes.apple.com/search?term={encoded}&entity=software&limit={limit}&country=us"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            return data.get("results", [])
    except Exception as e:
        log(f"  iTunes fetch failed for '{term}': {e}")
        return []


def fetch_reddit_subscribers(subreddit: str) -> int:
    """Get subscriber count for a subreddit via JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "PRINTMAXX-CI-Bot/1.0 (autonomous research)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("data", {}).get("subscribers", 0)
    except Exception as e:
        log(f"  Reddit fetch failed for r/{subreddit}: {e}")
        return 0


def is_generic(name: str) -> bool:
    for excl in GENERIC_TRACKER_EXCLUSIONS:
        if excl.lower() in name.lower():
            return True
    return False


def analyze_niche(niche: dict, raw_itunes: list, reddit_subs: dict) -> dict:
    """Determine BO / SOFT_COMPETITION / OCCUPIED verdict."""
    dedicated = []
    generic_filtered = []

    for app in raw_itunes:
        name = app.get("trackName", "")
        if is_generic(name):
            generic_filtered.append({"name": name, "ratings_count": app.get("userRatingCount", 0)})
        else:
            dedicated.append({
                "name": name,
                "ratings_count": app.get("userRatingCount", 0),
                "price": f"${app.get('price', 0):.2f}" if app.get("price", 0) > 0 else "Free",
                "developer": app.get("artistName", ""),
                "version": app.get("version", ""),
            })

    total_community = sum(reddit_subs.values())
    top_dedicated_ratings = dedicated[0]["ratings_count"] if dedicated else 0

    if not dedicated:
        verdict = "BLUE_OCEAN"
        reasoning = (
            f"No dedicated niche app found. {len(generic_filtered)} generic trackers filtered out. "
            f"Community: {total_community:,}."
        )
    elif top_dedicated_ratings < 5_000:
        verdict = "SOFT_COMPETITION"
        reasoning = (
            f"Weak dedicated app ({dedicated[0]['name']}, {top_dedicated_ratings:,} ratings). "
            f"Beatable with quality build. Community: {total_community:,}."
        )
    elif top_dedicated_ratings < 50_000:
        verdict = "SOFT_COMPETITION"
        reasoning = (
            f"Moderate competition ({dedicated[0]['name']}, {top_dedicated_ratings:,} ratings). "
            f"Undercut with UX + price. Community: {total_community:,}."
        )
    else:
        verdict = "OCCUPIED"
        reasoning = (
            f"Strong dedicated app ({dedicated[0]['name']}, {top_dedicated_ratings:,} ratings). "
            f"Market occupied. Community: {total_community:,}."
        )

    return {
        "verdict": verdict,
        "dedicated_apps": dedicated,
        "generic_filtered": generic_filtered,
        "reddit_breakdown": reddit_subs,
        "total_community": total_community,
        "reasoning": reasoning,
    }


def run_cycle():
    log(f"=== CYCLE {CYCLE} START — {TIMESTAMP} ===")
    log(f"Strategy: FINANCE_WELLNESS + MENTAL_HEALTH + SLEEP_HYGIENE + DIGITAL_WELLNESS + MICRO_HABITS")
    log(f"Niches to scan: {len(NICHES)}")

    results = {}
    raw_data = {}

    for niche in NICHES:
        nid = niche["id"]
        log(f"\n── Scanning: {nid} ──")

        # iTunes scan — use first term, fallback to second
        all_itunes = []
        for term in niche["itunes_terms"][:2]:
            results_raw = fetch_itunes(term, limit=12)
            all_itunes.extend(results_raw)
            time.sleep(2.5)

        # Dedupe by trackId
        seen_ids = set()
        deduped_itunes = []
        for app in all_itunes:
            tid = app.get("trackId")
            if tid not in seen_ids:
                seen_ids.add(tid)
                deduped_itunes.append(app)

        # Reddit subs
        reddit_counts = {}
        for sub in niche["reddit_subs"][:3]:
            count = fetch_reddit_subscribers(sub)
            reddit_counts[sub] = count
            log(f"  r/{sub}: {count:,}")
            time.sleep(2.0)

        analysis = analyze_niche(niche, deduped_itunes, reddit_counts)
        results[nid] = {"niche": niche, "analysis": analysis}
        raw_data[nid] = {"itunes_raw": deduped_itunes, "reddit_raw": reddit_counts}

        log(f"  VERDICT: {analysis['verdict']} | Community: {analysis['total_community']:,}")
        log(f"  {analysis['reasoning']}")

    # ── CLEAN DATA ────────────────────────────────────────────────────────────
    log("\n── CLEAN ──")
    clean_data = {}
    for nid, r in results.items():
        a = r["analysis"]
        clean_data[nid] = {
            "niche": r["niche"],
            "analysis": {
                "verdict": a["verdict"],
                "dedicated_apps": a["dedicated_apps"][:5],
                "generic_filtered_count": len(a["generic_filtered"]),
                "reddit_breakdown": a["reddit_breakdown"],
                "total_community": a["total_community"],
                "reasoning": a["reasoning"],
            },
        }

    with open(DATA_DIR / f"clean_cycle{CYCLE:03d}.json", "w") as f:
        json.dump(clean_data, f, indent=2)
    log(f"CLEAN: Saved clean_cycle{CYCLE:03d}.json")

    # ── ANALYZE ──────────────────────────────────────────────────────────────
    log("\n── ANALYZE ──")
    new_bos = [nid for nid, r in results.items() if r["analysis"]["verdict"] == "BLUE_OCEAN"]
    soft_competition = [nid for nid, r in results.items() if r["analysis"]["verdict"] == "SOFT_COMPETITION"]
    occupied = [nid for nid, r in results.items() if r["analysis"]["verdict"] == "OCCUPIED"]

    analyze_summary = {
        "cycle": CYCLE,
        "timestamp": TIMESTAMP,
        "strategy": "FINANCE_WELLNESS + MENTAL_HEALTH + SLEEP_HYGIENE + DIGITAL_WELLNESS + MICRO_HABITS",
        "total_scanned": len(NICHES),
        "blue_oceans": new_bos,
        "soft_competition": soft_competition,
        "occupied": occupied,
        "top_opportunities": sorted(
            [(nid, results[nid]["analysis"]["total_community"]) for nid in new_bos + soft_competition],
            key=lambda x: x[1],
            reverse=True,
        )[:5],
    }

    with open(DATA_DIR / f"analyze_cycle{CYCLE:03d}.json", "w") as f:
        json.dump(analyze_summary, f, indent=2)
    log(f"ANALYZE: {len(new_bos)} BOs | {len(soft_competition)} soft | {len(occupied)} occupied")

    # ── STORE ─────────────────────────────────────────────────────────────────
    log("\n── STORE ──")
    ci_rows = []
    for nid, r in results.items():
        analysis = r["analysis"]
        ci_rows.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "cycle": CYCLE,
            "niche_id": nid,
            "label": r["niche"]["label"],
            "verdict": analysis["verdict"],
            "community_size": analysis["total_community"],
            "reddit_subs": ",".join(r["niche"]["reddit_subs"]),
            "dedicated_apps_found": len(analysis["dedicated_apps"]),
            "generic_filtered": len(analysis["generic_filtered"]),
            "top_app_name": analysis["dedicated_apps"][0]["name"] if analysis["dedicated_apps"] else "",
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

    # ── ALPHA STAGING ──────────────────────────────────────────────────────
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

    # ── UPDATE CYCLE STATE ─────────────────────────────────────────────────
    state_file = DATA_DIR / "cycle_state.json"
    state = {}
    if state_file.exists():
        with open(state_file) as f:
            state = json.load(f)

    prev_bos = state.get("cumulative_blue_oceans", 45)
    total_bos = prev_bos + len(new_bos)

    # Maintain p0 alerts, appending any new large BOs
    p0 = list(state.get("p0_alerts", []))
    for nid in new_bos:
        community = results[nid]["analysis"]["total_community"]
        if community > 1_000_000:
            label = f"{nid.upper().replace('_', '_')}: {community // 1_000_000:.1f}M community. BUILD NOW."
            if label not in p0:
                p0.append(label)

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
        "p0_alerts": p0,
        f"cycle_{CYCLE}_results": {
            "strategy": "FINANCE_WELLNESS + MENTAL_HEALTH + SLEEP_HYGIENE + DIGITAL_WELLNESS + MICRO_HABITS",
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

    # ── GENERATE ALERT ──────────────────────────────────────────────────────
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
    for i, alert in enumerate(new_state.get("p0_alerts", [])[:8], 1):
        alert_lines.append(f"  #{i} {alert}")

    alert_lines.append("")
    alert_lines.append("CRITICAL: PRAYERLOCK — Ramadan ending ~April 1. Ship NOW.")
    alert_lines.append("CRITICAL: Reading streak (23M demand) still unbuilt.")
    alert_lines.append("CRITICAL: Clean eating streak (11.4M demand) still unbuilt.")

    alert_text = "\n".join(alert_lines)
    alert_file = DATA_DIR / "alert_latest.txt"
    cycle_alert_file = DATA_DIR / f"alert_20260317_1500_cycle{CYCLE:03d}.txt"
    for af in [alert_file, cycle_alert_file]:
        with open(af, "w") as f:
            f.write(alert_text)

    log(f"\n=== CYCLE {CYCLE} COMPLETE ===")
    log(f"New BOs: {new_bos}")
    log(f"Soft competition: {soft_competition}")
    log(f"Cumulative BOs: {total_bos}")
    print("\n" + alert_text)

    return new_state


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    run_cycle()
