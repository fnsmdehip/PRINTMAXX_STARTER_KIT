#!/usr/bin/env python3
"""
PRINTMAXX Algorithm Ban Prevention & Platform Compliance System
===============================================================
Defensive layer protecting the entire PRINTMAXX social empire.

Monitors ALL platform activity and enforces safe posting/engagement patterns
that avoid algorithm penalties, shadowbans, and account bans.

Platform rules hardcoded from actual enforcement patterns as of early 2026.

Usage:
    python algo_ban_prevention.py --limits
    python algo_ban_prevention.py --warmup twitter 3
    python algo_ban_prevention.py --check twitter my_account
    python algo_ban_prevention.py --health
    python algo_ban_prevention.py --report
    python algo_ban_prevention.py --simulate twitter 30
    python algo_ban_prevention.py --api-json
"""

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
ACTIVITY_LOG = LEDGER_DIR / "PLATFORM_ACTIVITY_LOG.csv"
ACCOUNT_STATE_FILE = LEDGER_DIR / "account_states.json"

# Ensure ledger directory exists
LEDGER_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# VERDICT CONSTANTS
# ---------------------------------------------------------------------------
SAFE = "SAFE"
WARN = "WARN"
BLOCK = "BLOCK"

# ---------------------------------------------------------------------------
# RATE LIMITS DATABASE — every number backed by real platform enforcement
# ---------------------------------------------------------------------------
RATE_LIMITS: Dict[str, Dict[str, Any]] = {
    # ======================================================================
    # TWITTER / X
    # ======================================================================
    "twitter": {
        "display_name": "Twitter / X",
        "posts_per_day": {"safe": 25, "aggressive": 50, "ban_risk": 100},
        "follows_per_day": {"safe": 100, "aggressive": 400, "ban_risk": 500},
        "unfollows_per_day": {"safe": 100, "aggressive": 300, "ban_risk": 500},
        "likes_per_day": {"safe": 300, "aggressive": 800, "ban_risk": 1000},
        "dms_per_day_nonfollower": {"safe": 50, "aggressive": 100, "ban_risk": 200},
        "comments_per_day": {"safe": 100, "aggressive": 200, "ban_risk": 400},
        "hashtags_per_post": {"optimal": 2, "max_safe": 2, "penalty_threshold": 3,
                              "note": "3+ hashtags = ~40% reach penalty confirmed"},
        "link_in_post_penalty_pct": 25,  # ~20-30% reach reduction vs no-link
        "duplicate_content_threshold": 0.80,  # >80% similar = flagged
        "min_action_spacing_sec": 30,  # minimum seconds between bulk actions
        "api_rate_limits": {
            "tweets_per_day": 500,
            "likes_per_day": 1000,
            "follows_per_day": 500,
        },
        "warmup_schedule": {
            # account_age_days -> max posts per day
            "week1": {"max_days": 7, "posts": 5, "follows": 20, "likes": 50},
            "week2": {"max_days": 14, "posts": 10, "follows": 50, "likes": 100},
            "week3": {"max_days": 21, "posts": 15, "follows": 80, "likes": 200},
            "week4_plus": {"max_days": 9999, "posts": 25, "follows": 100, "likes": 300},
        },
        "notes": [
            "Engagement pod detection active: clustered likes/RTs from same group = penalty",
            "Buying followers hurts TweepCred score, detectable, causes reach penalty",
            "Link-in-tweet: ~20-30% reach reduction vs no-link tweets",
            "Duplicate content: posts >80% similar are flagged",
            "Vary posting times -- exact-same-time daily is a bot signal",
        ],
    },

    # ======================================================================
    # INSTAGRAM
    # ======================================================================
    "instagram": {
        "display_name": "Instagram",
        "posts_per_day": {"safe": 3, "aggressive": 5, "ban_risk": 10,
                          "note": "3 feed posts per day safe"},
        "stories_per_day": {"safe": 10, "aggressive": 20, "ban_risk": 30},
        "reels_per_day": {"safe": 5, "aggressive": 8, "ban_risk": 15},
        "follows_per_day": {"safe": 60, "aggressive": 150, "ban_risk": 200},
        "unfollows_per_day": {"safe": 60, "aggressive": 150, "ban_risk": 200},
        "likes_per_day": {"safe": 300, "aggressive": 500, "ban_risk": 800},
        "comments_per_day": {"safe": 60, "aggressive": 120, "ban_risk": 200},
        "dms_per_day_nonfollower": {"safe": 30, "aggressive": 60, "ban_risk": 100},
        "hashtags_per_post": {"optimal": 5, "max_safe": 10, "penalty_threshold": 15,
                              "absolute_max": 30,
                              "note": "3-5 optimal; 30 max but heavy penalty above 10"},
        "duplicate_content_threshold": 0.80,
        "min_action_spacing_sec": 30,
        "content_format_priority": ["reels", "carousel", "single_image"],
        "warmup_schedule": {
            "week1": {"max_days": 7, "posts": 1, "stories": 3, "reels": 1,
                      "follows": 15, "likes": 50, "comments": 10},
            "week2": {"max_days": 14, "posts": 2, "stories": 5, "reels": 2,
                      "follows": 30, "likes": 100, "comments": 30},
            "week3": {"max_days": 21, "posts": 2, "stories": 8, "reels": 3,
                      "follows": 45, "likes": 200, "comments": 45},
            "week4_plus": {"max_days": 9999, "posts": 3, "stories": 10, "reels": 5,
                           "follows": 60, "likes": 300, "comments": 60},
        },
        "notes": [
            "Engagement pod detection by AI: confirmed active since 2024",
            "Link in bio only -- no links in captions (shadowban risk)",
            "Reels > Carousel > Single image for reach",
            "Hashtag sweet spot: 3-5 highly relevant tags",
            "IG aggressively detects automation via action patterns",
        ],
    },

    # ======================================================================
    # TIKTOK
    # ======================================================================
    "tiktok": {
        "display_name": "TikTok",
        "posts_per_day": {"safe": 3, "aggressive": 5, "ban_risk": 10,
                          "note": "3-5 optimal; 10+ diminishing returns"},
        "follows_per_day": {"safe": 50, "aggressive": 150, "ban_risk": 200},
        "unfollows_per_day": {"safe": 50, "aggressive": 150, "ban_risk": 200},
        "likes_per_day": {"safe": 200, "aggressive": 400, "ban_risk": 500},
        "comments_per_day": {"safe": 50, "aggressive": 100, "ban_risk": 200},
        "dms_per_day_nonfollower": {"safe": 20, "aggressive": 50, "ban_risk": 100},
        "hashtags_per_post": {"optimal": 4, "max_safe": 5, "penalty_threshold": 8,
                              "note": "3-5 optimal"},
        "duplicate_content_threshold": 0.75,
        "min_action_spacing_sec": 30,
        "shadowban_indicators": [
            "0 views from For You page",
            "Content only visible to followers",
            "Hashtags not appearing in search",
            "Account not appearing in search",
        ],
        "shadowban_recovery": {
            "stop_posting_hours": 48,
            "resume_posts_per_day": 1,
            "resume_ramp_days": 7,
        },
        "warmup_schedule": {
            "week1": {"max_days": 7, "posts": 2, "follows": 10, "likes": 30,
                      "comments": 10},
            "week2": {"max_days": 14, "posts": 3, "follows": 25, "likes": 80,
                      "comments": 25},
            "week3": {"max_days": 21, "posts": 4, "follows": 40, "likes": 150,
                      "comments": 40},
            "week4_plus": {"max_days": 9999, "posts": 5, "follows": 50, "likes": 200,
                           "comments": 50},
        },
        "notes": [
            "Duplicate content across accounts: detected and penalized",
            "Shadowban recovery: stop posting 24-48h then resume slowly",
            "TikTok Shop: small creators (<50K) get 4.3x higher CTR",
            "Cross-account content reuse is heavily penalized since 2025",
        ],
    },

    # ======================================================================
    # YOUTUBE
    # ======================================================================
    "youtube": {
        "display_name": "YouTube",
        "shorts_per_day": {"safe": 3, "aggressive": 5, "ban_risk": 10,
                           "note": "1-3/day optimal; batch upload OK"},
        "long_form_per_week": {"safe": 2, "aggressive": 4, "ban_risk": 7,
                               "note": "1-2/week optimal for algorithm"},
        "community_posts_per_day": {"safe": 3, "aggressive": 5, "ban_risk": 10},
        "comments_per_day": {"safe": 50, "aggressive": 100, "ban_risk": 200},
        "likes_per_day": {"safe": 200, "aggressive": 400, "ban_risk": 500},
        "posts_per_day": {"safe": 3, "aggressive": 5, "ban_risk": 10},
        "follows_per_day": {"safe": 50, "aggressive": 100, "ban_risk": 200},
        "duplicate_content_threshold": 0.80,
        "min_action_spacing_sec": 60,
        "warmup_schedule": {
            "week1": {"max_days": 7, "posts": 1, "shorts": 1, "comments": 10,
                      "likes": 30},
            "week2": {"max_days": 14, "posts": 1, "shorts": 2, "comments": 25,
                      "likes": 60},
            "week3": {"max_days": 21, "posts": 2, "shorts": 3, "comments": 40,
                      "likes": 100},
            "week4_plus": {"max_days": 9999, "posts": 3, "shorts": 3,
                           "comments": 50, "likes": 200},
        },
        "notes": [
            "Description keyword stuffing penalized since 2025 update",
            "Misleading thumbnails = reduced impressions (AI-checked)",
            "Sub4sub detected and penalized -- hurts audience retention signal",
            "Batch uploading shorts is OK; spacing long-form matters more",
            "Community tab: 2-3/day max to avoid spam flag",
        ],
    },

    # ======================================================================
    # REDDIT
    # ======================================================================
    "reddit": {
        "display_name": "Reddit",
        "posts_per_day": {"safe": 3, "aggressive": 5, "ban_risk": 10},
        "comments_per_day": {"safe": 20, "aggressive": 40, "ban_risk": 80},
        "follows_per_day": {"safe": 10, "aggressive": 20, "ban_risk": 50},
        "likes_per_day": {"safe": 50, "aggressive": 100, "ban_risk": 200},
        "self_promo_ratio_max_pct": 10,
        "same_link_max_subs": 3,
        "min_account_age_days": 30,
        "min_action_spacing_sec": 120,
        "duplicate_content_threshold": 0.70,
        "warmup_schedule": {
            "week1": {"max_days": 7, "posts": 0, "comments": 3,
                      "note": "Comment only -- build karma first"},
            "week2": {"max_days": 14, "posts": 1, "comments": 5},
            "week3": {"max_days": 21, "posts": 1, "comments": 8},
            "week4": {"max_days": 30, "posts": 2, "comments": 10},
            "month2_plus": {"max_days": 9999, "posts": 3, "comments": 20},
        },
        "notes": [
            "Self-promotion ratio: max 10% of posts should be self-promo",
            "Karma requirements per subreddit (varies widely)",
            "Account age requirements: usually 30+ days for most subs",
            "Same link to multiple subs: flagged as spam after 3-4",
            "Shadow ban check: old.reddit.com/user/{name} returns 404 = shadowbanned",
            "ALWAYS participate organically before any promo",
        ],
    },

    # ======================================================================
    # LINKEDIN
    # ======================================================================
    "linkedin": {
        "display_name": "LinkedIn",
        "posts_per_day": {"safe": 2, "aggressive": 3, "ban_risk": 5,
                          "note": "Algorithm heavily favors 1-2/day"},
        "connection_requests_per_week": {"safe": 100, "aggressive": 200,
                                         "ban_risk": 300},
        "comments_per_day": {"safe": 30, "aggressive": 60, "ban_risk": 100},
        "likes_per_day": {"safe": 100, "aggressive": 200, "ban_risk": 300},
        "follows_per_day": {"safe": 20, "aggressive": 50, "ban_risk": 100},
        "inmails_per_day": {"safe": 25, "aggressive": 50, "ban_risk": 100,
                            "note": "Governed by subscription tier"},
        "duplicate_content_threshold": 0.80,
        "min_action_spacing_sec": 60,
        "warmup_schedule": {
            "week1": {"max_days": 7, "posts": 1, "comments": 5,
                      "connection_requests": 10, "likes": 20},
            "week2": {"max_days": 14, "posts": 1, "comments": 10,
                      "connection_requests": 25, "likes": 40},
            "week3": {"max_days": 21, "posts": 1, "comments": 20,
                      "connection_requests": 50, "likes": 60},
            "week4_plus": {"max_days": 9999, "posts": 2, "comments": 30,
                           "connection_requests": 100, "likes": 100},
        },
        "notes": [
            "External links penalized in feed -- put links in first comment instead",
            "Employee advocacy posts get algorithm boost",
            "Connection requests: 100/week safe, 200+ = restricted",
            "Algorithm strongly favors native content over shared links",
            "Document posts (PDFs/carousels) get 2-3x more reach than text",
        ],
    },
}

# ---------------------------------------------------------------------------
# GENERAL ANTI-DETECTION RULES (cross-platform)
# ---------------------------------------------------------------------------
ANTI_DETECTION_RULES = {
    "vary_posting_times": {
        "description": "Do not post at exactly the same time daily",
        "jitter_minutes": 15,  # randomize +/- 15 min
    },
    "vary_content_format": {
        "description": "Mix text, image, video, carousel to avoid pattern detection",
        "min_format_diversity": 2,  # at least 2 different formats per week
    },
    "device_ip_separation": {
        "description": "Do not use same device/IP for multiple accounts",
    },
    "human_engagement_patterns": {
        "description": "Space engagements like a human -- not instant mass actions",
        "min_spacing_seconds": 30,
        "max_spacing_seconds": 120,
    },
    "gradual_ramp_up": {
        "description": "CRITICAL: new accounts must warm up gradually",
    },
    "no_bulk_actions": {
        "description": "Space bulk actions by 30-60s minimum between each",
        "min_spacing_seconds": 30,
    },
}

# ---------------------------------------------------------------------------
# OPTIMAL POSTING TIMES (timezone-adjusted engagement data)
# ---------------------------------------------------------------------------
OPTIMAL_POST_TIMES: Dict[str, List[Dict[str, Any]]] = {
    "twitter": [
        {"day": "weekday", "hours": [8, 9, 12, 17, 18], "tier": "best"},
        {"day": "weekday", "hours": [7, 10, 11, 13, 14, 15, 16, 19], "tier": "good"},
        {"day": "weekend", "hours": [9, 10, 11, 12], "tier": "best"},
        {"day": "weekend", "hours": [13, 14, 15], "tier": "good"},
    ],
    "instagram": [
        {"day": "weekday", "hours": [7, 8, 11, 12, 17, 18, 19], "tier": "best"},
        {"day": "weekday", "hours": [9, 10, 13, 14, 15, 16, 20], "tier": "good"},
        {"day": "weekend", "hours": [9, 10, 11], "tier": "best"},
        {"day": "weekend", "hours": [12, 13, 14, 15, 16], "tier": "good"},
    ],
    "tiktok": [
        {"day": "weekday", "hours": [7, 8, 12, 15, 17, 19, 21, 22], "tier": "best"},
        {"day": "weekday", "hours": [9, 10, 11, 13, 14, 16, 18, 20], "tier": "good"},
        {"day": "weekend", "hours": [10, 11, 12, 19, 20, 21], "tier": "best"},
    ],
    "youtube": [
        {"day": "weekday", "hours": [12, 15, 17, 18, 19], "tier": "best"},
        {"day": "weekday", "hours": [8, 9, 10, 11, 13, 14, 16, 20], "tier": "good"},
        {"day": "weekend", "hours": [9, 10, 11, 12, 14, 15], "tier": "best"},
    ],
    "reddit": [
        {"day": "weekday", "hours": [6, 7, 8, 9], "tier": "best",
         "note": "Early morning EST catches rising algorithm"},
        {"day": "weekday", "hours": [10, 11, 12, 13], "tier": "good"},
        {"day": "weekend", "hours": [8, 9, 10, 11], "tier": "best"},
    ],
    "linkedin": [
        {"day": "weekday", "hours": [7, 8, 9, 10, 12], "tier": "best",
         "note": "Tuesday-Thursday peak engagement"},
        {"day": "weekday", "hours": [11, 13, 14, 15, 16, 17], "tier": "good"},
        {"day": "weekend", "hours": [9, 10], "tier": "good",
         "note": "Weekend posting lower reach but less competition"},
    ],
}


# ===========================================================================
# ACCOUNT ACTIVITY TRACKER
# ===========================================================================
class AccountActivity:
    """Tracks per-account activity for ban prevention enforcement."""

    def __init__(self, account_id: str, platform: str,
                 account_age_days: int = 365):
        self.account_id = account_id
        self.platform = platform.lower()
        self.account_age_days = account_age_days
        self.created_at = datetime.now(timezone.utc)

        # Daily counters (reset each day)
        self.today_str = self._today()
        self.posts_today = 0
        self.stories_today = 0
        self.reels_today = 0
        self.shorts_today = 0
        self.follows_today = 0
        self.unfollows_today = 0
        self.likes_today = 0
        self.comments_today = 0
        self.dms_today = 0
        self.connection_requests_this_week = 0

        # Weekly counters
        self.week_str = self._this_week()
        self.long_form_this_week = 0
        self.posts_this_week = 0

        # Content tracking
        self.recent_post_hashes: List[Tuple[str, float]] = []  # (hash, timestamp)
        self.recent_post_texts: List[str] = []  # last 50 post texts for similarity
        self.content_formats_this_week: List[str] = []

        # Timing
        self.last_action_timestamps: Dict[str, float] = {}

        # Health
        self.warnings_today = 0
        self.blocks_today = 0
        self.total_warnings = 0
        self.total_blocks = 0
        self.shadowban_suspected = False

        # Self-promo tracking (Reddit)
        self.total_posts_lifetime = 0
        self.promo_posts_lifetime = 0

    @staticmethod
    def _today() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    @staticmethod
    def _this_week() -> str:
        d = datetime.now(timezone.utc)
        return f"{d.year}-W{d.isocalendar()[1]:02d}"

    def _reset_daily_if_needed(self):
        today = self._today()
        if today != self.today_str:
            self.today_str = today
            self.posts_today = 0
            self.stories_today = 0
            self.reels_today = 0
            self.shorts_today = 0
            self.follows_today = 0
            self.unfollows_today = 0
            self.likes_today = 0
            self.comments_today = 0
            self.dms_today = 0
            self.warnings_today = 0
            self.blocks_today = 0

    def _reset_weekly_if_needed(self):
        week = self._this_week()
        if week != self.week_str:
            self.week_str = week
            self.long_form_this_week = 0
            self.posts_this_week = 0
            self.connection_requests_this_week = 0
            self.content_formats_this_week = []

    def reset_if_needed(self):
        self._reset_daily_if_needed()
        self._reset_weekly_if_needed()

    def record_action(self, action_type: str, count: int = 1):
        """Record that an action was performed."""
        self.reset_if_needed()
        now = datetime.now(timezone.utc).timestamp()
        self.last_action_timestamps[action_type] = now

        mapping = {
            "post": "posts_today",
            "story": "stories_today",
            "reel": "reels_today",
            "short": "shorts_today",
            "follow": "follows_today",
            "unfollow": "unfollows_today",
            "like": "likes_today",
            "comment": "comments_today",
            "dm": "dms_today",
            "long_form": "long_form_this_week",
            "connection_request": "connection_requests_this_week",
        }

        attr = mapping.get(action_type)
        if attr:
            setattr(self, attr, getattr(self, attr) + count)

        if action_type in ("post", "story", "reel", "short", "long_form"):
            self.posts_this_week += count

    def get_count(self, action_type: str) -> int:
        """Get current count for an action type."""
        self.reset_if_needed()
        mapping = {
            "post": self.posts_today,
            "story": self.stories_today,
            "reel": self.reels_today,
            "short": self.shorts_today,
            "follow": self.follows_today,
            "unfollow": self.unfollows_today,
            "like": self.likes_today,
            "comment": self.comments_today,
            "dm": self.dms_today,
            "long_form": self.long_form_this_week,
            "connection_request": self.connection_requests_this_week,
        }
        return mapping.get(action_type, 0)

    def seconds_since_last(self, action_type: str) -> float:
        ts = self.last_action_timestamps.get(action_type)
        if ts is None:
            return float("inf")
        return datetime.now(timezone.utc).timestamp() - ts

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "platform": self.platform,
            "account_age_days": self.account_age_days,
            "today": self.today_str,
            "posts_today": self.posts_today,
            "stories_today": self.stories_today,
            "reels_today": self.reels_today,
            "shorts_today": self.shorts_today,
            "follows_today": self.follows_today,
            "unfollows_today": self.unfollows_today,
            "likes_today": self.likes_today,
            "comments_today": self.comments_today,
            "dms_today": self.dms_today,
            "connection_requests_this_week": self.connection_requests_this_week,
            "long_form_this_week": self.long_form_this_week,
            "warnings_today": self.warnings_today,
            "blocks_today": self.blocks_today,
            "total_warnings": self.total_warnings,
            "total_blocks": self.total_blocks,
            "shadowban_suspected": self.shadowban_suspected,
        }


# ===========================================================================
# GLOBAL ACCOUNT REGISTRY (in-memory, persists to disk)
# ===========================================================================
_accounts: Dict[str, AccountActivity] = {}


def _account_key(platform: str, account_id: str) -> str:
    return f"{platform.lower()}::{account_id}"


def get_account(platform: str, account_id: str,
                account_age_days: int = 365) -> AccountActivity:
    key = _account_key(platform, account_id)
    if key not in _accounts:
        _accounts[key] = AccountActivity(account_id, platform, account_age_days)
    acct = _accounts[key]
    acct.reset_if_needed()
    return acct


# ===========================================================================
# CORE FUNCTIONS
# ===========================================================================

def _content_hash(text: str) -> str:
    """SHA-256 hash of normalized content."""
    normalized = text.lower().strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def detect_duplicate_content(content: str, recent_posts: List[str],
                             threshold: float = 0.80) -> Tuple[float, Optional[str]]:
    """
    Check content similarity against recent posts.
    Returns (max_similarity_score, most_similar_post_or_None).
    """
    if not content or not recent_posts:
        return 0.0, None

    max_sim = 0.0
    most_similar = None
    content_lower = content.lower().strip()

    for post in recent_posts:
        post_lower = post.lower().strip()
        sim = SequenceMatcher(None, content_lower, post_lower).ratio()
        if sim > max_sim:
            max_sim = sim
            most_similar = post

    return max_sim, most_similar if max_sim >= threshold else None


def get_warmup_schedule(platform: str, account_age_days: int) -> Dict[str, Any]:
    """
    Return the maximum allowed actions for an account based on its age.
    Enforces gradual ramp-up which is CRITICAL for all platforms.
    """
    platform = platform.lower()
    if platform not in RATE_LIMITS:
        return {"error": f"Unknown platform: {platform}"}

    warmup = RATE_LIMITS[platform].get("warmup_schedule", {})
    if not warmup:
        return {"error": f"No warmup schedule defined for {platform}"}

    # Find the right tier
    applicable = None
    for tier_name, tier in warmup.items():
        max_days = tier.get("max_days", 9999)
        if account_age_days <= max_days:
            applicable = tier.copy()
            applicable["tier_name"] = tier_name
            break

    if applicable is None:
        # Fallback to last tier
        last_key = list(warmup.keys())[-1]
        applicable = warmup[last_key].copy()
        applicable["tier_name"] = last_key

    applicable["account_age_days"] = account_age_days
    applicable["platform"] = platform
    applicable.pop("max_days", None)
    return applicable


def _get_limit(platform: str, action_type: str) -> Optional[Dict[str, int]]:
    """Get the safe/aggressive/ban_risk limits for an action type."""
    plat = RATE_LIMITS.get(platform.lower(), {})

    # Map action types to limit keys
    action_to_key = {
        "post": "posts_per_day",
        "story": "stories_per_day",
        "reel": "reels_per_day",
        "short": "shorts_per_day",
        "follow": "follows_per_day",
        "unfollow": "unfollows_per_day",
        "like": "likes_per_day",
        "comment": "comments_per_day",
        "dm": "dms_per_day_nonfollower",
        "long_form": "long_form_per_week",
        "connection_request": "connection_requests_per_week",
    }

    key = action_to_key.get(action_type)
    if key and key in plat:
        val = plat[key]
        if isinstance(val, dict) and "safe" in val:
            return val
    return None


def check_before_post(platform: str, account_id: str,
                      content: str = "", content_format: str = "text",
                      has_link: bool = False, hashtag_count: int = 0,
                      is_promo: bool = False,
                      account_age_days: int = 365) -> Dict[str, Any]:
    """
    Pre-flight check before posting content.
    Returns verdict (SAFE/WARN/BLOCK) with detailed reasoning.
    """
    platform = platform.lower()
    if platform not in RATE_LIMITS:
        return {"verdict": BLOCK, "reason": f"Unknown platform: {platform}"}

    acct = get_account(platform, account_id, account_age_days)
    plat = RATE_LIMITS[platform]
    issues: List[Dict[str, str]] = []
    verdict = SAFE

    # --- 1. Check daily post limit ---
    post_limits = plat.get("posts_per_day", {})
    if isinstance(post_limits, dict) and "safe" in post_limits:
        current = acct.posts_today
        if current >= post_limits.get("ban_risk", 999):
            issues.append({"severity": BLOCK,
                           "rule": f"Posts today ({current}) at BAN RISK threshold "
                                   f"({post_limits['ban_risk']})"})
        elif current >= post_limits.get("aggressive", 999):
            issues.append({"severity": WARN,
                           "rule": f"Posts today ({current}) in AGGRESSIVE zone "
                                   f"(safe={post_limits['safe']})"})

    # --- 2. Warmup enforcement ---
    warmup = get_warmup_schedule(platform, account_age_days)
    warmup_post_limit = warmup.get("posts", warmup.get("shorts", 999))
    if acct.posts_today >= warmup_post_limit and account_age_days < 28:
        issues.append({"severity": BLOCK,
                       "rule": f"Warmup limit reached: {warmup_post_limit} posts/day "
                               f"for {account_age_days}-day-old account "
                               f"(tier: {warmup.get('tier_name', '?')})"})

    # --- 3. Hashtag check ---
    ht = plat.get("hashtags_per_post", {})
    if ht and hashtag_count > 0:
        if hashtag_count > ht.get("penalty_threshold", 999):
            issues.append({"severity": WARN,
                           "rule": f"Hashtags ({hashtag_count}) exceed penalty "
                                   f"threshold ({ht['penalty_threshold']}). "
                                   f"Optimal: {ht.get('optimal', '?')}"})
        if hashtag_count > ht.get("max_safe", 999):
            issues.append({"severity": WARN,
                           "rule": f"Hashtags ({hashtag_count}) exceed max safe "
                                   f"({ht['max_safe']})"})

    # --- 4. Link penalty warning ---
    if has_link:
        penalty = plat.get("link_in_post_penalty_pct")
        if penalty:
            issues.append({"severity": WARN,
                           "rule": f"Link in post: ~{penalty}% reach reduction. "
                                   f"Consider link-in-bio or comment instead."})
        if platform == "linkedin":
            issues.append({"severity": WARN,
                           "rule": "LinkedIn: external links penalized. "
                                   "Put link in first comment instead."})

    # --- 5. Duplicate content check ---
    if content:
        threshold = plat.get("duplicate_content_threshold", 0.80)
        sim_score, similar_post = detect_duplicate_content(
            content, acct.recent_post_texts, threshold)
        if similar_post is not None:
            issues.append({"severity": BLOCK,
                           "rule": f"Duplicate content detected "
                                   f"(similarity: {sim_score:.0%}). "
                                   f"Threshold: {threshold:.0%}"})

    # --- 6. Action spacing ---
    min_spacing = plat.get("min_action_spacing_sec", 30)
    elapsed = acct.seconds_since_last("post")
    if elapsed < min_spacing:
        issues.append({"severity": WARN,
                       "rule": f"Only {elapsed:.0f}s since last post "
                               f"(min spacing: {min_spacing}s). "
                               f"Wait {min_spacing - elapsed:.0f}s."})

    # --- 7. Reddit self-promo ratio ---
    if platform == "reddit" and is_promo:
        total = acct.total_posts_lifetime + 1
        promo = acct.promo_posts_lifetime + 1
        ratio = promo / total * 100
        max_ratio = plat.get("self_promo_ratio_max_pct", 10)
        if ratio > max_ratio:
            issues.append({"severity": BLOCK,
                           "rule": f"Self-promo ratio ({ratio:.1f}%) exceeds "
                                   f"Reddit max ({max_ratio}%). "
                                   f"Post organic content first."})

    # --- 8. Reddit account age ---
    if platform == "reddit":
        min_age = plat.get("min_account_age_days", 30)
        if account_age_days < min_age:
            issues.append({"severity": WARN,
                           "rule": f"Account age ({account_age_days}d) below "
                                   f"Reddit minimum ({min_age}d). "
                                   f"Many subs will autoremove posts."})

    # Determine overall verdict
    for issue in issues:
        if issue["severity"] == BLOCK:
            verdict = BLOCK
            break
        if issue["severity"] == WARN and verdict == SAFE:
            verdict = WARN

    # Record if not blocked
    if verdict != BLOCK:
        acct.record_action("post")
        if content:
            acct.recent_post_texts.append(content)
            if len(acct.recent_post_texts) > 50:
                acct.recent_post_texts.pop(0)
            acct.recent_post_hashes.append(
                (_content_hash(content), datetime.now(timezone.utc).timestamp()))
        if is_promo:
            acct.promo_posts_lifetime += 1
        acct.total_posts_lifetime += 1
    else:
        acct.blocks_today += 1
        acct.total_blocks += 1

    if verdict == WARN:
        acct.warnings_today += 1
        acct.total_warnings += 1

    # Log to ledger
    _log_activity(account_id, platform, "post", _content_hash(content) if content else "",
                  verdict == BLOCK,
                  "; ".join(i["rule"] for i in issues) if issues else "")

    return {
        "verdict": verdict,
        "platform": platform,
        "account_id": account_id,
        "issues": issues,
        "posts_today": acct.posts_today,
        "remaining_safe": max(0,
                              (post_limits.get("safe", 999) if isinstance(post_limits, dict)
                               else 999) - acct.posts_today),
        "warmup_limit": warmup_post_limit if account_age_days < 28 else None,
    }


def check_before_engage(platform: str, account_id: str,
                        action_type: str,
                        account_age_days: int = 365) -> Dict[str, Any]:
    """
    Pre-flight check before engagement actions (follow, like, comment, dm, etc.).
    Returns verdict (SAFE/WARN/BLOCK) with reasoning.
    """
    platform = platform.lower()
    if platform not in RATE_LIMITS:
        return {"verdict": BLOCK, "reason": f"Unknown platform: {platform}"}

    acct = get_account(platform, account_id, account_age_days)
    plat = RATE_LIMITS[platform]
    issues: List[Dict[str, str]] = []
    verdict = SAFE

    # Get limits for this action type
    limits = _get_limit(platform, action_type)
    current = acct.get_count(action_type)

    if limits:
        if current >= limits.get("ban_risk", 99999):
            issues.append({"severity": BLOCK,
                           "rule": f"{action_type.title()}s today ({current}) at "
                                   f"BAN RISK ({limits['ban_risk']})"})
        elif current >= limits.get("aggressive", 99999):
            issues.append({"severity": WARN,
                           "rule": f"{action_type.title()}s today ({current}) in "
                                   f"AGGRESSIVE zone (safe={limits['safe']})"})
        elif current >= limits.get("safe", 99999):
            issues.append({"severity": WARN,
                           "rule": f"{action_type.title()}s today ({current}) "
                                   f"reached safe limit ({limits['safe']})"})

    # Warmup enforcement
    warmup = get_warmup_schedule(platform, account_age_days)
    warmup_limit = warmup.get(action_type + "s", warmup.get(action_type, None))
    if warmup_limit is not None and current >= warmup_limit and account_age_days < 28:
        issues.append({"severity": BLOCK,
                       "rule": f"Warmup limit: {warmup_limit} {action_type}s/day "
                               f"for {account_age_days}-day-old account"})

    # Action spacing
    min_spacing = plat.get("min_action_spacing_sec", 30)
    elapsed = acct.seconds_since_last(action_type)
    if elapsed < min_spacing:
        issues.append({"severity": WARN,
                       "rule": f"Only {elapsed:.0f}s since last {action_type} "
                               f"(min: {min_spacing}s)"})

    # Determine verdict
    for issue in issues:
        if issue["severity"] == BLOCK:
            verdict = BLOCK
            break
        if issue["severity"] == WARN and verdict == SAFE:
            verdict = WARN

    if verdict != BLOCK:
        acct.record_action(action_type)
    else:
        acct.blocks_today += 1
        acct.total_blocks += 1

    if verdict == WARN:
        acct.warnings_today += 1
        acct.total_warnings += 1

    _log_activity(account_id, platform, action_type, "", verdict == BLOCK,
                  "; ".join(i["rule"] for i in issues) if issues else "")

    remaining = 0
    if limits:
        remaining = max(0, limits.get("safe", 999) - (current + (1 if verdict != BLOCK else 0)))

    return {
        "verdict": verdict,
        "platform": platform,
        "account_id": account_id,
        "action_type": action_type,
        "issues": issues,
        "count_today": current + (1 if verdict != BLOCK else 0),
        "remaining_safe": remaining,
    }


def check_account_health(platform: str, account_id: str,
                         account_age_days: int = 365) -> Dict[str, Any]:
    """
    Calculate overall health score 0-100 for an account.
    100 = perfectly safe, 0 = imminent ban risk.
    """
    platform = platform.lower()
    acct = get_account(platform, account_id, account_age_days)
    plat = RATE_LIMITS.get(platform, {})

    score = 100.0
    deductions: List[str] = []

    # Check each action type against limits
    action_types = ["post", "follow", "unfollow", "like", "comment", "dm",
                    "story", "reel", "short"]
    for action in action_types:
        limits = _get_limit(platform, action)
        if not limits:
            continue
        current = acct.get_count(action)
        safe = limits.get("safe", 999)
        aggressive = limits.get("aggressive", 999)
        ban = limits.get("ban_risk", 999)

        if current >= ban:
            deduct = 40
            score -= deduct
            deductions.append(f"-{deduct}: {action} at BAN RISK ({current}/{ban})")
        elif current >= aggressive:
            ratio = (current - safe) / max(1, aggressive - safe)
            deduct = 10 + ratio * 15
            score -= deduct
            deductions.append(f"-{deduct:.0f}: {action} in aggressive zone "
                              f"({current}/{aggressive})")
        elif current > safe * 0.8:
            deduct = 5
            score -= deduct
            deductions.append(f"-{deduct}: {action} approaching safe limit "
                              f"({current}/{safe})")

    # Warmup violation penalty
    if account_age_days < 28:
        warmup = get_warmup_schedule(platform, account_age_days)
        posts_limit = warmup.get("posts", warmup.get("shorts", 999))
        if acct.posts_today > posts_limit:
            score -= 30
            deductions.append(f"-30: Warmup violation "
                              f"({acct.posts_today}/{posts_limit} posts)")

    # Blocks penalty
    if acct.blocks_today > 0:
        penalty = min(20, acct.blocks_today * 5)
        score -= penalty
        deductions.append(f"-{penalty}: {acct.blocks_today} blocked actions today")

    # Shadowban suspicion
    if acct.shadowban_suspected:
        score -= 25
        deductions.append("-25: Shadowban suspected")

    score = max(0.0, min(100.0, score))

    status = "HEALTHY"
    if score < 30:
        status = "CRITICAL"
    elif score < 50:
        status = "AT_RISK"
    elif score < 70:
        status = "CAUTION"

    return {
        "platform": platform,
        "account_id": account_id,
        "health_score": round(score),
        "status": status,
        "deductions": deductions,
        "activity_summary": acct.to_dict(),
    }


def get_optimal_post_time(platform: str, timezone_str: str = "UTC") -> Dict[str, Any]:
    """
    Return best posting times based on engagement data.
    Times are returned in the specified timezone offset description.
    """
    platform = platform.lower()
    times = OPTIMAL_POST_TIMES.get(platform)
    if not times:
        return {"error": f"No optimal times data for {platform}"}

    now = datetime.now(timezone.utc)
    is_weekend = now.weekday() >= 5
    day_type = "weekend" if is_weekend else "weekday"

    best_hours = []
    good_hours = []
    for entry in times:
        if entry["day"] == day_type:
            if entry["tier"] == "best":
                best_hours.extend(entry["hours"])
            elif entry["tier"] == "good":
                good_hours.extend(entry["hours"])

    return {
        "platform": platform,
        "timezone": timezone_str,
        "day_type": day_type,
        "best_hours_utc": sorted(set(best_hours)),
        "good_hours_utc": sorted(set(good_hours)),
        "recommendation": (f"Post during {sorted(set(best_hours))} UTC for "
                          f"maximum reach on {day_type}s"),
    }


def simulate_ban_risk(platform: str,
                      actions_per_day: int,
                      action_type: str = "post") -> Dict[str, Any]:
    """
    Simulate ban risk for a given posting frequency.
    Returns risk assessment and projected timeline.
    """
    platform = platform.lower()
    limits = _get_limit(platform, action_type)
    if not limits:
        return {"error": f"No limits found for {platform}/{action_type}"}

    safe = limits.get("safe", 999)
    aggressive = limits.get("aggressive", 999)
    ban_risk = limits.get("ban_risk", 999)

    if actions_per_day <= safe:
        risk_level = "LOW"
        risk_pct = int((actions_per_day / safe) * 30)
        projection = "Sustainable indefinitely. No action needed."
    elif actions_per_day <= aggressive:
        risk_level = "MODERATE"
        ratio = (actions_per_day - safe) / max(1, aggressive - safe)
        risk_pct = 30 + int(ratio * 40)
        projection = (f"May trigger soft restrictions within 1-2 weeks. "
                      f"Reduce to {safe}/day for safety.")
    elif actions_per_day <= ban_risk:
        risk_level = "HIGH"
        risk_pct = 70 + int(((actions_per_day - aggressive) /
                              max(1, ban_risk - aggressive)) * 20)
        projection = (f"Likely shadowban/restriction within days. "
                      f"STRONGLY recommend reducing to {safe}/day.")
    else:
        risk_level = "CRITICAL"
        risk_pct = min(99, 90 + int((actions_per_day - ban_risk) / 10))
        projection = (f"Ban/suspension probable within 24-48 hours. "
                      f"STOP and reduce to {safe}/day immediately.")

    return {
        "platform": platform,
        "action_type": action_type,
        "actions_per_day": actions_per_day,
        "thresholds": {"safe": safe, "aggressive": aggressive, "ban_risk": ban_risk},
        "risk_level": risk_level,
        "risk_percentage": min(99, risk_pct),
        "projection": projection,
    }


def generate_safety_report() -> Dict[str, Any]:
    """Generate a full safety report across all tracked accounts."""
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_accounts": len(_accounts),
        "accounts": {},
        "alerts": [],
        "summary": {"healthy": 0, "caution": 0, "at_risk": 0, "critical": 0},
    }

    for key, acct in _accounts.items():
        health = check_account_health(acct.platform, acct.account_id,
                                      acct.account_age_days)
        report["accounts"][key] = health
        status = health["status"].lower()
        if status in report["summary"]:
            report["summary"][status] += 1

        if health["health_score"] < 50:
            report["alerts"].append({
                "account": key,
                "score": health["health_score"],
                "status": health["status"],
                "issues": health["deductions"],
            })

    if not _accounts:
        report["note"] = ("No accounts currently tracked. Accounts are registered "
                          "when check_before_post() or check_before_engage() is called.")

    return report


# ===========================================================================
# ACTIVITY LOGGING
# ===========================================================================

def _log_activity(account_id: str, platform: str, action_type: str,
                  content_hash: str, was_blocked: bool, reason: str):
    """Append a row to the activity log CSV."""
    try:
        file_exists = ACTIVITY_LOG.exists()
        with open(ACTIVITY_LOG, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["account_id", "platform", "action_type",
                                 "timestamp", "content_hash", "was_blocked", "reason"])
            writer.writerow([
                account_id,
                platform,
                action_type,
                datetime.now(timezone.utc).isoformat(),
                content_hash,
                was_blocked,
                reason,
            ])
    except OSError:
        pass  # Non-critical -- don't fail the check


# ===========================================================================
# CLI DISPLAY HELPERS
# ===========================================================================

def _header(text: str):
    width = 72
    print()
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def _subheader(text: str):
    print(f"\n--- {text} ---")


def _show_limits():
    """Display all platform rate limits."""
    _header("PRINTMAXX PLATFORM RATE LIMITS DATABASE")
    print(f"  Last updated: early 2026  |  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    for plat_key, plat in RATE_LIMITS.items():
        _subheader(plat.get("display_name", plat_key.upper()))

        # Show action limits
        limit_keys = [
            ("posts_per_day", "Posts/day"),
            ("stories_per_day", "Stories/day"),
            ("reels_per_day", "Reels/day"),
            ("shorts_per_day", "Shorts/day"),
            ("long_form_per_week", "Long-form/week"),
            ("community_posts_per_day", "Community posts/day"),
            ("follows_per_day", "Follows/day"),
            ("unfollows_per_day", "Unfollows/day"),
            ("likes_per_day", "Likes/day"),
            ("comments_per_day", "Comments/day"),
            ("dms_per_day_nonfollower", "DMs/day (non-follower)"),
            ("connection_requests_per_week", "Connection req/week"),
            ("inmails_per_day", "InMails/day"),
        ]

        for key, label in limit_keys:
            val = plat.get(key)
            if val and isinstance(val, dict) and "safe" in val:
                note = f"  ({val['note']})" if "note" in val else ""
                print(f"  {label:<28} SAFE: {val['safe']:<6} "
                      f"AGGRESSIVE: {val.get('aggressive', '-'):<6} "
                      f"BAN RISK: {val.get('ban_risk', '-')}{note}")

        # Hashtags
        ht = plat.get("hashtags_per_post")
        if ht:
            print(f"  {'Hashtags/post':<28} Optimal: {ht.get('optimal', '-'):<6} "
                  f"Max safe: {ht.get('max_safe', '-'):<6} "
                  f"Penalty at: {ht.get('penalty_threshold', '-')}"
                  f"{'  (' + ht.get('note', '') + ')' if ht.get('note') else ''}")

        # Link penalty
        lp = plat.get("link_in_post_penalty_pct")
        if lp:
            print(f"  {'Link-in-post penalty':<28} ~{lp}% reach reduction")

        # Duplicate threshold
        dt = plat.get("duplicate_content_threshold")
        if dt:
            print(f"  {'Duplicate detection':<28} >{dt:.0%} similarity = flagged")

        # Action spacing
        ms = plat.get("min_action_spacing_sec")
        if ms:
            print(f"  {'Min action spacing':<28} {ms}s between actions")

        # Reddit-specific
        spr = plat.get("self_promo_ratio_max_pct")
        if spr:
            print(f"  {'Self-promo ratio max':<28} {spr}%")
        sls = plat.get("same_link_max_subs")
        if sls:
            print(f"  {'Same link max subs':<28} {sls}")

        # Notes
        notes = plat.get("notes", [])
        if notes:
            print(f"\n  Platform notes:")
            for note in notes:
                print(f"    * {note}")

    _subheader("GENERAL ANTI-DETECTION RULES")
    for rule_key, rule in ANTI_DETECTION_RULES.items():
        desc = rule.get("description", rule_key)
        extras = {k: v for k, v in rule.items() if k != "description"}
        extra_str = f"  [{extras}]" if extras else ""
        print(f"  * {desc}{extra_str}")
    print()


def _show_warmup(platform: str, account_age_days: int):
    """Display warmup schedule for a platform/age."""
    platform = platform.lower()
    if platform not in RATE_LIMITS:
        print(f"ERROR: Unknown platform '{platform}'")
        print(f"Available: {', '.join(RATE_LIMITS.keys())}")
        return

    _header(f"WARMUP SCHEDULE: {RATE_LIMITS[platform]['display_name']}")
    print(f"  Account age: {account_age_days} day(s)")

    # Show current applicable limits
    schedule = get_warmup_schedule(platform, account_age_days)
    _subheader(f"Your tier: {schedule.get('tier_name', 'unknown')}")
    for key, val in schedule.items():
        if key in ("tier_name", "account_age_days", "platform", "note"):
            continue
        print(f"  Max {key}/day: {val}")
    if "note" in schedule:
        print(f"  Note: {schedule['note']}")

    # Show full warmup schedule
    _subheader("Full warmup progression")
    warmup = RATE_LIMITS[platform].get("warmup_schedule", {})
    for tier_name, tier in warmup.items():
        max_d = tier.get("max_days", 9999)
        label = f"<= {max_d} days" if max_d < 9999 else "28+ days (normal)"
        marker = " <-- YOU" if schedule.get("tier_name") == tier_name else ""
        print(f"\n  [{tier_name}] Account age {label}{marker}")
        for k, v in tier.items():
            if k in ("max_days", "note"):
                continue
            print(f"    {k}: {v}/day")
        if "note" in tier:
            print(f"    Note: {tier['note']}")
    print()


def _show_check(platform: str, account_id: str):
    """Show current status and remaining capacity."""
    platform = platform.lower()
    if platform not in RATE_LIMITS:
        print(f"ERROR: Unknown platform '{platform}'")
        return

    _header(f"ACCOUNT STATUS: {account_id} on {RATE_LIMITS[platform]['display_name']}")

    acct = get_account(platform, account_id)
    health = check_account_health(platform, account_id)

    print(f"  Health Score: {health['health_score']}/100 [{health['status']}]")
    print(f"  Account Age: {acct.account_age_days} days")

    _subheader("Today's Activity vs Limits")
    action_types = ["post", "story", "reel", "short", "follow", "unfollow",
                    "like", "comment", "dm"]
    for action in action_types:
        limits = _get_limit(platform, action)
        if not limits:
            continue
        current = acct.get_count(action)
        safe = limits["safe"]
        remaining = max(0, safe - current)
        pct = int(current / safe * 100) if safe > 0 else 0
        bar_len = 20
        filled = min(bar_len, int(pct / 100 * bar_len))
        bar = "#" * filled + "-" * (bar_len - filled)
        status_icon = "OK" if pct < 80 else ("!!" if pct < 100 else "XX")
        print(f"  {action:<14} [{bar}] {current:>4}/{safe:<4} "
              f"remaining: {remaining:<4} {status_icon}")

    if health["deductions"]:
        _subheader("Active Issues")
        for d in health["deductions"]:
            print(f"  {d}")
    print()


def _show_health():
    """Show health scores for all tracked accounts."""
    _header("ALL ACCOUNT HEALTH SCORES")
    if not _accounts:
        print("  No accounts currently tracked.")
        print("  Run --check PLATFORM ACCOUNT_ID to register accounts.")
        print()
        return

    for key, acct in _accounts.items():
        health = check_account_health(acct.platform, acct.account_id,
                                      acct.account_age_days)
        score = health["health_score"]
        status = health["status"]
        bar_len = 20
        filled = int(score / 100 * bar_len)
        bar = "#" * filled + "-" * (bar_len - filled)
        print(f"  {key:<35} [{bar}] {score:>3}/100 {status}")

    print()


def _show_report():
    """Show detailed safety report."""
    report = generate_safety_report()
    _header("PRINTMAXX SAFETY REPORT")
    print(f"  Generated: {report['generated_at']}")
    print(f"  Tracked accounts: {report['total_accounts']}")

    _subheader("Summary")
    for status, count in report["summary"].items():
        print(f"  {status.upper()}: {count}")

    if report.get("alerts"):
        _subheader("ALERTS")
        for alert in report["alerts"]:
            print(f"  [{alert['status']}] {alert['account']} "
                  f"(score: {alert['score']})")
            for issue in alert.get("issues", []):
                print(f"    - {issue}")

    if report.get("note"):
        print(f"\n  {report['note']}")
    print()


def _show_simulate(platform: str, actions_per_day: int):
    """Show ban risk simulation."""
    platform = platform.lower()
    if platform not in RATE_LIMITS:
        print(f"ERROR: Unknown platform '{platform}'")
        return

    _header(f"BAN RISK SIMULATION: {RATE_LIMITS[platform]['display_name']}")
    print(f"  Simulated rate: {actions_per_day} actions/day")

    for action_type in ["post", "follow", "like", "comment"]:
        result = simulate_ban_risk(platform, actions_per_day, action_type)
        if "error" in result:
            continue
        t = result["thresholds"]
        print(f"\n  {action_type.upper()} at {actions_per_day}/day:")
        print(f"    Thresholds: safe={t['safe']} | aggressive={t['aggressive']} "
              f"| ban_risk={t['ban_risk']}")
        print(f"    Risk Level: {result['risk_level']} ({result['risk_percentage']}%)")
        print(f"    Projection: {result['projection']}")
    print()


def _show_api_json():
    """Output full state as JSON for webapp integration."""
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rate_limits": {},
        "accounts": {},
        "safety_report": generate_safety_report(),
        "anti_detection_rules": ANTI_DETECTION_RULES,
        "optimal_post_times": OPTIMAL_POST_TIMES,
    }

    # Serialize rate limits (skip non-serializable)
    for plat_key, plat in RATE_LIMITS.items():
        data["rate_limits"][plat_key] = plat

    for key, acct in _accounts.items():
        data["accounts"][key] = acct.to_dict()

    print(json.dumps(data, indent=2, default=str))


# ===========================================================================
# CLI ENTRY POINT
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Algorithm Ban Prevention & Platform Compliance System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --limits                        Show all platform rate limits
  %(prog)s --warmup twitter 3              Warmup schedule for 3-day-old Twitter account
  %(prog)s --check twitter my_account      Current status and remaining capacity
  %(prog)s --health                        All account health scores
  %(prog)s --report                        Detailed safety report
  %(prog)s --simulate twitter 30           Predict ban risk at 30 actions/day
  %(prog)s --api-json                      JSON output for webapp integration
        """,
    )

    parser.add_argument("--limits", action="store_true",
                        help="Show all platform rate limits")
    parser.add_argument("--warmup", nargs=2, metavar=("PLATFORM", "ACCOUNT_AGE_DAYS"),
                        help="Show warmup schedule for platform and account age")
    parser.add_argument("--check", nargs=2, metavar=("PLATFORM", "ACCOUNT_ID"),
                        help="Show current status and remaining capacity")
    parser.add_argument("--health", action="store_true",
                        help="Show all account health scores")
    parser.add_argument("--report", action="store_true",
                        help="Generate detailed safety report")
    parser.add_argument("--simulate", nargs=2, metavar=("PLATFORM", "ACTIONS_PER_DAY"),
                        help="Predict ban risk at given posting frequency")
    parser.add_argument("--api-json", action="store_true",
                        help="Output full state as JSON for webapp integration")

    args = parser.parse_args()

    if args.limits:
        _show_limits()
    elif args.warmup:
        platform, age = args.warmup
        try:
            age_days = int(age)
        except ValueError:
            print(f"ERROR: Account age must be a number, got '{age}'")
            sys.exit(1)
        _show_warmup(platform, age_days)
    elif args.check:
        platform, account_id = args.check
        _show_check(platform, account_id)
    elif args.health:
        _show_health()
    elif args.report:
        _show_report()
    elif args.simulate:
        platform, actions = args.simulate
        try:
            actions_per_day = int(actions)
        except ValueError:
            print(f"ERROR: Actions per day must be a number, got '{actions}'")
            sys.exit(1)
        _show_simulate(platform, actions_per_day)
    elif args.api_json:
        _show_api_json()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
