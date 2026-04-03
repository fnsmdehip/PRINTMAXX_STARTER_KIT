# WhatsApp AI CRM for Service Businesses

## What
A WhatsApp-integrated CRM that uses Claude API to auto-qualify inbound leads, book appointments, and follow up with prospects for local service businesses (HVAC, plumbing, dental, real estate agents).

## Why Now
- Proven model: r/microsaas user hit $7K/mo MRR with 160 paying customers at $49/mo in under 12 months building exactly this
- WhatsApp Business API became self-serve in 2025, removing the previous $15K/year Meta partner requirement
- Local businesses drowning in WhatsApp inquiries (especially outside US where WhatsApp > SMS)
- No incumbent has combined WhatsApp + AI lead qualification + appointment booking in a single product under $100/mo
- The $23K MRR solo SaaS pattern (r/SAAS this week, 223 upvotes) shows the niche B2B playbook works: solve one painful workflow for one type of business
- r/slavelabour showing demand for "cold DMs and Zillow scraping" at $3.25/hr -- these buyers would pay $49/mo for automation instead

## How to Execute
1. Build a Next.js dashboard that connects to WhatsApp Business Cloud API (free tier: 1,000 conversations/mo)
2. Claude API handles message classification (lead vs support vs spam), extracts intent, and generates contextual responses
3. Calendly/Cal.com integration for appointment booking when lead is qualified
4. Stripe billing at $49/mo per connected WhatsApp number

## Stack
Python (backend/Claude API), Next.js (dashboard), WhatsApp Business Cloud API (free tier), Claude API ($5-20/mo usage), Stripe (billing), Vercel (hosting)

## Startup Cost
$0 (WhatsApp Cloud API free tier + Claude API free tier for testing + Vercel free tier)

## Time to First Revenue
7-10 days. MVP = WhatsApp webhook -> Claude classifier -> auto-response + dashboard showing conversation history. Land first customer via cold DM to businesses with WhatsApp numbers on Google Maps.

## Monthly Potential
$2,000-10,000 at 40-200 customers at $49/mo. The r/microsaas validated case hit $7K/mo at 160 customers.

## Competition
LOW-MEDIUM. Existing players (Respond.io, Trengo, WATI) charge $79-199/mo and focus on enterprise. No one owns the $49/mo tier for solo service businesses with AI-first lead qualification. The Algerian car dealership post (262 upvotes on r/SideProject) shows that even custom-built desktop ERPs for niche markets get traction -- WhatsApp CRM is the horizontal version of that same unserved market.

## First 3 Steps
1. TODAY: Set up WhatsApp Business Cloud API (meta.com/business/whatsapp), create a Next.js project with webhook receiver, wire Claude API for message classification into 4 buckets (hot lead, warm lead, support question, spam)
2. DAYS 2-4: Build dashboard showing conversation threads, lead scores, auto-response templates. Add Cal.com booking link injection when lead is classified as hot.
3. DAYS 5-7: Deploy to Vercel, create Stripe payment link ($49/mo), find 5 local businesses with WhatsApp numbers listed on Google Maps (search: "plumber [city] WhatsApp"), send cold outreach offering 14-day free trial.

## Score: 8.6/10
- Market Size: 9 (every service business globally uses WhatsApp)
- Speed to Revenue: 8 (MVP buildable in a week, validated pricing)
- Automation Potential: 9 (Claude handles the hard part, minimal human involvement)
- Stack Fit: 9 (Python + Next.js + Claude API = our exact stack)
- Low Competition: 8 ($49/mo tier is wide open)
