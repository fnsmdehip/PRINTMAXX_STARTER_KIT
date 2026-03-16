# OUTBOUND SEND QUEUE
**Last updated:** 2026-03-15
**Status:** READY TO SEND — 20 personalized + 8 category sequences loaded

---

## HOW TO USE THIS

1. Start at TOP of Priority Queue (P0 first)
2. Open the personalized email file for that lead
3. Copy the body into your email client
4. Replace any [bracketed] placeholders
5. Send from a warmed domain (NOT your main domain)
6. Mark sent date in the "Status" column
7. Follow sequence schedule: +3 days for Email 2, +7 days for Email 3

**Domain needed:** Use a burner domain for cold outbound — main domain never touches cold email. Set up SPF/DKIM/DMARC before sending.

**From name:** Use a real first name, e.g. "Alex from [brand]" — not a company name

---

## PRIORITY QUEUE — TOP 20 PERSONALIZED

### P0 — HIGH-VALUE TARGETS (Send first — best revenue potential)

| # | Company | Contact | Email | Category | Price Point | File | Status |
|---|---------|---------|-------|----------|-------------|------|--------|
| 1 | Legacy Partners | M. Nicholson | mnicholson@legacypartners.com | Real Estate | $750 | personalized/legacy_partners_email1.txt | UNSENT |
| 2 | G & H Dental Arts, Inc | Brian | brian@gandhdental.com | Dentist | $750 | personalized/g_and_h_dental_arts_email1.txt | UNSENT |
| 3 | é by José Andrés | Concierge | concierge@cosmopolitanlasvegas.com | Fine Dining | $750 | personalized/e_by_jose_andres_email1.txt | UNSENT |
| 4 | Polk County Animal Hospital | — | info@polkcountyanimalhospital.com | Veterinarian | $750 | personalized/polk_county_animal_hospital_email1.txt | UNSENT |
| 5 | ChiroConcepts | — | info@chiroconcepts.net | Chiropractor | $1,000 | personalized/chiroconcepts_mckinney_email1.txt | UNSENT |
| 6 | Zora Urieff / Renovation Realty | Zora | zora@renovationrealty.com | Real Estate | $750 | personalized/zora_urieff_renovation_realty_email1.txt | UNSENT |
| 7 | Mercy Family Medicine | Denise Maier | denise.maier@mercyic.org | Doctor | $1,000 | personalized/mercy_family_medicine_west_liberty_email1.txt | UNSENT |
| 8 | All American Septic | Jordan | jordan@aasepticpro.com | Plumbing/Septic | $500 | personalized/all_american_septic_bryan_email1.txt | UNSENT |
| 9 | Nail Elite | — | info@naileliteofsouthlake.com | Nail Salon | $500 | personalized/nail_elite_southlake_email1.txt | UNSENT |
| 10 | Ironman Plumbing | — | ironman_plumbing@yahoo.com | Plumbing | $500 | personalized/ironman_plumbing_houston_email1.txt | UNSENT |

### P1 — STRONG TARGETS (Send day 2-3)

| # | Company | Contact | Email | Category | Price Point | File | Status |
|---|---------|---------|-------|----------|-------------|------|--------|
| 11 | Reflections Hair Design & Spa | — | maish@destinationsfl.com | Hair Salon | $500 | personalized/reflections_hair_design_san_jose_email1.txt | UNSENT |
| 12 | Dick Robinson Real Estate | — | rrobin@pe.net | Real Estate | $750 | personalized/dick_robinson_real_estate_email1.txt | UNSENT |
| 13 | A.W. Baghal D.D.S. | Dr. Baghal | drbaghal1@optonline.net | Dentist | $750 | personalized/aw_baghal_dds_email1.txt | UNSENT |
| 14 | Advanced Health Care | — | ahl@ah.com | Chiropractor | $1,000 | personalized/advanced_health_care_peekskill_email1.txt | UNSENT |
| 15 | New Image Salon | Renae | renae@newimageint.com | Hair Salon | $500 | personalized/new_image_salon_roseau_email1.txt | UNSENT |
| 16 | Primos' Restaurant | Ahmad | ahmadz@primos.com | Restaurant | $750 | personalized/primos_restaurant_wimauma_email1.txt | UNSENT |

### P2 — GOOD TARGETS (Send day 4-5)

| # | Company | Contact | Email | Category | Price Point | File | Status |
|---|---------|---------|-------|----------|-------------|------|--------|
| 17 | Mio Dental Center | — | tootlet@m33access.com | Dentist | $750 | personalized/mio_dental_center_email1.txt | UNSENT |
| 18 | Glenwood Family Dentistry | — | info@bbbnebraska.org | Dentist | $750 | personalized/glenwood_family_dentistry_email1.txt | UNSENT |
| 19 | Smith Chiropractic Health Center | — | fordoni2@ameritrade.com | Chiropractor | $1,000 | personalized/smith_chiropractic_jasper_email1.txt | UNSENT |
| 20 | 21st Century Surveying | Jerry | jerryburns@farmerstel.com | Real Estate/Survey | $750 | personalized/21st_century_surveying_email1.txt | UNSENT |

---

## CATEGORY SEQUENCE LIBRARY

Use these for bulk outreach after personalized batch:

| Sequence | File | Price | Best Market | Volume Potential |
|----------|------|-------|-------------|-----------------|
| Dentist | email_sequences/dentist_sequence.md | $750 | Any US city | 72K+ leads |
| Real Estate Agent | email_sequences/real_estate_sequence.md | $750 | Any US city | 233K+ leads |
| Restaurant | email_sequences/restaurant_sequence.md | $750 | High-density metros | 57K+ leads |
| Lawyer | email_sequences/lawyer_sequence.md | $1,250 | Major cities | 70K+ leads |
| Plumber / Home Services | email_sequences/plumber_home_services_sequence.md | $500 | Any US city | 28K+ leads |
| Auto Repair | email_sequences/auto_repair_sequence.md | $750 | Suburban markets | 112K+ leads |
| Beauty Salon | email_sequences/beauty_salon_sequence.md | $500 | Any US city | 170K+ leads |
| Chiropractor / Doctor | email_sequences/chiropractor_doctor_sequence.md | $1,000 | Any US city | 98K+ leads |
| Veterinarian | email_sequences/veterinarian_sequence.md | $750 | Suburban markets | 30K+ leads |

---

## BULK SEND PLAN (after personalized batch converts)

**Week 1:** Send 20 personalized emails above. Target 1-3 replies.

**Week 2:** Pull 50 dentist leads from AUTOMATIONS/leads/bulk/US_LEADS_DENTIST.csv with emails. Send Email 1 of dentist_sequence.md. Use mail merge to swap [Practice Name] and [City].

**Week 3:** Pull 50 real estate leads. Send real_estate_sequence.md Email 1.

**Week 4:** Follow up Weeks 1-2 with Email 2 versions.

**Target:** 200 sends/week at 3-5% reply rate = 6-10 conversations/week. Close 10-20% of conversations = 1-2 clients/week at $500-$1,250 each = $500-$2,500/week in new revenue.

---

## PERSONALIZATION FORMULA (for bulk)

1. **Open** — name the specific problem you found on their site/listing (broken URL, no booking, no mobile view)
2. **Quantify** — how many customers/patients/clients this costs them per month
3. **Demo** — link to the most relevant demo URL
4. **Social proof** — one specific case study with real numbers
5. **Offer** — price + timeline + refund guarantee
6. **Close** — single question, not "let me know" garbage

**Fastest personalization trick:** Look up their Google Business listing before sending. Note: star rating, review count, listed website, and whether the website actually loads on mobile. 5-minute research. Quadruples reply rate.

---

## REPLY HANDLING

| Reply type | Response |
|------------|----------|
| "Interested, tell me more" | Send demo link + schedule a 15-min call: "here's my calendar — pick a time" |
| "How much?" | "$750 setup, yours live in 48 hours. 30-day refund if you're not happy." |
| "Not right now" | "No worries — ok if I follow up in 60 days when you might be revisiting the site?" |
| "Not interested" | "Appreciate the reply. If anything changes, you have my email." (DON'T pitch again) |
| No reply after E3 | Archive. Re-engage in 60 days with a different angle. |
| Negative/angry reply | Apologize and remove. Don't argue. |

---

## COMPLIANCE NOTES

- Include one-click unsubscribe in every email (required by CAN-SPAM)
- From domain must be separate from main domain
- Don't send more than 50 cold emails/day per inbox until warmed (2-4 weeks warmup)
- FTC: No income guarantees. "Typically see" and "most clients see" are safer than "you will get"
- GDPR note: if sending to EU businesses, need legitimate interest basis — stick to US leads for now

---

## SEQUENCE SCHEDULE REFERENCE

| Email | Send When | Goal |
|-------|-----------|------|
| Email 1 | Day 1 | Get them to click the demo |
| Email 2 | Day 4 (if no reply) | Overcome inertia with case study |
| Email 3 | Day 7-9 (if no reply) | Scarcity + final CTA |
| Archive | Day 10+ (if no reply) | Move to next batch |
