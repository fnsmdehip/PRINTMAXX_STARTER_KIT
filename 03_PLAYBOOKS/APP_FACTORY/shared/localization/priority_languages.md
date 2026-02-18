# Priority Languages for App Localization

Analysis of target languages for app localization, ranked by market size, revenue potential, and ROI.

## Executive summary

**Tier 1 (highest ROI):** Spanish, Portuguese, French, German

These four languages cover 80%+ of non-English app revenue opportunity with manageable translation costs.

## Tier 1: Priority languages

### Spanish (es)

| Metric | Value |
|--------|-------|
| Native speakers | 475M |
| App Store countries | Spain, Mexico, Argentina, Colombia, Chile, Peru, + 15 others |
| iOS revenue share | ~8% of global (ex-US) |
| Android revenue share | ~12% of global (ex-US) |
| Translation cost (est.) | $150-400 per 3,000 words |
| Localization complexity | Low |

**Why prioritize:**
- Single translation covers 20+ countries
- Strong in-app purchase conversion in Spain and Mexico
- Growing premium app adoption in Latin America
- Cultural familiarity with US apps

**Regional considerations:**
- Use "neutral" Spanish (avoid heavy regional slang)
- Currency: EUR (Spain), MXN, ARS, COP
- Date format: DD/MM/YYYY

### Portuguese (pt)

| Metric | Value |
|--------|-------|
| Native speakers | 250M |
| App Store countries | Brazil, Portugal |
| iOS revenue share | ~4% of global (ex-US) |
| Android revenue share | ~8% of global (ex-US) |
| Translation cost (est.) | $150-400 per 3,000 words |
| Localization complexity | Low-Medium |

**Why prioritize:**
- Brazil is 6th largest app market globally
- High smartphone penetration (85%+)
- Growing middle class with disposable income
- Android-dominant (ideal for subscription apps)

**Regional considerations:**
- Use Brazilian Portuguese (pt-BR), not European
- Currency: BRL
- Local payment methods matter (Pix, boleto)

### French (fr)

| Metric | Value |
|--------|-------|
| Native speakers | 280M |
| App Store countries | France, Belgium, Switzerland, Canada (Quebec), African markets |
| iOS revenue share | ~5% of global (ex-US) |
| Android revenue share | ~4% of global (ex-US) |
| Translation cost (est.) | $180-450 per 3,000 words |
| Localization complexity | Medium |

**Why prioritize:**
- France is 5th largest app market
- High ARPU (average revenue per user)
- Strong subscription culture
- Growing African mobile markets

**Regional considerations:**
- France French is standard (works for Quebec with minor adjustments)
- Currency: EUR (France), CHF (Switzerland), CAD (Canada)
- GDPR compliance required for EU

### German (de)

| Metric | Value |
|--------|-------|
| Native speakers | 100M |
| App Store countries | Germany, Austria, Switzerland |
| iOS revenue share | ~6% of global (ex-US) |
| Android revenue share | ~5% of global (ex-US) |
| Translation cost (est.) | $180-500 per 3,000 words |
| Localization complexity | Medium |

**Why prioritize:**
- Germany is 4th largest app market
- Highest willingness to pay in Europe
- Strong subscription economy
- Quality-conscious users (good reviews if app is good)

**Regional considerations:**
- Formal tone preferred ("Sie" not "du")
- Currency: EUR (Germany/Austria), CHF (Switzerland)
- Strict data privacy expectations
- Longer words = UI spacing issues

## Tier 2: Secondary priority

### Japanese (ja)

| Metric | Value |
|--------|-------|
| Native speakers | 125M |
| iOS revenue share | ~15% of global (ex-US) |
| Translation cost (est.) | $300-800 per 3,000 words |
| Localization complexity | High |

**Why consider:**
- 3rd largest app market
- Extremely high ARPU
- iOS-dominant market

**Why deprioritize for MVP:**
- High translation cost
- Requires cultural adaptation (not just translation)
- Different UX expectations
- Requires dedicated support

### Korean (ko)

| Metric | Value |
|--------|-------|
| Native speakers | 80M |
| iOS revenue share | ~6% of global (ex-US) |
| Translation cost (est.) | $250-600 per 3,000 words |
| Localization complexity | High |

**Why consider:**
- High in-app purchase rates
- Tech-savvy users
- Strong gaming/utility app market

### Italian (it)

| Metric | Value |
|--------|-------|
| Native speakers | 65M |
| iOS revenue share | ~3% of global (ex-US) |
| Translation cost (est.) | $150-400 per 3,000 words |
| Localization complexity | Low |

**Why consider:**
- Easy translation from Spanish/French base
- Growing premium app market
- Part of EU (GDPR covered)

## Tier 3: Future consideration

| Language | Speakers | Market potential | Complexity | Notes |
|----------|----------|-----------------|------------|-------|
| Chinese (zh) | 1.3B | Huge but requires Alibaba/Tencent partnership | Very High | Different app stores, regulations |
| Russian (ru) | 250M | Medium | Medium | Payment processing challenges |
| Hindi (in) | 600M | Growing | Medium | Low ARPU currently |
| Arabic (ar) | 350M | Medium | High | RTL layout required |
| Dutch (nl) | 25M | Small but high ARPU | Low | Consider if German performs well |
| Polish (pl) | 40M | Medium | Medium | Growing tech adoption |
| Turkish (tr) | 80M | Medium | Medium | Currency volatility |

## Cost analysis

### Estimated translation costs (full app)

Based on ~3,000 words for a typical utility/productivity app:

| Language | Budget Option | Premium Option | Recommended |
|----------|--------------|----------------|-------------|
| Spanish | $150 | $360 | Budget + native review |
| Portuguese | $150 | $360 | Budget + native review |
| French | $180 | $450 | Budget + native review |
| German | $180 | $500 | Premium (quality matters) |

### Total Tier 1 investment

- Budget path: $660 total
- Premium path: $1,670 total
- Recommended (mixed): ~$900 total

### Translation services

**Budget ($0.05-0.08/word):**
- Gengo
- OneSky
- Crowdin marketplace

**Mid-range ($0.08-0.12/word):**
- Lokalise
- Phrase
- TextMaster

**Premium ($0.12-0.20/word):**
- Professional agencies
- Smartling
- TransPerfect

**AI + Human review ($0.03-0.05/word):**
- DeepL Pro + native speaker review
- Best ROI for Tier 1 languages

## Revenue potential

### Conservative estimates (monthly, per language)

Assuming 10K downloads/month, 2% conversion, $5 ARPU:

| Language | Monthly users | Revenue potential |
|----------|--------------|-------------------|
| Spanish | 10,000 | $1,000 |
| Portuguese | 8,000 | $800 |
| French | 6,000 | $600 |
| German | 5,000 | $500 |
| **Total** | **29,000** | **$2,900** |

### ROI timeline

- Translation investment: ~$900
- Monthly revenue increase: $2,900
- Payback period: <1 month

This is conservative. Apps with good ASO see 3-5x these numbers.

## Localization checklist by language

### Spanish
- [ ] Translate all JSON namespaces
- [ ] Review by native speaker (prefer neutral accent)
- [ ] Test plural forms (same as English)
- [ ] Localize App Store metadata
- [ ] Generate localized screenshots
- [ ] Test date/currency formatting

### Portuguese
- [ ] Use Brazilian Portuguese (pt-BR)
- [ ] Translate all JSON namespaces
- [ ] Review by Brazilian native speaker
- [ ] Consider Pix payment mentions if applicable
- [ ] Localize App Store metadata
- [ ] Generate localized screenshots

### French
- [ ] Translate all JSON namespaces
- [ ] Review by native speaker
- [ ] Check formal/informal tone consistency
- [ ] Test longer text in UI (French expands ~20%)
- [ ] Localize App Store metadata
- [ ] GDPR compliance check

### German
- [ ] Translate all JSON namespaces
- [ ] Premium translation recommended
- [ ] Use formal tone (Sie form)
- [ ] Test compound words in UI
- [ ] Localize App Store metadata
- [ ] Generate localized screenshots
- [ ] Legal text review (Germans are precise)

## Launch sequence

**Week 1-2:** Spanish
- Largest market, easiest translation
- Test localization infrastructure

**Week 3-4:** Portuguese
- Similar process, different market
- Learn from Spanish launch

**Week 5-6:** French + German
- Can be done in parallel
- More complex, higher ARPU

**Week 7+:** Monitor and optimize
- Track revenue by language
- A/B test paywall copy per language
- Collect user feedback

## Metrics to track

Post-launch, track these per language:

1. **Downloads/installs** - Is ASO working?
2. **Conversion rate** - Does paywall translate well?
3. **ARPU** - Revenue per user by language
4. **Retention D1/D7/D30** - Is UX culturally appropriate?
5. **Reviews** - Quality of translation feedback
6. **Support tickets** - Language-specific issues

## Key takeaways

1. Start with Spanish and Portuguese. Together they cover massive markets with low complexity.

2. Add French and German to capture premium European users.

3. Use AI translation + human review for best ROI.

4. Tier 1 languages can add 30-50% revenue at <$1K investment.

5. Track metrics per language to inform future localization decisions.

6. Don't over-localize. Neutral, clear language beats regional slang.
