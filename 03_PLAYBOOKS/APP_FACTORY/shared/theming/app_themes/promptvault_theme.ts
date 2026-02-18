/**
 * PromptVault Theme
 * Tech blues with gradient accents
 * For AI prompt management app
 */

import { colors } from '../tokens/colors';
import { lightTheme } from '../themes/light';
import { darkTheme } from '../themes/dark';
import type { Theme } from '../themes';

// Brand colors
const brandColors = {
  // Tech-forward blues
  primary: {
    50: '#EFF6FF',
    100: '#DBEAFE',
    200: '#BFDBFE',
    300: '#93C5FD',
    400: '#60A5FA',
    500: '#3B82F6', // Main brand blue
    600: '#2563EB',
    700: '#1D4ED8',
    800: '#1E40AF',
    900: '#1E3A8A',
  },
  // Cyan for highlights
  cyan: {
    300: '#67E8F9',
    400: '#22D3EE',
    500: '#06B6D4',
    600: '#0891B2',
  },
  // Electric violet for accents
  violet: {
    400: '#A78BFA',
    500: '#8B5CF6',
    600: '#7C3AED',
  },
};

// Custom shadows with tech feel
const brandShadows = {
  glow: '0 0 20px rgba(59, 130, 246, 0.4)',
  cyanGlow: '0 0 15px rgba(6, 182, 212, 0.4)',
  neon: '0 0 30px rgba(139, 92, 246, 0.3)',
  card: '0 4px 24px rgba(30, 64, 175, 0.15)',
};

export const promptvaultLightTheme: Theme = {
  ...lightTheme,

  colors: {
    ...lightTheme.colors,

    // Clean, modern backgrounds
    background: {
      primary: '#FFFFFF',
      secondary: '#F8FAFC',
      tertiary: '#F1F5F9',
      inverse: brandColors.primary[900],
      elevated: '#FFFFFF',
      sunken: '#F1F5F9',
    },

    surface: {
      primary: '#FFFFFF',
      secondary: '#F8FAFC',
      tertiary: '#F1F5F9',
      inverse: brandColors.primary[800],
      overlay: 'rgba(30, 64, 175, 0.4)',
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

    border: {
      ...lightTheme.colors.border,
      primary: colors.gray[200],
      focus: brandColors.primary[500],
    },

    accent: {
      primary: brandColors.cyan[500],
      secondary: brandColors.cyan[300],
      text: brandColors.cyan[600],
    },

    focus: {
      ring: brandColors.primary[500],
      ringOffset: '#FFFFFF',
    },
  },
};

export const promptvaultDarkTheme: Theme = {
  ...darkTheme,

  colors: {
    ...darkTheme.colors,

    // Deep tech backgrounds
    background: {
      primary: '#0B1120',
      secondary: '#0F172A',
      tertiary: '#1E293B',
      inverse: brandColors.primary[50],
      elevated: '#1E293B',
      sunken: '#020617',
    },

    surface: {
      primary: '#0F172A',
      secondary: '#1E293B',
      tertiary: '#334155',
      inverse: colors.gray[100],
      overlay: 'rgba(11, 17, 32, 0.9)',
    },

    interactive: {
      primary: brandColors.primary[400],
      primaryHover: brandColors.primary[300],
      primaryActive: brandColors.primary[200],
      primaryDisabled: brandColors.primary[700],

      secondary: brandColors.primary[900],
      secondaryHover: brandColors.primary[800],
      secondaryActive: brandColors.primary[700],
      secondaryDisabled: brandColors.primary[950],

      ghost: 'transparent',
      ghostHover: 'rgba(59, 130, 246, 0.1)',
      ghostActive: 'rgba(59, 130, 246, 0.2)',
    },

    text: {
      primary: '#F8FAFC',
      secondary: colors.gray[300],
      tertiary: colors.gray[400],
      muted: colors.gray[500],
      inverse: colors.gray[900],
      link: brandColors.primary[400],
      linkHover: brandColors.primary[300],
    },

    border: {
      ...darkTheme.colors.border,
      primary: colors.gray[700],
      focus: brandColors.primary[400],
    },

    accent: {
      primary: brandColors.cyan[400],
      secondary: brandColors.cyan[900],
      text: brandColors.cyan[300],
    },

    focus: {
      ring: brandColors.primary[400],
      ringOffset: '#0B1120',
    },
  },
};

// Export brand assets
export const promptvaultBrand = {
  name: 'PromptVault',
  tagline: 'Your AI prompt library',
  colors: brandColors,
  shadows: brandShadows,
  fonts: {
    heading: '-apple-system, BlinkMacSystemFont, sans-serif',
    body: '-apple-system, BlinkMacSystemFont, sans-serif',
    mono: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace',
  },
  gradients: {
    primary: `linear-gradient(135deg, ${brandColors.primary[500]} 0%, ${brandColors.primary[700]} 100%)`,
    tech: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.violet[500]} 100%)`,
    cyan: `linear-gradient(135deg, ${brandColors.cyan[400]} 0%, ${brandColors.cyan[600]} 100%)`,
    header: `linear-gradient(90deg, ${brandColors.primary[600]} 0%, ${brandColors.violet[600]} 100%)`,
    card: `linear-gradient(180deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%)`,
    codeBlock: `linear-gradient(180deg, #1E293B 0%, #0F172A 100%)`,
  },
  effects: {
    glassMorphism: `
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
    `,
    codeHighlight: `
      background: linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.1) 50%, transparent 100%);
    `,
  },
};
