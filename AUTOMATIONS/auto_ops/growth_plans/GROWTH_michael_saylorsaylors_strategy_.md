# Growth Plan: Michael Saylor(
@saylor
)'s 
@Strategy
 bought another 17,99

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Post within 1h of Strategy press release for first-mover engagement advantage on crypto Twitter
2. Lead with unrealized loss angle (-$5.3B, -9.4%) — contrarian framing outperforms bullish framing for engagement
3. Cross-post to r/Bitcoin, r/CryptoCurrency, r/investing with different angle per subreddit
4. Stack with cost-basis data posts: average $75,862 vs current price = gap narrative content

## Budget Tier Strategies

### FREE
Auto-generate 3 post variants per purchase event via engagement_bait_converter.py (raw data, unrealized-loss take, accumulation-pattern analysis); route to posting_queue; target crypto subreddits organically

### LOW
$0-50/mo: Boost best-performing crypto content on X Ads targeting Bitcoin/treasury audiences; no paid tool needed

### MID
$50-200/mo: Build free Corporate BTC Treasury Tracker page (surge.sh) as SEO magnet; email capture for crypto content list

## Daily Actions

- [ ] Route entry directly to engagement_bait_converter.py — extract hook: unrealized loss % + cost-basis-vs-market gap = contrarian hook structure
- [ ] Generate 3 variants: (1) raw data post with numbers, (2) contrarian loss-angle take, (3) accumulation pattern / average-down narrative
- [ ] Append all 3 to CONTENT/social/posting_queue/ for next content cycle
- [ ] Wire btc_treasury_intel_scraper.py cron (8 AM daily) to poll strategy.com/press RSS for new purchase press releases — triggers generator on match

## Tooling

```json
{
  "browser": "requests \u2014 strategy.com press releases are static HTML, no JS rendering needed",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
