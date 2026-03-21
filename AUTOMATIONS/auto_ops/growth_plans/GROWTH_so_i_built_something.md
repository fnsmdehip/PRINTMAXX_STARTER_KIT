# Growth Plan: So I built something

**Created:** 2026-03-20 13:50
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Post build threads on r/MicroSaas and r/SideProject for organic distribution
2. Cross-post validated builds to Indie Hackers and HN Show
3. Content repurpose each build into 3 tweets + 1 thread per Rule 9

## Budget Tier Strategies

### FREE
Post build reports on r/MicroSaas, r/SideProject, IndieHackers. Engage in comments of similar build posts. Cross-pollinate with existing app factory launches.

### LOW
$10-30/mo: Boost top-performing build thread on Twitter. Product Hunt launch for best candidate.

### MID
$50-100/mo: Micro-influencer seeding — pay 2-3 indie hacker accounts to share the tool.

## Daily Actions

- [ ] Wire r/MicroSaas into background_reddit_scraper.py weekly scan (already scrapes Reddit, add this sub)
- [ ] Filter for posts with revenue proof or user validation signals (comments, upvotes > 50)
- [ ] Cross-reference extracted pain points against app_factory_priority_queue.json to avoid duplicates
- [ ] For novel gaps: create app factory entry with landing page using existing template pipeline
- [ ] Route build report content to engagement_bait_converter.py for social distribution

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory"
}
```
