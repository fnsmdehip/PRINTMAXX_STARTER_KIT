#!/usr/bin/env python3
"""Opportunity research via Gemini API."""
import json
import os
import urllib.request
import urllib.error
import sys

# Read key from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
api_key = None
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith('GEMINI_API_KEY='):
                api_key = line.strip().split('=', 1)[1]
                break

if not api_key:
    print("ERROR: No GEMINI_API_KEY found in .env")
    sys.exit(1)

queries = [
    "List 10 specific micro-SaaS and solopreneur business opportunities for April 2026 startable with $0-100 that generate revenue within 1-2 weeks. Focus on: MCP server marketplace for Claude/AI agents, vibe coding tools ecosystem, AI workflow automation for local businesses, Claude API wrapper products, Expo/React Native niche apps, Next.js template businesses, digital product arbitrage on Whop/Gumroad. For each give: opportunity name, why NOW in April 2026, estimated monthly revenue, competition level (low/med/high), specific first action. Be specific with real platforms and price points.",

    "What are the highest-paying AI tool affiliate programs in 2026? List 10 with: commission rates, cookie duration, average order value, monthly earning potential for 10K visitors. Include Claude/Anthropic, Cursor, Windsurf, Bolt.new, Lovable, v0 by Vercel, Replit, new AI coding tool affiliates. Give dollar amounts per referral.",

    "Most profitable digital product categories on Gumroad, Whop, Lemon Squeezy in Q1-Q2 2026. List 10 product types: average price, monthly units by top sellers. Focus on AI prompt packs, Claude Code configs, cursor rules, AI agent templates, n8n workflows, Notion AI templates, vibe coding kits, MCP server bundles.",

    "Best local business AI automation service opportunities April 2026. List 10 services a solopreneur with Python + Claude API + scraping can offer for $500-2000/month. Include AI receptionist, Google review responses, AI social media, scheduling, local SEO, chatbots, lead qualification. For each: target business type, current manual cost, how to find first 3 clients this week.",

    "What new API and developer tool marketplaces have launched or grown significantly in 2025-2026? List opportunities for selling: MCP servers, API wrappers, developer tools, code templates, AI agent frameworks. Include RapidAPI, Smithery.ai, Composio, any MCP registries, npm/PyPI monetizable packages. Give pricing models and revenue potential.",

    "What are the most underserved mobile app niches on iOS App Store in April 2026 that a solo developer with Expo/React Native can fill? List 10 niches with: search volume, current top app quality rating (bad=opportunity), monetization model (subscription vs one-time), realistic monthly revenue after 3 months. Focus on utility apps, not games.",

    "What content monetization platforms launched or expanded in 2025-2026 that creators are not yet saturated on? List emerging platforms beyond YouTube/TikTok/Instagram. Include: Substack, Beehiiv, Ghost, Kit (ConvertKit), Skool, Whop communities, paid Discord servers, Patreon alternatives. Give specific niches that are underserved on each.",

    "List 10 specific ways to monetize Claude Code / AI coding assistant expertise in April 2026. Include: selling CLAUDE.md configurations, MCP server development for hire, AI agent consulting, Claude Code tutorial courses, custom automation builds for non-technical founders, vibe coding as a service for MVPs. For each: price point, target customer, acquisition channel, competition level."
]

output_dir = os.path.join(os.path.dirname(__file__), 'opportunities')
os.makedirs(output_dir, exist_ok=True)

results = []
for i, query in enumerate(queries):
    print(f"\n--- Query {i+1}/{len(queries)} ---")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": query}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 3000}
    }).encode('utf-8')

    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            text = data['candidates'][0]['content']['parts'][0]['text']
            results.append(text)
            print(text[:500] + "...")
    except Exception as e:
        print(f"Error on query {i+1}: {e}")
        results.append(f"ERROR: {e}")

# Save all results
output_file = os.path.join(output_dir, 'raw_research_20260402.md')
with open(output_file, 'w') as f:
    f.write("# Opportunity Research Results - April 2, 2026\n\n")
    topics = [
        "Micro-SaaS Opportunities",
        "AI Affiliate Programs",
        "Digital Product Categories",
        "Local Business AI Automation",
        "API/Developer Tool Marketplaces",
        "Underserved iOS App Niches",
        "Content Monetization Platforms",
        "Claude Code Expertise Monetization"
    ]
    for i, (topic, result) in enumerate(zip(topics, results)):
        f.write(f"\n## {i+1}. {topic}\n\n{result}\n\n---\n")

print(f"\nResults saved to {output_file}")
print(f"Total queries: {len(queries)}, Successful: {sum(1 for r in results if not r.startswith('ERROR'))}")
