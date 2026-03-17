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

### Cycle Structure

Each cycle applies a different critique lens in sequence:

**Cycle 1 — Customer/User Perspective:**
- Read the target content as the end user or customer would.
- Apply: Would this confuse, bore, or lose a customer? Is there anything that triggers skepticism?
- Check: Are there AI slop words? Em dashes? Hedging? Banned vocabulary from copy-style.md?
- Check: Does it pass the voice model's directness test (10/10)?

**Cycle 2 — Depth-First (Anti-Lazy):**
- Apply DEPTH-FIRST meta-rule: What would the user ask in follow-up? Include that answer now.
- Apply ANTI-LAZY meta-rule: Is this below the user's expectations? Is it "basic bitch work"?
- Check: Are there specific numbers, specific tools, specific proof points? Vague claims = fail.
- Check: Bias-null filter — am I defaulting to popular/safe instead of genuinely best?

**Cycle 3 — Competitive Differentiation:**
- Apply: If 10,000 other people built this, what makes this version non-obvious?
- Check: Is there a unique angle, positioning, or specificity that a competitor wouldn't have?
- Apply SATISFACTION-PATTERN: What makes the user say "this is exactly what I wanted"?
- Final pass: Run all 5 bias-null filters on every major claim or recommendation.

**Cycles 4+ (if requested):** Alternate between:
- Even cycles: Customer perspective + depth-first (Cycle 1+2 combined)
- Odd cycles: Competitive differentiation + voice model fidelity check

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

## Rules

- NEVER do full file rewrites. Use targeted Edit tool calls for surgical changes.
- Each cycle should produce 3-7 edits, not a complete rewrite.
- If copy-style.md applies (HTML/marketing), run the pre-publish checklist after the final cycle.
- Always show what changed and why after each cycle.
- The backup MUST be created before ANY edits happen. Non-negotiable.
- If the cognitive engine or pattern miner scripts fail, proceed without them. The voice model + meta-rules are the core of the process.
