# Growth Plan: [ACQUISITION] I'm 17 and built a screenshot beautifier for W

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Post r/Windows as 'I built the CleanShot X for Windows because it doesn't exist — free' (story format, no link in title)
2. SEO: surge.sh landing page title 'CleanShot X for Windows — Free Screenshot Beautifier' targeting near-zero competition keyword
3. Add to Alternativeto.net as 'CleanShot X alternative' — passive discovery from 2M+ monthly users
4. Embed watermark on free exports 'Made with [AppName]' — every shared screenshot is organic viral distribution
5. Twitter: 'CleanShot X is $30 and Mac-only. I built the Windows version in a weekend. Link in bio.' — engineer audience bait
6. Product Hunt launch as 'CleanShot X for Windows' — Mac-only gap fills average 300-600 upvotes, confirmed demand category
7. Systematic Mac-to-Windows gap arbitrage: replicate this playbook across top 10 scanner outputs, each is a validated build target

## Budget Tier Strategies

### FREE
r/Windows + r/SideProject posts as solo dev story. Surge.sh SEO page. Alternativeto.net listing. Free watermark viral loop. Twitter thread targeting indie hacker + Windows power user accounts.

### LOW
$20 Reddit Promoted Post targeting r/Windows (500K members, low CPM). $15 Product Hunt feature. Affiliate sidebar links to complementary tools (Loom, Cleanshot Mac, etc.) for passive affiliate income.

### MID
$50-200/mo: Google Ads on 'cleanshot windows' (~$0.80 CPC, high intent). Micro-influencer seeding to Windows 11 tips YouTube channels (5K-50K subs, cheap sponsorships). Retarget site visitors with $20 Stripe upsell for premium backgrounds pack.

## Daily Actions

- [ ] 1. Build screenshot beautifier as static web app — client-side JS only: drag-drop or paste image, choose background color/gradient/blur, padding, rounded corners, drop shadow, device frame option, export PNG. Zero backend. Zero infra cost.
- [ ] 2. Deploy to surge.sh: domain screenmaxx.surge.sh or similar. SEO meta: 'CleanShot X for Windows — Free Screenshot Beautifier'. No robots.txt block on this one.
- [ ] 3. Wire Stripe Payment Link ($9 one-time) for premium tier: removes watermark, unlocks 20+ custom backgrounds, batch export. Embed as upgrade button with data-upgrade attribute.
- [ ] 4. Run mac_only_gap_scanner.py immediately to validate pipeline and surface next 9 targets from top-10 list. Add to Monday 7AM cron.
- [ ] 5. Generate launch posts via engagement_bait_converter.py. Queue to CONTENT/social/posting_queue/ for r/Windows, r/SideProject, Twitter.
- [ ] 6. Add to OPS/KPI_DASHBOARD.md: weekly unique visitors, free-to-paid CVR, screenshots processed.
- [ ] 7. Update app_factory_command_center.py with new app entry. Update PRINTMAXX_SYSTEM_MAP.md if gap scanner is a net-new recurring cron.

## Tooling

```json
{
  "browser": "playwright (Setapp catalog + Product Hunt scraping)",
  "email": "none",
  "content": "engagement_bait_converter.py for launch posts, content_repurposer.py for cross-platform"
}
```
