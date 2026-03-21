# Growth Plan: I analyzed HeyGen, Deel, and Vercel’s exact growth strategie

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo direct (content drives traffic to paid products and builds authority for cold outreach credibility)

---

## Tactics

1. Growth teardown threads get 3-5x engagement vs generic advice posts — use specific company names and exact numbers in hooks
2. Cross-post teardowns to r/SaaS, r/startups, Indie Hackers, and LinkedIn simultaneously — each platform rewards 'I analyzed X' format
3. Tag the companies analyzed on Twitter for amplification — founders often RT growth analyses of their own companies
4. Bundle 10 teardowns into a free PDF lead magnet for email list building

## Budget Tier Strategies

### FREE
Organic posting of teardown threads across Reddit/Twitter/LinkedIn. Tag founders. Reply to SaaS growth questions with our teardown links. Repurpose into carousel posts.

### LOW
$10-30/mo boosting top-performing teardown threads on Twitter. A/B test hook formats (specific numbers vs contrarian takes).

### MID
$50-100/mo for LinkedIn sponsored posts targeting SaaS founders. Bundle teardowns into Gumroad lead magnet with email upsell.

## Daily Actions

- [ ] Wire into existing chain_i_analyzed_1500_bootstrapped_startups for shared scraping infra
- [ ] Build saas_growth_teardown_content.py DAG: scrape r/SaaS + r/startups + IH for posts mentioning specific company growth strategies with numbers
- [ ] Extract structured tactics: company, channel used, stage applied, result, replicability score
- [ ] Generate 2 teardown threads per week using claude -p with hook templates from engagement_bait_converter
- [ ] Queue to CONTENT/social/posting_queue/ with cross-platform variants
- [ ] Secondary feed: match extracted tactics against our active ventures and flag applicable ones in growth_tactics.json
- [ ] Cron: Mon+Thu 7 AM

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
