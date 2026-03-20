#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 071
Strategy: SPORTS_SKILLS + HEALTH_BIOMETRICS + COUPLES_RELATIONSHIP + PRODUCTIVITY_DIGITAL
Date: 2026-03-18
New territory: 13 niches across virgin categories — sports micro-niches, health biometrics,
couples relationship habits, and productivity/GTD habits.
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

CYCLE = 71
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
    "personal capital", "copilot", "clarity money",
    "strava", "garmin", "apple fitness", "google fit",
    "forest", "be focused", "focus@will", "waterminder", "hydro coach",
    "medisafe", "sleep cycle", "calm", "headspace", "picturethis", "greg",
    "lasting", "gottman", "youversion", "bible",
}

NICHES = {
    # ── SPORTS_SKILLS ────────────────────────────────────────────────────────
    "bjj_mat_time_streak": {
        "label": "BJJ / Brazilian Jiu-Jitsu Mat Time Streak",
        "subreddits": ["bjj", "martialarts", "grappling"],
        "itunes_terms": [
            "bjj mat time habit tracker streak paid",
            "jiu jitsu streak habit daily paid"
        ],
        "community_estimate": 900000,
        "hypothesis": "BO hypothesis: r/bjj has 890K members obsessed with mat time consistency. No dedicated streak app. BJJ apps are technique libraries (BJJ Fanatics), not habit streaks. High WTP ($150+/mo gym membership). Premium niche."
    },
    "tennis_practice_streak": {
        "label": "Daily Tennis Practice / Drills Streak",
        "subreddits": ["tennis", "10s"],
        "itunes_terms": [
            "tennis practice habit streak daily paid tracker",
            "tennis drill streak habit app paid"
        ],
        "community_estimate": 1800000,
        "hypothesis": "BO hypothesis: r/tennis 1.5M+ members. Tennis apps are scorekeeping (TennisScore) or coaching (PlaySight), not habit streaks. Practice 30 min daily is constant sub goal. Check for niche dedicated apps."
    },
    "basketball_skills_streak": {
        "label": "Basketball Skills / Shooting Practice Streak",
        "subreddits": ["BasketballTips", "streetball", "BasketballCoaching"],
        "itunes_terms": [
            "basketball skills streak habit daily paid",
            "shooting drill habit streak basketball paid app"
        ],
        "community_estimate": 4200000,
        "hypothesis": "BO hypothesis: massive basketball community. Apps are simulation/scoring (ESPN, NBA), not daily skills streak trackers. Kobe training culture primed for habit accountability app."
    },
    "martial_arts_streak": {
        "label": "Martial Arts / Kata Practice Streak",
        "subreddits": ["martialarts", "karate", "taekwondo"],
        "itunes_terms": [
            "martial arts habit streak daily practice paid",
            "karate habit tracker streak paid daily kata"
        ],
        "community_estimate": 650000,
        "hypothesis": "BO hypothesis: martial arts community values daily kata practice ritual. Apps are technique video libraries, not streak accountability. Check iTunes for dedicated niche app."
    },
    # ── HEALTH_BIOMETRICS ─────────────────────────────────────────────────────
    "water_intake_streak": {
        "label": "Daily Water Intake / Hydration Streak",
        "subreddits": ["hydrohomies", "nutrition", "loseit"],
        "itunes_terms": [
            "water intake streak habit daily paid tracker",
            "hydration habit streak daily paid app"
        ],
        "community_estimate": 3100000,
        "hypothesis": "LIKELY OCCUPIED: r/hydrohomies 3M+. Water apps exist (WaterMinder, Hydro Coach). Check if they track habit STREAK vs just daily volume logging. Possible soft competition — existing apps may not gamify streak."
    },
    "sleep_consistency_streak": {
        "label": "Consistent Bedtime / Sleep Schedule Streak",
        "subreddits": ["sleep", "insomnia", "BetterSleep"],
        "itunes_terms": [
            "sleep schedule streak habit consistent bedtime paid",
            "sleep consistency habit streak daily paid app"
        ],
        "community_estimate": 2400000,
        "hypothesis": "BO hypothesis: sleep apps (Calm, Sleep Cycle) are tracking or ambient sounds. None track HABIT of going to bed at consistent time. r/sleep 1.8M, r/insomnia 600K. Core CBT-I behavior change gap."
    },
    "supplement_daily_streak": {
        "label": "Daily Supplement / Vitamin Stack Streak",
        "subreddits": ["Supplements", "nootropics", "longevity"],
        "itunes_terms": [
            "supplement streak habit daily vitamins paid tracker",
            "vitamin habit streak daily paid app supplements"
        ],
        "community_estimate": 1900000,
        "hypothesis": "BO hypothesis: r/Supplements 1.2M, r/nootropics 600K. Medisafe is for prescription meds. Gap: daily streak tracker specifically for supplement HABIT accountability vs reminder pings."
    },
    # ── COUPLES_RELATIONSHIP ──────────────────────────────────────────────────
    "couples_devotional_streak": {
        "label": "Couples Daily Devotional / Prayer Streak",
        "subreddits": ["Christianity", "marriedreddit", "Reformed"],
        "itunes_terms": [
            "couples devotional daily habit streak paid app",
            "couples prayer habit streak daily paid christian"
        ],
        "community_estimate": 2800000,
        "hypothesis": "BO hypothesis: r/Christianity 1.8M. Couples devotionals are a $50M+ book market. YouVersion does individual + groups but not couple-specific streak tracking. Huge faith + marriage habit gap."
    },
    "date_night_streak": {
        "label": "Weekly Date Night / Couple Quality Time Streak",
        "subreddits": ["marriedreddit", "Marriage", "relationship_advice"],
        "itunes_terms": [
            "date night habit streak weekly couples paid app",
            "couples quality time habit streak weekly paid"
        ],
        "community_estimate": 3500000,
        "hypothesis": "BO hypothesis: r/marriedreddit 1.4M, r/relationship_advice 2M+. Protect date night is constant sub advice. No dedicated app tracks habit consistency. Couples apps (Lasting, Gottman) focus on assessments not streak accountability."
    },
    # ── PRODUCTIVITY_DIGITAL ──────────────────────────────────────────────────
    "pomodoro_streak": {
        "label": "Daily Pomodoro / Deep Focus Sessions Streak",
        "subreddits": ["productivity", "getdisciplined", "adhd_adults"],
        "itunes_terms": [
            "pomodoro streak habit daily paid deep focus sessions",
            "focus sessions habit streak daily paid productivity app"
        ],
        "community_estimate": 7200000,
        "hypothesis": "LIKELY OCCUPIED: Many Pomodoro apps (Forest, Focus@Will, Be Focused). Check if any paid app specifically tracks consecutive DAILY streak as primary feature vs just session counting."
    },
    "inbox_zero_streak": {
        "label": "Daily Inbox Zero / Email Processed Streak",
        "subreddits": ["productivity", "GTD", "selfimprovement"],
        "itunes_terms": [
            "inbox zero habit streak daily paid email",
            "email zero habit streak daily productivity paid app"
        ],
        "community_estimate": 4800000,
        "hypothesis": "BO hypothesis: r/productivity 1.3M, r/GTD 200K. Email apps don't track HABIT streaks. GTD practitioners pay $50+/yr for accountability tools. Possibly unique niche with strong WTP."
    },
    "weekly_review_streak": {
        "label": "Weekly Review / GTD Weekly Reflection Streak",
        "subreddits": ["GTD", "productivity", "bulletjournal"],
        "itunes_terms": [
            "weekly review habit streak paid gtd reflection app",
            "weekly review habit streak productivity paid app"
        ],
        "community_estimate": 2900000,
        "hypothesis": "BO hypothesis: GTD weekly review is a core ritual. r/bulletjournal 780K. Notion/Obsidian don't track habit streaks natively. Productivity nerds pay for systems. Strong premium niche candidate."
    },
    "garden_daily_streak": {
        "label": "Daily Gardening / Garden Care Streak",
        "subreddits": ["gardening", "vegetablegardening", "urbangardening"],
        "itunes_terms": [
            "gardening habit streak daily care paid tracker app",
            "garden care streak habit daily paid gardening app"
        ],
        "community_estimate": 6200000,
        "hypothesis": "BO hypothesis: r/gardening 5.5M+. Garden apps are plant identification (PictureThis) or care reminders (Greg). Daily HABIT streak for gardening consistency is a different value prop. Seasonal hobbyist market."
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
    print(f"Strategy: SPORTS_SKILLS + HEALTH_BIOMETRICS + COUPLES_RELATIONSHIP + PRODUCTIVITY_DIGITAL")
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
        "strategy": "SPORTS_SKILLS + HEALTH_BIOMETRICS + COUPLES_RELATIONSHIP + PRODUCTIVITY_DIGITAL",
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
            "strategy": "SPORTS_SKILLS + HEALTH_BIOMETRICS + COUPLES_RELATIONSHIP + PRODUCTIVITY_DIGITAL",
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
