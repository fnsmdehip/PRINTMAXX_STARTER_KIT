# Growth Plan: Whale 0x743d just spent 3.79M $USDT to buy 1,827 $ETH again.

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect via engagement → followers → sponsorship pipeline

---

## Tactics

1. Quote-tweet lookonchain and other whale trackers with added analysis to piggyback their audience
2. Use consequence-first hooks: 'A whale just mass-bought $25M of ETH. Here's why that matters.' — engagement bait converter format
3. Cross-post whale alerts to Reddit r/cryptocurrency and r/ethtrader for multi-platform reach

## Budget Tier Strategies

### FREE
Etherscan free API (5 calls/sec), auto-generate threads via claude -p, post to existing content queue, QT whale tracker accounts for piggyback reach

### LOW
$0-50/mo: Arkham Intel free tier for richer wallet labels, boost top whale alert tweets

### MID
$50-200/mo: Arkham Pro for real-time alerts + Dune dashboards embedded in threads

## Daily Actions

- [ ] Create whale_alert_content_generator.py: poll Etherscan API for transfers >$1M from known whale watchlist (start with 0x743d + 10 known accumulators from lookonchain)
- [ ] When large transfer detected, generate 3 tweet variants via claude -p using consequence-first hook pattern from procedural memory
- [ ] Write output to CONTENT/social/posting_queue/whale_alerts_{date}.txt
- [ ] Add cron every 4 hours to check for new large movements
- [ ] Route through existing engagement_bait_converter.py for hook optimization

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
