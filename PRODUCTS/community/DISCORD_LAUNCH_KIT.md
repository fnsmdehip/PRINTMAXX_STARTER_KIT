# Discord Launch Kit: PRINTMAXX Community Server

**Setup time: 90 minutes** | **Revenue: $29/mo (hustler) + $99/mo (inner circle)**

---

## Server name

PRINTMAXX HQ

## Server description

the server where people actually make money. no gurus. no courses about courses. just builders sharing what works, what doesn't, and what's printing right now.

## Server icon

Use `MEDIA/generated_images/twitter_pfp.png` (the PRINTMAXX logo). If unavailable, white text "PM" on black background, 512x512px.

## Server banner

Use `MEDIA/generated_images/twitter_banner.png`. If unavailable, dark gradient with "PRINTMAXX HQ" in bold white, 960x540px.

---

## Channel structure (18 channels, 5 categories)

### Category: START HERE
| Channel | Purpose | Permissions |
|---------|---------|-------------|
| `#rules` | Read-only. Server rules + expectations. | Everyone reads, only admin posts |
| `#start-here` | Welcome flow. What this server is, what to do first. | Everyone reads, only admin posts |
| `#introductions` | New members post what they're building + current MRR | Everyone posts |
| `#roles` | React-to-claim roles (builder, designer, marketer, dev) | Everyone reacts |

### Category: FREE ZONE
| Channel | Purpose | Permissions |
|---------|---------|-------------|
| `#general` | Main chat. Daily conversation. | Everyone |
| `#wins` | Revenue screenshots, milestones, launches | Everyone |
| `#roast-my-landing-page` | Post your page, get brutally honest feedback | Everyone |
| `#tools-and-deals` | Tool recommendations, lifetime deals, discounts | Everyone |
| `#content-drops` | Daily alpha drops from PRINTMAXX team (auto-posted) | Admin posts, everyone reads |
| `#opportunities` | Job leads, freelance gigs, partnership asks | Everyone |

### Category: HUSTLER TIER ($29/mo)
| Channel | Purpose | Permissions |
|---------|---------|-------------|
| `#paid-alpha` | Daily actionable intel. Revenue methods, tested tactics. | Hustler + Inner Circle |
| `#accountability` | Weekly check-ins. Post your numbers or get called out. | Hustler + Inner Circle |
| `#swipe-file` | Proven templates: emails, landing pages, ad copy | Hustler + Inner Circle |
| `#ask-anything` | Direct questions. Guaranteed response within 24h. | Hustler + Inner Circle |

### Category: INNER CIRCLE ($99/mo)
| Channel | Purpose | Permissions |
|---------|---------|-------------|
| `#inner-circle` | High-level strategy. Revenue breakdowns. Real numbers. | Inner Circle only |
| `#1on1-booking` | Book monthly 1-on-1 calls | Inner Circle only |
| `#deal-flow` | Acquisition targets, partnership opps, revenue share deals | Inner Circle only |

### Category: META
| Channel | Purpose | Permissions |
|---------|---------|-------------|
| `#feedback` | Server improvement suggestions | Everyone |

---

## Role hierarchy

Set up in this exact order (top = highest priority):

| Role | Color | Permissions | How to get it |
|------|-------|-------------|---------------|
| `@admin` | Red (#FF0000) | Full admin | Manual assignment |
| `@moderator` | Orange (#FF8C00) | Manage messages, kick, timeout | Manual assignment |
| `@inner-circle` | Gold (#FFD700) | Access to all paid channels | $99/mo subscription |
| `@hustler` | Green (#00FF88) | Access to hustler tier channels | $29/mo subscription |
| `@og` | Purple (#8B5CF6) | Cosmetic. First 100 members. | Auto-assigned to first 100 joins |
| `@verified-builder` | Blue (#3B82F6) | Cosmetic. Proved $1K+ MRR | Post proof in #wins, mod verifies |
| `@member` | Gray (#9CA3AF) | Basic access, free channels only | Default on join |

**Subscription setup:** Use Whop, Launchpass, or Discord's native subscriptions (Server Settings > Monetization > Subscriptions). Connect Stripe. Create two tiers matching the roles above.

---

## Welcome message sequence (3 messages)

### Message 1: Immediate (on join, in #start-here)

```
welcome to printmaxx hq.

this is where builders share what actually works. no courses about courses. no "just be consistent" advice. real tactics, real numbers, real results.

here's what to do right now:

1. go to #introductions and post what you're building + your current MRR (even if it's $0. especially if it's $0.)
2. go to #roles and grab your skill tags
3. read #rules (takes 60 seconds)
4. check #content-drops for today's alpha

the free channels have more signal than most paid communities. the paid tiers ($29 and $99) are for people who want the unfair advantage.

see you in the chat.
```

### Message 2: DM after 5 minutes (via MEE6 or Carl-bot)

```
hey, quick orientation:

the most valuable channels:
- #wins -- see what other members are building/earning
- #roast-my-landing-page -- post yours, get honest feedback
- #content-drops -- daily alpha from the printmaxx pipeline (14,000+ intel entries and growing)

if you want the paid alpha, tested templates, and accountability:
- hustler tier: $29/mo -- daily tactics, swipe files, weekly accountability
- inner circle: $99/mo -- strategy calls, deal flow, 1-on-1 booking

no pressure. the free zone alone has more value than most $50/mo communities.
```

### Message 3: DM after 48 hours (via bot)

```
been here 48 hours. quick check:

did you post in #introductions yet? members who intro get 3x more engagement.

did you check #content-drops? there's been [X] alpha drops since you joined.

one thing that separates members who get value from members who lurk: they post their work. even if it's rough. even if they're at $0.

the roast channel exists because feedback from builders > feedback from friends who don't want to hurt your feelings.

post something today. doesn't have to be perfect.
```

---

## Bot setup

### MEE6 (free tier is enough to start)

1. Go to mee6.xyz, add to server
2. **Welcome plugin:** Enable. Set welcome channel to #start-here. Use Message 1 template above.
3. **Auto-role:** Assign @member on join
4. **Leveling:** Enable XP system. Members level up by chatting. Cosmetic only.
   - Level 5: Unlock custom nickname color
   - Level 10: Unlock image posting in #general
   - Level 20: "Regular" role badge
5. **Moderation:** Enable anti-spam, anti-link (except in #tools-and-deals and #opportunities)

### Carl-bot (free, handles reaction roles)

1. Go to carl.gg, add to server
2. **Reaction roles:** Set up in #roles channel:
   - React with hammer emoji = @builder role
   - React with paintbrush = @designer role
   - React with chart = @marketer role
   - React with keyboard = @dev role
3. **Auto-mod:** Duplicate protection (catches spam), word filter for slurs
4. **Timed messages:** Set up Message 2 (5 min delay DM) and Message 3 (48h delay DM)

### Optional: Whop bot or Launchpass

For paid role automation. When someone subscribes:
- Whop: Auto-assigns @hustler or @inner-circle role. Removes on cancel.
- Launchpass: Same. launchpass.com. Connects Stripe directly.
- Native Discord Subscriptions: If available in your region, simplest option. No external tool needed.

---

## Rules and guidelines

Post this in #rules (read-only channel):

```
PRINTMAXX HQ RULES

1. post what you're building. lurking is allowed but builders get priority.

2. share real numbers. "$X MRR" or "0 revenue" -- both are fine. fake screenshots get banned.

3. give feedback that's actually useful. "looks good" is useless. "your headline is vague, try leading with the result" is useful.

4. no guru energy. if your advice is "just be consistent" or "provide value," you're not providing value.

5. no pitching in general chat. you have a product? cool. put it in #opportunities with context on what it does and who it's for. cold DMing members = ban.

6. no politics, no drama, no personal attacks. disagree with ideas, not people.

7. paid channel content stays in paid channels. screenshotting and sharing hustler/inner-circle content = permanent ban + blacklist.

8. one self-promo per week max (in #opportunities only). must include: what it is, who it's for, price, link.

9. ask specific questions. "how do I make money online?" is not a question. "how do I get my first 3 cold email replies for a web design service targeting dentists?" is a question.

10. have fun. this is supposed to be the best part of your day. if it's not, tell us why in #feedback.

breaking rules 2, 5, or 7 = instant ban. everything else gets a warning first.
```

---

## Content calendar: first 30 days

Format: `Day X | Channel | Content type | Topic`

### Week 1: Foundation

| Day | Channel | Type | Topic |
|-----|---------|------|-------|
| 1 | #content-drops | Alpha drop | "5 tools that replaced my $2,000/mo SaaS stack for $47/mo total" |
| 1 | #general | Discussion prompt | "what's your current MRR? reply with the real number. no judgment." |
| 2 | #content-drops | Framework | "the 3-email cold outreach sequence that books 10 calls/week ($37/mo total cost)" |
| 2 | #roast-my-landing-page | Example roast | Admin posts their own landing page, does a self-roast to set the tone |
| 3 | #content-drops | Tool breakdown | "I tested 8 AI writing tools for cold email. here's the only one that doesn't get spam-flagged." |
| 3 | #wins | Seed content | Admin posts a real revenue screenshot + breakdown |
| 4 | #content-drops | Tactic | "how to find 500 leads in 30 minutes using Apollo.io (exact filters)" |
| 4 | #general | Poll | "what's your biggest blocker right now? (options: leads, product, pricing, time)" |
| 5 | #content-drops | Alpha drop | "3 freelance niches paying $5K+/project on Upwork right now (with search links)" |
| 5 | #opportunities | Seed | Admin posts a real collab opportunity |
| 6 | #content-drops | Case study | "how a member went from $0 to $2.3K MRR in 6 weeks (exact steps)" |
| 7 | #content-drops | Weekly roundup | "this week's top wins, best roasts, and highest-signal drops" |

### Week 2: Engagement

| Day | Channel | Type | Topic |
|-----|---------|------|-------|
| 8 | #content-drops | Alpha drop | "the Twitter/X reply strategy that grew me from 0 to 1K followers in 14 days" |
| 9 | #content-drops | Revenue method | "how to make $500-2K/mo with a single Gumroad product (step by step)" |
| 9 | #general | Challenge launch | "7-day sprint: ship something by Sunday. post daily updates in #accountability." |
| 10 | #content-drops | Tactic | "the 'stack ranking' method for choosing what to build next (kills analysis paralysis)" |
| 11 | #content-drops | Tool | "how I monitor 200+ competitor pages for free and get alerts when anything changes" |
| 12 | #content-drops | Alpha drop | "5 Fiverr gig titles that actually rank (tested across 30+ gigs)" |
| 13 | #content-drops | Framework | "the $100/day freelance formula: niche + platform + outreach cadence" |
| 14 | #content-drops | Weekly roundup | "week 2 recap: sprint results, new members, top alpha" |

### Week 3: Depth

| Day | Channel | Type | Topic |
|-----|---------|------|-------|
| 15 | #content-drops | Deep dive | "SEO for solopreneurs: how to rank a new site in 30 days (real case study)" |
| 16 | #content-drops | Tactic | "the 'portfolio snowball' method: every client = 3 more portfolio pieces = higher rates" |
| 17 | #content-drops | Alpha drop | "3 underpriced skills on Upwork right now (before they get saturated)" |
| 17 | #general | AMA | Admin does a live "ask me anything" for 2 hours |
| 18 | #content-drops | Revenue method | "building a $1K/mo newsletter from scratch (exact tech stack, content calendar, monetization)" |
| 19 | #content-drops | Tool | "the 4 Chrome extensions that save me 3 hours/day (all free)" |
| 20 | #content-drops | Framework | "the 'revenue per hour' audit: calculating your real hourly rate across all income streams" |
| 21 | #content-drops | Weekly roundup | "week 3: member highlights, revenue milestones, best content" |

### Week 4: Monetization push

| Day | Channel | Type | Topic |
|-----|---------|------|-------|
| 22 | #content-drops | Alpha drop | "how to price your freelance services (the formula that 3x'd my rates)" |
| 23 | #content-drops | Case study | "from fired to $8K/mo: a member's 90-day breakdown" |
| 24 | #content-drops | Tactic | "the 'weekend product' method: build and launch a digital product in 48 hours" |
| 25 | #content-drops | Deep dive | "cold DM templates that get replies (tested on 2,000+ sends across LinkedIn, Twitter, Instagram)" |
| 26 | #content-drops | Alpha drop | "5 micro-SaaS ideas validated by real demand (with keyword data)" |
| 27 | #content-drops | Framework | "the printmaxx stack: $280/mo in tools generating $5K+/mo in revenue" |
| 28 | #content-drops | Revenue method | "affiliate marketing without a following: the forum + SEO + comparison page play" |
| 29 | #general | Challenge | "30-day challenge kickoff: $1,000 in new revenue. starts tomorrow." |
| 30 | #content-drops | Monthly recap | "month 1 stats: members, total community MRR, top wins, what's coming in month 2" |

---

## Monetization details

### Hustler tier: $29/mo

**What they get:**
- Daily alpha drops in #paid-alpha (exclusive, not posted anywhere else)
- Swipe file access: 50+ proven templates (emails, landing pages, DM scripts, ad copy)
- Weekly accountability threads (post numbers or get called out)
- "Ask anything" channel with guaranteed 24h response
- Early access to all PRINTMAXX products

**Pitch (for landing page / checkout):**
```
the hustler tier.

daily alpha you won't find on Twitter. tested templates you can copy-paste. weekly accountability so you can't hide from your own numbers.

$29/mo. cancel anytime. the average member makes back the subscription cost in week 1.

what you get:
- daily actionable intel in #paid-alpha (not available anywhere else)
- 50+ proven templates (cold emails, landing pages, DM scripts)
- weekly accountability (post your numbers or get called out)
- guaranteed 24h response to any question
- early access to every new PRINTMAXX product

this isn't a course. it's a room full of people who are actually building.
```

### Inner Circle: $99/mo

**What they get:**
- Everything in Hustler tier
- Monthly 1-on-1 call (30 min, calendar booking)
- Deal flow channel (acquisition targets, partnerships, revenue shares)
- Inner circle strategy discussions (high-level, no beginners)
- Direct access to PRINTMAXX founder

**Pitch:**
```
the inner circle.

everything in hustler, plus the stuff that doesn't scale.

monthly 1-on-1 calls. deal flow. strategy with people doing $5K+ MRR.

$99/mo. limited to 50 members (not artificial scarcity, real bandwidth constraint).

what you get on top of hustler:
- monthly 30-min 1-on-1 call (book via Calendly in #1on1-booking)
- deal flow channel: acquisitions, partnerships, rev-share opps
- inner circle chat: strategy with verified $5K+ MRR builders
- direct founder access (DMs open, response within 12h)

this tier is not for beginners. it's for people ready to go from $1K to $10K+.
```

---

## Growth tactics (first 100 members)

1. **Cross-post from Twitter.** Every alpha drop in #content-drops also becomes a tweet with "full breakdown in the discord (link in bio)."
2. **Invite incentive.** First 100 members get @og role (permanent, cosmetic, but exclusive). Tell them: "invite 3 builders, you keep the role forever."
3. **Landing page roasts.** Post the best roasts to Twitter as content. Tag the person being roasted. They share it. Their audience joins.
4. **Reddit seeding.** Post value-first content in r/solopreneur, r/EntrepreneurRideAlong, r/SideProject. Include "I run a free discord for builders" at the end. Not spammy, just contextual.
5. **Collab with other small servers.** Find 3-5 discord servers with 100-500 members in adjacent niches. Cross-promote.
6. **Launch on Twitter Spaces.** Host a weekly 30-min Twitter Space. Topic = that week's top alpha drop. Pin the discord link during the space.

---

## Retention mechanics

1. **Weekly streaks.** MEE6 XP system tracks engagement. Miss a week, lose your streak. Top 10 streakers get shouted out monthly.
2. **Monthly challenges.** Revenue challenges, shipping challenges, outreach challenges. Winner gets free month of inner circle.
3. **Verified builder badge.** Post proof of $1K+ MRR in #wins, get the @verified-builder role. Social proof that keeps people pushing.
4. **Content drops never stop.** The 14,000+ alpha entry pipeline feeds daily content drops. Members should feel like missing a day = missing alpha.
5. **Accountability pressure.** Weekly threads where you post your numbers. Peer pressure works. People stay because they don't want to be the one who stopped posting.

---

## Launch checklist

- [ ] Create Discord server
- [ ] Set up all 18 channels in 5 categories
- [ ] Create all 7 roles with correct permissions
- [ ] Install MEE6, configure welcome + leveling + auto-mod
- [ ] Install Carl-bot, configure reaction roles + timed DMs
- [ ] Set up paid subscriptions (Whop, Launchpass, or native)
- [ ] Connect Stripe to subscription tool
- [ ] Post rules in #rules
- [ ] Post welcome message in #start-here
- [ ] Seed #wins with 2-3 real screenshots
- [ ] Seed #content-drops with first 3 alpha drops
- [ ] Post self-roast in #roast-my-landing-page
- [ ] Post 1 opportunity in #opportunities
- [ ] Announce on Twitter (@PRINTMAXXER)
- [ ] Share invite link in bio

**Total time to launch: ~90 minutes if all content is prepped (it is).**
