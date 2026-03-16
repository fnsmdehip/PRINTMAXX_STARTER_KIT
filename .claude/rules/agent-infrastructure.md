# Agent Infrastructure

Root: `AUTOMATIONS/agent/` — orchestration, state, inter-agent communication.

## Core Agents
| Script | Purpose |
|--------|---------|
| `ceo_agent.py` | 24/7 orchestrator, 16 phases, xlsx scoring |
| `venture_autonomy.py` | 8 venture types, self-managing schedules |
| `agent_swarm.py` | 25 operational agents, launchd deployment |
| `loop_closer.py` | 3 loops: decisions, feedback, pipeline advancement |

## Venture Commands
- Status: `venture_autonomy.py --status`
- Run all: `--run-all` | Create: `--create TYPE NAME` | Bootstrap: `--bootstrap`
- Self-manage: `--self-manage` | Daemon: `--daemon`
- Types: OUTBOUND, CONTENT, APP, LOCAL_BIZ, RESEARCH, MONETIZE, PRODUCT, SCRAPING

## Swarm (25 agents, 6 categories)
- Status: `agent_swarm.py --status` | Deploy: `--deploy` | Health: `--health`
- Categories: META, DISCOVERY, ACTION, MEDIA, OPTIMIZE, QUALITY, INTELLIGENCE, MAINTENANCE, GROWTH, NOTIFICATION
- Total: 8 venture + 25 swarm = 33 autonomous agents via launchd

## State Files
- Agent state: `AUTOMATIONS/agent/state.json`
- CEO decisions: `AUTOMATIONS/agent/ceo_agent/decisions.jsonl`
- Missions: `AUTOMATIONS/agent/missions.jsonl`
- Message bus: `AUTOMATIONS/agent/message_bus.jsonl`
- Autonomy state: `AUTOMATIONS/agent/autonomy/autonomy_state.json`
- Swarm state: `AUTOMATIONS/agent/swarm/swarm_state.json`

## Quality Pipeline
- quality_gate (Opus, 2h) — HARD gate, blocks slop
- playwright_tester — auto-tests deployed sites

## Media Pipeline
- image_factory: Playwright HTML-to-image (zero cost)
- video_factory: Remotion (React video)
- Templates: `MEDIA/image_templates/`

## Loop Closer
- `loop_closer.py --cycle` (runs all 3 loops)
- Safety: max 10 actions/cycle, allowlisted actions, audit trail
- Schedule: every 2h cron + Phase 16 of CEO
