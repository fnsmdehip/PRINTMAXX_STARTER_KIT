# OPP_034: Vertical AI Automation Packages for Skilled Trades

**Score: 8.0/10** | **Category: SERVICE/OUTBOUND** | **Cost: $0** | **Speed: 1-2 weeks**

---

## What

Sell done-for-you AI automation packages specifically to skilled trades businesses (plumbers, electricians, HVAC, roofers, landscapers). These businesses have money, high pain, and zero technical staff. They need: automated follow-up sequences, review generation, quote-to-invoice automation, and customer scheduling. They can't afford enterprise tools ($500+/month) but will pay $200-$500 one-time + $100-$200/month.

This is a more targeted, higher-ROI version of OPP_014 (Local Biz Automation) and OPP_023 (AI Automation Agency). The differentiation: hyper-vertical focus on trades (not generic "local business") with pre-built templates they can deploy in 24 hours.

---

## Why Now

- Skilled trades market: $657B annually in the US, highly fragmented
- These businesses generate $250K-$2M/year but run operations on paper/Excel
- Existing tools (Jobber, ServiceTitan) are $49-$249/month with long learning curves — 40% churn
- AI automation (n8n + Claude API) can replicate $300/month Jobber functionality for $50/month
- Gartner: 65% of small businesses will use AI automation by 2027 (from <20% in 2024)
- Trades have PERSONAL referral networks — 1 happy client = 3-5 referrals

---

## How

**Package tier:**
- Starter ($297 one-time): Auto-reply to missed calls, review request SMS, basic CRM in Airtable
- Growth ($497 one-time + $97/month): Starter + quote follow-up, job scheduling, payment reminders
- Empire ($997 one-time + $197/month): Growth + AI customer service chatbot, weekly analytics report

**Build approach:**
1. Create n8n template pack for trades: missed call → SMS auto-reply → follow-up → review request
2. Connect with Twilio (SMS), Airtable (CRM), Google Calendar (scheduling), Stripe (invoicing)
3. Cold outreach: find plumbers/HVAC companies in local Facebook Groups and Google Maps
4. Message: "I built automation that recovers missed calls for [trade] businesses. Gets you 3-5 more jobs per month. Demo in 15 min?"

---

## Stack

n8n (automation) | Twilio (SMS) | Airtable (CRM) | Stripe (payment) | Python (lead finder from Google Maps scraping)

---

## Expected ROI

- 1 client/week at $497 = $1,988/month
- Build to 10 recurring clients at $97/month = $970/month passive
- Combined realistic Month 2: **$2,958/month**
- Month 6 (20 recurring + 4 new/month): **$6,000-$10,000/month**

---

## First 3 Steps

1. Run `python3 AUTOMATIONS/local_biz_website_scraper.py` (scored 95/100 in SaaS engine) to pull 50 plumbers and HVAC companies in target cities
2. Build the "missed call → SMS auto-reply" n8n template (3-4 hours) — this is the core demo hook
3. Send 10 cold DMs on Facebook (Business Owner groups) with: "I built X for [specific trade] that recovers Y jobs. Free demo?" — measure response rate before scaling

---

## Competitive Moat

- Vertical specificity: messaging built for trades, not generic "local biz"
- Speed: 24-hour deployment vs 2-week Jobber onboarding
- Price: 60% cheaper than Jobber/ServiceTitan
- Results-focused: charge on outcomes (recovered calls, 5-star reviews) not software seats

---

## Human Blockers

- None for outreach phase
- Twilio account ($10 to start) for SMS automation
- Stripe for payment collection

---

## Fit Assessment

We have `local_biz_website_scraper.py` (95/100 SaaS score), `local_biz_pipeline.py` (94/100), and n8n automation templates. The outbound machine exists. The product just needs to be packaged as trades-specific. This is a LEVERAGE play — use existing infrastructure, just change the targeting and messaging.

_Source: swarm_opportunity_scanner | 2026-04-01_
