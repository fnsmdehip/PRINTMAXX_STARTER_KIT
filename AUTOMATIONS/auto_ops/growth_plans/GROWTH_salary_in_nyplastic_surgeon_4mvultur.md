# Growth Plan: Salary in NY

Plastic Surgeon $4m
Vulture Capitalist $3.5m
H

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct (content format, not revenue method) — indirect value via follower growth feeding monetized accounts. Realistic: 500-2K new followers/month if posted consistently with controversy framing.

---

## Tactics

1. Controversy framing: pair surprising salary combos (Pastor $67K vs Dog Walker $92K) to trigger debate replies
2. Quote-tweet bait: end each post with 'Which surprised you most?' to drive QTs
3. Cross-niche repurpose: faith niche (pastor salary), fitness niche (Pilates instructor salary), tech niche (Head of AI salary)
4. Reply to trending salary/career tweets with our own data for algorithmic lift

## Budget Tier Strategies

### FREE
Organic posting of salary lists 2x/week, reply to trending career/salary tweets with our data, cross-post across X/LinkedIn/Reddit r/dataisbeautiful

### LOW
$10-20/mo boosting top-performing salary posts on X

### MID
$50-100/mo for carousel ads on LinkedIn targeting career-switchers

## Daily Actions

- [ ] Create dag_runner_salary_in_ny.py with 3-phase DAG: collect salary data, generate variants, queue posts
- [ ] Scrape free salary data sources (BLS.gov public API, Glassdoor estimates) for 10 US cities
- [ ] Generate 10+ post variants: city-specific, niche-specific, controversial pairings
- [ ] Route all generated posts through engagement_bait_converter.py for hook optimization
- [ ] Push to CONTENT/social/posting_queue/ for scheduled distribution
- [ ] Add weekly cron (Monday 7:30 AM) to refresh data and generate new variants
- [ ] Track engagement per post variant in CONTENT_PERFORMANCE_LOG.csv

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter.py"
}
```
