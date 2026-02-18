# YOUR MANUAL TASKS

Things only YOU can do. I can't touch payments, credentials, or account creation.

---

## PRIORITY 0: CRITICAL BLOCKER (Do TODAY)

### FamilyControls API (Apple) - 1-4 WEEK WAIT

**This is the longest lead time item. Start immediately.**

Required for: PrayerLock, WalkToUnlock, StudyLock (any app that blocks other apps)

- [ ] Apply at: https://developer.apple.com/contact/request/family-controls-distribution
- [ ] Write business justification (why your app needs Screen Time access)
- [ ] Provide privacy policy URL
- [ ] Wait 1-4 weeks for approval
- [ ] DO NOT submit blocker apps until approved

**If your apps DON'T block other apps** (just track habits without blocking), skip this.

---

## PRIORITY 1: Accounts (Do This Week)

### Developer Accounts
- [ ] **Apple Developer Program** - $99/year - developer.apple.com
  - Required for: All iOS apps
  - Takes 24-48h approval
  - Video call verification sometimes required

- [ ] **Google Play Console** - $25 one-time - play.google.com/console
  - Required for: All Android apps
  - Instant approval

### Payment Setup
- [x] Stripe account (you have this)
- [x] RevenueCat account (you have this)
- [ ] **Connect Stripe to RevenueCat** - revenuecat.com dashboard
- [ ] **Create RevenueCat apps** for PrayerLock, WalkToUnlock, StudyLock
- [ ] **Set up subscription products** in RevenueCat:
  - Monthly: $9.99
  - Annual: $79.99 (or per-app pricing)

### Domains
- [ ] **printmaxx.io** or similar main domain
- [ ] **prayerlock.app** (or .com)
- [ ] **walktounlock.app** (or .com)
- [ ] **studylock.app** (or .com)
- [ ] 3-5 cold email domains (~$10 each, different registrars)

---

## PRIORITY 2: Social Accounts (Create Manually)

### PRINTMAXX Brand
- [ ] @printmaxxer on X
- [ ] @printmaxxer on TikTok
- [ ] @printmaxxer on Instagram

### PrayerLock
- [ ] @prayerlock on X
- [ ] @prayerlock on TikTok
- [ ] @prayerlock on Instagram

### WalkToUnlock
- [ ] @walktounlock on X
- [ ] @walktounlock on TikTok
- [ ] @walktounlock on Instagram

### StudyLock
- [ ] @studylock on X
- [ ] @studylock on TikTok
- [ ] @studylock on Instagram

**After creation:**
- [ ] Enable 2FA on all accounts
- [ ] Save backup codes in password manager
- [ ] Complete all profile fields
- [ ] Follow 10-20 relevant accounts per niche

---

## PRIORITY 3: Infrastructure

### Proxies (Required for Automation)
- [ ] **Soax account** - $99/mo minimum - soax.com
  - OR Decodo/Smartproxy $75-110/mo
  - Required for: Instagram/TikTok automation
  - Mobile proxies, not datacenter

### Cold Email
- [ ] **Instantly.ai** - $37-97/mo (easiest)
  - OR Smartlead $39/mo
  - OR Emailbison $39/mo
- [ ] **Set up warmup** (2-3 weeks before sending)

### Email Infrastructure
- [ ] Google Workspace OR Outlook for cold domains ($6/user/mo)
- [ ] 3 inboxes per domain minimum
- [ ] SPF/DKIM/DMARC configured

### Hosting
- [x] DigitalOcean droplet (you have this)
- [ ] **Vercel** for landing pages (free tier)
  - Connect GitHub repo
  - Deploy LANDING/printmaxx-site

---

## PRIORITY 4: Before Each App Launch

### App Store Connect (iOS)
- [ ] Create app in App Store Connect
- [ ] Add screenshots (I can generate these)
- [ ] Add privacy policy URL
- [ ] Add support URL
- [ ] Submit for review (manual button click)

### Google Play Console (Android)
- [ ] Create app in Google Play Console
- [ ] Add screenshots
- [ ] Add privacy policy URL
- [ ] Submit for review

### RevenueCat (Per App)
- [ ] Create products in App Store Connect
- [ ] Create products in Google Play Console
- [ ] Link products in RevenueCat
- [ ] Test purchase flow with sandbox

---

## PRIORITY 5: FamilyControls API (For Blocker Apps)

Required for: PrayerLock, WalkToUnlock, StudyLock (any app that blocks other apps)

- [ ] Apply at: developer.apple.com/contact/request/family-controls-distribution
- Takes: 1-4 weeks for approval
- Required: Business justification, app description

**Do this ASAP - it's the longest lead time item**

---

## Environment Variables (When Ready)

Create `.env` file with (DO NOT COMMIT):

```bash
# RevenueCat
REVENUECAT_API_KEY=your_key
REVENUECAT_WEBHOOK_SECRET=your_secret

# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Apple (for automated builds)
APP_STORE_CONNECT_API_KEY=xxx
APP_STORE_CONNECT_ISSUER_ID=xxx
APP_STORE_CONNECT_KEY_ID=xxx

# Google (for automated builds)
GOOGLE_PLAY_SERVICE_ACCOUNT_JSON=path/to/json

# Proxies
SOAX_PROXY_USER=xxx
SOAX_PROXY_PASS=xxx
SOAX_PROXY_HOST=xxx
```

---

## Ongoing Tasks (After Setup)

### Daily (5 min)
- Check crash reports
- Respond to app reviews
- Monitor social engagement

### Weekly (30 min)
- Review revenue dashboard
- Check ad performance
- Review ALPHA_STAGING.csv

### Monthly (1 hour)
- Full metrics review
- Update pricing if needed
- Tax/accounting review

---

## What I'm Doing While You Handle This

1. Building apps in simulator
2. Running ralph loops for content
3. Generating more marketing materials
4. Building landing pages
5. Creating Remotion brand videos
6. Implementing high-priority alpha

---

**START WITH:**
1. Apple Developer Program signup
2. FamilyControls API application (longest wait)
3. Social account creation

Everything else can wait until those are in progress.
