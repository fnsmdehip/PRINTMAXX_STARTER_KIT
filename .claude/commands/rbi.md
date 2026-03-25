---
name: rbi
description: Research, Backtest, Implement loop. Finds validated revenue methods and implements them. Usage: /rbi [research|backtest|implement|full|status]
---

# RBI Loop — Research, Backtest, Implement

**Arguments:** $ARGUMENTS

Parse the first argument to determine which phase to run. If no argument provided, default to `status`.

## Phase Routing

| Argument | Action |
|----------|--------|
| `research` | `python3 AUTOMATIONS/rbi_loop.py --research` |
| `backtest` | `python3 AUTOMATIONS/rbi_loop.py --backtest` |
| `implement` | `python3 AUTOMATIONS/rbi_loop.py --implement` |
| `full` | `python3 AUTOMATIONS/rbi_loop.py --full` |
| `status` | `python3 AUTOMATIONS/rbi_loop.py --status` |
| `top N` | `python3 AUTOMATIONS/rbi_loop.py --research --top N` |
| (none) | `python3 AUTOMATIONS/rbi_loop.py --status` |

## Process

1. Run the appropriate command from the table above.
2. Parse the output and present a clean summary:
   - **Research**: How many methods found, top candidates, sources scanned
   - **Backtest**: How many passed/failed/conditional, reasons for failures
   - **Implement**: What was implemented, what needs human action, what was wired to cron
   - **Full**: All three phases in sequence with a combined report
   - **Status**: Current pipeline state — researched count, backtested count, implemented count, pending actions

3. If any methods scored PASS in backtest, highlight them as ready for implementation.
4. If any methods are CONDITIONAL, surface what conditions need to be met.
5. If implementation created new scripts or cron entries, verify they work (Rule 19: TEST ON CREATE).

## Context Files (read if needed for deeper analysis)

- `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` — current priority rankings
- `OPS/ACTIONABLE_QUEUE.md` — items waiting for action
- `AUTOMATIONS/agent/rbi_state.json` — RBI pipeline state
- `LEDGER/CAPITAL_GENESIS_RANKINGS.csv` — full method scores

## Rules

- NEVER implement without backtesting first. The whole point is validation before building.
- PASS methods get implemented immediately. CONDITIONAL methods go to actionable queue.
- FAIL methods are logged and skipped. Don't waste time on them.
- After implementation, verify the output actually works (End-to-End Verification rule).
- This replaces "build whatever sounds good" with "validate then build" (CLAUDE.md Rule 21).
