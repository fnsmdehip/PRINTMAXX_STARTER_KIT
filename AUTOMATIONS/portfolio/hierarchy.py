"""
Method hierarchy module for the PRINTMAXX portfolio.

Defines parent/child relationships and category groupings for all 70+ money methods.
"""

from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Category -> method IDs
# ---------------------------------------------------------------------------

METHOD_HIERARCHY: Dict[str, List[str]] = {
    "APPS_SOFTWARE": [
        "MM001",  # APP_FACTORY
        "MM004",  # SAAS
        "MM011",  # ROBLOX_GAMES
        "MM019",  # PORTFOLIO_APP_BUILDER
        "MM027",  # AI_WRAPPER
        "MM028",  # MICRO_SAAS
        "MM044",  # RAPID_BUILD_MONETIZATION
    ],
    "CONTENT_MEDIA": [
        "MM006",  # CONTENT_FARM (parent of CF001-CF013)
        "MM010",  # STREAMER_CLIPS
        "MM014",  # YOUTUBE_LONGFORM
        "MM035",  # YOUTUBE_AUTOMATION
        "MM039",  # FACELESS_YOUTUBE
        "CF001",  # RELAX_CHANNELS
        "CF002",  # SLEEP_TIMER_ALARM
        "CF003",  # NEWS_SOCIALS
        "CF004",  # MEME_CHANNELS
        "CF005",  # WOMEN_APPRECIATION
        "CF006",  # CLIP_CHANNELS
        "CF007",  # MOTIVATION_QUOTES
        "CF008",  # FINANCE_NEWS
        "CF009",  # TECH_EXPLAINERS
        "CF010",  # SPORTS_HIGHLIGHTS
        "CF011",  # CRYPTO_NEWS
        "CF012",  # STOCK_RESEARCH
        "CF013",  # YOUTUBE_SHORTS
    ],
    "AI_PERSONAS": [
        "MM009",  # AI_INFLUENCER (parent of AI001-AI008)
        "AI001",  # NICHE_EXPERTS
        "AI002",  # FINDOM
        "AI003",  # ONLYFANS_FANSLY
        "AI004",  # ASMR
        "AI005",  # FITNESS_COACHES
        "AI006",  # LIFESTYLE_CURATORS
        "AI007",  # GAMING_PERSONAS
        "AI008",  # RELATIONSHIP_ADVICE
    ],
    "ECOMMERCE": [
        "MM003",  # AFFILIATE_SITES
        "MM016",  # TIKTOK_SHOP
        "MM022",  # ECOM_DROPSHIP
        "MM023",  # ECOM_ARB
        "MM024",  # PRINT_ON_DEMAND
        "MM025",  # DIGITAL_PRODUCTS
        "MM026",  # AMAZON_KDP
        "MM036",  # ETSY_DIGITAL
        "MM038",  # PINTEREST_AFFILIATE
        "MM046",  # NOTION_TEMPLATES
    ],
    "OUTBOUND_SERVICES": [
        "MM005",  # AGENCY_SERVICES
        "MM007",  # COLD_OUTBOUND
        "MM008",  # UGC_ARBITRAGE
        "MM018",  # PAYWALL_OPTIMIZATION_SERVICE
        "MM029",  # LOCAL_LEAD_GEN
        "MM033",  # WHITE_LABEL
        "MM042",  # WAITLIST_PRESALE_SERVICE
        "MM070",  # WEB_REDESIGN_COLD_OUTREACH
    ],
    "FINANCIAL_TRADING": [
        "MM012",  # ALGO_TRADING
        "MM034",  # MEMECOIN_TRADING
        "MM045",  # DOMAIN_FLIPPING
    ],
    "GROWTH_DISTRIBUTION": [
        "MM013",  # PAID_ADS
        "MM015",  # NEWSLETTER
        "MM017",  # MICRO_INFLUENCER_NETWORK
        "MM020",  # X_LAUNCH_VIRAL
        "MM021",  # PERSONAL_BRAND_SEO
        "MM037",  # TIKTOK_CREATIVITY
        "MM040",  # TWITTER_MONETIZATION
        "MM041",  # DIRECTORY_LISTING_SITES
        "MM043",  # INFLUENCER_REVENUE_SHARE
        "SWARM001",  # SWARM_PROMOTION
    ],
    "INFO_EDUCATION": [
        "MM002",  # INFO_PRODUCTS
        "MM030",  # COURSE_CREATOR
        "MM031",  # COMMUNITY_PAID
        "MM032",  # NEWSLETTER_PREMIUM
    ],
    "HARDWARE_PHYSICAL": [
        "PEMF_WEBERMAXX",
    ],
}


# ---------------------------------------------------------------------------
# Display names and icons for TUI rendering
# ---------------------------------------------------------------------------

CATEGORY_DISPLAY_NAMES: Dict[str, str] = {
    "APPS_SOFTWARE": "Apps & Software",
    "CONTENT_MEDIA": "Content & Media",
    "AI_PERSONAS": "AI Personas",
    "ECOMMERCE": "E-Commerce",
    "OUTBOUND_SERVICES": "Outbound & Services",
    "FINANCIAL_TRADING": "Financial & Trading",
    "GROWTH_DISTRIBUTION": "Growth & Distribution",
    "INFO_EDUCATION": "Info & Education",
    "HARDWARE_PHYSICAL": "Hardware & Physical",
}

CATEGORY_ICONS: Dict[str, str] = {
    "APPS_SOFTWARE": "\u25b6",       # right-pointing triangle
    "CONTENT_MEDIA": "\u25cf",       # filled circle
    "AI_PERSONAS": "\u2605",         # star
    "ECOMMERCE": "\u25a0",          # filled square
    "OUTBOUND_SERVICES": "\u2192",   # right arrow
    "FINANCIAL_TRADING": "\u2191",   # up arrow
    "GROWTH_DISTRIBUTION": "\u2740", # flower
    "INFO_EDUCATION": "\u2261",      # triple bar
    "HARDWARE_PHYSICAL": "\u2592",   # medium shade block
}


# ---------------------------------------------------------------------------
# Sub-method parent mapping (child -> parent)
# ---------------------------------------------------------------------------

SUB_METHOD_PARENTS: Dict[str, str] = {
    "CF001": "MM006",
    "CF002": "MM006",
    "CF003": "MM006",
    "CF004": "MM006",
    "CF005": "MM006",
    "CF006": "MM006",
    "CF007": "MM006",
    "CF008": "MM006",
    "CF009": "MM006",
    "CF010": "MM006",
    "CF011": "MM006",
    "CF012": "MM006",
    "CF013": "MM006",
    "AI001": "MM009",
    "AI002": "MM009",
    "AI003": "MM009",
    "AI004": "MM009",
    "AI005": "MM009",
    "AI006": "MM009",
    "AI007": "MM009",
    "AI008": "MM009",
}

# Reverse lookup: parent -> list of children
_PARENT_TO_CHILDREN: Dict[str, List[str]] = {}
for _child, _parent in SUB_METHOD_PARENTS.items():
    _PARENT_TO_CHILDREN.setdefault(_parent, []).append(_child)
for _children in _PARENT_TO_CHILDREN.values():
    _children.sort()


# ---------------------------------------------------------------------------
# Pre-built reverse index: method_id -> category
# ---------------------------------------------------------------------------

_METHOD_TO_CATEGORY: Dict[str, str] = {}
for _cat, _methods in METHOD_HIERARCHY.items():
    for _mid in _methods:
        _METHOD_TO_CATEGORY[_mid] = _cat


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_category_for_method(method_id: str) -> Optional[str]:
    """Return the category key for a given method ID, or None if not found."""
    return _METHOD_TO_CATEGORY.get(method_id)


def get_methods_in_category(category: str) -> List[str]:
    """Return all method IDs in a category. Empty list if category unknown."""
    return list(METHOD_HIERARCHY.get(category, []))


def get_all_categories() -> List[str]:
    """Return category keys in display order."""
    return list(METHOD_HIERARCHY.keys())


def get_category_display_name(category: str) -> str:
    """Return the human-readable display name for a category."""
    return CATEGORY_DISPLAY_NAMES.get(category, category)


def get_sub_methods(parent_id: str) -> List[str]:
    """Return child method IDs for a parent (e.g. MM006 -> CF001-CF013)."""
    return list(_PARENT_TO_CHILDREN.get(parent_id, []))


def get_parent_method(child_id: str) -> Optional[str]:
    """Return the parent method ID for a sub-method, or None."""
    return SUB_METHOD_PARENTS.get(child_id)


def is_sub_method(method_id: str) -> bool:
    """Return True if method_id is a child of another method."""
    return method_id in SUB_METHOD_PARENTS


def get_all_method_ids() -> List[str]:
    """Return every method ID across all categories."""
    result = []
    for methods in METHOD_HIERARCHY.values():
        result.extend(methods)
    return result
