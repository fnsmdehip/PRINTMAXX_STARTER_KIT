# App Spec: ALPHA1475
## source: 2026-02-13
## generated: 2026-02-13 20:20:45
## roi_potential: https://reddit.com/r/Entrepreneur/comments/1r0upe7/i_fired_my_biggest_client_and_it_was_the_best/

## core insight
I fired my biggest client and it was the best business decision I ever made Last year I had a client that made up about 40% of my revenue. They were also the reason I was working 60+ hour weeks, constantly stressed, and slowly losing every other client I had.

Here's what happened and why letting them go changed everything.

**The situation:**

This client was a mid-size ecommerce brand. They paid well -- around $4,500/month. But they were absolutely brutal to work with. Scope creep on every pro

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