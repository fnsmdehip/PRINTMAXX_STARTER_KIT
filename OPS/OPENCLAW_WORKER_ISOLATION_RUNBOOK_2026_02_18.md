# PRINTMAXX OpenClaw Worker Isolation Runbook

Date: 2026-02-18

## Goal

Run official OpenClaw + PRINTMAXX automation on the M2 worker only, controlled from the M1, with hard daily API spend limits.

## Topology

- Control node (M1 64GB): command, supervision, approvals.
- Worker node (M2 16GB): OpenClaw gateway + Ship Captain loops.
- Source of truth repo: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt`

## 0) Required one-time secrets

Set these on the worker shell profile (`~/.zshrc`) before live runs:

```bash
export OPENROUTER_API_KEY="sk-or-..."            # runtime key (daily-capped)
export OPENCLAW_GATEWAY_TOKEN="replace-me-long-random"
```

Optional admin key on control node for policy enforcement:

```bash
export OPENROUTER_ADMIN_API_KEY="sk-or-admin-..."
```

## 1) On control node (M1): establish SSH link + alias

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
bash scripts/setup_control_to_worker_ssh.sh <user@worker-host> <worker_project_path>
```

Example:

```bash
bash scripts/setup_control_to_worker_ssh.sh macbookpro@192.168.1.44 /Users/macbookpro/PRINTMAXX_STARTER_KITttttt
```

This script:

- creates key `~/.ssh/printmaxx_worker_ed25519`
- appends key to worker `authorized_keys`
- creates SSH alias `printmaxx-worker`

## 2) Sync repo to worker

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
bash scripts/sync_to_worker.sh printmaxx-worker /Users/macbookpro/PRINTMAXX_STARTER_KITttttt
```

## 3) Prepare worker runtime (official OpenClaw + worker role)

```bash
ssh printmaxx-worker "cd /Users/macbookpro/PRINTMAXX_STARTER_KITttttt && bash scripts/setup_openclaw_worker_stack.sh"
```

This performs:

- `NODE_ROLE=worker`
- secure cron install
- `ollama serve` keepalive (if installed)
- Node >=22 check
- `npm install -g openclaw@latest`
- seed `~/.openclaw/openclaw.json` from `OPS/openclaw/openclaw_worker_template.json5` (if missing)

## 4) Finish OpenClaw onboarding once (interactive)

```bash
ssh -t printmaxx-worker "cd /Users/macbookpro/PRINTMAXX_STARTER_KITttttt && bash scripts/setup_openclaw_worker_stack.sh --run-onboard"
```

## 5) Use remote tunnel from control node

Terminal A (keep running):

```bash
ssh -N -L 18789:127.0.0.1:18789 printmaxx-worker
```

Terminal B:

```bash
openclaw gateway status --url ws://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
openclaw status --url ws://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
```

## 6) Enforce hard daily OpenRouter caps

Policy file:

- `OPS/OPENROUTER_BUDGET_POLICY.json`

Guard script:

- `AUTOMATIONS/openrouter_budget_guard.py`

Run from control node:

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
python3 AUTOMATIONS/openrouter_budget_guard.py --enforce
```

Dry run:

```bash
python3 AUTOMATIONS/openrouter_budget_guard.py --enforce --dry-run
```

Read-only status:

```bash
python3 AUTOMATIONS/openrouter_budget_guard.py --status
```

Outputs:

- `output/openrouter_budget_guard/latest.json`
- `output/openrouter_budget_guard/latest.md`
- `LEDGER/OPENROUTER_BUDGET_GUARD.csv`

## 7) Put the daily-capped key on worker

After `--enforce`, copy the created runtime key value into worker `OPENROUTER_API_KEY`.

Keep worker using only that key for loops.

## 8) Start PRINTMAXX loop on worker only

```bash
ssh printmaxx-worker "cd /Users/macbookpro/PRINTMAXX_STARTER_KITttttt && ./ship.sh"
```

Or rely on secure cron every 30 minutes (`AUTOMATIONS/crontab_secure_minimal.txt`).

## 9) Why this isolates blast radius

- All live loops execute on worker filesystem.
- Control node only sends commands via SSH.
- `sync_to_worker.sh` has destination safety checks to prevent remote wipes.
- OpenClaw gateway remains loopback-only on worker and is reached through SSH tunnel.
- OpenRouter runtime key has strict daily spend cap.

## 10) Official OpenClaw source reference

Official repo now exists in this project:

- `external/openclaw-official`

Use it as upstream reference while keeping runtime automation in PRINTMAXX scripts.
