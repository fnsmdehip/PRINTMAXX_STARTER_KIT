# App Spec: ALPHA1773995827
## source: 2026-03-21
## generated: 2026-03-22 22:53:00
## roi_potential: https://reddit.com/r/passive_income/comments/1rmcm56/2k_users_800_with_a_habit_tracker_i_cant_explain/

## core insight
2k users, $800 with a Habit Tracker - I can't explain how good this feels App name - [HabitSwipe](http://www.habitswipe.app) 
Platform - Android &amp; iOS
Number of users - 2500
Total Revenue in last 2 months - $799
Total Reviews - 120 
**Story**
I've crossed 2k installs. It might sound a small number but the journey from to idea to \~2500 users is just incredible. 
I built this app for my personal use, a very minimalist 2 screen app, but the reddit community has showed soo much love to

## execution route
- route: ITERATE_EXISTING_FIRST
- portfolio target: Streakr
- cluster: habits
- if this maps cleanly to an existing app, upgrade that app before greenfield work

## market thesis
- target niches: reddit
- build a focused app around this insight. one painful problem, one obvious promise.
- use live category leaders as the quality bar, not current internal PWA quality.
- if the product cannot produce a clear first win inside 60 seconds, the concept is too broad.

## concept direction
reddit

### suggested name direction
- insider baseball naming. something someone in the niche would say.
- no generic "AI Helper Pro" slop. research actual top apps in the category.
- 1-2 words max. lowercase energy.

### monetization model
- primary: subscription with 7-day trial and annual anchor
- secondary: light affiliate add-ons only if they reinforce the streak outcome
- first price test: $24.99 to $39.99/yr first test
- use RevenueCat or a real billing path. no fake localStorage subscriptions.

### onboarding model
- goal picker -> starter pack -> first completion -> reminder permission -> paywall
- paywall placement: after first completion, show streak preview and annual plan
- review prompt timing: ask only after a real value moment or streak milestone

### visual direction
- warm ivory, emerald progress rings, satisfying completion states
- pull color and motion patterns from MONEY_METHODS/APP_FACTORY/AGGREGATE_DESIGN_SYSTEM.md
- study top category competitors before finalizing visuals

### monetization and onboarding experiments
- paywall timing: after first value moment vs after onboarding preview
- pricing: annual-first anchor vs cheaper monthly plan
- review prompt: milestone trigger only, never a day-one pop-up
- onboarding length: 3-screen fast path vs 5-screen personalized path

### ASO keywords (research and expand)
- extract 5-10 keywords from the insight
- check App Store search volume before committing
- long-tail beats head terms for new apps

### competitor notes
- find top 3 apps in this space
- what are they missing? what do 1-star reviews complain about?
- that gap is the product.

### implementation
- do not ship another single-file HTML monolith
- use App Factory standards from:
 - MONEY_METHODS/APP_FACTORY/APP_FACTORY_CENTRAL_INDEX.md
 - MONEY_METHODS/APP_FACTORY/APP_DISCOVERY_ENGINE.md
 - MONEY_METHODS/APP_FACTORY/ONBOARDING_PLAYBOOK.md
- required before App Store submission: native-feeling interactions, haptics, privacy URL, real billing, real review-prompt timing
- PWA can be a prototype, not the final quality bar
- lighthouse score > 90 before submission

### next action
1. refresh the ranked queue: `python3 AUTOMATIONS/app_factory_command_center.py --refresh`
2. confirm whether this should upgrade `Streakr` or become a new app
3. build the narrowest version that creates a real first win and supports monetization testing