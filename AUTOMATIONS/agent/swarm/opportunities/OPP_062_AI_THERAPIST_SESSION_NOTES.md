# OPP-062: AI Session Note Generator for Solo Therapists

**Score:** 8.5/10 (Fit: 8, Effort: 6, ROI: 9)
**Startup Cost:** $0 (Claude API via subscription)
**Time to First Revenue:** 7-10 days
**Monthly Potential:** $4,000-12,000
**Competition:** Low (SimplePractice dominates but is $69-99/mo and bloated for solo use)

## What

A focused micro-SaaS that auto-generates SOAP/DAP/BIRP therapy session notes from brief therapist input (bullet points, audio snippets, or post-session summary). Therapists spend 10-15 hours/month on documentation. We cut that to under 2 hours. Price: $49-79/mo per solo practitioner.

## Why Now

- Mental health practice software market: $2.72B in 2026, growing at 12.44% CAGR to 2035
- SimplePractice (dominant) costs $69-99/mo and bundles scheduling, billing, notes — solo therapists only need the notes piece
- Mental health therapists led the market segment in 2025 — strongest buying cohort
- Post-COVID telehealth explosion created a permanent solo practitioner wave
- Claude Sonnet 4.6 is ideal for HIPAA-adjacent structured note generation
- No existing AI-first session notes tool focused ONLY on solo practitioners
- 10-15 hrs/month admin pain = clear ROI conversation at $49/mo ($49 to save 10 hrs = $4.90/hr saved)

## How

1. Build a Next.js app with a simple form: session type, client age/gender (no PII), presenting concern, session observations (free text), treatment approach
2. Claude API generates formatted SOAP note in <5 seconds
3. User copies or downloads PDF
4. Stripe subscription at $49/mo (monthly) or $399/yr (annual)
5. No storing client data (privacy story is clean — input is minimal, output is local)
6. Distribution: therapist subreddits (r/therapists, r/psychotherapy), Psychology Today therapist forums, Cold DMs to solo practice therapist directories

## Revenue Model

- 50 paying subscribers at $49/mo = $2,450/mo
- 100 subscribers = $4,900/mo
- Annual plan push: 30% of users on $399/yr = better LTV
- Ceiling: 500 subscribers = $24,500/mo before any upsells

## Expected Build Time

- Core product: 8-12 hours (Claude Code can build 80% of it)
- Note templates (SOAP, DAP, BIRP): 2 hours research + prompt engineering
- Payment integration: Stripe Checkout, 2 hours
- Landing page: 1 hour (surge.sh deploy)
- Total: ~14-16 hours to MVP

## First 3 Steps

1. Validate demand: post in r/therapists asking "what note format do you use and how long does it take?" (free research)
2. Build 3-template demo (SOAP, DAP, BIRP) with Claude API, deploy to surge for feedback
3. Cold DM 20 solo therapists from Psychology Today directory with demo link

## Stack Fit

Next.js + Claude API + Stripe. Matches our exact stack. We have app_factory pipeline that builds this. HIPAA note: we don't store PHI (Protected Health Info) — input is clinical shorthand, no client identifiers. Position as a "note drafting assistant" not a medical records system.

## Risk

- HIPAA compliance positioning: critical to word carefully — we're a drafting tool, not a records system
- SimplePractice could add this feature (but won't prioritize for solo segment fast enough)
- Churn risk: therapists are busy but sticky once habits form

## Source Signal

- Market research: Mental Health PMS market sizing (towardshealthcare.com, March 2026)
- G2 Reviews: therapists cite documentation time as top pain point
- Reddit r/therapists: 10+ posts about note fatigue, searching for tools
