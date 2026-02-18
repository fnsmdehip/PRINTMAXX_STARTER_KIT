#!/usr/bin/env python3
"""
method_stack_analyzer.py - Calculate method synergies and optimal stacks

Reads CROSS_POLLINATION_MATRIX.csv, analyzes synergy scores between methods,
and recommends the highest-value stacks. Identifies which methods multiply
each other's revenue when combined.

Usage:
    python3 method_stack_analyzer.py
    python3 method_stack_analyzer.py --method MM001
    python3 method_stack_analyzer.py --min-score 85
    python3 method_stack_analyzer.py --top-stacks 10

Example:
    # Show all method synergies
    python3 method_stack_analyzer.py

    # Find best stacks for APP_FACTORY
    python3 method_stack_analyzer.py --method MM001

    # Show only high-synergy stacks (score 85+)
    python3 method_stack_analyzer.py --min-score 85
"""

import argparse
import csv
import json
import logging
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "method_stack_analyzer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load CSV safely."""
    if not filepath.exists():
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_synergy_graph():
    """Build a graph of method synergies from cross-pollination matrix."""
    matrix = load_csv(LEDGER_DIR / "CROSS_POLLINATION_MATRIX.csv")
    methods = load_csv(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")

    method_names = {m.get("method_id"): m.get("method_name", "") for m in methods}
    method_status = {m.get("method_id"): m.get("status", "") for m in methods}

    graph = {}

    for row in matrix:
        mid = row.get("method_id", "")
        partners_str = row.get("synergy_partners", "")
        score = 0
        try:
            score = int(row.get("synergy_score", 0))
        except (ValueError, TypeError):
            score = 50  # Default if not numeric

        synergy_type = row.get("synergy_type", "")
        cross_sell = row.get("cross_sell_products", "")
        shared_audience = row.get("shared_audience", "")
        auto_combo = row.get("automation_combo", "").upper() == "TRUE"

        partners = [p.strip() for p in partners_str.split(",") if p.strip()]

        graph[mid] = {
            "name": method_names.get(mid, mid),
            "status": method_status.get(mid, "Unknown"),
            "partners": partners,
            "synergy_score": score,
            "synergy_type": synergy_type,
            "cross_sell": cross_sell,
            "shared_audience": shared_audience,
            "automation_combo": auto_combo,
        }

    return graph, method_names


def find_best_partners(graph, method_id, min_score=0):
    """Find the best synergy partners for a given method."""
    if method_id not in graph:
        return []

    method = graph[method_id]
    partner_scores = []

    for partner_id in method["partners"]:
        partner = graph.get(partner_id, {})
        # Calculate combined synergy
        score = method["synergy_score"]
        if partner:
            # Average of both directions
            score = (score + partner.get("synergy_score", 50)) // 2

        if score >= min_score:
            partner_scores.append({
                "partner_id": partner_id,
                "partner_name": partner.get("name", partner_id),
                "synergy_score": score,
                "synergy_type": method["synergy_type"],
                "automation_combo": method["automation_combo"],
                "shared_audience": method["shared_audience"],
            })

    partner_scores.sort(key=lambda x: x["synergy_score"], reverse=True)
    return partner_scores


def find_top_stacks(graph, method_names, top_n=10, min_score=80):
    """Find the top N method stacks by combined synergy."""
    all_methods = list(graph.keys())
    stacks = []

    # Check pairs
    for m1, m2 in combinations(all_methods, 2):
        g1 = graph.get(m1, {})
        g2 = graph.get(m2, {})

        # Check if they're synergy partners
        is_partner = m2 in g1.get("partners", []) or m1 in g2.get("partners", [])
        if not is_partner:
            continue

        score = (g1.get("synergy_score", 50) + g2.get("synergy_score", 50)) // 2
        if score >= min_score:
            stacks.append({
                "methods": [m1, m2],
                "method_names": [method_names.get(m1, m1), method_names.get(m2, m2)],
                "combined_score": score,
                "automation": g1.get("automation_combo", False) and g2.get("automation_combo", False),
                "type": f"{g1.get('synergy_type', '')} + {g2.get('synergy_type', '')}",
            })

    # Check triples (top synergy pairs extended)
    for m1, m2, m3 in combinations(all_methods, 3):
        g1 = graph.get(m1, {})
        g2 = graph.get(m2, {})
        g3 = graph.get(m3, {})

        # At least 2 of 3 must be synergy partners
        connections = 0
        if m2 in g1.get("partners", []) or m1 in g2.get("partners", []):
            connections += 1
        if m3 in g1.get("partners", []) or m1 in g3.get("partners", []):
            connections += 1
        if m3 in g2.get("partners", []) or m2 in g3.get("partners", []):
            connections += 1

        if connections >= 2:
            score = (g1.get("synergy_score", 50) + g2.get("synergy_score", 50) + g3.get("synergy_score", 50)) // 3
            if score >= min_score:
                stacks.append({
                    "methods": [m1, m2, m3],
                    "method_names": [method_names.get(m, m) for m in [m1, m2, m3]],
                    "combined_score": score,
                    "automation": all(graph.get(m, {}).get("automation_combo", False) for m in [m1, m2, m3]),
                    "type": "triple_stack",
                })

    stacks.sort(key=lambda x: x["combined_score"], reverse=True)
    return stacks[:top_n]


def print_synergy_report(graph, method_names, method_filter=None, min_score=0, top_stacks=10):
    """Print formatted synergy report."""
    print("\n" + "=" * 80)
    print("  METHOD SYNERGY ANALYZER")
    print("=" * 80)

    if method_filter:
        # Show partners for specific method
        partners = find_best_partners(graph, method_filter, min_score)
        method_name = method_names.get(method_filter, method_filter)
        print(f"\n  Synergy partners for {method_filter} ({method_name}):")
        print(f"  {'Partner':<25} {'Score':>6} {'Auto':>5}  Type")
        print("-" * 80)

        for p in partners:
            auto = "YES" if p["automation_combo"] else " no"
            print(
                f"  {p['partner_id']:<25} "
                f"{p['synergy_score']:>5} "
                f"{auto:>5}  "
                f"{p['synergy_type'][:40]}"
            )
    else:
        # Show top stacks
        stacks = find_top_stacks(graph, method_names, top_stacks, min_score)
        print(f"\n  {'--- TOP METHOD STACKS ---':^80}")
        print(f"  {'#':>3} {'Score':>6} {'Auto':>5}  Methods")
        print("-" * 80)

        for i, stack in enumerate(stacks, 1):
            auto = "YES" if stack["automation"] else " no"
            methods_str = " + ".join(f"{m}" for m in stack["method_names"])
            print(
                f"  {i:>3} "
                f"{stack['combined_score']:>5} "
                f"{auto:>5}  "
                f"{methods_str}"
            )

    # Method overview
    print(f"\n  {'--- METHOD OVERVIEW ---':^80}")
    for mid, data in sorted(graph.items()):
        print(
            f"  {mid:<15} {data['name']:<25} "
            f"Score: {data['synergy_score']:>3} | "
            f"Partners: {len(data['partners']):>2} | "
            f"Status: {data['status']}"
        )

    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze method synergies and find optimal stacks"
    )
    parser.add_argument("--method", type=str, default=None, help="Show partners for specific method")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum synergy score")
    parser.add_argument("--top-stacks", type=int, default=10, help="Number of top stacks to show")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    graph, method_names = build_synergy_graph()

    if not graph:
        logger.error("No synergy data found in CROSS_POLLINATION_MATRIX.csv")
        sys.exit(1)

    if args.output == "json":
        if args.method:
            result = find_best_partners(graph, args.method, args.min_score)
        else:
            result = find_top_stacks(graph, method_names, args.top_stacks, args.min_score)
        print(json.dumps(result, indent=2))
    else:
        print_synergy_report(graph, method_names, args.method, args.min_score, args.top_stacks)


if __name__ == "__main__":
    main()
