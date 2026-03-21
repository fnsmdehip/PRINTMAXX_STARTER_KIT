# Growth Plan:  i am your client &amp; sell me your service. what are you b

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (lead gen feeds outbound pipeline, not direct revenue)

---

## Tactics

1. Post during peak X engagement hours (10am-12pm EST Sunday/weekday evenings)
2. Quote-tweet top replies to boost thread visibility and reward engagement
3. Cross-post prompt variants to indie hacker subreddits and communities
4. Tag 2-3 larger accounts to seed initial engagement
5. Reply to every response within first hour to signal algorithm engagement

## Budget Tier Strategies

### FREE
Organic posting on X + cross-post to r/SideProject r/indiehackers. QT best replies for double engagement. Rotate 5 prompt templates weekly. Scrape replies for lead pipeline.

### LOW
$0-50/mo: Boost top-performing threads with X ads at $5-10/thread to expand reach beyond existing followers

### MID
$50-200/mo: Run persistent engagement campaigns across 3 niche accounts (tech/faith/fitness) with scheduled posting and paid boosts on winners

## Daily Actions

- [ ] Add 5 reverse-prospecting prompt templates to CONTENT/social/posting_queue/reverse_prospecting_templates.txt
- [ ] Wire into twitter_warmup_poster.py as a weekly Sunday 10am post type
- [ ] Add cron job: 0 10 * * 0 to post one engagement prompt
- [ ] Add cron job: 0 10 * * 1 to scrape replies from Sunday post and route to INBOUND_LEADS.csv
- [ ] Score reply leads and hand off hot ones to existing outbound chain

## Tooling

```json
{
  "browser": "playwright for reply scraping",
  "email": "none",
  "content": "engagement_bait_converter.py + twitter_warmup_poster.py"
}
```
