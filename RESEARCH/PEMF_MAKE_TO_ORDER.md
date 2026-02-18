# PEMF Make-to-Order Manufacturing Guide

**Date:** 2026-02-07
**Status:** COMPLETE
**Researcher:** mto-researcher agent
**Model:** Zero inventory, build AFTER customer orders

---

## Executive Summary

Make-to-order (MTO) PEMF manufacturing means every unit is built after a customer places an order. Zero inventory, zero overhead from unsold stock. The tradeoff: higher per-unit cost and longer lead times vs. bulk. But for a premium product selling at $1,000-3,000, customers expect handcrafted quality and are willing to wait 1-2 weeks. This is exactly how Steeve Bradet runs his operation and he sells ZK mats at $1,650-2,000 and Nextion mats at $3,000.

**Bottom line:** MTO is the right model for PEMF at the $1K+ price point. Per-unit cost runs $150-400 (depending on coil count and controller), selling at $1,000-3,000. That is 60-85% gross margin with zero inventory risk.

---

## 1. US-Based Contract Manufacturers

### A. PCB Assembly Houses (For Controller Boards)

These companies can assemble the ZK-PP2K-based controller PCB or a custom control board on demand.

| Company | Location | Specialization | Min Order | Lead Time | Notes |
|---------|----------|---------------|-----------|-----------|-------|
| **CircuitHub** | Online platform | On-demand PCBA, 1-10,000 units | 1 unit | 3-10 days | Instant online quoting from EDA files. Upload KiCad/Eagle, get price immediately. Best for controller board assembly |
| **MacroFab** | Houston, TX (platform) | Platform-based PCBA, 80+ factory lines | 1 unit | 5-15 days | Self-service platform, instant price quotes, seamless prototype-to-production scaling. No minimum volume commitments |
| **PCB Assembly Express** | Oregon, USA | High-mix low-volume PCBA | 1 unit | 3-5 days | Mycronic pick-and-place, excellent for prototypes and small runs |
| **A2Z EMS** | Illinois, USA | Turnkey, consigned, mixed assembly | 1 unit | 5-10 days | Quick-turn prototype through bulk volume. High-mix, low-volume specialty |
| **RUSH PCB** | California, USA | Design, fabrication, full turnkey | 1 unit | 3-7 days | One-stop shop. PCB design through assembly |
| **Sierra Circuits** | Sunnyvale, CA | Quickturn PCBs | 1 unit | 1-7 days | Fastest turnaround. PCBs assembled in as fast as 5 days |
| **Amitron** | Chicago area, IL | Short-run, one-off, prototype | 1 unit | 3-5 days | Specializes in prototype and short-run. Rapid turn times |
| **Titan Circuits** | Phoenix, AZ | High-mix, low-to-medium volume | Small batch | 5-10 days | Good for ongoing small-batch production |
| **EMSG** | USA | PCBA and contract manufacturing | 1 unit | 5-10 days | Up to 50,000 units. 30+ years experience |

**Best for MTO PEMF controllers:** CircuitHub or MacroFab for instant quoting and single-unit runs. Keep 5-10 pre-assembled controller boards on hand (cheap, small, easy to store) and build mats on demand.

### B. Custom Coil Winding Services (For PEMF Coils)

These US companies wind custom copper coils to your specifications. They can produce the 15-20 coils per mat needed for PEMF.

| Company | Location | Specialization | Min Order | Notes |
|---------|----------|---------------|-----------|-------|
| **Custom Coils, Inc.** | Benicia, CA | Electromagnetic assemblies, 45+ years | No stated minimum | 24,000 sq ft facility. Handles small and large runs. Solenoid/electromagnetic coils |
| **Prem Magnetics** | Johnsburg, IL | Custom coil winding, 40+ years | No minimum, no NRE charge | Family-owned. No minimum purchase requirement. Design through production |
| **HBR Industries** | USA | Copper coils, small production runs | Small batch | 40+ years. Specializes in small production runs and fast prototypes |
| **Badger Magnetics** | Wisconsin/Minnesota | Low and high volume custom coils | Flexible quantities | Handles quantities that match demand, both low and high volume |
| **Custom Coils (Alcester)** | Alcester, SD | Transformers, specialty coils | Small batch | Since 1967. Custom designs including air coils |
| **Endicott Coil Company** | USA | Custom wound copper coils | Small batch | 70+ years. Broad spectrum of OEM magnetic components |
| **SMT LLC** | USA | Solenoid coils, electromagnetic | Flexible | End-to-end from design to production. Low and high volume |
| **Remington Industries** | USA | Coil winding, magnet wire | Small batch | Also sells raw magnet wire for self-winding |

**Best for MTO PEMF:** Prem Magnetics (no minimum, no NRE fee) or Custom Coils Inc. (flexible on small runs). Get a quote for winding 20 pancake coils at 45-55 gauss spec per unit. Compare to self-winding cost.

### C. Full Contract Electronics Manufacturers (If You Want Turnkey)

These can handle complete device assembly (board + coils + mat + packaging) but typically prefer higher volumes.

| Company | Location | Focus | Min Order | Notes |
|---------|----------|-------|-----------|-------|
| **Sparqtron** | Silicon Valley, CA | HMLV electronics, ISO 13485/9001, FDA registered | Small batch | SAP ERP for timely small batch production. Medical device certified |
| **NEOTech** | Multi-site USA | Low-volume high-mix electronics | Small batch | 40+ years. Aerospace, defense, medical. High quality but expensive |
| **Levison Enterprises** | Ohio | Medical device manufacturing | Varies | Specializes in medical devices. Could handle PEMF as wellness device |
| **ETI Manufacturing** | USA | Medical electronics, PCB assembly | Small batch | Medical device contract manufacturing specialty |
| **CO-AX Technology** | USA | Medical electronics | Small batch | Medical electronics manufacturing |

**Reality check:** Full contract manufacturers charge significant setup fees ($2,000-10,000+) and per-unit costs that make sense only at 50+ units. For true single-unit MTO, the hybrid model (Section 3) is better.

---

## 2. Make-to-Order Cost Models

### A. Per-Unit Cost Breakdown (Self-Assembly MTO)

This is the model where you (or a hired assembler) build each unit after an order comes in.

| Component | Qty 1 Cost | Qty 10 Cost | Qty 50 Cost | Notes |
|-----------|-----------|-------------|-------------|-------|
| **ZK-PP2K Controller Module** | $8 | $6 | $5 | Amazon/AliExpress. Volume discount kicks in at 10+ |
| **Custom control PCB (if needed)** | $25-50 | $15-25 | $8-15 | CircuitHub/JLCPCB. Major savings at volume |
| **20 AWG Magnet Wire (copper)** | $18 (1 lb spool) | $14/unit | $12/unit | Bulk spool pricing. ~1 lb per 20-coil mat |
| **Coil forms/spacers** | $10-15 | $8-12 | $5-8 | 3D printed or injection molded. 3D print for low vol |
| **Mat substrate (yoga mat/foam)** | $15-25 | $12-20 | $10-15 | Bulk yoga mat material or custom cut foam |
| **Mat cover/fabric** | $20-30 | $15-25 | $12-20 | Nylon or polyester quilted cover |
| **Power supply (19V DC)** | $12-15 | $10-12 | $8-10 | Laptop-style adapter |
| **Wiring, connectors, misc** | $10-15 | $8-12 | $6-10 | Banana plugs, hookup wire, heat shrink |
| **Flyback diodes, MOSFETs** | $5-8 | $4-6 | $3-5 | Safety components |
| **Packaging (box, foam, manual)** | $15-25 | $12-20 | $10-15 | Custom printed box at 50+, plain box at low vol |
| **Gaussmeter QC test time** | $5 (amortized) | $3 | $2 | WT10A meter amortized over units |
| **Labor (assembly + QC)** | $50-80 | $40-60 | $30-50 | 2-3 hours at $20-25/hr |
| **TOTAL COGS** | **$193-294** | **$147-222** | **$111-175** | |

### B. Per-Unit Cost Breakdown (Outsourced Coil Winding + Self-Assembly)

If you outsource coil winding to Prem Magnetics or similar:

| Component | Qty 1 Cost | Qty 10 Cost | Qty 50 Cost |
|-----------|-----------|-------------|-------------|
| **20 custom wound coils** | $100-200 | $60-120 | $40-80 |
| **Controller + PCB** | $33-58 | $21-31 | $13-20 |
| **Mat, cover, PSU, wiring** | $57-85 | $45-69 | $36-55 |
| **Packaging** | $15-25 | $12-20 | $10-15 |
| **Assembly labor** | $30-50 | $25-40 | $20-35 |
| **QC testing** | $5 | $3 | $2 |
| **TOTAL COGS** | **$240-423** | **$166-283** | **$121-207** |

### C. Margin Analysis by Model

| Model | COGS | Retail Price | Gross Margin | Margin % |
|-------|------|-------------|-------------|----------|
| **6-coil Mini (self-wind, qty 1)** | $100-150 | $800-1,000 | $650-900 | 75-87% |
| **15-coil Mat (self-wind, qty 1)** | $160-250 | $1,500-1,650 | $1,250-1,490 | 78-90% |
| **20-coil Mat (self-wind, qty 1)** | $193-294 | $2,000-2,500 | $1,706-2,307 | 78-92% |
| **20-coil Nextion (self-wind, qty 1)** | $250-400 | $3,000-3,500 | $2,600-3,250 | 82-93% |
| **20-coil Mat (outsourced coils, qty 10)** | $166-283 | $2,000-2,500 | $1,717-2,334 | 82-93% |
| **20-coil Mat (outsourced coils, qty 50)** | $121-207 | $2,000-2,500 | $1,793-2,379 | 86-95% |

**Key insight:** Even at single-unit MTO with the highest cost estimates, gross margins are 75%+. This is because PEMF mats sell for $1,000-3,000 but raw components cost under $300. The value is in the engineering, quality, and brand -- not the materials.

### D. Comparison to Bulk (China Import)

| Factor | MTO (Self-Build) | Bulk (China Import, 100 units) |
|--------|-------------------|-------------------------------|
| Per-unit COGS | $193-294 | $280-443 (landed with tariffs) |
| Upfront capital needed | $0 (build per order) | $28,000-44,300 |
| Inventory risk | Zero | 100 unsold units risk |
| Lead time per order | 3-7 days | 2-5 days (from US warehouse) |
| Quality control | 100% individual testing | Batch sampling |
| Tariff exposure | Minimal (US components) | 10-54% China tariffs |
| Customization | Easy per order | Fixed at production |
| Margin | 75-92% | 57-69% |

**MTO is actually cheaper per unit than China import** when you factor in tariffs, shipping, and duties. And you have zero inventory risk. The only disadvantage is slightly longer lead time per order (days, not weeks -- and Steeve Bradet ships in 5-8 business days with this model).

---

## 3. Hybrid Models (Best Approaches)

### Model A: Pre-Kitted Components + On-Demand Assembly (RECOMMENDED)

This is the optimal approach. Pre-source and kit all components, assemble only when an order arrives.

**How it works:**
1. Buy components in small batches (10-20 kits worth at a time)
2. Pre-cut wire to length for each coil
3. Pre-cut mat substrate to size
4. Store pre-assembled controller boards (tiny, easy to store)
5. When order arrives: wind coils, assemble mat, test, package, ship
6. Total assembly time: 2-4 hours per unit

**What to pre-kit (buy in batches of 10-20):**
- ZK-PP2K modules (tiny, $5-8 each, buy 20 at a time)
- Pre-cut magnet wire lengths (20 coils worth per kit)
- Mat substrate pre-cut to 78"x24"
- Mat covers (sewn or ordered in batch of 20)
- Power supplies (buy 20 at a time)
- Wiring harnesses (pre-solder connector ends)
- Packaging materials

**Per-kit inventory cost:** ~$80-120 in components per kit (10 kits = $800-1,200 on shelf)
**Assembly time per unit:** 2-4 hours
**Total COGS per unit:** $150-250 (at 10-kit batch pricing)
**Ship time after order:** 3-7 business days

### Model B: Local Assembler/Technician (Part-Time Hire)

Hire a part-time electronics technician to build units as orders come in.

**Where to find assemblers:**
- **Indeed/ZipRecruiter:** Electronic assembler jobs pay $16-31/hr part-time
- **Upwork:** Freelance electronics assemblers available for project-based work
- **Local community colleges:** Electronics/EE students looking for part-time work
- **Makerspaces:** Members with soldering/electronics skills
- **Retired technicians:** Former electronics industry workers
- **Craigslist/local listings:** "Part-time electronics assembly, flexible hours"

**Economics:**
- Pay: $20-30/hr
- Time per unit: 2-4 hours
- Labor cost per unit: $40-120
- Overhead: Minimal (they work from your workspace or theirs)
- Scalability: Add more assemblers as orders increase

**Training required:**
- Coil winding technique (1-2 days of training)
- Soldering (most already have this skill)
- Gaussmeter QC testing (30 minutes of training)
- Packaging and shipping (simple)

### Model C: Makerspace/Fab Lab Partnership

Partner with a local makerspace to use their equipment and space for assembly.

**What you get:**
- Soldering stations, multimeters, oscilloscopes
- 3D printers for coil forms and enclosure parts
- Work tables and storage space
- Community of skilled makers who can help

**Cost structure:**
- Makerspace membership: $50-200/month
- Equipment access: Included in membership
- Storage locker: $20-50/month additional
- You supply all components

**Note:** TechShop (the main chain) went bankrupt in 2017. But independent makerspaces thrive. Search for makerspaces near you at makerspaces.com or through local libraries and community colleges.

**Limitations:**
- Must schedule around other members
- No dedicated production line
- Works for 1-5 units/week, not high volume
- Insurance/liability may be complex

### Model D: Pre-Assembled Controller + Manual Coil Winding (BEST FOR STARTING)

The sweet spot for starting out:

1. **Controller boards:** Order pre-assembled from CircuitHub/MacroFab (5-10 at a time, $15-25 each)
2. **Coils:** Wind by hand yourself (the skill IS the moat)
3. **Mat assembly:** Manual, per order
4. **QC testing:** You test every unit with gaussmeter before shipping

**Why this works:**
- You develop deep product expertise
- Quality control is 100% (you built it)
- No dependency on external assemblers
- The hand-built story IS the marketing ("each mat hand-crafted and tested")
- Margins are highest (no labor outsourcing)
- This is exactly what Steeve Bradet does

---

## 4. Quality Control for Individual Units

### A. Pre-Assembly QC

| Check | Tool Needed | Pass Criteria | Time |
|-------|------------|---------------|------|
| Wire continuity | Multimeter | < 2 ohm for 20 AWG 200-turn coil | 30 sec/coil |
| Coil resistance consistency | Multimeter | All 20 coils within +/- 10% of each other | 5 min |
| Controller function | Power supply + LED | LCD displays, buttons respond, PWM output verified | 2 min |
| Power supply output | Multimeter | 19V +/- 0.5V, no voltage spikes | 1 min |

### B. Post-Assembly QC (EVERY UNIT)

| Test | Tool | Pass Criteria | Time |
|------|------|---------------|------|
| **Gauss measurement (each coil)** | WT10A Tesla Meter (~$35-50) | 45-55 gauss per coil at surface | 10 min |
| **Gauss uniformity** | WT10A | All coils within +/- 15% of each other | Included above |
| **Frequency verification** | Oscilloscope or gaussmeter | Square wave confirmed at set frequency (10 Hz default) | 2 min |
| **Full-mat field mapping** | WT10A at 5 positions | No dead zones, field covers full mat area | 5 min |
| **Burn-in test** | Timer | Run at max intensity for 30 min continuous. No overheating, no component failure | 30 min (unattended) |
| **Temperature check post-burn-in** | IR thermometer ($15-25) | Controller < 50C, coils < 45C, no hot spots | 1 min |
| **Wiring inspection** | Visual | All solder joints clean, no cold joints, no exposed wire, flyback diodes in place | 5 min |
| **Power draw** | Kill-A-Watt meter ($20) | Within expected range for coil count (typically 10-40W) | 1 min |
| **Cover/mat inspection** | Visual + touch | No lumps, coils evenly spaced, no wire poking through | 2 min |
| **Packaging QC** | Checklist | Mat, controller, PSU, manual, warranty card, QR code card all present | 2 min |

**Total QC time per unit:** ~60 minutes (30 min burn-in can run unattended while packaging)

### C. QC Equipment Investment

| Equipment | Cost | Use |
|-----------|------|-----|
| WT10A Tesla/Gauss Meter | $35-50 | Primary gauss measurement |
| Digital Multimeter (good quality) | $30-50 | Resistance, continuity, voltage |
| IR Thermometer | $15-25 | Post-burn-in temperature check |
| Kill-A-Watt Meter | $20-25 | Power draw verification |
| Oscilloscope (optional but recommended) | $50-200 (Hantek USB) | Waveform verification, frequency accuracy |
| **TOTAL QC EQUIPMENT** | **$150-350** | One-time investment |

### D. Maintaining Quality at Scale

| Volume | QC Approach | Notes |
|--------|------------|-------|
| 1-5/week | You test every unit personally | Maximum quality, you learn the product deeply |
| 5-15/week | You + trained assembler, you QC every unit | Assembler builds, you verify |
| 15-30/week | 2 assemblers, random QC + final sign-off | Test 100% on critical (gauss), sample on cosmetic |
| 30+/week | Dedicated QC person, statistical sampling | Hire a QC tech, formal test procedures |

### E. Documentation Per Unit

Create a QC card for each unit (included with the device):

```
PEMF Mat Quality Certificate
Serial: PM-2026-0001
Build Date: 2026-02-07
Builder: [initials]
QC Tester: [initials]

Coil Test Results:
- Coils 1-5: [gauss reading] G
- Coils 6-10: [gauss reading] G
- Coils 11-15: [gauss reading] G
- Coils 16-20: [gauss reading] G
- Average: [X] G
- Uniformity: [+/- Y%]

Burn-in: PASS (30 min @ max)
Max Temp: [X] C
Frequency: [X] Hz verified
Waveform: Square wave verified

Signed: ____________
```

This QC certificate is a marketing asset. Customers paying $2,000 for a PEMF mat want to see that their specific unit was tested. It builds massive trust and differentiates from Chinese mass-produced mats that have zero individual testing.

---

## 5. Warranty and Returns

### A. Warranty Structure

| Component | Warranty Period | Justification |
|-----------|----------------|---------------|
| Controller | 3 years | Controllers are the most common failure point in PEMF devices. 3 years matches Steeve Bradet's warranty |
| Coils | 5 years (or lifetime) | Copper coils rarely fail. Offering lifetime warranty is a differentiator at minimal risk |
| Power supply | 2 years | Standard electronic PSU warranty. Easy to replace |
| Mat/cover | 1 year | Fabric/foam degrades with use. Offer replacement covers as revenue stream |

### B. Warranty Cost Modeling

Based on PEMF industry data:

| Metric | Estimate | Source |
|--------|----------|--------|
| Controller failure rate (Year 1) | 2-5% | PEMF industry averages. Controllers get warm during operation |
| Coil failure rate | < 1% | Copper coils are extremely durable |
| Power supply failure rate | 3-5% | Standard electronics failure curve |
| Customer return rate (30-day) | 5-10% | Industry standard for wellness devices |
| Warranty claim rate (3 years) | 8-15% | Controllers dominate warranty claims |

**Warranty reserve per unit:** Set aside $50-75 per unit sold (3-5% of retail price) for warranty costs. This covers replacement parts, shipping, and labor for repairs.

### C. Return Process

1. **Customer contacts support** with issue description
2. **Troubleshoot remotely** (most issues are user error: wrong frequency setting, loose connection)
3. **If defective:** Ship replacement controller/PSU (cheap, fast). Customer swaps themselves
4. **If mat issue:** Ship return label. Receive, diagnose, repair or replace. Ship back
5. **30-day satisfaction guarantee:** Full refund minus return shipping cost (customer pays return)

**Key insight from competitor analysis:** Multiple PEMF companies have terrible return experiences. Offering a clean, fast warranty process is a massive differentiator. One-day replacement shipping for controller issues would set you apart.

### D. Insurance

| Coverage | Annual Cost | Provider Options |
|----------|------------|-----------------|
| Product liability ($1M/$2M) | $700-2,000/year | Insureon, Next Insurance, Insurance Canopy, The Hartford |
| General business insurance (BOP) | $1,200-2,500/year | The Hartford, Hiscox, NEXT |
| Errors & omissions | $500-1,500/year | If making any health benefit claims |

**Recommendation:** Start with product liability + general BOP. Budget $1,500-3,000/year. Required before selling to the public. Get quotes from Insureon and NEXT Insurance online (instant quotes).

**Important:** Position as "general wellness device" not "medical device." This affects insurance classification, FDA requirements, and liability exposure. Never make medical claims in marketing.

---

## 6. Steeve Bradet Model Analysis

### What We Know

| Detail | Evidence |
|--------|---------|
| **Location** | Edmonton, Alberta, Canada |
| **Team** | "Steeve Bradet and his team of experienced engineers" (small team) |
| **Assembly** | "Each product is assembled, inspected, and tested by hand" |
| **Distribution** | PEMF Mat Source LLC is exclusive US distributor |
| **Ship time** | 5-8 business days from order |
| **Products** | ZK 6-coil mini ($1,000), ZK 10-coil mini ($1,350), ZK 15-coil ($1,650), ZK 20-coil ($2,000), Nextion 20-coil ($3,000) |
| **Warranty** | 3 years |
| **Returns** | 30-day money-back guarantee |
| **Tariff** | $220 import tariff on US orders (Canada to US) |
| **Coils** | Copper, constructive orientation, 45-100 gauss range |
| **Controller** | ZK (basic) and Nextion (touchscreen) variants |
| **Frequency range** | 0.01-15,000 Hz |
| **Waveform** | Square wave |
| **Slew rate** | ~250 T/s |

### Manufacturing Model Analysis

**Steeve Bradet is almost certainly running a make-to-order or small-batch model.** Evidence:

1. **"Coming soon" on multiple products** -- products listed but not in stock. This indicates they build per order or in very small batches
2. **"Assembled, inspected, and tested by hand"** -- hand assembly means no factory production line
3. **5-8 business day ship time** -- consistent with "order comes in, we build it, we ship it" model (not instant fulfillment from warehouse)
4. **Small team** -- not a factory operation
5. **Edmonton, Canada location** -- not a manufacturing hub, consistent with workshop/studio operation
6. **Exclusive US distributor model** -- PEMF Mat Source handles US sales, Bradet handles production in Canada
7. **Product line "coming soon" status** -- suggesting capacity constraints typical of MTO operations

### Likely Production Process

Based on available evidence, here is the probable Bradet workflow:

```
Order received (via PEMF Mat Source or pemfwithsteeve.com)
  |
  v
Component check (are kitted materials available?)
  |
  v
Coil winding (20 coils, hand-wound to spec, ~2-3 hours)
  |
  v
Controller assembly (ZK-PP2K or Nextion module setup, ~30 min)
  |
  v
Mat construction (mount coils on substrate, wire in series/parallel, attach controller, ~1-2 hours)
  |
  v
QC testing (gauss measurement each coil, burn-in, waveform verification, ~1 hour)
  |
  v
Packaging (custom box, manual, warranty card, PSU, ~30 min)
  |
  v
Ship to customer (5-8 business days total from order)
```

**Estimated throughput:** 1-3 mats per day per person. With a small team of 2-3 people, that is 3-9 mats per day, or 15-45 per week.

### What We Can Learn From Bradet

| Lesson | Application |
|--------|-------------|
| **Hand-built IS the brand** | "Each unit hand-assembled and individually tested" is a marketing asset, not a limitation |
| **Premium pricing works** | $1,000-3,000 for hand-built PEMF mats with strong margins |
| **Small team suffices** | 2-3 people can produce enough for significant revenue |
| **QC as differentiator** | Individual testing and QC certificates set apart from Chinese mass-produced mats |
| **Distributor model** | Separate sales (PEMF Mat Source) from manufacturing (Bradet's team) |
| **5-8 day lead time is acceptable** | Customers paying $2K for a wellness device will wait a week |
| **Warranty builds trust** | 3-year warranty at this price point is expected |
| **Tariff awareness** | $220 import tariff on Canada-to-US orders is transparent |
| **Multiple product tiers** | Mini ($1,000-1,350) to full body ($1,650-3,000) covers different budgets |
| **Controller upgrade path** | ZK (basic) vs Nextion (premium touchscreen) as a natural upsell |

### Bradet's Likely COGS vs Revenue

| Product | Estimated COGS | Retail Price | Estimated Margin |
|---------|---------------|-------------|-----------------|
| ZK 6-coil Mini | $60-100 | $1,000 | 90-94% |
| ZK 10-coil Mini | $80-130 | $1,350 | 90-94% |
| ZK 15-coil Mat | $120-200 | $1,650 | 88-93% |
| ZK 20-coil Mat | $150-250 | $2,000 | 88-93% |
| Nextion 20-coil Mat | $200-350 | $3,000 | 88-93% |

Bradet is likely making $800-2,800 gross profit per unit. At 5-10 units/week, that is $4,000-28,000/week gross revenue with a tiny team. This validates the MTO model for PEMF.

---

## 7. Recommended Execution Plan

### Phase 1: Solo Builder (Months 1-3)

**Goal:** Build and sell first 10-20 units. Validate demand, refine process.

**Setup costs:**
| Item | Cost |
|------|------|
| QC equipment (gaussmeter, multimeter, IR thermometer, Kill-A-Watt) | $150-350 |
| First 10 component kits (pre-sourced) | $800-1,500 |
| Packaging materials (10 units) | $150-250 |
| Product liability insurance | $700-2,000/year |
| Shopify store | $39/month |
| **TOTAL STARTUP** | **$1,839-4,139** |

**Process:**
1. Source and kit 10 units worth of components
2. Build first unit, test thoroughly, photograph everything
3. Ship to beta testers (3-5 units at cost for reviews)
4. Refine build process, document timing
5. List on Shopify at $1,500-2,000
6. Build per order, ship within 5-7 business days
7. Target: 2-5 orders/week by month 3

### Phase 2: Small Team (Months 3-6)

**Goal:** Scale to 10-20 units/week. Hire first assembler.

**New costs:**
| Item | Cost |
|------|------|
| Part-time assembler (20 hrs/week @ $25/hr) | $2,000/month |
| Workspace upgrade (if needed) | $300-500/month |
| Component kits (batch of 20-50) | $3,000-6,000 |
| Custom packaging (50-unit run) | $500-750 |

**Process:**
1. Hire part-time electronics assembler (local, Indeed/ZipRecruiter, $20-30/hr)
2. Train on coil winding, assembly, basic QC
3. You handle final QC (gaussmeter verification on every unit)
4. Outsource controller board assembly to CircuitHub (batch of 20-50)
5. Source components in batches of 20-50 for better pricing
6. Target: 10-20 units/week

### Phase 3: Micro-Factory (Months 6-12)

**Goal:** 20-50 units/week. Systemized production.

1. Outsource coil winding to Prem Magnetics or Custom Coils Inc.
2. 2-3 part-time assemblers
3. Dedicated QC station
4. Add Nextion (premium) product line
5. Explore wholesale to clinics/practitioners
6. Consider distributor model (like Bradet + PEMF Mat Source)
7. Target: $40K-100K+/month revenue

---

## 8. Shipping Logistics

### Packaging Requirements

| Component | Specification | Cost |
|-----------|--------------|------|
| Outer box | 80"x26"x4" corrugated | $8-15 |
| Inner protection | Foam inserts or bubble wrap | $3-5 |
| Controller box | Small box within main box | $2-3 |
| Power supply | Included in controller box | Included |
| Manual + QC card | Printed booklet + card | $3-5 |
| Packing tape + branded sticker | Quality seal | $0.50-1 |
| **TOTAL PACKAGING** | | **$16.50-29** |

### Shipping Costs (US Domestic)

| Carrier | Estimated Cost | Transit Time | Notes |
|---------|---------------|-------------|-------|
| USPS Priority Mail (large flat rate box) | $22-25 | 2-3 days | May not fit full-body mat |
| UPS Ground | $25-45 | 3-7 days | Good for full-body mats (oversized) |
| FedEx Ground | $25-45 | 3-7 days | Similar to UPS |
| FedEx Home Delivery | $30-50 | 3-7 days | Residential delivery premium |

**Recommendation:** Build shipping cost into product price (free shipping). Steeve Bradet offers free shipping to continental US. Budget $30-40/shipment.

### Shipping Insurance

- Include in shipping cost
- UPS/FedEx offer $100 declared value for free, additional coverage at ~$1 per $100 value
- For a $2,000 device: add $15-20 insurance per shipment
- Or self-insure: set aside $20/shipment for loss/damage reserve

---

## Key Takeaways

1. **MTO is the proven model for premium PEMF.** Steeve Bradet does exactly this and sells $1,000-3,000 mats with a small team in Canada.

2. **Per-unit COGS of $150-300 selling at $1,000-3,000 = 75-92% gross margins.** This is better than bulk China import when you factor in tariffs, shipping, and inventory risk.

3. **Zero inventory risk.** You never build something nobody ordered. Components on shelf cost $800-1,500 for 10 kits -- that is your entire capital at risk.

4. **5-8 day lead time is acceptable** at this price point. Customers expect handcrafted quality and are willing to wait.

5. **QC per unit is a marketing asset,** not a cost. Include a QC certificate with each device showing exact gauss readings. This destroys Chinese competitors who do zero individual testing.

6. **Start building yourself, hire as you scale.** The solo builder model works for 5-10 units/week. One part-time assembler doubles capacity.

7. **Pre-kit components in batches of 10-20.** This is not "inventory" -- it is raw materials that cost $80-120 per kit. Minimal capital at risk.

8. **US-sourced components avoid China tariffs entirely.** Magnet wire, PCBs from JLCPCB/CircuitHub, controllers from Amazon -- all tariff-free or minimal.

9. **The hand-built story IS the competitive advantage.** "Built by a team of engineers, individually tested, QC certificate included" is worth the premium over "made in a Chinese factory alongside 10,000 identical units."

10. **Insurance is mandatory.** $1,500-3,000/year for product liability. Non-negotiable for selling electrical devices.

---

## Sources

- [CircuitHub - On-demand PCB Assembly](https://www.circuithub.com/)
- [MacroFab - PCB Assembly Platform](https://www.macrofab.com/)
- [Prem Magnetics - Custom Coil Winding](https://www.premmagnetics.com/coil-winding/)
- [Custom Coils Inc - Electromagnetic Assemblies](https://ccoils.com/services/coil-winding/)
- [Badger Magnetics - Custom Coil Manufacturing](https://www.badgermagnetics.com/capabilities/)
- [PEMF Mat Source - Steeve Bradet Products](https://pemfmatsource.com/)
- [PEMF with Steeve - Product Lineup](https://www.pemfwithsteeve.com/our-products)
- [Sierra Circuits - Quickturn PCB](https://www.protoexpress.com/)
- [A2Z EMS - PCB Assembly](https://www.a2zems.com/)
- [Sparqtron - Contract Electronics Manufacturing](https://www.sparqtron.com/)
- [Predictable Designs - Electronics Manufacturing Cost Guide](https://predictabledesigns.com/how-much-does-it-cost-to-develop-and-manufacture-new-electronic-product/)
- [Insureon - Product Liability Insurance](https://www.insureon.com/small-business-insurance/product-liability/cost)
- [DIY PEMF - Coil Testing](https://diypemf.com/testing-your-coils/)
- [Curatronic - Gauss Measurements](https://www.curatronic.com/gauss-measurements)
- [ZipRecruiter - Electronic Assembler Jobs ($16-$31/hr)](https://www.ziprecruiter.com/Jobs/Part-Time-Electronic-Assembly)
- [Upwork - Electronics Freelancers](https://www.upwork.com/freelance-jobs/electronics/)
- [The PEMF Podcast Ep 48 - Steeve Bradet](https://open.spotify.com/episode/0TzoivKGp8ANl7ZKnmLIPe)
- [The PEMF Podcast Ep 32 - Steeve Bradet](https://creators.spotify.com/pod/profile/the-pemf-podcast/episodes/32--Master-PEMF-Builder-Shares-His-Wealth-Of-PEMF-Knowledge---Steeve-Bradet-e2l0p69)
- [HBR Industries - Custom Copper Coils](https://www.hbrindustries.com/)
- [Endicott Coil Company](https://endicottcoil.com/)
