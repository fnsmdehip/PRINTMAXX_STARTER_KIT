# Growth Plan: [PH LAUNCH] Caplo: Real-time AI captions &amp; translation f

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Upvote Caplo and leave genuine comment referencing our captioning/accessibility integration capabilities — visibility to 400+ upvoters
2. Reply to Caplo maker's PH discussion thread with use case question — draws iOS dev audience to our profile
3. Generate tweet thread: 'Caplo just launched real-time AI captions for iOS — here are 5 apps that should add this today' — tag Caplo, positions us as market commentator
4. Scrape Caplo's competitors on PH (caption/translation tools) for cumulative lead pool across all upvoter bases

## Budget Tier Strategies

### FREE
Playwright scrape PH upvoters → enrich via Twitter bio search → custom cold email script with EAS pitch; reply to PH comments organically

### LOW
$0-50/mo: Apollo.io free tier for email enrichment on top leads; boost tweet thread with $20 Twitter ads targeting iOS developers

### MID
$50-200/mo: Hunter.io enrichment on full lead list; Instantly warmup for dedicated outreach domain

## Daily Actions

- [ ] WIRE into chain_14_ph_launches_today__high_quality_b2b_ — add Caplo URL as a new target, no new chain needed
- [ ] Run playwright scraper against producthunt.com/posts/caplo — extract upvoter profiles
- [ ] Filter for iOS devs/mobile founders (keyword match on bios: iOS, Swift, mobile app, founder)
- [ ] Generate personalized outreach: 'Saw you upvoted Caplo on PH — we build full iOS apps with AI features integrated from day one. Worth a 15-min call?'
- [ ] Queue in cold email pipeline with 48h send window post-launch (peak intent window)
- [ ] Generate 1 tweet thread via engagement_bait_converter.py: AI accessibility tools for iOS — Caplo angle
- [ ] Post tweet + PH comment same day as launch for max visibility

## Tooling

```json
{
  "browser": "playwright (PH scraping, no login needed)",
  "email": "custom cold email script (AUTOMATIONS/cold_email_sender.py)",
  "content": "engagement_bait_converter.py for tweet thread generation"
}
```
