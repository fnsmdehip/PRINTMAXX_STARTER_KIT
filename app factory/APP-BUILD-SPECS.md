# APP FACTORY: BUILD SPECIFICATIONS

## Quick Reference

| App | Model | Niche Overlay | Est. Revenue | Build Time | Complexity |
|-----|-------|---------------|--------------|------------|------------|
| 1. Scripture Streak | Follow Jesus | Christian | $50-200K/mo | 1 week | Low |
| 2. GlowUp Scanner | UMAX | Looksmaxxing | $50-150K/mo | 2 weeks | Medium |
| 3. FaithFit | Habit Tracker | Christian + Fitness | $10-50K/mo | 1 week | Low |
| 4. MealVision | Cal AI | Health/Keto/Carnivore | $20-80K/mo | 2 weeks | Medium |
| 5. QuitNic | Puff Count | Addiction Recovery | $15-40K/mo | 1 week | Low |
| 6. Prayer Partner AI | AI Companion | Christian | $10-30K/mo | 1-2 weeks | Medium |
| 7. StyleMax | UMAX | Women's Beauty | $30-100K/mo | 2 weeks | Medium |
| 8. Devotion Duo | Lovelee | Christian Couples | $5-20K/mo | 1 week | Low |

---

## TECH STACK (Standard for All Apps)

### Core Stack
```
Framework: Expo (React Native) - Ships iOS + Android from one codebase
Backend: Supabase ($25/mo) - Auth + Database + Storage + Edge Functions
Payments: RevenueCat (free up to $2.5K MTR) - Handles subscriptions
Analytics: Mixpanel or Amplitude (free tier)
Push Notifications: Expo Push + OneSignal
```

### AI Integration (for photo analysis apps)
```
Primary: OpenAI GPT-4 Vision API ($0.01-0.03 per image)
Alternative: Claude Vision API
Fallback: Replicate (for custom models)
```

### Recommended Project Structure
```
app/
├── (tabs)/                 # Tab navigation screens
│   ├── index.tsx          # Home/Main feature
│   ├── progress.tsx       # Tracking/Stats
│   └── settings.tsx       # Settings + Account
├── (auth)/                # Auth screens
│   ├── login.tsx
│   ├── signup.tsx
│   └── onboarding.tsx
├── paywall.tsx            # Hard paywall screen
├── _layout.tsx            # Root layout
components/
├── ui/                    # Reusable UI components
├── features/              # Feature-specific components
lib/
├── supabase.ts           # Supabase client
├── revenuecat.ts         # RevenueCat setup
├── openai.ts             # AI API calls
├── analytics.ts          # Event tracking
hooks/
├── useAuth.ts
├── useSubscription.ts
├── useStreak.ts
constants/
├── paywall.ts            # Pricing, trial length
├── prompts.ts            # AI system prompts
```

---

## SECURITY CHECKLIST (Run Before Every Submission)

### Critical (Will Get You Rejected or Hacked)
- [ ] **NO hardcoded API keys** in source code - use environment variables
- [ ] **Supabase Row Level Security (RLS)** enabled on all tables
- [ ] **Validate all user inputs** - never trust client data
- [ ] **HTTPS only** - no HTTP calls anywhere
- [ ] **Authentication on all API routes** - check session before operations

### Important (Security Best Practices)
- [ ] API keys stored in secure storage (expo-secure-store)
- [ ] Rate limiting on API calls
- [ ] Input sanitization on all text fields
- [ ] No sensitive data in console.log (remove before production)
- [ ] Proper error handling - don't expose stack traces to users

### AI-Generated Code Specific
- [ ] Review all database queries for SQL injection
- [ ] Check for exposed endpoints (test with Postman)
- [ ] Verify authentication flow manually
- [ ] Test paywall bypass attempts
- [ ] Audit file upload functionality if present

### Pre-Submission Security Scan
```bash
# Run these before submitting to App Store:

# 1. Search for hardcoded secrets
grep -r "sk-" --include="*.ts" --include="*.tsx" .
grep -r "supabase" --include="*.ts" --include="*.tsx" . | grep -i "key\|secret"
grep -r "api_key\|apiKey\|API_KEY" --include="*.ts" --include="*.tsx" .

# 2. Check for console.log statements
grep -r "console.log" --include="*.ts" --include="*.tsx" . | wc -l

# 3. Run Semgrep (if installed)
semgrep --config=auto .
```

---

## APP #1: SCRIPTURE STREAK (Follow Jesus Clone)

### The Model
**Proven Revenue:** Follow Jesus did $138.6K in 5 DAYS
**Psychological Trigger:** Faithful → Certainty + Guilt about not being "good enough"
**Why It Works:** Guilt-driven content + gamification + built-in viral sharing

### Core Features (MVP)
1. **Daily Verse** - Morning push notification with scripture
2. **Streak Tracking** - Gamified daily check-ins (read, pray, share)
3. **Share to Social** - One-tap share verse image to Instagram/TikTok
4. **Progress Stats** - Verses read, prayer minutes, sharing streak
5. **Hard Paywall** - After onboarding, before any features

### Onboarding Flow (Critical for Conversion)
```
Screen 1: "Transform Your Spiritual Life"
         - Emotional imagery, person praying
         
Screen 2: "How often do you read your Bible?"
         - Multiple choice: Daily / Few times a week / Rarely / Never
         - This creates GUILT if they answer poorly
         
Screen 3: "You're not alone. 73% of Christians struggle with consistency"
         - Social proof + validation of their guilt
         
Screen 4: "Scripture Streak helps you build an unbreakable habit"
         - Show the solution
         
Screen 5: PAYWALL
         - $4.99/week with 3-day free trial
         - "Start Your Journey" CTA
```

### Paywall Copy
```
UNLOCK YOUR SPIRITUAL POTENTIAL

✓ Daily personalized scripture
✓ Guided prayer sessions  
✓ Track your spiritual growth
✓ Share your faith journey
✓ Join 50,000+ believers

[Start 3-Day Free Trial]
Then $4.99/week. Cancel anytime.

"This app changed my prayer life" - Sarah M. ⭐⭐⭐⭐⭐
```

### Database Schema (Supabase)
```sql
-- Users table (extends Supabase auth.users)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  streak_count INTEGER DEFAULT 0,
  last_check_in DATE,
  total_verses_read INTEGER DEFAULT 0,
  total_shares INTEGER DEFAULT 0,
  subscription_status TEXT DEFAULT 'free'
);

-- Daily check-ins
CREATE TABLE check_ins (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id),
  date DATE DEFAULT CURRENT_DATE,
  read_verse BOOLEAN DEFAULT FALSE,
  prayed BOOLEAN DEFAULT FALSE,
  shared BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE check_ins ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);
  
CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);
```

### Build Prompt (For Cursor)
```
Build a React Native app using Expo with the following:

STACK:
- Expo Router for navigation
- Supabase for auth and database
- RevenueCat for subscriptions
- Expo Notifications for push

SCREENS:
1. Onboarding flow (5 screens with guilt-building questions)
2. Hard paywall with $4.99/week subscription
3. Home screen with daily verse and check-in buttons
4. Progress screen with streak counter and stats
5. Settings with account management

FEATURES:
- Daily verse from API (use Bible API or static JSON)
- Streak tracking that resets if user misses a day
- Share button that creates an image with the verse and shares to social
- Push notification at 7am with daily verse
- Confetti animation when completing daily check-in

MONETIZATION:
- Hard paywall after onboarding
- 3-day free trial with RevenueCat
- Weekly subscription at $4.99

SECURITY:
- All API keys in environment variables
- Supabase RLS enabled
- Input validation on all fields
```

### Monetization Add-Ons
- **Info Product Funnel:** "The 30-Day Bible Challenge" ebook ($19.99)
- **Affiliate:** Christian book recommendations (Amazon Associates)
- **Upsell:** Premium tier with audio devotionals ($9.99/week)

---

## APP #2: GLOWUP SCANNER (UMAX Clone)

### The Model
**Proven Revenue:** UMAX does $350-500K/month
**Psychological Trigger:** Men → Lust/Status + Young → Status
**Why It Works:** Users share their "scores" on TikTok = free viral marketing

### Core Features (MVP)
1. **Face Scan** - Take photo → AI analyzes facial features
2. **Rating System** - Overall score + breakdown (jawline, symmetry, etc.)
3. **Improvement Tips** - Personalized advice based on analysis
4. **Progress Tracking** - Before/after comparisons
5. **Shareable Results** - Generate image with score for social media

### AI Analysis Prompt (GPT-4 Vision)
```
You are a facial aesthetics analyzer. Analyze this face photo and provide:

1. OVERALL_SCORE: Rate 1-10 based on conventional attractiveness standards
2. BREAKDOWN scores (1-10 each):
   - jawline_definition
   - facial_symmetry
   - eye_area (canthal tilt, eye shape)
   - cheekbone_prominence
   - skin_quality
   - facial_harmony
   
3. TOP_3_STRENGTHS: List the person's best features

4. TOP_3_IMPROVEMENTS: Actionable advice for improvement
   - Be specific (e.g., "mewing exercises for jawline")
   - Reference looksmaxxing terminology users expect
   
5. POTENTIAL_SCORE: What they could achieve with improvements (1-10)

Return as JSON:
{
  "overall_score": 7.2,
  "breakdown": {
    "jawline_definition": 6,
    "facial_symmetry": 8,
    ...
  },
  "strengths": ["Strong brow ridge", ...],
  "improvements": ["Practice mewing for jaw definition", ...],
  "potential_score": 8.5
}

Be encouraging but honest. Users want real feedback, not flattery.
```

### Onboarding Flow
```
Screen 1: "Unlock Your True Potential"
         - Before/after transformation imagery
         
Screen 2: "What's your goal?"
         - Better dating life / More confidence / Career success / General improvement
         
Screen 3: "Most guys have no idea how they actually look to others"
         - Statistics about attractiveness blind spots
         
Screen 4: "Our AI analyzes 20+ facial features used by surgeons and models"
         - Scientific credibility
         
Screen 5: PAYWALL
         - $6.99/week with 3-day free trial
```

### Database Schema
```sql
CREATE TABLE scans (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users,
  image_url TEXT NOT NULL,
  overall_score DECIMAL(3,1),
  breakdown JSONB,
  strengths TEXT[],
  improvements TEXT[],
  potential_score DECIMAL(3,1),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  total_scans INTEGER DEFAULT 0,
  highest_score DECIMAL(3,1),
  subscription_status TEXT DEFAULT 'free'
);
```

### Build Prompt (For Cursor)
```
Build a looksmaxxing face analysis app with Expo:

STACK:
- Expo Router, Expo Camera, Expo Image Picker
- Supabase for auth, database, and image storage
- OpenAI GPT-4 Vision API for face analysis
- RevenueCat for subscriptions

FLOW:
1. User takes selfie or uploads photo
2. Photo sent to GPT-4 Vision with analysis prompt
3. Results displayed with animated score reveal
4. Breakdown shown with gauge charts
5. Tips displayed with expandable cards
6. Share button generates branded result image

SCREENS:
1. Onboarding (5 screens building desire)
2. Hard paywall ($6.99/week)
3. Camera/upload screen
4. Analysis loading screen with scanning animation
5. Results screen with score, breakdown, and tips
6. History screen showing past scans
7. Progress screen comparing scans over time

IMPORTANT:
- Score reveal should be dramatic (count up animation)
- Share image must include app branding and download link
- Cache analysis results to avoid re-calling API
- Limit free users to 1 scan, paywall blocks second

SECURITY:
- Store images in Supabase Storage with user-only access
- Never expose OpenAI API key to client
- Use Supabase Edge Function for AI calls
```

### Monetization Add-Ons
- **Affiliate:** Skincare products, supplements (jawline gum, collagen)
- **Info Product:** "The Complete Looksmaxxing Guide" ($29-49)
- **Upsell:** Unlimited scans + personalized routine ($14.99/week)
- **Twitter Account:** Build @GlowUpScanner posting transformation content → funnel to app

---

## APP #3: FAITHFIT (Christian Fitness Habit Tracker)

### The Model
**Proven Revenue:** Habit trackers do $5-30K/mo consistently
**Psychological Trigger:** Faithful + Healthy → Certainty + Fear
**Why It Works:** Christian niche has high willingness to pay + fitness is evergreen

### Core Features (MVP)
1. **Faith Habits** - Bible reading, prayer, church attendance tracking
2. **Fitness Habits** - Workouts, water intake, steps
3. **Unified Dashboard** - "Body & Spirit" score
4. **Daily Devotional** - Short scripture + reflection tied to fitness
5. **Community Accountability** - Optional sharing with prayer partners

### Sample Devotional Content
```
DAY 1: "Your Body is a Temple"

"Do you not know that your bodies are temples of the Holy Spirit?"
- 1 Corinthians 6:19

Today's Reflection:
God gave you this body as a gift. Caring for it through exercise 
and discipline is an act of worship. When you feel like quitting 
your workout, remember: you're honoring the One who created you.

Today's Challenge:
✓ 30 minutes of movement (any kind)
✓ Read 1 Corinthians 6:19-20
✓ Pray for strength and discipline
```

### Onboarding Flow
```
Screen 1: "Honor God with Your Body AND Spirit"
         - Image of fit person in prayer pose
         
Screen 2: "Which area needs the most work?"
         - Spiritual discipline / Physical health / Both equally
         
Screen 3: "Christians who track both see 3x better results"
         - Social proof statistic
         
Screen 4: "Build habits that honor God"
         - Feature preview
         
Screen 5: PAYWALL ($4.99/week)
```

### Build Prompt (For Cursor)
```
Build a Christian fitness habit tracking app:

STACK:
- Expo Router, Expo Notifications
- Supabase for auth and data
- RevenueCat for subscriptions
- HealthKit/Google Fit integration for step tracking

FEATURES:
1. Two habit categories: Faith (Bible, prayer, church) and Fitness (workout, water, steps)
2. Daily check-in screen with all habits as toggleable cards
3. Combined "Temple Score" (average of faith + fitness completion)
4. Streak counter that motivates consistency
5. Daily devotional that connects faith to fitness
6. Weekly summary email/push notification

SCREENS:
1. Onboarding (4 screens)
2. Hard paywall
3. Today view with all habits
4. Stats/progress view
5. Devotional reader
6. Settings

GAMIFICATION:
- Streaks with milestone badges (7 days, 30 days, 100 days)
- "Temple Score" percentage displayed prominently
- Confetti on completing all daily habits

MONETIZATION:
- Hard paywall at $4.99/week after onboarding
- Include "Share Progress" feature for viral loop
```

---

## APP #4: MEALVISION (Cal AI Clone - Niche Diet Version)

### The Model
**Proven Revenue:** Cal AI does $300K+/month
**Psychological Trigger:** Healthy → Fear + Everyone → Time
**Why It Works:** Photo-based = zero friction, AI makes it feel magical

### Niche Angle Options
Choose ONE for differentiation:
1. **Carnivore AI** - Meat-focused, tracks protein/fat, no carbs
2. **Keto Vision** - Tracks net carbs, ketone-friendly suggestions
3. **Vegan Scan** - Plant-based, tracks protein sources, B12, iron
4. **Macro King** - Bodybuilder-focused, protein-first tracking

### Core Features (MVP)
1. **Photo Analysis** - Snap meal → get calories, protein, fat, carbs
2. **Daily Tracking** - Running totals with goal progress
3. **Meal History** - Scroll through past meals with photos
4. **Goal Setting** - Set macro targets based on diet type
5. **Streaks** - Track logging consistency

### AI Analysis Prompt (GPT-4 Vision)
```
You are a nutrition analysis AI specialized in [CARNIVORE/KETO/VEGAN] diets.

Analyze this food photo and provide:

1. FOOD_ITEMS: List each identifiable food item
2. PORTION_ESTIMATE: Estimated portion size for each
3. NUTRITION (total for entire meal):
   - calories
   - protein_g
   - fat_g  
   - carbs_g (net carbs for keto)
   - [diet-specific]: ketone impact / protein quality / iron content
   
4. DIET_SCORE: How well this meal fits [DIET TYPE] (1-10)
5. SUGGESTION: One tip to make this meal better for the diet

Return as JSON with confidence scores where uncertain.
Be conservative with calorie estimates - users prefer accuracy over flattery.
```

### Build Prompt (For Cursor)
```
Build a photo-based calorie tracking app for [CARNIVORE/KETO/VEGAN] diet:

STACK:
- Expo Router, Expo Camera, Expo Image Picker
- Supabase for auth, database, image storage
- OpenAI GPT-4 Vision for food analysis
- RevenueCat for subscriptions

FLOW:
1. User opens app → camera ready
2. Take photo of meal
3. AI analyzes → shows nutrition breakdown
4. User confirms or edits values
5. Saved to daily log

SCREENS:
1. Quick onboarding (diet type, goals)
2. Hard paywall ($5.99/week)
3. Camera screen (main view)
4. Analysis results with edit capability
5. Daily log with running totals
6. History/calendar view
7. Stats and streaks

KEY UX:
- Camera should open FAST (under 1 second)
- Analysis should show loading animation
- Results should be editable (users want control)
- Daily totals prominently displayed

MONETIZATION:
- Hard paywall after onboarding
- Free users get 3 scans, then paywall
- Premium: unlimited scans + AI meal suggestions
```

### Monetization Add-Ons
- **Affiliate:** Diet-specific supplements (carnivore: organ supplements, keto: MCT oil)
- **Info Product:** "[Diet] Meal Plan Guide" ($19.99)
- **Upsell:** AI meal planning + grocery lists ($9.99/week)

---

## APP #5: QUITNIC (Puff Count Clone)

### The Model
**Proven Revenue:** Puff Count hit $44K MRR, sold for exit
**Psychological Trigger:** Sick → Miracles + Everyone → Time
**Why It Works:** Anti-vaping content goes viral on TikTok, clear pain point

### Core Features (MVP)
1. **Quit Timer** - Days, hours, minutes since last use
2. **Money Saved** - Calculate savings based on usage
3. **Health Timeline** - Show body recovery milestones
4. **Craving Logger** - Track and beat cravings
5. **Streak Protection** - Emergency motivation when tempted

### Health Recovery Timeline (Key Feature)
```
20 MINUTES: Heart rate returns to normal
8 HOURS: Nicotine levels drop 50%
24 HOURS: Carbon monoxide eliminated
48 HOURS: Taste and smell improve
72 HOURS: Breathing becomes easier
2 WEEKS: Circulation improves
1 MONTH: Lung function increases 30%
3 MONTHS: Coughing and shortness of breath decrease
1 YEAR: Heart disease risk drops 50%
```

### Onboarding Flow
```
Screen 1: "Your Lungs Are Begging You to Quit"
         - Stark health imagery
         
Screen 2: "How much do you spend on vaping per week?"
         - Slider: $10 - $100+
         - Shows annual cost in real-time
         
Screen 3: "In 1 year, you could save $[X] and add years to your life"
         - Personalized calculation
         
Screen 4: "Join 100,000+ people who quit with QuitNic"
         - Social proof
         
Screen 5: PAYWALL ($4.99/week)
```

### Build Prompt (For Cursor)
```
Build a quit vaping/nicotine tracking app:

STACK:
- Expo Router, Expo Notifications
- Supabase for auth and data
- RevenueCat for subscriptions
- Local storage for offline quit timer

CORE FEATURE:
The quit timer must work offline and be accurate to the second.
This is THE most important feature - users check this constantly.

SCREENS:
1. Onboarding with cost calculator
2. Hard paywall
3. Main dashboard with:
   - Giant quit timer (days/hours/minutes)
   - Money saved counter (animated)
   - Current health milestone with progress bar
4. Health timeline (all milestones with unlock animations)
5. Craving SOS button (quick tips, breathing exercise, motivation)
6. Stats (cravings beaten, money saved over time)

NOTIFICATIONS:
- Milestone achieved: "24 hours! Your body is eliminating carbon monoxide 🎉"
- Daily motivation: "Day X: You've saved $Y and your lungs are healing"
- Craving check-in: "How are you feeling today?"

GAMIFICATION:
- Badge system for milestones
- Streak counter with fire emoji
- Share milestone achievements

MONETIZATION:
- Hard paywall at $4.99/week
- Include social share for viral potential
```

---

## APP #6: PRAYER PARTNER AI (AI Companion - Christian)

### The Model
**Proven Revenue:** AI companions do $120M+ market, $1.18 revenue per download
**Psychological Trigger:** Faithful → Certainty + Lonely → Belonging
**Why It Works:** Combines trending AI companion format with high-paying Christian niche

### Core Features (MVP)
1. **AI Prayer Companion** - Chat-based prayer partner
2. **Guided Prayers** - AI leads through prayer types (gratitude, confession, petition)
3. **Scripture Integration** - AI references relevant Bible verses
4. **Prayer Journal** - Logged prayers with AI-generated summaries
5. **Prayer Reminders** - Scheduled prayer times

### AI System Prompt
```
You are a compassionate Christian prayer companion named Grace. Your role is to:

1. LISTEN with empathy to whatever the user shares
2. GUIDE them in prayer appropriate to their situation
3. REFERENCE scripture that's relevant and encouraging
4. NEVER judge or condemn - only show God's love
5. KEEP responses warm, personal, and conversational

Prayer styles you can lead:
- Gratitude prayers: Help them thank God for blessings
- Petition prayers: Help them ask God for needs
- Confession prayers: Gently guide through repentance
- Intercession: Pray for others together
- Praise: Focus on God's attributes

Always end interactions with hope and encouragement.
Use "we" language: "Let's pray together..."
Keep responses concise - 2-3 paragraphs max.
```

### Build Prompt (For Cursor)
```
Build a Christian AI prayer companion app:

STACK:
- Expo Router
- OpenAI GPT-4 API for chat
- Supabase for auth and prayer journal storage
- RevenueCat for subscriptions

SCREENS:
1. Onboarding (establish personal prayer struggles)
2. Hard paywall ($5.99/week)
3. Chat interface (main screen)
4. Prayer journal (past conversations summarized)
5. Guided prayer modes (gratitude, petition, confession)
6. Settings with prayer time reminders

CHAT UX:
- Typing indicator while AI responds
- Message bubbles (user on right, AI on left)
- Quick-reply suggestions for common responses
- "Pray Together" button that initiates guided prayer

KEY FEATURES:
- AI remembers context within conversation
- Save "prayer highlights" to journal
- Daily prayer streak tracking
- Morning/evening prayer reminders

IMPORTANT:
- AI must NEVER give harmful advice
- Include content safety layer
- Responses should feel warm, not robotic
- Always include scriptural encouragement
```

---

## APP #7: STYLEMAX (UMAX for Women)

### The Model
**Proven Revenue:** UMAX model but for women = underserved market
**Psychological Trigger:** Women → Beauty + Young → Status
**Why It Works:** Women spend more on beauty, no good female version of UMAX

### Core Features (MVP)
1. **Face Analysis** - Skin quality, facial harmony, features analysis
2. **Style Recommendations** - AI suggests colors, styles that suit their features
3. **Skincare Routine** - Personalized product type recommendations
4. **Glow Score** - Overall rating with breakdown
5. **Progress Tracking** - See improvement over time

### AI Analysis Prompt (GPT-4 Vision)
```
You are a beauty and style AI advisor for women. Analyze this face photo and provide:

1. GLOW_SCORE: Overall rating 1-10 based on skin health, harmony, and natural beauty
2. SKIN_ANALYSIS:
   - skin_type: oily/dry/combination/normal
   - skin_concerns: [list any visible concerns]
   - skin_score: 1-10
3. FEATURE_HIGHLIGHTS:
   - List 3 best natural features to enhance
4. COLOR_ANALYSIS:
   - season: warm/cool/neutral
   - best_colors: [5 colors that would complement]
   - avoid_colors: [colors to minimize]
5. STYLE_SUGGESTIONS:
   - makeup_style: natural/glam/bold that suits them
   - hair_suggestions: based on face shape
3. SKINCARE_PRIORITIES:
   - Top 3 product types to focus on
   
Return as JSON. Be empowering and positive - focus on enhancement, not fixing flaws.
```

### Build Prompt (For Cursor)
```
Build a women's beauty analysis app (UMAX for women):

STACK:
- Expo Router, Expo Camera, Expo Image Picker
- OpenAI GPT-4 Vision for analysis
- Supabase for auth and data
- RevenueCat for subscriptions

AESTHETIC:
- Feminine, elegant design (think rose gold, soft pinks, cream)
- Clean typography, lots of white space
- Smooth animations, not harsh transitions

SCREENS:
1. Onboarding focused on "discovering your unique beauty"
2. Hard paywall ($6.99/week)
3. Camera/upload screen
4. Analysis results:
   - Glow Score (animated reveal)
   - Skin analysis tab
   - Color palette tab  
   - Style suggestions tab
5. Progress tracking
6. Saved analyses

UNIQUE FEATURES:
- "Best Colors" palette user can screenshot/save
- Skincare routine builder based on analysis
- Shareable result card with Glow Score

MONETIZATION:
- Hard paywall
- Affiliate: Link to recommended skincare products (Sephora, Ulta affiliates)
- Upsell: Personalized skincare routine ($9.99/week)
```

---

## APP #8: DEVOTION DUO (Christian Couples App)

### The Model
**Proven Revenue:** Lovelee couples app model + Christian niche
**Psychological Trigger:** Faithful + Lonely → Certainty + Belonging
**Why It Works:** Christian couples = high willingness to pay, church distribution channel

### Core Features (MVP)
1. **Shared Devotional** - Daily reading both partners see
2. **Prayer Requests** - Share and pray for each other
3. **Love Notes** - Send encouraging messages
4. **Date Ideas** - Faith-centered date suggestions
5. **Anniversary/Milestone Tracking**

### Build Prompt (For Cursor)
```
Build a Christian couples devotional app:

STACK:
- Expo Router
- Supabase for auth, real-time sync between partners
- RevenueCat for subscriptions
- Expo Notifications

PAIRING FLOW:
1. User 1 creates account, gets unique couple code
2. User 1 shares code with partner
3. User 2 enters code to link accounts
4. Both now see shared content

SCREENS:
1. Onboarding (relationship status, how long together)
2. Pairing screen (create/join couple)
3. Hard paywall ($4.99/week)
4. Home: Today's devotional + partner activity
5. Prayer board (shared prayer requests)
6. Love notes (like messaging but special)
7. Date ideas generator

SYNC FEATURES:
- Real-time: When one marks devotional complete, other sees
- Notifications when partner sends prayer request or love note
- "Praying for you" reaction on prayer requests

CONTENT:
- 365 daily devotionals for couples
- Discussion questions for each day
- Weekly date night suggestions
```

---

## PARALLEL DEVELOPMENT STRATEGY

### Running Multiple Cursor Agents

**Current Limitations:**
- Cursor doesn't have official parallel agent support
- Workaround: Open multiple Cursor windows, each with different project folder
- Each window = independent agent session

**Recommended Approach:**
```
1. Create separate folders for each app:
   /app-factory/
   ├── scripture-streak/
   ├── glowup-scanner/
   ├── faithfit/
   ├── mealvision/
   └── ...

2. Open each folder in separate Cursor window
3. Start builds in parallel
4. Context limit management:
   - Start fresh chat when context gets long
   - Reference specific files, don't re-paste entire codebase
   - Use @file mentions to load specific files
```

### Build Order (Optimized for Learning + Revenue)

**Phase 1 (Week 1):** Build 2 simple apps
- Scripture Streak (simplest, proven model)
- QuitNic (simple, clear mechanics)

**Phase 2 (Week 2):** Build 2 AI-powered apps  
- GlowUp Scanner (learn GPT-4 Vision integration)
- MealVision (same pattern, different niche)

**Phase 3 (Week 3):** Build remaining
- FaithFit, Prayer Partner AI, StyleMax, Devotion Duo

**Submit as you complete** - don't wait for all apps to be done.

---

## COMMON CURSOR PROMPTS

### Starting a New App
```
Create a new Expo app with:
- Expo Router (file-based routing)
- TypeScript
- Supabase integration (auth + database)
- RevenueCat for subscriptions
- NativeWind for styling (Tailwind CSS)

Project structure should follow best practices with:
- app/ folder for screens using Expo Router
- components/ for reusable UI
- lib/ for API clients and utilities
- hooks/ for custom React hooks
- constants/ for config values

Start with a basic auth flow (sign up, sign in, forgot password) 
and a tab navigator with Home, Progress, and Settings tabs.
```

### Adding Paywall
```
Add a hard paywall screen to this app:

Requirements:
- Shows after onboarding, before any features
- Displays pricing: $X.XX/week with 3-day free trial
- Lists 4-5 key benefits with checkmarks
- Has prominent CTA button
- Shows social proof (review quote + star rating)
- "Restore Purchases" link at bottom
- Integrates with RevenueCat for purchase handling

Design should be clean, high-converting, with:
- Gradient or attractive background
- Clear price display
- Urgency without being scammy
```

### Security Audit Prompt
```
Audit this codebase for security issues:

Check for:
1. Hardcoded API keys or secrets
2. Missing input validation
3. SQL injection vulnerabilities
4. Missing authentication on routes
5. Exposed sensitive data in logs
6. Insecure storage of tokens
7. Missing HTTPS enforcement
8. Improper error handling exposing internals

For each issue found:
- Explain the vulnerability
- Show the affected code
- Provide the fix

Also check that Supabase RLS policies are properly configured.
```

### Pre-Submission Checklist Prompt
```
Prepare this app for App Store submission:

1. Remove all console.log statements
2. Verify all API keys are in environment variables
3. Add proper error handling with user-friendly messages
4. Ensure privacy policy link is visible before paywall
5. Verify terms of service are accessible
6. Check that subscription pricing is clearly displayed
7. Test that restore purchases works
8. Verify deep links work correctly
9. Check all images are optimized
10. Run through onboarding flow manually

Generate a summary of changes made.
```

---

## MONETIZATION ARCHITECTURE

### In-App Revenue Stack
```
Primary: Weekly subscription ($4.99-9.99/week)
  ↓ RevenueCat handles
  
Secondary: Affiliate links
  ↓ Amazon Associates, supplement brands
  ↓ Track clicks with UTM parameters
  
Tertiary: Info product upsells
  ↓ Link to Gumroad/Whop products
  ↓ "Want to go deeper? Get the complete guide"
```

### Apple's Rules on External Links
**What's Allowed:**
- Links to your website (must not have better pricing)
- Affiliate links to physical products (supplements, books)
- Links to info products sold elsewhere (but can't advertise in-app purchase alternative)

**What's NOT Allowed:**
- Directing users to cheaper subscription elsewhere
- "Reader" app exceptions (like Netflix) don't apply to most apps
- Advertising that purchases can be made outside the app

**Safe Pattern:**
```
In looks/fitness apps:
"Recommended Products" section → Amazon affiliate links to supplements

In faith apps:
"Recommended Reading" section → Amazon affiliate links to books

Info products:
Twitter/Instagram bio → Gumroad link
NOT directly in the app (gray area, risky)
```

### Funnel Architecture

```
                     TIKTOK/INSTAGRAM
                           |
            [Viral content with app CTA]
                           |
                       APP STORE
                           |
                    [App Download]
                           |
                      ONBOARDING
                           |
                  [Build investment]
                           |
                    HARD PAYWALL
                           |
              [Weekly subscription $4.99-9.99]
                           |
                     APP USAGE
                    /         \
           [In-app]           [External]
               |                   |
        Affiliate links      Twitter/IG Follow
               |                   |
        Physical products    Info product sales
        (Amazon)             (Gumroad/Whop)
                                   |
                            [Upsell to course/coaching]
```

---

## NEXT STEPS

1. **Pick first app** from the list (recommend Scripture Streak)
2. **Create project folder** in this workspace
3. **Use the Build Prompt** to start development
4. **Run Security Audit** before submission
5. **Submit to App Store** (budget 5-7 attempts)
6. **Start next app** while waiting for review

Ready to start building. Which app first?
