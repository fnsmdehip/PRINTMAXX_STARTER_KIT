# Chapter 3: AI-Personalized Outreach at Scale With Claude

## What You'll Have After This Chapter

A system that produces personalized emails for each prospect in under 30 seconds — emails that reference specific details about their business, sound like you spent 10 minutes researching them, and cost $0 in tooling.

## Why Personalization Breaks Cold Email

The average decision-maker receives 120+ emails per day. They can detect a template in under 2 seconds. The delete-or-read decision happens based on two things:

1. **Subject line**: Does it look like it was written for ME?
2. **First sentence**: Does this person know anything about MY business?

If both answers are "no," your email is dead. If both are "yes," they read the rest.

Generic personalization ("I love what you're doing at [COMPANY]") is as bad as no personalization. It screams template. Real personalization references something specific enough that the recipient thinks "this person actually looked at my stuff."

## The Personalization Data Pipeline

Before you write any emails, you need personalization data for each prospect. This is the "Personalization Note" column from your spreadsheet in Chapter 2.

### What Makes Good Personalization

**Strong personalization (use these):**
- A specific article or blog post they wrote
- A recent LinkedIn post and your take on it
- A specific feature of their product/website
- A recent company milestone (funding, launch, hire, award)
- A specific number from their business (if publicly available)
- A mutual connection or shared community

**Weak personalization (avoid these):**
- "I love your website" (everyone says this)
- "Congrats on your recent growth" (vague)
- "I noticed you're in the [INDUSTRY] space" (obviously)
- "Great company you've built" (hollow)

### Gathering Personalization Data (2 minutes per prospect)

For each prospect, do this:

1. **Visit their website** (30 seconds): Note one specific thing — a product feature, a design choice, a piece of copy, a blog post title. Not "nice website" — something like "I noticed your checkout page has a progress bar with estimated delivery dates."

2. **Check their LinkedIn** (30 seconds): Read their most recent post. Note the topic and your genuine reaction. If they haven't posted, check their profile headline or About section for something specific.

3. **Check their Twitter** (30 seconds): Read their last 3-5 tweets. Find one you can reference.

4. **Check for news** (30 seconds): Google "[Company Name] news" or "[Person's Name] [Company Name]." Recent press coverage, podcast appearances, or events are gold.

Record the best data point in your spreadsheet's Personalization Note column.

Example entries:
- "Published article about CAC payback periods in SaaS on LinkedIn last week"
- "Website homepage loads in 7.2 seconds (GTmetrix), competitor loads in 1.8s"
- "Just launched a new product line on Shopify, announced it on Twitter March 3"
- "Speaking at SaaSOpen in June on pricing strategies"

## Using Claude for Personalization at Scale

Here's where the system gets powerful. Instead of writing each email from scratch, you use Claude to generate personalized emails from your data.

### The Master Prompt

This prompt produces consistently good cold emails. The key is giving Claude enough constraints that it can't produce slop.

```
I'm sending a cold email to a prospect. Write the email using the data below.

My service: [DESCRIBE WHAT YOU DO IN ONE SENTENCE]
My best result: [YOUR TOP CASE STUDY — specific numbers]

Prospect details:
- Name: {{FIRST_NAME}}
- Company: {{COMPANY}}
- Title: {{TITLE}}
- Personalization data: {{PERSONALIZATION_NOTE}}

Rules:
1. First sentence must reference the personalization data specifically — not generically
2. Second sentence connects their situation to the problem I solve
3. Third sentence states my result with a specific number
4. Fourth sentence is the CTA — a question, not a demand
5. Total email: under 75 words
6. Subject line: under 5 words, references them not me
7. No "I hope this finds you well"
8. No "I'd love to hop on a quick call"
9. No exclamation marks
10. No compliments that could apply to anyone
11. Tone: peer-to-peer, not salesperson-to-prospect
12. Sign off with first name only, no title or company
```

### Real Example

**Input data:**
- Name: Sarah
- Company: Bloom Skincare
- Title: Founder
- Personalization: "Just launched DTC Shopify store, mentioned struggling with paid ads on Twitter March 8"

**Output:**
```
Subject: Bloom's ad spend

Sarah,

Saw your tweet about the paid ads struggle after the Shopify launch. Most DTC skincare brands I've worked with were burning 40-60% of ad spend on audiences that would never convert.

I helped a similar brand (Glow Labs, $2M ARR) cut their CAC by 52% in 6 weeks by restructuring their Meta ad targeting around purchase-intent signals instead of interest-based audiences.

Would it be useful to see the exact targeting framework we used?

Alex
```

73 words. Specific reference. Specific result. Low-pressure CTA.

### The Batch Process

Here's how to personalize 50 emails in 30 minutes:

1. Open your prospect spreadsheet
2. Take 10 prospects at a time
3. Paste the master prompt into Claude with all 10 prospects' data
4. Ask Claude to generate all 10 emails at once

Modified batch prompt:

```
Generate 10 cold emails using my master template. Each email must be unique —
different first sentences, different angles, different CTAs.

My service: [DESCRIPTION]
My best result: [RESULT]

[Paste the master prompt rules from above]

Prospects:

1. Name: Sarah, Company: Bloom Skincare, Title: Founder
   Personalization: Just launched DTC Shopify store, struggling with paid ads (Twitter March 8)

2. Name: Marcus, Company: DevStack, Title: CEO
   Personalization: Published blog post about developer burnout, 200+ comments on HN

3. Name: Priya, Company: NutriPlan, Title: Co-founder
   Personalization: Website loads in 8.1 seconds, competitor MealPrep Pro loads in 1.4s

[Continue for all 10]
```

Claude generates all 10 emails in about 90 seconds. Review each one — spend 10-15 seconds per email checking that the personalization feels genuine and the CTA is clear. Adjust anything that feels off.

50 prospects = 5 batches = 30 minutes of your time.

### Quality Control Checklist

Before sending any AI-generated email, check:

- [ ] Does the first sentence reference something only THEY would recognize?
- [ ] Would this email make sense if sent to a different prospect? (If yes, it's too generic — rewrite)
- [ ] Is the result specific? (Not "improved results" but "cut CAC by 52%")
- [ ] Is the CTA a question they can answer with one sentence?
- [ ] Is it under 80 words?
- [ ] Does it sound like a human wrote it? (Read it out loud. If it sounds like AI, rewrite)

### Anti-Slop Vocabulary List

Tell Claude to never use these words in cold emails:

- "Leverage" (use "use")
- "Synergy" (delete)
- "Innovative" (prove it with a number instead)
- "Cutting-edge" (meaningless)
- "Circle back" (use "follow up")
- "Reach out" (you already did — you're emailing them)
- "Touch base" (use "check in")
- "In today's landscape" (delete)
- "Unlock" (delete)
- "Elevate" (delete)
- "Transform" (use "change" or better, describe the specific change)
- "Best-in-class" (everyone says this)

Add this to your prompt: "Do not use any corporate jargon, buzzwords, or filler phrases. Write like a smart friend sending a casual but professional email."

## Personalization Tiers

Not every prospect deserves the same level of personalization. Tier your list:

### Tier 1: High-Value Prospects (top 10%)

These are your dream clients. Spend 5-10 minutes per email. Research their business deeply. Reference multiple data points. Maybe record a 60-second Loom video showing something specific about their website you'd fix.

Expected response rate: 15-30%

### Tier 2: Good-Fit Prospects (middle 40%)

Solid matches for your service. Spend 2-3 minutes per email. One strong personalization data point. Use the Claude batch process.

Expected response rate: 5-12%

### Tier 3: Worth-a-Shot Prospects (bottom 50%)

They fit your ICP broadly but you don't have strong personalization data. Use a lighter template with just their name, company, and industry. Focus on a compelling result rather than deep personalization.

Expected response rate: 2-5%

The mistake most people make is treating all 500 prospects the same. Spend 80% of your personalization effort on Tier 1 and Tier 2. Tier 3 is volume — send enough and the numbers work even at low response rates.

## The Subject Line System

Subject lines determine whether your email gets opened. Here's what works in cold email:

**Format 1: Their company name**
- "Bloom Skincare" — simple, looks like internal communication
- Open rate: typically 45-65%

**Format 2: Mutual reference**
- "John mentioned you" — only if it's true
- Open rate: 55-75%

**Format 3: Specific observation**
- "Your checkout page" — references something specific
- Open rate: 40-55%

**Format 4: Short question**
- "Quick question" — overused but still works
- Open rate: 35-50%

**What fails:**
- "Increase Your Revenue by 300%" — spam filter instant kill
- "Exciting Opportunity for Bloom Skincare" — screams sales email
- Anything over 6 words
- Anything with ALL CAPS or emojis

Test 2-3 subject line formats across your first 100 sends. Track which gets the highest reply rate (not open rate — you're not tracking opens, remember). Double down on what works.

## Maintaining Authenticity

The point of using AI for personalization is speed, not deception. You're using it to say what you would say if you had 10 minutes per email instead of 30 seconds. The personalization data is real. The observations are real. The results you cite are real. Claude is just the writing assistant.

If at any point an email feels dishonest — you're claiming to have noticed something you didn't, or referencing a conversation that didn't happen — delete it and write that section manually.

The moment personalization feels fake, it performs worse than no personalization at all.

Next chapter: Seven proven email sequences with exact templates.
