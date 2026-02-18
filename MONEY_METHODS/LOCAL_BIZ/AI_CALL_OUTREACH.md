# AI Voice Call Outreach for Local Business Lead Gen

**Status:** RESEARCH COMPLETE - READY TO IMPLEMENT
**Created:** 2026-02-10
**Purpose:** Add AI voice calling as a second outreach channel after cold email. Catches the 70-80% of leads who read your email but didn't reply.

---

## The case for AI calling

Cold email alone converts 1-3% of prospects. Adding voice follow-up to non-responders adds 2-5% incremental conversion. Combined: 3-8% total conversion rate. At 200 leads/batch, that's the difference between 2 deals and 16 deals.

Local business owners pick up the phone. They're not in meetings all day like SaaS executives. A well-scripted AI call that leads with value and sounds human enough gets you past the "who is this" barrier in 5 seconds.

---

## AI cold calling platforms (2025-2026)

### Bland.ai

**What it is:** API-first AI phone calling platform. Most developer-friendly.
**Pricing:** $0.09/min connected time. No monthly fee. Pay per use.
**Volume:** Unlimited concurrent calls. No daily cap.
**Voice quality:** Good. Multiple voices. Custom voice cloning available.
**Latency:** ~800ms response time (noticeable but acceptable).
**Integration:** REST API, webhook callbacks, Zapier.
**Best for:** Developers who want full control. Our pick for V1.

Cost math: Average call = 1.5 min. At $0.09/min = $0.14/call. 200 calls/day = $28/day = $616/mo.

### Vapi.ai

**What it is:** Voice AI platform with built-in conversation management.
**Pricing:** $0.05/min (base) + LLM costs ($0.01-0.03/min depending on model). Total: ~$0.06-0.08/min.
**Volume:** Concurrent call limits based on plan. Free tier: 10 min/day.
**Voice quality:** Very good. ElevenLabs integration for premium voices.
**Latency:** ~600ms (better than Bland).
**Integration:** REST API, WebSocket, extensive SDKs.
**Best for:** Complex conversations with branching logic.

Cost math: Average call = 1.5 min. At $0.07/min = $0.11/call. 200 calls/day = $22/day = $484/mo.

### Retell.ai

**What it is:** Conversational AI for phone calls. Focus on natural-sounding dialogue.
**Pricing:** $0.07-0.12/min depending on plan. Starter: free 60 min/mo.
**Volume:** Enterprise plans for high volume.
**Voice quality:** Excellent. Best natural-sounding voices in the space.
**Latency:** ~500ms (best in class).
**Integration:** REST API, real-time WebSocket.
**Best for:** When voice quality matters most (our use case).

Cost math: Average call = 1.5 min. At $0.09/min = $0.14/call. 200 calls/day = $28/day = $616/mo.

### Air.ai

**What it is:** Full-service AI sales agent. Less customizable, more turnkey.
**Pricing:** $0.11/min. Higher but includes built-in CRM features.
**Volume:** Managed service, they handle scaling.
**Voice quality:** Good.
**Latency:** ~700ms.
**Integration:** Limited API. More of a managed platform.
**Best for:** Non-technical users who want plug-and-play.

### Synthflow.ai

**What it is:** No-code AI calling platform with pre-built templates.
**Pricing:** $29/mo starter (600 min), $99/mo pro (6,000 min).
**Volume:** Plan-based limits.
**Voice quality:** Good. Multiple accent options.
**Best for:** Quick setup without coding.

### Platform comparison

| Feature | Bland.ai | Vapi.ai | Retell.ai | Air.ai | Synthflow |
|---------|----------|---------|-----------|--------|-----------|
| Per-minute cost | $0.09 | $0.06-0.08 | $0.07-0.12 | $0.11 | $0.05-0.17 |
| Voice quality | Good | Very good | Excellent | Good | Good |
| Latency | 800ms | 600ms | 500ms | 700ms | 700ms |
| API quality | Excellent | Excellent | Good | Limited | Limited |
| Custom voices | Yes | Yes (ElevenLabs) | Yes | No | Limited |
| Free tier | No | 10 min/day | 60 min/mo | No | No |
| Ease of setup | Medium | Medium | Medium | Easy | Easy |
| **Recommendation** | **V1 pick** | **V2 upgrade** | **Premium option** | Skip | Budget option |

### Our pick: Bland.ai for V1, Vapi.ai for V2

Bland.ai for starting because: no monthly fee (pay per use only), excellent API, fast to integrate. Once we validate the channel works, upgrade to Vapi.ai for better voice quality and lower per-minute cost at scale.

---

## Legal requirements (TCPA compliance)

### Federal TCPA rules

The Telephone Consumer Protection Act is the primary law governing automated calls.

**Key requirements:**
1. **Prior express consent is NOT required for B2B calls.** TCPA consent rules primarily apply to residential/consumer numbers. Calling a business number listed on their website or Google Business profile is legal.
2. **Autodialer restrictions:** Using an ATDS (automatic telephone dialing system) to call cell phones without consent IS restricted. However, AI-initiated calls to published business numbers are generally permissible.
3. **Do Not Call list:** Scrub all numbers against the National DNC Registry ($75/year for up to 5 area codes). Business numbers are usually exempt, but scrub anyway.
4. **Time restrictions:** No calls before 8 AM or after 9 PM in the recipient's local time zone.
5. **Caller ID:** Must transmit accurate caller ID. Don't spoof numbers.

### State-specific AI disclosure laws

**States that REQUIRE disclosure that the caller is AI (as of 2025-2026):**

| State | Requirement | Penalty |
|-------|-------------|---------|
| California (SB 1001) | Must disclose AI/bot nature "clearly and conspicuously" at start of call | Up to $2,500/violation |
| Washington | Must disclose artificial voice use | Varies |
| Colorado | AI transparency in sales required | Consumer protection penalties |
| New York | Pending legislation, likely to pass | TBD |
| Illinois | BIPA considerations if voice recording | Up to $5,000/violation |

**Safe approach (use in ALL states):** Start every call with: "Hi, this is [Name] calling on behalf of [Agency Name]. I should let you know I'm an AI assistant reaching out about your business website." This covers you in every state and most people don't care if the content is relevant.

### FCC rules (2024-2025 updates)

The FCC ruled in early 2024 that AI-generated voices in robocalls are "artificial" under TCPA. This primarily targets political robocalls and scam calls. For B2B outreach to published business numbers with value-driven scripts, enforcement risk is minimal, but disclosure is still best practice.

### Our compliance protocol

1. Only call published business phone numbers (from website or Google Business)
2. Scrub against DNC registry before calling
3. Disclose AI nature within first 10 seconds of call
4. Respect "do not call" requests immediately (add to internal DNC list)
5. Only call 8 AM - 6 PM recipient local time (conservative window)
6. Log all calls with timestamps for compliance records
7. Maintain internal DNC list, check before every call
8. Never call the same number more than 2x in 30 days

---

## Call scripts

### Script 1: Cold outreach (first contact)

**Objective:** Get them to look at the demo website. That's it. Don't try to close on the call.

```
[RING]

THEM: Hello, [Business Name].

AI: Hi there, I'm calling about your business website. My name is [Agent Name]
    and I work with a web design firm. I should mention upfront that I'm an AI
    assistant making this call.

    I noticed that [Business Name]'s website hasn't been updated in a while,
    and I wanted to let you know that we actually went ahead and designed a
    modern version for you -- completely free, no strings attached.

[PAUSE 2 seconds - let them process]

THEM: [Likely response: "What do you mean?" or "Who is this?" or "Not interested"]

--- IF "What do you mean?" / curious ---

AI: So what we do is help local [industry] businesses get modern, mobile-friendly
    websites. We noticed your current site [specific issue: "doesn't load well on
    phones" / "has an expired SSL certificate" / "hasn't been updated since 2019"].

    We went ahead and built a preview of what a new version would look like with
    your business name, phone number, and address already on it.

    Would you like me to send the link to your email so you can take a look?
    No obligation at all.

THEM: Sure / What's the catch?

AI: No catch. If you like it and want to use it, the setup is five hundred dollars
    and includes hosting, mobile optimization, and SEO. But honestly, even if you
    don't go with us, the preview might give you ideas for what to ask your current
    web person to fix.

    What's the best email to send the preview to?

--- IF "Not interested" ---

AI: Totally understand. Quick question though -- are you happy with how your
    website looks on mobile right now? Because we ran a quick check and it's not
    loading properly on phones, which means about 60% of people searching for
    [industry] in [city] might be bouncing off your site.

    I can send you a free audit showing exactly what's happening. Takes 30 seconds
    to look at. Would that be helpful?

--- IF hard no ---

AI: Got it. Sorry to bother you. If you ever want a free website audit, you can
    reach us at [agency website]. Have a good day.

[HANG UP]
```

### Script 2: Follow-up after email (warm lead)

**Objective:** Follow up on cold email that was sent but got no reply.

```
AI: Hi, is this [First Name] at [Business Name]?

THEM: Yes.

AI: Hey [First Name], this is [Agent Name] with [Agency Name]. I'm an AI assistant
    calling to follow up on an email we sent a few days ago about [Business Name]'s
    website. Did you get a chance to see it?

--- IF "No" / "Don't remember" ---

AI: No worries. The short version is: we noticed your website has a few issues that
    might be costing you customers -- [specific issue]. We actually built a free
    preview of what a modern version would look like.

    Can I send it to your email right now? It takes 30 seconds to look at and
    there's zero obligation.

--- IF "Yes, I saw it" ---

AI: Great! What did you think? Did the design match what you're looking for?

[Branch based on response - handle objections, book a call, or close]
```

### Script 3: Appointment confirmation / nurture

```
AI: Hi [First Name], this is [Agent Name] with [Agency Name]. I'm confirming our
    call tomorrow at [time] to go over the website preview for [Business Name].
    Does that still work for you?

    I'm an AI assistant, so if you have any questions before the call, you can
    reply to our email or call us at [phone number] to speak with our team directly.
```

### Voice and delivery guidelines

**Pacing:**
- Speak at 140-160 words per minute (natural conversation speed)
- Add 1-2 second pauses after key statements (let information land)
- Don't rush through the AI disclosure
- Use contractions: "we've" not "we have", "it's" not "it is"

**Tone:**
- Friendly but professional (imagine calling a neighbor who owns a business)
- Not salesy, not pushy
- Curious and helpful energy
- Slight upward inflection on questions

**Filler words (add for naturalness):**
- "So..." (at start of explanations)
- "Actually..." (before surprising facts)
- "Honestly..." (before transparency moments)
- "You know..." (occasional, not overused)
- Brief "um" or "uh" (1-2 per call max)

---

## Volume and safety limits

### Daily call limits (recommended)

| Scenario | Calls/day | Cost/day | Monthly cost |
|----------|----------|---------|-------------|
| Testing phase | 20 | $2.80 | $62 |
| Ramp-up | 50 | $7.00 | $154 |
| Steady state | 100 | $14.00 | $308 |
| Aggressive | 200 | $28.00 | $616 |
| Max safe volume | 500 | $70.00 | $1,540 |

### Safety rules

- Never call the same number twice in 7 days
- If someone says "stop calling" or "do not call," add to DNC list immediately
- Monitor complaint rates: if >1% of calls result in complaints, reduce volume
- Keep call duration under 3 minutes (respect their time)
- Track connection rate: if <30% connect, your caller ID may be flagged
- Use local area code numbers when possible (higher pickup rate)
- Rotate caller ID numbers (2-3 numbers) to avoid spam flagging

### Cost per acquisition estimate

| Metric | Value |
|--------|-------|
| Calls per day | 100 |
| Connect rate | 35% |
| Connected calls | 35 |
| "Send me the demo" rate | 15% |
| Demo requests | 5 |
| Demo-to-call rate | 40% |
| Sales calls booked | 2 |
| Close rate | 25% |
| Deals per day | 0.5 |
| Deals per month (22 days) | 11 |
| Cost per call | $0.14 |
| Monthly call cost | $308 |
| **Cost per acquisition** | **$28** |
| Revenue per deal | $500 setup + $99/mo |
| **ROI: 18x on first month alone** | |

---

## Implementation steps

### Phase 1: Set up Bland.ai (1 hour)

```bash
# 1. Create Bland.ai account at bland.ai
# 2. Add payment method
# 3. Get API key
# 4. Test with a call to your own phone:

curl -X POST https://api.bland.ai/v1/calls \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1YOUR_PHONE",
    "task": "You are calling to test the system. Say hello, confirm the connection is clear, and hang up.",
    "voice": "maya",
    "max_duration": 30
  }'
```

### Phase 2: Configure call script (30 min)

```json
{
  "phone_number": "+1{{PROSPECT_PHONE}}",
  "task": "You are an AI assistant named Sarah calling on behalf of WebCraft Digital, a web design firm. You are calling {{BUSINESS_NAME}} in {{CITY}}, {{STATE}}. Their website {{SPECIFIC_ISSUE}}. You have already built a free preview of a modern website for them. Your goal is to get their email address so you can send them the preview link. Be friendly, professional, and transparent about being an AI. If they say not interested, offer a free website audit instead. If they say do not call, apologize and end the call.",
  "voice": "maya",
  "max_duration": 180,
  "wait_for_greeting": true,
  "first_sentence": "Hi there, I'm calling about {{BUSINESS_NAME}}'s website. This is Sarah from WebCraft Digital, and I should mention I'm an AI assistant making this call.",
  "transfer_phone_number": "+1YOUR_REAL_PHONE",
  "webhook": "https://your-server.com/api/call-completed"
}
```

### Phase 3: Build call pipeline (2 hours)

Create `AUTOMATIONS/ai_call_pipeline.py` that:
1. Reads scored leads CSV
2. Filters for leads with phone numbers and score >60
3. Checks against internal DNC list
4. Sends calls via Bland.ai API
5. Logs results to `LEDGER/CALL_LOG.csv`
6. Tracks: connected, demo requested, DNC requested, voicemail
7. Feeds "demo requested" leads back into email pipeline

### Phase 4: Integrate with email sequence

**Workflow:**
1. Day 0: Send cold email
2. Day 3: Send follow-up email
3. Day 5: AI call to non-responders ("Following up on an email we sent...")
4. Day 7: Send social proof email
5. Day 10: AI call #2 to demo-opened-but-not-replied leads
6. Day 14: Breakup email

Adding calls at Day 5 and Day 10 increases total sequence conversion by 2-5x vs email only.

---

## Metrics to track

| Metric | Target | Where to log |
|--------|--------|-------------|
| Connect rate (calls answered) | 30-40% | LEDGER/CALL_LOG.csv |
| AI disclosure dropoff | <20% | Track hangups within 10 sec |
| Demo request rate | 10-20% of connected | LEDGER/CALL_LOG.csv |
| DNC request rate | <5% of connected | Internal DNC list |
| Cost per connected call | <$0.40 | Bland.ai dashboard |
| Cost per demo request | <$3.00 | Calculated |
| Calls to deal ratio | 100:1 | Calculated |
| Complaint rate | <1% | Monitor, reduce volume if hit |

---

## Related files

- Master playbook: `MONEY_METHODS/LOCAL_BIZ/NATIONWIDE_LEAD_GEN_SYSTEM.md`
- Nationwide scraper: `AUTOMATIONS/nationwide_scraper.py`
- Mass outreach: `AUTOMATIONS/mass_outreach.py`
- Cold email checklist: `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md`
- Agency website spec: `MONEY_METHODS/LOCAL_BIZ/AGENCY_WEBSITE.md`
