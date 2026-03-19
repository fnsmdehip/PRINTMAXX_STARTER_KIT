# Sovrun Feature Guide — What Runs Automatically vs What You Can Trigger

## AUTOMATIC (no action needed, already running)

| Feature | When | What It Does |
|---|---|---|
| Method discovery crawler | 5 AM daily cron | Crawls 18 subreddits + HN + Twitter for new revenue methods |
| Capital Genesis ranker | 5:30 AM daily cron | Scores all methods, outputs priority stack |
| CEO agent reads priority stack | Every 2h CEO cycle | Uses Capital Genesis rankings in decisions |
| Daily planner reads priority stack | 7 AM daily | Incorporates top priorities into daily plan |
| Actionable aggregator reads priority stack | 7:30 AM daily | Pulls P0 items into actionable queue |
| Procedural memory capture | Every agent run | Captures successful task solutions as skills |
| Procedural memory injection | Every agent run | Injects relevant past skills into agent prompts |
| Boomer alpha routing | Every alpha review cycle | Agents discover boomer demographic alpha via intelligence router |
| Edge mindset rule | Every session | Silent 5-point competitive check on all significant outputs |
| Bias-null protocol | Every session | Silent 5-point pre-output filter |
| Soul drift scoring | Every 2h (loop closer) | Scores agent outputs 0-10 against SOUL.md |
| Voice model injection | Every agent run | Agents match your tone/vocabulary |

## OPT-IN (run when you want them)

| Feature | Command | When To Use |
|---|---|---|
| `/edge` | `/edge <target> [cycles]` | Apply competitive edge thinking (baseline → synergy → MEV) |
| `/refine` | `/refine <file> [cycles]` | Improve content quality through cognitive refinement cycles |
| CEO DAG mode | `python3 AUTOMATIONS/ceo_agent.py --dag` | Run CEO phases in parallel instead of sequential |
| Agent handoff | `python3 AUTOMATIONS/agent_swarm.py --handoff SOURCE TARGET "task"` | Real-time agent-to-agent delegation |
| Skills query | `python3 AUTOMATIONS/agent_swarm.py --skills "search"` | Search procedural memory for past solutions |
| Memory consolidation | `sovrun-memory --consolidate` | Extract skills from conversation history |
| MCP server | `sovrun-mcp --serve` | Expose agents as MCP tools for external systems |
| Tracing | `sovrun-trace --agents` | Per-agent token usage and cost breakdown |
| HTML trace | `sovrun-trace --html TRACE_ID` | Visual timeline of agent execution |
| Durable replay | `sovrun-durable --replay ID` | View crash recovery replay data |
| Connector setup | `python3 connectors/setup.py --list` | See available MCP connectors |

## DECISION-SUPPORT (system checks these for you)

| Feature | How It Helps |
|---|---|
| Capital Genesis Priority Stack | When you ask "what should I work on?" — system checks ranked priorities |
| Intelligence Router | Before any agent action — queries 484 docs + 14.8K alpha entries |
| Procedural Memory | Before any agent run — searches for relevant past solutions |
| Competitive Analysis | When evaluating sovrun vs competitors — OPS/SOVRUN_COMPETITIVE_ANALYSIS.md |
| Boomer Alpha Thesis | When planning content/affiliate — full playbook with specific affiliate programs |

## SHOULD ADD TO CRON (recommended)

| Feature | Suggested Cron | Why |
|---|---|---|
| Memory consolidation | `0 4 * * *` (4 AM daily) | Auto-extract skills from conversation history |
| Tracing cost report | `0 23 * * *` (11 PM daily) | Track daily token spend |
