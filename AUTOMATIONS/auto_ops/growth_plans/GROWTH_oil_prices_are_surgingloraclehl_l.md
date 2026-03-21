# Growth Plan: Oil prices are surging.

loracle.hl (
@loraclexyz
) is short

**Created:** 2026-03-20 18:35
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0-25/mo

---

## Tactics

1. Crypto Twitter QTs on whale moves with chart screenshots
2. Tag original signal accounts for engagement farming

## Budget Tier Strategies

### FREE
QT lookonchain-style whale alerts with PRINTMAXX branding, post to crypto subreddits

### LOW
$0-20/mo for proxy rotation if hypurrscan rate-limits

### MID
N/A - not worth paid scaling until crypto niche validated

## Daily Actions

- [ ] Build hyperliquid_whale_scraper.py using requests against hypurrscan.io public API
- [ ] Track wallets with >$1M positions on commodity perps (CL, etc.)
- [ ] Log to LEDGER/WHALE_SIGNALS.csv with columns: timestamp, wallet, asset, direction, size_usd, pnl_usd
- [ ] Route notable P&L swings (>$500K) to CONTENT/social/posting_queue/ as signal threads
- [ ] Cron at 7:30 AM daily

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for signal threads"
}
```
