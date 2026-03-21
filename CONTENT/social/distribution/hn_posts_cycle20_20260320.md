# HACKER NEWS — Cycle 20 Distribution (2026-03-20)
# Rules: HN values technical depth, honesty, lack of marketing spin.
# Show HN = you built it. Ask HN = genuine question. Share HN = interesting link.

---

## POST 1 — Show HN: SoberStreak
# Timing: Monday/Tuesday 9-11 AM EST. Front page window is 2-4 hours.
# Why this works on HN: personal story + minimal tool + technical simplicity = hacker values

**Title:** Show HN: SoberStreak – A 55KB offline-first sober day counter, no account required

**Body:**

I wanted a simple sober day tracker that didn't make me create an account, didn't send me push notifications, and worked offline.

Everything I found was either a full recovery app with community features I didn't need, or it had paywalls after 30 days.

This is a single HTML file (~55KB) deployed to surge.sh. It:
- Counts days sober
- Has a confirmation prompt before resetting (so you can't fat-finger it)
- Shows milestone unlocks at 7, 30, 60, 90, 180, 365 days
- Stores everything in localStorage — no server, no account, no sync
- Works offline after first load (service worker)

Built it for myself. Figured others might use it.

→ soberstreak.surge.sh

The source is readable if you view-source. Happy to answer questions.

---

## POST 2 — Show HN: RunningStreak
# Alternative to SoberStreak post — pick one for this cycle

**Title:** Show HN: RunningStreak – Minimal running habit tracker without Strava's complexity

**Body:**

I run to build a habit, not to analyze data. Strava tracks 15 metrics I don't care about.

What I wanted: Did I run today? What's my current streak?

Single HTML file. Offline-first (service worker + localStorage). Tap "Yes I ran today." See your streak. Get a small celebration on milestones (7, 14, 30, 60 days).

Optional goals: set how many days per week you want to run. Shows progress toward weekly goal.

No GPS. No accounts. No backend. 43KB.

→ runningstreak.surge.sh

---

## POST 3 — Ask HN: Using AI to run cold outreach at scale — what does your deliverability stack look like?

**Body:**

I've been running a system for 60 days that:
- Analyzes leads from a database of 1.45M businesses
- Scores and qualifies them against custom criteria
- Generates personalized outreach based on public signals (website tech, BBB status, review recency, seasonal relevance)
- Routes sends through Instantly with AI-generated personalization

The volume is there (17K+ qualified leads) but I'm still figuring out the deliverability piece at scale — specifically around domain warming strategy when running multiple sending domains.

Questions for anyone who's done this:
1. How many domains do you warm at once before sending live traffic?
2. Do you use the platform's built-in warmup (Instantly/Mailreach) or a separate warmup service?
3. At what daily send volume per domain do you start seeing reputation degradation?

Happy to share my qualification scoring methodology if useful to others.

---

## POST 4 — Show HN: Lead Generation Tools Compared (unaffiliated review)

**Title:** Show HN: I compared 12 lead gen tools over 60 days – honest breakdown with no affiliate links

**Body:**

Most "best lead generation tools" articles are affiliate content farms. Rankings are determined by commission rates, not tool quality.

I spent 60 days using Apollo, Instantly, Clay, Lemlist, Phantombuster, Hunter.io, ZoomInfo, Lusha, and others with real money and real outreach campaigns.

Built a comparison page with:
- Actual pricing (including hidden per-seat costs)
- Feature comparison tables
- My honest ranking by use case (high volume vs multi-channel vs budget)
- What I actually use vs what I tested and dropped

→ best-lead-generation-tools.surge.sh

The short version: Apollo + Instantly is the MVP stack for most people. Clay is high-leverage but has a real learning curve. ZoomInfo is hard to justify unless you're an enterprise.

No affiliate links. No sponsored placements. Just what I found.
