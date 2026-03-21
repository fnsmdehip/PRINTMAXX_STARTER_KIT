# Growth Plan: Whale 0x15a4 opened 20x longs on 600 $BTC($42.5M) and 20,000

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-25/mo

---

## Tactics

1. Post whale alerts within 5-10min of detection for first-mover engagement on crypto Twitter
2. Quote-tweet lookonchain/hypurrscan with added analysis layer to ride their existing audience
3. Reply to @HyperliquidX official posts with whale data — algo surfaces replies from data accounts
4. Tag $BTC $ETH cashtags so content surfaces in ticker feeds
5. Thread format: alert tweet → position size tweet → historical context tweet → 'follow for more' CTA

## Budget Tier Strategies

### FREE
Post 3-4 whale alerts/day via posting_queue using existing Twitter warmup poster. Quote-tweet lookonchain, Arkham, and Hypurrscan to leech audience. Cashtag and crypto hashtag injection on every post.

### LOW
$10-20/mo Hyperliquid premium data if free API rate-limited. Boost top-performing whale alert posts with $5-10 Twitter ads targeting crypto traders.

### MID
$50-200/mo: Buy aged crypto Twitter account with existing followers to post alerts. Run ads targeting @HyperliquidX and @lookonchain followers.

## Daily Actions

- [ ] Wire into existing chain_my_bot_scanned_400000_wallets_to_find_t — enhance with Hyperliquid-specific endpoint rather than creating new chain
- [ ] Script polls POST api.hyperliquid.xyz/info with {type: 'openInterest'} and {type: 'allMids'} every 30min
- [ ] Filter positions: notional >$5M, leverage >=10x, detect net new opens vs existing state file (AUTOMATIONS/agent/state/hyperliquid_positions.json)
- [ ] On new whale detect: call engagement_bait_converter.py with position data to generate 3-tweet thread
- [ ] Append to CONTENT/social/posting_queue/hyperliquid_alerts_queue.txt
- [ ] twitter_warmup_poster.py picks up from queue on next run
- [ ] Add cron entry: */30 * * * * python3 AUTOMATIONS/hyperliquid_whale_monitor.py >> AUTOMATIONS/logs/hyperliquid.log 2>&1

## Tooling

```json
{
  "browser": "none \u2014 Hyperliquid API is public REST (api.hyperliquid.xyz/info), no auth required",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
