#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Generates HealthKit integration boilerplate (permissions manifest, step/heart-rate/sleep/workout fetch hooks, permission request UI component) and injects it into the app factory base template so every new fitness or streak app ships with HealthKit wired by default. Runs once on template change and on each new app scaffold.
# Created: 2026-03-24T18:50:41.189941
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_mit_repo_kingstinct_reactnat.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
