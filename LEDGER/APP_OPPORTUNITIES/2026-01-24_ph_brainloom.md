# BrainLoom - PDF to Flashcards Learning OS

**Source:** Product Hunt
**URL:** https://www.producthunt.com/posts/brainloom
**Date Found:** 2026-01-24
**Upvotes:** 157+ (Day Rank #2)

---

## What It Does

Local-first Learning OS that:
- Turns PDF highlights into flashcards instantly
- Keeps flashcards linked to source text for deep context
- Infinite Canvas for visual idea structuring
- "Smart Paste" for mouse-free organization
- Currently Windows v1.0 (Mac coming)

**Pricing:** $29 Lifetime License (first 150 users)

---

## Clone Difficulty

**Rating:** MEDIUM

**Why:**
- PDF parsing requires native capabilities
- Spaced repetition algorithm (well-documented)
- Infinite canvas is complex but doable
- Cross-device sync adds complexity

**Tech Stack Estimate:**
- React Native with PDF.js or native PDF kit
- SQLite for local-first storage
- Spaced repetition: SM-2 algorithm (open source)
- Canvas: react-native-canvas or custom view

**Existing Open Source:**
- Anki (spaced repetition, GPL - can study but not fork)
- Logseq (local-first, AGPL)
- Obsidian plugins (various licenses)

---

## Niche Angles

| Niche | App Name Ideas | Unique Hook |
|-------|---------------|-------------|
| **Faith** | BibleCards, ScriptureLoop | PDF Bible study notes to memory verses, sermon notes to flashcards |
| **Med Students** | MedCards, AnatomyLoop | Textbook PDFs to USMLE-style flashcards, image-based cards |
| **Law Students** | CaseBrief Cards, BarPrep | Case PDFs to legal flashcards, statute memorization |
| **Language Learners** | VocabPDF, LanguageLoop | PDF ebooks to vocabulary cards with context sentences |
| **Nursing** | NurseCards, NCLEXPrep | Nursing textbooks to exam prep flashcards |
| **Real Estate** | RECards, LicensePrep | Study materials to real estate exam prep |

---

## Monetization Model

**Primary:** Subscription + Lifetime Option
- Free: 50 flashcards, 1 PDF import/month
- Pro ($6.99/mo or $49 lifetime): Unlimited cards, cloud sync
- Student ($3.99/mo): Verified .edu discount

**Secondary:**
- Premium AI features (auto-generate cards from highlights)
- Deck marketplace (user-created decks)
- Affiliate links to textbooks/courses

---

## Competitive Landscape

- **Anki** (free, complex UI, desktop-first)
- **Quizlet** (established, general purpose)
- **RemNote** (PDF + spaced repetition, complex)
- **Obsidian** (not flashcard focused)

**Differentiation opportunity:** Mobile-first, niche-specific (e.g., "The Anki for Bible Study" or "The Anki for Med School")

---

## Implementation Priority

**Score:** 7/10

**Reasons:**
- Medium complexity (4-6 week MVP)
- Strong niche potential (med/law/nursing students spend heavily)
- Proven market (Anki, Quizlet both successful)
- PDF parsing is the main technical challenge
- High retention (daily use for studying)

---

## Next Steps

1. Research PDF parsing libraries for React Native
2. Choose one niche (recommend: Med Students or Faith - high willingness to pay)
3. Build MVP with basic PDF highlight to flashcard
4. Add spaced repetition as core feature
5. Infinite canvas can be v2.0
