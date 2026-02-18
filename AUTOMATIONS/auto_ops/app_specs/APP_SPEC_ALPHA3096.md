# App Spec: ALPHA3096
## source: 2026-02-14
## generated: 2026-02-15 14:15:05
## roi_potential: https://reddit.com/r/AppBusiness/comments/1r04b3j/2k_mrr_132_subs_only_tiktok_full_funnel_breakdown/

## core insight
$2K MRR. 132 subs. Only TikTok. Full funnel breakdown inside. I launched a mobile app (iOS + Android) 8 weeks ago. Solo dev. Zero ad budget. The only acquisition channel has been organic TikTok content.

Sharing the full business breakdown because I think the numbers are interesting . and because I need help figuring out where to go from here.

**The app:** AI-powered stock analysis for retail investors. Subscription model with weekly pricing + a hidden annual option.

**8-week revenue timeline:

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