# Campaign optimization playbook

How to diagnose and fix underperforming cold outbound campaigns.

## Diagnostic framework

### Step 1: Identify the problem

Look at your metrics and find where the funnel breaks:

| Metric | Target | Your number | Problem? |
|--------|--------|-------------|----------|
| Bounce rate | < 2% | ___% | |
| Open rate | > 50% | ___% | |
| Reply rate | > 5% | ___% | |
| Positive reply rate | > 2% | ___% | |
| Meeting rate | > 1.5% | ___% | |

### Step 2: Focus on the bottleneck

Fix problems in order:
1. High bounces → Fix list quality
2. Low opens → Fix deliverability or subject lines
3. Opens but no replies → Fix body copy
4. Replies but not positive → Fix targeting or offer
5. Positive but no meetings → Fix CTA or follow-up

## Problem: High bounce rate (> 3%)

### Symptoms:
- Many emails bouncing
- "Undeliverable" responses
- Email tool warnings

### Diagnosis:
- List data is old or inaccurate
- Using catch-all domains
- Role-based emails (info@, sales@)

### Fixes:

**Immediate:**
1. Stop campaign immediately (bounces hurt reputation)
2. Check which emails bounced
3. Remove bounced addresses from all lists

**Prevent future:**
1. Verify emails before sending (ZeroBounce, NeverBounce)
2. Remove catch-all addresses
3. Remove role-based addresses
4. Use fresher data sources
5. Target: < 2% bounce rate before scaling

**Tools:**
- ZeroBounce: $0.008/email
- NeverBounce: $0.008/email
- MillionVerifier: $0.0003/email (bulk)

## Problem: Low open rate (< 40%)

### Possible causes:

**1. Deliverability issues**

Symptoms:
- Opens dropped suddenly
- mail-tester.com score < 8/10
- Emails going to spam

Fixes:
- Check SPF, DKIM, DMARC
- Check blacklists (mxtoolbox.com)
- Reduce send volume
- Increase warmup
- Rest problem inboxes
- Use different domains

**2. Bad subject lines**

Symptoms:
- Opens consistently low across inboxes
- mail-tester score is fine
- Deliverability checks pass

Fixes:
- A/B test subject lines
- Try shorter subject lines (< 40 chars)
- Try personalization ({{company}}, {{firstName}})
- Avoid spam triggers (free, guarantee, etc.)
- Test question vs statement format

**3. Wrong send time**

Symptoms:
- Opens vary significantly by day
- Some days much worse than others

Fixes:
- Test different days (Tue-Thu usually best)
- Test different times (morning vs afternoon)
- Consider recipient time zone

### Subject line improvement checklist:
- [ ] Under 40 characters
- [ ] No spam trigger words
- [ ] Personalized or intriguing
- [ ] Sounds like a human wrote it
- [ ] Tested against alternatives

## Problem: Opens but low replies (< 3%)

### Possible causes:

**1. Irrelevant message**

Symptoms:
- Opens are fine
- Almost no replies
- No engagement at all

Fixes:
- Improve targeting (wrong ICP)
- Better personalization (not relevant to them)
- Clearer value proposition
- Stronger pain point

**2. Message too long**

Symptoms:
- Opens good
- Low replies across all campaigns
- Feedback that emails are "too salesy"

Fixes:
- Cut email length in half
- Remove unnecessary details
- One idea per email
- Target: Under 100 words

**3. No clear CTA**

Symptoms:
- Opens good
- Some positive sentiment in rare replies
- But no action taken

Fixes:
- Single, clear CTA
- Lower commitment ask
- Make it easy to say yes
- Test different CTAs

**4. Weak opening line**

Symptoms:
- Opens good
- But quick exits (no reply, no click)
- They read subject but not body

Fixes:
- First line must hook
- Personalized observation
- Question that makes them think
- Not a generic intro

### Copy improvement checklist:
- [ ] Personalized first line
- [ ] Clear value proposition
- [ ] Under 100 words
- [ ] Single CTA
- [ ] Sounds like a human

## Problem: Replies but not positive (< 40% positive)

### Symptoms:
- Getting replies
- But most are objections, not interested, wrong person

### Diagnosis:
- Targeting wrong people
- Offer doesn't resonate
- Wrong timing

### Fixes:

**Wrong person:**
- Review who's replying negatively
- Adjust ICP definition
- Better job title targeting
- Better company criteria

**Offer doesn't resonate:**
- Test different value propositions
- Different pain points
- Different outcomes
- More relevant case studies

**Wrong timing:**
- Focus on trigger events
- Seasonal timing
- Company stage matching

### Targeting improvement checklist:
- [ ] Clear ICP documented
- [ ] Job titles match decision makers
- [ ] Company size appropriate
- [ ] Industry relevance clear
- [ ] Timing/trigger events considered

## Problem: Positive replies but no meetings

### Symptoms:
- People say they're interested
- But don't book calls
- Ghost after positive reply

### Diagnosis:
- Too many steps to book
- Slow follow-up
- Interest cools off

### Fixes:

**Make booking easier:**
- Include calendar link in first reply
- Offer specific times
- Remove friction
- Simple scheduling tool (Calendly, Cal.com)

**Faster follow-up:**
- Respond within 4 hours
- Same day if possible
- Have templates ready

**Improve follow-up sequence:**
- If no response to booking link, follow up in 2 days
- Try different times
- Try phone/LinkedIn as alternative

### Follow-up template:

```
Thanks for your interest, {{firstName}}!

Here's my calendar to grab 15 minutes: [link]

Or if easier, are you free [specific day/time option]?
```

If no response after 2 days:

```
Hey {{firstName}}, just bubbling this up.

Here's that link again: [calendar]

Or just reply with a few times that work and I'll send an invite.
```

## Problem: Meetings but no opportunities

### Symptoms:
- Booking meetings
- But leads aren't qualified
- Low conversion to opportunity

### Diagnosis:
- Wrong people showing up
- Expectations misaligned
- Qualification issue

### Fixes:

**Better pre-qualification:**
- Ask qualifying questions before booking
- Confirmation email with agenda
- Clear what you offer and who it's for

**Better meeting prep:**
- Research the prospect before call
- Prepare relevant examples
- Know what "qualified" looks like

**Alignment check:**
- Does email promise match meeting agenda?
- Are you attracting right type of lead?
- Is your offer clear?

## Rapid optimization cycle

### Week-by-week optimization

**Week 1: Diagnose**
- Run campaign at low volume (200-300 emails)
- Measure all metrics
- Identify biggest bottleneck

**Week 2: Fix bottleneck**
- Implement 1-2 changes
- Continue running
- Compare to baseline

**Week 3: Validate**
- Did changes improve metrics?
- If yes, scale up
- If no, try different fix

**Week 4: Next bottleneck**
- Move to next problem
- Repeat cycle

### Continuous improvement loop

```
Measure → Diagnose → Hypothesize → Test → Implement → Repeat
```

## Emergency fixes

### If open rate crashes suddenly:
1. **Stop sending immediately**
2. Check mail-tester.com score
3. Check blacklists
4. If blacklisted: Rest domain 2 weeks, use different domain
5. If not blacklisted: Subject line problem, test new ones

### If reply rate drops suddenly:
1. Check if targeting changed
2. Check if list quality changed
3. Review recent emails for obvious issues
4. Roll back to previous working copy

### If meetings drop suddenly:
1. Check if your CTA changed
2. Check calendar link isn't broken
3. Check if confirmation emails going to spam
4. Review recent follow-up responses

## Optimization checklist

### Weekly review:
- [ ] Bounce rate < 2%?
- [ ] Open rate > 50%?
- [ ] Reply rate > 5%?
- [ ] Any campaigns need pausing?
- [ ] Any tests ready to call?

### Monthly review:
- [ ] Full funnel analysis
- [ ] Cost per meeting calculation
- [ ] ROI assessment
- [ ] Next optimization priorities
- [ ] Test roadmap for next month

## Quick fixes by symptom

| Symptom | Likely cause | Quick fix |
|---------|--------------|-----------|
| High bounces | Bad list | Verify before sending |
| Low opens | Subject line or deliverability | Test new subject lines |
| Opens but no replies | Copy or relevance | Shorter email, better personalization |
| Objection replies | Wrong targeting | Refine ICP |
| Interest but no meeting | Friction to book | Calendar link + specific times |
| Low meeting show rate | No confirmation/reminder | Confirmation email + reminder |

## Resources

### Free tools:
- mail-tester.com (deliverability check)
- mxtoolbox.com (blacklist check)
- Hemingway App (copy simplification)

### Paid tools:
- Glockapps (deliverability monitoring)
- Lavender (email coaching)
- Instantly/Smartlead (campaign analytics)

### Learning resources:
- Cold Email University (Instantly)
- The Cold Email Manifesto
- Cold Outreach Twitter/X community
