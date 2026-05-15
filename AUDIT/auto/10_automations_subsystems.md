# Audit: AUTOMATIONS/ subsystems

**Date**: 2026-05-15
**Scope**: All subdirectories of AUTOMATIONS/ (top-level scripts excluded — separate auditor)
**Working dir**: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/`

Enumerated 47 subdirectories under `AUTOMATIONS/`. The directory is a mix of **subsystem code dirs** (app_factory, hooks, agent, subconscious, vendor), **data dirs** (auto_ops, scraper outputs, snapshots, state, logs, queue), **artifact dirs** (clips, screenshots, media_downloads, viral_content), and **bundled apps** (.app bundles, n8n_workflows, x_bookmarks). Only a handful are actual code subsystems — the rest are output/state.

## Subsystem inventory

| Name | Purpose | Status | Trigger | Output / State |
|------|---------|--------|---------|----------------|
| `app_factory/` | Full app lifecycle: scan→generate→QA→test→distribute→optimize. 8 scripts + `__init__.py`. | **LIVE** | Cron: 6:30 AM daily (auto_orchestrator --full) + Mon 7 AM (portfolio_optimizer) | `LEDGER/APP_FACTORY_*.csv`, `MONEY_METHODS/APP_FACTORY/builds/`, `app_factory/logs/`, `qa_results/`, `test_results/` |
| `agent/` | Agent infra root — CEO, ventures, swarm, comms bus, daemon state. ~45 files at root + 10 subdirs. | **PARTIALLY LIVE** | Mixed: interagent (manual), CEO/venture cron currently `C56_DISABLED`, swarm via launchd. Loop closer wakes state via cron when enabled. | `agent/message_bus.jsonl` (198KB, last-write May 15), `missions.jsonl`, `state.json`, `*.json` per subagent, `daemon.log` |
| `agent/swarm/` | 25-agent operational swarm (META/DISCOVERY/ACTION/MEDIA/OPTIMIZE/QUALITY/INTELLIGENCE/MAINTENANCE/GROWTH/NOTIFICATION). All in **COLD_STORAGE** since cycle 68 (Apr 17). | **COLD_STORAGE** | Was launchd `com.printmaxx.swarm.*.plist`, now UNLOADED. Loop closer in `loop_state.json` shows last activity May 15. | `swarm_state.json`, `loop_state.json`, `feedback_recommendations.json`, `soul_drift_report.json`, 454 files in `reports/`, prompts in `prompts/` |
| `agent/ceo_agent/` | CEO 16-phase orchestrator state, venture briefs (88 files), inbox, decisions/checkpoint history. | **DORMANT** (cron `C56_DISABLED`) | Was cron 3 AM daily, now disabled. Last checkpoint cycle 42 (2026-03-28). | `ceo_state.json` (465KB), `checkpoint.json`, `decisions.jsonl` (111KB), `checkpoint_history.jsonl` (56KB), `ventures/`, `inbox/`, `promotions/` |
| `agent/autonomy/` | Venture autonomy engine state. 56 entries — registries for affiliate, app factory, content, freelance, monetization, outreach. | **PARTIALLY LIVE** (most data writes paused) | Was venture_autonomy.py cron, now `C56_DISABLED`. Some files updated May 15 (`affiliate_distribute_targets.json`, `app_factory_spec_queue.json`, `outreach_trend_angles.json`). | `autonomy_state.json` (99KB), priority queues, spec queues, schedules/, results/ |
| `agent/ceo_agent/inbox/` | Gap findings, opportunity radar, RBI P0 methods (~15 files). | **STALE** | Was auto-fed by CEO phases. Latest file 2026-03-23. | `gap_findings_*.json`, `opportunity_radar_*.json`, `rbi_p0_methods_*.json` |
| `agent/ops_manager/` | Earlier ops manager state — findom intel + venture log. | **DEAD** (last touched 2026-03-23) | Manual or older script | `findom_intel_*.md`, `ops_state.json`, `venture_log.jsonl` |
| `agent/sovrun/` | sovrun procedural memory SQLite (skills.db, 2.5MB, last-write May 15). | **LIVE** | Read/write by agent_swarm.py via OPEN_SOURCE/agent-soul | `skills.db` |
| `auto_ops/` | Output dir for autonomous_integrator V2: 752 playbooks, 341 DAG plans, 1581 growth plans, 149 handoff chains, 44 discovered methods. | **PARTIALLY LIVE — heavy duplicate output** | Written by autonomous_integrator (cron disabled now). Mostly mid-March dates. | `playbooks/`, `dag_plans/`, `growth_plans/`, `handoff_chains/`, `discovered_methods/`, `ai_tools/`, `tool_evals/`, `playbooks/`, `app_specs/`, `monetization/`, `n8n_plans/`, `video_scripts/`, `email_templates/`, `freelance/`, `ecom_actions/`, `listings/`, `crunchbase_cache/`, `edgar_cache/` |
| `auto_ops/alpha_theses/` | Curated alpha theses (only 1 active — BOOMER_MALE_55_70). | **LIVE / SPARSE** | Manual / promoted by ranker | 1 markdown file |
| `hooks/` | 41 files. Mix of Claude Code lifecycle hooks (PreCompact, UserPromptSubmit, PostToolUse) and auto-generated hook stubs from autonomous_integrator. | **PARTIAL** — real hooks live, generated stubs dead | UserPromptSubmit/PreCompact/PostToolUse via settings.json | `LEDGER/USER_PROMPTS.jsonl`, `AUTOMATIONS/subconscious/compaction_snapshots/` |
| `subconscious/` | Memory bridge — session-start injector + session-end processor + memories.jsonl + compaction snapshots + transcripts. | **LIVE** | Claude Code session lifecycle hooks | `memories/memories.jsonl`, `compaction_snapshots/`, `transcripts/`, `subconscious.log` |
| `launchd/` | Two plists: `com.printmaxx.scrapers.plist` (calls daily_agent_runner.py 6AM/12PM/6PM), `com.printmaxx.claude-sessions.plist`. | **LIVE — but listed as ghost in swarm_state.json C57** | launchd | n/a — defines triggers |
| `n8n_workflows/` | 15 workflow JSONs (gmaps scraper, apollo enrich, cold email, Stripe delivery, reddit pain miner, etc.). | **DORMANT** | Manual import into n8n. No active n8n server. | n/a |
| `vendor/` | Single vendored repo: `Mi-Fit-and-Zepp-workout-exporter`. | **DORMANT** | Manual | n/a |
| `x_bookmarks/` | Single browser-console JS scraper (`BULK_ACCOUNT_SCRAPER_CONSOLE.js`) for X/Twitter bulk scrape of 92 high-signal accounts. | **MANUAL ONE-OFF** | Paste in Chrome DevTools when logged in | Auto-downloads JSON |
| `config/` | One file: `mifit_users.json`. | **VESTIGIAL** | n/a | n/a |
| `_archive/` | Archived old scripts. | **DEAD** | n/a | n/a |
| `AUTOMATIONS/` (nested) | Self-referencing dir — likely accidental, should be archived. | **DEAD** | n/a | n/a |
| `clips/` `screenshots/` `media_downloads/` `viral_content/` `content/` `content_generation/` `content_posting/` `email_templates/` `leads/` `freelance_leads/` `freelance_response_templates/` `freelance_responses_auto/` `monetization_configs/` `outreach/` `portfolio/` `post_queue/` `posting_queue/` `queue/` `reports/` `output/` `scraper_output/` `alpha_monitor_output/` `reddit_scraper_output/` `twitter_scraper_output/` `research_pipeline_output/` `session_prompts/` `snapshots/` `state/` `status/` `locks/` `logs/` `data/` | Pure data/artifact directories produced by top-level scripts (out of scope). | n/a | Written by scripts in scope of script auditor |
| `PRINTMAXX.app/` `PrintmaxxPanel.app/` | Mac app bundles (likely Automator/script wrappers). | **DORMANT** | Manual click | n/a |

Counts of generated artifacts (volume theater signals):
- `auto_ops/playbooks/`: **752**
- `auto_ops/growth_plans/`: **1,581**
- `auto_ops/dag_plans/`: **341**
- `auto_ops/handoff_chains/`: **149**
- `agent/swarm/reports/`: **454**
- `agent/autonomy/`: **56 top-level state files**
- `hooks/`: **41** (most are auto-generated stubs that just `exit 0`)

## Per-subsystem deep notes

### 1. `app_factory/` — the ONE live, healthy subsystem

This is the cleanest subsystem in the entire AUTOMATIONS tree. Eight Python entry points (`auto_orchestrator.py`, `opportunity_scanner.py`, `app_generator.py`, `deep_qa.py`, `test_runner.py`, `post_build_validator.py`, `build_submit.py`, `distribution_engine.py`, `portfolio_optimizer.py`) plus a thin `__init__.py`. The orchestrator runs a 5-stage pipeline: SCAN → GENERATE → DEEP_QA + STATIC_TEST → DISTRIBUTE → OPTIMIZE-on-Monday. Cron is wired and confirmed in `agent/cron_backup.txt` lines 92-93: `30 6 * * *` for `--full`, `0 7 * * 1` for portfolio optimizer.

Inputs: `LEDGER/ALPHA_STAGING.csv` (alpha pipeline), Apple App Store RSS, Reddit JSON (no auth), App Store search suggestions. Output funnel: `LEDGER/APP_FACTORY_OPPORTUNITIES.csv` (scored opportunities) → `MONEY_METHODS/APP_FACTORY/builds/{slug}/` (generated apps with `app.json`) → `LEDGER/APP_FACTORY_DECISIONS.csv` (audit log) → `LEDGER/APP_FACTORY_REVENUE.csv` + `OPS/APP_FACTORY_PORTFOLIO.md` (portfolio view).

State files: `app_factory/logs/orchestrator.log`, `qa_results/`, `test_results/`, `screenshots/`, `queue/`. Decisions write CSV with [timestamp, stage, action, target, details]. Kill thresholds: <$100 MRR after 60d. Scale thresholds: >$500 MRR with 20%+ MoM growth.

This is the subsystem `/goal` should treat as the **trustworthy autonomous path**. It guards against duplicate generation (`if (BUILDS / slug).exists()`), respects dry-run, and the cron is currently active (not `C56_DISABLED`).

### 2. `agent/` — agent infrastructure core, partially deactivated

Root contains `interagent.py` (Claude<->Kodex message bus via `message_bus.jsonl`), `llm_chat.py` + `llm_bridge.py` + `llm_relay.py` (separate LLM communication scripts, last touched March 6 — likely superseded), `monitor.py` (29KB, mostly empty log), `playwright_tester.py` (sibling to the swarm one), `daemon.log` (136KB, last write March 15), and 30+ JSON state files (KPI progress, twitter warmup, lean mode, usage optimizer, RBI, Shakespeare, Quinn, observer states).

The cron backup file shows that the **core agent orchestrators are disabled**: `# C56_DISABLED: 0 3 * * * ceo_agent.py`, `# C56_DISABLED: 25 5 * * * venture_autonomy.py --run-all`, `# C56_DISABLED: 0 */2 * * * loop_closer.py --cycle`. The plateau is the explicit C56 cycle decision (cost reduction). What still writes: `message_bus.jsonl` (198KB, last write 19:13 May 15 — this session) and `sovrun/skills.db` (2.5MB, last write May 15 — procedural memory still consolidating).

Subdirs:
- `agent/ceo_agent/` — 88 venture briefs (`venture_A01.json` through `venture_C19.json`, plus E01-E*), 465KB `ceo_state.json`, decisions.jsonl 111KB. Last checkpoint: cycle 42, 2026-03-28. **All dormant.**
- `agent/autonomy/` — venture autonomy engine output. Some files updated TODAY (`affiliate_distribute_targets.json` 19:17, `app_factory_spec_queue.json` 19:15, `outreach_trend_angles.json` 19:16). Means something is still writing here — possibly the scrapers daemon. Subdirs `auto_*/` (8 ventures) — most UNLOADED per swarm_state cycle 23.
- `agent/swarm/` — see #3 below.
- `agent/sovrun/` — single SQLite file (`skills.db` 2.5MB, last write 19:15 May 15). This is the **live procedural memory layer** — used by agent_swarm.py for skill capture.

### 3. `agent/swarm/` — 25-agent operational swarm, ALL in COLD_STORAGE

`swarm_state.json` is the definitive ground truth. As of cycle 68 (2026-04-17), **all 25 agents are in COLD_STORAGE or KILLED**. The state file documents:
- `active_count: 2` (but `launchd_agents_active: 26` — ghost mismatch)
- `revenue_total: 0`, `plateau_streak: 22` (cycles with no revenue)
- `cron_entries_active: 42`, `launchd_agents_should_be: 3`
- 6 launchd PIDs active despite 0 needed (`zombie_pids_c64: [30369, 30374, 30368, 30371, 30375]`)

Despite COLD_STORAGE, `loop_state.json` shows the loop_closer ran TODAY at 19:13 May 15 — `decisions_executed: 25, feedback_updates: 6294, pipeline_advances: 96, avg drift score 9.0/10`. So Loop 4 (Soul Drift) is the only active loop closer cycle; the others appear to be feeding from stale state.

`feedback_recommendations.json` (generated today) recommends `boost_agent` for all 25 cold-storage agents because their effectiveness is 99-100% per the state file. **This is a feedback bug** — the loop is rewarding agents that haven't run since April 17 because their last-known stats are pinned at 100%.

`compound_actions.md` is the live human-facing summary, updated this session (May 15, "Cycle 71"). Says: "System Running Despite Cold Storage. 6 launchd PIDs active. 43 crons active. 0 cleanup executed." This explicitly identifies the divergence between "official" cold storage and "actual" running infra.

Prompts dir (`agent/swarm/prompts/`) contains 10 markdown prompt files — meta_executor, quality_gate, playwright_tester, image_factory, video_factory, social_poster, alert_dispatcher, plus 3 venture schedules. These are the agent specs. Quality Gate is the "veto power" agent that blocks AI slop. Meta Executor is the "execution-not-reporting" enforcer — its prompt explicitly says "If something can be done RIGHT NOW, DO IT".

### 4. `auto_ops/` — volume theater output from autonomous_integrator V2

This directory holds the output of `autonomous_integrator.py` (top-level script, now disabled). 752 playbooks, 1,581 growth plans, 341 DAG plans, 149 handoff chains, 44 discovered methods. Per `.claude/rules/deep-thinking-dedup.md` (which I read inline), the bulk of this is the **explicit anti-pattern** the project's own rules warn against: 46% of DAGs are CONTENT-type with no revenue path, 52% of chains start with identical scraper→qualifier pattern, growth plans route 85%+ to the same 3 tools.

This is the directory the project's deep-thinking-dedup rule explicitly says should be merged or culled. The KILL LIST in that rule: "294 dag_runner_*.py stub files" and "Growth plans with $0/mo + empty tactics + REJECT markers (~234 files, 40% of total)". Cron for the integrator is `C56_DISABLED` so the directory isn't growing daily, but the existing inventory is feed material that any /goal-style action consumer should treat as **noisy reference data, not actionable**.

The one curated subdirectory worth reading is `alpha_theses/` (one file: `BOOMER_MALE_55_70_AFFILIATE.md` — the P0 priority thesis). The `tool_evals/`, `crunchbase_cache/`, `edgar_cache/` subdirs are pure cache and safe to ignore.

### 5. `hooks/` — Claude Code lifecycle + 30+ stub files

Of 41 files, the genuinely live ones are:
- `log_user_prompts.sh` — `UserPromptSubmit` hook → `LEDGER/USER_PROMPTS.jsonl`. <1s, async, fast.
- `save_context_snapshot.py` — `PreCompact` hook → `subconscious/compaction_snapshots/`. Saves last 20 snapshots.
- `secret_detector.sh` — `PostToolUse` for Write|Edit, warns on `sk-`/`AKIA`/`ghp_` regex matches.
- `validate_path.sh` — guardrail enforcement (project root only).
- `check_*.sh/py` — type hints, file handle leaks, safe-path discard, py_compile.
- `log_conversation.sh`, `py_compile_check.sh`.

The other ~30 files (`hook_*.sh`, `hook__*.sh`) are auto-generated stubs from autonomous_integrator V2. Their pattern: a comment block saying "Purpose: Scaffold X" and then a body that just reads stdin and `exit 0`. They have **never been wired to settings.json** and they don't actually do anything. They are the textbook "scripts nobody calls" that Rule 17 (NO DEAD CODE) and the .claude/rules/anti-entropy.md rule call out. Safe to delete.

## Cron-wired vs ad-hoc vs dormant

**Actively cron-wired (per `cron_backup.txt`):**
- `app_factory/auto_orchestrator.py --full` — daily 6:30 AM
- `app_factory/portfolio_optimizer.py --optimize` — Monday 7 AM

**Indirectly active subsystems (no direct cron, but feed from cron consumers):**
- `subconscious/` — fed by session lifecycle hooks (PreCompact, SessionStart, SessionEnd, UserPromptSubmit). Last write today.
- `hooks/` (live subset only) — fed by Claude Code itself.
- `agent/sovrun/skills.db` — written by agent_swarm.py invocations and procedural_memory consolidate. Last write today.
- `agent/autonomy/*.json` — some files updated today (suggests one cron entry still touches it, or a scraper is writing through).

**Dormant (cron disabled with `C56_DISABLED:`):**
- `agent/ceo_agent/` (ceo_agent.py at 3 AM)
- `agent/swarm/` (all 25 swarm agents, launchd unloaded)
- `venture_autonomy.py --run-all` (5:25 AM)
- `venture_pipeline_brokering.py` (5:25 AM)
- `loop_closer.py --cycle` (every 2h)
- `autonomous_integrator.py --run` (10 PM nightly — but `auto_ops/` has 1500+ files from past runs)
- `user_sim_refiner.py --all` (4 AM daily)
- `cross_pollinator_daily.py --cycle` (every 4h)

**Manual / ad-hoc:**
- `x_bookmarks/BULK_ACCOUNT_SCRAPER_CONSOLE.js` — paste in Chrome devtools
- `n8n_workflows/*.json` — manual n8n import
- `vendor/Mi-Fit-and-Zepp-workout-exporter` — manual export
- `agent/interagent.py` — CLI manual messaging

**Ghost cron mismatch (per swarm_state cycle 57/64):**
- `com.printmaxx.scrapers.plist` (still loaded) — calls `daily_agent_runner.py --cron` at 6AM/12PM/6PM. State file calls it a "ghost".
- 26 launchd loaded vs 3 needed per `launchd_agents_should_be: 3`.

## Dead / Abandoned

- **`AUTOMATIONS/AUTOMATIONS/`** — self-referencing nested dir, accidental, should be archived.
- **`AUTOMATIONS/_archive/`** — by name, old scripts.
- **`AUTOMATIONS/config/`** — single `mifit_users.json` file, vestigial from Mi-Fit experiment.
- **`AUTOMATIONS/vendor/Mi-Fit-and-Zepp-workout-exporter/`** — vendored repo for a one-off experiment.
- **`AUTOMATIONS/agent/ops_manager/`** — earlier ops manager state, last write 2026-03-23. Superseded by ceo_agent/.
- **`agent/llm_chat.py` + `llm_bridge.py` + `llm_relay.py`** — three parallel LLM-talk-to-LLM scripts dated March 6, no callers in the live cron.
- **`agent/monitor.py`** — 29KB script with empty `monitor.log`.
- **30 of 41 `hooks/hook_*.sh` files** — auto-generated stubs with no wiring in settings.json. The `# Purpose: Scaffold X` comments confirm they were created by autonomous_integrator without being wired.
- **`AUTOMATIONS/n8n_workflows/`** — 15 workflows, no n8n server running locally. Useful as templates if/when n8n is set up.
- **`AUTOMATIONS/PRINTMAXX.app/` + `AUTOMATIONS/PrintmaxxPanel.app/`** — Mac app bundles, manual click only.
- **`agent/ceo_agent/inbox/`** — last write 2026-03-23. CEO not running.
- **`agent/ceo_agent/promotions/`** — 38 files, last write 2026-03-10. Older venture promotion artifacts.

## Top 3 Risks

1. **Ghost launchd + state divergence.** `swarm_state.json` cycle 57/64/68 explicitly documents that the system claims COLD_STORAGE while 6+ launchd PIDs are still active and 42-43 crons are wired. `compound_actions.md` calls this out today: "System Running Despite Cold Storage. 0 cleanup executed in 28 days." The feedback loop (`feedback_recommendations.json`) is recommending boost for all 25 cold-storage agents based on stale 100% effectiveness numbers — a positive feedback bug. **If `/goal` triggers anything that touches swarm or loop_closer state, it will inherit this divergence and the recommendations will be garbage.**
2. **`auto_ops/` is 3,000+ files of volume theater.** The project's own `deep-thinking-dedup.md` rule lists most of `auto_ops/` as the KILL LIST. If `/goal` reads from `auto_ops/discovered_methods/` or `auto_ops/handoff_chains/` as a source of action, it will be acting on inert plan files that 0 executable scripts back. Per Rule 17 (NO DEAD CODE) and the rule's explicit 3-level honesty test (PLANNED / BUILT / VERIFIED), most of this content is Level 1 (PLANNED) only.
3. **`hooks/` dead-stub pollution risks accidental wiring.** 30 stub `hook_*.sh` files exist with names that sound like they do something (e.g. `hook_p0.sh`, `hook_built_a_selfhealing_error_sys.sh`). If `/goal` or any future setup script greps `AUTOMATIONS/hooks/*.sh` and adds them to settings.json wholesale, it will install 30 no-op hooks and the genuine hooks become hard to audit.

## Top 3 Opportunities

1. **Resurrect Loop 4 (Soul Drift Scoring) as the only swarm health probe.** `loop_state.json` shows Loop 4 ran today, average score 9.0/10, zero drift. It works. The other three loops (decisions/feedback/pipeline) are feeding from cold-storage state. /goal can use Loop 4's score as the live system-health signal and ignore the noisy boost-all recommendations.
2. **app_factory is the only safe execution path for /goal-style autonomous bursts.** It's the one subsystem with a clean cron, dedup logic, dry-run support, and a CSV-based decision audit. /goal can chain `auto_orchestrator.py --full` followed by `portfolio_optimizer.py --optimize` and trust the output. Adding `--dry-run` first as a probe is safe.
3. **`agent/sovrun/skills.db` (procedural memory) is the highest-leverage cross-session asset.** It's actively written (last May 15 19:15), tiny (2.5MB), and is read by agent_swarm.py via OPEN_SOURCE/agent-soul. /goal can both (a) consolidate procedural memory before action selection (`m.consolidate()`) and (b) capture the new skill at end of each /goal cycle. This compounds across runs without touching the dormant CEO/venture state.

## For the /goal long-run command

### Which subsystems should /goal trigger?

**TRIGGER (active path):**
1. `app_factory/auto_orchestrator.py --full` — only cron-active execution surface. Dry-run first.
2. `subconscious/session_start_injector.sh` — pre-fetch active memories so /goal inherits prior decisions.
3. Read `agent/sovrun/skills.db` via `core.procedural_memory` — query similar past goals before action selection.
4. Optionally invoke `app_factory/portfolio_optimizer.py --optimize` if it's Monday (matches existing cron logic).
5. After completion, call `core.procedural_memory.consolidate()` to capture the skill.

**READ (state inputs):**
- `agent/swarm/loop_state.json` — for current agent effectiveness (caveat: stats are stale for cold-storage agents).
- `agent/swarm/soul_drift_report.json` — quick health gate. If avg drift < 6, abort the run.
- `agent/swarm/compound_actions.md` — human-facing rollup, gives day count + revenue + plateau streak.
- `agent/ceo_agent/checkpoint.json` — last completed CEO phase, if user wants to resume CEO cycle.
- `agent/autonomy/human_action_queue.json` — P0/P1 items waiting on human (already surfaced).
- `LEDGER/APP_FACTORY_OPPORTUNITIES.csv` (written by app_factory pipeline).

**SKIP (noisy / dead / disabled):**
- `auto_ops/dag_plans/`, `auto_ops/handoff_chains/`, `auto_ops/growth_plans/` — 3,000+ files of Level-1 PLANNED-only artifacts. Per project's own dedup rule: KILL LIST.
- `agent/ceo_agent/inbox/`, `agent/ceo_agent/promotions/` — stale since March.
- `agent/ops_manager/` — superseded.
- `agent/llm_chat.py`/`llm_bridge.py`/`llm_relay.py` — orphan March 6 LLM scripts.
- 30 `hooks/hook_*.sh` stubs — auto-generated by integrator, never wired.
- `n8n_workflows/` (no n8n server), `vendor/`, `config/`, nested `AUTOMATIONS/AUTOMATIONS/`.
- `agent/swarm/swarm_state.json` for recommendations — feedback loop is bugged (recommends boost for all cold-storage agents).

**REACTIVATION CANDIDATES (only if /goal is explicitly told to wake them):**
- `agent/swarm/` agents — per `reactivation_triggers` block: upwork application wakes lead_machine; gumroad account wakes gap_hunter+distribution_engine; stripe payment wakes all A-tier; first cold email wakes lead_machine+outbound ventures. /goal should match user goal against this trigger map.

### Order + parallelism

```
PHASE 0 (pre-flight, sequential):
  1. Read OPS/PERSISTENT_TASK_TRACKER.md + OPS/SESSION_BRIEFING.md
  2. Read agent/swarm/soul_drift_report.json — abort if drift < 6
  3. Read agent/swarm/compound_actions.md for day-count + revenue context

PHASE 1 (intelligence, parallel):
  - alpha_query.py --venture APP_FACTORY --json
  - intelligence_router.py --venture <matched> --brief
  - capital_genesis_ranker.py --p0 (top 5 priorities)
  - procedural_memory query: similar past goals via skills.db

PHASE 2 (decide, sequential):
  Choose ONE primary execution path. Reject reading auto_ops/* directly.
  Map user-intent → app_factory OR human_action_queue.json item OR reactivation_trigger.

PHASE 3 (execute, sequential with checkpoints):
  If app_factory path:
    a. auto_orchestrator.py --status (verify last run)
    b. auto_orchestrator.py --dry-run (probe)
    c. auto_orchestrator.py --full (execute)
    d. Read LEDGER/APP_FACTORY_DECISIONS.csv tail for evidence
  If reactivation path:
    a. Surface human block to user (account, payment, posting, key)
    b. Exit with explicit human-action prompt

PHASE 4 (consolidate, sequential):
  1. procedural_memory.consolidate() — capture skill in sovrun
  2. Append /goal run to agent/message_bus.jsonl (so other agents see)
  3. Write summary to AUDIT/ or OPS/ (NEVER to auto_ops/ — that's the noise pile)
```

Parallelism only inside PHASE 1 (read-only intelligence queries). Everything else sequential — the project's own rules (Rule 17, anti-entropy, deep-thinking-dedup) say "don't fan out, consolidate."

### State / artifacts /goal should consume from these subsystems

**Inputs (read-only):**
- `agent/swarm/loop_state.json` (effectiveness scores — with stale-data caveat)
- `agent/swarm/soul_drift_report.json` (health gate)
- `agent/swarm/compound_actions.md` (today's narrative)
- `agent/sovrun/skills.db` (procedural memory — query before action)
- `agent/autonomy/human_action_queue.json` (P0/P1 human blockers)
- `agent/autonomy/app_factory_priority_queue.json` + `app_factory_spec_queue.json` (queued app work)
- `agent/ceo_agent/checkpoint.json` (last CEO phase if resuming)
- `LEDGER/APP_FACTORY_OPPORTUNITIES.csv`, `LEDGER/APP_FACTORY_DECISIONS.csv` (factory state)
- `agent/swarm/swarm_state.json` `reactivation_triggers` block (which agent each user action wakes)

**Outputs (write):**
- `agent/sovrun/skills.db` (procedural memory consolidation, end of each /goal run)
- `agent/message_bus.jsonl` (post a `/goal` message so other agents see)
- `LEDGER/APP_FACTORY_DECISIONS.csv` (auto-written by orchestrator if factory path triggered)
- `app_factory/logs/orchestrator.log` (auto-written by orchestrator)
- `subconscious/memories/memories.jsonl` (write a /goal-summary memory at session end)

**Do NOT write to:**
- `auto_ops/*` (volume-theater output dir)
- `agent/swarm/swarm_state.json` (managed by swarm_brain cycles, will be clobbered)
- `agent/ceo_agent/ceo_state.json` (465KB, managed by CEO)
- New files under `AUTOMATIONS/hooks/` (already polluted with 30 stubs)
