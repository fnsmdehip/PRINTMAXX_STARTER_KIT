# PRD: cnsnt — Production-Quality App Spec
# Version: 2.0 — Full Edge-Case Hardened
# Date: 2026-04-07
# Status: READY FOR ONE-SHOT BUILD

> This spec covers every screen, every edge case, every security boundary, and every
> App Store requirement. An agent reading ONLY this doc should be able to build cnsnt
> to production quality without asking clarifying questions.

---

## 1. APP OVERVIEW

**Name:** cnsnt
**Bundle ID:** com.printmaxx.cnsnt
**Tagline:** Consent. Contracts. Protection.
**Category:** Productivity (primary), Utilities (secondary)
**Target User:** Professionals who need to create, sign, and store consent/liability agreements — personal trainers, photographers, event organizers, landlords, healthcare workers, lawyers, freelancers, and anyone concerned about legal protection.
**Monetization:** Stripe Payment Links — Monthly $4.99, Annual $29.99 (save 50%)
**Free Tier:** 3 total records, 3 basic templates, text only, no PDF/video/audio

---

## 2. TECH STACK

| Layer | Library | Version |
|-------|---------|---------|
| Framework | Expo SDK 50+ | latest |
| Language | TypeScript strict | 5.x |
| Navigation | @react-navigation/native + native-stack + bottom-tabs | 6.x |
| State | React hooks + AsyncStorage | — |
| Encryption | expo-crypto (AES-256-CTR + HMAC-SHA-256) | latest |
| Secure storage | expo-secure-store | latest |
| Biometrics | expo-local-authentication | latest |
| Audio | expo-av | latest |
| Video | expo-camera (CameraView) | latest |
| PDF | expo-print | latest |
| File system | expo-file-system | latest |
| Sharing | expo-sharing | latest |
| Location | expo-location (video GPS stamp) | latest |
| UI icons | @expo/vector-icons (Ionicons) | latest |
| Safe area | react-native-safe-area-context | latest |
| Payment | Stripe Payment Links via Linking.openURL | — |

**Build command (native):**
```bash
npx expo prebuild --platform ios && npx expo run:ios
```
Never use `expo start --ios` — no native modules in Expo Go.

---

## 3. DATA TYPES (canonical)

```typescript
type ConsentStatus = 'active' | 'expired' | 'revoked' | 'draft';
type Entitlement = 'free' | 'pro';
type TemplateCategory = 'medical' | 'legal' | 'business' | 'media' | 'research' | 'property' | 'personal' | 'custom';

interface ConsentRecord {
  id: string;                     // cr_<timestamp36>_<6-char-random>
  templateId: string;
  templateName: string;
  title: string;
  status: ConsentStatus;
  createdAt: string;              // ISO 8601
  expiresAt: string | null;
  revokedAt: string | null;
  parties: PartyInfo[];
  consentText: string;
  signatures: SignatureData[];
  recordingUri: string | null;    // encrypted file URI
  recordingDuration: number | null; // seconds
  pdfUri: string | null;
  documentHash: string | null;    // HMAC-SHA-256 hex
  metadata: Record<string, string>;
}

interface PartyInfo {
  name: string;
  role: string;
  email?: string;
}

interface SignatureData {
  partyName: string;
  signatureImage: string;   // base64 PNG
  timestamp: string;        // ISO 8601
}

interface ConsentTemplate {
  id: string;
  name: string;
  category: TemplateCategory;
  description: string;
  fields: TemplateField[];
  consentText: string;
  requiresDualSignature: boolean;
  defaultExpiryDays: number | null;
  isPremium: boolean;
  icon: string;
}

interface TemplateField {
  key: string;
  label: string;
  placeholder: string;
  type: 'text' | 'date' | 'multiline' | 'email' | 'number';
  required: boolean;
}

interface DashboardStats {
  total: number;
  active: number;
  expired: number;
  revoked: number;
  draft: number;
  expiringSoon: number;      // expires within 7 days
  recentlyCreated: number;   // created in last 7 days
}

type RootStackParamList = {
  Splash: undefined;
  Onboarding: undefined;
  Lock: undefined;
  Main: undefined;
  TemplateForm: { templateId: string };
  ConsentBuilder: { title: string; templateId?: string };
  Recording: { consentId?: string };
  VideoConsent: { consentId?: string; partyA?: string; partyB?: string };
  NDA: undefined;
  Waiver: undefined;
  MutualRelease: undefined;
  PDFPreview: { recordId: string };
  BackupSettings: undefined;
};
```

---

## 4. CONSTANTS (from theme.ts)

```typescript
const FREE_TIER_LIMIT = 3;         // max records on free plan
const PRO_MONTHLY_PRICE = '$4.99/mo';
const PRO_YEARLY_PRICE = '$29.99/yr';
const STRIPE_MONTHLY = 'https://buy.stripe.com/5kQ14o6LK7NH51nend3F60E';
const STRIPE_ANNUAL  = 'https://buy.stripe.com/5kQcN60nm8RL9hDgvl3F60D';
const AUTO_LOCK_OPTIONS = [1, 2, 5, 10, 15, 30]; // minutes
const DEFAULT_AUTO_LOCK = 5;
const VAULT_AUTO_LOCK_MS = 2 * 60 * 1000; // 2 min (vault-level, separate from app-level)
const MAX_PIN_ATTEMPTS = 5;         // before lockout
const PIN_LOCKOUT_SECONDS = 30;
const MAX_VIDEO_SECONDS = 300;      // 5 minutes
const RECORD_ID_PREFIX = 'cr_';
const PBKDF2_ITERATIONS = 100_000;
```

---

## 5. SECURITY ARCHITECTURE

### 5a. Vault (encryption.ts)

**Algorithm:** AES-256-CTR + HMAC-SHA-256 (encrypt-then-MAC)
**Key derivation:** Iterated SHA-256 with 100,000 rounds (simulates PBKDF2)
**Salt:** 32 bytes, cryptographic random via expo-crypto per write operation
**IV:** 16 bytes (128-bit), cryptographic random per write
**Encryption key:** 256-bit (first 32 bytes of derived key material)
**MAC key:** 256-bit (next 32 bytes of derived key material, separate)
**Storage format:** `base64(salt):base64(iv):base64(ciphertext):base64(mac)`
**Vault key storage:** expo-secure-store (NOT AsyncStorage) — Keychain on iOS
**Auto-lock:** 2 minutes inactivity at vault level (separate from app-level lock)

**Key operations:**
- `encryptAndStore(key, plaintext)` — encrypts then MACs, stores in AsyncStorage
- `retrieveAndDecrypt(key)` — retrieves, verifies MAC, decrypts
- `computeDocumentHmac(record)` — keyed HMAC over canonical JSON of all record fields + hashTimestamp (replay attack prevention)

**Edge cases:**
- Vault key lost (SecureStore wiped on app uninstall on some iOS versions): CANNOT recover data. Show "Vault unavailable — your data cannot be decrypted on this device."
- MAC verification failure: record is corrupted. Show "Integrity check failed. This record may have been tampered with."
- expo-crypto unavailable: fallthrough to zero-padded XOR cipher (NEVER — if expo-crypto missing, throw hard error, reject build)
- Key rotation: NOT YET IMPLEMENTED. Document this as known gap.

### 5b. Authentication (auth.ts)

**PIN:** 4 digits. Stored as SHA-256 hash in expo-secure-store.
**PIN lockout:** After MAX_PIN_ATTEMPTS (5) wrong attempts → 30-second cooldown. After 10 total wrong: nuclear wipe option (show alert, require second confirmation).
**Biometric:** expo-local-authentication, Face ID or Touch ID.
**Auto-lock:** Configurable 1–30 minutes. Tracked via AppState events. Resets on foreground.
**First launch:** No PIN set → LockScreen shows PIN setup flow.

**Auth state object:**
```typescript
interface AuthState {
  pinIsSet: boolean;
  hasBiometrics: boolean;       // device has Face ID / Touch ID enrolled
  biometricEnabled: boolean;    // user has enabled it in settings
  failedAttempts: number;
  lockedUntil: number | null;   // timestamp ms
}
```

---

## 6. SERVICES ARCHITECTURE

| Service | File | Purpose |
|---------|------|---------|
| Vault | services/encryption.ts | AES-256-CTR encrypt/decrypt, HMAC |
| Auth | services/auth.ts | PIN + biometric, lockout |
| Database | services/database.ts | Encrypted CRUD for ConsentRecord |
| Audit log | services/auditLog.ts | Append-only action log |
| Cloud backup | services/cloudBackup.ts | iCloud, Google Drive, Dropbox |
| Export | services/export.ts | PDF, CSV, JSON export |
| Purchases | services/purchases.ts | Stripe Payment Links, entitlement |

**Dependency flow:**
```
purchases.ts → AsyncStorage (entitlement cache)
database.ts → encryption.ts → expo-secure-store + AsyncStorage
auth.ts → expo-secure-store + expo-local-authentication
cloudBackup.ts → database.ts + encryption.ts + expo-file-system
export.ts → database.ts + expo-print + expo-sharing
```

---

## 7. NAVIGATION STRUCTURE

```
SplashScreen
  ├── [first launch] → OnboardingFlow
  │     └── [completed] → LockScreen (or Main if no PIN set)
  └── [returning] → LockScreen
        └── [unlocked] → Main (BottomTabs)
              ├── Tab: HomeScreen (Templates)
              │     └── [template selected] → TemplateForm
              │           └── [saved] → PDFPreviewScreen
              ├── Tab: Dashboard (Records)
              │     └── [record selected] → PDFPreviewScreen
              │     └── [record long-press] → Action sheet
              └── Tab: Settings
                    ├── [backup] → BackupSettingsScreen
                    └── [upgrade] → plan selector → Stripe (browser)

Stack screens (modal/push):
  ConsentBuilderScreen   (custom template builder)
  RecordingScreen        (audio consent)
  VideoConsentScreen     (video consent, premium)
  NdaScreen              (NDA template flow)
  WaiverScreen           (liability waiver flow)
  MutualReleaseScreen    (mutual release flow)
```

---

## 8. TEMPLATES (11 total)

| ID | Name | Category | Premium | Dual Sig | Expiry Days |
|----|------|----------|---------|---------|------------|
| tpl_medical_consent | Medical Consent | medical | false | false | 365 |
| tpl_photo_video_release | Photo/Video Release | media | false | false | null |
| tpl_nda | Non-Disclosure Agreement | legal | true | true | 730 |
| tpl_gdpr_consent | GDPR Data Consent | legal | true | false | 365 |
| tpl_research_participation | Research Participation | research | true | false | 180 |
| tpl_property_entry | Property Entry Authorization | property | false | false | null |
| tpl_liability_waiver | Liability Waiver | legal | true | false | null |
| tpl_mutual_release | Mutual Release | legal | true | true | null |
| tpl_personal_consent | Personal Consent Agreement | personal | true | true | null |
| tpl_service_agreement | Service Agreement | business | true | true | 365 |
| tpl_custom | Custom Agreement | custom | true | false | null |

**Free templates (3):** tpl_medical_consent, tpl_photo_video_release, tpl_property_entry
**Premium templates (8):** all others

---

## 9. SCREEN SPECIFICATIONS

### SCREEN 1: SplashScreen (screens/SplashScreen.tsx)

**Purpose:** App boot, asset preload, navigation decision.

**Layout:**
- Full-screen, light gray background (#F8F9FA)
- Center: logo_fullcolor.png + splash_showcase.png
- No loading spinner (fast enough)

**Logic on mount:**
```
1. Initialize purchaseService (loads cached entitlement)
2. Check AsyncStorage: 'cnsnt_onboarding_complete' === 'true'
   - false → navigate('Onboarding')
3. Check auth state via authService.getAuthState()
   - pinIsSet === false AND biometricEnabled === false → navigate('Main')
   - otherwise → navigate('Lock')
```

**Timing:** 1.5 seconds minimum display (feels intentional, not glitchy)

**Edge cases:**
- AsyncStorage read throws → assume first launch → Onboarding
- Vault init throws → navigate to Lock, show "Vault error" banner on Lock screen
- Very fast device skips splash too quickly → enforce 1.5s minimum via setTimeout

---

### SCREEN 2: OnboardingFlow (screens/OnboardingFlow.tsx)

**12 screens, animated slide transitions, progress bar (1-12)**

**Shared UI:**
- Progress bar top: thin bar filling left-to-right, animated
- Back button top-left (hidden on screen 1 and 12)
- Skip button top-right (hidden on screens 1, 11, 12)
- Answers persisted to AsyncStorage key 'cnsnt_onboarding_answers' after each step

**Screen 1 — Welcome**
- Logo + tagline "Secure Consent Management for Professionals"
- "Get Started" button (no skip available)

**Screen 2 — Use Case** (multi-select)
- Options: Intimate Consent, Guest & Event Liability, NDAs & Confidentiality, Service & Freelance, Property & Vehicle, Photo/Video Releases
- Continue disabled until ≥1 selected
- Selected state: filled card with primary color border

**Screen 3 — Industry** (single-select)
- Options: Legal, Healthcare, Real Estate, Photography, Fitness, Events, Consulting, Other
- Continue enabled after selection

**Screen 4 — Volume** (single-select)
- Options: 1-5, 5-20, 20-50, 50+ (with subtitle)

**Screen 5 — Pain Point** (single-select)
- Options: Paper forms are slow, Can't find old agreements, No proof of consent, Clients won't sign digitally

**Screen 6 — Validation (personalized)**
- Dynamic text: "Based on your [volume] agreements/month, cnsnt will save you approximately [N] hours of paperwork per year."
- Calculation: volume_midpoint * 15min_per_paper_form * 12_months / 60 = hours
- Show bar chart animation illustrating time saved

**Screen 7 — Feature Showcase**
- 5 features: Digital Signatures, AES-256 Encryption, 11+ Templates, Audit Trail, PDF Export
- Each: icon + title + one-line description
- Scrollable if needed

**Screen 8 — Security**
- Headline: "Your records, only yours."
- 3 trust points: End-to-end encrypted, Local-first storage, Biometric lock
- Shield icon animation (fade in)

**Screen 9 — Social Proof**
- Headline: "Trusted by 5,000+ professionals"
- 3 testimonials (static, realistic): name, role, 5 stars, 1-line quote
- Testimonials scroll horizontally

**Screen 10 — Notification Permission**
- Headline: "Stay on top of your agreements"
- Body: "Get notified when agreements need renewal or are about to expire."
- "Allow Notifications" → Notification.requestPermissionsAsync()
- "Not Now" → skip silently
- Edge case: permission already denied → show "You can enable later in Settings" instead of request button

**Screen 11 — Plan Ready**
- Headline: "Your [industry] consent vault is ready!"
- Summary box: use case + volume personalization
- "See Your Plan" CTA → go to Screen 12

**Screen 12 — Paywall (hard)**
- Annual plan card (highlighted, "Most Popular"): $29.99/yr = $2.50/mo | "Save 50%"
- Monthly plan card: $4.99/mo
- Trial timeline visual: "7-day free trial" banner (if applicable, otherwise "Start Free")
- "No payment due today" subtext
- Primary CTA: "Start Free Trial" or "Get Pro"
- Secondary: "Maybe Later" → triggers rescue offer Alert
  - Rescue offer: "You get 3 free records to start. Upgrade anytime for full access." → "Continue Free" | "Get Pro"
- On purchase: purchaseService.purchaseMonthly() or .purchaseYearly()
  - Opens Stripe in browser via Linking.openURL
  - On app return (AppState 'active'): Alert "Did you complete your purchase?" → Yes → set entitlement pro

**Edge cases (ALL screens):**
- AsyncStorage save fails: retry 3x with 500ms delays, then continue without persistence
- Back pressed on Screen 12 (paywall): push back to Screen 11 (never let user bypass paywall via back)
- Rapid tapping Continue: debounce at 300ms
- App backgrounded mid-onboarding: save progress, resume on foreground

---

### SCREEN 3: LockScreen (screens/LockScreen.tsx)

**Two modes: PIN Setup and PIN Entry**

**PIN Setup Flow (first time, no PIN set):**
1. "Create your 4-digit PIN" title
2. 4-dot indicator (hollow dots)
3. 12-key numpad (1-9, blank, 0, ⌫)
4. Each digit entered: dot fills, haptic feedback (light)
5. After 4 digits: transition to "Confirm your PIN"
6. Confirm matches: save SHA-256(pin) to SecureStore('cnsnt_pin_hash'), navigate Main
7. Confirm mismatch: shake animation, clear both, "PINs don't match. Try again."

**PIN Entry Flow (returning user):**
1. "Enter your PIN" + cnsnt logo + shield icon
2. If biometricEnabled + hasBiometrics: auto-trigger biometric on mount (500ms delay)
3. Biometric success → onUnlock()
4. Biometric fail / cancel → fall back to PIN
5. "Use [Face ID / Touch ID]" button if biometric available
6. Each digit: dot fills
7. 4th digit entered: auto-submit (no confirm button)
8. Correct PIN → onUnlock()
9. Wrong PIN:
   - Increment failedAttempts in SecureStore
   - Shake animation
   - Show "Incorrect PIN" below dots
   - At 5 attempts: show "Too many attempts. Try again in 30 seconds." + countdown
   - At 10 attempts: show "Vault lock protection activated." + Alert with "Wipe All Data" (two-tap confirmation) and "Contact Support"
10. Delete key: removes last digit, re-hollows dot

**Auto-lock behavior:**
- AppState listener: when app goes to 'background', record timestamp
- When app returns to 'active': if elapsed > autoLockMinutes * 60 * 1000 → show LockScreen
- Timer in App.tsx, not in LockScreen component

**Edge cases:**
- SecureStore read fails: show "Unable to verify PIN. Please contact support." + "Reset App" (wipes everything)
- Biometric enrollment changed (new face added): expo-local-authentication returns error → fall back to PIN, show "Biometric unavailable"
- Device has no biometric enrolled: hide biometric button entirely
- App killed during lockout countdown: countdown resets (acceptable UX tradeoff)

---

### SCREEN 4: HomeScreen — Templates Hub (screens/HomeScreen.tsx)

**Layout:**
- SafeAreaView + SectionList (grouped by category)
- Categories in order: Medical, Legal, Business, Media, Research, Property, Personal, Custom
- Each section: category header + template cards

**Template card:**
- Icon (asset or Ionicons fallback)
- Template name (bold)
- Description (2 lines max, truncated)
- "Premium" badge if isPremium (gold badge top-right)
- Lock overlay if premium and user is free tier

**Free tier behavior:**
- canUseTemplates: free users can only see 3 templates without lock overlays
- Lock overlay: semi-transparent dark overlay + lock icon
- Tapping locked template: navigate to Settings (paywall prompt)

**Free record limit:**
- canCreateRecord: false if recordCount >= FREE_TIER_LIMIT (3)
- Tapping ANY template when at limit: Alert "You've used your 3 free records. Upgrade to Pro for unlimited." [Upgrade] [Not Now]

**Quick-create buttons (top of screen):**
- "Audio Consent" → navigate('Recording')
- "Video Consent" → navigate('VideoConsent') [premium indicator]
- "Custom" → navigate('ConsentBuilder') [premium indicator]

**Edge cases:**
- 0 templates loaded: EmptyState with reload button
- Template data error: show error toast, still show other categories
- Network-dependent template assets: use local fallback icons from Ionicons

---

### SCREEN 5: Dashboard — Records Overview (screens/Dashboard.tsx)

**Layout:**
- Stats row: Total | Active | Expiring Soon | Revoked (4 cards with numbers)
- Filter bar: All | Active | Expired | Revoked | Draft (horizontal scroll)
- Search bar: filters by title, templateName, party names (real-time, debounced 300ms)
- FlatList of records with pull-to-refresh

**Record row:**
- Title (bold)
- StatusBadge (colored pill: active=green, expired=gray, revoked=red, draft=orange)
- Template name + date
- Party names (first 2, "+N more" if more)
- Swipe-left actions: Export PDF | Delete

**Long-press record:** Action sheet with:
- View / PDF Preview
- Export PDF
- Share
- Revoke (if active)
- Delete (with confirmation)

**Stats calculation:**
- expiringSoon: expiresAt within next 7 days AND status === 'active'
- recentlyCreated: createdAt within last 7 days

**Loading states:**
- Initial load: SkeletonList (3 skeleton cards)
- Refresh: RefreshControl spinner

**Empty states:**
- No records: EmptyState "No records yet. Tap Home to create your first agreement." + CTA
- No filter results: "No [filter] records."
- No search results: "No records matching '[query]'."

**Edge cases:**
- Database read fails: ErrorState with "Retry" button
- Decryption fails for one record: skip it, show "1 record could not be decrypted" banner
- Decryption fails for ALL records: "Vault unavailable. Your encryption key may be lost." + "Export Encrypted Backup" button
- 100+ records: ensure FlatList virtualization, no jank (test with 200 records)
- Concurrent navigation (navigate to record while deleting): no crash (key-based deduplication)

---

### SCREEN 6: TemplateForm (screens/TemplateForm.tsx)

**Input:** templateId (from route.params)

**Layout:**
- ScrollView with form fields
- Party section at top: Add Party button, list of added parties
- Fields section: rendered from template.fields
- Consent text section: read-only, formatted
- Signature section: one pad per party
- Action buttons: "Save as Draft" | "Complete & Sign"

**Field rendering by type:**
- text: TextInput, single line
- multiline: TextInput multiline, 4 rows
- email: TextInput, keyboardType='email-address', validate on blur
- date: DateTimePicker (native), shows formatted date string
- number: TextInput, keyboardType='numeric'

**Required field validation:**
- Red border + error text below on submit if empty
- Email validation: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- Phone validation (if applicable): 10+ digits

**Party management:**
- "Add Party" button → modal: name (required), role (required), email (optional)
- Minimum 1 party
- Maximum: 5 (pro) or 2 (free)
- Role options: Consenting Party, Witness, Legal Representative, Employer, Contractor, Client, Other

**Signature pad:**
- One per party (requiresDualSignature determines if ≥2 required)
- Draw with finger
- "Clear" button
- Minimum stroke validation: must have ≥ 20 touch points before saving (prevent empty/accidental signatures)
- "Type Signature" alternative: TextInput → rendered as cursive-style text → saved as base64 PNG

**On "Complete & Sign":**
1. Validate all required fields
2. Validate all required signatures present
3. If entitlement === 'free' AND recordCount >= FREE_TIER_LIMIT: show upgrade prompt
4. Generate record ID: `cr_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 8)}`
5. Build ConsentRecord object
6. Compute HMAC via vault.computeDocumentHmac(record)
7. Encrypt and store via db.save(record)
8. Increment record count in AsyncStorage
9. Log to audit log
10. Navigate to PDFPreview (with recordId)

**On "Save as Draft":**
- No signature requirement
- status = 'draft'
- Save encrypted to database
- Navigate back to Dashboard

**Edge cases:**
- Vault locks mid-form: save current state as draft automatically, navigate to Lock, resume on unlock
- Record save fails: retry 3x → show "Save failed. Your form data is preserved. Try again." (do NOT lose the form data)
- App killed mid-form: form data is lost (document intent in UX: "Your data is saved when you tap Save As Draft")
- Template not found: show "Template not available" + navigate back

---

### SCREEN 7: ConsentBuilderScreen (screens/ConsentBuilderScreen.tsx)

**Purpose:** Create custom templates (pro only)

**PaywallGate:** wrap entire screen, check canUseTemplates

**Fields:**
- Template name (required, max 100 chars)
- Description (optional, max 200 chars)
- Fields editor: add/remove/reorder fields
  - Each field: label, type (text/date/multiline/email/number), required toggle
  - Max 20 fields
- Consent text: large multiline textarea (required)
- Dual signature toggle
- Default expiry: "Never" | 30 | 60 | 90 | 180 | 365 days

**On save:**
- Validate name + consent text + at least 1 field
- Save to local templates list (AsyncStorage key 'cnsnt_custom_templates')
- Navigate back, refresh HomeScreen templates list

**Edge cases:**
- 0 fields: "Add at least one field to continue"
- Name conflict with existing template: allow (templates use unique ID, not name)
- Max custom templates: 20 (prevent unbounded storage)

---

### SCREEN 8: RecordingScreen (screens/RecordingScreen.tsx)

**Purpose:** Audio consent recording linked to a consent record

**PaywallGate:** wrap, check canRecord

**Permission flow:**
- On mount: Audio.requestPermissionsAsync()
- Denied: show "Microphone access required" + "Open Settings" button
- Granted: show recording UI

**Recording UI:**
- Large pulsing record button (red circle, pulse animation during recording)
- Duration counter: MM:SS
- Waveform visualization: 30 animated vertical bars, heights driven by recording metering data
- Pause / Resume toggle
- Stop button

**Post-recording UI:**
- Waveform static (last state)
- Playback: play/pause, scrubber (Slider), speed: 1x / 1.5x / 2x
- "Retake" button (clears recording, back to recording UI)
- "Save" button

**On save:**
- Read file bytes from expo-av temp URI
- Encrypt bytes via vault.encryptAndStore
- Store encrypted URI reference in consent record
- Log to audit log
- Navigate back (or to next step in form flow)

**On share:**
- expo-sharing → share the unencrypted .m4a file (user explicitly exports)

**Timer cleanup on unmount:**
- Stop recording
- Unload sound
- Clear all intervals
- Cancel animations

**Edge cases:**
- Recording interrupted by phone call: Audio.setAudioModeAsync with `staysActiveInBackground: true` keeps recording going; show "Recording paused by interruption" if audio session is interrupted
- Storage full (< 10MB free): check before recording, show "Not enough storage to record"
- Max duration: 2 hours — warn at 1:45 remaining, auto-stop at 2:00:00
- App backgrounded: recording continues (background audio mode)
- App killed: recording lost, file may be partially saved (acceptable, document this)
- Playback position out of sync: reset position to 0 on error

---

### SCREEN 9: VideoConsentScreen (screens/VideoConsentScreen.tsx)

**Purpose:** Video consent with timestamp overlay and GPS stamp (premium)

**PaywallGate:** wrap, check canRecord

**Permissions:**
- useCameraPermissions() + useMicrophonePermissions()
- If either denied: explain both needed + "Open Settings" button

**Pre-recording:**
- Camera preview (front camera default, toggle to rear)
- GPS capture on tap-to-start: expo-location.getCurrentPositionAsync()
  - Timeout 5s; if GPS unavailable, proceed without GPS (mark as "GPS not captured")
- Party name overlays (from route.params: partyA, partyB) rendered at top of preview

**During recording:**
- Timestamp overlay: live clock (HH:MM:SS AM/PM + date) in corner
- Duration counter in opposite corner
- Red blinking REC indicator
- Countdown at 60 seconds remaining: "1:00 remaining" bar appears
- Auto-stop at MAX_DURATION_SECONDS (300)

**Post-recording:**
- Video player: expo-av Video component with controls
- Scrub, play/pause
- "Retake" / "Save" buttons

**On save:**
- expo-av saves to temp file (mp4)
- Read file → encrypt bytes → store encrypted
- Attach GPS coordinates + timestamp to record metadata
- Delete original temp file
- Navigate back

**Edge cases:**
- Camera unavailable (tablet with no front camera): show rear only, no toggle
- Camera access blocked by Screen Time: show "Camera blocked by restrictions"
- Low battery (<10%): Alert "Battery is low. Video may be interrupted. Continue?" [Continue] [Cancel]
- Storage check: verify ≥ 100MB free before starting (video files are large)
- GPS permission denied: skip GPS, mark metadata.gps = 'denied'
- App backgrounded during video: video recording stops (iOS constraint) — show warning before user leaves screen: "Backgrounding will stop recording"

---

### SCREEN 10: NdaScreen (screens/NdaScreen.tsx)

**Purpose:** Guided NDA creation flow (premium)

**Fields:**
- Disclosing Party: name (required), company (optional), jurisdiction (required)
- Receiving Party: name (required), company (optional)
- Effective date (date picker, defaults to today)
- Duration: dropdown (1 year, 2 years, 3 years, 5 years, Indefinite)
- Confidential Information description: multiline (required)
- Exclusions: multiline (optional)
- Optional: Witness name + signature

**Auto-generated consent text:**
- Template-filled NDA text based on inputs
- Jurisdiction-specific boilerplate (US-general, UK, CA, AU available)
- Edit mode toggle: show/hide raw text for advanced users

**Dual signatures required:**
- Party A signature pad
- Party B signature pad
- Optional witness signature

**On save:** same as TemplateForm save flow

**Edge cases:**
- Back-dated effective date: Alert "Effective date is in the past. Are you sure?" [Continue] [Change Date]
- Same party A and party B name: allowed (one person representing two entities)
- Jurisdiction not supported: fall back to "General US" boilerplate

---

### SCREEN 11: WaiverScreen (screens/WaiverScreen.tsx)

**Purpose:** Liability waiver for activities/events

**Fields:**
- Activity / Event name (required)
- Date of activity (date picker)
- Location (optional)
- Known risks: auto-populated from activity type, editable
- Activity type: dropdown (Sports, Fitness, Adventure, Medical, Travel, Other)
- Emergency contact: name + phone
- "Assumption of Risk" checkbox: required to tick before signing
- "Hold Harmless" checkbox: required to tick

**Single signature (participant)**

**Edge cases:**
- Emergency contact phone: must be 10+ digits if entered (not required but validated if present)
- Activity date in past: warn, allow

---

### SCREEN 12: MutualReleaseScreen (screens/MutualReleaseScreen.tsx)

**Purpose:** Both parties release each other from claims

**Fields:**
- Dispute / Matter description (required, multiline)
- Release effective date
- Consideration: amount (optional, numeric), description (optional)
- Both parties: name + role
- Recitals: optional context section
- "Mutual Release of Claims" checkbox (required)

**Dual signatures required**

**Edge cases:**
- Consideration amount: validate decimal format (no letters)

---

### SCREEN 13: PDFPreviewScreen (screens/PDFPreviewScreen.tsx)

**Purpose:** View, share, print generated PDF

**Input:** recordId from route.params

**On mount:**
1. Load record from database (decrypt)
2. Generate PDF via exportService.generatePdf(record)
3. Display in WebView (expo-print generates HTML → PDF → WebView loads)

**UI:**
- WebView filling screen
- Bottom toolbar: Share | Download | Print
- Share: expo-sharing
- Download: expo-file-system.copyAsync to DocumentDirectory
- Print: expo-print.printAsync

**Free tier:** PDF preview locked for free users
- Show preview blurred
- Overlay: "PDF Export is a Pro feature" + Upgrade button

**Edge cases:**
- PDF generation fails: "Unable to generate PDF. Please try again." + Retry button
- WebView render error: fall back to HTML text view
- Share fails (permissions): "Unable to share. Check Files app permissions."
- Large PDF (many signatures): may take 2-3 seconds — show ActivityIndicator during generation

---

### SCREEN 14: Settings (screens/Settings.tsx)

**Sections:**

**Subscription (top):**
- Free: "3 / 3 records used" progress bar + "Upgrade to Pro" card
- Pro: "Pro Member" badge, expiry (if known), "Manage Subscription" → Stripe customer portal

**Security:**
- Biometric toggle (only shown if hasBiometrics === true)
  - Toggle off: verify PIN first ("Enter PIN to disable biometric")
- "Change PIN" button → navigate to Lock in setup mode
- "Auto-Lock" → picker: 1, 2, 5, 10, 15, 30 min, or "Never"
- "Lock Now" button → immediately lock app

**Data:**
- "X total records" count
- "Export All Records (JSON)" → encrypted JSON export
- "Backup Settings" → navigate BackupSettings
- "View Audit Log" → show audit entries list

**Support:**
- "Rate cnsnt" → expo-store-review
- "Privacy Policy" → Linking.openURL(PRIVACY_URL)
- "Terms of Service" → Linking.openURL(TOS_URL)
- "Contact Support" → Linking.openURL('mailto:support@printmaxx.com')
- App version: shown at bottom

**Danger Zone:**
- "Delete All Data": Alert "This will permanently delete all records and cannot be undone."
  - First confirmation: Alert with [Delete Everything] [Cancel]
  - Second confirmation: TextInput "Type DELETE to confirm"
  - On confirmed: wipe all AsyncStorage keys + SecureStore + file system records → navigate to Splash

**Edge cases:**
- Auto-lock "Never" option: store -1, skip lock timer
- Biometric toggle ON while feature unavailable: show "Face ID not set up on this device. Configure in iOS Settings."
- Delete All Data during cloud sync: cancel sync, then wipe

---

### SCREEN 15: BackupSettingsScreen (screens/BackupSettingsScreen.tsx)

**Cloud providers:**
- iCloud Drive (iOS only) — no OAuth, uses expo-file-system to iCloud container
- Google Drive — OAuth via expo-auth-session
- Dropbox — OAuth via expo-auth-session

**Per provider status:**
- "Connected" (green) / "Not Connected" (gray)
- Last backup: "Never" | relative timestamp + health indicator (good/warning/critical)
- Connect / Disconnect button

**Controls:**
- Auto-backup toggle (backs up on every record save if enabled)
- "Back Up Now" button → shows progress bar → "Backup complete ✓" or error
- "Restore from Backup" → file picker (per provider) → shows backup list → select → decrypt → import confirmation Alert

**Export .cnsnt:**
- "Export Backup File" → generates encrypted JSON → share via expo-sharing
- Format: `{ version: 1, createdAt: ISO, records: [encrypted_records], integrity: HMAC }`

**Import .cnsnt:**
- "Import Backup" → file picker (DocumentPicker)
- Decrypt with current vault key
- Conflict resolution: "X records already exist. Skip duplicates / Overwrite / Merge"
- Merge = keep both (different IDs)

**Encryption notice:** "All backups use your vault encryption key. You cannot restore on a new device without re-entering your PIN."

**Edge cases:**
- Google Drive OAuth fails: retry once → show "Sign in to Google Drive" button
- iCloud unavailable (iCloud disabled): show "iCloud Drive is disabled. Enable in iOS Settings > [Your Name] > iCloud."
- Backup file corrupted: "This backup file is damaged and cannot be restored."
- Restore on different device (different vault key): "Decryption failed. This backup was created on a different device or with a different PIN."
- Large backup (100+ records): progress bar (0-100%), abort button

---

## 10. COMPONENTS

| Component | File | Purpose |
|-----------|------|---------|
| ErrorBoundary | components/ErrorBoundary.tsx | Catch React render errors, show fallback |
| EmptyState | components/EmptyState.tsx | Friendly empty list/grid state |
| StatusBadge | components/StatusBadge.tsx | Colored status pill |
| SkeletonLoader | components/SkeletonLoader.tsx | Loading placeholder cards |
| PaywallGate | components/PaywallGate.tsx | Wraps premium screens, shows upgrade prompt |
| DualSignature | components/DualSignature.tsx | Two signature pads side by side |
| VideoPlayer | components/VideoPlayer.tsx | expo-av Video wrapper with controls |

**Missing components that need to be added:**
- SoundTouchable — replaces TouchableOpacity everywhere, adds tap sound + haptic
- SignaturePad — reusable canvas signature component with min-stroke validation

---

## 11. SOUND DESIGN (missing — must be added)

Per app-factory-pipeline Rule 14: every app MUST have sound effects.

**Required sounds:**
- `tap.wav` — all button taps (replace TouchableOpacity with SoundTouchable)
- `success.wav` — record saved, backup complete
- `error.wav` — validation error, wrong PIN
- `lock.wav` — app locked
- `unlock.wav` — app unlocked
- `signature.wav` — signature drawn (soft scratch)
- `pdf.wav` — PDF generated

**Source:** Octave (CC0 iOS sounds) for taps/slides. Kenney (CC0) for UI interactions.

**Implementation:**
1. Create `assets/sounds/` directory with 7 sound files
2. Create `src/sounds/SoundEngine.ts` — preloads all sounds, `playSound(name)` method
3. Create `src/components/SoundTouchable.tsx` — wraps Pressable, calls playSound('tap') + Haptics.impactAsync on press
4. Replace all `Pressable` imports with `SoundTouchable as Pressable` in every screen
5. Add contextual sounds: unlock.wav on LockScreen success, signature.wav in signature pad, pdf.wav in PDFPreview

---

## 12. FREE VS PRO GATING (enforcement matrix)

Every gate MUST be enforced IN CODE, not just visually labeled.

| Feature | Free | Pro | Enforcement Location |
|---------|------|-----|---------------------|
| Total records | 3 | Unlimited | TemplateForm: check before save |
| Templates | 3 basic | 11+ all | HomeScreen: lock overlay + check before navigate |
| Audio recording | No | Yes | RecordingScreen: PaywallGate on mount |
| Video recording | No | Yes | VideoConsentScreen: PaywallGate on mount |
| PDF export | No | Yes | PDFPreviewScreen: blur + overlay |
| Custom templates | No | Yes | ConsentBuilderScreen: PaywallGate on mount |
| Cloud backup | No | Yes | BackupSettings: disable controls |
| Audit log export | No | Yes | Settings: disable button |
| Add parties (max) | 2 | 5 | TemplateForm: hide "Add Party" at limit |

**Code verification (grep these patterns):**
```
grep -rn "canCreateRecord" screens/  # should appear in TemplateForm
grep -rn "canRecord" screens/        # should appear in Recording + Video
grep -rn "PaywallGate" screens/      # should wrap Recording, VideoConsent, ConsentBuilder
grep -rn "canUseTemplates" screens/  # should appear in HomeScreen
grep -rn "isPremium\|isPro" screens/ # should appear in PDFPreview, BackupSettings
```

---

## 13. PURCHASE FLOW (complete)

### Initiate Purchase
1. User taps "Upgrade" anywhere
2. Navigate to Settings (if not already there)
3. Show plan selector: Annual ($29.99/yr, highlighted) + Monthly ($4.99/mo)
4. User selects plan → purchaseService.purchaseMonthly() or purchaseYearly()
5. Linking.openURL(STRIPE_LINK) opens Safari
6. User completes Stripe checkout

### Return to App
7. AppState changes to 'active' (returns from browser)
8. After 2-second delay (UX buffer): Alert "Did you complete your purchase?"
   - "Yes, I paid" → AsyncStorage.setItem('cnsnt_entitlement', 'pro')
   - "Not yet" → dismiss, no change
9. All screens that call usePurchases() re-read entitlement on next mount

### Restore Purchases
- Stripe Payment Links have no SDK-based restore
- Settings shows: "To restore your purchase, contact support@printmaxx.com with your Stripe receipt"
- Manual restore: support confirms via email → user taps "I have a receipt" → honor system set

### CRITICAL GAPS TO ADDRESS BEFORE LAUNCH
1. No Stripe webhook verification — entitlement is honor-system. Fraud risk is low (delete app = lose entitlement), but should add webhook endpoint eventually.
2. Entitlement lost on uninstall (AsyncStorage wiped). Document in App Store review notes and FAQ.
3. Consider: hash email to create pseudo-account so entitlement survives reinstall.

---

## 14. QA CHECKLIST (run before every build submission)

### First Launch Flow
- [ ] Fresh install → shows Splash → OnboardingFlow
- [ ] All 12 onboarding screens render without crash
- [ ] Back navigation works on screens 2-11 (not 1, not 12)
- [ ] Skip button appears on screens 3-10, hidden on 1, 11, 12
- [ ] Progress bar animates 1→12
- [ ] Answers save to AsyncStorage between steps
- [ ] Paywall: both plan options selectable
- [ ] "Maybe Later" shows rescue offer Alert
- [ ] Completing onboarding: AsyncStorage 'cnsnt_onboarding_complete' = 'true'

### Authentication
- [ ] PIN setup: 4 digits, confirm must match, mismatch shakes and resets
- [ ] PIN entry: correct PIN navigates to Main
- [ ] Wrong PIN: shake + "Incorrect PIN" message
- [ ] 5 wrong PINs: 30-second lockout with countdown
- [ ] Biometric auto-prompts on LockScreen load (if enabled)
- [ ] Biometric cancel/fail: falls back to PIN pad
- [ ] Auto-lock: background app for configured minutes → LockScreen on return
- [ ] "Lock Now" in Settings immediately shows LockScreen

### Record Creation
- [ ] All field types render: text, date, multiline, email, number
- [ ] Required field validation: empty required field blocks submit
- [ ] Email validation: invalid format blocks submit
- [ ] Add party modal works: name, role, email
- [ ] Remove party works
- [ ] Signature pad: draw, clear, redraw
- [ ] "Save as Draft": saves with status 'draft', no signature required
- [ ] "Complete & Sign": requires all required fields + at least 1 signature
- [ ] Saved record appears in Dashboard
- [ ] Record count increments in AsyncStorage

### Free Tier Enforcement
- [ ] Create 3 records: allowed
- [ ] Attempt 4th record: blocked with upgrade prompt
- [ ] Premium template tap on free: shows lock overlay + upgrade prompt
- [ ] Recording tap on free: PaywallGate shows upgrade screen
- [ ] Video consent tap on free: PaywallGate shows upgrade screen
- [ ] PDF generation on free: blurred preview with upgrade overlay

### Pro Features (test after setting entitlement = 'pro' in AsyncStorage)
- [ ] 4th, 5th+ records: allowed
- [ ] All 11 templates accessible
- [ ] Audio recording: records, plays back, saves
- [ ] Video recording: starts with timestamp overlay, GPS captured
- [ ] PDF generates with all data
- [ ] PDF shareable
- [ ] Cloud backup settings accessible

### Dashboard
- [ ] Records list loads (decrypted)
- [ ] Filter buttons change list
- [ ] Search filters by title / template name / party name
- [ ] Pull-to-refresh reloads
- [ ] Swipe-left reveals Export + Delete actions
- [ ] Delete: confirms, removes from list
- [ ] Stats cards show correct counts
- [ ] Empty state shows when 0 records

### Settings
- [ ] Biometric toggle saves and persists
- [ ] Auto-lock picker: change works, persists after restart
- [ ] "Delete All Data": double confirmation required, wipes everything

### Security Tests
- [ ] Vault key stored in SecureStore (check: AsyncStorage keys are encrypted ciphertext)
- [ ] HMAC verification: use test to corrupt 1 byte in AsyncStorage → app shows "integrity failed"
- [ ] Vault auto-locks after 2 min inactivity (test: pause app operations for 2 min)

### Build Checks
- [ ] `npx tsc --noEmit` — 0 errors
- [ ] `npx expo export --platform ios` — clean
- [ ] No console.log in production builds
- [ ] All sound files load without error (SoundEngine.preloadAll() in App.tsx)

---

## 15. APP STORE SUBMISSION CHECKLIST

- [ ] Bundle ID: com.printmaxx.cnsnt (unique)
- [ ] Version: 1.0.0, Build: 1
- [ ] Privacy Policy URL: https://printmaxx-privacy.surge.sh (resolves 200)
- [ ] Terms URL: https://printmaxx-tos.surge.sh (resolves 200)
- [ ] NSCameraUsageDescription: "cnsnt needs camera access to capture photos as part of consent record documentation."
- [ ] NSMicrophoneUsageDescription: "cnsnt needs microphone access to record audio consent sessions."
- [ ] NSFaceIDUsageDescription: "cnsnt uses Face ID to protect your sensitive consent records from unauthorized access."
- [ ] ITSAppUsesNonExemptEncryption: false (AES from expo-crypto, classified as exempt under EAR 740.17(b)(3))
- [ ] usesNonExemptEncryption: false in ios config
- [ ] Age rating: 17+ (adult-use consent forms)
- [ ] Category: Productivity (primary), Utilities (secondary)
- [ ] Screenshots: 6.7" (iPhone Pro Max) and 6.1" (iPhone standard), all 5 required screenshots
- [ ] App preview video: optional but recommended (30-sec demo of consent creation flow)
- [ ] Minimum useful free functionality: yes (3 complete consent records)
- [ ] Payment handled via external Stripe checkout: document in App Store Review Notes
- [ ] No simulated sensor data
- [ ] App Store review notes template:
  ```
  cnsnt is a consent record management and liability protection app with AES-256 encryption,
  biometric lock, and SHA-256 integrity verification. Users create, sign, and export consent
  documents and agreements as verified PDFs. Includes 11 professional templates covering
  consent agreements, NDAs, waivers, service contracts, and more.

  Payment is handled via Stripe Payment Links (external web checkout). This is intentional —
  we use Stripe and not in-app purchases. The app does not collect payment card information.

  To test the free tier: launch app, complete onboarding, dismiss paywall. 3 records available.
  To test pro features: contact us for a promo code or use test account: [EMAIL]
  ```

---

## 16. KNOWN PRODUCTION GAPS (address before App Store submission)

### P0 (blocking)
1. **Sound design missing.** No SoundEngine, no SoundTouchable. Violates Rule 14 (app-factory-pipeline). Every screen needs sound.
2. **App icon not production-ready.** Current icon in assets/app_icon.png — verify it's not a Pillow-generated geometric shape. Generate via Google ImageFX (Imagen 4) if needed.
3. **Video encryption incomplete.** VideoConsentScreen calls vault.encryptAndStore() but must: read temp file bytes → encrypt → delete temp file → store encrypted bytes. Verify this is actually happening.

### P1 (should fix before launch)
4. **Vault key recovery.** If user forgets PIN + reinstalls, all data is gone. Add "Export encryption key" to Settings (secure backup). Document loss in FAQ.
5. **Record count drift.** Count cached in AsyncStorage separately from index. Derive count from index.length on each load instead of cached counter.
6. **Biometric re-enrollment.** If user adds new Face to Face ID, old biometric session invalidated. Handle gracefully (catch LocalAuthenticationError, re-prompt, fall back to PIN with "Biometric security updated" message).
7. **Stripe entitlement persistence.** Entitlement lost on reinstall. Document in FAQ + support flow.

### P2 (nice to have before v1.1)
8. **Webhook validation.** Add Stripe webhook to verify payment server-side.
9. **Multi-device sync.** Two devices → backup conflict. Need merge-by-ID strategy.
10. **Record search speed.** Decrypting 100+ records on search is slow. Cache decrypted records in memory (clear on lock).

---

## 17. BUILD COMMANDS

```bash
# Development
npx expo run:ios

# Production build (EAS)
eas build --platform ios --profile production

# Submit
eas submit --platform ios

# TypeScript check
npx tsc --noEmit

# Clean build
npx expo prebuild --clean --platform ios && npx expo run:ios
```

---

## 18. STRIPE PRODUCTS

| Plan | Price | Stripe Link |
|------|-------|------------|
| Pro Monthly | $4.99/mo | https://buy.stripe.com/5kQ14o6LK7NH51nend3F60E |
| Pro Annual | $29.99/yr | https://buy.stripe.com/5kQcN60nm8RL9hDgvl3F60D |

Product IDs in Stripe dashboard: cnsnt_pro_monthly, cnsnt_pro_annual

---

*This spec is authoritative. All code changes to cnsnt must maintain consistency with this document. Update this spec when architecture changes.*
