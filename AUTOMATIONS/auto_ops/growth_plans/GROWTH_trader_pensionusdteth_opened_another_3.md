# Growth Plan: Trader pension-usdt.eth opened another 3x long on 1,000 $BTC

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-15/mo

---

## Tactics

1. Post whale alerts with exchange affiliate links (Bybit/Binance) — CPC converts well on crypto content
2. Reply to @lookonchain original tweets with 'analysis' angle to steal their engagement
3. Tag wallet address in post for searchability — on-chain curious audience finds it
4. Cross-post identical content to TikTok finance niche — whale trade content gets organic push

## Budget Tier Strategies

### FREE
Scrape lookonchain Twitter + Whale Alert RSS → engagement_bait_converter.py → post to queue with exchange affiliate appended. Zero cost, fully automated.

### LOW
$0-50/mo: Nansen free tier or DeBankAPI for real-time wallet monitoring. Widens source beyond lookonchain.

### MID
$50-200/mo: Paid Nansen/Arkham subscription for faster alerts + broader wallet universe. First-mover advantage on big moves.

## Daily Actions

- [ ] 1. Scrape lookonchain.io RSS or @lookonchain Twitter timeline via requests (no browser needed)
- [ ] 2. Parse: wallet address, asset, position size, PnL, win streak from tweet text
- [ ] 3. Filter: only pass entries with >$500K PnL or win_streak >= 5 (noise reduction)
- [ ] 4. Call engagement_bait_converter.py with extracted stats as seed
- [ ] 5. Append exchange affiliate link (Bybit referral in .env) to generated post
- [ ] 6. Write to CONTENT/social/posting_queue/whale_alerts_{date}.txt
- [ ] 7. Cron every 4h — dedup by wallet+timestamp to avoid reposting

## Tooling

```json
{
  "browser": "none \u2014 lookonchain RSS + Twitter API or requests scrape",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
