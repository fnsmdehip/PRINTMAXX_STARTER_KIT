# Sovrun × Master Ops Integration Map

Generated: 2026-03-19 | Source: PRINTMAXX_MASTER_OPS_ENHANCED (181 ops, 14 sheets)

## P0 — Deploy This Week (15 ops)

| OP_ID | OP_NAME | Enhancement | Sovrun Module | New n8n Workflow? |
|---|---|---|---|---|
| N61 | Nationwide Local Biz Website Redesign | handoff chain: scraper→scorer→outreach→closer | handoff.py + workflow_bridge.py | w01 (GMaps) already built |
| D01 | Gumroad Digital Product Store | crash recovery for batch listing | durable.py | w14 (Stripe delivery) already built |
| N02 | Faceless YouTube Channel (Golf/Fishing) | DAG parallel: script gen + thumbnail gen + SEO | orchestration.py | w20 (YouTube upload) needed |
| N12 | Newsletter + Beehiiv Setup | content repurposing pipeline | workflow_bridge.py | w09 (content repurpose) already built |
| S02 | Local Biz Automation Service (EAS) | full handoff chain: lead→qualify→pitch→close→deliver | handoff.py | w01+w02 already built |
| C12 | Boomer Male 55-70 Affiliate | n8n workflow for affiliate link tracking + Facebook posting | workflow_bridge.py | NEW: w24 needed |
| S01 | Claude Code Freelance Arbitrage | procedural memory for proposal templates | procedural_memory.py | No |
| N01 | Twitter/X Content Machine | skill docs from past viral posts | procedural_memory.py | No |
| N13 | Cold Email Outreach Engine | SendGrid workflow already built | workflow_bridge.py | w04 already built |
| I05 | Reddit Pain Point Mining | n8n workflow already built | workflow_bridge.py | w13 already built |
| G01 | SEO Programmatic Pages | DAG parallel: keyword research + page gen + deploy | orchestration.py | No |
| G04 | Affiliate Link Optimization | crash recovery for batch processing | durable.py | No |
| G12 | Cross-Platform Content Distribution | content repurposing workflow | workflow_bridge.py | w09 already built |
| N68 | Ramadan Fasting Tracker PWA | already deployed, needs Stripe webhook | workflow_bridge.py | w14 already built |
| P01 | AI Persona Content Factory | parallel persona generation | orchestration.py | No |

## P1 — Deploy This Month (50 ops)

### Content (C01-C18)
| OP_ID | OP_NAME | Enhancement | Module |
|---|---|---|---|
| C01 | TikTok Content Farm | procedural memory for hook patterns | procedural_memory.py |
| C02 | YouTube Automation (Faceless) | DAG: script→voice→edit→thumbnail→upload | orchestration.py |
| C04 | Twitter Thread Factory | skill docs from high-engagement threads | procedural_memory.py |
| C05 | Newsletter Pipeline | handoff: content_gen→editor→scheduler | handoff.py |
| C08 | Viral Content Scanner | tracing for which content types convert | tracing.py |

### Services (S04-S18)
| OP_ID | OP_NAME | Enhancement | Module |
|---|---|---|---|
| S04 | Voice AI Automation (Bland.ai) | n8n workflow for call routing + CRM | workflow_bridge.py |
| S05 | Vertical SaaS Builder | crash recovery for multi-day builds | durable.py |
| S08 | Cold Outreach at Scale | handoff: lead_scrape→enrich→personalize→send→track | handoff.py |

### Digital Products (D02-D12)
| OP_ID | OP_NAME | Enhancement | Module |
|---|---|---|---|
| D02 | Whop Digital Store | sales webhook pipeline | workflow_bridge.py |
| D05 | Prompt Pack Store | procedural memory for best-selling prompt patterns | procedural_memory.py |

### Apps (A01-A04)
| OP_ID | OP_NAME | Enhancement | Module |
|---|---|---|---|
| A01 | PWA Factory | DAG: design→build→test→deploy→ASO (parallel where possible) | orchestration.py |
| A02 | Chrome Extension Factory | crash recovery for build pipeline | durable.py |

## New n8n Workflows Needed

| ID | Name | What It Does | Venture |
|---|---|---|---|
| w20 | YouTube Auto-Upload | Webhook receives generated video → uploads to YouTube via API → sets title/description/tags/thumbnail → schedules publish | C02, N02 |
| w21 | Bland.ai Call Router | Inbound call → Bland.ai answers → qualifies lead → routes to CRM → sends Telegram alert | S04, S02 |
| w22 | A/B Test Data Collector | Cron collects engagement metrics from multiple platforms → aggregates in Sheets → identifies winners → triggers scale-up workflow | G01, C01 |
| w23 | Telegram Command Center | Telegram bot receives commands → routes to appropriate PRINTMAXX agent via webhook → returns results | ALL |
| w24 | Facebook Group Poster | Cron → generates boomer-friendly content via claude -p → posts to Facebook Groups via Graph API → tracks engagement | C12 |

## Agent Handoff Chains

### Chain 1: Local Biz Pipeline (N61 + S02)
```
savvy_lead_scraper → lead_enrichment → eas_lead_pipeline → cold_email_generator → follow_up_tracker → close_tracker
```
Each step hands off context (lead data, enrichment results, email draft) to the next via handoff.py.

### Chain 2: Content Factory (C01-C12)
```
alpha_scanner → topic_selector → content_generator → voice_injector → platform_formatter → scheduler
```
Intelligence router feeds alpha → agent picks best topic → generates content → voice model ensures user's tone → formats per platform → schedules posts.

### Chain 3: Product Launch (D01-D12)
```
demand_scanner → product_builder → listing_creator → distribution_engine → sales_tracker
```
Scans for demand signals → builds digital product → creates listing on Gumroad/Whop → distributes via email/social → tracks sales via Stripe webhook.

### Chain 4: Freelance Pipeline (S01)
```
job_scanner → proposal_writer → submission_tracker → delivery_manager → review_collector → upsell_generator
```
Procedural memory injects winning proposal templates at step 2.

### Chain 5: Alpha-to-Revenue (ALL)
```
scraper_fleet → alpha_processor → intelligence_router → capital_genesis_ranker → venture_autonomy → execution_agent
```
This is the master chain. Everything feeds into it. The ranker decides priority, venture_autonomy picks the best execution path.

### Chain 6: Brokering Pipeline (BROKERING venture type)
```
target_scraper → lead_qualifier → service_matcher → intro_drafter → cold_emailer → follow_up_tracker → referral_closer → revenue_tracker
```
**Handoff chain:** Each step passes enriched lead data to the next via handoff.py.

- **target_scraper**: savvy_lead_scraper.py / nationwide_scraper.py scrape businesses needing services (equipment, loans, processing, insurance). Output: broker_targets.csv
- **lead_qualifier**: Score leads 1-10 on deal size, urgency, fit. Enrich via Apollo/Clearbit. Move 7+ to qualified_broker_leads.csv
- **service_matcher**: Match qualified leads to best service provider (lender, broker, vendor, agent) from provider database
- **intro_drafter**: Generate warm intro email for both parties using cold email templates adapted for brokering
- **cold_emailer**: n8n w04 (SendGrid) sends intro emails. CAN-SPAM compliant.
- **follow_up_tracker**: Auto follow-up Day 3/5/7. Track opens, replies, meetings booked.
- **referral_closer**: When deal progresses, send referral agreement. Track deal value.
- **revenue_tracker**: Log referral fees to LEDGER/BROKERING_REVENUE.csv. Feed into Capital Genesis ranker.

**Sovrun modules used:**
- `handoff.py` — context passing between pipeline steps
- `workflow_bridge.py` — n8n w25 (lead gen service), w26 (domain flipper), w27 (white-label reports)
- `procedural_memory.py` — capture winning intro email patterns and successful vertical plays
- `durable.py` — crash recovery for batch outreach operations

**n8n workflows:**
| ID | Name | What It Does | Verticals |
|---|---|---|---|
| w25 | Lead Gen Service | Scrape leads for client businesses → deliver via Google Sheets → charge monthly | All brokering verticals |
| w26 | Domain Flipper | Scan expiring domains with SEO value → alert on opportunities → track acquisitions | Domain arbitrage |
| w27 | White Label Reports | intelligence_router generates industry report → formats → delivers to client email | White-label reports |

**Verticals (rotate through):**
1. Real estate referrals (1-3% per deal)
2. Equipment financing brokerage ($500-5K per deal)
3. Merchant processing referrals (residual income)
4. Insurance referrals ($50-500 per referral)
5. SBA loan brokerage (1-2% origination fee)
6. Wholesale/distribution connecting (connector fee)
7. Lead gen as a service ($500-2K/mo per client)
8. White-label reports ($200-500 per report)

**Cross-pollination:**
- Feeds OUTBOUND (same cold email infra)
- Feeds SCRAPING (same scraper fleet)
- Feeds LOCAL_BIZ (same lead enrichment pipeline)
- Feeds EAS (brokering is a lighter version of EAS service delivery)
- Feeds PRODUCT (white-label reports are digital products)

## DAG Candidates (Currently Sequential, Should Parallel)

### 1. Morning Intelligence Pipeline
Currently: Twitter scraper (6AM) → Reddit scraper (6:15) → Alpha processor (6:30) → Sequential
Should be: All scrapers parallel → merge results → single alpha processing pass
```mermaid
graph TD
    A[Twitter Scraper] --> D[Alpha Processor]
    B[Reddit Scraper] --> D
    C[HN Scraper] --> D
    D --> E[Intelligence Router]
    E --> F[Capital Genesis Ranker]
    F --> G[CEO Agent]
```

### 2. Content Production
Currently: Generate text → generate image → format → post → Sequential
Should be: Text + image in parallel → format → post
Saves ~40% time per content batch.

### 3. Lead Gen + Outreach
Currently: Scrape → enrich → email → Sequential
Should be: GMaps + Apollo + Reddit scrape in parallel → merge → parallel email + LinkedIn + Telegram outreach

### 4. App Factory
Currently: Design → build → test → deploy → Sequential
Should be: Design + competitor research in parallel → build → test + ASO prep in parallel → deploy

## Procedural Memory Skill Categories (P0)

| Skill Category | Source Data | Benefit |
|---|---|---|
| proposal_writing | Past freelance proposals (S01 wins/losses) | 3x faster proposals with proven templates |
| cold_email_personalization | Past email campaigns (open rates, replies) | Higher response rates from patterns that worked |
| content_hook_patterns | Past viral content (engagement metrics) | Reuse hooks that got >1K engagement |
| app_listing_copy | Past ASO results (download rates) | Better app store descriptions from proven patterns |
| client_objection_handling | Past EAS sales conversations | Pre-built responses to common objections |

## Conflict Avoidance Rules

These existing systems must NOT be disrupted:
1. **Cron schedule** — don't overlap new crons with existing 112 entries
2. **CEO checkpoint** — DAG orchestration complements, doesn't replace CycleCheckpoint
3. **Resilience layer** — new modules import from resilience.py, don't reinvent
4. **Twitter warmup** — Day 2 of 21-day ramp, don't touch posting cadence
5. **Loop closer** — new skill capture hooks INTO loop_closer, doesn't replace it
6. **Intelligence router** — new workflows CONSUME router output, don't bypass it
7. **Control panel** — ONE dashboard rule still applies (localhost:9999)

## Tool Integration Decision Log (2026-03-19)

### SKIP (we already have better versions)
| Tool | Our Version | Why Skip |
|---|---|---|
| MoneyPrinterTurbo | auto_clip_pipeline.py + ai_video_content_pipeline.py | Ours has affiliate hooks, voice model injection, PRINTMAXXER copy style |
| ShortGPT | auto_clip_pipeline.py | Ours uses Claude for viral moment detection, theirs uses GPT |
| yt-dlp | Already installed, used in clip pipeline | Already integrated |

### WIRE IN (adds genuine value)
| Tool | What It Adds | Which Ventures |
|---|---|---|
| Postiz | 30+ platform scheduling (we only have Twitter + manual) | C01-C18 content ventures |
| Crawl4AI | LLM-friendly web crawling (cleaner than our custom scrapers for generic URLs) | Intelligence pipeline, alpha scraping |
| Polar | Self-hosted payment platform (replaces Gumroad dependency, better margins) | D01-D12 digital products |
| Freqtrade | Crypto trading backtesting (new capability) | I01-I05 investment ventures |
| listmonk | Self-hosted newsletter (replaces Beehiiv dependency) | N12 newsletter, C05 pipeline |
| Google Stitch | UI generation via browser control (when API available) | App factory, landing pages |

### HYBRID (combine best of both)
| Tool | Our Version | Hybrid Approach |
|---|---|---|
| Mautic | eas_lead_pipeline.py | Use Mautic CRM for EAS clients, our pipeline for PRINTMAXX internal leads |

## Unwired Money Methods (Wired 2026-03-20)

### API Arbitrage (MONEY_METHODS/API_ARBITRAGE/API_ARBITRAGE_PLAYBOOK.md)
- **Venture mapping:** BROKERING, APP_FACTORY, MONETIZATION
- **Sovrun module:** orchestration.py (DAG: API discovery -> MVP build -> Stripe checkout -> launch)
- **Revenue:** $500-10K/mo portfolio, 70-99% margins, $0 startup
- **Synergy:** Feeds MCP_MARKETPLACE (API wrappers as MCP servers), PRODUCT (micro-SaaS), CONTENT (build-in-public threads)

### MCP Marketplace (MONEY_METHODS/MCP_MARKETPLACE/LAUNCH.md + MONETIZATION.md)
- **Venture mapping:** APP_FACTORY, PRODUCT, MONETIZATION
- **Sovrun module:** durable.py (crash recovery for directory scraping), workflow_bridge.py (hosting affiliate tracking)
- **Revenue:** Featured $29/mo, verified $9/mo, enterprise $99/mo, hosting affiliate. $5.6K/mo at 1K servers.
- **Synergy:** Feeds API_ARBITRAGE (API wrappers sold as MCP servers), CONTENT (weekly MCP roundup newsletter)

### GitHub Repurpose Strategy (MONEY_METHODS/GITHUB_REPURPOSE_STRATEGY.md)
- **Venture mapping:** APP_FACTORY, PRODUCT, RESEARCH
- **Sovrun module:** procedural_memory.py (capture winning splice patterns), tracing.py (track which repos yielded best code)
- **Revenue:** Saves $3.5-7K per SaaS build. Accelerates APP_FACTORY 10x.
- **Synergy:** Feeds APP_FACTORY (faster builds), API_ARBITRAGE (splice auth + payments from proven repos)

### POD / TikTok Arbitrage (MONEY_METHODS/POD_TIKTOK_ARBITRAGE_AUDIT.md)
- **Venture mapping:** CONTENT, MONETIZATION, PRODUCT
- **Sovrun module:** orchestration.py (DAG: design gen -> mockup -> listing -> cross-post), workflow_bridge.py (Etsy/Redbubble listing)
- **Revenue:** POD $1K-3K/mo at 150+ designs, TikTok Shop $1K/mo at Month 3, content cross-post RPM $200/mo
- **Synergy:** Feeds CONTENT (product review videos), MONETIZATION (affiliate commissions), 7 revenue touchpoints per video

### Synergies/Tools/Missing Audit (MONEY_METHODS/SYNERGIES_TOOLS_MISSING_AUDIT.md)
- **Venture mapping:** ALL (cross-cutting)
- **Coverage:** 10 synergy stacks, 5 tool listicles (50 tools), 40 missing method directories, 5 bundle product concepts ($47-297)
- **Synergy:** Feeds PRODUCT (bundle concepts ready to list), CONTENT (tool listicles as threads), MONETIZATION (method stacking)

### Affiliate Research Mar 2026 (MONEY_METHODS/AFFILIATE_RESEARCH_MAR18.md)
- **Venture mapping:** CONTENT, MONETIZATION
- **Top programs:** Beehiiv 50% (60d cookie), SEMrush $200-450 (120d cookie), Instantly 20-40%, Kit 50%+lifetime, Smartlead 15-35% lifetime
- **Revenue:** Base $3.9K/yr, Bull $15.6K/yr from existing pages
- **Synergy:** 8 comparison pages LIVE on surge.sh need real affiliate IDs swapped in. Single highest-ROI human action.
| Crawl4AI + our scrapers | Platform-specific scrapers (Twitter, Reddit) | Use our scrapers for authenticated/platform-specific, Crawl4AI for generic web crawling |
