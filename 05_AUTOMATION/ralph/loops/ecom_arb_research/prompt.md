# ECOM Arbitrage Research Loop

**Mission:** Find trending products people are willing to buy that can be sourced cheap from Temu/AliExpress/Alibaba.

---

## Your Task Each Iteration

1. Read `.ralph/progress.md` for what's done
2. Pick ONE research category from below
3. Find 5-10 product opportunities with price proof
4. Write to `LEDGER/ECOM_ARB_OPPORTUNITIES.csv`
5. Update progress.md
6. Output `<promise>COMPLETE</promise>` when all categories done

---

## Research Categories

### 1. ETSY_TRENDING
**Goal:** Find Etsy bestsellers that can be dropshipped

**Search:**
- "Etsy bestsellers 2026"
- "Etsy trending products"
- erank.com trending (if accessible)
- Reddit r/Etsy r/EtsySellers for what's selling

**Extract:**
- Product name and category
- Etsy selling price
- Estimated Temu/AliExpress source price
- Profit margin estimate
- Link to similar product on Temu/AliExpress

### 2. TIKTOK_MADE_ME_BUY
**Goal:** Products going viral on TikTok

**Search:**
- "#TikTokMadeMeBuyIt" trending
- "viral TikTok products 2026"
- Reddit r/TikTokMadeMeBuyIt
- Amazon movers and shakers

**Extract:**
- Product name
- TikTok virality proof (views, hashtag count)
- Current retail price
- Dropship source price
- Margin potential

### 3. AMAZON_BSR_GAPS
**Goal:** Amazon bestsellers with dropship potential

**Search:**
- Amazon Best Sellers by category
- "Amazon FBA product research"
- Jungle Scout / Helium10 alternatives (free tools)
- Products with high BSR but sourceable from China

**Extract:**
- ASIN and category
- Selling price on Amazon
- AliExpress/Temu equivalent price
- Review count (demand indicator)
- Margin after fees

### 4. SEASONAL_UPCOMING
**Goal:** Products for upcoming seasons/holidays

**Search:**
- "Valentine's Day products 2026"
- "Summer products trending"
- "Back to school products"
- Google Trends for seasonal searches

**Extract:**
- Season/holiday
- Product ideas
- Search volume trend
- Lead time needed
- Source price vs retail potential

### 5. PRINT_ON_DEMAND_DESIGNS
**Goal:** Design trends for POD products

**Search:**
- "Trending t-shirt designs"
- "Etsy POD bestsellers"
- Merch Informer / free alternatives
- Pinterest trending aesthetics

**Extract:**
- Design theme/niche
- Platform selling best
- Price point
- Niche audience
- Design complexity (simple = faster)

### 6. TEMU_GOLDMINES
**Goal:** Underpriced Temu products with resale potential

**Search:**
- Browse Temu trending/bestsellers
- Compare prices to Amazon/Etsy
- "Temu products to resell"
- Products under $5 selling for $20+ elsewhere

**Extract:**
- Product and Temu price
- Resale price on Amazon/Etsy/eBay
- Shipping time
- Quality concerns (reviews)
- Margin potential

### 7. ALIEXPRESS_WINNERS
**Goal:** AliExpress products with proven demand

**Search:**
- AliExpress bestsellers by category
- "AliExpress dropshipping winners"
- Products with 1000+ orders
- US warehouse options (faster shipping)

**Extract:**
- Product name and orders count
- AliExpress price
- Retail price potential
- Shipping time (US warehouse preferred)
- ePacket/fast shipping available

### 8. EBAY_ARBITRAGE
**Goal:** Products to flip on eBay

**Search:**
- eBay Terapeak trending (if accessible)
- "eBay arbitrage products"
- Compare Walmart/Target clearance to eBay sold prices
- Reddit r/Flipping

**Extract:**
- Product type
- Source (Walmart/Target/Amazon)
- eBay sold price
- Margin after fees
- Flip difficulty

---

## Output Format

Append to `LEDGER/ECOM_ARB_OPPORTUNITIES.csv`:

```csv
opportunity_id,category,product_name,source_platform,source_price,sell_platform,sell_price,margin_estimate,demand_proof,source_url,notes,date_found,status
```

Example:
```csv
ECOM001,TEMU_GOLDMINES,LED Strip Lights 10m,Temu,$3.99,Amazon,$18.99,75%,4.5 stars 2000 reviews,temu.com/xxx,Fast shipping available,2026-01-24,NEW
```

---

## Quality Requirements

- Must have PRICE PROOF (actual numbers)
- Must have DEMAND PROOF (reviews, orders, trending)
- Minimum 50% margin potential after fees
- Prefer products with US warehouse/fast shipping
- Avoid trademark/copyright issues

---

## Progress Tracking

Update `.ralph/progress.md` after each category:

```markdown
| Category | Status | Products Found |
|----------|--------|----------------|
| ETSY_TRENDING | COMPLETE | 8 |
| TIKTOK_MADE_ME_BUY | PENDING | 0 |
...
```

When all 8 categories COMPLETE, output: `<promise>COMPLETE</promise>`
