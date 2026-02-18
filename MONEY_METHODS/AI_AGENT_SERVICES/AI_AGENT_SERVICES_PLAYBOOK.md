# AI Agent Services Playbook

**Created:** 2026-02-12
**Method ID:** MM-AIAGENT
**Status:** READY TO EXECUTE
**Revenue potential:** $3,000-15,000/mo within 90 days

---

## the opportunity

the AI agent market is growing at 41.5% CAGR and projected to hit $196.6B by 2034. agencies charge $5,000-$25,000 per AI automation build. freelancers on Upwork bill $50-150/hr for the same work.

but here's the arbitrage: most of these "builds" take 2-8 hours using n8n, Dify, Claude, and existing templates. the client pays $2,000 for what takes you an afternoon. your effective hourly rate: $250-1,000/hr.

the supply side is thin. search "AI agent developer" on Upwork -- the median rate is $50/hr. search "AI automation" on Fiverr -- most gigs start at $100-500. the people charging those rates are building from scratch every time. we have templates, scripts, and working systems we've already built. we just sanitize and resell.

this is the highest-margin service play in PRINTMAXX. every automation we build for ourselves becomes a product we sell to others.

---

## SECTION 1: Service Tiers

### Tier 1: Basic ($200-500)

**what the client gets:** a custom AI assistant configured for their specific use case. system prompt engineered. knowledge base loaded. tested. documented.

**what you actually do:** write a system prompt, upload their docs to a GPT or Claude project, test it, write a 1-page setup guide. 1-3 hours of work.

**delivery format:** custom GPT (OpenAI), Claude project, or Dify app with shareable link
**turnaround:** 1-3 business days
**revisions:** 2 rounds included

**target clients:**
- small business owners who heard about ChatGPT but don't know how to make it useful
- solopreneurs who want a "virtual assistant" for specific tasks
- content creators who need a consistent AI writing voice
- coaches/consultants who want to productize their expertise into a bot

**real pricing comps (Fiverr/Upwork, Feb 2026):**
- custom GPT creation: $50-300 on Fiverr
- prompt engineering: $100-500 per project
- AI chatbot setup (basic): $100-800
- we price at $200-500 because we deliver more than a prompt -- we deliver a tested, documented system

**example deliverables:**
- "AI sales assistant trained on your product catalog that answers customer questions in your brand voice"
- "AI content writer that produces blog posts matching your existing style, trained on 50 of your articles"
- "AI email responder that drafts replies to common customer inquiries"

---

### Tier 2: Standard ($500-2,000)

**what the client gets:** a complete automation workflow. triggers, actions, integrations with their existing tools. not just AI -- AI connected to their business.

**what you actually do:** build an n8n or Make.com workflow. connect their CRM/email/calendar/Slack. add AI nodes for processing. test end-to-end. document. train them on a 30-min Loom video. 4-10 hours of work.

**delivery format:** n8n workflow (self-hosted or cloud), Make.com scenario, or Zapier setup + documentation + training video
**turnaround:** 3-7 business days
**revisions:** 3 rounds + 14 days of bug-fix support

**target clients:**
- agencies drowning in repetitive tasks (reporting, lead routing, content scheduling)
- SaaS companies that need automated onboarding or support flows
- ecom stores that want AI-powered customer service
- real estate agents/brokers wanting automated lead follow-up
- service businesses needing appointment booking + follow-up automation

**real pricing comps (Feb 2026):**
- n8n workflow automation: $500-2,000 per workflow on Upwork
- Make.com automation setup: $300-1,500 on Fiverr
- AI chatbot with CRM integration: $500-3,000
- agencies charge $2,500-15,000 for the same builds (source: HummingAgent, Digital Agency Network)
- we price at $500-2,000 which undercuts agencies while still earning $50-200/hr effective

**example deliverables:**
- "AI lead qualification system: form submission -> AI scores lead 0-100 -> routes hot leads to sales Slack channel -> cold leads get nurture email sequence"
- "AI content pipeline: topic input -> AI drafts blog post -> sends to Google Docs for review -> approved posts auto-publish to WordPress + schedule social posts via Buffer"
- "AI email triage: incoming emails -> AI categorizes (support/sales/billing/spam) -> routes to correct team member -> drafts suggested reply"

---

### Tier 3: Premium ($2,000-5,000)

**what the client gets:** a custom AI agent or multi-agent system with full integrations, data pipelines, and ongoing optimization. this is the "it just runs" tier.

**what you actually do:** architect a multi-step AI system. build custom integrations (API connections, database queries, webhook handlers). deploy on their infrastructure or ours. test extensively. provide 30-day support window. 15-40 hours of work.

**delivery format:** deployed system (n8n + Supabase + custom code) + full documentation + video walkthrough + 30-day support
**turnaround:** 7-14 business days
**revisions:** unlimited within scope + 30-day bug-fix guarantee

**target clients:**
- businesses spending $5,000+/mo on manual processes that AI can handle
- companies that tried ChatGPT internally and want a "real" implementation
- agencies that want to offer AI services to their own clients (white-label)
- funded startups that need AI features fast without hiring an ML engineer

**real pricing comps (Feb 2026):**
- custom AI agent development: $5,000-25,000 at agencies (ProductCrafters, Fulminous Software)
- AI voice agent setup: $500-5,000 setup + $200-3,000/mo ongoing (HummingAgent)
- enterprise chatbot with integrations: $3,000-25,000 (multiple sources)
- AI automation retainer: $2,000-8,000/mo (Digital Agency Network)
- we price at $2,000-5,000 per project, well below agency rates but premium on freelance marketplaces

**example deliverables:**
- "AI appointment setter: Bland.ai voice agent calls leads from your CRM -> qualifies them with 5 questions -> books qualified leads on your Cal.com -> sends you a Slack summary -> logs everything to your CRM"
- "AI competitive intelligence system: monitors 50 competitor websites daily -> detects pricing changes, new features, hiring signals -> generates weekly report -> flags urgent changes immediately"
- "multi-agent content system: AI researcher finds trending topics -> AI writer drafts posts for 3 platforms -> AI editor checks brand voice and compliance -> schedules via Buffer API -> tracks engagement -> adjusts strategy weekly"

---

### Retainer Add-On ($300-1,000/mo)

**what it is:** ongoing maintenance, monitoring, and optimization of any Tier 2 or Tier 3 build.

**what you actually do:** check workflows weekly (30 min). fix any breakages. optimize based on performance data. add new features quarterly. 2-5 hours/mo.

**why it matters:** recurring revenue. 10 retainer clients at $500/mo = $5,000/mo baseline that compounds. retainers are where the real money is -- project work is lumpy, retainers are predictable.

---

## SECTION 2: 10 Service Packages (Ready to Sell)

### Package 1: AI Customer Support Bot

**tier:** Standard ($800-1,500)
**what it does:** answers customer questions 24/7 using the client's docs, FAQ, and product info. handles 60-80% of support tickets automatically. escalates complex issues to human.
**tech stack:** Dify.ai (knowledge base + chatbot) + n8n (ticket routing) + Slack/email integration
**build time:** 5-8 hours
**client ROI:** replaces 1-2 support reps ($3,000-6,000/mo saved). AI cost: $0.10-0.50 per conversation vs $5-15 for human (HummingAgent 2026 data).
**our existing assets:** Dify already in our stack (FREE_TIER_SETUP_GUIDE.md). customer support guide at `OPS/CUSTOMER_SUPPORT_GUIDE.md`.

---

### Package 2: AI Content Generation Pipeline

**tier:** Standard ($500-1,200)
**what it does:** client inputs a topic or keyword. system outputs a complete content package: blog post draft, 5 social posts, email newsletter section, SEO metadata. all in their brand voice.
**tech stack:** n8n workflow + Claude API + Google Docs + Buffer API
**build time:** 4-6 hours
**client ROI:** replaces 10-15 hours/week of content creation ($500-1,500/mo in freelancer costs)
**our existing assets:** content distributor CLI at `ralph/loops/social_setup/output/`, content generation workflows throughout AUTOMATIONS/, copy-style.md voice system.

---

### Package 3: AI Lead Qualification System

**tier:** Standard-Premium ($1,000-2,500)
**what it does:** scores incoming leads 0-100 based on custom criteria. routes hot leads to sales immediately. nurtures warm leads with email sequences. rejects junk.
**tech stack:** n8n + Claude API + Supabase (lead database) + email integration
**build time:** 6-10 hours
**client ROI:** sales team spends 100% of time on qualified leads. close rate improves 20-40%.
**our existing assets:** `AUTOMATIONS/savvy_lead_scraper.py` has a full 0-100 scoring system. `AUTOMATIONS/lead_scoring_criteria.md` documents the scoring logic. sanitize and adapt for client use cases.

---

### Package 4: AI Email Responder

**tier:** Basic-Standard ($300-800)
**what it does:** reads incoming emails. categorizes (support/sales/billing/feedback/spam). drafts reply in client's voice. either auto-sends for simple queries or queues for human review.
**tech stack:** n8n + Claude API + Gmail/Outlook API
**build time:** 3-5 hours
**client ROI:** saves 1-2 hours/day on email. response time drops from hours to minutes.
**our existing assets:** email sequence templates at `CONTENT/email_sequences/`. cold email playbook at `MONEY_METHODS/COLD_OUTBOUND/`.

---

### Package 5: AI Data Extraction / Scraping System

**tier:** Standard-Premium ($800-2,000)
**what it does:** automatically extracts data from websites, PDFs, or documents. structures it into client's preferred format (spreadsheet, database, CRM import).
**tech stack:** Python (requests/Playwright) + Claude API for parsing + n8n for scheduling + CSV/Supabase output
**build time:** 5-10 hours
**client ROI:** replaces manual data entry ($15-25/hr VA work). handles 10-100x the volume.
**our existing assets:** `AUTOMATIONS/savvy_lead_scraper.py` (880 lines), `AUTOMATIONS/nationwide_scraper.py` (880 lines, 203 cities), `AUTOMATIONS/twitter_alpha_scraper.py`. we have production-grade scraping code that just needs client-specific targeting.

---

### Package 6: AI Social Media Manager

**tier:** Standard ($700-1,500)
**what it does:** generates platform-specific content from a single brief. schedules across channels. suggests optimal posting times based on engagement data. generates weekly performance report.
**tech stack:** n8n + Claude API + Buffer API + analytics integration
**build time:** 5-8 hours
**client ROI:** replaces social media VA ($500-2,000/mo). consistent posting without human bottleneck.
**our existing assets:** Buffer integration workflow, content calendar system at `LEDGER/CONTENT_CALENDAR_30DAY.csv`, 1,278 post templates across 5 niches.

---

### Package 7: AI Appointment Setter (Voice)

**tier:** Premium ($2,000-4,000)
**what it does:** AI calls leads from CRM. follows a natural conversation script. qualifies with pre-set questions. books qualified leads on client's calendar. sends summary to client.
**tech stack:** Bland.ai API + Cal.com + n8n + CRM integration (HubSpot/Pipedrive/Supabase)
**build time:** 10-15 hours
**client ROI:** replaces SDR ($4,000-6,000/mo salary). calls 100 leads/day vs human doing 30-50. AI never calls in sick. ROI data: 136% ROI, $45,300 annual savings, 5-month payback (HummingAgent).
**our existing assets:** `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md` (374 lines, 3 call scripts, TCPA compliance). Bland.ai free tier = 100 calls/day. Cal.com integration ready.

---

### Package 8: AI Document Processor

**tier:** Basic-Standard ($300-1,000)
**what it does:** ingests documents (contracts, invoices, reports, applications). extracts key data. populates structured fields. flags anomalies or missing information.
**tech stack:** Claude API (PDF parsing) + n8n + Google Sheets/Supabase output
**build time:** 3-6 hours
**client ROI:** replaces manual document review ($20-40/hr). 10x faster. fewer errors.
**target verticals:** law firms (contract review), accounting (invoice processing), real estate (application processing), insurance (claims processing)

---

### Package 9: AI Competitive Intelligence System

**tier:** Premium ($1,500-3,500)
**what it does:** monitors competitor websites, social accounts, job postings, and press releases. detects changes (pricing, features, hiring, partnerships). generates weekly intelligence report. flags urgent changes immediately.
**tech stack:** Python (web monitoring) + Claude API (analysis) + n8n (scheduling + alerting) + Slack/email notifications
**build time:** 10-15 hours
**client ROI:** replaces competitive intelligence analyst ($5,000-8,000/mo). always-on monitoring vs periodic manual checks.
**our existing assets:** `AUTOMATIONS/triggering_events_monitor.py` monitors SEC filings, news, job postings, Glassdoor sentiment. `AUTOMATIONS/niche_meta_detector.py` detects pattern shifts. `AUTOMATIONS/platform_meta_monitor.py` tracks algorithm changes. sanitize any one of these for client vertical.

---

### Package 10: AI Sales Assistant

**tier:** Standard-Premium ($1,000-2,500)
**what it does:** AI chatbot on client's website that qualifies visitors, answers product questions, handles objections, and books demos. trained on client's sales materials, case studies, and pricing.
**tech stack:** Dify.ai (chatbot + knowledge base) + Cal.com (booking) + n8n (CRM logging) + website embed
**build time:** 6-10 hours
**client ROI:** captures leads 24/7. converts 2-5% of website visitors vs 0.5-1% with just a contact form.
**our existing assets:** Dify setup in FREE_TIER_SETUP_GUIDE.md. service offering templates at `OPS/SERVICE_OFFERING_PACKAGES.md`.

---

## SECTION 3: Where to Sell

### 1. Fiverr (Quickest to First Sale)

**category:** Programming & Tech > AI Development > AI Agents Development
**also list under:** Programming & Tech > Chatbots, Business > AI Consulting

**what to list (5 gigs):**

| Gig Title | Starting Price | Packages |
|-----------|---------------|----------|
| I will build a custom AI chatbot for your business | $100 | Basic $100 / Standard $500 / Premium $1,500 |
| I will create an AI automation workflow with n8n or Make | $150 | Basic $150 / Standard $750 / Premium $2,000 |
| I will build an AI lead qualification system | $200 | Basic $200 / Standard $1,000 / Premium $2,500 |
| I will set up an AI voice agent for appointment booking | $500 | Basic $500 / Standard $2,000 / Premium $4,000 |
| I will create a custom GPT or Claude AI assistant | $50 | Basic $50 / Standard $200 / Premium $500 |

**Fiverr tips:**
- start at lower prices to build reviews. first 5 clients at 30-50% discount.
- Fiverr takes 20% fee. price accordingly. a $500 gig nets you $400.
- response time matters for ranking. respond to inquiries within 1 hour.
- gig videos increase conversion 40%. record a 60-second Loom showing a working demo.
- Fiverr Seller Plus ($29/mo) gives analytics and priority support. worth it after first 5 sales.

**Fiverr SEO (rank higher in search):**
- use exact keywords in gig title: "AI agent," "AI automation," "chatbot," "n8n," "Make.com"
- fill all 5 tag slots: "ai agent", "ai automation", "chatbot development", "n8n automation", "ai integration"
- FAQ section: add 3-5 questions buyers commonly ask
- portfolio: add screenshots/videos of working builds

---

### 2. Upwork (Highest Ticket)

**profile category:** AI & Machine Learning > AI Agent Development
**also apply under:** Automation > Workflow Automation, Chatbots > AI Chatbot Development

**profile strategy:**
- title: "AI Agent Developer | n8n & Claude Automation | Custom AI Systems"
- rate: $75-150/hr (Upwork median for AI is $50/hr -- price above median for quality positioning)
- portfolio: 3-5 case studies from your own builds (sanitized PRINTMAXX systems)
- specialized profiles: create separate profiles for "AI Chatbot Developer" and "Automation Engineer"

**what jobs to apply for (search these terms weekly):**
- "AI agent" -- 500+ open jobs at any time
- "AI automation" -- 300+ open jobs
- "chatbot development" -- 200+ open jobs
- "n8n automation" -- 50-100 open jobs
- "custom GPT" -- 100+ open jobs
- "AI integration" -- 200+ open jobs

**Upwork proposal template:**

```
Hi [name],

I read your brief about [specific need]. I've built similar systems before --
here's one that [specific result, e.g., "reduced support tickets by 70% for
a SaaS company"].

Quick questions to scope this properly:
1. What tools/platforms are you currently using? (CRM, email, etc.)
2. What's the expected volume? (leads/day, emails/day, etc.)
3. Do you have an existing AI budget or API keys?

I can deliver a working prototype within [3-5 days] and iterate from there.

Happy to do a quick 15-min call to understand the full scope.

[Your name]
```

**Upwork fees:** 10% on first $500 with a client, 5% after. keep long-term clients on platform for reputation, move to direct billing after trust is built.

---

### 3. Twitter/X DMs (Highest Margin, Zero Fees)

**strategy:** build in public -> demonstrate expertise -> attract inbound leads

**content flywheel:**
1. build an automation for yourself
2. tweet about it: "built an AI agent that calls 100 leads/day and books the qualified ones on my calendar. bland.ai + cal.com + n8n. total cost: $0/mo."
3. get DMs: "can you build this for my business?"
4. close at full price. no platform fees.

**tweet templates for attracting AI agent clients:**

```
built an AI system that:
- monitors 200 competitor websites
- detects price changes in real-time
- generates a report every Monday morning

took 4 hours. replaces a $5K/mo analyst.

tools: n8n + claude API + python. total monthly cost: $40.
```

```
a dental practice asked me to "automate their front desk."

here's what I built:
- AI answers phone calls (bland.ai)
- qualifies the patient
- books the appointment
- sends confirmation text

100 calls/day. $0.40 per call. replaces a $3,500/mo receptionist.
```

```
my client was spending 15 hours/week writing content for 3 platforms.

built them an AI pipeline:
- input: 1 topic
- output: blog post + 5 tweets + LinkedIn post + email newsletter

time per week now: 2 hours (review + approve).

charge: $1,200. build time: 6 hours.
```

**DM closing sequence:**
1. lead DMs you asking about a build
2. reply: "what's the specific problem you're trying to solve?"
3. they describe it
4. reply: "I've built exactly this. takes [X] days. [price range]. want me to scope it properly on a quick call?"
5. hop on 15-min Cal.com call
6. send proposal within 24 hours
7. 50% upfront, 50% on delivery

---

### 4. Cold Email to Businesses

**who to target:** businesses spending money on manual processes that AI can automate. look for:
- companies hiring for "data entry," "customer support," "social media manager" on Indeed/LinkedIn
- businesses with outdated chatbots on their website (inspect -> if it's Intercom/Drift/Zendesk, they're paying $200-500/mo for basic chat)
- agencies posting on Twitter about being "overwhelmed" or "need to scale"
- local businesses with no online booking system

**cold email template:**

```
subject: cut your [support/data entry/content] costs 60% with AI

hi [name],

i noticed [specific observation: "your website uses Intercom for chat support" / "you're hiring for a data entry role" / "your social media hasn't posted in 3 weeks"].

i build AI systems that handle this automatically. recent example: built an AI support bot for a SaaS company that resolves 70% of tickets without human intervention. took 5 days. saves them $4,000/mo.

would you be open to a 15-min call to see if something similar makes sense for [company]?

no pitch on the call. i'll audit your current workflow and tell you exactly what's automatable and what isn't. if there's no fit, I'll tell you.

[name]
[cal.com booking link]
```

**send volume:** 20-30 personalized emails per day. use Apollo.io free tier to find email addresses. send from warmed domains (not your primary).

**expected metrics:** 3-5% reply rate. 1-2% meeting rate. 1 client per 100-200 emails sent. at $1,000 average deal size, 200 emails = $1,000.

---

### 5. LinkedIn Outbound

**target:** decision-makers at companies with 10-200 employees. filter by title: "CEO," "COO," "VP Operations," "Head of Customer Success."

**connection request message (keep under 300 characters):**

```
hi [name] -- i build AI automations for [industry] companies.
saw [company] is [specific observation].
would love to share a case study that might be relevant. no pitch.
```

**after they accept, send value-first DM:**

```
hey [name], thanks for connecting.

quick question: is your team spending significant time on [specific task: customer support / data entry / content creation / lead follow-up]?

i recently built an AI system for a [similar company] that cut their [task] time by 70%. happy to share the breakdown if it's relevant to what you're working on.
```

---

## SECTION 4: Portfolio Pieces (From Our Codebase)

these are real, working systems we've built. sanitize them (remove PRINTMAXX-specific data) and use as portfolio demos.

### Portfolio Piece 1: Lead Scoring Engine

**source:** `AUTOMATIONS/savvy_lead_scraper.py` + `lead_scoring_criteria.md`
**what it shows:** quantitative lead scoring (0-100) based on website quality, online presence, review sentiment, social signals
**sanitized demo:** "AI lead scoring system for a web design agency. scrapes local business websites, scores them on 15 criteria, and prioritizes outreach."
**screenshot:** run against 10 real businesses, show the scoring output
**sell as:** Package 3 (AI Lead Qualification, $1,000-2,500)

### Portfolio Piece 2: Content Distribution System

**source:** content distributor CLI, Buffer CSV pipeline, content calendar system
**what it shows:** one input -> multi-platform content output with scheduling
**sanitized demo:** "AI content pipeline for a solopreneur. one topic produces blog post + 5 social posts + newsletter draft. scheduled across 3 platforms automatically."
**sell as:** Package 2 (AI Content Pipeline, $500-1,200) or Package 6 (AI Social Media Manager, $700-1,500)

### Portfolio Piece 3: Competitive Intelligence Monitor

**source:** `AUTOMATIONS/triggering_events_monitor.py` + `platform_meta_monitor.py` + `niche_meta_detector.py`
**what it shows:** automated monitoring of websites, news, job postings, and sentiment changes
**sanitized demo:** "AI competitive intelligence system. monitors 50 competitor websites, detects pricing changes, new features, and hiring signals. weekly report + instant alerts for urgent changes."
**sell as:** Package 9 (AI Competitive Intelligence, $1,500-3,500)

### Portfolio Piece 4: Multi-Source Data Extraction

**source:** `AUTOMATIONS/nationwide_scraper.py` (880 lines, 203 cities)
**what it shows:** large-scale data extraction with structured output
**sanitized demo:** "AI data extraction system for a sales team. extracts business data from 200 cities, structures into CRM-ready format, scores leads automatically."
**sell as:** Package 5 (AI Data Extraction, $800-2,000)

### Portfolio Piece 5: Quant Dashboard / Analytics

**source:** `AUTOMATIONS/printmaxx_quant_terminal.py` (44KB, 6-panel TUI)
**what it shows:** real-time business intelligence from multiple data sources
**sanitized demo:** "AI-powered business dashboard. aggregates data from 10+ sources, generates daily briefings, highlights anomalies and opportunities."
**sell as:** custom analytics dashboard ($2,000-5,000)

---

## SECTION 5: Cold Outreach Templates

### Template A: For SaaS Companies (Target: Customer Support Automation)

```
subject: your intercom bill is $[X]/mo. i can replace 60% of it.

hi [name],

i build AI support bots that handle tier-1 tickets automatically. one client
went from 400 tickets/week handled by 3 reps to 400 tickets handled by
1 rep + AI. the AI resolves 65% without human involvement.

your team is probably answering the same 20 questions over and over.
AI handles that. humans handle the complex stuff. everyone's happier.

build time: 5-7 days. one-time cost. your support reps focus on real problems
instead of password resets.

15-min call to see if it fits?

[name]
[booking link]
```

### Template B: For Agencies (Target: Workflow Automation)

```
subject: your team is doing 30 hours of manual work that takes AI 30 minutes

hi [name],

noticed [agency name] does [service]. i build AI automation workflows
for agencies like yours.

recent example: marketing agency was spending 15 hours/week on client
reporting. built them an AI system that pulls data from Google Analytics,
Meta Ads, and email platforms, writes the report in their template, and
sends it to clients. 15 hours -> 30 minutes.

i focus on [2-3 specific automations relevant to their agency type]:
- AI content generation (one brief -> multi-platform output)
- automated client reporting (data pull -> AI analysis -> formatted report)
- lead scoring and routing (inbound leads scored and assigned automatically)

open to a quick chat about what's eating your team's time?

[name]
[booking link]
```

### Template C: For Local Businesses (Target: AI Receptionist)

```
subject: what if your phone was answered 24/7 for $0.40/call?

hi [name],

i set up AI phone systems for [industry] practices. the AI answers calls,
qualifies patients/customers, and books appointments on your calendar.
24/7. no hold times. no missed calls.

one dental practice I set up handles 80+ calls per day. cost per call:
$0.40. that's $32/day vs a receptionist at $160/day.

the AI doesn't replace your front desk. it handles the calls they can't
get to -- after hours, during lunch, when they're with a patient.

15-min call to see the demo? i'll show you exactly how it works with
a live test call.

[name]
[booking link]
```

### Template D: For Ecom Companies (Target: AI Content + Customer Support)

```
subject: you have 500 products and 3 people writing descriptions

hi [name],

i build AI systems for ecom brands. two specific things:

1. AI product description writer: feed it your product specs, brand voice
   guide, and SEO keywords. it writes descriptions that match your existing
   style. one client went from 5 descriptions/day to 100/day.

2. AI customer service bot: handles returns, tracking, sizing questions,
   product recommendations. trained on YOUR products and policies.
   resolves 60-70% of tickets without human help.

both are one-time builds. no monthly fees from me. just the AI API cost
which runs $20-50/mo for most stores.

worth a 15-min chat?

[name]
[booking link]
```

---

## SECTION 6: Revenue Projections

### Month 1 (Ramp-Up)

| Channel | Activity | Expected Deals | Revenue |
|---------|----------|---------------|---------|
| Fiverr | list 5 gigs, first reviews at discount | 3-5 small ($100-300 avg) | $300-1,500 |
| Upwork | 3-5 proposals/day, 20/week | 1-2 projects ($500-1,500 avg) | $500-3,000 |
| Twitter | 3 build-in-public posts/week | 0-1 DM clients ($1,000 avg) | $0-1,000 |
| Cold email | 20 emails/day, 400 total | 1-2 meetings, 0-1 close ($1,000 avg) | $0-1,000 |
| **TOTAL** | | **4-9 deals** | **$800-6,500** |

### Month 3 (Established)

| Channel | Activity | Expected Deals | Revenue |
|---------|----------|---------------|---------|
| Fiverr | established gigs, 4.8+ rating | 8-15 projects ($300 avg) | $2,400-4,500 |
| Upwork | Top Rated badge, repeat clients | 3-5 projects ($1,000 avg) | $3,000-5,000 |
| Twitter | 1K+ followers, weekly build posts | 2-3 DM clients ($1,500 avg) | $3,000-4,500 |
| Cold email | refined templates, higher reply rate | 2-3 closes ($1,500 avg) | $3,000-4,500 |
| Retainers | 3-5 clients from months 1-2 | ongoing | $1,500-2,500 |
| **TOTAL** | | **18-31 deals + retainers** | **$12,900-21,000** |

### Month 6 (Scaled)

| Channel | Revenue |
|---------|---------|
| Fiverr/Upwork | $5,000-8,000 |
| Direct clients (Twitter, cold email, referrals) | $8,000-15,000 |
| Retainers (10-15 clients) | $5,000-10,000 |
| **TOTAL** | **$18,000-33,000/mo** |

---

## SECTION 7: Fulfillment Workflow

### when you get a client

```
1. SCOPE (30 min)
   - 15-min call or detailed DM exchange
   - document: what they want, what tools they use, what volume they handle
   - determine tier: Basic, Standard, or Premium

2. PROPOSAL (30 min)
   - send written scope: what you'll build, timeline, price, what's included
   - include 1-2 relevant portfolio pieces
   - payment terms: 50% upfront, 50% on delivery

3. BUILD (2-40 hrs depending on tier)
   - start from existing templates (don't build from scratch)
   - daily progress updates for Premium tier
   - test thoroughly before showing client

4. DELIVER
   - loom video walkthrough (5-15 min)
   - written documentation (how to use, how to troubleshoot)
   - handoff: credentials, access, training
   - 2-3 revision rounds included

5. FOLLOW UP (day 7 and day 30)
   - "how's the system working?"
   - fix any issues
   - ask for review/testimonial
   - pitch retainer: "want me to monitor and optimize monthly?"
   - pitch upsell: "now that [X] is automated, here's what we could do with [Y]"
```

### template library (build once, reuse forever)

every client build starts from a template. never from blank.

| Template | Location | Reuse For |
|----------|----------|-----------|
| Lead scorer | `AUTOMATIONS/savvy_lead_scraper.py` | any lead qual project |
| Web scraper | `AUTOMATIONS/nationwide_scraper.py` | any data extraction project |
| Content pipeline | content distributor + Buffer CSV | any content automation |
| Monitoring system | `AUTOMATIONS/triggering_events_monitor.py` | any competitive intel |
| Email automation | `CONTENT/email_sequences/` | any email responder |
| Voice agent | `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md` | any appointment setter |
| Chatbot | Dify.ai template | any customer support bot |
| Dashboard | `AUTOMATIONS/printmaxx_quant_terminal.py` | any analytics project |

**effective hourly rate math:** if a Standard project ($1,000) takes 6 hours, and 4 of those hours are template customization (not building from scratch), your effective rate is $167/hr. without templates, the same build takes 15 hours = $67/hr. templates are the competitive moat.

---

## SECTION 8: Pricing Strategy

### how to price

**never price by hours.** price by value.

if your AI system saves a business $5,000/mo, a one-time fee of $2,000 is a steal. they ROI in 12 days. price based on what the alternative costs (hiring someone, paying for software, losing revenue to inefficiency).

### pricing framework

```
1. what does the client currently pay for this? (salary, software, opportunity cost)
2. what does our solution save them? (time, money, errors)
3. price at 10-30% of annual savings

example:
- client pays $4,000/mo for a customer support rep
- AI handles 60% of tickets = $2,400/mo saved = $28,800/yr saved
- price: $2,500 one-time (8.7% of annual savings)
- client ROI: 31 days
```

### negotiation guardrails

| Tier | Minimum Price | Walk-Away Below |
|------|--------------|-----------------|
| Basic | $200 | $100 |
| Standard | $500 | $300 |
| Premium | $2,000 | $1,500 |
| Retainer | $300/mo | $200/mo |

**never compete on price with $20/hr freelancers.** compete on speed, quality, and proven results. if a client wants cheap, they're not your client.

### discount rules

- first 5 clients on a new platform: 30% discount (for reviews)
- bundle discount (2+ projects): 15%
- retainer commitment (6+ months): 10%
- referral from existing client: 10% for both
- never: "negotiated down" discounts. your price is your price.

---

## SECTION 9: Legal and Compliance

### contract essentials (non-negotiable)

every project gets a simple agreement covering:
1. **scope:** exactly what you're building (prevents scope creep)
2. **timeline:** delivery date with buffer
3. **payment:** 50% upfront, 50% on delivery. no net-30.
4. **IP:** client owns the delivered system. you retain rights to your templates/frameworks.
5. **liability:** you're not liable for the client's use of the system. no guarantees on specific revenue outcomes.
6. **revisions:** 2-3 rounds included. additional revisions billed hourly.
7. **support:** included window (14-30 days). after that, retainer or hourly.

### API costs disclosure

always disclose that AI systems have ongoing API costs:
- Claude API: ~$0.01-0.05 per interaction
- OpenAI API: ~$0.01-0.10 per interaction
- Bland.ai: $0.09/min connected call
- n8n self-hosted: $0 (client's server costs only)

client pays their own API costs. this is NOT your expense. make this clear upfront.

### data handling

- never store client data on personal devices longer than needed
- use client's own infrastructure where possible (their Supabase, their API keys)
- delete all client data within 30 days of project completion
- if handling PII: GDPR/CCPA compliance is on the client, but don't build systems that obviously violate it

---

## SECTION 10: Scaling Path

### solo operator ($3K-15K/mo)

- handle 5-10 projects per month personally
- use templates to keep build time low
- retainers provide baseline
- focus: quality + reviews + portfolio building

### with subcontractors ($15K-40K/mo)

- hire 1-2 freelancers from Fiverr/Upwork at $20-40/hr
- you handle sales, scoping, and quality review
- subcontractors handle the builds using your templates
- your margin: 40-60% on subcontracted work
- focus: sales machine + QA + client relationships

### productized service ($40K-100K+/mo)

- turn most common builds into fixed-scope products with fixed prices
- "AI customer support bot for ecom stores: $1,500. 5-day delivery. done."
- no custom scoping calls. buyer fills out a form. you (or your team) builds it.
- scale horizontally: more products, more niches, more volume
- focus: systems + hiring + niche specialization

### info product flywheel

every client project also becomes:
- a portfolio piece (anonymized)
- a tweet thread ("built this for a client. here's how.")
- a Gumroad product ($27-97 playbook of the method)
- a template you reuse for the next client
- a case study that sells the next client

the builds feed the content. the content feeds the pipeline. the pipeline feeds the builds. infinite loop.

---

## SECTION 11: Quick-Start Checklist

### week 1: setup

- [ ] create Fiverr account. list 3 gigs (AI chatbot, AI automation, custom GPT)
- [ ] create Upwork profile. apply to 5 AI automation jobs
- [ ] post first build-in-public tweet about an AI system you've built
- [ ] set up Cal.com for discovery calls (15-min and 30-min event types)
- [ ] sanitize 2 portfolio pieces from existing codebase
- [ ] write 3 cold email templates (support bot, automation, lead qual)
- [ ] send 10 cold emails to test response

### week 2: first clients

- [ ] offer 3-5 Fiverr gigs at 30% discount for first reviews
- [ ] submit 10 Upwork proposals
- [ ] post 3 more build-in-public tweets with demos
- [ ] send 50 cold emails
- [ ] close first paying client

### week 3-4: momentum

- [ ] deliver first projects. collect testimonials.
- [ ] update Fiverr/Upwork profiles with reviews
- [ ] refine cold email templates based on reply data
- [ ] pitch retainer to first 2 clients
- [ ] identify most-requested service. build out that template further.
- [ ] begin tracking revenue: `python3 scripts/revenue_intake.py log --method MM-AIAGENT --amount X --source fiverr`

### month 2+: scale

- [ ] raise prices 20% after 10 completed projects
- [ ] launch LinkedIn outbound (20 connections/day)
- [ ] create Gumroad product from most popular service ($27-97 DIY playbook)
- [ ] consider first subcontractor if demand exceeds 10 projects/mo
- [ ] target $5,000/mo minimum from AI agent services alone

---

## APPENDIX: Market Research Sources

pricing data and market projections sourced from:
- Fiverr AI Agent Development category (fiverr.com/categories/programming-tech/ai-coding/ai-agents-development)
- Upwork AI Agent Developers marketplace (upwork.com/hire/ai-agent-developers)
- HummingAgent 2026 AI Automation Cost Guide (hummingagent.ai)
- Digital Agency Network AI Agency Pricing Guide 2026 (digitalagencynetwork.com)
- ProductCrafters AI Agent Development Cost Report (productcrafters.io)
- NoCodeFinder AI Agent Pricing 2026 (nocodefinder.com)
- Fulminous Software AI Agent Development Cost Guide (fulminoussoftware.com)
- Upwork Artificial Intelligence Engineer Hourly Rates (upwork.com/hire/artificial-intelligence-engineers/cost)

**key data points used:**
- Upwork AI engineer median rate: $50/hr, range $35-60/hr (Upwork, Dec 2025)
- specialized AI/ML freelancers: $100-200+/hr (Jobbers.io, 2026)
- AI agent development cost: $5K-25K basic, $20K-100K mid, $150K-300K+ enterprise (ProductCrafters, 2026)
- AI automation builds: $2,500-15,000+ per project (Digital Agency Network, 2026)
- AI voice agent ROI: 136%, $45,300 annual savings, 5-month payback (HummingAgent, 2026)
- agentic AI market CAGR: 41.48% through 2030 (multiple sources)
- market projected at $196.6B by 2034 (multiple sources)
- AI chatbot cost per conversation: $0.10-0.50 vs human at $5-15 (HummingAgent, 2026)
- Fiverr AI automation gigs: $100-800 per project typical range
- Fiverr AI chatbot gigs: $100-800 per project
- agency AI retainers: $2,000-8,000/mo (Digital Agency Network)

---

**STATUS:** playbook complete. start by listing 3 Fiverr gigs and applying to 5 Upwork jobs this week.

**INTEGRATION:** log all AI agent service revenue to `FINANCIALS/REVENUE_TRACKER.csv` with method_id MM-AIAGENT. track leads in `LEDGER/FREELANCE_PIPELINE.csv`.
