# Growth Plan: [PH LAUNCH] Claude Cowork Projects: Tasks, context, and file

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-700/mo

---

## Tactics

1. Scrape PH daily at 7 AM — launches go live at midnight PST, peak engagement 8-10 AM PST
2. Filter for AI/productivity/workspace/developer-tools tags — highest willingness to pay
3. Extract founder Twitter + email from PH maker profile (public data)
4. Personalize outreach referencing their specific launch (product name + hook from PH listing)
5. Route into existing chain_14_ph_launches_today__high_quality_b2b_ for 48h sequence
6. Post thread: 'Top AI workspace tools launching this week on PH' — drives engagement + positions as curator
7. Comment on top PH launches with value-add insight (establishes presence, inbound pull)

## Budget Tier Strategies

### FREE
Playwright scrape PH daily, extract public maker emails/Twitter handles, personalized cold email via custom script using Claude -p for copy generation, comment on launches for visibility

### LOW
$0-50/mo — Instantly warmup pool for cold email deliverability, 1-2 targeted PH sponsored comments ($20-30)

### MID
$50-200/mo — PH Ship subscriber list access for pre-launch founders, Browserbase for anti-bot scraping at scale

## Daily Actions

- [ ] Enhance existing PH scraper to filter launches by tags: AI, productivity, workspace, developer-tools, SaaS
- [ ] Extract: product name, tagline, maker name, maker Twitter, upvote count, comment count
- [ ] Score lead quality: upvotes >50 = HOT, team size 1-3 = solo founder = best prospect
- [ ] Append scored leads to LEDGER/INBOUND_LEADS.csv with source=ProductHunt
- [ ] Route into chain_14_ph_launches_today__high_quality_b2b_ for automated 48h outreach sequence
- [ ] Run engagement_bait_converter.py on top 3 launches for weekly 'PH picks' Twitter thread

## Tooling

```json
{
  "browser": "playwright (PH scrape) + requests fallback (PH API /v1/posts)",
  "email": "custom cold email script (existing outbound pipeline)",
  "content": "engagement_bait_converter.py for weekly PH roundup thread"
}
```
