# TECH INFRASTRUCTURE SETUP - RETARDMAXXED

**Last Updated:** 2026-02-05
**Purpose:** Actual tech infra - proxies, anti-detect, warmed accounts, the real stack

---

## STACK OPTIONS BY BUDGET

Pick your budget tier, follow that stack exactly.

### 🆓 TIER 0: ZERO BUDGET ($0/mo)
**Who:** Testing before spending, ultra-bootstrap mode
**Limitation:** Manual posting only, no automation, new account penalties

| Component | Tool | Cost | What You Get |
|-----------|------|------|---------------|
| **Proxies** | None | $0 | Use home IP (risky for multiple accounts) |
| **Anti-Detect** | GoLogin Free | $0 | 3 browser profiles max |
| **Accounts** | Manual creation | $0 | New accounts (3-5 day warmup required) |
| **Email** | Gmail free | $0 | Manual warmup (14-21 days) |
| **Posting** | Manual | $0 | You post everything by hand |

**Reality Check:** This works but you're fighting platform algorithms. New accounts = shadowbanned. No proxies = account linking. Manual warmup takes weeks.

**Upgrade When:** You hit $500/mo revenue OR you're serious about scaling

---

### 💰 TIER 1: BOOTSTRAP STACK ($200 one-time + $150-300/mo)
**Who:** First revenue coming in, ready to automate
**Sweet Spot:** Best bang for buck, 80% of results at 20% cost

| Component | Tool | Cost | Setup Link |
|-----------|------|------|------------|
| **Proxies** | SOAX Mobile | $50/mo | https://soax.com |
| **Anti-Detect** | GoLogin Pro | $49/mo | https://gologin.com |
| **Phone Numbers** | SMSPool | $10 one-time | https://smspool.net |
| **Email** | Google Workspace | $18/mo (3 inboxes) | https://workspace.google.com |
| **Email Warmup** | Instantly.ai | $97/mo | https://instantly.ai |
| **Accounts** | Manual creation | $0 | Create yourself with proxies |
| **Scheduling** | Buffer/Publer | $0-12/mo | https://buffer.com or https://publer.io |

**What This Unlocks:**
- 3-5 social accounts (IG/TikTok/X) running safely
- Cold email that actually delivers
- Browser fingerprinting protection
- Mobile IP rotation (looks like real users)

**Setup Time:** 2-3 hours
**Monthly Cost:** $214-226/mo
**Revenue Unlock:** $1K-10K/mo

---

### 🚀 TIER 2: FIRST SCALE ($500-750/mo)
**Who:** Hitting $3K+/mo, ready to scale accounts
**Focus:** Skip warmup periods, buy initial engagement, more accounts

| Component | Tool | Cost | Why Upgrade |
|-----------|------|------|-------------|
| **Proxies** | SOAX Mobile | $100/mo | 2x IPs, run 6-10 accounts |
| **Anti-Detect** | GoLogin Pro | $49/mo | Same (10 profiles enough) |
| **Pre-Warmed Accounts** | AccsMarket | $60-120 one-time | Skip new account penalty |
| **Pre-Warmed Inboxes** | DeliverOn | $49/mo | Skip 14-day warmup, 3 ready inboxes |
| **OR** | EmailBison | $99/mo | 10 pre-warmed inboxes (if doing volume) |
| **Lead Data** | Apollo.io | $79/mo | Verified emails for cold outbound |
| **Scheduling** | Publer | $12/mo | Bulk upload, more channels |
| **Initial Engagement** | Kicksta (IG) | $49/mo | Trigger algorithm (cancel after boost) |

**What This Unlocks:**
- 6-10 social accounts running
- Cold email at scale (200+ sends/day)
- Pre-warmed = skip weeks of setup
- Bought engagement = algorithm boost

**Setup Time:** 1-2 hours
**Monthly Cost:** $500-750/mo
**Revenue Unlock:** $5-25K/mo

---

### 💎 TIER 3: FULL SCALE ($1,500-2,500/mo)
**Who:** $10K+/mo revenue, scaling hard
**Focus:** VA team, LinkedIn automation, paid ads, premium tools

| Component | Tool | Cost | Why Premium |
|-----------|------|------|-------------|
| **Proxies** | SOAX Mobile | $200/mo | Run 15-20 accounts |
| **Anti-Detect** | GoLogin Pro | $49/mo | Still enough |
| **Pre-Warmed Inboxes** | Smartlead | $39-99/mo | Better deliverability |
| **+ AI Personalization** | Clay | $149/mo | 7x reply rate vs generic |
| **LinkedIn** | Sales Navigator | $80-135/mo | Better lead lists |
| **LinkedIn Automation** | Expandi (safest) | $99/mo | Cloud-based, no bans |
| **VA** | OnlineJobs.ph | $400/mo | Part-time VA for posting/outreach |
| **Paid Ads Test** | Meta + TikTok | $500/mo | Test winners only |
| **CRM** | Close.com | $49/mo | Track deals properly |

**What This Unlocks:**
- 15-20 accounts automated
- Cold email personalized at scale
- LinkedIn outreach running
- VA handles manual tasks
- Paid ads on proven content

**Setup Time:** 4-6 hours + VA onboarding
**Monthly Cost:** $1,500-2,500/mo
**Revenue Unlock:** $15-50K/mo

---

### 🏆 TIER 4: ENTERPRISE ($3,000-8,000/mo)
**Who:** $25K+/mo revenue, full team
**Focus:** Enterprise tools, multiple VAs, clipping army, communities

| Component | Tool | Cost | Enterprise Features |
|-----------|------|------|---------------------|
| **Proxies** | SOAX or Bright Data | $500+/mo | Unlimited IPs, all types |
| **Anti-Detect** | Multilogin | $99-399/mo | Unlimited profiles, better fingerprinting |
| **Team** | 2-3 VAs | $1,000-2,000/mo | Content, posting, outreach, support |
| **Cold Email** | Smartlead + Clay | $188/mo | AI personalization, max scale |
| **Paid Ads** | Meta + TikTok | $2,000-5,000/mo | Aggressive scaling on winners |
| **Communities** | Skool | $99/mo per community | Membership revenue |
| **Clipping Army** | Whop + bounties | $1,700+/mo | 750+ clippers, 10M+ views/mo |

**What This Unlocks:**
- 30+ accounts running
- Full team leverage
- Paid ads at scale
- Community revenue stacking
- Distribution army (Tate playbook)

**Setup Time:** 1-2 weeks (team onboarding)
**Monthly Cost:** $3,000-8,000/mo
**Revenue Unlock:** $50-150K/mo

---

## SPECIFIC TOOL SETUP GUIDES

### 📱 SOAX Mobile Proxies Setup

**Why Mobile Proxies:**
- Instagram/TikTok detect datacenter IPs instantly
- Mobile IPs = real user behavior
- IP rotation every request or time-based

**Setup:**
1. Go to: https://soax.com
2. Sign up
3. Add balance ($50 minimum)
4. Dashboard → Get Credentials
   - Proxy type: Mobile (4G/5G)
   - Country: US (or your target geo)
   - Rotation: 5-10 min
5. Copy proxy string: `username:password@proxy.soax.com:port`
6. Add to anti-detect browser (see below)

**Config File Location:** `AUTOMATIONS/SOAX_MOBILE_PROXIES.md`

**Cost:**
- $50/mo: ~15GB traffic (good for 3-5 accounts)
- $100/mo: ~35GB traffic (6-10 accounts)
- $200/mo: ~75GB traffic (15-20 accounts)

---

### 🌐 GoLogin Anti-Detect Browser Setup

**Why Anti-Detect:**
- Each browser profile = unique fingerprint
- Prevents account linking
- Mimics real devices (fonts, canvas, WebGL, etc.)

**Setup:**
1. Go to: https://gologin.com
2. Download app (Mac/Windows/Linux)
3. Sign up
   - Free: 3 profiles
   - Pro ($49/mo): 10 profiles
4. Create Profile:
   - Click "New Profile"
   - Name: "IG_FaithNiche" (or descriptive)
   - OS: Random (or match your real OS)
   - Proxy: Add SOAX proxy string
   - Geolocation: Match proxy country
   - Timezone: Auto (matches geo)
   - WebRTC: Altered
   - Canvas: Noise
   - Fonts: Real fonts (don't use "Off")
5. Launch profile
6. Log in to social account
7. Close profile (saves cookies + session)

**Best Practices:**
- 1 profile = 1 account (never reuse)
- Name profiles clearly (platform_niche_accountname)
- Keep profiles running while active (don't close mid-session)
- Use different proxy per profile

**When to Upgrade to Multilogin ($99/mo):**
- Need 10+ profiles
- Running high-value accounts (avoid bans at all costs)
- Enterprise clients (better fingerprinting)

---

### 📧 Pre-Warmed Email Inbox Setup (Skip 14-Day Warmup)

**Option A: DeliverOn ($49/mo) - FASTEST**

**Why:**
- 3 inboxes pre-warmed and ready DAY 1
- Skip 14-21 day warmup entirely
- Good deliverability out of the box

**Setup:**
1. Go to: https://deliveron.org
2. Sign up ($49/mo)
3. Get 3 inbox credentials (they provide)
4. Load your email sequences from `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES/`
5. Start sending same day (20-30 emails/inbox/day to start)

**When to Use:** You need cold email running THIS WEEK, can't wait 2 weeks

---

**Option B: EmailBison ($99/mo) - VOLUME**

**Why:**
- 10 pre-warmed inboxes
- Higher volume capacity
- Better for scaling (200+ sends/day total)

**Setup:**
1. Go to: https://emailbison.com
2. Sign up ($99/mo)
3. Get 10 inbox credentials
4. Connect to cold email tool (Instantly, Smartlead, etc.)
5. Start sending

**When to Use:** You're doing serious volume (500+ sends/day), have good leads

---

**Option C: Instantly.ai ($97/mo) - DIY AUTO-WARMUP**

**Why:**
- Cheaper if you can wait 14-21 days
- Unlimited inboxes (you provide domains)
- Auto-warmup included

**Setup:**
1. Buy 3-5 domains on Porkbun ($12 each)
2. Set up Google Workspace ($6/user/mo)
3. Connect to Instantly.ai
4. Enable auto-warmup
5. Wait 14-21 days
6. Start sending (50 emails/inbox/day max)

**When to Use:** You're not in a rush, want to own infrastructure

---

### 🛒 Buy Pre-Warmed Social Accounts (Skip New Account Penalty)

**Why Buy Warmed Accounts:**
- New accounts = shadowbanned for 7-30 days
- Pre-warmed = algorithm trusts them already
- Instant posting, no warmup period

**Where to Buy:**

**Option A: AccsMarket** (https://accsmarket.com)
- Price: $15-80 per account
- Platforms: IG, TikTok, X/Twitter, FB
- Quality: 6-12 months old, activity history
- **Best for:** Bootstrap budget

**Option B: Fameswap** (https://fameswap.com)
- Price: $100-10K (some have followers already)
- Platforms: IG, TikTok, YouTube
- Quality: Aged accounts, some with 1K-100K followers
- **Best for:** Buying starter audience

**Option C: SocialTradia** (https://socialtradia.com)
- Price: $50-5K
- Platforms: All major platforms
- Quality: Mixed (check reviews per seller)

**What to Check Before Buying:**
- Account age (6+ months minimum)
- Activity history (regular posts, not dormant)
- No policy violations (check account health)
- Email access included
- 2FA recovery codes provided

**After Buying:**
1. Change password immediately
2. Add your 2FA
3. Manual activity 3-5 days (browse, like, comment - NO posting)
4. Then light posting (1-2x/day)
5. Ramp to normal schedule after 7 days

**Cost:**
- Bootstrap: 3 accounts × $20-40 = $60-120 one-time
- Scale: 10 accounts × $30-50 = $300-500 one-time

---

### 📞 SMSPool for Phone Verification

**Why:**
- Platforms require phone verification
- Don't use your real number (account linking risk)
- Cheap virtual numbers

**Setup:**
1. Go to: https://smspool.net
2. Add $10 balance
3. When creating account, select:
   - Service: Instagram / TikTok / Twitter
   - Country: US (or target geo)
   - Get number
4. Use number for verification
5. Receive SMS in SMSPool dashboard
6. Enter code on platform

**Cost:** ~$0.50-$2 per verification (depends on platform)
**Budget:** $10 = 5-20 verifications

---

## COMPLETE TIER 1 SETUP WALKTHROUGH (STEP-BY-STEP)

**Budget:** $200 one-time + $214/mo
**Time:** 2-3 hours
**Result:** 3-5 accounts running with automation + cold email ready

### Step 1: SOAX Proxies (10 min)
1. Go to https://soax.com
2. Sign up
3. Add $50 balance
4. Dashboard → Mobile Proxies → US
5. Copy proxy credentials
6. Save to: `AUTOMATIONS/SOAX_CREDENTIALS.txt` (gitignored)

### Step 2: GoLogin Anti-Detect (15 min)
1. Go to https://gologin.com
2. Download app
3. Sign up ($49/mo for Pro - need 10 profiles)
4. Create 5 profiles:
   - Profile 1: "IG_Faith" + SOAX proxy
   - Profile 2: "IG_Fitness" + SOAX proxy (different IP)
   - Profile 3: "TikTok_Faith" + SOAX proxy
   - Profile 4: "TikTok_Fitness" + SOAX proxy
   - Profile 5: "Twitter_Main" + SOAX proxy
5. Test each profile (launch, check IP at https://whoer.net, should show mobile + US)

### Step 3: SMSPool Phone Numbers (5 min)
1. Go to https://smspool.net
2. Add $10
3. Ready to use when creating accounts

### Step 4: Create Social Accounts (30 min)
**For EACH account:**
1. Launch GoLogin profile
2. Go to platform signup
3. Use unique email (create 5 new Gmail accounts)
4. Get SMSPool number for verification
5. Complete signup
6. Add profile pic + bio + link
7. Enable 2FA (save codes)
8. Close profile (saves session)

**Accounts to create:**
- Instagram: Faith niche
- Instagram: Fitness niche
- TikTok: Faith niche
- TikTok: Fitness niche
- X/Twitter: @PRINTMAXXER

### Step 5: Warmup Period (3-5 days)
**Manual activity ONLY - NO POSTING:**
- Launch each GoLogin profile daily
- Browse feed 5-10 min
- Like 10-20 posts
- Follow 5-10 accounts (relevant to niche)
- Comment 2-3 times (genuine, not spammy)
- Close profile

**Do this for 3-5 days before first post.**

### Step 6: Google Workspace for Email (10 min)
1. Buy 3 domains on Porkbun ($36 total)
   - printmaxx-hq.com
   - printmaxx-mail.com
   - printmaxx-co.com
2. Go to https://workspace.google.com
3. Create 3 inboxes per domain:
   - sales@printmaxx-hq.com
   - support@printmaxx-mail.com
   - hello@printmaxx-co.com
4. Cost: $18/mo (3 inboxes)

### Step 7: DNS Setup for Email Deliverability (20 min)
**For EACH domain:**
1. Go to Cloudflare (free DNS)
2. Add domain
3. Update nameservers at Porkbun
4. Add DNS records:

**SPF Record:**
```
Type: TXT
Name: @
Content: v=spf1 include:_spf.google.com ~all
```

**DKIM Record:**
1. Google Workspace Admin → Apps → Gmail → Authenticate
2. Generate DKIM key
3. Copy TXT record to Cloudflare DNS

**DMARC Record:**
```
Type: TXT
Name: _dmarc
Content: v=DMARC1; p=none; rua=mailto:dmarc@printmaxx-hq.com
```

### Step 8: Instantly.ai Email Warmup (15 min)
1. Go to https://instantly.ai
2. Sign up ($97/mo)
3. Connect 3 Google Workspace inboxes
4. Enable auto-warmup
5. Settings:
   - Warmup emails/day: 20 (increase gradually)
   - Warmup duration: 14-21 days
6. Let it run for 2 weeks before cold sending

### Step 9: Buffer/Publer Scheduling (10 min)
1. Go to https://publer.io (or https://buffer.com)
2. Sign up ($12/mo for Publer)
3. Connect your social accounts (IG, TikTok, Twitter)
4. Tell agent: **"Upload 30 days of content to Publer for all accounts"**
5. Agent formats and uploads from `LEDGER/CONTENT_CALENDAR_30DAY.csv`

### Step 10: First Content (After 3-5 Day Warmup)
**Days 4-7:**
- First 10 posts per account = TEXT ONLY (no links)
- Post 1x/day per account
- Engage with replies

**Days 8-14:**
- Ramp to 2x/day
- Add links to bio (not in posts yet)

**Days 15+:**
- 3x/day posting
- Links allowed in posts
- Full automation via Publer

---

## TIER 1 COMPLETE SHOPPING LIST

**One-Time Purchases:**
| Item | Cost | Where |
|------|------|-------|
| 3 domains | $36 | https://porkbun.com |
| SMSPool balance | $10 | https://smspool.net |
| **Total One-Time** | **$46** | |

**Monthly Subscriptions:**
| Tool | Cost | Where |
|------|------|-------|
| SOAX Proxies | $50/mo | https://soax.com |
| GoLogin Pro | $49/mo | https://gologin.com |
| Google Workspace | $18/mo | https://workspace.google.com |
| Instantly.ai | $97/mo | https://instantly.ai |
| Publer | $12/mo | https://publer.io |
| **Total Monthly** | **$226/mo** | |

**Grand Total:** $46 one-time + $226/mo

---

## UPGRADE PATHS

### From Tier 1 → Tier 2 ($500-750/mo)
**Add:**
- More SOAX bandwidth ($50 → $100/mo)
- DeliverOn pre-warmed inboxes ($49/mo)
- AccsMarket accounts ($60-120 one-time)
- Apollo.io lead data ($79/mo)
- Kicksta initial engagement ($49/mo for 1 month)

### From Tier 2 → Tier 3 ($1,500-2,500/mo)
**Add:**
- Clay AI personalization ($149/mo)
- LinkedIn Sales Navigator ($80/mo)
- Expandi automation ($99/mo)
- VA part-time ($400/mo)
- Paid ads test budget ($500/mo)
- Close.com CRM ($49/mo)

### From Tier 3 → Tier 4 ($3,000-8,000/mo)
**Add:**
- More VAs ($1,000-2,000/mo total)
- Paid ads scale ($2,000-5,000/mo)
- Multilogin ($99-399/mo)
- Communities (Skool $99/mo)
- Clipping army ($1,700+/mo)

---

## DANGER ZONES & COMMON MISTAKES

❌ **Using same proxy for multiple accounts** → All accounts get linked and banned
✅ **Use 1 proxy per account, different IPs**

❌ **Skipping warmup period** → Instant shadowban
✅ **3-5 days manual activity before posting**

❌ **Posting links on new accounts** → Flagged as spam
✅ **Text-only posts for first 10 posts**

❌ **Using datacenter proxies for IG/TikTok** → Detected instantly
✅ **Mobile proxies only (SOAX, not cheap residential)**

❌ **Sending cold email from new domain** → 90% spam folder
✅ **14-21 day warmup mandatory**

❌ **Buying cheap sketchy accounts** → Banned within days
✅ **AccsMarket/Fameswap only, check seller reviews**

---

## READY TO START?

**Pick your tier:**
- **Tier 1** ($226/mo) - Most people start here
- **Tier 2** ($500-750/mo) - If you have budget and want speed
- **Tier 3** ($1,500+/mo) - If you're already making $10K+/mo

Tell me: **"Set up Tier X infrastructure"** and I'll generate:
- All signup URLs in order
- Proxy configs ready to copy-paste
- GoLogin profile settings
- DNS records formatted
- Account creation checklist

Or tell me: **"I want to start but I'm confused"** and I'll simplify it even more.
