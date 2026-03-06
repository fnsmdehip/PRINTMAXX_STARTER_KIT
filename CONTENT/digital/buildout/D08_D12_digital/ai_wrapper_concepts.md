# AI Wrapper Concepts — 5 Micro-SaaS Ideas

**Target:** Solopreneur builds in 1-2 weeks. Each wraps existing AI API. Priced at $9-49/mo. Ship with Stripe + simple Next.js or Python Flask frontend.

---

## Concept 1: ColdCraft — AI Cold Email Generator

**Tagline:** paste a LinkedIn URL. get a personalized cold email in 3 seconds.

**Problem:** Cold email writers spend 5-10 minutes per prospect researching and writing. At 50 prospects/day that's 4+ hours of manual work.

**Core Mechanic:**
1. User inputs LinkedIn URL (or company URL + name)
2. App scrapes public profile data (via ScraperAPI $29/mo or Apify)
3. Claude API generates personalized email: subject + body + P.S. line
4. User copies or auto-sends via connected SMTP

**Feature Spec:**
- Input: LinkedIn URL, company URL, or manual name + company + title
- Output: subject line (3 variants), email body (150-200 words), P.S. line, follow-up email #1 and #2
- Settings: tone (formal/casual/aggressive), length (short/medium/long), CTA type (call/reply/demo)
- History: saves all generated emails with open tracking via pixel
- Export: CSV for bulk import to Lemlist/Instantly/Apollo
- Bulk mode: paste 20 URLs → generate 20 emails → download CSV

**Tech Stack:**
- Frontend: Next.js + Tailwind + shadcn/ui
- API: Claude claude-haiku-4-5-20251001 (fast, $0.0025/1K tokens input)
- Scraping: ScraperAPI $29/mo or Apify free tier
- DB: Supabase free tier
- Auth: Clerk $0 to 10K MAU
- Payments: Stripe

**Pricing:**
- Free: 5 emails/day
- Starter $9/mo: 50 emails/day + history
- Pro $29/mo: 200 emails/day + bulk CSV + follow-up sequences
- Agency $79/mo: unlimited + team seats + API access

**COGS per 1K users:**
- Claude API: ~$0.40/user/mo (avg 30 emails × 500 tokens)
- ScraperAPI: ~$0.03/user/mo (30 scrapes × $29/50K)
- Supabase/infra: ~$0.05/user/mo
- **Total COGS: ~$0.48/user/mo on $9+ plans = 95%+ gross margin**

**Build Time:** 8-12 days solo
**Revenue Target:** 100 paying users at avg $18/mo = $1,800/mo MRR

**Differentiation vs Lavender/Copy.ai:**
- Lavender is $29/mo just for email scoring — not generation
- Copy.ai is bloated, not cold-email-specific
- ColdCraft is laser-focused: one input, one output, instant

**Launch Plan:**
- ProductHunt Day 1: aim for top 5 in Apps
- Reddit: r/Entrepreneur, r/sales, r/SaaS value post "I built X to solve Y"
- Cold email outreach to cold emailers (meta play)
- Twitter thread: "I built a tool that writes cold emails while you sleep"

---

## Concept 2: ReplyIQ — Twitter/X Reply Generator

**Tagline:** 10 high-quality replies per tweet. one click. never stare at blank reply box again.

**Problem:** Consistent engagement on X requires 30-50 replies/day. Quality matters — low-effort replies get ignored, high-effort replies take 3-5 minutes each. At 30 replies that's 1.5+ hours.

**Core Mechanic:**
1. User pastes tweet URL or raw tweet text
2. App analyzes sentiment, topic, audience context
3. Generates 5-10 reply variants across tones (agree/push back/add value/funny/question/personal story hook)
4. User selects and copies

**Feature Spec:**
- Input: tweet URL or pasted text (detects context automatically)
- Output: 5-10 reply variants with tone labels
- Tone options: agree + add value, contrarian, question, personal story hook, stat/data add, funny, compliment + insight
- Batch mode: paste 10 tweet URLs → generate replies for all in one batch
- Reply thread builder: chains 3-5 replies into a thread
- Account voice training: paste 20 of your tweets → app matches your style
- History + favorites: save best reply templates
- Chrome extension: highlight any tweet, click button, get replies inline

**Tech Stack:**
- Frontend: Next.js + Tailwind
- Chrome Extension: Manifest V3
- API: Claude Sonnet (better style matching than Haiku)
- DB: Supabase
- Auth: Clerk
- Payments: Stripe

**Pricing:**
- Free: 10 replies/day
- Solo $12/mo: 100 replies/day + voice training + history
- Growth $29/mo: 500 replies/day + batch mode + thread builder
- Agency $79/mo: 5 seats + unlimited + API

**COGS per user/mo:**
- Claude API: ~$0.80/user/mo (avg 50 replies × 300 tokens)
- Infra: ~$0.05/user/mo
- **Total: ~$0.85/user/mo on $12+ plans = 93% gross margin**

**Build Time:** 6-10 days (Chrome extension adds 2-3 days)
**Revenue Target:** 200 paying users at avg $20/mo = $4,000/mo MRR

**Differentiation:**
- Tribescaler is $25/mo just for hook analysis
- No tool specifically does reply generation at this price point
- Voice training makes replies sound like YOU — not generic AI

---

## Concept 3: AuditBot — Instant Website Audit Tool

**Tagline:** paste a URL. get a 47-point conversion audit in 60 seconds.

**Problem:** CRO agencies charge $2,000-5,000 for conversion audits. Solopreneurs and small SaaS teams can't afford it. Generic tools like GTmetrix only check speed.

**Core Mechanic:**
1. User pastes URL
2. Playwright headless browser visits page, takes screenshot, extracts HTML
3. Claude analyzes: headline clarity, CTA strength, social proof presence, trust signals, mobile experience, load speed, copy quality, form friction, pricing page structure
4. Returns scored report (0-100) with specific fixes ranked by impact

**Feature Spec:**
- Input: any URL (landing page, homepage, pricing page, sales page)
- Output: 47-point audit report with:
  - Overall score 0-100
  - Category scores: Headline (0-20), CTA (0-15), Social Proof (0-15), Trust (0-10), Copy (0-20), Speed (0-20)
  - Specific issues with severity (High/Medium/Low)
  - Fix recommendations with examples
  - Competitive benchmark (compares to top 10% in their niche)
- PDF export with agency-quality formatting
- Comparison mode: audit competitor URLs side-by-side
- Monitoring: re-audit weekly + email diff report
- White-label: agencies can remove AuditBot branding, add their own logo

**Tech Stack:**
- Frontend: Next.js
- Browser: Playwright (self-hosted) or Browserbase ($29/mo managed)
- Lighthouse API: free via Google PageSpeed API
- Claude API: Sonnet for analysis quality
- PDF: Puppeteer or react-pdf
- DB: Supabase
- Auth: Clerk
- Payments: Stripe

**Pricing:**
- Free: 3 audits/mo
- Solo $19/mo: 20 audits/mo + PDF export + monitoring
- Agency $49/mo: 100 audits/mo + white-label + comparison mode + team
- Enterprise $149/mo: unlimited + API + custom scoring weights

**COGS per audit:**
- Claude API: ~$0.05/audit (2K tokens)
- Browserbase or self-hosted Playwright: ~$0.01/audit
- **Total COGS: ~$0.06/audit → 99% gross margin at $19+ plan**

**Build Time:** 10-14 days (Playwright setup adds complexity)
**Revenue Target:** 150 paying users at avg $35/mo = $5,250/mo MRR

**Differentiation:**
- PageSpeed = speed only
- GTmetrix = speed + some SEO, no conversion analysis
- Hotjar = heatmaps, not audit reports
- AuditBot is the only tool that gives a CRO audit with specific copy rewrites

**Agency Upsell:** agencies use white-label version and charge clients $500-1,500 for the "audit" they generate with $0.06 of API cost = 99% margin arbitrage

---

## Concept 4: ContractCraft — Freelance Contract Generator

**Tagline:** stop losing clients to contract friction. sign-ready contracts in 90 seconds.

**Problem:** Freelancers lose deals because contracts are confusing or take too long. Using a lawyer is $300+/hour. Docusign templates are generic. Most just use Google Docs and lose.

**Core Mechanic:**
1. User fills brief form: project type, deliverables, timeline, payment terms, revision rounds, kill fee
2. Claude generates jurisdiction-appropriate contract
3. User reviews + sends via embedded e-sign (HelloSign/DocuSign API or native)
4. Client signs online, both parties get PDF copy

**Feature Spec:**
- Contract types: Web design, copywriting, social media management, video editing, consulting, app development, SEO, VA/admin
- Custom clauses: NDA, IP assignment, non-compete, white-label permission
- E-sign: embedded signing via HelloSign API ($25/mo) or PDFMonkey
- Client portal: client gets link, signs online without account
- Template library: 20+ base templates by project type
- Clause library: 50+ add-on clauses (late payment fee, revision limits, IP ownership, etc.)
- Payment integration: invoice generation post-signature
- Revision tracking: track all contract versions

**Tech Stack:**
- Frontend: Next.js
- E-sign: HelloSign API ($25/mo, 10 req/mo free)
- PDF: PDFMonkey or Puppeteer
- Claude API: Haiku (contract generation is mostly templating)
- DB: Supabase
- Payments: Stripe

**Pricing:**
- Free: 3 contracts/mo (no e-sign)
- Solo $14/mo: 15 contracts/mo + e-sign + PDF
- Pro $29/mo: unlimited + template library + clause builder
- Agency $69/mo: team seats + client portal + branded PDFs

**COGS per contract:**
- Claude API: ~$0.02/contract
- HelloSign API: ~$0.50/contract on $25/mo plan
- **Total COGS: ~$0.52/contract → 96% gross margin at $14+ plan**

**Build Time:** 7-10 days
**Revenue Target:** 200 paying users at avg $22/mo = $4,400/mo MRR

**Differentiation:**
- HelloSign/Docusign are signing platforms — don't generate contracts
- ChatGPT will generate a contract but with no e-sign or storage
- ContractCraft is end-to-end: generate → send → sign → archive

---

## Concept 5: BriefBuilder — Client Brief Generator for Agencies

**Tagline:** 10 minutes of scattered client babble → clean creative brief. one click.

**Problem:** Agencies and freelancers get rambling client emails and calls. Turning that into a structured brief takes 30-60 minutes. Bad briefs cause revision hell and scope creep.

**Core Mechanic:**
1. User pastes client email/transcript/notes OR records voice note (transcribed via Whisper)
2. Claude extracts: objective, target audience, deliverables, tone, timeline, budget, success metrics, constraints
3. Returns structured brief in agency-standard format
4. One-click export to Notion, PDF, or shareable link for client approval

**Feature Spec:**
- Input types: paste text, upload file (PDF/DOCX), voice record (Whisper transcription)
- Output: structured brief with sections: Background, Objective, Target Audience, Deliverables, Tone & Style, Timeline, Budget, Success Metrics, Constraints, Questions for Client
- Brief formats: Creative Brief, Project Brief, Campaign Brief, Content Brief
- Client approval: shareable link → client reviews + approves with comments
- Revision tracker: track what changed between brief versions
- Notion integration: push directly to Notion database
- Team mode: multiple team members can annotate brief
- AI brief scoring: rates brief completeness (forces better client inputs)

**Tech Stack:**
- Frontend: Next.js
- Voice: OpenAI Whisper API ($0.006/min)
- Claude API: Sonnet (extraction quality matters)
- Notion API: native integration
- DB: Supabase
- Auth: Clerk
- Payments: Stripe

**Pricing:**
- Free: 5 briefs/mo
- Solo $19/mo: 30 briefs/mo + voice input + Notion sync
- Agency $49/mo: unlimited + team + client approval + PDF export
- Enterprise $129/mo: custom brief templates + API + white-label

**COGS per brief:**
- Claude API: ~$0.06/brief (2.5K tokens)
- Whisper (if voice): ~$0.06/min of audio
- **Total COGS: ~$0.10-0.15/brief → 99% gross margin at $19+ plan**

**Build Time:** 8-12 days
**Revenue Target:** 150 paying users at avg $35/mo = $5,250/mo MRR

**Differentiation:**
- No dedicated brief generator exists at this price point
- Notion templates are static — BriefBuilder is AI-powered extraction
- Agency positioning lets you charge 5x solopreneur price

---

## Build Priority Matrix

| Concept | Build Time | Revenue Potential | Differentiation | Build First? |
|---------|-----------|------------------|-----------------|-------------|
| ColdCraft | 8-12 days | $1,800/mo at 100 users | Medium (crowded) | #3 |
| ReplyIQ | 6-10 days | $4,000/mo at 200 users | High | #2 |
| AuditBot | 10-14 days | $5,250/mo at 150 users | Very High | #4 |
| ContractCraft | 7-10 days | $4,400/mo at 200 users | High | #1 |
| BriefBuilder | 8-12 days | $5,250/mo at 150 users | Very High | #5 |

**Start with ContractCraft** — shortest path to first dollar, clear pain point, zero competition at this price/feature combo.

## Shared Launch Playbook (All Concepts)

1. Build MVP in 1 week: core flow only, no extras
2. ProductHunt launch: Tuesday-Thursday, 9 AM EST
3. Twitter thread: "I built X to solve Y — here's how it works" with Loom demo
4. Reddit post: r/SideProject, r/SaaS, r/Entrepreneur (value-first, no promotion)
5. Cold email outreach: scrape 200 leads on Apollo, send from ContractCraft/ColdCraft (dogfood your own tool)
6. Lifetime deal on AppSumo: $49-79 LTD for first 500 customers to get $25K-39K upfront
7. G2/Capterra listing: free listing, collect reviews
8. SEO: target "[tool name] alternatives" and "how to [solve the problem]" keywords

## API Cost Reference

| Model | Input | Output | Use Case |
|-------|-------|--------|----------|
| claude-haiku-4-5-20251001 | $0.0008/1K | $0.0004/1K | Bulk generation, drafts |
| claude-sonnet-4-6 | $0.003/1K | $0.015/1K | Quality-critical tasks |
| gpt-4o-mini | $0.00015/1K | $0.0006/1K | Cheapest fallback |
| Whisper | $0.006/min | — | Voice transcription |
