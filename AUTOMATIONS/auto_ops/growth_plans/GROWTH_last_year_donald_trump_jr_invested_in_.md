# Growth Plan: Last year, Donald Trump Jr. invested in a rare earths startu

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo

---

## Tactics

1. Quote-tweet unusual_whales and similar finance accounts with our own deeper analysis to draft off their audience
2. Post threads with specific dollar amounts and timelines (10x in 3 months) — finance Twitter rewards specificity
3. Cross-post to r/wallstreetbets, r/politics, r/stocks for organic reach
4. Tag political figures in posts for controversy-driven engagement

## Budget Tier Strategies

### FREE
Organic threads on political-insider trades using free STOCK Act data (efdsearch.senate.gov) + USAspending.gov API. Reply to unusual_whales/finance accounts with deeper analysis. Cross-post Reddit.

### LOW
$10-30/mo for proxy rotation if Senate disclosure site rate-limits scraper

### MID
$50-100/mo for a dedicated finance newsletter via Beehiiv free tier upgraded, paid Twitter promotion on best-performing threads

## Daily Actions

- [ ] Build scraper for efdsearch.senate.gov (Senate STOCK Act periodic transaction reports — free, public, no API key needed)
- [ ] Build scraper for House financial disclosures (clerk.house.gov)
- [ ] Build USAspending.gov API client for government contracts/loans/grants over $10M
- [ ] Cross-reference: when a political figure buys stock in company X AND company X receives government contract/loan within 90 days, flag as high-signal
- [ ] Route flagged signals to engagement_bait_converter.py for Twitter thread generation
- [ ] Queue threads to CONTENT/social/posting_queue/ with unusual_whales-style formatting (dollar amounts, timelines, named entities)
- [ ] Cron weekday mornings — political disclosures update on business days

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
