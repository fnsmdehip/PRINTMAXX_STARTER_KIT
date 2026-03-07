# SYSTEM HEALER — Health Report
**Date:** 2026-03-07 01:15 AM
**Agent:** system_healer (com.printmaxx.swarm.system_healer)
**Cycle:** 2-hour scheduled run

---

## DISK
- **Root:** 17GB used / 926GB total (22%) — OK, well above 10GB threshold
- **Logs dir:** 15MB (after cleanup) — healthy

## CRON
- **Daemon:** RUNNING (PID 212)
- **Active entries:** 98 active cron jobs
- **Script existence check:** ALL 32 critical scripts found — no missing references

## LAUNCHD
| Agent | Status | Action |
|-------|--------|--------|
| com.printmaxx.swarm.quality_gate | exit 2 → **FIXED** | Bash syntax error: unescaped `"` in claude prompt broke bash -c string. Fixed: replaced inner `&quot;` with single quotes, reloaded plist |
| com.printmaxx.claude-sessions | exit 126 (OPEN ISSUE) | "Operation not permitted" — macOS TCC/Full Disk Access restriction on launchd agent. Requires user action: System Settings > Privacy & Security > Full Disk Access — add Terminal or bash |
| com.printmaxx.swarm.asset_deployer | running (PID 27022) | OK |
| com.printmaxx.swarm.content_compounder | running (PID 27023) | OK |
| com.printmaxx.swarm.system_healer | running (PID 27027) | OK |
| All other swarm agents | idle (exit 0) | OK |

## PROCESSES
- **printmaxx_agent.py:** was DEAD (stale PID 82736). **Restarted as PID 32266** — daemon.log confirms clean start.
- **monitor.pid (87051):** process not running. Non-critical (dashboard server, not mission-critical).
- **Lock files:** None found — clean.
- **Zombie processes:** None detected.

## LOGS
### Errors Found
| Log | Issue |
|-----|-------|
| sam_gov_monitor.log | HTTP 404s on keyword searches (SAM.gov API endpoint issues) — non-blocking, scraper falls back to HTML |
| quality_gate error log | bash syntax error (fixed above) |

### No errors in:
- decision_engine.log — running clean, processing freelance + ecom cycles
- guardian_heal.log — healed 2 issues at 00:30 (HEARTBEAT refresh + search index rebuild)
- alpha_processor.log — completed clean at 00:41
- competitive_intel.log — 163 rows written at 00:38

### Log Cleanup
- **Truncated to 2000 lines:** alpha_processor.log (9019→2000), compliance_scan.log (6075→2000), rbi_scanner.log (6192→2000), indeed_hiring.log (3143→2000), uk_contracts.log (8939→2000), sam_gov_monitor.log (6638→2000)
- **Archived:** overnight_2026-02-27, 02-28, 03-01, 03-05 → overnight_archive_20260307.tar.gz (269KB)
- **Savings:** ~3MB freed

## SYSTEM STATUS
- **Disk:** 59GB free — OK
- **Active pipelines:** decision_engine (30min cycle), guardian (15min pulse), perpetual_guardian (heal every 4h)
- **Agent daemon:** restarted and healthy
- **Quality gate:** fixed and operational

---

## OPEN ISSUES (require user action)
1. **com.printmaxx.claude-sessions (exit 126):** macOS Full Disk Access needed.
   Fix: System Settings > Privacy & Security > Full Disk Access > add `/bin/bash` or Terminal.
   This affects the 3x daily scheduled Claude sessions (7am/1pm/6pm).

2. **SAM.gov 404s:** API endpoint may have changed. `sam_gov_monitor.py` falls back to HTML scraping but results are sparse. Low priority.

---

## FIXES APPLIED THIS CYCLE
1. Fixed `com.printmaxx.swarm.quality_gate.plist` — bash syntax error causing exit code 2 every 2 hours
2. Restarted `printmaxx_agent.py` daemon (PID 32266)
3. Truncated 6 oversized log files to 2000 lines
4. Archived 4 old overnight log files
