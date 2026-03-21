# Growth Plan: affiliate review structure. honesty converts better long-ter

**Created:** 2026-03-20 18:35
**Venture:** MONETIZE
**Budget Tier:** FREE
**Revenue Est:** $50-500/mo

---

## Tactics

1. Programmatic SEO: generate longtail review pages for '[tool] vs [tool]' and '[tool] review 2026' queries
2. Reddit seeding: post genuine comparisons in relevant subreddits (r/SaaS, r/Entrepreneur, r/smallbusiness) linking to full review
3. Cross-link from existing 47 deployed landing pages to review pages for internal link juice
4. Content repurpose: convert each review into Twitter thread + LinkedIn post via content_repurposer.py

## Budget Tier Strategies

### FREE
Programmatic SEO for comparison keywords, Reddit posts with genuine value, cross-linking from existing 47 sites, Twitter threads from review content, internal linking between affiliate pages

### LOW
$10-30/mo boosting top-performing review posts on Twitter/Reddit, basic backlink outreach to indie hacker blogs

### MID
$50-150/mo for guest posting on SaaS review sites, sponsored newsletter mentions in niche communities

## Daily Actions

- [ ] 1. Audit existing affiliate pages in LANDING/affiliate-pages/ — check which programs are signed up vs placeholder links
- [ ] 2. Build affiliate_honest_review_generator.py that outputs review HTML with: verdict box, pros/cons list with specifics, pricing table with real numbers, named alternatives, 'who this is NOT for' section (the honesty signal)
- [ ] 3. Pull product data from LEDGER/TOOLS_SERVICES_MASTER.csv and COMPETITIVE_INTEL.csv for features and pricing
- [ ] 4. Generate 10 review pages targeting '[tool] review 2026' and '[tool] vs [tool]' longtail keywords
- [ ] 5. Deploy to surge alongside existing landing pages, cross-link from relevant existing pages
- [ ] 6. Add cron (1st and 15th of month) to refresh pricing data and redeploy
- [ ] 7. Route each new review through content_repurposer.py for Twitter/LinkedIn/Reddit distribution
- [ ] 8. Track via UTM parameters on affiliate links — log clicks in LEDGER/AFFILIATE_CLICK_LOG.csv

## Tooling

```json
{
  "browser": "none",
  "email": "custom cold email scripts for affiliate program signups",
  "content": "content_repurposer.py + engagement_bait_converter.py"
}
```
