# Growth Plan: [PLATFORM UPDATE] WordPress.com now lets AI agents write and

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Create 3-5 WordPress.com free-tier satellite sites targeting different niches (faith, fitness, solopreneur tools) — each one links back to our deployed surge.sh apps
2. Use WordPress.com's AI agent API (application passwords + REST /wp/v2/posts endpoint) to auto-publish 10 longtail posts/day per site — zero manual effort
3. Internal link every post to our affiliate pages and app landing pages for link equity transfer
4. Submit WordPress.com site sitemaps to Google Search Console — WordPress.com domain authority accelerates indexing vs our new surge.sh domains
5. Repurpose every published WP post through content_repurposer.py for social distribution — one piece, 5+ channels

## Budget Tier Strategies

### FREE
WordPress.com free tier (3 sites) + REST API with application passwords. Feed content from existing content_multiplier.py. 10 posts/day/site = 300 posts/month = SEO compounding. No cost.

### LOW
$4/mo WordPress.com Personal plan removes ads on satellite sites, adds custom domain mapping — worth it once one site hits 500 organic visits/mo.

### MID
$25/mo WordPress.com Business plan adds plugins (Yoast SEO, AdSense integration) — upgrade when organic traffic justifies monetization via display ads.

## Daily Actions

- [ ] Create 3 WordPress.com accounts (faith niche, fitness niche, solopreneur/tools niche) — free tier, 10 min
- [ ] Generate application passwords via WordPress.com dashboard for each site (Settings → Security → Application Passwords)
- [ ] Build wordpress_content_publisher.py: pulls from CONTENT/social/posting_queue/, hits /wp/v2/posts REST endpoint, handles auth, sets categories/tags, publishes or schedules
- [ ] Wire into n8n: trigger = content_multiplier.py output file created → format for WP → POST to 3 sites in parallel
- [ ] Add cron 0 7 * * * to run daily content push (10 posts per site)
- [ ] Submit sitemaps to Google Search Console for each WP site
- [ ] Add internal links in post template pointing to top affiliate pages (SEMrush, Instantly, surge-deployed apps)

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_multiplier.py + engagement_bait_converter.py \u2192 WordPress REST API"
}
```
