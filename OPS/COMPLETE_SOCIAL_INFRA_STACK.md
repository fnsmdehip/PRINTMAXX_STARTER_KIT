# COMPLETE SOCIAL INFRASTRUCTURE STACK
Updated: 2026-04-17 | Sources: 3 research agents + master ops xlsx + 200+ existing guides

---

## BUDGET TIER SUMMARY (pick your level, follow the stack)

| Tier | Monthly | What you get |
|------|---------|-------------|
| **$0** | $0 | 5-10 accounts, manual management, free tools only |
| **STARTER** | ~$50/mo | 15-20 accounts, basic automation, decent proxies |
| **GROWTH** | ~$150/mo | 30-50 accounts, cloud phones for TikTok, full automation |
| **SCALE** | ~$300/mo | 50-100+ accounts, premium everything, agency-grade |
| **PREMIUM** | ~$600+/mo | Unlimited, mobile proxies, Multilogin, full pipeline |

---

## 1. ANTI-DETECT BROWSERS

**Full comparison:** `OPS/ANTIDETECT_BROWSER_MARKET_COMPARISON_2026.md` (280 lines, 14 browsers)

| Budget | Pick | Why | Profiles |
|--------|------|-----|----------|
| $0 | **ixBrowser** | Unlimited profiles free, full fingerprinting | Unlimited |
| $0 alt | **Dolphin Anty** | 5 free profiles with Cookie Robot warmup | 5 |
| $25 | **GoLogin** | 100 profiles, Android app, cloud sync, API | 100 |
| $50 | **GoLogin** or **Dolphin Anty** | 300 profiles, warmup automation | 300 |
| $100 | **Multilogin X** | Gold-standard fingerprinting + cloud phones | 100 |
| $200+ | **Multilogin X Scale** | 10K profiles, unlimited seats, built-in proxies | 10,000 |

**For TikTok specifically:** Desktop anti-detect is NOT enough. TikTok detection is mobile-native. You need cloud phones:
- **GeeLark** -- purpose-built TikTok cloud phones, ~$25/phone/mo, free tier (2 profiles)
- **Multilogin cloud phones** -- real ARM Android devices, from €1.99
- **MoreLogin** -- 2 free cloud phones on free tier

**Existing playbook:** `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` (717 lines)

---

## 2. PROXIES

**Full comparison:** `OPS/alpha_research/CONTAINERIZED_ACCOUNTS_INFRASTRUCTURE_2026-04-17.md`

### Residential Proxies (for social media browsing)
| Provider | Price | Speed | Social Media OK? | Notes |
|----------|-------|-------|-------------------|-------|
| **Decodo (Smartproxy)** | $3.50/GB PAYG | 0.63s | YES | Best overall. In your master ops ($7/mo listed) |
| **Webshare** | $1.40/GB (50% promo active) | Good | YES | Budget king |
| **PacketStream** | $1/GB | Variable | YES | Cheapest per GB |
| **IPRoyal** | $1.75/GB | Good | YES | Good value mid-tier |
| **Bright Data** | $5.04/GB | Fast | YES | Enterprise, most features |
| **922 S5** | $0.04/IP (unmetered) | Good | YES | Buy IPs not bandwidth, different model |

### Mobile 4G/5G Proxies (ESSENTIAL for TikTok)
| Provider | Price | Bandwidth | Why |
|----------|-------|-----------|-----|
| **ProxyLTE** | $25/port/mo | Unlimited | Best for long sessions, cheapest mobile |
| **TheSocialProxy** | $89/port/mo | Unlimited | Built specifically for social media |
| **AirProxy** | $90/port/mo | Unlimited | Italy-only, good EU coverage |
| **Proxy-Cheap mobile** | ~$50/port/mo | Varies | Budget mobile option |

**Strategy:** Residential for X/LinkedIn/Reddit/Pinterest. Mobile 4G for TikTok/Instagram.

**Existing in your stack:** Decodo already in master ops LEAD GEN sheet at $7/mo.

---

## 3. VIRTUAL PHONE / SMS VERIFICATION

**Critical update:** SMS-Activate shut down March 2026.

| Service | Cost | Best for | Success rate |
|---------|------|----------|-------------|
| **VerifySMS** | Varies | WhatsApp/high-security platforms | 96% |
| **5sim** | $0.008-$0.50/code | Bulk cheap verifications | Good |
| **TextVerified** | $0.25+ | Non-VoIP US numbers (best for TikTok) | High |
| **Hushed** | $5/mo | Persistent US numbers (3 numbers) | Good |
| **MySudo** | $5/mo | Privacy-focused, 3 numbers | Good |
| **TextNow** | Free | Basic US number | 50-60% (declining) |
| **Google Voice** | Free | Backup number | 50-60% (declining) |

**For TikTok:** Free VoIP numbers (TextNow, Google Voice) are increasingly blocked. Use **TextVerified** (non-VoIP) or **5sim** for one-time verification.

**Strategy:**
- Primary accounts: Real phone or Hushed/MySudo ($5/mo)
- Scale accounts: 5sim for one-time codes ($0.05-0.50 each)
- Don't reuse numbers across accounts

---

## 4. EMAIL CONTAINERIZATION

| Service | Cost | Aliases | Send from alias? | Best for |
|---------|------|---------|------------------|----------|
| **Cloudflare Email Routing** | FREE | Unlimited catch-all | NO (receive only) | Maximum scale at $0 |
| **SimpleLogin** | $2.50/mo (or free w/ Proton) | Unlimited | YES | Reply from aliases |
| **Proton Mail Plus** | $4/mo | 10 + catch-all | YES | Privacy + sending |
| **Tuta Mail** | $3/mo | Unlimited custom domain | YES | Underrated value |
| **Zoho Mail** | Free (5 users) | 5 emails | YES | Free business email |
| **Google Workspace** | $6/mo | 30 aliases | YES | Cold email + deliverability |

**Strategy:** Cloudflare catch-all domain ($10/yr domain + $0 email) for receiving. SimpleLogin or Proton for sending. One unique email per social account.

**Existing:** `09_LEGAL/email_compliance/` has CAN-SPAM, GDPR, B2B/B2C templates.

---

## 5. COLD EMAIL & OUTREACH

| Tool | Cost | Emails/day | Best for |
|------|------|-----------|----------|
| **Instantly.ai** | $30/mo | 50/day/mailbox, unlimited mailboxes | Volume cold email |
| **Smartlead** | $39/mo | Agency features, unlimited mailboxes | Teams/agencies |
| **Lemlist** | $39/mo | Personalization, multichannel | High-touch outreach |
| **Bland AI** | 100 FREE calls/day | N/A | AI voice calls + appointment setting |
| **Apollo.io** | 50 credits/mo free | Varies | Lead database + email finding |
| **Hunter.io** | 25 searches/mo free | N/A | Email finding |
| **Clay** | Free tier | N/A | Data enrichment, waterfall search |

**Your existing tools:** savvy_lead_scraper.py (1,656 lines), nationwide_scraper.py (880 lines), mass_outreach.py (732 lines) -- all built and ready.

**Existing playbooks:**
- `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES_TIER1.md` -- elite sequences (>10% reply rate tactics)
- `MONEY_METHODS/COLD_OUTBOUND/AUSTIN_LOCAL_BIZ_COLD_EMAIL_SEQUENCES.md` -- 9 industries
- `03_PLAYBOOKS/COLD_OUTBOUND/COLD_DM_TEMPLATES_ALL_NICHES.md` -- 2,491 lines, 33 niches
- `03_PLAYBOOKS/COLD_OUTBOUND/research/DELIVERABILITY_2026.md`
- `03_PLAYBOOKS/COLD_OUTBOUND/research/WARM_UP_PROTOCOLS.md`
- `EMAIL/sequences/` -- 5 ready sequences
- `04_CONTENT/longtail_pages/instantly-vs-smartlead-vs-lemlist-cold-email-tools-compared-2026.md`

---

## 6. LINKEDIN AUTOMATION

| Tool | Cost | Ban risk | Best for |
|------|------|----------|----------|
| **Linked Helper** | $15/mo | Low (local) | Budget, safest |
| **Dripify** | $39/mo | Medium | Ease of use, sequences |
| **Waalaxy** | $56/mo | Medium | Multi-channel (email + LinkedIn) |
| **Expandi** | $99/mo | Low (cloud) | Scale, smart limits |
| **Zopto** | $215/mo | Low | Agency scale |

**Safe limits:** 15-20 connection requests/day (free), 30-50 (Sales Navigator). New accounts start at 25% of these. 23% of automation users face restrictions within 90 days regardless of tool.

**Existing playbooks:**
- `03_PLAYBOOKS/COLD_OUTBOUND/linkedin/AUTOMATION_SAFE.md`
- `03_PLAYBOOKS/COLD_OUTBOUND/lead_gen/LINKEDIN_SCRAPING.md`
- `CONTENT/growth/buildout/N_series/linkedin_automation.md`
- `OPS/DM_FUNNEL_AND_MONETIZATION_PLAN.md` (662 lines)
- `CONTENT/LINKEDIN_POSTS_30.md` -- 30 posts ready

---

## 7. SOCIAL SCHEDULING & MULTI-PLATFORM MANAGEMENT

**Full comparison:** `OPS/alpha_research/SOCIAL_MEDIA_AUTOMATION_STACK_2026-04-17.md`

| Tool | Cost | Platforms | Accounts | iPhone app? | Reddit? |
|------|------|-----------|----------|-------------|---------|
| **Buffer** | $6/channel | 8 platforms | 1 per channel | YES (best) | No |
| **Publer** | $12/mo | 9 platforms | 5-500 | YES | No |
| **Vista Social** | $15/mo | 14 platforms | 8 | YES | YES |
| **Metricool** | $18/mo | 9 platforms | 5 | YES | No |
| **SocialBee** | $29/mo | 8 platforms | 5-150 | YES | No |
| **SocialPilot** | $30/mo | 9 platforms | 10-unlimited | YES | No |
| **Later** | $25/mo | 6 platforms | 1 per | YES | No |
| **Hootsuite** | $99/mo | 8 platforms | 10 | YES | No |

**Winner by budget:**
- $0: Buffer free (3 channels) + TikTok Studio + YouTube Studio + Meta Business Suite
- $12: **Publer** -- best value, TikTok + all major platforms
- $30: **SocialPilot** -- 50+ accounts on Ultimate
- $15: **Vista Social** -- only one with Reddit scheduling

**Existing in your stack:** Buffer CSVs prepared (`LEDGER/buffer_import_*.csv`, 12 files), posting queue (1,588 files)

---

## 8. TIKTOK-SPECIFIC TOOLS

**TikTok is the hardest platform.** Key facts:
- Official API cap: 15-20 posts/day per account
- Fingerprint detection: 100+ parameters
- Posting on Day 1 = near-guaranteed shadowban
- Full warmup: 3 weeks minimum (Week 1 = zero posting, browse + engage only)

| Tool | Cost | What it does |
|------|------|-------------|
| **GeeLark** | Free (2) / $25/phone/mo | Cloud phones for TikTok (ESSENTIAL) |
| **Publer** | $12/mo | TikTok scheduler |
| **Pentos** | Free tier | TikTok analytics + competitor tracking |
| **TokPortal** | Varies | TikTok API management |
| **TikBuddy** | Free tier | TikTok analytics |
| **CapCut** | Free | Video editing (owned by ByteDance) |
| **PiPiADS** | $77/mo | TikTok ad spy (see winning ads) |

**Existing playbooks:**
- `CONTENT/social/TIKTOK_LAUNCH_SCRIPTS.md` -- 5 scripts
- `CONTENT/social/TIKTOK_VIRAL_STRATEGY_2026.md`
- `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` (TikTok section)
- `CONTENT/growth/buildout/G01_G15_growth/multi_account_warmup.md`

---

## 9. CONTENT REPURPOSING PIPELINE

**Goal:** 1 piece of content -> all platforms automatically.

| Tool | Cost | What it does |
|------|------|-------------|
| **CapCut** | Free | Edit video, add captions, transitions |
| **Opus Clip** | $15/mo | Auto-clip long videos into shorts |
| **Vidyo.ai** | $30/mo | AI video repurposing |
| **Repurpose.io** | $25/mo | Auto cross-post: TikTok -> IG Reels -> YT Shorts -> X |
| **Descript** | $24/mo | Audio/video editing, transcription |
| **Headliner** | Free tier | Audiograms, video clips |
| **AutoFaceless.ai** | ~$100/mo | Daily faceless video generation |

**The $0 pipeline:** Write script -> CapCut (free) -> Post manually to each platform
**The $50 pipeline:** Script -> CapCut -> Opus Clip ($15) -> Repurpose.io ($25) -> auto-distributes everywhere
**The $100 pipeline:** Add Publer ($12) for scheduling + Metricool ($18) for analytics + Pentos for TikTok

**Existing in your stack:**
- Kling AI (66 free credits/day), Remotion (free), Suno (10 songs/day free)
- ElevenLabs ($5/mo for voice), Leonardo.ai (150 tokens/day free)
- CapCut (free), HeyGen ($29/mo for avatars)
- `AUTOMATIONS/auto_clip_pipeline.py` -- built and ready
- `CONTENT/AI_UGC_VIDEO_SCRIPTS.md` -- 10 scripts ready

---

## 10. UGC, CLIPPING & AD SPY TOOLS

### UGC Creation
| Tool | Cost | Notes |
|------|------|-------|
| **HeyGen** | $29/mo | AI avatar videos |
| **Kling AI** | 66 free credits/day | Video gen, product videos |
| **Nano Banana** | $9.99/mo | AI persona consistency |
| **Arcads** | Varies | AI UGC ads at scale |
| **Creatify** | $36/mo | AI ad generation from URL |

### Clipping
| Tool | Cost | Notes |
|------|------|-------|
| **Opus Clip** | $15/mo | Best for long -> short |
| **CapCut** | Free | Manual clipping + auto captions |
| **Munch** | $49/mo | AI clip selection |
| **Pictory** | $23/mo | Script-to-video |
| **VontenRewards** | Free | Pay clippers per 1K views (in your master ops) |

### Ad Spy
| Tool | Cost | Notes |
|------|------|-------|
| **PiPiADS** | $77/mo | TikTok ad spy |
| **Minea** | $49/mo | Multi-platform (TikTok, FB, Pinterest) |
| **BigSpy** | Free tier | Cross-platform ad library |
| **AdSpy** | $149/mo | Facebook/Instagram focused |
| **Meta Ad Library** | Free | Facebook official ad transparency |

### Affiliate Link Management
| Tool | Cost | Notes |
|------|------|-------|
| **ThirstyAffiliates** | Free WP plugin | Link cloaking + tracking |
| **Pretty Links** | Free WP plugin | Short links + tracking |
| **Voluum** | $199/mo | Full affiliate tracker |
| **RedTrack** | $83/mo | Attribution + tracking |
| **ClickMagick** | $12/mo | Click tracking, link rotators |

**Existing in master ops:** Xreacher + DMpro (Twitter DM tools), SparkLoop (newsletter referrals), Swapstack (newsletter sponsorships)

---

## 11. GROWTH & EDGE TACTICS

**Existing playbooks (this is where PRINTMAXX is richest):**
- `OPS/GREY_HAT_EDGE_GROWTH_MASTER.md` -- **8,461 lines** of edge tactics
- `OPS/DEFINITIVE_GROWTH_STACK.md` -- full toolkit
- `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md` -- legal analysis per tactic
- `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md`
- `CONTENT/growth/buildout/G01_G15_growth/grey_hat_legal.md` -- ALLOWED/RISKY/ILLEGAL status per tactic
- `AUTOMATIONS/edge_growth_engine.py` -- automated growth engine

---

## RECOMMENDED STACKS BY BUDGET

### $0/mo -- BOOTSTRAPPING
| Layer | Tool | Cost |
|-------|------|------|
| Anti-detect | ixBrowser (unlimited) | $0 |
| Proxy | None (home IP + VPN) | $0 |
| Phone | TextNow (1 number) | $0 |
| Email | Cloudflare catch-all | $0 (need $10/yr domain) |
| Scheduling | Buffer free (3 channels) | $0 |
| Video | CapCut | $0 |
| Outreach | Bland AI (100 calls/day free) | $0 |
| LinkedIn | Manual | $0 |
| **Total** | **5-10 accounts, manual** | **$0/mo** |

### $50/mo -- STARTER
| Layer | Tool | Cost |
|-------|------|------|
| Anti-detect | GoLogin (100 profiles) | $24 |
| Proxy | Webshare residential 2GB | $3 |
| Phone | Hushed (3 numbers) + 5sim for bulk | $7 |
| Email | Cloudflare + SimpleLogin | $2.50 |
| Scheduling | Publer (9 platforms, 5 accounts) | $12 |
| Video | CapCut (free) | $0 |
| Outreach | Apollo free + Bland AI free | $0 |
| LinkedIn | Linked Helper | $0 (use GoLogin profiles) |
| **Total** | **15-20 accounts** | **~$49/mo** |

### $150/mo -- GROWTH
| Layer | Tool | Cost |
|-------|------|------|
| Anti-detect | GoLogin 300 profiles | $49 |
| Cloud phones | GeeLark (3 TikTok phones) | $25 |
| Proxy residential | Decodo 5GB | $18 |
| Proxy mobile | ProxyLTE (2 ports for TikTok) | $50 |
| Phone | Hushed + 5sim | $7 |
| Email | Proton Plus + catch-all | $4 |
| Scheduling | SocialPilot (10 accounts) | $30 |
| Cold email | Instantly.ai | $30 |
| Video | CapCut + Opus Clip | $15 |
| LinkedIn | Dripify | $39 |
| Repurpose | Repurpose.io | $25 |
| **Total** | **30-50 accounts, full automation** | **~$292/mo** |

Trim: drop Dripify (-$39), drop Repurpose.io (-$25), drop 1 ProxyLTE port (-$25) = **~$148/mo**

### $300/mo -- SCALE
| Layer | Tool | Cost |
|-------|------|------|
| Anti-detect | Multilogin X Team (100 profiles + cloud phones) | $100 |
| Cloud phones | GeeLark (5 TikTok phones) | $42 |
| Proxy residential | Decodo 10GB | $35 |
| Proxy mobile | TheSocialProxy (1 port unlimited) | $89 |
| Phone | Hushed + 5sim bulk | $10 |
| Email | Proton + SimpleLogin | $7 |
| Scheduling | SocialPilot Ultimate (50+ accounts) | $60 |
| Cold email | Instantly.ai Growth | $58 |
| Video | CapCut + Opus Clip + HeyGen | $44 |
| LinkedIn | Dripify + Sales Nav | $120 |
| Ad spy | PiPiADS | $77 |
| Repurpose | Repurpose.io | $25 |
| Analytics | Pentos (TikTok) + Metricool | $18 |
| **Total** | **50-100+ accounts, agency-grade** | **~$685/mo** |

Pick and choose -- you don't need everything at once.

---

## CROSS-REFERENCE: YOUR 200+ EXISTING GUIDES

Everything above connects to guides you already have. Key index:

| Topic | Your existing guide | New research |
|-------|--------------------|-------------|
| Anti-detect | `OPS/ANTIDETECT_MOBILE_MANAGEMENT.md` | `OPS/ANTIDETECT_BROWSER_MARKET_COMPARISON_2026.md` |
| Proxies | Master ops LEAD GEN sheet (Decodo entry) | `OPS/alpha_research/CONTAINERIZED_ACCOUNTS_INFRASTRUCTURE_2026-04-17.md` |
| Warmup | `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` (717 lines) | Integrated above |
| Cold email | `MONEY_METHODS/COLD_OUTBOUND/` (5+ files) | Tool comparison added |
| LinkedIn | `03_PLAYBOOKS/COLD_OUTBOUND/linkedin/` | Safety data + tool pricing |
| TikTok | `CONTENT/social/TIKTOK_VIRAL_STRATEGY_2026.md` | `OPS/alpha_research/SOCIAL_MEDIA_AUTOMATION_STACK_2026-04-17.md` |
| Content farm | `03_PLAYBOOKS/CONTENT_FARM/` (5 niche playbooks) | Repurposing pipeline added |
| Growth hacking | `OPS/GREY_HAT_EDGE_GROWTH_MASTER.md` (8,461 lines) | Already comprehensive |
| DM outreach | `03_PLAYBOOKS/COLD_OUTBOUND/COLD_DM_TEMPLATES_ALL_NICHES.md` (2,491 lines) | Added Xreacher/DMpro |
| Email sequences | `EMAIL/sequences/` + `03_PLAYBOOKS/INFO_PRODUCTS/EMAIL_SEQUENCES_ALL_NICHES.md` (3,437 lines) | Already comprehensive |
| Fiverr/Upwork | `03_PLAYBOOKS/AGENCY_SERVICES/FIVERR_GIGS_ALL_NICHES.md` (2,275 lines) | Already comprehensive |
| Video/media | Master ops VIDEO & MEDIA sheet (27 tools) | UGC + clipping tools added |
| Legal | `09_LEGAL/` (24 templates) + `CONTENT/growth/buildout/G01_G15_growth/grey_hat_legal.md` | Already comprehensive |

---

## START HERE (same as MASTER_LAUNCH_PLAYBOOK.md)

1. Create accounts (OPS/ACCOUNT_CREATION_CHECKLIST.md) -- 2-3 hours
2. Set up anti-detect + proxy stack at your budget tier -- 1-2 hours
3. Create social accounts in GoLogin profiles -- 1 hour
4. Start warmup (3 weeks for TikTok, 1 week for others)
5. While warming up: list Gumroad products, send cold emails, post on warmed accounts
6. Week 4: full content distribution across all platforms
