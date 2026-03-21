# Growth Plan: [ACQUISITION] I built a group trip planner with a Game Boy a

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo per app (viral acquisition spike → freemium conversions or affiliate clicks)

---

## Tactics

1. Post to r/SideProject with aesthetic screenshot as hero — nostalgia hooks drive upvotes organically
2. Cross-post to r/webdev, r/InternetIsBeautiful, r/NostalgiaForInfinity for the retro angle
3. Twitter: screenshot + short caption 'built [app] with a [aesthetic] UI because the web is too clean' — high shareability, no follower requirement
4. Apply 4-5 retro aesthetic variants across existing APP_FACTORY streak/habit apps to maximize weekly posting surface area without rebuilding anything
5. Batch-produce 8 themed screenshots in one Playwright session, schedule across 8 consecutive Mondays

## Budget Tier Strategies

### FREE
Post to r/SideProject + Twitter with retro aesthetic screenshots weekly. Apply Game Boy/Win95/terminal CSS themes to 5 existing APP_FACTORY builds using a single shared stylesheet. Use engagement_bait_converter.py to convert each screenshot post into 3 tweets. Zero cost, leverages existing 47 live apps.

### LOW
$0-50/mo: Submit top-performing aesthetic app to ProductHunt with aesthetic as the differentiator. Boost 1-2 Reddit posts. Post to IndieHackers Show IH thread.

### MID
$50-200/mo: Sponsor niche retro-computing or indie-dev newsletters with aesthetic screenshots. Run $30-50 Reddit promoted posts targeting r/gaming or r/nostalgia adjacent audiences.

## Daily Actions

- [ ] Create MONEY_METHODS/APP_FACTORY/themes/retro/ with CSS files: gameboy.css, win95.css, terminal.css, y2k.css
- [ ] Apply gameboy.css to 3 existing streak apps (soberstreak, prayerlock, or fitness-streak) as CSS overlay only
- [ ] Run Playwright screenshot bot to capture themed apps at 1280x800 and 375x812 viewports, output to themes/screenshots/
- [ ] Run claude -p to generate r/SideProject post copy for each themed app — emphasize aesthetic + utility angle
- [ ] Post to r/SideProject + r/webdev + Twitter via Playwright MCP, log post URLs to distribution_log.json
- [ ] Track upvote velocity after 24h; if any post hits 50+ upvotes apply same aesthetic to 5 more apps
- [ ] Wire weekly Monday 10 AM cron entry to aesthetic_arbitrage_poster.py --next-app
- [ ] Feed screenshots into engagement_bait_converter.py for 3 tweets per app launch

## Tooling

```json
{
  "browser": "playwright (screenshot capture + Reddit/Twitter posting)",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
