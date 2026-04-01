# Lie Detector App -- Competitive Research

Date: 2026-04-01

---

## 1. Current iOS App Store Landscape

### The Market Is 99% Fake/Prank Apps

Every top result for "lie detector" on the App Store is entertainment-only:

| App | What It Actually Does |
|-----|-----------------------|
| Lie Detector Truth Test (First Class Media) | Fingerprint scan animation, random result |
| Truth and Lie Detector (Ichiban Mobile) | Finger on screen "sensors," riggable results for pranking friends |
| Lie Detector - Scanner Game | Self-describes as "a fun game," not a polygraph |
| Test Lie Detector for Prank | Random results, added "Future Prediction" gimmick |
| AI Lie Detector | Analyzes uploaded images with AI for "playful" results |
| LIE DETECTOR... FREE! | Legacy prank app, still getting downloads |

Key observation: These apps monetize through ads and simple IAP. They compete on entertainment value, not accuracy. One prank app (Prank Sounds & Lie Detector) hit 3.1M downloads with 670K in the last 30 days alone. The category has massive demand and zero real competition.

### What They All Have In Common
- Random number generators dressed up as "analysis"
- Fingerprint scan or finger-on-screen as fake biometric input
- Entertainment disclaimers
- Ad-supported with optional premium
- 3-4 star ratings from people who understand it's a prank

---

## 2. Apps Attempting Real Biometrics

A small handful try actual measurement. This is where the gap lives.

### LiarLiar.ai (Web/Desktop -- NOT a mobile app)
- Uses rPPG (remote photoplethysmography) via webcam to detect heart rate from facial skin color changes
- Monitors eye movements, facial micro-expressions, body language
- Real-time transcription with truthfulness scoring
- Designed for Zoom/Google Meet/Skype -- job interviews, negotiations
- Generates session reports with HR variability, body language metrics
- Subscription model, positioned as a professional tool
- NOT on the App Store. Desktop/web only.

### TruthScan AI (iOS)
- Claims voice stress analysis + facial micro-expression detection
- Uses ML for real-time voice and camera analysis
- Newer entrant, limited traction

### Real Lie Detector PRO (Amazon Appstore)
- Camera-based heart rate from fingertip + voice stress analysis
- Contact PPG (finger on camera lens), not remote/face-based
- Not on iOS App Store

### Converus VerifEye
- Eye behavior analysis (pupil dilation, eye movement tracking)
- Developed by University of Utah researchers since 2003
- Enterprise/law enforcement pricing
- Not a consumer app

### Gap Analysis
Nobody has built a consumer mobile app that combines REAL biometrics (camera PPG + voice analysis) with entertainment/social/party UX. LiarLiar.ai proves the tech works but only targets desktop video calls. The App Store has zero apps doing real rPPG from the phone camera for lie detection.

---

## 3. What Makes Lie Detector Content Go Viral

### The TikTok/YouTube Formula
Lie detector content consistently generates millions of views. The pattern:

1. **Couples/friends format**: One person "hooked up" to detector, other asks provocative questions
2. **Escalating questions**: Start innocent, build to relationship bombs ("Have you ever cheated?")
3. **Visual drama**: The meter/gauge/light changing provides the money shot for thumbnails
4. **Riggable results**: Creators can control outcomes for maximum drama
5. **Party game integration**: Truth or Dare + lie detection = content goldmine

### Viral Mechanics
- **Meme Lie Detector** (memeliedetector.com): Quick mode for rapid-fire content, normal mode for dramatic tension, fun meme mode for unexpected viral moments with special animations
- **TikTok filters**: "Truth or Lie Detector" filters get massive usage
- **Streamer adoption**: Twitch/YouTube live streamers use lie detector as viewer interaction
- **Physical products too**: Lie detector party games sell on TikTok Shop

### What Drives Downloads
1. Someone sees a viral lie detector video
2. They want to recreate it with their friends/partner
3. They search "lie detector" on App Store
4. They download the first thing that looks real

### The Content Creator Angle
Apps that make it EASY to create shareable content win. Features that drive virality:
- Screen recording mode with clean UI for TikTok/Reels
- Dramatic animations and sound effects on "truth" vs "lie" verdict
- Shareable result cards/images
- Party mode for groups
- Couples mode with spicy question packs

---

## 4. react-native-vision-camera Frame Processing for PPG

### Architecture
react-native-vision-camera (by mrousavy) provides native Frame Processors that run on a dedicated thread, not the JS thread. Key capabilities:

- Frame processors written in C++/Java/Objective-C execute natively
- 2-5ms per frame processing, supports 30-60 FPS
- Plugin system for custom processors (face detection, barcode, OCR exist)
- Can integrate TensorFlow Lite, MediaPipe, OpenCV
- Community MLKit plugin available for face detection (useful for rPPG face ROI)

### PPG Implementation Path
No existing plugin does PPG/rPPG. Must build custom frame processor:

**Contact PPG (finger on camera + flash):**
- Turn on torch/flash for consistent illumination
- Capture red channel intensity from frames
- Detect pulse peaks in the signal
- Well-documented algorithm, simpler than rPPG
- Most "real" heart rate apps use this approach

**Remote PPG (face via front camera):**
- Detect face region using MLKit face detection plugin
- Extract green channel signal from forehead/cheek ROI
- Apply bandpass filter (0.7-4 Hz for 42-240 BPM range)
- Use CHROM or POS algorithm for signal extraction
- More complex but more impressive UX (contactless)
- Green channel contains strongest pulsatile signal per research

### What Exists in the Ecosystem
- `react-native-vision-camera-mlkit`: Face detection, text recognition, barcode scanning
- `react-native-fast-opencv`: OpenCV bindings for frame processing
- Custom C++ frame processors: Can implement any algorithm natively

### Feasibility Assessment
Building a custom rPPG frame processor is achievable. The core algorithm (green channel extraction from face ROI, bandpass filtering, peak detection) is well-documented in academic literature. The hard part is robustness: handling motion artifacts, lighting changes, and skin tone variations. For a consumer entertainment app, 80% accuracy is more than sufficient -- current apps use literal random numbers.

---

## 5. expo-camera vs react-native-vision-camera

### Clear Winner: react-native-vision-camera

| Feature | expo-camera | react-native-vision-camera |
|---------|-------------|---------------------------|
| Real-time frame access | NO | YES (native frame processors) |
| Frame processing speed | N/A (no frame access) | 2-5ms native, 30-60 FPS |
| Custom ML integration | NO | YES (TFLite, MediaPipe, OpenCV) |
| PPG feasibility | IMPOSSIBLE | FEASIBLE |
| Weekly downloads (2026) | 529K | 451K |
| Setup complexity | Easy (Expo managed) | Moderate (requires dev client) |
| Torch/flash control | Basic | Full control |

expo-camera does not expose raw camera frames to JavaScript or native modules. This makes it impossible for real-time ML, AR, video filters, or PPG analysis. It captures frames through the JS bridge which is too slow for any real-time analysis.

**Decision: Must use react-native-vision-camera.** This means using an Expo dev client (not Expo Go), which is standard for production apps anyway.

---

## 6. React Native Audio Analysis Libraries

### Pitch Detection
| Library | What It Does | Status |
|---------|-------------|--------|
| react-native-pitchy | Two-stage pitch detection (coarse 4x downsampled + refined search) | Active, production-ready |
| react-native-pitch-detector | High performance real-time pitch detection, YIN algorithm in C++ TurboModule | Active, New Architecture |
| react-native-live-pitch-detection | Frequency, note, octave from device mic | Active |

### Voice Analysis Approach
For voice stress analysis in a lie detector:
- **Pitch variation**: Stress causes measurable pitch changes (micro-tremors at 8-12 Hz)
- **Voice onset time**: Deceptive responses show longer onset latency
- **Fundamental frequency (F0)**: Rises under stress
- **Jitter/shimmer**: Voice quality metrics that change under cognitive load

### Recommended Stack
1. `react-native-pitch-detector` (New Architecture, C++ TurboModule, lowest latency)
2. Supplement with raw audio buffer access for custom FFT analysis
3. `react-native-voice` for speech recognition (detect WHAT they said)
4. Custom spectral analysis for stress markers (voice micro-tremors, F0 tracking)

### Expo Real-Time Audio
Expo published a blog post on real-time audio processing with native code, combining high-level TypeScript with low-level C++/Swift/Kotlin modules. This approach works for custom audio analysis within an Expo dev client build.

---

## 7. THE GAP WE'RE FILLING

### Current State of the Market
- **100+ prank apps** using random numbers = huge demand signal, zero real product
- **LiarLiar.ai** proves rPPG + voice analysis works, but only on desktop for video calls
- **Zero consumer mobile apps** combining real biometrics with entertainment UX
- **Massive viral content demand** -- lie detector content gets millions of views on TikTok/YouTube

### Our Positioning
The FIRST mobile lie detector app with REAL biometric signals (camera PPG + voice stress analysis) wrapped in a viral entertainment UX. Not claiming 100% accuracy -- positioning as "the most real lie detector you can get on your phone" vs. the completely fake alternatives.

### Why This Wins
1. **Real enough to be impressive**: Actual heart rate display + voice stress meter vs. random numbers
2. **Entertainment-first UX**: Party mode, couples mode, dramatic animations, shareable results
3. **Content creator friendly**: Clean screen recording UI, result cards for TikTok/Reels
4. **Defensible moat**: Custom frame processor for PPG is hard to clone vs. random number apps
5. **Multiple monetization**: Premium question packs, ad-free, advanced analytics, couples subscription

### Viral Hooks
- "This app can actually detect your heart rate changing when you lie"
- Side-by-side with prank apps showing the difference
- Couples challenge format (already proven viral)
- Streamer/creator tool for audience interaction

---

## 8. RECOMMENDED TECH STACK

```
Camera:       react-native-vision-camera (frame processors for PPG)
Face detect:  react-native-vision-camera-mlkit (face ROI for rPPG)
Audio:        react-native-pitch-detector (voice stress via C++ TurboModule)
Speech:       react-native-voice (transcription of answers)
Build:        Expo dev client (NOT Expo Go -- need native modules)
State:        Zustand or Redux Toolkit
Animations:   react-native-reanimated (dramatic UI transitions)
Charts:       react-native-skia (real-time heart rate / stress visualization)
Payments:     Stripe Payment Links (per existing PRINTMAXX pattern)
```

### MVP Feature Set
1. Front camera rPPG heart rate detection (green channel extraction)
2. Voice stress meter (pitch analysis during speech)
3. Combined "truth score" from both signals
4. 3 modes: Solo, Couples, Party
5. Built-in spicy question packs (truth or dare style)
6. Dramatic reveal animations with sound effects
7. Shareable result cards
8. Screen recording overlay mode

### What Makes It Real vs. Fake
- Live heart rate graph updating in real-time from face
- Voice stress waveform visualization during speech
- Baseline calibration period ("tell me something true" then "tell me a lie")
- Visible biometric data that users can verify (check HR against Apple Watch)

---

## Sources

- [App Store - Lie Detector Truth Test](https://apps.apple.com/us/app/lie-detector-truth-test/id1113503715)
- [App Store - AI Lie Detector](https://apps.apple.com/us/app/ai-lie-detector/id6502961125)
- [App Store - TruthScan AI](https://apps.apple.com/gh/app/truthscan-ai-lie-detector/id6759193664)
- [LiarLiar.ai](https://liarliar.ai/)
- [LiarLiar.ai - Heart Rate Detection Mechanism](https://liarliar.ai/understanding-heart-rate-detection-through-computer-vision-a-dive-into-liarliar-ais-mechanism/)
- [TikTok Polygraph Trends](https://liedetectortest.com/alert/tiktok-polygraph-trends-viral-lie-detector-content-reviewed)
- [Meme Lie Detector](https://memeliedetector.com/truth-lie-detector)
- [VisionCamera Frame Processors](https://react-native-vision-camera.com/docs/guides/frame-processors)
- [VisionCamera Community Plugins](https://react-native-vision-camera.com/docs/guides/frame-processor-plugins-community)
- [VisionCamera MLKit Plugin](https://github.com/pedrol2b/react-native-vision-camera-mlkit)
- [React Native Fast OpenCV](https://lukaszkurantdev.github.io/react-native-fast-opencv/examples/realtimedetection/)
- [expo-camera vs VisionCamera Comparison](https://blog.patrickskinner.tech/react-native-camera-expo-vs-visioncamera-what-you-need-to-know)
- [PkgPulse - Camera Libraries 2026](https://www.pkgpulse.com/blog/react-native-vision-camera-vs-expo-camera-vs-expo-image-picker-2026)
- [react-native-pitchy](https://github.com/rnheroes/react-native-pitchy)
- [react-native-pitch-detector](https://github.com/1fabiopereira/react-native-pitch-detector)
- [Expo Real-Time Audio Processing](https://expo.dev/blog/real-time-audio-processing-with-expo-and-native-code)
- [Awesome rPPG Research](https://github.com/zx-pan/Awesome-rPPG)
- [Understanding rPPG - Rouast Labs](https://www.rouast.com/blog/articles/understanding-remote-photoplethysmography/)
- [rPPG Review - Nature Communications Medicine](https://www.nature.com/articles/s43856-024-00519-6)
- [Converus VerifEye](https://converus.com/verifeye/)
