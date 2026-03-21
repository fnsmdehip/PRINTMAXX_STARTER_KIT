#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Entry is malformed — the 'method' field contains the CSV column header row (alpha_id,source,source_url,...) rather than actual method content. ALPHA10700 from @pipelineabuser has a truncated source URL and no extractable tactic. Procedural memory shows this exact pattern repeated 3x with $0 revenue outcome each time. Root cause: orphan_doc_scanner is staging the CSV schema row as alpha entries when it scans malformed or header-only rows.
# Created: 2026-03-20T23:12:24.837911
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_alpha_idsourcesource_urlcat.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
