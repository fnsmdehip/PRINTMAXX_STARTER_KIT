# C11 SEO, Site Architecture: Content Hub Strategy

---

## The Hub-and-Spoke Model

One pillar page (broad topic, 3,000-5,000 words) surrounded by cluster pages (specific angles, 1,500-2,000 words each). Every spoke links back to the hub. The hub links to every spoke. Google reads this as topical authority, ranks all pages higher.

```
PILLAR: "How to make money online in 2025"
├── SPOKE: Make money on Etsy digital downloads
├── SPOKE: Best affiliate programs for beginners
├── SPOKE: How to make money with AI tools
├── SPOKE: How to start freelancing with no experience
├── SPOKE: Faceless YouTube channel guide
├── SPOKE: TikTok affiliate marketing beginners
├── SPOKE: Make money on Fiverr
└── SPOKE: Passive income ideas that work
```

---

## Recommended Domain Strategy

**Option A, Niche focus** (higher topical authority, faster to rank):
- `solopreneurkit.com`, all solopreneur methods
- `printmaxxer.com`, branded authority play
- `onlineincomestack.com`, broad but focused

**Option B, Multi-niche authority site** (more traffic ceiling, slower):
- `incomemethods.com`, covers all niches
- Risk: takes longer to establish topical authority per niche

**Recommendation:** Option A with one tight niche first. Add second niche after 50+ indexed pages.

---

## Full Site Architecture

### Level 1, Homepage
- URL: `domain.com/`
- Purpose: Authority signal, links to all hubs
- Content: Brief intro + links to 4 main content hubs
- No need to rank this page, it feeds PageRank to hubs

### Level 2, Pillar Pages (Content Hubs)
4 pillar pages, one per niche:

**Hub 1: Money Methods**
- URL: `domain.com/make-money-online/`
- Target keyword: "how to make money online 2025"
- Word count: 4,000-5,000 words
- Content: complete overview of all methods covered in spokes
- Internal links: to all 15 spokes in this hub

**Hub 2: AI Tools**
- URL: `domain.com/ai-tools/`
- Target keyword: "best AI tools for business 2025"
- Word count: 3,500-4,500 words
- Content: overview of AI income methods + tool comparisons

**Hub 3: Content Creation**
- URL: `domain.com/content-creation/`
- Target keyword: "how to make money creating content"
- Word count: 3,500-4,000 words
- Content: YouTube, TikTok, newsletter, podcast methods

**Hub 4: Ecommerce & Selling**
- URL: `domain.com/sell-online/`
- Target keyword: "how to sell products online"
- Word count: 4,000-4,500 words
- Content: Etsy, dropshipping, POD, digital products

### Level 3, Cluster Pages (Spokes)
50 cluster pages (20 written from outlines + 30 additional):

**Money Methods cluster (15 pages):**
```
/make-money-online/etsy-digital-downloads/
/make-money-online/affiliate-programs-beginners/
/make-money-online/dropshipping-guide/
/make-money-online/freelancing-no-experience/
/make-money-online/notion-templates/
/make-money-online/fiverr-beginners/
/make-money-online/cold-email-templates/
/make-money-online/passive-income/
/make-money-online/start-newsletter/
/make-money-online/gumroad-alternatives/
/make-money-online/make-money-blogging/
/make-money-online/print-on-demand/
/make-money-online/digital-product-business/
/make-money-online/side-hustle-introverts/
/make-money-online/one-person-business/
```

**AI Tools cluster (13 pages):**
```
/ai-tools/chatgpt-make-money/
/ai-tools/best-ai-tools-small-business/
/ai-tools/ai-tools-no-coding/
/ai-tools/mcp-servers-explained/
/ai-tools/chatbot-for-website/
/ai-tools/claude-vs-chatgpt/
/ai-tools/best-ai-writing-tools/
/ai-tools/midjourney-make-money/
/ai-tools/eleven-labs-review/
/ai-tools/ai-tools-content-creators/
/ai-tools/automate-small-business-ai/
/ai-tools/n8n-vs-zapier/
/ai-tools/ai-tools-pay-you/
```

**Content Creation cluster (10 pages):**
```
/content-creation/faceless-youtube-channel/
/content-creation/tiktok-affiliate-marketing/
/content-creation/best-tools-solopreneurs/
/content-creation/grow-instagram-without-face/
/content-creation/reddit-marketing-small-business/
/content-creation/monetize-newsletter-1000-subscribers/
/content-creation/pinterest-affiliate-marketing/
/content-creation/best-time-post-tiktok/
/content-creation/youtube-shorts-get-views/
/content-creation/linkedin-lead-generation/
```

**Ecommerce cluster (12 pages):**
```
/sell-online/shopify-alternatives/
/sell-online/etsy-vs-shopify-digital/
/sell-online/printify-vs-printful/
/sell-online/amazon-kdp-worth-it/
/sell-online/winning-dropshipping-products/
/sell-online/best-niches-print-on-demand/
/sell-online/tiktok-shop-vs-amazon/
/sell-online/sell-etsy-without-making/
/sell-online/erank-vs-marmalead/
/sell-online/build-email-list-zero/
/sell-online/landing-page-converts/
/sell-online/best-digital-products-sell/
```

### Level 4, Supporting Pages
- `/tools/`, recommended tools page (heavy affiliate links)
- `/resources/`, free downloads (lead magnet landing pages)
- `/about/`, authority signal
- `/start-here/`, guides new visitors to right content

---

## URL Structure Rules
1. All lowercase, no uppercase
2. Hyphens not underscores
3. Short: under 60 characters
4. Keyword in URL, no stop words if possible
5. No dates (content stays evergreen)
6. No trailing slash inconsistency (pick one, stick with it)

**Good:** `/make-money-online/etsy-digital-downloads/`
**Bad:** `/2025/01/15/how-to-make-money-on-etsy-selling-your-digital-downloads/`

---

## Technical SEO Requirements

### Site Speed Targets
- First Contentful Paint: under 1.5s
- LCP: under 2.5s
- CLS: under 0.1
- Use: lightweight WordPress theme (Kadence, GeneratePress) or static site (Astro, Hugo)

### Platform Recommendation
- **WordPress + Kadence theme:** $3-15/mo hosting (Hostinger/Cloudways), fastest to set up
- **Astro (static):** free hosting on Vercel/Netlify, fastest site speed, requires coding
- **Ghost:** $9/mo, best for newsletter + blog combo

### Essential Plugins/Config (WordPress)
- RankMath or Yoast: on-page SEO
- WP Rocket or Perfmatters: speed optimization
- Cloudflare free: CDN + bot protection
- Short Pixel: image compression

### Schema Markup (Add to Every Article)
```json
{
  "@type": "Article",
  "headline": "[Article Title]",
  "datePublished": "2025-01-01",
  "dateModified": "2025-01-01",
  "author": {
    "@type": "Person",
    "name": "Site Author"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Site Name"
  }
}
```

---

## Content Production Schedule

### Month 1 (Foundation)
- Week 1: Build site, configure technical SEO
- Week 2: Publish Hub 1 (Money Methods pillar)
- Week 3: Publish 3 Phase 1 cluster articles (KD under 22)
- Week 4: Publish 3 more Phase 1 cluster articles

### Month 2 (Scaling)
- Publish 10-12 cluster articles (3x/week)
- Add internal links to all Month 1 content
- Set up email list capture with lead magnet

### Month 3 (Authority Push)
- Complete all 50 cluster articles
- Begin Phase 2 keyword targets
- First backlink outreach (link to competitor resource pages)

### Month 4-6 (Compound)
- 3-5 new articles/week
- Update Month 1-2 articles with fresh data
- Build 5-10 backlinks via HARO, guest posts, resource pages

---

## Competitor Sites to Study

| Site | Estimated Traffic | Why Study |
|------|-----------------|-----------|
| nichepursuits.com | 400K/mo | Affiliate review + content farm model |
| incomeschool.com | 200K/mo | Beginner money methods, low KD targeting |
| sidehustlenation.com | 350K/mo | Side hustle angle, Pinterest traffic |
| smartpassiveincome.com | 500K/mo | Newsletter + affiliate combination |
| shoutmeloud.com | 600K/mo | Large content farm, broad coverage |

**What they all share:**
1. Pillar + cluster content structure
2. High internal link density
3. Strong lead magnet capturing emails
4. 200-500+ published articles
5. Consistent publishing (2-4x/week for years)

---

## Revenue Milestones by Site Size

| Articles Published | Est Monthly Traffic | Est Revenue |
|-------------------|--------------------|-----------:|
| 20 articles | 500-2K visitors | $50-200/mo |
| 50 articles | 3K-10K visitors | $300-1,000/mo |
| 100 articles | 10K-30K visitors | $1,000-3,000/mo |
| 200 articles | 30K-80K visitors | $3,000-8,000/mo |
| 500 articles | 100K-300K visitors | $10,000-30,000/mo |

*Revenue mix: display ads (Mediavine at 50K+ sessions) + affiliate commissions + email list monetization*
