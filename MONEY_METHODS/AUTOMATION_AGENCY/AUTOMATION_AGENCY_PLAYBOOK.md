# AI Automation Agency Playbook (n8n / Make / Zapier)

**OP_ID:** S04
**Revenue Range:** $2K-$20K/mo
**Automation Level:** Medium
**Phase:** 1 (launch now)
**Status:** ACTIVE (was NEW, promoted)

---

## What This Is

Build automated workflows for businesses using n8n, Make.com, or Zapier. the boring stuff companies do manually: move data between tools, send notifications, process forms, sync databases, generate reports.

the edge: Claude Code + n8n = you build in 2 hours what takes agencies 2 weeks. self-hosted n8n costs $0. your margin is 90%+. businesses pay $500-$5K for workflows that take you an afternoon.

this is the most underrated service play in 2026. every business with 3+ SaaS tools needs automation. most don't know it exists.

---

## Market Size

- Global iPaaS market: $11.2B in 2025, $32B by 2028 (Gartner)
- 94% of SMBs perform repetitive tasks that could be automated (Salesforce)
- Average SMB uses 37 SaaS tools (Productiv 2025 report)
- n8n: 40K+ GitHub stars, growing 200%+ YoY
- Make.com: 500K+ users
- Zapier: 2.2M+ companies

**Key insight:** businesses don't search for "iPaaS" or "automation platform." they search "how to connect Shopify to Google Sheets" or "automatic email when form is submitted." sell the outcome, not the platform.

---

## Revenue Model

### Tier 1: Simple Automations ($200-$500)
- 1-2 tool connections
- Linear workflow (trigger -> action)
- Examples: "When Stripe payment received, add to Google Sheet and send Slack notification"
- Build time: 30-60 minutes
- **Target: 10-15/month = $2K-$7.5K**

### Tier 2: Complex Workflows ($500-$2K)
- 3-5 tool connections
- Branching logic, conditional paths
- AI decision nodes (Claude API for classification/extraction)
- Examples: "When email received, classify intent, route to correct team, draft response, log in CRM"
- Build time: 2-6 hours
- **Target: 4-8/month = $2K-$16K**

### Tier 3: System Integration ($2K-$5K)
- Full business process automation
- Multiple workflows connected
- Error handling, retry logic, monitoring
- Custom webhooks and API integrations
- Examples: "Complete order fulfillment: order received -> inventory check -> supplier notification -> shipping label -> customer notification -> accounting entry"
- Build time: 8-20 hours
- **Target: 1-3/month = $2K-$15K**

### Tier 4: Retainer ($300-$1.5K/mo per client)
- Ongoing maintenance of all automations
- Monthly optimization report
- Priority support
- New automation builds at 50% off
- **Target: 5-15 clients = $1.5K-$22.5K/mo**

---

## Platform Selection Guide

| Feature | n8n | Make.com | Zapier |
|---------|-----|---------|--------|
| **Cost (self-hosted)** | $0 | N/A | N/A |
| **Cost (cloud)** | $24/mo | $10.59/mo | $29.99/mo |
| **Integrations** | 400+ | 1,800+ | 7,000+ |
| **Code execution** | Yes (JS, Python) | Limited | Limited |
| **AI integration** | Native (Claude, GPT) | Via HTTP | Limited |
| **Complexity cap** | Unlimited | High | Medium |
| **Client handoff** | Harder (self-host) | Easy | Easiest |
| **Best for** | Complex, AI-heavy | Visual, medium complexity | Simple, client self-service |

**Recommendation:**
- Build on n8n (free, unlimited, code execution, AI native)
- Deliver on Make.com (client-friendly UI, easy handoff)
- Use Zapier only if client already has Zapier account
- For AI-heavy workflows: always n8n (Claude API node is native)

---

## The 12 Automations That Sell Best

### Category 1: Lead Management ($500-$2K each)

**1. Lead Capture + CRM Sync + Notification**
- Trigger: Form submission (Typeform, Tally, website)
- Action: Create contact in CRM (HubSpot, Pipedrive)
- Action: Score lead based on form answers
- Action: If hot lead: Slack alert to sales + auto-schedule Calendly link
- Action: If warm: add to email nurture sequence
- Platforms: 42K businesses use HubSpot free CRM

**2. LinkedIn Lead Scraper + Enrichment**
- Trigger: Daily schedule
- Action: Pull new connections from LinkedIn (via Phantombuster or API)
- Action: Enrich with Clearbit/Hunter.io (email, company, role)
- Action: Score and add to CRM
- Action: If matches ICP: draft personalized outreach email
- Note: Stay within LinkedIn limits (20-25 connections/day)

### Category 2: Ecommerce ($500-$2K each)

**3. Order Fulfillment Pipeline**
- Trigger: New Shopify order
- Action: Check inventory levels
- Action: If in stock: create shipping label (ShipStation)
- Action: Send customer tracking email
- Action: Update Google Sheet/Airtable with order data
- Action: If out of stock: alert purchasing team + delay notification to customer

**4. Review Request Automation**
- Trigger: Order delivered (7 days after shipping)
- Action: Check if customer left review already
- Action: If no review: send personalized email asking for review
- Action: If negative interaction logged: skip review request
- Action: Aggregate reviews in dashboard weekly

### Category 3: Content & Marketing ($300-$1.5K each)

**5. Content Repurposing Pipeline**
- Trigger: New blog post published (WordPress webhook)
- Action: Extract key points with Claude API
- Action: Generate: 3 tweets, 1 LinkedIn post, 1 email snippet
- Action: Schedule via Buffer API
- Action: Log in content calendar (Airtable/Notion)

**6. Social Mention Monitor + Response**
- Trigger: Brand mention detected (via Mention.com or Twitter API)
- Action: Classify sentiment (Claude API)
- Action: If positive: like + thank reply (draft for approval)
- Action: If negative: alert community manager + draft response
- Action: Log all mentions in weekly report

### Category 4: Operations ($500-$3K each)

**7. Invoice Processing Pipeline**
- Trigger: Email with attachment (Gmail filter)
- Action: Extract invoice data with Claude API (vendor, amount, date, line items)
- Action: Match against POs in Airtable/Sheet
- Action: If match: auto-approve and log
- Action: If mismatch: flag for human review
- Action: Monthly summary report

**8. Meeting Notes + Action Items**
- Trigger: New transcript from Otter.ai/Fireflies (webhook)
- Action: Summarize with Claude API (decisions, action items, key points)
- Action: Create tasks in Asana/Monday.com for each action item
- Action: Send summary to all attendees via email
- Action: Add to team knowledge base (Notion)

### Category 5: HR & Internal ($500-$2K each)

**9. Employee Onboarding Sequence**
- Trigger: New hire added to HRIS
- Action: Create accounts (Google Workspace, Slack, tools)
- Action: Send welcome email with first-week schedule
- Action: Assign onboarding buddy
- Action: Schedule check-in meetings (day 1, week 1, month 1)
- Action: Track completion of onboarding tasks

**10. PTO/Absence Management**
- Trigger: PTO request form submitted
- Action: Check team calendar for conflicts
- Action: Route to manager for approval
- Action: If approved: update calendar, notify team, adjust workload
- Action: Track PTO balance

### Category 6: Finance ($1K-$3K each)

**11. Expense Report Automation**
- Trigger: Receipt photo uploaded (email or app)
- Action: Extract data with Claude API (amount, vendor, category, date)
- Action: Categorize and add to expense report
- Action: Check against policy limits
- Action: Route for approval if over threshold
- Action: Export to QuickBooks/Xero

**12. Subscription/Vendor Cost Tracker**
- Trigger: Weekly schedule
- Action: Pull transactions from bank API (Plaid)
- Action: Categorize recurring charges
- Action: Alert on new subscriptions or price increases
- Action: Monthly vendor spend report with YoY comparison

---

## Setup (Week 1)

### Day 1-2: Platform Setup
```
1. Self-host n8n (for your own builds):
   - Railway.app: $5/mo
   - OR Docker on any VPS: $4/mo (Hetzner)
   - OR local: docker run -it --rm -p 5678:5678 n8nio/n8n
2. Create Make.com account (for client delivery): Free tier = 1,000 ops/mo
3. Create Zapier account: Free tier = 100 tasks/mo
4. Set up Claude API key in n8n (HTTP Request node or native AI node)
```

### Day 3-4: Build Portfolio
```
1. Build 3 demo workflows:
   - #5 Content Repurposing (easiest to demo, every business wants this)
   - #1 Lead Capture + CRM (most common need)
   - #7 Invoice Processing (highest value, impresses decision-makers)
2. Record 2-min Loom for each showing workflow in action
3. Create before/after comparison:
   - Before: "Manual process takes 2 hours/day"
   - After: "Automated, takes 0 hours/day"
```

### Day 5-7: Launch
```
1. Landing page: "We automate your boring work"
   - Use Lovable.dev or v0.dev, deploy on Vercel
   - 3 case studies with ROI numbers
   - "Free automation audit" CTA
2. Fiverr gig: "I will build n8n, Make, or Zapier automations for your business"
   - Basic ($100): 1 simple automation
   - Standard ($350): Complex workflow
   - Premium ($1,000): Full system integration
3. Upwork profile: "Automation Specialist | n8n, Make.com, Zapier"
4. Cold email 50 businesses using this template:

Subject: you're probably doing [TASK] manually

[First name],

I noticed [COMPANY] uses [TOOL1] and [TOOL2]. Are you manually moving data between them?

I built an automation for [SIMILAR COMPANY] that eliminated 12 hours/week of manual data entry. Took me an afternoon to set up.

Want me to do a free 15-minute audit of what you could automate?

[Your name]
```

---

## Client Delivery Process

### 1. Free Audit (15 min call)
- "Walk me through your typical day. What tasks feel repetitive?"
- "What tools does your team use? How do they connect?"
- Identify 3-5 automation opportunities
- Prioritize by time saved / impact
- Send proposal within 24 hours

### 2. Proposal Template
```
AUTOMATION PROPOSAL FOR [COMPANY]

OPPORTUNITY IDENTIFIED:
[Description of manual process]

CURRENT COST:
- [X] hours/week at $[Y]/hr = $[Z]/year in labor

PROPOSED AUTOMATION:
[Description of automated workflow]

DELIVERABLES:
- Fully functional automation on [n8n/Make/Zapier]
- Documentation and training video
- 30-day support window

INVESTMENT: $[amount] one-time + $[amount]/mo maintenance (optional)

ROI: Pays for itself in [X] weeks
```

### 3. Build (2-20 hours)
- Map workflow visually first (share with client for approval)
- Build in n8n (your dev environment)
- Test with real data
- Deploy to client's Make/Zapier account (or n8n cloud)
- Record walkthrough video

### 4. Handoff
- Loom training video (5-10 min)
- Written documentation
- Test together on a live call
- 30-day support via email

---

## Upsell Ladder

```
Free audit → $350 first automation → $1K second automation → $300/mo retainer
                                                                    |
                                                              After 3 months:
                                                              → "Let me rebuild your entire workflow stack" ($5K-$15K)
                                                              → Annual contract ($3.6K-$18K)
```

---

## Client Acquisition Channels

| Channel | Strategy | Expected Volume |
|---------|----------|----------------|
| Fiverr | "I will automate your business with n8n/Make" | 5-10 orders/mo |
| Upwork | Bid on automation projects ($500-$5K range) | 2-5 contracts/mo |
| Cold email | Target SaaS companies 10-50 employees | 1-3 clients/mo |
| X/LinkedIn content | "I automated [X] for a client. saved them [Y] hours." | 1-2 inbound/mo |
| Reddit | r/zapier, r/nocode, r/smallbusiness value posts | 1 lead/mo |
| Referrals | Ask every client for 2 referrals | 1-2/mo after month 3 |
| Partner with SaaS companies | Offer as certified integration partner | Long-term play |

---

## n8n Workflow Templates (Open Source for Marketing)

Build these and open-source them on GitHub. Each drives traffic back to your service.

1. **Startup CRM Automation** - HubSpot + Slack + Google Sheets
2. **Content Calendar Autopilot** - WordPress + Buffer + Airtable
3. **Ecommerce Order Pipeline** - Shopify + ShipStation + Klaviyo
4. **AI Email Sorter** - Gmail + Claude API + Slack notifications
5. **Expense Tracker** - Receipt email + Claude extraction + Google Sheets

**Marketing play:** Open-source template -> README says "Need help customizing? [link to service page]" -> Inbound leads.

---

## Synergy Map

| Stack With | How |
|-----------|-----|
| D13 (AI Agent Service) | Agent IS an automation. Same client, bigger scope. |
| S02 (Local Biz Website) | Add automation to every website project. "Your contact form now auto-adds to CRM." |
| S08 (Cold Email Agency) | Automate your own outreach pipeline. Meta: use your product to sell your product. |
| D09 (AI Wrapper Micro-SaaS) | Productize your best automations as standalone SaaS tools. |
| N37 (AI Workflow Marketplace) | Sell automation templates on Gumroad/Whop. |
| S09 (AI Chatbot Service) | Chatbot + automation = complete business AI stack. |

---

## Cost Structure

| Item | Monthly Cost |
|------|-------------|
| n8n self-hosted | $5 (Railway.app) |
| Make.com (for client delivery) | $10.59 (Team plan) |
| Claude API (development) | $5-$20 |
| Loom Pro | $0 (free tier sufficient) |
| Domain + hosting | $0 (Vercel free) |
| **Total** | **$20-$36/mo** |

**At $2K/mo revenue: 98% margin**
**At $10K/mo revenue: 99.7% margin**

---

## Risk Assessment

| Risk | Probability | Mitigation |
|------|------------|-----------|
| Client can't maintain automation | HIGH | Retainer model. Train their team. Detailed docs. |
| Platform changes break workflows | MEDIUM | Monitor changelogs. Build with error handling. Retainer covers fixes. |
| Race to bottom on pricing | MEDIUM | Specialize in AI-powered automations. Generic automations = commodity. AI = premium. |
| Client scope creep | HIGH | Fixed-price proposals with clear deliverables. Change requests = new quote. |

---

## KPIs

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Automations built | 5-8 | 20-30 | 40-60 |
| Revenue | $1K-$3K | $5K-$12K | $10K-$20K |
| Retainer clients | 0-1 | 3-5 | 8-15 |
| Fiverr reviews | 3-5 | 15+ | 30+ |
| Avg deal size | $350 | $700 | $1.2K |
| Repeat client rate | N/A | 25% | 40% |

---

## Quick Start Checklist

- [ ] Self-host n8n (Railway or Docker)
- [ ] Build 3 demo workflows (#1, #5, #7)
- [ ] Record Loom demos
- [ ] Create landing page (Lovable.dev -> Vercel)
- [ ] List on Fiverr (3 tiers: $100/$350/$1,000)
- [ ] List on Upwork
- [ ] Cold email 50 SaaS companies
- [ ] Open-source 2 n8n templates on GitHub
- [ ] Post first X thread showing automation in action
- [ ] Set up Stripe for direct payments
