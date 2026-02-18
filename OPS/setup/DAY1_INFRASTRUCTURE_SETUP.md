# Day 1 Infrastructure Setup - Complete Guide

**Time Required:** 4-6 hours (one session)
**Total Cost:** $230-400 first month + $124 one-time
**Goal:** Get all accounts, tools, and infrastructure ready for revenue operations

---

## Cost Breakdown

### One-Time Costs ($124)

| Item | Cost | Required For |
|------|------|--------------|
| Apple Developer Account | $99 | App Store submissions (biomaxx, PrayerLock) |
| Google Play Developer | $25 | Android apps (future) |
| **Total One-Time** | **$124** | |

### Monthly Recurring ($230-400)

| Tier | Cost | What You Get |
|------|------|--------------|
| **TIER 0 (Bootstrap)** | $230-260/mo | Minimum viable stack (3 accounts, basic tools) |
| **TIER 1 (Growth)** | $400-450/mo | Full 12-account operation + better tools |

**Start with TIER 0. Upgrade to TIER 1 when revenue hits $500+/mo.**

---

## Hourly Breakdown

### Hour 1: Critical Accounts (Free)

**These are FREE but REQUIRED for revenue:**

#### 1. Gumroad + Stripe (15 min)

**Gumroad:**
1. Go to gumroad.com
2. Sign up with email (or Google)
3. Skip onboarding wizard for now
4. Go to Settings → Payments
5. Click "Connect Stripe"

**Stripe:**
1. Create Stripe account (free)
2. Connect bank account:
   - Routing number
   - Account number
   - Verify micro-deposits (2-3 days)
3. Set payout schedule: Weekly (fastest)

**Why:** You need this before you can receive your first payment from Gumroad.

#### 2. Social Media Accounts (45 min)

**Create 3 Twitter accounts:**

**@daily_anchor_faith (Faith niche)**
1. twitter.com → Sign up
2. Use email: dailyanchorfaith@gmail.com (create new Gmail if needed)
3. Username: @daily_anchor_faith
4. Bio:
   ```
   5-minute morning prayer changed my life. tracking 147/180 days consistent.
   building PrayerLock to help others do the same.
   ```
5. Profile image: Generate with Gemini AI
   - Prompt: "minimalist praying hands icon, purple gradient, peaceful, modern"
   - Download and upload
6. Pin first post (copy from CONTENT_CALENDAR_30DAY.csv Day 1)

**@three_hour_physique (Fitness niche)**
1. twitter.com → Sign up (different email)
2. Use email: threehourphysique@gmail.com
3. Username: @three_hour_physique
4. Bio:
   ```
   3 hours per week in the gym. gained 12lbs of muscle in 8 months.
   monday wednesday friday. compound lifts only.
   ```
5. Profile image: Gemini AI - "minimalist dumbbell icon, red gradient, strong"
6. Pin first post

**@ai_workflows_daily (Tech/AI niche)**
1. twitter.com → Sign up (different email)
2. Use email: aiworkflowsdaily@gmail.com
3. Username: @ai_workflows_daily
4. Bio:
   ```
   automating everything. n8n + claude + python.
   shipped 4 playbooks on gumroad. building apps with AI.
   ```
5. Profile image: Gemini AI - "minimalist circuit board icon, blue gradient, tech"
6. Pin first post

**Note:** Use different devices or browsers for each account to avoid Twitter shadow bans. Or use anti-detect browser (see TIER 1).

---

### Hour 2: Developer Accounts (One-Time Payment)

#### 1. Apple Developer Account ($99, 30 min)

**Required to submit biomaxx and PrayerLock to App Store.**

1. Go to developer.apple.com
2. Sign in with Apple ID (or create one)
3. Enroll as Individual
4. Fill out profile:
   - Legal name (your real name)
   - Address
   - Phone number
5. Pay $99 (credit card)
6. Wait for approval:
   - Usually instant
   - Can take up to 24 hours
   - Check email for confirmation

**Once approved:**
1. Go to appstoreconnect.apple.com
2. Familiarize with dashboard
3. Don't create apps yet (wait until ready to submit)

#### 2. Google Play Developer ($25, 15 min)

**Required for Android apps (future).**

1. Go to play.google.com/console
2. Sign in with Google account
3. Pay $25 one-time fee
4. Fill out developer profile:
   - Name
   - Address
   - Email
5. Verification (can take 2-3 days)

**Can skip for now** if you're iOS-only to start. Come back when you want to launch Android.

#### 3. Revenue Cat (15 min, FREE)

**Subscription management for apps.**

1. Go to revenuecat.com
2. Sign up with email
3. Create new project: "Lock Apps Portfolio"
4. Get API keys:
   - iOS key
   - Android key (future)
5. Don't configure products yet (do this when submitting apps)

**Why:** Handles iOS/Android subscriptions, server-side receipt validation, analytics.

---

### Hour 3: AI Tools (Monthly Recurring)

**TIER 0 Stack ($23/mo):**

#### 1. Leonardo.ai ($12/mo, 10 min)

**For app icons, marketing images, social graphics.**

1. Go to leonardo.ai
2. Sign up with Google
3. Start with free tier (150 credits/day)
4. Upgrade to Apprentice ($12/mo) when needed (unlimited generations)

**Test generation:**
- Generate an app icon for PrayerLock
- Prompt: "3D app icon, Christian prayer theme, praying hands, purple to gold gradient, 1024x1024, iOS style"

#### 2. ElevenLabs ($5/mo, 10 min)

**For AI voice (if doing video content).**

1. Go to elevenlabs.io
2. Sign up with email
3. Free tier: 10K characters/month
4. Upgrade to Starter ($5/mo) when needed: 30K characters/month

**Skip for now** if not doing video content. Add later when scaling.

#### 3. D-ID ($6/mo, 10 min)

**For AI talking head videos (UGC content).**

1. Go to d-id.com
2. Sign up with email
3. Free tier: 20 credits (5 videos)
4. Upgrade to Lite ($6/mo) when needed: 1 video/day

**Skip for now** if not doing video. Add when starting TikTok/Reels.

**TIER 0 Total: $0-23/mo** (depending on what you activate)

---

### Hour 4: Content Scheduling (Free or $12/mo)

#### Option A: Buffer (FREE for 3 accounts)

1. Go to buffer.com
2. Sign up with Google
3. Connect 3 Twitter accounts:
   - @daily_anchor_faith
   - @three_hour_physique
   - @ai_workflows_daily
4. Free plan:
   - 3 social accounts
   - 10 posts per queue
5. Upload CSV files (see `OPS/BUFFER_CSV_UPLOAD_INSTRUCTIONS.md`)

**Limitation:** Free tier only allows 3 accounts. Upgrade to Essentials ($6/account/mo) for more.

#### Option B: Publer ($12/mo, RECOMMENDED)

1. Go to publer.io
2. Sign up with email
3. Start 14-day free trial (no credit card)
4. Connect all accounts:
   - 3 Twitter accounts
   - 3 Instagram accounts (when created)
   - 3 TikTok accounts (when created)
   - 3 LinkedIn profiles (when created)
5. Upload master CSV: `LEDGER/CONTENT_CALENDAR_30DAY.csv`
6. Schedule all 1,008 posts at once

**Why Publer over Buffer:**
- Unlimited accounts on Pro plan ($12/mo)
- Better TikTok support
- Bulk CSV upload easier
- First month free (trial)

---

### Hour 5: Email Setup (FREE for now)

#### Gmail Setup for Cold Email (FREE)

**For initial cold outbound (before scaling):**

1. Create 3 Gmail accounts:
   - faith.outreach@gmail.com
   - fitness.outreach@gmail.com
   - tech.outreach@gmail.com
2. Enable 2FA on each
3. Warm up manually:
   - Send 5 emails/day to friends
   - Reply to emails
   - Do this for 14 days before cold outreach
   - Gradually increase to 20-30/day

**Limitation:** Manual warmup takes 2 weeks. For faster: Use DeliverOn/EmailBison (TIER 1).

#### Email Sequences Ready to Send

**Location:** `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES.md`

**7 verticals ready:**
- Healthcare/dental
- Legal services
- Real estate
- Home services
- B2B SaaS
- Local businesses
- Tech/startups

**Don't send yet.** Warm up accounts first (or upgrade to pre-warmed inboxes in TIER 1).

---

### Hour 6: Optional Tools (Add When Scaling)

#### Notion (FREE)

**For organizing everything:**
1. Go to notion.so
2. Sign up with Google
3. Create workspaces:
   - Content calendar
   - Product roadmap
   - Revenue tracker
4. Can also use for building Notion templates to sell

#### Canva (FREE)

**For graphics:**
1. Go to canva.com
2. Sign up with Google
3. Use free templates:
   - eBook covers (for Gumroad PDFs)
   - Social media posts
   - App screenshots
4. Pro plan ($13/mo) adds brand kit, more templates

#### Google Sheets (FREE)

**For tracking:**
1. Import LEDGER CSVs to Google Sheets
2. Share with collaborators (if any)
3. Create dashboard
4. Link to Gumroad via Zapier (future)

---

## TIER 1 Upgrade (When Revenue Hits $500+/mo)

**Added Monthly Costs: +$170-190/mo**

### Warmed Email Inboxes ($50-100/mo)

**Why:** Skip the 2-week manual warmup. Start sending immediately.

**Option A: DeliverOn ($50/mo)**
1. Go to deliveron.com
2. Buy 3 warmed inboxes
3. Each inbox comes with:
   - Pre-warmed (30 days of activity)
   - High deliverability
   - Can send 50-100/day immediately

**Option B: EmailBison ($75/mo)**
1. Go to emailbison.com
2. Similar to DeliverOn
3. Slightly better deliverability
4. 3 inboxes for $75/mo

### Anti-Detect Browser ($49-99/mo)

**Why:** Manage multiple social accounts safely. Prevents shadow bans.

**GoLogin ($49/mo)**
1. Go to gologin.com
2. Download app
3. Create 10 browser profiles (one per social account)
4. Each profile has unique:
   - Fingerprint
   - IP address (needs proxies)
   - Cookies/cache

**Multilogin ($99/mo)**
1. Go to multilogin.com
2. Better fingerprinting
3. More professional

**Combine with SOAX mobile proxies (see below).**

### Mobile Proxies ($50/mo)

**Why:** Instagram and TikTok detect datacenter IPs. Mobile IPs are safer.

**SOAX ($50/mo)**
1. Go to soax.com
2. Buy mobile proxy plan
3. Configure in GoLogin/Multilogin
4. Rotate IPs for each account

**Critical for:** Instagram automation, TikTok posting, multiple accounts.

### Paid Tool Upgrades ($20-40/mo)

**When scaling:**

**Leonardo.ai Premium ($30/mo)**
- Unlimited image generations
- Better quality

**ElevenLabs Scale ($22/mo)**
- More voice minutes
- Better voice cloning

**HeyGen ($24/mo)**
- Better AI UGC videos
- API access

---

## Account Security Best Practices

### Use Password Manager

**1Password or Bitwarden (FREE)**
1. Install extension
2. Generate unique passwords for every account
3. Enable 2FA everywhere possible
4. Never reuse passwords

### 2FA Setup

**Enable on:**
- [ ] Gumroad
- [ ] Stripe
- [ ] Apple Developer
- [ ] Google Play
- [ ] Twitter accounts (all 3)
- [ ] Email accounts (all 3)
- [ ] RevenueCat

**Use authenticator app, not SMS:**
- Google Authenticator
- Authy
- 1Password (has built-in 2FA)

### Email Organization

**Create email structure:**
```
Primary: your@gmail.com (personal, payments)
Faith: dailyanchorfaith@gmail.com (social + outreach)
Fitness: threehourphysique@gmail.com (social + outreach)
Tech: aiworkflowsdaily@gmail.com (social + outreach)
Support: support@printmaxx.com (customer support - set up later)
```

---

## Verification Checklist

**By end of Hour 6, you should have:**

### Accounts Created ✓

- [ ] Gumroad + Stripe connected
- [ ] 3 Twitter accounts (@daily_anchor_faith, @three_hour_physique, @ai_workflows_daily)
- [ ] Apple Developer account ($99 paid)
- [ ] RevenueCat account
- [ ] Buffer or Publer account

### Accounts Pending ✓

- [ ] Google Play ($25 paid, verification pending)
- [ ] Email accounts warming (14 days if manual)

### Tools Subscribed ✓

- [ ] Leonardo.ai (free tier or $12/mo)
- [ ] Publer ($12/mo) OR Buffer (free)

### Optional Tools ✓

- [ ] ElevenLabs (if doing video)
- [ ] D-ID (if doing UGC)
- [ ] Notion (free)
- [ ] Canva (free)

---

## What NOT to Buy Yet

**Wait until you have revenue:**

- ❌ Domain names (unless free via Namecheap promo)
- ❌ Paid ads budget (wait until organic proves product-market fit)
- ❌ Premium tool upgrades (start with free tiers)
- ❌ VA/contractor help (do it yourself first)
- ❌ Expensive courses/coaching (you have 88 methods documented)

**Exception:** If something blocks revenue, buy it. Otherwise, wait.

---

## Next Steps After Setup

**Once all accounts are created:**

1. **Execute Week 1 Revenue Plan**
   - See `OPS/WEEK1_REVENUE_EXECUTION.md`
   - Compile first Gumroad product
   - Upload Buffer CSVs
   - Start posting

2. **Submit biomaxx to App Store**
   - See `03_PLAYBOOKS/APP_FACTORY/builds/biomaxx-sdk54/LAUNCH_PLAN.md`
   - 2-4 hours to submit
   - First potential app revenue

3. **Begin content calendar**
   - 1,008 posts scheduled for 30 days
   - Monitor engagement
   - Reply to comments

---

## Troubleshooting Common Issues

### Twitter Suspends Account

**Cause:** Creating multiple accounts from same IP/device

**Fix:**
1. Use different browsers for each account
2. Or use anti-detect browser (GoLogin)
3. Appeal suspension: twitter.com/appeals
4. Usually restored within 24-48 hours

### Stripe Verification Delayed

**Cause:** Bank verification can take 2-3 days

**Fix:**
1. Check for micro-deposits in bank account
2. Enter amounts in Stripe dashboard
3. Can take up to 5 business days
4. Can't receive payouts until verified (but can still sell)

### Apple Developer Approval Delayed

**Cause:** Sometimes manual review required

**Fix:**
1. Check email for requests for more info
2. Usually approved within 24 hours
3. Can take up to 48 hours
4. Contact support if >48 hours

### Buffer CSV Upload Fails

**Cause:** Incorrect date/time format

**Fix:**
1. Ensure dates are YYYY-MM-DD
2. Ensure times are HH:MM (24-hour)
3. Remove any special characters from post text
4. Try uploading smaller batch (100 posts) first

---

## Cost Summary by Tier

### TIER 0: Bootstrap Start ($230-260/mo + $124 one-time)

**One-Time:**
- Apple Developer: $99
- Google Play: $25
- **Total:** $124

**Monthly:**
- Leonardo.ai: $0-12
- Publer: $12
- SOAX proxies: $50 (if using multiple accounts)
- Buffer alternative: $0 (free tier)
- **Total:** $12-74/mo

**When to use:** Starting out, validating products, first $500 in revenue.

### TIER 1: Growth Stack ($400-450/mo)

**Everything in TIER 0 plus:**
- DeliverOn/EmailBison: $50-100
- GoLogin: $49
- SOAX proxies: $50
- Leonardo Premium: $30
- ElevenLabs Scale: $22
- **Total:** $~200/mo added

**When to use:** Revenue at $500+/mo, scaling cold outbound, need multiple warmed accounts.

---

## Timeline

| Hour | Task | Cost | Status |
|------|------|------|--------|
| 1 | Gumroad + Twitter accounts | $0 | Critical |
| 2 | Apple/Google Developer | $124 | Critical for apps |
| 3 | AI tools (Leonardo) | $0-23 | Optional initially |
| 4 | Content scheduler (Publer) | $12 | Critical |
| 5 | Email setup | $0 | Critical |
| 6 | Optional tools | $0 | Nice to have |

**Total Time:** 4-6 hours
**Total Cost:** $136-159 (first month) + $124 one-time

---

**Status:** Complete infrastructure setup guide. Start with TIER 0. Upgrade to TIER 1 at $500+/mo revenue.
