# MASTER FILE AUDIT - PRINTMAXX Project

**Generated:** 2026-02-12
**Purpose:** Complete inventory of every file in the project, grouped by domain, with duplicates, orphans, and consolidation opportunities flagged.

---

## EXECUTIVE SUMMARY

| Metric | Count |
|--------|-------|
| **Top-level directories** | 35+ (many are DUPLICATES of each other) |
| **Estimated total files** | 800,000+ (most are node_modules bloat) |
| **Meaningful content/code files** | ~2,500+ |
| **Files NOT in CLAUDE.md navigation** | ~1,000+ |
| **Duplicate/overlapping file sets** | 15+ groups identified |
| **Legacy/deletable directories** | 8 identified |
| **Empty directories** | 6 (clips, EMAIL, LEGAL, logs, output, tasks, RESEARCH, MASTER_DOC) |

### CRITICAL FINDING: PARALLEL DIRECTORY STRUCTURES

The project has TWO parallel directory hierarchies that duplicate each other:

**Hierarchy A (numbered, OLD):**
- `01_STRATEGY/` = mirrors content in `OPS/` and root-level strategy files
- `02_TRACKING/` = mirrors `LEDGER/` and `FINANCIALS/`
- `03_PLAYBOOKS/` = mirrors `MONEY_METHODS/` (779K files due to node_modules)
- `04_CONTENT/` = mirrors `CONTENT/`
- `05_AUTOMATION/` = mirrors `AUTOMATIONS/`
- `06_OPERATIONS/` = active, has unique content (growth/, gtm/, setup/, trend_intel/)
- `07_LANDING/` = mirrors `LANDING/`
- `08_PRODUCTS/` = mirrors `PRODUCTS/` (6 files)
- `09_LEGAL/` = mirrors `LEGAL/` (24 files)
- `10_RESEARCH/` = mirrors `RESEARCH/` (29 files)

**Hierarchy B (named, CURRENT):**
- `OPS/`, `LEDGER/`, `MONEY_METHODS/`, `CONTENT/`, `AUTOMATIONS/`, `LANDING/`, `PRODUCTS/`, `FINANCIALS/`, `LEGAL/`, `RESEARCH/`

**The numbered directories (01-10) appear to be the ORIGINAL structure, while the named directories are the CURRENT working structure. The FOLDER_REORGANIZATION_PLAN.md exists but was NEVER FULLY EXECUTED.**

---

## SECTION 1: DUPLICATE AND OVERLAPPING FILES (CONSOLIDATE THESE)

### 1.1 COLD EMAIL/OUTBOUND (6+ locations)

| File/Dir | Location | Notes |
|----------|----------|-------|
| EMAIL_SEQUENCES_TIER1.md | `MONEY_METHODS/COLD_OUTBOUND/` | |
| TIER1_COLD_EMAIL_SEQUENCES.md | `MONEY_METHODS/COLD_OUTBOUND/` | DUPLICATE of above |
| COLD_EMAIL_LAUNCH_CHECKLIST.md | `OPS/` | |
| cold_email_playbook.md | `PRODUCTS/` | Product version |
| 05_cold_email_playbook.md | `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` | Another copy |
| 05_COLD_EMAIL_PLAYBOOK.md | `DIGITAL_PRODUCTS/ready_to_sell/` | Yet another copy |
| cold_email_sequences_ready.csv | `AUTOMATIONS/content_posting/` | |
| cold_email_subject_lines_100.csv | `AUTOMATIONS/content_posting/` | |
| COLD_EMAIL_INFRASTRUCTURE_GUIDE.md | `03_PLAYBOOKS/COLD_OUTBOUND/` | Old hierarchy |
| COLD_EMAIL_SEQUENCES_3_INDUSTRIES.md | `CONTENT/email_sequences/cold/` | |
| INDUSTRY_SEQUENCES_5.md | `CONTENT/email_sequences/cold/` | |
| cold_email_2026.py | `AUTOMATIONS/` | Script |
| generate_cold_emails.py | `AUTOMATIONS/` | Another script |
| mass_outreach.py | `AUTOMATIONS/` | Another script |
| All outreach CSVs | `AUTOMATIONS/outreach/` | 30+ email CSV files |
| VA cold email scripts | `OPS/VA_SCRIPTS/` | |

**Recommendation:** Consolidate all cold email/outbound content into `MONEY_METHODS/COLD_OUTBOUND/` with subdirs for sequences, scripts, products, and templates.

### 1.2 ACCOUNT CREATION (5 locations)

| File | Location |
|------|----------|
| ACCOUNT_CREATION_CHECKLIST.md | `OPS/` |
| ACCOUNT_CREATION_MASTER_PROCESS.md | `OPS/` |
| ACCOUNT_CREATION_NOW.md | `OPS/` |
| T7_HUMAN_ACCOUNT_CREATION_MASTER.md | `ralph/loops/social_setup/output/` |
| ACCOUNT_CREATION_CHECKLIST.md | `06_OPERATIONS/setup/archive/` |
| auto_account_creator.py | `AUTOMATIONS/` |
| account_creation_helper.py | `AUTOMATIONS/` |
| account_tracker.py | `scripts/` |

**Recommendation:** Single source of truth at `OPS/ACCOUNT_CREATION_MASTER.md`. Delete duplicates.

### 1.3 GUMROAD PRODUCTS (5 locations)

| File | Location |
|------|----------|
| GUMROAD_READY_LISTINGS.md | `PRODUCTS/` |
| GUMROAD_LAUNCH_CHECKLIST.md | `OPS/` |
| GUMROAD_PRODUCT_SPECS.md | `06_OPERATIONS/gtm/` |
| GUMROAD_LAUNCH_EXECUTION_GUIDE.md | `DIGITAL_PRODUCTS/` |
| PRODUCT1-4 listings | `DIGITAL_PRODUCTS/listings/` |
| 01-13 product files | `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` |
| GUMROAD_LISTINGS_ENHANCED.md | `PRODUCTS/ECOM_LISTINGS_READY/` |
| GUMROAD_COVER_SPECS.md | `PRODUCTS/` |
| LISTING_METADATA.md | `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` |

**Recommendation:** Consolidate all Gumroad content into `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` as the single listing source.

### 1.4 SESSION HANDOFFS (8 files)

| File | Location |
|------|----------|
| SESSION_HANDOFF.md | Root (`/`) |
| SESSION_HANDOFF.md | `06_OPERATIONS/` |
| SESSION_HANDOFF_2026-02-02.md | `OPS/` |
| SESSION_HANDOFF_FEB3_2026.md | `OPS/` |
| SESSION_HANDOFF_FEB5_2026.md | `OPS/` |
| SESSION_HANDOFF_FEB5B_2026.md | `OPS/` |
| SESSION_HANDOFF_FEB6_2026.md | `OPS/` |
| SESSION_HANDOFF_FEB10_2026.md | `OPS/` |
| SESSION_HANDOFF_FEB10B_2026.md | `OPS/` |
| SESSION_HANDOFF_FEB12_2026.md | `OPS/` |
| SESSION_SUMMARY_FEB4_EVENING.md | `OPS/` |
| SESSION_SUMMARY_FEB4_LATE.md | `OPS/` |

**Recommendation:** Keep only the latest (FEB12). Archive old ones in `OPS/archive/handoffs/`.

### 1.5 ALPHA STAGING (10+ related files)

| File | Location |
|------|----------|
| ALPHA_STAGING.csv | `LEDGER/` (PRIMARY) |
| ALPHA_STAGING.csv | `02_TRACKING/alpha/` (DUPLICATE) |
| ALPHA_STAGING_APPEND_FEB2026.csv | `LEDGER/` |
| ALPHA_STAGING_BACKUP_20260205.csv | `LEDGER/` |
| ALPHA_STAGING_REPAIRED.csv | `LEDGER/` |
| ALPHA_STAGING.csv.backup_* | `LEDGER/` |
| ALPHA_STAGING.csv.bak_* | `LEDGER/` |
| ALPHA_BATCH2_FINAL.csv | `LEDGER/` |
| ALPHA_BATCH2_TEMP.csv | `LEDGER/` |
| + 28 snapshot directories | `LEDGER/.snapshots/` |

**Recommendation:** Keep `LEDGER/ALPHA_STAGING.csv` as sole source. Delete all backup/repair/append files. Snapshots are OK.

### 1.6 APP QUALITY / REJECTION (4 overlapping files)

| File | Location |
|------|----------|
| APP_QUALITY_STANDARDS.md | `MONEY_METHODS/APP_FACTORY/` |
| APP_QUALITY_AUDIT_REAL.md | `MONEY_METHODS/APP_FACTORY/` |
| IOS_REJECTION_PREVENTION.md | `MONEY_METHODS/APP_FACTORY/` |
| REJECTION_PREVENTION.md | `MONEY_METHODS/APP_FACTORY/` |
| IOS_SUBMISSION_PROCESS.md | `MONEY_METHODS/APP_FACTORY/` |

**Recommendation:** Merge REJECTION_PREVENTION and IOS_REJECTION_PREVENTION into one file.

### 1.7 AI AGENT/AUTOMATION SERVICES (2 near-identical)

| File | Location |
|------|----------|
| AI_AGENT_SERVICES_PLAYBOOK.md | `MONEY_METHODS/AI_AGENT_SERVICES/` |
| AI_AGENT_SERVICE_PLAYBOOK.md | `MONEY_METHODS/AI_AGENTS_SERVICE/` |

**Recommendation:** Delete one. Two directories with almost identical names and content.

### 1.8 POD DESIGNS (2 files, one supersedes)

| File | Location |
|------|----------|
| POD_DESIGNS_20.md | `PRODUCTS/` |
| POD_DESIGNS_50.md | `PRODUCTS/` |

**Recommendation:** POD_DESIGNS_50 supersedes. Delete POD_DESIGNS_20.

### 1.9 KDP JOURNALS (2 files)

| File | Location |
|------|----------|
| KDP_JOURNALS_5.md | `PRODUCTS/` |
| KDP_JOURNALS_10.md | `PRODUCTS/` |

**Recommendation:** KDP_JOURNALS_10 supersedes. Delete KDP_JOURNALS_5.

### 1.10 ETSY LISTINGS (3 locations)

| File | Location |
|------|----------|
| ETSY_LISTINGS_20.md | `PRODUCTS/` |
| ETSY_LISTINGS_ALL.md | `PRODUCTS/ETSY_INSTANT_UPLOAD/` |
| ETSY_LISTINGS_COMPLETE.md | `PRODUCTS/ECOM_LISTINGS_READY/` |
| ETSY_UPLOAD_READY_20.md | `PRODUCTS/ECOM_LISTINGS_READY/` |

**Recommendation:** Consolidate into `PRODUCTS/ETSY_INSTANT_UPLOAD/`.

### 1.11 REDBUBBLE LISTINGS (3 locations)

| File | Location |
|------|----------|
| REDBUBBLE_LISTINGS.md | `PRODUCTS/` |
| REDBUBBLE_LISTINGS_20.md | `PRODUCTS/ECOM_LISTINGS_READY/` |
| REDBUBBLE_UPLOAD_READY_20.md | `PRODUCTS/ECOM_LISTINGS_READY/` |

### 1.12 WHOP LISTINGS (3 locations)

| File | Location |
|------|----------|
| WHOP_LAUNCH_CHECKLIST.md | `OPS/` |
| WHOP_LISTINGS_1-8.md | `PRODUCTS/listings/` |
| WHOP_LISTINGS_01-08.md | `PRODUCTS/WHOP_INSTANT_UPLOAD/` |
| WHOP_LISTINGS_QUICK.md | `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` |

### 1.13 FIVERR (3+ locations)

| File | Location |
|------|----------|
| FIVERR_LAUNCH_CHECKLIST.md | `OPS/` |
| FIVERR_LAUNCH_PACKAGE.md | `OPS/` |
| FIVERR_GIGS_10.md | `PRODUCTS/FREELANCE_LISTINGS_READY/` |
| GIG_01-10 files | `PRODUCTS/FIVERR_INSTANT_UPLOAD/` |
| FIVERR_BORING_CATEGORY_GIGS.md | `PRODUCTS/listings/` |
| FIVERR_GOV_CONTRACT_CONSULTING.md | `PRODUCTS/listings/` |

### 1.14 TWITTER SCRAPERS (8+ overlapping scripts)

| File | Location |
|------|----------|
| twitter_alpha_scraper.py | `AUTOMATIONS/` |
| twitter_content_scraper.py | `AUTOMATIONS/` |
| twitter_scraper_live.py | `AUTOMATIONS/` |
| background_twitter_scraper.py | `AUTOMATIONS/` |
| daily_twitter_scraper.py | `AUTOMATIONS/` |
| enhanced_twitter_scraper.py | `AUTOMATIONS/` |
| headless_twitter_scraper.py | `AUTOMATIONS/` |
| parallel_twitter_scraper.py | `AUTOMATIONS/` |
| scrape_twitter_applescript.py | `AUTOMATIONS/` |
| scrape_twitter_selenium.py | `AUTOMATIONS/` |

**Recommendation:** Keep twitter_alpha_scraper.py as primary. Mark others DEPRECATED or delete.

### 1.15 REDDIT SCRAPERS (5+ overlapping scripts)

| File | Location |
|------|----------|
| reddit_alpha_scraper.py | `AUTOMATIONS/` |
| reddit_deep_scraper.py | `AUTOMATIONS/` |
| daily_reddit_scraper.py | `AUTOMATIONS/` |
| enhanced_reddit_scraper.py | `AUTOMATIONS/` |
| headless_reddit_scraper.py | `AUTOMATIONS/` |
| background_reddit_scraper.py | `AUTOMATIONS/` |

### 1.16 LOCAL BIZ PIPELINE (scattered docs)

| File | Location |
|------|----------|
| LOCAL_BIZ_PIPELINE_README.md | `AUTOMATIONS/` |
| LOCAL_BIZ_PIPELINE_SUMMARY.md | `AUTOMATIONS/` |
| LOCAL_BIZ_PIPELINE_DIAGRAM.txt | `AUTOMATIONS/` |
| LOCAL_BIZ_SCRAPER_INDEX.md | `AUTOMATIONS/` |
| LOCAL_BIZ_SCRAPER_QUICKSTART.md | `AUTOMATIONS/` |
| LOCAL_BIZ_SCRAPER_README.md | `AUTOMATIONS/` |
| LOCAL_BIZ_SCRAPER_SUMMARY.md | `AUTOMATIONS/` |
| LOCAL_BIZ_QUICK_START.md | `AUTOMATIONS/` |
| LOCAL_BIZ_EMAIL_TEMPLATES.md | `AUTOMATIONS/` |
| LOCAL_BIZ_SYSTEM_MAP.txt | `AUTOMATIONS/` |

**Recommendation:** All 10 of these docs should be ONE file: `MONEY_METHODS/LOCAL_BIZ/PIPELINE_GUIDE.md`.

### 1.17 CLIP PIPELINE (5 overlapping docs)

| File | Location |
|------|----------|
| CLIP_PIPELINE_INDEX.md | `AUTOMATIONS/` |
| CLIP_PIPELINE_INTEGRATION.md | `AUTOMATIONS/` |
| CLIP_PIPELINE_QUICKSTART.md | `AUTOMATIONS/` |
| CLIP_PIPELINE_SUMMARY.md | `AUTOMATIONS/` |
| CLIP_PIPELINE_FLOW_DIAGRAM.txt | `AUTOMATIONS/` |
| AUTO_CLIP_PIPELINE_README.md | `AUTOMATIONS/` |
| auto_clip_pipeline.py | `AUTOMATIONS/` |
| clip_automation_pipeline.py | `AUTOMATIONS/` |
| clip_post_scheduler.py | `AUTOMATIONS/` |

**Recommendation:** Consolidate docs into single `MONEY_METHODS/CLIPPING_SERVICE/PIPELINE_GUIDE.md`.

---

## SECTION 2: ORPHANED FILES NOT IN CLAUDE.md

### 2.1 Root-level orphans (should be in proper directories)

| File | Status |
|------|--------|
| `app guide.rtf` | ORPHAN - no reference anywhere |
| `hyper rat soft engin.rtf` | ORPHAN - appears to be user notes |
| `iuhkm.csv.rtf` | ORPHAN - unclear purpose |
| `landind page prtopmt.rtf` | ORPHAN - user notes for landing page prompt |
| `money methods and sub category methods to add.rtf` | ORPHAN - user notes |
| `comprehensive_results.csv` | ORPHAN - should be in LEDGER/ |
| `ecom_arb_opportunities.csv` | ORPHAN - should be in LEDGER/ |
| `NEW_APP_FACTORY_ALPHA_FEB_2026.csv` | ORPHAN - should be in LEDGER/ |
| `update_ledger.py` | ORPHAN - should be in scripts/ |
| `deploy_all_apps.sh` | ORPHAN - duplicated in AUTOMATIONS/ |
| `deploy_apps.py` | ORPHAN - should be in scripts/ |
| `deploy_surge_quick.sh` | ORPHAN - should be in scripts/ |
| `CAPITAL_GENESIS_EXECUTION_SUMMARY.md` | ORPHAN - should be in 01_STRATEGY/ |
| `CLAUDE_CODE_SETUP.md` | ORPHAN - not referenced |
| `DAY1_EXECUTION.md` | ORPHAN - not referenced |
| `HANDOFF_NEXT_CHAT.md` | ORPHAN - superseded by OPS handoffs |
| `NEW_METHODS_SUMMARY_2026-01-24.md` | ORPHAN - not referenced |
| `PELVICPRO_SDK54_UPGRADE_COMPLETE.txt` | ORPHAN - different project? |
| `PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.docx` | ORPHAN |
| `PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.js` | ORPHAN |
| `PRINTMAXX_MASTER_OPS_BACKUP.xlsx` | Backup of main XLSX |
| `PRINTMAXX_OPS_PLAYBOOK_BACKUP.xlsx` | Backup of main XLSX |
| `PRINTMAXX_SYSTEM_AUDIT_FEB9_2026.docx` | ORPHAN |
| `PRINTMAXX_SYSTEM_AUDIT_FEB9_2026.js` | ORPHAN |
| `RBI_AND_AUTOMATION_ANALYSIS.md` | ORPHAN - should be in OPS/ |
| `README_ADDENDUM_PARALLEL_AGENT_LAUNCH.md` | ORPHAN |
| `RESEARCH_NEW_METHODS_2026.md` | ORPHAN - should be in OPS/ |
| `SESSION_DELIVERABLES_2026_02_04.md` | ORPHAN - should be in OPS/ |
| `SESSION_HANDOFF.md` | ORPHAN - duplicated in OPS/ |
| `START_HERE.md` | ORPHAN |
| `WHATS_BEEN_BUILT.md` | ORPHAN |
| `YOUR_MANUAL_TASKS.md` | ORPHAN |
| `.~lock.*.xlsx#` files (8) | LibreOffice lock files - DELETE |

### 2.2 MONEY_METHODS orphans (not in CLAUDE.md nav)

| File | Not in CLAUDE.md |
|------|-----------------|
| `AI_AGENT_SERVICES/AI_AGENT_SERVICES_PLAYBOOK.md` | Missing |
| `AI_AGENTS_SERVICE/AI_AGENT_SERVICE_PLAYBOOK.md` | Missing (duplicate dir) |
| `AI_INFLUENCER/AI_NSFW_EXECUTION_FULL.md` | Missing |
| `AI_INFLUENCER/AI_VIDEO_TOOLS_COMPARISON.md` | Missing |
| `AI_INFLUENCER/NSFW_STATUS_AUDIT.md` | Missing |
| `API_ARBITRAGE/API_ARBITRAGE_PLAYBOOK.md` | Missing |
| `APP_FACTORY/ANDROID_CLONE_SPECS.md` | Missing |
| `APP_FACTORY/APP_DISCOVERY_ENGINE.md` | Missing |
| `APP_FACTORY/APP_STORE_AUDIT_FEB2026.md` | Missing |
| `APP_FACTORY/CLONECHART_DATA_EXTRACT.md` | Missing |
| `APP_FACTORY/COMPETITOR_REAL_DATA.md` | Missing |
| `APP_FACTORY/IOS_SUBMISSION_PROCESS.md` | Missing |
| `APP_FACTORY/NOFAP_KARMAMAXX_APP_SPEC.md` | Missing |
| `APP_FACTORY/VIBE_CODING_5_APPS_PLAN.md` | Missing |
| `APP_FACTORY/builds/robloxmaxx/` (entire dir) | Missing - full Roblox app |
| `APP_FACTORY/builds/roblox_tycoon/` (entire dir) | Missing |
| `APP_FACTORY/builds/biomaxx-sdk54/` | Missing |
| `AUTOMATION_AGENCY/AUTOMATION_AGENCY_PLAYBOOK.md` | Missing |
| `COMMUNITY/COMMUNITY_MONETIZATION_PLAYBOOK.md` | Missing |
| `CONTENT_FARM/FB_REELS_GTM.md` | Missing |
| `CONTENT_FARM/SLEEP_YOUTUBE/` (4 files) | Missing |
| `CONTENT_FARM/YOUTUBE_AI_AUTOMATION_PLAYBOOK.md` | Missing |
| `CONTENT_FARM/YOUTUBE_AUTOMATION_DUE_DILIGENCE.md` | Missing |
| `DIGITAL_PRODUCTS/INFO_PRODUCT_OPS_STRATEGY.md` | Missing |
| `ECOM_ARB/NORDIC_ECOM_PLAYBOOK.md` | Missing |
| `GOVERNMENT_CONTRACTS/GOVERNMENT_CONTRACTS_OP.md` | Missing |
| `PLATFORM_ARBITRAGE/ECOM_ARB_PLAYBOOK.md` | Missing |
| `PLATFORM_ARBITRAGE/FB_REELS_CROSSPOST_PLAYBOOK.md` | Missing |
| `PLATFORM_ARBITRAGE/POD_TRENDING_PHRASES.md` | Missing |
| `PREDICTION_MARKETS/PREDICTION_MARKET_ARB_PLAYBOOK.md` | Missing |
| `PROMPT_MARKETPLACE/PROMPT_MARKETPLACE_PLAYBOOK.md` | Missing |
| `SYNERGY_PACKAGES/` (entire dir, 17 files) | Missing |
| `SYNERGY_STACKS/` (entire dir, 5 files) | Missing |
| `TIKTOK_SHOP/AFFILIATE_GTM.md` | Missing |
| `TOOL_ALPHA/MCP_SERVER_BUILD_PLAN.md` | Missing |

### 2.3 OPS orphans (not in CLAUDE.md nav)

**Over 100 files in OPS/ not referenced in CLAUDE.md.** Key ones:

| File | Description |
|------|-------------|
| `OPS/analytics/` (6 files) | AB testing, analytics, conversion, pricing guides |
| `OPS/automation/` (8 files) | Automation workflows, MCP roadmap, vibe coding |
| `OPS/BROWSER_CONTROL/` (3 files) | Browser agent guides |
| `OPS/CONTENT_QA_QUEUE/` (150+ files) | Content pending review - massive backlog |
| `OPS/content/` (16 files) | Content strategies for all 33 niches |
| `OPS/operations/` (12 files) | Daily ops, affiliate DB, email guides |
| `OPS/playbooks/` (10 files) | Daily/weekly/monthly routines |
| `OPS/prompts/` (30+ files) | Prompt library |
| `OPS/reports/` (4 files) | Method performance reports |
| `OPS/SERVICE_LANDING_PAGES/` | Service page templates |
| `OPS/SERVICE_SOPS/` | Service fulfillment SOPs |
| `OPS/SUPPORT/` (15+ files) | Customer support system |
| `OPS/templates/` (15+ files) | Launch checklists, outreach, video scripts |
| `OPS/TWITTER_ACCOUNT_QUICK_SHEETS/` (6 files) | Quick sheets per account |
| `OPS/VA_SCRIPTS/` (9 files) | VA outreach scripts |
| `OPS/VA_TRAINING/` (4 files) | VA training docs |

### 2.4 AUTOMATIONS orphans

**Many scripts in AUTOMATIONS/ not referenced in CLAUDE.md.** Key missing:

| Script | Purpose |
|--------|---------|
| `app_clone_finder.py` | Find app clones |
| `app_security_audit.py` | Security audit |
| `aso_keyword_research.py` | ASO keywords |
| `auto_list_products.py` | Auto-list products |
| `bulk_landing_page_generator.py` | Bulk landing pages |
| `cold_email_2026.py` | Cold email system |
| `competitor_price_monitor.py` | Price monitoring |
| `content_multiplier.py` | Content multiplication |
| `ecom_arb_scanner.py` | Ecom arb scanner |
| `ecom_distributor.py` | Ecom distribution |
| `email_sender.py` | Email sending |
| `engagement_bait_converter.py` | Convert engagement bait |
| `fb_ads_library_scanner.py` | FB Ads Library |
| `fiverr_gig_scraper.py` | Scrape Fiverr |
| `g2_reviewer_scraper.py` | G2 reviews |
| `generate_cold_emails.py` | Generate cold emails |
| `geo_content_optimizer.py` | GEO optimizer |
| `gov_contract_tweet_alerts.py` | Gov contract alerts |
| `gov_tenders_scraper.py` | Gov tenders |
| `hexomatic_lead_gen.py` | Hexomatic leads |
| `indeed_hiring_monitor.py` | Indeed monitoring |
| `linkedin_events_scraper.py` | LinkedIn events |
| `master_portfolio_dashboard.py` | Portfolio dashboard |
| `micro_info_product_builder.py` | Micro products |
| `nordic_ecom_arb.py` | Nordic ecom |
| `pemf_quant_dashboard.py` | PEMF dashboard |
| `perpetual_improvement_runner.py` | Perpetual improvement |
| `portfolio_rebalancer.py` | Rebalancer |
| `process_console_scrape.py` | Console scraping |
| `producthunt_scraper.py` | Product Hunt |
| `sam_gov_monitor.py` | SAM.gov monitor |
| `sam_gov_scraper.py` | SAM.gov scraper |
| `scrape_caiden_cdp.py` | Caiden scraper |
| `self_reply_funnel.py` | Self-reply funnel |
| `storeleads_ecom_scraper.py` | StoreLeads |
| `theirstack_tech_intel.py` | TheirStack intel |
| `trending_products_scanner.py` | Trending products |
| `triggering_events_monitor.py` | Trigger events |
| `uk_contracts_finder.py` | UK contracts |
| `usaspending_scraper.py` | USASpending |
| `venture_performance_tracker.py` | Venture tracker |
| `viral_content_scanner.py` | Viral content |
| `voicemail_drop_system.py` | Voicemail drops |
| `website_signal_scorer.py` | Website scoring |
| `portfolio/` (5 Python modules) | Portfolio analysis package |

### 2.5 PRODUCTS orphans

| File | Not in CLAUDE.md |
|------|-----------------|
| `ai_automation_toolkit.md` | Missing |
| `ai_content_farm_blueprint.md` | Missing |
| `branding/` (10 files) | Missing - brand identities for all niches |
| `descriptions/PRODUCT_DESCRIPTIONS_20.md` | Missing |
| `ECOM_LISTINGS_READY/` (8 files) | Missing |
| `ETSY_INSTANT_UPLOAD/` (2 files) | Missing |
| `FIVERR_INSTANT_UPLOAD/` (12 files) | Missing |
| `FREELANCE_LISTINGS_READY/` (2 files) | Missing |
| `funnel_teardown_guide.md` | Missing |
| `gov_contract_samples/` (5 files) | Missing |
| `GUMROAD_INSTANT_UPLOAD/` (17 files) | Missing |
| `listings/` (11 files) | Missing |
| `local_biz_client_system.md` | Missing |
| `progress.md` | Missing |
| `sleep_youtube_starter.md` | Missing |
| `solopreneur_tech_stack.md` | Missing |
| `twitter_growth_playbook.md` | Missing |
| `UPLOAD_CHECKLIST.md` | Missing |
| `VIBE_CODER_SECURITY_CHECKLIST.md` | Missing |
| `vibe_coding_playbook.md` | Missing |
| `WHOP_INSTANT_UPLOAD/` (9 files) | Missing |

### 2.6 CONTENT orphans

| File | Not in CLAUDE.md |
|------|-----------------|
| `AI_UGC_VIDEO_SCRIPTS.md` | Missing |
| `ARTICLE_OUTLINES_50.md` | Missing |
| `LINKEDIN_POSTS_30.md` | Missing |
| `NEWSLETTER_ISSUES_20.md` | Missing |
| `NEWSLETTER_WELCOME_SEQUENCES.md` | Missing |
| `newsletters/NEWSLETTER_ISSUES_10.md` | Missing |
| `REDDIT_POSTS_50.md` | Missing |
| `SOCIAL_LAUNCH_SCHEDULE.md` | Missing |
| `social/linkedin/LINKEDIN_POSTS_30.md` | Missing |
| `social/memes/MEME_BATCH_100.md` | Missing |
| `social/pinterest/PINTEREST_PINS_50.md` | Missing |
| `social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md` | Missing |
| `social/printmaxxer/SESSION_SQUEEZE_FEB12.md` | Missing |
| `social/reddit/REDDIT_POSTS_30.md` | Missing |
| `social/REPLY_TEMPLATES_100.md` | Missing |
| `social/threads/PRINTMAXXER_THREADS_20.md` | Missing |
| `substack_posts/` (3 files) | Missing |
| `video/SHORTS_SCRIPTS_20.md` | Missing |
| `video/TIKTOK_SCRIPTS_20.md` | Missing |
| `YOUTUBE_SCRIPTS_30.md` | Missing |

### 2.7 DIGITAL_PRODUCTS orphans

| File | Not in CLAUDE.md |
|------|-----------------|
| `SYSTEM_PRODUCTS_PACKAGE.md` | Missing |
| `ready_to_sell/` (5 .md files + 5 PDFs + converter) | Missing - ACTUAL READY-TO-SELL PRODUCTS |
| `micro_products/GUMROAD_LISTINGS_MICRO_PRODUCTS.md` | Missing |
| `micro_products/PRODUCT_2_50_viral_tweet_templates.md` | Missing |
| `micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md` | Missing |
| `micro_products/TWEET_THREAD_micro_products.md` | Missing |

### 2.8 LEDGER orphans (key CSVs not in nav)

| File | Purpose |
|------|---------|
| `AB_EXPERIMENTS_MASTER.csv` | A/B tests |
| `AB_TESTS_MASTER.csv` | More A/B tests (DUPLICATE?) |
| `ACCOUNT_HEALTH_DAILY.csv` | Account health |
| `ACCOUNT_PORTFOLIO_MASTER.csv` | Account portfolio |
| `AUTOMATION_RESULTS.csv` | Automation tracking |
| `COMPLIANCE_LOG.csv` | Compliance |
| `CONTENT_INTEL_TRACKER.csv` | Content intel |
| `CONTENT_PERFORMANCE_TRACKER.csv` | Content performance |
| `CONTENT_QA_LOG.csv` | QA log |
| `CONTENT_TO_REVENUE_MAP.csv` | Content-to-revenue |
| `DAILY_OPS_TRACKER.csv` | Daily ops |
| `ECOM_LEADS.csv` | Ecom leads |
| `EMAIL_HEALTH_DAILY.csv` | Email health |
| `ENGAGEMENT_METRICS_DAILY.csv` | Engagement |
| `FB_ADS_PRODUCT_RESEARCH.csv` | FB Ads research |
| `FIVERR_BORING_GIGS.csv` | Fiverr gigs |
| `GOV_OPPORTUNITIES.csv` | Gov opportunities |
| `HEALTH_DAILY_CHECKLIST.csv` | Personal health |
| `HEALTH_STACK.csv` | Health stack |
| `IDEAS_BACKLOG.csv` | Ideas |
| `INDIE_HACKER_TRACKER.csv` | Indie hackers |
| `INFLUENCER_CAMPAIGNS.csv` | Influencer campaigns |
| `INTENT_SIGNALS_DAILY.csv` | Intent signals |
| `KELLY_ALLOCATIONS.csv` | Kelly criterion |
| `KEYWORD_RESEARCH_MASTER.csv` | Keywords |
| `NORDIC_ECOM_GAPS.csv` | Nordic ecom |
| `PLATFORM_ALGO_CHANGES.csv` | Algo changes |
| `PLATFORM_CHANGES.csv` | Platform changes (DUP?) |
| `PLATFORM_RPM_TRACKER.csv` | RPM tracking |
| `STACK_AB_TESTS.csv` | Stack tests |
| `SYNERGY_PACKAGES_FEB2026.csv` | Synergy packages |
| `TECH_LEADERS_ALPHA_BATCH.csv` | Tech leaders |
| `TECH_STACK_INTEL.csv` | Tech stack intel |
| `TIME_TRACKING.csv` | Time tracking |
| `TOOLS_SERVICES_MASTER.csv` | Tools master |
| `VIRAL_PRODUCTS_SCAN.csv` | Viral products |
| `WARMUP_DEVICE_MATRIX.csv` | Device warmup |

---

## SECTION 3: LEGACY/DELETABLE DIRECTORIES

### 3.1 DEFINITELY DELETE

| Directory | Why |
|-----------|-----|
| `app factory/` | LEGACY - superseded by `MONEY_METHODS/APP_FACTORY/`. Has node_modules bloat. |
| `clips/` | EMPTY directory |
| `EMAIL/` | EMPTY directory |
| `logs/` | EMPTY directory |
| `output/` | EMPTY directory |
| `tasks/` | EMPTY directory |
| `RESEARCH/` | EMPTY directory |
| `MASTER_DOC/` | EMPTY directory |
| `new money method ideas/` | EMPTY directory |
| `SECRETS/` | EMPTY directory (gitignored, fine to keep) |
| `PRINTMAXX Terminal.app/` | macOS app bundle - likely not needed in project |
| All `.~lock.*.xlsx#` files | LibreOffice lock files |
| `PRINTMAXX_MASTER_OPS_BACKUP.xlsx` | Backup - use git for versioning |
| `PRINTMAXX_OPS_PLAYBOOK_BACKUP.xlsx` | Backup - use git for versioning |

### 3.2 CONSIDER ARCHIVING (Numbered hierarchy)

These numbered directories (02-10) are the OLD structure that was partially migrated to the named directories. They contain content that is MOSTLY duplicated in the named dirs.

| Directory | Size | Status |
|-----------|------|--------|
| `02_TRACKING/` | 59 files | Duplicates LEDGER/ and FINANCIALS/ |
| `03_PLAYBOOKS/` | 779K files (node_modules) | Duplicates MONEY_METHODS/ |
| `04_CONTENT/` | 733 files | Duplicates CONTENT/ |
| `05_AUTOMATION/` | 742 files | Duplicates AUTOMATIONS/ |
| `07_LANDING/` | 29K files | Duplicates LANDING/ |
| `08_PRODUCTS/` | 6 files | Duplicates PRODUCTS/ |
| `09_LEGAL/` | 24 files | Duplicates LEGAL/ |
| `10_RESEARCH/` | 29 files | Duplicates RESEARCH/ |

**Recommendation:** Audit each numbered dir for UNIQUE content not in the named dirs. Move unique files. Then delete the numbered dirs entirely.

**EXCEPTION:** `06_OPERATIONS/` has unique content (growth/, gtm/, setup/, trend_intel/) that IS actively used and referenced in CLAUDE.md. KEEP THIS ONE.

### 3.3 Files that are DEPRECATED

| File | Why |
|------|-----|
| `AUTOMATIONS/backtest_alpha_DEPRECATED.py` | Already marked deprecated |
| `scripts/builders/build_master_ops.py` | Superseded by build_master_ops_v2.py |
| `scripts/builders/build_names.py` | Superseded by build_names_v2.py |
| `scripts/repair_alpha_staging.py` | One-time fix, no longer needed |
| `scripts/repair_alpha_staging_v2.py` | One-time fix, no longer needed |

---

## SECTION 4: FILE INVENTORY BY DOMAIN

### DOMAIN: APP FACTORY

| File | Location | Status |
|------|----------|--------|
| AGGREGATE_DESIGN_SYSTEM.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| ANDROID_CLONE_SPECS.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| APP_ARBITRAGE_MATRIX.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| APP_ASSET_GENERATION_PROMPTS.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| APP_CLONE_REBRAND_STRATEGY.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| APP_DISCOVERY_ENGINE.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| APP_FACTORY_GTM_MASTER.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| APP_NAMING_AUDIT.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| APP_QUALITY_AUDIT_REAL.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| APP_QUALITY_STANDARDS.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| APP_RESTRUCTURE_PLAN.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| APP_STORE_AUDIT_FEB2026.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| APP_STORE_TRENDS_FEB2026.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| APP_UIUX_RESEARCH.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| ARB_OPPORTUNITIES_10.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| AUDIT_OUTPUT.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| CLONECHART_DATA_EXTRACT.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| COMPETITOR_GTM_TACTICS.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| COMPETITOR_REAL_DATA.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| FAVICON_SVG_PACK.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| GTM_BY_BUDGET.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| ICON_GENERATION_PROMPTS_V3.md | `MONEY_METHODS/APP_FACTORY/assets/` | NOT in nav |
| IOS_REJECTION_PREVENTION.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| IOS_SUBMISSION_PROCESS.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| NOFAP_KARMAMAXX_APP_SPEC.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| ONBOARDING_PLAYBOOK.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| PRINTMAXX_APP_PLAYBOOK.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| REJECTION_PREVENTION.md | `MONEY_METHODS/APP_FACTORY/` | DUPLICATE of IOS_REJECTION_PREVENTION |
| TOP_APP_AUDIT.md | `MONEY_METHODS/APP_FACTORY/` | In nav |
| VIBE_CODING_5_APPS_PLAN.md | `MONEY_METHODS/APP_FACTORY/` | NOT in nav |
| **PWA Builds (6 apps)** | `ralph/loops/app_factory/output/` | In nav |
| **RobloxMaxx** | `MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/` | NOT in nav (50+ files) |
| **Roblox Tycoon** | `MONEY_METHODS/APP_FACTORY/builds/roblox_tycoon/` | NOT in nav |
| **BioMaxx** | `MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54/` | NOT in nav |
| **PrayerLock Web** | `MONEY_METHODS/APP_FACTORY/builds/prayerlock-web/` | NOT in nav (also in ralph output) |

### DOMAIN: LOCAL BUSINESS

| File | Location | Status |
|------|----------|--------|
| AGENCY_WEBSITE.md | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| AI_CALL_OUTREACH.md | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| AI_WEB_DESIGN_TOOLS.md | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| COLD_EMAIL_DEMO_TEMPLATE.md | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| fix_placeholders.py | `MONEY_METHODS/LOCAL_BIZ/` | NOT in nav |
| motion_templates/ (3 files) | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| MOTION_UPSELL_PRICING.md | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| MOTION_UPSELL.md | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| NATIONWIDE_LEAD_GEN_SYSTEM.md | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| personalize_template.py | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| templates/ (6 files) | `MONEY_METHODS/LOCAL_BIZ/` | In nav |
| output/test-joes-plumbing.html | `MONEY_METHODS/LOCAL_BIZ/` | NOT in nav |
| LOCAL_BIZ_WEBSITE_SERVICE.md | `MONEY_METHODS/COLD_OUTBOUND/` | Wrong location |
| 10 README/docs | `AUTOMATIONS/` | SCATTERED - consolidate |
| local_biz_pipeline.py | `AUTOMATIONS/` | In nav |
| local_biz_website_scraper.py | `AUTOMATIONS/` | NOT in nav |
| nationwide_scraper.py | `AUTOMATIONS/` | In nav |
| mass_outreach.py | `AUTOMATIONS/` | In nav |
| savvy_lead_scraper.py | `AUTOMATIONS/` | In nav |
| 60+ lead CSV files | `AUTOMATIONS/leads/` | NOT in nav |
| 30+ outreach CSV files | `AUTOMATIONS/outreach/` | NOT in nav |

### DOMAIN: NSFW / FINDOM

| File | Location | Status |
|------|----------|--------|
| AI_NSFW_FINDOM_EXECUTION_PLAN.md | `MONEY_METHODS/AI_INFLUENCER/` | In nav |
| AI_NSFW_EXECUTION_FULL.md | `MONEY_METHODS/AI_INFLUENCER/` | NOT in nav |
| NSFW_STATUS_AUDIT.md | `MONEY_METHODS/AI_INFLUENCER/` | NOT in nav |
| FINDOM/ (6 research files) | `MONEY_METHODS/AI_INFLUENCER/` | Partially in nav |
| FINDOM_PERSONAS.md | `PRODUCTS/branding/` | In nav |
| findom_tweets_50.csv | `AUTOMATIONS/content_posting/` | In nav |

### DOMAIN: ECOM / POD

| File | Location | Status |
|------|----------|--------|
| VIRAL_PRODUCT_ARB_PLAYBOOK.md | `MONEY_METHODS/ECOM/` | In nav |
| NORDIC_ECOM_PLAYBOOK.md | `MONEY_METHODS/ECOM_ARB/` | NOT in nav |
| ECOM_ARB_PLAYBOOK.md | `MONEY_METHODS/PLATFORM_ARBITRAGE/` | NOT in nav |
| TRENDING_MEME_POD_PLAYBOOK.md | `MONEY_METHODS/POD/` | NOT in nav |
| TRENDING_OPPORTUNITIES.csv | `MONEY_METHODS/POD/` | In nav |
| POD_TIKTOK_ARBITRAGE_AUDIT.md | `MONEY_METHODS/` | In nav |
| POD_TRENDING_PHRASES.md | `MONEY_METHODS/PLATFORM_ARBITRAGE/` | NOT in nav |
| viral_product_scanner.py | `AUTOMATIONS/` | In nav |
| ecom_arb_scanner.py | `AUTOMATIONS/` | NOT in nav |
| nordic_ecom_arb.py | `AUTOMATIONS/` | NOT in nav |
| ecom_distributor.py | `AUTOMATIONS/` | NOT in nav |
| trending_products_scanner.py | `AUTOMATIONS/` | NOT in nav |
| storeleads_ecom_scraper.py | `AUTOMATIONS/` | NOT in nav |

### DOMAIN: CONTENT / SOCIAL MEDIA

| File | Location | Status |
|------|----------|--------|
| 150+ QA queue files | `OPS/CONTENT_QA_QUEUE/` | NOT individually in nav |
| 16 content strategy files | `OPS/content/` | NOT in nav |
| 30+ social posts | `CONTENT/social/` | Partially in nav |
| 12 Buffer CSVs | `AUTOMATIONS/content_posting/` | Partially in nav |
| 50+ tweets + scripts | `ralph/loops/social_setup/output/` | In nav |
| MASTER_CONTENT_BATCH_FEB12.csv | `AUTOMATIONS/content_posting/` | NOT in nav |

### DOMAIN: GOVERNMENT CONTRACTS

| File | Location | Status |
|------|----------|--------|
| GOVERNMENT_CONTRACTS_OP.md | `MONEY_METHODS/GOVERNMENT_CONTRACTS/` | NOT in nav |
| gov_contract_tweet_alerts.py | `AUTOMATIONS/` | NOT in nav |
| gov_tenders_scraper.py | `AUTOMATIONS/` | NOT in nav |
| sam_gov_monitor.py | `AUTOMATIONS/` | NOT in nav |
| sam_gov_scraper.py | `AUTOMATIONS/` | NOT in nav |
| uk_contracts_finder.py | `AUTOMATIONS/` | NOT in nav |
| usaspending_scraper.py | `AUTOMATIONS/` | NOT in nav |
| gov_contract_tweets_50.csv | `AUTOMATIONS/content_posting/` | NOT in nav |
| gov_contract_tweets.csv | `AUTOMATIONS/content_posting/` | NOT in nav |
| gov_contract_samples/ (5 files) | `PRODUCTS/` | NOT in nav |
| GOV_OPPORTUNITIES.csv | `LEDGER/` | NOT in nav |
| sam_gov_opportunities.csv | `AUTOMATIONS/leads/` | NOT in nav |
| gov_tenders_active.csv | `AUTOMATIONS/leads/` | NOT in nav |
| uk_contracts_finder_leads.csv | `AUTOMATIONS/leads/` | NOT in nav |
| usaspending_*.csv (5 files) | `AUTOMATIONS/leads/` | NOT in nav |

### DOMAIN: AUTOMATION / CRON

| File | Location | Status |
|------|----------|--------|
| printmaxx_cron.sh | Root | In nav |
| crontab_printmaxx.txt | `AUTOMATIONS/` | In nav |
| crontab_printmaxx_v2.txt | `AUTOMATIONS/` | NOT in nav (supersedes?) |
| overnight_master_runner.sh | `AUTOMATIONS/` | In nav |
| auto_resume_monitor.sh | `AUTOMATIONS/` | In nav |
| ralph_overnight_loop.sh | `AUTOMATIONS/` | In nav |
| deploy_all_apps.sh | `AUTOMATIONS/` | NOT in nav |
| perpetual_ship_engine.sh | `AUTOMATIONS/` | NOT in nav |
| safety_watchdog.sh | `AUTOMATIONS/` | NOT in nav |
| daily_agent_runner.py | `AUTOMATIONS/` | NOT in nav |
| daily_todo_generator.py | `AUTOMATIONS/` | In nav |
| run_all_research_ops.py | `AUTOMATIONS/` | NOT in nav |
| run_all_research_background.sh | `AUTOMATIONS/` | NOT in nav |

### DOMAIN: LEADS DATA

| File | Location | Count |
|------|----------|-------|
| City+Industry lead CSVs | `AUTOMATIONS/leads/` | 40+ files |
| HOT_LEADS.csv | `AUTOMATIONS/leads/` | Master hot leads |
| MASTER_LEADS.csv | `AUTOMATIONS/leads/` | Master all leads |
| SCORED_LEADS.csv | `AUTOMATIONS/leads/` | Scored leads |
| Checkpoint files | `AUTOMATIONS/leads/.checkpoints/` | 38 files |
| Specialized leads | `AUTOMATIONS/leads/` | g2, producthunt, linkedin, indeed |
| Outreach emails | `AUTOMATIONS/outreach/` | 30+ files |
| PIPELINE_TRACKER.csv | `AUTOMATIONS/outreach/` | Pipeline tracking |

### DOMAIN: SYNERGY PACKAGES (ENTIRELY MISSING FROM NAV)

| File | Location |
|------|----------|
| INDEX.md | `MONEY_METHODS/SYNERGY_PACKAGES/` |
| README.md | `MONEY_METHODS/SYNERGY_PACKAGES/` |
| SYN351-357 (5 files) | `MONEY_METHODS/SYNERGY_PACKAGES/` |
| SYNERGY_PACKAGE_* (11 files) | `MONEY_METHODS/SYNERGY_PACKAGES/` |
| STACK_* (5 files) | `MONEY_METHODS/SYNERGY_STACKS/` |
| SYNERGIES_TOOLS_MISSING_AUDIT.md | `MONEY_METHODS/` |

### DOMAIN: QUANT / FINANCIAL

| File | Location | Status |
|------|----------|--------|
| All FINANCIALS/ files (8) | `FINANCIALS/` | In nav |
| SWARM_PROJECTIONS_SUMMARY.csv | `FINANCIALS/` | NOT in nav |
| CAPITAL_ALLOCATION_MODEL.csv | `OPS/` | NOT in nav |
| RISK_CORRELATION_MATRIX.csv | `OPS/` | NOT in nav |
| REVENUE_PROJECTIONS_2026.md | `OPS/` | NOT in nav |
| PORTFOLIO_OPTIMIZATION_REPORT.md | `OPS/` | NOT in nav |
| TOP_10_PORTFOLIO_POSITIONS.md | `OPS/` | NOT in nav |
| portfolio/ (5 Python modules) | `AUTOMATIONS/portfolio/` | NOT in nav |
| portfolio_rebalancer.py | `AUTOMATIONS/` | NOT in nav |
| venture_performance_tracker.py | `AUTOMATIONS/` | NOT in nav |
| revenue_math_calculator.py | `AUTOMATIONS/` | NOT in nav |

### DOMAIN: RALPH LOOPS

| Loop | Location | Status |
|------|----------|--------|
| app_factory | `ralph/loops/app_factory/` | ACTIVE - 6 PWAs built |
| comprehensive_alpha_research | `ralph/loops/comprehensive_alpha_research/` | Has output |
| content_machine | `ralph/loops/content_machine/` | Prompt only |
| daily_ops | `ralph/loops/daily_ops/` | Prompt only |
| digital_products | `ralph/loops/digital_products/` | Prompt only |
| full_printmaxx_audit | `ralph/loops/full_printmaxx_audit/` | Prompt only |
| master_ops_build | `ralph/loops/master_ops_build/` | Has output (7 files) |
| master_ops | `ralph/loops/master_ops/` | Prompt only |
| mega | `ralph/loops/mega/` | Has output (2 files) |
| meme_coin_backtest | `ralph/loops/meme_coin_backtest/` | Prompt only |
| niche_meta_detection | `ralph/loops/niche_meta_detection/` | Has output (5 files) |
| project_refactor | `ralph/loops/project_refactor/` | Prompt only |
| retardmaxx_execution | `ralph/loops/retardmaxx_execution/` | Prompt only |
| social_branding | `ralph/loops/social_branding/` | Prompt only |
| social_setup | `ralph/loops/social_setup/` | ACTIVE - 20+ files |
| synergy_package_builder | `ralph/loops/synergy_package_builder/` | Prompt only |
| .swarm/ | `ralph/.swarm/` | Has output (12 files) |

---

## SECTION 5: RECOMMENDED ACTIONS (PRIORITY ORDER)

### P0: IMMEDIATE CLEANUP

1. **Delete all `.~lock.*.xlsx#` files** (8 LibreOffice lock files)
2. **Delete empty directories:** clips/, EMAIL/, logs/, output/, tasks/, RESEARCH/, MASTER_DOC/, "new money method ideas/"
3. **Delete backup XLSXs** at root level (use git instead)
4. **Move root orphan files** (.rtf files, stray .csv/.md files) to `OPS/archive/root_orphans/`
5. **Delete `PELVICPRO_SDK54_UPGRADE_COMPLETE.txt`** (wrong project)

### P1: RESOLVE DUPLICATE HIERARCHY

1. **Audit 02_TRACKING vs LEDGER/FINANCIALS** - identify unique files, move them, delete 02_TRACKING
2. **Audit 03_PLAYBOOKS vs MONEY_METHODS** - identify unique playbooks, move them, delete 03_PLAYBOOKS (saves 779K files)
3. **Audit 04_CONTENT vs CONTENT** - identify unique files, move them, delete 04_CONTENT
4. **Audit 05_AUTOMATION vs AUTOMATIONS** - identify unique files, move them, delete 05_AUTOMATION
5. **Audit 07_LANDING vs LANDING** - identify unique files, move them, delete 07_LANDING
6. **Move unique files from 08_PRODUCTS, 09_LEGAL, 10_RESEARCH** to named dirs, delete numbered
7. **KEEP 06_OPERATIONS/** - it has unique, actively-used content

### P2: CONSOLIDATE DUPLICATES

1. **Cold email:** Merge all cold email content into `MONEY_METHODS/COLD_OUTBOUND/`
2. **Account creation:** Single file at `OPS/ACCOUNT_CREATION_MASTER.md`
3. **Gumroad:** Keep `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` as source, clean others
4. **Session handoffs:** Archive old ones, keep only latest
5. **Alpha staging:** Delete all backup/repair/append files
6. **Twitter scrapers:** Keep `twitter_alpha_scraper.py`, deprecate rest
7. **Reddit scrapers:** Keep `reddit_alpha_scraper.py`, deprecate rest
8. **Local biz docs:** Consolidate 10 AUTOMATIONS docs into one guide
9. **Clip pipeline docs:** Consolidate 6 docs into one guide
10. **AI Agent services:** Delete one of the two identical directories
11. **Fiverr/Etsy/Redbubble/Whop:** Consolidate into single INSTANT_UPLOAD dirs

### P3: ADD MISSING FILES TO CLAUDE.md NAV

1. Add all `MONEY_METHODS/SYNERGY_PACKAGES/` files
2. Add all `MONEY_METHODS/SYNERGY_STACKS/` files
3. Add RobloxMaxx build docs
4. Add `OPS/content/` strategy files
5. Add `OPS/analytics/` guides
6. Add `OPS/SUPPORT/` system
7. Add `OPS/VA_SCRIPTS/` and `OPS/VA_TRAINING/`
8. Add `OPS/templates/` launch checklists
9. Add `PRODUCTS/GUMROAD_INSTANT_UPLOAD/`
10. Add `PRODUCTS/FIVERR_INSTANT_UPLOAD/`
11. Add `PRODUCTS/WHOP_INSTANT_UPLOAD/`
12. Add `PRODUCTS/branding/` files
13. Add `DIGITAL_PRODUCTS/ready_to_sell/` (actual PDFs ready to sell!)
14. Add `AUTOMATIONS/leads/` and `AUTOMATIONS/outreach/` as data directories
15. Add government contract domain files
16. Add all missing CONTENT/ files

---

## SECTION 6: DISK SPACE OFFENDERS

| Directory | Estimated Size | Cause |
|-----------|---------------|-------|
| `03_PLAYBOOKS/` | HUGE (779K files) | node_modules in APP_FACTORY subdir |
| `app factory/` | Large | Legacy node_modules |
| `MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/api/node_modules/` | Large | node_modules |
| `ralph/loops/app_factory/output/*/native-wrapper/` | Medium | iOS build artifacts |
| `LEDGER/.snapshots/` | Large | 28 full snapshot directories |
| `builds/programmatic_seo/` | 604 files | Programmatic SEO pages |
| `AUTOMATIONS/scraper_output/` | Medium | JSON scraper output files |
| `AUTOMATIONS/reddit_scraper_output/` | Medium | JSON scraper output |

**Total estimated recoverable space by deleting empty dirs + legacy + node_modules: Several GB**

---

## SECTION 7: TOTAL FILE COUNT BY DIRECTORY

| Directory | Meaningful Files (excl node_modules) | In CLAUDE.md Nav |
|-----------|--------------------------------------|-----------------|
| MONEY_METHODS/ | ~200 | ~60% |
| OPS/ | ~350+ | ~30% |
| AUTOMATIONS/ | ~200 scripts + ~100 data files | ~25% |
| LEDGER/ | ~130 CSVs + 28 snapshot dirs | ~40% |
| CONTENT/ | ~50+ (excl longtail) | ~20% |
| PRODUCTS/ | ~80+ | ~15% |
| DIGITAL_PRODUCTS/ | ~25 | ~30% |
| ralph/ | ~100+ | ~30% |
| scripts/ | ~35 | ~60% |
| FINANCIALS/ | 8 | ~85% |
| builds/ | 604 (mostly SEO pages) | ~10% |
| 01_STRATEGY/ | 10 | ~80% |
| 06_OPERATIONS/ | ~90 | ~30% |
| Root files | ~50 | ~20% |
| **02-05, 07-10** | **~800K (mostly bloat)** | **0%** |

---

*End of audit. This file should be updated whenever major file reorganization occurs.*
