# Gumroad Launch Execution Guide - Ship in 8-12 Hours

**Conservative Week 1 Revenue:** $451 net ($480 gross)
**Time to First Dollar:** 8-12 hours total work
**Startup Cost:** $0 (Gumroad free until first sale)

**Last Updated:** 2026-02-04

---

## EXECUTION PRIORITY (Do These in Order)

### TIER 1 - Human Setup (5 minutes)
**BLOCKING: Must complete before anything else**

1. Create Gumroad account (gumroad.com)
2. Connect Stripe for payouts
3. Set payout schedule to Weekly

**Status:** ⬜ NOT STARTED

---

### TIER 2 - P0 Products (List These First)

| Product | Price | Hours | Week 1 Sales | Revenue | Priority |
|---------|-------|-------|--------------|---------|----------|
| **P0-1: Funnel Teardown** | $7 | 2-3 | 17 | $119 | 🔴 HIGHEST |
| **P0-2: Paywall Playbook** | $27 | 3-4 | 9 | $243 | 🔴 HIGHEST |
| **P0-3: Cold Email Stack** | $27 | 2-3 | 3 | $81 | 🟡 HIGH |
| **P0-4: Clipping Business** | $37 | 2-3 | 1 | $37 | 🟡 HIGH |

**Total:** 9-13 hours, $480 gross, $451 net

---

## P0-1: FUNNEL TEARDOWN ($7) - SHIP FIRST

### Source Files
✅ **Already exists:** `03_PLAYBOOKS/DIGITAL_PRODUCTS/listings/funnel_teardown_clavvicular_gumroad.md`
✅ **Source content:** `OPS/TREND_INTEL/analyses/CLAVVICULAR_FUNNEL_BREAKDOWN.md` (584 lines)

### Execution Steps

**Step 1: Export to PDF (1 hour)**

```bash
# Option A: Pandoc (if installed)
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
pandoc OPS/TREND_INTEL/analyses/CLAVVICULAR_FUNNEL_BREAKDOWN.md \
  -o DIGITAL_PRODUCTS/pdfs/funnel-teardown-clavvicular.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in

# Option B: Notion (easier, recommended)
# 1. Copy CLAVVICULAR_FUNNEL_BREAKDOWN.md content
# 2. Paste into new Notion page
# 3. File > Export > PDF
# 4. Save to DIGITAL_PRODUCTS/pdfs/
```

**Step 2: Create Cover (30 min)**

Use Canva (canva.com):
1. Search "eBook Cover" template (1600x2400px)
2. Title: "The Clipping Army Model"
3. Subtitle: "$70K/mo funnel teardown"
4. Brand: "PRINTMAXX"
5. Colors: Dark charcoal background, white/green text
6. Export as PDF → save to DIGITAL_PRODUCTS/covers/

**Step 3: Merge PDFs (10 min)**

Mac Preview:
1. Open cover.pdf in Preview
2. View > Thumbnails
3. Drag content.pdf pages into sidebar
4. File > Export as PDF
5. Save as: `DIGITAL_PRODUCTS/final/funnel-teardown-clavvicular-FINAL.pdf`

**Step 4: Create Gumroad Listing (30 min)**

Use listing copy from: `03_PLAYBOOKS/DIGITAL_PRODUCTS/listings/funnel_teardown_clavvicular_gumroad.md`

**Product Name:** $70K/month from a $200 tech stack: full funnel teardown

**Price:** $7

**Description:**
```
a 22 year old runs a $70K/month business on $200/month in tools. i spent 6 hours taking his entire funnel apart. this is everything i found.

this is not a "10 tips for building a community" PDF. this is a surgical teardown of a real funnel generating real revenue, with the exact numbers, tools, scripts, and structures you can replicate.

what's inside:

- full revenue breakdown: $49/month Skool (1,400 members) + $25/month female edition + $3-5K coaching closes. math on every layer
- the clipping army model: how 750 people redistribute his content (some with 70K+ followers each). why this generates 10x the reach of paid ads
- VSSL script framework: the 9-step video sales letter structure that converts 43K monthly visitors. fill-in-the-blank version included
- unique mechanism naming: why "Ascension" converts where "better looksmaxxing" doesn't
- Skool retention playbook: timed content gates at day 7, 10, and 14
- tech stack with costs: Framer ($20), Wistia ($19), Skool ($99). total: under $200/month
- 12 weaknesses i found and the fixes for each
- niche adaptation worksheet: fill-in-the-blank templates for 5 niches

$7. cheaper than lunch. worth more than most courses.
```

**Categories:** Business, Marketing, Education

**Tags:** funnel teardown, Skool community, content creator, clipping army, sales funnel

**Thumbnail:** Upload cover PDF first page as thumbnail

**Step 5: Test Purchase (10 min)**

1. Click "View Product" link
2. Buy your own product for $1 (set custom price)
3. Verify download works
4. Refund yourself via Gumroad dashboard

**Status:** ⬜ NOT STARTED

---

## P0-2: PAYWALL PLAYBOOK ($27) - SHIP SECOND

### Source Files
✅ **Listing copy:** `03_PLAYBOOKS/DIGITAL_PRODUCTS/listings/paywall_playbook_gumroad.md`
✅ **Source content:**
- `MONEY_METHODS/APP_FACTORY/PAYWALL_PSYCHOLOGY_AB_PLAYBOOK.md`
- biomaxx implementation code
- Medium article (if exists)

### Execution Steps

**Step 1: Compile Master Doc (1.5 hours)**

Create new document in this order:
1. Introduction (300 words about 8x revenue)
2. Full Paywall Psychology Playbook content
3. Code implementation examples
4. A/B testing framework
5. Conclusion + implementation checklist

Save to: `DIGITAL_PRODUCTS/source/paywall-playbook-master.md`

**Step 2: Export to PDF (30 min)**

Same process as P0-1 (Notion or Pandoc)

**Step 3: Create Cover (30 min)**

Canva concept:
- Title: "The Hard Paywall Playbook"
- Subtitle: "8x revenue apps use hard paywalls"
- Visual: Two bar charts (Freemium small, Hard Paywall 8x taller)
- Colors: Dark charcoal, green/teal accents

**Step 4: Create Gumroad Listing (30 min)**

**Product Name:** the freemium trap is costing you 8x revenue. here's the fix.

**Price:** $27

**Description:** (See `paywall_playbook_gumroad.md` for full copy)

**Step 5: Test & Publish (10 min)**

**Status:** ⬜ NOT STARTED

---

## P0-3: COLD EMAIL STACK ($27) - SHIP THIRD

### Source Files
✅ **Listing copy:** `03_PLAYBOOKS/DIGITAL_PRODUCTS/listings/cold_email_sequences_gumroad.md`
✅ **Source content:** `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES.md` (698 lines)

### Execution Steps

**Step 1: Structure Content (1 hour)**

Create master doc:
1. Cold email fundamentals
2. 6-question framework
3. 4 core sequences
4. 7 vertical-specific sequences
5. LinkedIn templates
6. Deliverability guide

**Step 2-5:** Same process as previous products

**Cover concept:**
- Inbox mockup with green "Replied" badges
- Title: "COLD EMAIL SEQUENCES"
- Subtitle: "that actually convert"

**Status:** ⬜ NOT STARTED

---

## P0-4: CLIPPING BUSINESS ($37) - SHIP FOURTH

### Source Files
✅ **Listing copy:** `03_PLAYBOOKS/DIGITAL_PRODUCTS/listings/clipping_army_playbook_gumroad.md`
✅ **Source content:** `MONEY_METHODS/STREAMER_CLIPS/CLIPPING_BUSINESS_PLAYBOOK.md` (667 lines)

### Execution Steps

Same 5-step process. Cover concept:
- Purple gradient background
- Scissors + play button icon
- Title: "THE CLIPPING ARMY PLAYBOOK"
- Subtitle: "10x reach. zero ad spend."

**Status:** ⬜ NOT STARTED

---

## LAUNCH DAY ACTIONS (2 Hours After All 4 Live)

### 1. Publish All Products (30 min)
- [ ] Set all to "Published"
- [ ] Verify Stripe connected
- [ ] Double-check prices
- [ ] Test purchase flow on each

### 2. Create Launch Posts (30 min)

**Twitter/X (4 posts, one per product):**

```
i reverse-engineered the $70K/mo community funnel. full breakdown: [link]

584 lines. zero fluff. $7.
```

```
hard paywalls generate 8x more revenue than freemium. here's why + full implementation code: [link]

500+ lines. RevenueCat integration included. $27.
```

```
11 cold email sequences. tested on real outbound campaigns: [link]

copy/paste ready. $27.
```

```
how to build a clipping army that drives 10M views/month: [link]

VA hiring guide + monetization paths included. $37.
```

### 3. Cross-Post (30 min)

**LinkedIn:** Professional angle, link in comments
**Reddit:** Value-first posts in:
- r/SideProject
- r/EntrepreneurRideAlong
- r/iOSProgramming (for paywall)
- r/coldemail (for sequences)

**IndieHackers:** Launch post with story

### 4. Update Bio Links (30 min)

Add Gumroad product links to:
- [ ] Twitter/X bio
- [ ] LinkedIn bio
- [ ] GitHub profile (if applicable)
- [ ] Personal website

---

## WEEK 1 PROMOTION (15 min/day × 7 days)

### Daily Actions

**Day 1-2:** Launch posts (1 per product per day)
**Day 3-4:** Value posts with product mentions
**Day 5-7:** Case study posts

### Example Value Post

```
the 6-question framework for cold emails that don't get ignored:

1. what you do
2. who you do it for
3. how you do it
4. what problem you solve
5. proof it works
6. what the ROI looks like

answer these in under 100 words. your cold email writes itself.

full breakdown in my cold email playbook: [link]
```

---

## REVENUE PROJECTIONS

### Conservative (Baseline)

| Product | Price | Week 1 Sales | Gross | Net (after 10% fee) |
|---------|-------|--------------|-------|---------------------|
| Funnel Teardown | $7 | 17 | $119 | $107 |
| Paywall Playbook | $27 | 9 | $243 | $219 |
| Cold Email | $27 | 3 | $81 | $73 |
| Clipping Army | $37 | 1 | $37 | $33 |
| **TOTAL** | | **30** | **$480** | **$432** |

After Stripe fees (2.9% + $0.30): **$451 net**

### Moderate (With Good Promotion)

| Product | Price | Week 1 Sales | Net |
|---------|-------|--------------|-----|
| Funnel Teardown | $7 | 30 | $189 |
| Paywall Playbook | $27 | 15 | $364 |
| Cold Email | $27 | 8 | $194 |
| Clipping Army | $37 | 3 | $99 |
| **TOTAL** | | **56** | **$846** |

### Optimistic (Viral Post)

| Product | Price | Week 1 Sales | Net |
|---------|-------|--------------|-----|
| Funnel Teardown | $7 | 50 | $315 |
| Paywall Playbook | $27 | 25 | $607 |
| Cold Email | $27 | 12 | $291 |
| Clipping Army | $37 | 5 | $165 |
| **TOTAL** | | **92** | **$1,378** |

---

## TIME BREAKDOWN

| Task | Time |
|------|------|
| Gumroad + Stripe setup | 5 min |
| P0-1: Funnel Teardown | 2-3 hrs |
| P0-2: Paywall Playbook | 3-4 hrs |
| P0-3: Cold Email Stack | 2-3 hrs |
| P0-4: Clipping Business | 2-3 hrs |
| Launch posts + promotion | 2 hrs |
| **TOTAL** | **11-15 hrs** |

**Realistic timeline:** 2 days (6-8 hours per day)

---

## BLOCKERS (Human Action Required)

### TIER 1 - Must Do First (5 minutes)
- [ ] Create Gumroad account
- [ ] Connect Stripe
- [ ] Verify email

### TIER 2 - Nice to Have (Optional)
- [ ] Twitter/X account (for promotion)
- [ ] Canva account (for covers, free tier OK)
- [ ] Notion account (for PDF export, free tier OK)

---

## AFTER LAUNCH

### Week 2: Upsell Funnels

**Add to each PDF (last page):**

```
want me to implement this for you?

[Product-specific offer]
- 60-90 min implementation call: $300-$500
- Done-for-you setup: $750-$1,500
- Ongoing optimization: $300-$800/month

book a call: [TYPEFORM LINK]

limited to 3-5 clients per month.
```

### Week 2: Create Bundles

**Bundle 1:** Funnel Teardown + Paywall Playbook = $29 (save $5)
**Bundle 2:** All 4 products = $59 (save $39)

---

## METRICS TO TRACK

| Metric | Tool | Target Week 1 |
|--------|------|---------------|
| Page views | Gumroad Analytics | 500+ |
| Conversion rate | Gumroad Analytics | 2-5% |
| Total sales | Gumroad Dashboard | 30+ |
| Revenue | Gumroad Dashboard | $450+ |
| Traffic source | Gumroad Analytics | Which posts drive sales |

---

## COMMON QUESTIONS

**"Do I need a big audience?"**

No. You need 500-1,000 targeted page views. Share in relevant communities (r/SideProject, r/EntrepreneurRideAlong, IndieHackers), not just your followers.

**"What if no one buys?"**

Week 1 conservative = $450. If you hit $100-200, that's still first dollar. Iterate on listing copy, add testimonials, improve promotion.

**"How do I get testimonials with zero sales?"**

Give 3-5 copies free to relevant people for honest feedback. Add testimonials to listing.

**"Should I discount?"**

No discounts Week 1. Launch at full price. Add time-limited discount Week 2 if sales slow.

---

## NEXT STEPS AFTER $450

1. **Monitor sales daily** - Check Gumroad every morning
2. **Respond to questions** - Answer DMs within 24 hours
3. **Add testimonials** - Update listings as positive feedback arrives
4. **Create more products** - P1 tier (Notion templates, more playbooks)
5. **Build email list** - Add free lead magnet to capture emails

---

**STATUS:** 4 products ready to compile. Conservative Week 1 revenue: $451 net.

**ACTION:** Start with P0-1 (Funnel Teardown). Ship in 2-3 hours. Then move to P0-2.

**EXECUTE.**

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
