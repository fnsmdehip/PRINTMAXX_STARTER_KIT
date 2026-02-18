# Remotion Video Generation Prompt

**Source:** JonnyBurger gist + Claude Code patterns
**Last Updated:** 2026-01-21
**Use Case:** Generate branded intro videos, product demos, social clips

---

## Key Insight

Remotion video generation with Claude Code is **conversational**, not rigid prompts. You describe what you want visually, and iterate through micro-adjustments.

---

## Basic Workflow

### 1. Describe the Visual
Start with a simple description of what you want:

```
Create a 10-second intro video for PrayerLock.

Visual:
- Clean white background fading to soft lavender (#E8D9F0)
- Logo centered, scales in with spring animation
- Tagline "Pray first. Scroll second." types out below
- CTA "Download free" pulses at the end
```

### 2. Iterate Through Micro-Adjustments

After seeing the result, request changes naturally:
- "make the logo bigger"
- "slow down the typewriter effect"
- "add a subtle glow behind the logo"
- "change the background to #F1FFD4"
- "make the CTA button pulse more slowly"

### 3. Technical Patterns Claude Code Understands

**Animation Hooks:**
- `useCurrentFrame()` - Get current frame
- `useVideoConfig()` - Get video dimensions/fps
- `interpolate()` - Animate values between keyframes
- `spring()` - Physics-based spring animation

**Timing:**
- `Sequence` - Time-based sequencing
- `Series` - Sequential playback
- `AbsoluteFill` - Full-screen positioning

**Common Animations:**
- Scale spring: `scale: spring({ frame, fps, config: { damping: 15, stiffness: 200 } })`
- Fade: `opacity: interpolate(frame, [0, 30], [0, 1])`
- Typewriter: Character-by-character reveal based on frame

---

## Brand Video Templates

### PRINTMAXX Intro (10 seconds)

```
Create a 10-second Remotion intro for PRINTMAXX.

Sequence:
0-2s: Black screen fades to off-white (#FAFAFA)
2-4s: "PRINTMAXX" text scales in from 0 with spring bounce
4-6s: Tagline "Ship fast. Measure. Scale." types out with cursor
6-8s: Three small icons animate in (📱 💰 🚀) with stagger
8-10s: "printmaxx.io" fades in at bottom

Style:
- Sans-serif bold font for logo
- Electric blue (#00AEEF) accent for cursor
- Clean, minimal, Vercel-style aesthetic
```

### App Launch Video (15 seconds)

```
Create a 15-second app launch video for [APP_NAME].

Sequence:
0-3s: Problem statement text fades in ("Tired of [PROBLEM]?")
3-6s: Text fades out, phone mockup slides in from right
6-9s: App interface animates on phone screen
9-12s: Key feature callouts appear with arrows
12-15s: App name + download CTA + App Store badge

Style:
- Match app color scheme
- Phone mockup as central element
- Feature callouts with soft shadows
```

### Social Clip (6 seconds)

```
Create a 6-second TikTok/Reels clip for [APP_NAME].

Sequence:
0-1s: Hook text appears big ("This changed my mornings")
1-3s: Quick app demo (3 screen transitions)
3-5s: Result ("Now I [BENEFIT] every day")
5-6s: App name + "Link in bio"

Style:
- Vertical format (1080x1920)
- Fast cuts, high energy
- Bold text overlays
- Bright accent colors
```

---

## Component Patterns

### Typewriter Effect
```tsx
const TypewriterText = ({ text, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const charsToShow = Math.floor((frame - startFrame) / 3);
  const visibleText = text.slice(0, charsToShow);
  const showCursor = (frame - startFrame) % 20 < 10;

  return (
    <span>
      {visibleText}
      {showCursor && <span style={{ color: '#00AEEF' }}>|</span>}
    </span>
  );
};
```

### Scale Spring
```tsx
const ScaleIn = ({ children, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame: frame - delay,
    fps,
    config: { damping: 15, stiffness: 200 }
  });

  return (
    <div style={{ transform: `scale(${scale})` }}>
      {children}
    </div>
  );
};
```

### Staggered List
```tsx
const StaggeredList = ({ items, staggerDelay = 10 }) => {
  const frame = useCurrentFrame();

  return items.map((item, i) => {
    const itemFrame = frame - (i * staggerDelay);
    const opacity = interpolate(itemFrame, [0, 20], [0, 1], {
      extrapolateRight: 'clamp'
    });

    return (
      <div key={i} style={{ opacity }}>
        {item}
      </div>
    );
  });
};
```

---

## Color Palette Reference

From landing page prompt:

| Color | Hex | Use |
|-------|-----|-----|
| Off-white | #FAFAFA | Background |
| Pastel green | #F1FFD4 | Accent background |
| Light lavender | #E8D9F0 | Accent background |
| Rich black | #0A0A0A | Text, dark sections |
| Electric blue | #00AEEF | Primary accent |
| Soft pink | #FFB3C1 | Secondary accent |
| Lime green | #A5E887 | Success, positive |
| Bright orange | #FFA500 | Attention |

---

## Project Setup

```bash
# Create new Remotion project
npx create-video@latest my-video

# Or add to existing project
npm install remotion @remotion/cli @remotion/bundler
```

**File Structure:**
```
src/
├── Root.tsx          # Main composition
├── Video.tsx         # Video component
├── components/
│   ├── Logo.tsx
│   ├── Typewriter.tsx
│   └── ScaleIn.tsx
└── lib/
    └── animations.ts
```

---

## Tips for Best Results

1. **Start simple** - Get basic structure, then add polish
2. **Use springs** - More natural than linear interpolation
3. **Stagger elements** - Don't animate everything at once
4. **Match brand colors** - Reference app/site palette
5. **Test at multiple speeds** - Ensure timing feels right
6. **Export at 60fps** - Smoother animations

---

## Related Files

- `OPS/prompts/templates/landing_page_prompt.md` - Design guidelines
- `.claude/rules/copy-style.md` - Text content rules
- `MONEY_METHODS/APP_FACTORY/products/` - App details for videos
