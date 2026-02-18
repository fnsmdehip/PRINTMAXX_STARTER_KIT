#!/usr/bin/env python3
"""
Design Aggregator - Competitor-based icon/asset generation system

Aggregates design patterns from top competitors, then generates
ChatGPT-optimized prompts for icon creation.

Usage:
    python design_aggregator.py --app biomaxx
    python design_aggregator.py --app biomaxx --type icon
    python design_aggregator.py --app biomaxx --type screenshot
    python design_aggregator.py --all
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

# Competitor design research database
# Aggregated from App Store analysis + competitor teardowns
COMPETITOR_DESIGN_DB = {
    # Health/Longevity Category Leaders
    "health_longevity": {
        "icons": {
            "zero_fasting": {
                "style": "minimal circle timer",
                "colors": ["purple gradient", "clean white"],
                "symbol": "timer ring with gap",
                "feel": "calm, premium, trustworthy",
                "success": "200k/mo revenue"
            },
            "noom": {
                "style": "bold wordmark",
                "colors": ["vibrant orange-coral"],
                "symbol": "N letterform in rounded square",
                "feel": "friendly, approachable, modern",
                "success": "$1B ARR"
            },
            "oura": {
                "style": "metallic ring 3D",
                "colors": ["silver/chrome gradient", "dark background"],
                "symbol": "ring product shot",
                "feel": "premium tech, sleek",
                "success": "unicorn status"
            },
            "eight_sleep": {
                "style": "abstract sleep symbol",
                "colors": ["deep blue to purple gradient"],
                "symbol": "infinity/8 sleep wave",
                "feel": "premium, scientific, calming",
                "success": "100M+ funding"
            },
            "whoop": {
                "style": "bold wordmark",
                "colors": ["green on black"],
                "symbol": "W mark or strap",
                "feel": "athletic, premium, elite",
                "success": "400k+ members"
            }
        },
        "patterns": {
            "dominant_style": "dark backgrounds with accent colors",
            "icon_shape": "rounded square (iOS standard)",
            "gradients": "subtle, premium (not garish)",
            "3d_elements": "light shadows, depth without kitsch",
            "typography": "clean sans-serif, premium weight"
        }
    },

    # Screen Time/Blocker Category
    "screen_blockers": {
        "icons": {
            "opal": {
                "style": "gemstone 3D",
                "colors": ["opal iridescent gradient"],
                "symbol": "faceted gem/crystal",
                "feel": "premium, protective, valuable",
                "success": "600k/mo"
            },
            "one_sec": {
                "style": "timer minimal",
                "colors": ["red/coral on white"],
                "symbol": "1 second timer concept",
                "feel": "urgent, simple, effective",
                "success": "top productivity app"
            },
            "screenzen": {
                "style": "zen garden minimal",
                "colors": ["sage green, cream"],
                "symbol": "plant/zen stone",
                "feel": "calm, natural, mindful",
                "success": "rising star"
            },
            "forest": {
                "style": "nature illustration",
                "colors": ["green gradient, brown"],
                "symbol": "tree growing",
                "feel": "gamified, friendly, growth",
                "success": "15M+ downloads"
            }
        },
        "patterns": {
            "dominant_style": "nature or precious materials metaphor",
            "icon_shape": "filled rounded square",
            "gradients": "organic, natural progressions",
            "3d_elements": "subtle depth, no harsh shadows",
            "mascots": "work well (Forest tree, etc)"
        }
    },

    # Faith/Spiritual Category
    "faith_spiritual": {
        "icons": {
            "hallow": {
                "style": "glowing H letterform",
                "colors": ["warm amber/gold on dark"],
                "symbol": "H with halo glow",
                "feel": "sacred, warm, inviting",
                "success": "$100M+ funding"
            },
            "pray": {
                "style": "praying hands simple",
                "colors": ["blue gradient"],
                "symbol": "hands or flame",
                "feel": "reverent, accessible",
                "success": "top faith app"
            },
            "glorify": {
                "style": "wordmark modern",
                "colors": ["purple/violet"],
                "symbol": "G with rays",
                "feel": "contemporary, uplifting",
                "success": "millions of users"
            },
            "abide": {
                "style": "nature leaf",
                "colors": ["green, earthy"],
                "symbol": "leaf/vine",
                "feel": "peaceful, growth",
                "success": "strong retention"
            }
        },
        "patterns": {
            "dominant_style": "warm glows, sacred geometry hints",
            "icon_shape": "filled square with soft corners",
            "colors": "warm (amber, gold) or purple (royalty)",
            "avoid": "overly religious symbols (cross alone)",
            "feel": "welcoming to all, not preachy"
        }
    },

    # Fitness Category
    "fitness": {
        "icons": {
            "strong": {
                "style": "bold S letterform",
                "colors": ["red on black"],
                "symbol": "S with strength implication",
                "feel": "powerful, serious, gym-focused",
                "success": "top lifting tracker"
            },
            "strava": {
                "style": "arrow/ribbon 3D",
                "colors": ["orange gradient"],
                "symbol": "forward arrow ribbon",
                "feel": "movement, energy, community",
                "success": "100M+ athletes"
            },
            "nike_run": {
                "style": "swoosh variation",
                "colors": ["neon on black"],
                "symbol": "running figure in swoosh",
                "feel": "athletic, premium, iconic",
                "success": "brand power"
            },
            "sweat": {
                "style": "script S",
                "colors": ["coral pink on white"],
                "symbol": "S script with energy",
                "feel": "feminine, energetic, motivating",
                "success": "women's fitness leader"
            }
        },
        "patterns": {
            "dominant_style": "bold, energetic, movement-implied",
            "icon_shape": "filled square",
            "colors": "high energy (orange, red, coral)",
            "3d_elements": "dynamic angles, implied motion",
            "gender": "consider target (coral for women, dark for men)"
        }
    }
}

# App configurations with design direction
APP_CONFIGS = {
    "biomaxx": {
        "name": "BioMaxx",
        "category": "health_longevity",
        "concept": "longevity protocol tracker",
        "primary_competitors": ["zero_fasting", "oura", "whoop"],
        "design_direction": {
            "symbol": "DNA helix merged with infinity/longevity symbol",
            "primary_gradient": "emerald green (#10B981) to teal (#14B8A6)",
            "background": "dark slate (#0F172A)",
            "accent": "warm amber glow (#F59E0B)",
            "style": "premium biohacker aesthetic",
            "feel": "scientific yet warm, not cold/clinical",
            "differentiator": "organic green vs clinical blue (like competitors)"
        }
    },
    "glowmaxx": {
        "name": "GlowMaxx",
        "category": "health_longevity",
        "concept": "habit tracker for appearance/confidence",
        "primary_competitors": ["noom", "oura"],
        "design_direction": {
            "symbol": "radiant face silhouette or glow burst",
            "primary_gradient": "rose gold (#F59E0B) to warm pink (#EC4899)",
            "background": "soft cream (#FDF4E3) or dark mode option",
            "accent": "gold sparkle",
            "style": "aspirational beauty meets health",
            "feel": "confident, radiant, premium",
            "differentiator": "glow/radiance vs clinical tracking"
        }
    },
    "prayerlock": {
        "name": "PrayerLock",
        "category": "faith_spiritual",
        "concept": "phone blocker that requires prayer",
        "primary_competitors": ["hallow", "opal"],
        "design_direction": {
            "symbol": "lock with divine light rays or praying hands on lock",
            "primary_gradient": "warm gold (#FFD93D) to amber (#F59E0B)",
            "background": "deep navy (#1E3A5F) or warm dark (#2D1F3D)",
            "accent": "soft white glow",
            "style": "sacred meets tech protection",
            "feel": "protective, peaceful, purposeful",
            "differentiator": "warmth of faith + security of lock"
        }
    },
    "walktounlock": {
        "name": "WalkToUnlock",
        "category": "fitness",
        "concept": "phone blocker requiring steps",
        "primary_competitors": ["opal", "strava"],
        "design_direction": {
            "symbol": "footsteps leading to unlock/freedom or running shoe with lock",
            "primary_gradient": "energetic orange (#F97316) to yellow (#FBBF24)",
            "background": "fresh white or dark charcoal",
            "accent": "green for progress",
            "style": "energetic, movement-focused",
            "feel": "motivating, fresh, rewarding",
            "differentiator": "unlock = reward for movement"
        }
    },
    "studylock": {
        "name": "StudyLock",
        "category": "screen_blockers",
        "concept": "focus blocker for students",
        "primary_competitors": ["forest", "opal"],
        "design_direction": {
            "symbol": "book with lock or owl with graduation cap",
            "primary_gradient": "deep blue (#3B82F6) to purple (#8B5CF6)",
            "background": "dark navy for focus",
            "accent": "gold for achievement",
            "style": "academic meets gamification",
            "feel": "focused, rewarding, studious",
            "differentiator": "study-specific, student identity"
        }
    },
    "devotionflow": {
        "name": "DevotionFlow",
        "category": "faith_spiritual",
        "concept": "daily devotional habit tracker",
        "primary_competitors": ["hallow", "glorify", "abide"],
        "design_direction": {
            "symbol": "flowing water or dove with gentle rays",
            "primary_gradient": "soft blue (#60A5FA) to peaceful teal (#5EEAD4)",
            "background": "warm cream or soft dark",
            "accent": "gold morning light",
            "style": "peaceful, consistent, flowing",
            "feel": "daily rhythm, gentle commitment",
            "differentiator": "flow state for faith vs meditation apps"
        }
    },
    "pelvicpro": {
        "name": "PelvicPro",
        "category": "health_longevity",
        "concept": "pelvic floor training app",
        "primary_competitors": ["sweat", "noom"],
        "design_direction": {
            "symbol": "abstract core/flower bloom or strength rings",
            "primary_gradient": "dusty rose (#FDA4AF) to mauve (#C084FC)",
            "background": "soft blush or clean white",
            "accent": "gold for achievement",
            "style": "feminine strength, medical credibility",
            "feel": "empowering, discreet, professional",
            "differentiator": "strength-focused not embarrassment"
        }
    },
    "focusprayer": {
        "name": "FocusPrayer",
        "category": "faith_spiritual",
        "concept": "guided prayer with focus timer",
        "primary_competitors": ["hallow", "one_sec"],
        "design_direction": {
            "symbol": "candle flame or focused light beam",
            "primary_gradient": "warm amber (#FCD34D) to deep orange (#EA580C)",
            "background": "contemplative dark (#1F1B24)",
            "accent": "soft white glow",
            "style": "candlelit focus",
            "feel": "intimate, focused, warm",
            "differentiator": "focus mechanics + prayer (unique combo)"
        }
    },
    "dailyanchor": {
        "name": "DailyAnchor",
        "category": "faith_spiritual",
        "concept": "morning routine with faith foundation",
        "primary_competitors": ["hallow", "abide"],
        "design_direction": {
            "symbol": "anchor with sunrise or compass with cross",
            "primary_gradient": "sunrise orange (#FB923C) to golden yellow (#FBBF24)",
            "background": "dawn sky gradient or clean white",
            "accent": "navy anchor color",
            "style": "morning hope, grounded start",
            "feel": "hopeful, grounded, consistent",
            "differentiator": "anchor = stability + morning routine"
        }
    },
    "learnlock": {
        "name": "LearnLock",
        "category": "screen_blockers",
        "concept": "educational blocker - learn to unlock",
        "primary_competitors": ["forest", "opal"],
        "design_direction": {
            "symbol": "brain with lock or lightbulb unlocking",
            "primary_gradient": "smart blue (#0EA5E9) to electric cyan (#22D3EE)",
            "background": "dark slate or white",
            "accent": "yellow for lightbulb moments",
            "style": "smart, progressive, rewarding",
            "feel": "clever, educational, motivating",
            "differentiator": "learn something to unlock (unique mechanic)"
        }
    }
}


def get_category_insights(category: str) -> dict:
    """Get aggregated design insights for a category."""
    return COMPETITOR_DESIGN_DB.get(category, {})


def generate_chatgpt_icon_prompt(app_key: str) -> str:
    """
    Generate a ChatGPT-optimized prompt that incorporates:
    1. Competitor design patterns (what works in category)
    2. App-specific differentiation
    3. Technical requirements for App Store
    """
    config = APP_CONFIGS.get(app_key)
    if not config:
        return f"Unknown app: {app_key}"

    category_data = get_category_insights(config["category"])
    competitors = config["primary_competitors"]
    direction = config["design_direction"]

    # Build competitor reference section
    comp_insights = []
    for comp in competitors:
        for cat_key, cat_data in COMPETITOR_DESIGN_DB.items():
            if "icons" in cat_data and comp in cat_data["icons"]:
                icon_data = cat_data["icons"][comp]
                comp_insights.append(f"- {comp.replace('_', ' ').title()}: {icon_data['style']}, {icon_data['colors'][0]}, feels {icon_data['feel']}")

    # Get category patterns
    patterns = category_data.get("patterns", {})

    prompt = f"""Create a professional mobile app icon for "{config['name']}" - a {config['concept']}.

COMPETITOR ANALYSIS (what works in this category):
{chr(10).join(comp_insights)}

CATEGORY WINNING PATTERNS:
- Dominant style: {patterns.get('dominant_style', 'premium, modern')}
- Common approach: {patterns.get('icon_shape', 'rounded square')}
- Gradient style: {patterns.get('gradients', 'subtle premium gradients')}

DESIGN DIRECTION FOR {config['name'].upper()}:
- Core symbol: {direction['symbol']}
- Primary gradient: {direction['primary_gradient']}
- Background: {direction['background']}
- Accent: {direction.get('accent', 'subtle glow')}
- Target feel: {direction['feel']}
- Key differentiator: {direction['differentiator']}

TECHNICAL REQUIREMENTS:
- Size: 1024x1024 pixels
- Shape: iOS rounded square (will be masked by system)
- NO text or letters - pure iconography only
- Must be instantly recognizable at 60x60 pixels
- Professional gradient execution with depth
- Subtle shadow and glow for dimension
- NOT flat - must have 3D depth/premium feel

QUALITY STANDARDS:
- Should look like a top 10 App Store app
- Premium enough to justify $9.99/mo subscription
- Distinctive from competitors while fitting category expectations
- Would make users want to download immediately

Generate ONE beautiful, polished app icon."""

    return prompt


def generate_chatgpt_screenshot_prompt(app_key: str, screen_type: str = "hero") -> str:
    """Generate prompt for app store screenshots."""
    config = APP_CONFIGS.get(app_key)
    if not config:
        return f"Unknown app: {app_key}"

    direction = config["design_direction"]

    screen_prompts = {
        "hero": f"""Create an App Store hero screenshot for "{config['name']}" - {config['concept']}.

DEVICE: iPhone 15 Pro frame (realistic device mockup)
SCREEN CONTENT: Show the main dashboard/home screen
COLOR SCHEME: {direction['primary_gradient']} gradient background behind phone
HEADLINE: Large text above phone: "{config['name']}"
SUBHEAD: Below: "Your daily {config['concept'].split()[0].lower()} companion"

STYLE:
- Premium, minimal, high contrast
- Phone slightly angled (5-10 degrees) for depth
- Soft shadow under device
- Background gradient with subtle texture
- iOS-style interface visible on screen

SIZE: 1290x2796 pixels (iPhone 6.7" required)""",

        "features": f"""Create an App Store feature showcase screenshot for "{config['name']}".

Show 3 key features with icons and short descriptions:
1. Track [main action] easily
2. Build consistent habits
3. See your progress

STYLE:
- Split into 3 horizontal sections
- Each with icon + 3-4 word label
- Use {direction['primary_gradient']} accent colors
- Clean white or dark background
- Premium iconography

SIZE: 1290x2796 pixels"""
    }

    return screen_prompts.get(screen_type, screen_prompts["hero"])


def save_all_prompts(output_dir: Path):
    """Save all prompts to files for easy copy/paste."""
    output_dir.mkdir(parents=True, exist_ok=True)

    all_prompts = []

    for app_key in APP_CONFIGS:
        icon_prompt = generate_chatgpt_icon_prompt(app_key)
        all_prompts.append(f"{'='*60}\n{app_key.upper()} - ICON PROMPT\n{'='*60}\n\n{icon_prompt}\n\n")

    # Save combined file
    combined_path = output_dir / "ALL_ICON_PROMPTS_CHATGPT.txt"
    with open(combined_path, "w") as f:
        f.write(f"# ChatGPT Icon Prompts - Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("# Competitor-aggregated design prompts for app icons\n")
        f.write("# Copy each prompt into ChatGPT with DALL-E for best results\n\n")
        f.write("\n".join(all_prompts))

    print(f"Saved all prompts to: {combined_path}")
    return combined_path


def main():
    parser = argparse.ArgumentParser(description="Generate competitor-aggregated design prompts")
    parser.add_argument("--app", type=str, help="App key (biomaxx, prayerlock, etc)")
    parser.add_argument("--type", type=str, default="icon", choices=["icon", "screenshot"], help="Asset type")
    parser.add_argument("--all", action="store_true", help="Generate all prompts")
    parser.add_argument("--list", action="store_true", help="List available apps")
    parser.add_argument("--save", action="store_true", help="Save prompts to file")

    args = parser.parse_args()

    if args.list:
        print("Available apps:")
        for key, config in APP_CONFIGS.items():
            print(f"  {key}: {config['name']} - {config['concept']}")
        return

    if args.save or args.all:
        script_dir = Path(__file__).parent
        output_dir = script_dir.parent / "assets" / "prompts"
        save_all_prompts(output_dir)
        return

    if args.app:
        if args.type == "icon":
            print(generate_chatgpt_icon_prompt(args.app))
        else:
            print(generate_chatgpt_screenshot_prompt(args.app))
    else:
        print("Usage: python design_aggregator.py --app biomaxx")
        print("       python design_aggregator.py --all --save")
        print("       python design_aggregator.py --list")


if __name__ == "__main__":
    main()
