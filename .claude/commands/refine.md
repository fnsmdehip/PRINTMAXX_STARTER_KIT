---
name: refine
description: Run hybrid cognitive refinement cycles on any file or directory. Uses user voice model, meta-rules, bias-null protocol, cognitive engine, and prompt pattern miner to iteratively improve content through simulated user-perspective critique. Usage: /refine <target_path> [num_cycles]
model: opus
---

# Hybrid Cognitive Refinement Loop

**Arguments:** $ARGUMENTS

Parse arguments: first arg = target path (file or directory), second arg = number of cycles (default 3).

If no arguments provided, ask the user what to refine and how many cycles.

## Phase 0: Backup

1. Determine the target (file or directory) from the first argument.
2. Create a backup:
   - If target is a single file: copy to `{filename}.backup.{timestamp}`
   - If target is a directory: copy entire directory to `{dirname}_backup_{timestamp}/`
   - Place backups adjacent to the original (same parent directory).
3. Confirm backup created. Store the backup path for later reference.

## Phase 1: Load Cognitive Architecture

Read these files to build the refinement context (do NOT skip any):

1. **User Voice Model**: `OPS/USER_VOICE_MODEL.json` — Extract directness level, banned patterns, preferred terms, style summary, correction history
2. **Meta-Rules**: `OPS/prompt_intelligence/comprehensive_meta_rules.md` — Extract the top triggered rules (ANTI-LAZY, DEPTH-FIRST, WRONG-DIRECTION, SATISFACTION-PATTERN, CHAIN-LENGTH)
3. **Bias-Null Protocol**: `.claude/rules/bias-null.md` — Load all 5 pre-output filters
4. **Copy Style Rules**: `.claude/rules/copy-style.md` — Load if refining any customer-facing content (HTML, marketing copy, product descriptions)

## Phase 2: Intelligence Lookup

Run these commands to find similar past work and patterns:

```bash
python3 AUTOMATIONS/cognitive_engine.py --lookup "<brief description of what's being refined>"
python3 AUTOMATIONS/prompt_pattern_miner.py --similar "<brief description of what's being refined>"
```

Extract any relevant patterns, past corrections, or similar task outcomes. If no results found, proceed — the voice model and meta-rules are sufficient.

## Phase 3: Refinement Cycles

For each cycle (1 through N):

### Cycle Structure — DRIVEN BY LIVE META-RULES

The cycle lenses come from `OPS/prompt_intelligence/comprehensive_meta_rules.md` (rebuilt weekly by cognitive_engine.py from 5,000+ conversation prompts). Read that file in Phase 1 and use its rules as cycle lenses. Current rules as of last rebuild:

**Cycle 1 — WRONG-DIRECTION check (468 triggers):**
- Re-read the target. What is the ACTUAL intent? Generate 2-3 interpretations.
- Pick the interpretation most consistent with the user's voice model patterns.
- Check: Am I refining what the user actually wanted, or what I assumed they wanted?
- Apply correction chains from cognitive engine lookup (Phase 2) for similar past tasks.

**Cycle 2 — DEPTH-FIRST + ANTI-LAZY (253+51 triggers):**
- Apply DEPTH-FIRST: What would the user ask in follow-up? Include that answer now.
- Apply ANTI-LAZY: Is this below expectations? Would the user call this lazy? Go deeper.
- Check: Specific numbers, tools, proof points? Vague claims = fail.
- Check: Bias-null filter 1-3 (legacy smuggling, preemptive appeasement, lived-gap check).

**Cycle 3 — SATISFACTION-PATTERN + Competitive (3964 triggers):**
- Apply SATISFACTION-PATTERN: The user is satisfied when the system executes autonomously, output exceeds the explicit ask, non-obvious angles are found, and work compounds.
- Check: If 10,000 people built this, what makes this version non-obvious?
- Apply bias-null filters 4-5 (popular-default trap, training-bias correction).
- Final pass: All 5 bias-null filters on every major claim or recommendation.

**Cycles 4+ (if requested):**
- Even cycles: CHAIN-LENGTH lens — average correction chain is 6.1 prompts. Can you get to the right output in ONE pass? Simulate what the user would correct.
- Odd cycles: HARD-TOPICS lens — topics that consistently need corrections (directory, autonomy, task, every, each). Extra care on these.

### IMPORTANT: If meta-rules have changed since this was written, USE THE LIVE RULES from the file, not these examples. The rules above are a snapshot — the live file is the source of truth.

### Per-Cycle Actions

For each cycle:
1. State which cycle number and which lens is being applied
2. Read the current state of the target content
3. Identify 3-7 specific issues through the cycle's lens
4. Make targeted edits to fix each issue (use Edit tool, not full rewrites)
5. After edits, do a quick AI slop scan: search for banned words from copy-style.md
6. State what changed and why

## Phase 4: Review

After all cycles complete:

1. Summarize all changes made across all cycles (grouped by cycle)
2. Tell the user: "Refinement complete. Review the changes. Say **approve** to delete the backup, or **revert** to restore the original."

## Phase 5: Resolution

**If user says "approve" (or equivalent):**
- Delete the backup file/directory
- Confirm: "Backup deleted. Refined version is now canonical."

**If user says "revert" (or equivalent):**
- Delete the refined version
- Move the backup back to the original location (rename, removing backup suffix)
- Confirm: "Reverted to original. Refined version discarded."

**If user says "keep both":**
- Leave both in place
- Confirm paths of both versions

## Phase 6: Self-Update (automatic, no user action needed)

After every refinement session, check if a new pattern emerged that should update the refinement process itself:

1. Did any cycle reveal a NEW critique pattern not already in comprehensive_meta_rules.md?
   - If yes: Append it to `AUTOMATIONS/logs/cognitive_refine.jsonl` with `{"type": "new_pattern", "pattern": "...", "source": "refine_session", "timestamp": "..."}`
2. Did the user reject or revert any changes?
   - If yes: Log what was rejected and why to cognitive_refine.jsonl — this trains future refinement to avoid that pattern
3. Did the user approve changes that were particularly good?
   - If yes: Log the technique used so it gets weighted higher in future cycles

The cognitive_engine.py weekly rebuild will pick up these entries and incorporate them into the meta-rules, which then flow back into this command's Phase 3 cycle lenses. This creates a feedback loop: refine sessions produce learnings that improve future refine sessions.

## Rules

- NEVER do full file rewrites. Use targeted Edit tool calls for surgical changes.
- Each cycle should produce 3-7 edits, not a complete rewrite.
- If copy-style.md applies (HTML/marketing), run the pre-publish checklist after the final cycle.
- Always show what changed and why after each cycle.
- The backup MUST be created before ANY edits happen. Non-negotiable.
- If the cognitive engine or pattern miner scripts fail, proceed without them. The voice model + meta-rules are the core of the process.
- Phase 3 lenses come from LIVE meta-rules file, not hardcoded examples. Always read the file.
