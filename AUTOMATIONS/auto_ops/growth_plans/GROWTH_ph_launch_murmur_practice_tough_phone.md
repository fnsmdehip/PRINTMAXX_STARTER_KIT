# Growth Plan: [PH LAUNCH] murmur: practice tough phone calls with AI befor

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo (ad-supported free tier + $9/mo premium with unlimited sessions)

---

## Tactics

1. Post on r/sales r/coldcalling r/sales_and_marketing with genuine value angle: 'built this after seeing murmur launch'
2. Cold email SDR managers: 'your team makes 50 calls/day — what if they practiced each one first?' (pair with chain_cold_outbound)
3. Comment on murmur's PH launch as a peer/user to get early eyeballs
4. SEO target: 'practice cold call with AI', 'AI sales call trainer', 'roleplay phone call anxiety' — low competition, high intent
5. Niche down from murmur: target one vertical (sales, therapy, job interviews) and own it

## Budget Tier Strategies

### FREE
Deploy app, post in sales subreddits, comment on murmur PH post, generate SEO landing page targeting 'AI cold call practice' keywords, add to existing PH launch monitoring scraper

### LOW
$0-50/mo: run cold email sequence via existing cold email scripts targeting 500 sales managers/SDR leads from HN/PH, boost 1 tweet per week

### MID
$50-200/mo: sponsor r/sales weekly thread, target LinkedIn sales ops job titles with cold DM, add to email warm-up sequence

## Daily Actions

- [ ] Run playwright to scrape murmur PH page: features, upvote count, top comments (what pain points resonated)
- [ ] Check MONEY_METHODS/APP_FACTORY/ for any existing call practice or voice roleplay apps to avoid duplicate
- [ ] python3 AUTOMATIONS/app_factory_command_center.py --build 'AI call practice simulator, web app, claude API roleplay, 3 scenarios: cold call / job interview / difficult conversation'
- [ ] Deploy to surge.sh: callcoach-ai.surge.sh or ai-call-practice.surge.sh
- [ ] python3 AUTOMATIONS/engagement_bait_converter.py --input 'murmur PH launch: practice phone calls with AI' --output 3 tweets + thread
- [ ] Add to chain_cold_outbound with ICP: 'sales managers with 5+ SDR teams, B2B SaaS companies'
- [ ] Add cron entry to monitor PH daily for AI voice/communication tool launches (trend signal)

## Tooling

```json
{
  "browser": "playwright (scrape murmur PH page)",
  "email": "existing cold email scripts",
  "content": "engagement_bait_converter.py",
  "app_build": "app_factory_command_center.py + claude -p as roleplay backend"
}
```
