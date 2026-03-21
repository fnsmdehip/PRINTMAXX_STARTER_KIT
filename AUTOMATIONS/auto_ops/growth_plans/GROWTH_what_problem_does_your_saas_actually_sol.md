# Growth Plan: What problem does your SaaS actually solve

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo (indirect via content growth and lead magnet potential)

---

## Tactics

1. Post 'what problem does your [niche] tool solve' weekly on Twitter/LinkedIn — high engagement, positions as thought leader
2. Mine existing r/SaaS, r/indiehackers threads for answers — free product research corpus
3. Convert top answers into 'problems people actually pay to solve' thread content

## Budget Tier Strategies

### FREE
Route mined pain points through engagement_bait_converter.py → 3 posts per thread. Post weekly 'what problem does your X solve' as community bait on Twitter.

### LOW
$0-50/mo: Boost top-performing engagement post with $10-20 Twitter ads to grow replies corpus faster.

### MID
$50-200/mo: Sponsor r/SaaS post for visibility + compile pain point report as lead magnet.

## Daily Actions

- [ ] Run background_reddit_scraper.py targeting r/SaaS threads with 'what problem' in title
- [ ] Pipe top 10 answers through engagement_bait_converter.py to generate 30+ posts
- [ ] Queue to CONTENT/social/posting_queue/ for weekly drip
- [ ] Add cron: 0 7 * * 1 to refresh weekly

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
