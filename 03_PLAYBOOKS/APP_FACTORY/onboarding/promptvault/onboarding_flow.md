# PromptVault Onboarding Flow

**App:** PromptVault
**Screens:** 4
**Goal:** Identify use case, personalize content, start trial, begin browsing
**Target conversion:** Trial start > 60% (freemium model, softer paywall)

---

## Screen 1: Use Case

**Screen name:** use_case
**Progress:** 1/4

### Copy

**Headline:** What do you use AI for?

**Body:** We'll show you the most relevant prompts first. Pick all that apply.

### Options (multi-select)

| Option | Icon | Category |
|--------|------|----------|
| Writing content | Pen | Writing |
| Coding & debugging | Code | Coding |
| Marketing & copy | Megaphone | Marketing |
| Research & analysis | Chart | Analysis |
| Creative projects | Lightbulb | Creative |
| Business & strategy | Briefcase | Business |
| Learning new things | Book | Learning |
| Just exploring | Compass | General |

### Image/Animation spec

Clean icons for each category. Soft color palette. Cards that highlight when selected.

### CTA

**Button text:** Continue
**Skip option:** Yes (small text "Show me everything")

---

## Screen 2: Interests

**Screen name:** interests
**Progress:** 2/4

### Copy

**Headline:** Get specific

**Body:** Based on your selection, which of these sound useful? We'll prioritize these prompts.

### Dynamic options based on Screen 1

**If Writing selected:**
- Blog posts & articles
- Email writing
- Social media captions
- Long-form content
- Editing & proofreading

**If Coding selected:**
- Debugging code
- Writing functions
- Code review
- Learning new languages
- Documentation

**If Marketing selected:**
- Ad copy
- Landing page copy
- SEO optimization
- Email sequences
- Product descriptions

**If Analysis selected:**
- Data analysis
- Market research
- Report summaries
- Competitor analysis
- Literature reviews

**If Creative selected:**
- Story writing
- Brainstorming ideas
- Image prompts
- Character development
- World building

**If Business selected:**
- Business plans
- Meeting notes
- Proposals
- Strategy docs
- SWOT analysis

**If Learning selected:**
- Explain concepts
- Quiz generation
- Study guides
- Tutoring
- Language learning

### Image/Animation spec

Checkbox list with category icons. Selected items get accent color highlight.

### CTA

**Button text:** Personalize my feed
**Skip option:** Yes (small text "Skip personalization")

---

## Screen 3: Trial

**Screen name:** paywall_trial
**Progress:** 3/4

### Copy

**Headline:** 500+ prompts. Free forever.

**Body:**
Browse and copy any prompt. No account needed.

Want AI to write prompts for you? Try Pro free for 7 days.

### Free vs Pro comparison

| Feature | Free | Pro |
|---------|------|-----|
| Browse 500+ prompts | Yes | Yes |
| Copy to clipboard | Yes | Yes |
| Save favorites | Yes | Yes |
| AI Prompt Improver | No | Yes |
| AI Prompt Generator | No | Yes |
| Folders & organization | No | Yes |
| Prompt history | No | Yes |
| New prompts first | No | Yes |

**Price display:**
- Pro: $19/month or $99/year (save 56%)
- 7-day free trial included

### Image/Animation spec

Side-by-side comparison. Pro features have subtle glow. Clean, tool-focused design.

### CTA

**Primary button:** Try Pro free for 7 days
**Secondary button:** Continue with Free
**Tertiary:** Restore purchase (small text link)
**Skip option:** Yes (Continue with Free acts as skip)

---

## Screen 4: Browse

**Screen name:** start_browsing
**Progress:** 4/4

### Copy

**Headline:** You're in

**Body:** Your personalized prompt feed is ready. Tap any prompt to copy it.

**Pro user text (if trial started):**
"Your 7-day Pro trial is active. Try the Prompt Improver in the bottom menu."

**Free user text:**
"You have full access to 500+ prompts. Upgrade anytime for AI features."

### Quick actions

- Search prompts
- Browse by category
- View favorites (empty state)
- Pro feature preview (grayed if free)

### Image/Animation spec

Prompt cards showing preview of feed. Categories visible. Search bar prominent.

### CTA

**Button text:** Start browsing
**Skip option:** No

---

## A/B Test Variations

### Screen 1: Use Case (Variant B - Problem framing)

**Headline:** What's your biggest AI struggle?

**Body:** Pick what frustrates you most. We'll fix it.

**Options:**
- My prompts don't get good results
- I can't think of what to ask
- I waste time writing prompts from scratch
- I forget prompts that worked
- I need prompts for specific tasks

**Hypothesis:** Problem-focused selection may create stronger intent to use Pro features.

---

### Screen 3: Trial (Variant B - Value demonstration)

**Headline:** Stop writing bad prompts

**Body:**
You type: "Write me an email"
Pro turns it into: "Write a professional email to [recipient] requesting [action]. Tone should be [formal/casual]. Include a clear subject line and call-to-action. Keep it under 150 words."

That's the Prompt Improver.

**Price display:**
- 7 days free, then $99/year

**Hypothesis:** Showing the transformation may increase Pro trial starts.

---

### Screen 3: Trial (Variant C - Social proof)

**Headline:** Join 50,000 prompt power users

**Body:**
- 500+ curated prompts
- Used by marketers, developers, and creators
- Updated weekly with new prompts

**Testimonial:**
"Saved me hours. I copy prompts straight into ChatGPT." - Product Manager, Spotify

**Hypothesis:** Social proof may work better for freemium conversion than feature lists.

---

## Technical Notes

### Permissions requested
- None required for core functionality
- Push notifications (optional, for new prompt alerts)

### Data stored locally
- selected_use_cases: array[string]
- selected_interests: array[string]
- favorites: array[string] (prompt IDs)
- is_pro: boolean
- trial_start_date: timestamp (if applicable)
- onboarding_completed: boolean

### Analytics events
- onboarding_started
- use_cases_selected (with array)
- interests_selected (with array)
- paywall_shown
- trial_started
- free_selected
- onboarding_completed
- first_prompt_copied
