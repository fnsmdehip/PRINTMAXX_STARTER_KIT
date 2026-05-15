# Audit: Root-level loose files
**Date**: 2026-05-15
**Scope**: every FILE (not directory) at project root — `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/`
**Total root files**: 81 (excluding directories)

---

## File-type breakdown (count by extension)

| Ext / Type | Count | Notes |
|---|---|---|
| `.md` | 24 | Handoff docs, status, research — overwhelmingly stale |
| `.xlsx` | 23 | 16 are dated MASTER_OPS snapshots (Feb 17 → Mar 3) — should be archived |
| `.txt` | 5 | AUTO_STATUS_LIVE, PARSED_*, REMAINING_SHEETS — Feb 19 dumps |
| `.rtf` | 5 | Mix of templates, lead CSVs disguised as RTF, prompt templates |
| `.sh` | 4 | `ship.sh`, `printmaxx_cron.sh`, `deploy_all_apps.sh`, `deploy_surge_quick.sh` |
| `.csv` | 4 | comprehensive_results, ecom_arb, NEW_APP_FACTORY_ALPHA, posting_schedule |
| `.json` | 3 | `package.json`, `package-lock.json`, `pyrightconfig.json` |
| `.py` | 2 | `deploy_apps.py`, `update_ledger.py` |
| `.png` | 2 | playwright_test_summary, test_report_printmaxx |
| `.js` | 2 | `PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.js`, `PRINTMAXX_SYSTEM_AUDIT_FEB9_2026.js` (docx-generators) |
| `.docx` | 2 | Output artifacts of the .js generators |
| `.log` | 1 | `firebase-debug.log` — 14 MB, last touched Mar 25 |
| `.env` | 1 | Live secrets (READ-ONLY for this audit) |
| `.gitignore` | 1 | Solid — explicitly ignores .env, SECRETS/, *.xlsx, *.png, AUDIT inventory dumps |
| `Makefile` | 1 | Mostly stale; CLAUDE_CODE_SETUP.md explicitly says it was "Replaced with natural language commands" |

---

## Authoritative entry point

**Root `CLAUDE.md` is a 6-line POINTER**, not the real instructions:
> "The real CLAUDE.md lives at `.claude/CLAUDE.md` — that's where Claude Code reads project instructions from."

**Truth:**
- **Claude Code → `.claude/CLAUDE.md`** (canonical, 33 rules, session start/end protocol, all references). System-reminder-injected every session.
- **Codex → `CODEX.md` at root** (operating contract, blast-radius controls, node roles, guardrails, swarm audit commands)
- **Humans / other agents → `START_HERE.md`** (last updated 2026-02-04, points to Capital Genesis quick start)
- **GitHub viewers → `README.md`** (Mar 17, public-facing summary, points back to `.claude/CLAUDE.md`)

`MASTER_DOC/` directory holds 4 archived versions of `PRINTMAXX_MASTER_OPERATING_SYSTEM_v22..v26` (Jan 18-20). v26 filename is the comedy item: `PRINTMAXX_MASTER_OPERATING_SYSTEM_FINAL_LATEST VERSION CHECK THIS ONE BUT ALSO CONIDDER OLDE RAND OTHER VERSION MAY HAVE GOOD ALPHA OR GUIDLIENS TO CONSIDERv26_2026-01-19.md`. Indicates archival lacks discipline — the user knows the system has multiple versions and they "may have good alpha" but never consolidated.

---

## Live config files (still active)

| File | Status | Used by |
|---|---|---|
| `.env` | LIVE — DO NOT print | All AUTOMATIONS scripts, `.gitignore` covers it |
| `.gitignore` | LIVE — good coverage (xlsx/png ignored, secrets/output/cal_ai excluded) | Git |
| `package.json` | LIVE — minimal, only `status` script | Project root workspace tag |
| `package-lock.json` | LIVE (small, 205 bytes) | npm |
| `pyrightconfig.json` | LIVE — targets `AUTOMATIONS`, excludes `LANDING`/`MONEY_METHODS` | Pyright/IDE |
| `requirements.txt` | LIVE — rich/textual/playwright/numpy/pytest, mostly stdlib | `pip install -r` |
| `printmaxx_cron.sh` | LIVE — 31 KB master orchestrator (morning/content/outreach/digest/backup/overnight/weekly/monthly/RBI). 39 cron entries reference this. | crontab |
| `ship.sh` | LIVE — wraps `ship_captain.py --swarm --max-parallel 4` | Codex contract names it as primary runner |
| `Makefile` | PARTIALLY LIVE — `make status` / `make validate` / `make content` / `make queue` referenced in HANDOFF_NEXT_CHAT.md; CLAUDE_CODE_SETUP.md says it was "removed", but the file still exists |
| `deploy_apps.py` | LIKELY STALE — Feb 10, deploys PWAs via Vercel/Surge/Netlify fallback |
| `deploy_all_apps.sh` / `deploy_surge_quick.sh` | LIKELY STALE — Feb 10, paired with deploy_apps.py |
| `update_ledger.py` | LIKELY STALE — Feb 15, one-shot for marking GEO pages published |

---

## Status / handoff docs (the chaos)

| File | Date | Length | Still relevant? | Recommendation |
|---|---|---|---|---|
| `CLAUDE.md` (root) | Mar 6 | 6 lines | YES — pointer | KEEP. Useful redirect. |
| `CODEX.md` | Feb 19 | 225 lines | YES — Codex contract | KEEP. Only doc Codex reads. |
| `README.md` | Mar 17 | 156 lines | YES — public GitHub face | KEEP. |
| `START_HERE.md` | Feb 4 | 333 lines | PARTIAL — "first dollar in 8-12 hours" plan from before warmup/automation took over | Archive to `AUDIT/_archived_handoffs/` |
| `WHATS_BEEN_BUILT.md` | Jan 19 | "50+ files / 20,000+ lines" inventory from one early session | NO — superseded by ALPHA_SCAN_*, INFRA_AUDIT, OPS/RESOURCE_MANIFEST | Archive |
| `HANDOFF_NEXT_CHAT.md` | Jan 21 | 161 lines | NO — pre-warmup, predates 99% of current architecture | Archive |
| `SESSION_HANDOFF.md` | Jan 19 | 10 KB | NO — Jan 19 session deliverables | Archive |
| `CLAUDE_CODE_HANDOFF.md` | Feb 10 | "copy this into Claude Code" prompt | NO — superseded by `.claude/CLAUDE.md` auto-injection | Archive |
| `CLAUDE_CODE_SETUP.md` | Jan 19 | 40 lines | NO — describes refactor that happened months ago | Archive |
| `DAY1_EXECUTION.md` | Jan 19 | Day 1-2 checklist (Decodo/SMSPool/GoLogin signup) | PARTIAL — accounts mostly created | Archive |
| `DISPATCH_HANDOFF_APR24.md` | Apr 24 | 157 lines | PARTIAL — most P0/P1 tasks now stale (ComfyUI, AI Art Venture, scrapers, app spec refinement) | Move to `AUDIT/_archived_handoffs/` once user confirms |
| `DISPATCH_STATUS.md` | Apr 17 | 62 lines | PARTIAL — corrections to Apr 17 dispatch findings, useful as historical record | Archive |
| `INFRA_AUDIT.md` | Apr 17 | 317 lines (per text) | YES — most recent infra snapshot, even if 4 weeks stale | Move to `AUDIT/INFRA_AUDIT_2026-04-17.md` |
| `MOBILE_CONTROL_PLAYBOOK.md` | Apr 17 | 250+ lines | YES — Tailscale/RustDesk/Telegram options, 7 ranked | KEEP at root OR move to `OPS/` |
| `CAPITAL_GENESIS_EXECUTION_SUMMARY.md` | Feb 3 | 20 deliverables checklist | NO — superseded by `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` and live ranker | Archive |
| `SESSION_DELIVERABLES_2026_02_04.md` | Feb 3 | Session-specific | NO | Archive |
| `FOLDER_REORGANIZATION_PLAN.md` | Feb 1 | 21 KB, full reorg blueprint | PARTIAL — was implemented (01_STRATEGY, 02_TRACKING, 03_PLAYBOOKS dirs exist) | Archive — plan was executed |
| `NEW_METHODS_SUMMARY_2026-01-24.md` | Jan 24 | Methods discovered Jan 24 | NO — superseded by method_discovery_crawler + Capital Genesis ranker | Archive |
| `NICHE_CONTENT_RESEARCH_2025_2026.md` | Mar 5 | 36 KB | PARTIAL — research doc, useful reference | Move to `10_RESEARCH/` or `OPS/` |
| `RBI_AND_AUTOMATION_ANALYSIS.md` | Feb 10 | 25 KB | PARTIAL — historical critique that the RBI system was "file-counting based"; RBI has since been replaced by `rbi_loop.py` (Mar 24) | Archive |
| `RESEARCH_NEW_METHODS_2026.md` | Jan 24 | 10 KB | NO — superseded | Archive |
| `README_ADDENDUM_PARALLEL_AGENT_LAUNCH.md` | Jan 18 | Parallel agent launch addendum | NO | Archive |
| `YOUR_MANUAL_TASKS.md` | Jan 21 | FamilyControls API + dev account checklist | PARTIAL — content overlaps with current human blocker tables in `.claude/CLAUDE.md` + memory | Archive once verified |
| `plan.md` | Feb 12 | Intelligent lead qualification plan | NO — likely shipped or abandoned | Archive |
| `AUTO_STATUS_LIVE.txt` | Feb 19 | 67 KB dump of AUTO_STATUS sheet from xlsx | NO — snapshot of one xlsx tab from Feb 19 | Delete or archive |
| `PARSED_COMPACT.txt` | Feb 19 | 406 KB parsed xlsx contents | NO | Delete or archive |
| `PARSED_OUTPUT.txt` | Feb 19 | 252 KB parsed xlsx contents | NO | Delete or archive |
| `REMAINING_SHEETS.txt` | Feb 19 | 55 KB parsed xlsx contents | NO | Delete or archive |

**Net:** of 24 .md files, ~17 are stale handoff docs that should be archived. CLAUDE.md, CODEX.md, README.md, INFRA_AUDIT.md, MOBILE_CONTROL_PLAYBOOK.md, NICHE_CONTENT_RESEARCH (move), and the .gitignore'd config files are the only ones worth keeping at root.

---

## Spreadsheet pile — recommendation

**16 dated copies** of `PRINTMAXX_MASTER_OPS_ENHANCED_2026-{date}.xlsx`:
- Feb 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28
- Mar 01, 02, 03

All ~343 KB, basically identical size. These are **daily auto-generated snapshots** by `AUTOMATIONS/master_ops_enhancer.py` (named in CODEX.md). The latest snapshot is Mar 3 — meaning the enhancer cron was likely killed or paused after Mar 3 (~73 days ago).

**Recommendation:**
1. Keep **only `PRINTMAXX_MASTER_OPS_ENHANCED_2026-03-03.xlsx`** (the last one) at root as the canonical "live enhanced clone" referenced by `master_ops_bridge.py`.
2. Move the other 15 to `AUDIT/_archived_master_ops_snapshots/` (or delete — `.gitignore` already excludes `*.xlsx` so they're not in git).
3. The other 7 xlsx files at root (BRAND_NAMES, FREELANCE_ARB, INFRA_ASSIGNMENTS, INFRA_STACKS, MASTER_OPS, OPS_PLAYBOOK, STRATEGIC_RBI, ZERO_COST_DEPLOYMENT) are all referenced by `scripts/builders/*.py` builders. Keep them — they're each a build target. Total: 7 keep + 1 enhanced = 8 xlsx at root, not 23.

---

## RTFs — disposition

| File | Date | Content sniff | Recommendation |
|---|---|---|---|
| `hyper rat soft engin.rtf` | Apr 9 2025 | "hyper-rational first-principles problem solver" system prompt — explicitly referenced by Rule 28 (DEBUGGER MODE) in `.claude/CLAUDE.md` | KEEP — load-bearing for /debug |
| `landind page prtopmt.rtf` | Apr 17 2025 | "Design a complete landing page for DevMode" prompt template — referenced by HANDOFF_NEXT_CHAT as basis for `OPS/prompts/templates/landing_page_prompt.md` | Archive — already migrated to OPS/prompts/templates/ |
| `app guide.rtf` | Jan 21 | Onboarding screen design spec (back button, progress bar, etc.) | Move to `OPS/prompts/templates/app_design_guide.rtf` |
| `iuhkm.csv.rtf` | Jan 10 | RTF wrapper around a CSV of 33 Twitter accounts with revenue/monetization data (Ben Lang, Zack, Alton Syn, etc.) — looks like one-off scrape result with bad filename | Rename + relocate: move to `LEDGER/ALPHA_INTEL/twitter_revenue_accounts_2026-01-10.csv` (strip RTF wrapper). Filename "iuhkm" looks like keysmash garbage. |
| `money methods and sub category methods to add.rtf` | Jan 22 | Loose ideation notes (relax channels, meme channel, news socials, etc.) | Archive or merge into `LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv` |
| `prtopmt.rtf` (already listed) | n/a | (Listed in task brief but actual file is `landind page prtopmt.rtf` — only one prtopmt rtf) | n/a |
| `engin.rtf` / `guide.rtf` / `add.rtf` (listed in brief) | not present | These were likely shortened names in the brief — actual files are `hyper rat soft engin.rtf`, `app guide.rtf`, and `money methods and sub category methods to add.rtf` | n/a |

**Net:** 1 RTF (hyper rat soft engin) is load-bearing per Rule 28. The other 4 are notes that should be migrated to their proper homes.

---

## Stale CSVs / logs / images

| File | Size | Date | Disposition |
|---|---|---|---|
| `comprehensive_results.csv` | 1.06 MB | Jun 10 2025 | Old scrape result — move to `LEDGER/archive/` |
| `ecom_arb_opportunities.csv` | 623 B | Mar 5 | Tiny, recent — likely live, but should be in `LEDGER/ecom_arb/` |
| `NEW_APP_FACTORY_ALPHA_FEB_2026.csv` | 6.4 KB | Feb 2 | Move to `LEDGER/ALPHA_INTEL/` |
| `posting_schedule.csv` | 6.3 KB | Apr 15 | Looks live — `printmaxx_cron.sh` references it via Makefile target `schedule`. Keep or move to `LEDGER/` |
| `firebase-debug.log` | **14.2 MB** | Mar 25 | Stale Firebase debug log. Delete — `.gitignore` doesn't catch it but it's huge bloat. |
| `playwright_test_summary_20260505.png` | 222 KB | May 5 | Move to `OPS/test_reports/` |
| `test_report_printmaxx.png` | 39 KB | Apr 1 | Move to `OPS/test_reports/` |
| `AUTO_STATUS_LIVE.txt` | 67 KB | Feb 19 | One-shot xlsx dump — delete/archive |
| `PARSED_COMPACT.txt` | 406 KB | Feb 19 | One-shot xlsx parse — delete/archive |
| `PARSED_OUTPUT.txt` | 252 KB | Feb 19 | One-shot xlsx parse — delete/archive |
| `REMAINING_SHEETS.txt` | 55 KB | Feb 19 | One-shot xlsx parse — delete/archive |

---

## .docx / .js pairs — explanation

Two pairs at root:
- `PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.docx` (25 KB) + `PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.js` (33 KB)
- `PRINTMAXX_SYSTEM_AUDIT_FEB9_2026.docx` (29 KB) + `PRINTMAXX_SYSTEM_AUDIT_FEB9_2026.js` (44 KB)

The `.js` files are **Node scripts that GENERATE the `.docx` files** using the `docx` npm library. Each script defines colors, tables, headings, and runs `Packer.toBuffer(doc).then(fs.writeFileSync(...))`. The `.docx` files are their outputs. Both pairs are dated Feb 8 2026.

**Recommendation:**
- Move the `.js` generators to `scripts/doc_generators/` (where `scripts/builders/` lives for xlsx).
- Move the `.docx` outputs to `OPS/reports/` or `AUDIT/_archived_handoffs/` (they're Feb 9 snapshots, ~3 months stale).
- Or, if the doc generators were one-shots and won't be re-run, archive the `.js` files alongside the `.docx`.

---

## Top 3 Risks

1. **Wrong handoff doc guides a session.** Eight different handoff/setup docs live at root (`START_HERE`, `HANDOFF_NEXT_CHAT`, `CLAUDE_CODE_HANDOFF`, `CLAUDE_CODE_SETUP`, `DAY1_EXECUTION`, `DISPATCH_HANDOFF_APR24`, `SESSION_HANDOFF`, `WHATS_BEEN_BUILT`). A new agent — or a future Claude session — could read `HANDOFF_NEXT_CHAT.md` (Jan 21) and execute Jan-era priorities (ralph_tasks, Greg Isenberg monitoring) that no longer exist. The pointer in root `CLAUDE.md` to `.claude/CLAUDE.md` helps, but only Claude Code respects it.
2. **Stale `.xlsx` snapshots get used as truth.** 15 dated MASTER_OPS_ENHANCED files. `master_ops_bridge.py` could (does?) load the wrong one. Codex contract names `PRINTMAXX_MASTER_OPS_ENHANCED_2026-02-17.xlsx` specifically — but the latest is Mar 3 (10 days newer). If the bridge ever falls back to filename pattern match without a "latest" rule, behavior is non-deterministic.
3. **15 MB of dead artifacts inflate every git operation.** `firebase-debug.log` (14 MB) alone, plus 700 KB of PARSED_* dumps and old PNGs, mean every `git status`, every `ls`, every backup tool reads through trash. `.gitignore` keeps git clean, but the working tree is noisy.

---

## Top 3 Opportunities

1. **Single canonical entry point**: keep `CLAUDE.md` (pointer), `CODEX.md`, `README.md` only. Move every other doc to `AUDIT/_archived_handoffs/{date}/`. Future agent confusion drops to near-zero. **Effort: 5 minutes (just `mv` commands).**
2. **Archive 14 of 16 dated xlsx**: keep `PRINTMAXX_MASTER_OPS_ENHANCED_2026-03-03.xlsx` (latest) + symlink or copy to `PRINTMAXX_MASTER_OPS_ENHANCED.xlsx` (canonical name). Move the other 15 to `AUDIT/_archived_master_ops_snapshots/`. Removes 5 MB of duplication. If `master_ops_enhancer.py` cron is reactivated, fix it to write `PRINTMAXX_MASTER_OPS_ENHANCED.xlsx` (no date) + drop dated copy in `AUDIT/_archived_master_ops_snapshots/`.
3. **Migrate the 5 RTFs**:
   - `hyper rat soft engin.rtf` → keep, but also extract to `.claude/rules/debugger-mode.md` for parity with the rule that references it
   - `app guide.rtf` → `OPS/prompts/templates/`
   - `landind page prtopmt.rtf` → already migrated, just delete
   - `iuhkm.csv.rtf` → rename/relocate to `LEDGER/ALPHA_INTEL/twitter_revenue_accounts_2026-01-10.csv` (strip RTF wrapper)
   - `money methods and sub category methods to add.rtf` → merge into MEGA_SHEET TAB1 or delete

Bonus: delete `firebase-debug.log` (14 MB), the 4 PARSED_* / REMAINING / AUTO_STATUS txt dumps (~780 KB), and move the 2 PNG test reports to `OPS/test_reports/`. Root file count drops from 81 → ~25.

---

## For the /goal long-run command

**Should /goal use any root-level config?** YES — but minimal:
- **`.env`** for credentials (Anthropic API key, Stripe, GitHub, Supabase, etc.). Loaded via `python-dotenv` or direct `os.environ` reads.
- **`.claude/CLAUDE.md`** is auto-injected by the harness — /goal inherits it. Don't re-read at the script level.
- **`CODEX.md`** if the goal involves the worker-node split or human-approval gates.
- **`printmaxx_cron.sh`** is the orchestrator — /goal can either (a) call `bash printmaxx_cron.sh status` for a yield snapshot, (b) trigger `morning` / `digest` lanes directly, or (c) pipe through `ship.sh` for parallel swarm execution.
- **`Makefile`** offers shortcut targets (`make status`, `make validate`, `make content`, `make queue`) — /goal can invoke these instead of remembering Python script paths.
- **`requirements.txt`** only if /goal needs to verify deps before a long run.

**Avoid reading**: any of the 17 stale handoff `.md` files, any RTF, any `.docx`, any of the 15 older MASTER_OPS xlsx, the `.txt` parsed dumps, `firebase-debug.log`.

**Should /goal produce status docs to root?** NO. Three reasons:
1. The root is already 81 files of historical artifacts — adding more compounds the problem.
2. `.claude/CLAUDE.md` Rule 2 ("NO ORPHANS") says every doc needs a consumer. Root-level output docs have no consumer; subdirs do.
3. Existing pipelines already have homes:
   - **Audit results** → `AUDIT/auto/` (this report's location — correct pattern)
   - **Session logs** → `OPS/SESSION_LOG.md`
   - **Task tracker** → `OPS/PERSISTENT_TASK_TRACKER.md`
   - **Status snapshots** → `OPS/CURRENT_STATUS.md`, `OPS/HEARTBEAT.md`, `OPS/KPI_DASHBOARD.md`
   - **Ledgers** → `LEDGER/`
   - **Research output** → `10_RESEARCH/` or `OPS/`
   - **System map updates** → `OPS/PRINTMAXX_SYSTEM_MAP.md`
   - **Daily plan / actionable queue** → `OPS/DAILY_TACTICAL_PLAN.md`, `OPS/ACTIONABLE_QUEUE.md`

**/goal's status output convention**:
- Append a one-line ledger entry to `LEDGER/GOAL_RUNS.csv` (or similar) per run
- Write a per-run timestamped report under `AUDIT/auto/goal/{YYYY-MM-DD_HH-MM}_summary.md` if a full report is needed
- Update `OPS/CURRENT_STATUS.md` with the latest /goal completion if it represents a meaningful state change
- Never drop a file at root.

**/goal should also AVOID** triggering anything that writes more dated `xlsx` snapshots — until the master_ops_enhancer's output convention is fixed to use a single canonical filename + archive, dated snapshots compound chaos.

---

**End audit. 81 root files → recommend trimming to ~25.**
