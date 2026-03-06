# Chrome Extension Specs — 3 Ideas

Full technical specs, manifest, permissions, monetization, and Chrome Web Store listing copy.

---

## Extension 1: FocusBlocker Pro — Site Blocker with Pomodoro Engine

**Concept:** Blocks distracting sites during focus sessions. Runs Pomodoro timer in the extension popup. When the session ends, blocked sites re-enable automatically. No complicated setup — install, start session, work.

**Core problem it solves:**
Cold turkey blockers are too rigid. People disable them. FocusBlocker blocks sites only during active sessions, automatically re-enables during breaks. The timer enforces both work and rest.

**Key features:**
1. One-click session start (25 min default, customizable)
2. Blocked sites list (default: Twitter/X, Reddit, YouTube, Instagram, TikTok, Facebook, LinkedIn feed)
3. Custom block list: any URL pattern
4. Break mode: 5-minute auto-unlock between sessions
5. Session counter: tracks Pomodoros completed today
6. Streak: consecutive days with 4+ sessions
7. Emergency override: type a 25-character phrase to unlock early (makes it intentional, not reflexive)
8. Stats page: sessions per day, total focus hours, streak calendar

**Manifest v3 spec:**
```json
{
  "manifest_version": 3,
  "name": "FocusBlocker Pro",
  "version": "1.0.0",
  "description": "Block distracting sites during Pomodoro sessions. Works automatically.",
  "permissions": [
    "declarativeNetRequest",
    "storage",
    "alarms",
    "notifications",
    "activeTab"
  ],
  "host_permissions": ["<all_urls>"],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/16.png",
      "48": "icons/48.png",
      "128": "icons/128.png"
    }
  },
  "options_page": "options.html"
}
```

**How it blocks:**
- Manifest v3 uses `declarativeNetRequest` instead of `webRequest`
- Dynamic rules: when session starts, inject block rules for each blocked domain
- Block rule redirects matched URLs to extension's `blocked.html` page
- `blocked.html` shows: time remaining in session, emergency override input, motivational message

**Popup UI (popup.html):**
```
┌─────────────────────────────┐
│  FocusBlocker Pro           │
│  ─────────────────────────  │
│                             │
│  [▶ START FOCUS] 25:00      │
│                             │
│  Today: 0 sessions ● 0 hrs  │
│  Streak: 12 days 🔥         │
│                             │
│  [⚙ Settings] [📊 Stats]   │
└─────────────────────────────┘

During session:
┌─────────────────────────────┐
│  🍅 FOCUS SESSION           │
│  ─────────────────────────  │
│                             │
│       18:43 remaining       │
│   ████████░░░░░░░░░░ 60%    │
│                             │
│  Blocking: 7 sites          │
│                             │
│  [■ END EARLY]              │
└─────────────────────────────┘
```

**Blocked page (blocked.html):**
```
Access blocked.
You're in a focus session. 18:43 remaining.

You blocked [twitter.com] to protect this time.
The session ends automatically — no temptation to manually unlock.

Emergency unlock: type "I am choosing distraction over my goal"
[                                           ]
```

**Settings page (options.html):**
- Session length: 15 / 25 / 45 / 90 / Custom
- Block list: text input to add/remove domains
- Break length: 5 / 10 / 15 minutes
- Auto-start next session after break: toggle
- Daily goal: number of sessions
- Notification sound: yes/no + volume
- Emergency phrase: custom text (default: "I am choosing distraction over my goal")

**Monetization:**
- Free: 1 block list, 5 sites max, no streak tracking, no stats
- Pro: $3.99/month or $24.99/year (unlimited sites, stats, streak, multiple block lists for different modes)
- One-time: $39.99 lifetime (offer via Lemon Squeezy, drive traffic from settings page)

**Revenue math:**
- 10,000 installs × 5% paid = 500 × $3.99/mo = $1,995/month
- Or 500 × $24.99/year = $12,495/year = $1,041/month
- Combined model expected: $1,500/month at 10K installs
- Chrome Web Store has 3B+ users — the organic discovery potential is massive

**Chrome Web Store listing:**

Title: FocusBlocker Pro — Pomodoro Site Blocker

Short description (132 chars max):
Block Twitter, Reddit, YouTube during focus sessions. Pomodoro timer built in. Sites auto-unblock on break.

Category: Productivity
Language: English
Price: Free (with IAP)

**Launch strategy:**
- ProductHunt: submit on a Tuesday morning (best day for tech crowd)
- Reddit: r/GetStudying, r/productivity, r/cscareerquestions
- HackerNews "Show HN:" post
- Build-in-public Twitter thread: "Built a Chrome extension in 2 days. Here's what I learned."
- Respond to every "I need a site blocker that..." post on Reddit for 30 days

---

## Extension 2: LinkedInMaxx — LinkedIn Power Tools for Outreach

**Concept:** Supercharges LinkedIn cold outreach. Adds AI-powered personalized message generation, contact export, connection tracking, and bulk message queue directly to LinkedIn's UI via content script injection.

**Core problem:**
LinkedIn native DM tools are terrible for cold outreach. No templates, no tracking, no bulk sending, no message personalization beyond [First Name]. LinkedInMaxx adds a professional outreach layer on top of LinkedIn.

**Key features:**
1. **Message generator**: hover over any profile, click "Generate Message" → AI writes personalized DM based on their headline, company, and recent activity visible on LinkedIn
2. **Template library**: save and reuse message templates with {first_name}, {company}, {role} variables
3. **Connection tracker**: shows last message date, reply status (manually updated), follow-up due dates
4. **Contact exporter**: export profile data (name, title, company, location) to CSV without needing Sales Navigator
5. **Profile enrichment**: when viewing a profile, shows estimated company size (via Crunchbase), open roles (via LinkedIn job search), recent funding news
6. **Bulk message queue**: queue up to 20 personalized messages, send with 30-60 second delays (anti-spam)

**Manifest v3 spec:**
```json
{
  "manifest_version": 3,
  "name": "LinkedInMaxx",
  "version": "1.0.0",
  "description": "AI-powered LinkedIn outreach. Generate messages, track connections, export contacts.",
  "permissions": [
    "storage",
    "tabs",
    "scripting",
    "alarms"
  ],
  "host_permissions": ["https://www.linkedin.com/*"],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["https://www.linkedin.com/*"],
      "js": ["content.js"],
      "css": ["content.css"]
    }
  ],
  "action": {
    "default_popup": "popup.html"
  }
}
```

**Content script injection strategy:**
- Detects URL changes (LinkedIn is a SPA) using MutationObserver
- On profile page: injects "Generate Message" button next to "Connect" and "Message" buttons
- On messaging page: injects template selector in message compose area
- On search results: adds "Export CSV" button to search toolbar
- On connections page: adds reply status badges to each connection row

**AI message generation:**
- Extracts from LinkedIn DOM: {name}, {title}, {company}, {headline}, {recent_post_snippet}
- Sends to Claude Haiku API via background.js
- Prompt template:
```
Write a short LinkedIn cold message (under 75 words) to connect with {name},
who is a {title} at {company}. Their headline: "{headline}".
My offer: {user_configured_offer}.
Tone: professional but human.
No "I hope this finds you well."
Lead with something specific about their work.
```
- Response displayed in popup for editing before sending

**Security considerations:**
- Never store LinkedIn credentials — use existing LinkedIn session cookies only
- Content scripts run in page context (no eval), follow CSP
- Export functionality: scrape only what's visible on screen (no undocumented API calls)
- Rate limiting enforced in extension: max 50 profile views/hour, 20 messages/day

**Monetization:**
- Free: 5 AI messages/month, 20 contact exports/month, 3 templates
- LinkedInMaxx Pro: $19.99/month or $149/year (unlimited AI messages, unlimited exports, full template library, CRM tracking, bulk queue)
- Agency: $49/month/seat (team dashboard, shared templates, reporting)

**Revenue math:**
- 5,000 installs × 8% paid = 400 × $19.99 = $7,996/month
- Agencies: 20 × $49 = $980/month
- Total: ~$9,000/month at this scale

**Legal/ToS considerations:**
- LinkedIn's ToS prohibits "scraping" and automated messaging
- Extension works by simulating manual user actions, not API calls
- Add ToS page: "This extension assists manual LinkedIn activity. Don't use for spam."
- Bulk queue includes 30-60 second delays + per-day limits to mimic human behavior
- LinkedIn has been known to restrict accounts that use automation — disclose risk to users

**Chrome Web Store listing:**

Title: LinkedInMaxx — AI LinkedIn Outreach Assistant

Short description:
Generate personalized LinkedIn messages with AI, track connections, export contacts. No Sales Navigator needed.

Category: Productivity / Social & Communication

---

## Extension 3: PriceTrackr — Amazon & TikTok Shop Price Intelligence

**Concept:** On any Amazon, TikTok Shop, or eBay product page, instantly shows: price history chart, competing seller prices, best buy day, profit calculator (for resellers), and alerts when price drops below a set threshold.

**Core problem:**
Consumers buy at the wrong price. Resellers need margin data instantly. Price history is locked in Keepa (paid) or CamelCamelCamel (Amazon only, ugly). PriceTrackr gives this data on TikTok Shop and eBay too — no competition there.

**Key features:**
1. **Price history chart**: 90-day price chart displayed below the product title on Amazon, eBay, TikTok Shop
2. **Best buy indicator**: "Price is 12% above average. Average price: $34.50. Best price in 90 days: $28.99."
3. **Competing sellers**: shows all sellers for this ASIN with their prices + seller ratings
4. **Price alert**: set target price → receive Chrome notification when price hits it
5. **Profit calculator** (for resellers): input buy price → shows FBA fees, estimated profit, ROI%, sales rank
6. **TikTok Shop integration**: shows seller history, price trends, competitor products with same supplier (via reverse image search shortcut)
7. **Export**: save tracked products to Google Sheets with one click

**Where price data comes from:**
- Amazon: Keepa API ($19/month, 100 tokens/minute free tier)
- CamelCamelCamel unofficial API (price history)
- eBay sold listings API (free, public)
- TikTok Shop: scrape product price from visible DOM (no API), track over time in extension's own database

**Manifest v3 spec:**
```json
{
  "manifest_version": 3,
  "name": "PriceTrackr",
  "version": "1.0.0",
  "description": "Price history + profit calculator on Amazon, TikTok Shop, and eBay. See if you're buying at the right price.",
  "permissions": [
    "storage",
    "alarms",
    "notifications",
    "scripting"
  ],
  "host_permissions": [
    "https://www.amazon.com/*",
    "https://www.amazon.co.uk/*",
    "https://www.ebay.com/*",
    "https://www.tiktok.com/shop/*",
    "https://www.tiktokshop.com/*"
  ],
  "content_scripts": [
    {
      "matches": ["https://www.amazon.com/dp/*", "https://www.amazon.com/gp/*"],
      "js": ["content_amazon.js"]
    },
    {
      "matches": ["https://www.ebay.com/itm/*"],
      "js": ["content_ebay.js"]
    },
    {
      "matches": ["https://www.tiktok.com/shop/*"],
      "js": ["content_tiktok.js"]
    }
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html"
  }
}
```

**Injected UI — Amazon product page:**
Below the price, inject a collapsible panel:

```
┌──────────────────────────────────────────────┐
│ PriceTrackr                                  │
│ Current: $34.99  ↕ Average: $31.20           │
│ 📉 Price is 12% ABOVE average                │
│ ─────────────────────────────────────────── │
│ [90-day price chart — sparkline]             │
│ Best: $27.99 (Jan 12)  Worst: $39.99 (Dec 3) │
│ ─────────────────────────────────────────── │
│ 🔔 Alert me at: [$____] [SET ALERT]          │
│ ─────────────────────────────────────────── │
│ Reseller: buy at $27 → sell at $34.99        │
│ FBA fees: ~$7.30  Profit: $0.39  ROI: 1.4%  │
│ [Open profit calculator]                     │
└──────────────────────────────────────────────┘
```

**Price alert system:**
- User sets target price on any product
- Extension background service_worker checks price every 6 hours (via Keepa API for Amazon)
- Chrome notification fires: "Amazon price alert: [product name] dropped to $28.99 — your target: $29.00"
- Click notification → opens product page

**Monetization:**
- Free: 5 tracked products, price history chart, 2 price alerts
- PriceTrackr Pro: $4.99/month or $34.99/year (unlimited tracking, unlimited alerts, profit calculator, TikTok Shop, eBay support, Google Sheets export)
- Reseller tier: $9.99/month (FBA fee calculator, bulk ASIN import, Keepa data without needing own Keepa subscription)

**Revenue math:**
- 20,000 installs (large TAM — any online shopper) × 5% paid = 1,000 × $4.99 = $4,990/month
- Reseller tier: 200 × $9.99 = $1,998/month
- Total: ~$7,000/month at 20,200 paying customers

**API cost breakdown:**
- Keepa API: $19/month flat for unlimited requests on free tier
- At scale: Keepa Pro plan needed ($100-200/month) but offset by revenue easily

**Chrome Web Store listing:**

Title: PriceTrackr — Amazon Price History & Alerts

Short description:
See 90-day price history on Amazon, eBay, and TikTok Shop. Set price alerts. Built-in FBA profit calculator.

Category: Shopping

**Competition:**
- Honey: focused on coupons, no reseller tools, no TikTok Shop
- CamelCamelCamel browser extension: Amazon only, dated UI
- Keepa: subscription service, better data but no UI injection on page, $19/month
- **Win on:** TikTok Shop support, reseller profit calculator, cleaner UI

---

## Chrome Extension Development Notes

**Manifest v3 key differences from v2:**
- Background scripts replaced by service workers (ephemeral, can sleep)
- `webRequest` blocking replaced by `declarativeNetRequest` (more restrictive but faster)
- Remote code execution (eval, remotely hosted JS) is banned — all code must be bundled
- `chrome.tabs.executeScript` replaced by `chrome.scripting.executeScript`
- Service workers don't have DOM access — use message passing to/from content scripts

**Message passing pattern (background ↔ content script):**
```javascript
// content script → background
chrome.runtime.sendMessage({action: 'fetchPriceHistory', asin: 'B07XYZ'}, (response) => {
  renderChart(response.data);
});

// background.js service worker
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'fetchPriceHistory') {
    fetchKeepa(message.asin).then(data => sendResponse({data}));
    return true; // keeps channel open for async response
  }
});
```

**Storage:**
- `chrome.storage.local`: up to 10MB, local to device, fast
- `chrome.storage.sync`: up to 100KB, syncs across Chrome profiles
- Use sync for: settings, small preferences, tracked items (under 100KB)
- Use local for: cached price data, history charts

**Publishing checklist:**
1. Create Google Developer account ($5 one-time registration fee)
2. Generate icons: 16x16, 48x48, 128x128 PNG (transparent background)
3. Create screenshots: 1280x800 or 640x400 for Chrome Web Store
4. Privacy policy required: host on your domain, link in listing
5. Review time: 1-3 business days for new extensions
6. Updates: typically same day review for existing published extensions

**Monetization implementation options:**
| Method | Pros | Cons |
|--------|------|-------|
| Lemon Squeezy | Easy, no Chrome Pay needed | Redirect outside extension |
| Stripe | Full control | Complex implementation |
| Chrome Web Store Payments | Native in-browser | 30% fee, limited countries |
| License key system | Simple | No auto-renewal |

**Recommended approach:**
- Lemon Squeezy for checkout (user clicks "Go Pro" → opens Lemon Squeezy checkout in new tab)
- After payment: Lemon Squeezy webhook sends license key to your server
- Extension validates license key against your API on each load
- Store license key in `chrome.storage.local`

**SEO for Chrome Web Store:**
- Title: include primary keyword (Site Blocker, Price History, LinkedIn Outreach)
- Description: keyword density matters, first 200 chars are critical
- Reviews: ask for reviews via in-extension prompt after 10 uses
- Screenshots: show the actual UI in use, not marketing graphics
- Promotional tile (440x280): shown in featured sections — invest in design here

**Development tools:**
- Plasmo framework: best DX for Chrome extension development (React-based, hot reload)
- WXT: alternative to Plasmo, lighter weight
- CRXJS: Vite plugin for Chrome extensions
- Without framework: vanilla JS + webpack/esbuild works fine for simpler extensions
