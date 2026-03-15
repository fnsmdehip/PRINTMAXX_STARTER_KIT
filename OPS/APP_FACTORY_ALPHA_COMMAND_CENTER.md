# App Factory Alpha Command Center

Generated: 2026-03-14 20:32:35

## Inputs
- ALPHA_STAGING app candidates: 3185
- APP_FACTORY_METHODS candidates: 5
- Reddit findings consumed: 6
- Existing app specs detected: 85

## Hard Gates
- No fake paywalls. Real RevenueCat or real billing path before shipping.
- No single-file HTML monolith as the final App Store build target.
- Native-feeling interactions required: haptics, offline states, privacy URL, and post-value review prompt timing.
- If an alpha item clearly upgrades an existing app, iterate that app before starting a greenfield clone.

## Top Queue
| Rank | Opportunity | Target | Score | Market | Monetization | Core Test |
|------|-------------|--------|-------|--------|--------------|-----------|
| 1 | BibleChat (Romanian 2-man studio pivot) reached $750K/mo net revenue in March 20 | PrayerLock / Scripture Streak AI layer | 179 | MEDIUM_HIGH | subscription with 7-day trial | paywall timing: after first value moment vs after onboarding prev |
| 2 | Pomodoro iOS app. Solo dev. $0 ad spend. 23 days to $300 MRR. 2.8K downloads. 4  | Vault | 133 | MEDIUM_HIGH | subscription with annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 3 | One timing change added 0.8 stars to app rating. Changed review prompt from earl | Streakr | 128 | HIGH | subscription with 7-day trial and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 4 | HabitSwipe app: 2500 users and $799 revenue in 2 months. 76 score 27 comments. R | Streakr | 127 | HIGH | subscription with 7-day trial and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 5 | Review prompt timing hack: +0.8 stars by delaying review request to value moment | PrayerLock / Scripture Streak AI layer | 125 | MEDIUM_HIGH | subscription with 7-day trial | paywall timing: after first value moment vs after onboarding prev |

## Iterate Existing Now
| Rank | Opportunity | Target | Score | Market | Monetization | Core Test |
|------|-------------|--------|-------|--------|--------------|-----------|
| 1 | BibleChat (Romanian 2-man studio pivot) reached $750K/mo net revenue in March 20 | PrayerLock / Scripture Streak AI layer | 179 | MEDIUM_HIGH | subscription with 7-day trial | paywall timing: after first value moment vs after onboarding prev |
| 2 | Pomodoro iOS app. Solo dev. $0 ad spend. 23 days to $300 MRR. 2.8K downloads. 4  | Vault | 133 | MEDIUM_HIGH | subscription with annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 3 | One timing change added 0.8 stars to app rating. Changed review prompt from earl | Streakr | 128 | HIGH | subscription with 7-day trial and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 4 | HabitSwipe app: 2500 users and $799 revenue in 2 months. 76 score 27 comments. R | Streakr | 127 | HIGH | subscription with 7-day trial and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 5 | Review prompt timing hack: +0.8 stars by delaying review request to value moment | PrayerLock / Scripture Streak AI layer | 125 | MEDIUM_HIGH | subscription with 7-day trial | paywall timing: after first value moment vs after onboarding prev |
| 6 | Habit tracker apps are printing: HabitSwipe $800 revenue, 2.5K users in 2 months | Streakr | 122 | HIGH | subscription with 7-day trial and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 7 | Minimum Viable Day concept: 307 upvotes, viral productivity framework | Streakr | 122 | HIGH | subscription with 7-day trial and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 9 | ASO HACK: Move app review prompt from day-1 to post-3day-streak → +0.8 App Store | Streakr | 117 | HIGH | subscription with 7-day trial and annual anchor | paywall timing: after first value moment vs after onboarding prev |

## Build New Now
| Rank | Opportunity | Target | Score | Market | Monetization | Core Test |
|------|-------------|--------|-------|--------|--------------|-----------|
| 8 | Free trial paywall framework: 7-day trial = 5x conversion lift (2% to 11%). Hard | NEW_BUILD | 118 | HIGH | subscription with fast time-to-value and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 11 | PDF editor product signal: 158 score, 80 comments on r/SideProject. 100% local,  | NEW_BUILD | 114 | HIGH | subscription with fast time-to-value and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 14 | Niche B2B SaaS: automated compliance reminders for dental/vet offices. Stack: Ne | NEW_BUILD | 110 | HIGH | subscription with fast time-to-value and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 20 | SaaS pricing: $9/mo = ZERO conversions. Raised to $29/mo = paying customers imme | NEW_BUILD | 104 | HIGH | subscription with fast time-to-value and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 22 | AI lowers app dev barrier → Cambrian explosion of niche apps imminent. levelsio  | NEW_BUILD | 101 | HIGH | subscription with fast time-to-value and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 28 | ChatBase $250K MRR + PDF.ai $30K MRR. Pattern: AI wrapper on existing platforms. | NEW_BUILD | 97 | HIGH | subscription with fast time-to-value and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 32 | Free trial converts 2% → 11% paid. Tested on SaaS product. Real data from r/Side | NEW_BUILD | 95 | HIGH | subscription with fast time-to-value and annual anchor | paywall timing: after first value moment vs after onboarding prev |
| 33 | Running 4 AI-driven companies from terminal via agent orchestration (auto-co-met | NEW_BUILD | 95 | HIGH | subscription with fast time-to-value and annual anchor | paywall timing: after first value moment vs after onboarding prev |

## Spec And Test
No items in this section.

## Validate First
No items in this section.

## Operating Rules
- Run `python3 AUTOMATIONS/app_factory_command_center.py --refresh` before any app-spec or build cycle.
- If the queue maps an alpha item to an existing app, ship that upgrade before greenfield work.
- Default pricing is lower-cost annual-first testing, not vanity $99 plans with no evidence.
- Affiliate links are secondary. Core retention and billing come first.
- Review prompts only fire after a real win, never in the first dead minutes of onboarding.

## Current Human Blockers
- Store account and payment rails still gate real app revenue. Queue quality is no longer the blocker.
- If App Store, Stripe, and platform auth are still missing, the system should keep ranking/specifying and avoid pretending the launch bottleneck is solved.
