# ACCOUNT CREATION -- SIT DOWN AND DO THIS RIGHT NOW

**Total time: ~2.5 hours**
**Revenue unlocked: $50K+ of pre-built assets finally go live**
**Date: 2026-02-12**
**Status: THE definitive account creation checklist. Supersedes all prior versions.**

0 out of 49 accounts are ACTIVE. This is the single biggest blocker to revenue. 10 Gumroad products, 7 PWA apps, 5 Fiverr gigs, 20 Etsy listings, 50 POD designs, 1,278 social posts, 3 newsletter sequences -- all built, all waiting on YOU to create accounts.

Sit down. Set a timer. Go top to bottom. Check each box. No skipping. No "I'll do it later."

---

## BEFORE YOU START (5 min)

- [ ] Open your password manager (1Password, Bitwarden, whatever)
- [ ] Have your phone ready for SMS verification
- [ ] Have a credit/debit card ready (only Stripe + Apple Dev need payment)
- [ ] Have a government-issued ID ready (Fanvue may need it)
- [ ] Open this file on a second screen or print it

---

## PHASE 1: MONEY PLUMBING (30 min -- unlocks EVERYTHING)

These 3 accounts are the foundation. Everything else connects to them.

---

### 1. Stripe -- 10 min

**URL:** https://dashboard.stripe.com/register
**Why first:** Every revenue platform pays through Stripe. This is the plumbing for all money.
**Email to use:** Your primary personal email (NOT protonmail -- this is your real business account)
**Payment needed:** NO (free, they take ~2.9% + $0.30 per transaction)

**Steps:**
1. Go to https://dashboard.stripe.com/register
2. Enter your email, full name, create password
3. Verify email (check inbox, click link)
4. Click "Activate your account" in dashboard
5. Fill in business details:
   - Business type: Individual / Sole proprietor
   - Legal name: your real name
   - Business name: PRINTMAXX (or leave blank)
   - Industry: Software / Digital products
6. Add your bank account for payouts (routing + account number)
7. Add your SSN (required for 1099-K tax reporting)
8. Submit verification (usually instant, sometimes 24hr)
9. Save your account ID (starts with `acct_`) and API keys to password manager

**After creation:**
```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/account_tracker.py add --platform Stripe --username printmaxxer --email YOUR_EMAIL --status CREATED
```
**Do NOT close this tab. You connect Gumroad and Medium to Stripe next.**

---

### 2. Gumroad -- 5 min

**URL:** https://gumroad.com/signup
**Why:** 10 digital products are READY to copy-paste. Revenue potential: $500-10K/mo.
**Email to use:** Your primary personal email (same as Stripe)
**Username:** printmaxxer
**Payment needed:** NO (free, Gumroad takes 10% per sale)

**Steps:**
1. Go to https://gumroad.com/signup
2. Enter email, create password
3. Verify email
4. Set display name: PRINTMAXXER
5. Set username: printmaxxer (becomes gumroad.com/printmaxxer)
6. Go to Settings > Payments
7. Click "Connect with Stripe" and authorize
8. Go to Settings > Profile
   - Bio: "digital products for solopreneurs. cold email systems, app building guides, local biz playbooks. real tactics, no fluff."
   - Profile photo: use PRINTMAXXER brand image

**After creation:**
```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/account_tracker.py add --platform Gumroad --username printmaxxer --email YOUR_EMAIL --status CREATED
```
**Next step:** After finishing ALL account creation, come back and list products. 10 listings ready to copy-paste from `PRODUCTS/GUMROAD_READY_LISTINGS.md`. ~5 min per product = 50 min total. This can generate first dollar TODAY.

---

### 3. Vercel -- 10 min

**URL:** https://vercel.com/signup
**Why:** 7 PWA apps built and ready to deploy. Ramadan tracker is URGENT (Ramadan starts Feb 28 = 16 days). Plus 600 programmatic SEO pages.
**Email to use:** Your primary email or GitHub account
**Payment needed:** NO (free hobby tier)

**Steps:**
1. Go to https://vercel.com/signup
2. Sign up with GitHub (recommended) or email
3. If GitHub: authorize Vercel to access repos
4. Complete onboarding (skip team, use "Hobby" plan)
5. Open terminal and run:
   ```bash
   npm i -g vercel && vercel login
   ```
6. Follow the auth prompt (opens browser, click authorize)
7. Verify it works:
   ```bash
   vercel whoami
   ```

**After creation:**
```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/account_tracker.py add --platform Vercel --username printmaxxer --email YOUR_EMAIL --status CREATED
```
**Deploy Ramadan tracker immediately:**
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/app_factory/output/ramadan-tracker && vercel --prod
```
**Deploy programmatic SEO (600 pages):**
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/builds/programmatic_seo && vercel --prod
```

---

## PHASE 2: FREELANCE REVENUE (30 min -- instant income channels)

Ready-made gig listings waiting to be copy-pasted.

---

### 4. Fiverr -- 10 min

**URL:** https://www.fiverr.com/join
**Why:** 5 complete gig listings ready at `OPS/FIVERR_LAUNCH_PACKAGE.md`. Revenue: $500-2K/mo within 60 days.
**Email to use:** Your primary personal email
**Username:** printmaxxer (or closest available)
**Payment needed:** NO (free, Fiverr takes 20%)

**Steps:**
1. Go to https://www.fiverr.com/join
2. Sign up with Google or email
3. Click "Become a Seller"
4. Complete seller profile:
   - Languages: English (Fluent)
   - Skills: Video Editing, Web Design, Python, Cold Email, AI Automation
   - Bio: "I build automations, websites, and content systems for solopreneurs and local businesses. AI-powered workflows. Cold email pipelines. Video clipping. Website redesigns. Real results, fast delivery."
5. Add profile photo (professional headshot or PRINTMAXXER brand image)
6. Create your first gig listing -- copy Gig 1 (Video Clipping) from `OPS/FIVERR_LAUNCH_PACKAGE.md`
7. Free tier: 7 active gigs allowed

**After creation:**
```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/account_tracker.py add --platform Fiverr --username printmaxxer --email YOUR_EMAIL --status CREATED
```
**Follow-up:** List remaining 4 gigs from `OPS/FIVERR_LAUNCH_PACKAGE.md` after all accounts done.

---

### 5. Upwork -- 10 min

**URL:** https://www.upwork.com/nx/signup/?dest=home
**Why:** Higher-ticket work ($50-200/hr). 5 specialized profiles ready at `OPS/UPWORK_LAUNCH_CHECKLIST.md`.
**Email to use:** Your primary personal email
**Payment needed:** NO (free, Upwork takes 10-20%)

**Steps:**
1. Go to URL above
2. Sign up as Freelancer
3. Enter name, email, create password, verify email
4. Complete profile:
   - Title: "AI Automation & Web Development | Cold Email Systems | Local Business Websites"
   - Hourly rate: $75/hr (adjustable per proposal)
   - Skills: Python, Web Development, Automation, AI/ML, Cold Email, Data Scraping
   - Overview: Copy the 500-word overview from `OPS/UPWORK_LAUNCH_CHECKLIST.md` (Profile 1)
   - Portfolio: Add screenshots of built apps/sites
5. Submit profile for review (takes 24-48 hrs)

**After creation:**
```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/account_tracker.py add --platform Upwork --username printmaxxer --email YOUR_EMAIL --status CREATED
```
**Note:** Upwork manually reviews new profiles. Apply to 3 jobs immediately after approval.

---

### 6. Etsy Seller -- 5 min

**URL:** https://www.etsy.com/sell
**Why:** 20 listings ready at `PRODUCTS/ETSY_LISTINGS_20.md` (digital downloads, templates, planners).
**Email to use:** Your primary personal email
**Payment needed:** YES ($0.20 per listing fee)

**Steps:**
1. Go to https://www.etsy.com/sell
2. Click "Get started"
3. Sign in or create Etsy account
4. Shop preferences: English, US, USD
5. Shop name: PrintmaxxDigital (or PrintmaxxShop)
6. Set up billing (credit card for $0.20/listing fee)
7. Set up payment method for receiving money (bank account)
8. List first product from `PRODUCTS/ETSY_LISTINGS_20.md`

**After creation:**
```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/account_tracker.py add --platform Etsy --username PrintmaxxDigital --email YOUR_EMAIL --status CREATED
```

---

### 7. Redbubble -- 5 min

**URL:** https://www.redbubble.com/signup
**Why:** 50+ POD designs ready at `PRODUCTS/POD_DESIGNS_50.md`. Passive income, zero inventory.
**Email to use:** Your primary personal email
**Username:** printmaxxer
**Payment needed:** NO (free, you earn markup on sales)

**Steps:**
1. Go to https://www.redbubble.com/signup
2. Enter username: printmaxxer
3. Enter email, create password, verify email
4. Go to Account > Artist Tools
5. Start uploading designs from `PRODUCTS/POD_DESIGNS_50.md`
6. For each: title, tags, description, select which products to enable

**After creation:**
```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/account_tracker.py add --platform Redbubble --username printmaxxer --email YOUR_EMAIL --status CREATED
```

---

## PHASE 3: TWITTER/X ACCOUNTS (30 min -- content distribution)

1,278 posts are ready to schedule. These accounts distribute them.

**SAFETY NOTE:** Creating 5 X accounts. X allows up to 10 per person. To avoid linking/flagging:
- Use different ProtonMail emails (listed below for each)
- Space them out: create 2-3, take a 30 min break, create the rest
- Use incognito/private window for each (or GoLogin if you have it)
- Do NOT have accounts interact with each other (no cross-liking)

---

### 8. X/Twitter -- @PRINTMAXXER (main hub) -- 8 min

**URL:** https://twitter.com/i/flow/signup
**Email:** printmaxxer@protonmail.com
**Handle:** @PRINTMAXXER

**Steps:**
1. **Create ProtonMail first** (if not done): go to https://account.proton.me/signup, create printmaxxer@protonmail.com, save password
2. Go to https://twitter.com/i/flow/signup
3. Sign up with printmaxxer@protonmail.com
4. Enter date of birth (required)
5. Verify email (check ProtonMail inbox)
6. Claim handle: @PRINTMAXXER
7. Display name: PRINTMAXXER
8. Skip all "follow people" suggestions
9. Set bio:
   ```
   building 11 revenue streams in public. $0 to $50K/mo arc. shipping apps, content, cold outbound, AI tools. everything documented. follow the build log.
   ```
10. Settings > Display > Dark mode ON
11. Settings > Notifications > Filters > turn off likes/retweets notifications

**After creation:** Follow 5 accounts: @levelsio @tdinh_me @dannypostmaa @marc_lou @paborMaker. Like 3 recent posts. DO NOT post yet -- let account age 24 hrs.

---

### 9. X/Twitter -- @SleepMaxx -- 5 min

**URL:** https://twitter.com/i/flow/signup (open in incognito)
**Email:** sleepmaxx@protonmail.com
**Handle:** @SleepMaxx

**Steps:**
1. Create sleepmaxx@protonmail.com at https://account.proton.me/signup
2. Open incognito window
3. Go to https://twitter.com/i/flow/signup
4. Sign up with sleepmaxx@protonmail.com
5. Handle: @SleepMaxx, Display: SleepMaxx
6. Bio:
   ```
   8pm screen cutoff. 65F room. 10pm lights out. went from 5.5 hrs of broken sleep to 7.5 hrs of deep sleep in 3 weeks. posting the protocol.
   ```
7. Dark mode ON

**Content ready at:** `ralph/loops/social_setup/output/T3_sleep_tweets_50.md`

---

### 10. X/Twitter -- @daily_anchor_faith -- 5 min

**URL:** https://twitter.com/i/flow/signup (incognito)
**Email:** daily.anchor.faith@protonmail.com
**Handle:** @daily_anchor_faith

**Steps:**
1. Create daily.anchor.faith@protonmail.com at ProtonMail
2. Incognito window
3. https://twitter.com/i/flow/signup
4. Sign up, claim handle: @daily_anchor_faith, Display: DailyAnchor
5. Bio:
   ```
   you miss prayer 4 days per week. i built an app that makes it impossible to skip. 127-day streak and counting. faith meets discipline meets tech.
   ```
6. Dark mode ON

**Content ready at:** `CONTENT/social/faith/`

---

### 11. X/Twitter -- @three_hour_physique -- 5 min

**URL:** https://twitter.com/i/flow/signup (incognito)
**Email:** three.hour.physique@protonmail.com
**Handle:** @three_hour_physique

**Steps:**
1. Create three.hour.physique@protonmail.com at ProtonMail
2. Incognito window
3. https://twitter.com/i/flow/signup
4. Sign up, claim handle: @three_hour_physique, Display: 3-Hour Physique
5. Bio:
   ```
   you spend 8 hrs/week in the gym. i get better results in 3. minimal effective dose training. real progress pics. no supplements to sell you.
   ```
6. Dark mode ON

---

### 12. X/Twitter -- @ai_workflows_daily -- 5 min

**URL:** https://twitter.com/i/flow/signup (incognito)
**Email:** ai.workflows.tips@protonmail.com
**Handle:** @ai_workflows_daily

**Steps:**
1. Create ai.workflows.tips@protonmail.com at ProtonMail
2. Incognito window
3. https://twitter.com/i/flow/signup
4. Sign up, claim handle: @ai_workflows_daily, Display: StackFlow
5. Bio:
   ```
   your AI tools don't talk to each other. i connect them. 12 tools in 4 minutes. daily workflows that save 5-10 hours/week. no code needed.
   ```
6. Dark mode ON

---

## PHASE 4: CONTENT PLATFORMS (20 min -- newsletter + blog revenue)

---

### 13. Beehiiv -- 5 min

**URL:** https://www.beehiiv.com/create
**Why:** 3 newsletter welcome sequences ready. Beehiiv's recommendation network = free subscribers.
**Email to use:** printmaxxer@protonmail.com (or primary)
**Payment needed:** NO (free Launch plan, up to 2,500 subs)

**Steps:**
1. Go to https://www.beehiiv.com/create
2. Sign up with email
3. Publication name: PRINTMAXXER
4. Handle: printmaxxer
5. Description: "building 11 revenue streams from $0. weekly updates with real numbers."
6. Complete onboarding wizard
7. Settings > Website > Enable web archive
8. Automations > Set up welcome email (use `ralph/loops/social_setup/output/T6_newsletter_tech.md`)

**After creation:** Create 2 more publications later (DailyAnchor, StackFlow) under separate emails.

---

### 14. Substack -- 5 min

**URL:** https://substack.com/sign-in
**Why:** 10 articles drafted. Substack Notes = built-in Twitter-like distribution. Discovery network = free subs.
**Email to use:** printmaxxer@protonmail.com
**Payment needed:** NO (free, 10% of paid subs)

**Steps:**
1. Go to https://substack.com/sign-in
2. Click "Create your Substack"
3. Enter email, verify
4. Publication name: PRINTMAXXER
5. Handle: printmaxxer
6. Description: "building 11 revenue streams from $0. documenting everything. real numbers, real failures."
7. Enable Notes (Substack social feature)
8. Free tier only for now

**Content ready at:** `CONTENT/substack_posts/`

---

### 15. Medium Partner Program -- 5 min

**URL:** https://medium.com
**Why:** 5 articles ready. Partner Program pays per read. Connect Stripe for payouts.
**Email to use:** printmaxxer@protonmail.com
**Username:** @printmaxxer
**Payment needed:** NO (free to write)

**Steps:**
1. Go to https://medium.com, click "Get started"
2. Sign up with Google or email
3. Username: @printmaxxer, Display: PRINTMAXXER
4. Bio: "building 11 revenue streams from $0 in public. real numbers, real failures."
5. Settings > Partner Program > Get started
6. Connect Stripe (from Step 1) for payouts

**Articles ready at:** `CONTENT/medium_articles/MEDIUM_BATCH_NEW_5.md`

---

### 16. Buffer -- 5 min

**URL:** https://buffer.com/signup
**Why:** 1,278 posts ready to schedule. 12 Buffer-ready CSVs. Upload = firehose ON.
**Email to use:** Your primary personal email
**Payment needed:** NO (free = 3 channels. $6/mo = unlimited)

**Steps:**
1. Go to https://buffer.com/signup
2. Sign up with email
3. Complete onboarding
4. Connect channels: @PRINTMAXXER Twitter first, add others as created
5. Go to Publishing > Upload CSV
6. Upload CSVs from `AUTOMATIONS/content_posting/`

**Posting guide:** `OPS/CONTENT_POSTING_GUIDE.md`

---

## PHASE 5: NSFW REVENUE (15 min -- high ceiling)

---

### 17. Fanvue -- 10 min

**URL:** https://www.fanvue.com/creator/signup
**Why:** AI NSFW is explicitly allowed on Fanvue. Platform doing $100M ARR. 10-persona portfolio planned. Revenue: $500-30K/mo.
**Email to use:** Create a NEW ProtonMail (separate from all other accounts, not linked to PRINTMAXXER brand)
**Payment needed:** NO (free, they take 15%)

**Steps:**
1. Create new ProtonMail for NSFW ops (something discreet)
2. Go to https://www.fanvue.com/creator/signup
3. Sign up as Creator with new email
4. Complete onboarding
5. ID verification may be required (real identity, kept private from subscribers)
6. IMPORTANT: Disclose AI-generated content per Fanvue policy and legal requirements
7. Set subscription price: $9.99/mo to start
8. Connect payout method (bank or Stripe)
9. Set up first persona profile (see execution plan below)

**Execution plan:** `MONEY_METHODS/AI_INFLUENCER/AI_NSFW_FINDOM_EXECUTION_PLAN.md`
**Personas:** `PRODUCTS/branding/FINDOM_PERSONAS.md`
**Content ready:** `AUTOMATIONS/content_posting/findom_tweets_50.csv`

---

### 18. Patreon -- 5 min

**URL:** https://www.patreon.com/create
**Why:** Tiered content. Backup/complement to Fanvue. Also works for non-NSFW community content.
**Email to use:** Same NSFW email or primary (depends on use case)
**Payment needed:** NO (free, they take 5-12%)

**Steps:**
1. Go to https://www.patreon.com/create
2. Sign up with email
3. Choose: Content Creator
4. Set up 3 tiers: Free / $5/mo / $25/mo
5. Add profile photo, description
6. Connect Stripe for payouts

---

## PHASE 6: DEVELOPER ACCOUNT (10 min)

---

### 19. Apple Developer -- 10 min

**URL:** https://developer.apple.com/programs/enroll/
**Why:** 7 apps built and ready. Can't submit to App Store without this. Deploy as PWAs on Vercel while waiting for approval.
**Email to use:** Your Apple ID email
**Payment needed:** YES ($99/year)

**Steps:**
1. Go to https://developer.apple.com/programs/enroll/
2. Sign in with Apple ID (or create one)
3. Agree to Developer Agreement
4. Choose Individual enrollment
5. Enter personal info (legal name, address, phone)
6. Pay $99/year
7. Wait for approval (usually instant to 48 hours)

**After approval:** See `06_OPERATIONS/setup/HUMAN_INFRA_CHECKLIST.md` TIER 4 for per-app App Store setup.
**Meanwhile:** All 7 apps work as PWAs on Vercel. Deploy them NOW, submit to App Store when approved.

---

## PHASE 7: BONUS -- HIGH IMPACT, FAST (15 min, optional but recommended)

---

### 20. Amazon Associates -- 3 min
**URL:** https://affiliate-program.amazon.com
**Why:** Affiliate links in apps, newsletters, content. Universal product catalog. Free.
1. Sign in with Amazon account
2. Enter website/app URLs (use Vercel URLs)
3. Preferred store ID: printmaxxer-20
4. Complete tax info

---

### 21. Bland AI -- 3 min
**URL:** https://www.bland.ai
**Why:** 100 FREE outbound calls/day. Pair with local biz pipeline for lead gen. Zero cost.
1. Sign up with email
2. Get API key
3. Call scripts: `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md`
4. Pipeline: `python3 AUTOMATIONS/local_biz_pipeline.py`

---

### 22. Instantly.ai -- 3 min
**URL:** https://instantly.ai
**Why:** Cold email at scale. Sequences ready. $30-37/mo after trial.
1. Sign up with email
2. Start free trial
3. Connect cold email domains (need domains purchased first)
4. Enable auto-warmup (takes 14-21 days -- start NOW)
5. Templates: `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md`

---

## POST-CREATION MASTER CHECKLIST

Run through this after finishing all accounts:

**Security:**
- [ ] All passwords saved in password manager
- [ ] 2FA enabled on: Stripe, Gumroad, all Twitter accounts, Etsy, Fiverr, Upwork
- [ ] NSFW email completely separate from business emails

**Connections:**
- [ ] Stripe connected to: Gumroad, Medium, Patreon
- [ ] Vercel CLI authenticated (`vercel whoami` returns your username)
- [ ] Buffer connected to at least @PRINTMAXXER Twitter

**Verification:**
- [ ] At least 1 Gumroad product listed (test the checkout flow)
- [ ] At least 1 Fiverr gig published (test the listing flow)
- [ ] Vercel deployed at least Ramadan tracker

**Tracking:**
```bash
python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/scripts/account_tracker.py status
```

---

## IMMEDIATE NEXT ACTIONS (after all accounts exist)

In priority order:

| Priority | Action | Time | Guide |
|----------|--------|------|-------|
| 1 | Deploy Ramadan Tracker to Vercel | 5 min | `vercel --prod` in ramadan-tracker dir |
| 2 | List 10 Gumroad products (copy-paste) | 50 min | `PRODUCTS/GUMROAD_READY_LISTINGS.md` |
| 3 | List 5 Fiverr gigs (copy-paste) | 30 min | `OPS/FIVERR_LAUNCH_PACKAGE.md` |
| 4 | Upload Buffer CSVs (schedule 1,278 posts) | 15 min | `AUTOMATIONS/content_posting/` |
| 5 | Deploy 600 SEO pages to Vercel | 5 min | `vercel --prod` in programmatic_seo dir |
| 6 | List 5 Etsy products | 25 min | `PRODUCTS/ETSY_LISTINGS_20.md` |
| 7 | Upload 10 Redbubble designs | 20 min | `PRODUCTS/POD_DESIGNS_50.md` |
| 8 | Publish first Medium article | 10 min | `CONTENT/medium_articles/MEDIUM_BATCH_NEW_5.md` |
| 9 | Send first Beehiiv welcome email | 10 min | `ralph/loops/social_setup/output/T6_newsletter_tech.md` |
| 10 | Post first tweet from @PRINTMAXXER | 5 min | After 24hr warmup period |

---

## REVENUE SUMMARY: WHAT EACH ACCOUNT UNLOCKS

| # | Account | Assets Waiting | Revenue Potential |
|---|---------|---------------|-------------------|
| 1 | Stripe | Payment plumbing for everything | Required for all $ |
| 2 | Gumroad | 10 digital products ready to list | $500-10K/mo |
| 3 | Vercel | 7 PWA apps + 600 SEO pages | App + SEO revenue |
| 4 | Fiverr | 5 complete gig listings | $500-2K/mo |
| 5 | Upwork | 5 specialized profiles | $2-10K/mo |
| 6 | Etsy | 20 product listings | $200-2K/mo |
| 7 | Redbubble | 50+ POD designs | $100-500/mo passive |
| 8-12 | 5 X/Twitter accounts | 1,278 posts queued | Audience + traffic |
| 13 | Beehiiv | 3 newsletter sequences | Subscriber revenue |
| 14 | Substack | 10 articles + Notes | Paid subs + discovery |
| 15 | Medium | 5 articles | Partner Program $ |
| 16 | Buffer | 1,278 posts to auto-schedule | Distribution engine |
| 17 | Fanvue | AI persona portfolio | $500-30K/mo |
| 18 | Patreon | Tiered community | $200-5K/mo |
| 19 | Apple Dev | 7 built apps for App Store | $1-10K/mo |
| 20 | Amazon Assoc | Affiliate links everywhere | $100-2K/mo |
| 21 | Bland AI | 100 free calls/day | Local biz leads |
| 22 | Instantly | Cold email sequences | $1-5K/mo services |

**Startup cost: ~$130** (Apple Dev $99 + Etsy listings ~$4 + Instantly $37/mo trial)
**Revenue ceiling with all channels active: $50-100K+/mo**

---

## ACCOUNTS TO CREATE LATER (not today)

These need the X/Twitter accounts warmed up first (2-4 weeks):
- TikTok (5 accounts) -- needs phone + mobile proxy per account
- Instagram (5 accounts) -- needs mobile proxy (SOAX)
- YouTube (5 channels) -- lower urgency, create when ready for video
- Facebook Pages (5) -- lowest priority
- LinkedIn (3 profiles) -- create when cold outbound is running
- Pinterest (3 business accounts) -- create when content pipeline is flowing

**Full 43-account setup guide:** `ralph/loops/social_setup/output/T7_HUMAN_ACCOUNT_CREATION_MASTER.md`

---

## ProtonMail QUICK REFERENCE

You need these 5 ProtonMail accounts. Create them at https://account.proton.me/signup

| Email | Used For |
|-------|----------|
| printmaxxer@protonmail.com | @PRINTMAXXER (main hub) + Gumroad + Beehiiv + Substack + Medium |
| sleepmaxx@protonmail.com | @SleepMaxx (sleep niche) |
| daily.anchor.faith@protonmail.com | @daily_anchor_faith (faith niche) |
| three.hour.physique@protonmail.com | @three_hour_physique (fitness niche) |
| ai.workflows.tips@protonmail.com | @ai_workflows_daily (AI niche) |
| [new discreet email] | Fanvue NSFW (separate from everything) |

---

*Every day these accounts don't exist = money left on the table. 2.5 hours now unlocks months of pre-built work. Go.*
