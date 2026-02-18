# AI Agent-as-a-Service Playbook

**OP_ID:** D13 (proposed) / aligns with S04, A04, D09
**Revenue Range:** $2K-$25K/mo
**Automation Level:** Medium (delivery automated, sales human-in-loop)
**Phase:** 1 (launch immediately)
**Status:** NEW

---

## What This Is

Sell custom AI agents to businesses. not chatbots. AGENTS. things that actually do work: process invoices, answer support tickets, generate reports, manage inventory alerts, qualify leads, draft proposals.

the edge: Claude Code lets you build these in 2-8 hours. agencies charge $5K-$50K and take 4-8 weeks. you undercut on price AND time. every business owner who tried ChatGPT and couldn't make it useful is your customer.

---

## Market Reality (2026)

- AI agent market: $3.5B in 2025, projected $28B by 2028 (IDC)
- 73% of businesses plan to adopt AI agents by end of 2026 (Gartner)
- Average enterprise AI agent project: $15K-$150K (McKinsey)
- SMB willingness to pay: $500-$5K for custom agent (Salesforce SMB survey)
- Custom GPT Store: 10M+ GPTs created but most are garbage. quality = differentiator.
- Claude MCP ecosystem: growing fast, fewer builders than GPT Store = less competition

**Key insight:** businesses don't want "AI." they want specific outcomes. "reduce support tickets by 40%" sells. "AI-powered chatbot" doesn't.

---

## Revenue Model

### Tier 1: Quick Agents ($200-$500 each)
- Custom GPTs with specific business knowledge
- Claude Projects with tailored instructions
- Simple MCP server configurations
- Delivery: 1-2 hours build time
- Volume: 10-20/month once pipeline running
- **Revenue: $2K-$10K/mo**

### Tier 2: Workflow Agents ($1K-$3K each)
- n8n/Make.com workflows with AI decision nodes
- Multi-step agents: intake -> process -> output -> notify
- Email processing agents (read, categorize, draft replies)
- Lead qualification agents (score, route, follow up)
- Delivery: 4-8 hours build time
- Volume: 3-8/month
- **Revenue: $3K-$24K/mo**

### Tier 3: Enterprise Agents ($5K-$15K each)
- Full agent systems with multiple tools
- MCP server + custom API integrations
- RAG over company documents
- Multi-agent orchestration
- Delivery: 20-40 hours
- Volume: 1-3/month
- **Revenue: $5K-$45K/mo**

### Tier 4: Retainer ($500-$2K/mo per client)
- Ongoing agent maintenance, updates, new capabilities
- Monthly usage reports and optimization
- Priority support
- New agent builds at 50% discount
- **Revenue: $2.5K-$10K/mo (5-10 clients)**

---

## The 10 Agents That Sell Best (Build These First as Portfolio)

### 1. Support Ticket Triage Agent ($1.5K)
- Reads incoming support tickets (email, form, helpdesk)
- Categorizes by urgency/type
- Drafts response for easy ones (60-70% of tickets)
- Escalates complex ones with context summary
- **Sell to:** Any SaaS, ecom, or service business with >50 tickets/week

### 2. Lead Qualification Agent ($2K)
- Processes inbound leads from forms/email
- Scores based on custom criteria (company size, budget, timeline)
- Routes hot leads to sales immediately (Slack/email notification)
- Sends personalized nurture sequence to warm leads
- **Sell to:** B2B companies, agencies, real estate, insurance

### 3. Invoice Processing Agent ($2.5K)
- Reads invoices (PDF, email, scan)
- Extracts key data (amount, vendor, date, line items)
- Matches against POs
- Flags discrepancies
- Exports to accounting software (QuickBooks, Xero)
- **Sell to:** Any business processing >20 invoices/month

### 4. Content Repurposer Agent ($1K)
- Takes blog post / video transcript
- Generates: 5 social posts, 1 email newsletter section, 3 LinkedIn posts, 1 Twitter thread
- Matches brand voice (trained on past content)
- Schedules via Buffer/Hootsuite API
- **Sell to:** Marketing teams, agencies, content creators

### 5. Meeting Summary Agent ($800)
- Processes meeting transcripts (Otter.ai, Fireflies, manual)
- Generates: action items, decisions made, key discussion points
- Sends summary to attendees
- Tracks action item completion
- **Sell to:** Remote teams, agencies, consulting firms

### 6. RFP Response Agent ($3K)
- Ingests company capability documents
- Reads RFP requirements
- Generates draft responses section by section
- Flags sections needing human input
- Formats to submission requirements
- **Sell to:** Government contractors, IT services, consulting firms

### 7. Competitor Monitor Agent ($1.5K)
- Monitors competitor websites, pricing pages, job postings
- Alerts on changes (new product, price change, new hire = expansion)
- Weekly digest with analysis
- **Sell to:** SaaS companies, ecom brands, agencies

### 8. Customer Feedback Analyzer ($1.5K)
- Aggregates reviews from Google, Yelp, G2, App Store
- Sentiment analysis + theme extraction
- Monthly report with actionable insights
- Alerts on negative review spikes
- **Sell to:** Restaurants, SaaS, service businesses, apps

### 9. Email Outreach Personalizer ($1K)
- Takes prospect list + context
- Generates personalized first lines for each prospect
- Researches company from LinkedIn/website
- Outputs ready-to-send sequences
- **Sell to:** Sales teams, recruiters, agencies

### 10. SOC/Compliance Report Generator ($5K)
- Reads audit requirements (SOC 2, HIPAA, ISO)
- Pulls evidence from existing documentation
- Generates report sections
- Flags gaps needing human attention
- **Sell to:** Tech companies, healthcare, finance (high-ticket niche)

---

## Setup (Week 1)

### Day 1-2: Build Portfolio
```
1. Build 3 demo agents from list above (#1, #4, #5 are fastest)
2. Record Loom walkthrough of each (2-3 min)
3. Create landing page: "Custom AI Agents for Your Business"
   - Use Lovable.dev or v0.dev for rapid build
   - Hero: "Your business runs on repetitive tasks. Our AI agents handle them."
   - 3 case studies (even if self-created demos)
   - Pricing: "Starting at $500" (anchor low, upsell high)
4. Deploy on Vercel free tier
```

### Day 3-4: Build Delivery System
```
1. Create intake form (Tally.so - free):
   - What task do you want automated?
   - How many times per day/week does this happen?
   - What tools do you currently use?
   - What's your budget?
2. Create Notion project template for client work:
   - Requirements doc
   - Build log
   - Delivery checklist
   - Follow-up schedule
3. Set up Stripe for payments ($0 to start)
```

### Day 5-7: Launch Outreach
```
1. List on Fiverr: "I will build a custom AI agent for your business"
   - $200 base (simple GPT), $500 (workflow agent), $1500 (enterprise)
2. List on Upwork: "AI Agent Developer | Claude & GPT Specialist"
3. Cold email 50 businesses (target: SaaS with 10-50 employees)
   - Use lead list from AUTOMATIONS/savvy_lead_scraper.py
   - Subject: "I built an AI agent that handles [specific task]"
   - Attach 30-second Loom demo
4. Post on r/SideProject, r/ChatGPT, r/ClaudeAI, r/artificial
   - "I built an AI agent that [does specific thing] — here's how"
5. X thread: "I'm building custom AI agents for businesses. here's the first 3 I made."
```

---

## Build Process (Per Client)

### Discovery (30 min)
1. What repetitive task costs you the most time?
2. Walk me through the process step by step
3. What tools/apps do you use today?
4. What does "success" look like? (specific metric)
5. What's your timeline?

### Build (2-8 hours depending on tier)
1. Map the workflow: input -> steps -> output
2. Choose stack:
   - Simple: Custom GPT or Claude Project
   - Medium: n8n + Claude API
   - Complex: Custom MCP server + multi-tool agent
3. Build core logic first, test with real data
4. Add error handling and edge cases
5. Create documentation for client

### Delivery
1. Loom walkthrough (5-10 min showing agent in action)
2. Written documentation (how to use, how to modify, troubleshooting)
3. 30-day support window
4. Upsell: "Want me to maintain and improve this monthly? $500/mo retainer."

---

## Tech Stack (Zero or Near-Zero Cost)

| Tool | Cost | Use |
|------|------|-----|
| Claude API | $0 (use client's key or include in pricing) | Agent brain |
| n8n (self-hosted) | $0 | Workflow orchestration |
| Supabase | $0 (free tier) | Database for agent state |
| Vercel | $0 (free tier) | Host agent dashboards |
| Tally.so | $0 | Intake forms |
| Loom | $0 (free tier) | Demo videos |
| Notion | $0 (free) | Project management |
| Stripe | 2.9% + $0.30 per transaction | Payments |

**Total startup cost: $0**
**Cost per agent build: $0-$5 (API calls during development)**
**Margin: 90%+**

---

## Pricing Psychology

- Never say "AI chatbot" - say "AI agent" or "AI workflow"
- Frame as ROI: "This agent saves your team 15 hours/week. At $30/hr that's $23K/year. Investment: $2K one-time."
- Always quote monthly time savings in dollars
- Offer money-back guarantee on first agent (you won't need it, they always work)
- Retainer anchor: $500/mo is nothing for a business saving $2K/mo in labor

---

## Client Acquisition Funnel

```
Cold email (50/day) → Demo video → Discovery call → Proposal → Build → Deliver → Retainer upsell
   |                       |              |
   |                    Fiverr/Upwork  → Inbound → Same flow
   |
   X/LinkedIn content → DM → Same flow
```

**Conversion targets:**
- Cold email: 3-5% reply rate, 10-15% of replies convert
- Fiverr: 5-10 orders/month after first 10 reviews
- Upwork: 2-5 contracts/month after JSS established
- Inbound (content): 1-3 leads/week after 3 months of posting

---

## Content Strategy (Building Authority)

Post weekly on X and LinkedIn:
1. "Built an AI agent that [does X] for a [industry] client. Saved them [Y hours/week]."
2. "The exact prompt engineering I use to make agents actually reliable"
3. "Why most AI chatbots fail (and what agents do differently)"
4. "Client asked me to automate [task]. Here's the 4-hour build process."
5. Behind-the-scenes of building an agent (screenshot of n8n workflow)

**Reddit posts:**
- r/ChatGPT: "I build custom AI agents for businesses. AMA about what works and what doesn't"
- r/SaaS: "How I automated customer support triage with Claude + n8n"
- r/Entrepreneur: "Selling AI agents to small businesses. Here are my first 10 clients."

---

## Synergy Map

| Stack With | How |
|-----------|-----|
| S04 (AI Automation Agency) | Same clients, different framing. Agents = specific. Automation = broad. |
| S02 (Local Biz Website) | Add chatbot agent to every website you build. $500 upsell. |
| S08 (Cold Email Agency) | Use agents to personalize cold email at scale. Meta: sell the tool you use. |
| D12 (MCP Server Marketplace) | Open-source generic version of agents you build. Monetize via marketplace. |
| MM007 (Cold Outbound) | Use your own lead qualification agent to run your own outbound. |
| N37 (AI Workflow Marketplace) | Sell template versions of agents as digital products on Gumroad. |

---

## Risk Assessment

| Risk | Probability | Mitigation |
|------|------------|-----------|
| Client expects magic, gets tool | HIGH | Set clear expectations in discovery. Demo EXACTLY what agent will do. |
| API costs exceed pricing | LOW | Include API cost estimate in proposal. Client pays own API key for heavy use. |
| Agent breaks after delivery | MEDIUM | 30-day support window. Build with error handling + notifications. |
| Competition from no-code platforms | MEDIUM | Your edge: custom, not template. Platforms serve templates, you serve outcomes. |
| Claude/OpenAI API changes | LOW | Build abstraction layer. Switch models in minutes. |

---

## KPIs

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Agents built | 5-8 | 15-25 | 30-50 |
| Revenue | $1K-$4K | $5K-$15K | $10K-$25K |
| Retainer clients | 0-1 | 3-5 | 8-12 |
| Fiverr reviews | 3-5 | 15-20 | 40+ |
| Repeat client rate | N/A | 30%+ | 50%+ |
| Average deal size | $500 | $1.2K | $2K |

---

## Quick Start Checklist

- [ ] Build 3 demo agents (support triage, content repurposer, meeting summary)
- [ ] Record Loom demos for each
- [ ] Create landing page on Vercel
- [ ] List on Fiverr ($200/$500/$1500 tiers)
- [ ] List on Upwork (AI agent specialist profile)
- [ ] Send 50 cold emails to SaaS companies (10-50 employees)
- [ ] Post first X thread showing agents in action
- [ ] Post on r/SideProject and r/ChatGPT
- [ ] Set up Stripe for payments
- [ ] Create Notion project template
- [ ] Log method in revenue tracker: `python3 scripts/revenue_intake.py log --method D13 --amount X --source [platform]`
