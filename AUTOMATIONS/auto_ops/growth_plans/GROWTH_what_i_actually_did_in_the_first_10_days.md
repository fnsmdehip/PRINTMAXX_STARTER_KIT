# Growth Plan: what I actually did in the first 10 days to make Google noti

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo indirect (organic traffic to apps with payment links drives conversions — discounted from original claim, but 47 indexed properties compound)

---

## Tactics

1. Cross-link all 47+ PRINTMAXX properties to each other (internal link graph = free trust signals)
2. Submit all sitemaps to IndexNow (Bing/Yandex/etc index within hours, Google follows)
3. Add JSON-LD schema markup to all landing pages (rich results = higher CTR = faster trust)
4. Surge.sh Disallow:/ blocker — generate meta robots index,follow tags to override at page level where possible, or migrate priority pages to Netlify/Vercel free tier
5. Programmatic internal linking: each app landing page links to 3-5 related app pages
6. Ping aggregators: submit URLs to Google, Bing, IndexNow simultaneously

## Budget Tier Strategies

### FREE
IndexNow API (free, instant Bing indexing), sitemap pings, internal cross-linking across 47 properties, JSON-LD schema injection, meta tag optimization, Google Search Console manual URL inspection (when account created)

### LOW
$13/mo Surge Plus removes robots.txt Disallow:/ block on ALL sites — single highest-ROI spend available. Alternatively migrate top 5 revenue sites to Netlify free tier

### MID
$50-100/mo for HARO/Connectively responses to earn backlinks from journalists, or Netlify Pro for all properties with proper SEO headers

## Daily Actions

- [ ] 1. Read OPS/DEPLOYMENT_URLS.md to get all 47+ live property URLs
- [ ] 2. Crawl each URL checking: robots.txt, sitemap.xml, meta robots tags, canonical URLs, schema markup, page load speed
- [ ] 3. CRITICAL: Address surge.sh Disallow:/ blocker — inject <meta name='robots' content='index,follow'> into all HTML pages (overrides robots.txt for compliant crawlers)
- [ ] 4. Auto-generate sitemap.xml for each property that lacks one
- [ ] 5. Inject JSON-LD Organization + WebApplication schema into all app landing pages
- [ ] 6. Add internal cross-links: each page links to 3-5 sibling properties in footer
- [ ] 7. Submit all URLs to IndexNow API (free, key-based, supports Bing/Yandex/Naver)
- [ ] 8. Ping Google sitemap endpoint for each property
- [ ] 9. Log results to LEDGER/SEO_INDEXING_TRACKER.csv with columns: url, has_sitemap, has_schema, indexed_pages, last_checked
- [ ] 10. Cron weekly (Monday 5 AM) to re-audit and track indexing progress

## Tooling

```json
{
  "browser": "playwright for crawl audits",
  "email": "none",
  "content": "none"
}
```
