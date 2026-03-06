# Email Segmentation Strategy

Platform: Beehiiv (primary) / ConvertKit (alternative)
Goal: Right message to right person at right time — without extra work

---

## WHY SEGMENTATION MATTERS (NUMBERS)

Unsegmented blast: 21% open rate, 1.8% click rate
Segmented sends: 39% open rate, 5.4% click rate (industry data, Mailchimp 2024)
Revenue impact: segmented lists generate 760% more revenue per send (DMA)

The math on 1,000 subscribers:
- unsegmented: 210 opens, 18 clicks, ~$54 revenue per send (avg $3 RPE)
- segmented: 390 opens, 54 clicks, ~$162 revenue per send
difference: $108/send from same list

---

## TIER 1: SOURCE SEGMENTATION (Do This First)

Tag subscribers by HOW they joined. Source predicts intent.

| Source Tag | Intent Level | Best Sequence |
|---|---|---|
| cold_email_playbook | Cold email buyer | Seq 1 (cold email → client) |
| newsletter_organic | Engaged reader | Seq 2 (welcome → paid tier) |
| lead_magnet_template | Product buyer intent | Seq 3 (lead mag → paid product) |
| trial_signup | Purchase intent | Seq 4 (trial → paid) |
| event_attendee | High intent, deadline-driven | Seq 10 (event follow-up) |
| referral | Trust transfer, high LTV | Custom: skip 3 warm-up emails |
| paid_ad | Price-sensitive, needs proof | Custom: proof-heavy sequence |
| organic_social | Low urgency, needs nurturing | Seq 2 + extended timeline |

**Setup in Beehiiv:**
- Each lead magnet gets its own landing page with UTM parameters
- Beehiiv captures UTM source → auto-tags on signup
- Tag name format: `source_[name]` and `joined_[YYYY-MM]`

---

## TIER 2: BEHAVIOR SEGMENTATION

Tag based on what subscribers DO after joining.

**Engagement tiers:**

| Tag | Trigger | List Treatment |
|---|---|---|
| engaged_active | Opens 3 of last 5 emails | Full send list |
| engaged_clicker | Clicked in last 30 days | Priority upsell candidates |
| cold_60 | No open in 60 days | Re-engagement sequence (Seq 6) |
| cold_90 | No open in 90 days | Final win-back or suppress |
| suppressed | No open in 120 days | Remove from main list |
| replied | Has replied to any email | VIP segment — personal tone |

**What to send each tier:**
- engaged_active: all emails, all sequences
- engaged_clicker: prioritize offers and product emails
- cold_60: re-engagement sequence only (no offers until re-engaged)
- suppressed: sunset or delete

**Rule:** Never send offers to cold_60 or cold_90 segments. Re-engagement sequence first. If they re-engage, move back to active segment.

---

## TIER 3: PRODUCT INTEREST SEGMENTATION

Tag by what they click. Tells you what they want to buy.

**Link click tracking:**
Set up tagged links in emails. Beehiiv/ConvertKit auto-tags on click.

| They Click | Tag Applied | Next Email Focus |
|---|---|---|
| any cold email content | interest_cold_email | Cold email products + sequences |
| any YouTube content | interest_youtube | YT courses + adsense strategies |
| any app/SaaS link | interest_saas | SaaS products + app offers |
| any ecom link | interest_ecom | POD, dropship, TikTok Shop |
| any free resource link | freebie_seeker | Needs more proof before offer |
| pricing page | high_intent_buyer | Trigger urgency follow-up within 24h |

**High-intent buyer automation:**
Trigger: clicked pricing page
Action: send "did you have any questions about [PRODUCT]?" within 4 hours
Result: 31% of these emails get a reply (vs 2% cold)

---

## TIER 4: PURCHASE HISTORY SEGMENTATION

Never upsell what they already have. Never undersell what they're ready for.

| Status Tag | Sequence |
|---|---|
| purchased_entry | Upsell sequence (Seq 8) |
| purchased_mid | Upgrade to annual or top tier |
| purchased_top | Retention + referral ask |
| refunded | Suppressed from offers for 90 days |
| churned | Win-back sequence after 30 days |

---

## SEGMENTATION AUTOMATION WORKFLOW

### Beehiiv Setup (Recommended)

**Step 1: Landing pages with UTM parameters**
- Each lead magnet: `?utm_source=cold_email_playbook&utm_medium=organic&utm_campaign=leadmag`
- Beehiiv captures this automatically

**Step 2: Tag-based automations**
```
Automation 1: On Subscribe
  IF source = cold_email_playbook → Add tag: source_cold_email → Start Sequence 1
  IF source = newsletter_organic → Add tag: source_organic → Start Sequence 2
  IF source = trial_signup → Add tag: source_trial → Start Sequence 4

Automation 2: On Click (pricing page)
  Tag: high_intent_buyer
  Delay: 4 hours
  Send: "quick question before you decide" email

Automation 3: Engagement check (runs weekly)
  IF last_open > 60 days AND NOT tag: cold_60 → Add tag: cold_60 → Start Sequence 6
  IF last_open > 90 days → Add tag: cold_90 → Pause all other sequences

Automation 4: On Purchase
  Add tag: purchased_[product_name]
  Remove from: pre-purchase sequences
  Start: post-purchase sequence
```

**Step 3: Weekly segment review (15 min)**
- Move cold_90 to suppressed if no re-engagement
- Check high_intent_buyer segment for manual follow-up
- Review source performance: which sources produce buyers?

---

## SEGMENTATION BY BUSINESS STAGE

Match sequence intensity to where the subscriber is.

**Pre-revenue (starting out):**
- Lead: curiosity + proof sequences
- Main ask: click to read case study
- Avoid: hard product sells before 3+ touches

**Early revenue ($0-$1K/mo):**
- Lead: specific tactics they can implement now
- Main ask: low-ticket product ($27-$97)
- Sequence: 5 emails, 1 ask on email 4

**Growing ($1K-$10K/mo):**
- Lead: systems + scale content
- Main ask: mid-ticket ($197-$497) or monthly subscription
- Sequence: 7 emails, 2 asks (soft on email 5, hard on email 7)

**Scaling ($10K+/mo):**
- Lead: leverage + exit + team building
- Main ask: high-ticket ($997+) or annual plan
- Sequence: custom — heavily personalized based on purchase history

---

## QUICK SEGMENTATION WINS (IMPLEMENT THIS WEEK)

1. **Add source tags immediately.** Every new signup gets a source tag. Takes 20 minutes to set up, saves months of confusion.

2. **Build a cold list segment.** Run a query for all subscribers with no open in 60 days. This is your re-engagement priority list. Send Sequence 6 to it today.

3. **Tag buyers vs non-buyers.** Two separate experiences. Non-buyers need proof. Buyers need value delivery + upsell. Never mix them.

4. **Track reply rates by segment.** The segment with the highest reply rate is your most engaged segment. Put your best content there.

5. **Suppress before sending offers.** Before any launch, suppress cold_60 and cold_90. Your open rates will go up. Your spam complaints will go down.

---

## PLATFORM COMPARISON

| Feature | Beehiiv | ConvertKit | Mailchimp |
|---|---|---|---|
| Tags | Yes | Yes | Lists (limited) |
| Automations | Yes | Yes (strong) | Basic |
| Link click tagging | Yes | Yes | Limited |
| Segmentation filters | Good | Excellent | Basic |
| Free tier | 2,500 subs | 1,000 subs | 500 subs |
| Paid from | $42/mo | $29/mo | $20/mo |
| Recommendation | Primary | Alternative | Avoid |

**Verdict:** Start on Beehiiv (better content experience + built-in monetization). If you need advanced automation logic, migrate to ConvertKit at 2,000+ subscribers.
