/**
 * Spacing Tokens
 * Consistent spacing scale for margins, paddings, and gaps
 */

export const spacing = {
  px: '1px',
  0: '0',
  0.5: '0.125rem',  // 2px
  1: '0.25rem',     // 4px
  1.5: '0.375rem',  // 6px
  2: '0.5rem',      // 8px
  2.5: '0.625rem',  // 10px
  3: '0.75rem',     // 12px
  3.5: '0.875rem',  // 14px
  4: '1rem',        // 16px
  5: '1.25rem',     // 20px
  6: '1.5rem',      // 24px
  7: '1.75rem',     // 28px
  8: '2rem',        // 32px
  9: '2.25rem',     // 36px
  10: '2.5rem',     // 40px
  11: '2.75rem',    // 44px
  12: '3rem',       // 48px
  14: '3.5rem',     // 56px
  16: '4rem',       // 64px
  20: '5rem',       // 80px
  24: '6rem',       // 96px
  28: '7rem',       // 112px
  32: '8rem',       // 128px
  36: '9rem',       // 144px
  40: '10rem',      // 160px
  44: '11rem',      // 176px
  48: '12rem',      // 192px
  52: '13rem',      // 208px
  56: '14rem',      // 224px
  60: '15rem',      // 240px
  64: '16rem',      // 256px
  72: '18rem',      // 288px
  80: '20rem',      // 320px
  96: '24rem',      // 384px
} as const;

// Semantic spacing aliases
export const semanticSpacing = {
  // Component internal padding
  componentPaddingXs: spacing[2],
  componentPaddingSm: spacing[3],
  componentPaddingMd: spacing[4],
  componentPaddingLg: spacing[6],
  componentPaddingXl: spacing[8],

  // Section spacing
  sectionPaddingMobile: spacing[6],
  sectionPaddingTablet: spacing[12],
  sectionPaddingDesktop: spacing[16],

  // Stack spacing (vertical rhythm)
  stackXs: spacing[1],
  stackSm: spacing[2],
  stackMd: spacing[4],
  stackLg: spacing[6],
  stackXl: spacing[8],

  // Inline spacing (horizontal)
  inlineXs: spacing[1],
  inlineSm: spacing[2],
  inlineMd: spacing[3],
  inlineLg: spacing[4],
  inlineXl: spacing[6],

  // Container max widths
  containerSm: '640px',
  containerMd: '768px',
  containerLg: '1024px',
  containerXl: '1280px',
  container2xl: '1536px',

  // Sidebar widths
  sidebarCollapsed: spacing[16],
  sidebarExpanded: spacing[64],

  // Header heights
  headerMobile: spacing[14],
  headerDesktop: spacing[16],

  // Bottom nav height (mobile)
  bottomNavHeight: spacing[16],
} as const;

export type SpacingToken = keyof typeof spacing;
export type SemanticSpacing = keyof typeof semanticSpacing;
