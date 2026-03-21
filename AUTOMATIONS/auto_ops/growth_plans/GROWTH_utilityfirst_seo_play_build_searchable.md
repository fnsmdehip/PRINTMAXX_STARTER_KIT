# Growth Plan: Utility-first SEO play: build searchable database of 1000+ c

**Created:** 2026-03-20 13:50
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Reddit viral seeding: post to r/InternetIsBeautiful, r/lifehacks, r/technology, r/software with genuine utility framing
2. SEO programmatic: 1000+ pages targeting '[company] cancel subscription' long-tail
3. Cross-link from existing PRINTMAXX landing pages to boost domain authority
4. Browser extension (Phase 2): detect subscription pages and offer one-click cancel links
5. Affiliate to alternatives: when user cancels Netflix, suggest free alternatives with affiliate links
6. HN Show HN post for developer audience

## Budget Tier Strategies

### FREE
Reddit organic posts (r/InternetIsBeautiful, r/lifehacks, r/degoogle, r/frugal), HN Show HN, programmatic SEO via longtail page generation, cross-linking from existing 47 deployed sites, Twitter threads about subscription waste

### LOW
$10-30/mo: Reddit promoted post in r/personalfinance, Google Ads on top 20 highest-volume cancel keywords

### MID
$50-150/mo: Micro-influencer sponsorships in personal finance niche, Product Hunt launch with upvote campaign, content syndication to Medium/Dev.to

## Daily Actions

- [ ] 1. Scrape cancellation URLs: crawl top 1000 SaaS sites for cancel/delete account pages using Playwright MCP + requests fallback
- [ ] 2. Supplement with existing databases (justdelete.me open data, Reddit compilations)
- [ ] 3. Build JSON database with fields: company, category, cancel_url, difficulty, steps_count, alternative_suggestions
- [ ] 4. Generate individual SEO pages per company using generate-longtail pattern (HTML template + JSON data)
- [ ] 5. Build search/filter homepage with client-side JS search over the JSON index
- [ ] 6. Deploy to surge.sh under cancelmaxx.surge.sh or similar domain
- [ ] 7. Generate sitemap.xml, submit to Google Search Console
- [ ] 8. Seed Reddit posts to r/InternetIsBeautiful, r/lifehacks, r/frugal with genuine utility angle
- [ ] 9. Add affiliate links to alternative services on each cancel page (ConvertKit, Beehiiv alternatives)
- [ ] 10. Schedule weekly cron to re-scrape and update database with new services
- [ ] 11. Route to engagement_bait_converter.py for social content generation about subscription waste stats

## Tooling

```json
{
  "browser": "playwright_mcp_for_scraping_cancel_pages",
  "email": "none",
  "content": "content_factory_for_reddit_distribution_posts"
}
```
