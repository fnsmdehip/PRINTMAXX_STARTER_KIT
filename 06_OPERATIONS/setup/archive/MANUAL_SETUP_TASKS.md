# Manual Setup Tasks

Things only YOU can do. Ralph can't touch these.

---

## Accounts you already have

Based on previous conversation:
- [x] RevenueCat account
- [x] Stripe account
- [x] Google Ads account
- [x] DigitalOcean droplet (considering Hetzner)

---

## One-time setup (do once)

### Developer accounts

| Task | Cost | Time | Priority |
|------|------|------|----------|
| [ ] Apple Developer Program | $99/year | 24-48h approval | HIGH |
| [ ] Google Play Developer | $25 one-time | Instant | HIGH |
| [ ] Apple App Store Connect setup | Free | 30 min | HIGH |
| [ ] Google Play Console setup | Free | 30 min | HIGH |

**Notes:**
- Apple sometimes requires video call verification for new accounts
- Use business email, not personal Gmail
- Consider separate LLC for app publishing

### Payment processing

| Task | Status | Notes |
|------|--------|-------|
| [ ] Stripe connected to RevenueCat | You have Stripe | Link accounts |
| [ ] RevenueCat app configured | You have RevenueCat | Create app entry |
| [ ] Test subscription flow | - | Use sandbox mode |

**RevenueCat setup:**
1. Log into RevenueCat
2. Create new app
3. Add iOS + Android platforms
4. Connect to App Store Connect / Play Console
5. Set up products/offerings
6. Test with sandbox accounts

### Domain/hosting

| Task | Status | Notes |
|------|--------|-------|
| [ ] Domain for each app | - | Use Cloudflare or Namecheap |
| [ ] Vercel account | - | For landing pages (free tier) |
| [ ] Privacy policy generator | - | termly.io or iubenda |

### Social accounts (per app)

| Platform | Required info | Notes |
|----------|---------------|-------|
| TikTok | Phone number | Can't automate signup |
| Instagram | Phone/email | Need to verify |
| X/Twitter | Email | Can batch create |
| YouTube | Google account | For video content |

**For PrayerLock:**
- [ ] @prayerlock TikTok
- [ ] @prayerlock Instagram
- [ ] @prayerlock X/Twitter

**For WalkToUnlock:**
- [ ] @walktounlock TikTok
- [ ] @walktounlock Instagram
- [ ] @walktounlock X/Twitter

### Email infrastructure

| Task | Notes |
|------|-------|
| [ ] Domain for cold email (not main domain) | Protect main domain reputation |
| [ ] Instantly/Smartlead account | For cold outreach |
| [ ] ConvertKit/Beehiiv for newsletters | For nurture sequences |
| [ ] SPF/DKIM/DMARC setup | Critical for deliverability |

### Proxy setup (for automation)

| Task | Budget | Notes |
|------|--------|-------|
| [ ] Soax account | $99/mo for mobile | Required for IG/TikTok automation |
| [ ] Or Decodo account | $110/mo | Alternative |
| [ ] Test proxy connectivity | - | Run proxy_tester.py |

---

## Per-app manual tasks

When launching each app, you must manually:

### App Store submission

| Task | Notes |
|------|-------|
| [ ] Create app in App Store Connect | Can't automate |
| [ ] Create app in Google Play Console | Can't automate |
| [ ] Add screenshots (Ralph can generate) | Manual upload |
| [ ] Submit for review | Manual button click |
| [ ] Respond to rejection (if any) | Manual |

### RevenueCat products

| Task | Notes |
|------|-------|
| [ ] Create products in App Store Connect | Manual |
| [ ] Create products in Google Play Console | Manual |
| [ ] Link products in RevenueCat | Manual |
| [ ] Test purchase flow | Manual with sandbox |

### Affiliate setup

| Task | Notes |
|------|-------|
| [ ] Join affiliate networks | Manual application |
| [ ] Apply for specific programs | Manual |
| [ ] Get affiliate links | Manual |
| [ ] Add links to app/content | Ralph can help |

---

## Ongoing manual tasks

### Daily (5 min)

- [ ] Check crash reports
- [ ] Respond to app reviews
- [ ] Approve/reject affiliate applications

### Weekly (30 min)

- [ ] Review revenue dashboard
- [ ] Approve content queue (if human-in-loop)
- [ ] Check ad performance
- [ ] Review ALPHA_STAGING.csv for new tactics

### Monthly (1 hour)

- [ ] Review full metrics
- [ ] Update pricing if needed
- [ ] Pay affiliates
- [ ] Tax/accounting review

---

## Environment variables to set up

When ready to enable automation, set these:

```bash
# .env file (DO NOT COMMIT)

# RevenueCat
REVENUECAT_API_KEY=your_key
REVENUECAT_WEBHOOK_SECRET=your_secret

# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Apple
APP_STORE_CONNECT_API_KEY=xxx
APP_STORE_CONNECT_ISSUER_ID=xxx
APP_STORE_CONNECT_KEY_ID=xxx

# Google
GOOGLE_PLAY_SERVICE_ACCOUNT_JSON=path/to/json

# Proxies
SOAX_PROXY_USER=xxx
SOAX_PROXY_PASS=xxx
SOAX_PROXY_HOST=xxx

# Social (when ready)
# IG_SESSION_TOKEN=xxx
# TIKTOK_SESSION_TOKEN=xxx
# X_SESSION_TOKEN=xxx
```

**Important:** Don't add passwords yet. When ready to automate login-requiring tasks, you'll add session tokens (not passwords) after manual login.

---

## Automation readiness levels

### Level 1: Manual everything (NOW)
- You do: Everything
- Ralph does: Content generation, code, docs

### Level 2: Semi-automated (SOON)
- You do: Account setup, approval, payments
- Ralph does: Content, posting with your approval, analytics

### Level 3: Mostly automated (LATER)
- You do: Weekly review, final approvals
- Ralph does: Everything else with guardrails

### Level 4: Full Ralph loop (GOAL)
- You do: Set strategy, review results
- Ralph does: Build, test, submit, market, iterate

---

## Next manual actions for you

### This week

1. [ ] Verify Apple Developer account is active
2. [ ] Verify Google Play Developer account is active
3. [ ] Set up RevenueCat with your Stripe
4. [ ] Create TikTok account for first app
5. [ ] Create Instagram account for first app
6. [ ] Purchase Soax mobile proxy plan

### Before first app launch

1. [ ] Create app in App Store Connect
2. [ ] Create app in Google Play Console
3. [ ] Configure RevenueCat products
4. [ ] Test subscription flow
5. [ ] Submit privacy policy URL
6. [ ] Submit support URL

### When ready to scale automation

1. [ ] Export session tokens from logged-in browsers
2. [ ] Add to .env file
3. [ ] Test automation scripts with small batch
4. [ ] Monitor for account warnings
5. [ ] Scale gradually

---

## Contact points for issues

### Apple
- App Store Connect Resolution Center (in-app)
- developer.apple.com/contact

### Google
- Play Console Help
- support.google.com/googleplay/android-developer

### RevenueCat
- support@revenuecat.com
- docs.revenuecat.com

### Stripe
- dashboard.stripe.com/support
- stripe.com/docs

---

Created: 2026-01-21
