# Growth Plan: Mar 17 Update:

#Bitcoin ETFs:
1D NetFlow: +2,955 $BTC(+$219

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo

---

## Tactics

1. Crypto Twitter engagement farming with real data
2. Quote-tweet major flow days with commentary
3. Tag institutional accounts for visibility

## Budget Tier Strategies

### FREE
Post ETF flow updates during US market hours for max engagement, use specific numbers as hooks (completion-rate optimized short-form), reply to crypto influencer posts with our data

### LOW
$0-20/mo boost top-performing crypto data posts on X

### MID
$50-100/mo crypto newsletter sponsorship cross-promotion

## Daily Actions

- [ ] Build crypto_etf_flow_scraper.py using requests to pull ETF flow data from free APIs (coinglass free tier, etf.com RSS)
- [ ] Auto-format flow data into tweet-ready content with specific numbers as hooks
- [ ] Route generated content to CONTENT/social/posting_queue/ via content_factory chain
- [ ] Schedule cron at 6:45 AM weekdays (after US market close data published)
- [ ] Feed significant flow days (>$500M daily) to engagement_bait_converter for thread expansion

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
