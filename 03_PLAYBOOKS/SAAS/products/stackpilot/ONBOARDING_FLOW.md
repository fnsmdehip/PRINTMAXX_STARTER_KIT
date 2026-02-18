# StackPilot Onboarding Flow

**Last updated:** 2026-01-20

---

## Overview

Goal: Get users to save and run their first prompt in under 5 minutes.

Key metric: Time to first prompt run
Target: Under 5 minutes from signup

---

## Step 1: Signup (1 minute)

### Screen: Create account

**Fields:**
- Email address
- Password

**CTA:** Create free account

**Social login options:**
- Continue with Google
- Continue with GitHub

**After submit:**
- Email verification (optional, can skip for free tier)
- Proceed to Step 2

---

## Step 2: First prompt (2 minutes)

### Screen: Save your first prompt

**Headline:** Let's save a prompt

**Options:**

**Option A: Use a template**
- Show 3 popular templates:
  - "Blog post outline"
  - "Code review assistant"
  - "Email draft helper"
- Click to add to library

**Option B: Create your own**
- Blank prompt editor
- Example shown: "Write a {{tone}} email to {{recipient}} about {{topic}}"

**Option C: Import from chat**
- Paste a prompt you've used
- We'll detect variables automatically

**Tip text:** Don't overthink it. You can edit everything later.

**CTA:** Save prompt

---

## Step 3: Add variables (1 minute)

### Screen: Make it reusable

**Headline:** Add variables

**Interface:**
- Highlight text in your prompt
- Click "Make variable"
- Name the variable

**Example:**
- Original: "Write a professional email to John about the project deadline"
- With variables: "Write a {{tone}} email to {{recipient}} about {{topic}}"

**Preview:**
Show the form that will appear when running this prompt.

**Skip option:** "Skip for now" (variables can be added later)

**CTA:** Continue

---

## Step 4: Run the prompt (1 minute)

### Screen: Try it

**Headline:** Run your prompt

**Interface:**
- Form with variable fields (if any)
- Model selector: ChatGPT, Claude, Gemini
- Run button

**After run:**
- Show output in panel
- "Save output?" toggle
- Quality rating: "Was this helpful?" (thumbs up/down)

**CTA:** Done! Go to library

---

## Step 5: Library tour (30 seconds)

### Screen: Your library

**Headline:** This is your prompt library

**Quick tooltips (auto-dismiss):**
1. "All your prompts live here"
2. "Click any prompt to run it"
3. "Use folders to organize"
4. "Search to find prompts fast"

**CTA:** Got it

---

## Onboarding emails

### Email 1: Welcome (immediate)

**Subject:** Your prompt library is ready

**Body:**
You're set up. Here's what to do next:

1. Save 3-5 prompts you use regularly
2. Add variables to make them reusable
3. Create your first workflow (Pro feature)

Most users save 30+ minutes per week after organizing their prompts.

[Open StackPilot]

---

### Email 2: Day 1 (if < 3 prompts saved)

**Subject:** Quick tip: Save prompts you already use

**Body:**
I noticed you have [X] prompts saved.

Here's the fastest way to build your library:

1. Open ChatGPT or Claude
2. Copy a prompt you've used recently
3. Paste it into StackPilot
4. Add variables for the parts that change

Takes 30 seconds per prompt. Do it for 5 prompts and you'll feel the difference.

[Add a prompt]

---

### Email 3: Day 3 (if using free tier)

**Subject:** What you're missing on Free

**Body:**
On Free, you get:
- 50 prompts
- 1 AI model
- Basic folders

On Pro ($19/month):
- Unlimited prompts
- All AI models
- Workflow builder
- Browser extension

If you use AI daily, Pro pays for itself in time saved.

[Try Pro free for 7 days]

---

### Email 4: Day 7 (engagement summary)

**Subject:** Your first week: [X] prompts saved

**Body:**
Here's your StackPilot summary:

- Prompts saved: [X]
- Prompts run: [Y]
- Most used: [Prompt name]
- Estimated time saved: [Z] minutes

[View your library]

Tip: Your most-used prompt is "[Prompt name]". Consider turning it into a workflow to automate even more.

---

### Email 5: Day 14 (Pro trial ending, if applicable)

**Subject:** Your Pro trial ends in 3 days

**Body:**
Quick reminder: Your trial ends on [date].

During your trial, you:
- Saved [X] prompts
- Ran [Y] workflows
- Used [Z] AI models

To keep these features, upgrade before [date].

[Upgrade to Pro - $19/month]

Not ready? No problem. You'll move to Free with 50 prompt limit.

---

## In-app tooltips (first session)

### Library first visit
"This is your prompt library. All saved prompts appear here."

### First prompt card
"Click any prompt to run it. Right-click to edit, duplicate, or delete."

### Folder sidebar
"Create folders to organize prompts by project or type."

### Search bar
"Search prompts by title, content, or tags."

### Workflow tab (Pro)
"Connect prompts into automated sequences. Output from one feeds the next."

---

## Success metrics

| Metric | Target | Current |
|--------|--------|---------|
| Signup to first prompt saved | < 3 min | TBD |
| Signup to first prompt run | < 5 min | TBD |
| Prompts saved in first week | > 5 | TBD |
| Day 7 retention | > 50% | TBD |
| Free to paid conversion | > 8% | TBD |

---

## Drop-off recovery

### If user abandons at Step 2 (first prompt)
- Email after 1 hour: "Here's a prompt template to start"
- Include direct link to template library

### If user saves prompts but never runs them
- Email after 24 hours: "Your prompts are waiting. Click to run your first one."
- Include "Run" button for their most recent prompt

### If user completes onboarding but doesn't return
- Email after 48 hours: "Import your existing prompts in 2 minutes"
- Include import guide and CSV template

---

## Browser extension onboarding

### After extension install

**Popup message:**
"Extension installed! When you see a prompt in ChatGPT or Claude, click the StackPilot icon to save it."

### First save via extension

**Popup message:**
"Prompt saved to your library. [Open library] to see it."

### Variable detection

**Popup message:**
"We detected {{variables}} in your prompt. [Edit variables] in your library."
