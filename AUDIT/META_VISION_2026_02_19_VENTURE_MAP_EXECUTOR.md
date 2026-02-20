# META VISION ADDENDUM — VENTURE MAP EXECUTOR

Date: 2026-02-19
Workspace: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt`

## Scope

Add an execution layer that processes the full `VENTURE_AUTOMATION_MAP` sheet
with dedupe + cooldown controls, then validate it in dry-run and apply modes.

Workbook used:

- `PRINTMAXX_MASTER_OPS_ENHANCED_2026-02-19.xlsx`

## New Artifact

- `AUTOMATIONS/venture_map_executor.py`

Core behavior:

- Loads all rows from `VENTURE_AUTOMATION_MAP`.
- Orders by readiness/source/score/signal.
- Supports blocker-aware prework gating (`--allow-blocked-prework` default on).
- Dedupes repeated command templates per pass (`--dedupe-commands` default on).
- Applies per-readiness cooldowns backed by persistent state.
- Writes structured outputs:
  - `output/venture_map_exec/manifest.json`
  - `output/venture_map_exec/latest.md`
- Persists state + run ledger:
  - `LEDGER/VENTURE_MAP_EXEC_STATE.json`
  - `LEDGER/VENTURE_MAP_EXEC_RUNS.csv`

## Validation Runs

### 1) Dry run

```bash
python3 AUTOMATIONS/venture_map_executor.py --workbook PRINTMAXX_MASTER_OPS_ENHANCED_2026-02-19.xlsx --max-rows 120 --max-per-lane 30 --max-commands 20
```

Observed:

- `rows_loaded=54`
- `rows_planned=52`
- `unique_commands=7`
- `skip_counts={"lane_cap": 2}`
- All command bundles were planned successfully.

### 2) Apply run

```bash
python3 AUTOMATIONS/venture_map_executor.py --workbook PRINTMAXX_MASTER_OPS_ENHANCED_2026-02-19.xlsx --max-rows 120 --max-per-lane 30 --max-commands 20 --reset-state --apply --timeout-sec 1200
```

Observed:

- `rows_loaded=54`
- `rows_planned=52`
- `unique_commands=7`
- `status_counts={"OK": 7}`
- Command failures: `0`

Executed command bundles:

1. `python3 AUTOMATIONS/clawdbot_rbi_engine.py --tick --max-intents 180 --max-syndication 420 --max-directories 900`
2. `python3 AUTOMATIONS/freelance_demand_scanner.py --hourly && python3 AUTOMATIONS/auto_freelance_responder.py --dry-run`
3. `python3 AUTOMATIONS/app_packager.py --write && python3 AUTOMATIONS/deploy_guard.py --tick`
4. `python3 AUTOMATIONS/gumroad_autolist_packager.py --write`
5. `python3 AUTOMATIONS/email_sender.py --preview --outreach AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv --max-sends 25`
6. `python3 AUTOMATIONS/alpha_monitor.py --cron`
7. `python3 AUTOMATIONS/ecom_arb_engine.py --hourly --top 2 && python3 AUTOMATIONS/ecom_autopilot.py --tick --top 12 --min-margin 20 --min-profit 3`

## Post-fix Note

Dry runs no longer mutate cooldown state.

Implementation detail:

- `update_state(...)` returns early when `apply` is false.

## Navigation Update

`CODEX.md` updated to include:

- `AUTOMATIONS/venture_map_executor.py`
- venture-map execution commands
- venture-map output and ledger paths
