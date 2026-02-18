# Cart Abandonment - 3-Email Recovery Sequence

**Purpose:** Recover sales from users who started checkout but didn't complete
**Trigger:** User reaches checkout page but doesn't purchase within 1 hour
**Works for:** All 3 products (AI Clarity Stack, Daily Anchor, 3-Hour Physique)

---

## Email 1: The reminder

**Send timing:** 1 hour after cart abandonment
**Segment:** Started checkout, did not complete

### Subject line
You left something behind

**A/B variants:**
- A: Your cart is waiting
- B: Did something go wrong?

### Preview text
Complete your order

### Body

Hey,

You started checking out for [PRODUCT_NAME] but didn't finish.

If something went wrong with the payment, let me know and I'll help sort it out.

If you just got distracted (happens to all of us), here's the link to pick up where you left off:

[Complete your order]

Your cart:
- [PRODUCT_NAME]: [PRICE]

The link above will take you straight to checkout. No need to start over.

[NAME]

### CTA button
Complete your order

---

## Email 2: The question

**Send timing:** 24 hours after cart abandonment
**Segment:** Started checkout, still not complete

### Subject line
Quick question about your order

**A/B variants:**
- A: Was it the price?
- B: What held you back?

### Preview text
I'd genuinely like to know

### Body

Hey,

You started an order for [PRODUCT_NAME] yesterday but didn't complete it.

I'm curious: what held you back?

Common reasons people don't finish:

**1. Price concern**
If $[PRICE] feels like a stretch right now, I get it. The product isn't going anywhere. It'll be here when the timing is better.

**2. Not sure it's right for you**
If you have questions about whether [PRODUCT_NAME] fits your situation, reply to this email. I read everything and can give you an honest answer.

**3. Just got busy**
Life happens. Here's the link to finish: [Complete your order]

**4. Something technical broke**
If checkout didn't work, let me know what happened and I'll fix it.

No pressure. Just wanted to check in.

[NAME]

### CTA button
Complete your order

### PS
If you decided it's not for you, totally fine. Just reply "not interested" and I'll stop these reminders.

---

## Email 3: The final chance

**Send timing:** 72 hours after cart abandonment
**Segment:** Started checkout, still not complete

### Subject line
Last reminder about your cart

**A/B variants:**
- A: Final chance: [PRODUCT_NAME]
- B: Closing your cart

### Preview text
After this, I'll stop asking

### Body

Hey,

This is the last email about your abandoned cart for [PRODUCT_NAME].

Quick recap of what you'd get:

[PRODUCT-SPECIFIC BULLET POINTS]

**For AI Clarity Stack:**
- Stack Audit Framework
- 12 Automation Templates
- 47 Tested Prompts
- Tool Decision Matrix
- 30-day guarantee

**For Daily Anchor System:**
- 30-Day Verse Guide
- Morning Template
- 4 Audio Devotions
- Habit Tracker
- 30-day guarantee

**For 3-Hour Physique:**
- 12-Week Program (36 workouts)
- Exercise Video Library
- Nutrition Guide
- Progress Tracker
- 12-week guarantee

Price: $[PRICE]

If you want it, here's the link: [Complete your order]

If not, no worries. I won't email about this again.

[NAME]

### CTA button
Complete your order

---

## Product-specific variables

| Variable | AI Clarity Stack | Daily Anchor | 3-Hour Physique |
|----------|------------------|--------------|-----------------|
| PRODUCT_NAME | AI Clarity Stack | Daily Anchor System | 3-Hour Physique |
| PRICE | $47 | $27 | $47 |
| SENDER | hello@stackpilot.ai | hello@dailyanchor.co | hello@3hourphysique.com |

---

## Sequence metrics to track

| Metric | Target |
|--------|--------|
| Email 1 open rate | 60%+ |
| Email 1 recovery rate | 15%+ |
| Email 2 recovery rate | 8%+ |
| Email 3 recovery rate | 5%+ |
| Total sequence recovery | 25-30% |

---

## Automation notes

- Trigger: checkout page visited + no purchase within 60 minutes
- Stop sequence immediately if purchase is made
- Tag recovered customers as "cart_recovery_[product]"
- After sequence: return to regular nurture with 48-hour gap
- Track which email converted for optimization
- If user replies "not interested," remove from sequence and tag accordingly
- Consider adding urgency (limited quantity, price increase) for Email 3 during promotions

---

## A/B test priority

1. Email 1 subject line (highest volume, test first)
2. Email 2 send timing (try 12 hours vs 24 hours)
3. Email 3 urgency elements (with discount vs without)

---

## Discount variant (use sparingly)

For Email 3, optional discount version:

### Subject line
10% off to complete your order

### Body addition after recap:

I don't usually do this, but since you got this far, here's 10% off to finish your order.

Use code: COMEBACK10

Link: [Complete your order with discount]

This code expires in 24 hours.

**Note:** Only use discount variant if recovery rates drop below 20%. Frequent discounts train customers to abandon carts.
