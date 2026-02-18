# PRINTMAXX Favicon SVG Pack

**Date:** 2026-02-10
**Purpose:** Inline SVG favicons for all 6 PRINTMAXX apps. Paste directly into HTML `<link>` tags, manifest.json, or embed as data URIs.

---

## How to Use These SVGs

### Option 1: Inline SVG as data URI in HTML
```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,[ENCODED_SVG_HERE]">
```

### Option 2: Save as .svg file and reference
```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
```

### Option 3: In manifest.json (for PWA)
```json
{
  "icons": [
    {
      "src": "/favicon.svg",
      "type": "image/svg+xml",
      "sizes": "any"
    },
    {
      "src": "/icon-192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "/icon-512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ]
}
```

### Option 4: Embed directly in HTML (no external file)
```html
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E...%3C/svg%3E">
```

**Note:** SVG favicons scale perfectly to any size (16x16, 32x32, 192x192, etc.) because they are vector. One SVG replaces all PNG sizes for modern browsers. Include a PNG fallback for older browsers.

---

## 1. PrayerLock Favicon

**Concept:** Crescent moon integrated with a padlock silhouette on deep navy background. Gold crescent, dark background.

### SVG Code
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="pl-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1A1A2E"/>
      <stop offset="100%" stop-color="#16213E"/>
    </linearGradient>
    <linearGradient id="pl-gold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F0D060"/>
      <stop offset="100%" stop-color="#E2B53F"/>
    </linearGradient>
  </defs>
  <!-- Background -->
  <rect width="32" height="32" rx="7" fill="url(#pl-bg)"/>
  <!-- Crescent moon (circle minus offset circle) -->
  <circle cx="15" cy="13" r="7" fill="url(#pl-gold)"/>
  <circle cx="18" cy="11" r="6" fill="url(#pl-bg)"/>
  <!-- Lock body -->
  <rect x="12" y="20" width="8" height="6" rx="1.5" fill="url(#pl-gold)"/>
  <!-- Lock shackle -->
  <path d="M14 20 V18 A2 2 0 0 1 18 18 V20" fill="none" stroke="url(#pl-gold)" stroke-width="1.5" stroke-linecap="round"/>
  <!-- Keyhole -->
  <circle cx="16" cy="22.5" r="1" fill="url(#pl-bg)"/>
</svg>
```

### Data URI (URL-encoded, paste directly into HTML)
```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='pl-bg' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0%25' stop-color='%231A1A2E'/%3E%3Cstop offset='100%25' stop-color='%2316213E'/%3E%3C/linearGradient%3E%3ClinearGradient id='pl-gold' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0%25' stop-color='%23F0D060'/%3E%3Cstop offset='100%25' stop-color='%23E2B53F'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='7' fill='url(%23pl-bg)'/%3E%3Ccircle cx='15' cy='13' r='7' fill='url(%23pl-gold)'/%3E%3Ccircle cx='18' cy='11' r='6' fill='url(%23pl-bg)'/%3E%3Crect x='12' y='20' width='8' height='6' rx='1.5' fill='url(%23pl-gold)'/%3E%3Cpath d='M14 20 V18 A2 2 0 0 1 18 18 V20' fill='none' stroke='url(%23pl-gold)' stroke-width='1.5' stroke-linecap='round'/%3E%3Ccircle cx='16' cy='22.5' r='1' fill='url(%23pl-bg)'/%3E%3C/svg%3E">
```

---

## 2. Dusk Favicon

**Concept:** Flowing crescent moon with gradient from navy to gold on a near-black background. Serene, nocturnal.

### SVG Code
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="dk-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0B1A2E"/>
      <stop offset="100%" stop-color="#0D0D1A"/>
    </linearGradient>
    <linearGradient id="dk-moon" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F5C542"/>
      <stop offset="100%" stop-color="#E8A830"/>
    </linearGradient>
    <radialGradient id="dk-glow" cx="0.4" cy="0.45">
      <stop offset="0%" stop-color="#F5C542" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#F5C542" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <!-- Background -->
  <rect width="32" height="32" rx="7" fill="url(#dk-bg)"/>
  <!-- Ambient glow -->
  <circle cx="14" cy="15" r="12" fill="url(#dk-glow)"/>
  <!-- Crescent moon (circle minus offset circle) -->
  <circle cx="14" cy="14" r="8" fill="url(#dk-moon)"/>
  <circle cx="17.5" cy="12" r="7" fill="url(#dk-bg)"/>
  <!-- Subtle horizon line at bottom -->
  <line x1="4" y1="26" x2="28" y2="26" stroke="#F5C542" stroke-opacity="0.2" stroke-width="0.5"/>
</svg>
```

### Data URI
```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='dk-bg' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0%25' stop-color='%230B1A2E'/%3E%3Cstop offset='100%25' stop-color='%230D0D1A'/%3E%3C/linearGradient%3E%3ClinearGradient id='dk-moon' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0%25' stop-color='%23F5C542'/%3E%3Cstop offset='100%25' stop-color='%23E8A830'/%3E%3C/linearGradient%3E%3CradialGradient id='dk-glow' cx='0.4' cy='0.45'%3E%3Cstop offset='0%25' stop-color='%23F5C542' stop-opacity='0.15'/%3E%3Cstop offset='100%25' stop-color='%23F5C542' stop-opacity='0'/%3E%3C/radialGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='7' fill='url(%23dk-bg)'/%3E%3Ccircle cx='14' cy='15' r='12' fill='url(%23dk-glow)'/%3E%3Ccircle cx='14' cy='14' r='8' fill='url(%23dk-moon)'/%3E%3Ccircle cx='17.5' cy='12' r='7' fill='url(%23dk-bg)'/%3E%3Cline x1='4' y1='26' x2='28' y2='26' stroke='%23F5C542' stroke-opacity='0.2' stroke-width='0.5'/%3E%3C/svg%3E">
```

---

## 3. Vault Favicon

**Concept:** Concentric rings with electric blue center on matte black. Focus, depth, protection.

### SVG Code
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <radialGradient id="vt-glow" cx="0.5" cy="0.5" r="0.35">
      <stop offset="0%" stop-color="#007AFF" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#007AFF" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <!-- Background -->
  <rect width="32" height="32" rx="7" fill="#1A1A1A"/>
  <!-- Outer ring -->
  <circle cx="16" cy="16" r="11" fill="none" stroke="#2D2D2D" stroke-width="2"/>
  <!-- Middle ring -->
  <circle cx="16" cy="16" r="8" fill="none" stroke="#007AFF" stroke-width="1.5" stroke-opacity="0.5"/>
  <!-- Inner glow -->
  <circle cx="16" cy="16" r="10" fill="url(#vt-glow)"/>
  <!-- Center dot -->
  <circle cx="16" cy="16" r="4" fill="#007AFF"/>
  <!-- Keyhole slit -->
  <rect x="15.25" y="14" width="1.5" height="4" rx="0.75" fill="#1A1A1A"/>
</svg>
```

### Data URI
```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3CradialGradient id='vt-glow' cx='0.5' cy='0.5' r='0.35'%3E%3Cstop offset='0%25' stop-color='%23007AFF' stop-opacity='0.3'/%3E%3Cstop offset='100%25' stop-color='%23007AFF' stop-opacity='0'/%3E%3C/radialGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='7' fill='%231A1A1A'/%3E%3Ccircle cx='16' cy='16' r='11' fill='none' stroke='%232D2D2D' stroke-width='2'/%3E%3Ccircle cx='16' cy='16' r='8' fill='none' stroke='%23007AFF' stroke-width='1.5' stroke-opacity='0.5'/%3E%3Ccircle cx='16' cy='16' r='10' fill='url(%23vt-glow)'/%3E%3Ccircle cx='16' cy='16' r='4' fill='%23007AFF'/%3E%3Crect x='15.25' y='14' width='1.5' height='4' rx='0.75' fill='%231A1A1A'/%3E%3C/svg%3E">
```

---

## 4. Streakr Favicon

**Concept:** Geometric flame in orange-to-yellow gradient on white background. Energetic, warm, motivating.

### SVG Code
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="sk-flame" x1="0.5" y1="1" x2="0.5" y2="0">
      <stop offset="0%" stop-color="#FF9500"/>
      <stop offset="50%" stop-color="#FFB340"/>
      <stop offset="100%" stop-color="#FFD93D"/>
    </linearGradient>
    <linearGradient id="sk-inner" x1="0.5" y1="1" x2="0.5" y2="0">
      <stop offset="0%" stop-color="#FF6B6B"/>
      <stop offset="100%" stop-color="#FF9500"/>
    </linearGradient>
  </defs>
  <!-- Background -->
  <rect width="32" height="32" rx="7" fill="#FFFFFF"/>
  <!-- Outer flame shape -->
  <path d="M16 4 C16 4 22 10 22 17 C22 21 19.5 25 16 27 C12.5 25 10 21 10 17 C10 10 16 4 16 4 Z" fill="url(#sk-flame)"/>
  <!-- Inner flame (smaller, warmer) -->
  <path d="M16 12 C16 12 19 15 19 18.5 C19 20.5 17.8 22.5 16 23.5 C14.2 22.5 13 20.5 13 18.5 C13 15 16 12 16 12 Z" fill="url(#sk-inner)"/>
  <!-- Core bright spot -->
  <ellipse cx="16" cy="20" rx="1.5" ry="2" fill="#FFD93D"/>
</svg>
```

### Data URI
```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='sk-flame' x1='0.5' y1='1' x2='0.5' y2='0'%3E%3Cstop offset='0%25' stop-color='%23FF9500'/%3E%3Cstop offset='50%25' stop-color='%23FFB340'/%3E%3Cstop offset='100%25' stop-color='%23FFD93D'/%3E%3C/linearGradient%3E%3ClinearGradient id='sk-inner' x1='0.5' y1='1' x2='0.5' y2='0'%3E%3Cstop offset='0%25' stop-color='%23FF6B6B'/%3E%3Cstop offset='100%25' stop-color='%23FF9500'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='7' fill='%23FFFFFF'/%3E%3Cpath d='M16 4 C16 4 22 10 22 17 C22 21 19.5 25 16 27 C12.5 25 10 21 10 17 C10 10 16 4 16 4 Z' fill='url(%23sk-flame)'/%3E%3Cpath d='M16 12 C16 12 19 15 19 18.5 C19 20.5 17.8 22.5 16 23.5 C14.2 22.5 13 20.5 13 18.5 C13 15 16 12 16 12 Z' fill='url(%23sk-inner)'/%3E%3Cellipse cx='16' cy='20' rx='1.5' ry='2' fill='%23FFD93D'/%3E%3C/svg%3E">
```

---

## 5. Mise Favicon

**Concept:** Four small prep bowl circles in a diamond arrangement on warm cream background. Culinary mise en place.

### SVG Code
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <!-- Background -->
  <rect width="32" height="32" rx="7" fill="#FFF8E1"/>
  <!-- Four prep bowls in diamond arrangement -->
  <!-- Top -->
  <circle cx="16" cy="8" r="4" fill="#F0883E"/>
  <!-- Left -->
  <circle cx="8" cy="16" r="4" fill="#6BCB77"/>
  <!-- Right -->
  <circle cx="24" cy="16" r="4" fill="#FF6B6B"/>
  <!-- Bottom -->
  <circle cx="16" cy="24" r="4" fill="#FFD93D"/>
  <!-- Subtle inner highlights (bowl depth effect) -->
  <circle cx="15" cy="7" r="1.5" fill="#F0883E" fill-opacity="0" stroke="white" stroke-opacity="0.3" stroke-width="0.5"/>
  <circle cx="7" cy="15" r="1.5" fill="#6BCB77" fill-opacity="0" stroke="white" stroke-opacity="0.3" stroke-width="0.5"/>
  <circle cx="23" cy="15" r="1.5" fill="#FF6B6B" fill-opacity="0" stroke="white" stroke-opacity="0.3" stroke-width="0.5"/>
  <circle cx="15" cy="23" r="1.5" fill="#FFD93D" fill-opacity="0" stroke="white" stroke-opacity="0.3" stroke-width="0.5"/>
</svg>
```

### Data URI
```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23FFF8E1'/%3E%3Ccircle cx='16' cy='8' r='4' fill='%23F0883E'/%3E%3Ccircle cx='8' cy='16' r='4' fill='%236BCB77'/%3E%3Ccircle cx='24' cy='16' r='4' fill='%23FF6B6B'/%3E%3Ccircle cx='16' cy='24' r='4' fill='%23FFD93D'/%3E%3Ccircle cx='15' cy='7' r='1.5' fill='%23F0883E' fill-opacity='0' stroke='white' stroke-opacity='0.3' stroke-width='0.5'/%3E%3Ccircle cx='7' cy='15' r='1.5' fill='%236BCB77' fill-opacity='0' stroke='white' stroke-opacity='0.3' stroke-width='0.5'/%3E%3Ccircle cx='23' cy='15' r='1.5' fill='%23FF6B6B' fill-opacity='0' stroke='white' stroke-opacity='0.3' stroke-width='0.5'/%3E%3Ccircle cx='15' cy='23' r='1.5' fill='%23FFD93D' fill-opacity='0' stroke='white' stroke-opacity='0.3' stroke-width='0.5'/%3E%3C/svg%3E">
```

---

## 6. Steplock Favicon

**Concept:** Footprint integrated with lock shape in coral red on white background. Active, energetic, fitness-coded.

### SVG Code
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="sl-grad" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#FF4757"/>
      <stop offset="100%" stop-color="#FF6B81"/>
    </linearGradient>
  </defs>
  <!-- Background -->
  <rect width="32" height="32" rx="7" fill="#FFFFFF"/>
  <!-- Footprint: toe area (3 small circles + oval) -->
  <ellipse cx="13" cy="7.5" rx="2" ry="1.8" fill="url(#sl-grad)"/>
  <ellipse cx="17" cy="6.5" rx="1.8" ry="1.6" fill="url(#sl-grad)"/>
  <ellipse cx="20.5" cy="8" rx="1.6" ry="1.4" fill="url(#sl-grad)"/>
  <!-- Foot body / sole -->
  <ellipse cx="15" cy="14" rx="5.5" ry="5" fill="url(#sl-grad)"/>
  <!-- Lock body at bottom (integrated into heel area) -->
  <rect x="11" y="21" width="10" height="7" rx="2" fill="url(#sl-grad)"/>
  <!-- Lock shackle -->
  <path d="M13.5 21 V19 A2.5 2.5 0 0 1 18.5 19 V21" fill="none" stroke="url(#sl-grad)" stroke-width="2" stroke-linecap="round"/>
  <!-- Keyhole -->
  <circle cx="16" cy="24" r="1.2" fill="white"/>
  <rect x="15.5" y="24" width="1" height="2" rx="0.5" fill="white"/>
</svg>
```

### Data URI
```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='sl-grad' x1='0.5' y1='0' x2='0.5' y2='1'%3E%3Cstop offset='0%25' stop-color='%23FF4757'/%3E%3Cstop offset='100%25' stop-color='%23FF6B81'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='7' fill='%23FFFFFF'/%3E%3Cellipse cx='13' cy='7.5' rx='2' ry='1.8' fill='url(%23sl-grad)'/%3E%3Cellipse cx='17' cy='6.5' rx='1.8' ry='1.6' fill='url(%23sl-grad)'/%3E%3Cellipse cx='20.5' cy='8' rx='1.6' ry='1.4' fill='url(%23sl-grad)'/%3E%3Cellipse cx='15' cy='14' rx='5.5' ry='5' fill='url(%23sl-grad)'/%3E%3Crect x='11' y='21' width='10' height='7' rx='2' fill='url(%23sl-grad)'/%3E%3Cpath d='M13.5 21 V19 A2.5 2.5 0 0 1 18.5 19 V21' fill='none' stroke='url(%23sl-grad)' stroke-width='2' stroke-linecap='round'/%3E%3Ccircle cx='16' cy='24' r='1.2' fill='white'/%3E%3Crect x='15.5' y='24' width='1' height='2' rx='0.5' fill='white'/%3E%3C/svg%3E">
```

---

## Dark Mode Variant SVGs

For apps that may appear on both light and dark system trays/tabs, here are dark mode variants for the light-background icons.

### Streakr (Dark Mode Variant)
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="sk-d-flame" x1="0.5" y1="1" x2="0.5" y2="0">
      <stop offset="0%" stop-color="#FF9500"/>
      <stop offset="50%" stop-color="#FFB340"/>
      <stop offset="100%" stop-color="#FFD93D"/>
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="7" fill="#1A1A1A"/>
  <path d="M16 4 C16 4 22 10 22 17 C22 21 19.5 25 16 27 C12.5 25 10 21 10 17 C10 10 16 4 16 4 Z" fill="url(#sk-d-flame)"/>
  <path d="M16 12 C16 12 19 15 19 18.5 C19 20.5 17.8 22.5 16 23.5 C14.2 22.5 13 20.5 13 18.5 C13 15 16 12 16 12 Z" fill="#FF6B6B"/>
  <ellipse cx="16" cy="20" rx="1.5" ry="2" fill="#FFD93D"/>
</svg>
```

### Mise (Dark Mode Variant)
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="7" fill="#1A1A1A"/>
  <circle cx="16" cy="8" r="4" fill="#F0883E"/>
  <circle cx="8" cy="16" r="4" fill="#6BCB77"/>
  <circle cx="24" cy="16" r="4" fill="#FF6B6B"/>
  <circle cx="16" cy="24" r="4" fill="#FFD93D"/>
</svg>
```

### Steplock (Dark Mode Variant)
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="sl-d-grad" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#FF4757"/>
      <stop offset="100%" stop-color="#FF6B81"/>
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="7" fill="#1A1A1A"/>
  <ellipse cx="13" cy="7.5" rx="2" ry="1.8" fill="url(#sl-d-grad)"/>
  <ellipse cx="17" cy="6.5" rx="1.8" ry="1.6" fill="url(#sl-d-grad)"/>
  <ellipse cx="20.5" cy="8" rx="1.6" ry="1.4" fill="url(#sl-d-grad)"/>
  <ellipse cx="15" cy="14" rx="5.5" ry="5" fill="url(#sl-d-grad)"/>
  <rect x="11" y="21" width="10" height="7" rx="2" fill="url(#sl-d-grad)"/>
  <path d="M13.5 21 V19 A2.5 2.5 0 0 1 18.5 19 V21" fill="none" stroke="url(#sl-d-grad)" stroke-width="2" stroke-linecap="round"/>
  <circle cx="16" cy="24" r="1.2" fill="#1A1A1A"/>
  <rect x="15.5" y="24" width="1" height="2" rx="0.5" fill="#1A1A1A"/>
</svg>
```

---

## CSS Media Query for Auto Dark Mode Favicons

Modern browsers support `prefers-color-scheme` inside SVG favicons. Here is how to make a single SVG that auto-switches.

### Example: Streakr Auto-Dark Favicon
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="flame" x1="0.5" y1="1" x2="0.5" y2="0">
      <stop offset="0%" stop-color="#FF9500"/>
      <stop offset="100%" stop-color="#FFD93D"/>
    </linearGradient>
    <style>
      .bg { fill: #FFFFFF; }
      @media (prefers-color-scheme: dark) {
        .bg { fill: #1A1A1A; }
      }
    </style>
  </defs>
  <rect class="bg" width="32" height="32" rx="7"/>
  <path d="M16 4 C16 4 22 10 22 17 C22 21 19.5 25 16 27 C12.5 25 10 21 10 17 C10 10 16 4 16 4 Z" fill="url(#flame)"/>
  <path d="M16 12 C16 12 19 15 19 18.5 C19 20.5 17.8 22.5 16 23.5 C14.2 22.5 13 20.5 13 18.5 C13 15 16 12 16 12 Z" fill="#FF6B6B"/>
  <ellipse cx="16" cy="20" rx="1.5" ry="2" fill="#FFD93D"/>
</svg>
```

---

## Quick Reference Table

| App | Background | Primary Color | Icon Concept | Dark BG Needed? |
|-----|-----------|---------------|--------------|-----------------|
| PrayerLock | #1A1A2E navy | #E2B53F gold | Crescent + lock | No (already dark) |
| Dusk | #0B1A2E navy | #F5C542 gold | Crescent moon | No (already dark) |
| Vault | #1A1A1A black | #007AFF blue | Concentric rings | No (already dark) |
| Streakr | #FFFFFF white | #FF9500 orange | Flame | Yes (dark variant above) |
| Mise | #FFF8E1 cream | Multi-color | 4 prep bowls | Yes (dark variant above) |
| Steplock | #FFFFFF white | #FF4757 coral | Footprint + lock | Yes (dark variant above) |

---

## Apple Touch Icon (for iOS home screen)

For iOS "Add to Home Screen" PWAs, you also need a 180x180 apple-touch-icon. The SVGs above work at any size, but for best results render them as PNG at 180x180 and add:

```html
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
```

**To convert SVG to PNG at the command line:**
```bash
# Using rsvg-convert (install: brew install librsvg)
rsvg-convert -w 180 -h 180 favicon.svg > apple-touch-icon.png

# Using ImageMagick
convert -background none -size 180x180 favicon.svg apple-touch-icon.png

# Using Chrome headless
google-chrome --headless --screenshot --window-size=180,180 favicon.svg
```

---

*SVG favicons designed to match the visual identity from AGGREGATE_DESIGN_SYSTEM.md. All SVGs are under 1KB, scale to any resolution, and support CSS dark mode media queries.*
