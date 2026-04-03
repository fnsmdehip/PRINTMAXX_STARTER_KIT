# Niche Vertical SaaS for Local Trade Businesses

## What
A dead-simple web app (PWA) for a single trade vertical (HVAC, plumbing, or auto repair) that replaces their WhatsApp + paper + spreadsheet workflow with: job tracking, customer database, invoicing, and AI-generated follow-up messages. One screen per function. $29-49/mo.

## Why Now
- The Algerian car dealership ERP post (262 upvotes, 95 comments on r/SideProject this week) proves the pattern: local businesses in specific verticals still run on paper and WhatsApp. The dev built a native desktop ERP and got massive traction.
- conductor.is hit $25K MRR as a solo SaaS doing ONE niche integration (accounting system connector). The lesson: hyper-niche B2B tools that solve one painful workflow for one type of business compound through word-of-mouth.
- The "$2K charge for $200 worth of work" post (202 upvotes, r/SAAS) shows B2B customers happily pay premium when the tool directly solves their workflow pain.
- The conversion data post (84 upvotes, r/microsaas) showed that removing onboarding friction was the breakthrough -- local tradespeople need ONE-SCREEN simplicity, not feature-rich dashboards.
- r/Entrepreneur "SaaS model falling apart for small businesses" post (588 upvotes) shows anger at paying for 23+ subscriptions. A single $29/mo tool that replaces 3-4 of them wins.
- Our stack (Next.js + Claude API + Stripe) is perfect for building PWAs that work offline on job sites.

## How to Execute
1. Pick ONE trade: HVAC is ideal (high ticket jobs $2K-10K, repeat customers, seasonal urgency, still running on paper/QuickBooks)
2. Build a PWA with 4 screens: Jobs (kanban: scheduled/in-progress/done), Customers (name, phone, address, job history), Invoices (generate from job, send via text/email), AI Follow-ups (Claude generates "your AC filter is due for replacement" messages based on job history)
3. Price at $29/mo (below their pain threshold, below competitor pricing)
4. Acquire customers by walking into local HVAC shops with an iPad showing the app running

## Stack
Next.js PWA (offline-capable), Claude API (follow-up message generation), Stripe (billing + invoice generation), Vercel (hosting), IndexedDB/LocalStorage (offline data)

## Startup Cost
$0 (Vercel free tier, Claude API free tier for testing, Stripe already live)

## Time to First Revenue
7-10 days. The app is simple by design -- 4 screens, no complex backend. Day 1-5: build. Day 6-7: walk into 10 local HVAC businesses with a demo on an iPad.

## Monthly Potential
$3,000-15,000. At $29/mo with 100-500 customers. conductor.is proved a solo dev can hit $25K MRR in niche B2B. HVAC alone has 100K+ businesses in the US. Capture 0.1% = 100 customers = $2,900/mo.

## Competition
LOW. Existing HVAC software (ServiceTitan, Housecall Pro) charges $200-500/mo and targets large operations. Nobody owns the $29/mo tier for 1-3 person HVAC shops. The gap is identical to what conductor.is found: big players ignore the small end of the market because it is not worth their sales team's time. But a solo dev with self-serve onboarding can capture it.

## First 3 Steps
1. TODAY: Research HVAC business workflow (Google "HVAC business management pain points reddit"). Build wireframes for 4 screens. Set up Next.js project with PWA config (next-pwa).
2. DAYS 2-5: Build the MVP. Jobs kanban with drag-and-drop status changes. Customer list with search. Invoice generator (PDF via react-pdf). AI follow-up message composer (Claude generates seasonal maintenance reminders from job history).
3. DAYS 6-10: Deploy to Vercel. Create Stripe subscription ($29/mo). Walk into 10 HVAC businesses within 20 miles with iPad demo. Offer first month free. Post before/after workflow comparison on r/HVAC and r/smallbusiness.

## Score: 8.4/10
- Market Size: 9 (100K+ HVAC businesses in US alone, expandable to other trades)
- Speed to Revenue: 8 (simple app, buildable in a week)
- Automation Potential: 7 (AI follow-ups automated, but customer acquisition requires legwork)
- Stack Fit: 9 (Next.js PWA + Claude + Stripe = exact stack)
- Low Competition: 9 (nobody at $29/mo for small trade shops)
