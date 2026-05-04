# Tech Stack Foundation

Everything that needs to be set up BEFORE launching apps/social. Do these first.

---

## User's current state

**Already have:**
- [x] Apple Developer account (active)
- [x] RevenueCat account
- [x] Stripe account
- [x] Google Mobile Ads account (iOS)
- [ ] Google Play Developer (skipping for now, low Android revenue)

**Need to do:**
- [ ] Link RevenueCat to Stripe
- [ ] Set up social infrastructure
- [ ] Configure proxies for automation

---

## Phase 1: Payment infrastructure (DO FIRST)

### RevenueCat + Stripe linking

**Manual steps (you do):**
1. Log into RevenueCat dashboard
2. Go to Project Settings → Integrations
3. Add Stripe integration
4. Copy Stripe webhook URL from RevenueCat
5. In Stripe Dashboard → Webhooks → Add endpoint
6. Paste RevenueCat URL
7. Select events: all checkout and subscription events
8. Copy signing secret back to RevenueCat

**Test:**
- Create test product in RevenueCat
- Make sandbox purchase
- Verify shows in both dashboards

### RevenueCat app setup (per app)

For each app (PrayerLock, WalkToUnlock, etc.):
1. Create new app in RevenueCat
2. Add iOS platform (skip Android for now)
3. Connect to App Store Connect
4. Create entitlements (e.g., "premium")
5. Create offerings (e.g., "default")
6. Create products:
   - monthly_999 ($9.99/mo)
   - annual_4999 ($49.99/yr)
7. Link products to App Store Connect products

---

## Phase 2: Social infrastructure

### Domain setup

**Per brand/app:**
- [ ] Purchase domain (Cloudflare or Namecheap)
- [ ] Set up DNS
- [ ] Create email (support@appname.com)
- [ ] Deploy landing page (Vercel)

**Recommended domains:**
- prayerlock.app or getprayerlock.com
- walktounlock.app or getwalktounlock.com

### Social accounts (manual creation required)

**For each app, create:**

| Platform | Handle | Email | Phone needed |
|----------|--------|-------|--------------|
| TikTok | @prayerlock | support@prayerlock.app | Yes |
| Instagram | @prayerlock | support@prayerlock.app | Yes |
| X/Twitter | @prayerlock | support@prayerlock.app | No |
| YouTube | PrayerLock | support@prayerlock.app | No |

**Account creation tips:**
- Use different phone numbers if possible (Google Voice works for some)
- Complete profile fully before any automation
- Post 5-10 manual posts before any automation
- Wait 7-14 days before automating (see ACCOUNT_WARMING_SOP.md)

### Proxy setup

**For IG/TikTok automation (required):**
1. Sign up for Soax ($99/mo mobile plan)
2. Get mobile proxy credentials
3. Add to .env file
4. Test with proxy_tester.py

**Proxy config:**
```bash
# .env
SOAX_MOBILE_HOST=gate.soax.com
SOAX_MOBILE_PORT=9000
SOAX_MOBILE_USER=your_user
SOAX_MOBILE_PASS=your_pass
```

---

## Phase 3: Email infrastructure

### Cold email (for outreach)

**Don't use main domain for cold email.** Buy separate domain.

**Setup:**
1. Buy domain (e.g., prayerlock-team.com)
2. Set up Google Workspace or Zoho
3. Configure SPF, DKIM, DMARC
4. Warm up for 2-4 weeks before sending
5. Connect to Instantly or Smartlead

### Transactional email (for apps)

**Options:**
- Resend (free tier, easy)
- SendGrid (free tier)
- Postmark (best deliverability)

**Setup:**
1. Create account
2. Verify domain
3. Get API key
4. Add to app .env

### Newsletter (for nurture)

**Options:**
- ConvertKit (creator-focused)
- Beehiiv (newsletter-first)
- Buttondown (simple)

**Setup:**
1. Create account
2. Import any existing emails
3. Set up welcome sequence
4. Create landing page form

---

## Phase 4: Analytics infrastructure

### App analytics

**RevenueCat handles:**
- Revenue metrics
- Subscription status
- Trial conversion

**Add for behavior:**
- Mixpanel (free tier) or Amplitude
- PostHog (open source option)

**Setup:**
1. Create project
2. Get API key
3. Add SDK to apps
4. Define key events:
   - app_open
   - onboarding_complete
   - feature_used
   - paywall_shown
   - trial_started
   - purchase_complete

### Web analytics

- Plausible (privacy-focused, $9/mo)
- PostHog (free, open source)
- Or just Google Analytics

### Social analytics

Built into platforms, but also:
- Social Blade for tracking growth
- Export data to LEDGER/SOCIAL_METRICS.csv

---

## Phase 5: Automation infrastructure

### Playwright setup

```bash
# Install
pip install playwright
playwright install chromium

# Test
python AUTOMATIONS/scripts/proxy_tester.py
```

### Session management

After manual login to social accounts:
1. Export browser storage state
2. Save to AUTOMATIONS/sessions/
3. Scripts will use saved sessions

**Never automate before:**
- Account is 7+ days old
- 10+ manual posts made
- Proxy is tested and working

---

## Dependency order

```
1. RevenueCat ↔ Stripe (before any app)
   ↓
2. Domains + landing pages (before social)
   ↓
3. Social accounts (manual creation)
   ↓
4. Email infrastructure
   ↓
5. Proxy setup (before automation)
   ↓
6. Analytics (before launch)
   ↓
7. Account warming (7-14 days)
   ↓
8. Launch apps + automation
```

---

## Checklist summary

### Before building apps
- [x] Apple Developer account
- [ ] RevenueCat linked to Stripe
- [ ] Test subscription flow works

### Before social automation
- [ ] Domains purchased
- [ ] Social accounts created (manual)
- [ ] Proxies purchased and tested
- [ ] Accounts warmed (7-14 days)

### Before launch
- [ ] Landing pages live
- [ ] Email infrastructure ready
- [ ] Analytics configured
- [ ] Content queue populated

---

## Quick actions for you now

1. **Today:** Link RevenueCat to Stripe (15 min)
2. **Today:** Purchase Soax mobile proxy ($99)
3. **Today:** Buy domains for first 2 apps
4. **This week:** Create social accounts (manual)
5. **This week:** Start warming accounts with manual posts

While you do that, Ralph can build the apps in parallel.

---

Created: 2026-01-21
