# Automated DM Outreach as a Productized Service

## What
A done-for-you Instagram/LinkedIn/Twitter DM outreach service that uses AI to find prospects, personalize messages, and manage responses -- sold as a flat monthly package to B2B founders and agencies.

## Why Now
- r/slavelabour THIS WEEK: "Instagram Outreach -- $0.20 per DM" task posted (14 upvotes). People are paying humans $0.20/DM when Claude + Playwright can do it for $0.002/DM.
- r/slavelabour THIS WEEK: "Need VA for cold DMs and Zillow scraping" -- direct demand signal for exactly this service
- Leadverse.ai (mentioned in r/microsaas, 69 upvotes) monitors Reddit/X/LinkedIn/Facebook for buying signals and automates DM outreach -- hit 100 paying customers in 260 days
- The r/microsaas conversion data point is key: the founder who went from 0 to 5-10 customers/day said the conversion tweak was removing friction from the onboarding path. DM outreach services have the simplest possible onboarding: "give us your target audience description, we send DMs"
- We already have Playwright infrastructure, 37 scrapers, and Claude for personalization. This is packaging existing capabilities as a service.

## How to Execute
1. Package our existing Playwright + Claude infrastructure as a managed service
2. Client fills a form: target audience, value prop, CTA. We configure the scraper + message generator.
3. System scrapes target profiles from LinkedIn/Instagram/Twitter, generates personalized DMs via Claude, sends via Playwright automation
4. Client gets a dashboard showing DMs sent, replies received, meetings booked
5. Charge $297-497/mo for 500-1000 DMs/month

## Stack
Python (Playwright automation), Claude API (message personalization), Next.js (client dashboard), Stripe (billing), existing scraper infrastructure from AUTOMATIONS/

## Startup Cost
$0 (existing Playwright + Claude infrastructure, Stripe already live)

## Time to First Revenue
3-5 days. We already have the automation stack. Package it, create a Stripe payment link, post on r/slavelabour as an [Offer] and on r/Entrepreneur as a case study.

## Monthly Potential
$1,500-5,000. At $297/mo with 5-17 clients. Leadverse.ai proved 100 customers is achievable. Even at a lower price point of $49/mo (self-serve version), 100 customers = $4,900/mo.

## Competition
MEDIUM. Manual VAs charge $200-500/mo for 100-300 DMs. Tools like Leadverse.ai ($49/mo self-serve) exist but don't do done-for-you. The gap is a productized service layer between cheap VAs ($3.25/hr) and expensive agencies ($2K+/mo). Our automated version delivers 10x the volume at VA pricing.

## First 3 Steps
1. TODAY: Create a landing page on Vercel with 3 packages: Starter (300 DMs/mo, $197), Growth (700 DMs/mo, $397), Scale (1500 DMs/mo, $697). Wire Stripe payment links.
2. TOMORROW: Post on r/slavelabour as [Offer], post on r/Entrepreneur showing "How I automated Instagram outreach for a local business and booked 12 calls in 2 weeks" (use our own testing data).
3. DAY 3-5: When first customer pays, configure their campaign using existing Playwright scraper + Claude message generator. Deliver first batch of DMs within 24 hours of payment.

## Score: 8.2/10
- Market Size: 8 (every B2B founder needs outreach)
- Speed to Revenue: 9 (existing infrastructure, just needs packaging)
- Automation Potential: 9 (Claude + Playwright handles everything)
- Stack Fit: 9 (we literally already have all the tools)
- Low Competition: 6 (VAs and tools exist, but productized AI service is the gap)
