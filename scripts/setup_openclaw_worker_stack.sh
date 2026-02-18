#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"

RUN_ONBOARD=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-onboard)
      RUN_ONBOARD=1
      shift
      ;;
    *)
      echo "unknown_arg=$1" >&2
      echo "usage: $0 [--run-onboard]" >&2
      exit 2
      ;;
  esac
done

cd "$BASE"
mkdir -p "$BASE/logs"

echo "[1/6] set node role to worker"
python3 scripts/set_node_role.py worker

echo "[2/6] install secure cron"
bash scripts/install_secure_cron.sh

echo "[3/6] keep local model daemon online if available"
if command -v ollama >/dev/null 2>&1; then
  if ! pgrep -f "ollama serve" >/dev/null 2>&1; then
    nohup ollama serve >> "$BASE/logs/ollama_serve.log" 2>&1 || true
  fi
fi

echo "[4/6] check node runtime for official openclaw"
if ! command -v node >/dev/null 2>&1; then
  echo "node_missing=1 install_hint='brew install node@22'" >&2
  exit 1
fi

NODE_MAJOR=$(node -v | sed -E 's/^v([0-9]+).*/\1/')
if [[ -z "$NODE_MAJOR" || "$NODE_MAJOR" -lt 22 ]]; then
  echo "node_too_old=$(node -v) install_hint='brew install node@22 && brew link --overwrite node@22'" >&2
  exit 1
fi

echo "[5/6] install/upgrade openclaw cli"
if command -v openclaw >/dev/null 2>&1; then
  npm install -g openclaw@latest >/dev/null 2>&1 || npm install -g openclaw@latest
else
  npm install -g openclaw@latest
fi

echo "[6/6] seed hardened openclaw config template (if missing)"
mkdir -p "$HOME/.openclaw"
if [[ ! -f "$HOME/.openclaw/openclaw.json" ]]; then
  cp "$BASE/OPS/openclaw/openclaw_worker_template.json5" "$HOME/.openclaw/openclaw.json"
  echo "openclaw_config_seeded=1 path=$HOME/.openclaw/openclaw.json"
else
  echo "openclaw_config_exists=1 path=$HOME/.openclaw/openclaw.json"
fi

openclaw doctor || true

if [[ "$RUN_ONBOARD" -eq 1 ]]; then
  echo "running_openclaw_onboard=1"
  openclaw onboard --install-daemon
else
  cat <<EOF
next_steps:
  - run onboarding interactively once:
      openclaw onboard --install-daemon
  - verify daemon + gateway health:
      openclaw gateway status
      openclaw status
EOF
fi

echo "worker_openclaw_ready=1 base=$BASE"
