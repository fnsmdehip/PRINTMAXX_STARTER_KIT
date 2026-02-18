# Landing Page Generation Prompt

**Source:** Converted from `landind page prtopmt.rtf`
**Last Updated:** 2026-01-21
**Use Case:** Generate complete landing page designs for apps and products

---

## Base Prompt Template

Design a complete landing page for **[PRODUCT_NAME]**. [PRODUCT_NAME] is **[ONE_SENTENCE_DESCRIPTION]**.

### Design Requirements

**Style:**
- Clean, modern, minimal
- Generous white space
- Layout inspired by high-end design tools (Linear, Vercel, Stripe)

**Color Palette:**
- Background sections: soft, light colors
  - Pastel yellow-green: #F1FFD4
  - Light lavender: #E8D9F0
  - Neutral off-white: #FAFAFA
  - Rich black (contrast): #0A0A0A

**Typography:**
- Large, bold sans-serif headlines: 40-48px
- Clean body text: 16-18px
- Strong hierarchy through font weight and spacing

**Accent Colors (use sparingly):**
- Electric blue: #00AEEF
- Soft pink: #FFB3C1
- Lime green: #A5E887
- Bright orange: #FFA500
- Deep plum: #4B0055

**Graphics:**
- SVG only (no photos or raster images)
- Abstract vector shapes: circles, squiggles, geometric blocks
- UI mockups as SVG representations

---

## Section Structure

### 1. Hero Section
- **Headline:** "[VALUE_PROP_HEADLINE]" (max 10 words)
- **Subheading:** "[WHO_ITS_FOR] + [WHAT_THEY_GET]"
- **CTA:** "[ACTION_VERB] + [BENEFIT]" (e.g., "Try it free", "Start building")
- **Visual:** Split-view SVG showing [BEFORE/AFTER or PROBLEM/SOLUTION]

### 2. Feature Section
- 3-4 feature cards with icons
- Short descriptions (one sentence each)
- Examples:
  - "[FEATURE_1]" - [BENEFIT]
  - "[FEATURE_2]" - [BENEFIT]
  - "[FEATURE_3]" - [BENEFIT]

### 3. How It Works / Walkthrough
- Left-aligned explanatory text
- Right-aligned SVG mockups
- Step-by-step progression
- Tab interface if applicable (Mode 1, Mode 2, Mode 3)

### 4. Use Cases / Social Proof
- Team/persona cards showing who uses it
- Quotes or testimonials (use "Verified User" not fake names)
- SVGs of workflows or shared workspaces

### 5. Final CTA Section
- Strong headline: "[OUTCOME_STATEMENT]"
- Colorful abstract background
- Button: "[ACTION]"

### 6. Footer
- Background: #0A0A0A (black)
- Organized link columns:
  - Product
  - Use Cases
  - Docs
  - Company
  - Community
  - Legal

---

## Voice Guidelines

- Empowering but not hype
- Transparent about what it does
- Developer/builder-first language
- Accessible to non-technical users
- No promotional adjectives (see copy-style.md)
- No em dashes

---

## Example: Adapting for PrayerLock

```markdown
Design a complete landing page for PrayerLock. PrayerLock is a screen time blocker app that requires users to pray before unlocking their phone.

Hero:
- Headline: "Pray first. Scroll second."
- Subhead: "PrayerLock helps Christians start their day with intention, not distraction."
- CTA: "Download free"
- Visual: SVG of phone showing lock screen with prayer prompt

Features:
- "Morning Prayer Lock" - Set a prayer requirement before your first unlock
- "Scripture Prompts" - Random verses to center your day
- "Streak Tracking" - Build a habit of prayer over scrolling

Social Proof:
- "Verified User" testimonials
- Church community logos (placeholder SVGs)

Final CTA:
- "Start your mornings with purpose"
- "Get PrayerLock"
```

---

## Remotion Video Adaptation

This prompt can also be adapted for Remotion video intros:

```markdown
Create a 10-second Remotion intro video for [PRODUCT_NAME].

Sequence:
1. Logo animation (0-2s): [LOGO] fades in with scale spring
2. Tagline (2-4s): "[TAGLINE]" types out with cursor
3. Feature flash (4-7s): 3 feature icons animate in sequence
4. CTA (7-10s): "[DOWNLOAD_CTA]" with button pulse animation

Style: Match landing page palette (#F1FFD4, #0A0A0A, accent colors)
```

---

## Related Files

- `.claude/rules/copy-style.md` - Writing guidelines
- `MONEY_METHODS/APP_FACTORY/landing_pages/` - Existing landing page examples
- `ralph_tasks/06_landing_components.md` - Component generation task
