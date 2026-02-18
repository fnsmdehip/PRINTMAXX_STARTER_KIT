/**
 * FemFit Theme
 * Empowering pinks and corals
 * For women's fitness and wellness app
 */

import { colors } from '../tokens/colors';
import { lightTheme } from '../themes/light';
import { darkTheme } from '../themes/dark';
import type { Theme } from '../themes';

// Brand colors
const brandColors = {
  // Vibrant, empowering pink
  primary: {
    50: '#FDF2F8',
    100: '#FCE7F3',
    200: '#FBCFE8',
    300: '#F9A8D4',
    400: '#F472B6',
    500: '#EC4899', // Main brand pink
    600: '#DB2777',
    700: '#BE185D',
    800: '#9D174D',
    900: '#831843',
  },
  // Coral for energy
  coral: {
    50: '#FFF5F5',
    100: '#FFE8E8',
    200: '#FECDD3',
    300: '#FDA4AF',
    400: '#FB7185',
    500: '#F43F5E', // Energizing coral
    600: '#E11D48',
    700: '#BE123C',
    800: '#9F1239',
    900: '#881337',
  },
  // Soft purple for balance
  purple: {
    300: '#D8B4FE',
    400: '#C084FC',
    500: '#A855F7',
    600: '#9333EA',
  },
  // Rose gold accents
  roseGold: {
    light: '#F4D4D4',
    main: '#E8B4B8',
    dark: '#D4919A',
  },
};

// Custom shadows
const brandShadows = {
  glow: '0 0 20px rgba(236, 72, 153, 0.3)',
  coralGlow: '0 0 15px rgba(244, 63, 94, 0.3)',
  soft: '0 4px 20px rgba(157, 23, 77, 0.1)',
  card: '0 4px 16px rgba(236, 72, 153, 0.1)',
};

export const femfitLightTheme: Theme = {
  ...lightTheme,

  colors: {
    ...lightTheme.colors,

    // Soft, feminine backgrounds
    background: {
      primary: '#FFFBFC',
      secondary: '#FDF2F8',
      tertiary: '#FCE7F3',
      inverse: brandColors.primary[900],
      elevated: '#FFFFFF',
      sunken: '#FCE7F3',
    },

    surface: {
      primary: '#FFFFFF',
      secondary: '#FDF2F8',
      tertiary: '#FCE7F3',
      inverse: brandColors.primary[800],
      overlay: 'rgba(157, 23, 77, 0.4)',
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
      primary: brandColors.coral[500],
      secondary: brandColors.coral[100],
      text: brandColors.coral[700],
    },

    semantic: {
      ...lightTheme.colors.semantic,
      success: colors.green[500],
      successLight: colors.green[50],
      successBorder: colors.green[200],
    },

    focus: {
      ring: brandColors.primary[500],
      ringOffset: '#FFFBFC',
    },
  },
};

export const femfitDarkTheme: Theme = {
  ...darkTheme,

  colors: {
    ...darkTheme.colors,

    // Deep, luxurious dark backgrounds
    background: {
      primary: '#1A0F14',
      secondary: '#21131A',
      tertiary: '#2A1922',
      inverse: brandColors.primary[50],
      elevated: '#2A1922',
      sunken: '#10080B',
    },

    surface: {
      primary: '#21131A',
      secondary: '#2A1922',
      tertiary: '#34202A',
      inverse: brandColors.primary[100],
      overlay: 'rgba(26, 15, 20, 0.9)',
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
      ghostHover: 'rgba(236, 72, 153, 0.1)',
      ghostActive: 'rgba(236, 72, 153, 0.2)',
    },

    text: {
      primary: '#FDF2F8',
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
      primary: brandColors.coral[400],
      secondary: brandColors.coral[900],
      text: brandColors.coral[300],
    },

    semantic: {
      ...darkTheme.colors.semantic,
      success: colors.green[400],
      successLight: colors.green[950],
      successBorder: colors.green[800],
    },

    focus: {
      ring: brandColors.primary[400],
      ringOffset: '#1A0F14',
    },
  },
};

// Export brand assets
export const femfitBrand = {
  name: 'FemFit',
  tagline: 'Strong is beautiful',
  colors: brandColors,
  shadows: brandShadows,
  fonts: {
    heading: '-apple-system, BlinkMacSystemFont, sans-serif',
    body: '-apple-system, BlinkMacSystemFont, sans-serif',
  },
  gradients: {
    primary: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.primary[600]} 100%)`,
    coral: `linear-gradient(135deg, ${brandColors.coral[400]} 0%, ${brandColors.coral[600]} 100%)`,
    energy: `linear-gradient(135deg, ${brandColors.coral[400]} 0%, ${brandColors.primary[500]} 100%)`,
    empowerment: `linear-gradient(135deg, ${brandColors.primary[400]} 0%, ${brandColors.purple[500]} 100%)`,
    roseGold: `linear-gradient(135deg, ${brandColors.roseGold.light} 0%, ${brandColors.roseGold.main} 100%)`,
    progress: `linear-gradient(90deg, ${brandColors.primary[400]} 0%, ${brandColors.coral[500]} 100%)`,
  },
  animations: {
    pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    heartbeat: `
      @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.1); }
        50% { transform: scale(1); }
        75% { transform: scale(1.05); }
      }
    `,
  },
};
