# Bland.ai Voice Script 05 — Re-engagement / Ghost Lead

## PURPOSE
Call leads who booked a call but didn't show, or who were interested but went cold after 30+ days. Pattern interrupt approach.

## CONFIGURATION
- Voice: Same as before
- Speed: 1.0x (direct energy for re-engagement)
- Max duration: 2 minutes
- Trigger: Manual or 30 days after last positive touchpoint with no conversion

---

## SCRIPT

**[OPENING — pattern interrupt]**

"Hey [FIRST_NAME], this is [YOUR_NAME]. I know it's been a while — [30 days / a month or so] since we last talked.

I'm calling because I'm going to close your file today unless there's still some interest. I don't want to keep following up if the timing is off."

---

**[PAUSE — let them respond]**

---

**[IF STILL INTERESTED]**

"Good to know. What happened — did something else come up, or was it more that the timing wasn't right?

[Listen]

Okay. So what would need to be true for this to make sense right now?"

[Get specific objection → handle or disqualify]

"Let's get something on the calendar then. I'll text you the link right now."

---

**[IF NOT INTERESTED / MOVED ON]**

"No problem at all — I appreciate you being straight with me. Good luck with [COMPANY_NAME]."

---

**[IF NO ANSWER — voicemail]**

"Hey [FIRST_NAME], this is [YOUR_NAME]. Leaving this as my last message — I don't want to be that person who keeps calling. If the website stuff ever becomes a priority, email me at [YOUR_EMAIL]. Otherwise, best of luck."

---

## NOTES
- This is a "take away" close by design
- Scarcity is real: you genuinely ARE closing the file if they don't respond
- Works better than persistent follow-up — creates urgency without pressure
- Many "lost" leads convert from this call simply because they feel the window closing

## BLAND.AI CONFIG

```json
{
  "task": "Re-engage cold lead with take-away close",
  "voice": "josh",
  "speed": 1.0,
  "dynamic_data": {
    "first_name": "{{lead.first_name}}",
    "company_name": "{{lead.company}}",
    "last_contact_days": "{{lead.days_since_last_contact}}"
  },
  "leave_voicemail": true,
  "retry_attempts": 1
}
```

## EXPECTED RESULTS
- Re-engagement rate from 30-day cold leads: 5-15%
- Worth running on every lead that showed initial interest
- 10 calls → 1-2 booked calls on average
