# Growth Plan: Super Micro $SMCI stock is down by almost 30% so far today 


**Created:** 2026-03-20 23:36
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo

---

## Tactics

1. Post stock mover content during market hours (9:30 AM - 4 PM ET) for peak engagement
2. Use ticker cashtags ($SMCI, $QQQ) — these get 3-5x more reach on X than regular posts
3. Reply to verified financial accounts' posts about the same stock within 10 min of their post
4. Stitch dramatic chart screenshots (Playwright screenshot of Yahoo Finance chart) into posts for visual hook
5. Cross-post to r/wallstreetbets, r/stocks with 'today's biggest loser' framing when moves >20%

## Budget Tier Strategies

### FREE
Monitor Yahoo Finance free API for top 10 daily movers. Auto-generate 3-5 posts per market session. Reply-bait to verified accounts posting about same tickers. Use cashtag targeting.

### LOW
$0-50/mo: Polygon.io free tier (5 API calls/min) for real-time quotes. Schedule posts via Buffer free tier. Target 10+ daily posts across financial content accounts.

### MID
$50-200/mo: Benzinga Pro RSS feed for pre-market movers. Alpaca API for after-hours data. Paid scheduling tool for multi-account posting.

## Daily Actions

- [ ] Pull top 10 daily movers via yfinance (pip install yfinance — already available)
- [ ] Filter: >10% move AND market cap >$1B (institutional names = more engagement)
- [ ] Generate 3 post variants per ticker: hook-only, hook+chart_description, hook+CTA_thread
- [ ] Stage to CONTENT/social/posting_queue/ with platform tags (X, Reddit)
- [ ] Cron at 10 AM, 1 PM, 4 PM ET on weekdays — catches pre-market gap, midday reversal, close

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter.py",
  "data": "yfinance (free) or Yahoo Finance JSON API"
}
```
