#!/usr/bin/env python3
"""
Programmatic SEO Generator - PRINTMAXX
Generates hundreds of "[service] in [city]" landing pages for local business targeting.

Usage:
    python3 scripts/programmatic_seo.py generate                           # Generate all 600 pages
    python3 scripts/programmatic_seo.py generate --service "web design" --limit 10  # Specific service
    python3 scripts/programmatic_seo.py stats                              # Show generation stats
"""

import argparse
import os
import re
import sys
import json
import hashlib
import textwrap
from datetime import datetime
from pathlib import Path
from string import Template
from xml.sax.saxutils import escape as xml_escape

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "builds" / "programmatic_seo"

SERVICES = [
    "Web Design",
    "SEO Services",
    "Social Media Management",
    "Google Ads Management",
    "Logo Design",
    "Content Writing",
    "Email Marketing",
    "Website Maintenance",
    "E-commerce Development",
    "Local SEO",
    "Video Production",
    "Branding",
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
    "Indianapolis", "San Francisco", "Seattle", "Denver", "Nashville",
    "Oklahoma City", "El Paso", "Washington DC", "Boston", "Las Vegas",
    "Portland", "Memphis", "Louisville", "Baltimore", "Milwaukee",
    "Albuquerque", "Tucson", "Fresno", "Mesa", "Sacramento",
    "Atlanta", "Kansas City", "Omaha", "Colorado Springs", "Raleigh",
    "Long Beach", "Virginia Beach", "Miami", "Oakland", "Minneapolis",
    "Tampa", "Tulsa", "Arlington", "New Orleans", "Wichita",
]

# Service-specific data for unique, non-generic content per page
SERVICE_DATA = {
    "Web Design": {
        "benefit": "fast, conversion-focused websites that turn visitors into customers",
        "icon": "&#127760;",
        "features": [
            "Custom responsive design built for your brand",
            "Mobile-first layouts that load in under 2 seconds",
            "Conversion-optimized landing pages and CTAs",
            "SEO-friendly architecture from day one",
            "ADA/WCAG accessibility compliance",
            "Ongoing support and iteration after launch",
        ],
        "why": [
            ("Speed", "Sites we build load in under 2s. Slow sites lose 53% of mobile visitors."),
            ("Conversion Focus", "Every element is designed to move visitors toward action. Not just pretty pixels."),
            ("Local Knowledge", "We understand what {city} customers expect. Regional design preferences matter."),
        ],
        "faqs": [
            ("How long does a website project take?", "Most projects go from kickoff to launch in 4-6 weeks. Simple sites can ship in 2 weeks. We move fast without cutting corners."),
            ("How much does a custom website cost?", "Projects start at $2,500 for a 5-page site. E-commerce and complex builds range $5K-15K. We scope every project individually so you only pay for what you need."),
            ("Do you redesign existing websites?", "Yes. We audit your current site, identify conversion leaks, and rebuild with better performance. Most redesigns see 30-50% improvement in lead generation."),
        ],
    },
    "SEO Services": {
        "benefit": "higher Google rankings that drive real traffic and revenue",
        "icon": "&#128270;",
        "features": [
            "Technical SEO audits and fixes",
            "Keyword research targeting buyer-intent terms",
            "On-page optimization for every key page",
            "Local pack and Google Business Profile optimization",
            "Link building with relevant, high-authority sites",
            "Monthly reporting with actual revenue attribution",
        ],
        "why": [
            ("Data-Driven", "Every decision backed by search volume, competition data, and conversion metrics. No guessing."),
            ("Revenue Focus", "Rankings mean nothing without revenue. We track from click to closed deal."),
            ("Local Expertise", "We know the {city} search landscape. Competitor gaps. Seasonal trends. What ranks here."),
        ],
        "faqs": [
            ("How long until I see SEO results?", "Most clients see measurable ranking improvements in 60-90 days. Competitive terms take 4-6 months. We set honest timelines, not hype."),
            ("What's included in your SEO service?", "Technical audit, keyword strategy, on-page optimization, content recommendations, link building, Google Business Profile optimization, and monthly reporting. Full stack, not partial."),
            ("Do you guarantee first page rankings?", "No legitimate SEO company guarantees rankings. Google's algorithm has 200+ factors. What we guarantee: more organic traffic, better rankings for target terms, and clear ROI reporting."),
        ],
    },
    "Social Media Management": {
        "benefit": "social media that builds an audience and drives real business results",
        "icon": "&#128241;",
        "features": [
            "Platform-specific content strategy",
            "Daily posting and community engagement",
            "Paid social campaign management",
            "Analytics and monthly performance reports",
            "Brand voice development and guidelines",
            "Competitor monitoring and trend tracking",
        ],
        "why": [
            ("Platform Expertise", "Each platform has different rules. We know what works on each one in 2026."),
            ("Consistency", "Posting 3x/week beats posting 10x then going silent. We keep your brand active daily."),
            ("Local Targeting", "{city} audiences respond to local content. We create geo-targeted posts that resonate."),
        ],
        "faqs": [
            ("Which platforms should my business be on?", "Depends on where your customers are. B2B = LinkedIn. Local services = Facebook + Instagram. E-commerce = TikTok + Instagram. We audit and recommend based on your audience."),
            ("How many posts per week do you create?", "Standard packages include 12-16 posts per month across 2-3 platforms. We handle content creation, scheduling, and engagement. You approve, we execute."),
            ("Can you manage paid social ads too?", "Yes. We run Meta (Facebook/Instagram), TikTok, and LinkedIn ad campaigns. Ad management starts at $500/month plus ad spend. Most clients see 3-5x ROAS within 90 days."),
        ],
    },
    "Google Ads Management": {
        "benefit": "Google Ads campaigns that generate leads at a profitable cost per acquisition",
        "icon": "&#128176;",
        "features": [
            "Campaign strategy and keyword targeting",
            "Ad copywriting optimized for CTR and conversions",
            "Landing page recommendations for quality score",
            "Bid management and budget optimization",
            "Conversion tracking and attribution setup",
            "Weekly performance reports with actionable insights",
        ],
        "why": [
            ("ROI Obsessed", "We track cost per lead and cost per customer, not just clicks. If it doesn't make money, we cut it."),
            ("Quality Score Focus", "Higher quality scores = lower CPCs. We optimize the full funnel, not just bids."),
            ("Local Targeting", "{city} has specific search patterns and competition levels. We bid strategically for your market."),
        ],
        "faqs": [
            ("How much should I budget for Google Ads?", "Most local businesses see results starting at $1,500-3,000/month in ad spend. Management fee is 15-20% of spend or a flat rate. We'll recommend a budget based on your market and goals."),
            ("How quickly will I see leads from Google Ads?", "Leads can start within 24-48 hours of campaign launch. Optimization to peak performance takes 30-60 days as we gather data and refine targeting."),
            ("What's your average cost per lead?", "Varies by industry. Home services: $25-75. Legal: $50-200. SaaS: $30-150. We benchmark against industry averages and work to beat them."),
        ],
    },
    "Logo Design": {
        "benefit": "a logo that makes your brand instantly recognizable and trustworthy",
        "icon": "&#127912;",
        "features": [
            "Discovery session to understand your brand",
            "3-5 initial concept directions",
            "Unlimited revisions on chosen direction",
            "Full brand file package (SVG, PNG, PDF, EPS)",
            "Brand guidelines document",
            "Social media profile kit included",
        ],
        "why": [
            ("Strategic Design", "A logo isn't art. It's a business tool. Every element communicates something about your brand."),
            ("Versatility", "Your logo needs to work on a billboard and a favicon. We design for every use case from day one."),
            ("Local Understanding", "We research {city} competitors so your logo stands out in your actual market, not just looks good in a vacuum."),
        ],
        "faqs": [
            ("How long does the logo design process take?", "Initial concepts in 5-7 business days. Full delivery including revisions in 2-3 weeks. Rush options available for 48-hour turnaround."),
            ("What files do I receive?", "Complete brand package: vector files (SVG, AI, EPS), raster files (PNG in multiple sizes), PDF, social media kit, favicon, and a brand guidelines document. Everything you need to use your logo anywhere."),
            ("How many revisions are included?", "Unlimited revisions on your chosen concept direction. We don't stop until you're satisfied. Most projects finalize in 2-3 revision rounds."),
        ],
    },
    "Content Writing": {
        "benefit": "content that ranks on Google and converts readers into customers",
        "icon": "&#9997;",
        "features": [
            "SEO-optimized blog posts and articles",
            "Website copy that converts",
            "Email sequences and newsletters",
            "Case studies and white papers",
            "Product descriptions at scale",
            "Content strategy and editorial calendar",
        ],
        "why": [
            ("SEO Native", "Every piece is written for humans first, search engines second. Keyword strategy built in from the outline."),
            ("Conversion Copy", "Content without CTAs is a hobby blog. We write to drive measurable business outcomes."),
            ("Local Angle", "Content about {city} ranks for {city} searches. We weave in local relevance naturally."),
        ],
        "faqs": [
            ("What types of content do you write?", "Blog posts, landing pages, email sequences, case studies, white papers, product descriptions, social media copy, and ad copy. If it has words and needs to convert, we write it."),
            ("How do you ensure content ranks on Google?", "Keyword research before writing. Proper heading structure. Internal linking strategy. Schema markup recommendations. We treat every piece as an SEO asset, not just words on a page."),
            ("What's your turnaround time?", "Blog posts: 3-5 business days. Landing pages: 5-7 days. Large projects (white papers, content batches): 2-3 weeks. Rush delivery available."),
        ],
    },
    "Email Marketing": {
        "benefit": "email campaigns that land in inboxes and generate consistent revenue",
        "icon": "&#128231;",
        "features": [
            "Email strategy and list segmentation",
            "Automated welcome and nurture sequences",
            "Newsletter design and copywriting",
            "A/B testing for subject lines and content",
            "Deliverability optimization (SPF, DKIM, DMARC)",
            "Revenue attribution and performance reporting",
        ],
        "why": [
            ("Deliverability First", "Emails that hit spam are worthless. We set up proper authentication and warmup before sending a single campaign."),
            ("Revenue Per Send", "We track revenue per email, not just open rates. Every send should make money or build toward a sale."),
            ("Local Personalization", "Emails referencing {city} events, weather, and local context see 2-3x higher engagement."),
        ],
        "faqs": [
            ("Which email platform do you recommend?", "Depends on your size. Under 5K contacts: Beehiiv or ConvertKit. 5K-50K: Klaviyo or ActiveCampaign. Enterprise: HubSpot or Marketo. We work with all major platforms."),
            ("How often should I email my list?", "Minimum: once per week. Sweet spot for most businesses: 2-3 times per week. We test frequency for your specific audience and optimize based on unsubscribe rates and revenue."),
            ("What kind of results can I expect?", "Industry average open rate: 20-25%. Our clients average 30-40%. Click rates: industry 2-3%, our clients 5-8%. Revenue: most see 20-30% of total revenue from email within 6 months."),
        ],
    },
    "Website Maintenance": {
        "benefit": "a website that stays fast, secure, and updated without you worrying about it",
        "icon": "&#128295;",
        "features": [
            "Weekly security updates and patches",
            "Daily automated backups",
            "Uptime monitoring (99.9% SLA)",
            "Performance optimization and speed checks",
            "Content updates and minor edits",
            "Monthly health reports",
        ],
        "why": [
            ("Security", "47% of hacked sites are small businesses. We patch vulnerabilities before they become problems."),
            ("Speed", "Sites slow down over time. Plugin bloat, database growth, cache issues. We keep performance optimized monthly."),
            ("Local Support", "Based near {city}, we understand your business hours and urgency. Same-day response for critical issues."),
        ],
        "faqs": [
            ("What does website maintenance include?", "Security updates, backups, uptime monitoring, performance optimization, content edits (up to 2 hours/month), and monthly reporting. Everything to keep your site running without you thinking about it."),
            ("How quickly do you respond to emergencies?", "Critical issues (site down, hacked): 1-hour response time, 24/7. Non-critical: same business day. We monitor your site around the clock."),
            ("Do I need maintenance if my site is new?", "Yes. WordPress sites need updates within weeks of launch. Plugins update constantly. Security vulnerabilities are discovered daily. Maintenance starts on day one."),
        ],
    },
    "E-commerce Development": {
        "benefit": "an online store that sells while you sleep",
        "icon": "&#128722;",
        "features": [
            "Custom Shopify or WooCommerce builds",
            "Product catalog setup and optimization",
            "Payment gateway and checkout optimization",
            "Inventory management integration",
            "Mobile-optimized shopping experience",
            "Conversion rate optimization from launch",
        ],
        "why": [
            ("Conversion Engineering", "Cart abandonment averages 70%. We build stores that recover 15-25% of abandoned carts automatically."),
            ("Speed = Revenue", "Every 1 second of load time costs 7% in conversions. Our stores load in under 2 seconds."),
            ("Local Commerce", "{city} customers want local shipping options and familiar payment methods. We configure stores for your market."),
        ],
        "faqs": [
            ("Shopify or WooCommerce?", "Shopify for simplicity and fast launch. WooCommerce for full customization and lower long-term costs. Under 100 products: Shopify. Complex catalog or custom features: WooCommerce. We build both."),
            ("How long to build an e-commerce site?", "Simple Shopify store: 2-3 weeks. Custom WooCommerce build: 4-8 weeks. Migration from existing platform: 3-6 weeks depending on product count and complexity."),
            ("Do you handle product photography?", "We partner with local photographers in {city} for product shoots. We handle all product listing optimization: titles, descriptions, images, and schema markup for Google Shopping."),
        ],
    },
    "Local SEO": {
        "benefit": "top rankings in Google Maps and local search results for your area",
        "icon": "&#128205;",
        "features": [
            "Google Business Profile optimization",
            "Local citation building and cleanup",
            "Review generation and management strategy",
            "Local link building campaigns",
            "Geo-targeted content creation",
            "Local pack ranking tracking and reporting",
        ],
        "why": [
            ("Map Pack Focus", "46% of Google searches have local intent. The 3-pack gets 44% of clicks. We get you in that pack."),
            ("Review Strategy", "Businesses with 50+ reviews get 266% more leads. We build a system that generates reviews on autopilot."),
            ("Hyperlocal", "We know {city} neighborhoods, landmarks, and search patterns. Generic national SEO misses these signals."),
        ],
        "faqs": [
            ("How long to rank in the Google Map Pack?", "Depends on competition. Low competition: 30-60 days. Medium: 60-120 days. High competition (legal, medical): 4-6 months. We audit your market before making promises."),
            ("How do you get more Google reviews?", "We set up automated review request sequences triggered after service delivery. SMS + email combo. Most clients go from 10 reviews to 50+ in 90 days without it feeling forced."),
            ("Do I need a physical office to rank locally?", "You need a legitimate business address. Service-area businesses can rank without showing their address publicly. We configure your Google Business Profile correctly for your business type."),
        ],
    },
    "Video Production": {
        "benefit": "professional video content that builds trust and drives sales",
        "icon": "&#127909;",
        "features": [
            "Brand story and company overview videos",
            "Product demos and explainer videos",
            "Social media short-form content",
            "Testimonial and case study videos",
            "Drone and aerial footage",
            "Post-production editing and motion graphics",
        ],
        "why": [
            ("Conversion Power", "Landing pages with video convert 80% better. Product pages with video see 144% more add-to-carts."),
            ("Platform Native", "We shoot and edit for each platform. TikTok vertical, YouTube horizontal, Instagram square. Not one-size-fits-all."),
            ("Local Production", "Based in {city}, we know the best locations, lighting conditions, and local talent for authentic shoots."),
        ],
        "faqs": [
            ("How much does video production cost?", "Short social videos: $500-1,500. Brand story video: $2,500-7,500. Full production day with crew: $3,000-10,000. We scope every project to your budget and goals."),
            ("What's the production timeline?", "Pre-production: 1 week. Shoot day: 1 day for most projects. Post-production: 1-2 weeks. Total: 3-4 weeks from kickoff to final delivery."),
            ("Can you create content for social media?", "Yes. We shoot long-form and cut it into 15-60 second clips for TikTok, Reels, and Shorts. One shoot day can yield 20-30 social clips. Maximum ROI on your production investment."),
        ],
    },
    "Branding": {
        "benefit": "a brand identity that commands attention and builds lasting customer loyalty",
        "icon": "&#10024;",
        "features": [
            "Brand strategy and positioning",
            "Visual identity system (logo, colors, typography)",
            "Brand voice and messaging framework",
            "Brand guidelines document",
            "Marketing collateral templates",
            "Brand launch strategy",
        ],
        "why": [
            ("Strategic Foundation", "A brand is not a logo. It's the reason customers choose you over competitors. We build that reason."),
            ("Consistency", "Consistent branding increases revenue by 23%. We create systems that keep your brand tight across every touchpoint."),
            ("Market Position", "We research {city} competitors to position your brand in whitespace. Stand out where others blend in."),
        ],
        "faqs": [
            ("What's the difference between branding and logo design?", "Logo design is one deliverable. Branding is the full identity: strategy, positioning, visual system, voice, messaging, and guidelines. A logo without branding is just a drawing."),
            ("How long does a branding project take?", "Full brand identity: 4-8 weeks. Includes discovery, strategy, visual design, messaging, and guidelines. Rebrands take 6-10 weeks due to audit and transition planning."),
            ("Do I need branding if I already have a logo?", "If your marketing feels inconsistent, you get mistaken for competitors, or your materials look different every time, yes. Branding creates the system that makes everything cohesive."),
        ],
    },
}


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def get_page_html(service, city):
    """Generate a complete HTML page for a service+city combination."""
    data = SERVICE_DATA[service]
    service_slug = slugify(service)
    city_slug = slugify(city)
    now = datetime.now().strftime("%Y-%m-%d")

    title = f"{service} in {city} | Professional {service} Services"
    meta_desc = f"Looking for {service.lower()} in {city}? We build {data['benefit']}. Free consultation. Get a quote today."
    h1 = f"Professional {service} in {city}"

    # Build features list HTML
    features_html = "\n".join(
        f'            <li>{feat}</li>' for feat in data["features"]
    )

    # Build why-us section
    why_items = []
    for heading, desc in data["why"]:
        desc_local = desc.replace("{city}", city)
        why_items.append(
            f"""        <div class="why-card">
            <h3>{heading}</h3>
            <p>{desc_local}</p>
        </div>"""
        )
    why_html = "\n".join(why_items)

    # Build FAQ section + schema
    faq_items_html = []
    faq_schema_items = []
    for question, answer in data["faqs"]:
        answer_local = answer.replace("{city}", city)
        faq_items_html.append(
            f"""        <details>
            <summary>{question}</summary>
            <p>{answer_local}</p>
        </details>"""
        )
        faq_schema_items.append({
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": answer_local,
            }
        })
    faq_html = "\n".join(faq_items_html)

    # Related pages for internal linking
    related_services = [s for s in SERVICES if s != service][:4]
    related_links = []
    for rs in related_services:
        rs_slug = slugify(rs)
        related_links.append(
            f'            <a href="/{rs_slug}/{city_slug}.html">{rs} in {city}</a>'
        )
    # Also link to same service in nearby cities
    city_idx = CITIES.index(city) if city in CITIES else 0
    nearby_cities = [c for c in CITIES if c != city][:4]
    for nc in nearby_cities:
        nc_slug = slugify(nc)
        related_links.append(
            f'            <a href="/{service_slug}/{nc_slug}.html">{service} in {nc}</a>'
        )
    related_html = "\n".join(related_links)

    # Schema markup
    local_biz_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": f"PRINTMAXX {service} - {city}",
        "description": meta_desc,
        "url": f"https://printmaxx.com/{service_slug}/{city_slug}",
        "areaServed": {
            "@type": "City",
            "name": city,
        },
        "serviceType": service,
    }, indent=2)

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema_items,
    }, indent=2)

    # Color generation from service name for visual variety
    hue = int(hashlib.md5(service.encode()).hexdigest()[:4], 16) % 360

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://printmaxx.com/{service_slug}/{city_slug}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:type" content="website">
    <script type="application/ld+json">
{local_biz_schema}
    </script>
    <script type="application/ld+json">
{faq_schema}
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #1a1a2e; line-height: 1.6; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 0 20px; }}
        header {{ background: hsl({hue}, 65%, 25%); color: #fff; padding: 20px 0; }}
        header nav {{ display: flex; justify-content: space-between; align-items: center; }}
        header nav a {{ color: #fff; text-decoration: none; font-weight: 600; }}
        header nav .cta-btn {{ background: hsl({hue}, 80%, 50%); padding: 8px 20px; border-radius: 6px; }}
        .hero {{ background: linear-gradient(135deg, hsl({hue}, 65%, 30%), hsl({hue}, 50%, 18%)); color: #fff; padding: 60px 0; }}
        .hero h1 {{ font-size: 2.2rem; margin-bottom: 16px; line-height: 1.2; }}
        .hero p {{ font-size: 1.15rem; opacity: 0.9; max-width: 600px; margin-bottom: 24px; }}
        .hero .btn {{ display: inline-block; background: #fff; color: hsl({hue}, 65%, 25%); padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 1rem; }}
        .hero .btn:hover {{ opacity: 0.9; }}
        section {{ padding: 48px 0; }}
        section h2 {{ font-size: 1.6rem; margin-bottom: 20px; }}
        .features ul {{ list-style: none; }}
        .features li {{ padding: 10px 0 10px 28px; position: relative; border-bottom: 1px solid #eee; }}
        .features li:before {{ content: "\\2713"; position: absolute; left: 0; color: hsl({hue}, 65%, 40%); font-weight: 700; }}
        .why-section {{ background: #f8f9fa; }}
        .why-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 20px; }}
        .why-card {{ background: #fff; padding: 24px; border-radius: 10px; border: 1px solid #e2e8f0; }}
        .why-card h3 {{ font-size: 1.1rem; margin-bottom: 8px; color: hsl({hue}, 65%, 30%); }}
        .local {{ border-left: 4px solid hsl({hue}, 65%, 45%); padding-left: 20px; }}
        .local h2 {{ margin-bottom: 12px; }}
        details {{ border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 10px; overflow: hidden; }}
        summary {{ padding: 16px 20px; cursor: pointer; font-weight: 600; background: #f8f9fa; }}
        summary:hover {{ background: #eef; }}
        details p {{ padding: 16px 20px; }}
        .cta-section {{ background: hsl({hue}, 65%, 25%); color: #fff; text-align: center; padding: 48px 0; }}
        .cta-section h2 {{ margin-bottom: 12px; }}
        .cta-section p {{ margin-bottom: 24px; opacity: 0.9; }}
        .cta-section .btn {{ display: inline-block; background: #fff; color: hsl({hue}, 65%, 25%); padding: 14px 36px; border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 1.05rem; }}
        .related {{ background: #f8f9fa; }}
        .related-links {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }}
        .related-links a {{ background: #fff; border: 1px solid #ddd; padding: 8px 16px; border-radius: 6px; text-decoration: none; color: hsl({hue}, 65%, 30%); font-size: 0.9rem; }}
        .related-links a:hover {{ background: hsl({hue}, 80%, 95%); }}
        footer {{ background: #1a1a2e; color: #ccc; padding: 32px 0; font-size: 0.85rem; text-align: center; }}
        footer a {{ color: #aaa; text-decoration: none; }}
        @media (max-width: 640px) {{
            .hero h1 {{ font-size: 1.6rem; }}
            .hero {{ padding: 40px 0; }}
            section {{ padding: 32px 0; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <nav>
                <a href="/index.html">PRINTMAXX</a>
                <a href="#contact" class="cta-btn">Free Quote</a>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>{h1}</h1>
            <p>We build {data['benefit']}. Serving businesses in {city} and surrounding areas.</p>
            <a href="#contact" class="btn">Get a Free Consultation</a>
        </div>
    </section>

    <section class="features">
        <div class="container">
            <h2>What you get with our {service.lower()} service</h2>
            <ul>
{features_html}
            </ul>
        </div>
    </section>

    <section class="why-section">
        <div class="container">
            <h2>Why {city} businesses choose us</h2>
            <div class="why-grid">
{why_html}
            </div>
        </div>
    </section>

    <section>
        <div class="container local">
            <h2>{service} built for {city}</h2>
            <p>Every market is different. {city} has its own competitive landscape, customer expectations, and growth opportunities. We don't run cookie-cutter campaigns. We research your specific market, analyze local competitors, and build a strategy that works for {city} businesses.</p>
            <p>Whether you're a startup looking to establish your presence or an established business ready to scale, we tailor our {service.lower()} approach to your goals and your market.</p>
        </div>
    </section>

    <section style="background: #f8f9fa;">
        <div class="container">
            <h2>Frequently asked questions</h2>
{faq_html}
        </div>
    </section>

    <section class="cta-section" id="contact">
        <div class="container">
            <h2>Ready to grow your {city} business?</h2>
            <p>Get a free {service.lower()} consultation. No commitment, no sales pressure. Just a clear plan for what's possible.</p>
            <a href="mailto:hello@printmaxx.com?subject={service} in {city} - Free Consultation" class="btn">Get Your Free Quote</a>
        </div>
    </section>

    <section class="related">
        <div class="container">
            <h2>Related services</h2>
            <div class="related-links">
{related_html}
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} PRINTMAXX. All rights reserved. | <a href="/index.html">All Services</a></p>
        </div>
    </footer>
</body>
</html>"""
    return html


def generate_sitemap(pages):
    """Generate sitemap.xml for all pages."""
    now = datetime.now().strftime("%Y-%m-%d")
    urls = []
    urls.append(f"""    <url>
        <loc>https://printmaxx.com/index.html</loc>
        <lastmod>{now}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>""")
    for service, city in pages:
        service_slug = slugify(service)
        city_slug = slugify(city)
        urls.append(f"""    <url>
        <loc>https://printmaxx.com/{service_slug}/{city_slug}.html</loc>
        <lastmod>{now}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
    urls_xml = "\n".join(urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_xml}
</urlset>"""


def generate_index(pages):
    """Generate index.html directory of all pages."""
    services_html = []
    for service in SERVICES:
        service_slug = slugify(service)
        data = SERVICE_DATA[service]
        city_links = []
        for city in CITIES:
            city_slug = slugify(city)
            city_links.append(
                f'                <a href="/{service_slug}/{city_slug}.html">{city}</a>'
            )
        cities_joined = "\n".join(city_links)
        services_html.append(f"""        <div class="service-group">
            <h2>{data['icon']} {service}</h2>
            <div class="city-grid">
{cities_joined}
            </div>
        </div>""")
    services_joined = "\n".join(services_html)
    total = len(pages)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PRINTMAXX - Professional Digital Services in 50 Cities</title>
    <meta name="description" content="Professional web design, SEO, social media, and digital marketing services in 50 major US cities. Find your city.">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #1a1a2e; line-height: 1.6; background: #f8f9fa; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 20px; }}
        header {{ background: #1a1a2e; color: #fff; padding: 40px 0; text-align: center; }}
        header h1 {{ font-size: 2rem; margin-bottom: 8px; }}
        header p {{ opacity: 0.8; }}
        main {{ padding: 32px 0; }}
        .service-group {{ background: #fff; border-radius: 10px; padding: 24px; margin-bottom: 20px; border: 1px solid #e2e8f0; }}
        .service-group h2 {{ font-size: 1.3rem; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 2px solid #eee; }}
        .city-grid {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .city-grid a {{ background: #f0f4f8; padding: 6px 14px; border-radius: 6px; text-decoration: none; color: #2d3748; font-size: 0.85rem; }}
        .city-grid a:hover {{ background: #e2e8f0; }}
        footer {{ text-align: center; padding: 32px 0; color: #666; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>PRINTMAXX Services Directory</h1>
            <p>{total} pages | {len(SERVICES)} services | {len(CITIES)} cities</p>
        </div>
    </header>
    <main>
        <div class="container">
{services_joined}
        </div>
    </main>
    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} PRINTMAXX. {total} pages generated.</p>
        </div>
    </footer>
</body>
</html>"""


def cmd_generate(args):
    """Generate landing pages."""
    # Determine which service/city combos to generate
    services = SERVICES
    cities = CITIES
    limit = None

    if args.service:
        match = [s for s in SERVICES if s.lower() == args.service.lower()]
        if not match:
            print(f"Error: Unknown service '{args.service}'")
            print(f"Available: {', '.join(SERVICES)}")
            sys.exit(1)
        services = match

    if args.limit:
        limit = args.limit

    pairs = []
    for service in services:
        for city in cities:
            pairs.append((service, city))
            if limit and len(pairs) >= limit:
                break
        if limit and len(pairs) >= limit:
            break

    print(f"Generating {len(pairs)} pages...")
    print(f"  Services: {len(services)}")
    print(f"  Cities: {len(cities)}")
    print(f"  Output: {OUTPUT_DIR}")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0
    total_bytes = 0
    for i, (service, city) in enumerate(pairs):
        service_slug = slugify(service)
        city_slug = slugify(city)

        page_dir = OUTPUT_DIR / service_slug
        page_dir.mkdir(parents=True, exist_ok=True)

        html = get_page_html(service, city)
        page_path = page_dir / f"{city_slug}.html"
        page_path.write_text(html, encoding="utf-8")

        page_size = len(html.encode("utf-8"))
        total_bytes += page_size
        generated += 1

        if (i + 1) % 50 == 0 or (i + 1) == len(pairs):
            print(f"  [{i+1}/{len(pairs)}] Generated {service_slug}/{city_slug}.html ({page_size:,} bytes)")

    # Generate sitemap
    sitemap_xml = generate_sitemap(pairs)
    sitemap_path = OUTPUT_DIR / "sitemap.xml"
    sitemap_path.write_text(sitemap_xml, encoding="utf-8")
    total_bytes += len(sitemap_xml.encode("utf-8"))

    # Generate index
    index_html = generate_index(pairs)
    index_path = OUTPUT_DIR / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    total_bytes += len(index_html.encode("utf-8"))

    print()
    print(f"Done. {generated} pages generated.")
    print(f"  Total size: {total_bytes / 1024 / 1024:.1f} MB ({total_bytes:,} bytes)")
    print(f"  Avg page size: {total_bytes // max(generated, 1):,} bytes")
    print(f"  Sitemap: {sitemap_path}")
    print(f"  Index: {index_path}")
    print(f"  Directory: {OUTPUT_DIR}")


def cmd_stats(args):
    """Show generation stats."""
    if not OUTPUT_DIR.exists():
        print("No pages generated yet. Run: python3 scripts/programmatic_seo.py generate")
        return

    total_files = 0
    total_bytes = 0
    service_counts = {}

    for service_dir in sorted(OUTPUT_DIR.iterdir()):
        if not service_dir.is_dir():
            continue
        html_files = list(service_dir.glob("*.html"))
        count = len(html_files)
        size = sum(f.stat().st_size for f in html_files)
        service_counts[service_dir.name] = (count, size)
        total_files += count
        total_bytes += size

    # Check for sitemap and index
    has_sitemap = (OUTPUT_DIR / "sitemap.xml").exists()
    has_index = (OUTPUT_DIR / "index.html").exists()

    print("=" * 60)
    print("  PROGRAMMATIC SEO - Generation Stats")
    print("=" * 60)
    print()
    print(f"  Total pages:     {total_files}")
    print(f"  Total size:      {total_bytes / 1024 / 1024:.1f} MB ({total_bytes:,} bytes)")
    print(f"  Avg page size:   {total_bytes // max(total_files, 1):,} bytes")
    print(f"  Sitemap:         {'YES' if has_sitemap else 'NO'}")
    print(f"  Index page:      {'YES' if has_index else 'NO'}")
    print(f"  Output dir:      {OUTPUT_DIR}")
    print()
    print(f"  {'Service':<30} {'Pages':>6} {'Size':>10}")
    print(f"  {'-'*30} {'-'*6} {'-'*10}")
    for name, (count, size) in sorted(service_counts.items()):
        print(f"  {name:<30} {count:>6} {size // 1024:>7} KB")
    print()
    print(f"  {'TOTAL':<30} {total_files:>6} {total_bytes // 1024:>7} KB")
    print()

    # Page size distribution
    if total_files > 0:
        sizes = []
        for service_dir in OUTPUT_DIR.iterdir():
            if service_dir.is_dir():
                for f in service_dir.glob("*.html"):
                    sizes.append(f.stat().st_size)
        if sizes:
            sizes.sort()
            print(f"  Size distribution:")
            print(f"    Min:    {sizes[0]:,} bytes")
            print(f"    Median: {sizes[len(sizes)//2]:,} bytes")
            print(f"    Max:    {sizes[-1]:,} bytes")
            over_50k = sum(1 for s in sizes if s > 50 * 1024)
            if over_50k:
                print(f"    Over 50KB: {over_50k} pages (WARNING)")
            else:
                print(f"    All pages under 50KB target")


def main():
    parser = argparse.ArgumentParser(
        description="Programmatic SEO page generator for local business targeting"
    )
    subparsers = parser.add_subparsers(dest="command")

    gen_parser = subparsers.add_parser("generate", help="Generate landing pages")
    gen_parser.add_argument("--service", type=str, help="Generate for specific service only")
    gen_parser.add_argument("--limit", type=int, help="Limit number of pages generated")

    stats_parser = subparsers.add_parser("stats", help="Show generation statistics")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "stats":
        cmd_stats(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
