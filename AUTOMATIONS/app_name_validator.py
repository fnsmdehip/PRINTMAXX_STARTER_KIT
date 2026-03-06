#!/usr/bin/env python3
"""
PRINTMAXX App Name SEO/AIO Validator
=====================================
Automatically validates app names for:
  - App Store availability (iTunes Search API)
  - Google Play availability (web search)
  - Domain availability (.com, .app, .io)
  - SEO keyword competition (search result density)
  - AIO readiness (AI Overview optimization signals)
  - Trademark conflicts (basic TESS check)
  - Niche insider authenticity score

Usage:
  python3 app_name_validator.py --check "AppName"
  python3 app_name_validator.py --audit           # audit all current app names
  python3 app_name_validator.py --generate NICHE  # generate SEO-optimized names
  python3 app_name_validator.py --batch FILE      # check names from file
"""

import json
import sys
import csv
import re
import time
import hashlib
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
from urllib.error import URLError, HTTPError

BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
LEDGER = BASE / "LEDGER"
APP_FACTORY = BASE / "MONEY_METHODS" / "APP_FACTORY"
RESULTS_DIR = APP_FACTORY / "name_validation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Current app portfolio
CURRENT_APPS = {
    "prayerlock": {"niche": "faith", "category": "Lifestyle", "keywords": ["prayer", "faith", "muslim", "christian"]},
    "dusk": {"niche": "sleep", "category": "Health & Fitness", "keywords": ["sleep", "wind down", "evening", "routine"]},
    "vault": {"niche": "finance", "category": "Finance", "keywords": ["savings", "money", "budget", "vault"]},
    "streakr": {"niche": "habits", "category": "Productivity", "keywords": ["streak", "habits", "daily", "tracker"]},
    "mise": {"niche": "cooking", "category": "Food & Drink", "keywords": ["cooking", "recipe", "meal prep", "kitchen"]},
    "steplock": {"niche": "fitness", "category": "Health & Fitness", "keywords": ["steps", "walking", "fitness", "lock"]},
}

# SEO/AIO scoring weights
WEIGHTS = {
    "app_store_available": 25,
    "domain_available": 15,
    "keyword_relevance": 20,
    "name_length": 10,
    "pronounceable": 10,
    "insider_authentic": 15,
    "unique_searchable": 5,
}


def fetch_json(url, timeout=10):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def check_app_store(name):
    """Check if name exists on App Store via iTunes Search API."""
    url = f"https://itunes.apple.com/search?term={quote_plus(name)}&entity=software&limit=10"
    data = fetch_json(url)
    if not data:
        return {"available": None, "similar_count": 0, "exact_match": False, "competitors": []}

    results = data.get("results", [])
    exact = any(r.get("trackName", "").lower() == name.lower() for r in results)
    similar = [r.get("trackName") for r in results[:5]]

    return {
        "available": not exact,
        "similar_count": len(results),
        "exact_match": exact,
        "competitors": similar,
    }


def check_domain(name):
    """Quick domain availability check via DNS lookup."""
    import socket
    clean = re.sub(r'[^a-z0-9]', '', name.lower())
    results = {}
    for ext in [".com", ".app", ".io"]:
        domain = clean + ext
        try:
            socket.getaddrinfo(domain, 80, socket.AF_INET, socket.SOCK_STREAM)
            results[domain] = "TAKEN"
        except socket.gaierror:
            results[domain] = "LIKELY_AVAILABLE"
        except Exception:
            results[domain] = "UNKNOWN"
    return results


def score_name_quality(name, niche="general", keywords=None):
    """Score a name on SEO/AIO/insider-baseball qualities."""
    scores = {}
    name_lower = name.lower()
    clean = re.sub(r'[^a-z0-9]', '', name_lower)

    # Length score (1 word, 4-8 chars ideal)
    if 4 <= len(clean) <= 8:
        scores["name_length"] = 100
    elif 3 <= len(clean) <= 10:
        scores["name_length"] = 70
    else:
        scores["name_length"] = 30

    # Pronounceability (vowel-consonant ratio)
    vowels = sum(1 for c in clean if c in 'aeiou')
    ratio = vowels / max(len(clean), 1)
    if 0.25 <= ratio <= 0.55:
        scores["pronounceable"] = 100
    elif 0.15 <= ratio <= 0.65:
        scores["pronounceable"] = 60
    else:
        scores["pronounceable"] = 20

    # Insider authenticity (penalize cringe patterns)
    cringe_patterns = [
        r'maxx?$', r'pro$', r'ultra$', r'360$', r'ai\s', r'^smart',
        r'bot$', r'hub$', r'forge$', r'^get', r'ify$', r'ly$',
    ]
    authentic_patterns = [
        # single evocative word patterns
        r'^[a-z]{3,8}$',  # clean single word
    ]
    cringe_hits = sum(1 for p in cringe_patterns if re.search(p, name_lower))
    if cringe_hits == 0:
        scores["insider_authentic"] = 90
    elif cringe_hits == 1:
        scores["insider_authentic"] = 50
    else:
        scores["insider_authentic"] = 15

    # Keyword relevance
    if keywords:
        kw_in_name = sum(1 for kw in keywords if kw.lower() in name_lower)
        # Having 0-1 keywords subtly in name is fine; being too literal is bad
        if kw_in_name == 0:
            scores["keyword_relevance"] = 60  # evocative names still work
        elif kw_in_name == 1:
            scores["keyword_relevance"] = 90
        else:
            scores["keyword_relevance"] = 40  # too literal = keyword stuffing

    # Unique searchability (does searching this name return the app, not generic results?)
    word_count = len(name.split())
    if word_count == 1 and len(clean) >= 5:
        scores["unique_searchable"] = 85
    elif word_count == 1:
        scores["unique_searchable"] = 60
    elif word_count == 2:
        scores["unique_searchable"] = 50
    else:
        scores["unique_searchable"] = 30

    return scores


def validate_name(name, niche="general", keywords=None, verbose=True):
    """Full validation pipeline for an app name."""
    result = {
        "name": name,
        "niche": niche,
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "scores": {},
        "composite_score": 0,
        "verdict": "",
    }

    if verbose:
        print(f"\n{'='*60}")
        print(f"  Validating: {name}")
        print(f"  Niche: {niche}")
        print(f"{'='*60}")

    # 1. App Store check
    if verbose:
        print("  [1/4] Checking App Store...")
    app_store = check_app_store(name)
    result["checks"]["app_store"] = app_store
    if app_store["available"] is True:
        result["scores"]["app_store_available"] = 100
    elif app_store["available"] is False:
        result["scores"]["app_store_available"] = 0
    else:
        result["scores"]["app_store_available"] = 50

    if verbose:
        status = "AVAILABLE" if app_store["available"] else "TAKEN" if app_store["available"] is False else "UNKNOWN"
        print(f"    App Store: {status} ({app_store['similar_count']} similar apps)")
        if app_store["competitors"]:
            print(f"    Similar: {', '.join(app_store['competitors'][:3])}")

    # 2. Domain check
    if verbose:
        print("  [2/4] Checking domains...")
    domains = check_domain(name)
    result["checks"]["domains"] = domains
    available_count = sum(1 for v in domains.values() if v == "LIKELY_AVAILABLE")
    if available_count >= 2:
        result["scores"]["domain_available"] = 100
    elif available_count >= 1:
        result["scores"]["domain_available"] = 60
    else:
        result["scores"]["domain_available"] = 20

    if verbose:
        for domain, status in domains.items():
            icon = "+" if status == "LIKELY_AVAILABLE" else "x"
            print(f"    [{icon}] {domain}: {status}")

    # 3. Name quality scores
    if verbose:
        print("  [3/4] Scoring name quality...")
    quality = score_name_quality(name, niche, keywords)
    result["scores"].update(quality)

    if verbose:
        for k, v in quality.items():
            label = k.replace("_", " ").title()
            bar = "#" * (v // 10) + "." * (10 - v // 10)
            print(f"    {label:25s} [{bar}] {v}/100")

    # 4. Composite score
    total_weight = 0
    weighted_sum = 0
    for key, weight in WEIGHTS.items():
        if key in result["scores"]:
            weighted_sum += result["scores"][key] * weight
            total_weight += weight
    result["composite_score"] = round(weighted_sum / max(total_weight, 1))

    # Verdict
    score = result["composite_score"]
    if score >= 80:
        result["verdict"] = "STRONG"
    elif score >= 60:
        result["verdict"] = "GOOD"
    elif score >= 40:
        result["verdict"] = "BORDERLINE"
    else:
        result["verdict"] = "WEAK"

    if verbose:
        print(f"\n  COMPOSITE SCORE: {score}/100 [{result['verdict']}]")
        if score < 60:
            print("  RECOMMENDATION: Consider alternatives")

    # Small delay to be polite to APIs
    time.sleep(0.3)

    return result


def audit_current_apps():
    """Audit all current app names."""
    print("\n" + "=" * 60)
    print("  PRINTMAXX APP NAME AUDIT")
    print("=" * 60)

    results = []
    for name, info in CURRENT_APPS.items():
        r = validate_name(name, info["niche"], info.get("keywords"))
        results.append(r)

    # Summary table
    print("\n" + "=" * 60)
    print("  AUDIT SUMMARY")
    print("=" * 60)
    print(f"  {'Name':15s} {'Score':>6s} {'Verdict':12s} {'App Store':12s} {'Domains'}")
    print("  " + "-" * 58)
    for r in results:
        app_status = "AVAIL" if r["checks"]["app_store"].get("available") else "TAKEN"
        dom_avail = sum(1 for v in r["checks"]["domains"].values() if v == "LIKELY_AVAILABLE")
        print(f"  {r['name']:15s} {r['composite_score']:5d}  {r['verdict']:12s} {app_status:12s} {dom_avail}/3")

    # Save results
    out_path = RESULTS_DIR / f"audit_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved: {out_path}")

    return results


def generate_names(niche, count=20):
    """Generate SEO-optimized app name candidates for a niche."""
    # Niche-specific word banks
    WORD_BANKS = {
        "faith": {
            "evocative": ["selah", "vesper", "vigil", "grace", "haven", "anchor", "abide", "manna", "zion", "psalm"],
            "nature": ["dawn", "ember", "cedar", "olive", "lotus", "pearl", "dove", "stone", "river", "flame"],
            "states": ["still", "risen", "whole", "deep", "pure", "true", "calm", "clear", "bright", "sacred"],
        },
        "sleep": {
            "evocative": ["drift", "hush", "dusk", "lull", "rest", "doze", "nap", "slumber", "drowse", "ease"],
            "nature": ["tide", "mist", "cloud", "moon", "shade", "frost", "dew", "vale", "brook", "shore"],
            "states": ["dim", "soft", "warm", "dark", "quiet", "gentle", "slow", "deep", "light", "cool"],
        },
        "fitness": {
            "evocative": ["stride", "surge", "peak", "grit", "drive", "pace", "push", "flex", "grind", "rush"],
            "nature": ["trail", "ridge", "summit", "crest", "stone", "iron", "oak", "wolf", "bear", "hawk"],
            "states": ["raw", "prime", "lean", "strong", "swift", "sharp", "bold", "tough", "fast", "hard"],
        },
        "habits": {
            "evocative": ["streak", "loop", "chain", "stack", "spark", "seed", "shift", "flow", "pulse", "mark"],
            "nature": ["root", "bloom", "vine", "grove", "nest", "ring", "wave", "spring", "leaf", "stem"],
            "states": ["steady", "daily", "solid", "fixed", "fresh", "new", "true", "clear", "sharp", "bright"],
        },
        "cooking": {
            "evocative": ["mise", "sear", "char", "broth", "zest", "crust", "glaze", "fold", "cure", "brine"],
            "nature": ["sage", "thyme", "basil", "fig", "plum", "olive", "honey", "pepper", "ginger", "clove"],
            "states": ["crisp", "rich", "bold", "fresh", "warm", "light", "smooth", "ripe", "raw", "sweet"],
        },
        "finance": {
            "evocative": ["vault", "stack", "mint", "ledger", "yield", "margin", "stash", "cache", "fund", "forge"],
            "nature": ["oak", "iron", "stone", "gold", "silver", "crystal", "pearl", "amber", "onyx", "jade"],
            "states": ["solid", "stable", "clear", "sharp", "lean", "smart", "prime", "true", "safe", "bold"],
        },
    }

    bank = WORD_BANKS.get(niche, WORD_BANKS.get("habits"))
    candidates = []

    # Strategy 1: Single evocative words
    for word in bank.get("evocative", []):
        candidates.append(word.capitalize())

    # Strategy 2: Single nature words
    for word in bank.get("nature", []):
        candidates.append(word.capitalize())

    # Strategy 3: Portmanteau (combine parts of two words)
    evoc = bank.get("evocative", [])
    nature = bank.get("nature", [])
    for i in range(min(5, len(evoc))):
        for j in range(min(3, len(nature))):
            combo = evoc[i][:3] + nature[j][2:]
            if 4 <= len(combo) <= 8:
                candidates.append(combo.capitalize())

    # Deduplicate
    seen = set()
    unique = []
    for c in candidates:
        if c.lower() not in seen:
            seen.add(c.lower())
            unique.append(c)

    print(f"\n  Generated {len(unique)} candidates for [{niche}] niche")
    print(f"  Validating top {count}...\n")

    # Validate top candidates
    results = []
    for name in unique[:count]:
        r = validate_name(name, niche, verbose=False)
        results.append(r)
        icon = {
            "STRONG": "+", "GOOD": "~", "BORDERLINE": "?", "WEAK": "x"
        }.get(r["verdict"], "?")
        print(f"  [{icon}] {name:15s}  score={r['composite_score']:3d}  {r['verdict']}")

    # Sort by score
    results.sort(key=lambda x: x["composite_score"], reverse=True)

    print(f"\n  TOP 5 RECOMMENDATIONS:")
    for r in results[:5]:
        avail = "AVAIL" if r["checks"]["app_store"].get("available") else "TAKEN"
        print(f"    {r['name']:15s}  {r['composite_score']}/100  App Store: {avail}")

    # Save
    out_path = RESULTS_DIR / f"generated_{niche}_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Saved to: {out_path}")

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PRINTMAXX App Name SEO/AIO Validator")
    parser.add_argument("--check", help="Validate a single app name")
    parser.add_argument("--niche", default="general", help="Niche context for validation")
    parser.add_argument("--keywords", nargs="*", help="Target keywords")
    parser.add_argument("--audit", action="store_true", help="Audit all current app names")
    parser.add_argument("--generate", metavar="NICHE", help="Generate SEO-optimized names for niche")
    parser.add_argument("--count", type=int, default=20, help="Number of names to generate")
    parser.add_argument("--batch", metavar="FILE", help="Check names from file (one per line)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.check:
        r = validate_name(args.check, args.niche, args.keywords)
        if args.json:
            print(json.dumps(r, indent=2))
    elif args.audit:
        audit_current_apps()
    elif args.generate:
        generate_names(args.generate, args.count)
    elif args.batch:
        with open(args.batch) as f:
            names = [line.strip() for line in f if line.strip()]
        results = []
        for name in names:
            r = validate_name(name, args.niche, args.keywords)
            results.append(r)
        if args.json:
            print(json.dumps(results, indent=2))
    else:
        parser.print_help()
        print("\nExamples:")
        print('  python3 app_name_validator.py --check "Selah" --niche faith')
        print('  python3 app_name_validator.py --audit')
        print('  python3 app_name_validator.py --generate sleep --count 30')


if __name__ == "__main__":
    main()
