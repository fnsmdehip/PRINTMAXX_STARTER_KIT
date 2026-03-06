# E03 Ecom Arbitrage Scanner — Scanning SOP

## What Is Ecom Arbitrage

Buy low on Platform A. Sell high on Platform B. Pocket the spread.

Four flavors:
1. **Retail Arb** — buy clearance/sale items in physical stores, sell on Amazon/eBay
2. **Online Arb** — buy discounted items online, sell on Amazon FBA or eBay
3. **Wholesale Arb** — buy from distributors at MAP, flip to consumers
4. **Reverse Arb** — buy from Amazon, sell on eBay/Walmart/Poshmark when price spread exists

This SOP covers primarily **Online Arb** (no car needed, scalable, automatable).

---

## Tool Stack

| Tool | Purpose | Cost |
|------|---------|------|
| **Tactical Arbitrage** | Bulk scans 1,000+ sources vs Amazon | $89/mo |
| **OAXray** | Chrome extension, scan one page at a time | $99/mo or $25 7-day trial |
| **SourceMogul** | UK-focused, Amazon-to-eBay flip finder | $67/mo |
| **RevSeller** | Amazon Chrome extension, FBA calc on listing page | $99.99/yr |
| **Keepa** | Price history, BSR history, stock alerts | $19/mo |
| **BrickSeek** | Retail clearance scanner (Walmart, Target, Home Depot) | Free/$9.99/mo |
| **OAXRAY** | Alternative to Tactical Arb, faster for single-source scans | $99/mo |
| **Sellerboard** | P&L tracking after you're selling | $15-23/mo |

**Minimum viable stack (getting started):** Keepa ($19) + OAXray trial ($25) + RevSeller ($8/mo) = $52/mo

**Power scanner stack:** Tactical Arbitrage ($89) + Keepa ($19) + RevSeller ($8) = $116/mo

---

## Platform Pairs — Where the Spreads Live

### Tier 1: Highest Spread Frequency

| Source (Buy) | Destination (Sell) | Avg Spread | Best Categories |
|---|---|---|---|
| Walmart Clearance | Amazon FBA | 40-80% | Toys, electronics, home goods |
| Target Clearance (Circle app) | Amazon FBA | 30-70% | Beauty, toys, seasonal |
| Home Depot Clearance | Amazon FBA | 50-150% | Tools, hardware, outdoor |
| Costco online | Amazon FBA | 20-50% | Supplements, food, household |
| eBay BIN listings | Amazon FBA | variable | Collectibles, specialty |

### Tier 2: Reliable but Slower

| Source | Destination | Notes |
|---|---|---|
| Amazon deals | eBay | Works when Amazon prices drop below eBay; higher friction |
| Macy's/Kohl's clearance | Amazon | Clothing is complex (variations), but jewelry/tools work |
| Wayfair clearance | Amazon | Furniture arb exists, but FBA logistics painful |
| Sam's Club | Amazon | Member pricing creates real spreads on pantry items |
| Woot.com | eBay | Refurb electronics, fast turnover |

### Tier 3: Niche But High Margin

| Source | Destination | Notes |
|---|---|---|
| TJ Maxx / Ross in-store | Amazon / eBay | Requires physical trips, but margins 100-300% |
| Dollar Tree | Amazon | $1.25 items selling for $6-15 on Amazon |
| Five Below | Amazon | Same play — clearance section |
| Facebook Marketplace | eBay / Amazon | Local pickup, zero shipping cost on source |
| ThredUp / Poshmark | eBay | Branded clothing arbitrage |

---

## Daily Scanning Workflow

### Morning Session (45-60 min)

**8:00 AM — Check price alerts (15 min)**
```
Keepa alert queue → review overnight price drops
RevSeller open → check Amazon Best Seller Rank changes
BrickSeek → scan Walmart/Target clearance updates
```

**8:15 AM — Run Tactical Arbitrage scan (20 min)**
```
Settings: Min ROI 30%, Min profit $3, Max buy price $50
Source rotation (daily):
  Mon/Thu: Walmart.com
  Tue/Fri: Target.com
  Wed/Sat: Home Depot, Costco
  Sun: eBay + Woot
Filter results: BSR < 100,000, 3+ FBA sellers, no Amazon sold
```

**8:35 AM — OAXray spot checks (10 min)**
```
Open 3-5 clearance/deals pages manually
Run OAXray scan on each page
Flag any item with ROI > 30% and BSR < 200K
```

**8:45 AM — Source new leads from Facebook groups (10 min)**
```
Groups to check daily:
- Online Arbitrage Source List (30K+ members)
- Amazon FBA Arbitrage (private, apply to join)
- Replens & Online Arbitrage
Copy interesting leads into scan queue
```

---

### Midday Check (15 min)

**12:00 PM — Process Keepa alerts**
```
Items on watchlist that hit price triggers
Quick RevSeller check on each
Buy or pass decision in < 2 min per item
```

---

### Evening Session (30 min)

**7:00 PM — Trend scanning**
```
Check Keepa trending BSR data (Products Trending tab)
Search Amazon "Movers & Shakers" by category
Cross-reference with current source prices
Look for items moving UP in rank = demand spike
```

**7:15 PM — Prep tomorrow's scans**
```
Queue up Tactical Arbitrage for overnight batch run
Set new Keepa price alerts on watchlist items
Update deal tracker spreadsheet
```

---

## How to Read a Keepa Chart

**Green line** = Amazon price
**Blue line** = New 3rd party (you)
**Orange line** = Sales rank (BSR)

**Green signals:**
- BSR trending DOWN over 90 days (selling faster)
- Price stable or trending UP (not a race to bottom)
- Amazon out of stock regularly (gap for 3P sellers)
- Sales spikes around holidays but consistent year-round baseline

**Red flags:**
- BSR 500K+ = slow mover, capital tied up too long
- Price crashing down = competition flooding in
- Amazon keeps going in/out of stock at MAP = they'll always undercut you
- No sales rank data = brand new listing, risky

---

## Lead Sourcing Beyond Scan Tools

### Deal Sites (Manual Review Daily)
- **Slickdeals.net** — community-voted deals, catch early before price normalizes
- **DealNews** — curated, usually reliable pricing
- **Brad's Deals** — good for retail clearance
- **Woot.com** — refurb electronics daily

### Cashback Stacking
Every arb purchase should run through cashback:
- **Rakuten** — 1-15% back at most major retailers
- **TopCashback** — often beats Rakuten on Walmart/Target
- **Stack with credit cards**: Chase Freedom (5% rotating) or Amex (6% grocery)
- **Stack with retailer apps**: Target Circle (1-5% off), Walmart Pay (2% back)

Cashback can add 5-15% to your effective margin. On a $100 buy = $5-15 back.

### Retail Clearance Apps
- **Flipp** — aggregates clearance flyers all retailers
- **Target Circle** — Target-specific clearance + coupon stacks
- **Walmart Savings Catcher** (now via Walmart app)
- **Store app barcode scanner** — scan in-store, compare to Amazon before buying

---

## Scanning Frequency by Strategy

| Strategy | Scan Frequency | Time Investment | ROI Range |
|---|---|---|---|
| Tactical Arbitrage bulk | Daily automated + 2x weekly manual review | 30 min/day | 25-60% |
| OAXray spot scans | 2-3x daily on target pages | 45 min/day | 30-80% |
| BrickSeek retail | 2-3x weekly | 20 min/session | 50-200% |
| Keepa alerts | Real-time alerts, review 2x daily | 15 min/day | varies |
| Facebook group leads | Daily | 10 min/day | varies |
| Deal site monitoring | 2x daily | 15 min/day | 30-100% |

**Full workflow daily time:** 2-3 hours to run it properly. Can compress to 1 hour with good Keepa alert setup doing most of the filtering.

---

## Scaling the Scan Operation

### Virtual Assistants for Scanning

Once process is documented (this SOP), offshore VAs can handle:
- Tactical Arbitrage daily scans and filtering
- BrickSeek checks
- Facebook group monitoring
- Deal site triage

Cost: $3-6/hr Philippines VA = $15-30/day for someone doing this full time
Their job: triage leads → pass only 30%+ ROI, BSR < 150K, no Amazon to you

### Automation Add-Ons

**Keepa API** ($20/mo developer access):
- Pull price history programmatically
- Build custom alerts beyond what the UI supports
- Cross-reference multiple ASINs at once

**Python + Keepa API workflow:**
```python
# Example: batch check ASINs against price thresholds
import keepa
api = keepa.Keepa('YOUR_API_KEY')
products = api.query(['ASIN1', 'ASIN2'], history=True)
for p in products:
    current_amazon = p['data']['AMAZON'][-1]
    my_buy_price = 14.99  # your source price
    if current_amazon > my_buy_price * 1.5:
        print(f"POTENTIAL FLIP: {p['asin']} | Buy: ${my_buy_price} | Amazon: ${current_amazon}")
```

**Sellerboard + Tactical Arb integration:**
- Export leads from TA → import into Sellerboard
- Auto-populate FBA fee estimates
- Track actual vs projected margins on every purchase

---

## Common Scan Failures and Fixes

| Problem | Cause | Fix |
|---|---|---|
| 0 results from TA scan | Filters too tight | Loosen ROI to 20%, raise max buy to $100 |
| Too many results, hard to review | Filters too loose | Add: min 5 reviews on Amazon, BSR < 100K |
| Items OOS when you try to buy | Scanning too slow | Set up price/stock alerts, buy same day |
| Amazon keeps undercutting | Amazon as competitor | Filter out ASINs where Amazon is selling |
| Item arrives, price crashed | Oversaturated, fast flood | Check seller count trend in Keepa before buying |
| Keepa shows good metrics but item won't sell | Seasonality | Check 365-day BSR chart, not just 90-day |
