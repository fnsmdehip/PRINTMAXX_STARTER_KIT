#!/usr/bin/env python3

from __future__ import annotations
"""
YouTube Content Factory Pipeline for PRINTMAXX

Orchestrates: Script → TTS → B-Roll → Assembly → Clip → Upload → Cross-Post

Usage:
    python3 AUTOMATIONS/youtube_factory.py --generate-script --niche tech --topic "5 AI tools"
    python3 AUTOMATIONS/youtube_factory.py --narrate --niche tech
    python3 AUTOMATIONS/youtube_factory.py --assemble --niche tech
    python3 AUTOMATIONS/youtube_factory.py --clip --niche tech
    python3 AUTOMATIONS/youtube_factory.py --upload --niche tech
    python3 AUTOMATIONS/youtube_factory.py --full-pipeline --niche tech --topic "topic here"
    python3 AUTOMATIONS/youtube_factory.py --full-pipeline --niche tech --topic "topic" --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# --- Project path validation ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
OUTPUT_BASE = PROJECT_ROOT / "output" / "youtube"


def safe_path(target: Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# ============================================================================
# CONFIGURATION
# ============================================================================

# API Keys (from environment)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
YOUTUBE_CLIENT_SECRETS = os.environ.get("YOUTUBE_CLIENT_SECRETS", "")

# Claude model for script generation
CLAUDE_MODEL = "claude-sonnet-4-6-20250514"

# TTS configuration
TTS_ENGINE = os.environ.get("TTS_ENGINE", "qwen3-tts")  # Options: qwen3-tts, bark, coqui
TTS_SCRIPT_PATH = PROJECT_ROOT / "TOOLS" / "qwen3-tts" / "tts.py"

# Video settings
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30
SHORTS_WIDTH = 1080
SHORTS_HEIGHT = 1920

# Niche configurations
NICHE_CONFIG = {
    "tech": {
        "channel_name": "AI Breakdown",
        "description": "Daily AI and tech breakdowns",
        "tags": ["AI", "technology", "automation", "artificial intelligence", "tech news"],
        "target_length_minutes": 10,
        "cpm_estimate": "$6-12",
        "voice_style": "professional, confident, slightly casual",
        "script_prompt_extra": "Focus on practical impact. Use specific numbers and examples. "
                               "Start with a compelling hook about what changed or what's new.",
    },
    "horror": {
        "channel_name": "Dark Archives",
        "description": "True crime, mysteries, and unsolved cases",
        "tags": ["horror", "mystery", "true crime", "unsolved", "creepy"],
        "target_length_minutes": 15,
        "cpm_estimate": "$8-15",
        "voice_style": "dramatic, suspenseful, measured pace",
        "script_prompt_extra": "Build tension gradually. Use atmospheric descriptions. "
                               "Include historical details and witness accounts.",
    },
    "finance": {
        "channel_name": "Money Mechanics",
        "description": "Investing, wealth building, and financial strategy",
        "tags": ["investing", "finance", "money", "stocks", "wealth"],
        "target_length_minutes": 12,
        "cpm_estimate": "$12-25",
        "voice_style": "authoritative, data-driven, accessible",
        "script_prompt_extra": "Use specific numbers, percentages, and historical data. "
                               "Avoid financial advice disclaimers in the script body (add in description).",
    },
    "comparison": {
        "channel_name": "Versus Lab",
        "description": "Head-to-head comparisons and tier lists",
        "tags": ["comparison", "versus", "tier list", "ranking", "review"],
        "target_length_minutes": 8,
        "cpm_estimate": "$5-10",
        "voice_style": "energetic, opinionated, entertaining",
        "script_prompt_extra": "Structure as clear categories with a winner for each. "
                               "Include surprising picks. End with overall recommendation.",
    },
    "reddit": {
        "channel_name": "Reddit Reads",
        "description": "Best stories from Reddit",
        "tags": ["reddit", "stories", "AITA", "askreddit", "tifu"],
        "target_length_minutes": 12,
        "cpm_estimate": "$4-8",
        "voice_style": "conversational, reactive, empathetic",
        "script_prompt_extra": "Read the story naturally with commentary. React to key moments. "
                               "Ask the audience what they think.",
    },
}


def get_output_dir(niche: str, topic: str = "") -> Path:
    """Get output directory for current video."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    topic_slug = topic.lower().replace(" ", "_")[:40] if topic else "untitled"
    output_dir = OUTPUT_BASE / niche / f"{date_str}_{topic_slug}"
    safe_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


# ============================================================================
# SCRIPT GENERATION
# ============================================================================

def generate_script(niche: str, topic: str, dry_run: bool = False) -> str:
    """Generate video script using Claude API."""
    config = NICHE_CONFIG.get(niche)
    if not config:
        print(f"[ERROR] Unknown niche: {niche}. Available: {list(NICHE_CONFIG.keys())}")
        return ""

    target_words = config["target_length_minutes"] * 150  # ~150 words per minute

    prompt = f"""Write a YouTube video script about: {topic}

Channel: {config['channel_name']} ({config['description']})
Target length: {target_words} words ({config['target_length_minutes']} minutes)
Voice style: {config['voice_style']}

{config['script_prompt_extra']}

Format the script as:

[HOOK - first 15 seconds, must grab attention immediately]
...

[INTRO - 30 seconds, what they'll learn]
...

[SECTION 1: Title]
...

[SECTION 2: Title]
...

[SECTION 3: Title]
...

[CTA - subscribe, like, comment prompt]
...

Rules:
- Write exactly what the narrator says, not stage directions
- Use conversational language, not academic
- Include specific numbers, names, and examples
- No filler phrases ("in this video we'll explore...")
- Hook must deliver value or shock in first sentence
- Every section should have a mini-hook that keeps viewers watching
- End with a question to drive comments"""

    output_dir = get_output_dir(niche, topic)
    script_file = output_dir / "script.md"

    if dry_run:
        print(f"\n[DRY RUN] Would generate {target_words}-word script about: {topic}")
        print(f"  Output: {script_file}")
        return ""

    if not ANTHROPIC_API_KEY:
        print("[ERROR] ANTHROPIC_API_KEY not set. Cannot generate script.")
        return ""

    print(f"\nGenerating script for: {topic}")
    print(f"  Niche: {niche} | Target: {target_words} words | Style: {config['voice_style']}")

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        script = response.content[0].text

        safe_path(script_file)
        with open(script_file, "w") as f:
            f.write(f"# {topic}\n")
            f.write(f"# Niche: {niche} | Generated: {datetime.now().isoformat()}\n\n")
            f.write(script)

        word_count = len(script.split())
        print(f"  Script generated: {word_count} words")
        print(f"  Saved to: {script_file}")
        return str(script_file)

    except Exception as e:
        print(f"[ERROR] Script generation failed: {e}")
        return ""


# ============================================================================
# TTS NARRATION
# ============================================================================

def generate_narration(niche: str, topic: str, dry_run: bool = False) -> str:
    """Generate TTS narration from script."""
    output_dir = get_output_dir(niche, topic)
    script_file = output_dir / "script.md"
    narration_file = output_dir / "narration.wav"

    if not script_file.exists():
        print(f"[ERROR] No script found at {script_file}. Run --generate-script first.")
        return ""

    if dry_run:
        print(f"\n[DRY RUN] Would generate narration from: {script_file}")
        print(f"  Output: {narration_file}")
        print(f"  TTS engine: {TTS_ENGINE}")
        return ""

    print(f"\nGenerating narration...")
    print(f"  Script: {script_file}")
    print(f"  TTS engine: {TTS_ENGINE}")

    # Read script and clean for TTS
    with open(script_file) as f:
        script_text = f.read()

    # Remove markdown headers and section markers
    clean_lines = []
    for line in script_text.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            continue  # Skip section markers
        if line:
            clean_lines.append(line)
    clean_text = " ".join(clean_lines)

    # Save clean text for TTS input
    tts_input = output_dir / "tts_input.txt"
    safe_path(tts_input)
    with open(tts_input, "w") as f:
        f.write(clean_text)

    # Run TTS based on engine
    if TTS_ENGINE == "qwen3-tts" and TTS_SCRIPT_PATH.exists():
        cmd = [
            sys.executable, str(TTS_SCRIPT_PATH),
            "--input", str(tts_input),
            "--output", str(narration_file),
        ]
    elif TTS_ENGINE == "bark":
        cmd = [
            sys.executable, "-m", "bark",
            "--text_file", str(tts_input),
            "--output", str(narration_file),
        ]
    else:
        # Fallback: use macOS say command (basic but always available)
        cmd = ["say", "-o", str(narration_file), "--data-format=LEI16@22050", "-f", str(tts_input)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print(f"  Narration saved to: {narration_file}")
            return str(narration_file)
        else:
            print(f"  [ERROR] TTS failed: {result.stderr[:200]}")
            # Fallback to macOS say
            print("  Falling back to macOS 'say' command...")
            fallback_cmd = ["say", "-o", str(narration_file), "--data-format=LEI16@22050",
                           "-f", str(tts_input)]
            subprocess.run(fallback_cmd, timeout=300)
            if narration_file.exists():
                print(f"  Narration saved (via macOS say): {narration_file}")
                return str(narration_file)
            return ""
    except subprocess.TimeoutExpired:
        print("  [ERROR] TTS timed out after 10 minutes.")
        return ""
    except Exception as e:
        print(f"  [ERROR] TTS failed: {e}")
        return ""


# ============================================================================
# VIDEO ASSEMBLY
# ============================================================================

def assemble_video(niche: str, topic: str, dry_run: bool = False) -> str:
    """Assemble final video from narration + visuals using ffmpeg."""
    output_dir = get_output_dir(niche, topic)
    narration_file = output_dir / "narration.wav"
    final_video = output_dir / "final.mp4"
    broll_dir = output_dir / "broll"

    if not narration_file.exists():
        print(f"[ERROR] No narration at {narration_file}. Run --narrate first.")
        return ""

    if dry_run:
        print(f"\n[DRY RUN] Would assemble video:")
        print(f"  Narration: {narration_file}")
        print(f"  B-roll dir: {broll_dir}")
        print(f"  Output: {final_video}")
        return ""

    print(f"\nAssembling video...")

    # Get narration duration
    try:
        probe_cmd = [
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(narration_file)
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        duration = float(result.stdout.strip()) if result.stdout.strip() else 600
    except Exception:
        duration = 600  # Default 10 minutes

    # Create video with solid background + narration
    # (B-roll overlay can be added when AI video gen models are configured)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=black:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:d={duration}:r={VIDEO_FPS}",
        "-i", str(narration_file),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(final_video)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        if result.returncode == 0 and final_video.exists():
            size_mb = final_video.stat().st_size / (1024 * 1024)
            print(f"  Video assembled: {final_video} ({size_mb:.1f} MB, {duration:.0f}s)")
            return str(final_video)
        else:
            print(f"  [ERROR] ffmpeg failed: {result.stderr[:200]}")
            return ""
    except subprocess.TimeoutExpired:
        print("  [ERROR] Assembly timed out after 30 minutes.")
        return ""


# ============================================================================
# AUTO-CLIPPING (long-form → shorts)
# ============================================================================

def clip_to_shorts(niche: str, topic: str, dry_run: bool = False) -> list:
    """Create 30-60 second vertical clips from long-form video."""
    output_dir = get_output_dir(niche, topic)
    final_video = output_dir / "final.mp4"
    shorts_dir = output_dir / "shorts"
    safe_path(shorts_dir)
    shorts_dir.mkdir(parents=True, exist_ok=True)

    if not final_video.exists():
        print(f"[ERROR] No video at {final_video}. Run --assemble first.")
        return []

    if dry_run:
        print(f"\n[DRY RUN] Would create shorts from: {final_video}")
        print(f"  Output dir: {shorts_dir}")
        return []

    print(f"\nClipping shorts from: {final_video}")

    # Get total duration
    try:
        probe_cmd = [
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(final_video)
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        total_duration = float(result.stdout.strip()) if result.stdout.strip() else 0
    except Exception:
        total_duration = 0

    if total_duration < 60:
        print("  Video too short for clips.")
        return []

    # Create clips at evenly spaced intervals
    clip_duration = 45  # seconds per short
    num_clips = min(5, int(total_duration / 120))  # One clip per 2 minutes, max 5

    clips = []
    for i in range(num_clips):
        start_time = int((total_duration / (num_clips + 1)) * (i + 1))
        clip_file = shorts_dir / f"short_{i + 1}.mp4"

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", str(final_video),
            "-t", str(clip_duration),
            "-vf", f"scale={SHORTS_WIDTH}:{SHORTS_HEIGHT}:force_original_aspect_ratio=decrease,"
                   f"pad={SHORTS_WIDTH}:{SHORTS_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            str(clip_file)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                clips.append(str(clip_file))
                print(f"  Created short #{i + 1}: {clip_file.name} (start: {start_time}s)")
        except Exception as e:
            print(f"  [ERROR] Failed to create clip #{i + 1}: {e}")

    print(f"\n{len(clips)} shorts created in: {shorts_dir}")
    return clips


# ============================================================================
# YOUTUBE UPLOAD
# ============================================================================

def upload_to_youtube(niche: str, topic: str, dry_run: bool = False) -> str:
    """Upload video to YouTube via Data API v3."""
    output_dir = get_output_dir(niche, topic)
    final_video = output_dir / "final.mp4"
    config = NICHE_CONFIG.get(niche, {})

    if not final_video.exists():
        print(f"[ERROR] No video at {final_video}. Run --assemble first.")
        return ""

    metadata = {
        "title": topic[:100],
        "description": f"{topic}\n\n{config.get('description', '')}\n\n"
                       f"Tags: {', '.join(config.get('tags', []))}\n\n"
                       f"---\nGenerated with PRINTMAXX YouTube Factory",
        "tags": config.get("tags", []),
        "categoryId": "28" if niche in ["tech", "comparison"] else "24",  # 28=Science&Tech, 24=Entertainment
        "privacyStatus": "public",
    }

    if dry_run:
        print(f"\n[DRY RUN] Would upload to YouTube:")
        print(f"  File: {final_video}")
        print(f"  Title: {metadata['title']}")
        print(f"  Tags: {metadata['tags']}")
        print(f"  Privacy: {metadata['privacyStatus']}")
        return ""

    if not YOUTUBE_CLIENT_SECRETS:
        print("[ERROR] YOUTUBE_CLIENT_SECRETS not set. Cannot upload.")
        print("  Get credentials from: https://console.cloud.google.com/apis/credentials")
        print("  Set YOUTUBE_CLIENT_SECRETS env var to the path of your client_secrets.json")
        return ""

    print(f"\nUploading to YouTube: {metadata['title']}")

    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google_auth_oauthlib.flow import InstalledAppFlow

        scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        flow = InstalledAppFlow.from_client_secrets_file(YOUTUBE_CLIENT_SECRETS, scopes)
        credentials = flow.run_local_server(port=0)
        youtube = build("youtube", "v3", credentials=credentials)

        body = {
            "snippet": {
                "title": metadata["title"],
                "description": metadata["description"],
                "tags": metadata["tags"],
                "categoryId": metadata["categoryId"],
            },
            "status": {
                "privacyStatus": metadata["privacyStatus"],
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(str(final_video), chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"  Upload progress: {int(status.progress() * 100)}%")

        video_id = response["id"]
        video_url = f"https://youtube.com/watch?v={video_id}"
        print(f"  Uploaded: {video_url}")

        # Save upload record
        record_file = output_dir / "upload_record.json"
        safe_path(record_file)
        with open(record_file, "w") as f:
            json.dump({"video_id": video_id, "url": video_url, "uploaded_at": datetime.now().isoformat(),
                        "metadata": metadata}, f, indent=2)

        return video_url

    except ImportError:
        print("[ERROR] google-api-python-client not installed.")
        print("  Run: pip3 install google-api-python-client google-auth-oauthlib")
        return ""
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return ""


# ============================================================================
# FULL PIPELINE
# ============================================================================

def run_full_pipeline(niche: str, topic: str, dry_run: bool = False):
    """Run complete pipeline: script → narrate → assemble → clip → upload."""
    print(f"\n{'='*60}")
    print(f"YOUTUBE FACTORY — FULL PIPELINE")
    print(f"Niche: {niche} | Topic: {topic}")
    print(f"Dry run: {dry_run}")
    print(f"{'='*60}")

    # Step 1: Generate script
    print(f"\n--- STEP 1/5: Script Generation ---")
    script = generate_script(niche, topic, dry_run)
    if not script and not dry_run:
        print("[ABORT] Script generation failed.")
        return

    # Step 2: Generate narration
    print(f"\n--- STEP 2/5: TTS Narration ---")
    narration = generate_narration(niche, topic, dry_run)
    if not narration and not dry_run:
        print("[ABORT] Narration generation failed.")
        return

    # Step 3: Assemble video
    print(f"\n--- STEP 3/5: Video Assembly ---")
    video = assemble_video(niche, topic, dry_run)
    if not video and not dry_run:
        print("[ABORT] Video assembly failed.")
        return

    # Step 4: Create shorts
    print(f"\n--- STEP 4/5: Auto-Clipping Shorts ---")
    shorts = clip_to_shorts(niche, topic, dry_run)

    # Step 5: Upload
    print(f"\n--- STEP 5/5: YouTube Upload ---")
    url = upload_to_youtube(niche, topic, dry_run)

    output_dir = get_output_dir(niche, topic)
    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE")
    print(f"  Output dir: {output_dir}")
    print(f"  Video: {'uploaded' if url else 'local only'}")
    print(f"  Shorts: {len(shorts)} clips created")
    if url:
        print(f"  YouTube URL: {url}")
    print(f"{'='*60}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX YouTube Content Factory")
    parser.add_argument("--niche", type=str, default="tech",
                        help=f"Content niche ({', '.join(NICHE_CONFIG.keys())})")
    parser.add_argument("--topic", type=str, default="",
                        help="Video topic/title")

    # Pipeline steps
    parser.add_argument("--generate-script", action="store_true", help="Generate video script")
    parser.add_argument("--narrate", action="store_true", help="Generate TTS narration")
    parser.add_argument("--generate-broll", action="store_true", help="Generate B-roll visuals")
    parser.add_argument("--assemble", action="store_true", help="Assemble final video")
    parser.add_argument("--clip", action="store_true", help="Create shorts from video")
    parser.add_argument("--upload", action="store_true", help="Upload to YouTube")
    parser.add_argument("--full-pipeline", action="store_true", help="Run complete pipeline")

    # Options
    parser.add_argument("--dry-run", action="store_true", help="Preview without executing")
    parser.add_argument("--list-niches", action="store_true", help="Show available niches")

    args = parser.parse_args()

    if args.list_niches:
        print("\n--- Available Niches ---")
        for name, config in NICHE_CONFIG.items():
            print(f"\n  {name}:")
            print(f"    Channel: {config['channel_name']}")
            print(f"    CPM: {config['cpm_estimate']}")
            print(f"    Target length: {config['target_length_minutes']} min")
            print(f"    Tags: {', '.join(config['tags'][:3])}")
        return

    if not any([args.generate_script, args.narrate, args.generate_broll, args.assemble,
                args.clip, args.upload, args.full_pipeline, args.list_niches]):
        parser.print_help()
        return

    if args.niche not in NICHE_CONFIG:
        print(f"[ERROR] Unknown niche: {args.niche}")
        print(f"  Available: {', '.join(NICHE_CONFIG.keys())}")
        return

    if args.full_pipeline:
        if not args.topic:
            print("[ERROR] --topic required for --full-pipeline")
            return
        run_full_pipeline(args.niche, args.topic, args.dry_run)
        return

    if args.generate_script:
        if not args.topic:
            print("[ERROR] --topic required for --generate-script")
            return
        generate_script(args.niche, args.topic, args.dry_run)

    if args.narrate:
        generate_narration(args.niche, args.topic, args.dry_run)

    if args.generate_broll:
        print("[INFO] B-roll generation requires local video models. See OPS/LOCAL_VIDEO_GEN_SETUP.md")

    if args.assemble:
        assemble_video(args.niche, args.topic, args.dry_run)

    if args.clip:
        clip_to_shorts(args.niche, args.topic, args.dry_run)

    if args.upload:
        upload_to_youtube(args.niche, args.topic, args.dry_run)


if __name__ == "__main__":
    main()
