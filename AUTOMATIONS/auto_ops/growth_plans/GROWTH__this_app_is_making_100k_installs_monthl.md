# Growth Plan:  this app is making 100k installs monthly and an mrr of $400

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $500-3000/mo

---

## Tactics

1. TikTok/Reels: 'What's your REAL fitness level?' quiz bait videos driving app installs
2. ASO: target '[niche] quiz' and '[niche] test' keywords — high intent, low competition
3. Reddit: post quiz results screenshots in r/fitness, r/GetDisciplined as organic seeding
4. Cross-pollinate: every streak app user gets quiz CTA, quiz completers see other streak apps
5. Engagement loop: weekly leaderboard email showing rank drop to re-engage churned users

## Budget Tier Strategies

### FREE
Quiz bait content on TikTok/Reels/Shorts (what level are you?), Reddit organic seeding of quiz results, ASO optimization for quiz/test keywords, cross-promote quiz across all 47 live apps

### LOW
$20-50/mo: Boost top-performing quiz bait videos on TikTok/IG, Apple Search Ads on '[niche] quiz' keywords at $0.30 CPI

### MID
$50-200/mo: UGC creators filming themselves taking the quiz (reaction content), retargeting quiz abandoners with paywall-skip offer

## Daily Actions

- [ ] Build reusable quiz component (5-7 questions, scoring algorithm, peer comparison chart) as shared module for app factory
- [ ] Build gamification points module (daily streak points, quiz completion bonus, achievement badges, level progression)
- [ ] Build soft paywall component triggered after first points earned (14-day free trial, Stripe checkout, no-commitment copy)
- [ ] Retrofit top 10 highest-traffic apps with quiz onboarding → gamification → paywall flow
- [ ] Create quiz bait content templates for TikTok/Reels (what level are you? screen recordings)
- [ ] Deploy updated apps, set up Firebase Analytics events for funnel tracking (quiz_start, quiz_complete, points_earned, paywall_shown, trial_started, converted)
- [ ] A/B test paywall timing: after first points vs after 3-day streak vs after reaching level 2
- [ ] Weekly cron reviews conversion funnel, flags apps with <5% quiz-to-trial rate for copy optimization

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for quiz bait videos"
}
```
