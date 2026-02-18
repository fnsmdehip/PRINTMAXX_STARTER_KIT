# GlowMaxx

Your complete glow up companion. Track mewing, facial exercises, skincare routines, debloating, and progress photos in one app.

## Features

- **Mewing Timer**: Guided timer with posture reminders and daily goal tracking
- **Facial Exercises**: Gender-specific routines for jawline, cheekbones, neck
- **Debloat Tracking**: Log water intake, sodium levels, and sleep
- **Progress Photos**: Before/after comparison with angle guidance
- **Skincare Routines**: Morning and evening skincare checklists
- **Educational Guides**: Mewing, softmaxxing, leanmaxxing, and more
- **Streaks & Achievements**: Stay motivated with gamified consistency

## Tech Stack

- Expo SDK 51
- React Native 0.74
- expo-router (file-based routing)
- Zustand (state management)
- AsyncStorage (persistence)
- react-native-purchases (RevenueCat)
- TypeScript

## Getting Started

### Prerequisites

- Node.js 18+
- Expo CLI
- iOS Simulator or Android Emulator

### Installation

```bash
# Clone and navigate
cd glowmaxx

# Install dependencies
npm install

# Start development server
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
```

### Environment Setup

1. Copy `.env.example` to `.env`
2. Add your RevenueCat API keys:
   - `REVENUECAT_API_KEY_IOS`
   - `REVENUECAT_API_KEY_ANDROID`

## Project Structure

```
glowmaxx/
├── app/                    # Expo Router pages
│   ├── (tabs)/            # Tab navigation
│   │   ├── home.tsx       # Daily dashboard
│   │   ├── routines.tsx   # Exercise routines
│   │   ├── progress.tsx   # Progress photos
│   │   ├── learn.tsx      # Educational content
│   │   └── settings.tsx   # App settings
│   ├── onboarding.tsx     # Onboarding flow
│   ├── paywall.tsx        # Subscription screen
│   └── routine-player.tsx # Exercise player
├── src/
│   ├── components/        # Reusable components
│   ├── data/              # Exercise and guide data
│   ├── services/          # RevenueCat, notifications
│   ├── stores/            # Zustand state stores
│   ├── types/             # TypeScript types
│   └── utils/             # Constants, helpers
├── marketing/             # ASO, social, GTM docs
└── assets/                # Images, icons
```

## Monetization

- 7-day free trial
- Monthly: $9.99
- Annual: $49.99

RevenueCat handles subscription management.

## Building for Production

```bash
# iOS
eas build --platform ios

# Android
eas build --platform android

# Both
eas build --platform all
```

## Marketing Assets

See `/marketing` folder:
- `app_store_description.md` - Store listing copy
- `keywords.txt` - ASO keywords
- `social_posts.md` - TikTok/Instagram content
- `aso_checklist.md` - Launch checklist
- `gtm_strategy.md` - Go-to-market plan
- `influencer_outreach.md` - Creator partnerships

## Target Audience

1. **Looksmaxxing community** (18-30, male-dominated)
2. **Glow up seekers** (18-35, female-dominated)
3. **Anti-aging seekers** (30-50, face yoga audience)

## Competitor Positioning

| Feature | GlowMaxx | Mewing Apps | Face Yoga Apps |
|---------|----------|-------------|----------------|
| Mewing timer | Yes | Yes | No |
| Facial exercises | Yes | Some | Yes |
| Debloat tracking | Yes | No | No |
| Progress photos | Yes | Some | Some |
| All-in-one | Yes | No | No |
| Price | $9.99 | $5-15 | $15-25 |

## Roadmap

### v1.1
- Home screen widget
- More exercise routines
- Improved progress comparison

### v1.2
- Apple Watch app
- Streak restoration IAP
- Weekly summaries

### v1.3
- Community features (optional)
- AI recommendations
- Posture tracking

## License

Proprietary. All rights reserved.

## Support

support@glowmaxx.app
