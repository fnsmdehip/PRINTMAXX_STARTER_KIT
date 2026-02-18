# BioMaxx Landing Page Style Guide

**Purpose:** Design system for the web landing page, marketing materials, and App Store presence.

---

## Brand Positioning

**Tagline:** "Your Daily Longevity Protocol"

**Value Prop:** Track every biohack. Learn the science. Optimize your biology.

**Tone:** Scientific but accessible. Premium but not elitist. Optimistic about human potential.

---

## Color Palette

### Primary Colors (CSS Variables)
```css
:root {
  /* Brand colors */
  --primary: #10B981;           /* Emerald green - longevity */
  --primary-dark: #059669;      /* Hover states */
  --primary-light: #6EE7B7;     /* Highlights */

  --secondary: #F59E0B;         /* Warm amber - energy */
  --secondary-dark: #D97706;

  --accent: #FFD93D;            /* Gold - achievements */

  /* Backgrounds (dark mode landing) */
  --bg-dark: #0F172A;           /* Deep slate */
  --bg-surface: #1E293B;        /* Cards */
  --bg-elevated: #334155;       /* Elevated elements */

  /* Text */
  --text-primary: #F8FAFC;      /* Off-white */
  --text-secondary: #94A3B8;    /* Muted */
  --text-muted: #64748B;

  /* Protocol colors */
  --protocol-fasting: #8B5CF6;
  --protocol-cold: #06B6D4;
  --protocol-heat: #EF4444;
  --protocol-light: #F59E0B;
  --protocol-supplements: #10B981;
  --protocol-movement: #3B82F6;
  --protocol-sleep: #6366F1;
}
```

### Gradient Usage
```css
/* Hero CTA gradient */
.btn-primary {
  background: linear-gradient(135deg, #10B981, #059669);
}

/* Premium badge gradient */
.badge-premium {
  background: linear-gradient(135deg, #FFD93D, #F59E0B);
}

/* Hero glow effect */
.hero-glow {
  background: radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.15), transparent 50%);
}
```

---

## Typography

### Font Stack
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Scale
| Use | Size | Weight | Line Height |
|-----|------|--------|-------------|
| Hero headline | 56-72px | 800 | 1.1 |
| Section headline | 40-48px | 700 | 1.2 |
| Feature headline | 28-32px | 700 | 1.3 |
| Subhead | 20-24px | 500 | 1.4 |
| Body | 16-18px | 400 | 1.6 |
| Caption | 14px | 500 | 1.4 |
| Badge | 12px | 600 | 1.0 |

### CSS Classes
```css
.heading-hero {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.heading-section {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
}

.text-body {
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--text-secondary);
}
```

---

## Page Sections

### Hero Section
```html
<section class="hero">
  <div class="hero-glow"></div>
  <div class="container">
    <span class="badge">Join 10,000+ biohackers</span>
    <h1 class="heading-hero">
      Your Daily<br>
      <span class="text-gradient">Longevity Protocol</span>
    </h1>
    <p class="subhead">
      Track every biohack. Learn the science. Optimize your biology.
    </p>
    <div class="cta-group">
      <a href="#" class="btn-primary">
        <img src="/app-store-badge.svg" alt="Download on App Store">
      </a>
      <a href="#" class="btn-secondary">See How It Works</a>
    </div>
    <div class="stats-row">
      <div class="stat">
        <span class="stat-value">10,000+</span>
        <span class="stat-label">Active Users</span>
      </div>
      <div class="stat">
        <span class="stat-value">4.8★</span>
        <span class="stat-label">App Store Rating</span>
      </div>
      <div class="stat">
        <span class="stat-value">500k+</span>
        <span class="stat-label">Sessions Logged</span>
      </div>
    </div>
  </div>
  <div class="hero-mockup">
    <img src="/app-mockup.png" alt="BioMaxx app dashboard">
  </div>
</section>
```

### Feature Sections

**Protocol Tracking Feature**
```
Headline: Track Every Protocol
Body: Fasting, cold exposure, red light therapy, supplements, and more.
      One app to optimize your entire longevity stack.
Visual: App screenshot showing protocol rings dashboard
```

**Learn Feature**
```
Headline: Learn the Science
Body: Understand why each protocol works.
      Protocol stacking guides. Evidence-based optimization.
Visual: App screenshot showing Learn tab with articles
```

**Progress Feature**
```
Headline: See Your Progress
Body: Daily longevity scores. Streak tracking. Weekly insights.
      Watch your biology improve over time.
Visual: App screenshot showing stats and streaks
```

**Gear Recommendations Feature**
```
Headline: Upgrade Your Stack
Body: Expert-curated gear for every protocol.
      From budget-friendly to Bryan Johnson tier.
Visual: Product grid (red light panel, cold plunge, etc.)
```

### Social Proof Section

**Metrics Bar**
```html
<div class="metrics-bar">
  <div class="metric">
    <span class="metric-icon">👥</span>
    <span class="metric-value">10,000+</span>
    <span class="metric-label">Users Optimizing</span>
  </div>
  <div class="metric">
    <span class="metric-icon">⭐</span>
    <span class="metric-value">4.8</span>
    <span class="metric-label">App Store Rating</span>
  </div>
  <div class="metric">
    <span class="metric-icon">🔥</span>
    <span class="metric-value">500k+</span>
    <span class="metric-label">Sessions Tracked</span>
  </div>
</div>
```

**Testimonial Format**
```
"[Specific result] after [timeframe]"
— Name, Age (optional: occupation)
```

**Example Testimonials**
```
"Down 15 lbs and sleeping better than I have in years. The protocol stacking feature is genius."
— Mike, 34, Software Engineer

"Finally an app that tracks everything I do. Fasting, cold plunge, red light - all in one place."
— Sarah, 28, Entrepreneur

"The science articles helped me understand WHY these protocols work. Not just another timer app."
— James, 45, Executive
```

---

## CTA Buttons

### Primary (Download)
```css
.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  padding: 16px 32px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(16, 185, 129, 0.4);
}
```

### Secondary
```css
.btn-secondary {
  background: transparent;
  border: 2px solid var(--primary);
  color: var(--primary);
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 600;
}

.btn-secondary:hover {
  background: rgba(16, 185, 129, 0.1);
}
```

---

## App Store Assets

### App Icon
- Emerald green gradient background
- Simple leaf or infinity symbol
- No text in icon
- 1024x1024 for App Store

### Screenshots (in order)
1. Dashboard with protocol rings and longevity score
2. Protocol list with categories
3. Active fasting timer session
4. Learn tab with science articles
5. Progress stats and achievements
6. Gear recommendations (affiliate)

### App Store Description
```
Track every biohack. Learn the science. Optimize your biology.

BioMaxx is the all-in-one protocol tracker for serious biohackers. Whether you're doing intermittent fasting, cold exposure, red light therapy, or building a supplement stack - track it all in one beautiful app.

TRACK EVERY PROTOCOL
• Fasting (16:8, OMAD, extended)
• Cold exposure (plunge, shower, cryo)
• Heat therapy (sauna, hot bath)
• Red light & PEMF
• Supplements & nootropics
• Sleep optimization
• Movement & exercise

LEARN THE SCIENCE
• Evidence-based protocol guides
• Optimal stacking combinations
• Deep-dive articles on longevity

SEE YOUR PROGRESS
• Daily longevity score
• Protocol streaks & achievements
• Weekly insights & trends

UPGRADE YOUR STACK
• Expert-curated gear recommendations
• From budget to Bryan Johnson tier

Join 10,000+ biohackers optimizing their biology.

Free to try. Premium unlocks all protocols.

---
BioMaxx is for educational purposes only. Not medical advice. Consult your healthcare provider before starting any new health protocols.
```

### Keywords (ASO)
Primary:
- biohacking app
- longevity tracker
- fasting timer
- cold plunge tracker
- red light therapy app

Secondary:
- protocol tracker
- supplement log
- biohacker
- bryan johnson app
- health optimization

Long-tail:
- intermittent fasting tracker with supplements
- cold exposure and sauna tracking
- longevity protocol app
- biohacking journal

---

## Responsive Breakpoints

```css
/* Mobile first */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

### Mobile Hero
- Single column layout
- App mockup below headline
- Full-width CTAs
- Stacked stats

---

## Animation Guidelines

### Micro-interactions
- Button hover: scale(1.02) + shadow increase
- Cards: subtle lift on hover
- Protocol rings: animate on scroll into view
- Numbers: count-up animation on load

### Scroll Animations
```css
/* Fade in on scroll */
.animate-in {
  animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## Footer

### Links
- Privacy Policy
- Terms of Service
- Contact/Support
- Instagram
- Twitter/X

### Legal Disclaimer
```
BioMaxx is a lifestyle and wellness app for educational purposes.
Results vary by individual. Not medical advice.
Consult your healthcare provider before starting any new health protocols.
```

---

## SEO Keywords

### Primary
- biohacking app
- longevity tracker
- protocol tracking app
- fasting timer
- cold plunge tracker

### Secondary
- red light therapy app
- supplement tracker
- biohacker tools
- health optimization app
- bryan johnson protocol

### Long-tail
- best app for tracking biohacks
- intermittent fasting and cold exposure app
- longevity protocol tracker
- biohacking journal app
- how to track sauna sessions

---

## Competitive Differentiation

| Element | Zero | Biohackr | BioMaxx |
|---------|------|----------|---------|
| Hero Color | Blue/White | Purple | Emerald Green |
| Hero Image | Phone mockup | Screenshots | Glowing phone |
| Value Prop | Fasting made simple | Track everything | Longevity protocol |
| Social Proof | Millions of users | None | 10k+ biohackers |
| Tone | Clinical | Tech-forward | Earthy premium |
| CTA | Download | Try free | Start optimizing |
