# App Spec: ALPHA21413
## source: 2026-03-10
## generated: 2026-03-10 18:45:01
## roi_potential: https://reddit.com/r/SideProject/comments/1rmb5lt/its_so_fking_hard_to_juggle_a_95_family_and_build/

## core insight
It's so fking hard to juggle a 9-5, family, and build a SaaS I'm Eusebiu, Dev for 8+ years, a dad, a normal WFH job.

And for some reason, I decided to start building my own SaaS.

Because hey, "why work for someone else when you can work for yourself?" Lots of freedom, no boss, good money. I saw it everywhere. People hitting $10k MRR in 3 months. Looks easy from the outside.

So I started in November 2025. Built a life tracker called [loggd.life](http://loggd.life/rd/10), something I actually w

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