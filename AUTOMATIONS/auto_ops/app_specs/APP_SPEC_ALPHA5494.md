# App Spec: ALPHA5494
## source: r/SideProject (https://reddit.com/r/SideProject/comments/1r544g7/my_free_pdf_editor_hit_10k_downloads_in_30_days/)
## generated: 2026-02-15 14:27:58
## roi_potential: HIGH

## core insight
My free PDF editor hit 10k downloads in 30 days with 0 spent marketing. Here's what worked (and what flopped).. 
**TL;DR:** Built RevPDF - a lightweight, offline-first PDF editor. No cloud, no signup, no bloat. Free on desktop (Windows/Mac/Linux/android/ios), small one-time payment on mobile. Hit 10k downloads

## app concept
build a focused utility app around this insight. single-purpose, solves one problem well.

### target niches
faith, fitness, tech, finance

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