# Growth Plan: A #BitcoinOG with 5K $BTC($356M) sold another 1,000 $BTC($71

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Post whale P&L threads during US market hours (9-11 AM ET) for max crypto Twitter engagement
2. Quote-tweet Lookonchain and similar whale trackers with our own analysis angle
3. Use the 'Nx return' hook format — proven engagement bait structure for fintwit

## Budget Tier Strategies

### FREE
Auto-generate whale P&L posts from free blockchain APIs (blockchain.com, etherscan free tier). Cross-post to printmaxxer Twitter. Reply to whale tracker accounts with our formatted version for engagement farming.

### LOW
$0-50/mo: Premium blockchain API tier for faster/more data. Boost top-performing whale threads.

### MID
$50-200/mo: Multiple niche finance accounts posting whale content. Paid promotion on best-performing threads.

## Daily Actions

- [ ] Extract viral template format: '[Entity] bought [N] [asset] at [$X] [time] ago → sold at [$Y] → [N]x return, $[Z] profit'
- [ ] Add template to CONTENT/social/COPY_STYLE_CORPUS.csv as proven engagement format
- [ ] Create whale_pnl_content_generator.py that hits free blockchain APIs for large transactions
- [ ] Wire output to engagement_bait_converter.py for multi-platform formatting
- [ ] Queue generated posts to CONTENT/social/posting_queue/
- [ ] Add 7 AM daily cron for fresh whale movement content

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
