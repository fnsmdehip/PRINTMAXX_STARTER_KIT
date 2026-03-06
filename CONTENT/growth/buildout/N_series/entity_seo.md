# Entity SEO — N27

**Concept:** Google ranks entities (people, brands, organizations) not just keywords. Building your entity — establishing who you are across the web — makes all your SEO easier because Google trusts you more.
**Goal:** Get Google to recognize "PRINTMAXX" and your personal brand as known, trusted entities with associated topical authority.
**Timeline to see effects:** 60-90 days for initial entity recognition; 6 months for meaningful ranking boost
**Cost:** $0-50 (mostly manual work)

---

## What Entity SEO Means

When Google sees your name or brand, it checks its Knowledge Graph:
- Does this entity exist?
- What topics are they authoritative on?
- Which websites mention them? Are those trusted sites?
- Do all the mentions say consistent things?

If Google can answer these questions confidently, it trusts your content more and ranks it higher.

---

## Step 1: Establish Your Entity Foundation

### Google Knowledge Panel Prerequisites

You won't get a Knowledge Panel immediately, but you set the foundation by:

1. **Consistent NAP (Name, Address, Phone) across the web**
   - For personal brand: consistent Name + X handle + website URL across all platforms
   - For business entity: consistent business name, address (can use PO box), contact email

2. **Wikipedia or Wikidata presence**
   - Difficult for new entities, but Wikidata is easier
   - Create a Wikidata item for your project/product
   - Link: wikidata.org → Create a new item
   - Include: instance of (Q5 = human or Q18127 = website), official website, social media accounts

3. **Google My Business (for local service angle)**
   - If you offer local services or have any physical location: create GMB profile
   - Signals to Google that your business is real

---

## Step 2: Build Citation Network

Citations are mentions of your entity across the web. More = more entity strength.

### Tier 1 Citations (High Authority, Do First)

**Professional profiles:**
- LinkedIn profile with full bio, company, website
- Crunchbase profile (free, just fill it out)
- AngelList/Wellfound company profile
- F6S founder profile
- Product Hunt profile (complete with all projects)

**Developer profiles:**
- GitHub profile (link your website)
- dev.to author profile
- Hashnode author profile

**Media listings:**
- Clutch.co listing (for freelancers/agencies)
- GoodFirms listing
- UpCity listing

**Each profile should:**
- Have consistent name and description
- Link back to your main website (backlinks + NAP consistency)
- Have your photo/logo
- List your services/products

---

### Tier 2 Citations (Medium Authority, Do Week 2)

**Directories:**
- Trustpilot business profile
- G2 profile (if you have software)
- Capterra listing (for apps)
- AlternativeTo (list your products)
- SaaSHub profile

**Local business (even if digital-only):**
- Yelp business profile
- Better Business Bureau (free listing)
- Bing Places
- Apple Maps Connect

**Niche-specific:**
- Indie Hackers profile (with your projects listed)
- Maker Hunt
- BetaList
- AppSumo marketplace (if you ever run a deal)

---

### Tier 3 Citations (Lower Authority, Ongoing)

- Medium author bio (links back to your site)
- Substack author page
- Guest posts on any site with DA 30+ (each one adds a citation)
- Podcast appearances (your name + website mentioned)
- Press releases (free services like PR.com, PRLog, OnlinePRNews)

---

## Step 3: Topical Authority

Google's entity system also tracks WHAT topics your entity is associated with.

**Your topical cluster:**
- Cold email outreach
- Solopreneur tools
- PWA/app building
- AI automation
- Side hustle / passive income
- Faith + productivity (for @selahmoments)

**How to build topical authority:**
1. Create 10+ pieces of content around each topic you want to own
2. Internally link all pieces in a cluster to a pillar page
3. Get external links from other sites writing about those topics (even 1-2 quality links help)
4. Have consistent mentions across the web where your name + topic appear together

---

## Step 4: Schema Markup

Schema markup tells Google explicitly who you are. Add to your landing page's HTML:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "PRINTMAXX",
  "url": "https://printmaxx.surge.sh",
  "sameAs": [
    "https://twitter.com/printmaxxer",
    "https://linkedin.com/in/[your-profile]",
    "https://github.com/[your-handle]",
    "https://www.producthunt.com/@[your-handle]"
  ],
  "knowsAbout": ["cold email", "solopreneur tools", "PWA development", "AI automation"],
  "description": "Solopreneur tools and systems for indie builders"
}
</script>
```

For your software products, use Product schema:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "PrayerLock",
  "applicationCategory": "LifestyleApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "description": "Prayer tracking and lock screen reminder app"
}
</script>
```

---

## Step 5: Consistent Bio Language

Across every platform, use the same 1-2 sentence bio so Google's entity resolution consistently maps mentions to you:

**Long bio (LinkedIn, GitHub, Medium):**
"I build tools for solopreneurs — cold email systems, PWAs, and AI automation workflows. Sharing everything at [website]."

**Short bio (Twitter, Instagram):**
"building tools for solopreneurs. cold email, AI, apps."

**Why consistency matters:** If your Twitter says "AI entrepreneur" but your LinkedIn says "cold email consultant" and your GitHub says "developer" — Google has a hard time resolving these into one entity. Consistent language = clear entity signal.

---

## Measuring Entity SEO Progress

**Google Search Console — Queries report:**
- After 60-90 days: are you seeing your brand name appear as a query?
- Are clicks going up when people search your brand name?

**Google Search your brand name:**
- Do you see a Knowledge Panel? (won't have one early, but note when it appears)
- Are your profiles showing in results?
- Are the results consistent and positive?

**Entity tracking tools:**
- kalicube.pro (free tier): tracks entity signals, Google Business Profile, Knowledge Panel status
- Brand24 ($49/mo): tracks brand mentions across the web

**Monthly check:**
1. Google your brand name: what do you see?
2. Check Google Search Console branded queries
3. Count how many new citations were built that month (track in spreadsheet)
4. Check if any new Knowledge Panel or Google entity features appeared

---

## Priority Action List (30-Day Sprint)

**Week 1:**
- [ ] Create/complete Crunchbase, AngelList, F6S profiles
- [ ] Complete LinkedIn profile with full bio + website + all experience
- [ ] Add schema markup to your main landing page
- [ ] Add consistent bio to all social profiles

**Week 2:**
- [ ] Create Product Hunt profile + list all products
- [ ] G2/Capterra/AlternativeTo listings for each app
- [ ] Indie Hackers profile with projects listed
- [ ] Create Wikidata item for your brand

**Week 3:**
- [ ] Guest post or interview on any site DA 40+
- [ ] Press release on free PR services
- [ ] Submit to 5 niche-specific directories
- [ ] Create dev.to author profile + publish 1 article

**Week 4:**
- [ ] Review all citations for NAP consistency
- [ ] Check Google Search Console for brand queries
- [ ] Set up Brand24 or Google Alerts for brand mentions
- [ ] Identify gaps (which Tier 1 citations are missing?)

**Target at 30 days:** 30+ consistent citations, schema markup live, Google beginning to recognize entity.
