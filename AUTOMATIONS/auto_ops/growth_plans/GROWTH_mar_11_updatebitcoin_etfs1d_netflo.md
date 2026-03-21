# Growth Plan: Mar 11 Update:

#Bitcoin ETFs:
1D NetFlow: +3,392 $BTC(+$238

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-20/mo

---

## Tactics

1. Post ETF flow data daily at 7 AM — lookonchain followers are 600K+, this is a known engagement pattern
2. Frame as signal not data: 'Smart money moved X BTC today — here is what that means' beats raw numbers
3. Cross-post to crypto subreddits (r/Bitcoin, r/ethfinance) with analysis framing

## Budget Tier Strategies

### FREE
Pull data from @lookonchain X posts via existing twitter_alpha_scraper.py, reframe with Claude, queue to posting_queue daily

### LOW
$0-50/mo — boost highest-engagement ETF post 1x/week to crypto audience on X

### MID
$50-200/mo — sponsor crypto newsletter slot when account hits 1K followers

## Daily Actions

- [ ] Check if existing ETF flow scraper from March 9/11 integrations already covers BTC — if yes, add ETH and SOL as config params only
- [ ] Run engagement_bait_converter.py on this raw data to generate 3 posts
- [ ] Drop into CONTENT/social/posting_queue/ with crypto tag
- [ ] Cron at 7 AM daily to auto-pull next day's flows from lookonchain X account

## Tooling

```json
{
  "browser": "none \u2014 X JSON API or existing twitter_alpha_scraper.py",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
