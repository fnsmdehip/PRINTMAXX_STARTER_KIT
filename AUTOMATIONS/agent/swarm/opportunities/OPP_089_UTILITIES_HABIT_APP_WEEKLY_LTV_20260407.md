# OPP_089: Utilities-Category iOS App (Weekly Plan, Max LTV)
**Date:** 2026-04-07 | **Score:** 8.5/10 | **Status:** QUALIFIED

## What
Build a niche Utilities app using the weekly+trial paywall configuration proven to generate the highest LTV ($49.27/yr average per user, per Adapty 2026 benchmarks). The Utilities category generates the highest 12-month LTV at $68.90 — significantly above Health ($45.10) and Productivity ($46.97). Target: a focused, one-function utility with obsessive retention.

**Best candidate niches (underserved + utility framing):**
- **Screen Time Truth**: Actual screen time audit tool — shows which apps are stealing your attention vs. your stated goals. Frames itself as a "utility" not a wellness app. Goal-setting + daily comparison report.
- **Battery Health Pro**: Deep iOS battery diagnostics, degradation forecast, charging optimization recommendations. Pure utility, no competitors with premium tier under $5/mo.
- **Focus Lock**: Hardcore website/app blocker for iOS. Existing options (Freedom, etc.) are overpriced ($7/mo+). Build leaner at $2.99/wk.

Recommended pick: **Screen Time Truth** — highest emotional hook, lowest competition in "utility + self-awareness" niche.

## Why Now
- Adapty 2026 data: Utilities LTV $68.90 (highest category), weekly plans generate 55.5% of all app revenue
- 14,700+ new subscription apps launch monthly — Utilities is LESS crowded than Health/Productivity
- Apps launched pre-2020 dominate (69% of revenue) — but weekly+trial can disrupt through LTV, not volume
- Our existing app factory pipeline (Expo + React Native + Stripe) can ship in 5-7 days
- Screen time anxiety is a documented cultural trend in 2026 — rising searches, rising media coverage

## How (This Week)
1. **App scaffold** (Day 1-2): Fork from existing app factory template (MONEY_METHODS/APP_FACTORY/builds/)
2. **Core feature** (Day 2-4): Screen Time API access via ScreenTime framework (requires Family Controls entitlement)
   - Display: daily app usage vs. user-set goal per category
   - Score: "focus score" from ratio of intentional vs. unintentional app opens
   - Report: weekly PDF summary emailed to user
3. **Paywall** (Day 4-5): Weekly $1.99 + 3-day free trial (Cal AI 14-screen onboarding)
4. **Submit** (Day 5-7): EAS Build + TestFlight + App Store submission

## Expected ROI
- Startup cost: $0 (reuses existing Expo template, Stripe already wired)
- Time to first revenue: 7-10 days (App Store review + first trial conversion)
- LTV benchmark: $68.90 per user (Utilities category average)
- Revenue at 100 paying users: $199/mo (weekly $1.99 × active weeks)
- Revenue at 500 paying users: $995/mo
- 6-month target at 1,000 downloads/mo with 5% conversion: $3,000-$5,000/mo

## Fit Score Breakdown
- Stack fit: 9/10 (Expo + React Native is our exact stack, template reuse)
- Time to first revenue: 7-10 days
- Competition: Low in Utilities sub-niche vs. Health/Fitness (which is saturated)
- Startup cost: $0 (template reuse eliminates scaffolding time)
- Moat: Weekly+trial config proven highest LTV; Screen Time API data creates retention (users want to track trends)

## First 3 Steps
1. Research iOS Screen Time API (FamilyControls entitlement) — confirm what data is accessible without MDM
2. Fork `scripture-streak` template (simplest skeleton) → rename + strip domain-specific content
3. Build `useScreenTimeData()` hook: reads daily app usage from Screen Time API, returns per-category totals

## Risk Factors
- Apple's Screen Time API has restrictions — confirm FamilyControls entitlement availability for App Store apps
- If Screen Time API access is limited: pivot to manual input (user logs their own screen time goals) — still useful, just less automated
- Utilities category requires genuine utility; avoid "feature theater"

## PRINTMAXX Synergies
- Reuses full app factory pipeline (no new tooling needed)
- Content: "I built a Screen Time app in 5 days using React Native" — high engagement for dev/productivity Twitter
- Upsell: "Focus Mode" subscription tier at $7.99/mo for power users
- Cross-sell to existing app portfolio users (NutriSnap, Scripture Streak customers)
