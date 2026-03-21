# Growth Plan: I built a tool that turns a restaurant's PDF menu into a pro

**Created:** 2026-03-20 13:50
**Venture:** LOCAL_BIZ
**Budget Tier:** FREE
**Revenue Est:** $100-500/mo

---

## Tactics

1. Cold outreach with free preview (reciprocity hook — menu already built before asking for money)
2. Target restaurants with NO website or outdated sites first (lowest competition, highest pain)
3. Cross-sell: digital menu → full website → Google Business optimization (upsell ladder)
4. Post before/after screenshots on local business subreddits and Twitter for organic leads

## Budget Tier Strategies

### FREE
Scrape leads from Google Maps, cold email with free preview links, post case studies on Reddit/Twitter

### LOW
$0-50/mo: Boost Facebook posts targeting restaurant owners in specific zip codes, run $5/day local awareness ads

### MID
$50-200/mo: Partner with local restaurant associations, sponsor small-biz meetups, Google Ads on 'digital menu for restaurants'

## Daily Actions

- [ ] Build pdf_menu_digitizer.py: accepts PDF URL → Claude extracts structured menu data → generates responsive HTML menu page
- [ ] Wire into existing LOCAL_BIZ lead scraping to find restaurants with PDF menus
- [ ] Auto-deploy generated menus to surge.sh preview URLs
- [ ] Cold email restaurant owners with the free preview as the hook
- [ ] Track conversions: free preview → paid ($29/mo hosting or $199 one-time)
- [ ] Add to weekly cron (Monday 7:30 AM) for batch processing new leads

## Tooling

```json
{
  "browser": "playwright",
  "email": "custom cold email scripts",
  "content": "claude -p for PDF parsing and HTML generation"
}
```
