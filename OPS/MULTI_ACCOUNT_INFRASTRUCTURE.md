# MULTI-ACCOUNT INFRASTRUCTURE -- Complete Setup Guide

**Status:** READY TO EXECUTE
**Last Updated:** 2026-03-08
**Purpose:** Step-by-step infrastructure for running 13+ social accounts across Twitter, TikTok, Instagram, LinkedIn, and forums without getting linked or banned.
**Time to set up:** ~2 hours purchasing + configuration
**Companion docs:** `OPS/ACCOUNT_STACK_ASSIGNMENTS.md` | `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` | `OPS/TECH_INFRA_SETUP_RETARDMAXXED.md`

---

## TABLE OF CONTENTS

1. [Antidetect Browser Setup](#1-antidetect-browser-setup)
2. [Proxy Strategy](#2-proxy-strategy)
3. [Account Architecture](#3-account-architecture)
4. [Session Management & Credential Storage](#4-session-management--credential-storage)
5. [A/B Test Framework](#5-ab-test-framework)
6. [Purchasing Guide](#6-purchasing-guide)
7. [Bootstrap Sequence](#7-bootstrap-sequence)
8. [Automation Integration](#8-automation-integration)

---

## 1. ANTIDETECT BROWSER SETUP

### The Pick: AdsPower Free + GoLogin Paid

Based on testing across the codebase and confirmed Feb 2026 data:

| Browser | Verdict | Why |
|---------|---------|-----|
| **AdsPower** | START HERE (free, 5 profiles) | Confirmed best free tier in 2026. 5 profiles covers Priority 1 accounts. |
| **GoLogin** | UPGRADE TARGET ($24/mo annual, 100 profiles) | Best value paid. Already referenced throughout the stack. Solid fingerprinting. |
| **Multilogin** | SCALE TIER ($29/mo, best fingerprints) | Only when running 20+ accounts and can't afford any bans. |
| **Dolphin Anty** | DO NOT USE | Confirmed FAILING fingerprint tests Feb 2026. Skip entirely. |

**Decision:** Start with AdsPower free (5 profiles). Upgrade to GoLogin when you need profile 6+. Upgrade to Multilogin only at $10K+/mo revenue.

### AdsPower Setup (Free Tier -- Do This First)

**Step 1: Download and install**
1. Go to: https://www.adspower.com
2. Click "Free Download" (Mac version)
3. Install the .dmg
4. Create account (email + password)
5. You get 5 free browser profiles

**Step 2: Create your first browser profile**
1. Open AdsPower
2. Click "New Profile" (blue button, top right)
3. Fill in:
   - **Profile name:** `TW_PRINTMAXXER` (format: `PLATFORM_HANDLE`)
   - **Operating System:** macOS (match your real OS for consistency)
   - **Browser core:** Chromium (default, best compatibility)
   - **User Agent:** Auto-generate (let AdsPower pick one that matches your OS selection)
4. Click "Advanced Settings" to configure fingerprint (next section)

**Step 3: Configure fingerprint settings (per profile)**

These settings make each browser profile look like a unique real device. Configure for EVERY profile:

| Setting | Value | Why |
|---------|-------|-----|
| **Canvas** | Noise mode | Adds random noise to canvas fingerprint. "Off" = you look like every other AdsPower user. |
| **WebGL** | Noise mode | Same concept -- randomizes WebGL rendering output. |
| **WebGL Vendor/Renderer** | Auto-match | Must match the OS you selected. If macOS, it should show Apple GPU info. |
| **Timezone** | Match proxy location | If proxy is US East, set to America/New_York. Mismatch = instant flag. |
| **Language** | en-US | Match your target audience geo. |
| **Screen Resolution** | Random common (1920x1080, 2560x1440, 1440x900) | Pick ONE per profile and never change it. |
| **WebRTC** | Altered (use proxy IP) | Prevents WebRTC leak showing your real IP. |
| **Fonts** | System fonts ON | "Off" gives you a unique but suspicious font list. Keep default system fonts. |
| **Hardware Concurrency** | 4 or 8 | CPU core count. Pick a realistic number and keep it consistent per profile. |
| **Device Memory** | 8 | Realistic RAM value. |
| **Do Not Track** | OFF | Ironically, enabling DNT makes you MORE unique because most users don't. |
| **Audio Context** | Noise mode | Prevents audio fingerprint matching across profiles. |

**Step 4: Assign proxy to profile**
1. In the profile creation screen, go to "Proxy" section
2. Select proxy type: HTTP or SOCKS5 (depends on provider)
3. Enter: Host, Port, Username, Password (from your proxy provider)
4. Click "Check proxy" to verify it works
5. Confirm the IP and location match what you expect

**Step 5: Launch and verify**
1. Click "Open" next to your profile
2. A new browser window opens with that profile's fingerprint
3. Go to https://whoer.net -- verify:
   - IP shows proxy IP (not your real IP)
   - Location matches proxy geo
   - Anonymity score is 70%+ (higher = better)
4. Go to https://browserleaks.com/canvas -- verify canvas fingerprint is unique
5. Go to https://browserleaks.com/webgl -- verify WebGL is randomized

### Profile Naming Convention

Use this exact format so you (and agents) can identify profiles instantly:

```
{PLATFORM}_{HANDLE}

Examples:
TW_PRINTMAXXER      -- Twitter @PRINTMAXXER
TW_growthpilled      -- Twitter @growthpilled
TT_PRINTMAXX         -- TikTok PRINTMAXX
IG_clipvault          -- Instagram @clipvault_
LI_PRINTMAXX         -- LinkedIn
RD_outboundtwts      -- Reddit
```

### Profiles to Create (5 for AdsPower Free)

Your 5 free AdsPower profiles should cover Priority 1 accounts:

| Profile # | Name | Account | Proxy Group |
|-----------|------|---------|-------------|
| 1 | `TW_PRINTMAXXER` | @PRINTMAXXER (Twitter) | Group A (IPRoyal #1) |
| 2 | `TW_growthpilled` | @growthpilled (Twitter) | Group B (Webshare #1) |
| 3 | `TW_outboundtwts` | @outboundtwts (Twitter) | Group E (Webshare #2) |
| 4 | `TW_clipvault` | @clipvault_ (Twitter) | Group B (Webshare #3) |
| 5 | `TW_toolstwts` | @toolstwts (Twitter) | Group A (Webshare #4) |

When you upgrade to GoLogin, create profiles for accounts 6-13 (repscheme, voidpilled, selahmoments, shiplog_, silentframes, velvetframes, GoddessAriaAI, drifthour) plus TikTok and Instagram profiles for cross-platform accounts.

### GoLogin Setup (When Upgrading)

1. Go to: https://gologin.com
2. Download app (Mac)
3. Sign up for annual plan: **$24/mo** (billed $288/year) -- gives 100 profiles
4. Profile creation is nearly identical to AdsPower
5. GoLogin has a "Quick Profile" button that auto-generates realistic fingerprints. Use it, then tweak timezone/language/proxy.
6. GoLogin also has **cloud profiles** -- browser runs on their servers, not your machine. Useful for running 10+ profiles simultaneously without killing your RAM.
7. Import/export: GoLogin supports exporting profile configs as JSON. Use this for backup.

### Fingerprint Testing (Run After Every New Profile)

After creating any profile, test it before using it for account creation:

```
Test URLs (open in each profile):
1. https://whoer.net                    -- IP, location, anonymity score
2. https://browserleaks.com/canvas      -- Canvas fingerprint uniqueness
3. https://browserleaks.com/webgl       -- WebGL fingerprint
4. https://amiunique.org                -- Overall uniqueness score
5. https://pixelscan.net                -- Anti-detect detection (should show "Not detected")
```

**Pass criteria:**
- whoer.net anonymity: 70%+ (ideally 80%+)
- pixelscan.net: "Not detected" as antidetect browser
- Canvas: unique hash (different from other profiles)
- WebGL: different renderer string per profile
- IP: shows proxy IP, not your real IP

**If pixelscan.net detects you as antidetect:** Switch Canvas/WebGL from "Noise" to a different noise seed, or switch to GoLogin which has better fingerprint masking.

---

## 2. PROXY STRATEGY

### Why Mobile Proxies for Social Media

Platforms categorize IP addresses by type. The hierarchy of trust:

```
MOST TRUSTED ──────────────────────────── LEAST TRUSTED
Mobile 4G/5G > Residential > ISP Static > Datacenter
```

**Mobile proxies** are the gold standard for Twitter and TikTok because:
- Hundreds of real users share the same mobile IP at any given time
- Platforms cannot ban a mobile IP without banning legitimate users
- Twitter and TikTok's detection systems treat mobile IPs as inherently trustworthy
- IP reputation databases rate mobile IPs highest

**Residential proxies** work for lower-risk platforms (LinkedIn, Reddit, Pinterest, forums) because:
- Still real user IPs, just from home connections
- Cheaper than mobile
- Adequate for platforms that don't aggressively fingerprint

**ISP static proxies** are the sweet spot for budget accounts:
- Real ISP-assigned IPs (not datacenter)
- Unlimited bandwidth (no per-GB billing)
- $2/IP/month from IPRoyal
- Good enough for Twitter accounts that aren't your flagship

**Datacenter proxies** will get you banned on any social platform. Never use them for accounts you want to keep.

### Provider Recommendations

#### Mobile Proxies (Twitter Main + TikTok)

| Provider | Price | Best For | URL | Notes |
|----------|-------|----------|-----|-------|
| **SOAX** | $99/mo (6.6GB) | TikTok + IG | https://soax.com | Clean mobile IPs. Rotation configurable. US, UK, EU pools. |
| **Proxy-Seller** | $90/mo per IP | Dedicated single account | https://proxy-seller.com | One sticky IP per account. Best isolation. |
| **The Social Proxy** | $90/mo per IP | Social-focused | https://thesocialproxy.com | Built specifically for social media ops. |

**Recommendation for PRINTMAXX:** SOAX at $99/mo. Gives you enough mobile bandwidth for 3-5 high-value accounts (TikTok + Twitter flagship). Use sticky sessions set to 30 minutes.

#### ISP Static Proxies (Twitter Alts)

| Provider | Price | Best For | URL | Notes |
|----------|-------|----------|-----|-------|
| **IPRoyal** | $2/IP/mo, unlimited bandwidth | Twitter alts, bulk accounts | https://iproyal.com/static-residential-proxies | Best value. Real ISP IPs. Unlimited bandwidth means no tracking data usage per account. |
| **Bright Data** | $15/GB residential | Enterprise/scale | https://brightdata.com | Overkill for current stage. |

**Recommendation for PRINTMAXX:** IPRoyal ISP static. $2/IP/month with unlimited bandwidth. Buy 8-13 IPs = $16-26/mo. Assign one IP per account permanently.

#### Free Tier (Testing Only)

| Provider | What You Get | URL | Limitation |
|----------|-------------|-----|------------|
| **Webshare** | 10 free proxies | https://www.webshare.io | Datacenter IPs. Will get flagged on Twitter/TikTok within weeks. Fine for LinkedIn, Reddit, Pinterest. |
| **Bright Data** | 15 IPs + 2GB free trial | https://brightdata.com | Trial expires. Use for initial testing only. |

### Proxy Assignment Map

One proxy per account. Never share proxies between accounts on the same platform. Accounts on different platforms CAN share a proxy (Twitter and TikTok on the same IP is actually fine -- that's what real users do).

```
PROXY GROUP A (Tech cluster -- same person vibes):
  IPRoyal ISP Static #1 (US East)  ──> @PRINTMAXXER (Twitter)
  Webshare #4                      ──> @toolstwts (Twitter)
  Webshare #4                      ──> @shiplog_ (Twitter)  [shared, same cluster]

PROXY GROUP B (Growth/Viral cluster):
  Webshare #1                      ──> @growthpilled (Twitter)
  Webshare #1                      ──> @voidpilled (Twitter)  [shared, same cluster]
  Webshare #3                      ──> @clipvault_ (Twitter)

PROXY GROUP C (NSFW -- COMPLETELY ISOLATED):
  IPRoyal ISP DEDICATED #X         ──> @GoddessAriaAI (Twitter)
  NEVER share this IP with ANY other account.
  Different email domain. Different everything.

PROXY GROUP D (Wellness/Aesthetic):
  Webshare #6                      ──> @selahmoments (Twitter)
  Webshare #7                      ──> @silentframes (Twitter)

PROXY GROUP E (Mixed):
  Webshare #2                      ──> @outboundtwts (Twitter)
  Webshare #5                      ──> @repscheme (Twitter)

PROXY GROUP F (Beauty -- isolated):
  IPRoyal ISP DEDICATED #Y         ──> @velvetframes (Twitter)

MOBILE PROXY (SOAX -- TikTok mandatory):
  SOAX Mobile #1 (US, 30min sticky) ──> PRINTMAXX TikTok
  SOAX Mobile #2 (US, 30min sticky) ──> TikTok Alt 1
  SOAX Mobile #3 (US, 30min sticky) ──> TikTok Alt 2
```

### IP Rotation Strategy

**Social media accounts: NEVER rotate.**
- Use sticky sessions (same IP for 30+ minutes per session)
- Same IP every time you log in
- Platforms track IP history. Changing IPs = suspicious.
- For SOAX: set `sessionduration-30` in your proxy string
- For ISP static: the IP never changes (that's the point)

**Scraping accounts: ALWAYS rotate.**
- New IP per request or every 1-5 requests
- Use residential rotating pool
- This is for the twitter scraper, reddit scraper, etc.
- Completely separate from social account proxies

**Proxy string formats:**

```
# SOAX Mobile (sticky 30 min session)
user-mobile-country-US-sessionduration-30:PASSWORD@proxy.soax.com:9000

# SOAX Residential (rotating)
user-residential-country-US:PASSWORD@proxy.soax.com:9000

# IPRoyal ISP Static
USERNAME:PASSWORD@geo.iproyal.com:PORT

# Webshare (free datacenter)
USERNAME:PASSWORD@proxy.webshare.io:PORT
```

### VPN for Main Account (Your Personal Device)

For @PRINTMAXXER on your personal device (not through antidetect browser):

Use a VPN. Not a proxy. A VPN encrypts your entire connection and is what normal users do.

| VPN | Price | Why | URL |
|-----|-------|-----|-----|
| **Mullvad** | $5.50/mo | No account needed. Pay with cash. Best privacy. | https://mullvad.net |
| **ProtonVPN** | Free tier available, $4.99/mo paid | Swiss privacy. Good speeds. Free tier is unlimited bandwidth. | https://protonvpn.com |
| **IVPN** | $6/mo | WireGuard. Multi-hop. Similar philosophy to Mullvad. | https://ivpn.net |

**Recommendation:** ProtonVPN free to start (unlimited bandwidth, good speeds). Upgrade to Mullvad ($5.50/mo) when revenue comes in.

**VPN rules for @PRINTMAXXER:**
- Pick ONE VPN server location (e.g., US East) and stick with it
- Don't hop between countries
- Use the same VPN location every session
- Kill switch ON (prevents IP leak if VPN disconnects)
- Don't use the VPN for any other social accounts (different IP fingerprint)

---

## 3. ACCOUNT ARCHITECTURE

### Complete Account Map

```
TIER 1: MAIN ACCOUNTS (highest protection)
=============================================

@PRINTMAXXER (Twitter)
  Device:   Your MacBook, personal browser (Safari/Brave)
  IP:       ProtonVPN (US East, same server always)
  Email:    printmaxxer@[yourdomain.com]
  Phone:    YOUR REAL PHONE
  2FA:      TOTP (Authy or 1Password)
  Premium:  X Premium Basic ($3/mo) -- MANDATORY
  Status:   Warmup Day 2 (started 2026-03-07)

PRINTMAXX TikTok
  Device:   Antidetect Profile `TT_PRINTMAXX`
  IP:       SOAX Mobile #1 (US, 30min sticky)
  Email:    printmaxx.tk@[yourdomain.com]
  Phone:    Ultra Mobile PayGo #1 ($3/mo)
  2FA:      TOTP
  Note:     TikTok REQUIRES mobile proxy. Will instant-ban on datacenter/residential.


TIER 2: PRIORITY ALTS (accounts 2-5)
=============================================

@growthpilled (Twitter)
  Device:   Antidetect Profile `TW_growthpilled`
  IP:       Webshare #1 (shared with @voidpilled -- different platform cluster)
  Email:    growthpilled@[yourdomain.com]
  Phone:    SMSPool one-time ($0.50)
  Premium:  X Premium Basic ($3/mo)

@outboundtwts (Twitter)
  Device:   Antidetect Profile `TW_outboundtwts`
  IP:       Webshare #2
  Email:    outboundtwts@[yourdomain.com]
  Phone:    SMSPool one-time ($0.50)
  Premium:  X Premium Basic ($3/mo)

@clipvault_ (Twitter)
  Device:   Antidetect Profile `TW_clipvault`
  IP:       Webshare #3
  Email:    clipvault@[yourdomain.com]
  Phone:    SMSPool one-time ($0.50)
  Premium:  X Premium Basic ($3/mo)

@toolstwts (Twitter)
  Device:   Antidetect Profile `TW_toolstwts`
  IP:       Webshare #4 (shared with @shiplog_ -- same tech cluster)
  Email:    toolstwts@[yourdomain.com]
  Phone:    Google Voice
  Premium:  X Premium Basic ($3/mo)


TIER 3: SECONDARY ALTS (accounts 6-10)
=============================================

@repscheme (Twitter + TikTok + IG)
  Twitter:  Antidetect Profile `TW_repscheme`, Webshare #5
  TikTok:   Antidetect Profile `TT_repscheme`, SOAX Mobile #2
  IG:       Antidetect Profile `IG_repscheme`, SOAX Mobile #2

@voidpilled (Twitter)
  Device:   Antidetect Profile `TW_voidpilled`
  IP:       Webshare #1 (shared with @growthpilled)

@selahmoments (Twitter + TikTok)
  Twitter:  Antidetect Profile `TW_selahmoments`, Webshare #6
  TikTok:   Antidetect Profile `TT_selahmoments`, SOAX Mobile #3

@shiplog_ (Twitter)
  Device:   Antidetect Profile `TW_shiplog`
  IP:       Webshare #4 (shared with @toolstwts)

@silentframes (Twitter + IG + Pinterest)
  Twitter:  Antidetect Profile `TW_silentframes`, Webshare #7
  IG:       Antidetect Profile `IG_silentframes`, Webshare #7


TIER 4: ISOLATED / SPECIAL (accounts 11-13)
=============================================

@velvetframes (Twitter + IG + TikTok + Pinterest)
  Device:   Antidetect Profile `TW_velvetframes`
  IP:       IPRoyal ISP DEDICATED (NEVER shared)
  Email:    velvetframes@[yourdomain.com]

@GoddessAriaAI (Twitter + Fanvue + Telegram) -- NSFW
  Device:   Antidetect Profile `TW_GoddessAria`
  IP:       IPRoyal ISP DEDICATED (COMPLETELY ISOLATED)
  Email:    SEPARATE DOMAIN -- NOT on same domain as other accounts
  Phone:    SMSPool one-time, NEVER reuse
  Note:     ZERO crossover with any other account. Different domain,
            different proxy, different browser profile group, different
            payment method if possible.

@drifthour (IG + TikTok + YouTube + Spotify) -- NO Twitter
  Device:   Antidetect Profile `IG_drifthour`
  IP:       Webshare #8


TIER 5: LOW-RISK PLATFORMS (LinkedIn, Reddit, Forums)
=============================================

LinkedIn PRINTMAXX
  Device:   Antidetect Profile `LI_PRINTMAXX`
  IP:       Any residential proxy
  Note:     LinkedIn is less aggressive on fingerprinting.
            Residential proxy is fine. No mobile needed.

Reddit accounts
  Device:   Antidetect profiles or Firefox Multi-Account Containers (free)
  IP:       Residential or even free Webshare
  Note:     Reddit barely fingerprints. Lowest risk platform.
            Firefox containers are free and sufficient.

Forums / Niche communities
  Device:   Regular browser with VPN
  IP:       ProtonVPN
  Note:     Forums have minimal detection. VPN is overkill but safe.
```

### A/B Test Accounts (Pre-Warmed vs Fresh)

For the A/B test, you need 2 extra accounts per platform being tested:

```
A/B TEST: Twitter
  CONTROL (Pre-warmed):
    Buy aged account from AccsMarket ($15-40)
    Antidetect Profile `TW_AB_WARM`
    IPRoyal ISP Static (dedicated)
    Same content as test account

  TEST (Fresh):
    Create new account
    Antidetect Profile `TW_AB_FRESH`
    IPRoyal ISP Static (dedicated, different IP)
    Same content as control account

A/B TEST: TikTok
  CONTROL (Pre-warmed):
    Buy aged account from AccsMarket/SocialTradia ($20-50)
    Antidetect Profile `TT_AB_WARM`
    SOAX Mobile (dedicated)

  TEST (Fresh):
    Create new account
    Antidetect Profile `TT_AB_FRESH`
    SOAX Mobile (dedicated, different session)
```

### Account Isolation Rules (Non-Negotiable)

1. **Never log into two accounts from the same browser profile.** One profile = one account. Period.
2. **Never share proxies between accounts on the SAME platform.** @growthpilled and @clipvault_ cannot use the same proxy since both are Twitter.
3. **Sharing proxies across DIFFERENT platforms is OK.** The same IP for a Twitter account and a TikTok account is normal user behavior.
4. **Never follow/DM/interact between your own accounts.** Platforms detect reciprocal patterns between accounts on the same IP block.
5. **Never use the same phone number for multiple accounts on the same platform.** SMSPool numbers are one-time use. Don't reuse.
6. **Keep @GoddessAriaAI completely isolated.** Different domain, different proxy, different everything. NSFW accounts getting linked to your main brand = nuclear.
7. **Never log into antidetect profiles from your personal browser.** Your personal browser is for @PRINTMAXXER only (via VPN).

---

## 4. SESSION MANAGEMENT & CREDENTIAL STORAGE

### Credential Storage

All credentials go in `SECRETS/CREDENTIALS.env` (already gitignored). Format:

```env
# ============================================
# SOCIAL ACCOUNTS — MULTI-ACCOUNT SECTION
# ============================================

# Format: PLATFORM_HANDLE_FIELD=value

# --- @PRINTMAXXER (Twitter) ---
TW_PRINTMAXXER_EMAIL=printmaxxer@yourdomain.com
TW_PRINTMAXXER_PASSWORD=
TW_PRINTMAXXER_PHONE=your_real_phone
TW_PRINTMAXXER_2FA_SECRET=
TW_PRINTMAXXER_PROXY=vpn_us_east
TW_PRINTMAXXER_PROFILE=personal_browser
TW_PRINTMAXXER_PREMIUM=basic_3mo

# --- @growthpilled (Twitter) ---
TW_GROWTHPILLED_EMAIL=growthpilled@yourdomain.com
TW_GROWTHPILLED_PASSWORD=
TW_GROWTHPILLED_PHONE=smspool_onetime
TW_GROWTHPILLED_2FA_SECRET=
TW_GROWTHPILLED_PROXY=webshare_1
TW_GROWTHPILLED_PROFILE=adspower_2

# --- PRINTMAXX TikTok ---
TT_PRINTMAXX_EMAIL=printmaxx.tk@yourdomain.com
TT_PRINTMAXX_PASSWORD=
TT_PRINTMAXX_PHONE=ultra_mobile_1
TT_PRINTMAXX_2FA_SECRET=
TT_PRINTMAXX_PROXY=soax_mobile_1
TT_PRINTMAXX_PROFILE=adspower_3_or_gologin

# --- PROXY CREDENTIALS ---
SOAX_USERNAME=
SOAX_PASSWORD=
SOAX_HOST=proxy.soax.com
SOAX_PORT=9000

IPROYAL_STATIC_1_HOST=
IPROYAL_STATIC_1_PORT=
IPROYAL_STATIC_1_USER=
IPROYAL_STATIC_1_PASS=

WEBSHARE_PROXY_1=username:password@proxy.webshare.io:port
WEBSHARE_PROXY_2=username:password@proxy.webshare.io:port
# ... up to WEBSHARE_PROXY_8

# --- ANTIDETECT BROWSER ---
ADSPOWER_EMAIL=
ADSPOWER_PASSWORD=
GOLOGIN_EMAIL=
GOLOGIN_PASSWORD=
GOLOGIN_API_TOKEN=
```

**Security rules:**
- `SECRETS/` is in `.gitignore`. Never committed.
- `chmod 600 SECRETS/*` -- only your user can read.
- 2FA secrets: store in 1Password or Authy, not just in this file. This file is a backup reference.
- Rotate passwords every 90 days for high-value accounts (@PRINTMAXXER, TikTok main).

### Browser Cookie Persistence

This is the main advantage of antidetect browsers. Here's how it works:

**How sessions persist in antidetect browsers:**
1. You open an antidetect profile and log into Twitter
2. Twitter sets cookies in that browser profile
3. You close the profile
4. All cookies, localStorage, IndexedDB, and session data are saved to the profile
5. Next time you open that profile, you're still logged in
6. No re-login needed unless the session expires server-side

**What causes re-login prompts (and how to avoid them):**

| Cause | Fix |
|-------|-----|
| Proxy IP changed between sessions | Use sticky proxy. Same IP every time. ISP static never changes. SOAX: set sessionduration-30 and use same session ID. |
| Browser fingerprint changed | Never modify fingerprint settings after account creation. Lock them in. |
| Cookies expired server-side | Twitter: ~30 days. TikTok: ~7-14 days. IG: ~30 days. Re-login before expiry by opening the profile at least weekly. |
| Platform detected suspicious activity | Reduce posting volume. Check shadowban status. |
| Different timezone/language than proxy geo | Ensure antidetect profile timezone matches proxy country. |

**Session health maintenance:**
- Open each antidetect profile at least once every 5 days to keep cookies fresh
- When you open a profile, scroll the feed for 2-3 minutes before doing anything (mimics human behavior)
- If forced to re-login, do it from the SAME profile with the SAME proxy. Never from a different profile.
- After re-login, wait 30 minutes of normal browsing before posting

### Session Health Monitoring

Create a simple tracking sheet (or use the existing warmup state tracker):

```
ACCOUNT HEALTH CHECK (run weekly)

Account             Last Login    Session Status    Shadowban Check    Notes
@PRINTMAXXER        2026-03-08    ACTIVE            CLEAN              Warmup Day 2
@growthpilled       NOT CREATED   -                 -                  Pending creation
@outboundtwts       NOT CREATED   -                 -                  Pending creation
@clipvault_         NOT CREATED   -                 -                  Pending creation
@toolstwts          NOT CREATED   -                 -                  Pending creation
TT_PRINTMAXX        NOT CREATED   -                 -                  Pending creation
```

**Shadowban check URLs:**
- Twitter: https://shadowban.eu (enter handle, checks search/reply/ghost ban)
- TikTok: No reliable checker. Monitor view counts -- sudden 80%+ drop = shadowbanned.
- Instagram: Use a second device to search for your posts in hashtags. Not appearing = shadowbanned.

---

## 5. A/B TEST FRAMEWORK

### Purpose

Answer the question: "Is it worth buying pre-warmed accounts ($15-40 each) or can fresh accounts perform just as well after warmup?"

This directly impacts how you scale. If pre-warmed accounts significantly outperform, you buy 10 and skip 3 weeks of warmup per account. If fresh accounts perform similarly after warmup, you save money.

### Test Protocol

**Platforms to test:** Twitter (first), then TikTok

**Variables held constant (same for both test and control):**
- Exact same content (same tweets, same times, same order)
- Same niche (pick one niche, e.g., growth hacks)
- Same proxy type (ISP static for Twitter, mobile for TikTok)
- Same antidetect browser (AdsPower or GoLogin)
- Same fingerprint quality settings
- Same posting schedule
- Same engagement activity (likes, follows, replies per day)

**Variable being tested:**
- Account age / warmup status (pre-warmed vs fresh with 21-day warmup)

### Setup

```
CONTROL: Pre-Warmed Account
1. Buy aged Twitter account from AccsMarket ($15-40)
   - Requirements: 6+ months old, some post history, clean (no violations)
   - Verify: email access included, no previous bans
2. Follow post-purchase protocol (OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md):
   - Day 0: Change password, add 2FA
   - Day 1-2: Manual engagement only
   - Day 3-4: Update profile gradually, first text post
   - Day 5-7: Normal posting, heavy engagement
3. Start A/B test content on Day 8

TEST: Fresh Account
1. Create new Twitter account in antidetect profile
2. Follow full 21-day warmup (OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md):
   - Days 1-3: Lurk only
   - Days 4-7: Light engagement
   - Days 8-14: Start posting (1-2/day)
   - Days 15-21: Build velocity (3-5/day)
3. Start A/B test content on Day 22
```

### Metrics to Track

Track daily for each account in a spreadsheet:

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| **Impressions per post** | Twitter Analytics (native) | Raw reach. Are posts being distributed? |
| **Engagement rate** | (Likes + Replies + RTs) / Impressions | Quality of distribution. Are impressions converting? |
| **Follower growth rate** | New followers per day | Account velocity. |
| **Reply visibility** | Check if replies appear in threads | Shadow ban indicator. |
| **Profile visits** | Twitter Analytics | Are people clicking through? |
| **Link clicks** | Twitter Analytics (after Day 22+) | Revenue potential. |
| **Suspension/restriction events** | Count any warnings or restrictions | Account health. |

### Test Duration

**Minimum:** 30 days of identical content posting (after warmup is complete for both)

**Why 30 days:**
- Twitter's algorithm needs ~2 weeks to "learn" an account's content pattern
- Week 1-2 data is noisy. Week 3-4 data is signal.
- Seasonal effects need at least a full month to average out

### Decision Criteria

**Pre-warmed wins if:**
- Average impressions per post are 2x+ higher over the 30-day period
- Engagement rate is 50%+ higher
- Zero suspension events vs any on fresh account
- Follower growth is 2x+ faster

**Fresh wins if:**
- Performance is within 20% of pre-warmed after full warmup
- Zero suspension events
- The $15-40 saved per account scales meaningfully (at 10+ accounts, that's $150-400)

**Likely outcome based on community data:**
Pre-warmed accounts typically outperform fresh accounts for the first 60 days, then the gap narrows. At 90 days, performance is roughly equal. The pre-warmed advantage is speed-to-revenue, not permanent superiority.

### When to Run

**Start the A/B test AFTER your main accounts are set up and posting.** Don't delay revenue-generating accounts to run experiments. The A/B test uses 2 extra accounts specifically allocated for testing.

---

## 6. PURCHASING GUIDE

### What to Buy and In What Order

**Phase 1: Day 1 Purchases ($15-26 total)**

| Item | Cost | Where to Buy | What You're Getting |
|------|------|-------------|---------------------|
| Domain for catch-all email | $5-8 | https://porkbun.com | One domain. Set up Cloudflare Email Routing (free, unlimited aliases). Every account gets handle@yourdomain.com. |
| AdsPower (free tier) | $0 | https://www.adspower.com | Download and install. 5 browser profiles. |
| Webshare (free tier) | $0 | https://www.webshare.io | Sign up. 10 free datacenter proxies. Good enough to start. |
| SMSPool balance | $5-10 | https://smspool.net | Add balance. Use for phone verification. ~$0.50-2 per verification. |
| Google Voice | $0 | https://voice.google.com | One free US number. Use for @toolstwts. |
| ProtonVPN (free) | $0 | https://protonvpn.com | For @PRINTMAXXER on your personal device. |
| **TOTAL** | **$10-18** | | |

**Phase 2: Immediately After Account Creation ($36/mo)**

| Item | Cost | Where to Buy | What You're Getting |
|------|------|-------------|---------------------|
| X Premium Basic (per account) | $3/mo each | Inside Twitter Settings > Premium | 10x impressions, reply priority, TweepCred boost. BUY THIS FOR EVERY TWITTER ACCOUNT THE SECOND IT'S CREATED. |
| **TOTAL (12 accounts)** | **$36/mo** | | |

**Phase 3: When Webshare Gets Flagged or You Need TikTok ($41-125/mo)**

| Item | Cost | Where to Buy | What You're Getting |
|------|------|-------------|---------------------|
| IPRoyal ISP Static (8 IPs) | $16/mo | https://iproyal.com/static-residential-proxies | 8 static IPs with unlimited bandwidth. One per priority Twitter account. Replaces Webshare. |
| SOAX Mobile (for TikTok) | $99/mo | https://soax.com | Mobile 4G/5G proxies. Required for TikTok. Use sticky sessions. |
| **TOTAL** | **$115/mo** | | |

**Phase 4: When You Need 10+ Profiles ($24/mo additional)**

| Item | Cost | Where to Buy | What You're Getting |
|------|------|-------------|---------------------|
| GoLogin annual plan | $24/mo (billed $288/year) | https://gologin.com | 100 browser profiles. Replace AdsPower free. Better fingerprinting. |
| **TOTAL** | **$24/mo** | | |

**Phase 5: A/B Test Accounts ($15-80 one-time)**

| Item | Cost | Where to Buy | What You're Getting |
|------|------|-------------|---------------------|
| Pre-warmed Twitter account | $15-40 | https://accsmarket.com | 6+ month aged account for A/B control. |
| Pre-warmed TikTok account | $20-50 | https://accsmarket.com or https://socialtradia.com | Aged TikTok for A/B control. |
| **TOTAL** | **$35-90 one-time** | | |

### Total Monthly Cost Breakdown

| Stage | Monthly Cost | What's Running |
|-------|-------------|----------------|
| **Day 1 (free start)** | $0/mo + $10-18 one-time | 5 Twitter accounts on free proxies, @PRINTMAXXER on VPN |
| **After account creation** | $36/mo | X Premium on all accounts |
| **Adding TikTok** | $151/mo | Above + SOAX mobile + IPRoyal upgrade |
| **10+ profiles** | $175/mo | Above + GoLogin annual |
| **Full stack** | $175/mo + $35-90 A/B one-time | Everything running |

### Purchasing Instructions (Step by Step)

**Porkbun Domain:**
1. Go to https://porkbun.com
2. Search for a domain (e.g., `yourname-mail.com` or similar)
3. Pick a .com for $10/year or a cheaper TLD (.xyz $5, .io $30)
4. Purchase with credit card
5. After purchase: Go to Cloudflare (https://cloudflare.com), add the domain, set up Email Routing
6. In Cloudflare Email Routing: Create catch-all rule that forwards `*@yourdomain.com` to your personal email
7. Now `printmaxxer@yourdomain.com`, `growthpilled@yourdomain.com`, etc. all forward to you

**SMSPool:**
1. Go to https://smspool.net
2. Create account
3. Add $10 via credit card or crypto
4. When creating a social account: SMSPool dashboard > Select service (Twitter/TikTok/IG) > Select country (US) > Click "Order" > Get temporary phone number > Use for verification > Code appears in SMSPool dashboard
5. Each verification costs $0.50-2. $10 covers 5-20 verifications.

**IPRoyal ISP Static:**
1. Go to https://iproyal.com/static-residential-proxies
2. Select: Country US, State (pick one close to you or East Coast)
3. Quantity: 8 (or however many accounts you're running)
4. Protocol: HTTP/HTTPS
5. Purchase ($2/IP/month = $16/mo for 8)
6. After purchase: Dashboard shows you each IP's host:port:user:pass
7. Copy each proxy string into the appropriate antidetect browser profile

**SOAX Mobile:**
1. Go to https://soax.com
2. Sign up
3. Select plan: Mobile Proxies, $99/mo (6.6GB)
4. Purchase
5. Dashboard > Get proxy credentials
6. Configure: Type = Mobile (4G/5G), Country = US, Rotation = 30 min
7. Copy proxy string: `user-mobile-country-US-sessionduration-30:PASSWORD@proxy.soax.com:9000`
8. Use different session IDs for different TikTok accounts (append `-sessid-ACCOUNT1` to username)

**GoLogin:**
1. Go to https://gologin.com
2. Click "Try Free" to test, or go straight to Pricing
3. Select "Professional" plan, toggle to Annual billing ($24/mo)
4. Download the Mac app
5. Sign in
6. Start creating profiles (same process as AdsPower described in Section 1)

---

## 7. BOOTSTRAP SEQUENCE

### Exact Order of Operations

Do these in order. Don't skip steps. Each step depends on the previous one.

```
DAY 1: INFRASTRUCTURE (1.5-2 hours)
====================================

Hour 1: Purchases
  [ ] 1. Buy domain on Porkbun ($5-10)
  [ ] 2. Add domain to Cloudflare (free)
  [ ] 3. Set up Cloudflare Email Routing (catch-all → your email)
  [ ] 4. Add $10 to SMSPool
  [ ] 5. Download and install AdsPower (free)
  [ ] 6. Download and install ProtonVPN (free)
  [ ] 7. Sign up for Webshare free tier (10 proxies)

Hour 2: Profile Creation
  [ ] 8. Create 5 AdsPower profiles (see Section 1 for settings):
         - TW_PRINTMAXXER (proxy: VPN -- this one uses your personal browser)
         - TW_growthpilled (proxy: Webshare #1)
         - TW_outboundtwts (proxy: Webshare #2)
         - TW_clipvault (proxy: Webshare #3)
         - TW_toolstwts (proxy: Webshare #4)
  [ ] 9. Test each profile at whoer.net and pixelscan.net
  [ ] 10. Fix any profiles that fail fingerprint tests


DAY 1-2: ACCOUNT CREATION (30 min per account)
================================================

For EACH account (do one at a time, not simultaneously):

  [ ] 1. Connect ProtonVPN (for @PRINTMAXXER only) or open antidetect profile
  [ ] 2. Go to twitter.com/signup
  [ ] 3. Use email: handle@yourdomain.com
  [ ] 4. Get phone verification from SMSPool (or your real phone for @PRINTMAXXER)
  [ ] 5. Complete signup
  [ ] 6. Set profile photo, banner, bio, link
         (All already generated -- MEDIA/generated_images/ for @PRINTMAXXER,
          CONTENT/social/TWITTER_PROFILE_SPEC.md for specs)
  [ ] 7. Enable 2FA (TOTP -- use Authy or 1Password, NOT SMS)
  [ ] 8. Screenshot the 2FA backup codes
  [ ] 9. Buy X Premium Basic ($3/mo) for this account
  [ ] 10. Close the browser profile (saves session/cookies)
  [ ] 11. Update SECRETS/CREDENTIALS.env with email, password, 2FA
  [ ] 12. Update SECRETS/created_accounts.json

  Wait 15-30 minutes between creating accounts.
  Do NOT create all 12 in one sitting. Do 3-5 per day max.


DAY 2-3: ACCOUNT SEPARATION VERIFICATION
==========================================

  [ ] 1. Open each profile one at a time
  [ ] 2. Verify at whoer.net: different IP per profile
  [ ] 3. Verify at browserleaks.com/canvas: different canvas fingerprint
  [ ] 4. Check Twitter doesn't show "We noticed a new login" warnings
  [ ] 5. Browse feed for 5-10 minutes per account (establish patterns)
  [ ] 6. Close each profile before opening the next one


DAY 3+: BEGIN WARMUP PROTOCOLS
================================

  Follow the warmup schedules in OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md

  @PRINTMAXXER is already on Day 2 of warmup (started 2026-03-07).
  The twitter_warmup_poster.py handles posting limits automatically.

  For each new account:
  [ ] 1. Days 1-3: LURK only (browse, no engagement)
  [ ] 2. Days 4-7: Light engagement (likes, follows)
  [ ] 3. Days 8-14: First posts (text only, no links)
  [ ] 4. Days 15-21: Ramp up (3-5 posts/day)
  [ ] 5. Day 22+: Full operations


WEEK 2: TIKTOK SETUP (requires SOAX mobile proxy purchase)
=============================================================

  [ ] 1. Purchase SOAX mobile proxies ($99/mo)
  [ ] 2. Create antidetect profiles for TikTok accounts
  [ ] 3. Assign SOAX mobile proxies to TikTok profiles
  [ ] 4. Create TikTok accounts (one per session, 30 min apart)
  [ ] 5. Begin TikTok warmup (30 days -- stricter than Twitter)
  [ ] 6. TikTok warmup: 7 days of ONLY watching videos before first upload


WEEK 3: SCALE (after first accounts are warmed)
================================================

  [ ] 1. If Webshare proxies got flagged: Purchase IPRoyal ISP Static ($16/mo)
  [ ] 2. If need 10+ profiles: Upgrade to GoLogin ($24/mo)
  [ ] 3. Create accounts 6-10 (repscheme, voidpilled, selahmoments, shiplog_, silentframes)
  [ ] 4. Begin A/B test: buy pre-warmed account, start comparison
  [ ] 5. Create @GoddessAriaAI on completely isolated infrastructure
```

### Quick Reference: What You Need Per Platform

| Platform | Proxy Type Required | Antidetect Required? | Warmup Duration |
|----------|-------------------|---------------------|-----------------|
| Twitter | ISP Static or Mobile | Yes | 21 days |
| TikTok | Mobile ONLY | Yes | 30 days |
| Instagram | Mobile or Residential | Yes | 21 days |
| LinkedIn | Residential | Optional (lower risk) | 14 days |
| Reddit | Any (even datacenter) | Optional | 7-14 days |
| Pinterest | Any | No | 7 days |
| YouTube | Any | No | 14 days |
| Forums | VPN sufficient | No | None |

---

## 8. AUTOMATION INTEGRATION

### How Agents Post Through Antidetect Profiles

The existing `twitter_warmup_poster.py` currently posts via Twitter API. To post through antidetect browser profiles instead (more realistic, less detectable), here's the integration pattern:

**Option A: Playwright + Proxy (No Antidetect Browser Needed)**

Playwright can be configured with the same proxy and a stealth plugin to mimic what an antidetect browser does. This is what the existing automation stack uses.

```python
# Example: Posting via Playwright with proxy (already in the stack)
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import random, time

def post_to_twitter(proxy_config, tweet_text, cookies_file=None):
    """Post a tweet through Playwright with proxy and stealth."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={
                "server": f"http://{proxy_config['host']}:{proxy_config['port']}",
                "username": proxy_config["user"],
                "password": proxy_config["pass"]
            }
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...",
            locale="en-US",
            timezone_id="America/New_York"
        )
        stealth_sync(context)

        page = context.new_page()

        # Load saved cookies (session persistence)
        if cookies_file:
            import json
            with open(cookies_file) as f:
                cookies = json.load(f)
            context.add_cookies(cookies)

        page.goto("https://twitter.com/compose/tweet")
        time.sleep(random.uniform(2, 4))

        # Type with human-like delays
        for char in tweet_text:
            page.keyboard.type(char)
            time.sleep(random.gauss(0.08, 0.02))

        time.sleep(random.uniform(1, 3))
        page.click('[data-testid="tweetButton"]')
        time.sleep(random.uniform(3, 5))

        # Save cookies for next session
        cookies = context.cookies()
        if cookies_file:
            with open(cookies_file, 'w') as f:
                json.dump(cookies, f)

        browser.close()
```

**Option B: GoLogin API + Playwright (Best of Both)**

GoLogin has an API that lets you programmatically launch browser profiles. This means agents can:
1. Start a GoLogin profile via API (gets the unique fingerprint)
2. Connect Playwright to the running profile via CDP (Chrome DevTools Protocol)
3. Post through the profile with full fingerprint protection

```python
# GoLogin API integration (requires GoLogin Pro)
# Docs: https://docs.gologin.com/api

import requests

GOLOGIN_API = "https://api.gologin.com"
GOLOGIN_TOKEN = os.environ.get("GOLOGIN_API_TOKEN")

def start_profile(profile_id):
    """Start a GoLogin browser profile and return connection URL."""
    headers = {"Authorization": f"Bearer {GOLOGIN_TOKEN}"}
    resp = requests.get(
        f"{GOLOGIN_API}/browser/{profile_id}/start",
        headers=headers
    )
    data = resp.json()
    return data["wsUrl"]  # WebSocket URL for Playwright CDP connection

def connect_and_post(ws_url, tweet_text):
    """Connect Playwright to running GoLogin profile and post."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        page = context.pages[0]
        # ... post tweet using same logic as above
```

**Option C: AdsPower Local API (Free Tier Compatible)**

AdsPower exposes a local API at `http://local.adspower.net:50325`. This lets agents launch profiles programmatically even on the free tier.

```python
# AdsPower Local API
# Docs: https://localapi-doc-en.adspower.com/

import requests

ADSPOWER_API = "http://local.adspower.net:50325"

def start_adspower_profile(profile_id):
    """Launch an AdsPower browser profile."""
    resp = requests.get(f"{ADSPOWER_API}/api/v1/browser/start?user_id={profile_id}")
    data = resp.json()
    if data["code"] == 0:
        ws_url = data["data"]["ws"]["puppeteer"]
        return ws_url
    raise Exception(f"Failed to start profile: {data['msg']}")

def stop_adspower_profile(profile_id):
    """Close an AdsPower browser profile."""
    requests.get(f"{ADSPOWER_API}/api/v1/browser/stop?user_id={profile_id}")
```

### Wiring the Warmup Poster to Use Correct Profile

The existing `AUTOMATIONS/twitter_warmup_poster.py` needs a profile mapping. Add this config:

```python
# Add to twitter_warmup_poster.py or a separate config file

ACCOUNT_PROFILES = {
    "PRINTMAXXER": {
        "method": "personal_browser",  # No antidetect, uses VPN
        "proxy": "vpn_proton_us_east",
        "cookies": "SECRETS/cookies/tw_printmaxxer.json"
    },
    "growthpilled": {
        "method": "adspower",
        "profile_id": "ADSPOWER_PROFILE_2_ID",
        "proxy": "webshare_1",
        "cookies": "SECRETS/cookies/tw_growthpilled.json"
    },
    "outboundtwts": {
        "method": "adspower",
        "profile_id": "ADSPOWER_PROFILE_3_ID",
        "proxy": "webshare_2",
        "cookies": "SECRETS/cookies/tw_outboundtwts.json"
    },
    # ... etc for each account
}

def get_posting_method(account_handle):
    """Return the correct posting method and config for an account."""
    config = ACCOUNT_PROFILES.get(account_handle)
    if not config:
        raise ValueError(f"No profile config for {account_handle}")
    return config
```

### Cookie Management for Scraper Integration

The twitter scraper (`AUTOMATIONS/twitter_alpha_scraper.py`) uses Brave browser cookies. This is separate from posting cookies. Keep them separate:

```
SECRETS/cookies/
  tw_printmaxxer.json       -- Posting cookies for @PRINTMAXXER
  tw_growthpilled.json      -- Posting cookies for @growthpilled
  tw_outboundtwts.json      -- Posting cookies for @outboundtwts
  tw_clipvault.json         -- Posting cookies for @clipvault_
  tw_toolstwts.json         -- Posting cookies for @toolstwts
  tw_scraper_brave.json     -- Scraping cookies (Brave browser, separate account)
  tt_printmaxx.json         -- TikTok posting cookies
```

**Cookie refresh protocol:**
1. Every 7 days, open each antidetect profile manually
2. Browse for 2-3 minutes (keeps session alive)
3. The antidetect browser auto-saves updated cookies
4. If using Playwright with cookie files: export cookies after each session

**Scraper cookies are independent.** The twitter scraper uses a dedicated Brave profile (not an antidetect profile). It monitors 133 accounts. It should never use the same cookies or IP as any posting account.

### Loading Profiles for Human Review

When you need to manually review what an account looks like or do human tasks:

**AdsPower:**
1. Open AdsPower app
2. Find the profile (e.g., `TW_growthpilled`)
3. Click "Open" -- a browser window launches with that profile's fingerprint and proxy
4. You're logged in (cookies persist)
5. Do your review, post, whatever
6. Close the browser -- session auto-saves

**GoLogin:**
1. Open GoLogin app
2. Find the profile
3. Click "Run" -- same as above
4. For cloud profiles: Click "Run in Cloud" -- browser runs on GoLogin's server, you get a stream

**Keyboard shortcut tip:** Both AdsPower and GoLogin let you set keyboard shortcuts to switch between profiles. Set these up if you're managing 5+ profiles daily.

### Agent Scheduling Integration

The existing cron system can trigger automated posting through antidetect profiles:

```bash
# In AUTOMATIONS/crontab_printmaxx.txt, the warmup poster already runs:
# 0 9,13,17 * * * cd $BASE && python3 AUTOMATIONS/twitter_warmup_poster.py --post

# To extend this to multiple accounts:
# Each account gets its own cron entry with a staggered time
0 9 * * *  cd $BASE && python3 AUTOMATIONS/twitter_warmup_poster.py --post --account PRINTMAXXER
15 9 * * * cd $BASE && python3 AUTOMATIONS/twitter_warmup_poster.py --post --account growthpilled
30 9 * * * cd $BASE && python3 AUTOMATIONS/twitter_warmup_poster.py --post --account outboundtwts
45 9 * * * cd $BASE && python3 AUTOMATIONS/twitter_warmup_poster.py --post --account clipvault
0 10 * * * cd $BASE && python3 AUTOMATIONS/twitter_warmup_poster.py --post --account toolstwts
```

**Stagger posting times by 15 minutes.** Posting from 5 accounts at the exact same second is a red flag.

### Full Integration Architecture

```
                    INTELLIGENCE ROUTER
                    (queries before posting)
                           |
                           v
                    TWITTER WARMUP POSTER
                    (enforces rate limits per account)
                           |
              +------------+-------------+
              |            |             |
              v            v             v
         @PRINTMAXXER  @growthpilled  @clipvault_
         (VPN + Safari) (AdsPower #2)  (AdsPower #4)
              |            |             |
              v            v             v
         ProtonVPN     Webshare #1    Webshare #3
         US East       (ISP Static    (ISP Static
                        when upgraded)  when upgraded)
              |            |             |
              v            v             v
         twitter.com   twitter.com   twitter.com
         (unique IP)   (unique IP)   (unique IP)
         (unique FP)   (unique FP)   (unique FP)

    Same content queue → Different posting times → Different IPs → Different fingerprints
    = Looks like 5 independent humans posting organic content
```

---

## QUICK REFERENCE: EMERGENCY PROCEDURES

### If an Account Gets Suspended

1. STOP all automation for that account immediately
2. Do NOT try to log in from a different profile or IP
3. Open the SAME antidetect profile that was used for that account
4. Appeal through Twitter's official appeal form
5. Be polite. Claim misunderstanding. NEVER mention automation.
6. If appeal denied: account is dead. Do NOT create a new account with the same email, phone, or IP.
7. Update SECRETS/created_accounts.json with status: SUSPENDED
8. Reallocate that proxy IP -- it may be flagged. Get a fresh one.

### If Multiple Accounts Get Suspended Simultaneously

This means your accounts got linked. Find the leak:
1. Check if any accounts shared a proxy IP (they shouldn't have)
2. Check if any accounts shared a phone number
3. Check if any accounts interacted with each other (follows, DMs, replies)
4. Check if you logged into multiple accounts from the same browser profile
5. Check if your antidetect fingerprints were too similar (same canvas, same WebGL)
6. Fix the leak before creating replacement accounts

### If a Proxy Gets Flagged

1. Stop using that proxy for social accounts immediately
2. Log into the account from a DIFFERENT proxy (same antidetect profile, just swap the proxy)
3. After swapping: browse normally for 30 minutes before posting
4. Monitor for 48 hours
5. If the account keeps getting restricted: the account itself is flagged, not just the proxy

---

## FILES REFERENCED IN THIS GUIDE

| File | What It Contains |
|------|------------------|
| `OPS/ACCOUNT_STACK_ASSIGNMENTS.md` | All 13 accounts with exact tool/proxy assignments |
| `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` | Platform-specific warmup protocols (21-30 days) |
| `OPS/TECH_INFRA_SETUP_RETARDMAXXED.md` | Tier-based tech stack with setup walkthroughs |
| `OPS/TECH_STACK_SIGNUP_URLS.md` | All signup URLs organized by tier |
| `OPS/SECURITY_ARCHITECTURE_PRINTMAXX.md` | Credential isolation, security hardening |
| `OPS/BROWSER_AUTOMATION_SETUP.md` | Playwright/Selenium/browser-use setup |
| `AUTOMATIONS/twitter_warmup_poster.py` | Automated warmup-safe posting |
| `SECRETS/CREDENTIALS.env` | All account credentials (gitignored) |
| `SECRETS/created_accounts.json` | Account creation tracker |
| `CONTENT/social/TWITTER_PROFILE_SPEC.md` | @PRINTMAXXER profile spec |
| `MEDIA/generated_images/twitter_banner.png` | @PRINTMAXXER banner (ready to upload) |
| `MEDIA/generated_images/twitter_pfp.png` | @PRINTMAXXER profile photo (ready to upload) |

---

**This guide is the single source of truth for multi-account infrastructure. Update it when you change providers, add accounts, or discover new detection vectors.**
