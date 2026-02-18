/**
 * Localization Module
 *
 * Type-safe internationalization for React Native apps.
 *
 * Quick start:
 * ```tsx
 * import { LocalizationProvider, useLocalization } from './shared/localization';
 *
 * // Wrap app with provider
 * function App() {
 *   return (
 *     <LocalizationProvider>
 *       <YourApp />
 *     </LocalizationProvider>
 *   );
 * }
 *
 * // Use in components
 * function MyComponent() {
 *   const { t } = useLocalization();
 *   return <Text>{t('buttons.save')}</Text>;
 * }
 * ```
 */

// Core i18n exports
export {
  // Initialization
  initializeI18n,
  setLanguage,
  getCurrentLanguage,
  detectDeviceLanguage,

  // Translation function
  t,
  createNamespacedT,

  // Formatting
  formatDate,
  formatNumber,
  formatCurrency,
  formatRelativeTime,

  // Utilities
  isRTL,
  getAvailableLanguages,
  getPluralCategory,
  loadTranslations,

  // Constants
  SUPPORTED_LANGUAGES,
  DEFAULT_LANGUAGE,
  LANGUAGE_META,

  // Types
  type SupportedLanguage,
  type TranslationNamespace,
  type PluralCategory,
  type TranslationValue,
  type TranslationObject,
} from './i18n';

// React hooks exports
export {
  // Provider
  LocalizationProvider,

  // Main hook
  useLocalization,

  // Namespace-specific hooks
  useTranslation,
  useOnboardingTranslation,
  useSettingsTranslation,
  useSubscriptionTranslation,
  useNotificationTranslation,

  // Formatting hooks
  useNumberFormat,
  useDateFormat,

  // Language switcher hook
  useLanguageSwitcher,
} from './useLocalization';
