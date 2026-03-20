# HACKER NEWS POSTS, Cycle 18 (2026-03-20)

---

## POST 1: Show HN, DeskBreak

**Title:** Show HN: DeskBreak – Screen locks until you get up (no reminders, no dismissing)

**URL:** https://deskbreak.surge.sh

**Comment to post with it:**
I built this after dismissing 10,000 desk break reminders without standing up.

The core behavior change: notifications fail because dismissing them has zero cost. When you miss the reminder, nothing happens. When you dismiss an alarm, nothing happens.

DeskBreak locks the screen. You can't interact with it until the break timer is done. The cost of not getting up is now higher than the cost of getting up.

Built as a PWA so it installs to any device. 5 seconds to set up. No account.

Technically it's a simple localStorage timer + fullscreen API call. The whole thing is under 200 lines. What's interesting is how a minimal behavior design change (cost structure) does what 100-feature apps haven't.

Happy to share the source if useful.

---

## POST 2: Show HN, AI Slop Detector

**Title:** Show HN: AI Slop Detector – Paste any text, score it for AI tells instantly

**URL:** https://ai-slop-detector.surge.sh

**Comment:**
We're at peak "AI-written but not labeled" content. Every newsletter, every blog post, every LinkedIn post.

This analyzes text for the patterns that training data made ubiquitous: em-dash overuse, "dig into," "it's worth noting," hollow phrases, fluffy transitions, and the specific cadence AI defaults to when asked to sound professional.

Not a classifier. It's a score with explanations. You see exactly which patterns fired and why.

Built it because I was writing AI-assisted content and wanted to catch my own slop before publishing. Ended up being useful for editing other people's stuff too.

It runs entirely in the browser. No API calls, no data sent anywhere.

---

## POST 3: Ask HN, Autonomous Agents Without Revenue

**Title:** Ask HN: How do you prevent autonomous AI agents from optimizing for activity instead of outcomes?

**Body:**
Built 25 Claude-based agents over the past 2 months. CEO agent, venture autonomy agents, content agents, scraper agents, a swarm brain. All running 24/7 on launchd.

45 days in. The system is genuinely impressive. 355 websites deployed, 191,000 leads scraped, 1,100+ content pieces generated, 384 alpha entries processed.

Revenue: $0.

The problem became clear this week: every agent was optimizing for metrics it could measure. Pages deployed, leads scraped, content created. Zero agents were accountable for the steps requiring human accounts I hadn't created.

The swarm_brain agent diagnosed it better than I could. It wrote: "building at 10x the rate we ship creates the illusion of progress."

It then hibernated all 25 agents.

The question I'm wrestling with: how do you define the accountability boundary for autonomous systems? Where does automation stop and human action begin, and how do you make the system aware of that boundary?

What approaches have you seen work for this?

---

## POST 4: Show HN, Comparison Pages (Invoice + Email Tools)

**Title:** Show HN: Two tool comparison pages built without affiliate bias (invoice tools + email tools)

**URLs:**
- https://invoice-tools-compared.surge.sh
- https://email-tools-compared.surge.sh

**Comment:**
Every "best invoice tool" article is either 2 years out of date or monetized by one of the tools it's recommending.

I was trying to pick tools for my own freelance setup and couldn't find anything trustworthy. So I built the comparisons myself. Tested the free tiers.

Invoice tools: 8 compared on free tier limits, transaction fees, PDF quality, client portal, recurring invoices, payment speed.

Email tools: 8 compared on deliverability, automation on free plan, landing pages, API access, sending limits.

No affiliate links on either. If they're useful I might add them later, but they're built for information first.

What tool comparison data would you want to see added?

---

## POST 5: Show HN, Fitness Streak Apps (6 new)

**Title:** Show HN: 6 free fitness streak trackers (HIIT, cycling, plank, pushup, yoga, sober) – no account required

**URLs:**
- cycling-streak-landing.surge.sh
- hiit-streak-landing.surge.sh
- plank-streak-landing.surge.sh
- pushup-streak-landing.surge.sh
- yoga-streak-landing.surge.sh
- soberstreak.surge.sh

**Comment:**
Duolingo's streak mechanic is the most effective habit loop I've encountered. The fear of breaking the streak does more than most habit coaching advice.

Built the same mechanic for 6 fitness habits. All free, no login, work offline as PWAs.

The only design choice that matters: the streak counter must be the biggest thing on the screen. Number prominence drives the emotional weight that creates the behavioral lock.

What fitness habit would you want a streak tracker for?
