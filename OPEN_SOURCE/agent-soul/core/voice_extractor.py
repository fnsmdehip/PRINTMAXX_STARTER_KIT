#!/usr/bin/env python3
"""
Voice Extractor -- Analyzes user prompt history and distills communication style
for autonomous agent use. Trains on actual human prompts to produce a voice/style
model that agents inject before generating outputs.

The core insight: your AI should sound like YOU, not like a generic assistant.
This module reads your prompt history, identifies your patterns (vocabulary,
tone, corrections, frustrations), and outputs a compact voice model that any
agent can consume.

Usage:
    python3 -m sovrun.core.voice_extractor --extract       # Analyze prompts, build model
    python3 -m sovrun.core.voice_extractor --inject        # Output compact injection string
    python3 -m sovrun.core.voice_extractor --status        # Show model stats
    python3 -m sovrun.core.voice_extractor --diff          # Compare current vs previous model

No external API calls. Pure Python text analysis.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths (configurable via environment)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(os.environ.get("SOVRUN_ROOT", Path.cwd()))

PROMPTS_FILE = Path(os.environ.get(
    "SOVRUN_PROMPTS", PROJECT_ROOT / "data" / "prompts.jsonl"))
CONVERSATION_FILE = Path(os.environ.get(
    "SOVRUN_CONVERSATIONS", PROJECT_ROOT / "data" / "conversations.jsonl"))
MODEL_PATH = Path(os.environ.get(
    "SOVRUN_VOICE_MODEL", PROJECT_ROOT / "output" / "voice_model.json"))
MODEL_PREV_PATH = MODEL_PATH.parent / "voice_model.prev.json"
SOUL_FILE = Path(os.environ.get(
    "SOVRUN_SOUL_MD", PROJECT_ROOT / "templates" / "SOUL.md"))
SYSTEM_INSTRUCTIONS = Path(os.environ.get(
    "SOVRUN_INSTRUCTIONS", PROJECT_ROOT / "templates" / "CLAUDE.md"))

LOGS_DIR = PROJECT_ROOT / "logs"


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------

def safe_path(target: str | Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    root = PROJECT_ROOT.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError(f"BLOCKED: {resolved} is outside project root {root}")
    return resolved


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [VOICE] [{level}] {msg}")


def log_to_file(msg: str) -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    path = LOGS_DIR / "voice_extractor.log"
    with open(path, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")


# ---------------------------------------------------------------------------
# Agent prompt detection -- filters OUT autonomous agent prompts
# ---------------------------------------------------------------------------

AGENT_PREAMBLES = [
    "You are the ",
    "You are @",
    "<task-notification>",
    "You are a ",
    "CYCLE:",
    "Your job:",
    "Working directory:",
    "Your job runs every",
]

AGENT_PATTERNS = [
    r"^You are the \w+ (agent|autonomy agent)",
    r"^<task-notification>",
    r"CYCLE:\n1\.",
    r"^You are a \w+ agent",
    r"Your job: .{50,}",
]

AGENT_REGEX = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in AGENT_PATTERNS]


def is_agent_prompt(text: str) -> bool:
    """Return True if this prompt looks like an autonomous agent prompt, not human input."""
    if not text:
        return True

    if len(text) > 800:
        for prefix in AGENT_PREAMBLES:
            if text.strip().startswith(prefix):
                return True
        for rx in AGENT_REGEX:
            if rx.search(text):
                return True
        if text.strip().startswith(("{", "<", "##", "---")):
            return True

    stripped = text.strip()
    for prefix in AGENT_PREAMBLES:
        if stripped.startswith(prefix) and len(stripped) > 200:
            return True

    if stripped.startswith("<task-notification>"):
        return True

    return False


def is_human_prompt(text: str) -> bool:
    """Return True if this looks like an actual human-typed prompt."""
    if not text or not text.strip():
        return False
    if is_agent_prompt(text):
        return False
    return True


# ---------------------------------------------------------------------------
# Configurable signal lists
# ---------------------------------------------------------------------------

# Override these with your own phrases via set_known_phrases()
KNOWN_USER_PHRASES: list[str] = []

# AI slop words to flag and ban
BANNED_AI_WORDS = [
    "I hope this helps", "Let me know if", "comprehensive", "leverage",
    "utilize", "delve", "innovative", "seamless", "game-changer",
    "unlock", "elevate", "cutting-edge", "empower", "foster",
    "frictionless", "journey", "robust", "streamlined", "furthermore",
    "moreover", "additionally", "testament", "landscape", "paradigm",
    "Great question", "That's a great", "I'd be happy to",
    "absolutely", "certainly",
]

# Correction patterns -- phrases indicating user corrected the system
CORRECTION_PATTERNS = [
    r"no[\s,]+not that",
    r"i said .+ not .+",
    r"i mean .+ not .+",
    r"that'?s not what i",
    r"wrong[\.\!\,]",
    r"don'?t (do|use|say|write|make)",
    r"stop (doing|using|saying|writing|making)",
    r"i told you",
    r"not like that",
    r"try again",
    r"redo ",
    r"rewrite",
    r"fix (this|that|it)",
]

CORRECTION_REGEX = [re.compile(p, re.IGNORECASE) for p in CORRECTION_PATTERNS]

# Frustration indicators
FRUSTRATION_PATTERNS = [
    (r"\bbruh\b", "mild"),
    (r"\bwtf\b", "strong"),
    (r"\bwhat the fuck\b", "strong"),
    (r"\bdude\b", "mild"),
    (r"\bffs\b", "strong"),
    (r"\bfor fuck'?s sake\b", "strong"),
    (r"\bjesus\b", "mild"),
    (r"\bcome on\b", "mild"),
    (r"\bi (already|just) (said|told|asked)", "moderate"),
    (r"again\?", "moderate"),
    (r"\bstop\b.{0,30}\basking\b", "moderate"),
    (r"\bugh\b", "mild"),
    (r"\bomg\b", "mild"),
    (r"\bsmh\b", "moderate"),
]

FRUSTRATION_REGEX = [(re.compile(p, re.IGNORECASE), level) for p, level in FRUSTRATION_PATTERNS]


def set_known_phrases(phrases: list[str]) -> None:
    """Set custom known user phrases for vocabulary analysis."""
    global KNOWN_USER_PHRASES
    KNOWN_USER_PHRASES = phrases


def set_banned_words(words: list[str]) -> None:
    """Set custom banned AI vocabulary."""
    global BANNED_AI_WORDS
    BANNED_AI_WORDS = words


# ---------------------------------------------------------------------------
# Extraction engine
# ---------------------------------------------------------------------------

def load_prompts_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load entries from a JSONL file."""
    if not path.exists():
        return []
    entries = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def extract_human_prompts(entries: list[dict[str, Any]]) -> list[str]:
    """Filter entries to only human-typed prompts."""
    human = []
    for entry in entries:
        role = entry.get("role", "")
        if role and role != "user":
            continue

        text = entry.get("prompt", "") or entry.get("content", "") or entry.get("text", "")
        if not text or not text.strip():
            continue

        stripped = text.strip()

        # Skip system/context messages
        if stripped.startswith("<task-notification>"):
            continue
        if stripped.startswith("This session is being continued"):
            continue
        if stripped.startswith("{") and '"type":"error"' in stripped:
            continue

        # Skip very long context dumps
        if len(stripped) > 2000 and entry.get("content_length", 0) > 5000:
            continue

        if is_human_prompt(stripped):
            human.append(stripped)
    return human


def analyze_vocabulary(prompts: list[str]) -> dict[str, Any]:
    """Analyze word frequency and preferred vocabulary."""
    word_counter: Counter = Counter()
    bigram_counter: Counter = Counter()
    phrase_hits: Counter = Counter()

    for prompt in prompts:
        words = re.findall(r"[a-zA-Z']+", prompt.lower())
        word_counter.update(words)

        for i in range(len(words) - 1):
            bigram_counter[(words[i], words[i + 1])] += 1

        lower = prompt.lower()
        for phrase in KNOWN_USER_PHRASES:
            if phrase in lower:
                phrase_hits[phrase] += 1

    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "out", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "both", "each", "few", "more", "most",
        "other", "some", "such", "no", "nor", "not", "only", "own", "same",
        "so", "than", "too", "very", "just", "but", "and", "or", "if", "it",
        "its", "i", "me", "my", "we", "our", "you", "your", "he", "him",
        "his", "she", "her", "they", "them", "their", "what", "which", "who",
        "whom", "this", "that", "these", "those", "am", "get", "got", "like",
        "make", "also", "up", "about", "one", "two", "new", "way", "use",
        "used", "using", "need", "want", "thing", "things", "know", "see",
        "don't", "dont", "doesn't", "didn't", "it's",
    }

    preferred = [
        w for w, c in word_counter.most_common(200)
        if w not in stopwords and c >= 2 and len(w) > 2
    ][:30]

    frequent_phrases = [p for p, c in phrase_hits.most_common(20) if c >= 1]

    return {
        "word_counter": word_counter,
        "bigram_counter": bigram_counter,
        "preferred_words": preferred,
        "frequent_phrases": frequent_phrases,
    }


def analyze_tone(prompts: list[str]) -> dict[str, Any]:
    """Analyze tone markers from prompts."""
    total = len(prompts) or 1

    imperative_count = 0
    question_count = 0
    profanity_count = 0
    abbreviation_count = 0
    typo_indicators = 0
    lowercase_count = 0
    short_prompt_count = 0

    profanity_words = {"shit", "fuck", "fucking", "damn", "hell", "ass", "wtf", "ffs", "crap", "bullshit"}
    abbreviations = {"u", "ur", "r", "w", "b", "n", "bc", "idk", "tbh", "imo", "lol", "lmao", "brb", "rn", "af"}

    for prompt in prompts:
        lower = prompt.lower()
        words = lower.split()

        if len(prompt) < 200:
            short_prompt_count += 1

        if prompt and prompt[0].islower():
            lowercase_count += 1

        if words and not prompt.strip().endswith("?"):
            imperative_count += 1
        if prompt.strip().endswith("?"):
            question_count += 1

        for w in words:
            cleaned = re.sub(r"[^a-z]", "", w)
            if cleaned in profanity_words:
                profanity_count += 1

        for w in words:
            cleaned = re.sub(r"[^a-z]", "", w)
            if cleaned in abbreviations:
                abbreviation_count += 1

        if re.search(r"\b(dont|cant|wont|shouldnt|wouldnt|couldnt|isnt|wasnt|im|ive|youre|theyre)\b", lower):
            typo_indicators += 1

    return {
        "directness": min(10, round(10 * imperative_count / total)),
        "formality": max(1, 10 - round(10 * lowercase_count / total)),
        "profanity_tolerance": min(10, round(10 * min(profanity_count, total) / total * 3)),
        "abbreviation_heavy": abbreviation_count > total * 0.1,
        "typo_tolerant": typo_indicators > total * 0.15,
        "avg_prompt_length": round(sum(len(p) for p in prompts) / total),
        "short_prompt_ratio": round(short_prompt_count / total, 2),
        "question_ratio": round(question_count / total, 2),
    }


def analyze_corrections(prompts: list[str]) -> list[dict[str, Any]]:
    """Find correction patterns where user corrected the system."""
    corrections = []
    for prompt in prompts:
        for rx in CORRECTION_REGEX:
            match = rx.search(prompt)
            if match:
                corrections.append({
                    "prompt_excerpt": prompt[:200],
                    "pattern": match.group(0),
                })
    seen = set()
    unique = []
    for c in corrections:
        key = c["pattern"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique[:20]


def analyze_frustration(prompts: list[str]) -> list[dict[str, str]]:
    """Detect escalation triggers and frustration markers."""
    triggers = []
    for prompt in prompts:
        for rx, level in FRUSTRATION_REGEX:
            match = rx.search(prompt)
            if match:
                triggers.append({
                    "phrase": match.group(0),
                    "level": level,
                    "context": prompt[:150],
                })
    seen = set()
    unique = []
    for t in triggers:
        key = t["phrase"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(t)
    return unique[:15]


def find_recurring_instructions(prompts: list[str], threshold: int = 2) -> list[str]:
    """Find instructions that appear multiple times across prompts."""
    instruction_counter: Counter = Counter()

    for prompt in prompts:
        lower = prompt.lower().strip()
        sentences = re.split(r"[\.!\n]", lower)
        for sent in sentences:
            sent = sent.strip()
            if 10 < len(sent) < 120:
                normalized = re.sub(r"\s+", " ", sent)
                instruction_counter[normalized] += 1

    recurring = [
        instr for instr, count in instruction_counter.most_common(30)
        if count >= threshold
    ]
    return recurring[:15]


def extract_banned_patterns_from_context() -> list[str]:
    """Pull banned patterns from system instruction files."""
    banned = list(BANNED_AI_WORDS)

    for path in [SYSTEM_INSTRUCTIONS, SOUL_FILE]:
        if path.exists():
            try:
                text = path.read_text(encoding="utf-8")
                for match in re.finditer(r'[Nn]ever (?:use|say|write|generate|output) ["\']?([^"\'.\n]{3,60})["\']?', text):
                    candidate = match.group(1).strip()
                    if candidate and candidate not in banned:
                        banned.append(candidate)
            except Exception:
                pass

    return banned


def extract_user_directives() -> list[str]:
    """Extract user directive quotes from system instruction files."""
    directives = []
    if SYSTEM_INSTRUCTIONS.exists():
        try:
            text = SYSTEM_INSTRUCTIONS.read_text(encoding="utf-8")
            for match in re.finditer(r'User directive:\s*"([^"]+)"', text):
                directives.append(match.group(1))
        except Exception:
            pass
    return directives


def build_style_summary(tone: dict, preferred: list, _banned: list, _directives: list) -> str:
    """Generate a compact human-readable style summary."""
    parts = []

    if tone.get("directness", 5) >= 7:
        parts.append("Direct, command-oriented")
    elif tone.get("directness", 5) >= 4:
        parts.append("Moderately direct")
    else:
        parts.append("Conversational")

    if tone.get("formality", 5) <= 3:
        parts.append("lowercase")
    elif tone.get("formality", 5) <= 5:
        parts.append("casual")

    if tone.get("abbreviation_heavy"):
        parts.append("abbreviation-heavy")

    prof = tone.get("profanity_tolerance", 0)
    if prof >= 7:
        parts.append("profanity-comfortable")
    elif prof >= 4:
        parts.append("occasional profanity")

    if tone.get("typo_tolerant"):
        parts.append("typos are speed not mistakes")

    parts.append("action-oriented")

    summary = ", ".join(parts) + ". "

    behavioral = []
    behavioral.append("Prefers execution over deliberation.")
    if preferred:
        sample = ", ".join([f"'{w}'" for w in preferred[:5]])
        behavioral.append(f"Uses {sample}.")
    behavioral.append("No AI slop vocabulary.")

    summary += " ".join(behavioral)
    return summary


# ---------------------------------------------------------------------------
# Main extraction pipeline
# ---------------------------------------------------------------------------

def run_extract() -> dict[str, Any]:
    """Run full extraction pipeline and build the voice model."""
    log("Loading prompt sources...")

    all_entries = []

    if PROMPTS_FILE.exists():
        entries = load_prompts_jsonl(PROMPTS_FILE)
        log(f"  Prompts file: {len(entries)} entries")
        all_entries.extend(entries)

    if CONVERSATION_FILE.exists():
        entries = load_prompts_jsonl(CONVERSATION_FILE)
        log(f"  Conversation file: {len(entries)} entries")
        all_entries.extend(entries)

    log(f"Total raw entries: {len(all_entries)}")

    human_prompts = extract_human_prompts(all_entries)
    log(f"Human prompts identified: {len(human_prompts)}")

    if not human_prompts:
        log("No human prompts found. Using user directives as fallback.", "WARN")
        directives = extract_user_directives()
        human_prompts = directives if directives else ["execute with best judgment"]

    directives = extract_user_directives()
    log(f"User directives: {len(directives)}")

    log("Analyzing vocabulary...")
    vocab = analyze_vocabulary(human_prompts)

    log("Analyzing tone...")
    tone = analyze_tone(human_prompts)

    log("Analyzing corrections...")
    corrections = analyze_corrections(human_prompts)

    log("Analyzing frustration triggers...")
    frustration = analyze_frustration(human_prompts)

    log("Finding recurring instructions...")
    recurring = find_recurring_instructions(human_prompts)

    log("Extracting banned patterns...")
    banned = extract_banned_patterns_from_context()

    preferred_terms = list(set(vocab["frequent_phrases"] + vocab["preferred_words"][:15]))

    correction_history = []
    pattern_counts: Counter = Counter()
    for c in corrections:
        pattern_counts[c["pattern"]] += 1
    for pattern, count in pattern_counts.most_common(10):
        correction_history.append({"pattern": pattern, "count": count})

    escalation_triggers = []
    for t in frustration:
        escalation_triggers.append(f"{t['phrase']} = {t['level']} frustration")

    recurring_instructions = list(set(recurring + [d.lower() for d in directives[:10]]))[:15]

    style_summary = build_style_summary(tone, preferred_terms, banned, directives)

    model = {
        "generated": datetime.now().isoformat(),
        "prompt_count_analyzed": len(human_prompts),
        "total_entries_scanned": len(all_entries),
        "sources": {
            "prompts_file": str(PROMPTS_FILE),
            "conversation_file": str(CONVERSATION_FILE) if CONVERSATION_FILE.exists() else None,
        },
        "tone_profile": {
            "directness": tone["directness"],
            "formality": tone["formality"],
            "profanity_tolerance": tone["profanity_tolerance"],
            "abbreviation_heavy": tone["abbreviation_heavy"],
            "typo_tolerant": tone["typo_tolerant"],
            "avg_prompt_length": tone["avg_prompt_length"],
            "short_prompt_ratio": tone["short_prompt_ratio"],
        },
        "preferred_terms": preferred_terms[:25],
        "banned_patterns": banned[:30],
        "correction_history": correction_history,
        "recurring_instructions": recurring_instructions,
        "escalation_triggers": escalation_triggers[:10],
        "style_summary": style_summary,
    }

    # Save previous model for diff
    if MODEL_PATH.exists():
        try:
            prev = MODEL_PATH.read_text(encoding="utf-8")
            MODEL_PREV_PATH.write_text(prev, encoding="utf-8")
            log("Previous model saved for diffing")
        except Exception as e:
            log(f"Could not save previous model: {e}", "WARN")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.write_text(json.dumps(model, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"Voice model written to {MODEL_PATH}")
    log(f"  Prompts analyzed: {model['prompt_count_analyzed']}")
    log(f"  Preferred terms: {len(model['preferred_terms'])}")
    log(f"  Banned patterns: {len(model['banned_patterns'])}")
    log(f"  Style: {model['style_summary'][:120]}...")

    log_to_file(f"Extract: {model['prompt_count_analyzed']} prompts, {len(model['preferred_terms'])} terms")

    return model


# ---------------------------------------------------------------------------
# Injection -- compact style string for agent prompts
# ---------------------------------------------------------------------------

def run_inject(max_chars: int = 500) -> str:
    """Read the voice model and output a compact injection string."""
    if not MODEL_PATH.exists():
        log("No voice model found. Run --extract first.", "ERROR")
        return ""

    try:
        model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        log(f"Failed to read voice model: {e}", "ERROR")
        return ""

    parts = []

    summary = model.get("style_summary", "")
    if summary:
        parts.append(f"VOICE: {summary}")

    banned = model.get("banned_patterns", [])[:8]
    if banned:
        parts.append(f"NEVER SAY: {', '.join(banned[:8])}")

    instructions = model.get("recurring_instructions", [])[:3]
    if instructions:
        parts.append(f"RULES: {'; '.join(instructions[:3])}")

    injection = " | ".join(parts)

    if len(injection) > max_chars:
        injection = injection[:max_chars - 3] + "..."

    return injection


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def run_status() -> None:
    """Print current model stats."""
    if not MODEL_PATH.exists():
        print("No voice model found. Run --extract first.")
        return

    try:
        model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to read model: {e}")
        return

    print("=" * 60)
    print("USER VOICE MODEL STATUS")
    print("=" * 60)
    print(f"Generated:          {model.get('generated', 'unknown')}")
    print(f"Prompts analyzed:   {model.get('prompt_count_analyzed', 0)}")
    print(f"Total scanned:      {model.get('total_entries_scanned', 0)}")
    print()

    tone = model.get("tone_profile", {})
    print("TONE PROFILE:")
    print(f"  Directness:       {tone.get('directness', '?')}/10")
    print(f"  Formality:        {tone.get('formality', '?')}/10")
    print(f"  Profanity:        {tone.get('profanity_tolerance', '?')}/10")
    print(f"  Abbreviations:    {'heavy' if tone.get('abbreviation_heavy') else 'normal'}")
    print(f"  Typo tolerant:    {'yes' if tone.get('typo_tolerant') else 'no'}")
    print(f"  Avg prompt len:   {tone.get('avg_prompt_length', '?')} chars")
    print()

    terms = model.get("preferred_terms", [])
    print(f"PREFERRED TERMS ({len(terms)}):")
    print(f"  {', '.join(terms[:15])}")
    print()

    banned = model.get("banned_patterns", [])
    print(f"BANNED PATTERNS ({len(banned)}):")
    print(f"  {', '.join(banned[:10])}")
    print()

    corrections = model.get("correction_history", [])
    print(f"CORRECTIONS: {len(corrections)} patterns tracked")
    for c in corrections[:5]:
        print(f"  - {c.get('pattern', '?')} (x{c.get('count', 1)})")
    print()

    print("STYLE SUMMARY:")
    print(f"  {model.get('style_summary', 'none')}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Diff
# ---------------------------------------------------------------------------

def run_diff() -> None:
    """Compare current model vs previous version for style drift."""
    if not MODEL_PATH.exists():
        print("No current model found. Run --extract first.")
        return

    if not MODEL_PREV_PATH.exists():
        print("No previous model found. Run --extract twice to enable diffing.")
        return

    try:
        current = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
        previous = json.loads(MODEL_PREV_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to read models: {e}")
        return

    print("=" * 60)
    print("VOICE MODEL DIFF")
    print("=" * 60)
    print(f"Previous: {previous.get('generated', 'unknown')}")
    print(f"Current:  {current.get('generated', 'unknown')}")
    print()

    prev_count = previous.get("prompt_count_analyzed", 0)
    curr_count = current.get("prompt_count_analyzed", 0)
    print(f"Prompts analyzed: {prev_count} -> {curr_count} ({curr_count - prev_count:+d})")

    prev_tone = previous.get("tone_profile", {})
    curr_tone = current.get("tone_profile", {})

    print("\nTONE DRIFT:")
    for key in ["directness", "formality", "profanity_tolerance"]:
        pv = prev_tone.get(key, 0)
        cv = curr_tone.get(key, 0)
        delta = cv - pv
        if delta != 0:
            print(f"  {key}: {pv} -> {cv} ({delta:+d})")
        else:
            print(f"  {key}: {cv} (unchanged)")

    prev_terms = set(previous.get("preferred_terms", []))
    curr_terms = set(current.get("preferred_terms", []))
    new_terms = curr_terms - prev_terms
    dropped_terms = prev_terms - curr_terms

    if new_terms:
        print(f"\nNEW TERMS: {', '.join(list(new_terms)[:10])}")
    if dropped_terms:
        print(f"DROPPED TERMS: {', '.join(list(dropped_terms)[:10])}")

    prev_summary = previous.get("style_summary", "")
    curr_summary = current.get("style_summary", "")
    if prev_summary != curr_summary:
        print(f"\nSTYLE SUMMARY CHANGED:")
        print(f"  WAS: {prev_summary[:200]}")
        print(f"  NOW: {curr_summary[:200]}")
    else:
        print("\nSTYLE SUMMARY: unchanged")

    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Voice Extractor: analyze prompts and distill communication style"
    )
    parser.add_argument("--extract", action="store_true", help="Analyze prompts, build/update model")
    parser.add_argument("--inject", action="store_true", help="Output compact injection string")
    parser.add_argument("--status", action="store_true", help="Show model stats")
    parser.add_argument("--diff", action="store_true", help="Compare current vs previous model")
    parser.add_argument("--max-chars", type=int, default=500, help="Max chars for injection string")
    args = parser.parse_args()

    if not any([args.extract, args.inject, args.status, args.diff]):
        parser.print_help()
        return

    if args.extract:
        run_extract()
    if args.inject:
        injection = run_inject(max_chars=args.max_chars)
        if injection:
            print(injection)
        else:
            print("[No model found. Run --extract first.]")
    if args.status:
        run_status()
    if args.diff:
        run_diff()


if __name__ == "__main__":
    main()
