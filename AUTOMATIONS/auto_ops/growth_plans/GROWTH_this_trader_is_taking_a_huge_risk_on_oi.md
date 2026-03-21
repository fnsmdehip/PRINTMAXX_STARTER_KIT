# Growth Plan: This trader is taking a huge risk on #oil!

He just opened a

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct — audience play. Monetize at 1K+ followers via trading affiliate links ($50-200/mo at scale)

---

## Tactics

1. Post whale alerts with liquidation countdown (builds urgency, gets reshares)
2. Add 'follow for live whale alerts' CTA on every post
3. Reply to lookonchain, hypurrscan, and whale_alert accounts with commentary to leech their audience
4. Cross-post to Reddit r/wallstreetbets, r/Superstonk, r/CryptoMoonShots with context
5. Wire into existing content_repurposer.py to multiply across platforms

## Budget Tier Strategies

### FREE
Post 3x/day whale alerts via twitter_warmup_poster.py. Reply-bait lookonchain and similar accounts. Hashtags: #whales #liquidation #oil #crypto #perps

### LOW
$10-20/mo boost top-performing whale alert posts targeting finance/crypto audiences

### MID
$50-100/mo paid promotion of 'whale alert' account + affiliate link to trading platform (Bybit/Binance affiliate = 30-50% commission)

## Daily Actions

- [ ] Wire playwright MCP to scrape hypurrscan.io /perps endpoint every 4h for positions >$500K notional + >10x leverage
- [ ] Filter: only include positions within 3% of liquidation price (high drama = high engagement)
- [ ] Format as template: 'This [trader/whale] just opened [Nx] [long/short] on [asset] ($[amount]) — liquidation at $[price]. [% away from liq].' 
- [ ] Pipe output to engagement_bait_converter.py with niche=finance
- [ ] Posts land in CONTENT/social/posting_queue/ for twitter_warmup_poster.py

## Tooling

```json
{
  "browser": "playwright MCP (scrape hypurrscan.io)",
  "email": "none",
  "content": "engagement_bait_converter.py \u2192 CONTENT/social/posting_queue/"
}
```
