# Ralph Task: Landing Page Components

Build Next.js components for landing site.

---

## Context
- Read `LANDING/printmaxx-site/` for existing structure
- Read `.claude/rules/code-style.md` for code rules
- Read `.claude/rules/copy-style.md` for content
- Output to `LANDING/printmaxx-site/components/`
- Stack: Next.js, TypeScript, Tailwind

## Success Criteria

### Hero Components
1. [x] `HeroSimple.tsx` - Text + CTA
2. [x] `HeroWithImage.tsx` - Text + image
3. [x] `HeroWithVideo.tsx` - Text + embedded video
4. [x] All responsive (mobile-first)
5. [x] Props typed with TypeScript

### Social Proof Components
6. [x] `TestimonialCard.tsx` - Single testimonial
7. [x] `TestimonialGrid.tsx` - Grid of testimonials
8. [x] `LogoBar.tsx` - "As seen in" logos
9. [x] `StatsBar.tsx` - Key metrics display

### CTA Components
10. [x] `EmailCapture.tsx` - Email input + submit
11. [x] `LeadMagnetCTA.tsx` - Download offer
12. [x] `PricingCard.tsx` - Single pricing tier
13. [x] `PricingTable.tsx` - Multiple tiers

### Content Components
14. [x] `FeatureGrid.tsx` - Icon + title + description
15. [x] `BenefitsList.tsx` - Checkmark list
16. [x] `FAQAccordion.tsx` - Expandable FAQ
17. [x] `ComparisonTable.tsx` - Us vs them

### Trust Components
18. [x] `GuaranteeBox.tsx` - Money back guarantee
19. [x] `SecurityBadges.tsx` - Trust indicators
20. [x] `SocialProofCounter.tsx` - Live counter

## Code Requirements
```typescript
// All components must have:
// 1. TypeScript interfaces for props
// 2. Tailwind for styling
// 3. Responsive design
// 4. Accessibility (aria labels)
// 5. No inline styles

interface ComponentProps {
  // Explicit typing
}

export function Component({ prop }: ComponentProps) {
  return (
    // JSX
  )
}
```

## Constraints
- Mobile-first responsive
- Dark mode support (optional)
- No external CSS libraries
- Tailwind only
- Accessible (WCAG 2.1)

## After Completion
- Update `.ralph/progress.md`
- Log any errors to `.ralph/errors.log`
- Add new guardrails if patterns discovered

---

test_command: "find LANDING/printmaxx-site/components -name '*.tsx' | wc -l"
expected_output: "20"
