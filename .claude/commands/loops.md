---
name: loops
description: Check and fix all 4 loop closer loops. Usage: /loops [status|fix|cycle]
---

# Loop Health Manager

**Arguments:** $ARGUMENTS

Parse the first argument to determine the action. Default to `status` if no argument provided.

## Action Routing

| Argument | Action |
|----------|--------|
| `status` | `python3 AUTOMATIONS/loop_closer.py --status` |
| `fix` | Run `--status` first, then fix any DEAD/STALE loops (see Fix Protocol below) |
| `cycle` | `python3 AUTOMATIONS/loop_closer.py --cycle` |
| `decisions` | `python3 AUTOMATIONS/loop_closer.py --decisions` |
| `feedback` | `python3 AUTOMATIONS/loop_closer.py --feedback` |
| `pipeline` | `python3 AUTOMATIONS/loop_closer.py --pipeline` |
| `drift` | `python3 AUTOMATIONS/loop_closer.py --drift` |
| (none) | `python3 AUTOMATIONS/loop_closer.py --status` |

## The 4 Loops

1. **Decision Execution** — Pending CEO decisions get executed
2. **Feedback Tracking** — Agent outputs get scored and fed back
3. **Pipeline Advancement** — Stuck pipeline items get unstuck
4. **Soul Drift** — Agent outputs scored 0-10 against SOUL.md directives

All 4 must show OK. Any DEAD or STALE loop means the system is not self-correcting.

## Fix Protocol (when argument is `fix`)

1. Run `python3 AUTOMATIONS/loop_closer.py --status` and parse output.
2. For each loop showing DEAD or STALE:
   - **Decision Execution DEAD**: Check `AUTOMATIONS/agent/ceo_agent/decisions.jsonl` for pending decisions. Run `--decisions` to execute them.
   - **Feedback Tracking DEAD**: Check `AUTOMATIONS/agent/swarm/swarm_state.json` for agents without recent feedback. Run `--feedback` to update.
   - **Pipeline Advancement DEAD**: Check `AUTOMATIONS/agent/autonomy/autonomy_state.json` for stuck ventures. Run `--pipeline` to advance.
   - **Soul Drift DEAD**: Run `--drift` to rescore agent outputs against SOUL.md.
3. After fixing, run `--status` again to verify all loops show OK.
4. If a loop still shows DEAD after fixing, report the specific error for manual investigation.

## Output

Present a clean table:

```
Loop                  | Status | Last Run         | Issues
Decision Execution    | OK     | 2026-03-24 06:00 | None
Feedback Tracking     | OK     | 2026-03-24 06:00 | None
Pipeline Advancement  | STALE  | 2026-03-22 06:00 | 2 days since last run
Soul Drift            | OK     | 2026-03-24 06:00 | Avg score: 7.2/10
```

## Rules

- CLAUDE.md Rule 20: Dead loops mean the system is not self-correcting. Fix before doing other work.
- Loop closer runs on cron every 2h + Phase 16 of CEO agent.
- Soul drift alert triggers if system average drops below 6/10.
- Anti-patterns: hedging, AI slop words, orphan docs, corporate voice, over-building.
