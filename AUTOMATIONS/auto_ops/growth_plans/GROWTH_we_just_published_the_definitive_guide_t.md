# Growth Plan: we just published the definitive guide to writing good prose

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-150/mo

---

## Tactics

1. Use @every guide as social proof anchor: 'Even [high-signal source] says X about AI writing' — credibility borrow
2. Build 3-tweet thread series: 'AI writes like slop by default. Here are 7 rules that fix it.' — hook on pain point
3. Create a Gumroad micro-product: AI Prose Style Checklist (PDF, $9) — 1-day build, zero cost
4. Quote-tweet the @every guide with our own angle to capture their audience spillover
5. Repurpose as LinkedIn post targeting founders who use AI for content (high intent audience)

## Budget Tier Strategies

### FREE
Publish 1 thread/week on AI writing quality. Quote-tweet high-signal accounts like @every when they cover this topic. Cross-post to LinkedIn + Reddit r/ChatGPT and r/MachineLearning.

### LOW
$0-50/mo: Boost best-performing AI writing thread ($10-20 on X Ads). Submit guide concept to ProductHunt as a free resource.

### MID
$50-200/mo: Sponsor a small newsletter slot in an AI writing niche newsletter. Bundle AI style guide with other digital products for a $29 pack.

## Daily Actions

- [ ] python3 AUTOMATIONS/engagement_bait_converter.py --input 'AI prose style guide by @every — topic: writing well with AI' --output CONTENT/social/posting_queue/
- [ ] Generate 3 tweet variants + 1 thread from the converter output
- [ ] Create stub Gumroad listing: 'AI Writing Style Checklist' — 10-rule PDF, $9 price point, wire to existing Stripe flow
- [ ] Add weekly cron: Monday 7 AM — run converter on 'AI writing quality' topic to keep content stream active
- [ ] Add KPI entry to OPS/KPI_DASHBOARD.md: track weekly AI writing thread engagement

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
