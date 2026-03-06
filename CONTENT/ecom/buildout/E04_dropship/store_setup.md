# E04 Dropshipping Automation — Store Setup Guide

## Platform Decision Matrix

| Factor | Shopify | WooCommerce | Standalone (Next.js) |
|--------|---------|-------------|---------------------|
| Monthly cost | $39-105/mo | $10-30/mo hosting | $0-20/mo VPS |
| Transaction fees | 0.5-2% (non-Shopify Pay) | 0% | 0% |
| App ecosystem | Best (8,000+ apps) | Good (plugin-heavy) | Build yourself |
| Speed of launch | Fastest (1-3 days) | Medium (3-7 days) | Slowest (2-4 weeks) |
| SEO control | Limited | Full | Full |
| Scale ceiling | High | Medium-High | High |
| Recommended for | First store, speed to revenue | SEO-heavy, cost control | Custom automation needs |

**Verdict:** Start on Shopify. Migrate to WooCommerce or custom once hitting $10K/mo and transaction fees hurt.

---

## Shopify Store Setup SOP (Day 1-3)

### Day 1: Foundation

**1. Account creation**
- Plan: Basic ($39/mo) to start
- Upgrade to Shopify ($105/mo) when adding 2+ staff accounts or needing professional reports
- Use Shopify Payments to eliminate 2% transaction fee (saves $200/mo at $10K revenue)

**2. Theme selection**
- Free: Dawn (fast, clean, converts well)
- Paid: Impulse ($350 one-time) — better for product collections, featured drops
- Do NOT buy a theme before validating the niche. Dawn handles $0-$50K/mo fine.

**3. Domain**
- Register at Namecheap ($10/yr) not through Shopify ($14/yr, same service)
- Connect via DNS within 24-48 hours
- Naming formula: [niche keyword] + [power word] + .com
- Examples: SwiftGadget.com, EdgeSupply.com, PeakGear.co

**4. Essential pages (build before launch)**
- Home page (hero + bestseller section + trust badges + testimonials)
- Product pages (description template below)
- Collection pages (organize by niche/category)
- About page (brand story, 200 words)
- Contact page (form + response time promise)
- Shipping policy (copy template below)
- Return policy (copy template below)
- Privacy policy (generate via Shopify's built-in generator)
- Terms of service (generate via Shopify's built-in generator)
- FAQ page (12 questions minimum)

### Day 2: Product Import + Trust Setup

**5. Install apps (free tier first)**

Must-have free:
- DSers (AliExpress order fulfillment, free up to 3,000 orders/mo)
- Loox (product reviews, $9.99/mo starter)
- PageFly (page builder, free tier)

Must-have paid:
- Klaviyo ($20/mo starter, email automation)
- Tidio (live chat, $29/mo)
- ReConvert (post-purchase upsell, $7.99/mo)

Optional but high ROI:
- Postscript (SMS marketing, $0.01/message)
- Gorgias (customer support, $10/mo starter)
- Lucky Orange (heatmaps, $10/mo)

**6. Trust badge setup**
- Add to product pages: "Free Shipping Over $49" | "30-Day Returns" | "Secure Checkout"
- Use Shopify's trust badge metafields OR PageFly component
- Verified badge icons: shield, lock, star (not clip art — use SVG icons from Heroicons)

**7. Payment gateways**
- Primary: Shopify Payments (requires US/UK/CA/AU business or sole prop)
- Secondary: PayPal (adds 30% checkout completion for non-card buyers)
- Backup: Stripe direct (if Shopify Payments banned)

### Day 3: Launch Checklist

- [ ] Test checkout with real $1 charge (refund after)
- [ ] Mobile view on iPhone and Android
- [ ] Google Analytics 4 installed
- [ ] Meta Pixel installed (even without ads — builds audience data)
- [ ] Klaviyo welcome flow live (3 emails minimum)
- [ ] Abandoned cart flow live (3 emails: 1h, 24h, 72h)
- [ ] All policy pages linked in footer
- [ ] Speed test: Shopify dashboard > Online Store > Themes > Speed score > 40+ minimum

---

## Product Page Template

```
[PRODUCT NAME] — [BENEFIT HEADLINE]

[Hero paragraph — 2 sentences: what it is + who it's for]

WHY [PRODUCT NAME]:
• [Specific benefit 1 with measurable outcome]
• [Specific benefit 2]
• [Specific benefit 3]
• [Specific benefit 4]

WHAT'S INCLUDED:
• [Item 1]
• [Item 2]
• [Item 3]

SPECS:
• Material: [exact material]
• Dimensions: [L x W x H]
• Weight: [Xg / Xoz]
• Colors available: [list]

SHIPPING:
• Standard: 8-15 days (Free over $49)
• Expedited: 5-8 days ($9.99)

GUARANTEE:
30-day money-back guarantee. No questions asked.

[Review widget — Loox auto-injected]
```

---

## Shipping Policy Template

```
SHIPPING POLICY

Processing Time
Orders are processed within 1-2 business days. Orders placed on weekends
are processed the next business day.

Shipping Times
Standard Shipping: 8-15 business days
Expedited Shipping: 5-8 business days

We ship from warehouses in [US/CN/EU]. Most customers receive orders within
10-12 business days on Standard.

Free Shipping
Free standard shipping on orders over $49.

Tracking
You'll receive a tracking number by email within 2-3 business days of order.
Track your order at [tracking page URL].

Delays
During peak periods (holidays, sales events), add 3-5 business days. We'll
notify you of any major delays.

Questions? Email [support email] — we respond within 24 hours.
```

---

## Return Policy Template

```
RETURN POLICY

We offer a 30-day return policy.

To be eligible, items must be:
• Unused and in original packaging
• Returned within 30 days of delivery

Non-returnable: sale items, digital products, custom/personalized items.

How to return:
1. Email [support email] with your order number
2. We'll send a return label within 24 hours
3. Ship the item back within 7 days
4. Refund processed within 3-5 business days of receipt

Damaged or wrong item? Email us a photo — we'll ship a replacement within 2
business days, no return required.
```

---

## WooCommerce Setup (Cost-Control Path)

For when you want to avoid Shopify fees at scale:

**Hosting:** Hostinger Business ($8/mo) or Cloudways DigitalOcean ($14/mo)
**Domain:** Namecheap ($10/yr)
**Theme:** Astra Pro ($59/yr) + Elementor Free
**Plugins:**
- WooCommerce (free)
- DSers WooCommerce plugin (free)
- CartFlows (checkout optimization, $299/yr)
- MailPoet or Klaviyo for WooCommerce (email)
- Yoast SEO (free tier sufficient)
- WP Rocket (caching, $59/yr — critical for speed)

**Total WooCommerce stack:** ~$140/yr fixed + $8-14/mo hosting vs Shopify's $468/yr base

**Migration trigger:** When Shopify transaction fees exceed $200/mo (roughly $15K/mo revenue at Basic plan)

---

## Standalone Next.js Store

Build only if:
- You need custom automation (price sync, multi-supplier logic)
- Shopify/WooCommerce limits your stack
- You have dev capability or budget ($2-5K build cost)

Stack: Next.js 14 + Stripe + Prisma + PlanetScale + Vercel
Headless commerce: Medusa.js (open source Shopify alternative, free)
Time to launch: 2-4 weeks vs 3 days on Shopify
