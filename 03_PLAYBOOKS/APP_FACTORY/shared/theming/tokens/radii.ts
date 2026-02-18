/**
 * Border Radius Tokens
 * Consistent corner rounding across all components
 */

export const radii = {
  none: '0',
  sm: '0.125rem',    // 2px
  base: '0.25rem',   // 4px
  md: '0.375rem',    // 6px
  lg: '0.5rem',      // 8px
  xl: '0.75rem',     // 12px
  '2xl': '1rem',     // 16px
  '3xl': '1.5rem',   // 24px
  full: '9999px',    // Pill shape
} as const;

// Semantic radii for component types
export const componentRadii = {
  // Buttons
  buttonSm: radii.md,
  buttonMd: radii.lg,
  buttonLg: radii.xl,
  buttonPill: radii.full,

  // Inputs
  inputSm: radii.md,
  inputMd: radii.lg,
  inputLg: radii.xl,

  // Cards
  cardSm: radii.lg,
  cardMd: radii.xl,
  cardLg: radii['2xl'],

  // Modals and dialogs
  modal: radii['2xl'],
  dialog: radii.xl,

  // Badges and chips
  badge: radii.full,
  chip: radii.full,

  // Avatars
  avatarSm: radii.lg,
  avatarMd: radii.xl,
  avatarLg: radii['2xl'],
  avatarRound: radii.full,

  // Tooltips and popovers
  tooltip: radii.md,
  popover: radii.lg,

  // Progress bars
  progress: radii.full,

  // Images
  imageSm: radii.lg,
  imageMd: radii.xl,
  imageLg: radii['2xl'],
} as const;

export type Radius = keyof typeof radii;
export type ComponentRadius = keyof typeof componentRadii;
