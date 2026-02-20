# App Spec: ALPHA9485
## source: 2026-02-19
## generated: 2026-02-19 06:00:02
## roi_potential: https://reddit.com/r/SideProject/comments/1qyl08n/i_launched_my_first_monetized_ios_app_3_months/

## core insight
I launched my first monetized iOS app 3 months ago. Here's every mistake I made (and the numbers). Hey everyone,

wanted to quickly share of what the last 3 months looked like after launching my first "proper" iOS app [DayZen](https://apps.apple.com/us/app/dayzen-visual-time-planner/id6754326173) (a visual time-blocking tool). I built one app before purely as a learning exercise and never tried to earn from it. This time I went all in on actually monetizing. Here's what happened.

**The numbers

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