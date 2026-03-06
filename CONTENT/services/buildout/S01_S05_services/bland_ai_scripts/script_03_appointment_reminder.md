# Bland.ai Voice Script 03 — Appointment Reminder

## PURPOSE
Reduce no-shows for booked calls. Trigger 2 hours before scheduled call. Simple, direct, warm.

## CONFIGURATION
- Voice: Same as previous calls
- Speed: 1.0x (normal — reminder doesn't need slow/trust build)
- Max duration: 45 seconds
- Trigger: 2 hours before Calendly booking

---

## SCRIPT

"Hey [FIRST_NAME], quick reminder from [YOUR_NAME] — we have our [15-minute / 30-minute] call today at [TIME] [TIMEZONE].

The Zoom link is in your calendar invite — it's the one from Calendly.

If something came up and you need to reschedule, just reply to the email I sent or text me back at [YOUR_NUMBER]. No problem at all.

Otherwise, see you at [TIME]. Looking forward to it."

---

## BLAND.AI CONFIG

```json
{
  "task": "Appointment reminder 2 hours before call",
  "voice": "josh",
  "speed": 1.0,
  "dynamic_data": {
    "first_name": "{{booking.first_name}}",
    "meeting_time": "{{booking.start_time_formatted}}",
    "timezone": "{{booking.timezone}}",
    "duration": "{{booking.duration_minutes}}",
    "zoom_link": "{{booking.location}}"
  },
  "trigger": {
    "type": "scheduled",
    "offset_minutes": -120,
    "reference": "booking.start_time"
  }
}
```

## NOTES
- No-show rate without reminder: 30-40%
- No-show rate with 2-hour Bland.ai reminder: 10-15%
- Worth setting up even if it's the only automation you run
