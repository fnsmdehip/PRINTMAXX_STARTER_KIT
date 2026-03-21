# Growth Plan: alpha_id,source,source_url,category,tactic,roi_potential,pri

**Created:** 2026-03-20 23:12
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0/mo

---

## Tactics


## Budget Tier Strategies

### FREE
No growth tactics applicable — entry contains no method

### LOW
N/A

### MID
N/A

## Daily Actions

- [ ] Add header-row filter to orphan_doc_scanner.py: skip any row where tactic field matches CSV column names pattern (alpha_id|source_url|roi_potential)
- [ ] Add PreToolUse hook on alpha_auto_processor.py — reject entries where extracted_method is empty or equals the column header string
- [ ] Backfill: search ALPHA_STAGING.csv for all rows with tactic starting with 'alpha_id,' and mark as REJECTED_MALFORMED
- [ ] Add gap_detection alert: if same ALPHA_ID appears in procedural memory as previously integrated with $0 outcome, flag as duplicate before re-processing

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "none"
}
```
