# Growth Plan: Whale 0x985f deposited 9.5M $USDC into HyperLiquid in the pa

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo

---

## Tactics

1. Reply to @lookonchain and @hypurrscan posts within 30min of whale event — parasitic reach on their audience
2. Cross-post whale data to r/wallstreetbets and r/CryptoCurrency as 'interesting on-chain data'
3. Build 'whale alert' brand angle — consistent format creates follows from traders who want the signal
4. Quote-tweet the original lookonchain source post with our analysis angle (not copy-paste)

## Budget Tier Strategies

### FREE
Organic: reply farming on whale tracker accounts, consistent posting format, hashtag stacking (#hyperliquid #onchain #whale #crypto), cross-post to Reddit as data observation not financial advice

### LOW
$0-50/mo: Boost 1-2 best-performing whale alert posts per week ($5-10 each), seed into crypto Discord servers with whale-watching channels

### MID
$50-200/mo: Paid promotion on crypto finance subreddits, sponsor slot in whale-watching Telegram channels, micro-influencer seeding to 3-5 accounts in trading niche

## Daily Actions

- [ ] 1. Check if existing wallet_scanner.py or similar already hits hypurrscan.io — DEDUP before creating new script
- [ ] 2. If no existing scraper: create hyperliquid_whale_tracker.py — requests GET to hypurrscan.io/api or Playwright scrape, filter positions >$1M, diff against last run state file
- [ ] 3. Pipe new positions to engagement_bait_converter.py with context: position size, leverage, asset, direction (long/short)
- [ ] 4. Output 3 post variants per whale event to CONTENT/social/posting_queue/
- [ ] 5. Add cron entry: 0 */4 * * * (every 4h — whales move during any hour)
- [ ] 6. Wire into chain_my_bot_scanned_400000_wallets_to_find_t as a parallel data source

## Tooling

```json
{
  "browser": "playwright (hypurrscan.io scrape) or requests if public API exists",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
