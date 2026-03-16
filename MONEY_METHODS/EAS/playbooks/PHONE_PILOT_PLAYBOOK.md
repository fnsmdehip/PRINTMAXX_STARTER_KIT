# Phone Pilot Delivery Playbook

**How to deliver the AI Phone Concierge in 10 days**

---

## Overview

The Phone Pilot replaces or augments a client's phone handling with an AI voice agent. Inbound calls are answered by Retell AI, routed based on intent, logged to the client's CRM, and escalated to humans when needed. The result is near-zero missed calls, 24/7 availability, and every call logged automatically.

**Package price:** $3,500
**Your payout:** $2,450 total (30/40/30 milestone split)
**Timeline:** 10 business days from kickoff
**Effort estimate:** 30-40 hours of actual work

---

## Payment Milestones

| Milestone | Trigger | Amount |
|-----------|---------|--------|
| M1 (30%) | SOW signed, kickoff confirmed | $735 |
| M2 (40%) | Quality Checkpoint 2 approved by EAS | $980 |
| M3 (30%) | Client accepts final deliverable + 3-day live period passes | $735 |

---

## Pre-Requisites Checklist

- [ ] Signal Map completed for this client (or equivalent discovery — you need workflow data)
- [ ] Client SOW signed and countersigned
- [ ] Client has provided:
  - [ ] Business phone number (or confirmed they can set up call forwarding)
  - [ ] Current call scripts, IVR menus, or phone tree documentation
  - [ ] CRM access (HubSpot, Salesforce, or equivalent — read/write credentials)
  - [ ] Escalation contacts: names, phone numbers, roles, availability windows
  - [ ] After-hours handling preferences (voicemail, SMS, email, or combination)
  - [ ] Top 10 FAQs their callers ask (or access to call recordings to extract these)
- [ ] You have a Retell AI account (retellai.com — sign up, 100 free calls/day on trial)
- [ ] You have an n8n instance running (self-hosted or n8n.cloud) OR Make/Zapier account
- [ ] You have access to EAS project tracker

**Tool selection guidance:**
- **n8n** (preferred): Self-hosted, no per-operation costs, full control. Use for clients who will have high call volume or complex routing.
- **Make**: Good middle ground. Use for clients who want a managed platform and have moderate volume.
- **Zapier**: Use only for very simple integrations or clients already on Zapier. Most expensive per-operation.

---

## Day-by-Day Execution

### DAY 1-2: SETUP (Estimated: 6-8 hours)

#### Step 1: Configure Retell AI Account (1-2 hours)

1. Log into retellai.com and create a new "pathway" for this client
2. Select voice:
   - Professional female: use for medical, legal, hospitality
   - Professional male: use for trades, construction, automotive
   - Avoid: overly casual voices, accented voices unless client requests, robotic/monotone options
   - Test 3-4 voice options by making test calls to yourself. Pick the one that sounds most natural for the client's industry.
3. Set base configuration:
   - Language: English (or client's preference)
   - Max call duration: 5 minutes (adjustable — most business calls resolve in 2-3 min)
   - Interruption sensitivity: Medium (allows caller to interrupt without cutting them off)
   - End-of-speech detection: 1.5 seconds (prevents premature responses)
   - Transfer number: client's main line or designated escalation number
   - Voicemail detection: Enabled (skip voicemail boxes, log as missed)

#### Step 2: Write Call Scripts (2-3 hours)

Write scripts for every call scenario. Each script is a Retell AI pathway node.

**Script 1 — Greeting:**
```
"Thank you for calling [Business Name]. This is [AI Name — optional, or just skip the name].
How can I help you today?"
```
Keep it short. No "Your call is important to us" filler.

**Script 2 — FAQ Handling (Top 10):**
For each FAQ, create a pathway branch:
```
Intent: [e.g., "What are your hours?"]
Response: "[Business Name] is open Monday through Friday, 8 AM to 6 PM,
and Saturday 9 AM to 2 PM. We're closed on Sundays.
Is there anything else I can help you with?"
```

Build these from the client's FAQ list. If they don't have one, pull from:
- Their website FAQ page
- Google Business listing Q&A
- Signal Map discovery notes
- Common industry questions (e.g., dental: insurance, emergency appointments; HVAC: service area, emergency rates; legal: consultation fees, practice areas)

**Script 3 — Appointment Booking:**
```
"I'd be happy to help you schedule an appointment. Let me check availability.
What day works best for you?"
[Integrate with Cal.com or client's scheduler — see Step 3]
"I have [time slot] available on [date]. Shall I book that for you?"
[Confirm: name, phone, email, reason for visit]
"You're all set for [date] at [time]. You'll receive a confirmation email shortly.
Is there anything else?"
```

**Script 4 — Routing/Escalation:**
Define which intents trigger human escalation:
- Angry/upset caller → immediate transfer to manager
- Complex technical question → transfer to specialist
- Billing dispute → transfer to billing
- Emergency (if applicable — medical, HVAC, plumbing) → transfer to on-call

```
"Let me connect you with [role] who can help you with that.
One moment please."
[Transfer to designated number]
[If no answer after 30 seconds]: "I apologize, [role] isn't available right now.
Can I take your information and have them call you back within [timeframe]?"
```

**Script 5 — After-Hours:**
```
"Thank you for calling [Business Name]. Our office is currently closed.
Our hours are [hours].

I can help you with a few things right now:
- If you'd like to schedule an appointment, I can do that.
- If you have a question, I may be able to answer it.
- If you need to speak with someone urgently, I can send a message to our team.

How would you like to proceed?"
```

After-hours handling:
- Appointment booking: still works (Cal.com integration runs 24/7)
- FAQ: still works
- Urgent message: capture name, number, brief description → send SMS to on-call + email to office

**Script 6 — Callback Request:**
```
"I'll have someone call you back. Can I get your name and the best number to reach you?
And briefly, what is this regarding?

[Capture: name, phone, topic]

"Got it. Someone from [Business Name] will call you back within [timeframe].
Is there anything else?"
```

**Variable handling:** Never hardcode client-specific values into scripts. Use Retell AI variables:
- `{{business_name}}` — set per pathway
- `{{business_hours}}` — set per pathway
- `{{escalation_number}}` — set per pathway
- `{{callback_timeframe}}` — set per pathway

This makes scripts reusable across clients with minimal changes.

#### Step 3: Set Up n8n/Make Workflow (2-3 hours)

Build the automation pipeline that processes calls after they happen.

**Workflow architecture:**

```
Retell AI Call Completed
    ↓ (webhook POST)
n8n Webhook Node
    ↓
Parse Call Data
  - Caller phone number
  - Call duration
  - Transcript
  - Intent classification (from Retell AI)
  - Outcome (resolved, escalated, callback requested, voicemail)
    ↓
Route by Outcome:
  ├── Resolved → Log to CRM + done
  ├── Escalated → Log to CRM + SMS to escalation contact + Slack notification
  ├── Callback → Log to CRM + create task for callback + SMS notification
  └── After-hours → Log to CRM + queue for morning follow-up + SMS if urgent
    ↓
CRM Integration (all paths):
  - Search for existing contact by phone number
  - If found: update contact, add call note with transcript summary
  - If not found: create new contact, add call note
  - Tag contact: "AI Call - [date]"
    ↓
Notifications (where applicable):
  - SMS via Twilio: "[Business Name]: New [escalation/callback] from [caller name] at [phone]. Topic: [summary]"
  - Slack: #calls channel (if client uses Slack)
  - Email: daily digest (batched, not per-call)
```

**n8n specific setup:**
1. Create new workflow named: `[Client] - Phone Pilot`
2. Node 1: Webhook (POST) — copy the webhook URL, paste into Retell AI pathway settings
3. Node 2: Set node — extract and normalize call data fields
4. Node 3: Switch node — route by call outcome
5. Node 4+: CRM nodes (HubSpot, Salesforce, or HTTP Request for other CRMs)
6. Node 5+: Twilio SMS node (for notifications)
7. Node 6: Slack node (optional)
8. Error handling: add Error Trigger workflow that sends you an email if any workflow execution fails

**CRM-specific integration notes:**

*HubSpot:*
- Use HubSpot node in n8n (built-in)
- API key: client provides from Settings → Integrations → API Key
- Contact search: by phone number
- Activity logging: create "Call" engagement with transcript in notes

*Salesforce:*
- Use Salesforce node in n8n (built-in, requires OAuth)
- Client provides: Connected App credentials (Client ID, Client Secret)
- Contact search: SOQL query by phone
- Activity logging: create Task or log Call Activity

*Other CRMs:*
- Use HTTP Request node with the CRM's REST API
- Most CRMs have: search contacts, create contacts, create activities/notes
- Document the API endpoints you use in the runbook

#### Step 4: Set Up SMS Notifications (30 minutes)

1. Create Twilio account (if EAS doesn't have a shared one — ask EAS first)
2. Get a Twilio phone number (local to client's area code preferred)
3. Configure n8n Twilio node with Account SID + Auth Token
4. Test: send yourself a test SMS through the workflow

---

### QUALITY CHECKPOINT 1 (End of Day 2)

**Submit to EAS:**

- [ ] Call script drafts — all 6 scenarios written out
- [ ] n8n/Make workflow diagram (screenshot of the workflow canvas)
- [ ] CRM integration plan: which CRM, what data gets logged, what fields
- [ ] Escalation tree diagram: visual showing which intents route where
- [ ] Retell AI voice selection (which voice, why)
- [ ] Variable list (all {{variables}} used in scripts)

**EAS reviews within 4 hours.**

---

### DAY 3-5: BUILD (Estimated: 10-14 hours)

#### Step 5: Implement Retell AI Pathways (3-4 hours)

1. Build out the full pathway in Retell AI's pathway editor
2. Configure every node with the scripts from Step 2
3. Set up intent detection:
   - Retell AI uses AI-native intent detection — define your intents as pathway branches
   - Test each branch by saying the trigger phrases out loud
4. Set global fallback: if AI can't classify the intent → offer transfer to human
5. Configure transfer settings:
   - Warm transfer (AI stays on line): use for escalations where context matters
   - Cold transfer (AI drops off): use for simple routing
6. Set business hours logic:
   - During hours: full menu (FAQ, booking, routing, escalation)
   - After hours: limited menu (FAQ, booking, urgent message, callback)

#### Step 6: Build n8n/Make Workflows (4-6 hours)

Implement the full workflow from the diagram in Step 3.

**Pipeline 1: Call Handling → CRM Logging**
- Trigger: Retell AI webhook
- Process: parse transcript, classify outcome, search/create CRM contact, log call
- Test: manually trigger with sample webhook payload

**Pipeline 2: Escalation Notifications**
- Trigger: call outcome = "escalated"
- Process: SMS to escalation contact, Slack message (if applicable), email to office manager
- Include in SMS: caller name, phone, reason, 1-sentence summary
- Test: trigger escalation scenario, verify SMS arrives

**Pipeline 3: After-Hours Handling**
- Trigger: call outcome = "after_hours_message"
- Process: log to CRM, create follow-up task for next business morning, SMS to on-call if urgent
- Urgent = keywords: "emergency," "urgent," "broken," "flooding," "pain" (customize per industry)
- Test: trigger after-hours call, verify task creation

**Pipeline 4: Daily Digest**
- Trigger: cron (every day at 8 AM client's timezone)
- Process: query yesterday's calls from CRM, summarize (total calls, AI-resolved, escalated, callbacks pending, missed)
- Output: email to client (formatted HTML email or Slack message)
- Template:
  ```
  Daily Call Summary — [Date]

  Total calls: XX
  AI resolved: XX (XX%)
  Escalated to team: XX
  Callbacks pending: XX
  After-hours calls: XX
  Average call duration: X:XX

  Top caller intents:
  1. [Intent] — XX calls
  2. [Intent] — XX calls
  3. [Intent] — XX calls

  Action items:
  - [X callbacks need follow-up today]
  - [Y escalations unresolved from yesterday]
  ```

#### Step 7: Connect CRM (2-3 hours)

1. Get API credentials from client (or have client generate them during a screen share)
2. Test connection: read a contact, create a test contact, delete it
3. Map fields:
   - Retell AI → CRM field mapping:
     - `caller_phone` → CRM Phone
     - `caller_name` (if captured) → CRM Name
     - `call_transcript_summary` → CRM Call Note
     - `call_duration` → CRM Call Duration
     - `call_outcome` → CRM Custom Field or Tag
     - `call_date` → CRM Activity Date
4. Handle duplicates: always search before creating. Match on phone number.
5. Handle edge cases:
   - No caller ID: log as "Unknown Caller" with timestamp
   - Multiple contacts with same phone: update most recently modified
   - CRM rate limits: add 1-second delay between API calls in n8n

#### Step 8: Configure Call Forwarding (1 hour)

Work with the client to set up forwarding from their business number to the Retell AI number.

**Options (depends on client's phone provider):**
- **Simple forwarding:** Client's provider settings → forward all calls to Retell AI number
- **Conditional forwarding:** Forward only when busy/no answer (keeps some calls human)
- **Porting:** Move the number to a SIP provider that can split traffic (advanced — only if needed)
- **Google Voice / RingCentral / Dialpad:** These all have forwarding settings in their admin panels

**Important:** Do not port the client's phone number away from their provider without explicit written approval. Forwarding is always safer and reversible.

Document the forwarding setup in the runbook so it can be reversed.

---

### QUALITY CHECKPOINT 2 (End of Day 7)

This checkpoint covers both Build (Days 3-5) and Test (Days 6-7).

---

### DAY 6-7: TEST (Estimated: 6-8 hours)

#### Step 9: Execute Test Calls (4-5 hours)

Run 20 test calls across all scenarios. Use a personal phone (not the Retell AI number) to call in. If possible, have a second person help (different voice, different phone number).

**Test matrix:**

| # | Scenario | What to Say | Expected Result |
|---|----------|-------------|-----------------|
| 1 | General inquiry — hours | "What time do you open?" | AI answers correctly, logs to CRM |
| 2 | General inquiry — location | "Where are you located?" | AI answers correctly, logs to CRM |
| 3 | General inquiry — services | "Do you do [specific service]?" | AI answers correctly, logs to CRM |
| 4 | General inquiry — pricing | "How much does [service] cost?" | AI gives range or offers callback |
| 5 | General inquiry — insurance/payment | "Do you accept [insurance/payment]?" | AI answers or routes appropriately |
| 6 | Appointment booking — standard | "I'd like to schedule an appointment" | AI books via Cal.com, confirms, CRM updated |
| 7 | Appointment booking — specific date | "Can I come in Thursday at 2?" | AI checks availability, books or offers alternatives |
| 8 | Appointment booking — reschedule | "I need to move my appointment" | AI handles or routes to human |
| 9 | Appointment booking — cancel | "I need to cancel" | AI handles or routes to human |
| 10 | Appointment booking — after hours | "I want to book for next week" (call after hours) | AI books, confirms, after-hours flow works |
| 11 | Escalation — angry caller | "This is unacceptable, I need to speak to a manager" | AI transfers to escalation contact, SMS sent |
| 12 | Escalation — complex question | "I have a complicated situation with [technical topic]" | AI offers transfer, routes correctly |
| 13 | Escalation — billing | "I have a question about my bill" | AI routes to billing contact |
| 14 | After-hours — general | Call after configured hours | After-hours greeting plays, limited menu offered |
| 15 | After-hours — urgent | "This is urgent, I need help now" | AI captures info, SMS to on-call immediately |
| 16 | After-hours — callback | "Can someone call me tomorrow?" | AI captures info, task created for morning |
| 17 | Edge — confused caller | Mumble, ask vague questions, change topic | AI asks clarifying questions, eventually offers transfer |
| 18 | Edge — angry caller | Yell, express frustration, demand manager | AI de-escalates, offers transfer quickly |
| 19 | Edge — wrong number | "Is this [wrong business name]?" | AI clarifies business name, offers help or politely ends |
| 20 | Callback request | "Can you have [role] call me back?" | AI captures info, notification sent, CRM task created |

**QA Rubric — score each call:**

| Criteria | Pass/Fail | Notes |
|----------|-----------|-------|
| Greeting correct (business name, professional tone) | | |
| Intent correctly identified | | |
| Response accurate and helpful | | |
| Routing/escalation correct | | |
| CRM entry created/updated | | |
| CRM data accurate (phone, name, notes) | | |
| Escalation SMS/notification sent (if applicable) | | |
| Transcript readable and coherent | | |
| Call ended appropriately | | |
| No awkward pauses > 3 seconds | | |

**Pass threshold:** 18/20 calls must pass all criteria. Fix all failures and re-test those specific scenarios.

#### Step 10: Fix and Document (1-2 hours)

1. Fix all issues found during testing
2. Re-test fixed scenarios (at least 2 calls per fix)
3. Document edge cases discovered:
   - New intents you didn't anticipate
   - Phrasing variations that confused the AI
   - Scenarios that need human handling (add to escalation rules)
4. Update call scripts based on test results
5. Update n8n workflows if any routing was wrong

#### Step 11: Load Test (30 minutes, if applicable)

If the client expects high call volume (50+ calls/day):
- Use Retell AI's batch call feature to simulate 10 simultaneous calls
- Verify n8n webhook processes all calls (check for dropped webhooks)
- Verify CRM doesn't rate-limit (add delays if needed)
- Verify SMS notifications don't get throttled by Twilio

---

### QUALITY CHECKPOINT 2 (End of Day 7)

**Submit to EAS:**

- [ ] QA rubric results for all 20 test calls (spreadsheet or table)
- [ ] List of issues found and fixes applied
- [ ] Edge cases documented (new intents, escalation rules added)
- [ ] All n8n workflows tested and passing (screenshot of successful executions)
- [ ] CRM integration verified (screenshot of test contact with call logs)
- [ ] SMS notification verified (screenshot of received test SMS)
- [ ] Load test results (if applicable)

**EAS reviews within 4 hours.**

---

### DAY 8-9: LAUNCH (Estimated: 6-8 hours)

#### Step 12: Go Live with Split Routing (2-3 hours)

**Day 8 morning:**
1. Configure 50/50 call split:
   - Option A (preferred): Set call forwarding to ring Retell AI number after 3 rings (no answer forwarding). Human answers first if available, AI catches overflow.
   - Option B: Time-based split — AI handles mornings, human handles afternoons (or reverse)
   - Option C: Manual toggle — client manually enables/disables forwarding as needed
2. Notify client team: "The AI phone system goes live today. Here's what to expect: [1-paragraph summary]"
3. Confirm escalation contacts are available and have received test SMS

**Day 8, first 4 hours:**
- Monitor every single call that comes in
- Check each CRM entry against the call transcript
- Verify escalations triggered correctly
- Note any new intents or edge cases
- Fix issues in real-time (script tweaks, routing adjustments)

**Day 8, end of day:**
- Send client a summary of Day 1 performance
- Include: total calls, AI-handled, escalated, any issues found and fixed
- Ask: "How did it feel on your end? Any calls that didn't go well?"

#### Step 13: Adjust and Optimize (2-3 hours)

**Day 9:**
1. Review all Day 8 calls:
   - Read transcripts for any AI responses that felt off
   - Check CRM entries for accuracy
   - Identify patterns: most common intents, most common escalation reasons
2. Update call scripts based on real data:
   - New FAQ answers (callers asked questions you didn't anticipate)
   - Better phrasing (reword any responses that confused callers)
   - New routing rules (if a common intent kept getting escalated unnecessarily)
3. Increase AI call percentage (with client approval):
   - Day 8: 50% AI
   - Day 9: 75% AI
   - Day 10+: 100% AI (or whatever the client is comfortable with)

#### Step 14: Train Client Team (1-2 hours)

Schedule a 30-minute video call with the client's team (anyone who will interact with the system).

**Training agenda:**

1. **How to access call logs and transcripts** (5 min)
   - Where to find them in CRM
   - How to read the AI-generated call summary
   - How to listen to call recordings (if Retell AI recording is enabled)

2. **How to update FAQ answers** (5 min)
   - Where the scripts live (Retell AI dashboard)
   - How to edit a response (show them the pathway editor)
   - When to ask EAS for help vs. doing it themselves

3. **How to add new escalation rules** (5 min)
   - How to add a new intent to the pathway
   - How to change who gets escalated calls
   - How to update escalation phone numbers

4. **Understanding the daily digest** (5 min)
   - What each metric means
   - What to look for (increasing escalation rate = new training needed)
   - How to flag issues

5. **When and how to contact EAS for support** (5 min)
   - What counts as P0/P1/P2 (reference SLA if on managed plan)
   - Contact method (email, Slack, phone)
   - Expected response times

Record the training call (with permission) and include the recording link in the runbook.

---

### DAY 10: HANDOFF (Estimated: 4-5 hours)

#### Step 15: Compile Runbook (2-3 hours)

Create the client-facing runbook document. This is different from the playbook — the runbook is what the client (or a future contractor) uses to maintain the system.

**Runbook structure:**

1. **System Overview**
   - Architecture diagram (what talks to what)
   - List of all tools and accounts used
   - Login credentials (stored in client's password manager, not in the document)

2. **Retell AI Configuration**
   - Pathway name and ID
   - Voice settings
   - All call scripts (current versions)
   - Variable values
   - Transfer/escalation numbers

3. **n8n/Make Workflows**
   - Workflow names and IDs
   - What each workflow does (1-sentence description)
   - Webhook URLs
   - Trigger conditions
   - Error handling behavior

4. **CRM Integration**
   - Which fields are mapped
   - How contacts are searched/created
   - How call notes are formatted
   - Custom fields or tags created

5. **How to Update**
   - Change FAQ answer: step-by-step with screenshots
   - Add new FAQ: step-by-step with screenshots
   - Change escalation contact: step-by-step
   - Change business hours: step-by-step
   - Update greeting: step-by-step

6. **Troubleshooting**
   | Symptom | Likely Cause | Fix |
   |---------|-------------|-----|
   | Calls not being answered by AI | Call forwarding disabled | Re-enable forwarding in phone provider settings |
   | CRM entries not appearing | n8n workflow failed | Check n8n execution log, re-run failed execution |
   | SMS notifications not sending | Twilio balance depleted | Add funds to Twilio account |
   | AI giving wrong answers | Script needs update | Update pathway in Retell AI dashboard |
   | Caller complains about long pause | Retell AI latency | Check Retell AI status page; increase end-of-speech detection |

7. **Contact & Support**
   - EAS support email/Slack
   - Retell AI support
   - n8n community/support
   - Twilio support

#### Step 16: Set Up Monitoring Dashboard (1 hour)

Create a monitoring view the client can access:

**Option A — n8n dashboard (preferred for n8n users):**
- Create a summary workflow that runs daily
- Outputs: Google Sheet or Notion database with daily metrics
- Share with client

**Option B — Google Sheet dashboard:**
- Create a Google Sheet with tabs: Daily Calls, Weekly Summary, Monthly Summary
- n8n workflow appends data daily
- Share with client (view-only)

**Option C — Simple email report:**
- Daily digest email (already built in Step 6)
- Weekly summary email (add a weekly cron workflow)

**Metrics to track:**

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Total calls handled by AI | Count from Retell AI API | Baseline + growth |
| AI resolution rate | Resolved / Total calls | > 70% |
| Escalation rate | Escalated / Total calls | < 20% |
| Average call duration | From Retell AI call data | 1-3 minutes |
| CRM entries created | Count from CRM API | Should match total calls |
| Missed calls (AI didn't answer) | Calls to business number not forwarded | < 5% |
| Callback completion rate | Callbacks completed / Callbacks requested | > 90% within 24 hours |
| After-hours calls handled | After-hours calls / Total | Track trend |

#### Step 17: Final Delivery (1 hour)

1. Send runbook to client (PDF + editable Google Doc)
2. Send dashboard access link
3. Schedule 2-week check-in call (15-30 min, calendar invite)
4. Send handoff email:

> Subject: Your AI Phone Concierge is Live
>
> Hi [Name],
>
> Your AI phone system is now handling calls. Here's everything you need:
>
> - **Runbook:** [link] — How everything works, how to make changes, troubleshooting
> - **Dashboard:** [link] — Daily metrics on call performance
> - **Training recording:** [link] — Replay of the team training session
>
> The system is currently handling [X]% of your inbound calls. Based on the first 3 days of data:
> - [X] calls handled by AI
> - [X]% resolved without escalation
> - [X] CRM entries created automatically
>
> I've scheduled a check-in call for [date] to review performance and make any adjustments.
>
> If anything comes up before then, reach out to [EAS support contact].
>
> Best,
> [Your name]

---

### QUALITY CHECKPOINT 3 (Day 10, before handoff)

**Submit to EAS:**

- [ ] Runbook document (complete)
- [ ] Dashboard/monitoring access (link or screenshot)
- [ ] 3-day performance data (calls handled, resolution rate, escalation rate)
- [ ] Training recording link
- [ ] Client handoff email draft
- [ ] Any outstanding issues or known limitations

**EAS reviews within 4 hours. Go/no-go for client handoff.**

---

## Post-Delivery

1. Log completion in EAS project tracker
2. Note client satisfaction level and any feedback
3. Flag upsell opportunities:
   - Client wants more automations → Ops Pilot ($4,500)
   - Client wants ongoing management → Managed Ops ($1,500-$3,000/mo)
   - Client wants to expand to SMS/chat → future product
4. Transfer all credentials/access to EAS vault (do not retain client credentials)
5. Remain available for the 2-week check-in call, then hand off fully

---

## Common Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|----------------|--------------|
| Going 100% AI routing on Day 1 | Confidence after testing | Always start 50/50. Real calls are messier than test calls. Ramp over 3 days. |
| Skipping the training call | Client says "we'll figure it out" | Insist on it. Untrained clients call EAS for every small issue. Training prevents 80% of support requests. |
| Forgetting after-hours handling | Focus on business hours flow | After hours is where most missed calls happen. It's often the highest-value part of the system. |
| Hardcoding client info in scripts | Moving fast, cutting corners | Use variables ({{business_name}}, etc.) from Day 1. Makes scripts reusable and updates easier. |
| Not testing edge cases | Only testing happy paths | The confused caller and angry caller tests catch real issues. AI handles polite callers fine — it's the messy calls that matter. |
| CRM duplicate contacts | No dedup logic in workflow | Always search by phone before creating. Handle the "no caller ID" case explicitly. |
| Retell AI voice sounds robotic | Default settings, no tuning | Test multiple voices. Adjust speech speed, pause duration, interruption sensitivity. Small tweaks make a big difference. |
| Client's phone provider blocks forwarding | Didn't check compatibility early | Verify forwarding works on Day 1 before building anything. Some VoIP providers have restrictions. |
| Twilio SMS gets filtered as spam | Generic message content | Include business name in every SMS. Register Twilio number with carrier verification if volume is high. |
| n8n workflow silently fails | No error handling | Add Error Trigger nodes to every workflow. Set up email alerts for failures. Check execution log daily during launch week. |

---

## Time Budget Summary

| Activity | Estimated Hours | Day |
|----------|----------------|-----|
| Retell AI account setup + voice config | 1-2 hrs | 1 |
| Call script writing (6 scenarios) | 2-3 hrs | 1-2 |
| n8n/Make workflow design + setup | 2-3 hrs | 2 |
| SMS notification setup | 0.5 hrs | 2 |
| Checkpoint 1 submission | 0.5 hrs | 2 |
| Retell AI pathway implementation | 3-4 hrs | 3-4 |
| n8n/Make workflow build (4 pipelines) | 4-6 hrs | 3-5 |
| CRM integration + testing | 2-3 hrs | 4-5 |
| Call forwarding setup | 1 hr | 5 |
| Test calls (20 scenarios) | 4-5 hrs | 6-7 |
| Fix issues + re-test | 1-2 hrs | 7 |
| Load test (if needed) | 0.5 hrs | 7 |
| Checkpoint 2 submission | 0.5 hrs | 7 |
| Go live + monitoring | 2-3 hrs | 8 |
| Script adjustments + optimization | 2-3 hrs | 9 |
| Client team training | 1-2 hrs | 9 |
| Runbook compilation | 2-3 hrs | 10 |
| Monitoring dashboard setup | 1 hr | 10 |
| Final delivery + handoff email | 1 hr | 10 |
| Checkpoint 3 submission | 0.5 hrs | 10 |
| **Total** | **32-43 hrs** | **10 days** |

---

## Tools & Accounts Reference

| Tool | Purpose | Account Setup | Cost |
|------|---------|--------------|------|
| Retell AI | AI voice agent | retellai.com — create account | Pay-per-minute after free tier |
| n8n | Workflow automation | Self-host or n8n.cloud | Free (self-hosted) or $20+/mo (cloud) |
| Make | Workflow automation (alternative) | make.com | Free tier, then $9+/mo |
| Zapier | Workflow automation (simple clients) | zapier.com | Free tier very limited, $20+/mo |
| Twilio | SMS notifications | twilio.com | ~$1/mo per number + $0.0079/SMS |
| Cal.com | Appointment scheduling | cal.com | Free tier available |
| HubSpot | CRM (if client uses) | Client provides access | N/A |
| Salesforce | CRM (if client uses) | Client provides access | N/A |

---

## Escalation

- **Retell AI outage:** Check status.retellai.com. If down, enable direct forwarding to client's team until resolved. Notify EAS and client.
- **Client wants to change scope mid-project:** "Great idea — let me capture that for phase 2. For this pilot, let's keep the scope tight so we can deliver on time." Notify EAS if client pushes hard.
- **Client team resists the AI:** Common. Address with data ("the AI caught X calls that would have been missed"). Never force 100% AI if the team isn't comfortable. Gradual ramp wins trust.
- **Call quality issues:** Check internet connection at client site, Retell AI voice settings, call forwarding configuration. Most quality issues are network-related, not AI-related.
