# PRINTMAXX — Autonomous Revenue System

392 scripts. 33 agents. 109 cron jobs. 30 revenue lanes. $0 → $200K+ target.

## what this is

a fully autonomous revenue generation system. agents scrape, analyze, build, deploy, and optimize across 30 venture types simultaneously. the system produces its own daily action plans, audits its own output quality, and closes its own loops. human does: account creation, payments, API keys.

## stack

Python 3.10+ | Playwright | Claude API (Opus/Sonnet/Haiku routing) | Next.js | Surge/Vercel | SQLite FTS5

## system architecture

```
CEO AGENT (24/7 orchestrator, 16 phases)
    |
    +-- VENTURE AUTONOMY ENGINE (30 venture types, self-managing)
    |       |-- APP_FACTORY, EAS, OUTBOUND, CONTENT_FARM, LOCAL_BIZ...
    |       +-- each venture: scrape → analyze → build → deploy → optimize
    |
    +-- AGENT SWARM (33 agents, smart model routing)
    |       |-- META: ceo, quality_gate, loop_closer
    |       |-- DISCOVERY: competitor_stalker, gap_hunter
    |       |-- ACTION: lead_machine, app_factory_autopilot
    |       |-- INTELLIGENCE: alpha_query, intelligence_router
    |       +-- GROWTH: twitter_warmup, content_distributor
    |
    +-- INTELLIGENCE PIPELINE
    |       |-- 484 docs mapped, 23K+ alpha entries, 16 CSVs
    |       |-- SQLite FTS5 index (full-text search across all alpha)
    |       |-- intelligence_router.py (central hub, queried before every action)
    |       +-- alpha_auto_processor.py (routes findings to ventures)
    |
    +-- COGNITIVE ENGINE (agent-soul)
    |       |-- voice_extractor: learns YOUR communication style from prompt history
    |       |-- cognitive_engine: correction chains + meta-rules from 1,510 prompts
    |       |-- pattern_miner: finds what makes you push back vs say "perfect"
    |       |-- user_sim_refiner: simulates your critique autonomously
    |       |-- loop_closer: soul drift scoring (0-10 alignment check)
    |       +-- bias-null protocol: 5-point pre-output filter
    |
    +-- RESILIENCE LAYER
    |       |-- agent_resilience.py: retry/backoff, file locking, circuit breaker
    |       |-- perpetual_guardian.py: 4h watchdog, self-heal, auto-commit/push
    |       |-- guardrails.py: all file ops locked to project root
    |       +-- security_audit.py: 6-category scan (secrets, injection, prompt injection)
    |
    +-- CONTENT & DISTRIBUTION
    |       |-- 588 posts generated, 40 approved, warmup scheduler
    |       |-- weighted voice aggregation (S/A/B/C tier account modeling)
    |       |-- image_factory (Playwright HTML-to-image, zero cost)
    |       +-- daily_engagement_planner.py (auto-generates daily action plans)
    |
    +-- DECISION ENGINE
            |-- rule-based + LLM pipeline, full CSV audit trail
            |-- every decision logged with reasoning
            +-- loop_closer verifies decisions led to results
```

## numbers

| metric | count |
|--------|-------|
| automation scripts | 392 (351 Python, 41 Shell) |
| autonomous agents | 33 (8 venture + 25 swarm) |
| cron jobs | 109 |
| revenue ventures | 30 |
| deployed apps/sites | 126 URLs |
| alpha intelligence entries | 23,429 |
| lead database rows | 10,521 across 75 CSVs |
| product files | 367 |
| intelligence docs mapped | 484 |
| correction chains analyzed | 168 (avg 6.9 corrections → target: 1) |

## key components

| script | what it does |
|--------|-------------|
| `AUTOMATIONS/ceo_agent.py` | 24/7 orchestrator, 16 phases, intelligence injection |
| `AUTOMATIONS/venture_autonomy.py` | 30 venture types, self-managing schedules |
| `AUTOMATIONS/agent_swarm.py` | 33 agents, Opus/Sonnet/Haiku model routing |
| `AUTOMATIONS/intelligence_router.py` | central intelligence hub, queried before every action |
| `AUTOMATIONS/loop_closer.py` | 4 loops: decisions, feedback, pipeline, soul drift |
| `AUTOMATIONS/perpetual_guardian.py` | 4h watchdog: commit, push, self-heal, cron audit |
| `AUTOMATIONS/decision_engine.py` | rule-based + LLM decisions with CSV audit trail |
| `AUTOMATIONS/agent_resilience.py` | retry/backoff, file locking, circuit breaker |
| `AUTOMATIONS/control_panel.py` | ONE dashboard at localhost:9999 |
| `AUTOMATIONS/daily_digest.py` | surfaces what system did overnight (cron 6:45 AM) |
| `AUTOMATIONS/session_briefing.py` | agents wake up informed, no LLM calls, < 30 seconds |
| `AUTOMATIONS/user_voice_model.py` | learns user communication style from prompt history |
| `AUTOMATIONS/competitive_cognition_audit.py` | weekly self-audit of system cognition quality |

## quick start

```bash
# clone
git clone https://github.com/fnsmdehip/PRINTMAXX_STARTER_KIT.git
cd PRINTMAXX_STARTER_KIT

# the real instructions live here
cat .claude/CLAUDE.md

# check system health
python3 AUTOMATIONS/system_health_monitor.py --quick

# run decision engine
python3 AUTOMATIONS/decision_engine.py --cycle

# check agent swarm
python3 AUTOMATIONS/agent_swarm.py --status

# check ventures
python3 AUTOMATIONS/venture_autonomy.py --status

# dashboard
python3 AUTOMATIONS/control_panel.py  # localhost:9999
```

## session workflow

```bash
# 1. read briefing
cat OPS/SESSION_BRIEFING.md

# 2. run decision engine
python3 AUTOMATIONS/decision_engine.py --cycle

# 3. check actionable queue
cat OPS/ACTIONABLE_QUEUE.md

# 4. deploy anything deployable

# 5. update tracker + generate content on exit
```

## operating rules

1. **SHIP NOW** — deploy what exists before building new things
2. **NO ORPHANS** — every doc has a consumer (agent or human task)
3. **NO SLOP** — no AI vocabulary, no em dashes, copy style enforced
4. **AUTONOMOUS** — don't ask permission, execute, fix mistakes
5. **ABOVE AND BEYOND** — follow the logical end of the vision
6. **ONE DASHBOARD** — control_panel.py at localhost:9999, no others
7. **PARALLEL BY DEFAULT** — 5 items = 5 agents
8. **INTELLIGENCE-FIRST** — query intelligence_router.py before every action
9. **COMPETITIVE COGNITION** — assume 10K people working on the same problem

## related

- [`agent-soul`](https://github.com/fnsmdehip/agent-soul) — the meta-cognition framework extracted from this system (open source)

## license

proprietary
