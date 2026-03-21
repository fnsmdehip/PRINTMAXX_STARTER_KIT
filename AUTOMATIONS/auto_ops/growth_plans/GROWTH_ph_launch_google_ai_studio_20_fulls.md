# Growth Plan: [PH LAUNCH] Google AI Studio 2.0: Full-stack vibe coding pow

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Post build thread on X: 'Built [app] in 4 hours with AI Studio 2.0 + Firebase — here's the exact stack'
2. Submit to Product Hunt as indie maker within 48h of launch
3. Add to OPS/DEPLOYMENT_URLS.md and link from MCP Marketplace page
4. Cross-post to r/SideProject, r/webdev, r/Firebase with build breakdown
5. Generate YouTube Short (Remotion) showing vibe-coding session sped up

## Budget Tier Strategies

### FREE
Build 3 apps/week with this pipeline, post build threads, submit each to PH, cross-post Reddit. AI Studio has generous free tier (1M tokens/day). Firebase Spark plan covers 10 projects free.

### LOW
$0-50/mo — Firebase Blaze plan ($5-20/mo actual usage) for apps with real traffic. Boost best PH launch post with $20 in targeted Reddit ads.

### MID
$50-200/mo — GoLogin + SOAX for multi-account PH upvote warming. $100 in Meta retargeting ads for the 1-2 apps with organic traction.

## Daily Actions

- [ ] 1. Get free Google AI Studio API key from aistudio.google.com (2 min, human action)
- [ ] 2. Add GOOGLE_AI_STUDIO_KEY to .env
- [ ] 3. Create ai_studio_firebase_app_scaffolder.py — calls Gemini 2.0 Flash to generate full app scaffold from niche_brief.json input
- [ ] 4. Wire firebase MCP calls (firebase_create_project, firebase_get_sdk_config) into scaffolder
- [ ] 5. ENHANCE chain_4day_saas_validation_vibe_coding_gemi — add Firebase auto-provisioning stage
- [ ] 6. Add cron: 0 7 * * * — daily check of app_factory_priority_queue.json, auto-scaffold top unbuilt niche
- [ ] 7. Test with one niche end-to-end before enabling cron
- [ ] 8. Route output through engagement_bait_converter.py for 3 tweets + 1 thread per build

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py",
  "llm": "Google AI Studio (Gemini 2.0 Flash, free tier API key from aistudio.google.com)",
  "backend": "Firebase MCP (firebase__firebase_create_project + firebase__firebase_get_sdk_config)",
  "deploy": "surge (existing)"
}
```
