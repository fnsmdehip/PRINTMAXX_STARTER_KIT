# Growth Plan:  post: my forgotten side project outranks zillow for dozens 

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Programmatic SEO at scale: generate 50-200 hyper-specific pages per niche targeting long-tail queries big players ignore
2. Internal linking web: cross-link all deployed surge sites to pass authority between niche clusters
3. Schema markup on every generated page for rich snippets (FAQ, HowTo, Product) to steal SERP real estate
4. Index forcing: submit sitemaps to Google Search Console + Bing Webmaster + IndexNow API
5. Content freshness signal: auto-update pages monthly with new data points to maintain ranking edge

## Budget Tier Strategies

### FREE
Programmatic page gen via claude -p, deploy to existing surge domains, manual sitemap submission, internal cross-linking between 47+ live sites

### LOW
$13/mo Surge Plus for custom robots.txt (currently blocked by Disallow: / on free tier — this is the #1 SEO blocker), or migrate to Netlify/Cloudflare Pages free tier

### MID
$50-100/mo for Ahrefs Lite or paid SERP API to automate keyword gap discovery at scale instead of manual scraping

## Daily Actions

- [ ] 1. Audit existing 47+ deployed pages for current keyword rankings using free SERP check tools
- [ ] 2. Identify 10 niche clusters where our apps/pages already have some authority (prayer, fitness, streak apps, MCP marketplace)
- [ ] 3. For each cluster, find 20-50 long-tail queries where top results are thin/generic content from big players
- [ ] 4. Generate programmatic pages targeting those gaps using claude -p with niche-specific templates
- [ ] 5. Deploy to existing surge domains with proper internal linking
- [ ] 6. Submit sitemaps and use IndexNow for fast crawling
- [ ] 7. Track rankings weekly and double down on clusters showing traction
- [ ] 8. CRITICAL BLOCKER: Surge free tier serves Disallow: / — must upgrade to Plus ($13/mo) or migrate to Netlify/Cloudflare Pages before any SEO benefit is possible

## Tooling

```json
{
  "browser": "playwright for SERP scraping",
  "email": "none",
  "content": "claude -p for page generation + existing generate-longtail skill"
}
```
