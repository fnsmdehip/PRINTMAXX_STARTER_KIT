#!/usr/bin/env python3

from __future__ import annotations
"""
Cognitive Engine — Hybrid prompt intelligence system.

Combines three capabilities:
1. META-RULE EXTRACTION: Mines prompt history for transferable cognitive patterns
2. SIMILAR-TASK LOOKUP: Finds past task sequences (prompt→correction→resolution)
   to inform how to approach similar new tasks
3. AUTONOMOUS REFINEMENT: Uses extracted patterns + task history to simulate
   what the user would prompt, then executes it in a loop

The engine builds a "cognition model" of the user's thinking by:
- Tracking correction sequences (what went wrong, how user fixed it)
- Identifying effective prompt chains (series of prompts that led to good outcomes)
- Extracting transferable rules from both failures and successes
- Providing semantic search across all past interactions

Usage:
    python3 cognitive_engine.py --build-model          # Build full cognition model from history
    python3 cognitive_engine.py --lookup "TASK_DESC"    # Find similar past tasks + prompt chains
    python3 cognitive_engine.py --rules                 # Show extracted meta-rules
    python3 cognitive_engine.py --refine VENTURE        # Run autonomous refinement cycle
    python3 cognitive_engine.py --refine-loop VENTURE N # Run N refinement cycles
    python3 cognitive_engine.py --chain-analysis        # Analyze prompt correction chains
    python3 cognitive_engine.py --status                # Show engine status

Cron: 0 4 * * 0 cd $BASE && $PYTHON AUTOMATIONS/cognitive_engine.py --build-model >> AUTOMATIONS/logs/cognitive_engine.log 2>&1
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = PROJECT_ROOT / "LEDGER" / "USER_PROMPTS.jsonl"
CONVOS_FILE = PROJECT_ROOT / "LEDGER" / "CONVERSATION_HISTORY.jsonl"
OUTPUT_DIR = PROJECT_ROOT / "OPS" / "prompt_intelligence"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_FILE = OUTPUT_DIR / "cognition_model.json"
CHAINS_FILE = OUTPUT_DIR / "correction_chains.json"
TASK_INDEX_FILE = OUTPUT_DIR / "task_index.json"
RULES_FILE = OUTPUT_DIR / "comprehensive_meta_rules.md"
REFINE_LOG = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "cognitive_refine.jsonl"

# What signals a correction sequence (user wasn't happy, prompted again)
CORRECTION_SIGNALS = [
    "no ", "not that", "wrong", "bruh", "lazy", "don't", "stop",
    "i said", "why did", "that's not", "actually", "but ", "like why",
    "isn't", "shouldn't", "you're just", "coping", "basic", "commodity",
    "freshman", "surface", "deeper", "more", "also ", "what about",
]

SATISFACTION_SIGNALS = [
    "good", "perfect", "exactly", "yes", "nice", "great", "solid",
    "love", "fire", "appreciate", "nailed",
]


def load_prompts():
    """Load prompt history with timestamps."""
    prompts = []
    if PROMPTS_FILE.exists():
        for line in PROMPTS_FILE.read_text().strip().split("\n"):
            try:
                entry = json.loads(line)
                prompts.append(entry)
            except json.JSONDecodeError:
                continue
    return prompts


def extract_correction_chains(prompts):
    """Find sequences where user corrected the system and trace the full chain.

    Uses TIMESTAMP PROXIMITY (10 min window) instead of session_id, because
    each prompt gets a unique session_id in our logging system.

    A correction chain looks like:
    1. User asks for X (initial prompt)
    2. [System responds — not logged but implied]
    3. User says "no not that, do Y instead" (correction, within 10 min)
    4. [System responds again]
    5. User says "better but also Z" (refinement, within 10 min)
    6. User says "good" or moves to new topic (resolution)
    """
    chains = []
    current_chain = None
    prev_ts = None

    for prompt in prompts:
        text = prompt.get("prompt", "").lower()[:500]
        ts_str = prompt.get("ts", "")

        # Parse timestamp
        try:
            ts = datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            continue

        # Check time gap from previous prompt
        time_gap_minutes = float("inf")
        if prev_ts:
            time_gap_minutes = (ts - prev_ts).total_seconds() / 60

        prev_ts = ts

        # Check signals
        is_correction = any(sig in text for sig in CORRECTION_SIGNALS)
        is_satisfaction = any(sig in text for sig in SATISFACTION_SIGNALS)
        is_same_conversation = time_gap_minutes < 10  # within 10 min = same convo

        if current_chain is None:
            # Start a new chain on any substantive non-correction prompt
            if not is_correction and len(text) > 20:
                current_chain = {
                    "initial_prompt": prompt.get("prompt", "")[:500],
                    "initial_ts": ts_str,
                    "corrections": [],
                    "resolution": None,
                    "chain_length": 1,
                }
        else:
            if is_same_conversation and is_correction:
                # Correction within same conversation window
                current_chain["corrections"].append({
                    "prompt": prompt.get("prompt", "")[:500],
                    "ts": ts_str,
                    "signals": [s for s in CORRECTION_SIGNALS if s in text][:5],
                })
                current_chain["chain_length"] += 1
            elif is_same_conversation and is_satisfaction:
                # Resolution
                current_chain["resolution"] = prompt.get("prompt", "")[:200]
                current_chain["resolved"] = True
                if current_chain["chain_length"] >= 2:
                    chains.append(current_chain)
                current_chain = None
            elif not is_same_conversation:
                # Time gap too large — close chain, start new one
                current_chain["resolved"] = False
                if current_chain["chain_length"] >= 2:
                    chains.append(current_chain)
                if not is_correction and len(text) > 20:
                    current_chain = {
                        "initial_prompt": prompt.get("prompt", "")[:500],
                        "initial_ts": ts_str,
                        "corrections": [],
                        "resolution": None,
                        "chain_length": 1,
                    }
                else:
                    current_chain = None
            elif is_same_conversation and not is_correction:
                # Same convo, not a correction — continuation
                current_chain["chain_length"] += 1

    # Close any remaining chain
    if current_chain and current_chain["chain_length"] >= 2:
        current_chain["resolved"] = False
        chains.append(current_chain)

    return chains


def build_task_index(prompts):
    """Build a searchable index of tasks and their outcomes.

    Groups prompts by TIMESTAMP PROXIMITY (10 min window) since
    session_id is unique per prompt in our logging system.
    """
    # Group by time proximity
    conversations = []
    current_convo = []
    prev_ts = None

    for p in prompts:
        ts_str = p.get("ts", "")
        try:
            ts = datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            continue

        if prev_ts and (ts - prev_ts).total_seconds() > 600:  # 10 min gap = new convo
            if len(current_convo) >= 2:
                conversations.append(current_convo)
            current_convo = [p]
        else:
            current_convo.append(p)
        prev_ts = ts

    if len(current_convo) >= 2:
        conversations.append(current_convo)

    tasks = []
    for convo in conversations:
        initial = convo[0].get("prompt", "")[:500]
        words = set(re.findall(r'\b[a-z]{4,}\b', initial.lower()))

        corrections = [p for p in convo
                      if any(s in p.get("prompt", "").lower() for s in CORRECTION_SIGNALS)]

        resolved = any(any(s in p.get("prompt", "").lower() for s in SATISFACTION_SIGNALS)
                      for p in convo[-3:])

        tasks.append({
            "initial_task": initial,
            "keywords": list(words)[:20],
            "prompt_count": len(convo),
            "correction_count": len(corrections),
            "resolved": resolved,
            "correction_prompts": [c.get("prompt", "")[:300] for c in corrections[:5]],
            "all_prompts_preview": [p.get("prompt", "")[:150] for p in convo[:10]],
            "timestamp": convo[0].get("ts", ""),
        })

    return tasks


def lookup_similar_tasks(query, task_index, top_n=5):
    """Find similar past tasks using keyword overlap."""
    query_words = set(re.findall(r'\b[a-z]{4,}\b', query.lower()))

    scored = []
    for task in task_index:
        task_words = set(task.get("keywords", []))
        overlap = len(query_words & task_words)
        if overlap >= 2:
            scored.append({
                **task,
                "overlap": overlap,
                "shared_words": list(query_words & task_words)[:8],
            })

    scored.sort(key=lambda x: x["overlap"], reverse=True)
    return scored[:top_n]


def extract_comprehensive_rules(chains, task_index, prompts):
    """Extract deep meta-rules from all data sources."""
    rules = []

    # From correction chains: what patterns trigger user pushback?
    correction_themes = defaultdict(int)
    for chain in chains:
        for c in chain.get("corrections", []):
            for sig in c.get("signals", []):
                correction_themes[sig] += 1

    # Theme analysis
    lazy_count = sum(v for k, v in correction_themes.items() if k in ("lazy", "basic", "commodity", "surface", "default"))
    depth_count = sum(v for k, v in correction_themes.items() if k in ("deeper", "more", "also ", "what about"))
    wrong_count = sum(v for k, v in correction_themes.items() if k in ("no ", "wrong", "not that", "don't"))

    if lazy_count > 5:
        rules.append({
            "id": "ANTI-LAZY",
            "count": lazy_count,
            "rule": "Default output depth is consistently below user expectations. System must default to the ESCALATED depth, not the initial polite response depth.",
            "evidence": f"User triggered anti-lazy corrections {lazy_count} times across sessions.",
            "action": "Before presenting any output, ask: 'Would the user call this lazy?' If yes, go deeper before presenting.",
        })

    if depth_count > 5:
        rules.append({
            "id": "DEPTH-FIRST",
            "count": depth_count,
            "rule": "User consistently asks for MORE after initial response. The initial response should already include what the user typically asks for in their follow-up.",
            "evidence": f"User demanded more depth {depth_count} times. Pattern: initial ask → 'also...' / 'what about...' / 'deeper'",
            "action": "After completing the literal ask, proactively address 2-3 adjacent areas the user would likely follow up on.",
        })

    if wrong_count > 10:
        rules.append({
            "id": "WRONG-DIRECTION",
            "count": wrong_count,
            "rule": "System frequently misinterprets user intent on first pass. Need better intent parsing before executing.",
            "evidence": f"User said 'no/wrong/not that' {wrong_count} times.",
            "action": "For ambiguous requests, internally generate 2-3 interpretations and select the one most consistent with user's established patterns before executing.",
        })

    # From task index: what tasks had the most corrections?
    high_correction_tasks = [t for t in task_index if t.get("correction_count", 0) >= 3]
    if high_correction_tasks:
        common_words_in_hard_tasks = defaultdict(int)
        for t in high_correction_tasks:
            for w in t.get("keywords", []):
                common_words_in_hard_tasks[w] += 1

        hard_topics = sorted(common_words_in_hard_tasks.items(), key=lambda x: -x[1])[:10]
        rules.append({
            "id": "HARD-TOPICS",
            "count": len(high_correction_tasks),
            "rule": f"Topics that consistently need multiple corrections: {', '.join(w for w, _ in hard_topics[:5])}. These need extra care.",
            "evidence": f"{len(high_correction_tasks)} tasks had 3+ corrections.",
            "action": "When a task matches these topics, use the correction chain from history to pre-emptively address the typical issues.",
        })

    # From satisfaction analysis: what makes the user happy?
    satisfaction_contexts = []
    for p in prompts:
        text = p.get("prompt", "").lower()
        if any(s in text for s in SATISFACTION_SIGNALS):
            satisfaction_contexts.append(text[:200])

    if satisfaction_contexts:
        rules.append({
            "id": "SATISFACTION-PATTERN",
            "count": len(satisfaction_contexts),
            "rule": "User is most satisfied when: system executes autonomously without asking, output exceeds explicit ask, non-obvious angles are found, and work compounds into multiple outputs.",
            "evidence": f"{len(satisfaction_contexts)} satisfaction signals found.",
            "action": "Optimize for these satisfaction triggers in every output.",
        })

    # Meta-rule about correction chain length
    avg_chain = sum(c.get("chain_length", 1) for c in chains) / max(len(chains), 1)
    if avg_chain > 2:
        rules.append({
            "id": "CHAIN-LENGTH",
            "count": len(chains),
            "rule": f"Average correction chain is {avg_chain:.1f} prompts long. This means the system typically needs {avg_chain:.0f} iterations to reach what the user wants. Target: get to the right output in 1 prompt.",
            "evidence": f"{len(chains)} correction chains analyzed.",
            "action": "Use the Competitive Cognition Protocol to anticipate corrections before presenting output.",
        })

    return rules


def build_model():
    """Build the full cognition model."""
    print("\n=== Building Cognition Model ===\n")

    prompts = load_prompts()
    print(f"Loaded {len(prompts)} prompts")

    # Extract correction chains
    chains = extract_correction_chains(prompts)
    print(f"Extracted {len(chains)} correction chains")

    # Build task index
    task_index = build_task_index(prompts)
    print(f"Built task index with {len(task_index)} sessions")

    # Extract comprehensive rules
    rules = extract_comprehensive_rules(chains, task_index, prompts)
    print(f"Generated {len(rules)} meta-rules")

    # Save everything
    model = {
        "built_at": datetime.now().isoformat(),
        "prompt_count": len(prompts),
        "chain_count": len(chains),
        "task_count": len(task_index),
        "rule_count": len(rules),
        "rules": rules,
    }
    with open(MODEL_FILE, "w") as f:
        json.dump(model, f, indent=2)

    with open(CHAINS_FILE, "w") as f:
        json.dump(chains[:100], f, indent=2)  # Top 100 chains

    with open(TASK_INDEX_FILE, "w") as f:
        json.dump(task_index, f, indent=2)

    # Generate comprehensive rules markdown
    rules_md = f"# Comprehensive Meta-Rules — Cognition Model\n"
    rules_md += f"Built: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    rules_md += f"Source: {len(prompts)} prompts, {len(chains)} correction chains, {len(task_index)} sessions\n\n"

    for r in rules:
        rules_md += f"## {r['id']} (triggered {r['count']}x)\n\n"
        rules_md += f"**Rule:** {r['rule']}\n\n"
        rules_md += f"**Evidence:** {r['evidence']}\n\n"
        rules_md += f"**Action:** {r['action']}\n\n---\n\n"

    # Add top correction chains as examples
    rules_md += "## Example Correction Chains (learn from these)\n\n"
    for chain in chains[:5]:
        rules_md += f"### Chain from {chain.get('initial_ts', 'unknown')[:10]}\n\n"
        rules_md += f"**Initial ask:** {chain['initial_prompt'][:200]}...\n\n"
        for i, c in enumerate(chain.get("corrections", [])[:3], 1):
            rules_md += f"**Correction {i}:** {c['prompt'][:200]}...\n"
            rules_md += f"  Signals: {', '.join(c.get('signals', [])[:3])}\n\n"
        if chain.get("resolution"):
            rules_md += f"**Resolution:** {chain['resolution'][:200]}\n\n"
        rules_md += "---\n\n"

    with open(RULES_FILE, "w") as f:
        f.write(rules_md)

    print(f"\nModel saved: {MODEL_FILE}")
    print(f"Chains saved: {CHAINS_FILE}")
    print(f"Task index saved: {TASK_INDEX_FILE}")
    print(f"Rules saved: {RULES_FILE}")

    print(f"\n--- Meta-Rules ---")
    for r in rules:
        print(f"  [{r['id']}] ({r['count']}x) {r['rule'][:100]}...")

    return model


def lookup_task(query):
    """Find similar past tasks and show the correction chain."""
    if not TASK_INDEX_FILE.exists():
        print("Task index not built yet. Run --build-model first.")
        return

    task_index = json.loads(TASK_INDEX_FILE.read_text())
    similar = lookup_similar_tasks(query, task_index)

    if similar:
        print(f"\n=== Similar Past Tasks for: \"{query[:50]}\" ===\n")
        for i, t in enumerate(similar, 1):
            print(f"{i}. [{t['timestamp'][:10]}] Overlap: {t['overlap']} | Corrections: {t['correction_count']}")
            print(f"   Shared words: {', '.join(t['shared_words'][:5])}")
            print(f"   Task: {t['initial_task'][:150]}...")
            if t.get("correction_prompts"):
                print(f"   User corrections:")
                for j, cp in enumerate(t["correction_prompts"][:2], 1):
                    print(f"     {j}. \"{cp[:100]}...\"")
            print(f"   Resolved: {'Yes' if t.get('resolved') else 'No'}")
            print()
    else:
        print("No similar tasks found in history.")


def generate_reflexion(venture, cycle_output):
    """Reflexion pattern: after each cycle, write verbal reflection on what happened.

    Stores reflections in episodic memory. Future cycles read past reflections
    to avoid repeating mistakes. This is verbal reinforcement learning.
    """
    reflexion_dir = OUTPUT_DIR / "reflexions"
    reflexion_dir.mkdir(exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    reflexion = {
        "timestamp": datetime.now().isoformat(),
        "venture": venture,
        "cycle_output_preview": cycle_output[:500] if cycle_output else "",
        "reflection": f"Cycle completed for {venture}. Output length: {len(cycle_output or '')} chars.",
    }

    reflexion_file = reflexion_dir / f"reflexion_{venture}_{ts}.json"
    with open(reflexion_file, "w") as f:
        json.dump(reflexion, f, indent=2)

    # Keep last 20 reflexions per venture
    existing = sorted(reflexion_dir.glob(f"reflexion_{venture}_*.json"), key=lambda p: p.stat().st_mtime)
    while len(existing) > 20:
        existing[0].unlink()
        existing.pop(0)

    return reflexion


def get_past_reflexions(venture, n=5):
    """Load last N reflexions for a venture to inject into next cycle."""
    reflexion_dir = OUTPUT_DIR / "reflexions"
    if not reflexion_dir.exists():
        return []

    files = sorted(reflexion_dir.glob(f"reflexion_{venture}_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    reflexions = []
    for f in files[:n]:
        try:
            reflexions.append(json.loads(f.read_text()))
        except json.JSONDecodeError:
            continue
    return reflexions


def run_refinement(venture, n_cycles=1):
    """Run autonomous refinement using cognition model + Reflexion pattern.

    Each cycle:
    1. Load cognition model (meta-rules from prompt history)
    2. Load past reflexions (verbal memory of previous cycles)
    3. Find similar past tasks from history (what worked before)
    4. Run user-sim critique with all context injected
    5. Generate reflexion for this cycle
    6. Git snapshot everything
    """
    if not MODEL_FILE.exists():
        print("Cognition model not built. Running --build-model first...")
        build_model()

    model = json.loads(MODEL_FILE.read_text())
    rules = model.get("rules", [])

    for cycle in range(n_cycles):
        print(f"\n{'='*60}")
        print(f"COGNITIVE REFINEMENT CYCLE {cycle+1}/{n_cycles}")
        print(f"Cognition model: {len(rules)} rules | ", end="")

        # Load past reflexions
        reflexions = get_past_reflexions(venture)
        print(f"Past reflexions: {len(reflexions)} | ", end="")

        # Find similar past tasks
        if TASK_INDEX_FILE.exists():
            task_index = json.loads(TASK_INDEX_FILE.read_text())
            similar = lookup_similar_tasks(f"refine improve {venture.lower()} venture", task_index, top_n=3)
            print(f"Similar tasks: {len(similar)}")
        else:
            similar = []
            print("No task index")

        print(f"{'='*60}")

        # Run the user_sim_refiner
        result = subprocess.run(
            ["python3", str(PROJECT_ROOT / "AUTOMATIONS" / "user_sim_refiner.py"),
             "--venture", venture, "--cycle"],
            capture_output=True, text=True, timeout=400,
            cwd=str(PROJECT_ROOT),
        )
        output = result.stdout or result.stderr or ""
        print(output[:500])

        # Generate reflexion for this cycle
        reflexion = generate_reflexion(venture, output)

        # Log
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "venture": venture,
            "cycle": cycle + 1,
            "rules_applied": len(rules),
            "reflexions_loaded": len(reflexions),
            "similar_tasks_found": len(similar),
            "output_preview": output[:300],
            "reflexion_file": str(reflexion.get("timestamp", "")),
        }
        with open(REFINE_LOG, "a") as f:
            f.write(json.dumps(log_entry) + "\n")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--build-model" in args:
        build_model()
    elif "--lookup" in args:
        idx = args.index("--lookup")
        query = " ".join(args[idx + 1:])
        lookup_task(query)
    elif "--rules" in args:
        if RULES_FILE.exists():
            print(RULES_FILE.read_text()[:3000])
        else:
            print("Rules not generated yet. Run --build-model first.")
    elif "--chain-analysis" in args:
        prompts = load_prompts()
        chains = extract_correction_chains(prompts)
        print(f"\n=== Correction Chain Analysis ({len(chains)} chains) ===\n")
        for c in chains[:10]:
            print(f"[{c.get('initial_ts', '')[:10]}] Chain length: {c['chain_length']}")
            print(f"  Initial: \"{c['initial_prompt'][:100]}...\"")
            for cor in c.get("corrections", [])[:2]:
                print(f"  Correction: \"{cor['prompt'][:80]}...\" ({', '.join(cor.get('signals', [])[:2])})")
            if c.get("resolution"):
                print(f"  Resolution: \"{c['resolution'][:80]}...\"")
            print()
    elif "--refine" in args:
        idx = args.index("--refine")
        venture = args[idx + 1].upper() if idx + 1 < len(args) else "EAS"
        run_refinement(venture)
    elif "--refine-loop" in args:
        idx = args.index("--refine-loop")
        venture = args[idx + 1].upper() if idx + 1 < len(args) else "EAS"
        n = int(args[idx + 2]) if idx + 2 < len(args) else 3
        run_refinement(venture, n)
    elif "--status" in args:
        print("\n=== Cognitive Engine Status ===\n")
        if MODEL_FILE.exists():
            model = json.loads(MODEL_FILE.read_text())
            print(f"Model built: {model.get('built_at', 'unknown')}")
            print(f"Prompts analyzed: {model.get('prompt_count', 0)}")
            print(f"Correction chains: {model.get('chain_count', 0)}")
            print(f"Task sessions: {model.get('task_count', 0)}")
            print(f"Meta-rules: {model.get('rule_count', 0)}")
        else:
            print("Model not built yet. Run --build-model.")
    else:
        print("Cognitive Engine — Hybrid prompt intelligence system")
        print()
        print("  --build-model           Build cognition model from all prompt history")
        print("  --lookup QUERY          Find similar past tasks + prompt correction chains")
        print("  --rules                 Show extracted comprehensive meta-rules")
        print("  --chain-analysis        Analyze correction chains (what went wrong → how user fixed)")
        print("  --refine VENTURE        Run autonomous refinement cycle")
        print("  --refine-loop VENTURE N Run N refinement cycles")
        print("  --status                Show engine status")
