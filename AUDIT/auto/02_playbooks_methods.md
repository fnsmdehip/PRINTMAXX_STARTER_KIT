# Audit: Playbooks + Money Methods
**Date**: 2026-05-15
**Scope**: 03_PLAYBOOKS/, MONEY_METHODS/
**Auditor**: Claude (read-only audit)

## Executive snapshot
- `03_PLAYBOOKS/` = **49 venture directories**, dominated by markdown strategy docs (mtimes mostly Jan-Feb 2026, 95% untouched in 75+ days). Source for the legacy "INDEX.md" doctrine.
- `MONEY_METHODS/` = **39 venture directories** (more recent, several edited Mar-Apr 2026). This is where current execution lives.
- **Two dirs were both modeled**: `MONEY_METHODS/CONTENT_FARM` (Feb) vs `03_PLAYBOOKS/CONTENT_FARM` (Jan). Overlap is heavy.
- **Only ONE venture is actually wired to cron with live activity: APP_FACTORY** (`auto_orchestrator.py --full` 6:30 AM daily, `portfolio_optimizer.py` Mon 7 AM).
- **EAS** has scripts + playbooks + a weekly surge deploy of the website, but the venture orchestration cron (`venture_autonomy.py --run-all`) is **DISABLED** ("C56_DISABLED" comment) — it is operational on paper but not running on schedule.
- **META_ADS_AUTONOMOUS** has a usable orchestrator and config skeleton but its `actions_log.csv` has only the header row (Mar 20), no health reports written, no Meta API account ID set → **stillborn**.
- **ALGO_TRADING**, **NSFW_AI_CONTENT**, **AI_INFLUENCER**, **CONTENT_FARM**, **NEWSLETTER**, **SKOOL_COMMUNITY**, **MICRO_SAAS**, **COMMUNITY**, etc. = playbook markdown only, no scripts wired to cron.
- Revenue: **$0**, 101 days at zero per `FINANCIALS/revenue_pipeline.json`. 529 assets built, 19 monetized, 0 producing revenue.

---

## Inventory (organized by venture)

### Live ventures (have BOTH playbook docs AND executable scripts)

| Venture | Path | Playbooks | Scripts/automation | Last script mtime |
|---------|------|-----------|--------------------|-------------------|
| APP_FACTORY | `MONEY_METHODS/APP_FACTORY/` | 30+ MD files (design system, ASO, QA standards, central index) + 67 build dirs | `AUTOMATIONS/app_factory/` (auto_orchestrator, opportunity_scanner, app_generator, deep_qa, test_runner, post_build_validator, build_submit, distribution_engine, portfolio_optimizer) | 2026-04-02 |
| EAS | `MONEY_METHODS/EAS/` | 4 delivery playbooks (Signal Map, Phone Pilot, Ops Pilot, Managed Ops), 4 legal templates (MSA, SOW, Risk Disclosure, Subcontractor) | `AUTOMATIONS/eas_lead_pipeline.py`, `eas_self_test.py`, `venture_pipeline_eas.py` | 2026-04-02 |
| META_ADS_AUTONOMOUS | `MONEY_METHODS/META_ADS_AUTONOMOUS/` | `META_ADS_PLAYBOOK.md`, `README.md` | `scripts/orchestrator.py` (6 steps: health, fatigue, budget, copy gen, ad upload, brief) | 2026-03-20 |
| BEFORE_YOU | `MONEY_METHODS/BEFORE_YOU/` | `BEFORE_YOU_VENTURE_README.md`, playbooks/legal/outreach subdirs | External codebase at `~/Documents/ancestry-research/before-you/` (not in scope) | 2026-03-21 |
| OUTBOUND | `MONEY_METHODS/OUTBOUND/` | `SEND_QUEUE.md` | `email_sequences/` (14 sequences), `personalized/` (65+ pre-built emails) — these are content, no runner script in MONEY_METHODS/ | 2026-03-22 |
| LOCAL_BIZ | `MONEY_METHODS/LOCAL_BIZ/` | Many MDs (AGENCY_WEBSITE, AI_CALL_OUTREACH, MOTION_UPSELL, NATIONWIDE_LEAD_GEN) | `personalize_template.py`, `fix_placeholders.py` + `templates/` + `motion_templates/` | 2026-02-12 |

### Playbook-only ventures in MONEY_METHODS/ (no executable scripts, recently touched)

| Venture | Path | mtime | Content |
|---------|------|-------|---------|
| AI_ART_VENTURE | `MONEY_METHODS/AI_ART_VENTURE/` | 2026-04-24 | `AI_ART_VENTURE_PLAYBOOK.md`, `install_now.sh`, `setup_comfyui.sh`, `test_output/` |
| NSFW_AI_CONTENT | `MONEY_METHODS/NSFW_AI_CONTENT/` | 2026-04-06 | 5 MD files (execution plan, viral tactics, safety, audit) + FINDOM subdir + ugc_scripts |
| AI_CONTENT_AFFILIATE | `MONEY_METHODS/AI_CONTENT_AFFILIATE/` | 2026-03-07 | `AI_CONTENT_AFFILIATE_PLAYBOOK.md`, `email_sequence_ai_stack.md` |
| COLD_OUTBOUND | `MONEY_METHODS/COLD_OUTBOUND/` | 2026-03-07 | 5 email sequence MDs |
| AI_INFLUENCER | `MONEY_METHODS/AI_INFLUENCER/` | 2026-03-06 | 5 MDs (AI_NSFW_EXECUTION_FULL, FINDOM_EXECUTION_PLAN, viral_tactics) + FINDOM subdir |
| MICRO_SAAS | `MONEY_METHODS/MICRO_SAAS/` | 2026-03-05 | 3 product folders (invoice-tracker, content-calendar, website-audit) — no orchestrator |
| NEWSLETTER | `MONEY_METHODS/NEWSLETTER/` | 2026-03-05 | 5 MDs (LEAD_MAGNETS, NEWSLETTER_LAUNCH_PLAN, 3 welcome sequences) |
| SKOOL_COMMUNITY | `MONEY_METHODS/SKOOL_COMMUNITY/` | 2026-03-05 | 4 MDs (course outlines, 5-day challenge, launch plan) |
| MCP_MARKETPLACE | `MONEY_METHODS/MCP_MARKETPLACE/` | 2026-03-20 | `LAUNCH.md`, `MONETIZATION.md`, `index.html`, `submit.html`, mcphub-mirror |

### Aspirational / static doc ventures (last touched Feb 2026 or earlier; treat as dormant unless promoted)

`SYNERGY_STACKS` (2/2), `TOOL_ALPHA` (2/3), `POD` (2/5), `TIKTOK_SHOP` (2/5), `CONTENT_FARM` (2/6), `PLATFORM_ARBITRAGE` (2/6), `SYNERGY_PACKAGES` (2/6 — 18 stack MDs), `CLIPPING_SERVICE` (2/10), `ECOM` (2/10), `ECOM_ARB` (2/10), `GOVERNMENT_CONTRACTS` (2/10), `AI_AGENT_SERVICES` (2/12), `AI_AGENTS_SERVICE` (2/12 — duplicate dir!), `API_ARBITRAGE` (2/12), `AUTOMATION_AGENCY` (2/12), `COMMUNITY` (2/12), `DIGITAL_PRODUCTS` (2/12), `PREDICTION_MARKETS` (2/12), `PROMPT_MARKETPLACE` (2/12).

### 03_PLAYBOOKS — strategy documents (Jan-Feb 2026)

Of 49 venture dirs in `03_PLAYBOOKS/`, only 3 contain real Python scripts:
- `ALGO_TRADING/signals/trading_signal_scraper.py` (Jan 2026)
- `APP_FACTORY/scripts/{generate_icons,design_aggregator}.py` + `ci_cd/scripts/`
- 4 build dirs under `APP_FACTORY/builds/*/complete_setup.py` etc.

Everything else in `03_PLAYBOOKS/` is markdown strategy documents (CONTENT_FARM/automation/REPURPOSING_SYSTEM.md, COLD_OUTBOUND/scripts/COLD_CALL_SCRIPT.md = a *script* in the sales sense, not executable code).

These 49 dirs are the **legacy doctrine layer**. The "INDEX.md" in `03_PLAYBOOKS/` (last edited 2026-01-25) is the master reference but lists status as "Active/Planning/New/Research" — none of those are wired to cron.

---

## Live / Operational (with trigger mechanism)

Cron audit confirms exactly **one venture** has an active recurring trigger:

### APP_FACTORY — fully operational
```
30 6 * * * python3 AUTOMATIONS/app_factory/auto_orchestrator.py --full
0 7 * * 1 python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --optimize
```
6-stage pipeline (scan → generate → QA → test → build/submit → distribute) runs daily. 67 builds in `MONEY_METHODS/APP_FACTORY/builds/`. Latest builds reach into early April. **This is the only venture that actually does work each day.**

### EAS — half-wired
- Script: `AUTOMATIONS/eas_lead_pipeline.py` (Mar 21). Available, ready to run.
- Website cron: `6 5 * * 0 npx surge . eas-preview.surge.sh` (deploys EAS website weekly Sunday 5:06 AM).
- **Master orchestration cron is commented out**: `# C56_DISABLED: 25 5 * * * cd $BASE && $PYTHON AUTOMATIONS/venture_autonomy.py --run-all` and `# C56_DISABLED: 25 5 * * * cd $BASE && $PYTHON AUTOMATIONS/venture_pipeline_brokering.py --run`.
- Lead pipeline script exists, but nothing automatically runs it. Manual invocation only.
- Revenue: $0. No clients booked. DBA / bank / Cal.com still flagged as blockers in README.

### Cross-venture engines (run daily but don't directly produce revenue)
These run every morning but are *intelligence* and *ranking* layers, not method execution:
- `method_discovery_crawler.py --crawl` (5 AM) — finds new methods
- `capital_genesis_ranker.py --rank --report` (5:15 AM) — scores methods
- `cross_pollinator_v2.py --cycle` (5:50 AM) — finds synergies
- `actionable_aggregator.py` (5:20 AM) — surfaces tasks
- `decision_engine.py --cycle` (5:20 AM)
- `rbi_loop.py --full` (5:20 AM) — Research/Backtest/Implement
- `sec_edgar_scanner`, `crunchbase_scanner`, `ecom_arb_engine`, `opportunity_radar`, `sam_gov_monitor`, `morning_intelligence_dag` (all 5 AM)
- 6 surge deploys on Sunday 5 AM (builders-ledger, devprint-portfolio, agent-soul/site, eas-preview, before-you-ancestry, fnsmdehip-research) — *static site refreshes*, not revenue actions.

Notable absence: **no cron for venture_pipeline_content, venture_pipeline_outbound, venture_pipeline_app, venture_pipeline_local_biz, venture_pipeline_eas, venture_pipeline_monetize, venture_pipeline_product, venture_pipeline_research, venture_pipeline_scraping**. The 9 venture pipeline scripts exist, but only `app_factory/auto_orchestrator.py` (a *separate* parallel pipeline) is on cron.

---

## Dead / Orphan / Abandoned

### META_ADS_AUTONOMOUS — stillborn
- Orchestrator script exists (385 lines, structured 6-step loop)
- Config exists: `targets.json` (Mar 20), `credentials.env` (Mar 20, empty token)
- `actions_log.csv` is just the header row (zero actions logged since creation Mar 20)
- `health_reports/` directory is empty
- NOT on cron. NO `META_AD_ACCOUNT_ID` configured. social-cli is not installed.
- Built but never lit up. Probably 2 hours from working if a Meta ad account existed.

### ALGO_TRADING (both locations)
- `03_PLAYBOOKS/ALGO_TRADING/` — 5 MDs + 1 Python `signals/trading_signal_scraper.py`. Last touched Jan 26.
- No cron. No active signals. Documented as "Planning" status in INDEX.md.

### 03_PLAYBOOKS/ legacy ventures (49 dirs, 95% Jan 2026)
- Most haven't been touched in 75+ days
- These are research/doctrine docs, never had execution scripts wired
- Examples of truly dormant: COURSE_CREATOR, NEWSLETTER_PREMIUM, PAYWALL_OPTIMIZATION_SERVICE, PERSONAL_BRAND_SEO, PORTFOLIO_APP_BUILDER, WHITE_LABEL, X_LAUNCH_VIRAL, MEMECOIN_TRADING, FACELESS_YOUTUBE, ETSY_DIGITAL, ECOM_DROPSHIP, COMMUNITY_PAID (all empty or near-empty, single MD).

### Recent venture dirs without execution path
- AI_ART_VENTURE (Apr 24, has install scripts but no cron, no monetization wire)
- NSFW_AI_CONTENT (Apr 6, plans only, FINDOM subdir empty of automation)
- AI_INFLUENCER (Mar 6, MDs only)
- MICRO_SAAS (3 product subdirs, no orchestration)
- SKOOL_COMMUNITY (4 launch MDs, no community created)
- NEWSLETTER (5 MDs, no ESP wiring)

### `AI_AGENT_SERVICES` vs `AI_AGENTS_SERVICE` (both Feb 12)
Two near-identical dir names. One holds `AGENCY_WEBSITE.md` material. Almost certainly accidental duplication.

### Scripts that exist but aren't called
From `AUTOMATIONS/`: `venture_pipeline_content.py`, `venture_pipeline_outbound.py`, `venture_pipeline_app.py`, `venture_pipeline_local_biz.py`, `venture_pipeline_eas.py`, `venture_pipeline_monetize.py`, `venture_pipeline_product.py`, `venture_pipeline_research.py`, `venture_pipeline_scraping.py`, `venture_pipeline_brokering.py`, `venture_autonomy.py --run-all` — all of these are orphaned by the C56_DISABLED comment.

---

## Duplication or Overlap

| Concept | Locations | Notes |
|---------|-----------|-------|
| **APP_FACTORY** | `03_PLAYBOOKS/APP_FACTORY/` (Feb 15) + `MONEY_METHODS/APP_FACTORY/` (Apr 2) + `AUTOMATIONS/app_factory/` | Three layers: doctrine, builds, execution. The doctrine/builds split is intentional but creates 30+ duplicated planning docs. |
| **CONTENT_FARM** | `03_PLAYBOOKS/CONTENT_FARM/` (Feb 2) + `MONEY_METHODS/CONTENT_FARM/` (Feb 6) | Both have account_matrix / channel sub-dirs. Heavy overlap, no clear winner. |
| **AI_INFLUENCER** | `03_PLAYBOOKS/AI_INFLUENCER/` (Feb 2) + `MONEY_METHODS/AI_INFLUENCER/` (Mar 6) | MONEY_METHODS version has different file names — these have *diverged* rather than mirrored. |
| **COLD_OUTBOUND** | `03_PLAYBOOKS/COLD_OUTBOUND/` (Feb 8, deep) + `MONEY_METHODS/COLD_OUTBOUND/` (Mar 7, shallow) | Playbook is deep with infrastructure / lead_gen / sequences. Money methods is just 5 email sequences. |
| **NEWSLETTER** | `03_PLAYBOOKS/NEWSLETTER/` (Feb 2) + `MONEY_METHODS/NEWSLETTER/` (Mar 5) | Both have launch plans / lead magnets — overlap. |
| **ECOM** | `03_PLAYBOOKS/ECOM/` (Jan 26) + `MONEY_METHODS/ECOM/` (Feb 10) | Strategy docs duplicated. |
| **ECOM_ARB** | `03_PLAYBOOKS/ECOM_ARB/` (empty Jan 24) + `MONEY_METHODS/ECOM_ARB/` (Feb 10) | Playbook is empty stub. |
| **DIGITAL_PRODUCTS** | `03_PLAYBOOKS/DIGITAL_PRODUCTS/` (Feb 2) + `MONEY_METHODS/DIGITAL_PRODUCTS/` (Feb 12) | Doctrine duplicated. |
| **COMMUNITY** | `03_PLAYBOOKS/COMMUNITY/` (Jan 28) + `MONEY_METHODS/COMMUNITY/` (Feb 12) | Doctrine duplicated. |
| **AI_AGENT_SERVICES / AI_AGENTS_SERVICE / AUTOMATION_AGENCY / EAS** | All four exist. EAS is the canonical evolved version. Other three are vestigial. |
| **PROMPT_ENGINEERING (playbooks)** vs **PROMPT_MARKETPLACE (money methods)** | Same goal, different name. |
| **OUTBOUND** | `03_PLAYBOOKS/OUTBOUND/` (Jan 23) + `MONEY_METHODS/OUTBOUND/` (Mar 22) + `03_PLAYBOOKS/COLD_OUTBOUND/` (Feb 8) + `MONEY_METHODS/COLD_OUTBOUND/` (Mar 7) | Four dirs. OUTBOUND ≠ COLD_OUTBOUND in directory naming but overlap heavily. |

The MONEY_METHODS layer is the *live execution slot*; the 03_PLAYBOOKS layer is mostly *legacy strategy*. Roughly **30% of dirs in 03_PLAYBOOKS/ are also re-created (and now diverged) in MONEY_METHODS/**.

---

## Venture matrix

Notation: A=active, D=dormant (mtime > 60 days, no cron, no recent activity), B=built-not-fired, X=abandoned/empty. Cron column refers to a dedicated venture-execution cron, not generic intelligence crons.

| Venture | Status | Cron? | Revenue-producing? | Last touched | Notes |
|---------|--------|-------|--------------------|--------------|-------|
| APP_FACTORY | A | YES (auto_orchestrator daily 6:30 AM, portfolio_optimizer Mon 7 AM) | No ($0, 67 builds, 0 confirmed sales) | 2026-04-02 | Only fully-wired venture. Pipeline exists end-to-end. |
| EAS | A (paper) / B (in practice) | NO (master cron DISABLED) — weekly surge of website only | No ($0, 0 clients) | 2026-04-02 (script), 2026-03-19 (website) | Lead pipeline script ready. Cron commented out. Needs DBA/bank/Cal.com human action. |
| META_ADS_AUTONOMOUS | B | NO | No (no token) | 2026-03-20 | Orchestrator built, never run live. |
| BEFORE_YOU | A | NO (external codebase, has Stripe live) | Stripe live, $0 sales | 2026-03-21 | Live MVP at `~/Documents/ancestry-research/before-you/`. Distribution not started. |
| OUTBOUND | B | NO | No | 2026-03-22 | 65+ pre-personalized emails drafted, SEND_QUEUE.md exists, no send automation. |
| LOCAL_BIZ | B | NO | No | 2026-02-12 | Templates + personalize script. Was used to generate sites but no cron. |
| AI_ART_VENTURE | B | NO | No | 2026-04-24 | ComfyUI install scripts, playbook. No monetization wired. |
| AI_INFLUENCER | B | NO | No | 2026-03-06 | Strategy docs only. |
| AI_CONTENT_AFFILIATE | B | NO | No | 2026-03-07 | Playbook only. |
| MICRO_SAAS | B | NO | No | 2026-03-05 | 3 product subdirs, no live products. |
| NEWSLETTER | B | NO | No | 2026-03-05 | 5 MDs, no ESP. |
| SKOOL_COMMUNITY | B | NO | No | 2026-03-05 | 4 launch MDs, no Skool created. |
| MCP_MARKETPLACE | B | NO | No | 2026-03-20 | Has index.html + submit.html, never deployed. |
| NSFW_AI_CONTENT | B | NO | No | 2026-04-06 | Plans only. |
| CLIPPING_SERVICE | D | NO | No | 2026-02-10 | 3 MDs. |
| CONTENT_FARM | D | NO | No | 2026-02-06 | YouTube automation plans + sleep YouTube subdir. |
| PLATFORM_ARBITRAGE | D | NO | No | 2026-02-06 | 3 MDs. |
| SYNERGY_PACKAGES | D | NO | No | 2026-02-06 | 18 synergy stack MDs (reference material). |
| POD | D | NO | No | 2026-02-05 | 3 MDs. |
| TIKTOK_SHOP | D | NO | No | 2026-02-05 | 3 MDs. |
| SYNERGY_STACKS | D | NO | No | 2026-02-02 | Strategy. |
| TOOL_ALPHA | D | NO | No | 2026-02-03 | Strategy. |
| AI_AGENT_SERVICES | D | NO | No | 2026-02-12 | Duplicate of EAS predecessor. |
| AI_AGENTS_SERVICE | D | NO | No | 2026-02-12 | Near-duplicate of above. |
| API_ARBITRAGE | D | NO | No | 2026-02-12 | Single MD. |
| AUTOMATION_AGENCY | D | NO | No | 2026-02-12 | Predecessor to EAS. |
| COMMUNITY | D | NO | No | 2026-02-12 | Single MD. |
| DIGITAL_PRODUCTS | D | NO | No | 2026-02-12 | Single MD. |
| ECOM | D | NO | No | 2026-02-10 | Single MD. |
| ECOM_ARB | D | NO | No | 2026-02-10 | Single MD. |
| GOVERNMENT_CONTRACTS | D | NO | No | 2026-02-10 | Single MD. (Note: `sam_gov_monitor` on daily cron — sourcing layer alive, execution not). |
| PREDICTION_MARKETS | D | NO | No | 2026-02-12 | Single MD. |
| PROMPT_MARKETPLACE | D | NO | No | 2026-02-12 | Single MD. |
| All 49 dirs in 03_PLAYBOOKS/ | D/X | NO | No | mostly 2026-01-2x | Doctrine docs, not execution paths. |

---

## Top 3 Risks

1. **Venture orchestration is disabled at the cron layer.** The `venture_autonomy.py --run-all` and `venture_pipeline_brokering.py --run` entries carry the `C56_DISABLED` comment. That means every `venture_pipeline_*.py` script in AUTOMATIONS/ — EAS, content, outbound, app, local_biz, monetize, product, research, scraping — has no automatic firing mechanism. Whatever `/goal` orchestrates needs either to re-enable that cron, call those scripts directly, or work around them. APP_FACTORY survives only because it has its own *parallel* orchestrator (`AUTOMATIONS/app_factory/auto_orchestrator.py`) on a separate cron.
2. **Doctrine/execution duplication confuses any orchestrator.** Roughly 30% of `03_PLAYBOOKS/` ventures have parallel (and divergent) `MONEY_METHODS/` siblings. A `/goal "build content factory"` command would face the choice of `03_PLAYBOOKS/CONTENT_FARM/` (deep doctrine, Jan 2026) vs `MONEY_METHODS/CONTENT_FARM/` (shallow, Feb 2026) — without a manifest that says which one wins. Same hazard for COLD_OUTBOUND, NEWSLETTER, AI_INFLUENCER, ECOM. The system memory says "use Resource Manifest", but `/goal` will hit ambiguity if it greps directories instead.
3. **Built-but-unfired scripts give a false impression of liveness.** META_ADS_AUTONOMOUS, EAS lead pipeline, OUTBOUND personalized email batch, MICRO_SAAS product folders, MCP_MARKETPLACE submit.html — every one of these *looks* live but has no firing cron and no human triggering it. The 39-cron count overstates operational coverage because the 39 are mostly intelligence/sourcing crons (scrapers, rankers, deployers), not method execution. Only APP_FACTORY actually executes a method daily.

---

## Top 3 Opportunities

1. **One un-disable from cash flow drill.** The single line `# C56_DISABLED: 25 5 * * * ... venture_autonomy.py --run-all` is what gates the entire venture pipeline ecosystem. If `venture_autonomy.py` is healthy (system memory says it is — 8 venture types, intelligence-first execution), uncommenting that one cron entry lights up 8 ventures simultaneously. `/goal` could include "verify-then-enable" of this entry as a first-order check.
2. **EAS is the closest revenue path that's already 80% built.** Playbooks complete, legal templates complete, website live on surge (auto-redeploys weekly), lead pipeline script ready, scrapers feeding daily. Missing only: human action (DBA filing, bank, Cal.com setup) and one cron entry to fire `eas_lead_pipeline.py` daily. `/goal "ship EAS"` could be a 3-step exec: enable cron, generate Send Queue update, surface human-action blockers with time estimates.
3. **APP_FACTORY pattern is replicable.** The reason APP_FACTORY works is its dedicated `auto_orchestrator.py --full` that runs the whole `scan→generate→QA→test→build→distribute` chain in one shot, separately from `venture_autonomy.py`. Every other venture in MONEY_METHODS that already has a real script (EAS, META_ADS) should follow that pattern: one orchestrator, one cron line, one log file. `/goal` is essentially asking for the same pattern at the meta-level — one orchestrator that calls the per-venture orchestrators.

---

## For the `/goal` long-run command

What `/goal` needs to know about this subtree:

1. **Treat `03_PLAYBOOKS/` as read-only doctrine.** It's the strategy library, last meaningfully maintained Jan-Feb 2026. Do not write new things here. Use it to load playbook prose for an agent prompt, then route execution to `MONEY_METHODS/` or `AUTOMATIONS/`.

2. **Authoritative venture list lives in `MONEY_METHODS/` (39 dirs).** Subset that has *any* executable wire:
   - APP_FACTORY (alive)
   - EAS (script exists, needs cron)
   - META_ADS_AUTONOMOUS (orchestrator exists, needs token + cron)
   - BEFORE_YOU (external codebase, Stripe live, needs distribution)
   - OUTBOUND (drafts exist, needs sender)
   - LOCAL_BIZ (templates exist, needs lead source feed)
   The other 33 are markdown only — `/goal` should either ignore them or treat them as "promote-to-build" backlog.

3. **Cron coverage map for the orchestrator to consult:**
   - `auto_orchestrator.py --full` covers APP_FACTORY end-to-end → don't reinvent
   - `eas_lead_pipeline.py` covers EAS lead-gen step → just needs daily cron entry or `/goal` call
   - `scripts/orchestrator.py` (inside `META_ADS_AUTONOMOUS/scripts/`) covers Meta ad management → needs Meta account first
   - Everything else needs `/goal` to call `venture_pipeline_<type>.py` from `AUTOMATIONS/` — but those won't fire on their own (cron is disabled).

4. **`/goal` should prefer existing orchestrators over building new ones.** From `AUTOMATIONS/`:
   - For APP work: `app_factory/auto_orchestrator.py --full`
   - For EAS: `eas_lead_pipeline.py` + `venture_pipeline_eas.py`
   - For all-venture sweep: `venture_autonomy.py --run-all` (currently disabled in cron — but the script runs standalone)
   - For prioritization: `capital_genesis_ranker.py --rank --top N`
   - For task surfacing: `actionable_aggregator.py`
   - For decisioning: `decision_engine.py --cycle`

5. **Honest revenue state to feed into `/goal` reasoning:**
   - $0 revenue, 101 days at zero
   - 529 assets built, 19 monetized, 0 revenue-producing
   - Bottleneck per `FINANCIALS/revenue_pipeline.json`: human action (Amazon Associates + ClickBank signup), not technical
   - Surge CLI is logged into the wrong account → previously-deployed properties can't be updated (separate from this audit but very relevant to /goal)

6. **Duplication risks for `/goal`** — when a user says "run the content farm", the orchestrator must pick `MONEY_METHODS/CONTENT_FARM/` for execution and `03_PLAYBOOKS/CONTENT_FARM/` for doctrine reference. A simple name→canonical-path resolver should be the first piece `/goal` initializes.

7. **What's missing that `/goal` should not try to fix in scope of one command:**
   - There is no central "venture status" health endpoint that aggregates all venture pipeline scripts. `venture_autonomy.py --status` is the closest. `/goal` should probably call this once per cycle.
   - No revenue confirmation hook. The pipeline produces "assets" but not income. `/goal` cannot manufacture revenue — it can only narrow down the 3 specific human actions that unblock it (EAS DBA, Stripe MCP auth, Amazon Associates signup).
