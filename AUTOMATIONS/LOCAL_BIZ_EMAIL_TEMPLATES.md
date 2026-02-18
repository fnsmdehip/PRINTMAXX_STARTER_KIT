# Local Business Website Outreach - Email Templates

Use these templates with data from the scraper CSV (`local_biz_prospects.csv`).

Replace placeholders with actual values from the CSV columns.

---

## Template 1: Mobile-Responsive Issue (No viewport)

**When to use:** `mobile_ready: False` in CSV

**Subject:** [Business Name] - mobile search question

```
Hi [Business Name] team,

Quick question: are you seeing customers find you on mobile?

I was searching for [category] in [city] on my phone and found your site at [url].

It's not showing up right on mobile (missing responsive design). That's 70% of local searches now.

I help [category] businesses fix this in 2 weeks. Usually runs $[budget_estimate].

Worth a 10-minute call?

[Your Name]
[Your Phone]
```

---

## Template 2: No SSL Certificate

**When to use:** `has_ssl: False` in CSV

**Subject:** Security warning on [Business Name] site

```
Hi [Business Name],

I found a security issue on your site ([url]).

Chrome is showing "Not Secure" warnings to visitors. That kills trust and Google rankings.

I can fix this in 24 hours for $200 (or include it in a full redesign for $[budget_estimate]).

Can I send you a screenshot of what customers see?

[Your Name]
[Your Phone]
```

---

## Template 3: Poor SEO Score

**When to use:** `seo_score: <50` in CSV

**Subject:** [Business Name] not showing up in Google?

```
Hi [Name],

I was searching Google for "[category] in [city]" and didn't see [Business Name] on page 1.

Checked your site at [url]. A few SEO issues:
[paste issues from notes column]

Most [category] businesses get 40% of calls from Google. If you're not on page 1, you're losing customers daily.

I can fix this in 2 weeks. $[budget_estimate]. Guarantee page 1 for your main keywords within 60 days or free revisions.

10-minute call to walk through it?

[Your Name]
[Your Phone]
```

---

## Template 4: Old/Outdated Site

**When to use:** `last_updated_estimate` shows 2020 or earlier

**Subject:** Quick question about [Business Name]

```
Hi [Team],

Are you still using the [Business Name] site at [url]?

I noticed it hasn't been updated since [year from last_updated_estimate]. Most customers assume that means you're closed or don't care.

Fresh website = more trust = more customers.

I help [category] businesses in [city] modernize their sites. 2 weeks, $[budget_estimate], includes mobile + SEO.

Worth exploring?

[Your Name]
[Your Phone]
```

---

## Template 5: No AI-SEO (Low ai_seo_score)

**When to use:** `ai_seo_score: <30` in CSV

**Subject:** [Business Name] missing from ChatGPT/Google AI

```
Hi [Name],

Big change happening: Google's AI search just launched. ChatGPT recommendations are replacing traditional search.

I checked [Business Name] at [url]. You're not showing up in AI results because your site is missing the new markup (schema.org).

Your competitors who add this get recommended by AI. You don't = you lose customers.

I can fix this in 1 week for $[budget_estimate]. Includes the AI markup plus mobile + SEO.

5-minute call?

[Your Name]
[Your Phone]
```

---

## Template 6: DIY Platform Limitations (Wix/Squarespace)

**When to use:** `tech_stack` contains "Wix" or "Squarespace"

**Subject:** Wix/Squarespace limiting [Business Name]?

```
Hi [Name],

Saw your site at [url] is built on [tech_stack].

Those platforms are fine for starting out. But they limit you:
- Slower load times (Google penalizes this)
- Can't fully customize for your [category] needs
- Monthly fees add up ($300/year vs $50/year hosting)

I migrate [category] businesses to custom WordPress sites. More control, better SEO, lower cost long-term.

Migration + redesign: $[budget_estimate]. Done in 2 weeks.

Interested in exploring?

[Your Name]
[Your Phone]
```

---

## Template 7: High Priority Prospect (Score <40, Active, Email Found)

**When to use:** `outreach_priority: HIGH` in CSV

**Subject:** [Business Name] - losing customers to Google?

```
Hi [Name],

I help [category] businesses in [city] show up in Google and convert visitors to customers.

Found [Business Name] at [url]. A few issues costing you customers:

[paste specific issues from notes - be direct]

Most [category] businesses get 5-10 new customers per month from their website. If you're getting fewer, something's broken.

I can fix this. 2 weeks. $[budget_estimate].

Before/after examples: [your portfolio link]

10-minute call this week?

[Your Name]
[Your Phone]
[Your website]
```

---

## Template 8: Direct Offer (No Fluff)

**When to use:** Any HIGH or MEDIUM priority prospect

**Subject:** $[budget_estimate] for new [Business Name] website

```
[Name],

Your site: [url]
Issues: [paste from notes]

I'll build you a new one:
✓ Mobile-ready
✓ Shows up in Google
✓ Modern design
✓ 2 weeks

$[budget_estimate].

Interested?

[Your Name]
[Your Phone]
```

---

## Template 9: Local Competitor Angle

**When to use:** When you have data on competitor sites in same city

**Subject:** [Competitor] is beating [Business Name] online

```
Hi [Name],

I was comparing [category] websites in [city].

[Competitor Name]'s site: Modern, mobile-ready, page 1 of Google
[Business Name]'s site: [issues from notes]

Your service might be better. But online, they look more professional.

I can level the playing field. New site in 2 weeks, $[budget_estimate].

Show you the comparison?

[Your Name]
[Your Phone]
```

---

## Template 10: Follow-Up (No Response After 3 Days)

**Subject:** Re: [Original Subject]

```
[Name],

Following up on my email about [Business Name]'s website at [url].

Still seeing these issues:
[paste 1-2 key issues]

If timing's not right, I get it. But this is costing you customers every day.

Even just a 5-minute call to point you in the right direction?

[Your Name]
[Your Phone]

P.S. If you're not interested, just let me know and I'll stop following up.
```

---

## Phone Script (If Email Doesn't Work)

**When to use:** `phone_if_found` has a number, email bounced or no response

```
Hi, this is [Your Name]. I'm trying to reach [Business Name/Decision Maker].

[If gatekeeper]: I sent an email about your website but wanted to follow up directly. Is [Name] available?

[If decision maker]: Hi [Name], I'm [Your Name]. I help [category] businesses in [city] get more customers online.

I found your site at [url] and noticed [1 specific issue - mobile/SSL/SEO].

That's usually costing [category] businesses 5-10 customers per month. Takes about 2 weeks to fix.

Do you have 5 minutes for me to explain what I found?

[If yes]: Great. So here's what I saw...

[If no]: No problem. Can I email you a quick audit? Takes 2 minutes to read. What's the best email?

[If not interested]: I understand. If things change in 3-6 months, should I follow up or are you all set?
```

---

## Advanced: Multi-Touch Sequence

**For highest value prospects (lawyers, doctors, score <30)**

### Day 1: Email (Template 7)
### Day 3: Follow-up email (Template 10)
### Day 5: Phone call (using script above)
### Day 7: Text message (if mobile number)

**Text:**
```
Hi [Name], [Your Name] here. Left VM about [Business Name] website. Worth a quick call? [Your Phone]
```

### Day 10: Final email

```
[Name],

Last email about [Business Name]'s website.

I found [issue]. You might not care. Or it might be costing you $10K+/year in lost customers.

If you want to know which, 5-minute call tells you.

Otherwise I'll assume you're all set and won't follow up again.

[Your Name]
[Your Phone]
```

---

## Response Handling

### "How much?"

```
Depends on scope. For [category] businesses, usually $[budget_estimate].

Can I show you examples and walk through what's included? 10 minutes?
```

### "Send me more info"

```
Sure. What specifically do you want to know?
- Pricing breakdown?
- Timeline?
- Examples of my work?
- How I'd fix [specific issue]?

Or easier: 5-minute call and I'll answer everything?
```

### "We just redesigned"

```
Got it. When did you launch?

[If recent]: Nice. Is it getting you the results you wanted? (Customers calling, showing up in Google)

[If they're happy]: Great, sounds like you're all set. Can I follow up in 6 months to see how it's going?

[If not getting results]: That's the issue I can help with. Might just need SEO work, not full redesign. Can I take a look?
```

### "Too expensive"

```
I get it. What's your budget?

[If they give number]: Let me see what I can do at [their budget]. Might mean phased approach - fix critical issues first, rest later.

[If no budget]: Fair enough. FYI these issues are probably costing you more than $[budget_estimate] in lost customers. But I understand budget constraints.

I can send you a DIY guide for fixing the critical stuff yourself. Would that help?
```

### "Not interested"

```
No problem. Mind if I ask - is it:
- Timing (not right now)?
- Budget?
- Already working with someone?
- Happy with current site?

[Based on answer, either accept gracefully or offer alternative]

Timing: "When should I follow up?"
Budget: "What if we did just the critical fixes?"
Happy: "Great. If anything changes, keep my info."
```

---

## Tracking Conversions

After sending emails, track in a spreadsheet:

| Business | Score | Template | Sent Date | Response? | Call Booked? | Closed? | Revenue |
|----------|-------|----------|-----------|-----------|--------------|---------|---------|
| Main St Dental | 32 | Template 7 | 2/6/26 | Yes | Yes | Yes | $1,500 |

**After 20+ outreach attempts, analyze:**
- Which scores convert best? (Focus there)
- Which templates get responses? (Use more)
- Which categories pay most? (Prioritize)
- What issues resonate most? (Lead with those)

---

## Legal/Compliance Notes

✅ **Legal (OK to say):**
- "Your site has SEO issues"
- "You're not showing up in Google"
- "Mobile-responsive design missing"
- "I can fix this in X weeks"

⚠️ **Requires proof (substantiate or don't claim):**
- "You're losing $X per month"
- "I'll get you to page 1 in X days"
- "Your competitors are beating you"

❌ **Don't say (unsubstantiated/false):**
- "I guarantee #1 ranking"
- "You'll definitely get X customers"
- "Google will penalize you" (unless true)

**FTC compliance:**
- If you use before/after examples, they must be real clients
- If you make income claims, have proof
- Disclose material connections (if you're affiliated with tools you recommend)
