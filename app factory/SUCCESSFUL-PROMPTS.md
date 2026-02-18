# Successful Prompts & Agent Playbook

This document captures prompts and techniques that worked successfully for building apps with Cursor AI agents.

---

## 🎯 Core Philosophy

1. **Be specific** - Vague prompts = vague results
2. **Break into chunks** - Don't try to build everything at once
3. **Context is king** - Reference existing files and patterns
4. **Iterate fast** - Test often, fix immediately

---

## 📱 App Building Prompts

### Initial Project Setup
```
Build [APP_NAME] using Expo (React Native) with:
- Expo Router for file-based navigation
- Supabase for authentication and database
- Zustand for state management
- TypeScript throughout

Project structure:
/app - Expo Router screens
/src/lib - Utilities (supabase.ts, store.ts)
/assets - Images and icons

Start by creating package.json with all dependencies, then the core files.
```

### Onboarding Flow (Psychological Conversion)
```
Create a 5-screen onboarding flow that follows the guilt -> hope -> action pattern:

Screen 1: Hook - Big promise with social proof ("Join 50,000+ users")
Screen 2: Question - Make them admit their problem (multiple choice)
Screen 3: Validation - "You're not alone" + statistics
Screen 4: Solution - What the app does (3 bullet points max)
Screen 5: CTA - "Start Your Journey" leading to paywall

Use state-based pagination (NOT FlatList - causes touch issues).
Use Pressable instead of TouchableOpacity for better touch handling.
Add hitSlop to all buttons for larger touch targets.
```

### Hard Paywall Screen
```
Create a paywall screen with:
1. Scarcity header: "🔥 Special Launch Offer"
2. Value stack: List 4-5 benefits with checkmarks
3. Price anchoring: Show crossed-out "regular" price
4. Primary CTA: "$4.99/week - Start Free Trial"
5. Secondary link: "Restore Purchases" 
6. Terms link at bottom

Use RevenueCat for subscription management.
Make the "Start Free Trial" button prominent with gradient background.
```

### Database Setup (Supabase)
```
Create a Supabase SQL migration for [APP_NAME] with:

1. profiles table:
   - id (uuid, references auth.users)
   - created_at, updated_at
   - [app-specific fields]
   - subscription_status (free/trial/active/expired)

2. [main_data] table:
   - id (uuid)
   - user_id (references profiles)
   - [app-specific fields]
   - created_at

3. Enable RLS on all tables
4. Create policies: users can only CRUD their own data
5. Create trigger to auto-create profile on signup
6. Create indexes for common queries

Output as SQL I can run in Supabase SQL Editor.
```

### Fixing Touch/Click Issues
```
The buttons in [SCREEN_NAME] aren't responding to clicks. 

Common fixes to apply:
1. Wrap root layout in GestureHandlerRootView
2. Replace TouchableOpacity with Pressable
3. Remove LinearGradient wrapping (blocks touches)
4. Don't use FlatList for simple lists (use map)
5. Add hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
6. Add zIndex: 100 to button styles
7. Use SafeAreaView instead of View for container
```

---

## 🔧 Debugging Prompts

### App Not Loading
```
The app shows a blank screen / loading spinner forever.

Check:
1. Console logs in Metro terminal
2. Supabase connection (are env vars loaded?)
3. Auth state initialization
4. Navigation guards (infinite redirect loops?)

Add console.log statements at key points to trace the flow.
```

### TypeScript Errors
```
Fix all TypeScript errors in [FILE_PATH].
Ensure proper typing for:
- Component props
- State variables
- API responses
- Navigation params
```

### Dependency Issues
```
I'm getting [ERROR_MESSAGE] when running npm install or expo start.

Steps to fix:
1. Delete node_modules and package-lock.json
2. Clear npm cache: npm cache clean --force
3. Reinstall: npm install --legacy-peer-deps
4. Clear Metro cache: npx expo start --clear
```

---

## 🚀 Deployment Prompts

### Pre-Submission Checklist
```
Review the app for App Store submission:

1. Privacy Policy URL configured in app.json
2. App icons at all required sizes
3. Splash screen configured
4. Bundle ID matches App Store Connect
5. No hardcoded test data
6. All console.log statements removed or conditional
7. Error boundaries in place
8. Offline handling considered
9. Push notification permissions requested properly
10. In-app purchases configured in RevenueCat
```

### EAS Build
```
Configure EAS Build for [APP_NAME]:

1. Create eas.json with development, preview, production profiles
2. Set up credentials (run eas credentials)
3. Configure app.json with:
   - Correct bundleIdentifier
   - Version numbers
   - Required permissions
4. Build: eas build --platform ios --profile production
```

---

## 🔄 Iteration Prompts

### Adding New Feature
```
Add [FEATURE_NAME] to the app:

Requirements:
- [Requirement 1]
- [Requirement 2]

Follow existing patterns in the codebase for:
- File structure
- Component styling
- State management
- API calls

Create/modify these files:
1. [file1] - [description]
2. [file2] - [description]
```

### Refactoring
```
Refactor [COMPONENT/FILE] to:
- Extract reusable components
- Improve type safety
- Follow DRY principles
- Match the existing code style

Don't change functionality, only improve code quality.
```

---

## 📊 Parallel Cursor Development

### Maximum Parallel Agents - DEFINITIVE ANSWER

**Cursor's Architecture:**
- Cursor uses Claude/GPT APIs with rate limiting
- Each "composer" or "agent" session consumes API quota
- The limit is primarily **account-based**, not machine-based

**Practical Limits:**
| Plan | Concurrent Agents | Notes |
|------|------------------|-------|
| Cursor Free | 1 | 50 slow requests/month |
| Cursor Pro ($20/mo) | **2-3** | 500 fast + unlimited slow requests |
| Cursor Business ($40/mo) | **3-5** | Higher limits + team features |
| Multiple Accounts | **Unlimited** | Each account = separate limits |

**The REAL Maximum:**
- **Same account**: 2-3 productive agents (diminishing returns after)
- **Multiple accounts**: As many as you can manage (2-4 accounts = 6-12 agents)
- **API Keys**: If using custom API keys, no Cursor limits apply

### Why More ≠ Better
1. **Human bottleneck**: Can't review 10 agents simultaneously
2. **Context loss**: Agents don't share context between windows
3. **File conflicts**: Multiple agents editing same files = disaster
4. **Quality drops**: More agents = less attention = more bugs

### Best Strategy for Max Output
```bash
# OPTION 1: Two Cursor Pro Accounts (Recommended)
# Account A: Apps 1-3 (rotate through)
# Account B: Apps 4-6 (rotate through)
# Total effective agents: 4-6

# OPTION 2: One account + staged workflow
# Window 1: Build new app
# Window 2: Fix bugs on yesterday's app
# Window 3: Add features to shipped app
# Rotate focus every 1-2 hours

# OPTION 3: Use Cursor + Other AI tools
# Cursor: Primary coding
# Claude/ChatGPT: Research, prompts, docs
# GitHub Copilot: Inline completions
```

### Opening Multiple Cursor Windows
```bash
# macOS - Open multiple workspace windows
open -na "Cursor" --args "/Users/you/projects/app1"
open -na "Cursor" --args "/Users/you/projects/app2"
open -na "Cursor" --args "/Users/you/projects/app3"

# Each window can run its own agent session
# BUT they share the same account limits
```

### Maximizing Single Agent Productivity
Instead of running many agents poorly, optimize ONE agent:
1. **Clear context**: Start fresh chats for new tasks
2. **Batch operations**: Group related files in prompts
3. **Template prompts**: Use proven prompts from this doc
4. **Pre-plan**: Use Plan mode before Agent mode
5. **Incremental**: Build in small, testable chunks

### Recommended Daily Workflow (1 Account)
```
6 AM - 9 AM: Agent builds App A structure
9 AM - 12 PM: Agent adds features to App A
12 PM - 1 PM: YOU test App A, make bug list
1 PM - 4 PM: Agent fixes App A bugs
4 PM - 6 PM: Agent builds App B structure
6 PM: YOU test App B, prepare tomorrow's tasks
```

**Output potential**: 
- 1-2 apps per week with focused attention
- 4-6 apps per month to production quality
- 10+ apps per month if accepting lower polish

---

## 🎨 UI/UX Prompts

### Making UI Beautiful
```
Improve the visual design of [SCREEN_NAME]:

Apply these principles:
1. Dark theme with accent color (#e94560)
2. Generous padding (24-32px)
3. Large touch targets (48px minimum)
4. Clear visual hierarchy
5. Subtle shadows/borders for depth
6. Consistent border radius (16px)
7. Font weights: 400 normal, 600 semi, 800 bold

Don't use:
- Pure black backgrounds (use #1a1a2e)
- Thin fonts
- Small text (min 14px)
- Cluttered layouts
```

### Animation
```
Add subtle animations to [COMPONENT]:

Use React Native Animated or Reanimated:
- Fade in on mount (opacity 0 -> 1, 300ms)
- Scale on press (1 -> 0.98 -> 1)
- Slide transitions between screens

Keep animations under 300ms for snappy feel.
```

---

## 📝 Session Notes Template

Use this to document each build session:

```markdown
## Session: [DATE] - [APP_NAME]

### Goal
[What you're trying to accomplish]

### Prompts Used
1. [Prompt 1] - [Result: Success/Partial/Failed]
2. [Prompt 2] - [Result]

### Issues Encountered
- [Issue 1]: [How it was fixed]
- [Issue 2]: [How it was fixed]

### What Worked Well
- [Thing 1]
- [Thing 2]

### What to Do Differently
- [Improvement 1]
- [Improvement 2]

### Files Changed
- [file1.tsx] - [changes made]
- [file2.ts] - [changes made]

### Next Steps
1. [Task 1]
2. [Task 2]
```

---

## 🔑 Key Learnings

1. **LinearGradient blocks touches** - Don't wrap interactive elements
2. **FlatList is overkill for <10 items** - Use simple map()
3. **Always add GestureHandlerRootView** - Required for RN gesture handling
4. **Pressable > TouchableOpacity** - More reliable touch handling
5. **Test on device early** - Simulator misses many touch issues
6. **Keep prompts focused** - One task per prompt = better results
7. **Reference existing code** - "Follow the pattern in X" works well
8. **Break complex tasks** - Multiple small prompts > one huge prompt

---

## 📱 Session Log: Scripture Streak (Jan 2026)

### What Was Built
- Daily Bible verse app with streak tracking
- 4-screen onboarding flow
- Freemium paywall ($1.99 lifetime / $0.99 monthly)
- Push notification reminders
- Local storage for offline functionality
- Ad banner placeholder (promotes premium)

### Successful Approaches

**1. Local-First Architecture**
```
Build the app to work WITHOUT a database first:
- Use AsyncStorage for user data
- No Supabase required for basic functionality  
- Add cloud sync later if needed
- Reduces complexity and dependencies
```
Why: Works offline, faster to build, no server costs.

**2. Freemium with House Ads**
```
Instead of real AdMob ads, use "house ads":
- Show promotional banner for premium
- "Upgrade to remove ads - $1.99"
- Taps go to paywall, not external ads
- Better conversion than real ads
- No ad network taking 30-40% cut
```
Why: Better UX, higher conversion, simpler integration.

**3. Removing Fake Testimonials**
```
DON'T use fake testimonials. Apple will reject.

Instead use:
- Generic social proof: "Loved by believers worldwide"
- Stats: "1000+ daily verses delivered"
- Feature benefits, not fake reviews
```
Why: Apple Guidelines 5.6.1 prohibits fake reviews.

**4. RevenueCat Requires Apple Developer Account**
```
To use RevenueCat, you MUST have:
1. Apple Developer Account ($99/year)
2. App created in App Store Connect
3. In-App Purchase Key (P8 file)

Without this, purchases won't work.
The app can still function with a "Demo Mode".
```

### Issues & Fixes

| Issue | Fix |
|-------|-----|
| Onboarding buttons not responding | Removed FlatList, used state-based slides |
| SafeAreaView deprecation | Use from 'react-native-safe-area-context' |
| Touch events blocked | Added GestureHandlerRootView wrapper |
| Missing tab layout | File was accidentally deleted, recreated |
| Tasks not completable | Added local state fallback for non-auth users |

### What Supabase IS and ISN'T Needed For

**NOT NEEDED:**
- Local streak tracking
- Storing daily check-ins
- User preferences
- Basic app functionality

**NEEDED ONLY IF:**
- Cross-device sync
- User accounts
- Leaderboards
- Server-side verification

### Final Stack (Simplified)

```
Scripture Streak Tech Stack:
├── Expo + React Native (frontend)
├── Expo Router (navigation)
├── AsyncStorage (local data)
├── RevenueCat (payments - optional until ready)
├── Expo Notifications (reminders)
└── Zustand (state management)

NO server required for MVP!
```

### Time to Build
- Initial working app: ~4 hours
- Fixing touch issues: ~2 hours
- Adding features (notifications, settings): ~2 hours
- RevenueCat setup: ~30 min (requires Apple Dev account)
- **Total: ~8 hours to production-ready**

---

## 🎯 Quick Reference: What You Actually Need

| Feature | Do You Need a Server? | Service |
|---------|----------------------|---------|
| User data storage | NO - use AsyncStorage | Local |
| Streak tracking | NO - use AsyncStorage | Local |
| Push notifications | NO - Expo handles it | Expo |
| In-app purchases | SORT OF - RevenueCat | RevenueCat (free) |
| User accounts | OPTIONAL - Supabase | Supabase (free tier) |
| Analytics | OPTIONAL | PostHog/Mixpanel |

### Bottom Line
**You do NOT need a Hetzner server or Supabase for simple apps.**
Only add backend complexity when you actually need:
- User accounts
- Cross-device sync
- Server-side logic
