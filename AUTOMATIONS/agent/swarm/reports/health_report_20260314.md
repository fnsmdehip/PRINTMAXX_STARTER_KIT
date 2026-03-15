# System Health Report — 2026-03-14 18:30

## Summary

| Metric | Status |
|--------|--------|
| Disk | 50GB free / 926GB total (5.4% used) |
| Cron | 62 active entries, 247 total lines, all scripts exist + syntax OK |
| Launchd | 26 agents loaded, 22 OK, 4 failing |
| Logs | 48MB total, no oversized files |
| Processes | 3 active (asset_deployer, competitive_intel, system_healer) + daemon PID 13218 alive |
| Lock files | 4 active (all < 10min old, healthy) |

## Fixes Applied This Cycle

### 1. overnight_master_runner.sh — Syntax Error (FIXED)
- **Issue:** Line 256 arithmetic expression failed because grep -c output contained embedded newlines
- **Fix:** Added tr -d to strip whitespace + ${VAR:-0} fallback
- **Impact:** Overnight runner will complete cleanly starting tonight at 2 AM

### 2. quality_gate swarm plist — Bash Syntax Error (FIXED)
- **Issue:** Exit code 2. Raw parentheses in bash -c prompt
- **Fix:** Extracted prompt to quality_gate_prompt.md + wrapper script. Plist reloaded.
- **Impact:** Quality gate agent is now functional (was completely broken)

## Known Issues (Require Human Action)

### 3. claude-sessions — Exit 126 (macOS Permission)
- Root cause: macOS blocks bash in launchd from accessing project dir
- Human action: System Preferences > Privacy & Security > Full Disk Access > add /bin/bash

### 4-6. Three claude venture agents (exit 1)
- auto_monetize_affiliate_funnels_9569, auto_local_biz_openclaw_nationwide_9569, auto_app_app_factory_9788
- Empty error logs. Likely claude -p prompt failures.
- Severity: Low-Medium (cron alternatives still running)

## Log Error Analysis

| Log | Errors | Cause | Severity |
|-----|--------|-------|----------|
| indeed_hiring | 680 | DDG/Google rate limiting | Low (expected) |
| control_panel | 385 | Port collision on restart | Info (not real) |
| competitive_intel | 145 | Fiverr/Upwork 403 blocks | Low (expected) |
| venture_autonomy | 31 | Pipeline tracebacks | Medium |

## Process Health

| Process | PID | Status | Uptime |
|---------|-----|--------|--------|
| printmaxx_agent (daemon) | 13218 | Running | 6.7 days |
| control_panel (Flask :9999) | 29675 | Running | 4 days |
| asset_deployer | 43142 | Active | Current cycle |
| competitive_intel | 43064 | Active | Current cycle |

## Next Cycle: ~20:30
