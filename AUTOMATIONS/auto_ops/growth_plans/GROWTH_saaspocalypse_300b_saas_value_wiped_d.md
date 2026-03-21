# Growth Plan: SaaSpocalypse: $300B SaaS value wiped. Default CRUD+SEO moat

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo per successful alternative (realistic: 1-2 hit from every 10 built)

---

## Tactics

1. Post 'I replaced $X/mo SaaS with free alternative' threads on r/SaaS, r/smallbusiness, r/selfhosted — proven engagement format
2. Reply to every 'what's the cheapest alternative to X' thread with our build
3. Tweet teardown threads: 'X SaaS charges $99/mo. Here's what it actually does: [3 API calls and a database]. We built it for $0.'
4. ProductHunt launch each alternative — 'the open-source/cheap alternative to X' positioning
5. Cross-pollinate: each SaaS alternative feeds App Factory portfolio count, content pipeline, and cold outreach targets (churned users of incumbent)

## Budget Tier Strategies

### FREE
Reddit/HN/Twitter organic threads positioning against incumbent. Reply targeting on 'alternative to X' searches. App Factory builds at $0 marginal cost. SEO longtail pages: 'best [incumbent] alternative 2026'

### LOW
$0-50/mo: Boost top-performing teardown threads. Target incumbent's branded keywords with cheap Google Ads ($0.10-0.30 CPC on '[SaaS name] alternative')

### MID
$50-200/mo: Sponsor relevant newsletters. Run retargeting on landing page visitors. Micro-influencer reviews of our alternative vs incumbent

## Daily Actions

- [ ] 1. Build saas_disruptor_scanner.py: scrape G2 low-rated SaaS (>$30/mo, <3.5 stars), Reddit complaint threads (r/SaaS, r/smallbusiness), HN 'expensive SaaS' discussions
- [ ] 2. Score vulnerability index: price_gap * complaint_volume * build_simplicity * market_size. Rank weekly top 5.
- [ ] 3. For each qualified target: generate App Factory spec (core features only, 70-90% cheaper pricing, Stripe payment link)
- [ ] 4. Queue into app_factory_command_center.py for build. Landing page auto-generated with '[Incumbent] alternative' positioning.
- [ ] 5. On deploy: auto-generate content (3 tweets + 1 thread + 1 Reddit post per alternative). Route through engagement_bait_converter.py.
- [ ] 6. SEO: generate longtail pages 'best [incumbent] alternative 2026' via generate-longtail skill for each target.
- [ ] 7. Cold outreach: extract emails from G2 reviewers who gave 1-2 stars, send 'we built what you wished X did' email.
- [ ] 8. Cron weekly Monday 5 AM: re-scan for new vulnerable targets. Append to LEDGER/SAAS_DISRUPTOR_TARGETS.csv.

## Tooling

```json
{
  "browser": "playwright for G2/Capterra scraping",
  "email": "custom cold outreach to churned users found in complaint threads",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
