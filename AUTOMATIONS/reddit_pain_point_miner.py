#!/usr/bin/env python3
"""
REDDIT PAIN POINT MINER - Extracts buying-intent signals from Reddit.

Scans subreddits for posts where users express:
- "I'd pay for..." / "I wish there was..."
- "Is there an app for..." / "Looking for a tool that..."
- "I need help with..." / "Anyone know a service that..."
- Feature requests, complaints about existing tools

These are the highest-signal opportunities for building products
people actually want. Auto-appends to ALPHA_STAGING.csv.

Built: 2026-02-15
Cron: 30 6 * * * python3 AUTOMATIONS/reddit_pain_point_miner.py --scan
"""

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: pip3 install requests")
    sys.exit(1)

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER = PROJECT_ROOT / "LEDGER"
LOGS = PROJECT_ROOT / "AUTOMATIONS" / "logs"
OPS = PROJECT_ROOT / "OPS"

LOGS.mkdir(parents=True, exist_ok=True)

# === BUYING INTENT PATTERNS ===
# Ranked by signal strength (higher = stronger buying intent)

PAIN_PATTERNS = {
    "willing_to_pay": {
        "weight": 100,
        "patterns": [
            r"i('d| would) pay (?:for|good money|anything)",
            r"shut up and take my money",
            r"i('d| would) (?:happily|gladly) pay",
            r"willing to pay",
            r"take my money",
            r"i('ll| will) pay for",
        ]
    },
    "wish_existed": {
        "weight": 90,
        "patterns": [
            r"i wish (?:there was|there were|someone would|I could)",
            r"why (?:isn't|isnt|is there no|doesn't) (?:there|anyone)",
            r"(?:someone|anybody) (?:should|needs to) (?:build|make|create)",
            r"if only (?:there was|there were|someone)",
        ]
    },
    "looking_for": {
        "weight": 80,
        "patterns": [
            r"(?:looking for|searching for|trying to find) (?:a|an|the|some) (?:app|tool|service|software|platform|solution)",
            r"is there (?:a|an|any) (?:app|tool|service|software|platform)",
            r"(?:anyone know|does anyone know) (?:of )?(?:a|an|any) (?:app|tool|service)",
            r"(?:recommend|suggestion) (?:for )?(?:a|an) (?:app|tool|service)",
            r"what (?:app|tool|service|software) do you (?:use|recommend)",
        ]
    },
    "frustrated_with": {
        "weight": 70,
        "patterns": [
            r"(?:so|really|extremely|incredibly) frustrated with",
            r"(?:sick|tired) of (?:using|dealing with|paying for)",
            r"(?:app|tool|service) (?:is|was) (?:terrible|awful|horrible|garbage|trash|broken)",
            r"why (?:is|does) .{5,30} (?:so bad|suck|terrible|not work)",
            r"(?:waste|wasted) (?:of|my) (?:money|time)",
        ]
    },
    "need_help": {
        "weight": 60,
        "patterns": [
            r"(?:need|needs?) (?:help|a solution|something) (?:with|for|to)",
            r"(?:how do|how can) (?:i|you|we) (?:automate|streamline|simplify|solve)",
            r"(?:struggling|having trouble|difficulty) (?:with|finding)",
        ]
    },
    "feature_request": {
        "weight": 50,
        "patterns": [
            r"(?:feature request|would love|would be great|would be nice) (?:if|to (?:have|see|get))",
            r"(?:missing feature|feature .{1,15} missing|no .{1,15} feature)",
            r"(?:can't believe|surprised) (?:there's no|it doesn't|they don't)",
        ]
    }
}

# Subreddits to mine (mix of product-focused and niche-specific)
MINING_SUBREDDITS = {
    # Product/tool discovery subs (highest signal)
    "high_signal": [
        "SaaS", "SideProject", "indiehackers", "Entrepreneur",
        "microsaas", "AppIdeas", "startups", "webdev",
    ],
    # Niche subs where our apps compete
    "app_niches": [
        "productivity", "GetStudying", "nosurf", "digitalminimalism",
        "ADHD", "Fitness", "loseit", "Biohackers", "sleep",
        "Christianity", "islam", "GetDisciplined",
    ],
    # Service/freelance subs
    "services": [
        "smallbusiness", "EntrepreneurRideAlong", "juststart",
        "Affiliatemarketing", "ecommerce",
    ],
}

HEADERS = {
    "User-Agent": "PrintmaxxPainMiner/1.0 (research bot)"
}

RATE_LIMIT = 2.0  # seconds between requests


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    log_file = LOGS / f"pain_miner_{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, "a") as f:
        f.write(line + "\n")


def fetch_subreddit_posts(subreddit, sort="new", limit=25, time_filter="day"):
    """Fetch posts from a subreddit via JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json"
    params = {"limit": limit, "t": time_filter}

    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if resp.status_code == 429:
            log(f"  Rate limited on r/{subreddit}, waiting 10s...", "WARN")
            time.sleep(10)
            resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if resp.status_code != 200:
            log(f"  r/{subreddit} returned {resp.status_code}", "WARN")
            return []

        data = resp.json()
        posts = []
        for child in data.get("data", {}).get("children", []):
            d = child.get("data", {})
            posts.append({
                "subreddit": subreddit,
                "title": d.get("title", ""),
                "selftext": d.get("selftext", "")[:500],
                "score": d.get("score", 0),
                "num_comments": d.get("num_comments", 0),
                "url": f"https://reddit.com{d.get('permalink', '')}",
                "created_utc": d.get("created_utc", 0),
                "author": d.get("author", ""),
            })
        return posts
    except Exception as e:
        log(f"  Error fetching r/{subreddit}: {e}", "ERROR")
        return []


def match_pain_patterns(text):
    """Check text against all pain patterns. Returns matches with weights."""
    text_lower = text.lower()
    matches = []
    for category, config in PAIN_PATTERNS.items():
        for pattern in config["patterns"]:
            if re.search(pattern, text_lower):
                matches.append({
                    "category": category,
                    "weight": config["weight"],
                    "pattern": pattern,
                })
                break  # one match per category is enough
    return matches


def score_opportunity(post, matches):
    """Score a post's opportunity value (0-100)."""
    base = sum(m["weight"] for m in matches) / len(matches) if matches else 0

    # Engagement multiplier
    engagement = post.get("score", 0) + post.get("num_comments", 0) * 2
    if engagement > 50:
        base = min(100, base * 1.3)
    elif engagement > 20:
        base = min(100, base * 1.15)
    elif engagement < 3:
        base = base * 0.85

    return round(base)


def scan_subreddits(sub_list, limit=25, time_filter="day"):
    """Scan a list of subreddits for pain points."""
    all_findings = []

    for sub in sub_list:
        posts = fetch_subreddit_posts(sub, sort="new", limit=limit, time_filter=time_filter)
        time.sleep(RATE_LIMIT)

        for post in posts:
            full_text = f"{post['title']} {post['selftext']}"
            matches = match_pain_patterns(full_text)

            if matches:
                opp_score = score_opportunity(post, matches)
                categories = [m["category"] for m in matches]

                all_findings.append({
                    "subreddit": post["subreddit"],
                    "title": post["title"][:120],
                    "url": post["url"],
                    "score": post["score"],
                    "comments": post["num_comments"],
                    "pain_categories": categories,
                    "opportunity_score": opp_score,
                    "top_pattern": categories[0] if categories else "",
                    "selftext_preview": post["selftext"][:200],
                    "created_utc": post["created_utc"],
                })

    return sorted(all_findings, key=lambda x: x["opportunity_score"], reverse=True)


def run_full_scan():
    """Run full pain point scan across all subreddit categories."""
    log("=" * 60)
    log("REDDIT PAIN POINT MINER - FULL SCAN")
    log("=" * 60)

    start = time.time()
    all_findings = []

    for category, subs in MINING_SUBREDDITS.items():
        log(f"\n  Scanning {category} ({len(subs)} subreddits)...")
        findings = scan_subreddits(subs, limit=25, time_filter="day")
        log(f"  Found {len(findings)} pain points in {category}")
        all_findings.extend(findings)

    # Deduplicate by URL
    seen_urls = set()
    unique = []
    for f in all_findings:
        if f["url"] not in seen_urls:
            seen_urls.add(f["url"])
            unique.append(f)

    unique.sort(key=lambda x: x["opportunity_score"], reverse=True)

    # Save results
    output_file = LEDGER / "REDDIT_PAIN_POINTS.csv"
    if unique:
        fieldnames = [
            "date", "subreddit", "title", "url", "score", "comments",
            "pain_categories", "opportunity_score", "top_pattern", "selftext_preview"
        ]
        # Append mode - add to existing file
        file_exists = output_file.exists()
        with open(output_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for finding in unique:
                writer.writerow({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "subreddit": finding["subreddit"],
                    "title": finding["title"],
                    "url": finding["url"],
                    "score": finding["score"],
                    "comments": finding["comments"],
                    "pain_categories": "|".join(finding["pain_categories"]),
                    "opportunity_score": finding["opportunity_score"],
                    "top_pattern": finding["top_pattern"],
                    "selftext_preview": finding["selftext_preview"][:150],
                })

    # Append high-value findings to ALPHA_STAGING
    append_to_alpha(unique)

    # Generate digest
    digest_path = generate_digest(unique)

    elapsed = time.time() - start

    log("=" * 60)
    log(f"SCAN COMPLETE in {elapsed:.1f}s")
    log(f"  Total pain points found: {len(unique)}")
    log(f"  High opportunity (score >= 70): {len([f for f in unique if f['opportunity_score'] >= 70])}")
    log(f"  Medium (50-69): {len([f for f in unique if 50 <= f['opportunity_score'] < 70])}")
    log(f"  Saved to: {output_file}")
    log(f"  Digest: {digest_path}")
    log("=" * 60)

    return unique


def append_to_alpha(findings):
    """Append high-score findings to ALPHA_STAGING.csv."""
    staging = LEDGER / "ALPHA_STAGING.csv"
    if not staging.exists():
        log("ALPHA_STAGING.csv not found", "WARN")
        return

    high_value = [f for f in findings if f["opportunity_score"] >= 65]
    if not high_value:
        return

    # Get max alpha_id
    max_id = 0
    try:
        with open(staging) as f:
            for row in csv.DictReader(f):
                aid = row.get("alpha_id", "")
                if aid.startswith("ALPHA"):
                    try:
                        max_id = max(max_id, int(aid.replace("ALPHA", "")))
                    except ValueError:
                        continue
    except Exception:
        max_id = 999

    new_entries = []
    for finding in high_value[:10]:  # Max 10 per scan
        max_id += 1
        pattern_label = finding["top_pattern"].replace("_", " ").title()
        new_entries.append({
            "alpha_id": f"ALPHA{max_id:04d}",
            "source": f"r/{finding['subreddit']}",
            "category": "APP_FACTORY",
            "title": f"[Pain Point: {pattern_label}] {finding['title'][:80]}",
            "url": finding["url"],
            "status": "PENDING_REVIEW",
            "roi_potential": "HIGH" if finding["opportunity_score"] >= 80 else "MEDIUM",
            "date_found": datetime.now().strftime("%Y-%m-%d"),
            "reviewer_notes": (
                f"Auto-mined pain point. Score: {finding['opportunity_score']}/100. "
                f"Categories: {', '.join(finding['pain_categories'])}. "
                f"Engagement: {finding['score']}↑ {finding['comments']}💬. "
                f"Preview: {finding['selftext_preview'][:80]}..."
            )
        })

    if new_entries:
        try:
            with open(staging, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(new_entries[0].keys()))
                for entry in new_entries:
                    writer.writerow(entry)
            log(f"  Appended {len(new_entries)} pain point entries to ALPHA_STAGING.csv")
        except Exception as e:
            log(f"  Error appending: {e}", "ERROR")


def generate_digest(findings):
    """Generate daily pain point digest."""
    today = datetime.now().strftime("%Y_%m_%d")
    digest_path = OPS / f"PAIN_POINT_DIGEST_{today}.md"

    lines = [
        "# Reddit Pain Point Digest",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\nTotal pain points found: {len(findings)}",
        "",
        "---",
        "",
    ]

    # High opportunity section
    high = [f for f in findings if f["opportunity_score"] >= 70]
    if high:
        lines.append(f"## HIGH Opportunity ({len(high)} posts, score >= 70)")
        lines.append("")
        for f in high[:15]:
            lines.append(f"### [{f['opportunity_score']}/100] r/{f['subreddit']} ({f['score']}↑ {f['comments']}💬)")
            lines.append(f"**{f['title']}**")
            lines.append(f"Pattern: {f['top_pattern']} | Categories: {', '.join(f['pain_categories'])}")
            if f["selftext_preview"]:
                lines.append(f"> {f['selftext_preview'][:200]}")
            lines.append(f"Link: {f['url']}")
            lines.append("")

    # Medium section
    medium = [f for f in findings if 50 <= f["opportunity_score"] < 70]
    if medium:
        lines.append(f"## MEDIUM Opportunity ({len(medium)} posts, score 50-69)")
        lines.append("")
        for f in medium[:10]:
            lines.append(f"- [{f['opportunity_score']}] r/{f['subreddit']}: {f['title'][:80]} ({f['top_pattern']})")
        lines.append("")

    # Pattern breakdown
    lines.append("## Pattern Breakdown")
    lines.append("")
    pattern_counts = {}
    for f in findings:
        for cat in f["pain_categories"]:
            pattern_counts[cat] = pattern_counts.get(cat, 0) + 1

    lines.append("| Pattern | Count | Signal |")
    lines.append("|---------|-------|--------|")
    for pat, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
        weight = PAIN_PATTERNS.get(pat, {}).get("weight", 0)
        lines.append(f"| {pat} | {count} | {weight}/100 |")
    lines.append("")

    # Action items
    lines.append("## Recommended Actions")
    lines.append("")
    if high:
        lines.append(f"1. REPLY to {len(high)} high-opportunity posts with value-first content")
        lines.append("2. Cross-reference with existing app features to find product-market fit signals")
    if any(f["top_pattern"] == "willing_to_pay" for f in findings):
        pay_posts = [f for f in findings if f["top_pattern"] == "willing_to_pay"]
        lines.append(f"3. URGENT: {len(pay_posts)} posts express willingness to pay - validate demand")
    if any(f["top_pattern"] == "frustrated_with" for f in findings):
        lines.append("4. Competitor weakness detected - check frustrated posts for feature gap opportunities")
    lines.append("")

    with open(digest_path, "w") as f:
        f.write("\n".join(lines))

    log(f"  Digest written to {digest_path}")
    return digest_path


def show_status():
    """Show pain point mining status."""
    print("\n=== REDDIT PAIN POINT MINER STATUS ===\n")

    csv_file = LEDGER / "REDDIT_PAIN_POINTS.csv"
    if csv_file.exists():
        with open(csv_file) as f:
            rows = list(csv.DictReader(f))
        print(f"Total pain points tracked: {len(rows)}")

        # Recent entries
        today = datetime.now().strftime("%Y-%m-%d")
        today_entries = [r for r in rows if r.get("date") == today]
        print(f"Today's findings: {len(today_entries)}")

        # By pattern
        patterns = {}
        for r in rows:
            top = r.get("top_pattern", "unknown")
            patterns[top] = patterns.get(top, 0) + 1
        print("\nBy pattern:")
        for p, c in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
            print(f"  {p}: {c}")

        # High opportunity
        high = [r for r in rows if int(r.get("opportunity_score", 0)) >= 70]
        print(f"\nHigh opportunity (>=70): {len(high)}")
    else:
        print("No data yet. Run --scan first.")

    total_subs = sum(len(v) for v in MINING_SUBREDDITS.values())
    print(f"\nMonitoring {total_subs} subreddits across {len(MINING_SUBREDDITS)} categories")
    print(f"Pattern types: {len(PAIN_PATTERNS)}")
    total_patterns = sum(len(v["patterns"]) for v in PAIN_PATTERNS.values())
    print(f"Total regex patterns: {total_patterns}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Reddit Pain Point Miner - Extract buying intent from Reddit")
    parser.add_argument("--scan", action="store_true", help="Run full pain point scan")
    parser.add_argument("--status", action="store_true", help="Show mining status")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--limit", type=int, default=25, help="Posts per subreddit (default: 25)")
    parser.add_argument("--time", choices=["hour", "day", "week"], default="day", help="Time filter")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.scan:
        results = run_full_scan()
        if args.json:
            # Serialize for JSON output
            for r in results:
                r["pain_categories"] = "|".join(r["pain_categories"])
            print(json.dumps(results[:20], indent=2))
    else:
        parser.print_help()
        print("\n\nExamples:")
        print("  python3 AUTOMATIONS/reddit_pain_point_miner.py --scan           # Full daily scan")
        print("  python3 AUTOMATIONS/reddit_pain_point_miner.py --scan --time week  # Past week")
        print("  python3 AUTOMATIONS/reddit_pain_point_miner.py --status          # Check stats")


if __name__ == "__main__":
    main()
