# Growth Plan: Kinda, in 2014 I made $5K/mo with Nomad List, 2015 was $10K/

**Created:** 2026-03-21 12:40
**Venture:** MONETIZE
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo incremental lift from cross-promotion on existing 47 live apps — no new build required

---

## Tactics

1. Inject 'Also by us' footer section on ALL deployed surge/vercel apps pointing to other apps in portfolio
2. AdSense blog → YouTube → directory stacking: each tier feeds the next with SEO content
3. Niche directory cross-links: streak apps link to each other, tool comparisons link to our tools
4. Build simple AdSense-eligible blog content auto-generated from existing app landing pages (repurpose copy)
5. Add 'built by same team as X' trust signal to newer apps using established app's brand equity
6. Auto-generate 'Tools we use' pages on each app that link other portfolio apps as recommended tools

## Budget Tier Strategies

### FREE
Auto-inject cross-promotion HTML snippets across all 47 live sites via script. Zero ad spend. SEO compounding from internal links. Each new app launch triggers automated backlink injection on all existing properties.

### LOW
$10-30/mo: One AdSense blog as content funnel feeding all apps. Auto-generated posts from existing app copy via claude -p. Blog feeds organic traffic → app portfolio.

### MID
$50-150/mo: Paid retargeting — pixel visitors to app A, retarget them with app B ads. Cross-audience arbitrage across portfolio.

## Daily Actions

- [ ] Scan MONEY_METHODS/APP_FACTORY/builds/ for all live index.html files
- [ ] Generate 'Also by us' HTML snippet with links to top 5 other apps by category (streak apps cross-link streaks, tools cross-link tools)
- [ ] Inject snippet before </body> in each index.html using portfolio_cross_promotion_injector.py
- [ ] Deploy updated files via surge CLI (all 47 sites)
- [ ] Wire weekly cron to re-run injection when new apps are added
- [ ] Route to chain_boring_tool_strategy_5kmo_path__tool for long-term niche directory expansion

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
