# Proxy Provider Comparison (2026)

Full comparison for social automation and scraping.

---

## Residential Proxies

| Provider | Min Price | Pool Size | Sticky Sessions | Best For |
|----------|-----------|-----------|-----------------|----------|
| **Soax** | $6.60/GB | 8.5M+ IPs | Up to 30min | Budget, clean IPs |
| **Smartproxy (Decodo)** | $12.50/GB | 55M+ IPs | Up to 30min | Social media |
| **Bright Data** | $15/GB | 72M+ IPs | Unlimited | Enterprise, best quality |
| **IPRoyal** | $7/GB | 2M+ IPs | Up to 24hr | Budget alternative |
| **Oxylabs** | $15/GB | 100M+ IPs | Up to 30min | Enterprise |
| **NetNut** | $15/GB | 52M+ IPs | Rotating | Sneaker/retail |
| **Webshare** | $5/GB | 30M+ IPs | Up to 30min | Super budget |
| **PacketStream** | $1/GB | P2P network | Limited | Cheapest (risky) |

---

## Soax vs Decodo (Smartproxy) - Head to Head

| Feature | Soax | Decodo (Smartproxy) |
|---------|------|---------------------|
| **Min price** | $6.60/GB | $12.50/GB |
| **Pool size** | 8.5M | 55M |
| **Geo targeting** | Country, city, ISP | Country, city, ASN |
| **Sticky sessions** | 30 min max | 30 min max |
| **Dashboard** | Better | Good |
| **API** | Yes | Yes |
| **Mobile proxies** | Yes ($$$) | Yes ($$$) |
| **Support** | Good | Good |
| **IP quality** | Very clean | Clean |
| **Best for** | Budget automation | Scale, social |

### When to use Soax:
- Budget is tight
- Need clean IPs (low abuse)
- Scraping or research
- Testing before scaling

### When to use Decodo:
- Running many accounts
- Need larger IP pool
- Want more geo options
- Social media at scale

### My take:
**Start with Soax** ($6.60/GB cheaper), switch to Decodo if you hit IP quality issues. Most people won't need to switch.

---

## Mobile Proxies (Premium)

For high-value accounts that can't get banned.

| Provider | Price | Type | Best For |
|----------|-------|------|----------|
| **Soax Mobile** | $150/mo | Rotating | Budget mobile |
| **Smartproxy Mobile** | $200/mo | Rotating | Scale |
| **Proxy-Seller** | $90/mo | Dedicated | Single account |
| **AirProxy** | $100/mo | Dedicated | High value |
| **The Social Proxy** | $90/mo | Dedicated | Social focused |
| **ProxyGuys** | $100/mo | Dedicated | US mobile |

**When mobile proxies matter:**
- Main brand accounts you can't lose
- Accounts with monetization enabled
- After a ban, when rebuilding

**When residential is fine:**
- Test accounts
- Burner accounts
- Scraping

---

## Datacenter Proxies (Cheapest)

For scraping, NOT for social media.

| Provider | Price | Use Case |
|----------|-------|----------|
| **Webshare** | $5.50/mo (10 IPs) | General scraping |
| **Proxy-Cheap** | $0.50/IP | Bulk scraping |
| **Smartproxy DC** | $7/mo (100 IPs) | Fast scraping |
| **BuyProxies** | $2/IP | Rotating |

**Warning:** Datacenter IPs get detected instantly on social platforms. Only use for:
- Web scraping (non-social)
- SEO tools
- Price monitoring
- Public data collection

---

## ISP Proxies (Middle Ground)

Datacenter speed + residential legitimacy.

| Provider | Price | Pool | Notes |
|----------|-------|------|-------|
| **Bright Data ISP** | $17/GB | Large | Best quality |
| **Smartproxy ISP** | $14/mo (2GB) | Growing | Good value |
| **Oxylabs ISP** | $15/GB | Large | Enterprise |
| **IPRoyal ISP** | $2.50/IP | Limited | Budget |

**When to use ISP:**
- Need speed + legitimacy
- Running automation 24/7
- Don't want residential costs
- Accounts somewhat established

---

## Setup Recommendations

### Budget Setup (~$50/mo)
```
Primary: Soax residential 5GB ($33)
Use for: Account warming, light posting
Backup: Home IP for main accounts
```

### Standard Setup (~$150/mo)
```
Primary: Soax residential 10GB ($66)
Secondary: Decodo residential 5GB ($62.50)
Use for: Multi-account management
Strategy: Soax for new accounts, Decodo for established
```

### Scale Setup (~$400/mo)
```
Primary: Decodo residential 20GB ($200)
Mobile: 2x dedicated mobile ($180)
Use for: Full automation, many accounts
Strategy: Mobile for main accounts, residential for rest
```

---

## Proxy Assignment Strategy

### Rule 1: One proxy per account
Never share proxies between accounts. Platforms detect this.

### Rule 2: Geographic consistency
If account was created in US, use US proxy. Don't jump countries.

### Rule 3: Session persistence
Use sticky sessions (same IP for 10-30 min) during each session.

### Rule 4: Rotation between sessions
Get new IP each day/session, but keep consistent during session.

### Rule 5: Track everything
```
LEDGER/proxy_assignments.csv

account_id,platform,proxy_provider,proxy_config,geo,assigned_date
faith_main,x,soax,us-residential-sticky,US-CA,2026-01-21
fitness_main,x,decodo,us-residential-sticky,US-NY,2026-01-21
```

---

## Anti-Detection Checklist

- [ ] Residential or mobile proxy (never datacenter for social)
- [ ] Same geo as account origin
- [ ] Sticky session during activity
- [ ] Consistent browser fingerprint
- [ ] Human-like timing (not bot patterns)
- [ ] One account per proxy assignment
- [ ] Log all proxy usage

---

## Red Flags

**Avoid:**
- Free proxies (data harvesting, blacklisted IPs)
- Shared datacenter pools for social
- Providers with no geo targeting
- Anything with "unlimited" bandwidth claims
- P2P networks for important accounts

**Warning signs:**
- IPs getting flagged often
- Accounts asking for phone verification
- Shadowbans appearing
- Action blocks increasing

---

## Quick Start

### Day 1:
1. Sign up for Soax ($99 minimum, ~15GB)
2. Get residential rotating proxy credentials
3. Test with one burner account
4. Verify IP is clean (whatismyipaddress.com)

### Day 2-7:
1. Assign proxies to accounts
2. Start manual warming with proxies
3. Document what works
4. Monitor for issues

### Week 2+:
1. Scale if working
2. Add Decodo if need more IPs
3. Consider mobile for main accounts
4. Automate with Playwright

---

## Related Documents

- `AUTOMATIONS/SOAX_MOBILE_PROXIES.md` - Deep dive on mobile proxies for IG/TikTok
- `AUTOMATIONS/ACCOUNT_WARMING_SOP.md` - Account warming protocols
- `AUTOMATIONS/SOCIAL_AUTOMATION_STRATEGY.md` - Overall automation approach
- `MONEY_METHODS/COLD_OUTBOUND/infrastructure/` - Email proxy considerations

---

Last updated: 2026-01-21
