# Growth Plan: built my MVP in 5 hours and got to $10k MRR in two months

**Created:** 2026-03-20 13:50
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $500-3000/mo

---

## Tactics

1. Post Show HN with the exact pain point thread as origin story
2. Reply to original complaint threads with free tool link
3. Cross-post build story to r/SideProject r/indiehackers
4. Generate 3 tweets per MVP build (hook: 'built this in 5 hours because someone on HN complained')
5. Offer free tier, gate premium features behind $9-29/mo

## Budget Tier Strategies

### FREE
Reply marketing in original pain-point threads, Show HN posts, Twitter build-in-public threads, cross-post to r/SideProject and r/indiehackers. Engagement warm existing printmaxxer account with indie hacker community.

### LOW
$20-50/mo on targeted Reddit ads in niche subreddits where pain point was found. Boost best-performing Show HN posts.

### MID
$50-200/mo on micro-influencer seeding — pay 2-3 indie hacker accounts to try and review the tool. AppSumo lifetime deal listing.

## Daily Actions

- [ ] 1. Create dag_runner_rapid_mvp_factory.py with 4-phase DAG: scan → qualify → build → validate
- [ ] 2. Wire HN and Reddit scrapers to feed pain-point opportunities into ALPHA_STAGING tagged MVP_OPPORTUNITY
- [ ] 3. Add scoring logic: 10+ upvotes on complaint, no existing free tool, buildable in <5hrs with templates
- [ ] 4. Reuse app_factory_autopilot.py scaffold pipeline for rapid MVP generation
- [ ] 5. Deploy each MVP to surge.sh with unique subdomain, add to DEPLOYMENT_URLS.md
- [ ] 6. Cold outreach script sends free-tool notification to original thread participants
- [ ] 7. Track week-1 metrics: signups, usage, willingness-to-pay signals
- [ ] 8. Feed build narrative to engagement_bait_converter.py for 3 tweets + 1 thread per build
- [ ] 9. Weekly cron (Monday 7AM) triggers new cycle: scan → build → validate → content
- [ ] 10. Wire to existing chain_built_a_saas_over_13_years_70_clients_ for SaaS-specific learnings

## Tooling

```json
{
  "browser": "playwright for scraping pain points",
  "email": "custom cold email script for validation outreach",
  "content": "content_factory + engagement_bait_converter for build-in-public posts"
}
```
