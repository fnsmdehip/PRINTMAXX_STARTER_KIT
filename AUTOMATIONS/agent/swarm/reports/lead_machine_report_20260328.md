# Lead Machine Report — 2026-03-28 20:36
**Agent:** lead_machine | **Cycle:** 20260328
**Status:** COMPLETE
**Next run:** +3 hours (~23:36)

---

## Summary

| Metric | Value |
|--------|-------|
| New leads generated | 10 |
| Email-contactable leads | 8 |
| Phone-only leads | 1 |
| Leads needing phone lookup | 1 |
| Average composite score | 7.9/10 |
| Top lead score | 9.5/10 |
| Outreach drafts created | 10 |
| Emails ready to send | 8 |

---

## Top 5 Leads (Priority Order)

### 1. Dentists of Houston — Score: 9.5/10
- **Email:** mike.warwick@pdq.net (direct owner)
- **Pain:** NO SSL in 2026 (Chrome shows "Not Secure" before page loads), copyright 1999, not mobile
- **Why it's the best lead:** Dental = $800-2000/yr patient LTV. Owner email confirmed. The SSL issue is catastrophic — every patient on Chrome sees a warning before the practice name. Undeniable pain point, direct contact, high-ticket vertical.
- **Draft:** `outreach_drafts/20260328/01_dentists_of_houston.md`

### 2. Professional Plumbers Denver — Score: 8.5/10
- **Email:** info@professional-plumbers-denver.com
- **Pain:** 9.6 second load time (10x slower than Google's 1s threshold)
- **Why it's strong:** Load time is a specific, measurable, verifiable claim. They cannot argue with it. Denver plumbing = emergency searches = mobile-first = load speed is the most expensive problem to have.
- **Draft:** `outreach_drafts/20260328/02_professional_plumbers_denver.md`

### 3. Villalobos Law Chicago — Score: 8.0/10
- **Email:** mvillalobos@villaloboslaw.com (direct attorney)
- **Pain:** NOT mobile, no contact form, defense law = 2am emergency searches
- **Why it's strong:** Direct attorney email. Defense clients search at peak urgency (arrests happen at night). Missing the mobile+after-hours capture = losing the highest-need clients. Case values $5K-$50K+.
- **Draft:** `outreach_drafts/20260328/09_villalobos_law_chicago.md`

### 4. Metro Dental Atlanta — Score: 8.0/10
- **Email:** metrohenson@yahoo.com (likely owner direct)
- **Pain:** NOT mobile, no contact form, Yahoo email = small practice = owner reads their own email
- **Why it's strong:** Yahoo address + dental = personal decision-maker, high-ticket vertical. No mobile = broken patient experience on every smartphone search.
- **Draft:** `outreach_drafts/20260328/06_metro_dental_atlanta.md`

### 5. Emerald Plumbing and Heating — Score: 7.75/10
- **Contact:** Phone (no email found) — need Google Maps/Yelp lookup
- **Pain:** GoDaddy subdomain (emeraldplumbingandheating.godaddysites.com = no owned domain)
- **Why it's good:** Spring = peak plumbing+HVAC season. GoDaddy subdomain is a specific, embarrassing pain point owners respond to.
- **Draft:** `outreach_drafts/20260328/03_emerald_plumbing_heating.md`

---

## All 10 Leads

| Rank | Name | City | Email | Score | Category | Status |
|------|------|------|-------|-------|----------|--------|
| 1 | Dentists of Houston | Houston TX | mike.warwick@pdq.net | 9.5 | Dentist | DRAFT_READY |
| 2 | Professional Plumbers Denver | Denver CO | info@professional-plumbers-denver.com | 8.5 | Plumbing | DRAFT_READY |
| 3 | Villalobos Law Chicago | Chicago IL | mvillalobos@villaloboslaw.com | 8.0 | Law | DRAFT_READY |
| 4 | Metro Dental Atlanta | Atlanta GA | metrohenson@yahoo.com | 8.0 | Dentist | DRAFT_READY |
| 5 | Emerald Plumbing & Heating | Unknown | Phone needed | 7.75 | Plumbing+HVAC | DRAFT_READY |
| 6 | Ultreia Denver | Denver CO | info@ultreiadenver.com | 7.5 | Restaurant | DRAFT_READY |
| 7 | Rioja Denver | Denver CO | info@riojadenver.com | 7.5 | Restaurant | DRAFT_READY |
| 8 | Addison Law Dallas | Dallas TX | info@addisonlaw.com | 7.5 | Law | DRAFT_READY |
| 9 | The Doctor's Office Seattle | Seattle WA | tdoseattle@gmail.com | 7.25 | Restaurant | DRAFT_READY |
| 10 | H+H Seattle (Hart and Hunter) | Seattle WA | sales@palihotelseattle.com | 7.25 | Restaurant | DRAFT_READY |

---

## Existing Pipeline Status

- **MASTER_LEADS.csv:** 1,537 rows (scraped Feb 2026 from dentists, lawyers, restaurants, plumbers across 10 cities)
- **swarm_leads_20260323.csv:** 10 HVAC/electrician/roofing leads, all DRAFT_READY (Uncle Fergie's Electrical top at 8.75)
- **HOT_LEADS.csv:** 22 leads, pre-qualified
- **Outreach drafts:** 20+ cycle folders, 80+ email drafts
- **Biggest blocker:** NO outreach platform set up — email drafts sit in files, not hitting inboxes

---

## Intelligence From This Cycle

- **Spring seasonality confirmed:** HVAC, roofing, plumbing all at peak demand right now in Southern/Sunbelt states
- **Dentists of Houston (http://):** The SSL issue is the strongest hook found this cycle — it's a literal browser warning before the practice name renders
- **9.6s load time (Denver plumber):** Measurable pain points consistently outperform vague "your site is outdated" hooks
- **Dual vertical (plumbing+heating):** Average job value higher than single-service contractors
- **Defense law + no mobile:** Timing of need (arrests = off-hours) + no after-hours capture = concrete dollar argument

---

## Next Cycle Actions

1. **HUMAN ACTION:** Send the top 5 email drafts (8 leads have confirmed emails). Drafts are ready in `outreach_drafts/20260328/`.
2. **Phone lookup:** Find Emerald Plumbing and Heating phone number via Google Maps or Yelp before calling
3. **Automate sending:** Connect `fused_immediate_outreach.jsonl` to a sending tool (Instantly.ai or Smartlead) — leads are bottlenecked at the sending layer
4. Continue cross-referencing `MASTER_LEADS.csv` (1,537 rows) — only ~30 rows have been converted to personalized drafts so far

---

## Files Created This Cycle

- `AUTOMATIONS/leads/swarm_leads_20260328.csv` — 10 leads with full scoring
- `AUTOMATIONS/leads/outreach_drafts/20260328/01_dentists_of_houston.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/02_professional_plumbers_denver.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/03_emerald_plumbing_heating.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/04_ultreia_denver.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/05_rioja_denver.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/06_metro_dental_atlanta.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/07_doctors_office_seattle.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/08_hart_hunter_seattle.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/09_villalobos_law_chicago.md`
- `AUTOMATIONS/leads/outreach_drafts/20260328/10_addison_law_dallas.md`

---

## Evening Cycle Update — 2026-03-28 23:50

**Status:** COMPLETE | **New leads added:** 10 | **Total today:** 20

### New Leads This Cycle (SL328_11 to SL328_20)

| # | Lead | Score | Email | Category | Source |
|---|------|-------|-------|----------|--------|
| 11 | SF Sauna | 9.0 | zach@sf-sauna.com | Physical biz | HN Who Is Hiring |
| 12 | SmileVillage NYC | 8.75 | dkonardds@gmail.com | Dentist | MASTER_LEADS |
| 13 | West Seattle Dental Center | 8.5 | frontoffice@wsdcenter.com | Dentist | MASTER_LEADS |
| 14 | ayeeye AI Camera Platform | 8.5 | ayeeye.careers@gmail.com | Tech startup | HN Who Is Hiring |
| 15 | Dental Care Seattle | 8.25 | smiles@dentalcareseattle.com | Dentist | MASTER_LEADS |
| 16 | Miami Beach Dental | 8.25 | info@miamibeachds.com | Dentist | MASTER_LEADS |
| 17 | Deep Core Technology | 8.0 | jeff@deepcoretech.com | Tech startup | HN Who Is Hiring |
| 18 | CiceroAI Legal | 8.0 | founders@ciceroailaw.com | Legal AI | HN Who Is Hiring |
| 19 | Plumbing School of Houston | 7.75 | roland@plumbingschoolofhouston.com | Trade education | MASTER_LEADS |
| 20 | E3 Restaurant Group Seattle | 7.25 | Info@E3Restaurantgroup.com | Restaurant group | MASTER_LEADS |

### Top 3 to Contact TODAY

1. **zach@sf-sauna.com** — Active HN post, $80-150/hr budget, $5K MRR. Highest priority: they're actively looking NOW.
2. **ayeeye.careers@gmail.com** — Contract starts April 2026 (3 days). React + Three.js rebuild. Must reply before someone else does.
3. **dkonardds@gmail.com** — NYC dental, doctor email direct, $8.75 composite.

### Notes

- HN Who Is Hiring March 2026 file already in repo has 15 pre-scored leads. Only top 4 used — 11 more available for next cycle.
- MASTER_LEADS.csv has 1,537 rows, ~20 processed total. Building a batch script to auto-score all rows is the highest-leverage automation for leads.
- Dental vertical (Squarespace + NOT_mobile) is the most repeatable pattern. 4 dental leads this cycle all came from same signal.

### Files Added (evening cycle)

- `outreach_drafts/20260328/11_sf_sauna.md`
- `outreach_drafts/20260328/12_smilevillage_nyc.md`
- `outreach_drafts/20260328/13_west_seattle_dental.md`
- `outreach_drafts/20260328/14_ayeeye_startup.md`
- `outreach_drafts/20260328/15_dental_care_seattle.md`
- `outreach_drafts/20260328/16_miami_beach_dental.md`
- `outreach_drafts/20260328/17_deep_core_tech.md`
- `outreach_drafts/20260328/18_ciceroai_legal.md`
- `outreach_drafts/20260328/19_plumbing_school_houston.md`
- `outreach_drafts/20260328/20_e3_restaurant_group.md`

*Evening cycle complete — 2026-03-28 23:50*
