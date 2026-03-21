# Growth Plan: Whale 0x049b opened 20x shorts on 428.73 $BTC($29.62M) and 1

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Whale alert threads tagged with $BTC $ETH cashtags for algorithmic reach
2. QT Lookonchain and similar accounts with our own analysis angle
3. Reply-bait under whale alert posts from major accounts

## Budget Tier Strategies

### FREE
Post whale alerts with cashtags for organic crypto Twitter reach, QT major whale watchers, build engagement via reply strategy under Lookonchain/Arkham/Nansen posts

### LOW
$0-50/mo for Hyperliquid data API if free tier is rate-limited

### MID
$50-200/mo not recommended at this stage — crypto content niche is supplementary, not core

## Daily Actions

- [ ] Build hyperliquid_whale_scraper.py using Hyperliquid public REST API (no auth needed for large position data)
- [ ] Filter for positions >$1M notional, >10x leverage — the newsworthy trades
- [ ] Format as tweet-ready whale alert content with liquidation prices and PnL
- [ ] Route to CONTENT/social/posting_queue/ for scheduling
- [ ] Cron every 4 hours to catch major moves

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory \u2014 route whale alerts through engagement_bait_converter.py for social formatting"
}
```
