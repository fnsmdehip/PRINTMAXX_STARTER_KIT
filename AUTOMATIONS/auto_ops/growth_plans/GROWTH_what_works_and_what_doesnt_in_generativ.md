# Growth Plan: What Works and What Doesn’t in Generative Engine Optimizatio

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-75/mo indirect (incremental AI traffic to existing monetized pages)

---

## Tactics

1. Add statistics with source citations to all existing landing pages — LLMs prioritize citable content
2. Restructure H2/H3 headers as natural language questions matching how users ask AI chatbots
3. Add 'What is X' and 'How does X work' FAQ sections to every app landing page — these are primary GEO entry points
4. Get app pages mentioned on Reddit threads — Reddit is heavily indexed by LLMs
5. Build topical authority: create 3-5 interlinked pages per app niche rather than isolated pages
6. Add comparison tables with verifiable numbers — LLMs cite structured data
7. Target Perplexity via submitting pages to their index via sitemap pings

## Budget Tier Strategies

### FREE
Rewrite existing pages with GEO structure via claude -p batch processor. Post Q&A content on Reddit threads in target niches. Submit sitemaps. Add FAQ schema markup to all pages.

### LOW
$0-50/mo: Use Perplexity API ($5/mo) to test whether pages get cited. Run weekly citation tracking script against 20 target queries.

### MID
$50-200/mo: Sponsored placement on a high-DA niche site that LLMs heavily cite (e.g., guest post on IndieHackers, HN Show HN). Pays citation dividends for months.

## Daily Actions

- [ ] Scan LANDING/ and MONEY_METHODS/APP_FACTORY/builds/ for pages with <500 words or no FAQ section
- [ ] For each page: claude -p prompt to add Q&A section, statistics with citations, and a 'How it works' block using GEO best practices
- [ ] Add FAQ schema JSON-LD to all rewritten pages
- [ ] Restructure existing H2/H3s to question format where missing
- [ ] Submit updated sitemaps to search consoles
- [ ] Wire into existing brand_mentions chain to track citation appearances weekly

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "claude -p for batch page rewriting + content_repurposer.py"
}
```
