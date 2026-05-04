# HUMAN INFRASTRUCTURE CHECKLIST

**Purpose:** Manual tasks only YOU can do to set up tech foundation. Claude checks this at session start.

**Status Key:** ⬜ = Not started | 🟡 = In progress | ✅ = Done

---

## TIER 1: BLOCKING (Can't build without these)

### Developer Accounts
- ⬜ Apple Developer ($99) → https://developer.apple.com/programs/enroll/
- ⬜ Google Play ($25) → https://play.google.com/console/signup

### Domains
- ⬜ Primary domain purchased → https://porkbun.com
- ⬜ 3 cold email domains purchased
- ⬜ All domains added to Cloudflare → https://cloudflare.com
- ⬜ Nameservers updated at registrar

### Email Infrastructure
- ⬜ Google Workspace account created → https://workspace.google.com
- ⬜ 2-3 inboxes created per cold email domain
- ⬜ SPF record added (per domain)
- ⬜ DKIM record added (per domain)
- ⬜ DMARC record added (per domain)

### Monetization
- ⬜ RevenueCat account created → https://app.revenuecat.com
- ⬜ Stripe account created → https://stripe.com
- ⬜ RevenueCat connected to Stripe
- ⬜ App Store Connect API key generated + added to RevenueCat
- ⬜ Play Console service account created + added to RevenueCat

---

## TIER 2: ACCOUNTS (Need for distribution)

### Social Accounts Created
- ⬜ X/Twitter: @PRINTMAXXER (main)
- ⬜ X/Twitter: AI niche account
- ⬜ X/Twitter: Faith niche account
- ⬜ X/Twitter: Fitness niche account
- ⬜ TikTok: AI niche
- ⬜ TikTok: Faith niche
- ⬜ TikTok: Fitness niche
- ⬜ Instagram: AI niche
- ⬜ Instagram: Faith niche
- ⬜ Instagram: Fitness niche

### 2FA Enabled
- ⬜ All X/Twitter accounts
- ⬜ All TikTok accounts
- ⬜ All Instagram accounts
- ⬜ Google Workspace
- ⬜ RevenueCat
- ⬜ Stripe

### Proxies & Verification
- ⬜ Soax account created + $50 balance → https://soax.com
- ⬜ SMSPool account created + $10 balance → https://smspool.net

### Voice/Audio Production
- ⬜ ElevenLabs account created → https://elevenlabs.io
- ⬜ ElevenLabs Creator plan ($22/mo) subscribed
- ⬜ API key added to .env (ELEVENLABS_API_KEY)
- ⬜ Voice presets configured per niche (see OPS/ELEVENLABS_MCP_INTEGRATION.md)

---

## TIER 3: TOOLS (Need for outbound)

### Cold Email Tool (Pick One)
- ⬜ Instantly.ai ($37-97/mo) → https://instantly.ai
- ⬜ OR Smartlead ($39/mo) → https://smartlead.ai
- ⬜ OR DeliverOn ($49/mo, pre-warmed) → https://deliveron.org
- ⬜ Cold email domains connected
- ⬜ Auto-warmup enabled

### Lead Data
- ⬜ Apollo.io account ($79/mo) → https://apollo.io

### LinkedIn (Optional)
- ⬜ Sales Navigator ($80/mo) → https://linkedin.com/sales/

---

## TIER 4: APP STORE SETUP (Per App)

### PrayerLock
- ⬜ App entry created in App Store Connect
- ⬜ Subscription group created
- ⬜ Monthly product created ($9.99)
- ⬜ Annual product created ($49.99)
- ⬜ Privacy policy URL set
- ⬜ Support URL set

### WalkToUnlock
- ⬜ App entry created in App Store Connect
- ⬜ Subscription group created
- ⬜ Monthly product created ($7.99)
- ⬜ Annual product created ($39.99)
- ⬜ Privacy policy URL set
- ⬜ Support URL set

### StudyLock
- ⬜ App entry created in App Store Connect
- ⬜ Subscription group created
- ⬜ Monthly product created ($6.99)
- ⬜ Annual product created ($34.99)
- ⬜ Privacy policy URL set
- ⬜ Support URL set

---

## TIER 5: AFFILIATE PROGRAMS (Apply manually)

### Faith Niche
- ⬜ Amazon Associates → https://affiliate-program.amazon.com
- ⬜ Hallow (direct outreach)

### Fitness Niche
- ⬜ Amazon Associates
- ⬜ Athletic Greens → https://athleticgreens.com/pages/affiliate
- ⬜ Thorne → https://thorne.com/affiliates

### AI/Productivity Niche
- ⬜ Impact.com → https://impact.com
- ⬜ PartnerStack → https://partnerstack.com

---

## WARMUP STATUS (Track manually)

### Email Warmup
- ⬜ Warmup started on: ____/____/____
- ⬜ 14 days complete
- ⬜ 21 days complete (safe to send)

### Social Warmup
- ⬜ X/Twitter: 7 days manual activity done
- ⬜ TikTok: 7 days manual activity done
- ⬜ Instagram: 7 days manual activity done

---

## CURRENT BLOCKERS

*Update this section with what's blocking progress:*

```
Example:
- Apple Developer approval pending (submitted 01/24)
- Waiting on DKIM propagation
- Need to purchase cold email domains
```

**Current blockers:**
- (none listed yet)

---

## SESSION START: Claude reads this file

When starting a session, Claude should:
1. Read this file
2. Check what TIER 1 items are incomplete
3. Remind human of blocking tasks
4. Only proceed with building if infrastructure exists

---

**Last Updated:** ____/____/____
