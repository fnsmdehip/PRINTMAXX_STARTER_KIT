# Growth Plan: A trader I know blew 5 accounts in 2 years.

Not small accou

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo (affiliate) + brand awareness for SoberStreak

---

## Tactics

1. Apply hook template: '$X lost over N years. Same pattern every time: [A]. [B]. [C]. He knew. He just couldn't stop. Then he tried something different.' — fill in for SoberStreak (days sober relapsed), FocusLock (hours wasted), habit apps
2. Quote-tweet TradeZella's post with SoberStreak angle: 'Same psychology. Different vice.' — borrow their viral momentum
3. Check TradeZella affiliate program — trading journal tools pay $30-100/referral, content already primed
4. Create a 5-part thread series using real failure pattern data from our apps for social proof

## Budget Tier Strategies

### FREE
Run hook template through engagement_bait_converter.py — generate 10 posts for SoberStreak/FocusLock/habit apps using the [loss numbers] + [pattern] + [cliffhanger] frame. Post 3x/week. QT TradeZella for momentum.

### LOW
$0-50/mo — boost 1-2 best-performing posts at $5-10 each targeting r/trading, r/stopdrinking, r/productivity audiences

### MID
$50-200/mo — micro-influencer in trading/sobriety niche posts the same hook framing with SoberStreak CTA

## Daily Actions

- [ ] Run: python3 AUTOMATIONS/engagement_bait_converter.py --method 'pattern-break failure hook' --apps soberstreak focuslock --count 10
- [ ] Add hook template to CONTENT/social/hook_library.md: '[N accounts/$X total]. Same pattern: [build-confidence-size-blow]. Knew it. Couldn't stop. Then: [product pivot].'
- [ ] Check TradeZella affiliate program URL for referral code — add to affiliate tracker
- [ ] Queue 3 SoberStreak posts using this frame to CONTENT/social/posting_queue/

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
