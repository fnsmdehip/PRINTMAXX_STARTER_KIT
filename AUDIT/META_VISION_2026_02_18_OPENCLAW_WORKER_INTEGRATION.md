# META VISION Addendum: Official OpenClaw Worker Integration

Date: 2026-02-18

## Scope

This addendum records the infrastructure changes that integrate official OpenClaw into PRINTMAXX while preserving worker-node isolation and budget guardrails.

## New/Updated Artifacts

### New files

1. `AUTOMATIONS/openrouter_budget_guard.py`
2. `OPS/OPENROUTER_BUDGET_POLICY.json`
3. `scripts/setup_openclaw_worker_stack.sh`
4. `scripts/setup_control_to_worker_ssh.sh`
5. `OPS/openclaw/openclaw_worker_template.json5`
6. `OPS/OPENCLAW_WORKER_ISOLATION_RUNBOOK_2026_02_18.md`
7. `AUDIT/META_VISION_2026_02_18_OPENCLAW_WORKER_INTEGRATION.md`

### Updated files

1. `AUTOMATIONS/crontab_secure_minimal.txt`
2. `scripts/install_secure_cron.sh`
3. `CODEX.md`

### External upstream source present

- `external/openclaw-official` (official OpenClaw repository clone for reference/integration)

## What Changed Operationally

1. Official OpenClaw bootstrap path now exists for worker setup:
   - Installs/updates `openclaw` CLI
   - Validates Node >= 22
   - Seeds worker-safe OpenClaw config if missing
2. Control-node SSH bootstrap path now exists:
   - Key generation + authorized key wiring
   - `printmaxx-worker` SSH alias creation
   - Runbook command output for sync and remote setup
3. Hard OpenRouter key budget guard now exists:
   - Declarative policy in `OPS/OPENROUTER_BUDGET_POLICY.json`
   - Create/update keys with daily limits via OpenRouter Keys API
   - Daily cron enforcement added in secure cron profile
4. Agent navigation contract updated in `CODEX.md`:
   - New runbook and command references added for OpenClaw + budget guard

## Budget Safety Outcome

With policy defaults (`monthly_budget_usd=100`, `daily_divisor_days=30`), runtime key budget resolves to a daily cap around `$3.33/day`, preventing single-day budget exhaustion.

## Isolation Outcome

Worker runtime remains isolated by design:

- Execution loops run on worker filesystem only.
- Gateway bind model is loopback-first with SSH tunnel control.
- Control node remains orchestrator/supervisor rather than execution host.

## Verification Commands

```bash
# Policy dry-run (no key mutations)
python3 AUTOMATIONS/openrouter_budget_guard.py --enforce --dry-run

# Live policy enforcement
python3 AUTOMATIONS/openrouter_budget_guard.py --enforce

# Worker stack bootstrap
bash scripts/setup_openclaw_worker_stack.sh

# Control->worker SSH bootstrap
bash scripts/setup_control_to_worker_ssh.sh <user@worker-host> <worker_project_path>
```
