# Growth Plan: Looking for Affiliates (10% flat commission fee is paid)

**Created:** 2026-03-20 13:50
**Venture:** MONETIZE
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Cross-promote affiliate products in existing landing pages and content posts
2. Bundle affiliate recommendations into existing digital products as resource lists

## Budget Tier Strategies

### FREE
Embed affiliate links in existing 47+ deployed landing pages and content queue posts. Use content_repurposer to generate comparison/review posts featuring affiliate products.

### LOW
$0-50/mo — Boost top-performing affiliate review posts on social platforms

### MID
$50-200/mo — Run targeted ads to high-converting affiliate landing pages

## Daily Actions

- [ ] Build affiliate_program_scout.py using Reddit JSON API (no browser needed) to scrape r/Affiliatemarketing for recruitment posts
- [ ] Filter: commission >= 10%, digital product preferred, niche alignment with productivity/faith/dev
- [ ] Append qualified programs to LEDGER/AFFILIATE_PROGRAMS_FOUND.csv with signup URL, commission rate, product type
- [ ] Schedule weekly cron (Monday 7 AM) to scan for new posts
- [ ] Wire output into existing AFFILIATE_OPPORTUNITIES docs for human batch signup

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for review posts"
}
```
