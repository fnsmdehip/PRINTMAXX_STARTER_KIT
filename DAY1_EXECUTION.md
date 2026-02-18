# PRINTMAXX DAY 1-2 EXECUTION CHECKLIST

**Date:** 2026-01-19
**Status:** Ready to execute
**Context:** Overnight agent swarm completed system design. Now execute.

---

## ⚡ DAY 1: SETUP & ACCOUNT CREATION

### Phase 1A: Service Subscriptions (30 min)

**Already Have:**
- ✅ Claude Max ($200/mo) - Active

**Need to Subscribe:**
1. [ ] **Decodo Proxies** - $50/mo
   - Go to: https://app.decodo.com
   - Plan: Starter 1GB residential proxies
   - Why: Multi-account safety (X, TikTok, etc.)
   - Setup: Get SOCKS5 credentials

2. [ ] **SMSPool** - $5-10 one-time
   - Go to: https://smspool.net
   - Why: Virtual phone numbers for account verification
   - Setup: Add balance, test with 1 number

3. [ ] **GoLogin** - $0 (free tier)
   - Go to: https://gologin.com
   - Why: Anti-detect browser profiles
   - Setup: Download app, create 3 profiles (one per niche)

**Total Cost Today:** $55-60 + one-time

---

### Phase 1B: Email Addresses (15 min)

Create 4 email addresses on ProtonMail:

1. [ ] **printmaxxer@protonmail.com** - Meta brand account
   - Used for: @PRINTMAXXER Twitter, all meta documentation

2. [ ] **ai.workflows.tips@protonmail.com** - AI Utilities niche
   - Used for: AI niche X, TikTok, YT, IG accounts

3. [ ] **daily.anchor.faith@protonmail.com** - Faith niche
   - Used for: Faith niche X, TikTok, YT, IG accounts

4. [ ] **three.hour.physique@protonmail.com** - Fitness niche
   - Used for: Fitness niche X, TikTok, YT, IG accounts

**Naming Pattern:** Use dots in username (harder to detect as bulk)

---

### Phase 1C: Social Account Creation (2-3 hours)

**Setup Notes:**
- Use GoLogin profiles (one per niche)
- Use Decodo proxies
- Use SMSPool for phone verification
- DO NOT post yet - warmup first

#### Meta Brand Account
1. [ ] **@PRINTMAXXER on X (Twitter)**
   - Email: printmaxxer@protonmail.com
   - Bio: "building internet cash flow systems in public | levels.io style | $0→$Xk tracker"
   - Profile pic: AI gen minimalist logo
   - Header: Simple text graphic
   - Pin: "Building PRINTMAXX - solopreneur OS. Follow for experiments."

#### AI Utilities Niche (4 accounts)
2. [ ] **X:** @ai_workflows_daily
3. [ ] **TikTok:** @aiworkflowsdaily
4. [ ] **YouTube:** AI Workflows Daily
5. [ ] **Instagram:** @aiworkflowsdaily

**Bio template:** "AI automation hacks for solopreneurs | Daily workflows that actually work | Free stack guide in bio"

#### Faith Niche (4 accounts)
6. [ ] **X:** @daily_anchor_faith
7. [ ] **TikTok:** @dailyanchorfaith
8. [ ] **YouTube:** Daily Anchor Faith
9. [ ] **Instagram:** @dailyanchorfaith

**Bio template:** "Daily faith-based motivation | Streak tracking | Scripture-backed mindset | Free journal in bio"

#### Fitness Niche (4 accounts)
10. [ ] **X:** @three_hour_physique
11. [ ] **TikTok:** @threehourphysique
12. [ ] **YouTube:** 3-Hour Physique
13. [ ] **Instagram:** @threehourphysique

**Bio template:** "Busy person's fitness system | 3 hours/week to peak physique | Free guide in bio"

---

### Phase 1D: Account Tracking (15 min)

Update `/LEDGER/ACCOUNTS.csv` with all account details:

```csv
Niche,Platform,Handle,Email,ProxyUsed,Status,CreatedDate,LastActive
Meta,Twitter,@PRINTMAXXER,printmaxxer@protonmail.com,Decodo-1,WARMUP,2026-01-19,2026-01-19
AI,Twitter,@ai_workflows_daily,ai.workflows.tips@protonmail.com,Decodo-2,WARMUP,2026-01-19,2026-01-19
...
```

---

## 🔥 DAY 1 EVENING: START WARMUP

### Warmup Protocol (M1: Manual Mode)

**Rules:**
- NO posting yet
- NO automation yet
- Pure manual engagement to build trust signals

#### Daily Warmup Tasks (20-30 min per niche)

**For each niche account:**

1. [ ] **Follow 15-20 accounts** in your niche
   - AI: Follow @levelsio, @bentossell, @gregisenberg, etc.
   - Faith: Follow @faithquotes, @bibleverseofday, etc.
   - Fitness: Follow @athleanx, @jeffnippard, etc.

2. [ ] **Like 10-15 posts** from those accounts
   - Scroll timeline
   - Like posts that align with your vibe
   - Don't like everything - be selective

3. [ ] **Reply to 3-5 posts** with genuine engagement
   - Short, thoughtful replies
   - No links, no promo
   - Just normal human interaction

4. [ ] **Bookmark 2-3 posts** for later repurposing

**Track in LEDGER/WARMUP_DEVICE_MATRIX.csv:**

```csv
Date,Niche,Platform,Mode,Follows,Likes,Replies,Posts,Flags
2026-01-19,AI,Twitter,M1-Manual,18,12,4,0,NONE
2026-01-19,Faith,Twitter,M1-Manual,15,10,3,0,NONE
...
```

---

## 📦 DAY 2: PRODUCT SETUP & CONTENT PREP

### Phase 2A: Gumroad Setup (30 min)

1. [ ] **Create Gumroad account**
   - Go to: https://gumroad.com
   - Email: printmaxxer@protonmail.com
   - Connect Stripe for payments

2. [ ] **Create 3 products (unpublished)**

   Use copy from: `/AUTOMATIONS/info_products/PRODUCT_STRATEGY.md`

   **Product 1: AI Clarity Stack - $47**
   - Title: "AI Clarity Stack - $47 Notion Template"
   - Short description: "Stop drowning in AI tools. The CLEAR framework."
   - Cover: Create in Canva (simple, clean)
   - Files: Notion template link (create from strategy doc)
   - Status: DRAFT (don't publish yet)

   **Product 2: Daily Anchor System - $27**
   - Title: "Daily Anchor System - $27 Faith Journal"
   - Short description: "Build unbreakable faith streak. ANCHOR method."
   - Cover: Create in Canva
   - Files: PDF journal (create from strategy doc)
   - Status: DRAFT

   **Product 3: 3-Hour Physique - $47**
   - Title: "3-Hour Physique - $47 Busy Person's Fitness"
   - Short description: "Peak physique in 3 hours/week. BMS system."
   - Cover: Create in Canva
   - Files: PDF guide (create from strategy doc)
   - Status: DRAFT

3. [ ] **Get Gumroad links** (for later bio placement)
   - Copy draft URLs
   - Save to LEDGER/PRODUCTS.csv

---

### Phase 2B: Content Queue Build (1 hour)

**Overnight agent should have generated 80+ posts. Let's review:**

1. [ ] Check `/AUTOMATIONS/content_generation/repurposed_content/`
   - Look for completed repurpose CSVs
   - Review quality of generated posts

2. [ ] Create posting schedule
   - Week 1: 0 posts (warmup only)
   - Week 2: 1 post/day per niche
   - Week 3+: 2-3 posts/day per niche

3. [ ] Update `/LEDGER/CONTENT_PIPELINE.csv`

---

### Phase 2C: Automation Setup (1-2 hours)

**Set up Hetzner + n8n for scheduled posting:**

1. [ ] **Create Hetzner account**
   - Go to: https://hetzner.com/cloud
   - Create CX11 instance (~€5/mo)
   - Ubuntu 22.04 LTS

2. [ ] **Install n8n** (via Docker)
   ```bash
   # SSH into Hetzner VPS
   docker run -d \
     --name n8n \
     -p 5678:5678 \
     -v ~/.n8n:/home/node/.n8n \
     docker.n8n.io/n8nio/n8n
   ```

3. [ ] **Create n8n workflows**
   - Workflow 1: Daily warmup automation (follows, likes)
   - Workflow 2: Scheduled posting (loads from CSV)
   - Workflow 3: Bookmark scraper (daily)

4. [ ] **Test workflows**
   - Run test post on one account
   - Verify tracking updates in CSVs

---

## 📊 DAY 2 EVENING: REVIEW & ADJUST

### Metrics Check

Review in `/LEDGER/METRICS_DASH.csv`:

1. [ ] **Account Health**
   - Any warnings/flags from platforms?
   - Engagement rates on warmup interactions?

2. [ ] **Warmup Progress**
   - Followers gained: Target 5-10 per day
   - No spam flags

3. [ ] **Content Quality**
   - Review generated posts
   - Kill bad ones, keep winners

### Adjustments

Based on Day 1-2 data:

1. [ ] **If accounts flagged:** Slow down warmup
2. [ ] **If content weak:** Regenerate with stricter prompts
3. [ ] **If costs high:** Cut optional services

---

## 🚨 BLOCKERS TO AVOID

### DON'T DO YET (Until Week 3+)
- ❌ Publish Gumroad products
- ❌ Add links to bios
- ❌ Run any automation
- ❌ Cold DMs
- ❌ Paid ads

### WARMUP-ONLY MODE (Days 1-7)
- ✅ Manual follows/likes/replies
- ✅ Profile setup
- ✅ Backend prep (products, content queue)
- ✅ NO posting content yet

---

## 📁 KEY FILES TO UPDATE

As you execute, update these files:

1. **LEDGER/ACCOUNTS.csv** - All account details
2. **LEDGER/WARMUP_DEVICE_MATRIX.csv** - Daily warmup logs
3. **LEDGER/METRICS_DASH.csv** - Performance tracking
4. **LEDGER/EXPERIMENTS_AB.csv** - Test variations
5. **LEDGER/STATUS_BOARD.md** - High-level progress

---

## ✅ DAY 2 COMPLETION CHECKLIST

At end of Day 2, you should have:

- [ ] 13 social accounts created (1 meta + 12 niche)
- [ ] Decodo proxies active
- [ ] GoLogin profiles configured
- [ ] 2 days of warmup completed
- [ ] 3 Gumroad products drafted (unpublished)
- [ ] n8n automation server running
- [ ] 80+ posts in content queue
- [ ] All tracking CSVs updated
- [ ] NO platform warnings/flags

**If ✅ on all:** Proceed to Day 3-7 (continued warmup + product builds)

**If ❌ on any:** Troubleshoot before moving forward

---

## 🎯 NEXT: DAY 3-7

See `/DAY3-7_EXECUTION.md` (will create after Day 2 completion)

Focus:
- Continue daily warmup
- Build actual product deliverables (Notion templates, PDF guides)
- Create product covers in Canva
- Test first app MVP
- Monitor account health

**No posting until Day 7+ when accounts are clean.**

---

*Last updated: 2026-01-19*
*Execute methodically. Speed + precision.*
