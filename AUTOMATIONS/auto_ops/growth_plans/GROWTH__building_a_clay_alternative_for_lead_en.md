# Growth Plan:  building a clay alternative for lead enrichment, would love

**Created:** 2026-03-20 18:09
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. List as Fiverr gig: 'I will enrich your lead list with emails, titles, and company data' ($50-150/batch)
2. Post on r/sales, r/agency, r/coldoutreach showing enrichment results vs Clay pricing
3. Twitter thread: 'Clay charges $349/mo. I built the same thing for $0. Here's the script.' with CTA to Gumroad
4. Use internally to improve our own cold outbound reply rates with better targeting
5. Package as digital product: 'Lead Enrichment Toolkit for Agencies' on Gumroad ($29-47)

## Budget Tier Strategies

### FREE
Post comparison content (our tool vs Clay pricing), list on Fiverr/Upwork, Reddit distribution in agency/sales subs, use internally for outbound enrichment, open-source lite version for GitHub stars

### LOW
$0-50/mo: Hunter.io paid tier for higher email lookup volume (150 vs 50/mo free), boost one Fiverr gig listing

### MID
$50-200/mo: Clearbit paid tier, proxy rotation for higher scrape volume, targeted Reddit/Twitter ads to agency owners

## Daily Actions

- [ ] Build lead_enrichment_engine.py with waterfall enrichment: Hunter.io free → Google dorking → company site scraping → LinkedIn Google cache
- [ ] Create DAG pipeline with 4 phases: ingest → enrich (parallel across sources) → score → output
- [ ] Wire output into existing cold outbound chain for internal use (immediate value)
- [ ] Create Fiverr gig listing draft in PRODUCTS/listings/ for lead enrichment service
- [ ] Create Gumroad product listing for the script as a digital product ($29-47)
- [ ] Generate 3 comparison tweets (our tool vs Clay pricing) + 1 thread for content queue
- [ ] Add cron job: daily 5 AM enrichment run on new leads from inbound pipeline
- [ ] Track enrichment hit rate and gig revenue in KPI dashboard

## Tooling

```json
{
  "browser": "playwright_mcp for Google cache scraping",
  "email": "custom cold email scripts feeding from enriched data",
  "content": "content_factory for comparison posts and threads"
}
```
