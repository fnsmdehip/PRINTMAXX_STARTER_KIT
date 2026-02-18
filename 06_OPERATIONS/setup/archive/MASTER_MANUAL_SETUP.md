# MASTER MANUAL SETUP - ALL PAYMENTS & ACCOUNTS

**One file. Every manual task. Direct URLs. Do these, then automation can take over.**

---

## TIER 1: BLOCKING - DO THESE FIRST ($125)

| # | Task | Cost | URL | Time |
|---|------|------|-----|------|
| 1 | Apple Developer | $99/yr | https://developer.apple.com/programs/enroll/ | 24-48h |
| 2 | Google Play Developer | $25 | https://play.google.com/console/signup | 24-48h |

**After approval:**
- App Store Connect: https://appstoreconnect.apple.com
- Play Console: https://play.google.com/console

---

## TIER 2: DOMAINS & DNS ($50-80)

| # | Task | Cost | URL |
|---|------|------|-----|
| 3 | Primary domain | $10-15/yr | https://porkbun.com |
| 4 | 3 cold email domains | $30-45/yr | https://porkbun.com |
| 5 | Cloudflare DNS (free) | $0 | https://cloudflare.com |

**Domain naming:**
- Main: printmaxx.io or similar
- Cold email: printmaxx-hq.com, printmaxx-mail.com, printmaxx-team.com

---

## TIER 3: EMAIL INFRASTRUCTURE ($18-36/mo)

| # | Task | Cost | URL |
|---|------|------|-----|
| 6 | Google Workspace | $6/user/mo | https://workspace.google.com |

**Create 2-3 inboxes per cold email domain:**
- sales@domain.com
- support@domain.com
- hello@domain.com

**DNS records (add in Cloudflare for EACH domain):**
```
SPF:   TXT  @       v=spf1 include:_spf.google.com ~all
DKIM:  TXT  google  (get from Google Admin console)
DMARC: TXT  _dmarc  v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

---

## TIER 4: MONETIZATION (Already have some)

| # | Task | Status | URL |
|---|------|--------|-----|
| 7 | Stripe | ✅ Have | https://stripe.com |
| 8 | RevenueCat | ✅ Have | https://app.revenuecat.com |
| 9 | Google Ads | ✅ Have | https://ads.google.com |

**RevenueCat setup steps:**
1. Create project → https://app.revenuecat.com
2. Add iOS app → connect App Store Connect API key
3. Add Android app → upload Play Console service account JSON
4. Create products (monthly $9.99, annual $49.99)
5. Create entitlement "premium"
6. Create offering "default"
7. Connect Stripe in Settings > Billing

---

## TIER 5: PROXIES & VERIFICATION ($60-110)

| # | Task | Cost | URL |
|---|------|------|-----|
| 10 | Soax proxies | $50+ | https://soax.com |
| 11 | SMSPool | $10-20 | https://smspool.net |

**Soax setup:**
- Select "Residential Proxies"
- For social media: Use sticky sessions (30 min)
- Credentials format: `user:pass@proxy.soax.com:port`

---

## TIER 6: VOICE/AUDIO ($22/mo)

| # | Task | Cost | URL |
|---|------|------|-----|
| 12 | ElevenLabs Creator | $22/mo | https://elevenlabs.io |

**After signup:**
- Get API key from profile
- Add to .env: `ELEVENLABS_API_KEY=xxx`

---

## TIER 7: COLD EMAIL TOOLS (Pick ONE) ($39-97/mo)

| Option | Cost | URL | Notes |
|--------|------|-----|-------|
| Instantly | $97/mo | https://instantly.ai | Easiest, recommended |
| Smartlead | $39/mo | https://smartlead.ai | Better analytics |
| DeliverOn | $49/mo | https://deliveron.org | Pre-warmed, skip warmup |

**Also get:**
| # | Task | Cost | URL |
|---|------|------|-----|
| 13 | Apollo.io | $79/mo | https://apollo.io |

---

## TIER 8: SOCIAL ACCOUNTS (Manual Creation)

### X/Twitter (4 accounts)
| Account | URL |
|---------|-----|
| @PRINTMAXXER (main) | https://x.com/i/flow/signup |
| AI niche | https://x.com/i/flow/signup |
| Faith niche | https://x.com/i/flow/signup |
| Fitness niche | https://x.com/i/flow/signup |

### TikTok (3 accounts)
| Account | URL |
|---------|-----|
| AI niche | https://www.tiktok.com/signup |
| Faith niche | https://www.tiktok.com/signup |
| Fitness niche | https://www.tiktok.com/signup |

### Instagram (3 accounts)
| Account | URL |
|---------|-----|
| AI niche | https://www.instagram.com/accounts/emailsignup/ |
| Faith niche | https://www.instagram.com/accounts/emailsignup/ |
| Fitness niche | https://www.instagram.com/accounts/emailsignup/ |

**After creating each:**
- Enable 2FA
- Complete profile fully
- NO posting for 3-5 days
- Manual engagement only first week

---

## TIER 9: AFFILIATE PROGRAMS (Apply manually)

| Program | URL | Commission |
|---------|-----|------------|
| Amazon Associates | https://affiliate-program.amazon.com | 4-8% |
| Athletic Greens | https://athleticgreens.com/pages/affiliate | varies |
| Thorne | https://www.thorne.com/affiliates | 15-25% |
| iHerb | https://www.iherb.com/info/rewards | 5-10% |
| Impact (SaaS) | https://impact.com | varies |
| PartnerStack | https://partnerstack.com | varies |

---

## TIER 10: COMMUNITY PLATFORMS (Optional)

| Platform | Cost | URL |
|----------|------|-----|
| Whop | Free + fees | https://whop.com |
| Skool | $99/mo | https://skool.com |
| Gumroad | Free + fees | https://gumroad.com |
| Beehiiv | Free tier | https://beehiiv.com |

---

## TIER 11: LINKEDIN (Optional) ($80-135/mo)

| Tool | Cost | URL |
|------|------|-----|
| Sales Navigator | $80-135/mo | https://www.linkedin.com/sales/ |
| Expandi | $99/mo | https://expandi.io |

---

## MONTHLY COST SUMMARY

| Category | Monthly |
|----------|---------|
| Developer accounts | ~$10 (amortized) |
| Domains | ~$5 (amortized) |
| Google Workspace | $18-36 |
| ElevenLabs | $22 |
| Cold email tool | $39-97 |
| Apollo.io | $79 |
| Soax | $50-100 |
| **TOTAL** | **$225-350/mo** |

---

## QUICK COPY: ALL PAYMENT URLS

```
# TIER 1 - BLOCKING
https://developer.apple.com/programs/enroll/
https://play.google.com/console/signup

# TIER 2 - DOMAINS
https://porkbun.com
https://cloudflare.com

# TIER 3 - EMAIL
https://workspace.google.com

# TIER 4 - MONETIZATION (already have)
https://stripe.com
https://app.revenuecat.com

# TIER 5 - PROXIES
https://soax.com
https://smspool.net

# TIER 6 - VOICE
https://elevenlabs.io

# TIER 7 - COLD EMAIL (pick one)
https://instantly.ai
https://smartlead.ai
https://deliveron.org
https://apollo.io

# TIER 8 - SOCIAL
https://x.com/i/flow/signup
https://www.tiktok.com/signup
https://www.instagram.com/accounts/emailsignup/

# TIER 9 - AFFILIATES
https://affiliate-program.amazon.com
https://athleticgreens.com/pages/affiliate
https://www.thorne.com/affiliates
https://impact.com
https://partnerstack.com

# TIER 10 - COMMUNITIES
https://whop.com
https://skool.com
https://gumroad.com
https://beehiiv.com

# TIER 11 - LINKEDIN
https://www.linkedin.com/sales/
https://expandi.io
```

---

## AFTER YOU COMPLETE SETUP

Once accounts are created, add credentials to `.env`:

```bash
# .env (DO NOT COMMIT)

# RevenueCat
REVENUECAT_API_KEY=
REVENUECAT_WEBHOOK_SECRET=

# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Apple (from App Store Connect)
APP_STORE_CONNECT_API_KEY=
APP_STORE_CONNECT_ISSUER_ID=
APP_STORE_CONNECT_KEY_ID=

# Google Play
GOOGLE_PLAY_SERVICE_ACCOUNT_JSON=path/to/json

# ElevenLabs
ELEVENLABS_API_KEY=

# Soax
SOAX_PROXY_USER=
SOAX_PROXY_PASS=
SOAX_PROXY_HOST=

# Apollo
APOLLO_API_KEY=

# Cold Email Tool
INSTANTLY_API_KEY=
```

Then I can automate everything else.

---

**Created:** 2026-01-26
**This is the ONLY manual setup file you need.**
