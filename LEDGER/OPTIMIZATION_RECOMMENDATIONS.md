# PRINTMAXX Optimization Recommendations

Generated: 2026-02-12 08:04

## Action Items (46 total)

| # | Priority | Action | Script | Impact | Effort |
|---|----------|--------|--------|--------|--------|
| 1 | P0 | FIX_NEEDED | daily_nocost_rbi_scanner | HIGH | LOW |
| 2 | P0 | BATCH_OPTIMIZE | lead_scrapers | HIGH | LOW |
| 3 | P0 | FIX_BOTTLENECK | active_pipeline | CRITICAL | VARIES |
| 4 | P1 | FIX_NEEDED | leads_Houston_restaurant | MEDIUM | LOW |
| 5 | P1 | FIX_NEEDED | leads_Dallas_dentist | MEDIUM | LOW |
| 6 | P1 | FIX_NEEDED | leads_Dallas_restaurant | MEDIUM | LOW |
| 7 | P1 | FIX_NEEDED | leads_Miami_restaurant | MEDIUM | LOW |
| 8 | P1 | FIX_NEEDED | leads_Miami_plumber | MEDIUM | LOW |
| 9 | P1 | FIX_NEEDED | leads_Miami_lawyer | MEDIUM | LOW |
| 10 | P1 | FIX_NEEDED | leads_Phoenix_restaurant | MEDIUM | LOW |
| 11 | P1 | FIX_NEEDED | leads_Phoenix_lawyer | MEDIUM | LOW |
| 12 | P1 | FIX_NEEDED | leads_Chicago_restaurant | MEDIUM | LOW |
| 13 | P1 | FIX_NEEDED | leads_Chicago_lawyer | MEDIUM | LOW |
| 14 | P1 | FIX_NEEDED | leads_Atlanta_restaurant | MEDIUM | LOW |
| 15 | P1 | FIX_NEEDED | leads_Atlanta_lawyer | MEDIUM | LOW |
| 16 | P1 | FIX_NEEDED | leads_Denver_restaurant | MEDIUM | LOW |
| 17 | P1 | FIX_NEEDED | leads_Denver_plumber | MEDIUM | LOW |
| 18 | P1 | FIX_NEEDED | leads_Denver_lawyer | MEDIUM | LOW |
| 19 | P1 | FIX_NEEDED | leads_Seattle_dentist | MEDIUM | LOW |
| 20 | P1 | FIX_NEEDED | leads_Seattle_restaurant | MEDIUM | LOW |
| 21 | P1 | FIX_NEEDED | viral_product_scanner | MEDIUM | LOW |
| 22 | P1 | FIX_NEEDED | linkedin_events | MEDIUM | LOW |
| 23 | P1 | FIX_NEEDED | g2_reviewers | MEDIUM | LOW |
| 24 | P1 | FIX_NEEDED | indeed_hiring | MEDIUM | LOW |
| 25 | P1 | FIX_NEEDED | nordic_ecom | MEDIUM | LOW |
| 26 | P1 | FIX_NEEDED | app_clone_finder | MEDIUM | LOW |
| 27 | P1 | FIX_NEEDED | leads_Houston_dentist | MEDIUM | LOW |
| 28 | P1 | FIX_NEEDED | leads_Houston_plumber | MEDIUM | LOW |
| 29 | P1 | FIX_NEEDED | leads_Houston_lawyer | MEDIUM | LOW |
| 30 | P1 | FIX_NEEDED | leads_Dallas_lawyer | MEDIUM | LOW |
| 31 | P1 | FIX_NEEDED | leads_Denver_dentist | MEDIUM | LOW |
| 32 | P1 | FIX_NEEDED | leads_Seattle_plumber | MEDIUM | LOW |
| 33 | P1 | FIX_NEEDED | leads_Seattle_lawyer | MEDIUM | LOW |
| 34 | P2 | INCREASE_FREQUENCY | platform_meta_monitor | MEDIUM | LOW |
| 35 | P2 | INCREASE_FREQUENCY | niche_meta_detector | MEDIUM | LOW |
| 36 | P2 | INCREASE_FREQUENCY | gov_tenders_refresh | MEDIUM | LOW |
| 37 | P2 | INCREASE_FREQUENCY | usaspending_refresh | MEDIUM | LOW |
| 38 | P2 | INCREASE_FREQUENCY | sam_gov_monitor | MEDIUM | LOW |
| 39 | P2 | INCREASE_FREQUENCY | alpha_screening | MEDIUM | LOW |
| 40 | P2 | INCREASE_FREQUENCY | alpha_validator | MEDIUM | LOW |
| 41 | P2 | INCREASE_FREQUENCY | platform_algo_detection | MEDIUM | LOW |
| 42 | P2 | INCREASE_FREQUENCY | hashtag_audio_tracking | MEDIUM | LOW |
| 43 | P2 | INCREASE_FREQUENCY | platform_rpm_tracking | MEDIUM | LOW |
| 44 | P2 | INCREASE_FREQUENCY | creator_program_monitoring | MEDIUM | LOW |
| 45 | P2 | INCREASE_FREQUENCY | aso_keyword_research | MEDIUM | LOW |
| 46 | P2 | INCREASE_FREQUENCY | run_all_research_ops | MEDIUM | LOW |

## Quick Fixes (P0/P1, LOW effort)

- **daily_nocost_rbi_scanner**: 0% success over 3 runs
- **lead_scrapers**: 24 lead scrapers timing out. Use --limit 10, rotate cities nightly
- **leads_Houston_restaurant**: 0% success over 3 runs
- **leads_Dallas_dentist**: 0% success over 3 runs
- **leads_Dallas_restaurant**: 0% success over 3 runs

## Script Health

| Script | Rate | Trend |
|--------|------|-------|
| alpha_screening | 100% | STABLE |
| alpha_validator | 100% | STABLE |
| app_clone_finder | 0% | STABLE |
| aso_keyword_research | 100% | STABLE |
| creator_program_monitoring | 100% | STABLE |
| daily_nocost_rbi_scanner | 0% | STABLE |
| ecom_arb_scanner | 100% | STABLE |
| g2_reviewers | 0% | STABLE |
| gov_tenders_refresh | 100% | STABLE |
| hashtag_audio_tracking | 100% | STABLE |
| indeed_hiring | 0% | STABLE |
| leads_Atlanta_dentist | 67% | STABLE |
| leads_Atlanta_lawyer | 0% | STABLE |
| leads_Atlanta_plumber | 67% | STABLE |
| leads_Atlanta_restaurant | 0% | STABLE |
| leads_Chicago_dentist | 67% | STABLE |
| leads_Chicago_lawyer | 0% | STABLE |
| leads_Chicago_plumber | 67% | STABLE |
| leads_Chicago_restaurant | 0% | STABLE |
| leads_Dallas_dentist | 0% | STABLE |
| leads_Dallas_lawyer | 33% | STABLE |
| leads_Dallas_plumber | 67% | STABLE |
| leads_Dallas_restaurant | 0% | STABLE |
| leads_Denver_dentist | 33% | STABLE |
| leads_Denver_lawyer | 0% | STABLE |
| leads_Denver_plumber | 0% | STABLE |
| leads_Denver_restaurant | 0% | STABLE |
| leads_Houston_dentist | 33% | STABLE |
| leads_Houston_lawyer | 33% | STABLE |
| leads_Houston_plumber | 33% | STABLE |
| leads_Houston_restaurant | 0% | STABLE |
| leads_Miami_dentist | 67% | STABLE |
| leads_Miami_lawyer | 0% | STABLE |
| leads_Miami_plumber | 0% | STABLE |
| leads_Miami_restaurant | 0% | STABLE |
| leads_Phoenix_dentist | 67% | STABLE |
| leads_Phoenix_lawyer | 0% | STABLE |
| leads_Phoenix_plumber | 67% | STABLE |
| leads_Phoenix_restaurant | 0% | STABLE |
| leads_Seattle_dentist | 0% | STABLE |
| leads_Seattle_lawyer | 33% | STABLE |
| leads_Seattle_plumber | 33% | STABLE |
| leads_Seattle_restaurant | 0% | STABLE |
| linkedin_events | 0% | STABLE |
| niche_meta_detector | 100% | STABLE |
| nordic_ecom | 0% | STABLE |
| platform_algo_detection | 100% | STABLE |
| platform_meta_monitor | 100% | STABLE |
| platform_rpm_tracking | 100% | STABLE |
| run_all_research_ops | 100% | STABLE |
| sam_gov_monitor | 100% | STABLE |
| trending_products | 100% | STABLE |
| usaspending_refresh | 100% | STABLE |
| viral_content_scanner | 67% | STABLE |
| viral_product_scanner | 0% | STABLE |
