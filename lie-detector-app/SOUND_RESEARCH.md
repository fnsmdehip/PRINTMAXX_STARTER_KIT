# Sound Design Research for Mobile Apps

Researched: 2026-04-01

---

## TIER 1: Download Right Now, Zero Licensing Risk

These are the safest options. CC0, CC-BY, or explicit commercial-use licenses. No attribution headaches.

### 1. Google Material Design Sound Resources

- **URL:** https://m2.material.io/design/sound/sound-resources.html
- **Mirror:** https://archive.org/details/material-design-sound-resources
- **License:** CC-BY 4.0 (free commercial use, attribution required)
- **What you get:** Alert tones, notification sounds, hero sounds, primary system sounds, secondary system sounds. Professionally designed by Google's sound team.
- **Format:** WAV
- **Why use it:** These are the actual sounds designed for Material Design. Professional quality, designed for mobile. The benchmark for what UI sounds should feel like.
- **How to get:** Download the ZIP from the Internet Archive mirror or the material.io page.

### 2. Kenney UI Audio + Interface Sounds

- **URL (UI Audio):** https://kenney.nl/assets/ui-audio
- **URL (Interface Sounds):** https://kenney.nl/assets/interface-sounds
- **URL (Digital Audio):** https://kenney.nl/assets/digital-audio
- **GitHub:** https://github.com/Calinou/kenney-ui-audio
- **License:** CC0 1.0 Universal (public domain, do literally anything)
- **What you get:** 50+ UI sound effects: button clicks, switches, generic clicks, notifications
- **Format:** WAV (converted from OGG)
- **Why use it:** CC0 means zero risk. No attribution, no restrictions. Kenney is legendary in the game dev community for quality free assets. Three separate packs cover different use cases.

### 3. Octave (Handmade iOS UI Sounds)

- **URL:** http://raisedbeaches.com/octave/
- **GitHub:** https://github.com/scopegate/octave
- **License:** Free for any use, no attribution required (attribution welcome but not mandatory)
- **What you get:** 48 hand-crafted sounds: taps, beeps, slides. Made specifically for iOS user interfaces.
- **Format:** 16-bit, 44.1kHz AIF files
- **Why use it:** Made BY an iOS developer FOR iOS apps. Curated from 10,000+ samples by a pro sound designer in Tasmania. Includes a UIButton category for easy integration.

### 4. Pixabay Sound Effects

- **URL:** https://pixabay.com/sound-effects/search/ui/
- **License:** Pixabay License (free commercial use, no attribution required)
- **What you get:** 120,000+ total sound effects. Search "UI", "notification", "click", "success", "error" for relevant ones.
- **Format:** MP3 download
- **Why use it:** Massive library, royalty-free, no sign-up needed. Good for finding specific sounds like success chimes, error buzzes, transition whooshes.

### 5. Mixkit

- **URL:** https://mixkit.co/free-sound-effects/
- **License:** Mixkit Free License (commercial and personal use, no attribution)
- **What you get:** 3,000+ sound effects. Interface/notification category has what we need.
- **Format:** WAV/MP3
- **Why use it:** High quality, no sign-up, no attribution. By Envato (the company behind ThemeForest). Browse interface and notification categories specifically.

### 6. Freesound.org (CC0 Filtered)

- **URL:** https://freesound.org/browse/tags/cc0/
- **Notification Pack:** https://freesound.org/people/JFRecords/packs/23782/
- **License:** Filter by CC0 for zero-risk sounds. Also has CC-BY options.
- **What you get:** Community-uploaded sounds. Quality varies but CC0 filter gives you safe picks. The JFRecords notification pack was specifically designed for app development.
- **Format:** WAV, FLAC, MP3 (varies by upload)
- **Why use it:** Filter by CC0 license and you get truly public domain sounds. The notification pack by JFRecords is purpose-built for mobile apps.

### 7. Sonniss GameAudioGDC Bundles

- **URL:** https://sonniss.com/gameaudiogdc/
- **2026 Bundle:** https://gdc.sonniss.com/
- **License:** Royalty-free, commercial use, no attribution, unlimited projects, lifetime use
- **What you get:** 30-50GB+ per annual bundle. Professional sound libraries donated by studios. Every year since ~2015. Combined archive is ~160GB.
- **Format:** WAV (professional quality, 24-bit/96kHz in many cases)
- **Why use it:** Professional studio quality. The annual GDC bundles are genuinely incredible. UI sounds are buried in there among ambient/foley/music, but they exist.
- **Restriction:** Cannot use for AI training. Cannot resell raw sounds.

---

## TIER 2: Free With Minor Conditions

### 8. SND (snd.dev)

- **URL:** https://snd.dev/
- **GitHub:** https://github.com/snd-lib/snd-lib
- **License:** Free for commercial and non-commercial use. Copyright retained by sound designers. MIT license on code.
- **What you get:** Curated UI sounds designed to fit modern UI components. JavaScript library included.
- **Format:** Built into a JS library (Web Audio API)
- **Why use it:** Purpose-built for UI/UX. Sounds designed to match common UI patterns. Includes a ready-to-use JS library. Japanese-designed, minimal aesthetic.

### 9. soundcn (700+ UI Sounds, shadcn-style)

- **URL:** https://github.com/kapishdima/soundcn
- **License:** CC0 licensed sounds, MIT licensed code
- **What you get:** 700+ curated UI sound effects: clicks, notifications, transitions, game sounds. Each sound is a self-contained TypeScript module with inline base64 data URI.
- **Format:** Base64-encoded audio in TypeScript modules (no external files)
- **Install:** `npx shadcn@latest add @soundcn/use-sound @soundcn/open-001`
- **Why use it:** Zero external audio files. No fetch requests at runtime. No hosting needed. Includes a useSound React hook via Web Audio API. The shadcn model applied to sound.
- **Note:** Designed for web/React. For React Native, you would extract the base64 audio data and play via expo-audio.

### 10. JDSherbert Ultimate UI SFX Pack

- **URL:** https://jdsherbert.itch.io/ultimate-ui-sfx-pack
- **License:** Royalty-free commercial use. Attribution required (mention in credits).
- **What you get:** 67 high-quality UI sound effects
- **Format:** WAV
- **Why use it:** Well-organized, clearly labeled. Good variety of UI interaction sounds.
- **Condition:** Must credit JDSherbert somewhere (credits screen, about page, etc.)

---

## TIER 3: Reference Only (Not Free or Not Downloadable for Commercial Use)

### 11. Facebook/Meta Sound Kit

- **URL:** https://design.facebook.com/toolsandresources/sound-kit-for-prototypes/
- **GitHub mirror:** https://github.com/omrobbie/Facebook-Sound-Kit
- **License:** Prototyping only. NOT licensed for commercial use without Meta's written permission.
- **What you get:** Two sound sets (full volume for desktop, low volume for mobile). Curated interaction sounds.
- **VERDICT:** Good for reference/inspiration. Do NOT ship in a production app unless you get explicit permission from Meta.

### 12. Dev_Tones by RCP Tones

- **URL:** https://rcptones.com/dev_tones/
- **Gumroad:** https://rcptones.gumroad.com/l/dev_tones
- **License:** Paid product. 630 royalty-free tones. No attribution required AFTER purchase.
- **What you get:** 630 professionally mastered mobile UI tones. Preview sounds available (cannot use previews in production).
- **VERDICT:** Worth buying if you want a massive professional library. Not free.

### 13. Microsoft Fluent Design Sounds

- **No official public sound library found.** Fluent Design System covers light, depth, motion, material, and scale but does not publish a downloadable sound asset pack as of this research date.
- **VERDICT:** Skip. No assets to download.

---

## BEST PRACTICES: How Top Apps Handle Sound

### What the Best Apps Do

**Duolingo:**
- Satisfying chimes for correct answers, playful boings for mistakes
- Character-specific voice feedback
- Clear visual signals alongside every sound (accessibility)
- Sound reinforces the gamification loop: correct = dopamine hit

**Headspace:**
- Soothing background music, gentle audio cues
- Careful vocal design (tone, excitement level, pause timing)
- Sound creates atmosphere rather than providing feedback

**Calm:**
- Nature sounds (birds, ocean, rain) as ambient background
- Minimal UI sounds; the content IS the audio experience

**Cal AI:**
- Subtle haptic + sound on successful scan
- Micro-interaction sounds during onboarding flow
- Sound used sparingly to mark milestones, not every tap

### Sound Design Principles for Mobile Apps

1. **Less is more.** Only add sound where it provides genuine feedback. Not every button needs a click sound.
2. **Respect system volume.** Your app sounds should be quieter than system sounds. Users should never be startled.
3. **Always pair with haptics.** On iOS, Core Haptics + sound together creates a more satisfying interaction than either alone.
4. **Provide a mute option.** Always. Some users hate app sounds. Respect that.
5. **Three categories of UI sounds:**
   - **Confirmation:** Success, completion, achievement (positive, bright, short)
   - **Alert:** Error, warning, attention needed (distinct, not harsh)
   - **Navigation:** Tap, swipe, transition (subtle, almost subliminal)
6. **Keep sounds under 1 second** for UI interactions. 0.1-0.3s is ideal for taps.
7. **Consistent sonic palette.** All sounds in your app should feel like they belong together. Pick one source/style and stick with it.

### Apple HIG Sound + Haptics Guidelines

- Use Core Haptics API for custom haptic patterns synchronized with audio
- Use UIFeedbackGenerator for standard UIKit control feedback (selection, impact, notification)
- Combine sound + haptics + visual animation for the best user experience
- Haptic types: Selection (light tap), Impact (medium thud), Notification (success/warning/error)
- Design for context: sounds should auto-adjust when device is silenced or other audio is playing

---

## TECHNICAL SPECS: iOS Audio Requirements

### Recommended Format for UI Sound Effects

| Property | Recommended | Also Acceptable |
|----------|-------------|-----------------|
| Format | CAF (Core Audio Format) | WAV, M4A, AAC |
| Bit depth | 16-bit | 24-bit (overkill for UI) |
| Sample rate | 44.1 kHz | 22.05 kHz (lighter) |
| Channels | Mono | Stereo (unnecessary for UI) |
| Encoding | Linear PCM (little-endian) | AAC-LC (compressed) |

### Why CAF for iOS

- Native Apple format, lowest latency
- Supports all iOS audio codecs
- Best for short UI sound effects
- WAV works fine too; CAF is technically optimal

### Implementation in React Native / Expo

**Primary library:** `expo-audio` (Expo's built-in)
```typescript
import { useAudioPlayer } from 'expo-audio';

const player = useAudioPlayer(require('./assets/sounds/tap.wav'));
player.play();
```

**Alternative:** `react-native-sound`
```typescript
import Sound from 'react-native-sound';

const tap = new Sound('tap.wav', Sound.MAIN_BUNDLE, (error) => {
  if (!error) tap.play();
});
```

**For advanced audio graphs:** `react-native-audio-api` (Web Audio API equivalent)

### Volume Levels

- UI sounds should be at -12dB to -18dB relative to full scale (0 dBFS)
- This means your WAV files should NOT be normalized to 0dB
- Target peak level: -12dB for alerts, -18dB for navigation taps
- This ensures sounds are noticeable but not jarring relative to system volume

---

## RECOMMENDED DOWNLOAD PLAN

### Phase 1: Immediate (today)

1. **Download Kenney packs** (CC0, safest possible):
   - https://kenney.nl/assets/ui-audio
   - https://kenney.nl/assets/interface-sounds
   - https://kenney.nl/assets/digital-audio

2. **Download Octave** (iOS-specific, free):
   - https://github.com/scopegate/octave

3. **Download Google Material Sound** (CC-BY, professional):
   - https://archive.org/details/material-design-sound-resources

### Phase 2: Cherry-pick specifics

4. Browse Pixabay for specific missing sounds (success chime, error, notification)
5. Browse Mixkit interface category for anything the packs miss
6. Check Freesound.org CC0 filter for unique sounds

### Phase 3: If more variety needed

7. Download latest Sonniss GDC bundle (massive, will have everything)
8. Evaluate soundcn for React integration convenience
9. Consider purchasing Dev_Tones ($) if volume of 630 pro sounds needed

### What to download for TruthScope specifically

| Sound Need | Best Source |
|------------|-----------|
| Scan start/stop beep | Octave (designed for iOS taps) |
| Heart rate detection pulse | Kenney Digital Audio |
| Analysis in progress (subtle loop) | Google Material (hero sounds) |
| Result reveal (dramatic) | Mixkit or Pixabay (search "reveal") |
| Success/truth detected | Google Material or Kenney (positive chime) |
| Warning/deception detected | Kenney Interface Sounds (alert tones) |
| Button taps throughout UI | Octave (all 48 sounds are taps/beeps/slides) |
| Onboarding transitions | SND library (designed for modern UI) |
| Party mode sounds | Sonniss GDC bundle (game audio variety) |
| Haptic sync sounds | Design custom using Octave as base + Core Haptics |

---

## NPM PACKAGES FOR PLAYBACK

| Package | Use Case | Stars | Maintained |
|---------|----------|-------|-----------|
| `expo-audio` | Expo apps, simplest API | Expo official | Yes |
| `react-native-sound` | Bare RN, lightweight | 2.8K+ | Yes |
| `react-native-audio-api` | Advanced audio graphs, Web Audio API | SW Mansion | Yes |
| `use-sound` | React web hook (not RN) | 1K+ | Josh Comeau |
| `soundcn` | React web, 700+ built-in sounds | New | Yes |

For TruthScope (Expo + React Native): use `expo-audio`. It is the official Expo audio module, cross-platform, handles background audio policies, and integrates with the Expo build pipeline.

---

## SUMMARY: Top 3 Picks for TruthScope

1. **Octave** -- 48 iOS-native UI sounds, free, no attribution. Made for exactly this use case.
2. **Kenney UI Audio + Interface Sounds + Digital Audio** -- CC0, 100+ sounds across 3 packs. Zero legal risk.
3. **Google Material Sound Resources** -- CC-BY 4.0, professional benchmark quality. Just credit Google.

Combined, these three give you 200+ professional UI sounds with essentially zero licensing risk. More than enough for any app.
