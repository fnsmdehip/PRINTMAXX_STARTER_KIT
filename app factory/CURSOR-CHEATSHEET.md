# CURSOR CHEATSHEET: Fast App Development

## QUICK START - New App in 5 Minutes

### Step 1: Create Project
```bash
npx create-expo-app@latest [app-name] --template tabs
cd [app-name]
```

### Step 2: Install Core Dependencies
```bash
# Paste this entire block into terminal
npx expo install @supabase/supabase-js expo-secure-store
npx expo install react-native-purchases
npx expo install expo-image-picker expo-camera
npx expo install nativewind tailwindcss
npx expo install expo-notifications expo-constants
npm install zustand # State management
```

### Step 3: Open in Cursor & Use This Prompt
```
I have a new Expo app. Set up:

1. Supabase client in lib/supabase.ts with auth persistence using expo-secure-store
2. RevenueCat in lib/revenuecat.ts with initialization
3. Environment variables in .env (create .env.example with placeholders)
4. Basic auth context with useAuth hook
5. NativeWind/Tailwind config

Use TypeScript. Don't include actual API keys - use process.env placeholders.
```

---

## CORE PROMPTS LIBRARY

### 🔐 Authentication Setup
```
Add complete authentication to this Expo app:

1. Sign up screen with email/password
2. Sign in screen
3. Forgot password flow
4. Protected route wrapper that redirects to auth if not logged in
5. Auth state persistence using Supabase + expo-secure-store
6. Loading screen while checking auth state

Use Expo Router's redirect pattern for protected routes.
Store session securely. Handle all error cases with user-friendly messages.
```

### 💳 Paywall Implementation
```
Add a hard paywall using RevenueCat:

1. Create PaywallScreen component showing:
   - App value proposition (3-4 bullet points)
   - Price: $[X.XX]/week with [X]-day free trial
   - "Start Free Trial" CTA button
   - "Restore Purchases" link
   - Social proof quote with 5 stars

2. RevenueCat integration:
   - Initialize on app load
   - Check subscription status before showing main app
   - Purchase flow with loading state
   - Restore purchases functionality
   - Handle all error cases

3. Navigation flow:
   - New users → Onboarding → Paywall → Main App
   - Returning subscribers → Main App directly
   - Expired subscribers → Paywall

Use environment variable for RevenueCat API key.
```

### 📸 GPT-4 Vision Integration
```
Add image analysis using GPT-4 Vision:

1. Create a Supabase Edge Function (or use lib/openai.ts if client-side is acceptable)
2. Function accepts base64 image and analysis type
3. Calls OpenAI API with vision model
4. Returns structured JSON response

For security:
- Keep API key server-side (Edge Function preferred)
- If client-side necessary, use Supabase as proxy
- Rate limit requests per user
- Validate image size before sending

Include error handling for:
- API failures
- Invalid images
- Rate limits
- Network errors
```

### 📊 Streak & Gamification System
```
Add a streak tracking system:

1. Database:
   - Track daily check-ins with timestamps
   - Calculate current streak
   - Store longest streak record

2. Logic:
   - Increment streak on daily check-in
   - Reset streak if day is missed (check timezone)
   - Milestone badges at 7, 30, 100, 365 days

3. UI:
   - Prominent streak counter with fire emoji 🔥
   - Progress bar to next milestone
   - Confetti animation on milestone achievement
   - "Don't break the streak!" motivation message

4. Notifications:
   - Daily reminder if not checked in
   - Congratulations on milestones
   - Warning when streak at risk (evening if not checked in)

Handle timezone correctly - use user's local date, not UTC.
```

### 📱 Onboarding Flow
```
Create a 5-screen onboarding flow:

Screen 1: Hero - App name, tagline, compelling imagery
Screen 2: Problem - Address the pain point with a question
Screen 3: Agitation - Statistics or emotional content that builds desire
Screen 4: Solution - Show how the app solves their problem
Screen 5: Paywall - Pricing with CTA

Requirements:
- Swipeable screens with pagination dots
- "Skip" button that goes to paywall
- Progress indicator
- Each screen should build on previous
- Final screen transitions to paywall component

Use Expo Router with (onboarding) group.
Include skip detection analytics (which screen did they skip from).
```

### 🔔 Push Notifications
```
Set up push notifications with Expo:

1. Request permissions on first app open
2. Store Expo push token in Supabase user profile
3. Create notification triggers:
   - Daily reminder at user-chosen time
   - Milestone achievements
   - Streak at risk warnings

4. Handle notification taps (deep linking)

For local notifications:
- Schedule recurring daily notification
- Cancel/reschedule when user changes settings

Don't be annoying - let user control notification preferences.
```

### 🖼️ Shareable Results Card
```
Create a shareable results image:

1. Component that renders result (score, stats, etc.)
2. Use react-native-view-shot to capture as image
3. Add branded overlay:
   - App logo in corner
   - "Download [App Name]" text
   - Optional: QR code to App Store

4. Share flow:
   - Capture component as image
   - Use expo-sharing to open share sheet
   - Track share events for analytics

Make the card visually appealing - users will post this on social media.
Include subtle but visible branding.
```

---

## SECURITY PROMPTS

### Pre-Build Security Setup
```
Set up security best practices for this app:

1. Environment variables:
   - Create .env.example with all required vars (no real values)
   - Add .env to .gitignore
   - Create app.config.js that reads from process.env

2. Supabase RLS:
   - Enable RLS on all tables
   - Create policies: users can only access own data
   - Test that unauthenticated requests fail

3. Secure storage:
   - Use expo-secure-store for tokens
   - Never store sensitive data in AsyncStorage
   - Clear secure storage on logout

4. API security:
   - All external API calls through Edge Functions
   - Rate limiting on sensitive endpoints
   - Input validation on all user inputs

Generate the security configuration files.
```

### Pre-Submission Audit
```
Audit this codebase for App Store submission:

Security:
- [ ] No hardcoded API keys (search for "sk-", "key", "secret")
- [ ] All sensitive data in environment variables
- [ ] Supabase RLS enabled and tested
- [ ] No console.log with sensitive data
- [ ] HTTPS only for all requests

Apple Requirements:
- [ ] Privacy policy accessible before paywall
- [ ] Clear pricing display on paywall
- [ ] Restore purchases works correctly
- [ ] No incentivized reviews/ratings
- [ ] App description matches functionality

Performance:
- [ ] Images optimized
- [ ] No memory leaks (check useEffect cleanups)
- [ ] Loading states for all async operations
- [ ] Error boundaries for crash prevention

Generate a report of issues found and fixes needed.
```

### Find Hardcoded Secrets
```
Search this entire codebase for potential security issues:

1. Hardcoded API keys or tokens
2. Database connection strings
3. Secret keys or passwords
4. URLs with credentials
5. Console logs exposing sensitive data

For each finding:
- Show the file and line
- Explain the risk
- Provide the fix

Also check:
- .gitignore includes .env
- No secrets in version control history
```

---

## CONTEXT MANAGEMENT

### When Context Gets Long (Signs)
- Cursor starts forgetting earlier instructions
- Responses become generic
- "I don't see that file" when file was discussed earlier

### How to Reset Context
```
Start a fresh chat with this context:

App: [App Name]
Stack: Expo + Supabase + RevenueCat
Current status: [What's done]

Files to reference:
@app/screens/MainScreen.tsx
@lib/supabase.ts
@lib/revenuecat.ts

Current task: [What you need done]
```

### Efficient File References
```
# Good - loads specific file
@app/paywall.tsx - fix the purchase button

# Good - loads just what's needed
@lib/supabase.ts @lib/auth.ts - add logout function

# Bad - loads too much
Look at all my files and... (context overflow)
```

---

## PARALLEL DEVELOPMENT

### Setup Multiple Projects
```bash
# Create workspace structure
mkdir -p app-factory/{scripture-streak,glowup-scanner,faithfit,mealvision,quitnic}

# Initialize each
cd app-factory/scripture-streak && npx create-expo-app@latest . --template tabs
cd ../glowup-scanner && npx create-expo-app@latest . --template tabs
# ... repeat for each
```

### Run Multiple Cursor Windows
1. Open Cursor
2. File → New Window
3. Open different project folder in each window
4. Each window has independent AI context

### Managing Multiple Builds
```
Terminal 1: cd scripture-streak && npx expo start
Terminal 2: cd glowup-scanner && npx expo start --port 8082
Terminal 3: cd faithfit && npx expo start --port 8083
```

---

## TROUBLESHOOTING

### Expo Build Issues
```
# Clear cache and rebuild
npx expo start --clear
rm -rf node_modules && npm install

# iOS specific
cd ios && pod install && cd ..

# Check Expo SDK compatibility
npx expo-doctor
```

### Supabase Connection Issues
```
Common fixes:

1. Check URL format (no trailing slash)
2. Verify anon key is correct
3. Test in Supabase dashboard first
4. Check RLS policies aren't blocking

Debug prompt:
"My Supabase connection returns [error]. Here's my setup: [paste supabase.ts]. What's wrong?"
```

### RevenueCat Issues
```
Common fixes:

1. Verify API key matches platform (iOS vs Android)
2. Check products are set up in RevenueCat dashboard
3. Test with sandbox account
4. Verify entitlements are configured

Debug prompt:
"RevenueCat purchase fails with [error code]. Here's my implementation: [paste code]. How do I fix this?"
```

---

## APP STORE SUBMISSION CHECKLIST

### Before Building for Production
- [ ] Update app.json with correct bundle ID, version
- [ ] Add App Store icon (1024x1024)
- [ ] Add splash screen
- [ ] Set correct permissions in app.json
- [ ] Remove development console.logs

### Build Commands
```bash
# Create production build
eas build --platform ios --profile production

# Submit to App Store
eas submit --platform ios
```

### Common Rejection Reasons & Fixes
| Rejection | Fix |
|-----------|-----|
| No privacy policy | Add link before paywall |
| Price not clear | Show exact price on paywall |
| Spam/duplicate | Differentiate features clearly |
| Bugs/crashes | Test thoroughly on real device |
| Incentivized reviews | Remove any review prompts tied to rewards |

---

## DAILY WORKFLOW

### Morning (Research)
1. Check AppKittie for new trending apps
2. Screenshot interesting paywalls/features
3. Update ideas list

### Build Time
1. Open project in Cursor
2. Set clear goal for session
3. Use prompts from this cheatsheet
4. Test frequently on device

### Pre-Submit
1. Run security audit prompt
2. Test complete user flow
3. Check all text for typos
4. Verify analytics events fire
5. Build and submit

### While Waiting for Review
1. Start next app
2. Prepare marketing content
3. Create social media assets
