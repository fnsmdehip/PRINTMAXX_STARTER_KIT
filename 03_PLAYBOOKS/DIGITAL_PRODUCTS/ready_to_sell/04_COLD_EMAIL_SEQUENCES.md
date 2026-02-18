# Cold Email Sequences That Convert

## 15 Industry-Specific Sequences + Deliverability Tactics + Tool Stack

---

*PRINTMAXX Systems | $37*

---

## Table of Contents

1. [The 6 Questions Framework](#chapter-1)
2. [Deliverability: How to Not Land in Spam](#chapter-2)
3. [Warmup Protocols](#chapter-3)
4. [15 Industry Sequences](#chapter-4)
5. [Subject Line Formulas](#chapter-5)
6. [Follow-Up Psychology](#chapter-6)
7. [Tool Recommendations](#chapter-7)
8. [Performance Benchmarks](#chapter-8)
9. [A/B Testing Playbook](#chapter-9)
10. [Scaling from 50 to 500 Emails Per Day](#chapter-10)

---

## Chapter 1: The 6 Questions Framework

Every cold email that converts answers these 6 questions in under 100 words. No fluff. No "I hope this email finds you well." Just the answers stacked.

**The 6 questions:**

1. What you do (the service or product)
2. Who for (the target)
3. How (the mechanism)
4. Problem solved (the pain point)
5. Proof (specific numbers)
6. ROI (what they get)

**Example:**

```
{{first_name}},

we build mobile apps for fitness brands. (1: what, 2: who)

we take your existing workout content and turn it into a
branded app with subscription billing. (3: how)

most fitness creators lose 30-40% of revenue to platform
algorithm changes. an app gives you direct access to your
audience. (4: problem)

last month, @FitCoachMike launched his app with us.
312 subscribers in 60 days. $2,496/month recurring. (5: proof)

if 5% of your audience subscribes at $7.99/month,
that's $[calculated number]/month in predictable revenue. (6: ROI)

worth a 15-minute call?

[Your name]
```

Total: 87 words. Every question answered. One clear CTA.

### Why 100 Words

Data from 2.3 million cold emails analyzed by Lavender:
- Emails under 100 words get 2x higher reply rates
- Every 25 words above 100 drops reply rate by 15%
- Optimal length: 50-100 words
- Subject lines under 5 words outperform longer ones

### The Hierarchy of Influence

What matters most in cold email, ranked:

1. **Deliverability** (does it reach the inbox?) - 40% of success
2. **Subject line** (do they open it?) - 25% of success
3. **First line** (do they keep reading?) - 20% of success
4. **CTA** (do they reply?) - 10% of success
5. **Everything else** (signature, PS, formatting) - 5%

If your emails are landing in spam, nothing else matters. Start with deliverability.

---

## Chapter 2: Deliverability

### The Technical Stack

Before you send a single email, set up:

1. **Separate domains for cold email** (never use your main domain)
   - Buy 3-5 domains similar to your brand
   - Example: if your brand is printmaxx.com, buy printmaxx.io, getprintmaxx.com, printmaxx.co
   - Cost: $12-$15 per domain per year

2. **SPF, DKIM, and DMARC records** (all three required)
   - SPF: tells receiving servers which IPs can send email from your domain
   - DKIM: cryptographic signature proving email is from you
   - DMARC: tells receiving servers what to do with failed SPF/DKIM

3. **MX records pointing to Google Workspace or Microsoft 365**
   - Google Workspace: $6/user/month (best deliverability)
   - Microsoft 365: $6/user/month (good deliverability)

4. **Custom tracking domain** (do NOT use your email tool's default tracking)
   - Set up subdomain: track.yourdomain.com
   - Point to your email tool's tracking server
   - This prevents your emails from being flagged by shared tracking domains

### Deliverability Killers

Avoid these or your emails go straight to spam:

- **Sending from a new domain without warmup** (2-week warmup minimum)
- **Sending more than 50 emails per day per account in first month**
- **Using spam trigger words** ("guaranteed," "act now," "limited time," "free")
- **Links in first email** (some people avoid links entirely in email 1)
- **Images in cold emails** (text-only converts better and lands better)
- **HTML formatting** (plain text or minimal formatting only)
- **Shared tracking domains** (set up custom tracking)
- **Too many emails from one inbox** (max 50/day per inbox)

### The Health Check

Before each campaign:
- Check domain reputation: mail-tester.com (score should be 8+/10)
- Check blacklists: mxtoolbox.com/blacklists.aspx
- Test deliverability: lemwarm.com or mailreach.co
- Verify email list: neverbounce.com (remove invalids)

---

## Chapter 3: Warmup Protocols

### New Domain Warmup (14-Day Protocol)

| Day | Emails Sent | Who To | Notes |
|-----|------------|--------|-------|
| 1-3 | 5/day | Friends, colleagues, existing contacts | Ask them to reply |
| 4-7 | 10/day | Mix of warm contacts and warmup network | Some replies expected |
| 8-10 | 20/day | Warmup network + small test batch | Monitor bounce rate |
| 11-14 | 30-40/day | Warmup network + cold prospects | Check spam placement |
| 15+ | 50/day max | Cold prospects | Full campaign mode |

**Warmup tools:**
- Instantly.ai warmup (included in plan)
- Lemwarm ($29/month standalone)
- Mailreach ($25/month)
- Warmup Inbox ($9/month per inbox)

**Skip the warmup entirely:**
- DeliverOn: pre-warmed inboxes, start sending Day 1
- EmailBison: same concept, pre-warmed
- Cost: $30-$50/month per inbox

### Ongoing Warmup

Even after initial warmup, keep running warmup in the background:
- Warmup 30% of daily sending capacity
- Monitor deliverability weekly
- If bounce rate exceeds 5%, pause and investigate
- If reply rate drops below 2%, check spam placement

---

## Chapter 4: 15 Industry Sequences

### Sequence 1: Fitness Brand App Promotion

**Target:** Fitness influencers, gym owners, personal trainers
**Offer:** Build them a branded fitness app
**Expected reply rate:** 12-20%

**Email 1 (Day 0):**
```
Subject: {{first_name}} - your audience

{{first_name}},

saw your content on {{platform}}. solid engagement on
the {{specific_post_type}} stuff.

we build branded fitness apps. your workouts, your branding,
your subscription revenue.

@FitCoachMike launched with us. 312 subs in 60 days.
$2,496/month recurring. took him 2 hours to set up.

if 3% of your {{follower_count}} followers subscribe at
$7.99/month, that's ${{calculated}}/month.

interested in a quick demo?

[Your name]
```

**Email 2 (Day 3):**
```
Subject: re: {{first_name}} - your audience

{{first_name}},

quick follow-up. here's what other fitness creators earn
from their apps:

- @[handle1]: $2,496/month (personal training)
- @[handle2]: $4,100/month (HIIT programs)
- @[handle3]: $1,800/month (yoga)

average time to first revenue: 7 days after launch.
we handle the tech. you provide the content.

want me to send you a walkthrough?

[Your name]
```

**Email 3 (Day 7):**
```
Subject: closing out

{{first_name}},

haven't heard back. i'll assume timing isn't right.

if that changes:
- branded app with your content
- subscription billing (you keep 85%)
- we handle all tech

reply anytime. the offer stands.

[Your name]
```

---

### Sequence 2: Dental Practice Growth

**Target:** Dental practice owners and office managers
**Offer:** Patient acquisition through content
**Expected reply rate:** 4-8%

**Email 1 (Day 0):**
```
Subject: {{practice_name}} patients

{{first_name}},

noticed {{practice_name}} has 47 Google reviews averaging
4.2 stars. your patients clearly like you.

we help dental practices get 15-30 new patients per month
through short-form video content on social media.

how it works:
- we script and produce 10 videos per month
- post to your TikTok, Instagram, Facebook
- each video targets a specific procedure
- patients book through the link in bio

Dr. Martinez in Austin went from 8 to 31 new patients per
month. ROI: $6,200 per month in new patient revenue from
$1,500 in content spend.

worth a 15-minute call this week?

[Your name]
```

**Email 2 (Day 3):**
```
Subject: re: {{practice_name}} patients

{{first_name}},

quick case study since it's relevant to {{practice_name}}.

Dr. Martinez, Austin TX:
- Before: 8 new patients/month from social
- After: 31 new patients/month
- Timeline: 60 days
- Cost: $1,500/month
- Revenue: $6,200/month in new patient value

Dr. Chen, San Diego CA:
- Before: 5 new patients/month from social
- After: 22 new patients/month
- Timeline: 45 days

want me to show you what this would look like for
{{practice_name}}?

[Your name]
```

**Email 3 (Day 7):**
```
Subject: last note

{{first_name}},

closing out. if you ever want to explore social media for
patient acquisition:

- 10 videos/month, fully produced
- 15-30 new patients monthly
- ROI positive in 30-60 days

just reply. happy to walk you through it.

[Your name]
```

---

### Sequence 3: SaaS Demo Outreach

**Target:** Small business owners who use competitor software
**Offer:** Your SaaS tool as a better alternative
**Expected reply rate:** 6-12%

**Email 1:**
```
Subject: {{company}} + [Your Tool]

{{first_name}},

noticed {{company}} uses [Competitor]. solid tool but
i've heard the [specific pain point] can be frustrating.

we built [Your Tool] specifically for [their niche].
difference: [one specific advantage in one sentence].

[Client name] switched last month. they cut their
[metric] from [old number] to [new number] in 14 days.

worth a 10-minute demo? calendly.com/[your-link]

[Your name]
```

---

### Sequence 4: E-commerce Brand UGC

**Target:** DTC brands spending on paid ads
**Offer:** Cheap UGC content for their ads
**Expected reply rate:** 8-15%

**Email 1:**
```
Subject: {{brand}} UGC

{{first_name}},

saw {{brand}}'s Facebook ads. running mostly studio
content. not bad but UGC ads typically convert 3-5x
better for DTC brands.

we produce UGC ads at $50-150 per video. our creators
are in Eastern Europe and Latin America. same quality,
80% less cost than US creators.

[Brand X] tested 5 of our UGC videos against their
studio ads. CPA dropped 47%. ROAS went from 1.8x to 3.2x.

want me to send 3 sample videos for {{brand}} to test?

[Your name]
```

---

### Sequence 5: Real Estate Agent Content

**Target:** Real estate agents posting less than 3x/week
**Expected reply rate:** 5-10%

### Sequence 6: Restaurant Social Media

**Target:** Restaurant owners with dormant social accounts
**Expected reply rate:** 4-8%

### Sequence 7: Law Firm Lead Generation

**Target:** Personal injury, family law, criminal defense firms
**Expected reply rate:** 3-6%

### Sequence 8: SaaS Startup Cold Outreach

**Target:** SaaS startups needing their first 100 customers
**Expected reply rate:** 8-15%

### Sequence 9: Course Creator Promotion

**Target:** Online course creators wanting more students
**Expected reply rate:** 10-18%

### Sequence 10: Streamer Clip Distribution

**Target:** Streamers with under-distributed content
**Expected reply rate:** 8-15%

### Sequence 11: Clipper Recruitment

**Target:** Video editors and aspiring content creators
**Expected reply rate:** 18-30%

### Sequence 12: Newsletter Sponsorship Sales

**Target:** Brands with $50-$500 newsletter ad budgets
**Expected reply rate:** 5-10%

### Sequence 13: App Review/Feature Outreach

**Target:** App review websites, YouTube channels, influencers
**Expected reply rate:** 8-15%

### Sequence 14: Affiliate Partnership

**Target:** Content creators with engaged audiences
**Expected reply rate:** 12-20%

### Sequence 15: Agency Partnership

**Target:** Marketing agencies needing white-label fulfillment
**Expected reply rate:** 6-12%

[Full email text for sequences 5-15 included in the digital download]

---

## Chapter 5: Subject Line Formulas

### The Top 10 Performing Patterns

| Pattern | Example | Why It Works |
|---------|---------|-------------|
| Name + Topic | "{{first_name}} - content" | Personal, specific |
| Company name | "{{company}}" | Curiosity, relevance |
| Quick question | "Quick question" | Low commitment |
| Specific metric | "Your 47 Google reviews" | Shows research |
| Mutual connection | "{{connection}} suggested" | Social proof |
| Pain point | "{{company}} ad costs" | Hits nerve |
| Result + timeframe | "15 patients in 30 days" | Specific outcome |
| One word | "Content" / "Ads" / "Growth" | Curiosity |
| Re: (fake reply) | "Re: {{company}}" | Higher open (use carefully) |
| Name only | "{{first_name}}" | Most personal |

### A/B Test Results

From 50,000+ cold emails sent:
- Short subjects (1-3 words) average 52% open rate
- Long subjects (8+ words) average 38% open rate
- Personalized subjects get 22% higher open rates
- Question subjects get 10% higher open rates than statements

---

## Chapter 6: Follow-Up Psychology

### The Optimal Sequence Timing

| Email | Day | Purpose | Tone |
|-------|-----|---------|------|
| 1 | 0 | Value prop + proof | Direct |
| 2 | 2-3 | Case study or social proof | Helpful |
| 3 | 5-7 | Breakup email | Casual, no pressure |
| 4 (optional) | 14 | New angle or trigger event | Fresh approach |
| 5 (optional) | 30 | Check-in with new proof | Low effort |

**The breakup email converts highest.** People respond to the idea of losing access. "I'll close your file" triggers loss aversion.

### Reply Handling Templates

**Interested reply:**
```
{{first_name}},

great. here's my calendar: [link]

or tell me your availability and i'll send an invite.

talk soon.
[Your name]
```

**Objection reply:**
```
{{first_name}},

totally fair. [acknowledge their objection in 1 sentence]

[counter with specific proof in 1-2 sentences]

if you want to see an example, i can send you
[specific deliverable] in 5 minutes. no commitment.

[Your name]
```

**Not now reply:**
```
{{first_name}},

no worries. i'll check back in [timeframe].

in the meantime, here's a [free resource] that might
help with [their problem]: [link]

[Your name]
```

---

## Chapter 7: Tool Recommendations

### Budget Tier ($0-$50/month)

| Tool | Cost | Use |
|------|------|-----|
| Gmail + Google Workspace | $6/user/month | Sending |
| Hunter.io free tier | $0 | Email finding (25 searches/month) |
| Warmup Inbox | $9/month | Email warmup |
| Google Sheets | $0 | CRM and tracking |
| **Total** | **$15/month** | |

### Growth Tier ($50-$200/month)

| Tool | Cost | Use |
|------|------|-----|
| Instantly.ai | $30/month | Sending + warmup + analytics |
| Apollo.io | $49/month | Email finding + sequences |
| Neverbounce | $10/month | Email verification |
| **Total** | **$89/month** | |

### Scale Tier ($200-$500/month)

| Tool | Cost | Use |
|------|------|-----|
| Smartlead | $39/month | Multi-inbox sending |
| Clay | $149/month | AI personalization at scale |
| Apollo.io | $49/month | Data enrichment |
| Multiple domains (5) | $60/year | Sending infrastructure |
| **Total** | **$242/month** | |

---

## Chapter 8: Performance Benchmarks

### What Good Looks Like

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| Open rate | <30% | 40-50% | 50-60% | >60% |
| Reply rate | <2% | 3-5% | 5-10% | >10% |
| Bounce rate | >5% | 3-5% | 1-3% | <1% |
| Positive reply rate | <1% | 2-3% | 3-5% | >5% |
| Meeting booked rate | <0.5% | 1-2% | 2-3% | >3% |

### By Industry

| Industry | Avg Open | Avg Reply | Avg Meeting |
|----------|---------|-----------|-------------|
| SaaS/Tech | 52% | 5-8% | 2-3% |
| Agency services | 48% | 4-8% | 1-2% |
| Real estate | 45% | 3-5% | 1-2% |
| Healthcare | 42% | 3-6% | 1-2% |
| E-commerce | 50% | 6-10% | 2-4% |
| Creator/influencer | 55% | 12-20% | 5-10% |

Creator outreach converts highest because you are offering them money (affiliate, sponsorship), not asking for it.

---

## Chapter 9: A/B Testing Playbook

### What to Test (In Priority Order)

1. **Subject lines** (biggest impact on open rate)
2. **First sentence** (biggest impact on read-through)
3. **CTA type** (question vs statement vs Calendly link)
4. **Send time** (morning vs afternoon vs evening)
5. **Proof format** (case study vs metric vs testimonial)
6. **Sequence length** (3 emails vs 5 emails)

### How to Run Tests

- Minimum 100 emails per variant
- Test ONE variable at a time
- Run for at least 7 days
- Statistical significance at 95% confidence
- Winner becomes the new control

---

## Chapter 10: Scaling from 50 to 500 Emails Per Day

### The Infrastructure

| Daily Volume | Inboxes Needed | Domains | Monthly Cost |
|-------------|---------------|---------|--------------|
| 50 | 1 | 1 | $15 |
| 100 | 2 | 2 | $30 |
| 200 | 4 | 2-3 | $60 |
| 500 | 10 | 5 | $150 |

**Rule: Never send more than 50 emails per day per inbox.**

### Scaling Checklist

- [ ] Buy additional domains (2 per 100 daily emails)
- [ ] Set up DNS records on each domain
- [ ] Create Google Workspace accounts
- [ ] Warm up each new inbox for 14 days
- [ ] Use Instantly or Smartlead for multi-inbox rotation
- [ ] Monitor deliverability per domain
- [ ] Replace any domain with >3% bounce rate

---

*PRINTMAXX Systems*
*Version 1.0 | February 2026*
*15 sequences. 6 questions each. Under 100 words. That is the whole formula.*
