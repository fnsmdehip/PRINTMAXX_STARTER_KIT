# Support metrics

What to track, benchmarks to hit, and how to set up dashboards.

---

## Core metrics

### 1. First response time (FRT)

**What it measures:** How long until customer gets first human response.

**Target:**
- Critical: <2 hours
- High: <8 hours
- Medium: <24 hours
- Low: <48 hours

**How to calculate:**
```
FRT = Timestamp of first response - Timestamp of ticket creation
```

**Why it matters:** Customers care most about being acknowledged. Fast FRT reduces anxiety even if resolution takes longer.

### 2. Average resolution time (ART)

**What it measures:** Time from ticket creation to resolution.

**Target:**
- Simple issues: <24 hours
- Medium issues: <48 hours
- Complex issues: <72 hours
- Overall average: <36 hours

**How to calculate:**
```
ART = Timestamp of resolution - Timestamp of ticket creation
```

**Why it matters:** Measures actual customer wait time.

### 3. First contact resolution (FCR)

**What it measures:** Percentage of tickets resolved in first response.

**Target:** >60%

**How to calculate:**
```
FCR = (Tickets resolved in one response / Total tickets) x 100
```

**Why it matters:** Higher FCR = faster resolution + happier customers + lower cost per ticket.

### 4. Customer satisfaction (CSAT)

**What it measures:** How satisfied customers are with support interaction.

**Target:** >90%

**How to calculate:**
```
CSAT = (Positive ratings / Total ratings) x 100
```

Send survey after resolution. Simple scale: Satisfied / Unsatisfied.

**Why it matters:** Direct measure of support quality.

### 5. Ticket volume

**What it measures:** Number of support requests.

**Targets:**
- Track trend over time
- Tickets per 100 active users should decrease
- Spikes indicate problems

**How to calculate:** Count tickets per day/week/month.

**Why it matters:** High volume signals product issues. Low volume per user signals good UX and documentation.

### 6. Tickets per user

**What it measures:** Support load relative to user base.

**Target:** <0.5 tickets per user per month

**How to calculate:**
```
Tickets per user = Total monthly tickets / Monthly active users
```

**Why it matters:** Normalizes for growth. Lets you compare support efficiency over time.

---

## Secondary metrics

### 7. Escalation rate

**What it measures:** Percentage of tickets that need escalation.

**Target:** <15%

**How to calculate:**
```
Escalation rate = (Escalated tickets / Total tickets) x 100
```

**Why it matters:** High escalation = training gaps or product complexity.

### 8. Reopen rate

**What it measures:** Tickets marked resolved but reopened by customer.

**Target:** <10%

**How to calculate:**
```
Reopen rate = (Reopened tickets / Resolved tickets) x 100
```

**Why it matters:** Low reopen rate = issues actually fixed, not just closed.

### 9. Reply count

**What it measures:** Average number of responses before resolution.

**Target:** <3 replies

**How to calculate:**
```
Avg replies = Total replies / Total resolved tickets
```

**Why it matters:** More replies = worse experience. Optimize canned responses and training.

### 10. Channel distribution

**What it measures:** Where tickets come from.

**Track:**
- Email: X%
- In-app chat: X%
- Social media: X%
- App store reviews: X%

**Why it matters:** Invest in channels customers prefer. Reduce friction where volume is high.

---

## Category metrics

Track volume by issue type:

| Category | Expected % | Action if higher |
|----------|------------|------------------|
| Billing | 30-35% | Simplify billing UX |
| Technical bugs | 20-25% | Prioritize fixes |
| How-to / feature questions | 25-30% | Improve docs/onboarding |
| Account issues | 10-15% | Audit account flows |
| Feature requests | 5-10% | Feed to product team |

Sudden spikes in category = investigate root cause.

---

## SLA compliance

Track percentage of tickets meeting SLA:

**Target:** >95% SLA compliance

| Priority | FRT SLA | Resolution SLA |
|----------|---------|----------------|
| Critical | 2h | 24h |
| High | 8h | 48h |
| Medium | 24h | 72h |
| Low | 48h | 5d |

Report SLA misses and investigate patterns.

---

## Benchmarks

Industry benchmarks for SaaS support:

| Metric | Good | Great | Elite |
|--------|------|-------|-------|
| First response time | <12h | <4h | <1h |
| Resolution time | <48h | <24h | <12h |
| First contact resolution | 50% | 65% | 80% |
| CSAT | 85% | 90% | 95% |
| Tickets per user/month | 1.0 | 0.5 | 0.2 |

Start with "Good" targets. Move to "Great" as you scale.

---

## Dashboard setup

### Tools

**Budget option (free):**
- Google Sheets for tracking
- Manual entry from help desk
- Weekly pivot table reports

**Mid-tier ($50-200/month):**
- Help Scout, Freshdesk, or Intercom
- Built-in reporting
- Automated dashboards

**Advanced ($200+/month):**
- Zendesk with Explore
- Custom analytics with Metabase
- API integrations

### Recommended dashboard layout

**Daily view:**
- Open tickets
- Tickets awaiting response
- SLA at risk (approaching breach)
- Today's CSAT ratings

**Weekly view:**
- Tickets opened vs closed
- Average FRT and ART
- CSAT trend
- Top categories
- Escalation count

**Monthly view:**
- All core metrics with MoM change
- SLA compliance %
- Category breakdown
- Agent performance (if applicable)
- Support cost per ticket

---

## Calculating support costs

**Cost per ticket:**
```
Cost per ticket = (Agent salary + tools + overhead) / Tickets handled
```

Example:
- Agent cost: $4,000/month
- Tools: $200/month
- Tickets: 400/month
- Cost per ticket: $10.50

**Target:** <$15 per ticket for early stage.

Reduce with:
- Better documentation (deflect tickets)
- Improved canned responses (faster resolution)
- Product fixes (fewer bugs = fewer tickets)

---

## Reporting cadence

**Daily:** Quick check on open tickets, urgent items
**Weekly:** Team review of metrics, identify trends
**Monthly:** Full report, action items, goal setting
**Quarterly:** Strategic review, benchmark comparison, tooling decisions

---

## Red flags to watch

| Metric change | Possible cause | Action |
|---------------|----------------|--------|
| FRT increasing | Volume spike, understaffed | Check for product incident, add capacity |
| CSAT dropping | Bad responses, frustrated users | Review recent tickets, retrain |
| Ticket volume spike | Bug, outage, confusing feature | Investigate product/comms |
| High reopen rate | Not actually solving issues | Review closed tickets |
| FCR dropping | Complex issues, training gaps | Update docs, add canned responses |

---

## Getting started

Minimum viable tracking:

1. **Week 1:** Count tickets manually. Note categories.
2. **Week 2:** Start tracking FRT and resolution time.
3. **Week 3:** Add CSAT survey (simple: thumbs up/down).
4. **Week 4:** Set up basic spreadsheet dashboard.
5. **Month 2:** Formalize targets, start weekly reviews.

Don't overcomplicate early. Track the basics well before adding complexity.
