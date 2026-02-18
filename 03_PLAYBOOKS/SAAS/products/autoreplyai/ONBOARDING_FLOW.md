# AutoReplyAI Onboarding Flow

**Last updated:** 2026-01-20

---

## Overview

Goal: Get users to their first successful AI response in under 10 minutes.

Key metric: Time to first automated conversation
Target: Under 10 minutes from signup

---

## Step 1: Signup (2 minutes)

### Screen: Create account

**Fields:**
- Email address
- Password
- Company name (optional)

**CTA:** Create free account

**After submit:**
- Send verification email
- Show "Check your email" screen
- Auto-progress to Step 2 if email verified within 2 minutes

### Email: Verification

**Subject:** Verify your AutoReplyAI account

**Body:**
Click to verify: [button]

That's it. Once verified, you're 10 minutes from your first automated reply.

Questions? Reply to this email.

---

## Step 2: Add your knowledge (3 minutes)

### Screen: What do you want the AI to know?

**Headline:** Teach the AI about your business

**Options (pick one or more):**

1. **Paste your FAQ** - Copy/paste existing FAQ text
2. **Upload documents** - PDF, DOCX, TXT (max 10MB each)
3. **Enter your website URL** - We'll crawl your help pages
4. **Start from scratch** - Use our template

**Tip text:** Start with 5-10 common questions. You can add more later.

**CTA:** Continue

### Processing screen

**Text:** Reading your content... (usually takes 30-60 seconds)

**Progress indicators:**
- Scanning documents...
- Extracting key information...
- Building knowledge base...
- Done!

---

## Step 3: Test the AI (2 minutes)

### Screen: Try it yourself

**Headline:** Ask a question your customers would ask

**Interface:**
- Chat preview on right side
- "Try these" suggestions on left:
  - "What's your return policy?"
  - "How do I track my order?"
  - "What are your business hours?"

**Instruction:** Type a question and see how the AI responds.

**After first test:**
- Show quality rating: "Was this response good?" (thumbs up/down)
- If thumbs down: "What was wrong?" (text field)
- Edit response option

**CTA:** Looks good, continue

---

## Step 4: Install the widget (3 minutes)

### Screen: Choose how to connect

**Headline:** Where should the AI answer questions?

**Options:**

**Option A: Website widget**
- Copy this code to your site (one-liner)
- Or: "I use Webflow / Squarespace / WordPress" (specific instructions)
- Preview: Show what widget looks like

**Option B: Slack**
- Click to connect Slack workspace
- Select channels for bot to monitor

**Option C: Email**
- Forward emails to: inbox-xyz@autoreplyai.io
- Or: Connect Gmail / Outlook directly

**CTA:** I've installed it

### Verification screen

**For widget:** "We're checking your site for the widget..."
- Success: "Found it! Widget is live on [yoursite.com]"
- Not found: "We couldn't find the widget yet. Need help?"

**For Slack:** "Bot connected! Send a message in #[channel] to test"

**For email:** "Send a test email to check the connection"

---

## Step 5: Go live (1 minute)

### Screen: You're ready

**Headline:** Your AI is live

**Summary:**
- Knowledge base: [X] documents, [Y] questions indexed
- Connected to: [Widget / Slack / Email]
- Plan: Free (100 conversations/month)

**Quick actions:**
- View your dashboard
- Customize widget appearance
- Invite team members
- Upgrade plan

**CTA:** Go to dashboard

---

## Onboarding emails

### Email 1: Welcome (immediate)

**Subject:** Your AI support agent is ready

**Body:**
You just set up AutoReplyAI. Here's what happens next:

1. Customers ask questions on your [widget/Slack/email]
2. AI answers using your knowledge base
3. You review conversations in your dashboard

Your first task: Send yourself a test message to see it work.

[Go to dashboard]

---

### Email 2: Day 1 (24 hours later)

**Subject:** Did you get your first question?

**Body:**
Quick check-in:

If you got your first AI-answered question: Great. Review the response and correct anything off.

If not: Here's how to get traffic to your chat widget:
- Add link to your email signature
- Add "Chat with us" to your website header
- Mention it in your next customer email

Most users get their first real conversation within 48 hours.

[View dashboard]

---

### Email 3: Day 3 (if no activity)

**Subject:** Need help setting up?

**Body:**
I noticed you signed up but haven't had any conversations yet.

Common reasons this happens:

1. Widget not installed correctly - [Check installation]
2. Need help uploading docs - [Upload guide]
3. Just haven't had time - No problem, your account is waiting

Reply to this email if you're stuck. I'll help you get running.

---

### Email 4: Day 7 (engagement summary)

**Subject:** Your first week: [X] questions answered

**Body:**
Here's your AutoReplyAI summary:

- Questions answered by AI: [X]
- Questions routed to you: [Y]
- Automation rate: [Z]%
- Time saved: ~[N] hours

[View full report]

Top questions customers asked:
1. [Question 1]
2. [Question 2]
3. [Question 3]

Tip: If any of these were answered incorrectly, edit them in your dashboard. The AI learns from corrections.

---

### Email 5: Day 14 (upgrade prompt, if on free)

**Subject:** You're at [X]/100 conversations this month

**Body:**
You've used [X] of your 100 free conversations.

At your current pace, you'll hit the limit in [Y] days.

What happens at the limit: New questions go directly to your inbox instead of the AI.

Options:
- Upgrade to Pro ($29/mo) for 1,000 conversations
- Stay on free and handle overflow manually

[See pricing]

No pressure. Free plan works for low-volume support.

---

## In-app tooltips (first session)

### Dashboard first visit
"This is your conversation feed. Click any conversation to see details."

### First conversation click
"Here's the full conversation. Click 'Edit response' if the AI got something wrong."

### Knowledge base first visit
"This is everything your AI knows. Add more docs or edit existing content anytime."

### Settings first visit
"Customize your widget colors, set confidence thresholds, and manage integrations here."

---

## Success metrics

Track these for onboarding optimization:

| Metric | Target | Current |
|--------|--------|---------|
| Signup to first test | < 5 min | TBD |
| Signup to widget installed | < 15 min | TBD |
| Signup to first real conversation | < 48 hrs | TBD |
| Onboarding completion rate | > 60% | TBD |
| Day 7 retention | > 40% | TBD |
| Free to paid conversion | > 5% | TBD |

---

## Drop-off recovery

### If user abandons at Step 2 (knowledge upload)
- Email after 1 hour: "Quick way to get started: just paste your FAQ"
- Include link directly to FAQ paste screen

### If user abandons at Step 4 (installation)
- Email after 24 hours: "Need help installing? Here's a 2-min video"
- Include installation guide for their platform (if known)

### If user completes onboarding but no real conversations after 48 hours
- Email: "Your widget might not be visible. Here's how to check"
- Include troubleshooting checklist
