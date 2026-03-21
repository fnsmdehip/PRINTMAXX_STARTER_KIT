# Growth Plan: Online business acquisition framework (Onfolio, Nasdaq: ONFO

**Created:** 2026-03-20 13:50
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo

---

## Tactics

1. Post acquisition teardown threads on r/Entrepreneur and r/sweatystartup (source community)
2. Cross-post deal analysis to Twitter as educational content (builds authority in biz acquisition niche)
3. Repurpose deal scanner data into weekly 'Undervalued Online Businesses' newsletter content
4. Engage in Flippa/Acquire.com community forums with analysis (inbound funnel)

## Budget Tier Strategies

### FREE
Scrape public marketplace listings, generate analysis threads, post to r/Entrepreneur and Twitter. Build authority as deal flow analyst. Engagement bait: 'I analyzed 500 online businesses for sale — here's what 3x cash flow ACTUALLY looks like'

### LOW
$0-50/mo: Flippa Pro API access for deeper deal data, promoted Reddit posts for acquisition analysis content

### MID
$50-200/mo: Empire Flippers verified listings access, paid newsletter (Beehiiv) for deal flow alerts to subscribers

## Daily Actions

- [ ] Build biz_acquisition_deal_scanner.py — scrapes Flippa JSON API, Acquire.com RSS, BizBuySell public listings
- [ ] Implement 3-3.5x cash flow scoring model (asking price / stated annual profit = multiple, flag anything under 3.5x)
- [ ] Add institutional knowledge risk flags (solo founder = low risk, team of 5+ = high risk, key-person dependency checks)
- [ ] Wire output into engagement_bait_converter.py for auto-thread generation ('I scanned 200 businesses for sale this week')
- [ ] Schedule cron 2x/week (Mon+Thu 7 AM) — fresh deal data for content calendar
- [ ] Feed high-signal deals into chain_i_analyzed_1500_bootstrapped_startups for cross-reference with bootstrapped startup patterns
- [ ] Route content to CONTENT/social/posting_queue/ for distribution

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
