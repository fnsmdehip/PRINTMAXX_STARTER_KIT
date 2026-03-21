# Growth Plan:  sold my first faceless account last month for $47,000i buil

**Created:** 2026-03-20 18:10
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo ongoing per account OR $5000-20000 lump sum per account sale (realistic discount: original claim $47K → expect $8-15K per sale after 3-4 month build)

---

## Tactics

1. Multi-account cross-promotion ring (our existing faceless accounts boost new ones)
2. Engagement warming: 2-week ramp from 1 post/day to 3 posts/day with comment seeding
3. Niche-specific hashtag rotation from HASHTAG_LIBRARY.csv (already built)
4. Repost viral content with attribution to build initial follower base fast
5. DM engagement pods within niche communities (free, manual-feel automation)
6. Time posts to platform peak hours per niche (use PLATFORM_ALGO_CHANGES.csv data)

## Budget Tier Strategies

### FREE
Cross-promote from existing 48 PRINTMAXX accounts, hashtag optimization, engagement warming protocol, content repurposing from existing content_factory pipeline, viral repost strategy

### LOW
$10-30/mo on 2-3 targeted boosts per account to jumpstart follower growth past the 1K algorithmic threshold. Use cheapest CPM niches (motivation, nature, facts).

### MID
$50-150/mo on micro-influencer shoutouts in target niche. Buy 3-5 shoutouts at $10-30 each to accelerate past 10K followers where monetization and sale value inflect.

## Daily Actions

- [ ] 1. Run marketplace_scanner to build comps database from Fameswap/SocialTradia (which niches sell, at what multiples)
- [ ] 2. Select top 3 niches by (sale_multiple * growth_speed * content_automation_ease) — likely: motivation quotes, nature/ASMR, financial tips
- [ ] 3. Create 3 new faceless accounts using existing ACCOUNT_PORTFOLIO_MASTER.csv tracking
- [ ] 4. Generate 90-day content batches per account via claude -p using existing content_multiplier.py
- [ ] 5. Execute warmup protocol (WARMUP_DEVICE_MATRIX.csv) — 2 weeks warm, then ramp
- [ ] 6. Cross-promote from existing PRINTMAXX accounts to seed initial followers
- [ ] 7. Weekly valuation check: MRR * 32 = estimated sale price. Track in LEDGER/FACELESS_ACCOUNT_VALUATIONS.csv
- [ ] 8. At $300+/mo MRR (sale value $10K+), draft marketplace listing and list on Fameswap
- [ ] 9. Feed sold-account revenue back into Capital Genesis for reinvestment scoring

## Tooling

```json
{
  "browser": "playwright MCP for marketplace scraping",
  "email": "none",
  "content": "content_factory + content_multiplier.py + engagement_bait_converter.py (all existing)"
}
```
