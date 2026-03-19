# Performance Rules

## Build Size Targets

**Maximum bundle sizes:**
- Initial load: < 500KB (gzipped)
- Per-route chunk: < 200KB
- Images: < 500KB each (< 100KB for thumbnails)
- Total page weight: < 2MB

**If exceeded:**
- Code split by route
- Lazy load components
- Optimize images
- Remove unused dependencies

## Image Optimization

**Required:**
- Use Next.js Image component
- Provide width/height attributes
- Use modern formats (WebP, AVIF)
- Implement lazy loading
- Generate multiple sizes for responsive

**Image Guidelines:**
```jsx
// ✅ Good
<Image
  src="/image.jpg"
  alt="Descriptive alt text"
  width={800}
  height={600}
  placeholder="blur"
/>

// ❌ Bad
<img src="/huge-image.png" />
```

## Core Web Vitals Targets

**Largest Contentful Paint (LCP):** < 2.5s
- Optimize server response time
- Use CDN for static assets
- Preload critical resources
- Optimize images above fold

**First Input Delay (FID):** < 100ms
- Break up long JavaScript tasks
- Use web workers for heavy computation
- Defer non-critical JavaScript

**Cumulative Layout Shift (CLS):** < 0.1
- Reserve space for images/ads
- Avoid inserting content above existing content
- Use CSS aspect ratio

## Database & API Performance

**Query optimization:**
- Index frequently queried fields
- Use pagination for large datasets
- Implement caching (Redis, CDN)
- Avoid N+1 queries

**API response times:**
- Target: < 200ms for most endpoints
- Implement request timeouts
- Use connection pooling
- Cache expensive operations

## Caching Strategy

**Static assets:**
- Long cache TTL (1 year) with content hashing
- Use CDN for global distribution

**Dynamic content:**
- ISR (Incremental Static Regeneration) for semi-static pages
- SWR (stale-while-revalidate) for user-specific data
- Redis for session/computed data

## JavaScript Performance

**Avoid:**
- Blocking synchronous operations
- Unnecessary re-renders (use React.memo)
- Expensive operations in render
- Large inline scripts

**Prefer:**
- Code splitting at route level
- Tree shaking (ES modules)
- Lazy loading heavy components
- Web workers for CPU-intensive tasks

## Monitoring & Metrics

**Track in production:**
- Core Web Vitals (Google Analytics, Vercel Analytics)
- API response times
- Error rates
- Bundle sizes (Bundlephobia, Webpack Bundle Analyzer)

**Regular audits:**
- Run Lighthouse weekly
- Check bundle size on each deploy
- Monitor real user metrics (RUM)
- Profile performance bottlenecks

## Performance Budget

**Alerts triggered if:**
- Initial bundle > 500KB
- LCP > 3s
- FID > 150ms
- CLS > 0.15
- API p95 > 500ms

## Optimization Checklist for New Features

- [ ] Images optimized and lazy loaded
- [ ] Code split if > 50KB
- [ ] No blocking third-party scripts
- [ ] Caching strategy defined
- [ ] Database queries indexed
- [ ] Lighthouse score > 90
- [ ] Bundle size impact measured
- [ ] No console.log in production
