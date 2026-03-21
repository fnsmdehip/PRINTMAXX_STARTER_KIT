#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Generate llms.txt files for all 47+ deployed PRINTMAXX sites/apps with structured product summaries, deploy them to each site root, then bulk-submit to llms.txt directories (llmstxt.site, directory.llmstxt.cloud). This is GEO (Generative Engine Optimization) — the emerging equivalent of SEO but for AI chatbot discoverability. With 47+ live sites, this is a massive surface area play at $0 cost.
# Created: 2026-03-20T18:09:57.998938
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook__to_get_your_website_seen_on_c.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
