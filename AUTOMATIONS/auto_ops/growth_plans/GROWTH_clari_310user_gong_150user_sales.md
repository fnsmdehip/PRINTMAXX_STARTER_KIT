# Growth Plan: Clari: $310/user. Gong: $150/user. Salesforce Revenue Intell

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-25/mo

---

## Tactics

1. Quote-tweet format: screenshot competitor pricing pages vs disruptor pricing — high engagement on X/LinkedIn
2. Tag relevant SaaS founders and Salesforce community accounts for organic reach
3. Repurpose pricing comparison as LinkedIn carousel (slide 1: pain, slide 2-4: price comparison, slide 5: CTA)

## Budget Tier Strategies

### FREE
Post pricing comparison threads on X/LinkedIn/Reddit r/salesforce r/saas. Tag @StratoForceAI for potential RT. Template the format for reuse across all SaaS niches we track.

### LOW
$10-20 boost best-performing pricing comparison post on LinkedIn for B2B reach

### MID
$50-100 targeted LinkedIn ads to Salesforce admins using the pricing disruption angle as lead magnet

## Daily Actions

- [ ] Log Clari/Gong/StratoForce pricing data to LEDGER/COMPETITIVE_INTEL.csv as SaaS pricing disruption signal
- [ ] Extract reusable content template: '[Incumbent] $X/user vs [Disruptor] $Y/user — same features' format
- [ ] Generate 3 pricing-comparison engagement posts via engagement_bait_converter.py using this template across tech/SaaS niche
- [ ] Generate 1 thread on 'SaaS pricing collapse' trend citing this + other examples from COMPETITIVE_INTEL
- [ ] Queue all posts to CONTENT/social/posting_queue/
- [ ] Add template to CONTENT/social/WINNING_CONTENT_STRUCTURES.md as reusable format

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
