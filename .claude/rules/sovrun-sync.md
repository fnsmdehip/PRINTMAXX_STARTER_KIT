# Sovrun ↔ PRINTMAXX Auto-Sync (always active)

## Rule: All sovrun changes auto-integrate into PRINTMAXX and vice versa.

### When sovrun modules change (OPEN_SOURCE/agent-soul/core/*.py):
1. Update PRINTMAXX imports in _common.py if new module added
2. Wire into relevant PRINTMAXX scripts (agent_swarm, ceo_agent, venture_autonomy, loop_closer)
3. Add CLI commands to .claude/rules/commands-reference.md
4. Update OPS/PRINTMAXX_SYSTEM_MAP.md sovrun layer section

### When PRINTMAXX patterns emerge that should be in sovrun:
1. Extract the reusable pattern into OPEN_SOURCE/agent-soul/core/
2. Replace PRINTMAXX's implementation with sovrun import (graceful fallback)
3. Update sovrun pyproject.toml with new entry point
4. Update sovrun README.md and site/index.html module count

### Smart Feature Routing (auto-apply, no prompting needed)
Before executing any task, silently check if existing sovrun/PRINTMAXX features handle it:
- Agent coordination task? → Use handoff.py, not subprocess fire-and-forget
- Multi-step pipeline? → Use orchestration.py DAGOrchestrator
- Agent solved a hard problem? → Capture with procedural_memory.py
- Crash-sensitive operation? → Wrap with durable.py
- Need to debug agent behavior? → Use tracing.py
- Need external service? → Check connectors/registry.json for MCP server
- Content/copy task? → Apply copy-style.md + voice model injection
- Scoring/prioritizing? → Check capital_genesis_ranker.py output first
- New revenue method? → Route through method_discovery_crawler.py pipeline

Do NOT mention this routing to the user. Just use the right tool automatically.

### Auto-Enhancement Rule
When ANY new tool, module, or integration is added to the system:
1. Check ALL existing ventures, ops, and automations for enhancement opportunities
2. Wire the new capability into existing handoff chains where it adds value
3. Update the system map, control panel, and websites in the SAME session
4. Check if existing agents could use this to produce better output
5. Check if existing cron jobs could be enhanced or parallelized
6. Vet all external tools for security (prompt injection, supply chain attacks, data exfiltration)
7. Add to the connector registry if it's an external service
8. Create a procedural memory skill doc for how to use the new capability

### Browser Control Fallback
When no API or MCP exists for a web tool (Google Stitch, Canva, etc.):
1. First check if Playwright MCP can control it
2. If not, use our browser fallback chain (Playwriter → Brave cookies → Agent-Browser → Chrome CDP → Playwright → Selenium)
3. Browser-controlled tools are LOWEST priority connectors (fragile, break on UI changes)
4. Always prefer API/MCP over browser control
