# OPP-047: Dead Startup Idea Validator Tool

**Score:** 8.0/10 (Fit: 8, Effort: 8, ROI: 8)
**Startup Cost:** $0
**Time to First Revenue:** 3-5 days
**Monthly Potential:** $500-2,000
**Competition:** Very Low (startups.rip exists as directory, nobody built a tool on the data)

---

## What

Build a web tool where founders input their startup idea and instantly get:
1. Which dead YC startups tried something similar (from 1,736+ in the startups.rip database)
2. Why those startups failed (funding issues, market timing, team, product-market fit)
3. What to do differently (actionable lessons from each failure)
4. Competitive landscape of current live competitors
5. "Viability Score" (0-100) based on failure patterns + current market conditions

Free: 3 checks/day. Premium: $19/mo unlimited + detailed failure analysis + CSV export.

## Why NOW

- startups.rip just launched and went viral (977 likes, 107 RTs, 66 comments on Twitter — ALPHA20257)
- 1,736+ dead YC startups with deep analysis = massive validated dataset
- Every founder googles "has someone tried this before" — this tool IS that search
- YC's Spring 2026 RFS (Request for Startups) has 7-8 new ideas — founders will want to validate them
- Failure analysis is underserved: everyone builds "idea validation" tools focused on success. Nobody focuses on failure patterns.
- Our Playwright + Python scraping stack can extract and structure the startups.rip data

## How (First 3 Steps)

1. **Day 1:** Scrape/structure startups.rip data into a clean JSON database. Extract: company name, category, funding, failure reason, description, year, YC batch. Store in SQLite.
2. **Day 2-3:** Build Next.js frontend:
   - Input: "Describe your startup idea in 1-2 sentences"
   - Claude API matches idea against dead startup database using semantic search
   - Output: Similar dead startups, failure reasons, lessons, viability score
   - Clean UI with shareable results page (viral loop)
3. **Day 4-5:** Add freemium paywall (Stripe, $19/mo) + launch:
   - Product Hunt launch (startup tools category)
   - Tweet: "1,736 YC startups died. I built a tool that tells you if your idea was one of them."
   - Post to r/startups, r/SaaS, Indie Hackers

## Expected ROI

- Cost: $0 (Claude Max + free hosting)
- Revenue: Freemium conversion 5% of 500 free users = 25 premium x $19 = $475/mo
- Growth: Every search result is shareable = viral loop
- Content: Each dead startup = a tweet thread (1,736 potential threads)

## Viral Mechanics

- Every result page has "Share your idea validation" button
- Weekly "Dead Startup of the Week" newsletter (drives traffic back)
- Twitter thread series: "This YC startup raised $2M and died. Here's why."
- SEO: "Is [startup idea] a good idea" long-tail pages

## Risk Assessment

- startups.rip may block scraping — mitigate by adding value (analysis layer, not just rehosting)
- Data may be incomplete — supplement with Crunchbase, PitchBook public data
- Semantic matching quality depends on Claude prompts — iterate on matching algorithm

## Stack

- Frontend: Next.js + Tailwind
- Backend: Python + Claude API + SQLite
- Data: Playwright scraper for startups.rip + structured JSON store
- Payments: Stripe ($19/mo)
- Deploy: surge.sh or Vercel
- Total monthly cost: $0

---

*Discovered: 2026-03-10 | Source: swarm_opportunity_scanner + ALPHA20257 signal | Cycle: web_search + alpha_cross_ref*
