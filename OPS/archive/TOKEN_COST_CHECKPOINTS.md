# TOKEN / COST CHECKPOINTS (PrintMaxx)

Goal: prevent expensive model burn (Opus) and long-running loops.

---

## Universal rule
Before ANY of the following, the agent must STOP and request approval:

- running Opus for a large rewrite
- generating > 10 pages/posts in one run
- refactoring > 5 files
- touching compliance copy
- touching payments/credentials
- running any automation that changes external systems (email platforms, ads, socials)

Approval format (agent must output this):
1) **Task name**
2) **Model planned** (Haiku/Sonnet/Opus)
3) **Estimated size** (files touched / tokens / time)
4) **Exact deliverable(s)**
5) **Abort conditions** (what triggers stop)
6) **Rollback plan** (how to undo)

Operator replies: “APPROVED” or “CHANGE: <instruction>”.

---

## Two-stage execution (required for Opus)
### Stage A — Preview (cheap)
Use Sonnet/Haiku to produce:
- outline / diff plan
- sample 1-page rewrite
- list of files to touch

STOP. Ask approval.

### Stage B — Full run (expensive)
Only after approval, run Opus for:
- final money pages
- compliance copy
- top Truth Pages
- policy blocks

---

## “Fresh Opus manager chat” pattern (min context, full scope)
Opus manager should NOT ingest the entire repo repeatedly.
Instead:

### Inputs to Opus manager (always small)
- `MASTER_DOC/PRINTMAXX_MASTER_OPERATING_SYSTEM.md` (or latest vXX)
- `OPS/logs/RUNLOG_*.md` from the last run (only)
- `OPS/logs/BLOCKED_*.md` (if exists)
- a short “Decision Request” file (below)

### Outputs from Opus manager
- a 1-page decision memo:
  - what to do next
  - which agent/model to run it
  - stop rules
  - success criteria

This keeps Opus cost down while retaining bird’s-eye control.

---

## Decision Request template (agents must create)
Write: `OPS/DECISION_REQUEST.md`

Template:
- Current state (3 bullets)
- What’s blocked (if any)
- Candidate options (A/B)
- What you recommend and why
- What you need approved

---

## Hard caps (defaults)
- Sonnet bulk generation: max **50** pages per run
- Haiku formatting: max **200** rows/edits per run
- Opus: max **1** major deliverable per run

---

## Loop kill switch
If the agent repeats the same failure twice:
- STOP
- write `OPS/logs/BLOCKED_<AGENT>.md`
- do NOT continue
