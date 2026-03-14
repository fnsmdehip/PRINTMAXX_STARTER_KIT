# PRINTMAXX Restructure V2 — Intelligence Brief

Source: PRINTMAXX_RESTRUCTURE_V2.xlsx (analyzed 2026-03-13)
Based on: metaswarm, Swan AI, ccswarm, OpenClaw, wshobson/agents, Claude native swarms, IH $30K/mo patterns

## Gap Analysis Summary

| Source | Key Pattern | PRINTMAXX Gap | Priority |
|--------|------------|---------------|----------|
| metaswarm | Cross-model adversarial review (writer != reviewer, 127 PRs/weekend) | evaluator_agent uses same model family to review itself | P0 |
| metaswarm external-tools | Cheapest-available model routing + $2/task budget caps | All agents use Claude, no budget caps | P1 |
| Claude Code Native Swarms | TaskCreate dependency graph, parallel reviewer pools | Cron scheduling is time-based not dependency-based | P1 |
| Swan AI | $1M ARR in 9 weeks via LinkedIn movement-first GTM, 3 agents (Shakespeare/Observer/Quinn) | No public content layer, channel-first not movement-first | P0 GTM |
| ccswarm / Gastown | Git worktree isolation for parallel agents | File-level race conditions between agents | P2 |
| wshobson/agents | 146 skills across 23 categories, Agent Skills marketplace | Monolithic scripts, not packaged as portable skills | P2 Revenue |
| OpenClaw | 250K GitHub stars via build-in-public, community sprints | Entirely private, zero public presence | P1 Distribution |
| IH $30K/mo | Always-on distribution channel from Day 1 | Twitter warmup blocking distribution | P0 GTM |
| BotBorne 2026 | 340% avg revenue increase, value-based pricing | EAS pilots underpriced vs value delivered | P1 Pricing |
| AgentHub (Karpathy) | Agent-native version control, DAG-based message board | message_bus.jsonl is flat append-only | P2 |

## Tickets Created

| ID | P | Title | Status |
|----|---|-------|--------|
| T013 | P0 | Cross-Model Adversarial Review | IN PROGRESS |
| T014 | P0 | BEADS-Style Blocking State Gates | IN PROGRESS |
| T015 | P0 | Swan AI LinkedIn Movement Engine | IN PROGRESS |
| T016 | P1 | Native Task Dependency Graph | IN PROGRESS |
| T017 | P1 | Git Worktree Isolation | IN PROGRESS |
| T018 | P1 | Agent Skills Packaging | IN PROGRESS |
| T019 | P1 | Build-in-Public Distribution | PARTIAL — directories created, warmup advanced |
| T020 | P1 | Observer Agent + Inbound Lead Intel | IN PROGRESS (part of T015) |
| T021 | P2 | Value-Based Pricing Framework | PENDING |
| T022 | P2 | Always-On Distribution | DONE — warmup advanced to FULL_OPS Day 22 |
| T023 | P2 | Parallel Challenger Review | IN PROGRESS |

## Key Architectural Changes

1. **SOUL.md**: Created at AUTOMATIONS/SOUL.md — behavioral identity for all agents
2. **Blocking Gates**: PENDING→IMPLEMENTING→REVIEWING→APPROVED pipeline quality control
3. **Task Graph**: DAG-based dependency chains replacing time-based cron for pipeline agents
4. **Cross-Model Review**: Writer model != reviewer model, budget circuit-breakers
5. **Movement-First GTM**: Shakespeare (content) → Observer (lead intel) → Quinn (warm outreach)
6. **Skills Marketplace**: 5 PRINTMAXX skills packaged for agentskills.io
7. **Worktree Isolation**: Git worktrees for parallel agent file access
