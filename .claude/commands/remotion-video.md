---
name: remotion-video
description: Create videos with Remotion using React. Supports animations, captions, 3D, charts, and more.
---

# Remotion Video Generation

Use Remotion to create programmatic videos in React.

## Setup Check

First verify Remotion is installed:
```bash
cd LANDING/printmaxx-site && npm list remotion 2>/dev/null || echo "Need to install: npm install remotion @remotion/cli @remotion/player"
```

## Quick Start

1. **Create a composition** in `src/remotion/` folder
2. **Define props** for dynamic content (text, images, data)
3. **Use interpolation** for smooth animations
4. **Render** with `npx remotion render`

## Rules Reference

Read these for domain-specific knowledge:
- `.claude/remotion-skills/skills/remotion/rules/animations.md` - Core animation patterns
- `.claude/remotion-skills/skills/remotion/rules/text-animations.md` - Typography effects
- `.claude/remotion-skills/skills/remotion/rules/display-captions.md` - TikTok-style captions
- `.claude/remotion-skills/skills/remotion/rules/transitions.md` - Scene transitions
- `.claude/remotion-skills/skills/remotion/rules/timing.md` - Easing and springs

## Common Tasks

### Social video with captions
```
Read rules/display-captions.md and rules/text-animations.md
Create 30-60 second vertical video (1080x1920)
Add animated text with TikTok-style highlighting
```

### Product demo
```
Read rules/videos.md and rules/sequencing.md
Embed screen recording
Add overlays and callouts
Export at 1080p
```

### Data visualization
```
Read rules/charts.md and rules/animations.md
Animate chart data entry
Use spring physics for organic feel
```

## Output

Videos render to `out/` folder. Common formats:
- MP4 (H.264) - universal compatibility
- WebM (VP9) - smaller size
- GIF - short loops

## Usage

After defining composition, render:
```bash
npx remotion render src/remotion/index.ts CompositionName out/video.mp4
```
