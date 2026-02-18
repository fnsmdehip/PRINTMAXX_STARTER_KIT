# Ecom Platform Account Requirements

**Created:** 2026-02-12
**Purpose:** Which accounts need to be created (HUMAN ACTION REQUIRED) before listings can go live
**Status:** BLOCKED until accounts created

---

## ACCOUNTS NEEDED (Priority Order)

### 1. ETSY (20 listings ready)

**URL:** https://www.etsy.com/sell
**What you need:**
- Email address (use dedicated business email)
- Shop name (suggestion: PrintMaxxDigital or niche-specific name)
- Payment method: bank account or PayPal for deposits
- Credit card on file for Etsy fees ($0.20/listing)
- Business address (can be home address)

**Setup time:** 15-20 minutes
**Fees:**
- $0.20 per listing (renews every 4 months)
- 6.5% transaction fee on sale price + shipping
- 3% + $0.25 payment processing fee
- No monthly subscription required (avoid Etsy Plus initially)

**After account creation:**
1. Complete shop settings (return policy, shipping profiles)
2. Create shipping profiles for digital downloads (instant download)
3. Upload all 20 listings from `ETSY_UPLOAD_READY_20.md`
4. Set up Etsy Ads at $1/day budget for top 5 listings

**Revenue target:** 2-5 sales/day = $600-1,800/month

---

### 2. REDBUBBLE (20 listings ready)

**URL:** https://www.redbubble.com/signup
**What you need:**
- Email address
- Username (public-facing shop name)
- PayPal or bank account for payments (minimum $20 payout)

**Setup time:** 10 minutes
**Fees:**
- FREE to list (no listing fees)
- FREE to sell (Redbubble handles printing, shipping, customer service)
- You set markup % above base price (recommend 35%)
- Redbubble keeps base price, you keep markup

**After account creation:**
1. Set default markup to 35% in Account Settings
2. Complete artist profile (bio, avatar, header image)
3. Upload all 20 designs from `REDBUBBLE_UPLOAD_READY_20.md`
4. Enable ALL product types per design (more products = more search surface)

**Revenue target:** 2-4 sales/day at 35% markup = $200-400/month

---

### 3. PRINTFUL (POD fulfillment for Etsy)

**URL:** https://www.printful.com/auth/register
**What you need:**
- Email address
- Connect to Etsy store after both are set up

**Setup time:** 10 minutes
**Fees:**
- FREE to sign up
- Pay per item when order comes in (production + shipping)
- No monthly fees, no inventory
- Typical margins: 30-50% on apparel, 40-60% on accessories

**After account creation:**
1. Connect Printful to Etsy store
2. Upload design files to Printful
3. Create product listings that sync to Etsy
4. Set retail prices (aim for 40%+ margin)

**This is OPTIONAL for Phase 1.** Etsy digital products don't need Printful. Only needed when adding physical POD products.

---

### 4. PRINTIFY (Alternative to Printful)

**URL:** https://printify.com/signup
**What you need:**
- Email address
- Connect to Etsy/Shopify

**Setup time:** 10 minutes
**Fees:**
- FREE plan: up to 5 stores
- Premium: $29/mo (20% discount on all products)
- No per-listing fees

**When to use:** If Printful prices are too high for certain products. Printify has more print providers to compare pricing.

**This is OPTIONAL.** Start with Printful, add Printify later for price comparison.

---

### 5. GUMROAD (Digital products - 10+ listings ready)

**URL:** https://gumroad.com
**What you need:**
- Email address
- PayPal or Stripe for payouts
- No approval process

**Setup time:** 5 minutes
**Fees:**
- 10% flat fee on every sale (no monthly)
- Payment processing included in the 10%

**Listings ready:** `PRODUCTS/GUMROAD_READY_LISTINGS.md` (10 products)
**Revenue target:** $200-800/month from digital products

---

## ACCOUNT CREATION ORDER (Fastest Revenue First)

| Step | Platform | Time | Listings Ready | Why This Order |
|------|----------|------|----------------|----------------|
| 1 | Gumroad | 5 min | 10 products | Fastest to list, zero listing fees, instant payouts |
| 2 | Redbubble | 10 min | 20 designs | Zero fees, zero risk, Redbubble handles everything |
| 3 | Etsy | 20 min | 20 products | Highest volume platform, $0.20/listing fee |
| 4 | Printful | 10 min | Connect to Etsy | Only if adding physical POD to Etsy |
| 5 | Printify | 10 min | Backup provider | Only if Printful pricing doesn't work |

**Total setup time:** ~55 minutes for all 5 platforms
**Total listings ready to upload immediately:** 50+ (20 Etsy + 20 Redbubble + 10+ Gumroad)

---

## WHAT'S ALREADY BUILT (No Account Needed)

These are ready to upload the moment accounts exist:

| Asset | Location | Count |
|-------|----------|-------|
| Etsy listings (formatted) | `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md` | 20 |
| Redbubble listings (formatted) | `PRODUCTS/ECOM_LISTINGS_READY/REDBUBBLE_UPLOAD_READY_20.md` | 20 |
| Gumroad product listings | `PRODUCTS/GUMROAD_READY_LISTINGS.md` | 10 |
| POD design specs | `PRODUCTS/POD_DESIGNS_50.md` | 50 |
| Browser upload automation | `PRODUCTS/ECOM_LISTINGS_READY/upload_listings.py` | 1 script |

---

## WHAT STILL NEEDS TO BE CREATED (Design Files)

The listings have titles, descriptions, tags, and pricing ready. The actual design PNG files need to be generated:

**For Redbubble:** 20 designs at 4500x5400px, transparent PNG, 300 DPI
**For Etsy POD:** Same designs, plus mockup images
**For Etsy Digital:** Product files (templates, PDFs, etc.) - most are already drafted

**Design generation tools:**
- Canva Pro (free trial) for typography designs
- Kittl.com for POD-optimized designs
- ImageFX / Nano Banana for AI-generated visuals
- Photopea.com for cleanup (free)

**AI prompts for all 50 designs:** `PRODUCTS/POD_DESIGNS_50.md`

---

## PAYMENT SETUP

All platforms need payment receiving capability:

| Platform | Payout Method | Minimum Payout | Payout Schedule |
|----------|--------------|-----------------|-----------------|
| Etsy | Direct deposit or PayPal | $0 (no minimum) | Weekly on Monday |
| Redbubble | PayPal or bank transfer | $20 | 15th of each month |
| Printful | N/A (you pay them) | N/A | Per order |
| Gumroad | PayPal or Stripe | $10 | Weekly (Friday) |

**Prerequisite:** Stripe and/or PayPal account must be set up first.
- Stripe: https://dashboard.stripe.com/register
- PayPal Business: https://www.paypal.com/us/webapps/mpp/account-selection

---

## HUMAN ACTION CHECKLIST

- [ ] Create Stripe account (if not already done)
- [ ] Create PayPal Business account (if not already done)
- [ ] Create Gumroad account and upload 10 products
- [ ] Create Redbubble account and upload 20 designs
- [ ] Create Etsy account and upload 20 listings
- [ ] Connect Printful to Etsy (optional, for physical POD)
- [ ] Set Etsy Ads budget to $1/day for top 5 listings
- [ ] Share all login credentials in SECRETS/PAYMENT_INFO.md (gitignored)

**After accounts are created, run:** `python3 scripts/account_tracker.py add --platform <name> --username <user> --email <email> --status CREATED`

---

**Total revenue potential once all listed: $1,000-3,000/month across all platforms combined.**
**Time to get all listed after accounts exist: 3-4 hours.**

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
