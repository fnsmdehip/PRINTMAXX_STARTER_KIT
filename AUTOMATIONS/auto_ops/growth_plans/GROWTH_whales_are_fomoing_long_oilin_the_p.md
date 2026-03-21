# Growth Plan: Whales are FOMO-ing long #oil!

In the past 30 minutes:

0xf

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Post whale alerts in real-time — lookonchain style, short, specific numbers, no fluff
2. Reply to @lookonchain, @hyperliquid_x, @coinglass posts with our own alert when timing overlaps
3. Thread format: lead tweet = whale alert, reply = 'this is the 3rd time this wallet has done this pattern' (adds analysis hook)
4. Pin bio link to Hyperliquid referral (25% fee share program — free to join)
5. Cross-post alerts to r/algotrading and r/wallstreetbets when position is large enough to be newsworthy

## Budget Tier Strategies

### FREE
Post every qualifying whale signal. Engage replies. Reply-bait format: 'Whales loading [asset] again — here is the pattern from last 3 times they did this [thread]'. Build Twitter/X account in crypto-signals niche. Zero ad spend.

### LOW
$0-50/mo — Boost top-performing alert posts. Use 1-2 additional Twitter accounts to QT and amplify the main account. Explore Telegram channel as secondary distribution (crypto audience expects Telegram alerts).

### MID
$50-200/mo — Small influencer seeding (DM crypto micro-influencers with verified signals, offer rev share on Hyperliquid referrals). Run paid Twitter promotion on threads that already hit >500 organic engagements.

## Daily Actions

- [ ] 1. Check if chain_my_bot_scanned_400000_wallets_to_find_t already covers this — enhance it with oil/CL futures filter rather than creating new chain
- [ ] 2. Create AUTOMATIONS/whale_position_monitor.py using Playwright MCP to scrape hypurrscan.io /perps and Hyperliquid public positions API
- [ ] 3. Filter: notional > $2M OR leverage > 10x, deduplicate by wallet+asset+side within 6h window
- [ ] 4. Pipe qualifying signals through claude -p with lookonchain-style prompt, output to CONTENT/social/posting_queue/
- [ ] 5. Wire cron: */30 6-22 * * * (every 30 min, US/EU trading hours)
- [ ] 6. Add Hyperliquid referral link to Twitter bio — free 25% fee share program
- [ ] 7. Test immediately: python3 AUTOMATIONS/whale_position_monitor.py --dry-run — verify it finds at least one signal from today's data
- [ ] 8. Add KPI entry to OPS/KPI_DASHBOARD.md: whale signals/day, posts queued/day, affiliate clicks/week

## Tooling

```json
{
  "browser": "playwright MCP for hypurrscan.io scraping (no API auth needed)",
  "email": "none",
  "content": "claude -p (Claude Max) for post generation, engagement_bait_converter.py for bulk variants"
}
```
