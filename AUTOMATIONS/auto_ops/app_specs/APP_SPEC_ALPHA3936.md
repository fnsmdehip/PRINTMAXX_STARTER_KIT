# App Spec: ALPHA3936
## source: 2026-02-14
## generated: 2026-02-15 14:15:05
## roi_potential: https://reddit.com/r/juststart/comments/1qw1kuw/my_forgotten_side_project_outranks_zillow_for/

## core insight
My forgotten side project outranks Zillow for dozens of searches. Here's the accidental playbook **Note**: *Not promoting this side project - its not relevant for people, only the lessons are. I blurred the name and details out for this reason.*

\---

3 years ago I built a simple site for college students looking for off-campus housing for a specific area. Put it up, ported the data from an old Excel sheet the students used, sent an email blast to the landlords on the Excel doc, and largely sto

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