# DATABASE_BACKEND_GUIDE.md

**PRINTMAXX Backend Infrastructure: Supabase + PostgreSQL**

Last updated: 2026-01-25

---

## Overview

This guide covers database and backend setup for PRINTMAXX apps and services. Supabase is the primary recommendation for rapid development with PostgreSQL power.

---

## Why Supabase for PRINTMAXX

### Cost-to-Value Analysis

| Feature | Supabase | Firebase | PlanetScale | Neon |
|---------|----------|----------|-------------|------|
| Free tier database | 500MB | 1GB (Firestore) | 5GB | 512MB |
| Free tier bandwidth | 2GB | 10GB/mo | 1B reads | Unlimited |
| PostgreSQL | Yes | No (NoSQL) | MySQL | Yes |
| Realtime built-in | Yes | Yes | No | No |
| Auth included | Yes | Yes | No | No |
| Edge Functions | Yes | Cloud Functions | No | No |
| Row Level Security | Yes | Rules | No | Yes |
| Open source | Yes | No | No | Yes |
| Self-host option | Yes | No | No | Yes |

**Verdict:** Supabase wins for PRINTMAXX because:
1. PostgreSQL = real database, not NoSQL limitations
2. Free tier covers MVP + early traction
3. Auth + Database + Storage + Functions in one
4. Can self-host later to cut costs at scale
5. React Native SDK is solid

---

## Supabase Pricing (As of 2025)

### Free Tier (Perfect for MVP)
- 500MB database
- 1GB file storage
- 50,000 monthly active users (auth)
- 500K edge function invocations
- 2GB bandwidth
- 7-day log retention

### Pro ($25/mo per project)
- 8GB database
- 100GB file storage
- 100,000 MAUs
- 2M edge function invocations
- 250GB bandwidth
- 90-day log retention
- Daily backups
- Email support

### Team ($599/mo)
- Everything in Pro
- SOC2 compliance
- HIPAA available
- Priority support
- SSO

### PRINTMAXX Cost Projection

| Stage | Users | Storage | Monthly Cost |
|-------|-------|---------|--------------|
| MVP (0-1K users) | <1K | <500MB | $0 |
| Early Traction (1K-10K) | 1-10K | <2GB | $25 |
| Growth (10K-50K) | 10-50K | <8GB | $25 |
| Scale (50K+) | 50K+ | 8GB+ | $25 + usage |

**Breakpoint:** Free tier handles first 1-2K users easily. Upgrade at traction.

---

## Quick Setup (15 Minutes to Backend)

### 1. Create Supabase Project

```bash
# Install Supabase CLI
brew install supabase/tap/supabase

# Login
supabase login

# Init local project
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT
supabase init
```

### 2. Create Project in Dashboard

1. Go to https://supabase.com/dashboard
2. New Project > Name: `printmaxx-prod`
3. Database Password: Generate strong (save to 1Password)
4. Region: `us-east-1` (or closest to target users)
5. Wait ~2 min for provisioning

### 3. Get API Keys

From Project Settings > API:
- `SUPABASE_URL`: `https://[project-ref].supabase.co`
- `SUPABASE_ANON_KEY`: Public key (safe for client)
- `SUPABASE_SERVICE_KEY`: Server-only (NEVER expose)

Add to `.env`:
```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_KEY=eyJhbGc... # Server only
```

---

## Schema Design for PRINTMAXX Apps

### Core Tables (All Apps)

```sql
-- Users (extends Supabase auth.users)
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  email TEXT,
  display_name TEXT,
  avatar_url TEXT,
  subscription_tier TEXT DEFAULT 'free',
  subscription_expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Users can only read/write their own profile
CREATE POLICY "Users can view own profile" ON public.profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles
  FOR UPDATE USING (auth.uid() = id);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

### App-Specific: PrayerLock

```sql
-- Prayer sessions
CREATE TABLE public.prayer_sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  duration_seconds INTEGER,
  completed BOOLEAN DEFAULT FALSE,
  prayer_type TEXT, -- morning, evening, custom
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.prayer_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own sessions" ON public.prayer_sessions
  FOR ALL USING (auth.uid() = user_id);

-- Prayer streaks
CREATE TABLE public.prayer_streaks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) UNIQUE NOT NULL,
  current_streak INTEGER DEFAULT 0,
  longest_streak INTEGER DEFAULT 0,
  last_prayer_date DATE,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.prayer_streaks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own streaks" ON public.prayer_streaks
  FOR ALL USING (auth.uid() = user_id);
```

### App-Specific: WalkToUnlock

```sql
-- Walk sessions
CREATE TABLE public.walk_sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  steps_counted INTEGER DEFAULT 0,
  target_steps INTEGER NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  calories_burned INTEGER,
  distance_meters NUMERIC(10,2),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.walk_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own walks" ON public.walk_sessions
  FOR ALL USING (auth.uid() = user_id);

-- Daily goals
CREATE TABLE public.daily_goals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  goal_date DATE DEFAULT CURRENT_DATE,
  target_steps INTEGER DEFAULT 10000,
  actual_steps INTEGER DEFAULT 0,
  goal_met BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, goal_date)
);

ALTER TABLE public.daily_goals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own goals" ON public.daily_goals
  FOR ALL USING (auth.uid() = user_id);
```

### App-Specific: StudyLock

```sql
-- Study sessions
CREATE TABLE public.study_sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  duration_minutes INTEGER,
  subject TEXT,
  blocked_apps_count INTEGER DEFAULT 0,
  distraction_attempts INTEGER DEFAULT 0,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.study_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own study sessions" ON public.study_sessions
  FOR ALL USING (auth.uid() = user_id);

-- Blocked apps config
CREATE TABLE public.blocked_apps (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  app_bundle_id TEXT NOT NULL,
  app_name TEXT,
  always_blocked BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, app_bundle_id)
);

ALTER TABLE public.blocked_apps ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own blocked apps" ON public.blocked_apps
  FOR ALL USING (auth.uid() = user_id);
```

### Lead Management (Landing Site)

```sql
-- Leads from landing pages
CREATE TABLE public.leads (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT NOT NULL,
  source TEXT, -- truth-page, magnet, organic
  utm_source TEXT,
  utm_medium TEXT,
  utm_campaign TEXT,
  lead_magnet TEXT, -- which magnet they downloaded
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- No RLS needed, this is server-side only
-- Use service key for writes

-- Create index for email lookups
CREATE INDEX idx_leads_email ON public.leads(email);
CREATE INDEX idx_leads_created ON public.leads(created_at DESC);
```

### Analytics Events

```sql
-- Generic event tracking
CREATE TABLE public.events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  anonymous_id TEXT, -- for non-logged-in users
  event_name TEXT NOT NULL,
  event_properties JSONB DEFAULT '{}',
  page_url TEXT,
  referrer TEXT,
  device_type TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for analytics queries
CREATE INDEX idx_events_name ON public.events(event_name);
CREATE INDEX idx_events_user ON public.events(user_id);
CREATE INDEX idx_events_created ON public.events(created_at DESC);
CREATE INDEX idx_events_properties ON public.events USING GIN(event_properties);
```

---

## Authentication Setup

### Supported Methods

| Method | Use Case | Setup Difficulty |
|--------|----------|------------------|
| Email/Password | Standard signup | Easy |
| Magic Link | Passwordless | Easy |
| Google OAuth | Quick signup | Medium |
| Apple Sign-In | iOS apps (required) | Medium |
| Phone/SMS | Premium feel | Medium |

### Enable Providers in Dashboard

Project Settings > Authentication > Providers

**Recommended for PRINTMAXX Apps:**
1. Email (enabled by default)
2. Apple (required for iOS if you have social login)
3. Google (optional, high conversion)

### Apple Sign-In Setup

1. Apple Developer Console > Certificates > Services IDs
2. Create Service ID for your app
3. Enable Sign In with Apple
4. Add Supabase callback URL: `https://[project].supabase.co/auth/v1/callback`
5. Get Team ID, Key ID, Private Key
6. Add to Supabase Dashboard > Auth > Apple

### Google OAuth Setup

1. Google Cloud Console > APIs & Services > Credentials
2. Create OAuth 2.0 Client ID
3. Authorized redirect: `https://[project].supabase.co/auth/v1/callback`
4. Add Client ID + Secret to Supabase Dashboard

### React Native Auth Code

```typescript
// lib/supabase.ts
import 'react-native-url-polyfill/auto';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage: AsyncStorage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});
```

```typescript
// hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';
import { Session, User } from '@supabase/supabase-js';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
        setUser(session?.user ?? null);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const signInWithEmail = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    return { data, error };
  };

  const signUpWithEmail = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });
    return { data, error };
  };

  const signInWithApple = async () => {
    // Requires expo-apple-authentication
    // See: https://supabase.com/docs/guides/auth/social-login/auth-apple
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    return { error };
  };

  return {
    user,
    session,
    loading,
    signInWithEmail,
    signUpWithEmail,
    signInWithApple,
    signOut,
  };
}
```

---

## Database Queries (React Native)

### Basic CRUD Operations

```typescript
// services/sessions.ts
import { supabase } from '../lib/supabase';

// CREATE
export async function createPrayerSession(userId: string, prayerType: string) {
  const { data, error } = await supabase
    .from('prayer_sessions')
    .insert({
      user_id: userId,
      prayer_type: prayerType,
    })
    .select()
    .single();

  return { data, error };
}

// READ
export async function getPrayerSessions(userId: string, limit = 10) {
  const { data, error } = await supabase
    .from('prayer_sessions')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
    .limit(limit);

  return { data, error };
}

// UPDATE
export async function completePrayerSession(sessionId: string, durationSeconds: number) {
  const { data, error } = await supabase
    .from('prayer_sessions')
    .update({
      ended_at: new Date().toISOString(),
      duration_seconds: durationSeconds,
      completed: true,
    })
    .eq('id', sessionId)
    .select()
    .single();

  return { data, error };
}

// DELETE
export async function deletePrayerSession(sessionId: string) {
  const { error } = await supabase
    .from('prayer_sessions')
    .delete()
    .eq('id', sessionId);

  return { error };
}
```

### Realtime Subscriptions

```typescript
// Subscribe to changes
useEffect(() => {
  const subscription = supabase
    .channel('prayer_sessions_changes')
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'prayer_sessions',
        filter: `user_id=eq.${userId}`,
      },
      (payload) => {
        console.log('Change received:', payload);
        // Update local state
        if (payload.eventType === 'INSERT') {
          setSessions(prev => [payload.new, ...prev]);
        }
      }
    )
    .subscribe();

  return () => {
    subscription.unsubscribe();
  };
}, [userId]);
```

### Aggregate Queries

```typescript
// Get user stats
export async function getUserStats(userId: string) {
  const { data, error } = await supabase
    .rpc('get_user_prayer_stats', { p_user_id: userId });

  return { data, error };
}

// SQL function (create in Supabase Dashboard > SQL Editor)
/*
CREATE OR REPLACE FUNCTION get_user_prayer_stats(p_user_id UUID)
RETURNS TABLE (
  total_sessions BIGINT,
  total_minutes BIGINT,
  avg_duration_minutes NUMERIC,
  completion_rate NUMERIC,
  current_streak INTEGER
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(*)::BIGINT as total_sessions,
    COALESCE(SUM(duration_seconds) / 60, 0)::BIGINT as total_minutes,
    COALESCE(AVG(duration_seconds) / 60, 0)::NUMERIC as avg_duration_minutes,
    COALESCE(
      (COUNT(*) FILTER (WHERE completed = true)::NUMERIC / NULLIF(COUNT(*), 0)) * 100,
      0
    )::NUMERIC as completion_rate,
    COALESCE(ps.current_streak, 0) as current_streak
  FROM prayer_sessions s
  LEFT JOIN prayer_streaks ps ON ps.user_id = s.user_id
  WHERE s.user_id = p_user_id
  GROUP BY ps.current_streak;
END;
$$ LANGUAGE plpgsql;
*/
```

---

## Edge Functions (Serverless)

### When to Use Edge Functions

| Use Case | Example |
|----------|---------|
| Webhooks | RevenueCat subscription events |
| Third-party API calls | OpenAI, Stripe, SendGrid |
| Complex business logic | Streak calculations |
| Scheduled jobs | Daily digest emails |
| Rate-limited operations | Prevent abuse |

### Create Edge Function

```bash
# Create function
supabase functions new process-subscription

# This creates: supabase/functions/process-subscription/index.ts
```

```typescript
// supabase/functions/process-subscription/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  try {
    // Verify webhook signature (RevenueCat example)
    const signature = req.headers.get('X-RevenueCat-Signature');
    // ... verify signature

    const payload = await req.json();

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );

    // Update user subscription
    const { data, error } = await supabase
      .from('profiles')
      .update({
        subscription_tier: payload.subscription_tier,
        subscription_expires_at: payload.expires_at,
      })
      .eq('id', payload.user_id);

    if (error) throw error;

    return new Response(JSON.stringify({ success: true }), {
      headers: { 'Content-Type': 'application/json' },
      status: 200,
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { 'Content-Type': 'application/json' },
      status: 400,
    });
  }
});
```

### Deploy Edge Function

```bash
# Deploy single function
supabase functions deploy process-subscription

# Deploy all functions
supabase functions deploy
```

### Call Edge Function from App

```typescript
const { data, error } = await supabase.functions.invoke('process-subscription', {
  body: { user_id: userId, action: 'upgrade' },
});
```

---

## Storage (File Uploads)

### Setup Storage Buckets

```sql
-- Create buckets via SQL or Dashboard
INSERT INTO storage.buckets (id, name, public)
VALUES
  ('avatars', 'avatars', true),
  ('app-assets', 'app-assets', true),
  ('user-content', 'user-content', false);

-- RLS for avatars (public read, owner write)
CREATE POLICY "Public avatars" ON storage.objects
  FOR SELECT USING (bucket_id = 'avatars');

CREATE POLICY "Users can upload own avatar" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );
```

### Upload from React Native

```typescript
import * as ImagePicker from 'expo-image-picker';
import { decode } from 'base64-arraybuffer';

async function uploadAvatar(userId: string) {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    aspect: [1, 1],
    quality: 0.5,
    base64: true,
  });

  if (!result.canceled && result.assets[0].base64) {
    const filePath = `${userId}/avatar.jpg`;

    const { data, error } = await supabase.storage
      .from('avatars')
      .upload(filePath, decode(result.assets[0].base64), {
        contentType: 'image/jpeg',
        upsert: true,
      });

    if (error) throw error;

    // Get public URL
    const { data: { publicUrl } } = supabase.storage
      .from('avatars')
      .getPublicUrl(filePath);

    // Update profile
    await supabase
      .from('profiles')
      .update({ avatar_url: publicUrl })
      .eq('id', userId);

    return publicUrl;
  }
}
```

---

## RevenueCat Integration

### Webhook Setup

1. RevenueCat Dashboard > Project Settings > Integrations
2. Add Webhook: `https://[project].supabase.co/functions/v1/revenuecat-webhook`
3. Copy webhook secret

### Edge Function for Webhooks

```typescript
// supabase/functions/revenuecat-webhook/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const WEBHOOK_SECRET = Deno.env.get('REVENUECAT_WEBHOOK_SECRET')!;

serve(async (req) => {
  // Verify signature
  const signature = req.headers.get('X-Signature');
  // ... implement HMAC verification

  const event = await req.json();

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  const userId = event.event.app_user_id;
  const eventType = event.event.type;

  switch (eventType) {
    case 'INITIAL_PURCHASE':
    case 'RENEWAL':
      await supabase.from('profiles').update({
        subscription_tier: 'pro',
        subscription_expires_at: event.event.expiration_at_ms
          ? new Date(event.event.expiration_at_ms).toISOString()
          : null,
      }).eq('id', userId);
      break;

    case 'CANCELLATION':
    case 'EXPIRATION':
      await supabase.from('profiles').update({
        subscription_tier: 'free',
        subscription_expires_at: null,
      }).eq('id', userId);
      break;
  }

  return new Response(JSON.stringify({ received: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
});
```

---

## Performance Optimization

### Indexes

```sql
-- Common query patterns need indexes
CREATE INDEX idx_sessions_user_date ON prayer_sessions(user_id, created_at DESC);
CREATE INDEX idx_events_user_name ON events(user_id, event_name);
CREATE INDEX idx_leads_source ON leads(source, created_at DESC);
```

### Query Optimization

```typescript
// BAD: Fetches all columns
const { data } = await supabase.from('profiles').select('*');

// GOOD: Only fetch what you need
const { data } = await supabase
  .from('profiles')
  .select('id, display_name, avatar_url')
  .single();

// BAD: N+1 queries
for (const session of sessions) {
  const { data } = await supabase
    .from('users')
    .select('*')
    .eq('id', session.user_id);
}

// GOOD: Single query with join
const { data } = await supabase
  .from('prayer_sessions')
  .select(`
    *,
    profiles:user_id (display_name, avatar_url)
  `);
```

### Connection Pooling

Supabase handles connection pooling automatically. For high-traffic apps:

1. Use PgBouncer (enabled by default on Supabase)
2. Set connection limit appropriately
3. Use `single()` for single-row queries
4. Batch inserts when possible

---

## Security Best Practices

### Row Level Security (RLS) Patterns

```sql
-- Basic: Users see only their data
CREATE POLICY "own_data" ON table_name
  FOR ALL USING (auth.uid() = user_id);

-- Read-only for all, write for owner
CREATE POLICY "read_all" ON table_name
  FOR SELECT USING (true);

CREATE POLICY "write_own" ON table_name
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Admin override
CREATE POLICY "admin_all" ON table_name
  FOR ALL USING (
    auth.uid() IN (SELECT id FROM profiles WHERE role = 'admin')
  );

-- Time-limited access
CREATE POLICY "recent_only" ON table_name
  FOR SELECT USING (
    auth.uid() = user_id
    AND created_at > NOW() - INTERVAL '30 days'
  );
```

### API Key Security

```typescript
// NEVER do this
const supabase = createClient(url, 'eyJ...service_role_key');

// ALWAYS use anon key on client
const supabase = createClient(url, process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY);

// Service key ONLY in Edge Functions / server-side
// supabase/functions/*/index.ts
const supabase = createClient(url, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY'));
```

### Input Validation

```typescript
import { z } from 'zod';

const CreateSessionSchema = z.object({
  prayer_type: z.enum(['morning', 'evening', 'custom']),
  duration_target: z.number().min(1).max(240),
});

async function createSession(input: unknown) {
  const validated = CreateSessionSchema.parse(input);

  const { data, error } = await supabase
    .from('prayer_sessions')
    .insert(validated);

  return { data, error };
}
```

---

## Migration from Firebase

If you have existing Firebase data:

### 1. Export Firebase Data

```javascript
// Firebase Admin SDK
const admin = require('firebase-admin');
const fs = require('fs');

async function exportCollection(collectionName) {
  const snapshot = await admin.firestore().collection(collectionName).get();
  const data = snapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  }));
  fs.writeFileSync(`${collectionName}.json`, JSON.stringify(data, null, 2));
}
```

### 2. Transform Data

```javascript
// Transform Firebase documents to PostgreSQL rows
const firebaseData = require('./users.json');

const pgData = firebaseData.map(user => ({
  id: user.id, // Keep Firebase UID if possible
  email: user.email,
  display_name: user.displayName,
  created_at: new Date(user.createdAt._seconds * 1000).toISOString(),
}));

fs.writeFileSync('users_pg.json', JSON.stringify(pgData, null, 2));
```

### 3. Import to Supabase

```sql
-- Use Supabase Dashboard > SQL Editor
-- Or pg_restore / psql for large datasets

INSERT INTO profiles (id, email, display_name, created_at)
SELECT
  (data->>'id')::uuid,
  data->>'email',
  data->>'display_name',
  (data->>'created_at')::timestamptz
FROM json_array_elements(:json_data) as data;
```

---

## Alternatives Comparison

### When to Use Firebase Instead

| Scenario | Firebase | Supabase |
|----------|----------|----------|
| Complex realtime (games, chat) | Better | Good |
| Google Cloud ecosystem | Better | N/A |
| NoSQL flexibility needed | Better | No |
| Team already knows Firebase | Better | Learning curve |
| Need full SQL power | No | Better |
| Self-hosting requirement | No | Better |
| Open source preference | No | Better |

### When to Use PlanetScale

- Need MySQL specifically
- Massive scale (billions of rows)
- Schema branching workflow
- Team prefers MySQL
- Don't need auth/storage/realtime bundled

### When to Use Neon

- Pure PostgreSQL need
- Serverless scaling priority
- Branch-based development
- Don't need auth/storage bundled
- Cost-sensitive at scale

### When to Use Railway

- Full platform (not just database)
- Docker deployment needs
- Simpler pricing model
- General backend hosting

---

## Cost Optimization

### Stay on Free Tier Longer

1. **Delete old data** - Prune logs, old sessions
2. **Optimize queries** - Fewer reads = less usage
3. **Client-side caching** - Use AsyncStorage for frequent reads
4. **Batch operations** - Single insert vs many
5. **Compress images** - Smaller storage footprint

### When to Upgrade

| Metric | Free Limit | Upgrade Trigger |
|--------|------------|-----------------|
| Database size | 500MB | >400MB |
| Monthly active users | 50K | >40K |
| Storage | 1GB | >800MB |
| Bandwidth | 2GB | >1.5GB |
| Edge function calls | 500K | >400K |

### Self-Hosting (Advanced)

At scale (100K+ users), self-hosting saves money:

```bash
# Docker Compose setup
git clone --depth 1 https://github.com/supabase/supabase
cd supabase/docker
cp .env.example .env
# Edit .env with your settings
docker compose up -d
```

Cost comparison at 100K MAU:
- Supabase Cloud: ~$50-100/mo
- Self-hosted (DigitalOcean): ~$20-40/mo
- Self-hosted requires DevOps knowledge

---

## Quick Reference

### Supabase CLI Commands

```bash
supabase login              # Authenticate CLI
supabase init               # Initialize project
supabase start              # Start local dev
supabase stop               # Stop local dev
supabase db push            # Push schema changes
supabase db pull            # Pull remote schema
supabase functions new X    # Create edge function
supabase functions deploy   # Deploy all functions
supabase gen types typescript --local > types/supabase.ts
```

### React Native Install

```bash
npm install @supabase/supabase-js
npm install react-native-url-polyfill
npm install @react-native-async-storage/async-storage
```

### Common Gotchas

1. **Expo Go limitation**: Some auth methods need dev build
2. **RLS must be enabled**: Or all data is public
3. **Service key exposure**: Never use in client code
4. **UUID format**: Supabase uses UUID, not Firebase strings
5. **Timestamps**: Use `timestamptz`, not `timestamp`

---

## Next Steps

1. Create Supabase project at https://supabase.com
2. Run schema SQL for your app (PrayerLock, WalkToUnlock, etc.)
3. Enable authentication providers
4. Test locally with `supabase start`
5. Deploy and connect from React Native app

---

## Files to Create

After reading this guide, create these files:

```
MONEY_METHODS/APP_FACTORY/
├── supabase/
│   ├── schema.sql          # All table definitions
│   ├── seed.sql            # Test data
│   └── functions/
│       ├── revenuecat-webhook/
│       └── daily-streak-update/
└── lib/
    ├── supabase.ts         # Client setup
    └── hooks/
        ├── useAuth.ts
        └── useDatabase.ts
```

---

**Bottom line:** Supabase is the right choice for PRINTMAXX. Free tier handles MVP, PostgreSQL gives real database power, and the all-in-one stack (auth + db + storage + functions) means faster shipping. Start with the schema above, connect your apps, and scale when you have revenue.
