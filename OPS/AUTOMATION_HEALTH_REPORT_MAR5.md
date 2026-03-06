# PRINTMAXX Automation Health Report - 2026-03-05 04:12

## Summary

| Metric | Count |
|--------|-------|
| Total scripts | 251 |
| WORKING (self-contained) | 218 |
| NEEDS_CONFIG (API keys/accounts) | 31 |
| NEEDS_DEPS (missing packages) | 2 |
| BROKEN | 0 |

## Category Breakdown

| Category | Total | Working | Needs Config | Needs Deps | Broken |
|----------|-------|---------|--------------|------------|--------|
| utility | 86 | 69 | 16 | 1 | 0 |
| scraper | 35 | 34 | 0 | 1 | 0 |
| monitor | 32 | 29 | 3 | 0 | 0 |
| orchestrator | 20 | 17 | 3 | 0 | 0 |
| content | 17 | 16 | 1 | 0 | 0 |
| research | 15 | 15 | 0 | 0 | 0 |
| ecommerce | 12 | 7 | 5 | 0 | 0 |
| safety | 10 | 9 | 1 | 0 | 0 |
| outbound | 9 | 8 | 1 | 0 | 0 |
| dashboard | 9 | 9 | 0 | 0 | 0 |
| deploy | 6 | 5 | 1 | 0 | 0 |

## Top 10 Fixes Applied (Mar 5, 2026)

1. **qwen3_tts_longform.py** - Added try/except guards for missing qwen_tts, soundfile, torch, numpy with install hints
2. **guardrails.py** - Replaced hardcoded PROJECT_ROOT with auto-detection from `Path(__file__)`
3. **daily_research_pipeline.py** - Replaced hardcoded PROJECT_DIR with auto-detection
4. **background_reddit_scraper.py** - Replaced hardcoded PROJECT_DIR with auto-detection
5. **background_twitter_scraper.py** - Replaced hardcoded PROJECT_DIR with auto-detection
6. **meme_coin_signal_tracker.py** - Added missing `from pathlib import Path`, replaced hardcoded PROJECT_ROOT
7. **download_bulk_leads.py** - Replaced hardcoded PROJECT_ROOT and PYTHON path with auto-detection using `sys.executable`
8. **autonomous_orchestrator.py** - Replaced hardcoded claude CLI path with `shutil.which()` auto-detection
9. **alpha_monitor.py** - Replaced hardcoded PROJECT_DIR with auto-detection
10. **alpha_screening.py** - Replaced hardcoded PROJECT_DIR with auto-detection

## Duplicate / Consolidation Candidates

### Reddit Scrapers (6 variants)

- `background_reddit_scraper.py`
- `daily_reddit_scraper.py`
- `enhanced_reddit_scraper.py`
- `headless_reddit_scraper.py`
- `reddit_alpha_scraper.py`
- `reddit_deep_scraper.py`

Recommendation: Keep `background_reddit_scraper.py` (JSON API, no auth) and `reddit_deep_scraper.py` (Playwright). Archive the rest.

### Twitter Scrapers (9 variants)

- `background_twitter_scraper.py`
- `daily_twitter_scraper.py`
- `enhanced_twitter_scraper.py`
- `headless_twitter_scraper.py`
- `parallel_twitter_scraper.py`
- `twitter_alpha_scraper.py`
- `twitter_bookmarks_scraper.py`
- `twitter_content_scraper.py`
- `twitter_scraper_live.py`

Recommendation: Keep `twitter_alpha_scraper.py` (primary) and `background_twitter_scraper.py` (cookie-based). Archive the rest.

### Content Scripts (12 variants)

- `ai_video_content_pipeline.py`
- `auto_content_from_metrics.py`
- `auto_content_poster.py`
- `content_factory.py`
- `content_multiplier.py`
- `content_queue.py`
- `content_repurposer.py`
- `content_trend_pipeline.py`
- `geo_content_optimizer.py`
- `scale_verdict_to_content.py`
- `twitter_content_scraper.py`
- `viral_content_scanner.py`

Recommendation: Consolidate around `content_factory.py` as primary, `auto_content_poster.py` for posting.

### Ecom Scripts (7 variants)

- `ecom_arb_engine.py`
- `ecom_arb_scanner.py`
- `ecom_autopilot.py`
- `ecom_deep_scanner.py`
- `ecom_distributor.py`
- `ecom_packager.py`
- `nordic_ecom_arb.py`
- `storeleads_ecom_scraper.py`

Recommendation: Keep `ecom_autopilot.py` (unified) and `ecom_arb_engine.py`. Archive scanners into archive/.

## Full Script Status

| Script | Lines | Status | Category | API Keys | Notes |
|--------|-------|--------|----------|----------|-------|
| browser_scraper_daily.py | 386 | NEEDS_DEPS | scraper | - | Missing: browser_cookie3 |
| qwen3_tts_longform.py | 491 | NEEDS_DEPS | utility | - | Missing: qwen_tts, soundfile |
| auto_clip_pipeline.py | 594 | NEEDS_CONFIG | orchestrator | ANTHROPIC | --help OK |
| auto_freelance_responder.py | 568 | NEEDS_CONFIG | outbound | REDDIT_CLIENT | --help OK |
| auto_list_products.py | 674 | NEEDS_CONFIG | ecommerce | GUMROAD | --help OK |
| autonomous_money_printer.py | 1001 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| clawwork_sidecar.py | 568 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| competitive_intelligence_engine.py | 1385 | NEEDS_CONFIG | utility | GUMROAD | Hardcoded paths: 1 |
| content_repurposer.py | 524 | NEEDS_CONFIG | content | ANTHROPIC | --help OK |
| daily_agent_runner.py | 290 | NEEDS_CONFIG | orchestrator | GUMROAD |  |
| daily_nocost_rbi_scanner.py | 1907 | NEEDS_CONFIG | monitor | GUMROAD | --help OK |
| deploy_guard.py | 305 | NEEDS_CONFIG | safety | VERCEL_TOKEN, SURGE_TOKEN, NETLIFY_AUTH_TOKEN | --help OK |
| ecom_distributor.py | 439 | NEEDS_CONFIG | ecommerce | GUMROAD |  |
| edge_growth_engine.py | 1904 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| gumroad_auto_list.py | 458 | NEEDS_CONFIG | ecommerce | GUMROAD | --help OK |
| gumroad_autolist_packager.py | 213 | NEEDS_CONFIG | ecommerce | GUMROAD | --help OK |
| master_ops_enhancer.py | 747 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| meme_coin_signal_tracker.py | 509 | NEEDS_CONFIG | monitor | ANTHROPIC |  |
| memory_manager.py | 464 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| meta_planner.py | 1201 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| money_printer_engine.py | 850 | NEEDS_CONFIG | utility | GUMROAD |  |
| perpetual_improvement_runner.py | 849 | NEEDS_CONFIG | orchestrator | GUMROAD | --help OK |
| platform_account_creator.py | 995 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| portfolio_rebalancer.py | 775 | NEEDS_CONFIG | utility | GUMROAD | Hardcoded paths: 1 |
| pricing_optimizer.py | 758 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| printmaxx.py | 848 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| ralph_loop_factory.py | 946 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| ship_captain.py | 934 | NEEDS_CONFIG | deploy | STRIPE, GUMROAD, VERCEL_TOKEN, SURGE_TOKEN, NETLIFY_AUTH_TOKEN | --help OK |
| stack_governor.py | 360 | NEEDS_CONFIG | utility | OPENAI, ANTHROPIC | --help OK |
| trend_to_listing.py | 364 | NEEDS_CONFIG | ecommerce | GUMROAD | --help OK |
| venture_map_executor.py | 668 | NEEDS_CONFIG | utility | GUMROAD | --help OK |
| venture_performance_tracker.py | 350 | NEEDS_CONFIG | monitor | GUMROAD |  |
| youtube_factory.py | 659 | NEEDS_CONFIG | utility | ANTHROPIC | --help OK |
| account_creation_helper.py | 275 | WORKING | utility | - | Hardcoded paths: 1 |
| ad_budget_tracker.py | 292 | WORKING | monitor | - | --help OK |
| agent_monitor.py | 253 | WORKING | monitor | - |  |
| agentic_discovery.py | 666 | WORKING | utility | - |  |
| ai_video_content_pipeline.py | 850 | WORKING | orchestrator | - | --help OK |
| algo_ban_prevention.py | 1425 | WORKING | utility | - | --help OK |
| alpha_auto_approver.py | 196 | WORKING | research | - | --help OK |
| alpha_auto_processor.py | 796 | WORKING | research | - | --help OK |
| alpha_csv_parser.py | 268 | WORKING | research | - |  |
| alpha_monitor.py | 741 | WORKING | monitor | - | --help OK |
| alpha_research_runner.py | 828 | WORKING | orchestrator | - | --help OK |
| alpha_review_bot.py | 332 | WORKING | research | - |  |
| alpha_screening.py | 851 | WORKING | research | - | --help OK |
| alpha_staging_migrate.py | 232 | WORKING | research | - |  |
| alpha_to_ops.py | 1232 | WORKING | research | - | --help OK |
| alpha_validator.py | 743 | WORKING | research | - | Hardcoded paths: 1 |
| app_clone_finder.py | 485 | WORKING | utility | - | --help OK |
| app_clone_pipeline.py | 538 | WORKING | orchestrator | - | --help OK |
| app_ideation_specialist.py | 1227 | WORKING | utility | - | --help OK |
| app_name_validator.py | 434 | WORKING | utility | - | --help OK |
| app_packager.py | 316 | WORKING | deploy | - | --help OK |
| app_security_audit.py | 579 | WORKING | utility | - | --help OK |
| app_store_aso_optimizer.py | 708 | WORKING | utility | - | Hardcoded paths: 1 |
| approved_script_voice_runner.py | 754 | WORKING | orchestrator | - | --help OK |
| arb_listing_generator.py | 446 | WORKING | ecommerce | - | --help OK |
| aso_keyword_research.py | 463 | WORKING | research | - | Hardcoded paths: 1 |
| auto_account_creator.py | 518 | WORKING | utility | - | --help OK |
| auto_clip_service.py | 1146 | WORKING | utility | - | --help OK |
| auto_content_from_metrics.py | 214 | WORKING | content | - | --help OK |
| auto_content_poster.py | 1815 | WORKING | content | - | --help OK |
| auto_dev_account_setup.py | 882 | WORKING | utility | - | Hardcoded paths: 1 |
| auto_rebalancer.py | 462 | WORKING | utility | - | --help OK |
| autonomous_alerts.py | 253 | WORKING | utility | - |  |
| autonomous_factory.py | 1132 | WORKING | utility | - | --help OK |
| autonomous_orchestrator.py | 562 | WORKING | orchestrator | - | --help OK |
| autonomous_supervisor.py | 1289 | WORKING | orchestrator | - | --help OK |
| background_reddit_scraper.py | 272 | WORKING | scraper | - | --help OK |
| background_twitter_scraper.py | 437 | WORKING | scraper | - | --help OK |
| backtest_alpha_DEPRECATED.py | 375 | WORKING | research | - | Hardcoded paths: 1 |
| backup_system.py | 686 | WORKING | safety | - | Hardcoded paths: 1 |
| browser_image_gen.py | 479 | WORKING | utility | - | --help OK |
| bulk_landing_page_generator.py | 894 | WORKING | utility | - | --help OK |
| carousel_factory.py | 391 | WORKING | utility | - | --help OK |
| checkpoint_manager.py | 224 | WORKING | safety | - | --help OK |
| clawdbot_rbi_engine.py | 1059 | WORKING | utility | - | --help OK |
| client_onboarding.py | 346 | WORKING | outbound | - | --help OK |
| clip_automation_pipeline.py | 632 | WORKING | orchestrator | - |  |
| clip_post_scheduler.py | 333 | WORKING | content | - | --help OK |
| closed_loop_pipeline.py | 612 | WORKING | orchestrator | - | --help OK |
| cluely_compliance_pack.py | 353 | WORKING | utility | - | --help OK |
| cold_email_2026.py | 528 | WORKING | content | - | --help OK |
| cold_email_ab_test.py | 396 | WORKING | content | - | --help OK |
| community_intel_scanner.py | 1282 | WORKING | monitor | - | --help OK |
| competitor_monitor.py | 500 | WORKING | monitor | - | Hardcoded paths: 1 |
| competitor_price_monitor.py | 372 | WORKING | monitor | - | --help OK |
| competitor_sourcing_pipeline.py | 768 | WORKING | orchestrator | - | --help OK |
| compliance_deadline_tracker.py | 770 | WORKING | monitor | - | --help OK |
| compliance_scanner.py | 511 | WORKING | monitor | - | --help OK |
| content_factory.py | 1030 | WORKING | content | - | --help OK |
| content_multiplier.py | 435 | WORKING | content | - | --help OK |
| content_queue.py | 401 | WORKING | content | - | --help OK |
| content_trend_pipeline.py | 524 | WORKING | orchestrator | - | --help OK |
| creative_sourcer.py | 450 | WORKING | utility | - |  |
| creator_program_monitoring.py | 418 | WORKING | monitor | - | Hardcoded paths: 1 |
| cron_fleet_report.py | 285 | WORKING | utility | - | --help OK |
| daily_ops_from_alpha.py | 422 | WORKING | research | - | Hardcoded paths: 2 |
| daily_reddit_scraper.py | 263 | WORKING | scraper | - |  |
| daily_research_orchestrator.py | 1054 | WORKING | orchestrator | - | --help OK |
| daily_research_pipeline.py | 986 | WORKING | orchestrator | - | Hardcoded paths: 1 |
| daily_todo_generator.py | 333 | WORKING | utility | - |  |
| daily_twitter_scraper.py | 266 | WORKING | scraper | - |  |
| deploy_static_sites.py | 116 | WORKING | deploy | - | --help OK |
| download_bulk_leads.py | 398 | WORKING | outbound | - | --help OK |
| ecom_arb_engine.py | 595 | WORKING | ecommerce | - | --help OK |
| ecom_arb_scanner.py | 431 | WORKING | monitor | - | --help OK |
| ecom_autopilot.py | 581 | WORKING | ecommerce | - | --help OK |
| ecom_deep_scanner.py | 1095 | WORKING | monitor | - | --help OK |
| ecom_packager.py | 284 | WORKING | ecommerce | - | --help OK |
| email_domain_health.py | 367 | WORKING | safety | - | --help OK |
| email_sender.py | 714 | WORKING | content | - | --help OK |
| engagement_bait_converter.py | 254 | WORKING | utility | - | --help OK |
| enhanced_reddit_scraper.py | 229 | WORKING | scraper | - |  |
| enhanced_twitter_scraper.py | 418 | WORKING | scraper | - |  |
| fb_ads_library_scanner.py | 309 | WORKING | monitor | - | --help OK |
| financial_intelligence.py | 1096 | WORKING | utility | - | --help OK |
| fiverr_gig_scraper.py | 841 | WORKING | scraper | - | --help OK |
| freelance_demand_scanner.py | 415 | WORKING | monitor | - | --help OK |
| freelance_packager.py | 259 | WORKING | outbound | - | --help OK |
| freelance_pipeline.py | 1332 | WORKING | orchestrator | - | --help OK |
| freshness_auditor.py | 173 | WORKING | utility | - | --help OK |
| full_context_swarm_dump.py | 420 | WORKING | utility | - | --help OK |
| g2_reviewer_scraper.py | 507 | WORKING | scraper | - | --help OK |
| generate_cold_emails.py | 1018 | WORKING | content | - |  |
| geo_content_optimizer.py | 452 | WORKING | content | - | --help OK |
| gov_bid_packager.py | 315 | WORKING | deploy | - | --help OK |
| gov_contract_tweet_alerts.py | 467 | WORKING | content | - | --help OK |
| gov_tenders_scraper.py | 1125 | WORKING | scraper | - | --help OK |
| greenlight_checker.py | 658 | WORKING | utility | - | --help OK |
| guardrails.py | 1110 | WORKING | safety | - | Hardcoded paths: 2 |
| hashtag_audio_tracking.py | 387 | WORKING | utility | - | Hardcoded paths: 1 |
| headless_reddit_scraper.py | 210 | WORKING | scraper | - |  |
| headless_twitter_scraper.py | 267 | WORKING | scraper | - |  |
| hexomatic_lead_gen.py | 315 | WORKING | outbound | - | --help OK |
| human_brief.py | 283 | WORKING | utility | - | --help OK |
| import_sourcing_scanner.py | 1645 | WORKING | monitor | - | --help OK |
| indeed_hiring_monitor.py | 642 | WORKING | monitor | - | --help OK |
| intelligent_lead_qualifier.py | 1051 | WORKING | outbound | - | Hardcoded paths: 1 |
| ios_rejection_screener.py | 1479 | WORKING | utility | - | --help OK |
| ios_release_pipeline.py | 996 | WORKING | orchestrator | - | Hardcoded paths: 1 |
| launch_directory_packager.py | 431 | WORKING | deploy | - | --help OK |
| lead_enrichment.py | 306 | WORKING | outbound | - | --help OK |
| linkedin_events_scraper.py | 417 | WORKING | scraper | - | --help OK |
| live_dashboard_server.py | 629 | WORKING | dashboard | - |  |
| llm_backends.py | 776 | WORKING | utility | - | --help OK |
| local_biz_pipeline.py | 836 | WORKING | orchestrator | - | --help OK |
| local_biz_website_scraper.py | 658 | WORKING | scraper | - | --help OK |
| log_rotator.py | 221 | WORKING | safety | - | --help OK |
| market_scanner.py | 1262 | WORKING | monitor | - | --help OK |
| market_size_estimator.py | 735 | WORKING | utility | - | Hardcoded paths: 1 |
| mass_outreach.py | 911 | WORKING | outbound | - | --help OK |
| master_ops_executor.py | 347 | WORKING | utility | - | --help OK |
| master_portfolio_dashboard.py | 259 | WORKING | dashboard | - | --help OK |
| meta_vision_swarm_audit.py | 566 | WORKING | utility | - | --help OK |
| method_performance_analyzer.py | 451 | WORKING | utility | - |  |
| micro_info_product_builder.py | 448 | WORKING | ecommerce | - | --help OK |
| monetization_engine.py | 1326 | WORKING | utility | - | --help OK |
| nationwide_scraper.py | 411 | WORKING | scraper | - | --help OK |
| native_app_packager.py | 330 | WORKING | deploy | - | --help OK |
| net_guard.py | 110 | WORKING | safety | - | --help OK |
| niche_meta_detector.py | 464 | WORKING | utility | - |  |
| nordic_ecom_arb.py | 614 | WORKING | ecommerce | - | --help OK |
| nsfw_safety_system.py | 1077 | WORKING | utility | - | --help OK |
| openclaw_hybrid.py | 1414 | WORKING | utility | - | --help OK |
| openrouter_budget_guard.py | 610 | WORKING | safety | - | --help OK |
| ops_dashboard.py | 725 | WORKING | dashboard | - | Hardcoded paths: 1 |
| ops_orchestrator.py | 1587 | WORKING | orchestrator | - |  |
| ops_web_dashboard.py | 721 | WORKING | dashboard | - | --help OK |
| overnight_orchestrator.py | 308 | WORKING | orchestrator | - | --help OK |
| paper_trade.py | 1154 | WORKING | utility | - | Hardcoded paths: 1 |
| parallel_background_scraper.py | 283 | WORKING | scraper | - |  |
| parallel_twitter_scraper.py | 217 | WORKING | scraper | - |  |
| pemf_quant_dashboard.py | 783 | WORKING | dashboard | - | Hardcoded paths: 1 |
| performance_optimizer.py | 939 | WORKING | utility | - | --help OK |
| perpetual_guardian.py | 731 | WORKING | safety | - | --help OK |
| persistent_memory.py | 510 | WORKING | utility | - | --help OK |
| personalize_demos.py | 326 | WORKING | utility | - | --help OK |
| platform_algo_detection.py | 322 | WORKING | utility | - | Hardcoded paths: 1 |
| platform_meta_monitor.py | 293 | WORKING | monitor | - |  |
| platform_posting_optimizer.py | 354 | WORKING | content | - | --help OK |
| platform_rpm_tracking.py | 388 | WORKING | utility | - | Hardcoded paths: 1 |
| playbook_enhancer.py | 714 | WORKING | utility | - | --help OK |
| printmaxx_brain.py | 813 | WORKING | utility | - | --help OK |
| printmaxx_desktop.py | 1790 | WORKING | dashboard | - | --help OK |
| printmaxx_quant_terminal.py | 2417 | WORKING | utility | - | Hardcoded paths: 1 |
| printmaxx_status.py | 163 | WORKING | utility | - | --help OK |
| printmaxx_tui.py | 3418 | WORKING | dashboard | - |  |
| process_console_scrape.py | 164 | WORKING | scraper | - | Hardcoded paths: 1 |
| product_launch_automator.py | 589 | WORKING | ecommerce | - | --help OK |
| producthunt_scraper.py | 634 | WORKING | scraper | - | --help OK |
| prompt_logger.py | 458 | WORKING | utility | - | --help OK |
| publish_pack.py | 335 | WORKING | utility | - | --help OK |
| qa_auto_approver.py | 332 | WORKING | utility | - | --help OK |
| quality_gate.py | 1445 | WORKING | utility | - | --help OK |
| quant_dashboard.py | 482 | WORKING | dashboard | - | Hardcoded paths: 1 |
| quick_client_sample.py | 211 | WORKING | outbound | - | --help OK |
| quote_tweet_scanner.py | 405 | WORKING | monitor | - | --help OK |
| ralph_loop_fixer.py | 222 | WORKING | utility | - |  |
| rbi_portfolio_optimizer.py | 351 | WORKING | utility | - | --help OK |
| reddit_alpha_scraper.py | 527 | WORKING | scraper | - |  |
| reddit_deep_scraper.py | 640 | WORKING | scraper | - | Hardcoded paths: 1 |
| reddit_pain_point_miner.py | 505 | WORKING | utility | - | --help OK |
| refresh_dashboard.py | 925 | WORKING | dashboard | - | --help OK |
| response_tracker.py | 392 | WORKING | monitor | - | --help OK |
| revenue_math_calculator.py | 256 | WORKING | utility | - | --help OK |
| revenue_projector.py | 915 | WORKING | utility | - |  |
| run_all_research_ops.py | 195 | WORKING | research | - | Hardcoded paths: 3 |
| saas_opportunity_engine.py | 1173 | WORKING | utility | - | --help OK |
| saas_product_scanner.py | 357 | WORKING | monitor | - | --help OK |
| sam_gov_monitor.py | 455 | WORKING | monitor | - | --help OK |
| sam_gov_scraper.py | 455 | WORKING | scraper | - | --help OK |
| savvy_lead_scraper.py | 962 | WORKING | scraper | - | --help OK |
| scale_verdict_to_content.py | 775 | WORKING | content | - | --help OK |
| scheduled_runs_manager.py | 571 | WORKING | utility | - | --help OK |
| scrape_caiden_cdp.py | 201 | WORKING | scraper | - | Hardcoded paths: 1 |
| scrape_caiden_playwright.py | 113 | WORKING | scraper | - |  |
| scrape_parallel_fixed.py | 255 | WORKING | scraper | - |  |
| scrape_twitter_applescript.py | 280 | WORKING | scraper | - | Hardcoded paths: 1 |
| scrape_twitter_selenium.py | 293 | WORKING | scraper | - | Hardcoded paths: 1 |
| scrape_via_websearch.py | 97 | WORKING | scraper | - |  |
| self_reply_funnel.py | 266 | WORKING | utility | - | --help OK |
| semantic_memory_search.py | 616 | WORKING | utility | - | --help OK |
| seo_competitor_analyzer.py | 736 | WORKING | utility | - | --help OK |
| signal_aggregator.py | 840 | WORKING | research | - | --help OK |
| storeleads_ecom_scraper.py | 353 | WORKING | scraper | - | --help OK |
| system_health_monitor.py | 858 | WORKING | monitor | - | --help OK |
| telegram_community_monitor.py | 658 | WORKING | monitor | - | --help OK |
| theirstack_tech_intel.py | 335 | WORKING | utility | - | --help OK |
| trend_aggregator.py | 409 | WORKING | research | - | --help OK |
| trend_scanner.py | 580 | WORKING | monitor | - | Hardcoded paths: 1 |
| trending_products_scanner.py | 407 | WORKING | monitor | - | --help OK |
| triggering_events_monitor.py | 461 | WORKING | monitor | - | --help OK |
| tweet_auto_drafter.py | 583 | WORKING | content | - | --help OK |
| twitter_alpha_scraper.py | 1009 | WORKING | scraper | - | Hardcoded paths: 1 |
| twitter_bookmarks_scraper.py | 850 | WORKING | scraper | - | Hardcoded paths: 2 |
| twitter_content_scraper.py | 564 | WORKING | scraper | - | Hardcoded paths: 1 |
| twitter_copy_style_ingest.py | 81 | WORKING | utility | - | --help OK |
| twitter_scraper_live.py | 510 | WORKING | scraper | - | Hardcoded paths: 1 |
| uk_contracts_finder.py | 568 | WORKING | utility | - | --help OK |
| unified_alpha_monitor.py | 1656 | WORKING | monitor | - | --help OK |
| update_system_architecture.py | 394 | WORKING | utility | - | --help OK |
| usaspending_scraper.py | 621 | WORKING | scraper | - | --help OK |
| venture_deep_scorer.py | 936 | WORKING | utility | - | --help OK |
| venture_map_health_check.py | 273 | WORKING | safety | - | --help OK |
| viral_content_scanner.py | 859 | WORKING | monitor | - | Hardcoded paths: 1 |
| viral_product_scanner.py | 1045 | WORKING | monitor | - | --help OK |
| voicemail_drop_system.py | 247 | WORKING | content | - | --help OK |
| website_signal_scorer.py | 810 | WORKING | research | - | --help OK |
| workflow_wirer.py | 1711 | WORKING | utility | - | --help OK |

## Scripts Requiring API Keys

| API Key | Used By | Description |
|---------|---------|-------------|
| GUMROAD | 24 scripts | Gumroad access token |
| ANTHROPIC | 5 scripts | Anthropic API key |
| VERCEL_TOKEN | 2 scripts | Vercel deploy token |
| SURGE_TOKEN | 2 scripts | Surge.sh token |
| NETLIFY_AUTH_TOKEN | 2 scripts | Netlify auth token |
| REDDIT_CLIENT | 1 scripts | Reddit API credentials |
| STRIPE | 1 scripts | Stripe payment key |
| OPENAI | 1 scripts | OpenAI API key |

## Self-Contained Scripts (run immediately, no config needed)

- `auto_content_from_metrics.py` (content, 214L)
- `auto_content_poster.py` (content, 1815L)
- `clip_post_scheduler.py` (content, 333L)
- `cold_email_2026.py` (content, 528L)
- `cold_email_ab_test.py` (content, 396L)
- `content_factory.py` (content, 1030L)
- `content_multiplier.py` (content, 435L)
- `content_queue.py` (content, 401L)
- `email_sender.py` (content, 714L)
- `geo_content_optimizer.py` (content, 452L)
- `gov_contract_tweet_alerts.py` (content, 467L)
- `platform_posting_optimizer.py` (content, 354L)
- `scale_verdict_to_content.py` (content, 775L)
- `tweet_auto_drafter.py` (content, 583L)
- `voicemail_drop_system.py` (content, 247L)
- `master_portfolio_dashboard.py` (dashboard, 259L)
- `ops_dashboard.py` (dashboard, 725L)
- `ops_web_dashboard.py` (dashboard, 721L)
- `printmaxx_desktop.py` (dashboard, 1790L)
- `refresh_dashboard.py` (dashboard, 925L)
- `app_packager.py` (deploy, 316L)
- `deploy_static_sites.py` (deploy, 116L)
- `gov_bid_packager.py` (deploy, 315L)
- `launch_directory_packager.py` (deploy, 431L)
- `native_app_packager.py` (deploy, 330L)
- `arb_listing_generator.py` (ecommerce, 446L)
- `ecom_arb_engine.py` (ecommerce, 595L)
- `ecom_autopilot.py` (ecommerce, 581L)
- `ecom_packager.py` (ecommerce, 284L)
- `micro_info_product_builder.py` (ecommerce, 448L)
- `nordic_ecom_arb.py` (ecommerce, 614L)
- `product_launch_automator.py` (ecommerce, 589L)
- `ad_budget_tracker.py` (monitor, 292L)
- `alpha_monitor.py` (monitor, 741L)
- `community_intel_scanner.py` (monitor, 1282L)
- `competitor_monitor.py` (monitor, 500L)
- `competitor_price_monitor.py` (monitor, 372L)
- `compliance_deadline_tracker.py` (monitor, 770L)
- `compliance_scanner.py` (monitor, 511L)
- `ecom_arb_scanner.py` (monitor, 431L)
- `ecom_deep_scanner.py` (monitor, 1095L)
- `fb_ads_library_scanner.py` (monitor, 309L)
- `freelance_demand_scanner.py` (monitor, 415L)
- `import_sourcing_scanner.py` (monitor, 1645L)
- `indeed_hiring_monitor.py` (monitor, 642L)
- `market_scanner.py` (monitor, 1262L)
- `quote_tweet_scanner.py` (monitor, 405L)
- `response_tracker.py` (monitor, 392L)
- `saas_product_scanner.py` (monitor, 357L)
- `sam_gov_monitor.py` (monitor, 455L)
- `system_health_monitor.py` (monitor, 858L)
- `telegram_community_monitor.py` (monitor, 658L)
- `trend_scanner.py` (monitor, 580L)
- `trending_products_scanner.py` (monitor, 407L)
- `triggering_events_monitor.py` (monitor, 461L)
- `unified_alpha_monitor.py` (monitor, 1656L)
- `viral_content_scanner.py` (monitor, 859L)
- `viral_product_scanner.py` (monitor, 1045L)
- `ai_video_content_pipeline.py` (orchestrator, 850L)
- `alpha_research_runner.py` (orchestrator, 828L)
- `app_clone_pipeline.py` (orchestrator, 538L)
- `approved_script_voice_runner.py` (orchestrator, 754L)
- `autonomous_orchestrator.py` (orchestrator, 562L)
- `autonomous_supervisor.py` (orchestrator, 1289L)
- `closed_loop_pipeline.py` (orchestrator, 612L)
- `competitor_sourcing_pipeline.py` (orchestrator, 768L)
- `content_trend_pipeline.py` (orchestrator, 524L)
- `daily_research_orchestrator.py` (orchestrator, 1054L)
- `daily_research_pipeline.py` (orchestrator, 986L)
- `freelance_pipeline.py` (orchestrator, 1332L)
- `ios_release_pipeline.py` (orchestrator, 996L)
- `local_biz_pipeline.py` (orchestrator, 836L)
- `overnight_orchestrator.py` (orchestrator, 308L)
- `client_onboarding.py` (outbound, 346L)
- `download_bulk_leads.py` (outbound, 398L)
- `freelance_packager.py` (outbound, 259L)
- `hexomatic_lead_gen.py` (outbound, 315L)
- `intelligent_lead_qualifier.py` (outbound, 1051L)
- `lead_enrichment.py` (outbound, 306L)
- `mass_outreach.py` (outbound, 911L)
- `quick_client_sample.py` (outbound, 211L)
- `alpha_auto_approver.py` (research, 196L)
- `alpha_auto_processor.py` (research, 796L)
- `alpha_screening.py` (research, 851L)
- `alpha_to_ops.py` (research, 1232L)
- `alpha_validator.py` (research, 743L)
- `backtest_alpha_DEPRECATED.py` (research, 375L)
- `signal_aggregator.py` (research, 840L)
- `trend_aggregator.py` (research, 409L)
- `website_signal_scorer.py` (research, 810L)
- `backup_system.py` (safety, 686L)
- `checkpoint_manager.py` (safety, 224L)
- `email_domain_health.py` (safety, 367L)
- `guardrails.py` (safety, 1110L)
- `log_rotator.py` (safety, 221L)
- `net_guard.py` (safety, 110L)
- `openrouter_budget_guard.py` (safety, 610L)
- `perpetual_guardian.py` (safety, 731L)
- `venture_map_health_check.py` (safety, 273L)
- `background_reddit_scraper.py` (scraper, 272L)
- `background_twitter_scraper.py` (scraper, 437L)
- `fiverr_gig_scraper.py` (scraper, 841L)
- `g2_reviewer_scraper.py` (scraper, 507L)
- `gov_tenders_scraper.py` (scraper, 1125L)
- `linkedin_events_scraper.py` (scraper, 417L)
- `local_biz_website_scraper.py` (scraper, 658L)
- `nationwide_scraper.py` (scraper, 411L)
- `producthunt_scraper.py` (scraper, 634L)
- `reddit_deep_scraper.py` (scraper, 640L)
- `sam_gov_scraper.py` (scraper, 455L)
- `savvy_lead_scraper.py` (scraper, 962L)
- `storeleads_ecom_scraper.py` (scraper, 353L)
- `twitter_alpha_scraper.py` (scraper, 1009L)
- `twitter_bookmarks_scraper.py` (scraper, 850L)
- `twitter_content_scraper.py` (scraper, 564L)
- `twitter_scraper_live.py` (scraper, 510L)
- `usaspending_scraper.py` (scraper, 621L)
- `algo_ban_prevention.py` (utility, 1425L)
- `app_clone_finder.py` (utility, 485L)
- `app_ideation_specialist.py` (utility, 1227L)
- `app_name_validator.py` (utility, 434L)
- `app_security_audit.py` (utility, 579L)
- `app_store_aso_optimizer.py` (utility, 708L)
- `auto_account_creator.py` (utility, 518L)
- `auto_clip_service.py` (utility, 1146L)
- `auto_dev_account_setup.py` (utility, 882L)
- `auto_rebalancer.py` (utility, 462L)
- `autonomous_factory.py` (utility, 1132L)
- `browser_image_gen.py` (utility, 479L)
- `bulk_landing_page_generator.py` (utility, 894L)
- `carousel_factory.py` (utility, 391L)
- `clawdbot_rbi_engine.py` (utility, 1059L)
- `cluely_compliance_pack.py` (utility, 353L)
- `cron_fleet_report.py` (utility, 285L)
- `engagement_bait_converter.py` (utility, 254L)
- `financial_intelligence.py` (utility, 1096L)
- `freshness_auditor.py` (utility, 173L)
- `full_context_swarm_dump.py` (utility, 420L)
- `greenlight_checker.py` (utility, 658L)
- `human_brief.py` (utility, 283L)
- `ios_rejection_screener.py` (utility, 1479L)
- `llm_backends.py` (utility, 776L)
- `market_size_estimator.py` (utility, 735L)
- `master_ops_executor.py` (utility, 347L)
- `meta_vision_swarm_audit.py` (utility, 566L)
- `monetization_engine.py` (utility, 1326L)
- `nsfw_safety_system.py` (utility, 1077L)
- `openclaw_hybrid.py` (utility, 1414L)
- `paper_trade.py` (utility, 1154L)
- `performance_optimizer.py` (utility, 939L)
- `persistent_memory.py` (utility, 510L)
- `personalize_demos.py` (utility, 326L)
- `playbook_enhancer.py` (utility, 714L)
- `printmaxx_brain.py` (utility, 813L)
- `printmaxx_quant_terminal.py` (utility, 2417L)
- `printmaxx_status.py` (utility, 163L)
- `prompt_logger.py` (utility, 458L)
- `publish_pack.py` (utility, 335L)
- `qa_auto_approver.py` (utility, 332L)
- `quality_gate.py` (utility, 1445L)
- `rbi_portfolio_optimizer.py` (utility, 351L)
- `reddit_pain_point_miner.py` (utility, 505L)
- `revenue_math_calculator.py` (utility, 256L)
- `saas_opportunity_engine.py` (utility, 1173L)
- `scheduled_runs_manager.py` (utility, 571L)
- `self_reply_funnel.py` (utility, 266L)
- `semantic_memory_search.py` (utility, 616L)
- `seo_competitor_analyzer.py` (utility, 736L)
- `theirstack_tech_intel.py` (utility, 335L)
- `twitter_copy_style_ingest.py` (utility, 81L)
- `uk_contracts_finder.py` (utility, 568L)
- `update_system_architecture.py` (utility, 394L)
- `venture_deep_scorer.py` (utility, 936L)
- `workflow_wirer.py` (utility, 1711L)
