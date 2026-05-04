# Email Sequences Library - Master Index

**Created:** 2026-01-20
**Purpose:** Complete email sequence library for all PRINTMAXX use cases
**Total sequences:** 12
**Total emails:** 57

---

## Quick reference

| Sequence Type | Files | Total Emails | Use Case |
|--------------|-------|--------------|----------|
| Welcome | 3 | 21 | New subscriber onboarding |
| Sales/Launch | 3 | 15 | Product launches |
| Nurture | 3 | 12 | Ongoing engagement |
| Abandoned Cart | 1 | 3 | Cart recovery |
| Cold Outreach | 2 | 10 | B2B prospecting |
| Re-engagement | 1 | 3 | Win back inactive |

---

## Welcome sequences

Convert new subscribers into customers within 7 days.

| File | Brand | Product | Emails | Price Point |
|------|-------|---------|--------|-------------|
| `welcome_sequences/ai_welcome_7day.md` | StackPilot | AI Clarity Stack | 7 | $47 |
| `welcome_sequences/faith_welcome_7day.md` | DailyAnchor | Daily Anchor System | 7 | $27 |
| `welcome_sequences/fitness_welcome_7day.md` | 3HourPhysique | 3-Hour Physique | 7 | $47 |

**Key metrics to target:**
- Email 1 open rate: 55-60%
- Email 7 click rate: 12-15%
- Sequence conversion: 4-8%

---

## Sales/Launch sequences

5-day campaigns for product launches or promotions.

| File | Brand | Product | Emails | Launch Price |
|------|-------|---------|--------|--------------|
| `sales_sequences/ai_clarity_launch_5day.md` | StackPilot | AI Clarity Stack | 5 | $37 |
| `sales_sequences/daily_anchor_launch_5day.md` | DailyAnchor | Daily Anchor System | 5 | $19 |
| `sales_sequences/3hour_physique_launch_5day.md` | 3HourPhysique | 3-Hour Physique | 5 | $37 |

**Key metrics to target:**
- Email 1 open rate: 45-50%
- Email 5 click rate: 15-20%
- Sequence conversion: 3-5%

---

## Nurture sequences

Weekly emails to maintain engagement and soft-sell.

| File | Brand | Frequency | Emails/Cycle |
|------|-------|-----------|--------------|
| `nurture_sequences/ai_weekly_tips.md` | StackPilot | Tuesday 10am | 4 |
| `nurture_sequences/faith_weekly_devotional.md` | DailyAnchor | Sunday 6pm | 4 |
| `nurture_sequences/fitness_weekly_motivation.md` | 3HourPhysique | Monday 6am | 4 |

**Key metrics to target:**
- Average open rate: 35-40%
- Average click rate: 4-5%
- Conversion per cycle: 2%

---

## Abandoned cart sequence

Recover sales from incomplete checkouts.

| File | Works For | Emails | Timing |
|------|-----------|--------|--------|
| `abandoned_cart/cart_abandonment_3email.md` | All products | 3 | 1hr, 24hr, 72hr |

**Key metrics to target:**
- Email 1 recovery rate: 15%
- Total sequence recovery: 25-30%

---

## Cold outreach sequences

B2B prospecting for agency and SaaS.

| File | Brand | Target | Emails |
|------|-------|--------|--------|
| `cold_outreach/agency_cold_5touch.md` | Enterprise Automation | SMB owners | 5 |
| `cold_outreach/saas_cold_5touch.md` | AutoReply AI | Shopify stores | 5 |

**Key metrics to target:**
- Email 1 reply rate: 5-8%
- Total sequence reply rate: 15-20%
- Meeting book rate: 3-8%

---

## Re-engagement sequence

Win back subscribers who stopped opening.

| File | Trigger | Emails | Timing |
|------|---------|--------|--------|
| `reengagement/30day_inactive_3email.md` | 30 days no opens | 3 | Day 31, 35, 42 |

**Key metrics to target:**
- Total re-engagement rate: 8-12%
- Healthy unsubscribe rate: 5-10%

---

## Implementation checklist

### Phase 1: Foundation (Week 1)
- [ ] Set up email platform (ConvertKit, Loops, or similar)
- [ ] Configure sending domain with SPF/DKIM/DMARC
- [ ] Create segments for each niche
- [ ] Import welcome sequences
- [ ] Test welcome flow end-to-end

### Phase 2: Automation (Week 2)
- [ ] Set up abandoned cart triggers
- [ ] Configure nurture sequence timing
- [ ] Set up re-engagement triggers (30-day rule)
- [ ] Test all automation paths

### Phase 3: Launch prep (Week 3)
- [ ] Prepare launch sequence variants
- [ ] Set up A/B testing infrastructure
- [ ] Configure conversion tracking
- [ ] Create reporting dashboard

### Phase 4: Cold outreach (Week 4+)
- [ ] Warm sending domain (2+ weeks)
- [ ] Build prospect list (LinkedIn, BuiltWith)
- [ ] Verify emails before sending
- [ ] Start with 20-30 emails/day

---

## Copy style reminders

All sequences follow `.claude/rules/copy-style.md`:

**Never use:**
- Em dashes
- AI vocabulary (leverage, utilize, comprehensive, etc.)
- "It's not just X, it's Y" constructions
- Vague attributions without links
- Promotional adjectives

**Always:**
- Start with the conclusion
- Use specific numbers
- Write like texting a smart friend
- Sentence case headings
- One clear CTA per email

---

## Maintenance schedule

| Task | Frequency | Owner |
|------|-----------|-------|
| Review open/click rates | Weekly | Marketing |
| Update subject line variants | Monthly | Marketing |
| Refresh nurture content | Quarterly | Content |
| Audit inactive subscribers | Monthly | Operations |
| A/B test new approaches | Ongoing | Marketing |

---

## Related files

- Copy style guide: `.claude/rules/copy-style.md`
- Brand accounts: `LEDGER/BRANDED_ACCOUNTS.md`
- Funnel metrics: `LEDGER/FUNNEL_METRICS.csv`
- Lead capture: `LEDGER/leads.csv`
- Email warmup protocols: `AUTOMATIONS/email_warmup/`

---

## Questions?

Check MASTER_DOC/ for full operating procedures or create an issue in OPS/logs/.
