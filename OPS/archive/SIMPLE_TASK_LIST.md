# SIMPLE TASK LIST

**Do these in order. Check off as you go.**

---

## THIS WEEK (Days 1-7)

### Day 1-2: Developer Accounts
- [ ] Go to https://developer.apple.com/programs/enroll/ → Pay $99
- [ ] Go to https://play.google.com/console/signup → Pay $25
- [ ] Wait 24-48 hours for approval

### Day 2-3: Domains
- [ ] Go to https://porkbun.com → Buy main domain ($12)
- [ ] Buy 3 cold email domains ($36 total) - examples: yourname-hq.com, yourname-mail.com
- [ ] Go to https://cloudflare.com → Add all domains → Copy nameservers
- [ ] Go back to Porkbun → Update nameservers to Cloudflare's

### Day 3-4: Email Setup
- [ ] Go to https://workspace.google.com → Sign up with cold email domain
- [ ] Create 2-3 inboxes: sales@, hello@, yourname@
- [ ] In Cloudflare, add DNS records:
  - SPF: Type TXT, Name @, Value `v=spf1 include:_spf.google.com ~all`
  - DMARC: Type TXT, Name _dmarc, Value `v=DMARC1; p=none;`
- [ ] In Google Workspace Admin → Apps → Gmail → Authenticate Email → Generate DKIM → Add to Cloudflare

### Day 4-7: Social Accounts (Create + Start Warming)
- [ ] Create X/Twitter account (main brand)
- [ ] Create X/Twitter account (AI niche)
- [ ] Create X/Twitter account (Faith niche)
- [ ] Create X/Twitter account (Fitness niche)
- [ ] Enable 2FA on all
- [ ] DO NOT POST YET - just follow 20-30 accounts, like stuff, scroll

### Day 5-7: Proxies + Phone Verify
- [ ] Go to https://soax.com → Add $50 balance
- [ ] Go to https://smspool.net → Add $10 balance
- [ ] Create TikTok accounts (use SMSPool for phone verify)
- [ ] Create Instagram accounts
- [ ] Complete all profiles 100%

---

## WEEK 2 (Days 8-14)

### Monetization Setup
- [ ] Go to https://app.revenuecat.com → Create account → Create project
- [ ] Go to https://stripe.com → Create account → Connect to RevenueCat
- [ ] In App Store Connect: Create app entry for PrayerLock
- [ ] In App Store Connect: Create subscription products ($9.99/mo, $49.99/yr)

### Continue Warming
- [ ] X/Twitter: Start posting (3/day, text only, no links)
- [ ] X/Twitter: Reply to 10-20 posts daily
- [ ] TikTok: Watch 30 min content daily, post 1-2 videos
- [ ] Instagram: Post stories first, then feed posts

### Email Warmup Start
- [ ] Go to https://instantly.ai OR https://smartlead.ai → Sign up ($37-97/mo)
- [ ] Connect your cold email domains
- [ ] Enable auto-warmup feature
- [ ] Wait 14-21 days before sending cold emails

---

## WEEK 3 (Days 15-21)

### Lead Data
- [ ] Go to https://apollo.io → Sign up ($79/mo)
- [ ] Build first lead list: Filter by job title, company size, industry
- [ ] Export 500 leads
- [ ] Go to https://neverbounce.com → Verify emails → Only keep "valid" ones

### LinkedIn Setup
- [ ] Complete LinkedIn profile 100%
- [ ] Optional: https://linkedin.com/sales/ → Sales Navigator ($80/mo)
- [ ] Send 20-25 connection requests/day (NO pitch in request)
- [ ] Engage on 10 posts/day

### App Work
- [ ] Get PrayerLock icons generated (use Gemini)
- [ ] Test in iOS Simulator: `cd builds/prayerlock && npx expo start --ios`
- [ ] Fix any issues
- [ ] Take App Store screenshots

---

## WEEK 4 (Days 22-30)

### First Cold Email Campaign
- [ ] Check warmup status (should be 2+ weeks now)
- [ ] Create first email sequence (use templates in EMAIL_SEQUENCES.md)
- [ ] Start with 20-30 emails/day per inbox
- [ ] Track: Open rate (target 50%+), Reply rate (target 5%+)

### LinkedIn Outreach
- [ ] After connection accepted: Wait 24 hours
- [ ] Send personalized message (reference their profile/content)
- [ ] Follow up after 3-5 days if no response

### Social Scaling
- [ ] X/Twitter: Now posting 4x/day with links in bio
- [ ] TikTok: Post 2-3x/day
- [ ] Start cross-promoting between accounts

### App Submission
- [ ] Upload PrayerLock build to TestFlight
- [ ] Internal testing
- [ ] Submit for App Store review

---

## ONGOING (Weekly)

### Every Monday
- [ ] Check email deliverability (open rates, bounce rates)
- [ ] Review social analytics
- [ ] Plan content for the week

### Every Day
- [ ] 30 min social engagement (replies, likes)
- [ ] Check cold email responses
- [ ] LinkedIn: 20 connections + 10 post engagements

### Research (1 hour/week)
- [ ] Scan Twitter bookmarks for alpha
- [ ] Check r/coldemail, r/SocialMediaMarketing
- [ ] Run /daily-research in Claude

---

## COST TRACKER

| Item | One-Time | Monthly |
|------|----------|---------|
| Apple Developer | $99 | - |
| Google Play | $25 | - |
| Domains (4) | $48 | - |
| Soax Proxies | - | $50 |
| SMSPool | $10 | - |
| Google Workspace | - | $18 |
| Instantly/Smartlead | - | $37-97 |
| Apollo.io | - | $79 |
| LinkedIn SalesNav | - | $80 (optional) |
| **TOTAL** | **$182** | **$180-320/mo** |

---

## WHAT YOU DO vs WHAT CLAUDE DOES

### You (Human) Must Do:
- Create accounts (any platform)
- Enter payment info
- Set up 2FA
- App Store submissions
- Reply to reviews
- Strategy decisions

### Claude Can Do (After You Set Up):
- Write email sequences
- Generate content
- Build apps
- Create marketing assets
- Research competitors
- Optimize copy

---

## APP PRIORITY

1. **PrayerLock** - 85% done, needs icons + RevenueCat
2. **biomaxx-sdk54** - Ready to ship
3. **WalkToUnlock** - 35% done, needs native code
4. **StudyLock** - 40% done, needs native blocking

---

## QUICK LINKS

| What | Where |
|------|-------|
| Email sequences | `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES.md` |
| LinkedIn templates | `MONEY_METHODS/COLD_OUTBOUND/LINKEDIN_TEMPLATES.md` |
| Content calendar | `OPS/NICHE_ACCOUNT_CONTENT_CALENDAR.md` |
| Voice guide | `OPS/prompts/PIPELINEABUSER_VOICE_GUIDE.md` |
| Warmup guide | `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` |
| RevenueCat code | `MONEY_METHODS/APP_FACTORY/REVENUECAT_INTEGRATION_GUIDE.md` |
| Full detailed setup | `OPS/RETARDMAXX_MANUAL_SETUP_CHECKLIST.md` |

---

**Start at the top. Work down. Check boxes. Ship.**
