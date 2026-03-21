# Growth Plan:  how to clone your competitor's entire tech stack in 60 seco

**Created:** 2026-03-20 18:09
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo direct (service), $0 indirect (better tool choices + content engagement)

---

## Tactics

1. Publish weekly 'competitor stack teardown' threads on Twitter — high engagement in indie hacker community
2. Cross-post stack analyses to r/SaaS, r/startups, r/Entrepreneur as value-first content
3. Use findings to pitch 'tech stack audit' as cold outbound service to local businesses
4. Content angle: 'I scanned 100 competitors in 60 seconds — here is what they all use' viral thread format

## Budget Tier Strategies

### FREE
BuiltWith free tier (5 lookups/day), Wappalyzer OSS npm package (unlimited local), organic content threads from scan results, cross-post to Reddit/HN/Twitter

### LOW
$0-20/mo for BuiltWith basic API if free tier rate-limited, boost top-performing stack teardown threads

### MID
$50-100/mo BuiltWith Pro API for bulk lookups, run as paid competitive intel service for clients

## Daily Actions

- [ ] Create competitor_techstack_scanner.py with BuiltWith free page scraper + Wappalyzer npm fallback
- [ ] Pull competitor domains from LEDGER/COMPETITIVE_INTEL.csv and COMPETITOR_FACTORY_MAP.csv
- [ ] For each domain: HTTP GET builtwith.com/DOMAIN public profile page, parse tech categories
- [ ] Fallback: run wappalyzer-core on domain directly for missed stacks
- [ ] Write results to LEDGER/TECH_STACK_INTEL.csv with columns: domain, category, tool, first_seen, competitor_count
- [ ] Diff against our known stack — flag tools used by 3+ competitors that we lack
- [ ] Generate Twitter thread content from top findings via engagement_bait_converter.py
- [ ] Schedule cron weekly Monday 5 AM
- [ ] Wire output into competitor_stalker swarm agent as enrichment data source

## Tooling

```json
{
  "browser": "playwright for JS-rendered stack detection fallback",
  "email": "none",
  "content": "content_factory for thread generation from scan data"
}
```
