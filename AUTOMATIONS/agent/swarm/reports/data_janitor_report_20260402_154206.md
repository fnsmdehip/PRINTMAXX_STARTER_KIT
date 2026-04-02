# DATA JANITOR REPORT

**Generated:** 2026-04-02 15:41:51

## Statistics

- Duplicates removed: 310
- Stale entries archived: 0
- Logs compressed: 22
- JSON files validated: 505
- JSON files fixed: 0
- Large directories flagged: 2
- Total size reduction: 1.07MB

## Detailed Report

🧹 DATA JANITOR v2 - Starting full cycle


============================================================
  STEP 1: DEDUPLICATE CSVs
============================================================
Found 175 CSV files to scan
  TREND_SIGNALS.csv: Found 310 duplicates (kept 256 unique)

============================================================
  STEP 2: ARCHIVE STALE PENDING_REVIEW ENTRIES
============================================================

============================================================
  STEP 3: ARCHIVE OLD LOGS
============================================================
  Found 69 log files
  Compressed lean_mode.log: 0.00MB → 0.00MB (0.00MB saved)
  Compressed trend_agg_2026-03-28.log: 0.00MB → 0.00MB (-0.00MB saved)
  Compressed ceo_agent.log: 0.70MB → 0.05MB (0.65MB saved)
  Compressed factory_2026-03-29.log: 0.01MB → 0.00MB (0.00MB saved)
  Compressed cognitive_engine.log: 0.00MB → 0.00MB (0.00MB saved)
  Compressed daily_research_pipeline.log: 0.07MB → 0.01MB (0.06MB saved)
  Compressed browser_image_gen_2026-03-29.log: 0.00MB → 0.00MB (0.00MB saved)
  Compressed ecom_arb_2026-03-29.log: 0.00MB → 0.00MB (-0.00MB saved)
  Compressed security_audit.log: 0.00MB → 0.00MB (0.00MB saved)
  Compressed orphan_doc_scanner.log: 0.01MB → 0.00MB (0.01MB saved)
  Compressed unified_alpha_2026-03-28.log: 0.00MB → 0.00MB (0.00MB saved)
  Compressed ecom_arb_2026-03-30.log: 0.00MB → 0.00MB (-0.00MB saved)
  Compressed browser_image_gen_2026-03-30.log: 0.00MB → 0.00MB (0.00MB saved)
  Compressed daily_research.log: 0.26MB → 0.03MB (0.23MB saved)
  Compressed factory_2026-03-30.log: 0.01MB → 0.00MB (0.00MB saved)
  Compressed launchd_scrapers_err.log: 0.00MB → 0.00MB (-0.00MB saved)
  Compressed launchd_claude.log: 0.00MB → 0.00MB (-0.00MB saved)
  Compressed guardian_2026-03-29.log: 0.01MB → 0.00MB (0.01MB saved)
  Compressed competitive_intel_cycle.log: 0.08MB → 0.01MB (0.07MB saved)
  Compressed guardian_2026-03-28.log: 0.01MB → 0.00MB (0.01MB saved)
  Compressed surge_deploy.log: 0.02MB → 0.00MB (0.02MB saved)
  Compressed competitor_appstore.log: 0.00MB → 0.00MB (0.00MB saved)

============================================================
  STEP 4: VALIDATE JSON STATE FILES
============================================================
  Found 505 JSON files to validate

============================================================
  STEP 5: FIND ORPHAN FILES
============================================================
  Large directories (>100MB):
    AUTOMATIONS: 2205.2MB
    LEDGER: 378.5MB

============================================================
  STEP 6: DIRECTORY SIZE REPORT
============================================================

Top directories by size:
  MONEY_METHODS                 :     2741.4MB
  AUTOMATIONS                   :     2205.2MB
  LEDGER                        :      378.5MB
  CONTENT                       :       45.2MB
  LANDING                       :        7.6MB
  PRODUCTS                      :        7.1MB
  DIGITAL_PRODUCTS              :        4.9MB

============================================================
  FINAL REPORT
============================================================