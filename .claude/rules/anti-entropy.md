# Anti-Entropy Rules (ALWAYS active)

## The Problem This Solves
The system reached 428 automation scripts, $0 revenue, 3 dead loops, 38% OAuth failures, and 4-day silent cron death. These rules prevent that from recurring.

## Before Creating ANY New Script
1. **Name the caller.** Who runs this? Cron? Another script? If nobody, don't create it.
2. **Name the existing alternative.** Can an existing script be parameterized? If yes, extend it.
3. **Run it immediately.** Don't just write it. Execute it. Check output. Fix errors. Re-run.
4. **Wire it.** Add cron entry, add to morning DAG, or add as venture pipeline step in SAME session.
5. **Count before creating.** `ls AUTOMATIONS/*.py | wc -l` — if >400, you MUST delete/consolidate before adding.

## OAuth / API Key Safety
- Every `subprocess.run(["claude"...)` call MUST include `--api-key` when `ANTHROPIC_API_KEY` is set
- Pattern to use everywhere:
  ```python
  cmd = ["claude", "-p"]
  if os.environ.get("ANTHROPIC_API_KEY"):
      cmd.append("--api-key")
  ```
- Every LLM call MUST have a heuristic fallback for when the call fails
- Test auth before running 300+ entries: run 1 entry first, check for 401, fix before proceeding

## Loop Health Checks
- Run `python3 AUTOMATIONS/loop_closer.py --status` at session start
- If ANY loop shows DEAD or STALE: fix it BEFORE doing other work
- All 4 loops must show OK: Decision Execution, Feedback Tracking, Pipeline Advancement, Soul Drift
- Cron watchdog runs hourly via launchd (`com.printmaxx.cron-watchdog`)

## Cron Resilience
- Cron watchdog (`AUTOMATIONS/cron_watchdog.py`) checks hourly for 9 required crons
- If crons are wiped, watchdog auto-restores from `AUTOMATIONS/agent/cron_backup.txt`
- After ANY cron change: verify with `crontab -l | grep PRINTMAXX | wc -l` (should be 10+)
- NEVER run `crontab -r` or equivalent

## Venture Pipeline Health
- Steps that need human action: mark as `human_blocked`, don't waste LLM tokens
- Steps that fail on auth: use `--api-key` flag, fall back to heuristic
- Steps missing script mappings: add the mapping, don't leave it to `_run_with_claude()`
- After ANY venture change: `python3 AUTOMATIONS/venture_autonomy.py --status` to verify

## RBI Discipline (Research, Backtest, Implement)
- Before building anything new: `python3 AUTOMATIONS/rbi_loop.py --research`
- Before implementing: `python3 AUTOMATIONS/rbi_loop.py --backtest`
- Only implement PASS methods, log CONDITIONAL to actionable queue
- This replaces "build whatever sounds good" with "validate then build"

## Revenue Reality Check (run before ANY autonomous building session)
- Current revenue: check `FINANCIALS/revenue_pipeline.json`
- If $0: ask "will this specific action lead to a dollar entering a bank account?"
- If "no" or "indirectly": deprioritize in favor of direct revenue actions
- The system builds systems that build systems. Break the cycle.

## Anti-Patterns This Rule Kills
- Creating scripts nobody calls
- Running `claude -p` without `--api-key` in headless contexts
- Scheduling crons without testing the script first
- Letting loops die silently for days
- Building new automations when existing ones are broken
- OAuth tokens expiring and killing entire pipelines
- 428 scripts growing to 500 scripts with zero additional revenue
