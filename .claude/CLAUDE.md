# PRINTMAXX — Autonomous Revenue System

Read `OPS/PERSISTENT_TASK_TRACKER.md` FIRST every session. Read `AUTOMATIONS/SOUL.md` for behavioral directives.

## Session Start (10 min max)
1. Read `OPS/SESSION_BRIEFING.md` + `OPS/PERSISTENT_TASK_TRACKER.md` + `OPS/DAILY_TACTICAL_PLAN.md`
2. `python3 AUTOMATIONS/decision_engine.py --cycle`
3. Deploy anything deployable. Check `OPS/ACTIONABLE_QUEUE.md`
4. For architecture/system analysis/naming: read `OPS/PRINTMAXX_SYSTEM_MAP.md` FIRST — canonical live architecture with L0-L6 hierarchy, data flow, agent topology, cron schedule, state files.

## Reference (read on demand, NOT every session)
| Need | File |
|------|------|
| Find a file | `OPS/NAV_INDEX.md` |
| **System map** | **`OPS/PRINTMAXX_SYSTEM_MAP.md`** — CANONICAL architecture. READ FIRST for system context. UPDATE same-session on ANY agent/cron/architecture/data-flow change. |
| **ALL resources/IP/playbooks** | **`OPS/RESOURCE_MANIFEST.md`** — COMPLETE index of 200+ resources: playbooks, products, guides, templates, research. READ BEFORE creating anything new (DEDUP). READ BEFORE executing any venture (load relevant playbooks). Capital Genesis, Intelligence Router, CEO Agent MUST consult this. |
| Status | `OPS/CURRENT_STATUS.md` |
| Commands | `.claude/rules/commands-reference.md` |
| Agent infra | `.claude/rules/agent-infrastructure.md` |
| File locations | `.claude/rules/file-locations.md` |
| Strategy | `.claude/rules/strategic-ethos.md` |
| Quality pipeline | `.claude/rules/auto-quality.md` |
| Ralph/Memory | `.claude/rules/ralph-and-memory.md` |
| Copy style | `.claude/reference/copy-style.md` (load on demand, NOT every message) |
| Guardrails | `.claude/rules/guardrails.md` |
| Security | `.claude/rules/security.md` + `.claude/reference/external-code-security.md` |
| Alpha review | `.claude/reference/alpha-review.md` (load on demand) |
| **Auto-integration** | **`.claude/rules/auto-integration.md`** — pipeline must self-feed, no human prompting for integration |
| **E2E Verification** | **`.claude/rules/end-to-end-verification.md`** — NEVER claim "done" without verifying actual output artifacts |
| **Deep Thinking** | **`.claude/rules/deep-thinking-dedup.md`** — dedup before creating, consolidate over duplicate, revenue reality check |
| **Reprocess on Discovery** | **`.claude/rules/reprocess-on-discovery.md`** — MUST rescore Capital Genesis + update KPIs when new resources/playbooks/tools are added |
| Before You | `MONEY_METHODS/BEFORE_YOU/BEFORE_YOU_VENTURE_README.md` |
| Before You codebase | `/Users/macbookpro/Documents/ancestry-research/before-you/` (generator, template, landing, content) |

## Core Rules (ALWAYS active)
1. **SHIP NOW** — Deploy what exists before building new things. $0 revenue at Day 35.
2. **NO ORPHANS** — Every doc has a CONSUMER (agent or human task). No dead-end reports.
3. **NO SLOP** — No AI vocabulary. No em dashes. Copy style in `.claude/rules/copy-style.md`.
4. **AUTONOMOUS** — Don't ask permission. Execute. Fix mistakes. AUTOMATE periodic tasks to cron immediately.
5. **ABOVE AND BEYOND** — Follow the logical end of the vision. Build implicit subtasks. Recursive value chain: SCAN→ANALYZE→DECIDE→CREATE→DISTRIBUTE→COMPOUND→OPTIMIZE.
6. **ONE DASHBOARD** — `AUTOMATIONS/control_panel.py` at localhost:9999. NEVER create new dashboards.
7. **FACTORY MODE** — Pre-build everything. Don't wait for accounts.
8. **NEVER DROP THE BALL** — Track all active systems. Include status after tasks.
9. **MAX SQUEEZE** — Every build session = 3 tweets + 1 thread minimum. Content from everything.
10. **PARALLEL BY DEFAULT** — 5 items = 5 agents. Background agents for >5K token output.
11. **CEO SANITY CHECK** — Am I building or selling? What's the obvious thing? Human blockers surfaced?
12. **ARCHITECTURE-FIRST** — Before analyzing/describing/naming the system, read `OPS/PRINTMAXX_SYSTEM_MAP.md`. On ANY architecture change (agents, cron, scripts, data flow, state files): update system map + task tracker + CLAUDE.md in SAME session. New ventures also update SOUL.md + memory. No stale maps. No orphan ventures.
13. **COMPETITIVE COGNITION** — Assume 10K power users working on the same problem. Find the non-obvious angle. Anti-lazy: am I defaulting to popular or critically analyzing for best? See SOUL.md protocol.
14. **INTELLIGENCE-FIRST** — Query `intelligence_router.py` before every action. 15K+ alpha entries, not default LLM knowledge. Check `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` for daily ranked priorities.
15. **RESOURCE-AWARE** — Before creating playbooks, guides, strategies, or products: check `OPS/RESOURCE_MANIFEST.md`. 200+ existing resources. DEDUP before creating. Load relevant playbook when executing any venture. Every resource is content source material AND potential sellable product.
16. **REPROCESS ON DISCOVERY** — When new resources, methods, playbooks, tools, or IP are discovered or created: (a) re-run `python3 AUTOMATIONS/capital_genesis_ranker.py --rank --report` to rescore ALL methods with new context, (b) update `OPS/KPI_DASHBOARD.md` if new ventures/products affect revenue projections, (c) update `OPS/RESOURCE_MANIFEST.md` with new entries, (d) check if any existing KPI tasks or actionable queue items are affected. New resources change the scoring landscape — a method with no playbook scoring 6.0 might score 7.5 with a playbook. NEVER add resources without reprocessing the scoring pipeline.

## Guardrails (for THIS project only)
When working in this PRINTMAXX project, file ops stay within: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/`
This does NOT restrict other projects. See `.claude/rules/guardrails.md` for details.

## Session End
1. Update `OPS/PERSISTENT_TASK_TRACKER.md` + `OPS/SESSION_LOG.md`
2. Generate content (Rule 9). Surface human blockers with time estimates.
3. If agents/cron/architecture/data-flow changed → update `OPS/PRINTMAXX_SYSTEM_MAP.md` THIS session. No stale maps.
4. If new resources/playbooks/tools/products created or discovered → update `OPS/RESOURCE_MANIFEST.md` AND rerun `python3 AUTOMATIONS/capital_genesis_ranker.py --rank --report` (Rule 16). No stale scores.

## Mindset
> Use every tool. Every shortcut. Every hack. Every legal advantage. Compete like your life depends on it.
> $0 → $1K → $10K → $50K → $200K+ → hedge fund capital management.
