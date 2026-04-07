# PRD: Pocket Alexandria — Production-Quality App Spec
# Version: 1.0 — Full Edge-Case Hardened
# Date: 2026-04-07
# Status: READY FOR ONE-SHOT BUILD

> This spec covers every screen, every edge case, every gating boundary, and every App Store
> requirement. An agent reading ONLY this doc should be able to build or audit Pocket Alexandria
> to production quality without asking clarifying questions.

---

## 1. APP OVERVIEW

**Name:** Pocket Alexandria
**Bundle ID:** com.printmaxx.pocketalexandria
**Tagline:** Classic Texts & Esoteric Library
**Category:** Books (primary), Education (secondary)
**Target User:** Readers who want public-domain classics — philosophy, sacred texts, psychology, hermetic tradition, esoterica — in a beautiful mobile reader. Niche appeal: self-improvement readers, philosophy students, people curious about occult/esoteric texts, religious studies.
**Monetization:** Stripe Payment Links — Annual $9.99 (https://buy.stripe.com/6oU5kE4DC5Fz1Pbdj93F60B), Monthly $1.99 (https://buy.stripe.com/dRm4gA7PO8RLalH5QH3F60C)
**Free Tier:** First 10 books (IDs 1-10), night reader theme only, bookmarks, progress tracking
**Premium Tier:** All 156 books, all 3 reader themes (night/sepia/day), highlights, notes, offline downloads
**Version:** 1.0.0 / Build 1

---

## 2. TECH STACK

| Layer | Library | Version |
|-------|---------|---------|
| Framework | Expo SDK | ~52.0.0 |
| Router | expo-router | ~4.0.0 |
| Language | TypeScript strict | ^5.3.0 |
| React | react / react-native | 18.3.1 / 0.76.7 |
| Navigation | expo-router (file-based) + @react-navigation/native-stack | 7.x |
| Tab Bar | @react-navigation/bottom-tabs via expo-router Tabs | 7.x |
| State | React hooks + AsyncStorage (local-first, no remote DB) | — |
| Storage | @react-native-async-storage/async-storage | 1.23.1 |
| File system | expo-file-system (book download + cache) | ~18.0.0 |
| Fonts | expo-font + Georgia (system serif) | ~13.0.0 |
| Gestures | react-native-gesture-handler | ~2.20.0 |
| Animations | react-native-reanimated | ~3.16.0 |
| Safe area | react-native-safe-area-context | 4.12.0 |
| Haptics | expo-haptics | ~14.0.1 |
| Audio | expo-av (no active audio use; installed for potential future use) | ~15.0.2 |
| Review prompt | expo-store-review | ~8.0.1 |
| Deep linking | expo-linking | ~7.0.5 |
| Icons | @expo/vector-icons (Ionicons) | ^14.0.0 |
| Payment | Stripe Payment Links via Linking.openURL (no SDK installed) | — |
| New Architecture | enabled (newArchEnabled: true) | — |

**Build command (native required):**
```bash
npx expo prebuild --platform ios && npx expo run:ios
```
Never use `expo start --ios` — Reanimated 3.16 requires native build.

**babel.config.js:** Uses only `babel-preset-expo`. No reanimated plugin entry. Verify Reanimated works with SDK 52's built-in support or add plugin if crashes occur.

---

## 3. DATA TYPES (canonical)

```typescript
// src/types/index.ts

interface Book {
  id: string;              // '1' through '156' (numeric string)
  title: string;
  author: string;
  year: number;
  category: string;        // one of the 10 category constants
  subcategory: string;
  url: string;             // Project Gutenberg or sacred-texts.com URL
  description: string;
  free?: boolean;          // annotated flag (not actually used in gating logic)
}

interface BookProgress {
  bookId: string;
  currentPage: number;
  totalPages: number;
  percentComplete: number; // 0-100
  lastReadAt: string;      // ISO 8601
}

interface Bookmark {
  id: string;              // Date.now().toString(36) + 4-char random
  bookId: string;
  page: number;
  label: string;           // 'Page N'
  createdAt: string;       // ISO 8601
}

interface Highlight {
  id: string;
  bookId: string;
  page: number;
  text: string;
  note?: string;
  color: string;
  createdAt: string;
}

interface DailyQuote {
  text: string;
  source: string;
  author: string;
  bookId: string;
}

interface ReadingStats {
  booksStarted: number;
  booksCompleted: number;
  totalPagesRead: number;
  totalTimeMinutes: number;   // NOTE: never actually updated (P1 bug — see Known Gaps)
  favoriteCategory: string;   // NOTE: never actually set (P1 bug)
}

type ReaderTheme = 'night' | 'sepia' | 'day';

interface ReaderSettings {
  fontSize: number;    // default 17, range 12-28
  theme: ReaderTheme;  // default 'night'
  lineHeight: number;  // default 1.7, range 1.2-2.2, step 0.1
}

interface OnboardingState {
  completed: boolean;
  selectedCategories: string[];
  isPremium: boolean;
}
```

---

## 4. CONSTANTS

```typescript
// Gating
FREE_BOOK_LIMIT = 10           // books with id <= 10 are free
CHARS_PER_PAGE = 2400          // at default font size 17; scales as (17/fontSize)*2400

// Pricing
STRIPE_ANNUAL_URL  = 'https://buy.stripe.com/6oU5kE4DC5Fz1Pbdj93F60B'
STRIPE_MONTHLY_URL = 'https://buy.stripe.com/dRm4gA7PO8RLalH5QH3F60C'
ANNUAL_PRICE_STRING  = '$9.99/year'
MONTHLY_PRICE_STRING = '$1.99/month'

// AsyncStorage keys
PREMIUM_CACHE_KEY      = '@pocket_alexandria_premium'    // 'true' | 'false' | null
PROGRESS_PREFIX        = '@pa_progress_'
BOOKMARKS_KEY          = '@pa_bookmarks'
HIGHLIGHTS_KEY         = '@pa_highlights'
SETTINGS_KEY           = '@pa_settings'
STATS_KEY              = '@pa_stats'
LIBRARY_KEY            = '@pa_library'
RECENT_KEY             = '@pa_recent'                    // up to 20 IDs
ONBOARDING_KEY         = '@pa_onboarding'
RECENT_SEARCHES_KEY    = '@pa_recent_searches'           // up to 10 queries
DAILY_QUOTE_DATE_KEY   = '@pa_daily_quote_date'
DAILY_QUOTE_INDEX_KEY  = '@pa_daily_quote_index'
COMPLETED_BOOKS_KEY    = '@pa_completed_books'
ONBOARDING_PREFS_KEY   = '@pa_onboarding_prefs'          // separate from onboarding state

// Book download directory
BOOKS_DIR = FileSystem.documentDirectory + 'books/'

// Catalog
TOTAL_BOOKS = 156
CATEGORIES  = 10
DAILY_QUOTES = 30+  (in quotes.ts)
ONBOARDING_STEPS = 12
```

---

## 5. NAVIGATION STRUCTURE

The app uses **expo-router** as its primary navigation system. It is NOT a pure react-navigation setup — expo-router wraps react-navigation under the hood with file-based routes.

### File-based Route Tree

```
app/
  _layout.tsx              # Root layout: splash → onboarding → Stack router
  (tabs)/
    _layout.tsx            # Tab bar definition (5 tabs)
    index.tsx              # Library tab (home)
    browse.tsx             # Browse tab
    reading.tsx            # Reading (in-progress/bookmarks) tab
    search.tsx             # Search tab
    settings.tsx           # Settings tab
  reader/
    [bookId].tsx           # Full-screen reader (modal presentation)
```

### Root Layout Flow (`app/_layout.tsx`)

```
App launch
  ↓ initPurchases() + checkEntitlements() + getOnboardingState()
  ↓
  ┌─ hasChecked=false → blank screen with StatusBar
  ├─ showSplash=true → AnimatedSplash → onFinish → showSplash=false
  ├─ showOnboarding=true → OnboardingFlow → onComplete → showOnboarding=false
  └─ normal → Stack (tabs + reader modal)
```

### Navigation APIs Used

- **expo-router:** `useRouter()`, `router.push('/reader/ID')`, `router.back()` — used in tab screens
- **react-navigation:** `useNavigation<NativeStackNavigationProp>()`, `navigation.navigate('Reader', { bookId })` — used in `src/screens/` (legacy screen files)
- **IMPORTANT:** Both navigation APIs exist. The `app/(tabs)/` files use expo-router. The `src/screens/` files use react-navigation hooks. This dual-system works because expo-router wraps react-navigation, but `navigation.navigate('Reader', ...)` from src/screens calls the Stack screen named "Reader" which expo-router resolves to `reader/[bookId]`.

### Tab Order

| Index | Route | Icon | Label |
|-------|-------|------|-------|
| 0 | (tabs)/index | library / library-outline | Library |
| 1 | (tabs)/browse | compass / compass-outline | Browse |
| 2 | (tabs)/reading | book / book-outline | Reading |
| 3 | (tabs)/search | search / search-outline | Search |
| 4 | (tabs)/settings | settings / settings-outline | Settings |

### Stack Screens (above tabs)

| Screen | Route | Presentation | Animation |
|--------|-------|-------------|-----------|
| (tabs) | (tabs) | default | default |
| Reader | reader/[bookId] | fullScreenModal | slide_from_bottom |

---

## 6. BOOK CATALOG

### Catalog Stats
- **Total books:** 156 (IDs '1' through '156')
- **Total categories:** 10
- **Source file:** `src/data/catalog.ts`
- **Format:** Hardcoded TypeScript array (no network request needed for catalog)

### Categories (10)
| Category | Icon (Unicode) | Books (approx) |
|----------|----------------|---------------|
| Sacred Texts | ✡ (U+2721) | 18 |
| Philosophy | ☇ (U+2687) | 22 |
| Hermetic / Occult | ☉ (U+2609) | 28 |
| Psychology | Ψ (U+03A8) | 9 |
| Apocrypha | ✝ (U+271D) | 11 |
| Astrology / Divination | ☆ (U+2606) | 5 |
| Eastern Wisdom | ☸ (U+2638) | 12 |
| Secret Societies | △ (U+25B3) | 9 |
| Alchemy / Mysticism | ⚗ (U+2697) | 16 |
| Forbidden / Controversial | ☠ (U+2620) | 14 |

### Free Tier Books (IDs 1-10)
| ID | Title | Author | Source |
|----|-------|--------|--------|
| 1 | King James Bible | Various | gutenberg.org |
| 2 | Douay-Rheims Bible | Various | gutenberg.org |
| 3 | The Book of Mormon | Joseph Smith | gutenberg.org |
| 4 | The Quran (Palmer) | Muhammad/E.H. Palmer | gutenberg.org |
| 5 | The Quran (Rodwell) | Muhammad/J.M. Rodwell | gutenberg.org |
| 6 | Bhagavad Gita | Vyasa/Edwin Arnold | gutenberg.org |
| 7 | The Upanishads | Various/F. Max Muller | gutenberg.org |
| 8 | The Vedanta Sutras | Badarayana/G. Thibaut | sacred-texts.com |
| 9 | Tao Te Ching | Lao Tzu | gutenberg.org |
| 10 | The Dhammapada | Buddha/F. Max Muller | gutenberg.org |

### URL Sources
- **Primary:** `https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt` — direct plain text
- **Secondary:** `https://www.sacred-texts.com/...` — HTML, requires stripping (IDs 8, 21, 29, 64, 65, 66, 67, 68, etc.)
- Mixed formats: ~120 books are gutenberg .txt, ~36 are sacred-texts HTML

### URL Reachability Status
The catalog URLs have NOT been verified for reachability at spec creation time. Project Gutenberg cache URLs are stable. Sacred-texts.com URLs may return HTML index pages instead of raw text for some entries (e.g., ID 70 points to `sacred-texts.com/gno/index.htm` which is a category index, not a single text). See Known Gaps section.

### Book Download Logic (`src/services/bookDownloader.ts`)
1. Check if premium required (ID > 10 + not premium → throw 'PREMIUM_REQUIRED')
2. Ensure `FileSystem.documentDirectory + 'books/'` directory exists
3. If file already exists at `books/{bookId}.txt` → return cached content
4. Fetch from `book.url` with User-Agent header
5. If HTML response (starts with `<` or URL ends `.htm`/`.html`) → `stripHtml()`
6. Strip Gutenberg header/footer with `cleanGutenbergText()`
7. Write to `books/{bookId}.txt`
8. Call `addToLibrary(bookId)` to track in `@pa_library`
9. Return text string

### HTML Stripping
`stripHtml()` in bookDownloader.ts: removes `<script>/<style>`, converts `<br>/<p>/<div>/<h1-6>` to newlines, strips remaining tags, decodes HTML entities.

### Gutenberg Cleaning
`cleanGutenbergText()`: strips from `*** START OF...` to `*** END OF...` markers.

---

## 7. READER SYSTEM

### Pagination Algorithm
- Base: `CHARS_PER_PAGE = 2400` characters
- Adjusted for font size: `adjustedChars = Math.round(2400 * (17 / fontSize))`
- Break preference: paragraph boundary (`\n\n`) if within last 30% of chunk
- Fallback: sentence boundary (`. `) if within last 30%
- Fallback: hard cut at `adjustedChars`
- Pages stored as `string[]` in component state

### Page Navigation
- **Tap left third:** prev page
- **Tap right third:** next page
- **Tap center third:** toggle controls overlay
- **Swipe left (dx < -50):** next page (expo-router reader uses PanResponder)
- **Swipe right (dx > 50):** prev page
- `goToPage(n)` clamps to [0, pages.length-1], scrolls to top

### Reader Themes
| Theme | Background | Text | Accent | Surface |
|-------|-----------|------|--------|---------|
| night (default) | #0D0D1A | #C8C0B0 | #C9A96E | #141428 |
| sepia | #F4E8D1 | #3A2F20 | #8B6914 | #EDE0C8 |
| day | #FAFAF5 | #2C2C2C | #8B6914 | #F0F0EB |

**Free gate:** Free users are locked to `night` theme only. In `app/reader/[bookId].tsx`:
```typescript
setTheme(premium ? settings.theme : 'night');
```
The Settings screen shows all 3 theme options regardless of tier (no lock shown there), but the reader enforces night-only on load.

### Font Size
- Range: 12-28 (inclusive), increment/decrement by 1
- Default: 17
- Persisted to `@pa_settings` immediately on change in both reader and settings

### Line Height
- Range: 1.2-2.2, step 0.1
- Default: 1.7
- Persisted to `@pa_settings`

### Bookmarks
- Available to ALL tiers (free + premium)
- One bookmark per page (checking `bm.some(b => b.page === currentPage)` to toggle)
- In `app/reader/[bookId].tsx`: toggle button in controls overlay, fills when page is bookmarked
- Stored in `@pa_bookmarks` (single JSON array for all books)
- Label: `'Page N'` where N = currentPage + 1

### Highlights (Premium only)
- Gate: `if (!isPremium) { Alert.alert('Premium Feature'...) }`
- Stored in `@pa_highlights`
- Color field exists in type but no color picker UI implemented (P2 gap)
- `app/reader/[bookId].tsx` has a "highlight page" button that saves entire page text as highlight

### Progress Persistence
- Saved on every page change (useEffect on currentPage)
- Key: `@pa_progress_{bookId}`
- On re-open: restores from saved `currentPage` if valid (> 0 and < pages.length)

### Store Review Prompt
- Triggered at 95% completion of a book (in `src/screens/ReaderScreen.tsx`)
- Fires only on 1st or 3rd completion
- Uses `expo-store-review`
- NOT present in `app/reader/[bookId].tsx` (the active reader for expo-router) — P1 gap

### Controls Overlay
Controls appear when user taps center of screen. Includes:
- Back button (top left)
- Book title + "Page N of M" (top center)
- Bookmark toggle button (top right)
- Font size controls (−/Aa/+)
- Theme picker (3 swatches)
- Bookmarks modal toggle
- Highlights modal toggle (premium gated)

---

## 8. ONBOARDING FLOW (12 steps)

**Total steps:** `TOTAL_STEPS = 12` (steps 0-11)
**Progress bar:** fills `(step+1)/12 * 100%`
**Transitions:** slide + fade animation (150ms out, 250ms in)
**Back navigation:** visible on steps 1-11, hidden on step 0

### Step-by-step

| Step | Screen | Content | Gate |
|------|--------|---------|------|
| 0 | Welcome | Book stack illustration, "Your Personal Library of Classics", 156 texts tagline | CTA: "Begin Your Journey" |
| 1 | Reading Goal | 4 radio options: Read more classics / Build daily habit / Explore new genres / Finish started books | Required (disabled CTA if none selected) |
| 2 | Favorite Genres | 8-chip multi-select grid: Fiction, Philosophy, Science & Mind, Poetry, History, Adventure, Mysticism, Divination | Requires ≥1 (disabled CTA) |
| 3 | Reading Pace | 3 radio options: Casual / Regular / Fast | Required |
| 4 | Daily Time | 4 radio options: 15min / 30min / 45min / 60min+ | Required |
| 5 | Projection | Animated bar chart showing books/year projection, pages/day, days/book | CTA: "See My Recommendations" |
| 6 | Book Preview | Grid of up to 6 recommended books + first book highlight (based on genre selections) | CTA: "Continue" |
| 7 | Social Proof | "8,000+ readers", 4.7 stars, 3 testimonials (Sarah M., James K., Aisha R.) | CTA: "Continue" |
| 8 | Feature Showcase | Mini reader mockup + 5 feature rows (Night Mode, Bookmarks, Reading Tracker, Offline, Themes) | CTA: "Continue" |
| 9 | Notification Permission | Notification preview mock, "Enable Reminders" / "Maybe Later" | Optional (skip allowed) |
| 10 | Plan Ready | Summary: first book, daily goal, yearly projection, genres | CTA: "Unlock My Library" |
| 11 | Paywall | Stripe payment links, plan selector, rescue offer on decline | CTA: "Start My Free Trial" |

### Projection Calculation (step 5)
`getReadingProjection(readingSpeed, dailyTime)` — not shown in excerpt but computed from readingSpeed (casual/regular/fast) and dailyTime ('15'/'30'/'45'/'60') to produce `{ booksPerYear, pagesPerDay, daysPerBook }`.

### Genre-to-Category Mapping
```typescript
fiction    → ['Sacred Texts']
philosophy → ['Philosophy']
science    → ['Psychology']
poetry     → ['Eastern Wisdom']
history    → ['Secret Societies', 'Forbidden / Controversial']
adventure  → ['Philosophy']
mysticism  → ['Hermetic / Occult', 'Alchemy / Mysticism']
divination → ['Astrology / Divination', 'Apocrypha']
```

### Paywall (Step 11) Details
- Default plan: annual (pre-selected)
- Monthly shown first as anchor price ($1.99/month — but fallback text shows '$3.99/month' — P1 price inconsistency)
- Annual shown second with "BEST VALUE" badge, "Save 83%"
- Trial timeline: Today (Free access) → Day 2 (Reminder) → Day 3 (Billing starts)
- "No payment due now" note
- Free tier note: "10 books, night theme only"
- Benefits list: "Full 50+ book library" (inaccurate — actually 156 books; P1 copy bug), all themes, reading plans, offline, bookmarks+highlights+notes
- Legal text: "3-day free trial, then $9.99/year or $1.99/month"
- Links: Privacy · Terms · Support
- CTA: "Start My Free Trial" → opens Stripe URL in browser
- Skip: "Continue with Free" → first press shows rescue offer, second press skips to app

### Rescue Offer (shown on first "Continue with Free" press)
- Shows before allowing free entry
- Price: $6.99/year (30% off $9.99)
- Detail: $0.58/month
- CTA: "Claim This Offer" → same purchase flow
- Secondary: "No thanks, continue free" → completes onboarding without purchase

### Purchase Flow
1. `purchasePackage(pkg)` called
2. `Linking.openURL(stripeUrl)` opens browser
3. App listens for `AppState 'active'` event (user returns to app)
4. Alert: "Did you finish the payment successfully?" Yes/No
5. If Yes: `AsyncStorage.setItem('@pocket_alexandria_premium', 'true')`
6. `saveOnboardingState({ isPremium: true })` + complete onboarding

### CRITICAL PURCHASE GAP
The purchase confirmation relies entirely on user self-reporting ("Did you finish the payment?"). There is NO Stripe webhook, NO server-side verification, NO RevenueCat entitlement check. A user can tap "Yes" without paying and get premium access. This is by design (same as other PRINTMAXX apps) but is a fraud risk. The `isPremium` state persists to AsyncStorage and is never re-verified.

### Onboarding Completion Storage
```typescript
// Stored at KEYS.ONBOARDING (@pa_onboarding)
{ completed: true, selectedCategories: string[], isPremium: boolean }

// Stored at @pa_onboarding_prefs (separate key)
{ readingGoal, selectedGenres, readingSpeed, dailyTime, notifGranted, savedAt }
```

---

## 9. SCREEN-BY-SCREEN SPEC

### 9.1 Library Tab (`app/(tabs)/index.tsx`)

**Header:**
- Time-based greeting ("Good morning/afternoon/evening")
- Title: "Your Library" (serif bold)
- Stats row: 4 cards — Books (downloaded count), Reading (in-progress count), Finished (completed count), Pages (sum of currentPage values)

**Body sections (in order):**
1. **Daily Wisdom Quote** (DailyQuoteCard) — one quote per day, persisted by date, tapping opens that book's reader
2. **Continue Reading** — horizontal FlatList of in-progress books (0% < progress < 95%), sorted by most recent `lastReadAt`, each showing BookCover + title + author + progress bar + percentage
3. **Recently Viewed** — horizontal FlatList of last 10 opened books (from `@pa_recent`)
4. **Empty state** (when no downloaded, no recent, no in-progress) — "Welcome, Seeker" + "Browse Collection" button that routes to `/(tabs)/browse`
5. **Featured categories** (empty state only) — first 3 categories, 5 books each, horizontal scrollable
6. **Your Library** section header (when downloaded books exist) + 3-column grid of downloaded BookCovers

**Pull to refresh:** reloads all async data

**Edge cases:**
- No recent books AND no downloads AND no progress → show empty state + featured categories
- Has downloaded books → show "Your Library" grid below all sections
- A book in "continue reading" that was downloaded but deleted from cache → still shows in list (progress persists); tapping opens reader which re-downloads

### 9.2 Browse Tab (`app/(tabs)/browse.tsx` / `src/screens/BrowseScreen.tsx`)

**Structure:** SectionList with one section per category (10 sections)

**Each category section:**
- Header: category icon (unicode) + category name + chevron (expand/collapse)
- Expanded state: horizontal FlatList of books in that category

**Book item display:** BookListItem component — shows lock icon overlay if book is locked

**Lock logic:**
```typescript
const isBookLocked = (book: Book): boolean => {
  if (isPremium) return false;
  return parseInt(book.id, 10) > FREE_BOOK_LIMIT;  // > 10
};
```

**Tapping a locked book:**
- Alert: "Premium Required" with 3 buttons: Cancel / Upgrade / Restore
- Upgrade: opens annual package Stripe URL
- Restore: calls `restorePurchases()` (self-reported confirm dialog)

**Tapping an unlocked book:** `navigation.navigate('Reader', { bookId })`

**Note:** Browse tab file `app/(tabs)/browse.tsx` exists but the main logic is in `src/screens/BrowseScreen.tsx` which uses react-navigation's `useNavigation`. The expo-router `browse.tsx` likely renders BrowseScreen.

### 9.3 Reading Tab (`app/(tabs)/reading.tsx` / `src/screens/ReadingScreen.tsx`)

**Sections:**
1. In Progress — books with 0% < progress < 95%, sorted by most recent
2. Completed — books with progress ≥ 95%, sorted by most recent
3. Bookmarks — all bookmarks across all books, sorted by createdAt descending, showing book title

**Each in-progress item:** BookListItem with progress percentage
**Each completed item:** BookListItem with checkmark
**Each bookmark item:** Bookmark icon + "Page N" + book title → tapping opens reader at that page

**Empty state:** message when all sections are empty

**Refresh:** pull-to-refresh reloads all data (useFocusEffect also fires on tab focus)

### 9.4 Search Tab (`app/(tabs)/search.tsx` / `src/screens/SearchScreen.tsx`)

**Search input:** TextInput, minimum 2 characters to trigger search
**Search scope:**
1. Title match (fast, catalog scan)
2. Author match (fast, catalog scan)
3. Description match (fast, catalog scan)
4. Content match (slow, reads downloaded .txt files from FileSystem for each book not already found)

**Result types:** SearchResult with `{ book, matchType: 'title'|'author'|'description'|'content', snippet? }`
- Content matches include 160-char snippet with query highlighted context (`...before query after...`)

**Display:** SearchResult sorted by matchType priority (title first, then author, description, content)

**No results state:** shown after search with zero results

**Recent searches:** stored in `@pa_recent_searches` (last 10), shown when search field is empty

**Edge cases:**
- Search while no books downloaded → only metadata matches (title/author/description), no content matches
- Very long query (>160 chars) — no special handling; search still works

### 9.5 Settings Tab (`app/(tabs)/settings.tsx` / `src/screens/SettingsScreen.tsx`)

**Sections:**

**READING STATISTICS**
- Books Opened (count from `getAllProgress()`)
- Completed
- In Collection (always 156)
- Total pages read
- Cache size (formatted bytes)

**READER**
- Font Size: stepper (−/17/+), range 12-28
- Line Spacing: stepper (−/1.7/+), range 1.2-2.2 step 0.1
- Reading Theme: 3 swatches (Night/Sepia/Day), each showing "Aa" preview
- Live preview card at bottom of section

**DOWNLOAD MANAGEMENT**
- Cache size display + "Clear Cache" destructive button
- "Download All Books" — iterates all 156 books, calls `downloadBook()` with progress counter; skips premium gate for premium users only (NOTE: the download loop in Settings calls `downloadBook(book)` which will throw PREMIUM_REQUIRED for books > 10 if free user — P1 bug)

**SUBSCRIPTION**
- Status: "Premium" (gold diamond icon) or "Free" (outline)
- If free: row showing "Upgrade to Premium" with chevron (tapping does NOT navigate to paywall — P1 gap, it shows the setting row but has no onPress)
- Restore Purchases button

**APP**
- "Show Onboarding Again" — calls `resetOnboarding()`, shows alert

**LEGAL**
- Privacy Policy → `printmaxx-privacy.surge.sh`
- Terms of Service → `printmaxx-tos.surge.sh`
- Support → `pocket-alexandria.surge.sh/support` (NOTE: this URL may not exist — P1 gap)
- About (version, etc.)

### 9.6 Reader Screen (`app/reader/[bookId].tsx`)

This is the PRIMARY reader (expo-router version). The `src/screens/ReaderScreen.tsx` is a duplicate/legacy file that is NOT used in the current navigation flow.

**Load sequence:**
1. Get `bookId` from `useLocalSearchParams`
2. Load settings + isPremium (parallel)
3. Lock theme to 'night' if !isPremium
4. Check `isBookFree(bookId)` — if !premium AND !free → set error='PREMIUM_REQUIRED', stop
5. Try `getBookText(bookId)` from filesystem
6. If null → `downloadBook(book)` (shows "Downloading..." state)
7. Paginate text on fontSize change
8. Restore reading position from saved progress

**PREMIUM_REQUIRED error state:**
Alert with "Premium Required" and option to go back. No paywall shown inline (P2 gap — user must return to onboarding to upgrade).

**Controls overlay:** animated fade, triggered by center-tap or swipe toggle:
- Top bar: back button, title/page counter, bookmark toggle
- Bottom bar: font size stepper, theme picker, bookmarks modal, highlights modal

**Bookmarks modal:** FlatList of bookmarks for this book, each row shows "Page N" with delete button, tapping jumps to that page

**Highlights modal:** FlatList of highlights for this book (premium only to add, but modal shows existing ones to all users)

**Swipe navigation:** PanResponder — horizontal swipe > 30px dx and < 30px dy triggers; dx < -50 = next, dx > 50 = prev

**Page transition:** opacity + scale animation (0.7 → 1.0, 200ms) on page change

**Progress save:** every page change saves to AsyncStorage

**Edge cases:**
- Book not found (invalid bookId) → shows error message
- Download failure (network error) → shows error with message
- Very short book (1 page) → prev/next are both no-ops (clamped)
- Book at last page → next is no-op
- Premium check fails after being on free tier → PREMIUM_REQUIRED error

---

## 10. FREE vs PRO GATING ENFORCEMENT MATRIX

Every gate is enforced at the point listed. Some redundancy exists (good) but some gaps exist (documented).

| Feature | Free User Gets | Premium Gets | Gate Location | Gate Mechanism |
|---------|---------------|-------------|---------------|----------------|
| Books 1-10 | Full access | Full access | `isBookFree()` check | `parseInt(id) <= 10` |
| Books 11-156 | Blocked | Full access | `downloadBook()` + `reader/[bookId].tsx` | PREMIUM_REQUIRED error |
| Night reader theme | Yes | Yes | `reader/[bookId].tsx` useEffect | `setTheme(premium ? settings.theme : 'night')` |
| Sepia reader theme | No | Yes | `reader/[bookId].tsx` useEffect | locked to 'night' on load |
| Day reader theme | No | Yes | `reader/[bookId].tsx` useEffect | locked to 'night' on load |
| Bookmarks | Yes | Yes | No gate | available to all |
| Highlights (add) | No | Yes | `reader/[bookId].tsx` handleHighlightPage | Alert + early return |
| Highlights (view) | Sees existing | Yes | No gate | show modal to all |
| Offline download (manual) | Books 1-10 | All 156 | `downloadBook()` | PREMIUM_REQUIRED throw |
| "Download All" in Settings | Bug: throws for books >10 | All 156 | `downloadBook()` in loop | same as above |
| Daily quotes | Yes | Yes | No gate | available to all |
| Progress tracking | Yes | Yes | No gate | available to all |
| Reading stats | Yes | Yes | No gate | available to all |

**Grep commands to verify gates:**

```bash
# Verify book gate in downloader
grep -n "isPremiumCached\|FREE_BOOK_LIMIT\|PREMIUM_REQUIRED" MONEY_METHODS/APP_FACTORY/builds/pocket-alexandria/src/services/bookDownloader.ts

# Verify theme gate in reader
grep -n "setTheme\|premium.*night\|night.*premium" MONEY_METHODS/APP_FACTORY/builds/pocket-alexandria/app/reader/\[bookId\].tsx

# Verify highlight gate
grep -n "isPremium\|Premium Feature" MONEY_METHODS/APP_FACTORY/builds/pocket-alexandria/app/reader/\[bookId\].tsx

# Verify browse screen lock
grep -n "isBookLocked\|FREE_BOOK_LIMIT\|isPremium" MONEY_METHODS/APP_FACTORY/builds/pocket-alexandria/src/screens/BrowseScreen.tsx

# Confirm premium reads from AsyncStorage (not hardcoded)
grep -n "isPremiumCached\|@pocket_alexandria_premium" MONEY_METHODS/APP_FACTORY/builds/pocket-alexandria/src/services/purchases.ts
```

---

## 11. PURCHASE FLOW

### Flow Diagram

```
User taps "Start My Free Trial" (paywall step 11) or "Upgrade" (locked book alert)
  ↓
getOfferings() → returns { annual, monthly } from hardcoded Stripe URLs (no network)
  ↓
User selects plan (annual default)
  ↓
purchasePackage(pkg)
  ↓
Linking.openURL(STRIPE_ANNUAL_URL or STRIPE_MONTHLY_URL)
  → Browser opens Stripe checkout
  ↓
AppState event: 'active' (user returns)
  ↓
Alert.alert("Did you finish the payment successfully?")
  → No: throw 'Purchase cancelled by user'
  → Yes: AsyncStorage.setItem('@pocket_alexandria_premium', 'true')
  ↓
Return { entitlements: { active: { premium: { expirationDate: null } } } }
  ↓
Caller: setIsPremium(true) + completeOnboarding()
```

### Restore Flow
```
User taps "Restore Purchases"
  ↓
Alert: "Do you have an active subscription?"
  → No: set '@pocket_alexandria_premium' = 'false', return false
  → Yes: set '@pocket_alexandria_premium' = 'true', return true
```

### entitlement check on app launch
```typescript
// In _layout.tsx:
await initPurchases(); // no-op
await checkEntitlements(); // reads AsyncStorage, doesn't update state
const state = await getOnboardingState();
setShowOnboarding(!state.completed);
```

**CRITICAL GAPS in purchase flow:**
1. `checkEntitlements()` is called on launch but its return value is NOT stored or used to update app state — premium status is re-checked per-screen via `isPremiumCached()`. This is fine but inconsistent.
2. No expiry date tracking — subscription could lapse but premium would remain 'true' in AsyncStorage indefinitely.
3. No receipt validation — any user can tap "Yes" to the payment confirmation dialog without actually paying.
4. `initPurchases()` is a no-op — if RevenueCat is added later, this is the hook point.

---

## 12. COMPONENTS

### BookCover (`src/components/BookCover.tsx`)
- Category-specific gradient backgrounds (10 colors defined)
- Category icon (unicode symbol)
- Renders book title + author text
- Sizes: small (listing), medium (featured), large (reader header)
- Optional progress bar at bottom (free users: no progress bar shown on locked books)

### BookListItem (`src/components/BookListItem.tsx`)
- Used in Browse (category lists) and Reading (in-progress/completed)
- Shows: cover + title + author + category + lock icon if locked

### DailyQuote (`src/components/DailyQuote.tsx`)
- One quote per day, selected from `src/data/quotes.ts` (30+ quotes)
- Date-keyed: changes at midnight, persists index to `@pa_daily_quote_date` + `@pa_daily_quote_index`
- Tapping navigates to the book that quote came from

### AnimatedSplash (`src/components/AnimatedSplash.tsx`)
- Shown immediately after app load
- Calls `onFinish()` when animation completes
- Used in `_layout.tsx` root layout

### SkeletonLoader (`src/components/SkeletonLoader.tsx`)
- Placeholder loading UI (exists but usage not confirmed in all screens)

### SectionHeader (`src/components/SectionHeader.tsx`)
- Used in Library and Reading tabs
- Props: title, subtitle?, icon

---

## 13. QA CHECKLIST

### Functional Tests

**Free User Flow:**
- [ ] Open app fresh install — AnimatedSplash plays, onboarding shows
- [ ] Complete onboarding without purchasing
- [ ] Library tab: empty state shows "Welcome, Seeker"
- [ ] Daily quote shows and tapping opens book 19 (The Kybalion, a free book? — NO, ID 19 > 10, will show PREMIUM_REQUIRED)
- [ ] Browse tab: books 1-10 show no lock icon, books 11+ show lock icon
- [ ] Tap book 1 (KJV Bible) → downloads and opens reader
- [ ] Reader shows night theme only — sepia/day swatches visible but switching them has no effect (theme resets to night on load)
- [ ] Add bookmark in reader → appears in Reading tab
- [ ] Tap book 11 → "Premium Required" alert with 3 buttons
- [ ] Search "meditations" → title match (book 31, ID > 10) shows in results with lock

**Premium User Flow (manually set `@pocket_alexandria_premium` to 'true' in AsyncStorage):**
- [ ] All 156 books accessible
- [ ] Sepia and Day themes work in reader
- [ ] Highlights button in reader does not show premium alert
- [ ] Download All in Settings progresses through all 156

**Purchase Flow:**
- [ ] Tap "Upgrade" on locked book → annual plan Stripe URL opens in browser
- [ ] Return to app → confirmation alert appears
- [ ] Tap "Yes" → premium status set, book opens
- [ ] Restore Purchases → self-report dialog → premium set on "Yes"

**Edge Cases:**
- [ ] Open reader on book with no network and not cached → error state shown
- [ ] Open reader while downloading → "Downloading..." state shows ActivityIndicator
- [ ] Open non-existent bookId (`router.push('/reader/999')`) → error state "book not found"
- [ ] Very long book (Bible) → paginated correctly, progress persists across sessions
- [ ] Font size changed in reader → page count recalculates, position resets to page 0 (P2 issue: should try to maintain position)
- [ ] All bookmarks deleted → Reading tab bookmarks section empty (no crash)
- [ ] Search with query < 2 chars → no results, no crash

### Build Checks
- [ ] `npx tsc --noEmit` passes with 0 errors
- [ ] `npx expo export --platform ios` completes without errors
- [ ] `npx expo prebuild --platform ios` completes without errors
- [ ] App launches on iOS 16+ Simulator
- [ ] No red-screen on cold launch

---

## 14. APP STORE SUBMISSION CHECKLIST

### Bundle & Identity
- [x] Bundle ID: `com.printmaxx.pocketalexandria`
- [x] Version: 1.0.0 / Build 1
- [x] Orientation: portrait only
- [x] `ITSAppUsesNonExemptEncryption: false`
- [ ] App icon: `assets/icon.png` must exist (1024x1024)
- [ ] Splash icon: `assets/splash-icon.png` must exist

### Legal
- [x] Privacy Policy URL: `https://printmaxx-privacy.surge.sh`
- [x] Terms URL: `https://printmaxx-tos.surge.sh`
- [ ] Support URL: `https://pocket-alexandria.surge.sh/support` — **VERIFY THIS EXISTS**
- [ ] Support email: `support@printmaxx.com` — verify inbox is monitored

### Content
- [x] All content is public domain (Project Gutenberg + sacred-texts.com)
- [x] App review notes prepared (in `extra.appReviewNotes`) — states 156 public domain texts
- [ ] Subscription terms displayed on paywall per Apple 3.1.1/3.1.2 — YES, legal text present in paywall
- [ ] "Cancel anytime" disclosure — YES, present
- [ ] Subscription renewal terms — YES, present in legal text

### Apple-Specific
- [x] `supportsTablet: true`
- [ ] Screenshot set for iPhone 6.7" display (required)
- [ ] Screenshot set for iPad (required since supportsTablet: true)
- [ ] App preview video (optional but boosts conversion)

### Potential Rejection Risks
- **4.3 Spam:** Low risk (unique esoteric/occult niche, distinct from common Bible apps)
- **Payment:** App uses Stripe via browser — Apple may reject apps that use external payment for digital content that should use IAP. **HIGH RISK.** Apple's guideline 3.1.1 requires IAP for in-app digital content. A browser redirect to Stripe likely violates this. Mitigation: switch to RevenueCat + Apple IAP before submission, or accept risk and proceed (other apps do this and get rejected eventually). **P0 issue for App Store approval.**
- **Content:** Book ID 156 (Protocols of the Elders of Zion, labeled "Debunked") — Apple may flag antisemitic content even with debunking note. **P1 risk.** Remove or add prominent disclaimer screen before opening.
- **Accuracy claims in marketing:** Paywall says "Full 50+ book library" when it's 156. Will cause Apple reviewer confusion but unlikely rejection.

---

## 15. KNOWN PRODUCTION GAPS

### P0 — Blocks App Store Approval

**P0-1: External Payment for Digital Content (Apple Guideline 3.1.1)**
- **What:** App opens Stripe checkout in browser for content that must use in-app purchases per Apple policy.
- **Where:** `src/services/purchases.ts` — `purchasePackage()` calls `Linking.openURL(STRIPE_URL)`
- **Fix:** Implement RevenueCat with `react-native-purchases` SDK. Create two products in App Store Connect: Annual $9.99, Monthly $1.99. Wire RevenueCat entitlements to replace AsyncStorage-based `isPremiumCached()`. See `03_PLAYBOOKS/APP_FACTORY/REVENUECAT_INTEGRATION_GUIDE.md`.

**P0-2: No Real Premium Verification**
- **What:** Any user can self-report "Yes" to the payment confirmation dialog and get premium access without paying.
- **Where:** `src/services/purchases.ts` lines 111-126
- **Fix:** Eliminated automatically when P0-1 is fixed (RevenueCat handles server-side entitlement verification).

### P1 — Functionality Broken

**P1-1: Daily Quote Navigation Broken for Most Users**
- **What:** DailyQuoteCard tapping opens the book that the quote came from. 26 of 30 quotes reference books with IDs > 10 (e.g., Kybalion = ID 19, Meditations = ID 31). Tapping a quote as a free user hits `PREMIUM_REQUIRED` error in reader.
- **Fix:** Either (a) add upgrade prompt inline instead of PREMIUM_REQUIRED error, or (b) only quote from books 1-10 for free users.

**P1-2: ReadingStats `totalTimeMinutes` Never Updated**
- **What:** `updateStats()` in storage.ts never adds to `totalTimeMinutes`. It's initialized to 0 and stays 0.
- **Where:** `src/services/storage.ts` `updateStats()` function
- **Fix:** Track reading session start time in reader, compute duration on close, call `updateStats()` with elapsed minutes.

**P1-3: ReadingStats `favoriteCategory` Never Set**
- **What:** Always empty string in stats display.
- **Fix:** Derive from category with most pages read when computing stats.

**P1-4: "Download All" in Settings Fails for Free Users**
- **What:** `handleDownloadAll()` iterates all 156 books and calls `downloadBook(book)` which throws `PREMIUM_REQUIRED` for books > 10. The try/catch swallows the error but premium books are never downloaded.
- **Where:** `src/screens/SettingsScreen.tsx` `handleDownloadAll()`
- **Fix:** Gate the "Download All" button: show it only to premium users, or check isPremium before the loop and show upgrade prompt if free.

**P1-5: "Upgrade to Premium" Row in Settings Has No onPress**
- **What:** The row in SettingsScreen showing "Upgrade to Premium" has no handler. Tapping does nothing.
- **Where:** `src/screens/SettingsScreen.tsx` lines 348-355
- **Fix:** Add `onPress` that triggers paywall (either reset onboarding to show paywall again, or show a dedicated upgrade modal).

**P1-6: Store Review Prompt Missing from Active Reader**
- **What:** `expo-store-review` is triggered in `src/screens/ReaderScreen.tsx` but the ACTIVE reader is `app/reader/[bookId].tsx` (expo-router version). The legacy file isn't used.
- **Fix:** Add review prompt to `app/reader/[bookId].tsx` at 95% completion milestone.

**P1-7: Support URL May Not Exist**
- **What:** `https://pocket-alexandria.surge.sh/support` is referenced in app.json and settings screen. `printmaxx-payments.surge.sh` and `printmaxx-privacy.surge.sh` exist (per memory), but `pocket-alexandria.surge.sh` may not.
- **Fix:** Verify and deploy, or change to generic `support@printmaxx.com` mailto link.

**P1-8: Paywall Copy Inconsistency**
- **What:** Monthly plan shows fallback "$3.99/month" in onboarding paywall (line 825: `?? '$3.99/month'`) but actual Stripe price is $1.99/month. If `getOfferings()` fails, wrong price shows.
- **Fix:** Change fallback to `'$1.99/month'`.

**P1-9: Paywall Benefits Copy Inaccurate**
- **What:** Paywall says "Full 50+ book library" when it's 156 books.
- **Where:** `src/screens/OnboardingFlow.tsx` line 860
- **Fix:** Change to "Full 156-book library".

### P2 — Quality Issues

**P2-1: Highlight Color Picker Not Implemented**
- **What:** `Highlight` type has a `color` field but no color picker exists. Color is set to whatever is passed, but the UI for selecting highlight color is absent.
- **Fix:** Add color picker to highlight creation flow, or default to a fixed color.

**P2-2: Font Size Change Resets Position to Page 0**
- **What:** When `fontSize` changes, pagination recalculates and `currentPage` stays at current value which may no longer be valid. The restore-position effect only runs when `pages.length` changes, not when the page content changes. In practice the user ends up on the wrong page.
- **Fix:** On pagination recalculate, find the page that contains the text from the previous position.

**P2-3: Sound Design Missing**
- **What:** No sounds wired anywhere. No SoundEngine, no SoundTouchable wrapper, no tap/success/transition sounds.
- **Fix:** Per app-factory-pipeline rule 14 — implement sound design (tap sounds, page turn sounds, notification success sounds).

**P2-4: No Deep Link Handling at Screen Level**
- **What:** `scheme: 'pocket-alexandria'` is configured in app.json, enabling URLs like `pocket-alexandria://reader/1`. expo-router handles this automatically for valid routes, but no custom deep link handler exists for marketing use cases.
- **Status:** Likely works automatically via expo-router's linking, but not tested.

**P2-5: Dual Screen Files (Legacy + Active)**
- **What:** Both `src/screens/ReaderScreen.tsx` and `app/reader/[bookId].tsx` implement the reader. The `src/screens/BrowseScreen.tsx`, `LibraryScreen.tsx`, `ReadingScreen.tsx`, `SearchScreen.tsx`, `SettingsScreen.tsx` exist alongside `app/(tabs)/*.tsx` files. The app/(tabs) files likely import and render the src/screens versions (need to verify), or they are duplicates.
- **Risk:** If any screen is updated in src/screens/ but the app/(tabs) file has different code, behavior is inconsistent.
- **Fix:** Verify which files are actually rendered. Remove dead code.

**P2-6: No Haptic Feedback Wired**
- **What:** `expo-haptics` is installed but no `Haptics.impactAsync()` calls exist in screens.
- **Fix:** Add haptics to button taps, page turns, bookmark add/remove.

**P2-7: Notification Permission is Fake**
- **What:** Step 9 "Enable Reminders" sets `notifGranted = true` but never calls `Notifications.requestPermissionsAsync()` or schedules any notification. It's a UI-only interaction.
- **Fix:** Either (a) implement push notifications properly with `expo-notifications`, or (b) remove the screen or clearly label it as "coming soon".

---

## 16. SOUND DESIGN REQUIREMENTS

Per app-factory-pipeline rule 14, all apps require sound design. Pocket Alexandria currently has none.

### Required Sounds
| Action | Sound Type | Source Recommendation |
|--------|-----------|----------------------|
| Tab bar tap | light tap (12ms) | Octave iOS taps |
| Page turn (left swipe) | soft page flip | Kenney UI pack |
| Page turn (right swipe) | soft page flip (reverse) | Kenney UI pack |
| Bookmark add | success chime (short) | Octave |
| Bookmark remove | soft click | Octave |
| Onboarding step advance | subtle whoosh | Kenney |
| Purchase success | triumphant short chord | Octave |
| Download complete | notification ding | Octave |
| Error/blocked | short negative tone | Octave |
| Controls overlay show | ambient reveal | custom |

### Implementation Steps
1. Download Octave (iOS) and Kenney UI packs (CC0)
2. Place sounds in `assets/sounds/`
3. Create `src/sounds/SoundEngine.ts` with `expo-av` Audio preloading
4. Create `src/components/SoundTouchable.tsx` wrapper
5. Replace `TouchableOpacity` with `SoundTouchable` in all interactive elements
6. Add `playsInSilentModeIOS: true` in Audio mode setup
7. Verify: `grep -rn "playSound\|SoundTouchable" src/screens/ app/` must show calls in every file

---

## 17. DEEP LINKING CONFIGURATION

### URL Scheme
- Scheme: `pocket-alexandria` (configured in `app.json`)
- Associated domain: not configured (no universal links)

### Supported Routes (via expo-router auto-handling)
```
pocket-alexandria:///             → Library tab
pocket-alexandria:///browse       → Browse tab
pocket-alexandria:///reading      → Reading tab
pocket-alexandria:///search       → Search tab
pocket-alabama:///settings       → Settings tab
pocket-alexandria:///reader/1    → Open KJV Bible in reader
pocket-alexandria:///reader/19   → Open The Kybalion in reader (premium gate applies)
```

### Test Deep Links
```bash
xcrun simctl openurl booted "pocket-alexandria:///reader/1"
xcrun simctl openurl booted "pocket-alexandria:///reader/31"
xcrun simctl openurl booted "pocket-alexandria:///"
xcrun simctl openurl booted "pocket-alexandria:///browse"
```

---

## 18. ARCHITECTURE DECISIONS & RATIONALE

### Why expo-router + react-navigation coexist
The app was originally built with react-navigation (src/screens/ files), then migrated to expo-router (app/ files). The migration was incomplete. The src/screens/ files use `useNavigation()` which still works because expo-router wraps react-navigation and registers the same screen names. This is technical debt but functional.

### Why no RevenueCat (yet)
Stripe Payment Links were used for faster initial development. RevenueCat is the intended upgrade path at $1K MRR per project strategy docs. The `initPurchases()` no-op and RevenueCat API key placeholder (`appl_REPLACE_WITH_YOUR_PUBLIC_KEY` in app.json) confirm this intent.

### Why AsyncStorage for premium state
No server, no user accounts, local-first approach. Simple but insecure (see P0-2). Acceptable trade-off pre-IAP implementation.

### Why 156 books are all public domain
Eliminates copyright risk entirely. Project Gutenberg + sacred-texts.com are established public domain archives. Content is free. App value is curation + UX.

---

## 19. FILE REFERENCE MAP

```
pocket-alexandria/
├── app.json                           # Config, bundle ID, scheme, permissions
├── package.json                       # Dependencies (no RevenueCat, no expo-notifications)
├── babel.config.js                    # babel-preset-expo only
├── tsconfig.json
├── metro.config.js
├── app/
│   ├── _layout.tsx                    # Root: splash → onboarding → Stack
│   ├── (tabs)/
│   │   ├── _layout.tsx                # Tab bar config (5 tabs)
│   │   ├── index.tsx                  # Library tab (ACTIVE)
│   │   ├── browse.tsx                 # Browse tab (renders BrowseScreen?)
│   │   ├── reading.tsx                # Reading tab
│   │   ├── search.tsx                 # Search tab
│   │   └── settings.tsx               # Settings tab
│   └── reader/
│       └── [bookId].tsx               # ACTIVE full-screen reader
├── src/
│   ├── components/
│   │   ├── AnimatedSplash.tsx
│   │   ├── BookCover.tsx
│   │   ├── BookListItem.tsx
│   │   ├── DailyQuote.tsx
│   │   ├── SectionHeader.tsx
│   │   └── SkeletonLoader.tsx
│   ├── constants/
│   │   └── theme.ts                   # colors, fonts, spacing, readerThemes, APP_CONFIG
│   ├── data/
│   │   ├── catalog.ts                 # 156 books, 10 categories, search functions
│   │   └── quotes.ts                  # 30+ daily quotes
│   ├── screens/                       # LEGACY — may or may not be actively rendered
│   │   ├── OnboardingFlow.tsx         # ACTIVE (imported by _layout.tsx)
│   │   ├── BrowseScreen.tsx
│   │   ├── LibraryScreen.tsx
│   │   ├── ReadingScreen.tsx
│   │   ├── ReaderScreen.tsx           # LEGACY (NOT used, replaced by app/reader/[bookId].tsx)
│   │   └── SearchScreen.tsx
│   │   └── SettingsScreen.tsx
│   ├── services/
│   │   ├── bookDownloader.ts          # download, cache, premium gate
│   │   ├── purchases.ts               # Stripe links, AsyncStorage premium state
│   │   └── storage.ts                 # All AsyncStorage operations
│   └── types/
│       └── index.ts                   # Book, BookProgress, Bookmark, Highlight, etc.
└── assets/
    ├── icon.png                       # 1024x1024 (must exist)
    ├── splash-icon.png
    ├── adaptive-icon.png
    └── favicon.png
```

---

## 20. ENVIRONMENT & CONFIGURATION

### No Environment Variables Required
The app has no `.env` file. Stripe URLs are hardcoded in `purchases.ts`. RevenueCat key is a placeholder in `app.json`.

### Required Before Launch
1. Replace `revenueCatApiKey: 'appl_REPLACE_WITH_YOUR_PUBLIC_KEY'` in `app.json` — either with real key or remove (currently unused)
2. Verify `pocket-alexandria.surge.sh/support` is live
3. Verify all 156 book URLs are reachable (especially sacred-texts.com HTML pages)
4. Replace Stripe payment links if test links (current links appear to be live Stripe links based on URL format)
5. Create App Store Connect app with bundle ID `com.printmaxx.pocketalexandria`
6. Generate screenshots for iPhone 6.7" and iPad

### Build Commands (in order)
```bash
cd MONEY_METHODS/APP_FACTORY/builds/pocket-alexandria/
npm install
npx expo prebuild --platform ios --clean
npx expo run:ios
# or for distribution:
eas build --platform ios --profile production
```
