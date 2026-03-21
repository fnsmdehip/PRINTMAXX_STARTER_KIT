# Growth Plan: Opened Google Search Console after weeks and honestly wasn't

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. programmatic SEO pages from discovered keywords
2. internal linking between existing deployed sites to boost GSC signals

## Budget Tier Strategies

### FREE
Monitor GSC weekly, create longtail pages for surprise keywords using generate-longtail skill, interlink 47 deployed sites

### LOW
$0-50/mo: Submit XML sitemaps for all surge.sh sites, use IndexNow API for faster crawling

### MID
$50-200/mo: Upgrade to custom domains for top-performing sites to boost domain authority

## Daily Actions

- [ ] BLOCKER: need GSC account verified for deployed sites (HUMAN ACTION)
- [ ] Build gsc_keyword_miner.py using GSC API to pull impressions/clicks/position data
- [ ] Identify high-impression low-click keywords (CTR optimization opportunities)
- [ ] Feed discovered keywords into content_multiplier.py for new page generation
- [ ] Schedule weekly cron Monday 7AM

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + generate-longtail"
}
```
