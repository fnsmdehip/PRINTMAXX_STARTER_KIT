# Growth Plan: We launched a 7 figure Amazon brand on tiktok shop and did $

**Created:** 2026-03-20 18:35
**Venture:** BROKERING
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Cross-post brokering wins as content on printmaxxer Twitter (builds deal flow inbound)
2. Scrape TikTok Shop affiliate leaderboards for warm creator leads already selling
3. DM brands whose TikTok Shop listings have low views but strong Amazon reviews (untapped demand)
4. Build a simple landing page for creator/brand signups to generate inbound leads
5. Leverage existing chain_i_made_100k_for_an_brand_in_under_2_mon for proven TikTok Shop playbook

## Budget Tier Strategies

### FREE
Scrape TikTok Shop + creator profiles, cold DM brands and creators directly, cross-post results as Twitter content, use existing cold outreach pipeline

### LOW
$20-50/mo for GoLogin multi-account to DM at scale without shadowban, residential proxy rotation for scraping

### MID
$100-200/mo for TikTok Shop analytics tool subscription (Kalodata or FastMoss) to identify high-GMV brands faster + email warmup for brand outreach

## Daily Actions

- [ ] 1. Build TikTok Shop brand scraper using Playwright MCP — target brands with $5K+/week GMV but no visible creator program
- [ ] 2. Build TikTok creator scraper — target creators posting product reviews with >3% engagement, filter by niche tags
- [ ] 3. Create matching algorithm: niche overlap score + audience size ratio + engagement rate + creator GMV history
- [ ] 4. Generate cold outreach templates: brand-side pitch (commission-only creators, zero risk) and creator-side pitch (vetted brands, guaranteed product)
- [ ] 5. Wire into existing cold outreach chain for automated sending
- [ ] 6. Track in LEDGER/BROKERING_PIPELINE.csv: brand, creator, match score, outreach status, deal status, GMV, commission earned
- [ ] 7. Cron Mon+Thu to refresh brand/creator lists and generate new matches
- [ ] 8. Content extraction: every successful match = Twitter thread on printmaxxer

## Tooling

```json
{
  "browser": "playwright for TikTok Shop scraping",
  "email": "custom cold email scripts via existing outreach pipeline",
  "content": "content_factory for case study posts from successful matches"
}
```
