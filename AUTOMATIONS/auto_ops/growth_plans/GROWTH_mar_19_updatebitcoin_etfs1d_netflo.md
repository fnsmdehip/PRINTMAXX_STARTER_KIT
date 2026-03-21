# Growth Plan: Mar 19 Update:

#Bitcoin ETFs:
1D NetFlow: -1,982 $BTC(-$137

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. crypto fintwit engagement — reply to lookonchain/similar accounts with our take on the data
2. hashtag riding on $BTC $ETH $SOL trending tickers

## Budget Tier Strategies

### FREE
Auto-generate market update tweets from scraped ETF data, reply to top crypto accounts with data-backed takes, use trending ticker hashtags

### LOW
N/A — content-only play, no paid spend warranted at this stage

### MID
N/A

## Daily Actions

- [ ] Build lightweight scraper that hits lookonchain-style public endpoints for daily ETF flow data
- [ ] Format data into 1-2 tweet templates (daily flow + weekly trend comparison)
- [ ] Push to CONTENT/social/posting_queue/ for distribution
- [ ] Wire into existing twitter_warmup_poster.py schedule

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + posting_queue"
}
```
