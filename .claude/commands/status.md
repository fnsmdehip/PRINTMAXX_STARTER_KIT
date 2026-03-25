---
name: status
description: Show PRINTMAXX project status.
model: sonnet
---

# Status Report

Display PRINTMAXX status: apps, content, accounts, metrics.

## Checks

1. Apps: MONEY_METHODS/APP_FACTORY/builds/
2. Content: LEDGER/CONTENT_PIPELINE.csv counts
3. Accounts: LEDGER/ACCOUNTS.csv status
4. Leads: LEDGER/leads.csv count
5. Library: CONTENT/ file counts
6. Infra: Makefile, scripts exist

### 7. Loop Health
Run `python3 AUTOMATIONS/loop_closer.py --status` and include in report.
All 4 loops (Decision Execution, Feedback Tracking, Pipeline Advancement, Soul Drift) must show OK.
Flag any DEAD or STALE loops prominently — these mean the system is not self-correcting.

### 8. RBI Pipeline
Run `python3 AUTOMATIONS/rbi_loop.py --status` and include in report.
Show: methods researched, backtested (pass/fail/conditional), implemented.
Highlight any PASS methods waiting for implementation.

### 9. Cron Health
Run `python3 AUTOMATIONS/cron_watchdog.py` and include in report.
Show total crons present vs required.

## Output

Clean status report with metrics and quick action commands.

Include a section at the end:

```
SYSTEM HEALTH
  Loops: N/4 OK [list any issues]
  Crons: N/N present
  RBI:   N researched | N backtested | N implemented
```

If any loops are DEAD, recommend running `/loops fix`.
If RBI has PASS methods waiting, recommend running `/rbi implement`.
