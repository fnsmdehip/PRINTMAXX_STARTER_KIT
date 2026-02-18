# DailyAnchor App Technical Specification

**Last updated:** 2026-01-20
**Status:** MVP specification

---

## Overview

DailyAnchor is a daily devotional mobile app with streak tracking. Users read a short scripture passage, reflection, and prayer prompt each day. Churches can track engagement and upload custom content.

Core components:
1. Mobile app (iOS + Android)
2. Daily devotional content system
3. Streak and engagement tracking
4. Church dashboard
5. Custom content upload
6. Group reading plans

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                            │
├─────────────────────────────────────────────────────────────┤
│  iOS App          │   Android App      │   Church Dashboard │
│  (React Native)   │   (React Native)   │   (Next.js)        │
└────────┬──────────┴─────────┬──────────┴─────────┬──────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Layer                              │
├─────────────────────────────────────────────────────────────┤
│  FastAPI / Python                                           │
│  - /devotionals (daily content)                             │
│  - /streaks (tracking)                                      │
│  - /plans (reading plans)                                   │
│  - /churches (dashboard data)                               │
│  - /auth (JWT + magic links)                                │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                            │
├─────────────┬────────────────┬──────────────────────────────┤
│   Content   │   Engagement   │   Notification               │
│   Manager   │   Tracker      │   Service                    │
│   (Daily    │   (Streaks,    │   (Push, Email)              │
│   content,  │   completions, │                              │
│   plans)    │   analytics)   │                              │
└─────────────┴────────────────┴──────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
├─────────────┬────────────────┬──────────────────────────────┤
│   Postgres  │   Redis        │   S3/R2                      │
│   (Users,   │   (Streak      │   (Audio files,              │
│   churches, │   cache,       │   uploaded content)          │
│   content,  │   sessions)    │                              │
│   plans)    │                │                              │
└─────────────┴────────────────┴──────────────────────────────┘
```

---

## Tech stack

### Mobile app
- **Framework:** React Native + Expo
- **State:** Zustand
- **Navigation:** React Navigation
- **Offline:** WatermelonDB (local SQLite)
- **Audio:** Expo AV
- **Notifications:** Expo Notifications + OneSignal

### Backend
- **Runtime:** Python 3.11
- **Framework:** FastAPI
- **Database:** Supabase Postgres
- **Cache:** Upstash Redis
- **File storage:** Cloudflare R2
- **Notifications:** OneSignal

### Church dashboard
- **Framework:** Next.js 14
- **Styling:** Tailwind CSS
- **Components:** Shadcn/ui
- **Charts:** Recharts

### Infrastructure
- **Backend hosting:** Railway
- **Dashboard hosting:** Vercel
- **App distribution:** App Store, Google Play
- **CDN:** Cloudflare

### Cost estimate (0-10000 users)
| Service | Free tier | Paid tier |
|---------|-----------|-----------|
| Railway | $5/month | $20/month |
| Vercel | Free | Free |
| Supabase | Free | $25/month |
| Upstash Redis | Free | $10/month |
| Cloudflare R2 | Free (10GB) | $0.015/GB |
| OneSignal | Free (10k users) | $0.01/user |
| Apple Developer | $99/year | $99/year |
| Google Play | $25 one-time | $25 one-time |

**Total MVP cost:** ~$150-250/month + $124/year for app stores

---

## Data models

### User
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255), -- NULL for magic link only
  name VARCHAR(255),
  timezone VARCHAR(50) DEFAULT 'America/New_York',
  reminder_time TIME DEFAULT '07:00',
  reminder_enabled BOOLEAN DEFAULT true,
  plan VARCHAR(50) DEFAULT 'free',
  stripe_customer_id VARCHAR(255),
  church_id UUID REFERENCES churches(id),
  focus_area VARCHAR(50), -- from onboarding
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Church
```sql
CREATE TABLE churches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  code VARCHAR(20) UNIQUE NOT NULL, -- invite code
  admin_user_id UUID NOT NULL REFERENCES users(id),
  plan VARCHAR(50) DEFAULT 'church_license',
  member_limit INTEGER DEFAULT 100,
  stripe_subscription_id VARCHAR(255),
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Devotional
```sql
CREATE TABLE devotionals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  church_id UUID REFERENCES churches(id), -- NULL for default content
  date DATE, -- NULL if part of a plan
  reading_plan_id UUID REFERENCES reading_plans(id),
  day_number INTEGER, -- which day in the plan
  scripture_reference VARCHAR(255) NOT NULL,
  scripture_text TEXT NOT NULL,
  translation VARCHAR(20) DEFAULT 'NIV',
  reflection TEXT NOT NULL,
  prayer_prompt TEXT NOT NULL,
  audio_url VARCHAR(500),
  author VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_devotionals_date ON devotionals(date);
CREATE INDEX idx_devotionals_church ON devotionals(church_id);
CREATE INDEX idx_devotionals_plan ON devotionals(reading_plan_id, day_number);
```

### Reading plan
```sql
CREATE TABLE reading_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  church_id UUID REFERENCES churches(id), -- NULL for default plans
  title VARCHAR(255) NOT NULL,
  description TEXT,
  duration_days INTEGER NOT NULL,
  category VARCHAR(50), -- 'gratitude', 'anxiety', 'purpose', etc.
  is_featured BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### User plan progress
```sql
CREATE TABLE user_plan_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  reading_plan_id UUID REFERENCES reading_plans(id),
  current_day INTEGER DEFAULT 1,
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  is_active BOOLEAN DEFAULT true
);
```

### Completion
```sql
CREATE TABLE completions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  devotional_id UUID REFERENCES devotionals(id),
  completed_date DATE NOT NULL,
  completed_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, completed_date)
);

CREATE INDEX idx_completions_user_date ON completions(user_id, completed_date);
```

### Streak (computed, cached)
```sql
CREATE TABLE streak_cache (
  user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  current_streak INTEGER DEFAULT 0,
  longest_streak INTEGER DEFAULT 0,
  last_completed_date DATE,
  total_completions INTEGER DEFAULT 0,
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Journal entry
```sql
CREATE TABLE journal_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  devotional_id UUID REFERENCES devotionals(id),
  entry_date DATE NOT NULL,
  content_encrypted TEXT NOT NULL, -- encrypted on client
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Group
```sql
CREATE TABLE groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  church_id UUID REFERENCES churches(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  leader_user_id UUID REFERENCES users(id),
  reading_plan_id UUID REFERENCES reading_plans(id),
  started_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE group_members (
  group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  joined_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (group_id, user_id)
);
```

---

## API endpoints

### Authentication
```
POST /auth/magic-link - Request magic link email
POST /auth/verify - Verify magic link token
POST /auth/register - Create account (optional password)
POST /auth/login - Email + password login
POST /auth/refresh - Refresh token
```

### Devotionals
```
GET /devotionals/today - Get today's devotional
GET /devotionals/:date - Get devotional for specific date
GET /devotionals/plan/:plan_id/day/:day - Get plan devotional
POST /devotionals/:id/complete - Mark as completed
```

### Streaks
```
GET /streaks/me - Get current user's streak stats
GET /streaks/calendar - Get completion calendar (month view)
```

### Reading plans
```
GET /plans - List available plans
GET /plans/:id - Get plan details
POST /plans/:id/start - Start a plan
GET /plans/active - Get user's active plans
POST /plans/:id/skip-day - Skip to next day
```

### Journal
```
GET /journal - List journal entries
POST /journal - Create entry
GET /journal/:date - Get entry for date
PUT /journal/:id - Update entry
DELETE /journal/:id - Delete entry
POST /journal/export - Export all entries
```

### Church (dashboard)
```
GET /churches/:id - Get church details
GET /churches/:id/members - List members with stats
GET /churches/:id/analytics - Engagement analytics
POST /churches/:id/invite - Generate invite link
POST /churches/:id/devotionals - Upload custom devotional
GET /churches/:id/groups - List groups
POST /churches/:id/groups - Create group
```

### User settings
```
GET /settings - Get user settings
PUT /settings - Update settings
PUT /settings/reminder - Update reminder time
DELETE /account - Delete account and all data
```

---

## Streak calculation

### Algorithm
```python
def calculate_streak(user_id: str) -> dict:
    """Calculate current and longest streak for user."""

    # Get all completions sorted by date
    completions = get_completions(user_id, order='date desc')

    if not completions:
        return {'current': 0, 'longest': 0}

    today = date.today()
    yesterday = today - timedelta(days=1)

    # Check if streak is still active
    last_completed = completions[0].completed_date
    if last_completed not in (today, yesterday):
        # Streak broken
        current_streak = 0
    else:
        # Count consecutive days
        current_streak = 1
        for i in range(1, len(completions)):
            if completions[i].completed_date == completions[i-1].completed_date - timedelta(days=1):
                current_streak += 1
            else:
                break

    # Calculate longest streak
    longest_streak = calculate_longest_streak(completions)

    return {
        'current': current_streak,
        'longest': longest_streak
    }
```

### Caching
- Streak cached in `streak_cache` table
- Updated on each completion
- Cache expires if not accessed for 24 hours
- Redis used for hot cache (frequently accessed users)

---

## Push notifications

### Daily reminder
```python
async def send_daily_reminders():
    """Send reminders at each user's preferred time."""

    # Group users by reminder time
    users_by_time = group_users_by_reminder_time()

    for reminder_time, users in users_by_time.items():
        # Check if they already completed today
        incomplete = filter_incomplete_users(users)

        # Send notification
        for user in incomplete:
            await send_push(
                user_id=user.id,
                title="Good morning",
                body=f"Today's devotional is ready. {get_scripture_preview()}",
                data={'screen': 'today'}
            )
```

### Streak at risk
```python
async def send_streak_reminders():
    """Send evening reminder if streak at risk."""

    # Users with active streaks who haven't completed today
    at_risk = get_users_with_incomplete_streak()

    for user in at_risk:
        await send_push(
            user_id=user.id,
            title=f"Your {user.streak_days}-day streak",
            body="Still time to complete today's devotional.",
            data={'screen': 'today'}
        )
```

### Notification scheduling
- Use timezone-aware scheduling
- OneSignal handles delivery timing
- Users can disable specific notification types

---

## Offline support

### Local database
```typescript
// WatermelonDB schema
const schema = appSchema({
  version: 1,
  tables: [
    tableSchema({
      name: 'devotionals',
      columns: [
        { name: 'date', type: 'string', isIndexed: true },
        { name: 'scripture_reference', type: 'string' },
        { name: 'scripture_text', type: 'string' },
        { name: 'reflection', type: 'string' },
        { name: 'prayer_prompt', type: 'string' },
        { name: 'is_completed', type: 'boolean' },
        { name: 'synced_at', type: 'number' },
      ]
    }),
    tableSchema({
      name: 'journal_entries',
      columns: [
        { name: 'entry_date', type: 'string', isIndexed: true },
        { name: 'content_encrypted', type: 'string' },
        { name: 'needs_sync', type: 'boolean' },
      ]
    }),
  ]
});
```

### Sync strategy
1. On app open: Check for new content
2. Download 7 days ahead (Premium: 30 days)
3. Completions sync immediately when online
4. Queue completions if offline, sync when back online
5. Journal entries encrypted locally, synced when online

---

## Content management

### Default content
- Written by approved devotional writers
- Reviewed for theological accuracy
- Scheduled 30 days in advance
- Stored in database with `church_id = NULL`

### Custom content (Church License)
- Churches upload via dashboard
- Required fields: scripture, reflection, prayer prompt
- Optional: audio, author name
- Can schedule specific dates or add to plans

### Content format
```json
{
  "scripture_reference": "Psalm 23:1-3",
  "scripture_text": "The Lord is my shepherd...",
  "translation": "NIV",
  "reflection": "150-200 words of reflection...",
  "prayer_prompt": "What are you trusting God for today?",
  "audio_url": "https://cdn.dailyanchor.co/audio/...",
  "author": "Pastor John Smith"
}
```

---

## Church dashboard features

### Member management
- View all members (name, email, streak, last active)
- Filter by: active, inactive, new
- Send encouragement messages
- Remove members

### Analytics
- Daily/weekly/monthly active users
- Completion rates
- Average streak length
- Most engaged times
- Plan completion rates

### Content management
- Upload custom devotionals
- Schedule content
- Create custom reading plans
- Preview before publishing

### Groups
- Create groups
- Assign leader
- Attach reading plan
- View group progress

---

## Security

### Data encryption
- Journal entries encrypted on device (client-side encryption)
- Encryption key derived from user password or device key
- Server cannot read journal content

### Authentication
- Magic links (passwordless by default)
- Optional password for users who prefer it
- JWT tokens (1 hour), refresh tokens (30 days)

### Privacy
- No personal data shared between users
- Church admins see names and streaks only
- No selling of user data
- GDPR compliant (data export, deletion)

---

## Development phases

### Phase 1: MVP (4 weeks)
- User auth (magic link)
- Daily devotional display
- Completion tracking
- Basic streak
- Push notifications

### Phase 2: Core features (4 weeks)
- Reading plans
- Offline support
- Journal
- Premium tier (Stripe)

### Phase 3: Church features (4 weeks)
- Church dashboard
- Member management
- Custom content upload
- Group reading plans
- Church License (Stripe)

### Phase 4: Polish (ongoing)
- Audio devotionals
- Advanced analytics
- Improved offline
- Android/iOS optimizations

---

## Monitoring

### Metrics
- Daily active users
- Completion rate
- Streak distribution
- Notification engagement
- Church onboarding conversion

### Alerts
- API error rate > 1%
- Push notification failures
- Sync failures
- Content missing for tomorrow

---

## App store requirements

### iOS
- Privacy labels required
- App Review guidelines compliance
- In-app purchase for Premium (30% Apple cut)
- TestFlight for beta testing

### Android
- Privacy policy required
- Play Store compliance
- In-app purchase or web subscription
- Internal testing track for beta

### Both
- Accessibility (screen readers, font sizes)
- Multiple device support (phones, tablets)
- Light/dark mode
