# Growth Plan: # Entity SEO + Agent-Readiness implementation playbook  **Cr

**Created:** 2026-03-20 18:10
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo indirect (SEO compound effect over 3-6 months, improves CTR on existing pages by 15-30% via rich snippets)

---

## Tactics

1. structured data markup for rich snippets in Google
2. AI agent readiness headers for Perplexity/ChatGPT citation
3. FAQ schema on all landing pages to capture zero-click featured snippets

## Budget Tier Strategies

### FREE
JSON-LD schema injection across all 47+ sites, FAQ/HowTo markup on landing pages, OpenGraph + meta description optimization for AI crawlers, sitemap.xml generation with lastmod dates

### LOW
$0-20/mo for Google Search Console API monitoring of rich result performance

### MID
$50-100/mo for Bing Webmaster + IndexNow API for faster crawl of schema changes

## Daily Actions

- [ ] 1. Build entity_seo_injector.py that glob-scans LANDING/ and MONEY_METHODS/*/builds/ for index.html files
- [ ] 2. For each page: detect page type (app landing, affiliate, tool page) and generate appropriate JSON-LD schema (Product, SoftwareApplication, FAQPage, HowTo, Organization)
- [ ] 3. Inject schema into <head> of each index.html, add AI-parsability meta tags (structured headings, canonical URLs, description meta)
- [ ] 4. Generate/update sitemap.xml with lastmod timestamps for all modified pages
- [ ] 5. Add to cron: Sunday 4 AM weekly run
- [ ] 6. Wire into existing seo_aso_optimizer swarm agent as a subtask

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "entity_seo_injector.py + existing SEO scripts"
}
```
