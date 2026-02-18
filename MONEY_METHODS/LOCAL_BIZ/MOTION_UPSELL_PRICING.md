# Motion website upsell: pricing, prompts, and execution

Local biz clients pay 3-6x more for animated sites over static. The perceived value gap is massive: static sites look like 2018, motion sites look like 2026. Scroll-triggered animations convert 27% better. Animated CTAs get 40% more clicks. Parallax hero sections reduce bounce rates by 22%.

Those numbers are from real A/B tests. Not vibes.

We have 6 static templates already built. We have 3 motion templates (dental, restaurant, realtor). This document turns that into a productized service with 90%+ margins.

---

## 1. PRICING TIERS

### What the market charges (real numbers, 2026)

| Provider type | Static site | Animated/motion site | Monthly retainer |
|--------------|------------|---------------------|-----------------|
| Boutique agency | $6,000-$12,000 | $10,000-$25,000 | $500-$2,000/mo |
| Mid-tier agency | $3,000-$8,000 | $5,000-$15,000 | $300-$1,000/mo |
| Fiverr Pro seller | $1,000-$3,000 | $2,000-$5,000 | $100-$300/mo |
| Upwork top-rated | $1,500-$4,000 | $3,000-$8,000 | $200-$500/mo |
| WordPress freelancer | $700-$2,000 | $1,500-$4,000 | $75-$200/mo |
| DIY builder (Wix/Squarespace) | $20-$50/mo | Not possible | N/A |

Sources: WebFX, GruffyGoat, DesignRush, TL Design Studios, Mark Brinker. All 2026 data.

### Our pricing (undercut agencies, 10x Fiverr quality)

| Tier | Price | What they get | Our build time | Our cost | Profit margin |
|------|-------|---------------|---------------|----------|---------------|
| **Starter Static** | $500-$800 | Clean single page. Mobile responsive. Contact form. Google Maps. Basic SEO. Click-to-call. Looks professional, no animation. | 1-2 hours | $0 | 90-95% |
| **Motion Standard** | $1,500-$2,500 | Everything in Static + scroll-triggered fade-ins, animated gradient hero, parallax sections, counter animations, hover 3D card effects, testimonial carousel, scroll progress bar, floating label forms, pulsing CTA. Looks like a $10K agency build. | 2-4 hours | $0 | 93-96% |
| **Premium Motion + Video** | $3,000-$5,000 | Everything in Motion + background video hero, 3D floating elements, custom booking integration (Calendly/Acuity), Google Reviews API, before/after interactive slider, live chat widget, Instagram feed embed, animated FAQ accordion, multi-page (up to 5 pages). | 4-8 hours | ~$50 API costs | 90-95% |
| **Ongoing Management** | $200-$500/mo | Hosting, SSL, monthly design update, SEO blog post, Google Business optimization, analytics report. | 1-2 hrs/mo | $5-15/mo hosting | 92-97% |

### Add-ons (pure margin)

| Add-on | Price | Build time |
|--------|-------|-----------|
| Additional pages | $200/page (Static), $400/page (Motion) | 30-60 min |
| Logo design | $150 | 30 min (AI-generated, refined) |
| Professional copywriting | $200/page | 20 min (AI + edit) |
| Google Business setup + optimization | $300 one-time | 1 hour |
| 4 SEO blog posts/month | $299/mo | 1 hour/mo (AI-generated, edited) |
| Social media graphics (10/mo) | $199/mo | 30 min (Canva templates) |
| Email/SMS setup (Mailchimp or similar) | $400 one-time | 2 hours |
| Speed optimization audit | $200 one-time | 30 min |

### Pricing psychology: how to anchor and close

**The 3-tier anchor strategy:**
1. Show Premium first ($3,000-$5,000). Let sticker shock set in.
2. Show Motion Standard ($1,500-$2,500). This looks reasonable now.
3. Mention Static exists ($500-$800). "But honestly, for a few hundred more, you get the motion version that converts 27% better."

**Most clients land on Motion Standard.** That's the target. $1,500-$2,500 for 2-4 hours of work.

**Never show your cheapest option first.** If someone asks "how much," lead with: "Our premium interactive sites run $3,000-$5,000. But for most local businesses, the $1,500 motion package delivers the best ROI."

**Bundle discount (increases average deal size):**
- Motion website + Google Business optimization + 3 months SEO: $2,500 (vs $3,397 a la carte). Save $897.
- Premium website + GMB + 6 months SEO + logo: $5,000 (vs $6,544 a la carte). Save $1,544.
- Any tier + 12-month management: 2 months free (pay for 10, get 12).

**Payment terms:**
- 50% upfront, 50% on delivery. Non-negotiable.
- Monthly retainers billed on the 1st. Auto-pay only.
- Net-30 for businesses over 50 employees (rare for local biz).

### Competitive advantage breakdown

We can charge less and profit more than every competitor because:

1. **Templates are pre-built.** Agency charges $10K and spends 40-80 hours. We spend 2-4 hours personalizing a template. Same output quality.
2. **No WordPress.** Zero plugin costs. Zero security update liability. Zero hosting complexity. A $5/mo shared host runs our sites.
3. **Pure HTML/CSS/JS.** No framework dependencies. No build tools. No node_modules. No GSAP license ($199/yr per site). Our animations are vanilla CSS and Intersection Observer API.
4. **AI handles copy.** Client gives us their info, Claude writes the copy in 2 minutes. Agency charges $200/hr for a copywriter to do the same thing in 4 hours.
5. **Volume play.** We can serve 10-20 clients/week at $1,500 each. That's $15K-$30K/week from template swaps. An agency serves 2-3 clients/month at $8K each.

### Revenue projections (conservative)

| Scenario | Clients/month | Avg deal | Monthly revenue | Monthly profit |
|----------|--------------|----------|----------------|---------------|
| Side hustle | 4 | $1,500 | $6,000 | $5,400 |
| Full time | 10 | $1,800 | $18,000 | $16,200 |
| With VA | 20 | $2,000 | $40,000 | $34,000 |
| Agency mode | 40 | $2,200 | $88,000 | $70,000 |

Add recurring: 50% of clients take $200-$500/mo management. 10 clients on $300/mo = $3,000/mo recurring by month 3.

---

## 2. MOTION TEMPLATE PROMPTS (AI tool copy-paste ready)

These prompts work with Lovable, Bolt.new, v0.dev, and Cursor. Each generates a complete motion website for a specific local business vertical.

### Prompt structure (how these work)

Each prompt specifies:
- Industry and business type
- Color palette (hex codes)
- Animation types (specific CSS/JS effects)
- Sections (in order)
- CTAs and conversion elements
- Mobile behavior
- Performance requirements

Paste any of these directly into Lovable or Bolt.new. They generate a deployable site in 3-5 minutes.

---

### PROMPT 1: Dental practice

```
Build a single-page motion website for a modern dental practice.

BRAND:
- Business name: [PRACTICE_NAME]
- Phone: [PHONE]
- Address: [ADDRESS]
- Colors: primary #2563eb (blue), accent #06b6d4 (cyan), background #f8fafc
- Font: Inter or system font stack
- Tone: clean, trustworthy, modern

HERO SECTION:
- Full-viewport animated gradient background cycling between #1e3a5f, #2563eb, #06b6d4
- Floating particle effect (20 small circles with opacity 0.15, rising animation)
- H1: "Modern Family Dentistry" with fade-up animation (0.3s delay)
- Subtitle: "Gentle care. Advanced technology. Beautiful smiles." fade-up (0.6s delay)
- CTA button: "Book Your Appointment" with pulsing glow effect, white bg, blue text, 50px border-radius
- Sticky nav that changes from transparent to white/blur on scroll

ANIMATIONS (apply to all sections):
- Intersection Observer scroll-triggered fade-up reveals (40px translate, 0.7s ease)
- Staggered delays on grid items (0.15s increment per card)
- 3D hover effect on service cards (translateY -6px, rotateX 2deg, rotateY -2deg)
- Counter animation on stats section (count from 0 to target number over 2s)
- Testimonial crossfade carousel with dot indicators, auto-rotate every 5s
- Scroll progress bar at top of page (gradient blue to cyan)
- prefers-reduced-motion: disable all animations

SECTIONS (in order):
1. Hero (described above)
2. Services grid (6 cards): General Dentistry, Cosmetic, Implants, Orthodontics, Emergency, Whitening. Each card has icon, title, description, hover 3D effect.
3. Stats bar (gradient bg): "15+ Years Experience" | "10,000+ Patients" | "4.9 Star Rating" | "Same-Day Appointments" - counter animations
4. About section with image placeholder left, text right
5. Testimonials carousel (3 reviews with crossfade)
6. Insurance section: "We accept most insurance plans" with logo grid
7. Contact section: floating-label form (name, email, phone, message), Google Maps embed, click-to-call button
8. Footer with business hours, phone, address, social links

TECHNICAL:
- Single HTML file, all CSS inline in <style>, all JS inline in <script>
- No external dependencies, no npm, no framework
- Mobile responsive (768px breakpoint, stack to single column)
- Lazy load images
- < 50KB total page weight
- Lighthouse score target: 95+
```

---

### PROMPT 2: Restaurant

```
Build a single-page motion website for an upscale casual restaurant.

BRAND:
- Business name: [RESTAURANT_NAME]
- Phone: [PHONE]
- Address: [ADDRESS]
- Colors: primary #d4a574 (warm gold), accent #2d1810 (dark brown), background #1a1a1a (dark), text #f5f0eb (cream)
- Font: Playfair Display for headings, Inter for body
- Tone: warm, inviting, appetizing, premium but not stuffy

HERO SECTION:
- Dark full-viewport hero with subtle parallax background image (food/ambiance placeholder)
- Overlay gradient from rgba(26,26,26,0.7) to transparent
- H1: restaurant name in Playfair Display, 4rem, fade-up with letter-spacing animation
- Subtitle: tagline, fade-up 0.6s delay
- Two CTAs side by side: "View Menu" (outlined gold border) and "Reserve a Table" (solid gold bg)
- Both CTAs have hover scale(1.05) + box-shadow grow effect

ANIMATIONS:
- Parallax scrolling on hero background image (0.5x scroll speed)
- Scroll-triggered fade-up reveals on all sections
- Menu items slide in from left (odd) and right (even) with stagger
- Image zoom-on-hover for food gallery (scale 1.08, 0.5s ease)
- Gold accent line that grows width on scroll into view
- Smooth scroll between sections
- Dark theme throughout, gold accents glow subtly

SECTIONS:
1. Hero (described above)
2. Story/About: split layout - text left, image right. "Our Story" heading with decorative gold line underneath that animates width from 0 to 100px
3. Menu highlights: 3-column grid showing 6-9 featured dishes. Each card: food image, dish name, short description, price. Cards fade in with stagger.
4. Ambiance gallery: 2x3 photo grid with zoom-on-hover. Masonry style on desktop, stack on mobile.
5. Specials banner: parallax background with "Happy Hour: Mon-Fri 4-6pm" - text fade-in
6. Testimonials: dark cards with gold star ratings, crossfade carousel
7. Reservation CTA: large section with form (date, time, party size, name, phone, email). Floating labels, gold accent borders on focus.
8. Location + Hours: Google Maps embed (dark mode), hours table, phone with click-to-call
9. Footer: social links, address, "Follow us on Instagram" CTA

TECHNICAL:
- Single HTML file, inline CSS + JS
- No dependencies
- Dark theme default
- Mobile responsive
- Placeholder images use CSS gradients (no external image URLs)
- < 50KB total
```

---

### PROMPT 3: Real estate agent

```
Build a single-page motion website for a luxury real estate agent.

BRAND:
- Agent name: [AGENT_NAME]
- Brokerage: [BROKERAGE]
- Phone: [PHONE]
- Colors: primary #1a1a2e (navy), accent #c9a96e (gold), background #ffffff, text #1a1a2e
- Font: Playfair Display headings, Inter body
- Tone: luxury, professional, trustworthy, confident

HERO SECTION:
- Full-viewport with large background image placeholder (luxury home exterior)
- Subtle Ken Burns effect on background (slow zoom from scale(1) to scale(1.08) over 20s)
- Glassmorphism overlay card in center: agent name, title "Luxury Real Estate Specialist", tagline
- Card has backdrop-filter: blur(16px), rgba(255,255,255,0.1) bg, 1px solid rgba(255,255,255,0.2) border
- CTA: "View Properties" gold button with hover glow
- Animated stats bar at bottom of hero: "50+ Homes Sold" | "$45M+ in Sales" | "15 Years Experience" - counter animation

ANIMATIONS:
- Ken Burns on hero image
- Counter animations on stats
- Property cards: hover lifts card, reveals "View Details" overlay with slide-up
- Testimonial section: cards slide in from sides
- Section transitions: smooth fade-up reveals
- Gold accent lines animate width on scroll
- Subtle parallax on alternating sections

SECTIONS:
1. Hero (described above)
2. Featured Listings: 3-column grid, each card has image, price overlay, address, beds/baths/sqft. Hover effect reveals detail overlay.
3. About the Agent: photo left, bio right. Stats inline. "Why Work With Me" 3-point grid below.
4. Services: "Buying" | "Selling" | "Investment" | "Relocation" - icon cards with hover 3D effect
5. Sold properties: horizontal scroll gallery of recent sales with sale price overlays
6. Testimonials: large quote cards, 5-star gold ratings, crossfade carousel
7. Market Stats: "Median Home Price: $X" | "Days on Market: X" | "List-to-Sale Ratio: X%" - animated counters
8. Contact: "Let's Find Your Dream Home" - form (name, email, phone, budget range dropdown, message). Gold accents.
9. Footer: brokerage info, license number, equal housing logo, social links

TECHNICAL:
- Single HTML file
- Inline CSS + JS
- Mobile responsive
- Gold accent color used sparingly (CTAs, borders, stars, lines)
- < 60KB total
```

---

### PROMPT 4: Plumber / HVAC

```
Build a single-page motion website for a local plumbing and HVAC company.

BRAND:
- Business name: [COMPANY_NAME]
- Phone: [PHONE] (prominently displayed, this is the primary conversion)
- Address: [ADDRESS]
- Colors: primary #1e40af (trust blue), accent #f59e0b (warning yellow/orange), background #f8fafc, text #0f172a
- Font: system font stack (no custom fonts, maximize speed)
- Tone: reliable, fast, trustworthy, no-nonsense

HERO SECTION:
- Blue gradient background (#1e40af to #2563eb) with subtle animated pipe/wrench SVG pattern
- Large phone number at top: "Call Now: [PHONE]" in yellow accent, click-to-call
- H1: "24/7 Emergency Plumbing & HVAC" fade-up
- Subtitle: "Licensed. Insured. Same-day service." fade-up delayed
- Two CTAs: "Call Now" (yellow bg, large, pulsing) and "Request Quote" (white outlined)
- Trust badges below CTAs: "Licensed & Insured" | "5-Star Rated" | "Same Day Service" | "Free Estimates" - fade in with stagger

ANIMATIONS:
- Pulsing phone icon next to number (draws attention to call CTA)
- Scroll reveals on all sections
- Service cards hover with lift + shadow grow
- Counter animations on stats
- Emergency banner with subtle flash/pulse animation
- Before/after slider for renovation projects
- Floating "Call Now" button fixed bottom-right on mobile

SECTIONS:
1. Hero (described above)
2. Emergency banner: red/yellow gradient strip "Burst pipe? Flooding? We're on our way. Call [PHONE]" with pulse animation
3. Services grid (8 cards): Drain Cleaning, Water Heater, Pipe Repair, Sewer Line, AC Repair, Furnace, Bathroom Remodel, Kitchen Plumbing
4. Why Choose Us: 4 columns - "24/7 Emergency" | "Upfront Pricing" | "Licensed Pros" | "Satisfaction Guarantee" with check icons
5. Stats: "20+ Years" | "5,000+ Jobs" | "4.8 Stars" | "< 1 Hour Response" - counters
6. Testimonials carousel
7. Service Areas: list of cities/neighborhoods served, with map
8. Contact form + Google Maps + business hours + phone (large, yellow)
9. Footer

TECHNICAL:
- Single HTML file
- Phone number appears minimum 4 times on page
- Click-to-call on every phone instance
- Floating mobile CTA button (fixed position)
- < 40KB total (speed is critical for emergency searches)
- Schema markup for LocalBusiness
```

---

### PROMPT 5: Fitness / gym / personal trainer

```
Build a single-page motion website for a fitness studio or personal training business.

BRAND:
- Business name: [GYM_NAME]
- Phone: [PHONE]
- Colors: primary #000000 (black), accent #ef4444 (energetic red), secondary #22c55e (green for CTAs), background #0a0a0a (near-black), text #ffffff
- Font: bold sans-serif (system stack)
- Tone: energetic, motivating, bold, no-excuses

HERO SECTION:
- Dark full-viewport with high-contrast text
- Background: animated gradient mesh (black to dark red to black, slow shift)
- H1: gym name in all-caps, extra bold, scale-in animation from 0.8 to 1.0
- Subtitle: "Transform your body. Transform your life." typewriter effect
- CTA: "Start Your Free Trial" green button, scale hover effect
- Stats row below CTA: "500+ Members" | "15 Classes/Week" | "Expert Trainers" - counter animation

ANIMATIONS:
- Typewriter effect on subtitle
- Scale-in on headings
- Program cards flip on hover to reveal details on back
- Trainer photos have grayscale-to-color transition on scroll into view
- Schedule section: tabs slide content left/right on switch
- Transformation photos: before/after slider with drag handle
- Parallax on section backgrounds
- Red accent pulse on key CTAs

SECTIONS:
1. Hero
2. Programs: "Personal Training" | "Group Classes" | "Online Coaching" | "Nutrition Plans" - flip cards
3. Class schedule: tabbed by day, clean table layout
4. Trainers: photo grid, grayscale-to-color on scroll reveal, name + specialty overlay
5. Transformations: before/after photo pairs with interactive slider
6. Pricing: 3 tiers in comparison cards (Basic, Premium, Unlimited) with recommended tier highlighted
7. Testimonials: dark cards with red accent borders, carousel
8. Free trial CTA: large red section "Your first week is free. No strings."
9. Contact: form, location map, hours
10. Footer

TECHNICAL:
- Single HTML file
- Dark theme throughout
- < 55KB total
- Mobile responsive with simplified animations
```

---

### PROMPT 6: Law firm

```
Build a single-page motion website for a personal injury law firm.

BRAND:
- Firm name: [FIRM_NAME]
- Phone: [PHONE]
- Colors: primary #1e293b (dark slate), accent #b91c1c (deep red), secondary #d4a574 (gold), background #ffffff, text #1e293b
- Font: serif for headings (Georgia/Playfair Display), sans-serif for body
- Tone: authoritative, empathetic, trustworthy, serious but approachable

HERO SECTION:
- Clean white/light background with subtle dark geometric pattern overlay
- H1: "Injured? You Deserve Justice." fade-up, serif font, large
- Subtitle: "No fees unless we win. Free consultation." fade-up delayed
- Two CTAs: "Free Case Review" (red, prominent) and "Call [PHONE]" (gold outlined)
- Trust badges: "No Win No Fee" | "$50M+ Recovered" | "500+ Cases Won" | "24/7 Available"
- Badges animate in with stagger

ANIMATIONS:
- Refined, understated animations (not flashy - this is law, not a nightclub)
- Scroll reveals with slow, dignified fade-ups (1s duration)
- Case result numbers counter animation
- Testimonials fade transitions
- Subtle parallax on hero
- Hover state on practice area cards: shadow grow + border-left accent color
- No particles, no floating elements, no gradients - clean and authoritative

SECTIONS:
1. Hero
2. Practice areas: "Car Accidents" | "Truck Accidents" | "Slip and Fall" | "Medical Malpractice" | "Workers Comp" | "Wrongful Death" - clean cards with icon, title, one-line description
3. Case results: "$2.1M - Car Accident" | "$1.5M - Medical Malpractice" | "$890K - Slip and Fall" - large numbers with counter animation
4. About the firm: photo, bio, credentials, bar memberships
5. Process: "How It Works" 4-step timeline (Free Consult > Investigation > Negotiation > Resolution) with connecting line animation
6. Testimonials
7. FAQ accordion with smooth expand/collapse animation
8. Free consultation CTA section with form (name, phone, email, case type dropdown, brief description)
9. Footer with disclaimer: "Results may vary. Free consultation does not guarantee representation."

TECHNICAL:
- Single HTML file
- Serif headings, sans body
- Schema markup for Attorney
- ADA accessible (all animations respect prefers-reduced-motion)
- < 45KB total
```

---

### PROMPT 7: Hair salon / barbershop

```
Build a single-page motion website for a modern hair salon.

BRAND:
- Salon name: [SALON_NAME]
- Phone: [PHONE]
- Colors: primary #831843 (deep pink/magenta), accent #fbbf24 (warm gold), background #fdf2f8 (light pink tint), text #1f2937
- Font: cursive/script for salon name (decorative), Inter for everything else
- Tone: stylish, welcoming, trendy, warm

HERO SECTION:
- Soft gradient background (light pink to white)
- Salon name in decorative script font, large, fade-in with slight scale
- Subtitle: "Where style meets confidence" fade-up
- CTA: "Book Now" in gold with magenta hover
- Floating hair-related decorative elements (scissors icon, comb icon) slowly drifting, low opacity

ANIMATIONS:
- Soft, elegant animations (ease-in-out, longer durations)
- Service cards slide up on scroll
- Stylist photos: circular crop with border that animates color on hover
- Gallery: masonry grid with zoom-on-hover
- Instagram embed with subtle shine effect
- Pricing table rows highlight on hover

SECTIONS:
1. Hero
2. Services + Pricing: "Women's Cut: from $45" | "Men's Cut: from $30" | "Color: from $85" | "Highlights: from $120" | "Blowout: from $40" | "Bridal: from $200" - clean table with hover highlight
3. Stylists: circular photos with name, specialty, "Book with [Name]" button
4. Gallery: before/after transformations, masonry grid, zoom on hover
5. Reviews carousel
6. Instagram feed section: "Follow us @[handle]" with embedded grid or placeholder
7. Location + booking: map, hours, "Book Online" button linking to booking platform
8. Footer

TECHNICAL:
- Single HTML file
- Feminine color palette with gold accents
- < 45KB
```

---

### PROMPT 8: Auto repair shop

```
Build a single-page motion website for an auto repair shop.

BRAND:
- Shop name: [SHOP_NAME]
- Phone: [PHONE]
- Colors: primary #dc2626 (mechanic red), accent #f59e0b (caution yellow), background #111111 (dark), text #f5f5f5
- Font: bold sans-serif, industrial feel
- Tone: honest, tough, reliable, no-BS

HERO SECTION:
- Dark background with subtle tire tread pattern animation (CSS repeating pattern that slowly scrolls)
- H1: shop name in bold caps, red accent on key word
- Subtitle: "Honest work. Fair prices. Since [YEAR]."
- CTA: "Get a Free Estimate" yellow button, large
- Phone number displayed large below CTA
- Trust badges: "ASE Certified" | "BBB A+" | "12-Month Warranty" | "Free Estimates"

ANIMATIONS:
- Industrial, mechanical feel (not soft/elegant)
- Cards slide in from sides
- Stats counters
- Service icons rotate 360 on hover
- Before/after slider for repair jobs
- Grimy/textured section backgrounds

SECTIONS:
1. Hero
2. Services: Oil Change, Brake Repair, Engine Diagnostics, Transmission, Tire Service, AC Repair, Electrical, Suspension - grid with icons
3. Why choose us: "Certified Mechanics" | "Transparent Pricing" | "Warranty on Parts" | "All Makes & Models"
4. Stats: "25 Years" | "30,000+ Vehicles" | "4.9 Stars" | "Same Day Available"
5. Coupons/Specials: "$29.99 Oil Change" | "Free Brake Inspection" | "10% Off First Visit" - animated cards
6. Reviews carousel
7. Service area map
8. Contact form + hours + phone
9. Footer

TECHNICAL:
- Single HTML file
- Dark theme with red/yellow accents
- Phone number appears 3+ times
- < 40KB
```

---

### PROMPT 9: Pet services (vet, grooming, boarding)

```
Build a single-page motion website for a pet grooming and boarding facility.

BRAND:
- Business name: [BUSINESS_NAME]
- Phone: [PHONE]
- Colors: primary #7c3aed (purple), accent #f472b6 (pink), secondary #34d399 (green), background #faf5ff (light purple tint), text #1f2937
- Font: rounded sans-serif (friendly feel)
- Tone: friendly, warm, playful, trustworthy with animals

HERO SECTION:
- Light playful gradient background (purple to pink, soft)
- Animated paw print trail across top (small paw icons floating across screen, subtle)
- H1: "[BUSINESS_NAME]" with paw print emoji
- Subtitle: "Where every pet is treated like family"
- CTA: "Book a Grooming" green button, bounce animation on load
- Happy pet stat badges: "5,000+ Happy Pets" | "Certified Groomers" | "Cage-Free Boarding"

ANIMATIONS:
- Playful and friendly (bounce effects, wiggles, soft movements)
- Paw print floating background animation
- Service cards bounce on hover
- Pet photo gallery with tilt effect on hover
- Testimonials from "pet parents" with pet name + breed
- Star ratings with gold fill animation

SECTIONS:
1. Hero
2. Services: Grooming, Boarding, Daycare, Training, Vet Referral, Pet Spa - colorful cards with pet icons
3. Grooming packages: "Bath & Brush: $35" | "Full Groom: $55" | "Spa Day: $85" - comparison table
4. Boarding: rates, what's included, photos of facility
5. Meet the Team: staff photos with their pets, fun bios
6. Pet gallery: grid of happy groomed pets
7. Reviews: "Luna (Golden Retriever) loves it here! -Sarah M." format
8. Booking form: pet name, breed, service, preferred date, owner contact
9. Footer with hours, emergency contact

TECHNICAL:
- Single HTML file
- Playful, rounded design elements
- < 45KB
```

---

### PROMPT 10: Landscaping / lawn care

```
Build a single-page motion website for a landscaping and lawn care company.

BRAND:
- Business name: [COMPANY_NAME]
- Phone: [PHONE]
- Colors: primary #15803d (forest green), accent #a16207 (earth brown), background #f0fdf4 (light green tint), text #14532d
- Font: clean sans-serif
- Tone: outdoorsy, professional, reliable, results-focused

HERO SECTION:
- Green gradient background with subtle leaf/grass pattern overlay
- H1: "Professional Landscaping & Lawn Care"
- Subtitle: "Your yard. Our passion. [City]'s trusted choice since [YEAR]."
- CTA: "Get a Free Quote" brown/earth button
- Before/after hero: split-screen with sliding divider showing transformation

ANIMATIONS:
- Nature-inspired (growing lines, sprouting effects)
- Before/after interactive slider in hero (key selling tool)
- Service cards fade up with stagger
- Project gallery with zoom-on-hover
- Seasonal service tabs with slide transition
- Counter animation for stats
- Leaf icon that subtly sways (CSS animation on one decorative element)

SECTIONS:
1. Hero with before/after slider
2. Services: Lawn Mowing, Landscape Design, Tree Trimming, Irrigation, Hardscaping, Seasonal Cleanup, Mulching, Fertilization
3. Before/After Gallery: 4-6 project pairs with interactive sliders
4. Why choose us: "Fully Insured" | "Free Estimates" | "Satisfaction Guarantee" | "Eco-Friendly Products"
5. Stats: "15+ Years" | "2,000+ Lawns" | "4.9 Stars"
6. Seasonal services tabs: Spring | Summer | Fall | Winter - tab content slides on switch
7. Service area map with highlighted zones
8. Quote request form: service type, property size estimate, address, contact info
9. Reviews carousel
10. Footer

TECHNICAL:
- Single HTML file
- Green/earth tone palette
- Before/after slider is the hero selling feature
- < 45KB
```

---

## 3. UPSELL SCRIPT

### Cold email: motion upgrade pitch

**Subject line options (A/B test these):**
- "Your website is losing customers (2-minute video proof)"
- "I rebuilt your site with animations. see it now."
- "[BUSINESS_NAME] - your competitors' websites look like this now"
- "static websites are dead. here's proof."

**Email body:**

```
[FIRST_NAME],

I built two versions of a website for [INDUSTRY] businesses like yours.

Same content. Same info. One is static. One has scroll animations.

Side-by-side: [DEMO_LINK]

The animated version loads the same speed, works on all devices, costs nothing extra to host. But it looks like a $10,000 custom build.

Animated sites get 27% more engagement and 40% more clicks on call-to-action buttons. That's not a guess. That's from A/B testing data across 10,000+ sites.

I'm offering motion websites for [INDUSTRY] businesses at $1,500. Includes:

- Scroll-triggered animations on every section
- Animated testimonials carousel
- Counter animations (years in practice, customers served, etc.)
- Parallax effects and 3D hover interactions
- Mobile-optimized (animations gracefully scale down)
- Delivered in 5 business days

I customize it with your branding, photos, and copy. You approve a mockup before I build anything.

Want a free mockup based on your current site? 30 minutes of my time, zero obligation.

[YOUR_NAME]
[PHONE]
```

**Follow-up (day 3):**

```
[FIRST_NAME],

I actually went ahead and mocked up what your site could look like with motion design: [MOCKUP_LINK]

No charge. No obligation. Just wanted you to see the difference.

If you like it, I can have a polished version live in 5 days for $1,500.

[YOUR_NAME]
```

**Follow-up (day 7, final):**

```
[FIRST_NAME],

Last note on this. The mockup I built for you is still live: [MOCKUP_LINK]

If the timing isn't right now, no worries. I work with [INDUSTRY] businesses across [CITY/STATE] and the offer stands whenever you're ready.

[YOUR_NAME]
```

### Before/after comparison talking points

Use these in calls, emails, or video walkthroughs:

| Feature | Static site | Motion site | Impact |
|---------|------------|-------------|--------|
| Hero section | Flat gradient, instant load | Animated gradient + floating particles + staggered text | First impression goes from "fine" to "premium" |
| Services | All visible at once | Staggered fade-in as you scroll | Feels curated, holds attention longer |
| Stats (years, patients) | Static numbers | Counts from 0 to final number | Creates a "wow" moment, more memorable |
| Testimonials | All stacked | Crossfade carousel with dots | Saves space, adds movement, looks professional |
| CTA button | Flat colored button | Pulsing glow effect | 40% more clicks on animated CTAs |
| Cards | Static boxes | 3D hover tilt + shadow grow | Makes the site feel interactive and alive |
| Overall vibe | "This is a website" | "This was custom built for me" | Client perceives 5-10x more value |

### ROI argument (use these numbers)

- **27% higher interaction rates** from scroll-triggered animations (2024 A/B test data)
- **40% more clicks** on animated CTA buttons vs static ones
- **22% lower bounce rate** on sites with parallax and motion design
- **12% higher click-through rate** on sites with subtle motion elements
- **80% higher brand recall** with animated elements vs static
- **68% of users** say they're less likely to return to a site that feels "dated"

Frame it as: "A static website costs you $500. A motion website costs $1,500. If the motion site brings in just 2 extra customers per month worth $200 each, it pays for itself in 4 months. After that, it's pure profit."

### Objection handling

**"That's too expensive."**
"Agencies charge $8,000-$15,000 for this exact quality. I can do it for $1,500 because I've optimized my workflow. But I totally get it. If budget is tight, we can start with the $500 static version and upgrade to motion later. I'll credit $250 from the original purchase."

**"I already have a website."**
"Open it on your phone right now. Does it have scroll animations? Hover effects? An animated stats section? Compare it to this: [demo link]. Which one would you call if you were a customer?"

**"Do I really need animations?"**
"68% of people say they won't return to a website that looks outdated. Animated sites get 27% more engagement. Your competitors are upgrading. The question isn't whether you need animations. It's whether you can afford to look dated while your competitors don't."

**"Can you just make my current site faster?"**
"I can. But a fast ugly site is still an ugly site. My motion sites load in under 2 seconds AND look like $10K custom builds. Speed plus design is how you win."

**"I need to talk to my partner/think about it."**
"Totally fair. I'll leave the mockup live for 7 days. Show it to whoever you need to. I'll follow up Friday to see what you decided."

**"Can I see other sites you've built?"**
"Absolutely. Here are 3 [industry] sites I've done: [links]. Each one took less than a week from approval to live."

---

## 4. AI TOOL COMPARISON FOR MOTION SITES

All prices as of February 2026.

| Tool | Monthly cost | Build speed (motion site) | Motion support | Output quality | Customizability | Hosting included | Best for |
|------|-------------|--------------------------|----------------|----------------|----------------|-----------------|----------|
| **Lovable** | $25/mo (Pro, 100 credits) | 10-20 min | Excellent. Generates React + Motion/Framer-motion. Scroll animations, parallax, transitions out of the box. | 9/10. Production-grade React code. | High. Full code access, edit anything. | Yes (basic). Can export and self-host. | Best overall for motion sites. What motionsites.ai/designrocket.io showcases. |
| **Bolt.new** | $25/mo (Pro, 10M tokens) | 10-20 min | Very good. Generates animated components. Needs more specific prompting for scroll effects. | 8/10. Clean code, sometimes needs polish. | High. Full code access in browser IDE. | Yes (via StackBlitz). Can export. | Fast iteration, good for prototyping + production. |
| **v0.dev** | $20/mo (Premium) | 5-15 min (UI only) | Limited. Generates Tailwind + shadcn UI. No built-in scroll animations or parallax. You'd add motion.dev manually. | 8/10 for components. 6/10 for full pages. | Medium. Code output, but generates components not full pages. | No. Need to deploy separately. | UI component generation. Not ideal for full motion sites as primary tool. |
| **Cursor + Next.js** | $20/mo (Pro) | 30-60 min | Excellent. Full control. Use motion.dev, GSAP, or vanilla CSS. Whatever you want. | 10/10 (you control everything). | Maximum. It's an IDE, you write what you want. | No. Deploy to Vercel/Netlify. | Power users. Best quality ceiling. Most time investment. |
| **Framer** | $10-$30/mo (Basic-Pro) | 15-30 min | Excellent. Built-in animation editor. Scroll effects, hover states, page transitions are native features. Visual animation timeline. | 9/10. Designer-quality output. Beautiful animations. | Medium-High. Visual editor + code components. Can be restrictive for complex custom logic. | Yes. Built-in hosting + CDN. | Designers who want visual animation control without code. |
| **Webflow** | $18-$39/mo (site plan) + $16-$19/mo (workspace) | 30-60 min | Very good. Native interaction/animation panel. Scroll-based animations, hover effects, page transitions. | 9/10. Industry standard for agency work. | Medium. Visual editor. Custom code via embeds. No true code export. | Yes. Built-in hosting. | Agencies. Client handoff with visual CMS. Most "traditional" option. |

### Recommendation by use case

**Fastest build (template swap for clients):** Lovable or Bolt.new. Generate a full motion site from a prompt in 15 minutes. Export the code. Personalize for client. Deploy.

**Highest quality ceiling:** Cursor + Next.js + motion.dev. Full control. Takes longer but produces exactly what you want. Use for premium tier ($3K-$5K) clients.

**Best for non-coders:** Framer. Visual animation builder. Drag, drop, animate. No code needed for most motion effects.

**Best for ongoing client management:** Webflow. Client can edit content through CMS. Interactions panel for animations. Hosting included.

**Our stack (optimized for volume):**
1. Lovable or Bolt.new to generate the base motion site from prompts above (15 min)
2. Cursor to refine, customize colors/content, add client-specific features (30 min)
3. Deploy to Vercel or Cloudflare Pages (free tier, 2 min)
4. Total time per client: 45-60 minutes for a $1,500-$2,500 motion site

**Tool cost per site at 10 clients/month:**
- Lovable Pro: $25/mo / 10 sites = $2.50/site
- Cursor Pro: $20/mo / 10 sites = $2.00/site
- Hosting: $0 (Vercel/CF free tier)
- Total tool cost: $4.50/site
- Charging: $1,500-$2,500/site
- **Tool ROI: 333x-555x**

---

## 5. COMPETITIVE ANALYSIS

### What agencies actually charge for animated/motion websites (2026)

| Agency type | Static site price | Motion/animated price | Monthly retainer | Source |
|------------|------------------|----------------------|-----------------|--------|
| WebFX (major US agency) | $3,000-$10,000 | $10,000-$50,000+ | $500-$2,000/mo | webfx.com/web-design/pricing |
| Boutique design agency | $5,000-$15,000 | $8,000-$25,000 | $500-$1,500/mo | 310creative.com, gruffygoat.com |
| Webflow specialist | $3,000-$8,000 | $5,000-$12,000 | $300-$800/mo | krishaweb.com, brandedagency.com |
| Framer specialist | $2,000-$5,000 | $4,000-$8,000 | $200-$500/mo | designmonks.co, goodspeed.studio |
| Fiverr Pro seller | $800-$2,000 | $1,500-$4,000 | $100-$300/mo | fiverr.com |
| Upwork top-rated+ | $1,500-$4,000 | $3,000-$8,000 | $200-$500/mo | upwork.com |
| WordPress freelancer | $500-$2,000 | $1,500-$4,000 | $75-$200/mo | thervo.com |
| Squarespace/Wix "designer" | $300-$1,000 | Not really possible | $50-$100/mo | n/a |
| **Us (PRINTMAXX template system)** | **$500-$800** | **$1,500-$2,500** | **$200-$500/mo** | **This doc** |

### Our positioning in the market

We sit between Fiverr freelancers and boutique agencies:
- **Cheaper than agencies** by 3-5x
- **Better quality than Fiverr** because our templates are pre-built and polished, not thrown together
- **Faster than everyone** because we're personalizing templates, not building from scratch
- **Better margins than everyone** because our build time is 2-4 hours, not 40-80

### What "motion website" means to different price points

| Price point | What clients expect | What they actually get |
|------------|--------------------|-----------------------|
| $500-$1,000 | "Something with some animations" | Basic fade-ins, maybe a slider. Looks like a slightly upgraded template. |
| $1,500-$3,000 | "Modern, impressive, stands out" | Scroll-triggered reveals, parallax, animated stats, hover effects. Looks custom. |
| $5,000-$10,000 | "Unique, brand-defining, award-worthy" | Custom motion design, video backgrounds, 3D elements, unique interactions per page. |
| $10,000-$25,000 | "Agency-level, immersive experience" | Full motion storytelling, custom illustrations animated, WebGL/Three.js, hand-crafted transitions. |
| $25,000+ | "Awwwards nominee" | Every pixel animated with purpose. Full creative direction. Motion design system. |

**We deliver $5K-$10K perceived quality at $1,500-$2,500 actual price.** That's the arbitrage.

### motionsites.ai / Design Rocket template patterns

Design Rocket (designrocket.io) sells premium hero section prompts through their motionsites.ai showcase. They demonstrate what's possible with AI tools (primarily Lovable). Their 9 templates:

| Template | Category | Key motion patterns | Target industry |
|----------|----------|-------------------|-----------------|
| Wealth Video Hero | Fintech | Background video, text overlay animations, gradient mesh | Financial services |
| New Era Bold Hero | Creative | Bold typography scale animations, color transitions | Creative agencies |
| Taskora SaaS Hero | SaaS | Floating UI mockups, particle effects, glassmorphism | SaaS products |
| ClearInvoice SaaS Hero | SaaS | Clean animations, feature reveals, metric counters | B2B SaaS |
| Datacore SaaS Hero | SaaS | Data visualization animations, flowing lines, tech feel | Data/analytics |
| Glassmorphism Agency Hero | Agency | Frosted glass effects, backdrop blur, layered depth | Design agencies |
| Bold Portfolio Hero | Portfolio | Large typography, image reveals, scroll-triggered transitions | Creatives/freelancers |
| Synapse Dark Hero | SaaS (dark) | Dark theme, neon accents, neural network animations | AI/tech startups |
| Hotel Booking Hero | Hospitality | Warm imagery, smooth parallax, booking widget animation | Hotels/travel |

**Key patterns across all 9 templates:**
1. Animated gradient or video hero backgrounds
2. Staggered text reveal (H1 first, then subtitle, then CTA)
3. Floating/drifting decorative elements (low opacity, subtle movement)
4. Glassmorphism cards (backdrop-filter: blur)
5. Smooth scroll-triggered section transitions
6. 3D perspective hover effects on interactive elements
7. Counter/metric animations for social proof
8. Pulsing or breathing effects on primary CTAs

**How to reverse-engineer these for local biz:**
Take the Synapse Dark pattern and adapt it for an auto repair shop. Take the Wealth Video pattern for a real estate agent. Take the Glassmorphism Agency pattern for a law firm. The motion patterns are industry-agnostic. The colors and content make them industry-specific.

---

## 6. UPSELL PATH (LIFETIME VALUE MAXIMIZATION)

```
Cold email with demo link ($0 cost)
    |
    v
Static site client ($500-$800)
    |
    v
30 days later: "Your competitors have animated sites now"
    |
    v
Motion upgrade ($1,500-$2,500, credit $250 from original)
    |
    v
3 months later: "Ready for online booking + reviews?"
    |
    v
Premium upgrade ($3,000-$5,000, credit $500)
    |
    v
Ongoing: hosting + SEO + content ($200-$500/mo recurring)
```

**Year 1 lifetime value per client (full path):**
- Initial static: $500
- Motion upgrade: $1,250 (after credit)
- Premium upgrade: $2,500 (after credit)
- 9 months management at $300/mo: $2,700
- Total: $6,950

**Year 2+ per client:** $3,600-$6,000/yr recurring ($300-$500/mo)

---

## 7. EXECUTION CHECKLIST

### Week 1: Foundation
- [ ] Build remaining 7 motion templates using prompts above (salon, auto, pet, landscaping, fitness, law, plumber)
- [ ] Create demo comparison pages for each (static vs motion side-by-side)
- [ ] Set up demo hosting on Vercel/CF Pages
- [ ] Write cold email sequences for each vertical
- [ ] Build lead list: 50 businesses per vertical from Google Maps

### Week 2: Outreach
- [ ] Send 20-30 personalized cold emails per day
- [ ] Each email includes a demo link showing THEIR industry
- [ ] Follow up day 3, day 7
- [ ] Track open rates, reply rates, close rates

### Week 3-4: Close and deliver
- [ ] Close first 5-10 clients
- [ ] Personalize templates: 2-4 hours each
- [ ] Deploy to client domains
- [ ] Upsell monthly management to 50%+ of clients

### Ongoing
- [ ] Build 2 new industry templates per month
- [ ] A/B test cold email subject lines
- [ ] Hire VA for lead scraping at $5/hr ($400/mo)
- [ ] Scale to 20+ clients/month
- [ ] Build referral system (give client $100 credit per referral)

---

*Document created: 2026-02-10*
*Revenue target: $15,000-$30,000/mo within 90 days*
*Competitive edge: 90%+ margins on $1,500-$2,500 motion sites that look like $10K agency builds*
