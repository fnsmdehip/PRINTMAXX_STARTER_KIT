# Audit: Operations directories
**Date**: 2026-05-15
**Scope**: 06_OPERATIONS/, OPS/

## Inventory

### 06_OPERATIONS/ (numbered legacy, frozen)
- Root size: 1 file (`SESSION_HANDOFF.md`, Jan 27)
- 7 subdirs: `checklists/` (empty), `growth/` (25 .md files Jan 23 - Feb 1), `gtm/` (3 files Feb 2), `research/` (3 files Jan-Feb), `setup/` (6 files + archive, latest Feb 12), `trend_intel/` (analyses + templates Jan 28 - Feb 2)
- Total files: ~50 markdown files
- Latest modification anywhere in tree: **Feb 12, 2026** (`setup/ULTIMATE_STACK_GUIDE.md`)
- Nothing modified in last 90 days
- Content type: static playbooks, algorithm research (Twitter/IG/TikTok/Pinterest/LinkedIn), GTM plans, growth tactics, infrastructure stack comparisons, copy psychology references
- All files are static reference material. No agent reads or writes here.

### OPS/ (live operational root)
- Root: ~1,097 entries (35 subdirs + hundreds of root-level .md/.json files)
- Heavily active. Files modified TODAY (May 15: `SESSION_BRIEFING.md`, `_state/session_briefing_state.json`)
- Key auto-generated outputs (all consumed by agents or session start hook):
  - `SESSION_BRIEFING.md` — auto-injected per warm-start hook (memory note); last refreshed 2026-05-15 19:13
  - `HEARTBEAT.md` — system pulse (May 8 last)
  - `ACTIONABLE_QUEUE.md` — actionable_aggregator output, 95 dedup items, last May 6
  - `CAPITAL_GENESIS_PRIORITY_STACK.md` — 9,441 methods ranked, last May 6
  - `ALPHA_BACKLOG_REPORT.md` — backlog scan, 409 matches, last May 6
  - `APP_FACTORY_ALPHA_COMMAND_CENTER.md` — app spec queue, last May 6
  - `DEPLOYMENT_URLS.md` — 76/136 sites live, last May 5
  - `GUARDIAN_IMPROVEMENT_2026_05_*.md` — daily guardian reports through May 9
  - `_state/session_briefing_state.json` — session start state cursor
- 14 JSON state/policy files at root (WORKFLOW_WIRING_REGISTRY, NODE_ROLE, INTELLIGENCE_CATALOG, USER_VOICE_MODEL, etc.)
- 13 venture-specific monetization briefs (`VENTURE_ALPHA*_monetization.md`)
- Key subdirs:
  - `_state/` — runtime state JSONs (session_briefing_state.json current)
  - `alpha_research/` — 4 long-form research reports (Mar-Apr)
  - `automation/launchd/` — 7 .plist files for launchd jobs
  - `cognition_audits/` — weekly self-audits (last Mar 16)
  - `discovery/` — discovery crawler outputs (last Mar 8)
  - `production_reports/` — app factory daily JSON+MD (last Apr 4)
  - `projections/` — METHOD_PROJECTIONS.csv (Feb 8, STALE)
  - `reports/` — METHOD_PERFORMANCE_REPORT_*, daily_digest_* (Feb 8, STALE)
  - `scheduled_runs/` — Mar 5 last
  - `archive/` — 21 dirs of archived material
- Reference docs at root: `PERSISTENT_TASK_TRACKER.md` (Apr 17, 83KB), `PRINTMAXX_SYSTEM_MAP.md` (Apr 1, 80KB), `KPI_DASHBOARD.md` (Apr 1, 228KB), `NAV_INDEX.md` (Mar 24, 67KB), `RESOURCE_MANIFEST.md` (Mar 24, 16KB), `INTELLIGENCE_CATALOG.json` (Mar 23, 153KB), `DAILY_TACTICAL_PLAN.md` (Mar 18)

## Live outputs (file, refresh cadence, who consumes it)

| File | Cadence | Producer | Consumer |
|---|---|---|---|
| `OPS/SESSION_BRIEFING.md` | per session start | `session_briefing.py` | warm-start.sh hook injects into every session |
| `OPS/HEARTBEAT.md` | periodic (May 8 last) | `system_health_monitor` / heartbeat script | dashboard, CEO agent context |
| `OPS/ACTIONABLE_QUEUE.md` | daily 7:30 AM cron | `actionable_aggregator.py` | session start, CEO agent, user view |
| `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` | daily 5:30 AM cron | `capital_genesis_ranker.py --rank --report` | CEO agent, venture_autonomy, user |
| `OPS/ALPHA_BACKLOG_REPORT.md` | daily | `alpha_backlog_scanner.py --scan` | autonomous_integrator V2, CEO agent |
| `OPS/APP_FACTORY_ALPHA_COMMAND_CENTER.md` | refresh on demand | `app_factory_command_center.py --refresh` | app factory orchestrator |
| `OPS/GUARDIAN_IMPROVEMENT_*.md` | daily | guardian script (auto-fix loop) | user surface |
| `OPS/DEPLOYMENT_URLS.md` | continuous | app factory build_submit / deploy scripts | user, distribution_engine |
| `OPS/INTELLIGENCE_CATALOG.json` | manual + wire script | `wire_missed_intelligence.py` | `intelligence_router.py`, CEO agent (high_value_summary key) |
| `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` | 5:30 AM cron | `capital_genesis_ranker.py` | priority decisions everywhere |
| `OPS/PERSISTENT_TASK_TRACKER.md` | session updates | manual + session_end hook | every session start (CLAUDE.md says read FIRST) |
| `OPS/PRINTMAXX_SYSTEM_MAP.md` | on architecture change | manual (Rule 12) | system context for agents |
| `OPS/RESOURCE_MANIFEST.md` | on resource discovery (Rule 15) | manual | Capital Genesis, Intelligence Router, CEO Agent |
| `OPS/SEMI_REVIEW_QUEUE.md` + `SEMI_ARCHIVE_*.md` | daily | review queue script | manual review |
| `OPS/DAILY_TACTICAL_PLAN.md` | engagement planner (7 AM) | `daily_engagement_planner.py` | session start (injected by warm-start) |
| `OPS/_state/session_briefing_state.json` | every session | `session_briefing.py` | self (avoid re-injection) |
| `OPS/production_reports/factory_metrics_*.json` + `PRODUCTION_REPORT_*.md` | every app build | app factory orchestrator | portfolio_optimizer |

## 06_OPERATIONS vs OPS — canonical answer

**OPS/ is canonical. 06_OPERATIONS/ is dead/legacy.**

Evidence:
1. Memory says: "OPS/ is heavily used... SESSION_BRIEFING.md, INTELLIGENCE_CATALOG.json, ACTIONABLE_QUEUE.md..." — every key reference in `.claude/CLAUDE.md` and rules files points to `OPS/...`, never to `06_OPERATIONS/...`.
2. Cross-referenced 20+ rules files: zero references to `06_OPERATIONS/`. All references are to `OPS/...`.
3. Freshness: 06_OPERATIONS frozen Feb 12, 2026. OPS/ has TODAY's session_briefing_state.json + SESSION_BRIEFING.md.
4. 06_OPERATIONS content was migrated/superseded — e.g. `06_OPERATIONS/setup/INFRASTRUCTURE_COST_TIERS_2026.md` is reflected in `OPS/COMPLETE_SOCIAL_INFRA_STACK.md` (Apr 17). `06_OPERATIONS/growth/*` algorithm research is superseded by `OPS/GREY_HAT_EDGE_GROWTH_MASTER.md` (269KB, Apr 20).
5. CLAUDE.md Session Start step 1 reads from `OPS/SESSION_BRIEFING.md` + `OPS/PERSISTENT_TASK_TRACKER.md` + `OPS/DAILY_TACTICAL_PLAN.md`. No mention of 06_OPERATIONS anywhere in session protocol.

**Verdict:** 06_OPERATIONS/ is a numbered-tree relic from an earlier directory scheme (`01_STRATEGY/`, `04_CONTENT/`, `09_LEGAL/`, `10_RESEARCH/` still exist). Its content was either migrated to OPS/ or is reference-only static research. Safe to mark "frozen / archive candidate" but do not delete — `04_CONTENT/` paths are still referenced in INTELLIGENCE_CATALOG.json, so other numbered dirs are likely still live; only 06_OPERATIONS is the stale one.

## Stale outputs (should be regenerating but aren't)

| File | Last modified | Expected cadence | Status |
|---|---|---|---|
| `OPS/HEARTBEAT.md` | May 8, 20:00 | should be hourly or per-cron-tick | STALE 7 days |
| `OPS/reports/METHOD_PERFORMANCE_REPORT_*.md` | Feb 8 | daily | DEAD 96 days |
| `OPS/reports/daily_digest_2026-02-09.md` | Feb 8 | daily 6:45 AM (memory note) | DEAD 96 days |
| `OPS/projections/METHOD_PROJECTIONS.csv` | Feb 8 | weekly | DEAD 96 days |
| `OPS/discovery/discovery_*.json` | Mar 8 | daily (method_discovery_crawler 5 AM) | STALE 68 days |
| `OPS/scheduled_runs/run_history.jsonl` | Mar 5 | every cron tick | DEAD 71 days |
| `OPS/cognition_audits/latest_audit.json` | Mar 16 | weekly Sunday 5 AM | STALE 60 days |
| `OPS/production_reports/factory_metrics_*.json` | Apr 4 | daily | STALE 41 days |
| `OPS/SESSION_BRIEFING.md` | May 15 (today) | per session | LIVE |
| `OPS/ACTIONABLE_QUEUE.md` | May 6 | daily 7:30 AM | STALE 9 days |
| `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` | May 6 | daily 5:30 AM | STALE 9 days |
| `OPS/PRINTMAXX_SYSTEM_MAP.md` | Apr 1 | on change (memory says cron-fed daily) | STALE 44 days |
| `OPS/KPI_DASHBOARD.md` | Apr 1 | on change | STALE 44 days |
| `OPS/PERSISTENT_TASK_TRACKER.md` | Apr 17 | every session per CLAUDE.md | STALE 28 days |

**Pattern:** Cron pipeline has been progressively dying. Daily digest dead since Feb 9. Method performance reports dead Feb 9. Capital Genesis last refreshed May 6 (was supposed to be daily) — implies 5:30 AM cron is OFF or failing silently. The CLAUDE.md anti-entropy Rule 20 mandates loop_closer health and the cron watchdog at hourly — these clearly aren't firing or have themselves died. SESSION_BRIEFING.md being today's date is the only convincing signal that the session warm-start hook still runs in-session, but the BACKGROUND cron pipeline is largely dead.

## Dead / Orphan

1. **`06_OPERATIONS/` entire tree** — zero callers/consumers, all content either migrated to OPS/ or pure reference. Archive candidate.
2. **`OPS/reports/`** — daily_digest and METHOD_PERFORMANCE_REPORT files stop at Feb 9. Producer scripts appear to have stopped running.
3. **`OPS/projections/METHOD_PROJECTIONS.csv`** — single file, Feb 8, no update mechanism.
4. **`OPS/discovery/`** — Mar 8 last; method_discovery_crawler 5 AM cron must be dead.
5. **`OPS/scheduled_runs/`** — Mar 5 last; scheduled_runs system inactive.
6. **`OPS/cognition_audits/`** — Mar 16 last, despite Sunday 5 AM cron.
7. **`OPS/_state/app_packager.json`, `carousel_factory.json`, `publish_pack.json`, `qa_auto_approver.json`, `deploy_guard_state.json`, `net_guard_state.json`** — all frozen Mar 3 14:30. These appear to be from an experiment that was abandoned.
8. **`OPS/automation/launchd/`** — 7 plist files frozen Feb 8. Suggests launchd-based scheduling was tried and abandoned in favor of crontab.
9. **`OPS/openclaw/`** — referenced as historical (256-vuln OpenClaw archive); not consumed.
10. **`OPS/BROWSER_CONTROL/`** — Jan 26 dir, almost certainly superseded by 8-level browser fallback in commands-reference.md.

## Top 3 Risks

1. **CRON PIPELINE LARGELY DEAD** — Capital Genesis stack hasn't refreshed in 9 days, ACTIONABLE_QUEUE hasn't updated in 9 days, daily digest dead since Feb 9, METHOD_PERFORMANCE_REPORT dead 96 days, discovery crawler dead 68 days, scheduled_runs dead 71 days. The user's memory says "39 cron entries active" and the anti-entropy rules say loop_closer must show OK — but the OUTPUT artifacts say otherwise. Either crons are silently failing or the agents that consume them have been silently producing stale signals to the CEO agent for weeks. SESSION_BRIEFING is fresh only because the warm-start hook fires it ON SESSION START, not from cron.
2. **STALE STATE FEEDS WRONG DECISIONS** — INTELLIGENCE_CATALOG.json is Mar 23 (53 days). CEO agent reads `high_value_summary` from this catalog to inject intelligence at Phase 3.5. If catalog is stale, CEO is acting on 53-day-old intelligence while system continues to scrape new alpha. The disconnect is invisible because catalog still parses cleanly.
3. **ORPHAN PROLIFERATION** — 1,097 entries in OPS/ root violates the deep-thinking-dedup rule. Many one-shot venture briefs (`VENTURE_ALPHA*_monetization.md`) and dated reports clutter the canonical operations dir. No retention policy. Future audits will hit cognitive limit reading this directory.

## Top 3 Opportunities

1. **Resurrect the daily cron output chain into `/goal` orchestrator** — `/goal` becomes the single command that regenerates all dead artifacts in correct order: heartbeat -> capital genesis rank -> actionable aggregator -> daily digest -> method performance report -> guardian improvement -> session briefing. This bypasses the cron failure mode by user-triggered regeneration.
2. **Move 06_OPERATIONS/ to `archive/` under OPS/** — 06_OPERATIONS is the cleanest case for archival. Move it inside `OPS/archive/06_legacy_operations/` so the consolidation principle is enforced. Memory should be updated.
3. **Add a "freshness gate" to SESSION_BRIEFING** — at session start, scan key OPS/ outputs and flag any artifact older than expected cadence (heartbeat >24h, capital genesis >24h, actionable queue >24h, daily digest >24h). Surface as red flag at top of briefing. This is the inverse of the guardian: instead of fixing things, it makes failures visible.

## For the /goal long-run command

### Should /goal regenerate OPS/ artifacts? Which ones?

Yes. /goal is the orchestrator that closes the dead-cron loop. Specific artifacts /goal MUST regenerate:

**Tier 1 (must regenerate every /goal invocation):**
- `OPS/HEARTBEAT.md` — call the heartbeat-producing script (likely `system_health_monitor.py --quick` or `closed_loop_pipeline.py` for the live counters)
- `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` — `python3 AUTOMATIONS/capital_genesis_ranker.py --rank --report`
- `OPS/ACTIONABLE_QUEUE.md` — `python3 AUTOMATIONS/actionable_aggregator.py`
- `OPS/SESSION_BRIEFING.md` — `python3 AUTOMATIONS/session_briefing.py` (or its session_start hook)
- `OPS/ALPHA_BACKLOG_REPORT.md` — `python3 AUTOMATIONS/alpha_backlog_scanner.py --scan`

**Tier 2 (regenerate when relevant to the goal):**
- `OPS/APP_FACTORY_ALPHA_COMMAND_CENTER.md` — only when app-factory-relevant goal
- `OPS/production_reports/factory_metrics_<date>.json` + `PRODUCTION_REPORT_*.md` — only after an app build
- `OPS/DEPLOYMENT_URLS.md` — only after a deploy
- `OPS/INTELLIGENCE_CATALOG.json` — wire from `wire_missed_intelligence.py` when intel changes
- `OPS/RESOURCE_MANIFEST.md` — when new IP created (per Rule 15)

**Tier 3 (regenerate weekly or on architecture change):**
- `OPS/PRINTMAXX_SYSTEM_MAP.md` — only on agent/cron/architecture changes (Rule 12)
- `OPS/cognition_audits/latest_audit.json` — `competitive_cognition_audit.py` (weekly Sunday)
- `OPS/KPI_DASHBOARD.md` — when revenue/KPI events occur

**Skip (already fresh via session_start hook):**
- `OPS/_state/session_briefing_state.json` — auto-maintained
- `OPS/SEMI_REVIEW_QUEUE.md` — auto-maintained

### Order of regeneration

The order matters because outputs feed each other. Recommended DAG:

```
1. heartbeat / system_health_monitor --quick           (fastest signal, no deps)
                          |
2. scrapers (twitter/reddit/HN) -> ALPHA_STAGING       (only if last scrape >6h)
                          |
3. alpha_auto_processor --process-new                   (drains backlog into ventures)
                          |
4. alpha_backlog_scanner --scan -> ALPHA_BACKLOG_REPORT.md
                          |
5. capital_genesis_ranker --rank --report -> CAPITAL_GENESIS_PRIORITY_STACK.md
                          |   (Rule 16: rescore on new resources)
6. wire_missed_intelligence.py -> INTELLIGENCE_CATALOG.json
                          |
7. intelligence_router rebuild (consumes catalog)
                          |
8. method_discovery_crawler --crawl --score             (only if last >24h)
                          |
9. actionable_aggregator -> ACTIONABLE_QUEUE.md         (consumes priority stack, tracker, swarm reports)
                          |
10. loop_closer --cycle                                  (decisions, feedback, pipeline, soul drift)
                          |
11. daily_engagement_planner -> DAILY_TACTICAL_PLAN.md   (consumes warmup state, alpha)
                          |
12. session_briefing -> SESSION_BRIEFING.md              (consumes ALL above; goes LAST so it reflects fresh state)
                          |
13. (in-goal work) -> goal-specific scripts             (app build / content gen / outbound / etc.)
                          |
14. on completion: revenue check + KPI dashboard + system map sync (if architecture changed)
                          |
15. final-state SESSION_BRIEFING refresh for next session
```

The pivotal anti-pattern to avoid: regenerating `SESSION_BRIEFING.md` early. It must run LAST because it aggregates the freshness of everything else.

For the user's stated need (orchestrating 39 crons + 38 sub-agents): /goal should be the dual-purpose command:
- Without args: run full DAG (this is the "resurrect cron" mode)
- With args (`/goal ship app X` / `/goal post 3 tweets` / `/goal launch venture Y`): scope the DAG to just Tier 1 + goal-specific Tier 2/3 items, then execute the goal.
