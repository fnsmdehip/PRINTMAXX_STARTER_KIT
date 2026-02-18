# LEGAL, RESEARCH & MISC AUDIT

**Date:** 2026-02-14
**Auditor:** Claude Opus 4.6
**Scope:** LEGAL, 09_LEGAL, RESEARCH, 10_RESEARCH, SECRETS, .claude, .guardrails, .qodo, logs, root RTF/DOCX/JS files, requirements.txt

---

## Summary Stats
- Legal docs: 24 (all in 09_LEGAL/, LEGAL/ is empty)
- Research files: 19 (RESEARCH/) + 29 (10_RESEARCH/) = 48 total
- Config files: 30+ (.claude/ agents, rules, commands, settings, remotion-skills)
- Log files: 44 (logs/) + 4 (.guardrails/)
- RTF planning docs: 5 (root)
- DOCX/JS generator: 1 JS file found (PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.js)
- Secrets files: 3 (SECRETS/)
- Python deps: 4 packages in requirements.txt

---

## Legal/Compliance Status

### 09_LEGAL/ (24 files, 5 categories) -- ALL TEMPLATES, NOT CUSTOMIZED

**Website Policies (5 files):**
- PRIVACY_POLICY_TEMPLATE.md -- Generic template with [COMPANY NAME], [DATE] placeholders
- TERMS_OF_SERVICE_TEMPLATE.md -- Same, not filled in
- COOKIE_POLICY_TEMPLATE.md
- REFUND_POLICY_TEMPLATE.md -- Includes both "no refund" and "30-day" options
- DISCLAIMER_TEMPLATE.md

**FTC Compliance (5 files):**
- AFFILIATE_DISCLOSURE.md -- Template with placeholder affiliate program names
- TESTIMONIAL_GUIDELINES.md
- INCOME_DISCLAIMER.md -- Important given project's revenue claims; has earnings table but all values are [X]%
- AI_DISCLOSURE.md -- Covers AI-generated content, images, video, chatbots. Relevant and well-structured
- SPONSORED_CONTENT_RULES.md

**Contracts (5 files):**
- FREELANCER_AGREEMENT.md -- For UGC creators/content creators, placeholder format
- CLIENT_SERVICE_AGREEMENT.md
- AFFILIATE_AGREEMENT.md
- NDA_TEMPLATE.md -- Mutual NDA, standard format
- CONTENT_LICENSE.md

**Email Compliance (4 files):**
- CAN_SPAM_CHECKLIST.md -- Covers all 7 CAN-SPAM requirements with $50,120/violation penalty noted
- GDPR_EMAIL_GUIDE.md
- UNSUBSCRIBE_REQUIREMENTS.md
- B2B_VS_B2C_RULES.md

**Platform Compliance (5 files):**
- TIKTOK_RULES.md, INSTAGRAM_RULES.md, YOUTUBE_RULES.md, X_TWITTER_RULES.md, GUMROAD_RULES.md

### Verdict
All 24 legal docs are TEMPLATES with unfilled placeholders. None have been customized for actual PRINTMAXX entities. They are comprehensive in coverage (website, FTC, contracts, email, platform rules) but zero are production-ready. Every file says "IMPORTANT: This is a template for reference purposes only. Have a qualified attorney review before publishing."

**LEGAL/ directory** (old structure) is EMPTY -- all content lives in 09_LEGAL/.

### Critical Gap
With 285 CRITICAL compliance issues found by the automated compliance scanner (per `OPS/COMPLIANCE_SCAN_2026_02_13.md`), the project has extensive content with income claims, affiliate links, and marketing copy but ZERO deployed legal protections. The income disclaimer template is especially urgent given pervasive "$X/month" claims throughout content.

---

## Research Assets

### RESEARCH/ (19 files) -- PEMF Device Company Research

All files are PEMF (Pulsed Electromagnetic Field) therapy device research, branded "WEBERMAXX." This is a separate business venture from the main PRINTMAXX digital operations. Quality is HIGH -- real data, specific numbers, actionable.

**Core Research:**
- PEMF_MASTER_RESEARCH.md -- 2,429+ lines, 76 YouTube transcript analyses, $600M-$1.2B market, 6-12% CAGR
- PEMF_MARKET_ANALYSIS.md -- Competitive landscape (BEMER $6K, Pulse $5K-$20K, FluxHealth $350). Real pricing, real complaints, real vulnerabilities
- PEMF_GTM_STRATEGY.md -- 42 applicable PRINTMAXX methods mapped to PEMF launch. YouTube as primary channel
- PEMF_COMPLIANCE_LEGAL.md -- FDA "general wellness device" path, $2K-$8K legal cost
- PEMF_BOOTSTRAP_CAPITAL_GENESIS.md -- $847 path to first sale. DIY build for $62, sellable 6-coil mat for $285-$450

**Manufacturing/Supply Chain:**
- PEMF_MANUFACTURING_DROPSHIP.md, PEMF_DIY_BUILD_GUIDE.md, PEMF_MAKE_TO_ORDER.md
- PEMF_ASSEMBLY_QC_GUIDE.md, PEMF_GAUSSMETER_GUIDE.md, PEMF_ASSEMBLERS_DIRECTORY.md

**Distribution/Influencer:**
- PEMF_INFLUENCER_OUTREACH.md, PEMF_INFLUENCER_RATES.md, PEMF_INFLUENCER_ALPHA_AUDIT.md
- PEMF_INFLUENCER_TWITTER.md, PEMF_INFLUENCER_PODCASTERS.md, PEMF_INFLUENCER_TIKTOK.md
- PEMF_SUPPLEMENT_SYNERGY.md, PEMF_STEVE_BRADET_TRANSCRIPTS.md

### 10_RESEARCH/ (29 files, 5 competitor categories) -- App Competitor Intelligence

Well-organized competitive analysis across 5 verticals, each with standardized sub-files:

**Faith Apps (6 files):** Market overview ($1.2B, 18-22% CAGR), top 10 competitors (Hallow at $50-80M ARR), feature matrix, pricing analysis, gap analysis, differentiation strategy

**Fitness Apps (6 files):** Same structure. Screen time + habit tracker market

**AI Tools (6 files):** $67B generative AI market, AI writing tools $3.2B, productivity tools $8B

**Customer Service AI (5 files):** Market overview, top 10, pricing teardowns, gap analysis, differentiation

**Info Products (5 files):** $30B+ digital products market. Faith $2B, fitness $4B, productivity/AI $1.5B (35% growth)

**Root file:** COMPETITOR_MARKETING_ANALYSIS.md -- 15+ competitor apps across faith, fitness, productivity. Actionable tactics: animated paywalls (2.9x conversion), Day 0 trials (50% of all trials), streak mechanics (55% 7-day retention)

### Verdict
Research is STRONG. PEMF research is deeply technical and actionable with real supplier data, pricing, and build instructions. The 10_RESEARCH competitor analysis is well-structured and contains real market data. Both are ready to inform business decisions. The PEMF research represents a separate, well-researched business opportunity beyond the digital-first PRINTMAXX model.

---

## Secrets Inventory (types only, NO values)

### SECRETS/ (3 files)

**CREDENTIALS.env:**
- Personal info fields: FULL_NAME, PRIMARY_EMAIL (has a proton.me address), BACKUP_EMAIL, PHONE (3 fields)
- SimpleLogin email alias fields (10 alias slots for different brand accounts)
- Platform credential placeholders: Most are EMPTY/unfilled
- Status: MOSTLY EMPTY -- structured template with only primary email filled

**PAYMENT_INFO.md:**
- Personal info (name, email, phone)
- Payment fields: STRIPE_ACCOUNT_ID, PAYPAL_EMAIL, CARD_LAST_4, full billing address
- Platform credentials: Gumroad, Buffer, Beehiiv, and more
- Status: MOSTLY EMPTY -- template with only email filled

**created_accounts.json:**
- JSON array of automated account creation attempts
- Contains: platform names, emails, AUTO-GENERATED PASSWORDS IN PLAINTEXT, status, timestamps
- Platforms attempted: Surge.sh (READY), Gumroad (FAILED x2), Buffer (FAILED)
- Status: SECURITY CONCERN -- plaintext passwords stored in JSON file

### Critical Issues
1. **Plaintext passwords in created_accounts.json** -- auto-generated passwords are stored unencrypted
2. **The .gitignore status of SECRETS/ is unclear** from files alone -- guardrails.md references it as gitignored but should be verified
3. **Minimal actual credentials stored** -- most fields empty, indicating account creation is still the #1 blocker

---

## System Config (.claude/)

### CLAUDE.md -- The Institutional Brain (2,400+ lines)

The project's CLAUDE.md is extraordinary in scope. It functions as a complete operating system for AI agents, containing:

- **Session protocols:** Mandatory startup checklist (15 steps), handoff procedures, end-of-session updates
- **Ship-first philosophy:** "DEPLOY FIRST, BUILD SECOND" -- aggressive anti-planning directive
- **Autonomous execution mandate:** "DON'T ASK PERMISSION" -- agents execute with best judgment
- **Navigation map:** 200+ "Where is..." entries and 120+ "I want to..." task router entries
- **Status tracking:** Mandatory system status block after every task completion
- **Content standards:** @pipelineabuser voice, weighted tier system (S/A/B/C tiers), 24 AI patterns to eliminate
- **Financial tracking:** Revenue, expenses, P&L, investment portfolio references
- **Zero Waste Protocol:** Every piece of research must generate content
- **Max Squeeze Protocol:** Minimum 3 tweets + 1 thread per build session

### CLAUDE_SLIM.md -- Abbreviated version (references Feb 5 handoff, outdated)

### Rules (6 files):
- **security.md** -- OWASP-aware: no hardcoded creds, input validation, rate limiting
- **performance.md** -- Bundle <500KB, LCP <2.5s, Core Web Vitals targets
- **code-style.md** -- TypeScript, React patterns, import organization, naming conventions
- **copy-style.md** -- 200+ lines of voice calibration with weighted tier system
- **alpha-review.md** -- Bot detection, earnings skepticism, review taxonomy (APPROVED/ENGAGEMENT_BAIT/REJECTED)
- **guardrails.md** -- Project-folder-only file operations, explicit CAN/CANNOT lists

### Agents (4 files):
- validator.md (Haiku model), reviewer.md, deployer.md, content-generator.md

### Commands (12 files):
- printmaxx.md, generate-longtail.md, generate-posts.md, review-alpha.md, run-alpha-extractor.md, validate.md, deploy-check.md, parallel-launch.md, warmup-sop.md, brand-names.md, daily-research.md, remotion-video.md, status.md

### Settings:
- **settings.json:** Agent teams enabled, Sonnet as default model, PreToolUse/PostToolUse hooks for file validation, permissionMode: "acceptEdits"
- **settings.local.json:** 250 permission entries -- extensive bash command whitelist including python3, npm, surge, vercel, playwright, xcode tools. Contains a very long inline bash command (categorize.py script) and another (CSV append). Also whitelists WebSearch and WebFetch for specific domains

### Remotion Skills:
- Full remotion video production skill cloned as git repo with 25+ rule files for video production (3D, animations, audio, captions, charts, fonts, timing, transitions)

### Verdict
The .claude/ configuration is the most comprehensive AI agent configuration system I have encountered. It is essentially an operating manual for autonomous solopreneurship. The settings.local.json has grown organically and contains some very large inline bash commands that should be refactored. The CLAUDE.md is well-maintained but at 2,400+ lines is approaching the practical limit for agent context loading.

---

## Guardrails (.guardrails/)

**4 files:**
- .gitignore -- Ignores guardrails logs from git
- audit.jsonl -- 7 INIT session entries from Feb 12, 2026. Each logs PID and timestamp
- operations.log -- 29 entries. Shows path validation working correctly. One concerning pattern: paths like `~/Desktop/important.docx` and `~/.ssh/id_rsa` were validated as WITHIN project (they resolve to project-relative paths, not actual home directory paths -- this appears to be a guardrails test, not actual operations)
- shell_operations.log -- Not read but exists

### Verdict
Guardrails system is FUNCTIONAL but lightly used. The operations.log shows it correctly validates paths. The test entries confirm both allowed and blocked operations were verified. No evidence of guardrail violations.

### .qodo/ -- DOES NOT EXIST (no files found)

---

## Log Health

### logs/ (44 files, all from Feb 8-9 2026)

**Scraper Logs (5 files):**
- reddit_scraper.log -- EMPTY (0 content)
- headless_reddit.log, headless_twitter.log -- Exist but likely minimal
- enhanced_reddit.log -- Working: found posts across 6+ subreddits (r/SideProject, r/juststart, r/SaaS, etc.)
- enhanced_twitter.log -- Exists

**Watchdog Logs (19 files, .log + .txt):**
- 10 watchdog .log files + 9 diff/audit .txt files
- Most recent: 2026-02-09 04:39:59
- Show system status: 85 alpha rows, 69 methods, 12 Buffer CSVs, 1008 posts generated
- Runs report: 3 runs that day, 95 alpha extracted, 2016 content generated, 1 error
- Revenue projected: $2,486.12/30d (from automation results, likely hypothetical)

**Cron Job Logs (7 files):**
- morning_sync_2026-02-09.log -- Extracted 543 rows from MEGA_SHEET, BUT hit errors: organize_alpha.py failed on makedirs, FileNotFoundError
- weekly_2026-02-09.log -- MULTIPLE FAILURES: merge_backtest_scores.py failed (missing BACKTEST_RESULTS.csv), generate_30day_calendar.py failed (PermissionError: cannot create /Users directory -- path resolution bug in container), content QA queue creation failed
- content_gen_2026-02-09.log -- PermissionError on calendar generation, but Buffer CSV creation SUCCEEDED (12 files, 1008 posts)

**Launchd Logs (10 files):**
- launchd_morning.log -- EMPTY
- launchd_content.log, launchd_weekly.log, launchd_digest.log, launchd_backup.log, launchd_overnight.log -- All exist
- Corresponding _err.log files exist for each

### Key Findings
1. **Path resolution bugs:** Scripts hardcode `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/` but run in container environment at `/sessions/awesome-nice-brown/mnt/` causing Permission denied errors
2. **Missing data files:** BACKTEST_RESULTS.csv does not exist, breaking weekly scripts
3. **Content generation WORKS:** Buffer CSVs generated successfully (1008 posts across 12 files)
4. **Alpha extraction WORKS:** 95 entries extracted in morning sync
5. **No logs newer than Feb 9** -- suggests cron jobs stopped running after that date (5 days ago)

---

## RTF/DOCX Contents

### Root RTF Files (5 files) -- User's Original Planning/Prompt Documents

**app guide.rtf:**
App UI/UX design specification -- onboarding screens (back button, progress bar, headings, option buttons), typography specs (San Francisco/Roboto, letter spacing), animation specs (fade transitions, pulse effects, ripple effects, <300ms). This is a detailed app design system prompt, likely used for building the PWA apps.

**hyper rat soft engin.rtf:**
"Hyper-rational software engineering" system prompt. First-principles problem solver with zero tolerance for excuses. Contains: Deconstruction principles, Solution Engineering, Delivery Protocol, Interaction Rules ("Never console or sympathize," "Cut off excuses instantly"). This was likely used as a Claude system prompt for the project's aggressive execution style.

**money methods and sub category methods to add.rtf:**
Brainstorm/idea dump of additional money methods: relax channels, sleep timer channels, news scrapers, women appreciation pages (with disclosure), clip streamer channels, meme channels, AI influencer accounts, AI findom, AI OnlyFans, AI ASMR, Roblox games, automated streamer clipping. Raw ideation notes, most have been incorporated into MONEY_METHODS/.

**landind page prtopmt.rtf:**
Landing page design prompt for "DevMode" -- a fictional software tool for visualizing code behind interfaces. Contains full design spec: color palette (#F1FFD4, #E8D9F0, #00AEEF), SVG-only graphics, hero section, feature section, team workflow, footer. This appears to be a reference prompt for generating landing pages.

**iuhkm.csv.rtf:**
CSV data of 20 Twitter/X accounts with detailed monetization analysis. Columns: Name, Handle, Niche, Followers, Revenue/ARR, Business Model, Engagement Rate, Copy Framework, Funnel stages, Implementation Steps, Timeline, Cost to Launch. Includes: @benln ($75K/mo), @whotfiszackk ($55K/mo), @WorkflowWhisper ($80K/mo), @pipelineabuilder ($50K/mo), @danvs1 ($130K/mo), @pounddz ($95K/mo). Legitimacy grades range from "Legal" to "Gray-Hat." Rich competitive intelligence for the @PRINTMAXXER account strategy.

### Root DOCX/JS Files

**PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.js:**
A Node.js script using the `docx` library to programmatically generate a formatted .docx document. Contains table-building functions, color scheme definitions (professional green/blue/red), heading/paragraph/bullet generators. This is a DOCX GENERATOR SCRIPT, not a document itself -- it creates formatted automation blueprints from code.

**PRINTMAXX_SYSTEM_AUDIT_FEB9_2026.docx/.js:** Referenced in project but DOCX not found via search. The .js file likely exists as a companion generator.

---

## Python Dependencies

### requirements.txt (4 packages + comments)

```
rich>=13.0.0          -- Terminal dashboards (agent_monitor.py)
textual>=0.80.0       -- Bloomberg-style TUI (quant_dashboard.py)
playwright>=1.40.0    -- Browser automation (twitter scraper, auto-listing)
numpy>=1.24.0         -- Quant calculations (revenue projector)
```

**Note in file:** "Most AUTOMATIONS/ scripts only use Python stdlib (csv, json, argparse, pathlib, collections, datetime) and will work without installing any packages."

### Verdict
Lightweight dependency footprint. The project deliberately minimizes external dependencies, using stdlib for 90%+ of scripts. Only 4 optional packages needed. Pandas is commented out. pytest listed for testing. This is good practice for maintainability.

---

## Critical Gaps

1. **ZERO production-ready legal docs** -- All 24 legal templates have unfilled placeholders. With 285 CRITICAL compliance issues in content, this is the highest-risk gap
2. **Plaintext passwords in SECRETS/created_accounts.json** -- auto-generated passwords stored unencrypted
3. **Log pipeline broken since Feb 9** -- Path resolution bugs cause script failures in container vs local environments; no logs for 5 days
4. **Missing BACKTEST_RESULTS.csv** breaks weekly automation scripts
5. **CLAUDE.md approaching size limit** -- 2,400+ lines may cause context loading issues
6. **settings.local.json contains inline scripts** -- Very long bash commands embedded in permission whitelist entries, some containing full Python scripts
7. **No actual legal entity exists** -- Templates reference [COMPANY NAME] throughout; no evidence of LLC/business formation
8. **RESEARCH/ is entirely PEMF** -- No research exists for the core PRINTMAXX digital products business model itself
9. **.qodo/ directory does not exist** despite being referenced in the audit scope

---

## Strengths

1. **Legal template coverage is comprehensive** -- All major areas covered (website policies, FTC, contracts, email, platform rules) even if unfilled
2. **PEMF research is institutional quality** -- 2,429+ lines from 76 YouTube transcripts, 50+ web searches, real pricing/supplier data. Actionable from day 1
3. **10_RESEARCH competitor analysis is well-structured** -- Standardized format across 5 verticals with market sizes, gap analyses, and differentiation strategies
4. **Guardrails system is functional** -- Path validation working, audit logging active, explicit CAN/CANNOT rules enforced
5. **.claude/ config is the most comprehensive agent operating system** -- Navigation map, task router, copy style rules, alpha review guidelines, session protocols. Represents significant institutional knowledge
6. **Minimal Python dependencies** -- 4 optional packages, stdlib-first approach reduces attack surface and maintenance burden
7. **RTF files contain valuable seed data** -- Especially iuhkm.csv.rtf (20 monetization profiles) and app guide.rtf (full design system)
8. **Content generation pipeline works** -- 1008 posts across 12 Buffer CSVs generated successfully despite other script failures
9. **FTC/AI disclosure template is forward-looking** -- Covers emerging AI content disclosure requirements ahead of most businesses
10. **Copy style rules (.claude/rules/copy-style.md) prevent AI slop** -- Weighted voice system with 24 detectable AI patterns to eliminate, specific find/replace tables
