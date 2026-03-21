# HACKER NEWS — Cycle 21 (2026-03-21)
# Format: Show HN: [title] — brief description
# Rules: honest, no marketing language, mention tech stack, be specific

---

## POST 1: n8n vs Zapier vs Make comparison

**Title:** Show HN: Free 2026 comparison of n8n, Zapier, and Make — pricing, limits, real verdict

**URL:** n8n-vs-zapier-vs-make.surge.sh

**Comment to post with it:**
Built this because every comparison article I found was either outdated (2023 pricing) or affiliate-driven.

It's a static HTML page. Covers:
- Actual 2026 pricing at each tier
- How "tasks" / "operations" / "executions" differ between platforms (this comparison is rarely done honestly)
- Where each tool wins
- A verdict based on volume + technical ability

n8n self-hosted is the clear winner on pure economics past ~500 tasks/mo but Zapier wins on breadth and onboarding quality. Make sits in the middle.

Happy to discuss — especially if anyone has data on n8n reliability at scale.

---

## POST 2: Best cold email tools comparison

**Title:** Show HN: 7 cold email tools compared — tested with real sends, honest pricing breakdown

**URL:** best-cold-email-tools.surge.sh

**Comment:**
Ran each tool for 2+ weeks with real sends to build this. Most comparison articles stop at feature lists. This one includes:

- Deliverability notes based on actual use
- Pricing at different volume tiers
- When to upgrade from $30/mo tools to $99+ tools (and when not to)
- Stack combinations that work (e.g. Apollo for prospecting + Instantly for sending)

The TLDR is that Instantly at $30/mo is the right call for most people starting cold outreach. The $99+ enterprise tools only make sense for teams running 5k+ sends/day.

---

## POST 3: Breathwork streak PWA

**Title:** Show HN: Breathwork Streak — simple PWA to build a daily breathwork habit, no account required

**URL:** breathwork-streak.surge.sh

**Comment:**
Built this after inconsistently doing breathwork for two years. The problem wasn't motivation — it was friction.

Technical notes:
- Static HTML/CSS/JS, no backend
- LocalStorage for streak state (no server, no account, no data leaving device)
- Installable to home screen as PWA
- Offline-capable via service worker
- Guided box breathing and 4-7-8 patterns built in

The streak mechanic does most of the work. Once you have a 10+ day streak, the psychological cost of breaking it is higher than the cost of 5 minutes of breathing.

No ads, no tracking, no login. Just the streak.

---

## POST 4: 23 SaaS tools ranked for solopreneurs

**Title:** Show HN: Ranked 23 SaaS tools by value for solopreneurs — real pricing, honest verdicts

**URL:** best-saas-tools-solopreneurs.surge.sh

**Comment:**
Did this after getting tired of "best tools" lists that are just affiliate pages in disguise.

Categories covered: cold email, newsletter, SEO, AI writing, design, analytics.

Ranking methodology: value per dollar at solopreneur scale (single user, under $500/mo total SaaS budget).

Controversial takes in the list:
- Ahrefs at $99/mo ranks higher than free alternatives despite the price
- Claude subscription beats GPT-4 for content automation specifically
- Two tools in the top 5 are free or under $10/mo

The list is opinionated. I used or tested everything on it.

---
