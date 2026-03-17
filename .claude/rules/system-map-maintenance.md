# System Map Maintenance (MANDATORY)

**File:** `OPS/PRINTMAXX_SYSTEM_MAP.md` — the canonical live architecture map.

## When to READ it
- Before ANY system analysis, architecture discussion, naming, or repo scoping
- Before describing "what this system does" to anyone or any agent
- When onboarding to a session that involves infrastructure work
- When spawning subagents that need system context — feed them the map

## When to UPDATE it (same session, no exceptions)
- Added/removed/modified an agent
- Changed cron schedule or timing
- Added/removed/modified a script in AUTOMATIONS/
- Changed data flow between components
- Added new state files or control surfaces
- Changed the execution hierarchy (L0-L6)
- Modified resilience, health monitoring, or guardrails
- Added new ventures, hooks, or integration points

## What to update
- Header comment (script count, agent count, cron count)
- `Latest verified` date
- Relevant section (STRUCTURE TREE, EXECUTION HIERARCHY, DATA FLOW, AGENT TOPOLOGY, CRON SCHEDULE, STATE FILES, etc.)
- Add new components to the correct layer (L0-L6)

## Why this exists
The system map was 4 days stale despite the rule existing in CLAUDE.md. The rule was buried in a reference table. This dedicated rules file auto-loads every session to prevent that from happening again. A stale map means subagents analyzing the system get wrong information, naming decisions miss capabilities, and architecture discussions are based on outdated state.
