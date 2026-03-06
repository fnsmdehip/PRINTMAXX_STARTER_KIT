# MCPHub monetization plan

## the model

MCP servers are free to list. always will be. the money comes from visibility, verification, and hosting.

---

## tier breakdown

### free tier - $0
- basic listing in directory
- search/filter visibility
- GitHub link, install command
- category placement
- this is the default. every server gets this.

### featured listing - $29/mo
- pinned to top of category
- highlighted card with accent border
- "featured" badge on card
- shows up in "featured servers" section on homepage
- priority in search results
- target: server authors who want downloads/adoption

### verified badge - $9/mo
- "verified" badge (we tested it, it works, docs are solid)
- manual review of docs, install process, basic functionality
- trust signal for users who don't want to debug broken servers
- re-verified monthly
- target: serious maintainers who want credibility

### enterprise - $99/mo
- everything in featured + verified
- custom integration guide written by us
- priority support channel (Discord or email)
- analytics dashboard (impressions, clicks, installs)
- co-marketing (featured in newsletter, social posts)
- target: companies building commercial MCP servers

### affiliate - hosting referrals
- 20% commission on hosting referral signups
- MCP servers need to run somewhere. most devs don't want to self-host.
- partner with: Railway, Render, Fly.io, Cloudflare Workers
- "deploy this server" button on each listing
- passive revenue that scales with directory traffic

---

## revenue projections

### 100 listed servers (month 2-3)
| source | conversion | revenue/mo |
|--------|-----------|------------|
| featured listings | 5% = 5 servers | $145 |
| verified badges | 8% = 8 servers | $72 |
| enterprise | 1% = 1 server | $99 |
| hosting affiliate | 10 referrals | $50 |
| **total** | | **$366/mo** |

### 500 listed servers (month 6-8)
| source | conversion | revenue/mo |
|--------|-----------|------------|
| featured listings | 5% = 25 servers | $725 |
| verified badges | 8% = 40 servers | $360 |
| enterprise | 2% = 10 servers | $990 |
| hosting affiliate | 80 referrals | $400 |
| **total** | | **$2,475/mo** |

### 1,000 listed servers (month 12+)
| source | conversion | revenue/mo |
|--------|-----------|------------|
| featured listings | 5% = 50 servers | $1,450 |
| verified badges | 8% = 80 servers | $720 |
| enterprise | 2% = 20 servers | $1,980 |
| hosting affiliate | 200 referrals | $1,000 |
| newsletter sponsorship | 2 sponsors | $500 |
| **total** | | **$5,650/mo** |

---

## why this works

1. **MCP ecosystem is growing fast.** Anthropic, OpenAI, and the open source community are all pushing MCP. server count will 10x in 2026.
2. **discovery is a real problem.** there's no central place to find MCP servers. awesome-mcp lists exist but they're GitHub READMEs with no search, no install commands, no verification.
3. **server authors want distribution.** building an MCP server is easy. getting people to use it is hard. featured listings solve this.
4. **hosting is a natural upsell.** every MCP server needs to run somewhere. affiliate commissions are passive.
5. **low cost to run.** static site on surge.sh or Cloudflare Pages. $0 hosting cost. the margins are almost 100%.

---

## payment infrastructure

- Stripe for subscriptions (featured, verified, enterprise)
- Stripe Connect or manual for affiliate payouts
- start collecting manually (email invoices) until volume justifies Stripe integration
- MVP: accept payments via Stripe Payment Links, no backend needed

---

## expansion plays (month 6+)

- **MCP server hosting** - one-click deploy, we host it for you. $5-20/mo per server. this is the real money.
- **MCP server templates** - starter kits for building servers. $29-49 one-time or $9/mo for updates.
- **MCP consulting** - help companies build custom servers. $150-300/hr.
- **API access** - programmatic access to the directory. free tier + paid for bulk/commercial use.
