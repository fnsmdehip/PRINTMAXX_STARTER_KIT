# MANAGER RUNBOOK (Opus/Sonnet) — PrintMaxx Dispatch

Purpose: run the operation with minimal context and zero loops.

---

## Inputs (keep tiny)
Read only:
1) `MASTER_DOC/PRINTMAXX_MASTER_OPERATING_SYSTEM.md`
2) latest `OPS/logs/RUNLOG_*.md`
3) any `OPS/logs/BLOCKED_*.md`
4) `OPS/DECISION_REQUEST.md` (if present)

---

## Output (single file)
Write: `OPS/NEXT_ACTIONS.md`

Format:
- Mission for next run (1 sentence)
- Assignments (Agent A/B/C/…)
  - model
  - folder ownership
  - exact deliverable
  - stop rules
- Approval checkpoints required (if any)
- Success criteria

---

## Dispatch rules
- Never assign two agents to the same folder.
- Never allow a worker to pick its own next task.
- Prefer deterministic scripts over UI automation.

---

## When to use Opus vs Sonnet as manager
- Use **Opus manager** when:
  - deciding offer/copy/compliance
  - settling strategy forks
  - approving automation thresholds
- Use **Sonnet manager** when:
  - coordinating code/content tasks
  - selecting next implementation steps
