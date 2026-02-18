# The Cold Email Playbook: From Zero to 100+ Emails/Day in 30 Days

*Complete cold email system: infrastructure setup, warmup protocol, 10 industry sequences, prospect list building, deliverability rules, and the exact metrics that matter in 2026.*

---

## Who this is for

You sell a service. Web design, automation, consulting, video editing, copywriting, whatever. You need clients. You don't have a marketing budget. You do have a laptop and 2-3 hours per day.

Cold email is the highest-ROI client acquisition channel that exists. Zero ad spend. No followers required. No content treadmill. Just you, an inbox, and a message that solves someone's problem.

This playbook takes you from zero infrastructure to 100+ cold emails per day across 3 warmed inboxes in 30 days. Expected timeline to first closed deal: 4-8 weeks.

---

## Part 1: Infrastructure Setup (Day 1-2)

### Step 1: Buy 3 cold email domains ($30-45 total)

Never use your main domain for cold email. If your cold domain gets flagged, your personal email is unaffected.

**Where to buy:** Namecheap ($10-12/domain) or Porkbun ($9-11/domain)

**Naming strategy:**
```
If your brand is "acme":
- acmeagency.com      (sounds professional)
- acmedev.com          (sounds technical)
- acmeconsulting.com   (sounds established)

Alternatives:
- tryacme.com
- acmehq.com
- getacme.com
```

Buy all 3. Takes 10 minutes.

### Step 2: Set up Google Workspace ($18/month total)

Each domain gets a Google Workspace mailbox. $6/month per mailbox.

1. Go to workspace.google.com/signup
2. Enter domain 1
3. Create mailbox: outreach@domain1.com
4. Pick Starter plan ($6/month)
5. Verify domain ownership (add a TXT record to your DNS)
6. Repeat for domains 2 and 3

**Why Google Workspace and not free Gmail:**
- Custom domain looks professional (outreach@youragency.com vs random23847@gmail.com)
- Better deliverability than free Gmail accounts
- Google Workspace emails land in Primary tab more often
- You can set up proper authentication (SPF, DKIM, DMARC)

### Step 3: Configure DNS authentication (30 minutes)

This is the most important technical step. Bad DNS = your emails go to spam.

For EACH of your 3 domains, add these DNS records:

**SPF Record:**
```
Type: TXT
Host: @
Value: v=spf1 include:_spf.google.com ~all
```
What this does: tells receiving servers that Google is authorized to send email on your domain's behalf.

**DKIM Record:**
```
1. Go to Google Workspace Admin > Apps > Gmail > Authenticate Email
2. Click "Generate New Record"
3. Copy the long TXT record value
4. Add to DNS as TXT record with the host Google provides
```
What this does: adds a cryptographic signature to your emails proving they're from you.

**DMARC Record:**
```
Type: TXT
Host: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```
What this does: tells receiving servers what to do if SPF/DKIM fail. Start with p=none (monitoring only).

**Verify everything:**
Go to mxtoolbox.com/SuperTool.aspx. Enter each domain. You should see:
- SPF: PASS
- DKIM: PASS
- DMARC: PASS

If any fail, you're going to spam. Fix before proceeding.

### Step 4: Set up Calendly (15 minutes)

Your cold emails need a CTA. That CTA is a calendar link.

1. calendly.com (free tier works)
2. Create a "15-Minute Quick Chat" meeting type
3. Set availability: Mon-Fri, 9 AM - 5 PM your timezone
4. Buffer: 15 min between meetings
5. Reminders: 24 hours and 1 hour before
6. Optional question: "What's your biggest challenge right now?" (one question max)

Copy your Calendly link. You'll paste it in every cold email.

---

## Part 2: Email Warmup (Days 1-21)

New email addresses have zero reputation. If you start blasting 100 emails from a brand new inbox, you'll land in spam immediately and burn the domain.

Warmup builds your sender reputation by simulating real email activity.

### Option A: Manual warmup ($0, takes 21 days)

**Days 1-7: 10 emails/day per inbox**

Each day, for each of your 3 inboxes:
1. Send 5 emails to your personal accounts (Gmail, Yahoo, Outlook)
2. Reply to those emails from the receiving account
3. Send 3 emails to friends/family, ask them to reply
4. Subscribe to 2 newsletters (generates real inbound)
5. Reply to newsletter emails with a short comment

Total: 10 sent + 5-8 replies received per inbox per day.

**Days 8-14: 20 emails/day per inbox**

1. Continue personal emails (5/day)
2. Send to business contacts you know (5/day)
3. Sign up for services that send confirmation emails (2/day)
4. Send cold emails to LOW-PRIORITY prospects as test (8/day)
5. Ask contacts to reply (reply signals = deliverability gold)

**Days 15-21: 30-40 emails/day per inbox**

Mix per inbox:
- 5 warmup emails (maintain engagement signals)
- 25-35 real cold emails (actual prospects)

Total cold sends across 3 inboxes: 75-105/day.

### Option B: Instantly.ai ($97/month, semi-automated)

1. Sign up at instantly.ai
2. Connect all 3 Google Workspace inboxes
3. Enable warmup on all 3 (auto sends + auto replies between warm accounts)
4. Let it run for 14 days untouched
5. Day 15: Start cold campaigns at 20/day per inbox
6. Day 22: Ramp to 50/day per inbox
7. Keep warmup running forever (even during cold campaigns)

### Option C: Pre-warmed inboxes ($49-99/month, fastest)

Services like DeliverOn ($49/mo) and EmailBison ($99/mo) sell pre-warmed inboxes. You skip the 14-21 day wait entirely.

- DeliverOn: 3 pre-warmed inboxes, start sending Day 1, 50/day limit per inbox
- EmailBison: 10 pre-warmed inboxes, 80/day per inbox

**Recommendation:** If you have $97/month, use Instantly.ai. It gives you warmup + campaign management + deliverability monitoring in one tool. It pays for itself with one closed deal.

---

## Part 3: Building Prospect Lists (During Warmup)

While your inboxes warm up, build your prospect lists. You need 200-500 contacts per industry vertical.

### Source 1: Apollo.io (free, 50 credits/month)

1. Create free account at app.apollo.io
2. Search by: Title, Industry, Location, Company Size
3. Export 50 contacts per month (free limit)
4. Focus on decision-makers: Owner, Manager, Partner, Director

### Source 2: Google Maps scraping (free, unlimited)

1. Search Google Maps: "[industry] in [city]"
2. For each result, note: business name, phone, website, address
3. Visit each website, find email on contact/about page
4. Compile into CSV

This takes time but gives you the best quality leads. You're finding people who actually have a web presence (which means they care about their business online).

### Source 3: Industry-specific directories (free)

| Industry | Directory | What You Get |
|----------|-----------|-------------|
| Dental | Healthgrades, Zocdoc | Practice name, location, providers |
| Legal | State Bar directory, Avvo | Attorney name, firm, practice area |
| Real Estate | Realtor.com, Zillow agent finder | Agent name, brokerage, volume |
| Restaurants | Yelp, Google Business | Name, location, reviews, website |
| Fitness | ClassPass, Mindbody | Gym name, owner, services |
| SaaS | Product Hunt, G2 | Company, founder, funding |

### Email verification (non-negotiable)

Before sending a single cold email, verify every address.

- NeverBounce: $8 per 1,000 emails
- ZeroBounce: 100 free/month, then $0.008/email

Run all emails through verification. Remove any that bounce. Sending to invalid addresses destroys your deliverability.

### Prospect CSV format

```csv
first_name,last_name,email,company_name,city,industry,website,pain_point,score
John,Smith,john@smithdental.com,Smith Family Dental,Austin TX,dental,smithdental.com,website loads in 6.2s,78
Sarah,Johnson,sarah@johnsonlaw.com,Johnson & Partners,Austin TX,legal,johnsonlaw.com,no intake form on site,82
```

The `pain_point` column is what separates amateur cold email from professional cold email. Spending 60 seconds researching each prospect's specific problem gets you from 3% reply rate to 10%+ reply rate.

---

## Part 4: The 10 Cold Email Sequences

Each sequence is 4 emails over 8-14 days. The first email does the heavy lifting. Each follow-up is shorter and softer.

### Sequence 1: Healthcare / Dental -- Custom App Development

**Target:** Dental practices with 3-10 providers, $500K-$3M revenue
**Pain:** Patient no-shows, scheduling chaos, paper systems

**Email 1 (Day 0)**

Subject: patient no-shows costing you $15K-50K/year

```
{{FIRST_NAME}},

we build custom patient apps for dental practices.

automated reminders. one-tap reschedule. 68% reduction in no-shows.

{{PRACTICE_NAME}} was losing $23K/year to no-shows. we built them an app. 6 months later: 11% no-show rate down to 4%.

saved them $18K year one. app cost $8K. ROI positive in 5 months.

custom build for {{PRACTICE_NAME}}:
- patient portal (appointment booking, reminders, forms)
- automated SMS 24h + 2h before appointment
- one-tap reschedule (keeps the slot filled)
- insurance card upload (reduces check-in time)

we've built 14 of these. average no-show reduction: 68%.

15-min call to see if this makes sense for you: [CALENDLY]

[YOUR NAME]
[PHONE]
```

**Email 2 (Day 2)**

Subject: re: patient no-shows

```
{{FIRST_NAME}},

circling back.

if {{PRACTICE_NAME}} has a no-show rate above 8%, this pays for itself.

math:
- 10 no-shows per week x $150 avg appointment = $1,500/week lost
- 52 weeks = $78K/year
- reduce by 50% = $39K saved
- app costs $8K one-time

ROI: 4.8x first year.

quick call? [CALENDLY]

[YOUR NAME]
```

**Email 3 (Day 5)**

Subject: last one -- {{PRACTICE_NAME}} no-shows

```
{{FIRST_NAME}},

last email.

3 options:
1. no-shows aren't a problem for you (awesome, ignore this)
2. you're handling it another way (also great)
3. you're interested but buried (reply "later" and i'll follow up in 30 days)

if it's #3, just reply "later." i'll check back in a month.

[YOUR NAME]
```

**Email 4 (Day 8)**

Subject: [breakup] moving on from {{PRACTICE_NAME}}

```
{{FIRST_NAME}},

moving on.

if no-shows ever become a priority, we're here: [YOUR WEBSITE]

our apps: $6K-12K one-time. no monthly fees. 50-70% no-show reduction average.

good luck with {{PRACTICE_NAME}}.

[YOUR NAME]
```

---

### Sequence 2: Legal Firms -- Website + Automation

**Target:** Law firms with 2-8 attorneys, personal injury/family/estate
**Pain:** Low website conversion, manual intake, lead leakage

**Email 1 (Day 0)**

Subject: your website is losing you $50K+ in cases

```
{{FIRST_NAME}},

we build websites for law firms that convert 12-18% of visitors into consultations.

most law firm sites convert 2-4%.

we built {{COMPETITOR_FIRM}}'s site. before: 3% conversion. after: 14%. generated 47 extra consultations in 6 months.

at {{LAW_FIRM}}'s $3K average case value = $141K in new revenue.

site cost them $9K. ROI: 15.6x.

what we do:
- website redesign (modern, mobile-first, <2s load time)
- intake automation (forms to CRM to automatic follow-up)
- SEO optimization (rank for "[your city] + [practice area]")
- lead nurture sequences (7 automated emails for prospects)

we've done this for 22 law firms. average conversion increase: 3.2x.

15-min call to see if it fits: [CALENDLY]

[YOUR NAME]
[PHONE]
```

**Email 2 (Day 3):** ROI math email (500 visitors x 3% vs 14% conversion, $165K/year difference)

**Email 3 (Day 7):** "Not a fit?" three-options email

**Email 4 (Day 10):** Breakup email with pricing transparency ($6K-15K)

---

### Sequence 3: Real Estate -- Lead Gen + CRM

**Target:** Individual agents or teams of 2-5, 10-30 sales/year
**Pain:** Manual follow-up, lead leakage, no CRM

**Email 1 (Day 0)**

Subject: you're losing 40% of your leads to follow-up gaps

```
{{FIRST_NAME}},

we set up CRM + automation for real estate agents.

automatic follow-up sequences. lead scoring. SMS + email nurture.

{{AGENT_NAME}} in {{CITY}} was manually following up with leads. converting 8%.

we set them up with our system. 6 months later: 22% conversion.

went from 18 closings/year to 31 closings/year. 13 extra deals x $12K avg commission = $156K additional GCI.

system cost $2,500 setup + $200/mo. paid for itself in 18 days.

what we do:
- CRM setup (GoHighLevel or Follow Up Boss)
- automated lead nurture (7-touch sequence for new leads)
- SMS automation (instant response to Zillow/Realtor.com leads)
- lead scoring (know which leads are hot)
- pipeline tracking (never lose a lead again)

we've done this for 31 agents. average conversion increase: 2.1x.

15-min call: [CALENDLY]

[YOUR NAME]
[PHONE]
```

**Emails 2-4:** Follow same pattern -- ROI math, three options, breakup.

---

### Sequence 4: Local Business -- Website Redesign (FREE AUDIT HOOK)

This is the highest-converting cold email template in this entire playbook. You lead with a free gift.

**How it works:**
1. Run the prospect's website through a free speed test (PageSpeed Insights, GTmetrix)
2. Note 3 specific issues you found
3. Reference those exact issues in your email
4. Offer a free video walkthrough of the fixes
5. The call converts to a paid redesign ($500-3,000)

**Email 1 (Day 0)**

Subject: 3 things hurting {{BUSINESS_NAME}}'s website

```
{{FIRST_NAME}},

ran a quick audit on {{BUSINESS_NAME}}'s site. found 3 issues:

1. mobile load time: {{LOAD_TIME}} seconds (google wants under 2)
2. {{MISSING_FEATURE_1}} ({{IMPACT_1}})
3. {{MISSING_FEATURE_2}} ({{IMPACT_2}})

these are costing you leads. every extra second of load time drops conversions 7%.

I recorded a 3-min video walking through the fixes: [LOOM_LINK]

no pitch in the video. just what I found.

if you want help fixing any of it, I'm here.

[YOUR NAME]
[PHONE]

PS - reply "remove" and you won't hear from me again.
```

**Email 2 (Day 4):** ROI math (200-500 visitors, 2% vs 5% conversion, revenue difference)

**Email 3 (Day 7):** Social proof (similar business fixed same issues, specific results)

**Email 4 (Day 14):** Breakup + free speed test tool link

---

### Sequence 5: Course Creators / YouTubers -- Video Clipping Service

**Target:** YouTubers/podcast hosts with 10K-500K subscribers
**Hook:** Send them a FREE sample clip from their latest video

**Email 1 (Day 0)**

Subject: clipped your latest video

```
{{FIRST_NAME}},

grabbed your latest video "{{VIDEO_TITLE}}" and pulled 3 clips that would crush on short-form:

1. [timestamp] - {{HOOK_1}} (30 sec)
2. [timestamp] - {{HOOK_2}} (45 sec)
3. [timestamp] - {{HOOK_3}} (20 sec)

sample clip attached: [LINK]

we do this for 6 creators. average: 3 clips per video, 15-30 clips per month. creators see 30-60% more subscribers from short-form repurposing.

cost: $500-1,500/month depending on volume.

worth trying? first batch is free if you want to test quality.

[YOUR NAME]
```

---

### Sequence 6: SaaS Companies -- Content Writing

**Email 1 (Day 0)**

Subject: your blog hasn't been updated in {{DAYS}} days

```
{{FIRST_NAME}},

checked {{COMPANY}}'s blog. last post was {{LAST_POST_DATE}}. that's {{DAYS}} days ago.

google deprioritizes stale sites. your competitors publishing weekly are taking your search traffic.

we write SEO-optimized blog content for SaaS companies. 4 posts per month, $800/month. each post targets keywords your competitors are ranking for.

one client went from 2,000 to 11,000 organic visitors in 5 months. same product, better content.

want to see what keywords {{COMPANY}} should target? reply "keywords" and I'll pull a free report.

[YOUR NAME]
```

---

### Sequence 7: E-commerce -- Email/SMS Marketing

**Email 1 (Day 0)**

Subject: your abandoned cart emails are leaving $3K-8K/month on the table

```
{{FIRST_NAME}},

checked {{STORE_NAME}}'s checkout flow. noticed a few things:

1. no abandoned cart email sequence (you're losing 60-70% of carts with no follow-up)
2. no post-purchase upsell flow
3. no win-back sequence for lapsed customers

we set up email + SMS flows for ecom stores. average result: 15-30% revenue increase from email alone.

last client (similar size to {{STORE_NAME}}): went from $0 email revenue to $4,200/month in 60 days.

cost: $1,500 one-time setup + $300/month management.

15-min call to review your flows: [CALENDLY]

[YOUR NAME]
```

---

### Sequence 8: Restaurants -- Online Ordering + Google

**Email 1 (Day 0)**

Subject: {{RESTAURANT_NAME}} -- your Google listing has 3 issues

```
{{FIRST_NAME}},

checked {{RESTAURANT_NAME}}'s Google Business Profile. found 3 fixable issues:

1. {{ISSUE_1}} (costs you visibility in local search)
2. {{ISSUE_2}} (hurts click-through from Google Maps)
3. {{ISSUE_3}} (losing to competitors who have this)

43% of diners check your menu online before visiting. these issues are sending them to the restaurant down the street.

we fix Google profiles + set up online ordering for restaurants. average result: 25-40% increase in online orders within 60 days.

cost: $500-1,500 depending on scope.

15-min call: [CALENDLY]

[YOUR NAME]
```

---

### Sequence 9: Fitness / Gyms -- Member Retention

**Email 1 (Day 0)**

Subject: {{GYM_NAME}} -- your member retention drops 34% after month 3

```
{{FIRST_NAME}},

industry data: gym members who don't get a structured onboarding in their first 90 days have a 34% higher churn rate.

we build automated member onboarding sequences for gyms. SMS + email + app notifications that keep members engaged through the critical first 90 days.

one gym (similar size to {{GYM_NAME}}): went from 62% 90-day retention to 81%. that's 19% more members staying past the danger zone.

at {{GYM_NAME}}'s membership price, that's roughly ${{RETENTION_VALUE}}/month in retained revenue.

setup cost: $2,000 one-time. monthly: $200 for automation + messaging costs.

15-min call: [CALENDLY]

[YOUR NAME]
```

---

### Sequence 10: Agencies / Freelancers -- Lead Generation System

**Email 1 (Day 0)**

Subject: {{AGENCY_NAME}} -- I can get you 10 calls/week for $37/mo

```
{{FIRST_NAME}},

most agencies get 70-80% of clients from referrals. works great until it doesn't. feast or famine.

we set up cold outreach systems for agencies. automated lead scraping + email sequences + booking calendar.

one agency (3-person team like {{AGENCY_NAME}}): went from 2 inbound calls/week to 12. closed 4 extra clients in the first month. $18K in new revenue.

system cost: $37/month (Instantly.ai) + $18/month (email inboxes) + our setup fee ($1,500).

pays for itself in the first week if you close just 1 deal.

15-min call to see if this fits: [CALENDLY]

[YOUR NAME]
```

---

## Part 5: Sending Rules (2026 Edition)

### Critical changes in 2026

**Gmail tracking pixel warnings:** Gmail now shows users "this email is tracking you" when it detects open-tracking pixels. Solution: disable ALL open tracking and link tracking. Track reply rate only.

**Warmup timeline increased:** Was 7-14 days. Now 14-21 days. Google is more aggressive about flagging new senders.

**Safe daily sending limits:**

| Inbox Age | Max Cold Emails/Day |
|-----------|-------------------|
| Brand new (Day 1) | 0 (warmup only) |
| 1 week warmed | 10 |
| 2 weeks warmed | 30 |
| 3 weeks warmed | 50 |
| 1 month+ warmed | 70-80 (absolute max) |

Never exceed 80 cold emails per day per inbox. Ever.

### The rules

**DO:**
- Keep warmup running even during live campaigns
- Respond to all replies within 2 hours
- Track reply rates daily (not open rates)
- A/B test subject lines after 50 sends per variant
- Personalize company name and city for EVERY email
- Include unsubscribe option (CAN-SPAM compliance)
- Send Tuesday through Thursday, 8-10 AM recipient local time
- Use plain text (no HTML templates, no images)

**DO NOT:**
- Use open tracking pixels (Gmail warns users)
- Use link tracking (flags as marketing email)
- Send more than 80 emails/day per inbox
- Send on weekends
- Send to unverified emails (bounces destroy deliverability)
- Use images in cold emails (text only)
- Use more than 1 link per email (just your Calendly link)
- Use "RE:" or "FWD:" fakes (instant spam flag)
- Use spam trigger words: opportunity, partnership, collaborate, synergy, innovative, special offer

### A/B testing framework

Test one variable at a time. 50 sends minimum per variant before calling a winner.

**Test priority order:**
1. Subject lines (biggest impact on whether they even see your email)
2. Email length (50 words vs 100 words vs 150 words)
3. CTA format ("15-min call: [CALENDLY]" vs "reply 'interested'" vs "quick call?")
4. Send time (8 AM vs 10 AM vs 2 PM)
5. Personalization level (name + company vs name + company + specific observation)

**How to run the test:**
1. Split your list 50/50 randomly
2. Send variant A to half, variant B to half
3. Same day, same time
4. Wait 48 hours
5. Winner = higher REPLY rate (not open rate)
6. Use winner for next 100 sends, test a new challenger

---

## Part 6: Metrics That Matter

### The only metrics worth tracking

| Metric | Formula | Acceptable | Good | Great |
|--------|---------|-----------|------|-------|
| Reply rate | (Replies / Sent) x 100 | 3-5% | 5-8% | 8%+ |
| Positive reply rate | (Interested / Sent) x 100 | 1-3% | 3-5% | 5%+ |
| Call book rate | (Calls booked / Sent) x 100 | 0.5-1% | 1-2% | 2%+ |
| Close rate | (Deals / Calls) x 100 | 10-20% | 20-30% | 30%+ |

### Weekly tracking spreadsheet

```csv
week,emails_sent,replies,positive_replies,calls_booked,deals_closed,revenue
Week 1,150,8,3,1,0,0
Week 2,350,21,9,4,1,2500
Week 3,500,35,14,6,2,7500
Week 4,700,49,20,8,3,12500
```

### What to do when metrics are bad

**Reply rate below 3%:**
1. Check deliverability (are emails landing in inbox? send test to gmail and check)
2. Improve personalization (add specific pain points per prospect)
3. Test different subject lines
4. Shorten email body to under 100 words
5. Check your prospect list quality (are these real decision-makers?)

**Replies positive but no calls booked:**
1. Make Calendly link more prominent
2. Simplify the CTA (just the link, no explanation needed)
3. Qualify prospects better (only email real fits)
4. Follow up faster (reply within 2 hours, ideally within 30 minutes)

**Calls happening but no deals closing:**
1. Qualify harder on the call (budget, timeline, authority, need)
2. Present ROI math specific to their business
3. Offer a small starter project to build trust ($500 vs $5,000)
4. Get better at objection handling (see Part 7)

---

## Part 7: The Call Framework

When someone replies positively and books a call, use this structure.

### The 15-minute discovery call

**Minutes 1-2: Rapport**
```
"Thanks for jumping on. Before I get into anything, can you give me a 30-second overview of [BUSINESS_NAME] and what you're working on right now?"
```

Let them talk. Take notes.

**Minutes 3-7: Pain discovery**
```
"You mentioned [THING THEY SAID]. Can you tell me more about that?"
"What's that costing you right now -- in time, money, or lost opportunities?"
"How long has this been an issue?"
"Have you tried to fix it before? What happened?"
```

Get specific numbers from them. "About how many leads do you get per month?" "What's your average deal size?"

**Minutes 8-10: Present the solution**
```
"Based on what you've told me, here's what I'd recommend..."
[Describe your service in their language, using their numbers]
"For businesses like yours, we typically see [SPECIFIC RESULT] within [TIMEFRAME]."
```

**Minutes 11-13: Pricing and next steps**
```
"The investment for this is [PRICE]. Based on the numbers you shared -- [THEIR REVENUE/COSTS] -- this would pay for itself in [TIMEFRAME]."
"Most clients start with [STARTER PACKAGE] and expand from there."
```

**Minutes 14-15: Close or next step**
```
If ready: "Want to get started? I can send the agreement today."
If not ready: "What would you need to see to feel comfortable moving forward?"
If needs approval: "When can we schedule a follow-up with [decision maker]?"
```

### Objection handling

| They say | You say |
|----------|---------|
| "Too expensive" | "What's the cost of NOT fixing this? You mentioned losing $X/month to [their problem]." |
| "I need to think about it" | "Totally understand. What specific concerns can I address right now?" |
| "We're already working with someone" | "How's that going? Most people I talk to came from another provider." |
| "Send me more info" | "Happy to. What specifically would help you decide? I'd rather send you exactly what you need." |
| "Not a good time" | "When would be better? I'll follow up then." (add to CRM, follow up on exact date) |

---

## Part 8: Scaling from 100 to 500+ Emails/Day

### Phase 1: 3 inboxes, 50/day each = 150/day (Week 3-6)

This is your starting point after warmup. 3 inboxes, 3 campaigns, 3 industries.

### Phase 2: 6 inboxes, 50/day each = 300/day (Month 2)

Buy 3 more domains ($30-45). Set up 3 more Google Workspace inboxes ($18/mo). Warm them up while your first 3 are running campaigns.

### Phase 3: 10 inboxes, 50/day each = 500/day (Month 3)

Same process. 4 more domains, 4 more inboxes.

**Cost at 500/day:**
- 10 domains: $100-150/year
- 10 Google Workspace inboxes: $60/month
- Instantly.ai: $97/month
- NeverBounce email verification: $40/month
- Total: ~$200/month

**Revenue at 500/day with 5% reply rate:**
- 500 emails/day = 25 replies/day
- 25 replies x 40% positive = 10 positive replies/day
- 10 positive x 20% book calls = 2 calls/day
- 2 calls/day x 25% close rate = 0.5 deals/day = ~10 deals/month
- At $2,000 average deal = $20,000/month

$200/month in costs for $20,000/month in revenue. That's cold email.

---

## Part 9: Compliance and Legal

### CAN-SPAM requirements (United States)

1. Include your physical mailing address (PO Box works)
2. Include an unsubscribe mechanism ("reply 'remove' to unsubscribe")
3. Don't use deceptive subject lines
4. Don't use a fake "from" name
5. Process unsubscribe requests within 10 business days

### GDPR considerations (if emailing EU)

Cold email to businesses is generally allowed under "legitimate interest" in the EU. But:
1. You must have a legitimate business reason for contacting them
2. You must offer easy opt-out
3. You cannot buy personal email lists
4. Business emails (info@, sales@, etc.) have different rules than personal emails

### Best practice: keep it clean

- Never scrape personal emails from social media
- Use business emails from business websites only
- Remove anyone who asks to be removed immediately
- Don't send more than 4 emails in a sequence
- Space follow-ups 2-7 days apart
- Be honest about who you are and what you want

---

## Part 10: The 30-Day Launch Plan

### Week 1: Infrastructure

- [ ] Day 1: Buy 3 domains ($30-45)
- [ ] Day 1: Set up Google Workspace ($18/mo)
- [ ] Day 1: Configure DNS (SPF, DKIM, DMARC)
- [ ] Day 1: Set up Calendly (free)
- [ ] Day 2: Start manual warmup OR sign up for Instantly.ai
- [ ] Day 2: Create Apollo.io account (free)

### Week 2: List Building

- [ ] Build 200 prospects for Industry 1
- [ ] Build 200 prospects for Industry 2
- [ ] Build 200 prospects for Industry 3
- [ ] Verify all emails through NeverBounce ($4.80 for 600)
- [ ] Continue warmup (daily, 15 min)
- [ ] Customize email sequences with your details

### Week 3: First Sends

- [ ] Day 15: Send first 10 test emails per inbox
- [ ] Day 16: Check deliverability (did they land in inbox?)
- [ ] Day 17: Ramp to 20/day per inbox if no bounces
- [ ] Day 18-21: Ramp to 30/day per inbox
- [ ] Track: reply rate, bounce rate, positive replies
- [ ] Respond to every reply within 2 hours

### Week 4: Scale and Optimize

- [ ] Ramp to 50/day per inbox (150 total)
- [ ] A/B test subject lines (2 variants, 50 sends each)
- [ ] Book first discovery calls
- [ ] Close first deal
- [ ] Order 3 more domains for Phase 2 expansion
- [ ] Start warmup on new domains

### Monthly targets

| Month | Daily Volume | Expected Replies | Calls | Deals | Revenue |
|-------|-------------|-----------------|-------|-------|---------|
| 1 | 100-150 | 5-12/day | 8-15 | 1-3 | $2K-9K |
| 2 | 200-300 | 10-24/day | 15-30 | 3-6 | $6K-18K |
| 3 | 300-500 | 15-40/day | 20-40 | 5-10 | $10K-30K |

---

## What to Do Right Now

1. Open Namecheap and buy 3 domains
2. Set up Google Workspace on all 3
3. Configure DNS records (SPF, DKIM, DMARC)
4. Start warmup today
5. While warming up, build your first 200-prospect list
6. On Day 15, send your first 10 cold emails
7. Track every reply in a spreadsheet

The math is simple. Send emails. Get replies. Book calls. Close deals.

Every day you wait is a day your competitors are sending.

---

*Built by PRINTMAXX. Get the full cold outreach toolkit (scrapers, automation scripts, CRM templates, deliverability monitoring): printmaxxer.gumroad.com*

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
