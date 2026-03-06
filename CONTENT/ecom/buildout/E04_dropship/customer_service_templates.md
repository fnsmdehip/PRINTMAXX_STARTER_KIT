# E04 Dropshipping Automation — Customer Service Templates

## Response Time Targets
- Standard tickets: 24 hours max (aim for 4 hours)
- Disputes/chargebacks: 12 hours (platform deadlines are hard)
- WISMO (where is my order): 4 hours (these escalate fastest)

## Tone Guide
- Professional but not corporate
- Direct answers, no runaround
- Specific next steps, not vague reassurances
- If you messed up, own it immediately — don't deflect

---

## CATEGORY 1: ORDER STATUS

**T01 — WISMO (Order Not Yet Shipped)**
```
Subject: Re: Order #[ORDER] Status

Hey [Name],

Your order is still being processed — we're in the fulfillment queue and
shipping within [X] business days.

Once it ships, you'll get a tracking number automatically by email.

Order details: [ORDER NUMBER] | Placed: [DATE]

Anything else I can help with?

[Name]
[Brand] Support
```

**T02 — WISMO (Shipped, Tracking Not Updating)**
```
Subject: Re: Order #[ORDER] Tracking

Hey [Name],

Tracking numbers sometimes take 2-3 business days to activate in the carrier's
system — that's normal and doesn't mean anything's wrong.

Your tracking link: [TRACKING URL]
Carrier: [CARRIER]
Expected arrival: [DATE RANGE]

If tracking still shows no movement after [DATE + 3 days], reply here and I'll
investigate directly with the supplier.

[Name]
[Brand] Support
```

**T03 — WISMO (Late, Past Estimated Delivery)**
```
Subject: Re: Order #[ORDER] Delay

Hey [Name],

I checked your order — you're right, it's past the estimated window.

Here's where things stand: [TRACKING STATUS]

I'm contacting our supplier now to get an update. I'll have a specific answer
for you within 24 hours.

If you'd prefer a refund while we sort this out, just say the word and I'll
process it immediately — no need to wait.

[Name]
[Brand] Support
```

**T04 — WISMO (Lost Package)**
```
Subject: Re: Order #[ORDER] — Replacement Shipping Now

Hey [Name],

This one's on us. After checking with the carrier, it's clear the package
is lost.

I'm shipping a replacement today at no charge. You'll get a new tracking
number within 24-48 hours.

If you'd prefer a full refund instead, just say the word — I'll process it
immediately.

Sorry for the hassle.

[Name]
[Brand] Support
```

---

## CATEGORY 2: RETURNS & REFUNDS

**T05 — Return Request (Within Policy)**
```
Subject: Re: Return for Order #[ORDER]

Hey [Name],

No problem at all — you're within our 30-day return window.

Here's how it works:
1. I'll send you a prepaid return label (check your inbox in 1-2 hours)
2. Drop the package off at any [CARRIER] location
3. Refund processed within 3-5 business days of us receiving it

You don't need to include anything special — just the item in its packaging.

[Name]
[Brand] Support
```

**T06 — Return Request (Outside Policy)**
```
Subject: Re: Return for Order #[ORDER]

Hey [Name],

Your order is outside our 30-day return window (ordered [DATE], delivered
approximately [DATE]).

I can't process a standard return, but let me see what I can do.

Can you tell me what the issue is with the product? If it's defective or not
as described, that's different from a standard return and I may be able to
help regardless of the timeframe.

[Name]
[Brand] Support
```

**T07 — Refund for Defective Product**
```
Subject: Re: Defective Item — Order #[ORDER]

Hey [Name],

That's not acceptable — I'm sorry you received a defective product.

I'm issuing a full refund right now. You'll see it back on your [PAYMENT
METHOD] within 5-7 business days.

You don't need to ship the item back.

If you'd prefer a replacement instead of a refund, I can arrange that too —
just let me know which you'd prefer.

[Name]
[Brand] Support
```

**T08 — Partial Refund Offer (Goodwill)**
```
Subject: Re: Order #[ORDER] — Resolution

Hey [Name],

Thank you for the detail — I understand your frustration.

Here's what I can offer:
- 30% partial refund ($[AMOUNT]) as compensation, no return required
- OR full store credit for a future order

The issue you described [BRIEF SUMMARY] is something we're actively working
to improve with our supplier.

Which would you prefer?

[Name]
[Brand] Support
```

---

## CATEGORY 3: WRONG/DAMAGED ITEMS

**T09 — Wrong Item Received**
```
Subject: Re: Wrong Item — Order #[ORDER]

Hey [Name],

That's a fulfillment error on our end — I'm sorry about that.

To get the right item to you:
1. Can you send a quick photo of what you received?
2. I'll ship the correct item within 1 business day
3. You keep the wrong item — no need to return it

Alternatively, if you'd prefer a full refund, I can do that immediately.

Which works better for you?

[Name]
[Brand] Support
```

**T10 — Damaged in Transit**
```
Subject: Re: Damaged Package — Order #[ORDER]

Hey [Name],

I'm sorry — damage in transit happens more than it should.

Two options:
1. Replacement shipped to you within 2 business days
2. Full refund processed today

Either way, can you send a photo of the damage? I need it for the carrier
claim (and to improve packaging going forward).

You won't be waiting long either way.

[Name]
[Brand] Support
```

---

## CATEGORY 4: PRE-PURCHASE QUESTIONS

**T11 — Shipping Time Question**
```
Subject: Re: Shipping Time

Hey [Name],

Standard shipping is 8-15 business days from order date. Most customers
receive within 10-12 days.

Expedited shipping (5-8 days) is available at checkout for $9.99.

All orders include tracking — you'll get updates via email automatically.

Anything else?

[Name]
[Brand] Support
```

**T12 — Product Availability / Size Question**
```
Subject: Re: Product Question

Hey [Name],

[PRODUCT] is currently in stock and available in [SIZES/COLORS].

[If OOS:] We're restocking [PRODUCT] and expect it back in [TIMEFRAME].
Want me to add you to the notification list?

[If custom request:] We don't currently offer [REQUEST], but I can pass
this to our product team as a suggestion.

[Name]
[Brand] Support
```

**T13 — Discount Request**
```
Subject: Re: Discount

Hey [Name],

Check your email — new customers get 10% off their first order via our
welcome email (sometimes lands in spam).

If you didn't get it: use code SAVE10 at checkout.

That's the best I can do on pricing — products are already priced as low
as we can go to maintain quality and service levels.

[Name]
[Brand] Support
```

---

## CATEGORY 5: DISPUTES & CHARGEBACKS

**T14 — PayPal Dispute Response**

Use in PayPal Resolution Center (submit as evidence):
```
Order ID: [ORDER]
Customer: [NAME]
Order Date: [DATE]
Tracking: [NUMBER] ([CARRIER])
Delivery Status: [STATUS from AfterShip]
Product Shipped: [EXACT PRODUCT NAME]
Invoice: [ATTACH]

Evidence:
- Order confirmation email sent [DATE]
- Tracking number provided [DATE]
- Tracking shows [STATUS] as of [DATE]
- Product matches listing description exactly

Resolution Offered:
We have offered [REFUND/REPLACEMENT] to the customer and received no response
within [X] days. We are willing to resolve this with a [FULL REFUND/
REPLACEMENT] if the customer is willing to close the dispute.
```

**T15 — Stripe Chargeback Response Template**

```
DISPUTE RESPONSE — Order [ORDER] — $[AMOUNT]

SUMMARY:
The customer [NAME] placed order [ORDER] on [DATE] for [PRODUCT]. The product
was fulfilled and delivered to the customer's address. We believe this dispute
was filed in error.

EVIDENCE PROVIDED:
1. Order confirmation (attached) — dated [DATE]
2. Customer's billing and shipping address match
3. Tracking number [NUMBER] via [CARRIER]
4. Delivery confirmation — marked delivered [DATE] to [CITY, STATE ZIP]
5. Product photos matching listing description (attached)
6. Our return policy (attached) — customer did not contact us before filing

RESOLUTION:
We attempted to contact the customer at [EMAIL] on [DATE] to resolve before
the dispute escalated. No response was received.

We stand by the legitimacy of this transaction and request the dispute be
resolved in our favor.
```

---

## CATEGORY 6: MISCELLANEOUS

**T16 — Cancel Order (Unfulfilled)**
```
Subject: Re: Cancel Order #[ORDER]

Hey [Name],

Cancelled and refunded. You'll see $[AMOUNT] back on your [PAYMENT METHOD]
within 5-7 business days.

Sorry it didn't work out — feel free to order again if you change your mind.

[Name]
[Brand] Support
```

**T17 — Cancel Order (Already Shipped)**
```
Subject: Re: Cancel Order #[ORDER]

Hey [Name],

Your order shipped [DATE] — I can't intercept it at this point.

When it arrives, I'll send a return label and refund you in full as soon as
it's back with us. You won't be out of pocket.

[Name]
[Brand] Support
```

**T18 — Wholesale / Bulk Inquiry**
```
Subject: Re: Wholesale Inquiry

Hey [Name],

We do offer bulk pricing for orders of 50+ units.

Send me:
- Which product(s) you're interested in
- Approximate quantity needed
- Shipping destination

I'll get you a quote within 24 hours.

[Name]
[Brand] Support
```

**T19 — Affiliate / Collab Inquiry**
```
Subject: Re: Partnership Opportunity

Hey [Name],

Thanks for reaching out.

We run an affiliate program at [RATE]% commission per sale. If that's a
fit, here's the signup link: [LINK]

For brand collaborations, send your media kit and engagement stats to
[EMAIL] — we review monthly.

[Name]
[Brand] Support
```

**T20 — Generic Angry Customer (De-escalation)**
```
Subject: Re: Order #[ORDER]

Hey [Name],

I hear you — and I want to fix this.

Can you tell me specifically what happened? Once I understand the issue, I
can give you a concrete solution rather than a runaround.

I have access to everything: refunds, replacements, store credit — I just
need to understand what went wrong first.

[Name]
[Brand] Support
```

---

## Response Speed Optimization

**Tidio chatbot auto-responses (no human needed):**
- "Where is my order" → T02 template auto-filled with order data
- "How do I return" → T05 template
- "What are your shipping times" → T11 template
- "Do you have [SIZE/COLOR]" → T12 template (manual review if OOS)

**Gorgias macro setup:**
- Create one macro per template above
- Tag tickets: WISMO, RETURN, DAMAGED, DISPUTE, GENERAL
- SLA rules: DISPUTE tag = 12h SLA, all others = 24h SLA
- Auto-close tickets with 5-star responses after 3 days no reply
