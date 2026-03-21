# Growth Plan: [ACQUISITION] I built a forced break tool for my own Tech Ne

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Post 'Is a screen lockout too aggressive?' as a genuine question in r/productivity — the controversy drives replies and surfaces our app naturally in comments
2. Reply to the original r/SideProject poster comparing their approach to DeskBreak/WalktounLock — instant warm traffic from their thread
3. SEO cluster: 'tech neck app', 'forced screen break software mac', 'burnout prevention desktop app' — 3 longtail pages pointing to our existing builds
4. Twitter/X thread: 'I tracked my screen time for 30 days without forced breaks vs with — here's the difference' (uses our apps as the mechanism)
5. Product Hunt launch for DeskBreak targeting 'Maker Stories' section — the original r/SideProject post format converts well to PH

## Budget Tier Strategies

### FREE
Reddit organic seeding in r/SideProject + r/productivity + r/workfromhome. Reply to high-traffic break/burnout threads with our app URL. Twitter thread repurposing the 'too aggressive?' hook. SEO longtail pages on deskbreak-web domain.

### LOW
$20-30 Reddit promoted post targeting r/workfromhome + r/remotework with the lockout controversy angle. 3-5x ROAS expected on $0.25-0.40 CPC subs.

### MID
$50-150/mo micro-influencer seeding with WFH + ergonomics creators on TikTok/YouTube Shorts. 'Tech Neck' is a trending search term — 30-60s demo video converts well.

## Daily Actions

- [ ] Verify deskbreak-web + walktounlock-web + focuslock-web are live (OPS/DEPLOYMENT_URLS.md)
- [ ] Wire Stripe payment link to whichever of the 3 apps lacks one (payment_integrator.py --route APP)
- [ ] Run subagent: scrape r/SideProject + r/productivity for break-tool pain language
- [ ] Run engagement_bait_converter.py with extracted pain phrases + our 3 app URLs as inputs
- [ ] Append generated posts to CONTENT/social/posting_queue/break_apps_cycle.txt
- [ ] Reply to original r/SideProject poster (manual — 1 min, high ROI warm traffic)
- [ ] Generate 2 SEO longtail pages via content-generator + deploy to deskbreak-web
- [ ] Add cron entry: break_app_content_seeder.py runs Mon/Thu 9 AM

## Tooling

```json
{
  "browser": "playwright (Playwright MCP for Reddit scraping)",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
