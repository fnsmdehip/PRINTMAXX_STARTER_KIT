# E03 Ecom Arbitrage — Margin Calculator

## The Core Equation

```
Net Profit = Sale Price - COGS - All Fees - Shipping In - Prep/Overhead
ROI % = (Net Profit / COGS) × 100
```

You need BOTH numbers. High ROI on a $2 profit is worthless. Low ROI on a $40 profit is great.

**Minimum targets:**
- ROI: 30% (anything below is too thin for risk + capital cost)
- Net profit: $3.00 minimum per unit (protects against miscalculation + returns)
- Monthly profit potential: $200+ on any product you decide to scale (vol × profit)

---

## Amazon FBA Fee Breakdown (2025 current rates)

### FBA Fulfillment Fees (by size tier)

| Size Tier | Max Dimensions | Max Weight | Fee |
|---|---|---|---|
| Small standard | 15" × 12" × 0.75" | 16 oz | $3.22 |
| Large standard – 4oz or less | 18" × 14" × 8" | ≤ 4 oz | $3.77 |
| Large standard – 4oz to 8oz | 18" × 14" × 8" | 4–8 oz | $4.03 |
| Large standard – 8oz to 12oz | 18" × 14" × 8" | 8–12 oz | $4.39 |
| Large standard – 12oz to 16oz | 18" × 14" × 8" | 12–16 oz | $4.75 |
| Large standard – 1 to 1.5 lbs | 18" × 14" × 8" | 1–1.5 lb | $5.48 |
| Large standard – 1.5 to 2 lbs | 18" × 14" × 8" | 1.5–2 lb | $5.97 |
| Large standard – 2 to 3 lbs | 18" × 14" × 8" | 2–3 lb | $6.87 |
| Large standard – 3+ lbs | 18" × 14" × 8" | 3+ lb | $6.87 + $0.32/lb over 3 |
| Small oversize | 60" × 30" | ≤ 70 lb | $9.54 + $0.42/lb over 1 |
| Medium oversize | 108" | ≤ 150 lb | $19.05 + $0.42/lb over 1 |

### Amazon Referral Fees (% of sale price)

| Category | Referral Fee |
|---|---|
| Books | 15% |
| Camera & Photo | 8% |
| Consumer Electronics | 8% |
| Clothing & Accessories | 17% |
| Grocery & Gourmet | 8% (< $15) / 15% (> $15) |
| Health & Personal Care | 8% (< $10) / 15% ($10+) |
| Home & Garden | 15% |
| Kitchen | 15% |
| Lawn & Garden | 15% |
| Musical Instruments | 12% |
| Office Products | 15% |
| Pet Supplies | 15% |
| Sports & Outdoors | 15% |
| Toys & Games | 15% |
| Tools & Home Improvement | 12% (< $500) |
| Video Games | 15% |

### Storage Fees (FBA)

| Month | Standard | Oversize |
|---|---|---|
| Jan–Sep | $0.87/cu ft | $0.56/cu ft |
| Oct–Dec (Q4) | $2.40/cu ft | $1.40/cu ft |

**Key:** Items sitting in FBA > 365 days get charged aged inventory surcharge ($1.50-6.90/unit). Don't send slow movers to FBA.

---

## Full Margin Calculation — Worked Examples

### Example 1: Standard Play — Toy from Walmart

```
PRODUCT: LEGO Set (2 lbs, 12" × 10" × 4")
Buy price (Walmart clearance):    $14.99
Walmart cashback (Rakuten 3%):   -$0.45
Effective buy price:              $14.54

Shipping to FBA (2 lbs):         +$1.20  (UPS rates with carrier account ~$0.60/lb)
Prep fees (sticker, poly bag):   +$0.35

Total COGS:                       $16.09

Amazon sale price:                $32.99
Amazon referral fee (15%):       -$4.95
FBA fulfillment fee (2 lbs):     -$5.97
FBA storage (1 month avg):       -$0.15

Total revenue after fees:         $21.92

Net Profit:                       $21.92 - $16.09 = $5.83
ROI:                              $5.83 / $16.09 = 36.2% ✅
```

### Example 2: Health & Beauty — Target Clearance

```
PRODUCT: Premium shampoo 32oz (1.5 lbs)
Buy price (Target 70% clearance): $3.99
Target Circle cashback (1%):      -$0.04
Effective buy:                     $3.95

Shipping to FBA (1.5 lbs):       +$0.90
Prep fees:                        +$0.25

Total COGS:                       $5.10

Amazon sale price:                $14.99
Referral fee (8%, under $10... wait, $14.99 so 15%): -$2.25
FBA fulfillment (1.5 lbs):       -$5.48

Revenue after fees:               $7.26

Net Profit:                       $7.26 - $5.10 = $2.16
ROI:                              $2.16 / $5.10 = 42.3% ✅ (ROI good but $2.16 is borderline)

DECISION: Only buy if I can get 20+ units. $2.16 × 20 = $43.20 for that buy.
If I can only get 5 units → skip. Capital opportunity cost too high.
```

### Example 3: Loser Deal — Looks Good, Isn't

```
PRODUCT: Kitchen gadget set (3 lbs, bulky)
Buy price (Costco online):        $24.99
No cashback available:            $0

Shipping to FBA (3 lbs):         +$1.80
Prep fees:                        +$0.35

Total COGS:                       $27.14

Amazon sale price:                $39.99
Referral fee (15%):              -$6.00
FBA fulfillment (3 lbs):         -$6.87
FBA storage (Q4 bulky):          -$0.80

Revenue after fees:               $26.32

Net Profit:                       $26.32 - $27.14 = -$0.82 ❌ LOSING MONEY
ROI:                              Negative

WHY IT LOOKED GOOD: 60% price spread ($25 vs $40) seemed promising
WHY IT'S NOT: FBA fees ate the margin, plus Q4 storage spike
```

---

## Quick Mental Math Formula

When scanning fast (in-store or quick online check):

```
AMAZON PRICE × 0.65 = Your Maximum Buy Price at ~30% ROI

(This accounts for ~15% referral + ~10% FBA fees + ~5% buffer)
```

**Examples:**
- Amazon at $20 → buy for ≤ $13
- Amazon at $35 → buy for ≤ $22.75
- Amazon at $50 → buy for ≤ $32.50

This is a conservative screen — run full calc on anything that passes.

**For electronics (8% referral):**
```
AMAZON PRICE × 0.72 = Max Buy Price
```

---

## Returns and Refund Buffer

Amazon has a ~5-8% return rate depending on category.

Add this to your cost model:
- Electronics: 8% return rate
- Clothing: 15-20% (avoid)
- Toys: 5%
- Health/Beauty: 4%
- Kitchen: 6%

**Return cost per unit:**
```
Return Cost = (Sale Price × Return Rate) × (1 - Resale Recovery %)
Where Recovery % = % of returns you can relist and resell (usually 60-70% for OA)
```

**Practical buffer:** Reduce projected net profit by 5% to account for returns/damage.

---

## FBA vs FBM (Merchant Fulfilled) Comparison

| Factor | FBA | FBM |
|---|---|---|
| Fees | Higher ($3.22-9.54/unit) | Lower (just referral fee) |
| Prime badge | Yes | Only with Seller Fulfilled Prime |
| Conversion rate | ~15-25% higher | Lower without Prime |
| Storage cost | Monthly + aged | None |
| Your time | Ship to FBA once | Ship to customer each order |
| Returns | Amazon handles | You handle |
| Best for | Fast movers, standard items | Slow movers, oversized, fragile |

**Rule of thumb:** Use FBA for BSR < 100K. FBM for BSR 100K-500K (slower, but still sells).

---

## Break-Even and Scale Math

### Capital Efficiency Model

```
Monthly Revenue Target: $5,000
Average Sale Price: $25
Avg Net Profit Per Unit: $5 (20% margin after all fees)
Units Needed: 200/month

Avg Turns Per Month (30-day sell-through):
- BSR 1K-10K: 30+ turns/month
- BSR 10K-50K: 10-20 turns/month
- BSR 50K-100K: 5-10 turns/month
- BSR 100K-200K: 2-5 turns/month

Capital required at 10 turns/month:
200 units ÷ 10 = 20 units in FBA at any time
20 × $20 COGS = $400 in working capital for this SKU
```

### Scaling from $1K to $10K/mo

```
Month 1-2 (learning):
  Capital deployed: $500-1,000
  SKUs actively flipping: 5-15
  Monthly profit: $100-300

Month 3-4 (systematized):
  Capital deployed: $2,000-5,000
  SKUs: 20-50
  Monthly profit: $500-1,500

Month 5-6 (scaled):
  Capital deployed: $5,000-15,000
  SKUs: 50-100+
  Monthly profit: $1,500-4,000

Month 7-12 (business):
  Capital deployed: $15,000-30,000
  SKUs: 100-300
  Monthly profit: $4,000-10,000

Key lever: Faster capital recycling (higher BSR items) > more SKUs
```

---

## Cashback Stack — How to Max Every Dollar

### Credit Card Stack for Arb Buying

| Card | Best For | Cashback |
|---|---|---|
| Chase Freedom Flex | Rotating 5% (often Walmart, Amazon) | 5% when active |
| Amex Blue Cash Preferred | US supermarkets, gas | 6% supermarkets |
| Citi Double Cash | Everything else | 2% |
| Chase Ink Unlimited | Small business purchases | 1.5% |
| Target RedCard | Target specifically | 5% off all Target |
| Walmart Credit Card | Walmart online | 5% online |

**Stack example (Walmart Q4):**
- Chase Freedom during Walmart 5% quarter: 5%
- + Rakuten (TopCashback): 3%
- + BrickSeek found 50% clearance item
- **Effective buy price: 8% cheaper than sticker clearance price**

### Cashback Portals — Annual Comparison

Track rates at **cashbackholic.com** or **cashbackmonitor.com** (live comparison tools).

Best portals for arb:
- Rakuten: Best for Macy's, Kohl's, Nike
- TopCashback: Best for Walmart, Target
- BeFrugal: Best for Home Depot
- Swagbucks: Sometimes beats all for specific retailers

**Note:** Can't stack multiple cashback portals. Pick the highest one per retailer.
