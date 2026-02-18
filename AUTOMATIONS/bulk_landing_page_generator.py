#!/usr/bin/env python3
"""
Bulk Landing Page Generator for Local Businesses
Generates professional, conversion-optimized landing pages for $500 website redesign service.

Usage:
    python bulk_landing_page_generator.py --csv local_biz_prospects.csv
    python bulk_landing_page_generator.py --name "Joe's Plumbing" --category "plumber" --city "Austin TX" --phone "512-555-1234" --preview
"""

import argparse
import csv
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Category-specific templates with professional copy
CATEGORY_TEMPLATES = {
    "dentist": {
        "tagline": "Creating Beautiful, Healthy Smiles",
        "hero_subtitle": "Comprehensive dental care for the whole family in a comfortable, modern setting",
        "services": [
            {"name": "General Dentistry", "desc": "Regular cleanings, exams, and preventive care to keep your smile healthy"},
            {"name": "Cosmetic Dentistry", "desc": "Teeth whitening, veneers, and smile makeovers that boost your confidence"},
            {"name": "Dental Implants", "desc": "Permanent tooth replacement that looks and feels natural"},
            {"name": "Emergency Care", "desc": "Same-day appointments for dental emergencies and urgent pain relief"}
        ],
        "about": "With over 20 years of experience serving our community, we combine advanced dental technology with a gentle, patient-centered approach. Our team is dedicated to making every visit comfortable and stress-free.",
        "colors": {"primary": "#0EA5E9", "secondary": "#0C4A6E", "accent": "#38BDF8"}
    },
    "plumber": {
        "tagline": "Licensed & Insured Plumbing Experts",
        "hero_subtitle": "24/7 emergency service and reliable repairs you can trust",
        "services": [
            {"name": "Emergency Repairs", "desc": "24/7 response for burst pipes, gas leaks, and urgent plumbing issues"},
            {"name": "Drain Cleaning", "desc": "Professional hydro-jetting and rooter service to clear any clog"},
            {"name": "Water Heater Service", "desc": "Installation, repair, and maintenance for tankless and traditional water heaters"},
            {"name": "Pipe Replacement", "desc": "Trenchless technology for minimal disruption to your property"}
        ],
        "about": "Family-owned and operated since 2005, we're your neighbors committed to honest pricing and quality workmanship. All technicians are licensed, background-checked, and trained in the latest plumbing technology.",
        "colors": {"primary": "#DC2626", "secondary": "#991B1B", "accent": "#F87171"}
    },
    "electrician": {
        "tagline": "Licensed Electrical Contractors",
        "hero_subtitle": "Safe, reliable electrical services for homes and businesses",
        "services": [
            {"name": "Electrical Repairs", "desc": "Fast diagnosis and repair of outlets, switches, breakers, and wiring issues"},
            {"name": "Panel Upgrades", "desc": "Modern electrical panels to meet your home's power demands safely"},
            {"name": "Lighting Installation", "desc": "Indoor and outdoor lighting design, including LED and smart lighting"},
            {"name": "Generator Installation", "desc": "Whole-home backup generators for uninterrupted power during outages"}
        ],
        "about": "With master electricians on staff and thousands of satisfied customers, we handle everything from simple repairs to complete rewiring. Safety is our top priority, and all work is guaranteed.",
        "colors": {"primary": "#F59E0B", "secondary": "#B45309", "accent": "#FCD34D"}
    },
    "hvac": {
        "tagline": "Heating & Cooling Specialists",
        "hero_subtitle": "Keep your home comfortable year-round with expert HVAC service",
        "services": [
            {"name": "AC Repair & Service", "desc": "Fast repairs and seasonal tune-ups to keep your AC running efficiently"},
            {"name": "Heating Systems", "desc": "Furnace and heat pump installation, repair, and maintenance"},
            {"name": "HVAC Installation", "desc": "Energy-efficient system installations with flexible financing options"},
            {"name": "Air Quality", "desc": "Indoor air quality solutions including filters, purifiers, and humidifiers"}
        ],
        "about": "As a certified HVAC contractor with 15+ years in the business, we provide honest assessments, upfront pricing, and expert installation. We're available 24/7 for emergency service.",
        "colors": {"primary": "#10B981", "secondary": "#047857", "accent": "#6EE7B7"}
    },
    "restaurant": {
        "tagline": "Where Every Meal is a Memory",
        "hero_subtitle": "Fresh ingredients, bold flavors, and warm hospitality",
        "services": [
            {"name": "Dine-In Experience", "desc": "Enjoy our full menu in a welcoming atmosphere perfect for any occasion"},
            {"name": "Takeout & Delivery", "desc": "Your favorite dishes prepared fresh and ready when you are"},
            {"name": "Catering Services", "desc": "Full-service catering for events, parties, and corporate gatherings"},
            {"name": "Private Events", "desc": "Host your special event in our private dining area with custom menus"}
        ],
        "about": "Our chef-driven menu celebrates local ingredients and traditional recipes with a modern twist. Whether you're joining us for a casual lunch or a special celebration, we're committed to exceptional food and service.",
        "colors": {"primary": "#EF4444", "secondary": "#B91C1C", "accent": "#FCA5A5"}
    },
    "law_firm": {
        "tagline": "Experienced Legal Representation",
        "hero_subtitle": "Protecting your rights with personalized attention and proven results",
        "services": [
            {"name": "Personal Injury", "desc": "Fight for the compensation you deserve after accidents, injuries, and negligence"},
            {"name": "Family Law", "desc": "Compassionate guidance through divorce, custody, and family matters"},
            {"name": "Estate Planning", "desc": "Wills, trusts, and estate plans that protect your legacy"},
            {"name": "Business Law", "desc": "Legal counsel for contracts, formation, disputes, and transactions"}
        ],
        "about": "With decades of combined legal experience, our attorneys provide aggressive advocacy and strategic counsel. We offer free consultations and work on contingency for personal injury cases.",
        "colors": {"primary": "#1E40AF", "secondary": "#1E3A8A", "accent": "#60A5FA"}
    },
    "real_estate": {
        "tagline": "Your Trusted Real Estate Partner",
        "hero_subtitle": "Expert guidance for buying, selling, and investing in property",
        "services": [
            {"name": "Home Buying", "desc": "Find your dream home with personalized search and negotiation expertise"},
            {"name": "Home Selling", "desc": "Maximize your sale price with professional marketing and staging"},
            {"name": "Investment Properties", "desc": "Build wealth through strategic real estate investments"},
            {"name": "Property Management", "desc": "Full-service management for rental properties and landlords"}
        ],
        "about": "As a top-producing agent with deep local market knowledge, I'm committed to making your real estate experience smooth and successful. My clients benefit from cutting-edge marketing and skilled negotiation.",
        "colors": {"primary": "#7C3AED", "secondary": "#5B21B6", "accent": "#A78BFA"}
    },
    "salon": {
        "tagline": "Where Beauty Meets Artistry",
        "hero_subtitle": "Expert cuts, color, and styling in a relaxing, upscale environment",
        "services": [
            {"name": "Hair Services", "desc": "Precision cuts, balayage, highlights, and custom color by master stylists"},
            {"name": "Nail Services", "desc": "Manicures, pedicures, gel polish, and nail art in a spa-like setting"},
            {"name": "Skincare", "desc": "Facials, waxing, and treatments for glowing, healthy skin"},
            {"name": "Special Events", "desc": "Bridal hair, makeup, and styling for weddings and special occasions"}
        ],
        "about": "Our team of licensed professionals stays current with the latest techniques and trends. We use premium products and create a welcoming atmosphere where you can relax and leave looking your best.",
        "colors": {"primary": "#EC4899", "secondary": "#BE185D", "accent": "#F9A8D4"}
    },
    "gym": {
        "tagline": "Transform Your Life Through Fitness",
        "hero_subtitle": "State-of-the-art equipment, expert trainers, and a supportive community",
        "services": [
            {"name": "Personal Training", "desc": "One-on-one coaching customized to your goals, fitness level, and schedule"},
            {"name": "Group Classes", "desc": "Energizing classes including yoga, spin, HIIT, and strength training"},
            {"name": "Nutrition Coaching", "desc": "Meal planning and nutritional guidance to fuel your results"},
            {"name": "24/7 Access", "desc": "Work out on your schedule with round-the-clock gym access"}
        ],
        "about": "More than just a gym, we're a community dedicated to helping you achieve your fitness goals. With certified trainers, clean facilities, and flexible membership options, we make fitness accessible for everyone.",
        "colors": {"primary": "#059669", "secondary": "#047857", "accent": "#6EE7B7"}
    },
    "auto_repair": {
        "tagline": "Honest Auto Repair You Can Trust",
        "hero_subtitle": "ASE-certified mechanics and transparent pricing for all makes and models",
        "services": [
            {"name": "Oil Changes & Maintenance", "desc": "Keep your vehicle running smoothly with regular maintenance services"},
            {"name": "Brake Service", "desc": "Expert brake repairs and replacements for safe, reliable stopping power"},
            {"name": "Engine Diagnostics", "desc": "Advanced computer diagnostics to quickly identify and fix issues"},
            {"name": "AC & Heating", "desc": "Climate control repairs to keep you comfortable in any weather"}
        ],
        "about": "Family-owned since 1998, we treat every vehicle like it's our own. Our ASE-certified technicians provide honest assessments, quality parts, and workmanship you can count on. Free estimates and shuttle service available.",
        "colors": {"primary": "#2563EB", "secondary": "#1E40AF", "accent": "#93C5FD"}
    },
    "landscaping": {
        "tagline": "Creating Outdoor Spaces You'll Love",
        "hero_subtitle": "Professional landscaping and lawn care for beautiful, healthy yards",
        "services": [
            {"name": "Lawn Care", "desc": "Weekly mowing, edging, trimming, and seasonal maintenance programs"},
            {"name": "Landscape Design", "desc": "Custom designs featuring plants, hardscaping, and outdoor living spaces"},
            {"name": "Irrigation Systems", "desc": "Smart irrigation installation and repairs for efficient water management"},
            {"name": "Tree & Shrub Care", "desc": "Pruning, trimming, and treatment to keep your plants healthy and shaped"}
        ],
        "about": "With over 15 years of experience transforming outdoor spaces, we combine horticultural expertise with artistic design. Our licensed team handles everything from routine maintenance to complete landscape renovations.",
        "colors": {"primary": "#16A34A", "secondary": "#15803D", "accent": "#86EFAC"}
    },
    "cleaning_service": {
        "tagline": "Sparkling Clean, Every Time",
        "hero_subtitle": "Professional cleaning services for homes and businesses",
        "services": [
            {"name": "Residential Cleaning", "desc": "Thorough home cleaning on your schedule - weekly, bi-weekly, or monthly"},
            {"name": "Deep Cleaning", "desc": "Intensive cleaning for move-ins, move-outs, or seasonal refresh"},
            {"name": "Commercial Cleaning", "desc": "Professional janitorial services for offices, retail, and facilities"},
            {"name": "Specialty Services", "desc": "Carpet cleaning, window washing, and post-construction cleanup"}
        ],
        "about": "Our insured and background-checked team takes pride in delivering exceptional results. We use eco-friendly products, bring our own supplies, and guarantee your satisfaction with every clean.",
        "colors": {"primary": "#06B6D4", "secondary": "#0E7490", "accent": "#67E8F9"}
    },
    "contractor": {
        "tagline": "Quality Construction & Remodeling",
        "hero_subtitle": "Licensed general contractor for residential and commercial projects",
        "services": [
            {"name": "Kitchen Remodeling", "desc": "Transform your kitchen with custom cabinets, countertops, and layouts"},
            {"name": "Bathroom Renovation", "desc": "Create your dream bathroom with modern fixtures and beautiful tile work"},
            {"name": "Home Additions", "desc": "Expand your living space with room additions and second-story builds"},
            {"name": "Commercial Build-Outs", "desc": "Professional tenant improvements and commercial construction"}
        ],
        "about": "As a fully licensed and insured general contractor, we manage every phase of your project with attention to detail and clear communication. Our team has completed hundreds of successful projects on time and on budget.",
        "colors": {"primary": "#EA580C", "secondary": "#C2410C", "accent": "#FDBA74"}
    },
    "accountant": {
        "tagline": "Expert Tax & Accounting Services",
        "hero_subtitle": "Maximize your returns and minimize your stress with professional tax help",
        "services": [
            {"name": "Tax Preparation", "desc": "Accurate personal and business tax returns with maximum deductions"},
            {"name": "Bookkeeping", "desc": "Monthly bookkeeping services to keep your finances organized year-round"},
            {"name": "Tax Planning", "desc": "Strategic planning to reduce tax liability and optimize financial decisions"},
            {"name": "IRS Representation", "desc": "Expert representation for audits, collections, and tax disputes"}
        ],
        "about": "As a CPA with 20+ years of experience, I provide personalized service and year-round support. My clients benefit from proactive tax strategies, accurate filings, and peace of mind knowing their finances are in expert hands.",
        "colors": {"primary": "#0891B2", "secondary": "#155E75", "accent": "#67E8F9"}
    },
    "chiropractor": {
        "tagline": "Natural Pain Relief & Wellness",
        "hero_subtitle": "Expert chiropractic care to help you live pain-free and feel your best",
        "services": [
            {"name": "Chiropractic Adjustments", "desc": "Gentle, precise adjustments to relieve pain and restore proper alignment"},
            {"name": "Sports Injury Treatment", "desc": "Specialized care for athletes and active individuals recovering from injury"},
            {"name": "Massage Therapy", "desc": "Therapeutic massage to reduce tension, improve circulation, and promote healing"},
            {"name": "Wellness Programs", "desc": "Customized care plans for long-term health, posture, and injury prevention"}
        ],
        "about": "Dr. [Name] is a licensed chiropractor dedicated to treating the root cause of pain, not just the symptoms. We accept most insurance plans and offer same-day appointments for acute pain.",
        "colors": {"primary": "#8B5CF6", "secondary": "#6D28D9", "accent": "#C4B5FD"}
    }
}


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def get_category_template(category: str) -> Dict:
    """Get template for business category, with fallback to generic."""
    category_key = slugify(category).replace('-', '_')

    if category_key in CATEGORY_TEMPLATES:
        return CATEGORY_TEMPLATES[category_key]

    # Fallback for unknown categories
    return {
        "tagline": f"Professional {category.title()} Services",
        "hero_subtitle": f"Quality {category} services you can trust",
        "services": [
            {"name": "Service 1", "desc": "Professional service tailored to your needs"},
            {"name": "Service 2", "desc": "Expert solutions with attention to detail"},
            {"name": "Service 3", "desc": "Reliable service backed by years of experience"},
            {"name": "Service 4", "desc": "Customer-focused approach to every project"}
        ],
        "about": f"We are dedicated professionals providing quality {category} services. With years of experience and a commitment to excellence, we deliver results you can count on.",
        "colors": {"primary": "#3B82F6", "secondary": "#1E40AF", "accent": "#93C5FD"}
    }


def generate_landing_page(business: Dict) -> str:
    """Generate complete HTML landing page for a business."""

    name = business.get('business_name', 'Local Business')
    category = business.get('category', 'business')
    city = business.get('city', 'Your City')
    phone = business.get('phone', '(555) 123-4567')
    email = business.get('email', 'info@business.com')
    url = business.get('url', '')

    template = get_category_template(category)
    colors = template['colors']

    # Generate schema.org structured data
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "description": template['about'],
        "telephone": phone,
        "email": email,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city
        }
    }
    if url:
        schema["url"] = url

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | {template['tagline']} in {city}</title>
    <meta name="description" content="{name} - {template['hero_subtitle']}. Serving {city} with professional {category} services.">
    <meta property="og:title" content="{name} | {template['tagline']}">
    <meta property="og:description" content="{template['hero_subtitle']}">
    <meta property="og:type" content="website">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">
    {str(schema).replace("'", '"')}
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
        .gradient-bg {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        }}
        .text-primary {{ color: {colors['primary']}; }}
        .bg-primary {{ background-color: {colors['primary']}; }}
        .border-primary {{ border-color: {colors['primary']}; }}
        .hover\\:bg-primary:hover {{ background-color: {colors['primary']}; }}
        .bg-accent {{ background-color: {colors['accent']}; }}
    </style>
</head>
<body class="antialiased text-gray-900">

    <!-- Navigation -->
    <nav class="fixed w-full bg-white shadow-md z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <div class="flex-shrink-0">
                    <h1 class="text-2xl font-bold text-primary">{name}</h1>
                </div>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="#services" class="text-gray-700 hover:text-primary transition">Services</a>
                    <a href="#about" class="text-gray-700 hover:text-primary transition">About</a>
                    <a href="#testimonials" class="text-gray-700 hover:text-primary transition">Reviews</a>
                    <a href="#contact" class="text-gray-700 hover:text-primary transition">Contact</a>
                    <a href="tel:{phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')}"
                       class="bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition">
                        Call Now
                    </a>
                </div>
                <div class="md:hidden">
                    <a href="tel:{phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')}"
                       class="bg-primary text-white px-4 py-2 rounded-lg font-semibold text-sm">
                        Call
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-32 pb-20 gradient-bg text-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center max-w-3xl mx-auto">
                <h2 class="text-5xl md:text-6xl font-bold mb-6 leading-tight">
                    {template['tagline']}
                </h2>
                <p class="text-xl md:text-2xl mb-8 text-gray-100 leading-relaxed">
                    {template['hero_subtitle']}
                </p>
                <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
                    <a href="#contact"
                       class="bg-white text-gray-900 px-8 py-4 rounded-lg font-bold text-lg hover:shadow-2xl transition transform hover:scale-105 w-full sm:w-auto">
                        Get Free Quote
                    </a>
                    <a href="tel:{phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')}"
                       class="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-white hover:text-gray-900 transition w-full sm:w-auto">
                        {phone}
                    </a>
                </div>
                <div class="mt-8 flex justify-center items-center space-x-6 text-sm">
                    <div class="flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <span>5-Star Rated</span>
                    </div>
                    <div class="flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                        </svg>
                        <span>Licensed & Insured</span>
                    </div>
                    <div class="flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
                        </svg>
                        <span>Serving {city}</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="py-20 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-5xl font-bold mb-4 text-gray-900">Our Services</h2>
                <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                    Professional {category} services tailored to your needs
                </p>
            </div>
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
"""

    # Add services
    for service in template['services']:
        html += f"""
                <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-2xl transition transform hover:-translate-y-1">
                    <div class="w-16 h-16 bg-accent rounded-full flex items-center justify-center mb-6">
                        <svg class="w-8 h-8 text-primary" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-gray-900">{service['name']}</h3>
                    <p class="text-gray-600 leading-relaxed">{service['desc']}</p>
                </div>
"""

    html += f"""
            </div>
            <div class="text-center mt-12">
                <a href="#contact"
                   class="inline-block bg-primary text-white px-8 py-4 rounded-lg font-bold text-lg hover:opacity-90 transition transform hover:scale-105">
                    Request Free Quote
                </a>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div>
                    <h2 class="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                        Why Choose {name}?
                    </h2>
                    <p class="text-lg text-gray-700 leading-relaxed mb-6">
                        {template['about']}
                    </p>
                    <div class="space-y-4">
                        <div class="flex items-start">
                            <svg class="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            <div>
                                <h4 class="font-bold text-gray-900">Local Experts</h4>
                                <p class="text-gray-600">Proudly serving {city} and surrounding areas</p>
                            </div>
                        </div>
                        <div class="flex items-start">
                            <svg class="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            <div>
                                <h4 class="font-bold text-gray-900">Quality Guaranteed</h4>
                                <p class="text-gray-600">We stand behind our work with a satisfaction guarantee</p>
                            </div>
                        </div>
                        <div class="flex items-start">
                            <svg class="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            <div>
                                <h4 class="font-bold text-gray-900">Transparent Pricing</h4>
                                <p class="text-gray-600">Upfront estimates with no hidden fees</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="relative">
                    <div class="aspect-w-4 aspect-h-3 bg-gray-200 rounded-2xl shadow-2xl">
                        <div class="flex items-center justify-center text-gray-400">
                            <svg class="w-24 h-24" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/>
                            </svg>
                        </div>
                    </div>
                    <div class="absolute -bottom-6 -right-6 bg-primary text-white p-6 rounded-xl shadow-xl">
                        <div class="text-3xl font-bold">100+</div>
                        <div class="text-sm">Happy Customers</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section id="testimonials" class="py-20 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-5xl font-bold mb-4 text-gray-900">What Our Customers Say</h2>
                <p class="text-xl text-gray-600">Real reviews from real customers in {city}</p>
            </div>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="bg-white rounded-xl shadow-lg p-8">
                    <div class="flex mb-4">
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                    </div>
                    <p class="text-gray-700 mb-4 italic">"[YOUR TESTIMONIAL HERE - Replace with actual customer review]"</p>
                    <p class="font-semibold text-gray-900">Customer Name</p>
                    <p class="text-sm text-gray-500">{city}</p>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-8">
                    <div class="flex mb-4">
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                    </div>
                    <p class="text-gray-700 mb-4 italic">"[YOUR TESTIMONIAL HERE - Replace with actual customer review]"</p>
                    <p class="font-semibold text-gray-900">Customer Name</p>
                    <p class="text-sm text-gray-500">{city}</p>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-8">
                    <div class="flex mb-4">
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                    </div>
                    <p class="text-gray-700 mb-4 italic">"[YOUR TESTIMONIAL HERE - Replace with actual customer review]"</p>
                    <p class="font-semibold text-gray-900">Customer Name</p>
                    <p class="text-sm text-gray-500">{city}</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-5xl font-bold mb-4 text-gray-900">Get Your Free Quote</h2>
                <p class="text-xl text-gray-600">Ready to get started? Contact us today</p>
            </div>
            <div class="grid md:grid-cols-2 gap-12">
                <div>
                    <form class="space-y-6">
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
                            <input type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent" placeholder="John Smith">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
                            <input type="email" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent" placeholder="john@example.com">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Phone Number</label>
                            <input type="tel" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent" placeholder="(555) 123-4567">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Message</label>
                            <textarea rows="4" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent" placeholder="Tell us about your project..."></textarea>
                        </div>
                        <button type="submit" class="w-full bg-primary text-white px-8 py-4 rounded-lg font-bold text-lg hover:opacity-90 transition">
                            Request Free Quote
                        </button>
                    </form>
                </div>
                <div class="space-y-8">
                    <div>
                        <h3 class="text-2xl font-bold mb-6 text-gray-900">Contact Information</h3>
                        <div class="space-y-4">
                            <div class="flex items-center">
                                <svg class="w-6 h-6 text-primary mr-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                                </svg>
                                <div>
                                    <div class="font-semibold text-gray-900">Phone</div>
                                    <a href="tel:{phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')}" class="text-primary hover:underline">{phone}</a>
                                </div>
                            </div>
                            <div class="flex items-center">
                                <svg class="w-6 h-6 text-primary mr-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                                </svg>
                                <div>
                                    <div class="font-semibold text-gray-900">Email</div>
                                    <a href="mailto:{email}" class="text-primary hover:underline">{email}</a>
                                </div>
                            </div>
                            <div class="flex items-center">
                                <svg class="w-6 h-6 text-primary mr-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                                </svg>
                                <div>
                                    <div class="font-semibold text-gray-900">Location</div>
                                    <div class="text-gray-600">{city}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <h3 class="text-2xl font-bold mb-6 text-gray-900">Business Hours</h3>
                        <div class="space-y-2 text-gray-700">
                            <div class="flex justify-between">
                                <span class="font-semibold">Monday - Friday:</span>
                                <span>8:00 AM - 6:00 PM</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="font-semibold">Saturday:</span>
                                <span>9:00 AM - 4:00 PM</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="font-semibold">Sunday:</span>
                                <span>Closed</span>
                            </div>
                            <div class="mt-4 p-4 bg-accent rounded-lg">
                                <p class="text-sm font-semibold text-gray-900">Emergency Service Available 24/7</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-3 gap-8 mb-8">
                <div>
                    <h3 class="text-2xl font-bold mb-4">{name}</h3>
                    <p class="text-gray-400 mb-4">{template['hero_subtitle']}</p>
                    <div class="flex space-x-4">
                        <a href="#" class="text-gray-400 hover:text-white transition">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white transition">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073z"/><path d="M12 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                        </a>
                    </div>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="#services" class="hover:text-white transition">Services</a></li>
                        <li><a href="#about" class="hover:text-white transition">About Us</a></li>
                        <li><a href="#testimonials" class="hover:text-white transition">Reviews</a></li>
                        <li><a href="#contact" class="hover:text-white transition">Contact</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Service Area</h4>
                    <p class="text-gray-400">Proudly serving {city} and surrounding areas</p>
                    <p class="text-gray-400 mt-4">{phone}</p>
                    <p class="text-gray-400">{email}</p>
                </div>
            </div>
            <div class="border-t border-gray-800 pt-8 text-center text-gray-400">
                <p>&copy; {datetime.now().year} {name}. All rights reserved.</p>
                <p class="mt-2 text-sm">Licensed, Insured & Background Checked</p>
            </div>
        </div>
    </footer>

</body>
</html>
"""
    return html


def process_csv(csv_path: str, output_dir: Path, preview: bool = False) -> List[Dict]:
    """Process CSV file of businesses and generate landing pages."""
    businesses = []

    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                businesses.append(row)
    except FileNotFoundError:
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    generated = []

    for business in businesses:
        slug = slugify(business.get('business_name', 'business'))
        output_file = output_dir / f"{slug}.html"

        print(f"Generating landing page for {business.get('business_name')}...")

        html = generate_landing_page(business)

        with open(output_file, 'w') as f:
            f.write(html)

        generated.append({
            'business_name': business.get('business_name'),
            'slug': slug,
            'file': str(output_file),
            'category': business.get('category'),
            'city': business.get('city')
        })

        print(f"✓ Generated: {output_file}")

        if preview:
            subprocess.run(['open', str(output_file)])

    return generated


def generate_index_page(generated: List[Dict], output_dir: Path) -> str:
    """Generate index page listing all generated landing pages."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Landing Pages - Preview Index</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-50 p-8">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-bold mb-2 text-gray-900">Generated Landing Pages</h1>
        <p class="text-gray-600 mb-8">Professional $500 website redesigns - preview all generated pages</p>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
"""

    for item in generated:
        html += f"""
            <a href="{item['slug']}.html" class="block bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition">
                <h2 class="text-xl font-bold mb-2 text-gray-900">{item['business_name']}</h2>
                <p class="text-gray-600 mb-1"><span class="font-semibold">Category:</span> {item['category']}</p>
                <p class="text-gray-600 mb-4"><span class="font-semibold">Location:</span> {item['city']}</p>
                <span class="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                    View Landing Page →
                </span>
            </a>
"""

    html += f"""
        </div>

        <div class="mt-12 bg-white rounded-lg shadow-md p-6">
            <h3 class="text-2xl font-bold mb-4 text-gray-900">Generated Files</h3>
            <p class="text-gray-600 mb-4">Total pages generated: <strong>{len(generated)}</strong></p>
            <ul class="space-y-2 text-sm text-gray-700">
"""

    for item in generated:
        html += f"""
                <li class="flex items-center">
                    <svg class="w-4 h-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                    {item['file']}
                </li>
"""

    html += """
            </ul>
        </div>
    </div>
</body>
</html>
"""

    index_path = output_dir / "index.html"
    with open(index_path, 'w') as f:
        f.write(html)

    return str(index_path)


def save_generation_log(generated: List[Dict], output_dir: Path):
    """Save CSV log of generated pages."""
    log_path = output_dir / "generation_log.csv"

    with open(log_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['business_name', 'category', 'city', 'slug', 'file', 'generated_at'])
        writer.writeheader()

        for item in generated:
            writer.writerow({
                'business_name': item['business_name'],
                'category': item['category'],
                'city': item['city'],
                'slug': item['slug'],
                'file': item['file'],
                'generated_at': datetime.now().isoformat()
            })

    print(f"\n✓ Generation log saved: {log_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate professional landing pages for local businesses')

    # CSV mode
    parser.add_argument('--csv', type=str, help='Path to CSV file with business data')

    # Single business mode
    parser.add_argument('--name', type=str, help='Business name')
    parser.add_argument('--category', type=str, help='Business category (dentist, plumber, restaurant, etc.)')
    parser.add_argument('--city', type=str, help='City/location')
    parser.add_argument('--phone', type=str, help='Phone number')
    parser.add_argument('--email', type=str, help='Email address')
    parser.add_argument('--url', type=str, help='Current website URL (optional)')

    # Options
    parser.add_argument('--preview', action='store_true', help='Open generated page in browser')
    parser.add_argument('--output', type=str, default='AUTOMATIONS/output/landing_pages',
                       help='Output directory (default: AUTOMATIONS/output/landing_pages)')

    args = parser.parse_args()

    # Setup output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = []

    if args.csv:
        # CSV mode
        generated = process_csv(args.csv, output_dir, args.preview)

    elif args.name and args.category and args.city:
        # Single business mode
        business = {
            'business_name': args.name,
            'category': args.category,
            'city': args.city,
            'phone': args.phone or '(555) 123-4567',
            'email': args.email or 'info@business.com',
            'url': args.url or ''
        }

        slug = slugify(business['business_name'])
        output_file = output_dir / f"{slug}.html"

        print(f"Generating landing page for {business['business_name']}...")

        html = generate_landing_page(business)

        with open(output_file, 'w') as f:
            f.write(html)

        print(f"✓ Generated: {output_file}")

        generated.append({
            'business_name': business['business_name'],
            'slug': slug,
            'file': str(output_file),
            'category': business['category'],
            'city': business['city']
        })

        if args.preview:
            subprocess.run(['open', str(output_file)])

    else:
        parser.print_help()
        sys.exit(1)

    # Generate index page
    if generated:
        index_path = generate_index_page(generated, output_dir)
        print(f"\n✓ Index page generated: {index_path}")

        # Save log
        save_generation_log(generated, output_dir)

        print(f"\n{'='*60}")
        print(f"SUCCESS: Generated {len(generated)} landing page(s)")
        print(f"{'='*60}")
        print(f"\nView all pages: file://{index_path}")
        print(f"Output directory: {output_dir.absolute()}\n")

        # List available categories
        print("Available categories:")
        for category in sorted(CATEGORY_TEMPLATES.keys()):
            print(f"  - {category}")


if __name__ == '__main__':
    main()
