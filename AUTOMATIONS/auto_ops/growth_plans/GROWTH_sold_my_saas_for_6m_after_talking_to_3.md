# Growth Plan: Sold my SaaS for $6M. After talking to 30 buyers, here's wha

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $20-100/mo

---

## Tactics

1. Tweet thread hook: '30 SaaS buyers told me what kills deals. Nobody talks about these 3 metrics' — targets indie hacker + SaaS founder audience
2. Cross-post to r/SaaS and r/indiehackers with framing: 'What I learned from 30 acquisition conversations'
3. LinkedIn version: 'Selling your SaaS? Acquirers rank customer concentration above revenue growth' — high-intent B2B audience
4. Gumroad listing: 'SaaS Exit Readiness Audit' — 10-point self-score checklist based on 30-buyer data ($29)
5. Quote-tweet the original Reddit post to capture existing thread traffic organically

## Budget Tier Strategies

### FREE
Tweet thread + Reddit cross-post + LinkedIn post + Gumroad listing creation. No ad spend. Organic reach via SaaS founder communities and quote-tweet of viral source.

### LOW
$10-30 boost on tweet thread if organic hits >50 likes within 4h. Cheap CPM on founder-adjacent audience.

### MID
$50-100 LinkedIn sponsored post targeting founders with $200K+ ARR — highest-intent buyers for the checklist product.

## Daily Actions

- [ ] python3 AUTOMATIONS/engagement_bait_converter.py --theme saas_exit --key_metrics 'customer_concentration,competitive_defensibility,founder_dependency'
- [ ] Output 3 tweet thread variants to CONTENT/social/posting_queue/
- [ ] Create DIGITAL_PRODUCTS/ready_to_sell/saas_exit_checklist/GUMROAD_LISTING.md with $29 price — this was flagged in prior memory as unconverted, execute it now
- [ ] Add LinkedIn version to posting queue (separate file, B2B framing)
- [ ] Mark ALPHA_STAGING entry INTEGRATED

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + DIGITAL_PRODUCTS pipeline"
}
```
