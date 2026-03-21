# Growth Plan: Oil prices are going down, and Rune (
@RuneKek
)'s seven-fig

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-25/mo

---

## Tactics

1. Post whale-move content 3x/day timed to US market open (9:30 AM ET), crypto peak (2 PM ET), evening recap (8 PM ET)
2. Quote-tweet original lookonchain posts with added commentary to ride existing viral threads
3. Tag $ticker symbols and use #Hyperliquid #crypto #whales to get discovery traffic from relevant searches
4. Reframe each position as a question hook: 'Would you hold a losing $2M oil long? This whale just doubled down...'
5. Cross-post to Reddit r/WallStreetBets, r/CryptoMarkets with chart screenshot for extra distribution

## Budget Tier Strategies

### FREE
Scrape hypurrscan.io + lookonchain Twitter via Playwright (Brave cookies). Generate 3 content pieces per scrape cycle via engagement_bait_converter.py. Post to printmaxxer account. No paid tools needed.

### LOW
$0-50/mo — Buy Nansen or DeBank pro tier ($9-29/mo) for better whale wallet filtering. Improves signal quality and reduces noise.

### MID
$50-200/mo — Sponsor a DeFi newsletter or pay a crypto influencer $100-200 for a shoutout to a whale-tracking signal Telegram channel.

## Daily Actions

- [ ] 1. Add hypurrscan_whale_content_scraper.py — Playwright scrapes /address/ pages for positions with PnL > $500K or size > $1M, extracts position changes
- [ ] 2. Filter for 'add to losing position' or 'liquidation approaching' signals (highest engagement)
- [ ] 3. Pipe each signal to engagement_bait_converter.py with template: 'Whale [action] on [asset] — [context hook]'
- [ ] 4. Write output to CONTENT/social/posting_queue/whale_signals_YYYYMMDD.txt
- [ ] 5. Cron 3x/day (8 AM, 2 PM, 8 PM) — aligns with lookonchain posting rhythm
- [ ] 6. Wire into existing chain_my_bot_scanned_400000_wallets_to_find_t as a data source param, not a new chain

## Tooling

```json
{
  "browser": "Playwright (Brave cookies for hypurrscan)",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
