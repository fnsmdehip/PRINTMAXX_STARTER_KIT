# Email Warmup Workflow

**Purpose:** Send warmup emails between inboxes, track deliverability, alert on issues.

**Workflow ID:** `email_warmup_v1`
**Trigger:** Schedule (multiple times daily)
**Est. Run Time:** 1-2 minutes per warmup cycle

---

## Architecture Overview

```
Schedule Trigger (8am, 12pm, 4pm, 8pm)
              |
              v
    Load Warmup Inbox Matrix
              |
              v
    Generate Warmup Pairs
    (Sender -> Recipient)
              |
              v
    For Each Pair:
        |
        v
    Send Warmup Email
    (Randomized subject/body)
              |
              v
    Wait 5-15 minutes
              |
              v
    Check Inbox for Delivery
              |
              v
    Mark as Read + Star
    (Positive engagement signals)
              |
              v
    Log Results to Sheet
              |
              v
    Alert if Issues Detected
```

---

## Warmup Strategy

### Daily Volume Ramp
```
Week 1: 5 emails/day per inbox
Week 2: 10 emails/day per inbox
Week 3: 15 emails/day per inbox
Week 4: 20 emails/day per inbox
Week 5+: 25 emails/day (maintenance)
```

### Inbox Matrix
Store in `LEDGER/WARMUP_DEVICE_MATRIX.csv`:

```csv
inbox_id,email,provider,status,warmup_start,current_volume,target_volume,health_score
INB001,sender1@yourdomain.com,Google Workspace,ACTIVE,2024-01-01,15,25,95
INB002,sender2@yourdomain.com,Google Workspace,ACTIVE,2024-01-01,15,25,92
INB003,receiver1@warmup-domain.com,Outlook,ACTIVE,2024-01-01,15,25,98
INB004,receiver2@warmup-domain.com,Zoho,ACTIVE,2024-01-01,15,25,88
```

---

## Node Configuration

### Node 1: Schedule Trigger
**Type:** `n8n-nodes-base.scheduleTrigger`
**Purpose:** Run 4x daily at optimal send times

```json
{
  "rule": {
    "interval": [
      {"field": "hours", "triggerAtHour": [8, 12, 16, 20]}
    ]
  }
}
```

---

### Node 2: Load Inbox Matrix
**Type:** `n8n-nodes-base.googleSheets`

```json
{
  "operation": "read",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "WARMUP_DEVICE_MATRIX",
  "range": "A:H",
  "options": {
    "filters": {
      "status": "ACTIVE"
    }
  }
}
```

---

### Node 3: Generate Warmup Pairs
**Type:** `n8n-nodes-base.code`
**Purpose:** Create sender-receiver pairs for this cycle

```javascript
const inboxes = $input.all().map(n => n.json);

// Separate senders (your domains) from receivers (warmup domains)
const senders = inboxes.filter(i =>
  i.email.includes('@yourdomain.com') || i.email.includes('@yourdomain2.com')
);
const receivers = inboxes.filter(i =>
  !i.email.includes('@yourdomain.com') && !i.email.includes('@yourdomain2.com')
);

// Also do reverse (receivers send to senders for reply chains)
const allPairs = [];

// Senders -> Receivers
senders.forEach(sender => {
  const dailyVolume = Math.min(sender.current_volume || 5, sender.target_volume || 25);
  const perCycle = Math.ceil(dailyVolume / 4); // 4 cycles per day

  // Pick random receivers
  const shuffled = [...receivers].sort(() => Math.random() - 0.5);
  const selectedReceivers = shuffled.slice(0, perCycle);

  selectedReceivers.forEach(receiver => {
    allPairs.push({
      sender_email: sender.email,
      sender_id: sender.inbox_id,
      receiver_email: receiver.email,
      receiver_id: receiver.inbox_id,
      direction: 'OUTBOUND',
      cycle_time: new Date().toISOString()
    });
  });
});

// Receivers -> Senders (reply simulation)
receivers.forEach(receiver => {
  const perCycle = Math.ceil((receiver.current_volume || 5) / 4);
  const shuffled = [...senders].sort(() => Math.random() - 0.5);
  const selected = shuffled.slice(0, Math.ceil(perCycle / 2)); // Half as many replies

  selected.forEach(sender => {
    allPairs.push({
      sender_email: receiver.email,
      receiver_email: sender.email,
      sender_id: receiver.inbox_id,
      receiver_id: sender.inbox_id,
      direction: 'REPLY_SIM',
      cycle_time: new Date().toISOString()
    });
  });
});

// Randomize order
const randomized = allPairs.sort(() => Math.random() - 0.5);

return randomized.map(p => ({json: p}));
```

---

### Node 4: Generate Email Content
**Type:** `n8n-nodes-base.code`
**Purpose:** Create natural-looking warmup emails

```javascript
const pair = $input.first().json;

// Randomized subject lines (conversational, not spammy)
const subjects = [
  'Quick question',
  'Following up',
  'Re: Our conversation',
  'Checking in',
  'Quick update',
  'Thoughts on this?',
  'Running a bit late',
  'Can you take a look?',
  'Meeting notes',
  'Thanks for yesterday',
  'Any updates?',
  'Scheduling update',
  'Project status',
  'Brief question',
  'For your review'
];

// Randomized body content (looks like real business emails)
const bodies = [
  'Hey, just wanted to check in on this. Let me know when you have a moment.',
  'Thanks for getting back to me. I\'ll review and follow up soon.',
  'Good morning! Do you have time for a quick call this week?',
  'I was thinking about what we discussed. Makes a lot of sense actually.',
  'Sounds good. I\'ll loop back once I have more details.',
  'Appreciate the update. Keep me posted on progress.',
  'Let me know if you need anything else from my end.',
  'Great, thanks for confirming. I\'ll mark it down.',
  'Running behind today but wanted to acknowledge receipt.',
  'Perfect timing. I was just about to reach out about this.',
  'That works for me. Looking forward to it.',
  'Thanks for the heads up. I\'ll adjust accordingly.',
  'Noted. Will add this to the agenda for our next sync.',
  'Makes sense. Let\'s reconnect early next week.',
  'Good to hear. Excited to see how this develops.'
];

// Random selection
const subject = subjects[Math.floor(Math.random() * subjects.length)];
const body = bodies[Math.floor(Math.random() * bodies.length)];

// Add some personalization
const greetings = ['Hi', 'Hey', 'Hello', ''];
const closings = ['Best', 'Thanks', 'Cheers', 'Talk soon', ''];
const greeting = greetings[Math.floor(Math.random() * greetings.length)];
const closing = closings[Math.floor(Math.random() * closings.length)];

let fullBody = body;
if (greeting) fullBody = `${greeting},\n\n${fullBody}`;
if (closing) fullBody = `${fullBody}\n\n${closing}`;

return [{
  json: {
    ...pair,
    subject,
    body: fullBody,
    generated_at: new Date().toISOString()
  }
}];
```

---

### Node 5: Send Warmup Email
**Type:** `n8n-nodes-base.emailSend` (or SMTP)
**Purpose:** Send the warmup email

```json
{
  "fromEmail": "={{ $json.sender_email }}",
  "toEmail": "={{ $json.receiver_email }}",
  "subject": "={{ $json.subject }}",
  "text": "={{ $json.body }}",
  "options": {
    "appendAttribution": false
  }
}
```

**Note:** For multiple inboxes, use HTTP Request with Gmail/Outlook API or n8n's credential switching.

---

### Node 6: Random Wait
**Type:** `n8n-nodes-base.wait`
**Purpose:** Natural timing between sends

```json
{
  "unit": "minutes",
  "amount": "={{ Math.floor(Math.random() * 10) + 5 }}"
}
```

Wait 5-15 minutes between sends (mimics human behavior).

---

### Node 7: Check Delivery (IMAP)
**Type:** `n8n-nodes-base.imap`
**Purpose:** Verify email arrived in inbox

```json
{
  "mailbox": "INBOX",
  "options": {
    "unseen": true,
    "customLimit": 20
  }
}
```

**Alternative:** Use Gmail API to search for specific message:
```json
{
  "method": "GET",
  "url": "https://gmail.googleapis.com/gmail/v1/users/me/messages",
  "qs": {
    "q": "from:{{ $json.sender_email }} subject:{{ $json.subject }} newer_than:1h"
  }
}
```

---

### Node 8: Positive Engagement Actions
**Type:** `n8n-nodes-base.code` + HTTP Request
**Purpose:** Mark as read, star, move from spam if needed

```javascript
// This would use Gmail API to:
// 1. Mark message as read
// 2. Add star
// 3. If in spam, move to inbox

const actions = {
  markRead: true,
  addStar: Math.random() > 0.5, // 50% get starred
  moveFromSpam: false // Check spam folder first
};

return [{json: {...$json, engagement_actions: actions}}];
```

**Gmail API Call (Mark Read + Star):**
```json
{
  "method": "POST",
  "url": "https://gmail.googleapis.com/gmail/v1/users/me/messages/{{ $json.message_id }}/modify",
  "body": {
    "removeLabelIds": ["UNREAD"],
    "addLabelIds": ["STARRED"]
  }
}
```

---

### Node 9: Check for Spam/Bounce
**Type:** `n8n-nodes-base.code`
**Purpose:** Detect deliverability issues

```javascript
const emailSent = $('Send Warmup Email').first().json;
const deliveryCheck = $('Check Delivery (IMAP)').all();

// Look for the sent email in received messages
const delivered = deliveryCheck.some(msg =>
  msg.json.subject === emailSent.subject &&
  msg.json.from.includes(emailSent.sender_email)
);

// Check timing
const sendTime = new Date(emailSent.generated_at);
const now = new Date();
const deliveryTime = delivered ? (now - sendTime) / 1000 / 60 : null; // minutes

let status = 'UNKNOWN';
let issue = null;

if (delivered && deliveryTime < 5) {
  status = 'DELIVERED_FAST';
} else if (delivered && deliveryTime < 30) {
  status = 'DELIVERED_NORMAL';
} else if (delivered) {
  status = 'DELIVERED_SLOW';
  issue = 'Slow delivery may indicate reputation issues';
} else {
  status = 'NOT_FOUND';
  issue = 'Email not found in inbox - may be in spam or bounced';
}

return [{
  json: {
    ...emailSent,
    delivery_status: status,
    delivery_time_minutes: deliveryTime,
    issue: issue,
    checked_at: now.toISOString()
  }
}];
```

---

### Node 10: Log Results
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Track all warmup activity

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "WARMUP_LOG",
  "columns": {
    "mappingMode": "defineBelow",
    "value": {
      "timestamp": "={{ $json.generated_at }}",
      "sender_email": "={{ $json.sender_email }}",
      "receiver_email": "={{ $json.receiver_email }}",
      "subject": "={{ $json.subject }}",
      "direction": "={{ $json.direction }}",
      "delivery_status": "={{ $json.delivery_status }}",
      "delivery_time_minutes": "={{ $json.delivery_time_minutes }}",
      "issue": "={{ $json.issue || '' }}",
      "checked_at": "={{ $json.checked_at }}"
    }
  }
}
```

---

### Node 11: Calculate Health Score
**Type:** `n8n-nodes-base.code`
**Purpose:** Update inbox health metrics

```javascript
// Aggregate recent results for this inbox
const logs = $('Load Recent Logs').all();
const senderEmail = $input.first().json.sender_email;

const myLogs = logs.filter(l => l.json.sender_email === senderEmail);
const last50 = myLogs.slice(-50);

// Calculate metrics
const deliveredCount = last50.filter(l =>
  l.json.delivery_status.startsWith('DELIVERED')
).length;
const deliveryRate = last50.length > 0 ? (deliveredCount / last50.length) * 100 : 100;

const fastDeliveries = last50.filter(l =>
  l.json.delivery_status === 'DELIVERED_FAST'
).length;
const fastRate = last50.length > 0 ? (fastDeliveries / last50.length) * 100 : 100;

// Health score = weighted average
const healthScore = Math.round(
  (deliveryRate * 0.6) + (fastRate * 0.4)
);

// Determine status
let status = 'HEALTHY';
let alert = null;

if (healthScore < 70) {
  status = 'CRITICAL';
  alert = `Inbox ${senderEmail} health critical: ${healthScore}%`;
} else if (healthScore < 85) {
  status = 'WARNING';
  alert = `Inbox ${senderEmail} needs attention: ${healthScore}%`;
}

return [{
  json: {
    email: senderEmail,
    health_score: healthScore,
    delivery_rate: deliveryRate,
    fast_delivery_rate: fastRate,
    status: status,
    alert: alert,
    calculated_at: new Date().toISOString()
  }
}];
```

---

### Node 12: Update Health in Matrix
**Type:** `n8n-nodes-base.googleSheets`

```json
{
  "operation": "update",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "WARMUP_DEVICE_MATRIX",
  "matchingColumns": ["email"],
  "columns": {
    "value": {
      "health_score": "={{ $json.health_score }}",
      "last_checked": "={{ $json.calculated_at }}"
    }
  }
}
```

---

### Node 13: Alert on Issues
**Type:** `n8n-nodes-base.if` + `n8n-nodes-base.slack`
**Purpose:** Immediate alert for deliverability problems

**Condition:**
```json
{
  "conditions": [
    {
      "leftValue": "={{ $json.alert }}",
      "rightValue": "",
      "operator": "isNotEmpty"
    }
  ]
}
```

**Slack Alert:**
```json
{
  "channel": "#email-health",
  "text": "DELIVERABILITY ALERT\n\n{{ $json.alert }}\n\nHealth Score: {{ $json.health_score }}%\nDelivery Rate: {{ $json.delivery_rate }}%\nFast Delivery: {{ $json.fast_delivery_rate }}%\n\nAction: Check spam folder, verify DNS, reduce volume"
}
```

---

## Human Approval Checkpoints

1. **Initial Setup:** Review inbox matrix before starting warmup
2. **Volume Increases:** Approve weekly volume ramps
3. **Issue Response:** Decide action when alerts fire (pause, reduce volume, investigate)

---

## Required Credentials

| Credential | Purpose | Notes |
|------------|---------|-------|
| `gmailOAuth2` | Send/receive Gmail | Per inbox |
| `outlookOAuth2` | Send/receive Outlook | Per inbox |
| `imapCredentials` | Check delivery | Alternative to API |
| `googleSheetsOAuth2Api` | Logging | Single credential |
| `slackApi` | Alerts | Single credential |

---

## Environment Variables

```bash
LEDGER_SHEET_ID=1abc...xyz
```

---

## Error Handling

### Send Failures
- **Auth Error:** Refresh OAuth, alert for manual intervention
- **Rate Limited:** Pause inbox for 1 hour
- **Invalid Recipient:** Remove from matrix, alert

### Delivery Check Failures
- **IMAP Connection Failed:** Retry 3x, then alert
- **API Error:** Log and continue

### Health Alerts
- **Score < 70:** CRITICAL - Pause inbox immediately
- **Score 70-85:** WARNING - Reduce volume by 50%
- **Score > 85:** HEALTHY - Continue normal volume

---

## Cost Estimation

| Component | Monthly Cost |
|-----------|--------------|
| n8n Cloud | $20 |
| Additional inboxes | $6/inbox (Workspace) |
| Warmup domain hosting | $10-20 |
| **Total (5 inboxes)** | ~$60/mo |

**Alternative:** Use warmup services like Instantly, Lemwarm (~$30-50/inbox/mo) but less control.

---

## Volume Ramp Schedule

```javascript
const RAMP_SCHEDULE = {
  week1: {daily: 5, perCycle: 2},
  week2: {daily: 10, perCycle: 3},
  week3: {daily: 15, perCycle: 4},
  week4: {daily: 20, perCycle: 5},
  week5: {daily: 25, perCycle: 7}  // Maintenance
};

// Auto-calculate based on warmup_start date
function getCurrentVolume(startDate) {
  const weeks = Math.floor((Date.now() - new Date(startDate)) / (7 * 24 * 60 * 60 * 1000));
  const weekKey = `week${Math.min(weeks + 1, 5)}`;
  return RAMP_SCHEDULE[weekKey];
}
```

---

## Testing Checklist

- [ ] Inbox matrix loads correctly
- [ ] Warmup pairs generate with proper distribution
- [ ] Emails send successfully
- [ ] Delivery confirmation works
- [ ] Positive engagement actions execute
- [ ] Logs save to sheet
- [ ] Health score calculates correctly
- [ ] Alerts fire when health drops
- [ ] Volume ramp applies correctly
- [ ] No duplicate sends

---

## Maintenance Tasks

**Daily:**
- Review any alerts
- Check health scores

**Weekly:**
- Review aggregate delivery rates
- Approve volume increases
- Check for bounces/complaints

**Monthly:**
- Rotate warmup content (new subjects/bodies)
- Review and update inbox matrix
- Check domain reputation (MXToolbox, Google Postmaster)

---

## DNS Requirements

Ensure all sending domains have:

```
SPF:   v=spf1 include:_spf.google.com ~all
DKIM:  Configured via provider
DMARC: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

Check with: https://mxtoolbox.com/
