#!/usr/bin/env python3
"""
RobloxMaxx content generator.

Generates social media content from templates and variables.
Outputs Buffer-ready CSVs for immediate scheduling.

Usage:
    python3 generate_content.py --type twitter --count 10
    python3 generate_content.py --type tiktok --count 5
    python3 generate_content.py --type all
    python3 generate_content.py --type twitter --template feature --variables '{"feature": "horror templates", "time": "65 seconds", "scripts": "16"}'
"""

import argparse
import csv
import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# Content templates with variable slots
TWITTER_TEMPLATES = {
    "feature": [
        "new in RobloxMaxx: {feature}. generates {scripts} scripts in {time}. {detail}. try it free.",
        "just shipped: {feature}. type what you want. get {scripts} production-ready Luau scripts in {time}. {detail}.",
        "{feature} is live. {scripts} scripts. {time}. modern Luau with type annotations. {detail}. link in bio.",
        "RobloxMaxx update: {feature}. one prompt. {scripts} scripts. {time}. DataStore, monetization, server-auth included. {detail}.",
    ],
    "dev_tip": [
        "Roblox tip: {tip}. {explanation}. RobloxMaxx handles this automatically.",
        "{tip}. most devs get this wrong. {explanation}. AI-generated code does it right by default.",
        "stop doing {bad_practice}. {tip}. {explanation}. or just generate it and skip the debugging.",
        "the difference between amateur and pro Roblox code: {tip}. {explanation}.",
    ],
    "engagement": [
        "roblox devs: {question}",
        "hot take: {opinion}. agree or disagree?",
        "name a {thing} and I'll {action}. most liked reply goes first.",
        "poll: {poll_question} A) {option_a} B) {option_b} C) {option_c} D) {option_d}",
    ],
    "meme": [
        "{setup} vs {punchline}. choose wisely.",
        "roblox devs when they {realization} [insert {meme_format}]",
        "me: {human_action}. AI: {ai_action}. me: [surprised pikachu]",
        "'{bad_take}' ok enjoy {consequence}. or {alternative}. your call.",
    ],
    "before_after": [
        "left: {hours} hours of manual scripting. right: {seconds} seconds with RobloxMaxx. same game. same features. different century.",
        "{hours} hours hand-coding a {genre}. or {seconds} seconds with AI. {scripts} scripts. {detail}. I know which one I'm picking.",
        "before RobloxMaxx: spend {hours} hours on {boring_task}. after: {seconds} seconds. the {hours} hours go to {fun_task} instead.",
    ],
}

TIKTOK_TEMPLATES = {
    "speedrun": [
        "watch me build a complete Roblox {genre} in {seconds} seconds with AI. I type one sentence. AI generates {scripts} scripts. paste into Studio. hit play. it works. {detail}.",
        "{seconds} seconds. that's how long it takes to build a Roblox {genre} with AI. [screen recording]. {scripts} scripts. all working. all monetized. link in bio.",
    ],
    "pov": [
        "POV: you described your dream Roblox {genre} and AI built the whole thing in {seconds} seconds. {scripts} scripts. {detail}. this is real.",
        "POV: you just typed '{prompt}' and got a complete playable game. {seconds} seconds. I can't go back to manual coding.",
    ],
    "before_after": [
        "what {hours} hours of Roblox scripting looks like vs {seconds} seconds with AI. same {genre}. same features. same monetization. I'm not even mad.",
        "me writing a Roblox {genre} by hand: 4 hours, 3 coffees, 47 bugs. me with AI: {seconds} seconds, 0 bugs, wondering why I ever did it manually.",
    ],
    "reaction": [
        "I showed a senior Roblox dev the code AI generated. he said it was cleaner than most human code he reviews. {detail}.",
        "my friend who's been coding Roblox for 5 years watched me generate a {genre} in {seconds} seconds. his face. priceless.",
    ],
}

# Default variable sets for each genre
GENRE_DEFAULTS = {
    "tycoon": {"genre": "tycoon", "seconds": "47", "scripts": "15", "hours": "3-4", "detail": "with gamepasses, upgrades, and DataStore persistence"},
    "obby": {"genre": "obby", "seconds": "52", "scripts": "11", "hours": "2-3", "detail": "20 stages with checkpoints and leaderboard"},
    "simulator": {"genre": "pet simulator", "seconds": "61", "scripts": "18", "hours": "5-6", "detail": "hatching, leveling, trading, and a shop"},
    "horror": {"genre": "horror game", "seconds": "65", "scripts": "16", "hours": "4-5", "detail": "flickering lights, chase AI, jumpscare system"},
    "rpg": {"genre": "RPG", "seconds": "82", "scripts": "24", "hours": "8-10", "detail": "combat, quests, inventory, NPC dialogue, skill tree"},
    "racing": {"genre": "racing game", "seconds": "73", "scripts": "22", "hours": "6-8", "detail": "5 tracks, garage, nitro boost, leaderboards"},
    "tower_defense": {"genre": "tower defense", "seconds": "70", "scripts": "21", "hours": "6-8", "detail": "10 waves, 5 tower types, upgrades, enemy pathfinding"},
    "fighting": {"genre": "fighting game", "seconds": "55", "scripts": "14", "hours": "4-5", "detail": "combo system, 4 character classes, ranked matchmaking"},
    "zombie": {"genre": "zombie survival", "seconds": "58", "scripts": "20", "hours": "5-6", "detail": "waves, 5 weapons, barricades, co-op for 4 players"},
}

TWITTER_HASHTAGS = {
    "primary": ["#RobloxDev", "#Roblox", "#GameDev", "#RobloxStudio"],
    "secondary": ["#AI", "#Luau", "#IndieDev", "#CodingWithAI", "#BuildInPublic"],
    "product": ["#RobloxMaxx"],
}

DEV_TIPS = [
    {"tip": "use UpdateAsync not SetAsync for player data", "explanation": "SetAsync overwrites without checking. UpdateAsync lets you merge. one lost save = one lost player", "bad_practice": "using SetAsync for player saves"},
    {"tip": "always disconnect RBXScriptConnections on player leave", "explanation": "Destroying a part doesn't auto-disconnect. connections leak memory. compounds over time", "bad_practice": "forgetting to clean up event connections"},
    {"tip": "never put game logic in LocalScripts", "explanation": "server authoritative or get exploited. RemoteEvents exist for a reason", "bad_practice": "trusting the client with game state"},
    {"tip": "use Scale not Offset for UI positioning", "explanation": "Offset breaks on different screen sizes. 60%+ of players are on mobile", "bad_practice": "using Offset for UI layout"},
    {"tip": "use task.spawn instead of deprecated spawn", "explanation": "spawn is deprecated. task.spawn is the modern replacement with better error handling", "bad_practice": "using spawn() and wait()"},
    {"tip": "validate all RemoteEvent arguments on the server", "explanation": "exploiters send whatever they want through RemoteEvents. type check everything", "bad_practice": "trusting RemoteEvent arguments from clients"},
    {"tip": "use OrderedDataStore for leaderboards", "explanation": "GetSortedAsync handles sorting for you. stop writing custom sort functions for 8 lines of code", "bad_practice": "writing custom leaderboard sorting code"},
    {"tip": "batch your DataStore calls", "explanation": "Roblox rate limits DataStore. 60 + 10*players requests per minute. batch saves or you'll hit throttling", "bad_practice": "saving to DataStore on every currency change"},
    {"tip": "use CollectionService for tagging", "explanation": "stop putting BoolValues inside parts to mark them. CollectionService:GetTagged() is faster and cleaner", "bad_practice": "using BoolValues as tags inside parts"},
    {"tip": "profile your game with MicroProfiler", "explanation": "Ctrl+F6 in Studio. shows exactly what's slow. stop guessing. measure.", "bad_practice": "guessing at performance bottlenecks"},
]

ENGAGEMENT_QUESTIONS = [
    {"question": "what takes you the longest when building a new game? (wrong answers only)"},
    {"question": "what's the first thing you build when starting a new Roblox game?"},
    {"question": "how many hours do you spend in Roblox Studio per week?"},
    {"poll_question": "hardest part of Roblox development?", "option_a": "DataStore", "option_b": "UI/UX", "option_c": "monetization", "option_d": "getting players"},
    {"poll_question": "what's your go-to Roblox game genre to build?", "option_a": "tycoon", "option_b": "obby", "option_c": "simulator", "option_d": "RPG"},
    {"opinion": "in 2 years no serious Roblox dev will hand-write boilerplate code. AI generates it better and faster"},
    {"opinion": "free models are the worst thing that happened to Roblox code quality"},
    {"thing": "Roblox game genre", "action": "generate the full code live on stream"},
    {"thing": "game feature", "action": "show how AI implements it in under 60 seconds"},
]


def pick_hashtags(count=4):
    """Select a mix of primary and secondary hashtags."""
    primary = random.sample(TWITTER_HASHTAGS["primary"], min(2, len(TWITTER_HASHTAGS["primary"])))
    secondary = random.sample(TWITTER_HASHTAGS["secondary"], min(count - 2, len(TWITTER_HASHTAGS["secondary"])))
    return " ".join(primary + secondary)


def fill_template(template, variables):
    """Fill template placeholders with variables. Skip missing vars."""
    result = template
    for key, value in variables.items():
        result = result.replace("{" + key + "}", str(value))
    return result


def generate_twitter_posts(count=10, template_type=None, custom_vars=None):
    """Generate Twitter posts from templates."""
    posts = []
    genres = list(GENRE_DEFAULTS.keys())

    for i in range(count):
        if template_type and template_type in TWITTER_TEMPLATES:
            category = template_type
        else:
            category = random.choice(list(TWITTER_TEMPLATES.keys()))

        templates = TWITTER_TEMPLATES[category]
        template = random.choice(templates)

        if custom_vars:
            variables = custom_vars
        elif category == "dev_tip":
            variables = random.choice(DEV_TIPS)
        elif category == "engagement":
            variables = random.choice(ENGAGEMENT_QUESTIONS)
        elif category == "meme":
            genre = random.choice(genres)
            g = GENRE_DEFAULTS[genre]
            variables = {
                "setup": f"{g['hours']} hours hand-coding a {g['genre']}",
                "punchline": f"{g['seconds']} seconds with AI. {g['scripts']} scripts. works first try",
                "realization": "AI can write their boilerplate faster and cleaner",
                "meme_format": "drake/surprised pikachu",
                "human_action": f"writes {int(g['scripts']) * 80} lines in {g['hours']} hours",
                "ai_action": f"generates {int(g['scripts']) * 100} lines of better code in {g['seconds']} seconds",
                "bad_take": "just use free models",
                "consequence": "the backdoor scripts and deprecated API",
                "alternative": f"generate clean code in {g['seconds']} seconds",
            }
        else:
            genre = genres[i % len(genres)]
            variables = GENRE_DEFAULTS[genre].copy()
            if category == "feature":
                variables["feature"] = f"{variables['genre']} template"

        try:
            text = fill_template(template, variables)
        except (KeyError, IndexError):
            text = fill_template(template, variables)

        posts.append({
            "id": f"GEN_T{i+1:03d}",
            "category": category,
            "post_text": text,
            "hashtags": pick_hashtags(),
            "media_type": "text" if category in ["dev_tip", "engagement"] else "image",
            "status": "DRAFT",
        })

    return posts


def generate_tiktok_scripts(count=5, custom_vars=None):
    """Generate TikTok video scripts from templates."""
    scripts = []
    genres = list(GENRE_DEFAULTS.keys())

    for i in range(count):
        category = random.choice(list(TIKTOK_TEMPLATES.keys()))
        templates = TIKTOK_TEMPLATES[category]
        template = random.choice(templates)

        if custom_vars:
            variables = custom_vars
        else:
            genre = genres[i % len(genres)]
            variables = GENRE_DEFAULTS[genre].copy()
            variables["prompt"] = f"build a {variables['genre']} with {variables['detail']}"

        text = fill_template(template, variables)

        scripts.append({
            "id": f"GEN_TK{i+1:03d}",
            "title": f"AI builds Roblox {variables.get('genre', 'game')} in {variables.get('seconds', '60')} seconds",
            "category": category,
            "script_body": text,
            "duration_seconds": random.choice([30, 45, 60]),
            "hashtags": "#roblox #robloxdev #ai #gamedev #coding",
            "status": "DRAFT",
        })

    return scripts


def write_twitter_csv(posts, output_path):
    """Write Twitter posts to Buffer-ready CSV."""
    fieldnames = ["id", "category", "post_text", "hashtags", "media_type", "status"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)
    print(f"wrote {len(posts)} twitter posts to {output_path}")


def write_tiktok_csv(scripts, output_path):
    """Write TikTok scripts to CSV."""
    fieldnames = ["id", "title", "category", "script_body", "duration_seconds", "hashtags", "status"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scripts)
    print(f"wrote {len(scripts)} tiktok scripts to {output_path}")


def generate_calendar(days=30):
    """Generate a content calendar starting from today."""
    calendar = []
    start_date = datetime.now()

    # Platform schedule: what posts on which days
    daily_schedule = {
        0: [("twitter", "dev_tip"), ("twitter", "feature")],           # Monday
        1: [("twitter", "feature"), ("tiktok", "speedrun"), ("reddit", "showcase")],  # Tuesday
        2: [("twitter", "dev_tip"), ("devforum", "tutorial")],         # Wednesday
        3: [("twitter", "feature"), ("tiktok", "before_after"), ("reddit", "discussion")],  # Thursday
        4: [("twitter", "engagement"), ("devforum", "update")],        # Friday
        5: [("twitter", "meme"), ("tiktok", "pov"), ("reddit", "value")],  # Saturday
        6: [("twitter", "before_after"), ("tiktok", "reaction")],      # Sunday
    }

    for day in range(days):
        current_date = start_date + timedelta(days=day)
        weekday = current_date.weekday()
        schedule = daily_schedule.get(weekday, [])

        for platform, content_type in schedule:
            calendar.append({
                "day": day + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "weekday": current_date.strftime("%A"),
                "platform": platform,
                "content_type": content_type,
                "status": "SCHEDULED",
            })

    return calendar


def write_calendar_csv(calendar, output_path):
    """Write content calendar to CSV."""
    fieldnames = ["day", "date", "weekday", "platform", "content_type", "status"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calendar)
    print(f"wrote {len(calendar)} calendar entries to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="RobloxMaxx content generator")
    parser.add_argument("--type", choices=["twitter", "tiktok", "calendar", "all"], default="all",
                        help="Type of content to generate")
    parser.add_argument("--count", type=int, default=10,
                        help="Number of posts to generate")
    parser.add_argument("--template", type=str, default=None,
                        help="Specific template type (feature, dev_tip, engagement, meme, before_after)")
    parser.add_argument("--variables", type=str, default=None,
                        help="JSON string of custom variables")
    parser.add_argument("--output-dir", type=str, default=str(SCRIPT_DIR / "generated"),
                        help="Output directory for generated files")

    args = parser.parse_args()

    # Parse custom variables if provided
    custom_vars = None
    if args.variables:
        custom_vars = json.loads(args.variables)

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.type in ("twitter", "all"):
        posts = generate_twitter_posts(args.count, args.template, custom_vars)
        output_path = output_dir / f"twitter_generated_{timestamp}.csv"
        write_twitter_csv(posts, output_path)

    if args.type in ("tiktok", "all"):
        scripts = generate_tiktok_scripts(args.count, custom_vars)
        output_path = output_dir / f"tiktok_generated_{timestamp}.csv"
        write_tiktok_csv(scripts, output_path)

    if args.type in ("calendar", "all"):
        calendar = generate_calendar(30)
        output_path = output_dir / f"calendar_generated_{timestamp}.csv"
        write_calendar_csv(calendar, output_path)

    print(f"\ndone. all files in {output_dir}/")


if __name__ == "__main__":
    main()
