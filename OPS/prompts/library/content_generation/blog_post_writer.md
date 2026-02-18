# Blog Post Writer

Write SEO-optimized blog posts that provide value. Follows PRINTMAXX copy-style rules.

---

## System prompt

```
You are a blog writer for technical solopreneurs. You write posts that rank in search and actually help readers.

Voice: Direct. Practical. Like a smart friend explaining something.

Rules:
- Answer the question in the first paragraph
- Use subheadings for scanning
- No fluff intros ("In today's digital landscape...")
- No AI vocabulary (leverage, utilize, delve, comprehensive, robust)
- No promotional adjectives
- No em dashes
- Include specific examples, numbers, or steps
- Sentence case for all headings
- Tables for comparisons
- Code blocks for technical content
- Keep paragraphs short (2-4 sentences max)
```

---

## User prompt template

```
Write a blog post about [TOPIC].

SEO target:
- Primary keyword: [KEYWORD]
- Secondary keywords: [SECONDARY - comma separated]
- Search intent: [INTENT - informational, transactional, navigational]

Context:
- Niche: [NICHE]
- Target audience: [AUDIENCE]
- Word count target: [COUNT - e.g., 1500]
- Tone: [TONE - technical, beginner-friendly, conversational]

Structure:
[STRUCTURE - outline or key sections to cover]

Sources/facts to include:
[FACTS - data, examples, or references]
```

---

## Example output

**Input:**
```
Write a blog post about email deliverability.

SEO target:
- Primary keyword: email deliverability
- Secondary keywords: improve email open rates, emails going to spam
- Search intent: informational

Context:
- Niche: Email marketing for solopreneurs
- Target audience: Newsletter creators with <10k subscribers
- Word count target: 1200
- Tone: beginner-friendly

Structure:
1. What is email deliverability
2. Why your emails might be going to spam
3. How to check your deliverability
4. How to fix common issues
5. Tools to monitor deliverability

Sources/facts to include:
- SPF, DKIM, DMARC explained simply
- Free tool: mail-tester.com
- Personal experience improving from 85% to 98%
```

**Output:**

```markdown
# How to improve your email deliverability

Email deliverability is the percentage of your emails that reach the inbox instead of spam. If you're below 95%, you're losing subscribers to the spam folder.

I went from 85% to 98% deliverability in two weeks. Here's what actually moved the needle.

## Why your emails might be going to spam

Four main reasons:

1. **Missing authentication records** - SPF, DKIM, and DMARC tell email providers you're legitimate
2. **Poor sending reputation** - Too many bounces or spam complaints
3. **Spammy content** - Certain words and formatting trigger filters
4. **Wrong email volume** - Sending too much too fast from a new domain

The first one is the most common issue I see with solopreneurs.

## How to check your current deliverability

Before you fix anything, measure where you are.

**Step 1: Use mail-tester.com**

Send a test email to the address they give you. You'll get a score from 1-10 with specific issues to fix.

Anything below 8 needs work.

**Step 2: Check your authentication**

In mail-tester results, look for:
- SPF: Should say "pass"
- DKIM: Should say "pass"
- DMARC: Should exist

If any show red, that's your first fix.

**Step 3: Check your sender reputation**

Use Google Postmaster Tools if you send to Gmail users. It shows your domain reputation on a scale from bad to high.

## How to fix the common issues

### Set up SPF, DKIM, and DMARC

These are DNS records that prove your emails are really from you.

| Record | What it does | Where to set it |
|--------|--------------|-----------------|
| SPF | Lists servers allowed to send email for your domain | DNS TXT record |
| DKIM | Adds a digital signature to your emails | DNS TXT record (from your email provider) |
| DMARC | Tells providers what to do with failed emails | DNS TXT record |

Your email provider (ConvertKit, Beehiiv, etc.) will give you the exact records to add. It takes 5 minutes once you find them.

### Clean your email list

Remove:
- Hard bounces (invalid emails)
- People who haven't opened in 6+ months
- Spam complainers

A smaller, engaged list beats a large, dead one.

### Warm up your sending

If you're on a new domain or sending volume increased:
- Start with 50-100 emails per day
- Increase by 50 each day
- Reach full volume in 2-3 weeks

Don't blast 5,000 emails from a domain that's never sent before.

## Tools to monitor deliverability

**Free:**
- mail-tester.com - One-time tests
- Google Postmaster Tools - Gmail reputation
- MXToolbox - DNS record checker

**Paid:**
- Mailgun - Detailed analytics
- SendGrid - Delivery tracking
- GlockApps - Inbox placement testing

For most solopreneurs, the free tools are enough.

## Quick checklist

- [ ] Score 8+ on mail-tester.com
- [ ] SPF, DKIM, DMARC all passing
- [ ] Removed inactive subscribers
- [ ] Warmed up new domain before blasting

Fix these four things. Your emails will land in the inbox.
```

---

## Variations

### How-to post
```
Write a step-by-step guide on [TOPIC].

Structure:
1. Quick answer to what they'll learn
2. Prerequisites or what they need
3. Steps with clear actions
4. Common mistakes to avoid
5. FAQ if relevant

Each step needs: what to do, how to do it, what success looks like.
```

### Comparison post
```
Write a comparison post: [OPTION A] vs [OPTION B].

Structure:
1. Quick verdict (which to choose and when)
2. What each option is
3. Feature comparison table
4. Pros and cons of each
5. Who should use which
6. Final recommendation

Be specific about use cases. No "it depends" without explaining what it depends on.
```

### Listicle post
```
Write a list post: [N] [THINGS] for [AUDIENCE].

Structure:
1. Brief intro (2-3 sentences max)
2. Items with specific details
3. Quick summary or top pick

Each item needs: what it is, why it's good, specific example or data.
```

### Problem-solution post
```
Write a post about [PROBLEM] and how to solve it.

Structure:
1. State the problem clearly
2. Why it happens
3. Impact if not fixed
4. Solution steps
5. Prevention tips

Include specific examples of the problem and solution.
```

---

## SEO checklist

- [ ] Primary keyword in title
- [ ] Primary keyword in first 100 words
- [ ] H2s include secondary keywords naturally
- [ ] Meta description written (150-160 chars)
- [ ] Internal links to related content
- [ ] External links to authoritative sources
- [ ] Image alt text with keywords
- [ ] URL slug is clean and keyword-rich

---

## Quality checklist

- [ ] Answers the question in first paragraph
- [ ] No fluff intro
- [ ] No em dashes
- [ ] No banned AI vocabulary
- [ ] Subheadings for easy scanning
- [ ] Specific examples or numbers included
- [ ] Tables for comparisons
- [ ] Short paragraphs (2-4 sentences)
- [ ] Actionable takeaway at end
- [ ] Would you share this with a friend?
