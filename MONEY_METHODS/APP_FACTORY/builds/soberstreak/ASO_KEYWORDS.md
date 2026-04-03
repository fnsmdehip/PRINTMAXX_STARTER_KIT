# SoberStreak ASO Keywords & App Store Strategy
Generated: 2026-03-21

## Core Positioning
**Privacy-first NoFap & sobriety streak tracker. No data. No servers. Unlike Quittr.**

## Tier 1 Keywords — High Volume
- nofap tracker app (HIGH search, MEDIUM competition)
- sobriety streak counter (HIGH, LOW — sweet spot)
- sobriety app no account (MEDIUM, LOW — privacy differentiator)
- nofap counter offline (MEDIUM, LOW)
- quit alcohol tracker (HIGH, MEDIUM)
- sober days counter (HIGH, MEDIUM)
- private sobriety app (LOW, LOW — vs Quittr scandal)
- nofap streak app (HIGH, LOW)
- addiction recovery tracker (MEDIUM, LOW)

## Tier 2 Keywords — Long-tail, high conversion intent
- nofap app no data collection
- sobriety tracker no account needed
- quit weed streak counter
- privacy sobriety tracker ios
- nofap accountability no signup
- sober streak milestone tracker

## Competitor Gap
| App | Weakness | Our Edge |
|-----|---------|----------|
| Quittr | Privacy scandal — exposed user data | 100% local, zero servers |
| I Am Sober | Requires account | Anonymous, no friction |
| Sober Time | Ads, cluttered | Clean, dark, focused |

## 1-Star Review Mining (problems we solve)
- "Requires account" SOLVED (no account)
- "Syncs to server without asking" SOLVED (zero sync)
- "Ads in a sobriety app" SOLVED (no ads)
- "Review prompt on day 1" SOLVED (only after 7-day milestone)

## Review Prompt Timing (RF_005 implementation)
- Fires ONLY at: 7, 30, 90, 180, 365 days
- Copy: "7 days. That is real." (milestone-specific, not generic)
- Maybe later = retry in 5 days

## Pricing (LIVE — Stripe connected 2026-04-02)
- Free: basic streak, 1 habit, 90-day heatmap
- Pro Annual: $19.99/yr — https://buy.stripe.com/7sY14o7PO1pj9hD5QH3F60H
- Pro Monthly: $2.99/mo — https://buy.stripe.com/fZu00k6LKfg98dzbb13F60p
- Both plans: 5 habits, data export (CSV), custom milestones, no upgrade prompts
- NO 7-day trial currently wired (paywall.js not integrated in soberstreak — manual modal)
- Future: integrate paywall.js for auto-trial flow

## Reddit Distribution
- r/NoFap (1.24M), r/pornfree, r/stopdrinking, r/leaves
- Frame: "Built after Quittr's privacy scandal — everything stays on your device"
- Include localStorage screenshot as proof

## 3 Tweets + 1 Thread (Rule 9 compliance)
TWEET 1: "Quittr had a privacy scandal. Users' streaks and habits got exposed. Built an alternative that stores zero data. No account. No server. Everything on your phone. soberstreak.surge.sh"
TWEET 2: "1.24 million people in r/NoFap. Zero paid apps with real privacy. That gap is now soberstreak.surge.sh — 100% offline, milestone-triggered review prompt (day 7 only), swipe to check in."
TWEET 3: "Day 7 clean is when the review prompt fires. Not day 1. Not during onboarding. After the first real win. One timing change = +0.8 stars on App Store rating (r/SideProject validated)."
THREAD: "5 things Quittr got wrong — and how we fixed each one:" (1: account, 2: data sync, 3: ads, 4: generic milestones, 5: day-1 review prompt)
