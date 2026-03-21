# Growth Plan: [r/SaaS] I’ve been talking to SaaS founders for weeks. Every

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo

---

## Tactics

1. Use curiosity-gap hook ('Everyone says the same thing') to drive comments — withhold the insight until comment threshold met
2. Repurpose across Twitter thread, LinkedIn post, and r/SaaS weekly
3. Collect replies as new alpha — founder comments = free market research

## Budget Tier Strategies

### FREE
Post synthesized pain point hooks weekly using existing alpha data via engagement_bait_converter.py → posting_queue

### LOW
Boost top-performing post with $10-20 Twitter promotion to SaaS audience

### MID
Not warranted for this method at current phase

## Daily Actions

- [ ] Run engagement_bait_converter.py on this entry to generate 3 hook-style posts using the 'I talked to X founders' template
- [ ] Pull top 5 SaaS pain points from alpha_query.py --venture CONTENT to populate the insight
- [ ] Append output to CONTENT/social/posting_queue/
- [ ] Schedule weekly cron to regenerate with fresh pain points from alpha corpus

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
