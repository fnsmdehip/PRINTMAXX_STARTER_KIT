#!/usr/bin/env python3
"""
Meta Detection System - Historical Pattern Matching
Tracks trends across ALL niches with Ghibli/Saratoga/Morning Routine pattern detection
"""

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Historical patterns to match
HISTORICAL_PATTERNS = {
    "GHIBLI_PATTERN": {
        "description": "Character/aesthetic virality → meme coin",
        "signals": ["character", "anime", "aesthetic", "nostalgic", "wholesome", "cozy"],
        "coin_potential": 9,
        "product_potential": 6,
        "content_potential": 10,
        "velocity_threshold": 5,  # mentions needed in 24h
    },
    "SARATOGA_PATTERN": {
        "description": "Quick pump meme coin",
        "signals": ["pump", "moon", "early", "presale", "gem", "100x"],
        "coin_potential": 10,
        "product_potential": 2,
        "content_potential": 7,
        "velocity_threshold": 8,
    },
    "ROUTINE_PATTERN": {
        "description": "Lifestyle trend → app/product",
        "signals": ["morning routine", "productivity", "optimization", "hack", "system"],
        "coin_potential": 3,
        "product_potential": 10,
        "content_potential": 9,
        "velocity_threshold": 4,
    },
    "MOLT_PATTERN": {
        "description": "AI agent → community coin",
        "signals": ["ai agent", "bot", "autonomous", "terminal", "dao"],
        "coin_potential": 8,
        "product_potential": 7,
        "content_potential": 8,
        "velocity_threshold": 6,
    },
    "FITNESS_TRANSFORMATION": {
        "description": "Before/after fitness → app/supplement",
        "signals": ["transformation", "weight loss", "muscle gain", "body recomp"],
        "coin_potential": 2,
        "product_potential": 10,
        "content_potential": 10,
        "velocity_threshold": 5,
    },
    "SPIRITUAL_WELLNESS": {
        "description": "Spiritual/wellness trend → app/course",
        "signals": ["manifestation", "meditation", "mindfulness", "healing"],
        "coin_potential": 3,
        "product_potential": 9,
        "content_potential": 9,
        "velocity_threshold": 4,
    },
}

# Niche definitions (from existing tracker)
NICHES = {
    "N001": {"name": "Faith", "keywords": ["prayer", "christian", "bible", "devotional", "worship"]},
    "N002": {"name": "Fitness", "keywords": ["workout", "gym", "fitness", "exercise", "muscle"]},
    "N003": {"name": "Tech", "keywords": ["coding", "developer", "ai", "tech", "programming"]},
    "N004": {"name": "Pet", "keywords": ["dog", "cat", "pet", "animal"]},
    "N005": {"name": "Senior", "keywords": ["senior", "elderly", "retirement", "boomer"]},
    "N006": {"name": "ADHD", "keywords": ["adhd", "focus", "attention", "neurodivergent"]},
    "N007": {"name": "GenZ Finance", "keywords": ["investing", "stocks", "crypto", "genz"]},
    "N008": {"name": "Couples", "keywords": ["relationship", "couples", "dating", "romance"]},
    "N009": {"name": "Women Wellness", "keywords": ["women", "wellness", "selfcare", "feminine"]},
    "N010": {"name": "Students", "keywords": ["student", "study", "college", "exam"]},
    "N011": {"name": "Sleep", "keywords": ["sleep", "insomnia", "rest", "bedtime"]},
    "N012": {"name": "Gaming", "keywords": ["gaming", "esports", "streamer", "twitch"]},
    "N013": {"name": "Crypto", "keywords": ["crypto", "bitcoin", "ethereum", "defi"]},
    "N014": {"name": "Stocks", "keywords": ["stocks", "trading", "investing", "market"]},
    "N015": {"name": "Motivation", "keywords": ["motivation", "mindset", "success", "goals"]},
    "N016": {"name": "Music", "keywords": ["music", "artist", "producer", "beats"]},
    "N017": {"name": "Fashion", "keywords": ["fashion", "style", "outfit", "clothing"]},
    "N018": {"name": "Food", "keywords": ["food", "cooking", "recipe", "nutrition"]},
    "N019": {"name": "Travel", "keywords": ["travel", "vacation", "adventure", "explore"]},
    "N020": {"name": "Parenting", "keywords": ["parenting", "kids", "children", "family"]},
    "N021": {"name": "Mental Health", "keywords": ["mental health", "therapy", "anxiety", "depression"]},
    "N022": {"name": "Career", "keywords": ["career", "job", "professional", "linkedin"]},
    "N023": {"name": "Investing", "keywords": ["investing", "portfolio", "wealth", "financial"]},
    "N024": {"name": "Productivity", "keywords": ["productivity", "time management", "efficiency"]},
    "N025": {"name": "Meditation", "keywords": ["meditation", "mindfulness", "zen", "calm"]},
    "N026": {"name": "Language Learning", "keywords": ["language", "duolingo", "learning", "bilingual"]},
    "N027": {"name": "Art", "keywords": ["art", "drawing", "painting", "creative"]},
    "N028": {"name": "Photography", "keywords": ["photography", "photo", "camera", "instagram"]},
    "N029": {"name": "Anime", "keywords": ["anime", "manga", "weeb", "otaku"]},
    "N030": {"name": "Sports", "keywords": ["sports", "athlete", "training", "competition"]},
    "N031": {"name": "Environment", "keywords": ["environment", "climate", "sustainable", "eco"]},
    "N032": {"name": "DIY", "keywords": ["diy", "handmade", "craft", "maker"]},
    "N033": {"name": "Memes", "keywords": ["meme", "funny", "humor", "viral"]},
}


class MetaDetector:
    def __init__(self):
        self.meta_data = []
        self.niche_opportunities = []
        self.new_niches = []

    def calculate_velocity_score(self, mentions: int, timeframe_hours: int = 24) -> int:
        """Calculate velocity score (0-10) based on mention frequency"""
        mentions_per_hour = mentions / timeframe_hours

        if mentions_per_hour >= 10:
            return 10
        elif mentions_per_hour >= 5:
            return 9
        elif mentions_per_hour >= 3:
            return 8
        elif mentions_per_hour >= 2:
            return 7
        elif mentions_per_hour >= 1:
            return 6
        elif mentions_per_hour >= 0.5:
            return 5
        elif mentions_per_hour >= 0.25:
            return 4
        else:
            return 3

    def match_historical_pattern(self, meta_keywords: List[str], meta_context: str) -> Tuple[str, int]:
        """Match meta against historical patterns, return (pattern_name, confidence_score)"""
        best_match = None
        best_score = 0

        meta_text = f"{' '.join(meta_keywords)} {meta_context}".lower()

        for pattern_name, pattern_data in HISTORICAL_PATTERNS.items():
            matches = sum(1 for signal in pattern_data["signals"] if signal in meta_text)
            confidence = min(100, int((matches / len(pattern_data["signals"])) * 100))

            if confidence > best_score:
                best_score = confidence
                best_match = pattern_name

        return best_match or "NOVEL_PATTERN", best_score

    def calculate_potentials(self, pattern: str, meta_type: str) -> Dict[str, int]:
        """Calculate coin/product/content potential based on pattern and type"""
        if pattern in HISTORICAL_PATTERNS:
            base = HISTORICAL_PATTERNS[pattern]
            return {
                "coin_potential": base["coin_potential"],
                "product_potential": base["product_potential"],
                "content_potential": base["content_potential"],
            }

        # Novel pattern - estimate based on meta type
        if "crypto" in meta_type.lower() or "coin" in meta_type.lower():
            return {"coin_potential": 9, "product_potential": 4, "content_potential": 7}
        elif "app" in meta_type.lower() or "tool" in meta_type.lower():
            return {"coin_potential": 3, "product_potential": 10, "content_potential": 8}
        elif "lifestyle" in meta_type.lower() or "trend" in meta_type.lower():
            return {"coin_potential": 4, "product_potential": 9, "content_potential": 10}
        else:
            return {"coin_potential": 5, "product_potential": 7, "content_potential": 8}

    def match_applicable_niches(self, meta_keywords: List[str]) -> List[str]:
        """Match meta to applicable niches"""
        applicable = []
        meta_text = " ".join(meta_keywords).lower()

        for niche_id, niche_data in NICHES.items():
            # Check if any niche keywords match meta keywords
            if any(keyword in meta_text for keyword in niche_data["keywords"]):
                applicable.append(niche_id)

        return applicable or ["N033"]  # Default to Memes if no match

    def detect_meta_from_sources(self):
        """
        Main detection logic - would scrape actual sources in production
        For now, creates sample data showing the pattern
        """

        # Example meta trends (in production, this would scrape Twitter, Reddit, TikTok, etc.)
        sample_metas = [
            {
                "name": "Cozy AI Companions",
                "keywords": ["ai", "companion", "cozy", "aesthetic", "wholesome"],
                "context": "AI companion apps with cozy aesthetic branding going viral on TikTok",
                "mentions_24h": 47,
                "category": "AI_LIFESTYLE",
            },
            {
                "name": "Morning Mobility Stack",
                "keywords": ["morning", "mobility", "routine", "optimization"],
                "context": "Morning mobility routine trend on fitness TikTok - people showing their stretch sequences",
                "mentions_24h": 12,
                "category": "LIFESTYLE_FITNESS",
            },
            {
                "name": "Prayer Streak Apps",
                "keywords": ["prayer", "streak", "gamification", "faith"],
                "context": "Christian prayer tracking apps gaining traction, gamification of devotional practice",
                "mentions_24h": 8,
                "category": "FAITH_TECH",
            },
            {
                "name": "AI Study Agents",
                "keywords": ["ai", "study", "agent", "academic", "automation"],
                "context": "AI agents that manage study schedules and generate practice tests",
                "mentions_24h": 23,
                "category": "AI_EDUCATION",
            },
            {
                "name": "Sleep Soundscape Coins",
                "keywords": ["sleep", "soundscape", "coin", "meme", "wholesome"],
                "context": "Meme coin around sleep/relaxation aesthetic - cozy vibes",
                "mentions_24h": 31,
                "category": "MEMECOIN_WELLNESS",
            },
            {
                "name": "Micro-Fasting Timers",
                "keywords": ["fasting", "timer", "health", "optimization"],
                "context": "Intermittent fasting timer apps with social features trending",
                "mentions_24h": 15,
                "category": "HEALTH_TECH",
            },
            {
                "name": "Couple's Finance Dashboard",
                "keywords": ["couples", "finance", "dashboard", "budgeting"],
                "context": "Apps for couples to manage shared finances, transparent budgeting",
                "mentions_24h": 9,
                "category": "FINTECH_RELATIONSHIP",
            },
            {
                "name": "GenZ Stock Memes",
                "keywords": ["genz", "stocks", "meme", "investing", "yolo"],
                "context": "GenZ creating meme accounts around stock market moves",
                "mentions_24h": 28,
                "category": "FINANCE_CONTENT",
            },
        ]

        meta_id = 1
        for meta in sample_metas:
            # Calculate velocity
            velocity = self.calculate_velocity_score(meta["mentions_24h"])

            # Match pattern
            pattern, confidence = self.match_historical_pattern(meta["keywords"], meta["context"])

            # Calculate potentials
            potentials = self.calculate_potentials(pattern, meta["category"])

            # Match niches
            applicable_niches = self.match_applicable_niches(meta["keywords"])

            # Add to meta tracker
            self.meta_data.append({
                "meta_id": f"META{meta_id:03d}",
                "meta_name": meta["name"],
                "category": meta["category"],
                "velocity_score": velocity,
                "coin_potential": potentials["coin_potential"],
                "product_potential": potentials["product_potential"],
                "content_potential": potentials["content_potential"],
                "applicable_niches": ",".join(applicable_niches),
                "historical_pattern_match": pattern,
                "pattern_confidence": confidence,
                "mentions_24h": meta["mentions_24h"],
                "detected_at": datetime.now().isoformat(),
                "keywords": ",".join(meta["keywords"]),
                "context": meta["context"],
            })

            # Generate niche opportunities
            for niche_id in applicable_niches:
                self._generate_niche_opportunities(meta, niche_id, pattern, potentials)

            meta_id += 1

    def _generate_niche_opportunities(self, meta: Dict, niche_id: str, pattern: str, potentials: Dict):
        """Generate specific opportunities for niche"""
        niche_name = NICHES[niche_id]["name"]

        # Determine opportunity type based on potentials
        opportunities = []

        if potentials["product_potential"] >= 8:
            opportunities.append({
                "type": "APP",
                "description": f"{meta['name']} app for {niche_name} niche",
                "methods": "MM001,MM019",
                "revenue_model": "IAP + Subs",
            })

        if potentials["content_potential"] >= 8:
            opportunities.append({
                "type": "CONTENT",
                "description": f"{meta['name']} content series for {niche_name}",
                "methods": "MM006,CF013",
                "revenue_model": "Ads + Creator Fund",
            })

        if potentials["coin_potential"] >= 7:
            opportunities.append({
                "type": "MEMECOIN",
                "description": f"{meta['name']} community coin for {niche_name}",
                "methods": "MM034",
                "revenue_model": "Trading",
            })

        # Add course/info product if routine/lifestyle pattern
        if "ROUTINE" in pattern or potentials["product_potential"] >= 7:
            opportunities.append({
                "type": "INFO_PRODUCT",
                "description": f"{meta['name']} guide/template for {niche_name}",
                "methods": "MM002,MM025,MM046",
                "revenue_model": "One-time sale",
            })

        for opp in opportunities:
            self.niche_opportunities.append({
                "meta_id": f"META{len(self.meta_data):03d}",
                "meta_name": meta["name"],
                "niche_id": niche_id,
                "niche_name": niche_name,
                "opportunity_type": opp["type"],
                "opportunity_description": opp["description"],
                "applicable_methods": opp["methods"],
                "revenue_model": opp["revenue_model"],
                "priority_score": (potentials.get(f"{opp['type'].lower()}_potential", 7) * 10
                                   + meta["mentions_24h"]),
                "detected_at": datetime.now().isoformat(),
            })

    def save_results(self):
        """Save all results to CSV files"""

        # Save META_TRACKER.csv
        meta_tracker_path = BASE_DIR / "LEDGER" / "META_TRACKER.csv"
        with open(meta_tracker_path, "w", newline="") as f:
            if self.meta_data:
                writer = csv.DictWriter(f, fieldnames=self.meta_data[0].keys())
                writer.writeheader()
                writer.writerows(self.meta_data)

        print(f"✅ Created {meta_tracker_path}")
        print(f"   {len(self.meta_data)} meta trends tracked")

        # Save NICHE_META_OPPORTUNITIES.csv
        niche_opp_path = BASE_DIR / "LEDGER" / "NICHE_META_OPPORTUNITIES.csv"
        with open(niche_opp_path, "w", newline="") as f:
            if self.niche_opportunities:
                writer = csv.DictWriter(f, fieldnames=self.niche_opportunities[0].keys())
                writer.writeheader()
                # Sort by priority score
                sorted_opps = sorted(self.niche_opportunities,
                                     key=lambda x: x["priority_score"],
                                     reverse=True)
                writer.writerows(sorted_opps)

        print(f"✅ Created {niche_opp_path}")
        print(f"   {len(self.niche_opportunities)} opportunities identified")

        # Save NEW_NICHES_DISCOVERED.csv (placeholder for future scraping)
        new_niches_path = BASE_DIR / "LEDGER" / "NEW_NICHES_DISCOVERED.csv"
        with open(new_niches_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "niche_id", "niche_name", "platform", "members",
                "growth_rate", "monetization_potential", "discovered_at"
            ])
            writer.writeheader()
            # Placeholder entries showing structure
            writer.writerow({
                "niche_id": "N034",
                "niche_name": "Looksmaxxing",
                "platform": "Reddit + TikTok",
                "members": "1.2M",
                "growth_rate": "340%",
                "monetization_potential": "HIGH",
                "discovered_at": datetime.now().isoformat(),
            })
            writer.writerow({
                "niche_id": "N035",
                "niche_name": "AI Companions",
                "platform": "Twitter + Discord",
                "members": "650K",
                "growth_rate": "520%",
                "monetization_potential": "HIGHEST",
                "discovered_at": datetime.now().isoformat(),
            })

        print(f"✅ Created {new_niches_path}")
        print(f"   Structure ready for niche discovery")

    def print_summary(self):
        """Print analysis summary"""
        print("\n" + "="*80)
        print("META DETECTION SUMMARY")
        print("="*80)

        # Pattern distribution
        pattern_counts = defaultdict(int)
        for meta in self.meta_data:
            pattern_counts[meta["historical_pattern_match"]] += 1

        print("\n📊 PATTERN DISTRIBUTION:")
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {pattern}: {count} trends")

        # Top opportunities by priority
        print("\n🎯 TOP 10 OPPORTUNITIES (by priority):")
        top_opps = sorted(self.niche_opportunities,
                         key=lambda x: x["priority_score"],
                         reverse=True)[:10]

        for i, opp in enumerate(top_opps, 1):
            print(f"\n   {i}. {opp['meta_name']} ({opp['niche_name']})")
            print(f"      Type: {opp['opportunity_type']}")
            print(f"      Methods: {opp['applicable_methods']}")
            print(f"      Priority: {opp['priority_score']}")

        # Velocity alerts
        high_velocity = [m for m in self.meta_data if m["velocity_score"] >= 8]
        if high_velocity:
            print(f"\n⚡ HIGH VELOCITY ALERTS ({len(high_velocity)} trends):")
            for meta in high_velocity:
                print(f"   {meta['meta_name']}: {meta['mentions_24h']} mentions/24h")

        print("\n" + "="*80)


def main():
    print("🔍 Meta Detection System - Historical Pattern Matching")
    print("="*80)

    detector = MetaDetector()

    print("\n1. Detecting meta trends...")
    detector.detect_meta_from_sources()

    print("\n2. Saving results...")
    detector.save_results()

    print("\n3. Analysis complete:")
    detector.print_summary()

    print("\n✅ All files created successfully!")
    print("\nNext steps:")
    print("1. Review LEDGER/META_TRACKER.csv for detected trends")
    print("2. Check LEDGER/NICHE_META_OPPORTUNITIES.csv for highest priority opportunities")
    print("3. Implement top opportunities using applicable_methods")
    print("4. Monitor velocity_score for emerging trends")


if __name__ == "__main__":
    main()
