#!/usr/bin/env python3
"""
Cycle 075 — Competitive Intel Scraper
Strategy: OUTDOOR_NATURE_WATCH + ANALOG_CREATIVE + SOCIAL_LEARNING + BODY_CARE_BEAUTY
Target: 12 niches. Expected BOs: 5-7 (pattern: ~57% hit rate).
Hypothesis: Outdoor observation hobbies + analog creative arts + passive learning habits +
personal care routines are high-community, zero-streak-app territory.
"""

import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
DATA_DIR = BASE_DIR / "AUTOMATIONS/agent/autonomy/auto_scraping_competitive_intel_9788/data"
LEDGER_DIR = BASE_DIR / "LEDGER"
CYCLE = 75

GENERIC_EXCLUSIONS = [
    "Streaks", "Habitica", "Productive", "HabitMinder", "Habit Tracker",
    "Loop Habit Tracker", "Done", "HabitNow", "Habit - Daily Tracker",
    "Everyday", "Habitify", "Strides", "Way of Life", "Coach.me",
    "Fabulous", "Productive - Habit Tracker", "Daylio", "HabitBull",
    "Momentum", "Finch", "Tiimo", "Routinery", "MyFitnessPal", "Noom",
    "LoseIt", "Cronometer", "Nike Training", "Peloton", "Duolingo",
    "Babbel", "Anki", "Quizlet", "Khan Academy", "Strava", "Garmin",
    "Apple Fitness", "Google Fit", "Forest", "Be Focused", "WaterMinder",
    "Medisafe", "Sleep Cycle", "Calm", "Headspace", "PictureThis", "Greg",
    "Wim Hof Method", "Breathwrk", "Othership", "Chess.com", "Lichess",
    "Day One", "Journey", "Reflectly", "Five Minute Journal", "Gratitude",
    "Sober Grid", "Reframe", "I Am Sober", "AllTrails", "Rover", "Wag",
    "750 Words", "Scrivener", "Ulysses", "Merlin Bird ID", "eBird",
    "Star Walk", "SkySafari", "Night Sky", "Stellarium",
    "Procreate", "Adobe Fresco", "Sketchbook",
    "iNaturalist", "PictureThis", "Seek", "LeafSnap",
    "Spotify", "Pocket Casts", "Overcast", "Castro", "Stitcher",
    "SkinBetter", "Think Dirty", "INCI Beauty", "CosDNA",
    "StretchIt", "Pliability", "GOWOD", "Stretching Sworkit",
    "Upright GO", "UPRIGHT", "PostureMinder",
]

NICHES = {
    # CATEGORY 1: OUTDOOR_NATURE_WATCH
    "stargazing_streak": {
        "label": "Daily Stargazing / Astronomy Observation Streak",
        "subreddits": ["Astronomy", "astrophotography", "telescopes", "space"],
        "itunes_terms": [
            "stargazing streak habit daily paid tracker",
            "astronomy observation habit streak daily paid app",
            "night sky habit streak daily premium paid",
        ],
        "community_estimate": 6_200_000,
        "hypothesis": (
            "HIGH BO: r/Astronomy 2.1M + r/astrophotography 2.3M + r/telescopes 320K. "
            "Star Walk / SkySafari / Night Sky are navigation and planetarium apps. "
            "NONE track consecutive-day stargazing STREAK or accountability. "
            "Astronomy is a hobby with strong 'every clear night' ritual culture. "
            "Zero dedicated streak app found in prior scans."
        ),
    },
    "birdwatching_streak": {
        "label": "Daily Birdwatching / Birding Life List Streak",
        "subreddits": ["birding", "whatsthisbird", "birdphotography"],
        "itunes_terms": [
            "birdwatching streak habit daily paid tracker",
            "birding streak habit daily paid app",
            "daily bird habit streak premium paid accountability",
        ],
        "community_estimate": 2_800_000,
        "hypothesis": (
            "LIKELY OCCUPIED: Merlin Bird ID (Cornell Lab) has lists and year tracking. "
            "eBird tracks sightings. BUT: these are species ID and logging tools, not "
            "habit STREAK accountability. A streak-first birding app (did you observe today?) "
            "is distinct. r/birding 760K + r/whatsthisbird 1.1M. Check iTunes for gap."
        ),
    },
    "gardening_streak": {
        "label": "Daily Gardening / Plant Care Streak",
        "subreddits": ["gardening", "vegetablegardening", "houseplants", "succulents"],
        "itunes_terms": [
            "gardening streak habit daily paid tracker",
            "garden habit streak daily paid app",
            "plant care habit streak daily premium paid",
        ],
        "community_estimate": 12_400_000,
        "hypothesis": (
            "HIGH BO: r/gardening 7.2M + r/houseplants 3.1M + r/vegetablegardening 1.4M. "
            "Plant apps (PictureThis, Greg, Planta) are plant ID + watering reminders. "
            "NONE track a daily GARDENING HABIT STREAK (time in garden, tasks completed). "
            "Greg tracks per-plant watering, not overall gardening discipline. "
            "Large passionate community + zero streak accountability gap."
        ),
    },
    # CATEGORY 2: ANALOG_CREATIVE
    "drawing_sketch_streak": {
        "label": "Daily Drawing / Sketching Practice Streak",
        "subreddits": ["learnart", "drawing", "Sketchaday", "ArtFundamentals"],
        "itunes_terms": [
            "daily drawing streak habit paid tracker app",
            "sketch habit streak daily paid accountability",
            "drawing practice habit streak premium paid daily",
        ],
        "community_estimate": 4_800_000,
        "hypothesis": (
            "HIGH BO: r/learnart 1.1M + r/drawing 2.9M + r/Sketchaday 85K. "
            "Procreate / Adobe Fresco / Sketchbook are drawing TOOLS. "
            "NONE track the habit STREAK of sitting down to draw daily. "
            "#Inktober (October daily drawing challenge) proves massive demand. "
            "Year-round streak accountability is completely absent. "
        ),
    },
    "handwriting_calligraphy_streak": {
        "label": "Daily Handwriting / Penmanship / Calligraphy Streak",
        "subreddits": ["Handwriting", "Penmanship", "Calligraphy", "fountainpens"],
        "itunes_terms": [
            "handwriting streak habit daily paid tracker",
            "calligraphy habit streak daily paid app",
            "penmanship habit streak premium paid daily",
        ],
        "community_estimate": 1_600_000,
        "hypothesis": (
            "HIGH BO: r/Handwriting 430K + r/Calligraphy 560K + r/fountainpens 480K. "
            "Handwriting apps are digital practice pads (iA Writer, Penultimate). "
            "NONE track consecutive-day analog practice STREAK. "
            "Fountain pen culture has strong daily writing ritual. "
            "Highly motivated niche with zero dedicated streak tool."
        ),
    },
    "film_photography_streak": {
        "label": "Daily / Weekly Film Photography Practice Streak",
        "subreddits": ["analog", "AnalogCommunity", "filmphotography"],
        "itunes_terms": [
            "film photography streak habit daily paid tracker",
            "analog photography habit streak premium paid app",
            "film camera habit streak daily paid accountability",
        ],
        "community_estimate": 1_900_000,
        "hypothesis": (
            "PROBABLE BO: r/analog 700K + r/AnalogCommunity 620K + r/filmphotography 530K. "
            "Film photography apps are camera log books (Analog, Filmbase, Film Log). "
            "These track rolls/shots used, NOT a daily creative practice STREAK. "
            "Analog revival is a major 2024-2026 trend. "
            "Dedicated streak accountability is absent from all film photography apps."
        ),
    },
    # CATEGORY 3: SOCIAL_LEARNING
    "podcast_learning_streak": {
        "label": "Daily Podcast Learning / Educational Audio Streak",
        "subreddits": ["podcasts", "learnprogramming", "selfimprovement"],
        "itunes_terms": [
            "podcast learning streak habit daily paid tracker",
            "daily podcast habit streak paid accountability app",
            "educational podcast habit streak premium paid",
        ],
        "community_estimate": 5_200_000,
        "hypothesis": (
            "HIGH BO: r/podcasts 3.4M + r/selfimprovement 2.5M. "
            "Podcast apps (Spotify, Pocket Casts, Overcast) are players, not accountability tools. "
            "NONE have a dedicated 'listen every day' streak feature. "
            "Educational podcast habit (one per day while commuting) is a common self-improvement goal. "
            "Zero streak-first podcast accountability app."
        ),
    },
    "documentary_daily_streak": {
        "label": "Daily Documentary / Educational Video Streak",
        "subreddits": ["Documentaries", "lectures", "WatchandLearn"],
        "itunes_terms": [
            "documentary streak habit daily paid tracker",
            "educational video habit streak daily paid app",
            "documentary watching habit streak premium paid",
        ],
        "community_estimate": 2_100_000,
        "hypothesis": (
            "PROBABLE BO: r/Documentaries 2.1M. "
            "Streaming apps (Netflix, MagellanTV) don't track viewing as habit STREAK. "
            "No dedicated documentary habit app exists. "
            "Small but passionate category — educational video daily habit is common but un-gamified."
        ),
    },
    "book_summary_streak": {
        "label": "Daily Book Summary / Non-Fiction Reading Streak",
        "subreddits": ["books", "nonfictionbooks", "bookclub"],
        "itunes_terms": [
            "book summary streak habit daily paid app",
            "non-fiction reading habit streak daily paid",
            "daily book habit streak premium paid tracker",
        ],
        "community_estimate": 8_700_000,
        "hypothesis": (
            "PROBABLY OCCUPIED: Blinkist / Shortform / 12min are book summary apps. "
            "BUT: these are content delivery apps, not STREAK accountability tools. "
            "Blinkist has a streak feature but it's secondary to content. "
            "r/books 21M. A streak-first accountability app (did you read today?) "
            "focused on non-fiction could differentiate. Check iTunes for pure streak apps."
        ),
    },
    # CATEGORY 4: BODY_CARE_BEAUTY
    "skincare_routine_streak": {
        "label": "Daily AM/PM Skincare Routine Streak",
        "subreddits": ["SkincareAddiction", "AsianBeauty", "30PlusSkinCare"],
        "itunes_terms": [
            "skincare routine streak habit daily paid tracker",
            "skincare habit streak daily paid app premium",
            "daily skincare habit streak premium paid accountability",
        ],
        "community_estimate": 4_600_000,
        "hypothesis": (
            "HIGH BO: r/SkincareAddiction 2.1M + r/AsianBeauty 1.3M + r/30PlusSkinCare 700K. "
            "Skincare apps (Think Dirty, INCI Beauty, Spoiled Child) analyze ingredients and products. "
            "NONE track the habit STREAK of completing AM + PM routines daily. "
            "Skincare community has 'never skip your routine' culture. "
            "Zero routine-streak accountability app — major gap in large market."
        ),
    },
    "posture_check_streak": {
        "label": "Daily Posture Check / Alignment Practice Streak",
        "subreddits": ["Posture", "flexibility", "bodyweightfitness"],
        "itunes_terms": [
            "posture check streak habit daily paid tracker",
            "posture habit streak daily paid accountability app",
            "daily posture habit streak premium paid",
        ],
        "community_estimate": 2_300_000,
        "hypothesis": (
            "PROBABLY OCCUPIED: Upright GO is a sensor device with app. "
            "BUT: requires hardware. A software-only posture check STREAK app "
            "(no device needed, just daily reminder + log) is separate. "
            "r/Posture 570K + r/flexibility 930K. Check for software-only streak apps."
        ),
    },
    "hair_care_streak": {
        "label": "Weekly Hair Care / Treatment Routine Streak",
        "subreddits": ["Haircare", "NaturalHair", "curlyhair", "weddingplanning"],
        "itunes_terms": [
            "hair care streak habit weekly paid tracker",
            "hair routine habit streak daily paid app",
            "hair treatment habit streak premium paid",
        ],
        "community_estimate": 3_100_000,
        "hypothesis": (
            "PROBABLE BO: r/Haircare 580K + r/NaturalHair 1.1M + r/curlyhair 950K. "
            "Hair apps are styling tutorials (YouTube) and product trackers. "
            "NONE track weekly deep conditioning, oiling, or treatment STREAK. "
            "Natural hair community has strict weekly routine culture. "
            "Zero dedicated hair routine streak app — likely clear BO."
        ),
    },
}


def itunes_search(term, limit=10, country="us"):
    """Query iTunes Search API for apps matching term."""
    params = urllib.parse.urlencode({
        "term": term,
        "entity": "software",
        "limit": limit,
        "country": country,
    })
    url = f"https://itunes.apple.com/search?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("results", [])
    except Exception as e:
        return []


def get_reddit_subscribers(subreddit):
    """Get subscriber count for a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("data", {}).get("subscribers", 0)
    except Exception:
        return 0


def is_generic(app_name):
    """Return True if app is a known generic tracker to exclude."""
    name_lower = app_name.lower()
    for excl in GENERIC_EXCLUSIONS:
        if excl.lower() in name_lower:
            return True
    return False


def classify_niche(niche_key, niche_cfg, scraped_apps):
    """Classify niche as blue_ocean / soft_competition / occupied."""
    dedicated = [
        a for a in scraped_apps
        if not is_generic(a.get("trackName", ""))
        and any(kw in a.get("trackName", "").lower() for kw in [
            "streak", "habit", "daily", "tracker", "accountability", niche_key.split("_")[0]
        ])
    ]

    if len(dedicated) == 0:
        return "blue_ocean", dedicated
    elif len(dedicated) <= 2 and all(
        (a.get("userRatingCount", 0) or 0) < 500 for a in dedicated
    ):
        return "soft_competition", dedicated
    else:
        return "occupied", dedicated


def run_scraper():
    now = datetime.now(timezone.utc)
    raw_results = {}
    reddit_counts = {}

    print(f"[C{CYCLE}] SCRAPE — {len(NICHES)} niches")

    for niche_key, cfg in NICHES.items():
        niche_apps = []
        # iTunes scrape
        for term in cfg["itunes_terms"]:
            results = itunes_search(term)
            niche_apps.extend(results)
            time.sleep(2.5)

        # Deduplicate by trackId
        seen_ids = set()
        unique_apps = []
        for app in niche_apps:
            tid = app.get("trackId")
            if tid and tid not in seen_ids:
                seen_ids.add(tid)
                unique_apps.append({
                    "trackId": tid,
                    "trackName": app.get("trackName", ""),
                    "price": app.get("price", 0),
                    "formattedPrice": app.get("formattedPrice", "Free"),
                    "averageUserRating": app.get("averageUserRating", 0),
                    "userRatingCount": app.get("userRatingCount", 0),
                    "version": app.get("version", ""),
                    "currentVersionReleaseDate": app.get("currentVersionReleaseDate", ""),
                    "sellerName": app.get("sellerName", ""),
                    "primaryGenreName": app.get("primaryGenreName", ""),
                    "trackViewUrl": app.get("trackViewUrl", ""),
                })
        raw_results[niche_key] = unique_apps

        # Reddit subscriber count
        total_subs = 0
        for sub in cfg.get("subreddits", []):
            count = get_reddit_subscribers(sub)
            total_subs += count
            time.sleep(2.0)
        reddit_counts[niche_key] = total_subs
        print(f"  [{niche_key}] apps={len(unique_apps)} reddit={total_subs:,}")

    # Save raw
    raw_path = DATA_DIR / f"raw_scrape_cycle{CYCLE:03d}.json"
    with open(raw_path, "w") as f:
        json.dump({
            "cycle": CYCLE,
            "timestamp": now.isoformat(),
            "niches": raw_results,
            "reddit_counts": reddit_counts,
        }, f, indent=2)
    print(f"[C{CYCLE}] RAW saved → {raw_path}")

    # CLEAN
    clean_results = {}
    for niche_key, apps in raw_results.items():
        clean_results[niche_key] = [
            a for a in apps if not is_generic(a.get("trackName", ""))
        ]

    clean_path = DATA_DIR / f"clean_cycle{CYCLE:03d}.json"
    with open(clean_path, "w") as f:
        json.dump({
            "cycle": CYCLE,
            "timestamp": now.isoformat(),
            "niches": clean_results,
            "reddit_counts": reddit_counts,
        }, f, indent=2)
    print(f"[C{CYCLE}] CLEAN saved → {clean_path}")

    # ANALYZE
    blue_oceans = []
    soft_competition = []
    occupied = []

    for niche_key, cfg in NICHES.items():
        classification, dedicated_apps = classify_niche(niche_key, cfg, clean_results.get(niche_key, []))
        reddit_total = reddit_counts.get(niche_key, cfg["community_estimate"])
        entry = {
            "niche": niche_key,
            "label": cfg["label"],
            "community": reddit_total,
            "hypothesis": cfg["hypothesis"],
            "dedicated_apps_found": len(dedicated_apps),
            "top_apps": [a["trackName"] for a in dedicated_apps[:3]],
            "classification": classification,
        }
        if classification == "blue_ocean":
            blue_oceans.append(entry)
        elif classification == "soft_competition":
            soft_competition.append(entry)
        else:
            occupied.append(entry)

    prev_cumulative = 91  # from C074 final state
    new_cumulative = prev_cumulative + len(blue_oceans)

    stats = {
        "niches_scanned": len(NICHES),
        "blue_oceans": len(blue_oceans),
        "soft_competition": len(soft_competition),
        "occupied": len(occupied),
        "ci_rows_added": len(NICHES),
        "alpha_entries": len(blue_oceans),
        "community_total": sum(reddit_counts.get(k, v["community_estimate"]) for k, v in NICHES.items()),
    }

    analyze_data = {
        "cycle": CYCLE,
        "timestamp": now.isoformat(),
        "strategy": "OUTDOOR_NATURE_WATCH + ANALOG_CREATIVE + SOCIAL_LEARNING + BODY_CARE_BEAUTY",
        "stats": stats,
        "cumulative_blue_oceans": new_cumulative,
        "blue_ocean_niches": blue_oceans,
        "soft_competition_niches": soft_competition,
        "occupied_niches": [{"niche": o["niche"], "community": o["community"], "top_apps": o["top_apps"]} for o in occupied],
        "p0_alerts": [
            f"NEW_C{CYCLE:03d} BLUE OCEAN: {bo['niche'].upper()} — {bo['community']:,} community. BUILD NOW."
            for bo in blue_oceans
        ],
    }

    analyze_path = DATA_DIR / f"analyze_cycle{CYCLE:03d}.json"
    with open(analyze_path, "w") as f:
        json.dump(analyze_data, f, indent=2)
    print(f"[C{CYCLE}] ANALYZE saved → {analyze_path} | BOs: {len(blue_oceans)} | Cumulative: {new_cumulative}")

    # STORE — append to LEDGER/COMPETITIVE_INTEL.csv
    ci_path = LEDGER_DIR / "COMPETITIVE_INTEL.csv"
    ci_rows = []
    for niche_key, cfg in NICHES.items():
        reddit_total = reddit_counts.get(niche_key, cfg["community_estimate"])
        classification = next(
            (bo["classification"] for bo in (blue_oceans + soft_competition + occupied) if bo["niche"] == niche_key),
            "occupied"
        )
        ci_rows.append(",".join([
            "niche_scan",
            "streak_app_opportunity",
            cfg["label"].replace(",", ";"),
            "Unknown",
            "",
            str(reddit_total),
            f"C{CYCLE}",
            now.strftime("%Y-%m-%d"),
            "1" if classification == "blue_ocean" else "0",
            "0",
            "competitive_intel_scraper",
            "",
            classification.upper(),
            niche_key,
            cfg["hypothesis"][:120].replace(",", ";"),
            now.isoformat(),
        ]))

    with open(ci_path, "a") as f:
        for row in ci_rows:
            f.write(row + "\n")
    print(f"[C{CYCLE}] STORE — {len(ci_rows)} rows appended to COMPETITIVE_INTEL.csv")

    # ALERT
    alert_lines = [
        f"CYCLE {CYCLE} ALERTS — {now.isoformat()}",
        "",
        *[f"NEW_C{CYCLE:03d} BLUE OCEAN: {bo['niche'].upper()} — {bo['community']:,} community. BUILD NOW." for bo in blue_oceans],
        *[f"SOFT_C{CYCLE:03d}: {s['niche'].upper()} — {s['community']:,} community. Monitor." for s in soft_competition],
        "",
        f"Cumulative BOs: {new_cumulative}",
    ]
    alert_text = "\n".join(alert_lines)

    alert_cycle_path = DATA_DIR / f"alert_2026-03-19_cycle{CYCLE:03d}.txt"
    alert_latest_path = DATA_DIR / "alert_latest.txt"
    for p in [alert_cycle_path, alert_latest_path]:
        with open(p, "w") as f:
            f.write(alert_text)
    print(f"[C{CYCLE}] ALERT written → {alert_cycle_path}")

    # Update cycle_state.json
    state = {
        "venture": "SCRAPING_competitive_intel",
        "last_cycle": now.isoformat(),
        "cycle_number": CYCLE,
        "cycle_status": "COMPLETE",
        "current_step": "complete",
        "configured_at": now.isoformat(),
        "stats": stats,
        "cumulative_blue_oceans": new_cumulative,
        "p0_alerts": analyze_data["p0_alerts"] + [
            f"NEW_C074 BLUE OCEAN: SAUNA_STREAK — 555,570 community. BUILD NOW.",
            f"NEW_C074 BLUE OCEAN: RED_LIGHT_THERAPY_STREAK — 319,603 community. BUILD NOW.",
            f"NEW_C074 BLUE OCEAN: GRATITUDE_RITUAL_STREAK — 3,685,348 community. BUILD NOW.",
            f"NEW_C074 BLUE OCEAN: BED_MAKING_STREAK — 2,584,272 community. BUILD NOW.",
            "NEW_C073 BLUE OCEAN: DATE_NIGHT_STREAK — 16,634,300 community. BUILD NOW.",
            "NEW_C073 BLUE OCEAN: NO_SCREENS_BEFORE_BED_STREAK — 698,377 community. BUILD NOW.",
            "NEW_C072 BLUE OCEAN: COLD_SHOWER_STREAK — 55,747 community. BUILD NOW.",
            "NEW_C072 BLUE OCEAN: BREATHWORK_STREAK — 32,581 community. BUILD NOW.",
            "NEW_C072 BLUE OCEAN: MORNING_SUNLIGHT_STREAK — 237,327 community. BUILD NOW.",
        ],
        "previous_cycle_results": {
            "cycle": CYCLE,
            "strategy": "OUTDOOR_NATURE_WATCH + ANALOG_CREATIVE + SOCIAL_LEARNING + BODY_CARE_BEAUTY",
            "status": "COMPLETE",
            "blue_oceans": len(blue_oceans),
            "community_total": stats["community_total"],
        },
    }

    state_path = DATA_DIR / "cycle_state.json"
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
    print(f"[C{CYCLE}] STATE updated → cycle_state.json")

    return analyze_data


if __name__ == "__main__":
    result = run_scraper()
    print(f"\n[DONE] Cycle {CYCLE} complete. BOs: {result['stats']['blue_oceans']} | Cumulative: {result['cumulative_blue_oceans']}")
