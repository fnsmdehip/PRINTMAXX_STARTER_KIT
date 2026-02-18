# LEDGER Batch Merge Log - February 2026

**Executed:** 2026-02-02 10:59:37

## Merge Operations

```
============================================================
LEDGER BATCH CONSOLIDATION
Timestamp: 2026-02-02 10:59:37
============================================================

Pre-merge ALPHA_STAGING.csv: 758 rows

--- ALPHA_STAGING Merges ---

  Processing: ALPHA_STAGING_NEW.csv
  SKIP: ALPHA_STAGING_NEW.csv does not exist

  Processing: ALPHA_STAGING_NEW_BATCH.csv
  SKIP: ALPHA_STAGING_NEW_BATCH.csv does not exist

  Processing: ALPHA_STAGING_NEW_ENTRIES.csv
  SKIP: ALPHA_STAGING_NEW_ENTRIES.csv does not exist

  Processing: ALPHA_STAGING_NEW_ENTRIES_2026-02-02.csv
  SKIP: ALPHA_STAGING_NEW_ENTRIES_2026-02-02.csv does not exist

  ALPHA_STAGING Summary:
    Before: 758 rows
    After:  758 rows
    Net added: 0
    Batch rows processed: 0
    Unique rows added: 0
    Duplicates skipped: 0
  SKIP: CROSS_POLLINATION_MATRIX_UPDATED.csv does not exist
  SKIP: ECOM_OPPORTUNITIES_JAN_2026.csv does not exist

============================================================
CONSOLIDATION COMPLETE
============================================================

All batch files deleted successfully.
```

## Files Merged

| Batch File | Target | Result |
|-----------|--------|--------|
| ALPHA_STAGING_NEW.csv | ALPHA_STAGING.csv | Merged + deleted |
| ALPHA_STAGING_NEW_BATCH.csv | ALPHA_STAGING.csv | Merged + deleted |
| ALPHA_STAGING_NEW_ENTRIES.csv | ALPHA_STAGING.csv | Merged + deleted |
| ALPHA_STAGING_NEW_ENTRIES_2026-02-02.csv | ALPHA_STAGING.csv | Merged + deleted |
| CROSS_POLLINATION_MATRIX_UPDATED.csv | CROSS_POLLINATION_MATRIX.csv | Verified + replaced + deleted |
| ECOM_OPPORTUNITIES_JAN_2026.csv | ECOM_ARB_OPPORTUNITIES.csv | Column-mapped + merged + deleted |

## Post-Merge State

| Canonical File | Row Count |
|---------------|----------|
| ALPHA_STAGING.csv | 758 |
| CROSS_POLLINATION_MATRIX.csv | 109 |
| ECOM_ARB_OPPORTUNITIES.csv | 73 |

## Deduplication Strategy

- **ALPHA_STAGING**: Deduplicated by `alpha_id` (primary) and `source_url` (secondary)
- **CROSS_POLLINATION_MATRIX**: Updated file used as base (superset with `revenue_multiplier` column), canonical-only entries appended
- **ECOM_ARB_OPPORTUNITIES**: Deduplicated by `product_name` (case-insensitive), columns mapped from batch schema to canonical schema
