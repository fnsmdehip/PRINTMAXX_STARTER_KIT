# Growth Plan: An Ethereum ICO wallet (0xF37b) transferred 100.275 $ETH($20

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-25/mo

---

## Tactics

1. QT lookonchain and whale_alert tweets with contrarian take within 15 min of post
2. Reply-bait under crypto whale tracker accounts with our own data additions
3. Cross-post whale movement threads to r/cryptocurrency and r/ethtrader for organic reach

## Budget Tier Strategies

### FREE
QT viral whale tweets with added context (ROI calc, dormancy stats), reply under lookonchain/whale_alert posts, cross-post to Reddit crypto subs, use free Etherscan API (5 calls/sec)

### LOW
$0-20/mo for Etherscan Pro API key (higher rate limits, richer data) if free tier bottlenecks

### MID
$50-100/mo for dedicated on-chain analytics API (Dune, Nansen free tier) for deeper whale profiling

## Daily Actions

- [ ] Create whale_wallet_content_generator.py using free Etherscan API to pull large transfers and dormant wallet reactivations
- [ ] Format findings as engagement-bait threads (ROI calc, dormancy period, original investment vs current value)
- [ ] Route generated threads to CONTENT/social/posting_queue/ for printmaxxer Twitter
- [ ] Add cron at 7 AM and 7 PM to catch overnight and daytime whale movements
- [ ] Wire output through engagement_bait_converter.py for multi-platform repurposing

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
