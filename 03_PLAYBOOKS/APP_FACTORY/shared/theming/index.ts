/**
 * Theming System
 * Central export for all theming utilities
 *
 * @example
 * // In your app's root layout
 * import { ThemeProvider, ThemeScript } from '@/shared/theming';
 * import { prayerlockLightTheme, prayerlockDarkTheme } from '@/shared/theming/app_themes';
 *
 * export default function RootLayout({ children }) {
 *   return (
 *     <html>
 *       <head>
 *         <ThemeScript />
 *       </head>
 *       <body>
 *         <ThemeProvider
 *           lightThemeOverride={prayerlockLightTheme}
 *           darkThemeOverride={prayerlockDarkTheme}
 *         >
 *           {children}
 *         </ThemeProvider>
 *       </body>
 *     </html>
 *   );
 * }
 *
 * @example
 * // In a component
 * import { useTheme, useColor, useModeValue } from '@/shared/theming';
 *
 * function MyComponent() {
 *   const { theme, toggleTheme, resolvedMode } = useTheme();
 *   const bgColor = useColor('background.primary');
 *   const textColor = useModeValue('#000', '#FFF');
 *
 *   return (
 *     <div style={{ background: bgColor, color: textColor }}>
 *       <button onClick={toggleTheme}>
 *         Current: {resolvedMode}
 *       </button>
 *     </div>
 *   );
 * }
 */

// Provider and Context
export {
  ThemeProvider,
  ThemeContext,
  ThemeScript,
  getThemeScript,
} from './ThemeProvider';

// Hooks
export {
  useTheme,
  useThemeValue,
  useThemeMode,
  useThemeControls,
  useColor,
  useSpacing,
  useShadow,
  useThemeReady,
  useModeValue,
  useThemeValues,
  useBreakpoint,
} from './useTheme';

// Styling utilities
export {
  createThemedStyle,
  createVariants,
  getVariantStyle,
  mergeStyles,
  conditionalStyle,
  themeColor,
  createCSSVariables,
  cssVariablesToString,
  responsive,
  buttonVariants,
  inputVariants,
  cardVariants,
  sizeScale,
} from './styled';
export type { StyleObject, VariantDefinition, ComponentVariants, Size } from './styled';

// Theme definitions
export { baseTheme } from './themes/base';
export { lightTheme } from './themes/light';
export { darkTheme } from './themes/dark';
export type { BaseTheme } from './themes/base';
export type { LightTheme } from './themes/light';
export type { DarkTheme } from './themes/dark';
export type { Theme, ThemeMode } from './themes';

// Design tokens
export {
  colors,
  fontFamilies,
  fontSizes,
  fontWeights,
  lineHeights,
  letterSpacings,
  textStyles,
  spacing,
  semanticSpacing,
  shadows,
  shadowsDark,
  coloredShadows,
  elevation,
  elevationDark,
  radii,
  componentRadii,
} from './tokens';

export type {
  ColorScale,
  ColorToken,
  FontSize,
  FontWeight,
  LineHeight,
  TextStyle,
  SpacingToken,
  SemanticSpacing,
  Shadow,
  Elevation,
  Radius,
  ComponentRadius,
} from './tokens';

// App themes
export {
  appThemes,
  // PrayerLock
  prayerlockLightTheme,
  prayerlockDarkTheme,
  prayerlockBrand,
  // WalkToUnlock
  walktounlockLightTheme,
  walktounlockDarkTheme,
  walktounlockBrand,
  // StudyLock
  studylockLightTheme,
  studylockDarkTheme,
  studylockBrand,
  // PromptVault
  promptvaultLightTheme,
  promptvaultDarkTheme,
  promptvaultBrand,
  // DailyAnchor
  dailyanchorLightTheme,
  dailyanchorDarkTheme,
  dailyanchorBrand,
  // FemFit
  femfitLightTheme,
  femfitDarkTheme,
  femfitBrand,
  // DailyDevotion
  dailydevotionLightTheme,
  dailydevotionDarkTheme,
  dailydevotionBrand,
} from './app_themes';
export type { AppName } from './app_themes';
