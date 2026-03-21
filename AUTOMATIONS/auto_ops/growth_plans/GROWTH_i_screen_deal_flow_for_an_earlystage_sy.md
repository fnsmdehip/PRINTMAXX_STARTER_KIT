# Growth Plan: I screen deal flow for an early-stage syndicate

**Created:** 2026-03-21 12:40
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo (content engagement + potential $49/mo newsletter, low ceiling)

---

## Tactics

1. Post weekly 'startups worth watching' thread on Twitter — high engagement from founder/investor community
2. DM syndicate leads on LinkedIn offering free sample of automated deal memos
3. Cross-post startup breakdowns to r/startups, r/entrepreneur, r/SideProject with engagement bait framing
4. Build email list around 'curated weekly deal flow' — free tier = 3 deals, paid = full 10

## Budget Tier Strategies

### FREE
Twitter threads from deal memos, Reddit posts, engage with funded founders to build credibility, post HN comments on Show HN threads with value-add analysis

### LOW
$20-50/mo Beehiiv for deal flow newsletter, cold email 50 syndicate leads/week with free sample memo

### MID
$50-200/mo LinkedIn outreach to 200+ angel investors per month, sponsor relevant newsletters with deal flow tool

## Daily Actions

- [ ] Wire startup_deal_flow_screener.py to pull from HN /newest, PH API, Reddit JSON — no auth needed
- [ ] Score each startup: +1 revenue mentioned, +1 team credentials, +1 traction number, +1 market keyword match
- [ ] Generate deal memos via claude -p for top 10% scored
- [ ] Route memo content to engagement_bait_converter.py for Twitter/LinkedIn posts
- [ ] Add to chain_14_ph_launches_today handoff — it already tracks PH launches, extend with scoring layer
- [ ] Cron at 7 AM daily — fresh deal flow before US market opens (timing advantage)

## Tooling

```json
{
  "browser": "playwright (HN/PH scraping)",
  "email": "none initially",
  "content": "content_factory + engagement_bait_converter.py"
}
```
