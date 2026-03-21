# Growth Plan: just got back from an industry conference and genuinely feel

**Created:** 2026-03-20 18:35
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo

---

## Tactics

1. Scrape conference hashtags on Twitter/LinkedIn for attendee self-identification
2. Monitor Eventbrite/Luma for new industry events and auto-scrape registrant-visible data
3. Cross-reference scraped names with LinkedIn Sales Navigator free tier for email enrichment
4. Content play: repurpose conference-waste narrative as contrarian thread (conferences are dead, cold email beats $4K flights)

## Budget Tier Strategies

### FREE
Scrape public conference sites (speakers, sponsors, exhibitors). Use conference hashtags on Twitter to find attendees. Cold email via existing outbound infra. Post contrarian content about conference ROI waste.

### LOW
$0-50/mo: Add Hunter.io free tier (50 lookups/mo) for email verification on scraped contacts

### MID
$50-200/mo: Apollo.io basic for bulk enrichment of conference attendee lists

## Daily Actions

- [ ] Build conference_attendee_scraper.py that takes conference URL and extracts speaker/sponsor/exhibitor lists
- [ ] Add to chain_cold_outbound as a new lead source type (conference_leads)
- [ ] Schedule weekly Monday 5AM cron to check 3 industry event aggregator pages for new conferences
- [ ] Feed scraped contacts into existing EAS lead pipeline for qualification
- [ ] Generate 1 contrarian content piece (conferences are $4K lead gen theater) for posting queue

## Tooling

```json
{
  "browser": "playwright for conference site scraping",
  "email": "existing cold outbound scripts",
  "content": "engagement_bait_converter.py for conference-waste narrative thread"
}
```
