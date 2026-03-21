# Growth Plan: I spent &gt; $60K/month on PR agencies at a startup that rai

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (press backlinks + traffic to existing apps)

---

## Tactics

1. Extract DIY PR framework from post — what agencies actually do (media list building, pitch angle testing, journalist relationship cadence) and wire into cold_outbound scripts for our own app press coverage
2. Convert to engagement bait: '6-country PR at $60K/mo taught me these 3 things you can do for $0' — hooks directly from the source material
3. Build journalist contact scraper targeting indie hacker / startup beat reporters using patterns from this post (Playwright MCP, existing chain already wired)

## Budget Tier Strategies

### FREE
Use extracted PR framework to pitch our own apps to TechCrunch/ProductHunt/IndieHackers. Generate 3 Twitter posts with engagement hooks. Add journalist contacts to cold outreach pipeline.

### LOW
$0-50/mo — PR Newswire free tier for 1 press release/mo about top app launch. Use HARO (free) to respond to journalist queries in relevant niches.

### MID
$50-200/mo — Qwoted or ProfNet subscription for journalist query access. One sponsored placement in a startup newsletter.

## Daily Actions

- [ ] Route to existing chain_i_spent__60kmonth_on_pr_agencies_at_a — already integrated, do not duplicate
- [ ] Run engagement_bait_converter.py on the PR framework angle to generate 3 posts for posting_queue
- [ ] Add 'DIY PR for app launches' to OPS/DAILY_TACTICAL_PLAN.md as a weekly KPI action
- [ ] Check CONTENT/social/posting_queue/ to confirm posts aren't already queued from prior integrations

## Tooling

```json
{
  "browser": "none",
  "email": "custom cold email scripts",
  "content": "engagement_bait_converter.py"
}
```
