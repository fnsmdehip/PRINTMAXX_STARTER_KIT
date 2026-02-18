/**
 * StudyLock Theme
 * Focused purples with clean aesthetics
 * For study and focus timer app
 */

import { colors } from '../tokens/colors';
import { lightTheme } from '../themes/light';
import { darkTheme } from '../themes/dark';
import type { Theme } from '../themes';

// Brand colors
const brandColors = {
  // Deep, focused purples
  primary: {
    50: '#FAF5FF',
    100: '#F3E8FF',
    200: '#E9D5FF',
    300: '#D8B4FE',
    400: '#C084FC',
    500: '#A855F7', // Main brand purple
    600: '#9333EA',
    700: '#7E22CE',
    800: '#6B21A8',
    900: '#581C87',
  },
  // Clean indigo for secondary
  secondary: {
    50: '#EEF2FF',
    100: '#E0E7FF',
    200: '#C7D2FE',
    300: '#A5B4FC',
    400: '#818CF8',
    500: '#6366F1',
    600: '#4F46E5',
    700: '#4338CA',
  },
  // Success green for completed tasks
  success: {
    400: '#4ADE80',
    500: '#22C55E',
    600: '#16A34A',
  },
};

// Custom shadows
const brandShadows = {
  glow: '0 0 20px rgba(168, 85, 247, 0.3)',
  focus: '0 0 0 3px rgba(168, 85, 247, 0.2)',
  soft: '0 4px 20px rgba(168, 85, 247, 0.15)',
};

export const studylockLightTheme: Theme = {
  ...lightTheme,

  colors: {
    ...lightTheme.colors,

    // Clean, minimal backgrounds
    background: {
      primary: '#FFFFFF',
      secondary: '#FAFAFA',
      tertiary: '#F5F5F5',
      inverse: brandColors.primary[900],
      elevated: '#FFFFFF',
      sunken: '#F5F5F5',
    },

    surface: {
      primary: '#FFFFFF',
      secondary: '#FAFAFA',
      tertiary: '#F5F5F5',
      inverse: brandColors.primary[800],
      overlay: 'rgba(88, 28, 135, 0.4)',
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
      primary: colors.gray[900],
      secondary: colors.gray[600],
      tertiary: colors.gray[500],
      muted: colors.gray[400],
      inverse: '#FFFFFF',
      link: brandColors.primary[600],
      linkHover: brandColors.primary[700],
    },

    accent: {
      primary: brandColors.secondary[500],
      secondary: brandColors.secondary[100],
      text: brandColors.secondary[700],
    },

    semantic: {
      ...lightTheme.colors.semantic,
      success: brandColors.success[500],
      successLight: '#F0FDF4',
      successBorder: '#BBF7D0',
    },

    focus: {
      ring: brandColors.primary[500],
      ringOffset: '#FFFFFF',
    },
  },
};

export const studylockDarkTheme: Theme = {
  ...darkTheme,

  colors: {
    ...darkTheme.colors,

    // Deep, focused dark backgrounds
    background: {
      primary: '#0F0A15',
      secondary: '#16101F',
      tertiary: '#1D1529',
      inverse: brandColors.primary[50],
      elevated: '#1D1529',
      sunken: '#080510',
    },

    surface: {
      primary: '#16101F',
      secondary: '#1D1529',
      tertiary: '#241A33',
      inverse: colors.gray[100],
      overlay: 'rgba(15, 10, 21, 0.9)',
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
      ghostHover: 'rgba(168, 85, 247, 0.1)',
      ghostActive: 'rgba(168, 85, 247, 0.2)',
    },

    text: {
      primary: '#FAFAFA',
      secondary: brandColors.primary[200],
      tertiary: brandColors.primary[300],
      muted: brandColors.primary[500],
      inverse: brandColors.primary[900],
      link: brandColors.primary[400],
      linkHover: brandColors.primary[300],
    },

    accent: {
      primary: brandColors.secondary[400],
      secondary: brandColors.secondary[900],
      text: brandColors.secondary[300],
    },

    semantic: {
      ...darkTheme.colors.semantic,
      success: brandColors.success[400],
      successLight: '#052E16',
      successBorder: '#166534',
    },

    focus: {
      ring: brandColors.primary[400],
      ringOffset: '#0F0A15',
    },
  },
};

// Export brand assets
export const studylockBrand = {
  name: 'StudyLock',
  tagline: 'Focus. Learn. Achieve.',
  colors: brandColors,
  shadows: brandShadows,
  fonts: {
    heading: '-apple-system, BlinkMacSystemFont, sans-serif',
    body: '-apple-system, BlinkMacSystemFont, sans-serif',
    mono: 'ui-monospace, SFMono-Regular, Menlo, monospace',
  },
  gradients: {
    primary: `linear-gradient(135deg, ${brandColors.primary[500]} 0%, ${brandColors.primary[700]} 100%)`,
    secondary: `linear-gradient(135deg, ${brandColors.secondary[500]} 0%, ${brandColors.secondary[700]} 100%)`,
    focus: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.secondary[500]} 100%)`,
    timer: `conic-gradient(${brandColors.primary[500]} var(--progress, 0%), ${colors.gray[200]} 0%)`,
  },
  effects: {
    focusRing: `0 0 0 2px #FFFFFF, 0 0 0 4px ${brandColors.primary[500]}`,
    glassEffect: 'backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.1);',
  },
};
