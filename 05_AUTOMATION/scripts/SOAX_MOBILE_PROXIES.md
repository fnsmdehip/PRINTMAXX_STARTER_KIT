# Soax Mobile Proxies for Instagram/TikTok

Mobile proxies are the gold standard for social media automation. Platforms trust mobile IPs more than residential because real users use them.

---

## Why Mobile Proxies for IG/TikTok

| Factor | Residential | Mobile |
|--------|-------------|--------|
| Trust level | Medium | High |
| Ban risk | Medium | Low |
| Cost | $6-15/GB | $150+/mo |
| Best for | Scale accounts | Main accounts |
| Detection | Sometimes flagged | Rarely flagged |

**Mobile IPs rotate naturally** (carrier NAT), so platforms expect multiple accounts from same IP. This is why mobile proxies are safer for high-value accounts.

---

## Soax Mobile Proxy Setup

### Pricing (2026)
- **Pay-as-you-go:** ~$3.5/GB (mobile residential)
- **Subscription:** $99/mo for 3GB mobile
- **Enterprise:** Custom pricing for high volume

### Getting Started
1. Sign up at soax.com
2. Select "Mobile Proxies" product
3. Choose location (US recommended for US accounts)
4. Get credentials in dashboard

### Configuration
```
Proxy format: user-package-country-US-sessionduration-30:password@proxy.soax.com:port

Example for 30-min sticky session:
user-mobile-country-US-sessionduration-30:yourpass@proxy.soax.com:9000
```

### Session Types
- **Rotating:** New IP each request (for scraping)
- **Sticky 10min:** Same IP for 10 minutes (light automation)
- **Sticky 30min:** Same IP for 30 minutes (social posting)

**For Instagram/TikTok:** Use sticky 30min sessions.

---

## Instagram Strategy with Mobile Proxies

### Account Setup
1. Create account on mobile proxy
2. Complete profile fully
3. Verify phone if prompted (use separate numbers)
4. First 7 days: Manual only

### Automation Limits (Even with Mobile)
| Action | Daily Limit | Notes |
|--------|-------------|-------|
| Follows | 50-100 | Space out over day |
| Unfollows | 50-100 | Don't unfollow same day as follow |
| Likes | 200-300 | Vary timing |
| Comments | 20-50 | Use variations |
| DMs | 20-30 | Personalize |
| Stories | 10-20 | Native app best |

### Red Flags to Avoid
- Following/unfollowing rapidly
- Same comment copy-paste
- Posting at exact intervals
- Action immediately after login

---

## TikTok Strategy with Mobile Proxies

### Why TikTok is Harder
- More aggressive bot detection
- Fingerprinting is sophisticated
- API changes frequently
- Best results with real device

### Mobile Proxy Approach
1. Use mobile proxy + real device (not emulator)
2. OR use mobile proxy + Playwright with real fingerprint
3. Keep sessions long (don't switch IPs mid-session)
4. Mimic real user patterns exactly

### Safe Automation Limits
| Action | Daily Limit | Notes |
|--------|-------------|-------|
| Posts | 3-5 | Space 3+ hours apart |
| Likes | 100-200 | While scrolling |
| Comments | 30-50 | Unique text |
| Follows | 30-50 | Very conservative |

### TikTok Detection Vectors
- Device fingerprint changes
- IP reputation
- Behavior patterns
- Upload metadata
- Caption patterns

**Best practice:** Use mobile proxy + real phone for TikTok. Automation is risky.

---

## Proxy Assignment Strategy

### Per-Account Assignment
```
LEDGER/proxy_assignments.csv

account_id,platform,proxy_type,proxy_config,geo,notes
ig_faith_main,instagram,soax_mobile,US-sticky30,US,Main account - never lose
ig_fitness_main,instagram,soax_mobile,US-sticky30,US,Main account
ig_ai_main,instagram,soax_mobile,US-sticky30,US,Main account
tiktok_faith,tiktok,soax_mobile,US-sticky30,US,Use real phone
tiktok_fitness,tiktok,soax_mobile,US-sticky30,US,Use real phone
x_faith_main,x,soax_residential,US-sticky30,US,Can use residential
x_burner_1,x,soax_residential,US-rotating,US,Test account
```

### When to Use Mobile vs Residential

**Use Mobile ($$$) for:**
- Main brand accounts
- Monetized accounts
- Accounts with 1k+ followers
- Instagram (stricter)
- TikTok (strictest)

**Use Residential ($) for:**
- Test accounts
- X/Twitter (more lenient)
- Accounts you can afford to lose
- High-volume scraping

---

## Cost Optimization

### Hybrid Strategy
```
Budget: $150/mo

Mobile (main accounts): $99/mo (3GB)
- 3 Instagram mains
- 3 TikTok mains

Residential (test/scale): $50/mo (~8GB)
- X accounts
- Test accounts
- Research/scraping
```

### Bandwidth Usage Estimates
| Activity | Data per session |
|----------|------------------|
| Post to IG | 5-20MB |
| Browse feed | 50-100MB |
| Upload TikTok | 20-100MB |
| Post to X | 1-5MB |

**3GB mobile** = ~100-150 posting sessions/month (enough for 3-5 accounts posting daily)

---

## Troubleshooting

### Account Flagged Anyway?
1. Stop all automation immediately
2. Switch to manual for 7+ days
3. Check if IP is burned (test with new account)
4. Consider new mobile proxy pool
5. Review automation patterns

### IP Quality Issues
- Soax mobile IPs are generally clean
- If getting challenges, try different geo
- Request fresh IP pool from support
- Consider dedicated mobile proxy ($90+/mo)

### Session Disconnects
- Increase timeout settings
- Use sticky sessions (not rotating)
- Check bandwidth limits
- Contact support if persistent

---

## Integration with Playwright

```python
# Example: Instagram with Soax mobile proxy

from playwright.sync_api import sync_playwright

SOAX_MOBILE = {
    "server": "http://proxy.soax.com:9000",
    "username": "user-mobile-country-US-sessionduration-30",
    "password": "your_password"
}

def post_to_instagram(content, image_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            proxy={
                "server": SOAX_MOBILE["server"],
                "username": SOAX_MOBILE["username"],
                "password": SOAX_MOBILE["password"]
            }
        )

        # Use mobile viewport
        context = browser.new_context(
            viewport={"width": 390, "height": 844},  # iPhone 12
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)...",
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )

        page = context.new_page()
        # ... rest of automation
```

---

## Checklist Before Automating IG/TikTok

- [ ] Mobile proxy configured (Soax or equivalent)
- [ ] Account warmed 7+ days manually
- [ ] Proxy assigned to specific account (logged)
- [ ] Session type: sticky 30min
- [ ] Geo matches account origin
- [ ] Rate limits documented
- [ ] Fallback plan if flagged
- [ ] Monitoring in place

---

## Related Documents

- `AUTOMATIONS/PROXY_COMPARISON.md` - Full proxy provider comparison
- `AUTOMATIONS/ACCOUNT_WARMING_SOP.md` - Account warming protocols
- `AUTOMATIONS/SOCIAL_AUTOMATION_STRATEGY.md` - Overall automation approach
- `LEDGER/proxy_assignments.csv` - Track proxy-account assignments
- `MONEY_METHODS/AI_INFLUENCER/` - AI influencer playbooks
- `MONEY_METHODS/CONTENT_FARM/` - Content scaling strategies

---

Last updated: 2026-01-21
