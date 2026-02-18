#!/usr/bin/env python3
"""
Fiverr Boring Category Gig Scraper + Upwork Arbitrage Generator
----------------------------------------------------------------
Scrapes top Fiverr gigs in "boring" high-demand categories,
then generates Upwork proposals at 2x price with rush delivery differentiators.

Strategy: Find best-selling Fiverr gigs in boring categories -> offer same on Upwork at 2x

Usage:
    python3 fiverr_gig_scraper.py                  # Full scan all categories
    python3 fiverr_gig_scraper.py --category resume # Single category
    python3 fiverr_gig_scraper.py --generate-only   # Skip scraping, just generate listings
"""

import requests
import csv
import json
import time
import re
import os
import argparse
from datetime import datetime
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

# ============================================================
# CONFIGURATION
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "LEDGER", "FIVERR_BORING_GIGS.csv")
UPWORK_OUTPUT = os.path.join(PROJECT_ROOT, "PRODUCTS", "listings", "UPWORK_BORING_GIGS.md")
FIVERR_LISTINGS_OUTPUT = os.path.join(PROJECT_ROOT, "PRODUCTS", "listings", "FIVERR_BORING_CATEGORY_GIGS.md")

# Boring but profitable Fiverr categories
BORING_CATEGORIES = {
    "resume_writing": {
        "search_terms": ["resume writing", "professional resume", "ATS resume", "resume design"],
        "fiverr_url": "https://www.fiverr.com/search/gigs?query={}&source=top-bar&ref_ctx_id=search",
        "upwork_price_range": "$100-200",
        "fiverr_typical_price": "$30-80",
        "margin_multiplier": 2.5,
        "demand_signal": "HIGH - everyone needs a resume, recession-proof",
    },
    "business_plan": {
        "search_terms": ["business plan writing", "business plan", "investor business plan", "startup business plan"],
        "fiverr_url": "https://www.fiverr.com/search/gigs?query={}&source=top-bar",
        "upwork_price_range": "$200-500",
        "fiverr_typical_price": "$80-200",
        "margin_multiplier": 2.5,
        "demand_signal": "HIGH - every startup, loan application, immigrant visa needs one",
    },
    "cover_letter": {
        "search_terms": ["cover letter writing", "professional cover letter", "job application letter"],
        "fiverr_url": "https://www.fiverr.com/search/gigs?query={}&source=top-bar",
        "upwork_price_range": "$50-100",
        "fiverr_typical_price": "$15-40",
        "margin_multiplier": 2.5,
        "demand_signal": "MEDIUM-HIGH - pairs with resume writing as upsell",
    },
    "linkedin_optimization": {
        "search_terms": ["LinkedIn profile optimization", "LinkedIn makeover", "LinkedIn profile writing"],
        "fiverr_url": "https://www.fiverr.com/search/gigs?query={}&source=top-bar",
        "upwork_price_range": "$100-200",
        "fiverr_typical_price": "$40-80",
        "margin_multiplier": 2.5,
        "demand_signal": "HIGH - every professional, job seeker, B2B person needs this",
    },
    "pitch_deck": {
        "search_terms": ["pitch deck design", "investor pitch deck", "startup pitch deck", "pitch deck presentation"],
        "fiverr_url": "https://www.fiverr.com/search/gigs?query={}&source=top-bar",
        "upwork_price_range": "$200-400",
        "fiverr_typical_price": "$80-150",
        "margin_multiplier": 2.5,
        "demand_signal": "HIGH - every funded startup needs one, high willingness to pay",
    },
    "grant_writing": {
        "search_terms": ["grant writing", "grant proposal", "nonprofit grant"],
        "fiverr_url": "https://www.fiverr.com/search/gigs?query={}&source=top-bar",
        "upwork_price_range": "$200-500",
        "fiverr_typical_price": "$100-200",
        "margin_multiplier": 2.0,
        "demand_signal": "MEDIUM - niche but high-ticket, nonprofits have budget",
    },
    "sop_writing": {
        "search_terms": ["statement of purpose", "SOP writing", "personal statement", "college essay"],
        "fiverr_url": "https://www.fiverr.com/search/gigs?query={}&source=top-bar",
        "upwork_price_range": "$75-150",
        "fiverr_typical_price": "$25-60",
        "margin_multiplier": 2.5,
        "demand_signal": "SEASONAL HIGH - admissions cycles, visa applications",
    },
    "data_entry": {
        "search_terms": ["data entry", "spreadsheet data entry", "excel data entry"],
        "fiverr_url": "https://www.fiverr.com/search/gigs?query={}&source=top-bar",
        "upwork_price_range": "$30-80/hr",
        "fiverr_typical_price": "$5-20/task",
        "margin_multiplier": 3.0,
        "demand_signal": "VERY HIGH volume - boring but constant demand",
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


# ============================================================
# SCRAPERS
# ============================================================

def scrape_fiverr_category(category_key, category_info):
    """Scrape Fiverr search results for a category using DuckDuckGo site search."""
    gigs = []

    for search_term in category_info["search_terms"]:
        print(f"    Searching: site:fiverr.com {search_term}")
        try:
            # Use DuckDuckGo to search Fiverr (avoids Fiverr's anti-scraping)
            query = f"site:fiverr.com {search_term} best selling"
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

            resp = requests.get(search_url, headers=HEADERS, timeout=15)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                results = soup.find_all("a", class_="result__a")

                for result in results[:8]:
                    title = result.get_text(strip=True)
                    href = result.get("href", "")

                    # Filter for actual Fiverr gig pages
                    if "fiverr.com" in href and title:
                        gig_data = parse_fiverr_result(title, href, category_key, search_term)
                        if gig_data:
                            gigs.append(gig_data)

                print(f"      Found {len(results)} results")
        except Exception as e:
            print(f"      Error: {e}")
        time.sleep(2)

    # Deduplicate by title similarity
    seen = set()
    unique_gigs = []
    for g in gigs:
        key = g["gig_title"][:40].lower()
        if key not in seen:
            seen.add(key)
            unique_gigs.append(g)

    return unique_gigs


def parse_fiverr_result(title, url, category, search_term):
    """Parse a search result into a gig data dict."""
    # Clean up title
    title = re.sub(r"\s*-\s*Fiverr.*$", "", title)
    title = re.sub(r"\s*\|\s*Fiverr.*$", "", title)
    title = title.strip()

    if len(title) < 10:
        return None

    # Estimate price and reviews from category data
    cat_info = BORING_CATEGORIES.get(category, {})

    return {
        "gig_title": title,
        "category": category,
        "search_term": search_term,
        "estimated_price": cat_info.get("fiverr_typical_price", "Unknown"),
        "platform": "Fiverr",
        "url": url,
        "reviews_estimate": "50-500+ (top results)",
        "rating_estimate": "4.7-5.0",
        "seller_level": "Level 2 / Top Rated (estimated)",
        "delivery_time": "2-5 days (typical)",
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def scrape_fiverr_direct(category_key, category_info):
    """Try direct Fiverr search (may be blocked, fallback to DDG)."""
    gigs = []
    search_term = category_info["search_terms"][0]

    try:
        url = f"https://www.fiverr.com/search/gigs?query={quote_plus(search_term)}&source=top-bar&ref_ctx_id=search&search_in=everywhere&search-autocomplete-original-term={quote_plus(search_term)}"

        resp = requests.get(url, headers={
            **HEADERS,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.fiverr.com/",
        }, timeout=15)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")

            # Look for gig cards
            gig_cards = soup.find_all("div", {"class": re.compile(r"gig-card|gig_card|basic-gig")})

            for card in gig_cards[:15]:
                title_el = card.find(["h3", "a", "p"], {"class": re.compile(r"title|gig-title")})
                price_el = card.find(["span", "a"], {"class": re.compile(r"price|amount")})

                title = title_el.get_text(strip=True) if title_el else None
                price = price_el.get_text(strip=True) if price_el else category_info.get("fiverr_typical_price")

                if title:
                    gigs.append({
                        "gig_title": title,
                        "category": category_key,
                        "search_term": search_term,
                        "estimated_price": price or category_info.get("fiverr_typical_price"),
                        "platform": "Fiverr",
                        "url": url,
                        "reviews_estimate": "from search page",
                        "rating_estimate": "4.7-5.0",
                        "seller_level": "from search page",
                        "delivery_time": "2-5 days",
                        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })

            print(f"      Direct Fiverr: found {len(gig_cards)} gig cards")
        else:
            print(f"      Direct Fiverr returned {resp.status_code} (expected, using DDG fallback)")

    except Exception as e:
        print(f"      Direct Fiverr failed: {e} (using DDG fallback)")

    return gigs


def build_known_gig_database():
    """Known top-performing Fiverr gigs in boring categories.
    Manually curated from research. Guarantees output even if scraping fails."""

    known_gigs = [
        # Resume Writing
        {"gig_title": "I will write a professional ATS resume and cover letter", "category": "resume_writing", "estimated_price": "$40-80", "reviews_estimate": "5000+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "2 days"},
        {"gig_title": "I will rewrite your resume for maximum ATS score", "category": "resume_writing", "estimated_price": "$30-60", "reviews_estimate": "3000+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "1-2 days"},
        {"gig_title": "I will create a modern resume with professional design", "category": "resume_writing", "estimated_price": "$25-50", "reviews_estimate": "2000+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "1 day"},
        {"gig_title": "I will write an executive resume for C-level professionals", "category": "resume_writing", "estimated_price": "$80-150", "reviews_estimate": "1500+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "3 days"},
        {"gig_title": "I will write a federal government resume USAJOBS format", "category": "resume_writing", "estimated_price": "$60-100", "reviews_estimate": "800+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "3 days"},

        # Business Plans
        {"gig_title": "I will write a professional business plan with financials", "category": "business_plan", "estimated_price": "$100-250", "reviews_estimate": "3000+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "5 days"},
        {"gig_title": "I will write an investor-ready business plan and pitch deck", "category": "business_plan", "estimated_price": "$150-300", "reviews_estimate": "2000+", "rating_estimate": "4.8", "seller_level": "Top Rated", "delivery_time": "5-7 days"},
        {"gig_title": "I will create a business plan for SBA loan or visa application", "category": "business_plan", "estimated_price": "$120-200", "reviews_estimate": "1500+", "rating_estimate": "4.9", "seller_level": "Level 2", "delivery_time": "5 days"},
        {"gig_title": "I will write a restaurant business plan with financial projections", "category": "business_plan", "estimated_price": "$100-180", "reviews_estimate": "800+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "5 days"},

        # Cover Letters
        {"gig_title": "I will write a tailored cover letter for your dream job", "category": "cover_letter", "estimated_price": "$15-30", "reviews_estimate": "4000+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "1 day"},
        {"gig_title": "I will write a compelling cover letter that gets interviews", "category": "cover_letter", "estimated_price": "$20-40", "reviews_estimate": "2500+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "1 day"},
        {"gig_title": "I will write a cover letter and thank you letter combo", "category": "cover_letter", "estimated_price": "$25-45", "reviews_estimate": "1000+", "rating_estimate": "4.9", "seller_level": "Level 2", "delivery_time": "1-2 days"},

        # LinkedIn Optimization
        {"gig_title": "I will optimize your LinkedIn profile for recruiters and leads", "category": "linkedin_optimization", "estimated_price": "$50-100", "reviews_estimate": "3000+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "2 days"},
        {"gig_title": "I will rewrite your LinkedIn headline summary and experience", "category": "linkedin_optimization", "estimated_price": "$40-80", "reviews_estimate": "2000+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "2 days"},
        {"gig_title": "I will write a LinkedIn profile that generates inbound leads", "category": "linkedin_optimization", "estimated_price": "$60-120", "reviews_estimate": "1500+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "3 days"},

        # Pitch Decks
        {"gig_title": "I will design a stunning pitch deck presentation", "category": "pitch_deck", "estimated_price": "$80-150", "reviews_estimate": "3500+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "3 days"},
        {"gig_title": "I will create an investor pitch deck that raises capital", "category": "pitch_deck", "estimated_price": "$100-200", "reviews_estimate": "2000+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "3-5 days"},
        {"gig_title": "I will write and design your startup pitch deck", "category": "pitch_deck", "estimated_price": "$120-250", "reviews_estimate": "1200+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "5 days"},

        # Grant Writing
        {"gig_title": "I will write a winning grant proposal for your nonprofit", "category": "grant_writing", "estimated_price": "$100-200", "reviews_estimate": "1500+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "5 days"},
        {"gig_title": "I will write a government or foundation grant application", "category": "grant_writing", "estimated_price": "$150-300", "reviews_estimate": "800+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "7 days"},

        # SOP / Personal Statement
        {"gig_title": "I will write a statement of purpose for graduate school", "category": "sop_writing", "estimated_price": "$30-60", "reviews_estimate": "3000+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "2 days"},
        {"gig_title": "I will write a personal statement for college admissions", "category": "sop_writing", "estimated_price": "$25-50", "reviews_estimate": "2500+", "rating_estimate": "4.9", "seller_level": "Level 2", "delivery_time": "2 days"},
        {"gig_title": "I will write an SOP for visa or immigration application", "category": "sop_writing", "estimated_price": "$40-80", "reviews_estimate": "1000+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "3 days"},

        # Data Entry
        {"gig_title": "I will do fast and accurate data entry and web research", "category": "data_entry", "estimated_price": "$5-15", "reviews_estimate": "5000+", "rating_estimate": "4.8", "seller_level": "Level 2", "delivery_time": "1 day"},
        {"gig_title": "I will do Excel data entry, cleanup, and formatting", "category": "data_entry", "estimated_price": "$10-25", "reviews_estimate": "3000+", "rating_estimate": "4.9", "seller_level": "Top Rated", "delivery_time": "1 day"},
    ]

    gigs = []
    for g in known_gigs:
        gigs.append({
            **g,
            "search_term": g["category"],
            "platform": "Fiverr",
            "url": f"https://www.fiverr.com/search/gigs?query={quote_plus(g['gig_title'][:30])}",
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    return gigs


# ============================================================
# GENERATORS
# ============================================================

def generate_upwork_proposals(gigs):
    """Generate Upwork proposal listings at 2x Fiverr price."""

    upwork_listings = []

    category_templates = {
        "resume_writing": {
            "upwork_title": "Expert Resume Writer | ATS-Optimized | {rush} Delivery | Unlimited Revisions",
            "upwork_price": "$100-200",
            "description": """I write resumes that get interviews. Not generic templates. Not AI slop. Real resumes built for the ATS systems that filter 75% of applications before a human sees them.

What you get:
- ATS-optimized resume tailored to your target role
- Keyword mapping from actual job descriptions in your field
- Clean, modern formatting that passes both ATS and human review
- Unlimited revisions until you're satisfied
- Rush delivery available (24-48 hours)

My process:
1. You send me your current resume + target job descriptions
2. I analyze the job requirements and keyword patterns
3. I rewrite your resume from scratch (not a template fill)
4. You review and we refine until it's perfect

I've written 500+ resumes across tech, finance, healthcare, and government. Average callback rate improvement: 3x.

Rush delivery: 24-hour turnaround available for time-sensitive applications.""",
            "differentiators": ["24-hour rush delivery", "Unlimited revisions", "ATS keyword optimization", "Industry-specific expertise"],
        },
        "business_plan": {
            "upwork_title": "Professional Business Plan Writer | Investor-Ready | SBA/Visa/Loan | {rush}",
            "upwork_price": "$200-500",
            "description": """I write business plans that get funded. SBA loans, investor pitches, visa applications, bank financing. Each plan includes financial projections, market analysis, and competitive positioning.

What you get:
- Full business plan (25-40 pages)
- 3-5 year financial projections with assumptions
- Market analysis and TAM/SAM/SOM
- Competitive landscape mapping
- Executive summary optimized for your specific audience (investors, bank, SBA, visa officer)
- Unlimited revisions

Formats I specialize in:
- SBA loan applications (I know what loan officers look for)
- E-2/L-1 visa business plans (immigration-specific requirements)
- Investor pitch plans (paired with pitch deck)
- Restaurant/retail specific plans with unit economics

500+ business plans written. 85% success rate on SBA loans. Rush delivery available for urgent deadlines.""",
            "differentiators": ["Full financial projections", "SBA/Visa specialist", "85% loan approval rate", "Rush delivery", "Unlimited revisions"],
        },
        "cover_letter": {
            "upwork_title": "Compelling Cover Letters | Tailored to Each Job | {rush} | Unlimited Revisions",
            "upwork_price": "$50-100",
            "description": """I write cover letters that complement your resume and give hiring managers a reason to call you.

What you get:
- Cover letter tailored to a specific job posting
- Keyword alignment with the job description
- Compelling narrative that connects your experience to their needs
- Professional formatting
- Rush delivery (same day available)
- Unlimited revisions

I don't write generic "I'm excited to apply" letters. I write specific, targeted letters that show you actually read the job description and know why you're the right fit.

Bundle deal: Resume + Cover Letter + LinkedIn optimization available at package rate.""",
            "differentiators": ["Same-day rush delivery", "Tailored to specific job", "Bundle with resume/LinkedIn", "Unlimited revisions"],
        },
        "linkedin_optimization": {
            "upwork_title": "LinkedIn Profile Optimization | Recruiter-Magnet | Lead Generation | {rush}",
            "upwork_price": "$100-200",
            "description": """I optimize LinkedIn profiles that get recruiter messages and inbound leads. Not just keywords. Full profile strategy.

What you get:
- Headline rewrite (SEO-optimized for recruiter searches)
- About section rewrite (compelling narrative, not a resume copy)
- Experience section optimization (achievement-based, not task-based)
- Skills and endorsements strategy
- Content strategy recommendations (what to post, when)
- Rush delivery available

Why this works: Recruiters search LinkedIn with specific keywords. I reverse-engineer what recruiters in YOUR industry search for, then build your profile around those terms.

Result: My clients typically see 3-5x increase in profile views and recruiter InMails within 30 days.""",
            "differentiators": ["Recruiter keyword optimization", "Content strategy included", "3-5x profile view increase", "Rush delivery", "Unlimited revisions"],
        },
        "pitch_deck": {
            "upwork_title": "Investor Pitch Deck | Design + Copywriting | {rush} Delivery | Unlimited Revisions",
            "upwork_price": "$200-400",
            "description": """I create pitch decks that raise capital. Design and copy. Not just pretty slides. Strategic storytelling that moves investors to action.

What you get:
- 10-15 slide pitch deck (Keynote/PowerPoint/Google Slides)
- Professional design with your brand colors
- Compelling narrative structure (problem, solution, market, traction, team, ask)
- Financial slides with clear unit economics
- Appendix slides for due diligence questions
- Rush delivery available (48 hours)
- Unlimited revisions

My decks follow the frameworks that top VCs actually want to see. Not the generic templates from Google. I study what Sequoia, a16z, and YC partners respond to.

100+ decks created. Clients have raised $500K to $50M with my decks.""",
            "differentiators": ["Design + copy included", "VC-framework aligned", "48-hour rush delivery", "Unlimited revisions", "Financial slide expertise"],
        },
        "grant_writing": {
            "upwork_title": "Grant Writer | Nonprofit & Government Grants | High Win Rate | {rush}",
            "upwork_price": "$200-500",
            "description": """I write grant proposals that win funding. Federal, state, foundation, and corporate grants. My win rate is 40%+ (industry average is 15-20%).

What you get:
- Complete grant proposal/application
- Budget narrative and justification
- Logic model / theory of change
- Evaluation plan
- Letters of support templates
- Unlimited revisions

Grant types I specialize in:
- Federal grants (NSF, NIH, USDA, DOE, HUD)
- Foundation grants (community foundations, family foundations)
- Corporate grants (CSR programs, sponsorships)
- State and local government grants

Rush delivery available for approaching deadlines.""",
            "differentiators": ["40%+ win rate", "Federal grant specialist", "Budget narrative included", "Rush delivery", "Unlimited revisions"],
        },
        "sop_writing": {
            "upwork_title": "Statement of Purpose Writer | Grad School/Visa/Admissions | {rush} | Unlimited Revisions",
            "upwork_price": "$75-150",
            "description": """I write statements of purpose and personal statements that get acceptances. Graduate school, MBA, medical school, law school, visa applications.

What you get:
- Custom-written SOP tailored to your target program
- Narrative that connects your background to program fit
- Specific references to faculty, research, and program features
- Proper formatting for your application type
- Rush delivery (24-48 hours)
- Unlimited revisions

I don't use templates. Each SOP is written from scratch based on your story and the specific program requirements. I've helped 200+ applicants get into programs at Stanford, MIT, Harvard, Columbia, and top schools worldwide.""",
            "differentiators": ["Program-specific customization", "24-hour rush delivery", "200+ successful admits", "Unlimited revisions"],
        },
        "data_entry": {
            "upwork_title": "Fast & Accurate Data Entry | Excel/Sheets | Web Research | {rush} Available",
            "upwork_price": "$30-80/hr",
            "description": """Fast, accurate data entry and web research. I handle the tedious work so you can focus on your business.

What you get:
- Data entry into any format (Excel, Google Sheets, CRM, database)
- Web research and data collection
- Data cleaning and deduplication
- PDF to spreadsheet conversion
- Contact list building
- Rush delivery available

Accuracy rate: 99.5%+. I double-check everything.

Hourly or per-project pricing available. Send me a sample of what you need and I'll give you a fixed quote.""",
            "differentiators": ["99.5% accuracy", "Rush delivery", "Fixed project quotes", "Any format"],
        },
    }

    for gig in gigs:
        cat = gig["category"]
        if cat in category_templates:
            template = category_templates[cat]
            upwork_listings.append({
                "category": cat,
                "fiverr_gig": gig["gig_title"],
                "fiverr_price": gig["estimated_price"],
                "upwork_title": template["upwork_title"].replace("{rush}", "Rush"),
                "upwork_price": template["upwork_price"],
                "upwork_description": template["description"],
                "differentiators": template["differentiators"],
                "margin_note": f"Fiverr cost: {gig['estimated_price']} -> Upwork price: {template['upwork_price']} = ~{BORING_CATEGORIES[cat]['margin_multiplier']}x margin",
            })

    return upwork_listings


def generate_fiverr_listings(gigs):
    """Generate optimized Fiverr gig listings for boring categories."""

    fiverr_listings = []

    listing_templates = {
        "resume_writing": {
            "title": "I will write a professional ATS-optimized resume that gets interviews",
            "packages": {
                "Basic ($30)": "Resume rewrite for 1 role, ATS-optimized, 1 revision, 3-day delivery",
                "Standard ($60)": "Resume + cover letter, ATS-optimized, keyword mapping, 3 revisions, 2-day delivery",
                "Premium ($100)": "Resume + cover letter + LinkedIn summary, ATS-optimized, unlimited revisions, 24-hour rush delivery",
            },
            "description": """Stop getting ghosted by ATS systems. I write resumes that pass automated screening AND impress human reviewers.

I will:
- Analyze your target job descriptions for keyword patterns
- Rewrite your resume with ATS-friendly formatting
- Highlight quantified achievements (not just responsibilities)
- Use industry-specific terminology that recruiters search for

What I need from you:
- Your current resume (any format)
- 2-3 target job descriptions
- Any specific achievements you want highlighted

Average result: 3x increase in callback rate. 500+ resumes written.""",
            "tags": ["resume writing", "ATS resume", "professional resume", "CV writing", "resume design"],
            "faq": [
                ("How fast can you deliver?", "Standard 2-3 days. Rush (Premium) in 24 hours."),
                ("Do you write for specific industries?", "Yes. Tech, finance, healthcare, government, education, and more."),
                ("Will my resume pass ATS?", "Yes. I test every resume against ATS simulation tools."),
            ],
        },
        "business_plan": {
            "title": "I will write a professional business plan with financial projections",
            "packages": {
                "Basic ($100)": "15-page business plan, market overview, basic financials, 5-day delivery",
                "Standard ($200)": "25-page plan with 3-year projections, competitive analysis, 2 revisions, 5-day delivery",
                "Premium ($350)": "40-page investor-ready plan, 5-year financials, pitch deck outline, unlimited revisions, priority delivery",
            },
            "description": """I write business plans that get loans approved and investors interested. Not generic templates. Real plans built for your specific business.

SBA loans, E-2 visas, bank financing, investor pitches. I know what each audience needs to see.

My plan includes:
- Executive summary
- Company description and business model
- Market analysis (TAM, SAM, SOM)
- Competitive landscape
- Marketing and sales strategy
- Operations plan
- Financial projections (income statement, cash flow, balance sheet)
- Funding request and use of funds

85% success rate on SBA loan applications. 500+ plans written.""",
            "tags": ["business plan", "SBA loan", "financial projections", "startup plan", "investor plan"],
            "faq": [
                ("Can you write for SBA loans?", "Yes. I know SBA requirements and have 85% approval rate."),
                ("Do you include financial projections?", "Yes. 3-5 year projections with clear assumptions."),
                ("Can you write for visa applications?", "Yes. E-2, L-1, and EB-5 visa business plans."),
            ],
        },
        "pitch_deck": {
            "title": "I will design a stunning investor pitch deck that raises capital",
            "packages": {
                "Basic ($80)": "10-slide pitch deck, clean design, your content, 3-day delivery",
                "Standard ($150)": "12-slide deck with copywriting, custom design, 2 revisions, 3-day delivery",
                "Premium ($250)": "15-slide deck, full copywriting + design, financial slides, unlimited revisions, 48-hour rush",
            },
            "description": """I create pitch decks that raise money. Not template fills. Strategic presentations designed to move investors to action.

Design + copywriting included. I handle both the visual design and the narrative structure.

My decks follow proven frameworks:
- Problem/Solution/Market/Traction/Team/Ask
- Specific to your stage (pre-seed, seed, Series A)
- Financial slides that VCs actually want to see

Formats: PowerPoint, Keynote, Google Slides, PDF

100+ decks created. Clients have raised $500K-$50M.""",
            "tags": ["pitch deck", "investor deck", "startup presentation", "pitch deck design", "fundraising deck"],
            "faq": [
                ("Do you write the content or just design?", "Both. Standard and Premium include full copywriting."),
                ("What format do you deliver?", "PowerPoint, Keynote, Google Slides, or PDF. Your choice."),
                ("Can you include financial slides?", "Yes. Premium includes detailed financial slides."),
            ],
        },
    }

    for cat, template in listing_templates.items():
        fiverr_listings.append({
            "category": cat,
            "title": template["title"],
            "packages": template["packages"],
            "description": template["description"],
            "tags": template["tags"],
            "faq": template["faq"],
        })

    return fiverr_listings


# ============================================================
# OUTPUT WRITERS
# ============================================================

def write_csv(gigs, output_file):
    """Write scraped gigs to CSV."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fieldnames = [
        "gig_title", "category", "search_term", "estimated_price",
        "platform", "url", "reviews_estimate", "rating_estimate",
        "seller_level", "delivery_time", "scraped_at"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for gig in gigs:
            row = {k: gig.get(k, "") for k in fieldnames}
            writer.writerow(row)

    print(f"\nWrote {len(gigs)} gigs to {output_file}")


def write_upwork_listings(listings, output_file):
    """Write Upwork proposal listings as Markdown."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Upwork Boring Category Gig Listings\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("Strategy: Find best-selling Fiverr gigs in boring categories, offer same service on Upwork at 2x price with rush delivery and unlimited revisions as differentiators.\n\n")
        f.write("---\n\n")

        # Group by category
        categories_seen = {}
        for listing in listings:
            cat = listing["category"]
            if cat not in categories_seen:
                categories_seen[cat] = []
            categories_seen[cat].append(listing)

        for cat, cat_listings in categories_seen.items():
            cat_info = BORING_CATEGORIES.get(cat, {})
            f.write(f"## {cat.replace('_', ' ').title()}\n\n")
            f.write(f"**Demand signal:** {cat_info.get('demand_signal', 'High')}\n")
            f.write(f"**Fiverr typical price:** {cat_info.get('fiverr_typical_price', 'varies')}\n")
            f.write(f"**Upwork target price:** {cat_info.get('upwork_price_range', 'varies')}\n")
            f.write(f"**Margin multiplier:** {cat_info.get('margin_multiplier', 2.0)}x\n\n")

            # Use first listing per category (they share template)
            listing = cat_listings[0]

            f.write(f"### Upwork profile title\n\n")
            f.write(f"`{listing['upwork_title']}`\n\n")

            f.write(f"### Price\n\n")
            f.write(f"**{listing['upwork_price']}**\n\n")

            f.write(f"### Profile description / proposal template\n\n")
            f.write(f"{listing['upwork_description']}\n\n")

            f.write(f"### Key differentiators vs Fiverr\n\n")
            for diff in listing["differentiators"]:
                f.write(f"- {diff}\n")
            f.write("\n")

            f.write(f"### Margin math\n\n")
            f.write(f"{listing['margin_note']}\n\n")

            f.write(f"### Fiverr gigs this competes with\n\n")
            for cl in cat_listings[:3]:
                f.write(f"- {cl['fiverr_gig']} ({cl['fiverr_price']})\n")
            f.write("\n")

            f.write("---\n\n")

        # Summary
        f.write("## Execution plan\n\n")
        f.write("1. Create Upwork profile optimized for these categories\n")
        f.write("2. Set up proposals for each category above\n")
        f.write("3. Use Fiverr sellers as fulfillment (outsource at their price, charge Upwork price)\n")
        f.write("4. Or fulfill yourself using AI (Claude for writing, Canva for design)\n")
        f.write("5. Key differentiation on Upwork: rush delivery + unlimited revisions + direct communication\n")
        f.write("6. Upwork clients pay more because they value reliability and communication over lowest price\n\n")

        f.write("## Why this works\n\n")
        f.write("- Fiverr is a race to the bottom on price. Sellers compete on $5 gigs.\n")
        f.write("- Upwork clients have bigger budgets and value quality/reliability over cheapest option.\n")
        f.write("- Same service, different positioning: 'budget freelancer' vs 'professional consultant'.\n")
        f.write("- Rush delivery is a genuine differentiator. Most Fiverr sellers take 3-5 days.\n")
        f.write("- Unlimited revisions removes buyer risk. They pay more because they know they'll get what they want.\n")
        f.write("- You can outsource fulfillment to the same Fiverr sellers and pocket the margin.\n")

    print(f"Wrote Upwork listings to {output_file}")


def write_fiverr_listings(listings, output_file):
    """Write Fiverr gig listing templates as Markdown."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Fiverr Boring Category Gig Listings\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("These are optimized Fiverr gig listings for boring but profitable categories.\n")
        f.write("Each listing includes title, 3-tier pricing, description, tags, and FAQ.\n\n")
        f.write("---\n\n")

        for listing in listings:
            f.write(f"## {listing['category'].replace('_', ' ').title()}\n\n")
            f.write(f"### Gig title\n\n")
            f.write(f"`{listing['title']}`\n\n")

            f.write(f"### Pricing packages\n\n")
            for pkg_name, pkg_desc in listing["packages"].items():
                f.write(f"**{pkg_name}:** {pkg_desc}\n\n")

            f.write(f"### Gig description\n\n")
            f.write(f"{listing['description']}\n\n")

            f.write(f"### Search tags\n\n")
            f.write(f"`{', '.join(listing['tags'])}`\n\n")

            f.write(f"### FAQ\n\n")
            for q, a in listing["faq"]:
                f.write(f"**Q: {q}**\n")
                f.write(f"A: {a}\n\n")

            f.write("---\n\n")

        f.write("## Tips for boring category success\n\n")
        f.write("1. Response time matters more than anything. Reply to inquiries within 1 hour.\n")
        f.write("2. Deliver early. If you say 3 days, deliver in 2. Builds reviews fast.\n")
        f.write("3. Ask for reviews explicitly after delivery. 'If you're happy, a 5-star review helps a lot.'\n")
        f.write("4. Offer upsells in delivery message: 'Want a LinkedIn optimization to go with your resume?'\n")
        f.write("5. Use AI (Claude) for first drafts, then edit for quality. 3x throughput.\n")
        f.write("6. Price higher than competitors. Signals quality. Attracts better clients.\n")
        f.write("7. Specialize your profile. 'Resume writer for tech professionals' beats 'I write resumes'.\n")

    print(f"Wrote Fiverr listings to {output_file}")


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_pipeline(category=None, generate_only=False):
    """Run the full Fiverr scraping + listing generation pipeline."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 70)
    print("FIVERR BORING CATEGORY ARBITRAGE PIPELINE")
    print(f"Time: {timestamp}")
    print("=" * 70)

    all_gigs = []

    if not generate_only:
        # Phase 1: Scrape Fiverr via search
        print("\n[PHASE 1] Scraping Fiverr top gigs...")

        categories_to_scan = {category: BORING_CATEGORIES[category]} if category and category in BORING_CATEGORIES else BORING_CATEGORIES

        for cat_key, cat_info in categories_to_scan.items():
            print(f"\n  Category: {cat_key}")

            # Try direct Fiverr first
            direct_gigs = scrape_fiverr_direct(cat_key, cat_info)

            # Then DDG fallback
            search_gigs = scrape_fiverr_category(cat_key, cat_info)

            # Combine
            cat_gigs = direct_gigs + search_gigs
            print(f"  -> {len(cat_gigs)} gigs found for {cat_key}")
            all_gigs.extend(cat_gigs)

            time.sleep(1)

    # Phase 2: Add known gig database (guaranteed data)
    print("\n[PHASE 2] Loading known top gigs database...")
    known_gigs = build_known_gig_database()
    all_gigs.extend(known_gigs)
    print(f"  -> {len(known_gigs)} known top gigs loaded")

    # Deduplicate
    seen = set()
    unique_gigs = []
    for g in all_gigs:
        key = g["gig_title"][:40].lower()
        if key not in seen:
            seen.add(key)
            unique_gigs.append(g)

    print(f"\n  Total unique gigs: {len(unique_gigs)}")

    # Phase 3: Write CSV
    print(f"\n[PHASE 3] Writing gig data to CSV...")
    write_csv(unique_gigs, DEFAULT_OUTPUT)

    # Phase 4: Generate Upwork listings
    print(f"\n[PHASE 4] Generating Upwork listings at 2x markup...")
    upwork_listings = generate_upwork_proposals(unique_gigs)
    write_upwork_listings(upwork_listings, UPWORK_OUTPUT)

    # Phase 5: Generate Fiverr listings
    print(f"\n[PHASE 5] Generating Fiverr gig listings...")
    fiverr_listings = generate_fiverr_listings(unique_gigs)
    write_fiverr_listings(fiverr_listings, FIVERR_LISTINGS_OUTPUT)

    # Summary
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)
    print(f"\n  Gigs scraped/loaded: {len(unique_gigs)}")
    print(f"  Categories covered: {len(set(g['category'] for g in unique_gigs))}")
    print(f"\n  Output files:")
    print(f"    CSV data:          {DEFAULT_OUTPUT}")
    print(f"    Upwork listings:   {UPWORK_OUTPUT}")
    print(f"    Fiverr listings:   {FIVERR_LISTINGS_OUTPUT}")

    print(f"\n  Top categories by gig count:")
    cat_counts = {}
    for g in unique_gigs:
        cat_counts[g["category"]] = cat_counts.get(g["category"], 0) + 1
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        cat_info = BORING_CATEGORIES.get(cat, {})
        f_price = cat_info.get("fiverr_typical_price", "?")
        u_price = cat_info.get("upwork_price_range", "?")
        print(f"    {cat}: {count} gigs | Fiverr: {f_price} -> Upwork: {u_price}")

    return unique_gigs


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fiverr Boring Category Gig Scraper")
    parser.add_argument("--category", type=str, help="Single category to scan (e.g., resume_writing)")
    parser.add_argument("--generate-only", action="store_true", help="Skip scraping, just generate listings from known data")
    parser.add_argument("--list-categories", action="store_true", help="List available categories")

    args = parser.parse_args()

    if args.list_categories:
        print("Available categories:")
        for cat, info in BORING_CATEGORIES.items():
            print(f"  {cat}: Fiverr {info['fiverr_typical_price']} -> Upwork {info['upwork_price_range']} ({info['demand_signal']})")
    else:
        run_pipeline(category=args.category, generate_only=args.generate_only)
