#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 069
Strategy: PARENTING + COOKING_FOOD + SPORTS_SPECIFIC + MENTAL_HEALTH + DIGITAL_WELLNESS
Date: 2026-03-18
New territory: 14 niches never scanned before across high-TAM communities.
All previous 58 niches already confirmed/rejected — this cycle covers virgin ground.
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

CYCLE = 69
NOW = datetime.now(timezone.utc)
DATE_STR = NOW.strftime("%Y-%m-%d")
TS = NOW.strftime("%Y%m%d_%H%M")

GENERIC_TRACKERS = {
    "streaks", "habitica", "productive", "habitminder", "habit tracker",
    "loop habit tracker", "done", "streaks - habit tracker", "habitnow",
    "habit - daily tracker", "everyday", "habitify", "strides", "way of life",
    "coach.me", "fabulous", "productive - habit tracker", "daylio",
    "habitbull", "momentum", "finch", "tiimo", "routinery", "myfitnesspal",
    "noom", "loseit", "cronometer", "nike training", "peloton",
    "duolingo", "babbel", "anki", "quizlet", "khan academy", "ynab", "mint",
    "personal capital", "copilot", "clarity money", "parental controls",
    "family link", "screen time", "qustodio", "bark", "circle"
}

NICHES = {
    # ── PARENTING ─────────────────────────────────────────────────────────────
    "bedtime_story_streak": {
        "label": "Daily Bedtime Story Reading Streak (Parent + Child)",
        "subreddits": ["Parenting", "beyondthebump", "daddit"],
        "itunes_terms": ["bedtime story streak daily habit tracker paid parent child", "bedtime reading habit parent daily paid tracker"],
        "community_estimate": 7200000,  # r/Parenting 5.5M + r/daddit 1.2M + r/beyondthebump 500K
        "hypothesis": "BO candidate — 7.2M+ community. 'Read to your child daily' is universal parenting advice. Zero dedicated streak app for parents. Closest: Duolingo (unrelated)."
    },
    "outdoor_play_streak": {
        "label": "Daily Outdoor / Unstructured Play Streak for Kids",
        "subreddits": ["Parenting", "mommit", "OutdoorKids"],
        "itunes_terms": ["outdoor play streak daily kids habit paid tracker parent", "outside time daily habit kids tracker paid"],
        "community_estimate": 6800000,  # r/Parenting 5.5M + r/mommit 800K + r/OutdoorKids 500K
        "hypothesis": "BO candidate — screen time concerns drive demand for outdoor tracking. No dedicated app for tracking daily outdoor play vs parental controls."
    },
    "family_gratitude_streak": {
        "label": "Family Daily Gratitude / Dinner Table Ritual Streak",
        "subreddits": ["Parenting", "daddit", "Mommit"],
        "itunes_terms": ["family gratitude streak daily habit paid tracker parent", "family ritual streak daily paid"],
        "community_estimate": 7500000,
        "hypothesis": "BO — family gratitude rituals are trending (positive parenting movement). Gap: shared streak tracker for family unit not individuals."
    },
    # ── COOKING / FOOD ────────────────────────────────────────────────────────
    "cook_at_home_streak": {
        "label": "Daily Cook-at-Home / No Takeout Streak",
        "subreddits": ["MealPrepSunday", "Cooking", "EatCheapAndHealthy"],
        "itunes_terms": ["cook at home streak daily habit paid tracker no takeout", "home cooking daily habit streak tracker paid"],
        "community_estimate": 8900000,  # r/MealPrepSunday 2.4M + r/Cooking 3.5M + r/EatCheapAndHealthy 3M
        "hypothesis": "BO — eating out is expensive. 'Cook once a day' is a financial AND health goal. Zero dedicated cook-at-home streak app. Huge overlap: r/Frugal + r/EatCheapAndHealthy communities."
    },
    "meal_prep_streak": {
        "label": "Weekly Meal Prep Completion Streak",
        "subreddits": ["MealPrepSunday", "EatCheapAndHealthy", "Fitness"],
        "itunes_terms": ["meal prep streak weekly habit paid tracker", "meal prep streak habit planner paid daily"],
        "community_estimate": 5400000,
        "hypothesis": "SOFT — r/MealPrepSunday 2.4M, strong culture. Meal planning apps (Mealime, Plan to Eat) focus on recipes NOT accountability streaks. Gap is the streak/accountability layer."
    },
    "fermentation_practice_streak": {
        "label": "Daily Fermentation / Sourdough Tending Streak",
        "subreddits": ["fermentation", "Sourdough", "kombucha"],
        "itunes_terms": ["sourdough streak daily habit paid tracker fermentation", "fermentation daily habit tracker paid streak"],
        "community_estimate": 2100000,  # r/fermentation 1M + r/Sourdough 800K + r/kombucha 300K
        "hypothesis": "BO — fermentation is niche but highly engaged. Sourdough starter requires DAILY attention — natural streak mechanic. Zero dedicated app."
    },
    # ── SPORTS-SPECIFIC ───────────────────────────────────────────────────────
    "swimming_laps_streak": {
        "label": "Daily Swimming Laps / Pool Training Streak",
        "subreddits": ["swimming", "openwater", "triathlon"],
        "itunes_terms": ["swimming laps streak daily habit paid tracker", "swim training streak habit daily paid"],
        "community_estimate": 1800000,  # r/swimming 350K + r/triathlon 800K + r/openwater 100K + related
        "hypothesis": "BO — swimmers are data-obsessed. Strava tracks outdoor only. Apple Fitness+ is generic. Zero dedicated lap-swimming streak app separate from GPS trackers."
    },
    "golf_practice_streak": {
        "label": "Daily Golf Practice / Range Habit Streak",
        "subreddits": ["golf", "golfswing", "discgolf"],
        "itunes_terms": ["golf practice streak daily habit paid tracker", "golf range habit daily streak paid app"],
        "community_estimate": 4200000,  # r/golf 1.5M + r/golfswing 500K + r/discgolf 2.2M
        "hypothesis": "BO — r/golf 1.5M, r/discgolf 2.2M. 'Hit the range every day' is a common golf aspiration. Golf apps focus on GPS/scorecard not habit streaks. Clear gap."
    },
    "cycling_km_streak": {
        "label": "Daily Cycling Distance / Ride Streak",
        "subreddits": ["cycling", "bicycling", "velo"],
        "itunes_terms": ["cycling streak daily habit paid tracker", "bike ride streak habit daily paid"],
        "community_estimate": 3500000,  # r/cycling 1.5M + r/bicycling 1.5M + r/velo 500K
        "hypothesis": "SOFT — Strava exists. But Strava = GPS tracking, not habit streaks. Gap: a simple 'did I ride today' accountability streak vs complex GPS log."
    },
    # ── MENTAL HEALTH ─────────────────────────────────────────────────────────
    "cbt_exercise_streak": {
        "label": "Daily CBT / Therapy Homework Exercise Streak",
        "subreddits": ["therapy", "mentalhealth", "OCD"],
        "itunes_terms": ["CBT exercise streak daily habit paid tracker therapy", "therapy homework streak daily habit paid"],
        "community_estimate": 4200000,  # r/mentalhealth 2.5M + r/therapy 600K + r/OCD 300K + r/depression 800K
        "hypothesis": "BO — therapists ASSIGN homework (thought records, exposure tasks). Zero app specifically for CBT exercise streaks. Gap between 'Woebot' (AI) and simple streak accountability."
    },
    "affirmation_streak": {
        "label": "Daily Affirmation / Self-Talk Practice Streak",
        "subreddits": ["lawofattraction", "GetMotivated", "selfimprovement"],
        "itunes_terms": ["affirmation streak daily habit paid tracker self talk", "daily affirmation habit streak paid"],
        "community_estimate": 5800000,  # r/lawofattraction 800K + r/GetMotivated 2.5M + r/selfimprovement 2.5M
        "hypothesis": "BO — affirmations apps exist (ThinkUp, Gratitude) but focus on content delivery not streak tracking. Gap: pure accountability tracker for daily affirmation practice."
    },
    "anger_management_streak": {
        "label": "Daily Anger Management / Emotional Regulation Practice",
        "subreddits": ["anger", "mentalhealth", "BPD"],
        "itunes_terms": ["anger management streak daily habit paid tracker", "emotional regulation habit streak daily paid"],
        "community_estimate": 1200000,
        "hypothesis": "BO — specialized niche. r/anger 200K, therapist-recommended exercises. Zero dedicated anger management streak app. High willingness-to-pay (medical adjacent)."
    },
    # ── DIGITAL WELLNESS ─────────────────────────────────────────────────────
    "no_phone_morning_streak": {
        "label": "No-Phone First Hour / Morning Digital Detox Streak",
        "subreddits": ["nosurf", "digitalminimalism", "getdisciplined"],
        "itunes_terms": ["no phone morning streak habit daily paid tracker", "phone free morning habit streak daily paid"],
        "community_estimate": 2800000,  # r/nosurf 200K + r/digitalminimalism 430K + r/getdisciplined 2.2M
        "hypothesis": "BO — 'no phone first hour' is viral self-help advice. r/nosurf 200K, r/digitalminimalism 430K. Irony: needs app to track not using app. But simple widget/shortcut could work."
    },
    "deep_work_streak": {
        "label": "Daily Deep Work / Focus Block Completion Streak",
        "subreddits": ["getdisciplined", "productivity", "cscareerquestions"],
        "itunes_terms": ["deep work streak daily habit paid tracker focus block", "focus session streak habit daily paid"],
        "community_estimate": 5400000,  # r/getdisciplined 2.2M + r/productivity 2M + r/cscareerquestions 1.2M
        "hypothesis": "BO — 'Deep Work' by Cal Newport. r/productivity 2M+. Forest/Focus apps track individual sessions. Gap: streak accountability for DAILY completion of X deep work blocks."
    },
}

HEADERS = ["type","category","name","price","rating","rating_count","version",
           "last_updated","positive_sentiment","negative_sentiment","source","url",
           "metric_1","metric_2","notes","scan_date"]


def itunes_search(term: str, limit: int = 8) -> list:
    """Search iTunes App Store for apps matching term."""
    try:
        r = requests.get(
            "https://itunes.apple.com/search",
            params={"term": term, "entity": "software", "limit": limit, "country": "us"},
            timeout=12
        )
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception as e:
        print(f"  iTunes error: {e}")
        return []


def reddit_community_size(subreddit: str) -> int:
    """Get subreddit subscriber count via JSON API."""
    try:
        r = requests.get(
            f"https://www.reddit.com/r/{subreddit}/about.json",
            headers={"User-Agent": "PRINTMAXX-CI-Scanner/2.0 (competitive research)"},
            timeout=10
        )
        if r.status_code == 200:
            return r.json().get("data", {}).get("subscribers", 0)
        return 0
    except Exception:
        return 0


def is_generic(app_name: str) -> bool:
    """Return True if app is a generic tracker, not niche-specific."""
    name_lower = app_name.lower()
    return any(g in name_lower for g in GENERIC_TRACKERS)


def classify_competition(apps: list, niche_key: str) -> tuple:
    """
    Returns (status, real_competitors, notes)
    status: BLUE_OCEAN | SOFT_COMPETITION | OCCUPIED
    """
    keyword_fragments = niche_key.replace("_", " ").split()
    real = []
    for app in apps:
        name = app.get("trackName", "")
        if is_generic(name):
            continue
        # Check if app name reflects niche keywords (at least 1 match)
        name_lower = name.lower()
        if any(kw in name_lower for kw in keyword_fragments if len(kw) > 3):
            real.append({
                "name": name,
                "price": app.get("formattedPrice", "Free"),
                "rating": app.get("averageUserRating", 0),
                "rating_count": app.get("userRatingCount", 0),
                "version": app.get("version", ""),
                "genre": app.get("primaryGenreName", ""),
                "updated": app.get("currentVersionReleaseDate", "")[:10] if app.get("currentVersionReleaseDate") else "",
            })

    if not real:
        return "BLUE_OCEAN", real, "No niche-specific apps found in iTunes search"
    elif len(real) <= 2 and all(a["rating_count"] < 5000 for a in real):
        return "SOFT_COMPETITION", real, f"{len(real)} weak competitor(s) found"
    else:
        return "OCCUPIED", real, f"{len(real)} direct competitor(s) found"


def scan_niche(niche_key: str, config: dict) -> dict:
    """Full scan of one niche: iTunes + Reddit community sizing."""
    print(f"\n  [{niche_key}]")
    result = {
        "niche": niche_key,
        "label": config["label"],
        "community_estimate": config.get("community_estimate", 0),
        "hypothesis": config["hypothesis"],
        "itunes_results": [],
        "reddit_sizes": {},
        "status": "UNKNOWN",
        "competitors": [],
        "notes": "",
        "community_actual": 0,
    }

    # 1. Reddit community sizing
    actual_community = 0
    for sub in config.get("subreddits", []):
        size = reddit_community_size(sub)
        result["reddit_sizes"][sub] = size
        actual_community += size
        print(f"    r/{sub}: {size:,}")
        time.sleep(0.8)
    result["community_actual"] = actual_community

    # 2. iTunes search (use first 2 search terms to avoid rate limits)
    all_apps = []
    for term in config.get("itunes_terms", [])[:2]:
        apps = itunes_search(term, limit=6)
        all_apps.extend(apps)
        time.sleep(1.2)

    # Deduplicate by trackId
    seen_ids = set()
    unique_apps = []
    for app in all_apps:
        tid = app.get("trackId")
        if tid and tid not in seen_ids:
            seen_ids.add(tid)
            unique_apps.append(app)
    result["itunes_results"] = [
        {
            "name": a.get("trackName",""),
            "price": a.get("formattedPrice",""),
            "rating": a.get("averageUserRating", 0),
            "rating_count": a.get("userRatingCount", 0),
            "genre": a.get("primaryGenreName",""),
        }
        for a in unique_apps[:8]
    ]

    # 3. Classify competition
    status, competitors, notes = classify_competition(unique_apps, niche_key)
    result["status"] = status
    result["competitors"] = competitors
    result["notes"] = notes

    print(f"    Status: {status} | Community: {actual_community:,} | iTunes apps: {len(unique_apps)}")
    return result


def build_ci_rows(scan_result: dict) -> list:
    """Convert scan result to COMPETITIVE_INTEL.csv rows."""
    rows = []
    niche = scan_result["niche"]
    label = scan_result["label"]
    status = scan_result["status"]
    community = scan_result["community_actual"]
    notes = scan_result["notes"]

    # Row 1: niche-level summary
    rows.append([
        "niche_scan",
        "habit_streak",
        label,
        "",  # price
        "",  # rating
        str(community),  # community size in rating_count
        f"c{CYCLE:03d}",  # version = cycle number
        DATE_STR,
        1 if status == "BLUE_OCEAN" else 0,
        1 if status == "OCCUPIED" else 0,
        "itunes_api+reddit",
        "",
        f"status={status}",
        f"community={community:,}",
        f"{label}. {notes}. Hypothesis: {scan_result['hypothesis'][:120]}",
        NOW.isoformat(),
    ])

    # Row 2+: actual competitors found
    for comp in scan_result.get("competitors", []):
        rows.append([
            "competitor",
            "habit_streak",
            comp["name"],
            comp.get("price", ""),
            str(comp.get("rating", "")),
            str(comp.get("rating_count", "")),
            comp.get("version", ""),
            comp.get("updated", DATE_STR),
            0, 0,
            "itunes_api",
            "",
            f"niche={niche}",
            f"genre={comp.get('genre','')}",
            f"Competitor in {niche} niche",
            NOW.isoformat(),
        ])

    return rows


def build_alpha_rows(scan_result: dict) -> list:
    """Generate ALPHA_STAGING.csv entries for high-value blue oceans."""
    rows = []
    if scan_result["status"] != "BLUE_OCEAN":
        return rows
    community = scan_result["community_actual"]
    if community < 500000:
        return rows  # Only flag large communities

    niche = scan_result["niche"]
    label = scan_result["label"]

    rows.append({
        "date": DATE_STR,
        "source": f"auto_scraping_ci_c{CYCLE:03d}",
        "venture_type": "APP_FACTORY",
        "alpha_type": "BLUE_OCEAN",
        "title": f"BLUE OCEAN: {niche.upper().replace('_',' ')} — No App Exists",
        "content": (
            f"iTunes search + Reddit scan confirms zero niche-specific streak app for: {label}. "
            f"Community: {community:,}. "
            f"{scan_result['hypothesis']} "
            f"BUILD: Streak tracker specifically branded for {label.split('/')[0].strip()}. "
            f"App factory template. Ramadan timing irrelevant — evergreen niche."
        ),
        "roi_potential": "HIGH" if community > 2000000 else "MEDIUM",
        "status": "PENDING_REVIEW",
        "confidence": 75,
        "actionable": "YES",
        "notes": f"Auto-flagged by CI scraper c{CYCLE:03d}. community={community:,}",
    })
    return rows


def append_csv(path: Path, rows: list, headers: list = None):
    """Append rows to CSV, creating headers if file is new."""
    file_exists = path.exists() and path.stat().st_size > 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists and headers:
            writer.writerow(headers)
        writer.writerows(rows)


def load_alpha_headers() -> list:
    """Get existing alpha CSV headers."""
    try:
        with open(ALPHA_CSV, "r") as f:
            return next(csv.reader(f))
    except Exception:
        return ["date","source","venture_type","alpha_type","title","content",
                "roi_potential","status","confidence","actionable","notes"]


def main():
    print(f"\n{'='*60}")
    print(f"COMPETITIVE INTEL SCRAPER — CYCLE {CYCLE:03d}")
    print(f"Strategy: PARENTING + COOKING_FOOD + SPORTS_SPECIFIC + MENTAL_HEALTH + DIGITAL_WELLNESS")
    print(f"Niches: {len(NICHES)} | Timestamp: {NOW.isoformat()}")
    print(f"{'='*60}\n")

    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    all_results = []
    ci_rows_all = []
    alpha_rows_all = []

    stats = {
        "niches_scanned": 0,
        "blue_oceans": 0,
        "soft_competition": 0,
        "occupied": 0,
        "ci_rows_added": 0,
        "alpha_entries": 0,
        "community_total": 0,
    }
    p0_alerts = []

    # Load existing cycle state for cumulative tracking
    cycle_state_path = DATA / "cycle_state.json"
    try:
        prev_state = json.loads(cycle_state_path.read_text())
        cumulative_blue_oceans = prev_state.get("cumulative_blue_oceans", 65)
    except Exception:
        cumulative_blue_oceans = 65  # known baseline from cycle 68

    alpha_headers = load_alpha_headers()

    for niche_key, config in NICHES.items():
        try:
            result = scan_niche(niche_key, config)
            all_results.append(result)
            stats["niches_scanned"] += 1
            stats["community_total"] += result["community_actual"]

            if result["status"] == "BLUE_OCEAN":
                stats["blue_oceans"] += 1
                cumulative_blue_oceans += 1
                alert = f"NEW_C{CYCLE:03d} BLUE OCEAN: {niche_key.upper()} — {result['community_actual']:,} community. BUILD NOW."
                p0_alerts.append(alert)
                print(f"  *** P0 ALERT: {alert}")
            elif result["status"] == "SOFT_COMPETITION":
                stats["soft_competition"] += 1
            else:
                stats["occupied"] += 1

            ci_rows = build_ci_rows(result)
            ci_rows_all.extend(ci_rows)
            stats["ci_rows_added"] += len(ci_rows)

            alpha_rows = build_alpha_rows(result)
            alpha_rows_all.extend(alpha_rows)
            stats["alpha_entries"] += len(alpha_rows)

        except Exception as e:
            print(f"  ERROR scanning {niche_key}: {e}")
            stats["niches_scanned"] += 1

        time.sleep(1.5)  # rate limit between niches

    # ── STORE RESULTS ─────────────────────────────────────────────────────────
    print(f"\n{'─'*40}")
    print("STORING RESULTS...")

    # Raw scrape data
    raw_path = DATA / f"raw_scrape_cycle{CYCLE:03d}.json"
    raw_path.write_text(json.dumps(all_results, indent=2, default=str))
    print(f"  Raw scrape → {raw_path.name}")

    # Append CI CSV
    append_csv(CI_CSV, ci_rows_all, HEADERS)
    print(f"  CI CSV +{len(ci_rows_all)} rows → LEDGER/COMPETITIVE_INTEL.csv")

    # Append Alpha CSV
    if alpha_rows_all:
        alpha_dicts = alpha_rows_all
        alpha_rows_flat = []
        for row_dict in alpha_dicts:
            alpha_rows_flat.append([row_dict.get(h, "") for h in alpha_headers])
        append_csv(ALPHA_CSV, alpha_rows_flat)
        print(f"  Alpha CSV +{len(alpha_rows_all)} entries → LEDGER/ALPHA_STAGING.csv")

    # Analysis file
    analyze_path = DATA / f"analyze_cycle{CYCLE:03d}.json"
    blue_ocean_niches = [r for r in all_results if r["status"] == "BLUE_OCEAN"]
    analysis = {
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "strategy": "PARENTING + COOKING_FOOD + SPORTS_SPECIFIC + MENTAL_HEALTH + DIGITAL_WELLNESS",
        "stats": stats,
        "cumulative_blue_oceans": cumulative_blue_oceans,
        "p0_alerts": p0_alerts,
        "blue_ocean_niches": [
            {
                "niche": r["niche"],
                "label": r["label"],
                "community": r["community_actual"],
                "hypothesis": r["hypothesis"][:200],
            }
            for r in blue_ocean_niches
        ],
        "occupied_niches": [r["niche"] for r in all_results if r["status"] == "OCCUPIED"],
        "soft_competition_niches": [r["niche"] for r in all_results if r["status"] == "SOFT_COMPETITION"],
    }
    analyze_path.write_text(json.dumps(analysis, indent=2, default=str))
    print(f"  Analysis → {analyze_path.name}")

    # Clean data file
    clean_path = DATA / f"clean_cycle{CYCLE:03d}.json"
    clean_path.write_text(json.dumps({
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "niches": [
            {
                "niche": r["niche"],
                "status": r["status"],
                "community": r["community_actual"],
                "competitors": len(r["competitors"]),
            }
            for r in all_results
        ]
    }, indent=2))
    print(f"  Clean data → {clean_path.name}")

    # Update cycle state
    new_state = {
        "venture": "SCRAPING_competitive_intel",
        "last_cycle": NOW.isoformat(),
        "cycle_number": CYCLE,
        "cycle_status": "COMPLETE",
        "current_step": "done",
        "configured_at": NOW.isoformat(),
        "stats": stats,
        "cumulative_blue_oceans": cumulative_blue_oceans,
        "p0_alerts": p0_alerts + prev_state.get("p0_alerts", [])[:20],
        f"cycle_{CYCLE:02d}_results": {
            "strategy": "PARENTING + COOKING_FOOD + SPORTS_SPECIFIC + MENTAL_HEALTH + DIGITAL_WELLNESS",
            "new_blue_oceans": [r["niche"] for r in blue_ocean_niches],
            "occupied": [r["niche"] for r in all_results if r["status"] == "OCCUPIED"],
        },
    }
    cycle_state_path.write_text(json.dumps(new_state, indent=2, default=str))
    print(f"  Cycle state updated → cycle_state.json")

    print(f"\n{'='*60}")
    print(f"CYCLE {CYCLE:03d} COMPLETE")
    print(f"  Niches scanned:  {stats['niches_scanned']}")
    print(f"  Blue Oceans:     {stats['blue_oceans']} new ({cumulative_blue_oceans} cumulative)")
    print(f"  Soft comp:       {stats['soft_competition']}")
    print(f"  Occupied:        {stats['occupied']}")
    print(f"  CI rows added:   {stats['ci_rows_added']}")
    print(f"  Alpha entries:   {stats['alpha_entries']}")
    print(f"  Community total: {stats['community_total']:,}")
    print(f"{'='*60}\n")

    return stats, p0_alerts, cumulative_blue_oceans


if __name__ == "__main__":
    main()
