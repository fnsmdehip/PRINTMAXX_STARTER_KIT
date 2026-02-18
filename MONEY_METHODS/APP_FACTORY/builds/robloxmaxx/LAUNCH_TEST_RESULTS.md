# RobloxMaxx API - Launch Test Results

**Date:** 2026-02-07
**Server:** Next.js 15.5.12 (Turbopack) on localhost:3000
**Database:** SQLite via better-sqlite3 (WAL mode)
**Architecture:** BYOK (Bring Your Own Key) - users provide their own Anthropic API key

---

## Environment Setup

### .env.local created with:
- `JWT_SECRET` - Random 64-char hex string (auto-generated)
- `ANTHROPIC_API_KEY` - NOT needed (BYOK model, users bring their own)
- Stripe keys commented out (not needed for local use)

### Configuration fix applied:
- Added `serverExternalPackages: ['better-sqlite3']` to `next.config.ts`
- Required because better-sqlite3 is a native Node module that cannot be bundled by Turbopack

### Database:
- SQLite DB auto-created at `data/robloxmaxx.db` on first request
- Tables: users, api_keys, usage_log, projects, project_history
- WAL journaling mode enabled for concurrent read/write

---

## Test Results Summary

| # | Endpoint | Method | Status | Result |
|---|----------|--------|--------|--------|
| 1 | /api/auth/register | POST | 200 | PASS - Creates user, returns JWT + API key |
| 2a | /api/auth/login | POST | 200 | PASS - Returns JWT token + userId |
| 2b | /api/auth/login (wrong pw) | POST | 401 | PASS - Rejects with "Invalid credentials" |
| 2c | /api/auth/register (dup) | POST | 400 | PASS - Rejects with "Email already registered" |
| 2d | /api/auth/register (short pw) | POST | 400 | PASS - Rejects with "Password must be at least 8 characters" |
| 3 | /api/templates | GET | 200 | PASS - Returns 3 templates (tycoon, obby, simulator) |
| 4a | /api/templates?genre=tycoon | GET | 200 | PASS - 4 scripts (config, manager, HUD, folder) |
| 4b | /api/templates?genre=obby | GET | 200 | PASS - 3 scripts |
| 4c | /api/templates?genre=simulator | GET | 200 | PASS - 2 scripts |
| 4d | /api/templates?genre=nonexistent | GET | 200 | PASS - Falls back to listing all templates |
| 5a | /api/usage (JWT) | GET | 200 | PASS - Returns plan, actions used/limit/remaining |
| 5b | /api/usage (API key) | GET | 200 | PASS - API key auth works too |
| 5c | /api/usage (no auth) | GET | 401 | PASS - Correctly rejects |
| 5d | /api/usage (bad token) | GET | 401 | PASS - Correctly rejects |
| 6a | /api/generate (no apiKey) | POST | 400 | PASS - "API key required. Bring your own Claude/Anthropic API key." |
| 6b | /api/generate (no prompt) | POST | 400 | PASS - "Missing prompt" |
| 6c | /api/generate (fake key) | POST | 401 | PASS - Anthropic returns authentication_error |
| 6d | /api/generate (header key) | POST | 401 | PASS - x-api-key header method works |
| 7 | /api/stripe/webhook | POST | 500 | EXPECTED - No Stripe keys configured (not needed locally) |
| 8 | /api/meta | GET | 200 | PASS - Returns 8 genres, trending, dying, platform updates |
| 9 | /api/estimate-revenue | POST | 200 | PASS - Revenue estimate with breakdowns |
| 10 | /api/scan-game | POST | 401 | EXPECTED - Requires real API key (BYOK) |
| 11 | /api/download | GET | 200 | PASS - Returns ~79KB Luau plugin source |

**Total: 21 tests, 19 PASS, 2 EXPECTED (Stripe/scan-game need real keys)**

---

## Detailed Test Outputs

### TEST 1: POST /api/auth/register
```
Request:  POST /api/auth/register
Body:     {"email": "test@robloxmaxx.com", "password": "testpass123"}
Response: {
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "apiKey": "rmx_f07a63330db5398...",
  "message": "Account created. 250 free actions included."
}
Status:   200 OK
```

### TEST 2a: POST /api/auth/login
```
Request:  POST /api/auth/login
Body:     {"email": "test@robloxmaxx.com", "password": "testpass123"}
Response: {"token": "eyJhbGciOiJIUzI1NiIs...", "userId": 1}
Status:   200 OK
```

### TEST 3: GET /api/templates
```
Request:  GET /api/templates
Response: {
  "templates": [
    {"genre": "tycoon", "name": "Basic Tycoon", "scriptCount": 4},
    {"genre": "obby", "name": "Basic Obby", "scriptCount": 3},
    {"genre": "simulator", "name": "Basic Simulator", "scriptCount": 2}
  ]
}
Status:   200 OK
```

### TEST 5a: GET /api/usage (JWT auth)
```
Request:  GET /api/usage
Headers:  Authorization: Bearer <jwt_token>
Response: {
  "plan": "free",
  "actionsUsed": 0,
  "actionsLimit": 250,
  "actionsRemaining": 250
}
Status:   200 OK
```

### TEST 8: GET /api/meta
```
Request:  GET /api/meta
Response: {
  "genres": [8 genre objects with health, trend, saturation, hot_mechanics, avoid],
  "trending_now": ["calm farming sims", "hybrid genres", "social fashion", ...],
  "dying": ["generic dropper tycoons", "basic obbies", "adopt me clones", ...],
  "platform_updates": ["4D Generation open beta", "PS5 launch", ...]
}
Status:   200 OK
```

### TEST 9: POST /api/estimate-revenue
```
Request:  POST /api/estimate-revenue
Body:     {"genre": "tycoon", "expected_dau": 500, "has_gamepasses": true, "has_devproducts": true}
Response: {
  "monthly_robux": {"low": 50625, "mid": 101250, "high": 202500},
  "monthly_usd": {"low": 134.66, "mid": 269.33, "high": 538.65},
  "creator_rewards_usd": 5.70,
  "total_monthly_usd": {"low": 140.36, "mid": 275.03, "high": 544.35},
  "breakdown": {"gamepasses": "59%", "devproducts": "29%", "creator_rewards": "12%"},
  "genre": "tycoon", "dau": 500
}
Status:   200 OK
```

### TEST 11: GET /api/download
```
Request:  GET /api/download
Response: Full Luau plugin source code (~79KB)
          Starts with: --[[ RobloxMaxx - AI Game Builder for Roblox Studio ...
Status:   200 OK
```

---

## Issues Found and Fixed

### Issue 1: better-sqlite3 bundling (FIXED)
**Problem:** Next.js Turbopack tried to bundle better-sqlite3 (native Node module), causing runtime errors.
**Fix:** Added `serverExternalPackages: ['better-sqlite3']` to next.config.ts.
**File:** `/api/next.config.ts`

### Issue 2: Stale .next cache from concurrent edits (TRANSIENT)
**Problem:** Other agents modifying files while server running caused Turbopack build manifest race conditions, resulting in 500 errors.
**Fix:** Server restart with `rm -rf .next` and fresh `npm run dev` resolves it. This is a development-only issue.

### Issue 3: No ANTHROPIC_API_KEY needed (NOT AN ISSUE)
**Context:** The API was refactored to BYOK model during this session. Users pass their own API key in each request via `apiKey` body param or `x-api-key` header. Zero API cost to us.

---

## How to Use Locally

### Start the server:
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/api
npm run dev
```

### Register (one time):
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "yourpassword"}'
```
Save the returned `token` and `apiKey`.

### Generate Roblox code (BYOK):
```bash
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "apiKey": "sk-ant-YOUR-REAL-ANTHROPIC-KEY",
    "prompt": "Create a tycoon game with pizza delivery mechanics",
    "mode": "scaffold",
    "genre": "tycoon",
    "token": "YOUR-JWT-TOKEN-FROM-REGISTER"
  }'
```

### Get genre templates:
```bash
curl http://localhost:3000/api/templates?genre=tycoon
```

### Check usage:
```bash
curl http://localhost:3000/api/usage -H "Authorization: Bearer YOUR-JWT-TOKEN"
```

### Get meta/trends:
```bash
curl http://localhost:3000/api/meta
```

### Estimate revenue:
```bash
curl -X POST http://localhost:3000/api/estimate-revenue \
  -H "Content-Type: application/json" \
  -d '{"genre": "rpg", "expected_dau": 1000, "has_gamepasses": true, "has_devproducts": true, "has_ads": true}'
```

### Download plugin:
```bash
curl http://localhost:3000/api/download > RobloxMaxx.lua
```

---

## API Endpoints Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| /api/auth/register | POST | None | Create account, get JWT + API key |
| /api/auth/login | POST | None | Login, get JWT token |
| /api/templates | GET | None | List all game templates |
| /api/templates?genre=X | GET | None | Get specific genre template |
| /api/usage | GET | JWT/API Key | Check usage stats |
| /api/generate | POST | BYOK (apiKey) | Generate Roblox code with AI |
| /api/meta | GET | None | Current Roblox genre meta/trends |
| /api/estimate-revenue | POST | None | Revenue estimation calculator |
| /api/scan-game | POST | BYOK (apiKey) | AI-powered code analysis |
| /api/download | GET | None | Download Roblox Studio plugin |
| /api/stripe/webhook | POST | Stripe sig | Stripe payment webhooks |

---

## Plugin Connection

The Roblox Studio plugin (downloaded via /api/download or from `plugin/` directory) connects to this API. Configure the plugin with:
- **API URL:** `http://localhost:3000` (for local use)
- **Anthropic API Key:** Your own key from console.anthropic.com
- **Auth Token:** JWT from /api/auth/register or /api/auth/login
