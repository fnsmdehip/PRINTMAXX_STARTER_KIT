---
name: edge
description: Apply competitive edge thinking to any task. Researches what power users do, finds novel synergies nobody has connected, identifies maximum extractable value. Usage: /edge <target> [num_cycles]
model: opus
---

# Competitive Edge Loop

**Arguments:** $ARGUMENTS

Parse arguments: first arg = target (file, directory, or concept), second arg = number of cycles (default 3).

If no arguments provided, ask the user what to apply edge thinking to and how many cycles.

## Phase 0: Context Load

Read these files for competitive context (skip any that don't exist):

1. `OPS/SOVRUN_COMPETITIVE_ANALYSIS.md` — what competitors do
2. `OPS/USER_VOICE_MODEL.json` — user preferences
3. `.claude/rules/bias-null.md` — pre-output filters

## Phase 1: Edge Cycles

**Cycle 1 — Baseline Audit (what everyone does):**
- Web search for current state-of-the-art for this exact task/domain
- Identify 5-10 standard techniques that are table stakes
- Score our current implementation against each
- List what we're missing from the baseline

**Cycle 2 — Synergy Mining (what nobody has combined yet):**
- Take techniques from Cycle 1 and look for UNCOMBINED synergies
- "A is great. B is great. Nobody has combined A+B. What would that produce?"
- Cross-pollinate from other domains — what do quants/traders/security researchers/compiler engineers do for the same underlying problem?
- Identify 3-5 novel combinations or cross-domain imports that nobody in this space is doing

**Cycle 3 — MEV Extraction (maximum extractable value):**
- From Cycle 2, which combination has highest ROI with lowest effort?
- What's the "alpha" — the insight that gives disproportionate returns?
- Think adversarially: if a competitor saw our system, what would they copy first? What CAN'T they copy? Double down on the uncopyable
- Make specific, actionable edits to implement the highest-value insight. Not theory — exact changes.

**Cycles 4+ (if requested):** Alternate:
- Even cycles: fresh synergy mining (new cross-domain imports)
- Odd cycles: MEV extraction (prioritize and implement)

## Per-Cycle Actions

1. State which cycle number and lens
2. Do the research (web search for Cycle 1, creative synthesis for 2-3)
3. Identify 3-7 specific insights
4. For Cycle 3+: make targeted edits to implement highest-value insight
5. State what changed and why

## Rules

- NOT the same as /refine. /refine improves quality. /edge finds alpha.
- Always web search in Cycle 1. Don't guess at "current best practices."
- Cross-domain imports are the highest-value output.
- Output should make the user say "I didn't know that was possible" at least once.
- Think like a quant: everyone does the obvious. Find the non-obvious edge. But don't over-engineer — if baseline is sufficient, ship it. The edge must be REAL, not complexity for its own sake.
