# Growth Plan: [PH LAUNCH] GentleLimit: Mindful screen time for macOS witho

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $150-400/mo

---

## Tactics

1. Comment on GentleLimit PH page within 24h of launch — helpful framing, builds visibility with their exact audience
2. Search Twitter for 'GentleLimit' and reply with our PWA alternative (no install required = objection removal)
3. Post on r/macapps and r/productivity: 'built a no-download version of mindful screen time' — PH launch creates SEO moment
4. Add to macOS app directories: AlternativeTo, Slant, Product Hunt (our own launch 2 weeks later)
5. Target PH upvoter Twitter handles for manual DM: 'Hey, saw you upvoted GentleLimit — built a cross-platform version'

## Budget Tier Strategies

### FREE
PH comment engagement + Twitter reply farming on GentleLimit mentions + post in r/macapps r/productivity + AlternativeTo listing + surge deploy

### LOW
$0-50/mo — boost our own PH launch with upvote seeding 2 weeks after GentleLimit's momentum fades, target same audience

### MID
$50-200/mo — micro-influencer in productivity/macOS space ($50-100 sponsored mention), Reddit promoted post in r/productivity targeting screen time keywords

## Daily Actions

- [ ] Run playwright scrape on GentleLimit PH page → ph_gentlelimit_intel.json
- [ ] Qualify commenters → identify USER segment (our buyers)
- [ ] app_factory_autopilot.py --build mindful-screentime-web — differentiate: no install, cross-platform, free
- [ ] surge deploy: mindful-screentime.surge.sh
- [ ] Stage qualified leads into existing cold outbound pipeline (chain_cold_outbound)
- [ ] Post comment on GentleLimit PH page with helpful framing
- [ ] Generate 3 tweets via engagement_bait_converter.py on 'blocking vs awareness' screen time debate
- [ ] Schedule our own PH launch 2 weeks out to ride the category momentum

## Tooling

```json
{
  "browser": "playwright MCP (scrape PH page, no auth needed)",
  "email": "custom cold email scripts (existing outbound pipeline)",
  "content": "engagement_bait_converter.py",
  "deploy": "surge.sh (existing)"
}
```
