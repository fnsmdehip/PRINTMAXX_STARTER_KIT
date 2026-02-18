#!/bin/bash
set -euo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
cd "$BASE"

python3 scripts/set_node_role.py worker
bash scripts/install_secure_cron.sh

# Start local model daemon if available (safe if already running)
if command -v ollama >/dev/null 2>&1; then
  nohup ollama serve >> "$BASE/logs/ollama_serve.log" 2>&1 || true
fi

echo "worker_ready=1 base=$BASE role=worker"
