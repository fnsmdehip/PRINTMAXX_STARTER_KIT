# MCP Marketplace Expansion — Next 30 Servers

**Context:** Model Context Protocol (MCP) is Anthropic's open standard for giving Claude tools/context. Servers published to the MCP ecosystem get indexed by Claude.ai, Cursor, Zed, and every Claude-based agent. Early movers in high-demand categories will dominate search results for the next 18+ months.

**Strategy:** Build servers in 3 categories:
1. **Monetizable data** (APIs people pay $50-500/mo to access → you wrap and resell)
2. **Workflow automation** (common operations that agents need repeatedly)
3. **Business intelligence** (competitive analysis, market data, financial data)

---

## Priority Tier 1 — Build First (Highest Search Demand)

### Server 1: Apollo.io MCP
**What it does:** Search and enrich B2B leads directly from Claude conversations
**Tools to expose:**
- `search_people(query, filters)` — search by job title, company, industry, location
- `search_companies(query, filters)` — find companies by size, revenue, tech stack
- `enrich_person(email_or_linkedin)` — get full profile from email or LinkedIn URL
- `enrich_company(domain)` — company info, employee count, funding, tech stack
- `create_sequence(contact_id, sequence_id)` — add to outreach sequence
- `get_email_credits()` — check remaining credits

**Who needs it:** SDRs, recruiters, cold emailers, growth hackers using Claude for outreach
**Why it wins:** Apollo is the #1 B2B contact database. no MCP server exists yet.
**Build time:** 4-6 hours
**Monetization:** $29/mo subscription OR $97 one-time purchase on Gumroad/Whop

---

### Server 2: Ahrefs MCP
**What it does:** SEO intelligence directly in Claude — keyword research, backlink analysis, site audits
**Tools to expose:**
- `keyword_overview(keyword, country)` — volume, KD, CPC, SERP features
- `keywords_for_site(domain, limit)` — what keywords a domain ranks for
- `backlinks_for_site(domain, limit)` — who links to a domain
- `site_audit_summary(domain)` — health score, errors, warnings
- `content_gap(domain, competitors)` — keywords competitors rank for that you don't
- `top_pages(domain, by_traffic)` — highest traffic pages

**Who needs it:** SEOs, content marketers, agency owners doing competitor research
**Why it wins:** Ahrefs API is $500/mo+ — wrapper makes it conversational
**Build time:** 6-8 hours
**Monetization:** $49/mo (partial API cost passthrough)

---

### Server 3: Notion MCP (Enhanced)
**What it does:** Full Notion read/write from Claude — not just basic queries but full database operations
**Tools to expose:**
- `search_pages(query)` — find pages by title or content
- `create_page(parent_id, title, content)` — create new pages with structured content
- `update_page(page_id, properties)` — update database properties
- `query_database(database_id, filter, sort)` — full filter+sort query
- `append_blocks(page_id, blocks)` — append content to existing page
- `create_database(parent_id, schema)` — create new database with schema
- `bulk_create_pages(database_id, rows[])` — batch create multiple database entries

**Why it wins over existing Notion MCP:** existing ones are read-only or have limited write. this is full CRUD with batch operations.
**Build time:** 4-6 hours
**Monetization:** free tier (drives adoption) → $14/mo Pro for bulk operations + webhooks

---

### Server 4: Linear MCP
**What it does:** Full project management operations for engineering teams via Claude
**Tools to expose:**
- `create_issue(team_id, title, description, priority, assignee)` — create issue
- `update_issue(issue_id, fields)` — update any field
- `list_issues(team_id, filter)` — list by assignee/priority/status/label
- `create_project(team_id, name, description)` — create project
- `get_cycle_issues(cycle_id)` — get all issues in current sprint
- `move_issue_to_cycle(issue_id, cycle_id)` — assign to sprint
- `add_comment(issue_id, body)` — comment on issue
- `get_team_members(team_id)` — list team members

**Who needs it:** engineering teams using Claude for sprint planning, ticket triage, standup summaries
**Build time:** 4-6 hours
**Monetization:** free (builds reputation) → $19/mo Pro for webhooks + Slack notifications

---

### Server 5: Shopify MCP
**What it does:** Full e-commerce operations via Claude — products, orders, customers, analytics
**Tools to expose:**
- `list_products(limit, status)` — get product catalog
- `create_product(title, description, price, inventory)` — add new product
- `get_orders(status, date_range, limit)` — fetch orders with filters
- `update_order(order_id, fulfillment_status)` — mark fulfilled
- `get_customers(query, limit)` — search customers
- `get_analytics(metric, date_range)` — revenue, conversion, AOV
- `create_discount(type, value, conditions)` — create discount code
- `list_collections(limit)` — get product collections
- `inventory_adjustment(variant_id, quantity)` — adjust stock

**Who needs it:** Shopify store owners, e-commerce VAs, agencies managing multiple stores
**Build time:** 6-8 hours
**Monetization:** $29/mo per store, $79/mo for agency (multi-store)

---

### Server 6: Stripe MCP (Enhanced Operations)
**What it does:** Full payment operations via Claude — not just reading, but creating
**Tools to expose:**
- `create_payment_link(amount, description, metadata)` — instant payment link
- `create_invoice(customer_id, items)` — send invoice
- `search_customers(query)` — find customers by email, name, metadata
- `get_revenue_summary(date_range)` — MRR, ARR, churn, new revenue
- `list_subscriptions(status, customer_id)` — active subscriptions
- `cancel_subscription(subscription_id, reason)` — cancel with reason
- `create_coupon(percent_off, duration)` — create discount
- `get_failed_charges(date_range)` — failed payments for dunning
- `update_subscription(subscription_id, price_id)` — upgrade/downgrade

**Build time:** 4-5 hours
**Monetization:** free (Stripe users are devs → strong install base → reputation)

---

## Priority Tier 2 — Build Second (High Value, Moderate Demand)

### Server 7: Google Analytics 4 MCP
**Tools:** get_report(property_id, metrics, dimensions, date_range), get_realtime(property_id), compare_periods(property_id, metric, period1, period2), get_top_pages(property_id, limit), get_traffic_sources(property_id, date_range), get_conversions(property_id, event_name)
**Who needs it:** marketers, agencies, founders checking metrics
**Build time:** 5-7 hours

### Server 8: Klaviyo MCP
**Tools:** search_profiles(email_or_query), get_flow_analytics(flow_id), create_segment(conditions), send_campaign(campaign_id, segment_id), get_list_growth(list_id, date_range), get_revenue_attribution(date_range)
**Who needs it:** e-commerce email marketers
**Build time:** 5-7 hours

### Server 9: HubSpot MCP (Enhanced)
**Tools:** create_contact(properties), create_deal(pipeline, stage, amount, contact_id), update_deal_stage(deal_id, stage), search_contacts(query), get_pipeline_summary(pipeline_id), schedule_activity(contact_id, type, date), create_task(contact_id, title, due_date)
**Who needs it:** sales teams, agencies, SDRs
**Build time:** 5-7 hours

### Server 10: Calendly MCP
**Tools:** get_availability(event_type, date_range), create_event_type(name, duration, location), list_scheduled_events(status, date_range), cancel_event(event_id, reason), get_event_analytics(event_type_id, date_range)
**Who needs it:** consultants, coaches, sales teams scheduling demos
**Build time:** 3-4 hours

### Server 11: Beehiiv MCP
**Tools:** create_post(title, content, publish_date), get_subscriber_count(publication_id), search_subscribers(query), get_post_analytics(post_id), create_automation_email(trigger, content), get_growth_data(publication_id, date_range)
**Who needs it:** newsletter operators
**Build time:** 3-4 hours

### Server 12: Webflow MCP
**Tools:** list_collections(site_id), create_item(collection_id, fields), update_item(item_id, fields), publish_site(site_id), get_form_submissions(site_id, form_id, date_range), update_page_seo(page_id, title, description)
**Who needs it:** Webflow developers, agencies
**Build time:** 5-6 hours

### Server 13: Intercom MCP
**Tools:** search_conversations(query, status), reply_to_conversation(conversation_id, message), create_note(conversation_id, note), list_users(segment_id), get_conversation_analytics(date_range)
**Who needs it:** customer success teams, support agents
**Build time:** 4-5 hours

### Server 14: Loom MCP
**Tools:** list_videos(folder_id), get_video_transcript(video_id), search_videos(query), create_folder(name), share_video(video_id, email), get_video_analytics(video_id)
**Who needs it:** teams using Loom for async communication
**Build time:** 3-4 hours

### Server 15: ClickUp MCP (Enhanced)
**Tools:** create_task(list_id, name, description, priority, assignees, due_date), update_task_status(task_id, status), get_tasks(list_id, assignee, status, due_date), create_doc(space_id, title, content), get_time_tracked(task_id), set_task_priority(task_id, priority)
**Who needs it:** ClickUp power users (large market)
**Build time:** 5-7 hours

---

## Priority Tier 3 — Build Third (Niche but High-Value)

### Server 16: Expensify MCP
**Tools:** create_expense(amount, merchant, date, category), submit_report(expenses[]), get_report_status(report_id), get_expense_analytics(date_range, category)
**Who needs it:** accountants, remote teams managing expenses
**Build time:** 3-4 hours

### Server 17: QuickBooks MCP
**Tools:** create_invoice(customer_id, items), get_profit_loss(date_range), create_expense(vendor, amount, account), search_customers(query), get_unpaid_invoices(), reconcile_account(account_id)
**Who needs it:** accountants, small business owners
**Build time:** 6-8 hours (complex OAuth)

### Server 18: Typeform MCP
**Tools:** list_forms(page), get_responses(form_id, date_range, limit), get_response_analytics(form_id), create_form(title, fields), export_responses_csv(form_id, date_range)
**Who needs it:** researchers, lead gen operators
**Build time:** 3-4 hours

### Server 19: Figma MCP (Read-Enhanced)
**Tools:** get_file(file_id), list_files(project_id), get_comments(file_id), get_component_library(team_id), export_frame(file_id, frame_id, format), get_version_history(file_id)
**Who needs it:** designers, front-end developers
**Build time:** 4-5 hours

### Server 20: Twitter/X MCP (Advanced)
**Tools:** search_tweets(query, sort, date_range), get_user_tweets(username, count), get_tweet_analytics(tweet_id), schedule_tweet(content, datetime), get_trending_topics(location), search_users(query, min_followers)
**Who needs it:** social media managers, growth hackers, researchers
**Build time:** 5-7 hours (rate limits tricky)

### Server 21: Reddit MCP
**Tools:** search_posts(query, subreddit, sort, time_filter), get_comments(post_id, limit), get_subreddit_hot(subreddit, limit), search_subreddits(query), get_user_posts(username), get_trending(category)
**Who needs it:** researchers, marketers, community managers
**Build time:** 3-4 hours (JSON API = no auth needed for read)

### Server 22: Lemon Squeezy MCP
**Tools:** list_products(store_id), get_order(order_id), list_customers(store_id), get_revenue_summary(store_id, date_range), create_discount(percent, code, expires_at), get_subscription_analytics(store_id)
**Who needs it:** digital product creators using LemonSqueezy
**Build time:** 4-5 hours

### Server 23: Gumroad MCP
**Tools:** list_products(), get_sales(product_id, date_range), search_customers(query), get_analytics_summary(date_range), create_offer_code(product_id, percent_off, max_uses)
**Who needs it:** Gumroad sellers (huge community)
**Build time:** 3-4 hours

### Server 24: Whop MCP
**Tools:** list_companies(), get_members(company_id, status), get_revenue(company_id, date_range), create_pass(company_id, name, price, duration), cancel_membership(member_id, reason)
**Who needs it:** Whop community and product operators
**Build time:** 4-5 hours

### Server 25: ProductHunt MCP
**Tools:** search_products(query, category, date_range), get_product(product_id), get_today_launches(limit), search_makers(query), get_upcoming_products(category), get_product_comments(product_id)
**Who needs it:** startup founders, VCs, growth teams
**Build time:** 3-4 hours

---

## Priority Tier 4 — Financial Intelligence Servers

### Server 26: Polygon.io MCP (Stock Data)
**Tools:** get_ticker(symbol), get_ohlc(symbol, from_date, to_date, timespan), get_news(symbol, limit), search_tickers(query, market, type), get_financials(symbol, type), get_snapshot(symbols[])
**Who needs it:** algo traders, quant analysts, finance blogs
**Build time:** 4-5 hours
**Monetization:** premium tier ($29/mo for real-time data operations)

### Server 27: Alpaca MCP (Automated Trading)
**Tools:** get_account(), get_positions(), place_order(symbol, side, qty, order_type), cancel_order(order_id), get_portfolio_history(period, timeframe), get_market_hours(), get_bars(symbol, timeframe, limit)
**Who needs it:** algo traders running bots on Claude
**Build time:** 5-6 hours
**Note:** paper trading first — real money trading needs user-side setup

### Server 28: CoinGecko MCP
**Tools:** get_price(ids, currencies), get_coin_data(coin_id), get_trending(), search_coins(query), get_market_chart(coin_id, vs_currency, days), get_global_market_data()
**Who needs it:** crypto traders, DeFi analysts, newsletter writers
**Build time:** 2-3 hours (free API, easy to wrap)

### Server 29: Federal Reserve (FRED) MCP
**Tools:** get_series(series_id, date_range), search_series(query, limit), get_releases(date_range), get_categories(), get_economic_data(indicator_list)
**Who needs it:** economists, macro investors, researchers
**Build time:** 3-4 hours

### Server 30: SimilarWeb MCP
**Tools:** get_website_overview(domain), get_traffic_sources(domain), get_top_competitors(domain, limit), get_keyword_rankings(domain, limit), get_audience_data(domain), compare_domains(domains[])
**Who needs it:** competitive intelligence, market research
**Build time:** 4-5 hours (requires API key)

---

## Build Stack (All Servers)

**Language:** TypeScript (Node.js)
**Framework:** `@modelcontextprotocol/sdk` (official Anthropic SDK)
**Template:**
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "server-name", version: "1.0.0" }, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "tool_name",
      description: "What it does",
      inputSchema: {
        type: "object",
        properties: {
          param: { type: "string", description: "..." }
        },
        required: ["param"]
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "tool_name") {
    const { param } = request.params.arguments as { param: string };
    // API call here
    return { content: [{ type: "text", text: JSON.stringify(result) }] };
  }
  throw new Error("Unknown tool");
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Publishing:**
1. npm publish `@yourname/mcp-apollo` etc.
2. Submit to smithery.ai (MCP server directory)
3. Submit to mcp.so
4. PR to `modelcontextprotocol/servers` GitHub repo (official listing)
5. Post on r/ClaudeAI, r/anthropic, Indie Hackers

---

## Revenue Model

### Option A: npm + Subscription
- Publish on npm (free)
- Gate advanced tools behind API key check
- Sell API keys via Stripe ($9-29/mo)
- Best for: servers wrapping APIs people already pay for

### Option B: Gumroad / Whop One-Time
- Sell as downloadable with instructions
- Price: $19-47 one-time
- Best for: servers that are pure automation (no ongoing API cost)

### Option C: Free (Traffic Play)
- Publish open source
- README links to your other products
- Best for: high-search-volume servers (Notion, GitHub) where downloads = brand awareness

### Revenue Projections

| Servers | Avg Downloads/Mo | Paid Conversion | Avg Revenue/User | MRR |
|---------|-----------------|-----------------|-----------------|-----|
| 5 servers | 200 | 5% | $19 | $950 |
| 10 servers | 500 | 5% | $22 | $2,750 |
| 20 servers | 1,200 | 5% | $25 | $7,500 |
| 30 servers | 2,500 | 5% | $25 | $15,625 |

**First-mover advantage is real:** smithery.ai shows total installs publicly. servers with 1,000+ installs get dramatically more new installs (social proof spiral). build fast, publish fast, collect installs before competitors.

---

## 30-Day Build Sprint

| Week | Servers to Build | Time | Priority |
|------|-----------------|------|----------|
| 1 | Apollo, Notion (enhanced), Shopify, Linear | 20 hours | Tier 1 |
| 2 | Stripe (enhanced), GA4, Klaviyo, HubSpot | 22 hours | Tier 2 |
| 3 | Beehiiv, Lemon Squeezy, Gumroad, Reddit | 14 hours | Tier 3 |
| 4 | Polygon.io, CoinGecko, ProductHunt, Twitter | 17 hours | Tier 3-4 |

**After 30 days:** 16 servers published, first installs rolling in, foundation for 30-server library by month 3
