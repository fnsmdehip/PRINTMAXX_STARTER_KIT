# Growth Plan:  to get your website seen on chatgpt, gemini, and the rest, 

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0 direct but $200-2000/mo indirect via AI chatbot referral traffic across 47+ sites

---

## Tactics

1. Submit ALL 47+ sites — massive surface area at zero marginal cost
2. Include structured data (JSON-LD) alongside llms.txt for double coverage
3. Add llms.txt generation to app_factory_autopilot.py so every NEW app auto-gets one
4. Cross-link between llms.txt files to create an internal recommendation web for AI crawlers
5. Monitor AI chatbot responses weekly to measure discoverability lift
6. Submit to Perplexity Pages, Bing Chat index, and Google SGE structured data as they emerge

## Budget Tier Strategies

### FREE
Generate llms.txt for all 47+ sites, submit to free directories, add to app factory pipeline so every new app auto-generates one. Monitor AI chatbot mentions manually.

### LOW
$0-50/mo: Use a monitoring service or custom scraper to track AI chatbot mentions of our products weekly. Submit to paid llms.txt premium directories if they emerge.

### MID
$50-200/mo: Paid GEO monitoring tools, submit to enterprise AI directories, create rich structured data (Schema.org) alongside llms.txt for maximum AI crawlability.

## Daily Actions

- [ ] 1. Parse OPS/DEPLOYMENT_URLS.md to get all 47+ live site URLs and their descriptions
- [ ] 2. Create llms.txt template with fields: title, description, features, pricing, url, contact
- [ ] 3. Generate llms.txt for each site using Claude (batch via claude -p for speed)
- [ ] 4. Deploy llms.txt to each surge.sh site root (surge deploy with llms.txt included)
- [ ] 5. Submit each site URL to llmstxt.site and directory.llmstxt.cloud via Playwright automation
- [ ] 6. Add PostToolUse hook to app_factory_autopilot.py: auto-generate llms.txt for every new app deploy
- [ ] 7. Add weekly cron (Sunday 4 AM) to check for new sites and submit any missing ones
- [ ] 8. Log all submissions to LEDGER/GEO_SUBMISSIONS.csv for tracking
- [ ] 9. Weekly KPI: query ChatGPT/Gemini/Perplexity for our product names to measure discoverability

## Tooling

```json
{
  "browser": "playwright for directory submission",
  "email": "none",
  "content": "claude -p for generating llms.txt summaries per site"
}
```
