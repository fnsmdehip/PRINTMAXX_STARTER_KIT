# Module 5: The Portfolio System — Ship 10 Apps, Kill 8, Scale 2

## What You'll Have After This Module

A repeatable system for generating app ideas, building them in 48 hours, testing them with real users, and making data-driven decisions about which ones to kill and which ones to pour fuel on. This is how solo developers build $10K/month income streams.

## The Math That Makes This Work

Most apps fail. This isn't pessimism — it's the base rate. Out of every 10 apps you launch:

- 5-6 will get zero traction (nobody cares)
- 2-3 will get some users but won't monetize
- 1-2 will make money

If each app takes you 6 months and $5K, you can't afford to fail. But if each app takes 48 hours and $2 in API credits, you can fail 8 times and still win.

Your job is not to predict which app will work. Your job is to ship fast enough that the numbers play out in your favor.

## Phase 1: Idea Generation (The Hit List)

You need 10 app ideas. Not 10 good ideas — 10 ideas that meet three criteria:

1. **Someone is already paying for a solution.** Search the App Store, Product Hunt, or Gumroad. If nobody's paying for it, the demand doesn't exist.
2. **You can build an MVP in under 48 hours.** If it needs user accounts, real-time data, or complex algorithms, it's too complex for a first pass.
3. **The value is obvious in 10 seconds.** If you need a paragraph to explain what it does, nobody will try it.

Here are 10 proven categories with specific examples:

| # | Category | Example App | Who Pays For This |
|---|----------|-------------|-------------------|
| 1 | Habit tracking | StreakPad (you built this) | 47 paid apps on App Store, $3-$10/mo |
| 2 | Pomodoro/Focus | FocusBlock — timer + website blocker | Forest app: $4, 10M+ downloads |
| 3 | Expense splitting | SplitEasy — simpler Splitwise | Splitwise: freemium, millions of users |
| 4 | Meal planning | MealMap — weekly meal planner + grocery list | Mealime: $6/mo, 1M+ downloads |
| 5 | Invoice generator | QuickBill — freelancer invoices in 30 seconds | Invoice Ninja, Wave (millions in revenue) |
| 6 | Bookmark manager | StackMark — save + tag + search bookmarks | Raindrop.io: $3/mo, 500K users |
| 7 | Daily journaling | OneLine — one sentence per day journal | Day One: $5/mo, Apple Design Award |
| 8 | Countdown timer | EventPulse — countdowns to things you care about | Multiple apps charging $2-$5 |
| 9 | Color palette | PaletteForge — generate + save color palettes | Coolors Pro: $3/mo |
| 10 | QR code generator | QRForge — styled QR codes with logos | QR Tiger: $7/mo |

Write your hit list. 10 apps. For each one, note:
- The existing paid competitor
- What they charge
- What you'd build differently (simpler, faster, offline-first, better design)

## Phase 2: The 48-Hour Sprint

You already know how to do this from Module 2. Here's the optimized workflow:

**Hours 0-4: Build the core loop.**

The core loop is the one thing your app does. For a habit tracker, it's: add habit, check it off, see streak. Everything else is decoration.

Tell Claude Code exactly what the core loop is. Don't describe features — describe the sequence of user actions.

**Hours 4-8: Add the paywall and polish.**

Apply one of the paywall strategies from Module 4. Add OG tags for sharing. Polish the UI with the prompts from Module 2.

**Hours 8-10: Deploy and create landing context.**

Deploy to Surge/Netlify. Write a one-paragraph description. Take 3 screenshots (mobile). You're ready to show it to people.

**Hours 10-48: Get 20 people to try it.**

This is the hard part. Not because it's technically difficult, but because most builders hide behind "it's not ready yet." It's ready. Ship it.

Where to find 20 testers:
- Reddit: Find the subreddit for your app's category. r/productivity, r/freelance, r/cooking, r/webdev. Post a Show HN-style post: "I built X in a weekend, looking for feedback."
- Twitter: Post a 30-second screen recording. Tag relevant accounts.
- Discord: Most niches have Discord servers. Search Disboard.org. Join and share in the appropriate channel.
- Indie Hackers: Post in the "Show IH" section. This audience specifically wants to see what you built.

## Phase 3: The Kill/Scale Decision (Day 7)

After 7 days, you have data. Here's how to read it:

### Kill Triggers (stop working on this app immediately)

- **Zero organic traffic after sharing in 5+ places.** If people saw it and didn't click, the idea doesn't resonate.
- **High bounce rate (>80%) with >50 visitors.** People clicked but left immediately. The value proposition failed.
- **Zero repeat usage.** People tried it once and never came back. The core loop isn't sticky.
- **Negative feedback about the concept, not the execution.** "I wouldn't use this" is different from "this is buggy." The first is a kill signal. The second is a fix signal.

When you kill an app, don't delete it. Archive it. You might cannibalize the code later, or the market might shift.

### Double-Down Triggers (pour fuel on this app)

- **Repeat usage without prompting.** If people come back without you reminding them, you've hit something.
- **Unprompted sharing.** Someone shared your app with someone else. This is the strongest signal.
- **Feature requests.** People wanting MORE from your app means the core value is right and they want to go deeper.
- **Any payment.** Someone gave you money. Even $3. That's validation that can't be faked.
- **"How do I get my data back?"** Someone asking about data portability means they've put real data into your app. They're invested.

### The Conversation You Have With Yourself

```
App: StreakPad
Users (7 days): 43
Return users: 12 (28%)
Feature requests: 4
Revenue: $0
Shares: 2

Verdict: DOUBLE DOWN.
Why: 28% return rate is exceptional for a free tool.
     Feature requests signal engagement.
     Next step: Add the paywall (Strategy 1, freemium).
     Timeline: This weekend.
```

```
App: QRForge
Users (7 days): 67
Return users: 3 (4%)
Feature requests: 0
Revenue: $0
Shares: 0

Verdict: KILL.
Why: High traffic, near-zero retention.
     QR codes are a one-time use tool — wrong model for recurring.
     Not worth competing with free QR generators.
     Archive and move on.
```

## Phase 4: Scaling What Works

You've killed 8 apps and found 2 with traction. Now what?

### Week 2-4: Feature Depth

Add the features people asked for. Every feature should take less than 4 hours to build. If it takes longer, break it into smaller pieces.

Priority order:
1. Features that increase retention (keep people coming back)
2. Features that justify the price (make the paywall feel fair)
3. Features that reduce churn (keep paying users from leaving)

Features that DON'T matter at this stage:
- Social features (sharing, profiles, friends)
- Design system overhauls
- Performance optimization (unless the app is literally slow)
- Multi-language support

### Month 2: Distribution

Your app works and people pay for it. Now get more people.

**SEO (free, slow):** Create a landing page with proper H1, H2, meta description. Target long-tail keywords like "free habit tracker app no account" or "simple invoice generator freelancers." Use Ubersuggest (free plan) to find keywords with >100 monthly searches and <30 difficulty.

**Content (free, medium speed):** Write 3-5 blog posts answering questions your target users search for. "How to build a daily habit routine" → links to your habit tracker. "How to invoice clients as a freelancer" → links to your invoice tool. Host the blog on the same domain.

**Product Hunt (free, fast spike):** Launch on Product Hunt on a Tuesday or Wednesday. Prepare screenshots, a 1-minute demo video, and a compelling tagline. Aim for top 5 of the day. One good PH launch can drive 1,000-5,000 users in a week.

**Paid ads (not yet):** Don't run ads until your conversion rate is stable and your LTV is clear. If you're converting 3% of visitors at $5/month with 4-month average retention, your LTV is $20. You can afford to spend $5-$8 per user acquisition. Not before.

### Month 3+: The Compound Effect

If you ship 10 apps every quarter:
- Quarter 1: 10 shipped, 2 survive = 2 revenue streams
- Quarter 2: 10 more shipped, 2 survive = 4 revenue streams
- Quarter 3: 10 more, 2 survive = 6 revenue streams

Each surviving app might make $200-$2,000/month. With 6 apps at an average of $500/month, you're at $3K/month from a portfolio of simple tools that each took 48 hours to build.

The apps that hit $1K/month get a second developer (you hire a freelancer on Upwork for $15/hr to add features while you keep shipping new ones).

## The Portfolio Tracker

Track your apps in a simple spreadsheet:

| App | Launch Date | Status | Users (7d) | Return Rate | MRR | Decision |
|-----|------------|--------|------------|-------------|-----|----------|
| StreakPad | Mar 1 | Active | 43 | 28% | $47 | SCALE |
| QRForge | Mar 8 | Killed | 67 | 4% | $0 | ARCHIVED |
| FocusBlock | Mar 15 | Testing | - | - | - | PENDING |

Update weekly. The data makes the decisions, not your emotions. If an app isn't performing after 14 days, kill it no matter how much you like the idea.

## The One Rule

Ship speed is your only competitive advantage. Funded teams have more resources, better designers, bigger networks. But they can't ship 10 apps in a quarter. They'll spend that quarter in planning meetings debating the color of the signup button.

You ship today. You learn tomorrow. You scale next week. That's the whole system.
