# Growth Plan: Whale bc1qfs has been buying $BTC every day since Mar 10, an

**Created:** 2026-03-20 13:50
**Venture:** SCRAPING
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Whale alert posts consistently get high retweet ratios on crypto Twitter — large dollar amounts trigger algorithmic boost
2. Tag/QT original sources like @lookonchain and @whale_alert for engagement farming and visibility
3. Use exact dollar figures and wallet labels in tweets — specificity drives engagement over vague market commentary
4. Cross-post to r/cryptocurrency and r/bitcoin for Reddit distribution

## Budget Tier Strategies

### FREE
Post whale alerts from free on-chain APIs, engage with crypto Twitter accounts, use engagement-bait formatting with large $ figures, cross-post to Reddit crypto subs

### LOW
$0-50/mo: boost top-performing whale alert tweets via Twitter ads, use scheduling tool for optimal timing

### MID
$50-200/mo: run dedicated crypto intel account with daily whale reports, paid newsletter via Beehiiv

## Daily Actions

- [ ] Build whale wallet tracker using free Blockchain.com and Etherscan public APIs — no API key needed for basic queries
- [ ] Seed with 20-30 known whale addresses from Arkham Intelligence free tier and public whale lists
- [ ] Monitor for transactions >$1M, auto-format into engagement-style tweet templates
- [ ] Route generated posts to CONTENT/social/posting_queue/ via existing content pipeline
- [ ] Schedule cron every 4 hours to check for new large transactions
- [ ] Feed whale data to engagement_bait_converter.py for multi-platform content variants

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
