# BEFORE YOU: Ancestry Narrative Website Generator

## What It Is
AI-powered product that turns family names and heritage info into beautiful, editorial-quality narrative websites tracing ancestry across thousands of years. Users input family data via a form; system generates a scroll-driven story site combining pre-written deep history with LLM-personalized family narrative.

## Revenue Model
| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 3 generations, watermarked, 3 sections |
| Standard | $19.99 one-time | Full depth, all sections, no watermark |
| Premium | $39.99 one-time | Everything + PDF download |
| Ancestry Affiliate | ~$5-10/conversion | CTA on every generated site |

## Cost Per Generation
- LLM (Groq free tier, Llama 3.3 70B): $0.00
- Vite build: ~$0.005 compute
- Hosting (Surge): $0
- **Total: ~$0.005 per site**

## Stripe (LIVE)
| Tier | Price ID | Payment Link |
|------|----------|--------------|
| Standard | price_1TDFSyKlbvFndmYLw063OcEj | https://buy.stripe.com/4gMbJ23zygkdeBX0wn3F600 |
| Premium | price_1TDFSyKlbvFndmYL1CWPHNC0 | https://buy.stripe.com/dRm5kE9XWec551nbb13F601 |

## Pipeline
1. User fills intake form (name, parents, grandparents, heritage)
2. Content selector picks pre-written historical blocks by region
3. LLM generates personalized family narrative (2 Groq calls, $0)
4. Data assembler builds 6 template data files
5. Vite builds static site from parameterized template
6. Site deployed to unique Surge subdomain
7. Ancestry affiliate CTA drives secondary revenue

## Venture Type
PRODUCT (primary) + MONETIZE (affiliate secondary)

## Codebase
Main: `/Users/macbookpro/Documents/ancestry-research/before-you/`
Worker: `MONEY_METHODS/BEFORE_YOU/before-you/` (copy on worker node)

- `generator/` - Node.js generation pipeline + server.js API
- `generator/lib/llm-pipeline.js` - Provider-agnostic LLM (Groq/DeepSeek/Together)
- `generator/lib/content-selector.js` - Heritage-based content block selection
- `generator/lib/data-assembler.js` - Template data file generation
- `template/` - Parameterized React + Vite + Tailwind + Framer Motion template
- `landing/` - Landing page with multi-step intake form (Vite + React + Tailwind)
- `content/regions/` - Pre-written historical content blocks

## Content Coverage
| Region | Files | Status |
|--------|-------|--------|
| Ireland | deep-past.json, medieval.json, plantation.json, famine.json | Complete |
| Italy | deep-past.json, roman.json, emigration.json | Complete |
| England | deep-past.json, medieval-modern.json | Complete |
| Germany | deep-past.json, medieval-modern.json | Complete |
| Shared | ice-age.json, neolithic.json | Complete |

## Live URLs
- Landing: https://before-you-landing.surge.sh
- Example (personal): https://donnelly-ancestry.surge.sh
- Example (family): https://donnelly-family-heritage.surge.sh
- Test generation: https://rossi-test-beforeyou.surge.sh

## Current Status
ACTIVE. MVP complete. E2E pipeline verified. Stripe payment links live. Needs: backend hosting (Railway/VPS), distribution launch, PDF generation (premium tier).

## Blockers
- **Backend hosting**: server.js runs locally. Needs Railway ($5/mo) or similar for production.
- **PDF generation**: Premium tier feature not yet built.
- **Distribution**: No active distribution channels yet. See Capital Genesis for priority.

## Kill Triggers
- <$100 MRR after 60 days of active distribution
- <50 generated sites after 30 days of launch
- Narrative quality gate <70% satisfaction in user feedback

## Double-Down Triggers
- >$500 MRR in first 60 days
- >5% affiliate conversion rate sustained
- >100 generated sites/week organic

## Cross-Pollination
- Genealogy content feeds CONTENT_FARM (blog posts, Twitter threads)
- Cold email templates reusable in COLD_OUTBOUND
- LLM narrative pipeline reusable in DIGITAL_PRODUCTS (story generation)
- User testimonials feed RESEARCH (buried alpha: "ancestors discovered X")
- Template engine reusable for other vertical story generators (career, travel)
- Before You sites link to Ancestry.com affiliate (MONETIZE lane)
- Meta Ads Autonomous can drive paid traffic once organic proves conversion

## Distribution Plan (Capital Genesis Priority Order)
1. Reddit r/genealogy, r/Ancestry, r/23andme (free, high-intent)
2. Facebook Groups: genealogy, family history (free, targeted)
3. Pinterest: ancestry/family history pins (free, long-tail)
4. TikTok/Reels: "I turned my family history into a website" (free, viral potential)
5. Content Farm cross-post: genealogy threads on niche accounts
6. Meta Ads Autonomous: only after organic proves demand
