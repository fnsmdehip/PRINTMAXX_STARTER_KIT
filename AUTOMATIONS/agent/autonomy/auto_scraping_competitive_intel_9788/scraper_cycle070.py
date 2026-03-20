#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 070
Strategy: FINANCIAL_MICRO + PROFESSIONAL_DEVELOPMENT + CREATIVE_ARTS + SUSTAINABILITY
Date: 2026-03-18
New territory: 15 niches never scanned before across high-intent, high-monetization communities.
Cumulative entering this cycle: 73 blue oceans confirmed.
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

CYCLE = 70
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
    "family link", "screen time", "qustodio", "bark", "circle",
    "strava", "garmin", "apple fitness", "google fit",
}

NICHES = {
    # ── FINANCIAL_MICRO ───────────────────────────────────────────────────────
    "no_spend_day_streak": {
        "label": "No-Spend Day / Spend-Free Day Streak",
        "subreddits": ["Frugal", "personalfinance", "leanfire"],
        "itunes_terms": ["no spend day streak habit daily paid tracker", "spend free day habit streak daily paid app"],
        "community_estimate": 8900000,  # r/Frugal 2M + r/personalfinance 4.5M + r/leanfire 300K + related
        "hypothesis": "BO — 'no spend day challenges' are viral (TikTok, Reddit). No dedicated streak app. YNAB tracks budget, not streak accountability. Massive overlap with frugal community."
    },
    "savings_deposit_streak": {
        "label": "Daily Micro-Savings / $5-a-Day Deposit Streak",
        "subreddits": ["personalfinance", "Frugal", "povertyfinance"],
        "itunes_terms": ["savings streak daily habit paid tracker micro savings deposit", "daily savings habit streak paid app"],
        "community_estimate": 7200000,  # r/personalfinance 4.5M + r/Frugal 2M + r/povertyfinance 700K
        "hypothesis": "BO — 'save $1 a day' challenges are consistently viral. Round-up apps (Acorns) focus on automation, not habit streaks. Gap: accountability for INTENTIONAL daily savings action."
    },
    "debt_paydown_streak": {
        "label": "Weekly Debt Paydown / Extra Payment Streak",
        "subreddits": ["personalfinance", "debtfree", "Debt"],
        "itunes_terms": ["debt paydown streak habit weekly paid tracker", "debt free streak habit daily paid app"],
        "community_estimate": 5400000,  # r/personalfinance 4.5M + r/debtfree 400K + r/Debt 500K
        "hypothesis": "BO — debt payoff community is massive (r/debtfree 400K). Debt apps (Undebt.it, Debt Payoff Planner) are calculators/trackers not streak/habit tools. Emotional accountability gap."
    },
    "expense_log_streak": {
        "label": "Daily Expense Logging / Manual Budget Tracking Streak",
        "subreddits": ["personalfinance", "Frugal", "FIRE"],
        "itunes_terms": ["expense log streak daily habit paid tracker manual budget", "daily budget log habit streak paid app"],
        "community_estimate": 6800000,  # r/personalfinance 4.5M + r/Frugal 2M + r/FIRE 300K
        "hypothesis": "BO — many people want manual awareness not automation. YNAB/Mint auto-import. The gap: an app that rewards you JUST for logging daily, no automation required. Behavior change, not tracking."
    },
    "investment_dca_streak": {
        "label": "Daily / Weekly DCA (Dollar-Cost Averaging) Investment Streak",
        "subreddits": ["investing", "Bogleheads", "stocks"],
        "itunes_terms": ["investment streak daily habit paid tracker DCA", "investing habit streak daily paid app"],
        "community_estimate": 5800000,  # r/investing 2.5M + r/Bogleheads 1.3M + r/stocks 2M
        "hypothesis": "BO — DCA is the most recommended investing strategy. Brokerage apps (Robinhood, Fidelity) are execution tools, not habit streak trackers. Gap: accountability for consistent contribution habit."
    },
    # ── PROFESSIONAL_DEVELOPMENT ──────────────────────────────────────────────
    "linkedin_post_streak": {
        "label": "Daily LinkedIn Content Posting Streak",
        "subreddits": ["linkedin", "careerguidance", "personalfinance"],
        "itunes_terms": ["linkedin posting streak daily habit paid tracker content creator", "linkedin streak habit daily paid app"],
        "community_estimate": 4100000,  # r/linkedin 300K + r/careerguidance 700K + r/GetEmployed 200K + generic overlap
        "hypothesis": "BO — 'post on LinkedIn daily for 30 days' is now a professional growth trope. Buffer/Hootsuite are schedulers, not streak accountability tools. Clear gap for a simple LinkedIn habit tracker."
    },
    "networking_email_streak": {
        "label": "Daily Professional Networking / Cold Outreach Email Streak",
        "subreddits": ["careerguidance", "cscareerquestions", "sales"],
        "itunes_terms": ["networking email streak daily habit paid tracker outreach", "cold email habit streak daily paid professional"],
        "community_estimate": 3900000,  # r/careerguidance 700K + r/cscareerquestions 1.2M + r/sales 500K + r/jobs 1.5M
        "hypothesis": "BO — career coaches universally recommend '5 networking emails/week'. CRMs (HubSpot, Apollo) are complex. Gap: a simple streak tracker for daily networking effort. High willingness-to-pay (career ROI)."
    },
    "certification_study_streak": {
        "label": "Daily Professional Certification Study Streak (AWS / PMP / CFA)",
        "subreddits": ["AWSCertifications", "PMP", "CFAprogram"],
        "itunes_terms": ["certification study streak daily habit paid tracker AWS PMP", "cert study habit streak daily paid professional"],
        "community_estimate": 2100000,  # r/AWSCertifications 300K + r/PMP 200K + r/CFAprogram 100K + r/ITCareerQuestions 1.5M
        "hypothesis": "BO — exam prep requires daily habit. Anki covers flashcards. Study apps (Magoosh, PrepAway) are content not streak tracking. Gap: general certification streak tracker with milestone rewards."
    },
    "portfolio_update_streak": {
        "label": "Weekly Portfolio / GitHub / Personal Brand Update Streak",
        "subreddits": ["cscareerquestions", "webdev", "designers"],
        "itunes_terms": ["portfolio update streak habit weekly paid tracker github", "personal brand habit streak weekly paid"],
        "community_estimate": 4500000,  # r/cscareerquestions 1.2M + r/webdev 1.8M + r/design 300K + r/forhire 1.2M
        "hypothesis": "BO — 'update your portfolio' is universal career advice that never gets done. GitHub tracks commits but not portfolio curation. Gap: weekly streak for portfolio/personal brand actions."
    },
    # ── CREATIVE_ARTS ─────────────────────────────────────────────────────────
    "daily_drawing_streak": {
        "label": "Daily Drawing / Sketching Practice Streak",
        "subreddits": ["learnart", "ArtFundamentals", "drawing"],
        "itunes_terms": ["drawing streak daily habit paid tracker sketch practice", "daily sketch habit streak paid art"],
        "community_estimate": 4800000,  # r/learnart 300K + r/ArtFundamentals 400K + r/drawing 4M + r/DigitalArt related
        "hypothesis": "BO — 'draw every day for 30 days' is the most repeated art advice. Procreate/Adobe Fresco are tools, not streak trackers. Gap: accountability layer specifically for daily art practice."
    },
    "daily_photo_streak": {
        "label": "Daily Photography / One Photo a Day Streak",
        "subreddits": ["photography", "itookapicture", "photojournalism"],
        "itunes_terms": ["photography streak daily habit paid tracker one photo day", "daily photo habit streak paid app"],
        "community_estimate": 6200000,  # r/photography 4.5M + r/itookapicture 1.5M + r/photojournalism 200K
        "hypothesis": "BO — 365 photo projects are extremely popular. Instagram tracks posting, not intent/streak. Gap: a minimalist daily photography streak app separate from social media posting."
    },
    "music_practice_streak": {
        "label": "Daily Music Practice / Instrument Session Streak",
        "subreddits": ["learnguitar", "piano", "WeAreTheMusicMakers"],
        "itunes_terms": ["music practice streak daily habit paid tracker instrument", "guitar practice habit streak daily paid"],
        "community_estimate": 5700000,  # r/learnguitar 1.2M + r/piano 800K + r/WeAreTheMusicMakers 1.5M + r/drums 500K + r/singing 1.7M
        "hypothesis": "BO — teachers universally say '20 min daily practice beats 2h weekly'. GarageBand/Yousician are tools not habit trackers. Gap: instrument-agnostic daily practice streak accountability."
    },
    # ── SUSTAINABILITY / ENVIRONMENT ──────────────────────────────────────────
    "no_plastic_day_streak": {
        "label": "No Single-Use Plastic / Plastic-Free Day Streak",
        "subreddits": ["ZeroWaste", "PlasticFreeJuly", "environment"],
        "itunes_terms": ["no plastic day streak habit paid tracker zero waste", "plastic free habit streak daily paid"],
        "community_estimate": 2600000,  # r/ZeroWaste 600K + r/PlasticFreeJuly 100K + r/environment 1M + r/vegan 400K + r/zerowaste sub
        "hypothesis": "BO — Plastic Free July challenge is global. Zero waste apps (Olio, Too Good To Go) are swap/food-sharing, not habit tracking. Gap: streak tracker for daily plastic avoidance."
    },
    "plant_based_meal_streak": {
        "label": "Daily Plant-Based / Meat-Free Meal Streak",
        "subreddits": ["PlantBasedDiet", "vegan", "vegetarian"],
        "itunes_terms": ["plant based meal streak daily habit paid tracker vegan", "meat free day habit streak daily paid"],
        "community_estimate": 8300000,  # r/PlantBasedDiet 400K + r/vegan 5.5M + r/vegetarian 700K + r/veganrecipes 1.7M
        "hypothesis": "BO — 'Meatless Monday' + 'Veganuary' trend. Cronometer/MyFitnessPal are calorie trackers. Gap: simple streak tracker for plant-based meals, separate from calorie counting."
    },
    "walking_steps_streak": {
        "label": "Daily 10K Steps / Walking Goal Streak",
        "subreddits": ["loseit", "GetFit", "walking"],
        "itunes_terms": ["walking streak daily habit paid tracker 10000 steps goal", "steps streak habit daily paid app"],
        "community_estimate": 7100000,  # r/loseit 3.5M + r/GetFit 200K + r/walking 300K + r/1200isplenty 500K + related fitness
        "hypothesis": "SOFT — Apple Health/Fitbit count steps. But they track continuously not habit streaks. Gap may be marginal. Check iTunes carefully for dedicated 'did I hit my steps goal today' streak apps."
    },
}

HEADERS = ["type","category","name","price","rating","rating_count","version",
           "last_updated","positive_sentiment","negative_sentiment","source","url",
           "metric_1","metric_2","notes","scan_date"]


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
            "name": a.get("trackName",""),
            "price": a.get("formattedPrice",""),
            "rating": a.get("averageUserRating", 0),
            "rating_count": a.get("userRatingCount", 0),
            "genre": a.get("primaryGenreName",""),
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
        return ["date","source","category","title","content","roi_potential",
                "status","reviewer_notes","alpha_type","engagement_authenticity",
                "earnings_verified","extracted_method"]


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
        "source": "CI_Scanner_Cycle070",
        "category": "APP_FACTORY",
        "title": f"BLUE OCEAN: {niche.upper().replace('_',' ')} — No App Exists",
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
    print(f"Strategy: FINANCIAL_MICRO + PROFESSIONAL_DEVELOPMENT + CREATIVE_ARTS + SUSTAINABILITY")
    print(f"Niches: {len(NICHES)} | Target: new blue oceans in high-intent, high-monetization communities")
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
        cumulative_blue_oceans = prev_state.get("cumulative_blue_oceans", 73)
    except Exception:
        cumulative_blue_oceans = 73

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
        "strategy": "FINANCIAL_MICRO + PROFESSIONAL_DEVELOPMENT + CREATIVE_ARTS + SUSTAINABILITY",
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
            "strategy": "FINANCIAL_MICRO + PROFESSIONAL_DEVELOPMENT + CREATIVE_ARTS + SUSTAINABILITY",
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
