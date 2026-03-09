# App Spec: ALPHA_REDDIT_0309_006
## source: reddit_scrape_20260309
## generated: 2026-03-09 16:07:43
## roi_potential: MEDIUM

## core insight
Bad habit tracking app Ban It. User discovered unexpected use case = PMF signal. 124 upvotes validates interest. Study the unexpected use case for product pivot insights.

## app concept
build a focused utility app around this insight. single-purpose, solves one problem well.

### target niches
habit-tracker,ios,behavior-change

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