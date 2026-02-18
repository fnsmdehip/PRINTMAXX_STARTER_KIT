/**
 * PrayerLock Theme
 * Calm blues with gold accents
 * For faith-focused meditation and prayer app
 */

import { colors } from '../tokens/colors';
import { lightTheme } from '../themes/light';
import { darkTheme } from '../themes/dark';
import type { Theme } from '../themes';

// Brand colors
const brandColors = {
  // Calm, peaceful blues
  primary: {
    50: '#EBF5FF',
    100: '#D6EBFF',
    200: '#ADd6FF',
    300: '#85C1FF',
    400: '#5CACFF',
    500: '#3B8DD9', // Main brand blue
    600: '#2E6FAD',
    700: '#225182',
    800: '#163456',
    900: '#0A1A2B',
  },
  // Sacred gold accents
  accent: {
    50: '#FFFBEB',
    100: '#FEF3C7',
    200: '#FDE68A',
    300: '#FCD34D',
    400: '#FBBF24',
    500: '#D4A418', // Regal gold
    600: '#B38B14',
    700: '#8A6B0F',
    800: '#614C0B',
    900: '#3D2F07',
  },
};

// Custom shadows with brand color tint
const brandShadows = {
  glow: '0 0 20px rgba(59, 141, 217, 0.3)',
  goldGlow: '0 0 15px rgba(212, 164, 24, 0.4)',
};

export const prayerlockLightTheme: Theme = {
  ...lightTheme,

  colors: {
    ...lightTheme.colors,

    // Background with subtle warmth
    background: {
      primary: '#FEFEFE',
      secondary: '#F8FAFC',
      tertiary: '#F1F5F9',
      inverse: brandColors.primary[900],
      elevated: '#FFFFFF',
      sunken: '#F1F5F9',
    },

    // Brand interactive colors
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

    // Text with brand tint
    text: {
      primary: brandColors.primary[900],
      secondary: brandColors.primary[700],
      tertiary: brandColors.primary[600],
      muted: brandColors.primary[400],
      inverse: '#FFFFFF',
      link: brandColors.primary[600],
      linkHover: brandColors.primary[700],
    },

    // Brand accent
    accent: {
      primary: brandColors.accent[500],
      secondary: brandColors.accent[100],
      text: brandColors.accent[700],
    },

    // Focus with brand color
    focus: {
      ring: brandColors.primary[500],
      ringOffset: '#FFFFFF',
    },
  },
};

export const prayerlockDarkTheme: Theme = {
  ...darkTheme,

  colors: {
    ...darkTheme.colors,

    // Deep, contemplative backgrounds
    background: {
      primary: '#0A1628',
      secondary: '#0F1E33',
      tertiary: '#14263F',
      inverse: brandColors.primary[50],
      elevated: '#14263F',
      sunken: '#050C14',
    },

    surface: {
      primary: '#0F1E33',
      secondary: '#14263F',
      tertiary: '#1A2F4D',
      inverse: colors.gray[100],
      overlay: 'rgba(10, 22, 40, 0.85)',
    },

    // Brand interactive colors for dark
    interactive: {
      primary: brandColors.primary[400],
      primaryHover: brandColors.primary[300],
      primaryActive: brandColors.primary[200],
      primaryDisabled: brandColors.primary[700],

      secondary: brandColors.primary[800],
      secondaryHover: brandColors.primary[700],
      secondaryActive: brandColors.primary[600],
      secondaryDisabled: brandColors.primary[900],

      ghost: 'transparent',
      ghostHover: brandColors.primary[800],
      ghostActive: brandColors.primary[700],
    },

    // Text for dark mode
    text: {
      primary: '#F8FAFC',
      secondary: brandColors.primary[200],
      tertiary: brandColors.primary[300],
      muted: brandColors.primary[500],
      inverse: brandColors.primary[900],
      link: brandColors.primary[300],
      linkHover: brandColors.primary[200],
    },

    // Gold accent stands out on dark
    accent: {
      primary: brandColors.accent[400],
      secondary: brandColors.accent[900],
      text: brandColors.accent[300],
    },

    focus: {
      ring: brandColors.primary[400],
      ringOffset: '#0A1628',
    },
  },
};

// Export brand assets
export const prayerlockBrand = {
  name: 'PrayerLock',
  tagline: 'Center your day in faith',
  colors: brandColors,
  shadows: brandShadows,
  fonts: {
    heading: 'Georgia, serif',
    body: '-apple-system, BlinkMacSystemFont, sans-serif',
  },
  gradients: {
    primary: `linear-gradient(135deg, ${brandColors.primary[500]} 0%, ${brandColors.primary[700]} 100%)`,
    accent: `linear-gradient(135deg, ${brandColors.accent[400]} 0%, ${brandColors.accent[600]} 100%)`,
    subtle: `linear-gradient(180deg, ${brandColors.primary[50]} 0%, #FFFFFF 100%)`,
    darkOverlay: `linear-gradient(180deg, transparent 0%, rgba(10, 22, 40, 0.9) 100%)`,
  },
};
