# Lie/Deception Detection via iPhone Sensors -- Technical Research

Last updated: 2026-04-01

This document covers what modern iPhones can ACTUALLY detect that's relevant to physiological stress/deception indicators, the real science behind each modality, achievable accuracy, and implementation paths for React Native/Expo.

---

## 1. Contact PPG (Finger on Camera + Flashlight)

### How It Works
The user places their fingertip over the rear camera lens while the flashlight (LED) illuminates the tissue. Blood volume changes with each heartbeat cause measurable changes in light absorption. The camera captures these pulsatile variations frame-by-frame.

### Signal Processing Pipeline

1. **Capture**: Record video at 30fps (or 60fps for better resolution) with torch ON, rear camera, lowest resolution sufficient (no need for 4K -- 480p is fine, reduces processing load).

2. **Red Channel Extraction**: Each frame is decoded and the average red channel intensity is computed across the fingertip region. Red light penetrates tissue deepest and shows the strongest pulsatile signal. Green also works well (peak oxyhemoglobin absorption) but red is standard for contact PPG with white LED.

3. **Signal Construction**: The per-frame red channel averages form a 1D time-series signal. This raw signal contains the PPG waveform riding on a DC baseline.

4. **Bandpass Filtering**: Apply a 2nd-order Butterworth bandpass filter. Passband: 0.7 Hz to 4.0 Hz (42-240 BPM range). This removes respiratory artifacts (below 0.7 Hz), DC drift, and high-frequency noise. A 5th-order zero-phase elliptic filter gives sharper cutoff if needed.

5. **Peak Detection**: Identify systolic peaks in the filtered signal. Methods:
   - Simple threshold-based: find local maxima above a rolling mean
   - First-derivative approach: peaks at zero-crossings of the derivative where slope goes from positive to negative
   - Adaptive threshold: use the signal's own statistics (mean + k * std) as threshold
   - For production: CNN-based peak detection (dilated convolutions) outperforms classical methods

6. **Heart Rate Calculation**: HR = 60 / mean(IBI), where IBI = time between consecutive peaks in seconds.

7. **HRV Extraction**: From the IBI series:
   - **RMSSD** (root mean square of successive differences) -- primary vagal tone metric, most useful for stress detection
   - **SDNN** (standard deviation of NN intervals) -- overall HRV
   - **pNN50** (percentage of successive intervals differing by >50ms)
   - **LF/HF ratio** (frequency domain, requires FFT on IBI series) -- historically used as sympathovagal balance indicator, though validity is debated

### Accuracy (validated research)
- Contact smartphone PPG vs ECG gold standard: correlations >0.996 for heart rate, with fixed biases of -0.12 to 0.10 BPM under controlled resting conditions.
- With proper calibration (camera settings, exposure lock), accuracy improves ~74% vs default settings.
- HRV metrics from smartphone PPG show acceptable agreement with ECG-derived HRV in resting, controlled environments.
- **Degradation factors**: motion artifact (huge problem), ambient light, skin tone variation, finger pressure inconsistency.

### Relevance to Deception
- Stress and cognitive load increase sympathetic nervous system activation, which:
  - Raises heart rate (typically 5-15 BPM above baseline during acute stress)
  - Decreases HRV (RMSSD drops, LF/HF ratio increases)
- These are the SAME physiological signals a polygraph measures via electrodermal and cardiovascular channels.
- **Critical limitation**: These changes reflect AROUSAL/STRESS, not deception specifically. An innocent person who is anxious produces identical signals.

### React Native Implementation Path
- Use `expo-camera` for rear camera access with `torch: 'on'`
- Use `react-native-vision-camera` for frame-by-frame pixel access (frame processor plugins)
- Extract red channel average per frame using a custom frame processor (JSI-based for performance)
- All DSP (bandpass filter, peak detection, HRV computation) can run in JS or via a native module
- Minimum measurement window: 30 seconds for HR, 60-120 seconds for reliable HRV (RMSSD needs enough IBI samples)
- Lock exposure and white balance to prevent auto-adjustment artifacts

---

## 2. Remote PPG (rPPG) -- Face Video Heart Rate

### How It Works
Blood volume changes cause subtle color fluctuations in facial skin that are invisible to the naked eye but detectable by camera. The front-facing camera captures these sub-pixel color changes, primarily in the green channel (peak oxyhemoglobin absorption wavelength).

### Processing Pipeline

1. **Face Detection**: Use Apple Vision framework or a face detection model to locate facial region of interest (ROI). Forehead and cheeks are best (most vascular, least motion).

2. **ROI Tracking**: Track the face across frames to maintain consistent skin region despite head movement.

3. **Color Signal Extraction**: Compute spatial average of green (and optionally red/blue) channel values within the ROI for each frame.

4. **Signal Separation**: Use chrominance-based methods (CHROM algorithm) or POS (Plane Orthogonal to Skin) to separate the pulse signal from motion and illumination artifacts. These leverage the fact that blood volume changes produce a specific color direction in RGB space that differs from motion artifacts.

5. **Bandpass Filter + Peak Detection**: Same pipeline as contact PPG (0.7-4.0 Hz bandpass, peak detection).

### Accuracy
- Under controlled conditions (good lighting, minimal movement, subject at rest): MAE of ~1.9 BPM vs ECG.
- Under realistic conditions (talking, moving): MAE degrades to ~5.5-8.0 BPM.
- One validation study found mean bias of 9.8 BPM with limits of agreement from -26 to +46 BPM -- indicating high variability.
- iPhone TrueDepth camera (front) adds infrared depth data that could theoretically help, but the RGB signal is what carries the PPG information.

### Relevance to Deception
- Can measure heart rate changes during questioning without requiring the subject to touch anything.
- Enables "passive" monitoring during a conversation -- subject doesn't know exactly when measurement is happening.
- Accuracy is too low for reliable HRV extraction from face video in uncontrolled settings. HR trend (up/down) is more reliable than absolute HR.

### Implementation Considerations
- Requires consistent, diffuse lighting (not direct harsh light or backlighting)
- Subject must be relatively still (talking degrades signal significantly)
- Front camera at arm's length is suboptimal -- farther = fewer pixels per face = worse SNR
- Processing is more compute-intensive than contact PPG
- Libraries: OpenCV via native module, or custom Vision framework integration

---

## 3. Voice Stress Analysis (VSA)

### What Changes During Stress/Deception

| Feature | What It Measures | Behavior Under Stress |
|---------|-----------------|----------------------|
| **Fundamental frequency (F0)** | Pitch of voice | Tends to increase (vocal cord tension from sympathetic activation). Speaker-dependent -- some people's pitch drops. |
| **Jitter** | Cycle-to-cycle pitch variation | Mixed findings. Some studies show increase, others show no discrimination for deception. |
| **Shimmer** | Cycle-to-cycle amplitude variation | Does NOT reliably correlate with stress in peer-reviewed studies. |
| **Formants (F1, F2)** | Vocal tract resonance frequencies | F1 and F2 correlate with stress (mouth/jaw tension changes resonance). |
| **Speech rate** | Words per second | Tends to decrease during deception (higher cognitive load = slower speech). |
| **Response latency** | Time to start answering | Increases during deception (cognitive load of constructing lie). |
| **Pause frequency** | Number and duration of pauses | More filled pauses ("um", "uh") and longer silent pauses during deception. |
| **Micro-tremor (8-12 Hz)** | Claimed subliminal voice tremor | **PSEUDOSCIENCE.** Commercial VSA systems (CVSA, LVA) claim to detect 8-12 Hz micro-tremors. Vocal fold vibration is 80-250 Hz, which drowns out any 8-12 Hz muscle tremor. The National Research Council (2003) concluded these systems have "little or no scientific basis." |

### Scientific Consensus on VSA Accuracy
- Peer-reviewed research: VSA systems perform at ~50% accuracy (coin flip level).
- The National Research Council's 2003 review found no scientific basis for CVSA or similar instruments.
- F0 (pitch) changes are the most reliable individual vocal indicator, but only in a speaker-dependent manner (you need a truthful baseline from the same person first).
- **Multi-feature approach** (F0 + response latency + speech rate + pause patterns) improves classification somewhat, but no published study achieves above ~65-70% accuracy with voice alone.

### What IS Implementable and Honest
- Measure F0 contour in real-time (FFT or autocorrelation on audio frames)
- Measure response latency (silence detection after question ends)
- Measure speech rate (syllable/word counting via energy envelope)
- Detect filled pauses via simple audio classification
- Present these as "stress indicators" not "lie detection"
- Require a baseline calibration phase (truthful questions first)

### React Native Implementation
- Use `expo-av` or `react-native-audio-api` for microphone access
- Audio processing: Web Audio API (via `react-native-audio-api`) for real-time FFT
- F0 extraction: autocorrelation method or YIN algorithm on audio frames
- Response latency: voice activity detection (energy threshold + zero-crossing rate)
- All audio DSP can run in JS for the features described above

---

## 4. Facial Micro-Expression Analysis (ARKit)

### What ARKit Provides
Apple's ARKit face tracking (requires TrueDepth camera = iPhone X and later) delivers:
- **52 blend shape coefficients** at 60fps, each ranging from 0.0 to 1.0
- **3D face mesh** with 1,220 vertices
- Real-time tracking of eyebrows, eyes, jaw, mouth, cheeks, nose

### Key Blend Shapes Relevant to Deception Research

| Blend Shape | FACS Equivalent | Deception Relevance |
|-------------|----------------|-------------------|
| `browInnerUp` | AU1 (Inner Brow Raise) | Part of "fear" and "sadness" expressions. Genuine distress vs. faked distress. |
| `browDownLeft/Right` | AU4 (Brow Lowerer) | Concentration, anger. Increased during cognitive load. |
| `eyeSquintLeft/Right` | AU6 (Cheek Raise) | Part of genuine smile (Duchenne). Absence during smile = masking. |
| `mouthSmileLeft/Right` | AU12 (Lip Corner Pull) | Smile without AU6 (eyeSquint) = social/masking smile, associated with deception in research. |
| `mouthFrownLeft/Right` | AU15 (Lip Corner Depressor) | Genuine grief. Absence in claimed distress = possible deception. |
| `jawOpen` | AU26/27 | Surprise. Genuine surprise is brief (<1 second). Faked surprise held longer. |
| `eyeBlinkLeft/Right` | AU45 | Blink rate increases under cognitive load. Baseline ~15-20/min, stress can increase to 25-30+/min. |
| `mouthPucker` / `mouthPress` | AU18/24 | Lip compression (AU24) associated with suppressed emotion. |

### Ekman's Research on Deception Cues
- No single facial expression reliably indicates deception. Accuracy of trained FACS coders detecting lies is only slightly above chance.
- The most useful signals are **asymmetry** (one-sided expressions suggest voluntary/faked), **duration** (micro-expressions last 1/25 to 1/5 second; macro-expressions are voluntary and last longer), and **incongruence** (smiling mouth with sad eyes).
- Deceptive subjects show more "masking smiles" (AU12 without AU6) and "failed sadness" attempts (AU1+2 frontalis contraction without lower face grief muscles).
- Liars in high-stakes situations showed more upper-face surprise and lower-face happiness than truth-tellers.

### What We Can Realistically Detect
- Blink rate changes (reliable, easy to measure via blend shapes)
- Smile authenticity (Duchenne vs non-Duchenne by comparing eyeSquint + mouthSmile)
- Micro-expression duration (flag expressions lasting <200ms as involuntary)
- Facial asymmetry (compare left/right blend shape pairs)
- Emotional incongruence (multiple simultaneous conflicting expressions)
- Cognitive load indicators (brow furrow frequency, eye squint during answers)

### Implementation
- ARKit face tracking requires native code (Swift/Objective-C bridge to React Native)
- Use `react-native-arkit` or custom native module exposing blend shape data
- Sample at 60fps, buffer blend shape values, compute derivatives for micro-expression detection
- Threshold-based detection: flag events where a blend shape spikes above 0.3 for <200ms then drops

---

## 5. Eye Tracking (Pupil Dilation, Gaze, Blink Rate)

### What's Detectable via iPhone Front Camera

| Metric | Detection Method | Accuracy | Deception Relevance |
|--------|-----------------|----------|-------------------|
| **Pupil dilation** | TrueDepth NIR camera + RGB | Median error 0.27mm absolute, 3.52% for dilation change | Pupils dilate 0.2-0.5mm under cognitive load. Deception requires more mental effort, causing dilation. |
| **Blink rate** | ARKit `eyeBlinkLeft/Right` | Very reliable at 60fps | Baseline ~15-20/min. Increases with cognitive load. Decreases during concentration (suppressed blinking during lie construction, then burst of blinks after). |
| **Gaze direction** | ARKit `eyeLookIn/Out/Up/Down` | Moderate accuracy | Gaze aversion is a commonly measured deception cue, but validity is disputed. More reliable: increased gaze fixity (staring to appear truthful). |
| **Eye openness** | ARKit `eyeWideOpen` | Reliable | Widened eyes = surprise/fear micro-expression. |

### EyeDetect System (Reference)
The commercial EyeDetect system by Converus claims 86-88% accuracy for ocular lie detection. It measures pupil diameter changes, eye movement, fixations, blinks, and reading behavior during a structured questionnaire. This uses dedicated eye-tracking hardware -- a consumer iPhone won't match this precision.

### Realistic iPhone Capability
- Pupil dilation tracking is possible with the TrueDepth camera but requires the subject to be at a consistent distance with consistent lighting (pupil size also responds to light level changes).
- Blink rate is the most reliable and easiest metric via ARKit.
- Gaze direction data from ARKit is useful as an auxiliary signal but not reliable enough as a primary deception indicator.

---

## 6. Realistic Accuracy Assessment

### What Each Modality Can Achieve Individually

| Modality | Best-Case Accuracy for Stress Detection | Deception-Specific Accuracy | Confidence Level |
|----------|----------------------------------------|----------------------------|-----------------|
| Contact PPG (HR + HRV) | 75-85% for stress vs. calm | ~60-65% for deception | Medium -- well-validated for stress, weak for deception specifically |
| rPPG (face video HR) | 60-70% for stress detection | ~55% for deception | Low -- too noisy in real conditions |
| Voice stress (F0 + latency + rate) | 60-70% for stress | ~55-60% for deception | Low-Medium -- F0 is speaker-dependent |
| Facial micro-expressions (ARKit) | N/A (categorical, not binary) | ~55-60% as classifier | Low -- even trained humans are only slightly above chance |
| Eye metrics (blink + pupil) | 65-75% for cognitive load | ~60-65% for deception | Medium -- pupil dilation is real but needs controlled conditions |

### Multi-Modal Fusion (All Channels Combined)
- **Theoretical ceiling: 65-75% accuracy** for a well-calibrated, multi-modal system with baseline comparison.
- This assumes: proper baseline calibration, controlled environment (consistent lighting, subject seated, quiet room), and a structured question protocol (control questions interspersed with relevant questions, similar to polygraph CQT method).
- Under uncontrolled conditions (normal conversation, varying lighting, movement): **55-65% accuracy** -- barely above chance for some channels.

### Comparison to Professional Instruments

| System | Claimed Accuracy | Independent Validation |
|--------|-----------------|----------------------|
| Polygraph (CQT) | 70-90% | National Academy of Sciences: ~70%, false positive rate unknown |
| EyeDetect | 86-88% | Limited independent validation |
| Commercial VSA (CVSA) | 70-90% claimed | Peer-reviewed: ~50% (chance level) |
| **Our multi-modal iPhone app** | **Honest claim: 60-70%** | Would need independent validation study |

### What to Tell Users
The app measures real physiological signals (heart rate, heart rate variability, vocal patterns, facial expressions, eye behavior) that are scientifically associated with stress and cognitive load. Deception typically increases cognitive load and stress. However:
- These same signals are produced by anxiety, nervousness, excitement, and other non-deceptive states.
- No system, including professional polygraphs, can detect "lies" with certainty.
- Results should be interpreted as "stress/arousal indicators during specific questions" not "proof of lying."

---

## 7. Legal Disclaimers and Limitations

### Required Disclaimers (Non-Negotiable)

1. **"For entertainment and educational purposes only. Not a real lie detector."** -- Every existing lie detector app on the App Store includes this. Without it, you risk false advertising claims.

2. **"This app measures physiological indicators of stress. Stress is not equivalent to deception."** -- Scientifically accurate and protects against liability.

3. **"Results should never be used to make employment, legal, relationship, or any consequential decisions about another person."** -- Critical for liability protection.

4. **"No technology, including professional polygraphs, can detect lies with certainty. The American Psychological Association states there is no unique physiological response to lying."** -- Citing APA adds credibility.

5. **"Do not use this app on anyone without their knowledge and informed consent."** -- Privacy and consent law protection.

### Legal Considerations

- **Employee Polygraph Protection Act (EPPA)**: In the US, most private employers are prohibited from using lie detectors on employees. An app claiming to be a lie detector used in employment contexts could create legal liability.
- **State laws**: Many US states have laws restricting polygraph use. Some prohibit polygraph evidence in court entirely.
- **GDPR/Privacy**: Recording someone's face, voice, and biometric data requires explicit consent in GDPR jurisdictions. The app MUST obtain consent before any recording.
- **Biometric data laws**: Illinois BIPA, Texas CUBI, Washington biometric law -- collecting biometric identifiers (face geometry, voice prints) has specific consent and disclosure requirements.
- **Apple App Store Review Guidelines**: Apps that provide inaccurate diagnostic or health information may be rejected. Framing as "entertainment" or "wellness/stress monitoring" rather than "medical device" or "lie detector" is the safe path.
- **FTC**: Claims must be substantiated. Claiming the app "detects lies" without evidence = potential FTC action. Claiming it "measures stress indicators" with real sensor data = defensible.

### Recommended App Store Positioning
- Category: Entertainment or Health & Fitness (stress monitoring angle)
- Name: Avoid "Lie Detector" as primary name. Consider "TruthSense" / "StressScope" / "Verity" with subtitle mentioning stress analysis.
- Description: Lead with the science (PPG, HRV, vocal analysis, facial tracking) and what it ACTUALLY measures. Frame deception detection as a secondary, entertainment feature.
- In-app: Show real data visualizations (heart rate graph, HRV metrics, voice pitch contour). This differentiates from pure prank apps and justifies a premium price.

---

## 8. Implementation Priority for React Native/Expo

### Phase 1 -- Contact PPG (Highest Signal, Proven Science)
- Rear camera + flashlight, finger placement
- Real heart rate and HRV measurement
- 30-60 second measurement window
- Show live HR graph, compute RMSSD
- This alone provides a legitimate wellness/stress measurement tool

### Phase 2 -- Voice Analysis
- Microphone recording during questions
- F0 extraction, response latency, speech rate
- Baseline calibration (5 truthful questions first)
- Visualize pitch contour in real-time

### Phase 3 -- Facial Analysis (ARKit)
- Requires native module bridge for ARKit blend shapes
- Blink rate, smile authenticity, micro-expression flagging
- Works simultaneously with voice analysis (front camera + mic)
- Most visually impressive feature for the user

### Phase 4 -- Multi-Modal Fusion
- Combine all channels into a composite "stress score"
- Weight channels by signal quality (contact PPG > voice > face > rPPG)
- Show per-question breakdown with individual channel contributions
- Structured question protocol with control questions

### Phase 5 -- Eye Metrics (Advanced)
- Pupil dilation from TrueDepth camera
- Requires controlled lighting conditions
- Add as "advanced mode" with environment checks

### What NOT to Build
- Do NOT claim micro-tremor (8-12 Hz) voice analysis works. It doesn't. Pseudoscience.
- Do NOT use rPPG as a primary channel. Too unreliable in uncontrolled settings. Use as supplementary only.
- Do NOT show a binary "LIE / TRUTH" result. Show a spectrum/score with the disclaimer that it represents arousal/stress level.
- Do NOT bypass the baseline calibration. Without a per-person baseline, all measurements are meaningless.

---

## 9. Key Technical Specifications

### Minimum Hardware
- iPhone X or later (TrueDepth camera required for ARKit face tracking)
- Rear camera with flashlight (all iPhones have this)
- Microphone (all iPhones have this)

### Sampling Requirements
- PPG video: 30fps minimum, 60fps preferred. Lock exposure and white balance.
- Audio: 44.1 kHz or 48 kHz sample rate. 16-bit minimum.
- ARKit blend shapes: 60fps native rate.
- Measurement duration: minimum 30 seconds per question for PPG, 5-10 seconds for voice features.

### Processing
- All DSP can run on-device (no server required)
- PPG processing: ~2ms per frame on modern iPhone
- Voice F0: real-time with 20ms frame, 10ms hop
- ARKit: native 60fps, near-zero additional processing cost
- Multi-modal fusion: simple weighted average or logistic regression model, trivially fast

### Data Privacy
- All processing should happen on-device (local-first architecture)
- Never transmit biometric data to a server
- Store session data encrypted (AES-256) if saved at all
- Offer clear data deletion option
- Comply with BIPA/GDPR for biometric data handling
