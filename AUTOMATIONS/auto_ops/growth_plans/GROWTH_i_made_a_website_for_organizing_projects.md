# Growth Plan: I made a website for organizing projects and tracking tasks 

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $20-150/mo per tool via display ads + affiliate links; compounding as more tools hit r/InternetIsBeautiful front page

---

## Tactics

1. Submit existing no-login browser-only builds (focuslock-web, prayerlock-web, soberstreak, walktounlock-web) to r/InternetIsBeautiful — these already qualify, zero build needed
2. Title formula proven by Kanjo: 'I made a [noun] for [verb]. No accounts. No servers. 100% private.' — use this template for all submissions
3. Cross-post to r/nosurf, r/productivity, r/selfhosted for tools with privacy angle
4. Pin 'no login required' and 'runs in browser' in the first sentence of every app landing page for SEO
5. Add AdSense or affiliate link (e.g. Notion affiliate) to the tools — r/InternetIsBeautiful traffic converts to display ad clicks
6. After each Reddit post hits >50 upvotes, repurpose as Twitter thread: 'I built X with no backend. Here is how.' — routes to printmaxxer account

## Budget Tier Strategies

### FREE
Submit 1 existing no-login app per week to r/InternetIsBeautiful using proven title formula. Cross-post to r/nosurf and r/productivity. Generate 3 tweets per submission via engagement_bait_converter.py.

### LOW
$0-50/mo: Boost top-performing Reddit post with Reddit Ads ($5-10 CPC) to drive app landing page traffic. Add email capture on landing page to build list.

### MID
$50-200/mo: Sponsor a r/InternetIsBeautiful-style newsletter or niche ProductHunt alternative. Run retargeting ads to visitors who bounced from app landing pages.

## Daily Actions

- [ ] Identify existing App Factory builds that are no-login/localStorage-only: focuslock-web, prayerlock-web, soberstreak, walktounlock-web, sleepmaxx-web, deskbreak-web, tasksmash-web
- [ ] Create rib_distribution_poster.py: reads MONEY_METHODS/APP_FACTORY/builds/, filters for no-login tools, generates r/InternetIsBeautiful submission titles using Kanjo template formula, outputs to CONTENT/social/posting_queue/
- [ ] Wire rib_distribution_poster.py to cron: 10 AM Monday weekly
- [ ] Route each generated submission through engagement_bait_converter.py for 3 companion tweets
- [ ] Add 'No login. No account. Runs in your browser.' badge to all qualifying app landing pages via sed/patch
- [ ] Add AdSense snippet to top 3 highest-traffic no-login apps to monetize incoming r/IIB traffic
- [ ] Wire into chain_boring_tool_strategy_5kmo_path__tool as a distribution step

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + twitter_warmup_poster.py"
}
```
