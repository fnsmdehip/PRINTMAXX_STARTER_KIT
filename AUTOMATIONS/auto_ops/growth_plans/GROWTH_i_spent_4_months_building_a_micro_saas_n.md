# Growth Plan: I spent 4 months building a micro SaaS nobody used. Then I s

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (improves app factory hit rate, not a direct revenue method — value is preventing wasted build cycles)

---

## Tactics

1. post problem-validation framework as content on r/micro_saas and r/SaaS for inbound
2. create thread showing our app factory kill/double-down decisions using this framework
3. use contrarian hook from procedural memory: 'I built 114 apps at $0. Here's what Marc Lou knows that I didn't.'

## Budget Tier Strategies

### FREE
Post problem-validation insights as threads on Twitter/Reddit/IndieHackers. Use our 114-apps-$0-revenue story as authentic contrarian content. Cross-post framework as engagement bait.

### LOW
$0-50/mo: Boost top-performing thread. Seed in micro SaaS Discord communities.

### MID
$50-200/mo: Sponsor a micro SaaS newsletter with our validation framework as lead magnet for app factory consulting.

## Daily Actions

- [ ] 1. Scrape top 100 revenue-confirmed micro SaaS posts from Reddit + IndieHackers for problem categories
- [ ] 2. Build problem-demand taxonomy (categories: pain frequency, willingness-to-pay signal, existing paid alternatives count, search volume proxy)
- [ ] 3. Score existing APP_FACTORY_METHODS.csv entries against taxonomy — add demand_validation_score column
- [ ] 4. Re-rank app_factory_priority_queue.json by demand score, deprioritize apps solving unvalidated problems
- [ ] 5. Feed top 3 validated problems into app_factory_autopilot for next build cycle
- [ ] 6. Generate content from the framework itself (our 114-apps story is high-engagement material)

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py for the 114-apps story angle"
}
```
