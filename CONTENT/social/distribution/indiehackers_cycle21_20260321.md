# INDIE HACKERS — Cycle 21 (2026-03-21)
# Format: builder community, honest, transparent about metrics, story-driven

---

## POST 1: Show IH — n8n vs Zapier vs Make comparison page

**Title:** Show IH: Built a free automation tool comparison page — n8n vs Zapier vs Make (2026 pricing)

**Body:**
Kept finding outdated comparison articles when I was auditing my automation stack, so I built one.

n8n-vs-zapier-vs-make.surge.sh

It's a static HTML page with:
- 2026 pricing at each tier for all three tools
- How task/operation/execution counting differs (this is where most comparisons get it wrong)
- A verdict broken down by user type (non-technical, technical, volume-sensitive)

The short version: n8n self-hosted wins on economics past ~500 tasks/month. Zapier wins on onboarding and breadth. Make is the middle ground.

Built it in about 4 hours. Static HTML, deployed to surge.sh. It's already ranking for some longtail comparison queries.

Anyone else found the comparison content gap in SaaS tools? The affiliate-driven articles are pretty bad.

---

## POST 2: Week 6 builder update — 155 sites, 6 new apps, still zero revenue

**Title:** Week 6 update: 155 live sites, 6 new habit apps, $0 revenue

**Body:**
Transparent update for the IH audience:

**Week 6 stats:**
- 155 sites live on surge.sh
- 40+ streak apps (breathwork, gratitude, water, yoga, plank, pushup + 30+ religious/niche variants)
- 9 affiliate comparison pages
- ~651 automation scripts
- Revenue: $0

**What's blocking revenue:**
1. No Stripe account wired — can't accept payments (I know, I know)
2. No Gumroad account — 16 digital products built, 0 listed
3. No Product Hunt profile — 0 launches

Every week I build more. Every week the same blockers stay.

**What I shipped this week:**
- breathwork-streak.surge.sh
- gratitude-streak.surge.sh
- water-streak.surge.sh
- n8n-vs-zapier-vs-make.surge.sh
- best-cold-email-tools.surge.sh
- best-saas-tools-solopreneurs.surge.sh

**Lesson this week:**
Building without a payment account is pure vanity metrics. Going to fix that in the next 48 hours.

Anyone else caught in the builder trap?

---

## POST 3: How I'm building 40+ habit streak apps from one template

**Title:** How I built 40+ niche habit tracking apps from one template (breathwork, gratitude, water, religious streaks)

**Body:**
The core insight: habit tracking apps all do the same thing.

1. Present a daily prompt or goal
2. Let user mark it done
3. Show a visual streak

Different skin. Different keyword. Same conversion mechanic.

**The template structure:**
- Streak counter with visual calendar heatmap
- LocalStorage persistence (no backend, no account needed)
- PWA manifest (home screen installable, offline-capable)
- One "upgrade" prompt at day 7 of any streak (optimal moment for paid conversion)

**The SEO play:**
Each app targets a specific keyword cluster.

"breathwork app free" — 1,900 searches/mo, weak competition
"gratitude journal app free" — 12,000/mo
"water tracking app no login" — 8,100/mo

All are free to use. Payment layer is: at day 7 streak, show a $2.99/mo prompt for streak backup + export.

**The portfolio math:**
If 1% of users who hit day 7 convert, and each app gets 500 MAU at day 7:
- 5 paying users/app × $2.99/mo = $15/mo/app
- 40 apps = $600/mo baseline

Small numbers but the marginal cost per new app is near zero.

Currently live: breathwork-streak.surge.sh, gratitude-streak.surge.sh, water-streak.surge.sh, and 35+ more in the streak universe.

Happy to share the template. Anyone else building niche app portfolios?

---

## POST 4: Built 23 SaaS tool comparisons — here's what I learned about affiliate content

**Title:** I built 23 SaaS tool comparison pages. Here's what I learned about affiliate content vs honest content.

**Body:**
Six months in, I've built comparison pages for ~23 categories (cold email tools, automation tools, SaaS stacks, etc.).

A few observations:

**On affiliate content:**
The existing comparison articles for most SaaS categories are genuinely terrible. Outdated pricing, sponsored placements disguised as "our testing," rankings based on affiliate commission rate.

This is an opportunity. Users Google these comparisons when they're about to spend money. If you're the honest result, you win.

**On what "honest" actually means:**
- 2026 pricing (not 2023 pricing)
- Stating when you didn't actually test something
- Giving a real verdict, not "it depends"
- Including limitations of the winners, not just the losers

**What's working:**
The pages are ranking for longtail queries within 3-4 weeks. Traffic is early but consistent.

**What's not working yet:**
Zero affiliate links active (haven't signed up for programs yet).

This is the most frustrating version of the builder trap: the SEO is working, the traffic is coming, but the monetization layer doesn't exist.

Latest comparison: best-saas-tools-solopreneurs.surge.sh

---
