# Manual Foundational Stack

**Everything you must sign up for, pay for, and configure manually.**

Ralph can't do these. You must.

---

## Quick Summary

| Category | Monthly Cost | One-Time Cost | Priority |
|----------|-------------|---------------|----------|
| Dev Accounts | ~$10/mo | $124 | CRITICAL |
| AI/Coding | $200/mo | $0 | HAVE |
| Proxies | $50-99/mo | $0 | HIGH |
| Hosting | $5-20/mo | $0 | MEDIUM |
| Email | $0-50/mo | $0 | MEDIUM |
| Payments | 2.9% + fees | $0 | HAVE |
| **TOTAL** | ~$265-380/mo | ~$124 | - |

---

## TIER 1: CRITICAL (Do First)

### Apple Developer Program
- **Cost:** $99/year (~$8.25/mo)
- **URL:** https://developer.apple.com/programs/
- **Time:** 24-48h approval (sometimes instant)
- **Needed for:** App Store submission, TestFlight

**Setup steps:**
1. Sign in with Apple ID
2. Enroll as Individual or Organization
3. Pay $99
4. Wait for approval email
5. Accept agreements in App Store Connect

**Watch out for:**
- May require video call verification
- Use business-sounding Apple ID if possible
- Don't use VPN during enrollment

### Google Play Developer
- **Cost:** $25 one-time
- **URL:** https://play.google.com/console/signup
- **Time:** Instant to 48h
- **Needed for:** Play Store submission

**Setup steps:**
1. Sign in with Google account
2. Pay $25 registration fee
3. Complete developer profile
4. Verify identity (may require ID upload)

### RevenueCat (Subscriptions)
- **Cost:** FREE up to $2.5k MRR, then 1%
- **URL:** https://www.revenuecat.com
- **Status:** YOU HAVE THIS
- **Needed for:** In-app purchases, subscription management

**Setup per app:**
1. Create new project
2. Add iOS app (bundle ID: com.printmaxx.[appname])
3. Add Android app (package: com.printmaxx.[appname])
4. Create entitlement: "premium"
5. Create offering: "default"
6. Create products:
   - [appname]_monthly_999 ($9.99/mo)
   - [appname]_annual_4999 ($49.99/yr)
7. Connect to App Store Connect (shared secret)
8. Connect to Play Console (service account JSON)
9. Test with sandbox

### Stripe (Payments)
- **Cost:** 2.9% + $0.30 per transaction
- **URL:** https://stripe.com
- **Status:** YOU HAVE THIS
- **Needed for:** Payment processing, RevenueCat integration

**Setup:**
1. Connect Stripe to RevenueCat
2. Set up webhook endpoints
3. Configure tax settings
4. Add bank account for payouts

---

## TIER 2: HIGH PRIORITY (Do This Week)

### Mobile Proxies (for Instagram/TikTok automation)
- **Cost:** $50-99/mo
- **Options:**
  - **Soax:** $99/mo - https://soax.com (recommended for mobile)
  - **Decodo:** $50/mo - https://app.decodo.com (good for residential)
- **Needed for:** Multi-account safety, automation without bans

**Setup:**
1. Create account
2. Choose mobile proxy plan
3. Get SOCKS5 credentials
4. Test with proxy_tester.py script
5. Add to .env file

### GoLogin (Anti-detect browser)
- **Cost:** FREE tier (3 profiles), $49/mo (100 profiles)
- **URL:** https://gologin.com
- **Needed for:** Separate browser fingerprints per account

**Setup:**
1. Download desktop app
2. Create profile for each niche (3 minimum)
3. Assign proxies to profiles
4. Import cookies after manual login

### SMSPool (Phone verification)
- **Cost:** $5-20 one-time (pay as you go)
- **URL:** https://smspool.net
- **Needed for:** Account verification without burning real numbers

**Setup:**
1. Create account
2. Add $10-20 balance
3. Use for TikTok/Instagram verification
4. Track which numbers used for which accounts

### ProtonMail (Secure email)
- **Cost:** FREE (or $4/mo for custom domain)
- **URL:** https://proton.me
- **Needed for:** Email addresses per niche

**Create these accounts:**
1. printmaxxer@proton.me - Meta brand
2. aiworkflows@proton.me - AI niche
3. dailyanchor@proton.me - Faith niche
4. fitphysique@proton.me - Fitness niche

---

## TIER 3: MEDIUM PRIORITY (Do This Month)

### Vercel (Hosting)
- **Cost:** FREE tier, $20/mo pro
- **URL:** https://vercel.com
- **Needed for:** Landing pages, Next.js site

**Setup:**
1. Connect GitHub repo
2. Deploy LANDING/printmaxx-site
3. Add custom domain when ready

### Cloudflare (DNS + CDN)
- **Cost:** FREE tier
- **URL:** https://cloudflare.com
- **Needed for:** Domain management, SSL, protection

### Namecheap/Porkbun (Domains)
- **Cost:** $10-15/year per domain
- **URL:** https://namecheap.com or https://porkbun.com
- **Needed for:** App websites, email domains

**Domains to consider:**
- focusprayer.app
- stepunlock.app
- learnlock.app
- dailyanchor.app
- pelvicpro.app
- promptvault.app
- devotionflow.app
- printmaxx.io (meta brand)

### Hetzner (VPS for automation)
- **Cost:** €5-10/mo
- **URL:** https://hetzner.com/cloud
- **Needed for:** n8n, scheduled tasks, Playwright runners

**Setup:**
1. Create CX21 instance (2 vCPU, 4GB RAM)
2. Ubuntu 22.04
3. Install Docker
4. Run n8n for automation workflows

---

## TIER 4: WHEN SCALING

### Email Marketing
- **ConvertKit:** FREE up to 1k subs - https://convertkit.com
- **Beehiiv:** FREE up to 2.5k subs - https://beehiiv.com
- **Needed for:** Welcome sequences, nurture campaigns

### Cold Email (If doing outreach)
- **Instantly:** $37/mo - https://instantly.ai
- **Smartlead:** $39/mo - https://smartlead.ai
- **Needed for:** Cold outreach at scale
- **Note:** Use separate domain, not your main

### Analytics
- **Mixpanel:** FREE up to 20M events - https://mixpanel.com
- **PostHog:** FREE self-hosted - https://posthog.com
- **Needed for:** App analytics, funnel tracking

### AdMob (In-app ads)
- **Cost:** FREE (you earn from ads)
- **URL:** https://admob.google.com
- **Needed for:** Free tier monetization

**Setup per app:**
1. Create app in AdMob
2. Create ad units (banner, interstitial, rewarded)
3. Copy ad unit IDs to app config
4. Implement ads in free tier only

---

## SOCIAL ACCOUNTS (Manual Creation Required)

### Per Niche (12 accounts total)

**AI/Productivity Niche:**
- [ ] X/Twitter: @aiworkflowsdaily
- [ ] TikTok: @aiworkflowsdaily
- [ ] Instagram: @aiworkflowsdaily
- [ ] YouTube: AI Workflows Daily

**Faith Niche:**
- [ ] X/Twitter: @dailyanchorfaith
- [ ] TikTok: @dailyanchorfaith
- [ ] Instagram: @dailyanchorfaith
- [ ] YouTube: Daily Anchor Faith

**Fitness Niche:**
- [ ] X/Twitter: @threehourphysique
- [ ] TikTok: @threehourphysique
- [ ] Instagram: @threehourphysique
- [ ] YouTube: 3-Hour Physique

**Meta Brand:**
- [ ] X/Twitter: @PRINTMAXXER

### Account Creation Rules
1. Use GoLogin with proxy per account
2. Use SMSPool for phone verification
3. Don't link accounts to each other
4. Complete profile before any activity
5. Warmup 5-7 days before posting

---

## WHAT YOU ALREADY HAVE

Based on your setup:
- [x] Claude Max ($200/mo)
- [x] RevenueCat account
- [x] Stripe account
- [x] Google Ads account (for future paid ads)
- [x] DigitalOcean droplet (or considering Hetzner)

---

## IMMEDIATE ACTION CHECKLIST

### Today (30 min)
- [ ] Verify Apple Developer account status
- [ ] Verify Google Play Developer account status
- [ ] Sign up for Soax or Decodo proxies ($50-99)
- [ ] Sign up for GoLogin (free tier)
- [ ] Create SMSPool account, add $10

### This Week (2-3 hours)
- [ ] Create 4 ProtonMail accounts
- [ ] Create first social accounts (start with X/Twitter)
- [ ] Configure RevenueCat for first app (StepUnlock)
- [ ] Create app in App Store Connect
- [ ] Create app in Play Console
- [ ] Start warmup protocol on social accounts

### Before First App Launch
- [ ] Privacy policy page live
- [ ] Terms of service page live
- [ ] Support email configured
- [ ] App icon finalized
- [ ] Screenshots ready
- [ ] App Store listing complete
- [ ] RevenueCat products linked
- [ ] Test purchase flow in sandbox

---

## BUDGET BREAKDOWN

### Minimum Viable Stack (~$265/mo)
| Service | Cost |
|---------|------|
| Claude Max | $200/mo |
| Apple Developer | $8.25/mo |
| Decodo Proxies | $50/mo |
| Hetzner VPS | €5/mo |
| **Total** | ~$265/mo |

### Recommended Stack (~$380/mo)
| Service | Cost |
|---------|------|
| Claude Max | $200/mo |
| Apple Developer | $8.25/mo |
| Soax Mobile Proxies | $99/mo |
| GoLogin Pro | $49/mo |
| Hetzner VPS | €10/mo |
| ConvertKit | $0 (free tier) |
| **Total** | ~$380/mo |

### One-Time Costs
| Service | Cost |
|---------|------|
| Google Play Developer | $25 |
| SMSPool balance | $10-20 |
| Domains (x3) | $30-45 |
| **Total** | ~$65-90 |

---

## ENV VARIABLES TEMPLATE

When ready to configure, add these to `.env`:

```bash
# Apple (get from App Store Connect)
APP_STORE_CONNECT_API_KEY=
APP_STORE_CONNECT_ISSUER_ID=
APP_STORE_CONNECT_KEY_ID=

# Google (service account JSON path)
GOOGLE_PLAY_SERVICE_ACCOUNT=./keys/play-service-account.json

# RevenueCat
REVENUECAT_API_KEY_IOS=
REVENUECAT_API_KEY_ANDROID=
REVENUECAT_WEBHOOK_SECRET=

# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Proxies (Soax example)
SOAX_PROXY_HOST=proxy.soax.com
SOAX_PROXY_PORT=9000
SOAX_PROXY_USER=
SOAX_PROXY_PASS=

# Analytics (when ready)
MIXPANEL_TOKEN=
POSTHOG_API_KEY=

# AdMob (per app)
ADMOB_APP_ID_IOS=
ADMOB_BANNER_ID=
ADMOB_INTERSTITIAL_ID=
ADMOB_REWARDED_ID=
```

---

## ACCOUNT PROTECTION STRATEGY

### App Store Account Safety
1. **Don't submit all 7 apps from same account**
   - Use 2-3 developer accounts
   - Different payment methods per account
   - Different addresses if possible

2. **Submission order (safest first)**
   - Week 1: DailyAnchor (most differentiated)
   - Week 2: PromptVault (unique utility)
   - Week 3: StepUnlock (fitness angle)
   - Week 4+: Others

3. **What triggers bans**
   - Multiple rejections in short time
   - Misleading app descriptions
   - Hidden functionality
   - Fake reviews/ratings
   - Duplicate apps (same code, different names)

### Social Account Safety
1. Use unique proxy per account
2. Unique browser fingerprint (GoLogin)
3. Don't cross-link accounts
4. Warmup 5-7 days minimum
5. Gradual activity increase

---

## QUICK REFERENCE LINKS

| Service | URL |
|---------|-----|
| Apple Developer | https://developer.apple.com/programs/ |
| App Store Connect | https://appstoreconnect.apple.com |
| Google Play Console | https://play.google.com/console |
| RevenueCat | https://app.revenuecat.com |
| Stripe | https://dashboard.stripe.com |
| Soax | https://soax.com |
| Decodo | https://app.decodo.com |
| GoLogin | https://gologin.com |
| SMSPool | https://smspool.net |
| Hetzner | https://hetzner.com/cloud |
| Vercel | https://vercel.com |
| Cloudflare | https://cloudflare.com |
| Namecheap | https://namecheap.com |
| ConvertKit | https://convertkit.com |
| Mixpanel | https://mixpanel.com |
| AdMob | https://admob.google.com |

---

**Created:** 2026-01-21
**Status:** Ready for execution
