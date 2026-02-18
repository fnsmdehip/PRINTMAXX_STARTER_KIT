# App Spec: ALPHA5097
## source: 2026-02-14
## generated: 2026-02-15 14:15:05
## roi_potential: https://reddit.com/r/SideProject/comments/1qs3rf5/everyones_posting_10k_mrr_screenshots_i_made_24/

## core insight
Everyone's posting 10k MRR screenshots. I made 24. Here's what 30 days actually looks like. 30 days ago I had never written a line of code. Today I have 2 apps live on the App Store, 2 apps scrapped, 2 landing pages, and another idea in the works. 52 downloads. $24 in revenue.

I'm posting about it anyway because every AI thread is "built this SaaS in 3 prompts" and I sat reading all of it thinking maybe I'm just not cut for this.

Here's the real timeline:

**Days 1-3:** Copied a proven concept

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