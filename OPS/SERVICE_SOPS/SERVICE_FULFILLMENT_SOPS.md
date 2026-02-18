# Service Fulfillment SOPs

**Purpose:** Step-by-step checklists for delivering all 8 PRINTMAXX services. Use these to train VAs or execute yourself.

**Philosophy:** Under-promise, over-deliver. Ship early if possible. Communicate proactively.

---

## Service 1: Paywall Implementation Call ($500, 90 min)

### Pre-Engagement Checklist

**Before scheduling:**
- [ ] Receive client's app (TestFlight invite or GitHub access)
- [ ] Verify app uses React Native, Swift, or Kotlin (confirm tech stack)
- [ ] Request current paywall screenshots (if exists)
- [ ] Send pre-call questionnaire: current MRR, conversion rate, subscription tiers, target user
- [ ] Create shared Notion doc for call notes and deliverables

**24 hours before call:**
- [ ] Test client's app on device
- [ ] Screenshot current paywall (or lack of)
- [ ] Review RevenueCat docs for their platform
- [ ] Prepare 3 paywall design examples from high-converting apps
- [ ] Set up screen recording software (Loom or QuickTime)

### Fulfillment Process (180 min total)

**Phase 1: Pre-Call Prep (30 min)**
- [ ] 10 min: Review client's app flow, note friction points
- [ ] 10 min: Research competitor apps' paywalls in App Store
- [ ] 10 min: Draft initial paywall copy variants (3 options)

**Phase 2: During Call (90 min)**
- [ ] 0-5 min: Intro, set agenda, confirm goals
- [ ] 5-25 min: Screen share walkthrough of current state
- [ ] 25-45 min: Design 6-screen onboarding flow together
  - Screen 1: Value prop
  - Screen 2: Key feature 1
  - Screen 3: Key feature 2
  - Screen 4: Social proof
  - Screen 5: Paywall with pricing
  - Screen 6: Post-purchase confirmation
- [ ] 45-70 min: Live RevenueCat configuration
  - Create products (monthly, yearly)
  - Set pricing
  - Configure offerings
  - Walk through iOS/Android setup
- [ ] 70-85 min: Copy variants walkthrough (3 options)
- [ ] 85-90 min: Action items recap, next steps

**Phase 3: Post-Call Delivery (60 min)**
- [ ] 20 min: Edit call recording, export key moments
- [ ] 20 min: Write action items doc with screenshots
- [ ] 15 min: Create 3 paywall copy variants in Google Doc
- [ ] 5 min: Export RevenueCat config (JSON file)
- [ ] Send completion email with all deliverables

### Deliverables Checklist

- [ ] Call recording (Loom link, full 90 min + edited highlights)
- [ ] Action items doc (Notion or Google Doc)
- [ ] 6-screen onboarding flow (mockup in Figma or annotated screenshots)
- [ ] 3 paywall copy variants (Google Doc)
- [ ] RevenueCat config file (JSON)
- [ ] Competitor analysis notes (3-5 apps with paywall screenshots)

### Quality Control Checkpoints

- [ ] Client confirms understanding of RevenueCat setup
- [ ] All 6 screens designed and approved during call
- [ ] Copy variants match client's brand voice
- [ ] Action items are specific and timestamped
- [ ] Client has clear next steps

### Client Communication Templates

**Welcome Email (send immediately after booking):**
```
subject: paywall call prep - action needed

hi [name],

call is scheduled for [date/time].

before the call, please:
1. send me TestFlight invite or GitHub access to your app
2. fill out this 2-min form: [link to typeform]
3. screenshot your current paywall (if you have one)

i'll send a Notion doc 24 hours before with my initial notes.

- printmaxx team
```

**24-Hour Reminder:**
```
subject: tomorrow's call - here's my prep

hi [name],

call tomorrow at [time]. here's what i found:

[link to Notion doc with initial analysis]

i tested your app and prepared 3 paywall examples. we'll design your flow live on the call.

zoom link: [link]

- printmaxx
```

**Completion Email:**
```
subject: call recording + deliverables

hi [name],

here's everything:

1. call recording: [loom link]
2. action items: [notion link]
3. 6-screen onboarding flow: [figma/doc link]
4. 3 paywall copy variants: [doc link]
5. revenuecat config: [json file]

next steps:
- implement the onboarding flow (or hire a dev)
- choose one copy variant and A/B test
- configure revenuecat following my notes

i'm available for quick questions via email for 2 weeks.

- printmaxx
```

### Tools Needed

- Zoom or Google Meet (screen sharing)
- Loom or QuickTime (recording)
- Figma or Excalidraw (mockups)
- RevenueCat account
- Notion or Google Docs (deliverables)
- iOS Simulator or Android Emulator (for testing)

### Common Issues & Solutions

**Issue:** Client doesn't have TestFlight/GitHub access ready
- **Solution:** Reschedule call, don't wing it without seeing the app

**Issue:** Client's app uses unsupported platform (Flutter without RevenueCat plugin)
- **Solution:** Offer to research alternative (Adapty, custom Stripe integration), charge extra $200 for setup complexity

**Issue:** Client wants more than 90 min of work during call
- **Solution:** Hard stop at 90 min, offer follow-up at $150/30min rate

**Issue:** RevenueCat setup fails during call (API errors, config issues)
- **Solution:** Document the error, pivot to design work, follow up async with RevenueCat support

**Issue:** Client doesn't like any of the 3 copy variants
- **Solution:** Offer 1 round of revisions included, or upsell to full copywriting service

---

## Service 2: Full Paywall Build-Out ($750)

### Pre-Engagement Checklist

**Before starting:**
- [ ] Receive GitHub repo access or create new branch
- [ ] Confirm tech stack (React Native, Swift, Kotlin, Flutter)
- [ ] Request design assets (brand colors, fonts, logo)
- [ ] Get sample copy or brand voice guidelines
- [ ] Set up RevenueCat account (or get client's API keys)
- [ ] Create project tracking board (Linear, Notion, or Trello)

**Kickoff call prep (30 min before):**
- [ ] Review client's app in TestFlight/APK
- [ ] Prepare 3-5 paywall design references
- [ ] Draft initial timeline (usually 7-10 days)

### Fulfillment Process (10-15 hours over 7-10 days)

**Phase 1: Kickoff Call (30 min)**
- [ ] 0-10 min: Confirm goals, pricing tiers, target conversion rate
- [ ] 10-20 min: Walkthrough design references, get style preferences
- [ ] 20-30 min: Agree on timeline and review milestones

**Phase 2: Design Phase (3-4 hours)**
- [ ] 60 min: Create 3 paywall variants in Figma (or code prototypes)
  - Variant A: Minimal (price + CTA)
  - Variant B: Feature list (bullets + price)
  - Variant C: Social proof (testimonials + price)
- [ ] 30 min: Design 6-screen onboarding flow
- [ ] 30 min: Client review and feedback
- [ ] 60 min: Revisions (1 round included)
- [ ] 30 min: Export design specs (spacing, colors, copy)

**Phase 3: Development (5-7 hours)**
- [ ] 90 min: Set up RevenueCat SDK in app
- [ ] 120 min: Build paywall UI component
- [ ] 90 min: Build 6-screen onboarding flow
- [ ] 60 min: Integrate purchase logic (subscriptions, restore)
- [ ] 30 min: Add analytics events (paywall_shown, purchase_initiated, purchase_completed)

**Phase 4: Testing (2 hours)**
- [ ] 30 min: Test monthly subscription purchase (sandbox)
- [ ] 30 min: Test yearly subscription purchase (sandbox)
- [ ] 20 min: Test restore purchases flow
- [ ] 20 min: Test edge cases (no internet, cancelled purchase, price loading errors)
- [ ] 20 min: Test on multiple devices (iPhone, iPad, Android if applicable)

**Phase 5: Delivery (1 hour)**
- [ ] 20 min: Create pull request with detailed notes
- [ ] 20 min: Record Loom walkthrough of code changes
- [ ] 20 min: Write handoff doc (how to deploy, how to A/B test, how to change pricing)

**Phase 6: Post-Launch Review Call (30 min, 2 weeks later)**
- [ ] 10 min: Review conversion data
- [ ] 10 min: Discuss A/B test ideas
- [ ] 10 min: Answer questions, troubleshoot issues

### Deliverables Checklist

- [ ] 3 paywall design variants (Figma or coded prototypes)
- [ ] 6-screen onboarding flow (fully functional)
- [ ] RevenueCat integration (SDK configured, products set up)
- [ ] Purchase logic (subscribe, restore, handle errors)
- [ ] Analytics events (paywall shown, purchase initiated, completed)
- [ ] Code via GitHub PR (or zip file if no repo)
- [ ] Loom walkthrough (15-20 min)
- [ ] Handoff doc (deployment, A/B testing, pricing changes)
- [ ] 30-min post-launch review call (2 weeks after deployment)

### Quality Control Checkpoints

- [ ] Paywall renders correctly on all device sizes
- [ ] Purchases work in sandbox mode (monthly + yearly)
- [ ] Restore purchases works
- [ ] No console errors or crashes
- [ ] Copy is typo-free and matches brand voice
- [ ] Analytics events fire correctly
- [ ] Client can deploy without assistance

### Client Communication Templates

**Kickoff Email:**
```
subject: paywall build kickoff - [date/time]

hi [name],

kickoff call scheduled for [date/time].

before the call:
1. share your github repo or create a new branch for me
2. send brand assets (logo, colors, fonts)
3. confirm your pricing tiers (monthly, yearly, prices)

i'll prepare 3-5 design references to review on the call.

zoom link: [link]

- printmaxx
```

**Design Review Email:**
```
subject: paywall designs ready for review

hi [name],

here are 3 paywall variants: [figma link]

variant a: minimal (just price + cta)
variant b: feature list (bullets + price)
variant c: social proof (testimonials + price)

which one do you prefer? or mix elements from multiple?

i'll do 1 round of revisions, then move to dev.

- printmaxx
```

**Code Delivery Email:**
```
subject: paywall build complete - ready for review

hi [name],

code is ready: [github PR link or zip]

deliverables:
1. 3 paywall variants (fully coded)
2. 6-screen onboarding flow
3. revenuecat integration
4. purchase + restore logic
5. analytics events
6. loom walkthrough: [link]
7. handoff doc: [link]

test in sandbox, then deploy when ready.

post-launch review call in 2 weeks: [calendly link]

- printmaxx
```

**Post-Launch Follow-Up:**
```
subject: paywall live? let's review data

hi [name],

it's been 2 weeks since delivery. is the paywall live?

if yes, let's review conversion data on our call: [calendly link]

if not live yet, any blockers i can help with?

- printmaxx
```

### Tools Needed

- Figma (design mockups)
- Xcode or Android Studio (development)
- RevenueCat account
- GitHub (code delivery)
- Loom (walkthrough video)
- TestFlight or APK distribution (testing)
- Notion or Google Docs (handoff documentation)

### Common Issues & Solutions

**Issue:** Client doesn't have RevenueCat account
- **Solution:** Create one for them, hand over credentials after project

**Issue:** Sandbox purchases fail (Apple/Google setup issues)
- **Solution:** Walk client through sandbox tester setup, provide troubleshooting doc

**Issue:** Client wants unlimited revisions
- **Solution:** 1 round included, additional rounds at $150/round

**Issue:** Client's codebase is a mess (no version control, spaghetti code)
- **Solution:** Charge extra $250 for code cleanup, or deliver as standalone component they integrate

**Issue:** Client wants Android + iOS
- **Solution:** Price assumes 1 platform, charge +$400 for second platform

**Issue:** Client changes pricing tiers mid-project
- **Solution:** Update RevenueCat config, no extra charge if design doesn't change

---

## Service 3: Monthly Paywall Optimization ($300/mo)

### Pre-Engagement Checklist

**Before first month:**
- [ ] Verify client has live paywall with RevenueCat
- [ ] Get RevenueCat dashboard access (or API keys)
- [ ] Confirm they have at least 100 paywall views/month (minimum for statistical significance)
- [ ] Set up recurring monthly meeting (same day/time each month)
- [ ] Create shared tracking doc (Notion or Google Sheets)

### Fulfillment Process (2 hours/month)

**Monthly Cycle (runs on the same date each month):**

**Phase 1: Data Pull (20 min)**
- [ ] 10 min: Export RevenueCat A/B test results (if running tests)
- [ ] 5 min: Pull conversion rates by variant
- [ ] 5 min: Screenshot key metrics dashboard

**Phase 2: Analysis (40 min)**
- [ ] 15 min: Compare conversion rates vs benchmarks (industry avg 2-5%)
- [ ] 10 min: Price point analysis (monthly vs yearly mix)
- [ ] 10 min: Churn analysis (if enough data)
- [ ] 5 min: Identify biggest drop-off point in funnel

**Phase 3: Recommendations (20 min)**
- [ ] 10 min: Draft next A/B test hypothesis
- [ ] 10 min: Write specific copy/design changes to test

**Phase 4: Monthly Call (30 min)**
- [ ] 0-10 min: Review last month's data
- [ ] 10-20 min: Present recommendations
- [ ] 20-25 min: Agree on next test
- [ ] 25-30 min: Action items and timeline

**Phase 5: Delivery (10 min)**
- [ ] 5 min: Update shared tracking doc
- [ ] 5 min: Send follow-up email with notes

### Deliverables Checklist

- [ ] Monthly performance report (conversion rate, revenue, churn)
- [ ] Benchmark comparison (vs industry averages)
- [ ] Next A/B test recommendation (hypothesis + variants)
- [ ] 30-min monthly call recording
- [ ] Written notes with action items

### Quality Control Checkpoints

- [ ] Data is accurate (matches client's dashboard)
- [ ] Recommendations are specific (not vague "test different copy")
- [ ] Next test has clear hypothesis and success criteria
- [ ] Client understands how to implement recommendations
- [ ] Tracking doc is updated before call

### Client Communication Templates

**Monthly Reminder (3 days before call):**
```
subject: monthly paywall review - [date]

hi [name],

monthly call on [date] at [time].

i pulled your data:
- conversion rate: [x]%
- monthly vs yearly mix: [x]% / [x]%
- total revenue: $[x]

i'll share full analysis on the call.

zoom link: [link]

- printmaxx
```

**Post-Call Summary:**
```
subject: paywall optimization notes - [month]

hi [name],

here's what we covered:

last month:
- conversion rate: [x]% (vs [x]% prior month)
- revenue: $[x]
- churn: [x]%

recommendation:
test [specific change] to improve [metric].

hypothesis: [why this should work]

next steps:
1. [action item 1]
2. [action item 2]

next call: [date/time]

full notes: [link to tracking doc]

- printmaxx
```

### Tools Needed

- RevenueCat dashboard access
- Zoom or Google Meet
- Notion or Google Sheets (tracking)
- Loom (if recording async recommendations)

### Common Issues & Solutions

**Issue:** Client doesn't have enough traffic for statistical significance
- **Solution:** Focus on qualitative feedback (user interviews, surveys) instead of A/B tests

**Issue:** Client hasn't implemented last month's recommendation
- **Solution:** Charge for implementation ($200-500) or pause optimization until they catch up

**Issue:** Conversion rate is stuck (no improvement for 3+ months)
- **Solution:** Recommend bigger changes (complete redesign, pricing change, value prop shift)

**Issue:** Client cancels recurring service after 2 months
- **Solution:** Offer one-time audit instead ($500) or pause/resume as needed

---

## Service 4: Cold Email Infrastructure Setup ($1,000)

### Pre-Engagement Checklist

**Before starting:**
- [ ] Confirm client's primary domain (don't use it for cold email)
- [ ] Get client's registrar login (Namecheap, GoDaddy, etc.) or buy domains yourself
- [ ] Decide on 3 domain names (variations of primary brand)
- [ ] Confirm email warmup budget ($60-150/month for 3 accounts)
- [ ] Get client's ICP (Ideal Customer Profile) for sequence writing

### Fulfillment Process (8-10 hours over 14 days)

**Phase 1: Domain Setup (Day 1, 2 hours)**
- [ ] 30 min: Purchase 3 domains (Namecheap, $10-15 each)
  - Example: if primary is `printmaxx.com`, buy `tryPrintmaxx.com`, `getPrintmaxx.io`, `printmaxx.co`
- [ ] 60 min: Configure DNS records for all 3 domains:
  - SPF: `v=spf1 include:_spf.google.com ~all`
  - DKIM: Generate via Google Workspace
  - DMARC: `v=DMARC1; p=none; rua=mailto:dmarc@[domain]`
  - MX records: Point to Google Workspace or email provider
- [ ] 30 min: Verify all records propagated (use MXToolbox)

**Phase 2: Email Account Setup (Day 1-2, 1 hour)**
- [ ] 30 min: Create 3 email accounts (Google Workspace or Outlook)
  - `hi@domain1.com`
  - `hello@domain2.com`
  - `team@domain3.com`
- [ ] 30 min: Set up email signatures (name, title, link, CTA)

**Phase 3: Warmup Initiation (Day 2, 1 hour)**
- [ ] 20 min: Sign up for warmup service (Instantly, Smartlead, or Lemwarm)
- [ ] 20 min: Connect all 3 email accounts
- [ ] 20 min: Configure warmup settings:
  - Start at 5 emails/day per account
  - Ramp to 40-50/day over 14 days
  - Enable inbox rotation and spam folder checks

**Phase 4: Sequence Writing (Day 3-5, 3 hours)**
- [ ] 60 min: Research client's ICP (LinkedIn, competitor analysis)
- [ ] 90 min: Write 3 custom sequences (5 emails each):
  - Sequence 1: Problem-agitate-solve
  - Sequence 2: Case study / social proof
  - Sequence 3: Direct offer / low-friction CTA
- [ ] 30 min: Client review and revisions

**Phase 5: Lead List Strategy (Day 6-7, 2 hours)**
- [ ] 60 min: Document lead sourcing strategy:
  - Apollo.io filters (title, company size, industry)
  - LinkedIn Sales Navigator search criteria
  - Manual list building process (if applicable)
- [ ] 30 min: Build sample list (50-100 leads) to validate ICP
- [ ] 30 min: Client review and approval

**Phase 6: Deliverability Monitoring Setup (Day 8, 1 hour)**
- [ ] 20 min: Set up Google Postmaster Tools
- [ ] 20 min: Configure bounce handling (remove hard bounces immediately)
- [ ] 20 min: Set up weekly deliverability report (MXToolbox + warmup service)

**Phase 7: Training Call (Day 14, 1 hour)**
- [ ] 0-15 min: Walkthrough email accounts and warmup status
- [ ] 15-35 min: Review sequences and lead sourcing strategy
- [ ] 35-50 min: Demo how to send campaigns (Instantly, Smartlead, or Lemlist)
- [ ] 50-60 min: Q&A and troubleshooting

### Deliverables Checklist

- [ ] 3 domains purchased and configured
- [ ] DNS records (SPF, DKIM, DMARC, MX) verified
- [ ] 3 email accounts created and warmed (14-day warmup initiated)
- [ ] 3 custom email sequences (5 emails each, 15 total)
- [ ] Lead sourcing strategy doc (Apollo filters, LinkedIn criteria)
- [ ] Sample lead list (50-100 verified contacts)
- [ ] Deliverability monitoring setup (Google Postmaster, bounce handling)
- [ ] 1-hour training call (recorded)
- [ ] Access credentials doc (domains, emails, warmup service, sending platform)

### Quality Control Checkpoints

- [ ] All DNS records pass (SPF, DKIM, DMARC green on MXToolbox)
- [ ] Email warmup at 40+ emails/day per account by Day 14
- [ ] Sequences are personalized (not generic templates)
- [ ] Lead list matches client's ICP
- [ ] Client can log in and send test campaign independently
- [ ] Bounce rate <2% on sample sends

### Client Communication Templates

**Kickoff Email:**
```
subject: cold email setup starts today

hi [name],

starting your cold email infrastructure today.

i need:
1. your registrar login (to buy/configure domains)
2. ICP details: who are we emailing? (title, company size, industry)
3. any existing sequences or templates you like

timeline:
- day 1-2: domains + dns + emails
- day 3-5: sequence writing
- day 6-7: lead sourcing strategy
- day 14: training call (after warmup completes)

- printmaxx
```

**Mid-Project Update (Day 7):**
```
subject: cold email setup - 50% done

hi [name],

progress update:

✅ 3 domains purchased and configured
✅ dns records verified (spf, dkim, dmarc)
✅ 3 email accounts created
✅ warmup initiated (currently at 20 emails/day, ramping to 40+)
✅ 3 sequences written: [link to doc]

next:
- finish lead sourcing strategy
- training call on day 14

- printmaxx
```

**Completion Email:**
```
subject: cold email infrastructure ready

hi [name],

setup complete. here's everything:

1. 3 domains: [list]
2. 3 email accounts: [list]
3. warmup status: 40+ emails/day per account
4. 3 sequences (15 emails total): [doc link]
5. lead sourcing strategy: [doc link]
6. sample lead list (100 contacts): [csv link]
7. training call recording: [loom link]
8. credentials doc: [notion link]

you can start sending campaigns now. recommended volume: 50 emails/day per account (150/day total).

monitor deliverability weekly. i included a checklist in the credentials doc.

- printmaxx
```

### Tools Needed

- Domain registrar (Namecheap, GoDaddy)
- Email provider (Google Workspace, Outlook)
- Warmup service (Instantly, Smartlead, Lemwarm)
- Sending platform (Instantly, Smartlead, Lemlist)
- MXToolbox (DNS verification)
- Apollo.io or LinkedIn Sales Navigator (lead sourcing)
- Google Postmaster Tools (deliverability monitoring)

### Common Issues & Solutions

**Issue:** DNS records don't propagate (still showing errors after 48 hours)
- **Solution:** Check registrar's DNS settings, ensure no conflicting records, use CloudFlare if registrar DNS is slow

**Issue:** Client doesn't want to pay for Google Workspace ($6/user/month)
- **Solution:** Use free Outlook.com accounts (less reliable but works for small volume)

**Issue:** Warmup service rejects accounts (spam score too high)
- **Solution:** Wait 3-5 days, send manual emails to friends first, then re-connect

**Issue:** Client's ICP is too broad ("anyone who needs X")
- **Solution:** Force them to pick 1 vertical for first campaign, expand later

**Issue:** Sequences are too salesy/spammy
- **Solution:** Rewrite with problem-first approach, remove all hype words, add personalization variables

**Issue:** Client wants to start sending before warmup completes
- **Solution:** Explain deliverability risk, offer compromise (send 10/day manually while warmup continues)

---

## Service 5: Managed Cold Outreach ($500-2,000/mo)

### Pre-Engagement Checklist

**Before first month:**
- [ ] Confirm client has warmed email infrastructure (or upsell Service 4)
- [ ] Get access to email accounts and sending platform
- [ ] Confirm lead sourcing responsibility (client provides or we source)
- [ ] Agree on volume tier:
  - **Tier 1 ($500/mo):** 500 emails/month, client provides leads
  - **Tier 2 ($1,000/mo):** 1,500 emails/month, we source leads
  - **Tier 3 ($2,000/mo):** 3,000 emails/month, we source leads + A/B testing
- [ ] Set up Slack or email for warm reply forwarding
- [ ] Create tracking spreadsheet (reply rate, meeting rate, bounce rate)

### Fulfillment Process (5-10 hours/week depending on tier)

**Weekly Cycle (repeats every week):**

**Monday: Lead Sourcing and Verification (1-3 hours)**
- [ ] 30-60 min: Source leads via Apollo, LinkedIn Sales Navigator, or manual research
  - Tier 1: client provides, skip this step
  - Tier 2: source 375 leads/week
  - Tier 3: source 750 leads/week
- [ ] 30-60 min: Verify emails (NeverBounce, ZeroBounce, or Hunter.io)
- [ ] 15 min: Remove duplicates and previous contacts
- [ ] 15 min: Upload to sending platform with personalization variables

**Tuesday: Sequence Loading and Scheduling (1 hour)**
- [ ] 20 min: Load verified leads into campaign
- [ ] 20 min: QA personalization (check merge tags, preview 5-10 emails)
- [ ] 20 min: Schedule sends (spread throughout week, avoid Mondays/Fridays)

**Daily: Deliverability and Reply Monitoring (15-30 min/day)**
- [ ] 10 min: Check bounce rate (pause campaign if >5%)
- [ ] 10 min: Check spam complaints (pause if any)
- [ ] 10 min: Flag warm replies for client (forward to Slack or email)
  - Warm reply = asks question, shows interest, or requests meeting
  - Cold reply = unsubscribe, not interested (mark as closed)

**Friday: Weekly Performance Report (1 hour)**
- [ ] 20 min: Compile metrics:
  - Emails sent
  - Bounce rate
  - Reply rate (total replies / emails sent)
  - Positive reply rate (warm replies / emails sent)
  - Meeting rate (meetings booked / emails sent)
- [ ] 20 min: Screenshot top-performing emails
- [ ] 20 min: Write summary with recommendations

**Tier 3 Only: A/B Testing (additional 2 hours/week)**
- [ ] 30 min: Design A/B test (subject line, email 1 copy, CTA)
- [ ] 30 min: Split leads 50/50 and load both variants
- [ ] 30 min: Monitor results mid-week
- [ ] 30 min: Declare winner and scale winning variant

### Deliverables Checklist

- [ ] Leads sourced and verified (Tier 2-3 only)
- [ ] Campaigns loaded and scheduled weekly
- [ ] Warm replies forwarded same-day
- [ ] Bounce management (hard bounces removed immediately)
- [ ] Weekly performance report (sent every Friday)
- [ ] Monthly summary (sent on last day of month)

**Tier 3 additional deliverables:**
- [ ] A/B test results (2-4 tests/month)
- [ ] Winning sequence documentation

### Quality Control Checkpoints

- [ ] Bounce rate <3% (pause campaign if higher)
- [ ] No spam complaints
- [ ] Personalization variables populate correctly (no "Hi {firstname}" sends)
- [ ] Warm replies forwarded within 2 hours
- [ ] Weekly report sent by Friday 5pm

### Client Communication Templates

**Weekly Report:**
```
subject: cold outreach report - week of [date]

hi [name],

this week's numbers:

📧 emails sent: [x]
📩 replies: [x] ([x]% reply rate)
✅ positive replies: [x]
📅 meetings booked: [x]
⚠️ bounce rate: [x]%

top performer:
subject line: "[subject]"
reply rate: [x]%

warm replies forwarded to your slack.

next week: sending [x] emails starting monday.

- printmaxx
```

**Monthly Summary:**
```
subject: cold outreach summary - [month]

hi [name],

[month] performance:

📧 total emails: [x]
📩 total replies: [x] ([x]% reply rate)
✅ positive replies: [x] ([x]% positive rate)
📅 meetings booked: [x] ([x]% meeting rate)
⚠️ avg bounce rate: [x]%

best performing sequence:
[sequence name] - [x]% reply rate

[tier 3 only]
A/B tests run: [x]
winning variant improved reply rate by [x]%

recommendations for next month:
1. [recommendation 1]
2. [recommendation 2]

- printmaxx
```

**Warm Reply Forward (Slack or Email):**
```
🔥 warm reply from [name] at [company]

their reply:
"[reply text]"

original email thread: [link]

suggested response: [optional - include if client wants this]
```

### Tools Needed

- Sending platform (Instantly, Smartlead, Lemlist)
- Lead sourcing (Apollo, LinkedIn Sales Navigator)
- Email verification (NeverBounce, ZeroBounce)
- Bounce monitoring (built into sending platform)
- Slack or email (warm reply forwarding)
- Google Sheets or Airtable (tracking)

### Common Issues & Solutions

**Issue:** Bounce rate spikes above 5%
- **Solution:** Pause campaign immediately, re-verify leads, check if list is stale

**Issue:** Client doesn't respond to warm replies fast enough (>24 hours)
- **Solution:** Offer to write first response on their behalf (+$200/mo), or set up auto-reply holding pattern

**Issue:** Reply rate drops below 1%
- **Solution:** Test new subject lines, rewrite email 1, check if ICP shifted

**Issue:** Client provides bad leads (wrong titles, wrong companies)
- **Solution:** Source leads yourself (upsell to Tier 2/3), or create detailed ICP doc and require approval

**Issue:** Spam complaints (even 1 is bad)
- **Solution:** Pause campaign, review copy for spammy language, ensure unsubscribe link is visible, check if list was scraped vs opted-in

**Issue:** Client wants daily reports instead of weekly
- **Solution:** Set up automated daily email from sending platform, or charge extra $100/mo for daily manual reports

---

## Service 6: Clipping Operation Setup ($1,500)

### Pre-Engagement Checklist

**Before starting:**
- [ ] Confirm client has content to clip (podcast, YouTube videos, streams)
- [ ] Get access to source content (YouTube channel, podcast RSS, Twitch)
- [ ] Agree on distribution channels (YouTube Shorts, TikTok, Instagram Reels)
- [ ] Set clip volume (30 clips/month minimum for algorithm traction)
- [ ] Get brand assets (logo, colors, fonts, intro/outro templates)

### Fulfillment Process (15-20 hours over 2 weeks)

**Phase 1: Clipper Hiring (Week 1, 4-6 hours)**
- [ ] 60 min: Post job on Fiverr, Upwork, OnlineJobs.ph
  - **Job title:** "Video clipper for [niche] content"
  - **Requirements:** Premiere Pro or CapCut, 10+ clips/week, fast turnaround
  - **Rate:** $3-8/clip (Eastern Europe, Philippines, LatAm)
- [ ] 120 min: Review applications (50-100 expected)
  - Check portfolio (watch 5-10 clips)
  - Check turnaround time claims
  - Check English communication skills
- [ ] 60 min: Conduct 3-5 short interviews (15 min each)
  - Ask: "What makes a clip go viral?"
  - Ask: "How do you choose which moments to clip?"
  - Test: "Clip this 10-min video and send me 3 clips in 24 hours"
- [ ] 30 min: Hire top 3 clippers (redundancy in case 1 flakes)

**Phase 2: Training Documentation (Week 1, 3-4 hours)**
- [ ] 90 min: Write clipper SOP:
  - How to access source content
  - Clip selection criteria (high-energy moments, controversial takes, actionable tips)
  - Editing style guide (captions, zoom-ins, music)
  - Naming convention (YYYY-MM-DD_topic_platform.mp4)
  - Delivery method (Google Drive, Dropbox)
- [ ] 60 min: Create example clips (good vs bad)
- [ ] 30 min: Record Loom training video (10-15 min)
- [ ] 30 min: Build clipper onboarding checklist

**Phase 3: Distribution Channel Setup (Week 1, 2-3 hours)**
- [ ] 45 min: Create accounts (YouTube Shorts, TikTok, Instagram Reels)
  - Optimize bios (link to main channel/product)
  - Add brand colors and profile pic
  - Enable monetization where possible
- [ ] 45 min: Set up posting tools (Publer, Buffer, or Later)
- [ ] 45 min: Build 30-day content calendar template
- [ ] 15 min: Configure analytics tracking (native platform analytics + optional: Dashthis)

**Phase 4: First Month Content Calendar (Week 1-2, 2 hours)**
- [ ] 60 min: Review client's last 10 long-form videos/episodes
- [ ] 30 min: Identify 30-50 high-potential moments to clip
- [ ] 30 min: Create content calendar (which clips post when, which platforms)

**Phase 5: Quality Control Framework (Week 2, 2 hours)**
- [ ] 60 min: Write QC checklist for client:
  - Captions accurate and readable
  - Audio levels consistent
  - No dead air at start/end
  - Thumbnail eye-catching
  - Hook in first 3 seconds
- [ ] 30 min: Create example QC sheet (Google Sheet or Notion)
- [ ] 30 min: Document revision process (how to request changes from clippers)

**Phase 6: Management Training Calls (Week 2, 2 hours total)**
- [ ] **Call 1 (60 min):** Clipper management
  - How to assign work to clippers
  - How to review clips for quality
  - How to handle revisions and missed deadlines
  - How to scale (hire more clippers as volume grows)
- [ ] **Call 2 (60 min):** Distribution and analytics
  - How to schedule posts in Publer/Buffer
  - How to read analytics (watch time, CTR, shares)
  - How to iterate (double down on winners, kill losers)

### Deliverables Checklist

- [ ] 3 hired clippers (names, contact info, rates)
- [ ] Clipper SOP (Google Doc or Notion)
- [ ] Training video for clippers (Loom, 10-15 min)
- [ ] Example clips (3 good, 3 bad)
- [ ] 3 distribution accounts created (YouTube, TikTok, Instagram)
- [ ] Posting tool configured (Publer, Buffer, or Later)
- [ ] 30-day content calendar (30-50 clips mapped)
- [ ] QC checklist (Google Sheet or Notion)
- [ ] 2 management training calls (recorded)

### Quality Control Checkpoints

- [ ] All 3 clippers delivered test clips on time
- [ ] Test clips meet quality standards (captions, pacing, hook)
- [ ] Distribution accounts are live and branded
- [ ] Content calendar has 30+ clips scheduled
- [ ] Client can assign work to clippers independently
- [ ] Client can QC and request revisions independently

### Client Communication Templates

**Kickoff Email:**
```
subject: clipping operation setup starts

hi [name],

starting your clipping operation setup.

i need:
1. access to your youtube/podcast (link or login)
2. brand assets (logo, colors, fonts)
3. any existing clip examples you like

timeline:
- week 1: hire 3 clippers, create training docs, set up distribution
- week 2: build content calendar, QC framework, management training

first clips should be ready by end of week 2.

- printmaxx
```

**Mid-Project Update (Week 1):**
```
subject: clipping setup - 3 clippers hired

hi [name],

week 1 progress:

✅ 3 clippers hired:
- [name 1]: $5/clip, 10 clips/week, portfolio: [link]
- [name 2]: $6/clip, 15 clips/week, portfolio: [link]
- [name 3]: $4/clip, 8 clips/week, portfolio: [link]

✅ clipper sop written: [doc link]
✅ training video recorded: [loom link]
✅ distribution accounts created (youtube shorts, tiktok, instagram)

next:
- content calendar (30 clips mapped)
- QC framework
- management training calls

- printmaxx
```

**Completion Email:**
```
subject: clipping operation ready to launch

hi [name],

setup complete. here's everything:

1. 3 clippers hired: [doc with contact info]
2. clipper sop: [link]
3. training video: [loom link]
4. distribution accounts: [youtube, tiktok, instagram links]
5. 30-day content calendar: [link]
6. qc checklist: [link]
7. management training recordings: [call 1 link] [call 2 link]

next steps:
1. assign first batch of clips to clippers (use sop)
2. review clips using qc checklist
3. schedule approved clips in publer/buffer
4. monitor analytics weekly

target: 30 clips/month (10 per platform).

- printmaxx
```

### Tools Needed

- Fiverr, Upwork, or OnlineJobs.ph (clipper hiring)
- Loom (training videos)
- Google Drive or Dropbox (clip delivery)
- Publer, Buffer, or Later (scheduling)
- Premiere Pro or CapCut (if creating example clips)
- Notion or Google Docs (SOPs and QC checklists)

### Common Issues & Solutions

**Issue:** Clippers ghost after hiring
- **Solution:** Hire 5 instead of 3, expect 40% attrition, replace immediately

**Issue:** Clip quality is inconsistent
- **Solution:** Create more detailed style guide with frame-by-frame examples, or fire and replace

**Issue:** Client doesn't have enough source content (only 1-2 videos/month)
- **Solution:** Recommend increasing content output first, or clip competitor content (fair use commentary)

**Issue:** Clips get low views (algorithm not picking up)
- **Solution:** A/B test hooks, titles, thumbnails. Focus on first 3 seconds. Increase posting frequency.

**Issue:** Client can't keep up with QC (30 clips/month is too much)
- **Solution:** Reduce volume to 15 clips/month, or offer managed service (+$500/mo for full management)

**Issue:** Distribution accounts get banned (TikTok/Instagram flagging)
- **Solution:** Appeal immediately, avoid copyrighted music, ensure captions don't violate TOS, diversify accounts (create backups)

---

## Service 7: Content Farm Setup ($800)

### Pre-Engagement Checklist

**Before starting:**
- [ ] Agree on 3 niches (from: faith, fitness, tech, finance, memes, women's lifestyle)
- [ ] Agree on 3 platforms per niche (X/Twitter, Instagram, TikTok recommended)
- [ ] Confirm content style (educational, memes, motivational, news aggregation)
- [ ] Get client's monetization preference (affiliate links, products, creator programs)
- [ ] Set up tracking sheet for analytics

### Fulfillment Process (12-15 hours over 1 week)

**Phase 1: Niche Research and Validation (2-3 hours)**
- [ ] 60 min: Research each niche:
  - Find 10 high-performing accounts per niche
  - Analyze top posts (what formats, hooks, topics get engagement)
  - Check monetization methods (what are competitors selling)
- [ ] 30 min: Validate engagement potential:
  - Use Social Blade or similar to check growth rates
  - Confirm audience size is large enough (>100K posts with niche hashtag)
- [ ] 30 min: Document findings (top accounts, content patterns, monetization paths)

**Phase 2: Account Setup (3 platforms × 3 niches = 9 accounts, 3 hours)**
- [ ] 90 min: Create 9 accounts:
  - Choose handles (brandable, easy to remember)
  - Set profile pics (AI-generated or Canva templates)
  - Write bios (clear value prop, CTA, link)
- [ ] 60 min: Optimize for monetization:
  - Add affiliate links or product links to bio
  - Enable creator programs (X Premium, Instagram creator, TikTok creator fund)
  - Set up Linktree or Beacons.ai for multi-link bio
- [ ] 30 min: Brand consistency check (colors, tone, imagery align per niche)

**Phase 3: Content Creation (50 posts × 3 niches = 150 posts, 5-6 hours)**
- [ ] 180 min: Write 50 posts per niche (AI-assisted, then humanized):
  - 20 educational posts (how-tos, tips, frameworks)
  - 15 engagement posts (questions, polls, hot takes)
  - 10 inspirational posts (quotes, stories, motivation)
  - 5 promotional posts (affiliate products, own products)
- [ ] 120 min: Humanize all posts:
  - Remove AI vocabulary (leverage, delve, comprehensive)
  - Add specific numbers and examples
  - Ensure no em dashes
  - Follow copy style rules (`.claude/rules/copy-style.md`)
- [ ] 60 min: Format for each platform:
  - X/Twitter: thread format, hashtags, character limits
  - Instagram: captions, hashtags (5-10), carousel ideas
  - TikTok: video script format (if applicable)

**Phase 4: Content Calendar (3 accounts × 30 days = 90 days mapped, 2 hours)**
- [ ] 90 min: Create 30-day calendar per account:
  - Map which posts go out when
  - Balance educational, engagement, inspirational, promotional
  - Optimal posting times per platform (morning, lunch, evening)
- [ ] 30 min: Load into scheduling tool (Buffer, Publer, Later)

**Phase 5: Monetization Setup (2 hours)**
- [ ] 60 min: Set up monetization funnels:
  - Gumroad products (templates, guides, mini-courses)
  - Affiliate links (Amazon, ClickBank, niche-specific)
  - Creator programs (apply for X Premium revenue share, etc.)
- [ ] 30 min: Create lead magnets (free download in exchange for email)
- [ ] 30 min: Link everything in bio (Linktree/Beacons)

### Deliverables Checklist

- [ ] 3 niches validated (competitor analysis, engagement data)
- [ ] 9 accounts created (3 platforms × 3 niches)
- [ ] 150 posts written (50 per niche, humanized)
- [ ] 3 content calendars (30 days per niche)
- [ ] Monetization setup (affiliate links, Gumroad, creator programs)
- [ ] Bio links configured (Linktree or Beacons)
- [ ] Posting scheduled in Buffer/Publer (first 30 days ready to go)

### Quality Control Checkpoints

- [ ] All posts pass copy style check (no AI tells)
- [ ] Accounts are branded consistently per niche
- [ ] Monetization links work and track correctly
- [ ] Content calendar has no gaps (posts every day for 30 days)
- [ ] Posts are varied (not all the same format)
- [ ] Hashtags are relevant and not banned/spammy

### Client Communication Templates

**Kickoff Email:**
```
subject: content farm setup - which 3 niches?

hi [name],

starting your content farm setup.

pick 3 niches from:
- faith (prayer, bible study, christian living)
- fitness (workouts, nutrition, motivation)
- tech (ai tools, productivity, solopreneurship)
- finance (budgeting, investing, side hustles)
- memes (engagement farming, viral content)
- women's lifestyle (beauty, wellness, relationships)

for each niche, confirm:
- 3 platforms (twitter, instagram, tiktok recommended)
- monetization goal (affiliates, products, creator revenue)

timeline: 1 week to deliver 9 accounts + 150 posts + 30-day calendar.

- printmaxx
```

**Mid-Project Update:**
```
subject: content farm - 9 accounts created

hi [name],

progress:

✅ 3 niches researched and validated
✅ 9 accounts created:
  - [niche 1]: @handle1 (twitter), @handle2 (instagram), @handle3 (tiktok)
  - [niche 2]: @handle4, @handle5, @handle6
  - [niche 3]: @handle7, @handle8, @handle9

✅ 150 posts written (50 per niche)

next:
- content calendars (30 days per niche)
- monetization setup (affiliate links, gumroad)

- printmaxx
```

**Completion Email:**
```
subject: content farm ready - 9 accounts, 150 posts, 30 days scheduled

hi [name],

content farm complete:

1. 9 accounts: [list with links]
2. 150 posts (50 per niche): [google doc link]
3. 30-day content calendars: [link]
4. monetization setup: [linktree links]
5. posting scheduled: first 30 days loaded in buffer

next steps:
1. review posts and approve (or request changes)
2. hit "publish" in buffer to activate schedule
3. monitor analytics weekly (i included tracking sheet: [link])

recommended: engage with comments daily for algorithm boost.

- printmaxx
```

### Tools Needed

- Social Blade or Similar (account research)
- Canva or AI image generator (profile pics)
- Claude or GPT (content generation)
- Buffer, Publer, or Later (scheduling)
- Linktree or Beacons (bio links)
- Gumroad (digital products)
- Google Sheets (content calendar + analytics tracking)

### Common Issues & Solutions

**Issue:** Client doesn't know which niches to pick
- **Solution:** Recommend based on their existing skills/audience, or default to tech + finance + memes (broad appeal)

**Issue:** Posts are too AI-sounding even after humanization pass
- **Solution:** Run through copy style checklist again, add more specific examples, read out loud to test

**Issue:** Accounts get shadowbanned immediately after creation
- **Solution:** Warm up accounts (post manually for 3-5 days before automating), avoid spammy hashtags, engage with others before posting

**Issue:** Client wants video content but this is text-only
- **Solution:** Upsell video content farm (+$500 for 30 short-form videos), or pivot to caption-only for now

**Issue:** Monetization links don't convert (no clicks)
- **Solution:** A/B test CTA in bio, ensure link is above the fold, add "link in bio" to posts

**Issue:** Client can't manage 9 accounts (too overwhelming)
- **Solution:** Start with 3 accounts (1 per niche), scale to 9 after proving concept

---

## Service 8: Method Stack Consultation ($300, 60 min)

### Pre-Engagement Checklist

**Before scheduling call:**
- [ ] Send pre-call skills questionnaire (Google Form or Typeform):
  - What skills do you have? (coding, design, writing, video, marketing)
  - What assets do you have? (audience, email list, website, products)
  - How much time/week can you dedicate? (5, 10, 20, 40 hours)
  - What's your revenue goal? ($1K, $5K, $10K, $50K/mo)
  - What have you tried before? (what worked, what didn't)
- [ ] Review client's online presence:
  - Check Twitter, LinkedIn, personal site
  - Look for existing audience or content
- [ ] Pull relevant LEDGER data:
  - `CROSS_POLLINATION_MATRIX.csv` (synergy scores)
  - `APP_FACTORY_METHODS.csv`, `CONTENT_FARM` files, etc.
  - `GTM_OPTIMIZATION_PRIORITIES.csv`

**24 hours before call:**
- [ ] Draft initial recommendations (top 3 methods based on questionnaire)
- [ ] Pull revenue projections for each method
- [ ] Create 90-day timeline mockup
- [ ] Prepare tool stack with costs

### Fulfillment Process (3 hours total)

**Phase 1: Pre-Call Assessment (60 min)**
- [ ] 20 min: Review questionnaire responses
- [ ] 20 min: Research client's existing assets/audience
- [ ] 20 min: Cross-reference LEDGER files:
  - Which methods match their skills?
  - Which methods have highest ROI for their level?
  - Which methods stack well together?

**Phase 2: During Call (60 min)**
- [ ] 0-5 min: Intro, confirm their situation hasn't changed since questionnaire
- [ ] 5-25 min: Present top 3 method recommendations:
  - **Method 1:** [name], why it fits, revenue potential, time investment
  - **Method 2:** [name], why it fits, synergy with Method 1
  - **Method 3:** [name], backup/diversification option
- [ ] 25-40 min: Revenue projections and timelines:
  - 30-day goal: $X (low-hanging fruit)
  - 90-day goal: $Y (consistent revenue)
  - 12-month goal: $Z (scaled operation)
- [ ] 40-55 min: Tool stack walkthrough:
  - What tools they need (costs, free alternatives)
  - Infrastructure setup (domains, emails, accounts)
  - Automation opportunities (ralph loops, scheduling)
- [ ] 55-60 min: Q&A and next steps

**Phase 3: Post-Call Delivery (60 min)**
- [ ] 30 min: Write consultation summary doc:
  - Top 3 method recommendations
  - Why each fits their situation
  - Revenue projections (30/90/365 days)
  - 90-day action plan (week-by-week)
  - Tool stack with costs
  - Synergy opportunities (how methods stack)
- [ ] 20 min: Add tactical action items:
  - Week 1 tasks (setup, research)
  - Week 2-4 tasks (first revenue)
  - Month 2-3 tasks (scale, optimize)
- [ ] 10 min: Send follow-up email with doc and offer for implementation services

### Deliverables Checklist

- [ ] 60-min consultation call (recorded)
- [ ] Top 3 method recommendations (with rationale)
- [ ] Revenue projections (30/90/365 days)
- [ ] 90-day action plan (week-by-week)
- [ ] Tool stack with costs (itemized)
- [ ] Synergy score analysis (which methods stack best)
- [ ] Written summary doc (Google Doc or Notion)
- [ ] Optional: upsell to implementation services

### Quality Control Checkpoints

- [ ] Recommendations match client's actual skills (not aspirational)
- [ ] Revenue projections are realistic (not inflated guru promises)
- [ ] Tool costs fit their budget
- [ ] 90-day plan is specific (not vague "create content")
- [ ] Client understands next steps clearly
- [ ] Doc is delivered within 24 hours of call

### Client Communication Templates

**Pre-Call Questionnaire Email:**
```
subject: method stack consultation - prep needed

hi [name],

consultation scheduled for [date/time].

before the call, fill out this 2-min questionnaire: [link]

questions:
- your skills (coding, design, writing, video, marketing)
- your assets (audience, email list, website, products)
- time available per week
- revenue goal
- what you've tried before

i'll use this to prepare personalized recommendations.

zoom link: [link]

- printmaxx
```

**24-Hour Reminder:**
```
subject: tomorrow's call - initial thoughts

hi [name],

call tomorrow at [time].

based on your questionnaire, i'm thinking:
- [method 1]: matches your [skill], potential $[X]/mo in 90 days
- [method 2]: stacks well with method 1, synergy score [Y]
- [method 3]: backup option if methods 1-2 don't fit

we'll finalize on the call and build your 90-day plan.

zoom link: [link]

- printmaxx
```

**Completion Email (within 24 hours):**
```
subject: method stack consultation summary

hi [name],

here's your personalized plan: [doc link]

top 3 methods:
1. [method 1] - $[X]/mo potential in 90 days
2. [method 2] - stacks with #1, synergy score [Y]
3. [method 3] - diversification option

90-day timeline:
- week 1: [setup tasks]
- week 2-4: [first revenue tasks]
- month 2-3: [scale tasks]

tool stack: $[total]/mo
- [tool 1]: $[X]/mo
- [tool 2]: $[Y]/mo
- [tool 3]: free

call recording: [loom link]

next steps:
1. review the doc
2. pick 1 method to start (recommend [method 1])
3. execute week 1 tasks

if you want help implementing, i offer:
- [service 1]: $[price]
- [service 2]: $[price]

let me know if you have questions.

- printmaxx
```

### Tools Needed

- Zoom or Google Meet (call)
- Loom (recording)
- Google Docs or Notion (deliverables)
- Google Forms or Typeform (questionnaire)
- LEDGER files (cross-reference methods, synergy scores)
- Calculator or spreadsheet (revenue projections)

### Common Issues & Solutions

**Issue:** Client has no clear skills ("I'm a beginner at everything")
- **Solution:** Recommend skill-stacking approach: start with content (build writing), then add low-code apps, then automation

**Issue:** Client's revenue goal is unrealistic ($100K/mo in 90 days with 5 hours/week)
- **Solution:** Reset expectations, show realistic numbers, offer path from $1K → $10K → $50K over 12-24 months

**Issue:** Client wants to do everything (all 10 methods at once)
- **Solution:** Force prioritization, explain opportunity cost, recommend 1-2 methods max to start

**Issue:** Client already tried a method and failed
- **Solution:** Dig into why it failed (execution, timing, fit), recommend different approach or different method entirely

**Issue:** Client has analysis paralysis (wants more research before deciding)
- **Solution:** Recommend paper trading (test method with $0-100 for 2 weeks), then decide based on data

**Issue:** Client can't afford recommended tool stack
- **Solution:** Provide free alternatives, or recommend bootstrapping with manual work first (automate later)

---

## General Fulfillment Best Practices

### Communication Cadence

**For all services:**
- Kickoff email within 2 hours of booking
- Mid-project update at 50% completion
- Completion email with all deliverables
- Follow-up 2 weeks later (check-in, upsell)

### Quality Over Speed

- Never rush to hit timeline if quality suffers
- If behind schedule, communicate proactively
- Offer to extend timeline or add bonus deliverable

### Scope Creep Management

- Define deliverables clearly upfront
- If client requests extra work, offer as upsell
- Use "included" vs "additional" language in contracts

### Upsell Opportunities

After delivering each service, offer:
- **Service 1 (Paywall Call)** → Upsell to Service 2 (Full Build)
- **Service 2 (Full Build)** → Upsell to Service 3 (Monthly Optimization)
- **Service 4 (Infrastructure)** → Upsell to Service 5 (Managed Outreach)
- **Service 6 (Clipping Setup)** → Upsell to managed clipping ($500/mo)
- **Service 7 (Content Farm)** → Upsell to managed posting ($300/mo)
- **Service 8 (Consultation)** → Upsell to any implementation service

### VA Training

For services that can be delegated:
- Service 4 (Infrastructure Setup) - technical VA
- Service 5 (Managed Outreach) - outreach VA
- Service 6 (Clipping Operation) - clippers are the VA
- Service 7 (Content Farm) - content writer VA

Train VAs using these SOPs. Record yourself doing the service once, then hand off.

### Refund Policy

**Full refund if:**
- Deliverables not completed within 2x stated timeline
- Quality doesn't meet stated standards
- Client cancels before work starts

**No refund if:**
- Client doesn't provide required access/info
- Client requests scope change mid-project
- Work is complete but client "doesn't like it" (subjective)

**Partial refund:**
- If only some deliverables completed, refund proportionally

---

## Post-Delivery Checklist (All Services)

- [ ] All deliverables sent to client
- [ ] Client confirms receipt
- [ ] Request testimonial (if satisfied)
- [ ] Add to portfolio (with permission)
- [ ] Update FINANCIALS/REVENUE_TRACKER.csv
- [ ] Schedule 2-week check-in
- [ ] Offer upsell or related service
- [ ] Archive project files for future reference

---

**Version:** 1.0
**Last Updated:** 2026-02-06
**Owner:** PRINTMAXX Operations
