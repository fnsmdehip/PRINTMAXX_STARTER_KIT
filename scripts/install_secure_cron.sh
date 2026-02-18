#!/bin/bash
set -euo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
CRON_FILE="$BASE/AUTOMATIONS/crontab_secure_minimal.txt"

if [[ ! -f "$CRON_FILE" ]]; then
  echo "missing_cron_file=$CRON_FILE" >&2
  exit 1
fi

crontab "$CRON_FILE"
echo "installed_secure_cron_from=$CRON_FILE"
crontab -l | grep -E "PRINTMAXX_SHIP_CAPTAIN|PRINTMAXX_OPENROUTER_BUDGET_GUARD|PRINTMAXX_OLLAMA" || true
