# Growth Plan: [r/SaaS] How do you get paying users to your saas ?

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0 direct / content attribution to $50-200/mo via audience growth → affiliate or product funnel

---

## Tactics

1. Post 'X ways to get your first 10 paying SaaS users' thread on Twitter — high engagement niche
2. Cross-post distilled tactic list to r/indiehackers and r/SaaS as value post (no promotion)
3. Use engagement_bait_converter.py to spin 5 variants from top tactics
4. Reply to similar threads on r/SaaS with our own content link as organic distribution

## Budget Tier Strategies

### FREE
Mine top-voted r/SaaS replies weekly via background_reddit_scraper.py, extract actionable tactics, convert to Twitter threads and Reddit value posts via engagement_bait_converter.py. Zero cost, high relevance to existing audience.

### LOW
$0-50/mo: Boost top-performing tweet from this angle with $10-20 Twitter ads targeting indie hacker / SaaS founder keywords.

### MID
$50-200/mo: Sponsor a r/SaaS post or pay a micro-influencer in the indie hacker space to amplify the thread.

## Daily Actions

- [ ] Run background_reddit_scraper.py targeting r/SaaS threads with keywords: 'paying users', 'first customers', 'user acquisition'
- [ ] Extract top-voted reply tactics (score > 50 upvotes) from matching threads
- [ ] Pipe extracted tactics into engagement_bait_converter.py with context 'SaaS user acquisition'
- [ ] Output 3+ posts to CONTENT/social/posting_queue/ for review
- [ ] Wire weekly cron: 0 7 * * 1 to repeat automatically

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + background_reddit_scraper.py"
}
```
