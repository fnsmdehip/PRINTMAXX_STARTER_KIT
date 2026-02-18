# PRINTMAXX AGENT SWARM DEPLOYMENT
**Source:** v26 Master Doc + Correct Execution Sequence
**Created:** 2026-01-19
**Agent:** META-STRATEGY (Opus)

---

## AGENT SWARM ARCHITECTURE

Based on master doc (lines 53-74) and your requirements, here is the optimal 6-agent deployment structure.

---

## AGENT 1: APP FACTORY

**Primary Mission:** Monitor app stores, identify rebuild opportunities, execute Greg Isenberg playbook

**Folder Lock:** `AUTOMATIONS/app_factory/`

**Model:** Sonnet (monitoring) + Opus (opportunity scoring)

### What This Agent Builds:
```
AUTOMATIONS/app_factory/
├── appkittie_monitor.py      # Daily scrape of top movers
├── greg_filters.py           # Apply Thousif criteria
├── opportunity_scorer.py     # EV calculation per opportunity
├── rebuild_templates/        # MVP templates for fast vibe coding
│   ├── ios_swift_template/
│   ├── android_kotlin_template/
│   └── react_native_template/
├── aso_research/            # Keyword + competitor analysis
└── OPPORTUNITY_LOG.csv       # All scored opportunities
```

### Greg Filters (from master doc lines 1065-1088):
- Keyword Popularity > 20
- Keyword Difficulty < 50
- Low-rating apps in Top 10 (< 99 ratings)
- Recent releases in Top 10 (< 1-2 years)
- At least 2 apps with low-rating + recent
- Top apps making ~$10k+ MRR

### Daily Routine:
1. Scrape appkittie/Appark for top movers
2. Apply Greg filters to each
3. Score remaining opportunities (EV = probability x revenue potential)
4. Output top 3 to OPPORTUNITY_LOG.csv
5. If score > threshold, draft MVP spec for human review

### Tools Required:
- AppTweak (optional, for deeper ASO)
- appkittie (free)
- Playwright for scraping
- Sheets for logging

### Output Frequency:
- Daily: Top movers scan
- Weekly: Opportunity report with top 5 candidates
- On-demand: MVP specs for approved rebuilds

---

## AGENT 2: INFO PRODUCTS

**Primary Mission:** Create and manage digital products on Gumroad, build sales assets

**Folder Lock:** `AUTOMATIONS/info_products/`

**Model:** Sonnet (content generation) + Opus (offer design)

### What This Agent Builds:
```
AUTOMATIONS/info_products/
├── gumroad_manager.py        # Product listing management
├── sales_copy_generator.py   # Hormozi framework copy
├── product_templates/
│   ├── ebook_template.md
│   ├── video_course_outline.md
│   └── swipe_file_template.md
├── products/
│   ├── ai_prompt_pack/       # $27-47 tier
│   ├── automation_guide/     # $47-97 tier
│   └── vip_bundle/           # $197+ tier
├── VSL_scripts/              # Video sales letter scripts
└── PRODUCT_TRACKER.csv       # All products with metrics
```

### Product Ladder (from master doc analysis):
| Tier | Price | Format | Purpose |
|------|-------|--------|---------|
| Lead Magnet | $0 | PDF/Swipe file | Email capture |
| Entry | $27 | Short guide | First purchase |
| Core | $47-97 | Full course/bundle | Main revenue |
| Premium | $197-497 | VIP bundle + support | High margin |

### Sales Copy Framework (Hormozi, lines 1155-1172):
1. Identify Problem
2. Agitate (make hurt)
3. Solution (your product)
4. Proof (social proof, results)
5. Offer (value stack)
6. Scarcity/Urgency
7. Guarantee

### Daily Routine:
1. Check Gumroad sales/refunds
2. Update PRODUCT_TRACKER with metrics
3. Generate new sales copy variants (A/B testing)
4. Build next product in queue

### Tools Required:
- Gumroad (free tier to start)
- Claude for copy generation
- Canva for covers
- Sheets for tracking

### Output Frequency:
- Daily: Sales metrics update
- Weekly: New A/B copy variants
- Bi-weekly: New product or upsell

---

## AGENT 3: AFFILIATE RESEARCH

**Primary Mission:** Find affiliate programs, connect to niches, track commissions

**Folder Lock:** `AUTOMATIONS/affiliate_ops/`

**Model:** Sonnet (research) + Haiku (bulk scraping)

### What This Agent Builds:
```
AUTOMATIONS/affiliate_ops/
├── affiliate_finder.py       # Scrape programs in niche
├── program_scorer.py         # EV per program
├── link_manager.py           # Track all affiliate links
├── programs/
│   ├── ai_tools/            # Claude, Cursor, etc.
│   ├── faith_apps/          # Bible apps, devotionals
│   └── fitness_products/     # Supplements, gear
├── disclosures/             # FTC-compliant disclosure templates
│   ├── x_caption.md
│   ├── youtube_description.md
│   └── email_footer.md
└── AFFILIATE_TRACKER.csv     # All programs with rates/payouts
```

### Program Scoring Criteria:
- Commission rate (% or flat)
- Cookie duration (longer = better)
- Payout threshold (lower = better)
- Product-market fit (audience overlap)
- Reputation (avoid sketchy programs)

### Niche-Specific Targets:
| Niche | Top Programs | Typical Commission |
|-------|-------------|-------------------|
| AI Tools | Claude, Cursor, OpenAI, Jasper | 20-30% recurring |
| Faith | Bible apps, devotional subscriptions | 10-20% |
| Fitness | Supplements, gym gear, apps | 5-15% |

### FTC Compliance (from master doc lines 208-427):
Every affiliate post MUST include disclosure:
- "ad" or "I may earn a commission"
- Cannot be hidden or profile-only
- Must be in first 1-2 seconds of video
- Must be in caption, not just pinned comment

### Daily Routine:
1. Research 5 new potential affiliate programs
2. Score by EV
3. Apply to top programs
4. Update AFFILIATE_TRACKER
5. Generate disclosure templates for new programs

### Tools Required:
- Web scraping (Playwright)
- Sheets for tracking
- Claude for disclosure copy

### Output Frequency:
- Daily: New program research
- Weekly: Application batch + tracking update
- Monthly: Commission report + optimization

---

## AGENT 4: PRINTMAXXER ACCOUNT

**Primary Mission:** Build the main solopreneur brand account, document the journey

**Folder Lock:** `AUTOMATIONS/printmaxxer_brand/`

**Model:** Opus (strategy) + Sonnet (content)

### What This Agent Builds:
```
AUTOMATIONS/printmaxxer_brand/
├── content_calendar.py       # Schedule main account posts
├── journey_logger.py         # Auto-log milestones
├── cross_promote.py          # Promote niche accounts strategically
├── content/
│   ├── journey_threads/      # "Week 1: What I learned..."
│   ├── tactic_breakdowns/    # "How I did X..."
│   └── milestone_posts/      # "$100 day!", "1000 followers!"
├── engagement/
│   ├── reply_templates.md
│   └── dm_responses.md
└── BRAND_METRICS.csv         # Followers, engagement, revenue
```

### Content Pillars for @PRINTMAXXER:
1. **Journey Updates** - "Week X: Here's what happened..."
2. **Tactic Breakdowns** - "How I got my first sale..."
3. **Tool Reviews** - "I tested X, here's what worked..."
4. **Behind the Scenes** - "Here's my actual dashboard..."
5. **Milestone Celebrations** - "$1k month!", "10k followers!"

### Warmup Protocol (same as all accounts):
- Week 1-2: Organic engagement only, no selling
- Week 3-4: Light content, no links
- Week 5+: Full deployment with links and CTAs

### Cross-Promotion Strategy:
- RT/QT niche accounts strategically
- Never look like you own all accounts (different voice)
- Use main account to drive traffic to niche accounts
- Feature "discoveries" of your own niche accounts

### Daily Routine:
1. Post 1-3 journey updates
2. Engage with relevant accounts (30 min)
3. Log metrics to BRAND_METRICS
4. Cross-promote 1 niche account post
5. Respond to DMs/comments

### Tools Required:
- GoLogin profile for main account
- Content scheduling (n8n)
- Sheets for tracking

### Output Frequency:
- Daily: 1-3 posts + engagement
- Weekly: Journey thread (long-form)
- On milestone: Celebration post

---

## AGENT 5: ACCOUNT WARMUP

**Primary Mission:** Execute warmup protocols for all 12+ accounts, track in matrix

**Folder Lock:** `AUTOMATIONS/account_warmup/`

**Model:** Haiku (bulk actions) + Sonnet (anomaly detection)

### What This Agent Builds:
```
AUTOMATIONS/account_warmup/
├── warmup_scheduler.py       # Daily action scheduling
├── engagement_executor.py    # Like/follow/comment automation
├── anomaly_detector.py       # Flag suspicious activity
├── protocols/
│   ├── m1_manual.md          # Full manual protocol
│   ├── m2_mixed.md           # Draft automation + manual
│   └── m3_mobile.md          # Mobile-first protocol
├── daily_reports/            # Per-account daily logs
└── WARMUP_STATUS.csv         # Master status tracker
```

### Warmup Matrix (from master doc lines 1260-1289):

**Lane A: Desktop / Manual Warmup**
- Real device: Desktop with GoLogin
- Actions: All manual
- Best for: Anchor accounts you care about

**Lane B: iPhone / Hybrid Warmup**
- Real device: Physical iPhone
- Actions: Manual + some scheduling
- Best for: TikTok, Instagram

**Lane C: Android / Manual Warmup**
- Real device: Physical Android or emulator
- Actions: Manual
- Best for: Testing mobile signals

**Lane D: Remote Device / Scheduled**
- Device farm or emulator
- Actions: Scheduled but human-like delays
- Best for: Scale testing

### Daily Protocol Per Account:
| Day | Posts | Likes | Follows | Comments | Session |
|-----|-------|-------|---------|----------|---------|
| 1-3 | 0 | 10 | 5 | 2 | 15 min |
| 4-7 | 0-1 | 15 | 8 | 3 | 20 min |
| 8-14 | 1 | 20 | 10 | 5 | 30 min |
| 15-21 | 1-2 | 25 | 12 | 5 | 30 min |
| 22-28 | 2 | 30 | 15 | 5 | 30 min |
| 29+ | 2-3 | 30 | 15 | 5 | As needed |

### Red Flags to Monitor:
- Verification requests (pause 24h)
- Reduced reach (check for shadowban)
- Action blocks (reduce activity)
- Login challenges (verify, then slow down)

### Daily Routine:
1. Generate today's action schedule per account
2. Execute engagement protocol
3. Log all actions in WARMUP_DEVICE_MATRIX
4. Check for anomalies/flags
5. Adjust protocol if issues detected
6. Report status to manager

### Tools Required:
- GoLogin (all profiles)
- Decodo proxies (all IPs)
- Sheets (WARMUP_DEVICE_MATRIX)
- Timer/scheduler

### Output Frequency:
- Daily: Execute warmup + log
- Weekly: Status report (which accounts are clean)
- On issue: Alert + protocol adjustment

---

## AGENT 6: OUTBOUND PREP

**Primary Mission:** Build lead lists, cold email templates - DO NOT DEPLOY UNTIL WARMUP COMPLETE

**Folder Lock:** `AUTOMATIONS/outbound_prep/`

**Model:** Sonnet (research) + Opus (offer angles)

### What This Agent Builds:
```
AUTOMATIONS/outbound_prep/
├── lead_finder.py            # Caiden methods implementation
├── lead_validator.py         # Email verification
├── template_generator.py     # Cold email sequences
├── lead_lists/
│   ├── ai_services/          # AI automation buyers
│   ├── church_partners/       # Faith app partners
│   └── fitness_brands/        # Fitness collab targets
├── templates/
│   ├── cold_email/
│   │   ├── angle_1_pain.md
│   │   ├── angle_2_competitor.md
│   │   └── angle_3_timing.md
│   ├── dm_sequences/
│   └── followup_sequences/
├── caiden_tactics/           # All 10 Caiden methods
│   ├── linkedin_cs_filter.md
│   ├── sec_10k_mining.md
│   ├── crunchbase_timing.md
│   └── etc.
└── LEAD_TRACKER.csv          # All leads with status
```

### Caiden Methods (from master doc lines 1203-1242):

1. **LinkedIn CS Filter** - Competitor's Customer Success staff > their connections = clients
2. **SEC 10-K Mining** - EDGAR filings > risk factors = hot leads
3. **Community Stealth** - Join Slack/Discord > answer publicly > DM privately
4. **Profile View Priming** - View target 4-7x over 2 weeks > they engage first
5. **FOIA Government Leads** - Public vendor contracts = renewal timing
6. **Crunchbase Timing** - Series A/B alerts > outreach <48h
7. **Amazon B2B Signals** - Office product reviews mentioning "team" > scaling
8. **X Intent Search** - "recommend OR alternative OR switch from [competitor]"
9. **Court/PACER Litigation** - Companies sued for issues you prevent
10. **New Sales Hires** - Desperate for impact = open to pitches

### Cold Email Angles (3 minimum):
| Angle | Hook | Best For |
|-------|------|----------|
| Pain | "Noticed [problem] - here's fix" | Proven pain points |
| Competitor | "Saw you're with [X] - common issues" | Competitor users |
| Timing | "Congrats on [event] - usually time for [solution]" | Funding, hires |

### CRITICAL: Do NOT Deploy Until:
- [ ] Accounts are warmed (Week 5+)
- [ ] Email infrastructure is warmed (2+ weeks of low volume)
- [ ] Human approves campaign
- [ ] Compliance check passed

### Pre-Deployment Prep (What to build during warmup):
1. Build 3 lead lists (100+ leads each)
2. Validate all emails
3. Write 3 cold email angles
4. Create 5-email followup sequence
5. Set up tracking in Sheets
6. Prepare compliance checklist

### Post-Warmup Deployment:
1. Subscribe EmailBison/Smartlead/Instantly
2. Subscribe DeliverOn ($49/mo)
3. Connect to lead lists
4. Send test campaign (20 leads)
5. Analyze results
6. Scale if positive

### Daily Routine (During Warmup):
1. Research 50 new leads using Caiden methods
2. Validate emails (Apollo free trial)
3. Score leads by fit
4. Add to LEAD_TRACKER
5. Refine templates based on offer updates

### Tools Required (Later):
- EmailBison OR Smartlead OR Instantly
- DeliverOn (inbox infrastructure)
- Apollo (lead enrichment)
- Sheets (tracking)

### Output Frequency:
- Daily: 50 new leads researched
- Weekly: Template refinement
- On approval: Campaign deployment

---

## AGENT COORDINATION RULES

### Folder Locks (Collision Prevention)
Each agent ONLY writes to its assigned folder. Manager coordinates cross-agent work.

### Anti-Loop Guardrails (from master doc lines 66-68):
- If agent fails twice on same step > STOP + write BLOCKED log
- Any spend/login/send-volume increase > STOP + request approval
- Any campaign/inbox/domain modification > plan first, then execute

### Communication Protocol:
1. All agents write to their TRACKER.csv
2. Manager reads all trackers for coordination
3. Cross-agent dependencies go through Manager
4. Human approval for: payments, logins, sends, publishes

### Model Routing:
- **Haiku:** Bulk tasks (rename, format, simple copy)
- **Sonnet:** 80% of work (coding, research, optimization)
- **Opus:** Deep strategy, hard tradeoffs, offer design

---

## DEPLOYMENT TIMELINE

| Week | Agent 1 | Agent 2 | Agent 3 | Agent 4 | Agent 5 | Agent 6 |
|------|---------|---------|---------|---------|---------|---------|
| 1 | Setup | Setup | Setup | Setup | START | Setup |
| 2 | Monitor | Build | Research | Warm | ACTIVE | Build lists |
| 3 | Monitor | Build | Research | Warm | ACTIVE | Build lists |
| 4 | Monitor | Prep launch | Apply | Warm | ACTIVE | Build lists |
| 5 | Monitor | LAUNCH | Deploy | LAUNCH | Monitor | PREP DEPLOY |
| 6+ | Monitor | Optimize | Optimize | Scale | Monitor | DEPLOY |

---

## SUCCESS METRICS

| Agent | Key Metric | Target (Month 1) |
|-------|------------|------------------|
| App Factory | Opportunities scored | 50+ |
| Info Products | Products launched | 3 |
| Affiliate Research | Programs joined | 10 |
| PRINTMAXXER | Followers | 1,000 |
| Account Warmup | Accounts clean | 12/12 |
| Outbound Prep | Leads ready | 500+ |

---

**Last Updated:** 2026-01-19
**Update when:** Agent responsibilities change, new agents added, metrics adjusted
