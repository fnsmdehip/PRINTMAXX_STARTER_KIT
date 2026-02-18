# HUMAN EXECUTION DASHBOARD

Single-page view of every action that requires a human. Ordered by dependency chain and revenue impact.
Updated: 2026-02-12

**Current state:** $0 revenue. 80+ scripts built. 7 PWA apps ready. 1,661 leads collected. 1,278 posts drafted. 10 Gumroad products written. 49 accounts tracked (0 fully active). Everything is built but nothing is deployed because account creation hasn't happened.

**Time to complete all TIER 0-1:** ~2 hours
**Time to complete all TIER 0-3:** ~4-5 hours
**Estimated revenue unlocked:** $2K-$10K/mo within 60 days of completing TIER 0-2

---

## STATUS SUMMARY

| Tier | Actions | Est. Time | Revenue Unlocked | Status |
|------|---------|-----------|-----------------|--------|
| TIER 0 | 3 actions | 15 min | Unblocks everything | NOT STARTED |
| TIER 1 | 5 actions | 30 min | Apps + digital products + freelance | NOT STARTED |
| TIER 2 | 8 actions | 45 min | Social content + newsletters | NOT STARTED |
| TIER 3 | 6 actions | 30 min | Cold outbound + paid services | NOT STARTED |
| TIER 4 | 4 actions | 20 min | Native apps on App Store | NOT STARTED |
| TIER 5 | 5 actions | 30 min | Affiliate + NSFW | NOT STARTED |

---

## TIER 0: AUTHENTICATION (15 min) -- BLOCKS LITERALLY EVERYTHING

These 3 actions unblock 90% of all other work. Do them first.

### 0.1 Vercel Login
- [ ] Run in terminal: `vercel login`
- [ ] Browser opens, click authorize
- [ ] Then run: `bash AUTOMATIONS/deploy_all_apps.sh`
- **Unblocks:** 7 PWA app deployments (ramadan-tracker, sleepmaxx, focuslock, habitforge, mealmaxx, walktounlock, prayerlock)
- **Time:** 2 min
- **URGENT:** Ramadan starts Feb 28 (16 days). Ramadan tracker must be live.

### 0.2 Stripe Account
- [ ] Go to https://stripe.com
- [ ] Sign up with email + bank account + SSN
- [ ] Complete identity verification
- **Unblocks:** Gumroad payouts, RevenueCat payments, all payment processing
- **Time:** 10 min
- **Dependency:** Required before Gumroad (0.3)

### 0.3 Gumroad Account
- [ ] Go to https://gumroad.com
- [ ] Sign up with email
- [ ] Connect Stripe (from 0.2)
- [ ] List 10 products from `PRODUCTS/GUMROAD_READY_LISTINGS.md` (copy-paste ready)
- **Unblocks:** $500-$10K/mo digital product revenue
- **Time:** 3 min signup + 20 min listing products
- **Dependency:** Requires Stripe (0.2)

---

## TIER 1: REVENUE PLATFORMS (30 min) -- DIRECT MONEY

Each of these directly enables a revenue stream.

### 1.1 Fiverr Account
- [ ] Go to https://fiverr.com
- [ ] Create seller account
- [ ] List top 5 services from `PRINTMAXX_FREELANCE_ARB.xlsx`
- [ ] Checklist: `OPS/FIVERR_LAUNCH_CHECKLIST.md`
- **Unblocks:** Freelance arbitrage ($500-$3K/mo)
- **Time:** 10 min
- **Ready assets:** `OPS/FIVERR_LAUNCH_PACKAGE.md` has gig descriptions, pricing, FAQs

### 1.2 Upwork Account
- [ ] Go to https://upwork.com
- [ ] Create freelancer profile
- [ ] Set up 5 specialized profiles per `OPS/UPWORK_LAUNCH_CHECKLIST.md`
- **Unblocks:** Freelance arbitrage + B2B services ($1K-$5K/mo)
- **Time:** 10 min

### 1.3 Beehiiv Account
- [ ] Go to https://beehiiv.com
- [ ] Sign up (free plan, 2,500 subs)
- [ ] Create 3 newsletters: Morning Grace (faith), 5AM Gains (fitness), The Stack (AI/tech)
- [ ] Import welcome sequences from `ralph/loops/social_setup/output/T6_newsletter_*.md`
- **Unblocks:** Newsletter revenue ($500-$68K/mo at scale), email list building
- **Time:** 10 min

### 1.4 Buffer or Typefully Account
- [ ] Go to https://buffer.com (free: 3 channels, 10 posts each)
- [ ] Or https://typefully.com (free: basic scheduling)
- [ ] Upload CSV content from `AUTOMATIONS/content_posting/` (12 CSVs, 1,278+ posts)
- **Unblocks:** Automated posting across all niches
- **Time:** 5 min signup + 15 min uploading CSVs

### 1.5 Medium Account
- [ ] Go to https://medium.com
- [ ] Sign up, join Partner Program
- [ ] Publish 5 articles from `CONTENT/medium_articles/`
- [ ] Cross-post guide: `OPS/CONTENT_SYNDICATION_LAUNCH.md`
- **Unblocks:** Medium Partner Program revenue + SEO backlinks
- **Time:** 5 min

---

## TIER 2: SOCIAL ACCOUNTS (45 min) -- CONTENT DISTRIBUTION

40+ accounts need creation. Prioritized by revenue impact. Use GoLogin + separate proxies per profile group.

**Pre-setup (do once):**
- [ ] Create email: sleepmaxx@protonmail.com (the only email not yet created)
- [ ] Set up GoLogin profiles with Decodo proxies (5 profiles for 5 niches)
- [ ] Have phone ready for SMS verification
- **Full guide:** `ralph/loops/social_setup/output/T7_HUMAN_ACCOUNT_CREATION_MASTER.md`

### 2.1 PRINTMAXXER accounts (Profile-Meta, Decodo-1)
- [ ] X/Twitter: @PRINTMAXXER (printmaxxer@protonmail.com)
- [ ] TikTok: @printmaxxer
- [ ] Instagram: @printmaxxer
- [ ] YouTube: PRINTMAXXER
- [ ] LinkedIn: PRINTMAXXER
- [ ] Facebook Page: PRINTMAXXER
- [ ] Substack: printmaxxer
- **Bios ready:** `ralph/loops/social_setup/output/T1_all_bios.md` (copy-paste)
- **Image prompts:** `ralph/loops/social_setup/output/T2_image_prompts.md`

### 2.2 AI niche accounts (Profile-AI, Decodo-2)
- [ ] X/Twitter: @ai_workflows_daily
- [ ] TikTok: @aiworkflowsdaily
- [ ] Instagram: @aiworkflowsdaily
- [ ] YouTube: AI Workflows Daily
- [ ] LinkedIn: StackFlow
- [ ] Beehiiv: stackflow

### 2.3 Faith niche accounts (Profile-Faith, Decodo-3)
- [ ] X/Twitter: @daily_anchor_faith
- [ ] TikTok: @dailyanchorfaith
- [ ] Instagram: @dailyanchorfaith
- [ ] YouTube: Daily Anchor Faith
- [ ] Beehiiv: dailyanchor
- [ ] Pinterest: DailyAnchor

### 2.4 Fitness niche accounts (Profile-Fitness, Decodo-4)
- [ ] X/Twitter: @three_hour_physique
- [ ] TikTok: @threehourphysique
- [ ] Instagram: @threehourphysique
- [ ] YouTube: 3-Hour Physique
- [ ] Beehiiv: threehourphysique
- [ ] Pinterest: 3-Hour Physique

### 2.5 Sleep niche accounts (Profile-Sleep, Decodo-5)
- [ ] X/Twitter: @SleepMaxx
- [ ] TikTok: @sleepmaxx
- [ ] Instagram: @sleepmaxx
- [ ] YouTube: Sleep Maxx
- [ ] Pinterest: SleepMaxx

### Post-Creation Warmup (Days 1-7, ongoing)
- [ ] Days 1-3: Like, follow, comment only (NO posting) on all accounts
- [ ] Days 4-7: Post 1x/day per account
- [ ] Day 8+: Ramp to 3x/day
- [ ] Track warmup: `python3 scripts/account_tracker.py warmup`
- **Warmup schedules:** `ralph/loops/social_setup/output/T5_warmup_schedule.md`

---

## TIER 3: OUTBOUND INFRASTRUCTURE (30 min) -- B2B REVENUE

### 3.1 Cold Email Domains (3 domains)
- [ ] Buy 3 domains on https://porkbun.com (~$10/yr each)
- [ ] Add to Cloudflare for DNS management
- [ ] Set SPF, DKIM, DMARC records per domain
- **Full guide:** `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md`
- **Unblocks:** Cold outbound to 1,661 collected leads
- **Time:** 15 min

### 3.2 Google Workspace
- [ ] Go to https://workspace.google.com
- [ ] Create 2-3 inboxes per cold email domain
- [ ] Set up forwarding and signatures
- **Time:** 10 min
- **Dependency:** Requires domains (3.1)

### 3.3 Cold Email Tool
- [ ] Pick one: Instantly.ai ($37/mo) OR Smartlead ($39/mo) OR DeliverOn ($49/mo, pre-warmed)
- [ ] Sign up, connect cold email domains
- [ ] Enable auto-warmup (14-21 days before sending)
- [ ] Import leads from `AUTOMATIONS/leads/` (1,661 leads across 26 files)
- **Templates ready:** `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md` has 4 sequences
- **Time:** 5 min

### 3.4 Bland AI (Free)
- [ ] Go to https://bland.ai
- [ ] Sign up (100 free calls/day)
- [ ] Configure with scripts from `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md`
- **Unblocks:** AI-powered cold calling to local biz leads
- **Time:** 5 min

### 3.5 Apollo.io (Optional, $79/mo)
- [ ] Go to https://apollo.io
- [ ] Sign up for lead data
- [ ] Only when cold email is generating ROI
- **Time:** 5 min

### 3.6 LinkedIn Sales Navigator (Optional, $80/mo)
- [ ] Only when B2B pipeline justifies the cost
- [ ] For targeted outreach to decision-makers

---

## TIER 4: APP STORE ACCOUNTS (20 min) -- NATIVE APP REVENUE

### 4.1 Apple Developer Account ($99/yr)
- [ ] Go to https://developer.apple.com/programs/enroll/
- [ ] Need: Apple ID + credit card + government ID
- [ ] Takes 24-48 hours to approve
- **Unblocks:** iOS app submissions (PrayerLock, WalkToUnlock, etc.)

### 4.2 Google Play Developer ($25 one-time)
- [ ] Go to https://play.google.com/console/signup
- [ ] Need: Google account + credit card
- [ ] Usually approved same day
- **Unblocks:** Android app submissions

### 4.3 RevenueCat (Free)
- [ ] Go to https://revenuecat.com
- [ ] Sign up, connect Stripe
- [ ] Free up to $2,500/mo revenue
- **Unblocks:** In-app subscription management
- **Dependency:** Requires Stripe (0.2) + Apple (4.1) + Google (4.2)

### 4.4 App Store Listings (per app)
- [ ] Create app entries in App Store Connect
- [ ] Set up subscription groups and products
- [ ] Privacy policy + Support URLs needed (deploy a simple page)
- **Guide:** `06_OPERATIONS/setup/HUMAN_INFRA_CHECKLIST.md` TIER 4 section

---

## TIER 5: EXPANSION PLATFORMS (30 min) -- ADDITIONAL REVENUE STREAMS

### 5.1 Fanvue Account (AI Findom)
- [ ] Go to https://fanvue.com (allows AI-generated content)
- [ ] Need: Government ID for age verification + bank account
- [ ] Set up 3 subscription tiers ($10-$15, $25-$35, $50-$100)
- [ ] Add AI disclosure to profile
- **Execution plan:** `MONEY_METHODS/AI_INFLUENCER/AI_NSFW_FINDOM_EXECUTION_PLAN.md`
- **Revenue potential:** $500-$30K/mo
- **Time:** 15 min

### 5.2 Fansly Account (Backup)
- [ ] Go to https://fansly.com
- [ ] Backup platform for AI findom content
- **Time:** 5 min

### 5.3 Affiliate Programs (apply to all)
- [ ] Amazon Associates: https://affiliate-program.amazon.com
- [ ] Athletic Greens: https://athleticgreens.com/pages/affiliate
- [ ] Impact.com: https://impact.com
- [ ] PartnerStack: https://partnerstack.com
- [ ] Full list of 42 programs: `OPS/AFFILIATE_LAUNCH_CHECKLIST.md`
- **Time:** 10 min (batch apply)

### 5.4 AI Tools (content creation)
- [ ] Leonardo.ai ($12/mo): https://leonardo.ai -- AI visuals
- [ ] ElevenLabs ($5-$22/mo): https://elevenlabs.io -- Voice cloning
- [ ] D-ID ($5.90/mo): https://d-id.com -- Talking avatars
- **Total:** $23-$40/mo
- **Time:** 10 min

### 5.5 Etsy + Redbubble (POD)
- [ ] Etsy seller account: https://etsy.com/sell
- [ ] Redbubble account: https://redbubble.com
- [ ] Listings ready: `PRODUCTS/ETSY_LISTINGS_20.md` (20 listings), `PRODUCTS/REDBUBBLE_LISTINGS.md`
- **Time:** 10 min

---

## DEPENDENCY CHAIN (What Blocks What)

```
Stripe (0.2)
  |
  +-- Gumroad (0.3) --> 10 digital products live
  +-- RevenueCat (4.3) --> In-app purchases
  +-- Fanvue payout (5.1)

Vercel Login (0.1)
  |
  +-- 7 PWA apps deployed --> Ramadan tracker LIVE

Cold Email Domains (3.1)
  |
  +-- Google Workspace (3.2)
       |
       +-- Cold Email Tool (3.3) --> Outreach to 1,661 leads

Social Accounts (2.1-2.5)
  |
  +-- 7-day warmup period
       |
       +-- Buffer CSV uploads (1.4) --> 1,278 posts scheduled
       +-- Newsletter signups linked in bios

Apple Developer (4.1) + Google Play (4.2)
  |
  +-- RevenueCat (4.3)
       |
       +-- Native app submissions with subscriptions
```

---

## REVENUE PROJECTION BY COMPLETION TIER

| After Completing | Monthly Revenue (30-day) | Monthly Revenue (90-day) |
|-----------------|------------------------|------------------------|
| TIER 0 only | $0-$100 (Gumroad sales) | $200-$500 |
| TIER 0 + 1 | $100-$500 (+ freelance + newsletter) | $500-$2,000 |
| TIER 0-2 | $200-$1,000 (+ social + content) | $1,000-$5,000 |
| TIER 0-3 | $500-$2,000 (+ cold outbound) | $2,000-$10,000 |
| TIER 0-4 | $1,000-$5,000 (+ app subscriptions) | $5,000-$25,000 |
| TIER 0-5 | $2,000-$10,000 (+ findom + affiliates) | $10,000-$50,000 |

---

## QUICK REFERENCE: Post-Account Commands

After creating accounts, run these to update tracking:

```bash
# After each account creation
python3 scripts/account_tracker.py add --platform <name> --username <user> --email <email> --status CREATED

# After Vercel login
bash AUTOMATIONS/deploy_all_apps.sh

# After Gumroad signup - products are copy-paste from:
cat PRODUCTS/GUMROAD_READY_LISTINGS.md

# After Buffer signup - upload these CSVs:
ls AUTOMATIONS/content_posting/*.csv

# After cold email domains - run warmup check:
python3 scripts/account_tracker.py warmup

# After all social accounts - start warmup tracking:
python3 scripts/account_tracker.py status

# Check overall system health:
python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary
```

---

## THE MATH: WHY THIS MATTERS

- 80+ Python scripts built and idle
- 7 PWA apps sitting in folders
- 1,661 leads collected with no outreach
- 1,278 social posts drafted with nowhere to post
- 10 Gumroad products written with no store
- 4 newsletter sequences with no Beehiiv
- 30 freelance service listings with no Fiverr/Upwork
- 600 programmatic SEO pages with no domain

**Every day without account creation = $0 revenue from $50K+ worth of built assets.**

The bottleneck is not building. The bottleneck is 2 hours of account signups.
