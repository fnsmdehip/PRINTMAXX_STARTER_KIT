# E08 Trending Products Scanner — Setup + SOPs

## WHAT THIS IS
A systematic process for identifying trending ecom products 3-6 weeks before they saturate.
Target: find products hitting momentum on TikTok/Amazon/AliExpress before the big dropshippers do.
Window: 3-6 weeks to list and start content before saturation.

---

## TOOL STACK

| Tool | Cost | What It Does | Signal Type |
|------|------|-------------|-------------|
| TikTok Kalodata | $35/mo | TikTok Shop GMV data, trending products | TikTok sales velocity |
| FastMoss | $29/mo | TikTok creator + product analytics | Creator-product match |
| Amazon Movers & Shakers | Free | Amazon hourly rank gainers | Amazon momentum |
| AliExpress Dropship Center | Free | AliExpress trending items | Supply-side demand |
| Google Trends | Free | Search volume trends | Intent-based signals |
| Exploding Topics | Free tier / $39/mo | Early-stage topic detection | Macro trends |
| Pinterest Trends | Free | Pinterest trending searches | Visual/lifestyle trends |
| Wish Trends (defunct — use Shein instead) | Free | Shein Rising section | Fast fashion signals |

**Minimum setup: $0 (all free tools)**
**Optimal setup: $64/mo (Kalodata + FastMoss)**

---

## DAILY SCANNING SOP (30 min/day)

### Step 1: Amazon Movers & Shakers (5 min)
1. Go to amazon.com/gp/movers-and-shakers
2. Check top 5 categories: Home & Kitchen, Health, Beauty, Toys, Electronics
3. Filter: look for products ranked 100-500 overall BSR climbing fast
4. Red flags for our purposes: existing heavy competition (100+ reviews), branded products
5. Green lights: <50 reviews, generic product, easy to source on CJ/Zendrop
6. Log in `trending_products_log.csv`: Date | Product | BSR | Category | Source | Action

### Step 2: TikTok Trending (10 min)
1. Open TikTok: search by category (beauty, home, gadgets)
2. Filter by "This week" and sort by views
3. Look for videos 500K-2M views (not yet at 10M — still entering phase)
4. Check comments for: "where to buy?" "link?" "what is this?" = buying intent
5. Cross-reference product on AliExpress: is it available? What's the supplier price?
6. With Kalodata (if active): check GMV velocity — is it doubling week over week?

### Step 3: AliExpress Dropship Center (5 min)
1. dropshippingcenter.aliexpress.com
2. Find Products → set category → sort by "Orders" and filter "Last 7 days"
3. Look for items with 500-5,000 orders in last week (scaling zone)
4. Check: shipping time to US (goal: <14 days via AliExpress Standard Shipping)
5. Profit check: AliExpress price × 3.5 = target sell price (must clear $15 margin min)

### Step 4: Google Trends Validation (5 min)
1. Check product name on trends.google.com
2. Look for: upward curve in last 30 days, NOT plateau
3. Set: United States, 90 days
4. Related queries: often reveal adjacent products to add to scan list

### Step 5: Log + Decide (5 min)
For each candidate product:
```
Product: [name]
Source: [where found]
AliExpress price: $X.XX
Target sell price: $X.XX (3.5x margin formula)
Competition scan: [# sellers on TikTok Shop / Amazon]
TikTok views (last week): [number]
BSR (if Amazon): [rank]
Decision: TEST / MONITOR / SKIP
Reason: [one line]
```

---

## PRODUCT VALIDATION CRITERIA

Pass all 5 gates before listing:

**Gate 1: Margin Gate**
- Cost (AliExpress/CJ): ≤$15
- Shipping to US: ≤$5
- Target sell price: ≥$35
- Net margin after fees: ≥40%
- Example: $8 product + $4 shipping = $12 COGS → sell at $39.99 → $19.99 net → 50% margin ✓

**Gate 2: Trend Gate**
- Minimum: 3 TikTok videos with 500K+ views in last 14 days
- OR: Amazon BSR rank improvement >5,000 positions in 7 days
- NOT: already on Trending Products pages of major dropship tools (too late)

**Gate 3: Differentiation Gate**
- Can we offer: better photos, better price, faster shipping, or bundle upgrade?
- If 10+ TikTok Shop sellers already selling identical product: SKIP
- If 3-5 sellers but you can undercut by 10% or bundle: TEST

**Gate 4: Supplier Gate**
- CJ Dropshipping: check stock >500 units
- Shipping time via CJ Direct: ≤12 days to US
- Product reviews on supplier: ≥4.5 stars
- Video sample available for content creation

**Gate 5: Content Potential Gate**
- Can you create a compelling 30-second demo video with this product?
- Does it have a clear "wow moment" visible on camera?
- Would you buy this after seeing a 30-second demo?
- Boring products don't go viral — skip them regardless of margins

---

## PRODUCT CATEGORIES TO TARGET (2026 Signals)

### Tier 1: Highest Opportunity (scan daily)
| Category | Why Now | Example Products |
|----------|---------|-----------------|
| AI-adjacent gadgets | ChatGPT/AI hype cycle carries adjacent products | AI pin recorders, voice memo devices |
| Sleep tech | Mental health macro trend + PEMF adjacency | sleep masks, red light therapy, grounding mats |
| Mini appliances | Kitchen content trending on TikTok | mini waffle makers, egg cookers, ice makers |
| Portable wellness | Work from anywhere + wellness = massive overlap | massage guns, fascia tools, acupressure mats |
| Lighting products | Content creator boom + aesthetic TikTok | LED neon signs, ring lights, ambient LED strips |

### Tier 2: Monitor Weekly
| Category | Signal | Caution |
|----------|--------|---------|
| Fashion accessories | Pinterest trends up | Fast trend = fast death |
| Pet products | Evergreen but competitive | Margin compression |
| Car accessories | Steady demand | Shipping weight issues |
| Home organization | Spring cleaning annual cycle | Very competitive |

### Tier 3: Avoid
- Supplements (regulatory risk, high return rate)
- Electronics over $50 (return rate kills margins)
- Clothing with sizing (return nightmare)
- Seasonal only (too short window)
- Branded/patented products (takedown risk)

---

## TRACKING SHEET STRUCTURE

`LEDGER/TRENDING_PRODUCTS_TRACKER.csv` columns:
```
Date_Found, Product_Name, Source, AliExpress_URL, Supplier_Price, Ship_Cost, Sell_Price, Est_Margin_Pct, TikTok_Views_7d, Amazon_BSR, Trend_Status [RISING/PLATEAU/DECLINING], Decision [TEST/MONITOR/SKIP/ACTIVE/DEAD], Revenue_30d, Notes
```

**Weekly review:** Every Sunday, move ACTIVE products to full P&L tracking.
**Monthly purge:** Kill any product that hasn't sold 5+ units in 30 days.
