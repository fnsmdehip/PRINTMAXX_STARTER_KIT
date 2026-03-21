# Growth Plan: extracted signal: hit $2,800 in january but traffic hasn't g

**Created:** 2026-03-20 18:09
**Venture:** MONETIZE
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Programmatic internal linking between all affiliate pages to boost domain authority signals
2. Content freshness hack: auto-update dates and add 2026 data points weekly
3. Parasite SEO: republish comparison content on Medium/dev.to with canonical back to our pages
4. Reddit seeding: post genuine answers in r/juststart r/affiliatemarketing linking to our comparison pages where relevant
5. Index forcing: Google Indexing API submission on every content refresh

## Budget Tier Strategies

### FREE
Internal linking optimization, content freshness updates via claude -p, parasite SEO on Medium/dev.to/LinkedIn articles, Reddit value-add seeding, Google Search Console monitoring

### LOW
$10-30/mo for a backlink checker API (or scrape free alternatives) to detect lost links causing plateau

### MID
$50-150/mo for guest post placements on DA40+ sites linking to top affiliate pages

## Daily Actions

- [ ] Inventory all deployed affiliate pages from LANDING/affiliate-pages/ and OPS/DEPLOYMENT_URLS.md
- [ ] Build affiliate_seo_plateau_detector.py with 4-phase DAG: audit → diagnose → fix → deploy
- [ ] Audit phase: crawl each page, check Google index via site: query, scrape SERP position for target keywords
- [ ] Diagnose phase: flag pages with no ranking movement in 30+ days, compare content freshness vs top 3 competitors
- [ ] Fix phase: auto-refresh stale content sections with updated 2026 data, add internal crosslinks between all affiliate pages, optimize meta tags
- [ ] Deploy phase: redeploy fixed pages to surge, ping Google Indexing API
- [ ] Add weekly cron (Monday 7 AM) to run full audit cycle
- [ ] Track KPI: pages indexed, SERP positions, affiliate click-through rates

## Tooling

```json
{
  "browser": "playwright_mcp",
  "email": "none",
  "content": "claude_p_content_refresh"
}
```
