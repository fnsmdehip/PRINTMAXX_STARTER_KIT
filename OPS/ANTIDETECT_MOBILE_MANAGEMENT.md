# Anti-Detect, Proxy & Virtual Phone -- Mobile Management Guide
Updated: 2026-04-17

How to manage multi-account infrastructure from your iPhone.

---

## THE STACK (what you need for multi-account ops)

| Layer | What | Best Options | Cost | Mobile App? |
|-------|------|-------------|------|-------------|
| Anti-detect browser | Separate browser fingerprints per account | GoLogin, Multilogin, AdsPower | $49-99/mo | YES (all 3) |
| Proxies | Different IP per account | Smartproxy, Bright Data, Decodo | $10-75/mo | Dashboard only |
| Virtual phones | SMS verification per account | TextNow, Hushed, SMS-Activate | $0-25/mo | YES |
| Email | Separate email per account | Gmail aliases, Proton, catch-all domain | $0-6/mo | YES |

---

## ANTI-DETECT BROWSERS (manage from iPhone)

### GoLogin (RECOMMENDED for mobile management)
- **iOS app:** YES -- full profile management, launch browsers, check fingerprints
- **Price:** $49/mo (100 profiles), $99/mo (300 profiles)
- **Why best for you:** Mobile app lets you create/manage profiles, assign proxies, and see which accounts are active. Cloud profiles sync between Mac and phone.
- **Setup:** goLogin.com > download Mac app + iPhone app > same login
- **Each profile =** unique fingerprint (canvas, WebGL, fonts, screen res, timezone, language)

### AdsPower
- **iOS app:** YES -- "AdsPower Mobile" on App Store
- **Price:** Free (2 profiles), $5.4/mo (10), $30/mo (100)
- **Cheapest option** if you only need a few accounts

### Multilogin
- **iOS app:** YES -- "Multilogin X" on App Store
- **Price:** $99/mo+
- **Best detection evasion** but most expensive

---

## PROXY MANAGEMENT (from iPhone)

### Smartproxy (RECOMMENDED)
- **Dashboard:** Mobile-friendly web dashboard at smartproxy.com
- **Price:** $12/mo residential (2GB), $25/mo (8GB)
- **Features:** Rotate IPs per session, sticky sessions for account maintenance, 195+ locations
- **How to use with anti-detect:** Assign different proxy to each GoLogin profile. Account A = US residential IP. Account B = UK residential IP. etc.

### Bright Data
- **Dashboard:** Full mobile web dashboard
- **Price:** $10/mo+ (pay per GB)
- **When to use:** Bigger scale, need specific geo targeting

### Decodo (SOCKS5)
- **Price:** $50/mo for 300 threads
- **In your crontab already** (referenced in CLAUDE.md budget tiers)

### Free option: Tailscale Exit Nodes
- If you have a VPS ($5/mo DigitalOcean), run Tailscale on it
- Use it as exit node from Mac: `tailscale set --exit-node=vps-name`
- Different VPS = different IP. Not residential but works for lower-security platforms.

---

## VIRTUAL PHONE NUMBERS (SMS verification from iPhone)

### For US numbers:
| Service | Cost | iPhone App | Notes |
|---------|------|-----------|-------|
| TextNow | Free | YES | Free US number, ad-supported. Works for most platforms |
| Google Voice | Free | YES | Needs existing US number to set up |
| Hushed | $5/mo | YES | Temporary numbers, burner-style |
| MySudo | $5/mo | YES | 3 phone numbers, privacy-focused |
| TextVerified | $0.50-3/code | Web only | One-time SMS verifications |

### For bulk verifications:
| Service | Cost | How |
|---------|------|-----|
| SMS-Activate | $0.10-2/code | sms-activate.org, web dashboard |
| SMSPVA | $0.10-1/code | smspva.com |
| 5sim | $0.05-1/code | 5sim.net |

### Strategy:
- **Primary accounts** (your real identity): Use your real phone or Google Voice
- **Brand accounts** (PRINTMAXX, EAS, etc.): Use Hushed or MySudo ($5/mo each)
- **Burner/scale accounts** (content farms, testing): SMS-Activate for one-time codes

---

## MANAGING IT ALL FROM iPHONE

### The Mobile Ops Stack:

**1. GoLogin app** -- manage all browser profiles + proxies
- Create profiles on Mac, manage from phone
- See which accounts are "hot" (recently active)
- Assign/change proxies per profile

**2. Hushed/MySudo** -- your virtual phone numbers
- Receive SMS verifications on iPhone
- Forward to specific profiles

**3. Proton Mail** -- separate emails per account
- Free: 1 email + 3 aliases
- Plus ($4/mo): 10 aliases, custom domain, catch-all
- Use `brand1@yourdomain.com`, `brand2@yourdomain.com` etc.
- All accessible from Proton Mail iPhone app

**4. RustDesk** -- when you need to actually USE the anti-detect browser
- Anti-detect browsers run on Mac (they're desktop apps)
- RustDesk lets you see/control the Mac screen from iPhone
- Open GoLogin on Mac > launch profile > use from iPhone via RustDesk

### The Flow:
```
iPhone GoLogin app: manage profiles + proxies
    |
    v
Need to actually browse? RustDesk into Mac
    |
    v
Mac GoLogin desktop: launch browser profile
    |
    v
Browse as that identity (unique fingerprint + IP + phone + email)
```

---

## QUICK-START: Multi-Account X/Twitter Setup

For the 13-brand content strategy referenced in the dispatch:

1. **GoLogin:** Create 13 profiles, each with unique:
   - Fingerprint (auto-generated)
   - Proxy (different residential IP per profile)
   - Timezone matching the proxy location
   - User agent (mix of Chrome/Firefox/Safari)

2. **Virtual phones:** Get 13 numbers via SMS-Activate ($0.50 each = $6.50 total)

3. **Emails:** Create 13 Proton Mail aliases (Plus plan, $4/mo)

4. **Create X accounts:** One per GoLogin profile, verify with unique phone + email

5. **Warmup:** Each account starts with 5 days of browsing/liking before posting. GoLogin's "cookie robot" can automate the warmup browsing.

6. **Content:** Route from `CONTENT/social/posting_queue/` to each account based on brand/niche

7. **Manage from iPhone:** GoLogin app shows all 13 profiles. RustDesk when you need to post manually.

---

## BUDGET TIERS

| Tier | What you get | Monthly cost |
|------|-------------|-------------|
| FREE | TextNow (1 number) + free AdsPower (2 profiles) + Proton free (1 email) | $0 |
| STARTER | Hushed (2 numbers) + AdsPower 10 profiles + Smartproxy 2GB | ~$22/mo |
| GROWTH | GoLogin 100 profiles + Smartproxy 8GB + MySudo 3 numbers + Proton Plus | ~$82/mo |
| SCALE | GoLogin 300 + Bright Data 20GB + Hushed 5 numbers + catch-all domain | ~$200/mo |

**Start at STARTER.** Scale up only when accounts are making money.

---

## SECURITY NOTES

- Never log into two different profiles from the same browser/IP
- Never reuse phone numbers across profiles
- Keep a spreadsheet mapping: profile name -> email -> phone -> proxy -> platform accounts
- GoLogin handles fingerprint separation; you handle the other identifiers
- If a platform asks for ID verification, that account is burned for multi-account use
- Residential proxies > datacenter proxies for social platforms
- Mobile proxies (4G/5G) > residential for highest security (natural IP rotation)
