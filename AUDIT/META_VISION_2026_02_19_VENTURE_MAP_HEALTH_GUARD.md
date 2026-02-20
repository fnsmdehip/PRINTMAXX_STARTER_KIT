# META VISION ADDENDUM — VENTURE MAP HEALTH GUARD

Date: 2026-02-19
Workspace: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt`

## Scope

Add a strict health guard for venture-map execution freshness and wire it into
Ship Captain so stale execution is surfaced automatically.

## New Artifact

- `AUTOMATIONS/venture_map_health_check.py`

Behavior:

- Reads `LEDGER/VENTURE_MAP_EXEC_RUNS.csv`
- Computes latest successful run age and latest batch status counts
- Marks status:
  - `OK` if last success <= `--max-age-hours`
  - `STALE` if last success > `--max-age-hours`
  - `CRITICAL` if too old (`--critical-age-hours`) or no successful history
- Writes:
  - `output/venture_map_health/manifest.json`
  - `output/venture_map_health/latest.md`
  - `LEDGER/VENTURE_MAP_HEALTH.csv`
- Exit code policy:
  - `0` OK
  - `1` STALE
  - `2` CRITICAL
  - `--no-fail` forces exit 0

## Ship Captain Wiring

Updated:

- `AUTOMATIONS/ship_captain.py`

Added step:

- `step_id`: `venture_map_health`
- command:
  - `python3 AUTOMATIONS/venture_map_health_check.py --max-age-hours 12 --critical-age-hours 24`
- timeout: `120s`

Swarm finalize order now includes:

- `venture_map_exec`
- `venture_map_health`

## Fleet Visibility

Updated:

- `AUTOMATIONS/cron_fleet_report.py`

Now tracks these additional artifacts:

- `output/venture_map_exec/latest.md`
- `output/venture_map_exec/manifest.json`
- `output/venture_map_health/latest.md`
- `output/venture_map_health/manifest.json`
- `LEDGER/VENTURE_MAP_EXEC_RUNS.csv`
- `LEDGER/VENTURE_MAP_HEALTH.csv`

## Validation

Commands run:

```bash
python3 -m py_compile AUTOMATIONS/venture_map_health_check.py
python3 -m py_compile AUTOMATIONS/ship_captain.py
python3 -m py_compile AUTOMATIONS/cron_fleet_report.py
python3 AUTOMATIONS/venture_map_health_check.py --max-age-hours 12 --critical-age-hours 24 --no-fail
```

Expected outcome:

- Health artifacts are written
- Status reflects current venture-map run freshness

Observed on validation run:

- `status=OK`
- `last_ok_age_h=5.58`
