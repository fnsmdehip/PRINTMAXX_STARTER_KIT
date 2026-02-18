# PromptVault Submission Checklist

Manual steps required before launching to App Store / Play Store.

## Pre-Setup (Do These First)

### 1. Install Dependencies
```bash
cd MONEY_METHODS/APP_FACTORY/builds/promptvault
npm install
```

### 2. Run Development Server
```bash
npx expo start
```
Scan QR code with Expo Go app to test.

---

## Asset Generation

### App Icons
Generate these using Figma, Canva, or DALL-E:

- [ ] `assets/icon.png` - 1024x1024 app icon
- [ ] `assets/adaptive-icon.png` - 1024x1024 Android adaptive icon
- [ ] `assets/splash.png` - 1284x2778 splash screen
- [ ] `assets/favicon.png` - 48x48 web favicon

Brand colors to use:
- Primary: #6366f1 (indigo)
- Background: #0f0f23 (dark navy)
- Accent: #22d3ee (cyan)

---

## RevenueCat Integration

### 1. Create RevenueCat Account
Go to: https://www.revenuecat.com

### 2. Create App in RevenueCat Dashboard
- [ ] Create iOS app
- [ ] Create Android app
- [ ] Note your API keys

### 3. Create Products in App Store Connect / Play Console

**iOS (App Store Connect):**
- [ ] Product ID: `promptvault_pro_monthly` - $19/month
- [ ] Product ID: `promptvault_pro_annual` - $99/year

**Android (Play Console):**
- [ ] Product ID: `promptvault_pro_monthly` - $19/month
- [ ] Product ID: `promptvault_pro_annual` - $99/year

### 4. Connect Products to RevenueCat
- [ ] Import products from App Store Connect
- [ ] Import products from Play Console
- [ ] Create "pro" entitlement
- [ ] Create offering with monthly/annual packages

### 5. Install RevenueCat SDK
```bash
npx expo install react-native-purchases
```

### 6. Update Code
Replace placeholder in `src/stores/subscriptionStore.ts`:
```typescript
import Purchases from 'react-native-purchases';

// In App.tsx or config:
Purchases.configure({ apiKey: 'YOUR_REVENUECAT_API_KEY' });

// In restorePurchases:
const customerInfo = await Purchases.restorePurchases();
const isPro = customerInfo.entitlements.active['pro'] !== undefined;
```

---

## AI API Integration (Pro Features)

### Option A: OpenAI
1. Get API key from: https://platform.openai.com
2. Add to environment:
```
OPENAI_API_KEY=sk-...
```
3. Update `src/screens/ImproveScreen.tsx`:
```typescript
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${OPENAI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'gpt-4o-mini',
    messages: [
      { role: 'system', content: IMPROVE_SYSTEM_PROMPT },
      { role: 'user', content: inputPrompt },
    ],
  }),
});
```

### Option B: Use Backend
Better for production (hides API key):
1. Deploy API routes (Next.js, Cloudflare Worker, etc.)
2. Call your backend instead of OpenAI directly
3. Rate limit on backend

---

## App Store Submission

### Apple App Store

- [ ] **Apple Developer Account** ($99/year)
  - https://developer.apple.com/programs/enroll/

- [ ] **App Store Connect Setup**
  - Create new app
  - Bundle ID: `com.promptvault.app`

- [ ] **Screenshots** (required sizes)
  - 6.7" iPhone: 1290x2796 (iPhone 14 Pro Max)
  - 6.5" iPhone: 1242x2688 (iPhone 11 Pro Max)
  - 5.5" iPhone: 1242x2208 (iPhone 8 Plus)
  - 12.9" iPad: 2048x2732

- [ ] **App Metadata**
  - Name: PromptVault
  - Subtitle: AI Prompt Library
  - Category: Productivity
  - Description (see below)
  - Keywords: prompts, ai, chatgpt, claude, productivity, writing

- [ ] **Privacy Policy URL**
  - Host at: https://promptvault.app/privacy

- [ ] **App Review Info**
  - Provide demo account if needed
  - Explain subscription flow

### Google Play Store

- [ ] **Google Play Developer Account** ($25 one-time)
  - https://play.google.com/console

- [ ] **Play Store Listing**
  - Package name: `com.promptvault.app`

- [ ] **Screenshots** (required)
  - Phone: 1080x1920 minimum
  - 7" tablet: 1200x1920
  - 10" tablet: 1600x2560

- [ ] **Feature Graphic**
  - 1024x500

- [ ] **Content Rating**
  - Complete questionnaire

---

## App Store Description

Use this copy:

**Short Description (80 chars):**
1,050+ AI prompts. Search, copy, improve. Get better results from ChatGPT.

**Full Description:**
PromptVault is your go-to library for AI prompts that actually work.

Stop spending time writing prompts from scratch. Browse 1,050+ tested prompts across categories like writing, coding, marketing, and more. Copy any prompt with one tap and paste into ChatGPT, Claude, or your favorite AI.

FREE FEATURES:
- 1,050+ curated, tested prompts
- Categories: Writing, Coding, Marketing, Business, Creative, and more
- Fast search to find what you need
- Save favorites for quick access
- Copy to clipboard instantly

PRO FEATURES ($19/month or $99/year):
- AI Prompt Improver: Paste your prompt, get a better version
- Prompt Generator: Describe what you need, get a ready-to-use prompt
- Unlimited folders and organization
- Prompt history
- Export to Notion/Sheets
- No ads

Whether you are writing emails, debugging code, or creating marketing copy, PromptVault has prompts ready to use.

---

## Build Commands

### Development
```bash
npx expo start
```

### iOS Build (requires Mac)
```bash
npx expo run:ios
```

### Android Build
```bash
npx expo run:android
```

### Production Build with EAS
```bash
# Install EAS CLI
npm install -g eas-cli

# Login
eas login

# Configure
eas build:configure

# Build for stores
eas build --platform ios
eas build --platform android

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

---

## Testing Before Submission

- [ ] Test on real iPhone device
- [ ] Test on real Android device
- [ ] Test search with various queries
- [ ] Test copy functionality
- [ ] Test favorites add/remove
- [ ] Test category filtering
- [ ] Test prompt detail view
- [ ] Test paywall appears for Pro features
- [ ] Test trial start/end flow
- [ ] Test restore purchases
- [ ] Test settings links work

---

## Post-Launch

### Week 1
- [ ] Monitor reviews
- [ ] Respond to support emails
- [ ] Fix critical bugs
- [ ] Track conversion metrics

### Week 2-4
- [ ] Add requested prompts based on feedback
- [ ] Optimize paywall conversion
- [ ] A/B test pricing if needed
- [ ] Start collecting testimonials

### Month 2+
- [ ] Build Chrome extension
- [ ] Add community prompts feature
- [ ] Explore partnerships

---

## Estimated Costs

| Item | Cost |
|------|------|
| Apple Developer | $99/year |
| Google Play | $25 one-time |
| RevenueCat | Free up to $10k MRR |
| OpenAI API | ~$3/month at 10k requests |
| Domain | ~$12/year |
| **Total Year 1** | ~$140 |

---

## Questions?

Check the PRD: `products/promptvault/PRD.md`
Check the Tech Spec: `products/promptvault/TECH_SPEC.md`
