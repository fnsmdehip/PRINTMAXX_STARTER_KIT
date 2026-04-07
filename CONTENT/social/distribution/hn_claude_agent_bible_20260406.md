# HN Posts: Show HN submissions
# Date: 20260406

---

## SHOW HN #1
**Title:** Show HN: I run 33 autonomous AI agents on a MacBook using cron, launchd, and Claude Code

**URL:** (link to truthscope.surge.sh as the most polished live product, or a dedicated landing page)

**Body for comments:**

I've been building an autonomous business system for the past 6 months. The stack is simpler than most "agent" frameworks suggest it needs to be.

The full architecture:
- 33 agents across 3 layers: pure automation (cron), AI-assisted (event-triggered Claude calls), fully autonomous (read state, decide, act, write state, exit)
- Inter-agent communication via a JSONL message bus file — no queue service needed
- Persistent memory via filesystem — every agent reads/writes JSON state files, stateless per run
- Model routing: Opus for strategic decisions, Sonnet for execution, Haiku for classification/routing
- Failure handling: lock files, 30-min hard timeouts, dead agent detection via cron watchdog

The "Ralph loop" is the overnight execution pattern: `while :; do cat PROMPT.md | claude --dangerously-skip-permissions --print; done`. PROMPT.md drives the agent. Memory is files. Context is disposable. Ships deliverables by morning.

I wrote up the full architecture as a guide ($47). Happy to answer questions here for free — the guide is the deep-dive with the actual configs, cron templates, and agent catalog.

**Key question I've been thinking about:** at what agent count does a JSONL message bus start to break down? Running 33 with no issues but curious where the ceiling is before you need an actual queue.

---

## SHOW HN #2
**Title:** Show HN: TruthScope — biometric stress detection using real PPG, voice analysis, and facial AUs (no simulated data)

**URL:** truthscope.surge.sh

**Body for comments:**

Most stress detection apps in the App Store use Math.random() with a setTimeout to simulate sensor readings. I wanted to see what real multi-modal detection looks like on consumer hardware.

TruthScope uses 3 signal channels:

1. PPG via rear camera: finger on lens, green channel pixel value fluctuations track blood volume pulse. ~900 frames per 30 seconds. FFT to extract BPM and HRV.

2. Voice stress analysis: pitch (F0) extraction using YIN algorithm, jitter (cycle-to-cycle frequency variation), shimmer (amplitude variation), harmonics-to-noise ratio. These are the actual acoustic correlates used in vocal stress research.

3. Facial micro-expressions: Action Unit detection via front camera. AU4 (brow lowerer), AU6/7 (eye narrowing), AU17/23 (lip stress markers). Not face recognition — feature tracking.

Multi-modal fusion: weighted scoring across all 3 channels. The "Party Mode" feature runs 4 players sequentially and ranks by stress level — surprisingly viral in early testing.

What I got wrong: camera PPG is genuinely less accurate than dedicated sensors. I say so explicitly in the app. Honest positioning matters more than claims of "medical grade accuracy."

Built with React Native / Expo SDK 54, react-native-vision-camera for real frame data, react-native-pitch-detector for voice F0.

---

## SHOW HN #3
**Title:** Show HN: cnsnt — encrypted consent documentation, local-first, AES-256-GCM, no cloud storage

**URL:** cnsnt-web.surge.sh

**Body for comments:**

Built this because every "consent" app I found either stored data on company servers or used weak encryption. Neither is acceptable for sensitive consent records.

Architecture decisions:
- All data stays on device (or encrypted iCloud backup)
- Key derivation: PBKDF2, 100K iterations, from user PIN
- Encryption: AES-256-GCM (authenticated — tamper-evident)
- Audit log: HMAC-SHA-256 integrity check on each entry
- No server, no account, no cloud sync without explicit user action

11 templates: general consent, medical procedures, photography, data sharing, financial, location, age verification, end-of-life, research participation, therapy, contractor.

Each creates a signed, timestamped, encrypted record. Records export as PDF for physical documentation needs.

The local-first architecture means: no breach risk on our end (nothing to breach), works offline, works if we shut down the service, user can verify the cryptography themselves.

Web version at cnsnt-web.surge.sh. iOS app pending App Store review. macOS desktop at cnsnt-downloads.surge.sh.

Technical question: for audit log integrity, I'm using HMAC-SHA-256 on each entry with a chain structure (each entry includes a hash of the previous entry). Is there a better pattern for tamper-evident append-only logs in a client-side context?

