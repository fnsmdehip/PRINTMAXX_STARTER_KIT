# Audit: Research
**Date**: 2026-05-15
**Scope**: 10_RESEARCH/, RESEARCH/, root-level research files

## Inventory

### Root-level research docs (4 files)
| File | Size | Last touched | Status |
|------|------|--------------|--------|
| `/RESEARCH_NEW_METHODS_2026.md` | 11K | Jan 24 | Stale (~3.5 mo) — defines MM017-MM021 |
| `/NICHE_CONTENT_RESEARCH_2025_2026.md` | 37K | Mar 5 | Stale-ish (~2.5 mo) — 11 niches, pricing, sounds, affiliates |
| `/NEW_METHODS_SUMMARY_2026-01-24.md` | 7K | Jan 24 | Stale (~3.5 mo) — summary of the 5 new MMs |
| `/RBI_AND_AUTOMATION_ANALYSIS.md` | 26K | Feb 10 | Stale (~3 mo) — meta-critique of the old RBI system (since rewritten as `AUTOMATIONS/rbi_loop.py`) |

### `/10_RESEARCH/` (12 entries; 2 docs + 2 subtree clusters + UAF dump)
- `COMPETITOR_MARKETING_ANALYSIS.md` (25K, Jan 25) — Hallow/Pray.com/Headspace marketing teardowns. Last touched almost 4 months ago.
- `competitors/` — 5 niche folders (ai_tools, customer_service_ai, faith_apps, fitness_apps, info_products). Each has TOP_10_COMPETITORS / GAP_ANALYSIS / PRICING / DIFFERENTIATION / FEATURE_MATRIX / MARKET_OVERVIEW. All dated Jan 20. Frozen since.
- `VIDEO_RESEARCH/` — most maintained subdir: `comparisons/MASTER_VIDEO_TOOLS_2026.md` (Mar 22), `pipeline/N8N_VIDEO_WORKFLOW.md` (Mar 22), `tools_tracker/ALL_TOOLS_TRACKER.csv` (Mar 21). Has a `README.md` declaring it the central command for video tool research. Auto-fed by `AUTOMATIONS/perpetual_tool_researcher.py`.
- `UAF_*` (memory, soul, meta_rules, bias_null, v45/v51 full text) — Mar 28. Cognitive-architecture references, not money-method research.

### `/RESEARCH/` (20 files, ALL `PEMF_*.md`)
- Single-venture research suite for PEMF (Pulsed Electromagnetic Field hardware). 17 files, Feb 7-8. Master research, GTM, compliance, DIY build, dropship, supplement synergy, influencer audits across podcasters/TikTok/Twitter, Steve Bradet transcripts, gaussmeter guide, capital genesis bootstrap path.
- 100% frozen since Feb 8. PEMF venture was never spun up — these docs are buried.

### Other research outputs (in-scope by content, out-of-scope by path)
- `OPS/alpha_research/` (5 files) — the real perpetual-research output dir. Newest: `CONTAINERIZED_ACCOUNTS_INFRASTRUCTURE_2026-04-17.md` and `SOCIAL_MEDIA_AUTOMATION_STACK_2026-04-17.md`. Earlier: `OPEN_SOURCE_MONEY_TOOLS_2026-03-08.md`, plus a `2026-01-21.md` daily.
- `AUTOMATIONS/auto_ops/discovered_methods/` (44 .md) — auto-generated method dossiers from the crawler. Newest = Mar 29. Stale 6+ weeks. Each file has scoring, summary, implementation plan.
- `AUTOMATIONS/auto_ops/alpha_theses/BOOMER_MALE_55_70_AFFILIATE.md` (Mar 18) — fully fleshed Capital Genesis P0 thesis. Only 1 of its kind. Should be a folder of these, not a folder of one.
- `LEDGER/METHOD_DISCOVERY_LOG.csv` (5,169 rows, last Apr 20) — the crawler's structured tail.
- `LEDGER/CAPITAL_GENESIS_RANKINGS.csv` (May 6) and `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` (May 6 05:18) — the LIVE ranking output. 9,441 methods scored.

## Research pipeline (source -> synthesis -> action) — diagram + commentary

```
SOURCES
  Twitter scrapers (6 AM cron)  ----+
  Reddit scraper (6:15 AM)      ----+--> LEDGER/ALPHA_STAGING.csv (raw)
  HN, SEC, Crunchbase scanners  ----+
  method_discovery_crawler.py   ----+--> LEDGER/METHOD_DISCOVERY_LOG.csv (scored)
   (5 AM, 18 subreddits + HN+Twitter)     + auto_ops/discovered_methods/*.md (dossier per method)
  perpetual_tool_researcher.py  --------> 10_RESEARCH/VIDEO_RESEARCH/comparisons/* + tools_tracker/*

SYNTHESIS / SCORING
  alpha_auto_processor.py (10 PM) --> approves entries -> routes to ventures
  capital_genesis_ranker.py (5:30 AM)
      reads ALPHA_STAGING + METHOD_DISCOVERY_LOG + auto_ops/* + master_ops_cache
      writes: OPS/CAPITAL_GENESIS_PRIORITY_STACK.md  (human-readable)
              LEDGER/CAPITAL_GENESIS_RANKINGS.csv     (machine-readable, 9,441 rows)
  autonomous_integrator (10:15 PM) -> growth_plans, dag_plans, handoff_chains

ACTION
  CEO Agent reads Priority Stack at Phase 3.5 (intelligence injection)
  Daily Engagement Planner (7 AM) reads it
  Daily Tactical Plan, Session Briefing, Resource Manifest all reference it
  actionable_aggregator.py (7:30 AM) -> OPS/ACTIONABLE_QUEUE.md
     >>> BUT: aggregator does NOT read 10_RESEARCH/ or RESEARCH/ or OPS/alpha_research/.
         It reads PERSISTENT_TASK_TRACKER, DAILY_TACTICAL_PLAN, PROMPT_META_REVIEW,
         swarm reports, CEO decisions, DECISIONS.csv. That is the loop hole.
```

**Commentary**
- The LIVE pipeline runs through `LEDGER/`, `auto_ops/`, and `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md`. That's where current intelligence lives.
- `10_RESEARCH/`, `RESEARCH/`, and the four root-level research docs are MOSTLY a frozen first-pass corpus from Jan-Mar. They were the inputs that informed the system; they are not currently being refreshed by it.
- `10_RESEARCH/VIDEO_RESEARCH/` is the one exception — `perpetual_tool_researcher.py` does write back here, so it has Mar 21-22 files. That subtree is the model for what the rest of `10_RESEARCH/` should look like.
- `OPS/alpha_research/` (out of scope but the real heir to `10_RESEARCH/`) is also a half-live dir: 2 fresh April 17 reports, then nothing.

## Live (recent / refreshing)

| Path | Last touched | Refresh mechanism |
|------|--------------|--------------------|
| `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` | May 6 | cron 5:30 AM daily (`capital_genesis_ranker.py`) |
| `LEDGER/CAPITAL_GENESIS_RANKINGS.csv` | May 6 | same cron |
| `LEDGER/METHOD_DISCOVERY_LOG.csv` | Apr 20 (stale ~25d) | cron 5 AM daily (`method_discovery_crawler.py`) — may be failing silently |
| `auto_ops/discovered_methods/*.md` | Mar 29 (stale ~47d) | crawler writes dossiers; appears stalled |
| `10_RESEARCH/VIDEO_RESEARCH/` | Mar 22 | `perpetual_tool_researcher.py` (no clear cron) |
| `OPS/alpha_research/CONTAINERIZED_ACCOUNTS_*` | Apr 17 | ad-hoc deep-research session |
| `OPS/alpha_research/SOCIAL_MEDIA_AUTOMATION_*` | Apr 17 | ad-hoc deep-research session |

## Stale / Forgotten research

| Path | Frozen since | Days stale | Notes |
|------|--------------|------------|-------|
| `RESEARCH/PEMF_*.md` (17 docs, 530K) | Feb 8 | ~97 | Whole venture frozen. Bootstrap-to-$1K plan literally costs $451-1,051. Either run it or archive it. |
| `10_RESEARCH/competitors/*` (30 files) | Jan 20 | ~115 | All 5 niches' marketing/pricing/gap analyses. PRICING gets stale fast. |
| `10_RESEARCH/COMPETITOR_MARKETING_ANALYSIS.md` | Jan 25 | ~110 | Hallow/Headspace tactics. App-factory pipeline still references it. |
| `RESEARCH_NEW_METHODS_2026.md` + `NEW_METHODS_SUMMARY_2026-01-24.md` | Jan 24 | ~111 | MM017-MM021 defined here. No follow-up doc; status of those 5 methods only knowable via Priority Stack lookup. |
| `NICHE_CONTENT_RESEARCH_2025_2026.md` | Mar 5 | ~71 | Cross-niche viral formats, sound trends, ad creatives, pricing benchmarks. Should be re-run quarterly. |
| `RBI_AND_AUTOMATION_ANALYSIS.md` | Feb 10 | ~94 | Critique of OLD rbi_audit.py. Already superseded by `AUTOMATIONS/rbi_loop.py`. Archive candidate. |
| `auto_ops/discovered_methods/*.md` | Mar 29 | ~47 | Crawler stopped writing dossiers. CSV still got Apr 20 entries, so the writer-of-md path is what broke. |

## Most actionable findings sitting unactioned (3-5 examples)

1. **Boomer Male 55-70 Faceless Affiliate thesis** (`auto_ops/alpha_theses/BOOMER_MALE_55_70_AFFILIATE.md`, Mar 18) — Filed P0 IMMEDIATE, "zero upfront cost, $10-30K/mo potential, demo arbitrage that nobody is competing for." 28K of executable detail: affiliate program table with commissions, Facebook Group seeding playbook, content tone shift, 7 cross-venture pollinations. Never spun up. Status hasn't been touched in 58 days.

2. **PEMF bootstrap to first dollar** (`RESEARCH/PEMF_BOOTSTRAP_CAPITAL_GENESIS.md`, Feb 7) — Explicit $451-1,051 path to first sale: $62 personal build, $250 first 2 sellable units, $139-639 legal/Shopify, first customer $0-100 via r/PEMF + YouTube build series. 77% gross margin on first sale ($539 on a $699 unit). Entire 17-doc research suite supporting this. Sitting cold for 97 days.

3. **Cal-AI-Style Paywall Optimization Service (MM018)** (`RESEARCH_NEW_METHODS_2026.md`) — 2.9x conversion boost data from RevenueCat, $3-15K/mo retainer model, 5-client target. Defined Jan 24, never built into a service offering. App-factory pipeline does "weekly + annual + rescue offer" but the SERVICE version (for clients) hasn't been productized.

4. **30+ video tools comparison + $0 stack** (`10_RESEARCH/VIDEO_RESEARCH/comparisons/MASTER_VIDEO_TOOLS_2026.md`, Mar 22) — Active intel: 25-40 free videos/day at $0 using Kling 3.0 (4K free tier) + Veo 3.1 + Wan 2.6 self-host + Hailuo. Concrete numbers, fresh as of March. ai_video_content_pipeline.py is supposed to use this but I see no recent video-output evidence.

5. **9,441-method Priority Stack is unfiltered for actionability** — May 6 stack shows 0 P0, 820 P1. P1 list reads like a wall of CONTENT_FARM noise — 95% of the top 50 entries are tweet/post fragments scored as if they were ventures. The ranker is grading raw alpha text as if it were a method. The signal is lost in the volume. `/goal` would drown if it pointed users here without a stricter filter.

## Duplication between 10_RESEARCH and RESEARCH

There is no overlap between the two directories. `10_RESEARCH/` is multi-niche / multi-tool research; `RESEARCH/` is the single-venture PEMF dump. The naming collision is dangerous though:

- `10_RESEARCH/` — sorted into ordered project numbering (01_STRATEGY, 09_LEGAL, 10_RESEARCH). This is the canonical location per `.claude/rules/file-locations.md`.
- `RESEARCH/` — escaped the numbering, just sat at root since Feb 7-8 when the PEMF venture was scoped. Functionally orphan.

The real duplication is elsewhere:
- **PEMF research vs. Capital Genesis ranker**: PEMF is one of the highest-ROI low-effort plays in the entire system (77% margin, $451-1K bootstrap) — yet I'd bet the Priority Stack ranks it below 9,000 generic tweet fragments because the ranker doesn't know it has a finished playbook.
- **Niche content research vs. competitor research**: `NICHE_CONTENT_RESEARCH_2025_2026.md` (root) and `10_RESEARCH/competitors/*` overlap on pricing tables, sound trends, ad creative formats for faith / fitness / focus / wellness. Two different snapshots of the same data, neither one currently fresh.

## Top 3 Risks (research that's already gone stale, paths that should be auto-archived)

1. **PEMF research suite (530K, 17 docs)** is the highest-ROI orphan in the system. Stale 97 days. If the venture isn't being run, archive it to `ARCHIVE/RESEARCH_PEMF/` so it doesn't pollute the manifest. If it IS being run, the Priority Stack should pin it. Right now it's neither.
2. **`10_RESEARCH/competitors/*` pricing data is 4 months stale**. Hallow / Pray.com / Calm / Headspace pricing tables are referenced by `app-factory-pipeline.md` for paywall benchmarking. Subscription pricing churns more than that — Calm hit $16.99/mo last year. Decisions on app pricing are running off out-of-date competitor tables.
3. **Crawler writer-half broke around Mar 29**. The CSV got updates through Apr 20, but the per-method dossier writer stopped. That means downstream consumers reading `auto_ops/discovered_methods/*.md` for context (CEO agent, growth plan generation) are seeing 47-day-old discoveries when the system thinks the pipeline is live. Silent failure.

## Top 3 Opportunities (research worth elevating into /goal's decision input)

1. **`auto_ops/alpha_theses/`** is the right unit of decision input. ONE file = ONE thesis = full Capital Genesis scoring + cross-pollination map + affiliate table + tone/platform/cadence + execution steps. We have one (Boomer Male). `/goal` should surface this directory and demand the system produce 8-12 of these (one per venture lane). This is the "synthesized for decision" layer the system is missing.
2. **`OPS/CAPITAL_GENESIS_PRIORITY_STACK.md`** as `/goal`'s default landing query, BUT with stricter pre-filter. Show only methods that have a matching alpha thesis or an `auto_ops/playbooks/` entry — i.e. methods with execution context. Drop the 9,000 unfiltered tweet fragments. Pre-filter from 9,441 -> ~30 actionable.
3. **`OPS/alpha_research/SOCIAL_MEDIA_AUTOMATION_STACK_2026-04-17.md` + `CONTAINERIZED_ACCOUNTS_INFRASTRUCTURE_2026-04-17.md`** are two deep-research reports from April that haven't been referenced anywhere downstream. The containerized-accounts research has cost tables on GoLogin / Multilogin / mobile proxies that directly enable the multi-account boomer-male strategy. Connecting these is a 30-min wiring job that unlocks the boomer thesis from "filed P0" to "executable today."

## For the /goal long-run command

- **Should /goal query existing research? Trigger new research? Both?** Both, but asymmetrically. Default mode: query existing. Trigger new research ONLY when the existing answer is older than X days for that decision class, OR when the user's goal explicitly references something not in the Priority Stack / alpha_theses / discovered_methods.
  - Decision class -> staleness threshold:
    - Pricing / competitor data: 30 days (currently 115 days stale — would trigger)
    - Tool stack (video, scraping, payments): 14 days (VIDEO_RESEARCH at 54 days — would trigger)
    - Capital Genesis ranking: 24 hours (currently fresh — would skip)
    - Method discoveries: 7 days (crawler dossiers at 47 days — would trigger)
    - Alpha theses: 30 days (Boomer at 58 days — would trigger a "still valid?" check, not a full rewrite)

- **Which specific research outputs should /goal surface to the user?** In this priority order:
  1. `auto_ops/alpha_theses/*.md` (full theses) — this is the single most decision-ready format.
  2. `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` filtered to the top 10-20 methods with thesis/playbook backing.
  3. `OPS/alpha_research/*` (deep-research reports) when goal aligns to their topic (social media stack, containerized accounts, open source money tools).
  4. `auto_ops/discovered_methods/*.md` (recent, last 14 days) — but only if their composite score >= 6.5 AND they have a real method (filter out the tweet-fragment noise).
  5. `10_RESEARCH/VIDEO_RESEARCH/comparisons/MASTER_VIDEO_TOOLS_2026.md` when goal touches video production.
  6. `RESEARCH/PEMF_*.md` ONLY when goal explicitly names PEMF or hardware product.
  7. Root-level research files: deprioritize. Either re-run them quarterly or archive.

- **What /goal must NOT do**: list the raw 9,441 Priority Stack methods. List the 5,169 METHOD_DISCOVERY_LOG.csv rows. Surface UAF_*.txt cognitive-architecture dumps. These flood the decision interface and obscure the 5-10 thesis-grade research outputs that actually drive action.

- **Wiring gap to close before /goal ships**: `actionable_aggregator.py` reads tracker / tactical plan / meta review / swarm reports / CEO decisions — but NOT `auto_ops/alpha_theses/`, NOT `OPS/alpha_research/`, NOT the Priority Stack. /goal will only feel "smart" if those three sources also reach the ACTIONABLE_QUEUE. Three-line patch to the aggregator.
