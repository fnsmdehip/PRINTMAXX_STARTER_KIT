# Growth Plan: Oil prices are surging.

loracle.hl (
@loraclexyz
) is short

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-15/mo

---

## Tactics

1. Post whale position updates as reaction content — 'loracle down $1.24M on oil short' format drives engagement in crypto Twitter
2. Add hypurrscan wallet addresses to watchlist for recurring content on same whales
3. Tie oil price macro moves (CPI, Fed, OPEC) to on-chain perp positioning for compound hooks
4. Quote-tweet lookonchain.com and hypurrscan directly — borrows existing audience trust

## Budget Tier Strategies

### FREE
Scrape hypurrscan.io whale position pages via Playwright, parse PnL changes, pipe into engagement_bait_converter.py — 3 posts per major position move. Zero cost.

### LOW
$0-50/mo — boost top-performing whale content posts with $5-10 Twitter ads targeting crypto traders

### MID
$50-200/mo — integrate Hyperliquid public API for real-time alerts, autopost within minutes of large position changes

## Daily Actions

- [ ] Check if existing oil/crypto whale scraper already exists in AUTOMATIONS/ before creating new script (dedup gate)
- [ ] If none exists: write hyperliquid_whale_content_generator.py — fetch hypurrscan.io top perp positions via Playwright, parse wallet PnL changes >$500K
- [ ] For each large position event, call engagement_bait_converter.py with the whale data as input
- [ ] Append generated posts to CONTENT/social/posting_queue/
- [ ] Schedule cron 8 AM daily — morning crypto audience peak
- [ ] Add KPI entry: daily check for new whale-content posts in queue

## Tooling

```json
{
  "browser": "Playwright MCP (scrape hypurrscan.io)",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
