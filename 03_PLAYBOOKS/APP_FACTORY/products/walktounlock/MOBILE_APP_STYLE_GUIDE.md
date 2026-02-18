# WalkToUnlock - Mobile App Style Guide

## Brand Identity

### Personality
- **Energetic** but not aggressive
- **Motivating** but not preachy
- **Simple** but not boring
- **Friendly** like a walking buddy

### Voice
- Encouraging: "You're almost there!"
- Direct: "Walk to unlock"
- Celebratory: "You did it!"
- Never: Guilt-tripping or negative

---

## Color Palette

### Primary Colors

| Color | Hex | Use |
|-------|-----|-----|
| Walk Green | #4CAF50 | Primary accent, progress, success |
| Deep Green | #2E7D32 | Buttons, CTAs |
| Light Green | #81C784 | Backgrounds, highlights |

### Secondary Colors

| Color | Hex | Use |
|-------|-----|-----|
| Energy Orange | #FF9800 | Warnings, almost there |
| Sunset Orange | #F57C00 | Emphasis |
| Warm Yellow | #FFC107 | Streak highlights |

### Neutral Colors

| Color | Hex | Use |
|-------|-----|-----|
| Dark Gray | #212121 | Primary text |
| Medium Gray | #757575 | Secondary text |
| Light Gray | #EEEEEE | Backgrounds, dividers |
| Off White | #FAFAFA | Card backgrounds |
| Pure White | #FFFFFF | Base background |

### State Colors

| State | Color | Hex |
|-------|-------|-----|
| Locked | Red | #F44336 |
| Progress | Orange | #FF9800 |
| Near Goal | Yellow | #FFC107 |
| Unlocked | Green | #4CAF50 |
| Streak | Gold | #FFD700 |

---

## Typography

### Font Family
- **Primary:** SF Pro (iOS) / Roboto (Android)
- **Numbers:** SF Pro Rounded for step counts
- **Fallback:** System default

### Font Sizes

| Element | Size | Weight |
|---------|------|--------|
| Hero number (steps) | 64px | Bold |
| Goal text | 24px | Medium |
| Section header | 20px | Semibold |
| Body text | 16px | Regular |
| Caption | 14px | Regular |
| Small label | 12px | Medium |

---

## Progress Ring Component

### Specifications
- **Outer diameter:** 250px
- **Stroke width:** 15px
- **Corner style:** Rounded caps

### Animation
- Fill animates clockwise from top
- Duration: 500ms ease-out
- Celebrate pulse at 100%

### Color States
```
0-25%    → Red (#F44336)
25-50%   → Orange (#FF9800)
50-75%   → Yellow (#FFC107)
75-99%   → Light Green (#81C784)
100%     → Green (#4CAF50) + pulse animation
```

---

## Screen Layouts

### Home Screen

```
┌─────────────────────────────────┐
│  ← Settings          Streak 🔥7 │
├─────────────────────────────────┤
│                                 │
│        ┌──────────────┐         │
│        │    3,247     │         │
│        │   / 5,000    │         │
│        └──────────────┘         │
│          Progress Ring          │
│                                 │
│      1,753 steps to go          │
│         ~35 min walk            │
│                                 │
├─────────────────────────────────┤
│  Blocked Apps (tap to manage)   │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│  │ IG │ │ TT │ │ TW │ │ FB │   │
│  │ 🔒 │ │ 🔒 │ │ 🔒 │ │ 🔒 │   │
│  └────┘ └────┘ └────┘ └────┘   │
├─────────────────────────────────┤
│         [Refresh Steps]         │
└─────────────────────────────────┘
```

### Blocked State Screen

```
┌─────────────────────────────────┐
│            🔒                   │
│                                 │
│     Instagram is blocked        │
│                                 │
│     Walk 1,753 more steps       │
│        to unlock                │
│                                 │
│   ┌──────────────────────┐      │
│   │    Progress: 65%     │      │
│   └──────────────────────┘      │
│                                 │
│      [Open WalkToUnlock]        │
│                                 │
│     Emergency unlock?           │
└─────────────────────────────────┘
```

### Unlocked Celebration

```
┌─────────────────────────────────┐
│         🎉  🎊  🎉              │
│                                 │
│      ✓ Goal Complete!          │
│                                 │
│        5,247 steps              │
│         today                   │
│                                 │
│      7 day streak! 🔥           │
│                                 │
│    All apps unlocked            │
│                                 │
│      [View Stats]               │
└─────────────────────────────────┘
```

---

## Buttons and CTAs

### Primary Button
- Background: #2E7D32 (Deep Green)
- Text: White, 16px Semibold
- Corner radius: 12px
- Height: 56px
- Shadow: subtle drop shadow
- Pressed state: darken 10%

### Secondary Button
- Background: #E8F5E9 (very light green)
- Text: #2E7D32, 16px Medium
- Corner radius: 12px
- Height: 48px
- No shadow

---

## Icons

### App Icon
- Green gradient background (light to dark)
- White walking figure silhouette
- Circular progress indicator
- Rounded corners (iOS standard)

### In-App Icons
- Style: SF Symbols (iOS) / Material Icons (Android)
- Size: 24px standard, 20px compact
- Color: Inherit from context

---

## Motion and Animation

### Key Animations
1. **Step update:** Number counts up smoothly (300ms)
2. **Progress fill:** Ring fills clockwise (500ms)
3. **Goal reached:** Confetti + ring pulse
4. **Unlock:** Lock icon rotates open
5. **Pull refresh:** Walking icon bounces

---

## Dark Mode

### Color Adjustments

| Light | Dark |
|-------|------|
| #FFFFFF | #121212 |
| #FAFAFA | #1E1E1E |
| #212121 | #FFFFFF |
| #4CAF50 | #66BB6A |

---

Last updated: 2026-01-23
