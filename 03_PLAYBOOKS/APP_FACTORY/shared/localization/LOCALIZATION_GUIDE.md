# Localization Guide

Step-by-step guide for adding languages, managing translations, and maintaining quality across localized apps.

## Quick start

```typescript
// 1. Wrap your app with the provider
import { LocalizationProvider } from './shared/localization/useLocalization';

function App() {
  return (
    <LocalizationProvider>
      <YourApp />
    </LocalizationProvider>
  );
}

// 2. Use translations in components
import { useTranslation } from './shared/localization/useLocalization';

function MyComponent() {
  const { t } = useTranslation('common');
  return <Text>{t('buttons.save')}</Text>;
}
```

## Directory structure

```
shared/localization/
├── i18n.ts                 # Core i18n logic
├── useLocalization.ts      # React hooks
├── LOCALIZATION_GUIDE.md   # This file
├── priority_languages.md   # Language prioritization
└── translations/
    ├── en/                 # English (base language)
    │   ├── common.json
    │   ├── onboarding.json
    │   ├── settings.json
    │   ├── subscription.json
    │   └── notifications.json
    ├── es/                 # Spanish
    ├── pt/                 # Portuguese
    ├── fr/                 # French
    └── de/                 # German
```

## Adding a new language

### 1. Create language folder

```bash
mkdir -p translations/[language_code]/
```

Use ISO 639-1 codes: `es` (Spanish), `pt` (Portuguese), `fr` (French), `de` (German).

### 2. Copy English files as base

```bash
cp translations/en/*.json translations/[language_code]/
```

### 3. Update i18n.ts

Add the language code to `SUPPORTED_LANGUAGES` and `LANGUAGE_META`:

```typescript
export const SUPPORTED_LANGUAGES = ['en', 'es', 'pt', 'fr', 'de', 'NEW_CODE'] as const;

export const LANGUAGE_META = {
  // ...existing languages
  NEW_CODE: { name: 'Language Name', nativeName: 'Nome Nativo', rtl: false },
};
```

### 4. Add plural rules (if different from English)

Update `getPluralCategory()` in i18n.ts if the language has different plural rules.

### 5. Translate

Send JSON files to translator or translation service.

## Key naming conventions

### Structure

Use dot notation for nested keys. Keep hierarchy shallow (max 3 levels).

```json
{
  "section": {
    "subsection": {
      "key": "value"
    }
  }
}
```

### Naming rules

| Type | Pattern | Example |
|------|---------|---------|
| Buttons | `buttons.[action]` | `buttons.save`, `buttons.cancel` |
| Labels | `labels.[noun]` | `labels.email`, `labels.name` |
| Errors | `errors.[type]` | `errors.network`, `errors.invalidEmail` |
| Titles | `[screen].title` | `settings.title`, `paywall.title` |
| Descriptions | `[screen].subtitle` or `[item].description` | `trial.subtitle` |
| Actions | `[context].[action]` | `account.signOut.confirm` |

### Key format

- Use camelCase: `passwordMismatch`, not `password_mismatch`
- Be descriptive: `confirmDeleteTitle`, not `title1`
- Group related keys: `subscription.plans.monthly.price`

## Translation workflow

### Export for translation

```bash
# Generate CSV for translators
python AUTOMATIONS/translation_export.py export \
  --source translations/en \
  --output translations_for_review.csv

# Or export specific namespaces
python AUTOMATIONS/translation_export.py export \
  --source translations/en \
  --namespace common,onboarding \
  --output partial_export.csv
```

### Send to translators

1. Share the CSV file with your translation team/service
2. Include the context section (column C) for each string
3. Specify character limits where applicable (UI buttons, push notifications)

### Import translations

```bash
# Import translated CSV back to JSON
python AUTOMATIONS/translation_export.py import \
  --input translated_spanish.csv \
  --output translations/es
```

### Review checklist

After importing translations, verify:

- [ ] All placeholders preserved ({{variable}})
- [ ] Plural forms complete (one, other, few, many)
- [ ] No truncated strings (check UI)
- [ ] Links and special characters intact
- [ ] App-specific terminology consistent

## Interpolation and plurals

### Variable interpolation

Use `{{variableName}}` syntax:

```json
{
  "greeting": "Hello, {{name}}!",
  "items": "You have {{count}} items"
}
```

```typescript
t('greeting', { variables: { name: 'John' } });
// Output: "Hello, John!"
```

### Pluralization

Define all required plural forms:

```json
{
  "items": {
    "one": "{{count}} item",
    "other": "{{count}} items"
  },
  "days": {
    "one": "{{count}} day left",
    "other": "{{count}} days left"
  }
}
```

```typescript
t('items', { count: 1 });  // "1 item"
t('items', { count: 5 });  // "5 items"
```

### Plural categories by language

| Language | Categories |
|----------|------------|
| English, German, Portuguese | one, other |
| French | one (0-1), other |
| Spanish | one, other |
| Russian | one, few, many, other |
| Arabic | zero, one, two, few, many, other |

## Context for translators

Provide context in comments or a separate context file:

```json
{
  "_context": {
    "buttons.cta": "Main call-to-action button on paywall screen. Max 20 characters.",
    "trial.badge": "Small badge shown on pricing card. Keep very short.",
    "errors.network": "Shown when device has no internet connection."
  },
  "buttons": {
    "cta": "Subscribe Now"
  }
}
```

### Context categories

1. **Screen context**: Where the string appears
2. **Character limits**: For UI elements with space constraints
3. **Placeholders**: What each {{variable}} contains
4. **Tone**: Formal vs. casual, urgency level
5. **Gender considerations**: If applicable

## Testing localization

### Manual testing checklist

For each language:

- [ ] All screens render without text overflow
- [ ] Dates/numbers format correctly
- [ ] RTL layout works (if applicable)
- [ ] Push notifications display properly
- [ ] No hardcoded strings visible
- [ ] Plurals work (test with 0, 1, 2, 5, 21)

### Automated validation

```bash
# Check for missing keys
python AUTOMATIONS/translation_export.py validate \
  --base translations/en \
  --target translations/es

# Output:
# Missing keys in es:
#   - onboarding.newFeature.title
#   - settings.danger.newOption
```

### Screenshot testing

Take screenshots of key screens in each language to verify layout.

### Pseudo-localization

For testing before real translations:

```typescript
// Pseudo-locale adds markers to detect hardcoded strings
// "Save" -> "[[ Śåvé ]]"
```

## Common issues and solutions

### Text truncation

**Problem**: Translated text too long for UI element.
**Solution**:
- Specify character limits in context
- Use flexible UI (auto-sizing, scrolling)
- Provide shorter alternatives

### Missing placeholders

**Problem**: Translator removes `{{variable}}`.
**Solution**:
- Highlight placeholders in red in export
- Validate imports automatically

### Inconsistent terminology

**Problem**: Same term translated differently.
**Solution**:
- Create glossary of app-specific terms
- Use translation memory tools

### Encoding issues

**Problem**: Special characters display wrong.
**Solution**:
- Ensure UTF-8 encoding throughout
- Test with non-ASCII characters

## Translation services

### Budget options (<$0.05/word)

- Gengo (crowdsourced)
- Translated.com
- TextMaster
- Community translation

### Premium options ($0.08-0.15/word)

- Lokalise
- Phrase (formerly PhraseApp)
- Smartling
- Professional agencies

### AI-assisted (use for draft, human review)

- DeepL (best quality for European languages)
- Google Cloud Translation
- Amazon Translate

**Recommendation**: Use AI for first draft, human translator for review. Saves 40-60% cost.

## File maintenance

### Adding new strings

1. Add to English file first (source of truth)
2. Run export script
3. Send delta to translators
4. Import translations

### Removing strings

1. Remove from all language files
2. Search codebase for key usage
3. Update changelog

### Renaming keys

1. Find all usages in code
2. Update code references
3. Update all language files
4. Run validation

## Performance tips

### Lazy loading translations

```typescript
// Load only needed namespaces per screen
const { t } = useTranslation('onboarding');
```

### Bundle size

- Each language adds ~20-50KB (gzipped: 5-15KB)
- Consider lazy-loading non-primary languages

### Caching

Translations are cached after first load. Language switch doesn't re-download already-loaded languages.

## Checklist: launching new language

- [ ] All namespaces translated
- [ ] Translation quality reviewed by native speaker
- [ ] Plural forms validated
- [ ] Date/number formatting tested
- [ ] Push notification copy fits character limits
- [ ] App Store metadata localized
- [ ] Screenshots updated for App Store
- [ ] Support documentation available
