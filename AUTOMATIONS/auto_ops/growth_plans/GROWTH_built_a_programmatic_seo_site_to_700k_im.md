# Growth Plan: Built a programmatic SEO site to 700K impressions in 12 mont

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo

---

## Tactics

1. Programmatic internal linking between all generated pages to boost crawl depth
2. Auto-submit sitemaps to Google/Bing on each batch deploy
3. Cross-link from existing 47 deployed surge sites to new pSEO pages for domain authority transfer
4. Repurpose top-performing pSEO pages into social content via content_repurposer.py
5. Target zero-volume longtails that aggregate to massive impressions (the real play)

## Budget Tier Strategies

### FREE
GSC free, custom SERP scraper, Claude Max for content gen, surge free tier deployment, auto-sitemap submission, internal linking automation

### LOW
$13/mo Surge Plus for custom robots.txt (already in P0 blockers) — enables proper crawling of all pSEO pages

### MID
$50-100/mo for Cloudflare Pro with better caching + edge SEO headers, or Netlify Pro for split testing page templates

## Daily Actions

- [ ] Wire into existing generate-longtail skill — it already does bulk longtail page creation
- [ ] Build keyword cluster scraper using Google autocomplete API (free, no key needed) + People Also Ask scraping via Playwright
- [ ] Create page template system with 3-5 layouts that auto-populate from keyword + Claude-generated content
- [ ] Deploy weekly batches of 50-100 pages to existing surge sites using programmatic_seo_scaler.py
- [ ] Auto-generate sitemaps and submit to GSC API
- [ ] Cross-link new pSEO pages with existing 47 deployed sites for link equity
- [ ] Weekly cron (Monday 4 AM) runs full pipeline: discover keywords → generate pages → deploy → submit
- [ ] Track via GSC impressions — kill clusters under 100 impressions/mo after 60 days

## Tooling

```json
{
  "browser": "playwright for SERP scraping",
  "email": "none",
  "content": "content_multiplier.py + generate-longtail skill + claude -p for bulk page gen"
}
```
