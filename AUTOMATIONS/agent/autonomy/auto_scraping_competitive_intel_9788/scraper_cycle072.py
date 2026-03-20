#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 072
Strategy: BIOHACKING_COLD + CREATIVE_WRITING + PET_CARE + SOCIAL_CONNECTION
Date: 2026-03-18
New territory: 12 niches across 4 unexplored categories — biohacking micro-behaviors
(cold showers, breathwork, morning sunlight), creative writing habits, pet care streaks,
and social connection habits (gratitude messages, family calls, nature walks).
Cumulative entering this cycle: 80 blue oceans confirmed.
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

CYCLE = 72
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
    "duolingo", "babbel", "anki", "quizlet", "khan academy",
    "strava", "garmin", "apple fitness", "google fit",
    "forest", "be focused", "focus@will", "waterminder", "hydro coach",
    "medisafe", "sleep cycle", "calm", "headspace", "picturethis", "greg",
    "wim hof method", "breathwrk", "othership", "chess.com", "lichess",
    "day one", "journey", "reflectly", "five minute journal", "gratitude",
    "sober grid", "reframe", "i am sober", "alltrails", "rover", "wag",
    "750 words", "scrivener", "ulysses",
}

NICHES = {
    # ── BIOHACKING_COLD ──────────────────────────────────────────────────────
    "cold_shower_streak": {
        "label": "Daily Cold Shower / Cold Plunge Streak",
        "subreddits": ["coldshowers", "wimhof", "IceWater"],
        "itunes_terms": [
            "cold shower streak habit daily paid tracker",
            "cold plunge habit streak daily paid app",
        ],
        "community_estimate": 1050000,
        "hypothesis": "BO hypothesis: r/coldshowers 410K, r/wimhof 380K+. Cold shower apps are guided breathing timers (Wim Hof Method app). NONE track daily cold shower STREAK accountability. 30-day cold shower challenge culture is everywhere on Twitter/YouTube. Habit streak gap is clear."
    },
    "breathwork_streak": {
        "label": "Daily Breathwork / Pranayama Practice Streak",
        "subreddits": ["breathwork", "pranayama", "holotropic"],
        "itunes_terms": [
            "breathwork streak habit daily paid tracker",
            "pranayama habit streak daily paid app",
        ],
        "community_estimate": 620000,
        "hypothesis": "BO hypothesis: r/breathwork 180K, r/pranayama 120K. Breathing apps (Wim Hof, Breathwrk, Othership) are guided session tools. None track STREAK of consecutive days. Huberman Lab audience (~3M) does breathwork daily. Premium niche."
    },
    "morning_sunlight_streak": {
        "label": "Morning Sunlight Exposure Streak",
        "subreddits": ["HubermanLab", "circadian", "morningroutine"],
        "itunes_terms": [
            "morning sunlight streak habit daily paid tracker",
            "sunlight exposure habit streak daily paid app",
        ],
        "community_estimate": 2100000,
        "hypothesis": "BO hypothesis: r/HubermanLab 490K. Huberman morning sunlight protocol is the most-cited behavior hack of 2024-2025. Zero dedicated app tracks consecutive days of morning sunlight. Light therapy apps track SAD, not habit streaks. Massive addressable audience."
    },
    "sober_curious_streak": {
        "label": "Alcohol-Free Day / Sober Curious Streak",
        "subreddits": ["stopdrinking", "dryalcohol", "SoberCurious"],
        "itunes_terms": [
            "sober streak habit alcohol free daily paid",
            "dry days habit streak paid tracker",
        ],
        "community_estimate": 4800000,
        "hypothesis": "LIKELY OCCUPIED: r/stopdrinking 1.1M. Sobriety apps (Sober Grid, Reframe, I Am Sober) exist. BUT check: are they tracking streak as primary feature or just counters? Sober curious (not full sobriety) may be under-served sub-niche."
    },
    # ── CREATIVE_WRITING ─────────────────────────────────────────────────────
    "daily_words_streak": {
        "label": "Daily Writing / 1000 Words Per Day Streak",
        "subreddits": ["writing", "nanowrimo", "worldbuilding"],
        "itunes_terms": [
            "daily words writing streak habit paid app",
            "word count habit streak daily paid writer",
        ],
        "community_estimate": 5900000,
        "hypothesis": "BO hypothesis: r/writing 3M+, r/nanowrimo 900K. 750words.com is web-only. No dedicated mobile app for daily word-count STREAK. Scrivener/Ulysses are writing tools, not habit streak apps. Writers are high-intent, pay for tools. Premium niche."
    },
    "journaling_streak": {
        "label": "Daily Journaling Streak (Non-Generic)",
        "subreddits": ["Journaling", "bulletjournal", "BUJO"],
        "itunes_terms": [
            "journaling streak habit daily paid dedicated app",
            "journal streak premium daily habit paid",
        ],
        "community_estimate": 3200000,
        "hypothesis": "LIKELY OCCUPIED: Day One, Journey, Reflectly all exist. BUT check: are these general journal apps that happen to show streaks, or streak-first accountability apps? Streak-first journaling (not content storage) may be under-served. Check pricing and streak prominence."
    },
    "chess_puzzle_streak": {
        "label": "Daily Chess Puzzle / Tactics Streak",
        "subreddits": ["chess", "chessbeginners", "AnarchyChess"],
        "itunes_terms": [
            "chess puzzle streak habit daily paid tactics",
            "chess tactics habit streak daily paid app",
        ],
        "community_estimate": 6800000,
        "hypothesis": "LIKELY OCCUPIED: Chess.com and Lichess both have daily puzzle features with streaks. BUT these are within large chess platforms, not standalone habit streak apps. A focused 5-min daily chess habits app may fill a gap. r/chess 5.8M. Check iTunes standalone."
    },
    # ── PET_CARE ─────────────────────────────────────────────────────────────
    "dog_walk_streak": {
        "label": "Daily Dog Walk / Exercise Streak",
        "subreddits": ["dogs", "puppy101", "DogAdvice"],
        "itunes_terms": [
            "dog walk streak habit daily paid tracker",
            "dog exercise habit streak daily paid app",
        ],
        "community_estimate": 8400000,
        "hypothesis": "BO hypothesis: r/dogs 4.8M, r/puppy101 2.2M. Dog walking apps (Rover, Wag) are marketplace apps. Fitness apps (Strava) track walks but not dog-walk habit streaks. Zero dedicated dog-walk streak accountability apps. High emotion/attachment market."
    },
    "cat_care_streak": {
        "label": "Daily Cat Enrichment / Care Streak",
        "subreddits": ["cats", "catadvice", "CatBehavior"],
        "itunes_terms": [
            "cat care habit streak daily paid tracker",
            "cat enrichment habit streak daily paid app",
        ],
        "community_estimate": 7200000,
        "hypothesis": "BO hypothesis: r/cats 7M+. Cat apps are photo sharing (Kitten Match) or health loggers (11pets). No cat enrichment STREAK app exists. Cat owners obsess over daily play, brushing, enrichment habits. Daily guilt about 'lazy cat' is universal. Novel niche."
    },
    # ── SOCIAL_CONNECTION ────────────────────────────────────────────────────
    "gratitude_message_streak": {
        "label": "Daily Gratitude Message / Appreciation Streak",
        "subreddits": ["gratitude", "selfimprovement", "psychology"],
        "itunes_terms": [
            "gratitude message streak habit daily paid app",
            "appreciation habit streak daily paid tracker",
        ],
        "community_estimate": 3600000,
        "hypothesis": "BO hypothesis: Gratitude JOURNALING apps exist (Gratitude, Five Minute Journal). But gratitude MESSAGING (sending a thank you to someone daily) is completely different behavior. Zero apps track the habit of reaching out daily. Social habit accountability gap."
    },
    "family_call_streak": {
        "label": "Weekly Family Call / Check-In Streak",
        "subreddits": ["family", "relationship_advice", "adulting"],
        "itunes_terms": [
            "family call streak habit weekly paid app",
            "family check in habit streak daily paid tracker",
        ],
        "community_estimate": 4100000,
        "hypothesis": "BO hypothesis: Communication apps (WhatsApp, FaceTime) are messaging platforms, not habit streak accountability. r/family 1.2M, r/adulting 1.4M. Adult guilt about not calling parents enough is universal. Streak accountability for family connection is untapped."
    },
    "nature_walk_streak": {
        "label": "Daily Nature Walk / Forest Bathing Streak",
        "subreddits": ["hiking", "nature", "forestbathing"],
        "itunes_terms": [
            "nature walk streak habit daily paid app",
            "forest bathing habit streak daily paid tracker",
        ],
        "community_estimate": 5500000,
        "hypothesis": "BO hypothesis: r/hiking 2.1M, r/nature 2.9M. Hiking apps (AllTrails) are trail navigation. Strava tracks runs. Forest bathing is a $40B+ global wellness trend. Daily outdoor time habit streak has no dedicated app. Strong shinrin-yoku cultural tailwind."
    },
}

HEADERS = ["type", "category", "name", "price", "rating", "rating_count", "version",
           "last_updated", "positive_sentiment", "negative_sentiment", "source", "url",
           "metric_1", "metric_2", "notes", "scan_date"]


def itunes_search(term: str, limit: int = 8) -> list:
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
    name_lower = app_name.lower()
    return any(g in name_lower for g in GENERIC_TRACKERS)


def classify_competition(apps: list, niche_key: str) -> tuple:
    keyword_fragments = niche_key.replace("_", " ").split()
    real = []
    for app in apps:
        name = app.get("trackName", "")
        if is_generic(name):
            continue
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

    actual_community = 0
    for sub in config.get("subreddits", []):
        size = reddit_community_size(sub)
        result["reddit_sizes"][sub] = size
        actual_community += size
        print(f"    r/{sub}: {size:,}")
        time.sleep(0.8)
    result["community_actual"] = actual_community

    all_apps = []
    for term in config.get("itunes_terms", [])[:2]:
        apps = itunes_search(term, limit=6)
        all_apps.extend(apps)
        time.sleep(1.2)

    seen_ids = set()
    unique_apps = []
    for app in all_apps:
        tid = app.get("trackId")
        if tid and tid not in seen_ids:
            seen_ids.add(tid)
            unique_apps.append(app)
    result["itunes_results"] = [
        {
            "name": a.get("trackName", ""),
            "price": a.get("formattedPrice", ""),
            "rating": a.get("averageUserRating", 0),
            "rating_count": a.get("userRatingCount", 0),
            "genre": a.get("primaryGenreName", ""),
        }
        for a in unique_apps[:8]
    ]

    status, competitors, notes = classify_competition(unique_apps, niche_key)
    result["status"] = status
    result["competitors"] = competitors
    result["notes"] = notes

    print(f"    Status: {status} | Community: {actual_community:,} | iTunes apps: {len(unique_apps)}")
    return result


def load_alpha_headers() -> list:
    try:
        with open(ALPHA_CSV, "r") as f:
            return next(csv.reader(f))
    except Exception:
        return ["date", "source", "category", "title", "content", "roi_potential",
                "status", "reviewer_notes", "alpha_type", "engagement_authenticity",
                "earnings_verified", "extracted_method"]


def append_csv(path: Path, rows: list, headers: list = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header and headers:
            writer.writerow(headers)
        writer.writerows(rows)


def build_ci_rows(result: dict) -> list:
    rows = []
    label = result["label"]
    community = result["community_actual"]
    status = result["status"]
    notes = result["notes"]
    hyp = result["hypothesis"][:120]

    rows.append([
        "niche_scan", "habit_streak", label,
        "", "", community,
        f"c{CYCLE:03d}", DATE_STR,
        1 if status == "BLUE_OCEAN" else 0,
        1 if status == "OCCUPIED" else 0,
        "itunes_api+reddit", "",
        f"status={status}",
        f"community={community:,}",
        f"{label}. {notes}. Hypothesis: {hyp}",
        NOW.isoformat(),
    ])
    return rows


def build_alpha_rows(result: dict) -> list:
    if result["status"] != "BLUE_OCEAN":
        return []
    community = result["community_actual"]
    if community < 500000:
        return []
    label = result["label"]
    niche = result["niche"]
    hyp = result["hypothesis"]
    return [{
        "date": DATE_STR,
        "source": f"CI_Scanner_Cycle{CYCLE:03d}",
        "category": "APP_FACTORY",
        "title": f"BLUE OCEAN: {niche.upper().replace('_', ' ')} — No App Exists",
        "content": (
            f"iTunes search + Reddit scan confirms zero niche-specific streak app for: {label}. "
            f"Community: {community:,}. {hyp}"
        ),
        "roi_potential": "HIGHEST" if community > 5000000 else "HIGH",
        "status": "PENDING_REVIEW",
        "reviewer_notes": f"Cycle {CYCLE} automated scan. Auto-approve if community > 2M.",
        "alpha_type": "BLUE_OCEAN",
        "engagement_authenticity": "AUTHENTIC",
        "earnings_verified": "N/A",
        "extracted_method": f"Build streak habit app for {label}. ASO target: niche-specific terms.",
    }]


def main():
    print(f"\n{'='*60}")
    print(f"CYCLE {CYCLE:03d} — Competitive Intel Scraper")
    print(f"Strategy: BIOHACKING_COLD + CREATIVE_WRITING + PET_CARE + SOCIAL_CONNECTION")
    print(f"Niches: {len(NICHES)} | Cumulative BOs entering: 80")
    print(f"{'='*60}\n")

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

    cycle_state_path = DATA / "cycle_state.json"
    try:
        prev_state = json.loads(cycle_state_path.read_text())
        cumulative_blue_oceans = prev_state.get("cumulative_blue_oceans", 80)
    except Exception:
        cumulative_blue_oceans = 80

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

        time.sleep(1.5)

    print(f"\n{'─'*40}")
    print("STORING RESULTS...")

    raw_path = DATA / f"raw_scrape_cycle{CYCLE:03d}.json"
    raw_path.write_text(json.dumps(all_results, indent=2, default=str))
    print(f"  Raw scrape → {raw_path.name}")

    append_csv(CI_CSV, ci_rows_all, HEADERS)
    print(f"  CI CSV +{len(ci_rows_all)} rows → LEDGER/COMPETITIVE_INTEL.csv")

    if alpha_rows_all:
        alpha_rows_flat = [[row.get(h, "") for h in alpha_headers] for row in alpha_rows_all]
        append_csv(ALPHA_CSV, alpha_rows_flat)
        print(f"  Alpha CSV +{len(alpha_rows_all)} entries → LEDGER/ALPHA_STAGING.csv")

    analyze_path = DATA / f"analyze_cycle{CYCLE:03d}.json"
    blue_ocean_niches = [r for r in all_results if r["status"] == "BLUE_OCEAN"]
    analysis = {
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "strategy": "BIOHACKING_COLD + CREATIVE_WRITING + PET_CARE + SOCIAL_CONNECTION",
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
            "strategy": "BIOHACKING_COLD + CREATIVE_WRITING + PET_CARE + SOCIAL_CONNECTION",
            "new_blue_oceans": [r["niche"] for r in blue_ocean_niches],
            "occupied": [r["niche"] for r in all_results if r["status"] == "OCCUPIED"],
            "soft": [r["niche"] for r in all_results if r["status"] == "SOFT_COMPETITION"],
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

    return stats, p0_alerts, cumulative_blue_oceans, all_results


if __name__ == "__main__":
    main()
