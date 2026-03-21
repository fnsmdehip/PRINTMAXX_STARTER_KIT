# Growth Plan: Whales are buying $ETH!

Someone created a new wallet (0xfDe

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo

---

## Tactics

1. Hook structure: lead with exact wallet address + USD amount (specificity = shareability)
2. Reply to @lookonchain posts with our own analysis to ride their distribution
3. Tag $ETH, $BTC cashtags for crypto algorithm reach
4. Post within 30 min of on-chain event for recency advantage

## Budget Tier Strategies

### FREE
Etherscan free API (5 calls/sec) + engagement_bait_converter.py → posting_queue. Reply to whale alert accounts for inbound follows.

### LOW
$0-50/mo: Buffer or native scheduling for optimal post times. No paid data needed.

### MID
Skip — crypto content has no MID-tier play without a paid signal product, which is out of scope for Phase 0.

## Daily Actions

- [ ] Call Etherscan API (free) to detect large wallet outflows >1000 ETH from known exchange hot wallets
- [ ] Format post: wallet address + ETH amount + USD equivalent + exchange name
- [ ] Pipe to engagement_bait_converter.py for Twitter/X format with cashtags
- [ ] Append to CONTENT/social/posting_queue/ for scheduled distribution
- [ ] Cron every 4h — crypto cycles are 24/7 but 4h cadence avoids spam flags

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py \u2192 CONTENT/social/posting_queue/"
}
```
