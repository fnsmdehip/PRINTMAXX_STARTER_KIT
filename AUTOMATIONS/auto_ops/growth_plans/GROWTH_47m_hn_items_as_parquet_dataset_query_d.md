# Growth Plan: 47M HN items as Parquet dataset. Query directly instead of s

**Created:** 2026-03-20 13:50
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (better alpha mining → faster method discovery → compounding across all ventures)

---

## Tactics

1. Publish weekly HN trend report threads on Twitter/LinkedIn for authority building
2. Use trend data to identify rising tools before competition — create comparison landing pages
3. Cross-reference HN trends with Reddit/Twitter alpha for compound signal detection
4. Mine Show HN posts with high engagement for app factory cloning opportunities

## Budget Tier Strategies

### FREE
Publish trend analysis threads across platforms. Use data to pick content farm topics with proven HN traction. Cross-pollinate findings into all ventures.

### LOW
$0-50/mo: Boost top trend posts. Target emerging niches with landing pages before saturation.

### MID
$50-200/mo: Paid distribution of trend reports as lead magnets. Newsletter sponsorships in HN-adjacent dev communities.

## Daily Actions

- [ ] pip3 install duckdb pyarrow — query Parquet with SQL, zero external service deps
- [ ] Create hn_parquet_alpha_miner.py with DuckDB: download dataset, SQL query templates for 4 categories (tools, revenue, competitors, niches)
- [ ] Query templates: Show HN with score>50 last 90d, posts containing MRR/ARR/revenue/profit keywords, posts mentioning competitor names from COMPETITIVE_INTEL, emerging topic clusters via title TF-IDF
- [ ] Dedup against existing ALPHA_STAGING entries before staging new findings
- [ ] Wire output into ALPHA_STAGING.csv as source=hn_parquet_bulk
- [ ] Add hn_parquet_bulk to auto_approve trusted sources list
- [ ] Schedule weekly cron Monday 5 AM for fresh dataset pull + full scan
- [ ] Update OPS/PRINTMAXX_SYSTEM_MAP.md with new script in L2 Intelligence layer

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for trend threads"
}
```
