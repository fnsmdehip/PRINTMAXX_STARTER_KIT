# Vision API Wrapper Factory

**Last updated:** 2026-02-27
**Purpose:** Build 10 niche camera apps that wrap powerful vision APIs behind beautiful, niche-specific mobile UIs. Each app is a separate $4.99-$9.99/mo subscription product. User points camera at thing, API identifies it, app presents results the way a niche insider would want them.
**Stack:** PWA (vanilla HTML/JS or Next.js) + MediaDevices API + Vision API + Capacitor for iOS + RevenueCat/Stripe
**Revenue model:** Freemium (5 free scans/day) + Pro ($4.99/mo) + Premium ($9.99/mo) + Affiliate
**References:** APP_QUALITY_STANDARDS.md, IOS_REJECTION_PREVENTION.md, IOS_SUBMISSION_PROCESS.md, AGGREGATE_DESIGN_SYSTEM.md

---

## 1. The play

Vision APIs are absurdly cheap and absurdly powerful. Google Cloud Vision does 1,000 image classifications for $1.50. Gemini Flash does multimodal understanding for $0.01/image. GPT-4o Vision does contextual reasoning for $0.01-0.03/image. Apple Vision and TensorFlow.js do basic classification for free, on-device, offline.

Normal people have no idea these APIs exist. They just know they want to point their phone at a plant and find out what it is. Or photograph their dinner plate and get calories. Or snap a picture of a bug and know if it bites.

The play: take the raw API, wrap it in a niche-specific UI with niche-specific language, niche-specific result formatting, and niche-specific affiliate product recommendations. Sell as a standalone subscription app. The API does the hard work. We do the UX and the marketing.

PlantNet (plant identification) has 50M+ downloads. MyFitnessPal (food logging, includes photo scan) was acquired for $475M. Picture Insect has 30M+ downloads. These are all vision API wrappers with nice UIs. The pattern is validated at scale.

Build time per app: ~1 hour of customization on top of a shared template. Total portfolio: 10 apps in 12 hours of actual development.

---

## 2. API options (ranked by cost/quality)

| Rank | API | Cost per image | Best for | Offline | Latency | Notes |
|------|-----|---------------|----------|---------|---------|-------|
| 1 | **Google Cloud Vision** | $1.50/1K ($0.0015/img) | Labels, objects, OCR, logos, landmarks, faces, safe search | No | 300-800ms | Most mature. Excellent label detection. Free 1K/mo tier. |
| 2 | **Gemini 2.0 Flash** | ~$0.01/image | Multimodal understanding, contextual reasoning, conversational follow-up | No | 500-1500ms | We already have an API key. Best understanding of context. Can ask follow-up questions about the image. |
| 3 | **GPT-4o Vision** | $0.01-0.03/image | Best contextual understanding, nuanced descriptions, safety analysis | No | 1-3s | Most expensive but highest quality reasoning. Best for health/safety apps (DermLens, ForageLens). |
| 4 | **Apple Vision (VNClassifyImageRequest)** | FREE | On-device classification, text recognition, barcode/QR, face detection | Yes | 50-200ms | Only works on Apple devices via Capacitor. Fastest. No network needed. Limited to Apple's pre-trained models. Good fallback. |
| 5 | **TensorFlow.js (MobileNet, COCO-SSD)** | FREE | On-device object detection, basic classification, custom models | Yes | 100-500ms | Works in browser. Can load custom models. Good for offline fallback. Limited accuracy vs cloud APIs. |
| 6 | **Clarifai** | $0.004/image | Specialized models: food recognition, fashion, moderation, general | No | 400-1200ms | Pre-built niche models (food, apparel, textures). Good for CalorieSnap and StyleSnap specifically. Food model identifies 1,000+ food items with nutritional data. |
| 7 | **Roboflow** | Free tier 1K/mo, then $0.004/img | Custom object detection, community models | No | 200-800ms | 90,000+ pre-trained models in universe. Find niche-specific models (crystals, insects, mushrooms). Train custom if needed. |
| 8 | **AWS Rekognition** | $1.00/1K images | Labels, faces, text, custom labels | No | 200-600ms | Comparable to Google Vision. Slightly cheaper at scale. |

### Recommended strategy per app

- **Primary:** Gemini Flash or GPT-4o (best understanding, we have keys)
- **Fallback:** TensorFlow.js on-device (offline mode, free)
- **Specialized:** Clarifai food model for CalorieSnap, Roboflow community models for niche apps

### Cost optimization tactics

1. **Cache common results.** Same plant species = same care instructions. Cache by perceptual image hash (pHash).
2. **On-device pre-classification.** TensorFlow.js identifies "this is a plant" locally, then send to cloud only for species-level ID. Eliminates 30-40% of API calls.
3. **Compress images before sending.** Resize to 640x480, JPEG quality 80 = 90% smaller payload vs full-res. Most vision APIs work fine at this resolution.
4. **Rate-limit free tier.** 5 scans/day prevents abuse, drives upgrade conversions.
5. **Batch similar requests.** If user scans 3 plants in 60 seconds, batch into single API call with multi-image prompt.
6. **Tiered model routing.** Simple identifications (common houseplants, popular dog breeds) use Gemini Flash ($0.01). Complex/safety-critical (mushrooms, skin concerns) use GPT-4o ($0.02-0.03). Route based on on-device pre-classification confidence.

---

## 3. Core architecture (shared across all 10 apps)

Every vision wrapper app uses the same codebase. The only things that change per app: theme colors, result formatting, prompt text, affiliate links, and copy.

### Shared template structure

```
vision-app-template/
├── index.html              # Camera UI + results display + onboarding + paywall
├── camera.js               # Camera access, capture, image compression
├── api.js                  # Vision API connector (swappable per app)
├── results.js              # Niche-specific result formatting + affiliate injection
├── history.js              # Scan history (IndexedDB for offline)
├── subscription.js         # RevenueCat/Stripe subscription management
├── styles.css              # Niche-specific theming (CSS variables)
├── manifest.json           # PWA manifest (name, icons, colors)
├── sw.js                   # Service worker (offline cache, queued scans)
├── config.js               # API keys, niche config, pricing, prompts
├── onboarding.js           # 4-screen onboarding flow
├── analytics.js            # PostHog/Plausible event tracking
└── capacitor.config.json   # iOS/Android native wrapper config
```

### Camera flow (camera.js)

```
User taps "Scan" button
  -> Request camera permission (getUserMedia, rear camera preferred)
  -> Show live viewfinder (video element)
  -> User taps capture button
  -> Freeze frame, show capture animation + haptic feedback
  -> Compress image (canvas -> JPEG, 640x480, quality 0.8)
  -> Convert to base64
  -> Send to api.js
  -> Show skeleton loading state with niche-specific copy ("Identifying your plant...")
  -> Receive results
  -> Pass to results.js for niche-specific formatting
  -> Display results card with affiliate recommendations
  -> Save to history (IndexedDB)
```

### API connector (api.js)

Swappable per app. config.js determines which API to call.

```javascript
const APIS = {
  gemini: async (imageBase64, prompt) => {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${CONFIG.GEMINI_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{
            parts: [
              { text: prompt },
              { inline_data: { mime_type: 'image/jpeg', data: imageBase64 } }
            ]
          }]
        })
      }
    );
    return response.json();
  },

  googleVision: async (imageBase64, features) => {
    // Google Cloud Vision API -- label detection, OCR, etc.
  },

  openai: async (imageBase64, prompt) => {
    // GPT-4o Vision -- highest quality, used for health/safety apps
  },

  tensorflowLocal: async (imageElement) => {
    // On-device TF.js classification (offline fallback)
  }
};
```

### Niche-specific prompt engineering

Each app has a carefully crafted system prompt that shapes the API response into the exact format the niche audience expects. This is the moat. The API is the same for everyone. The prompt determines the product.

**Example prompt -- LeafLens (plant ID):**
```
You are an expert botanist. Analyze this plant image. Return JSON:
{
  "common_name": "string",
  "scientific_name": "string",
  "family": "string",
  "confidence": 0-100,
  "care": {
    "light": "full sun / partial shade / shade",
    "water": "frequency and amount",
    "soil": "type",
    "temperature": "range in F"
  },
  "toxicity": {
    "pets": true/false,
    "children": true/false,
    "details": "string"
  },
  "fun_fact": "string",
  "similar_species": ["string", "string"]
}
If uncertain, say so. Never guess on toxicity -- err on the side of caution.
If the image is not a plant, say so clearly.
```

**Example prompt -- CalorieSnap (food/macros):**
```
You are a registered dietitian analyzing a meal photo. Identify all visible food
items and estimate portions. Return JSON:
{
  "meal_name": "string (e.g. 'Grilled chicken with rice and broccoli')",
  "items": [
    {
      "name": "string",
      "portion": "string (e.g. '6 oz')",
      "calories": number,
      "protein_g": number,
      "carbs_g": number,
      "fat_g": number,
      "fiber_g": number
    }
  ],
  "total_calories": number,
  "total_protein_g": number,
  "total_carbs_g": number,
  "total_fat_g": number,
  "meal_score": 1-10,
  "suggestions": ["string"]
}
Err conservative on portions. Round to nearest 5 calories.
Note visible condiments and drinks. If uncertain about portion size, give a range.
```

### Subscription flow (subscription.js)

Same for all apps. RevenueCat for iOS (via Capacitor), Stripe for web.

**Free tier:**
- 5 scans per day (tracked in localStorage + server-side, reset at midnight)
- Basic identification only
- No history
- Ads between scans (AdMob interstitial, every 3rd scan)

**Pro ($4.99/mo):**
- Unlimited scans
- Full detailed analysis
- Scan history (last 90 days)
- No ads
- Export results (share card, CSV)

**Premium ($9.99/mo):**
- Everything in Pro
- API integrations (share to Apple Health for CalorieSnap, export data)
- Priority processing (faster API, higher quality model)
- Offline mode (TensorFlow.js fallback with downloaded models)
- Family sharing (up to 5 devices)

---

## 4. The 10 apps (detailed specs)

---

### App 1: LeafLens (Plant Identification)

**Name options:** LeafLens, Botaniq, PlantPulse, Frondly
**Name verdict:** LeafLens. Sounds like something a plant parent would actually use. "Lens" is established camera-app convention. Short, memorable, alliterative.

**Target audience + market size:**
- Plant parents (18-45, 65% female, urban). 66% of US households have at least one houseplant.
- Home gardeners (35-65, suburban). 55% of US households garden.
- Hikers/nature walkers who want to identify wild plants.
- Parents worried about toxic plants around kids and pets.
- Market size: $1.2B plant care app market (2025). PlantNet has 50M+ downloads. PictureThis has 100M+ and does $100M+ ARR.

**Vision API:** Gemini Flash (primary) + TensorFlow.js MobileNet (offline fallback)
- Why Gemini: Multimodal understanding means it can identify plants from partial views, flowers, bark, or leaves. Can also answer follow-up questions ("Is this safe for cats?"). $0.01/image.
- Why not Google Vision: Generic labels ("plant", "flower") are too vague for species-level ID.
- Fallback: TF.js with PlantNet's open model for offline basic classification.

**Monetization:**
- Subscription: Free (5/day) -> Pro $4.99/mo -> Premium $9.99/mo
- Affiliate: Amazon plant care products (pots, soil, fertilizer, grow lights). Average commission: 4-8%. Embed product recs in every scan result. "Your Monstera needs humidity. Here's a misting bottle we recommend."
- Seasonal upsell: "Overwintering guide" PDF ($2.99 IAP) in October. "Spring planting calendar" in March.
- Estimated affiliate revenue per user: $0.15-0.40/mo (2-3 product clicks/mo, 5% conversion, $2-3 commission)

**API cost per user per month:**
- Free users: 5 scans/day x 20 active days = 100 scans x $0.01 = $1.00/mo
- Pro users: 8 scans/day x 25 active days = 200 scans x $0.01 = $2.00/mo
- Premium users: 12 scans/day x 28 active days = 336 scans x $0.01 = $3.36/mo

**Revenue per user (margin):**
- Pro: $4.99 - $2.00 API - $0.75 Apple 15% - $0.10 infra = **$2.14 margin (43%)**
- Premium: $9.99 - $3.36 - $1.50 - $0.10 = **$5.03 margin (50%)**
- Plus affiliate: +$0.15-0.40/mo

**ASO keywords (100 chars):** plant identifier,leaf scan,garden plant,toxic plant,houseplant care,plant disease,flower id,weed identify

**Content marketing:**
- @selahmoments: "God's creation is incredible. Scanned 5 plants on my walk today." (nature appreciation angle)
- @repscheme: Plant-based nutrition angle. "Identified wild herbs on my hike."
- @toolstwts: "I built a plant ID app using Gemini Vision API. Here's how."
- TikTok: "POV: You scan every plant in your house to check if it's toxic for your cat" (pet safety content goes viral)
- Reddit: r/houseplants (3.2M members), r/gardening (6.7M), r/PlantIdentification (427K), r/IndoorGarden (1.3M)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| PictureThis | 100M+ | $100M+ ARR | $29.99/year feels expensive. Aggressive upselling. 2.3-star recent reviews. Inaccurate on houseplants. |
| PlantNet | 50M+ | Free (research) | No care instructions. No toxicity. Academic UI, not consumer-friendly. |
| Planta | 10M+ | $50M+ ARR | Plant ID is secondary feature. Primarily a watering reminder. $35.99/year. |
| Seek by iNaturalist | 10M+ | Free | Volunteer-powered. Slow ID. No care instructions. Academic feel. |
| LeafSnap | 5M+ | Unknown | Outdated. Last major update 2023. Poor accuracy on recent reviews. |

**Our edge:** $4.99/mo undercuts PictureThis ($7.99/mo). We include toxicity warnings for pets and children (parents and pet owners care deeply). We use Gemini for follow-up questions ("Can I propagate this?"). We have niche content marketing via our owned accounts.

**Cross-promotion:** LeafLens results page: "Track your garden walks -> Steplock." Push notification: "Your Monstera needs sunlight. Track your own sunlight exposure with biomaxx."

---

### App 2: CalorieSnap (Meal Photo Calorie Counter)

**Name options:** CalorieSnap, MealLens, PlateScan, MacroShot, NutriSnap
**Name verdict:** CalorieSnap. Direct, says exactly what it does. People search "calorie counter" not "nutrition scanner."

**Target audience + market size:**
- Fitness enthusiasts tracking macros (18-40, 55% male)
- Dieters (all ages, 60% female)
- Diabetics monitoring carb intake (30-70)
- Bodybuilders in prep (meal tracking is mandatory)
- Market size: $4.4B health and fitness app market. MyFitnessPal has 200M+ registered users. Cal.ai (hard paywall, $8.33/mo) raised $1M+ from users.

**Vision API:** Gemini Flash (primary) + Clarifai Food model (validation)
- Why Gemini: Can understand plate composition, estimate portions from visual cues, handle complex mixed dishes. $0.01/image.
- Why Clarifai backup: Pre-trained food model identifies 1,000+ food items with nutritional data. $0.004/image. Use for cross-reference.

**Monetization:**
- Subscription: Free (5/day) -> Pro $4.99/mo -> Premium $9.99/mo
- Affiliate: Supplement brands (protein powder, vitamins, meal prep containers). Commission: 10-20%. Embed: "You're 30g short on protein today. Here's a protein powder that fits your macros."
- Partner: Meal delivery (HelloFresh, Factor, Trifecta). CPA: $15-40 per signup.
- Estimated affiliate per user: $0.50-1.50/mo (supplement recs convert well with fitness audience)

**API cost per user per month:**
- Free/Pro: ~$1.00/mo (meals are naturally capped at 3-5/day)
- Premium: ~$1.40/mo

**Revenue per user (margin):**
- Pro: $4.99 - $1.00 - $0.75 - $0.10 = **$3.14 margin (63%)**
- Premium: $9.99 - $1.40 - $1.50 - $0.10 = **$6.99 margin (70%)**
- Best margins in portfolio because meal scans are naturally rate-limited by eating frequency

**ASO keywords (100 chars):** calorie counter photo,food scanner,macro tracker,meal calories,plate scan,nutrition ai,diet log,carb count

**Content marketing:**
- @repscheme (fitness): "Scanned my meal prep. 2,847 calories, 195g protein. In 3 seconds."
- TikTok: "Scan your Chipotle order" challenge. "How many calories is a Costco food court trip?"
- Reddit: r/loseit (3.6M), r/MealPrepSunday (3.3M), r/1200isplenty (1.1M), r/CICO (534K), r/bodybuilding (2.1M)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| MyFitnessPal | 200M+ | $200M+ ARR | Photo scan buried, inaccurate. Manual barcode is core. $19.99/mo premium. Bloated. |
| Lose It | 50M+ | ~$80M ARR | Photo scan poor accuracy. Manual correction 70% of time. $39.99/year. |
| Cal.ai | 1M+ | ~$2M ARR (est) | Hard paywall $8.33/mo. Only photo scan, no manual entry. Good accuracy but expensive. |
| Yazio | 50M+ | ~$70M ARR | German-made. Photo scan added recently. Primarily manual. $6.99/mo. |
| FatSecret | 10M+ | ~$20M ARR | Free with ads. Photo scan poor quality. Outdated UI. |

**Our edge:** CalorieSnap is ONLY photo scanning, done extremely well. No bloated food diary, no exercise logging, no social features. Point, scan, get macros. 3 seconds. Cal.ai proved this model works. We undercut at $4.99/mo with a free tier funnel. We add supplement affiliate recs that Cal.ai doesn't.

**Cross-promotion:** "Track your daily nutrition streak" links to Streakr. "Optimize your sleep for better metabolism" links to Dusk.

---

### App 3: DermLens (Skin Concern Analysis)

**Name options:** DermLens, SkinScan, ClearView, SkinPulse, SpotCheck
**Name verdict:** DermLens. "Derm" signals dermatological credibility without claiming to be medical advice.

**Target audience + market size:**
- Skincare enthusiasts (18-35, 75% female)
- Acne sufferers seeking product recommendations
- People with moles/spots wanting preliminary screening
- Market size: $5.6B skincare app market by 2028. SkinVision has 2M+ downloads. TroveSkin has 5M+.

**Vision API:** GPT-4o Vision (primary) -- deliberately choosing the most accurate model for health-adjacent content
- Why GPT-4o: Health-related analysis demands highest accuracy. Worth the extra $0.02-0.03/image for liability reduction.
- CRITICAL: Every result includes prominent disclaimer: "This is not medical advice. Consult a dermatologist for diagnosis."

**Monetization:**
- Subscription: Free (3/day) -> Pro $6.99/mo -> Premium $12.99/mo (premium pricing justified by health category)
- Affiliate: CeraVe, La Roche-Posay, Paula's Choice, The Ordinary. Skincare affiliate commissions: 8-15%. Every scan = personalized product recommendations with affiliate links.
- Referral: Telehealth dermatology (MDLive, Nurx, Curology). CPA: $20-50.
- Estimated affiliate per user: $1.00-3.00/mo (skincare buyers have high AOV, $30-80)

**API cost per user per month:**
- Pro: 100 scans x $0.02 = $2.00/mo
- Premium: 200 scans x $0.02 = $4.00/mo

**Revenue per user (margin):**
- Pro: $6.99 - $2.00 - $1.05 - $0.10 = **$3.84 margin (55%)**
- Premium: $12.99 - $4.00 - $1.95 - $0.10 = **$6.94 margin (53%)**
- Plus affiliate: +$1.00-3.00/mo (skincare affiliate is high-margin)

**ASO keywords (100 chars):** skin analyzer,acne scanner,mole check,skincare routine,skin type test,dermatology,rash identifier,skin ai

**Content marketing:**
- TikTok: "I scanned my face and it told me exactly what products I need" (#skincare has 200B+ views)
- Reddit: r/SkincareAddiction (2.2M), r/acne (354K), r/30PlusSkinCare (455K)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| SkinVision | 2M+ | ~$10M ARR | Only mole/melanoma. $19.99/quarter. No product recs. Clinical feel. |
| TroveSkin | 5M+ | ~$5M ARR | General analysis. Outdated AI. Generic product recs. |
| Skinive | 2M+ | ~$3M ARR | Medical focus. Not consumer-friendly. |

**Our edge:** We're the Wirecutter of skincare. Every scan = personalized product recommendation with affiliate link. "You have combination skin with mild rosacea around your nose. Here are 3 products: CeraVe Moisturizing Cream, Paula's Choice BHA, La Roche-Posay Cicaplast."

**LEGAL:** Never diagnose. Never say "you have eczema." Say "this appears similar to what dermatologists describe as..." Include "Not medical advice" on every result screen. Have a lawyer review the disclaimer. Health category gets extra Apple review scrutiny.

---

### App 4: TypeSnap (Font Identification)

**Name options:** TypeSnap, FontLens, TypeID, GlyphFinder
**Name verdict:** TypeSnap. Designers call fonts "type." Clean, professional, insider-sounding.

**Target audience + market size:**
- Graphic designers (25-45). Small but loyal niche.
- Brand designers, social media managers, design students.
- Market size: WhatTheFont has 10M+ downloads. $600M font licensing market.

**Vision API:** Google Cloud Vision OCR (text detection) + Gemini Flash (font matching)
- Dual approach: OCR extracts text + visual characteristics. Gemini analyzes letterforms and matches.
- Cost: $0.0015 (OCR) + $0.01 (Gemini) = $0.0115/scan

**Monetization:**
- Subscription: Free (3/day) -> Pro $3.99/mo -> Premium $7.99/mo (smaller market, lower price)
- Affiliate: MyFonts, Creative Market, Adobe Fonts. Commission: 10-20% on $20-50 font purchases.
- Estimated affiliate per user: $0.50-2.00/mo

**Revenue per user (margin):**
- Pro: $3.99 - $1.32 - $0.60 - $0.10 = **$1.97 margin (49%)**
- Premium: $7.99 - $3.00 - $1.20 - $0.10 = **$3.69 margin (46%)**

**ASO keywords (100 chars):** font identifier,font finder,what font,typography scanner,font match,typeface id,design tool,font camera

**Content marketing:**
- @toolstwts: "Point your camera at any sign and instantly know the font."
- Reddit: r/graphic_design (3.7M), r/typography (365K), r/identifythisfont (115K)
- TikTok: "Scanning fonts in the wild" walking series

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| WhatTheFont | 10M+ | Unknown | Inaccurate on custom fonts. Only suggests MyFonts catalog (conflict of interest). Clunky UI. |
| Adobe Capture | 5M+ | Free (Adobe sub) | Requires Adobe subscription. Feature buried. Not focused. |

**Our edge:** Show free alternatives (Google Fonts) alongside paid options. WhatTheFont only shows paid fonts because Monotype wants sales. Designers love free alternatives.

---

### App 5: CrystalLens (Crystal/Gemstone Identification)

**Name options:** CrystalLens, StoneID, GemSnap, RockOracle
**Name verdict:** CrystalLens. The community says "crystals," not "rocks" or "gems."

**Target audience + market size:**
- Crystal collectors and spiritual community (18-45, 80% female)
- New-age/wellness community (massive overlap with yoga, meditation, astrology)
- Market size: $2.3B crystal market (2024), growing 6.5% annually. Crystal content on TikTok has 30B+ views. #crystaltok is one of the largest wellness niches.

**Vision API:** Gemini Flash (primary)
- Why Gemini: Crystal identification requires understanding color, translucency, crystal structure, luster, matrix patterns. Can also generate metaphysical properties and chakra associations.
- Cost: $0.01/image

**Monetization:**
- Subscription: Free (5/day) -> Pro $4.99/mo -> Premium $9.99/mo
- Affiliate: Energy Muse, Healing Crystals, Etsy crystal shops. Commission: 10-15%. Crystal care products (charging plates, selenite bowls, sage bundles). 8-12%.
- Digital products: "Crystal healing guide" ebook ($4.99 IAP). "Birth chart crystal guide" ($2.99 IAP).
- Estimated affiliate per user: $0.30-1.00/mo

**Revenue per user (margin):**
- Pro: $4.99 - $1.00 - $0.75 - $0.10 = **$3.14 margin (63%)**
- Premium: $9.99 - $2.50 - $1.50 - $0.10 = **$5.89 margin (59%)**

**ASO keywords (100 chars):** crystal identifier,gemstone scanner,rock id,crystal healing,chakra crystals,mineral identify,stone finder

**Content marketing:**
- @voidpilled (esoteric): DIRECT product fit. "Scanned the crystal I found hiking. It's labradorite. Third eye chakra."
- @selahmoments: "God created 4,000 minerals on Earth. Here are the ones I found today."
- TikTok: "Scanning my crystal collection." "Is your crystal real or fake?" series.
- Reddit: r/crystals (289K), r/Minerals (292K), r/rockhounds (183K)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| Rock Identifier | 5M+ | ~$8M ARR | Geology-focused, not spiritual. No metaphysical properties. $9.99/week (aggressive). 3.0 stars. |
| Crystal Guide (various) | 1M+ combined | Unknown | Static databases, no camera scan. Just a reference book. |

**Our edge:** No good app combines visual identification with the metaphysical/spiritual information that 80% of crystal buyers want. Rock Identifier is for geologists (Mohs hardness). Our audience wants: "This is rose quartz. It opens the heart chakra. Place it on your nightstand. Charge it under the full moon. Pair it with amethyst. Here's where to buy genuine ones."

---

### App 6: BugLens (Insect Identification)

**Name options:** BugLens, InsectID, CreepSnap, BugRadar
**Name verdict:** BugLens. Everyone says "bug" not "insect." Friendly, not scary.

**Target audience + market size:**
- Homeowners who find bugs and want to know danger level (25-65)
- Gardeners checking for beneficial vs harmful insects
- Market size: Picture Insect has 30M+ downloads. Bug identification is a real, recurring need.

**Vision API:** Gemini Flash + Roboflow insect models (validation)
- Cost: $0.01/image

**Monetization:**
- Subscription: Free (5/day) -> Pro $4.99/mo -> Premium $9.99/mo
- Affiliate: Pest control products (Raid, Ortho, diatomaceous earth, bug traps). Amazon 4-8%. Pest control services (Terminix, Orkin). CPA: $25-75.
- Estimated affiliate per user: $0.20-0.80/mo

**Revenue per user (margin):**
- Pro: $4.99 - $0.60 - $0.75 - $0.10 = **$3.54 margin (71%)**
- Premium: $9.99 - $1.25 - $1.50 - $0.10 = **$7.14 margin (71%)**
- HIGHEST margins in portfolio. Bug scanning is low-frequency (people don't scan bugs 10x/day).

**ASO keywords (100 chars):** bug identifier,insect scanner,spider id,what bug is this,pest control,cockroach id,ant identify,tick check

**Content marketing:**
- TikTok: "Scanning every bug in my house" (fear + curiosity = viral). "Is this spider dangerous?"
- Reddit: r/whatsthisbug (1.2M members), r/Entomology (137K), r/pestcontrol (61K)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| Picture Insect | 30M+ | ~$30M ARR | $19.99/year. Pushes premium aggressively before showing results. |
| Insect Identifier | 10M+ | ~$10M ARR | $9.99/week (extremely aggressive). Low accuracy. |

**Our edge:** Danger assessment + actionable removal advice. Competitors say "This is a brown recluse." We say "This is a brown recluse. DANGER: Venomous. Do not touch. Trap with a jar. If bitten, clean wound with soap, seek medical attention within 2 hours. Common in: basements, closets, woodpiles."

---

### App 7: BreedSnap (Dog Breed Identification)

**Name options:** BreedSnap, PupLens, DogID, PawScan
**Name verdict:** BreedSnap. Dog people say "breed" constantly. "What breed is that?" is the #1 question dog owners get.

**Target audience + market size:**
- Dog owners curious about their mixed-breed's heritage (65M+ US households own dogs)
- Prospective dog buyers researching breeds
- Market size: Dog Scanner app has 10M+ downloads. DNA tests (Embark, Wisdom Panel) cost $100-200. This is the free/cheap alternative.

**Vision API:** Gemini Flash. $0.01/image. Excellent at breed identification including mixed breeds.

**Monetization:**
- Subscription: Free (5/day) -> Pro $4.99/mo -> Premium $9.99/mo
- Affiliate: Embark DNA test ($139-199, 10% commission = $14-20). Dog insurance (Lemonade, Spot). Commission: $10-30/policy. Breed-specific products.
- Estimated affiliate per user: $0.50-2.00/mo (DNA test conversions are high-value)

**Revenue per user (margin):**
- Pro: $4.99 - $0.80 - $0.75 - $0.10 = **$3.34 margin (67%)**
- Premium: $9.99 - $2.00 - $1.50 - $0.10 = **$6.39 margin (64%)**

**ASO keywords (100 chars):** dog breed identifier,puppy scanner,what breed is my dog,dog breed mix,breed detector,pet identify,mutt scan

**Content marketing:**
- TikTok: "Scanning my rescue dog to find out what breed mix she is." Dog content is #1 most engaged category on TikTok.
- Reddit: r/dogs (4.5M), r/aww (35M), r/IDmydog (161K)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| Dog Scanner | 10M+ | ~$15M ARR | $6.99/mo or $29.99/year. No health info, no product recs, purely identification. |
| Google Lens | Free | Google | General purpose. Identifies breed but no health info, temperament, or care tips. |

**Our edge:** Every scan includes breed-specific health risks ("Prone to hip dysplasia"), temperament ("High energy, great with kids"), and product recommendations. Then: "Want to know for sure? Get an Embark DNA test." App is the free visual estimate, DNA test is the paid confirmation. Classic upsell funnel.

---

### App 8: StyleSnap (Outfit/Fashion Identification)

**Name options:** StyleSnap, OutfitID, FashionLens, LookFinder
**Name verdict:** StyleSnap. "Style" is insider fashion language. Amazon killed their "StyleSnap" feature (discontinued), so name is available.

**Target audience + market size:**
- Fashion-conscious shoppers (18-35, 70% female)
- Thrift shoppers trying to ID brands
- "w2c" (where to cop) culture on Reddit and TikTok
- Market size: Google Lens shopping has 12B+ visual searches/month. LTK, Lyst, ShopStyle are $100M+ businesses.

**Vision API:** Gemini Flash + Google Cloud Vision product search. $0.012/scan combined.

**Monetization:**
- Subscription: Free (5/day) -> Pro $4.99/mo -> Premium $9.99/mo
- Affiliate: Amazon Fashion, ASOS, Nordstrom, Zara, H&M. Commission: 5-15% per sale. Average order: $50-200. Every scan = affiliate link to buy.
- Estimated affiliate per user: **$2.00-8.00/mo** (fashion buyers have highest conversion from visual search)
- HIGHEST total revenue per user in portfolio when subscription + affiliate combined

**Revenue per user (margin):**
- Pro: $4.99 - $1.58 - $0.75 - $0.10 = **$2.56 margin (51%)**
- Premium: $9.99 - $3.60 - $1.50 - $0.10 = **$4.79 margin (48%)**
- Plus affiliate: +$2.00-8.00/mo = total $6.79-12.79/mo per premium user

**ASO keywords (100 chars):** outfit finder,fashion identifier,find this look,where to buy,style match,clothing scanner,brand id,w2c

**Content marketing:**
- TikTok: "Scanning celebrity outfits and finding them for under $50" (millions of views on this format already)
- Reddit: r/findfashion (172K), r/FashionReps (1.9M), r/ThriftStoreHauls (2.5M)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| Google Lens | Free | Google | Good at finding exact items. Bad at cheaper alternatives. |
| Pinterest Lens | Free | Pinterest | Pinterest-only ecosystem. |
| Amazon StyleSnap | Discontinued | N/A | Amazon killed it. Only searched Amazon catalog. |

**Our edge:** "Find this look, but cheaper." Every scan: 1) What it is (brand, style), 2) Exact match, 3) Similar at 3 price tiers (budget/mid/premium) with affiliate links. Google Lens finds the exact item. We find the $30 dupe of the $300 item.

---

### App 9: ForageLens (Mushroom/Wild Plant Identification)

**Name options:** ForageLens, ShroomScan, MushroomID, WildHarvest
**Name verdict:** ForageLens. "Forage" is the insider term. Foragers call themselves foragers. The community will recognize this.

**Vision API:** GPT-4o Vision (primary) -- DELIBERATELY using the most expensive model
- Why: Mushroom misidentification can be FATAL. Amanita phalloides (death cap) looks similar to several edible species. Accuracy is life-or-death. No cost optimization here.
- Cost: $0.02-0.03/image
- Every result: confidence level + lookalike warnings + "WHEN IN DOUBT, THROW IT OUT"

**Target audience + market size:**
- Mushroom foragers (growing rapidly, post-COVID trend)
- r/mycology has 665K members. r/foraging has 556K. Picture Mushroom has 10M+ downloads.
- Foraging grew 300% during COVID and hasn't dropped back.

**Monetization:**
- Subscription: Free (3/day, lower due to safety) -> Pro $6.99/mo -> Premium $12.99/mo (premium for safety-critical)
- Affiliate: Foraging guides, knives, baskets, dehydrators, mushroom growing kits (North Spore, 10-15%).
- Digital products: "Regional foraging guide" IAPs ($3.99 each by state/region).
- Estimated affiliate per user: $0.30-1.00/mo

**Revenue per user (margin):**
- Pro: $6.99 - $2.00 - $1.05 - $0.10 = **$3.84 margin (55%)**
- Premium: $12.99 - $5.00 - $1.95 - $0.10 = **$5.94 margin (46%)**
- Lowest margins due to expensive API. Justified by liability reduction.

**ASO keywords (100 chars):** mushroom identifier,foraging app,wild mushroom,edible plant,fungus id,mycology,shroom scanner,wild food

**Content marketing:**
- TikTok: "Found this in my backyard. Is it edible?" Foraging TikTok is massive.
- Reddit: r/mycology (665K), r/foraging (556K), r/mushroomID (88K), r/ShroomID (134K)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| Picture Mushroom | 10M+ | ~$20M ARR | $29.99/year. Sometimes confident but wrong (dangerous). |
| Shroomify | 1M+ | ~$2M ARR | Weaker AI. Good reference but slow scan. |

**Our edge:** Triple-layer safety. 1) GPT-4o identification with confidence score. 2) Automatic lookalike warnings for every edible species. 3) "Never eat based on app alone" with link to local mycological society. We never say "edible" -- we say "commonly consumed by experienced foragers" with toxic lookalike list. Marketing hook: "The mushroom app that won't get you killed."

**LEGAL:** Same approach as DermLens. Prominent disclaimers. Never claim safety.

---

### App 10: LabelLens (Supplement/Product Label Analysis)

**Name options:** LabelLens, SupplementScan, IngredientCheck, CleanLabel
**Name verdict:** LabelLens. Broader than just supplements (food labels, cosmetics, cleaning products).

**Target audience + market size:**
- Supplement users wanting ingredient verification (fitness community, 18-50)
- Health-conscious parents checking ingredients
- People with allergies
- Market size: Yuka app (ingredient scanner) has 50M+ downloads and $30M+ ARR. Think Dirty has 5M+.

**Vision API:** Google Cloud Vision OCR (text extraction) + Gemini Flash (ingredient analysis)
- OCR extracts the supplement facts panel text. Gemini analyzes for quality, dosage, interactions, alternatives.
- Cost: $0.0015 (OCR) + $0.01 (Gemini) = $0.0115/scan

**Monetization:**
- Subscription: Free (5/day) -> Pro $4.99/mo -> Premium $9.99/mo
- Affiliate: Recommend better supplement alternatives for every scan. "Your vitamin D is only 1,000 IU in a low-absorption form. Here's 5,000 IU D3+K2 in bioavailable form." Supplement commissions: 15-30% (highest in all ecommerce). Average order: $30-50.
- Brand partnerships: Supplement brands pay for "recommended alternative" placement. CPM: $20-50.
- Estimated affiliate per user: **$2.00-5.00/mo** (supplement buyers are repeat purchasers)

**Revenue per user (margin):**
- Pro: $4.99 - $0.96 - $0.75 - $0.10 = **$3.18 margin (64%)**
- Premium: $9.99 - $2.40 - $1.50 - $0.10 = **$5.99 margin (60%)**
- Plus affiliate: +$2.00-5.00/mo = total $7.99-10.99/mo per premium user

**ASO keywords (100 chars):** supplement scanner,ingredient checker,label reader,vitamin quality,protein powder review,clean label,food scan

**Content marketing:**
- @repscheme (fitness): "Scanned my preworkout. 3 ingredients are underdosed. 1 is banned in the EU. Here's what I switched to."
- TikTok: "Scanning popular supplements to see if they're actually good" (callout content goes viral)
- Reddit: r/Supplements (524K), r/Nootropics (402K), r/fitness (11.3M), r/nutrition (1.7M)

**Competitive landscape:**

| Competitor | Downloads | Revenue | Weakness |
|-----------|-----------|---------|----------|
| Yuka | 50M+ | ~$30M ARR | Scans food/cosmetics, not supplement-focused. No dosage analysis. European-made, weak on US brands. |
| Think Dirty | 5M+ | ~$5M ARR | Cosmetics only. Not supplements. Accuracy controversy. |
| Labdoor | Web + app | ~$2M ARR | Lab tests supplements (legit). No scan feature. Slow (weeks). Limited to popular brands. |

**Our edge:** No app scans a supplement label and tells you: 1) Is this dosed properly? 2) Are these forms bioavailable? 3) Interaction warnings? 4) Here are 3 better alternatives (with affiliate links). Yuka rates food. Think Dirty rates cosmetics. Labdoor tests supplements but no scanning. We're the only one doing instant AI-powered label analysis with affiliate-driven alternative recommendations.

---

## 5. Build priority matrix

Each app scored 1-10 on 5 dimensions. Total /50.

| App | Market size | API simplicity | Low competition | Affiliate potential | Content marketing fit | TOTAL | Rank |
|-----|-----------|---------------|----------------|--------------------|--------------------|-------|------|
| **LabelLens** | 8 | 8 | 9 | 10 | 10 (@repscheme) | **45** | **1** |
| **CalorieSnap** | 10 | 9 | 5 | 9 | 10 (@repscheme) | **43** | **2** |
| **CrystalLens** | 7 | 8 | 9 | 7 | 9 (@voidpilled) | **40** | **3** |
| **BreedSnap** | 9 | 9 | 6 | 8 | 6 | **38** | 4 (tie) |
| **StyleSnap** | 8 | 7 | 7 | 10 | 6 | **38** | 4 (tie) |
| **LeafLens** | 9 | 9 | 4 | 6 | 7 | **35** | 6 (tie) |
| **DermLens** | 8 | 6 | 7 | 9 | 5 | **35** | 6 (tie) |
| **TypeSnap** | 4 | 7 | 8 | 6 | 7 (@toolstwts) | **32** | 8 |
| **BugLens** | 7 | 8 | 5 | 5 | 5 | **30** | 9 |
| **ForageLens** | 6 | 5 | 6 | 5 | 7 | **29** | 10 |

### Top 3 to build first (and why)

**1. LabelLens (Supplement Scanner) -- Score: 45/50**
Highest affiliate potential in the portfolio ($2-5/user/mo from supplement recs on top of subscription). Low competition (no one does this well). Perfect fit for @repscheme audience. The fitness/supplement community is our strongest content channel. Supplement affiliate commissions (15-30%) are the highest in all of ecommerce.

**2. CalorieSnap (Meal Scanner) -- Score: 43/50**
Largest TAM ($4.4B health app market). Proven model (Cal.ai raised $1M+ at $8.33/mo hard paywall). Best natural retention (people eat 3x/day). Best unit economics (70% margin on premium). @repscheme is the perfect distribution channel.

**3. CrystalLens (Crystal ID) -- Score: 40/50**
@voidpilled is a DIRECT product-market fit. The crystal/spiritual community on TikTok is massive (30B+ views). Rock Identifier ($8M ARR) proves demand but serves geologists, not spiritual community. 80% of crystal buyers want metaphysical properties, not Mohs hardness. Blue ocean.

---

## 6. Portfolio revenue projection

### Per-app revenue waterfall (conservative)

**Month 1-3 (launch):**
- 5,000 downloads (organic ASO + content + Reddit)
- 3% Pro = 150 x $4.99 = $748/mo
- 1% Premium = 50 x $9.99 = $500/mo
- Affiliate: 200 active users x $0.50 avg = $100/mo
- **Total: ~$1,348/mo per app**

**Month 6 (growth):**
- 25,000 total downloads, 15,000 MAU
- 4% Pro = 600 x $4.99 = $2,994/mo
- 1.5% Premium = 225 x $9.99 = $2,248/mo
- Affiliate: 1,000 active users x $1.00 = $1,000/mo
- **Total: ~$6,242/mo per app**

**Month 12 (mature):**
- 100,000 total downloads, 40,000 MAU
- 4% Pro = 1,600 x $4.99 = $7,984/mo
- 2% Premium = 800 x $9.99 = $7,992/mo
- Affiliate: 5,000 active users x $1.50 = $7,500/mo
- **Total: ~$23,476/mo per app**

### Portfolio totals (10 apps)

| Timeframe | Per app avg | Portfolio total | API cost | Apple 15% | Net |
|-----------|------------|----------------|----------|-----------|-----|
| Month 3 | $1,348 | $13,480 | $3,000 | $2,022 | $8,458 |
| Month 6 | $6,242 | $62,420 | $12,000 | $9,363 | $41,057 |
| Month 12 | $23,476 | $234,760 | $50,000 | $35,214 | $149,546 |

**Bear case (50%):** $75K/mo net at month 12 = $900K ARR.
**Bull case (150%):** $225K/mo net at month 12 = $2.7M ARR.

These numbers assume content marketing drives the initial downloads. With @repscheme (fitness), @voidpilled (crystals), @toolstwts (tech), TikTok organic, and Reddit, the distribution is there.

---

## 7. Implementation timeline

### Phase 1: Template + Top 3 (Week 1)

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| Day 1 | Build shared vision-app-template | 2 | Working camera -> API -> results pipeline |
| Day 1 | Customize LabelLens | 1 | LabelLens PWA deployed to Vercel |
| Day 2 | Customize CalorieSnap | 1 | CalorieSnap PWA deployed |
| Day 2 | Customize CrystalLens | 1 | CrystalLens PWA deployed |
| Day 3 | Capacitor wrap all 3 for iOS | 2 | 3 iOS builds in TestFlight |
| Day 4 | RevenueCat + paywall for all 3 | 2 | Subscriptions working |
| Day 5 | App Store assets + submission | 2 | 3 apps submitted to Apple Review |

### Phase 2: Next 4 apps (Week 2)

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| Day 6 | BreedSnap + StyleSnap | 2 | PWA + iOS |
| Day 7 | LeafLens + BugLens | 2 | PWA + iOS |
| Day 8 | RevenueCat + assets + submit all 4 | 4 | 4 apps in Apple Review |

### Phase 3: Final 3 apps (Week 2-3)

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| Day 9 | DermLens + ForageLens + TypeSnap | 3 | PWA + iOS |
| Day 10 | RevenueCat + assets + submit all 3 | 3 | Final 3 in Apple Review |

### Phase 4: GTM (Week 3-4)

| Day | Task | Output |
|-----|------|--------|
| Day 11-14 | Content creation for all 10 apps | TikTok videos, Reddit posts, tweet threads |
| Day 15-21 | Launch on @repscheme, @voidpilled, @toolstwts | First 1,000 downloads/app |
| Day 22-30 | Iterate on paywall conversion + scan UX | Optimized flows |

**Total build: 10 working days, ~24 hours of development. 10 apps live.**

---

## 8. GTM strategy

### The "magic moment" TikTok format

Every vision app has the same viral content format: "Point camera at thing, get instant answer."

**Script template (15-60 seconds):**
```
[Camera pointing at subject]
"I found this [thing] and had no idea what it was."
[Open app, tap scan]
"Let me scan it real quick."
[Scanning animation + results appearing]
"It's a [identification]. [Interesting fact]."
[Detailed info card]
"The app even tells you [niche-specific detail]."
[Optional affiliate rec] "And apparently I should get [product]."
```

Works because: curiosity hook + instant satisfaction + unexpected detail + repeat viewability.

### Platform tactics

**TikTok:** "Scanning every [thing] in my [location]" series. "Is this [thing] dangerous?" fear hooks. Target: #PlantTok, #FoodTok, #DogTok, #CrystalTok, #ForagingTok

**Reddit (organic):** Post in niche subs with genuine value. Answer identification requests in r/whatsthisbug, r/mycology, r/IDmydog with app screenshots. Rule: provide the answer first, mention app second. Never be spammy.

**Our owned accounts:**
- @repscheme: CalorieSnap + LabelLens (fitness audience)
- @voidpilled: CrystalLens (esoteric audience, direct fit)
- @toolstwts: All apps (tech angle, "built 10 apps with one API")
- @selahmoments: LeafLens + ForageLens (nature/creation appreciation)
- @PRINTMAXXER: Meta content ("Built 10 vision AI apps. Here's revenue after 30 days.")
- @shiplog_: Build-in-public for development process

### Cross-promotion flywheel

Each app promotes others through contextual recs on result screens:
- LeafLens -> "Track your walks" -> Steplock
- CalorieSnap -> "Track your habits" -> Streakr
- BreedSnap -> "Walk your dog" -> Steplock
- CrystalLens -> "Meditate with your crystals" -> PrayerLock
- LabelLens -> "Track your supplement routine" -> Streakr
- ForageLens -> "Identify plants too" -> LeafLens

One download leads to 2-3 more. Every app result screen has a small "From the makers of..." section.

---

## 9. Color schemes per app

| App | Primary | Secondary | Accent | Background | Emotion |
|-----|---------|-----------|--------|------------|---------|
| LeafLens | #16a34a (green) | #166534 (dark green) | #fbbf24 (amber) | #f0fdf4 (mint) | Natural, alive |
| CalorieSnap | #2563eb (blue) | #1e40af (navy) | #22c55e (green) | #eff6ff (light blue) | Clean, scientific |
| DermLens | #ec4899 (pink) | #9d174d (rose) | #f9a8d4 (light pink) | #fdf2f8 (blush) | Gentle, clinical |
| TypeSnap | #0f172a (slate) | #334155 (gray) | #f59e0b (amber) | #f8fafc (white) | Professional, precise |
| CrystalLens | #7c3aed (purple) | #4c1d95 (deep purple) | #c4b5fd (lavender) | #f5f3ff (light purple) | Mystical, spiritual |
| BugLens | #ea580c (orange) | #9a3412 (dark orange) | #fbbf24 (amber) | #fff7ed (warm) | Alert, outdoorsy |
| BreedSnap | #b45309 (warm brown) | #78350f (dark brown) | #3b82f6 (blue) | #fefce8 (warm white) | Warm, friendly |
| StyleSnap | #000000 (black) | #18181b (near black) | #f43f5e (coral) | #fafafa (white) | Fashion-forward, bold |
| ForageLens | #065f46 (forest) | #064e3b (dark forest) | #fbbf24 (amber) | #ecfdf5 (mint) | Earthy, cautious |
| LabelLens | #0d9488 (teal) | #0f766e (dark teal) | #f59e0b (amber) | #f0fdfa (light teal) | Scientific, trustworthy |

---

## 10. Legal and compliance

### Health/safety disclaimers (mandatory for DermLens, ForageLens, CalorieSnap)

Every health-adjacent app MUST include on every result screen, onboarding, and App Store description:

```
DISCLAIMER: This app provides informational content only and is not a substitute
for professional medical advice, diagnosis, or treatment. Always consult a
qualified healthcare provider. Results are AI-generated estimates and may not
be accurate. Never eat wild mushrooms based solely on app identification.
Never delay seeking medical attention based on app results.
```

### Apple App Store review

- Health apps get extra scrutiny. DermLens and ForageLens may need Apple's health team.
- Never use "diagnose" in any app. Use "analyze," "identify," "suggest."
- Calorie estimates must say "estimated."
- Camera permission needs clear Info.plist usage description.
- Privacy nutrition label must reflect image data sent to APIs.
- Run RevylAI Greenlight before submission (see APP_QUALITY_STANDARDS.md Gate 2/3).

### API data privacy

- Images sent to Gemini/GPT-4o are subject to provider data policies.
- Privacy policy must disclose third-party AI processing.
- Offer on-device option (TF.js) for premium users who want privacy.
- Never store user images on our servers. API call is stateless.
- IndexedDB history stores results text only, not original images (unless user opts in).

### Affiliate disclosure (FTC)

- Every result screen with affiliate links: "We may earn a commission from links on this page."
- Disclosure ABOVE affiliate links, not below.
- #ad or "Sponsored" on any social content promoting affiliate products.

---

## 11. API key management and cost control

### Rate limits per tier

| Tier | Scans/day | Monthly cap | Cost cap/user |
|------|-----------|-------------|---------------|
| Free | 5 | 150 | $1.50 |
| Pro | 50 | 1,500 | $15.00 |
| Premium | 200 | 6,000 | $60.00 |

### Cost control

1. Image compression: 640x480 JPEG quality 80%. 90% smaller payload.
2. Response caching: IndexedDB keyed by perceptual image hash. Same plant = cached result.
3. Tiered API routing: TF.js pre-classification. If confidence > 90%, skip cloud API.
4. API key rotation: Separate keys per app for billing visibility. Budget alerts at $100/day.
5. Abuse detection: Flag >100 scans/day. Block repeated same-image scanning.

---

## 12. Metrics to track per app

**Acquisition:** Downloads (daily), install source, ASO keyword rankings (weekly), content marketing attribution.

**Engagement:** Scans/user/day (target: 3-5), scan completion rate, result interaction rate (affiliate clicks, shares, saves), D1/D7/D30 retention (target: 40%/20%/10%).

**Monetization:** Free-to-paid conversion (target: 3-5%), paywall view-to-subscribe (target: 15-25%), monthly churn (target: <8%), ARPU including affiliate, LTV (target: >$20), affiliate CTR (target: >5%), affiliate conversion (target: >2%).

**Technical:** API response time (target: <2s cloud, <500ms on-device), API error rate (target: <1%), identification accuracy (sample 100/week, score manually), crash rate (target: <0.5%).

---

## 13. Infrastructure

### Backend (minimal)

Vision apps are client-side PWAs. Only backend needed:

1. **API proxy** (Cloudflare Worker) -- hides API keys from client. Free tier: 100K requests/day.
2. **User auth** (Supabase) -- anonymous ID or email. Free tier: 50K MAU.
3. **Scan counter** (Supabase or Redis) -- server-side rate limiting.
4. **Analytics** (PostHog) -- event tracking. Free tier: 1M events/mo.
5. **Affiliate redirect** (Cloudflare Worker) -- tracks clicks, redirects.

**Total infra cost: $0-20/mo on free tiers.**

### Deployment

- PWA: Vercel (free, auto-deploy from git)
- iOS: Capacitor -> Xcode -> App Store Connect
- API proxy: Cloudflare Workers (global edge, free)

### RevenueCat

One account, separate apps. Shared entitlements: `vision_pro`, `vision_premium`. Per-app products: `com.leaflens.pro.monthly`, `com.calorienap.pro.monthly`, etc.

---

## 14. Template location

Working PWA template: `ralph/loops/app_factory/output/vision-app-template/`

Files:
- `index.html` -- camera UI with viewfinder, settings, history, paywall modal
- `app.js` -- camera, API integration (gemini/openai/google vision), niche presets, scan history, soft paywall
- `styles.css` -- responsive, CSS custom properties for reskinning
- `manifest.json` -- PWA manifest
- `sw.js` -- service worker for offline shell caching
- `config-presets/presets.json` -- all 10 niches with colors, pricing, ASO keywords, affiliate config

---

## Key insight

The vision API is the commodity. The niche UX is the moat. Nobody downloads "google vision API wrapper." They download "plant identifier" or "calorie scanner" or "supplement checker." Same API, different packaging, different audience, different willingness to pay.

10 apps x $6K avg MRR at month 6 = $60K/mo from one template and one API key.

---

## Quick start

Build LabelLens first:
1. Clone vision-app-template
2. Set config.js: Gemini key, OCR + analysis dual-API, teal theme, supplement prompt
3. Deploy to Vercel: `vercel deploy --prod`
4. Test 10 supplement label scans, iterate prompt until JSON output is consistent
5. Add RevenueCat: `npm install @revenuecat/purchases-capacitor`
6. Wrap in Capacitor: `npx cap add ios && npx cap open ios`
7. Submit to App Store with assets from APP_ASSET_GENERATION_PROMPTS.md pattern
8. Post launch content on @repscheme: "Scanned my pre-workout. Here's what I found."
9. Post on Reddit: r/Supplements, r/Nootropics, r/fitness
10. Monitor: scan completion rate, paywall conversion, affiliate CTR

---

## References

- [Google Cloud Vision API pricing](https://cloud.google.com/vision/pricing) -- $1.50/1K images
- [Gemini API pricing](https://ai.google.dev/pricing) -- Flash: ~$0.01/image for vision
- [OpenAI Vision pricing](https://openai.com/api/pricing/) -- GPT-4o: $0.01-0.03/image
- [Clarifai pricing](https://www.clarifai.com/pricing) -- Free tier 1K ops/mo
- [TensorFlow.js models](https://www.tensorflow.org/js/models) -- MobileNet, COCO-SSD (free)
- [Apple Vision Framework](https://developer.apple.com/documentation/vision) -- On-device, free
- [PlantNet](https://plantnet.org/) -- 50M+ downloads
- [Cal.ai](https://cal.ai/) -- Hard paywall $8.33/mo, $2M+ ARR
- [Picture Insect](https://apps.apple.com/app/id1461694973) -- 30M+ downloads
- [Yuka](https://yuka.io/) -- 50M+ downloads, $30M+ ARR
- [SkinVision](https://www.skinvision.com/) -- 2M+ downloads
- [Dog Scanner](https://play.google.com/store/apps/details?id=com.siwalusoftware.dogscanner) -- 10M+ downloads
- [Picture Mushroom](https://apps.apple.com/app/id1474578078) -- 10M+ downloads, ~$20M ARR
- [RevenueCat State of Subscription Apps 2025](https://www.revenuecat.com/state-of-subscription-apps-2025/)
- APP_QUALITY_STANDARDS.md -- PRINTMAXX app quality requirements
- IOS_REJECTION_PREVENTION.md -- Apple rejection avoidance
- IOS_SUBMISSION_PROCESS.md -- Step-by-step submission checklist
- AGGREGATE_DESIGN_SYSTEM.md -- Color palettes, typography, spacing
