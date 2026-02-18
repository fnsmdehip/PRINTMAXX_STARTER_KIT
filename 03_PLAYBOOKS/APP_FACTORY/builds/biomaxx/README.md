# BioMaxx - Biohacking & Longevity Tracker

A premium React Native Expo app for tracking biohacking protocols and optimizing your biology.

## Features

- **Protocol Tracking**: Log fasting, cold exposure, sleep, red light therapy, supplements, and movement
- **Daily Longevity Score**: Aggregate metric based on completed protocols
- **Streak System**: Motivational streaks with flame badges
- **Session Timer**: Built-in timer for timed protocols
- **Learn Section**: Evidence-based articles and guides
- **Premium Subscriptions**: Trial and premium tiers

## Tech Stack

- Expo SDK 51
- expo-router v3 (file-based routing)
- React Native 0.74.0
- Zustand (state management with AsyncStorage persistence)
- @expo/vector-icons (Ionicons)
- expo-haptics

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
```

## Project Structure

```
biomaxx/
├── app/                    # expo-router pages
│   ├── _layout.tsx        # Root layout
│   ├── index.tsx          # Entry redirect
│   ├── onboarding.tsx     # Onboarding flow
│   └── (tabs)/            # Tab navigation
│       ├── dashboard.tsx  # Home with protocol rings
│       ├── protocols.tsx  # Protocol list & logging
│       ├── learn.tsx      # Education articles
│       └── profile.tsx    # Settings & subscription
├── src/
│   ├── stores/            # Zustand stores
│   ├── components/        # Reusable components
│   ├── types/             # TypeScript types
│   └── utils/             # Constants & helpers
├── assets/                # App icons & splash
└── package.json
```

## Color Palette

```typescript
const COLORS = {
  primary: '#10B981',      // Deep emerald green
  secondary: '#F59E0B',    // Warm amber
  accent: '#FFD93D',       // Gold (achievements)
  background: '#0F172A',   // Deep slate
  surface: '#1E293B',      // Elevated surface
};
```

## Protocols Included

### Free Tier
- Intermittent Fasting
- Cold Exposure
- Sleep
- Red Light Therapy
- Supplements
- Movement

### Premium Tier
- Sauna / Heat Therapy
- Breathwork
- Morning Sunlight
- Grounding

## Assets Required

Add these to the `assets/` folder:
- `icon.png` (1024x1024)
- `splash.png` (1284x2778)
- `adaptive-icon.png` (1024x1024)
- `favicon.png` (48x48)

## Disclaimer

BioMaxx is for educational purposes only and does not provide medical advice. Always consult with healthcare professionals before starting any new health protocol.
