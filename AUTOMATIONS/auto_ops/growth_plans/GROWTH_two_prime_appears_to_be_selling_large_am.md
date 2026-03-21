# Growth Plan: Two Prime appears to be selling large amounts of $BTC — 3,94

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect via crypto audience growth

---

## Tactics

1. Post whale movement alerts with $BTC/$ETH cashtags for algo amplification
2. Reply to @lookonchain @WatcherGuru @whale_alert posts to piggyback their reach
3. Timestamp posts within minutes of Arkham alerts — speed = credibility in crypto
4. Use 'JUST IN:' hook format — proven engagement trigger in crypto Twitter

## Budget Tier Strategies

### FREE
Auto-post whale alerts via posting queue. Reply to existing viral crypto threads. Use cashtags and whale alert hashtags for organic reach.

### LOW
$0-50/mo: Boost highest-engagement whale posts. Follow/engage top crypto accounts to seed algorithmic distribution.

### MID
$50-200/mo: Paid promotion on breakout whale posts. Sponsor crypto newsletter drops with whale intel snippets.

## Daily Actions

- [ ] Call engagement_bait_converter.py with this entry — generate 3 posts with JUST IN hook, specific dollar amounts, and cashtags
- [ ] Append generated posts to CONTENT/social/posting_queue/
- [ ] Wire whale_movement_content_generator.py to poll Arkham public data every 4h for movements >$50M BTC
- [ ] Add cron entry: 0 */4 * * * python3 AUTOMATIONS/whale_movement_content_generator.py

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
