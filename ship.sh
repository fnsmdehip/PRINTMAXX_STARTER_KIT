#!/bin/bash
set -euo pipefail

cd "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
# Swarm mode: parallel lanes with capped concurrency. Safe: critical steps still
# require human approvals + worker role.
python3 AUTOMATIONS/ship_captain.py --run --swarm --max-parallel 4 "$@"
