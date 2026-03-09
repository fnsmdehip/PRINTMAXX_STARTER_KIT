# Leads and Outreach Central Index

**Created:** 2026-02-12
**Purpose:** Single source of truth for ALL lead data, email templates, scrapers, outreach tools, and pipeline status across the entire PRINTMAXX project.
**Updated by:** Any agent, every session that touches leads/outreach.

---

## Quick numbers (as of 2026-02-12)

| Metric | Count | Notes |
|--------|-------|-------|
| Total lead rows (MASTER_LEADS.csv) | 1,035 | Consolidated from city-level scrapes |
| Individual city lead CSVs | 40+ | 10 cities x 4 industries + specialty leads |
| Gov contract leads | 1,093 | SAM.gov + USAspending + UK tenders |
| Pipeline tracker rows | 87 | In AUTOMATIONS/outreach/PIPELINE_TRACKER.csv |
| Cold email CSVs generated | 12+ | Multi-step Instantly-format sequences |
| Individual cold email .txt files | 100+ | Per-business personalized emails |
| Outreach pipeline leads (LEDGER) | 10+ | LEDGER/OUTREACH_PIPELINE.csv (manual high-value) |
| Hot leads (scored, demo-ready) | 5 | AUTOMATIONS/leads/HOT_LEADS.csv |
| Emails sent | 0 | No sending infrastructure set up yet |
| Revenue from outreach | $0 | Blocked on account creation + domain purchase |

---

## 1. Lead data: where every CSV lives

### 1A. Consolidated / master files

| File | Path | Rows | What it is |
|------|------|------|------------|
| MASTER_LEADS.csv | `AUTOMATIONS/leads/MASTER_LEADS.csv` | 1,035 | All local biz leads merged. Columns: business_name, address, phone, website, google_rating, review_count, website_score, signals_detected, email_if_found, category, city, scraped_at |
| SCORED_LEADS.csv | `AUTOMATIONS/leads/SCORED_LEADS.csv` | 5 | Leads that went through scoring + demo_url assignment. Same columns as MASTER plus demo_url, demo_category, template_file, issues |
| HOT_LEADS.csv | `AUTOMATIONS/leads/HOT_LEADS.csv` | 5 | Subset of scored leads that had demos attached. Same schema as SCORED_LEADS |
| PIPELINE_TRACKER.csv | `AUTOMATIONS/outreach/PIPELINE_TRACKER.csv` | 87 | Leads with assigned IDs (L-00001 through L-00087), email, website_score, top_issue, template_used, sequence status (READY/SENT/REPLIED). This is the closest thing to a CRM right now. |
| OUTREACH_PIPELINE.csv | `LEDGER/OUTREACH_PIPELINE.csv` | 10+ | Manually curated high-value prospects (B2B SaaS, apps, gyms, newsletters). Has deal_value, sequence_name, status (cold/discovery/qualified/nurture). Different from local biz leads. |
| ECOM_LEADS.csv | `LEDGER/ECOM_LEADS.csv` | 0 (header only) | Placeholder for ecom store leads. Schema: lead_id, store_url, store_name, niche, source, tech_detected, estimated_revenue, contact_email, status |
| leads.csv | `LEDGER/leads.csv` | 0 (header only) | Landing page lead captures (email signups). Schema: date, email, source, notes. Currently empty. |

### 1B. Local business leads by city (AUTOMATIONS/leads/)

All scraped by `savvy_lead_scraper.py` or `nationwide_scraper.py`. Schema: business_name, address, phone, website, google_rating, review_count, website_score, signals_detected, email_if_found, category, city, scraped_at.

**Dentists / Dental:**

| File | City | Rows |
|------|------|------|
| dentist_atlanta_leads.csv | Atlanta | 30 |
| dentist_chicago_leads.csv | Chicago | 47 |
| dentist_dallas_leads.csv | Dallas | 29 |
| dentist_denver_leads.csv | Denver | 36 |
| dentist_houston_leads.csv | Houston | 23 |
| dentist_los_angeles_ca_leads.csv | Los Angeles | 18 |
| dentist_miami_leads.csv | Miami | 38 |
| dentist_new_york_ny_leads.csv | New York | 20 |
| dentist_phoenix_leads.csv | Phoenix | 23 |
| dentist_seattle_leads.csv | Seattle | 27 |
| dental_austin_tx_leads.csv | Austin TX | 15 |
| dental_dallas_tx_leads.csv | Dallas TX | 10 |

**Restaurants:**

| File | City | Rows |
|------|------|------|
| restaurant_atlanta_leads.csv | Atlanta | 42 |
| restaurant_austin_tx_leads.csv | Austin TX | 10 |
| restaurant_chicago_leads.csv | Chicago | 44 |
| restaurant_dallas_leads.csv | Dallas | 45 |
| restaurant_denver_leads.csv | Denver | 39 |
| restaurant_houston_leads.csv | Houston | 42 |
| restaurant_miami_leads.csv | Miami | 43 |
| restaurant_phoenix_leads.csv | Phoenix | 33 |
| restaurant_seattle_leads.csv | Seattle | 44 |

**Plumbers:**

| File | City | Rows |
|------|------|------|
| plumber_atlanta_leads.csv | Atlanta | 25 |
| plumber_chicago_leads.csv | Chicago | 27 |
| plumber_dallas_leads.csv | Dallas | 18 |
| plumber_dallas_tx_leads.csv | Dallas TX | 10 |
| plumber_denver_leads.csv | Denver | 27 |
| plumber_houston_leads.csv | Houston | 29 |
| plumber_miami_leads.csv | Miami | 25 |
| plumber_phoenix_leads.csv | Phoenix | 19 |
| plumber_seattle_leads.csv | Seattle | 22 |

**Lawyers:**

| File | City | Rows |
|------|------|------|
| lawyer_atlanta_leads.csv | Atlanta | 40 |
| lawyer_chicago_leads.csv | Chicago | 46 |
| lawyer_dallas_leads.csv | Dallas | 38 |
| lawyer_denver_leads.csv | Denver | 19 |
| lawyer_houston_leads.csv | Houston | 21 |
| lawyer_houston_tx_leads.csv | Houston TX | 10 |
| lawyer_miami_leads.csv | Miami | 40 |
| lawyer_phoenix_leads.csv | Phoenix | 35 |
| lawyer_seattle_leads.csv | Seattle | 24 |

### 1C. Government / B2B / Specialty leads (AUTOMATIONS/leads/)

| File | Rows | Source | Notes |
|------|------|--------|-------|
| sam_gov_opportunities.csv | 22 | SAM.gov API | Active solicitations. Schema: notice_id, title, solicitation_number, agency, naics_code, response_deadline, contact_email |
| sam_gov_opportunities.json | -- | SAM.gov API | Raw JSON of same data |
| gov_tenders_active.csv | 218 | gov_tenders_scraper.py | Active government tenders. Similar schema to SAM |
| usaspending_awards.csv | 800 | USAspending API | Already-awarded contracts. Schema: opportunity_id, title, agency, award_amount, deadline |
| usaspending_ai.csv | 50 | USAspending filtered | AI-related awards |
| usaspending_cybersecurity.csv | 50 | USAspending filtered | Cybersecurity awards |
| usaspending_cloud.csv | 36 | USAspending filtered | Cloud computing awards |
| usaspending_data_analytics.csv | 50 | USAspending filtered | Data analytics awards |
| uk_contracts_finder_leads.csv | 788 | UK Contracts Finder | UK government contracts |
| g2_reviewer_leads.csv | 10 | G2 scraper | G2 review data (Lemlist, etc) |
| producthunt_b2b_leads.csv | 12 | Product Hunt scraper | B2B product launches |
| indeed_hiring_leads.csv | 22 | Indeed scraper | Companies actively hiring |
| linkedin_events_leads.csv | 5 | LinkedIn scraper | Event-based leads |
| android_clone_opportunities.csv | 8 | App research | Not leads per se, app clone targets |

### 1D. Other lead files (scattered)

| File | Path | Rows | Notes |
|------|------|------|-------|
| sample_prospects.csv | `AUTOMATIONS/sample_prospects.csv` | 8 | Fake sample data for testing local_biz_pipeline.py |
| local_biz_leads_sample.csv | `AUTOMATIONS/output/local_biz_leads_sample.csv` | 24 | Early pipeline test output |
| prospects.csv (pipeline_austin_dental) | `AUTOMATIONS/output/pipeline_austin_dental/prospects.csv` | 12 | Pipeline test run output |
| prospects.csv (pipeline_low_score) | `AUTOMATIONS/output/pipeline_low_score/prospects.csv` | 16 | Pipeline test run output |
| prospects.csv (pipeline_run) | `AUTOMATIONS/AUTOMATIONS/output/pipeline_run/prospects.csv` | 20 | Pipeline test run output (nested dir, likely bug) |
| austin_dental_REAL_TEST.csv | `AUTOMATIONS/leads/austin_dental_REAL_TEST.csv` | 3 | Real test: 3 Austin dental practices with full scores |
| austin_dental_urls.csv | `AUTOMATIONS/output/austin_dental_urls.csv` | -- | URL list for pipeline input |
| low_score_urls.csv | `AUTOMATIONS/output/low_score_urls.csv` | -- | URL list for pipeline input |
| sample_local_biz_urls.csv | `AUTOMATIONS/sample_local_biz_urls.csv` | -- | Sample URLs for testing |

---

## 2. Email templates: every template across the project

### 2A. Local business cold email templates (AUTOMATIONS/email_templates/)

3-email sequence: cold, followup, breakup. Used by `mass_outreach.py` and `generate_cold_emails.py`.

| File | Path | Purpose |
|------|------|---------|
| local_biz_cold.txt | `AUTOMATIONS/email_templates/local_biz_cold.txt` | Initial outreach. "I built a website for a {industry} in {city}." $500 flat offer. |
| local_biz_followup.txt | `AUTOMATIONS/email_templates/local_biz_followup.txt` | Follow-up. Adds motion site upsell ($1,500). Two pricing options. |
| local_biz_breakup.txt | `AUTOMATIONS/email_templates/local_biz_breakup.txt` | Breakup email. Closing the loop, low pressure. |

### 2B. Cold email sequences by industry (MONEY_METHODS/COLD_OUTBOUND/)

| File | Path | Lines | Industries | Emails per sequence |
|------|------|-------|------------|-------------------|
| EMAIL_SEQUENCES_TIER1.md | `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES_TIER1.md` | 818 | Healthcare, Legal, Real Estate | 7 emails each, 2026 meta integrated |
| TIER1_COLD_EMAIL_SEQUENCES.md | `MONEY_METHODS/COLD_OUTBOUND/TIER1_COLD_EMAIL_SEQUENCES.md` | 537 | Healthcare, Legal, Real Estate | 4 emails each + LinkedIn templates + voice notes |
| LOCAL_BIZ_WEBSITE_SERVICE.md | `MONEY_METHODS/COLD_OUTBOUND/LOCAL_BIZ_WEBSITE_SERVICE.md` | 505 | All local biz | Full service playbook, $500-$3K packages |
| AUDIT_OUTPUT.md | `MONEY_METHODS/COLD_OUTBOUND/AUDIT_OUTPUT.md` | -- | Audit of cold outbound status | Assessment of what exists vs what's needed |

### 2C. Cold email sequences (CONTENT/email_sequences/cold/)

| File | Path | Industries | Notes |
|------|------|-----------|-------|
| COLD_EMAIL_SEQUENCES_3_INDUSTRIES.md | `CONTENT/email_sequences/cold/COLD_EMAIL_SEQUENCES_3_INDUSTRIES.md` | Healthcare, Legal, Fitness | 6 emails over 12 days each, 100-word limit, 6-question framework |
| INDUSTRY_SEQUENCES_5.md | `CONTENT/email_sequences/cold/INDUSTRY_SEQUENCES_5.md` | Dental, + 4 more | 4 emails per sequence, 5 industries total |

### 2D. Local biz demo cold email (MONEY_METHODS/LOCAL_BIZ/)

| File | Path | Purpose |
|------|------|---------|
| COLD_EMAIL_DEMO_TEMPLATE.md | `MONEY_METHODS/LOCAL_BIZ/COLD_EMAIL_DEMO_TEMPLATE.md` | 4 template variants (A: Direct demo, B: Problem-first, C: No website, D: Competitor comparison). Used with personalize_template.py |

### 2E. Government contract outreach (EMAIL/)

| File | Path | Purpose |
|------|------|---------|
| GOV_CONTRACT_COLD_EMAIL.md | `EMAIL/GOV_CONTRACT_COLD_EMAIL.md` | Templates for losing bidders + teaming partners. 3 A/B subject lines. |
| GOV_TENDER_OUTREACH_EMAILS.md | `EMAIL/GOV_TENDER_OUTREACH_EMAILS.md` | Outreach to small businesses about gov contract intel service ($47/mo) + proposal writing upsell ($500-$2K) |

### 2F. Ecom outreach (EMAIL/ecom_outreach/)

| File | Path | Purpose |
|------|------|---------|
| tech_stack_template.txt | `EMAIL/ecom_outreach/tech_stack_template.txt` | Targets Shopify stores by detected tech. Quick audit offer. |
| growth_offer_template.txt | `EMAIL/ecom_outreach/growth_offer_template.txt` | Targets fast-growing stores. "12 stores at your stage" social proof. |

### 2G. Newsletter / product email sequences (EMAIL/)

| File | Path | Purpose |
|------|------|---------|
| sequence_v1.md | `EMAIL/sequence_v1.md` | 5-email warmup sequence for 3 niches (AI Clarity Stack, Daily Anchor System, 3-Hour Physique). Product sales, not cold outreach. |
| offer_copy_v1.md | `EMAIL/offer_copy_v1.md` | Landing page sales copy for 3 products. Not cold email. |
| welcome_sequence.md | `EMAIL/sequences/welcome_sequence.md` | Welcome email sequence |
| launch_sequence.md | `EMAIL/sequences/launch_sequence.md` | Product launch sequence |
| reengagement_sequence.md | `EMAIL/sequences/reengagement_sequence.md` | Re-engagement sequence |

### 2H. Content posting cold email assets (AUTOMATIONS/content_posting/)

| File | Path | Rows | Purpose |
|------|------|------|---------|
| cold_email_sequences_ready.csv | `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv` | multi | CSV-formatted cold email sequences by industry. Ready for import into Instantly/Smartlead. |
| cold_email_subject_lines_100.csv | `AUTOMATIONS/content_posting/cold_email_subject_lines_100.csv` | 100+ | A/B test subject lines by industry and variant. Schema: id, industry, subject_line, email_stage, variant |

### 2I. Cold email writer prompt (OPS/)

| File | Path | Purpose |
|------|------|---------|
| cold_email_writer.md | `OPS/prompts/library/outreach/cold_email_writer.md` | System prompt for generating cold emails. Rules: under 100 words, research-based personalization, soft CTA. |

### 2J. Cold email subject line product (DIGITAL_PRODUCTS/)

| File | Path | Purpose |
|------|------|---------|
| PRODUCT_1_73_cold_email_subject_lines.md | `DIGITAL_PRODUCTS/micro_products/PRODUCT_1_73_cold_email_subject_lines.md` | Gumroad product: 73 tested subject lines. 42% avg open rate. Organized by industry. |

---

## 3. Tools: scrapers, scorers, senders, generators

### 3A. Lead scrapers

| Tool | Path | Purpose | Input | Output |
|------|------|---------|-------|--------|
| savvy_lead_scraper.py | `AUTOMATIONS/savvy_lead_scraper.py` | Quant-level 0-100 scoring scraper. Searches Google, visits websites, scores on SSL/mobile/speed/SEO/forms. | --city "City" --industry "type" --count N | AUTOMATIONS/leads/{industry}_{city}_leads.csv |
| nationwide_scraper.py | `AUTOMATIONS/nationwide_scraper.py` | 880 lines. Runs savvy_lead_scraper across 203 cities. Outputs MASTER_LEADS.csv. | --cities CSV --industries "list" --max-cities N | AUTOMATIONS/leads/MASTER_LEADS.csv + per-city CSVs |
| local_biz_website_scraper.py | `AUTOMATIONS/local_biz_website_scraper.py` | Simpler website-focused scraper. Audits existing URLs for score. | URL list | Score + issues |
| local_biz_pipeline.py | `AUTOMATIONS/local_biz_pipeline.py` | Full pipeline: scrape, analyze, generate personalized outreach. | --city --industry or URL list | prospects.csv + personalized emails |
| storeleads_ecom_scraper.py | `AUTOMATIONS/storeleads_ecom_scraper.py` | Ecom store lead scraper (Shopify stores). | Keywords | LEDGER/ECOM_LEADS.csv |
| sam_gov_scraper.py | `AUTOMATIONS/sam_gov_scraper.py` | SAM.gov opportunities API scraper. | Keywords, NAICS codes | leads/sam_gov_opportunities.csv |
| usaspending_scraper.py | `AUTOMATIONS/usaspending_scraper.py` | USAspending.gov awards scraper. | Keywords | leads/usaspending_*.csv |
| gov_tenders_scraper.py | `AUTOMATIONS/gov_tenders_scraper.py` | Government tenders scraper. | -- | leads/gov_tenders_active.csv |
| hexomatic_lead_gen.py | `AUTOMATIONS/hexomatic_lead_gen.py` | Hexomatic-powered lead gen. | -- | -- |
| fiverr_gig_scraper.py | `AUTOMATIONS/fiverr_gig_scraper.py` | Scrapes Fiverr gigs for competitive intel. | Keywords | -- |
| producthunt_scraper.py | `AUTOMATIONS/producthunt_scraper.py` | Product Hunt B2B lead scraper. | -- | leads/producthunt_b2b_leads.csv |
| linkedin_events_scraper.py | `AUTOMATIONS/linkedin_events_scraper.py` | LinkedIn event attendee scraper. | -- | leads/linkedin_events_leads.csv |
| g2_reviewer_scraper.py | `AUTOMATIONS/g2_reviewer_scraper.py` | G2 reviewer data scraper. | Product slug | leads/g2_reviewer_leads.csv |

### 3B. Lead scoring and processing

| Tool | Path | Purpose |
|------|------|---------|
| lead_scoring_criteria.md | `AUTOMATIONS/lead_scoring_criteria.md` | Scoring rubric documentation. 0-100 scale based on website quality signals. |
| cities_top200.csv | `AUTOMATIONS/cities_top200.csv` | Database of 203 US cities across 44 states with population data. Input for nationwide_scraper. |

### 3C. Outreach generators and senders

| Tool | Path | Purpose |
|------|------|---------|
| mass_outreach.py | `AUTOMATIONS/mass_outreach.py` | 732 lines. Reads scored leads, generates 3-step email sequences, outputs Instantly-format CSVs. |
| generate_cold_emails.py | `AUTOMATIONS/generate_cold_emails.py` | Generates personalized cold emails from lead CSVs. Outputs per-business .txt files + batch CSVs. |
| cold_email_2026.py | `AUTOMATIONS/cold_email_2026.py` | Cold email system with 2026 best practices. |
| email_sender.py | `AUTOMATIONS/email_sender.py` | Actual email sending script. Needs SMTP credentials to function. |
| voicemail_drop_system.py | `AUTOMATIONS/voicemail_drop_system.py` | Ringless voicemail drop. Integrates with Slybroadcast or similar. |
| personalize_template.py | `MONEY_METHODS/LOCAL_BIZ/personalize_template.py` | Takes a template HTML + lead data, generates personalized demo page with business name/phone/address. |

### 3D. Support scripts

| Tool | Path | Purpose |
|------|------|---------|
| run_lead_gen.sh | `AUTOMATIONS/run_lead_gen.sh` | Shell script: runs savvy_lead_scraper across 10 cities x 5 industries. |
| fix_placeholders.py | `MONEY_METHODS/LOCAL_BIZ/fix_placeholders.py` | Fixes placeholder text in generated templates. |

---

## 4. Generated outreach CSVs (AUTOMATIONS/outreach/)

### 4A. Per-lead-source email sequences (original pipeline output)

Generated by `mass_outreach.py` from early lead batches:

| File | Rows | Industry + City |
|------|------|-----------------|
| dental_austin_tx_leads_emails.csv | 141 | Dental, Austin TX |
| dental_austin_tx_leads_emails_step1.csv | 49 | Step 1 only |
| dental_austin_tx_leads_emails_step2.csv | 45 | Step 2 only |
| dental_austin_tx_leads_emails_step3.csv | 49 | Step 3 only |
| restaurant_austin_tx_leads_emails.csv | 141 | Restaurant, Austin TX |
| restaurant_austin_tx_leads_emails_step1-3.csv | 45-53 | Steps 1-3 |
| plumber_dallas_tx_leads_emails.csv | 103 | Plumber, Dallas TX |
| plumber_dallas_tx_leads_emails_step1-3.csv | 34-37 | Steps 1-3 |
| lawyer_houston_tx_leads_emails.csv | 67 | Lawyer, Houston TX |
| lawyer_houston_tx_leads_emails_step1-3.csv | 19-27 | Steps 1-3 |

### 4B. Master leads email sequences

| File | Rows | Notes |
|------|------|-------|
| MASTER_LEADS_emails.csv | 2,987 | All master leads with 3-step sequences |
| MASTER_LEADS_emails_step1.csv | 936 | Step 1 only, Instantly import format |
| MASTER_LEADS_emails_step2.csv | 958 | Step 2 only |
| MASTER_LEADS_emails_step3.csv | 1,095 | Step 3 only |

### 4C. Batch cold email runs (timestamped)

Generated by `generate_cold_emails.py`:

| File | Rows | Source |
|------|------|--------|
| cold_emails_20260212_0219.csv | 21,093 | Full email bodies, all leads |
| cold_emails_20260212_0223.csv | 26,405 | Second run, more leads |
| cold_emails_batch_Austin_Miami_Phoenix_20260212_0222.csv | 5,371 | Austin + Miami + Phoenix batch |
| instantly_step1/2/3_cold_emails_*.csv | 76-304 each | Instantly-format imports per step |
| quick_send_*.csv | 901-3,671 | Quick-send format CSVs |
| cold_emails_txt_Austin_Miami_Phoenix/ | 100+ files | Individual .txt files per business |

---

## 5. Playbooks and guides

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| COLD_EMAIL_LAUNCH_CHECKLIST.md | `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md` | 748 | Phase 0-5 launch guide. Domain purchase, warmup, Instantly setup, sequences, tracking. NOT_STARTED. |
| NATIONWIDE_LEAD_GEN_SYSTEM.md | `MONEY_METHODS/LOCAL_BIZ/NATIONWIDE_LEAD_GEN_SYSTEM.md` | 488 | Full system docs: pricing, competitive analysis, scaling to 100 clients. |
| LOCAL_BIZ_WEBSITE_SERVICE.md | `MONEY_METHODS/COLD_OUTBOUND/LOCAL_BIZ_WEBSITE_SERVICE.md` | 505 | Method playbook: scraper to outreach to close. Packages $500-$3K. |
| AI_CALL_OUTREACH.md | `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md` | -- | Bland.ai integration, TCPA compliance, 3 call scripts. |
| AGENCY_WEBSITE.md | `MONEY_METHODS/LOCAL_BIZ/AGENCY_WEBSITE.md` | -- | Spec for credibility website. 8 name options + wireframe. |
| MOTION_UPSELL.md | `MONEY_METHODS/LOCAL_BIZ/MOTION_UPSELL.md` | -- | Upsell motion-animated sites ($500/$1,500/$3,000 tiers). |
| MOTION_UPSELL_PRICING.md | `MONEY_METHODS/LOCAL_BIZ/MOTION_UPSELL_PRICING.md` | 42K | 10 industry prompts, AI tool comparison, competitive analysis, objection handling. |
| AI_WEB_DESIGN_TOOLS.md | `MONEY_METHODS/LOCAL_BIZ/AI_WEB_DESIGN_TOOLS.md` | -- | Comparison of 7 AI web design tools (Lovable, Bolt, v0, Cursor, Framer, Webflow, Wix). |
| AUDIT_OUTPUT.md | `MONEY_METHODS/COLD_OUTBOUND/AUDIT_OUTPUT.md` | -- | Status assessment of entire cold outbound pipeline. |
| Email tool comparison | `LEDGER/OUTBOUND_OPPORTUNITIES/2026-02-01_email_tool_comparison_instantly_smartlead_lemlist.md` | -- | Instantly vs Smartlead vs Lemlist comparison. Conclusion: Instantly for most, Smartlead for deliverability. |
| Lead sources research | `LEDGER/OUTBOUND_OPPORTUNITIES/2026-01-24_lead-sources_databases-enrichment.md` | -- | Lead source databases and enrichment tools. |
| Lead scraping research | `LEDGER/OUTBOUND_OPPORTUNITIES/2026-01-24_lead_sources_scraping_enrichment.md` | -- | Scraping and enrichment research. |
| QA cold email content | `OPS/CONTENT_QA_QUEUE/QA_2026-02-02_cold-email-150x-roi-the-exact-system.md` | -- | Social content about cold email ROI, pending review. |
| Personalized outreach sample | `AUTOMATIONS/output/personalized_outreach_10.md` | -- | 10 Austin TX leads with fully personalized cold emails. |

---

## 6. Website templates for demos (MONEY_METHODS/LOCAL_BIZ/templates/)

These are the actual HTML files sent as "I already built this for you" demos:

| Template | Path | Industry |
|----------|------|----------|
| dental.html | `MONEY_METHODS/LOCAL_BIZ/templates/dental.html` | Dental practices |
| restaurant.html | `MONEY_METHODS/LOCAL_BIZ/templates/restaurant.html` | Restaurants |
| fitness.html | `MONEY_METHODS/LOCAL_BIZ/templates/fitness.html` | Fitness/gyms |
| legal.html | `MONEY_METHODS/LOCAL_BIZ/templates/legal.html` | Law firms |
| plumber.html | `MONEY_METHODS/LOCAL_BIZ/templates/plumber.html` | Plumbers |
| realtor.html | `MONEY_METHODS/LOCAL_BIZ/templates/realtor.html` | Real estate |

Motion-animated versions (upsell):

| Template | Path | Industry |
|----------|------|----------|
| dental_motion.html | `MONEY_METHODS/LOCAL_BIZ/motion_templates/dental_motion.html` | Dental (animated) |
| restaurant_motion.html | `MONEY_METHODS/LOCAL_BIZ/motion_templates/restaurant_motion.html` | Restaurant (animated) |
| realtor_motion.html | `MONEY_METHODS/LOCAL_BIZ/motion_templates/realtor_motion.html` | Realtor (animated) |

Generated demo landing pages (AUTOMATIONS/output/landing_pages/):
9 sample pages: joes-plumbing, smith-family-dentistry, mikes-hvac, bellas-salon, johnson-associates-law-firm, elite-fitness-center, perfect-lawn-landscaping, tonys-italian-restaurant, quick-auto-repair, plus index.html.

---

## 7. Pipeline status and funnel

```
SCRAPE (savvy_lead_scraper / nationwide_scraper)
  |
  v
RAW LEADS (AUTOMATIONS/leads/{industry}_{city}_leads.csv)
  |
  v
CONSOLIDATE (nationwide_scraper --> MASTER_LEADS.csv, 1,035 rows)
  |
  v
SCORE + DEMO (local_biz_pipeline.py --> SCORED_LEADS.csv, HOT_LEADS.csv)
  |
  v
GENERATE EMAILS (mass_outreach.py / generate_cold_emails.py)
  |
  v
OUTREACH CSVs (AUTOMATIONS/outreach/*.csv, ~70K rows generated)
  |
  v
IMPORT TO INSTANTLY/SMARTLEAD  <--- BLOCKED (no account yet)
  |
  v
SEND  <--- BLOCKED (no warmed domains, no warmed inboxes)
  |
  v
TRACK (PIPELINE_TRACKER.csv, 87 leads with status)
  |
  v
CLOSE  <--- $0 revenue from outreach so far
```

**Current bottleneck:** No sending infrastructure. Need:
1. Buy 3 cold email domains ($30-45)
2. Set up Instantly or Smartlead account
3. Warm inboxes for 2-4 weeks
4. Then import the already-generated CSVs and start sending

See `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md` for the full Phase 0-5 plan.

---

## 8. Run the full pipeline end-to-end

### Step 1: Scrape leads for a new city

```bash
python3 AUTOMATIONS/savvy_lead_scraper.py --city "Austin TX" --industry dental --count 50
```

Output: `AUTOMATIONS/leads/dental_austin_tx_leads.csv`

### Step 2: Run nationwide (multiple cities)

```bash
python3 AUTOMATIONS/nationwide_scraper.py \
  --cities AUTOMATIONS/cities_top200.csv \
  --industries "dentist,plumber,lawyer,restaurant" \
  --max-cities 10
```

Output: Per-city CSVs + `AUTOMATIONS/leads/MASTER_LEADS.csv`

### Step 3: Score and generate demos

```bash
python3 AUTOMATIONS/local_biz_pipeline.py \
  --leads AUTOMATIONS/leads/MASTER_LEADS.csv \
  --min-score 40
```

Output: `AUTOMATIONS/leads/SCORED_LEADS.csv`, `HOT_LEADS.csv`

### Step 4: Generate cold emails

```bash
python3 AUTOMATIONS/mass_outreach.py \
  --leads AUTOMATIONS/leads/MASTER_LEADS.csv \
  --min-score 60 \
  --template-dir MONEY_METHODS/LOCAL_BIZ/templates/
```

Output: `AUTOMATIONS/outreach/MASTER_LEADS_emails.csv` + step1/2/3 CSVs

### Step 5: Generate personalized per-business emails

```bash
python3 AUTOMATIONS/generate_cold_emails.py \
  --leads AUTOMATIONS/leads/MASTER_LEADS.csv \
  --cities "Austin,Miami,Phoenix"
```

Output: `AUTOMATIONS/outreach/cold_emails_batch_*.csv` + individual .txt files

### Step 6: Import to Instantly (MANUAL - needs account)

1. Go to instantly.ai, create account
2. Import `AUTOMATIONS/outreach/instantly_step1_*.csv` as Campaign Step 1
3. Import step2 and step3 CSVs
4. Set delays (Day 0, Day 3, Day 7)
5. Start campaign

### Step 7: Track responses

Update `AUTOMATIONS/outreach/PIPELINE_TRACKER.csv` with status changes (SENT, REPLIED, MEETING, CLOSED, LOST).

### One-liner for steps 1-5:

```bash
# Scrape 5 cities, generate emails, output ready-to-send CSVs
python3 AUTOMATIONS/nationwide_scraper.py --cities AUTOMATIONS/cities_top200.csv --industries "dentist,plumber,lawyer,restaurant" --max-cities 5 && \
python3 AUTOMATIONS/mass_outreach.py --leads AUTOMATIONS/leads/MASTER_LEADS.csv --min-score 50 --template-dir MONEY_METHODS/LOCAL_BIZ/templates/
```

---

## 9. Duplicate and staleness audit

### 9A. Duplicate lead CSVs (CONFIRMED)

**dental_austin_tx_leads.csv vs dentist_*_leads.csv naming inconsistency:**
- Files named `dental_austin_tx_leads.csv` and `dental_dallas_tx_leads.csv` use "dental" prefix
- Files named `dentist_houston_leads.csv`, `dentist_miami_leads.csv` etc. use "dentist" prefix
- Same schema, same scraper, different naming conventions from different runs
- Both sets are in MASTER_LEADS.csv, so duplicates may exist there
- **Action needed:** Deduplicate MASTER_LEADS.csv by website URL

**lawyer_houston_tx_leads.csv vs lawyer_houston_leads.csv:**
- `lawyer_houston_tx_leads.csv` = 10 rows (older run, "TX" suffix format)
- `lawyer_houston_leads.csv` = 21 rows (newer run, no "TX" suffix)
- Different scrape times, likely overlapping businesses
- **Action needed:** Merge and deduplicate by website URL

**plumber_dallas_tx_leads.csv vs plumber_dallas_leads.csv:**
- Same situation: 10 rows vs 18 rows
- **Action needed:** Same merge + dedup

### 9B. Duplicate email template content

**EMAIL_SEQUENCES_TIER1.md vs TIER1_COLD_EMAIL_SEQUENCES.md:**
- Both in `MONEY_METHODS/COLD_OUTBOUND/`
- Both cover Healthcare, Legal, Real Estate
- EMAIL_SEQUENCES_TIER1.md = 818 lines, 7 emails/sequence, more detailed
- TIER1_COLD_EMAIL_SEQUENCES.md = 537 lines, 4 emails/sequence, adds LinkedIn templates
- **Overlap:** ~60% content overlap. The 818-line version is more complete.
- **Recommendation:** Merge unique content from TIER1 into EMAIL_SEQUENCES, archive TIER1.

**COLD_EMAIL_SEQUENCES_3_INDUSTRIES.md vs EMAIL_SEQUENCES_TIER1.md:**
- CONTENT/email_sequences/cold/ version covers Healthcare, Legal, Fitness
- MONEY_METHODS/COLD_OUTBOUND/ version covers Healthcare, Legal, Real Estate
- Healthcare and Legal overlap. Fitness vs Real Estate differ.
- **Recommendation:** Keep both. Different industries in each. Reference both from this index.

**INDUSTRY_SEQUENCES_5.md vs the above:**
- 5 industries, 4 emails each
- Overlaps with dental sequence in other files
- **Recommendation:** This is the broadest. Keep as the "quick start" set.

### 9C. Stale / empty files

| File | Issue | Recommendation |
|------|-------|---------------|
| LEDGER/leads.csv | Empty (header only) | Not used. Landing page captures go here but no landing page is live. Keep as placeholder. |
| LEDGER/ECOM_LEADS.csv | Empty (header only) | Schema defined but no ecom leads scraped yet. Keep as placeholder. |
| LEDGER/FREELANCE_PIPELINE.csv | Empty (header only) | No freelance orders tracked. Keep as placeholder. |
| AUTOMATIONS/sample_prospects.csv | Fake data | Test file with fictional businesses. Do not use for outreach. |
| AUTOMATIONS/output/pipeline_*/ | Old test runs | Early pipeline test outputs. Can be deleted to reduce clutter. |
| AUTOMATIONS/AUTOMATIONS/ (nested) | Buggy path | `AUTOMATIONS/AUTOMATIONS/output/pipeline_run/` is a double-nested directory, likely from a script bug. Clean up. |

### 9D. Data quality issues in MASTER_LEADS.csv

- Many entries are directories/listings (e.g., "Plumbers in Houston, Texas" from meetaplumber.com) rather than actual businesses
- website_score of 10 means "unreachable or listing site" -- these are not real leads
- Only entries with website_score 40+ are actionable leads
- Many entries lack email_if_found (the field is mostly empty)
- **Recommendation:** Filter MASTER_LEADS to score >= 40 before any outreach run

### 9E. Data quality issues in PIPELINE_TRACKER.csv

- All 87 leads have template_used = "plumbing" regardless of category (dentist, restaurant, lawyer)
- Several emails are generic (user@domain.com, forwarding@pro.houzz.com, customer.support@ferguson.com)
- Some entries are news articles or job postings, not actual businesses
- **Recommendation:** Re-run pipeline with proper template matching and email validation

---

## 10. Cross-reference map

| If you need... | Look at... |
|---------------|-----------|
| All lead data in one place | `AUTOMATIONS/leads/MASTER_LEADS.csv` (filter score >= 40) |
| Best leads with demos ready | `AUTOMATIONS/leads/HOT_LEADS.csv` (5 leads) |
| Pipeline CRM status | `AUTOMATIONS/outreach/PIPELINE_TRACKER.csv` (87 leads) |
| High-value B2B leads | `LEDGER/OUTREACH_PIPELINE.csv` (10+ manually curated) |
| Ready-to-import email CSVs | `AUTOMATIONS/outreach/instantly_step*_cold_emails_*.csv` |
| Local biz cold email template | `AUTOMATIONS/email_templates/local_biz_cold.txt` |
| Industry-specific sequences | `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES_TIER1.md` |
| Demo template HTMLs | `MONEY_METHODS/LOCAL_BIZ/templates/*.html` |
| Full launch checklist | `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md` |
| Nationwide scaling plan | `MONEY_METHODS/LOCAL_BIZ/NATIONWIDE_LEAD_GEN_SYSTEM.md` |
| Tool comparison (Instantly etc) | `LEDGER/OUTBOUND_OPPORTUNITIES/2026-02-01_email_tool_comparison_*.md` |
| Gov contract leads | `AUTOMATIONS/leads/sam_gov_opportunities.csv` + `gov_tenders_active.csv` + `usaspending_*.csv` |
| Gov outreach emails | `EMAIL/GOV_CONTRACT_COLD_EMAIL.md` + `EMAIL/GOV_TENDER_OUTREACH_EMAILS.md` |
| Ecom store outreach | `EMAIL/ecom_outreach/*.txt` + `LEDGER/ECOM_LEADS.csv` (empty) |
| Subject line A/B variants | `AUTOMATIONS/content_posting/cold_email_subject_lines_100.csv` |
| AI call outreach | `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md` |
| Motion site upsell | `MONEY_METHODS/LOCAL_BIZ/MOTION_UPSELL.md` |
| Cold email writer prompt | `OPS/prompts/library/outreach/cold_email_writer.md` |
| Scoring criteria docs | `AUTOMATIONS/lead_scoring_criteria.md` |


    ---

    ## Pending Enhancement (ALPHA1219, Score: 26)

    **Source:** 2026-02-13 | **URL:** @pipelineabuser
    **Added:** 2026-02-18T06:49:18-05:00

    Send 15,000 cold emails per month for $49/month

As a direct Microsoft partner, we offer the best deliverability at the best price.

Fully done-for-you: we create your inboxes, upload them to your sequencer, and configure sending/warmup settings.


http://
deliveron.org



---

## Pending Enhancement (ALPHA1860, Score: 26)

**Source:** 2026-02-13 | **URL:** @codyschneiderxx
**Added:** 2026-02-18T07:12:19-05:00

if you're a startup founder just read this so I can sleep peacefully tonight

most companies can get to $1M ARR with only two channels

the channels you should pick from are

- paid ads 
- cold email
- cold DMs
- yt influencer marketing + affiliate

the channels you should not



---

## Pending Enhancement (ALPHA6604, Score: 20)

**Source:** r/socialmedia (https://reddit.com/r/socialmedia/comments/1r6h5dw/are_commissionbased_lead_gen_partnerships/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

Are Commission-Based Lead Gen Partnerships Sustainable for SMM Agencies?. I run a social media management agency focused primarily on organic growth for service-based businesses.

I’ve been exploring a commission-only lead generation partnership model instead of hiring in-h



---

## Pending Enhancement (ALPHA8346, Score: 23)

**Source:** @seanb2b (high-signal-accounts) | **URL:** https://x.com/seanb2b/status/2023429186308776227
**Added:** 2026-02-18T08:54:20-05:00

Marcin Joins CCG 
Week 1 of him sending cold emails:
→ 5 calls booked
→ 100% show rate

Get the system inside CCG ($97/mo)  


http://
closingclientsgroup.com



---

## Pending Enhancement (ALPHA12309, Score: 32)

**Source:** r/SaaS (https://reddit.com/r/SaaS/comments/1rck8ud/how_i_hit_27k_mrr_by_ignoring_standard_startup/) | **URL:** 
**Added:** 2026-02-24T06:00:01-05:00

How I hit $27k MRR by ignoring standard startup advice with 5 channels. If you are burning cash on ads and praying for a return, or sending 100 cold emails a day just to hear crickets, stop what you are doing.

I just hit $27k MRR with [my tool](https://tryrebelgrowth.com



---

## Pending Enhancement (ALPHA13716, Score: 24)

**Source:** r/Affiliatemarketing (https://reddit.com/r/Affiliatemarketing/comments/1rgp4dm/i_made_800_in_affiliate_commissions_from_a/) | **URL:** 
**Added:** 2026-02-28T06:00:01-05:00

I Made $800+ in Affiliate Commissions From a Business I Already Sold. I’m *not* here to sell you anything.

No course.  
No funnel.  
No DM me.

Just sharing something that surprised me.

A while back I was selling AI automation bots for **$147 each**.

Nothing crazy. N



---

## Pending Enhancement (ALPHA16381, Score: 23)

**Source:** ProductHunt | **URL:** https://www.producthunt.com/products/chatgpt
**Added:** 2026-03-07T00:41:17-05:00

ProductHunt launch: Build and update spreadsheets with ChatGPT in real time



---

## Pending Enhancement (ALPHA16404, Score: 50)

**Source:** IndieHackers | **URL:** https://www.indiehackers.com/product/storyclips
**Added:** 2026-03-07T00:41:17-05:00

Create viral faceless videos on autopilot. $2.5k/mo 2026. Faceless video creation is a validated $2k+ MRR niche with low CAC from creator communities.



---

## Pending Enhancement (ALPHA16410, Score: 52)

**Source:** IndieHackers | **URL:** https://www.indiehackers.com/product/kintsu-ai
**Added:** 2026-03-07T00:41:17-05:00

Vibe code your existing WordPress site. $50k/mo Feb 2026. AI code generation applied to the world's largest CMS. 40% of the internet is WordPress.



---

## Pending Enhancement (ALPHA16413, Score: 49)

**Source:** IndieHackers | **URL:** https://optiway.io/
**Added:** 2026-03-07T00:41:17-05:00

Route planning SaaS hitting $30k MRR with SEO-driven acquisition in a niche B2B category. No VC funding mentioned. Solo/small team.



---

## Pending Enhancement (ALPHA16416, Score: 51)

**Source:** IndieHackers | **URL:** https://www.indiehackers.com/product/contagent
**Added:** 2026-03-07T00:41:17-05:00

Grow your X audience on autopilot. $10k/mo Feb 2026. X/Twitter growth automation tool. Platform risk but high current demand.



---

## Pending Enhancement (ALPHA16421, Score: 36)

**Source:** IndieHackers | **URL:** https://wifimouse.necta.us
**Added:** 2026-03-07T00:41:17-05:00

Utility app with $6k/mo revenue. Phone as wireless mouse/keyboard. One-time purchase + premium upgrade model. Low churn by design.



---

## Pending Enhancement (ALPHA16443, Score: 41)

**Source:** IndieHackers | **URL:** https://www.indiehackers.com/product/image-to-photo
**Added:** 2026-03-07T00:41:17-05:00

Image-to-realistic-photo AI tool. $20k/mo Feb 2026. Likely pure SEO play targeting image transformation keywords. Chinese domain (.cn variant) suggests global SEO arbitrage.



---

## Pending Enhancement (ALPHA16444, Score: 30)

**Source:** IndieHackers | **URL:** https://www.indiehackers.com/product/hullo-ai-matchmaking
**Added:** 2026-03-07T00:41:17-05:00

AI-powered matchmaking for more intentional connections. $4.5k/mo March 2026. Premium dating with AI matchmaking rather than algorithmic swiping. High willingness to pay in dating niche.



---

## Pending Enhancement (ALPHA16449, Score: 42)

**Source:** IndieHackers - Interview | **URL:** https://www.indiehackers.com/post/turning-my-popular-open-source-tool-into-a-1-200-mo-product-VuSVTzKTfXPjRYA44Ezn
**Added:** 2026-03-07T00:41:17-05:00

Built open-source Twitch music display tool. Added paid tier after 1000+ GitHub stars. $1.2k/mo from converting OSS users to paid. Key: open source as distribution then monetize the power users.



---

## Pending Enhancement (ALPHA16447, Score: 23)

**Source:** @Argona0x (high-signal-accounts) | **URL:** https://x.com/Argona0x/status/2029996108487745909
**Added:** 2026-03-07T03:02:27-05:00

he told me to never share the rest

i'm sharing it anyway

the 2 pages were just the intro

47 more just landed in my inbox

full quant fund playbook

the models, the formulas, the filters

everything that made him $400K/year

my bot is already running on it

don’t you dare miss



---

## Pending Enhancement (ALPHA17073, Score: 22)

**Source:** HackerNews | **URL:** https://news.ycombinator.com/item?id=47278426
**Added:** 2026-03-07T08:10:08-05:00

Tech employment crisis worse than 2008/2020. 929pts 609 comments. MASSIVE market of laid-off devs needing income. Perfect cold outreach target: "build your own SaaS instead of job hunting" angle. Sell toolkits/courses to displaced tech workers.



---

## Pending Enhancement (TW_INTEL_20260307_001, Score: 24)

**Source:** twitter_accounts_scraper | **URL:** https://twitter.com/dimitarangg
**Added:** 2026-03-07T10:44:04-05:00

@dimitarangg: 59 B2B calls booked in 16 days - leaked entire cold outreach system. 666 engagement.



---

## Pending Enhancement (ALPHA19233, Score: 23)

**Source:** Reddit/r/coldemail | **URL:** https://www.reddit.com/r/coldemail
**Added:** 2026-03-09T07:47:13-04:00

Cold email system from scratch: exact framework for building a cold email machine today. Community thread with real practitioners sharing current working systems. High signal for current deliverability tactics.



---

## Pending Enhancement (ALPHA19234, Score: 20)

**Source:** Reddit/r/growthhacking | **URL:** https://www.reddit.com/r/growthhacking
**Added:** 2026-03-09T07:47:13-04:00

How startups land top-tier publications (Business Insider, Yahoo Finance). Community thread reveals PR strategies. Key: HARO responses, PR Newswire alternatives, cold pitching journalists directly vs wire services.

