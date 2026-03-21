# Growth Plan: [PH LAUNCH] Joy for Gmail: A Gmail with clearer inbox, focus

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-500/mo

---

## Tactics

1. Route to existing chain_14_ph_launches_today chain — same pattern, no new infra needed
2. Filter PH scraper for email/productivity/inbox/SaaS tags — Joy for Gmail signals this niche has active makers
3. Reach out within 24-48h of launch — makers are online, checking comments, maximally receptive
4. Reference their specific value prop in cold outreach (noise reduction = they value signal — pitch signal tools or EAS)
5. Mine PH comments for early adopters — these users are warm leads for complementary tools and affiliate products

## Budget Tier Strategies

### FREE
Daily PH scrape via Playwright or PH JSON API, extract maker Twitter/site from profile, send personalized cold DMs via existing cold email scripts, mine upvoter list for ICP prospects

### LOW
$0-50/mo — Hunter.io free tier (25/mo) for maker email discovery, Apollo free tier for enrichment, schedule via existing cron

### MID
$50-200/mo — Instantly warm inboxes for scaled maker outreach, LinkedIn Sales Nav to enrich PH founder profiles, retarget upvoters via Twitter ads

## Daily Actions

- [ ] Route this entry to existing chain: chain_14_ph_launches_today__high_quality_b2b_ — identical pattern
- [ ] Verify ph_scraper has email/productivity/SaaS category filter active (not just top-of-day launches)
- [ ] Add upvote velocity threshold: >50 upvotes in first 6h = priority outreach queue
- [ ] Confirm cron at 8 AM daily catches fresh launches before 48h window closes
- [ ] Add Joy for Gmail maker as seed contact in outreach queue for same-day test

## Tooling

```json
{
  "browser": "Playwright (PH scrape, profile extraction)",
  "email": "custom cold email scripts (existing)",
  "content": "none"
}
```
