# Grey Hat Legal Guide — What's Allowed, Risky, and Illegal

**Scope:** Compliance analysis of growth tactics commonly used in solopreneur/indie hacker space.
**Purpose:** Know the rules so you can operate at the edge without crossing legal lines.
**Disclaimer:** This is not legal advice. Consult an attorney for your specific situation. Laws vary by jurisdiction.

**Last updated:** 2026-03-05
**Status of each tactic:** ALLOWED | RISKY (depends on execution) | ILLEGAL

---

## CATEGORY 1: CONTENT MARKETING

### Multiple Social Accounts (Same Person)

**Status: ALLOWED**
Running multiple accounts on the same platform as the same person is permitted on most platforms IF:
- You're not impersonating anyone
- You're not using one account to boost another (coordination policy)
- Each account follows platform ToS individually

**What's risky:** Coordinated inauthentic behavior — using Account A to like/RT Account B to make it look like organic engagement. Twitter, Meta, and TikTok explicitly prohibit this.

**What's fine:** Maintaining @printmaxxer and @selahmoments as separate accounts with separate content strategies.

---

### AI-Generated Personas / Faceless Accounts

**Status: ALLOWED with disclosures**

Using AI-generated faces, voices, and personas is legal. However:
- You cannot claim to be a real person who doesn't exist and defraud people with that claim
- FTC may require disclosure that content is AI-generated (pending rulemaking, 2026)
- Some platforms (TikTok, YouTube) require labeling AI-generated content in specific categories (news, politics)

**Best practice:** Add "AI-generated content" to bio or video description on platforms that require it.

---

### Posting the Same Content to Multiple Platforms

**Status: ALLOWED**

Syndicating your own content is fully legal. Platform ToS restrictions only apply to that platform's own policies (which can't make you liable to laws — only affect your account).

**What gets penalized:** Platforms algorithmically suppress duplicate content. This is a reach problem, not a legal problem.

---

### Scraping Publicly Available Data for Research

**Status: RISKY — depends on source and use**

**Generally ALLOWED:**
- Scraping publicly visible posts, prices, content (not requiring login)
- Using scraped data for personal research
- Public social media posts (hiQ Labs v. LinkedIn, 2022 ruling favors scrapers of public data)

**RISKY:**
- Scraping behind login walls (violates platform ToS; Computer Fraud and Abuse Act gray area)
- Storing scraped PII (GDPR/CCPA implications)
- Using scraped emails for cold outreach without consent (CAN-SPAM compliance required)

**ILLEGAL:**
- Scraping to build a competing database and selling it without permission
- Scraping medical, financial, or government data with specific protections
- Scraping a site that has explicitly blocked your IP and you bypass the block (CFAA risk)

**Safe approach:** Use Reddit JSON API (designed for this), Twitter API v2 (within rate limits), and publicly available data only. Never bypass CAPTCHAs or login walls programmatically.

---

### Using Competitors' Brand Names in SEO Content

**Status: ALLOWED with limits**

**Allowed:**
- Comparative articles: "X vs Y" (e.g., "Convertkit vs Beehiiv")
- Mentioning competitors in reviews
- Using competitor names as SEO keywords in your content

**NOT allowed:**
- Claiming your product IS the competitor's product
- Using competitor's trademark in your domain name (trademark infringement)
- Creating false impressions about competitor products (defamation/trade libel)

---

## CATEGORY 2: EMAIL MARKETING

### Cold Email — B2B

**Status: ALLOWED in US with CAN-SPAM compliance**

CAN-SPAM Act (US) governs B2B cold email. Requirements:
1. Your email must have your real physical address
2. Must have clear unsubscribe mechanism that works within 10 business days
3. No deceptive subject lines ("RE:" or "FWD:" when it's not a reply = violation)
4. Must clearly identify as advertisement if it is one (B2B gray area — commercial email to a business contact can be less strict)

**GDPR note (EU):** Cold B2B email to EU citizens requires a "legitimate interest" basis. Mass cold email to EU targets without legitimate interest = GDPR violation. Fines up to 4% of annual revenue.

**What's allowed:**
- Buying a prospect list and emailing it (US B2B — with CAN-SPAM compliance)
- Scraping LinkedIn for emails and cold emailing (risky but widely practiced, see above)
- Automated follow-up sequences

**What's not allowed:**
- Emailing people who explicitly opted out
- Harvesting emails from websites and emailing B2C consumers without consent
- Spoofing your sender address

---

### Email List Purchasing

**Status: RISKY**

Purchasing email lists for B2C email is broadly prohibited under:
- CAN-SPAM (still requires opt-out mechanism)
- GDPR (purchased list rarely has proper consent documentation)
- Platform ToS (Mailchimp, Klaviyo will ban you for high bounce/complaint rates from purchased lists)

**For B2B only:** Purchasing lists from reputable vendors (ZoomInfo, Apollo.io) where contacts are business professionals is the standard practice. Still need CAN-SPAM compliance.

---

## CATEGORY 3: SOCIAL MEDIA GROWTH

### Engagement Pods

**Status: RISKY — platform ToS violation, not illegal**

Coordinated engagement groups where members like/comment/share each other's content:
- Not illegal (no law prohibits it)
- Violates platform ToS on X, Instagram, TikTok (inauthentic engagement)
- Risk: account suspension or reach suppression

**Safer alternative:** Real communities where members organically engage because they find value.

---

### Buying Followers

**Status: RISKY — platform ToS violation, not illegal**

- Not illegal
- Violates platform ToS universally
- Platforms routinely purge fake followers
- May constitute fraud if you use inflated numbers to attract sponsors (representing fake reach as real to get paid)

**Don't do it for business accounts.** The algorithmic damage (poor engagement ratio) lasts longer than the fake numbers help.

---

### Using Bots for Engagement

**Status: RISKY to ILLEGAL depending on use**

**RISKY (platform ToS only):**
- Auto-like, auto-follow, auto-comment bots
- Risk: account ban, no legal liability unless fraud

**ILLEGAL territory:**
- Using bots to manipulate stock prices or trading platforms (securities fraud)
- Using bots to disrupt someone else's service (CFAA — DoS)
- Using bots to create fake reviews (FTC guidelines, state consumer protection laws)
- Using bots to inflate political content (some state laws, federal election laws if political ads involved)

---

### Automating DMs

**Status: RISKY**

Sending automated DMs to people who didn't request them:
- Not illegal (CAN-SPAM covers email, not social DMs)
- Violates platform ToS on most platforms
- Instagram and Twitter aggressively detect and suspend DM automation
- If you're selling something via DM, FTC disclosure rules may apply

**Safe use:** ManyChat-style automation where someone triggers the DM by commenting or clicking — they initiated the interaction.

---

## CATEGORY 4: AFFILIATE MARKETING

### Affiliate Link Disclosure

**Status: REQUIRED BY LAW (FTC)**

The FTC requires clear disclosure when you receive compensation (money, products, services) for recommending something.

**Minimum compliant disclosure:**
- Must appear BEFORE the affiliate link (not buried in footer or "see full disclaimer page")
- Must be clear and conspicuous (can't be in tiny text or light grey)
- Language: "Disclosure: I may earn a commission if you purchase through this link" or shorter

**Common violations:**
- "(Ad)" in font so small it's missed
- Affiliate links on social posts without disclosure
- "I partnered with Brand X" without specifying it's paid
- Reviews where you got the product free without disclosing

**FTC penalties:** Up to $51,744 per violation (2026 rate). Enforcement historically focused on large accounts; small creators still face cease-and-desist letters from brand legal teams.

---

### Review Websites with Hidden Affiliate Angles

**Status: ALLOWED with disclosure**

Review sites where all recommendations are affiliate links are legal if:
- Every page with affiliate links clearly discloses the relationship
- Reviews are not fabricated (can write positive reviews, but can't make up testimonials)
- You don't manipulate rankings to favor higher-commission products without disclosure

**Safe structure:** "This site contains affiliate links. We may earn a commission when you purchase through our links. This doesn't affect our reviews." — in header or footer of every page.

---

### Coupon Sites with Expired Coupons

**Status: LEGALLY GRAY, ETHICALLY BAD**

Displaying coupon codes that don't work:
- Not illegal in most jurisdictions
- May violate platform ToS if you're a publisher partner of that brand
- Consumer protection laws in some states may apply if the deception is intentional

**Better approach:** Only list active, verified codes. Expired codes kill trust and SEO rankings.

---

## CATEGORY 5: PRODUCT AND PRICING

### AI-Generated Content Sold as Original

**Status: ALLOWED (currently) with evolving risk**

Selling AI-generated content (articles, templates, books, art) is legal in 2026 in the US.

**Copyright status (US):** AI-generated content is NOT copyrightable without significant human authorship. You can sell it, but you cannot register a copyright on pure AI output. If you extensively edit and curate AI output, the human-created portions are protectable.

**Disclosure:** No current law requires disclosing AI-generated content outside of news (journalism ethics codes) and some academic contexts. May change — EU AI Act and state laws are evolving.

---

### Drop Shipping Without Disclosing Supplier

**Status: ALLOWED**

You don't have to tell customers who manufactures or ships the product. This is standard retail practice.

**What you must do:**
- Accurately describe the product (false advertising laws)
- Ship within the timeframe you promise (FTC "30-Day Rule" — must ship within 30 days of order or notify customer)
- Honor your return policy
- Don't claim products have qualities they don't

---

### Urgency and Scarcity Marketing

**Status: RISKY if fake**

**Allowed:**
- "Sale ends Sunday" (if it actually ends Sunday)
- "Only 50 spots available" (if actually limited to 50)
- Rolling countdowns where the price actually increases

**Illegal:**
- "Offer expires in 24 hours" (evergreen countdown that resets) — FTC deceptive practices
- "Only 3 left in stock" (when you have unlimited digital products)
- Flash_sale_funnel_template.html note: the rolling deadline approach is legally risky in some jurisdictions. Use genuine time-limited sales.

**FTC enforcement:** Explicitly targets fake scarcity. Class action lawsuits have succeeded against brands using fake countdown timers.

---

### White-Label SaaS Reselling

**Status: ALLOWED**

Reselling software you license under your own brand is legal if:
- Your agreement with the underlying platform permits it (check ToS — most explicitly allow reselling/agency plans)
- You're not misrepresenting the underlying technology if asked directly
- You provide the service as described to your customers

**What's not allowed:** Claiming you built software you licensed. If a customer asks "did you build this?", you cannot lie. You can decline to disclose the underlying platform.

---

## CATEGORY 6: INTELLIGENCE GATHERING

### Monitoring Competitor Activity

**Status: ALLOWED**

- Reading competitor websites, pricing pages, social media: fully legal
- Using tools to track price changes (visualping.io type tools): fully legal
- Reverse-engineering publicly available algorithms: fully legal
- Purchasing competitor products to review them: fully legal

**NOT allowed:**
- Accessing competitor's internal systems (CFAA)
- Hiring away employees specifically to get trade secrets (trade secret law)
- Industrial espionage (obviously illegal)

---

### Using Wayback Machine / Historical Data

**Status: ALLOWED**

Archive.org's Wayback Machine is public. Using cached versions of pages for research is legal.

---

## QUICK REFERENCE TABLE

| Tactic | Legal Status | Platform ToS | Risk Level |
|--------|------------|--------------|------------|
| Multiple social accounts | Legal | Usually allowed | Low |
| AI personas (disclosed) | Legal | Allowed | Low |
| Content scraping (public) | Legal | Gray area | Medium |
| Cold email B2B (CAN-SPAM) | Legal | Allowed | Low |
| Email list purchase (B2C) | GDPR risk | Often prohibited | High |
| Engagement pods | Legal | Violates ToS | Medium |
| Buying followers | Legal | Violates ToS | Medium |
| DM bots | Legal | Violates ToS | Medium |
| FTC affiliate disclosure | Required by law | Required | HIGH |
| Fake scarcity/urgency | ILLEGAL | Violates ToS | Very High |
| White-label reselling | Legal | Usually allowed | Low |
| Competitor monitoring | Legal | Allowed | Low |
| Competitor brand in SEO | Legal (with limits) | Allowed | Low |

---

## When to Get an Actual Lawyer

These situations require professional legal advice:
- Revenue over $100K/year from affiliate marketing (FTC exposure)
- Collecting and storing user data at scale (GDPR/CCPA compliance)
- Operating in regulated industries: finance, health, legal advice
- Incorporating (even Delaware LLC decisions have tax implications)
- Any cease-and-desist letter received
- Any contract with a brand for paid promotion over $10K

**Resources:**
- EFF.org — free digital rights information
- FTC.gov/business-guidance — free FTC compliance materials
- Priori Legal or Clerky — affordable legal services for startups
