# PRINTMAXX Design System

Version 1.0 | March 2026

---

## Table of Contents

1. [Brand Color Palettes](#brand-color-palettes)
2. [Typography](#typography)
3. [Component Patterns](#component-patterns)
4. [Social Media Image Sizes](#social-media-image-sizes)
5. [Bio Templates](#bio-templates)

---

## Brand Color Palettes

### @printmaxxer — Dark Mode / Terminal Aesthetic

| Role         | Color   | Hex       | Usage                          |
|--------------|---------|-----------|--------------------------------|
| Background   | Black   | `#0D0D0D` | Primary background             |
| Surface      | Charcoal| `#1A1A2E` | Cards, panels                  |
| Primary      | Neon Green | `#00FF41` | Headlines, CTAs, accents    |
| Secondary    | Cyan    | `#00D4FF` | Links, hover states            |
| Accent       | Amber   | `#FFB300` | Warnings, revenue highlights   |
| Text Primary | White   | `#E0E0E0` | Body text                      |
| Text Muted   | Gray    | `#6B6B6B` | Secondary text                 |
| Border       | Dark Green | `#0A3D0A` | Subtle borders, dividers    |
| Error        | Red     | `#FF3333` | Alerts, errors                 |
| Success      | Bright Green | `#39FF14` | Confirmations, metrics up  |

### @selahmoments — Warm Earth Tones / Peaceful

| Role         | Color       | Hex       | Usage                        |
|--------------|-------------|-----------|------------------------------|
| Background   | Warm White  | `#FFF8F0` | Primary background           |
| Surface      | Linen       | `#FAF0E6` | Cards, panels                |
| Primary      | Gold        | `#C9A84C` | Headlines, CTAs              |
| Secondary    | Terracotta  | `#C67B5C` | Accents, buttons             |
| Accent       | Sage        | `#8B9A6B` | Tags, badges                 |
| Text Primary | Espresso    | `#3C2415` | Body text                    |
| Text Muted   | Warm Gray   | `#8C7B6B` | Secondary text               |
| Border       | Sand        | `#DDD0C0` | Borders, dividers            |
| Highlight    | Soft Amber  | `#F5E6CC` | Callout backgrounds          |
| Deep Gold    | Antique     | `#B8860B` | Premium accents              |

### @repscheme — High Contrast / Bold / Aggressive

| Role         | Color       | Hex       | Usage                        |
|--------------|-------------|-----------|------------------------------|
| Background   | True Black  | `#000000` | Primary background           |
| Surface      | Dark Gray   | `#1C1C1C` | Cards, panels                |
| Primary      | Blood Red   | `#E60012` | Headlines, CTAs, power moves |
| Secondary    | White       | `#FFFFFF` | Contrast text                |
| Accent       | Steel       | `#B0B0B0` | Secondary accents            |
| Text Primary | White       | `#FFFFFF` | Body text on dark            |
| Text Dark    | Black       | `#000000` | Body text on light           |
| Border       | Dark Red    | `#8B0000` | Borders, dividers            |
| Warning      | Orange      | `#FF6B00` | Urgency, timers              |
| Highlight    | Yellow      | `#FFD700` | PR numbers, achievements     |

### @drifthour — Soft Blues / Lavender / Calming

| Role         | Color       | Hex       | Usage                        |
|--------------|-------------|-----------|------------------------------|
| Background   | Cloud White | `#F5F0FF` | Primary background           |
| Surface      | Mist        | `#EDE7F6` | Cards, panels                |
| Primary      | Lavender    | `#7C4DFF` | Headlines, CTAs              |
| Secondary    | Soft Blue   | `#64B5F6` | Links, accents               |
| Accent       | Periwinkle  | `#9FA8DA` | Tags, badges                 |
| Text Primary | Deep Indigo | `#1A0A3E` | Body text                    |
| Text Muted   | Slate       | `#78748C` | Secondary text               |
| Border       | Light Lilac | `#D1C4E9` | Borders, dividers            |
| Calm Blue    | Sky         | `#B3E5FC` | Backgrounds, wellness cues   |
| Highlight    | Blush       | `#F3E5F5` | Callout backgrounds          |

### @clipvault — Vibrant Purple/Orange / Streaming Energy

| Role         | Color       | Hex       | Usage                        |
|--------------|-------------|-----------|------------------------------|
| Background   | Deep Navy   | `#0A0A1A` | Primary background           |
| Surface      | Dark Purple | `#1A1030` | Cards, panels                |
| Primary      | Electric Purple | `#9B30FF` | Headlines, CTAs           |
| Secondary    | Hot Orange  | `#FF6B35` | Accents, highlights          |
| Accent       | Magenta     | `#FF2D95` | Badges, live indicators      |
| Text Primary | White       | `#F0F0F0` | Body text                    |
| Text Muted   | Soft Lilac  | `#A090B0` | Secondary text               |
| Border       | Purple Glow | `#4A1080` | Borders, dividers            |
| Gradient Start | Purple    | `#9B30FF` | Gradient backgrounds         |
| Gradient End | Orange      | `#FF6B35` | Gradient backgrounds         |

---

## Typography

All fonts are free Google Fonts.

### @printmaxxer
- **Headings:** `JetBrains Mono` (monospace, terminal feel)
- **Body:** `Inter` (clean, readable)
- **Accent/Code:** `Fira Code` (code snippets, stats)

### @selahmoments
- **Headings:** `Playfair Display` (elegant serif)
- **Body:** `Lora` (warm serif body)
- **Accent:** `Cormorant Garamond` (quotes, callouts)

### @repscheme
- **Headings:** `Oswald` (bold condensed sans-serif)
- **Body:** `Roboto` (clean sans-serif)
- **Accent:** `Anton` (impact headers, numbers)

### @drifthour
- **Headings:** `Quicksand` (soft, rounded sans-serif)
- **Body:** `Nunito` (gentle, airy)
- **Accent:** `Comfortaa` (display text, light feel)

### @clipvault
- **Headings:** `Space Grotesk` (modern geometric sans)
- **Body:** `DM Sans` (clean, tech-forward)
- **Accent:** `Orbitron` (futuristic display)

### Font Loading Snippet

```html
<!-- printmaxxer -->
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">

<!-- selahmoments -->
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lora:wght@400;600&family=Cormorant+Garamond:wght@400;600&display=swap" rel="stylesheet">

<!-- repscheme -->
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Roboto:wght@400;500;700&family=Anton&display=swap" rel="stylesheet">

<!-- drifthour -->
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=Nunito:wght@400;600&family=Comfortaa:wght@400;600&display=swap" rel="stylesheet">

<!-- clipvault -->
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=DM+Sans:wght@400;500;700&family=Orbitron:wght@400;600&display=swap" rel="stylesheet">
```

---

## Component Patterns

### Cards

```css
/* Dark card (printmaxxer, repscheme, clipvault) */
.card-dark {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* Light card (selahmoments, drifthour) */
.card-light {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
```

### Buttons

```css
/* Primary CTA */
.btn-primary {
  background: var(--primary);
  color: var(--bg);
  font-weight: 700;
  padding: 12px 28px;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(var(--primary-rgb), 0.4);
}

/* Ghost / Outline */
.btn-ghost {
  background: transparent;
  color: var(--primary);
  border: 2px solid var(--primary);
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
```

### Badges

```css
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.badge-live { background: #E60012; color: #FFF; }
.badge-new  { background: var(--primary); color: var(--bg); }
.badge-free { background: var(--accent); color: var(--bg); }
```

### Headers

```css
.section-header {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}
.section-subheader {
  font-size: 1.1rem;
  color: var(--text-muted);
  margin-bottom: 32px;
}
```

---

## Social Media Image Sizes

### X (Twitter)
| Asset          | Size (px)   | Aspect Ratio |
|----------------|-------------|--------------|
| Profile Photo  | 400 x 400   | 1:1          |
| Header         | 1500 x 500  | 3:1          |
| In-feed Image  | 1200 x 675  | 16:9         |
| Card Image     | 800 x 418   | 1.91:1       |
| Thread Visual  | 1080 x 1080 | 1:1          |

### Instagram
| Asset          | Size (px)   | Aspect Ratio |
|----------------|-------------|--------------|
| Profile Photo  | 320 x 320   | 1:1          |
| Feed Post      | 1080 x 1080 | 1:1          |
| Portrait       | 1080 x 1350 | 4:5          |
| Story / Reel   | 1080 x 1920 | 9:16         |
| Carousel       | 1080 x 1080 | 1:1          |

### LinkedIn
| Asset          | Size (px)   | Aspect Ratio |
|----------------|-------------|--------------|
| Profile Photo  | 400 x 400   | 1:1          |
| Banner         | 1584 x 396  | 4:1          |
| Post Image     | 1200 x 627  | 1.91:1       |
| Article Cover  | 1200 x 644  | ~1.86:1      |

---

## Bio Templates

### @printmaxxer
```
Building in public. Shipping apps, content, and systems daily.
7 apps live. $0 to revenue documented.
Founder @PRINTMAXX | Dev + Creator
[link-in-bio URL]
```

### @selahmoments
```
Daily reflections for the intentional soul.
Faith. Gratitude. Stillness.
A space to pause and breathe.
[link-in-bio URL]
```

### @repscheme
```
No days off. Track every rep, every set, every win.
Fitness accountability for people who show up.
Built by @printmaxxer
[link-in-bio URL]
```

### @drifthour
```
Your hour to exhale.
Ambient sound. Gentle focus. Digital calm.
Wind down. Drift off.
[link-in-bio URL]
```

### @clipvault
```
Curate. Clip. Create.
The best moments, organized and ready to share.
Content creator's toolkit.
[link-in-bio URL]
```

---

## CSS Custom Property Template

Use this starter template for any brand page. Swap values per brand.

```css
:root {
  /* Swap these per brand */
  --bg: #0D0D0D;
  --surface: #1A1A2E;
  --primary: #00FF41;
  --primary-rgb: 0, 255, 65;
  --secondary: #00D4FF;
  --accent: #FFB300;
  --text-primary: #E0E0E0;
  --text-muted: #6B6B6B;
  --border: #0A3D0A;

  /* Shared */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.15);
  --shadow-md: 0 4px 20px rgba(0,0,0,0.25);
  --shadow-lg: 0 8px 40px rgba(0,0,0,0.35);
  --transition: 0.2s ease;
}
```
