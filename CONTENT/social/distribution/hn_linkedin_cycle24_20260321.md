# HackerNews + LinkedIn Distribution — Cycle 24 — 2026-03-21

Status: PENDING_REVIEW

---

## HACKER NEWS

### Post 1: Show HN — Free habit streak tracker suite (meditation, reading, journal, coding, art)
**URL:** meditation-streak.surge.sh
**Body:**
Built 5 minimal streak tracker PWAs for the habits that don't have a good free tracker:
meditation-streak.surge.sh, reading-streak.surge.sh, journal-streak.surge.sh, coding-streak.surge.sh, art-streak.surge.sh

Each app:
- ~850KB, offline-capable PWA
- Zero email, zero account, local storage only
- One-tap logging, visual streak calendar
- No upsells

The core insight: paid apps (Headspace $70/yr, Day One $35/yr) bundle tracking with features (guided content, sync, AI). For people who already have their preferred method, they're just paying for a streak counter.

Open source if there's interest. Would appreciate feedback on UX — specifically whether the streak reset mechanic should be forgiving (grace day) or strict (Duolingo-style reset).

---

### Post 2: Show HN — Prospectmaxx: domain → company signals in 10 seconds (free, no API key)
**URL:** prospectmaxx.surge.sh
**Body:**
Paste any domain, get: tech stack, estimated employee count, revenue range signal, funding status, social presence.

Built this after doing manual prospect research for cold outreach and watching the workflow eat 3 hours per 20 prospects.

No API key, no account, no CORS issues. Runs 100% in the browser using public signals from multiple sources.

Caveats: signals are probabilistic, not definitive. Works best for B2B software companies. Employee count estimation has ±30% variance. Revenue range is based on tech stack signals + social signals, not verified data.

Would be useful to know: what signals would make this actually useful for your outbound workflow? Currently considering adding: hiring velocity (indeed/LinkedIn job posting frequency), ad spend signals, and competitor cross-reference.

---

### Post 3: Ask HN — What habit tracking app do you actually use daily and why?
**Body:**
Looking for signal on what makes a habit tracker sticky for technical users specifically.

I've built 5 simple streak trackers (meditation, reading, journal, coding, art — all free PWAs) and I'm trying to understand: is the thing that makes habit tracking work the app, the method, or something else entirely?

My hypothesis: the app matters for the first 30 days (friction reduction). After 30 days, the habit either runs on autopilot or it doesn't — the app becomes irrelevant.

Counter-hypothesis I've seen: the social/accountability layer matters more than the local streak, which is why Duolingo's leagues work and solo streak apps get abandoned.

What's your actual experience? Do you use an app or some analog system?

---

### Post 4: Show HN — Stackmaxx: SaaS stack auditor — find your tool overlap and cheaper alternatives
**URL:** stackmaxx.surge.sh
**Body:**
Paste your current SaaS tools. Get: overlap analysis, cheaper alternatives, free tier substitutes, estimated savings.

Built after helping a 6-person SaaS team audit their $4,200/mo tool spend. Found $1,100/mo in overlap (Notion + Confluence + Basecamp all active) and $600/mo in tools with free alternatives that covered their use case.

No API needed — uses a local database of 800+ SaaS tools with pricing tiers, alternative mappings, and feature overlap scores.

Known limitations: pricing data goes stale. Last updated March 2026. Enterprise custom pricing not covered. Would appreciate PRs if you spot outdated data.

---

## LINKEDIN

### Post 1: Habit tracker suite (professional angle)
**Target: HR, L&D, productivity coaches, people managers**

I built free streak trackers for 5 habits that professionals consistently struggle to maintain:

- Meditation (most cited burnout prevention habit, least consistently practiced)
- Journaling (most cited "I should do this" habit among leaders)
- Reading (most claimed, least verified)
- Coding practice (most commonly dropped by senior engineers with heavy meeting load)
- Language learning (most started, least finished)

Each app: zero friction, works offline, no account required.

The design principle: if logging takes more than 10 seconds, you'll skip it when you're tired. And you build habits on your worst days, not your best.

meditation-streak.surge.sh | reading-streak.surge.sh | journal-streak.surge.sh

---

### Post 2: Prospectmaxx (sales/BD angle)
**Target: sales leaders, SDRs, BD professionals, founders doing outbound**

The math of manual prospect research:

30 min per prospect × 40 prospects/week = 20 hours of research per week.

At a $75K SDR salary, that's $750 in salary cost per week producing research — not conversations.

Built prospectmaxx.surge.sh to cut that to 10 seconds per domain.

Paste a URL → get company signals (size, tech stack, revenue range, funding, social presence) → use that to segment and personalize at the company level, not the individual level.

Company-level personalization converts 2-3x better than first-name tokens. The research just needs to be fast enough to actually do it.

Free. No account. prospectmaxx.surge.sh

What's your current prospect research workflow? Curious how this compares to what teams are actually using.

---

### Post 3: Stackmaxx (operations/finance angle)
**Target: COOs, finance leads, operations managers, founders**

Most SaaS teams have 3 tools doing the same job.

Usually: project management (Asana + Monday + Notion). Sometimes: CRM (HubSpot + Salesforce + something someone signed up for 2 years ago). Always: communication (Slack + Teams + email + whatever the sales team uses).

Built stackmaxx.surge.sh to surface this quickly.

Paste your tool list → see overlap, cheaper alternatives, and estimated monthly savings.

The average audit surfaces $200-600/mo in either direct overlap or significantly overpriced tools where a free tier covers the actual use case.

Takes 2 minutes. Free. No account.

What's the most surprising tool redundancy you've found in your own stack?

---

### Post 4: Couples streak (values-based, authentic angle)
**Target: general professional audience — relatable relationship content**

We track every business metric religiously.

Revenue. Churn. NPS. Burn rate. Conversion rate.

Most couples don't track the one thing that actually matters for long-term wellbeing: whether they're actually spending intentional time together.

Built couples-streak.surge.sh as a shared habit tracker for couples — no location sharing, no check-ins, no surveillance. Just: did you do the thing today?

Pick a shared habit (evening walk, cooking together, no-phone dinner). Both log it. See the streak.

Simple thing. Harder than it sounds.

---
