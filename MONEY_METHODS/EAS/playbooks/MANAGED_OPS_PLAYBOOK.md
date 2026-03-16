# Managed Ops Delivery Playbook

**How to deliver ongoing Managed Operations at $1,500-$3,000/month**

---

## Overview

Managed Ops is the recurring revenue tier. After a client has a Phone Pilot or Ops Pilot deployed, they pay monthly for you to keep it running, optimize it, and extend it over time. Your job is proactive maintenance, iterative improvement, and monthly reporting. The client should feel like they have a part-time automation engineer on staff without hiring one.

**Package price:** $1,500-$3,000/month (depends on complexity and volume)
**Your payout:** $1,050-$2,100/month (70% of package price)
**Timeline:** Ongoing, month-to-month after initial 3-month commitment
**Effort estimate:** 15-25 hours/month (varies by client needs)

---

## Pricing Tiers

| Tier | Monthly Price | Sub Payout | Typical Client | Included |
|------|--------------|------------|----------------|----------|
| Standard | $1,500/mo | $1,050/mo | 1 automation, low-moderate volume | Monitoring, maintenance, 1-2 improvements/month, monthly report |
| Professional | $2,250/mo | $1,575/mo | 2-3 automations, moderate volume | Everything in Standard + priority support, 3-4 improvements/month |
| Enterprise | $3,000/mo | $2,100/mo | 4+ automations, high volume, complex integrations | Everything in Professional + dedicated Slack channel, weekly check-ins, unlimited improvements |

---

## Monthly Payment

Managed Ops is paid monthly in advance. Payment is not milestone-based like project work.

- Client pays EAS on the 1st of each month
- EAS pays you by the 5th of each month
- If client cancels mid-month, you are paid for the full month

---

## Onboarding (First Month Setup)

Before the monthly cadence begins, set up the infrastructure for ongoing management. This happens once, during the first week.

### Step 1: Inherit the System (2-3 hours)

If you didn't build the original automation:
1. Read the runbook cover to cover
2. Get access to all tools and accounts (n8n, Make, CRM, Bland AI, etc.)
3. Review the workflow diagram and data schema
4. Run 5 test cases to verify you understand how everything works
5. Identify any gaps in documentation and fill them

If you built the original automation:
1. Verify all access is still active
2. Confirm monitoring is still working
3. Review any changes the client made since handoff

### Step 2: Set Up Monitoring Infrastructure (1-2 hours)

If not already in place:
1. **Health check workflow:** Cron that runs every 4 hours, verifies:
   - n8n/Make platform is up and running
   - All webhook endpoints are responsive
   - All API connections are authenticated (not expired)
   - No executions have been stuck for > 1 hour
   - Error rate in last 4 hours is below threshold (10%)
2. **Alert routing:**
   - Health check fails → SMS to you + Slack to EAS
   - Execution error → email to you (batched every 30 min, not per-error)
   - Client reports issue → email + Slack notification
3. **Monthly metrics collection:**
   - Set up automatic data collection for the monthly report (see Week 3)
   - Pull from: n8n execution logs, CRM activity counts, Bland AI call data, error logs

### Step 3: Set Up Communication Channels (30 minutes)

1. **Client communication:**
   - Primary: Email for non-urgent items
   - Secondary: Slack shared channel (Professional/Enterprise tier) or email thread
   - Emergency: Phone/SMS (your number or EAS support number)
2. **EAS communication:**
   - Weekly: 15-min sync with EAS owner (Friday afternoon, async summary if no call needed)
   - Escalation: Slack DM to EAS owner for anything that affects client satisfaction
3. **Documentation:**
   - Maintain a running changelog (Google Doc or Notion page): every change you make, when, and why
   - Update the runbook whenever you change something

### Step 4: Create Automation Backlog (1 hour)

Start a backlog of potential improvements. Sources:
- Signal Map recommendations that weren't implemented yet
- Client requests (from handoff notes, post-delivery feedback)
- Your own observations from reviewing the system
- Industry best practices

**Backlog format:**

| # | Improvement | Impact (H/M/L) | Effort (H/M/L) | Status | Month Planned |
|---|-------------|----------------|-----------------|--------|---------------|
| 1 | Add SMS confirmation after appointment booking | High | Low | Backlog | Month 1 |
| 2 | Build weekly summary report for owner | Medium | Medium | Backlog | Month 1 |
| 3 | Add second language support to phone AI | Medium | High | Backlog | Month 2 |

Prioritize: High impact + Low effort first. Present backlog to client in first monthly meeting.

---

## Monthly Cadence

Every month follows the same 4-week rhythm. This is your operating heartbeat.

---

### WEEK 1: REVIEW + MONITORING (Estimated: 4-6 hours)

**Goal:** Make sure everything is working. Fix anything that's broken. Catch problems before the client notices them.

#### Day 1-2: Health Dashboard Review (1-2 hours)

Pull and review the past month's metrics:

**For Phone Pilot automations:**
| Metric | Last Month | This Month | Trend | Action Needed? |
|--------|-----------|------------|-------|----------------|
| Total calls handled by AI | | | | |
| AI resolution rate (%) | | | | |
| Escalation rate (%) | | | | |
| Average call duration | | | | |
| After-hours calls handled | | | | |
| Missed calls (AI didn't answer) | | | | |
| CRM entries created | | | | |
| New intents detected | | | | |

**For Ops Pilot automations:**
| Metric | Last Month | This Month | Trend | Action Needed? |
|--------|-----------|------------|-------|----------------|
| Total items processed | | | | |
| Success rate (%) | | | | |
| Error rate (%) | | | | |
| Human intervention rate (%) | | | | |
| Average processing time | | | | |
| Items flagged for review | | | | |
| Rollbacks triggered | | | | |

**For all automations:**
| Metric | Last Month | This Month | Trend | Action Needed? |
|--------|-----------|------------|-------|----------------|
| Uptime (%) | | | | |
| Total errors | | | | |
| Unique error types | | | | |
| API credential status | | | | |
| Tool/platform updates needed | | | | |

If any metric is trending in the wrong direction, investigate and add a fix to this week's work.

#### Day 3-4: Error Log Review (1-2 hours)

1. Pull all error logs from the past month
2. Categorize errors:
   - **Transient:** API timeout, network blip — self-resolved on retry. No action needed unless frequency is increasing.
   - **Data quality:** Bad input from client's system — document the pattern, add validation to catch it.
   - **Integration failure:** API changed, credentials expired — fix immediately.
   - **Logic error:** Automation made wrong decision — root cause analysis, fix, add test case.
3. Fix any outstanding errors
4. Update error handling if you see patterns (e.g., "This API times out every Tuesday at 3 PM" → add retry logic specific to that window)

#### Day 5: AI Script/Logic Review (1-2 hours)

**For Phone Pilot:**
- Review call transcripts from the past month (sample 10-15 calls)
- Look for:
  - New questions callers are asking (add to FAQ)
  - Intents the AI misclassified (update pathway)
  - Calls that escalated unnecessarily (tighten AI handling)
  - Calls that should have escalated but didn't (add escalation triggers)
- Update Bland AI scripts based on findings

**For Ops Pilot:**
- Review flagged/failed items from the past month
- Look for:
  - New data patterns the automation doesn't handle
  - Steps that frequently need human intervention (can they be automated?)
  - Performance bottlenecks (slow steps that could be optimized)
- Update workflow logic based on findings

---

### WEEK 2: ITERATION (Estimated: 5-8 hours)

**Goal:** Make the system better. Implement 1-4 improvements from the backlog (depending on tier).

#### Improvement Delivery Process

For each improvement:

1. **Scope it** (15 min)
   - What exactly will change?
   - What's the expected impact?
   - What could go wrong?
   - How long will it take?

2. **Build it** (1-3 hours per improvement)
   - Create the change in a test/staging environment first
   - Follow the same build standards as the original Pilot:
     - Error handling on every node that can fail
     - Data validation for new inputs
     - Variables for configurable values (no hardcoding)

3. **Test it** (30-60 min per improvement)
   - Minimum 3 test cases: happy path, edge case, failure case
   - Verify existing functionality still works (regression test)
   - If the change touches integrations: verify data flows correctly end-to-end

4. **Deploy it** (15 min)
   - Deploy during low-traffic period (early morning or weekend)
   - Monitor for 1 hour after deployment
   - Have rollback plan ready (revert to previous workflow version)

5. **Document it** (15 min)
   - Update the changelog
   - Update the runbook if the change affects operations or troubleshooting
   - Note the improvement in the monthly report

#### A/B Testing (when applicable)

For changes where the impact isn't certain:
1. Run both versions simultaneously (e.g., old call script vs. new call script)
2. Split traffic 50/50 for 1 week
3. Measure the difference (resolution rate, customer satisfaction, processing time)
4. Keep the winner, discard the loser
5. Document the test and result in the monthly report

**Good candidates for A/B testing:**
- Call script wording changes
- Email template variations
- Routing logic tweaks
- Notification timing

**Bad candidates for A/B testing (just ship it):**
- Bug fixes
- Security updates
- New integrations
- Error handling improvements

---

### WEEK 3: REPORTING (Estimated: 3-4 hours)

**Goal:** Show the client what their money is buying. Generate the monthly performance report.

#### Monthly Performance Report Template

**Structure:**

**Page 1: Executive Summary**
- Month at a glance: 3-4 bullet points covering the most important numbers
- Key wins: what went well
- Issues resolved: what broke and how you fixed it
- Next month preview: what improvements are planned

**Page 2: Performance Metrics**

Present all metrics from Week 1 dashboard review in a client-friendly format.

For Phone Pilot clients:
```
CALLS
Total calls handled by AI: XXX
Resolution rate: XX% (target: >70%)
Escalation rate: XX% (target: <20%)
Missed calls: XX (target: <5%)

EFFICIENCY
Average call duration: X:XX
After-hours calls handled: XX
New FAQ questions identified: X (added to system)

CRM
Contacts created/updated: XX
Call notes logged: XX
Tasks created: XX
```

For Ops Pilot clients:
```
PROCESSING
Total items processed: XXX
Success rate: XX% (target: >95%)
Error rate: XX% (target: <5%)
Human intervention: XX items (XX%)

EFFICIENCY
Average processing time: X:XX
Time saved this month: XX hours
Cost saved this month: $X,XXX

RELIABILITY
Uptime: XX.X%
Total errors: XX
Resolved automatically: XX
Required manual fix: XX
```

**Page 3: ROI Summary**

| Metric | Before Automation | This Month | Cumulative (All Time) |
|--------|------------------|------------|----------------------|
| Hours spent on process/week | XX hrs | X hrs | XX hrs saved total |
| Monthly labor cost | $X,XXX | $XXX | $XX,XXX saved total |
| Error/rework cost/month | $XXX | $XX | $X,XXX saved total |
| Automation tool costs/month | $0 | $XXX | $X,XXX total cost |
| **Net savings/month** | — | **$X,XXX** | **$XX,XXX total** |
| **ROI on managed ops fee** | — | **X.Xx** | — |

The ROI section is the most important part of the report. If you can show the client they're saving $5,000/month on a $1,500/month contract, renewals are automatic.

**Page 4: Changes Made This Month**

| Date | Change | Impact | Status |
|------|--------|--------|--------|
| Mar 3 | Added FAQ: "Do you accept [insurance]?" | Resolved 12 calls that previously escalated | Live |
| Mar 10 | Fixed CRM duplicate contact issue | Eliminated 15 duplicate records/month | Live |
| Mar 15 | A/B tested new greeting script | Version B increased resolution rate by 4% | Monitoring |

**Page 5: Recommendations for Next Month**

- Priority improvements from the backlog (2-4 items)
- Any scope expansion opportunities (new processes to automate)
- Tool updates or migrations recommended
- Risks to watch (API deprecations, tool pricing changes, etc.)

#### Report Delivery

- Generate report as PDF
- Send to client 2 business days before the monthly review meeting
- Subject line: "[Business Name] — Monthly Automation Report — [Month Year]"
- Body: brief summary (3-4 sentences) + PDF attached
- CC the EAS owner

---

### WEEK 4: PLANNING (Estimated: 3-5 hours)

**Goal:** Review the month with the client, plan next month, keep the engagement valuable.

#### Monthly Review Meeting (30-45 minutes)

**Agenda:**

1. **Report walkthrough** (10 min)
   - Hit the highlights: calls/items processed, savings, resolution rate
   - Don't read the report — they should have read it. Walk through key insights.
   - "Your AI handled 340 calls this month with an 82% resolution rate, up from 76% last month."

2. **Issues and resolutions** (5 min)
   - What broke, how you fixed it, what you did to prevent recurrence
   - Be transparent. Clients respect honesty more than perfection.

3. **Improvements made** (5 min)
   - What you shipped this month
   - Impact of each change (even if small)

4. **Client feedback** (10 min)
   - "How has the system felt this month?"
   - "Are your team members comfortable with it?"
   - "Anything that's been frustrating or confusing?"
   - "Any new processes you've been thinking about automating?"
   - Listen more than you talk. Write everything down.

5. **Next month plan** (10 min)
   - Present top 2-4 backlog items you recommend
   - Get client input on priority
   - Agree on what gets built next month
   - Discuss any scope changes (flag for EAS if pricing needs to change)

**Post-meeting:**
- Send meeting summary email within 24 hours
- Update backlog with agreed priorities
- Update project tracker
- Notify EAS of any scope change requests or upsell opportunities

#### Backlog Grooming (1-2 hours)

1. Review entire backlog
2. Re-prioritize based on:
   - Client feedback from the meeting
   - Error patterns from Week 1 review
   - New capabilities available (tool updates, new integrations)
   - ROI potential of each improvement
3. Archive completed items
4. Add new items discovered during the month
5. Plan next month's improvements (2-4 items for Standard, 3-4 for Professional, unlimited for Enterprise)

#### SOW Review (if applicable, 30 minutes)

At the end of Month 3 (initial commitment period) and annually thereafter:
- Review the SOW against actual work performed
- If scope has expanded significantly: notify EAS to adjust pricing
- If client is getting less value: proactively suggest improvements or scope changes
- Prepare renewal recommendation for EAS

---

## Incident Response

When something breaks, follow this protocol.

### Priority Definitions

| Priority | Definition | Examples | Response SLA | Resolution SLA |
|----------|-----------|----------|-------------|----------------|
| P0 — Down | Automation is completely non-functional. Business operations affected. | Phone AI not answering, invoice processing stopped, all calls going to voicemail | Within 2 hours | Within 8 hours |
| P1 — Degraded | Automation is running but with significant errors or reduced functionality. | 30% of calls misrouting, CRM entries missing data, slow processing | Within 4 hours | Within 24 hours |
| P2 — Minor | Cosmetic issues, minor inaccuracies, non-critical feature requests. | AI greeting slightly off, report formatting issue, minor data field missing | Within 24 hours | Within 1 week |

### P0 Response Protocol

1. **Acknowledge** (within 30 minutes of detection):
   - Reply to alert or client message: "I'm aware of the issue and investigating."
   - Notify EAS: "P0 incident at [Client Name] — [brief description]. Investigating."

2. **Diagnose** (within 1 hour):
   - Check n8n/Make execution logs for errors
   - Check API connections (credentials, rate limits, service status)
   - Check trigger configuration (webhooks active, cron running)
   - Check external service status pages (Bland AI, CRM, Twilio)

3. **Mitigate** (immediately after diagnosis):
   - If possible: fix the root cause and restart
   - If not immediately fixable: enable manual fallback
     - Phone Pilot: redirect calls to client's team directly (disable forwarding)
     - Ops Pilot: notify SME to process items manually until automation is restored
   - Communicate to client: "Here's what happened, here's our temporary solution, here's when I expect full resolution."

4. **Resolve** (within 8 hours):
   - Fix the root cause
   - Test the fix (minimum 3 test cases)
   - Re-enable automation
   - Verify first 5 real transactions process correctly
   - Notify client: "Resolved. Here's what happened and what we did to prevent it from happening again."

5. **Post-mortem** (within 48 hours):
   - Document: what happened, why, how it was fixed, how to prevent recurrence
   - Add preventive measures to the system (new monitoring, new validation, new error handling)
   - Add to monthly report
   - Send post-mortem summary to EAS

### P1 Response Protocol

1. Acknowledge within 2 hours
2. Diagnose within 4 hours
3. Implement fix within 24 hours
4. Test and verify
5. Notify client of resolution
6. Document in changelog

### P2 Response Protocol

1. Acknowledge within 24 hours
2. Add to backlog with priority
3. Fix within 1 week (or schedule for next iteration cycle)
4. Notify client when fixed
5. Document in changelog

---

## Client Communication Standards

### Response Times

| Channel | Expected Response | Notes |
|---------|-------------------|-------|
| Email (non-urgent) | Within 24 hours (business days) | Acknowledge receipt, provide timeline if can't answer immediately |
| Slack (Professional/Enterprise) | Within 4 hours (business days) | Short, direct answers. Use threads. |
| Phone/SMS (emergency only) | Within 30 minutes | Only for P0 incidents. Client should email/Slack for everything else. |

### Communication Tone

- Professional but human. You're their automation engineer, not a vendor.
- Proactive: tell them about issues before they notice, improvements before they ask
- Direct: no corporate fluff. "The email parsing had 3 failures last week due to a format change from [vendor]. Fixed — added a new parser for the new format."
- Educational: help them understand their system. "Escalation rate dropped 5% because we added [specific FAQ]. Here's why that matters: [explanation]."

### Monthly Communication Cadence

| When | What | Channel |
|------|------|---------|
| Week 1 | "Quick update: reviewed system health, everything looking good / found X issues, fixing now" | Email or Slack |
| Week 2 | "Shipped X improvements this week: [brief list]" (only if significant changes) | Email or Slack |
| Week 3 | Monthly report delivered | Email (formal) |
| Week 4 | Monthly review meeting + summary | Video call + email follow-up |

---

## Handoff Protocol (When You Leave)

If you stop managing a client (moving on, EAS reassigns, etc.):

1. **2-week notice:** Give EAS 2 weeks' notice before your last month
2. **Documentation update:** Ensure runbook is 100% current
3. **Backlog handoff:** Clean up and annotate the backlog
4. **Credentials transfer:** Verify all account access is in EAS vault, not your personal accounts
5. **Successor briefing:** 60-minute call with the new subcontractor covering:
   - System architecture walkthrough
   - Known quirks and edge cases
   - Client preferences and communication style
   - Current backlog priorities
   - Active issues or risks
6. **Client introduction:** Warm handoff email from EAS introducing the new sub
7. **Shadow period:** Available for questions from successor for 2 weeks after transition

---

## Common Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|----------------|--------------|
| Going dark between reports | "Everything's working, nothing to say" | Send a brief update in Weeks 1 and 2, even if it's just "all systems healthy." Silence makes clients nervous. |
| Skipping monitoring for a week | Busy with other clients | Set up automated health checks (Week 1, Step 2). The monitoring should alert YOU, not rely on you remembering to check. |
| Not tracking ROI | "The system works, that should be enough" | The ROI section justifies the monthly fee. If you can't show savings > cost, the client will cancel. Track it from month 1. |
| Reactive only (no improvements) | Just fixing what breaks | Standard tier includes 1-2 improvements/month. If you're only doing maintenance, the client will feel like they're overpaying. Ship something every month. |
| Making changes without documenting | "I'll update the docs later" | You won't. Update the changelog and runbook the same day you make a change. Future-you (or your successor) will thank you. |
| Letting the backlog grow stale | Adding items, never removing | Groom the backlog monthly. Archive anything older than 3 months that hasn't been prioritized — it's not important enough. |
| Not flagging scope changes | Client slowly asks for more | If what the client needs consistently exceeds the tier, notify EAS. It's better to upgrade the tier than to burn out on underpaid work. |
| Ignoring tool updates | Platform pushes update, you don't check | Check n8n/Make/Bland AI changelogs monthly. Breaking changes happen. Catch them before they catch you. |
| Over-communicating | Sending 5 Slack messages a day | Batch your updates. One update per week is enough unless there's an incident. |

---

## Time Budget Summary (Monthly)

| Activity | Estimated Hours | Week |
|----------|----------------|------|
| Dashboard/metrics review | 1-2 hrs | 1 |
| Error log review + fixes | 1-2 hrs | 1 |
| AI script/logic review | 1-2 hrs | 1 |
| Brief status update to client | 0.5 hrs | 1 |
| Improvement 1: scope + build + test + deploy + document | 2-4 hrs | 2 |
| Improvement 2: scope + build + test + deploy + document | 2-4 hrs | 2 |
| A/B test setup (if applicable) | 1 hr | 2 |
| Brief status update to client | 0.5 hrs | 2 |
| Monthly report generation | 2-3 hrs | 3 |
| Report delivery email | 0.5 hrs | 3 |
| Monthly review meeting | 0.75 hrs | 4 |
| Meeting summary email | 0.5 hrs | 4 |
| Backlog grooming + next month planning | 1-2 hrs | 4 |
| EAS weekly sync (4x/month) | 1 hr | All |
| Ad hoc client communication | 1-2 hrs | All |
| **Total (Standard tier)** | **15-22 hrs/mo** | — |
| **Total (Professional tier, 3-4 improvements)** | **20-28 hrs/mo** | — |
| **Total (Enterprise tier, weekly check-ins + unlimited improvements)** | **25-35 hrs/mo** | — |

---

## Renewal & Upsell

### Renewal Signals (Client Will Stay)

- Client references the automation positively in meetings
- Client asks "can we automate [new thing]?"
- Client's team is actively using the system and dashboards
- Engagement metrics are improving month over month
- Client pays on time without reminders

### Churn Signals (Client May Leave)

- Client stops attending monthly meetings
- Client's team reverts to manual processes for some items
- Declining engagement metrics
- Client pushes back on monthly fee without asking for improvements
- Client's business is shrinking (cuts in other areas too)

**If you see churn signals:** Notify EAS immediately with specifics. Don't wait for the client to cancel. EAS may offer pricing adjustment, scope change, or direct outreach.

### Upsell Opportunities

| Signal | Upsell |
|--------|--------|
| "Can we add another process?" | Second Ops Pilot ($4,500) then add to Managed Ops |
| "We're getting more calls than the AI can handle" | Scale phone system, potentially upgrade tier |
| "We want AI for our website chat too" | Future product — flag to EAS |
| "Our other location needs this" | Second deployment — flag to EAS |
| "Can you help our [partner/friend]'s business?" | Referral — flag to EAS immediately |

Always flag upsell opportunities to EAS. Never sell directly — your job is delivery, EAS handles sales.

---

## Tools & Templates Reference

| Resource | Purpose | Location |
|----------|---------|----------|
| Monthly Report Template | Performance report | EAS Shared Drive → Templates |
| Backlog Tracker | Improvement backlog | Google Sheet or Notion (create per client) |
| Changelog Template | Document all changes | Google Doc or Notion (create per client) |
| Incident Post-Mortem Template | P0/P1 documentation | EAS Shared Drive → Templates |
| Meeting Agenda Template | Monthly review meeting | EAS Shared Drive → Templates |
| Health Check Workflow | n8n workflow template | EAS Shared Drive → n8n Templates |
| Project Tracker | Log milestones and deliverables | EAS Notion / Airtable |
