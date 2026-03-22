#!/usr/bin/env python3
"""
Claude Video Editor — FFmpeg Auto-Edit Pipeline

Takes raw AI-generated video → adds captions (whisper) → hook text overlay →
CTA overlay → resize for platforms → optional background music → outputs to
video posting queue.

This is the [3] AUTO-EDITOR from VIDEO_AUTOPILOT_SPEC.md.
Primary: FFmpeg pipeline ($0, fully automated).
Secondary: Remotion (MEDIA/remotion/) for template-based branded content.

Usage:
    python3 claude_video_editor.py --edit INPUT.mp4 --platform tiktok
    python3 claude_video_editor.py --edit INPUT.mp4 --platform all --hook "Stop scrolling" --cta "Link in bio"
    python3 claude_video_editor.py --edit INPUT.mp4 --no-captions --music BGM.mp3
    python3 claude_video_editor.py --batch /path/to/raw_videos/
    python3 claude_video_editor.py --queue                        # Show video posting queue
    python3 claude_video_editor.py --status                       # Pipeline stats
"""

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# PATHS
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
MEDIA_DIR = PROJECT_ROOT / "MEDIA"
REMOTION_DIR = MEDIA_DIR / "remotion"
VIDEO_OUTPUT_DIR = MEDIA_DIR / "video_output"
VIDEO_RAW_DIR = MEDIA_DIR / "video_raw"
VIDEO_QUEUE_CSV = PROJECT_ROOT / "LEDGER" / "VIDEO_POSTING_QUEUE.csv"
VIDEO_EDIT_LOG = AUTOMATIONS_DIR / "logs" / "video_editor.log"
BGM_DIR = MEDIA_DIR / "bgm"
LOCK_FILE = AUTOMATIONS_DIR / ".video_editor.lock"
VIRAL_FORMATS_MD = PROJECT_ROOT / "10_RESEARCH" / "VIDEO_RESEARCH" / "templates" / "VIRAL_FORMATS.md"

# Ensure directories exist
for d in [VIDEO_OUTPUT_DIR, VIDEO_RAW_DIR, BGM_DIR, VIDEO_EDIT_LOG.parent]:
    d.mkdir(parents=True, exist_ok=True)


# ============================================================
# GUARDRAILS (required by guardrails.md)
# ============================================================

def safe_path(target) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved

# ============================================================
# QUEUE HEADERS
# ============================================================
QUEUE_HEADERS = [
    "video_id", "source_file", "edited_file", "platform", "hook_text",
    "cta_text", "has_captions", "has_music", "duration_sec", "resolution",
    "created_at", "status", "posted_at", "niche", "notes",
]

# ============================================================
# PLATFORM SPECS
# ============================================================
PLATFORM_SPECS = {
    "tiktok":    {"width": 1080, "height": 1920, "aspect": "9:16", "max_sec": 180, "suffix": "_tiktok"},
    "reels":     {"width": 1080, "height": 1920, "aspect": "9:16", "max_sec": 90,  "suffix": "_reels"},
    "shorts":    {"width": 1080, "height": 1920, "aspect": "9:16", "max_sec": 60,  "suffix": "_shorts"},
    "youtube":   {"width": 1920, "height": 1080, "aspect": "16:9", "max_sec": 600, "suffix": "_yt"},
    "square":    {"width": 1080, "height": 1080, "aspect": "1:1",  "max_sec": 60,  "suffix": "_sq"},
    "twitter":   {"width": 1280, "height": 720,  "aspect": "16:9", "max_sec": 140, "suffix": "_tw"},
}

# ============================================================
# CAPTION STYLES
# ============================================================
CAPTION_STYLES = {
    "default": "FontSize=22,Bold=1,Alignment=2,MarginV=40,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2",
    "bold":    "FontSize=28,Bold=1,Alignment=2,MarginV=40,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=3",
    "minimal": "FontSize=18,Bold=0,Alignment=2,MarginV=30,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=1",
    "impact":  "FontSize=32,Bold=1,Alignment=2,MarginV=50,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=3",
}

# ============================================================
# HELPERS
# ============================================================

def _log(msg: str):
    """Append to log file and print."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(VIDEO_EDIT_LOG, "a") as f:
        f.write(line + "\n")


def _run(cmd: list | str, timeout: int = 300) -> subprocess.CompletedProcess:
    """Run shell command with timeout."""
    if isinstance(cmd, str):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    else:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        _log(f"CMD FAILED: {cmd}")
        _log(f"STDERR: {result.stderr[:500]}")
    return result


def _check_tool(name: str) -> bool:
    """Check if a CLI tool is available."""
    return shutil.which(name) is not None


def _get_duration(video_path: str) -> float:
    """Get video duration in seconds via ffprobe."""
    result = _run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
    ])
    try:
        return float(result.stdout.strip())
    except (ValueError, AttributeError):
        return 0.0


def _get_resolution(video_path: str) -> tuple:
    """Get video width, height via ffprobe."""
    result = _run([
        "ffprobe", "-v", "quiet", "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0", str(video_path)
    ])
    try:
        parts = result.stdout.strip().split(",")
        return int(parts[0]), int(parts[1])
    except (ValueError, IndexError, AttributeError):
        return 0, 0


def _generate_video_id() -> str:
    """Generate a unique video ID."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    import random
    return f"vid_{ts}_{random.randint(1000,9999)}"


# ============================================================
# CORE PIPELINE STEPS
# ============================================================

def step_transcribe(video_path: str, output_dir: str) -> str | None:
    """Step 1: Transcribe video with whisper, output SRT."""
    if not _check_tool("whisper"):
        _log("WARNING: whisper not installed. Skipping captions. Install: pip3 install openai-whisper")
        return None

    srt_name = Path(video_path).stem + ".srt"
    srt_path = Path(output_dir) / srt_name

    _log(f"Transcribing: {video_path}")
    result = _run([
        "whisper", str(video_path),
        "--model", "small",
        "--output_format", "srt",
        "--output_dir", str(output_dir),
    ], timeout=600)

    if srt_path.exists():
        _log(f"SRT generated: {srt_path}")
        return str(srt_path)

    # whisper sometimes names output differently
    possible = list(Path(output_dir).glob(f"{Path(video_path).stem}*.srt"))
    if possible:
        _log(f"SRT found: {possible[0]}")
        return str(possible[0])

    _log("WARNING: No SRT file generated")
    return None


def _has_audio(video_path: str) -> bool:
    """Check if video has an audio stream."""
    result = _run([
        "ffprobe", "-v", "quiet", "-select_streams", "a",
        "-show_entries", "stream=codec_type",
        "-of", "csv=p=0", str(video_path)
    ])
    return bool(result.stdout.strip())


def _audio_args(video_path: str) -> list:
    """Return ffmpeg audio args: copy if audio exists, omit if not."""
    if _has_audio(video_path):
        return ["-c:a", "copy"]
    return ["-an"]


def step_burn_captions(video_path: str, srt_path: str, output_path: str,
                       style: str = "default") -> str | None:
    """Step 2: Burn SRT captions into video with ffmpeg.

    Uses symlink trick to avoid ffmpeg subtitle filter path escaping issues
    (colons, spaces, apostrophes in macOS paths break the subtitles= filter).
    """
    force_style = CAPTION_STYLES.get(style, CAPTION_STYLES["default"])

    # Symlink SRT to a simple path to avoid escaping hell
    import tempfile
    tmp_dir = tempfile.mkdtemp(prefix="vidsrt_")
    simple_srt = Path(tmp_dir) / "captions.srt"
    try:
        simple_srt.symlink_to(Path(srt_path).resolve())
    except OSError:
        shutil.copy2(srt_path, str(simple_srt))

    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", f"subtitles={simple_srt}:force_style='{force_style}'",
        *_audio_args(video_path),
        str(output_path),
    ]
    result = _run(cmd)

    # Cleanup temp
    simple_srt.unlink(missing_ok=True)
    Path(tmp_dir).rmdir()

    if Path(output_path).exists():
        return output_path
    return None


def step_hook_overlay(video_path: str, output_path: str, hook_text: str,
                      duration: float = 3.0) -> str | None:
    """Step 3: Add hook text overlay for first N seconds."""
    if not hook_text:
        return video_path  # passthrough

    # Wrap text if too long
    words = hook_text.split()
    lines = []
    line = []
    for w in words:
        line.append(w)
        if len(" ".join(line)) > 25:
            lines.append(" ".join(line))
            line = []
    if line:
        lines.append(" ".join(line))
    wrapped = "\\n".join(lines)

    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", (
            f"drawtext=text='{wrapped}':"
            f"fontsize=44:fontcolor=white:borderw=3:bordercolor=black:"
            f"x=(w-tw)/2:y=h/4:"
            f"enable='between(t,0,{duration})'"
        ),
        *_audio_args(video_path),
        str(output_path),
    ]
    result = _run(cmd)
    if Path(output_path).exists():
        return output_path
    return None


def step_cta_overlay(video_path: str, output_path: str, cta_text: str,
                     cta_duration: float = 3.0) -> str | None:
    """Step 4: Add CTA text overlay for last N seconds."""
    if not cta_text:
        return video_path  # passthrough

    total_dur = _get_duration(video_path)
    if total_dur <= 0:
        return video_path

    start_time = max(0, total_dur - cta_duration)

    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", (
            f"drawtext=text='{cta_text}':"
            f"fontsize=36:fontcolor=yellow:borderw=2:bordercolor=black:"
            f"x=(w-tw)/2:y=3*h/4:"
            f"enable='between(t,{start_time},{total_dur})'"
        ),
        *_audio_args(video_path),
        str(output_path),
    ]
    result = _run(cmd)
    if Path(output_path).exists():
        return output_path
    return None


def step_resize(video_path: str, output_path: str, platform: str) -> str | None:
    """Step 5: Resize/pad video for target platform."""
    spec = PLATFORM_SPECS.get(platform)
    if not spec:
        _log(f"Unknown platform: {platform}")
        return video_path

    w, h = spec["width"], spec["height"]
    max_sec = spec.get("max_sec", 600)

    # Auto-trim to platform max duration
    duration = _get_duration(video_path)
    trim_args = []
    if duration > max_sec:
        trim_args = ["-t", str(max_sec)]
        _log(f"  Auto-trimming {duration:.0f}s → {max_sec}s for {platform}")

    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        *trim_args,
        "-vf", (
            f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black"
        ),
        *_audio_args(video_path),
        str(output_path),
    ]
    result = _run(cmd)
    if Path(output_path).exists():
        return output_path
    return None


def step_add_music(video_path: str, output_path: str, music_path: str,
                   volume: float = 0.12) -> str | None:
    """Step 6: Mix background music at low volume."""
    if not music_path or not Path(music_path).exists():
        return video_path

    cmd = [
        "ffmpeg", "-y", "-i", str(video_path), "-i", str(music_path),
        "-filter_complex",
        f"[1:a]volume={volume}[bg];[0:a][bg]amix=inputs=2:duration=first",
        "-c:v", "copy",
        str(output_path),
    ]
    result = _run(cmd)
    if Path(output_path).exists():
        return output_path
    return None


# ============================================================
# FULL PIPELINE
# ============================================================

def edit_video(
    input_path: str,
    platforms: list[str] | None = None,
    hook_text: str = "",
    cta_text: str = "",
    music_path: str = "",
    caption_style: str = "default",
    skip_captions: bool = False,
    niche: str = "",
    notes: str = "",
) -> list[dict]:
    """
    Run the full FFmpeg auto-edit pipeline on a single video.
    Returns list of queue entries (one per platform).
    """
    if not _check_tool("ffmpeg"):
        _log("FATAL: ffmpeg not installed. Install: brew install ffmpeg")
        return []

    input_path = str(safe_path(input_path))
    if not Path(input_path).exists():
        _log(f"ERROR: Input file not found: {input_path}")
        return []

    # Auto-select BGM from BGM_DIR if no music specified
    if not music_path and BGM_DIR.exists():
        bgm_files = list(BGM_DIR.glob("*.mp3")) + list(BGM_DIR.glob("*.wav")) + list(BGM_DIR.glob("*.m4a"))
        if bgm_files:
            import random as _rnd
            music_path = str(_rnd.choice(bgm_files))
            _log(f"Auto-selected BGM: {Path(music_path).name}")

    if platforms is None:
        platforms = ["tiktok"]
    if "all" in platforms:
        platforms = list(PLATFORM_SPECS.keys())

    video_id = _generate_video_id()
    work_dir = VIDEO_OUTPUT_DIR / video_id
    work_dir.mkdir(parents=True, exist_ok=True)

    duration = _get_duration(input_path)
    src_w, src_h = _get_resolution(input_path)
    _log(f"Input: {input_path} ({src_w}x{src_h}, {duration:.1f}s)")

    # Track current working file through pipeline
    current = input_path

    # Step 1: Captions
    has_captions = False
    if not skip_captions:
        srt_path = step_transcribe(current, str(work_dir))
        if srt_path:
            captioned = str(work_dir / "captioned.mp4")
            result = step_burn_captions(current, srt_path, captioned, style=caption_style)
            if result:
                current = result
                has_captions = True

    # Step 2: Hook overlay
    if hook_text:
        hooked = str(work_dir / "hooked.mp4")
        result = step_hook_overlay(current, hooked, hook_text)
        if result and result != current:
            current = result

    # Step 3: CTA overlay
    if cta_text:
        ctad = str(work_dir / "cta.mp4")
        result = step_cta_overlay(current, ctad, cta_text)
        if result and result != current:
            current = result

    # Step 4-6: Per-platform resize + music + queue
    queue_entries = []
    for platform in platforms:
        spec = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["tiktok"])
        suffix = spec["suffix"]

        # Resize
        resized = str(work_dir / f"resized{suffix}.mp4")
        result = step_resize(current, resized, platform)
        platform_file = result if result and result != current else current

        # Music
        has_music = False
        if music_path:
            musicd = str(work_dir / f"final{suffix}.mp4")
            result = step_add_music(platform_file, musicd, music_path)
            if result and result != platform_file:
                platform_file = result
                has_music = True
        else:
            # Rename to final
            final_name = str(work_dir / f"final{suffix}.mp4")
            if platform_file != final_name:
                try:
                    shutil.copy2(platform_file, final_name)
                    platform_file = final_name
                except Exception:
                    pass

        final_dur = _get_duration(platform_file)
        final_w, final_h = _get_resolution(platform_file)

        entry = {
            "video_id": f"{video_id}{suffix}",
            "source_file": input_path,
            "edited_file": platform_file,
            "platform": platform,
            "hook_text": hook_text,
            "cta_text": cta_text,
            "has_captions": "yes" if has_captions else "no",
            "has_music": "yes" if has_music else "no",
            "duration_sec": f"{final_dur:.1f}",
            "resolution": f"{final_w}x{final_h}",
            "created_at": datetime.now().isoformat(),
            "status": "READY",
            "posted_at": "",
            "niche": niche,
            "notes": notes,
        }
        queue_entries.append(entry)
        _log(f"  {platform}: {platform_file} ({final_w}x{final_h}, {final_dur:.1f}s)")

    # Append to queue CSV
    _append_to_queue(queue_entries)

    _log(f"Pipeline complete: {video_id} -> {len(queue_entries)} platform versions")
    return queue_entries


def _append_to_queue(entries: list[dict]):
    """Append entries to VIDEO_POSTING_QUEUE.csv."""
    VIDEO_QUEUE_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = VIDEO_QUEUE_CSV.exists()

    with open(VIDEO_QUEUE_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=QUEUE_HEADERS)
        if not file_exists:
            writer.writeheader()
        for entry in entries:
            writer.writerow(entry)


# ============================================================
# BATCH MODE
# ============================================================

def batch_edit(input_dir: str, **kwargs) -> int:
    """Process all .mp4 files in a directory."""
    input_dir = Path(input_dir)
    if not input_dir.exists():
        _log(f"ERROR: Directory not found: {input_dir}")
        return 0

    videos = sorted(input_dir.glob("*.mp4"))
    if not videos:
        _log(f"No .mp4 files found in {input_dir}")
        return 0

    _log(f"Batch editing {len(videos)} videos from {input_dir}")
    total = 0
    for i, vid in enumerate(videos, 1):
        _log(f"[{i}/{len(videos)}] {vid.name}")
        entries = edit_video(str(vid), **kwargs)
        total += len(entries)

    _log(f"Batch complete: {total} platform versions from {len(videos)} source videos")
    return total


# ============================================================
# QUEUE MANAGEMENT
# ============================================================

def show_queue():
    """Display the video posting queue."""
    if not VIDEO_QUEUE_CSV.exists():
        print("No video posting queue found. Run --edit to generate videos.")
        return

    with open(VIDEO_QUEUE_CSV, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("Video posting queue is empty.")
        return

    # Count by status
    by_status = {}
    by_platform = {}
    for r in rows:
        s = r.get("status", "UNKNOWN")
        p = r.get("platform", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
        by_platform[p] = by_platform.get(p, 0) + 1

    print(f"\n{'='*60}")
    print(f"VIDEO POSTING QUEUE")
    print(f"{'='*60}")
    print(f"Total videos: {len(rows)}")
    print(f"\nBy status:")
    for s, c in sorted(by_status.items()):
        print(f"  {s}: {c}")
    print(f"\nBy platform:")
    for p, c in sorted(by_platform.items()):
        print(f"  {p}: {c}")

    # Show recent READY entries
    ready = [r for r in rows if r.get("status") == "READY"]
    if ready:
        print(f"\nReady to post ({len(ready)}):")
        for r in ready[-10:]:
            hook = r.get("hook_text", "")[:30]
            print(f"  {r['video_id']:30s} | {r['platform']:8s} | {r['duration_sec']:5s}s | {hook}")
    print(f"{'='*60}\n")


def show_status():
    """Show pipeline status."""
    print(f"\n{'='*60}")
    print(f"VIDEO EDITOR PIPELINE STATUS")
    print(f"{'='*60}")

    # Check tools
    tools = {"ffmpeg": _check_tool("ffmpeg"), "whisper": _check_tool("whisper"), "ffprobe": _check_tool("ffprobe")}
    print(f"\nTools:")
    for t, ok in tools.items():
        print(f"  {'OK' if ok else 'MISSING':8s} {t}")

    # Check directories
    print(f"\nDirectories:")
    for name, path in [("raw input", VIDEO_RAW_DIR), ("output", VIDEO_OUTPUT_DIR), ("bgm", BGM_DIR), ("remotion", REMOTION_DIR)]:
        exists = path.exists()
        count = len(list(path.iterdir())) if exists else 0
        print(f"  {'OK' if exists else 'MISSING':8s} {name}: {path} ({count} items)")

    # Queue stats
    if VIDEO_QUEUE_CSV.exists():
        with open(VIDEO_QUEUE_CSV, "r") as f:
            rows = list(csv.DictReader(f))
        ready = sum(1 for r in rows if r.get("status") == "READY")
        posted = sum(1 for r in rows if r.get("status") == "POSTED")
        print(f"\nQueue: {len(rows)} total, {ready} ready, {posted} posted")
    else:
        print(f"\nQueue: not created yet")

    print(f"\nQueue CSV: {VIDEO_QUEUE_CSV}")
    print(f"Log: {VIDEO_EDIT_LOG}")
    print(f"{'='*60}\n")


# ============================================================
# REMOTION INTEGRATION
# ============================================================

def render_remotion(comp: str, props: dict, output_path: str = "") -> str | None:
    """Render a Remotion composition. Delegates to MEDIA/remotion/render.py."""
    render_script = REMOTION_DIR / "render.py"
    if not render_script.exists():
        _log(f"WARNING: Remotion render.py not found at {render_script}")
        return None

    props_json = json.dumps(props)
    cmd = ["python3", str(render_script), "--comp", comp, "--props", props_json]
    if output_path:
        cmd.extend(["--output", output_path])

    result = _run(cmd, timeout=120)
    if result.returncode == 0:
        # Parse output path from render.py stdout
        for line in result.stdout.strip().split("\n"):
            if line.strip().endswith(".mp4") or line.strip().endswith(".webm"):
                return line.strip()
    return None


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Claude Video Editor - FFmpeg auto-edit pipeline for AI video content"
    )
    parser.add_argument("--edit", metavar="FILE", help="Edit a single video file")
    parser.add_argument("--batch", metavar="DIR", help="Batch edit all .mp4 files in directory")
    parser.add_argument("--platform", default="tiktok",
                        help="Target platform(s): tiktok,reels,shorts,youtube,square,twitter,all (comma-sep)")
    parser.add_argument("--hook", default="", help="Hook text overlay (first 3 seconds)")
    parser.add_argument("--cta", default="", help="CTA text overlay (last 3 seconds)")
    parser.add_argument("--music", default="", help="Path to background music file")
    parser.add_argument("--no-captions", action="store_true", help="Skip whisper caption generation")
    parser.add_argument("--caption-style", default="default",
                        choices=list(CAPTION_STYLES.keys()), help="Caption style preset")
    parser.add_argument("--niche", default="", help="Content niche (for queue tracking)")
    parser.add_argument("--notes", default="", help="Notes (for queue tracking)")
    parser.add_argument("--queue", action="store_true", help="Show video posting queue")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--remotion", metavar="COMP", help="Render a Remotion composition instead")
    parser.add_argument("--props", default="{}", help="JSON props for Remotion render")

    args = parser.parse_args()

    if not any([args.edit, args.batch, args.queue, args.status, args.remotion]):
        parser.print_help()
        print("\nExamples:")
        print("  python3 claude_video_editor.py --edit raw.mp4 --platform tiktok --hook 'Stop scrolling'")
        print("  python3 claude_video_editor.py --edit raw.mp4 --platform all --cta 'Link in bio'")
        print("  python3 claude_video_editor.py --batch MEDIA/video_raw/ --platform tiktok,reels")
        print("  python3 claude_video_editor.py --remotion SocialHook --props '{\"hookText\":\"Big news\"}'")
        print("  python3 claude_video_editor.py --queue")
        print("  python3 claude_video_editor.py --status")
        return

    if args.status:
        show_status()
        return

    if args.queue:
        show_queue()
        return

    if args.remotion:
        props = json.loads(args.props)
        output = render_remotion(args.remotion, props)
        if output:
            _log(f"Remotion render complete: {output}")
            # Optionally run through FFmpeg pipeline
            if args.platform != "tiktok" or args.hook or args.cta or args.music:
                platforms = [p.strip() for p in args.platform.split(",")]
                edit_video(output, platforms=platforms, hook_text=args.hook,
                          cta_text=args.cta, music_path=args.music,
                          niche=args.niche, notes=args.notes)
        else:
            _log("Remotion render failed")
        return

    platforms = [p.strip() for p in args.platform.split(",")]

    if args.edit:
        edit_video(
            args.edit,
            platforms=platforms,
            hook_text=args.hook,
            cta_text=args.cta,
            music_path=args.music,
            caption_style=args.caption_style,
            skip_captions=args.no_captions,
            niche=args.niche,
            notes=args.notes,
        )
        return

    if args.batch:
        batch_edit(
            args.batch,
            platforms=platforms,
            hook_text=args.hook,
            cta_text=args.cta,
            music_path=args.music,
            caption_style=args.caption_style,
            skip_captions=args.no_captions,
            niche=args.niche,
            notes=args.notes,
        )
        return


if __name__ == "__main__":
    main()
