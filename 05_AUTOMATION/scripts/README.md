# AUTOMATIONS - Script Index

All automation scripts for the PRINTMAXX system. Most scripts use Python stdlib only (csv, json, argparse, pathlib). Scripts needing external packages are noted.

## Quick start

```bash
pip install -r /path/to/PRINTMAXX_STARTER_KITttttt/requirements.txt
```

## Developer tools (CLI)

| Script | Purpose | Usage |
|--------|---------|-------|
| `ledger_cli.py` | Query LEDGER CSV files | `python3 ledger_cli.py stats` |
| `system_health_check.py` | Validate infrastructure integrity | `python3 system_health_check.py` |
| `revenue_sync.py` | Sync FINANCIALS P&L and dashboard | `python3 revenue_sync.py` |
| `content_pipeline.py` | 15-output content chain + QA queue | `python3 content_pipeline.py create --source "text" --category APP_FACTORY` |
| `method_stack_calculator.py` | Find optimal method combinations | `python3 method_stack_calculator.py top` |
| `roi_analyzer.py` | ROI analysis across all methods | `python3 roi_analyzer.py report` |
| `alpha_to_method.py` | Route approved alpha to method files | `python3 alpha_to_method.py route` |
| `app_batch_fix.py` | Apply templates to all SDK54 apps | `python3 app_batch_fix.py audit` |

## Quant infrastructure (dashboards)

| Script | Purpose | Requires |
|--------|---------|----------|
| `agent_monitor.py` | Live agent progress tracking | `rich` |
| `quant_dashboard.py` | 6-panel Bloomberg-style TUI | `textual`, `rich` |
| `backtest_alpha.py` | Alpha validation (0-100 scoring) | stdlib |
| `paper_trade.py` | Minimal capital testing system | stdlib |

## Research and data

| Script | Purpose | Usage |
|--------|---------|-------|
| `twitter_alpha_scraper.py` | Scrape Twitter bookmarks + accounts | `python3 twitter_alpha_scraper.py --all` |
| `daily_alpha_extractor.py` | Extract alpha from various sources | |
| `research_orchestrator.py` | Coordinate multi-source research | |
| `alpha_processor.py` | Process raw alpha into staging format | |

## Content and social

| Script | Purpose |
|--------|---------|
| `tweet_scraper.py` | Scrape tweets for alpha |
| `quick_tweet_scraper.py` | Fast tweet extraction |
| `competitor_review_mining.py` | Mine competitor app reviews |
| `review_keyword_mining.py` | Extract keywords from reviews |
| `test_report_generator.py` | Generate test reports |
| `va_dashboard.py` | VA task tracking dashboard |

## App factory

| Script | Purpose |
|--------|---------|
| `app_batch_fix.py` | Batch apply missing templates to apps |
| `asset_generator.py` | Generate app icons and assets |
| `bulk_test_runner.py` | Run tests across all apps |
| `translation_export.py` | Export strings for translation |

## Tracking and analytics

| Script | Purpose |
|--------|---------|
| `affiliate_tracker.py` | Track affiliate link performance |
| `ab_test_analyzer.py` | Analyze A/B test results |

## Common commands

```bash
# Daily workflow
python3 AUTOMATIONS/system_health_check.py        # Check system health
python3 AUTOMATIONS/ledger_cli.py stats            # LEDGER overview
python3 AUTOMATIONS/revenue_sync.py                # Update financials
python3 AUTOMATIONS/roi_analyzer.py report         # Full ROI report

# Alpha management
python3 AUTOMATIONS/ledger_cli.py count ALPHA_STAGING --group-by status
python3 AUTOMATIONS/backtest_alpha.py --pending     # Score pending alpha
python3 AUTOMATIONS/alpha_to_method.py unrouted     # Show unrouted alpha

# App management
python3 AUTOMATIONS/app_batch_fix.py audit          # Audit all apps
python3 AUTOMATIONS/app_batch_fix.py fix-all        # Apply all fixes
python3 AUTOMATIONS/app_batch_fix.py status         # Completion status

# Content
python3 AUTOMATIONS/content_pipeline.py stats       # Pipeline overview
python3 AUTOMATIONS/content_pipeline.py queue       # QA queue

# Method stacking
python3 AUTOMATIONS/method_stack_calculator.py top   # Top synergies
python3 AUTOMATIONS/method_stack_calculator.py for MM001  # Stacks for method

# Monitoring (separate terminal)
python3 AUTOMATIONS/agent_monitor.py                # Live agent tracking
python3 AUTOMATIONS/quant_dashboard.py              # Bloomberg-style dashboard
```

## Directory structure

```
AUTOMATIONS/
  *.py                    # Main automation scripts
  alpha_extraction/       # Alpha extraction utilities
  app_factory/            # App-specific automation
  content_generation/     # Content generation scripts
  content_posting/        # Posting queue and schedules
  cross_pollination/      # Cross-pollination analysis
  daily_research/         # Daily research utilities
  github_actions/         # CI/CD workflows
  lead_enrichment/        # Lead processing
  logs/                   # Automation logs
  n8n/                    # n8n workflow configs
  n8n_workflows/          # n8n workflow definitions
  playwright_scripts/     # Browser automation
  prompt_service/         # Prompt management
  python_scripts/         # Utility scripts
  ralph_dashboard/        # Ralph monitoring
  revenue_tracking/       # Revenue tracking utils
  scripts/                # Misc scripts
  seo_monitoring/         # SEO tracking
  social/                 # Social media automation
  social_metrics/         # Social analytics
  tests/                  # Test suite
  tiktok_viral_scraper/   # TikTok trend scraping
  twitter_scraper_output/ # Twitter scraper data
  x_bookmarks/            # X/Twitter bookmark extraction
```
