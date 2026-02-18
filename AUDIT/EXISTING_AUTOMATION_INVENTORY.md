# EXISTING AUTOMATION INVENTORY

**Audit Date:** 2026-02-18
**Audited by:** infra-auditor agent (alpha-integration team)

---

## Section 1: CURRENTLY RUNNING

These systems are **confirmed active** based on log file timestamps from today (2026-02-18) and crontab entries that are installed.

### 1.1 Crontab (61+ active entries installed)

The crontab is installed and actively firing. Last verified log activity: 2026-02-18 06:20 AM.

#### DAILY (every day)

| Time | Script | Lines | Last Modified | Log Evidence | Status |
|------|--------|-------|---------------|--------------|--------|
| 1:00 AM | `perpetual_ship_engine.sh layer1` | 290 | 2026-02-12 | `layer1_reddit_20260218.log` (01:02) | RUNNING |
| 2:00 AM | `overnight_master_runner.sh` | 237 | 2026-02-12 | `cron_overnight.log` (02:40) -- 21/28 succeeded | RUNNING |
| 3:00 AM | `closed_loop_pipeline.py --cycles 5` | 587 | 2026-02-13 | `closed_loop.log` (03:31) -- 93K/1.4M leads analyzed | RUNNING |
| 4:00 AM | `lead_enrichment.py --enrich --top 100` | 306 | 2026-02-13 | `lead_enrichment.log` (04:00) | RUNNING |
| 4:30 AM | `refresh_dashboard.py` | 916 | 2026-02-16 | `dashboard.log` (04:30) | RUNNING |
| 5:00 AM | `memory_manager.py --full` | 464 | 2026-02-15 | No dedicated log found -- runs silently | LIKELY RUNNING |
| 5:30 AM | `printmaxx_brain.py --morning` | 801 | 2026-02-12 | No recent log checked | LIKELY RUNNING |
| 5:30 AM | `daily_research_pipeline.py --cron` | 986 | 2026-02-13 | `research_pipeline.log` exists | LIKELY RUNNING |
| 5:45 AM | `unified_alpha_monitor.py --full` | 1656 | 2026-02-17 | `unified_alpha.log` (05:47) | RUNNING |
| 6:00 AM | `daily_twitter_scraper.py` | 261 | 2026-02-03 | No recent log | UNKNOWN |
| 6:15 AM | `daily_reddit_scraper.py` | 263 | 2026-02-03 | `scraper_daily_reddit.log` (06:17) | RUNNING |
| 6:30 AM | `reddit_pain_point_miner.py --scan` | 505 | 2026-02-16 | No recent log checked | LIKELY RUNNING |
| 7:00 AM | `platform_algo_detection.py` | 322 | 2026-02-10 | `platform_meta_monitor.log` (02:01) | RUNNING |
| 7:15 AM | `hashtag_audio_tracking.py` | 387 | 2026-02-10 | No recent log | UNKNOWN |
| 8:00 AM | `daily_nocost_rbi_scanner.py --scan` | 1907 | 2026-02-10 | `layer1_rbi_20260218.log` (01:00) | RUNNING |
| 8:00 AM | `memory_manager.py --heartbeat` | 464 | 2026-02-15 | No dedicated log | LIKELY RUNNING |
| 8:15 AM | `guardrails.py --audit-all` | 1107 | 2026-02-12 | No recent log | UNKNOWN |
| 8:30 AM | `daily_todo_generator.py` | 333 | 2026-02-10 | No recent log | UNKNOWN |
| 8:30 AM | `compliance_scanner.py --audit-all` | 511 | 2026-02-15 | No recent log | UNKNOWN |
| 8:45 AM | `compliance_deadline_tracker.py --check` | 770 | 2026-02-17 | No recent log | UNKNOWN |
| 9:00 AM | `perpetual_ship_engine.sh handoff` | 290 | 2026-02-12 | No recent log | UNKNOWN |
| 9:00 AM | `response_tracker.py --followups` | 392 | 2026-02-13 | No recent log | UNKNOWN |
| 9:15 AM | `telegram_community_monitor.py --scan` | 658 | 2026-02-15 | No recent log | UNKNOWN |
| 9:30 AM | `live_dashboard_server.py --refresh` | 629 | 2026-02-13 | No recent log | UNKNOWN |
| 10:00 AM | `seo_competitor_analyzer.py --summary` | 736 | 2026-02-13 | No recent log | UNKNOWN |
| 6:30 PM | `printmaxx_brain.py --evening` | 801 | 2026-02-12 | No recent log | UNKNOWN |
| 9:00 PM | `perpetual_ship_engine.sh backup` | 290 | 2026-02-12 | No recent log | UNKNOWN |
| 9:15 PM | `backup_system.py --incremental` | 686 | 2026-02-12 | `guardrails_pre_overnight.log` (01:46) | RUNNING |
| 11:59 PM | `memory_manager.py --daily-summary` | 464 | 2026-02-15 | No recent log | UNKNOWN |

#### RECURRING (multi-hour intervals)

| Interval | Script | Lines | Last Modified | Log Evidence | Status |
|----------|--------|-------|---------------|--------------|--------|
| Every 30 min (0-8 AM) | `auto_resume_monitor.sh` | 85 | 2026-02-10 | `auto_resume.log` (06:00) | RUNNING |
| Every 30 min | `ship.sh` (ship_captain.py) | 920 | 2026-02-17 | `ship_cron.log` (06:01) 966KB | RUNNING |
| Every 2h | `freelance_demand_scanner.py` | 415 | 2026-02-12 | `freelance_demand_2026-02-18.log` (06:00) | RUNNING |
| Every 2h (offset) | `ecom_arb_engine.py` | 595 | 2026-02-16 | `ecom_arb_2026-02-18.log` (04:34) | RUNNING |
| Every 3h | `signal_aggregator.py --scan` | 828 | 2026-02-12 | `signal_agg.log` (06:00) 1.2MB | RUNNING |
| Every 4h | `venture_performance_tracker.py` | 350 | 2026-02-12 | `cron_ventures.log` (04:00) | RUNNING |
| Every 4h (offset) | `ops_orchestrator.py --run` | 1587 | 2026-02-12 | `orchestrator.log` (04:30) | RUNNING |
| Every 4h (offset) | `trend_aggregator.py` | 409 | 2026-02-12 | `trend_agg_2026-02-18.log` (04:45) | RUNNING |
| Every 6h | `sam_gov_monitor.py` | 455 | 2026-02-15 | `sam_gov.log` (06:00) | RUNNING |
| Every 6h (offset) | `alpha_screening.py --pending` | 851 | 2026-02-04 | No recent log | UNKNOWN |
| Hourly (:20) | `approved_voice_runner.sh` | -- | 2026-02-17 | `voice_render.log` (06:20) | RUNNING |

#### WEEKLY

| Time | Script | Lines | Last Modified | Status |
|------|--------|-------|---------------|--------|
| Mon 3:00 AM | `platform_rpm_tracking.py` | 388 | 2026-02-10 | UNKNOWN |
| Mon 3:30 AM | `creator_program_monitoring.py` | 418 | 2026-02-10 | UNKNOWN |
| Mon 4:00 AM | `aso_keyword_research.py` | 463 | 2026-02-10 | UNKNOWN |
| Mon 4:30 AM | `gov_tenders_scraper.py --all-sources` | 1125 | 2026-02-10 | UNKNOWN |
| Mon 5:00 AM | `ecom_arb_scanner.py` | 431 | 2026-02-06 | UNKNOWN |
| Mon 5:15 AM | `trending_products_scanner.py` | 407 | 2026-02-06 | UNKNOWN |
| Mon 5:30 AM | `ecom_distributor.py --status` | 439 | 2026-02-16 | UNKNOWN |
| Mon 6:00 AM | `email_domain_health.py --check-all` | 367 | 2026-02-13 | UNKNOWN |
| Mon 6:30 AM | `compliance_deadline_tracker.py --scan` | 770 | 2026-02-17 | UNKNOWN |
| Wed 5:00 AM | `personalize_demos.py --hot-leads` | 326 | 2026-02-13 | UNKNOWN |
| Sun 2:00 AM | `performance_optimizer.py --report` | 939 | 2026-02-12 | UNKNOWN |
| Sun 3:00 AM | `backup_system.py --full + --prune` | 686 | 2026-02-12 | UNKNOWN |
| Sun 6:00 AM | `seo_competitor_analyzer.py --all-hot` | 736 | 2026-02-13 | UNKNOWN |

#### SPECIAL

| Trigger | Script | Status |
|---------|--------|--------|
| @reboot | `ollama serve` | RUNNING (confirmed via pid file) |

### 1.2 LaunchD Agents (7 agents loaded, ALL BROKEN)

All 7 PrintMAXX `.plist` files are **loaded** (`launchctl list` confirms), but they ALL call `printmaxx_cron.sh` which is throwing `Operation not permitted` errors on every execution. This is a macOS permissions issue -- the shell script needs Full Disk Access in System Preferences.

| Agent | Schedule | Calls | Error |
|-------|----------|-------|-------|
| `com.printmaxx.morning-sync` | Daily 6:00 AM | `printmaxx_cron.sh morning` | Operation not permitted |
| `com.printmaxx.content-gen` | Daily 6:30 AM | `printmaxx_cron.sh content` | Operation not permitted |
| `com.printmaxx.evening-digest` | Daily 6:00 PM | `printmaxx_cron.sh digest` | Operation not permitted |
| `com.printmaxx.nightly-backup` | Daily 9:00 PM | `printmaxx_cron.sh backup` | Operation not permitted |
| `com.printmaxx.overnight-sprint` | Daily 10:00 PM | `printmaxx_cron.sh overnight` | Operation not permitted |
| `com.printmaxx.weekly-tasks` | Mon 9:00 AM | `printmaxx_cron.sh weekly` | Operation not permitted |
| `com.printmaxx.monthly-tasks` | 1st 8:00 AM | `printmaxx_cron.sh monthly` | Operation not permitted |

**ROOT CAUSE:** macOS Sequoia restricts launchd agent scripts from accessing directories unless `/bin/bash` or the script itself has Full Disk Access. The crontab entries work because cron runs in a different permission context.

**FIX:** System Preferences > Privacy & Security > Full Disk Access > Add `/bin/bash` and/or Terminal.app. Or rely solely on crontab (which is already working).

### 1.3 Ship Captain Control Loop

The `ship.sh` -> `ship_captain.py` system runs every 30 minutes via crontab. It is the most active automation, with a 966KB log file updated as of 06:01 AM today. It orchestrates non-critical execution and gates critical actions behind human approvals.

- **Lines:** 920 (ship_captain.py) + 7 (ship.sh)
- **Last Modified:** 2026-02-17
- **Log Size:** 966KB (ship_cron.log), 1.1MB (ship_captain.log)
- **Status:** RUNNING, confirmed active

---

## Section 2: MANUAL BUT FUNCTIONAL

These scripts work when executed manually but are NOT wired into any automatic schedule, or they require manual triggers.

### 2.1 Quant & Analysis Tools

| Script | Lines | Last Modified | Purpose | Invocation |
|--------|-------|---------------|---------|------------|
| `printmaxx_quant_terminal.py` | 2417 | 2026-02-10 | Bloomberg-style 6-panel TUI | `python3 AUTOMATIONS/printmaxx_quant_terminal.py` |
| `quant_dashboard.py` | 482 | 2026-02-04 | Simplified 6-panel TUI | `python3 AUTOMATIONS/quant_dashboard.py` |
| `ops_dashboard.py` | 725 | 2026-02-04 | Track 53 ops patterns | `python3 AUTOMATIONS/ops_dashboard.py` |
| `revenue_projector.py` | 912 | 2026-02-05 | Monte Carlo + Kelly Criterion | `python3 AUTOMATIONS/revenue_projector.py` |
| `alpha_validator.py` | 743 | 2026-02-04 | Validate alpha entries | Manual |
| `paper_trade.py` | 1154 | 2026-02-04 | Test methods with $0-100 | Manual |
| `portfolio_rebalancer.py` | 775 | 2026-02-04 | Portfolio rebalancing | Manual |
| `method_performance_analyzer.py` | 451 | 2026-02-05 | Weekly performance reports | Manual |
| `pemf_quant_dashboard.py` | 783 | 2026-02-07 | PEMF-specific dashboard | Manual |
| `master_portfolio_dashboard.py` | 259 | 2026-02-07 | Master portfolio view | Manual |

### 2.2 Lead Pipeline Tools (functional, some on cron)

| Script | Lines | Last Modified | Purpose | Status |
|--------|-------|---------------|---------|--------|
| `intelligent_lead_qualifier.py` | 1051 | 2026-02-12 | 2.87M lead qualification, website analysis | Works, called by closed_loop_pipeline |
| `website_signal_scorer.py` | 810 | 2026-02-12 | Score websites 0-100, 15 signals | Manual |
| `generate_cold_emails.py` | 1018 | 2026-02-13 | Auto-match surge.sh demos, 3-email sequences | Manual |
| `email_sender.py` | 714 | 2026-02-15 | smtplib, rate-limited, --dry-run | Manual (no SMTP configured) |
| `savvy_lead_scraper.py` | 962 | 2026-02-12 | Quant-level 0-100 lead scoring | Manual |
| `nationwide_scraper.py` | 411 | 2026-02-10 | 203 cities, 0-100 scoring | Manual |
| `mass_outreach.py` | 911 | 2026-02-10 | 4-email sequence, demo generator | Manual |
| `download_bulk_leads.py` | 398 | 2026-02-12 | Download bulk lead lists | Manual |

### 2.3 Content & Social Tools

| Script | Lines | Last Modified | Purpose | Status |
|--------|-------|---------------|---------|--------|
| `auto_content_poster.py` | 1815 | 2026-02-14 | Content posting automation | Manual |
| `content_multiplier.py` | 435 | 2026-02-10 | One piece to 20+ variants | Manual |
| `engagement_bait_converter.py` | 254 | 2026-02-10 | Convert alpha to engagement content | Manual |
| `self_reply_funnel.py` | 266 | 2026-02-10 | Self-reply tweet funnels | Manual |
| `platform_posting_optimizer.py` | 354 | 2026-02-10 | Platform-specific optimization | Manual |
| `geo_content_optimizer.py` | 452 | 2026-02-10 | GEO content optimization | Manual |
| `carousel_factory.py` | 391 | 2026-02-15 | Carousel content generation | Manual |
| `clip_automation_pipeline.py` | 632 | 2026-02-12 | Video clipping pipeline | Manual |
| `auto_clip_pipeline.py` | 594 | 2026-02-06 | Auto clip pipeline | Manual |
| `clip_post_scheduler.py` | 333 | 2026-02-06 | Schedule clip posts | Manual |

### 2.4 Research & Scraping (manual invocation)

| Script | Lines | Last Modified | Purpose |
|--------|-------|---------------|---------|
| `twitter_alpha_scraper.py` | 1009 | 2026-02-15 | Brave cookie Twitter scraper (89 accounts) |
| `background_twitter_scraper.py` | 437 | 2026-02-05 | Background Twitter scraping |
| `background_reddit_scraper.py` | 272 | 2026-02-04 | Background Reddit scraping |
| `reddit_deep_scraper.py` | 640 | 2026-02-05 | Deep Reddit scraping (comments + replies) |
| `twitter_content_scraper.py` | 564 | 2026-02-05 | Twitter content extraction |
| `enhanced_twitter_scraper.py` | 418 | 2026-02-04 | Enhanced Twitter extraction |
| `enhanced_reddit_scraper.py` | 229 | 2026-02-04 | Enhanced Reddit extraction |
| `viral_product_scanner.py` | 1045 | 2026-02-12 | FB Ads Library scanner |
| `viral_content_scanner.py` | 859 | 2026-02-06 | Viral content detection |
| `fiverr_gig_scraper.py` | 841 | 2026-02-10 | Fiverr gig scraping |
| `import_sourcing_scanner.py` | 1645 | 2026-02-13 | ImportYeti US customs data (Playwright) |
| `producthunt_scraper.py` | 634 | 2026-02-10 | Product Hunt scraping |
| `g2_reviewer_scraper.py` | 507 | 2026-02-10 | G2 reviewer scraping |
| `indeed_hiring_monitor.py` | 642 | 2026-02-10 | Indeed hiring monitoring |
| `linkedin_events_scraper.py` | 417 | 2026-02-10 | LinkedIn events scraping |
| `uk_contracts_finder.py` | 568 | 2026-02-10 | UK government contracts |

### 2.5 Deployment & Packaging

| Script | Lines | Last Modified | Purpose |
|--------|-------|---------------|---------|
| `deploy_all_apps.sh` | 100 | 2026-02-12 | Deploy all apps to surge.sh |
| `deploy_static_sites.py` | 116 | 2026-02-15 | Deploy static sites |
| `deploy_guard.py` | 305 | 2026-02-15 | Deployment safety guard |
| `auto_list_products.py` | 652 | 2026-02-16 | Playwright automated product listing |
| `app_packager.py` | 316 | 2026-02-15 | App packaging |
| `native_app_packager.py` | 330 | 2026-02-15 | Native app packaging |
| `greenlight_checker.py` | 658 | 2026-02-13 | iOS App Store compliance scan |

### 2.6 Freelance & Client Tools

| Script | Lines | Last Modified | Purpose |
|--------|-------|---------------|---------|
| `freelance_pipeline.py` | 1332 | 2026-02-12 | Full freelance pipeline (scan/pipeline/revenue/daily) |
| `auto_freelance_responder.py` | 568 | 2026-02-15 | Auto-respond to freelance posts |
| `quick_client_sample.py` | 211 | 2026-02-12 | Generate client sample work |
| `client_onboarding.py` | 346 | 2026-02-13 | Auto-generate welcome/brief/timeline |
| `cold_email_ab_test.py` | 396 | 2026-02-13 | Hash-based A/B test split |
| `freelance_packager.py` | 259 | 2026-02-15 | Package freelance deliverables |

---

## Section 3: BROKEN/STALE

### 3.1 LaunchD Agents -- ALL BROKEN

All 7 `com.printmaxx.*` plist agents fail with `Operation not permitted`. They have been broken since at least Feb 9 (empty stdout logs from that date, error logs filling since). The crontab system runs the equivalent scripts successfully, so these are **redundant but broken**.

**Impact:** LOW -- crontab covers all the same jobs. These are a secondary/backup scheduling layer.

**Fix:** Grant Full Disk Access to `/bin/bash` in System Preferences, or simply unload them since crontab works.

### 3.2 Overnight Runner Failures (7/28 scripts failing)

From the overnight log (2026-02-18): 21 succeeded, 1 failed, 6 timed out.

Scripts that consistently timeout or fail during overnight runs need investigation:
- The overnight runner has a 300-second (5 min) default timeout which may be too short for heavy scrapers
- Twitter scrapers often timeout because they require Brave cookies that may be stale

### 3.3 Stale Scrapers (pre-Feb 10)

| Script | Lines | Last Modified | Issue |
|--------|-------|---------------|-------|
| `scrape_caiden_playwright.py` | 113 | 2026-02-03 | Single-target scraper, no longer needed |
| `scrape_caiden_cdp.py` | 201 | 2026-02-03 | CDP-based variant, same target |
| `scrape_twitter_selenium.py` | 293 | 2026-02-03 | Superseded by twitter_alpha_scraper.py |
| `scrape_twitter_applescript.py` | 280 | 2026-02-03 | Superseded |
| `scrape_via_websearch.py` | 97 | 2026-02-03 | Incomplete, 97 lines |
| `scrape_parallel_fixed.py` | 255 | 2026-02-03 | Superseded by parallel_twitter_scraper.py |
| `parallel_background_scraper.py` | 283 | 2026-02-03 | Superseded |
| `process_console_scrape.py` | 164 | 2026-02-03 | Console output processor |
| `backtest_alpha_DEPRECATED.py` | 375 | 2026-02-02 | EXPLICITLY DEPRECATED in filename |

### 3.4 Ralph Loops -- PARTIALLY BROKEN

| Component | Status | Notes |
|-----------|--------|-------|
| `ralph/run_parallel_loops.sh` | BROKEN | Uses `--max-tokens` flag which is not valid for Claude CLI |
| `ralph/run_overnight_sprint.sh` | WORKS | Modified 2026-02-06, uses correct CLI flags |
| `ralph/loops/` (62 loop dirs) | MIXED | Loop dirs a01-a08, af01-af02, c01-c10, e01 etc. have prompt.md + prd.json but `--max-tokens` bug prevents autonomous runs |
| `ralph/.swarm/` | WORKS | 184 alpha entries, swarm research summary complete |
| `ralph/progress_monitor.py` | WORKS | 275 lines, monitors ralph loop progress |

### 3.5 Deprecated/Unused Files

| File | Lines | Last Modified | Notes |
|------|-------|---------------|-------|
| `backtest_alpha_DEPRECATED.py` | 375 | 2026-02-02 | Explicitly deprecated |
| `scraper_log.txt` | 0 | 2026-02-03 | Empty file |
| `example_urls.txt` | 14 | 2026-02-06 | Test data |
| `crontab_printmaxx.txt` | 71 | 2026-02-12 | Superseded by crontab_printmaxx_v2.txt |
| `crontab_secure_minimal.txt` | 9 | 2026-02-15 | Minimal crontab variant, not used |

---

## Section 4: RESEARCH CAPABILITIES

What the system CAN monitor/research if properly wired up:

### 4.1 Active Intelligence Feeds (currently running via cron)

| Capability | Script | Frequency | Data Output |
|------------|--------|-----------|-------------|
| Reddit subreddit monitoring | `daily_reddit_scraper.py` | Daily 6:15 AM | `scraper_output/` |
| Reddit pain point extraction | `reddit_pain_point_miner.py` | Daily 6:30 AM | ALPHA_STAGING.csv |
| Reddit niche + GitHub MIT + ASO + competitors | `unified_alpha_monitor.py` | Daily 5:45 AM | alpha_monitor_output/ |
| Freelance demand scanning | `freelance_demand_scanner.py` | Every 2h | FREELANCE_DEMAND_SCAN.csv |
| Ecom arbitrage pricing | `ecom_arb_engine.py` | Every 2h | ECOM_ARB_OPPORTUNITIES.csv |
| Trend aggregation (Google + Reddit + PH) | `trend_aggregator.py` | Every 4h | TREND_SIGNALS.csv |
| Signal fusion (all sources) | `signal_aggregator.py` | Every 3h | FUSED_SIGNALS.csv |
| SAM.gov federal contracts | `sam_gov_monitor.py` | Every 6h | sam_gov.log |
| Platform algorithm changes | `platform_algo_detection.py` | Daily 7:00 AM | algo_detection.log |
| Venture performance scoring | `venture_performance_tracker.py` | Every 4h | cron_ventures.log |
| Lead qualification pipeline | `closed_loop_pipeline.py` | Daily 3:00 AM | leads/qualified/ |
| System health & self-healing | `printmaxx_brain.py --heal` | Daily 1:30 AM | heal.log |

### 4.2 Available But Not Automated (manual only)

| Capability | Script | Lines | Wiring Needed |
|------------|--------|-------|---------------|
| Twitter deep scraping (89 accounts) | `twitter_alpha_scraper.py` | 1009 | Needs Brave cookies refresh, could be cron'd |
| US customs/factory intelligence | `import_sourcing_scanner.py` | 1645 | Needs Playwright, was cron'd but may timeout |
| FB Ads Library scanning | `viral_product_scanner.py` | 1045 | Needs browser automation |
| Fiverr gig analysis | `fiverr_gig_scraper.py` | 841 | Needs authentication |
| Indeed hiring trends | `indeed_hiring_monitor.py` | 642 | Could be cron'd |
| UK government contracts | `uk_contracts_finder.py` | 568 | Could be cron'd |
| Product Hunt tracking | `producthunt_scraper.py` | 634 | Could be cron'd |
| G2 review mining | `g2_reviewer_scraper.py` | 507 | Needs authentication |
| LinkedIn events | `linkedin_events_scraper.py` | 417 | Needs authentication |
| Telegram channel monitoring | `telegram_community_monitor.py` | 658 | On cron but unverified |
| Compliance deadline tracking | `compliance_deadline_tracker.py` | 770 | On cron but unverified |
| Competitor price monitoring | `competitor_price_monitor.py` | 372 | Not wired |
| Triggering events monitoring | `triggering_events_monitor.py` | 461 | Log shows activity (04:31) |
| USAspending federal data | `usaspending_scraper.py` | 621 | Not wired |
| StoreLeads ecom intel | `storeleads_ecom_scraper.py` | 353 | Not wired |
| TheirStack tech intel | `theirstack_tech_intel.py` | 335 | Not wired |
| Hexomatic lead gen | `hexomatic_lead_gen.py` | 315 | Not wired |
| Nordic ecom arbitrage | `nordic_ecom_arb.py` | 614 | Not wired |
| App clone finder | `app_clone_finder.py` | 485 | Not wired |
| Meme coin signals | `meme_coin_signal_tracker.py` | 508 | Not wired |
| Niche meta detection | `niche_meta_detector.py` | 464 | Not wired |

### 4.3 Content Generation Capabilities

| Capability | Script | Lines | Status |
|------------|--------|-------|--------|
| AI video content pipeline | `ai_video_content_pipeline.py` | 850 | Manual |
| Alpha-to-Ops conversion | `alpha_to_ops.py` | 1232 | On cron (7:30 AM) |
| Auto-content from metrics | `auto_content_from_metrics.py` | 214 | Called by closed-loop pipeline |
| Content compliance scanning | `compliance_scanner.py` | 511 | On cron (8:30 AM) |
| Micro info product builder | `micro_info_product_builder.py` | 448 | Manual |
| Revenue math calculator | `revenue_math_calculator.py` | 256 | Manual |
| Competitor sourcing pipeline | `competitor_sourcing_pipeline.py` | 768 | Manual |

---

## Section 5: SCHEDULING INFRASTRUCTURE

### 5.1 Current Scheduling Systems

| System | Status | Job Count | Reliability |
|--------|--------|-----------|-------------|
| **crontab** | WORKING | 61+ entries | HIGH -- logs confirm daily execution |
| **launchd** (7 plists) | BROKEN | 7 agents | ZERO -- all fail with Operation not permitted |
| **ship.sh / ship_captain.py** | WORKING | 1 (every 30 min) | HIGH -- 966KB log, active today |
| **printmaxx_cron.sh** | WORKING (via cron) | 10 commands | HIGH (from cron), BROKEN (from launchd) |
| **overnight_master_runner.sh** | WORKING | 28 sub-scripts | 75% (21/28 succeed) |
| **perpetual_ship_engine.sh** | WORKING | 3 layers | Layer 1 confirmed, Layer 2-3 unknown |
| **auto_resume_monitor.sh** | WORKING | 1 (every 30 min, midnight-8am) | HIGH -- log active |
| **ralph loops** | PARTIALLY BROKEN | 62 loop dirs | `--max-tokens` bug, swarm works |

### 5.2 Crontab File Versions

| File | Lines | Last Modified | Status |
|------|-------|---------------|--------|
| `AUTOMATIONS/crontab_printmaxx_v2.txt` | 226 | 2026-02-17 | INSTALLED (active crontab) |
| `AUTOMATIONS/crontab_printmaxx.txt` | 71 | 2026-02-12 | SUPERSEDED by v2 |
| `AUTOMATIONS/crontab_secure_minimal.txt` | 9 | 2026-02-15 | NOT IN USE |

### 5.3 Overlap/Conflict Analysis

**Duplicate scheduling detected:**

1. **Crontab vs LaunchD overlap:** Both try to run morning sync, content gen, backup, overnight, etc. Since launchd is broken, crontab is the sole executor. But if launchd is fixed, there will be double-runs.

2. **Brain vs Orchestrator overlap:** `printmaxx_brain.py` and `ops_orchestrator.py` both attempt to orchestrate and schedule. The brain calls the orchestrator, but they can also run independently via separate cron entries.

3. **Multiple scraper variants:** Twitter has 8+ scraper files (`daily_twitter_scraper.py`, `twitter_alpha_scraper.py`, `background_twitter_scraper.py`, `enhanced_twitter_scraper.py`, etc.). Only `daily_twitter_scraper.py` is on cron. The others are manual but do similar things.

4. **Ship Captain vs Cron overlap:** `ship_captain.py` runs every 30 minutes and can execute scripts that cron also runs. Potential double-execution risk.

### 5.4 Recommendations

#### CRITICAL (do now)

1. **Fix or remove launchd agents.** Either:
   - Grant Full Disk Access to `/bin/bash` in System Preferences
   - OR unload all 7 agents (`launchctl unload ~/Library/LaunchAgents/com.printmaxx.*.plist`) since crontab covers everything

2. **Investigate overnight failures.** 7/28 scripts failing or timing out nightly. Check `AUTOMATIONS/logs/overnight_status_2026-02-18.json` for which ones and increase timeouts or fix dependencies.

3. **Verify scripts after 8 AM actually fire.** Most confirmed logs are from midnight-6 AM. Scripts scheduled 8 AM+ (todo generator, compliance scanner, response tracker, telegram monitor, live dashboard refresh, SEO analyzer) have no recent log evidence. They may be running but not logging, or they may be failing silently.

#### HIGH PRIORITY

4. **Consolidate scraper variants.** 8+ Twitter scraper files is confusing. Deprecate old ones, keep `twitter_alpha_scraper.py` (primary) and `daily_twitter_scraper.py` (cron lightweight).

5. **Add health monitoring for cron.** Currently no alerting if a cron job fails. Consider:
   - Add a 7 AM script that checks if all expected log files were updated in the last 24h
   - Use `system_health_monitor.py` (825 lines, exists) on cron to detect failures

6. **Wire up high-value unwired scanners.** Priority candidates for cron:
   - `indeed_hiring_monitor.py` (hiring demand signals)
   - `competitor_price_monitor.py` (price change alerts)
   - `uk_contracts_finder.py` (additional gov contract source)
   - `storeleads_ecom_scraper.py` (ecom intelligence)

#### NICE TO HAVE

7. **Clean up deprecated files.** Remove or move to an `_archive/` directory:
   - `backtest_alpha_DEPRECATED.py`
   - `scrape_caiden_*.py`
   - `scrape_twitter_selenium.py`
   - `scrape_twitter_applescript.py`
   - `scrape_via_websearch.py`
   - `scrape_parallel_fixed.py`
   - `crontab_printmaxx.txt` (v1)

8. **Fix ralph loops.** Remove `--max-tokens` flag from loop runner scripts so autonomous overnight loops can execute.

9. **Resolve cron/launchd/ship_captain triple-scheduling.** Pick ONE scheduling system and decommission the others to avoid confusion. Recommendation: **crontab as primary** (proven working), ship_captain as secondary orchestrator (for human-in-loop gating), decommission launchd entirely.

---

## Appendix A: Full Script Count Summary

| Category | Count | Total Lines |
|----------|-------|-------------|
| Python scripts in AUTOMATIONS/ | 145+ | ~85,000+ |
| Shell scripts in AUTOMATIONS/ | 15+ | ~1,500+ |
| Ralph scripts | 4 | ~823 |
| Root-level scripts (printmaxx_cron.sh, ship.sh) | 2 | 747 |
| **TOTAL** | **166+** | **~88,000+** |

## Appendix B: Log File Activity Summary (2026-02-18)

| Log File | Last Updated | Size | Active? |
|----------|-------------|------|---------|
| voice_render.log | 06:20 | 989B | YES |
| scraper_daily_reddit.log | 06:17 | 13KB | YES |
| ship_cron.log | 06:01 | 966KB | YES |
| ship_captain.log | 06:01 | 1.1MB | YES |
| freelance_demand_2026-02-18.log | 06:00 | 15KB | YES |
| sam_gov.log | 06:00 | 107KB | YES |
| signal_agg.log | 06:00 | 1.2MB | YES |
| auto_resume.log | 06:00 | 20KB | YES |
| unified_alpha.log | 05:47 | 10KB | YES |
| trend_agg_2026-02-18.log | 04:45 | 518B | YES |
| ecom_arb_2026-02-18.log | 04:34 | 34KB | YES |
| orchestrator.log | 04:30 | 13KB | YES |
| dashboard.log | 04:30 | 579B | YES |
| lead_enrichment.log | 04:00 | 26KB | YES |
| cron_ventures.log | 04:00 | 80KB | YES |
| closed_loop.log | 03:31 | 51KB | YES |
| overnight_2026-02-18.log | 03:13 | 474KB | YES |
| cron_overnight.log | 02:40 | 36KB | YES |
| heal.log | 01:30 | 1KB | YES |
| cron_engine_layer1.log | 01:02 | 780B | YES |

## Appendix C: Ralph Loop Inventory

| Directory | Type | Status |
|-----------|------|--------|
| `ralph/.swarm/` | Swarm orchestration | WORKING (184 alpha, summary complete) |
| `ralph/loops/a01-a08` | Alpha research loops | Created 2026-02-12, have prompts |
| `ralph/loops/af01-af02` | Alpha factory loops | Created 2026-02-12 |
| `ralph/loops/c01-c10` | Content loops | Created 2026-02-12 |
| `ralph/loops/e01` | Execution loop | Created 2026-02-12 |
| `ralph/loops/app_factory` | App factory loop | Created 2026-02-10 |
| `ralph/loops/comprehensive_alpha_research` | Research loop | Created 2026-02-06 |
| `ralph/loops/content_machine` | Content gen loop | Created 2026-02-06 |
| `ralph/loops/daily_ops` | Daily ops loop | Created 2026-02-05 |
| `ralph/loops/digital_products` | Product loop | Created 2026-02-06 |
| `ralph/loops/content_distribution` | Distribution loop | Created 2026-02-10 |

---

*End of audit. Total scripts inventoried: 166+. Total cron entries: 61+. LaunchD agents: 7 (all broken). Active log files today: 20+.*
