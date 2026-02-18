# Account Creation Master Process

**Created:** 2026-02-12
**Status:** EXECUTE NOW
**Total estimated time:** 3-4 hours (one focused session)
**Purpose:** Create every account needed to start generating revenue. Ordered by dependency chain. Nothing later works without the earlier steps.

**Track progress:** `python3 scripts/account_tracker.py status`
**See blockers:** `python3 scripts/account_tracker.py blockers`

---

## How to use this document

Do the phases in order. Phase 1 blocks everything. Phase 2 needs Phase 1. Phases 3-5 can run in parallel once Phase 2 is done.

Have these ready before you start:
- Business email address (printmaxxer@protonmail.com or similar)
- Government ID (for Stripe, Upwork identity verification)
- SSN or EIN (Stripe payouts)
- Bank account or debit card (Stripe payouts)
- Phone number (SMS verification for social accounts)
- Professional headshot photo (real, not AI-generated for platforms that check)
- Password manager open (you will create 15+ accounts)

---

## PHASE 1: Payment Rails (DO FIRST - blocks everything)

**Time:** 30 minutes active, 24-48 hours verification wait
**Why first:** Every product platform and freelance site needs a connected payment method. Without Stripe, you cannot receive money on Gumroad, Whop, or your own sites. Without PayPal, you cannot receive Fiverr or Upwork payouts.

---

### 1A. Stripe

**URL:** stripe.com
**Signup time:** 15 minutes
**Verification:** 24-48 hours (sometimes instant)
**What it unlocks:** Gumroad payments, Whop payments, Beehiiv paid subscriptions, direct website payments, Substack payouts
**What to have ready:** Legal name, DOB, SSN/EIN, bank account details

**Steps:**
- [ ] Go to stripe.com, click "Start now"
- [ ] Sign up with business email
- [ ] Select "Individual / Sole proprietor" (unless you have an LLC)
- [ ] Enter legal name, date of birth, last 4 SSN
- [ ] Add bank account for payouts (checking account, not savings)
- [ ] Set payout schedule to "daily" (fastest cash flow)
- [ ] Upload government ID if prompted
- [ ] Enable test mode, run a $1 test charge to verify setup works
- [ ] Save API keys in password manager (needed for direct integrations later)

**After verification:**
```bash
python3 scripts/account_tracker.py add --platform Stripe --username primary --email <your-email> --status ACTIVE
```

**If verification takes longer than 48 hours:** Check email for requests for additional documentation. Stripe sometimes wants a utility bill or bank statement for address verification. Upload immediately, don't wait.

---

### 1B. PayPal Business

**URL:** paypal.com/business
**Signup time:** 15 minutes
**Verification:** Usually instant for basic, 3-5 days for full
**What it unlocks:** Fiverr payouts, Upwork payouts, international payments, backup payment method for everything
**What to have ready:** Business email, bank account, phone number

**Steps:**
- [ ] Go to paypal.com/business
- [ ] Click "Sign Up for Free"
- [ ] Select "Individual/Sole Proprietor" business type
- [ ] Enter business email, create password
- [ ] Enter legal name, address, phone number, DOB
- [ ] Link bank account (same account as Stripe is fine)
- [ ] Verify email (check inbox, click link)
- [ ] Verify phone number (SMS code)
- [ ] Optional: Apply for PayPal business debit card (useful for expenses tracking)

**After setup:**
```bash
python3 scripts/account_tracker.py add --platform PayPal --username <email> --email <email> --status ACTIVE
```

**Note:** PayPal has a 21-day hold on new seller accounts for first few transactions. This is normal. Clears after you build transaction history.

---

**PHASE 1 CHECKPOINT:** Wait for Stripe verification before proceeding to Phase 2. While waiting, you can set up social media accounts (Phase 3) since they don't need payment rails.

---

## PHASE 2: Product Platforms

**Time:** 90 minutes total
**Prerequisite:** Stripe account verified (Phase 1A)
**Why second:** These are where revenue happens. 10 Gumroad products are ready to list. Beehiiv newsletters are ready to launch. Whop community is ready to build. Every day these aren't live is money left on the table.

---

### 2A. Gumroad (10 products ready to list)

**URL:** gumroad.com
**Signup time:** 10 minutes for account, 30 minutes to list all 10 products
**What it unlocks:** Digital product sales ($7-$197/product), passive revenue from existing content
**What to have ready:** Stripe account (for payouts), product files and descriptions from `PRODUCTS/GUMROAD_READY_LISTINGS.md`
**Existing assets:** 10 products copy-paste ready at `PRODUCTS/GUMROAD_READY_LISTINGS.md`, cover specs at `PRODUCTS/GUMROAD_COVER_SPECS.md`
**Detailed guide:** `OPS/GUMROAD_LAUNCH_CHECKLIST.md` (731 lines, click-by-click)

**Steps:**
- [ ] Go to gumroad.com, click "Start selling"
- [ ] Sign up with business email
- [ ] Verify email
- [ ] Go to Settings > Profile:
  - [ ] Display name: PRINTMAXX
  - [ ] Bio: "AI-powered playbooks for solopreneurs. specific tactics. real numbers. zero fluff."
  - [ ] Profile URL: gumroad.com/printmaxx
  - [ ] Upload profile pic (logo or clean icon)
- [ ] Go to Settings > Payments:
  - [ ] Connect Stripe account
  - [ ] Verify payout method works
- [ ] List products (follow `OPS/GUMROAD_LAUNCH_CHECKLIST.md` for each):
  - [ ] Product 1: Solopreneur Revenue Tracker ($17)
  - [ ] Product 2: AI Workflow Pack - 47 Prompts ($17)
  - [ ] Product 3: Prayer Journal - Notion ($7)
  - [ ] Product 4: 7-Day Prayer Challenge ($7)
  - [ ] Product 5: Prayer Bundle ($12)
  - [ ] Product 6: Fitness Tracker - Notion ($19)
  - [ ] Product 7: Sleep Optimization System ($14)
  - [ ] Product 8: Cold Email Subject Lines - 73 Templates ($5)
  - [ ] Product 9: Funnel Teardown Pack ($19)
  - [ ] Product 10: Monthly Revenue Blueprint ($29)
- [ ] Set launch discount code: LAUNCH50 (50% off first 48 hours)
- [ ] Publish all products

**After setup:**
```bash
python3 scripts/account_tracker.py add --platform Gumroad --username printmaxx --email <email> --status ACTIVE
python3 scripts/revenue_intake.py log --method MM034 --amount 0 --source Gumroad --note "10 products listed"
```

---

### 2B. Whop (digital products + community)

**URL:** whop.com
**Signup time:** 15 minutes
**What it unlocks:** Community monetization, course hosting, paid Discord alternative, higher-ticket products
**What to have ready:** Stripe account, product descriptions
**Detailed guide:** `OPS/WHOP_LAUNCH_CHECKLIST.md`

**Steps:**
- [ ] Go to whop.com, click "Start selling"
- [ ] Sign up with business email
- [ ] Create your Whop:
  - [ ] Name: PRINTMAXX HQ (or niche-specific name)
  - [ ] Description: 1-2 sentences, what members get
  - [ ] Upload logo/banner
- [ ] Connect Stripe for payouts (Settings > Billing)
- [ ] Create access passes:
  - [ ] Free tier: basic resources, community access
  - [ ] Pro tier ($19/mo): all playbooks, templates, weekly updates
  - [ ] Founding tier ($49/mo): everything + direct access + monthly call
- [ ] Upload first 3-5 digital products (same as Gumroad, different audience)
- [ ] Set up welcome flow for new members
- [ ] Publish and share link

**After setup:**
```bash
python3 scripts/account_tracker.py add --platform Whop --username printmaxx --email <email> --status ACTIVE
```

---

### 2C. Beehiiv (newsletters x4)

**URL:** beehiiv.com
**Signup time:** 20 minutes (account + 4 newsletter setups)
**What it unlocks:** Newsletter revenue (ads, paid subscriptions), email list building, welcome sequence funnels to Gumroad products
**What to have ready:** Newsletter names, welcome sequences from `ralph/loops/social_setup/output/T6_newsletter_*.md`
**Existing assets:** 4 newsletter packages ready with 7-email welcome sequences each

**Steps:**
- [ ] Go to beehiiv.com, click "Start for free"
- [ ] Sign up with business email
- [ ] Create first publication:
  - [ ] Name: "The AI Edge" (tech/productivity)
  - [ ] From name: PRINTMAXX
  - [ ] Subdomain: theaiedge.beehiiv.com
  - [ ] Upload logo
- [ ] Set up welcome email (paste from `ralph/loops/social_setup/output/T6_newsletter_tech.md`)
- [ ] Create 3 more publications:
  - [ ] "Daily Devotion" (faith) - copy from T6_newsletter_faith.md
  - [ ] "The Gains Report" (fitness) - copy from T6_newsletter_fitness.md
  - [ ] "The Sleep Letter" (health/sleep) - copy from T6_newsletter_sleep.md
- [ ] For each publication:
  - [ ] Set up welcome sequence (7 emails, pre-written)
  - [ ] Enable recommendations (cross-recommend your other publications)
  - [ ] Add CTA links to Gumroad products in welcome sequence
  - [ ] Enable Beehiiv Ad Network (passive revenue from day 1)
- [ ] Connect custom domains if available

**After setup:**
```bash
python3 scripts/account_tracker.py add --platform Beehiiv --username printmaxx --email <email> --status ACTIVE
```

---

### 2D. Substack

**URL:** substack.com
**Signup time:** 15 minutes
**What it unlocks:** Long-form content monetization, Substack discovery network, Notes (short-form feed), paid subscriptions
**What to have ready:** Publication name, bio, first article (Article 10 from `CONTENT/substack_posts/SUBSTACK_BATCH_10.md`)
**Existing assets:** 10 articles ready at `CONTENT/substack_posts/SUBSTACK_BATCH_10.md`, launch guide at `CONTENT/substack_posts/SUBSTACK_LAUNCH_GUIDE.md`

**Steps:**
- [ ] Go to substack.com/publish
- [ ] Create publication
  - [ ] Name: "The PRINTMAXX Report" or "Ship Weekly"
  - [ ] Bio: "I build internet businesses from zero and share every number."
  - [ ] Upload profile photo
- [ ] Enable Substack Notes
- [ ] Enable recommendations
- [ ] Set up welcome email (template in `CONTENT/substack_posts/SUBSTACK_LAUNCH_GUIDE.md`)
- [ ] Create sections: Tech & Tools, Health & Data, Building in Public, Faith
- [ ] Publish first article (Article 10: "30 days from $0 to $3,147")
- [ ] Post first Substack Note (teaser for the article)
- [ ] Enable paid tier ($7/mo, $70/year) after week 4

**After setup:**
```bash
python3 scripts/account_tracker.py add --platform Substack --username printmaxx --email <email> --status ACTIVE
```

---

**PHASE 2 CHECKPOINT:** All product platforms live. Products listed. Newsletters configured. Now you can accept money. Phases 3-5 run in parallel from here.

---

## PHASE 3: Social Media Accounts

**Time:** 60-75 minutes total
**Prerequisite:** Phase 2 done (you need product links for bios)
**Why:** Distribution channels. Content is ready (1,278+ posts in `AUTOMATIONS/content_posting/`). Accounts are the bottleneck.

**Reference for all bios and images:** `ralph/loops/social_setup/output/T1_all_bios.md` (80 bios), `ralph/loops/social_setup/output/T2_image_prompts.md` (60 image prompts)
**Warmup guide:** `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md`

---

### 3A. Twitter/X (5 accounts)

**URL:** x.com
**Signup time:** 10 minutes per account (50 min total)
**What it unlocks:** Primary distribution for all niches, building-in-public audience, traffic to products
**What to have ready:** 5 email addresses (one per account), profile photos, bios from `ralph/loops/social_setup/output/T1_all_bios.md`, content from `AUTOMATIONS/content_posting/`

**5 accounts to create:**

| Account | Niche | Email | Bio focus |
|---------|-------|-------|-----------|
| @PRINTMAXXER | Meta/tech/building-in-public | printmaxxer@protonmail.com | "building internet businesses from zero. every number. every mistake." |
| Faith account | Faith/prayer | separate email | PrayerLock app, daily devotion, prayer community |
| Fitness account | Fitness/health | separate email | WalkToUnlock, 3-hour physique, data-driven fitness |
| Sleep account | Sleep/wellness | separate email | SleepMaxx, 365 nights data, Oura ring tips |
| Memes account | Engagement farming | separate email | Meme curation, viral content, niche humor |

**For each account:**
- [ ] Go to x.com, sign up with dedicated email
- [ ] Verify email
- [ ] Set profile photo (512x512px min, see image prompts doc)
- [ ] Set banner (1500x500px)
- [ ] Write bio (max 160 chars, pull from T1_all_bios.md)
- [ ] Add website link (Gumroad, newsletter, or app)
- [ ] Switch to Professional account (free, gives analytics)
- [ ] Write and schedule 5 initial tweets
- [ ] Write 1 thread (5-7 tweets)
- [ ] Follow 50 relevant accounts in niche

**Warmup schedule (days 1-7):**
- Days 1-3: Follow 50 accounts, like/RT 20 tweets, post 2 tweets/day
- Days 4-5: 3-5 tweets/day, reply to 15 accounts with real value
- Days 6-7: 5 tweets, first thread, quote tweet 2-3 posts
- Day 8+: Full posting schedule from `AUTOMATIONS/content_posting/`

**Important:** Use different IPs or a gap of 10+ minutes between account creations. Don't create all 5 from the same IP in 5 minutes. Twitter flags this.

```bash
# After each account:
python3 scripts/account_tracker.py add --platform "Twitter/X" --username @HANDLE --email <email> --status CREATED --niche <niche>
```

---

### 3B. TikTok (3 accounts)

**URL:** tiktok.com
**Signup time:** 5 minutes per account (15 min total)
**What it unlocks:** Short-form video distribution, Creator Fund, TikTok Shop affiliate, younger demographics
**What to have ready:** 3 email addresses, profile photos, video content ideas

**3 accounts to create:**

| Account | Niche | Content type |
|---------|-------|-------------|
| Faith | Prayer/devotion | Short devotionals, prayer reminders, PrayerLock demos |
| Fitness | Workout/health | Exercise form, nutrition tips, WalkToUnlock demos |
| Memes | Engagement farming | Trending memes adapted for niche, reaction content |

**For each account:**
- [ ] Go to tiktok.com, sign up with dedicated email
- [ ] Verify phone number (can reuse same number for up to 3 accounts)
- [ ] Set profile photo and bio
- [ ] Switch to Business account (free, gives analytics + commercial music library)
- [ ] Link to relevant product/newsletter in bio
- [ ] Watch 30+ minutes of niche content (trains the algorithm on your category)
- [ ] Like 20+ videos in your niche (same reason)
- [ ] Post first video (can be a text-over-background format, no face needed)

**Warmup schedule:**
- Days 1-3: Watch niche content, like/comment, post 1 video/day
- Days 4-7: Post 2-3 videos/day, engage in comments on similar creators
- Day 8+: Full posting schedule, 3-5 videos/day

```bash
python3 scripts/account_tracker.py add --platform TikTok --username <handle> --email <email> --status CREATED --niche <niche>
```

---

### 3C. Instagram (3 accounts)

**URL:** instagram.com
**Signup time:** 5 minutes per account (15 min total)
**What it unlocks:** Visual content distribution, Reels (same as TikTok but different audience), link in bio for products, IG Shopping
**What to have ready:** 3 email addresses, profile photos, Reels content

**3 accounts to create:**

| Account | Niche | Content type |
|---------|-------|-------------|
| Faith | Prayer/devotion | Quote cards, Reels, prayer prompts |
| Fitness | Workout/health | Workout clips, progress photos, Reels |
| Tech/brand | Building-in-public | Dashboard screenshots, code snippets, founder content |

**For each account:**
- [ ] Go to instagram.com, sign up with dedicated email
- [ ] Verify email/phone
- [ ] Set profile photo, write bio (150 chars max)
- [ ] Switch to Professional account (Creator or Business, free)
- [ ] Link Beehiiv newsletter or Gumroad in bio (use Linktree or bio.link if multiple)
- [ ] Post 3 initial posts (carousel, Reel, static image)
- [ ] Follow 50 niche accounts

**Warmup:** Same pattern as Twitter. Organic engagement for 7 days before going full speed.

```bash
python3 scripts/account_tracker.py add --platform Instagram --username <handle> --email <email> --status CREATED --niche <niche>
```

---

### 3D. YouTube (2 faceless channels)

**URL:** youtube.com
**Signup time:** 10 minutes per channel (20 min total)
**What it unlocks:** YouTube Partner Program ad revenue, long-form SEO content, Shorts (TikTok equivalent), highest RPM of all platforms
**What to have ready:** Google accounts (one per channel), channel art, video content ideas

**2 channels to create:**

| Channel | Niche | Content type |
|---------|-------|-------------|
| Tech/AI | Productivity + solopreneurship | Faceless explainer videos, screen recordings, Shorts |
| Health/sleep | Sleep + fitness data | Data visualizations, tips, product reviews, Shorts |

**For each channel:**
- [ ] Sign into a Google account (or create one)
- [ ] Go to youtube.com, click your avatar > Create a channel
- [ ] Set channel name (niche-relevant, not generic)
- [ ] Upload profile picture and banner (2560x1440px)
- [ ] Write channel description (2-3 sentences, what viewers get + posting schedule)
- [ ] Add links to products/newsletter in About section
- [ ] Upload first video or Short (can be a simple screen recording with voiceover)
- [ ] Set default upload settings (category, tags, language)

**Monetization path:** 1,000 subscribers + 4,000 watch hours OR 10M Shorts views in 90 days. Faceless channels with consistent posting reach this in 3-6 months.

```bash
python3 scripts/account_tracker.py add --platform YouTube --username <channel> --email <email> --status CREATED --niche <niche>
```

---

**PHASE 3 CHECKPOINT:** All social accounts created. Warmup period begins. Post daily using content from `AUTOMATIONS/content_posting/`. Full speed posting starts after 7 days of warmup.

---

## PHASE 4: Freelance / Service Platforms

**Time:** 45-60 minutes total
**Prerequisite:** PayPal account (Phase 1B), headshot photo
**Why:** Direct revenue from services. Fiverr gigs are copy-paste ready. Upwork profiles are pre-written. Cold outreach fills the pipeline while these platforms warm up.

---

### 4A. Fiverr

**URL:** fiverr.com
**Signup time:** 15 minutes for account, 30 minutes to list first 5 gigs
**What it unlocks:** Service revenue ($50-$500/order), freelance arbitrage (outsource fulfillment)
**What to have ready:** Professional headshot, service descriptions from `OPS/FIVERR_LAUNCH_PACKAGE.md` (5 gigs copy-paste ready)
**Detailed guide:** `OPS/FIVERR_LAUNCH_CHECKLIST.md` + `OPS/FIVERR_LAUNCH_PACKAGE.md`

**Steps:**
- [ ] Go to fiverr.com, click "Become a Seller"
- [ ] Sign up with business email
- [ ] Complete seller profile:
  - [ ] Professional photo (real, clear face, neutral background)
  - [ ] Display name (professional)
  - [ ] Description: 2-3 paragraphs, lead with results
  - [ ] Languages: English (Native/Fluent)
  - [ ] Skills: add all relevant
- [ ] Create first 5 gigs (copy-paste from `OPS/FIVERR_LAUNCH_PACKAGE.md`):
  - [ ] Gig 1: Video clipping service
  - [ ] Gig 2: Landing page builds
  - [ ] Gig 3: AI automation setup
  - [ ] Gig 4: Content writing pack
  - [ ] Gig 5: Notion dashboard design
- [ ] For each gig: title, category, 3-tier pricing, description, requirements, 3+ gallery images, FAQ
- [ ] Publish all gigs

**Warmup (days 2-7):**
- Check Buyer Requests daily, apply to 5+ with personalized proposals
- Share gig links on social and Reddit (r/forhire)
- Offer first order at discount for a review

```bash
python3 scripts/account_tracker.py add --platform Fiverr --username <handle> --email <email> --status ACTIVE
```

---

### 4B. Upwork

**URL:** upwork.com
**Signup time:** 30 minutes (profile is more detailed than Fiverr)
**What it unlocks:** Higher-ticket freelance ($500-$5,000+ projects), recurring clients, agency scaling
**What to have ready:** Government ID (verification required), portfolio samples, profile text from `OPS/UPWORK_LAUNCH_CHECKLIST.md`
**Detailed guide:** `OPS/UPWORK_LAUNCH_CHECKLIST.md` (629 lines)

**Steps:**
- [ ] Go to upwork.com/signup, sign up as Freelancer
- [ ] Use real name (Upwork verifies identity)
- [ ] Upload professional headshot (NOT AI-generated, Upwork detects this)
- [ ] Verify identity (government ID)
- [ ] Complete profile:
  - [ ] Professional title: "AI Automation Specialist" (specific, not generic)
  - [ ] Rate: $75/hour (can adjust per proposal)
  - [ ] Overview: 3-4 paragraphs (pre-written in `OPS/UPWORK_LAUNCH_CHECKLIST.md`)
  - [ ] Skills: 10+ relevant tags
  - [ ] Portfolio: 3-5 samples (create if needed)
- [ ] Create specialized profiles (up to 2 beyond main):
  - [ ] Profile 1: AI/Automation specialist
  - [ ] Profile 2: Web development / landing pages
- [ ] Connect PayPal for payouts (Settings > Get Paid)
- [ ] Send first 5 proposals (you start with 40 free Connects, each proposal costs 2-6)

**Warmup:**
- Send 3-5 proposals per day for first 2 weeks
- Price first 2-3 jobs at a discount to build reviews
- Focus on jobs with <10 proposals (less competition)

```bash
python3 scripts/account_tracker.py add --platform Upwork --username <name> --email <email> --status ACTIVE
```

---

**PHASE 4 CHECKPOINT:** Freelance profiles live. Start sending proposals immediately. First revenue from services typically in 1-2 weeks.

---

## PHASE 5: Email + Outreach Infrastructure

**Time:** 30-45 minutes active, 14 days warmup
**Prerequisite:** None (can start in parallel with Phase 2)
**Why:** Cold email is the single fastest path to $3K+ revenue (proven: 500 emails, 2 clients, $3,000 in 30 days). But inboxes need 14 days of warmup before you can send at volume.
**Detailed guide:** `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md` (748 lines)

---

### 5A. Cold email domains (3 domains)

**URL:** namecheap.com or porkbun.com
**Signup time:** 10 minutes
**Cost:** $30-45 total (3 domains at $10-15 each)
**What it unlocks:** Dedicated cold outreach without risking your main domain

**Steps:**
- [ ] Go to namecheap.com
- [ ] Search and purchase 3 domains. Naming pattern:
  - [ ] [yourname]agency.com (e.g., printmaxxagency.com)
  - [ ] [yourname]dev.com (e.g., printmaxxdev.com)
  - [ ] [yourname]consulting.com (e.g., printmaxxconsulting.com)
- [ ] Purchase all 3 ($30-45 total)
- [ ] Save login credentials in password manager

**Important:** Never use your main domain for cold email. If a cold domain gets flagged, your main brand stays clean.

---

### 5B. Google Workspace mailboxes (3 inboxes)

**URL:** workspace.google.com
**Signup time:** 15 minutes (5 min per domain)
**Cost:** $18/month total ($6/month per mailbox)
**What it unlocks:** Professional email addresses for outreach, SPF/DKIM/DMARC authentication

**Steps:**
- [ ] Go to workspace.google.com/signup
- [ ] For each of the 3 domains:
  - [ ] Enter domain name
  - [ ] Create admin account: outreach@[domain].com
  - [ ] Pick Google Workspace Starter ($6/month)
  - [ ] Verify domain ownership (add TXT record to DNS in Namecheap)
  - [ ] Set up SPF record (TXT record in DNS)
  - [ ] Set up DKIM record (from Google Admin Console)
  - [ ] Set up DMARC record (TXT record in DNS)

**DNS records to add for each domain (in Namecheap DNS settings):**
```
SPF:   TXT  @  v=spf1 include:_spf.google.com ~all
DKIM:  TXT  google._domainkey  (get value from Google Admin Console > Apps > Google Workspace > Gmail > Authenticate email)
DMARC: TXT  _dmarc  v=DMARC1; p=none; rua=mailto:outreach@[domain].com
```

---

### 5C. Instantly.ai (warmup + sequences)

**URL:** instantly.ai
**Signup time:** 10 minutes
**Cost:** $30/month (Growth plan: 1,000 emails/day, unlimited warmup)
**What it unlocks:** Automated email warmup, send sequences, track opens/replies, A/B test subject lines
**What to have ready:** 3 Google Workspace mailboxes (from 5B), email sequences from `CONTENT/email_sequences/cold/`

**Steps:**
- [ ] Go to instantly.ai, sign up
- [ ] Pick Growth plan ($30/month)
- [ ] Connect all 3 email accounts:
  - [ ] Settings > Email Accounts > Add Account
  - [ ] Connect each Google Workspace inbox via OAuth
- [ ] Enable warmup on ALL 3 accounts immediately:
  - [ ] Daily warmup limit: 30 emails/day (starts slow, ramps up)
  - [ ] Reply rate: 30-40%
  - [ ] Warmup tag: leave default
- [ ] Wait 14 days before sending any real cold emails (critical - sending before warmup destroys deliverability)
- [ ] While waiting: build prospect lists using Apollo.io free tier, prepare email sequences

**After 14-day warmup:**
- [ ] Create first campaign:
  - [ ] Upload prospect list (from `AUTOMATIONS/savvy_lead_scraper.py` output or Apollo.io)
  - [ ] Paste email sequence (from `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md`)
  - [ ] Set sending limit: 25 emails/day per inbox (75 total/day across 3)
  - [ ] Set sending window: 8 AM - 5 PM recipient timezone
  - [ ] Enable open tracking, reply detection
  - [ ] Launch campaign

```bash
python3 scripts/account_tracker.py add --platform Instantly --username <email> --email <email> --status WARMING_UP
```

---

**PHASE 5 CHECKPOINT:** Cold email infrastructure is live. 14-day warmup running. Use this time to build prospect lists and refine email sequences. First cold emails go out on day 15. First replies by day 17-18. First calls by day 20-22.

---

## Dependency chain (visual)

```
PHASE 1: Payment Rails
  Stripe ─────────────────┐
  PayPal Business ────┐   │
                      │   │
PHASE 2: Products     │   │
  Gumroad ────────────┼───┤ (needs Stripe)
  Whop ───────────────┼───┤ (needs Stripe)
  Beehiiv ────────────┼───┘ (needs Stripe for paid subs)
  Substack ───────────┘
                      │
PHASE 3: Social       │ (needs product links for bios)
  Twitter x5 ─────────┤
  TikTok x3 ──────────┤
  Instagram x3 ────────┤
  YouTube x2 ──────────┘
                      │
PHASE 4: Freelance    │ (needs PayPal for payouts)
  Fiverr ─────────────┤
  Upwork ─────────────┘

PHASE 5: Cold Email   (independent - start in parallel)
  Domains ────────────┐
  Google Workspace ───┤
  Instantly.ai ───────┘ (14-day warmup required)
```

---

## Time estimates (realistic)

| Phase | Active time | Wait time | Accounts created |
|-------|-------------|-----------|------------------|
| Phase 1: Payment rails | 30 min | 24-48 hrs (Stripe verification) | 2 |
| Phase 2: Product platforms | 90 min | None | 4 |
| Phase 3: Social media | 60-75 min | 7-day warmup (organic) | 13 |
| Phase 4: Freelance | 45-60 min | None (start proposing immediately) | 2 |
| Phase 5: Cold email | 30-45 min | 14-day warmup (automated) | 4 |
| **Total** | **~4 hours** | **14 days (warmup runs in background)** | **25 accounts** |

---

## After all accounts are created

### Day 1 (after Phase 1-4 complete)
- [ ] All 10 Gumroad products live
- [ ] 4 Beehiiv newsletters live with welcome sequences
- [ ] Substack publication live with first article
- [ ] All 13 social accounts created and posting
- [ ] Fiverr gigs live (5 gigs)
- [ ] Upwork profile live, first 5 proposals sent
- [ ] Cold email warmup running on 3 inboxes
- [ ] Run: `python3 scripts/account_tracker.py status` to verify all accounts

### Day 7
- [ ] Social accounts past warmup, full posting schedule active
- [ ] Upload content from `AUTOMATIONS/content_posting/` to Buffer for scheduling
- [ ] Fiverr: check Buyer Requests daily, 5+ proposals sent
- [ ] Upwork: 3-5 proposals per day
- [ ] First Gumroad/Whop sales expected (share links on all social accounts)

### Day 14
- [ ] Cold email warmup complete
- [ ] Launch first cold email campaign (75 emails/day)
- [ ] Social accounts fully active across all niches
- [ ] First freelance clients from Fiverr/Upwork expected
- [ ] Run: `python3 scripts/self_test.py` to check all op readiness scores

### Day 30
- [ ] Cold email: 1,500+ emails sent, first replies and calls
- [ ] Gumroad: 10-30 sales ($70-$500 revenue)
- [ ] Freelance: 2-5 clients ($500-$3,000 revenue)
- [ ] Newsletters: 50-200 subscribers across 4 publications
- [ ] Social: 100-500 followers per account
- [ ] Run: `python3 scripts/revenue_intake.py dashboard` to see revenue across all sources

---

## Tracking commands (run daily)

```bash
# See all accounts and their status
python3 scripts/account_tracker.py status

# See what's blocking progress
python3 scripts/account_tracker.py blockers

# Log revenue from any platform
python3 scripts/revenue_intake.py log --method <ID> --amount <$> --source <platform>

# See total revenue dashboard
python3 scripts/revenue_intake.py dashboard

# Check op readiness scores
python3 scripts/self_test.py
```

---

## Troubleshooting

**Stripe verification stuck:** Check email for documentation requests. Upload utility bill or bank statement. Contact support after 72 hours.

**Twitter account suspended during creation:** IP flagged. Use a different network (phone hotspot vs wifi). Wait 24 hours between account creations. Don't create more than 2 per day from same IP.

**Fiverr profile rejected:** Profile photo doesn't meet guidelines (too dark, sunglasses, AI-generated detected). Use a real photo with clear face, good lighting, plain background.

**Upwork identity verification failed:** Government ID must match the name on the account exactly. No nicknames. If rejected, contact support with additional documentation.

**Instantly warmup not improving:** Check DNS records are correct (SPF, DKIM, DMARC). Run deliverability test at mail-tester.com. If inbox placement is below 80%, check for domain blacklisting.

**Gumroad products not selling:** Share on social media. Post direct links in relevant communities (Reddit, Discord). Offer launch discount. Get first 3 reviews (offer free product for honest review).
