# Theming System Guide

A comprehensive design token and theming system for the APP_FACTORY apps. Built with TypeScript for type safety and React context for runtime theme switching.

## Quick Start

### 1. Wrap your app with ThemeProvider

```tsx
// app/layout.tsx
import { ThemeProvider, ThemeScript } from '@/shared/theming';
import { prayerlockLightTheme, prayerlockDarkTheme } from '@/shared/theming/app_themes';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* Prevents flash of wrong theme */}
        <ThemeScript />
      </head>
      <body>
        <ThemeProvider
          defaultMode="system"
          lightThemeOverride={prayerlockLightTheme}
          darkThemeOverride={prayerlockDarkTheme}
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

### 2. Use theme values in components

```tsx
'use client';

import { useTheme, useColor, useModeValue } from '@/shared/theming';

function MyComponent() {
  const { theme, toggleTheme, resolvedMode } = useTheme();

  return (
    <div style={{
      background: theme.colors.background.primary,
      color: theme.colors.text.primary,
      padding: theme.spacing[4],
      borderRadius: theme.radii.lg,
    }}>
      <button onClick={toggleTheme}>
        Switch to {resolvedMode === 'light' ? 'dark' : 'light'} mode
      </button>
    </div>
  );
}
```

## Directory Structure

```
theming/
├── tokens/                    # Design tokens
│   ├── colors.ts             # Color palette
│   ├── typography.ts         # Font scales
│   ├── spacing.ts            # Spacing scale
│   ├── shadows.ts            # Shadow definitions
│   ├── radii.ts              # Border radii
│   └── index.ts              # Token exports
│
├── themes/                    # Theme definitions
│   ├── base.ts               # Shared values (no colors)
│   ├── light.ts              # Light mode colors
│   ├── dark.ts               # Dark mode colors
│   └── index.ts              # Theme exports
│
├── app_themes/               # Brand-specific themes
│   ├── prayerlock_theme.ts   # Faith/meditation app
│   ├── walktounlock_theme.ts # Fitness app
│   ├── studylock_theme.ts    # Focus/study app
│   ├── promptvault_theme.ts  # AI prompts app
│   ├── dailyanchor_theme.ts  # Journaling app
│   ├── femfit_theme.ts       # Women's fitness app
│   ├── dailydevotion_theme.ts# Devotional app
│   └── index.ts              # App theme exports
│
├── ThemeProvider.tsx         # React context provider
├── useTheme.ts               # Theme hooks
├── styled.ts                 # Styling utilities
├── index.ts                  # Main exports
└── THEMING_GUIDE.md          # This file
```

## Design Tokens

### Colors

The color system uses a 10-step scale (50-950) for fine-grained control:

```ts
import { colors } from '@/shared/theming';

// Access raw colors
colors.blue[500]     // '#3B82F6'
colors.gray[900]     // '#171717'
colors.earth.sage    // '#9CAF88'
```

### Typography

```ts
import { fontSizes, fontWeights, textStyles } from '@/shared/theming';

// Font sizes
fontSizes.base  // '1rem'
fontSizes['2xl'] // '1.5rem'

// Predefined text styles
textStyles.h1   // { fontSize, fontWeight, lineHeight, letterSpacing }
textStyles.body // { fontSize, fontWeight, lineHeight, letterSpacing }
```

### Spacing

Based on a 4px grid system:

```ts
import { spacing, semanticSpacing } from '@/shared/theming';

// Raw spacing
spacing[4]   // '1rem' (16px)
spacing[8]   // '2rem' (32px)

// Semantic spacing
semanticSpacing.componentPaddingMd  // spacing[4]
semanticSpacing.sectionPaddingMobile // spacing[6]
```

### Shadows

```ts
import { shadows, elevation, coloredShadows } from '@/shared/theming';

// Standard shadows
shadows.sm   // subtle card shadow
shadows.lg   // modal shadow

// Semantic elevation
elevation.raised   // for cards
elevation.floating // for dropdowns
elevation.overlay  // for modals

// Colored shadows for buttons
coloredShadows.blue.md
coloredShadows.green.lg
```

### Border Radii

```ts
import { radii, componentRadii } from '@/shared/theming';

// Raw radii
radii.lg   // '0.5rem'
radii.full // '9999px' (pill)

// Component-specific
componentRadii.buttonMd  // default button radius
componentRadii.cardLg    // large card radius
componentRadii.badge     // pill-shaped badge
```

## Theme Structure

Each theme contains:

```ts
interface Theme {
  mode: 'light' | 'dark';

  // From base theme
  fonts: { sans, serif, mono };
  fontSizes: { xs, sm, base, lg, ... };
  fontWeights: { thin, normal, bold, ... };
  lineHeights: { tight, normal, relaxed, ... };
  spacing: { 0, 1, 2, 4, 8, ... };
  radii: { sm, md, lg, full, ... };
  breakpoints: { sm, md, lg, xl };
  zIndices: { modal, dropdown, tooltip, ... };
  transitions: { durations, easings, presets };

  // Mode-specific
  colors: {
    background: { primary, secondary, tertiary, ... };
    surface: { primary, secondary, overlay, ... };
    text: { primary, secondary, muted, link, ... };
    border: { primary, focus, error, ... };
    interactive: { primary, primaryHover, ... };
    semantic: { success, error, warning, info, ... };
    accent: { primary, secondary, text };
    focus: { ring, ringOffset };
    input: { background, border, placeholder, ... };
  };
  shadows: { xs, sm, md, lg, xl };
  elevation: { surface, raised, floating, overlay };
}
```

## Hooks Reference

### useTheme

Main hook for accessing theme and controls:

```ts
const {
  theme,        // Current theme object
  mode,         // 'light' | 'dark' | 'system'
  resolvedMode, // 'light' | 'dark' (actual mode after system detection)
  setMode,      // (mode: ThemeMode) => void
  toggleTheme,  // () => void
  isReady,      // boolean (false during hydration)
} = useTheme();
```

### useThemeMode

Get mode information only:

```ts
const {
  mode,         // 'light' | 'dark' | 'system'
  resolvedMode, // 'light' | 'dark'
  isDark,       // boolean
  isLight,      // boolean
  isSystem,     // boolean
} = useThemeMode();
```

### useThemeControls

Get controls only:

```ts
const {
  setMode,     // (mode: ThemeMode) => void
  toggleTheme, // () => void
  setLight,    // () => void
  setDark,     // () => void
  setSystem,   // () => void
} = useThemeControls();
```

### useModeValue

Return different values based on mode:

```ts
const bgColor = useModeValue('#FFFFFF', '#000000');
const icon = useModeValue(<SunIcon />, <MoonIcon />);
```

### useColor

Get a specific color with dot notation:

```ts
const primary = useColor('background.primary');
const link = useColor('text.link');
```

## Adding a New App Theme

1. Create a new file in `app_themes/`:

```ts
// app_themes/myapp_theme.ts
import { colors } from '../tokens/colors';
import { lightTheme } from '../themes/light';
import { darkTheme } from '../themes/dark';
import type { Theme } from '../themes';

// Define brand colors
const brandColors = {
  primary: {
    50: '#...',
    // ... 50 through 950
    500: '#...', // Main brand color
    // ...
  },
  accent: {
    // Secondary brand color
  },
};

// Create light theme
export const myappLightTheme: Theme = {
  ...lightTheme,
  colors: {
    ...lightTheme.colors,
    // Override with brand colors
    interactive: {
      primary: brandColors.primary[500],
      primaryHover: brandColors.primary[600],
      // ...
    },
    accent: {
      primary: brandColors.accent[500],
      // ...
    },
  },
};

// Create dark theme
export const myappDarkTheme: Theme = {
  ...darkTheme,
  colors: {
    ...darkTheme.colors,
    // Override for dark mode
  },
};

// Export brand assets
export const myappBrand = {
  name: 'MyApp',
  tagline: 'Your app tagline',
  colors: brandColors,
  gradients: {
    primary: `linear-gradient(...)`,
  },
};
```

2. Export from `app_themes/index.ts`:

```ts
export {
  myappLightTheme,
  myappDarkTheme,
  myappBrand,
} from './myapp_theme';
```

3. Export from main `index.ts`:

```ts
export {
  myappLightTheme,
  myappDarkTheme,
  myappBrand,
} from './app_themes';
```

## Brand Theme Reference

| App | Primary Color | Accent | Mood |
|-----|---------------|--------|------|
| PrayerLock | Calm blue (#3B8DD9) | Gold (#D4A418) | Peaceful, sacred |
| WalkToUnlock | Green (#10B981) | Orange (#F97316) | Energetic, motivating |
| StudyLock | Purple (#A855F7) | Indigo (#6366F1) | Focused, clean |
| PromptVault | Blue (#3B82F6) | Cyan (#06B6D4) | Tech-forward, modern |
| DailyAnchor | Terracotta (#C88B54) | Sage (#6B8E6B) | Warm, grounding |
| FemFit | Pink (#EC4899) | Coral (#F43F5E) | Empowering, vibrant |
| DailyDevotion | Teal (#14B8A6) | Gold (#D4A418) | Serene, natural |

## Dark Mode Considerations

1. **Contrast ratios**: Ensure 4.5:1 minimum for text
2. **Shadows**: Use darker, more opaque shadows in dark mode
3. **Brand colors**: Shift to lighter variants (400 vs 600)
4. **Backgrounds**: Layer with subtle differences (not pure black)
5. **Images**: Consider providing dark mode variants

## CSS Variables

Generate CSS variables from theme:

```ts
import { createCSSVariables, cssVariablesToString } from '@/shared/theming';

const variables = createCSSVariables(theme);
const cssString = cssVariablesToString(variables);

// Use in global styles
// --color-background-primary: #FFFFFF;
// --spacing-4: 1rem;
// etc.
```

## Best Practices

1. **Use semantic tokens**: Prefer `theme.colors.text.primary` over `colors.gray[900]`

2. **Use the hooks**: Don't import theme objects directly in components

3. **Consider both modes**: Test all UI in both light and dark modes

4. **Respect system preference**: Default to `system` mode

5. **Prevent flash**: Always include `<ThemeScript />` in head

6. **Type safety**: Use TypeScript's autocomplete for theme paths

7. **Consistent spacing**: Use spacing tokens, not arbitrary values

8. **Semantic elevation**: Use `elevation.raised` not `shadows.sm`

## Troubleshooting

### Flash of wrong theme

Ensure `<ThemeScript />` is in `<head>` before stylesheets.

### Hydration mismatch

Add `suppressHydrationWarning` to `<html>` element.

### Theme not updating

Make sure component is a client component (`'use client'`).

### TypeScript errors

Import types explicitly:

```ts
import type { Theme, ThemeMode } from '@/shared/theming';
```
