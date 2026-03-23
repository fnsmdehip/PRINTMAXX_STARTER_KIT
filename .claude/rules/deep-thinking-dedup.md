# Deep Thinking & Deduplication Gate (ALWAYS active before creating anything)

## The Problem This Solves
The autonomous_integrator V2 processed 294 alpha entries and created 294 DAG configs + 294 stub runners + 90 handoff chains + 589 growth plans. Zero of them execute. All are structurally unique at the text level but functionally repetitive at the pattern level. 46% of DAGs are CONTENT-type with no revenue path. 52% of handoff chains start with the identical scraper->qualifier pattern. Growth plans route 85%+ of actions to the same 3 tools. This is volume theater, not integration.

## Pre-Creation Gate (run BEFORE writing any new config, plan, DAG, chain, or script)

### 1. DEDUP CHECK (mandatory, no exceptions)
Before creating a new automation artifact, answer these three questions:
- **Does an existing Python script already do this?** Check the 601 real scripts in AUTOMATIONS/ first. Scraping? We have 37 scrapers. Content? 16 generators. Leads? 27 outreach scripts. If yes, WIRE INTO THE EXISTING SCRIPT instead of creating a new config file.
- **Does an existing playbook/guide/resource already cover this?** Check `OPS/RESOURCE_MANIFEST.md` FIRST — it indexes 200+ playbooks, products, guides, templates, and research docs. If a playbook exists, LOAD IT and use it rather than creating a new strategy from scratch.
- **Does an existing DAG/chain already cover this pattern?** The system has 294 DAGs. If the new method is "scrape X, score Y, generate content, post it" — that pattern exists 100+ times. Don't create #295. Find the closest existing one and ENHANCE it.
- **Will this actually execute?** If the output is a JSON config + a stub runner that prints "DAG execution complete" — it's not integration, it's a plan file. Plans are Level 1 (PLANNED). Don't count them as done.

### 2. FUNCTIONAL EQUIVALENCE TEST
Two methods are functionally equivalent if they:
- Use the same tool chain (scrape -> score -> generate -> post)
- Differ only in the target niche or data source
- Would share >70% of their actual code if implemented

If functionally equivalent to an existing integration, the correct action is:
- Add the new niche/source as a PARAMETER to the existing script
- Don't create new files. Parameterize.

### 3. REVENUE REALITY CHECK
Before creating integration artifacts, classify honestly:
- **REAL METHOD** ($100+/mo potential, executable steps, clear revenue path): Full integration — script + cron + KPI tracking
- **CONTENT SEED** ($0-50/mo, engagement bait, no direct revenue): Route to engagement_bait_converter ONLY. No DAG. No handoff chain. No growth plan. One function call.
- **INTELLIGENCE** (research, competitive intel, no method): File in RESEARCH directory. No automation. No growth plan.
- **NOISE** (crypto whale alerts, stock tips, lifestyle flexes): REJECT. Don't even create a growth plan.

Current reality: 186 growth plans (31%) are CONTENT-venture-zero-revenue. These should have been one-line routes to engagement_bait_converter, not 50-line markdown files with budget tiers.

### 4. TOOL ROUTING (use the RIGHT tool, not every tool)
| Need | Right tool | Wrong tool |
|------|-----------|------------|
| Connect two APIs | n8n workflow JSON | Python script |
| Scrape + process data | Existing scraper + new config | New DAG + stub runner |
| Generate content from method | engagement_bait_converter.py | New growth plan + new DAG |
| Multi-step pipeline | Enhance existing handoff chain | Create 90th chain with scraper->qualifier->X |
| Validate inputs | Hook in settings.json | New Python script |
| Schedule recurring task | Cron entry on existing script | New DAG runner stub |
| Score/rank methods | capital_genesis_ranker.py | New scoring script |

### 5. CONSOLIDATION OVER CREATION
When the integrator encounters 10 methods that are all "scrape [platform], find [opportunity], generate [content], post [everywhere]":
- Create ONE parameterized pipeline script with a config file listing the 10 variants
- NOT 10 DAG configs + 10 stub runners + 10 handoff chains + 10 growth plans = 40 files that do nothing

### 6. THE THREE-LEVEL HONESTY TEST (from end-to-end-verification.md)
Before reporting anything as "integrated":
1. **PLANNED** = config/JSON exists. This is what 294 DAGs + 90 chains are. Say so.
2. **BUILT** = executable code exists that actually does the work. Stubs don't count.
3. **VERIFIED** = code ran at least once and produced expected output.
Only Level 3 is "done." The integrator MUST label its output honestly.

### 7. MERGE CANDIDATES (apply before next integration run)
These should be merged into parameterized scripts, not kept as separate configs:
- All OUTBOUND chains (18) → single `outbound_pipeline.py` with lead source configs
- All CONTENT DAGs (137) → engagement_bait_converter.py already handles this
- All scraper->qualifier->connector chains (34) → single `lead_qualify_connect.py`
- All "post on Reddit, do SEO, cold email" growth plans → single growth template with venture-specific params

### 8. KILL LIST (safe to delete)
- 294 dag_runner_*.py stub files in AUTOMATIONS/ (they all print "DAG execution complete" and exit)
- Growth plans with $0/mo + empty tactics + REJECT markers (~234 files, 40% of total)
- Handoff chains that duplicate existing scripts' functionality

### 9. BEFORE EVERY `autonomous_integrator.py` RUN
Add this pre-flight check:
```
1. Count existing DAG configs. If >50, STOP. Consolidate before adding more.
2. Count existing growth plans. If >100, STOP. Merge by venture type.
3. Count dag_runner stubs. If any exist, convert to real scripts or delete.
4. For each new entry: grep existing scripts for the core verb (scrape, post, email, score).
   If 3+ scripts already do this verb: ENHANCE, don't create.
5. Revenue reality check on every entry before integration begins.
```

## Anti-Patterns This Rule Kills
- Creating 294 identical-structure configs instead of 1 parameterized pipeline
- Generating growth plans for rejected/zero-revenue entries
- Counting plan files as "integrated assets"
- Building handoff chain JSONs without an executor
- Routing engagement bait through full venture integration instead of one converter call
- Creating DAG configs for methods that existing scripts already handle
