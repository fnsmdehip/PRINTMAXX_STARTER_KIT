# MEGA SHEET - PRINTMAXX Consolidated Data

**Built:** 2026-01-27
**Total rows:** 2,512 across 10 tabs
**Total size:** 764KB

## Upload to Google Sheets

Upload each CSV as a separate tab in one Google Sheet:

| Tab # | File | Rows | Cols | What It Contains |
|-------|------|------|------|------------------|
| 1 | TAB1_MONEY_METHODS_MASTER.csv | 68 | 22 | All 46+ money methods + cross-pollination synergy data |
| 2 | TAB2_NICHES_MASTER.csv | 33 | 8 | All 33 niches with demos, themes, offer stacks |
| 3 | TAB3_ALPHA_MASTER.csv | 835 | 21 | All alpha entries (ALPHA_STAGING + watchlist + research) |
| 4 | TAB4_TOOLS_CHANNELS_MASTER.csv | 225 | 41 | Tools, marketing channels, MCP servers |
| 5 | TAB5_CONTENT_MASTER.csv | 569 | 36 | Content pipeline, calendar, structures, hashtags |
| 6 | TAB6_APPS_ECOM_MASTER.csv | 154 | 47 | App factory, clone opps, ecom arb, micro SaaS |
| 7 | TAB7_SOURCES_ACCOUNTS.csv | 158 | 23 | High signal sources (81+), social accounts |
| 8 | TAB8_OPERATIONS.csv | 213 | 49 | GTM priorities, affiliates, outreach, warmup |
| 9 | TAB9_EXPERIMENTS_METRICS.csv | 78 | 61 | A/B tests, experiments, funnel metrics, compliance |
| 10 | TAB10_RESEARCH_MISC.csv | 179 | 39 | Research findings, content farm alpha, SEO, repos |

## Source Files Consolidated

These 10 tabs combine 70+ individual LEDGER CSV files. No columns deleted. Source file tracked in `source_file` column where applicable.

## Quick Import (Google Sheets)

1. Create new Google Sheet
2. File > Import > Upload > select TAB1_MONEY_METHODS_MASTER.csv
3. Import to NEW SHEET, comma separator
4. Rename tab to "MONEY_METHODS"
5. Repeat for each TAB file
6. Rename tabs: NICHES, ALPHA, TOOLS_CHANNELS, CONTENT, APPS_ECOM, SOURCES, OPERATIONS, EXPERIMENTS, RESEARCH

## Key Columns for Agent Work

**TAB1 - Money Methods:**
- `method_id` - Primary key (MM001-MM046, CF001-CF013, AI001-AI008)
- `synergy_score` - Cross-pollination score (0-100)
- `monthly_potential_low/high` - Revenue range

**TAB3 - Alpha:**
- `alpha_id` - Primary key (ALPHA001-ALPHA835)
- `status` - APPROVED/PENDING_REVIEW/REJECTED
- `roi_potential` - HIGHEST/HIGH/MEDIUM/LOW

**TAB6 - Apps/Ecom:**
- `app_id` / `opportunity_id` - Primary keys
- `build_status` - Current development state
