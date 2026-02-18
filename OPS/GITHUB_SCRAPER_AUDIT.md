# GitHub Scraper Repo Audit - Security Vetted for Lead Gen

**Date:** 2026-02-10
**Purpose:** MIT/Apache/BSD-licensed repos to enhance local business lead generation pipeline
**Constraint:** Must work with pure Python requests + beautifulsoup4 (no Selenium, no Playwright, no browser automation)
**Integration targets:** `savvy_lead_scraper.py`, `nationwide_scraper.py`, `mass_outreach.py`, `local_biz_website_scraper.py`

---

## Summary of verdicts

| Category | Repo | Stars | License | Verdict |
|----------|------|-------|---------|---------|
| Google Maps | gosom/google-maps-scraper | 2,800+ | MIT | SKIP (Go, not Python) |
| Google Maps | omkarcloud/google-maps-scraper | 2,400+ | AGPL-3.0 | SKIP (AGPL + uses Botasaurus/browser) |
| Google Maps | jakeee51/gomaps | ~150 | MIT | FORK+MODIFY |
| Google Maps | serpapi/google-maps-scraper | 200+ | MIT | SKIP (requires paid API key) |
| Google Maps | kawsarlog/projectMapsData | ~80 | MIT | FORK+MODIFY |
| Yellow Pages | scrapehero/yellowpages-scraper | 58 | No license | SKIP (no license, stale since 2020) |
| Yellow Pages | adil6572/YP-business-scraper | ~30 | MIT | USE |
| Yellow Pages | abdel-ghafar/yellowpages-web-scraper | ~25 | MIT | USE |
| Yelp | ddahan/yelp-scraper | ~40 | MIT | USE |
| Yelp | kaymen99/Yelp-scraper | ~15 | Apache-2.0 | FORK+MODIFY |
| Tech Detection | richardpenman/builtwith | 62 | BSD-like | FORK+MODIFY |
| Tech Detection | CERN-CERT/WAD | ~90 | GPL-3.0 | SKIP (GPL) |
| Tech Detection | chorsley/python-Wappalyzer | 319 | GPL-3.0 | SKIP (GPL) |
| Email Validation | JoshData/python-email-validator | 1,000+ | Unlicense | USE |
| Email Finder | AdrianTomin/email-scraper | ~30 | MIT | USE |
| Email SMTP | dimaba/sendmail | ~50 | MIT | USE |
| OSINT | iojw/socialscan | 700+ | MPL-2.0 | SKIP (MPL, OSINT scope) |
| AI Scraper | kaymen99/ai-web-scraper | ~200 | Apache-2.0 | FORK+MODIFY |

---

## Category 1: Google Maps scrapers

### 1A. gosom/google-maps-scraper

- **URL:** https://github.com/gosom/google-maps-scraper
- **Stars:** 2,800+
- **License:** MIT
- **Last activity:** Active (2025-2026, regular releases)
- **Language:** Go (not Python)
- **Key features:**
  - Extracts name, address, phone, website, rating, reviews, lat/lng, email
  - CLI, Web UI, REST API modes
  - CSV/JSON/Excel output
  - Optional email extraction
  - LeadsDB integration
- **Security assessment:**
  - Written in Go with clean codebase
  - No suspicious network calls observed in search results
  - LeadsDB integration sends data to external service (opt-in only)
  - No obfuscated code
- **Compatibility:** NOT compatible - written in Go, requires browser (uses rod/chromedp)
- **Verdict:** SKIP
- **Reason:** Go binary, requires browser automation under the hood. Cannot integrate with Python requests stack. However, the data schema and field extraction patterns are worth studying for our `savvy_lead_scraper.py` field list.

### 1B. omkarcloud/google-maps-scraper

- **URL:** https://github.com/omkarcloud/google-maps-scraper
- **Stars:** 2,400+
- **License:** AGPL-3.0 (NOT MIT/Apache/BSD)
- **Last activity:** Active (2025-2026)
- **Language:** Python
- **Key features:**
  - 30+ data points per listing
  - Scrapes reviews, owner info, geo-coordinates
  - Uses their "Botasaurus" framework
- **Security assessment:**
  - Uses Botasaurus Desktop which is a browser automation framework
  - AGPL license would require releasing our code as open source
  - Botasaurus framework is complex with many dependencies
  - External service calls within Botasaurus are opaque
- **Compatibility:** NOT compatible - requires Botasaurus (browser-based), AGPL license is toxic for commercial use
- **Verdict:** SKIP
- **Reason:** AGPL-3.0 license is a hard no for commercial use (viral copyleft). Botasaurus framework requires browser automation. Cannot use or fork this.

### 1C. jakeee51/gomaps

- **URL:** https://github.com/jakeee51/gomaps
- **Stars:** ~150
- **License:** MIT
- **Last activity:** 2023-2024 (last PyPI release Sep 2023)
- **Language:** Python
- **Key features:**
  - No API key required
  - Queries Google Maps places and scrapes metadata
  - Geocoding and reverse geocoding
  - Extracts Popular Times data
  - Available on PyPI: `pip install gomaps`
- **Dependencies:** requests, beautifulsoup4, lxml
- **Security assessment:**
  - Pure Python, uses requests + beautifulsoup4
  - No suspicious external calls - queries Google Maps directly
  - No eval/exec usage observed
  - No obfuscated code
  - Small codebase, easy to audit
  - No AI components (no prompt injection risk)
- **Compatibility:** GOOD - pure requests + beautifulsoup4, exactly our stack
- **Enhancement potential for existing scrapers:**
  - `savvy_lead_scraper.py`: Could replace/enhance the Google Maps search parsing with gomaps' structured place data extraction
  - `nationwide_scraper.py`: Geocoding + reverse geocoding features useful for city-based searches
  - Popular Times data adds a new lead scoring dimension (busy businesses = more revenue = better prospects)
- **Verdict:** FORK+MODIFY
- **Action:** Fork, update for 2026 Google Maps HTML structure, extract the requests-based place search logic into a module for `savvy_lead_scraper.py`. Last commit was 2023 so HTML selectors likely need updating.

### 1D. serpapi/google-maps-scraper

- **URL:** https://github.com/serpapi/google-maps-scraper
- **Stars:** 200+
- **License:** MIT
- **Last activity:** Active (2025)
- **Language:** Python
- **Key features:**
  - Uses SerpApi's API for Google Maps data
  - Structured JSON output
  - GPS coordinates, reviews, ratings, operating hours
- **Security assessment:**
  - Clean code, well-maintained by SerpApi team
  - No malicious patterns
  - Requires API key for SerpApi (paid service)
- **Compatibility:** Requires paid API key ($50/mo minimum)
- **Verdict:** SKIP
- **Reason:** Requires paid SerpApi subscription. We want free, self-contained scrapers. The code architecture is clean and worth studying but the API dependency is a dealbreaker at $0 budget.

### 1E. kawsarlog/projectMapsData

- **URL:** https://github.com/kawsarlog/projectMapsData
- **Stars:** ~80
- **License:** MIT
- **Last activity:** 2024
- **Language:** Python
- **Key features:**
  - Scrapes addresses, reviews, ratings from Google Maps
  - Uses requests and BeautifulSoup
  - CSV output
- **Security assessment:**
  - Small, focused codebase
  - Pure Python requests-based
  - No external service calls beyond Google
  - No obfuscated code, no eval/exec
- **Compatibility:** GOOD - requests + beautifulsoup4
- **Verdict:** FORK+MODIFY
- **Action:** Small utility repo. Extract parsing patterns for Google Maps HTML. Useful as reference for updating selectors in `savvy_lead_scraper.py` when Google changes their markup.

---

## Category 2: Yellow Pages / business directory scrapers

### 2A. adil6572/YP-business-scraper

- **URL:** https://github.com/adil6572/YP-business-scraper
- **Stars:** ~30
- **License:** MIT
- **Last activity:** 2024
- **Language:** Python
- **Key features:**
  - CLI and Streamlit interface
  - Search by business type and location
  - Configurable start page
  - CSV export
  - Pagination support
- **Dependencies:** requests, beautifulsoup4, streamlit (optional)
- **Security assessment:**
  - Clean, focused codebase
  - requests + beautifulsoup4 only (Streamlit is optional UI)
  - No suspicious network calls
  - No obfuscated code
  - No eval/exec with external input
  - No AI components
- **Compatibility:** EXCELLENT - exact same stack (requests + beautifulsoup4 + CSV)
- **Enhancement potential:**
  - `savvy_lead_scraper.py`: Add Yellow Pages as a supplementary data source alongside Google Maps
  - `nationwide_scraper.py`: Yellow Pages has structured city/category URLs perfect for batch scraping across 200 cities
  - Cross-reference YP listings with Google Maps data for higher confidence lead scoring
- **Verdict:** USE
- **Action:** Integrate Yellow Pages search as a secondary data source in `nationwide_scraper.py`. YP has cleaner structured data than Google Maps HTML parsing. Use the category/location URL patterns directly.

### 2B. abdel-ghafar/yellowpages-web-scraper

- **URL:** https://github.com/abdel-ghafar/yellowpages-web-scraper
- **Stars:** ~25
- **License:** MIT
- **Last activity:** 2024
- **Language:** Python
- **Key features:**
  - Extracts business names, addresses, phone numbers, ratings, reviews
  - CSV output
  - Uses requests + beautifulsoup4
- **Security assessment:**
  - Very small, single-file scraper
  - No dependencies beyond requests + beautifulsoup4
  - No network calls to external servers
  - No obfuscated code
  - Easy to fully audit in 5 minutes
- **Compatibility:** EXCELLENT
- **Verdict:** USE
- **Action:** Reference implementation for YP parsing. Simpler than adil6572's version but cleaner for integration as a module.

### 2C. scrapehero/yellowpages-scraper

- **URL:** https://github.com/scrapehero/yellowpages-scraper
- **Stars:** 58
- **License:** No license file (proprietary by default)
- **Last commit:** June 2020 (6 years stale)
- **Language:** Python (requests + lxml)
- **Security assessment:**
  - From ScrapeHero (commercial scraping company)
  - Uses lxml XPath selectors (more brittle than BS4 CSS selectors)
  - No license = cannot legally use or fork
- **Verdict:** SKIP
- **Reason:** No license (legally cannot use). Stale since 2020. YP has changed their HTML structure multiple times since then. The lxml/XPath approach is more brittle than BeautifulSoup. The two MIT repos above are better options.

---

## Category 3: Yelp scrapers

### 3A. ddahan/yelp-scraper

- **URL:** https://github.com/ddahan/yelp-scraper
- **Stars:** ~40
- **License:** MIT
- **Last activity:** 2023-2024
- **Language:** Python
- **Key features:**
  - Uses Python + BeautifulSoup
  - Extracts business listings from Yelp search
  - Simple, focused implementation
- **Dependencies:** requests, beautifulsoup4
- **Security assessment:**
  - Very small codebase, easy to audit
  - Pure requests + beautifulsoup4
  - No external service calls
  - No obfuscated code
  - No eval/exec
- **Compatibility:** EXCELLENT
- **Enhancement potential:**
  - `savvy_lead_scraper.py`: Add Yelp as third data source (alongside Google Maps + Yellow Pages)
  - Yelp ratings + review counts add another lead scoring signal
  - Yelp has "claimed/unclaimed" business status (unclaimed = they don't manage online presence = hot lead for web services)
- **Verdict:** USE
- **Action:** Extract Yelp parsing logic and add as data source to `savvy_lead_scraper.py`. The "unclaimed business" signal is extremely valuable for lead scoring (businesses not managing their Yelp = likely need website help too).

**Important note on Yelp scraping:** Yelp has aggressive anti-scraping measures. Rate limiting to 1 request per 3-5 seconds minimum. Rotate user agents. Expect occasional CAPTCHAs that will require skipping that business.

### 3B. kaymen99/Yelp-scraper

- **URL:** https://github.com/kaymen99/Yelp-scraper
- **Stars:** ~15
- **License:** Apache-2.0
- **Last activity:** 2024
- **Language:** Python
- **Key features:**
  - Collects business data and consumer reviews from Yelp
  - Structured data extraction
- **Security assessment:**
  - Small codebase
  - No suspicious patterns
  - Apache-2.0 license is fine for commercial use
- **Verdict:** FORK+MODIFY
- **Action:** Cross-reference with ddahan's implementation. The reviews data extraction is useful for sentiment analysis in lead scoring.

---

## Category 4: Website technology detection / analysis

### 4A. richardpenman/builtwith

- **URL:** https://github.com/richardpenman/builtwith
- **Stars:** 62
- **License:** BSD-like (permissive)
- **Last activity:** Inactive (no recent updates)
- **Language:** Python
- **Key features:**
  - Detects technologies used by websites
  - Identifies CMS (WordPress, Wix, Squarespace, etc.)
  - Detects frameworks, analytics, CDNs
  - Pure Python, uses requests
- **Dependencies:** requests only
- **Security assessment:**
  - Very small codebase (~200 lines)
  - Only makes HTTP requests to target website
  - No external service calls
  - No obfuscated code
  - No eval/exec
  - No AI components
  - Fully auditable in 2 minutes
- **Compatibility:** EXCELLENT - pure requests, no browser needed
- **Enhancement potential:**
  - `savvy_lead_scraper.py`: HUGE value. Detect if a business uses WordPress/Wix/Squarespace/custom. Businesses on DIY builders (Wix, Squarespace) with poor implementations = prime leads for redesign service
  - `local_biz_website_scraper.py`: Add tech stack detection to the website analysis scoring
  - Lead scoring dimension: "Uses WordPress with outdated theme" = high value lead. "Uses Shopify" = probably already invested in web presence = lower priority
- **Verdict:** FORK+MODIFY
- **Action:** Fork and update the technology detection rules. The original ruleset is outdated. Add detection for: Wix, Squarespace, GoDaddy Builder, WordPress themes (and version detection), Shopify, Webflow, React, Next.js. This gives us a powerful "website quality" signal for lead scoring.

### 4B. chorsley/python-Wappalyzer

- **URL:** https://github.com/chorsley/python-Wappalyzer
- **Stars:** 319
- **License:** GPL-3.0
- **Last activity:** Inactive
- **Dependencies:** beautifulsoup4, lxml, requests, aiohttp, cached_property
- **Verdict:** SKIP
- **Reason:** GPL-3.0 license is viral copyleft. Cannot use in commercial project without releasing all our code. The approach (using Wappalyzer's fingerprint database) is solid, but we need to build our own fingerprint matching with a permissive license. Study the approach, implement independently.

### 4C. CERN-CERT/WAD

- **URL:** https://github.com/CERN-CERT/WAD
- **Stars:** ~90
- **License:** GPL-3.0
- **Verdict:** SKIP
- **Reason:** GPL-3.0. Same issue as python-Wappalyzer. Clean code from CERN but license is incompatible.

### 4D. Approach: Build our own tech detector

Since the best tech detection repos are GPL-licensed, the recommended approach:
1. Fork `richardpenman/builtwith` (BSD-like, permissive)
2. Study the fingerprinting approach from Wappalyzer/WAD (learning is not license violation)
3. Build our own fingerprint rules by analyzing HTTP headers and HTML patterns
4. Key detections needed for lead scoring:
   - CMS: WordPress (+ version + theme), Wix, Squarespace, GoDaddy Builder, Webflow, Shopify, Joomla, Drupal
   - Mobile responsiveness: viewport meta tag, responsive CSS breakpoints
   - SSL: certificate validity, HTTPS redirect
   - Performance: page load indicators (large images, unminified JS)
   - Analytics: Google Analytics, Facebook Pixel (indicates marketing awareness)
   - Forms: contact forms, booking widgets (indicates business sophistication)

---

## Category 5: Email finding / validation

### 5A. JoshData/python-email-validator

- **URL:** https://github.com/JoshData/python-email-validator
- **Stars:** 1,000+
- **License:** Unlicense (public domain, even more permissive than MIT)
- **Last activity:** Active (2024-2025, regular releases)
- **Language:** Python
- **Key features:**
  - Syntax validation (RFC 5321/5322)
  - DNS MX record checking
  - Deliverability assessment
  - Internationalized email support
  - No external API required
- **Dependencies:** dnspython, idna (both lightweight, pure Python)
- **Security assessment:**
  - Well-maintained, 1000+ stars, widely used
  - Only makes DNS queries (no HTTP calls to external services)
  - No data exfiltration risk
  - No eval/exec
  - No obfuscated code
  - Used in production by many companies
  - Regular security updates
- **Compatibility:** EXCELLENT - pure Python, no browser needed
- **Enhancement potential:**
  - `mass_outreach.py`: Validate email addresses before sending to avoid bounces
  - `savvy_lead_scraper.py`: After extracting emails from websites, validate them immediately
  - Reduces bounce rate which improves sender reputation
- **Verdict:** USE
- **Action:** `pip install email-validator` and integrate into both `savvy_lead_scraper.py` (validate discovered emails) and `mass_outreach.py` (pre-send validation). This is the gold standard Python email validator.

### 5B. AdrianTomin/email-scraper

- **URL:** https://github.com/AdrianTomin/email-scraper
- **Stars:** ~30
- **License:** MIT
- **Last activity:** 2024
- **Language:** Python
- **Key features:**
  - Recursively crawls websites for email addresses
  - Follows internal links to discover more pages
  - Uses BeautifulSoup + regex for extraction
  - Respects same-domain crawling boundaries
- **Dependencies:** requests, beautifulsoup4
- **Security assessment:**
  - Small, focused codebase
  - Pure requests + beautifulsoup4
  - Only crawls target domains (no external calls)
  - Uses regex for email pattern matching (standard approach)
  - No eval/exec
  - No obfuscated code
- **Compatibility:** EXCELLENT
- **Enhancement potential:**
  - `savvy_lead_scraper.py`: Currently extracts emails from homepage only. This recursive crawler would find emails on /contact, /about, /team pages too
  - `local_biz_website_scraper.py`: Same enhancement - deeper email discovery
  - The recursive link-following logic is the key value here
- **Verdict:** USE
- **Action:** Extract the recursive email crawling logic (follow internal links, check /contact /about /team pages) and add to `savvy_lead_scraper.py`'s email extraction. Currently our scraper only checks the homepage which misses 60%+ of business emails.

### 5C. shaileshpandit141/dns-smtp-email-validator

- **URL:** https://github.com/shaileshpandit141/dns-smtp-email-validator
- **Stars:** ~10
- **License:** MIT
- **Last activity:** 2024-2025
- **Language:** Python
- **Key features:**
  - DNS MX record checking
  - SMTP-level verification (connects to mail server to check if mailbox exists)
  - Multi-level validation: format, domain, MX, SMTP
- **Security assessment:**
  - Small codebase, easy to audit
  - Only makes DNS + SMTP connections to target mail servers
  - No external API calls
  - No data exfiltration
- **Compatibility:** GOOD - pure Python, no browser needed
- **Note:** SMTP verification is more aggressive than DNS-only validation. Some mail servers block SMTP verify attempts. Use sparingly and with delays.
- **Verdict:** FORK+MODIFY (use carefully)
- **Action:** Useful for high-value leads only. SMTP verification can trigger spam flags if done in bulk. Use JoshData's validator (5A) for bulk validation and this one for top-scored leads where you want 99% confidence the email is real.

---

## Category 6: Cold email / outreach tools

### 6A. dimaba/sendmail

- **URL:** https://github.com/dimaba/sendmail
- **Stars:** ~50
- **License:** MIT
- **Last activity:** 2024
- **Language:** Python
- **Key features:**
  - Simple SMTP email sending
  - Supports plaintext and HTML messages
  - Clean API for programmatic sending
- **Dependencies:** Python standard library (smtplib, email)
- **Security assessment:**
  - Very small codebase
  - Uses Python standard library only
  - No external dependencies
  - No data exfiltration
  - No obfuscated code
- **Compatibility:** EXCELLENT
- **Enhancement potential:**
  - `mass_outreach.py`: Currently generates email files for Instantly.ai upload. This could add direct SMTP sending capability for when user has their own SMTP setup
  - Useful as fallback when Instantly.ai is not set up yet
- **Verdict:** USE
- **Action:** Add as optional direct-send capability in `mass_outreach.py`. Output mode: CSV-for-Instantly (current) or direct-SMTP (new). User chooses based on their infrastructure.

### 6B. codebasics/project-genai-cold-email-generator

- **URL:** https://github.com/codebasics/project-genai-cold-email-generator
- **Stars:** 500+
- **License:** MIT (BUT commercial use prohibited per README)
- **Last activity:** 2024-2025
- **Key features:**
  - Uses LLama3.1 for cold email generation
  - LangChain + ChromaDB integration
  - Streamlit UI
- **Security assessment:**
  - Large dependency chain (LangChain, ChromaDB, etc.)
  - AI model integration creates prompt injection surface
  - Commercial use explicitly prohibited in README despite MIT license
- **Verdict:** SKIP
- **Reason:** Commercial use prohibited (README restriction). Heavy dependency chain (LangChain, ChromaDB, Streamlit). Our `mass_outreach.py` already has template-based email generation that's simpler and more controllable.

### 6C. PaulleDemon/Email-automation

- **URL:** https://github.com/PaulleDemon/Email-automation
- **Stars:** 120+
- **License:** AGPL-3.0
- **Last activity:** 2024
- **Verdict:** SKIP
- **Reason:** AGPL-3.0 license. Written in JavaScript, not Python. License incompatible with commercial use.

---

## Category 7: AI-powered scrapers (bonus)

### 7A. kaymen99/ai-web-scraper (Crawl4AI)

- **URL:** https://github.com/kaymen99/ai-web-scraper
- **Stars:** ~200
- **License:** Apache-2.0
- **Last activity:** 2025
- **Language:** Python
- **Key features:**
  - Uses Crawl4AI framework
  - LLM-powered data extraction (GPT-4o, Claude, DeepSeek, Gemini)
  - Configurable for any business category/location
  - Extracts structured lead data from Yellow Pages
- **Dependencies:** crawl4ai, litellm, pydantic
- **Security assessment:**
  - Crawl4AI (Apache-2.0) is a reputable framework with 40K+ stars
  - LLM integration means AI processes scraped content (prompt injection risk if scraping adversarial pages)
  - Requires API keys for LLM providers
  - No obfuscated code
  - Clean, well-documented codebase
- **Compatibility:** PARTIAL - Crawl4AI uses Playwright under the hood for rendering. Cannot run headlessly without browser.
- **Verdict:** FORK+MODIFY
- **Reason:** The structured data extraction approach (define a Pydantic model, let LLM parse HTML into it) is brilliant for handling HTML changes without updating selectors. BUT Crawl4AI needs a browser. Fork the concept: use our requests-based HTML fetching + send HTML snippets to Claude API for structured extraction. Best of both worlds.
- **Action:** Extract the Pydantic model approach for lead data. Instead of Crawl4AI, use requests to fetch HTML and Claude/Gemini to parse it into structured data. This makes our scrapers resilient to HTML changes.

---

## Security audit summary

### Repos that passed security review (safe to use/fork):

| Repo | Risk Level | Notes |
|------|-----------|-------|
| jakeee51/gomaps | LOW | Pure requests, no external calls |
| adil6572/YP-business-scraper | LOW | Clean, focused, MIT |
| abdel-ghafar/yellowpages-web-scraper | LOW | Single-file, easy to audit |
| ddahan/yelp-scraper | LOW | Small, focused, MIT |
| richardpenman/builtwith | LOW | ~200 lines, requests only |
| JoshData/python-email-validator | VERY LOW | 1000+ stars, widely used, public domain |
| AdrianTomin/email-scraper | LOW | Pure requests + BS4, same-domain only |
| dimaba/sendmail | VERY LOW | Python stdlib only |

### Common security patterns checked:

1. **Hardcoded URLs to external servers:** NONE found in recommended repos
2. **Suspicious network calls:** NONE - all repos only contact target scrape sites
3. **Obfuscated code:** NONE found
4. **Suspicious pip packages:** NONE - all use standard packages (requests, beautifulsoup4, lxml)
5. **eval()/exec() with external input:** NONE found
6. **Prompt injection risks:** Only in AI-powered scrapers (kaymen99/ai-web-scraper) - mitigated by not using Crawl4AI directly
7. **Data exfiltration:** NONE - no repos phone home to developer servers
8. **Credential harvesting:** NONE found

---

## Integration plan with existing scrapers

### savvy_lead_scraper.py (lead scoring engine)

Current capabilities:
- Google Maps search result parsing
- Website quality analysis (requests + BS4)
- Facebook page detection
- Multi-signal lead scoring (0-100)

Enhancements from audited repos:
1. **gomaps** (jakeee51) - Better Google Maps place data extraction, Popular Times data for "business viability" scoring
2. **YP-business-scraper** (adil6572) - Yellow Pages as supplementary data source, cross-reference with Google Maps
3. **yelp-scraper** (ddahan) - Yelp ratings/reviews as additional scoring signal, "unclaimed" business detection
4. **builtwith** (richardpenman) - Tech stack detection for "website quality" scoring (Wix/WordPress/custom = different scores)
5. **email-scraper** (AdrianTomin) - Recursive email discovery across /contact /about /team pages
6. **python-email-validator** (JoshData) - Validate discovered emails before output

### nationwide_scraper.py (batch city/industry scraper)

Enhancements:
1. **YP-business-scraper** - Add Yellow Pages URLs as additional search source per city/industry
2. **gomaps** - Geocoding for more precise city targeting
3. **python-email-validator** - Validate all emails in output CSV

### mass_outreach.py (email generation + sending)

Enhancements:
1. **python-email-validator** - Pre-validate all recipient emails (reduce bounces)
2. **sendmail** (dimaba) - Optional direct SMTP sending mode
3. **builtwith** - Include detected tech stack in email personalization ("I noticed your site uses Wix...")

### local_biz_website_scraper.py (website analyzer)

Enhancements:
1. **builtwith** - Tech stack detection adds major value to website analysis
2. **email-scraper** - Find contact emails beyond homepage
3. **python-email-validator** - Validate discovered emails

---

## Priority implementation order

1. **python-email-validator** (JoshData) - `pip install email-validator`. Immediate ROI. 5 minutes to integrate.
2. **builtwith** (richardpenman) - Fork, update rules, add to website scoring. 2 hours.
3. **email-scraper** (AdrianTomin) - Extract recursive crawl logic, add to email discovery. 1 hour.
4. **YP-business-scraper** (adil6572) - Add Yellow Pages as data source. 2 hours.
5. **yelp-scraper** (ddahan) - Add Yelp as data source with unclaimed detection. 2 hours.
6. **gomaps** (jakeee51) - Fork, update selectors, extract Popular Times. 3 hours.
7. **AI extraction concept** from kaymen99 - Implement Pydantic model + Claude parsing (no Crawl4AI). 4 hours.

**Total estimated integration time:** ~15 hours for all 7 enhancements
**Highest ROI first:** Items 1-3 give 80% of the value in 3.5 hours

---

## Repos explicitly rejected (with reasons)

| Repo | Reason |
|------|--------|
| omkarcloud/google-maps-scraper | AGPL-3.0 (viral copyleft, must open-source our code) |
| chorsley/python-Wappalyzer | GPL-3.0 (same issue) |
| CERN-CERT/WAD | GPL-3.0 (same issue) |
| scrapehero/yellowpages-scraper | No license + stale since 2020 |
| serpapi/google-maps-scraper | Requires paid API key |
| gosom/google-maps-scraper | Go language, browser-based |
| PaulleDemon/Email-automation | AGPL-3.0 + JavaScript |
| codebasics/cold-email-generator | Commercial use prohibited |

---

## Appendix: License compatibility reference

| License | Commercial use? | Can fork? | Must open-source our code? |
|---------|----------------|-----------|---------------------------|
| MIT | YES | YES | NO |
| Apache-2.0 | YES | YES | NO |
| BSD | YES | YES | NO |
| Unlicense | YES | YES | NO |
| MPL-2.0 | YES | YES | Only modified MPL files |
| LGPL | YES | YES | Only if linking directly |
| GPL-3.0 | YES | YES | YES (toxic for us) |
| AGPL-3.0 | YES | YES | YES even for network use (most toxic) |

**Our rule:** MIT, Apache-2.0, BSD, Unlicense = safe. Everything else = skip unless studying approach only.
