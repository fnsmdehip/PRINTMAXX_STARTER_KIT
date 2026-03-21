# Growth Plan: [PH LAUNCH] Educato App: Personalized exam prep, now in your

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-700/mo

---

## Tactics

1. Contact Educato founders within 48h of PH launch — warm window, they're growth-hungry
2. Leave value-add comment on PH listing (no spam) to build credibility before DM
3. Monitor PH education category daily — exam prep, flashcards, study tools all signal our app niche
4. Cross-reference launches with App Store rankings to find ones with traction but weak ASO
5. Use Educato as social proof anchor: 'we helped an app like Educato that launched on PH'

## Budget Tier Strategies

### FREE
Playwright scrapes PH daily for edtech launches. Extract Twitter/email from founder profiles. Queue outreach via cold_email_scripts.py with EAS pitch (we build growth infra for their app). Target: 3-5 contacts/day in 48h launch window.

### LOW
$0-50/mo — Build ExamStreak using existing streak template (1-2 day effort), list on App Store, ride search traffic from Educato's PH buzz. Zero incremental infra cost.

### MID
$50-200/mo — Promote ExamStreak via targeted Reddit posts in r/Mcat, r/Sat, r/LSAT, r/medicalschool. PH comment engagement on education launches to drive profile traffic.

## Daily Actions

- [ ] Wire ph_edtech_launch_scraper.py into existing chain_14_ph_launches_today__high_quality_b2b_ — no new chain needed, parameterize category filter to 'education,exam,study,learning'
- [ ] Scraper extracts: app name, founder Twitter/email, launch date, upvote count, PH page URL
- [ ] Route to cold outreach queue with EAS pitch template (48h window = warm lead)
- [ ] Subagent check: does scripture-streak template support exam-question content type? If yes, add 'ExamStreak' to APP_FACTORY backlog as validated clone candidate
- [ ] Add cron entry: 0 8 * * * to catch daily PH education launches
- [ ] Log to LEDGER/COMPETITIVE_INTEL.csv with category=EDTECH_APP

## Tooling

```json
{
  "browser": "playwright (PH profile scraping)",
  "email": "custom cold_email_scripts.py (existing)",
  "content": "none"
}
```
