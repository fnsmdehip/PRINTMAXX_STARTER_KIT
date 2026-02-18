# Thumbnail Design Guide

Platform-specific thumbnail specs, design principles, tools, and A/B testing methodology.

---

## Platform Specifications

### YouTube

**Dimensions:** 1280 x 720 px (16:9)
**File Size:** Under 2MB
**Formats:** JPG, PNG, GIF, BMP

**Display Sizes:**
- Search results: ~360 x 202 px
- Suggested videos: ~168 x 94 px
- Home page: ~240 x 135 px
- Mobile: ~160 x 90 px

**Best Practices:**
- Design for mobile first (smallest display)
- Text must be readable at 160px width
- Face/emotion highly effective
- Contrast with YouTube's white/dark UI
- Avoid text in bottom right (timestamp)

---

### TikTok

**Dimensions:** 1080 x 1920 px (9:16)
**Format:** Auto-generated from video or custom upload

**Display Notes:**
- Thumbnail is first frame unless custom selected
- Bottom 15% covered by UI elements
- Username and caption overlay
- Select from video or upload custom

**Best Practices:**
- Engaging first frame essential
- Clear subject/face
- Avoid important info at bottom
- Movement/action implies video
- Text overlay optional but common

---

### Instagram Reels

**Dimensions:** 1080 x 1920 px (9:16)
**Cover Image:** Can select from video or upload

**Display Notes:**
- Profile grid shows center square
- Bottom area covered by engagement icons
- Cover affects grid aesthetics

**Best Practices:**
- Design for square crop on grid
- Keep focus in center
- Consistent style across content
- Less text than YouTube thumbnails

---

### Instagram Feed

**Square:** 1080 x 1080 px
**Portrait:** 1080 x 1350 px (4:5)
**Landscape:** 1080 x 608 px (1.91:1)

**Best Practices:**
- Portrait (4:5) takes most screen space
- Carousel first image most critical
- Consistent visual style
- Grid planning for profile aesthetics

---

## Design Principles

### The 3-Second Rule

Viewer decides in 3 seconds. Your thumbnail needs:
1. One clear subject/focus point
2. Emotion or intrigue
3. Promise of value

### Face and Emotion

Faces with clear emotion dramatically increase CTR:
- Surprise (raised eyebrows, open mouth)
- Excitement (big smile, wide eyes)
- Shock/disbelief
- Intense focus

**What works:**
- Eyes looking at camera
- Exaggerated expressions
- Clear, well-lit face
- Subject fills 40-60% of frame

### Text on Thumbnails

**YouTube (2-5 words max):**
- Large, bold, sans-serif fonts
- High contrast colors
- Drop shadow or stroke for readability
- Complement title, don't repeat it

**TikTok/Reels (0-3 words):**
- Less common/necessary
- Use for series or category labels
- Keep minimal

### Color and Contrast

**High-performing colors:**
- Yellow (attention)
- Red (urgency)
- Blue (trust)
- Green (money/growth)
- White text on dark, dark text on light

**Contrast rules:**
- Background vs. subject
- Text vs. background
- Thumbnail vs. platform UI

### Composition

**Rule of thirds:**
- Face/subject at intersection points
- Text on opposite third from subject

**Visual hierarchy:**
- Largest: Main subject/face
- Medium: Key text
- Smallest: Supporting elements

---

## Thumbnail Styles by Content Type

### Tutorial/How-To

**Elements:**
- Face with engaged expression
- Text: "How I [result]" or "[Number] [Thing]"
- Optional: Screenshot/tool preview
- Arrow pointing to result

**Example:** Face + "5 Tools" + Screenshot background

### Before/After

**Elements:**
- Split screen (left: before, right: after)
- Clear visual difference
- Arrow or separator
- Minimal text

**Example:** Sad face (left) arrow Happy face + money (right)

### Reaction/Commentary

**Elements:**
- Big emotional face
- Subject of reaction visible
- Expression matches content tone
- Minimal text

### List/Ranking

**Elements:**
- Number prominently displayed
- Subject images arranged
- Face expressing opinion
- Text: "Best [X]" or "Top [N]"

### News/Update

**Elements:**
- Relevant imagery
- Date or "NEW" badge
- News-style text treatment
- Urgency indicators

---

## Design Tools

### Free

| Tool | Best For | Notes |
|------|----------|-------|
| Canva | General thumbnails | Templates, easy |
| Photopea | Advanced editing | Photoshop alternative |
| GIMP | Full editing | Steeper learning curve |
| Remove.bg | Background removal | Free for low-res |

### Paid

| Tool | Best For | Price |
|------|----------|-------|
| Photoshop | Professional editing | $21/mo |
| Canva Pro | Templates + assets | $13/mo |
| Figma | Design systems | Free-$15/mo |
| Thumbnail.AI | AI generation | $10/mo |

### Quick Workflow

1. **Capture:** Take photo or screenshot
2. **Remove BG:** Remove.bg or Photoshop
3. **Compose:** Canva or Photoshop
4. **Add text:** Bold, readable font
5. **Export:** Check dimensions, file size

---

## Template Library

### YouTube Template 1: Face + Text

```
Layout:
[Face 60%] [Text 40%]
- Subject on left, looking right
- 2-4 word text on right
- Gradient or solid background
- Drop shadow on text
```

### YouTube Template 2: Before/After

```
Layout:
[Before 50%] | [After 50%]
- Split with line or arrow
- Same subject, different state
- Minimal text ("Before" | "After")
- Consistent lighting style
```

### YouTube Template 3: List/Number

```
Layout:
[Number 30%] [Subject 50%] [Face 20%]
- Large number in corner
- Product/topic images center
- Reaction face small
- Text: "Best [X]"
```

### TikTok Template: Hook Frame

```
Layout:
[Full-frame face or action shot]
- Engaging expression
- Clear subject
- Optional: 2-3 word overlay
- Safe zone: avoid bottom 20%
```

---

## A/B Testing Methodology

### What to Test

| Element | Variations |
|---------|------------|
| Face expression | Smile vs. shock vs. serious |
| Text | With vs. without, different words |
| Colors | Background, text colors |
| Layout | Face left vs. right |
| Zoom | Close-up vs. wide |

### Testing Process

**YouTube (TubeBuddy or native):**
1. Create 2-3 thumbnail variants
2. Use A/B test feature
3. Run for minimum 7 days or 10k impressions
4. Compare CTR
5. Roll out winner

**TikTok/Instagram:**
1. Post similar content with different covers
2. Compare views at 24 and 48 hours
3. Note which performs better
4. Apply learnings to future content

### Metrics to Track

| Metric | Good | Great |
|--------|------|-------|
| YouTube CTR | 4-6% | 8%+ |
| TikTok view rate | 20%+ | 40%+ |
| IG Reel reach | 10x followers | 50x+ followers |

### Testing Schedule

- Week 1-2: Baseline (current style)
- Week 3-4: Test element A (face vs. no face)
- Week 5-6: Test element B (text style)
- Week 7-8: Test element C (colors)
- Ongoing: Apply learnings, test new ideas

---

## Common Mistakes

1. **Too much text** - Unreadable on mobile
2. **Low contrast** - Blends into background
3. **Clickbait mismatch** - Thumbnail doesn't match content
4. **Inconsistent style** - No brand recognition
5. **Ignoring platform** - YouTube style on TikTok
6. **No face** - Lower CTR in most niches
7. **Boring expression** - Neutral face doesn't grab attention
8. **Not testing** - Guessing instead of measuring

---

## Niche-Specific Tips

### Tech/Tutorial

- Screenshot with annotation
- Tool logo visible
- "How to" or result text
- Clean, minimal style

### Finance/Business

- Green/gold colors
- Money imagery
- Numbers/charts
- Professional expression

### Fitness

- Before/after physique
- Action shots
- High energy expression
- Bright, vibrant colors

### Lifestyle/Vlog

- Authentic expression
- Location/context visible
- Warmer color tones
- Less text, more visual

### Gaming

- Game footage/character
- Dramatic lighting
- Reaction face
- Bold, gaming-style text

---

## Quick Checklist

### Before Publishing

- [ ] Correct dimensions for platform
- [ ] File size under limit
- [ ] Text readable at smallest display
- [ ] Face/emotion visible (if using)
- [ ] High contrast throughout
- [ ] No important elements in danger zones
- [ ] Consistent with brand style
- [ ] Thumbnail matches content
- [ ] Would I click this?

---

Last updated: 2026-01-23
