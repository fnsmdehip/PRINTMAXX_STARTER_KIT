# Email Sequences - PRINTMAXX

**Created:** 2026-01-21
**Status:** Ready to use
**Format:** Plain text (per ALPHA021)

---

## Overview

Three complete email sequences for PRINTMAXX list:

1. **Welcome Sequence** (5 emails) - Onboard new subscribers
2. **Launch Sequence** (4 emails) - Product launches
3. **Re-engagement Sequence** (3 emails) - Win back inactive subscribers

**Total:** 12 emails across 3 sequences

---

## File Locations

```
EMAIL/sequences/
├── welcome_sequence.md (5 emails)
├── launch_sequence.md (4 emails)
└── reengagement_sequence.md (3 emails)
```

---

## Sequence Details

### Welcome Sequence (5 emails)
**Purpose:** Build trust, deliver value, soft pitch
**Timing:** Days 0, 2, 4, 7, 10

1. Welcome + what to expect
2. Quick win (3-tool content stack)
3. Value bomb (distribution system)
4. Story + credibility ($200 to $3k in 90 days)
5. Soft pitch (PRINTMAXX OS preview)

**Target metrics:**
- Open rate: 40-60% (Email 1), 30-45% (Emails 2-5)
- Click rate: 5-10%
- Reply rate: 2-5%

### Launch Sequence (4 emails)
**Purpose:** Convert warm leads to buyers
**Timing:** Days 0, 2, 4, 6

1. Announcement (product is live)
2. Features + benefits (what's inside)
3. Social proof (what people are building)
4. Last chance (price increase + deadline)

**Target metrics:**
- Open rate: 30-50% (Email 1), 25-40% (Emails 2-4)
- Click rate: 5-10%
- Conversion rate: 3-8%

### Re-engagement Sequence (3 emails)
**Purpose:** Clean list + win back inactive subscribers
**Timing:** Days 0, 3, 7
**Trigger:** 60+ days no opens

1. Miss you + value recap
2. What's new (results update)
3. Special offer (30% off + last chance)

**Target metrics:**
- Re-activation rate: 5-10%
- Win-back conversion: 1-3%
- List removal: 80-90% (this is good)

---

## Copy Quality Checklist

All sequences verified for:
- [x] Zero em dashes
- [x] Zero banned AI vocabulary
- [x] No "It's not just X, it's Y" constructions
- [x] No vague attributions
- [x] No promotional adjectives
- [x] Sentence case headings
- [x] Direct statements (minimal hedging)
- [x] PRINTMAXXER voice (practical, specific, honest)
- [x] Plain text format
- [x] Specific numbers over vague claims

---

## Technical Implementation

### ESP Setup
- Format: Plain text (no HTML)
- Personalization: [NAME] variable
- Send from: personal domain (not ESP domain)
- Reply-to: actual email you monitor

### Deliverability Protocol
- Warm sending: 10/day → 100/day over 2 weeks
- Include physical address (CAN-SPAM)
- Clear unsubscribe link
- Monitor bounce rate (<2%)
- Monitor spam complaints (<0.1%)

### Tracking Setup
Add to `LEDGER/EMAIL_METRICS.csv`:
- sequence_name
- email_number
- sent_count
- open_count
- click_count
- reply_count
- unsubscribe_count
- conversion_count (if applicable)
- sent_date

### Segmentation Tags
After sequences, tag subscribers:
- `welcome_completed` (finished welcome sequence)
- `product_buyer` (purchased from launch)
- `re_engaged` (clicked in re-engagement sequence)
- `inactive_removed` (cleaned from list)

---

## Usage Instructions

### Welcome Sequence
**When to use:** Every new subscriber
**Trigger:** Immediately after email capture
**Next step:** Move to regular content emails

### Launch Sequence
**When to use:** Product launches
**Prerequisites:**
- Subscribers completed welcome sequence OR
- Existing list (warm)
**Next step:**
- Buyers → customer onboarding
- Non-buyers → regular content

### Re-engagement Sequence
**When to use:** Quarterly list cleaning
**Prerequisites:** Subscriber inactive 60+ days
**Next step:**
- Re-engaged → regular content
- No action → remove from list

---

## Personalization Variables

All sequences use:
- `[NAME]` - First name (fallback: "there")

Optional additions:
- `[PRODUCT]` - Product name
- `[PRICE]` - Product price
- `[DEADLINE]` - Offer deadline

---

## A/B Testing Recommendations

### Welcome Sequence
Test Email 1 subject lines:
- "You're on the list" (current)
- "What to expect from PRINTMAXX"
- "No AI cringe here"

### Launch Sequence
Test Email 4 scarcity:
- Price increase (current)
- First 100 buyers bonus
- Launch week only

### Re-engagement Sequence
Test Email 3 offer:
- 30% off (current)
- $30 off
- Free bonus instead of discount

---

## Compliance Notes

### FTC
- All claims substantiated
- No fake testimonials
- Income claims include disclaimer
- Digital product clearly stated

### CAN-SPAM
- Physical address in footer
- Clear unsubscribe mechanism
- No misleading subject lines
- Honor unsubscribes within 10 days

### Refund Policy
- 30-day guarantee (welcome/launch)
- Requires proof of use
- No argument refunds (builds trust)
- Process within 48 hours

---

## Next Steps

1. **Import to ESP**
   - Upload sequences to email platform
   - Set up automation triggers
   - Configure personalization variables

2. **Test Send**
   - Send to personal email
   - Check formatting
   - Verify links work
   - Test on mobile

3. **Launch**
   - Start with 10 subscribers (test)
   - Monitor metrics daily
   - Scale after 1 week

4. **Iterate**
   - A/B test subject lines
   - Track sequence completion rate
   - Adjust timing if needed
   - Update based on replies

---

## Performance Benchmarks

### Good Performance
- Open rate: 30%+
- Click rate: 3%+
- Reply rate: 1%+
- Conversion (launch): 3%+
- Unsubscribe: <1%

### Excellent Performance
- Open rate: 40%+
- Click rate: 5%+
- Reply rate: 2%+
- Conversion (launch): 5%+
- Unsubscribe: <0.5%

If underperforming:
- Check deliverability (spam folder?)
- Test different subject lines
- Shorten email body
- Simplify CTA

---

## Files Integration

These sequences integrate with:
- `LEDGER/EMAIL_METRICS.csv` - Performance tracking
- `LEDGER/leads.csv` - Subscriber data
- `LEDGER/FUNNEL_METRICS.csv` - Conversion tracking
- `EMAIL/sequence_v1.md` - Niche-specific sequences (AI, Faith, Fitness)
- `EMAIL/offer_copy_v1.md` - Landing page copy

---

*Last updated: 2026-01-21*
*Plain text. No fluff. Ship it.*
