#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Venture Deep Scorer - 10-Dimension Portfolio Analysis Engine
======================================================================
Goes beyond venture_performance_tracker.py with institutional-grade scoring.

Scores EVERY venture/op on 10 dimensions:
  1. Market size (TAM in $)
  2. Revenue velocity (time to $1K/mo)
  3. Margin potential (%)
  4. Defensibility (moat score 0-100)
  5. Automation potential (% automatable)
  6. Capital efficiency (revenue per $ invested)
  7. Scalability (linear vs exponential)
  8. Risk (regulatory, platform, technical)
  9. Synergy (cross-pollination with other ops)
  10. Momentum (trend direction: rising/flat/declining)

Generates: KILL / REDUCE / MAINTAIN / INVEST / DOUBLE_DOWN recommendations.
Outputs to: LEDGER/VENTURE_DEEP_SCORES.csv

Usage:
    python3 AUTOMATIONS/venture_deep_scorer.py --score-all
    python3 AUTOMATIONS/venture_deep_scorer.py --compare OP_MCP OP_AGENT_CONSULT
    python3 AUTOMATIONS/venture_deep_scorer.py --recommend
    python3 AUTOMATIONS/venture_deep_scorer.py --portfolio-optimize
    python3 AUTOMATIONS/venture_deep_scorer.py --export
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# PATH SAFETY
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER = PROJECT_ROOT / "LEDGER"
OUTPUT_CSV = LEDGER / "VENTURE_DEEP_SCORES.csv"
PERF_DIR = LEDGER / "VENTURE_PERFORMANCE"
FINANCIALS = PROJECT_ROOT / "FINANCIALS"

def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved

# ============================================================
# DIMENSION WEIGHTS (configurable)
# ============================================================
DEFAULT_WEIGHTS = {
    "market_size":       0.10,
    "revenue_velocity":  0.15,
    "margin_potential":  0.10,
    "defensibility":     0.10,
    "automation":        0.10,
    "capital_efficiency": 0.10,
    "scalability":       0.10,
    "risk":              0.10,
    "synergy":           0.08,
    "momentum":          0.07,
}

# Aggressive growth weights: favor speed + automation
AGGRESSIVE_WEIGHTS = {
    "market_size":       0.05,
    "revenue_velocity":  0.25,
    "margin_potential":  0.10,
    "defensibility":     0.05,
    "automation":        0.15,
    "capital_efficiency": 0.15,
    "scalability":       0.05,
    "risk":              0.05,
    "synergy":           0.10,
    "momentum":          0.05,
}

# Defensive weights: favor moat + margins + risk
DEFENSIVE_WEIGHTS = {
    "market_size":       0.10,
    "revenue_velocity":  0.05,
    "margin_potential":  0.15,
    "defensibility":     0.20,
    "automation":        0.05,
    "capital_efficiency": 0.05,
    "scalability":       0.15,
    "risk":              0.15,
    "synergy":           0.05,
    "momentum":          0.05,
}


# ============================================================
# VENTURE DATABASE - All ops with 10-dimension scores
# ============================================================
# Each dimension scored 0-100
# risk is INVERTED: high score = LOW risk (good)

VENTURES = {
    # ===== EDGE OPS (from deep scan) =====
    "OP_MCP": {
        "name": "MCP Server Marketplace",
        "category": "EDGE",
        "revenue_range": "$3K-$10K/mo",
        "scores": {
            "market_size": 70,        # $500M+ growing 85% MoM
            "revenue_velocity": 75,   # 2-4 weeks to first dollar
            "margin_potential": 92,   # 90%+ digital products
            "defensibility": 80,     # first-mover + ecosystem knowledge
            "automation": 85,         # code once, sell repeatedly
            "capital_efficiency": 95, # $0-100 capital, $3K+ potential
            "scalability": 80,        # each server sells independently
            "risk": 65,              # platform risk (Anthropic spec changes)
            "synergy": 90,           # feeds community, products, consulting
            "momentum": 95,          # 85% MoM growth, explosive
        },
        "dependencies": ["D12", "Claude Code Max"],
        "automation_script": "mcp_server_builder.py",
    },
    "OP_AGENT_CONSULT": {
        "name": "AI Agent Consulting",
        "category": "EDGE",
        "revenue_range": "$2.5K-$10K/mo",
        "scores": {
            "market_size": 95,        # $7.63B -> $182.97B by 2033
            "revenue_velocity": 85,   # 1-2 weeks to first dollar
            "margin_potential": 70,   # 60-70% margins
            "defensibility": 55,     # growing competition
            "automation": 50,         # services = less automatable
            "capital_efficiency": 95, # $0 capital, $2.5K+ potential
            "scalability": 45,        # linear with hours
            "risk": 70,              # demand risk low, delivery risk med
            "synergy": 85,           # feeds community, MCP, infra
            "momentum": 92,          # 49.6% CAGR
        },
        "dependencies": ["S04", "S01", "CrewAI"],
        "automation_script": "agent_consult_pipeline.py",
    },
    "OP_VIBE_PRODUCTS": {
        "name": "Vibe Coding Products",
        "category": "EDGE",
        "revenue_range": "$500-$3K/mo",
        "scores": {
            "market_size": 55,        # $2B+ but narrow niche
            "revenue_velocity": 90,   # 1 week to first dollar
            "margin_potential": 97,   # 95%+ pure digital
            "defensibility": 70,     # first-mover, practitioner knowledge
            "automation": 90,         # package once, sell forever
            "capital_efficiency": 99, # $0 capital, pure knowledge
            "scalability": 60,        # template sales cap out
            "risk": 80,              # low risk, worst case no sales
            "synergy": 85,           # feeds community, MCP bundle
            "momentum": 80,          # vibe coding recognized category
        },
        "dependencies": ["D01", "N02", "CLAUDE.md knowledge"],
        "automation_script": "vibe_product_packager.py",
    },
    "OP_COMMUNITY": {
        "name": "Skool Community ($47/mo)",
        "category": "EDGE",
        "revenue_range": "$5K-$50K/mo",
        "scores": {
            "market_size": 80,        # $5B+ creator community market
            "revenue_velocity": 55,   # 2-4 weeks, needs growth
            "margin_potential": 82,   # 80% after Skool fee
            "defensibility": 75,     # community moat, switching costs
            "automation": 40,         # requires engagement, content
            "capital_efficiency": 65, # $99/mo overhead, needs members
            "scalability": 85,        # exponential with viral loops
            "risk": 60,              # churn risk, content requirement
            "synergy": 95,           # hub that connects all edge ops
            "momentum": 85,          # Skool growing, communities hot
        },
        "dependencies": ["M02", "OP_VIBE_PRODUCTS", "OP_AGENT_CONSULT"],
        "automation_script": "community_growth_tracker.py",
    },
    "OP_CLIP_SERVICE": {
        "name": "Streamer Clipping Service",
        "category": "EDGE",
        "revenue_range": "$1.5K-$5K/mo",
        "scores": {
            "market_size": 75,        # $150M/mo TAM theoretical
            "revenue_velocity": 80,   # 1-2 weeks to first client
            "margin_potential": 88,   # 85-90% margins
            "defensibility": 40,     # low moat, tools available
            "automation": 80,         # auto_clip_pipeline exists
            "capital_efficiency": 85, # $30/mo tools, $300+/client
            "scalability": 35,        # linear with clients
            "risk": 75,              # low risk, validated demand
            "synergy": 60,           # feeds community content
            "momentum": 70,          # stable demand
        },
        "dependencies": ["C09", "N26", "auto_clip_pipeline.py"],
        "automation_script": "auto_clip_pipeline.py",
    },
    "OP_INFRA_SERVICE": {
        "name": "Solopreneur Infrastructure Setup",
        "category": "EDGE",
        "revenue_range": "$2K-$5K/mo",
        "scores": {
            "market_size": 50,        # $50M+ niche
            "revenue_velocity": 80,   # 1 week to first client
            "margin_potential": 72,   # 70% effective
            "defensibility": 30,     # easy to replicate
            "automation": 70,         # checklists, templates
            "capital_efficiency": 95, # $0 capital
            "scalability": 30,        # linear with hours
            "risk": 85,              # very low risk
            "synergy": 65,           # feeds agent consulting
            "momentum": 60,          # stable market
        },
        "dependencies": ["S02", "S18", "G01"],
        "automation_script": "infra_setup_generator.py",
    },
    "OP_API_ARB": {
        "name": "API Arbitrage (LLM Routing)",
        "category": "EDGE",
        "revenue_range": "$1K-$10K/mo",
        "scores": {
            "market_size": 90,        # $10B+ LLM API market
            "revenue_velocity": 50,   # 2-4 weeks
            "margin_potential": 92,   # 90%+ API markup
            "defensibility": 20,     # race to bottom
            "automation": 95,         # fully automated
            "capital_efficiency": 60, # needs API credits upfront
            "scalability": 90,        # exponential with usage
            "risk": 35,              # high risk: pricing competition
            "synergy": 55,           # backend for consulting
            "momentum": 45,          # window narrowing
        },
        "dependencies": ["D09", "A04", "N54"],
        "automation_script": "api_arb_router.py",
    },

    # ===== EXISTING HIGH-PRIORITY OPS =====
    "S01": {
        "name": "Claude Code Freelance Arbitrage",
        "category": "SERVICE",
        "revenue_range": "$2K-$15K/mo",
        "scores": {
            "market_size": 80,
            "revenue_velocity": 90,
            "margin_potential": 95,
            "defensibility": 50,
            "automation": 75,
            "capital_efficiency": 95,
            "scalability": 50,
            "risk": 65,
            "synergy": 70,
            "momentum": 85,
        },
        "dependencies": ["Fiverr", "Upwork", "Claude Code Max"],
        "automation_script": "N/A (manual delivery)",
    },
    "S02": {
        "name": "Local Biz Website Service",
        "category": "SERVICE",
        "revenue_range": "$3K-$50K/mo",
        "scores": {
            "market_size": 85,
            "revenue_velocity": 75,
            "margin_potential": 85,
            "defensibility": 45,
            "automation": 80,
            "capital_efficiency": 90,
            "scalability": 55,
            "risk": 70,
            "synergy": 65,
            "momentum": 75,
        },
        "dependencies": ["local_biz_pipeline.py", "bulk_landing_page_generator.py"],
        "automation_script": "local_biz_pipeline.py",
    },
    "D01": {
        "name": "Gumroad Product Portfolio",
        "category": "DIGITAL",
        "revenue_range": "$500-$10K/mo",
        "scores": {
            "market_size": 70,
            "revenue_velocity": 85,
            "margin_potential": 90,
            "defensibility": 55,
            "automation": 90,
            "capital_efficiency": 95,
            "scalability": 75,
            "risk": 80,
            "synergy": 80,
            "momentum": 70,
        },
        "dependencies": ["Gumroad account", "Stripe"],
        "automation_script": "N/A (manual upload)",
    },
    "C01": {
        "name": "TikTok Content Farm",
        "category": "CONTENT",
        "revenue_range": "$500-$10K/mo",
        "scores": {
            "market_size": 90,
            "revenue_velocity": 60,
            "margin_potential": 85,
            "defensibility": 30,
            "automation": 75,
            "capital_efficiency": 90,
            "scalability": 70,
            "risk": 45,
            "synergy": 75,
            "momentum": 65,
        },
        "dependencies": ["TikTok accounts", "Kling", "CapCut"],
        "automation_script": "content_posting/",
    },
    "A01": {
        "name": "Portfolio App Builder",
        "category": "APP",
        "revenue_range": "$5K-$50K/mo",
        "scores": {
            "market_size": 85,
            "revenue_velocity": 45,
            "margin_potential": 80,
            "defensibility": 60,
            "automation": 65,
            "capital_efficiency": 70,
            "scalability": 85,
            "risk": 55,
            "synergy": 55,
            "momentum": 70,
        },
        "dependencies": ["Apple Developer", "Play Store"],
        "automation_script": "app_factory/",
    },
    "P01": {
        "name": "AI Influencer Portfolio (SFW)",
        "category": "PERSONA",
        "revenue_range": "$500-$20K/mo",
        "scores": {
            "market_size": 80,
            "revenue_velocity": 50,
            "margin_potential": 85,
            "defensibility": 65,
            "automation": 70,
            "capital_efficiency": 80,
            "scalability": 75,
            "risk": 50,
            "synergy": 80,
            "momentum": 75,
        },
        "dependencies": ["Kling", "Leonardo.ai", "ElevenLabs"],
        "automation_script": "ai_influencer_pipeline.py",
    },
    "N02": {
        "name": "Whop Digital Storefront",
        "category": "DIGITAL",
        "revenue_range": "$2K-$50K/mo",
        "scores": {
            "market_size": 75,
            "revenue_velocity": 80,
            "margin_potential": 94,
            "defensibility": 50,
            "automation": 85,
            "capital_efficiency": 95,
            "scalability": 80,
            "risk": 70,
            "synergy": 85,
            "momentum": 85,
        },
        "dependencies": ["Whop account"],
        "automation_script": "N/A (platform-based)",
    },
    "S18": {
        "name": "Rapid Build Monetization",
        "category": "SERVICE",
        "revenue_range": "$6K-$60K/mo",
        "scores": {
            "market_size": 80,
            "revenue_velocity": 90,
            "margin_potential": 90,
            "defensibility": 55,
            "automation": 60,
            "capital_efficiency": 95,
            "scalability": 40,
            "risk": 70,
            "synergy": 70,
            "momentum": 85,
        },
        "dependencies": ["Claude Code Max", "Vercel"],
        "automation_script": "N/A (manual builds)",
    },
    "G02": {
        "name": "RBI Perpetual Improvement System",
        "category": "GROWTH",
        "revenue_range": "Meta-op",
        "scores": {
            "market_size": 0,
            "revenue_velocity": 0,
            "margin_potential": 0,
            "defensibility": 90,
            "automation": 90,
            "capital_efficiency": 99,
            "scalability": 95,
            "risk": 95,
            "synergy": 99,
            "momentum": 80,
        },
        "dependencies": ["scripts/rbi_audit.py"],
        "automation_script": "rbi_audit.py",
    },
    "N04": {
        "name": "Clipper Army Full SOP",
        "category": "GROWTH",
        "revenue_range": "$5K-$54K/mo",
        "scores": {
            "market_size": 75,
            "revenue_velocity": 55,
            "margin_potential": 70,
            "defensibility": 45,
            "automation": 60,
            "capital_efficiency": 65,
            "scalability": 80,
            "risk": 55,
            "synergy": 75,
            "momentum": 70,
        },
        "dependencies": ["TikTok accounts", "Clipper recruitment"],
        "automation_script": "clipper_management.py",
    },
    "C05": {
        "name": "Newsletter Empire",
        "category": "CONTENT",
        "revenue_range": "$500-$68K/mo",
        "scores": {
            "market_size": 75,
            "revenue_velocity": 50,
            "margin_potential": 80,
            "defensibility": 75,
            "automation": 60,
            "capital_efficiency": 85,
            "scalability": 70,
            "risk": 80,
            "synergy": 80,
            "momentum": 65,
        },
        "dependencies": ["Beehiiv/Substack account"],
        "automation_script": "newsletter_pipeline.py",
    },
    "S04": {
        "name": "AI Automation Agency",
        "category": "SERVICE",
        "revenue_range": "$2K-$20K/mo",
        "scores": {
            "market_size": 85,
            "revenue_velocity": 70,
            "margin_potential": 80,
            "defensibility": 50,
            "automation": 65,
            "capital_efficiency": 90,
            "scalability": 50,
            "risk": 65,
            "synergy": 75,
            "momentum": 80,
        },
        "dependencies": ["n8n", "Claude Code"],
        "automation_script": "N/A",
    },
}


# ============================================================
# SCORING ENGINE
# ============================================================

def compute_composite(scores, weights):
    """Compute weighted composite score 0-100."""
    total = 0.0
    for dim, weight in weights.items():
        total += scores.get(dim, 0) * weight
    return round(total, 1)


def get_recommendation(composite):
    """Map composite score to action recommendation."""
    if composite >= 80:
        return "DOUBLE_DOWN"
    elif composite >= 65:
        return "INVEST"
    elif composite >= 50:
        return "MAINTAIN"
    elif composite >= 35:
        return "REDUCE"
    else:
        return "KILL"


def get_recommendation_color(rec):
    """Terminal color codes for recommendations."""
    colors = {
        "DOUBLE_DOWN": "\033[92m",  # green
        "INVEST":      "\033[96m",  # cyan
        "MAINTAIN":    "\033[93m",  # yellow
        "REDUCE":      "\033[91m",  # red
        "KILL":        "\033[31m",  # dark red
    }
    return colors.get(rec, "")

RESET = "\033[0m"


def score_all(weights=None):
    """Score all ventures and return sorted results."""
    if weights is None:
        weights = DEFAULT_WEIGHTS
    results = []
    for vid, venture in VENTURES.items():
        composite = compute_composite(venture["scores"], weights)
        rec = get_recommendation(composite)
        results.append({
            "id": vid,
            "name": venture["name"],
            "category": venture["category"],
            "revenue_range": venture["revenue_range"],
            "composite": composite,
            "recommendation": rec,
            "scores": venture["scores"],
            "dependencies": venture.get("dependencies", []),
            "automation_script": venture.get("automation_script", "N/A"),
        })
    results.sort(key=lambda x: -x["composite"])
    return results


def print_dimension_bar(label, value, width=30):
    """Print a visual bar for a dimension score."""
    filled = int(value / 100 * width)
    bar = "#" * filled + "-" * (width - filled)
    if value >= 75:
        color = "\033[92m"
    elif value >= 50:
        color = "\033[93m"
    else:
        color = "\033[91m"
    print(f"  {label:<22} {color}[{bar}] {value:>3}/100{RESET}")


# ============================================================
# CLI COMMANDS
# ============================================================

def cmd_score_all(args):
    """Score all ventures and display ranked results."""
    weights = DEFAULT_WEIGHTS
    if args.aggressive:
        weights = AGGRESSIVE_WEIGHTS
        print("Using AGGRESSIVE weights (favor speed + automation)\n")
    elif args.defensive:
        weights = DEFENSIVE_WEIGHTS
        print("Using DEFENSIVE weights (favor moat + margins)\n")

    results = score_all(weights)

    print(f"{'='*80}")
    print(f"  VENTURE DEEP SCORER - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  {len(results)} ventures scored across 10 dimensions")
    print(f"{'='*80}\n")

    # Group by recommendation
    for rec_type in ["DOUBLE_DOWN", "INVEST", "MAINTAIN", "REDUCE", "KILL"]:
        items = [r for r in results if r["recommendation"] == rec_type]
        if not items:
            continue
        color = get_recommendation_color(rec_type)
        print(f"{color}{rec_type}{RESET} ({len(items)} ventures):")
        print(f"  {'ID':<18} {'NAME':<36} {'SCORE':>6}  {'REVENUE':<20} {'CATEGORY':<10}")
        print(f"  {'-'*18} {'-'*36} {'-'*6}  {'-'*20} {'-'*10}")
        for item in items:
            print(f"  {item['id']:<18} {item['name']:<36} {item['composite']:>5.1f}  "
                  f"{item['revenue_range']:<20} {item['category']:<10}")
        print()

    # Top 3 actions
    print(f"{'='*80}")
    print("TOP 3 ACTIONS:")
    for i, item in enumerate(results[:3], 1):
        color = get_recommendation_color(item["recommendation"])
        print(f"  {i}. {color}{item['name']}{RESET} (score: {item['composite']}/100)")
        # Show weakest dimension
        weakest = min(item["scores"], key=item["scores"].get)
        print(f"     Weakest: {weakest} ({item['scores'][weakest]}/100) - address this first")
    print(f"{'='*80}\n")

    if args.export or args.score_all:
        export_csv(results)


def cmd_compare(args):
    """Compare two ops head-to-head."""
    op1_id = args.compare[0]
    op2_id = args.compare[1]

    if op1_id not in VENTURES:
        print(f"Unknown op: {op1_id}. Available: {', '.join(sorted(VENTURES.keys()))}")
        return
    if op2_id not in VENTURES:
        print(f"Unknown op: {op2_id}. Available: {', '.join(sorted(VENTURES.keys()))}")
        return

    v1 = VENTURES[op1_id]
    v2 = VENTURES[op2_id]
    s1 = compute_composite(v1["scores"], DEFAULT_WEIGHTS)
    s2 = compute_composite(v2["scores"], DEFAULT_WEIGHTS)

    print(f"\n{'='*70}")
    print(f"  HEAD-TO-HEAD: {op1_id} vs {op2_id}")
    print(f"{'='*70}\n")

    print(f"  {'DIMENSION':<22} {op1_id:>12} {op2_id:>12}  {'WINNER':>12}")
    print(f"  {'-'*22} {'-'*12} {'-'*12}  {'-'*12}")

    dimensions = [
        ("market_size", "Market Size"),
        ("revenue_velocity", "Revenue Velocity"),
        ("margin_potential", "Margin Potential"),
        ("defensibility", "Defensibility"),
        ("automation", "Automation"),
        ("capital_efficiency", "Capital Efficiency"),
        ("scalability", "Scalability"),
        ("risk", "Risk (inverted)"),
        ("synergy", "Synergy"),
        ("momentum", "Momentum"),
    ]

    wins = {op1_id: 0, op2_id: 0}
    for dim_key, dim_name in dimensions:
        val1 = v1["scores"].get(dim_key, 0)
        val2 = v2["scores"].get(dim_key, 0)
        if val1 > val2:
            winner = op1_id
            wins[op1_id] += 1
        elif val2 > val1:
            winner = op2_id
            wins[op2_id] += 1
        else:
            winner = "TIE"

        color1 = "\033[92m" if val1 > val2 else "\033[91m" if val1 < val2 else "\033[93m"
        color2 = "\033[92m" if val2 > val1 else "\033[91m" if val2 < val1 else "\033[93m"

        print(f"  {dim_name:<22} {color1}{val1:>12}{RESET} {color2}{val2:>12}{RESET}  {winner:>12}")

    print(f"\n  {'COMPOSITE':<22} {s1:>12.1f} {s2:>12.1f}")
    print(f"  {'DIMENSION WINS':<22} {wins[op1_id]:>12} {wins[op2_id]:>12}")
    print(f"  {'RECOMMENDATION':<22} {get_recommendation(s1):>12} {get_recommendation(s2):>12}")

    overall = op1_id if s1 > s2 else op2_id if s2 > s1 else "TIE"
    overall_score = max(s1, s2)
    print(f"\n  VERDICT: {overall} wins with {overall_score:.1f}/100")
    print(f"{'='*70}\n")


def cmd_recommend(args):
    """Generate portfolio recommendations."""
    results = score_all(DEFAULT_WEIGHTS)

    print(f"\n{'='*70}")
    print(f"  PORTFOLIO RECOMMENDATIONS - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}\n")

    # Immediate actions (top 5)
    print("IMMEDIATE ACTIONS (This Week):")
    for item in results[:5]:
        color = get_recommendation_color(item["recommendation"])
        print(f"  {color}{item['recommendation']:<14}{RESET} {item['id']:<18} "
              f"{item['name']:<36} {item['composite']:.1f}/100")
        # Show top strength and weakest link
        strongest = max(item["scores"], key=item["scores"].get)
        weakest = min(item["scores"], key=item["scores"].get)
        print(f"    Strength: {strongest} ({item['scores'][strongest]}/100)")
        print(f"    Fix: {weakest} ({item['scores'][weakest]}/100)")
        print(f"    Deps: {', '.join(item['dependencies'][:3])}")
        print()

    # Kill list
    kills = [r for r in results if r["recommendation"] in ("KILL", "REDUCE")]
    if kills:
        print("\nREDUCE/KILL (Reallocate time from these):")
        for item in kills:
            color = get_recommendation_color(item["recommendation"])
            print(f"  {color}{item['recommendation']:<14}{RESET} {item['id']:<18} "
                  f"{item['name']:<36} {item['composite']:.1f}/100")
        print()

    # Synergy clusters
    print("SYNERGY CLUSTERS (ops that amplify each other):")
    clusters = [
        ("MCP Flywheel", ["OP_MCP", "OP_VIBE_PRODUCTS", "OP_COMMUNITY", "OP_AGENT_CONSULT"]),
        ("Service Stack", ["S01", "S02", "S18", "OP_INFRA_SERVICE"]),
        ("Content Machine", ["C01", "C05", "P01", "OP_CLIP_SERVICE"]),
        ("Digital Products", ["D01", "N02", "OP_VIBE_PRODUCTS"]),
    ]
    for cluster_name, ops_in_cluster in clusters:
        present = [oid for oid in ops_in_cluster if oid in VENTURES]
        if present:
            avg_score = sum(
                compute_composite(VENTURES[oid]["scores"], DEFAULT_WEIGHTS)
                for oid in present
            ) / len(present)
            print(f"  {cluster_name}: {', '.join(present)} (avg: {avg_score:.1f}/100)")
    print()


def cmd_portfolio_optimize(args):
    """Optimize portfolio allocation across ventures."""
    results = score_all(DEFAULT_WEIGHTS)

    print(f"\n{'='*70}")
    print(f"  PORTFOLIO OPTIMIZATION - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}\n")

    # Assume 40 hours/week available
    total_hours = 40
    print(f"Available hours/week: {total_hours}\n")

    # Allocation tiers
    allocation = {
        "DOUBLE_DOWN": 0.40,
        "INVEST":      0.30,
        "MAINTAIN":    0.20,
        "REDUCE":      0.08,
        "KILL":        0.02,
    }

    print(f"  {'TIER':<14} {'ALLOCATION':>10} {'HOURS':>8}  VENTURES")
    print(f"  {'-'*14} {'-'*10} {'-'*8}  {'-'*40}")

    for tier, pct in allocation.items():
        tier_items = [r for r in results if r["recommendation"] == tier]
        hours = total_hours * pct
        color = get_recommendation_color(tier)
        names = ", ".join(r["id"] for r in tier_items[:4])
        if len(tier_items) > 4:
            names += f" +{len(tier_items)-4} more"
        print(f"  {color}{tier:<14}{RESET} {pct*100:>9.0f}% {hours:>7.1f}h  {names}")

    print()

    # Specific time allocation per venture (top 10)
    print("SPECIFIC TIME ALLOCATION (Top 10 by score):")
    total_score = sum(r["composite"] for r in results[:10])
    for item in results[:10]:
        pct = item["composite"] / total_score
        hours = total_hours * pct
        color = get_recommendation_color(item["recommendation"])
        print(f"  {item['id']:<18} {item['name']:<32} {color}{hours:>5.1f}h/wk{RESET}  "
              f"({pct*100:.0f}%)")

    print(f"\n  Total allocated: {total_hours:.0f}h/wk")

    # Risk analysis
    print("\nRISK DISTRIBUTION:")
    high_risk = [r for r in results if r["scores"]["risk"] < 50]
    med_risk = [r for r in results if 50 <= r["scores"]["risk"] < 75]
    low_risk = [r for r in results if r["scores"]["risk"] >= 75]
    print(f"  High risk: {len(high_risk)} ventures ({', '.join(r['id'] for r in high_risk[:3])})")
    print(f"  Med risk:  {len(med_risk)} ventures")
    print(f"  Low risk:  {len(low_risk)} ventures")

    # Concentration warning
    top3_pct = sum(r["composite"] for r in results[:3]) / total_score * 100
    if top3_pct > 50:
        print(f"\n  WARNING: Top 3 ventures = {top3_pct:.0f}% of allocation. Consider diversifying.")
    print(f"\n{'='*70}\n")


def cmd_deep_score(args):
    """Show deep score breakdown for a single venture."""
    vid = args.deep
    if vid not in VENTURES:
        print(f"Unknown venture: {vid}")
        print(f"Available: {', '.join(sorted(VENTURES.keys()))}")
        return

    venture = VENTURES[vid]
    composite = compute_composite(venture["scores"], DEFAULT_WEIGHTS)
    rec = get_recommendation(composite)

    print(f"\n{'='*60}")
    print(f"  {venture['name']} ({vid})")
    print(f"  Composite: {composite}/100 -> {rec}")
    print(f"  Revenue: {venture['revenue_range']}")
    print(f"  Category: {venture['category']}")
    print(f"{'='*60}\n")

    print("DIMENSION BREAKDOWN:")
    print_dimension_bar("Market Size", venture["scores"]["market_size"])
    print_dimension_bar("Revenue Velocity", venture["scores"]["revenue_velocity"])
    print_dimension_bar("Margin Potential", venture["scores"]["margin_potential"])
    print_dimension_bar("Defensibility", venture["scores"]["defensibility"])
    print_dimension_bar("Automation", venture["scores"]["automation"])
    print_dimension_bar("Capital Efficiency", venture["scores"]["capital_efficiency"])
    print_dimension_bar("Scalability", venture["scores"]["scalability"])
    print_dimension_bar("Risk (inv)", venture["scores"]["risk"])
    print_dimension_bar("Synergy", venture["scores"]["synergy"])
    print_dimension_bar("Momentum", venture["scores"]["momentum"])

    # Strengths and weaknesses
    sorted_dims = sorted(venture["scores"].items(), key=lambda x: -x[1])
    print(f"\n  TOP 3 STRENGTHS:")
    for dim, val in sorted_dims[:3]:
        print(f"    {dim}: {val}/100")
    print(f"  TOP 3 WEAKNESSES:")
    for dim, val in sorted_dims[-3:]:
        print(f"    {dim}: {val}/100")

    print(f"\n  Dependencies: {', '.join(venture.get('dependencies', []))}")
    print(f"  Automation: {venture.get('automation_script', 'N/A')}")

    # Weight sensitivity
    print(f"\n  WEIGHT SENSITIVITY:")
    for wname, weights in [("Default", DEFAULT_WEIGHTS), ("Aggressive", AGGRESSIVE_WEIGHTS),
                           ("Defensive", DEFENSIVE_WEIGHTS)]:
        sc = compute_composite(venture["scores"], weights)
        rc = get_recommendation(sc)
        print(f"    {wname:<12} {sc:>5.1f}/100 -> {rc}")
    print(f"\n{'='*60}\n")


# ============================================================
# EXPORT
# ============================================================

def export_csv(results=None):
    """Export scores to CSV."""
    if results is None:
        results = score_all(DEFAULT_WEIGHTS)

    os.makedirs(LEDGER, exist_ok=True)
    output = safe_path(OUTPUT_CSV)

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "op_id", "name", "category", "revenue_range",
            "composite_score", "recommendation",
            "market_size", "revenue_velocity", "margin_potential",
            "defensibility", "automation", "capital_efficiency",
            "scalability", "risk", "synergy", "momentum",
            "dependencies", "automation_script"
        ])
        ts = datetime.now().isoformat()
        for r in results:
            writer.writerow([
                ts, r["id"], r["name"], r["category"], r["revenue_range"],
                r["composite"], r["recommendation"],
                r["scores"]["market_size"], r["scores"]["revenue_velocity"],
                r["scores"]["margin_potential"], r["scores"]["defensibility"],
                r["scores"]["automation"], r["scores"]["capital_efficiency"],
                r["scores"]["scalability"], r["scores"]["risk"],
                r["scores"]["synergy"], r["scores"]["momentum"],
                "|".join(r["dependencies"]), r["automation_script"]
            ])

    print(f"Exported {len(results)} venture scores to {output}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Venture Deep Scorer - 10-Dimension Portfolio Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --score-all                    Score all ventures
  %(prog)s --score-all --aggressive       Score with aggressive weights
  %(prog)s --compare OP_MCP S01           Head-to-head comparison
  %(prog)s --recommend                    Portfolio recommendations
  %(prog)s --portfolio-optimize           Time allocation optimization
  %(prog)s --deep OP_MCP                  Deep dive on one venture
  %(prog)s --export                       Export scores to CSV
  %(prog)s --list                         List all venture IDs
        """
    )
    parser.add_argument("--score-all", action="store_true",
                        help="Score all ventures across 10 dimensions")
    parser.add_argument("--compare", nargs=2, metavar=("OP1", "OP2"),
                        help="Compare two ops head-to-head")
    parser.add_argument("--recommend", action="store_true",
                        help="Generate portfolio recommendations")
    parser.add_argument("--portfolio-optimize", action="store_true",
                        help="Optimize time allocation across ventures")
    parser.add_argument("--deep", metavar="OP_ID",
                        help="Deep score breakdown for a single venture")
    parser.add_argument("--export", action="store_true",
                        help="Export scores to LEDGER/VENTURE_DEEP_SCORES.csv")
    parser.add_argument("--aggressive", action="store_true",
                        help="Use aggressive weights (favor speed + automation)")
    parser.add_argument("--defensive", action="store_true",
                        help="Use defensive weights (favor moat + margins)")
    parser.add_argument("--list", action="store_true",
                        help="List all venture IDs")

    args = parser.parse_args()

    if args.list:
        print(f"\n{len(VENTURES)} ventures tracked:\n")
        for vid in sorted(VENTURES.keys()):
            v = VENTURES[vid]
            print(f"  {vid:<18} {v['name']:<36} [{v['category']}]")
        print()
        return

    if args.compare:
        cmd_compare(args)
    elif args.recommend:
        cmd_recommend(args)
    elif args.portfolio_optimize:
        cmd_portfolio_optimize(args)
    elif args.deep:
        cmd_deep_score(args)
    elif args.export:
        results = score_all(DEFAULT_WEIGHTS)
        export_csv(results)
    elif args.score_all:
        cmd_score_all(args)
    else:
        # Default: score all
        cmd_score_all(args)


if __name__ == "__main__":
    main()
