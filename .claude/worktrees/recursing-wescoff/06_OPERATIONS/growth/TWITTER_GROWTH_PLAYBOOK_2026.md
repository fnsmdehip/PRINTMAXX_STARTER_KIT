# Twitter/X Growth Playbook 2026

**Last Updated:** 2026-01-25
**Purpose:** Complete guide to X algorithm optimization, growth tactics, monetization, and account building
**Companion Docs:** `X_ALGORITHM_OPTIMIZATION.md`, `NICHE_POSTING_STRATEGY.md`, `EDGE_GROWTH_TACTICS.md`

---

## Table of Contents

1. [Algorithm Deep Dive](#section-1-algorithm-deep-dive)
2. [Content Strategy](#section-2-content-strategy)
3. [Profile Optimization](#section-3-profile-optimization)
4. [Engagement Tactics](#section-4-engagement-tactics)
5. [Growth Systems](#section-5-growth-systems)
6. [Monetization Path](#section-6-monetization-path)
7. [Automation Stack](#section-7-automation-stack)
8. [Account Types & Playbooks](#section-8-account-types--playbooks)
9. [PRINTMAXX Account Strategy](#section-9-printmaxx-account-strategy)
10. [Weekly Workflow](#section-10-weekly-workflow)

---

## SECTION 1: Algorithm Deep Dive

### How the X Algorithm Works (Jan 2026)

**Source:** X open-sourced algorithm on GitHub (12.8k stars)

The X "For You" feed uses a **Grok-based transformer model** that predicts engagement probability for each post.

### Scoring Formula

```
Final Score = Sum (weight x P(action))

Actions scored:
- P(like) - MEDIUM weight
- P(reply) - HIGHEST weight
- P(repost) - HIGH weight
- P(quote) - HIGH weight
- P(click) - MEDIUM weight
- P(dwell time) - HIGH weight (time spent on post)
- P(profile click) - HIGH weight (users visiting profile)
- P(video watch) - HIGH weight (for video content)
- P(bookmark) - HIGH weight (save signal)
```

### Key Algorithm Components

| Component | Function |
|-----------|----------|
| **Thunder** | In-network content (from accounts you follow) |
| **Phoenix** | Out-of-network content (ML-discovered) |
| **Home Mixer** | Combines both into final feed |
| **VFFilter** | Removes spam, policy violations |

### Engagement Signals Ranked by Weight

| Signal | Weight | Why It Matters |
|--------|--------|----------------|
| Replies | HIGHEST | Indicates conversation, deeper engagement |
| Quote tweets | HIGH | Shows thoughtful engagement |
| Bookmarks | HIGH | Strong save signal, indicates value |
| Reposts | HIGH | Distribution signal |
| Dwell time | HIGH | Content is compelling enough to read |
| Profile clicks | HIGH | Interest in author beyond single post |
| Video watch time | HIGH | For video content specifically |
| Likes | MEDIUM | Low-effort engagement |

### What Gets FILTERED OUT (Avoid These)

**Pre-Scoring Filters:**
- Duplicates (same content multiple times)
- Too old (recency matters heavily)
- From blocked/muted accounts
- Containing muted keywords
- Previously seen or recently served
- Ineligible subscription content

**Post-Selection Filters (VFFilter):**
- Deleted content
- Spam patterns
- Violence/gore
- Policy violations

### What Gets BOOSTED (Optimize For These)

**Author Factors:**
- Verification status (Premium boost confirmed)
- Author diversity (algorithm attenuates repeated author scores)
- Account age and history
- Engagement velocity on previous posts

**Content Factors:**
- Recency (newer posts preferred)
- Media type (videos get special handling)
- Reply count velocity
- Quote tweet depth
- Thread engagement

### The Author Diversity Problem

**Critical insight:** Posting too frequently HURTS individual post scores.

The algorithm applies a decaying multiplier to repeated posts from the same author:
- Post 1: 100% score
- Post 2 (within 2 hours): ~80% score
- Post 3 (within 2 hours): ~60% score
- Post 4+: Diminishing returns

**Tactic:** Space posts 2-4 hours apart minimum.

---

## SECTION 2: Content Strategy

### Hook Formulas That Work

Based on analysis of 10K+ viral posts from high-signal accounts:

**Tier 1: Consequence-First Hooks (HIGHEST engagement)**
```
[NUMBER] [OUTCOME] in [TIMEFRAME].
here's how:

Example:
$47k in 14 days from cold email.
here's the exact framework:
```

**Tier 2: Insider/Gatekeeping Hooks**
```
[ACTIVITY] I do that most people don't:

Example:
3 things I do before 7am that most people won't:
```

**Tier 3: Problem-Solution Hooks**
```
stop [COMMON BEHAVIOR].
[ALTERNATIVE] instead.

Example:
stop building in public.
build in private. launch in public.
```

**Tier 4: Contrarian Hooks**
```
unpopular opinion: [HOT TAKE]

Example:
unpopular opinion: most "productivity" is procrastination disguised as work.
```

**Tier 5: Curiosity Gap Hooks**
```
[RESULT] and I only did [SIMPLE THING].

Example:
10k followers in 60 days and I only posted once per day.
```

### Content Types by Performance

| Content Type | Avg Engagement | Best For | Frequency |
|--------------|----------------|----------|-----------|
| Single insight | 3-5% | Quick value, high volume | Daily |
| Thread (5-7 tweets) | 5-8% | Deep tutorials, authority | 2-3x/week |
| Quote tweet + insight | 4-6% | Trend riding, commentary | Daily |
| Screenshot + analysis | 6-10% | Proof, case studies | 2-3x/week |
| Poll | 8-12% | Community engagement | 1-2x/week |
| Video clip (<60s) | 4-7% | Tutorials, behind-scenes | 2-3x/week |
| Meme/humor | 5-15% | Relatability, shares | 1x/day |

### Thread Structure That Works

**The 7-Tweet Thread Formula:**

1. **Tweet 1 (Hook):** Big promise or result + "here's how:"
2. **Tweet 2 (Context):** Why this matters or backstory
3. **Tweet 3-5 (Body):** The actual steps/framework/method
4. **Tweet 6 (Proof):** Results, metrics, screenshots
5. **Tweet 7 (CTA):** Repost request + follow ask

**Thread Formatting Rules:**
- Number each tweet for easy reference
- One idea per tweet
- Use line breaks for readability
- Include image/screenshot in tweet 1 or 6
- Self-reply with bonus content or resource

### Reply Bait Patterns (Drive Comments)

**Pattern 1: Binary Choice**
```
[OPTION A] or [OPTION B]?

pick one. defend it below.
```

**Pattern 2: Fill in the Blank**
```
the best [TOOL/METHOD/HABIT] I discovered in 2026:

___________

I'll go first: [YOUR ANSWER]
```

**Pattern 3: Rate Request**
```
rate my [STACK/WORKFLOW/ROUTINE] 1-10:

[LIST]

be honest.
```

**Pattern 4: Wrong Answers Only**
```
describe [NICHE THING] using only wrong answers.

I'll start: [JOKE ANSWER]
```

**Pattern 5: Comment Keyword Trigger**
```
I made a [RESOURCE] that [BENEFIT].

giving it away free.

comment "[KEYWORD]" and I'll DM it to you.
```

### A/B Post Strategy (Contrarian Double-Post)

**Proven by @aftermagics:**
```
Post 1: "start using ai to write your replies" (1K views)
Post 2: "stop using ai to write your replies" (1.9K views)

Result: Contrarian "stop" got 2x engagement
```

**How to implement:**
1. Post same topic with opposite takes
2. Space 4-8 hours apart
3. Track which performs better
4. Double down on winning angle
5. Use insights for future content

**A/B Post Ideas:**
- "ship fast break things" vs "ship slow get it right"
- "raise VC" vs "stay bootstrapped"
- "build in public" vs "build in private"
- "use AI for everything" vs "AI is overrated"
- "morning routine" vs "routines are overrated"

---

## SECTION 3: Profile Optimization

### Bio Formula

**Character limit:** 160 characters

**High-converting bio structure:**
```
[RESULT/CREDENTIAL] | [WHAT YOU DO] | [WHO YOU HELP]
[CTA or personality note]
```

**Examples:**

**Business/SaaS:**
```
built 3 apps to $100k+ MRR
teaching AI automation to solopreneurs
link = free workflow templates
```

**Creator:**
```
$2M+ earned writing online
daily threads on growth + monetization
DM "GUIDE" for free content system
```

**Expert:**
```
10 years in cold email
helped 500+ companies book meetings
deliverability wizard | deliveron.org
```

### Pinned Tweet Strategy

**Option 1: Lead Magnet (Highest Conversion)**
```
[HOOK with big promise]

[3-5 bullet points of what's included]

[X,000] people have it.

[LINK or "DM [KEYWORD]"]
```

**Option 2: Thread Compilation**
```
my 10 best posts of 2025:

1. [TOPIC] - [LINK]
2. [TOPIC] - [LINK]
...

follow + save for later.
```

**Option 3: About Me + Social Proof**
```
hi, I'm [NAME].

- [CREDENTIAL 1]
- [CREDENTIAL 2]
- [CREDENTIAL 3]

building @[PROJECT] and sharing everything.

DM me "[WORD]" to connect.
```

**Option 4: Proof/Results Post**
```
[SCREENSHOT of results]

how I did it (full breakdown):

[LINK to thread or resource]
```

### Banner Optimization

**Banner dimensions:** 1500 x 500 pixels

**High-converting banner elements:**
1. Clear headline (what you do/offer)
2. Social proof or credential
3. CTA (website, newsletter, product)
4. Consistent brand colors

**Banner types that work:**
- Product showcase with tagline
- Revenue/growth screenshot
- "Featured in" logo bar
- Simple value proposition text
- Call to action with arrow to bio

### Link in Bio Strategy

**Use a link aggregator** (Linktree, Beacons, Stan Store, or custom page)

**Order links by priority:**
1. Primary CTA (newsletter, product, book call)
2. Free resource (lead magnet)
3. Secondary offers
4. Social proof (press, podcast)
5. Other socials (optional)

**Or use Gumroad/Stripe link directly** if selling one product.

---

## SECTION 4: Engagement Tactics

### The Reply-Guy Strategy (Fastest Growth)

**The concept:** Be first to reply on big accounts with value-adding comments.

**Step-by-step:**
1. **Identify 20-30 target accounts** in your niche (10K-500K followers)
2. **Turn on notifications** for their posts
3. **Reply within first 5-10 minutes** with insight
4. **Reply format:** Add value, don't just agree

**Reply templates that get engagement:**

**Value Addition:**
```
this. and to add:

[YOUR ADDITIONAL INSIGHT]
```

**Personal Experience:**
```
tried this for [TIME PERIOD].

results: [SPECIFIC NUMBERS]

one thing I'd add: [INSIGHT]
```

**Thoughtful Question:**
```
curious about [SPECIFIC ASPECT].

did you find [RELATED QUESTION]?
```

**Data Point:**
```
the numbers back this up.

[STAT or YOUR DATA]
```

**What NOT to reply:**
- "great post!" (zero value)
- link drops without context
- arguments or negativity
- off-topic promotion

### Quote Tweet Strategy

**Daily target:** 2-3 quote tweets

**Quote tweet patterns:**

**Add Context:**
```
[QRT]

this worked for me too.

my results: [SPECIFIC NUMBERS]
```

**Contrarian Take:**
```
[QRT]

respectfully disagree.

here's why: [REASONING]
```

**Expansion:**
```
[QRT]

adding to this:
- [POINT 1]
- [POINT 2]
- [POINT 3]
```

**Personal Application:**
```
[QRT]

tried this in [MY NICHE].

results: [OUTCOME]
```

### Self-Reply Funnel (Convert Engagement to Leads)

**The pattern:** Hook tweet gets attention, self-reply has the CTA.

**Why it works:**
- Hook tweet shows in feed (no link penalty)
- Self-reply shows as first comment
- Algorithm doesn't penalize link in reply
- Feels less salesy than link in main tweet

**Template:**

**Main Tweet:**
```
[CONSEQUENCE-FIRST HOOK]

[METHOD or INSIGHT in 2-3 lines]

here's the exact process:
```

**Self-Reply (CTA):**
```
if you want to do this:

1. [STEP]
2. [STEP]
3. [STEP]

I have a free [RESOURCE] that walks through everything.

[LINK]
```

**Self-Reply Variations:**
- DM keyword ("DM me 'STACK' for the template")
- Bio link ("full breakdown in bio")
- Product pitch ("we built [PRODUCT] for this")
- Newsletter ("I send these weekly: [LINK]")

### Engagement Pods (Legal, Community-Based)

**What they are:** Private groups that engage with each other's content.

**How to find/create:**
1. DM creators in your niche of similar size
2. Create Telegram/Discord group
3. Share posts when published
4. Members like + reply within 30 minutes
5. Quality > quantity (real engagement only)

**Pod rules that work:**
- Max 10-15 members (too big = spam pattern)
- Similar niche/audience
- Genuine engagement (not just likes)
- Reply requirement (algorithm weights replies highest)
- No bots or automation

**Where to find pods:**
- Twitter DM groups
- Discord servers (search "[niche] Twitter growth")
- Telegram groups
- IndieHackers / Twitter communities

---

## SECTION 5: Growth Systems

### The 1000 True Followers System

**Goal:** First 1,000 engaged followers in 90 days.

**Week 1-2: Foundation**
- Complete profile 100%
- Follow 30-50 niche accounts
- Engage only (no posting)
- Study what works in your niche
- Build swipe file of viral posts

**Week 3-4: Content Start**
- Post 3x/day
- Reply to 20+ accounts daily
- Quote tweet 2x/day
- Join 1-2 engagement pods
- Track what gets engagement

**Week 5-8: Optimization**
- Post 4x/day
- Double down on working content types
- Start threads (2x/week)
- Run A/B tests on hooks
- Begin self-reply funnels

**Week 9-12: Scale**
- Post 4-5x/day
- Launch lead magnet
- Build email list from X
- Collaborate with similar accounts
- Guest threads on larger accounts

### Posting Schedule by Niche

**Tech/Business (ET timezone):**
| Time | Content Type |
|------|--------------|
| 8:00 AM | Value drop / insight |
| 12:00 PM | Engagement bait / poll |
| 4:00 PM | Industry commentary |
| 8:00 PM | Thread or meme |

**Best days:** Tuesday-Thursday
**Avoid:** Saturday

**Creator/Solopreneur:**
| Time | Content Type |
|------|--------------|
| 7:00 AM | Morning motivation |
| 11:00 AM | Tutorial / how-to |
| 3:00 PM | Quote tweet / commentary |
| 7:00 PM | Personal story / lesson |

**Best days:** Monday, Wednesday, Friday
**Avoid:** Weekend mornings

**General/Lifestyle:**
| Time | Content Type |
|------|--------------|
| 9:00 AM | Inspirational |
| 1:00 PM | Engagement post |
| 5:00 PM | Story / personal |
| 9:00 PM | Casual / meme |

**Best days:** Every day works, Sunday slightly higher

### The Viral Tweet Checklist

Before posting, verify:

- [ ] Hook in first line (not buried)
- [ ] Specific number included
- [ ] Invites replies (question, opinion request)
- [ ] Under 280 characters (or thread)
- [ ] 2+ hours since last post
- [ ] No muted keywords
- [ ] Media attached if relevant
- [ ] Self-reply drafted with CTA

### Growth Milestones & Tactics

| Followers | Primary Tactic | Secondary |
|-----------|----------------|-----------|
| 0-500 | Reply-guy strategy | Engagement pods |
| 500-1K | Consistent posting | Quote tweets |
| 1K-5K | Threads + lead magnets | Collaborations |
| 5K-10K | Guest threads | Viral content attempts |
| 10K-50K | Newsletter + products | Paid shoutouts |
| 50K+ | Platform diversification | Monetization focus |

---

## SECTION 6: Monetization Path

### Twitter/X Revenue Streams

**1. Ads Revenue Share (X Premium)**

Requirements:
- X Premium subscriber ($8/mo or $84/yr)
- 500+ followers
- 5M organic impressions in last 3 months
- Active in last 30 days

Earnings: ~$0.50-$2.00 per 1K impressions (varies widely)

**2. Subscriptions**

Requirements:
- X Premium subscriber
- 500+ followers

How it works:
- Set monthly price ($3-$100)
- Offer exclusive content
- X takes 0% fee first year, then 3%

Best for:
- Thought leaders
- Curators
- Niche experts

**3. Tips**

Requirements:
- Enable tips in settings
- Connect payment (Stripe, PayPal, Cash App, etc.)

How it works:
- Followers can tip any amount
- You keep most (minus payment processor fee)
- X takes no cut

**4. Affiliate Links**

No platform requirements.

High-converting affiliate strategies:
- Tool recommendations in threads
- "My stack" posts with affiliate links
- Tutorial content with product links
- Comparison posts

**Where to find affiliate programs:**
- Impact.com
- ShareASale
- PartnerStack
- Direct brand outreach
- "brand name affiliate program" Google search

**5. Products/Services**

Sell directly:
- Digital products (courses, templates, guides)
- Services (consulting, coaching, done-for-you)
- Physical products (merch, books)
- SaaS subscriptions

**6. Sponsorships**

Requirements: Typically 10K+ engaged followers

How to get sponsors:
- Put "open for sponsorships" in bio
- Create media kit with engagement stats
- Reach out to brands in your niche
- Use platforms like Passionfroot, Grapevine

Rates: $50-$500 per post (10K-100K followers)

### Monetization Timeline

| Month | Focus | Revenue Target |
|-------|-------|----------------|
| 1-3 | Growth only | $0 |
| 4-6 | Lead magnet + email list | $0-100 (tips) |
| 7-9 | Launch first product | $500-2K |
| 10-12 | Optimize + affiliates | $2K-5K |
| Year 2 | Scale products + subs | $5K-20K/mo |

### The Product Ladder

**Start simple, add complexity:**

1. **Free Lead Magnet** (0 friction)
   - Template, checklist, guide
   - Builds email list
   - Establishes expertise

2. **Low-Ticket Product** ($7-47)
   - Expanded lead magnet
   - Mini-course or toolkit
   - Low friction purchase

3. **Mid-Ticket Product** ($97-297)
   - Full course or system
   - Community access
   - Templates + support

4. **High-Ticket** ($500-2000+)
   - Coaching/consulting
   - Done-for-you services
   - Cohort programs

---

## SECTION 7: Automation Stack

### Scheduling Tools

| Tool | Cost | Best For |
|------|------|----------|
| **Typefully** | $12-40/mo | Threads, drafting |
| **Hypefury** | $19-49/mo | Scheduling + auto-engagement |
| **Buffer** | $6-120/mo | Multi-platform |
| **TweetHunter** | $49/mo | AI writing + CRM |
| **Hootsuite** | $99/mo | Enterprise |
| **Twitter native** | Free | Basic scheduling |

**Recommended:** Hypefury for solopreneurs, Typefully for thread-focused

### Analytics Tools

| Tool | Cost | Best For |
|------|------|----------|
| **Twitter Analytics** | Free | Basic metrics |
| **Hypefury** | Included | Scheduling + analytics combo |
| **TweetHunter** | Included | Growth-focused metrics |
| **Followerwonk** | $29-79/mo | Audience analysis |
| **SparkToro** | $50-225/mo | Audience research |

### Thread Tools

| Tool | Cost | Best For |
|------|------|----------|
| **Typefully** | $12-40/mo | Thread writing + publishing |
| **ThreadStart** | Free | Thread formatting |
| **Chirr App** | Free | Thread splitting |
| **Tweet Hunter** | $49/mo | AI thread writing |

### Safe Automation Limits (Jan 2026)

| Action | New Account | Aged Account |
|--------|-------------|--------------|
| Follows/day | 50-100 | 200-400 |
| Likes/day | 200-300 | 500-1000 |
| Tweets/day | 5-10 | 20-50 |
| DMs/day | 20-30 | 50-100 |
| Retweets/day | 50-100 | 200-300 |

**Note:** X is the most lenient platform for automation.

### Automation Don'ts

- No Chrome extensions (detectable)
- No follow/unfollow bots
- No auto-DM spam
- No bought followers/engagement for marketing claims
- No aggressive scraping

---

## SECTION 8: Account Types & Playbooks

### Personal Brand Account

**Best for:** Experts, consultants, creators

**Content mix:**
- 40% Value (tutorials, insights)
- 25% Personal (stories, lessons)
- 20% Engagement (polls, questions)
- 15% Promotion (products, services)

**Growth tactics:**
- Authentic voice development
- Story-driven threads
- Behind-the-scenes content
- Networking with peers

### Niche Expert Account

**Best for:** Specific skill/topic authority

**Content mix:**
- 50% Educational (how-tos, frameworks)
- 25% Industry commentary
- 15% Tool/resource sharing
- 10% Promotion

**Growth tactics:**
- Deep-dive threads
- Resource compilations
- Case study breakdowns
- Guest appearances on podcasts

### Curated Content Account

**Best for:** News, aggregation, niche coverage

**Content mix:**
- 60% Curated (shares, summaries)
- 25% Commentary (hot takes)
- 10% Original insights
- 5% Promotion

**Growth tactics:**
- First to break news
- Daily/weekly roundups
- Engaging with sources
- Building source network

### Meme/Entertainment Account

**Best for:** Niche humor, relatable content

**Content mix:**
- 70% Entertainment (memes, jokes)
- 20% Relatable (observations)
- 10% Occasional value

**Growth tactics:**
- Trend riding
- Format remixing
- Cross-platform repurposing
- Collaboration with similar accounts

### Business/Brand Account

**Best for:** Companies, products, services

**Content mix:**
- 40% Value (industry content)
- 30% Social proof (customers, results)
- 20% Product (features, updates)
- 10% Culture (team, behind-scenes)

**Growth tactics:**
- Employee advocacy
- Customer spotlights
- Industry thought leadership
- Responsive engagement

---

## SECTION 9: PRINTMAXX Account Strategy

### @PRINTMAXXER Main Account

**Positioning:** Solopreneur building multiple revenue streams in public

**Voice:** Weighted blend (see copy-style.md)
- 50% @pipelineabuser energy (aggressive, specific numbers)
- 25% @tom777kruise brevity (philosophical, short)
- 15% @codyschneiderxx bluntness (action-oriented)
- 10% @levelsio authenticity (real numbers, honest)

**Content Pillars:**

1. **Build Updates** (30%)
   - App launches
   - Revenue milestones
   - Technical wins/failures

2. **Tactics/Methods** (30%)
   - AI automation workflows
   - Cold outreach strategies
   - Content distribution systems

3. **Industry Commentary** (20%)
   - AI/tech news takes
   - Solopreneur meta
   - Tool recommendations

4. **Engagement Content** (20%)
   - Polls
   - Reply bait
   - Memes

**Posting Schedule:**
| Time | Content Type |
|------|--------------|
| 8 AM ET | Build update / value |
| 12 PM ET | Engagement bait |
| 4 PM ET | Commentary / hot take |
| 8 PM ET | Thread or meme |

### Faith Niche Account

**Positioning:** Faith-based productivity and spiritual growth

**Content Pillars:**
1. Morning devotionals (30%)
2. Scripture application (25%)
3. PrayerLock promotion (20%)
4. Community engagement (25%)

**Unique Angles:**
- "Phone vs prayer" accountability
- Digital discipline + faith
- Prayer tracking/habits
- Modern application of scripture

**Voice:** Warm but direct, no preachiness, action-oriented

### Fitness Niche Account

**Positioning:** No-BS fitness for busy people

**Content Pillars:**
1. Workout tips (30%)
2. Motivation (25%)
3. WalkToUnlock promotion (20%)
4. Lifestyle/nutrition (25%)

**Unique Angles:**
- Phone addiction vs movement
- Gamified fitness
- Simple protocols
- Time-efficient workouts

**Voice:** Direct, motivational, no guru energy

### AI/Tech Niche Account

**Positioning:** AI tools and automation for solopreneurs

**Content Pillars:**
1. Tool discoveries (30%)
2. Workflow tutorials (30%)
3. Industry news takes (25%)
4. Prompt templates (15%)

**Unique Angles:**
- Real tool comparisons with numbers
- Automation stacks that work
- AI + business integration
- No hype, just results

**Voice:** Technical but accessible, specific, skeptical of hype

### Cross-Pollination Strategy

**Daily Cross-Account Actions:**

| Day | Action |
|-----|--------|
| Monday | AI account retweets Faith devotional |
| Tuesday | Faith retweets Fitness motivation |
| Wednesday | Fitness retweets AI tool |
| Thursday | AI retweets Fitness transformation |
| Friday | Faith retweets AI workflow (work-related) |
| Saturday | Fitness retweets Faith community |
| Sunday | All accounts soft-promote each other |

**Shared content opportunities:**
- "The stack" posts showing all three niches
- Cross-niche tutorials (AI for prayer tracking, etc.)
- Collaborative threads

---

## SECTION 10: Weekly Workflow

### Monday: Planning Day

**Morning (30 min):**
- Review last week's analytics
- Identify top 3 performing posts
- Note content types/hooks that worked
- Update swipe file

**Afternoon (1 hour):**
- Draft week's content in Typefully/Hypefury
- Schedule main posts
- Plan threads for Tuesday/Thursday
- Prepare engagement pod submissions

### Tuesday-Thursday: Execution Days

**Daily Routine (1.5 hours):**

**Morning (30 min):**
- Reply to notifications
- Engage on 10 target accounts
- Quote tweet 1 trending post
- Check scheduled posts

**Midday (15 min):**
- Reply to morning post engagement
- Engage on lunch-scroll content
- Post midday content

**Evening (45 min):**
- Reply to day's engagement
- Post evening content
- Engage on 10 more accounts
- DM any new connections

### Friday: Analysis & Prep

**Afternoon (1 hour):**
- Export week's analytics
- Document what worked/didn't
- Update content calendar
- Batch create weekend content
- Schedule weekend posts

### Saturday-Sunday: Light Engagement

**Daily (30 min):**
- Reply to notifications
- Light engagement (optional posting)
- Consume content for inspiration
- Build swipe file

### Monthly Tasks

**Week 1:**
- Deep analytics review
- Update posting times based on data
- Refresh pinned tweet if needed

**Week 2:**
- A/B test new content type
- Reach out to 5 potential collaborators
- Update bio/banner if needed

**Week 3:**
- Launch new lead magnet or update existing
- Review monetization performance
- Analyze competitor accounts

**Week 4:**
- Content strategy review
- Plan next month's themes
- Update automation/tools if needed

---

## Quick Reference Cards

### Before You Post Checklist

- [ ] Hook in first 5 words
- [ ] Specific number included
- [ ] No muted keywords
- [ ] 2+ hours since last post
- [ ] Invites engagement (question, poll, take)
- [ ] Self-reply CTA ready
- [ ] Would @pipelineabuser post this?

### Engagement Priority Order

1. Reply to replies on your posts (algorithm signal)
2. Reply to large accounts in niche (visibility)
3. Quote tweet trending content (ride waves)
4. Engage in pod (mutual growth)
5. Reply to similar-size accounts (networking)

### Content Performance Tiers

| Tier | Impressions | Action |
|------|-------------|--------|
| Viral | 10x avg | Create variations |
| Strong | 3-10x avg | Repeat format |
| Average | 0.5-3x avg | Test hooks |
| Weak | <0.5x avg | Abandon format |

### Emergency Recovery (If Engagement Drops)

1. Stop automated actions for 24 hours
2. Post only text (no links) for 3 days
3. Increase reply engagement 2x
4. Return to basics (proven formats only)
5. Analyze what changed

---

## Resources

**Internal docs:**
- `OPS/X_ALGORITHM_OPTIMIZATION.md` - Algorithm deep dive
- `OPS/NICHE_POSTING_STRATEGY.md` - Reply bait, A/B testing
- `OPS/EDGE_GROWTH_TACTICS.md` - Automation limits
- `OPS/NICHE_ACCOUNT_CONTENT_CALENDAR.md` - Full posting calendar
- `LEDGER/WINNING_CONTENT_STRUCTURES.csv` - Content templates
- `.claude/rules/copy-style.md` - Voice guidelines

**External tools:**
- [X Algorithm GitHub](https://github.com/xai-org/x-algorithm)
- [Typefully](https://typefully.com)
- [Hypefury](https://hypefury.com)
- [TweetHunter](https://tweethunter.io)

**High-signal accounts to study:**
- @pipelineabuser (cold outreach + growth)
- @levelsio (indie hacking)
- @tdinh_me (technical solopreneur)
- @knoxtwts (content marketing)
- @codyschneiderxx (SaaS growth)
- @dannypostmaa (honest building)

---

## Maintenance

- Update algorithm section when X releases changes
- Refresh automation limits monthly
- Add new monetization options as X releases them
- Update high-signal accounts quarterly
- Review content performance weekly

---

*Last Updated: 2026-01-25*
*Next Review: 2026-02-01*
