# Growth Plan: The chillest business you can run right now is building AI U

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $300-900/mo (2-3 pages at $150-300/page realistic, discounted 60% from stated $500-2k)

---

## Tactics

1. Start 3 pages simultaneously across different niches to find winner faster
2. Use engagement warming on new pages (comment pods via existing accounts)
3. Cross-promote pages from each other to bootstrap follower transfer
4. Stagger posting times to avoid algorithmic suppression of same-account patterns
5. Repost top-performing UGC from organic creators (with credit) to seed algorithmic trust
6. Reply to all comments within first 30 min of posting to boost early engagement signal

## Budget Tier Strategies

### FREE
3 pages, claude -p UGC scripts, FB/IG Graph API scheduling (free tier), affiliate links from programs already in LEDGER/CREATOR_PROGRAMS.csv, cross-promote between pages, manual brand outreach once threshold hit

### LOW
$0-50/mo: $20-30 boost on top-performing posts to hit retainer-ready engagement thresholds faster, sign up 2-3 higher-commission affiliate programs (ConvertKit, SEMrush)

### MID
$50-200/mo: paid micro-influencer shoutouts ($50-100 each) to seed 5 pages simultaneously, GoLogin for multi-account management, SOAX proxies for account isolation

## Daily Actions

- [ ] Route to existing chain_the_chillest_business_you_can_run_right_ — wire new DAG into it
- [ ] Create ai_ugc_affiliate_page_manager.py with FB/IG Graph API posting + claude -p content gen
- [ ] Pull affiliate programs from LEDGER/CREATOR_PROGRAMS.csv for link injection
- [ ] Set engagement threshold trigger: 1K engagements/week → auto-fire brand retainer outreach
- [ ] Cron at 7AM daily: generate 30 scripts across 3 niches, schedule 6 posts/page/day
- [ ] Track in KPI_DASHBOARD.md: pages active, avg engagement, retainer pipeline

## Tooling

```json
{
  "browser": "playwright (FB/IG Graph API preferred, browser fallback for setup only)",
  "email": "existing cold_email scripts for brand outreach",
  "content": "claude -p for UGC script generation + engagement_bait_converter.py for repurposing winners"
}
```
