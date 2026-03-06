# E01 TikTok Shop — Fulfillment SOP

## Overview

TikTok Shop requires shipment confirmation with tracking within 3 business days of order. Failure to meet this results in:
- Order cancellation
- Seller score damage
- Account suspension risk at pattern level

Every order must have tracking uploaded. This SOP ensures zero missed shipments.

---

## Fulfillment Stack

| Component | Tool | Cost |
|-----------|------|------|
| Order management | TikTok Seller Center | Free |
| Automation layer | AutoDS or DSers | $26-49/mo |
| Primary supplier | CJ Dropshipping | Free (pay per order) |
| Backup supplier | Zendrop | $49/mo if needed |
| Tracking upload | Automated via AutoDS | Included |
| Customer service | Freshdesk or email | Free tier |

---

## Daily Order Processing Routine (15 min/day)

### 8:00 AM Daily Checklist

1. **Open TikTok Seller Center** → Orders → check "Awaiting Shipment"
2. **Verify AutoDS auto-fulfillment ran overnight** — should show 0 pending if configured correctly
3. **Any manual orders?** (AutoDS misses ~2-5% — handle these manually)
4. **Check for returns/disputes** → Disputes tab → respond within 24 hours
5. **Check supplier stock levels** on hero products → if <50 units, alert supplier or activate backup

### Manual Order Process (when AutoDS fails)

1. Note order details: product, quantity, buyer name, ship address
2. Go to CJ Dropshipping → My Orders → New Order
3. Paste buyer address, select product, confirm
4. CJ generates tracking number within 24-48 hours
5. Return to TikTok Seller Center → mark order as shipped → enter tracking number
6. Done

---

## Tracking Upload SOP

TikTok requires tracking number uploaded within 72 hours of order. AutoDS handles this automatically when configured. Manual backup:

1. CJ Dropshipping emails tracking number when item ships
2. Log into Seller Center → Find order → "Arrange Shipment"
3. Select carrier (USPS, DHL, etc. — match what CJ uses)
4. Enter tracking number
5. Click Confirm

**Carriers accepted by TikTok Shop:**
- USPS
- UPS
- FedEx
- DHL
- 4PX (most CJ packages)
- YunExpress
- EMS

If CJ uses a carrier not on TikTok's list: contact TikTok seller support. They can add carriers.

---

## Returns and Refunds

### TikTok Shop Return Policy (Platform Mandated)
- Buyer has 30 days to return after delivery
- You pay return shipping if product defective
- Buyer pays return shipping if buyer's remorse
- TikTok mediates disputes — they usually side with buyer on first offense

### Return Categories

**Defective/Wrong Item:**
- Accept return immediately
- Apologize sincerely in response
- Issue refund same day return arrives
- Report defect to supplier — request replacement unit credit
- If >5% defect rate on a SKU: pause that SKU, investigate supplier

**Buyer's Remorse:**
- Accept return (mandatory if within 30 days)
- Provide return shipping label within 3 days
- Issue refund within 48 hours of receiving returned item
- Track: if same buyer pattern repeats, flag account

**Dispute (Buyer Claims Non-Delivery):**
1. Check tracking status first
2. If tracking shows delivered: respond with tracking proof
3. If tracking shows in transit: wait 2 more days, check again
4. If genuinely lost: file claim with carrier + issue refund to buyer
5. Document all disputes in spreadsheet

### Return Rate Benchmarks

| Rate | Status | Action |
|------|--------|--------|
| <3% | Excellent | No action needed |
| 3-7% | Normal | Monitor closely |
| 7-12% | Warning | Investigate product quality, description accuracy |
| >12% | Critical | Pause product immediately, source new supplier or fix description |

---

## Customer Service Templates

**Response to "Where is my order?"**
```
Hey [name], thanks for reaching out! Your order was shipped on [date] and the tracking number is [#].
Based on carrier updates, expected delivery is [date range].
If it hasn't arrived by [date+2], message me and I'll sort it out immediately.
```

**Response to "I received the wrong item"**
```
So sorry about that — that's on us.
Two options: I can send you the correct item right away (no need to return the wrong one), or give you a full refund.
Which do you prefer? Just reply and I'll handle it today.
```

**Response to "This doesn't work as advertised"**
```
That's not acceptable — sorry to hear it.
Can you send me a quick video or photo of the issue? Want to make sure I understand exactly what happened.
Either way, you'll get a replacement or refund — just want to see if this is a one-off or a batch issue I need to flag.
```

**Response to positive review:**
```
Thank you! Genuinely glad it's working for you. If you get a chance to post a TikTok about it, would love to see it.
```

---

## Inventory Management

### Minimum Stock Rules

| Sales Volume | Min Stock to Maintain | Reorder Trigger |
|-------------|----------------------|----------------|
| <20 orders/day | 50 units | When stock hits 30 |
| 20-50 orders/day | 150 units | When stock hits 75 |
| 50-100 orders/day | 300 units | When stock hits 150 |
| 100+ orders/day | 500+ units | When stock hits 300 |

For dropshipping: confirm supplier has adequate stock, not just "in stock" status. Ask directly.

### Stockout Prevention

When a product starts gaining traction (>10 orders/day):
1. Place a bulk pre-order with Alibaba for 200-500 units to be stored in CJ's US warehouse
2. Delivery time: 7-10 days sea to CJ warehouse
3. CJ fulfills from US warehouse → 3-5 day domestic shipping → reviews improve → flywheel

### CJ US Warehouse Process

1. Find CJ product → click "Check US Stock"
2. If not stocked: use "Overseas Warehouse Request" form
3. Order 100-500 units to CJ US warehouse
4. Set fulfillment preference: US warehouse first, China warehouse fallback

Cost: ~$0.50-1.50/unit storage per month. Worth it on any product doing >20 orders/day.

---

## Seller Score Maintenance

TikTok scores every seller. Low scores = lower search visibility = lower sales.

**Score Factors:**
| Factor | Weight | Target |
|--------|--------|--------|
| Shipment rate within 3 days | High | >98% |
| Order defect rate | High | <2% |
| Dispute resolution | High | <1% unresolved |
| Response time | Medium | <24 hours |
| Star rating | High | >4.5 |

**Weekly seller score audit:**
1. Seller Center → Account Health → Seller Score
2. Note any declining metrics
3. If shipment rate drops: check AutoDS configuration
4. If star rating drops: check last 20 reviews for patterns

---

## Scaling Milestones

### $0 → $5K/month
- Manual order checking daily
- AutoDS auto-fulfillment for primary supplier
- 1 hero product driving volume

### $5K → $20K/month
- AutoDS Pro tier
- CJ US warehouse stocked for hero product
- Hire VA for customer service ($200-400/mo, Philippines)
- 3-5 products in rotation

### $20K+ /month
- Bulk Alibaba ordering (2-3 week lead time, plan ahead)
- VA team: 1 CS + 1 order management
- Semi-automated dispute resolution
- Monthly supplier review meetings via Alibaba Trade Manager

---

## Emergency Protocols

**Supplier Out of Stock (Hero Product):**
1. Immediately switch to backup supplier (have this pre-identified)
2. Update product listing if delivery time changes
3. Hold all new orders if no backup available — do NOT take orders you can't fill
4. Message supplier: get restock ETA
5. If ETA >14 days: pause TikTok ads and affiliate program temporarily

**Sudden Sales Spike (Viral Video):**
1. Check current inventory immediately
2. If less than 3 days of inventory: pause ads, contact supplier for emergency stock
3. TikTok allows "out of stock" status — use it rather than miss shipment SLA
4. Message affiliates: "high volume — please slow promotion for 48 hours"
5. Never promise stock you don't have

**Account Suspension (Rare):**
1. Do NOT create a new account immediately (ban evasion)
2. Open TikTok Seller Center support ticket
3. Prepare documentation: business info, tracking records, return records
4. Most suspensions for first-time violations are reversed within 3-7 days
5. Root cause: almost always missed shipment SLA or defect rate spike
