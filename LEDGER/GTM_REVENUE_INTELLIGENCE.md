# GTM & REVENUE INTELLIGENCE MASTER DOC

**Created:** 2026-01-20
**Purpose:** Single source of truth for all money paths, channels, tools, strategies, and costs
**Update Frequency:** Weekly minimum + whenever new alpha discovered

---

# CORE PHILOSOPHY: PARALLEL LANES + A/B EVERYTHING

**The PrintMaxx way:** Run multiple methods simultaneously. Track everything. Kill losers. Scale winners.

There is no "best" method. Platforms drift. What works today fails tomorrow. The only sustainable edge is **iteration speed + redundancy**.

## The 4-Lane Testing Framework

For EVERY channel (email, social, ads, outreach), run parallel lanes:

| Lane | Description | Purpose |
|------|-------------|---------|
| **Lane A** | Conservative/Manual | Safest, baseline performance |
| **Lane B** | Semi-Automated | Balance of scale + safety |
| **Lane C** | Full Automation | Max throughput, higher risk |
| **Lane D** | Experimental | New tools, methods, edge cases |

**Rules:**
- Minimum 3 accounts/inboxes per lane
- 7-day minimum test period
- Track: deliverability, response rate, flags/bans, conversion
- Weekly review: kill losers, double down on winners

## A/B Test Everything

**Content:** Hook variants, CTA variants, posting times
**Email:** Subject lines, body copy, send windows, inbox providers
**Ads:** Creative variants, audiences, placements
**Outreach:** Opening lines, value props, follow-up cadence

**Minimum sample before decisions:**
- Email: 100 sends per variant
- Content: 10 posts per variant
- Ads: $50 spend per variant
- Outreach: 50 touches per variant

## Redundancy Principle

Never rely on a single:
- Email provider (run 2-3 simultaneously)
- Social platform (diversify across X, TikTok, IG, YT)
- Proxy provider (have backup ready)
- Lead source (multiple data providers)
- Payment processor (Stripe + Gumroad + backup)

If one fails, others keep printing.

---

## QUICK REFERENCE: Current Priority Stack

| Priority | Channel | Tool | Cost | Status |
|----------|---------|------|------|--------|
| 1 | Content Farm (X/TikTok/IG/YT) | Native + n8n | $0 | ACTIVE |
| 2 | Email List Building | Substack/Landing | $0 | ACTIVE |
| 3 | Cold Email (B2B) | EmailBison/Instantly | $30-100/mo | WEEK 5+ |
| 4 | LinkedIn InMail | Native/Dux-Soup | $0-50/mo | WEEK 5+ |
| 5 | Paid Ads | Meta/TikTok | Variable | POST-REVENUE |

---

# SECTION 1: OUTBOUND CHANNELS

## 1.1 COLD EMAIL

### The Multi-Lane Email Strategy

**Run ALL tiers simultaneously. Track. Compare. Scale winners.**

### Lane A: API-First Platforms (Primary)
- **Instantly** - $30/mo starter, good deliverability, API access
- **Smartlead** - $39/mo, unlimited inboxes, solid API
- **EmailBison** - $49/mo, Claude-friendly integration

**Start with 2 platforms. Compare deliverability over 2 weeks.**

### Lane B: Inbox-as-a-Service (Parallel)
- **DeliverOn.org** - $49/mo, pre-warmed inboxes
- **Mailforge** - $3/inbox/mo, bulk warm inboxes
- **Mailscale** - Similar pricing, newer

**Use for instant scale without warmup wait.**

### Lane C: DIY Infrastructure (Redundancy)
- Buy domain ($10/yr GoDaddy/Namecheap)
- Set up SPF/DKIM/DMARC
- Warm for 2-4 weeks (20 emails/day gradual increase)
- Use warmup tool (Warmbox, Lemwarm)

**Cheapest long-term. Requires patience.**

### Lane D: Old School Gmail Method (Experimental)
- Create Gmail accounts with real phone verification
- Warm manually: send to friends, reply chains, calendar invites
- Keep under 50 sends/day
- Use for high-value targets where deliverability is critical

**Limits:** ~50/day per inbox, manual work, but highest inbox placement

### Volume Guidelines
- Week 1-2: 10-20 emails/day/inbox
- Week 3-4: 30-50 emails/day/inbox
- Week 5+: 50-100 emails/day/inbox (max)
- Never exceed 100/day/inbox or you burn it

### Lead Sources
| Source | Cost | Quality | Volume |
|--------|------|---------|--------|
| Apollo.io | Free trial → $49/mo | HIGH | 1000s |
| Hunter.io | Free tier → $49/mo | HIGH | 100s |
| BuiltWith | Free tier | MEDIUM | Filter by tech |
| LinkedIn Sales Nav | $80/mo | HIGHEST | Targeted |
| Crunchbase | Free tier | HIGH | Funding-timed |
| RocketReach | $39/mo | HIGH | 100s |
| Clearbit | $99/mo+ | HIGHEST | Enterprise |
| ZoomInfo | $$$$ | HIGHEST | Enterprise |
| Manual scraping (Apify/Phantombuster) | $0-50/mo | VARIES | Custom |

### Email Copy Structure (Proven)
```
SUBJECT: {Specific hook} - {Personalization}
Example: "Saw your {tech stack} - quick idea"

LINE 1: Observation (proves you looked)
"Noticed you're using [competitor] for [thing]"

LINE 2-3: Problem → Bridge
"Most [role] waste [X hours] on [pain point]"

LINE 4: Offer (specific, low commitment)
"Happy to show you how [Company X] cut that by 80% - 15 min call?"

LINE 5: Soft CTA
"Worth a look?"

SIGNATURE: Name, title (keep short)
```

### Costs Summary
| Setup | Monthly Cost |
|-------|-------------|
| DIY (1 domain + warmup) | $10/yr + time |
| Instantly Starter | $30/mo |
| Smartlead + Apollo | $88/mo |
| Full Stack (Instantly + Sales Nav + DeliverOn) | $160-200/mo |

---

## 1.2 LINKEDIN OUTBOUND

### Strategy Tiers

**Tier A: Manual (Free, Safest)**
- 100 connection requests/week limit
- 150 InMails/mo with Premium
- Focus on warm DMs to 2nd connections

**Tier B: Semi-Automated**
- **Dux-Soup** - $15/mo, LinkedIn automation
- **Expandi** - $99/mo, cloud-based, safer
- **Linked Helper** - $15/mo, desktop app
- **Waalaxy** - Free tier → $30/mo

**Tier C: Full Automation (Higher Risk)**
- **Phantombuster LinkedIn Flows** - $30-100/mo
- Use with residential proxies
- Expect some profile restrictions

### LinkedIn Copy Structure
```
CONNECTION REQUEST (300 char max):
"Hey {FirstName}, saw your work on {specific thing}.
Building something similar in {niche}. Would love to connect."

FOLLOW-UP DM 1 (Day 2):
"Thanks for connecting! Quick q - how are you handling {pain point}?"

FOLLOW-UP DM 2 (Day 5):
"Most {role}s I talk to waste hours on {thing}.
Built a {solution} that {specific result}.
Want me to show you?"

FOLLOW-UP DM 3 (Day 10):
"Last ping - free to hop on a call this week?
Worst case you get {specific takeaway}."
```

### Costs Summary
| Setup | Monthly Cost |
|-------|-------------|
| Free (manual) | $0 |
| LinkedIn Premium | $60/mo |
| Premium + Dux-Soup | $75/mo |
| Sales Nav + Expandi | $180/mo |

---

## 1.3 COLD CALLING

### Strategy Tiers

**Tier A: AI Cold Call (New Meta)**
- **Bland.ai** - $0.09/min, AI voice agent
- **Synthflow** - $30/mo, AI caller
- **Air.ai** - Enterprise pricing
- **Retell.ai** - $0.10/min
- **Vapi.ai** - $0.05/min, developer-friendly

**Tier B: Human VA Cold Call**
- **Upwork VA (Philippines)** - $5-10/hr
- **OnlineJobs.ph** - $4-8/hr
- **Specialized SDR agencies** - $2-5k/mo

**Tier C: DIY Cold Call**
- **OpenPhone** - $15/mo, multiple numbers
- **Google Voice** - Free (personal use)
- **PhoneBurner** - $149/mo, power dialer

### Script Structure
```
OPENER (5 sec):
"Hi {Name}, this is {You} from {Company}.
Got 30 seconds?"

PITCH (15 sec):
"We help {role} at {company type}
cut {pain point} by {specific %}.
{Social proof - "Just did this for X"}."

QUALIFICATION:
"Is that something you're dealing with?"

CLOSE:
"Want to see how it works?
I can show you in 15 minutes."
```

### Costs Summary
| Setup | Monthly Cost |
|-------|-------------|
| DIY (OpenPhone + manual) | $15/mo |
| AI Caller (Bland.ai 1000 min) | ~$90/mo |
| VA (20 hrs/mo) | $100-200/mo |
| Power Dialer + VA | $300-500/mo |

---

## 1.4 SOCIAL DM OUTBOUND

### Platforms & Tools

**X (Twitter)**
- Manual DMs only (automation = ban)
- Use saved replies for speed
- Target followers of competitors

**Instagram**
- **ManyChat** - $15/mo, DM automation
- **IGdm Pro** - Desktop app, faster replies
- Manual mass story views → reply to replies

**TikTok**
- Manual only (no reliable automation)
- Comment on competitor videos → DM responders

### DM Copy Structure (Non-Cringe)
```
OPENER:
"Yo, saw your post about {specific thing}.
Actually working on something similar."

VALUE:
"Built a {thing} that {result}.
Might be useful for you."

SOFT CTA:
"Want me to send it over?"
```

### Costs Summary
| Platform | Tool | Cost |
|----------|------|------|
| X | Manual | $0 |
| IG | ManyChat | $15/mo |
| TikTok | Manual | $0 |

---

# SECTION 2: CONTENT CHANNELS

## Account Testing Matrix (4 Lanes)

**Apply the 4-lane framework to social accounts:**

| Lane | Device | Warmup Method | Risk Level |
|------|--------|---------------|------------|
| **Lane A** | Real iPhone/Android | Manual only | LOWEST |
| **Lane B** | Desktop + GoLogin | Hybrid (manual + scheduled) | LOW |
| **Lane C** | Anti-detect + Proxy | Semi-automated | MEDIUM |
| **Lane D** | Remote device farm | Full automation | HIGHEST |

**Per lane:** 3 accounts minimum, 7-day test period

**Track per account:**
- views_24h
- engagement_rate
- follower_growth
- flags/restrictions
- time_cost

**Weekly decision:** Kill restricted accounts, double down on growing ones.

---

## 2.1 SHORT-FORM VIDEO

### Platform Breakdown (Run ALL Simultaneously)

| Platform | Best For | Posting Cadence | Monetization |
|----------|----------|-----------------|--------------|
| TikTok | Discovery, virality | 1-3x/day | Creator Fund, affiliates |
| YouTube Shorts | SEO, long-tail | 1-2x/day | Adsense, affiliates |
| Instagram Reels | Brand, trust | 1x/day | Affiliates, DM sales |
| X Video | Tech audience | 1x/day | Course/product links |

**Redundancy rule:** Post same content to ALL platforms. Track which converts best per niche.

### Content Types (Ranked by ROI)

**Tier 1: How-To / Tutorial**
- "How I automated X in 10 minutes"
- "3-step setup for Y"
- Clear problem → solution

**Tier 2: Results / Proof**
- "Made $X from this strategy"
- "Here's the dashboard"
- Numbers + screenshots

**Tier 3: Hot Takes / Opinions**
- "Most people get X wrong"
- "Stop doing Y"
- Controversial = engagement

**Tier 4: Storytelling**
- "Went from X to Y"
- Journey content
- Builds trust

### Hook Formulas (Proven)
```
1. "Stop doing X. Do Y instead."
2. "I made $X in Y days. Here's how."
3. "3 tools I use every day (free)"
4. "This one change increased my Z by 80%"
5. "I tested X for 30 days. Results:"
6. "The trick nobody talks about"
7. "{Thing} is dead. Here's what works now."
8. "Copy this exact workflow"
9. "Most people waste hours on X"
10. "Free tool that replaced my $Y/mo subscription"
```

### CTA Library
```
COMMENT-BASED:
- "Comment 'TOOL' and I'll DM the link"
- "Comment 'GUIDE' for the free template"
- "Comment your niche - I'll reply with a custom tip"

BIO-BASED:
- "Link in bio for the full breakdown"
- "Free guide in bio"
- "Full tutorial linked above"

DM-BASED:
- "DM me 'START' for the step-by-step"
- "DM for the exact template I use"
```

---

## 2.2 LONG-FORM CONTENT

### Platform Breakdown

| Platform | Best For | Frequency | Monetization |
|----------|----------|-----------|--------------|
| YouTube | SEO, authority | 1-2x/week | Adsense, sponsors, affiliates |
| Podcast | Trust, depth | 1x/week | Sponsors, course sales |
| Blog/SEO | Long-tail traffic | 2-4x/month | Affiliates, lead gen |
| Substack | Email list | 1-2x/week | Paid subs, course upsells |

### Content Pillars (Per Niche)

**AI/Productivity Niche:**
1. Tool reviews & comparisons
2. Automation tutorials
3. Workflow breakdowns
4. "Day in the life" productivity
5. Tool updates & news

**Faith Niche:**
1. Daily devotional content
2. Scripture application
3. Habit building (faith context)
4. Community/accountability
5. App/tool recommendations

**Fitness Niche:**
1. Workout breakdowns
2. Nutrition simplified
3. Recovery protocols
4. Progress tracking
5. Gear reviews

---

## 2.3 UGC & CREATIVE

### Sourcing Options

**Tier A: AI-Generated**
- **HeyGen** - $24/mo, AI avatars
- **Synthesia** - $30/mo, AI presenters
- **D-ID** - $4.70/min, talking photos
- **Veed.io** - Free tier, AI avatars

**Tier B: Cheap Human UGC**
- **Eastern European creators** - $3-20/video
  - @dansugcmodels (X) - DM for roster
  - @franci__ugc (X) - $3-10/video
  - Search #prettyukraine on IG/TikTok
- **Fiverr UGC** - $30-100/video
- **Billo** - $99+ per video
- **Trend** - $100+ per video

**Tier C: Hybrid AI + Human**
- Use Zeely or similar for face swaps
- Real voice + AI face (or vice versa)
- Most cost-effective for scale

### UGC Script Structure
```
HOOK (0-3 sec):
"[Problem statement]"
OR "[Result tease]"
OR "[Pattern interrupt]"

BRIDGE (3-10 sec):
"I was dealing with X..."
"Then I found Y..."

BODY (10-25 sec):
"Here's what it does..."
"Step 1... Step 2... Step 3..."

CTA (25-30 sec):
"Link in bio"
"Comment [word] for the link"
```

### Costs Summary
| Type | Cost Per Video | Quality |
|------|----------------|---------|
| AI Avatar | $1-5 | MEDIUM |
| Eastern EU UGC | $3-20 | HIGH |
| Fiverr UGC | $30-100 | VARIES |
| Professional UGC | $100-500 | HIGHEST |

---

# SECTION 3: PAID ADVERTISING

## 3.1 META (Facebook/Instagram)

### Minimum Viable Setup
- Business Manager account
- Pixel installed on landing
- $10-20/day starting budget

### Campaign Structure
```
Campaign: Conversions
  Ad Set 1: Broad (interests)
    Ad 1: UGC Video
    Ad 2: Static Image
    Ad 3: Carousel
  Ad Set 2: Lookalike (email list)
    Ad 1-3: Same creatives
  Ad Set 3: Retargeting
    Ad 1-3: Testimonial focus
```

### Budget Guidelines
| Phase | Daily Budget | Goal |
|-------|-------------|------|
| Testing | $10-20/day | Find winning creative |
| Scaling | $50-100/day | Optimize for conversions |
| Growth | $200+/day | Scale winners |

---

## 3.2 TIKTOK ADS

### Minimum Viable Setup
- TikTok Business account
- Pixel on landing page
- $20/day minimum budget

### Best Practices
- Use native-looking UGC (not polished)
- Hook in first 0.5 seconds
- Use trending sounds when possible
- 9:16 format only

### Budget Guidelines
| Phase | Daily Budget | Notes |
|-------|-------------|-------|
| Testing | $20-50/day | Minimum $500/campaign |
| Scaling | $100-500/day | Spark Ads perform well |

---

## 3.3 GOOGLE/YOUTUBE ADS

### Campaign Types
- Search: High intent, expensive
- Display: Cheap, low quality
- YouTube: Best for awareness + retargeting

### For PrintMaxx Niches
- Focus on YouTube In-Stream (skippable)
- Target competitor keywords
- Use discovery ads for tutorials

---

## 3.4 INFLUENCER/CREATOR PARTNERSHIPS

### Paid Placement Strategy

**Micro-Influencers (1K-10K followers)**
- Cost: $50-200/post
- Best ROI for niche products
- DM directly, negotiate

**Mid-Tier (10K-100K)**
- Cost: $200-1000/post
- Use platforms: Collabstr, Grin, Aspire
- Higher reach, still affordable

**Strategic Accounts to Pay for Promotion**

For AI/Productivity:
- Newsletter sponsorships (Morning Brew, TLDR)
- YouTube sponsor segments
- Podcast mentions

For Faith:
- Church partnerships (offer rev share)
- Christian influencer placements
- Ministry newsletter sponsorships

For Fitness:
- Fitness YouTuber segments
- Supplement brand partnerships
- Gym influencer posts

---

# SECTION 4: STRATEGIC OUTREACH IDEAS

## 4.1 VERTICAL-SPECIFIC PLAYS

### Prayer App → Church Distribution

**The Play:**
1. Scrape all churches in US with websites
2. Filter by: modern website, no existing app, congregation size >200
3. Offer: Free app for parishioners, discount for church, % of premium revenue to church
4. Outreach: Email pastor + follow up with phone

**Tools:**
- BuiltWith (filter by church CMS)
- Apollo (pastor emails)
- Google Maps API (church locations)

**Template:**
```
Subject: Digital ministry tool for [Church Name]

Pastor [Name],

Noticed [Church Name] doesn't have a dedicated app for your congregation yet.

We built a daily Scripture + prayer app specifically for churches.
Offering it free to your members with your church branding.

For every premium upgrade, 20% goes directly to your ministry fund.

Happy to show you a demo - 15 minutes max.

[Name]
```

### AI Tool → Specific Tech Stack

**The Play:**
1. Use BuiltWith to find companies using specific tools
2. Filter by: using competitor tool, company size 10-100
3. Position: "Better alternative for [tool]"

**Template:**
```
Subject: Noticed you're using [Competitor]

Hey [Name],

Saw [Company] uses [Competitor] for [function].

We help teams using [Competitor] cut [time/cost] by [%].
Just helped [Similar Company] do exactly this.

Worth a 15-min look?

[Name]
```

### Fitness Product → Gym Owners

**The Play:**
1. Scrape gym listings (Yelp API, Google Maps)
2. Filter by: independent gyms, <500 reviews (not chains)
3. Offer: Bulk discount for members, co-branding opportunity

---

## 4.2 TIMING-BASED OUTREACH

### Funding Trigger
- Monitor: Crunchbase, TechCrunch
- Timing: 1-2 weeks after funding announcement
- Angle: "Congrats on the round - here's how to deploy some of that budget"

### Hiring Trigger
- Monitor: LinkedIn job postings, Indeed
- Timing: When they're hiring for role your product replaces
- Angle: "Saw you're hiring for X - our tool does that for 1/10th the cost"

### Bad Review Trigger
- Monitor: G2, Capterra, App Store
- Timing: When competitor gets bad reviews
- Angle: "Saw your review of [Competitor] - we solve exactly that problem"

---

# SECTION 5: TOOL & SERVICE DIRECTORY

## 5.1 COLD EMAIL STACK

| Category | Tool | Cost | Notes |
|----------|------|------|-------|
| Platform | Instantly | $30/mo | Best starter |
| Platform | Smartlead | $39/mo | Unlimited inboxes |
| Platform | EmailBison | $49/mo | Good API |
| Platform | Lemlist | $39/mo | Personalization |
| Inbox Provider | DeliverOn | $49/mo | Pre-warmed |
| Inbox Provider | Mailforge | $3/inbox | Bulk inboxes |
| Warmup | Warmbox | $15/mo | Warm existing |
| Leads | Apollo | Free→$49/mo | Best free tier |
| Leads | Hunter | Free→$49/mo | Email finder |
| Leads | LinkedIn Sales Nav | $80/mo | Highest quality |
| Verification | NeverBounce | $8/1000 | Clean lists |

## 5.2 LINKEDIN STACK

| Category | Tool | Cost | Notes |
|----------|------|------|-------|
| Account | LinkedIn Premium | $60/mo | InMail credits |
| Account | Sales Navigator | $80/mo | Best for B2B |
| Automation | Dux-Soup | $15/mo | Simple, safe |
| Automation | Expandi | $99/mo | Cloud, safer |
| Automation | Waalaxy | Free→$30/mo | Newer, good |
| Data | Phantombuster | $30→$100/mo | Scraping |

## 5.3 CONTENT CREATION STACK

| Category | Tool | Cost | Notes |
|----------|------|------|-------|
| AI Copy | Claude | $20→$200/mo | Primary |
| AI Images | Leonardo | Free→$20/mo | Best quality |
| AI Images | Ideogram | Free→$20/mo | Text-in-image |
| AI Video | Veo/Flow | Free→Paid | Google's tool |
| Video Edit | CapCut | Free | Best for shorts |
| Design | Canva | Free→$13/mo | Graphics |
| AI Avatar | HeyGen | $24/mo | Talking head |
| AI Avatar | Synthesia | $30/mo | Professional |
| Voice | ElevenLabs | Free→$20/mo | Voice clone |

## 5.4 AUTOMATION STACK

| Category | Tool | Cost | Notes |
|----------|------|------|-------|
| Workflows | n8n (self-hosted) | $0 | Best for devs |
| Workflows | Make | $9→$16/mo | Visual |
| Workflows | Zapier | $20/mo | Easiest |
| Hosting | Hetzner | €5/mo | VPS |
| Browser | Playwright | $0 | Bulk engine |
| Browser | Puppeteer | $0 | Alternative |
| Scheduling | Cron/Launchd | $0 | Local |

## 5.5 MULTI-ACCOUNT STACK

| Category | Tool | Cost | Notes |
|----------|------|------|-------|
| Anti-detect | GoLogin | Free→$99/mo | Start here |
| Anti-detect | Multilogin | $99/mo | Enterprise |
| Proxies | Decodo | $50/mo | Residential |
| Proxies | SOAX | $50/mo | Alternative |
| Proxies | Oxylabs | $50/mo | Backup |
| Phone | SMSPool | $5-10 | Verification |
| Phone | TextNow | Free | Basic |

## 5.6 AI CALLING STACK

| Category | Tool | Cost | Notes |
|----------|------|------|-------|
| AI Caller | Bland.ai | $0.09/min | Best |
| AI Caller | Synthflow | $30/mo | Simple |
| AI Caller | Vapi.ai | $0.05/min | Developer |
| AI Caller | Retell.ai | $0.10/min | Good quality |
| Power Dialer | PhoneBurner | $149/mo | Human callers |
| VoIP | OpenPhone | $15/mo | Multiple lines |

---

# SECTION 6: HIGH-SIGNAL SOURCES (Auto-Research Targets)

## 6.1 X ACCOUNTS TO MONITOR

**Solopreneur/Indie Hackers:**
- @levelsio - pure signal, numbers
- @tdinh_me - technical depth
- @dannypostmaa - honest takes
- @marc_louvion - structured how-tos
- @paborojek - AI tools
- @yaborojek - growth hacks

**Cold Email/Outbound:**
- @caiden_cole - email deliverability
- @alexberman - outbound tactics
- @jaborojek - B2B sales

**Content/Growth:**
- @GrammarHippy - viral hooks
- @dickiebush - content systems
- @nicolascole77 - writing systems

**AI/Automation:**
- @godofprompt - prompt engineering
- @mcaborojek - AI apps
- @minchoi - AI tools

## 6.2 REDDIT COMMUNITIES

- r/SideProject
- r/EntrepreneurRideAlong
- r/juststart
- r/Emailmarketing
- r/coldemail
- r/indiehackers
- r/SaaS

## 6.3 NEWSLETTERS

- TLDR (daily tech)
- Morning Brew (business)
- Indie Hackers newsletter
- Product Hunt daily
- Ben's Bites (AI)

## 6.4 YOUTUBE CHANNELS

- My First Million clips
- Greg Isenberg
- Simon Hoiberg
- Fireship (tech trends)

---

# SECTION 7: WINNING STRUCTURES

## 7.1 THUMBNAIL FORMULAS

**For Tutorial Content:**
- Face + Text overlay + Tool screenshot
- High contrast colors (yellow/black, red/white)
- Numbers in title ("3 Steps", "$10K")

**For Results Content:**
- Dashboard screenshot + reaction face
- Dollar amounts visible
- Before/after split

## 7.2 CAPTION STRUCTURES

**Hook → Problem → Solution → CTA**
```
Most people waste 3 hours/day on [X].

Here's the 10-minute automation that fixed it:

Step 1: [Action]
Step 2: [Action]
Step 3: [Action]

Comment "AUTO" for the exact template.
```

**Story → Lesson → CTA**
```
6 months ago I was [situation].

Then I discovered [thing].

Now I [result].

Here's what I learned:

1. [Insight]
2. [Insight]
3. [Insight]

DM me "START" if you want the full breakdown.
```

## 7.3 EMAIL SUBJECT LINES (Proven)

**Cold Email:**
- "Quick question about [Company]"
- "Saw your [specific thing]"
- "[Mutual connection] suggested I reach out"
- "Idea for [their problem]"

**Newsletter:**
- "I made $X doing this (step-by-step)"
- "The tool I use every day (free)"
- "3 mistakes that cost me [X]"
- "Copy my exact [system]"

---

# SECTION 8: REVENUE PATH DECISION MATRIX

## When to Use What

| Revenue Goal | Best Path | Timeline | Upfront Cost |
|--------------|-----------|----------|--------------|
| $0-1K/mo | Content + affiliate | 2-4 months | $0-50 |
| $1K-5K/mo | Digital product + email | 1-3 months | $50-200 |
| $5K-10K/mo | Cold email + services | 1-2 months | $200-500 |
| $10K+/mo | All channels + team | 3-6 months | $500-2K |

## Quick Start by Situation

**"I have $200 and time"**
→ Content farm + digital product
→ Focus: X + TikTok + Gumroad
→ Timeline: 60-90 days to first sale

**"I have $500 and need revenue fast"**
→ Cold email + service offer
→ Focus: Apollo + Instantly + $500 offer
→ Timeline: 2-4 weeks to first client

**"I have an existing audience"**
→ Digital product + email
→ Focus: Launch to list + upsell
→ Timeline: 1-2 weeks to revenue

---

# SECTION 9: AGENT AUTO-RESEARCH PROMPT

Use this prompt to have Claude/agent scan for new alpha:

```
You are the PrintMaxx Intelligence Agent.

TASK: Scan these sources for new money-making tactics, tools, or strategies:

SOURCES:
1. X accounts: @levelsio, @tdinh_me, @dannypostmaa, @marc_louvion (last 7 days)
2. r/SideProject, r/EntrepreneurRideAlong (top posts this week)
3. Product Hunt (trending AI/automation tools)
4. Indie Hackers (recent launches with traction)

OUTPUT FORMAT:
For each finding:
- Source: [where you found it]
- Tactic/Tool: [what it is]
- Why it matters: [1-2 sentences]
- How to apply to PrintMaxx: [specific action]
- EV estimate: [Low/Medium/High]
- Effort: [Low/Medium/High]

FILTER: Only include if:
- It's new (not already in our playbook)
- It's actionable within $200-$500 budget
- It has proof of working (numbers, testimonials)

OUTPUT: 5-10 actionable findings
```

---

# SECTION 10: WEEKLY INTELLIGENCE ROUTINE

## Monday: Scan
- Run auto-research agent
- Check trending on ProductHunt
- Review X timeline for new tactics

## Wednesday: Test
- Implement 1 new tactic from research
- A/B test 2 content variations
- Review email campaign metrics

## Friday: Analyze
- Update this doc with findings
- Kill losers, scale winners
- Queue weekend content

---

# SECTION 11: ADULT/NSFW REVENUE METHODS (LEGAL, DISCLOSED)

**Key Principle:** Full disclosure = no FTC issues. No deception.

## 11.1 AI Influencer (Disclosed)

**How it works:**
- Create AI-generated character/avatar
- Full disclosure in bio: "Fully AI-generated character - no real human"
- Disclosure in terms pre-subscription
- Monetize via tips, subscriptions, affiliate links

**Platforms:**
- **Fansly** - Less restrictive than OnlyFans
- **Character.AI** - Virtual character platform
- **Patreon** - Tiered subscriptions

**Compliance (non-negotiable):**
- Bio: "Virtual creator" / "AI-generated character"
- Pre-sub terms: Clear statement that no real human involved
- No deception = no FTC suits

## 11.2 Animated NSFW

**Why it works:**
- Fully animated = no real human concerns
- Lower platform risk
- Still requires AI disclosure

**Tools:**
- Civitai models for generation
- ComfyUI workflows
- Fansly for monetization

**Disclosure:**
- "AI-generated art" in bio and posts
- No claims of being real human

## 11.3 Findom Waifu

**How it works:**
- Disclosed AI findom persona
- Clear fantasy framing
- Payment for "attention" from AI character

**Setup:**
- Character.AI or similar for chat
- Payment links via Ko-fi or similar
- Fantasy-only framing

**Disclosure:**
- "Your AI dom" / "Virtual findom character"
- Clear that this is entertainment/fantasy
- No claims of real human interaction

## 11.4 Study: Cluely's Compliance Edge

**What they do:**
- VC-backed company using AI influencers
- Formats that don't explicitly claim to be real
- Appear authentic but stay legally compliant

**What to copy:**
- Bio framing: "Virtual creator" not "I'm a real person"
- No fake testimonials from "real users"
- Affiliate disclosure where required

**Their safe patterns:**
- AI-generated spokesperson with disclosure
- Native-looking content that converts
- Rides the line of compliance

---

# SECTION 12: OVERNIGHT AGENT FRAMEWORK

**Purpose:** Run batch operations autonomously while you sleep.

## Human-in-Loop (REQUIRED)

Never automate:
- Payment decisions (>$50)
- Major architecture changes
- Publishing to production
- Account creation
- Anything with financial or legal implications

## Non-Human-in-Loop (SAFE TO AUTOMATE)

Run overnight:
- Content generation (longtails, social posts)
- Web scraping (tweets, competitor research)
- Code builds and tests
- Data processing and cleanup
- Email drafting (not sending)

## Tool: Ralph (github.com/snarktank/ralph)

**How it works:**
1. Define PRD with user stories
2. Ralph runs Amp agent in cycles
3. Each cycle: pick story → implement → test → commit
4. Fresh context per cycle prevents degradation
5. Knowledge persists via git + progress.txt

**Good for:**
- Batch content generation
- Multi-file code changes
- Overnight builds

**Limitations:**
- No built-in human approval gates
- Need to add payment/decision checkpoints manually
- Best for well-defined, non-critical tasks

## Alternative: Claude Code Cowork Mode

**How it works:**
- Run multiple Claude agents in parallel
- Each agent works on separate task
- Coordinate via shared files (LEDGER)

**Good for:**
- Parallel scraping jobs
- Content generation across niches
- Research and analysis

## Overnight Run Checklist

Before starting overnight run:
- [ ] Define clear scope and stopping conditions
- [ ] Remove any payment/credential access
- [ ] Set max_iterations limit
- [ ] Point outputs to staging (not production)
- [ ] Review first few outputs manually before sleeping

---

**LAST UPDATED:** 2026-01-20
**NEXT REVIEW:** 2026-01-27
