/**
 * Dark Theme
 * Color values and shadows for dark mode
 */

import { colors } from '../tokens/colors';
import { shadowsDark, elevationDark } from '../tokens/shadows';
import { baseTheme } from './base';

export const darkTheme = {
  ...baseTheme,

  mode: 'dark' as const,

  colors: {
    // Backgrounds
    background: {
      primary: colors.gray[950],
      secondary: colors.gray[900],
      tertiary: colors.gray[800],
      inverse: colors.gray[50],
      elevated: colors.gray[900],
      sunken: colors.black,
    },

    // Surfaces (cards, modals, etc.)
    surface: {
      primary: colors.gray[900],
      secondary: colors.gray[800],
      tertiary: colors.gray[700],
      inverse: colors.gray[100],
      overlay: 'rgba(0, 0, 0, 0.7)',
    },

    // Text colors
    text: {
      primary: colors.gray[50],
      secondary: colors.gray[300],
      tertiary: colors.gray[400],
      muted: colors.gray[500],
      inverse: colors.gray[900],
      link: colors.blue[400],
      linkHover: colors.blue[300],
    },

    // Border colors
    border: {
      primary: colors.gray[800],
      secondary: colors.gray[700],
      focus: colors.blue[500],
      error: colors.red[500],
      success: colors.green[500],
      warning: colors.yellow[500],
    },

    // Interactive states
    interactive: {
      // Primary action color
      primary: colors.blue[500],
      primaryHover: colors.blue[400],
      primaryActive: colors.blue[300],
      primaryDisabled: colors.blue[800],

      // Secondary action color
      secondary: colors.gray[800],
      secondaryHover: colors.gray[700],
      secondaryActive: colors.gray[600],
      secondaryDisabled: colors.gray[800],

      // Ghost/minimal style
      ghost: 'transparent',
      ghostHover: colors.gray[800],
      ghostActive: colors.gray[700],
    },

    // Semantic colors
    semantic: {
      success: colors.green[500],
      successLight: colors.green[950],
      successBorder: colors.green[800],

      error: colors.red[500],
      errorLight: colors.red[950],
      errorBorder: colors.red[800],

      warning: colors.yellow[500],
      warningLight: colors.yellow[950],
      warningBorder: colors.yellow[800],

      info: colors.blue[500],
      infoLight: colors.blue[950],
      infoBorder: colors.blue[800],
    },

    // Focus ring
    focus: {
      ring: colors.blue[500],
      ringOffset: colors.gray[950],
    },

    // Input specific
    input: {
      background: colors.gray[800],
      backgroundDisabled: colors.gray[900],
      border: colors.gray[700],
      borderHover: colors.gray[600],
      borderFocus: colors.blue[500],
      borderError: colors.red[500],
      placeholder: colors.gray[500],
    },

    // Brand accent (can be overridden by app themes)
    accent: {
      primary: colors.blue[500],
      secondary: colors.blue[900],
      text: colors.blue[300],
    },
  },

  // Shadows (darker for dark mode)
  shadows: shadowsDark,
  elevation: elevationDark,
} as const;

export type DarkTheme = typeof darkTheme;
