# Growth Plan: [r/SaaS] I made $413 from 1,700 users in 3 months...here's t

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo indirect (traffic → app signups → conversions). Direct content revenue $0 but acquisition cost = $0 so ROI is infinite on any conversion.

---

## Tactics

1. Post honest numbers on r/SaaS, r/SideProject, r/IndieHackers, r/Entrepreneur — transparency posts get 3-10x engagement vs promotional posts
2. Cross-post to HN Show HN with technical angle (how we built 47 apps with Claude Code)
3. Reply to OTHER people's revenue breakdown posts with our own numbers — piggyback on existing engagement
4. Build in public Twitter thread series — weekly metrics updates create recurring audience
5. Use contrarian hooks: 'I deployed 47 apps and made $0. Here's why I'm not worried.'
6. Seed comments from warm accounts within first 30 min of posting for algorithm boost

## Budget Tier Strategies

### FREE
Organic Reddit/HN/Twitter posting with honest metrics. Reply engagement on competitor breakdown posts. Build-in-public thread series. Cross-pollinate: each platform post links to different app.

### LOW
$10-30/mo: Boost top-performing breakdown posts on Reddit via promoted posts. A/B test headlines.

### MID
$50-150/mo: Sponsor newsletter placements in IndieHackers/Bootstrapped Founder newsletters with our breakdown story as native content.

## Daily Actions

- [ ] 1. Build transparent_breakdown_generator.py that pulls real metrics from OPS/DEPLOYMENT_URLS.md (47 apps, build dates, categories)
- [ ] 2. Template library: 5 Reddit formats (honest breakdown, lessons learned, month-N update, comparison, AMA), 3 Twitter thread formats, 2 HN formats
- [ ] 3. Wire into content_factory chain — breakdown posts feed into engagement_bait_converter for hook optimization
- [ ] 4. Cron Mon/Thu 8AM: generate fresh breakdown post with latest metrics, queue to CONTENT/social/posting_queue/
- [ ] 5. Track referrer traffic from Reddit/HN to app URLs — feed back into metrics for next breakdown post (flywheel)
- [ ] 6. After 4 weeks: analyze which format/platform drives most signups, double down on winner

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter + content_repurposer"
}
```
