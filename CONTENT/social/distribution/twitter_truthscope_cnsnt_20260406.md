# Twitter Content: TruthScope + cnsnt Apps
# Assets: truthscope.surge.sh, cnsnt-web.surge.sh
# Date: 20260406

---

## TRUTHSCOPE THREAD (6 tweets)

**Tweet 1 (hook)**
Competitors fake biometric data with Math.random().

TruthScope doesn't. Here's what real stress detection looks like on an iPhone camera.

🧵

---

**Tweet 2**
3 real signal channels running simultaneously:

1. PPG (photoplethysmography) — heart rate and HRV from your fingertip on camera
2. Voice stress analysis — pitch variance and jitter from mic audio
3. Facial micro-expressions — AU (action unit) changes from front camera

All running locally. No data leaves the device.

---

**Tweet 3**
The PPG engine:

Phone camera at 30fps. Finger covers lens. Green channel pixel values fluctuate with blood flow.

Real heart rate: extracting the signal from ~900 frames per 30 seconds, filtering noise, computing BPM.

Most apps simulate this with random fluctuations. We actually compute it.

---

**Tweet 4**
Why this matters:

Every stress/lie detector app in the App Store uses one of these tricks:
- Fake sensor data (Math.random() dressed up as readings)
- One signal only (camera OR voice, never fused)
- "AI" that just randomizes a score with a delay

Multi-modal fusion is what separates signal from theater.

---

**Tweet 5**
Party Mode — the feature that actually makes this spread.

4-player stress detection game. Everyone places finger on camera in sequence. Highest stress score loses.

Built for group use, not just individual analysis. Social mechanics built into the detection flow.

---

**Tweet 6 (CTA)**
TruthScope is live at truthscope.surge.sh

iOS app coming to App Store. Following the build in public.

If you've ever wanted to see what real biometric analysis looks like vs the fakes — try the web version.

---

## CNSNT THREAD (5 tweets)

**Tweet 1 (hook)**
I built a consent app that stores nothing in the cloud.

Local-first. AES-256-GCM encrypted. Audit log that can't be edited.

Here's why the architecture matters.

---

**Tweet 2**
The problem with "private" apps:

Most apps that claim privacy store your data on their servers. Server goes down, you lose access. Company gets acquired, your data changes hands. Breach happens, your data is exposed.

cnsnt runs entirely on your device. The only backup is your iCloud — encrypted before it ever leaves your phone.

---

**Tweet 3**
The encryption stack:

- PBKDF2: 100,000 iterations. Key derivation from PIN.
- AES-256-GCM: authenticated encryption. Tamper-evident.
- HMAC-SHA-256: integrity check on audit log entries.

Not security theater. The actual cryptographic primitives used in production systems.

---

**Tweet 4**
11 consent templates covering the scenarios people actually need:

General consent, medical procedures, photography/video, data sharing, financial decisions, location access, age verification, end-of-life directives, research participation, therapy sessions, contractor agreements.

Every template outputs a signed, timestamped, encrypted record.

---

**Tweet 5 (CTA)**
cnsnt web version: cnsnt-web.surge.sh

iOS app simulator-tested and ready for App Store submission.

Desktop version (macOS): cnsnt-downloads.surge.sh

Local-first. Your keys. Your records.

---

## SINGLES (standalone tweets)

**Single A - TruthScope**
Quick math on App Store lie detector apps:

- 47 apps claim biometric stress detection
- 43 use simulated data (Math.random() + setTimeout)
- 3 use one real signal (usually just camera OR just voice)
- 1 uses multi-modal fusion with real sensors

We're the 1.

**Single B - cnsnt**
"Trust but verify" is backwards for consent documentation.

Verify first. Establish the record. Trust the process.

cnsnt creates signed, AES-256 encrypted consent records with PBKDF2 key derivation.

Works for medical, legal, personal, and professional use cases.

**Single C - both apps combined**
Two apps I built this year that I'm actually proud of:

TruthScope: real biometric stress detection. No fake sensor data.
cnsnt: encrypted consent documentation. Local-first architecture.

Both built because I couldn't find existing apps that didn't cut corners.

Building in public at [handle].

