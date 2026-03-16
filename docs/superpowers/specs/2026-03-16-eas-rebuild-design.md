# Enterprise Automation Solutions — Full Rebuild Design Spec

## What we're building

A complete rebuild of enterpriseautomation.solutions as a productized automation service business, fully integrated into the PRINTMAXX venture ecosystem. Includes: website (7 pages), legal framework, subcontractor system, and PRINTMAXX system wiring.

## Business model

- **DBA** "Enterprise Automation Solutions" under existing Wyoming LLC
- **Productized packages**: Signal Map ($1,500), Phone Pilot ($3,500), Ops Pilot ($4,500), Managed Ops ($1,500-3,000/mo)
- **Delivery**: Subcontractors follow playbooks. Owner does sales/marketing, occasional consulting.
- **Cash flow**: 50% upfront, 50% on delivery. Subcontractors paid from client funds.
- **Lead gen**: PRINTMAXX scrapers (savvy_lead_scraper, nationwide_scraper, mass_outreach) repurposed.

## Design direction

"Private Bank" aesthetic: black (#0a0a0a), gold (#c9a227), cream text (#f5f0e8), serif headings (Georgia/Playfair Display), system sans-serif body. Subtle scroll animations via IntersectionObserver. No particles, gradients, glow, stock photos.

## Website pages

1. **Home** — Hero + value props + trust signals + package overview + CTA
2. **Packages** — 4 productized tiers with scope, price, timeline
3. **Results** — Case studies with real numbers (use existing PRINTMAXX data initially, placeholder company names)
4. **Playbooks** — Free resources / lead magnets (email capture)
5. **ROI Calculator** — Interactive: input hours/rates → see savings
6. **Contact** — Smart intake form with heuristics checkboxes
7. **Book** — Cal.com scheduling embed

## Legal documents

- Client MSA (limitation of liability, IP assignment, termination)
- SOW template (fixed scope, fixed price)
- Risk Disclosure Addendum (AI error, detection, compliance)
- Subcontractor Agreement (NDA, non-compete, non-solicitation, IP assignment, milestone payments)

## PRINTMAXX integration

- Register EAS as new venture type SERVICE in venture_autonomy.py
- Add EAS ops (EAS01-EAS06) to master ops tracking
- Update CLAUDE.md with EAS venture instructions
- Update SOUL.md with EAS behavioral directives
- Add memory entry for EAS venture
- Wire lead generation pipeline (scraper → scorer → outreach → EAS)
- Add cron entries for EAS-specific automation

## Automation tools (best current, no hype traps)

- **n8n** (self-hosted, open-source) — primary automation backbone for client delivery
- **Bland AI** (100 free calls/day) — AI phone concierge
- **Cal.com** (free) — scheduling
- **Instantly.ai** ($30/mo) — cold email when ready
- **Supabase** (free tier) — backend for ROI calculator data capture
- **surge.sh** (free) — website deployment

## Success criteria

- Website deployed and live
- All legal docs written and stored in appropriate folders
- EAS registered as PRINTMAXX venture with full system wiring
- Lead pipeline connected (scrapers → EAS outreach)
- All sessions auto-load EAS context via existing system hooks
