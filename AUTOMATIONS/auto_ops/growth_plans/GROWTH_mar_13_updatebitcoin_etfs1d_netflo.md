# Growth Plan: Mar 13 Update:

#Bitcoin ETFs:
1D NetFlow: +570 $BTC(+$41.87

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-10/mo

---

## Tactics

1. Reply to @lookonchain and other on-chain data accounts with our formatted take within 15 min of their post
2. Cross-post ETF flow summaries to r/cryptocurrency and r/ethfinance for karma farming
3. Use ETF flow direction as hook for longer threads on institutional crypto adoption

## Budget Tier Strategies

### FREE
Quote-tweet major on-chain analysts with formatted flow data and contrarian take. Reply-chain engagement on crypto Twitter. Post daily flow summaries to Reddit finance subs.

### LOW
$0-20/mo for proxy rotation if scraping rate-limited sources

### MID
N/A — content play, not paid acquisition

## Daily Actions

- [ ] Create crypto_etf_flow_poster.py that formats ETF flow data into Twitter-ready posts with clean formatting
- [ ] Wire into existing content posting queue at CONTENT/social/posting_queue/
- [ ] Add cron at 6:45 AM weekdays to generate daily flow post
- [ ] Add KPI task to track engagement on crypto content posts

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
