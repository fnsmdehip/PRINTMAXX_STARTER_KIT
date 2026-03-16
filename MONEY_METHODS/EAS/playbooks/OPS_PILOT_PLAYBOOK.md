# Ops Pilot Delivery Playbook

**How to deliver a Back-Office Automation Pilot in 10 days**

---

## Overview

The Ops Pilot automates a single back-office workflow that the client identified during their Signal Map (or equivalent discovery). Unlike the Phone Pilot which has a fixed scope (phone handling), the Ops Pilot adapts to whatever process the client needs automated. Common targets: invoice processing, dispatch/scheduling, customer support triage, lead intake, and reporting.

**Package price:** $4,500
**Your payout:** $3,150 total (30/40/30 milestone split)
**Timeline:** 10 business days from kickoff
**Effort estimate:** 35-45 hours of actual work

---

## Payment Milestones

| Milestone | Trigger | Amount |
|-----------|---------|--------|
| M1 (30%) | SOW signed, kickoff confirmed | $945 |
| M2 (40%) | Quality Checkpoint 2 approved by EAS | $1,260 |
| M3 (30%) | Client accepts final deliverable + 3-day shadow period passes | $945 |

---

## Pre-Requisites Checklist

- [ ] Signal Map completed for this client (or equivalent discovery with workflow data)
- [ ] Client SOW signed — must specify WHICH process is being automated
- [ ] Client has provided:
  - [ ] Access to all tools involved in the workflow (logins, API keys, or admin invites)
  - [ ] Sample data: 10-20 real examples of the process being done manually (e.g., 10 invoices, 10 support tickets, 10 leads)
  - [ ] Current process documentation (even if informal — screenshots, notes, "how we do it" doc)
  - [ ] Contact person who currently does this task (the "subject matter expert" / SME)
  - [ ] Edge cases they already know about ("watch out for [X]")
  - [ ] Approval workflow: who signs off on automated outputs before they go to clients/customers?
- [ ] You have an n8n instance running (self-hosted or cloud) OR Make/Zapier account
- [ ] You have access to EAS project tracker

**Tool selection for Ops Pilots:**

| Scenario | Recommended Tool | Reason |
|----------|-----------------|--------|
| Complex logic, branching, error handling needed | n8n (self-hosted) | Full control, no per-operation costs, code nodes for custom logic |
| Client wants managed platform, moderate complexity | Make | Visual builder, reliable, good integrations, reasonable pricing |
| Simple linear workflow, client already on Zapier | Zapier | Don't migrate if they're already paying for it |
| Needs database/data storage | n8n + Airtable or Supabase | n8n for logic, Airtable/Supabase for structured data |
| Needs document generation | n8n + Google Docs API or Carbone | Template-based doc generation |
| Needs approval workflows | n8n + Slack/email approval nodes | Human-in-the-loop before automated action fires |

---

## Common Ops Automation Patterns

Before diving into the day-by-day, here are the 5 most common Ops Pilot builds. Identify which pattern matches your client's process and use it as your starting architecture.

### Pattern 1: Invoice Processing

**Trigger:** Invoice/receipt arrives (email attachment, upload, scan)
**Pipeline:**
```
Email/Upload received
  → Extract document (PDF/image)
  → OCR + data extraction (vendor, amount, date, line items)
  → Validate against PO or expected amounts
  → Route for approval (if above threshold)
  → Create entry in QuickBooks/Xero/FreshBooks
  → Attach original document
  → Notify finance team
  → Weekly reconciliation report
```

**Key integrations:** Gmail/Outlook (trigger), Google Vision or Mindee (OCR), QuickBooks/Xero (accounting), Slack/email (approval + notification)

**Edge cases to handle:**
- Duplicate invoices (same vendor + amount + date = flag, don't auto-process)
- Missing information (no PO number, no date) → flag for human review
- Foreign currency → convert using exchange rate API
- Multi-page invoices → combine before OCR
- Handwritten/poor quality scans → flag for human entry

**Approval logic:** Invoices under $500: auto-approve. $500-$5,000: single approver. $5,000+: two approvers.

### Pattern 2: Dispatch / Scheduling

**Trigger:** New job/service request (form, phone call, CRM entry)
**Pipeline:**
```
New job request received
  → Extract: service type, location, urgency, customer info
  → Check technician availability (calendar API)
  → Match: skill set + location + availability
  → Assign technician
  → Create calendar event
  → Notify technician (SMS + email with job details)
  → Notify customer (confirmation email/SMS with tech name + ETA)
  → Update CRM/job board
  → Post-completion: trigger follow-up survey
```

**Key integrations:** CRM or form (trigger), Google Calendar/Cal.com (availability), Twilio (SMS), Google Maps API (distance/ETA), CRM (job tracking)

**Edge cases to handle:**
- No technician available → escalate to dispatcher
- Emergency/urgent job → override scheduling, bump to top
- Technician calls in sick → re-route their jobs for the day
- Customer cancels → free up slot, notify tech
- Job runs long → alert next customer of delay

### Pattern 3: Customer Support Triage

**Trigger:** Support request arrives (email, form, chat)
**Pipeline:**
```
Support request received
  → Classify: category (billing, technical, general, complaint)
  → Classify: priority (P0-P3 based on keywords and customer tier)
  → Auto-respond with acknowledgment + expected response time
  → Route to correct team/person based on category
  → If common question: send auto-response from knowledge base
  → Create ticket in helpdesk (Zendesk, Freshdesk, or simple tracker)
  → SLA timer starts
  → If no response within SLA: escalate notification
  → Post-resolution: send satisfaction survey
```

**Key integrations:** Gmail/form/chat (trigger), OpenAI API (classification), helpdesk tool (ticketing), Slack (routing), email (auto-responses)

**Edge cases to handle:**
- Customer replies to auto-response → update ticket, don't create duplicate
- Multiple issues in one message → create one ticket with tags for each issue
- VIP customer → auto-escalate to senior team regardless of category
- Spam/irrelevant → auto-archive, don't create ticket
- Language detection → route non-English to appropriate team

### Pattern 4: Lead Intake

**Trigger:** New lead arrives (form submission, ad click, referral, manual entry)
**Pipeline:**
```
New lead captured
  → Enrich: company size, industry, location (Clearbit, Apollo, or manual)
  → Score: based on criteria (industry match, company size, budget)
  → Route:
    - Hot leads (score > 80): immediate notification to sales, auto-schedule call
    - Warm leads (score 50-80): add to nurture sequence
    - Cold leads (score < 50): add to newsletter, low-priority follow-up
  → Create CRM contact with all data + score
  → Send appropriate auto-response:
    - Hot: "Let's schedule a call" + Cal.com link
    - Warm: "Thanks for your interest" + relevant resource
    - Cold: "We'll keep you updated" + newsletter opt-in
  → Add to appropriate email sequence
  → Notify assigned sales rep
```

**Key integrations:** Forms/ads (trigger), Clearbit/Apollo (enrichment, optional), CRM (storage), Cal.com (scheduling), email tool (sequences), Slack (notifications)

**Edge cases to handle:**
- Duplicate leads (same email) → merge, update existing contact
- Competitor inquiry (domain match) → flag, don't add to pipeline
- Bot/spam submissions → honeypot field or reCAPTCHA validation
- Incomplete form data → still create lead, tag as "incomplete"
- Lead from existing customer → route to account manager, not sales

### Pattern 5: Reporting / Data Consolidation

**Trigger:** Scheduled (weekly, monthly) or on-demand
**Pipeline:**
```
Report trigger fires (cron or manual)
  → Pull data from Source 1 (CRM — deals, pipeline, activities)
  → Pull data from Source 2 (Accounting — revenue, expenses, AR/AP)
  → Pull data from Source 3 (Ops tool — tickets, completion rates, SLAs)
  → Transform and combine data
  → Calculate KPIs:
    - Revenue this period vs. last period
    - Pipeline value and conversion rates
    - Support metrics (tickets, resolution time, CSAT)
    - Operational metrics (jobs completed, on-time rate)
  → Generate report (Google Docs, PDF, or HTML email)
  → Send to stakeholders
  → Archive in shared drive
```

**Key integrations:** CRM, accounting, ops tools (data sources), Google Sheets/Docs (output), email (distribution)

**Edge cases to handle:**
- API rate limits on data sources → stagger pulls, cache results
- Missing data (source unavailable) → report with available data, flag gaps
- Data format changes (API version update) → version-check at start of workflow
- Large data sets → paginate API calls, process in batches
- Stakeholder list changes → maintain distribution list separately from report logic

---

## Day-by-Day Execution

### DAY 1-2: REQUIREMENTS + WORKFLOW MAPPING (Estimated: 6-8 hours)

#### Step 1: Kickoff Call with SME (60-90 minutes)

Meet with the client's subject matter expert — the person who currently does this task manually.

**Call goals:**
1. Watch them do the process live (screen share). Do NOT skip this. Reading documentation is not the same as watching someone do it.
2. Understand every step, every decision point, every exception
3. Identify what data comes in, what goes out, and what transforms happen in between
4. Learn the "tribal knowledge" — the stuff that's not written down

**Questions to ask the SME:**

- "Can you walk me through this process from start to finish, doing a real one right now?"
- "What do you do when [this step] goes wrong?"
- "How often does [exception X] happen? What do you do?"
- "What's the most annoying part of this process?"
- "What would you never trust a computer to do in this process?" (This defines your human-in-the-loop boundaries)
- "How do you know when this process is done correctly?"
- "Who else touches this process? Do they do it the same way you do?"
- "What happens if this process doesn't get done for a day? A week?"

**Record the call** (with permission). You will reference it during build.

#### Step 2: Map the Workflow (2-3 hours)

Create a detailed workflow map using draw.io, Miro, or Lucidchart.

**Map must include:**
- Every trigger (what starts the process)
- Every step (what happens, in order)
- Every decision point (if X → do Y, else → do Z)
- Every tool/system touched
- Every handoff between people
- Every output (what gets created/updated)
- Every error state (what happens when something fails)
- Human-in-the-loop checkpoints (where human approval is required)

**Color code:**
- Green: will be fully automated
- Yellow: will be semi-automated (human approval step)
- Red: stays manual (can't or shouldn't automate)
- Blue: new capability (doesn't exist today, automation adds it)

#### Step 3: Define Data Schema (1-2 hours)

Document every piece of data that flows through the process:

**Input schema:**
| Field | Source | Type | Required | Example |
|-------|--------|------|----------|---------|
| customer_name | Form/Email | String | Yes | "John Smith" |
| service_type | Form/Email | Enum | Yes | "Repair" / "Install" / "Maintenance" |
| ... | ... | ... | ... | ... |

**Output schema:**
| Field | Destination | Type | Format | Example |
|-------|-------------|------|--------|---------|
| ticket_id | Helpdesk | String | UUID | "TK-20260316-001" |
| assigned_to | Calendar + CRM | String | Name | "Mike Johnson" |
| ... | ... | ... | ... | ... |

**Transformation rules:**
- Input X maps to Output Y because [reason]
- If Input Z is missing, default to [value]
- If Input Z equals [condition], skip step [N]

#### Step 4: Validate with Client (30 minutes)

Send the workflow map and data schema to the SME for confirmation:
- "Does this accurately represent how you do this today?"
- "Did I miss any steps or edge cases?"
- "Are these the right data fields?"

Get written confirmation (email or Slack) before proceeding.

---

### QUALITY CHECKPOINT 1 (End of Day 2)

**Submit to EAS:**

- [ ] Workflow map (visual diagram with color coding)
- [ ] Data schema (input, output, transformations)
- [ ] Edge case inventory (all exceptions identified, with handling plan)
- [ ] Human-in-the-loop checkpoints defined
- [ ] Tool/integration inventory (what needs to connect to what)
- [ ] SME validation confirmation
- [ ] Estimated complexity assessment: "This is a Pattern [1-5] build with [X] custom modifications"

**EAS reviews within 4 hours.**

---

### DAY 3-5: BUILD (Estimated: 12-16 hours)

#### Step 5: Set Up Infrastructure (1-2 hours)

1. Create n8n workflow (or Make scenario) named: `[Client] - [Process Name]`
2. Set up any required accounts:
   - API keys for integrations
   - Webhook endpoints
   - Database/Airtable base (if data storage needed)
3. Create error notification workflow:
   - Any workflow failure → email to you + Slack to EAS
   - Include: workflow name, error message, input data, timestamp
4. Set up test environment:
   - Duplicate production workflow as `[Client] - [Process Name] - TEST`
   - Point test workflow at sandbox/test accounts (not production CRM, not real customers)

#### Step 6: Build Core Pipeline (6-8 hours)

Build the automation step by step, testing each node as you go.

**Build order (regardless of pattern):**

1. **Trigger node:** Set up the entry point (webhook, email trigger, form, schedule)
   - Test: verify trigger fires correctly with sample data

2. **Data extraction/parsing:** Get data from the trigger into a clean, structured format
   - Test: verify all fields are extracted correctly from 5 sample inputs
   - Handle: missing fields, unexpected formats, encoding issues

3. **Validation node:** Check that required data is present and valid
   - If invalid: route to error handling (notify human, don't process)
   - If valid: continue
   - Test: send deliberately bad data, verify it gets caught

4. **Business logic:** Implement the core workflow (routing, calculations, decisions)
   - Match your workflow map step by step
   - Use Switch/IF nodes for decision points
   - Use Code nodes (JavaScript in n8n) for complex transformations
   - Test: run 5 sample inputs through, verify correct routing

5. **Integration nodes:** Connect to external systems (CRM, accounting, calendar, etc.)
   - Test each integration independently first
   - Handle API errors: retry 3 times with exponential backoff, then fail gracefully
   - Handle rate limits: add delays between API calls if needed
   - Test: verify data appears correctly in each connected system

6. **Output/notification nodes:** Send confirmations, notifications, create outputs
   - Test: verify correct people get notified, outputs look right

7. **Error handling:** Add error paths for every node that can fail
   - Principle: every error should result in a notification, never silent failure
   - Log errors to a Google Sheet or Airtable base for review
   - Test: deliberately break each integration, verify error notifications fire

**n8n-specific best practices:**
- Use sticky notes on the canvas to label sections
- Name every node clearly (not "HTTP Request" but "Create HubSpot Contact")
- Use Set nodes to clean/normalize data between steps
- Use Error Trigger nodes, not try/catch in code
- Keep workflows under 30 nodes — if more complex, split into sub-workflows

**Make-specific best practices:**
- Use routers for branching logic
- Set up error handlers on every module
- Use data stores for state that persists between runs
- Set execution limits to prevent runaway scenarios
- Use filters to skip unnecessary processing

#### Step 7: Build Data Validation & Rollback (2-3 hours)

This is what separates a toy automation from a production system.

**Validation rules to implement:**

1. **Input validation:**
   - Required fields present
   - Data types correct (number is number, date is date, email is email)
   - Values within expected range (invoice amount > 0, date not in the past, etc.)
   - No duplicate processing (check if this input was already processed)

2. **Output validation:**
   - CRM entry was actually created (verify with a read-back API call)
   - Email was actually sent (check send status)
   - Calendar event was actually created (verify)
   - Document was actually generated (check file exists)

3. **Rollback capability:**
   - If step 5 fails after steps 1-4 succeeded, can you undo steps 1-4?
   - At minimum: log what was done so a human can undo it manually
   - At best: automated rollback (delete created records, revert status changes)
   - Document rollback procedures in the runbook

4. **Idempotency:**
   - If the same input runs twice, it should not create duplicates
   - Use unique identifiers (invoice number, email message ID, form submission ID)
   - Check for existing records before creating new ones

#### Step 8: Build Monitoring (1-2 hours)

Every Ops Pilot gets a monitoring layer:

1. **Execution log:** Every run logged to Google Sheet or Airtable
   - Columns: timestamp, trigger_type, input_summary, outcome (success/fail/partial), duration, errors
2. **Daily summary:** Cron workflow that sends daily stats
   - Total runs, success rate, failure rate, average duration, errors to investigate
3. **Alert threshold:** If error rate exceeds 10% in a day → immediate notification to EAS + client

---

### DAY 6-7: TEST (Estimated: 6-8 hours)

#### Step 9: Execute Test Runs (4-5 hours)

Run 20 test cases through the automation. Use the client's sample data (provided during pre-requisites) plus synthetic edge cases you create.

**Test matrix:**

| Category | # Tests | What to Test |
|----------|---------|-------------|
| Happy path (normal inputs) | 8 | Standard inputs that should process successfully |
| Missing data | 3 | Required field missing, optional field missing, all optional fields missing |
| Bad data | 3 | Wrong data types, out-of-range values, special characters |
| Duplicates | 2 | Same input submitted twice, similar-but-different inputs |
| Edge cases | 2 | Unusual but valid inputs (very long text, large numbers, unicode) |
| Integration failure | 2 | CRM API down (simulate by using wrong credentials), email service timeout |

**For each test, record:**

| Test # | Input Summary | Expected Result | Actual Result | Pass/Fail | Notes |
|--------|--------------|-----------------|---------------|-----------|-------|
| 1 | Standard invoice, $500, Vendor A | Logged to QuickBooks, notification sent | ... | ... | ... |

**Pass threshold:** 18/20 tests must pass. All 8 happy-path tests must pass. Fix all failures and re-test.

#### Step 10: Fix Issues (1-2 hours)

1. Fix all failing tests
2. Re-test each fix with at least 2 test cases
3. Update workflow documentation with any changes made
4. Add any new edge cases discovered to the runbook

#### Step 11: Load/Stress Test (30 minutes, if applicable)

If the workflow will process high volume (50+ items/day):

1. Feed 50 items through in rapid succession
2. Verify: no items dropped, no duplicates, no race conditions
3. Verify: API rate limits handled gracefully (retries work, don't lose data)
4. Measure: average processing time per item, total throughput capacity
5. Document capacity limits in the runbook ("This workflow can handle X items per hour")

---

### QUALITY CHECKPOINT 2 (End of Day 7)

**Submit to EAS:**

- [ ] Test results for all 20 test cases (spreadsheet with results)
- [ ] List of issues found and fixes applied
- [ ] Edge cases documented and handled
- [ ] All workflows tested and passing (screenshot of n8n/Make execution logs showing green)
- [ ] Integration verification (screenshots of data appearing correctly in connected systems)
- [ ] Load test results (if applicable)
- [ ] Monitoring/logging working (screenshot of execution log)
- [ ] Rollback procedures documented

**EAS reviews within 4 hours.**

---

### DAY 8-9: LAUNCH (Estimated: 6-8 hours)

#### Step 12: Shadow Mode Launch (Day 8, 3-4 hours)

Shadow mode = automation runs in parallel with the human process. Both happen. Results are compared.

1. Enable the automation in production (real triggers, real data)
2. Tell the SME: "Keep doing the process manually like normal. The automation will run alongside you. At the end of today, we'll compare results."
3. Monitor every execution in real time:
   - Is the automation producing the same output as the human?
   - Are there any discrepancies?
   - Are there inputs the automation handles that the human would miss?
4. End of Day 8: compare results side by side
   - Create a comparison table: Human Result vs. Automation Result for each item
   - Identify and fix any discrepancies
   - If accuracy is below 95%: stay in shadow mode for Day 9, fix issues overnight

**Why shadow mode matters:** It catches issues that testing doesn't. Real production data is messier, more varied, and more creative than test data. Shadow mode is your safety net.

#### Step 13: Live Mode Launch (Day 9, 2-3 hours)

If shadow mode results are clean (95%+ match):

1. Disable the manual process (with client approval — verbal + written confirmation)
2. Enable the automation as the primary handler
3. Keep the SME available as backup for the first day
4. Monitor every execution for the first 4 hours
5. Adjust anything that needs adjusting based on live data
6. At end of Day 9: send client Day 1 performance summary

If shadow mode results are NOT clean:
- Stay in shadow mode for Day 9
- Fix all discrepancies
- Day 10 becomes your live launch day (handoff may extend by 1 day — notify EAS)

#### Step 14: Train Client Team (1-2 hours)

Schedule a 30-minute training call with the SME and their manager.

**Training agenda:**

1. **What the automation does** (5 min)
   - Walk through the workflow diagram
   - Show: trigger → process → output
   - Show: what happens when something goes wrong

2. **How to monitor it** (5 min)
   - Where to find the execution log
   - What the daily summary email tells them
   - What "green" vs. "red" means

3. **How to handle exceptions** (10 min)
   - What gets flagged for human review (and where to find it)
   - How to approve/reject items in the approval queue (if applicable)
   - How to manually process an item that the automation couldn't handle

4. **How to make changes** (5 min)
   - What they can change themselves (e.g., update a Google Sheet lookup table)
   - What requires EAS help (e.g., adding a new integration, changing logic)
   - How to request changes

5. **Support and escalation** (5 min)
   - P0/P1/P2 definitions and response times
   - How to contact EAS
   - When to contact EAS vs. troubleshoot themselves

Record the training call. Include in runbook.

---

### DAY 10: HANDOFF (Estimated: 4-5 hours)

#### Step 15: Compile Runbook (2-3 hours)

Client-facing runbook with everything needed to maintain the system.

**Runbook structure:**

1. **System Overview**
   - What this automation does (1 paragraph)
   - Architecture diagram (tools, data flow, integration points)
   - Accounts and credentials (reference client's password manager — never put credentials in the doc)

2. **Workflow Details**
   - n8n/Make workflow name and location
   - Every node explained (what it does, what it connects to)
   - Decision logic documented (if X → Y, else → Z)
   - Variables and configuration values (what to change for different settings)

3. **Data Schema**
   - Input format and required fields
   - Output format and where data goes
   - Transformation rules

4. **Monitoring**
   - Where to find execution logs
   - What the daily summary report contains
   - Alert thresholds and what they mean

5. **Exception Handling**
   - Common errors and how to resolve them
   - Where flagged items go for human review
   - How to re-run a failed execution
   - How to manually process an item

6. **Making Changes**
   - How to update lookup tables / reference data
   - How to add a new routing rule
   - How to change notification recipients
   - What changes require developer help

7. **Rollback**
   - How to disable the automation (emergency shutoff)
   - How to revert to manual process
   - How to undo automated actions (if possible)

8. **Troubleshooting**

   | Symptom | Likely Cause | Fix |
   |---------|-------------|-----|
   | Automation stopped running | Trigger disconnected, n8n down | Check n8n status, re-activate trigger |
   | Duplicate entries in CRM | Dedup check failed, re-run of same input | Check for duplicate, merge or delete |
   | Wrong routing | Decision logic needs update | Review Switch node conditions |
   | API error from [tool] | Credentials expired, rate limit, API change | Renew credentials, check API docs |
   | Slow processing | Large batch, API throttling | Check queue, verify rate limit handling |

9. **Support Contacts**
   - EAS support email/Slack
   - Tool-specific support links

#### Step 16: Set Up Telemetry Dashboard (1 hour)

Create a monitoring view the client can access.

**Dashboard metrics:**

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Total items processed | Execution log count | Match expected volume |
| Success rate | Successful / Total | > 95% |
| Error rate | Errors / Total | < 5% |
| Average processing time | Mean execution duration | < [benchmark from testing] |
| Human intervention rate | Flagged items / Total | < 10% |
| Time saved per day | (Items processed x manual time per item) - (Items x automated time) | Report monthly |
| Cost saved per month | Time saved x hourly rate | Report monthly |

**Implementation options:**
- Google Sheet with n8n daily update (simplest, recommended)
- Airtable dashboard view (good for clients who already use Airtable)
- n8n built-in execution history (technical, for power users)

#### Step 17: Final Delivery (1 hour)

1. Send runbook (PDF + editable doc)
2. Send dashboard access
3. Schedule 2-week check-in call
4. Send handoff email:

> Subject: Your [Process Name] Automation is Live
>
> Hi [Name],
>
> Your [process name] automation is now running in production. Here's everything you need:
>
> - **Runbook:** [link] — Complete system documentation
> - **Dashboard:** [link] — Daily performance metrics
> - **Training recording:** [link] — Team training session replay
>
> Performance from the first [X] days:
> - [X] items processed automatically
> - [X]% success rate
> - Estimated [X] hours saved per week
> - Estimated $[X] saved per month
>
> I've scheduled a check-in for [date] to review performance and discuss any adjustments.
>
> For any issues, reach out to [EAS support contact].
>
> Best,
> [Your name]

---

### QUALITY CHECKPOINT 3 (Day 10, before handoff)

**Submit to EAS:**

- [ ] Runbook document (complete)
- [ ] Dashboard/telemetry access (link or screenshot)
- [ ] Shadow mode comparison data (human vs. automation results)
- [ ] Live mode performance data (success rate, error rate, items processed)
- [ ] Training recording link
- [ ] Client handoff email draft
- [ ] Known limitations or edge cases not yet handled (be honest)
- [ ] Rollback plan documented and tested

**EAS reviews within 4 hours. Go/no-go for client handoff.**

---

## Post-Delivery

1. Log completion in EAS project tracker
2. Note: success rate, volume processed, time saved, client satisfaction
3. Flag upsell opportunities:
   - Client wants another process automated → second Ops Pilot ($4,500)
   - Client wants ongoing management → Managed Ops ($1,500-$3,000/mo)
   - Client wants phone system → Phone Pilot ($3,500)
4. Transfer all credentials/access to EAS vault
5. Attend 2-week check-in call, then hand off fully

---

## Common Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|----------------|--------------|
| Automating the wrong process | Client picked their "favorite" process instead of highest-ROI | Refer back to Signal Map scoring. Push back if the chosen process has low priority score. |
| Skipping shadow mode | "Tests passed, let's go live" | Shadow mode catches things tests don't. Real data is always messier. Never skip it. |
| No rollback plan | Assumed everything would work | Always document how to turn it off and go back to manual. Test the rollback before go-live. |
| Silent failures | Error handling not thorough enough | Every node that can fail must have an error handler. Every error must produce a notification. |
| Over-automating | Automating steps that should stay manual (judgment calls, exceptions) | If the SME says "I have to think about this one" — that step stays human. Add an approval node. |
| Not involving the SME enough | Building based on documentation alone | The SME knows things nobody wrote down. Watch them do it live. Have them test your automation. |
| Scope creep during build | "While you're in there, can you also..." | Scope is defined in the SOW. New requests go into a backlog for a future engagement. Say: "That's a great idea for phase 2." |
| Fragile integrations | Hardcoded values, no error handling | Use variables for everything. Handle API errors with retries. Build for the API being down, not just up. |
| No monitoring | "It's working, we're done" | If you can't see it running, you can't see it failing. Monitoring is required, not optional. |
| Training too technical | Showing the SME your n8n canvas | Train on WHAT it does, not HOW it's built. Show them the monitoring dashboard, not the workflow editor. Unless they're technical and want to see it. |

---

## Time Budget Summary

| Activity | Estimated Hours | Day |
|----------|----------------|-----|
| Kickoff call with SME | 1.5 hrs | 1 |
| Workflow mapping | 2-3 hrs | 1-2 |
| Data schema definition | 1-2 hrs | 2 |
| Client validation | 0.5 hrs | 2 |
| Checkpoint 1 submission | 0.5 hrs | 2 |
| Infrastructure setup | 1-2 hrs | 3 |
| Core pipeline build | 6-8 hrs | 3-5 |
| Data validation + rollback | 2-3 hrs | 5 |
| Monitoring setup | 1-2 hrs | 5 |
| Test runs (20 cases) | 4-5 hrs | 6-7 |
| Fix issues + re-test | 1-2 hrs | 7 |
| Load test (if applicable) | 0.5 hrs | 7 |
| Checkpoint 2 submission | 0.5 hrs | 7 |
| Shadow mode launch + monitoring | 3-4 hrs | 8 |
| Live mode launch + monitoring | 2-3 hrs | 9 |
| Client team training | 1-2 hrs | 9 |
| Runbook compilation | 2-3 hrs | 10 |
| Telemetry dashboard setup | 1 hr | 10 |
| Final delivery + handoff email | 1 hr | 10 |
| Checkpoint 3 submission | 0.5 hrs | 10 |
| **Total** | **35-47 hrs** | **10 days** |

---

## Escalation

- **SME unavailable:** If the client's subject matter expert is unresponsive for 24+ hours, notify EAS immediately. The build depends on SME access for validation and shadow mode.
- **Integration blocked:** If a required API doesn't support what you need (no endpoint, broken docs, auth issues), notify EAS within 4 hours. Propose a workaround (e.g., Google Sheets as intermediate layer, manual import/export as bridge).
- **Data quality issues:** If the client's data is too messy to automate reliably (e.g., no consistent format, missing critical fields), document the issues and propose a "data cleanup" prerequisite step. This may require scope adjustment — notify EAS.
- **Shadow mode fails repeatedly:** If after 2 days of shadow mode the automation still doesn't match manual results above 90%, escalate to EAS. The process may be more complex than scoped, requiring a larger engagement.
- **Client wants to change the target process mid-project:** Redirect to EAS. This is a scope change that requires SOW amendment.
