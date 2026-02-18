/**
 * Base Theme
 * Shared values across all themes (light and dark)
 * These values don't change based on color mode
 */

import {
  fontFamilies,
  fontSizes,
  fontWeights,
  lineHeights,
  letterSpacings,
  textStyles,
} from '../tokens/typography';
import { spacing, semanticSpacing } from '../tokens/spacing';
import { radii, componentRadii } from '../tokens/radii';

export const baseTheme = {
  // Typography
  fonts: fontFamilies,
  fontSizes,
  fontWeights,
  lineHeights,
  letterSpacings,
  textStyles,

  // Spacing
  spacing,
  semanticSpacing,

  // Border radius
  radii,
  componentRadii,

  // Breakpoints
  breakpoints: {
    xs: '0px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },

  // Z-index scale
  zIndices: {
    hide: -1,
    auto: 'auto',
    base: 0,
    docked: 10,
    dropdown: 1000,
    sticky: 1100,
    banner: 1200,
    overlay: 1300,
    modal: 1400,
    popover: 1500,
    skipLink: 1600,
    toast: 1700,
    tooltip: 1800,
  },

  // Transitions
  transitions: {
    // Durations
    durations: {
      instant: '0ms',
      fast: '100ms',
      normal: '200ms',
      slow: '300ms',
      slower: '400ms',
      slowest: '500ms',
    },
    // Timing functions
    easings: {
      linear: 'linear',
      ease: 'ease',
      easeIn: 'ease-in',
      easeOut: 'ease-out',
      easeInOut: 'ease-in-out',
      // Custom easings
      smooth: 'cubic-bezier(0.4, 0, 0.2, 1)',
      bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
      spring: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
    },
    // Preset transitions
    presets: {
      fast: 'all 100ms ease',
      normal: 'all 200ms ease',
      slow: 'all 300ms ease',
      color: 'color 200ms ease, background-color 200ms ease, border-color 200ms ease',
      transform: 'transform 200ms ease',
      opacity: 'opacity 200ms ease',
      shadow: 'box-shadow 200ms ease',
    },
  },

  // Border widths
  borderWidths: {
    none: '0',
    thin: '1px',
    medium: '2px',
    thick: '4px',
  },

  // Opacity scale
  opacities: {
    0: '0',
    5: '0.05',
    10: '0.1',
    20: '0.2',
    25: '0.25',
    30: '0.3',
    40: '0.4',
    50: '0.5',
    60: '0.6',
    70: '0.7',
    75: '0.75',
    80: '0.8',
    90: '0.9',
    95: '0.95',
    100: '1',
  },

  // Aspect ratios
  aspectRatios: {
    square: '1 / 1',
    video: '16 / 9',
    photo: '4 / 3',
    portrait: '3 / 4',
    wide: '21 / 9',
  },
} as const;

export type BaseTheme = typeof baseTheme;
