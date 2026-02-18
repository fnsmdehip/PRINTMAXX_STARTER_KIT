# Subscription Model: Hybrid Usage-Based + Flat Pricing

## Source
- SaaS pricing trends 2026
- AI billing analysis
- IDC research

## Tactic
Combine flat subscription base with usage-based overages to balance predictability and value capture.

## Specific Numbers
- **59% of software companies** expect usage-based revenue to grow (18% rise from 2023)
- **42% of SaaS buyers prefer usage-based** pricing (vs 38% for flat subscriptions)
- **80% of customers report better value alignment** with usage-based pricing
- **50% of companies witnessed customer growth** from usage-based
- **66% saw revenue increase** from existing customers
- **84% of enterprises saw >6% gross margin erosion** from unmetered AI costs
- **51.7% of IT leaders find licensing models difficult** to manage
- **65% report unexpected charges** from usage-based pricing

## How It Works (Hybrid Model)
1. Base subscription tier (predictable recurring revenue)
   - Example: $99/month for 10,000 API calls
2. Usage-based overages beyond included allowance
   - Example: $0.01 per additional API call
3. Optional "fair use" caps to prevent bill shock
   - Example: Max overage $200/month

## Why Hybrid Works Best
- **Predictable base revenue** for business planning
- **Captures value from power users** via overages
- **Reduces gross margin erosion** from AI/compute costs
- **Better perceived value** than pure usage-based (80% alignment)
- **Avoids complexity** of pure usage pricing (51.7% find it difficult)

## Implementation Requirements
- Usage tracking infrastructure
- Metering system (Stripe Billing, custom)
- Clear communication of allowances and overage rates
- Billing alerts to prevent surprise charges

## Tools Needed
- Stripe Usage-Based Billing
- Orb (usage metering)
- Lago (open source usage billing)
- RevenueCat (for mobile app usage tracking)

## Pricing Model Examples
**Example 1: API SaaS**
- Starter: $29/month (5K API calls included)
- Pro: $99/month (25K API calls included)
- Overages: $0.01 per additional call

**Example 2: AI Tool**
- Base: $49/month (100 AI generations)
- Overages: $0.50 per generation
- Cap: Max $149/month total

**Example 3: Mobile App**
- Free tier: 10 exports/month
- Pro: $9.99/month (unlimited exports + premium features)
- No overages (simple conversion)

## Applicable Money Methods
- SAAS (MM004) - API, AI, compute-intensive SaaS
- APP_FACTORY (MM001) - Apps with variable usage (exports, generations)
- INFO_PRODUCTS (MM002) - Seat-based courses with usage limits

## Implementation Priority
HIGH for AI/API products, MEDIUM for simple apps (stick to flat pricing for simplicity)

## When to Use Hybrid vs Flat
**Use Hybrid if:**
- Costs scale with usage (API calls, AI inference, storage)
- Power users create gross margin issues with flat pricing
- Enterprise customers prefer usage-based (42% preference)

**Use Flat if:**
- Costs are fixed regardless of usage
- Simple product with predictable value delivery
- Consumer market (usage tracking adds friction)
- Mobile app without variable compute costs

## Anti-Patterns to Avoid
- Pure usage-based without base tier (65% unexpected charges)
- No usage caps (bill shock kills retention)
- Complex usage formulas (51.7% find it difficult)
- Hiding overage rates (transparency critical)

## 2026 Trend: Return to Simplicity
Some SaaS providers are reintroducing seat-based packages or tightening caps due to:
- AI efficiency improvements making flat pricing viable again
- Customer preference for predictability
- Reducing "gross margin erosion" from power users

**Watch for:** Flat pricing with "fair use" limits becoming more common in 2026.

## Sources
- [SaaS 3.0 Analysis: Usage-Based AI Billing Shift 2026](https://editorialge.com/saas-3-0-ai-billing-shift-analysis/)
- [Usage-Based Pricing Guide for SaaS and AI](https://www.revenera.com/blog/software-monetization/usage-based-pricing-saas-ai/)
- [2026 Guide to SaaS, AI, and Agentic Pricing Models](https://www.getmonetizely.com/blogs/the-2026-guide-to-saas-ai-and-agentic-pricing-models)
- [Usage-Based vs Subscription Pricing Pros/Cons](https://www.withorb.com/blog/usage-based-revenue-vs-subscription-revenue)
