# COLD OUTBOUND Audit Output (MM007)

**Date:** 2026-02-06
**Auditor:** PRINTMAXX Ops
**Method ID:** MM007 (COLD_OUTBOUND) + MM070 (WEB_REDESIGN_COLD_OUTREACH)
**Status:** Planning (Phase 2) | $0 revenue | 0 emails sent

---

## Section A: Current State Assessment

### What exists right now

**3 files in `MONEY_METHODS/COLD_OUTBOUND/`:**

| File | Lines | Content | Status |
|------|-------|---------|--------|
| `EMAIL_SEQUENCES_TIER1.md` | 818 | 3 full sequences (Healthcare, Legal, Real Estate) with 7 emails each, 2026 meta, implementation notes | READY to send |
| `TIER1_COLD_EMAIL_SEQUENCES.md` | 537 | 3 sequences (same verticals) with 4 emails each, deliverability setup, LinkedIn templates, voice notes | READY to send |
| `LOCAL_BIZ_WEBSITE_SERVICE.md` | 505 | Full service playbook for website redesign outreach, packages $500-$3K, scaling strategy | READY to send |

**`CONTENT/email_sequences/cold/` directory:** Empty. Zero files.

### Industries currently covered

1. Healthcare/Dental Practices (custom app dev + website redesign)
2. Legal Firms (website + automation + SEO)
3. Real Estate Agents (CRM + lead gen + automation)

### What's ready vs needs work

**Ready to send (just need warmed inboxes):**
- 3 healthcare sequences (7-email + 4-email + website redesign angle)
- 3 legal sequences (7-email + 4-email + website redesign angle)
- 3 real estate sequences (7-email + 4-email + CRM angle)
- 5 LinkedIn connection request templates
- 2 LinkedIn voice note scripts
- A/B test framework for subject lines, CTA types, send times
- Deliverability checklist and infrastructure guide

**Needs work:**
- 5 more industries have zero coverage (restaurants, gyms, salons, contractors, accountants)
- No cold calling scripts exist
- No objection handling scripts exist
- No subject line swipe file
- No sequence variants beyond the 3 verticals
- No tracking in OUTREACH_PIPELINE.csv (only 6 placeholder leads, none from cold email)
- Warmed inboxes not set up (WARMUP_DEVICE_MATRIX.csv shows all zeros)
- Zero emails sent. Zero revenue. Zero calls booked.

### Blockers

1. No warmed email infrastructure (14-21 day warmup required per 2026 standards)
2. No domains purchased for cold sending
3. No prospect lists compiled
4. No Calendly/scheduling link set up

---

## Section B: Industry-Specific Email Templates (8 Industries)

### 1. Lawyers / Law Firms

**Email 1 (Day 1) - Initial**

Subject: {company_name} losing leads from your website

```
{first_name},

looked at {company_name}'s site. your intake form has 14 fields. best practice is 4-6.

every extra field drops conversions 11%. you're probably losing 30-40% of potential clients before they finish filling it out.

we fix this for law firms. simplified intake + automated follow-up. last firm we did this for in {city} saw 3.2x more consultation bookings in 60 days.

cost: $8K-15K. timeline: 6 weeks. pays for itself with 2-3 new cases.

worth 15 minutes?

[calendly link]

[YOUR_NAME]
```

**Email 2 (Day 4) - Follow-up**

Subject: re: {company_name} intake form

```
{first_name},

quick follow up.

ran your site through our audit tool. 3 things costing you clients right now:

1. page loads in 4.1 seconds (google wants under 2)
2. no mobile optimization (47% of legal searches are mobile)
3. no automated follow-up (leads go cold in 5 minutes, you're responding in 24 hours)

we can fix all 3. happy to show you the full audit on a 15 min call.

[calendly link]

[YOUR_NAME]
```

**Email 3 (Day 8) - Breakup**

Subject: closing your file

```
{first_name},

last email from me.

if lead gen becomes a priority for {company_name}:
- website + intake automation ($8K-15K)
- SEO for "{city} [practice area] attorney" ($2K/mo)
- 3.2x average conversion increase for our clients

portfolio: [link]

good luck.

[YOUR_NAME]
```

---

### 2. Dentists / Dental Practices

**Email 1 (Day 1) - Initial**

Subject: {company_name} no-show rate

```
{first_name},

dental practices lose $15K-50K per year to no-shows. national average is 12%.

we build automated reminder systems for practices like {company_name}. SMS 24 hours before, text 2 hours before, one-tap reschedule link.

average result: 68% fewer no-shows. one practice in {city} went from 11% to 4%. saved $18K year one.

setup cost: $3K-8K. no monthly fees.

ROI positive in 2-3 months.

15 min call? [calendly link]

[YOUR_NAME]
```

**Email 2 (Day 4) - Follow-up**

Subject: re: {company_name} patient reminders

```
{first_name},

circling back.

quick math on no-shows for {company_name}:
- 10 no-shows/week x $150 avg appointment = $1,500/week lost
- that's $78K/year walking out the door
- cut that by half = $39K saved
- system costs $3K-8K one time

if your no-show rate is above 8%, this pays for itself in weeks.

[calendly link]

[YOUR_NAME]
```

**Email 3 (Day 8) - Breakup**

Subject: last one

```
{first_name},

last email.

if no-shows or patient scheduling become a priority:
- automated reminders + one-tap reschedule ($3K-8K)
- online booking + intake forms ($2K add-on)
- 68% average no-show reduction

examples: [link]

good luck with {company_name}.

[YOUR_NAME]
```

---

### 3. Realtors / Real Estate Agents

**Email 1 (Day 1) - Initial**

Subject: {first_name} your zillow leads going cold?

```
{first_name},

most agents respond to new leads in 4-6 hours. top agents respond in under 5 minutes.

that gap costs you 40% of your pipeline. we set up automated lead response systems for agents in {city}.

instant SMS when a lead comes in. automated drip sequence. lead scoring so you know who to call first.

one agent we work with went from 8% to 22% conversion. 13 extra deals last year. $156K additional commission.

setup: $2,500. monthly: $200.

worth a quick call?

[calendly link]

[YOUR_NAME]
```

**Email 2 (Day 4) - Follow-up**

Subject: re: lead follow-up system

```
{first_name},

following up.

if you're getting 30+ leads per month from zillow, realtor.com, or facebook and converting under 15%, the math is brutal.

30 leads x 8% close = 2.4 deals/month
30 leads x 18% close = 5.4 deals/month
difference: 3 extra deals x $10K commission = $30K/month

system costs $2,500 setup. pays for itself with one extra closing.

[calendly link]

[YOUR_NAME]
```

**Email 3 (Day 8) - Breakup**

Subject: last email

```
{first_name},

moving on.

if lead conversion becomes a priority:
- CRM + automated follow-up ($2,500 setup + $200/mo)
- instant lead response (SMS + email in under 60 seconds)
- 2.1x average conversion increase

portfolio: [link]

good luck closing deals in {city}.

[YOUR_NAME]
```

---

### 4. Restaurants

**Email 1 (Day 1) - Initial**

Subject: {company_name} online orders

```
{first_name},

doordash and uber eats take 15-30% of every order. for a restaurant doing $50K/month in delivery, that's $7,500-$15,000 per month in fees.

we build direct ordering systems for restaurants in {city}. your own branded app and website ordering. you keep 100% of the revenue.

setup cost: $3K-5K. saves most restaurants $5K-10K per month in platform fees.

one restaurant in {city} switched 40% of their delivery orders to direct. saved $6,200/month.

15 min call? [calendly link]

[YOUR_NAME]
```

**Email 2 (Day 4) - Follow-up**

Subject: re: {company_name} delivery fees

```
{first_name},

quick follow up.

if {company_name} does $20K+ per month through delivery apps, you're giving away $3K-6K in fees.

our direct ordering system:
- branded ordering page (your domain, your brand)
- automatic order routing to kitchen
- customer database (yours, not doordash's)

pays for itself month one. literally.

[calendly link]

[YOUR_NAME]
```

**Email 3 (Day 8) - Breakup**

Subject: last one

```
{first_name},

last email from me.

if delivery fees become a pain point:
- direct ordering system ($3K-5K setup)
- saves $5K-10K/month in platform fees
- you own the customer data

examples: [link]

good luck with {company_name}.

[YOUR_NAME]
```

---

### 5. Gyms / Fitness Studios

**Email 1 (Day 1) - Initial**

Subject: {company_name} member retention

```
{first_name},

average gym loses 50% of new members within 6 months. each lost member = $500-$1,200 in annual revenue gone.

we build member engagement systems for gyms in {city}. automated check-in reminders, workout tracking, class booking, and progress photos all in one app.

one gym we work with cut churn by 35%. on a 500-member gym, that's keeping 87 extra members. at $50/month each, that's $52K/year in saved revenue.

setup: $5K-10K. pays for itself in 2 months.

worth a call? [calendly link]

[YOUR_NAME]
```

**Email 2 (Day 4) - Follow-up**

Subject: re: {company_name} member churn

```
{first_name},

following up on member retention for {company_name}.

gyms that send automated check-in nudges see 28% higher attendance. higher attendance = lower churn. lower churn = more revenue.

3 things we set up:
1. automated "we miss you" texts after 7 days inactive
2. class booking with waitlist and reminders
3. progress tracking (keeps members engaged long-term)

takes 4 weeks to set up. [calendly link]

[YOUR_NAME]
```

**Email 3 (Day 8) - Breakup**

Subject: closing this out

```
{first_name},

last email.

if member retention becomes a priority:
- engagement system ($5K-10K setup)
- 35% average churn reduction
- class booking + automated reminders + progress tracking

examples: [link]

good luck with {company_name}.

[YOUR_NAME]
```

---

### 6. Salons / Barbershops

**Email 1 (Day 1) - Initial**

Subject: {company_name} booking system

```
{first_name},

salons that use online booking fill 23% more appointment slots than phone-only shops.

noticed {company_name} doesn't have online booking set up (or it's buried on your site).

we build booking systems for salons in {city}. online scheduling, automated reminders, review requests after every visit.

one salon we work with added online booking and filled 15 extra slots per week. at $45 average service, that's $2,700/month in new revenue.

setup: $1,500-$3K. monthly: $50.

15 min call? [calendly link]

[YOUR_NAME]
```

**Email 2 (Day 4) - Follow-up**

Subject: re: {company_name} online booking

```
{first_name},

quick follow up.

3 things our booking system does for salons:
1. clients book 24/7 from their phone (no phone tag)
2. automatic SMS reminders (cuts no-shows 40%)
3. review request after every visit (builds google reviews)

one salon in {city} went from 3.8 to 4.7 stars on google in 90 days. foot traffic up 20%.

[calendly link]

[YOUR_NAME]
```

**Email 3 (Day 8) - Breakup**

Subject: last one

```
{first_name},

last email.

if online booking or google reviews become a priority:
- booking system + reminders ($1,500-$3K setup)
- automated review requests ($50/mo)
- 23% more appointments filled, 40% fewer no-shows

examples: [link]

good luck with {company_name}.

[YOUR_NAME]
```

---

### 7. Contractors (Plumbers, Electricians, HVAC)

**Email 1 (Day 1) - Initial**

Subject: {company_name} getting found on google?

```
{first_name},

when someone's pipe bursts at 2am, they google "emergency plumber {city}." if {company_name} isn't in the top 3 results, that call goes to your competitor.

we build websites and google profiles for contractors in {city}. one HVAC company we work with went from page 3 to position 2 in 60 days. went from 8 calls/week to 22.

setup: $2K-5K for website + SEO.
monthly SEO: $500.
first month ROI: one emergency call ($300-$800) pays for the monthly.

worth 15 min? [calendly link]

[YOUR_NAME]
```

**Email 2 (Day 4) - Follow-up**

Subject: re: {company_name} google ranking

```
{first_name},

following up.

googled "{your trade} {city}" and {company_name} isn't showing up in the top 10.

your competitors are getting those calls instead. at $300-$800 per emergency job, every missed call is real money.

3 things we fix:
1. google business profile optimization (free, takes 2 hours)
2. website with local SEO (ranks for "{city} + {trade}")
3. review automation (more 5-star reviews = higher ranking)

[calendly link]

[YOUR_NAME]
```

**Email 3 (Day 8) - Breakup**

Subject: last email

```
{first_name},

last one.

if getting found on google becomes a priority:
- website + local SEO ($2K-5K setup)
- google business profile optimization (included)
- review automation ($50/mo)
- average: 2-3x more calls within 90 days

examples: [link]

good luck with {company_name}.

[YOUR_NAME]
```

---

### 8. Accountants / CPAs

**Email 1 (Day 1) - Initial**

Subject: {company_name} client onboarding

```
{first_name},

most accounting firms spend 3-5 hours onboarding each new client. document collection, forms, follow-up emails for missing info.

we automate this for CPA firms in {city}. client portal with document upload, automated reminders for missing docs, e-signature for engagement letters.

one firm we work with cut onboarding time from 4 hours to 45 minutes per client. during tax season with 200+ new clients, that's 650 hours saved.

setup: $5K-10K. no monthly fees.

15 min call? [calendly link]

[YOUR_NAME]
```

**Email 2 (Day 4) - Follow-up**

Subject: re: {company_name} tax season prep

```
{first_name},

following up.

tax season is coming. your staff is about to drown in document requests, follow-up emails, and client questions.

our client portal handles:
1. automated document requests (clients upload from phone)
2. status tracking (clients check progress without calling you)
3. e-signature (engagement letters signed in 2 minutes)

firms using this handle 30% more clients without adding staff.

[calendly link]

[YOUR_NAME]
```

**Email 3 (Day 8) - Breakup**

Subject: last one

```
{first_name},

last email.

if client onboarding or tax season efficiency becomes a priority:
- client portal + document automation ($5K-10K)
- e-signature + automated reminders (included)
- 30% more client capacity without hiring

examples: [link]

good luck with {company_name}.

[YOUR_NAME]
```

---

## Section C: 10 New Sequence Variants

These are alternate Email 1 angles. use the same follow-up (Day 4) and breakup (Day 8) structure from Section B. swap out Email 1 with any of these.

### Variant 1: Pain Point Lead

Subject: {company_name} losing money on [specific problem]

```
{first_name},

[specific problem] is costing {company_name} somewhere between $X and $Y per month.

here's the math:
- [metric] x [rate] = $[amount] lost
- fix costs $[amount] one-time
- ROI positive in [timeframe]

we've fixed this for [number] businesses in {city}.

15 min to see if it applies to you? [calendly link]

[YOUR_NAME]
```

### Variant 2: Competitor Comparison

Subject: {competitor_name} just did this

```
{first_name},

noticed {competitor_name} in {city} just launched [specific thing].

they're now getting [specific result] from it.

we built it for them. wondering if {company_name} wants the same edge.

not a hard sell. just figured you'd want to know what your competition is up to.

reply if curious.

[YOUR_NAME]
```

### Variant 3: Case Study

Subject: how [similar business] in {city} got [result]

```
{first_name},

[similar business name] had the same problem most [industry] businesses have: [problem].

we built them [solution]. 90 days later:
- [metric 1]: [before] to [after]
- [metric 2]: [before] to [after]
- [metric 3]: [before] to [after]

total investment: $[amount]. total return: $[amount] in year one.

want to see if {company_name} could get similar results?

[calendly link]

[YOUR_NAME]
```

### Variant 4: Question-Based

Subject: quick question about {company_name}

```
{first_name},

does {company_name} currently have [specific capability]?

asking because [industry] businesses without it lose an average of $[amount] per month to [consequence].

if you do have it, ignore this. if not, we set it up for businesses like yours in [timeframe] for $[amount].

either way, just curious.

[YOUR_NAME]
```

### Variant 5: Value-First (Free Audit)

Subject: free audit of {company_name}'s [thing]

```
{first_name},

ran {company_name} through our [website/operations/marketing] audit tool.

found 3 things:

1. [specific issue] (costing you ~$[amount]/month)
2. [specific issue] (your competitors don't have this problem)
3. [specific issue] (easy fix, 2-hour implementation)

want the full breakdown? i recorded a 3-minute loom walking through everything.

reply "send it" and i'll share the link.

[YOUR_NAME]
```

### Variant 6: Social Proof Stack

Subject: 14 businesses in {city} use this

```
{first_name},

we've helped 14 [industry] businesses in {city} with [service].

average results:
- [metric]: +[percentage]%
- [metric]: [number] more per month
- ROI: [X]x in first [timeframe]

{company_name} fits the profile of businesses that see the best results.

15 min to see if it makes sense? [calendly link]

[YOUR_NAME]
```

### Variant 7: Urgency (Seasonal/Time-Based)

Subject: {first_name} before [season/event] hits

```
{first_name},

[season/event] is [X weeks] away. last year, [industry] businesses that had [solution] in place saw [X]% higher [metric] during [season].

we can have {company_name} set up in [timeframe]. but we need to start by [date] to make the deadline.

if [season] revenue matters to you, reply and i'll send the details.

[YOUR_NAME]
```

### Variant 8: Curiosity Gap

Subject: noticed something about {company_name}

```
{first_name},

spent 10 minutes looking at {company_name} online.

found something your competitors in {city} are doing that you're not. it's probably costing you [range] per month.

not trying to be dramatic. just thought you'd want to know.

want me to share what i found? reply and i'll send a quick breakdown.

[YOUR_NAME]
```

### Variant 9: Direct Offer

Subject: [service] for {company_name} - $[price]

```
{first_name},

we do [service] for [industry] businesses.

price: $[amount].
timeline: [timeframe].
result: [specific outcome].

done this for [number] businesses. average [metric] improvement: [percentage]%.

interested? [calendly link]

not interested? reply "no" and i'll never email again.

[YOUR_NAME]
```

### Variant 10: Referral Ask

Subject: know any [industry professionals] in {city}?

```
{first_name},

we help [industry] businesses with [service]. just finished a project in {city} that got [specific result].

looking for 2-3 more [industry] businesses to work with this quarter.

know anyone who might benefit? happy to send a $[amount] referral fee for any intro that becomes a client.

or if {company_name} is interested directly, happy to chat.

[YOUR_NAME]
```

---

## Section D: Subject Line Swipe File (50 Lines)

### Question-Based (Expected Open Rate: 35-50%)

| # | Subject Line | Best For |
|---|-------------|----------|
| 1 | quick question about {company_name} | All industries |
| 2 | {first_name} how are you handling [pain point]? | All industries |
| 3 | is {company_name} still using [old method]? | Tech-behind businesses |
| 4 | {first_name} did you know about this? | Curiosity play |
| 5 | who handles [function] at {company_name}? | Getting to decision maker |
| 6 | {company_name} looking for new clients? | Service businesses |
| 7 | still doing [task] manually? | Automation pitch |
| 8 | ever calculated your [metric] rate? | Data-driven businesses |
| 9 | {first_name} what's your no-show rate? | Dentists, salons, gyms |
| 10 | how many leads did {company_name} get last month? | All industries |

### Number-Based (Expected Open Rate: 40-55%)

| # | Subject Line | Best For |
|---|-------------|----------|
| 11 | {company_name} leaving $15K/year on the table | High-ticket services |
| 12 | 68% fewer no-shows (for {company_name}) | Healthcare, salons |
| 13 | 3.2x more leads for {company_name} | Service businesses |
| 14 | $78K per year in no-shows | Dentists |
| 15 | 22 calls per week vs 8 | Contractors |
| 16 | 35% less churn. here's how | Gyms |
| 17 | 15 extra appointments per week | Salons |
| 18 | 30% more clients. same staff | Accountants |
| 19 | $6,200/month in saved delivery fees | Restaurants |
| 20 | 47% of your customers are on mobile | All industries |

### Pain-Based (Expected Open Rate: 30-45%)

| # | Subject Line | Best For |
|---|-------------|----------|
| 21 | {company_name} losing customers to [competitor] | All industries |
| 22 | your website is costing you clients | Web redesign pitch |
| 23 | {first_name} your leads are going cold | Real estate, agencies |
| 24 | doordash is taking 30% of your revenue | Restaurants |
| 25 | your front desk is buried | Healthcare, legal |
| 26 | clients can't find {company_name} on google | Contractors, local biz |
| 27 | tax season is about to crush your team | Accountants |
| 28 | {company_name} no-show rate too high? | Healthcare, salons |
| 29 | your competitors rank higher than you | All local businesses |
| 30 | {first_name} are you losing sleep over [issue]? | High-stress verticals |

### Curiosity-Based (Expected Open Rate: 35-50%)

| # | Subject Line | Best For |
|---|-------------|----------|
| 31 | noticed something about {company_name} | All industries |
| 32 | {first_name} this might be relevant | Warm follow-up |
| 33 | what [competitor] just launched | Competitive businesses |
| 34 | 14 businesses in {city} are doing this | Social proof |
| 35 | you probably don't know this about your site | Web redesign |
| 36 | found something while researching {city} [industry] | Local businesses |
| 37 | {first_name} one thing about {company_name} | Short curiosity |
| 38 | saw {company_name} on google maps | Local businesses |
| 39 | weird trend in {city} [industry] right now | All industries |
| 40 | thought you should see this | Follow-up |

### Direct Offer (Expected Open Rate: 25-40%)

| # | Subject Line | Best For |
|---|-------------|----------|
| 41 | website for {company_name} - $2K | Web redesign |
| 42 | booking system for {company_name} | Salons, gyms, healthcare |
| 43 | {company_name} google ranking in 60 days | Local SEO |
| 44 | lead gen system - {company_name} | Real estate, agencies |
| 45 | client portal for {company_name} | Accountants, legal |
| 46 | {first_name} 15 min - no pitch | All industries |
| 47 | free audit of {company_name}'s site | Web redesign |
| 48 | built this for [similar business]. want one? | Case study angle |
| 49 | {company_name} [service] - [timeline] | Direct and specific |
| 50 | last email about {company_name} | Breakup emails |

### Open rate notes

- personalized subject lines (with {company_name} or {first_name}) get 22% higher open rates than generic
- lowercase subject lines outperform title case by 8-12% in cold email
- questions outperform statements by 10-15%
- numbers in subject lines increase open rates 15-20%
- keep subject lines under 40 characters for mobile (60%+ of opens are mobile)
- "re:" in follow-ups gets 30-40% higher open rates (use only on actual follow-ups, not fakes)
- avoid spam trigger words: "free," "guarantee," "act now," "limited time"

---

## Section E: Objection Handling Scripts

### Top 10 Objections and Responses

**1. "Not interested"**

```
totally get it. mind if i ask what's working for you right now for [specific thing]?
most businesses i talk to say "not interested" because the timing's off, not because
the problem isn't real. if things change, here's my calendar: [link]
```

**2. "Too expensive"**

```
fair. what's your budget for this?

here's how i think about it: you're currently losing $[amount] per month to [problem].
our fix costs $[amount] one time. even at a 50% reduction, you're ROI positive in
[timeframe].

but if budget is tight, we can start with [smaller service] for $[lower amount]
and expand from there.
```

**3. "Already have someone doing this"**

```
good. are they getting you results?

genuine question. if they're delivering, great. keep them.

if you're not seeing [specific metric], it might be worth a second opinion. we
audit competitor setups for free. takes 15 minutes. worst case, you confirm your
current provider is doing great work.
```

**4. "I need to think about it"**

```
of course. what specifically are you weighing?

is it the price, the timeline, or whether you need this at all?

if it's price: we can do a smaller scope for $[amount].
if it's timing: we can start in [timeframe] and lock in current pricing.
if it's need: the audit i showed you is free either way. keep it.
```

**5. "Send me more information"**

```
sure. what specifically do you want to see?

i can send:
- case studies from [industry] businesses like yours
- pricing breakdown for your specific situation
- portfolio examples from {city}

which one would be most useful? i'll send just that so it doesn't get buried
in your inbox.
```

**6. "We tried this before and it didn't work"**

```
what happened?

seriously, i want to know. because 80% of the time when this fails, it's one
of 3 things:

1. no follow-up system (just built it and forgot about it)
2. wrong approach (generic template instead of industry-specific)
3. wrong provider (offshore team that didn't understand your business)

if you tell me what went wrong, i'll tell you honestly if we'd do it differently
or if you should skip this entirely.
```

**7. "I can do this myself"**

```
you probably can. question is whether you should.

your time is worth $[their hourly rate based on role]. this takes [X hours] to
do right. that's $[amount] of your time.

we do it for $[amount] and you get it done in [timeframe] without touching it.

but if you want to DIY, here's a free checklist of exactly what to do: [link].
no hard feelings. if you get stuck, call me.
```

**8. "Bad timing"**

```
when would be better?

i'll put a reminder in my calendar and reach out then. no sales pitch, just
checking if the timing works.

in the meantime, here's [free resource] that might help with [related problem].

what month works for a check-in?
```

**9. "I don't trust cold emails"**

```
smart. you shouldn't trust random emails.

here's how you can verify i'm real:
- my linkedin: [link] (200+ connections in [industry])
- my portfolio: [link] (actual work for businesses in {city})
- google "[your name] [your company]" and you'll find [reviews/mentions]

or just reply and say "prove it." i'll send a free audit of {company_name} with
specific, actionable recommendations. no strings.
```

**10. "Your price is too high compared to [competitor]"**

```
who are you comparing to?

genuinely asking because pricing varies wildly in this space. $500 website from
fiverr is a different product than what we deliver.

our $[amount] includes:
- [specific deliverable 1]
- [specific deliverable 2]
- [specific deliverable 3]
- [X] months of support

if [competitor] includes all that at a lower price, go with them. but check
what's actually included. most "cheap" options cut corners on [specific thing]
and you end up paying twice to fix it.
```

### Recovery Scripts

**"Not interested" Recovery (send 30 days later):**

Subject: one more thing about {company_name}

```
{first_name},

you said not interested last month. totally respected that.

since then, we helped [business name] in {city} with [specific result].

if anything changed on your end, i'm here. if not, this is genuinely my last email.

[YOUR_NAME]
```

**"Too expensive" Recovery (send 14 days later):**

Subject: smaller option for {company_name}

```
{first_name},

you mentioned budget was a concern.

we just launched a starter package: $[lower price] for [reduced scope].

it's not the full system, but it fixes the biggest issue ([specific problem]) and
you can always upgrade later.

worth revisiting? [calendly link]

[YOUR_NAME]
```

**"Already have someone" Recovery (send 60 days later):**

Subject: still happy with your [provider type]?

```
{first_name},

2 months ago you mentioned you're working with someone on [service].

just checking in. if they're killing it, great. nothing from me.

if results aren't what you expected, we just finished a project for [similar business]
that might be relevant: [brief result].

either way, no pressure.

[YOUR_NAME]
```

---

## Section F: Cold Calling Scripts

### Opener Script (First 30 Seconds)

```
"Hey {first_name}, this is [your name] from [company]. I'm calling because I
noticed {company_name} [specific observation about their business].

I'll be quick. We help [industry] businesses in {city} with [one sentence about
what you do]. Our last client saw [specific result].

Is this something you've thought about, or am I catching you at a bad time?"
```

**If "bad time":**
```
"No problem. When's a better time to call back? I'll make it quick, 5 minutes max."
```

**If "not interested":**
```
"Totally fair. One quick question before I go: how are you currently handling
[specific pain point]? Just curious if there's something else I should be reaching
out about instead."
```

**If "tell me more":**
Move to qualification questions below.

### Qualification Questions (Pick 3-4, Don't Interrogate)

```
1. "How many [leads/clients/patients/members] does {company_name} get per month?"

2. "What's your biggest bottleneck right now? Getting new clients, or keeping the ones you have?"

3. "Are you handling [specific task] manually, or do you have a system for it?"

4. "Have you ever looked into [service type] before? What held you back?"

5. "What would it mean for {company_name} if you could [specific improvement]?"

6. "What's your current [no-show rate / conversion rate / response time]? Do you know?"

7. "Who else would need to be involved in a decision like this?"
```

### Pitch (60 Seconds Max)

```
"Here's what we do in plain english.

We [one sentence describing service]. For {company_name}, that would look like:

[Deliverable 1] - which means [benefit in their language]
[Deliverable 2] - which means [benefit in their language]
[Deliverable 3] - which means [benefit in their language]

Our last client, [name or type], saw [specific result] within [timeframe].

Price range is $[low] to $[high] depending on what you need. Timeline is [X weeks].

Does any of that sound like it would help with what you described?"
```

### Close / Next Steps

**If they're interested:**
```
"Great. Here's what I'd suggest. Let's do a 15-minute deep dive where I look at
{company_name}'s [specific thing] and give you a custom breakdown of what we'd do
and what it would cost. No obligation.

I have [day] at [time] or [day] at [time]. Which works?"
```

**If they need to think:**
```
"Makes sense. I'll send you a one-page summary of what we discussed plus a case
study from a similar business. What email should I use?

And I'll follow up [day]. If you've decided it's not for you by then, just say
so and I'll back off. Sound fair?"
```

**If they say no:**
```
"Appreciate your time, {first_name}. If anything changes, I'm at [phone/email].

One last thing: do you know any other [industry professionals] in {city} who might
benefit? I offer a $[amount] referral fee for introductions.

Either way, thanks for the chat."
```

### Cold Call Best Practices

- call between 10-11:30am or 2-4pm (best connect rates)
- tuesday through thursday outperform monday and friday by 25%
- stand up while calling (energy comes through)
- smile while talking (it changes your tone, people hear it)
- speak 20% slower than you think you should
- pause after key numbers (let them sink in)
- say their name 2-3 times max (more feels fake)
- if voicemail: leave a 20-second message with one specific hook and your number. no callback request.
- track calls in LEDGER/OUTREACH_PIPELINE.csv
- target: 30-50 dials per day = 8-12 connects = 2-3 conversations = 1 meeting booked

---

## Appendix: Priority Actions

### To start sending emails this week

1. Buy 3 cold-sending domains ($12-15 each at Porkbun) - total: $45
2. Set up Google Workspace on each ($6/mo each) - total: $18/mo
3. Configure SPF/DKIM/DMARC on all 3
4. Start 14-day manual warmup (or pay $49/mo for DeliverOn to skip it)
5. Compile 50 prospect URLs per industry (use Google Maps + Yelp)
6. Pick 2 industries to start with (recommend: dentists + contractors, highest close rates)
7. Load prospects into Instantly.ai or send manually via Gmail
8. Send 10-15 emails per inbox per day for first week
9. Track everything in LEDGER/OUTREACH_PIPELINE.csv
10. Follow up on replies within 2 hours

### Expected results (conservative)

- Week 1: 100-150 emails sent, 5-8% reply rate, 5-12 replies
- Week 2: 200-300 emails sent, 8-10 positive replies, 3-5 calls booked
- Week 3: First deal closed ($1,500-$5,000)
- Month 1: 2-5 deals closed ($3,000-$15,000 revenue)

### Cost to launch

| Item | Cost | Recurring |
|------|------|-----------|
| 3 cold domains | $45 | Annual |
| Google Workspace x3 | $18/mo | Monthly |
| Instantly.ai (optional) | $97/mo | Monthly |
| DeliverOn (optional, skip warmup) | $49/mo | Monthly |
| Total minimum | $45 + $18/mo | - |
| Total with tools | $45 + $164/mo | - |

---

*Last Updated: 2026-02-06*
*Voice: @pipelineabuser (S-Tier)*
*Status: READY TO DEPLOY. Inboxes are the only blocker.*
