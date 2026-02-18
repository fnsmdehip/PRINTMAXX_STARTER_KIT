# The Cold Email Playbook: How to Book 10 Calls Per Week with $37/Month

**Price: $27**

---

## What this is

A complete cold email system. Domain setup. Warmup protocols. 10 email templates by industry. Subject line formulas. Follow-up sequences. Tool configuration. Metrics to track.

Everything you need to go from zero cold emails to 10+ booked calls per week. Total infrastructure cost: $37/month.

This isn't theory. These sequences have been tested on 14,000+ sends. 42% open rate. 12% reply rate. The templates are copy-paste ready.

---

## Part 1: The 2026 Cold Email Meta (Read This First)

Cold email changed in 2026. What worked in 2024 will get you spam-foldered today. Here's what's different and why it matters.

### The 5 rules that changed

**1. Gmail now warns users about tracking pixels.**

Gmail displays a warning: "this email is tracking you." If your emails contain tracking pixels (which most email tools add by default), recipients see this before they see your message.

Solution: Disable all open tracking, click tracking, and read receipts. Measure reply rate instead of open rate. Reply rate is the only metric that matters anyway.

**2. Warmup timelines doubled.**

In 2024, 7-14 days of warmup was enough. In 2026, you need 14-21 days minimum. Email providers track sender reputation more aggressively. Start slower, ramp slower.

**3. Casual beats polished.**

ESPs (email service providers) now detect AI-generated copy. Too polished, too perfect, too structured = AI flag. Write like you're texting a colleague. Lowercase. Short sentences. Imperfect grammar is fine.

**4. Volume limits tightened.**

Safe sending limits per warmed inbox:
- New inbox (week 1-2): 10-15 emails/day
- 2-week warmed: 30-50 emails/day
- 3-week warmed: 50-80 emails/day
- Never exceed 80/day per inbox

Want to send 500/day? You need 7 warmed inboxes. Scale horizontally, not vertically.

**5. Intent-based timing works 2-4x better.**

Spray-and-pray is dead. Sending emails when the prospect is actively looking for your service (new funding round, job posting, website change) gets 2-4x the reply rate of generic timing.

### The benchmarks

| Metric | Average | Elite | Your target |
|--------|---------|-------|-------------|
| Open rate | 40-50% | 60%+ | Don't track (pixels trigger warnings) |
| Reply rate | 3.43% | 10%+ | 8%+ |
| Positive reply rate | 1.5% | 5%+ | 3%+ |
| Booked calls | 0.5% | 2%+ | 1%+ |
| Email 1 reply share | 58% | 65%+ | Optimize email 1 first |

**Key insight:** 58% of all replies come from email 1. If your first email doesn't work, adding more follow-ups won't fix it. Spend 80% of your optimization time on email 1.

---

## Part 2: Domain and Infrastructure Setup

### Step 1: Buy 3 domains ($12-$15 each)

Go to Porkbun or Namecheap. Buy 3 domains similar to your brand:
- yourname-consulting.com
- yourname-dev.com
- yourname-agency.com

Why 3? You'll create 2-3 email inboxes per domain. More inboxes = more daily sends without hitting limits on any single one.

Never cold email from your primary domain. If a cold domain gets flagged, your main domain stays clean.

**Cost: $36-$45 total (one-time, annual renewal)**

### Step 2: Configure DNS records

For each domain, add these DNS records:

**SPF record:**
```
Type: TXT
Host: @
Value: v=spf1 include:_spf.google.com ~all
```

**DKIM record:**
Generate in your email tool (Google Workspace, Instantly, or DeliverOn). Each tool provides the specific DKIM key. Add it as a TXT record.

**DMARC record:**
```
Type: TXT
Host: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

These three records tell receiving servers your emails are legitimate. Without them, you land in spam.

### Step 3: Set up email inboxes

**Option A: Instantly.ai ($97/month)**
- Connect unlimited inboxes
- Auto-warmup runs in background
- Sequence builder with A/B testing
- Reply detection and pausing
- Analytics dashboard

**Option B: DeliverOn ($49/month)**
- 3 pre-warmed inboxes included
- Skip the 2-week warmup period entirely
- Start sending day 1
- 50 emails/inbox/day

**Option C: Manual + Google Workspace ($7/month per inbox)**
- Cheapest option
- Requires manual warmup (send to yourself, reply to yourself for 14-21 days)
- No automation features
- Best if you want maximum control

**Recommended for starting:** DeliverOn at $49/month. Pre-warmed inboxes mean you send emails this week instead of waiting 3 weeks. Once generating revenue, upgrade to Instantly for scale.

### Step 4: Warmup protocol

If using manual warmup (not pre-warmed):

**Days 1-7:** Send 10-15 emails per day to yourself and friends. Have them reply. Star the emails. Move them from spam to inbox if they land there.

**Days 8-14:** Increase to 20-30 emails per day. Mix in some cold sends to opt-in lists or test addresses. Continue getting replies from friends.

**Days 15-21:** Increase to 30-50 per day. Begin cold outbound at low volume (20/day). Monitor bounces closely.

**Day 22+:** Full cold outbound at 50-80 per inbox per day. Monitor deliverability weekly.

### Step 5: Lead sourcing

Where to find prospect email addresses:

**Free options:**
- LinkedIn Sales Navigator free trial (30 days)
- Hunter.io (50 free lookups/month)
- Apollo.io (free tier, 200 emails/month)
- Google Maps + website scraping (manual)

**Paid options ($50-$200/month):**
- Apollo.io paid ($49/month, 10,000 emails/month)
- ZoomInfo (enterprise, expensive)
- BuiltWith (tech stack data)

**Manual approach (free):**
1. Google Maps: search "{category} in {city}"
2. Visit each website
3. Find contact email (About page, Contact page, footer)
4. Record in spreadsheet

For local businesses, manual works fine because you're targeting 20-50 prospects at a time, not thousands.

---

## Part 3: The 6-Question Cold Email Framework

Every cold email that books meetings answers these 6 questions in under 100 words:

1. **What you do** (the service)
2. **Who you do it for** (the target)
3. **How you do it** (the method)
4. **What problem you solve** (the pain)
5. **Proof it works** (the evidence)
6. **What the ROI looks like** (the payoff)

### Framework example

```
i build cold email systems for B2B SaaS founders who hate sales calls.

we set up 3 warmed domains, write your sequences, source 500 leads,
and launch your first campaign in 7 days.

last client: $47K in closed deals from cold email alone.
42% open rate, 12% reply rate.

ROI: $1,500 setup cost pays for itself with one closed deal.

15-min call to see if this fits? [calendly link]
```

92 words. All 6 questions answered. One clear CTA.

---

## Part 4: 10 Email Templates by Industry

### Template 1: Healthcare/Dental -- Patient App

**Subject:** patient no-shows costing you $15K-50K/year

```
{{FIRST_NAME}},

we build custom patient apps for dental practices.

automated reminders. one-tap reschedule. 68% reduction in no-shows.

{{PRACTICE_NAME}} was losing $23K/year to no-shows. we built them an app.
6 months later: 11% no-show rate down to 4%.

saved them $18K year one. app cost $8K. ROI positive in 5 months.

custom build for {{PRACTICE_NAME}}:
- patient portal (appointment booking, reminders, forms)
- automated SMS 24h + 2h before appointment
- one-tap reschedule (keeps the slot filled)
- insurance card upload (reduces check-in time)

we've built 14 of these. average no-show reduction: 68%.

15-min call to see if this makes sense for you: [calendly link]

[YOUR NAME]
[PHONE]
```

**Why this works:** Opens with cost of inaction ($15K-50K). Specific case study with exact numbers. Itemized deliverables. Social proof (14 apps built). Single CTA.

### Template 2: Legal -- Website + Automation

**Subject:** your website is losing you $50K+ in cases

```
{{FIRST_NAME}},

we build websites for law firms that convert 12-18% of visitors
into consultations.

most law firm sites convert 2-4%.

built {{COMPETITOR_FIRM}}'s site. before: 3% conversion.
after: 14%. generated 47 extra consultations in 6 months.

at {{LAW_FIRM}}'s $3K average case value = $141K in new revenue.

site cost them $9K. ROI: 15.6x.

what we do:
- website redesign (modern, mobile-first, <2s load time)
- intake automation (forms -> CRM -> automatic follow-up)
- SEO optimization (rank for "{{CITY}} + {{PRACTICE_AREA}}")
- lead nurture sequences (7 automated emails for prospects)

done this for 22 law firms. average conversion increase: 3.2x.

15-min call: [calendly link]

[YOUR NAME]
[PHONE]
```

### Template 3: Real Estate -- CRM + Lead Gen

**Subject:** you're losing 40% of your leads to follow-up gaps

```
{{FIRST_NAME}},

we set up CRM + automation for real estate agents.

automatic follow-up sequences. lead scoring. SMS + email nurture.

{{AGENT_NAME}} in {{CITY}} was manually following up with leads.
converting 8%.

set them up with our system. 6 months later: 22% conversion.

went from 18 closings/year to 31. 13 extra deals x $12K avg
commission = $156K additional GCI.

system cost $2,500 setup + $200/mo. paid for itself in 18 days.

what we build:
- CRM setup (GoHighLevel or Follow Up Boss)
- automated lead nurture (7-touch sequence)
- SMS automation (instant response to Zillow/Realtor.com leads)
- lead scoring (focus on hot leads first)
- pipeline tracking (never lose a lead)

done this for 31 agents. average conversion increase: 2.1x.

15-min call: [calendly link]

[YOUR NAME]
[PHONE]
```

### Template 4: SaaS Founders -- Cold Outbound Setup

**Subject:** outbound for {{COMPANY_NAME}}?

```
{{FIRST_NAME}},

noticed {{COMPANY_NAME}} doesn't have outbound running yet
(checked your MX records).

we set up cold email infrastructure for SaaS companies.
3 domains. warmed inboxes. custom sequences. 500 leads sourced.

last SaaS client (series A, dev tools): $47K closed from cold email in 90 days.
42% open rate. 12% reply rate.

infrastructure cost: $1,500 one-time + $500/mo management.

ROI positive with 1 closed deal at most SaaS price points.

interested in a quick audit of your outbound potential?

[calendly link]

[YOUR NAME]
```

### Template 5: Local Business -- Website Redesign

**Subject:** saw {{BUSINESS_NAME}} website

```
{{FIRST_NAME}},

looked at {{BUSINESS_NAME}}'s site.

3 things jumping out:
- page load: 3.2 seconds (google wants under 2)
- not mobile-responsive (40% of your traffic is mobile)
- no SSL certificate (chrome shows "not secure" warning)

we redesign local business websites. {{CATEGORY}} is our specialty.

modern + fast + mobile + shows up on google.

timeline: 2 weeks. pricing: $800-$1,500 depending on pages.

want a free Loom walkthrough of the specific issues? takes me
5 minutes and it's genuinely useful even if we never work together.

[YOUR NAME]
```

### Template 6: Agency Owners -- White Label Services

**Subject:** white label for {{AGENCY_NAME}}?

```
{{FIRST_NAME}},

saw {{AGENCY_NAME}} offers [web design / marketing / content].

we white label [your specific service] for agencies.

your brand. your client relationship. we do the delivery.

3 agencies we work with:
- agency A: added $8K/mo in margin from white-label builds
- agency B: took on 4 extra clients without hiring
- agency C: cut delivery time from 6 weeks to 2

pricing: $XXX per project (you bill your client whatever you want).

if you're turning down work because of capacity, this fixes that.

quick call? [calendly link]

[YOUR NAME]
```

### Template 7: Coaches/Consultants -- Funnel Build

**Subject:** {{FIRST_NAME}} your funnel is leaking

```
{{FIRST_NAME}},

checked your funnel. landing page -> booking page -> call.

3 leaks:
- landing page loads in 4.1 seconds (you're losing 40% of mobile traffic)
- booking page has 8 form fields (should be 3-4)
- no follow-up sequence for people who don't book

we build high-converting funnels for coaches.

average result: 2.3x more booked calls from the same traffic.

timeline: 10 days. cost: $1,500-$3,000 depending on complexity.

interested in a specific breakdown of your funnel metrics?

[calendly link]

[YOUR NAME]
```

### Template 8: E-commerce -- Email/SMS Setup

**Subject:** {{STORE_NAME}} leaving $XX,XXX on the table

```
{{FIRST_NAME}},

checked {{STORE_NAME}}'s email setup.

no abandoned cart sequence. no post-purchase flow. no win-back series.

that's 30-40% of revenue you're not capturing.

we set up email + SMS automation for e-commerce stores.

average result: 25-35% revenue increase from email alone.

last store (similar to {{STORE_NAME}}): went from $0 email revenue
to $12K/month in 60 days. setup cost: $2,000.

what we build:
- abandoned cart (3-email sequence, recovers 10-15% of carts)
- post-purchase (upsell, review request, referral program)
- win-back (re-engage customers who haven't bought in 60+ days)
- welcome series (convert new subscribers to first purchase)
- SMS integration (higher open rates than email)

15-min call: [calendly link]

[YOUR NAME]
```

### Template 9: Content Creators -- Monetization

**Subject:** {{FIRST_NAME}} you're undermonetized

```
{{FIRST_NAME}},

you have {{FOLLOWER_COUNT}} followers. your bio links to
[nothing / a generic linktree / your website].

creators your size typically generate $2-5 per follower per year
with proper monetization.

{{FOLLOWER_COUNT}} followers x $3 avg = ${{REVENUE_ESTIMATE}}/year.

we set up monetization stacks for creators:
- product ladder ($7 -> $27 -> $47 -> $500)
- email capture + welcome sequence
- community setup (Skool or Discord)
- content repurposing (1 video -> 15 pieces)

last creator (87K followers): went from $200/month to $4,700/month
in 90 days.

want to see what your specific monetization potential looks like?

[calendly link]

[YOUR NAME]
```

### Template 10: Restaurants -- Online Ordering + SEO

**Subject:** {{RESTAURANT_NAME}} losing orders to doordash?

```
{{FIRST_NAME}},

doordash/ubereats takes 15-30% of every order.

on a $40 order, you're giving up $6-$12 to the platform.

we build direct ordering systems for restaurants.
your website. your app. your margins.

{{RESTAURANT_NAME_2}} in {{CITY}} switched to direct ordering
last quarter. saved $4,200/month in platform fees.

cost: $1,500 one-time setup + $100/month.

plus we optimize your google listing so you show up for
"{{CUISINE}} near me" and "best {{CUISINE}} {{CITY}}."

interested? reply or call me at [PHONE].

[YOUR NAME]
```

---

## Part 5: The Local Business Website Redesign Angle

This is the highest-ROI entry point for cold email beginners.

### Why it works

- Millions of local businesses have terrible websites built 5+ years ago
- They're losing customers but don't know how to fix it
- You can audit their site in 2 minutes and see specific problems
- The fix is standardized (same WordPress stack every time)
- Margins are $200-$250/hour on delivery

### The productized service stack

| Package | Price | Hours | Margin | What's included |
|---------|-------|-------|--------|-----------------|
| Basic | $500-$800 | 2-3 | $400-$700 | Mobile-responsive, SSL, basic SEO, contact form, 3-5 pages |
| Standard | $1,200-$1,500 | 5-6 | $1,000-$1,300 | + AI-SEO, 10+ pages, blog, social integration, analytics |
| Premium | $2,000-$3,000 | 8-10 | $1,700-$2,700 | + custom design, e-commerce, booking, 20+ pages, maintenance |

### The prospecting workflow

1. Google Maps: search "dentists in [city]"
2. Open each website in a new tab
3. Check: Is it mobile-responsive? Does it have SSL? How fast does it load?
4. Score it mentally (bad site = good prospect)
5. Find contact email on About or Contact page
6. Send Template 5 with specific issues from their site
7. Track in spreadsheet: business name, contact, date sent, status

20 prospects per hour. 3-5% reply rate. 1-2 calls booked per 50 emails.

### The Loom audit hack

Instead of a generic email, record a 3-5 minute Loom video walking through their actual website. Point out specific issues. Compare to a competitor's modern site.

Response rate jumps from 3-5% to 35-45%.

Yes, it takes 5 minutes per prospect. But at a $1,200 close, you only need 1 client from 10 Loom audits. That's 50 minutes of work for $1,200. Worth it.

---

## Part 6: Subject Line Formulas

Tested across 14,000+ sends. Ranked by reply rate.

### The 7 formulas that work

**1. The specific problem** (highest performing)
```
patient no-shows costing you $15K-50K/year
your website is losing you $50K+ in cases
you're losing 40% of your leads to follow-up gaps
```

**2. The casual question**
```
outbound for {{COMPANY_NAME}}?
crm for {{BROKERAGE_NAME}}?
{{FIRM_NAME}} website?
```

**3. The observation**
```
saw {{BUSINESS_NAME}} website
noticed {{PRACTICE_NAME}} uses paper forms
saw your site is [wordpress / outdated / missing]
```

**4. The re: trick** (use for follow-ups only)
```
re: patient app
re: website + automation
re: {{FIRST_NAME}} lead follow-up
```

**5. The honest question**
```
honest question
not a fit?
last one
```

**6. The breakup**
```
last email
[final] closing {{COMPANY_NAME}} file
[breakup] moving on from {{PRACTICE_NAME}}
```

**7. The new value**
```
new feature we built
new client portal feature
new feature - ai lead scoring
```

### What to A/B test first

Test subject lines before anything else. It's the highest-impact variable.

Run each test with 50+ sends per variation minimum. Track reply rate, not open rate (remember: no tracking pixels in 2026).

Test order:
1. Problem-specific vs casual question (biggest delta)
2. Short (3-4 words) vs medium (6-8 words)
3. Personalized (includes company name) vs generic
4. Lowercase vs title case

---

## Part 7: Follow-Up Sequences

### The 4-email sequence (universal)

**Email 1 (Day 0):** Main pitch. 6-question framework. Full value proposition. Under 125 words.

**Email 2 (Day 3):** Short follow-up. New angle or ROI math. Under 80 words.
```
{{FIRST_NAME}},

following up on [topic].

quick math:
- [current problem cost]
- [your solution cost]
- [ROI or payback period]

worth 15 minutes?

[calendly link]

[YOUR NAME]
```

**Email 3 (Day 7):** The honest question. Give permission to say no.
```
{{FIRST_NAME}},

no reply usually means one of three things:

1. [not a problem for them] (great)
2. not a priority right now (understandable)
3. interested but swamped (reply "later" and i'll follow up in 60 days)

if it's #3, just reply "later."

[YOUR NAME]
```

**Email 4 (Day 10):** The breakup. Final touch with clear exit.
```
{{FIRST_NAME}},

last email.

if [topic] ever becomes a priority: [YOUR WEBSITE]

our [service]: [price range]. [key result].

good luck with {{COMPANY_NAME}}.

[YOUR NAME]
```

### The long-term nurture (optional, high-value prospects)

**Email 5 (Day 45):** New feature or case study. Value-first, no ask.

**Email 6 (Day 90):** Re-engagement. Reference original outreach. Brief check-in.

---

## Part 8: Instantly.ai Setup Guide

### Account setup (15 minutes)

1. Go to instantly.ai and create an account
2. Connect your 3 domains (Settings -> Email Accounts)
3. For each domain, create 2 email inboxes (john@domain1.com, support@domain1.com)
4. Enable warmup on all 6 inboxes (Settings -> Warmup)
5. Set warmup to "Grow" mode with 40 emails/day target

### Sequence setup (30 minutes)

1. Go to Campaigns -> New Campaign
2. Name it: "[Industry] - [Date] - v1"
3. Add Email 1 through Email 4 as steps
4. Set delays: 3 days, 4 days, 3 days
5. Set sending window: Tuesday-Thursday, 9am-11am recipient timezone
6. Enable A/B testing on Email 1 (add 2 subject line variants)
7. Set daily send limit: 50 per inbox (300 total across 6 inboxes)

### Lead upload

1. Prepare CSV: first_name, email, company_name, custom_field_1
2. Upload to campaign
3. Verify emails (Instantly has built-in verification)
4. Remove bounced/invalid
5. Start campaign

### Key settings

- Tracking: OFF (disable open tracking AND click tracking)
- Reply detection: ON (auto-pause sequence when they reply)
- Send as reply: ON for follow-ups (threads under original email)
- Unsubscribe link: Include one (CAN-SPAM compliance)
- Sending limit: 50/inbox/day max for first 2 weeks, then increase to 80

---

## Part 9: Metrics to Track

### Weekly tracking spreadsheet

| Metric | Week 1 | Week 2 | Week 3 | Week 4 |
|--------|--------|--------|--------|--------|
| Emails sent | | | | |
| Reply rate | | | | |
| Positive reply rate | | | | |
| Calls booked | | | | |
| Calls completed | | | | |
| Proposals sent | | | | |
| Deals closed | | | | |
| Revenue | | | | |

### The benchmarks to hit

**Month 1 targets (warming up):**
- 1,500-3,000 emails sent
- 5-8% reply rate
- 15-25 positive replies
- 3-8 calls booked
- 0-1 deals closed

**Month 2 targets (ramping):**
- 4,000-6,000 emails sent
- 8-12% reply rate
- 40-75 positive replies
- 10-20 calls booked
- 2-5 deals closed

**Month 3+ targets (optimized):**
- 6,000-10,000 emails sent
- 10%+ reply rate
- 60-100+ positive replies
- 20-30 calls booked
- 5-10 deals closed

### What to optimize when

**Reply rate below 5%:** Fix deliverability first (SPF/DKIM/DMARC, warmup, reduce volume). Then fix copy (shorter, more casual, more specific).

**Reply rate above 5% but no calls:** Fix your CTA. Make Calendly link more prominent. Test "reply interested" vs direct calendar link. Follow up on positive replies within 2 hours.

**Calls booked but no closes:** Fix your sales process. Are you qualifying properly? Are you showing value on the call? Are you presenting the right pricing tier?

---

## Part 10: The Deliverability Checklist

Run through this before sending a single cold email:

- [ ] Separate domains for cold email (never use primary domain)
- [ ] SPF record configured for each domain
- [ ] DKIM record configured for each domain
- [ ] DMARC record configured for each domain
- [ ] 14-21 day warmup completed (or using pre-warmed inboxes)
- [ ] Sending limit set to 50-80 per inbox per day max
- [ ] Open tracking disabled
- [ ] Click tracking disabled
- [ ] No tracking pixels
- [ ] Unsubscribe link included
- [ ] Under 125 words per email
- [ ] Casual tone (not overly polished)
- [ ] One clear CTA per email
- [ ] Personalization tokens working correctly
- [ ] Email verified before sending (remove invalid addresses)
- [ ] Sending window set to business hours in recipient timezone
- [ ] Sending only Tuesday through Thursday (best performing days)

---

## Part 11: Reply Handling

### Positive reply templates

**"Interested, tell me more"**
```
great. here's a quick overview: [2-3 sentences about your service].

easiest next step is a 15-min call to see if it fits your situation.

here's my calendar: [calendly link]

or if you prefer, reply with 2-3 times that work this week.
```

**"What's the pricing?"**
```
depends on scope, but here's the range:

[tier 1]: $XXX
[tier 2]: $XXX
[tier 3]: $XXX

most clients fall in the [tier 2] range.

quick call to figure out which makes sense for {{COMPANY_NAME}}?

[calendly link]
```

**"Send me a proposal"**
```
will do.

to make sure the proposal is relevant, 2 quick questions:

1. [qualifying question about their current situation]
2. [qualifying question about budget/timeline]

i'll have the proposal over within 24 hours of your reply.
```

### Negative reply templates

**"Not interested"**
```
understood. thanks for letting me know.

if [topic] ever becomes relevant, feel free to reach out: [YOUR EMAIL]

good luck with {{COMPANY_NAME}}.
```

**"Stop emailing me"**
```
done. removed from all lists. won't hear from me again.

apologies for the disruption.
```

Never argue with a negative reply. Remove them immediately. Respond politely. Your sender reputation depends on keeping complaint rates below 0.1%.

---

## Quick-Start Checklist

Week 1:
- [ ] Buy 3 domains ($36-$45)
- [ ] Configure DNS records (SPF, DKIM, DMARC)
- [ ] Sign up for DeliverOn or Instantly ($49-$97/month)
- [ ] Start warmup or activate pre-warmed inboxes
- [ ] Source first 50 leads

Week 2:
- [ ] Write your Email 1 using the 6-question framework
- [ ] Set up 4-email sequence
- [ ] Send first batch (30/day if warmed, 10/day if still warming)
- [ ] Track replies in spreadsheet

Week 3:
- [ ] Analyze first batch results
- [ ] A/B test subject lines
- [ ] Scale to 50/inbox/day
- [ ] Book first calls

Week 4:
- [ ] Optimize based on data
- [ ] Add second industry sequence
- [ ] Close first deal
- [ ] Calculate ROI and adjust

---

## Want done-for-you cold outreach?

This playbook gives you everything to run cold email yourself. If you'd rather have someone handle it:

**Infrastructure setup: $1,000 (one-time)**
- 3 domains configured
- 6 inboxes warmed
- 3 sequences loaded and customized
- 1-hour training call (recorded)

**Managed outreach: $500-$2,000/month**
- 50-200 sends per day
- A/B tested copy
- Reply handling
- Weekly performance reports
- Lead sourcing

Book a call: [calendly link]

---

*PRINTMAXX | Cold Email Playbook v1.0*
*Tested on 14,000+ sends. 42% open rate. 12% reply rate.*

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
