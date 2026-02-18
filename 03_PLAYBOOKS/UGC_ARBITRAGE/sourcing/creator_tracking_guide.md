# Creator tracking guide

How to use the creator_tracking.csv file and manage your creator roster.

---

## CSV column definitions

| Column | Description | Values |
|--------|-------------|--------|
| creator_id | Unique identifier | CRE001, CRE002, etc. |
| name | Creator's name | Full name |
| platform | Primary platform | Instagram, TikTok, Fiverr, etc. |
| handle | Social handle or profile | @username |
| email | Contact email | For contracts and briefs |
| niche | Content niche | fitness, faith, student, wellness, lifestyle |
| tier | Pricing tier | entry, standard, premium, influencer |
| location | Country/region | USA, UK, Poland, Philippines, etc. |
| rate_30s | 30-second video rate | Dollar amount |
| rate_60s | 60-second video rate | Dollar amount |
| quality_score | Quality rating | 1-5 (5 = excellent) |
| reliability_score | Reliability rating | 1-5 (5 = always on time) |
| turnaround_days | Typical delivery time | Number of days |
| total_videos_delivered | Lifetime deliveries | Count |
| last_video_date | Most recent delivery | YYYY-MM-DD |
| status | Current relationship status | prospect, active, inactive, blacklist |
| payment_method | Preferred payment | PayPal, Wise, Venmo, etc. |
| notes | Free-form notes | Any relevant info |

---

## Status definitions

| Status | Description | Action |
|--------|-------------|--------|
| prospect | Reached out, no project yet | Follow up or send brief |
| active | Currently working together | Prioritize for new projects |
| inactive | Worked before, not recently | Re-engage for new campaigns |
| blacklist | Do not work with | Document reason in notes |

---

## Quality score guide

| Score | Definition | Characteristics |
|-------|------------|-----------------|
| 5 | Exceptional | Professional quality, needs no direction, could resell as premium |
| 4 | Good | Solid quality, minor adjustments only, reliable output |
| 3 | Adequate | Gets the job done, may need specific direction |
| 2 | Below average | Frequent revisions needed, inconsistent |
| 1 | Poor | Major quality issues, avoid unless desperate |

---

## Reliability score guide

| Score | Definition | Characteristics |
|-------|------------|-----------------|
| 5 | Always on time | Never misses deadline, proactive communication |
| 4 | Usually on time | Rare delays, communicates if late |
| 3 | Sometimes late | Occasional delays, needs reminders |
| 2 | Often late | Frequent delays, poor communication |
| 1 | Unreliable | Missed deadlines, ghosted, excuses |

---

## Niche categories

| Niche | Apps it serves | Creator profile |
|-------|----------------|-----------------|
| fitness | FemFit, WalkToUnlock | Gym goers, fitness enthusiasts, wellness creators |
| faith | PrayerLock, DailyDevotion, DailyAnchor | Christian creators, faith lifestyle, church communities |
| student | StudyLock | College students, studytok, productivity creators |
| wellness | WalkToUnlock | Digital wellness, walking, health lifestyle |
| lifestyle | Multiple | General lifestyle creators, relatable content |

---

## Tier definitions

| Tier | Rate range | Quality expectation | Use for |
|------|------------|---------------------|---------|
| entry | $25-50 | Basic, may need direction | Volume, testing, budget |
| standard | $50-100 | Good, reliable | Core production |
| premium | $100-200 | High, minimal revision | Important campaigns |
| influencer | $200-500 | Exceptional, organic reach | Launch, premium clients |

---

## Roster management

### Target roster size
- **Primary creators (active):** 2-3 per niche
- **Secondary creators (backup):** 2-3 per niche
- **Prospects (in development):** 3-5 per niche

### Niche roster targets

| Niche | Primary | Secondary | Prospects | Total |
|-------|---------|-----------|-----------|-------|
| Fitness | 3 | 3 | 5 | 11 |
| Faith | 3 | 3 | 5 | 11 |
| Student | 2 | 2 | 5 | 9 |
| Wellness | 2 | 2 | 3 | 7 |
| **Total** | 10 | 10 | 18 | 38 |

### Who to prioritize
1. Quality 4-5, Reliability 4-5
2. Niche experts (specific demographic match)
3. Volume availability (can handle 5+ videos/month)
4. Quick turnaround (3-5 days)

---

## When to promote creators

### Entry to Standard
- Delivered 3+ videos successfully
- Quality score improved to 4+
- Reliability score 4+
- Understands briefs without hand-holding

### Standard to Premium
- Delivered 10+ videos
- Quality score 4-5 consistently
- Client feedback positive
- Can handle complex briefs
- Quick turnaround capability

### Standard to Retainer
- Consistent quality over 3+ months
- Available for volume work
- Responsive communication
- Willing to negotiate package rates

---

## When to demote or remove

### Demote to lower tier
- Quality dropped below tier standard
- Reliability issues emerged
- Rates increased beyond tier range

### Move to inactive
- No project in 60+ days
- Unresponsive to outreach
- Rates no longer competitive

### Blacklist
- Missed deadline without communication
- Delivered plagiarized content
- Unprofessional behavior
- Refused to do revisions
- Violated usage rights

---

## Outreach tracking companion

Use this alongside the CSV to track outreach:

| Field | Purpose |
|-------|---------|
| outreach_date | When you first messaged |
| outreach_platform | Where you messaged |
| outreach_template | Which template used |
| response_date | When they replied |
| response_type | yes, no, no response |
| followup_date | When to follow up |

### Add to CSV or separate sheet

```
outreach_id,creator_id,outreach_date,platform,template_used,response,response_date,next_action
OUT001,CRE001,2026-01-15,Instagram,fitness_initial,yes,2026-01-16,send_brief
OUT002,CRE002,2026-01-15,TikTok,student_initial,no_response,,followup_1/20
```

---

## Project tracking companion

Track individual projects separately:

| Field | Purpose |
|-------|---------|
| project_id | Unique project identifier |
| creator_id | Links to creator |
| app | Which app |
| brief_sent_date | When brief was sent |
| deadline | Expected delivery |
| delivered_date | Actual delivery |
| videos_count | Number of videos |
| hooks_count | Number of hooks |
| cost | What you paid |
| revisions | Number of revision rounds |
| quality_rating | Quality of this delivery |

### Project tracking CSV

```
project_id,creator_id,app,brief_sent,deadline,delivered,videos,hooks,cost,revisions,quality
PRJ001,CRE001,FemFit,2026-01-10,2026-01-17,2026-01-16,2,6,$150,1,4
PRJ002,CRE003,StudyLock,2026-01-12,2026-01-19,2026-01-20,1,3,$50,2,3
```

---

## Monthly review checklist

### Weekly
- [ ] Check for missed deadlines
- [ ] Follow up on outstanding projects
- [ ] Update quality/reliability scores
- [ ] Outreach to 5-10 new prospects

### Monthly
- [ ] Review roster balance by niche
- [ ] Update rates based on market
- [ ] Promote/demote creators as needed
- [ ] Clear inactive prospects
- [ ] Calculate creator costs vs revenue

### Quarterly
- [ ] Negotiate retainers with top performers
- [ ] Expand roster in high-demand niches
- [ ] Drop consistently low performers
- [ ] Review pricing tiers

---

## Google Sheets sync

If using Google Sheets as source of truth:

1. Export this CSV to Google Sheets
2. Set up IMPORTRANGE to LEDGER/CREATOR_ROSTER.csv
3. Use data validation for status, tier, niche columns
4. Add conditional formatting for quality/reliability scores
5. Create pivot tables for roster analysis

---

## Related files

- `creator_brief_template.md` - Briefs for each app
- `outreach_dm_templates.md` - DM templates by niche
- `pricing_tiers.md` - Pricing structure
- `/LEDGER/UGC_PROJECTS.csv` - Project tracking (create when needed)
- `/LEDGER/UGC_PAYMENTS.csv` - Payment tracking (create when needed)

---

Created: 2026-01-21
