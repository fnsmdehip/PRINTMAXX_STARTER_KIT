# MASTER LAUNCH PLAYBOOK -- From $0 to Revenue
Updated: 2026-04-17 | The ONLY doc you need to follow. Everything else is reference.

This connects ALL the guides, playbooks, templates, and tools already built. Follow it top to bottom.

---

## PHASE 0: INFRA SETUP (2-3 hours, one-time)

### Step 0A: Accounts (see OPS/ACCOUNT_CREATION_CHECKLIST.md)
Do ALL of these first. Nothing works without them.

| # | Account | Time | Guide |
|---|---------|------|-------|
| 1 | Surge.sh login fix | 5 min | `OPS/ACCOUNT_CREATION_CHECKLIST.md` |
| 2 | Gumroad | 15 min | `OPS/GUMROAD_SPEED_UPLOAD.md` |
| 3 | Whop | 15 min | whop.com/sell |
| 4 | Fiverr | 20 min | `MONEY_METHODS/FREELANCE/fiverr_gigs/` |
| 5 | Upwork | 15 min | `MONEY_METHODS/FREELANCE/upwork_proposals/` |
| 6 | X/@PRINTMAXXER finalize | 10 min | `CONTENT/social/TWITTER_PROFILE_SPEC.md` |
| 7 | Affiliate programs (5) | 30 min | `OPS/AFFILIATE_LINK_SETUP.md` |
| 8 | Tailscale | 5 min | `MOBILE_CONTROL_PLAYBOOK.md` |
| 9 | Email domain + Instantly | 30 min | Below |

### Step 0B: Anti-Detect + Proxy + Virtual Phone Stack
**Guide:** `OPS/ANTIDETECT_MOBILE_MANAGEMENT.md`
**Warmup guide:** `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md`
**Safe automation:** `OPS/SAFE_WARMUP_AUTOMATION_GUIDE.md`
**Device matrix:** `LEDGER/WARMUP_DEVICE_MATRIX.csv`

| Tool | Action | Budget |
|------|--------|--------|
| GoLogin | Sign up, install Mac + iPhone apps, create 15 profiles | $49/mo (100 profiles) |
| Smartproxy | Sign up, get residential proxies, assign 1 per profile | $12/mo (2GB) |
| Hushed/MySudo | Get 3-5 virtual phone numbers | $5-15/mo |
| Proton Mail Plus | Set up catch-all domain for unlimited emails | $4/mo |
| TextNow | Free backup number | $0 |

**Total infra cost: ~$70-80/mo** (covers unlimited account containerization)

### Step 0C: Social Account Creation (use anti-detect stack)
Create accounts in GoLogin profiles. Each gets unique fingerprint + proxy + phone + email.

| Platform | Accounts | Purpose | Warmup Guide |
|----------|----------|---------|-------------|
| X/Twitter | 13 (1 per brand/niche) | Content distribution | `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` |
| Reddit | 5-10 | Engagement + traffic | `OPS/REDDIT_ACCOUNT_WARMUP_SOP.md` |
| LinkedIn | 2-3 | B2B outreach + content | Personal + business profiles |
| Pinterest | 3 | Affiliate traffic | Business accounts |
| TikTok | 3-5 | Short-form content | `CONTENT/social/TIKTOK_VIRAL_STRATEGY_2026.md` |
| Instagram | 3-5 | Visual content | Auto-post from content queue |

**Warmup schedule per platform:**
- **X/Twitter:** Days 1-5 browse/like only. Days 6-10 replies only. Day 11+ post original content. `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md`
- **Reddit:** 2 weeks of genuine commenting before any self-promo. `OPS/REDDIT_ACCOUNT_WARMUP_SOP.md`
- **LinkedIn:** Normal usage, no automation for first week
- **Pinterest:** Pin 5-10 curated pins/day for first week before own content

---

## PHASE 1: FIRST REVENUE (Week 1 -- do these the SAME DAY accounts are created)

### 1A: List Digital Products (30-60 min)
**Gumroad:** Upload 13+ products from `GUMROAD_INSTANT_UPLOAD/`
**Whop:** Cross-list top sellers ($27+ products)
**Listings pre-written:** `DIGITAL_PRODUCTS/ready_to_sell/LISTING_*.md`
**All PDFs ready:** `DIGITAL_PRODUCTS/ready_to_sell/pdfs/`

### 1B: Replace Affiliate Placeholder IDs (15 min)
Run: `python3 AUTOMATIONS/payment_integrator.py --replace-placeholders`
**Pages affected:** 13 comparison/review pages with live traffic potential
**Full list:** `OPS/AFFILIATE_LINK_SETUP.md`

### 1C: Send Cold Emails (1 hour)
**54 emails pre-drafted.** 21 hot leads with real contact info.
**Email sequences:** `EMAIL/sequences/` (5 sequences ready)
- `launch_sequence.md` -- for product launches
- `welcome_sequence.md` -- for new subscribers
- `local_biz_followup_sequence.md` -- for local biz outreach
- `reengagement_sequence.md` -- for cold leads
**Cold outbound playbooks:**
- `MONEY_METHODS/COLD_OUTBOUND/TIER1_COLD_EMAIL_SEQUENCES.md`
- `MONEY_METHODS/COLD_OUTBOUND/AUSTIN_LOCAL_BIZ_COLD_EMAIL_SEQUENCES.md`
- `MONEY_METHODS/COLD_OUTBOUND/LOCAL_BIZ_WEBSITE_SERVICE.md`
**Priority send list:** `OPS/SEND_NOW_PRIORITY_EMAILS.md`

### 1D: List Fiverr Gigs (30 min)
**10 gig descriptions ready.** Price low for first 5 reviews.
**Service packages:** `OPS/SERVICE_OFFERING_PACKAGES.md`

### 1E: Publish First 50 Content Pieces
**1,588 pieces in posting queue.** Start with top-performing formats.
**Content sources:**
- `CONTENT/social/posting_queue/` -- 1,588 ready-to-post files
- `CONTENT/YOUTUBE_SCRIPTS_30.md` -- 30 video scripts
- `CONTENT/REDDIT_POSTS_50.md` -- 50 Reddit posts
- `CONTENT/LINKEDIN_POSTS_30.md` -- 30 LinkedIn posts
- `CONTENT/social/dm_sequences/TWITTER_DM_SCRIPTS_50.md` -- 50 DM scripts
- `CONTENT/social/REPLY_ENGAGEMENT_STRATEGY.md` -- reply templates
- `CONTENT/social/REPLY_TEMPLATES_100.md` -- 100 reply hooks
**Buffer CSVs ready for import:** `LEDGER/buffer_import_*.csv` (12 files, 3 niches x 4 platforms)
**Posting guide:** `CONTENT/social/MANUAL_POSTING_GUIDE_MAR9.md`
**Content factory:** `OPS/CONTENT_FACTORY_PLAYBOOK.md`

---

## PHASE 2: SCALE (Weeks 2-4)

### 2A: Cold Outreach at Volume
**LinkedIn:**
- DM funnel: `OPS/DM_FUNNEL_AND_MONETIZATION_PLAN.md`
- LinkedIn content: `CONTENT/social/linkedin/` + `CONTENT/LINKEDIN_POSTS_30.md`
- Cold outreach templates: `EMAIL/sequences/` + `MONEY_METHODS/COLD_OUTBOUND/`
- EAS packages: `MONEY_METHODS/EAS/` (4 tiers: $1,500 / $3,500 / $4,500 / $1,500-3K/mo)

**Email at scale:**
- Instantly.ai for warmup + sending (30-100/day/mailbox)
- Add 2-3 email domains over first month
- **9 industry cold email sequences built:** `MONEY_METHODS/COLD_OUTBOUND/AUSTIN_LOCAL_BIZ_COLD_EMAIL_SEQUENCES.md`
- **Gov contract outreach:** `EMAIL/GOV_CONTRACT_COLD_EMAIL.md` + `EMAIL/GOV_TENDER_OUTREACH_EMAILS.md`

### 2B: Content Compounding
**Daily targets (from KPI dashboard):**
| Metric | Week 1-2 | Week 3-4 | Month 2+ |
|--------|----------|----------|----------|
| Content published | 3-5/day | 5-10/day | 10-20/day |
| Cold emails sent | 50-100/day | 100-200/day | 200-500/day |
| Freelance proposals | 5-10/day | 10-20/day | 10-20/day |

**Platform-specific tactics:**
- **Twitter/X:** `CONTENT/social/TWITTER_GROWTH_ENGINE.md` + reply strategy from `REPLY_ENGAGEMENT_STRATEGY.md`
- **TikTok:** `CONTENT/social/TIKTOK_LAUNCH_SCRIPTS.md` + `TIKTOK_VIRAL_STRATEGY_2026.md`
- **Reddit:** `CONTENT/REDDIT_POSTS_50.md` + warmup SOP
- **Pinterest:** 17 pins ready (`pinterest/`)

### 2C: Edge Growth (use with caution)
**Master guide (8,461 lines!):** `OPS/GREY_HAT_EDGE_GROWTH_MASTER.md`
**Growth stack:** `OPS/DEFINITIVE_GROWTH_STACK.md`
**Edge tactics:** `CONTENT/social/edge_tactics/` (3 tactical docs)
**Legal playbook:** `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md`
**Growth engine automation:** `AUTOMATIONS/edge_growth_engine.py`

---

## PHASE 3: AUTOMATE + OPTIMIZE (Month 2+)

### 3A: Let the System Take Over
Once accounts exist and content is flowing, the autonomous system handles:
- **Capital Genesis:** Ranks all 8,899 methods, surfaces P0 actions daily
- **Decision Engine:** Routes opportunities to ventures automatically
- **Loop Closer:** Self-corrects pipeline, feedback, and drift
- **Scrapers:** Twitter (133 accounts), Reddit, HN -- feeding alpha 24/7
- **Morning pipeline:** SCAN→PROCESS→RANK→DECIDE→EXECUTE at 5 AM daily

### 3B: Kill/Scale
**Kill triggers:** App <$100 MRR/60d, Content <500 followers/90d, Outbound <2% reply/3 optimizations
**Scale triggers:** App 20%+ growth at $500+, engagement >5% sustained
**Portfolio optimizer:** `python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --optimize`

---

## REFERENCE INDEX -- ALL YOUR GUIDES IN ONE PLACE

### Account & Identity Management
| Guide | Path | Lines |
|-------|------|-------|
| Account Creation Checklist | `OPS/ACCOUNT_CREATION_CHECKLIST.md` | 80 |
| Anti-Detect Mobile Management | `OPS/ANTIDETECT_MOBILE_MANAGEMENT.md` | 200 |
| Ultimate Account Warmup | `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` | 717 |
| Safe Warmup Automation | `OPS/SAFE_WARMUP_AUTOMATION_GUIDE.md` | 671 |
| Reddit Warmup SOP | `OPS/REDDIT_ACCOUNT_WARMUP_SOP.md` | 358 |
| Warmup Device Matrix | `LEDGER/WARMUP_DEVICE_MATRIX.csv` | CSV |
| Twitter Profile Spec | `CONTENT/social/TWITTER_PROFILE_SPEC.md` | — |
| 3-Niche Brand System | `PRODUCTS/branding/PRINTMAXX_3NICHE_BRAND_SYSTEM.md` | — |
| Brand Identity | `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md` | — |

### Cold Email & Outreach
| Guide | Path | Lines |
|-------|------|-------|
| Tier 1 Cold Email Sequences | `MONEY_METHODS/COLD_OUTBOUND/TIER1_COLD_EMAIL_SEQUENCES.md` | — |
| Austin Local Biz Sequences | `MONEY_METHODS/COLD_OUTBOUND/AUSTIN_LOCAL_BIZ_COLD_EMAIL_SEQUENCES.md` | — |
| Local Biz Website Service | `MONEY_METHODS/COLD_OUTBOUND/LOCAL_BIZ_WEBSITE_SERVICE.md` | — |
| Gov Contract Cold Email | `EMAIL/GOV_CONTRACT_COLD_EMAIL.md` | — |
| Gov Tender Outreach | `EMAIL/GOV_TENDER_OUTREACH_EMAILS.md` | — |
| Email Sequences (5) | `EMAIL/sequences/` | 5 files |
| DM Funnel + Monetization | `OPS/DM_FUNNEL_AND_MONETIZATION_PLAN.md` | 662 |
| Service Packages | `OPS/SERVICE_OFFERING_PACKAGES.md` | — |
| Priority Send List | `OPS/SEND_NOW_PRIORITY_EMAILS.md` | — |
| Twitter DM Scripts (50) | `CONTENT/social/dm_sequences/TWITTER_DM_SCRIPTS_50.md` | — |

### Content & Distribution
| Guide | Path | Lines |
|-------|------|-------|
| Content Factory Playbook | `OPS/CONTENT_FACTORY_PLAYBOOK.md` | 333 |
| Twitter Growth Engine | `CONTENT/social/TWITTER_GROWTH_ENGINE.md` | — |
| Reply Strategy | `CONTENT/social/REPLY_ENGAGEMENT_STRATEGY.md` | — |
| Reply Templates (100) | `CONTENT/social/REPLY_TEMPLATES_100.md` | — |
| TikTok Launch Scripts | `CONTENT/social/TIKTOK_LAUNCH_SCRIPTS.md` | — |
| TikTok Viral Strategy | `CONTENT/social/TIKTOK_VIRAL_STRATEGY_2026.md` | — |
| Posting Queue | `CONTENT/social/posting_queue/` | 1,588 files |
| Buffer Import CSVs | `LEDGER/buffer_import_*.csv` | 12 files |
| Manual Posting Guide | `CONTENT/social/MANUAL_POSTING_GUIDE_MAR9.md` | — |
| LinkedIn Posts (30) | `CONTENT/LINKEDIN_POSTS_30.md` | 30 posts |
| YouTube Scripts (30) | `CONTENT/YOUTUBE_SCRIPTS_30.md` | 30 scripts |
| Reddit Posts (50) | `CONTENT/REDDIT_POSTS_50.md` | 50 posts |
| Newsletter Issues (20) | `CONTENT/NEWSLETTER_ISSUES_20.md` | 20 issues |
| AI UGC Video Scripts | `CONTENT/AI_UGC_VIDEO_SCRIPTS.md` | 10 scripts |

### Growth & Edge Tactics
| Guide | Path | Lines |
|-------|------|-------|
| Grey Hat Edge Growth MASTER | `OPS/GREY_HAT_EDGE_GROWTH_MASTER.md` | 8,461 |
| Definitive Growth Stack | `OPS/DEFINITIVE_GROWTH_STACK.md` | 154 |
| Grey Hat Legal Playbook | `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md` | — |
| Edge Growth Tactics | `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` | — |
| Grey Hat Jan 2026 Update | `06_OPERATIONS/growth/GREY_HAT_UPDATE_JAN_2026.md` | — |
| Edge Tactics (3 batches) | `CONTENT/social/edge_tactics/` | 3 files |
| Growth Engine Automation | `AUTOMATIONS/edge_growth_engine.py` | — |

### Money Method Playbooks (30+)
| Method | Path |
|--------|------|
| Cold Outbound | `MONEY_METHODS/COLD_OUTBOUND/` |
| AI Agent Services | `MONEY_METHODS/AI_AGENT_SERVICES/` |
| AI Content Affiliate | `MONEY_METHODS/AI_CONTENT_AFFILIATE/` |
| AI Influencer (NSFW/Findom) | `MONEY_METHODS/AI_INFLUENCER/` |
| App Factory | `MONEY_METHODS/APP_FACTORY/` |
| Automation Agency | `MONEY_METHODS/AUTOMATION_AGENCY/` |
| Community Monetization | `MONEY_METHODS/COMMUNITY/` |
| Content Farm (YouTube) | `MONEY_METHODS/CONTENT_FARM/` |
| Digital Products | `MONEY_METHODS/DIGITAL_PRODUCTS/` |
| EAS (Enterprise Automation) | `MONEY_METHODS/EAS/` |
| E-Commerce Arbitrage | `MONEY_METHODS/ECOM/` + `ECOM_ARB/` |
| Local Business | `MONEY_METHODS/LOCAL_BIZ/` |
| Meta Ads | `MONEY_METHODS/META_ADS_AUTONOMOUS/` |
| Newsletter | `MONEY_METHODS/NEWSLETTER/` |
| Platform Arbitrage | `MONEY_METHODS/PLATFORM_ARBITRAGE/` |
| POD (Print on Demand) | `MONEY_METHODS/POD/` |
| Prompt Marketplace | `MONEY_METHODS/PROMPT_MARKETPLACE/` |
| Skool Community | `MONEY_METHODS/SKOOL_COMMUNITY/` |
| Synergy Packages (17) | `MONEY_METHODS/SYNERGY_PACKAGES/` |

### Legal & Compliance
| Guide | Path |
|-------|------|
| Contracts (5) | `09_LEGAL/contracts/` |
| Email Compliance (4) | `09_LEGAL/email_compliance/` |
| FTC Compliance (5) | `09_LEGAL/ftc_compliance/` |
| Platform Rules (5) | `09_LEGAL/platform_compliance/` |
| Website Policies (5) | `09_LEGAL/website_policies/` |

### Payment & Monetization
| Guide | Path |
|-------|------|
| Payment Integration | `.claude/rules/payment-integration.md` |
| Stripe Products | `OPS/STRIPE_PRODUCTS.md` |
| Gumroad Speed Upload | `OPS/GUMROAD_SPEED_UPLOAD.md` |
| Affiliate Opportunities | `OPS/AFFILIATE_OPPORTUNITIES_MAR08.md` |
| Affiliate Link Setup | `OPS/AFFILIATE_LINK_SETUP.md` |
| First Dollar Action Plan | `OPS/FIRST_DOLLAR_ACTION_PLAN.md` |

### Mobile Control
| Guide | Path |
|-------|------|
| Mobile Control Playbook | `MOBILE_CONTROL_PLAYBOOK.md` |
| Anti-Detect Mobile | `OPS/ANTIDETECT_MOBILE_MANAGEMENT.md` |

### KPIs & Tracking
| Guide | Path |
|-------|------|
| KPI Dashboard | `OPS/KPI_DASHBOARD.md` |
| Capital Genesis Priority Stack | `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` |
| Revenue Pipeline | `FINANCIALS/revenue_pipeline.json` |
| Heartbeat | `OPS/HEARTBEAT.md` |

---

## DAILY KPI CHECKLIST (print this, tape to wall)

| # | Metric | Target | Track How |
|---|--------|--------|-----------|
| 1 | Content published | 5+/day | Count posts across platforms |
| 2 | Cold emails sent | 50+/day | Instantly.ai dashboard |
| 3 | Freelance proposals | 5+/day | Fiverr + Upwork dashboards |
| 4 | Products listed (new) | 1/day first week | Gumroad + Whop dashboards |
| 5 | Revenue today | $X | Stripe dashboard |
| 6 | Leads generated | 5+/day | Email signups + DMs |
| 7 | System health | Check 1x/day | Telegram bot `/health` or dashboard |
| 8 | Alpha processed | Auto (50-100/day) | `python3 AUTOMATIONS/alpha_auto_processor.py --process-new` |

---

## THE ONE THING

Everything above is built. 2,277 content pieces. 13 products. 54 emails. 1,588 posts in queue. 30+ playbooks. The system has been running for 58 days building assets.

**The only thing between $0 and revenue is creating accounts and pressing "publish."**

Start with Step 0A. Do it now. Everything after that is follow-the-playbook.
