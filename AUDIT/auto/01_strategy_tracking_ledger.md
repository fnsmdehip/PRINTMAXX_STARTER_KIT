# Audit: Strategy + Tracking + Ledger + State
**Date**: 2026-05-15
**Scope**: 01_STRATEGY/, 02_TRACKING/, LEDGER/, state/

## Inventory

### 01_STRATEGY/ (10 files, ~280 KB, frozen Jan 27 - Feb 2)
Top-level strategy markdown only. No subdirs. No scripts.
- `CAPITAL_GENESIS_UNIFIED_PLAN.md` (Jan 27) - master $0 to $1M plan
- `CAPITAL_GENESIS_REPRIORITIZED_EXECUTION.md` (Jan 28) - 42KB exec plan
- `CAPITAL_GENESIS_DASHBOARD.md` (Jan 27)
- `CAPITAL_GENESIS_FASTEST_PATH.md` (Jan 27) - first-dollar hierarchy
- `CAPITAL_GENESIS_HUMAN_TASKS.md` (Jan 27)
- `COHERENCE_AUDIT_2026-01-28.md` (Jan 27)
- `HEDGE_FUND_INTELLIGENCE_REPORT.md` (Jan 27)
- `METHOD_STACKING_PLAYBOOK.md` (Jan 27)
- `PRINTMAXX_STRATEGIC_SYNTHESIS_FEB_2026.md` (Feb 2) - most recent; declares $0 revenue, 5 recommendations
- `ULTRATHINK_CAPITAL_STACKS.md` (Jan 27)

### 02_TRACKING/ (7 subdirs, ~2.1 MB)
- `MEGA_SHEET/` - 10 consolidated CSVs + `build_mega_sheet.py` (Feb 2)
- `methods/` - 21 method CSVs (MONEY_METHODS_TRACKER, CROSS_POLLINATION_MATRIX, ECOM_ARB, etc.) frozen Feb 2
- `financials/` - REVENUE_TRACKER (all $0 examples + 1 paper trade), EXPENSE_TRACKER, P&L, FINANCIAL_DASHBOARD.md (last update Feb 2), budgets/projections/unit_economics subdirs (Jan 20)
- `alpha/` - 3 CSVs frozen Feb 2 (ALPHA_STAGING here is stale snapshot, NOT live one)
- `metrics/` - FUNNEL_METRICS.csv (Jan 19), MEGA_RALPH_TRACKER.csv (Feb 2)
- `content/`, `niches/` - empty directories

### LEDGER/ (440+ entries, ~290 MB total, deeply layered)
- **Hot (May 6 - May 15)**: `ALPHA_STAGING.csv` (9.4 MB, live), `USER_PROMPTS.jsonl` (53.5 MB, live - hooks pipe every prompt), `DECISIONS.csv`, `CAPITAL_GENESIS_RANKINGS.csv` (1.9 MB, 9,374 rows), `GOV_OPPORTUNITIES.csv` (953 KB), `OPPORTUNITY_RADAR.csv`, `alpha_index.db` (17.7 MB SQLite FTS5)
- **Warm (Apr)**: COMPETITIVE_INTEL.csv, AUTO_OPS_TRACKER.csv, COMMUNITY_INTEL.csv, COMPETITOR_CHANGES.csv, AI_VIDEO_CONTENT_TRACKER.csv, METHOD_DISCOVERY_LOG.csv (Apr 20)
- **Cold (Feb-Mar)**: BRAIN_LOG.jsonl (Mar 23), BRAIN_STATE.json (Mar 23, stuck), CONVERSATION_HISTORY.jsonl (Mar 15), ~30 compliance_scan_*.json files, ~140 .csv.backup_*.gz from Mar 20 mass backup
- **Frozen (Jan)**: ~30 .md files (STATUS_BOARD, DAILY_CHECKLIST, AGENT_SWARM_DEPLOYMENT, ALPHA_AUDIT, GTM_REVENUE_INTELLIGENCE etc.)
- **Subdirs**: `_archived_cleanup_20260401/`, `_janitor_backup_20260405/`, `_salvage/`, `.snapshots/` (30 dated dirs from Feb 9), `archive/`, `ALPHA_INTEL/` (1 file), `APP_OPPORTUNITIES/`, `BACKTESTS/`, `ALPHA_BY_CATEGORY/`, `buffer_imports/`, `CONTENT_OPPORTUNITIES/`, `DAILY_BRIEFINGS/` (1 file from Feb 10), `GROWTH_OPPORTUNITIES/`, `INFOPRODUCT_OPPORTUNITIES/`, `AI_INFLUENCER_OPPORTUNITIES/`
- **Misc**: `failed_integrations.jsonl` (1.25 MB, Apr 5), `integration_runs.jsonl` (Apr 1), `content.db` (Jan 24 SQLite)

### state/ (tiny)
- `orchestration_checkpoint.json` (May 6, 4 KB) - DAG state for the morning intelligence pipeline (scrape_twitter -> scrape_reddit -> scrape_hn -> merge_results -> alpha_processor -> intelligence_router -> capital_genesis_ranker). Last run May 6 ended OK except intelligence_router subcall failed on `--refresh` arg.
- `locks/` (empty since Mar 18)

## Live / Operational (and what triggers each)

| Asset | Triggered by | Cadence | Evidence |
|---|---|---|---|
| `LEDGER/ALPHA_STAGING.csv` | `twitter_alpha_scraper`, `background_reddit_scraper`, `hn_scraper`, `method_discovery_crawler`, `sec_edgar_scanner`, `crunchbase_scanner`, `opportunity_radar`, `sam_gov_monitor` (cron 5:00 AM, fan-in) | hourly+daily | mtime May 15 |
| `LEDGER/CAPITAL_GENESIS_RANKINGS.csv` | `capital_genesis_ranker.py --rank --report` (cron 5:15 AM) | daily | 9,374 rows, mtime May 6 |
| `LEDGER/alpha_index.db` | `sqlite_alpha_index.py --rebuild` (cron 5:10 AM) | daily | FTS5 17.7 MB, mtime May 6 |
| `LEDGER/USER_PROMPTS.jsonl` | UserPromptSubmit hook (`AUTOMATIONS/hooks/log_user_prompts.sh`) | per prompt | 53 MB, mtime May 15 |
| `LEDGER/DECISIONS.csv` | `decision_engine.py --cycle` (cron 5:20 AM) | daily | mtime May 15 |
| `LEDGER/GOV_OPPORTUNITIES.csv` | `gov_tenders_scraper.py` (cron Wed 4 AM) + `sam_gov_monitor.py` | weekly + daily | mtime May 6 |
| `LEDGER/OPPORTUNITY_RADAR.csv` | `opportunity_radar.py --scan` (cron 5 AM) | daily | mtime May 6 |
| `LEDGER/ECOM_ARB_OPPORTUNITIES.csv` | `ecom_arb_engine.py --scan` (cron 5 AM) | daily | mtime May 6 |
| `state/orchestration_checkpoint.json` | morning DAG runner (likely `morning_intelligence_dag.py`) | daily | mtime May 6 |
| `LEDGER/MEGA_SHEET/*.csv` | `build_mega_sheet.py` (cron Sun 4:15 AM via `15 4 * * 0`) | weekly | NOT regenerated since Feb 2 - cron entry exists but BASE path mismatch (script hardcodes `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER` without the `p/` and trailing `ttttt`); cron is silently dead |
| `LEDGER/COMPETITIVE_INTEL.csv` | scrapers + competitor_stalker agent | recent (May 5) | live |
| `LEDGER/AUTO_OPS_TRACKER.csv` | `alpha_to_ops.py` | recent (Apr 6) | warm |

Confirmed cron count: ~43 active lines (not 39 as user message stated).

## Dead / Orphan / Abandoned (mtime + reason)

| Item | mtime | Reason |
|---|---|---|
| All of `01_STRATEGY/` | Jan 27 - Feb 2 | Reference docs only. Zero scripts in AUTOMATIONS reference these files. The Capital Genesis ETHOS is encoded in `intelligence_router.py` / `capital_genesis_ranker.py` / `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md`, but the source `01_STRATEGY/*.md` docs are not re-read. They are human-readable historical artifacts. |
| `02_TRACKING/alpha/ALPHA_STAGING.csv` | Feb 2 | Stale snapshot - the LIVE one is `LEDGER/ALPHA_STAGING.csv` (May 15). Confused duplicate. |
| `02_TRACKING/methods/*.csv` (21 files) | Feb 2 | Frozen mirrors of MEGA_SHEET tabs. Not consumed by any active cron. |
| `02_TRACKING/financials/REVENUE_TRACKER.csv` | Feb 2 | 5 example $0 rows + 1 paper trade. Never updated (matches user's $0 revenue reality). |
| `02_TRACKING/financials/FINANCIAL_DASHBOARD.md` | Feb 2 | Hardcoded snapshot. Not auto-regenerated. |
| `02_TRACKING/MEGA_SHEET/*` | Feb 2 | Cron exists but BROKEN (path mismatch in `build_mega_sheet.py` line 12 - hardcodes `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER`, missing `p/` prefix and `ttttt` suffix). Dead cron, never errors visibly. |
| `LEDGER/BRAIN_STATE.json`, `BRAIN_LOG.jsonl` | Mar 23 | "Brain" subsystem stopped writing. `last_heal: 2026-03-23`. Dead. |
| `LEDGER/CONVERSATION_HISTORY.jsonl` | Mar 15 | `conversation_logger.py` stopped running. Cron entry not found. Dead. |
| `LEDGER/compliance_scan_2026_*.json` (~30 files) | Feb 13 - Mar 14 | Compliance scanner stopped. Dead. |
| `LEDGER/DAILY_BRIEFINGS/` | Feb 10 (1 file only) | `daily_digest.py` writes elsewhere now (`OPS/`). Dead folder. |
| `LEDGER/.snapshots/` (30 dirs) | Feb 8-9 | Pre-migration backups. Safe to archive. |
| `LEDGER/_archived_cleanup_20260401/`, `_janitor_backup_20260405/`, `_salvage/` | Apr 1-5 | Already-archived junk. |
| ~140 `LEDGER/*.csv.backup_20260320_*.gz` | Mar 20 | One-time mass backup. Safe to delete after verification. |
| `LEDGER/failed_integrations.jsonl` | Apr 5 | 1.25 MB log of failures from the integrator V2 catastrophe (294 stub DAGs). Historical only. |
| `LEDGER/AUTOMATION_RESULTS.csv` | Feb 9 | One row only. Schema unused. Dead. |
| `LEDGER/content.db` | Jan 24 | Old SQLite, unreferenced. |
| `state/locks/` | Mar 18 | Empty since Mar 18. Locks rotated. |
| `LEDGER/CONTROL_CENTER_*`, `EXECUTION_PROGRESS`, `STATUS_BOARD`, `MASTER_TASKS`, `DAILY_CHECKLIST`, `BRANDED_ACCOUNTS`, `QUICK_START_SETUP`, etc. | Jan 19-21 | Initial-bootstrap markdown files. Not consumed. Dead. |

## Duplication or Overlap (with which siblings)

1. **ALPHA_STAGING.csv exists in THREE places**:
   - `LEDGER/ALPHA_STAGING.csv` (LIVE, May 15, 9.4 MB) - canonical
   - `02_TRACKING/alpha/ALPHA_STAGING.csv` (Feb 2, 612 KB) - stale snapshot
   - `LEDGER/MEGA_SHEET/TAB3_ALPHA_MASTER.csv` (Feb 2) - frozen consolidation
   Plus 8+ historical backups in `LEDGER/archive/` and `_archived_cleanup_*/`.

2. **MONEY_METHODS_TRACKER**:
   - `02_TRACKING/methods/MONEY_METHODS_TRACKER.csv` (Feb 2)
   - `LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv` (Feb 2)
   Both stale. Active scoring lives in `LEDGER/CAPITAL_GENESIS_RANKINGS.csv`.

3. **Strategy docs**:
   - `01_STRATEGY/CAPITAL_GENESIS_UNIFIED_PLAN.md` (Jan 27)
   - `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` (regenerated daily by ranker)
   Stack is live, plan is reference. Plan should remain read-only; not actual overlap, but two sources of "what to do."

4. **Financial tracking**:
   - `02_TRACKING/financials/REVENUE_TRACKER.csv` (Feb 2, examples only)
   - `FINANCIALS/revenue_pipeline.json` (referenced in anti-entropy rule, lives outside this scope)
   The `02_TRACKING/financials/` tree never wired into active automation.

5. **Cross-pollination**:
   - `02_TRACKING/methods/CROSS_POLLINATION_MATRIX.csv` (Feb 2)
   - `LEDGER/CROSS_POLLINATION_MATRIX.csv` (Mar 20)
   - `LEDGER/CROSS_POLLINATION_STACKS_FEB_2026.json` (Feb 8)
   Three sources. Live cross-pollinator scripts (`cross_pollinator_v2.py` cron 5:50 AM) write to LEDGER root.

6. **DECISIONS**:
   - `LEDGER/DECISIONS.csv` (LIVE, May 15) - decision_engine output
   - `LEDGER/DECISION_REVIEWS.jsonl` (Mar 13) - dead
   - `AUTOMATIONS/agent/ceo_agent/decisions.jsonl` (per CLAUDE.md, not in scope)

## Top 3 Risks

1. **MEGA_SHEET cron is silently dead.** `LEDGER/MEGA_SHEET/build_mega_sheet.py` hardcodes a path that doesn't exist (`/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER`, missing `p/` and `ttttt` suffix - this project moved). The cron `15 4 * * 0 ... build_mega_sheet.py` fires weekly but produces nothing useful. Last regen Feb 2. Anything downstream expecting fresh MEGA_SHEET data (Google Sheets imports for human review) has been getting Feb 2 data for 3+ months. This is exactly the silent failure mode anti-entropy Rule 17 was meant to prevent.

2. **02_TRACKING is a shadow database.** It looks active (tidy structure, README, schema docs) but nothing writes to it. Any agent (or human) that looks at `MONEY_METHODS_TRACKER.csv`, `REVENUE_TRACKER.csv`, `FINANCIAL_DASHBOARD.md`, `EXPENSE_TRACKER.csv` gets Feb 2 data presented as if current. The Feb 2 strategic synthesis already revealed $0 revenue; nothing has updated this since. Risk: a /goal slash command that reads "money method status" from 02_TRACKING will base decisions on Feb 2 reality.

3. **LEDGER is unbounded and bursting.** 290 MB, 440+ root entries, 30 .snapshots/ subdirs, 140+ .gz backups, dozens of one-off compliance scans, dead jsonl files (BRAIN, CONVERSATION_HISTORY, DECISION_REVIEWS). Every read from `intelligence_router` or `alpha_query` walks this tree. The hot files (~12 of them) live alongside ~400 dead files. SQLite FTS index covers alpha but not metadata. Cognitive load + I/O cost grows monotonically. No cleanup cron exists (only the one-shot `_archived_cleanup_20260401/`).

## Top 3 Opportunities

1. **Promote LEDGER hot-set to canonical and demote everything else.** The actually-live LEDGER files (12-15 of them) drive the entire pipeline. A short manifest at `LEDGER/_MANIFEST.md` listing which files are live (with last-writer cron) + an `archive_old.py` that moves anything >60 days untouched into a structured archive would prevent the agentic system from confusing stale snapshots with live data.

2. **Auto-regenerate `02_TRACKING/financials/FINANCIAL_DASHBOARD.md` and `02_TRACKING/methods/MONEY_METHODS_TRACKER.csv` from LIVE sources.** A 60-line script reading `LEDGER/CAPITAL_GENESIS_RANKINGS.csv` + `FINANCIALS/revenue_pipeline.json` could regen MONEY_METHODS_TRACKER nightly. Same for FINANCIAL_DASHBOARD from real revenue + expense data. Either fix it or delete 02_TRACKING entirely.

3. **Fix MEGA_SHEET path bug and rewire build cron** OR delete it. If MEGA_SHEET is meant to be a Google Sheets export target, one path fix turns a dead cron into a weekly snapshot for human reviewing. If it isn't actually used, the entire `02_TRACKING/MEGA_SHEET/` dir + cron line can go.

## For the /goal long-run command

- **Should /goal touch this area? (yes/no/maybe + reason)**
  - **YES for LEDGER hot-set** - `/goal` MUST query the live LEDGER (CAPITAL_GENESIS_RANKINGS.csv for priorities, ALPHA_STAGING.csv for new signal, DECISIONS.csv for what's been chosen, USER_PROMPTS.jsonl for thread continuity, alpha_index.db for FTS search across 15K entries). This is the system's actual brain.
  - **NO for `01_STRATEGY/`** - These are frozen reference docs. The live equivalent is `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` (regenerated daily). Reading 01_STRATEGY adds 280 KB of stale context for zero decision-relevant gain.
  - **NO for `02_TRACKING/`** - Entirely stale. Either fix it (Opportunity #2) or skip it. Reading it gives Feb 2 numbers.
  - **MAYBE for `state/orchestration_checkpoint.json`** - Useful for `/goal` to know what the morning DAG accomplished or where it broke (the May 6 run shows `intelligence_router --refresh` arg error - that's a fixable bug `/goal` could surface).

- **If yes, which specific scripts/actions should /goal invoke?**
  - `python3 AUTOMATIONS/capital_genesis_ranker.py --rank --top 10` -> read priority stack
  - `python3 AUTOMATIONS/alpha_query.py --venture <type> --json` -> live alpha for current focus
  - SQLite query against `LEDGER/alpha_index.db` -> FTS search for specific topics
  - Read `LEDGER/DECISIONS.csv` -> what's PENDING + needs execution (note 30+ PENDING rows since Mar - decisions are being recorded but not closed)
  - Read `state/orchestration_checkpoint.json` -> last DAG status, flag failed steps
  - Tail `LEDGER/USER_PROMPTS.jsonl` -> recent user intent for context
  - Read `LEDGER/AUTO_OPS_TRACKER.csv` -> what auto-ops are READY_TO_DEPLOY

- **One-time setup needed first?**
  1. **Fix the broken cron** in `LEDGER/MEGA_SHEET/build_mega_sheet.py` line 12 (hardcoded wrong path). Either repair or delete the cron entry.
  2. **Add a LEDGER manifest** distinguishing live (12 files) from archived (rest). One-shot script, then `/goal` only reads from the manifest's "live" set.
  3. **Decide on 02_TRACKING fate**: either wire it as the human-facing dashboard auto-regenerated from live sources, or delete it from `/goal`'s read set. Currently it's a trap.
  4. **Fix the `intelligence_router --refresh` arg error** the May 6 DAG hit (state/orchestration_checkpoint shows the call failed). It's a one-line fix; `/goal` will hit the same wall.
  5. **Re-run `conversation_logger.py` cron** (currently dead since Mar 15) if `/goal` is meant to read CONVERSATION_HISTORY for context continuity. Otherwise drop the reference.
