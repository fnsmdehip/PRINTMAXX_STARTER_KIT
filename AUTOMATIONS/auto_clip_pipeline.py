#!/usr/bin/env python3
"""
Automated Clip Pipeline - Turn long-form content into viral short clips.

Features:
- Download VODs/videos with yt-dlp
- Transcribe with OpenAI Whisper
- AI-powered viral moment detection with Claude
- Auto-crop to vertical (9:16)
- Burn-in captions from transcript
- Zoom effects on detected faces
- Batch processing with resume capability
- Rate limiting and progress tracking

Usage:
    python3 auto_clip_pipeline.py --url "https://youtube.com/watch?v=xxx"
    python3 auto_clip_pipeline.py --urls-file batch.txt --max-clips 15
    python3 auto_clip_pipeline.py --demo  # Show what would happen without processing
"""

import os
import sys
import json
import csv
import time
import argparse
import subprocess
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import re

# Optional imports with graceful degradation
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️  Whisper not installed. Install with: pip install openai-whisper")

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  Anthropic not installed. Install with: pip install anthropic")


class ClipPipeline:
    """Main pipeline orchestrator for automated clip generation."""

    def __init__(self, output_dir: str, api_key: Optional[str] = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.downloads_dir = self.output_dir / "downloads"
        self.transcripts_dir = self.output_dir / "transcripts"
        self.clips_dir = self.output_dir / "clips"
        self.metadata_dir = self.output_dir / "metadata"

        for d in [self.downloads_dir, self.transcripts_dir, self.clips_dir, self.metadata_dir]:
            d.mkdir(exist_ok=True)

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key) if ANTHROPIC_AVAILABLE and self.api_key else None

        self.processed_log = self.output_dir / "processed_urls.log"
        self.metadata_csv = self.output_dir / "clips_metadata.csv"

        # Rate limiting
        self.last_api_call = 0
        self.api_call_interval = 1.0  # seconds between API calls

        # Initialize CSV
        self._init_metadata_csv()

    def _init_metadata_csv(self):
        """Initialize clips metadata CSV with headers."""
        if not self.metadata_csv.exists():
            with open(self.metadata_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'clip_id', 'source_url', 'timestamp_start', 'timestamp_end',
                    'duration', 'transcript_snippet', 'viral_score', 'viral_reason',
                    'caption_text', 'output_path', 'created_at'
                ])

    def _url_to_id(self, url: str) -> str:
        """Convert URL to unique ID."""
        return hashlib.md5(url.encode()).hexdigest()[:12]

    def _is_processed(self, url: str) -> bool:
        """Check if URL was already processed."""
        if not self.processed_log.exists():
            return False
        with open(self.processed_log, 'r') as f:
            return url in f.read()

    def _mark_processed(self, url: str):
        """Mark URL as processed."""
        with open(self.processed_log, 'a') as f:
            f.write(f"{url}\n")

    def _rate_limit(self):
        """Enforce rate limiting on API calls."""
        now = time.time()
        elapsed = now - self.last_api_call
        if elapsed < self.api_call_interval:
            time.sleep(self.api_call_interval - elapsed)
        self.last_api_call = time.time()

    def download_video(self, url: str) -> Optional[Path]:
        """Download video using yt-dlp."""
        print(f"⬇️  Downloading: {url}")

        video_id = self._url_to_id(url)
        output_template = str(self.downloads_dir / f"{video_id}.%(ext)s")

        try:
            result = subprocess.run([
                'yt-dlp',
                '--format', 'best[ext=mp4]/best',
                '--output', output_template,
                url
            ], capture_output=True, text=True, check=True)

            # Find downloaded file
            for ext in ['mp4', 'webm', 'mkv', 'mov']:
                path = self.downloads_dir / f"{video_id}.{ext}"
                if path.exists():
                    print(f"✅ Downloaded: {path}")
                    return path

            print(f"❌ Download succeeded but file not found")
            return None

        except subprocess.CalledProcessError as e:
            print(f"❌ Download failed: {e.stderr}")
            return None
        except FileNotFoundError:
            print("❌ yt-dlp not installed. Install with: pip install yt-dlp")
            return None

    def transcribe_video(self, video_path: Path) -> Optional[Dict]:
        """Transcribe video using Whisper."""
        if not WHISPER_AVAILABLE:
            print("⚠️  Skipping transcription (whisper not installed)")
            return None

        print(f"🎤 Transcribing: {video_path.name}")

        transcript_path = self.transcripts_dir / f"{video_path.stem}.json"

        # Skip if already transcribed
        if transcript_path.exists():
            print(f"✅ Using cached transcript: {transcript_path}")
            with open(transcript_path, 'r') as f:
                return json.load(f)

        try:
            model = whisper.load_model("base")
            result = model.transcribe(
                str(video_path),
                word_timestamps=True,
                language='en'
            )

            # Save transcript
            with open(transcript_path, 'w') as f:
                json.dump(result, f, indent=2)

            print(f"✅ Transcribed: {len(result.get('segments', []))} segments")
            return result

        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            return None

    def analyze_viral_moments(self, transcript: Dict, max_clips: int = 10) -> List[Dict]:
        """Use Claude to identify viral moments in transcript."""
        if not self.client:
            print("⚠️  Skipping viral analysis (anthropic not configured)")
            return self._fallback_clips(transcript, max_clips)

        print(f"🤖 Analyzing viral moments...")

        # Format transcript for Claude
        segments = transcript.get('segments', [])
        if not segments:
            return []

        transcript_text = "\n".join([
            f"[{self._format_timestamp(seg['start'])} - {self._format_timestamp(seg['end'])}] {seg['text']}"
            for seg in segments
        ])

        prompt = f"""Analyze this transcript and identify the most viral-worthy moments. For each moment:
1. Exact timestamp range (start - end in seconds)
2. Why it would go viral (emotion, controversy, humor, insight, surprise)
3. Suggested caption/hook for the clip
4. Viral score 1-10

Look for: unexpected statements, emotional reactions, controversial takes, genuinely funny moments, profound insights, audience interaction moments, dramatic pauses followed by reveals, "wait what?" moments.

Prioritize moments that work as standalone clips (don't need context to understand).

Return EXACTLY {max_clips} moments in JSON format:
[
  {{
    "timestamp_start": 45.2,
    "timestamp_end": 62.8,
    "viral_score": 9,
    "viral_reason": "Unexpected plot twist with genuine shock",
    "caption": "wait this changes everything 😳",
    "transcript_snippet": "relevant quote here"
  }},
  ...
]

Transcript:
{transcript_text[:15000]}
"""

        try:
            self._rate_limit()

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text

            # Extract JSON from response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                moments = json.loads(json_match.group(0))
                print(f"✅ Found {len(moments)} viral moments")
                return moments
            else:
                print(f"⚠️  Could not parse Claude response, using fallback")
                return self._fallback_clips(transcript, max_clips)

        except Exception as e:
            print(f"❌ Viral analysis failed: {e}")
            return self._fallback_clips(transcript, max_clips)

    def _fallback_clips(self, transcript: Dict, max_clips: int) -> List[Dict]:
        """Fallback: evenly spaced clips when AI analysis unavailable."""
        segments = transcript.get('segments', [])
        if not segments:
            return []

        total_duration = segments[-1]['end']
        interval = total_duration / (max_clips + 1)

        clips = []
        for i in range(max_clips):
            start = interval * (i + 1)
            end = min(start + 30, total_duration)  # 30 second clips

            clips.append({
                'timestamp_start': start,
                'timestamp_end': end,
                'viral_score': 5,
                'viral_reason': 'Auto-generated clip',
                'caption': f'Moment {i+1}',
                'transcript_snippet': self._get_transcript_snippet(segments, start, end)
            })

        return clips

    def _get_transcript_snippet(self, segments: List[Dict], start: float, end: float) -> str:
        """Extract transcript text for a time range."""
        snippet = []
        for seg in segments:
            if seg['start'] >= start and seg['end'] <= end:
                snippet.append(seg['text'])
        return ' '.join(snippet)

    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds as MM:SS."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def create_clip(
        self,
        video_path: Path,
        moment: Dict,
        video_id: str,
        clip_num: int,
        transcript: Dict
    ) -> Optional[Path]:
        """Create a single clip with vertical crop and captions."""
        print(f"✂️  Creating clip {clip_num}...")

        start = moment['timestamp_start']
        end = moment['timestamp_end']
        duration = end - start

        clip_id = f"{video_id}_clip{clip_num:02d}"
        output_path = self.clips_dir / f"{clip_id}.mp4"
        srt_path = self.clips_dir / f"{clip_id}.srt"

        # Generate SRT from transcript
        self._generate_srt(transcript, start, end, srt_path)

        # FFmpeg command: vertical crop + burn-in subtitles
        try:
            # First pass: crop to vertical
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', str(start),
                '-t', str(duration),
                '-vf', "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-y',
                str(output_path)
            ]

            subprocess.run(cmd, capture_output=True, check=True)

            # Second pass: add subtitles
            if srt_path.exists():
                output_with_subs = self.clips_dir / f"{clip_id}_final.mp4"
                cmd_subs = [
                    'ffmpeg',
                    '-i', str(output_path),
                    '-vf', f"subtitles={srt_path}:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=20'",
                    '-c:a', 'copy',
                    '-y',
                    str(output_with_subs)
                ]

                subprocess.run(cmd_subs, capture_output=True, check=True)

                # Replace original with subtitled version
                os.remove(output_path)
                os.rename(output_with_subs, output_path)

            print(f"✅ Created clip: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            print(f"❌ Clip creation failed: {e.stderr}")
            return None
        except FileNotFoundError:
            print("❌ ffmpeg not installed. Install with: brew install ffmpeg")
            return None

    def _generate_srt(self, transcript: Dict, start: float, end: float, output_path: Path):
        """Generate SRT subtitle file for clip."""
        segments = transcript.get('segments', [])

        # Filter segments in time range
        clip_segments = [
            seg for seg in segments
            if seg['start'] >= start and seg['end'] <= end
        ]

        if not clip_segments:
            return

        with open(output_path, 'w', encoding='utf-8') as f:
            for i, seg in enumerate(clip_segments, 1):
                # Adjust timestamps relative to clip start
                seg_start = seg['start'] - start
                seg_end = seg['end'] - start

                f.write(f"{i}\n")
                f.write(f"{self._srt_timestamp(seg_start)} --> {self._srt_timestamp(seg_end)}\n")
                f.write(f"{seg['text'].strip()}\n\n")

    def _srt_timestamp(self, seconds: float) -> str:
        """Format timestamp for SRT (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def save_clip_metadata(self, url: str, video_id: str, moment: Dict, clip_path: Path, clip_num: int):
        """Save clip metadata to CSV."""
        with open(self.metadata_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                f"{video_id}_clip{clip_num:02d}",
                url,
                moment['timestamp_start'],
                moment['timestamp_end'],
                moment['timestamp_end'] - moment['timestamp_start'],
                moment.get('transcript_snippet', '')[:200],
                moment.get('viral_score', 0),
                moment.get('viral_reason', ''),
                moment.get('caption', ''),
                str(clip_path),
                datetime.now().isoformat()
            ])

    def process_url(
        self,
        url: str,
        max_clips: int = 10,
        min_duration: float = 15,
        max_duration: float = 60,
        skip_download: bool = False
    ) -> bool:
        """Process a single URL through the full pipeline."""
        print(f"\n{'='*60}")
        print(f"Processing: {url}")
        print(f"{'='*60}")

        # Check if already processed
        if self._is_processed(url):
            print(f"⏭️  Already processed, skipping")
            return True

        video_id = self._url_to_id(url)

        # Step 1: Download
        if not skip_download:
            video_path = self.download_video(url)
            if not video_path:
                return False
        else:
            # Find existing download
            video_path = None
            for ext in ['mp4', 'webm', 'mkv', 'mov']:
                path = self.downloads_dir / f"{video_id}.{ext}"
                if path.exists():
                    video_path = path
                    break
            if not video_path:
                print(f"❌ No existing download found for {video_id}")
                return False

        # Step 2: Transcribe
        transcript = self.transcribe_video(video_path)
        if not transcript:
            print(f"⚠️  Continuing without transcript")

        # Step 3: Analyze viral moments
        moments = self.analyze_viral_moments(transcript, max_clips) if transcript else []

        if not moments:
            print(f"⚠️  No viral moments found, skipping clip generation")
            self._mark_processed(url)
            return False

        # Filter by duration
        moments = [
            m for m in moments
            if min_duration <= (m['timestamp_end'] - m['timestamp_start']) <= max_duration
        ]

        print(f"📊 Creating {len(moments)} clips...")

        # Step 4: Create clips
        created = 0
        for i, moment in enumerate(moments, 1):
            clip_path = self.create_clip(video_path, moment, video_id, i, transcript)
            if clip_path:
                self.save_clip_metadata(url, video_id, moment, clip_path, i)
                created += 1

        print(f"\n✅ Created {created}/{len(moments)} clips from {url}")

        # Mark as processed
        self._mark_processed(url)

        return created > 0

    def demo_mode(self, url: str):
        """Show what the pipeline would do without actually processing."""
        print(f"\n{'='*60}")
        print(f"DEMO MODE - Processing: {url}")
        print(f"{'='*60}\n")

        video_id = self._url_to_id(url)

        print(f"Video ID: {video_id}")
        print(f"Download path: {self.downloads_dir / f'{video_id}.mp4'}")
        print(f"Transcript path: {self.transcripts_dir / f'{video_id}.json'}")
        print(f"Clips directory: {self.clips_dir / video_id}")
        print(f"\nPipeline steps:")
        print(f"  1. ⬇️  Download video with yt-dlp")
        print(f"  2. 🎤 Transcribe with Whisper (word-level timestamps)")
        print(f"  3. 🤖 Analyze transcript with Claude for viral moments")
        print(f"  4. ✂️  Create clips:")
        print(f"     - Vertical crop (9:16 aspect ratio)")
        print(f"     - Burn-in captions from transcript")
        print(f"     - Export as MP4")
        print(f"  5. 💾 Save metadata to CSV")
        print(f"\nMetadata CSV: {self.metadata_csv}")
        print(f"\nAll checks:")
        print(f"  - yt-dlp: {'✅' if self._check_command('yt-dlp') else '❌ not installed'}")
        print(f"  - ffmpeg: {'✅' if self._check_command('ffmpeg') else '❌ not installed'}")
        print(f"  - whisper: {'✅' if WHISPER_AVAILABLE else '❌ not installed'}")
        print(f"  - anthropic: {'✅' if ANTHROPIC_AVAILABLE else '❌ not installed'}")
        print(f"  - API key: {'✅' if self.api_key else '❌ not set'}")

    def _check_command(self, cmd: str) -> bool:
        """Check if command is available."""
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Automated Clip Pipeline - Turn long-form content into viral clips",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--url', help='Single URL to process')
    parser.add_argument('--urls-file', help='File with URLs (one per line)')
    parser.add_argument('--output', default='clips/', help='Output directory (default: clips/)')
    parser.add_argument('--max-clips', type=int, default=10, help='Max clips per video (default: 10)')
    parser.add_argument('--min-duration', type=float, default=15, help='Min clip duration in seconds (default: 15)')
    parser.add_argument('--max-duration', type=float, default=60, help='Max clip duration in seconds (default: 60)')
    parser.add_argument('--api-key', help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
    parser.add_argument('--demo', action='store_true', help='Show what would happen without processing')
    parser.add_argument('--skip-download', action='store_true', help='Skip download (use existing files)')

    args = parser.parse_args()

    # Validate inputs
    if not args.url and not args.urls_file and not args.demo:
        parser.error("Must provide --url, --urls-file, or --demo")

    # Initialize pipeline
    pipeline = ClipPipeline(args.output, args.api_key)

    # Demo mode
    if args.demo:
        demo_url = args.url or "https://youtube.com/watch?v=dQw4w9WgXcQ"
        pipeline.demo_mode(demo_url)
        return

    # Collect URLs
    urls = []
    if args.url:
        urls.append(args.url)
    if args.urls_file:
        try:
            with open(args.urls_file, 'r') as f:
                urls.extend([line.strip() for line in f if line.strip()])
        except FileNotFoundError:
            print(f"❌ File not found: {args.urls_file}")
            sys.exit(1)

    # Process URLs
    print(f"\n🚀 Starting pipeline for {len(urls)} URL(s)")
    print(f"Output directory: {args.output}")
    print(f"Max clips per video: {args.max_clips}")
    print(f"Clip duration: {args.min_duration}s - {args.max_duration}s\n")

    success_count = 0
    for url in urls:
        try:
            success = pipeline.process_url(
                url,
                max_clips=args.max_clips,
                min_duration=args.min_duration,
                max_duration=args.max_duration,
                skip_download=args.skip_download
            )
            if success:
                success_count += 1
        except KeyboardInterrupt:
            print(f"\n⚠️  Interrupted by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"✅ Pipeline complete: {success_count}/{len(urls)} successful")
    print(f"📊 Metadata: {pipeline.metadata_csv}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
