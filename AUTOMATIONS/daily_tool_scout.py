#!/usr/bin/env python3
"""Daily tool scout — discovers new open source tools from GitHub trending, HN, Reddit.
Outputs to OPS/DAILY_TOOL_SCOUT.md for human review.
Cron: 0 7 * * * (runs after method_discovery_crawler at 5AM)
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
OPS = PROJECT / "OPS"
LOG = PROJECT / "AUTOMATIONS" / "logs" / "tool_scout.log"

GITHUB_TRENDING_URL = "https://api.github.com/search/repositories?q=created:>={date}&language=python&sort=stars&order=desc&per_page=20"
TOPICS = [
    "agent+framework", "automation+tool", "ai+agent", "workflow+automation",
    "content+generation", "trading+bot", "video+generation", "voice+ai",
    "web+scraper", "lead+generation", "seo+tool", "newsletter",
    "social+media+automation", "mcp+server", "browser+automation",
    # Claude/Anthropic — we run on Claude Max, track everything they ship
    "anthropic+claude", "claude+code", "claude+agent+sdk", "model+context+protocol",
    # Competitor LLM tools we might leverage or need to match
    "openai+agents", "gemini+agent", "llm+orchestration",
]

# Anthropic-specific: check SDK/Claude Code releases for features that affect our system
ANTHROPIC_REPOS = [
    ("anthropics/anthropic-sdk-python", "Claude Python SDK"),
    ("anthropics/claude-code", "Claude Code CLI"),
    ("anthropics/courses", "Anthropic courses/examples"),
    ("modelcontextprotocol/servers", "Official MCP servers"),
]


def check_anthropic_updates():
    """Check Anthropic repos for recent releases/commits that could improve our system."""
    from datetime import timedelta
    updates = []
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00Z")
    for repo, label in ANTHROPIC_REPOS:
        try:
            # Check releases
            url = f"https://api.github.com/repos/{repo}/releases?per_page=3"
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "sovrun-scout"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                releases = json.loads(resp.read().decode())
                for rel in releases:
                    if rel.get("published_at", "") > week_ago:
                        updates.append({
                            "source": label,
                            "type": "release",
                            "name": rel.get("tag_name", ""),
                            "title": rel.get("name", ""),
                            "url": rel.get("html_url", ""),
                            "body": (rel.get("body") or "")[:200],
                            "date": rel.get("published_at", "")[:10],
                        })
        except Exception as e:
            log(f"Anthropic check failed for {repo}: {e}")
        try:
            # Check recent commits
            url = f"https://api.github.com/repos/{repo}/commits?since={week_ago}&per_page=5"
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "sovrun-scout"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                commits = json.loads(resp.read().decode())
                if len(commits) > 3:
                    updates.append({
                        "source": label,
                        "type": "active_development",
                        "name": f"{len(commits)} commits this week",
                        "title": commits[0]["commit"]["message"].split("\n")[0][:80] if commits else "",
                        "url": f"https://github.com/{repo}/commits",
                        "body": "",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                    })
        except Exception:
            pass
    return updates


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def search_github(query):
    """Search GitHub for repos matching query, created in last 7 days."""
    from datetime import timedelta
    date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    url = f"https://api.github.com/search/repositories?q={query}+created:>={date}&sort=stars&order=desc&per_page=5"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "sovrun-scout"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("items", [])
    except Exception as e:
        log(f"GitHub search failed for {query}: {e}")
        return []

def main():
    log("Starting daily tool scout")
    all_repos = []
    seen = set()
    
    for topic in TOPICS:
        repos = search_github(topic)
        for r in repos:
            if r["full_name"] not in seen and r["stargazers_count"] >= 50:
                seen.add(r["full_name"])
                all_repos.append({
                    "name": r["name"],
                    "full_name": r["full_name"],
                    "url": r["html_url"],
                    "stars": r["stargazers_count"],
                    "description": (r.get("description") or "")[:120],
                    "language": r.get("language", ""),
                    "license": (r.get("license") or {}).get("spdx_id", "unknown"),
                    "created": r.get("created_at", "")[:10],
                    "topic": topic,
                })
    
    # Sort by stars
    all_repos.sort(key=lambda x: x["stars"], reverse=True)
    
    # Check Anthropic/Claude updates
    anthropic_updates = check_anthropic_updates()

    # Write report
    output = OPS / "DAILY_TOOL_SCOUT.md"
    with open(output, "w") as f:
        f.write(f"# Daily Tool Scout — {datetime.now().strftime('%Y-%m-%d')}\n\n")

        # Anthropic section FIRST (highest priority — affects our entire system)
        if anthropic_updates:
            f.write("## CLAUDE/ANTHROPIC UPDATES (check these first — affects our system)\n\n")
            f.write("| Date | Source | Type | Name | Details |\n")
            f.write("|------|--------|------|------|--------|\n")
            for u in anthropic_updates:
                f.write(f"| {u['date']} | {u['source']} | {u['type']} | [{u['name']}]({u['url']}) | {u['title']} {u['body'][:100]} |\n")
            f.write("\n**Action:** Check if any updates unlock new capabilities for our agent system, MCP integrations, or Claude Code workflows.\n\n")
        else:
            f.write("## CLAUDE/ANTHROPIC: No new updates this week\n\n")

        f.write(f"## NEW TOOLS ({len(all_repos)} repos, 50+ stars, last 7 days)\n\n")
        f.write("| Stars | Name | Description | License | Language | Topic |\n")
        f.write("|-------|------|-------------|---------|----------|-------|\n")
        for r in all_repos[:30]:
            f.write(f"| {r['stars']} | [{r['name']}]({r['url']}) | {r['description']} | {r['license']} | {r['language']} | {r['topic']} |\n")
        f.write(f"\n\n*Auto-generated by daily_tool_scout.py. Review before integrating.*\n")
    
    log(f"Scout complete: {len(all_repos)} repos found, report at {output}")
    print(f"\nReport saved: {output}")

if __name__ == "__main__":
    main()
