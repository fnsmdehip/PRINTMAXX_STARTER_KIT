# GlowMaxx Landing Page Style Guide

**Purpose:** Aggregate best practices from top looksmaxxing apps (UMAX, LooksMax AI, Maxxing) while differentiating with warm, encouraging aesthetic.

---

## Color Palette

### Primary Colors
```css
--primary: #FF6B6B;         /* Warm coral - main CTA, highlights */
--primary-dark: #E85555;    /* Hover states */
--secondary: #4ECDC4;       /* Teal accent - secondary buttons */
--accent: #FFD93D;          /* Gold - achievements, badges */
```

### Background & Surface
```css
--bg-dark: #0F0F0F;         /* True black - premium feel */
--bg-surface: #1A1A1A;      /* Card backgrounds */
--bg-elevated: #2D2D2D;     /* Elevated cards */
```

### Text
```css
--text-primary: #FFFFFF;
--text-secondary: #9CA3AF;
--text-muted: #6B7280;
```

### Rating Colors (like LooksMax AI)
```css
--rating-high: #10B981;     /* Green for high scores */
--rating-mid: #F59E0B;      /* Amber for medium */
--rating-low: #EF4444;      /* Red for low */
```

---

## Typography

### Font Stack
```css
font-family: 'SF Pro Display', 'Inter', -apple-system, sans-serif;
```

### Scale
| Use | Size | Weight |
|-----|------|--------|
| Hero headline | 48-64px | 700 |
| Section headline | 32-40px | 600 |
| Card headline | 20-24px | 600 |
| Body | 16-18px | 400 |
| Caption | 12-14px | 400 |

---

## Layout Principles

### Hero Section
- Dark background for premium feel
- Large app mockup on right (or centered on mobile)
- Clear value prop headline
- Social proof immediately visible
- Two CTAs: Primary (App Store) + Secondary (Learn More)

### Feature Sections
- Alternating image/text layout
- Dark cards with subtle borders
- Progress visualization (rings, charts)
- Before/after comparisons

### Testimonials
- Real photos (or anonymized)
- Star ratings
- Specific results mentioned
- Short, scannable quotes

---

## Hero Section Copy Template

```
Headline: Your Daily Glow-Up Companion
Subhead: Track mewing, master debloating, build habits that actually work.

Social Proof: Trusted by 50,000+ on their transformation journey
Rating: ⭐ 4.8 stars (1.2k reviews)

CTA Primary: Download Free
CTA Secondary: See How It Works
```

---

## Feature Blocks

### 1. Mewing Timer
```
Headline: Master proper tongue posture
Body: Track your mewing sessions with guided reminders.
      Build the habit that changes everything.
Visual: App screenshot showing mewing timer UI
```

### 2. Debloat Tracker
```
Headline: Wake up looking your best
Body: Track water, sleep, and sodium.
      See exactly what's causing puffiness.
Visual: App screenshot showing debloat dashboard
```

### 3. Daily Routines
```
Headline: 5-minute routines that compound
Body: Facial exercises, skincare protocols, posture checks.
      Gender-specific routines for your goals.
Visual: App screenshot showing routine cards
```

### 4. Progress Photos
```
Headline: See your transformation
Body: Same angles, same lighting, real results.
      Compare week-over-week changes.
Visual: Before/after comparison UI
```

---

## Social Proof Elements

### Metrics Bar
```
50,000+ Users | 4.8 ⭐ Rating | 1.2k Reviews
```

### Testimonial Format
```
"[Specific result] in [timeframe]"
— Name, Age (optional: before/after thumbnail)
```

### Example Testimonials
```
"My jawline is more defined after 3 months of consistent mewing"
— Alex, 24

"The debloat tracker helped me figure out sodium was the problem"
— Jordan, 28

"Finally an app that's not just AI rating. Actual habits that work."
— Taylor, 22
```

---

## CTA Buttons

### Primary (Download)
```css
background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
color: white;
border-radius: 12px;
padding: 16px 32px;
font-weight: 600;
```

### Secondary
```css
background: transparent;
border: 2px solid #FF6B6B;
color: #FF6B6B;
border-radius: 12px;
padding: 16px 32px;
```

---

## App Store Badge Placement

- Both iOS and Android badges
- Horizontal alignment
- White variant on dark backgrounds
- Minimum 135px width

---

## Screenshot Guidelines

### Style
- Dark device frames (iPhone 15 Pro, Space Black)
- Actual app UI (not mockups)
- Show key features: mewing timer, progress rings, routines
- Status bar showing good time (9:41 AM)

### Order (App Store)
1. Progress dashboard overview
2. Mewing timer in action
3. Debloat tracker
4. Routines list
5. Progress photos comparison
6. Learn/education section

---

## Footer

### Links
- Privacy Policy
- Terms of Service
- Contact/Support
- Instagram (if active)

### Legal
```
GlowMaxx is a lifestyle and wellness app. Results vary by individual.
Not medical advice. Consult healthcare provider before starting any routine.
```

---

## Differentiation from Competitors

| Competitor | Their Approach | GlowMaxx Difference |
|------------|----------------|---------------------|
| UMAX | AI face rating focus | Daily habit tracking focus |
| UMAX | Cold blue aesthetic | Warm coral/teal aesthetic |
| UMAX | Masculine-only | Gender-inclusive with toggle |
| LooksMax AI | Paywall before value | Free trial with real features |
| All | One-time scan | Daily engagement loop |
| All | Scores without education | Full Learn tab with guides |

---

## Mobile Responsive

### Breakpoints
```css
/* Mobile first */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
```

### Mobile Hero
- Center aligned
- App mockup below headline
- Single column layout
- Full-width CTAs

---

## Animation Guidelines

### Micro-interactions
- Button hover: slight scale (1.02) + shadow
- Cards: subtle lift on hover
- Progress rings: animate on scroll into view
- Numbers: count-up animation for metrics

### Page Transitions
- Fade in on scroll
- Stagger feature cards
- Smooth anchor scrolling

---

## SEO Keywords (For Landing Page)

### Primary
- looksmaxxing app
- mewing tracker
- facial exercises app
- debloating app
- glow up app

### Secondary
- jawline exercises
- face yoga app
- softmaxxing guide
- facial structure improvement
- looksmax routine

### Long-tail
- how to debloat face
- mewing progress tracker
- daily looksmaxxing routine
- before and after looksmax
