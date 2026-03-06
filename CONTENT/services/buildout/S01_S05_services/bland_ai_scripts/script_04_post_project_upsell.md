# Bland.ai Voice Script 04 — Post-Project Upsell / Maintenance Offer

## PURPOSE
Call clients 30 days after project delivery. Goal: offer monthly maintenance retainer and collect testimonial. Best time to upsell = when they're happy.

## CONFIGURATION
- Voice: Same as before (consistency)
- Speed: 0.9x
- Max duration: 3 minutes
- Trigger: 30 days after project marked "delivered" in your CRM

---

## SCRIPT

**[OPENING]**

"Hey [FIRST_NAME], this is [YOUR_NAME]. It's been about a month since we launched [WEBSITE_DOMAIN] — just wanted to check in and see how things are going."

---

**[LISTEN FIRST]**

[Let them respond — acknowledge what they say]

If positive: "That's great to hear. Have you noticed any change in calls or Google traffic yet?"

If neutral: "Makes sense — usually takes 4-8 weeks to see the Google movement. We're still early."

If negative: "Tell me more — what's feeling off? I want to make sure everything's working right."

---

**[SEGUE TO MAINTENANCE]**

"The reason I'm calling is — a lot of clients at the 30-day mark ask me about ongoing support. Keeping the site updated, making content changes, monitoring speed and uptime.

I have a simple $149/month maintenance package that covers all of that. No contract, cancel any time.

Does that sound like something that would be useful for [COMPANY_NAME]?"

---

**[IF YES]**

"Perfect. I'll send you an invoice today — it's just a Stripe payment link. Covers the first month and you get the second month free if you stay on for 3 months.

Appreciate the trust, [FIRST_NAME]. I'll send that now."

---

**[IF NO]**

"Totally understand — not everyone needs it. If something comes up with the site or you want changes later, just email me and I'll quote it separately.

One other thing — would you be open to leaving a quick Google review or Trustpilot review? Even just a sentence or two. It genuinely helps my business."

[If yes] "Amazing. I'll text you the link right now. Takes 2 minutes."

---

**[CLOSE]**

"Thanks for the time, [FIRST_NAME]. Good luck with [BUSINESS_TYPE]. You know where to find me."

---

## BLAND.AI CONFIG

```json
{
  "task": "30-day check-in: collect feedback, offer maintenance, request review",
  "voice": "josh",
  "dynamic_data": {
    "first_name": "{{client.first_name}}",
    "website_domain": "{{project.domain}}",
    "company_name": "{{client.company}}",
    "business_type": "{{client.industry}}"
  },
  "post_call_sms": {
    "if_maintenance_yes": "Hey {{first_name}}, here's the invoice: [STRIPE_LINK]",
    "if_review_yes": "Hey {{first_name}}, here's the Google review link: [GOOGLE_REVIEW_LINK]. Takes 2 minutes — really appreciate it!"
  },
  "trigger": {
    "type": "crm_event",
    "event": "project_delivered",
    "offset_days": 30
  }
}
```

## EXPECTED RESULTS
- Maintenance conversion rate: 20-35% of happy clients
- Review collection rate: 40-60% of clients who answer
- Revenue from 10 active clients: $1,490/mo recurring
