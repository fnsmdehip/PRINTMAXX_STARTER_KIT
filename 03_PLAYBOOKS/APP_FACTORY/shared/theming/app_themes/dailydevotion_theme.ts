/**
 * DailyDevotion Theme
 * Serene, natural colors
 * For daily devotional and spiritual reading app
 */

import { colors } from '../tokens/colors';
import { lightTheme } from '../themes/light';
import { darkTheme } from '../themes/dark';
import type { Theme } from '../themes';

// Brand colors
const brandColors = {
  // Serene teal/green-blue
  primary: {
    50: '#F0FDFA',
    100: '#CCFBF1',
    200: '#99F6E4',
    300: '#5EEAD4',
    400: '#2DD4BF',
    500: '#14B8A6', // Main brand teal
    600: '#0D9488',
    700: '#0F766E',
    800: '#115E59',
    900: '#134E4A',
  },
  // Warm gold for highlights
  gold: {
    50: '#FFFBEB',
    100: '#FEF3C7',
    200: '#FDE68A',
    300: '#FCD34D',
    400: '#FBBF24',
    500: '#D4A418', // Sacred gold
    600: '#B38B14',
    700: '#8A6B0F',
  },
  // Soft sky for backgrounds
  sky: {
    50: '#F7FBFE',
    100: '#EEF6FC',
    200: '#DCE9F7',
    300: '#C5D9EF',
  },
  // Natural sage
  sage: {
    400: '#84A686',
    500: '#6B8E6B',
    600: '#567156',
  },
};

// Custom shadows
const brandShadows = {
  soft: '0 2px 12px rgba(15, 118, 110, 0.1)',
  glow: '0 0 20px rgba(20, 184, 166, 0.25)',
  goldGlow: '0 0 15px rgba(212, 164, 24, 0.3)',
  card: '0 4px 16px rgba(19, 78, 74, 0.08)',
};

export const dailydevotionLightTheme: Theme = {
  ...lightTheme,

  colors: {
    ...lightTheme.colors,

    // Peaceful, open backgrounds
    background: {
      primary: brandColors.sky[50],
      secondary: brandColors.sky[100],
      tertiary: brandColors.sky[200],
      inverse: brandColors.primary[900],
      elevated: '#FFFFFF',
      sunken: brandColors.sky[200],
    },

    surface: {
      primary: '#FFFFFF',
      secondary: brandColors.sky[100],
      tertiary: brandColors.sky[200],
      inverse: brandColors.primary[800],
      overlay: 'rgba(19, 78, 74, 0.4)',
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
      inverse: '#FFFFFF',
      link: brandColors.primary[600],
      linkHover: brandColors.primary[700],
    },

    border: {
      ...lightTheme.colors.border,
      primary: brandColors.primary[200],
      secondary: brandColors.primary[300],
    },

    accent: {
      primary: brandColors.gold[500],
      secondary: brandColors.gold[100],
      text: brandColors.gold[700],
    },

    focus: {
      ring: brandColors.primary[500],
      ringOffset: brandColors.sky[50],
    },
  },
};

export const dailydevotionDarkTheme: Theme = {
  ...darkTheme,

  colors: {
    ...darkTheme.colors,

    // Deep, contemplative backgrounds
    background: {
      primary: '#0A1614',
      secondary: '#0F1E1B',
      tertiary: '#142723',
      inverse: brandColors.primary[50],
      elevated: '#142723',
      sunken: '#050B09',
    },

    surface: {
      primary: '#0F1E1B',
      secondary: '#142723',
      tertiary: '#1A302B',
      inverse: brandColors.primary[100],
      overlay: 'rgba(10, 22, 20, 0.9)',
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
      ghostHover: 'rgba(20, 184, 166, 0.1)',
      ghostActive: 'rgba(20, 184, 166, 0.2)',
    },

    text: {
      primary: brandColors.primary[50],
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
      primary: brandColors.gold[400],
      secondary: brandColors.gold[900],
      text: brandColors.gold[300],
    },

    focus: {
      ring: brandColors.primary[400],
      ringOffset: '#0A1614',
    },
  },
};

// Export brand assets
export const dailydevotionBrand = {
  name: 'DailyDevotion',
  tagline: 'Nourish your spirit daily',
  colors: brandColors,
  shadows: brandShadows,
  fonts: {
    heading: 'Georgia, "Times New Roman", serif',
    body: 'Georgia, "Times New Roman", serif',
    verse: 'Georgia, "Times New Roman", serif',
  },
  gradients: {
    primary: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.primary[600]} 100%)`,
    gold: `linear-gradient(135deg, ${brandColors.gold[300]} 0%, ${brandColors.gold[500]} 100%)`,
    sky: `linear-gradient(180deg, ${brandColors.sky[50]} 0%, ${brandColors.sky[200]} 100%)`,
    serenity: `linear-gradient(135deg, ${brandColors.primary[200]} 0%, ${brandColors.sky[200]} 100%)`,
    sunrise: `linear-gradient(180deg, ${brandColors.gold[200]} 0%, ${brandColors.sky[100]} 50%, ${brandColors.primary[100]} 100%)`,
  },
  typography: {
    verse: {
      fontFamily: 'Georgia, serif',
      fontStyle: 'italic',
      lineHeight: 1.8,
    },
    scripture: {
      fontFamily: 'Georgia, serif',
      fontSize: '1.125rem',
      lineHeight: 1.75,
    },
    prayer: {
      fontFamily: 'Georgia, serif',
      fontStyle: 'italic',
      color: brandColors.primary[700],
    },
  },
  decorations: {
    divider: `
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, ${brandColors.gold[400]}, transparent);
    `,
    verseMark: `
      border-left: 3px solid ${brandColors.gold[400]};
      padding-left: 1rem;
    `,
  },
};
