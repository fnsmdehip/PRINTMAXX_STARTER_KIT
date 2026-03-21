# Growth Plan: [r/SaaS] I built 4 products in 18 months. Zero paying custom

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct — indirect credibility driver that improves conversion rates on app launches

---

## Tactics

1. Template the failure-arc narrative for every PRINTMAXX app launch: '47 apps, $0 revenue, here is what I learned'
2. Vulnerability marketing outperforms hype on r/SaaS and HN — lead with real failure stats, not aspirational numbers
3. Use authentic failure posts as credibility anchors before pitching any tool or service in the same thread

## Budget Tier Strategies

### FREE
Repurpose the 'N products, 0 customers, so I built X' structure for each app factory launch on Twitter, r/SaaS, and HN ShowHN. Authenticity of stated failure metrics drives organic upvotes and trust.

### LOW
$5-10 boost per failure arc post targeted at SaaS/indie hacker audiences to seed engagement before organic spread

### MID
A/B test failure framing vs success framing on identical product — measure which drives more signup conversions over 30 days

## Daily Actions

- [ ] Run: python3 AUTOMATIONS/engagement_bait_converter.py --method 'failure-to-pivot narrative arc: built N products, zero customers, then built the solution'
- [ ] Generate 3 posts using template: 'I built [N] [things] in [time]. [Painful zero result]. So I built [solution].'
- [ ] Save template to CONTENT/social/templates/failure_arc_template.txt for reuse on every app launch
- [ ] No new script, no new DAG, no new venture — one converter call, one saved template

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
