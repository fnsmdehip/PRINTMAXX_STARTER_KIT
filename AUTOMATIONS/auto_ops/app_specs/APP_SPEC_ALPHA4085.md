# App Spec: ALPHA4085
## source: 2026-02-14
## generated: 2026-02-15 14:15:05
## roi_potential: https://reddit.com/r/coldemail/comments/1qttl53/these_outbound_sales_mistakes_are_killing_your/

## core insight
These outbound sales mistakes are killing your reply rate I recently read a solid breakdown of the most common outbound mistakes and realized how many of us are probably tripping over the same issues without knowing it. Thought I’d share a quick, practical list so you can audit your outreach and start getting better results.

Sharing a condensed version here so it’s easy to audit your own outreach:

* Targeting the wrong accounts On paper they fit the ICP. In reality, they had no real reason to

## app concept
build a focused utility app around this insight. single-purpose, solves one problem well.

### target niches
reddit

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