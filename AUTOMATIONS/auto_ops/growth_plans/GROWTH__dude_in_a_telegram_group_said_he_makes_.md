# Growth Plan:  dude in a telegram group said he makes money "rating produc

**Created:** 2026-03-20 18:10
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo per niche guide, $1K-4K/mo with 5+ niches (discounted from claimed $17K)

---

## Tactics

1. SEO: programmatic 'best X for Y' longtail pages (best meditation app for beginners, best quran app 2026, etc.)
2. Reddit: post genuine reviews in niche subreddits with link to full ranked guide
3. Twitter: thread format — 'I bought and tested 30 [niche] apps. Here's my ranking:' with paywall for full list
4. Cross-pollinate: each ranking guide links to our own apps where they rank well (self-serving but legitimate)
5. Affiliate stacking: earn affiliate commission on products we rank AND sell the guide itself — double monetization
6. Update cycle: 'Updated March 2026' freshness signal drives repeat purchases and SEO

## Budget Tier Strategies

### FREE
SEO longtail pages (generate_longtail skill), Reddit organic posts, Twitter threads, cross-link from our 114 deployed sites, email to existing leads

### LOW
$10-30/mo boosted tweets on ranking threads, Product Hunt launch for the guide site itself

### MID
$50-150/mo Google Ads on 'best X app' keywords (high commercial intent, converts well for comparison content)

## Daily Actions

- [ ] 1. Build niche_product_ranker.py with scraping + Claude scoring pipeline
- [ ] 2. Start with niches we already know: AI tools, prayer/faith apps, fitness trackers, meditation apps, streak apps
- [ ] 3. Generate first guide: 'Best AI Coding Tools 2026 — 30 Tools Ranked' (we have deep alpha on this)
- [ ] 4. Build landing page template (reuse app factory pattern), deploy to surge
- [ ] 5. Create Stripe product ($29-39), wire payment link
- [ ] 6. Generate SEO longtail pages: 'best X for Y' variations (50+ per niche)
- [ ] 7. Distribute: Twitter thread + Reddit posts + email to relevant leads
- [ ] 8. Cron: weekly rescrape for freshness, monthly guide updates
- [ ] 9. Stack affiliates: sign up for affiliate programs of top-ranked products, embed links in guides

## Tooling

```json
{
  "browser": "playwright_mcp",
  "email": "custom_cold_script",
  "content": "claude_p_content_gen + content_factory"
}
```
