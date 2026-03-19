#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 068
Strategy: FINANCIAL_WELLNESS + ENTREPRENEURSHIP + ENVIRONMENTAL + CREATIVE_SKILLS
Date: 2026-03-18
Targets: debt payoff streak, no-spend challenge, savings goal streak, cold outreach streak,
         content creation streak, side hustle revenue streak, recycling streak, zero-waste streak,
         composting streak, drawing streak, music practice streak, daily writing streak,
         hand lettering streak, sketching streak
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

CYCLE = 68
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
    "personal capital", "copilot", "clarity money"
}

NICHES = {
    # ── FINANCIAL WELLNESS ───────────────────────────────────────────────────
    "debt_payoff_streak": {
        "label": "Daily Debt Payoff Progress Streak",
        "subreddits": ["personalfinance", "debtfree", "povertyfinance"],
        "itunes_terms": ["debt payoff streak daily habit paid tracker", "debt free streak habit tracker paid daily"],
        "hypothesis": "BO — r/debtfree 400K+, r/povertyfinance 3M+. Debt payoff motivation app distinct from budgeting. Zero dedicated streak for debt-reduction daily action."
    },
    "no_spend_challenge": {
        "label": "No-Spend Day / Challenge Streak Tracker",
        "subreddits": ["nobuy", "personalfinance", "Frugal"],
        "itunes_terms": ["no spend streak daily habit paid tracker", "no spend challenge habit tracker paid"],
        "hypothesis": "BO — r/nobuy 450K+, r/Frugal 2.8M+. No-spend challenges are viral. Zero dedicated streak app vs general spending trackers."
    },
    "savings_goal_streak": {
        "label": "Daily Savings Action / Goal Streak",
        "subreddits": ["personalfinance", "financialindependence", "Frugal"],
        "itunes_terms": ["savings goal streak daily habit paid", "daily savings habit streak tracker paid"],
        "hypothesis": "SOFT — YNAB/Mint track balances. Gap: gamified DAILY SAVINGS ACTION streak (not balance, but act of saving)."
    },
    "invest_daily_streak": {
        "label": "Daily Investing / Dollar-Cost Averaging Streak",
        "subreddits": ["investing", "personalfinance", "stocks"],
        "itunes_terms": ["daily invest streak habit paid tracker", "investing habit streak daily paid dollar cost"],
        "hypothesis": "BO — r/investing 2M+. DCA philosophy = invest daily. Zero streak app for investors vs brokerage apps."
    },
    # ── ENTREPRENEURSHIP / SOLOPRENEUR ───────────────────────────────────────
    "cold_outreach_streak": {
        "label": "Daily Cold Outreach / Sales Activity Streak",
        "subreddits": ["sales", "Entrepreneur", "smallbusiness"],
        "itunes_terms": ["cold outreach streak daily habit paid", "sales activity streak habit tracker paid daily"],
        "hypothesis": "BO — r/sales 300K+, r/Entrepreneur 3M+. 'Send X cold emails/day' is universal advice. Zero dedicated outreach streak app."
    },
    "content_creation_streak": {
        "label": "Daily Content Creation Streak",
        "subreddits": ["NewTubers", "Entrepreneur", "juststart"],
        "itunes_terms": ["content creation streak daily habit paid tracker", "creator streak habit daily paid"],
        "hypothesis": "BO — r/NewTubers 500K+. Creator accountability is huge. Gap between YouTube Studio and a simple streak tracker."
    },
    "side_hustle_streak": {
        "label": "Daily Side Hustle Work / Revenue Activity Streak",
        "subreddits": ["sidehustle", "Entrepreneur", "WorkOnline"],
        "itunes_terms": ["side hustle streak daily habit paid tracker", "hustle habit streak daily paid tracker"],
        "hypothesis": "BO — r/sidehustle 1.5M+. Daily action toward side hustle = distinct accountability gap. No streak app exists."
    },
    "networking_streak": {
        "label": "Daily Professional Networking Streak",
        "subreddits": ["networking", "jobs", "careerguidance"],
        "itunes_terms": ["networking streak daily habit paid tracker", "professional networking habit streak paid"],
        "hypothesis": "BO — r/careerguidance 700K+. 'Reach out to 1 person/day' is standard career advice. Zero streak tracker."
    },
    # ── ENVIRONMENTAL / SUSTAINABILITY ───────────────────────────────────────
    "recycling_streak": {
        "label": "Daily Recycling / Green Action Streak",
        "subreddits": ["ZeroWaste", "environment", "Sustainable"],
        "itunes_terms": ["recycling streak daily habit paid tracker", "green habit streak daily paid eco"],
        "hypothesis": "BO — r/ZeroWaste 1.4M+. Environmental accountability is trending. Zero dedicated recycling streak app."
    },
    "zero_waste_streak": {
        "label": "Daily Zero Waste / Low Impact Habit Streak",
        "subreddits": ["ZeroWaste", "ZeroWasteHome", "environment"],
        "itunes_terms": ["zero waste streak daily habit paid tracker", "low impact habit streak daily paid"],
        "hypothesis": "BO — r/ZeroWaste 1.4M+. Specific zero-waste DAILY habit tracker vs generic habit app = clear gap."
    },
    "plant_based_streak": {
        "label": "Daily Plant-Based / Vegan Meal Streak",
        "subreddits": ["vegan", "plantbased", "veganfitness"],
        "itunes_terms": ["plant based streak daily habit paid tracker", "vegan meal streak daily habit paid"],
        "hypothesis": "SOFT — MyFitnessPal tracks calories. Gap: streak for choosing plant-based meal today (not nutrition, motivation)."
    },
    # ── CREATIVE SKILLS ───────────────────────────────────────────────────────
    "drawing_streak": {
        "label": "Daily Drawing / Sketch Practice Streak",
        "subreddits": ["learnart", "drawing", "sketching"],
        "itunes_terms": ["drawing streak daily habit paid tracker", "sketch habit streak daily paid art practice"],
        "hypothesis": "BO — r/learnart 500K+, r/drawing 2M+. 'Draw every day' is #1 art advice. Zero dedicated drawing streak tracker."
    },
    "music_practice_streak": {
        "label": "Daily Music Practice Streak (Instrument)",
        "subreddits": ["learnmusic", "guitarlessons", "piano"],
        "itunes_terms": ["music practice streak daily habit paid tracker", "instrument practice streak habit daily paid"],
        "hypothesis": "BO — r/guitarlessons 400K+, r/piano 400K+. Practice apps (Yousician) are lesson platforms. Gap: simple streak for ANY instrument."
    },
    "daily_writing_streak": {
        "label": "Daily Writing Practice Streak (Fiction/Non-fiction)",
        "subreddits": ["writing", "worldbuilding", "nanowrimo"],
        "itunes_terms": ["writing streak daily habit paid tracker", "daily writing habit streak paid fiction"],
        "hypothesis": "BO — r/writing 2.5M+, r/nanowrimo 500K+. '1000 words/day' is universal advice. Zero dedicated writing streak tracker."
    },
}


def reddit_community_size(subreddits: list) -> tuple:
    total = 0
    breakdown = {}
    headers = {"User-Agent": "PRINTMAXX-intel-bot/1.0"}
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/about.json"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json().get("data", {})
                subs = data.get("subscribers", 0)
                total += subs
                breakdown[sub] = subs
            elif r.status_code == 429:
                print(f"    [RATE] r/{sub} — backing off 8s")
                time.sleep(8)
            else:
                print(f"    [SKIP] r/{sub} → HTTP {r.status_code}")
            time.sleep(1.2)
        except Exception as e:
            print(f"    [ERR] r/{sub}: {e}")
    return total, breakdown


def itunes_search(terms: list) -> dict:
    found = {}
    for term in terms:
        try:
            url = "https://itunes.apple.com/search"
            params = {"term": term, "entity": "software", "limit": 5, "country": "us"}
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 200:
                results = r.json().get("results", [])
                for app in results:
                    name = app.get("trackName", "").lower()
                    price = app.get("price", 0)
                    rating = app.get("averageUserRating", 0)
                    rating_count = app.get("userRatingCount", 0)
                    found[name] = {
                        "price": price,
                        "rating": rating,
                        "rating_count": rating_count,
                        "genre": app.get("primaryGenreName", ""),
                        "dev": app.get("artistName", ""),
                        "bundle_id": app.get("bundleId", ""),
                        "url": app.get("trackViewUrl", ""),
                    }
            time.sleep(0.8)
        except Exception as e:
            print(f"    [ERR] iTunes '{term}': {e}")
    return found


def classify_competition(niche_key: str, apps: dict) -> str:
    relevant = []
    for name, meta in apps.items():
        name_lower = name.lower()
        if any(g in name_lower for g in GENERIC_TRACKERS):
            continue
        niche_words = set(niche_key.replace("_", " ").split())
        app_words = set(name_lower.split())
        overlap = niche_words & app_words
        if len(overlap) >= 1 and meta["rating_count"] > 100:
            relevant.append((name, meta))

    if not relevant:
        return "BLUE_OCEAN"
    strong = [(n, m) for n, m in relevant if m["rating_count"] > 2000]
    if strong:
        return "OCCUPIED"
    return "SOFT_COMPETITION"


def score_opportunity(community_total: int, status: str, hypothesis: str) -> int:
    base = 0
    if status == "BLUE_OCEAN":
        base = 70
    elif status == "SOFT_COMPETITION":
        base = 45
    else:
        base = 15

    if community_total > 10_000_000:
        base += 25
    elif community_total > 5_000_000:
        base += 18
    elif community_total > 2_000_000:
        base += 12
    elif community_total > 500_000:
        base += 6

    for signal in ["CRITICAL", "MASSIVE", "ZERO dedicated", "zero apps", "Zero apps", "time-sensitive", "distinct"]:
        if signal.lower() in hypothesis.lower():
            base += 3

    return min(base, 100)


def main():
    print(f"\n{'='*60}")
    print(f"COMPETITIVE INTEL CYCLE {CYCLE}")
    print(f"Strategy: FINANCIAL_WELLNESS + ENTREPRENEURSHIP + ENVIRONMENTAL + CREATIVE_SKILLS")
    print(f"Timestamp: {NOW.isoformat()}")
    print(f"{'='*60}\n")

    DATA.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)

    raw_results = {}
    blue_oceans = []
    soft_competition = []
    occupied = []
    ci_rows = []
    alpha_entries = []

    print(f"[CONFIGURE] {len(NICHES)} niches queued for cycle {CYCLE}")

    for niche_key, niche_cfg in NICHES.items():
        label = niche_cfg["label"]
        print(f"\n[SCRAPE] {niche_key}")
        print(f"  Subreddits: {niche_cfg['subreddits']}")

        community_total, breakdown = reddit_community_size(niche_cfg["subreddits"])
        print(f"  Community: {community_total:,} ({breakdown})")

        print(f"  iTunes search: {niche_cfg['itunes_terms'][0][:60]}...")
        apps = itunes_search(niche_cfg["itunes_terms"])
        print(f"  Apps found: {len(apps)}")
        for name, meta in list(apps.items())[:3]:
            print(f"    '{name}' | ${meta['price']} | ★{meta['rating']:.1f} ({meta['rating_count']:,})")

        status = classify_competition(niche_key, apps)
        score = score_opportunity(community_total, status, niche_cfg["hypothesis"])
        print(f"  Status: {status} | Score: {score}")

        raw_results[niche_key] = {
            "label": label,
            "community_total": community_total,
            "community_breakdown": breakdown,
            "apps_found": len(apps),
            "apps": apps,
            "status": status,
            "score": score,
            "hypothesis": niche_cfg["hypothesis"],
        }

        if status == "BLUE_OCEAN":
            blue_oceans.append((niche_key, community_total))
        elif status == "SOFT_COMPETITION":
            soft_competition.append(niche_key)
        else:
            occupied.append(niche_key)

        ci_rows.append([
            "app_gap",
            niche_key.split("_")[0],
            label,
            "paid",
            "",
            community_total,
            f"C{CYCLE:03d}",
            DATE_STR,
            1 if status == "BLUE_OCEAN" else 0,
            0,
            "reddit+itunes",
            f"r/{'+'.join(niche_cfg['subreddits'][:2])}",
            status,
            score,
            niche_cfg["hypothesis"][:120],
            NOW.isoformat(),
        ])

        if status == "BLUE_OCEAN" and community_total > 1_000_000:
            alpha_entries.append({
                "date": DATE_STR,
                "source": f"competitive_intel_cycle_{CYCLE}",
                "venture": "APP_FACTORY",
                "category": "APP_OPPORTUNITY",
                "title": f"BLUE OCEAN [{niche_key.upper()}]: {label}",
                "content": (
                    f"Community: {community_total:,} | "
                    f"Apps found: {len(apps)} (none dominant). "
                    f"{niche_cfg['hypothesis']} "
                    f"Score: {score}/100. Build: streak UI + {label.lower()} context. $2.99-$4.99."
                ),
                "roi_potential": "HIGH",
                "status": "PENDING_REVIEW",
                "score": score,
            })
        elif status == "SOFT_COMPETITION" and community_total > 3_000_000:
            alpha_entries.append({
                "date": DATE_STR,
                "source": f"competitive_intel_cycle_{CYCLE}",
                "venture": "APP_FACTORY",
                "category": "APP_OPPORTUNITY",
                "title": f"NEAR-BO [{niche_key.upper()}]: {label}",
                "content": (
                    f"Community: {community_total:,} | "
                    f"Weak competition. {niche_cfg['hypothesis']} "
                    f"Score: {score}/100."
                ),
                "roi_potential": "MEDIUM",
                "status": "PENDING_REVIEW",
                "score": score,
            })

    # STORE
    print(f"\n[STORE] Writing {len(ci_rows)} rows to COMPETITIVE_INTEL.csv...")
    try:
        with open(CI_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in ci_rows:
                writer.writerow(row)
        print(f"  [OK] {len(ci_rows)} rows appended")
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

    # SAVE DATA FILES
    raw_out = DATA / f"raw_scrape_cycle{CYCLE:03d}.json"
    clean_out = DATA / f"clean_cycle{CYCLE:03d}.json"
    analyze_out = DATA / f"analyze_cycle{CYCLE:03d}.json"

    with open(raw_out, "w") as f:
        json.dump(raw_results, f, indent=2, default=str)

    clean_data = {k: v for k, v in raw_results.items() if v.get("community_total", 0) > 0}
    with open(clean_out, "w") as f:
        json.dump(clean_data, f, indent=2, default=str)

    top_opps = sorted(
        [(k, v["community_total"]) for k, v in raw_results.items()
         if v.get("status") in ("BLUE_OCEAN", "SOFT_COMPETITION")],
        key=lambda x: x[1], reverse=True
    )[:8]

    analyze_data = {
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "strategy": "FINANCIAL_WELLNESS + ENTREPRENEURSHIP + ENVIRONMENTAL + CREATIVE_SKILLS",
        "total_scanned": len(raw_results),
        "blue_oceans": [b[0] for b in blue_oceans],
        "soft_competition": soft_competition,
        "occupied": occupied,
        "top_opportunities": top_opps,
        "blue_ocean_details": {k: {"community": c, "score": raw_results.get(k, {}).get("score", 0)} for k, c in blue_oceans},
    }
    with open(analyze_out, "w") as f:
        json.dump(analyze_data, f, indent=2, default=str)

    print(f"  [OK] Data files saved to data/")

    # UPDATE CYCLE STATE
    try:
        state_path = DATA / "cycle_state.json"
        with open(state_path) as f:
            state = json.load(f)
        prev_bos = state.get("cumulative_blue_oceans", 56)
        prev_p0_alerts = state.get("p0_alerts", [])
    except Exception:
        prev_bos = 56
        prev_p0_alerts = []

    new_total_bos = prev_bos + len(blue_oceans)
    p0_alerts = list(prev_p0_alerts)
    for bo_key, bo_community in sorted(blue_oceans, key=lambda x: x[1], reverse=True):
        label = NICHES[bo_key]["label"]
        alert_str = f"NEW_C068 BLUE OCEAN: {bo_key.upper()} — {bo_community:,} community. BUILD NOW."
        if alert_str not in p0_alerts:
            p0_alerts.insert(0, alert_str)

    near_bos = [
        s for s in soft_competition
        if raw_results.get(s, {}).get("community_total", 0) > 2_000_000
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
            "new_bos_confirmed": len(blue_oceans),
            "soft_competition": len(soft_competition),
            "occupied": len(occupied),
            "alpha_entries": alpha_written,
            "ci_rows_added": len(ci_rows),
            "blue_oceans_confirmed": new_total_bos,
        },
        "cumulative_blue_oceans": new_total_bos,
        "p0_alerts": p0_alerts,
        f"cycle_{CYCLE}_results": {
            "strategy": "FINANCIAL_WELLNESS + ENTREPRENEURSHIP + ENVIRONMENTAL + CREATIVE_SKILLS",
            "new_blue_oceans": [b[0] for b in blue_oceans],
            "near_bos": near_bos,
            "soft_competition": soft_competition,
            "occupied": occupied,
            "biggest_community": sorted(
                [(k, v["community_total"]) for k, v in raw_results.items()],
                key=lambda x: x[1], reverse=True
            )[0] if raw_results else ["N/A", 0],
        },
    }

    with open(DATA / "cycle_state.json", "w") as f:
        json.dump(new_state, f, indent=2, default=str)
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
    print(f"  Blue Oceans:      {len(results['blue_oceans'])}")
    print(f"  Soft Competition: {len(results['soft_competition'])}")
    print(f"  Occupied:         {len(results['occupied'])}")
    print(f"  Cumulative BOs:   {results['new_total_bos']}")
    print(f"  CI rows added:    {results['ci_rows']}")
    print(f"  Alpha entries:    {results['alpha_written']}")
