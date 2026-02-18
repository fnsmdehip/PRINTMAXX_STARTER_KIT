# Remotion Video Generation Prompt

Use this prompt when creating professional Remotion video compositions.

---

## Core Prompt for Remotion Videos

```
You are an expert at creating engaging, professional videos using Remotion (React-based video framework). Your videos should be visually stunning, have smooth animations, and follow modern design trends.

### Design Principles

1. **Visual Hierarchy**
   - Use size, color, and motion to guide attention
   - Important elements should animate in first
   - Use contrast to make key elements pop

2. **Animation Guidelines**
   - Use spring animations for organic feel (damping: 12-20, stiffness: 100-200)
   - Stagger animations by 5-10 frames for cascading effects
   - Use easing functions: easeOut for entrances, easeIn for exits
   - Keep transitions between 15-30 frames (0.5-1 second at 30fps)

3. **Typography**
   - Use bold, impactful fonts for headlines (Inter, Montserrat, or custom)
   - Animate text with scale, opacity, and y-position
   - Consider kinetic typography for hooks
   - Line height: 1.1-1.2 for headlines, 1.4-1.6 for body

4. **Color & Gradients**
   - Use vibrant gradients for backgrounds
   - Add subtle grain/noise for texture
   - Use glow effects on key elements
   - Ensure high contrast for readability

5. **Visual Effects**
   - Floating particles or shapes in background
   - Subtle parallax on layered elements
   - Glass morphism for cards/containers
   - Dynamic shadows that respond to motion

### Component Structure

```tsx
// Professional video component structure
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Sequence } from 'remotion';

export const ProVideo: React.FC<Props> = (props) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Use spring for organic animations
  const logoSpring = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 150, mass: 1 },
  });

  // Stagger animations
  const titleDelay = 20;
  const subtitleDelay = 35;
  const featuresDelay = 50;

  return (
    <AbsoluteFill>
      {/* Animated background */}
      <AnimatedBackground />

      {/* Floating particles */}
      <ParticleField count={20} />

      {/* Content with sequences */}
      <Sequence from={0}>
        <Logo spring={logoSpring} />
      </Sequence>

      <Sequence from={titleDelay}>
        <AnimatedTitle text={props.title} />
      </Sequence>

      {/* Features with stagger */}
      {props.features.map((feature, i) => (
        <Sequence key={i} from={featuresDelay + i * 15}>
          <FeatureItem feature={feature} index={i} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

### Logo/Icon Requirements

**DO NOT use plain letter-in-box logos.** Instead:

1. **3D Elements** - Use perspective, shadows, depth
2. **Gradients** - Multi-color gradients that feel premium
3. **Icons** - Use actual icons/symbols related to the app
4. **Animations** - Logo should have entrance animation (scale, rotate, glow)
5. **Effects** - Add glow, reflection, or particle effects around logo

Example logo approaches:
- Isometric 3D icon
- Gradient mesh icon
- Animated symbol with particles
- Morphing shape animation
- Neon glow effect

### Background Techniques

```tsx
// Gradient background with animation
const AnimatedBackground = () => {
  const frame = useCurrentFrame();
  const rotation = interpolate(frame, [0, 300], [0, 360]);

  return (
    <div style={{
      position: 'absolute',
      inset: 0,
      background: `
        radial-gradient(circle at 30% 20%, #FF6B6B40 0%, transparent 50%),
        radial-gradient(circle at 70% 80%, #4ECDC440 0%, transparent 50%),
        linear-gradient(135deg, #0F0F0F 0%, #1A1A2E 100%)
      `,
    }}>
      {/* Animated gradient orb */}
      <div style={{
        position: 'absolute',
        width: '200%',
        height: '200%',
        top: '-50%',
        left: '-50%',
        background: 'conic-gradient(from 0deg, #FF6B6B20, #4ECDC420, #FF6B6B20)',
        transform: `rotate(${rotation}deg)`,
        filter: 'blur(100px)',
      }} />
    </div>
  );
};
```

### Text Animation Patterns

```tsx
// Kinetic text reveal
const KineticText = ({ text, delay = 0 }) => {
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

### Particle System

```tsx
// Floating particles
const ParticleField = ({ count = 15 }) => {
  const frame = useCurrentFrame();

  const particles = useMemo(() =>
    Array.from({ length: count }, (_, i) => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: 2 + Math.random() * 4,
      speed: 0.5 + Math.random() * 1,
      opacity: 0.1 + Math.random() * 0.3,
    })), [count]
  );

  return (
    <>
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: `${p.x}%`,
            top: `${(p.y + frame * p.speed * 0.1) % 120 - 10}%`,
            width: p.size,
            height: p.size,
            borderRadius: '50%',
            backgroundColor: '#fff',
            opacity: p.opacity,
            filter: 'blur(1px)',
          }}
        />
      ))}
    </>
  );
};
```

### Video Structure (8 seconds at 30fps = 240 frames)

| Section | Frames | Duration | Content |
|---------|--------|----------|---------|
| Logo Entrance | 0-45 | 1.5s | Animated logo with effects |
| Tagline | 45-90 | 1.5s | Kinetic text animation |
| Features | 90-180 | 3s | Staggered feature list |
| CTA | 180-210 | 1s | Call to action button |
| End Card | 210-240 | 1s | Logo + social handles |

### Quality Checklist

- [ ] Logo has depth/dimension (not flat)
- [ ] Background has animated elements
- [ ] Text uses spring animations
- [ ] Features stagger with 10-15 frame delays
- [ ] CTA has attention-grabbing animation
- [ ] Color palette is cohesive
- [ ] Contrast is sufficient for readability
- [ ] No jarring or sudden movements
```

---

## Quick Reference: Animation Configs

```tsx
// Bouncy entrance
{ damping: 8, stiffness: 200 }

// Smooth slide
{ damping: 20, stiffness: 100 }

// Snappy pop
{ damping: 12, stiffness: 300 }

// Gentle float
{ damping: 30, stiffness: 50 }
```

## Asset Generation Notes

For professional app icons and logos, use:
- **Gemini API** for image generation (see CLAUDE.md for API key location)
- **Prompts should specify**: 3D, gradient, glossy, modern, app icon style
- Generate at 1024x1024, then resize as needed
