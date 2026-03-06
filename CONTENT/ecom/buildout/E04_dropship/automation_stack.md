# E04 Dropshipping Automation — Automation Stack

## Core Principle

Automate: order fulfillment, price sync, stock sync, customer emails, review requests, upsells
Don't automate (yet): customer dispute resolution, ad creative, product selection

Manual intervention time target: under 30 min/day at $5K/mo revenue

---

## Full Automation Stack

### Tier 1: Order Automation (Zero-Touch Fulfillment)

**Tool: DSers (AliExpress) — Free up to 3,000 orders/mo**

What it automates:
- Maps Shopify products to AliExpress/CJ suppliers
- Auto-places orders on supplier when Shopify order comes in
- Syncs tracking numbers back to Shopify (triggers Shopify email to customer)
- Handles order splitting when products ship from different warehouses

Setup:
1. Install DSers from Shopify App Store
2. Connect AliExpress account (personal is fine)
3. Import products via DSers Chrome extension or URL
4. Set fulfillment to "Auto Sync" mode
5. Enable "Auto Fulfill" in DSers settings (Settings > Auto Sync Tracking Number)

Auto-fulfill settings:
- Payment method: Credit card pre-loaded in AliExpress
- Default shipping: AliExpress Standard Shipping or ePacket
- Auto-message to supplier: "Please ship without invoice or promotional materials"

**Tool: CJ Dropshipping App (Shopify)**
- Direct CJ integration — better than routing through AliExpress for CJ products
- Auto-places orders, syncs tracking, handles US warehouse routing
- Free tier: 50 auto-orders/day
- Pro ($15.99/mo): Unlimited auto-orders

**Tool: AutoDS ($26.90-$66.90/mo)**
- Use when scaling to multi-platform or needing price/stock auto-monitoring
- Auto-reprice when supplier raises/lowers price (maintains your margin)
- Auto-unpublish when supplier OOS (prevents selling items you can't fulfill)
- Price monitoring runs every 6 hours

---

### Tier 2: Email Automation (Revenue on Autopilot)

**Tool: Klaviyo ($20/mo starter, free up to 250 contacts)**

Flows to build on day 1:

**Welcome Series (3 emails)**
- Email 1 (immediate): Welcome + bestsellers + 10% off first order
- Email 2 (day 2): Brand story + why we exist + social proof
- Email 3 (day 5): FAQ + trust builders + reminder of discount

**Abandoned Cart (3 emails)**
- Email 1 (1 hour): "You left something behind" — show cart items
- Email 2 (24 hours): Social proof + "Others are buying this" scarcity
- Email 3 (72 hours): Last chance + offer small discount (5-10%)

Expected recovery rate: 5-15% of abandoned carts. At $500/day cart abandonment volume, that's $25-75/day automated.

**Post-Purchase Series (3 emails)**
- Email 1 (immediate): Order confirmation + tracking link (Shopify sends this natively)
- Email 2 (day 3): Shipping update + cross-sell related products
- Email 3 (day 12): "Your order should have arrived" + review request + referral ask

**Win-Back (for 90-day non-purchasers)**
- Email 1: "We miss you" + what's new
- Email 2 (7 days later): 15% off for returning customer
- Email 3 (14 days later): Last chance — if no open, suppress for 90 days

**Klaviyo revenue attribution at scale:**
- 1,000 email subscribers: $500-1,500/mo from email alone
- 10,000 subscribers: $5,000-15,000/mo
- Email should represent 30-40% of total store revenue

---

### Tier 3: Post-Purchase Automation (LTV Multipliers)

**Tool: ReConvert ($7.99/mo)**
- Thank-you page upsell
- One-click upsell (customer adds to order without re-entering payment)
- Birthday collector (date of birth → personalized email campaigns)
- Product cross-sells based on what was ordered

Typical uplift: 10-15% increase in average order value
At $50 AOV: ReConvert adds $5-7.50 per order average

**Tool: AfterShip ($9/mo)**
- Branded tracking page (your domain, not carrier's)
- Proactive delivery notifications (reduces "where is my order" tickets by 40%)
- Integrates with Klaviyo for trigger-based email on delivery milestones

---

### Tier 4: Customer Service Automation

**Tool: Tidio ($29/mo)**
- Live chat widget on site
- AI chatbot handles 40-60% of tickets automatically:
  - "Where is my order?" → pull tracking from AfterShip
  - "How do I return?" → show return policy
  - "Does this come in X color?" → pull product variants
- Escalation to human for: disputes, refund requests, quality complaints

**Pre-built Tidio responses to create:**
- WISMO (Where Is My Order): [pull tracking] "Your order was shipped on [date] and is expected to arrive [date]. Track here: [link]"
- Return request: "No problem! Email [address] with your order number and we'll send a prepaid label within 24 hours."
- Discount request: "Use code SAVE10 for 10% off your next order!" (generic — protects margins)
- Out of stock: "We're restocking [product] soon! Drop your email here and we'll notify you first."

---

### Tier 5: Review Automation

**Tool: Loox ($9.99/mo starter)**
- Auto-request review 7-14 days after estimated delivery
- Discount incentive for reviews with photo (adds social proof faster)
- One-click import reviews from AliExpress supplier listing (seed reviews at launch)

Review request email sequence:
- Day 12 post-ship: Photo review request (offer 10% off next order for photo)
- Day 19 (if no review): Text review request (lower ask, higher completion)

Target: 50+ reviews before scaling ads. Social proof is the #1 conversion lever.

---

### Tier 6: Inventory + Pricing Automation

**AutoDS or DSers Price Rules:**

Pricing formula automation:
```
if supplier_price < 5: multiplier = 4x (retail $20)
if supplier_price 5-10: multiplier = 3x (retail $15-30)
if supplier_price 10-20: multiplier = 2.5x (retail $25-50)
if supplier_price 20-40: multiplier = 2x (retail $40-80)
if supplier_price > 40: multiplier = 1.7x (custom pricing)
```

Stock rules:
- Auto-unpublish when quantity drops to 0
- Auto-republish when restocked
- Alert when quantity drops under 5 (manual check: find backup supplier)

---

### Tier 7: Ad + Analytics Automation

**Google Analytics 4 + Enhanced Ecommerce**
- Install via Shopify GA4 integration
- Track: add to cart, checkout started, purchase, refund events
- Set up: Conversion tracking for "Purchase" event in Google Ads

**Meta Pixel**
- Install via Shopify > Online Store > Preferences > Facebook Pixel
- Events to track: ViewContent, AddToCart, InitiateCheckout, Purchase
- Build Custom Audiences for retargeting (install pixel day 1, even before ads)

**Klaviyo SMS (Optional, Postscript $0.01/message)**
- Abandoned cart SMS: 20-30% recovery rate vs 5-15% email
- Add SMS to abandoned cart flow as first touch (1 hour)
- Compliance: TCPA compliant opt-in required — Postscript handles this

---

## Automation Launch Order

**Week 1:**
1. DSers auto-fulfillment (must have before first sale)
2. Klaviyo abandoned cart (highest ROI email flow)
3. Klaviyo welcome series

**Week 2:**
3. Loox review requests
4. Tidio chatbot (basic WISMO flow)
5. ReConvert thank-you page upsell

**Week 3:**
6. AutoDS price/stock monitoring (if using multi-supplier)
7. Klaviyo post-purchase + win-back flows
8. AfterShip tracking page

**Month 2:**
9. Postscript SMS (add to existing Klaviyo flows)
10. Analytics deep dive + A/B testing

---

## Automation Cost Summary

| Tool | Monthly Cost | When to Add |
|------|-------------|-------------|
| DSers | $0 | Day 1 |
| Klaviyo | $20 | Day 1 |
| Loox | $9.99 | Day 1 |
| Tidio | $29 | Day 3 |
| ReConvert | $7.99 | Day 7 |
| AfterShip | $9 | Day 7 |
| AutoDS | $26.90 | Month 2 |
| Postscript SMS | $0 + usage | Month 2 |
| **Total Month 1** | **$75.98/mo** | |
| **Total Month 2+** | **$102.88/mo** | |

ROI math: $103/mo automation stack → 30-40% more revenue vs manual.
At $5,000/mo store: automation stack generates $1,500-2,000/mo extra. Pays back 15-20x.
