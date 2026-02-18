# MASTER UPLOAD CHECKLIST — All Platforms

**Date:** 2026-02-12
**Total products across all platforms:** 41 listings (13 Gumroad + 8 Whop + 20 Etsy)
**Estimated total upload time:** 2-3 hours (once accounts exist)
**Estimated monthly revenue at 2-5 daily sales:** $600-2,500/mo

---

## PHASE 0: Account Creation (Must Do First)

- [ ] **Stripe** — dashboard.stripe.com/register (required for Gumroad + Etsy payments)
- [ ] **Gumroad** — gumroad.com/signup (connect Stripe in Settings > Payments)
- [ ] **Whop** — whop.com (create account, 3% fee)
- [ ] **Etsy** — etsy.com/sell (shop name: "PrintMaxxDigitals", $0.20/listing fee)

---

## PHASE 1: Convert Product Files to PDF

Before uploading to any platform, convert markdown product files to PDF:

```bash
cd PRODUCTS/GUMROAD_INSTANT_UPLOAD && bash convert_to_pdf.sh
```

If pandoc not installed: `brew install pandoc` or use markdowntopdf.com manually.

---

## PHASE 2: GUMROAD (13 products)

**Directory:** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/`
**Metadata:** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/LISTING_METADATA.md`
**Fee:** 10% per sale

Upload in this order (free lead magnet first, then ascending price):

| # | Product | Price | File | Status |
|---|---------|-------|------|--------|
| [ ] | 10. Free AI Prompts (Lead Magnet) | $0+ (PWYW) | `10_free_lead_magnet.md` | |
| [ ] | 11. Cold Email Subject Lines (73) | $3 | `11_cold_email_subject_lines.md` | |
| [ ] | 12. Viral Tweet Templates | $3 | `12_viral_tweet_templates.md` | |
| [ ] | 13. Local Biz Cold Email Pack | $5 | `13_local_biz_cold_email_pack.md` | |
| [ ] | 09. Funnel Teardown Guide | $7 | `09_funnel_teardown_guide.md` | |
| [ ] | 08. Sleep YouTube Starter | $7 | `08_sleep_youtube_starter.md` | |
| [ ] | 04. AI Content Farm Blueprint | $9 | `04_ai_content_farm_blueprint.md` | |
| [ ] | 05. Cold Email Playbook | $9 | `05_cold_email_playbook.md` | |
| [ ] | 06. Twitter Growth Playbook | $9 | `06_twitter_growth_playbook.md` | |
| [ ] | 07. Solopreneur Tech Stack | $9 | `07_solopreneur_tech_stack.md` | |
| [ ] | 02. AI Automation Toolkit | $19 | `02_ai_automation_toolkit.md` | |
| [ ] | 03. Vibe Coding Playbook | $19 | `03_vibe_coding_playbook.md` | |
| [ ] | 01. Local Biz Client System | $29 | `01_local_biz_client_system.md` | |

**After uploading all 13:**
- [ ] Set up upsell chain (each product upsells next tier — see LISTING_METADATA.md)
- [ ] Enable "Pay what you want" on products 10-13 (with minimum)
- [ ] Create 3 bundles: Starter ($19), Growth ($39), Complete ($59)
- [ ] Enable Gumroad Discover (marketplace visibility)
- [ ] Set up Gumroad affiliate program (25% commission default)

---

## PHASE 3: WHOP (8 products)

**Directory:** `PRODUCTS/WHOP_INSTANT_UPLOAD/`
**Fee:** 3% per sale (much lower than Gumroad)

| # | Product | Price | File | Status |
|---|---------|-------|------|--------|
| [ ] | 1. Funnel Teardown Guide | $7 | `01_whop_listing.md` | |
| [ ] | 2. Cold Email Playbook | $27 | `02_whop_listing.md` | |
| [ ] | 3. AI Automation Toolkit | $47 | `03_whop_listing.md` | |
| [ ] | 4. Vibe Coding Playbook | $47 | `04_whop_listing.md` | |
| [ ] | 5. Solopreneur Tech Stack | $17 | `05_whop_listing.md` | |
| [ ] | 6. Twitter Growth Playbook | $27 | `06_whop_listing.md` | |
| [ ] | 7. Sleep YouTube Starter | $17 | `07_whop_listing.md` | |
| [ ] | 8. AI Content Farm Blueprint | $47 | `08_whop_listing.md` | |

**After uploading all 8:**
- [ ] Enable Whop marketplace listing
- [ ] Set up affiliate program

---

## PHASE 4: ETSY (20 products)

**Directory:** `PRODUCTS/ETSY_INSTANT_UPLOAD/`
**Full listings:** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md`
**Fee:** $0.20/listing + 6.5% transaction + 3% payment (~$4.00 total upfront for 20 listings)

Upload in revenue-optimized order:

| # | Product | Price | Listing # in File | Status |
|---|---------|-------|--------------------|--------|
| [ ] | Notion Budget Tracker | $9.99 | Listing 11 | |
| [ ] | Notion Habit Tracker | $7.99 | Listing 12 | |
| [ ] | Printable Planner Bundle | $11.99 | Listing 19 | |
| [ ] | Canva Social Templates 100-pack | $14.99 | Listing 16 | |
| [ ] | Notion Content Calendar | $12.99 | Listing 13 | |
| [ ] | AI Prompts Pack | $2.99 | Listing 10 | |
| [ ] | Local Biz Client System | $27.99 | Listing 1 | |
| [ ] | Cold Email Playbook | $9.99 | Listing 5 | |
| [ ] | Twitter Growth Playbook | $9.99 | Listing 6 | |
| [ ] | Solopreneur Tech Stack | $9.99 | Listing 7 | |
| [ ] | AI Automation Toolkit | $14.99 | Listing 2 | |
| [ ] | Vibe Coding Playbook | $14.99 | Listing 3 | |
| [ ] | AI Content Farm Blueprint | $14.99 | Listing 4 | |
| [ ] | Sleep YouTube Starter | $9.99 | Listing 8 | |
| [ ] | Funnel Teardown Guide | $7.99 | Listing 9 | |
| [ ] | Notion Meal Planner | $8.99 | Listing 14 | |
| [ ] | Notion Reading Tracker | $6.99 | Listing 15 | |
| [ ] | Canva Presentation Templates | $12.99 | Listing 17 | |
| [ ] | Canva Resume Bundle | $11.99 | Listing 18 | |
| [ ] | Goal Setting Workbook | $9.99 | Listing 20 | |

**After uploading all 20:**
- [ ] Enable auto-renew on all listings
- [ ] Set quantity to 999 on all
- [ ] Add shop sections: "Business Playbooks", "Notion Templates", "Canva Templates", "Printable Planners"
- [ ] Set up Etsy Ads ($1/day initial budget)
- [ ] Optimize SEO tags based on Etsy search suggestions

---

## PHASE 5: ALSO LIST ON (Bonus Platforms — Same Products)

### Fiverr (10 service gigs — NOT products)
**Directory:** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md`
- [ ] Create Fiverr seller account
- [ ] List 10 gigs (service versions of our products + done-for-you offers)
- [ ] See `OPS/FIVERR_LAUNCH_PACKAGE.md` for full gig copy

### Upwork (5 profiles)
**Directory:** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md`
- [ ] Create Upwork freelancer account
- [ ] Set up 5 specialized profiles
- [ ] See `OPS/UPWORK_LAUNCH_CHECKLIST.md` for full setup

### Redbubble (20 POD designs)
**Source:** `PRODUCTS/ECOM_LISTINGS_READY/REDBUBBLE_UPLOAD_READY_20.md`
- [ ] Create Redbubble account (free)
- [ ] Upload 20 designs

### Amazon KDP (10-15 journals)
**Source:** `PRODUCTS/KDP_JOURNALS_10.md` + `PRODUCTS/KDP_JOURNALS_5.md`
- [ ] Create KDP account (free, uses Amazon account)
- [ ] Upload 10-15 journal interiors + covers

---

## PHASE 6: POST-UPLOAD OPTIMIZATION

- [ ] Cross-link all platforms (Gumroad bio links to Whop, Etsy links to Gumroad, etc.)
- [ ] Create one "link in bio" page listing all products (use linktr.ee or carrd.co free tier)
- [ ] Set up email capture on Gumroad (collect emails from $0 lead magnet downloads)
- [ ] Schedule social posts promoting products (Buffer CSVs at `AUTOMATIONS/content_posting/`)
- [ ] Log first revenue: `python3 scripts/revenue_intake.py log --method MM_DIGITAL_PRODUCTS --amount X --source gumroad`

---

## REVENUE PROJECTIONS

| Platform | Products | Avg Price | Sales/Day Target | Monthly Revenue |
|----------|----------|-----------|------------------|-----------------|
| Gumroad | 13 | $10.23 | 2-5 | $600-1,500 |
| Whop | 8 | $28.88 | 1-2 | $860-1,730 |
| Etsy | 20 | $11.33 | 3-8 | $1,020-2,720 |
| **Total** | **41** | — | **6-15** | **$2,480-5,950** |

These are realistic Day 60-90 targets assuming basic SEO optimization and social promotion.

---

## FILE REFERENCE

| Directory | Contents | Count |
|-----------|----------|-------|
| `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` | 13 product files + metadata + README + convert script | 16 files |
| `PRODUCTS/WHOP_INSTANT_UPLOAD/` | 8 listing files + README | 10 files |
| `PRODUCTS/ETSY_INSTANT_UPLOAD/` | All 20 listings in one file + README | 3 files |
| `PRODUCTS/ECOM_LISTINGS_READY/` | Enhanced versions, upload scripts | ~10 files |
| `PRODUCTS/FREELANCE_LISTINGS_READY/` | Fiverr + Upwork listings | 2 files |

---

*Checklist created 2026-02-12 by ops-auditor. All file paths verified.*

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
