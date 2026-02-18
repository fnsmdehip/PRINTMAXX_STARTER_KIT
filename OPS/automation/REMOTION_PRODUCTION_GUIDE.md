# Remotion Video Production Guide

**Purpose:** Comprehensive guide for automated video creation with Remotion
**Last Updated:** January 2026
**Project Location:** `LANDING/printmaxx-site/src/remotion/`

---

## Table of Contents

1. [Setup and Installation](#setup-and-installation)
2. [Project Structure](#project-structure)
3. [Video Types and Templates](#video-types-and-templates)
4. [Animation Recipes](#animation-recipes)
5. [Audio Integration](#audio-integration)
6. [Batch Rendering](#batch-rendering)
7. [Workflow Integration](#workflow-integration)
8. [Best Practices](#best-practices)

---

## Setup and Installation

### Prerequisites

```bash
# Node.js 18+ required
node --version  # Should be 18.x or higher

# Navigate to project
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LANDING/printmaxx-site
```

### Initial Setup

```bash
# Install dependencies
npm install remotion @remotion/cli @remotion/player

# Install required Remotion packages
npm install @remotion/bundler @remotion/renderer

# Optional: Lambda rendering (for cloud batch processing)
npm install @remotion/lambda
```

### Project Initialization

If starting fresh:

```bash
# Create new Remotion project
npx create-video@latest

# Or add to existing Next.js project
npm install remotion @remotion/cli
```

### Configuration Files

**remotion.config.ts:**

```typescript
import { Config } from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
Config.setConcurrency(4); // Adjust based on CPU cores
Config.setChromiumOpenGlRenderer('angle');
```

**package.json scripts:**

```json
{
  "scripts": {
    "remotion:preview": "npx remotion preview src/remotion/index.tsx",
    "remotion:render": "npx remotion render src/remotion/index.tsx",
    "remotion:studio": "npx remotion studio src/remotion/index.tsx"
  }
}
```

---

## Project Structure

### Current PRINTMAXX Structure

```
LANDING/printmaxx-site/src/remotion/
├── Root.tsx                 # Main composition registry
├── index.tsx                # Entry point
├── entry.tsx                # Remotion bundle entry
├── AppPromoVideo.tsx        # Shared promo components
├── HookVideo.tsx            # Hook video template
├── components/
│   └── AnimatedText.tsx     # Reusable text animations
├── compositions/
│   ├── PrayerLockPromoV2.tsx
│   ├── StepUnlockPromoV2.tsx
│   ├── BioMaxxPromoV2.tsx
│   ├── GlowMaxxPromoV2.tsx
│   ├── ... (20+ compositions)
│   └── index.ts             # Composition exports
└── public/
    ├── icons/               # App icons (1024x1024 PNG)
    └── music/               # Audio tracks (MP3)
```

### Composition Registration (Root.tsx)

```typescript
import { Composition } from 'remotion';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VideoName"
        component={VideoComponent}
        durationInFrames={360}  // 12 seconds at 30fps
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
```

### Asset Organization

```
public/
├── icons/
│   ├── prayerlock-icon-1024.png
│   ├── walktounlock-icon-1024.png
│   ├── studylock-icon-1024.png
│   └── biomaxx-icon-1024.png
├── music/
│   ├── meditation.mp3       # Faith apps (60-80 BPM)
│   ├── phonk-energy.mp3     # Fitness apps (140-150 BPM)
│   ├── lofi-study.mp3       # Productivity apps (70-90 BPM)
│   └── empowering-pop.mp3   # Women's wellness
└── images/
    └── app-screenshots/
```

---

## Video Types and Templates

### 1. App Announcement (15-30 seconds)

**Best for:** App launches, major feature releases
**Structure:**

| Frames | Duration | Scene | Content |
|--------|----------|-------|---------|
| 0-90 | 3s | HOOK | Bold claim + visual impact |
| 90-270 | 6s | PROBLEM | Relatable struggle |
| 270-540 | 9s | SOLUTION | App reveal + features |
| 540-750 | 7s | PROOF | Stats or social proof |
| 750-900 | 5s | CTA | Download prompt |

### 2. App Promo (8-12 seconds)

**Best for:** TikTok, Reels, app store previews
**Structure:**

| Frames | Duration | Scene |
|--------|----------|-------|
| 0-100 | 3.3s | Logo + tagline entrance |
| 100-240 | 4.7s | Feature showcase |
| 240-360 | 4s | CTA + end card |

### 3. Hook Video (3-6 seconds)

**Best for:** Scroll stoppers, attention grabbers
**Structure:**

| Frames | Duration | Content |
|--------|----------|---------|
| 0-45 | 1.5s | Line 1 entrance |
| 45-95 | 1.67s | Line 2 entrance |
| 95-150 | 1.83s | Line 3 + hold |

### 4. Feature Highlight (10-15 seconds)

**Best for:** Single feature demos
**Structure:**

| Frames | Duration | Scene |
|--------|----------|-------|
| 0-45 | 1.5s | Feature in action |
| 45-270 | 7.5s | Demo walkthrough |
| 270-390 | 4s | Benefit statement |
| 390-450 | 2s | CTA |

### 5. Testimonial (20-30 seconds)

**Best for:** Social proof, case studies
**Structure:**

| Frames | Duration | Scene |
|--------|----------|-------|
| 0-120 | 4s | BEFORE state |
| 120-180 | 2s | Discovery transition |
| 180-600 | 14s | AFTER + quote |
| 600-780 | 6s | Proof/stats |
| 780-900 | 4s | CTA |

### 6. Tutorial (30-60 seconds)

**Best for:** How-to content, onboarding
**Structure:**

| Frames | Duration | Scene |
|--------|----------|-------|
| 0-90 | 3s | Result preview |
| 90-180 | 3s | Introduction |
| 180-1440 | 42s | 4-6 numbered steps |
| 1440-1620 | 6s | Final result |
| 1620-1800 | 6s | CTA |

---

## Animation Recipes

### Spring Animation Configs

```typescript
// Bouncy entrance (fitness, high-energy)
const bouncySpring = { damping: 8, stiffness: 200 };

// Smooth slide (professional)
const smoothSpring = { damping: 20, stiffness: 100 };

// Snappy pop (attention-grabbing)
const snappySpring = { damping: 12, stiffness: 300 };

// Gentle float (faith, wellness)
const gentleSpring = { damping: 30, stiffness: 50 };

// Peaceful (prayer apps)
const faithSpring = { damping: 25, stiffness: 80 };

// Energetic (fitness apps)
const fitnessSpring = { damping: 10, stiffness: 250, mass: 0.8 };

// Academic (study apps)
const studySpring = { damping: 15, stiffness: 180 };
```

### Text Animations

**Kinetic Text Reveal:**

```typescript
const KineticText: React.FC<{ text: string; delay?: number }> = ({
  text,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: 'flex', overflow: 'hidden' }}>
      {text.split('').map((char, i) => {
        const charSpring = spring({
          frame: frame - delay - i * 2,
          fps,
          config: { damping: 12, stiffness: 200 },
        });

        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              transform: `translateY(${interpolate(charSpring, [0, 1], [100, 0])}%)`,
              opacity: charSpring,
            }}
          >
            {char === ' ' ? '\u00A0' : char}
          </span>
        );
      })}
    </div>
  );
};
```

**Staggered Feature Cards:**

```typescript
const FeatureCards: React.FC<{ features: string[]; stagger?: number }> = ({
  features,
  stagger = 15,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <>
      {features.map((feature, index) => {
        const delay = index * stagger;
        const featureSpring = spring({
          frame: frame - delay,
          fps,
          config: { damping: 20, stiffness: 120 },
        });
        const x = interpolate(featureSpring, [0, 1], [-50, 0]);
        const opacity = interpolate(frame - delay, [0, 20], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

        return (
          <div
            key={feature}
            style={{
              transform: `translateX(${x}px)`,
              opacity,
              marginBottom: 16,
            }}
          >
            {feature}
          </div>
        );
      })}
    </>
  );
};
```

### Background Effects

**Animated Gradient:**

```typescript
const AnimatedBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const rotation = interpolate(frame, [0, 300], [0, 360]);

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        background: `
          radial-gradient(circle at 30% 20%, #FF6B6B40 0%, transparent 50%),
          radial-gradient(circle at 70% 80%, #4ECDC440 0%, transparent 50%),
          linear-gradient(135deg, #0F0F0F 0%, #1A1A2E 100%)
        `,
      }}
    >
      <div
        style={{
          position: 'absolute',
          width: '200%',
          height: '200%',
          top: '-50%',
          left: '-50%',
          background: 'conic-gradient(from 0deg, #FF6B6B20, #4ECDC420, #FF6B6B20)',
          transform: `rotate(${rotation}deg)`,
          filter: 'blur(100px)',
        }}
      />
    </div>
  );
};
```

**Floating Particles:**

```typescript
const ParticleField: React.FC<{ count?: number; color?: string }> = ({
  count = 15,
  color = '#fff',
}) => {
  const frame = useCurrentFrame();

  const particles = useMemo(
    () =>
      Array.from({ length: count }, (_, i) => ({
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 4,
        speed: 0.5 + Math.random() * 1,
        opacity: 0.1 + Math.random() * 0.3,
      })),
    [count]
  );

  return (
    <>
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: `${p.x}%`,
            top: `${((p.y + frame * p.speed * 0.1) % 120) - 10}%`,
            width: p.size,
            height: p.size,
            borderRadius: '50%',
            backgroundColor: color,
            opacity: p.opacity,
            filter: 'blur(1px)',
          }}
        />
      ))}
    </>
  );
};
```

**Light Rays (Faith Apps):**

```typescript
const LightRays: React.FC<{ color?: string }> = ({ color = '#FFD700' }) => {
  const frame = useCurrentFrame();
  const rotation = frame * 0.02;

  return (
    <AbsoluteFill style={{ overflow: 'hidden', opacity: 0.15 }}>
      <div
        style={{
          position: 'absolute',
          top: '-50%',
          left: '50%',
          width: '200%',
          height: '200%',
          transform: `translateX(-50%) rotate(${rotation}rad)`,
          background: `conic-gradient(
            from 0deg,
            ${color}00 0deg,
            ${color}30 15deg,
            ${color}00 30deg,
            ${color}00 45deg,
            ${color}30 60deg,
            ${color}00 75deg,
            /* ... repeat pattern ... */
            ${color}00 360deg
          )`,
        }}
      />
    </AbsoluteFill>
  );
};
```

### Counter Animation

```typescript
const AnimatedCounter: React.FC<{
  from: number;
  to: number;
  duration: number;
  suffix?: string;
}> = ({ from, to, duration, suffix = '' }) => {
  const frame = useCurrentFrame();

  const value = interpolate(frame, [0, duration], [from, to], {
    extrapolateRight: 'clamp',
  });

  return (
    <span>
      {Math.floor(value).toLocaleString()}
      {suffix}
    </span>
  );
};
```

### Progress Bar

```typescript
const ProgressBar: React.FC<{
  progress: number;
  color: string;
  height?: number;
}> = ({ progress, color, height = 12 }) => {
  const frame = useCurrentFrame();
  const animated = interpolate(frame, [0, 60], [0, progress], {
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        width: '100%',
        height,
        backgroundColor: `${color}30`,
        borderRadius: height / 2,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          width: `${animated}%`,
          height: '100%',
          backgroundColor: color,
          borderRadius: height / 2,
        }}
      />
    </div>
  );
};
```

### CTA Button with Pulse

```typescript
const CTAButton: React.FC<{ text: string; color: string }> = ({
  text,
  color,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const buttonSpring = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 180 },
  });
  const buttonScale = interpolate(buttonSpring, [0, 1], [0.6, 1]);
  const pulse = Math.sin(frame * 0.12) * 0.03 + 1;

  return (
    <div
      style={{
        transform: `scale(${buttonScale * pulse})`,
        backgroundColor: color,
        padding: '22px 56px',
        borderRadius: 18,
        fontSize: 32,
        fontWeight: 700,
        color: '#000',
        boxShadow: `0 0 40px ${color}50`,
      }}
    >
      {text}
    </div>
  );
};
```

---

## Audio Integration

### Adding Audio to Compositions

```typescript
import { Audio, staticFile } from 'remotion';

// Basic audio
<Audio src={staticFile('music/track.mp3')} />

// With volume control
<Audio
  src={staticFile('music/track.mp3')}
  startFrom={0}
  volume={(f) => {
    const { durationInFrames } = useVideoConfig();
    // Fade in (first 30 frames)
    if (f < 30) return (f / 30) * 0.4;
    // Fade out (last 30 frames)
    if (f > durationInFrames - 30) {
      return ((durationInFrames - f) / 30) * 0.4;
    }
    // Normal volume
    return 0.4;
  }}
/>
```

### Volume Levels by Context

| Context | Volume Level | dB Equivalent |
|---------|--------------|---------------|
| Background music (under content) | 0.15-0.25 | -12 to -15 dB |
| Music hook (no voice) | 0.4-0.6 | -6 to -9 dB |
| SFX transitions | 0.4-0.6 | -6 to -9 dB |
| SFX subtle UI sounds | 0.15-0.25 | -15 to -18 dB |

### Music by Niche

| Niche | Style | BPM | Royalty-Free Source |
|-------|-------|-----|---------------------|
| Faith/Prayer | Worship ambient, soft piano | 60-80 | Pixabay, YouTube Audio Library |
| Fitness/Gym | Brazilian phonk, aggressive trap | 140-150 | FreeToUse, Tunetank |
| Women's Wellness | Soft pop, empowering R&B | 90-110 | Uppbeat |
| Tech/Productivity | Lo-fi beats, minimal electronic | 70-90 | Pixabay, Lo-fi Girl |
| Biohacking | Electronic synth, ambient | 80-100 | Mixkit |

### Beat Sync Tips

```typescript
// For 140 BPM phonk: 1 beat = 0.43 seconds = 13 frames at 30fps
// Sync cuts to every 2 beats (26 frames)

const BPM = 140;
const FRAMES_PER_BEAT = (60 / BPM) * 30; // ~13 frames

// Cut on beat
const shouldCut = frame % (FRAMES_PER_BEAT * 2) < 1;
```

---

## Batch Rendering

### Single Video Render

```bash
# Preview first
npx remotion preview src/remotion/index.tsx --props='{"app":"prayerlock"}'

# Render single composition
npx remotion render src/remotion/index.tsx PrayerLockPromoV2 out/prayerlock-promo.mp4
```

### Batch Render Script

```bash
#!/bin/bash
# render-all-promos.sh

COMPOSITIONS=(
  "PrayerLockPromoV2"
  "StepUnlockPromoV2"
  "BioMaxxPromoV2"
  "GlowMaxxPromoV2"
  "PromptVaultPromoV2"
  "DailyAnchorPromoV2"
  "DevotionFlowPromoV2"
  "FocusPrayerPromoV2"
  "LearnLockPromoV2"
)

OUTPUT_DIR="out/videos"
mkdir -p $OUTPUT_DIR

for comp in "${COMPOSITIONS[@]}"; do
  echo "Rendering $comp..."
  npx remotion render src/remotion/index.tsx $comp "$OUTPUT_DIR/$comp.mp4"
done

echo "All videos rendered to $OUTPUT_DIR"
```

### Parallel Rendering (Faster)

```bash
#!/bin/bash
# render-parallel.sh

COMPOSITIONS=(
  "PrayerLockPromoV2"
  "StepUnlockPromoV2"
  "BioMaxxPromoV2"
)

OUTPUT_DIR="out/videos"
mkdir -p $OUTPUT_DIR

# Run renders in parallel (adjust -P based on CPU cores)
printf '%s\n' "${COMPOSITIONS[@]}" | xargs -P 3 -I {} \
  npx remotion render src/remotion/index.tsx {} "$OUTPUT_DIR/{}.mp4"
```

### Programmatic Batch Rendering

```typescript
// batch-render.ts
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';

const compositions = [
  'PrayerLockPromoV2',
  'StepUnlockPromoV2',
  'BioMaxxPromoV2',
];

async function renderAll() {
  const bundled = await bundle({
    entryPoint: './src/remotion/index.tsx',
  });

  for (const compositionId of compositions) {
    const composition = await selectComposition({
      serveUrl: bundled,
      id: compositionId,
    });

    await renderMedia({
      composition,
      serveUrl: bundled,
      codec: 'h264',
      outputLocation: `out/${compositionId}.mp4`,
    });

    console.log(`Rendered ${compositionId}`);
  }
}

renderAll();
```

### Export Settings

```typescript
// Recommended export config
const exportConfig = {
  width: 1080,
  height: 1920,
  fps: 30,
  codec: 'h264',
  crf: 18, // High quality (lower = better, larger file)
  audioCodec: 'aac',
  audioBitrate: '192k',
};

// For smaller file size
const webConfig = {
  ...exportConfig,
  crf: 23, // Good quality, smaller file
};

// For maximum quality (slow)
const qualityConfig = {
  ...exportConfig,
  crf: 15,
  pixelFormat: 'yuv420p',
};
```

---

## Workflow Integration

### Creating Videos for New Apps

1. **Generate App Icon** (required first)

```bash
# Use Gemini API via MCP or browser
# Prompt: "3D app icon, [APP_NAME], [NICHE], gradient, glossy, 1024x1024"

# Save to:
# public/icons/{app-name}-icon-1024.png
```

2. **Create Composition File**

```typescript
// src/remotion/compositions/NewAppPromoV2.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
  Img,
  Audio,
  staticFile,
} from 'remotion';

// Define brand colors
const PRIMARY = '#00FF88';
const SECONDARY = '#1A1A1A';
const TEXT = '#FFFFFF';

// ... composition code following existing patterns
```

3. **Register in Root.tsx**

```typescript
import { NewAppPromoV2 } from './compositions/NewAppPromoV2';

// Add to RemotionRoot
<Composition
  id="NewAppPromoV2"
  component={NewAppPromoV2}
  durationInFrames={360}
  fps={30}
  width={1080}
  height={1920}
/>
```

4. **Preview and Render**

```bash
# Preview
npx remotion preview src/remotion/index.tsx NewAppPromoV2

# Render
npx remotion render src/remotion/index.tsx NewAppPromoV2 out/newapp-promo.mp4
```

### Ralph Loop Integration

Videos can be generated as part of overnight ralph loops:

```bash
# In ralph loop script
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LANDING/printmaxx-site

# Render all pending videos
./scripts/render-all-promos.sh >> ../../../ralph/logs/video_render.log 2>&1
```

### Output Locations

```
LANDING/printmaxx-site/out/              # Default Remotion output
builds/{app}/marketing/videos/           # Per-app marketing assets
MONEY_METHODS/APP_FACTORY/assets/videos/ # Shared templates
```

---

## Best Practices

### Performance Optimization

1. **Use `useMemo` for static calculations**

```typescript
const particles = useMemo(
  () => Array.from({ length: 20 }, () => ({
    x: Math.random() * 100,
    y: Math.random() * 100,
  })),
  [] // Empty deps = calculated once
);
```

2. **Optimize image loading**

```typescript
// Preload images
import { preloadImage } from '@remotion/preload';

preloadImage(staticFile('icons/app-icon.png'));
```

3. **Limit particle counts**

- TikTok videos: 8-15 particles max
- Long-form: 15-25 particles max
- Complex backgrounds: reduce to 5-10

### Code Organization

1. **One composition per file** for maintainability
2. **Shared components** in `components/` directory
3. **Constants at top** (colors, durations, spring configs)
4. **Scene components** as separate functions within file

### Quality Checklist

Before rendering:

- [ ] Logo has depth/dimension (not flat letter)
- [ ] Background has animated elements
- [ ] Text uses spring animations
- [ ] Features stagger with 10-15 frame delays
- [ ] CTA has attention-grabbing animation
- [ ] Audio fades in/out (no abrupt starts)
- [ ] Colors match brand palette
- [ ] Tested at 1080x1920 resolution

### Common Mistakes to Avoid

1. **No audio fade** - Always fade in/out
2. **Static backgrounds** - Add subtle motion
3. **Uniform timing** - Stagger everything
4. **Hard cuts** - Use transitions
5. **Wrong aspect ratio** - Always 9:16 for TikTok

---

## Quick Reference

### Resolution Presets

| Platform | Width | Height | Aspect |
|----------|-------|--------|--------|
| TikTok/Reels | 1080 | 1920 | 9:16 |
| YouTube Shorts | 1080 | 1920 | 9:16 |
| YouTube | 1920 | 1080 | 16:9 |
| Square (IG Feed) | 1080 | 1080 | 1:1 |

### Duration Presets

| Video Type | Frames | Seconds | Best For |
|------------|--------|---------|----------|
| Hook | 150 | 5 | Scroll stoppers |
| Promo | 360 | 12 | TikTok/Reels |
| Demo | 450 | 15 | Features |
| Announcement | 750 | 25 | Launches |
| Tutorial | 1800 | 60 | How-to |

### Commands Cheat Sheet

```bash
# Preview
npx remotion preview src/remotion/index.tsx

# Preview specific composition
npx remotion preview src/remotion/index.tsx --props='{"compositionId":"PrayerLockPromoV2"}'

# Render
npx remotion render src/remotion/index.tsx CompositionName output.mp4

# Render with custom settings
npx remotion render src/remotion/index.tsx CompositionName output.mp4 \
  --crf=18 \
  --codec=h264 \
  --audio-codec=aac

# List all compositions
npx remotion compositions src/remotion/index.tsx

# Studio (visual editor)
npx remotion studio src/remotion/index.tsx
```

---

## Related Files

- `OPS/prompts/remotion/REMOTION_MASTER_PROMPT.md` - Full prompts by style
- `OPS/prompts/remotion/REMOTION_VIDEO_PROMPT.md` - Animation guidelines
- `OPS/prompts/remotion/APP_LAUNCH_VIDEO_SPECS.md` - Per-app specifications
- `OPS/prompts/remotion/SOUND_DESIGN_GUIDE.md` - Audio selection
- `OPS/prompts/remotion/TIKTOK_MUSIC_TRENDS.md` - Trending sounds
- `MONEY_METHODS/APP_FACTORY/ASSET_GENERATION_GUIDE.md` - Icon generation

---

## Troubleshooting

### Common Issues

**"Cannot find module 'remotion'"**
```bash
npm install remotion @remotion/cli
```

**Black screen on render**
- Check image paths are correct
- Ensure staticFile paths exist in public/
- Verify composition is registered in Root.tsx

**Audio not playing in preview**
- Browser may block autoplay
- Click in preview to enable audio
- Check file exists in public/music/

**Slow rendering**
- Reduce particle count
- Lower CRF for faster (but lower quality) renders
- Use `--concurrency` flag to utilize more CPU cores

**Out of memory**
- Reduce resolution for testing
- Close other applications
- Use `--frames` to render segments

---

*Created: January 2026 | Maintained by PRINTMAXX automation system*
