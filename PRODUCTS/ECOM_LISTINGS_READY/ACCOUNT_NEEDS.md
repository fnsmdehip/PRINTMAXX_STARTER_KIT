# Account Creation Requirements - Ecom Listings

**Created:** 2026-02-12
**Status:** HUMAN ACTION REQUIRED
**Purpose:** List every account needed to go live with ecom listings

---

## PRIORITY ORDER (Do These First)

### 1. Stripe (PAYMENT - REQUIRED FIRST)

**URL:** https://dashboard.stripe.com/register
**Why First:** Gumroad, Etsy, and most platforms require Stripe or PayPal for payouts. Set this up before anything else.

**Required Info:**
- Full legal name
- Email address
- Phone number
- Date of birth
- Last 4 digits of SSN (US) or government ID
- Bank account (routing + account number) for payouts
- Business type (Individual / Sole Proprietor)
- Business address (can be home address)

**Payment Required:** No upfront cost. Stripe takes 2.9% + $0.30 per transaction.

**HUMAN ACTION FLAG:** YES - requires SSN/bank details. Cannot be automated.

**Time to Set Up:** 10-15 minutes. Instant verification for most US applicants.

---

### 2. Gumroad

**URL:** https://gumroad.com/signup
**Why:** 15 digital products ready to list (10 enhanced + 5 new). Largest immediate revenue opportunity. File: `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md`

**Required Info:**
- Email address
- Password
- Display name (use "PRINTMAXX" or brand name)
- Profile bio (use: "Tools and playbooks for solopreneurs. No fluff. Just systems that work.")
- Profile image (use brand avatar)
- Stripe connection for payouts

**Payment Required:** No upfront cost. Gumroad takes 10% flat fee on all sales.

**HUMAN ACTION FLAG:** YES - requires Stripe connection (set up Stripe first).

**Time to Set Up:** 5 minutes for account. 10-15 minutes per product listing. Budget 3-4 hours to list all 15 products.

**Post-Setup Actions:**
- [ ] Enable Gumroad Discover (marketplace visibility)
- [ ] Set up email automation (purchase trigger emails)
- [ ] Configure custom domain if available
- [ ] Upload all 15 products from GUMROAD_LISTINGS_ENHANCED.md
- [ ] Create 5 bundle products after individual products are live
- [ ] Set PWYW minimums per pricing notes in listing file

---

### 3. Etsy Seller Account

**URL:** https://www.etsy.com/sell
**Why:** 20 digital product listings ready. File: `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md`

**Required Info:**
- Email address (or Google/Facebook/Apple sign-in)
- Password
- Shop name (ideas: PrintMaxxDigitals, MaxxTemplates, MaxxStudio, MaxxPlanners)
- Shop language: English
- Shop country: United States
- Shop currency: USD
- Payment method for Etsy fees (credit/debit card)
- Bank account or PayPal for deposit payouts
- SSN or EIN for tax reporting (US sellers with $600+ revenue)

**Payment Required:** YES
- $0.20 per listing fee (20 listings = $4.00 upfront)
- 6.5% transaction fee on each sale
- 3% + $0.25 payment processing fee per sale
- Total upfront cost: ~$4.00

**HUMAN ACTION FLAG:** YES - requires payment method for listing fees + bank/PayPal for payouts.

**Time to Set Up:** 15-20 minutes for account. 5-10 minutes per listing. Budget 2-3 hours for all 20 listings.

**Post-Setup Actions:**
- [ ] Upload all 20 listings from ETSY_LISTINGS_COMPLETE.md
- [ ] Set up Shop sections (Notion Templates, Canva Templates, Printable Planners, Digital Products)
- [ ] Add shop banner and logo
- [ ] Write "About" section
- [ ] Set up shipping profiles (Digital Download = instant)
- [ ] Configure auto-replies for common questions
- [ ] Enable Etsy Ads ($1/day minimum, optional)
- [ ] Request Star Seller badge once eligible (90+ day, 95% shipping, 95% reviews, $300+ revenue)

---

### 4. Redbubble

**URL:** https://www.redbubble.com/signup
**Why:** 20 POD design listings ready. File: `PRODUCTS/ECOM_LISTINGS_READY/REDBUBBLE_LISTINGS_20.md`

**Required Info:**
- Email address
- Password
- Display name / Artist name (use "PRINTMAXX" or "MaxxDesigns")
- Profile bio
- Profile image
- PayPal email for payouts (or bank transfer in some regions)

**Payment Required:** No upfront cost. Redbubble handles production and shipping. You earn markup on base price (recommended 20-35%).

**HUMAN ACTION FLAG:** PARTIAL - account creation is straightforward, but payout requires PayPal or bank details.

**Time to Set Up:** 5 minutes for account. 5-10 minutes per design upload (need to upload actual design image files). Budget 2-3 hours for 20 designs.

**Post-Setup Actions:**
- [ ] Create design image files (4500x5400px PNG, 300 DPI, transparent background)
- [ ] Upload all 20 designs from REDBUBBLE_LISTINGS_20.md
- [ ] Enable all relevant product types per listing (t-shirts, stickers, mugs, phone cases, etc.)
- [ ] Set markup percentages (35% recommended for most products)
- [ ] Optimize tags (15 max per design, use all 15)
- [ ] Set up collections by niche (Faith, Fitness, Tech, Motivational)
- [ ] Link PayPal for payouts

**IMPORTANT NOTE:** Design image files need to be CREATED before uploading. The listing file has descriptions, tags, and product selections, but the actual PNG design files must be generated using:
- Canva (free) for text-based designs
- AI image generators (Midjourney, DALL-E, Ideogram) for illustration-based designs
- Reference: `MONEY_METHODS/APP_FACTORY/APP_ASSET_GENERATION_PROMPTS.md` for AI image prompt patterns

---

### 5. Printful (Optional, connects to Etsy)

**URL:** https://www.printful.com/auth/register
**Why:** Handles POD production and shipping for Etsy POD products. Connects directly to Etsy shop.

**Required Info:**
- Email address
- Password
- Business name (optional)
- Country

**Payment Required:** No upfront cost. Printful charges per item when an order is placed. You set the retail price on Etsy, Printful deducts production cost.

**HUMAN ACTION FLAG:** PARTIAL - account is free, but connecting to Etsy requires Etsy account to be set up first.

**Time to Set Up:** 5 minutes for account. 15-30 minutes for Etsy integration.

**Post-Setup Actions:**
- [ ] Connect Printful to Etsy shop
- [ ] Upload design files to Printful
- [ ] Create product listings in Printful (select products, mockups, pricing)
- [ ] Sync products to Etsy
- [ ] Set up billing (credit card for production costs, charged when orders come in)

---

### 6. PayPal Business (If Not Already Set Up)

**URL:** https://www.paypal.com/us/business
**Why:** Required for Redbubble payouts. Also useful as backup payment processor for other platforms.

**Required Info:**
- Email address
- Password
- Full legal name
- Business name (can be personal name for sole proprietors)
- Business type
- Phone number
- Address
- SSN or EIN
- Bank account for withdrawals

**Payment Required:** No upfront cost. PayPal takes fees on received payments (2.99% + $0.49 for standard commercial).

**HUMAN ACTION FLAG:** YES - requires SSN/bank details.

**Time to Set Up:** 10-15 minutes.

---

## ACCOUNT SETUP ORDER (Dependency Chain)

```
Step 1: Stripe (required by Gumroad, others)
   |
Step 2: PayPal Business (required by Redbubble, backup for Etsy)
   |
Step 3 (parallel):
   ├── Gumroad (connect Stripe, list 15 products)
   ├── Etsy (add payment method, list 20 products)
   └── Redbubble (connect PayPal, upload 20 designs)
   |
Step 4: Printful (connect to Etsy after Etsy is live)
```

**Total accounts to create:** 5-6 (Stripe, PayPal, Gumroad, Etsy, Redbubble, Printful)
**Total estimated setup time:** 1-2 hours for accounts, 6-10 hours for all product listings
**Total upfront cost:** ~$4 (Etsy listing fees only)

---

## WHAT'S READY TO LIST IMMEDIATELY (After Account Creation)

| Platform | Products Ready | File Location | Est. Upload Time |
|----------|---------------|---------------|-----------------|
| Gumroad | 15 products (10 enhanced + 5 new) | `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md` | 3-4 hours |
| Etsy | 20 digital product listings | `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md` | 2-3 hours |
| Redbubble | 20 POD designs | `PRODUCTS/ECOM_LISTINGS_READY/REDBUBBLE_LISTINGS_20.md` | 2-3 hours (need design files) |

**Total products ready:** 55 listings across 3 platforms

---

## BLOCKER: Design File Creation for Redbubble

Redbubble requires actual image files (PNG, 4500x5400px, 300 DPI). The listings file has all metadata (titles, tags, descriptions) but the design images must be created.

**Options for creating design files:**
1. **Canva (Free)** - Best for text-heavy designs. Create 4500x5400 artboard, add text, export PNG.
2. **Ideogram.ai (Free tier)** - Good for typography + illustration combos.
3. **Midjourney ($10/month)** - Best for illustration-heavy designs.
4. **DALL-E via ChatGPT ($20/month)** - Good for simple designs.
5. **Photopea.com (Free)** - Photoshop alternative for combining elements.

**Estimated time to create 20 design files:** 3-5 hours depending on tool and complexity.

**For Gumroad and Etsy:** Digital products (Notion templates, Canva templates, PDFs) need the actual product files created. The listings are the sales copy. The products themselves need to be built in Notion/Canva/Google Docs and exported.

---

## COST SUMMARY

| Item | Cost | When Charged |
|------|------|-------------|
| Stripe | $0 upfront | 2.9% + $0.30 per transaction |
| PayPal Business | $0 upfront | 2.99% + $0.49 per transaction |
| Gumroad | $0 upfront | 10% per sale |
| Etsy | ~$4.00 upfront | $0.20/listing + 6.5% + 3% + $0.25 per sale |
| Redbubble | $0 upfront | Production cost deducted from sale price |
| Printful | $0 upfront | Production cost per order |
| **TOTAL UPFRONT** | **~$4.00** | |

---

## REVENUE PROJECTIONS (Conservative, Month 1-3)

| Platform | Products | Avg Price | Monthly Sales Est. | Monthly Revenue |
|----------|----------|-----------|-------------------|-----------------|
| Gumroad | 15 | $32 avg | 5-15 sales | $160-$480 |
| Etsy | 20 | $8 avg | 10-30 sales | $80-$240 |
| Redbubble | 20 | $3-5 markup | 5-20 sales | $15-$100 |
| **Total** | **55** | | | **$255-$820/mo** |

These are conservative first-month estimates with zero marketing spend. Revenue scales with: SEO optimization, social media promotion, Etsy/Gumroad marketplace algorithms, paid ads, and cross-platform promotion.

---

## NEXT STEPS AFTER ACCOUNT CREATION

1. List free Gumroad lead magnet first (captures emails, marketplace visibility)
2. List $7 Funnel Teardown next (impulse buy, proves the system works)
3. Upload Etsy listings in priority order from ETSY_LISTINGS_COMPLETE.md
4. Create design files and upload to Redbubble
5. Set up cross-platform links (Gumroad thank-you pages link to Etsy, etc.)
6. Begin social media promotion using existing content from `AUTOMATIONS/content_posting/`
7. Track all revenue in `FINANCIALS/REVENUE_TRACKER.csv`
8. Log via: `python3 scripts/revenue_intake.py log --method MM_ECOM --amount $X --source gumroad`

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
