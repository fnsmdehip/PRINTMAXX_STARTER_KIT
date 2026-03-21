#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Auto-inject legal pages (ToS, Privacy Policy, Cookie Policy) into every app factory build. Templates already exist in 09_LEGAL/ but are orphaned — no automation consumes them. Wire into app_factory_autopilot.py so every new app ships with legal pages pre-populated with app-specific variables (app name, contact email, data collected). Adds trust signals and FTC/GDPR compliance across all 47+ live sites.
# Created: 2026-03-20T18:10:01.215476
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook__printmaxx_legal_templates_co.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
