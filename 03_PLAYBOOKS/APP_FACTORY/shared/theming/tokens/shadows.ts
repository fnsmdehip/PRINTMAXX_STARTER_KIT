/**
 * Shadow Tokens
 * Box shadows and elevation system
 */

export const shadows = {
  none: 'none',

  // Subtle shadows for cards and surfaces
  xs: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  sm: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',

  // Inner shadow
  inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
} as const;

// Dark mode shadows (need more opacity)
export const shadowsDark = {
  none: 'none',
  xs: '0 1px 2px 0 rgb(0 0 0 / 0.2)',
  sm: '0 1px 3px 0 rgb(0 0 0 / 0.3), 0 1px 2px -1px rgb(0 0 0 / 0.2)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.3), 0 2px 4px -2px rgb(0 0 0 / 0.2)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.2)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.4), 0 8px 10px -6px rgb(0 0 0 / 0.3)',
  '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.5)',
  inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.2)',
} as const;

// Colored shadows for buttons and interactive elements
export const coloredShadows = {
  blue: {
    sm: '0 1px 3px 0 rgb(59 130 246 / 0.3), 0 1px 2px -1px rgb(59 130 246 / 0.2)',
    md: '0 4px 6px -1px rgb(59 130 246 / 0.3), 0 2px 4px -2px rgb(59 130 246 / 0.2)',
    lg: '0 10px 15px -3px rgb(59 130 246 / 0.3), 0 4px 6px -4px rgb(59 130 246 / 0.2)',
  },
  green: {
    sm: '0 1px 3px 0 rgb(34 197 94 / 0.3), 0 1px 2px -1px rgb(34 197 94 / 0.2)',
    md: '0 4px 6px -1px rgb(34 197 94 / 0.3), 0 2px 4px -2px rgb(34 197 94 / 0.2)',
    lg: '0 10px 15px -3px rgb(34 197 94 / 0.3), 0 4px 6px -4px rgb(34 197 94 / 0.2)',
  },
  purple: {
    sm: '0 1px 3px 0 rgb(168 85 247 / 0.3), 0 1px 2px -1px rgb(168 85 247 / 0.2)',
    md: '0 4px 6px -1px rgb(168 85 247 / 0.3), 0 2px 4px -2px rgb(168 85 247 / 0.2)',
    lg: '0 10px 15px -3px rgb(168 85 247 / 0.3), 0 4px 6px -4px rgb(168 85 247 / 0.2)',
  },
  pink: {
    sm: '0 1px 3px 0 rgb(236 72 153 / 0.3), 0 1px 2px -1px rgb(236 72 153 / 0.2)',
    md: '0 4px 6px -1px rgb(236 72 153 / 0.3), 0 2px 4px -2px rgb(236 72 153 / 0.2)',
    lg: '0 10px 15px -3px rgb(236 72 153 / 0.3), 0 4px 6px -4px rgb(236 72 153 / 0.2)',
  },
  gold: {
    sm: '0 1px 3px 0 rgb(245 158 11 / 0.3), 0 1px 2px -1px rgb(245 158 11 / 0.2)',
    md: '0 4px 6px -1px rgb(245 158 11 / 0.3), 0 2px 4px -2px rgb(245 158 11 / 0.2)',
    lg: '0 10px 15px -3px rgb(245 158 11 / 0.3), 0 4px 6px -4px rgb(245 158 11 / 0.2)',
  },
} as const;

// Elevation levels (semantic naming)
export const elevation = {
  // Surface level (base)
  surface: shadows.none,

  // Raised surfaces (cards, tiles)
  raised: shadows.sm,

  // Floating elements (dropdowns, popovers)
  floating: shadows.md,

  // Overlays (modals, dialogs)
  overlay: shadows.lg,

  // Highest elevation (toasts, tooltips)
  highest: shadows.xl,
} as const;

export const elevationDark = {
  surface: shadowsDark.none,
  raised: shadowsDark.sm,
  floating: shadowsDark.md,
  overlay: shadowsDark.lg,
  highest: shadowsDark.xl,
} as const;

export type Shadow = keyof typeof shadows;
export type Elevation = keyof typeof elevation;
