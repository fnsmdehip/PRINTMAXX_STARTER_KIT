# TruthScope Launch Content
# Date: 2026-04-01
# Platforms: Twitter/X
# Status: READY TO POST

---

## TWEET 1 — The "Every App is Fake" Angle

Every lie detector app on the App Store is fake.

Random number generators with fingerprint animations. Needles that bounce for no reason. 100+ apps, zero real measurement.

So I built one that actually reads your heart rate, analyzes your voice, and tracks your facial micro-expressions.

TruthScope. Real biometrics. Real signals. Still not a polygraph. But it's the closest thing your iPhone can get.

[App Store link]

---

## TWEET 2 — The Tech/Builder Angle

Your iPhone camera can detect your heartbeat through your fingertip.

Blood volume changes cause measurable shifts in light absorption. Frame-by-frame red channel extraction + bandpass filtering at 0.7-4.0 Hz + peak detection = real-time heart rate and HRV.

Validated to correlate >0.996 with ECG.

We turned that into a lie detector app.

TruthScope ships today.

[App Store link]

---

## TWEET 3 — The Viral/Streamer Angle

Lie detector content gets millions of views on TikTok.

Couples asking "have you ever cheated?" with a meter bouncing around.

Problem: every app they use is literally a random number generator.

TruthScope actually measures your heart rate, voice stress, and facial behavior in real-time.

Built-in Party Mode. 30+ questions. Dramatic verdict animations.

Streamers and content creators are going to have a field day with this.

[App Store link]

---

## THREAD — How TruthScope Works (Technical Breakdown)

### Tweet 1/7 (Hook)

I built a lie detector app that uses real biometric signals instead of random numbers.

4 detection engines. 3 sensor modalities. Multi-modal fusion scoring.

Here's exactly how it works and what the science actually says:

### Tweet 2/7 (Finger Pulse / PPG)

ENGINE 1: Contact PPG

Put your finger on the rear camera. Flash turns on. Blood volume changes with each heartbeat cause measurable shifts in red light absorption.

We extract the red channel average per frame, detrend it, bandpass filter at 0.7-4.0 Hz, detect peaks, and calculate HR + HRV (RMSSD).

Smartphone PPG vs ECG gold standard: >0.996 correlation for heart rate.

HRV drops when you're stressed. HR rises. Same signals a polygraph measures.

### Tweet 3/7 (Face Scan / rPPG)

ENGINE 2: Remote PPG

Your face has invisible color fluctuations caused by blood flow. The front camera captures them.

Green channel extraction from forehead/cheek ROI. CHROM algorithm separates the pulse signal from motion artifacts.

No contact needed. The subject doesn't even need to touch the phone.

Under controlled conditions: ~1.9 BPM mean absolute error vs ECG.

### Tweet 4/7 (Voice Analysis)

ENGINE 3: Voice Stress

When you lie, your brain works harder. That shows up in your voice.

Fundamental frequency (pitch) rises from vocal cord tension. Response latency increases because fabricating an answer takes more processing than remembering truth. Speech rate shifts.

We measure F0, jitter, shimmer, response latency, and speech patterns in real-time at 44.1 kHz.

### Tweet 5/7 (Facial Behavior)

ENGINE 4: Facial Behavior Analysis

Blink rate: baseline 15-20/min, jumps to 25-30+ under cognitive load.

Duchenne smile detection: real smiles engage the eyes (eyeSquint). Fake smiles don't.

Micro-expressions last under 200ms. Facial asymmetry indicates voluntary (faked) vs involuntary (genuine) expressions.

We track blink rate, gaze stability, asymmetry, lip compression, and eye contact percentage.

### Tweet 6/7 (Multi-Modal Fusion)

All four engines feed into a deception analyzer.

Weighting based on published meta-analyses:
- Physiological (PPG): 40%
- Vocal analysis: 30%
- Facial cues: 30%

Temporal smoothing accounts for question-response spikes. Confidence scoring adjusts for signal quality and measurement duration.

Baseline calibration first. Then the real questions.

### Tweet 7/7 (The Honest Part + CTA)

Let me be direct about what this is and what it isn't.

It measures real biometric signals. Peer-reviewed signal processing. Actual data from your body.

But no lie detection technology is 100% accurate. Professional polygraphs hover around 70%. Stress is not the same as deception.

TruthScope is the most real lie detector you can put on a phone. Built for parties, content, and curiosity. Not courtrooms.

Available now.

[App Store link]

---

## DISTRIBUTION NOTES

- Tweet 1 targets the broad audience. Lead with the gap. Best for first post.
- Tweet 2 targets indie hackers and technical audiences. The >0.996 stat is the money line.
- Tweet 3 targets streamers, content creators, couples content. Viral angle.
- Thread is the deep dive. Post 2-4 hours after the initial tweet for a second wave.
- Cross-post Tweet 1 to Reddit: r/sideproject, r/indiegaming (party game angle), r/streaming
- Cross-post Thread to LinkedIn as a long-form post about the build process
- Tweet 3 should be quote-tweeted by secondary accounts tagging streamers
