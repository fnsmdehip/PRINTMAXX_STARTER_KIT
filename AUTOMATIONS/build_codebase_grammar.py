#!/usr/bin/env python3
"""
CODEBASE GRAMMAR BUILDER — LLM-optimized representation of the PRINTMAXX system.

Generates a compact, pre-linked grammar file that gives any LLM instant
omniscience over the entire automation system WITHOUT tool calls.

Output: OPS/CODEBASE_GRAMMAR.md — a single file that, when loaded into context,
lets the LLM know every function, every data flow, every dependency, every
state file, every CLI command, and every cross-script interaction.

Token target: <15K tokens for full system understanding (vs 100K+ raw source).

Usage:
    python3 build_codebase_grammar.py              # Build grammar
    python3 build_codebase_grammar.py --json        # Output as JSON
    python3 build_codebase_grammar.py --stats       # Show compression stats
"""

from __future__ import annotations

import ast
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
OPS = PROJECT / "OPS"


def _safe_path(target: str | Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved

# Every script that matters
CORE_SCRIPTS = {
    "ceo_agent.py": "24/7 orchestrator — scores ops, makes PROMOTE/ENHANCE/CREATE/KILL/DISCOVER decisions, delegates to ventures",
    "agent_swarm.py": "22 operational agents — generates launchd plists, manages health, AGENT_VENTURE_MAP for intelligence injection",
    "venture_autonomy.py": "8 venture types — universal execution engine, self-managing schedules, SelfManager auto-adjusts",
    "intelligence_router.py": "central intelligence hub — 484 docs, 14,799 alpha, 16 CSVs across 9 ventures",
    "daily_engagement_planner.py": "warmup-aware daily action plan — posts, replies, likes, follows with timing",
    "twitter_warmup_poster.py": "21-day warmup poster — 5 phases (LURK/ENGAGE/SOFT_POST/RAMP/FULL_OPS)",
    "daily_digest.py": "human-readable system activity summary — alpha, content, agents, changes",
    "alpha_query.py": "venture-based alpha queries with ROI normalization — search/filter 14,799 entries",
    "loop_closer.py": "closes open loops — decision execution, feedback tracking, pipeline advancement",
    "decision_engine.py": "closed-loop decision processing — pending data → actions",
    "alpha_auto_processor.py": "auto-processes ALPHA_STAGING.csv — routes to ventures/OPS/cron/archive",
    "system_health_monitor.py": "health checks — agents, cron, disk, processes",
    "daily_research_orchestrator.py": "research pipeline — scrapers, alpha review, content generation",
    "quality_gate.py": "hard quality gate — blocks slop before deployment, rewrites bad content",
    "twitter_alpha_scraper.py": "scrapes 133 Twitter accounts via Brave cookies + Playwright",
    "background_reddit_scraper.py": "Reddit JSON API scraper — no auth needed",
    "compliance_scanner.py": "FTC/platform compliance auditing",
    "memory_manager.py": "filesystem-based memory management",
    "wire_missed_intelligence.py": "parses MISSED_INTELLIGENCE_SCAN.md → updates catalog",
    "build_codebase_grammar.py": "LLM-optimized codebase representation — AST parsing, 100x+ compression",
}


def extract_script_grammar(script_path: Path, description: str) -> dict[str, Any]:
    """Extract a compact grammar representation of a Python script."""
    try:
        source = script_path.read_text()
        tree = ast.parse(source)
    except Exception as e:
        return {"error": str(e)}

    grammar = {
        "desc": description,
        "lines": len(source.splitlines()),
        "classes": [],
        "functions": [],
        "cli": [],
        "state_files": [],
        "reads": [],
        "writes": [],
        "calls_scripts": [],
        "constants": [],
    }

    # Extract classes with their methods
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    sig = f"{item.name}({', '.join(a.arg for a in item.args.args if a.arg != 'self')})"
                    methods.append(sig)
            grammar["classes"].append({
                "name": node.name,
                "methods": methods[:20],  # Cap at 20
            })

    # Extract top-level functions with signatures
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            # Get first line of docstring if exists
            doc = ""
            if (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, (ast.Constant, ast.Str))):
                doc_val = node.body[0].value
                doc_text = doc_val.value if isinstance(doc_val, ast.Constant) else doc_val.s
                doc = doc_text.split("\n")[0].strip()[:80]
            grammar["functions"].append({
                "name": node.name,
                "args": args,
                "doc": doc,
            })

    # Extract CLI arguments (argparse)
    for line in source.splitlines():
        match = re.search(r'add_argument\(["\'](-[-\w]+)', line)
        if match:
            grammar["cli"].append(match.group(1))

    # Extract state/data file references
    state_patterns = [
        (r'STATE_FILE\s*=\s*.*?["\'](.+?)["\']', "state_files"),
        (r'([A-Z_]+_FILE)\s*=\s*.*?["\'](.+?)["\']', "state_files"),
    ]
    for line in source.splitlines():
        # State files
        for pat, key in state_patterns:
            m = re.search(pat, line)
            if m:
                grammar[key].append(m.group(1))

        # File reads/writes
        if ".csv" in line or ".json" in line or ".md" in line:
            files = re.findall(r'["\']([A-Za-z_/]+\.(?:csv|json|md))["\']', line)
            for f in files:
                if any(w in line for w in ["write", "dump", "save", '"w"', '"a"', "append"]):
                    grammar["writes"].append(f)
                elif any(r in line for r in ["read", "load", "open", "exists"]):
                    grammar["reads"].append(f)

        # Cross-script calls
        for other_script in CORE_SCRIPTS:
            if other_script in line and other_script != script_path.name:
                if "subprocess" in line or "run(" in line:
                    if other_script not in grammar["calls_scripts"]:
                        grammar["calls_scripts"].append(other_script)

    # Extract important constants
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper() and len(target.id) > 3:
                    if isinstance(node.value, ast.Dict):
                        grammar["constants"].append(f"{target.id} = {{...}} ({len(node.value.keys)} keys)")
                    elif isinstance(node.value, (ast.List, ast.Set)):
                        grammar["constants"].append(f"{target.id} = [...] ({len(node.value.elts)} items)")
                    elif isinstance(node.value, ast.Constant):
                        val = repr(node.value.value)[:50]
                        grammar["constants"].append(f"{target.id} = {val}")

    # Deduplicate
    grammar["reads"] = list(set(grammar["reads"]))[:15]
    grammar["writes"] = list(set(grammar["writes"]))[:15]
    grammar["state_files"] = list(set(grammar["state_files"]))[:10]

    return grammar


def build_grammar() -> dict[str, Any]:
    """Build the full codebase grammar."""
    grammar = {
        "generated": datetime.now().isoformat(),
        "project": "PRINTMAXX",
        "total_scripts": len(CORE_SCRIPTS),
        "scripts": {},
        "data_flows": [],
        "execution_hierarchy": {
            "level_0_orchestrator": ["ceo_agent.py"],
            "level_1_engines": ["venture_autonomy.py", "agent_swarm.py", "decision_engine.py"],
            "level_2_intelligence": ["intelligence_router.py", "alpha_query.py", "daily_digest.py"],
            "level_3_execution": ["twitter_warmup_poster.py", "daily_engagement_planner.py",
                                  "alpha_auto_processor.py", "daily_research_orchestrator.py"],
            "level_4_collection": ["twitter_alpha_scraper.py", "background_reddit_scraper.py"],
            "level_5_quality": ["quality_gate.py", "compliance_scanner.py", "system_health_monitor.py"],
            "level_6_maintenance": ["loop_closer.py", "memory_manager.py", "wire_missed_intelligence.py", "build_codebase_grammar.py"],
        },
        "state_topology": {
            "ceo_state": "AUTOMATIONS/agent/ceo_agent/ceo_state.json",
            "swarm_state": "AUTOMATIONS/agent/swarm/swarm_state.json",
            "autonomy_state": "AUTOMATIONS/agent/autonomy/autonomy_state.json",
            "warmup_state": "AUTOMATIONS/agent/twitter_warmup_state.json",
            "alpha_staging": "LEDGER/ALPHA_STAGING.csv",
            "intelligence_catalog": "OPS/INTELLIGENCE_CATALOG.json",
            "decisions_log": "AUTOMATIONS/agent/ceo_agent/decisions.jsonl",
            "missions_log": "AUTOMATIONS/agent/missions.jsonl",
            "message_bus": "AUTOMATIONS/agent/message_bus.jsonl",
        },
        "cron_schedule": {
            "6:00 AM": "twitter_alpha_scraper (133 accounts)",
            "6:15 AM": "background_reddit_scraper",
            "6:30 AM": "alpha_auto_processor --process-new",
            "6:45 AM": "daily_digest --days 1 --save",
            "7:00 AM": "daily_engagement_planner --save",
            "midnight": "twitter_warmup_poster --advance",
            "every 2h": "ceo_agent cycle, loop_closer --cycle",
            "every 4h": "agent_swarm swarm_brain cycle",
        },
    }

    for script_name, desc in CORE_SCRIPTS.items():
        script_path = AUTOMATIONS / script_name
        if script_path.exists():
            grammar["scripts"][script_name] = extract_script_grammar(script_path, desc)

    # Build data flow map
    all_writes = {}
    all_reads = {}
    for name, info in grammar["scripts"].items():
        if isinstance(info, dict) and "writes" in info:
            for f in info["writes"]:
                all_writes.setdefault(f, []).append(name)
            for f in info["reads"]:
                all_reads.setdefault(f, []).append(name)

    # Find producer-consumer relationships
    for f in set(list(all_writes.keys()) + list(all_reads.keys())):
        producers = all_writes.get(f, [])
        consumers = all_reads.get(f, [])
        if producers and consumers:
            grammar["data_flows"].append({
                "file": f,
                "producers": producers,
                "consumers": consumers,
            })

    return grammar


def render_markdown(grammar: dict[str, Any]) -> str:
    """Render grammar as compact markdown for LLM consumption."""
    lines = []
    lines.append("# PRINTMAXX CODEBASE GRAMMAR")
    lines.append(f"# Generated: {grammar['generated']}")
    lines.append(f"# {grammar['total_scripts']} scripts | Instant system understanding")
    lines.append("")

    # Execution hierarchy
    lines.append("## EXECUTION HIERARCHY")
    for level, scripts in grammar["execution_hierarchy"].items():
        lines.append(f"  {level}: {', '.join(scripts)}")
    lines.append("")

    # State topology
    lines.append("## STATE FILES")
    for name, path in grammar["state_topology"].items():
        lines.append(f"  {name}: {path}")
    lines.append("")

    # Cron schedule
    lines.append("## CRON SCHEDULE")
    for time, what in grammar["cron_schedule"].items():
        lines.append(f"  {time}: {what}")
    lines.append("")

    # Scripts
    lines.append("## SCRIPTS")
    lines.append("")
    for name, info in grammar["scripts"].items():
        if isinstance(info, dict) and "error" not in info:
            lines.append(f"### {name} ({info['lines']}L) — {info['desc']}")

            if info["classes"]:
                for cls in info["classes"]:
                    methods_str = ", ".join(cls["methods"][:10])
                    lines.append(f"  class {cls['name']}: [{methods_str}]")

            if info["functions"]:
                fn_strs = []
                for fn in info["functions"][:15]:
                    args = ", ".join(fn["args"][:4])
                    doc = f" — {fn['doc']}" if fn["doc"] else ""
                    fn_strs.append(f"{fn['name']}({args}){doc}")
                lines.append(f"  fn: {' | '.join(fn_strs)}")

            if info["cli"]:
                lines.append(f"  cli: {' '.join(info['cli'])}")

            if info["calls_scripts"]:
                lines.append(f"  calls: {', '.join(info['calls_scripts'])}")

            if info["reads"]:
                lines.append(f"  reads: {', '.join(info['reads'][:8])}")
            if info["writes"]:
                lines.append(f"  writes: {', '.join(info['writes'][:8])}")

            lines.append("")

    # Data flows
    if grammar["data_flows"]:
        lines.append("## DATA FLOWS (producer → file → consumer)")
        for flow in grammar["data_flows"]:
            lines.append(f"  {','.join(flow['producers'])} → {flow['file']} → {','.join(flow['consumers'])}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build codebase grammar")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--stats", action="store_true", help="Show compression stats")
    args = parser.parse_args()

    grammar = build_grammar()

    if args.json:
        out_path = _safe_path(OPS / "CODEBASE_GRAMMAR.json")
        with open(out_path, "w") as f:
            json.dump(grammar, f, indent=2)
        print(f"Saved to {out_path}")
    elif args.stats:
        md = render_markdown(grammar)
        total_source_lines = sum(
            info.get("lines", 0)
            for info in grammar["scripts"].values()
            if isinstance(info, dict)
        )
        grammar_lines = len(md.splitlines())
        print(f"Source lines:  {total_source_lines:,}")
        print(f"Grammar lines: {grammar_lines}")
        print(f"Compression:   {total_source_lines / grammar_lines:.1f}x")
        print(f"Est. tokens:   ~{len(md.split()) * 1.3:.0f}")
    else:
        md = render_markdown(grammar)
        out_path = _safe_path(OPS / "CODEBASE_GRAMMAR.md")
        with open(out_path, "w") as f:
            f.write(md)
        print(f"Saved to {out_path}")
        print(f"Lines: {len(md.splitlines())}")

        # Also save JSON version
        json_path = _safe_path(OPS / "CODEBASE_GRAMMAR.json")
        with open(json_path, "w") as f:
            json.dump(grammar, f, indent=2)


if __name__ == "__main__":
    main()
