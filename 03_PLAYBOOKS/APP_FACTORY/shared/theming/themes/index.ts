/**
 * Theme Exports
 * Central export point for all theme definitions
 */

export { baseTheme } from './base';
export type { BaseTheme } from './base';

export { lightTheme } from './light';
export type { LightTheme } from './light';

export { darkTheme } from './dark';
export type { DarkTheme } from './dark';

// Combined theme type that works for both light and dark
export type Theme = typeof import('./light').lightTheme | typeof import('./dark').darkTheme;

// Theme mode type
export type ThemeMode = 'light' | 'dark' | 'system';
