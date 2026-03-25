---
name: health
description: Full system health check — loops, crons, ventures, pipelines, RBI status. Usage: /health
---

# Full System Health Check

Run all health checks in parallel and present a unified report.

## Checks to Run

### 1. System Health Monitor
```bash
python3 AUTOMATIONS/system_health_monitor.py --check --skip-sites
```
16-point automated system check covering scripts, state files, agents, cron.

### 2. Loop Health
```bash
python3 AUTOMATIONS/loop_closer.py --status
```
All 4 loops must show OK. Flag any DEAD or STALE.

### 3. Cron Health
```bash
python3 AUTOMATIONS/cron_watchdog.py
```
Verifies all required cron jobs are installed. Reports missing crons.

### 4. Venture Status
```bash
python3 AUTOMATIONS/venture_autonomy.py --status
```
Shows all 8 venture types and their current state.

### 5. RBI Pipeline Status
```bash
python3 AUTOMATIONS/rbi_loop.py --status
```
Shows research/backtest/implement pipeline state.

### 6. Revenue Check
```bash
cat FINANCIALS/revenue_pipeline.json 2>/dev/null || echo "No revenue data"
```
Current revenue status and pipeline.

## Report Format

Present a unified dashboard:

```
SYSTEM HEALTH — 2026-03-24
===========================

OVERALL: [OK | DEGRADED | CRITICAL]

Loops:      4/4 OK | [details if not]
Crons:      9/9 present | [missing if any]
Ventures:   N active / N paused / N blocked
RBI:        N researched, N backtested, N implemented
Revenue:    $X current | $Y pipeline
Health:     N/16 checks passed

ISSUES REQUIRING ATTENTION:
- [any DEAD loops]
- [any missing crons]
- [any blocked ventures needing human action]
- [any RBI methods ready for implementation]
```

## Severity Classification

- **CRITICAL**: Dead loops, missing crons, system health <12/16
- **DEGRADED**: Stale loops, paused ventures, RBI backlog >10
- **OK**: All loops OK, all crons present, ventures running, RBI flowing

## Actions

If CRITICAL issues found:
1. Fix dead loops first (run `/loops fix`)
2. Restore missing crons (`python3 AUTOMATIONS/cron_watchdog.py` auto-restores)
3. Surface human blockers with time estimates

If DEGRADED:
1. Note the issues but don't block on them
2. Recommend specific `/loops`, `/rbi`, or venture commands to address

## Rules

- Run this check at session start if the session involves infrastructure or pipeline work.
- CLAUDE.md Rule 20: Dead loops must be fixed before other work.
- CLAUDE.md Rule 21: RBI over building. Check if validated methods are waiting.
- Never claim the system is healthy without running these checks.
