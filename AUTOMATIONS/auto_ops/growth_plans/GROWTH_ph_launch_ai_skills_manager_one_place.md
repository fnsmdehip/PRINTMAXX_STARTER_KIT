# Growth Plan: [PH LAUNCH] AI Skills Manager: One place for all your AI ski

**Created:** 2026-03-21 12:40
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo indirect — feeds MCP Marketplace positioning which is the $7.55-scored top venture

---

## Tactics

1. Monitor PH makers on Twitter — they are the exact ICP for MCP Marketplace
2. Auto-comment on PH launches with value-add positioning our tool differently
3. Extract taglines from top-voted AI tools and A/B test variants on our landing pages
4. Identify skills categories with 0 dedicated tools — build fast clones as streak apps

## Budget Tier Strategies

### FREE
Daily PH scrape → competitive LEDGER → weekly positioning review. Route hook structures to content pipeline. Zero cost.

### LOW
$0-50/mo — sponsor a PH launch or use PH Ads to position MCP Marketplace against newly launched competitors while their traffic is hot

### MID
$50-200/mo — pay micro-influencer makers to review MCP Marketplace immediately after launching competing products (timing arbitrage)

## Daily Actions

- [ ] Create AUTOMATIONS/ph_ai_skills_monitor.py — scrape PH /ai daily, extract top 20 by upvotes
- [ ] Wire output to LEDGER/COMPETITIVE_INTEL.csv append + COMPETITIVE_INTEL_MASTER.csv
- [ ] Pipe hook structures to engagement_bait_converter.py for content
- [ ] Add cron: 0 7 * * * python3 AUTOMATIONS/ph_ai_skills_monitor.py
- [ ] Add gap analysis subagent: compare features to MONEY_METHODS/MCP_MARKETPLACE/ — flag unaddressed categories
- [ ] Update OPS/PRINTMAXX_SYSTEM_MAP.md with new scraper entry

## Tooling

```json
{
  "browser": "playwright MCP",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
