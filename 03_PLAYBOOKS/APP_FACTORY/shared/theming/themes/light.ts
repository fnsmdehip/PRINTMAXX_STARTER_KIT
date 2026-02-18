/**
 * Light Theme
 * Color values and shadows for light mode
 */

import { colors } from '../tokens/colors';
import { shadows, elevation } from '../tokens/shadows';
import { baseTheme } from './base';

export const lightTheme = {
  ...baseTheme,

  mode: 'light' as const,

  colors: {
    // Backgrounds
    background: {
      primary: colors.white,
      secondary: colors.gray[50],
      tertiary: colors.gray[100],
      inverse: colors.gray[900],
      elevated: colors.white,
      sunken: colors.gray[100],
    },

    // Surfaces (cards, modals, etc.)
    surface: {
      primary: colors.white,
      secondary: colors.gray[50],
      tertiary: colors.gray[100],
      inverse: colors.gray[800],
      overlay: 'rgba(0, 0, 0, 0.5)',
    },

    // Text colors
    text: {
      primary: colors.gray[900],
      secondary: colors.gray[600],
      tertiary: colors.gray[500],
      muted: colors.gray[400],
      inverse: colors.white,
      link: colors.blue[600],
      linkHover: colors.blue[700],
    },

    // Border colors
    border: {
      primary: colors.gray[200],
      secondary: colors.gray[300],
      focus: colors.blue[500],
      error: colors.red[500],
      success: colors.green[500],
      warning: colors.yellow[500],
    },

    // Interactive states
    interactive: {
      // Primary action color
      primary: colors.blue[600],
      primaryHover: colors.blue[700],
      primaryActive: colors.blue[800],
      primaryDisabled: colors.blue[300],

      // Secondary action color
      secondary: colors.gray[100],
      secondaryHover: colors.gray[200],
      secondaryActive: colors.gray[300],
      secondaryDisabled: colors.gray[100],

      // Ghost/minimal style
      ghost: 'transparent',
      ghostHover: colors.gray[100],
      ghostActive: colors.gray[200],
    },

    // Semantic colors
    semantic: {
      success: colors.green[600],
      successLight: colors.green[50],
      successBorder: colors.green[200],

      error: colors.red[600],
      errorLight: colors.red[50],
      errorBorder: colors.red[200],

      warning: colors.yellow[600],
      warningLight: colors.yellow[50],
      warningBorder: colors.yellow[200],

      info: colors.blue[600],
      infoLight: colors.blue[50],
      infoBorder: colors.blue[200],
    },

    // Focus ring
    focus: {
      ring: colors.blue[500],
      ringOffset: colors.white,
    },

    // Input specific
    input: {
      background: colors.white,
      backgroundDisabled: colors.gray[100],
      border: colors.gray[300],
      borderHover: colors.gray[400],
      borderFocus: colors.blue[500],
      borderError: colors.red[500],
      placeholder: colors.gray[400],
    },

    // Brand accent (can be overridden by app themes)
    accent: {
      primary: colors.blue[600],
      secondary: colors.blue[100],
      text: colors.blue[700],
    },
  },

  // Shadows
  shadows,
  elevation,
} as const;

export type LightTheme = typeof lightTheme;
