# META VISION ADDENDUM — SHIP CAPTAIN VENTURE MAP WIRING

Date: 2026-02-19
Workspace: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt`

## Scope

Wire the new all-venture executor into the persistent Ship Captain runtime loop
so it runs automatically with conservative cadence.

## Code Change

Updated:

- `AUTOMATIONS/ship_captain.py`

Added new auto step:

- `step_id`: `venture_map_exec`
- `command`:
  - `python3 AUTOMATIONS/net_guard.py --key venture_map_exec --min-interval-sec 21600 -- python3 AUTOMATIONS/venture_map_executor.py --max-rows 120 --max-per-lane 30 --max-commands 20 --apply`
- `timeout_sec`: `1500`

Swarm integration:

- Added `venture_map_exec` to swarm finalization sequence after:
  - `master_ops_exec_plan`

## Runtime Behavior

- Non-swarm mode:
  - Step runs as part of standard `AUTO_STEPS` sequence.
- Swarm mode:
  - Step runs in finalization phase (single-threaded post-lane).
- Frequency control:
  - Outer throttle: `net_guard` key `venture_map_exec` at 6h interval.
  - Inner throttle: `venture_map_executor.py` cooldown state in:
    - `LEDGER/VENTURE_MAP_EXEC_STATE.json`

## Validation

Validation commands run:

```bash
python3 -m py_compile AUTOMATIONS/ship_captain.py
python3 - <<'PY'
import AUTOMATIONS.ship_captain as s
step = next((x for x in s.AUTO_STEPS if x.step_id=='venture_map_exec'), None)
print(bool(step))
print(step.command if step else "")
PY
```

Result:

- `venture_map_exec` present in `AUTO_STEPS`
- command string matches intended throttled apply call
- swarm finalize list includes `venture_map_exec`

Guard behavior check:

```bash
python3 AUTOMATIONS/net_guard.py --key venture_map_exec --min-interval-sec 21600 -- python3 AUTOMATIONS/venture_map_executor.py --max-rows 120 --max-per-lane 30 --max-commands 20 --apply
```

Expected when recently run:

- best-effort skip via `net_guard` (exit 0, no runaway re-execution)

## Navigation Update

`CODEX.md` runtime loop section now documents:

- Ship Captain `venture_map_exec` auto step
- 6-hour throttle policy
- venture cooldown state file path
