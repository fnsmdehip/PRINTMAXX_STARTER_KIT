# Payment Integration (ALWAYS active)

## Rule: Every product/app MUST have a payment path wired before claiming "done"

### Payment Processor Routing (auto-apply)
| Product Type | Primary | Fallback | Notes |
|-------------|---------|----------|-------|
| Digital product/ebook/guide | Stripe | Whop, Gumroad | Stripe lowest fees |
| Web app premium tier | Stripe | PayPal | Stripe Checkout or Payment Links |
| SaaS subscription | Stripe | LemonSqueezy | LemonSqueezy handles taxes as MoR |
| Mobile app (iOS/Android) | RevenueCat | Stripe | RevenueCat wraps Apple/Google IAP |
| Course/community access | Whop | Gumroad, Stripe | Whop has built-in delivery |
| Template pack | Whop | Gumroad | Whop/Gumroad handle file delivery |
| International/trust-critical | PayPal | Stripe | PayPal buyer trust signal |

### Monetization routing by build type (auto-apply, no prompting)
| Build type | IAP / Subscriptions | Ads | Web payments |
|------------|--------------------|----|--------------|
| Mobile app (iOS/Android) | RevenueCat (`REVENUECAT_API_KEY`) | AdMob (`ADMOB_APP_ID`) | — |
| Web app / SaaS | — | — | Stripe (`STRIPE_SECRET_KEY`) |
| Landing page / site | — | AdMob display ads | Stripe Payment Link |
| Digital product | — | — | Stripe or Whop |

### When building ANY product or app
1. Load keys from `.env` (never hardcode). Confirm present before wiring.
2. Check `python3 AUTOMATIONS/payment_integrator.py --route PRODUCT_TYPE`
3. Mobile apps: wire `src/lib/purchases.ts` (RevenueCat) + `src/components/AdBanner.tsx` (AdMob) from base template
4. Web apps / landing pages: inject Stripe checkout snippet via `--wire-app`
5. Update `OPS/STRIPE_PRODUCTS.md` with product IDs and payment links
6. Add upgrade button with `data-upgrade` attribute to any premium tier
7. Do NOT claim "done" until at least one payment path is wired and smoke-tested

### Processor API Keys (env vars)
| Processor | Env Var | Status |
|-----------|---------|--------|
| Stripe | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY` | LIVE |
| RevenueCat | `REVENUECAT_API_KEY` | LIVE |
| AdMob | `ADMOB_APP_ID` | LIVE — ca-app-pub-5277873663568466~6431629011 |
| Whop | `WHOP_API_KEY` | NEEDS SETUP |
| PayPal | `PAYPAL_CLIENT_SECRET` | NEEDS SETUP |
| LemonSqueezy | `LEMONSQUEEZY_API_KEY` | NEEDS SETUP |
| Gumroad | `GUMROAD_ACCESS_TOKEN` | NEEDS SETUP |

### MCP Tools Available
When Stripe MCP is connected, use these tools directly:
- `mcp__Stripe__create_product` / `create_price` / `create_payment_link`
- `mcp__Stripe__list_products` / `list_prices`
- `mcp__Stripe__create_customer` / `create_subscription`
- `mcp__Stripe__retrieve_balance` (check revenue)

### Auto-Payment Check (run every session)
```
python3 AUTOMATIONS/payment_integrator.py --status
```
If products exist without payment links, create them. This is Rule 1 (SHIP NOW).

### NEVER
- Hardcode API keys in source files (use env vars / `.env`)
- Create payment links without verifying the processor account is fully onboarded
- Skip payment integration when building apps ("we'll add it later" = never)
- Use only one processor (diversify to avoid single-point holds)
- Ship a mobile app without both RevenueCat IAP and AdMob wired
- Ship a web app or landing page without a Stripe checkout or payment link

### Revenue Tracking
After payment links are live, Stripe balance check via MCP:
- `mcp__Stripe__retrieve_balance` shows available + pending
- `mcp__Stripe__list_payment_intents` shows recent transactions
- Wire into `OPS/KPI_DASHBOARD.md` for unified view
