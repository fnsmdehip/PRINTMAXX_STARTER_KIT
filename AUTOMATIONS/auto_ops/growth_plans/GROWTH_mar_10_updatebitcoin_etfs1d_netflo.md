# Growth Plan: Mar 10 Update:

#Bitcoin ETFs:
1D NetFlow: +2,070 $BTC(+$146

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-20/mo

---

## Tactics

1. Post ETF flow data at 6:30 AM EST (pre-market open) for maximum crypto audience engagement
2. Frame data as 'institutional signal' — use numbers verbatim, no editorializing
3. Cross-post to finance subreddits (r/cryptocurrency, r/ethfinance) with context paragraph
4. Reply to lookonchain original tweets with 'TL;DR' summary to capture their engaged audience

## Budget Tier Strategies

### FREE
Schedule posts pre-market open, reply to source tweets, cross-post to Reddit with context, use existing twitter_warmup_poster.py

### LOW
$0-50/mo — boost high-engagement ETF posts on X for finance audience targeting

### MID
$50-200/mo — Beehiiv newsletter digest of weekly ETF flows, monetize with affiliate links to crypto exchanges

## Daily Actions

- [ ] Scrape ETF flow data: coinglass.com/etf free endpoint OR parse lookonchain tweet via twitter_alpha_scraper.py (already running at 6 AM)
- [ ] Generate 3 post variants per asset (BTC/ETH/SOL) using claude -p with tight number-forward template
- [ ] Append to CONTENT/social/posting_queue/etf_flows_$(date +%Y%m%d).txt
- [ ] twitter_warmup_poster.py picks up queue at next scheduled run

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_repurposer.py + CONTENT/social/posting_queue/"
}
```
