# Lead Machine Report — 2026-03-22 Cycle 11
**Agent:** lead_machine
**Run time:** 2026-03-22 ~23:20
**Status:** COMPLETE

---

## Summary

- **Leads generated:** 10
- **Source:** OpenClaw priority_targets.json (pre-scored leads with verified emails)
- **Categories:** auto_repair(1), dentist(1), chiropractor(5), physical_therapist(2), funeral_home(1)
- **Avg composite score:** 8.0/10
- **All 10 have direct email addresses**
- **0 duplicate leads** (cross-checked against all existing personalized/ drafts)

---

## Leads (Ranked by Composite Score)

| Rank | Lead | Category | City | Email | Score | Key Issue |
|------|------|----------|------|-------|-------|-----------|
| 1 | JC Automotive Service | auto_repair | St Petersburg, FL | john@jcautomotive.com | 9.25 | 502 site down |
| 2 | East Portland Dentistry | dentist | Portland, OR | eastportlanddentistry@gmail.com | 8.25 | Gmail email + table layout |
| 3 | Shorewood Family Chiro | chiropractor | Milwaukee, WI | monicamaroney@shorewoodfamilychiro.com | 8.25 | No mobile/form/schema |
| 4 | Pope Family Chiro | chiropractor | Milwaukee, WI | lakeviewchiro@att.net | 8.0 | att.net email + no mobile |
| 5 | The Healing Touch Chiro | chiropractor | Sacramento, CA | reception@fixmyback.com | 8.25 | SSL 501 + brand mismatch |
| 6 | Durham Spine & Rehab | physical_therapist | Durham, NC | dsr@mindspring.com | 8.0 | Flash + no SSL |
| 7 | Columbia Physical Therapy | physical_therapist | Columbia, SC | columbiapt@earthlink.net | 7.5 | Flash + no SSL + no mobile |
| 8 | Magnolia Funeral Home | funeral_home | Baton Rouge, LA | magnolia@cox.net | 7.5 | Flash + no SSL (trust-critical) |
| 9 | Huntsville Chiropractic Center | chiropractor | Huntsville, AL | hsvchiro@charter.net | 7.25 | No mobile (high-growth market) |
| 10 | ACME Chiropractic | chiropractor | Sacramento, CA | acmechiropractic@att.net | 7.25 | SSL 501 + att.net email |

---

## Files Created

### Lead CSV
- `AUTOMATIONS/leads/swarm_leads_20260322_cycle11.csv`

### Outreach Drafts (detailed)
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/01_jc_automotive_st_pete.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/02_east_portland_dentistry.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/03_shorewood_family_chiro_milwaukee.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/04_pope_family_chiro_milwaukee.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/05_durham_spine_rehab.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/06_columbia_pt_sc.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/07_magnolia_funeral_baton_rouge.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/08_huntsville_chiro_al.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/09_healing_touch_chiro_sacramento.md`
- `AUTOMATIONS/leads/outreach_drafts/20260322_c11/10_acme_chiro_sacramento.md`

### Send-Ready (paste into Gmail)
- `MONEY_METHODS/OUTBOUND/personalized/jc_automotive_st_pete_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/east_portland_dentistry_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/shorewood_family_chiro_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/pope_family_chiro_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/durham_spine_rehab_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/columbia_pt_sc_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/magnolia_funeral_baton_rouge_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/huntsville_chiro_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/healing_touch_chiro_sacramento_email1.txt`
- `MONEY_METHODS/OUTBOUND/personalized/acme_chiro_sacramento_email1.txt`

---

## Source Intelligence

**From:** `AUTOMATIONS/leads/auto_local_biz_openclaw_nationwide_9569/priority_targets.json`
All leads had:
- Composite score >= 7.25 (sourced by OpenClaw scraper)
- Direct email addresses (not contact forms)
- No existing draft in `MONEY_METHODS/OUTBOUND/personalized/`

**OpenClaw remaining high-value targets** (score 8.0+, undrafted):
- Martinez Family Dental (Mason, OH) — mandmdental@hotmail.com
- Progressive Dental Care (Hanover, PA) — xrays@myprogressivedental.com
- Higgins Law Office (Phoenix, AZ) — dbhiggins85012@hotmail.com
- Tyler Allen Law (Phoenix, AZ) — tyler@allenlawaz.com
- Smile Village NYC (New York, NY) — dentaladmin@smilevillage.nyc
- Wellness Dental (Portland, OR) — office@wellnessdentalpdx.com
- Downing Street Dental (Denver, CO) — office@downingstreetdental.com
- Montgomery Eye Center (Montgomery, AL) — mgeye@charter.net

---

## Quality Notes

**High-urgency (send first):**
1. JC Automotive — site is ACTIVELY DOWN (502). Emergency pitch.
2. Healing Touch Chiro — SSL 501 broken right now. Emergency pitch.
3. Durham Spine & Rehab — Flash detected. Every visitor hits error. Emergency pitch.

**Handle with care:**
- Magnolia Funeral Home: sensitive niche, 1 follow-up max, respectful tone only

**Stagger Sacramento sends:**
- Healing Touch (day 1) and ACME Chiro (day 3-4) — same market, don't send same day

---

## Pipeline Status

Total personalized drafts now in `MONEY_METHODS/OUTBOUND/personalized/`: 48
Total swarm_leads CSVs (cycle 1-11): 11 for today
Total leads cycle 11: 10
Cumulative pipeline: GROWING

**Next cycle focus (c12):** Phoenix law firms, NYC dentists, Denver dental, remaining OpenClaw 8.0+ targets
