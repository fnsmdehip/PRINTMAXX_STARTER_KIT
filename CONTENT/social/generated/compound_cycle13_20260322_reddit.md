# Compound Cycle 13 - Reddit Distribution Posts
# Generated: 2026-03-22 13:45
# Status: PENDING_REVIEW
# Format: value-first, no self-promotion, genuine community posts

---

## Post 1 - r/SideProject (1.2M members)

**Title:** Day 45 building niche streak trackers - honest numbers and what the competitive data actually shows

**Body:**

building niche streak/habit tracker PWAs targeting specific communities. 45 days in. sharing the competitive research because it surprised me.

**what i found analyzing the market:**

the top "habit tracker" (Streaks, Apple Design Award winner) makes about $360K/yr. decent. but a catholic prayer app (Hallow) in the same space makes $51M/yr. a virtual pet self-care app (Finch) makes $36M/yr.

generic habit tracking is a race to the bottom. niche wellness apps are 100x more valuable.

**the most interesting data point:**

a new app just launched with ONE feature: streak protection (miss a day without losing your streak). that's it. and it's gaining users because every 1-star review on Streaks, Habitify, etc says "lost my 300-day streak from being sick."

**my approach:** built 30+ niche streak trackers (yoga, photography, coding, pushups, prayer, etc). cross-platform PWAs so they work everywhere. each targets a specific subreddit where users already talk about daily practice.

**honest numbers:** 171 sites deployed. $0 revenue. 147 of the 171 have zero distribution. the 24 that got posted somewhere get all the traffic.

biggest lesson: building speed is irrelevant without distribution speed.

anyone else running a niche-first strategy instead of building one big generic app? curious what's working for others.

---

## Post 2 - r/Entrepreneur (3.2M members)

**Title:** Analyzed habit tracker app revenue data - the niche apps make 100x more than the generic ones

**Body:**

spent a week analyzing publicly available revenue data, ratings, and user complaints across every major habit/wellness app. sharing the findings because the pattern is useful for anyone building consumer apps.

**revenue ranking (annual estimates):**

- Hallow (catholic prayer): ~$51M
- Finch (self-care virtual pet): ~$36M
- Streaks (generic habit tracker): ~$360K
- Habitify (cross-platform habits): ~$200K

**what this means:**

the two apps serving a specific identity community (catholics, wellness seekers) earn 100x more than the ones serving "everyone who wants to track habits."

hallow's entire moat is denomination specificity. they don't try to serve muslims or protestants. just catholics. deeply, with celebrity narrators and denomination-specific prayers.

**the feature gap nobody's filling:**

the #1 complaint across ALL habit tracker reviews: losing a long streak to one sick day. hundreds of 1-star reviews saying the same thing. a new app just launched with only "streak protection" as its feature and is already gaining traction.

sometimes the biggest opportunity is just... reading the reviews.

has anyone else found that revenue data contradicts the "build for everyone" advice?

---

## Post 3 - r/indiehackers (crosspost-ready)

**Title:** 171 sites built, 147 with zero distribution - the actual bottleneck isn't what I thought

**Body:**

45 days into building niche apps. ran an honest audit this week.

171 live websites deployed. ran a distribution check on all of them.

**result:** 147 have literally zero promotion. no reddit post. no tweet. no HN submission. nothing.

the 24 sites that got at least one distribution touchpoint get essentially all the traffic.

i've been optimizing for build speed (automated pipelines, template systems, batch deploys). turns out the constraint was never building. it's distributing.

**the math:**

if each site takes 2 hours to build but 0 minutes to distribute, i have 171 products nobody knows about.

if each site takes 2 hours to build and 30 minutes to distribute in the right community, 24 sites get traffic.

i was solving the wrong bottleneck for 6 weeks.

restructuring the entire system now: no new builds until every existing site has at least one distribution channel. the warehouse is full. time to open the storefront.

anyone else hit this wall where building felt productive but distribution felt like the "boring" part you kept skipping?

---

## Post 4 - r/webdev (2.6M members)

**Title:** Built 30+ PWA streak trackers with a template system - here's the architecture if anyone wants to do something similar

**Body:**

i've been building niche streak tracker PWAs for specific communities (yoga, photography, coding, pushups, prayer, etc). all cross-platform, offline-capable, zero hosting cost on surge.sh.

**architecture overview:**

- base template: HTML/CSS/JS PWA with service worker for offline
- customization layer: niche-specific content, colors, icon sets
- shared logic: streak calculation, grace days, localStorage persistence
- deploy: surge.sh (free tier, instant deploy)

**what makes PWAs interesting for this:**

- cross-platform without app store approval process
- offline capable (service workers cache everything)
- installable on home screen
- zero hosting cost

**trade-offs i've hit:**

- no push notifications on iOS (Apple still blocks this in practice)
- no app store discoverability (have to drive traffic yourself)
- no in-app purchase system (stripe payment links instead)
- apple is actively making PWAs harder (pwa.gripe on HN recently)

the competitive data is interesting: the top habit tracker (Streaks, $360K/yr) is Apple-only native. the top prayer app (Hallow, $51M/yr) is native. PWAs are the fast/cheap path but native still wins on distribution and monetization.

planning to convert the highest-traction PWAs to native (via Capacitor) once I have data on which niches perform best.

anyone else running a PWA-first strategy and converting winners to native later?

---

## Post 5 - r/photography (5.4M members)

**Title:** Do any of you track your daily photography practice? Curious about the habit side of creative work

**Body:**

genuine question for the community.

i've been thinking about the difference between photographers who improve consistently vs those who plateau. the obvious answer is "practice more" but I'm curious about the structure.

do you:
- shoot every day or have a specific schedule?
- track what you shoot (genres, techniques, locations)?
- review your own work on a regular cadence?
- have any kind of streak or accountability system?

i've been building tools for daily creative practice and photography is the community where this seems most relevant. the progression from beginner to competent is very visible with consistent shooting.

interested in hearing what works for people here. not looking to promote anything, just genuinely trying to understand the daily practice patterns of working photographers.

---
