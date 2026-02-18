# PromptVault

AI prompt library and management app. Free prompts for everyone. Pro features for power users.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npx expo start
```

Scan QR code with Expo Go app to test on your device.

## Features

### Free Tier
- 1,050+ curated prompts across 9 categories
- Search with fuzzy matching (Fuse.js)
- Save favorites (persisted with AsyncStorage)
- Copy to clipboard with one tap
- Create your own prompts

### Pro Tier ($19/month or $99/year)
- AI Prompt Improver
- Prompt Generator
- Unlimited organization
- Prompt history
- No ads

## Tech Stack

- **Framework:** React Native with Expo
- **Navigation:** React Navigation 6
- **State:** Zustand with persist middleware
- **Search:** Fuse.js for fuzzy search
- **Storage:** AsyncStorage for local data
- **Payments:** RevenueCat (placeholder)
- **AI:** OpenAI API (placeholder)

## Project Structure

```
promptvault/
├── App.tsx                 # Entry point
├── src/
│   ├── screens/           # Screen components
│   │   ├── HomeScreen.tsx
│   │   ├── PromptDetailScreen.tsx
│   │   ├── FavoritesScreen.tsx
│   │   ├── ImproveScreen.tsx
│   │   └── SettingsScreen.tsx
│   ├── components/        # Reusable components
│   │   ├── PromptCard.tsx
│   │   ├── SearchBar.tsx
│   │   ├── CategoryChip.tsx
│   │   ├── Toast.tsx
│   │   ├── Paywall.tsx
│   │   └── CreatePromptModal.tsx
│   ├── stores/            # Zustand state management
│   │   ├── promptStore.ts
│   │   ├── favoriteStore.ts
│   │   └── subscriptionStore.ts
│   ├── data/              # Static data
│   │   └── prompts.ts     # 1,050+ prompts from awesome-chatgpt-prompts (MIT)
│   ├── navigation/        # Navigation setup
│   │   └── RootNavigator.tsx
│   ├── types/             # TypeScript types
│   │   └── index.ts
│   └── utils/             # Utilities
│       └── theme.ts       # Colors, spacing, fonts
├── __tests__/             # Jest tests
│   ├── promptStore.test.ts
│   ├── favoriteStore.test.ts
│   └── subscriptionStore.test.ts
└── assets/                # App icons, splash screens
```

## Commands

```bash
# Development
npm start            # Start Expo dev server
npm run ios          # Run on iOS simulator
npm run android      # Run on Android emulator

# Testing
npm test             # Run Jest tests

# Linting
npm run lint         # Run ESLint
```

## Configuration

### Environment Variables

Create `.env` for production:
```
OPENAI_API_KEY=sk-...
REVENUECAT_API_KEY=...
```

### App Store IDs

Update in `app.json`:
- iOS: `ios.bundleIdentifier`
- Android: `android.package`

## Next Steps

See `SUBMISSION_CHECKLIST.md` for:
1. Asset generation
2. RevenueCat setup
3. AI API integration
4. App store submission

## Documentation

- PRD: `products/promptvault/PRD.md`
- Tech Spec: `products/promptvault/TECH_SPEC.md`
