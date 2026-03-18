# TEST ACTION PLAN — 2026-03-18

**Status:** 87.5% health pass rate (28/32 tested)  
**Blocker:** 3 sites with DNS failures (domain names >63 chars)  
**Timeline:** Auto-fix deployable this cycle  

---

## IMMEDIATE ACTIONS

### Action 1: Add Domain Name Validation to asset_deployer.py

**Current:** No validation on domain name length  
**Required:** Enforce max 60-char limit  

```python
# Add to asset_deployer.py before deployment:

MAX_DOMAIN_LENGTH = 60

def validate_domain_name(domain: str) -> bool:
    """Validate domain meets Surge.sh + DNS requirements."""
    if len(domain) > MAX_DOMAIN_LENGTH:
        logger.error(f"Domain too long: {domain} ({len(domain)} chars, max {MAX_DOMAIN_LENGTH})")
        return False
    
    if not domain or not domain[0].isalnum():
        logger.error(f"Invalid domain start: {domain}")
        return False
    
    return True

# Usage before deployment:
assert validate_domain_name(generated_domain), f"Domain validation failed: {generated_domain}"
```

**Impact:** Prevents future deployments of unreachable sites  
**Effort:** 10 minutes  

---

### Action 2: Re-deploy 3 RED Sites with Shorter Names

**Current Broken Domains → New Short Names:**

1. `mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh` (84 chars)
   → `mobile-detailing-okc-champion.surge.sh` (35 chars) ✅

2. `window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh` (77 chars)
   → `window-cleaning-portland-allpro.surge.sh` (39 chars) ✅

3. `local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky.surge.sh` (78 chars)
   → `window-cleaning-louisville-pinks.surge.sh` (41 chars) ✅

**Deployment Command:**
```bash
surge publish /path/to/source --domain mobile-detailing-okc-champion.surge.sh
surge publish /path/to/source --domain window-cleaning-portland-allpro.surge.sh
surge publish /path/to/source --domain window-cleaning-louisville-pinks.surge.sh
```

**Expected Result:** 3 RED → 3 GREEN  
**Effort:** 15 minutes  
**Estimated revenue recovered:** $240+/mo

---

### Action 3: Profile & Optimize prayerlock-web.surge.sh

**Current:** 8.5s load time (YELLOW)  
**Target:** <3s (GREEN)  

**Profiling Steps:**
1. Check bundle size: `npm run build --analyze`
2. Identify large JS chunks (>500KB)
3. Look for render-blocking resources
4. Check for missing lazy loading

**Optimization Options:**
- [ ] Code split routes (Vite)
- [ ] Lazy load components
- [ ] Compress assets (gzip/brotli)
- [ ] Use service worker for caching
- [ ] Remove unused dependencies

**Effort:** 30-45 minutes  

---

## EXECUTION QUEUE

| Priority | Action | Est. Time | Owner | Status |
|----------|--------|-----------|-------|--------|
| P0 | Add domain validation | 10m | asset_deployer | Ready |
| P0 | Re-deploy 3 RED sites | 15m | surge deployer | Ready |
| P1 | Profile prayerlock-web | 10m | profiler agent | Ready |
| P1 | Fix prayerlock-web | 30m | frontend dev | Pending profile |
| P2 | Scale test coverage | 20m | test automation | Backlog |

**Total Time to Full Fix:** ~75 minutes  

---

## SUCCESS CRITERIA

- [ ] All 3 RED sites resolve and load (DNS tests pass)
- [ ] No regressions in previously GREEN sites
- [ ] prayerlock-web load time <3s
- [ ] Domain validation prevents future >60-char names

---

## MONITORING

**Post-fix test schedule:**
- Immediate: Test 3 redeployed sites
- 1 hour: Full suite of 32 critical sites
- Weekly: Expand to 80+ sites across all categories

**Automation:**
```bash
# Schedule weekly test
0 2 * * 0 python3 /path/to/playwright_test_batch.py
```

