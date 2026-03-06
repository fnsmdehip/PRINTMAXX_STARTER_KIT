# A/B Test Registry — 20 Tests to Run

**Purpose:** Systematic testing beats gut feel. Every assumption about content, pricing, copy, and distribution is testable. This document defines 20 tests, the hypothesis, how to run it, and what to measure.

**Methodology:**
- Run each test for minimum 14 days (content tests) or 7 days with 100+ impressions (copy tests)
- Only change ONE variable per test
- Document results in LEDGER/AB_TEST_RESULTS.csv
- Act on results immediately. If B wins, replace A with B as default.

---

## BATCH 1: CONTENT TESTS (X/Twitter)

### Test 1: Thread Format vs Single Long Post
**Hypothesis:** Single long posts (Premium 25K chars) outperform threads for depth content because algorithm treats them as one unit instead of penalizing continuation tweets.
**Variable A:** 7-tweet thread on same topic
**Variable B:** Single long-form post (1,500-2,000 chars) covering same ground
**Measure:** Impressions, profile visits, bookmark rate per 1K impressions
**Run:** 14 days, 5 examples each format
**Win condition:** >20% improvement in bookmark rate

---

### Test 2: Hook Type — Consequence-First vs Question
**Hypothesis:** Consequence-first hooks ("I 10x'd my cold email reply rate in 2 weeks") outperform question hooks ("Do you know why your cold emails aren't working?") because they deliver value immediately.
**Variable A:** "I [outcome] in [timeframe]" opener
**Variable B:** "Why do most [people] fail at [thing]?" opener
**Measure:** Click-to-profile rate, reply count, bookmark rate
**Run:** 14 days, 10 examples each
**Win condition:** >15% improvement in reply + bookmark combined

---

### Test 3: With vs Without External Link
**Hypothesis:** Posts without external links in body get 2x+ reach. Putting link in first comment captures most traffic with minimal reach penalty.
**Variable A:** Tweet with link in body
**Variable B:** Tweet with no link, "link in first reply" CTA, link in first comment
**Measure:** Impressions per post
**Run:** 7 days, 20 posts each
**Win condition:** B gets >50% more impressions

---

### Test 4: Posting Time — Morning vs Evening
**Hypothesis:** 8-9 AM EST posts get more reach due to lower competition but higher audience online; 7-9 PM EST posts get better engagement rate due to more casual browsing behavior.
**Variable A:** Post at 8:00 AM EST
**Variable B:** Post at 7:30 PM EST
**Measure:** Impressions (reach), likes + replies (engagement), bookmark rate
**Run:** 21 days, same content types posted at each time
**Win condition:** One time slot wins on either reach or engagement by >20%

---

### Test 5: With vs Without Image/Screenshot
**Hypothesis:** Static screenshots (revenue dashboards, code, tool UIs) outperform text-only posts on reach but text-only wins on retweet/quote rate.
**Variable A:** Text-only post
**Variable B:** Same post with screenshot attached
**Measure:** Impressions, replies, quote tweet rate
**Run:** 14 days, 10 examples each
**Win condition:** B wins on impressions by >30%; track whether engagement rate suffers

---

## BATCH 2: NEWSLETTER TESTS

### Test 6: Subject Line — Specificity vs Curiosity
**Hypothesis:** Specific subject lines ("How I got 47% reply rate on cold emails") outperform curiosity gaps ("I almost missed this") because the audience is self-selected high-signal readers who prefer substance.
**Variable A:** Specific, numbered subject: "3 tools that cut my workflow from 4 hours to 45 minutes"
**Variable B:** Curiosity gap subject: "What most people skip (and it's obvious)"
**Sample size:** Split to 500 subscribers each
**Measure:** Open rate, click-through rate, unsubscribe rate
**Win condition:** >5 percentage point open rate difference

---

### Test 7: Newsletter Length — Short Brief vs Deep Dive
**Hypothesis:** 400-word briefs with 1 core insight have higher click rates; 1,000-word deep dives have higher open-to-subscribe conversion.
**Variable A:** 400-word issue: one insight, one tool, one action
**Variable B:** 1,000-word issue: full case study, step-by-step
**Measure:** Open rate, click rate, reply rate, unsubscribe rate
**Run:** 4 issues each format (alternating)
**Win condition:** One format wins on 2+ metrics

---

### Test 8: CTA Placement — In Body vs at End
**Hypothesis:** CTA placed mid-newsletter (after the value, before the close) gets more clicks than CTA only at the end, because readers are still engaged.
**Variable A:** CTA at end of newsletter
**Variable B:** Same CTA placed mid-newsletter after the core insight
**Measure:** Click-through rate on CTA
**Run:** 6 issues each format
**Win condition:** >30% improvement in CTR

---

### Test 9: From Name — Personal vs Brand
**Hypothesis:** Emails from "Malik" (personal name) get higher open rates than emails from "PrintMaxx" (brand name) because inboxes feel personal.
**Variable A:** From: "PrintMaxx" reply-to: [email]
**Variable B:** From: "Malik from PrintMaxx" reply-to: [email]
**Measure:** Open rate
**Run:** 500 subscribers each for 1 issue
**Win condition:** >3 percentage point open rate difference

---

## BATCH 3: PRICING TESTS

### Test 10: Gumroad Product Pricing — Charm vs Round
**Hypothesis:** $17 (charm pricing) outperforms $20 (round) in conversion rate; $20 may outperform on revenue per sale if it signals higher value.
**Variable A:** $20 (round)
**Variable B:** $17 (charm)
**Measure:** Conversion rate, revenue per 100 visitors
**Run:** 500 page views each
**Win condition:** Revenue per 100 visitors (accounts for both conversion and price)

---

### Test 11: Fiverr Gig — 3-Tier vs 2-Tier Pricing
**Hypothesis:** Offering 3 tiers (Basic/Standard/Premium) creates anchoring effect where Standard becomes obvious choice; 2 tiers creates simpler decision.
**Variable A:** 3-tier gig ($49/$149/$299)
**Variable B:** 2-tier gig ($79/$249)
**Measure:** Order rate, average order value
**Run:** 30 days each configuration
**Win condition:** One version produces higher monthly revenue

---

### Test 12: Price Increase Test
**Hypothesis:** A 25% price increase on digital products will reduce orders by less than 25%, resulting in net revenue increase.
**Current price:** $X
**Test price:** $X * 1.25
**Measure:** Conversion rate before and after, revenue per week
**Run:** 30 days at new price
**Win condition:** Revenue per week stays flat or increases

---

## BATCH 4: LANDING PAGE TESTS

### Test 13: Headline — Outcome vs Process
**Hypothesis:** Outcome-focused headline ("Get your first client in 7 days") outperforms process-focused headline ("The cold email system that works in 2026").
**Variable A:** Process headline
**Variable B:** Outcome headline
**Measure:** Time on page, scroll depth, conversion rate
**Run:** 500 visits each
**Win condition:** >10% improvement in conversion rate

---

### Test 14: Social Proof — Numbers vs Quotes
**Hypothesis:** Specific numbers ("412 people have used this system") outperform testimonial quotes as social proof on landing pages.
**Variable A:** Testimonial quotes section (3 quotes)
**Variable B:** Numbers/statistics section ("412 users, 83% got first client in 14 days")
**Measure:** Conversion rate
**Run:** 500 visits each
**Win condition:** >5% improvement in conversion rate

---

### Test 15: CTA Button — Verb + Benefit vs Generic
**Hypothesis:** "Get the Cold Email System" outperforms "Buy Now" because it reinforces what the buyer is getting.
**Variable A:** "Buy Now" button
**Variable B:** "Get the [Specific Product Name]" button
**Measure:** Click-through rate on CTA button
**Run:** 500 visits each
**Win condition:** >10% improvement in CTA click rate

---

## BATCH 5: OUTREACH TESTS

### Test 16: Cold Email Length — 50 words vs 120 words
**Hypothesis:** 50-word ultra-short emails get higher reply rates because they signal respect for the reader's time; 120-word emails can convey more proof and get higher positive reply rates.
**Variable A:** 50-word email (problem + offer + CTA)
**Variable B:** 120-word email (hook + problem + proof + offer + CTA)
**Measure:** Open rate, reply rate, positive reply rate
**Sample size:** 200 emails each version to similar ICP
**Win condition:** One version gets >30% higher positive reply rate

---

### Test 17: Cold Email Subject — Question vs Statement
**Hypothesis:** Question subjects ("Quick question about [Company]") get higher open rates; Statement subjects ("I found 3 leads you're missing") get higher reply rates.
**Variable A:** "Quick question about [Company Name]"
**Variable B:** "[Company Name] — found something you might want"
**Measure:** Open rate, reply rate
**Sample size:** 200 emails each
**Win condition:** Either open rate or reply rate improves by >20%

---

### Test 18: Follow-Up Cadence — Day 3 vs Day 7
**Hypothesis:** Following up on Day 3 (while memory of first email is fresh) gets more replies than waiting until Day 7.
**Variable A:** Follow up on Day 7 after first email
**Variable B:** Follow up on Day 3 after first email
**Measure:** Reply rate on follow-up emails
**Sample size:** 100 leads each sequence
**Win condition:** >20% difference in follow-up reply rate

---

## BATCH 6: APP/PRODUCT TESTS

### Test 19: App Onboarding — Long vs Short
**Hypothesis:** A 3-step onboarding (Name → Goal → First task) retains users better than a 6-step onboarding (full profile setup) because less friction to first value moment.
**Variable A:** 6-step onboarding
**Variable B:** 3-step onboarding
**Measure:** Day 1 retention rate, Day 7 retention rate
**Run:** 200 signups each
**Win condition:** B wins on Day 7 retention

---

### Test 20: App Pricing Page — Monthly vs Annual Default
**Hypothesis:** Showing Annual pricing as the default selected option (with monthly as alternative) increases Annual plan uptake without reducing overall conversion.
**Variable A:** Monthly plan highlighted as default
**Variable B:** Annual plan highlighted as default (better value framed prominently)
**Measure:** Conversion rate, mix of monthly vs annual, LTV per conversion
**Run:** 200 pricing page views each
**Win condition:** Annual LTV per conversion increases by >20%

---

## Test Tracking Sheet

Record all results in `LEDGER/AB_TEST_RESULTS.csv`:

```
test_id, test_name, variable_a, variable_b, start_date, end_date,
primary_metric, result_a, result_b, winner, confidence, action_taken, notes
```

**Example row:**
```
T01, Thread vs Long Post, thread, long_post, 2026-03-10, 2026-03-24,
bookmark_rate, 2.3%, 3.8%, B, 65%, "switched to long-form for depth content", "need more samples"
```

---

## Result Application Rules

- Winner by >20%: Implement immediately as new default
- Winner by 10-20%: Test again with larger sample before implementing
- Winner by <10%: Not statistically meaningful, keep testing
- No winner: Investigate why. Usually means wrong metric, not that both are equal.
- Document every test result, even inconclusive ones. Patterns emerge over 10+ tests.
