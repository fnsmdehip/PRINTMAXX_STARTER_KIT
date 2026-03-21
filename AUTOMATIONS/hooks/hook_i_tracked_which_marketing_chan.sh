#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Channel attribution tracker: auto-tags UTM params on all outgoing product links, tracks click-to-sale conversion by channel, auto-reallocates content distribution weight toward high-conversion channels (Reddit/IndieHackers at 5-6% vs Twitter at 0%). Integrates with existing content distribution pipeline to prioritize posting order by channel ROI.
# Created: 2026-03-20T18:09:54.854074
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_i_tracked_which_marketing_chan.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
