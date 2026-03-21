# Reddit Distribution — Cycle 22 — 2026-03-21

Assets: pushup-streak, plank-streak, yoga-streak, cycling-streak, hiit-streak, invoiceforge, promptvault, studylock, framer-vs-webflow, claude-code-vs-opencode

---

## POST 1 — r/bodyweightfitness

**Title:** Built a free pushup + plank streak tracker — no login, no account, just open and log

**Body:**
I was tired of habit apps that make you sign up, verify your email, set up a profile, and subscribe before you can log a single pushup.

So I built two apps that skip all of that:

**Pushup Streak** (pushup-streak.surge.sh) — log your daily reps, see a visual streak calendar, works offline. That's literally it.

**Plank Streak** (plank-streak.surge.sh) — daily plank timer with streak tracking.

Both are free, no ads, no signup. I built them as web apps so nothing to install either.

The philosophy: friction kills habits. The fewer steps between waking up and logging, the better.

Would love feedback from anyone who actually tries it. Still early.

---

## POST 2 — r/yoga

**Title:** Made a free yoga streak tracker — just a URL, no app install, no subscription

**Body:**
I keep seeing recommendations for $10-15/mo yoga apps when most people just need two things:
1. A reminder to practice
2. A streak to keep them honest

Built Yoga Streak (yoga-streak.surge.sh) — a web app that tracks your daily yoga streak. Works offline, no account, no paywall.

Open it. Tap "I practiced today." See your streak. That's the whole product.

I'm not trying to replace YogaGlo. I just want the thing that makes me not break my streak at day 47 because the app was complicated.

---

## POST 3 — r/cycling

**Title:** Free cycling habit tracker — streak-based, no Strava account required

**Body:**
Not a replacement for Strava — this doesn't track routes or GPS.

It's specifically for daily riding habits. Did you get on the bike today? Yes/No. Streak tracker. Visual calendar.

Built for people who want the habit consistency without the full data overhead.

cycling-streak.surge.sh — free, no signup, works on mobile browser.

---

## POST 4 — r/freelance

**Title:** I built a free invoice generator with no watermark, no signup, no subscription

**Body:**
The number of times I've Googled "free invoice generator" and ended up on a site that wants my email, credit card, and firstborn before showing me a download button.

Built this: invoiceforge.surge.sh

Fill in client name, your name, line items, payment terms. Download PDF. Done.

No watermark. No account. No free tier with 3 invoices/month.

I use it myself for freelance work. Works great on mobile too if you're logging invoices on the go.

Feedback welcome if something doesn't look right.

---

## POST 5 — r/ChatGPT (or r/LocalLLaMA)

**Title:** I keep losing my best prompts — built a free prompt vault to fix this

**Body:**
The pattern: spend 30 minutes engineering a perfect prompt. It works great. Save it in... a Notes doc somewhere. Never find it again.

Built Prompt Vault (promptvault.surge.sh) to save, tag, and search my best prompts across Claude, GPT-4, and Gemini.

Free, no login required. You can share prompts with a link.

Nothing fancy — it's basically a searchable library with tags and categories. But it's better than a Notes doc.

---

## POST 6 — r/learnprogramming

**Title:** Built a free study streak tracker for CS students — Pomodoro + subject streaks

**Body:**
r/learnprogramming has a lot of posts about staying consistent. Most recommendations are $10/mo apps.

Built Study Lock (studylock.surge.sh) — free, no account:
- Pomodoro timer built in
- Track streaks per subject (Algorithms, Math, etc.)
- See your most consistent study days on a heatmap
- Works offline

I built this for myself when I was grinding leetcode. The streak mechanic genuinely kept me honest.

No subscription, no signup. Just a URL you can bookmark.

---

## POST 7 — r/webdev or r/web_design

**Title:** Framer vs Webflow — I built in both, here's what I actually think

**Body:**
I've shipped sites in both Framer and Webflow over the past year. Here's my honest take:

**Framer:**
- Faster to build beautiful landing pages
- AI-native (generate sections in 10 seconds)
- Free tier that actually lets you publish
- Better for indie builders and SaaS landing pages

**Webflow:**
- More control over HTML/CSS (you can inspect and edit the output)
- Better for complex CMS-driven sites
- Steeper learning curve but more powerful
- $23+/mo just to publish

**My actual recommendation:**
If you're building a product landing page → Framer every time.
If you're building a client site with blog/CMS needs → Webflow.

Built a full comparison with pricing, use cases, and a feature matrix:
framer-vs-webflow.surge.sh

Open to pushback from anyone who's used them more than I have.

---

## POST 8 — r/programming

**Title:** OpenCode vs Claude Code — compared them after OpenCode hit 685 on HN today

**Body:**
OpenCode launched today (open-source AI coding agent) and hit 685 HN points. I built a comparison page after spending the morning testing both.

Short version:

**OpenCode** is better if:
- You want model flexibility (not locked to Anthropic)
- You want auditable, open-source code
- You want community contributions/forks

**Claude Code** is better if:
- You're deep in Anthropic's ecosystem (Opus models)
- You want the MCP server ecosystem
- You want deeper integration with the Anthropic API

Neither is "better" — they're targeting different priorities.

Full comparison: claude-code-vs-opencode.surge.sh

What's everyone's actual daily driver for AI-assisted coding?
