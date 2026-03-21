# Growth Plan: Month 2 of serious restructure

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. topical authority clustering on deployed sites
2. internal link optimization for SEO juice flow
3. content consolidation to reduce index bloat
4. programmatic meta tag optimization across all 47 sites

## Budget Tier Strategies

### FREE
Audit existing 47 sites with custom script, prune thin pages, consolidate overlapping content, fix internal links, submit updated sitemaps to GSC

### LOW
$10-20/mo for Cloudflare Pro on top-performing sites for edge caching + faster crawl

### MID
$50-100/mo for backlink building to restructured hub pages via guest posting

## Daily Actions

- [ ] 1. Crawl all 47 deployed sites from OPS/DEPLOYMENT_URLS.md — collect page count, word count, meta tags, internal links per page
- [ ] 2. Score each page: thin (<500 words), orphan (0 internal links in), duplicate (>60% content overlap with another page)
- [ ] 3. Generate restructure plan: merge candidates, prune list, hub-spoke cluster map per niche
- [ ] 4. Auto-generate improved internal link blocks for hub pages
- [ ] 5. Output report to OPS/CONTENT_RESTRUCTURE_REPORT.md with prioritized actions
- [ ] 6. Feed restructure insights to content_factory for next generation cycle

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + existing landing page builds"
}
```
