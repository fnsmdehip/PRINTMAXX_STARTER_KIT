# Growth Plan: Abraxas Capital is shorting #oil.

In the past 13 hours, the

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Crypto Twitter quote-tweeting whale moves within 15 min of detection
2. Tag relevant accounts (Lookonchain-style) to ride engagement waves
3. Thread format: whale move + historical accuracy of wallet + what it means

## Budget Tier Strategies

### FREE
Auto-generate whale alert tweets from scraper output, post to content queue, QT existing whale trackers with our analysis angle

### LOW
$0-50/mo: Boost top-performing whale alert tweets, cross-post to Telegram crypto channels

### MID
$50-200/mo: Premium whale alert Telegram/Discord channel with paywall

## Daily Actions

- [ ] Build hyperliquid_whale_scraper.py using requests against hypurrscan.io public API
- [ ] Track top 20 known fund wallets for position changes >$1M notional
- [ ] Route detected whale moves to engagement_bait_converter.py for tweet generation
- [ ] Add to CONTENT/social/posting_queue/ for scheduled posting
- [ ] Cron every 4 hours to catch major moves

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
