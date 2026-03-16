#!/usr/bin/env python3
"""
Prompt Pattern Miner — Extracts meta-rules from user's prompt history.

Reads USER_PROMPTS.jsonl (1,510+ prompts) and CONVERSATION_HISTORY.jsonl (12K+ entries).
Mines for: recurring patterns, correction sequences, escalation triggers,
effective prompting styles, and transferable meta-rules.

Also provides semantic search: before executing a task, find similar past prompts
and what approach worked.

Usage:
    python3 prompt_pattern_miner.py --mine              # Extract all patterns
    python3 prompt_pattern_miner.py --similar "QUERY"   # Find similar past prompts
    python3 prompt_pattern_miner.py --corrections        # Find correction sequences (user pushback)
    python3 prompt_pattern_miner.py --escalations        # Find escalation patterns
    python3 prompt_pattern_miner.py --effective          # Find most effective prompt styles
    python3 prompt_pattern_miner.py --rules              # Generate meta-rules from patterns
    python3 prompt_pattern_miner.py --inject             # Update SOUL.md/rules with new patterns

Cron: 0 3 * * 0 cd $BASE && $PYTHON AUTOMATIONS/prompt_pattern_miner.py --mine >> AUTOMATIONS/logs/prompt_miner.log 2>&1
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = PROJECT_ROOT / "LEDGER" / "USER_PROMPTS.jsonl"
CONVOS_FILE = PROJECT_ROOT / "LEDGER" / "CONVERSATION_HISTORY.jsonl"
OUTPUT_DIR = PROJECT_ROOT / "OPS" / "prompt_intelligence"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PATTERNS_FILE = OUTPUT_DIR / "extracted_patterns.json"
RULES_FILE = OUTPUT_DIR / "mined_meta_rules.md"
SIMILAR_CACHE = OUTPUT_DIR / "prompt_index.json"

# Markers of user pushback / correction (these are gold — they reveal where the system fails)
CORRECTION_MARKERS = [
    "no not", "don't do that", "that's not what", "bruh", "lazy", "wrong",
    "i said", "not that", "why did you", "stop", "you're just", "coping",
    "didn't ask", "too much", "too generic", "not good", "freshman",
    "basic bitch", "secret sauce", "giving away", "just the old",
    "same old", "commodity", "default", "aggregate", "popular",
    "actually think", "critically", "not just", "deeper", "above and beyond",
    "surprise me", "proactive", "use ur best", "best judgment",
    "jimmy neutron", "brainblast", "ultrathink",
]

# Markers of satisfaction / effective prompts
SATISFACTION_MARKERS = [
    "good boy", "perfect", "exactly", "yes that", "love it", "fire",
    "this is what", "appreciate", "nice", "great", "solid", "nailed",
]

# Markers of escalation (user pushing for more depth)
ESCALATION_MARKERS = [
    "like why", "isn't our", "but why", "what about", "also",
    "you've only scratched", "think bigger", "think harder",
    "ralph loop", "agent teams", "surprise me", "above and beyond",
    "i feel like", "shouldn't we", "what if", "best latest",
    "every case every kind of nuance", "loop for a while",
]


def load_prompts():
    """Load all user prompts."""
    prompts = []
    if PROMPTS_FILE.exists():
        for line in PROMPTS_FILE.read_text().strip().split("\n"):
            try:
                prompts.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return prompts


def load_conversations():
    """Load conversation history."""
    convos = []
    if CONVOS_FILE.exists():
        for line in CONVOS_FILE.read_text().strip().split("\n"):
            try:
                convos.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return convos


def find_corrections(prompts):
    """Find prompts where user corrected/pushed back on the system."""
    corrections = []
    for p in prompts:
        text = p.get("prompt", "").lower()
        triggered = [m for m in CORRECTION_MARKERS if m in text]
        if triggered:
            corrections.append({
                "timestamp": p.get("ts", ""),
                "prompt": p.get("prompt", "")[:500],
                "markers": triggered,
                "marker_count": len(triggered),
            })
    # Sort by marker density (most pushback first)
    corrections.sort(key=lambda x: x["marker_count"], reverse=True)
    return corrections


def find_escalations(prompts):
    """Find prompts where user pushed for deeper thinking."""
    escalations = []
    for p in prompts:
        text = p.get("prompt", "").lower()
        triggered = [m for m in ESCALATION_MARKERS if m in text]
        if triggered:
            escalations.append({
                "timestamp": p.get("ts", ""),
                "prompt": p.get("prompt", "")[:500],
                "markers": triggered,
            })
    return escalations


def find_satisfactions(prompts):
    """Find prompts where user expressed satisfaction."""
    satisfactions = []
    for p in prompts:
        text = p.get("prompt", "").lower()
        triggered = [m for m in SATISFACTION_MARKERS if m in text]
        if triggered:
            satisfactions.append({
                "timestamp": p.get("ts", ""),
                "prompt": p.get("prompt", "")[:500],
                "markers": triggered,
            })
    return satisfactions


def extract_keyword_patterns(prompts):
    """Find recurring themes and keywords across prompts."""
    all_words = Counter()
    bigrams = Counter()
    for p in prompts:
        text = p.get("prompt", "").lower()
        words = re.findall(r'\b[a-z]{4,}\b', text)
        all_words.update(words)
        for i in range(len(words) - 1):
            bigrams[f"{words[i]} {words[i+1]}"] += 1

    # Filter out common words
    common = {"that", "this", "with", "from", "have", "like", "just", "what",
              "make", "sure", "also", "want", "need", "think", "about", "them",
              "their", "they", "would", "could", "should", "every", "some",
              "other", "then", "when", "into", "more", "been", "will", "your",
              "does", "know", "good", "best", "dont"}
    filtered = {k: v for k, v in all_words.items() if k not in common and v >= 3}
    return dict(Counter(filtered).most_common(50)), dict(bigrams.most_common(30))


def find_similar_prompts(query, prompts, top_n=5):
    """Find prompts similar to a query using keyword overlap."""
    query_words = set(re.findall(r'\b[a-z]{4,}\b', query.lower()))
    scored = []
    for p in prompts:
        text = p.get("prompt", "")
        prompt_words = set(re.findall(r'\b[a-z]{4,}\b', text.lower()))
        overlap = len(query_words & prompt_words)
        if overlap >= 2:
            scored.append({
                "timestamp": p.get("ts", ""),
                "prompt": text[:300],
                "overlap": overlap,
                "shared_words": list(query_words & prompt_words)[:10],
            })
    scored.sort(key=lambda x: x["overlap"], reverse=True)
    return scored[:top_n]


def generate_meta_rules(corrections, escalations, satisfactions):
    """Generate meta-rules from pattern analysis."""
    rules = []

    # From corrections: what patterns trigger user pushback?
    correction_themes = Counter()
    for c in corrections:
        for m in c["markers"]:
            correction_themes[m] += 1

    top_corrections = correction_themes.most_common(10)
    for marker, count in top_corrections:
        if marker in ("lazy", "basic bitch", "commodity", "default", "aggregate", "popular"):
            rules.append(f"ANTI-LAZY (triggered {count}x): User pushes back when output defaults to popular/generic solutions instead of critically analyzing for best. Always justify WHY something is recommended, not just that it's popular.")
        elif marker in ("bruh", "wrong", "no not"):
            rules.append(f"DIRECT-CORRECTION (triggered {count}x): User gives direct corrections — extract the rule and never repeat the mistake.")
        elif marker in ("surprise me", "above and beyond", "proactive"):
            rules.append(f"DEPTH-DEMAND (triggered {count}x): User expects output BEYOND the literal ask. Find adjacent improvements, non-obvious angles, and implicit subtasks.")
        elif marker in ("secret sauce", "giving away"):
            rules.append(f"PROTECT-IP (triggered {count}x): User wants to protect proprietary knowledge. Never expose specific tool names, methodologies, or internal architecture to public-facing outputs.")
        elif marker in ("ultrathink", "jimmy neutron", "brainblast"):
            rules.append(f"MAX-EFFORT (triggered {count}x): User explicitly demands maximum reasoning depth. Use extended thinking, multi-perspective analysis, and iterative refinement.")

    # From escalations: what depth patterns work?
    if len(escalations) > 5:
        rules.append(f"ESCALATION-PATTERN: User escalated {len(escalations)} times across sessions. The system consistently under-delivers on first pass. Default response should be at the depth of what the user typically escalates TO, not what they initially ask for.")

    # From satisfactions: what makes the user happy?
    if satisfactions:
        rules.append(f"SATISFACTION-TRIGGERS: User expressed satisfaction {len(satisfactions)} times. Common context: when system executes autonomously, when output exceeds expectations, when system finds non-obvious angles.")

    return rules


def mine_all():
    """Run full pattern mining pipeline."""
    print("\n=== Prompt Pattern Miner ===\n")
    prompts = load_prompts()
    print(f"Loaded {len(prompts)} prompts")

    # Find patterns
    corrections = find_corrections(prompts)
    escalations = find_escalations(prompts)
    satisfactions = find_satisfactions(prompts)
    keywords, bigrams = extract_keyword_patterns(prompts)

    print(f"Corrections (user pushback): {len(corrections)}")
    print(f"Escalations (depth demands): {len(escalations)}")
    print(f"Satisfactions: {len(satisfactions)}")

    # Generate meta-rules
    rules = generate_meta_rules(corrections, escalations, satisfactions)

    # Save patterns
    patterns = {
        "mined_at": datetime.now().isoformat(),
        "total_prompts": len(prompts),
        "correction_count": len(corrections),
        "escalation_count": len(escalations),
        "satisfaction_count": len(satisfactions),
        "top_corrections": corrections[:20],
        "top_escalations": escalations[:15],
        "satisfactions": satisfactions[:10],
        "top_keywords": dict(list(keywords.items())[:30]),
        "top_bigrams": dict(list(bigrams.items())[:20]),
        "meta_rules": rules,
    }
    with open(PATTERNS_FILE, "w") as f:
        json.dump(patterns, f, indent=2)

    # Save rules as markdown
    rules_md = f"# Mined Meta-Rules — {datetime.now().strftime('%Y-%m-%d')}\n\n"
    rules_md += f"Source: {len(prompts)} prompts analyzed\n\n"
    for i, rule in enumerate(rules, 1):
        rules_md += f"{i}. {rule}\n\n"

    rules_md += "\n## Top Correction Triggers (what makes user push back)\n\n"
    for c in corrections[:10]:
        rules_md += f"- [{c['timestamp'][:10]}] Markers: {', '.join(c['markers'][:3])} — \"{c['prompt'][:100]}...\"\n"

    rules_md += "\n## Top Escalation Triggers (what makes user demand more depth)\n\n"
    for e in escalations[:10]:
        rules_md += f"- [{e['timestamp'][:10]}] Markers: {', '.join(e['markers'][:3])} — \"{e['prompt'][:100]}...\"\n"

    with open(RULES_FILE, "w") as f:
        f.write(rules_md)

    print(f"\nPatterns saved: {PATTERNS_FILE}")
    print(f"Rules saved: {RULES_FILE}")
    print(f"\nMeta-rules extracted: {len(rules)}")
    for r in rules:
        print(f"  - {r[:100]}...")

    return patterns


def show_similar(query):
    """Find similar past prompts."""
    prompts = load_prompts()
    similar = find_similar_prompts(query, prompts)
    if similar:
        print(f"\n=== Similar Past Prompts for: \"{query[:50]}...\" ===\n")
        for i, s in enumerate(similar, 1):
            print(f"{i}. [{s['timestamp'][:10]}] (overlap: {s['overlap']} words)")
            print(f"   Shared: {', '.join(s['shared_words'][:5])}")
            print(f"   Prompt: {s['prompt'][:150]}...")
            print()
    else:
        print("No similar prompts found.")


def show_corrections():
    """Show correction patterns."""
    prompts = load_prompts()
    corrections = find_corrections(prompts)
    print(f"\n=== User Correction Patterns ({len(corrections)} found) ===\n")
    for c in corrections[:15]:
        print(f"[{c['timestamp'][:10]}] Markers: {', '.join(c['markers'][:4])}")
        print(f"  \"{c['prompt'][:200]}...\"")
        print()


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--mine" in args:
        mine_all()
    elif "--similar" in args:
        idx = args.index("--similar")
        query = " ".join(args[idx + 1:])
        show_similar(query)
    elif "--corrections" in args:
        show_corrections()
    elif "--escalations" in args:
        prompts = load_prompts()
        escalations = find_escalations(prompts)
        print(f"\n=== Escalation Patterns ({len(escalations)} found) ===\n")
        for e in escalations[:15]:
            print(f"[{e['timestamp'][:10]}] {', '.join(e['markers'][:3])}")
            print(f"  \"{e['prompt'][:200]}...\"")
            print()
    elif "--rules" in args:
        patterns = mine_all()
    elif "--effective" in args:
        prompts = load_prompts()
        sats = find_satisfactions(prompts)
        print(f"\n=== Satisfaction Triggers ({len(sats)} found) ===\n")
        for s in sats[:10]:
            print(f"[{s['timestamp'][:10]}] {', '.join(s['markers'][:3])}")
            print(f"  \"{s['prompt'][:200]}...\"")
            print()
    else:
        print("Prompt Pattern Miner — extracts meta-rules from your prompt history")
        print()
        print("  --mine              Full pattern extraction (1,510+ prompts)")
        print("  --similar QUERY     Find similar past prompts")
        print("  --corrections       Show user pushback patterns")
        print("  --escalations       Show depth-demand patterns")
        print("  --effective         Show satisfaction triggers")
        print("  --rules             Generate meta-rules")
