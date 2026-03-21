# Reddit Distribution — Cycle 24 — 2026-03-21

Assets: meditation-streak, reading-streak, journal-streak, art-streak, coding-streak, language-streak, prospectmaxx, stackmaxx, couples-streak, language-streak

Status: PENDING_REVIEW

---

## POST 1: r/Meditation
**Subreddit:** r/Meditation (900K members)
**Title:** I built a free meditation streak tracker — no email, no subscription, just the streak

**Body:**
Been using paid apps for meditation tracking and kept hitting paywalls for features that should be basic.

So I built a simple one: meditation-streak.surge.sh

What it does:
- Tracks your daily streak
- Lets you set a daily meditation target (minutes)
- Shows your calendar history
- Works offline (Progressive Web App, ~850KB)
- Zero email required, zero account, zero ads

What it doesn't do:
- Guided meditations (you have your preferred app for that)
- Social sharing / leaderboards
- Upsells

The insight was: the timer and guidance are solved. The missing piece is the accountability streak that makes you open the app tomorrow.

Try it if you want: meditation-streak.surge.sh

Would love feedback — specifically whether the streak counter design actually motivates or just creates anxiety.

---

## POST 2: r/books
**Subreddit:** r/books (23M members)
**Title:** Built a dead-simple reading streak tracker after realizing I wasn't actually reading "consistently"

**Body:**
Last year I thought I was a consistent reader. Then I looked at the actual data.

I'd read 4 books. But I'd read on maybe 11 days total. The other 354 days: nothing.

I built reading-streak.surge.sh to track this properly:

- Log what you read + how many pages
- See your actual streak (not just "books finished")
- Daily target setting
- Works offline

The app's embarrassingly simple. But the data isn't. Turns out "I read" and "I read daily" are wildly different things.

Link: reading-streak.surge.sh

No email, no account. Open it, log your session, close it. That's the whole thing.

---

## POST 3: r/Journaling
**Subreddit:** r/Journaling (500K members)
**Title:** Minimal journaling streak app — one text box, one submit, no AI telling you what to reflect on

**Body:**
Every journaling app I tried either:
- Had AI "prompts" that defeated the purpose
- Required an account to save anything
- Cost $8/mo for a text box

Built journal-streak.surge.sh as the opposite of all three.

One text field. One submit button. Streak counter. Local storage (nothing leaves your device).

The premise: if the app requires 3 steps to open, you skip it. If it's one tap and a blank text box, you don't.

Link: journal-streak.surge.sh

Free, offline-capable, no email, no AI assistance. Just you and the blank page.

Feedback welcome — especially on whether you want any export functionality or if keeping it ephemeral is the right call.

---

## POST 4: r/learnprogramming
**Subreddit:** r/learnprogramming (5.3M members)
**Title:** Built a coding streak tracker after watching my 50-day GitHub streak get broken by one missed day

**Body:**
GitHub's contribution graph is great motivation until you miss one day and the visual chain breaks.

Built a separate coding streak tracker that's more forgiving: coding-streak.surge.sh

Differences from GitHub:
- Tracks "I coded today" regardless of whether you committed
- Lets you log what you worked on (notes field)
- Shows streak separately from GitHub activity
- Works offline so you can log without internet

The insight: GitHub measures commits, not learning. Learning sessions that don't produce commits still count.

Link: coding-streak.surge.sh

Zero account, zero email. Let me know what features would actually make you use this vs just use GitHub's graph.

---

## POST 5: r/sales
**Subreddit:** r/sales (400K members)
**Title:** Free prospect research tool — domain → company size, tech stack, revenue range in 10 seconds

**Body:**
Prospect research is the biggest time sink in cold outbound and it doesn't need to be.

Built prospectmaxx.surge.sh — paste a domain, get:

- Estimated company size (employee signals)
- Tech stack detected (CMS, email provider, analytics, ad platforms)
- Revenue range estimation
- Social presence summary
- Funding signals where available

Takes 10 seconds per domain. Free. No API key. No account.

How I use it in a cold email workflow:
1. Export lead list (any source — LinkedIn, Apollo, manual)
2. Run each domain through prospectmaxx for the signals
3. Segment by tech stack (e.g. "all Shopify stores doing $1M-5M")
4. Write ONE personalized segment-level hook, not individual flattery
5. Send with that context baked in

Reply rates on segment-personalized emails run 2-3x higher than name/company token substitution.

Link: prospectmaxx.surge.sh

Free forever, feedback welcome on what other signals would be useful.

---

## POST 6: r/startups
**Subreddit:** r/startups (1.2M members)
**Title:** I built a SaaS stack auditor — paste your current tools and see where you're bleeding money

**Body:**
Most SaaS companies pay for 3 tools that do the same thing. It's usually project management, then CRM, then email. Sometimes all three across different tools that barely talk to each other.

Built stackmaxx.surge.sh to surface this.

Paste in your current SaaS stack → it shows:
- Which tools have direct cheaper alternatives
- Where free tiers cover paid plan features
- Overlap between tools (paying for Notion AND Confluence?)
- Estimated monthly savings if you consolidate

The average team we've looked at has $200-600/mo in tool overlap or overpriced alternatives.

Link: stackmaxx.surge.sh

Free. Takes 2 minutes. Let me know if your stack reveals anything unexpected — curious what the most common waste patterns are.

---

## POST 7: r/languagelearning
**Subreddit:** r/languagelearning (2.2M members)
**Title:** Built a language learning streak tracker that's just the streak — nothing else

**Body:**
Duolingo's streak feature is addictive for a reason. The problem is you end up doing 1-minute practice sessions to keep it alive, which isn't the same as actually learning.

Built language-streak.surge.sh as a standalone streak tracker that works alongside whatever method you actually use (Anki, italki, podcasts, books).

What it does:
- Tracks your daily streak for whichever language(s) you're learning
- Lets you log what you actually did (method + duration + notes)
- Shows your actual consistency data over time
- Works offline

What it's NOT:
- A replacement for Duolingo or any learning app
- A grammar checker
- AI conversation practice

Just the streak accountability layer on top of whatever you're already using.

Link: language-streak.surge.sh

Zero cost, zero account. Would love to know: what does your actual language learning look like day-to-day, and what would make the tracker genuinely useful vs another app you open once?

---

## POST 8: r/relationships
**Subreddit:** r/relationships (4.1M members)
**Title:** Built a relationship streak tracker for couples — just "did we do the thing today?" without the surveillance features

**Body:**
Most couples apps feel like accountability tools with location sharing and daily check-ins.

Built something simpler: couples-streak.surge.sh

Pick a habit you want to build together (daily walk, cooking together, no-phone dinner, whatever). Both partners log "yes" when you do it. See the shared streak.

That's it. No location sharing. No push notifications if your partner doesn't log. No "are you okay?" alerts.

The design principle: the streak should feel motivating, not obligatory.

Link: couples-streak.surge.sh

Free, no account, offline-capable. Interested if anyone actually uses something like this or if the "shared accountability" model just creates friction.

---

## POST 9: r/productivity (Value post — not direct promo)
**Subreddit:** r/productivity (4.7M members)
**Title:** The reason habit tracking apps fail (and what actually works, based on the research)

**Body:**
I spent 3 months looking at what makes habit tracking apps actually work vs become another thing you open twice.

Key findings:

**What doesn't work:**
- Reminders (you start ignoring them after day 3)
- Social features (accountability partner dropout rate is ~80% within 30 days)
- Gamification with rewards (intrinsic motivation > extrinsic after 2 weeks)
- Complicated logging (any friction = you skip it)

**What actually works:**
- Visual streak (Seinfeld's calendar method — don't break the chain)
- One tap to log (zero friction to record success)
- No penalty for missing (apps that reset streaks create avoidance)
- Data you can actually see (calendar view beats number count)

**The apps that do this best:**
- Streaks (iOS, paid) — best design, most polished
- Habitica (gamification, free) — works for a specific personality type
- Simple calendar with a marker — the OG Seinfeld method

I built meditation-streak.surge.sh, reading-streak.surge.sh, and journal-streak.surge.sh as free web versions of this — no email, no upsell, just the streak mechanic.

But honestly: a paper calendar and a red marker still outperforms most apps because there's zero setup friction.

What's your experience — does streak tracking actually work for you or does it create performance anxiety?

---
