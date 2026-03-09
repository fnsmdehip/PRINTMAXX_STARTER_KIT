# App Spec: ALPHA_REDDIT_APP002
## source: r/AppBusiness post - FocusBuddy $300 MRR iOS app
## generated: 2026-03-09 16:07:43
## roi_potential: HIGHEST

## core insight
Localize to 20+ languages at launch. Market native SwiftUI as differentiator. Reddit posts use human narrative not product pitch (girlfriend story). Lifetime pricing at ~1x annual sub . productivity users hate subscriptions. Next step: Apple Search Ads once LTV confirmed.

## app concept
build a focused utility app around this insight. single-purpose, solves one problem well.

### target niches
productivity|focus|pomodoro|habit-tracking

### suggested name direction
- insider baseball naming. something someone in the niche would say.
- no generic "AI Helper Pro" slop. research actual top apps in the category.
- 1-2 words max. lowercase energy.

### monetization model
- freemium with 7-day trial
- $4.99/mo or $29.99/yr subscription via RevenueCat
- affiliate links to relevant physical products (supplements, books, gear)
- apple now allows external payment links. use them.

### ASO keywords (research and expand)
- extract 5-10 keywords from the insight
- check App Store search volume before committing
- long-tail beats head terms for new apps

### competitor notes
- find top 3 apps in this space
- what are they missing? what do 1-star reviews complain about?
- that gap is the product.

### implementation
- PWA first (ships fastest), wrap with Capacitor for iOS
- use aggregate design system v2 (MONEY_METHODS/APP_FACTORY/AGGREGATE_DESIGN_SYSTEM_V2.md)
- 4-screen onboarding minimum
- lighthouse score > 90 before submission

### next action
build MVP in one session. test in simulator. deploy to surge.sh. wrap for iOS.