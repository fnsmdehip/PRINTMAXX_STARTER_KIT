# Growth Plan: Rejected from YC three times, built it anyway

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (audience growth → funnel to paid products)

---

## Tactics

1. Post rejection narratives in r/SaaS, r/startups, r/Entrepreneur during peak hours (Tue/Wed 9-11am EST)
2. Quote-tweet YC rejection stories with our own build-in-public angle
3. Engagement bait: 'YC said no 3 times. Here's what $0 funding looks like at [X] MRR' — drives replies
4. Cross-post narrative variants across Reddit/Twitter/LinkedIn for 3x reach from 1 story
5. Reply to @ycombinator batch announcements with bootstrap counter-narrative

## Budget Tier Strategies

### FREE
Organic posting of rejection→success narratives across Reddit and Twitter. Reply engagement on YC-related threads. Cross-pollinate with existing printmaxxer account buildinpublic content.

### LOW
$10-20/mo boosting top-performing rejection narrative posts on Twitter/Reddit

### MID
$50-100/mo for micro-influencer seeding — pay 2-3 indie hacker accounts to QT our bootstrap stories

## Daily Actions

- [ ] Wire into existing background_reddit_scraper.py to flag posts matching 'rejected|turned down|said no' + 'built|launched|revenue' pattern in r/SaaS, r/startups
- [ ] Extract narrative template: [Authority] said no → built anyway → [metric] in [timeframe]
- [ ] Feed templates to engagement_bait_converter.py with printmaxxer voice model
- [ ] Queue 2 posts/week to CONTENT/social/posting_queue/ using rejection framework
- [ ] Any concrete SaaS methods found during scraping → route to ALPHA_STAGING for separate integration
- [ ] Track engagement rate of rejection-narrative posts vs baseline to validate template

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
