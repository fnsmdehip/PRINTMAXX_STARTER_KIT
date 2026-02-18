#!/bin/bash
set -euo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
cd "$BASE"

python3 scripts/set_node_role.py control
bash scripts/install_secure_cron.sh

echo "control_ready=1 base=$BASE role=control"
