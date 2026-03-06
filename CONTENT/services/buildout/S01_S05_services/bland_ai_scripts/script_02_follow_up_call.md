# Bland.ai Voice Script 02 — Follow-Up / Warm Lead Call

## PURPOSE
Follow up with leads who opened cold email or visited your site but didn't book. Warmer context = less friction. Goal: get on a call this week.

## CONFIGURATION
- Voice: Same as intro call (consistency matters)
- Speed: 0.9x
- Max duration: 2 minutes
- Trigger: Use after email open + no reply (24-48 hours later)

---

## SCRIPT

**[OPENING]**

"Hey [FIRST_NAME], this is [YOUR_NAME] — I sent you an email [yesterday/two days ago] about [COMPANY_NAME]'s website.

Saw you opened it, which usually means there's at least some curiosity. Figured a 60-second call was better than another email."

---

**[BRIDGE]**

"The short version: I do free website audits for [INDUSTRY] businesses and found a few things on your site that are probably costing you calls from Google.

Not a sales call — I'm just going to tell you what I found. If it's useful, great. If not, you've lost 15 minutes."

---

**[ASK]**

"Do you have literally 15 minutes this week? I can send you a Calendly link right now."

---

**[IF YES]**

"Great. I'll text you the link in the next 2 minutes — just pick the slot that works.

One question before we hang up: is the website your main source of leads, or do you mostly get business from referrals?"

[Listen and note — this context helps you in the actual call]

"Got it. That's helpful context. See you on the call, [FIRST_NAME]."

---

**[IF BUSY/NOT NOW]**

"No problem. When would be a better week — next week? Week after?"

[Get a specific timeframe]

"Perfect, I'll follow up then. Thanks for picking up."

---

**[IF NOT INTERESTED]**

"Totally fair. One question — is it more that the website is already working well, or just not a priority right now?"

[Listen — this is market research]

"Makes sense. I'll take you off the list. Thanks for your time."

---

## BLAND.AI CONFIG

```json
{
  "task": "Follow up with email opener, book 15-min call",
  "voice": "josh",
  "dynamic_data": {
    "first_name": "{{lead.first_name}}",
    "company_name": "{{lead.company}}",
    "industry": "{{lead.industry}}",
    "email_subject": "{{email.subject_line}}"
  },
  "call_timing": "business_hours_only",
  "timezone": "{{lead.timezone}}",
  "retry_if_no_answer": {
    "attempts": 2,
    "gap_hours": 4
  }
}
```

## PERFORMANCE BENCHMARKS
- Open rate → call trigger: Only call leads with 2+ email opens
- Connection rate: 20-35% (warmer than cold)
- Book rate: 25-40% of connections
