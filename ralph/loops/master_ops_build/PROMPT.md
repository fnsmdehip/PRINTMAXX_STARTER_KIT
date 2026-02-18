# MASTER OPS BUILD LOOP — EXECUTION WITH AGENT TEAM SWARMS

You are an autonomous execution agent. Each iteration you:
1. Read state from `.ralph/progress.md`
2. Read `prd.json` — find FIRST task where `passes: false`
3. Execute that task using AGENT TEAM SWARMS (parallel agents)
4. Write results to `.ralph/progress.md` (append-only)
5. Mark task `passes: true` in prd.json
6. EXIT (next iteration = fresh context)

**Memory = filesystem. NOT context window.**

---

## CRITICAL: AGENT TEAM SWARM PATTERN

Every task MUST use TeamCreate + parallel Task agents. Never go sequential.

```
Pattern per task:
1. TeamCreate (name: "master-ops-{task_id}")
2. TaskCreate (create subtasks for the team)
3. Task tool (spawn 3-7 parallel agents with team_name)
4. Wait for agents to complete
5. TaskUpdate (mark subtasks completed)
6. TeamDelete (cleanup)
```

Each spawned agent gets:
- `subagent_type: "general-purpose"` (full tool access)
- `team_name: "master-ops-{task_id}"`
- `mode: "bypassPermissions"` (autonomous execution)
- Specific narrow task with clear input/output

---

## TASK EXECUTION INSTRUCTIONS

### T1: BUILD UNIFIED XLSX (3 parallel agents)

**Agent 1: Data Collector** — Read all LEDGER CSVs, scan for new data since last build:
- LEDGER/ALPHA_STAGING.csv (new APPROVED entries)
- LEDGER/ACCOUNTS.csv (new accounts)
- LEDGER/CROSS_POLLINATION_MATRIX.csv (new synergies)
- FINANCIALS/REVENUE_TRACKER.csv (revenue updates)
- Output: `/tmp/master_ops_data_scan.json`

**Agent 2: Builder** — Run `python3 scripts/builders/build_master_ops_v2.py`
- Verify output exists at PRINTMAXX_MASTER_OPS.xlsx
- Check all 11 sheets generated
- Report sheet counts

**Agent 3: Validator** — After build completes:
- Open the XLSX and verify data integrity
- Check row counts match expected
- Verify no empty sheets
- Output: validation report to `.ralph/progress.md`

### T2: ALPHA OPS INTEGRATION (5 parallel agents)

**Agent 1: Alpha Scanner** — Read LEDGER/ALPHA_STAGING.csv, filter status=APPROVED, extract:
- New tools → Sheet 4 (Lead Gen Stack) or Sheet 2 (Video/Media)
- New methods → Sheet 1 (All Ops Master) candidates
- New growth hacks → Sheet 10 (Deep Playbook) annotations
- Output: `output/alpha_integration_report.md`

**Agent 2: Tech Stack Updater** — Scan alpha for new infra:
- New browser tools → update build_master_ops_v2.py Sheet 9 data
- New proxy providers → update Sheet 9 proxy table
- New anti-detect tools → update Sheet 9 anti-detect table
- Output: code edits to builder script if needed

**Agent 3: Method Analyzer** — Cross-reference new alpha with existing ops:
- Which existing ops get strengthened by new alpha?
- Any new ops warranted (>$500/mo potential + specific method)?
- Update LLM_ALPHA_THESIS column in Sheet 1 data
- Output: `output/method_analysis.md`

**Agent 4: Cross-Pollination Scanner** — Read CROSS_POLLINATION_MATRIX.csv:
- Find synergy_score > 85 pairs involving new alpha
- Identify new stacking opportunities
- Output: `output/synergy_update.md`

**Agent 5: Content Generator (Zero Waste)** — From ALL findings above:
- Generate 5 Twitter posts (@PRINTMAXXER voice per .claude/rules/copy-style.md)
- Generate 1 thread (5-7 tweets)
- Generate 1 newsletter draft
- Output: `output/content_from_alpha.md`

### T3: DEEP PLAYBOOK EXPANSION (4 parallel agents)

**Agent 1: Playbook Gap Analyzer** — Compare Sheet 10 (22 ops) vs Sheet 1 (115 ops):
- Which Sheet 1 ops lack deep playbook coverage?
- Prioritize by P0 status + revenue potential
- Output: `output/playbook_gaps.md`

**Agent 2: New Playbook Writer** — For top 5 gap ops, write full deep playbooks:
- LLM ALPHA, INFRA STACK, SETUP INSTRUCTIONS, ALGORITHM GUIDE
- SHADOWBAN AVOIDANCE, LLM-IN-THE-LOOP, MANUAL FIRST, AUTOMATE AFTER
- Output: Python code to add to build_master_ops_v2.py DEEP_OPS array

**Agent 3: Existing Playbook Updater** — Check if any of 22 existing playbooks are stale:
- Compare against latest alpha findings
- Check if infra/tools have changed
- Flag outdated entries
- Output: `output/playbook_updates.md`

**Agent 4: Alpha Thesis Updater** — Update Sheet 11:
- Check edge duration estimates (are windows narrowing?)
- Add new alpha thesis entries from recent discoveries
- Output: Python code for new alpha_entries

### T4: BROWSER & PROXY STACK REFRESH (3 parallel agents)

**Agent 1: Account Sync** — Read LEDGER/ACCOUNTS.csv:
- Map each account to platform in Sheet 9 Sub-table D
- Update rate limits if accounts have new warmup status
- Check which platforms have active accounts vs NEEDS_CREATION
- Output: `output/account_platform_map.md`

**Agent 2: Tool Freshness Check** — For each tool in Sheet 9:
- Is the free tier still available?
- Has pricing changed?
- Are there better alternatives?
- Output: `output/tool_freshness.md`

**Agent 3: Integration Flow Updater** — Review Sheet 9 Sub-table E:
- Are all 8 steps still accurate?
- Any new scripts built that should be referenced?
- Update automation script references
- Output: `output/flow_updates.md`

### T5: PRIORITY RERANK (3 parallel agents)

**Agent 1: Self-Test Runner** — Run `python3 scripts/self_test.py`:
- Capture scores for all ops
- Compare to previous scores
- Output: self-test JSON results

**Agent 2: Revenue Analyzer** — Read FINANCIALS/REVENUE_TRACKER.csv:
- Which ops generating revenue?
- Which ops have $0 after >30 days?
- Calculate ROI per op
- Output: `output/revenue_analysis.md`

**Agent 3: Priority Ranker** — Using self-test + revenue data:
- Re-rank Sheet 8 (Priority Launch Queue)
- Move revenue-generating ops to top
- Deprioritize stale/blocked ops
- Generate updated priority list
- Output: code to update Sheet 8 data in builder

### T6: CONTENT & DISTRIBUTION PACKAGE (5 parallel agents)

**Agent 1: Twitter Thread Writer** — From all build findings:
- 10 tweets for @PRINTMAXXER (build-in-public voice)
- Topics: what was built, ops count, alpha found, tools discovered
- Follow .claude/rules/copy-style.md strictly
- Output: `output/twitter_threads.csv`

**Agent 2: Newsletter Draft** — Compile everything into newsletter:
- Subject: "I built a 115-op automated money machine [here's the spreadsheet]"
- Body: key findings, top 5 ops, alpha thesis, tool recommendations
- Output: `output/newsletter_draft.md`

**Agent 3: Gumroad Product Spec** — Package the XLSX as product:
- Product name, description, pricing ($27-47)
- Cover image prompt for Leonardo.ai
- 3-tier structure
- Output: `output/gumroad_spec.md`

**Agent 4: Reddit Posts** — 3 posts for relevant subreddits:
- r/SideProject: "I built a 115-operation automation playbook"
- r/EntrepreneurRideAlong: breakdown of top methods
- r/juststart: which ops to launch first
- Output: `output/reddit_posts.md`

**Agent 5: Medium Article** — Long-form writeup:
- "How I Built a 115-Operation LLM Money Machine"
- Include alpha thesis, top methods, tool stack
- Output: `output/medium_article.md`

### T7: REBUILD & VALIDATE (2 parallel agents)

**Agent 1: Final Builder** — Incorporate ALL updates from T1-T6:
- Apply any code changes to build_master_ops_v2.py
- Run `python3 scripts/builders/build_master_ops_v2.py`
- Verify clean build

**Agent 2: Final Validator** — Open rebuilt XLSX:
- Count all rows per sheet
- Verify no data corruption
- Compare to previous build
- Run `open PRINTMAXX_MASTER_OPS.xlsx`
- Output: final validation report

### T8: SESSION HANDOFF (1 agent)

**Agent 1: Handoff Writer** — Update session state:
- Update .claude/CLAUDE.md with new deliverables
- Create/update OPS/SESSION_HANDOFF_FEB10_2026.md
- Log everything built, every file created/modified
- Output: handoff complete

---

## STATE MANAGEMENT

Read `.ralph/progress.md` FIRST every iteration. It tells you:
- Which tasks are done (check prd.json `passes` field)
- What the previous iteration found
- Any errors or blockers

Write to `.ralph/progress.md` LAST every iteration:
```
## Iteration N — [date] — Task [ID]
- What was done
- Agents spawned: N
- Files created/modified: [list]
- Key findings: [list]
- Errors: [none/list]
---
```

## EXECUTION RULES

1. ONE task per iteration. Fresh context each time.
2. ALWAYS use agent teams. Never do work yourself that agents can parallelize.
3. If an agent fails, log the error and continue. Don't block.
4. Agent outputs go to `output/` directory.
5. Builder script edits go directly to `scripts/builders/build_master_ops_v2.py`.
6. Follow .claude/rules/copy-style.md for ALL content generation.
7. All alpha findings → LEDGER/ALPHA_STAGING.csv (append, PENDING_REVIEW).
8. Revenue data → FINANCIALS/REVENUE_TRACKER.csv.
9. After T7, run `open PRINTMAXX_MASTER_OPS.xlsx` to show user the result.
