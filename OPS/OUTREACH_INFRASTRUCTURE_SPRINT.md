# Outreach Infrastructure Sprint

**Created:** 2026-02-19
**Status:** READY TO EXECUTE
**Assets:** 9,123 hot leads (HOT_LEADS_QUALIFIED.csv) | 13,221 cold emails pre-generated (cold_emails_ready.csv) | 51 Instantly-format CSVs | 6 live demo sites | email_sender.py + response_tracker.py built
**Blocker:** Email infrastructure not configured. $0 today, $46/mo to unblock at scale.

---

## A. Email Infrastructure (Cheapest Path to Sending)

### The $0 Path: Start Sending TODAY

You already have `AUTOMATIONS/email_sender.py` built. It supports Gmail SMTP and Resend API. Here is how to send your first email in 15 minutes with zero dollars.

**Option 1: Personal Gmail + App Password ($0/mo, 500 emails/day limit)**

```
Step 1: Go to myaccount.google.com/apppasswords
Step 2: Select "Mail" and "Mac" (or "Other")
Step 3: Click "Generate" — copy the 16-character password
Step 4: Add to SECRETS/PAYMENT_INFO.md:
   GMAIL_ADDRESS=your@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
Step 5: Test immediately:
   python3 AUTOMATIONS/email_sender.py --preview --leads AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv --industry dental --max-sends 1
```

**Limits:** 500 emails/day. Google watches for spam patterns. If you send 500 cold emails from your personal Gmail, your account WILL get flagged within 48 hours. This is for testing only (10-20 sends).

**Option 2: Gmail Alias + Send-As ($0/mo, same 500 limit)**

```
Step 1: Gmail Settings > Accounts > "Send mail as" > Add another email
Step 2: Enter your alias (e.g., outreach@yourdomain.com if you own a domain)
Step 3: Gmail routes through Google servers (SPF/DKIM inherited)
Step 4: Update email_sender.py FROM_EMAIL to alias
```

This does NOT add deliverability protection. Same Gmail reputation. Useful only for cosmetic separation.

**Option 3: Outlook.com ($0/mo, 300 emails/day limit)**

```
Step 1: Create free Outlook account at outlook.com
Step 2: SMTP: smtp-mail.outlook.com:587
Step 3: 300 emails/day limit
Step 4: Lower deliverability than Gmail for cold email
```

**Option 4: Zoho Mail Free ($0/mo, 50 emails/day limit)**

```
Step 1: zoho.com/mail — free plan (5 users, 5GB)
Step 2: Requires custom domain (you need a domain anyway)
Step 3: SMTP: smtp.zoho.com:587
Step 4: 50 emails/day — too low for serious outreach
Step 5: Good for: testing sequences, warmup supplement
```

### The Cheapest Proper Setup: $46/mo

This is the minimum to send cold email safely at scale without burning your personal Gmail.

| Component | Cost | What It Does |
|-----------|------|-------------|
| 3 domains (Namecheap/Porkbun) | $30-45/year (~$3/mo) | Separate sending domains (protects main brand) |
| Google Workspace Starter x3 | $18/mo ($6 each) | 3 warmed inboxes with Google deliverability |
| Instantly.ai Growth plan | $30/mo | Warmup + sending + campaign management |
| **Total** | **~$51/mo** | **150 cold emails/day across 3 inboxes** |

Alternative budget combos:

| Setup | Monthly Cost | Emails/Day | Notes |
|-------|-------------|-----------|-------|
| Personal Gmail only | $0 | 10-20 safe | Testing only. Will get flagged at volume. |
| 1 domain + 1 Workspace + Instantly | $36/mo | 50/day | Minimum viable cold email |
| 3 domains + 3 Workspace + Instantly | $51/mo | 150/day | Recommended starter |
| DeliverOn pre-warmed (3 inboxes) | $49/mo | 150/day | Skip warmup period, start Day 1 |
| EmailBison (50 inboxes) | $99/mo | 2,500/day | Nuclear option for scale |
| Smartlead | $39/mo | Unlimited mailboxes | Good for rotating many inboxes |

### Platform Pricing Comparison (Feb 2026)

| Platform | Price | Mailboxes | Emails/mo | Warmup | Key Feature |
|----------|-------|-----------|-----------|--------|------------|
| **Instantly.ai** | $30/mo (Growth) | 5 | 5,000 | Built-in | Best campaign UI, reply tracking |
| **Smartlead** | $39/mo (Basic) | Unlimited | 6,000 | Built-in | Unlimited mailbox rotation |
| **DeliverOn** | $49/mo | 3 pre-warmed | 4,500 | Pre-done | Skip 14-21 day warmup |
| **EmailBison** | $99/mo | 50 | 75,000 | Built-in | Pure volume play |
| **Lemlist** | $32/mo | 1 | 1,500 | Built-in | LinkedIn + email combo |
| **Woodpecker** | $29/mo | 2 | 1,500 | Basic | Agency-friendly |

**Recommendation for PRINTMAXX:** Start with Instantly.ai ($30/mo) + 3 Google Workspace inboxes ($18/mo). Total $48/mo. This gives you campaign management, built-in warmup, reply tracking, and Instantly-compatible CSVs are already generated (51 files in `output/cold_emails/`).

### Domain Warmup Timeline

Cold email domains MUST be warmed before sending at volume. Sending 200 cold emails from a brand-new domain = instant spam folder.

```
Day 1-3:   Buy domain. Set up Workspace. Configure DNS (SPF/DKIM/DMARC).
Day 1-14:  Warmup phase. Send 10-20 emails/day to real addresses.
           Have friends reply. Subscribe to newsletters. Generate inbound.
           OR: Use Instantly.ai auto-warmup (sends + auto-replies).
Day 15-21: Start cold sending at 10/inbox/day (30 total across 3 inboxes).
Day 22-28: Ramp to 35/inbox/day (105 total) if bounce rate < 3%.
Day 29+:   Steady state at 50/inbox/day (150 total).
Day 45+:   Can push to 70/inbox/day (210 total) with good reputation.
```

**Skip warmup entirely:** DeliverOn ($49/mo) sells pre-warmed inboxes. Start sending Day 1 at 30/inbox/day. Pay more upfront, save 2-3 weeks.

### SPF/DKIM/DMARC Setup (Per Domain, 15 Minutes Each)

These DNS records tell email servers your messages are legitimate. Without them, 40-60% of cold emails go to spam.

**SPF Record (tells servers who can send from your domain):**
```
Type: TXT
Host: @
Value: v=spf1 include:_spf.google.com ~all
TTL: Auto
```

**DKIM Record (cryptographic signature on every email):**
```
1. Google Workspace Admin > Apps > Gmail > Authenticate Email
2. Click "Generate New Record"
3. Copy the TXT value (long string starting with "v=DKIM1;")
4. Add to DNS:
   Type: TXT
   Host: google._domainkey
   Value: [the copied string]
   TTL: Auto
```

**DMARC Record (tells servers what to do with failed emails):**
```
Type: TXT
Host: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
TTL: Auto
```

**Verify all 3:**
```bash
# Check SPF
nslookup -type=txt yourdomain.com

# Check DKIM
nslookup -type=txt google._domainkey.yourdomain.com

# Check DMARC
nslookup -type=txt _dmarc.yourdomain.com

# Or use web tool:
# https://mxtoolbox.com/SuperTool.aspx — enter domain, check SPF/DKIM/DMARC
```

**Also check domain health with our tool:**
```bash
python3 AUTOMATIONS/email_domain_health.py --check yourdomain.com
```

### Recommendation: Cheapest Way to Start TODAY with $0

```
1. Use personal Gmail with App Password (15 min setup)
2. Send 10 test emails to HOT_LEADS (score 90+, worst websites)
3. Track responses in response_tracker.py
4. If ANY responses come back positive, invest in $48/mo infra
5. One $500 deal pays for 10 months of email infrastructure

Command to send first test batch RIGHT NOW:
python3 AUTOMATIONS/email_sender.py \
  --preview \
  --leads AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv \
  --industry dental \
  --max-sends 10

(Remove --preview to actually send after reviewing output)
```

---

## B. Bland.ai Voice Outreach (AI Phone Calls)

### Current Status

Bland.ai pricing from our research (`AI_CALL_OUTREACH.md`):
- $0.09/min connected time
- No monthly fee (pay per use)
- Average call = 1.5 min = $0.14/call
- 100 calls/day = $14/day = $308/mo

**There is NO free tier on Bland.ai.** The earlier mention of "100 free calls/day" was incorrect. Bland.ai is pay-per-minute from the start.

**Cheapest AI calling options:**
| Platform | Free Tier | Per-Minute Cost | Best For |
|----------|-----------|----------------|---------|
| Vapi.ai | 10 min/day (~7 calls) | $0.06-0.08 | Free testing |
| Retell.ai | 60 min/month (~40 calls) | $0.07-0.12 | Monthly free testing |
| Bland.ai | None | $0.09 | Best API, production use |
| Synthflow | None ($29/mo starter) | ~$0.05 | No-code, easy setup |

**Cheapest path:** Use Vapi.ai free tier (10 min/day) to test scripts. Upgrade to Bland.ai when ready to scale.

### Bland.ai Setup Steps (1 Hour)

```bash
# Step 1: Create account
open "https://www.bland.ai"
# Click "Get Started" > sign up with email > add payment method

# Step 2: Get API key
# Dashboard > API Keys > Create New Key > Copy it

# Step 3: Add to SECRETS/PAYMENT_INFO.md
echo "BLAND_AI_KEY=sk-xxxxxxxxxxxxxxxx" >> SECRETS/PAYMENT_INFO.md

# Step 4: Test call to YOUR phone
curl -X POST https://api.bland.ai/v1/calls \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1YOURPHONE",
    "task": "You are testing a phone system. Say hello, confirm the call is clear, then say goodbye.",
    "voice": "maya",
    "max_duration": 30,
    "wait_for_greeting": true
  }'

# Step 5: Check call status
curl https://api.bland.ai/v1/calls/CALL_ID \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 3 Call Scripts for Local Business Outreach

**Script 1: Cold Outreach (First Contact) — Goal: Get Email for Demo Link**

```json
{
  "phone_number": "+1{{PHONE}}",
  "task": "You are Sarah, an AI assistant calling on behalf of a web design firm. You must disclose you are AI within the first 10 seconds. You are calling {{BUSINESS_NAME}} in {{CITY}}, {{STATE}}. Their website at {{WEBSITE}} has issues: {{PAIN_SIGNALS}}. You already built a free preview at {{DEMO_URL}}. Your ONLY goal is to get their email so you can send the preview. If they say not interested, offer a free website speed audit. If they say do not call, apologize immediately and end the call. Be friendly and conversational. Use contractions. Add brief pauses.",
  "voice": "maya",
  "max_duration": 180,
  "wait_for_greeting": true,
  "first_sentence": "Hi there, I'm calling about {{BUSINESS_NAME}}'s website. This is Sarah, and I should mention upfront I'm an AI assistant reaching out on behalf of a web design team.",
  "model": "enhanced",
  "temperature": 0.7,
  "transfer_phone_number": "+1YOUR_REAL_PHONE",
  "webhook": "https://your-webhook.com/call-complete"
}
```

**Script 2: Warm Follow-Up (Called After Email Was Sent, No Reply)**

```json
{
  "phone_number": "+1{{PHONE}}",
  "task": "You are Sarah, an AI assistant following up on an email sent a few days ago to {{FIRST_NAME}} at {{BUSINESS_NAME}}. Disclose AI nature immediately. The email contained a free website preview at {{DEMO_URL}}. Ask if they saw it. If no: briefly explain you noticed their site has issues and built a free modern preview, offer to resend. If yes: ask what they thought, handle objections, try to book a 15-min call with the human team. If not interested: thank them and end politely. If do not call: apologize and end immediately.",
  "voice": "maya",
  "max_duration": 180,
  "wait_for_greeting": true,
  "first_sentence": "Hi, is this {{FIRST_NAME}} at {{BUSINESS_NAME}}? This is Sarah, an AI assistant calling to follow up on an email we sent about your website.",
  "model": "enhanced",
  "temperature": 0.7
}
```

**Script 3: Demo Viewer Follow-Up (They Opened the Demo Link)**

```json
{
  "phone_number": "+1{{PHONE}}",
  "task": "You are Sarah, an AI assistant. {{FIRST_NAME}} at {{BUSINESS_NAME}} recently viewed their free website preview at {{DEMO_URL}}. Disclose AI nature. Your goal: find out what they thought and book a 15-min strategy call with the human team. Key talking points: the preview shows what a modern version of their site would look like, setup is $500 with hosting and SEO included, timeline is 2 weeks, monthly maintenance optional at $99/mo. If they have objections about price: mention that fixing just one issue (mobile speed) typically increases calls by 30-50%. If not interested: offer to send a PDF audit of their site for free. If do not call: end immediately.",
  "voice": "maya",
  "max_duration": 180,
  "wait_for_greeting": true,
  "first_sentence": "Hi {{FIRST_NAME}}, this is Sarah, an AI assistant with a web design team. I noticed you checked out the website preview we built for {{BUSINESS_NAME}} and wanted to see what you thought.",
  "model": "enhanced",
  "temperature": 0.7
}
```

### Connecting Bland.ai to HOT_LEADS_QUALIFIED.csv

The CSV has these relevant columns: `name`, `phone`, `email`, `website`, `city`, `state`, `category`, `demo_url`, `pain_signals`, `total_score`

**Python script to batch-call from CSV:**

```python
#!/usr/bin/env python3
"""Batch caller using Bland.ai API. Reads HOT_LEADS_QUALIFIED.csv."""

import csv
import json
import time
import requests
from pathlib import Path

API_KEY = "YOUR_BLAND_AI_KEY"  # Or read from SECRETS/PAYMENT_INFO.md
BASE = Path(__file__).resolve().parent.parent
LEADS = BASE / "AUTOMATIONS" / "leads" / "qualified" / "HOT_LEADS_QUALIFIED.csv"
CALL_LOG = BASE / "LEDGER" / "CALL_LOG.csv"
DNC_LIST = BASE / "LEDGER" / "DNC_LIST.csv"

def load_dnc():
    if not DNC_LIST.exists():
        return set()
    with open(DNC_LIST) as f:
        return {row["phone"] for row in csv.DictReader(f)}

def make_call(lead, script="cold"):
    """Send one call via Bland.ai API."""
    phone = lead.get("phone", "").strip()
    if not phone or len(phone) < 10:
        return None

    payload = {
        "phone_number": phone if phone.startswith("+") else f"+1{phone.replace('(','').replace(')','').replace('-','').replace(' ','')}",
        "task": f"You are Sarah, an AI assistant for a web design firm. Disclose AI nature in first 10 seconds. Calling {lead['name']} in {lead['city']}, {lead['state']}. Their site {lead['website']} has issues. You built a free preview at {lead['demo_url']}. Goal: get their email to send the preview link. Be conversational. If they say stop calling, end immediately.",
        "voice": "maya",
        "max_duration": 180,
        "wait_for_greeting": True,
        "first_sentence": f"Hi there, I'm calling about {lead['name']}'s website. This is Sarah, an AI assistant reaching out about a free website preview we built for you.",
    }

    resp = requests.post(
        "https://api.bland.ai/v1/calls",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload
    )
    return resp.json()

def batch_call(max_calls=20, min_score=80):
    dnc = load_dnc()
    with open(LEADS) as f:
        leads = [r for r in csv.DictReader(f)
                 if r.get("phone") and r["phone"] not in dnc
                 and int(r.get("total_score", 0)) >= min_score]

    print(f"Found {len(leads)} callable leads with score >= {min_score}")
    called = 0
    for lead in leads[:max_calls]:
        result = make_call(lead)
        if result and result.get("call_id"):
            print(f"  Called {lead['name']} ({lead['city']}) - ID: {result['call_id']}")
            called += 1
            time.sleep(2)  # Rate limit: 2 sec between calls
    print(f"Completed {called} calls")

if __name__ == "__main__":
    batch_call(max_calls=20, min_score=85)
```

### TCPA Compliance (Safe Harbor Rules)

**Federal TCPA Rules for B2B Calls:**
1. Prior express consent is NOT required for B2B calls to published business numbers
2. MUST transmit accurate caller ID (no spoofing)
3. No calls before 8 AM or after 9 PM in recipient's local time zone
4. Scrub against National DNC Registry ($75/year for up to 5 area codes)
5. Business numbers are generally DNC-exempt, but scrub anyway
6. Maintain internal DNC list. If someone says "stop calling," add immediately.
7. Never call same number more than 2x in 30 days

**State AI Disclosure Laws (2025-2026):**
| State | Requirement | Penalty |
|-------|-------------|---------|
| California (SB 1001) | Disclose AI/bot nature at start of call | Up to $2,500/violation |
| Washington | Must disclose artificial voice use | Varies |
| Colorado | AI transparency in sales required | Consumer protection penalties |
| Illinois | BIPA considerations if voice recording | Up to $5,000/violation |

**Safe approach (ALL states):** Disclose AI within first 10 seconds of every call. Our scripts do this.

**Our compliance protocol (already defined in AI_CALL_OUTREACH.md):**
1. Only call published business phone numbers
2. Scrub against DNC registry before calling
3. Disclose AI nature within first 10 seconds
4. Respect "do not call" requests immediately
5. Only call 8 AM - 6 PM recipient local time (conservative)
6. Log all calls with timestamps
7. Maintain internal DNC list
8. Never call same number more than 2x in 30 days

### ROI Calculation: AI Calling

```
Assumptions:
- 100 calls/day via Bland.ai
- $0.14 per call (1.5 min avg at $0.09/min)
- 35% connect rate = 35 conversations
- 15% demo request rate = 5 demo requests
- 40% demo-to-call rate = 2 sales calls
- 25% close rate = 0.5 deals/day
- 22 working days/month = 11 deals/month

Revenue:
- 11 deals x $500 setup = $5,500/mo
- 11 deals x $99/mo recurring = $1,089/mo (grows monthly)
- Month 1 total: $6,589

Costs:
- Bland.ai: 100 calls x 22 days x $0.14 = $308/mo
- Cost per acquisition: $308 / 11 = $28/deal

ROI: $6,589 revenue / $308 cost = 21.4x return
```

---

## C. Outreach Sequence (The Actual Campaign)

### Multi-Channel 7-Day Sequence

All assets exist. This connects them.

**Day 1: Email Intro with Personalized Demo Link**
```
Trigger: Lead enters pipeline (score >= 65 in HOT_LEADS_QUALIFIED.csv)
Action: Send Email 1 from cold_emails_ready.csv (already generated)
Subject: "quick win for {{BUSINESS_NAME}}"
Body: References specific website issues + links to personalized demo
Tool: python3 AUTOMATIONS/email_sender.py --outreach output/cold_emails/instantly_step1.csv --max-sends 50
Track: python3 AUTOMATIONS/response_tracker.py log --status SENT
```

**Day 3: Follow-Up Email with ROI Math**
```
Trigger: No reply to Day 1 email
Action: Send Email 2 (follow-up with conversion math)
Subject: "re: {{BUSINESS_NAME}} website"
Body: "fixing 3 issues = 2-3x more leads. same traffic."
Tool: python3 AUTOMATIONS/email_sender.py --outreach output/cold_emails/instantly_step2.csv --max-sends 50
Track: python3 AUTOMATIONS/response_tracker.py log --status SENT
```

**Day 5: Bland.ai Call to Non-Responders**
```
Trigger: Email opened but no reply (or no open data available)
Action: AI call using Script 2 (warm follow-up)
Target: Leads who received emails but did not reply
Tool: python3 batch_caller.py --script warm --max-calls 50 --min-score 70
Track: Log to LEDGER/CALL_LOG.csv
```

**Day 7: Final Email with Urgency**
```
Trigger: No reply to Day 3 email AND no positive call outcome
Action: Send Email 3 (breakup + free tool offer)
Subject: "last email + free tool"
Body: "last one from me. built a speed test tool you might find useful."
Tool: python3 AUTOMATIONS/email_sender.py --outreach output/cold_emails/instantly_step3.csv --max-sends 50
Track: python3 AUTOMATIONS/response_tracker.py log --status SENT
```

**Day 10 (Hot Leads Only): Second AI Call**
```
Trigger: Opened demo link but didn't reply to any email
Action: AI call using Script 3 (demo viewer follow-up)
Target: Leads who visited demo_url
Tool: python3 batch_caller.py --script demo-viewer --max-calls 20 --min-score 80
Track: Log to LEDGER/CALL_LOG.csv
```

### Pipeline Stages

Track every lead through this funnel using response_tracker.py:

```
QUEUED → SENT → OPENED → REPLIED → BOOKED → CLOSED
                                  → BOUNCED
                                  → UNSUBSCRIBED
```

**Commands:**
```bash
# View pipeline dashboard
python3 AUTOMATIONS/response_tracker.py dashboard

# Log a status change
python3 AUTOMATIONS/response_tracker.py log --id L00001 --status REPLIED

# See overdue follow-ups
python3 AUTOMATIONS/response_tracker.py followups

# Export for CRM
python3 AUTOMATIONS/response_tracker.py export --format csv
```

### Tracking Responses

The response_tracker.py reads `output/cold_emails/cold_emails_ready.csv` and maintains `AUTOMATIONS/leads/qualified/campaign_tracker.csv` with these columns:

```
email_id, to_email, business_name, city, industry, website,
demo_url, lead_score, status, deal_value, sent_at, opened_at,
replied_at, booked_at, closed_at, followup_1_due, followup_2_due,
followup_1_sent, followup_2_sent, notes
```

**Initialize tracker from existing cold emails:**
```bash
python3 AUTOMATIONS/response_tracker.py init
```

---

## D. Quick Start Commands (Copy-Paste Ready)

### Send First 10 Test Emails (5 Minutes)

```bash
# Step 1: Set up Gmail credentials
# Edit SECRETS/PAYMENT_INFO.md and add:
#   GMAIL_ADDRESS=your@gmail.com
#   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
# (Get app password from myaccount.google.com/apppasswords)

# Step 2: Preview emails (dry run, nothing sent)
python3 AUTOMATIONS/email_sender.py \
  --preview \
  --leads AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv \
  --industry dental \
  --max-sends 10

# Step 3: Review the preview output. If it looks good:
python3 AUTOMATIONS/email_sender.py \
  --leads AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv \
  --industry dental \
  --max-sends 10

# Step 4: Or send from pre-generated Instantly CSVs
python3 AUTOMATIONS/email_sender.py \
  --outreach output/cold_emails/instantly_step1.csv \
  --max-sends 10
```

### Make First Bland.ai Test Call (10 Minutes)

```bash
# Step 1: Sign up at bland.ai and get API key

# Step 2: Test call to YOUR phone
curl -X POST https://api.bland.ai/v1/calls \
  -H "Authorization: Bearer YOUR_BLAND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1YOURPHONENUMBER",
    "task": "You are Sarah, an AI assistant testing a phone system for a web design firm. Say hello, confirm the call is clear, mention you are an AI, then say goodbye. Keep it under 30 seconds.",
    "voice": "maya",
    "max_duration": 30,
    "wait_for_greeting": true
  }'

# Step 3: Call a real lead (highest score, worst website)
curl -X POST https://api.bland.ai/v1/calls \
  -H "Authorization: Bearer YOUR_BLAND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+17193848703",
    "task": "You are Sarah, an AI assistant for a web design firm. Disclose AI nature in first 10 seconds. You are calling David N. Trujillo DDS in La Junta, CO. Their website smilehighdentistry.com has no mobile viewport, no SSL, and missing SEO. You built a free preview at https://dental-demo.surge.sh. Goal: get their email to send the preview. Be friendly. If they say stop, end immediately.",
    "voice": "maya",
    "max_duration": 180,
    "wait_for_greeting": true,
    "first_sentence": "Hi there, I am calling about Smile High Dentistry website. This is Sarah, an AI assistant reaching out about a free website preview we built for you."
  }'
```

### Track Everything in the Pipeline

```bash
# Initialize the campaign tracker from existing cold emails
python3 AUTOMATIONS/response_tracker.py init

# View the full pipeline dashboard
python3 AUTOMATIONS/response_tracker.py dashboard

# Log when someone replies
python3 AUTOMATIONS/response_tracker.py log --id L00001 --status REPLIED --notes "interested in pricing"

# Log when a call is booked
python3 AUTOMATIONS/response_tracker.py log --id L00001 --status BOOKED --notes "call scheduled Feb 21 2pm"

# Log when a deal closes
python3 AUTOMATIONS/response_tracker.py log --id L00001 --status CLOSED --deal-value 500

# Check what needs follow-up today
python3 AUTOMATIONS/response_tracker.py followups

# Refresh the visual pipeline dashboard (Bloomberg-style)
python3 AUTOMATIONS/refresh_dashboard.py
# View it: open https://printmaxx-dashboard.surge.sh

# Check email domain health before sending
python3 AUTOMATIONS/email_domain_health.py --check yourdomain.com

# Full system health check
python3 AUTOMATIONS/system_health_monitor.py --quick
```

### Full Daily Outreach Routine (30 min/day)

```bash
# Morning (15 min)
python3 AUTOMATIONS/response_tracker.py followups          # Check overdue follow-ups
python3 AUTOMATIONS/response_tracker.py dashboard           # View pipeline state
python3 AUTOMATIONS/email_sender.py --outreach output/cold_emails/instantly_step1.csv --max-sends 50  # Send batch

# Afternoon (15 min)
# Check Gmail for replies manually
# Log any responses:
python3 AUTOMATIONS/response_tracker.py log --id LXXXXX --status REPLIED
# Send follow-up emails for Day 3/7 leads:
python3 AUTOMATIONS/email_sender.py --outreach output/cold_emails/instantly_step2.csv --max-sends 30

# Weekly
python3 AUTOMATIONS/refresh_dashboard.py                    # Update dashboard
python3 AUTOMATIONS/email_domain_health.py --check yourdomain.com  # Domain health
```

---

## E. Asset Inventory (What You Already Have)

### Leads

| Asset | Count | Location |
|-------|-------|----------|
| Hot leads (score >= 65) | 9,123 | `AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv` |
| Warm leads (score 45-64) | ~17,400 | `AUTOMATIONS/leads/qualified/WARM_LEADS_QUALIFIED.csv` |
| All analyzed leads | ~53,200 | `AUTOMATIONS/leads/qualified/ANALYZED_LEADS.csv` |
| Pre-filtered leads | ~1,450,000 | `AUTOMATIONS/leads/qualified/PREFILTERED_LEADS.csv` |

### Cold Emails (Pre-Generated)

| Asset | Count | Location |
|-------|-------|----------|
| Master cold emails (3-step sequences) | 13,221 | `output/cold_emails/cold_emails_ready.csv` |
| Instantly-format CSVs (Step 1) | ~4,400 | `output/cold_emails/instantly_step1.csv` |
| Instantly-format CSVs (Step 2) | ~4,400 | `output/cold_emails/instantly_step2.csv` |
| Instantly-format CSVs (Step 3) | ~4,400 | `output/cold_emails/instantly_step3.csv` |
| Hot batch (high-priority) | 359 | `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv` |
| Time-stamped Instantly batches | 47 files | `output/cold_emails/cold_emails_instantly_*.csv` |

### Demo Sites (Live)

| Template | URL | For Industries |
|----------|-----|----------------|
| Dental | https://dental-demo.surge.sh | dentist, cosmetic_dentist, orthodontist, general_dentistry |
| Restaurant | https://restaurant-site-demo.surge.sh | restaurant, cafe, bakery |
| Fitness | https://fitness-demo.surge.sh | gym, trainer, yoga |
| Legal | https://legal-demo.surge.sh | lawyer, attorney |
| Plumber | https://plumber-demo.surge.sh | plumber, HVAC, electrician |
| Realtor | https://realtor-demo.surge.sh | real_estate_agent |
| Dental Motion | https://dental-motion.surge.sh | premium dental upsell |
| Realtor Motion | https://realtor-motion.surge.sh | premium realtor upsell |
| Restaurant Motion | https://restaurant-motion.surge.sh | premium restaurant upsell |

### Personalized Demos (Live)

| Asset | Count | URL |
|-------|-------|-----|
| Personalized landing pages | 600+ | https://printmaxx-demos.surge.sh |
| Demo manifest | 600+ rows | `output/personalized_demos/MANIFEST.csv` |

### Tools (Built and Ready)

| Tool | File | Purpose |
|------|------|---------|
| Email sender | `AUTOMATIONS/email_sender.py` | Gmail SMTP / Resend API sending |
| Email generator | `AUTOMATIONS/generate_cold_emails.py` | Generate personalized 3-email sequences |
| Response tracker | `AUTOMATIONS/response_tracker.py` | Campaign funnel tracking |
| Pipeline dashboard | `AUTOMATIONS/refresh_dashboard.py` | Bloomberg-style visual dashboard |
| Lead qualifier | `AUTOMATIONS/intelligent_lead_qualifier.py` | Score leads 0-100 |
| Demo personalizer | `AUTOMATIONS/personalize_demos.py` | Generate personalized landing pages |
| SEO analyzer | `AUTOMATIONS/seo_competitor_analyzer.py` | Competitive analysis |
| Domain health | `AUTOMATIONS/email_domain_health.py` | SPF/DKIM/DMARC checker |
| A/B tester | `AUTOMATIONS/cold_email_ab_test.py` | Split test email variants |
| Lead enricher | `AUTOMATIONS/lead_enrichment.py` | Google rating, social, tech stack |

---

## F. Revenue Math

### Conservative Scenario (Email Only, $0 Budget)

```
Send 10 emails/day from personal Gmail (safe limit)
= 220 emails/month
x 5% reply rate = 11 replies
x 30% positive = 3.3 interested
x 25% close rate = ~1 deal/month
x $500 = $500/month

Cost: $0
ROI: Infinite
Time to first deal: 30-60 days
```

### Standard Scenario ($48/mo Email Infrastructure)

```
Send 150 emails/day across 3 warmed inboxes
= 3,300 emails/month
x 5% reply rate = 165 replies
x 30% positive = 50 interested leads
x 25% close rate = 12.5 deals/month
x $500 = $6,250/month

Cost: $48/month
ROI: 130x
Time to first deal: 21-35 days (after warmup)
```

### Aggressive Scenario ($356/mo Email + Calls)

```
Email: 150/day = 3,300/month → 12.5 deals
Calls: 100/day via Bland.ai → 11 deals
Combined (subtract overlap): ~18 deals/month

Revenue: 18 x $500 = $9,000/month setup
         18 x $99 = $1,782/month recurring (grows)
Total Month 1: $10,782

Cost: $48 (email) + $308 (Bland.ai) = $356/month
ROI: 30x
```

---

## G. Decision Matrix: What to Do RIGHT NOW

| Priority | Action | Cost | Time | Expected Result |
|----------|--------|------|------|-----------------|
| 1 | Set up Gmail App Password | $0 | 5 min | Can send emails immediately |
| 2 | Send 10 test emails to top leads | $0 | 10 min | Validate email templates work |
| 3 | Monitor for replies (48 hours) | $0 | Passive | See if the offer resonates |
| 4 | Sign up for Bland.ai | $0 signup | 15 min | Can make test calls |
| 5 | Make 5 test calls to top leads | ~$0.70 | 20 min | Validate call scripts |
| 6 | Buy 3 cold email domains | $30-45 | 10 min | Separate sending reputation |
| 7 | Set up Google Workspace x3 | $18/mo | 30 min | Proper sending infrastructure |
| 8 | Configure SPF/DKIM/DMARC | $0 | 30 min | Deliverability protection |
| 9 | Start 14-day warmup (or buy DeliverOn) | $0 or $49 | 14 days | Safe to send at volume |
| 10 | Sign up for Instantly.ai | $30/mo | 15 min | Campaign management + warmup |
| 11 | Upload Instantly CSVs | $0 | 10 min | 13,221 emails loaded and ready |
| 12 | Launch campaigns at 30/day | $0 | 5 min | Revenue pipeline is live |

**The single most important step:** Priority 1 and 2. Takes 15 minutes, costs $0, and tells you whether this entire pipeline will work before you spend a dollar on infrastructure.
