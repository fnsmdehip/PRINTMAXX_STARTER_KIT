#!/bin/bash
set -euo pipefail

# One-command control-node bootstrap for a remote worker running PRINTMAXX +
# official OpenClaw. This script is intended to run on the control machine.

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <user@worker-host> <worker_project_path> [--run-onboard]" >&2
  echo "example: $0 macbookpro@192.168.1.44 /Users/macbookpro/PRINTMAXX_STARTER_KITttttt --run-onboard" >&2
  exit 1
fi

DEST_HOST="$1"
DEST_PATH="${2%/}"
RUN_ONBOARD=0

if [[ $# -ge 3 ]]; then
  if [[ "$3" == "--run-onboard" ]]; then
    RUN_ONBOARD=1
  else
    echo "unknown_arg=$3 (only --run-onboard is supported)" >&2
    exit 2
  fi
fi

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
cd "$BASE"

echo "[1/4] configuring ssh alias + key trust"
bash scripts/setup_control_to_worker_ssh.sh "$DEST_HOST" "$DEST_PATH"

echo "[2/4] syncing project to worker"
bash scripts/sync_to_worker.sh printmaxx-worker "$DEST_PATH"

echo "[3/4] bootstrapping worker runtime + official openclaw"
ssh printmaxx-worker "cd $DEST_PATH && bash scripts/setup_openclaw_worker_stack.sh"

if [[ "$RUN_ONBOARD" -eq 1 ]]; then
  echo "[4/4] running openclaw onboarding on worker (interactive)"
  ssh -t printmaxx-worker "cd $DEST_PATH && bash scripts/setup_openclaw_worker_stack.sh --run-onboard"
else
  echo "[4/4] onboarding skipped (pass --run-onboard to run now)"
fi

cat <<EOF
remote_worker_install_complete=1

next_steps:
  - enforce OpenRouter key caps from control node:
      cd $BASE
      python3 AUTOMATIONS/openrouter_budget_guard.py --enforce

  - set worker runtime key + gateway token on worker shell profile:
      export OPENROUTER_API_KEY=\"sk-or-...\"
      export OPENCLAW_GATEWAY_TOKEN=\"<long-random-token>\"

  - open control tunnel:
      ssh -N -L 18789:127.0.0.1:18789 printmaxx-worker

  - verify remote gateway:
      openclaw gateway status --url ws://127.0.0.1:18789 --token "\$OPENCLAW_GATEWAY_TOKEN"
EOF
