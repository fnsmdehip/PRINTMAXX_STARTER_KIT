# PromptVault SDK 54 - Modern Expo App

A completely rebuilt version of PromptVault for Expo SDK 54 with Expo Router, React 19, and React Native 0.81.5.

## Quick Start

```bash
# Install dependencies
npm install

# Copy assets from original app
cp ../promptvault/assets/* ./assets/

# Run on iOS
npm run ios

# Run on Android
npm run android
```

## What's New

✅ **Expo Router** - File-based routing (no more @react-navigation)
✅ **React 19** - Latest features and performance
✅ **New Architecture** - Better performance on modern devices
✅ **Zustand v5** - Simplified state management
✅ **SDK 54** - Latest Expo version with improvements

## File Structure

```
promptvault-sdk54/
├── app/                    # File-based routing (Expo Router)
│   ├── _layout.tsx        # Root layout
│   ├── index.tsx          # Initialization & routing
│   ├── onboarding.tsx     # First-time setup
│   └── (tabs)/            # Tab group
│       ├── _layout.tsx    # Tab navigation
│       ├── home.tsx       # Library
│       ├── favorites.tsx  # Saved prompts
│       ├── improve.tsx    # Enhancement tool
│       └── settings.tsx   # User settings
│
├── src/
│   ├── screens/           # Screen components
│   │   ├── HomeScreen.tsx
│   │   ├── FavoritesScreen.tsx
│   │   ├── ImproveScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   ├── OnboardingScreen.tsx
│   │   └── ...
│   │
│   ├── components/        # UI components
│   │   ├── PromptCard.tsx
│   │   ├── SearchBar.tsx
│   │   ├── CategoryChip.tsx
│   │   └── ...
│   │
│   ├── stores/           # Zustand state management
│   │   ├── promptStore.ts
│   │   ├── favoriteStore.ts
│   │   ├── subscriptionStore.ts
│   │   └── onboardingStore.ts
│   │
│   ├── types/            # TypeScript definitions
│   ├── utils/            # Utilities (theme, constants)
│   ├── services/         # Business logic
│   └── data/             # Static data (1000+ prompts)
│
├── assets/               # App icons, splashes, etc.
├── package.json          # Dependencies
├── app.json              # Expo config
└── SETUP.md              # Setup instructions
```

## Key Features

### 📚 Library
- Browse 1000+ AI prompts
- Search and filter by category
- Create custom prompts
- Copy to clipboard

### ❤️ Favorites
- Save prompts you use often
- Quick access from tab
- Persists across sessions

### ✨ Improve
- Enhance prompt quality
- AI-powered suggestions
- Better results

### ⚙️ Settings
- Manage subscription (Pro/Free)
- Privacy & terms
- About & support

## State Management

All state uses Zustand with AsyncStorage persistence:

| Store | Purpose | Persisted |
|-------|---------|-----------|
| `usePromptStore` | Prompt data, search, filtering | No |
| `useFavoriteStore` | Saved prompt IDs | Yes |
| `useSubscriptionStore` | Pro status, trial, expiration | Yes |
| `useOnboardingStore` | Completion, preferences | Yes |

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| expo | 54.0.32 | React Native framework |
| expo-router | 6.0.22 | File-based routing |
| react | 19.1.0 | UI library |
| react-native | 0.81.5 | Native components |
| zustand | 5.0.10 | State management |
| fuse.js | 7.0.0 | Fuzzy search |

## Development

### Install Dependencies
```bash
npm install
```

### Run on Device
```bash
npm run ios      # iOS Simulator
npm run android  # Android Emulator
npm start        # Dev server
```

### Build for Submission
```bash
# Use EAS CLI (Expo Application Services)
eas build --platform ios
eas build --platform android
```

## Migration from Original

**What Changed:**
- Navigation from React Navigation → Expo Router
- App entry from `App.tsx` → `app/` directory
- Onboarding from AsyncStorage → Zustand store
- Package versions upgraded across the board

**What Stayed the Same:**
- All screens and components work identically
- All prompt data (1000+ prompts)
- All state logic
- All UI/UX

## Testing

Before submitting:
- [ ] App launches without errors
- [ ] Onboarding flow works
- [ ] Search and filtering work
- [ ] Favorites save and persist
- [ ] Settings load correctly
- [ ] No console warnings

## Troubleshooting

**Issue: "Module not found"**
→ Run `npm install`

**Issue: "Assets not found"**
→ Copy from original: `cp ../promptvault/assets/* ./assets/`

**Issue: App crashes**
→ Clear cache: `expo start -c`

See `SETUP.md` for detailed troubleshooting.

## Documentation

- **SETUP.md** - Complete setup and configuration guide
- **SDK54_UPGRADE.md** - Migration details and breaking changes

## Support

For issues or questions about the upgrade, refer to:
- [Expo Router Documentation](https://docs.expo.dev/routing/)
- [React 19 Migration Guide](https://react.dev/blog/2024/12/19/react-19)
- [Zustand Documentation](https://github.com/pmndrs/zustand)

---

**Version:** 1.0.0
**SDK:** Expo 54
**React:** 19.1.0
**React Native:** 0.81.5
