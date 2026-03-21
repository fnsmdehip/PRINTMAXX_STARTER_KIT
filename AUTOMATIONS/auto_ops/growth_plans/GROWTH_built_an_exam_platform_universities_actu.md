# Growth Plan: Built an exam platform universities actually use

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct — content engagement only, feeds follower growth → product awareness funnel

---

## Tactics

1. Use 'built X that Y actually uses' hook template for future content — institutional social proof outperforms revenue claims in engagement
2. Target edtech niche subreddits (r/learnprogramming, r/professors, r/highereducation) with this story angle for organic reach
3. Repurpose as Twitter thread: 'How I got a university to use my $0-budget tool over $50K enterprise software'

## Budget Tier Strategies

### FREE
Convert story to 3 platform posts via engagement_bait_converter.py — use the institutional validation angle as hook, no paid distribution needed

### LOW
Boost best-performing post variant ($10-20 on Twitter/X), target indie hacker and SaaS founder audiences

### MID
Not warranted at Phase 0 for LOW ROI method

## Daily Actions

- [ ] Run: python3 AUTOMATIONS/engagement_bait_converter.py --entry 'Built exam platform universities actually use' --angle 'solo_vs_institution'
- [ ] Review 3 generated posts, approve best variant to CONTENT/social/posting_queue/
- [ ] No venture creation, no cron, no DAG — single content extraction pass only

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
