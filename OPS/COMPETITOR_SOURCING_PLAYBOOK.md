# Competitor Sourcing Playbook - Factory-Direct via US Customs Data

US customs data is public. every single shipment entering the country is logged. company names, factory names, volumes, dates. ImportYeti makes it searchable.

find a competitor doing $500k/mo. search their company name. see exactly which factory in china they source from. contact that factory directly. your own branding, their proven supply chain. margin goes from 25% to 60%+.

---

## Step 1: Find the Competitor (5 min)

pick a product from `LEDGER/ECOM_ARB_OPPORTUNITIES.csv` with >25% margin. then:

1. search Amazon for the product. sort by "Best Sellers"
2. pick the top 3 sellers. note their brand name.
3. check their estimated revenue on Jungle Scout, Helium 10, or just look at review count (1000+ reviews = $100K+/mo likely)

or use the pre-built competitor list: `python3 AUTOMATIONS/competitor_sourcing_pipeline.py --status`

---

## Step 2: Search ImportYeti (5 min)

go to `https://www.importyeti.com/search?q=COMPETITOR_NAME`

you'll see:
- every shipment they received
- which factory sent it
- factory name and location
- shipment volumes and dates
- reorder frequency

or run the automated scanner:
```bash
python3 AUTOMATIONS/import_sourcing_scanner.py --search "BlendJet"
```

**what to look for:**
- factory in Shenzhen, Guangzhou, Dongguan, Yiwu = manufacturing hub (good)
- 10+ shipments = established relationship (proven factory)
- recent shipments (last 6 months) = still active
- multiple US importers using same factory = factory is reliable

---

## Step 3: Contact the Factory (1 day)

### Find Contact Info

search Alibaba for the exact factory name from ImportYeti:
```
https://www.alibaba.com/trade/search?SearchText=FACTORY_NAME&tab=supplier
```

also try:
- Made-in-China.com
- GlobalSources.com
- Google: "FACTORY_NAME contact email"

### First Contact Email Template

subject: Product inquiry - [PRODUCT] - new US brand

```
Hi,

I found your company through trade records showing you supply [PRODUCT] to US importers.

We are a new US brand looking for a reliable manufacturer for [PRODUCT]. We plan to start with a sample order and scale to [100-500] units/month within 3 months.

Could you please share:
1. Your product catalog for [PRODUCT CATEGORY]
2. Price list (FOB pricing for 100, 500, 1000 units)
3. MOQ for custom branding/packaging
4. Sample pricing and lead time
5. Payment terms for new customers

Our timeline:
- Week 1: Review catalog and pricing
- Week 2-3: Order samples
- Week 4-6: Place first production order

Thank you,
[YOUR NAME]
[YOUR COMPANY]
```

### Follow-up Template (if no response after 3 days)

```
Hi,

Following up on my inquiry about [PRODUCT]. We're comparing 3 factories and making a decision this week.

If you're able to provide pricing and a sample within 2 weeks, we'd like to include your factory in our evaluation.

Best,
[NAME]
```

---

## Step 4: Negotiate MOQ (3-5 days)

**standard MOQ negotiation tactics:**
- start by asking for their standard MOQ. typically 500-2000 units.
- counter with: "we'd like to start with 100 units as a trial order, then scale to 500+ monthly"
- most factories will accept a smaller first order at slightly higher unit price
- offer to pay by T/T (wire transfer) for better pricing vs Trade Assurance
- mention you plan to be a recurring customer (factories love this)

**pricing benchmarks (factory-direct vs AliExpress):**
- typical factory price = 35-60% of AliExpress retail price
- led face mask: AliExpress $15-24 → factory $5-10
- yoga mat: AliExpress $5-10 → factory $2-5
- wireless earbuds: AliExpress $5-7 → factory $2-3
- portable blender: AliExpress $7-11 → factory $3-5

---

## Step 5: Private Label (2-4 weeks)

**what you need from the factory:**
1. logo placement options (printed, embossed, engraved)
2. custom packaging design (provide your AI-generated design)
3. product insert card (use Canva, include QR code to your site)
4. custom color options if available
5. compliance certificates (FCC, CE, FDA if applicable)

**cost for private labeling:**
- logo/branding: usually free above MOQ threshold
- custom packaging: $0.30-$1.00/unit additional
- product inserts: $0.05-$0.15/unit
- custom mold (if needed): $500-$3000 one-time

---

## Timeline Summary

| Phase | Time | Action |
|-------|------|--------|
| Research | 15 min | Find competitor on ImportYeti, identify factory |
| Outreach | 1 day | Email factory via Alibaba/direct, request catalog |
| Evaluation | 3-5 days | Compare 3 factory quotes, negotiate MOQ |
| Samples | 2-3 weeks | Order samples, test quality |
| First Order | 4-6 weeks | Production + shipping (sea freight) |
| Live | Week 8-10 | Products in hand, list on marketplace |

---

## Real Numbers from Our Scan Data

from `LEDGER/CONTACT_READY_FACTORIES.csv` (8 factories identified):

| Factory | Location | Shipments | Products | Confidence |
|---------|----------|-----------|----------|------------|
| Mester Led | Shenzhen | 1,487 | LED face mask | HIGH |
| Wuxi Pro Face | Wuxi | 802 | LED face mask | MEDIUM |
| Face Time International | Hong Kong | 556 | LED face mask | MEDIUM |
| Face Impex | India | 409 | LED face mask | MEDIUM |
| Disposable Mask | Shenzhen, Guangdong | 131 | LED face mask | HIGH |
| Mask Impex | India | 135 | LED face mask | MEDIUM |

**Mester Led** has 1,487 shipments and supplies Spring Lighting Group, Zls International. this is a proven, high-volume manufacturer. contacting them for LED face masks is the highest-priority action.

---

## Margin Improvement Calculator

```
Current flow:  Factory → AliExpress → You → Customer
Your margin:   sell_price - (AliExpress_price + fees + shipping)

Factory-direct: Factory → You → Customer
Your margin:    sell_price - (factory_price + fees + shipping + import_duty)

Example (LED face mask):
  AliExpress price:     $15.00
  Factory-direct price: $5.50 (estimated 37% of AliExpress)
  Sell price:           $45.99

  Current margin:       ~$20 (44%)
  Factory-direct margin: ~$30 (65%)
  Improvement:          +$10/unit (+21% margin)

  At 100 units/mo:      +$1,000/mo additional profit
  At 500 units/mo:      +$5,000/mo additional profit
```

---

## Commands

```bash
# Full pipeline (maps competitors to factories)
python3 AUTOMATIONS/competitor_sourcing_pipeline.py --scan

# Single product deep dive
python3 AUTOMATIONS/competitor_sourcing_pipeline.py --product "led face mask"

# Status dashboard
python3 AUTOMATIONS/competitor_sourcing_pipeline.py --status

# Top opportunities
python3 AUTOMATIONS/competitor_sourcing_pipeline.py --top 10

# Run the underlying import scanner for a specific company
python3 AUTOMATIONS/import_sourcing_scanner.py --search "CurrentBody"

# Export contact-ready factory list
python3 AUTOMATIONS/import_sourcing_scanner.py --export
```

---

## Risk Mitigation

1. **always order samples before bulk**. $20-50 for a sample saves you from a $2000 bad batch.
2. **use Alibaba Trade Assurance** for first orders. protects payment if factory doesn't deliver.
3. **get compliance certs upfront**. FCC for electronics, FDA for beauty/health, CPSC for kids.
4. **start with 100-200 units**. don't order 2000 before you've validated demand.
5. **inspect before shipping**. use a QC service like QIMA ($300/inspection) or DIY via video call.
6. **sea freight for bulk, air for samples**. sea = $3-5/kg, air = $8-15/kg. plan 3-4 weeks for sea.

---

*generated by PRINTMAXX competitor sourcing pipeline. data from ImportYeti US customs records.*
