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
- LLM (Claude Haiku): ~$0.01
- Vite build: ~$0.005
- Hosting (Surge): $0
- **Total: ~$0.02 per site**

## Pipeline
1. User fills intake form (name, parents, grandparents, heritage)
2. Content selector picks pre-written historical blocks by region
3. LLM generates personalized family narrative (2 Haiku calls)
4. Data assembler builds 6 template data files
5. Vite builds static site from parameterized template
6. Site deployed to unique Surge subdomain
7. Ancestry affiliate CTA drives secondary revenue

## Venture Type
PRODUCT (primary) + MONETIZE (affiliate secondary)

## Codebase
`/Users/macbookpro/Documents/ancestry-research/before-you/`
- `generator/` - Node.js generation pipeline
- `template/` - Parameterized React + Vite + Tailwind template
- `landing/` - Landing page with intake form
- `content/regions/` - Pre-written historical content blocks (Ireland, Italy)

## Live URLs
- Landing: https://before-you-landing.surge.sh
- Example (personal): https://donnelly-ancestry.surge.sh
- Example (family): https://donnelly-family-heritage.surge.sh

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

## Status
ACTIVE. MVP built. Landing page live. Generator pipeline complete. Content blocks for Ireland + Italy written. Needs: Stripe integration, end-to-end test, England/Germany content, distribution launch.
