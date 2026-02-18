/**
 * WalkToUnlock Theme
 * Energetic greens with orange accents
 * For fitness and step-tracking app
 */

import { colors } from '../tokens/colors';
import { lightTheme } from '../themes/light';
import { darkTheme } from '../themes/dark';
import type { Theme } from '../themes';

// Brand colors
const brandColors = {
  // Vibrant, energetic greens
  primary: {
    50: '#ECFDF5',
    100: '#D1FAE5',
    200: '#A7F3D0',
    300: '#6EE7B7',
    400: '#34D399',
    500: '#10B981', // Main brand green
    600: '#059669',
    700: '#047857',
    800: '#065F46',
    900: '#064E3B',
  },
  // Energizing orange accents
  accent: {
    50: '#FFF7ED',
    100: '#FFEDD5',
    200: '#FED7AA',
    300: '#FDBA74',
    400: '#FB923C',
    500: '#F97316', // Motivating orange
    600: '#EA580C',
    700: '#C2410C',
    800: '#9A3412',
    900: '#7C2D12',
  },
  // Achievement gold
  achievement: {
    400: '#FBBF24',
    500: '#F59E0B',
    600: '#D97706',
  },
};

// Custom shadows
const brandShadows = {
  glow: '0 0 20px rgba(16, 185, 129, 0.4)',
  orangeGlow: '0 0 15px rgba(249, 115, 22, 0.4)',
  achievementGlow: '0 0 25px rgba(245, 158, 11, 0.5)',
};

export const walktounlockLightTheme: Theme = {
  ...lightTheme,

  colors: {
    ...lightTheme.colors,

    // Fresh, clean backgrounds
    background: {
      primary: '#FFFFFF',
      secondary: '#F0FDF4',
      tertiary: '#ECFDF5',
      inverse: brandColors.primary[900],
      elevated: '#FFFFFF',
      sunken: '#ECFDF5',
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

    // Text
    text: {
      primary: colors.gray[900],
      secondary: colors.gray[700],
      tertiary: colors.gray[600],
      muted: colors.gray[400],
      inverse: '#FFFFFF',
      link: brandColors.primary[600],
      linkHover: brandColors.primary[700],
    },

    // Orange accent
    accent: {
      primary: brandColors.accent[500],
      secondary: brandColors.accent[100],
      text: brandColors.accent[700],
    },

    // Semantic overrides
    semantic: {
      ...lightTheme.colors.semantic,
      success: brandColors.primary[500],
      successLight: brandColors.primary[50],
      successBorder: brandColors.primary[200],
    },

    focus: {
      ring: brandColors.primary[500],
      ringOffset: '#FFFFFF',
    },
  },
};

export const walktounlockDarkTheme: Theme = {
  ...darkTheme,

  colors: {
    ...darkTheme.colors,

    // Dark with green tint
    background: {
      primary: '#0D1912',
      secondary: '#121F18',
      tertiary: '#17261E',
      inverse: brandColors.primary[50],
      elevated: '#17261E',
      sunken: '#080F0B',
    },

    surface: {
      primary: '#121F18',
      secondary: '#17261E',
      tertiary: '#1D2E24',
      inverse: colors.gray[100],
      overlay: 'rgba(13, 25, 18, 0.85)',
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
      ghostHover: brandColors.primary[900],
      ghostActive: brandColors.primary[800],
    },

    text: {
      primary: '#F0FDF4',
      secondary: brandColors.primary[200],
      tertiary: brandColors.primary[300],
      muted: brandColors.primary[500],
      inverse: brandColors.primary[900],
      link: brandColors.primary[400],
      linkHover: brandColors.primary[300],
    },

    accent: {
      primary: brandColors.accent[400],
      secondary: brandColors.accent[900],
      text: brandColors.accent[300],
    },

    semantic: {
      ...darkTheme.colors.semantic,
      success: brandColors.primary[400],
      successLight: brandColors.primary[900],
      successBorder: brandColors.primary[700],
    },

    focus: {
      ring: brandColors.primary[400],
      ringOffset: '#0D1912',
    },
  },
};

// Export brand assets
export const walktounlockBrand = {
  name: 'WalkToUnlock',
  tagline: 'Every step counts',
  colors: brandColors,
  shadows: brandShadows,
  fonts: {
    heading: '-apple-system, BlinkMacSystemFont, sans-serif',
    body: '-apple-system, BlinkMacSystemFont, sans-serif',
  },
  gradients: {
    primary: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.primary[600]} 100%)`,
    accent: `linear-gradient(135deg, ${brandColors.accent[400]} 0%, ${brandColors.accent[600]} 100%)`,
    energy: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.accent[500]} 100%)`,
    achievement: `linear-gradient(135deg, ${brandColors.achievement[400]} 0%, ${brandColors.achievement[600]} 100%)`,
    progress: `linear-gradient(90deg, ${brandColors.primary[500]} 0%, ${brandColors.accent[500]} 100%)`,
  },
  animations: {
    pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    bounce: 'bounce 1s infinite',
  },
};
