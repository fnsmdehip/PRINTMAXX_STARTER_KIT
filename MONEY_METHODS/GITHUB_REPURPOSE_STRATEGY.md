# GitHub Repo Repurposing Strategy

**Created:** 2026-02-10
**Purpose:** Systematic approach to finding, vetting, splicing, and shipping open source code across every PRINTMAXX money method.
**Tracker:** `LEDGER/GITHUB_REPURPOSE_TRACKER.csv`

---

## 1. Philosophy: Smart Splicing, Not Copying

never ship a raw fork. ever.

the move is surgical extraction. you take the BEST pieces from multiple repos, splice them with your custom business logic, and ship something that's 10x faster than building from scratch but 100% yours.

this is how real engineering teams at Stripe, Vercel, and every YC company operate. nobody writes auth from scratch. nobody builds a CSV parser from zero. they stand on shoulders of giants and focus their time on the thing that actually makes money: the custom business logic, the monetization layer, the niche-specific UX.

**the formula:**
```
auth from Repo A + UI from Repo B + payments from Repo C + YOUR business logic = your product
```

**what you build custom (always):**
- monetization / paywall / pricing logic
- branding / design system / visual identity
- domain-specific business rules
- content and copy
- analytics and tracking
- the "secret sauce" that makes your version better for your niche

**what you take from repos (save 10-100 hours per project):**
- auth flows (OAuth, magic link, session management)
- CRUD boilerplate
- API integrations (Stripe, Twilio, SendGrid, etc.)
- parsing logic (scrapers, data transformers)
- UI component patterns
- rate limiting, caching, queue management
- deployment configs (Docker, Vercel, Railway)

be smart and strategic. big brain. the goal is speed-to-revenue, not ego about writing every line yourself.

---

## 2. Security Protocol (NON-NEGOTIABLE)

before using ANY code from a GitHub repo, run this checklist. no exceptions. one malicious dependency can leak your API keys, exfiltrate customer data, or crypto-mine on your server.

### Automated Checks (Run Every Time)

```
[ ] LICENSE FILE EXISTS and is MIT / Apache 2.0 / BSD / ISC
    - never GPL/AGPL for commercial use (your code becomes open source)
    - never SSPL (MongoDB-style trap)
    - if no license file exists: treat as ALL RIGHTS RESERVED, do not use

[ ] DEPENDENCY AUDIT CLEAN
    - npm: npm audit
    - Python: pip-audit or safety check
    - Rust: cargo audit
    - Go: govulncheck
    - zero critical/high vulnerabilities, or you patch them before using

[ ] NO HARDCODED URLS TO UNKNOWN DOMAINS
    - grep -r "http://" src/ --include="*.js" --include="*.ts" --include="*.py"
    - grep -r "https://" src/ --include="*.js" --include="*.ts" --include="*.py"
    - every URL should point to a known service (github.com, api.stripe.com, etc.)
    - unknown domains = instant red flag

[ ] NO DANGEROUS DYNAMIC EXECUTION
    - grep -r "eval(" src/
    - grep -r "exec(" src/
    - grep -r "Function(" src/
    - grep -r "child_process" src/
    - grep -r "subprocess" src/
    - any of these with dynamic/user input = reject or rewrite

[ ] NO OBFUSCATED CODE
    - grep -r "atob\|btoa\|Buffer.from" src/ (base64)
    - grep -r "\\\\x[0-9a-f]" src/ (hex encoded)
    - grep -r "String.fromCharCode" src/
    - if source code is minified in non-build directories = reject

[ ] NO SUSPICIOUS PACKAGE SCRIPTS
    - check package.json for "preinstall", "postinstall", "prepare" scripts
    - if postinstall curls/wgets anything = instant reject
    - if postinstall runs anything beyond standard build steps = investigate

[ ] NO UNAUTHORIZED TELEMETRY
    - grep -r "analytics\|telemetry\|tracking\|sentry\|mixpanel\|amplitude" src/
    - any data being sent to third parties without explicit opt-in = strip it out

[ ] GITHUB ISSUES CHECK
    - search issues for "security", "vulnerability", "CVE", "malicious"
    - check if maintainer responds to security reports

[ ] MAINTENANCE STATUS
    - last commit < 6 months ago (actively maintained)
    - if abandoned but code is solid: fork and maintain yourself
    - stars > 50 minimum (community vetted)
    - check if it's a single anonymous contributor with no history
```

### Manual Review (For Core Dependencies)

when you're going to heavily depend on a repo (auth, payments, data pipeline), do a manual code review:

```
[ ] READ CORE SOURCE FILES (not just the README)
    - actually open the main entry points and read them
    - understand the data flow

[ ] CHECK ALL NETWORK CALLS
    - every fetch(), axios.get(), requests.get(), http.get()
    - where is data going? what's being sent?

[ ] VERIFY NO DATA EXFILTRATION IN ERROR HANDLERS
    - error handlers that POST to external URLs = red flag
    - catch blocks that send stack traces to unknown endpoints = red flag

[ ] CHECK ENVIRONMENT VARIABLE USAGE
    - are they reading env vars they shouldn't need?
    - is the .env.example asking for keys unrelated to the project?

[ ] REVIEW TEST FILES FOR HIDDEN FUNCTIONALITY
    - test files can contain code that runs during CI/CD
    - check for side effects in test setup/teardown

[ ] CHECK CONTRIBUTOR LIST
    - single anonymous person with no other repos = higher risk
    - known open source contributors = lower risk
    - org-backed repos (vercel, stripe, supabase) = lowest risk
```

### Red Flags (INSTANT REJECT)

do not use repos that exhibit any of these:

- repo asks for API keys but doesn't need them for its stated purpose
- postinstall scripts that curl/wget external resources
- minified source code in a non-build directory
- dependencies with typosquatting names (e.g., "lodassh" instead of "lodash", "crross-env" instead of "cross-env")
- suspiciously recent repos with very high stars (possible star farming - check star history on star-history.com)
- repo has open security issues that maintainer ignores
- source contains IP addresses or raw domain connections to non-standard services
- package has been deprecated with a warning but no alternative specified

### Quick Security Scan Script

save this and run against any repo before extracting code:

```bash
#!/bin/bash
# github_repo_security_scan.sh
# Usage: ./github_repo_security_scan.sh /path/to/cloned/repo

REPO_DIR="$1"

if [ -z "$REPO_DIR" ]; then
  echo "Usage: $0 /path/to/repo"
  exit 1
fi

echo "=== PRINTMAXX REPO SECURITY SCAN ==="
echo "Scanning: $REPO_DIR"
echo ""

# 1. License check
echo "--- LICENSE CHECK ---"
if [ -f "$REPO_DIR/LICENSE" ] || [ -f "$REPO_DIR/LICENSE.md" ] || [ -f "$REPO_DIR/LICENSE.txt" ]; then
  echo "License file found:"
  head -5 "$REPO_DIR/LICENSE"* 2>/dev/null
else
  echo "WARNING: No license file found. Treat as ALL RIGHTS RESERVED."
fi
echo ""

# 2. Dangerous patterns
echo "--- DANGEROUS PATTERNS ---"
echo "eval() calls:"
grep -rn "eval(" "$REPO_DIR/src" "$REPO_DIR/lib" "$REPO_DIR/app" 2>/dev/null | grep -v node_modules | grep -v ".min." | head -10
echo "exec() calls:"
grep -rn "exec(" "$REPO_DIR/src" "$REPO_DIR/lib" "$REPO_DIR/app" 2>/dev/null | grep -v node_modules | head -10
echo "Function() constructor:"
grep -rn "new Function(" "$REPO_DIR/src" "$REPO_DIR/lib" "$REPO_DIR/app" 2>/dev/null | grep -v node_modules | head -10
echo ""

# 3. Network calls to unknown domains
echo "--- EXTERNAL URLS ---"
grep -rn "https\?://" "$REPO_DIR/src" "$REPO_DIR/lib" "$REPO_DIR/app" 2>/dev/null | grep -v node_modules | grep -v "github.com\|npmjs.com\|googleapis.com\|stripe.com\|localhost\|127.0.0.1\|example.com" | head -20
echo ""

# 4. Base64/obfuscated code
echo "--- OBFUSCATION CHECK ---"
echo "Base64 patterns:"
grep -rn "atob\|btoa\|Buffer.from" "$REPO_DIR/src" "$REPO_DIR/lib" "$REPO_DIR/app" 2>/dev/null | grep -v node_modules | head -10
echo "Hex encoded:"
grep -rn "\\\\x[0-9a-f]" "$REPO_DIR/src" "$REPO_DIR/lib" "$REPO_DIR/app" 2>/dev/null | grep -v node_modules | head -10
echo ""

# 5. Suspicious package.json scripts
echo "--- PACKAGE.JSON SCRIPTS ---"
if [ -f "$REPO_DIR/package.json" ]; then
  python3 -c "
import json
with open('$REPO_DIR/package.json') as f:
    pkg = json.load(f)
scripts = pkg.get('scripts', {})
suspicious = ['preinstall', 'postinstall', 'prepare']
for s in suspicious:
    if s in scripts:
        print(f'WARNING: {s}: {scripts[s]}')
if not any(s in scripts for s in suspicious):
    print('No suspicious install scripts found.')
" 2>/dev/null || echo "Could not parse package.json"
fi
echo ""

# 6. Dependency count
echo "--- DEPENDENCY COUNT ---"
if [ -f "$REPO_DIR/package.json" ]; then
  python3 -c "
import json
with open('$REPO_DIR/package.json') as f:
    pkg = json.load(f)
deps = len(pkg.get('dependencies', {}))
dev_deps = len(pkg.get('devDependencies', {}))
print(f'Dependencies: {deps}, DevDependencies: {dev_deps}')
if deps > 50:
    print('WARNING: High dependency count. More attack surface.')
" 2>/dev/null
fi
if [ -f "$REPO_DIR/requirements.txt" ]; then
  count=$(wc -l < "$REPO_DIR/requirements.txt")
  echo "Python requirements: $count packages"
fi
echo ""

echo "=== SCAN COMPLETE ==="
echo "Review findings above. If any WARNING items, investigate before using."
```

---

## 3. Repurposing Categories and Strategy

### A. App Templates and Starters

what to take: auth flow, navigation structure, design system boilerplate, deployment config.
what to build custom: business logic, branding, monetization, niche-specific content, paywall.

**search queries:**
```
"{niche} app template" license:mit stars:>100
"react native starter" license:mit stars:>500
"expo template" license:mit stars:>200
"pwa template" license:mit stars:>100
"nextjs saas starter" license:mit stars:>300
"nextjs boilerplate" license:mit stars:>500
"t3 stack template" license:mit
"supabase starter" license:mit stars:>200
"firebase template react" license:mit stars:>100
"tailwind dashboard template" license:mit stars:>200
"prayer app" license:mit
"fitness tracker react native" license:mit
"habit tracker" license:mit stars:>50
"pomodoro timer" license:mit stars:>100
"meditation app" license:mit
"ramadan" license:mit
"islamic app" license:mit
"todo app react native" license:mit stars:>200
"subscription app template" license:mit
"revenueCat example" license:mit
```

**splice strategy:**
1. find 2-3 starter repos in your niche
2. extract auth flow from the one with best OAuth implementation
3. extract navigation/routing from the one with cleanest UX
4. extract UI components from the one with best design
5. wire them together with your custom business logic
6. add RevenueCat for monetization, your branding, your content

**example combo for a faith app:**
- auth: supabase starter (magic link + Google OAuth)
- UI: shadcn/ui components + tailwind
- prayer times: aladhan API integration from an Islamic app repo
- custom: gamification, streaks, community features, paywall

### B. Scrapers and Data Collection

what to take: parsing logic, anti-detection patterns, rate limiting, proxy rotation.
what to build custom: target-specific selectors, data pipeline, output format, integration with your LEDGER.

**search queries:**
```
"google maps scraper" license:mit stars:>100
"yelp scraper" license:mit
"linkedin scraper" license:mit stars:>50
"twitter scraper" license:mit stars:>200
"instagram scraper" license:mit stars:>100
"tiktok scraper" license:mit stars:>100
"web scraper python" license:mit stars:>500
"selenium scraper" license:mit
"playwright scraper" license:mit stars:>100
"puppeteer scraper" license:mit stars:>200
"beautiful soup scraper" license:mit
"amazon product scraper" license:mit
"price tracker" license:mit stars:>100
"job scraper" license:mit
"real estate scraper" license:mit
"reddit scraper" license:mit stars:>100
"product hunt scraper" license:mit
"craigslist scraper" license:mit
"facebook marketplace scraper" license:mit
"email finder" license:mit stars:>50
"lead generation scraper" license:mit
```

**splice strategy:**
1. find scrapers that already hit your target platform
2. extract the parsing/selector logic (CSS selectors, XPath, regex patterns)
3. extract anti-detection code (user agent rotation, delays, fingerprint spoofing)
4. wrap in your own pipeline: scrape -> clean -> dedupe -> output to LEDGER CSV
5. add your own rate limiting, proxy integration (SOAX), error handling

**critical: scraper repos go stale fast.** website structures change. always verify selectors work before depending on them. extract the PATTERNS, not just the selectors.

### C. Automation and Scheduling

what to take: queue management, scheduling logic, API integrations, retry patterns.
what to build custom: content strategy, timing optimization, analytics, niche-specific rules.

**search queries:**
```
"social media scheduler" license:mit stars:>100
"twitter bot" license:mit stars:>200
"email automation" license:mit stars:>100
"cron job manager" license:mit stars:>200
"task queue" license:mit stars:>500
"bullmq" license:mit
"content scheduler" license:mit
"auto poster" license:mit
"social media manager" license:mit stars:>100
"rss to social" license:mit
"buffer alternative" license:mit
"n8n" license:mit (careful - check specific license)
"zapier alternative" license:mit
"workflow automation" license:mit stars:>200
"telegram bot" license:mit stars:>500
"discord bot" license:mit stars:>500
"slack bot" license:mit stars:>200
"webhook handler" license:mit
"notification service" license:mit
```

**splice strategy:**
1. take queue/scheduling infrastructure from battle-tested repos (BullMQ, Agenda, etc.)
2. take API integration boilerplate for your target platforms
3. build custom: your content strategy, your posting schedule, your analytics
4. add monitoring: know when posts fail, when queues back up, when rate limits hit

### D. AI/ML Tools

what to take: model serving patterns, preprocessing pipelines, embedding generation.
what to build custom: fine-tuning for your niche, custom prompts, UI, monetization.

**search queries:**
```
"openai api wrapper" license:mit stars:>200
"langchain" license:mit stars:>500
"llm wrapper" license:mit stars:>100
"image generation api" license:mit stars:>100
"stable diffusion api" license:mit
"text to speech" license:mit stars:>200
"speech to text" license:mit stars:>200
"whisper api" license:mit
"rag chatbot" license:mit stars:>100
"vector database" license:mit
"ai chatbot" license:mit stars:>300
"recommendation engine" license:mit stars:>100
"sentiment analysis" license:mit stars:>200
"text classification" license:mit stars:>200
"ocr" license:mit stars:>500
"computer vision" license:mit stars:>200
"face detection" license:mit stars:>100
"ai image upscaler" license:mit
"ai background remover" license:mit
"comfyui workflow" license:mit
```

**splice strategy:**
1. use established wrappers for API calls (don't reinvent HTTP calls to OpenAI)
2. take preprocessing pipelines (tokenization, chunking, embedding)
3. take RAG patterns from well-tested repos
4. build custom: your prompts, your fine-tuning data, your UI, your monetization
5. the AI model is a commodity. the niche-specific application is the product.

### E. Marketing and Growth

what to take: analysis frameworks, template engines, SEO auditing logic.
what to build custom: scoring algorithms, niche-specific rules, your content, your funnels.

**search queries:**
```
"seo analyzer" license:mit stars:>100
"keyword research tool" license:mit
"email template builder" license:mit stars:>100
"landing page builder" license:mit stars:>200
"ab testing" license:mit stars:>100
"analytics dashboard" license:mit stars:>200
"google analytics alternative" license:mit stars:>500
"heatmap" license:mit stars:>100
"link shortener" license:mit stars:>200
"qr code generator" license:mit stars:>500
"newsletter" license:mit stars:>200
"email marketing" license:mit stars:>100
"popup builder" license:mit
"social proof" license:mit
"referral system" license:mit
"affiliate tracking" license:mit
"waitlist" license:mit stars:>100
"feedback widget" license:mit
"nps survey" license:mit
"customer feedback" license:mit
```

**splice strategy:**
1. take SEO analysis logic, wrap in your own reporting UI
2. take email template rendering, add your copywriting + sequences
3. take analytics collection code, build your own dashboard on top
4. take referral/affiliate tracking logic, integrate with your products
5. never pay for SaaS when an MIT repo does 80% of the job

### F. Payment and Billing

what to take: webhook handlers, subscription management, receipt validation, checkout flows.
what to build custom: pricing logic, trial flows, paywall design, upgrade nudges.

**search queries:**
```
"stripe subscription" license:mit stars:>100
"stripe checkout" license:mit stars:>200
"stripe webhook" license:mit stars:>100
"revenueCat" license:mit
"in app purchase" license:mit stars:>100
"lemon squeezy" license:mit
"payment gateway" license:mit stars:>200
"saas billing" license:mit stars:>100
"subscription management" license:mit
"invoice generator" license:mit stars:>100
"paywall" license:mit stars:>50
"freemium" license:mit
"stripe react" license:mit
"paddle integration" license:mit
"gumroad api" license:mit
```

**splice strategy:**
1. stripe webhook handling is surprisingly complex. take it from a proven repo.
2. subscription state management (active, past_due, canceled, trial) - take the state machine
3. receipt validation for iOS/Android - take from RevenueCat examples
4. build custom: your pricing tiers, your upgrade flows, your paywall copy, your trial length
5. the billing infrastructure is commodity. pricing strategy is your edge.

### G. UI Component Libraries

what to take: individual components (not whole libraries). calendar widgets, charts, modals, forms.
what to build custom: branding, animation, responsive behavior, accessibility tweaks.

**search queries:**
```
"react components" license:mit stars:>1000
"tailwind components" license:mit stars:>500
"shadcn ui" license:mit
"headless ui" license:mit stars:>500
"radix ui" license:mit
"chart component react" license:mit stars:>500
"calendar component" license:mit stars:>200
"date picker" license:mit stars:>500
"rich text editor" license:mit stars:>1000
"markdown editor" license:mit stars:>500
"table component react" license:mit stars:>500
"drag and drop" license:mit stars:>1000
"file upload component" license:mit stars:>200
"color picker" license:mit stars:>200
"toast notification" license:mit stars:>500
"modal dialog" license:mit stars:>200
"accordion" license:mit stars:>100
"carousel slider" license:mit stars:>500
"infinite scroll" license:mit stars:>200
"virtual list" license:mit stars:>500
```

**splice strategy:**
1. shadcn/ui is the GOAT for this. copy individual components, own the code.
2. for specialized components (rich text editor, charts), take from purpose-built repos
3. always strip out the styling and apply your own design tokens
4. never import a full component library just for one component. that's bundle bloat.
5. one component from here, one from there, unified under your Tailwind config = custom design system

### H. Backend Services

what to take: auth middleware, rate limiting, caching patterns, API structure.
what to build custom: business logic, data models, API design, integrations.

**search queries:**
```
"api boilerplate" license:mit stars:>200
"express boilerplate" license:mit stars:>500
"fastapi template" license:mit stars:>300
"serverless functions" license:mit stars:>200
"rate limiter" license:mit stars:>500
"redis cache" license:mit stars:>200
"jwt auth middleware" license:mit stars:>200
"oauth2 server" license:mit stars:>200
"api gateway" license:mit stars:>300
"graphql boilerplate" license:mit stars:>200
"trpc" license:mit
"rest api template" license:mit stars:>200
"websocket server" license:mit stars:>200
"file upload server" license:mit stars:>100
"image processing api" license:mit stars:>100
"pdf generator api" license:mit stars:>100
"email sender service" license:mit stars:>100
"sms notification" license:mit
"push notification server" license:mit
"background job processor" license:mit stars:>200
```

**splice strategy:**
1. auth middleware is the #1 thing to take from repos. nobody should write JWT validation from scratch.
2. rate limiting patterns are critical for APIs and scrapers. take battle-tested implementations.
3. caching strategies (Redis patterns, in-memory cache) - take the infrastructure, customize TTLs
4. API structure/routing patterns - take from well-organized repos, fill with your business logic
5. the boilerplate is free. the business logic on top is what generates revenue.

---

## 4. The Hybrid Splice Workflow

step-by-step process for every repurposing operation:

```
STEP 1: IDENTIFY NEED
  what specific functionality do you need?
  is it auth? scraping? UI? payments? scheduling?
  be specific. "I need Google OAuth with magic link fallback" not "I need auth"

STEP 2: SEARCH
  use GitHub search with license:mit filter
  use the search queries from Section 3 above
  sort by stars, recently updated, or best match depending on what you need
  check 3-5 repos minimum before picking

STEP 3: EVALUATE
  run the full security protocol from Section 2
  check: license, dependencies, network calls, obfuscation, maintenance status
  if anything fails = next repo

STEP 4: EXTRACT
  DO NOT fork the whole repo
  copy ONLY the files and functions you actually need
  strip unused imports, unused dependencies, unused config
  less code = less attack surface = easier to maintain

STEP 5: AUDIT
  read every line of extracted code
  understand what it does, where data flows, what external calls it makes
  if you can't explain what a line does, don't include it

STEP 6: ADAPT
  modify for your use case
  remove unnecessary dependencies
  rename to match your codebase conventions
  add your error handling patterns
  integrate with your logging/monitoring

STEP 7: INTEGRATE
  splice into your existing codebase
  resolve import conflicts
  run your test suite
  verify no breaking changes

STEP 8: TEST
  unit tests for extracted logic
  integration tests for the splice points
  end-to-end test of the full flow
  load test if it's a critical path

STEP 9: DOCUMENT
  log in LEDGER/GITHUB_REPURPOSE_TRACKER.csv:
  - source repo URL
  - license
  - what files/functions were extracted
  - what modifications were made
  - date integrated
  - which project it went into

STEP 10: SHIP
  deploy with confidence
  monitor for issues in first 48 hours
  if something breaks, you have the source to debug
```

---

## 5. Splicing Patterns (Advanced)

### Pattern 1: Component Harvest

take individual UI components from different repos, unify under your design system.

```
Repo A: calendar widget (date picking, event display)
Repo B: notification toast system (queue, animation, dismiss)
Repo C: chart components (line, bar, pie)
YOUR CODE: Tailwind config, color tokens, spacing, typography
RESULT: custom design system with battle-tested components
```

when to use: building any user-facing app. saves 20-40 hours of component building.

### Pattern 2: Logic Extraction

take core algorithms and business logic, wrap in your own API.

```
Repo A: SEO scoring algorithm (keyword density, readability, meta analysis)
YOUR CODE: custom UI dashboard, niche-specific rules, report generation
RESULT: SEO tool that scores content for your specific niche
```

when to use: building tools or SaaS. the algorithm is the hard part. take it, wrap it, sell it.

### Pattern 3: Architecture Template

use repo as architectural reference, rewrite key implementations.

```
Repo A: well-structured SaaS boilerplate (folder structure, patterns, conventions)
YOUR CODE: rewrite the actual business logic following the same architecture
RESULT: clean codebase with proven architecture patterns, zero copied code
```

when to use: starting a new project. don't copy code, copy structure. learn from how they organized things.

### Pattern 4: Dependency Replacement

replace a paid SaaS with an open-source self-hosted alternative.

```
PAID: Mixpanel ($25+/mo for analytics)
MIT REPO: self-hosted analytics (Umami, Plausible CE)
YOUR CODE: deployment config, custom event tracking, dashboard customization
SAVINGS: $300+/year per product
```

when to use: any time you're paying for SaaS that has an MIT alternative. compound savings across all products.

**common replacements:**
| Paid Service | MIT Alternative | Annual Savings |
|-------------|----------------|----------------|
| Mixpanel/Amplitude | Umami, Plausible CE | $300-$1,200 |
| Intercom | Chatwoot | $500-$2,000 |
| Mailchimp | Listmonk | $200-$600 |
| Airtable | NocoDB | $120-$500 |
| Notion (API) | AppFlowy | $100-$400 |
| Calendly | Cal.com | $100-$300 |
| Typeform | Formbricks | $300-$1,000 |
| Hotjar | OpenReplay | $400-$1,200 |

### Pattern 5: Multi-Repo Frankenstein

best pieces from 3-5 repos combined into one superior product. this is the most powerful pattern.

```
Repo A: auth system (OAuth + magic link + session management)
Repo B: UI framework (dashboard layout + components + responsive)
Repo C: API layer (CRUD + validation + error handling)
Repo D: payments (Stripe integration + webhook handlers)
YOUR CODE: business logic + branding + monetization strategy + content
RESULT: full SaaS product built in days instead of months
```

when to use: building any substantial product. this is the default play.

**example for building a PrayerLock-style app:**
```
Repo 1: React Native starter with Expo (navigation, splash screen, app structure)
Repo 2: Prayer times library (calculation algorithms, timezone handling)
Repo 3: Notification scheduler (local notifications, background tasks)
Repo 4: RevenueCat example (IAP, subscription management)
YOUR CODE: gamification (streaks, rewards), community features, Islamic content, branding
```

### Pattern 6: Scraper Pipeline Assembly

combine scraping components into a full data pipeline.

```
Repo A: proxy rotation library
Repo B: browser fingerprint spoofing
Repo C: target-platform-specific parser
YOUR CODE: data cleaning, deduplication, output to LEDGER, monitoring
RESULT: production-grade scraping pipeline
```

when to use: any lead gen, competitive intel, price monitoring, or data collection operation.

---

## 6. License Quick Reference

| License | Commercial Use | Modify | Distribute | Must Include | Risk Level |
|---------|:-:|:-:|:-:|-------------|:--:|
| **MIT** | YES | YES | YES | License text in your repo | SAFE |
| **Apache 2.0** | YES | YES | YES | License + NOTICE file + state changes | SAFE |
| **BSD 2-Clause** | YES | YES | YES | License text | SAFE |
| **BSD 3-Clause** | YES | YES | YES | License text, no endorsement claims | SAFE |
| **ISC** | YES | YES | YES | License text | SAFE |
| **Unlicense** | YES | YES | YES | Nothing required | SAFE |
| **CC0** | YES | YES | YES | Nothing required | SAFE |
| **MPL 2.0** | YES | YES | YES | Modified files must stay MPL | MODERATE |
| **LGPL** | YES | YES | YES | Dynamic linking OK, static = share | MODERATE |
| **GPL v2/v3** | AVOID | YES | Must GPL | Your entire codebase becomes GPL | DANGEROUS |
| **AGPL** | AVOID | YES | Must AGPL | Even server-side use = must share ALL code | DANGEROUS |
| **SSPL** | AVOID | Limited | Very restricted | MongoDB-style trap, avoid completely | DANGEROUS |
| **BSL** | AVOID | Limited | Time-delayed | Business Source License, commercial restrictions | DANGEROUS |
| **No License** | NO | NO | NO | Treat as all rights reserved | REJECT |

**rule of thumb:** MIT, Apache 2.0, BSD, ISC = green light. everything else = read carefully or skip.

**compliance:** when you use MIT/Apache/BSD code, include the license text somewhere in your project (usually a LICENSES or THIRD_PARTY_NOTICES file). takes 30 seconds. do it.

---

## 7. Tracking and Documentation

every repo you extract code from gets logged in `LEDGER/GITHUB_REPURPOSE_TRACKER.csv`.

**why track:**
- legal compliance (know which licenses you're using)
- update awareness (if a source repo patches a security issue, you need to know)
- avoid duplicate work (don't re-evaluate repos you've already checked)
- portfolio visibility (how much value are you extracting from open source?)

**CSV format:**

```
repo_url,license,stars,last_commit,what_taken,files_extracted,security_check_passed,integrated_into,date_integrated,estimated_hours_saved,notes
```

**update this CSV every time you extract code from a repo. no exceptions.**

---

## 8. GitHub Search Power Queries

### Direct Search URLs

these are ready to paste into your browser. sorted by category.

**App Templates:**
- https://github.com/search?q=nextjs+saas+starter+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=react+native+template+license%3Amit+stars%3A%3E200&type=repositories&s=stars
- https://github.com/search?q=expo+starter+license%3Amit+stars%3A%3E100&type=repositories&s=stars
- https://github.com/search?q=pwa+template+license%3Amit+stars%3A%3E50&type=repositories&s=stars
- https://github.com/search?q=supabase+starter+license%3Amit&type=repositories&s=stars

**Scrapers:**
- https://github.com/search?q=web+scraper+python+license%3Amit+stars%3A%3E200&type=repositories&s=stars
- https://github.com/search?q=playwright+scraper+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=google+maps+scraper+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=lead+generation+scraper+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=price+tracker+license%3Amit+stars%3A%3E50&type=repositories&s=stars

**Automation:**
- https://github.com/search?q=social+media+scheduler+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=task+queue+license%3Amit+stars%3A%3E500&type=repositories&s=stars
- https://github.com/search?q=cron+job+manager+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=telegram+bot+license%3Amit+stars%3A%3E500&type=repositories&s=stars
- https://github.com/search?q=workflow+automation+license%3Amit+stars%3A%3E200&type=repositories&s=stars

**AI/ML:**
- https://github.com/search?q=langchain+template+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=rag+chatbot+license%3Amit+stars%3A%3E100&type=repositories&s=stars
- https://github.com/search?q=openai+api+wrapper+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=whisper+api+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=ai+chatbot+license%3Amit+stars%3A%3E300&type=repositories&s=stars

**Marketing:**
- https://github.com/search?q=seo+analyzer+license%3Amit+stars%3A%3E100&type=repositories&s=stars
- https://github.com/search?q=analytics+dashboard+license%3Amit+stars%3A%3E200&type=repositories&s=stars
- https://github.com/search?q=email+template+builder+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=landing+page+builder+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=waitlist+license%3Amit+stars%3A%3E100&type=repositories&s=stars

**Payments:**
- https://github.com/search?q=stripe+subscription+license%3Amit+stars%3A%3E100&type=repositories&s=stars
- https://github.com/search?q=stripe+webhook+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=in+app+purchase+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=saas+billing+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=invoice+generator+license%3Amit&type=repositories&s=stars

**UI Components:**
- https://github.com/search?q=react+components+license%3Amit+stars%3A%3E1000&type=repositories&s=stars
- https://github.com/search?q=tailwind+components+license%3Amit+stars%3A%3E500&type=repositories&s=stars
- https://github.com/search?q=rich+text+editor+license%3Amit+stars%3A%3E1000&type=repositories&s=stars
- https://github.com/search?q=chart+component+react+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=drag+and+drop+license%3Amit+stars%3A%3E1000&type=repositories&s=stars

**Backend:**
- https://github.com/search?q=fastapi+template+license%3Amit+stars%3A%3E300&type=repositories&s=stars
- https://github.com/search?q=express+boilerplate+license%3Amit+stars%3A%3E500&type=repositories&s=stars
- https://github.com/search?q=rate+limiter+license%3Amit+stars%3A%3E500&type=repositories&s=stars
- https://github.com/search?q=jwt+auth+middleware+license%3Amit&type=repositories&s=stars
- https://github.com/search?q=websocket+server+license%3Amit+stars%3A%3E200&type=repositories&s=stars

### Advanced Search Operators

```
# Find repos updated in 2026 with MIT license and 100+ stars
language:typescript license:mit stars:>100 pushed:>2025-06-01 "saas"

# Find repos with specific file patterns
license:mit filename:docker-compose.yml "nextjs"

# Find repos by topic tag
license:mit topic:saas topic:boilerplate stars:>200

# Find repos with good documentation
license:mit stars:>500 "getting started" in:readme language:python

# Exclude forks (original repos only)
license:mit stars:>100 fork:false "scraper" language:python

# Find repos with recent activity
license:mit stars:>50 pushed:>2025-09-01 "stripe subscription"
```

---

## 9. PRINTMAXX-Specific Repo Targets

repos that map directly to current money methods:

### App Factory
- prayer/Islamic app repos (PrayerLock base)
- fitness/step tracker repos (StepLock base)
- habit tracker repos (Streakr base)
- recipe/cooking app repos (Mise base)
- journaling/vault app repos (Vault base)

### Content Farm
- social media posting tools
- content scheduling repos
- RSS-to-social bridges
- auto-captioning tools (whisper-based)
- thumbnail generators

### Cold Outbound
- email sending libraries (nodemailer wrappers, SMTP)
- email warmup tools
- lead enrichment (clearbit-style)
- CRM repos (pipeline management)
- email template renderers

### Local Biz
- website template repos (restaurant, dental, fitness, legal)
- contact form handlers
- Google Business Profile tools
- review management repos
- appointment scheduling

### AI Influencer
- image generation pipelines
- face consistency tools (LoRA, IP-Adapter)
- voice cloning repos
- video generation tools
- social media automation for personas

### Ecom
- Shopify theme repos
- product listing tools
- inventory management
- price comparison scrapers
- review aggregation

---

## 10. ROI Calculator

before extracting code from any repo, estimate the ROI:

```
TIME TO BUILD FROM SCRATCH: X hours
TIME TO EXTRACT + ADAPT FROM REPO: Y hours
HOURLY VALUE OF YOUR TIME: $Z

SAVINGS = (X - Y) * Z

if SAVINGS > $50, use the repo.
if SAVINGS < $50, just build it yourself (simpler to maintain).
```

**typical savings by category:**

| Category | Build From Scratch | Extract + Adapt | Hours Saved |
|----------|:-:|:-:|:-:|
| Auth system | 20-40 hrs | 2-4 hrs | 18-36 hrs |
| Payment integration | 15-30 hrs | 2-5 hrs | 13-25 hrs |
| Scraper pipeline | 10-20 hrs | 2-4 hrs | 8-16 hrs |
| UI component set | 30-60 hrs | 5-10 hrs | 25-50 hrs |
| API boilerplate | 10-20 hrs | 1-3 hrs | 9-17 hrs |
| Full SaaS template | 80-160 hrs | 10-20 hrs | 70-140 hrs |

at even a modest $50/hr valuation, a full SaaS splice saves $3,500-$7,000 worth of time.

---

## 11. Maintenance Protocol

extracted code is YOUR code now. you maintain it.

```
MONTHLY:
- check source repos for security patches (star them on GitHub for easy tracking)
- run npm audit / pip-audit on your projects
- update dependencies if needed

QUARTERLY:
- review GITHUB_REPURPOSE_TRACKER.csv for stale integrations
- check if better alternatives have emerged for any component
- consider replacing outdated extractions with newer repos

ON SECURITY ALERT:
- if a source repo publishes a CVE or security advisory
- immediately check if your extracted code is affected
- patch or replace immediately
```

---

## 12. Anti-Patterns (What NOT to Do)

**DO NOT:**
- fork a repo and just change the colors. that's not a product.
- use GPL code in your commercial project. you will get sued.
- skip the security scan because "it has lots of stars." stars != security.
- depend on a single abandoned repo for critical functionality. have a backup.
- extract code you don't understand. if you can't debug it, don't ship it.
- ignore license attribution requirements. MIT says include the license. include it.
- use a whole framework when you need one function. extract the function.
- trust code from repos with 0 issues and 0 PRs. real projects have both.
- copy-paste from Stack Overflow without checking the license (it's CC BY-SA, which has share-alike requirements).

**DO:**
- extract surgically. take only what you need.
- read every line you extract. understand it.
- test extracted code in isolation before integrating.
- track everything in the CSV.
- check for updates to source repos quarterly.
- attribute properly (license files, THIRD_PARTY_NOTICES).
- combine pieces from multiple repos for a superior result.
- build custom where it matters (monetization, UX, business logic).

---

## Quick Reference Card

```
SEARCH:  github.com/search?q={keywords}+license%3Amit+stars%3A%3E{min_stars}&type=repositories
SCAN:    ./github_repo_security_scan.sh /path/to/cloned/repo
TRACK:   LEDGER/GITHUB_REPURPOSE_TRACKER.csv
SPLICE:  extract -> audit -> adapt -> integrate -> test -> document -> ship
NEVER:   GPL, raw forks, unaudited deps, skip attribution
ALWAYS:  MIT/Apache/BSD, surgical extraction, security scan, license compliance
```
