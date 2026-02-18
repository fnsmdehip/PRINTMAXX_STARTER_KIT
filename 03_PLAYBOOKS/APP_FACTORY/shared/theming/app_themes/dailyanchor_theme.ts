/**
 * DailyAnchor Theme
 * Warm earth tones for grounding
 * For daily reflection and journaling app
 */

import { colors } from '../tokens/colors';
import { lightTheme } from '../themes/light';
import { darkTheme } from '../themes/dark';
import type { Theme } from '../themes';

// Brand colors
const brandColors = {
  // Warm, grounding browns
  primary: {
    50: '#FDF8F3',
    100: '#F9EDE2',
    200: '#F2D9C4',
    300: '#E8C19F',
    400: '#DBA577',
    500: '#C88B54', // Main brand color - warm terracotta
    600: '#B5734A',
    700: '#965D3E',
    800: '#7A4B33',
    900: '#5E3A28',
  },
  // Sage green for calm
  sage: {
    50: '#F4F7F4',
    100: '#E4ECE4',
    200: '#C9D9C9',
    300: '#A8C1A8',
    400: '#84A684',
    500: '#6B8E6B', // Calming sage
    600: '#567156',
    700: '#445844',
    800: '#364436',
    900: '#2A342A',
  },
  // Cream for backgrounds
  cream: {
    50: '#FFFEFB',
    100: '#FDF9F3',
    200: '#FAF4E8',
    300: '#F5EBDA',
  },
};

// Custom shadows with warmth
const brandShadows = {
  warm: '0 4px 20px rgba(200, 139, 84, 0.15)',
  soft: '0 2px 12px rgba(94, 58, 40, 0.1)',
  card: '0 4px 16px rgba(94, 58, 40, 0.08)',
};

export const dailyanchorLightTheme: Theme = {
  ...lightTheme,

  colors: {
    ...lightTheme.colors,

    // Warm, inviting backgrounds
    background: {
      primary: brandColors.cream[50],
      secondary: brandColors.cream[100],
      tertiary: brandColors.cream[200],
      inverse: brandColors.primary[900],
      elevated: '#FFFFFF',
      sunken: brandColors.cream[200],
    },

    surface: {
      primary: '#FFFFFF',
      secondary: brandColors.cream[100],
      tertiary: brandColors.cream[200],
      inverse: brandColors.primary[800],
      overlay: 'rgba(94, 58, 40, 0.4)',
    },

    interactive: {
      primary: brandColors.primary[500],
      primaryHover: brandColors.primary[600],
      primaryActive: brandColors.primary[700],
      primaryDisabled: brandColors.primary[300],

      secondary: brandColors.primary[50],
      secondaryHover: brandColors.primary[100],
      secondaryActive: brandColors.primary[200],
      secondaryDisabled: brandColors.primary[50],

      ghost: 'transparent',
      ghostHover: brandColors.primary[50],
      ghostActive: brandColors.primary[100],
    },

    text: {
      primary: brandColors.primary[900],
      secondary: brandColors.primary[700],
      tertiary: brandColors.primary[600],
      muted: brandColors.primary[400],
      inverse: brandColors.cream[50],
      link: brandColors.primary[600],
      linkHover: brandColors.primary[700],
    },

    border: {
      ...lightTheme.colors.border,
      primary: brandColors.primary[200],
      secondary: brandColors.primary[300],
    },

    accent: {
      primary: brandColors.sage[500],
      secondary: brandColors.sage[100],
      text: brandColors.sage[700],
    },

    semantic: {
      ...lightTheme.colors.semantic,
      success: brandColors.sage[500],
      successLight: brandColors.sage[50],
      successBorder: brandColors.sage[200],
    },

    focus: {
      ring: brandColors.primary[500],
      ringOffset: brandColors.cream[50],
    },
  },
};

export const dailyanchorDarkTheme: Theme = {
  ...darkTheme,

  colors: {
    ...darkTheme.colors,

    // Deep, cozy dark backgrounds
    background: {
      primary: '#1A1512',
      secondary: '#211B17',
      tertiary: '#2A231E',
      inverse: brandColors.cream[100],
      elevated: '#2A231E',
      sunken: '#110E0C',
    },

    surface: {
      primary: '#211B17',
      secondary: '#2A231E',
      tertiary: '#352D27',
      inverse: brandColors.cream[200],
      overlay: 'rgba(26, 21, 18, 0.9)',
    },

    interactive: {
      primary: brandColors.primary[400],
      primaryHover: brandColors.primary[300],
      primaryActive: brandColors.primary[200],
      primaryDisabled: brandColors.primary[700],

      secondary: brandColors.primary[900],
      secondaryHover: brandColors.primary[800],
      secondaryActive: brandColors.primary[700],
      secondaryDisabled: brandColors.primary[900],

      ghost: 'transparent',
      ghostHover: 'rgba(200, 139, 84, 0.1)',
      ghostActive: 'rgba(200, 139, 84, 0.2)',
    },

    text: {
      primary: brandColors.cream[100],
      secondary: brandColors.primary[200],
      tertiary: brandColors.primary[300],
      muted: brandColors.primary[500],
      inverse: brandColors.primary[900],
      link: brandColors.primary[400],
      linkHover: brandColors.primary[300],
    },

    border: {
      ...darkTheme.colors.border,
      primary: brandColors.primary[800],
      secondary: brandColors.primary[700],
    },

    accent: {
      primary: brandColors.sage[400],
      secondary: brandColors.sage[900],
      text: brandColors.sage[300],
    },

    semantic: {
      ...darkTheme.colors.semantic,
      success: brandColors.sage[400],
      successLight: brandColors.sage[900],
      successBorder: brandColors.sage[700],
    },

    focus: {
      ring: brandColors.primary[400],
      ringOffset: '#1A1512',
    },
  },
};

// Export brand assets
export const dailyanchorBrand = {
  name: 'DailyAnchor',
  tagline: 'Ground your day in purpose',
  colors: brandColors,
  shadows: brandShadows,
  fonts: {
    heading: 'Georgia, "Times New Roman", serif',
    body: '-apple-system, BlinkMacSystemFont, sans-serif',
  },
  gradients: {
    primary: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.primary[600]} 100%)`,
    sage: `linear-gradient(135deg, ${brandColors.sage[400]} 0%, ${brandColors.sage[600]} 100%)`,
    warmth: `linear-gradient(180deg, ${brandColors.cream[50]} 0%, ${brandColors.cream[200]} 100%)`,
    sunset: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.sage[400]} 100%)`,
    paper: `linear-gradient(180deg, ${brandColors.cream[100]} 0%, ${brandColors.cream[200]} 100%)`,
  },
  textures: {
    paper: `
      background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    `,
  },
};
