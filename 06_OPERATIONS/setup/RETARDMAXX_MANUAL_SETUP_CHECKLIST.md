# RETARDMAXX MANUAL SETUP CHECKLIST

**Last Updated:** 2026-01-24
**Purpose:** Every manual task that requires human action. Go here, click here, buy this, set up like this.

---

## PHASE 1: FOUNDATION ($150-200)

### Apple Developer Account - $99/year
- [ ] Go to: https://developer.apple.com/programs/enroll/
- [ ] Click "Start Your Enrollment"
- [ ] Sign in with Apple ID (use business email, not personal)
- [ ] Pay $99
- [ ] Wait 24-48 hours (sometimes video call required)
- [ ] Once approved, go to App Store Connect: https://appstoreconnect.apple.com

### Google Play Developer - $25 one-time
- [ ] Go to: https://play.google.com/console/signup
- [ ] Sign in with Google account
- [ ] Pay $25
- [ ] Wait 24-48 hours for approval
- [ ] Once approved: https://play.google.com/console

### Soax Proxies - $50 minimum
- [ ] Go to: https://soax.com
- [ ] Sign up with email
- [ ] Select "Residential Proxies"
- [ ] Add $50 minimum balance
- [ ] Get credentials from dashboard: `user:pass@proxy.soax.com:port`
- [ ] For social media: Use sticky sessions (30 min)

### SMSPool - $10-20
- [ ] Go to: https://smspool.net
- [ ] Create account
- [ ] Add $10-20 balance
- [ ] Use for: TikTok, Instagram phone verification
- [ ] Track which numbers used for which accounts (don't reuse)

### Primary Domain - $10-15/year
- [ ] Go to: https://porkbun.com or https://namecheap.com
- [ ] Search for your domain (printmaxx.io, yourapp.app, etc.)
- [ ] Buy it
- [ ] Point nameservers to Cloudflare (next step)

---

## PHASE 2: EMAIL & DOMAINS ($50-100)

### Cloudflare DNS (Free)
- [ ] Go to: https://cloudflare.com
- [ ] Create account
- [ ] Click "Add Site"
- [ ] Enter your domain
- [ ] Copy the 2 nameservers they give you
- [ ] Go back to your domain registrar
- [ ] Update nameservers to Cloudflare's

### Cold Email Domains (3 minimum) - $30-45/year
- [ ] Buy 3 DIFFERENT domains for cold email (protect main domain)
- [ ] Use different registrar than main domain
- [ ] Example names: yourcompany-hq.com, yourcompany-mail.com, yourcompany-team.com
- [ ] Add all 3 to Cloudflare

### Google Workspace - $6/user/month
- [ ] Go to: https://workspace.google.com
- [ ] Sign up with your cold email domain
- [ ] Create 2-3 inboxes per domain:
  - sales@yourdomain.com
  - support@yourdomain.com
  - noreply@yourdomain.com
- [ ] Total: 6-9 email addresses across 3 domains

### DNS Records Setup (CRITICAL for email)
For EACH domain in Cloudflare:

**SPF Record:**
- [ ] Type: TXT
- [ ] Name: @
- [ ] Value: `v=spf1 include:_spf.google.com ~all`

**DKIM Record:**
- [ ] Go to Google Workspace Admin: https://admin.google.com
- [ ] Navigate: Apps > Google Workspace > Gmail > Authenticate Email
- [ ] Click "Generate New Record"
- [ ] Copy the TXT record to Cloudflare

**DMARC Record:**
- [ ] Type: TXT
- [ ] Name: _dmarc
- [ ] Value: `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com`

---

## PHASE 3: MONETIZATION SETUP

### RevenueCat Setup (Free tier available)
- [ ] Go to: https://app.revenuecat.com
- [ ] Sign up
- [ ] Create new project: "PRINTMAXX Apps"
- [ ] Click "Add App" for each platform (iOS, Android)

**For iOS app:**
- [ ] In RevenueCat: Apps > iOS > App Store Connect API
- [ ] In App Store Connect: Users and Access > Keys > Generate API Key
- [ ] Download the .p8 file (save it securely!)
- [ ] Copy: Key ID, Issuer ID
- [ ] Paste into RevenueCat

**For Android app:**
- [ ] In RevenueCat: Apps > Android
- [ ] In Play Console: Setup > API Access > Create Service Account
- [ ] Download JSON key
- [ ] Upload to RevenueCat

**Create Products:**
- [ ] In RevenueCat: Products > New Product
- [ ] Product ID format: `app_monthly_999` (999 = $9.99)
- [ ] Create: monthly, annual for each app

**Create Entitlements:**
- [ ] In RevenueCat: Entitlements > New
- [ ] Name: "premium"
- [ ] Add your products to this entitlement

**Create Offerings:**
- [ ] In RevenueCat: Offerings > New
- [ ] Name: "default"
- [ ] Add packages (monthly, annual)

### Stripe Setup
- [ ] Go to: https://stripe.com
- [ ] Create account (or use existing)
- [ ] In RevenueCat: Settings > Billing > Connect Stripe
- [ ] Follow OAuth flow

### App Store Connect - Per App Setup
For each app (PrayerLock, WalkToUnlock, StudyLock):

- [ ] Log in: https://appstoreconnect.apple.com
- [ ] My Apps > + New App
- [ ] Fill in: Name, Primary Language, Bundle ID, SKU
- [ ] Create Subscription Group: "Premium"
- [ ] Add subscription products:
  - Monthly: $9.99 (PrayerLock) / $7.99 (WalkToUnlock) / $6.99 (StudyLock)
  - Annual: $49.99 / $39.99 / $34.99
- [ ] Upload icon (1024x1024)
- [ ] Add 5 screenshots (6.5" iPhone)
- [ ] Add 5 screenshots (12.9" iPad)
- [ ] Write description
- [ ] Set privacy policy URL
- [ ] Set support URL
- [ ] Complete privacy nutrition labels

---

## PHASE 4: SOCIAL ACCOUNTS (Manual Only)

### X/Twitter Accounts
For each niche (AI, Faith, Fitness, Main brand):

- [ ] Go to: https://x.com/i/flow/signup
- [ ] Use unique email (ProtonMail recommended)
- [ ] Complete profile:
  - Profile pic
  - Header image
  - Bio (include niche keywords)
  - Location
  - Website (optional, no links first 2 weeks)
- [ ] Enable 2FA: Settings > Security > Two-factor authentication
- [ ] Save backup codes in password manager
- [ ] Follow 10-20 relevant accounts
- [ ] NO POSTING for first 3-5 days (just engage)
- [ ] First 10 posts: Text only, no links

### TikTok Accounts
For each niche account:

- [ ] Go to: https://www.tiktok.com/signup
- [ ] Use SMSPool for phone verification
- [ ] Complete profile fully
- [ ] Watch videos for 10 minutes (algorithm training)
- [ ] NO links in bio for first week
- [ ] First 7 days: Manual only, no automation
- [ ] First posts: Duets or stitches (engagement signals)

### Instagram Accounts
For each niche account:

- [ ] Go to: https://www.instagram.com/accounts/emailsignup/
- [ ] Use unique email
- [ ] Complete profile with bio
- [ ] Enable 2FA
- [ ] 7-day manual warmup minimum
- [ ] Stories before feed posts
- [ ] Max 50 follows/day even when warm

---

## PHASE 5: PRE-WARMED ACCOUNTS (Optional - $50-200)

### Where to Buy Aged Accounts

**AccsMarket (Best reputation):**
- [ ] Go to: https://accsmarket.com
- [ ] Browse: Twitter/X aged ($15-50), Instagram ($20-80), TikTok ($10-40)
- [ ] Check reviews before buying
- [ ] Look for: 6+ months age, some post history, original email access

**Fameswap (Instagram focus):**
- [ ] Go to: https://fameswap.com
- [ ] Higher quality, verified accounts
- [ ] More expensive ($100+)
- [ ] Use escrow

**SocialTradia (Multi-platform):**
- [ ] Go to: https://socialtradia.com
- [ ] X, IG, TikTok, YouTube
- [ ] Escrow included

**After buying account:**
- [ ] Change password immediately
- [ ] Add your 2FA
- [ ] Change email gradually (some platforms flag this)
- [ ] Manual activity for 3-5 days before automation
- [ ] Assign dedicated proxy to account

---

## PHASE 6: COLD EMAIL & LINKEDIN TOOLS (Week 3-4)

### Pick One Cold Email Tool

**Instantly.ai (Recommended for beginners):**
- [ ] Go to: https://instantly.ai
- [ ] Sign up: $97/mo plan
- [ ] Connect your 3 cold email domains
- [ ] Enable auto-warmup (runs for 14-21 days before sending)

**OR Smartlead:**
- [ ] Go to: https://smartlead.ai
- [ ] Sign up: $39/mo plan
- [ ] Connect domains
- [ ] Enable warmup

**OR EmailBison:**
- [ ] Go to: https://emailbison.com
- [ ] Sign up: $39/mo
- [ ] Connect domains

### Pre-Warmed Email Inboxes (Skip DIY Warmup)

**DeliverOn (Recommended):**
- [ ] Go to: https://deliveron.org
- [ ] $49/mo - Pre-built warm inbox infrastructure
- [ ] Skip 30-day warmup, start sending faster

**MailForge (Bulk/Budget):**
- [ ] Go to: https://mailforge.ai
- [ ] $3/inbox - Bulk warm inboxes
- [ ] Good for scaling to 20+ inboxes

### LinkedIn Automation (Safe Options)

**Expandi (Safest):**
- [ ] Go to: https://expandi.io
- [ ] $99/mo - Cloud-based, anti-detection
- [ ] Safest LinkedIn automation available

**Dripify:**
- [ ] Go to: https://dripify.io
- [ ] $59/mo - LinkedIn drip campaigns
- [ ] Good for sequence building

**InMailers Service:**
- [ ] Go to: https://inmailers.co
- [ ] Outsourced LinkedIn InMail sending
- [ ] Pay per InMail sent

### Apollo.io (Lead Data)
- [ ] Go to: https://apollo.io
- [ ] Sign up: $79/mo Pro plan
- [ ] 275M+ contacts, built-in verification
- [ ] Filter by: Job title, company size, industry, location
- [ ] Export to cold email tool

### Email Verification
- [ ] Go to: https://neverbounce.com OR https://zerobounce.net
- [ ] Add $20-50 credit
- [ ] Verify all lists before sending ($8-16 per 1000 emails)
- [ ] Only send to "valid" emails (not "catch-all")

---

## PHASE 7: CLIP COMMUNITY & AFFILIATE

### Find Streamers to Clip

**TwitchTracker:**
- [ ] Go to: https://twitchtracker.com/channels/ranking
- [ ] Find rising streamers (1K-50K followers)
- [ ] Note their content style

**SullyGnome:**
- [ ] Go to: https://sullygnome.com
- [ ] Browse trending games/categories
- [ ] Find top streamers per game

### Clipper Reward Platforms

**VontenRewards (MrBeast Network):**
- [ ] Go to: https://vontenrewards.gg
- [ ] Apply via form
- [ ] Pay: $1-3/1k views
- [ ] MrBeast/Beast Philanthropy approved clips

**ClippingFor (Marketplace):**
- [ ] Go to: https://clippingfor.com
- [ ] Create clipper profile
- [ ] Browse available gigs
- [ ] Connect with streamers directly

**Clipping Communities:**
- [ ] Reddit: r/YouTubeClippers, r/TwitchClippers
- [ ] Discord: Search "streamer clips" or "clipper community"
- [ ] Twitter: Search "looking for clipper" or "need editor"

### AI Clip Tools

**Opus Clip:**
- [ ] Go to: https://opus.pro
- [ ] $15+/mo - Auto-generates clips from long videos
- [ ] AI highlight detection

**Vizard:**
- [ ] Go to: https://vizard.ai
- [ ] $25+/mo - AI video repurposing
- [ ] Auto-captions and formatting

**Direct Outreach to Streamers:**
```
Template:
"Hey [Streamer], love your content on [game/topic].
I clip/edit for creators and would love to make clips for your TikTok/Shorts.
Free trial - 5 clips to see if you like my style.
DM me if interested."
```

### Affiliate Programs by Niche

**Faith Apps:**
- [ ] Amazon Associates: https://affiliate-program.amazon.com (4-8%)
- [ ] Christian Book Distributors: https://www.christianbook.com/page/affiliate-program
- [ ] Church management software: Direct outreach

**Fitness Apps:**
- [ ] Amazon Associates (workout gear, supplements)
- [ ] iHerb: https://www.iherb.com/info/rewards (5-10%)
- [ ] Bodybuilding.com: https://www.bodybuilding.com/store/affiliates.htm (5-15%)
- [ ] Thorne: https://www.thorne.com/affiliates (15-25%)
- [ ] Athletic Greens: https://athleticgreens.com/pages/affiliate

**AI/Productivity Apps:**
- [ ] Impact: https://impact.com (SaaS network)
- [ ] PartnerStack: https://partnerstack.com (SaaS affiliate)

---

## PHASE 8: WHOP & SKOOL

### Whop Setup
- [ ] Go to: https://whop.com
- [ ] Create account
- [ ] Click "Create a Whop"
- [ ] Name your product/community
- [ ] Set pricing (one-time, recurring, or free)
- [ ] Add: Description, features, images
- [ ] Connect Stripe for payouts
- [ ] Share link

### Skool Setup
- [ ] Go to: https://skool.com
- [ ] Create account
- [ ] Click "Create Community"
- [ ] Name it, add description
- [ ] Set: Free or paid ($29-99/mo typical)
- [ ] Add welcome post
- [ ] Set up course modules (if applicable)
- [ ] Connect Stripe

---

## PHASE 9: ZERO-SOCIAL REVENUE (Cold Outreach)

### LinkedIn Sales Navigator
- [ ] Go to: https://www.linkedin.com/sales/
- [ ] Sign up: $80/mo Core or $135/mo Advanced
- [ ] Build lead lists by: Job title, company size, industry
- [ ] Save leads to lists
- [ ] Send 20-30 connection requests/day (no pitch)
- [ ] Follow up 24-48 hours after connection

**LinkedIn Connection Template:**
```
Hi [Name], noticed you're at [Company] working on [area].
Would love to connect.
```

**LinkedIn Follow-up (Day 2-3):**
```
Thanks for connecting [Name]. Quick question -
how's [Company] handling [problem you solve]?
```

### Cold Call VA Approach
- [ ] Hire VA from: OnlineJobs.ph or Upwork
- [ ] Cost: $300-500/month full-time
- [ ] VA tasks:
  - Build prospect lists in Apollo
  - Personalize email first lines
  - Send follow-ups
  - Log CRM data
  - Basic qualification

**VA Job Post Template:**
```
Title: Cold Email & Research VA - Remote

Looking for someone to:
- Build prospect lists using Apollo.io
- Research companies and find decision makers
- Personalize cold emails
- Track responses in spreadsheet
- Follow up with non-responders

Requirements:
- Fluent English
- Detail-oriented
- Available 40 hrs/week
- Experience with cold email preferred

Pay: $4-6/hour depending on experience
```

### Paid Ads (Quick Revenue)
**Google Ads:**
- [ ] Go to: https://ads.google.com
- [ ] Create campaign
- [ ] Target: Keywords related to your service
- [ ] Budget: Start $20-50/day
- [ ] Landing page required

**Meta Ads:**
- [ ] Go to: https://business.facebook.com
- [ ] Create Business Manager
- [ ] Add ad account
- [ ] Create campaign targeting your ICP
- [ ] Budget: Start $20-50/day

---

## MONTHLY COST SUMMARY

| Item | Cost | Notes |
|------|------|-------|
| Apple Developer | $8.25 | ($99/year) |
| Google Play | $2.08 | ($25 one-time, amortized) |
| Soax Proxies | $50-100 | Residential |
| Google Workspace | $18-36 | 3-6 inboxes |
| Cold Email Tool | $39-97 | Instantly/Smartlead |
| Apollo.io | $79 | Lead data |
| LinkedIn SalesNav | $80-135 | Optional |
| SMSPool | $5-10 | As needed |
| Domains | $20-30 | 4-5 domains |
| **TOTAL** | **$300-500/mo** | Without optional upgrades |

---

## QUICK REFERENCE: What Requires Human

**Can't Automate (Must Do Manually):**
- Account creation on any platform
- Payment/credit card entry
- 2FA setup
- App Store submissions
- Review responses
- Affiliate program applications
- VA hiring/management
- Strategy decisions

**Can Automate After Setup:**
- Email sending (after warmup)
- Social posting (after warmup)
- Lead list building
- Email follow-ups
- Analytics tracking
- Content scheduling

---

## PHASE TIMELINE

**This Week (Days 1-7):**
- [ ] Apple + Google developer accounts
- [ ] Buy domains
- [ ] Set up Cloudflare
- [ ] Create social accounts (manual)
- [ ] Start account warming

**Week 2:**
- [ ] Google Workspace setup
- [ ] DNS records (SPF/DKIM/DMARC)
- [ ] RevenueCat setup
- [ ] Continue account warming

**Week 3:**
- [ ] Cold email tool setup
- [ ] Apollo.io setup
- [ ] Start warmup on email domains
- [ ] Create first email sequences

**Week 4:**
- [ ] First cold email campaigns
- [ ] LinkedIn outreach
- [ ] Affiliate applications
- [ ] Consider VA hiring

**Month 2+:**
- [ ] Scale what's working
- [ ] Add paid ads if profitable
- [ ] Expand account network
- [ ] Optimize based on data

---

**This checklist is the ONLY manual setup doc needed. Everything else can be automated or done by Claude.**
