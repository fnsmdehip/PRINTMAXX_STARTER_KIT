#!/bin/bash
set -euo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
cd "$BASE"

mkdir -p logs

ts="$(date +%Y%m%d_%H%M%S)"
backup="logs/crontab_backup_${ts}.txt"

crontab -l > "$backup" || true

tmp="/tmp/printmaxx_cron_merged_${ts}.txt"
cp "$backup" "$tmp"

if ! rg -q "PRINTMAXX_SHIP_CAPTAIN" "$tmp"; then
  {
    echo ""
    echo "# ============================================================"
    echo "# PRINTMAXX SHIP CAPTAIN (control loop)"
    echo "# ============================================================"
    echo "*/30 * * * * cd \$BASE && /bin/bash ./ship.sh >> logs/ship_cron.log 2>&1 # PRINTMAXX_SHIP_CAPTAIN"
  } >> "$tmp"
fi

if ! rg -q "PRINTMAXX_OLLAMA" "$tmp"; then
  {
    echo ""
    echo "# Keep local model tier online"
    echo "@reboot cd \$BASE && nohup /opt/homebrew/bin/ollama serve >> logs/ollama_serve.log 2>&1 # PRINTMAXX_OLLAMA"
  } >> "$tmp"
fi

crontab "$tmp"
echo "cron_merged=1 backup=$backup"
crontab -l | rg -n "PRINTMAXX_SHIP_CAPTAIN|PRINTMAXX_OLLAMA" || true

