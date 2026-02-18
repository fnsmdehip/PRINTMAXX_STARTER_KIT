# PRINTMAXX Prompt Library

A comprehensive library of AI prompts for all PRINTMAXX operations. Each prompt includes system prompts, user prompt templates, example outputs, and variations.

All prompts follow the PRINTMAXX copy-style rules from `.claude/rules/copy-style.md`.

---

## Quick access

### Content generation
Create content across platforms and formats.

| Prompt | Purpose | Use when... |
|--------|---------|-------------|
| [social_post_generator.md](content_generation/social_post_generator.md) | Generate social posts | Creating individual posts for any platform |
| [thread_writer.md](content_generation/thread_writer.md) | Write viral threads | Creating multi-post threads on Twitter/X |
| [video_script_writer.md](content_generation/video_script_writer.md) | Short-form video scripts | Creating TikTok, Reels, or Shorts content |
| [blog_post_writer.md](content_generation/blog_post_writer.md) | SEO blog posts | Writing search-optimized articles |
| [email_writer.md](content_generation/email_writer.md) | Email sequences | Writing newsletters, nurture, or sales emails |
| [ad_copy_writer.md](content_generation/ad_copy_writer.md) | Ad copy variations | Creating ads for paid campaigns |
| [headline_generator.md](content_generation/headline_generator.md) | A/B test headlines | Generating headline variations to test |

### Research
Gather intelligence and insights.

| Prompt | Purpose | Use when... |
|--------|---------|-------------|
| [competitor_analyzer.md](research/competitor_analyzer.md) | Analyze competitors | Understanding competitive landscape |
| [market_research.md](research/market_research.md) | Research opportunities | Validating niches or business ideas |
| [keyword_research.md](research/keyword_research.md) | Find SEO keywords | Building keyword strategy |
| [trend_scanner.md](research/trend_scanner.md) | Find trending topics | Identifying content opportunities |
| [pain_point_finder.md](research/pain_point_finder.md) | Extract pain points | Mining reviews and forums for problems |

### Product
Build and price products.

| Prompt | Purpose | Use when... |
|--------|---------|-------------|
| [prd_generator.md](product/prd_generator.md) | Generate PRDs | Specifying features or products |
| [feature_prioritizer.md](product/feature_prioritizer.md) | Prioritize features | Deciding what to build next |
| [pricing_analyzer.md](product/pricing_analyzer.md) | Analyze pricing | Setting or adjusting prices |
| [landing_page_writer.md](product/landing_page_writer.md) | Write landing pages | Creating conversion-focused pages |
| [sales_page_writer.md](product/sales_page_writer.md) | Write sales pages | Creating long-form sales copy |

### Operations
Run the business day-to-day.

| Prompt | Purpose | Use when... |
|--------|---------|-------------|
| [daily_planner.md](operations/daily_planner.md) | Plan daily tasks | Starting each work day |
| [weekly_reviewer.md](operations/weekly_reviewer.md) | Review and plan | Weekly retrospective and planning |
| [decision_maker.md](operations/decision_maker.md) | Make decisions | Facing business decisions |
| [problem_solver.md](operations/problem_solver.md) | Troubleshoot issues | Diagnosing and fixing problems |
| [brainstormer.md](operations/brainstormer.md) | Generate ideas | Need ideas for content, products, growth |

### Outreach
Connect with people.

| Prompt | Purpose | Use when... |
|--------|---------|-------------|
| [cold_email_writer.md](outreach/cold_email_writer.md) | Write cold emails | Reaching out to new contacts |
| [dm_script_writer.md](outreach/dm_script_writer.md) | Write DM scripts | Social media outreach |
| [follow_up_writer.md](outreach/follow_up_writer.md) | Write follow-ups | Following up on outreach |
| [proposal_writer.md](outreach/proposal_writer.md) | Write proposals | Pitching clients or partners |

---

## How to use these prompts

### Basic usage

1. Open the prompt file for your task
2. Copy the system prompt into your AI chat
3. Fill in the user prompt template with your specifics
4. Review and iterate on the output

### Customization

Each prompt includes:
- **System prompt:** Sets the AI's role and rules
- **User prompt template:** Fill-in-the-blank structure with [PLACEHOLDERS]
- **Example output:** Shows what good output looks like
- **Variations:** Alternative approaches for different situations
- **Quality checklist:** Verify output meets standards

### Model routing

Follow PRINTMAXX model routing policy:
- **Haiku:** Bulk generation, simple variations
- **Sonnet:** Quality content, standard operations
- **Opus:** Critical decisions, complex analysis

---

## Prompt structure

All prompts follow this format:

```markdown
# [Prompt name]

[One-line description]

---

## System prompt

[The role and rules for the AI]

---

## User prompt template

[Template with [PLACEHOLDERS] to fill in]

---

## Example output

[Complete example showing expected quality]

---

## Variations

[Alternative approaches for different situations]

---

## Quality checklist

[Checkboxes to verify output quality]
```

---

## Copy style rules (quick reference)

All content prompts enforce these rules:

**Never use:**
- Em dashes
- AI vocabulary (leverage, utilize, delve, comprehensive, robust)
- "It's not just X, it's Y" constructions
- Vague attributions (experts say, studies show)
- Promotional adjectives (revolutionary, game-changing)

**Always:**
- Start with the conclusion
- Use specific numbers
- Write like texting a smart friend
- Sentence case for headings
- One hedge per sentence max

Full reference: `.claude/rules/copy-style.md`

---

## Adding new prompts

When creating new prompts:

1. Use the standard structure (system, template, example, variations, checklist)
2. Include copy-style rules if the prompt generates content
3. Provide realistic example output
4. Add variations for common use cases
5. Update this README with the new prompt

---

## Feedback and improvements

If a prompt isn't working well:
1. Note what went wrong
2. Check if copy-style rules were followed
3. Try a variation or different approach
4. Consider if the prompt needs updating

Document improvements in the prompt file for future use.
