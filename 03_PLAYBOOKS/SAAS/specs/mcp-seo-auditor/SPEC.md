# RankPulse MCP -- SEO/Marketing Intelligence MCP Server

**Product Name:** RankPulse MCP
**Tagline:** "Give your AI agent SEO superpowers. Keyword research, rank tracking, site audits -- all via MCP."
**Category:** MCP Server Product (MM050) + SEO/GEO (GTM Optimization)
**Target:** Claude Code users, AI-powered marketers, indie devs, solopreneurs

---

## Product Overview

RankPulse is an MCP server that gives Claude (and any MCP-compatible AI) direct access to SEO intelligence. Instead of switching between Claude and Ahrefs/Semrush/Google Search Console, your AI agent queries SEO data directly through MCP tools. Keyword research, rank tracking, technical audits, competitor analysis -- all without leaving your AI workflow.

**Distribution:** Apify (pay-per-event) + MCPize (subscription) + Cline Marketplace (free listing)

---

## MVP Features (5 MCP Tools)

### Tool 1: `keyword_research`
```typescript
// Input
{
  query: string,          // seed keyword
  country?: string,       // default "us"
  language?: string,      // default "en"
  limit?: number          // default 20
}

// Output
{
  keywords: [{
    keyword: string,
    search_volume: number,
    difficulty: number,    // 0-100
    cpc: number,
    trend: string,         // up, down, stable
    intent: string,        // informational, commercial, navigational, transactional
    serp_features: string[] // featured snippet, people_also_ask, video, etc.
  }],
  related_questions: string[],
  related_topics: string[]
}
```

### Tool 2: `site_audit`
```typescript
// Input
{
  url: string,            // page or domain URL
  checks?: string[]       // specific checks, default all
}

// Output
{
  score: number,          // 0-100 overall health
  title_tag: { value: string, length: number, issues: string[] },
  meta_description: { value: string, length: number, issues: string[] },
  headings: { h1_count: number, h2_count: number, hierarchy_valid: boolean },
  images: { total: number, missing_alt: number, oversized: number },
  links: { internal: number, external: number, broken: number },
  mobile_friendly: boolean,
  page_speed: { lcp: number, fid: number, cls: number },
  schema_markup: { types_found: string[], missing_recommended: string[] },
  security: { https: boolean, mixed_content: boolean },
  recommendations: string[]   // prioritized fix list
}
```

### Tool 3: `rank_check`
```typescript
// Input
{
  domain: string,
  keywords: string[],     // up to 10 per call
  country?: string
}

// Output
{
  rankings: [{
    keyword: string,
    position: number | null,
    url: string,
    featured_snippet: boolean,
    serp_features: string[]
  }],
  average_position: number,
  top_10_count: number
}
```

### Tool 4: `competitor_analysis`
```typescript
// Input
{
  domain: string,         // your domain
  competitors?: string[], // auto-detect if empty
  metrics?: string[]      // traffic, keywords, backlinks
}

// Output
{
  your_domain: { traffic_estimate: number, keyword_count: number, backlinks: number },
  competitors: [{
    domain: string,
    traffic_estimate: number,
    keyword_count: number,
    backlinks: number,
    content_gap: string[], // keywords they rank for, you don't
    common_keywords: number
  }],
  opportunities: string[] // actionable gaps to exploit
}
```

### Tool 5: `content_optimizer`
```typescript
// Input
{
  url: string,            // existing page to optimize
  target_keyword: string
}

// Output
{
  current_score: number,  // content optimization score 0-100
  target_keyword_density: { current: number, recommended: number },
  missing_topics: string[],        // semantic topics to add
  missing_questions: string[],     // FAQs to include
  word_count: { current: number, recommended: number },
  readability_score: number,
  internal_link_opportunities: string[],
  schema_suggestions: string[],
  ai_citation_readiness: number    // GEO score 0-100
}
```

---

## Tech Stack

```
MCP Server:
  - TypeScript (Apify MCP template)
  - @modelcontextprotocol/sdk for MCP protocol
  - Apify SDK for hosting + billing

Data Sources:
  - DataForSEO API (keyword data, rank tracking)
  - Google PageSpeed Insights API (Core Web Vitals)
  - Custom web scraper for SERP analysis
  - Schema.org validator
  - Lighthouse CLI for audits

Hosting:
  - Apify (automatic scaling, PPE billing)
  - MCPize (subscription alternative)

Project Structure:
  src/
  ├── main.ts                    # MCP server entry
  ├── tools/
  │   ├── keyword-research.ts    # Tool 1
  │   ├── site-audit.ts          # Tool 2
  │   ├── rank-check.ts          # Tool 3
  │   ├── competitor-analysis.ts # Tool 4
  │   └── content-optimizer.ts   # Tool 5
  ├── apis/
  │   ├── dataforseo.ts          # DataForSEO wrapper
  │   ├── pagespeed.ts           # Google PSI wrapper
  │   └── scraper.ts             # Custom SERP scraper
  └── schemas/
      └── types.ts               # Shared TypeScript types
  pay_per_event.json             # Apify pricing config
  .actor/                        # Apify actor config
  package.json
```

---

## Database Schema

No database needed for the MCP server itself (stateless). For the companion dashboard (optional):

```sql
-- API usage tracking (managed by Apify)
-- User accounts (managed by Apify/MCPize)

-- Optional: Rank tracking history (if we build companion app)
CREATE TABLE rank_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain TEXT NOT NULL,
  keyword TEXT NOT NULL,
  position INTEGER,
  checked_at TIMESTAMPTZ DEFAULT now(),
  INDEX idx_domain_keyword (domain, keyword)
);
```

---

## API / MCP Tool Endpoints

MCP tools are exposed as function calls, not HTTP endpoints. The MCP SDK handles transport:

```
Tools exposed via MCP:
1. keyword_research(query, country?, language?, limit?)
2. site_audit(url, checks?)
3. rank_check(domain, keywords, country?)
4. competitor_analysis(domain, competitors?, metrics?)
5. content_optimizer(url, target_keyword)
```

For the Apify Actor (HTTP fallback):
```
POST /api/keyword-research
POST /api/site-audit
POST /api/rank-check
POST /api/competitor-analysis
POST /api/content-optimizer
```

---

## Pricing Model

### Apify Pay-Per-Event (Primary)

```json
{
  "events": [
    {
      "name": "keyword_research",
      "price_per_event": 0.05,
      "description": "Research keywords for a seed term"
    },
    {
      "name": "site_audit",
      "price_per_event": 0.10,
      "description": "Full technical SEO audit of a URL"
    },
    {
      "name": "rank_check",
      "price_per_event": 0.03,
      "description": "Check ranking for up to 10 keywords"
    },
    {
      "name": "competitor_analysis",
      "price_per_event": 0.15,
      "description": "Competitor gap analysis"
    },
    {
      "name": "content_optimizer",
      "price_per_event": 0.08,
      "description": "Content optimization recommendations"
    }
  ]
}
```

**Revenue per active user:** ~$5-$20/mo (estimated 100-400 tool calls/mo)

### MCPize Subscription (Secondary)

| Plan | Price | Calls/mo | Best For |
|------|-------|----------|----------|
| Starter | $19/mo | 500 calls | Solo bloggers |
| Pro | $49/mo | 2,000 calls | Marketers |
| Agency | $99/mo | 10,000 calls | Agencies |

---

## Landing Page Copy

### Hero

**Headline:** SEO intelligence inside your AI workflow.
**Subheadline:** RankPulse gives Claude keyword data, site audits, rank tracking, and competitor analysis via MCP. No more tab switching between AI and SEO tools.

### Use Cases

**"Hey Claude, what keywords should I target for my prayer app?"**
Claude uses RankPulse to pull keyword data, search volume, difficulty scores, and SERP features. Returns a prioritized keyword strategy in seconds.

**"Audit my landing page for SEO issues."**
Claude runs a full technical audit -- title tags, meta descriptions, schema markup, Core Web Vitals, broken links. Returns a prioritized fix list.

**"Who are my competitors and what are they ranking for that I'm not?"**
Claude analyzes competitor domains, finds content gaps, and suggests keywords to target.

### CTA
Install RankPulse MCP. First 50 calls free.

---

## Distribution Plan

| Channel | Action | Timeline |
|---------|--------|----------|
| Apify Marketplace | List as Actor + MCP server | Day 1 |
| Apify $1M Challenge | Submit before Jan 31 | Day 1 |
| MCPize | List subscription version | Week 1 |
| Cline Marketplace | Submit GitHub issue | Week 1 |
| awesome-mcp-servers | PR to punkpeye repo | Week 1 |
| MCP.so | Submit for indexing | Week 1 |
| Smithery | Submit for auto-install | Week 1 |
| Product Hunt | Launch "MCP server for SEO" | Week 2 |
| X/Twitter | Build-in-public thread | Week 1+ |
| r/SEO, r/ClaudeAI | Share tool + use cases | Week 2 |
| SEO content | "Best MCP servers for marketing" | Month 2 |

---

## Build Timeline

| Day | Task |
|-----|------|
| 1 | Apify MCP template setup + keyword_research tool |
| 2 | site_audit tool (DNS, headers, content, schema) |
| 3 | rank_check tool + competitor_analysis tool |
| 4 | content_optimizer tool + GEO scoring |
| 5 | Pay-per-event config + testing + Apify deployment |
| 6 | MCPize listing + Cline submission + landing page |
| 7 | Launch on Product Hunt + social posts |

**Total: 7 days to launch**

---

## Revenue Projections

| Month | Active Users | Tool Calls | Revenue (Apify PPE) | Revenue (MCPize) |
|-------|-------------|-----------|---------------------|------------------|
| 1 | 50 | 5,000 | $300 | $200 |
| 3 | 300 | 40,000 | $2,400 | $1,500 |
| 6 | 1,000 | 150,000 | $9,000 | $5,000 |
| 12 | 3,000 | 500,000 | $30,000 | $15,000 |

**Combined Year 1 target:** $45K+ MRR from both distribution channels

---

## Competitive Landscape

| Competitor | Price | Our Edge |
|------------|-------|----------|
| Ahrefs | $99-$999/mo | We're MCP-native. 10x cheaper for AI workflows. |
| Semrush | $129-$499/mo | We integrate directly with Claude. No tab switching. |
| Ahrefs MCP (exists) | Requires Ahrefs subscription | We're standalone, no dependency |
| Screaming Frog | $259/yr | Desktop tool. We're cloud + MCP. |
| SurferSEO | $89-$219/mo | Content-only. We do full SEO stack. |

**Our moat:** MCP-native (competitors are web-first, MCP is an afterthought). Built for AI-first workflows. PPE pricing makes it accessible to indie devs. No subscription lock-in on Apify.

---

## Internal Use Synergies

This MCP server directly serves PRINTMAXX operations:

| Use Case | How RankPulse Helps |
|----------|---------------------|
| GEO optimization | `content_optimizer` checks AI citation readiness |
| Longtail page generation | `keyword_research` feeds LEDGER/GEO_LONGTAIL_SLUGS |
| Truth page SEO | `site_audit` validates each truth page |
| App Store landing pages | `rank_check` tracks keyword rankings |
| Competitor monitoring | `competitor_analysis` weekly for all methods |
| Content farm SEO | `keyword_research` for niche content topics |

**Build for ourselves, sell to everyone else.**

---

*Spec ready to build. Start with `apify create rankpulse-mcp --template ts-mcp-proxy` and implement tools against DataForSEO API.*
