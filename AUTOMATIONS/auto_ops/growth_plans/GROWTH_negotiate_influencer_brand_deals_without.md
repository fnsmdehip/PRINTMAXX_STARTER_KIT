# Growth Plan: Negotiate Influencer Brand Deals Without Overpaying

**Created:** 2026-03-20 13:50
**Venture:** BROKERING
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. post negotiation horror stories as engagement bait on r/Affiliatemarketing and r/influencermarketing
2. create free rate calculator landing page as lead magnet
3. reply to influencer pricing complaint threads with value-first takes linking to guide

## Budget Tier Strategies

### FREE
Post weekly threads on influencer overpaying mistakes to Twitter + Reddit. Reply to brand owners asking about influencer rates. Cross-post rate benchmarks to LinkedIn.

### LOW
$20/mo boost top-performing negotiation thread on Twitter. Seed rate card PDF in 3 niche Slack/Discord communities.

### MID
$100/mo run targeted ads to ecom brand owners searching influencer pricing keywords. Partner with micro-influencer management tool for cross-promo.

## Daily Actions

- [ ] Build influencer_rate_analyzer.py that scrapes public influencer metrics and calculates fair CPM/CPE by niche
- [ ] Generate negotiation template library (5 email scripts for different scenarios: counter-offer, bulk deal, performance-based, rev-share, flat fee)
- [ ] Package as digital product: Influencer Negotiation Kit (rate card + templates + red flag checklist)
- [ ] Add to Gumroad draft queue at $19-29 price point
- [ ] Generate 3 content threads: 'Signs you're overpaying influencers', 'The CPM formula brands don't use', 'How to counter-offer influencer rates'
- [ ] Route threads to CONTENT/social/posting_queue/ via engagement_bait_converter
- [ ] Schedule weekly cron to refresh rate benchmarks from public data

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
