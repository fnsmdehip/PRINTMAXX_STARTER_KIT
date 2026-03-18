#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 066
Strategy: HOBBY_TRACKERS + PHYSICAL_WELLNESS_MICRO_HABITS
Date: 2026-03-17
Targets: knitting/craft streaks, hiking habits, yoga/sun salutation, IF streak,
         water intake, 10k steps, declutter daily, language immersion,
         daily doodle, breathwork, cold plunge, sauna weekly
"""

import json
import time
import requests
import csv
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "data"
OUTPUT = BASE / "output"
LEDGER = Path(__file__).parent.parent.parent.parent.parent / "LEDGER"
ALPHA_CSV = LEDGER / "ALPHA_STAGING.csv"
CI_CSV = LEDGER / "COMPETITIVE_INTEL.csv"

CYCLE = 66
NOW = datetime.now(timezone.utc)
DATE_STR = NOW.strftime("%Y-%m-%d")
TS = NOW.strftime("%Y%m%d_%H%M")

GENERIC_TRACKERS = {
    "streaks", "habitica", "productive", "habitminder", "habit tracker",
    "loop habit tracker", "done", "streaks - habit tracker", "habitnow",
    "habit - daily tracker", "everyday", "habitify", "strides", "way of life",
    "coach.me", "fabulous", "productive - habit tracker", "daylio",
    "habitbull", "momentum", "finch", "tiimo", "routinery", "myfitnesspal",
    "noom", "loseit", "cronometer", "nike training", "peloton"
}

NICHES = {
    "knitting_craft_streak": {
        "label": "Daily Knitting / Craft Practice Streak",
        "subreddits": ["knitting", "crochet", "crafts"],
        "itunes_terms": ["knitting streak daily habit paid", "craft practice tracker streak paid"],
        "hypothesis": "BO — knitting 1M+, crochet 3M+. Zero dedicated streak apps. Craft is massive TikTok trend."
    },
    "hiking_weekly_habit": {
        "label": "Weekly Hiking / Trail Habit Tracker",
        "subreddits": ["hiking", "trailrunning", "backpacking"],
        "itunes_terms": ["hiking habit tracker weekly paid streak", "trail hiking daily streak paid"],
        "hypothesis": "SOFT — Alltrails dominates logging but NOT habit streak. Dedicated hiking-streak niche open."
    },
    "sun_salutation_streak": {
        "label": "Daily Sun Salutation / Morning Yoga Streak",
        "subreddits": ["yoga", "morningroutine", "Meditation"],
        "itunes_terms": ["sun salutation streak daily paid", "morning yoga habit tracker streak paid"],
        "hypothesis": "BO — r/yoga 500K+. Sun salutation is universal entry yoga. No dedicated streak app."
    },
    "intermittent_fasting_streak": {
        "label": "Intermittent Fasting Streak Tracker",
        "subreddits": ["intermittentfasting", "fasting", "OMAD"],
        "itunes_terms": ["intermittent fasting streak habit paid daily", "IF fasting tracker streak paid"],
        "hypothesis": "SOFT — Zero (IF tracker) exists but no pure habit-streak app. 900K IF community."
    },
    "water_intake_daily": {
        "label": "Daily Water Intake Habit Streak",
        "subreddits": ["hydrohomies", "nutrition", "loseit"],
        "itunes_terms": ["water intake streak daily habit paid", "hydration habit tracker streak paid"],
        "hypothesis": "SOFT — WaterMinder exists but habit-streak framing untapped. r/hydrohomies 400K+ active."
    },
    "walking_10k_steps_streak": {
        "label": "Daily 10K Steps Streak Tracker",
        "subreddits": ["walking", "fitness", "running"],
        "itunes_terms": ["10000 steps streak daily habit paid", "walking habit streak tracker paid"],
        "hypothesis": "SOFT — Samsung Health/Apple Health do steps but no streak-gamification. 10K steps is cultural shorthand."
    },
    "declutter_daily_streak": {
        "label": "Daily Declutter / Minimalism Habit Streak",
        "subreddits": ["minimalism", "declutter", "ZeroWaste"],
        "itunes_terms": ["declutter daily streak habit paid", "minimalism habit tracker daily paid"],
        "hypothesis": "BO — r/minimalism 500K+, r/declutter 350K+. No dedicated declutter streak app exists."
    },
    "language_immersion_streak": {
        "label": "Daily Language Immersion / Listening Streak",
        "subreddits": ["languagelearning", "learnspanish", "LearnJapanese"],
        "itunes_terms": ["language immersion streak daily paid", "language listening habit streak paid"],
        "hypothesis": "SOFT — Duolingo owns gamified learning but passive immersion (listening/reading) has no streak app."
    },
    "daily_doodle_streak": {
        "label": "Daily Drawing / Doodle Practice Streak",
        "subreddits": ["learnart", "drawing", "Sketch"],
        "itunes_terms": ["daily drawing streak habit paid", "doodle practice streak tracker paid"],
        "hypothesis": "BO — r/learnart 500K+. Learn-to-draw communities huge. No pure doodle streak app."
    },
    "breathwork_daily": {
        "label": "Daily Breathwork / Box Breathing Streak",
        "subreddits": ["breathwork", "Meditation", "Wim_Hof"],
        "itunes_terms": ["breathwork streak daily habit paid", "box breathing habit tracker streak paid"],
        "hypothesis": "BO — Breathwork rising fast post-COVID. Wim Hof community 200K+. Zero dedicated breathwork streak apps."
    },
    "cold_plunge_streak": {
        "label": "Daily Cold Plunge / Ice Bath Streak",
        "subreddits": ["coldplunge", "Wim_Hof", "biohackers"],
        "itunes_terms": ["cold plunge streak daily habit paid", "ice bath habit tracker streak paid"],
        "hypothesis": "SOFT — Community growing rapidly. Wim Hof app exists but no cold-plunge-specific streak tracker."
    },
    "sauna_weekly_habit": {
        "label": "Weekly Sauna / Heat Therapy Habit Tracker",
        "subreddits": ["Sauna", "biohackers", "longevity"],
        "itunes_terms": ["sauna habit tracker weekly paid streak", "heat therapy streak tracker paid"],
        "hypothesis": "BO — r/Sauna 200K+. Sauna + longevity trend massive. Absolutely zero dedicated sauna tracker apps."
    },
}


def reddit_community_size(subreddits: list) -> tuple[int, dict]:
    """Fetch subscriber counts from Reddit JSON API (no auth needed)."""
    total = 0
    breakdown = {}
    headers = {"User-Agent": "PRINTMAXX-intel-bot/1.0"}
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/about.json"
            resp = requests.get(url, headers=headers, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                subs = data.get("data", {}).get("subscribers", 0)
                total += subs
                breakdown[sub] = subs
                print(f"    r/{sub}: {subs:,}")
            elif resp.status_code == 404:
                breakdown[sub] = 0
                print(f"    r/{sub}: NOT FOUND")
            else:
                breakdown[sub] = 0
                print(f"    r/{sub}: HTTP {resp.status_code}")
            time.sleep(1.2)
        except Exception as e:
            breakdown[sub] = 0
            print(f"    r/{sub}: ERROR {e}")
    return total, breakdown


def itunes_top_competitor(search_terms: list) -> tuple[str, int, int]:
    """Search iTunes for niche apps, filter out generic trackers, return top competitor."""
    best_app = ""
    best_count = 0
    generics_filtered = 0

    for term in search_terms:
        try:
            url = "https://itunes.apple.com/search"
            params = {
                "term": term,
                "entity": "software",
                "country": "us",
                "limit": 10
            }
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code != 200:
                time.sleep(2)
                continue

            results = resp.json().get("results", [])
            for app in results:
                name = app.get("trackName", "").lower().strip()
                ratings = app.get("userRatingCount", 0)

                if any(g in name for g in GENERIC_TRACKERS):
                    generics_filtered += 1
                    continue

                if ratings > best_count:
                    best_count = ratings
                    best_app = app.get("trackName", "")

            time.sleep(1.5)
        except Exception as e:
            print(f"    iTunes error for '{term}': {e}")
            time.sleep(2)

    return best_app, best_count, generics_filtered


def classify_competition(community: int, top_ratings: int, generics_filtered: int) -> str:
    """Score opportunity based on community size vs. competition."""
    if top_ratings == 0 and community >= 100_000:
        return "BLUE_OCEAN"
    if top_ratings <= 500 and community >= 200_000:
        return "BLUE_OCEAN"
    if top_ratings <= 5_000 and community >= 1_000_000:
        return "BLUE_OCEAN"
    if top_ratings <= 20_000 and community >= 5_000_000:
        return "SOFT_COMPETITION"
    if top_ratings <= 50_000 and community >= 10_000_000:
        return "SOFT_COMPETITION"
    if top_ratings > 100_000:
        return "OCCUPIED"
    if community < 50_000:
        return "OCCUPIED"
    return "SOFT_COMPETITION"


def score_opportunity(status: str, community: int, top_ratings: int) -> int:
    score = 0
    if status == "BLUE_OCEAN":
        score += 6
    elif status == "SOFT_COMPETITION":
        score += 3
    if community >= 10_000_000:
        score += 3
    elif community >= 1_000_000:
        score += 2
    elif community >= 100_000:
        score += 1
    if top_ratings == 0:
        score += 1
    elif top_ratings < 1_000:
        score += 1
    return min(score, 10)


def main():
    print(f"\n{'='*60}")
    print(f"COMPETITIVE INTEL SCRAPER — CYCLE {CYCLE}")
    print(f"Strategy: HOBBY_TRACKERS + PHYSICAL_WELLNESS_MICRO_HABITS")
    print(f"Targets: {len(NICHES)} niches")
    print(f"{'='*60}\n")

    raw_results = {}
    blue_oceans = []
    soft_competition = []
    occupied = []
    ci_rows = []
    alpha_entries = []

    # ── STEP 1: CONFIGURE + SCRAPE ──────────────────────────────────
    for niche_key, config in NICHES.items():
        print(f"\n[SCRAPE] {niche_key} — {config['label']}")
        print(f"  Subreddits: {config['subreddits']}")

        community_total, subreddit_breakdown = reddit_community_size(config["subreddits"])
        top_app, top_ratings, generics_filtered = itunes_top_competitor(config["itunes_terms"])

        if top_app:
            print(f"  Top app: '{top_app}' ({top_ratings:,} ratings) | Generic filtered: {generics_filtered}")
        else:
            print(f"  Top app: NONE found | Generic filtered: {generics_filtered}")

        raw_results[niche_key] = {
            "label": config["label"],
            "community_total": community_total,
            "subreddit_breakdown": subreddit_breakdown,
            "top_competitor": top_app,
            "top_competitor_ratings": top_ratings,
            "generics_filtered": generics_filtered,
            "hypothesis": config["hypothesis"]
        }

    # ── STEP 2: CLEAN + ANALYZE ──────────────────────────────────────
    print(f"\n[CLEAN+ANALYZE] Classifying {len(raw_results)} niches...")
    for niche_key, result in raw_results.items():
        status = classify_competition(
            result["community_total"],
            result["top_competitor_ratings"],
            result.get("generics_filtered", 0)
        )
        score = score_opportunity(status, result["community_total"], result["top_competitor_ratings"])
        result["status"] = status
        result["score"] = score

        if status == "BLUE_OCEAN":
            blue_oceans.append((niche_key, result["community_total"]))
        elif status == "SOFT_COMPETITION":
            soft_competition.append(niche_key)
        else:
            occupied.append(niche_key)

        notes_parts = []
        if result["top_competitor"]:
            notes_parts.append(f"Top: '{result['top_competitor']}' ({result['top_competitor_ratings']:,} ratings).")
        else:
            notes_parts.append(f"No dedicated niche app found. {result['generics_filtered']} generic trackers filtered.")
        notes_parts.append(f"Community: {result['community_total']:,}.")

        ci_row = [
            DATE_STR,
            CYCLE,
            niche_key,
            result["label"],
            status,
            result["community_total"],
            ",".join(NICHES[niche_key]["subreddits"]),
            result["top_competitor_ratings"],
            result["generics_filtered"],
            result["top_competitor"],
            result["top_competitor_ratings"],
            " ".join(notes_parts),
            False,
            json.dumps(result["subreddit_breakdown"])
        ]
        ci_rows.append(ci_row)

        if status in ("BLUE_OCEAN", "SOFT_COMPETITION") and result["community_total"] > 500_000:
            alpha_entries.append({
                "date": DATE_STR,
                "source": f"auto_scraper_cycle066_{niche_key}",
                "venture": "APP_FACTORY",
                "category": "APP_FACTORY",
                "title": f"{'BLUE OCEAN' if status == 'BLUE_OCEAN' else 'SOFT'}: {result['label']} — {result['community_total']:,} community",
                "content": (
                    f"Niche: {niche_key}. Status: {status}. Community: {result['community_total']:,}. "
                    f"Top app: {result['top_competitor'] or 'NONE'} ({result['top_competitor_ratings']:,} ratings). "
                    f"{NICHES[niche_key]['hypothesis']}"
                ),
                "roi_potential": "HIGH" if status == "BLUE_OCEAN" else "MEDIUM",
                "status": "PENDING_REVIEW",
                "score": score
            })

    # ── STEP 3: STORE ────────────────────────────────────────────────
    print(f"\n[STORE] Writing {len(ci_rows)} rows to COMPETITIVE_INTEL.csv...")
    try:
        with open(CI_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in ci_rows:
                writer.writerow(row)
        print(f"  [OK] {len(ci_rows)} rows appended to {CI_CSV}")
    except Exception as e:
        print(f"  [ERR] CI CSV write failed: {e}")

    alpha_written = 0
    if alpha_entries and ALPHA_CSV.exists():
        try:
            with open(ALPHA_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for entry in alpha_entries:
                    writer.writerow([
                        entry["date"], entry["source"], entry["venture"],
                        entry["category"], entry["title"], entry["content"],
                        entry["roi_potential"], entry["status"], entry["score"]
                    ])
                    alpha_written += 1
            print(f"  [OK] {alpha_written} alpha entries appended")
        except Exception as e:
            print(f"  [ERR] Alpha staging write failed: {e}")

    # ── STEP 4: SAVE DATA FILES ──────────────────────────────────────
    raw_out = DATA / f"raw_scrape_cycle{CYCLE:03d}.json"
    clean_out = DATA / f"clean_cycle{CYCLE:03d}.json"
    analyze_out = DATA / f"analyze_cycle{CYCLE:03d}.json"

    with open(raw_out, "w") as f:
        json.dump(raw_results, f, indent=2)

    clean_data = {k: v for k, v in raw_results.items() if v.get("community_total", 0) > 0}
    with open(clean_out, "w") as f:
        json.dump(clean_data, f, indent=2)

    top_opps = sorted(
        [(k, v["community_total"]) for k, v in raw_results.items()
         if v.get("status") in ("BLUE_OCEAN", "SOFT_COMPETITION")],
        key=lambda x: x[1], reverse=True
    )[:8]

    analyze_data = {
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "strategy": "HOBBY_TRACKERS + PHYSICAL_WELLNESS_MICRO_HABITS",
        "total_scanned": len(raw_results),
        "blue_oceans": [b[0] for b in blue_oceans],
        "soft_competition": soft_competition,
        "occupied": occupied,
        "top_opportunities": top_opps
    }
    with open(analyze_out, "w") as f:
        json.dump(analyze_data, f, indent=2)

    print(f"  [OK] Raw/clean/analyze JSON saved to data/")

    # ── STEP 5: UPDATE CYCLE STATE ───────────────────────────────────
    try:
        state_path = DATA / "cycle_state.json"
        with open(state_path) as f:
            state = json.load(f)
        prev_bos = state.get("cumulative_blue_oceans", 50)
        prev_p0_alerts = state.get("p0_alerts", [])
    except Exception:
        prev_bos = 50
        prev_p0_alerts = []

    new_bos_count = len(blue_oceans)
    new_total_bos = prev_bos + new_bos_count

    p0_alerts = list(prev_p0_alerts)
    for bo_key, bo_community in sorted(blue_oceans, key=lambda x: x[1], reverse=True):
        label = NICHES[bo_key]["label"]
        alert_str = f"NEW_C066 BLUE OCEAN: {bo_key.upper()} — {bo_community:,} community. BUILD NOW."
        if alert_str not in p0_alerts:
            p0_alerts.insert(0, alert_str)

    near_bos = [
        s for s in soft_competition
        if raw_results.get(s, {}).get("community_total", 0) > 3_000_000
    ]

    new_state = {
        "venture": "SCRAPING_competitive_intel",
        "last_cycle": NOW.isoformat(),
        "cycle_number": CYCLE,
        "cycle_status": "COMPLETE",
        "current_step": "done",
        "configured_at": NOW.isoformat(),
        "stats": {
            "niches_scanned": len(raw_results),
            "new_bos_confirmed": new_bos_count,
            "soft_competition": len(soft_competition),
            "occupied": len(occupied),
            "alpha_entries": alpha_written,
            "ci_rows_added": len(ci_rows),
            "blue_oceans_confirmed": new_total_bos
        },
        "cumulative_blue_oceans": new_total_bos,
        "p0_alerts": p0_alerts,
        f"cycle_{CYCLE}_results": {
            "strategy": "HOBBY_TRACKERS + PHYSICAL_WELLNESS_MICRO_HABITS",
            "new_blue_oceans": [b[0] for b in blue_oceans],
            "near_bos": near_bos,
            "soft_competition": soft_competition,
            "occupied": occupied,
            "biggest_community": sorted(
                [(k, v["community_total"]) for k, v in raw_results.items()],
                key=lambda x: x[1], reverse=True
            )[0] if raw_results else ["N/A", 0]
        }
    }

    with open(DATA / "cycle_state.json", "w") as f:
        json.dump(new_state, f, indent=2)
    print(f"  [OK] cycle_state.json updated → cycle {CYCLE}, {new_total_bos} total BOs")

    return {
        "raw_results": raw_results,
        "blue_oceans": blue_oceans,
        "soft_competition": soft_competition,
        "occupied": occupied,
        "alpha_written": alpha_written,
        "ci_rows": len(ci_rows),
        "new_total_bos": new_total_bos,
        "analyze_data": analyze_data,
        "near_bos": near_bos,
    }


if __name__ == "__main__":
    results = main()
    print(f"\n[CYCLE {CYCLE}] COMPLETE")
    print(f"  Blue Oceans: {len(results['blue_oceans'])}")
    print(f"  Soft Competition: {len(results['soft_competition'])}")
    print(f"  Occupied: {len(results['occupied'])}")
    print(f"  Cumulative BOs: {results['new_total_bos']}")
    print(f"  CI rows added: {results['ci_rows']}")
    print(f"  Alpha entries: {results['alpha_written']}")
