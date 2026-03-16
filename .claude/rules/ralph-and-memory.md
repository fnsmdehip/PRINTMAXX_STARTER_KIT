# Ralph Loops & Memory

## Ralph Pattern
`while :; do cat PROMPT.md | claude --dangerously-skip-permissions --print ; done`

Memory = filesystem + git, NOT context window. Each iteration: fresh context → read state → ONE task → write state → exit.

Reference: `OPS/RALPH_CANONICAL_REFERENCE.md` | Overnight: `OPS/OVERNIGHT_PROCESS_GUIDE.md`
Autonomous loop: `bash AUTOMATIONS/schedule_claude.sh morning|midday|evening`
Orchestrator: `python3 AUTOMATIONS/autonomous_orchestrator.py --status`

## Subconscious Memory
- Session Start: `AUTOMATIONS/subconscious/session_start_injector.sh` (injects memories)
- Session End: `AUTOMATIONS/subconscious/session_end_processor.sh` (extracts via `claude -p`)
- Store: `AUTOMATIONS/subconscious/memories/memories.jsonl`
- Categories: PREFERENCE, DECISION, STRATEGIC, BLOCKER, LEARNED, CREATED, COMPLETED
- PreCompact: `AUTOMATIONS/hooks/save_context_snapshot.py` (captures state before compaction)

## Alpha & Ledger
All findings → `LEDGER/ALPHA_STAGING.csv` as PENDING_REVIEW.
Process: Scrape → ALPHA_STAGING → `alpha_auto_processor.py --process-new` → routes to ventures
MEGA_SHEET: `LEDGER/MEGA_SHEET/` — 10 CSVs, 2,512 rows
