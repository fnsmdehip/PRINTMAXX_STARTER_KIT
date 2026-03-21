# Growth Plan: The #Matrixport-linked whale closed a 40,000 $ETH($94.16M) l

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Crypto Twitter engagement farming — whale posts get high retweets
2. Quote-tweet real whale trackers (lookonchain, whale_alert) with hot takes
3. Post during high-volatility windows when crypto audience is most active

## Budget Tier Strategies

### FREE
Scrape free Etherscan API for large transactions, auto-generate posts with engagement hooks, QT existing whale trackers for visibility

### LOW
$0-50/mo — Dune Analytics free tier for richer on-chain queries, schedule posts via Buffer free tier during peak hours

### MID
$50-200/mo — Nansen or Arkham lite for better whale labeling, targeted crypto community ads

## Daily Actions

- [ ] Register free Etherscan API key
- [ ] Build scraper to monitor wallets with >10K ETH for large position changes
- [ ] Feed whale moves into engagement_bait_converter.py to generate crypto-audience posts
- [ ] Route to CONTENT/social/posting_queue/ for scheduling
- [ ] Track engagement metrics to find which whale narratives perform best

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
