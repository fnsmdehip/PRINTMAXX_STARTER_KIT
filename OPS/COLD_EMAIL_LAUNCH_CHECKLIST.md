# Cold Email Launch Checklist

**Created:** 2026-02-10
**Status:** NOT_STARTED
**Goal:** Go from 0 to 100+ cold emails/day across 3 warmed inboxes in 30 days. Close first cold email deal within 6-10 weeks.
**Existing assets:** 3 verticals fully sequenced (Healthcare, Legal, Real Estate), 5 additional industry sequences, deliverability guides, LinkedIn templates. All in `MONEY_METHODS/COLD_OUTBOUND/` and `CONTENT/email_sequences/cold/`.

---

## PHASE 0: Infrastructure Setup (Day 1-2)

### Step 1: Buy 3 Cold Email Domains ($30-45 total)

Do NOT use your main domain for cold email. Buy separate domains that look similar.

```
Where: Namecheap (namecheap.com) or Porkbun (porkbun.com) or Cloudflare Registrar
Cost: $10-15 per domain

Domain naming strategy (pick 3):
- [yourname]agency.com
- [yourname]dev.com
- [yourname]consulting.com
- try[yourname].com
- [yourname]hq.com
- get[yourname].com

Example if your name is "printmaxx":
1. printmaxxagency.com
2. printmaxxdev.com
3. printmaxxconsulting.com

Purchase all 3 right now. Takes 10 minutes.
```

**Action:**
- [ ] Go to namecheap.com
- [ ] Search for 3 domains
- [ ] Purchase all 3 ($30-45 total)
- [ ] Save login credentials in password manager

### Step 2: Set Up Google Workspace on Each Domain ($18/mo total)

```
Where: workspace.google.com
Cost: $6/month per mailbox = $18/month for 3

For each domain:
1. Go to workspace.google.com/signup
2. Enter domain name
3. Create admin account: outreach@[domain].com
4. Pick Google Workspace Starter ($6/month)
5. Verify domain ownership (add TXT record to DNS)

Create these 3 mailboxes:
1. outreach@printmaxxagency.com     (healthcare sequence)
2. outreach@printmaxxdev.com        (legal sequence)
3. outreach@printmaxxconsulting.com  (real estate sequence)
```

**Action:**
- [ ] Set up Google Workspace on domain 1
- [ ] Set up Google Workspace on domain 2
- [ ] Set up Google Workspace on domain 3
- [ ] Verify all 3 domains

### Step 3: Configure DNS Authentication (30 minutes)

For EACH domain, add these DNS records. Do this in Namecheap/Cloudflare DNS manager.

```
SPF Record:
- Type: TXT
- Host: @
- Value: v=spf1 include:_spf.google.com ~all
- TTL: Automatic

DKIM Record:
- Go to Google Workspace Admin > Apps > Gmail > Authenticate Email
- Click "Generate New Record"
- Copy the TXT record value
- Add to DNS as TXT record

DMARC Record:
- Type: TXT
- Host: _dmarc
- Value: v=DMARC1; p=none; rua=mailto:dmarc@[yourdomain].com
- TTL: Automatic
```

**Verify all 3:**
- Go to https://mxtoolbox.com/SuperTool.aspx
- Enter each domain
- Check SPF: PASS
- Check DKIM: PASS
- Check DMARC: PASS

**Action:**
- [ ] Add SPF record for domain 1
- [ ] Add DKIM record for domain 1
- [ ] Add DMARC record for domain 1
- [ ] Verify domain 1 on MXToolbox
- [ ] Repeat for domain 2
- [ ] Repeat for domain 3

### Step 4: Set Up Calendly (15 minutes)

```
Where: calendly.com (free tier works)
What to create:
1. 15-minute "Quick Chat" meeting type
2. 30-minute "Strategy Call" meeting type

Settings:
- Buffer time: 15 minutes between meetings
- Availability: Mon-Fri 9am-5pm your timezone
- Confirmation emails: ON
- Reminder emails: 24h and 1h before
- Questions: "What's your biggest challenge right now?" (optional, 1 question max)
```

**Action:**
- [ ] Create Calendly account
- [ ] Set up 15-min meeting type
- [ ] Set up 30-min meeting type
- [ ] Copy Calendly link for email signatures

---

## PHASE 1: Email Warmup (Days 1-21)

### Option A: Manual Warmup ($0, slower)

**Days 1-7: Personal Emails (10/day per inbox)**

```
Daily tasks per inbox (5 minutes each):
1. Send 5 emails to your personal gmail/yahoo/outlook accounts
2. Reply to those emails from the receiving account
3. Send 3 emails to friends/family and ask them to reply
4. Subscribe to 2 newsletters (generates real inbound)
5. Reply to any newsletters with a short comment

Total: 10 emails sent + 5-8 replies received per inbox per day
Time: 15 minutes per day across all 3 inboxes
```

**Days 8-14: Increase Volume (20/day per inbox)**

```
Daily tasks per inbox (10 minutes each):
1. Continue personal emails (5/day)
2. Start sending to business contacts you know (5/day)
3. Sign up for services that send confirmation emails (2/day)
4. Send cold emails to LOW-PRIORITY prospects as test (8/day)
5. Make sure you're getting real replies (ask contacts to reply)

Total: 20 emails sent + 8-12 replies received per inbox per day
```

**Days 15-21: Start Real Outreach (30-40/day per inbox)**

```
Mix per inbox:
- 5 personal/warmup emails (maintain engagement signals)
- 25-35 cold emails (real prospects)
- Track reply rates starting now

Total cold sends across 3 inboxes: 75-105/day
```

### Option B: Instantly.ai Warmup ($97/mo, faster)

```
1. Sign up at instantly.ai ($97/month)
2. Connect all 3 Google Workspace inboxes
3. Enable warmup on all 3 (auto sends + auto replies)
4. Settings: 30 emails/day warmup, gradual ramp
5. Let it run for 14 days untouched
6. Day 15: Start cold campaigns at 20/day per inbox
7. Day 22: Ramp to 50/day per inbox
8. Keep warmup running FOREVER (even during cold campaigns)
```

### Option C: DeliverOn Pre-Warmed ($49/mo, fastest)

```
1. Sign up at deliveron.io ($49/month)
2. Get 3 pre-warmed inboxes (skip 14-21 day wait)
3. Start sending cold emails Day 1 at 30/day per inbox
4. Ramp to 50/day per inbox after 7 days
5. Max: 50/day per inbox (their limit)
```

**Recommendation:** Use Option B (Instantly.ai) for the best balance of speed, deliverability monitoring, and campaign management. $97/mo pays for itself with 1 closed deal.

**Action:**
- [ ] Choose warmup option (A, B, or C)
- [ ] Begin warmup process
- [ ] Set calendar reminder for Day 15 (start cold sending)
- [ ] Set calendar reminder for Day 22 (ramp volume)

---

## PHASE 2: Build Prospect Lists (During Warmup Period)

### While your inboxes warm up, build lists. You need 200-500 contacts per vertical.

### Healthcare/Dental Lists

```
Source 1: Apollo.io (free, 50 credits/month)
1. Go to app.apollo.io
2. Create free account
3. Search: Title = "Owner" OR "Office Manager" OR "Practice Manager"
4. Industry = "Dental" OR "Healthcare"
5. Location = [your target city/state]
6. Company size = 2-50 employees
7. Export 50 contacts (free limit)

Source 2: Google Maps Scraping (free, unlimited)
1. Search Google Maps: "dentist in [city]"
2. Scroll through all results
3. For each practice, note: name, phone, website, address
4. Visit website, find email (usually on contact or about page)
5. Compile into CSV

Source 3: Healthgrades / Zocdoc (free)
1. Search by specialty and location
2. Get practice names
3. Cross-reference with Google/website for email

Email verification:
- Run all emails through NeverBounce (neverbounce.com, $8/1,000 emails)
- Or ZeroBounce (zerobounce.net, 100 free/month)
- Remove any bounced emails before sending
```

**Target:** 200 verified dental practice emails in your metro area.

### Legal Firm Lists

```
Source 1: State Bar Directory (free, most complete)
1. Google "[your state] bar association attorney search"
2. Filter by practice area: Personal Injury, Family Law, Estate Planning
3. Filter by city
4. Get attorney name, firm, location
5. Cross-reference with firm website for email

Source 2: Avvo.com (free)
1. Search by practice area and location
2. Get attorney profiles with firm info
3. Visit firm websites for emails

Source 3: Apollo.io
1. Title = "Managing Partner" OR "Attorney" OR "Founding Partner"
2. Industry = "Legal Services"
3. Location = [target city]
4. Export contacts

Email verification: Same as above (NeverBounce or ZeroBounce)
```

**Target:** 200 verified law firm emails in your metro area.

### Real Estate Agent Lists

```
Source 1: Realtor.com / Zillow Agent Finder (free)
1. Search agents in your target area
2. Many have email directly on profile
3. Note: brokerage, sales volume, specialty

Source 2: Google Maps
1. Search "real estate agent [city]"
2. Visit websites, get emails

Source 3: Your local MLS (if accessible)
1. Check your state's MLS for agent directories

Source 4: Apollo.io
1. Title = "Real Estate Agent" OR "Realtor" OR "Real Estate Broker"
2. Location = [target city]
3. Export contacts

Email verification: Same process.
```

**Target:** 200 verified real estate agent emails in your metro area.

**Action:**
- [ ] Create Apollo.io account (free)
- [ ] Build 200 dental practice contacts
- [ ] Build 200 law firm contacts
- [ ] Build 200 real estate agent contacts
- [ ] Verify all emails through NeverBounce ($4.80 for 600 emails)
- [ ] Save as CSVs: `dental_prospects.csv`, `legal_prospects.csv`, `realestate_prospects.csv`
- [ ] Upload to Instantly.ai or your sending tool

---

## PHASE 3: Launch Cold Campaigns (Day 15-21)

### Sending Schedule (Per Inbox)

| Day Range | Cold Emails/Day/Inbox | Total Across 3 Inboxes | Notes |
|-----------|----------------------|------------------------|-------|
| Day 15-17 | 10 | 30/day | Test deliverability |
| Day 18-21 | 20 | 60/day | Monitor bounce rates |
| Day 22-28 | 35 | 105/day | Ramp if bounce <3% |
| Day 29+ | 50 | 150/day | Steady state |
| Day 45+ | 70 | 210/day | Max safe volume |

### Campaign Setup in Instantly.ai

```
Campaign 1: Healthcare/Dental
- Inbox: outreach@printmaxxagency.com
- Sequence: Use EMAIL_SEQUENCES_TIER1.md Healthcare sequence
- List: dental_prospects.csv
- Schedule: Tue-Thu, 8:30-10:30am local time
- Daily limit: start 10, ramp to 50
- Tracking: replies only (NO open tracking, NO link tracking)

Campaign 2: Legal Firms
- Inbox: outreach@printmaxxdev.com
- Sequence: Use EMAIL_SEQUENCES_TIER1.md Legal sequence
- List: legal_prospects.csv
- Schedule: Tue-Thu, 9:00-11:00am local time
- Daily limit: start 10, ramp to 50

Campaign 3: Real Estate
- Inbox: outreach@printmaxxconsulting.com
- Sequence: Use TIER1_COLD_EMAIL_SEQUENCES.md Real Estate sequence
- List: realestate_prospects.csv
- Schedule: Mon-Wed, 10:00am-12:00pm local time
- Daily limit: start 10, ramp to 50
```

### Critical Rules

```
DO:
- Keep warmup running even during campaigns
- Respond to all replies within 2 hours
- Track reply rates daily
- A/B test subject lines after 50 sends per variant
- Personalize {{PRACTICE_NAME}} and {{CITY}} for EVERY email
- Include unsubscribe in every email (CAN-SPAM)

DO NOT:
- Use open tracking pixels (Gmail warns users in 2026)
- Use link tracking (flags as marketing email)
- Send more than 80 emails/day per inbox
- Send on weekends
- Send to unverified emails (bounce = deliverability death)
- Use images in cold emails (text only)
- Use more than 1 link per email (just calendly)
```

**Action:**
- [ ] Set up Campaign 1 (Healthcare)
- [ ] Set up Campaign 2 (Legal)
- [ ] Set up Campaign 3 (Real Estate)
- [ ] Send first 10 test emails per campaign
- [ ] Monitor for bounces (must be <3%)
- [ ] Ramp daily as scheduled

---

## PHASE 4: Templates for All Targets

### Template 1: Local Business Website Redesign (FREE AUDIT HOOK)

This is the highest-converting cold email. You send a FREE automated website audit before asking for anything.

**How the free hook works:**
1. Run `python3 AUTOMATIONS/local_biz_website_scraper.py` on prospect's URL
2. Get their site quality score, missing features, specific issues
3. Reference the SPECIFIC issues in your cold email
4. Offer free full audit -> they get on a call -> upsell to paid redesign ($500-3,000)

**Email 1 (Day 1) - Free Audit Hook**

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

{{YOUR_NAME}}
{{PHONE}}

PS - reply "remove" and you won't hear from me again.
```

**Email 2 (Day 4) - ROI Math**

Subject: re: {{BUSINESS_NAME}} website

```
{{FIRST_NAME}},

following up on the audit.

quick math: {{BUSINESS_NAME}} probably gets 200-500 website visitors per month. at your current conversion rate (~2%), that's 4-10 leads.

fix the 3 issues I found, conversion goes to 4-6%. same traffic, 2-3x more leads.

that's 8-30 leads per month instead of 4-10. at your average job value, that's ${{ADDITIONAL_REVENUE}}/month.

fix costs $500-1,500 depending on scope. timeline: 2 weeks.

worth 15 minutes? [CALENDLY]

{{YOUR_NAME}}
```

**Email 3 (Day 7) - Social Proof**

Subject: how {{SIMILAR_BUSINESS}} in {{CITY}} fixed this

```
{{FIRST_NAME}},

{{SIMILAR_BUSINESS}} had the same issues. slow site, no mobile optimization, terrible Google Business listing.

rebuilt their site in 12 days. results after 60 days:
- page load: 6.2s to 1.8s
- mobile conversion: up 89%
- new customer calls: 4/week to 11/week

cost them $1,200. paid for itself in 3 weeks.

your site has the same problems. same fix applies.

want the case study? reply "yes" and I'll send it.

{{YOUR_NAME}}
```

**Email 4 (Day 14) - Breakup + Free Tool**

Subject: last email + free tool

```
{{FIRST_NAME}},

last one from me. but I built something you might find useful.

free speed test tool that shows exactly what's slowing your site: [LINK]

takes 30 seconds. shows your score vs competitors in {{CITY}}.

if you ever want the full fix: $500-1,500, 2 weeks, mobile-responsive, SEO-optimized, SSL secured.

good luck with {{BUSINESS_NAME}}.

{{YOUR_NAME}}

reply "remove" to unsubscribe.
```

### Template 2: Course Creator Video Clipping

**Target:** YouTubers, course creators, podcast hosts with 10K-500K subscribers
**Hook:** Send them a FREE sample clip from their latest video

**Email 1 (Day 1) - Free Clip Sample**

Subject: clipped your latest video

```
{{FIRST_NAME}},

grabbed your latest video "{{VIDEO_TITLE}}" and pulled 3 clips that would crush on short-form:

1. [timestamp] - {{HOOK_DESCRIPTION_1}} (30 sec)
2. [timestamp] - {{HOOK_DESCRIPTION_2}} (45 sec)
3. [timestamp] - {{HOOK_DESCRIPTION_3}} (20 sec)

sample clip attached: [LINK_TO_CLIP]

we do this for 6 creators. average: 3 clips per video, 15-30 clips per month. creators see 30-60% more subscribers from short-form repurposing.

cost: $500-1,500/month depending on volume.

worth trying? first batch is free if you want to test quality.

{{YOUR_NAME}}
```

**Follow-up 1 (Day 3)**

Subject: re: clips from {{VIDEO_TITLE}}

```
{{FIRST_NAME}},

circling back on the clips.

if you're already clipping content, great. most creators we talk to either:
1. don't clip at all (leaving views on the table)
2. clip themselves (spending 3-5 hours per video)
3. have a team but quality is inconsistent

we handle the full pipeline: download -> transcribe -> identify hooks -> cut -> add captions -> optimize for each platform (TikTok, Shorts, Reels).

turnaround: 24-48 hours per video.

did you check the sample clip? [LINK]

{{YOUR_NAME}}
```

**Follow-up 2 (Day 7)**

Subject: this is what 30 clips per month looks like

```
{{FIRST_NAME}},

{{SIMILAR_CREATOR}} was posting 1 video per week on YouTube. no short-form presence.

we started clipping: 4-5 clips per video, 20 clips per month across TikTok, Shorts, and Reels.

6 months later:
- YouTube subscribers: +47K (from short-form discovery)
- TikTok followers: 0 to 89K
- Monthly video revenue: up 34% (more views on long-form from shorts traffic)

total cost: $800/month. ROI: 12x.

your channel has the content. you just need the clips.

try one video free: [CALENDLY]

{{YOUR_NAME}}
```

**Breakup (Day 14)**

Subject: moving on

```
{{FIRST_NAME}},

last email. the sample clip is still here if you want it: [LINK]

if video clipping ever becomes a priority: $500-1,500/month, 24-48h turnaround, all platforms.

keep making great content.

{{YOUR_NAME}}
```

### Template 3: SaaS Company Content Writing

**Email 1 (Day 1)**

Subject: your blog hasn't been updated in {{DAYS}} days

```
{{FIRST_NAME}},

checked {{COMPANY}}'s blog. last post was {{LAST_POST_DATE}}. that's {{DAYS}} days ago.

google deprioritizes stale sites. your competitors publishing weekly are taking your search traffic.

we write SEO-optimized blog content for SaaS companies. 4 posts per month, $800/month. each post targets keywords your competitors are ranking for.

one client went from 2,000 to 11,000 organic visitors in 5 months. same product, better content.

want to see what keywords {{COMPANY}} should target? I'll pull a free report.

reply "keywords" and I'll send it.

{{YOUR_NAME}}
```

### Template 4: Newsletter Growth Consulting

**Email 1 (Day 1)**

Subject: {{NEWSLETTER_NAME}} growth

```
{{FIRST_NAME}},

subscribed to {{NEWSLETTER_NAME}}. good content. but I noticed a few growth levers you're not pulling:

1. no referral program (SparkLoop adds 20-30% organic growth)
2. no cross-promotion with similar newsletters (free subscriber swap)
3. landing page converts ~2% (benchmark is 15-25% for newsletters)

we've helped 4 newsletters grow from {{CURRENT_SIZE}} to {{TARGET_SIZE}} in 3-6 months.

tactics: referral programs, cross-promotions, landing page optimization, paid growth ($0.50-2 per subscriber on Meta).

15-min call to see what would work for {{NEWSLETTER_NAME}}? [CALENDLY]

{{YOUR_NAME}}
```

---

## PHASE 5: FREE HOOK STRATEGY (Key Differentiator)

The secret to high reply rates: give something valuable BEFORE asking for anything.

### Free Hook 1: Automated Website Audit

```
Process:
1. Run local_biz_pipeline.py on prospect's website
2. Generate personalized audit report (mobile speed, SEO, missing features)
3. Record 3-min Loom video walking through findings
4. Send Loom link in Email 1

Cost: $0 (your time: 5 min per prospect)
Reply rate boost: 3-5x vs generic cold email
```

### Free Hook 2: Sample Content Clip

```
Process:
1. Download prospect's latest YouTube video (yt-dlp)
2. Run through auto-clip pipeline (whisper -> claude -> ffmpeg)
3. Generate 1 sample clip with captions
4. Attach clip in Email 1

Cost: $0 (pipeline already built)
Reply rate boost: 5-10x (they see the actual deliverable)
```

### Free Hook 3: Newsletter Growth Audit

```
Process:
1. Subscribe to their newsletter
2. Analyze: landing page conversion estimate, referral program presence, content frequency
3. Write 3 specific improvement suggestions
4. Send in Email 1

Cost: $0 (15 min per prospect)
Reply rate boost: 3-4x
```

### Free Hook 4: Keyword Research Report

```
Process:
1. Run their domain through free SEO tool (Ubersuggest free, or SEMrush free trial)
2. Pull top 10 keywords they should rank for but don't
3. Show competitor keywords they're missing
4. Send as PDF attachment or Loom walkthrough

Cost: $0
Reply rate boost: 2-3x
```

---

## TRACKING

### What to Track (Weekly)

| Metric | Where | Target |
|--------|-------|--------|
| Emails sent per day | Instantly.ai dashboard | 100-200/day |
| Bounce rate | Instantly.ai dashboard | <3% |
| Reply rate | Instantly.ai dashboard | 5-12% |
| Positive reply rate | Manual tracking | 2-5% |
| Calls booked | Calendly dashboard | 3-8/week |
| Deals closed | LEDGER/OUTREACH_PIPELINE.csv | 1-2/month |
| Revenue per deal | FINANCIALS/REVENUE_TRACKER.csv | $500-3,000 |

### Update Pipeline CSV After Every Interaction

```
File: LEDGER/OUTREACH_PIPELINE.csv
Columns: prospect_id,company,contact_name,email,linkedin_url,offer_type,sequence_name,status,sent_date,last_response,deal_value,notes

Status values:
- COLD (not yet contacted)
- SENT (email sent, no reply)
- REPLIED (got a reply)
- CALL_BOOKED (meeting scheduled)
- PROPOSAL_SENT (sent pricing)
- DEAL_CLOSED (payment received)
- LOST (declined or went cold)
```

---

## TIMELINE SUMMARY

| Week | Activity | Output |
|------|----------|--------|
| Week 1 | Buy domains, set up Workspace, configure DNS, start warmup | Infrastructure ready |
| Week 1-2 | Build prospect lists (600 contacts across 3 verticals) | 3 CSVs ready |
| Week 2-3 | Continue warmup, prep Loom audit videos for top 20 prospects | 20 personalized audits |
| Week 3 | Start cold sending at 30/day (10/inbox) | First replies |
| Week 4 | Ramp to 100/day, book first calls | 3-8 calls booked |
| Week 5-6 | Continue campaigns, A/B test subject lines | Optimize for >5% reply |
| Week 6-8 | Close first deals | $500-3,000 first revenue |
| Week 8+ | Steady state: 150-200 emails/day, 2-5 deals/month | $1,000-10,000/mo |

### Total Startup Costs

| Item | Cost | Recurring |
|------|------|-----------|
| 3 cold email domains | $30-45 | $30-45/year |
| Google Workspace (3 inboxes) | $18/mo | Monthly |
| Instantly.ai (or equivalent) | $97/mo | Monthly |
| NeverBounce email verification | ~$5-10 | Per batch |
| Calendly | $0 (free tier) | Free |
| **Total Month 1** | **$150-170** | |
| **Total Monthly Ongoing** | **$115/mo** | |

### Expected Returns

| Timeframe | Cold Emails Sent | Replies | Calls | Deals | Revenue |
|-----------|-----------------|---------|-------|-------|---------|
| Month 1 | 500-1,000 | 25-50 | 5-10 | 0-1 | $0-1,500 |
| Month 2 | 2,000-3,000 | 100-150 | 15-30 | 1-3 | $500-5,000 |
| Month 3 | 3,000-4,500 | 150-225 | 20-40 | 2-5 | $1,000-10,000 |

**Break-even:** 1 deal at $500+ covers 3-4 months of infrastructure costs.

---

**Status:** NOT_STARTED. Begin Phase 0 (buy domains + set up Workspace) today. Everything else follows sequentially.
