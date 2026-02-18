/**
 * App Theme Exports
 * Central export point for all app-specific themes
 */

// PrayerLock - Faith/Meditation App
export {
  prayerlockLightTheme,
  prayerlockDarkTheme,
  prayerlockBrand,
} from './prayerlock_theme';

// WalkToUnlock - Fitness/Steps App
export {
  walktounlockLightTheme,
  walktounlockDarkTheme,
  walktounlockBrand,
} from './walktounlock_theme';

// StudyLock - Focus/Study App
export {
  studylockLightTheme,
  studylockDarkTheme,
  studylockBrand,
} from './studylock_theme';

// PromptVault - AI Prompt Management
export {
  promptvaultLightTheme,
  promptvaultDarkTheme,
  promptvaultBrand,
} from './promptvault_theme';

// DailyAnchor - Journaling/Reflection App
export {
  dailyanchorLightTheme,
  dailyanchorDarkTheme,
  dailyanchorBrand,
} from './dailyanchor_theme';

// FemFit - Women's Fitness App
export {
  femfitLightTheme,
  femfitDarkTheme,
  femfitBrand,
} from './femfit_theme';

// DailyDevotion - Devotional/Spiritual App
export {
  dailydevotionLightTheme,
  dailydevotionDarkTheme,
  dailydevotionBrand,
} from './dailydevotion_theme';

// Theme registry for easy access
export const appThemes = {
  prayerlock: {
    light: () => import('./prayerlock_theme').then((m) => m.prayerlockLightTheme),
    dark: () => import('./prayerlock_theme').then((m) => m.prayerlockDarkTheme),
    brand: () => import('./prayerlock_theme').then((m) => m.prayerlockBrand),
  },
  walktounlock: {
    light: () => import('./walktounlock_theme').then((m) => m.walktounlockLightTheme),
    dark: () => import('./walktounlock_theme').then((m) => m.walktounlockDarkTheme),
    brand: () => import('./walktounlock_theme').then((m) => m.walktounlockBrand),
  },
  studylock: {
    light: () => import('./studylock_theme').then((m) => m.studylockLightTheme),
    dark: () => import('./studylock_theme').then((m) => m.studylockDarkTheme),
    brand: () => import('./studylock_theme').then((m) => m.studylockBrand),
  },
  promptvault: {
    light: () => import('./promptvault_theme').then((m) => m.promptvaultLightTheme),
    dark: () => import('./promptvault_theme').then((m) => m.promptvaultDarkTheme),
    brand: () => import('./promptvault_theme').then((m) => m.promptvaultBrand),
  },
  dailyanchor: {
    light: () => import('./dailyanchor_theme').then((m) => m.dailyanchorLightTheme),
    dark: () => import('./dailyanchor_theme').then((m) => m.dailyanchorDarkTheme),
    brand: () => import('./dailyanchor_theme').then((m) => m.dailyanchorBrand),
  },
  femfit: {
    light: () => import('./femfit_theme').then((m) => m.femfitLightTheme),
    dark: () => import('./femfit_theme').then((m) => m.femfitDarkTheme),
    brand: () => import('./femfit_theme').then((m) => m.femfitBrand),
  },
  dailydevotion: {
    light: () => import('./dailydevotion_theme').then((m) => m.dailydevotionLightTheme),
    dark: () => import('./dailydevotion_theme').then((m) => m.dailydevotionDarkTheme),
    brand: () => import('./dailydevotion_theme').then((m) => m.dailydevotionBrand),
  },
} as const;

export type AppName = keyof typeof appThemes;
