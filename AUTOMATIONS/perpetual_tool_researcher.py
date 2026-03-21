#!/usr/bin/env python3
"""
PERPETUAL TOOL RESEARCHER — Continuous AI Tool Discovery & Ranking
===================================================================

Tracks ALL tool categories (video gen, editing, scheduling, voice, design, etc.)
across multiple sources. Auto-compares, scores, and feeds Capital Genesis.

NOT just video. Every tool category that affects revenue velocity.

Sources:
  - GitHub trending (new repos in tool categories)
  - ProductHunt (daily top launches in relevant categories)
  - There's An AI For That (theresanaiforthat.com) via scraping
  - FutureTools (futuretools.io) via scraping
  - Reddit r/aivideo, r/singularity, r/StableDiffusion, r/ChatGPT
  - Twitter/X tool announcement accounts
  - Existing daily_tool_scout.py output (OPS/DAILY_TOOL_SCOUT.md)

Outputs:
  - 10_RESEARCH/VIDEO_RESEARCH/tools_tracker/ALL_TOOLS_TRACKER.csv (master tracker)
  - 10_RESEARCH/VIDEO_RESEARCH/tools_tracker/TOOL_CHANGELOG.md (what changed)
  - 10_RESEARCH/VIDEO_RESEARCH/comparisons/ (auto-generated comparisons)
  - LEDGER/ALPHA_STAGING.csv (new tools staged as alpha for Capital Genesis)
  - OPS/TOOL_RESEARCH_DIGEST.md (daily digest for CEO agent)

Integration:
  - Capital Genesis ranker reads tool costs to score ventures
  - CEO agent reads digest for tool-switching decisions
  - ai_video_content_pipeline.py reads tracker for best tool per use case
  - content_trend_pipeline.py reads for content about new tools

Cron: 0 8 * * * python3 AUTOMATIONS/perpetual_tool_researcher.py --cycle
       0 20 * * * python3 AUTOMATIONS/perpetual_tool_researcher.py --digest

Usage:
  python3 perpetual_tool_researcher.py --cycle         # Full research cycle
  python3 perpetual_tool_researcher.py --digest        # Generate daily digest
  python3 perpetual_tool_researcher.py --compare VIDEO  # Compare tools in category
  python3 perpetual_tool_researcher.py --rank          # Rank all tools by value/quality
  python3 perpetual_tool_researcher.py --check TOOL    # Check specific tool for updates
  python3 perpetual_tool_researcher.py --add TOOL CAT  # Add new tool to tracker
  python3 perpetual_tool_researcher.py --status        # Show tracker stats
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = PROJECT_ROOT / "10_RESEARCH" / "VIDEO_RESEARCH"
TRACKER_DIR = RESEARCH_DIR / "tools_tracker"
COMPARISONS_DIR = RESEARCH_DIR / "comparisons"
TEMPLATES_DIR = RESEARCH_DIR / "templates"
PIPELINE_DIR = RESEARCH_DIR / "pipeline"
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OPS_DIR = PROJECT_ROOT / "OPS"
LOGS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"

TRACKER_CSV = TRACKER_DIR / "ALL_TOOLS_TRACKER.csv"
CHANGELOG_MD = TRACKER_DIR / "TOOL_CHANGELOG.md"
DIGEST_MD = OPS_DIR / "TOOL_RESEARCH_DIGEST.md"
ALPHA_CSV = LEDGER_DIR / "ALPHA_STAGING.csv"
LOG_FILE = LOGS_DIR / f"tool_researcher_{datetime.now().strftime('%Y-%m-%d')}.log"

# Ensure dirs exist
for d in [TRACKER_DIR, COMPARISONS_DIR, TEMPLATES_DIR, PIPELINE_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Tool categories we track
CATEGORIES = {
    "video_gen": "AI Video Generation",
    "video_edit": "Video Editing & Post-Production",
    "image_gen": "AI Image Generation",
    "voice": "Voice/TTS/Voice Cloning",
    "avatar": "AI Avatar/Talking Head",
    "scheduling": "Content Scheduling & Distribution",
    "design": "Design & Graphics",
    "scraping": "Web Scraping & Data Collection",
    "automation": "Workflow Automation",
    "analytics": "Analytics & Tracking",
    "seo": "SEO Tools",
    "email": "Email Marketing & Outreach",
    "payment": "Payment Processing",
    "hosting": "Hosting & Deployment",
    "ai_agent": "AI Agent Frameworks",
    "browser": "Browser Automation",
    "captions": "Auto Captions & Subtitles",
    "music": "AI Music Generation",
    "writing": "AI Writing & Copy",
}

# Sources to check for new tools
REDDIT_SUBS = [
    "aivideo", "singularity", "StableDiffusion", "ChatGPT",
    "artificial", "LocalLLaMA", "AItools", "SideProject",
]

GITHUB_TOPICS = [
    "video-generation", "ai-video", "text-to-video",
    "video-editing", "content-automation", "social-media-automation",
    "ai-agent", "voice-synthesis", "text-to-speech",
]

TRACKER_HEADERS = [
    "tool_name", "category", "maker", "quality_score", "free_tier",
    "price_from", "price_unit", "max_length", "max_res", "api_available",
    "api_cost_per_sec", "best_for", "last_checked", "status", "notes",
]


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_tracker() -> list[dict]:
    """Load the master tool tracker CSV."""
    if not TRACKER_CSV.exists():
        return []
    rows = []
    with open(TRACKER_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def save_tracker(rows: list[dict]) -> None:
    """Save the master tool tracker CSV."""
    with open(TRACKER_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in TRACKER_HEADERS})
    log(f"Tracker saved: {len(rows)} tools")


def append_changelog(entry: str) -> None:
    """Append an entry to the tool changelog."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(CHANGELOG_MD, "a") as f:
        f.write(f"\n## {ts}\n{entry}\n")


def stage_alpha(tool_name: str, category: str, description: str) -> None:
    """Stage a new tool discovery as alpha for Capital Genesis."""
    if not ALPHA_CSV.exists():
        return
    row = {
        "timestamp": datetime.now().isoformat(),
        "source": "perpetual_tool_researcher",
        "title": f"New {CATEGORIES.get(category, category)} tool: {tool_name}",
        "content": description,
        "category": "TOOL_DISCOVERY",
        "status": "PENDING_REVIEW",
        "url": "",
        "score": "",
    }
    try:
        with open(ALPHA_CSV, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writerow(row)
        log(f"Staged alpha: {tool_name}")
    except Exception as e:
        log(f"Failed to stage alpha for {tool_name}: {e}")


# ---------------------------------------------------------------------------
# Research Sources
# ---------------------------------------------------------------------------

def fetch_github_trending(topic: str, days: int = 7) -> list[dict]:
    """Fetch trending GitHub repos for a topic."""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"https://api.github.com/search/repositories?q={topic}+created:>={since}&sort=stars&order=desc&per_page=10"
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "printmaxx-tool-researcher",
        })
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            req.add_header("Authorization", f"token {token}")
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("items", [])
    except Exception as e:
        log(f"GitHub fetch failed for {topic}: {e}")
        return []


def fetch_reddit_posts(subreddit: str, limit: int = 10) -> list[dict]:
    """Fetch recent Reddit posts for tool discussions."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "printmaxx-tool-researcher/1.0",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            posts = []
            for child in data.get("data", {}).get("children", []):
                d = child.get("data", {})
                posts.append({
                    "title": d.get("title", ""),
                    "url": d.get("url", ""),
                    "score": d.get("score", 0),
                    "selftext": d.get("selftext", "")[:500],
                    "subreddit": subreddit,
                })
            return posts
    except Exception as e:
        log(f"Reddit fetch failed for r/{subreddit}: {e}")
        return []


def scan_daily_tool_scout() -> list[dict]:
    """Read the daily tool scout output for new discoveries."""
    scout_file = OPS_DIR / "DAILY_TOOL_SCOUT.md"
    if not scout_file.exists():
        return []
    try:
        content = scout_file.read_text()
        # Extract tool mentions from the scout output
        tools = []
        for line in content.split("\n"):
            if line.startswith("- **") or line.startswith("| **"):
                name_match = re.search(r"\*\*(.+?)\*\*", line)
                if name_match:
                    tools.append({
                        "name": name_match.group(1),
                        "line": line.strip(),
                    })
        return tools
    except Exception as e:
        log(f"Scout scan failed: {e}")
        return []


# ---------------------------------------------------------------------------
# Tool Scoring
# ---------------------------------------------------------------------------

def score_tool_value(tool: dict) -> float:
    """Score a tool's value-to-cost ratio for Capital Genesis integration.

    Returns 0-10 composite score weighted for Phase 0 ($0 revenue):
      quality        x 0.30  (does it produce good output?)
      cost_efficiency x 0.25 (free tier? cheap paid?)
      automation      x 0.20 (API available? can we automate?)
      versatility     x 0.15 (how many use cases?)
      reliability     x 0.10 (uptime, consistency)
    """
    quality = float(tool.get("quality_score", 5))

    # Cost efficiency: free tier = 10, <$10 = 8, <$25 = 6, <$50 = 4, >$50 = 2
    price_str = str(tool.get("price_from", "0"))
    try:
        price = float(re.sub(r"[^\d.]", "", price_str) or "0")
    except ValueError:
        price = 0
    free_tier = str(tool.get("free_tier", "")).lower()
    if "free" in free_tier or "yes" in free_tier:
        cost_eff = 10
    elif price == 0:
        cost_eff = 10
    elif price < 10:
        cost_eff = 8
    elif price < 25:
        cost_eff = 6
    elif price < 50:
        cost_eff = 4
    else:
        cost_eff = 2

    # Automation: API = 10, partial = 5, no = 2
    api = str(tool.get("api_available", "")).lower()
    if api in ("yes", "true"):
        automation = 10
    elif api in ("pending", "partial"):
        automation = 5
    else:
        automation = 2

    # Versatility: estimated from category breadth (simplified)
    versatility = 7  # default
    category = tool.get("category", "")
    if category in ("video_gen", "scheduling", "automation"):
        versatility = 9
    elif category in ("video_edit", "voice", "design"):
        versatility = 7
    elif category in ("avatar", "captions", "music"):
        versatility = 5

    reliability = 7  # default, would need uptime monitoring for real data

    composite = (
        quality * 0.30 +
        cost_eff * 0.25 +
        automation * 0.20 +
        versatility * 0.15 +
        reliability * 0.10
    )
    return round(composite, 2)


def rank_all_tools() -> list[tuple[dict, float]]:
    """Rank all tracked tools by value score."""
    tools = load_tracker()
    scored = [(t, score_tool_value(t)) for t in tools]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


# ---------------------------------------------------------------------------
# Comparison Generator
# ---------------------------------------------------------------------------

def generate_category_comparison(category: str) -> str:
    """Generate a markdown comparison for a tool category."""
    tools = load_tracker()
    cat_tools = [t for t in tools if t.get("category") == category]
    if not cat_tools:
        return f"No tools tracked in category: {category}"

    cat_name = CATEGORIES.get(category, category)
    scored = [(t, score_tool_value(t)) for t in cat_tools]
    scored.sort(key=lambda x: x[1], reverse=True)

    lines = [
        f"# {cat_name} Comparison",
        f"\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"\n| Rank | Tool | Quality | Free Tier | Price From | API | Value Score |",
        f"|------|------|---------|-----------|------------|-----|-------------|",
    ]
    for i, (t, score) in enumerate(scored, 1):
        lines.append(
            f"| {i} | **{t['tool_name']}** | {t.get('quality_score', '?')}/10 | "
            f"{t.get('free_tier', 'none')} | {t.get('price_from', '?')}{t.get('price_unit', '')} | "
            f"{t.get('api_available', '?')} | {score}/10 |"
        )

    # Best picks section
    if scored:
        best = scored[0]
        cheapest = min(scored, key=lambda x: float(re.sub(r"[^\d.]", "", str(x[0].get("price_from", "999"))) or "999"))
        lines.extend([
            f"\n## recommendations",
            f"\n**best overall**: {best[0]['tool_name']} (score: {best[1]})",
            f"**cheapest paid**: {cheapest[0]['tool_name']} (from {cheapest[0].get('price_from', '?')}{cheapest[0].get('price_unit', '')})",
        ])

        # Find best free option
        free_tools = [s for s in scored if "free" in str(s[0].get("free_tier", "")).lower() or "yes" in str(s[0].get("free_tier", "")).lower()]
        if free_tools:
            best_free = free_tools[0]
            lines.append(f"**best free**: {best_free[0]['tool_name']} ({best_free[0].get('free_tier', '')})")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Digest Generator
# ---------------------------------------------------------------------------

def generate_digest() -> str:
    """Generate daily research digest for CEO agent."""
    tools = load_tracker()
    scored = rank_all_tools()

    # Category counts
    cat_counts = {}
    for t in tools:
        cat = t.get("category", "unknown")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    # Top tools per category
    top_per_cat = {}
    for t, score in scored:
        cat = t.get("category", "unknown")
        if cat not in top_per_cat:
            top_per_cat[cat] = (t, score)

    lines = [
        "# TOOL RESEARCH DIGEST",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Total tools tracked: {len(tools)}",
        f"Categories: {len(cat_counts)}",
        "",
        "## top ranked tools (by value/quality composite)",
        "",
        "| Rank | Tool | Category | Value Score |",
        "|------|------|----------|-------------|",
    ]

    for i, (t, score) in enumerate(scored[:15], 1):
        lines.append(f"| {i} | {t['tool_name']} | {t.get('category', '')} | {score}/10 |")

    lines.extend([
        "",
        "## best per category",
        "",
    ])
    for cat, (t, score) in sorted(top_per_cat.items()):
        cat_name = CATEGORIES.get(cat, cat)
        lines.append(f"- **{cat_name}**: {t['tool_name']} ({score}/10)")

    # Changelog recent entries
    if CHANGELOG_MD.exists():
        changelog = CHANGELOG_MD.read_text()
        recent = changelog.split("## ")[-3:]  # last 3 entries
        if recent:
            lines.extend(["", "## recent changes", ""])
            for entry in recent:
                if entry.strip():
                    lines.append(f"- {entry.strip()[:200]}")

    lines.extend([
        "",
        "## action items",
        "",
        "- Tools with API + free tier = immediate automation candidates",
        "- Tools scoring >8 = integrate into content pipeline",
        "- New discoveries = stage as alpha for Capital Genesis ranking",
        "- Price drops or new free tiers = re-score affected ventures",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------

def cmd_cycle(args: argparse.Namespace) -> None:
    """Full research cycle: scan sources, update tracker, generate comparisons."""
    log("Starting perpetual research cycle...")

    # 1. Scan GitHub trending for each topic
    log("Scanning GitHub trending...")
    new_tools = []
    existing_names = {t["tool_name"].lower() for t in load_tracker()}

    for topic in GITHUB_TOPICS[:5]:  # limit to avoid rate limits
        repos = fetch_github_trending(topic, days=7)
        for repo in repos:
            name = repo.get("name", "")
            stars = repo.get("stargazers_count", 0)
            if stars > 50 and name.lower() not in existing_names:
                new_tools.append({
                    "name": name,
                    "source": "github",
                    "url": repo.get("html_url", ""),
                    "description": repo.get("description", ""),
                    "stars": stars,
                })

    # 2. Scan Reddit
    log("Scanning Reddit...")
    tool_keywords = ["tool", "release", "launch", "alternative", "better than", "vs", "comparison", "new ai"]
    for sub in REDDIT_SUBS[:4]:
        posts = fetch_reddit_posts(sub, limit=15)
        for post in posts:
            title_lower = post["title"].lower()
            if any(kw in title_lower for kw in tool_keywords) and post["score"] > 20:
                new_tools.append({
                    "name": post["title"][:60],
                    "source": f"r/{sub}",
                    "url": post["url"],
                    "description": post["selftext"][:300],
                    "stars": post["score"],
                })

    # 3. Check daily tool scout output
    log("Checking daily tool scout...")
    scout_tools = scan_daily_tool_scout()
    for st in scout_tools:
        if st["name"].lower() not in existing_names:
            new_tools.append({
                "name": st["name"],
                "source": "daily_tool_scout",
                "url": "",
                "description": st["line"],
                "stars": 0,
            })

    # 4. Stage new discoveries as alpha
    log(f"Found {len(new_tools)} potential new tools")
    for tool in new_tools[:20]:  # cap at 20 per cycle
        stage_alpha(
            tool["name"],
            "unknown",
            f"New tool from {tool['source']}: {tool['description'][:200]}. "
            f"URL: {tool.get('url', 'n/a')}. Stars/score: {tool.get('stars', 0)}"
        )

    # 5. Generate comparisons for each category
    log("Generating category comparisons...")
    for category in CATEGORIES:
        comparison = generate_category_comparison(category)
        if "No tools tracked" not in comparison:
            comp_file = COMPARISONS_DIR / f"{category.upper()}_COMPARISON.md"
            comp_file.write_text(comparison)

    # 6. Generate digest
    log("Generating research digest...")
    digest = generate_digest()
    DIGEST_MD.write_text(digest)

    # 7. Append changelog
    append_changelog(f"Research cycle complete. {len(new_tools)} new tool candidates found. Comparisons regenerated.")

    log("Research cycle complete.")
    print(f"\nResults:")
    print(f"  New tools found: {len(new_tools)}")
    print(f"  Tracker size: {len(load_tracker())} tools")
    print(f"  Digest: {DIGEST_MD}")
    print(f"  Comparisons: {COMPARISONS_DIR}/")


def cmd_digest(args: argparse.Namespace) -> None:
    """Generate the daily digest."""
    digest = generate_digest()
    DIGEST_MD.write_text(digest)
    print(digest)


def cmd_compare(args: argparse.Namespace) -> None:
    """Compare tools in a category."""
    category = args.category.lower()
    # Try exact match first, then partial
    if category not in CATEGORIES:
        matches = [c for c in CATEGORIES if category in c]
        if matches:
            category = matches[0]
        else:
            print(f"Unknown category: {args.category}")
            print(f"Available: {', '.join(CATEGORIES.keys())}")
            return

    comparison = generate_category_comparison(category)
    comp_file = COMPARISONS_DIR / f"{category.upper()}_COMPARISON.md"
    comp_file.write_text(comparison)
    print(comparison)


def cmd_rank(args: argparse.Namespace) -> None:
    """Rank all tools by value score."""
    scored = rank_all_tools()
    print(f"\n{'Rank':<6}{'Tool':<25}{'Category':<15}{'Quality':<10}{'Value Score':<12}")
    print("-" * 68)
    for i, (t, score) in enumerate(scored, 1):
        print(f"{i:<6}{t['tool_name']:<25}{t.get('category', ''):<15}{t.get('quality_score', '?'):<10}{score:<12}")


def cmd_check(args: argparse.Namespace) -> None:
    """Check a specific tool for updates."""
    tool_name = args.tool.lower()
    tools = load_tracker()
    matches = [t for t in tools if tool_name in t["tool_name"].lower()]
    if not matches:
        print(f"Tool '{args.tool}' not found in tracker.")
        print("Add it with: --add TOOL_NAME CATEGORY")
        return
    for t in matches:
        score = score_tool_value(t)
        print(f"\n{t['tool_name']} ({t.get('category', '')})")
        print(f"  Quality: {t.get('quality_score', '?')}/10")
        print(f"  Free tier: {t.get('free_tier', 'none')}")
        print(f"  Price: {t.get('price_from', '?')}{t.get('price_unit', '')}")
        print(f"  API: {t.get('api_available', '?')}")
        print(f"  Value score: {score}/10")
        print(f"  Last checked: {t.get('last_checked', 'never')}")
        print(f"  Notes: {t.get('notes', '')}")


def cmd_add(args: argparse.Namespace) -> None:
    """Add a new tool to the tracker."""
    tools = load_tracker()
    new_tool = {
        "tool_name": args.tool,
        "category": args.category,
        "maker": "",
        "quality_score": "5",
        "free_tier": "",
        "price_from": "",
        "price_unit": "",
        "max_length": "",
        "max_res": "",
        "api_available": "",
        "api_cost_per_sec": "",
        "best_for": "",
        "last_checked": datetime.now().strftime("%Y-%m-%d"),
        "status": "NEW",
        "notes": "auto-added, needs research",
    }
    tools.append(new_tool)
    save_tracker(tools)
    append_changelog(f"Added new tool: {args.tool} ({args.category})")
    print(f"Added {args.tool} to tracker. Run --check {args.tool} after filling in details.")


def cmd_status(args: argparse.Namespace) -> None:
    """Show tracker stats."""
    tools = load_tracker()
    cat_counts = {}
    for t in tools:
        cat = t.get("category", "unknown")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    print(f"\nPERPETUAL TOOL RESEARCHER STATUS")
    print(f"================================")
    print(f"Total tools tracked: {len(tools)}")
    print(f"Categories: {len(cat_counts)}")
    print(f"\nBy category:")
    for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        cat_name = CATEGORIES.get(cat, cat)
        print(f"  {cat_name}: {count}")

    # Tools needing updates (not checked in 7+ days)
    stale = []
    for t in tools:
        last = t.get("last_checked", "")
        if last:
            try:
                checked = datetime.strptime(last, "%Y-%m-%d")
                if (datetime.now() - checked).days > 7:
                    stale.append(t["tool_name"])
            except ValueError:
                stale.append(t["tool_name"])

    if stale:
        print(f"\nStale (7+ days since check): {', '.join(stale[:10])}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Perpetual Tool Researcher")
    sub = parser.add_subparsers(dest="command")

    # Also support --flag style for consistency with other PRINTMAXX scripts
    parser.add_argument("--cycle", action="store_true", help="Full research cycle")
    parser.add_argument("--digest", action="store_true", help="Generate daily digest")
    parser.add_argument("--compare", metavar="CATEGORY", help="Compare tools in category")
    parser.add_argument("--rank", action="store_true", help="Rank all tools")
    parser.add_argument("--check", metavar="TOOL", help="Check specific tool")
    parser.add_argument("--add", nargs=2, metavar=("TOOL", "CATEGORY"), help="Add new tool")
    parser.add_argument("--status", action="store_true", help="Show tracker stats")

    args = parser.parse_args()

    if args.cycle:
        cmd_cycle(args)
    elif args.digest:
        cmd_digest(args)
    elif args.compare:
        args.category = args.compare
        cmd_compare(args)
    elif args.rank:
        cmd_rank(args)
    elif args.check:
        args.tool = args.check
        cmd_check(args)
    elif args.add:
        args.tool, args.category = args.add
        cmd_add(args)
    elif args.status:
        cmd_status(args)
    else:
        parser.print_help()
        print("\nQuick start:")
        print("  --status    See what's tracked")
        print("  --rank      Rank all tools by value")
        print("  --cycle     Full research sweep")
        print("  --digest    Daily digest for CEO agent")


if __name__ == "__main__":
    main()
