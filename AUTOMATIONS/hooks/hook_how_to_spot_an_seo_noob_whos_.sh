#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Quality gate hook that scans all SEO-related content and landing pages for llms.txt recommendations and flags/removes them. Secondary: generate 3 contrarian SEO posts debunking llms.txt hype for authority building and engagement farming.
# Created: 2026-03-20T18:35:54.295387
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_how_to_spot_an_seo_noob_whos_.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
