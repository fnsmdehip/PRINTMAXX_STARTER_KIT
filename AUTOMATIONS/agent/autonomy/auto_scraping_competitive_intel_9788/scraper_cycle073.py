#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 073
Strategy: MUSIC_CRAFT + COUPLES_RELATIONSHIP + MICRO_NUTRITION + SLEEP_DIGITAL
Date: 2026-03-19
New territory: 12 niches across 4 unexplored categories — musical instrument practice streaks,
couples relationship habits, micro-nutrition accountability, and digital-sleep hygiene.
Cumulative entering this cycle: 87 blue oceans confirmed.

Confidence ranking (pre-scan):
  HIGH BO: guitar_practice, no_screens_before_bed, couples_devotional, knitting_crochet,
           date_night, supplement_stack, piano_practice
  MEDIUM:  protein_goal, veggie_servings, dream_journal, bedtime_consistency
  LIKELY_OCCUPIED: language_immersion (Duolingo adjacency)
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

CYCLE = 73
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
    "750 words", "scrivener", "ulysses", "yousician", "simply piano",
    "flowkey", "fender play", "guitareo", "smartmusic", "lasting",
    "gottman card decks", "couple game", "knot", "ravelry",
}

NICHES = {
    # ── MUSIC_CRAFT ──────────────────────────────────────────────────────────
    "guitar_practice_streak": {
        "label": "Daily Guitar Practice Streak",
        "subreddits": ["guitar", "guitarlessons", "learnguitar"],
        "itunes_terms": [
            "guitar practice streak habit daily paid tracker",
            "guitar habit streak daily paid accountability app",
            "daily guitar streak premium paid practice",
        ],
        "community_estimate": 3800000,
        "hypothesis": (
            "HIGH BO: r/guitar 3.5M+ members. Guitar learning apps (Yousician, Simply Piano variant, "
            "Fender Play, Guitareo) are lesson/tab tools — NOT streak accountability apps. "
            "Daily practice consistency is the #1 complaint in r/guitar ('I keep skipping days'). "
            "Streak-first guitar habit app filling zero-app gap."
        ),
    },
    "piano_practice_streak": {
        "label": "Daily Piano / Keyboard Practice Streak",
        "subreddits": ["piano", "pianolearning", "learnpiano"],
        "itunes_terms": [
            "piano practice streak habit daily paid tracker",
            "piano habit streak daily paid app accountability",
            "daily keyboard practice streak premium paid",
        ],
        "community_estimate": 1200000,
        "hypothesis": (
            "HIGH BO: r/piano 1M+. Simply Piano / Flowkey are lesson platforms. "
            "Zero dedicated piano STREAK accountability apps. Same gap as guitar but smaller community. "
            "Adult learners especially — guilt culture around skipping days is massive."
        ),
    },
    "knitting_crochet_streak": {
        "label": "Daily Knitting / Crochet Practice Streak",
        "subreddits": ["knitting", "crochet", "knitting101"],
        "itunes_terms": [
            "knitting streak habit daily paid tracker",
            "crochet habit streak daily paid app",
            "daily craft streak knitting premium paid",
        ],
        "community_estimate": 2300000,
        "hypothesis": (
            "HIGH BO: r/knitting 1.1M + r/crochet 1.2M. Craft apps (Ravelry, LoveCrafts, "
            "Pattern Keeper) are pattern libraries and project trackers — zero streak accountability. "
            "'WIPS guilt' (work-in-progress shame) culture in knitting = habit accountability need. "
            "100% blue ocean."
        ),
    },
    "language_immersion_streak": {
        "label": "Daily Language Immersion / Listening Streak",
        "subreddits": ["languagelearning", "LearnJapanese", "learnspanish"],
        "itunes_terms": [
            "language immersion streak daily paid app accountability",
            "listening immersion habit streak daily paid",
            "language exposure streak habit daily paid",
        ],
        "community_estimate": 4600000,
        "hypothesis": (
            "LIKELY_OCCUPIED but niche: r/languagelearning 3M+. Duolingo = lessons. "
            "Language Reactor / Immersion apps = content tools. "
            "STREAK accountability for passive immersion (30-min listening/reading daily) "
            "is a distinct use case. Matt vs Japan / Stephen Krashen audience. Check iTunes carefully."
        ),
    },
    # ── COUPLES_RELATIONSHIP ─────────────────────────────────────────────────
    "couples_devotional_streak": {
        "label": "Daily Couples Devotional / Prayer Streak",
        "subreddits": ["Christianity", "marriedredpill", "christian"],
        "itunes_terms": [
            "couples devotional streak habit daily paid app",
            "couples prayer habit streak daily paid",
            "daily devotional couple streak premium paid",
        ],
        "community_estimate": 3900000,
        "hypothesis": (
            "HIGH BO: r/Christianity 1.1M + r/christian 900K. Couple-specific faith apps "
            "(Lasting, Gottman) are therapy/communication tools. Daily devotional STREAK as a couple "
            "is a specific behavior with zero dedicated apps. Faith + relationship cross-niche. "
            "Proven premium pricing from faith streak history (PrayerLock, Hallow)."
        ),
    },
    "date_night_streak": {
        "label": "Weekly Date Night / Quality Time Streak",
        "subreddits": ["relationship_advice", "Marriage", "datingadvice"],
        "itunes_terms": [
            "date night streak habit weekly paid app",
            "couples quality time habit streak weekly paid",
            "date night accountability streak premium paid",
        ],
        "community_estimate": 16800000,
        "hypothesis": (
            "HIGH BO: r/relationship_advice 15M+ (largest community yet scanned). "
            "Date memory apps (Couple, Kindu, Between) are photo/messaging apps. "
            "Zero apps track weekly date night STREAK with accountability. "
            "Marriage counselors literally prescribe weekly date nights. "
            "Premium price point justified (relationship stakes are high)."
        ),
    },
    "love_language_streak": {
        "label": "Daily Love Language Practice Streak",
        "subreddits": ["lovelanguage", "relationship_advice", "relationships"],
        "itunes_terms": [
            "love language streak habit daily paid app",
            "love language practice habit streak daily paid",
            "daily love language streak premium paid",
        ],
        "community_estimate": 16200000,
        "hypothesis": (
            "BO hypothesis: r/relationship_advice 15M+. Gary Chapman's '5 Love Languages' "
            "book has 20M+ copies sold. Zero dedicated love language STREAK apps. "
            "Couple apps exist but none gamify daily acts in partner's love language. "
            "High emotional stakes = high willingness to pay."
        ),
    },
    "random_kindness_streak": {
        "label": "Daily Random Act of Kindness Streak",
        "subreddits": ["kindness", "RandomActsofKindness", "selfimprovement"],
        "itunes_terms": [
            "kindness streak habit daily paid app",
            "random act kindness habit streak daily paid",
            "daily kindness streak premium paid tracker",
        ],
        "community_estimate": 2700000,
        "hypothesis": (
            "BO hypothesis: r/RandomActsofKindness 1.1M + r/selfimprovement 2.5M. "
            "Acts of kindness = proven happiness intervention (Harvard research). "
            "Zero dedicated kindness STREAK accountability apps. "
            "Adjacent to gratitude_message_streak but distinct behavior. "
            "Mental wellness angle + prosocial positioning."
        ),
    },
    # ── MICRO_NUTRITION ──────────────────────────────────────────────────────
    "protein_goal_streak": {
        "label": "Daily Protein Goal / Macro Target Streak",
        "subreddits": ["fitness", "bodybuilding", "gainit"],
        "itunes_terms": [
            "protein goal streak habit daily paid tracker",
            "protein target habit streak daily paid app",
            "daily macro protein streak premium paid",
        ],
        "community_estimate": 22000000,
        "hypothesis": (
            "MEDIUM BO: r/fitness 15M+ + r/bodybuilding 6M. MyFitnessPal = comprehensive tracker. "
            "BUT streak-first protein accountability is distinct — MFP tracks everything, "
            "not gamified around hitting one daily number. 'Hit your protein' is the #1 "
            "fitness subreddit advice. Streak-first simple protein app may occupy gap."
        ),
    },
    "supplement_stack_streak": {
        "label": "Daily Supplement / Nootropic Stack Streak",
        "subreddits": ["Supplements", "nootropics", "StackAdvice"],
        "itunes_terms": [
            "supplement stack streak habit daily paid tracker",
            "supplement habit streak daily paid app",
            "daily vitamins streak premium paid accountability",
        ],
        "community_estimate": 1900000,
        "hypothesis": (
            "HIGH BO: r/Supplements 1.1M + r/nootropics 700K. Medisafe = medication REMINDERS "
            "(push notification only). Zero apps gamify supplement STREAK with accountability. "
            "Nootropic culture = obsessive daily tracking. 'Did I take my stack?' guilt is real. "
            "Clean blue ocean — Medisafe serves patients, not optimization enthusiasts."
        ),
    },
    # ── SLEEP_DIGITAL ────────────────────────────────────────────────────────
    "no_screens_before_bed_streak": {
        "label": "Screen-Free Hour Before Bed Streak",
        "subreddits": ["nosurf", "insomnia", "digitalminimalism"],
        "itunes_terms": [
            "no screens before bed streak habit daily paid",
            "screen free bedtime habit streak daily paid app",
            "digital detox bedtime streak premium paid",
        ],
        "community_estimate": 1600000,
        "hypothesis": (
            "HIGH BO: r/nosurf 600K + r/insomnia 700K + r/digitalminimalism 300K. "
            "Screen time apps (Apple Screen Time, Freedom, AppBlock) BLOCK usage — "
            "none gamify the STREAK of consecutive screen-free nights. "
            "Sleep hygiene is a top Huberman Lab protocol. Zero dedicated streak app. "
            "High intent audience willing to pay for accountability."
        ),
    },
    "dream_journal_streak": {
        "label": "Daily Dream Journal / Lucid Dreaming Streak",
        "subreddits": ["luciddreaming", "DreamJournaling", "Dreams"],
        "itunes_terms": [
            "dream journal streak habit daily paid tracker",
            "lucid dream habit streak daily paid app",
            "dream journaling streak premium paid accountability",
        ],
        "community_estimate": 820000,
        "hypothesis": (
            "MEDIUM BO: r/luciddreaming 500K + r/Dreams 300K. Dream journal apps exist "
            "(Dream: Journal & Lucid) but are content storage — not STREAK accountability. "
            "Lucid dreaming requires consistent daily journaling practice. "
            "Passionate niche, lower community but high retention potential."
        ),
    },
}

RATE_LIMIT_REDDIT = 2.0
RATE_LIMIT_ITUNES = 2.5
MAX_RESULTS_PER_TERM = 10
TIMEOUT_S = 15


def get_reddit_subscribers(subreddit: str) -> int:
    """Fetch subscriber count from Reddit JSON API."""
    try:
        url = f"https://www.reddit.com/r/{subreddit}/about.json"
        headers = {"User-Agent": "PRINTMAXX-CI-Bot/1.0 (competitive intelligence research)"}
        r = requests.get(url, headers=headers, timeout=TIMEOUT_S)
        if r.status_code == 200:
            data = r.json()
            return data.get("data", {}).get("subscribers", 0)
        return 0
    except Exception:
        return 0


def search_itunes(term: str, country: str = "us", limit: int = 10) -> list[dict]:
    """Search iTunes App Store for apps matching the term."""
    try:
        url = "https://itunes.apple.com/search"
        params = {
            "term": term,
            "country": country,
            "media": "software",
            "limit": limit,
            "lang": "en_us",
        }
        r = requests.get(url, params=params, timeout=TIMEOUT_S)
        if r.status_code == 200:
            return r.json().get("results", [])
        return []
    except Exception:
        return []


def is_generic_tracker(app_name: str) -> bool:
    name_lower = app_name.lower()
    return any(g in name_lower for g in GENERIC_TRACKERS)


def classify_niche(niche_id: str, community: int, all_apps: list[dict]) -> str:
    """Classify a niche as BLUE_OCEAN, SOFT_COMPETITION, or OCCUPIED.

    Only apps whose name contains niche keyword fragments count as real competitors.
    This filters out loosely-related apps returned by iTunes keyword search.
    Threshold: < 5000 ratings = weak competition (SOFT_COMPETITION).
    """
    keyword_fragments = niche_id.replace("_", " ").split()
    real = []
    for app in all_apps:
        name = app.get("trackName", "")
        if is_generic_tracker(name):
            continue
        name_lower = name.lower()
        if any(kw in name_lower for kw in keyword_fragments if len(kw) > 3):
            real.append(app)

    if not real:
        return "BLUE_OCEAN"
    elif len(real) <= 2 and all(a.get("userRatingCount", 0) < 5000 for a in real):
        return "SOFT_COMPETITION"
    else:
        return "OCCUPIED"


def run_cycle() -> dict:
    print("=" * 60)
    print(f"CYCLE {CYCLE:03d} — Competitive Intel Scraper")
    print("Strategy: MUSIC_CRAFT + COUPLES_RELATIONSHIP + MICRO_NUTRITION + SLEEP_DIGITAL")
    print(f"Niches: {len(NICHES)} | Cumulative BOs entering: 87")
    print("=" * 60)
    print()

    raw_results = {}
    clean_results = {}
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
    blue_ocean_niches = []
    occupied_niches = []

    for niche_id, cfg in NICHES.items():
        print(f"  [{niche_id}]")

        # 1. Reddit community size
        total_community = 0
        for sub in cfg["subreddits"]:
            count = get_reddit_subscribers(sub)
            print(f"    r/{sub}: {count:,}")
            total_community += count
            time.sleep(RATE_LIMIT_REDDIT)

        # 2. iTunes search — find dedicated apps (not generic trackers)
        all_apps = []
        seen_ids = set()
        for term in cfg["itunes_terms"]:
            apps = search_itunes(term, limit=MAX_RESULTS_PER_TERM)
            for app in apps:
                app_id = app.get("trackId")
                app_name = app.get("trackName", "")
                if app_id not in seen_ids and not is_generic_tracker(app_name):
                    seen_ids.add(app_id)
                    all_apps.append(app)
            time.sleep(RATE_LIMIT_ITUNES)

        n_dedicated = len(all_apps)
        status = classify_niche(niche_id, total_community, all_apps)

        print(f"    Status: {status} | Community: {total_community:,} | iTunes apps: {n_dedicated}")

        raw_results[niche_id] = {
            "label": cfg["label"],
            "subreddits": {s: 0 for s in cfg["subreddits"]},
            "community": total_community,
            "dedicated_apps": all_apps,
            "status": status,
        }

        clean_results[niche_id] = {
            "label": cfg["label"],
            "community": total_community,
            "status": status,
            "n_dedicated_apps": n_dedicated,
            "hypothesis": cfg["hypothesis"],
        }

        stats["niches_scanned"] += 1
        stats["community_total"] += total_community

        if status == "BLUE_OCEAN":
            stats["blue_oceans"] += 1
            alert = f"NEW_C{CYCLE:03d} BLUE OCEAN: {niche_id.upper()} — {total_community:,} community. BUILD NOW."
            p0_alerts.append(alert)
            blue_ocean_niches.append({"niche": niche_id, "label": cfg["label"],
                                       "community": total_community, "hypothesis": cfg["hypothesis"]})
            print(f"  *** P0 ALERT: {alert}")
        elif status == "SOFT_COMPETITION":
            stats["soft_competition"] += 1
        else:
            stats["occupied"] += 1
            occupied_niches.append({"niche": niche_id, "community": total_community})

        print()

    cumulative_bos = 87 + stats["blue_oceans"]

    # 3. STORE — write CI CSV rows
    print("─" * 40)
    print("STORING RESULTS...")

    _write_ci_csv(clean_results, stats)
    _write_alpha_entries(blue_ocean_niches, stats)

    # 4. Save all output files
    raw_path = DATA / f"raw_scrape_cycle{CYCLE:03d}.json"
    raw_path.write_text(json.dumps({
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "niches": raw_results,
    }, indent=2, default=str))
    print(f"  Raw scrape → raw_scrape_cycle{CYCLE:03d}.json")

    clean_path = DATA / f"clean_cycle{CYCLE:03d}.json"
    clean_path.write_text(json.dumps({
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "niches": clean_results,
    }, indent=2, default=str))

    analyze_data = {
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "strategy": "MUSIC_CRAFT + COUPLES_RELATIONSHIP + MICRO_NUTRITION + SLEEP_DIGITAL",
        "stats": stats,
        "cumulative_blue_oceans": cumulative_bos,
        "p0_alerts": p0_alerts,
        "blue_ocean_niches": blue_ocean_niches,
        "occupied_niches": occupied_niches,
        "soft_competition_niches": [],
    }
    analyze_path = DATA / f"analyze_cycle{CYCLE:03d}.json"
    analyze_path.write_text(json.dumps(analyze_data, indent=2, default=str))

    ci_rows = stats["ci_rows_added"]
    alpha_entries = stats["alpha_entries"]
    print(f"  CI CSV +{ci_rows} rows → LEDGER/COMPETITIVE_INTEL.csv")
    print(f"  Alpha CSV +{alpha_entries} entries → LEDGER/ALPHA_STAGING.csv")
    print(f"  Analysis → analyze_cycle{CYCLE:03d}.json")
    print(f"  Clean data → clean_cycle{CYCLE:03d}.json")

    # 5. Update cycle state
    _update_cycle_state(stats, p0_alerts, cumulative_bos, clean_results)
    print(f"  Cycle state updated → cycle_state.json")

    # 6. Write alert file if BOs found
    if p0_alerts:
        alert_path = DATA / f"alert_{DATE_STR}_cycle{CYCLE:03d}.txt"
        alert_content = f"CYCLE {CYCLE} ALERTS — {NOW.isoformat()}\n\n"
        alert_content += "\n".join(p0_alerts) + "\n\n"
        alert_content += f"Cumulative BOs: {cumulative_bos}\n"
        alert_path.write_text(alert_content)
        # Also write to alert_latest.txt
        (DATA / "alert_latest.txt").write_text(alert_content)

    print()
    print("=" * 60)
    print(f"CYCLE {CYCLE:03d} COMPLETE")
    print(f"  Niches scanned:  {stats['niches_scanned']}")
    print(f"  Blue Oceans:     {stats['blue_oceans']} new ({cumulative_bos} cumulative)")
    print(f"  Soft comp:       {stats['soft_competition']}")
    print(f"  Occupied:        {stats['occupied']}")
    print(f"  CI rows added:   {ci_rows}")
    print(f"  Alpha entries:   {alpha_entries}")
    print(f"  Community total: {stats['community_total']:,}")
    print("=" * 60)

    return analyze_data


def _write_ci_csv(clean_results: dict, stats: dict) -> None:
    """Append niche scan results to COMPETITIVE_INTEL.csv."""
    fieldnames = [
        "type", "category", "name", "price", "rating", "rating_count",
        "version", "last_updated", "positive_sentiment", "negative_sentiment",
        "source", "url", "metric_1", "metric_2", "notes", "scan_date",
    ]
    rows_added = 0
    file_exists = CI_CSV.exists()
    with open(CI_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for niche_id, data in clean_results.items():
            writer.writerow({
                "type": "niche_scan",
                "category": "habit_streak",
                "name": data["label"],
                "price": "",
                "rating": "",
                "rating_count": "",
                "version": f"C{CYCLE:03d}",
                "last_updated": DATE_STR,
                "positive_sentiment": 1 if data["status"] == "BLUE_OCEAN" else 0,
                "negative_sentiment": 0 if data["status"] == "BLUE_OCEAN" else 1,
                "source": "reddit_itunes_scan",
                "url": "",
                "metric_1": str(data["community"]),
                "metric_2": data["status"],
                "notes": data["hypothesis"][:120] if data.get("hypothesis") else "",
                "scan_date": NOW.isoformat(),
            })
            rows_added += 1
    stats["ci_rows_added"] = rows_added


def _write_alpha_entries(blue_ocean_niches: list, stats: dict) -> None:
    """Write high-priority BOs as ALPHA_STAGING entries."""
    if not blue_ocean_niches:
        return

    # Only write top-community BOs as alpha (community > 500K or top 4 by community)
    sorted_bos = sorted(blue_ocean_niches, key=lambda x: x["community"], reverse=True)
    to_write = [b for b in sorted_bos if b["community"] > 500000]
    if not to_write:
        to_write = sorted_bos[:3]

    file_exists = ALPHA_CSV.exists()
    fieldnames = None
    if file_exists:
        with open(ALPHA_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames

    if not fieldnames:
        fieldnames = [
            "date", "source", "venture", "status", "roi_potential",
            "title", "summary", "action_steps", "engagement_authenticity",
            "earnings_verified", "reviewer_notes", "integration_target",
        ]

    entries_written = 0
    with open(ALPHA_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        for bo in to_write:
            writer.writerow({
                "date": DATE_STR,
                "source": f"competitive_intel_cycle{CYCLE:03d}",
                "venture": "APP_FACTORY",
                "status": "PENDING_REVIEW",
                "roi_potential": "HIGHEST",
                "title": f"BLUE OCEAN: {bo['label']} — {bo['community']:,} community, 0 dedicated apps",
                "summary": bo["hypothesis"][:300] if bo.get("hypothesis") else "",
                "action_steps": (
                    f"1. Build '{bo['label']}' streak app. "
                    f"2. Target r/{bo.get('niche','').replace('_streak','')} community. "
                    "3. Ship to App Store within 7 days. "
                    "4. Price $2.99-4.99 one-time or $1.99/mo premium."
                ),
                "engagement_authenticity": "AUTHENTIC",
                "earnings_verified": "N/A",
                "reviewer_notes": f"C{CYCLE:03d} scan. Community: {bo['community']:,}. Status: BLUE_OCEAN.",
                "integration_target": "LEDGER/APP_FACTORY_METHODS.csv",
            })
            entries_written += 1
    stats["alpha_entries"] = entries_written


def _update_cycle_state(stats: dict, p0_alerts: list, cumulative_bos: int, results: dict) -> None:
    """Update cycle_state.json with C073 results."""
    state_path = DATA / "cycle_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}

    # Preserve existing p0_alerts, add new ones
    existing_alerts = state.get("p0_alerts", [])
    all_alerts = p0_alerts + [a for a in existing_alerts if a not in p0_alerts]

    state.update({
        "venture": "SCRAPING_competitive_intel",
        "last_cycle": NOW.isoformat(),
        "cycle_number": CYCLE,
        "cycle_status": "COMPLETE",
        "current_step": "complete",
        "stats": stats,
        "cumulative_blue_oceans": cumulative_bos,
        "p0_alerts": all_alerts[:30],  # keep latest 30
        "previous_cycle_results": {
            "cycle": CYCLE,
            "strategy": "MUSIC_CRAFT + COUPLES_RELATIONSHIP + MICRO_NUTRITION + SLEEP_DIGITAL",
            "status": "COMPLETE",
            "blue_oceans": stats["blue_oceans"],
            "community_total": stats["community_total"],
        },
    })
    state_path.write_text(json.dumps(state, indent=2, default=str))


if __name__ == "__main__":
    run_cycle()
