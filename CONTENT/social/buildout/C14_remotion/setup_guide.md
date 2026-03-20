# C14 Remotion Video Production, Setup Guide

## What Remotion Is

React-based video framework. You write components. It renders them as MP4/WebM at exact framerates. No Premiere, no CapCut. Pure code.

**Why it matters:**
- Generate 50 videos from one script, different text/data per video
- 4K at 60fps is config, not a hardware question
- Reuse React component logic, if you have a chart, it animates
- Costs: ~$0.01 per video on a VPS vs $200/mo for Synthesia

---

## Install (5 minutes)

```bash
# Node 18+ required
node --version  # must be >= 18

# Create new Remotion project
npx create-video@latest printmaxx-videos
cd printmaxx-videos

# Choose: Blank (start from scratch) or Hello World template
# Install dependencies
npm install

# Start preview server
npm start
# Opens http://localhost:3000, live scrubbing preview
```

---

## Project Structure

```
printmaxx-videos/
├── src/
│   ├── Root.tsx              # Register all compositions here
│   ├── compositions/
│   │   ├── ShortClip.tsx     # YouTube Shorts / TikTok template
│   │   ├── Stats.tsx         # Revenue/stats reveal
│   │   ├── Listicle.tsx      # "5 ways to..." slide deck
│   │   ├── ColdEmail.tsx     # Animated cold email tutorial
│   │   └── Quote.tsx        # Quote card with logo
│   └── assets/
│       ├── fonts/
│       ├── music/
│       └── logos/
├── public/
├── remotion.config.ts
└── package.json
```

---

## remotion.config.ts (base config)

```typescript
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setCodec("h264");           // h264 = fastest, widest compat
Config.setCrf(18);                  // 0=lossless, 51=worst. 18 = YouTube-ready
Config.setConcurrency(4);           // CPU cores to use. Set to logical core count
Config.setChromiumOpenGlRenderer("angle");
```

---

## Root.tsx (Register Compositions)

```typescript
import { Composition } from "remotion";
import { ShortClip } from "./compositions/ShortClip";
import { Stats } from "./compositions/Stats";
import { Listicle } from "./compositions/Listicle";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* YouTube Shorts / TikTok, 9:16 */}
      <Composition
        id="ShortClip"
        component={ShortClip}
        durationInFrames={900}   // 30 seconds at 30fps
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          title: "I made $3,200 last month",
          steps: ["Cold email 50 people", "Close 2 clients", "Collect payment"],
          accent: "#FF5733",
        }}
      />
      {/* Stats reveal, 16:9 landscape */}
      <Composition
        id="Stats"
        component={Stats}
        durationInFrames={450}   // 15 seconds at 30fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          metric: "$3,200",
          label: "Revenue in 30 days",
          breakdown: [
            { label: "Cold email", value: "$1,800" },
            { label: "Affiliate", value: "$900" },
            { label: "Digital products", value: "$500" },
          ],
        }}
      />
      {/* Listicle slides */}
      <Composition
        id="Listicle"
        component={Listicle}
        durationInFrames={1500}  // 50 seconds at 30fps
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          title: "5 tools I used to make $3K last month",
          items: [
            { number: "01", text: "Hunter.io, found 200 leads in 2 hours" },
            { number: "02", text: "Instantly.ai, sent 500 emails for $30" },
            { number: "03", text: "Beehiiv, newsletter at $0 to 1K subs" },
            { number: "04", text: "Gumroad, sold 2 templates for $600" },
            { number: "05", text: "visualping.io, tracked 200 competitor pages" },
          ],
        }}
      />
    </>
  );
};
```

---

## Render Single Video (CLI)

```bash
# Render one composition to file
npx remotion render ShortClip out/short_v1.mp4

# Override props at render time
npx remotion render ShortClip out/short_v2.mp4 \
  --props='{"title":"I cold emailed 500 people","accent":"#6C63FF"}'

# Render GIF (for Twitter previews)
npx remotion render ShortClip out/preview.gif --frames=0-60

# Render still image (thumbnail)
npx remotion still ShortClip out/thumbnail.jpg --frame=45
```

---

## Key Remotion Hooks

```typescript
import {
  useCurrentFrame,       // current frame number (0 to durationInFrames)
  useVideoConfig,        // fps, width, height, durationInFrames
  interpolate,           // map frame range to value range
  spring,               // physics-based easing
  Sequence,             // time-offset children
  Audio,                // background music
  Video,                // embed video
  Img,                  // images with lazy loading
  AbsoluteFill,         // full-frame positioned div
} from "remotion";

// Example: fade in over first 30 frames
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp",
});

// Spring animation (bouncy)
const scale = spring({ frame, fps: 30, config: { stiffness: 120, damping: 10 } });
```

---

## Typography Setup

```bash
# Install Google Fonts loader
npm install @remotion/google-fonts

# In component:
import { loadFont } from "@remotion/google-fonts/Inter";
const { fontFamily } = loadFont();
// Then use fontFamily in your styles
```

---

## Dependencies to Install

```bash
npm install @remotion/cli @remotion/renderer
npm install @remotion/google-fonts
npm install @remotion/noise      # Perlin noise for organic animations
npm install @remotion/motion-blur # Motion blur post-processing
npm install @remotion/shapes     # SVG shape primitives

# For data-driven videos (charts)
npm install recharts             # Works perfectly inside Remotion
npm install d3                   # Full D3 support
```

---

## Font + Color System

```typescript
// src/tokens.ts
export const TOKENS = {
  fonts: {
    heading: "'Inter', sans-serif",
    mono: "'JetBrains Mono', monospace",
  },
  colors: {
    bg: "#0A0A0A",
    bgCard: "#141414",
    text: "#F5F5F5",
    textMuted: "#666666",
    accent: "#FF5733",    // override per video
    accentAlt: "#6C63FF",
  },
  spacing: {
    sm: 16,
    md: 32,
    lg: 64,
    xl: 96,
  },
};
```

---

## Before First Render Checklist

- [ ] Node 18+ confirmed: `node --version`
- [ ] Project created: `npx create-video@latest`
- [ ] Preview running: `npm start` → localhost:3000
- [ ] Root.tsx has at least one Composition registered
- [ ] Test render succeeds: `npx remotion render ShortClip out/test.mp4`
- [ ] Output file plays in QuickTime / VLC
- [ ] File size reasonable (< 50MB per minute of video)

---

## Common Errors + Fixes

| Error | Fix |
|-------|-----|
| `ENOENT: no such file or directory, open 'out/...'` | Create `out/` directory first: `mkdir out` |
| Blank white video | Check `AbsoluteFill` wraps all content |
| Font not rendering | Move `loadFont()` call outside component, at module level |
| Slow render | Lower `setConcurrency` to 2, set `setVideoImageFormat('jpeg')` |
| Audio sync off | Use `<Audio src={...} startFrom={0} endAt={frames} />` explicitly |
| `interpolate` extrapolation warning | Add `extrapolateLeft: 'clamp', extrapolateRight: 'clamp'` |

---

## Platform Export Settings

| Platform | Width | Height | FPS | CRF | Duration |
|----------|-------|--------|-----|-----|----------|
| TikTok | 1080 | 1920 | 30 | 18 | 15-60s |
| YouTube Shorts | 1080 | 1920 | 30 | 16 | 15-60s |
| Instagram Reels | 1080 | 1920 | 30 | 18 | 15-90s |
| YouTube (16:9) | 1920 | 1080 | 30 | 16 | any |
| Twitter/X | 1280 | 720 | 30 | 20 | < 2:20 |
| LinkedIn | 1920 | 1080 | 30 | 18 | 3-10 min |
